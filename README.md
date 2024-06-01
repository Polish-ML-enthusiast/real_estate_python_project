# real_estate_python_project

# Prognoza Ceny Nieruchomości - Aplikacja Streamlit

## Opis projektu
Aplikacja analizuje rzeczywiste dane dotyczące nieruchomości we Wrocławiu, które pochodzą z serwisu [Kaggle](https://www.kaggle.com/datasets/krzysztofjamroz/apartment-prices-in-poland?select=apartments_rent_pl_2024_04.csv). Korzystając z różnych metod uczenia maszynowego, pozwala przewidywać ceny mieszkań na podstawie wybranych parametrów.

## Funkcjonalności
- **EDA (Exploratory Data Analysis):** Podstawowe statystyki opisowe zbioru danych.
- **Parametry wejściowe:** Możliwość wyboru interesujących parametrów nieruchomości.
- **Wyniki:** Prognozowane ceny nieruchomości oraz wizualizacje wyników.

## Metody uczenia maszynowego
- Regresja liniowa
- Regresja wielomianowa
- Drzewa decyzyjne
- Lasy losowe
- K Najbliższych Sąsiadów (KNN)
- XGBoost

## Cel aplikacji
Aplikacja powstała na potrzeby projektu zaliczeniowego studiów podyplomowych na Uniwersytecie MERIOTO w Warszawie na kierunku "Programista Python Developer".

## Wymagania
- Python 3.7+
- Biblioteki wymienione w `requirements.txt`

## Instalacja
1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/twoje-repo/prognoza-ceny-nieruchomosci.git
    cd prognoza-ceny-nieruchomosci
    ```

2. Zainstaluj wymagane biblioteki:
    ```bash
    pip install -r requirements.txt
    ```

## Uruchomienie
1. Uruchom aplikację Streamlit:
    ```bash
    streamlit run pages/Intro.py
    ```

2. Otwórz przeglądarkę internetową i przejdź do adresu `http://localhost:8501`.

## Struktura projektu
├── data
│ ├── apartments_pl_2024_04.csv
│ └── wroclaw_streets.csv
├── models
├── metrics
├── pages
│ ├── Intro.py
│ ├── contact.py
│ ├── EDA.py
│ ├── o_aplikacji.py
│ ├── o_mnie.py
│ ├── parameters.py
│ ├── results.py
│ └── train_models.py
├── pictures
├── README.md
├── requirements.txt

## Użycie aplikacji
1. **EDA (Exploratory Data Analysis):** Obejmuje analizę eksploracyjną danych, w tym podstawowe statystyki i wizualizacje.
2. **Parametry wejściowe:** Umożliwia użytkownikom wprowadzenie parametrów nieruchomości, takich jak powierzchnia, liczba pokoi, piętro, rok budowy i posiadanie balkonu.
3. **Wyniki:** Wyświetla prognozowane ceny nieruchomości na podstawie wprowadzonych parametrów oraz prezentuje wykresy i wizualizacje.

## Kontakt
Jeśli masz pytania lub uwagi dotyczące aplikacji, prosimy o kontakt:
- [LinkedIn](https://www.linkedin.com/in/grzegorz-macowicz-b75962122/)
- [Strona internetowa](https://grzegorzmacowicz.pl/)