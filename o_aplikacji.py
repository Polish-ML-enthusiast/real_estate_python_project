import streamlit as st

def app():
    st.title('O aplikacji 👨‍💻')

    st.write("""
    ## Jak działa aplikacja?⚙️

    Aplikacja analizuje dane dotyczące nieruchomości, które pochodzą z serwisu Kaggle. Ze względu na potencjalne zmiany w układzie stron internetowych, zdecydowano się nie stosować technik webscrapingu, a skorzystać z gotowych, niezawodnych zestawów danych.

    ## Moduły aplikacji🗂️

    - **EDA (Exploratory Data Analysis):** W tej sekcji znajdziesz podstawowe statystyki opisowe zbioru danych, które pomagają zrozumieć jego strukturę i kluczowe zmienne.

    - **Parametry wejściowe:** Użytkownik może wybrać interesujące parametry nieruchomości, takie jak rok budowy, liczba pokoi czy powierzchnia, używając suwaków i innych elementów interfejsu.

    ## Metody uczenia maszynowego🛠️

    Do predykcji cen nieruchomości wykorzystano następujące metody uczenia maszynowego:
    
    - **Regresja liniowa:** Jest to podstawowa metoda statystyczna, która modeluje zależność między zmienną zależną a jedną lub więcej zmiennymi niezależnymi poprzez dopasowanie liniowej równania do obserwowanych danych.
    
    - **Algorytm najbliższych sąsiadów (k-NN):** Metoda ta polega na znalezieniu najbliższych próbek w przestrzeni cech i przewidywaniu wartości na ich podstawie. Jest to przykład tzw. uczenia leniwego, gdzie obliczenia są odroczone do momentu klasyfikacji nowej próbki.
    
    - **XGBoost:** Skrót od eXtreme Gradient Boosting, jest to zaawansowana technika oparta na drzewach decyzyjnych, która korzysta z gradientowego wzmacniania, aby zwiększyć dokładność modeli.
    
    Każda z tych metod ma swoje specyficzne zastosowania i efektywność w różnych scenariuszach danych i jest odpowiednio dostosowywana do cech analizowanego zbioru danych.

    ## Cel aplikacji🎯

    Celem aplikacji jest umożliwienie użytkownikom intuicyjnej analizy danych o nieruchomościach i przewidywania cen, bazując na wybranych parametrach. Aplikacja ma na celu także edukację użytkowników w zakresie metod uczenia maszynowego i analizy danych.
    """)

