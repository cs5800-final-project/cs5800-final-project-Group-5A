### This repository is accompanying CS5800 Final Project Report of Group 5A
## Data
Local data is stored in the data folder  
**Note:**
Since the json file that stores all the distances is relatively big that requires Git Large File Storage go handle, in the case you don't want to bother with git lfs, rerun the utility file **shortest_path_for_all_nodes.py** to regenerate the cached shortest distances. It should only take seconds to put the file the data folder. 

## Files to run
**driver_local_scenario1.py:**
1. This file corresponds Scenario 1 in the report. 
2. It incorporated Dijkstra, Bellman-Ford, Floyd-Warshall algorithms. Bellman-Ford and Floyd-Warshall are currently short-circuited due to slow performances. If you want to see those two in action(...prompt blinking for hours), please go to main() to uncomment those lines. 
3. It uses cached airbnb nodes information to calculate shortest path. 
4. It recommonds airbnbs based on the scoring system.
5. To interact with the program, type 5 museums by their ID number, seperated by comma. 

**driver_local_scenario2.py**
1. This file corresponds to Scenario 2 in the report. You would see the result in the "Finding the optimal Airbnb with brute force..." section of the program output. 
2. The shortest path based on scenario 1 is also kept by this program for comparison, as shown in "Finding the optimal Airbnb with preload data" section of the program output. 
3. It incorporated Brute Force for Scenario 2. It does not incorporate the score system.
4. The program is using cached airbnb nodes as well as cached shortest distances
5. To interact with the program, type 5 museums by their ID number, seperated by comma. 

## Algorithms
Algorithms are stored in **algorithm_1_dijkstra.py**, **algorithm_2_bellman_ford.py**, and **algorithm_3_floyd_warshall.py**

## Score System
The scoring system's code is in **score_system_utility.py**

## Utilities
**data_loader.py**, **local_storage_utility.py** and **shortest_path_for_all_nodes.py**  are utilities. 
