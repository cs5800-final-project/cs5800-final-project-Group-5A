'''
This file contains functions to load data from csv files.
'''

import pandas as pd

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

