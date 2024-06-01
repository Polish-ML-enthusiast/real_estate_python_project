import streamlit as st
from streamlit_option_menu import option_menu
from pages import contact, o_aplikacji, o_mnie, parameters, results, EDA

# Ustawienie konfiguracji strony
st.set_page_config(page_title="Projekt Python - Predykcja cech nieruchomości", layout='wide', initial_sidebar_state='expanded', page_icon='pictures/EDA.png')

def main():
    # Inicjalizacja stanu, jeśli jeszcze nie istnieje
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'O mnie'

    # Definiowanie opcji w pasku bocznym
    options = ["O mnie", "O aplikacji", "EDA", "Parametry wejściowe", "Wyniki", "Kontakt"]
    icons = ['person', 'info', 'graph-up', 'sliders', 'bar-chart', 'envelope']

    # Tworzenie menu w pasku bocznym
    with st.sidebar:
        chosen_page = option_menu(
            menu_title="Menu aplikacji",
            options=options,
            icons=icons,
            default_index=options.index(st.session_state['current_page']),
            orientation="vertical"
        )

    # Aktualizacja stanu bieżącej strony
    if chosen_page != st.session_state['current_page']:
        st.session_state['current_page'] = chosen_page
        st.experimental_rerun()

    # Wywołanie funkcji odpowiadającej aktualnie wybranej stronie
    pages = {
        'O mnie': o_mnie.app,
        'O aplikacji': o_aplikacji.app,
        'EDA': EDA.app,
        'Parametry wejściowe': parameters.app,
        'Wyniki': results.app,
        'Kontakt': contact.app
    }

    # Uruchomienie funkcji związanej z aktualnie wybraną stroną
    pages[st.session_state['current_page']]()

if __name__ == "__main__":
    main()
