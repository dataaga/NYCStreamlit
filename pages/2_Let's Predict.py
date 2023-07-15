import streamlit as st
import pandas as pd
import numpy as np
import time

import pickle
import lightgbm

st.title('Prediction of NYC Taxi Trip Duration')

st.markdown("""Welcome to the NYC Taxi Trip Duration Predictor!
            This tool utilizes a machine learning model using
            LGBMRegressor trained on various factors such as
            pickup and dropoff locations, passenger count,
            and other trip-specific details to predict the
            duration of your taxi journeys in the streets
            of New York City. Fill in your trip journey
            below and we'll guess trip duration!""")


st.subheader('Pick Your Vendor')

vendor = st.radio('Type of Vendor: ', ['Vendor 1', 'Vendor 2'])
if vendor == 'Vendor 1':
    vendor = 1
else:
    vendor = 2

# Pickup Date
st.subheader('Pickup & Dropoff Date')

pickup_datetime = st.date_input('Select pickup date')

# Dropoff Date
dropoff_datetime = st.date_input('Select dropoff date')

# Convert to Date
pickup_datetime = pd.to_datetime(pickup_datetime)
dropoff_datetime = pd.to_datetime(dropoff_datetime)

# Extracting Datetime to Hour
hour_pickup_datetime = pickup_datetime.hour
hour_dropoff_datetime = dropoff_datetime.hour

# Extracting Datetime to Day
day_pickup_datetime = pickup_datetime.day
day_dropoff_datetime = dropoff_datetime.day

# Extracting Datetime to Week
week_pickup_datetime= pickup_datetime.dayofweek
week_dropoff_datetime = dropoff_datetime.dayofweek

# Extracting Datetime to Month
month_pickup_datetime = pickup_datetime.month
month_dropoff_datetime = dropoff_datetime.month

# Number of Passenger Count
st.subheader('Number of Passenger')

passenger_count = st.slider('How many the Passenger?', 1, 9, 1)

st.subheader('New York Pickup Location')

# Disclaimer for map input
st.markdown("""Since streamlit version 1.2.4 doesn't have yet the map input
            feature like your fav ride-hailing app, it must be input manually :)""")

# New York Pickup to Dropoff Location
st.markdown("""Please note that this application focuses on taxi trips within
            the New York City area. The geographic boundaries for this service
            are limited to the following coordinates:
            Latitude Range: 40.63 to 40.85
            Longitude Range: -74.03
            When entering pickup and dropoff locations, please ensure that the
            latitude and longitude values fall within these boundaries.
            This restriction ensures that the predictions provided are relevant
            and accurate for taxi trips specifically within the New York City area.""")

pickup_latitude = st.number_input('Enter the latitude (40.63 ~ 40.85) for pickup location:', min_value=40.63, max_value=40.85)
pickup_longitude = st.number_input('Enter the longitude (-74.03 ~ -73.75) for pickup location:', min_value=-74.03, max_value=-73.75)

st.subheader('New York Dropoff Location')
dropoff_latitude = st.number_input('Enter the latitude (40.63 ~ 40.85) for dropoff location:', min_value=40.63, max_value=40.85)
dropoff_longitude = st.number_input('Enter the longitude (-74.03 ~ -73.75) for dropoff location:', min_value=-74.03, max_value=-73.75)

# Define Distance Haversine
def haversine(lat1, long1, lat2, long2):
    lat1_rad, long1_rad, lat2_rad, long2_rad = np.radians([lat1, long1, lat2, long2])
    average_earth_rad = 6371
    lat_diff = lat2_rad - lat1_rad
    long_diff = long2_rad - long1_rad
    haversine = 2 * average_earth_rad * np.arcsin(np.sqrt(
                                                        np.sin(lat_diff * 0.5) ** 2
                                                        + np.cos(lat1_rad) * np.cos(lat2_rad)
                                                        * np.sin(long_diff * 0.5) ** 2))
    return haversine

# Input Latitude and longitude to Find Distance
distance_haversine = haversine(pickup_latitude,
                               pickup_longitude,
                               dropoff_latitude,
                               dropoff_longitude)


# Store and forward
st.subheader('Store and Forward')

st.markdown("""
The "store and forward" flag indicates whether the trip record was held in the vehicle's memory before being sent to the vendor's server.

- **Y (Yes)**: Trip data was stored in the vehicle's memory and sent to the server later.
- **N (No)**: Trip data was transmitted to the server in real-time.

This flag helps identify trips where the vehicle did not have a connection to the server during the trip.
""")

store_and_fwd_flag = st.radio('Does it come with store and forward?', ['Yes', 'No'])
if store_and_fwd_flag == 'Yes':
    store_and_fwd_flag = 1
else:
    store_and_fwd_flag = 0



@st.cache_data
def load_model():
    return pickle.load(open('model/NYC_TripDuration_tuned_model.pkl', 'rb'))

model = load_model()

your_trip = pd.DataFrame({
    'vendor_id':[vendor],
    'hour_pickup':[hour_pickup_datetime],
    'hour_dropoff':[hour_dropoff_datetime],
    'day_pickup':[day_pickup_datetime],
    'day_dropoff':[day_dropoff_datetime],
    'week_pickup':[week_pickup_datetime],
    'week_dropoff':[week_dropoff_datetime],
    'month_pickup':[month_pickup_datetime],
    'month_dropoff':[month_dropoff_datetime],
    'passenger_count':[passenger_count],
    'pickup_latitude':[pickup_latitude],
    'pickup_longitude':[pickup_longitude],
    'dropoff_latitude':[dropoff_latitude],
    'dropoff_longitude':[dropoff_longitude],
    'distance_haversine':[distance_haversine],
    'store_and_fwd_flag':[store_and_fwd_flag]
})

if st.button('Calculate the Duration!'):
    your_trip_duration = model.predict(your_trip)
    your_trip_duration = your_trip_duration[0]
    your_trip_duration = np.round(your_trip_duration)
    st.write(f"### Your trip duration is predicted {your_trip_duration}")


st.markdown("""DISCLAIMER: Please note that the predicted trip durations
            are based on historical data and statistical patterns.
            While we strive to provide accurate estimates,
            unforeseen circumstances such as heavy traffic,
            road closures, or weather conditions may affect
            the actual duration of your trip.""")