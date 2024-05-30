import os
import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from sklearn.metrics import mean_squared_error, r2_score
import osmnx as ox

@st.cache_data
def load_data():
    data = pd.read_csv('data/apartments_pl_2024_04.csv', encoding='ISO-8859-1')
    return data

@st.cache_data
def load_streets():
    streets = pd.read_csv('data/wroclaw_streets.csv')
    return streets

def fetch_and_save_streets():
    city = "Wrocław, Poland"
    graph = ox.graph_from_place(city, network_type='all')
    nodes, edges = ox.graph_to_gdfs(graph)

    def get_first_name(name):
        if isinstance(name, list):
            return name[0]
        return name

    edges['name'] = edges['name'].apply(get_first_name)
    streets = edges[['name', 'geometry']].dropna(subset=['name']).drop_duplicates(subset=['name'])

    streets['lon'] = streets['geometry'].apply(lambda x: x.centroid.x)
    streets['lat'] = streets['geometry'].apply(lambda x: x.centroid.y)

    streets_df = streets[['name', 'lon', 'lat']]
    streets_df = streets_df.drop_duplicates().reset_index(drop=True)

    output_file = 'data/wroclaw_streets.csv'
    streets_df.to_csv(output_file, index=False)

def app():
    st.title('Wybór parametrów 🔍 - cech nieruchomości 🏘️')
    
    # Fetch and save street data if the file does not exist
    if not os.path.exists('data/wroclaw_streets.csv'):
        fetch_and_save_streets()

    data = load_data()
    data = data[data['city'].str.capitalize() == 'Wroclaw']

    # Ładowanie danych o ulicach i sortowanie alfabetyczne
    streets = load_streets()
    street_names = streets['name'].sort_values().unique()
    
    st.subheader('Określ interesujące Ciebie nieruchomości⚙️')

    # Lista rozwijalna z możliwością wyszukiwania
    selected_street = st.selectbox('Wybierz ulicę', street_names, help="Wpisz nazwę ulicy, aby wyszukać")

    area = st.slider('Powierzchnia mieszkania w m2', int(data['squareMeters'].min()), int(data['squareMeters'].max()), int(data['squareMeters'].min()))
    rooms = st.slider('Liczba pokoi', int(data['rooms'].min()), int(data['rooms'].max()), int(data['rooms'].min()))
    floor = st.slider('Piętro', int(data['floor'].min()), int(data['floor'].max()), int(data['floor'].min()))
    min_year = int(data['buildYear'].dropna().min())
    max_year = int(data['buildYear'].dropna().max())
    buildYear = st.selectbox('Rok budowy:', list(range(min_year, max_year + 1)))
    balconies = st.radio('Czy posiada balkon', (0, 1))
    
    # Wybór modeli ML do trenowania
    st.subheader('Wybór modeli 🛠️uczenia maszynowego 🤖 (ML) 🚀')
    ml_models = {
        'Regresja liniowa': 'linear_regression',
        'k-najbliższych sąsiadów (KNN)': 'k-nearest_neighbors',
        'XGBoost': 'xgboost'
    }
    selected_models_display = st.multiselect('Wybierz modele', list(ml_models.keys()), default=list(ml_models.keys()))
    selected_models = [ml_models[model] for model in selected_models_display]

    if st.button('Prognozuj cenę mieszkania'):
        st.session_state['input_data'] = [selected_street, area, rooms, floor, buildYear, balconies, selected_models]
        st.session_state['current_page'] = 'Wyniki'  # Zapewnienie nawigacji
        st.session_state['navigate_to_results'] = True  # Ustawienie flagi
        st.experimental_rerun()

if __name__ == "__main__":
    app()
