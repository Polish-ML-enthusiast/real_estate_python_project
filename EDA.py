import os
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import matplotlib.ticker as ticker

def get_processed_data():
    df = pd.read_csv('data/apartments_pl_2024_04.csv', encoding='ISO-8859-1')
    
    df = df[df['city'].str.capitalize() == 'Wroclaw']
    
    df.drop(columns=['id', 'schoolDistance', 'clinicDistance', 'kindergartenDistance', 'restaurantDistance', 'collegeDistance',
                     'pharmacyDistance', 'postOfficeDistance'], inplace=True)

    floor_median = df['floor'].median()
    floorCount_median = df['floorCount'].median()
    buildYear_median = df['buildYear'].median()
    df['floor'].fillna(floor_median, inplace=True)
    df['floorCount'].fillna(floorCount_median, inplace=True)
    df['buildYear'].fillna(buildYear_median, inplace=True)
    df['hasElevator'].fillna('yes', inplace=True)

    df['city'] = df['city'].str.capitalize()

    df['price1m2'] = df['price'] / df['squareMeters']
    df['price1m2'] = df['price1m2'].astype(float)

    columns_yes_no = ['hasParkingSpace', 'hasBalcony', 'hasSecurity', 'hasStorageRoom', 'hasElevator']
    df = pd.get_dummies(df, columns=columns_yes_no, drop_first=True, prefix=columns_yes_no, dtype=int)

    if 'rooms' in df.columns:
        df['rooms'] = df['rooms'].astype('int32')
    if 'floor' in df.columns:
        df['floor'] = df['floor'].astype('int32')
    if 'buildYear' in df.columns:
        df['buildYear'] = df['buildYear'].astype('int32')

    pd.set_option('display.float_format', '{:.2f}'.format)

    return df

def get_neighborhood_boundaries():
    shapefile_path = "data/GraniceOsiedli.shp"
    if not os.path.exists(shapefile_path):
        st.error(f"Plik {shapefile_path} nie istnieje. Upewnij się, że plik jest w odpowiednim miejscu.")
        return gpd.GeoDataFrame()

    try:
        neighborhoods = gpd.read_file(shapefile_path)
        neighborhoods = neighborhoods.to_crs(epsg=4326)  # Konwersja do układu współrzędnych WGS84
        st.write("Kolumny w pliku shapefile:", neighborhoods.columns)
        st.write(neighborhoods.head())  # Wyświetlenie kilku wierszy danych
        return neighborhoods
    except Exception as e:
        st.error(f"Nie udało się załadować pliku shapefile: {e}")
        return gpd.GeoDataFrame()

def app():
    st.title('📈 Exploratory Data Analysis (EDA) 📊 - Nieruchomości we Wrocławiu')
    
    df = get_processed_data()  # Załadowanie przetworzonych danych
    neighborhoods = get_neighborhood_boundaries()  # Załadowanie granic osiedli

    if neighborhoods.empty:
        st.error("Nie udało się załadować granic osiedli. Sprawdź poprawność plików shapefile.")

    # Obliczanie statystyk
    st.header('Statystyki cenowe dla miasta Wrocław 🔢')
    stats = {
        'Liczba ofert': len(df),
        'Średnia cena za m²': df['price1m2'].mean(),
        'Mediana ceny za m²': df['price1m2'].median(),
        'Cena minimalna za m²': df['price1m2'].min(),
        'Cena maksymalna za m²': df['price1m2'].max(),
        'Odchylenie standardowe ceny za m²': df['price1m2'].std()
    }

    stats_df = pd.DataFrame.from_dict(stats, orient='index', columns=['Wartość'])
    stats_df = stats_df.style.format("{:.2f}")
   
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.table(stats_df)

    show_button = st.button('Pokaż dane')
    hide_button = st.button('Schowaj dane')

    if show_button:
        st.session_state['show_data'] = True
    if hide_button:
        st.session_state['show_data'] = False

    if st.session_state.get('show_data', False):
        df_display = df.drop(columns='city')
        df['price1m2'] = df['price1m2'].astype(float)
        st.dataframe(df_display.style.format("{:.2f}"))

    st.subheader('Histogram ceny za metr kwadratowy - Wrocław')
    fig, ax = plt.subplots()
    sns.histplot(df['price1m2'], bins=30, kde=True, color='skyblue', ax=ax)
    ax.set_title('Rozkład ceny za metr kwadratowy')
    ax.set_xlabel('Cena za m²')
    ax.set_ylabel('Ilość ofert')
    st.pyplot(fig)

    st.subheader('Macierz korelacji 🔗cech mieszkania na przykładzie miasta Wrocław')
    correlation_matrix = df[['price1m2', 'squareMeters', 'floor', 'floorCount', 'buildYear', 'centreDistance']].corr()
    fig, ax = plt.subplots()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(correlation_matrix, annot=True, cmap='Oranges', ax=ax, mask=mask,
                xticklabels=['Cena za m²', 'Powierzchnia m²', 'Piętro', 'Liczba pięter', 'Rok budowy', 'Odległość od centrum w km'],
                yticklabels=['Cena za m²', 'Powierzchnia m²', 'Piętro', 'Liczba pięter', 'Rok budowy', 'Odległość od centrum w km'])
    ax.set_title('Macierz korelacji')
    st.pyplot(fig)

    st.subheader('Mapa lokalizacji nieruchomości 🗺️')
    if 'latitude' in df.columns and 'longitude' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        sc = ax.scatter(df['longitude'], df['latitude'], c=df['price1m2'], cmap='Oranges', alpha=0.6)
        fig.colorbar(sc, label='Cena za m²')
        ax.set_xlabel('Długość geograficzna')
        ax.set_ylabel('Szerokość geograficzna')
        ax.set_title('Mapa cenowa nieruchomości w Wrocławiu')
        st.pyplot(fig)
    else:
        st.error('Brak danych geograficznych dla miasta Wrocław.')

    st.subheader('Mapa lokalizacji nieruchomości w Wrocławiu 📍')
    map_data = df.dropna(subset=['latitude', 'longitude'])
    if not map_data.empty:
        map_center = [map_data['latitude'].mean(), map_data['longitude'].mean()]
        folium_map = folium.Map(location=map_center, zoom_start=13, control_scale=True)
        for _, row in map_data.iterrows():
            color = plt.cm.YlOrRd((row['price1m2'] - map_data['price1m2'].min()) / (map_data['price1m2'].max() - map_data['price1m2'].min()))
            folium.CircleMarker(location=[row['latitude'], row['longitude']],
                                radius=5,
                                weight=1,
                                color=mcolors.to_hex(color),
                                fill_color=mcolors.to_hex(color),
                                fill=True,
                                fill_opacity=0.7,
                                popup=f"Cena za m²: {float(row['price1m2']):.2f}").add_to(folium_map)
        folium_static(folium_map)
    else:
        st.error('Brak danych geograficznych dla miasta Wrocław.')

    # Nowa mapa z medianami cen na osiedlach
    st.subheader('Mapa osiedli Wrocławia z medianami cen')
    if not map_data.empty and not neighborhoods.empty:
        map_center = [map_data['latitude'].mean(), map_data['longitude'].mean()]
        neighborhood_map = folium.Map(location=map_center, zoom_start=13, control_scale=True)

        folium.GeoJson(neighborhoods, name="Osiedla").add_to(neighborhood_map)

        # Oblicz mediany cen dla każdego osiedla
        df_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
        joined = gpd.sjoin(df_gdf, neighborhoods, how="inner", op='within')
        st.write("Kolumny połączonego GeoDataFrame:", joined.columns)
        st.write(joined.head())

        if 'NAZWAOSIED,C,50' not in joined.columns:
            st.error("Kolumna 'NAZWAOSIED,C,50' nie istnieje w połączonym GeoDataFrame.")
        else:
            median_prices = joined.groupby('NAZWAOSIED,C,50')['price1m2'].median().reset_index()

            for _, row in median_prices.iterrows():
                neighborhood = neighborhoods[neighborhoods['NAZWAOSIED,C,50'] == row['NAZWAOSIED,C,50']]
                centroid = neighborhood.geometry.centroid.iloc[0]
                folium.Marker(
                    location=[centroid.y, centroid.x],
                    popup=f"{row['NAZWAOSIED,C,50']}: {row['price1m2']:.2f} zł/m²",
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(neighborhood_map)

            folium_static(neighborhood_map)
    else:
        st.error('Brak danych geograficznych dla miasta Wrocław lub nie udało się załadować granic osiedli.')

    st.subheader('Wykresy Kernel Density Estimate (KDE) na przykładzie miasta Wrocław')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    binary_columns_yes = ['hasParkingSpace_yes', 'hasBalcony_yes', 'hasSecurity_yes', 'hasStorageRoom_yes', 'hasElevator_yes']

    for col in binary_columns_yes:
        if col in df.columns:
            df[col] = df[col].astype('category')

    df['price'] /= 1000

    plt.figure(figsize=(18, 16))

    for i, column in enumerate(binary_columns_yes, 1):
        ax = plt.subplot(3, 2, i)
        if column in df.columns:
            sns.kdeplot(data=df, x='price', hue=column, fill=True, ax=ax, palette=['#ff2b2b', '#D3D3D3'])
            title = f'Rozkład cen nieruchomości w tys. PLN w zależności od cechy {column}'
            ax.set_title(title, pad=20)
            ax.set_xlabel('Cena [tys. PLN]')
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    plt.tight_layout()
    st.pyplot()

if __name__ == "__main__":
    app()
