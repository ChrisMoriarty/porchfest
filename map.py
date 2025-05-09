import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_js_eval import get_geolocation

# Load the data
df = pd.read_csv('bands_with_lat_long.csv')

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
    user_location_df = pd.DataFrame({
        'latitude': ["42.3555"],
        'longitude': ["71.0565"],
        'name': ['Your Location']
    })

# Create a map using pydeck
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=42.3876,  # Latitude for Somerville, MA
        longitude=-71.0995,  # Longitude for Somerville, MA
        zoom=13,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',  # Red for bands
            get_radius=30,
            pickable=True,  # Enable picking for tooltips
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=user_location_df,
            get_position='[longitude, latitude]',
            get_color='[0, 0, 255, 160]',  # Blue for user location
            get_radius=100,
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