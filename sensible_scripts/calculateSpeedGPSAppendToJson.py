# Use this file as 2 of 3

# this file is to calculate momentary speed from my data from JSON array and append that value into each JSON in json array.
# Wolrd forgive me for this spaghetti, it it one-use only with chances of it being useful in the future - but then will be the time to write it properly. Also I will rewrite this probably.


import json
from math import radians, sin, cos, sqrt, atan2

#source: bing. Checked that with wikipedia.
def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371000 # Radius of the Earth in meters
    #c*r is distance in meters, and it also is speed in meters/second because the values are measured one second apart

    return round((c * r * 3.6),1)


path_to_read = r"Y:\our\path"
filename_to_read = "\stuff.json"

# Load the CLEANED UP data from the file
with open(path_to_read+filename_to_read, 'r') as f:
    clean_json_array = json.load(f)

n_entries = len(clean_json_array)





path_to_save = r"Y:\our\path"
filename_to_save = "\stuff_goodTimestamp.json" 

with open(path_to_save+filename_to_save, 'w') as f:
  json.dump(clean_json_array, f, indent=2)