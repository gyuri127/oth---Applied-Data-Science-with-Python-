#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install geopy')
get_ipython().system('pip install gmaps')
import chardet
import pandas as pd
import gmaps
from geopy.distance import great_circle
from googlemaps import Client
from IPython.display import display


#Real-time data of bike stations
import requests
import json


# Set Google Maps API Key
gmaps.configure(api_key='AIzaSyCXi1V53ZRrZ7evMN1Gay1UWLCIr6h38KM') 
gmaps_client = Client(key='AIzaSyCXi1V53ZRrZ7evMN1Gay1UWLCIr6h38KM')





# In[4]:


### Data Loading Module
def load_station_data(file_path):

    return pd.read_csv(file_path, encoding='Windows-1252')



# Data Processing Module 
def process_data(original_df, selected_columns):
    
    # Create a DataFrame with the first row removed
    df_without_first_row = original_df.iloc[1:].reset_index(drop=True)
    # Create a new DataFrame 
    df = df_without_first_row[selected_columns].copy()
    # Create a new data frame with Status == Active
    active_df = df[df['Status'] == 'Active']
    return active_df


#Real-Time Data Fetching Module
def fetch_realtime_data(url):
    # Get JSON data from URL
    response = requests.get(url)
    # Verify that data responded successfully
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data. Status Code: {response.status_code}")



#Real-Time Data Processing Module
def create_realtime_df(stations_data):
    station_ids = []
    num_docks_availables = []
    num_bikes_availables = []

    for station in stations_data:
        station_id = int(station['station_id'].replace('bcycle_lametro_', ''))
        station_ids.append(station_id)
        num_docks_availables.append(station['num_docks_available'])
        num_bikes_availables.append(station['num_bikes_available'])

    realtime_df = pd.DataFrame({
        'Station_ID': station_ids,
        'Num_docks_available': num_docks_availables,
        'Num_bikes_available': num_bikes_availables,
    })
    return realtime_df



    
    
# User Interaction Module
def get_user_selection():
    while True:
        print("Select the desired option:")
        print("1. Find the nearest bike station where you can rent a bike")
        print("2. Find the nearest bike station where you can return a bike")
        print("3. Draw route from departure to destination")
        
        choice = input("Choice: ")
        
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("\n Invalid choice.\n")

    
    

def get_user_input(choice):

    if choice in ['1', '2']:
        # Latitude of the departure point
        latitude = float(input("Enter the latitude of the current location:"))
        # Longitutde of the departure point
        longitude = float(input("Enter the longitude of the current location: "))
        k = int(input(" Enter the number of stations you want to find:"))
        
        return (latitude, longitude), k


    elif choice == '3':
       
        k=0
        # departure point
        latitude = float(input("Enter the latitude of source location:"))
        longitude = float(input("Enter the longitude of the source location: "))
        
        # destination location
        destination_latitude = float(input("Enter the latitude of the destination location: "))
        destination_longitude = float(input("Enter the longitude of the destination location: "))
        return (latitude, longitude), k, (destination_latitude, destination_longitude)



# Distance Calculation Module
def calculate_distance(loc1, loc2):
    return great_circle(loc1, loc2).kilometers

#Nearest Stations Finding Module
def find_nearest_stations(user_location, stations, k, is_borrow):
    if is_borrow:
        available_stations = stations[stations['Num_bikes_available'] > 0].copy()
    else:
        available_stations = stations[stations['Num_docks_available'] > 0].copy()
    
    available_stations['Distance'] = available_stations.apply(
        lambda row: calculate_distance(user_location, (row['Latitude'], row['Longitude'])),
        axis=1
    )
    
    nearest_stations = available_stations.nsmallest(k, 'Distance')
    return nearest_stations


#Route Mapping Module
def create_route_map(start_location, nearest_start_station, nearest_end_station, end_location):

     # Create the map
    fig = gmaps.figure()
 
    
    if nearest_start_station != nearest_end_station:
        walking_directions1 = gmaps.directions_layer(
            start=start_location, end=nearest_start_station, travel_mode="WALKING")
        fig.add_layer(walking_directions1)
    
        bicycling_directions = gmaps.directions_layer(
            start=nearest_start_station, end=nearest_end_station, travel_mode="BICYCLING")
        fig.add_layer(bicycling_directions)
        
        
        walking_directions2 = gmaps.directions_layer(
            start=nearest_end_station, end=end_location, travel_mode="WALKING")
        fig.add_layer(walking_directions2)
        
    else :

        walking_directions1 = gmaps.directions_layer(
            start=start_location, end=end_location, travel_mode="WALKING")
        fig.add_layer(walking_directions1)


    return fig




def main():
    
      
    # Information file path of the bike station
    file_path = "station1.csv"
    # Real-time data of bike stations
    url = "https://gbfs.bcycle.com/bcycle_lametro/station_status.json"
    # List of required column names
    selected_columns = ['Station_ID', 'Station_Name', 'Status', 'Latitude' , 'Longitude']
    
    # Load and process station data
    original_df = load_station_data(file_path)
    active_df = process_data(original_df, selected_columns)
    # Fetch real-time data
    realtime_data = fetch_realtime_data(url)
    # Extract necessary information
    stations_data = realtime_data['data']['stations']
    realtime_df = create_realtime_df(stations_data)

  
    
    choice = get_user_selection()
    user_location, k, *destination = get_user_input(choice)
    
    # Convert to tuple
    if destination:
        destination = destination[0]
    
    # Merge DataFrames
    merged_df = pd.merge(active_df, realtime_df, on='Station_ID')

    if choice == '1':
        nearest_stations = find_nearest_stations(user_location, merged_df, k, is_borrow=True)
        print(f"\nThe closest {k} stations to borrow a bike are as follows:")
        print(nearest_stations[[ 'Station_Name', 'Distance', 'Num_bikes_available']].to_string(index=False))
    
    elif choice == '2':
        nearest_stations = find_nearest_stations(user_location, merged_df, k, is_borrow=False)
        print(f"The closest {k} stations to return a bike are as follows:")
        print(nearest_stations[['Station_Name', 'Distance', 'Num_docks_available']].to_string(index=False))
    
    elif choice == '3':
        # Find the nearest bicycle station from the current location
        nearest_start_station = find_nearest_stations(user_location, merged_df, 1, True).iloc[0]
        nearest_start_station_location = (nearest_start_station['Latitude'], nearest_start_station['Longitude'])

        # Find the nearest bicycle station from the destination
        nearest_end_station = find_nearest_stations(destination, merged_df, 1, False).iloc[0]
        nearest_end_station_location = (nearest_end_station['Latitude'], nearest_end_station['Longitude'])
        
        # Generate a route map
        route_map = create_route_map(user_location, nearest_start_station_location, nearest_end_station_location, destination)

        # disgplay route map
        display(route_map)

if __name__ == "__main__":
    main()


# In[ ]:




