import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_js_eval import get_geolocation

# Load the data
df = pd.read_csv('bands_with_lat_long.csv')

# Define a color mapping based on the Time column
def map_time_to_color(time):
    if time.startswith("12:"):
        return [51, 212, 255]  # Blue
    elif time.startswith("1:"):
        return [51, 212, 255]  # Blue
    elif time.startswith("2:"):
        return [103, 255, 51]  # Green
    elif time.startswith("3:"):
        return [255, 255, 0]  # Green
    else:
        return [255, 249, 51 ]  # Yellow

# Add a color column to the dataframe
df['color'] = df['Time'].apply(map_time_to_color)


# Streamlit app title
st.title("Somerville Porchfest Map :musical_note: :beers:")

# Filter data for valid latitude and longitude
df = df.dropna(subset=['latitude', 'longitude'])

# Get user's location
loc = get_geolocation()

if loc is not None:
    user_lat = loc["coords"]["latitude"]
    user_lon = loc["coords"]["longitude"]

    # Add user's location to the map if available
    user_location_df = pd.DataFrame({
        'latitude': [user_lat],
        'longitude': [user_lon],
        'name': ['Your Location']
    })
else:
    user_lat = None
    user_lon = None
    user_location_df = pd.DataFrame({
        'latitude': ["42.3555"],
        'longitude': ["71.0565"],
        'name': ['Your Location']
    })

if user_lat is None:
    start_lat = 42.3876     # Latitude for Somerville, MA
    start_lon = -71.0995    # Longitude for Somerville, MA
else:
    start_lat = user_lat
    start_lon = user_lon

# Create a map using pydeck
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=start_lat,
        longitude=start_lon,
        zoom=13,
        pitch=25,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[longitude, latitude]',
            get_color='color',
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=5,
            radius_max_pixels=10,
            line_width_min_pixels=1,
            get_line_color=[0, 0, 0],
            pickable=True,  # Enable picking for tooltips
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=user_location_df,
            get_position='[longitude, latitude]',
            opacity=0.8,
            get_color='[0, 0, 255, 160]',  # Blue for user location
            get_line_color=[0, 0, 0],
            radius_scale=6,
            radius_min_pixels=10,
            radius_max_pixels=15,
            line_width_min_pixels=1,
        ),
    ],
    tooltip={
        "html": "<b>Band Name:</b> {Band Name}<br>"
                "<b>Time:</b> {Time}<br>"
                "<b>Genre:</b> {Genre}<br>"
                "<b>Address:</b> {Address}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
))