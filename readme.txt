1. Project Title

Metro Bike Share: Los Angeles Bike Station Live Feed


2.  Project Description

This project is a Python application that helps users find the nearest bike stations where they can rent or return bikes, and visualize routes using both biking and walking modes from their departure to destination.


3.  Features

- Find the nearest bike station from current location to rent a bike.
- Find the nearest bike station from current location to return a bike.
- Visualize the route from departure to destination.

4. Installation and Setup

pip install geopy gmaps pandas requests googlemaps


5.  Usage

Location coordinates (latitude, longitude) must be entered for the following options:

1) Rent a Bike
Select the desired option:
1. Find the nearest bike station where you can rent a bike
2. Find the nearest bike station where you can return a bike
3. Draw route from departure to destination
Choice: 1
Enter the latitude of the current location: 34.052235
Enter the longitude of the current location: -118.243683
Enter the number of stations you want to find: 3

2) Return a Bike
Select the desired option:
1. Find the nearest bike station where you can rent a bike
2. Find the nearest bike station where you can return a bike
3. Draw route from departure to destination
Choice: 2
Enter the latitude of the current location: 34.052235
Enter the longitude of the current location: -118.243683
Enter the number of stations you want to find: 3

3) View Route on Google Maps
Select the desired option:
1. Find the nearest bike station where you can rent a bike
2. Find the nearest bike station where you can return a bike
3. Draw route from departure to destination
Choice: 3
Enter the latitude of source location: 34.052235
Enter the longitude of the source location: -118.243683
Enter the latitude of the destination location: 34.052235
Enter the longitude of the destination location: -118.243683


