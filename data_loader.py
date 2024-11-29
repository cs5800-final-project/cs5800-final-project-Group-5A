import pandas as pd
import geopandas as gpd
import score_system_utility as ssu

def load_airbnb_data(file_path):
    airbnb_data = pd.read_csv(file_path)
    airbnb_data.columns = airbnb_data.columns.str.strip()
    airbnb_data = airbnb_data[airbnb_data['neighbourhood_group'] == "Manhattan"]
    airbnb_data = airbnb_data[['id', 'latitude', 'longitude', 'rating']]
    airbnb_data['rating'] = pd.to_numeric(airbnb_data['rating'], errors='coerce')
    airbnb_data['rating_score'] = None
    airbnb_data['crime'] = None
    airbnb_data['crime_score'] = None
    airbnb_data['distance'] = None
    airbnb_data['distance_score'] = None
    airbnb_data['overall_score'] = None
    return airbnb_data[['id', 'latitude', 'longitude', 'rating', 'rating_score', 'crime', 'crime_score', 'distance', 'distance_score', 'overall_score']]

def load_museum_data(file_path):
    museum_data = pd.read_csv(file_path)
    museum_data.columns = museum_data.columns.str.strip()
    museum_data = museum_data[['name', 'lat', 'lon']]
    return museum_data[['name', 'lat', 'lon']]

def load_felony_data(file_path):
    crime_data = pd.read_csv(file_path)
    crime_data.columns = crime_data.columns.str.strip()
    crime_data = crime_data[['CMPLNT_NUM', 'Latitude', 'Longitude', 'Lat_Lon']]
    return crime_data[['CMPLNT_NUM', 'Latitude', 'Longitude', 'Lat_Lon']]

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
