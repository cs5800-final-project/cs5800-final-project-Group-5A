import pandas as pd
import geopandas as gpd

def load_airbnb_data(file_path):
    airbnb_data = pd.read_csv(file_path)
    airbnb_data.columns = airbnb_data.columns.str.strip()
    airbnb_data = airbnb_data[airbnb_data['neighbourhood_group'] == "Manhattan"]
    airbnb_data = airbnb_data[['id', 'latitude', 'longitude']]
    return airbnb_data[['id', 'latitude', 'longitude']]

def load_museum_data(file_path):
    museum_data = pd.read_csv(file_path)
    museum_data.columns = museum_data.columns.str.strip()
    museum_data = museum_data[['name', 'lat', 'lon']]
    return museum_data[['name', 'lat', 'lon']]


# def main():
#     # print("Loading Airbnb data...")
#     # airbnb_data = load_airbnb_data('new_york_airbnb_2024.csv')
#     # print("Airbnb Data Loaded Successfully!")
#     # print(airbnb_data.head())  # Preview the first 5 rows

#     print("\nLoading Museum data...")
#     museum_data = load_museum_data('manhattan_ny_museums.csv')
#     print("Museum Data Loaded Successfully!")
#     print(museum_data.head())  # Preview the first 5 rows

# if __name__ == "__main__":
#     main()
