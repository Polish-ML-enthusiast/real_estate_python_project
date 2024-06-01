import osmnx as ox
import pandas as pd

# Definiowanie miasta
city = "Wrocław, Poland"

# Pobieranie danych 
print("Pobieranie danych o ulicach z OpenStreetMap...")
graph = ox.graph_from_place(city, network_type='all')
nodes, edges = ox.graph_to_gdfs(graph)

# Wybieranie tylko ulic z danych
print("Przetwarzanie danych o ulicach...")

# Funkcja do przekształcenia nazw ulic, które są listami, na pojedyncze wartości
def get_first_name(name):
    if isinstance(name, list):
        return name[0]
    return name

# Przekształcenie kolumny 'name' aby zawierała tylko pierwsze nazwy
edges['name'] = edges['name'].apply(get_first_name)

# Kontynuowanie przetwarzania
streets = edges[['name', 'geometry']].dropna(subset=['name']).drop_duplicates(subset=['name'])

# Przekształcanie geometrii do współrzędnych geograficznych
streets['lon'] = streets['geometry'].apply(lambda x: x.centroid.x)
streets['lat'] = streets['geometry'].apply(lambda x: x.centroid.y)

# Tworzenie DataFrame z nazwami ulic i ich współrzędnymi
streets_df = streets[['name', 'lon', 'lat']]
streets_df = streets_df.drop_duplicates().reset_index(drop=True)

# Zapisanie
output_file = 'data/wroclaw_streets.csv'
streets_df.to_csv(output_file, index=False)

print("Dane zostały zapisane do pliku:", output_file)
print(streets_df.head())
