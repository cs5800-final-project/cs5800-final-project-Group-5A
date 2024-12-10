from data_loader import *
from dijkstra_algorithm import *
from map_generator import *
import osmnx as ox
import score_system_utility as ssu
import json as js
import time
import bellman_ford as bf
import itertools

MUSEUM_FILE_PATH = 'data/manhattan_ny_museums.csv'
AIRBNB_FILE_PATH = 'data/new_york_airbnb_2024.csv'
FELONY_FILE_PATH = 'data/NYPD_Felony_Complaint_Data_2023.csv'
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


def find_optimal_airbnb_dijkstra(airbnb_data, museum_data, road_network, rtree_index):
    adjacency_list = convert_to_adjacency_list(road_network)
    
    # Find the nearest node in the road network for each Airbnb and museum
    airbnb_nodes = js.load(open(AIRBNB_NODES_FILE_PATH, "r"))
    museum_nodes = [
        ox.distance.nearest_nodes(road_network, row['lon'], row['lat']) for _, row in museum_data.iterrows()
    ]
    
    # Compute total distance for each Airbnb
    current = time.time()
    for airbnb, airbnb_node in zip(airbnb_data.to_dict('records'), airbnb_nodes):
        # Get shortest distances to museum nodes only
        shortest_distances = dijkstra(adjacency_list, airbnb_node, museum_nodes)
        total_distance = sum(shortest_distances.values())
        
        ssu.assign_distance(airbnb_data, airbnb['id'], total_distance)
        ssu.assign_crime(airbnb_data, airbnb['id'], ssu.count_crimes_within_radius(rtree_index, airbnb['latitude'], airbnb['longitude'], 500))
    score_and_rank_airbnbs(airbnb_data)
    print(f"Time taken to find optimal airbnb: {time.time() - current:.2f} seconds")


def find_optimal_airbnb_bellman_ford(airbnb_data, museum_data, road_network, rtree_index):
    adjacency_list = convert_to_adjacency_list(road_network)
    
    # Find the nearest node in the road network for each Airbnb and museum
    airbnb_nodes = js.load(open(AIRBNB_NODES_FILE_PATH, "r"))
    museum_nodes = [
        ox.distance.nearest_nodes(road_network, row['lon'], row['lat']) for _, row in museum_data.iterrows()
    ]
    
    # Compute total distance for each Airbnb
    optimal_airbnb = None
    min_total_distance = float('inf') # Initialize with infinity
    current = time.time()
    for airbnb, airbnb_node in zip(airbnb_data.to_dict('records'), airbnb_nodes):
        # Get shortest distances to museum nodes only
        edge_list = bf.adjacency_list_to_edge_list(adjacency_list)
        shortest_distances = bf.bellman_ford(adjacency_list, edge_list, airbnb_node, museum_nodes)
        total_distance = sum(shortest_distances.values())
        
        ssu.assign_distance(airbnb_data, airbnb['id'], total_distance)
        ssu.assign_crime(airbnb_data, airbnb['id'], ssu.count_crimes_within_radius(rtree_index, airbnb['latitude'], airbnb['longitude'], 500))
        
        if total_distance < min_total_distance:
            min_total_distance = total_distance
            optimal_airbnb = airbnb
    print(f"Time taken to find optimal airbnb using bf: {time.time() - current:.2f}")


def score_and_rank_airbnbs(airbnb_data, distance_weight=50, crime_weight=40, rating_weight=10, top_n=3):
    # Assign scores
    ssu.assign_rating_score(airbnb_data)
    ssu.assign_distance_score(airbnb_data)
    ssu.assign_crime_score(airbnb_data)
    ssu.assign_overall_score(airbnb_data, distance_weight, crime_weight, rating_weight)
    
    # Sort the Airbnb data by overall score in descending order
    sorted_airbnb_data = airbnb_data.sort_values(by='overall_score', ascending=False)
    
    # Select relevant columns for display
    sorted_airbnb_data = sorted_airbnb_data[['id', 'rating', 'crime', 'distance', 'overall_score']]
    
    # Print the top N Airbnbs based on overall score
    print(f"\nTop {top_n} Airbnb based on overall score:")
    print(sorted_airbnb_data.head(top_n))


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
        
        # Load crime data
        print("\nLoading crime data...")
        crime_data = load_felony_data(FELONY_FILE_PATH)
        rtree_index = ssu.build_rtree_index(crime_data)

        # Find the optimal Airbnb
        print("\nFinding the optimal Airbnbs using Dijkstra...")
        find_optimal_airbnb_dijkstra(airbnb_data, selected_museums, road_network, rtree_index)

        print("\nFinding the optimal Airbnbs using Bellman-Ford...")
        find_optimal_airbnb_bellman_ford(airbnb_data, selected_museums, road_network, rtree_index)
        
        # Generate the map
        # print("\nGenerating map...")
        # map_object = generate_map(selected_museums, optimal_airbnb, road_network)
        # map_object.save("map.html")
        # print("Map generated successfully!")
        
    
    except Exception as e:
        print(f"Error: {e}")
   