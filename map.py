import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_js_eval import get_geolocation

# Load the data
df = pd.read_csv('bands_with_lat_long.csv')

# Streamlit app title
st.title("Bands Map")

# Filter data for valid latitude and longitude
df = df.dropna(subset=['latitude', 'longitude'])

# Get user's location
loc = get_geolocation()
user_lat = loc["coords"]["latitude"]
user_lon = loc["coords"]["longitude"]

# Add user's location to the map if available
if user_lat is not None and user_lon is not None:
    user_location_df = pd.DataFrame({
        'latitude': [user_lat],
        'longitude': [user_lon],
        'name': ['Your Location']
    })
else:
    user_location_df = pd.DataFrame(columns=['latitude', 'longitude', 'name'])

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
            get_radius=100,
            pickable=True,  # Enable picking for tooltips
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=user_location_df,
            get_position='[longitude, latitude]',
            get_color='[0, 0, 255, 160]',  # Blue for user location
            get_radius=150,
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

# Display the data table
st.write("Band Details")
st.dataframe(df)