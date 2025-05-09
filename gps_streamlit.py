import streamlit as st
from streamlit_js_eval import get_geolocation

# if st.checkbox("Check my location"):
loc = get_geolocation()
lat = loc["coords"]["latitude"]
lon = loc["coords"]["longitude"]
st.write(f"Your coordinates are {lat}, {lon}")


