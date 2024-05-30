import os
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def load_model_metrics(model_name):
    try:
        model = joblib.load(f"models/{model_name}_model.sav")
        metrics = pd.read_csv(f"metrics/{model_name}_metrics.csv")
        return model, metrics
    except FileNotFoundError:
        st.error(f"Nie znaleziono pliku dla modelu {model_name.replace('_', ' ').title()}. Sprawdź, czy plik istnieje.")
        return None, None
    except Exception as e:
        st.error(f"Wystąpił błąd przy ładowaniu danych modelu {model_name.replace('_', ' ').title()}: {e}")
        return None, None

def plot_feature_importance(model_name):
    plot_path = f"pictures/{model_name}_feature_importance.png"
    if os.path.exists(plot_path):
        return plot_path
    return None

def app():
    st.title('Wyniki💡prognozy cen mieszkań 🏡')
    

    if 'navigate_to_results' in st.session_state and st.session_state['navigate_to_results']:
        input_data = st.session_state['input_data']
        selected_street, area, rooms, floor, buildYear, balconies, selected_models = input_data
        input_df = pd.DataFrame([[area, rooms, floor, buildYear, balconies, 0]], columns=['squareMeters', 'rooms', 'floor', 'buildYear', 'hasBalcony_yes', 'centreDistance'])

        st.header("Podsumowanie wybranych parametrów 📌")
        st.write(f"**Ulica:** {selected_street}")
        st.write(f"**Powierzchnia:** {area} m²")
        st.write(f"**Liczba pokoi:** {rooms}")
        st.write(f"**Piętro:** {floor}")
        st.write(f"**Rok budowy:** {buildYear}")
        st.write(f"**Czy posiada balkon:** {'Tak' if balconies == 1 else 'Nie'}")

        model_names = {
            'linear_regression': 'Regresja liniowa',
            'k-nearest_neighbors': 'k-najbliższych sąsiadów (KNN)',
            'xgboost': 'XGBoost'
        }

        results_data = []
        feature_importance_plots = []

        for model_key in selected_models:
            model, metrics = load_model_metrics(model_key)
            if model:
                prediction = model.predict(input_df)[0]
                model_display_name = model_names.get(model_key, model_key)
                if model_key == 'k-nearest_neighbors':
                    model_display_name += f" - k: {model.n_neighbors}"
                
                results_data.append({
                    'Model': model_display_name,
                    'Prognozowana cena': prediction,
                    'MSE': metrics['MSE'].iloc[0] if metrics is not None else 'N/A',
                    'R^2': metrics['R^2'].iloc[0] if metrics is not None else 'N/A',
                    'MAE': metrics['MAE'].iloc[0] if metrics is not None else 'N/A',
                    'EVS': metrics['EVS'].iloc[0] if metrics is not None else 'N/A'
                })

                feature_importance_plot = plot_feature_importance(model_key)
                if feature_importance_plot:
                    feature_importance_plots.append((model_display_name, feature_importance_plot))

        if results_data:
            st.header("Porównanie wyników 📋")
            results_df = pd.DataFrame(results_data)
            results_df = results_df.set_index('Model')
            st.write(
                results_df.style.format({
                    'Prognozowana cena': '{:.2f} PLN',
                    'MSE': '{:.2f}',
                    'R^2': '{:.2f}',
                    'MAE': '{:.2f}',
                    'EVS': '{:.2f}'
                }).set_table_styles(
                    [{'selector': 'thead th', 'props': [('text-align', 'center'), ('background-color', '#0C2D57'), ('color', 'white')]}]
                ).set_properties(**{'text-align': 'center'}).set_properties(subset=['Prognozowana cena', 'MSE', 'R^2', 'MAE', 'EVS'], **{'width': '20%'})
            )

        st.header("Wizualizacje 📈- wykresy rozrzutu")
        for result in results_data:
            plot_path = f"pictures/{result['Model'].replace(' ', '_').lower()}.png"
            if os.path.exists(plot_path):
                st.subheader(f"Model: {result['Model']}")
                st.image(plot_path, use_column_width=True)
            else:
                st.write(f"Brak dostępnych wizualizacji dla modelu {result['Model']}.")

        st.header("Wizualizacje - Ważność cech")
        for model_name, plot_path in feature_importance_plots:
            st.subheader(f"Model: {model_name}")
            st.image(plot_path, use_column_width=True)

        st.session_state['navigate_to_results'] = False  # Reset flagi
    else:
        st.write("Wybierz parametry wejściowe w module 'Parametry wejściowe' i kliknij 'Prognozuj cenę', aby zobaczyć wyniki.")

    if st.button("Powrót do wyboru parametrów"):
        st.session_state['current_page'] = 'Parametry wejściowe'
        st.experimental_rerun()

if __name__ == "__main__":
    app()

