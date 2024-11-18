import folium
from folium.plugins import MarkerCluster
import osmnx as ox

def generate_map(selected_museums, optimal_airbnb, road_network):
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

    # Add optimal Airbnb marker
    folium.Marker(
        location=[optimal_airbnb['latitude'], optimal_airbnb['longitude']],
        popup=f"Optimal Airbnb (ID: {optimal_airbnb['id']}, Name: {optimal_airbnb['name']})",
        icon=folium.Icon(color='green', icon='home')
    ).add_to(map_object)

    # Plot shortest paths
    for _, row in selected_museums.iterrows():
        museum_node = ox.distance.nearest_nodes(road_network, row['lon'], row['lat'])
        airbnb_node = ox.distance.nearest_nodes(road_network, optimal_airbnb['longitude'], optimal_airbnb['latitude'])

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