import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="NYC Taxi Trip Duration",
    page_icon="🚖",
)

st.write("# Explore the City That Never Sleeps")

st.sidebar.success("You could select other sidebar.")

image = Image.open('vidar-nordli-mathisen-unsplash.jpg')

st.image(image, caption='New York Taxi at Times Square. Photo by Vidar Nordli-Mathisen (Unsplash.com).')

st.markdown(
    """Plan your NYC taxi trips with ease using our Taxi Trip Duration Estimator.
    Whether you're a local New Yorker or a visitor, our predictive model
    provides accurate estimates of trip durations, helping you make informed
    decisions about your travel plans.
    """
    )

st.subheader('Key Features:')
st.markdown(
    """
    1. Estimate Trip Duration: Enter your trip details, such as pickup and dropoff locations, and our model will provide an estimated duration for your taxi journey.
    2. Interactive Chart: Visualize pickup and dropoff locations on an interactive map.
    """)

st.subheader('About the Data that I used:')
st.markdown(
    """
    1. id - a unique identifier for each trip
    2. vendor_id - a code indicating the provider associated with the trip record
    3. pickup_datetime - date and time when the meter was engaged
    4. dropoff_datetime - date and time when the meter was disengaged
    5. passenger_count - the number of passengers in the vehicle (driver entered value)
    6. pickup_longitude - the longitude where the meter was engaged
    7. pickup_latitude - the latitude where the meter was engaged
    8. dropoff_longitude - the longitude where the meter was disengaged
    9. dropoff_latitude - the latitude where the meter was disengaged
    10. store_and_fwd_flag - This flag indicates whether the trip record was held in vehicle memory before sending to the vendor because the vehicle did not have a connection to the server - Y=store and forward; N=not a store and forward trip
    11. trip_duration - duration of the trip in seconds
    """)


st.subheader('Documentation:')
st.markdown(
    """
    - Data source: kaggle.com/competitions/nyc-taxi-trip-duration
    - Find the github: (https://github.com/dataaga/NYCStreamlit)
    """)