'''
This is implementation of Dijkstra algorithm.
'''

import osmnx as ox
import heapq

# Load the road network of Manhattan
# ROAD_NETWORK = ox.graph_from_place("Manhattan, New York, USA", network_type="drive")

# Convert OSMnx graph to adjacency list
def convert_to_adjacency_list(road_network) -> dict:
    adjacency_list = {}
    for node in road_network.nodes:
        adjacency_list[node] = {}
        for neighbor, data in road_network[node].items():
            edge_data = list(data.values())[0]
            weight = edge_data.get('length', 1)
            adjacency_list[node][neighbor] = weight
    return adjacency_list

# adjacency_list = convert_to_adjacency_list(ROAD_NETWORK)

# Implement Dijkstra algorithm
def dijkstra(adjacency_list, start_node, target_nodes) -> dict:
    # A dictionary to store the shortest distance to each target node
    # Initialize shortest distances to all target nodes as infinity
    shortest_distances = {node: float('inf') for node in target_nodes}
    priority_queue = [(0, start_node)]  # A list of tuples, (distance, start node)
    visited = set() # Prevents revisiting nodes and ensures the algorithm terminates
    
    while priority_queue:
        # Removes and returns the node with the smallest distance from the priority queue (min-heap)
        current_distance, current_node = heapq.heappop(priority_queue) 
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Check if this node is one of the target nodes
        if current_node in target_nodes:
            # If the current_node is one of the target nodes, update its shortest distance in shortest_distances
            shortest_distances[current_node] = current_distance
            # Stop if all target nodes are found
            if len(visited.intersection(target_nodes)) == len(target_nodes):
                break
        
        # Update distances to neighbors
        # Retrieves the neighbors of the current_node and their edge weights
        for neighbor, weight in adjacency_list.get(current_node, {}).items():
            # For each unvisited neighbor:
            # Calculate its potential new shortest distance as current_distance + weight
            # Add it to the priority queue for future processing
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_distance + weight, neighbor))
    
    return shortest_distances