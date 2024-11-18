import matplotlib.pyplot as plt
import osmnx as ox

def generate_static_map(selected_museums, optimal_airbnb, road_network):
    # Plot the road network
    fig, ax = ox.plot_graph(road_network, show=False, close=False, bgcolor="white", node_size=0, edge_color="gray")

    # Add markers for museums
    for _, row in selected_museums.iterrows():
        ax.scatter(row['lon'], row['lat'], c='blue', s=100, label="Museum" if 'Museum' not in ax.get_legend_handles_labels()[1] else "")

    # Add a marker for the optimal Airbnb
    ax.scatter(
        optimal_airbnb["longitude"], optimal_airbnb["latitude"],
        c='green', s=150, marker="*", label="Optimal Airbnb"
    )

    # Draw shortest paths
    for _, row in selected_museums.iterrows():
        museum_node = ox.distance.nearest_nodes(road_network, row['lon'], row['lat'])
        airbnb_node = ox.distance.nearest_nodes(road_network, optimal_airbnb['longitude'], optimal_airbnb['latitude'])

        # Compute shortest path
        path = ox.shortest_path(road_network, airbnb_node, museum_node, weight='length')
        
        # Extract path coordinates
        path_coords = [(road_network.nodes[node]['x'], road_network.nodes[node]['y']) for node in path]
        path_lons, path_lats = zip(*path_coords)
        
        # Plot the path
        ax.plot(path_lons, path_lats, c='red', linewidth=2, label="Shortest Path" if 'Shortest Path' not in ax.get_legend_handles_labels()[1] else "")

    # Add legend
    ax.legend(loc="upper right", fontsize=8)

    # Set titles and labels
    ax.set_title("Optimal Airbnb and Selected Museums", fontsize=14)
    ax.set_xlabel("Longitude", fontsize=10)
    ax.set_ylabel("Latitude", fontsize=10)

    # Save the figure
    plt.savefig("optimal_airbnb_static_map.png", dpi=300)
    print("Static map saved as 'optimal_airbnb_static_map.png'.")

    # Show the plot
    plt.show()