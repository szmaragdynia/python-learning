# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now

# perhaps should have used virtual environment
# import pandas as pd
import gpxpy
import gpxpy.gpx
import json
import csv
import datetime

path_to_file_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"
input_filename = "kubaORG.gpx"

# -------------------------------------------- reading and parsing gpx for further use --------------------------------------------
gpx_file = open(path_to_file_dir + input_filename, 'r')
gpx = gpxpy.parse(gpx_file)

measures = []


for track in gpx.tracks[:1]: # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
    for segment in track.segments[:1]: # same as above
        for point in segment.points[:30]:                           # --------- BEWARE OF THE RESTRICTION
            measures.append({"original_data": True, 
                            "latitude_deg": point.latitude,
                             "longitude_deg": point.longitude,
                             "elevation_m": point.elevation,
                             "datetimeISO8601": point.time.isoformat(),
                             "time": point.time.time().isoformat()}) # "time" is handy for 'debugging' in After Effects



# saving at this stage, so that I could take a peek at what is going on
csv_headers = measures[0].keys()
output_filename_step1_csv = input_filename[:input_filename.index(".")] + "_1dataStraightFromGpx.csv" # add postfix and change extension
with open(path_to_file_dir + output_filename_step1_csv, 'w', newline='') as output_file: #  '' is imporant, beacuse else I get empty rows in csv every entry
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures)


# -------------------------------------------- removing duplicates --------------------------------------------
#this is very, very, very ugly. I just wanted to finish merging, tidying will be the next step (should that step occur)
indexes_to_delete = []
for i in range(len(measures)-1):
    print(i,"/",len(measures)-1)
    if (measures[i]["time"] == measures[i+1]["time"]): # if this seems to be duplicate of the next one
        if (None in measures[i].values() and not None in measures[i+1].values()) or (not None in measures[i].values() and None in measures[i+1].values()): #only one of two dicts can have some None values.
            if not any([
                measures[i]["original_data"] == None,
                measures[i]["latitude_deg"] == None,
                measures[i]["longitude_deg"] == None,
                measures[i]["datetimeISO8601"] == None,
                measures[i]["time"] == None,
                measures[i+1]["original_data"] == None,
                measures[i+1]["latitude_deg"] == None,
                measures[i+1]["longitude_deg"] == None,
                measures[i+1]["datetimeISO8601"] == None,
                measures[i+1]["time"] == None,
            ]): #the only key that has None value, is Elevation (it's missing from the list, and we know that only one of two dicts have None as value)
                if measures[i]["elevation_m"] == None:
                    indexes_to_delete.append(i)
                    print ("Adding index i to deletion, i::",i)
                elif measures[i+1]["elevation_m"] == None:
                    indexes_to_delete.append(i+1)
                    print ("Adding index i+1 to deletion, i+1::",i+1)
                else:
                    print("Bug, program will now exit. 1.")
                    exit()
            else:
                print("1This case is not handled. Program will now exit (so you can upgrade the code or manually modify the files).")
                exit()
        else:
            print("2This case is not handled. Program will now exit (so you can upgrade the code or manually modify the files).")
            exit()

indexes_to_delete.sort(reverse=True)
print("deleting i=",end='')
for index in indexes_to_delete:    
    print(index,", ",end ='', sep='')
    del measures[index]
    
    

output_filename_step2_csv = input_filename[:input_filename.index(".")] + "_2noDuplicates.csv" # add postfix and change extension
with open(path_to_file_dir + output_filename_step2_csv, 'w', newline='') as output_file: #  '' is imporant, beacuse else I get empty rows in csv every entry
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures)
    
        




# ------------------------------------------------------------------------
#with open(path_to_file_dir + output_filename, 'w') as f:
#  json.dump(measures, f, indent=2)
print()
print("finished")