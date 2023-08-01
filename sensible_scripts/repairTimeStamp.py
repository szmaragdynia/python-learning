# This script reads json array and repairs timestamp which is coded in iso 8601 time format. The file repaired must be broken by previous files, that is, it is broken such that the timestamps show incorrect time (copied values).
# This script also changes hours in the timestamp 
# Use this file 3rd.

import json
import datetime



# BEWARE FOR THE key name for the time, depending on the source of the data (strava/zepp life) and how I named the column in excel/csv
#time_key_name = "ns1:time55" #zepp life
time_key_name = "time" #strava

hours_to_add = 3 # 3 because footage is one hour ahead of localtime, which (localtime) is 2 hours ahead of the time from gpx

path_to_read = r"Y:\our\path"
path_to_save = r"Y:\our\path"
filename_to_read = "\stuff.json" 
filename_to_save = "\stuff_goodTimestamp.json" 

with open(path_to_read+filename_to_read, 'r') as f:
    clean_with_speed_json_array = json.load(f)

for i,entry in enumerate(clean_with_speed_json_array[:]):
  if entry['real values'] == "TRUE": # not duplicates
    # convert this json's time in iso 8601 into datetime python module
    dt = datetime.datetime.strptime(entry[time_key_name], "%Y-%m-%dT%H:%M:%S%z")
    dt = dt + datetime.timedelta(hours=3) # compensate for erroneous time written
    #convert to iso again, for the second condition (I personally wouldn't need that in ISO)
    dt_ISO = dt.isoformat()
    #print("datetime new: ",dt_ISO," original: ",entry[time_key_name])
    entry[time_key_name] = dt_ISO
  elif entry['real values'] == "FALSE": #
    # convert PREVIOUS json's time in iso 8601 into datetime python module
    dt = datetime.datetime.strptime((clean_with_speed_json_array[i-1])[time_key_name], "%Y-%m-%dT%H:%M:%S%z")
      #in case of an error I will just manually do the magic in the file, it's one-use (for now)
    # previous should already have changed hours appropriately, but we are FAKE, thus we need to compensate for missing second
    dt = dt + datetime.timedelta(seconds=1) # compensate for erroneous time written
    #convert to iso again, for the second condition (I personally wouldn't need that in ISO)
    dt_ISO = dt.isoformat()
    #print("datetime new: ",dt_ISO," original: ",entry[time_key_name]," previous: ", (clean_with_speed_json_array[i-1])[time_key_name])
    entry[time_key_name] = dt_ISO
    
for entry in clean_with_speed_json_array[:]:
  dt = datetime.datetime.strptime(entry[time_key_name], "%Y-%m-%dT%H:%M:%S%z")
  dt_no_ms = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) # clean up missing miliseconds
  dt_no_ms_ISO = dt_no_ms.isoformat()
  entry[time_key_name] = dt_no_ms_ISO
  # print("dt: ",dt," dt_no_ms: ",dt_no_ms)
  
with open(path_to_save+filename_to_save, 'w') as f:
  json.dump(clean_with_speed_json_array, f, indent=2)
