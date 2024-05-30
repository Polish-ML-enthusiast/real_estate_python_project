import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from EDA import get_processed_data
import joblib

def train_and_save_model():
    # Wczytanie danych z funkcji get_processed_data
    data = get_processed_data()

    # Definiowanie zmiennej docelowej
    y = data['price']

    # Definiowanie cech do modelowania
    features = ['squareMeters', 'rooms', 'floor', 'buildYear', 'hasBalcony_yes', 'centreDistance']
    if 'price1m2' in data.columns:
        data = data.drop(columns=['price1m2'])

    # Użycie tylko wybranych cech do trenowania
    X = data[features]

    # Dzielenie danych na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    # Trenowanie modelu regresji liniowej
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # Przewidywanie na zbiorze testowym
    y_pred = lr.predict(X_test)

    # Ocena modelu
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}, R^2: {r2}")

    # Zapisywanie modelu do pliku
    joblib.dump(lr, "lr_model.sav")

# Wywołanie funkcji, jeśli plik jest uruchamiany samodzielnie
if __name__ == "__main__":
    train_and_save_model()
