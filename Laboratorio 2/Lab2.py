import pandas as pd
import networkx as nx
import folium
from math import radians, sin, cos, sqrt, atan2
from IPython.display import display, HTML

# Función para calcular la distancia entre dos coordenadas geográficas
def haversine(lat1, lon1, lat2, lon2):
    radius = 6371  # Radio de la Tierra en kilómetros
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c
    return distance

def mostrar_informacion_aeropuerto(codigo_aeropuerto):
    if codigo_aeropuerto in G.nodes:
        aeropuerto_info = {
            "Código": codigo_aeropuerto,
            "Nombre": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Name"].values[0],
            "Ciudad": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport City"].values[0],
            "País": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Country"].values[0],
            "Latitud": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Latitude"].values[0],
            "Longitud": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Longitude"].values[0]
        }

        print("Información del aeropuerto:")
        for key, value in aeropuerto_info.items():
            print(f"{key}: {value}")
        


        return True

    else:
        print(f"No se encontró información para el aeropuerto con código {codigo_aeropuerto}")
        return False

def obtener_informacion_aeropuerto(codigo_aeropuerto):
    if codigo_aeropuerto in G.nodes:
        aeropuerto_info = {
            "Código": codigo_aeropuerto,
            "Nombre": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Name"].values[0],
            "Ciudad": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport City"].values[0],
            "País": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Country"].values[0],
            "Latitud": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Latitude"].values[0],
            "Longitud": data[data["Source Airport Code"] == codigo_aeropuerto]["Source Airport Longitude"].values[0]
        }
        return aeropuerto_info
    else:
        return None

data = pd.read_csv("Laboratorios-Estructura-de-Datos-2/laboratorio 2/flights_final.csv")
# Crear un grafo no dirigido y Crear diccionarios para almacenar las posiciones de origen y destino
G = nx.Graph()
pos_aeropuerto = {}


for index, row in data.iterrows():
    source_airport = row["Source Airport Code"]
    airport_name = row["Source Airport Name"]
    airport_city = row["Source Airport City"]
    airport_country = row["Source Airport Country"]
    airport_lat = row["Source Airport Latitude"]
    airport_lon = row["Source Airport Longitude"]
    destination_airport = row["Destination Airport Code"]
    source_coords = (row["Source Airport Latitude"], row["Source Airport Longitude"])
    dest_coords = (row["Destination Airport Latitude"], row["Destination Airport Longitude"])

    # Agregar nodos (aeropuertos)
    if not G.has_node(source_airport):
        G.add_node(source_airport, pos=source_coords)
        pos_aeropuerto[source_airport] = source_coords
    if not G.has_node(destination_airport):
        G.add_node(destination_airport, pos=dest_coords)
        pos_aeropuerto[destination_airport] = dest_coords

    # Calcular la distancia y agregar la arista ponderada
    distance = haversine(*source_coords, *dest_coords)
    G.add_edge(source_airport, destination_airport, weight=distance)



aeropuerto_origen_seleccionado = None
while True:
    print("\nMenú de consulta de aeropuertos:")
    print("1. Mostrar información de un aeropuerto y Mostrar la información de los 10 aeropuertos cuyos caminos mínimos desde el vértice dado sean los más largos.")
    print("2. Mostrar el camino mínimo entre el primer y el segundo vértice sobre el mapa de la interfaz gráfica")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")
    if opcion == '1':
        codigo_aeropuerto = input("Ingrese el código del aeropuerto: ")
        aeropuerto_origen_seleccionado = codigo_aeropuerto
        aux = mostrar_informacion_aeropuerto(codigo_aeropuerto)
        
        if not aux:
             aeropuerto_origen_seleccionado= None
        
        if aux:
            longest_paths = nx.single_source_dijkstra_path_length(G, codigo_aeropuerto)
            sorted_longest_paths = sorted(longest_paths.items(), key=lambda x: x[1], reverse=True)[:10]
            print("\nLos 10 aeropuertos con los caminos mínimos más largos:")
            for airport, distance in sorted_longest_paths:
                mostrar_informacion_aeropuerto(airport)
                print(f"Distancia del camino mínimo: {distance} km")
                print("-------------------------------------------")

            # Crear un mapa con Folium
            m = folium.Map(location=pos_aeropuerto[codigo_aeropuerto], zoom_start=5)

            # Agregar el aeropuerto original al mapa
            lat, lon = pos_aeropuerto[codigo_aeropuerto]
            info_aeropuerto = obtener_informacion_aeropuerto(codigo_aeropuerto)
            if info_aeropuerto:
                popup_content = f"{info_aeropuerto['Nombre']}<br/>Código: {info_aeropuerto['Código']}<br/>Ciudad: {info_aeropuerto['Ciudad']}<br/>País: {info_aeropuerto['País']}<br/>Latitud: {info_aeropuerto['Latitud']}<br/>Longitud: {info_aeropuerto['Longitud']}<br/>Distancia del camino mínimo: 0.0 km"
                folium.Marker([lat, lon], popup=popup_content, icon=folium.Icon(color='green')).add_to(m)
            else:
                folium.Marker([lat, lon], popup="Aeropuerto sin información", icon=folium.Icon(color='green')).add_to(m)

             # Agregar los 10 aeropuertos con los caminos mínimos más largos al mapa
            for airport, distance in sorted_longest_paths:
                lat, lon = pos_aeropuerto[airport]
                info_aeropuerto = obtener_informacion_aeropuerto(airport)
                if info_aeropuerto:
                    popup_content = f"{info_aeropuerto['Nombre']}<br/>Código: {info_aeropuerto['Código']}<br/>Ciudad: {info_aeropuerto['Ciudad']}<br/>País: {info_aeropuerto['País']}<br/>Latitud: {info_aeropuerto['Latitud']}<br/>Longitud: {info_aeropuerto['Longitud']}<br/>Distancia del camino mínimo: {distance:.2f} km"
                    folium.Marker([lat, lon], popup=popup_content).add_to(m)
                else:
                    folium.Marker([lat, lon], popup="Aeropuerto sin información").add_to(m)

             # Guardar el mapa como HTML
            ruta_mapa = f"ruta_mapa_{codigo_aeropuerto}_top10.html"
            m.save(ruta_mapa)
            print(f"Mapa guardado como {ruta_mapa}")

            # Mostrar el mapa
            display(HTML(ruta_mapa))   


    elif opcion == '2':
        if aeropuerto_origen_seleccionado is None:
            source_vertex = input("Ingresa el código del aeropuerto de origen: ")
            dest_vertex = input("Ingresa el código del aeropuerto de destino: ")

            if source_vertex not in G.nodes or dest_vertex not in G.nodes:
                print("Uno o ambos aeropuertos no se encuentran en el grafo.")
            else:
                try:
                    shortest_path = nx.shortest_path(G, source=source_vertex, target=dest_vertex, weight="weight")
                    Peso = sum(G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))
                    print(f"Peso total del camino mínimo: {Peso:.2f} km")
                except nx.NetworkXNoPath:
                    print("No se encontró un camino entre los aeropuertos seleccionados.")
                    shortest_path = []

                # Obtener las coordenadas del primer aeropuerto en el camino más corto
                if shortest_path:
                    center_coords = G.nodes[shortest_path[0]]['pos']
                else:
                    center_coords = (0.0, 0.0)  # Coordenadas por defecto si no hay aeropuertos en el camino

                # Crear un mapa con Folium
                m = folium.Map(location=center_coords, zoom_start=5)

                # Agregar los aeropuertos al mapa
                for airport in shortest_path:
                    lat, lon = G.nodes[airport]['pos']
                    info_aeropuerto = obtener_informacion_aeropuerto(airport)
                    if info_aeropuerto:
                        popup_content = f"{info_aeropuerto['Nombre']}<br/>Código: {info_aeropuerto['Código']}<br/>Ciudad: {info_aeropuerto['Ciudad']}<br/>País: {info_aeropuerto['País']}<br/>Latitud: {info_aeropuerto['Latitud']}<br/>Longitud: {info_aeropuerto['Longitud']}"
                    if airport == source_vertex or airport == dest_vertex:
                        folium.Marker([lat, lon], popup=popup_content, icon=folium.Icon(color='green')).add_to(m)
                    else:
                        folium.Marker([lat, lon], popup=popup_content).add_to(m)
                
                # Agregar las aristas que conectan los aeropuertos en el recorrido
                for i in range(len(shortest_path) - 1):
                    node1 = shortest_path[i]
                    node2 = shortest_path[i + 1]
                    lat1, lon1 = G.nodes[node1]['pos']
                    lat2, lon2 = G.nodes[node2]['pos']
                    weight = G[node1][node2]['weight']
                    folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", popup=f"Distancia: {weight:.2f} km").add_to(m)

                # Guardar el mapa como HTML
                ruta_mapa = f"ruta_mapa_{source_vertex}_{dest_vertex}.html"
                m.save(ruta_mapa)
                print(f"Mapa guardado como {ruta_mapa}")

                # Mostrar el mapa
                display(HTML(ruta_mapa))
        else:
            source_vertex = aeropuerto_origen_seleccionado  # Utiliza el aeropuerto seleccionado en la opción 1 como origen
            dest_vertex = input("Ingresa el código del aeropuerto de destino: ")

            if source_vertex not in G.nodes or dest_vertex not in G.nodes:
                print("Uno o ambos aeropuertos no se encuentran en el grafo.")
            else:
                try:
                    shortest_path = nx.shortest_path(G, source=source_vertex, target=dest_vertex, weight="weight")
                    Peso = sum(G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1))
                    print(f"Peso total del camino mínimo: {Peso:.2f} km")
                except nx.NetworkXNoPath:
                    print("No se encontró un camino entre los aeropuertos seleccionados.")
                    shortest_path = []

                # Obtener las coordenadas del primer aeropuerto en el camino más corto
                if shortest_path:
                    center_coords = G.nodes[shortest_path[0]]['pos']
                else:
                    center_coords = (0.0, 0.0)  # Coordenadas por defecto si no hay aeropuertos en el camino

                # Crear un mapa con Folium
                m = folium.Map(location=center_coords, zoom_start=5)

                # Agregar los aeropuertos al mapa
                for airport in shortest_path:
                    lat, lon = G.nodes[airport]['pos']
                    info_aeropuerto = obtener_informacion_aeropuerto(airport)
                    if info_aeropuerto:
                        popup_content = f"{info_aeropuerto['Nombre']}<br/>Código: {info_aeropuerto['Código']}<br/>Ciudad: {info_aeropuerto['Ciudad']}<br/>País: {info_aeropuerto['País']}<br/>Latitud: {info_aeropuerto['Latitud']}<br/>Longitud: {info_aeropuerto['Longitud']}"
                        folium.Marker([lat, lon], popup=popup_content).add_to(m)
                    else:
                        folium.Marker([lat, lon], popup="Aeropuerto sin información").add_to(m)

                # Agregar las líneas que conectan los aeropuertos en el recorrido
                for i in range(len(shortest_path) - 1):
                    node1 = shortest_path[i]
                    node2 = shortest_path[i + 1]
                    lat1, lon1 = G.nodes[node1]['pos']
                    lat2, lon2 = G.nodes[node2]['pos']
                    weight = G[node1][node2]['weight']
                    folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", popup=f"Distancia: {weight:.2f} km").add_to(m)

                # Guardar el mapa como HTML
                ruta_mapa = f"ruta_mapa_{source_vertex}_{dest_vertex}.html"
                m.save(ruta_mapa)
                print(f"Mapa guardado como {ruta_mapa}")

                # Mostrar el mapa
                display(HTML(ruta_mapa))
                


    elif opcion == "3":
        break
    else:
        print("Opción no válida. Por favor, seleccione 1 o 2 para Mostrar información o Salir.")
