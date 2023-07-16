import streamlit as st
import pandas as pd
import numpy as np
import time

import folium
import branca.colormap as cm
from branca.colormap import LinearColormap
from streamlit_folium import folium_static, st_folium
import plotly.express as px
import zipfile


import matplotlib.pylab as plt
from datetime import datetime
import os
from folium.plugins import MarkerCluster


st.title('NYC Taxi Trip in New York')

st.markdown(
    """
    Mostly NYC taxi pickup/dropoff is around
    the lower Manhattan and the Central Park,
    but the dropoff has more wider since they're
    need to deliver the passenger comeback home
    """
)


# Path to the ZIP file
zip_file_path = 'dataset/trainn.zip'

# Name of the CSV file within the ZIP
csv_file_name = 'train_.csv'

# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    # Check if the CSV file exists in the ZIP
    if csv_file_name in zip_file.namelist():
        # Read the CSV file directly from the ZIP
        with zip_file.open(csv_file_name) as csv_file_in_zip:
            # Use pandas to read the CSV data
            df = pd.read_csv(csv_file_in_zip)
            df = df.sample(frac =.1)
    else:
        print(f"The file '{csv_file_name}' does not exist in the ZIP file.")

#file_path = ('yourpath/test.csv')
#df = pd.read_csv(file_path)

@st.cache_data
def show_data():
    st.write(df)

@st.cache_data
def draw_map_pickup():
    # Limit the DataFrame to 1000 rows
    #df_limited = df.head(1000)
    df['trip_duration'] = np.log(df['trip_duration'].values + 1)

    # Then, we define how we'd like to set the color
    colormap_pickup = LinearColormap(colors=['green', 'darkgreen'], vmin=df['trip_duration'].min(), vmax=df['trip_duration'].max())
    
    m_pickup = folium.Map(location=[40.73569, -73.87133], zoom_start=11, tiles='stamentoner')

    # For each 'row' in the limited dataframe, add the pickup locations to the map
    for lat, lon, ap in zip(df['pickup_latitude'], df['pickup_longitude'], df['trip_duration']):
        folium.Circle(
            location=[lat, lon],
            radius=100,
            fill=True,
            color=colormap_pickup(ap),
            fill_opacity=0.25,
            weight=2
        ).add_to(m_pickup)

    st.write("## Pickup Locations")
    folium_static(m_pickup)

# Call the function to draw the map
draw_map_pickup()


@st.cache_data
def show_data():
    st.write(df)

@st.cache_data
def draw_map_dropoff():
    # Limit the DataFrame to 1000 rows
    #df_limited = df.head(1000)

    # Then, we define how we'd like to set the color
    colormap_dropoff = LinearColormap(colors=['blue', 'darkblue'], vmin=df['trip_duration'].min(), vmax=df['trip_duration'].max())

    # Create a new map for dropoff locations
    m_dropoff = folium.Map(location=[40.73569, -73.87133], zoom_start=11, tiles='stamentoner')

    # For each 'row' in the limited dataframe, add the dropoff locations to the map
    for lat, lon, ap in zip(df['dropoff_latitude'], df['dropoff_longitude'], df['trip_duration']):
        folium.Circle(
            location=[lat, lon],
            radius=100,
            fill=True,
            color=colormap_dropoff(ap),
            fill_opacity=0.25,
            weight=2
        ).add_to(m_dropoff)

    st.write("## Dropoff Locations")
    folium_static(m_dropoff)

# Call the function to draw the map
draw_map_dropoff()





st.subheader('Scatterplot of Trip Duration and Distance')

@st.cache_data
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

# Calculate the interquartile range (IQR)
Q1 = df['trip_duration'].quantile(0.25)
Q3 = df['trip_duration'].quantile(0.75)
IQR = Q3 - Q1

# Define the upper and lower bounds for outlier detection
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out the outliers of trip_duration
filtered_df = df[(df['trip_duration'] >= lower_bound) & (df['trip_duration'] <= upper_bound)]

# Filter out the outliers of longitude and latitude
filtered_df = filtered_df[filtered_df['pickup_longitude'] <= -73.75]
filtered_df = filtered_df[filtered_df['pickup_longitude'] >= -74.03]
filtered_df = filtered_df[filtered_df['pickup_latitude'] <= 40.85]
filtered_df = filtered_df[filtered_df['pickup_latitude'] >= 40.63]
filtered_df = filtered_df[filtered_df['dropoff_longitude'] <= -73.75]
filtered_df = filtered_df[filtered_df['dropoff_longitude'] >= -74.03]
filtered_df = filtered_df[filtered_df['dropoff_latitude'] <= 40.85]
filtered_df = filtered_df[filtered_df['dropoff_latitude'] >= 40.63]

filtered_df['distance_haversine'] = haversine(filtered_df['pickup_latitude'].values,
                                    filtered_df['pickup_longitude'].values,
                                    filtered_df['dropoff_latitude'].values,
                                    filtered_df['dropoff_longitude'].values)

fig = px.scatter(filtered_df, x = 'distance_haversine', y = 'trip_duration', color = 'passenger_count')
st.plotly_chart(fig, theme = 'streamlit')



st.subheader('Trip Duration Boxplot for Distance in New York')

@st.cache_data
def visualize_boxplot():
    # Calculate the interquartile range (IQR)
    Q1 = df['trip_duration'].quantile(0.25)
    Q3 = df['trip_duration'].quantile(0.75)
    IQR = Q3 - Q1

    # Define the upper and lower bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers
    filtered_df_bp = df[(df['trip_duration'] >= lower_bound) & (df['trip_duration'] <= upper_bound)]

    # Filter passenger count equal or above 1
    filtered_df_bp = filtered_df_bp[filtered_df_bp['passenger_count'] >= 1]

    fig = px.box(filtered_df_bp, x = 'passenger_count', y = 'trip_duration')
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

visualize_boxplot()




# Convert to Date
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

# Define the plot for each time type
@st.cache_data
def create_plot(df, datetime_col, group_col, time_attr):
    title_name = "Pickup" if datetime_col == 'pickup_datetime' else "Dropoff"
    if time_attr == 'hour':
        df[datetime_col+'_hour'] = df[datetime_col].dt.hour
        summary_time = pd.DataFrame(df.groupby([group_col, datetime_col+'_hour'])['trip_duration'].mean())
        summary_time.reset_index(inplace = True)
        fig = px.line(summary_time, x=datetime_col+'_hour', y='trip_duration', color=group_col)
        fig.update_layout(title=f'Hourly Trip Duration for {title_name}')
    elif time_attr == 'dayofweek':
        df['day_of_week_'+datetime_col] = df[datetime_col].dt.dayofweek
        summary_day = pd.DataFrame(df.groupby([group_col, 'day_of_week_'+datetime_col])['trip_duration'].mean())
        summary_day.reset_index(inplace = True)
        fig = px.line(summary_day, x='day_of_week_'+datetime_col, y='trip_duration', color=group_col)
        fig.update_layout(title=f'Daily Trip Duration for {title_name}')
    elif time_attr == 'month':
        df[datetime_col+'_month'] = df[datetime_col].dt.month
        summary_month = pd.DataFrame(df.groupby([group_col, datetime_col+'_month'])['trip_duration'].mean())
        summary_month.reset_index(inplace = True)
        fig = px.line(summary_month, x=datetime_col+'_month', y='trip_duration', color=group_col)
        fig.update_layout(title=f'Monthly Trip Duration for {title_name}')
    else:
        raise ValueError(f"Unsupported time attribute: {time_attr}")
    st.plotly_chart(fig)



## Define the tabs
hour_tab, day_tab, month_tab = st.tabs(["Hour", "Day", "Month"])

# Code for the Hour tab
with hour_tab:
    st.header("Analysis based on Hour")
    create_plot(df, 'pickup_datetime', 'vendor_id', 'hour')
    create_plot(df, 'dropoff_datetime', 'vendor_id', 'hour')

# Code for the Day tab
with day_tab:
    st.header("Analysis based on Day of the Week")
    create_plot(df, 'pickup_datetime', 'vendor_id', 'dayofweek')
    create_plot(df, 'dropoff_datetime', 'vendor_id', 'dayofweek')

# Code for the Month tab
with month_tab:
    st.header("Analysis based on Month")
    create_plot(df, 'pickup_datetime', 'vendor_id', 'month')
    create_plot(df, 'dropoff_datetime', 'vendor_id', 'month')
