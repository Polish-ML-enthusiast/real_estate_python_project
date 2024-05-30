import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Konfiguracja połączenia z bazą danych
DATABASE_URL = "sqlite:///otodom_data.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Definicja tabeli w SQLAlchemy
otodom_table = Table('otodom', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('type', String),
                     Column('surface', String),
                     Column('price', String),
                     Column('location', String)
                    )

# Tworzenie tabeli w bazie danych
metadata.create_all(engine)

# Pobieranie zawartości strony
url = "https://www.otodom.pl/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


# Sprawdzenie odpowiedzi od serwera
print("Status odpowiedzi:", response.status_code)
if response.status_code != 200:
    print("Problem z pobraniem strony. Sprawdź URL lub połączenie internetowe.")

# Znajdowanie interesujących danych - przykładowo tytuły, ceny i lokalizacje ogłoszeń
# UWAGA: Poniższy selektor CSS jest tylko przykładem i może wymagać dostosowania!
listings = soup.find_all('id', class_='search-form-submit')
print(f"Znaleziono {len(listings)} elementów.")

# Przetwarzanie każdej oferty
data = []
for listing in listings:
    type = listing.find('span', class_='css-1dlj142.e1xs6odl1').get_text(strip=True)
    surface = listing.find('span', class_='css-1ssixle enmtvg52').get_text(strip=True)
    price = listing.find('li', class_='css-1ssixle enmtvg52').get_text(strip=True)
    location = listing.find('li', class_='css-19rap2 eia0eze1').get_text(strip=True)
    data.append({'type': type,'surface': surface, 'price': price, 'location': location})


# Sprawdzenie, czy dane zostały poprawnie pobrane
if not data:
    print("Brak danych do zapisania. Sprawdź selektory CSS.")
else:
    print("Dane do zapisu:", data)


# Zapisywanie danych do bazy danych
with engine.connect() as connection:
    for item in data:
        ins = otodom_table.insert().values(type=item['type'], surface=item['surface'], price=item['price'], location=item['location'])
        connection.execute(ins)

print("Dane zostały zapisane w bazie danych.")