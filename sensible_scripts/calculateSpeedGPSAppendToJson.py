# Use this file as 2 of 3

# this file is to calculate momentary speed from my data from JSON array and append that value into each JSON in json array.
# God forgive this spaghetti, it it one-use only with chances of it being useful in the future - but then will be the time to write it properly


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



# Load the CLEANED UP data from the file
with open(r'E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\kubaORG_cleanUp.json', 'r') as f:
    clean_json_array = json.load(f)

n_entries = len(clean_json_array)



(clean_json_array[0])['speed km/h'] = 0 #dummy
(clean_json_array[0])['speed status'] = "dummy value"

i=1
while i < n_entries: #iterate from 2nd because we append speed to second element from pair it was calculated from, and it convenient in code to use such indexing
    print(n_entries-1,"/",i)

    # we need to take care of fake (copied) values, because they make speed constant and just before real value - very large. 
    # we need to take the last real speed value before fake values, and then the first real speed value after fake values, and intepolate (poor man's:linearly) in the fake-value objects, so we have gradual change of speed
    # assumptions: 1. before any fake-entries, there is at least one real one with appriopriate geolocation data 
    #              2. after fake-entries, there are at least TWO real ones with appriopriate geolocation data (two because we want to calculate real speed to interpolate from)


    # if second entry is false then we would need dummy speed val in first element, but this might not make sense if began recording while on the move, because then average speed would make more sense.

    if (clean_json_array[i])['real values'] == 'TRUE':
        latitude_now = (clean_json_array[i])['lat52']
        longitude_now = (clean_json_array[i])['lon53']
        
        latitude_prev = (clean_json_array[i-1])['lat52']
        longitude_prev = (clean_json_array[i-1])['lon53']
        
        speed = haversine(latitude_prev, longitude_prev, latitude_now, longitude_now)
        (clean_json_array[i])['speed km/h'] = speed
        (clean_json_array[i])['speed status'] = "distance from prev to now"
    elif (clean_json_array[i])['real values'] == 'FALSE':
        #search for first not-fake and determine number of fakes
        j = i
        while (clean_json_array[j]['real values'] == 'FALSE'):
            j += 1 
        # j is now first not-fake
        # if second element after FALSE is ALSO TRUE (because first is, since we exited while) [t f f f f T T]
        if (j+1<n_entries-1 and clean_json_array[j+1]['real values'] == 'TRUE'): 
            # calculate the speed for the second realvalue basing on first and second realvaluem and insert it into proper place
            latitude_now = (clean_json_array[j+1])['lat52']
            longitude_now = (clean_json_array[j+1])['lon53']
            
            latitude_prev = (clean_json_array[j])['lat52']
            longitude_prev = (clean_json_array[j])['lon53']

            speed = haversine(latitude_prev, longitude_prev, latitude_now, longitude_now)
            (clean_json_array[j+1])['speed km/h'] = speed
            (clean_json_array[j+1])['speed status'] = "distance from prev to now"

            # now lets interpolate speed for all fake values and first true value
            number_of_fakes = j-i # because j points at first after last fake, and i points at first fake
            magic_number = 2 # well...
            speed_change_every_second = ((clean_json_array[j+1])['speed km/h'] - (clean_json_array[i-1])['speed km/h'])/(number_of_fakes+magic_number)
            # now insert interpolated speeds
            k=0
            # while the main iterator (i) is not yet the same as  look-ahead-iterator (j), which (j) points to first not fake, which needs interpolated speed as well
            while i <= j:
                (clean_json_array[i])['speed km/h'] = (clean_json_array[i-1])['speed km/h'] + speed_change_every_second
                (clean_json_array[i])['speed status'] = "interpolated "
                i += 1
            i -= 1 #compensation - we and at unchecked element, and later we increment again.
        # if second element after FALSE is FALSE, despite first being TRUE [t f f f f T f]
        # then we dont have enought data points to calculate speed for "T", and simpliest we can do is to use average speed throughout the entire false-scope
        # in the future I could interpolate speeds more properly - that is maybe loot at previous true speed values and use them to calculate the speed that must had been kept over the distance that is 'fake'
        elif (j+1<n_entries-1 and clean_json_array[j+1]['real values'] == 'FALSE'): 
            # j is still first not-fake
            # i is first fake
            # calculate the AVERAGE speed for each missing element, basing on pre-fake realvalue and on post-fake realvalue and insert it into proper place
            latitude_now = (clean_json_array[j])['lat52']
            longitude_now = (clean_json_array[j])['lon53']
            
            latitude_prev = (clean_json_array[i-1])['lat52']
            longitude_prev = (clean_json_array[i-1])['lon53']

            speed = haversine(latitude_prev, longitude_prev, latitude_now, longitude_now)
            while i <= j:
                (clean_json_array[i])['speed km/h'] = speed
                (clean_json_array[i])['speed status'] = "average over time"
                i += 1
            i -= 1 #compensation - we and at unchecked element, and later we increment again.
    i=i+1

with open(r'E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\kubaORG_cleanUp_speed.json', 'w') as f:
    json.dump(clean_json_array, f, indent=2)

