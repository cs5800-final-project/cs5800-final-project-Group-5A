'''
This file generates a map containing the selected museums, the optimal Airbnb, and the shortest paths between them.
'''

import folium
from folium.plugins import MarkerCluster
import osmnx as ox

def generate_map(selected_museums, top_airbnbs, road_network):
    # Initialize the map centered on Manhattan
    center_lat = selected_museums['lat'].mean()
    center_lon = selected_museums['lon'].mean()
    map_object = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Add museum markers
    museum_cluster = MarkerCluster(name="Museums").add_to(map_object)
    for _, row in selected_museums.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"Museum: {row['name']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(museum_cluster)

    # Add markers for each of the top Airbnbs
    for _, airbnb in top_airbnbs.iterrows():
        folium.Marker(
            location=[airbnb['latitude'], airbnb['longitude']],
            popup=f"Airbnb (ID: {airbnb['id']}, Name: {airbnb['name']})",
            icon=folium.Icon(color='green', icon='home')
        ).add_to(map_object)

    # Plot shortest paths for each Airbnb
    for _, airbnb in top_airbnbs.iterrows():
        airbnb_node = ox.distance.nearest_nodes(road_network, airbnb['longitude'], airbnb['latitude'])
        for _, row in selected_museums.iterrows():
            museum_node = ox.distance.nearest_nodes(road_network, row['lon'], row['lat'])

            # Get shortest path
            path = ox.shortest_path(road_network, airbnb_node, museum_node, weight='length')

            # Extract coordinates from nodes
            path_coords = [(road_network.nodes[node]['y'], road_network.nodes[node]['x']) for node in path]

            # Add path to map
            folium.PolyLine(
                path_coords,
                color='red',
                weight=2,
                opacity=0.8,
                tooltip="Shortest Path"
            ).add_to(map_object)

    return map_object