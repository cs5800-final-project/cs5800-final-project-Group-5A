'''
This is the driver script for the scenario 2.
'''

from data_loader import *
from algorithm_1_dijkstra import *
from map_generator import *
import osmnx as ox
import score_system_utility as ssu
import json as js
import time
import itertools

MUSEUM_FILE_PATH = 'data/manhattan_ny_museums.csv'
AIRBNB_FILE_PATH = 'data/new_york_airbnb_2024.csv'
AIRBNB_NODES_FILE_PATH = 'data/airbnb_nodes.json'
NETWORK_FILE_PATH = 'data/manhattan_road_network.graphml'
SHORTEST_DISTANCES_FILE_PATH = 'data/shortest_distances.json'


# Allow the user to select museums
def user_select_museums(museum_data, num_museums=5):
    print("\nAvailable Museums:")
    for idx, row in museum_data.iterrows():
        print(f"{idx}: {row['name']}")

    print(f"\nPlease select {num_museums} museums by their numbers (comma-separated):")
    while True:
        try:
            selections = input("> ").split(",")
            selected_indices = [int(idx.strip()) for idx in selections]
            if len(selected_indices) != num_museums:
                print(f"You must select exactly {num_museums} museums. Try again.")
                continue
            if any(idx < 0 or idx >= len(museum_data) for idx in selected_indices):
                print("Invalid selection. Ensure your choices are within the valid range.")
                continue
            selected_museums = museum_data.iloc[selected_indices]
            print("\nSelected Museums:")
            print(selected_museums[['name', 'lat', 'lon']])
            return selected_museums
        except ValueError:
            print("Invalid input. Please enter only numbers separated by commas. Try again.")
        except KeyError:
            print("The selected indices are invalid. Try again.")
        except Exception as e:
            print(f"Unexpected error: {e}. Try again.")


def find_optimal_airbnb_preload(airbnb_data, museum_data, road_network):
    current = time.time()
    preload = js.load(open(SHORTEST_DISTANCES_FILE_PATH, 'r'))
    
    # Find the nearest node in the road network for each Airbnb and museum
    airbnb_nodes = js.load(open(AIRBNB_NODES_FILE_PATH, "r"))
    museum_nodes = [
        ox.distance.nearest_nodes(road_network, row['lon'], row['lat']) for _, row in museum_data.iterrows()
    ]
    
    # Compute total distance for each Airbnb
    optimal_airbnb = None
    min_total_distance = float('inf') # Initialize with infinity
    
    for airbnb, airbnb_node in zip(airbnb_data.to_dict('records'), airbnb_nodes):
        # Get shortest distances to museum nodes only
        shortest_distances = 0
        for museum_node in museum_nodes:
            shortest_distances += preload.get(str(airbnb_node), {}).get(str(museum_node), float('inf'))
        
        if shortest_distances < min_total_distance:
            min_total_distance = shortest_distances
            optimal_airbnb = airbnb
    # Extract only the required fields for the result
    result_airbnb = {
        "id": optimal_airbnb["id"],
        "name": optimal_airbnb.get("name", "N/A"),  # If "name" is not in the data, return "N/A"
        "longitude": optimal_airbnb["longitude"],
        "latitude": optimal_airbnb["latitude"]
    }
    print(f"Time taken to find the optimal airbnb with preload data: {time.time() - current:.2f} seconds")
    return {"optimal_airbnb": result_airbnb, "total_distance": min_total_distance}


def bruteforce_shortest_path(airbnb_data, museum_data):
    preload = js.load(open(SHORTEST_DISTANCES_FILE_PATH, 'r'))
    airbnb_nodes = js.load(open(AIRBNB_NODES_FILE_PATH, "r"))
    museum_nodes = [
        ox.distance.nearest_nodes(road_network, row['lon'], row['lat']) for _, row in museum_data.iterrows()
    ]
    perm_list = list(itertools.permutations(museum_nodes))
    min_total_distance = float('inf')
    optimal_airbnb = None
    current = time.time()
    for airbnb, airbnb_node in zip(airbnb_data.to_dict('records'), airbnb_nodes):
        for perm in perm_list:
            total_distance = 0
            for i in range(len(perm) - 2):
                total_distance += preload.get(str(perm[i]), {}).get(str(perm[i + 1]), float('inf'))
            total_distance += preload.get(str(airbnb_node), {}).get(str(perm[0]), float('inf'))
            total_distance += preload.get(str(airbnb_node), {}).get(str(perm[-1]), float('inf'))
            if total_distance < min_total_distance:
                min_total_distance = total_distance
                optimal_airbnb = airbnb
    result_airbnb = {
    "id": optimal_airbnb["id"],
    "name": optimal_airbnb.get("name", "N/A"),  # If "name" is not in the data, return "N/A"
    "longitude": optimal_airbnb["longitude"],
    "latitude": optimal_airbnb["latitude"]
    }
    print(f"Time taken to find optimal airbnb with brute force: {time.time() - current:.2f} seconds")

    return {"optimal_airbnb": result_airbnb, "total_distance": min_total_distance}


if __name__ == "__main__":
    try:
        # Load museum data
        print("\nLoading Museum data...")
        museum_data = load_museum_data(MUSEUM_FILE_PATH)

        # Let the user select museums
        print("\nSelecting museums...")
        selected_museums = user_select_museums(museum_data, 5)

        # Load Airbnb data (assuming it's a CSV file with latitude and longitude columns)
        print("\nLoading Airbnb data...")
        airbnb_data = load_airbnb_data(AIRBNB_FILE_PATH)
        
        # Load road network using OSMnx
        print("\nLoading road network...")
        road_network = ox.load_graphml(NETWORK_FILE_PATH)

        print("\nFinding the optimal Airbnb with preload data...")
        result = find_optimal_airbnb_preload(airbnb_data, selected_museums, road_network)
        # Print only the required details
        optimal_airbnb = result['optimal_airbnb']
        print(f"Optimal Airbnb:")
        print(f"Airbnb id: {optimal_airbnb['id']}")
        print(f"Name: {optimal_airbnb['name']}")
        print(f"Latitude: {optimal_airbnb['latitude']}")
        print(f"Longitude: {optimal_airbnb['longitude']}")
        print(f"Total Distance: {result['total_distance']} meters")

        print("\nFinding the optimal Airbnb with brute force...")
        result = bruteforce_shortest_path(airbnb_data, selected_museums)
        # Print only the required details
        optimal_airbnb = result['optimal_airbnb']
        print(f"Optimal Airbnb:")
        print(f"Airbnb id: {optimal_airbnb['id']}")
        print(f"Name: {optimal_airbnb['name']}")
        print(f"Latitude: {optimal_airbnb['latitude']}")
        print(f"Longitude: {optimal_airbnb['longitude']}")
        print(f"Total Distance: {result['total_distance']} meters")

        # Generate the map
        # print("\nGenerating map...")
        # map_object = generate_map(selected_museums, optimal_airbnb, road_network)
        # map_object.save("map.html")
        # print("Map generated successfully!")
        
    
    except Exception as e:
        print(f"Error: {e}")
   