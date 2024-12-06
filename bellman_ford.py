def adjacency_list_to_edge_list(adjacency_list):
    """
    Convert an adjacency list to an edge list.
    
    :param adjacency_list: The adjacency list representation of the graph
    :return: The edge list representation of the graph
    """
    edge_list = []
    for node, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors.items():
            edge_list.append((node, neighbor, weight))
    return edge_list


def bellman_ford(adjacency_list, edge_list, source, destinations):
    """
    Find the shortest distance from the source node to all destination nodes using Bellman-Ford algorithm.
    
    :param adjacency_list: The adjacency list representation of the graph
    :param source: The source node
    :param destinations: The list of destination nodes
    :return: A dictionary of shortest distances from the source node to all destination nodes
    """
    # Initialize distances from the source node to all other nodes as infinity
    shortest_distances = {node: float('inf') for node in destinations}
    distances = {node: float('inf') for node in adjacency_list}
    # print("distances: ", distances)
    distances[source] = 0
    # print(edge_list)
    # Relax edges repeatedly
    for _ in range(len(adjacency_list) - 1):
        j = 0
        # print("#: ", _, "of: ", len(adjacency_list) - 1)
        for u, v, w in edge_list:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                j = j + 1
        if j == 0:
            break
    for node in destinations:
        shortest_distances[node] = distances[node]
    return shortest_distances # Return the shortest distances to all destination nodes

'''
if __name__ == "__main__":
    # Load the road network of Manhattan
    adjacency_list = {
        0: {1: 1, 2: 4},
        1: {2: 2},
        2: {3: 1},
        3: {1: 3}
    }

    source = 0
    destinations = [1, 2, 3]
    shortest_distances = bellman_ford(adjacency_list, source, destinations)
    print(shortest_distances)
'''