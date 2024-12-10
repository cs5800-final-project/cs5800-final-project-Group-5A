'''
This is the implementation of the Floyd-Warshall algorithm.
'''

import osmnx as ox

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

# adjacency_list = convert_to_adjacency_list(road_network)

def floyd_warshall(adjacency_list) -> dict:
    # Initialize the distance dictionary with infinity
    nodes = list(adjacency_list.keys())
    dist = {node: {neighbor: float('inf') for neighbor in nodes} for node in nodes}
    
    # Set the distance from a node to itself to 0
    for node in nodes:
        dist[node][node] = 0
    
    # Set the initial distances based on the adjacency list
    for node, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors.items():
            dist[node][neighbor] = weight
    
    # Floyd-Warshall algorithm
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist