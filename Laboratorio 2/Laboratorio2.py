import math
import pandas as pd

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