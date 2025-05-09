import pandas as pd
from opencage.geocoder import OpenCageGeocode
import time

# Initialize the OpenCage client with your API key
key = 'e28527909973470cad49964e338bc3dc'
geocoder = OpenCageGeocode(key)

def get_lat_long(address):
    try:
        result = geocoder.geocode(address)
        if result and len(result):
            location = result[0]['geometry']
            return location['lat'], location['lng']
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

# Read the data from bands.csv
df = pd.read_csv('bands.csv')

# Compute latitude and longitude for each address with rate limiting
lat_long_results = []
for addr in df['Address']:
    lat_long = get_lat_long(addr)
    lat_long_results.append(lat_long)
    print(lat_long)
    # time.sleep(1)  # Add a delay to respect rate limits

df[['latitude', 'longitude']] = pd.DataFrame(lat_long_results, columns=['latitude', 'longitude'])

# Save the updated data to a new CSV file
df.to_csv('bands_with_lat_long.csv', index=False)