# this file is for cleaning up data from gps, in order for it to work somehow in after effects

import json

# Load the data from the file
with open('C:\\Users\\Admin\\Desktop\\zepp life\\kuby\\test.json', 'r') as f:
    json_array = json.load(f)

for item in json_array:
    if item['normalized time in seconds'] == 0:
        print('found him, his time in seconds is.' )
# Copy the second object and insert it after the second object
# data.insert(2, data[1].copy())

# Save the modified data to the file
with open('C:\\Users\\Admin\\Desktop\\zepp life\\kuby\\test_saved.json', 'w') as f:
    json.dump(json_array, f, indent=2)
