# this file is to calculate momentary speed from my data from JSON and append that value into each JSON in json array.

import json
from math import radians, sin, cos, sqrt, atan2

#source: my dear, beloved internet. However I should double-check that
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

    return (c * r)*3.6



# Load the CLEANED UP data from the file
with open('C:\\Users\\Admin\\Desktop\\zepp life\\kuby\\kubaORG_cleanUp_test.json', 'r') as f:
    clean_json_array = json.load(f)

n_entries = len(clean_json_array)

for i, clean_entry in enumerate(clean_json_array[1:], start=1): #iterate from 2nd because we append speed to second element from pair it was calculated from
    print(n_entries-2,"/",i)

    latitude_now = clean_entry['lat52']
    longitude_now = clean_entry['lon53']
    
    latitude_prev = (clean_json_array[i - 1])['lat52']
    longitude_prev = (clean_json_array[i - 1])['lon53']

    speed = haversine(latitude_prev, longitude_prev, latitude_now, longitude_now)

    clean_entry['speed'] = speed


with open('C:\\Users\\Admin\\Desktop\\zepp life\\kuby\\kubaORG_cleanUp_test_withSpeed.json', 'w') as f:
    json.dump(clean_json_array, f, indent=2)
