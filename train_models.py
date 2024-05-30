import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, explained_variance_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib
from sklearn.inspection import permutation_importance

def load_data():
    df = pd.read_csv('data/apartments_pl_2024_04.csv')
    df.drop(columns=['id', 'schoolDistance', 'clinicDistance', 'kindergartenDistance', 
                     'restaurantDistance', 'collegeDistance', 'pharmacyDistance', 
                     'postOfficeDistance'], inplace=True)
    df.fillna({
        'floor': df['floor'].median(),
        'floorCount': df['floorCount'].median(),
        'buildYear': df['buildYear'].median(),
        'hasElevator': 'yes'
    }, inplace=True)
    df['city'] = df['city'].str.capitalize()
    df['price1m2'] = df['price'] / df['squareMeters']
    df = pd.get_dummies(df, columns=['hasParkingSpace', 'hasBalcony', 'hasSecurity', 
                                     'hasStorageRoom', 'hasElevator'], drop_first=True)
    return df

def save_plot(predictions, y_test, filename):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, alpha=0.3, c=predictions, cmap='coolwarm')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Rzeczywiste ceny')
    plt.ylabel('Przewidywane ceny')
    plt.colorbar(label='Przewidywane ceny', aspect=40)
    plt.savefig(f"pictures/{filename}.png")
    plt.close()

def save_feature_importance(model, X_train, y_train, X_test, y_test, filename):
    feature_names = {
        'squareMeters': 'Powierzchnia m²',
        'rooms': 'Liczba pokoi',
        'floor': 'Piętro',
        'buildYear': 'Rok budowy',
        'hasBalcony_yes': 'Posiadanie balkonu',
        'centreDistance': 'Odległość od centrum'
    }
    
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        features = X_train.columns
    elif hasattr(model, 'coef_'):
        importance = model.coef_
        features = X_train.columns
    else:
        # Permutation Feature Importance for KNN
        result = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42, n_jobs=1)
        importance = result.importances_mean
        features = X_train.columns

    feature_importance_df = pd.DataFrame({'Cecha': [feature_names.get(f, f) for f in features], 'Waga': importance})
    feature_importance_df = feature_importance_df.sort_values(by='Waga', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Waga', y='Cecha', data=feature_importance_df, palette='Blues')
    plt.xlabel('Waga')
    plt.ylabel('Cecha')
    plt.tight_layout()
    plt.savefig(f"pictures/{filename}_feature_importance.png")
    plt.close()

def train_models(df):
    X = df[['squareMeters', 'rooms', 'floor', 'buildYear', 'hasBalcony_yes', 'centreDistance']]
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'linear_regression': LinearRegression(),
        'xgboost': XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    }

    knn = KNeighborsRegressor()
    param_grid = {'n_neighbors': list(range(1, 21))}
    knn_grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=1)
    knn_grid_search.fit(X_train, y_train)
    best_knn = knn_grid_search.best_estimator_
    models['k-nearest_neighbors'] = best_knn

    for name, model in models.items():
        if name == 'k-nearest_neighbors':  # Skalowanie dla KNN
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            model.fit(X_train_scaled, y_train)
            predictions = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        evs = explained_variance_score(y_test, predictions)

        # Zapis metryk
        metrics = {'MSE': mse, 'R^2': r2, 'MAE': mae, 'EVS': evs}
        pd.DataFrame([metrics]).to_csv(f"metrics/{name}_metrics.csv", index=False)

        # Zapis wykresów
        save_plot(predictions, y_test, name)

        # Zapis ważności cech
        save_feature_importance(model, X_train, y_train, X_test, y_test, name)

        # Zapis modeli
        joblib.dump(model, f"models/{name}_model.sav")

if __name__ == '__main__':
    df = load_data()
    train_models(df)
