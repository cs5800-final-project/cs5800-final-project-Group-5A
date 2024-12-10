'''
This file loaded the road network of Manhattan and the nodes of Airbnb data, and saves them as local files in the 'data' folder.
'''

import osmnx as ox
import data_loader as dl
import json as js
# Load and Save the road network of Manhattan
ROAD_NETWORK = ox.graph_from_place("Manhattan, New York, USA", network_type="drive")
ox.save_graphml(ROAD_NETWORK, filepath="manhattan_road_network.graphml")

# Load Airbnb data and save the nodes
AIRBNB_FILE_PATH = 'new_york_airbnb_2024.csv'
airbnb_data = dl.load_airbnb_data(AIRBNB_FILE_PATH)

airbnb_nodes = [
        ox.distance.nearest_nodes(ROAD_NETWORK, row['longitude'], row['latitude']) for _, row in airbnb_data.iterrows()
    ]

js.dump(airbnb_nodes, open("data/airbnb_nodes.json", "w"))