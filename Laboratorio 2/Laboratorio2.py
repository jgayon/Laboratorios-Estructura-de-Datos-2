import math
import pandas as pd
import networkx as nx
import folium


def haversine_distance(lat1, lon1, lat2, lon2):
  # Convertir grados a radianes
  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)

  # Diferencia de latitudes y longitudes
  dlat = lat2 - lat1
  dlon = lon2 - lon1

  # Cálculo del seno y coseno de las diferencias
  a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.sin(lat2) * math.sin(dlon / 2) ** 2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

  # Radio de la Tierra (en kilómetros)
  R = 6371

  # Distancia entre dos puntos
  distance = R * c

  return distance

df = pd.read_csv('flights_final.csv')

# Creación de un diccionario para almacenar los aeropuertos y sus coordenadas
airports = {}
for index, row in df.iterrows():
  airport_code = row['Source Airport Code']
  name= row['Source Airport Name']
  latitude = row['Source Airport Latitude']
  longitude = row['Source Airport Longitude']
  city = row['Source Airport City']
  country = row['Source Airport Country']
  
  airports[airport_code] = [(latitude, longitude),name,city,country]

for index, row in df.iterrows():
  if row['Destination Airport Code'] not in airports:
    airport_code = row['Destination Airport Code']
    name= row['Destination Airport Name']
    latitude = row['Destination Airport Latitude']
    longitude = row['Destination Airport Longitude']
    city = row['Destination Airport City']
    country = row['Destination Airport Country']
    
    airports[airport_code] = [(latitude, longitude),name,city,country]

#Creaccion diccionario destinos de viajes por Aeropuertos
airports_trips={}
for element in airports:
  airports_trips[element]=[]

for index, row in df.iterrows():
  airport_code = row['Source Airport Code']
  destination_code = row['Destination Airport Code']
  airports_trips[airport_code].append(destination_code)

# Creación del grafo
G = nx.Graph()

# Adición de nodos (aeropuertos)
for airport_code in airports:
  G.add_node(airport_code)

for element in airports_trips:
    source_code = element
    for trip in airports_trips[source_code]:
        destination_code= trip
        lat1 = airports[source_code][0][0]
        lon1 = airports[source_code][0][1]
        lat2 = airports[destination_code][0][0]
        lon2 = airports[destination_code][0][1]
        #distance = haversine_distance(lat1,lon1,lat2,lon2)  no esta funcionando, math error
        G.add_edge(source_code, destination_code)

# Creación del mapa
map = folium.Map(location=[0, 0], zoom_start=2)

# Adición de marcadores para cada aeropuerto
for element in airports:
  latitude, longitude = airports[element][0]
  folium.Marker(location=[latitude, longitude], popup=element).add_to(map)

# Visualización del mapa
map