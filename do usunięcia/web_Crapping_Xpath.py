from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import time

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
                     Column('location', String))

# Tworzenie tabeli w bazie danych
metadata.create_all(engine)

# Ustawienia Selenium WebDriver
service = Service("C:\\Users\\User\\Desktop\\RMA6807\\Moje dokumenty\\Programista Python Developer\\Projekt\\chromedriver-win64\\chromedriver.exe")
  # ścieżka do ChromeDriver
driver = webdriver.Chrome(service=service)

# Ustawienie czasu oczekiwania
driver.implicitly_wait(1200) 

# Otwieranie strony
url = "https://www.otodom.pl/"
driver.get(url)


# Czekanie na załadowanie strony i wyszukanie przycisku akceptacji cookies
try:
    # Czekanie na przycisk akceptacji cookies i kliknięcie go
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id="onetrust-accept-btn-handler"]"))
    )
    accept_button.click()
    print("Przycisk akceptacji cookies został kliknięty.")

    # Opcjonalne: dodaj opóźnienie, aby umożliwić ręczne badanie strony
    time.sleep(30)

except Exception as e:
    print("Nie znaleziono przycisku akceptacji cookies: ", e)

# Pobieranie danych za pomocą Selenium
listings = driver.find_elements(By.XPATH, '//*[@id="search-form-submit"]')  # Aktualizuj XPath

# Przetwarzanie danych
data = []
for listing in listings:
    type = listing.find_element(By.XPATH, './/span[@class="type"]').text
    surface = listing.find_element(By.XPATH, './/span[@class="surface"]').text
    price = listing.find_element(By.XPATH, './/span[@class="price"]').text
    location = listing.find_element(By.XPATH, './/span[@class="location"]').text
    data.append({'type': type, 'surface': surface, 'price': price, 'location': location})

# Zamykanie przeglądarki
driver.quit()

# Zapisywanie danych do bazy danych
with engine.connect() as connection:
    for item in data:
        ins = otodom_table.insert().values(type=item['type'], surface=item['surface'], price=item['price'], location=item['location'])
        connection.execute(ins)

print("Dane zostały zapisane w bazie danych.")