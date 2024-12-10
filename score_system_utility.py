'''
This file contains utility functions for the scoring system.
'''

import math
import rtree as rt
import pandas as pd

def radius_to_lat_lon_diff(radius_meters, latitude):
    # Approximate latitude difference
    lat_diff = radius_meters / 111000  # 1 degree latitude ≈ 111 km
    
    # Approximate longitude difference (adjusted by cos(latitude))
    lon_diff = radius_meters / (111000 * math.cos(math.radians(latitude)))
    
    return lat_diff, lon_diff

def build_rtree_index(crime_data):
    return rt.index.Index(((_, (row["Longitude"], row["Latitude"], row["Longitude"], row["Latitude"]), None) for _, row in crime_data.iterrows()))

def count_crimes_within_radius(rtree_index, latitude, longitude, radius_meters):
    lat_diff, lon_diff = radius_to_lat_lon_diff(radius_meters, latitude)
    bbox = (longitude - lon_diff, latitude - lat_diff, longitude + lon_diff, latitude + lat_diff)
    hits = list(rtree_index.intersection(bbox, objects=True))
    return len(hits)

def assign_rating_score(airbnb_data):
    max_rating = airbnb_data['rating'].max()
    min_rating = airbnb_data['rating'].min()
    q25 = airbnb_data['rating'].quantile(0.25)
    q50 = airbnb_data['rating'].quantile(0.50)
    q75 = airbnb_data['rating'].quantile(0.75)
    # if the rating is within the first quartile, assign a score of 0
    # if the rating is within the second quartile, assign a score of 40
    # if the rating is within the third quartile, assign a score of 60
    # if the rating is within the fourth quartile, assign a score of 80
    # if the rating is the maximum rating, assign a score of 100
    for index, row in airbnb_data.iterrows():
        if pd.isna(row['rating']):
            airbnb_data.loc[index, 'rating_score'] = 50
        if row['rating'] == max_rating:
            airbnb_data.loc[index, 'rating_score'] = 100
        if row['rating'] >= q75:
            airbnb_data.loc[index, 'rating_score'] = 80
        elif row['rating'] >= q50:
            airbnb_data.loc[index, 'rating_score'] = 60
        elif row['rating'] >= q25:
            airbnb_data.loc[index, 'rating_score'] = 40
        elif row['rating'] == min_rating:
            airbnb_data.loc[index, 'rating_score'] = 0
        else:
            airbnb_data.loc[index, 'rating_score'] = 20
    
def assign_distance(airbnb_data, id, distance):
    airbnb_data.loc[airbnb_data['id'] == id, 'distance'] = distance

def assign_distance_score(airbnb_data):
    max_distance = airbnb_data['distance'].max()
    min_distance = airbnb_data['distance'].min()
    q25 = airbnb_data['distance'].quantile(0.25)
    q50 = airbnb_data['distance'].quantile(0.50)
    q75 = airbnb_data['distance'].quantile(0.75)
    # if the distance is within the first quartile, assign a score of 70
    # if the distance is within the second quartile, assign a score of 60
    # if the distance is within the third quartile, assign a score of 40
    # if the distance is within the fourth quartile, assign a score of 10
    # if the distance is the maximum distance, assign a score of 0
    for index, row in airbnb_data.iterrows():
        if row['distance'] == max_distance:
            airbnb_data.loc[index, 'distance_score'] = 0
        elif row['distance'] >= q75:
            airbnb_data.loc[index, 'distance_score'] = 20
        elif row['distance'] >= q50:
            airbnb_data.loc[index, 'distance_score'] = 40
        elif row['distance'] >= q25:
            airbnb_data.loc[index, 'distance_score'] = 60
        elif row['distance'] != min_distance:
            airbnb_data.loc[index, 'distance_score'] = 80
        else:
            airbnb_data.loc[index, 'distance_score'] = 100

def assign_crime(airbnb_data, id, crime_count):
    airbnb_data.loc[airbnb_data['id'] == id, 'crime'] = crime_count

def assign_crime_score(airbnb_data):
    max_crime = airbnb_data['crime'].max()
    min_crime = airbnb_data['crime'].min()
    q25 = airbnb_data['crime'].quantile(0.25)
    q50 = airbnb_data['crime'].quantile(0.50)
    q75 = airbnb_data['crime'].quantile(0.75)
    # if the crime count is within the first quartile, assign a score of 100
    # if the crime count is within the second quartile, assign a score of 80
    # if the crime count is within the third quartile, assign a score of 60
    # if the crime count is within the fourth quartile, assign a score of 40
    for index, row in airbnb_data.iterrows():
        if row['crime'] == max_crime:
            airbnb_data.loc[index, 'crime_score'] = 0
        elif row['crime'] == min_crime:
            airbnb_data.loc[index, 'crime_score'] = 100
        elif row['crime'] >= q75:
            airbnb_data.loc[index, 'crime_score'] = 20
        elif row['crime'] >= q50:
            airbnb_data.loc[index, 'crime_score'] = 40
        elif row['crime'] >= q25:
            airbnb_data.loc[index, 'crime_score'] = 60
        else:
            airbnb_data.loc[index, 'crime_score'] = 80

def assign_overall_score(airbnb_data, distance_weight, crime_weight, rating_weight):
    for index, row in airbnb_data.iterrows():
        airbnb_data.loc[index, 'overall_score'] = row['rating_score'] * rating_weight / 100 + distance_weight * row['distance_score'] / 100 + crime_weight * row['crime_score'] / 100
    
def return_top_n_airbnb(airbnb_data, n):
    return airbnb_data.nlargest(n, 'overall_score')