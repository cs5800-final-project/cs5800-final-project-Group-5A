import osmnx as ox
import heapq
import data_loader as dl
import time
import json as js

AIREBNB_NODES_FILE_PATH = 'airbnb_nodes.json'
NETWORK_FILE_PATH = 'manhattan_road_network.graphml'
MUSEUM_FILE_PATH = 'manhattan_ny_museums.csv'

# Convert OSMnx graph to adjacency list
def convert_to_adjacency_list(ROAD_NETWORK) -> dict:
    adjacency_list = {}
    for node in ROAD_NETWORK.nodes:
        adjacency_list[node] = {}
        for neighbor, data in ROAD_NETWORK[node].items():
            edge_data = list(data.values())[0]
            weight = edge_data.get('length', 1)
            adjacency_list[node][neighbor] = weight
    return adjacency_list

# Implement Dijkstra algorithm
def dijkstra(adjacency_list, adjacency_list_all, start_node, target_node) -> dict:
    # A dictionary to store the shortest distance to each target node
    # Initialize shortest distances to all target nodes as infinity
    if str(target_node) in adjacency_list_all[str(start_node)]:
        return
    priority_queue = [(0, start_node)]  # A list of tuples, (distance, start node)
    visited = set() # Prevents revisiting nodes and ensures the algorithm terminates
    
    while priority_queue:
        # Removes and returns the node with the smallest distance from the priority queue (min-heap)
        current_distance, current_node = heapq.heappop(priority_queue) 
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        adjacency_list_all[str(start_node)][str(current_node)] = current_distance
        # Update distances to neighbors
        # Retrieves the neighbors of the current_node and their edge weights
        for neighbor, weight in adjacency_list.get(current_node, {}).items():
            # For each unvisited neighbor:
            # Calculate its potential new shortest distance as current_distance + weight
            # Add it to the priority queue for future processing
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_distance + weight, neighbor))
                
    

def main():
    # Load the road network of Manhattan
    road_network = ox.load_graphml(NETWORK_FILE_PATH)
    # load the museum data  
    museum_data = dl.load_museum_data(MUSEUM_FILE_PATH)

    # Convert the road network to an adjacency list
    adjacency_list = convert_to_adjacency_list(road_network)
    
    # Find the nearest node in the road network for each Airbnb and museum
    airbnb_nodes = js.load(open(AIREBNB_NODES_FILE_PATH, "r"))
    museum_nodes = [
        ox.distance.nearest_nodes(road_network, row['lon'], row['lat']) for _, row in museum_data.iterrows()
    ]
    '''    
    print(f"Number of museum nodes: {len(museum_nodes)}")
    set_museum_nodes = set(museum_nodes)
    set_airbnb_nodes = set(airbnb_nodes)
    set_intersection = set_museum_nodes.intersection(set_airbnb_nodes)
    print(f"Number of intersection nodes: {len(set_intersection)}")
    '''
    all_nodes = []
    all_nodes.extend(airbnb_nodes)
    all_nodes.extend(museum_nodes)
    adjacency_list_all = {}
    for node in all_nodes:
        adjacency_list_all[str(node)] = {}
    current = time.time()
    i = 1
    for airbnb_node in airbnb_nodes:
        # Get shortest distances to museum nodes only
        print(f"Airbnb node: ", airbnb_node, "#: ", i)    
        i += 1
        for node in museum_nodes:
            dijkstra(adjacency_list, adjacency_list_all, airbnb_node, node)
    for node in museum_nodes:
        for node1 in museum_nodes:
            if node != node1:
                dijkstra(adjacency_list, adjacency_list_all, node, node1)

    print(f"Time taken to build shortest distances: {time.time() - current:.2f}")

    js.dump(adjacency_list_all, open('shortest_distances.json', 'w'))

if __name__ == "__main__":
    main()