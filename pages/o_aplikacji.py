import streamlit as st

def app():
    st.title('O aplikacji 👨‍💻')

    st.write("""
    ## Jak działa aplikacja?⚙️

    Aplikacja analizuje rzeczywiste dane dotyczące nieruchomości we Wrocławiu, które pochodzą z serwisu [Kaggle](https://www.kaggle.com/datasets/krzysztofjamroz/apartment-prices-in-poland?select=apartments_rent_pl_2024_04.csv). Korzystając z różnych metod uczenia maszynowego, pozwala przewidywać ceny mieszkań na podstawie wybranych parametrów.

    ## Moduły aplikacji🗂️

    - **EDA (Exploratory Data Analysis):** W tej sekcji znajdziesz podstawowe statystyki opisowe zbioru danych, które pomagają zrozumieć jego strukturę i kluczowe zmienne.

    - **Parametry wejściowe:** Użytkownik może wybrać interesujące parametry nieruchomości, takie jak rok budowy, liczba pokoi czy powierzchnia, używając suwaków i innych elementów interfejsu.

    - **Wyniki:** W tej sekcji można zobaczyć prognozowane ceny nieruchomości na podstawie wybranych parametrów oraz wizualizacje wyników.

    ## Metody uczenia maszynowego🛠️

    Do predykcji cen nieruchomości wykorzystano następujące metody uczenia maszynowego:
    
    - **Regresja liniowa:** Podstawowa metoda statystyczna modelująca zależność między zmienną zależną a jedną lub więcej zmiennymi niezależnymi poprzez dopasowanie liniowego równania do danych.

    - **Regresja wielomianowa:** Rozszerzenie regresji liniowej, które modeluje zależności nieliniowe poprzez dodanie potęg zmiennych niezależnych.

    - **Drzewa decyzyjne:** Metoda, która używa drzewa decyzji jako modelu predykcyjnego, odwzorowując zmienne wejściowe na wartości wyjściowe.

    - **Lasy losowe:** Algorytm oparty na drzewach decyzyjnych, który używa wielu drzew decyzyjnych do poprawy dokładności predykcji.

    - **Algorytm najbliższych sąsiadów (KNN):** Metoda polegająca na znalezieniu najbliższych próbek w przestrzeni cech i przewidywaniu wartości na ich podstawie.

    - **XGBoost:** Zaawansowana technika oparta na drzewach decyzyjnych, korzystająca z gradientowego wzmacniania do zwiększenia dokładności modeli.
    
    Każda z tych metod ma swoje specyficzne zastosowania i efektywność w różnych scenariuszach danych, i jest odpowiednio dostosowywana do cech analizowanego zbioru danych.

    ## Cel aplikacji🎯

    Aplikacja powstała na potrzeby projektu zaliczeniowego studiów podyplomowych na Uniwersytecie MERITO w Warszawie na kierunku "Programista Python Developer".

    Niniejsza aplikacja zbudowana w Streamlit jest moim pierwszym projektem w tym frameworku. Jej głównym celem było poszerzenie moich umiejętności w kontekście budowania aplikacji webowych oraz wizualizacji danych.

    Chociaż modele uczenia maszynowego zawarte w tej aplikacji zostały zaprojektowane i przetestowane, projekt ten nie powinien być traktowany jako wzorcowy przykład zaawansowanego modelowania ML. Moje główne zainteresowanie skupiało się na eksploracji możliwości, jakie oferuje Streamlit, oraz na tworzeniu intuicyjnych i atrakcyjnych wizualizacji danych.

    Zachęcam do korzystania z aplikacji w celu zrozumienia podstawowych technik analizy danych i wizualizacji, jednakże, wyniki uzyskane z modeli ML mogą wymagać dalszej optymalizacji i walidacji przed zastosowaniem w rzeczywistych scenariuszach biznesowych.
    """)

if __name__ == "__main__":
    app()
