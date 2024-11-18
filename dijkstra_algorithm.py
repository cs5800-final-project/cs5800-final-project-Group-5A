import osmnx as ox
import heapq

# Load the road network of Manhattan
ROAD_NETWORK = ox.graph_from_place("Manhattan, New York, USA", network_type="drive")

# Convert OSMnx graph to adjacency list
def convert_to_adjacency_list(ROAD_NETWORK):
    adjacency_list = {}
    for node in ROAD_NETWORK.nodes:
        adjacency_list[node] = {}
        for neighbor, data in ROAD_NETWORK[node].items():
            edge_data = list(data.values())[0]
            weight = edge_data.get('length', 1)
            adjacency_list[node][neighbor] = weight
    return adjacency_list

adjacency_list = convert_to_adjacency_list(ROAD_NETWORK)

# Implement Dijkstra algorithm
def dijkstra(adjacency_list, start_node, target_nodes):
    shortest_distances = {node: float('inf') for node in target_nodes}
    priority_queue = [(0, start_node)]  # (distance, node)
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Check if this node is one of the target nodes
        if current_node in target_nodes:
            shortest_distances[current_node] = current_distance
            # Stop if all target nodes are found
            if len(visited.intersection(target_nodes)) == len(target_nodes):
                break
        
        # Update distances to neighbors
        for neighbor, weight in adjacency_list.get(current_node, {}).items():
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_distance + weight, neighbor))
    
    return shortest_distances