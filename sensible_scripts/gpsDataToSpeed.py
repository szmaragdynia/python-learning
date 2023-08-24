# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now
# Todo: make it into separate modules...or am I biased?
# Todo: swap tabs with constant widths wherever appropriate

# perhaps should have used virtual environment
# import pandas as pd
import gpxpy
import gpxpy.gpx
import json
import csv
import time
from datetime import datetime, timedelta

time_start = time.time()

path_to_file_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"
gpx_filename = "kubaORG.gpx"

log_filename = "log.txt"
log_file = open(path_to_file_dir + log_filename, 'w')

def log(*args_list, **keyword_args_dict):                          # names for future-me
    print(*args_list, **keyword_args_dict)
    print(*args_list, file=log_file, **keyword_args_dict)

# -------------------------------------------- reading and parsing gpx for further use --------------------------------------------
time_start_gpx = time.time()
gpx_file = open(path_to_file_dir + gpx_filename, 'r')
gpx = gpxpy.parse(gpx_file)

measures = []
for track in gpx.tracks[:1]:                                        # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
    for segment in track.segments[:1]: # same as above
        for point in segment.points:                           # --------- BEWARE OF THE >TEMPORARY< RESTRICTION FOR TESTING-CODE PURPOSES
            measures.append({"original_data": True, 
                            "latitude_deg": point.latitude,
                             "longitude_deg": point.longitude,
                             "elevation_m": point.elevation,
                             "datetimeISO8601": point.time.isoformat(),
                             "time": point.time.time().isoformat(),   # "time" is handy for 'debugging' in After Effects
                             "date": point.time.date().isoformat()}) # "time" is handy for 'debugging' in After Effects



# saving at this stage, so that I can take a peek at what is going on
csv_headers = measures[0].keys()
output_filename_step1_csv = gpx_filename[:gpx_filename.index(".")] + "__1dataStraightFromGpx.csv" # add postfix and change extension
with open(path_to_file_dir + output_filename_step1_csv, 'w', newline='') as output_file:             #  '' is imporant, beacuse else I get empty rows in csv every entry
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures)

time_end_gpx = time.time()


# -------------------------------------------- removing duplicates --------------------------------------------
#this is very, very, very ugly. I just wanted to finish merging, tidying will be the next step (should that step occur)
time_start_collecting_dupes = time.time()

indexes_to_delete = []

for i in range(len(measures)-1):
    log("\n", len(measures)-1, "/", i,  end='\t')
    if (measures[i]["time"] == measures[i+1]["time"]):                          # if this measure seems to be duplicate of the next one
        if (None in measures[i].values() and not None in measures[i+1].values()) or (not None in measures[i].values() and None in measures[i+1].values()): 
                                                                                # only one of two dicts can have some None values.
            if not any([
                measures[i]["original_data"] == None,
                measures[i]["latitude_deg"] == None,
                measures[i]["longitude_deg"] == None,
                measures[i]["datetimeISO8601"] == None,
                measures[i]["time"] == None,
                measures[i]["date"] == None,
                measures[i+1]["original_data"] == None,
                measures[i+1]["latitude_deg"] == None,
                measures[i+1]["longitude_deg"] == None,
                measures[i+1]["datetimeISO8601"] == None,
                measures[i+1]["time"] == None,
                measures[i+1]["date"] == None,
            ]):                                                                 # the only key that has None value is Elevation (it's missing from the logic above, and we know that only one of two dicts have None as value)
                if measures[i]["elevation_m"] == None:                          # if the current measure has None in Elevation
                    indexes_to_delete.append(i)
                    log ("Adding index i to deletion list, i:",i, end='')
                elif measures[i+1]["elevation_m"] == None:                      # if the current measure has None in Elevation
                    indexes_to_delete.append(i+1)
                    log ("Adding index i+1 to deletion list, i+1:",i+1,end='')
                else:
                    log("\n\n\nBug, program will now exit. 1.")
                    exit()
            else:
                log("\n\n\n1This case is not handled. Program will now exit (so you can upgrade the code or manually modify the files).")
                exit()
        else:
            log("\n\n\n2This case is not handled. Program will now exit (so you can upgrade the code or manually modify the files).")
            exit()
time_end_collecting_dupes = time.time()

log("\n\nList of indexes to delete:\n",indexes_to_delete, sep='')
log("Elevations \"of indexes\" TO DELETE (should all BE EMPTY):")
for index in indexes_to_delete:
    log(index,":",measures[index]["elevation_m"])

time_start_o2 = time.time()
log("\nEntering [almost] o^2 space. Be patient.")                                                 # I underestimated (even not so modern) CPU computational power.
log("\nElevations \"of indexes\" NOT TO DELETE (should all HAVE VALUE):")
for i,measure in enumerate(measures):
    matching_value = next((index for index in indexes_to_delete if index == i), None)           # if this index IS EQUAL to any of the indexes to delete. 
                                                                                                # USE WITH CAUTION, TIME HEAVY! (o^2 almost)
                                                                                                    # I could log these previously, but this serves as double-check.
                                                                                                # list comprehension in next - generator expression is used (read more some time)
    if matching_value == None:                                                                  # if no index is equal to current index = current index is not on a list to delete
        log(index,":",measure["elevation_m"], end='\t')
        log("in o^2, script alive, i= ", i)
    else:
        log("\t\t",end='')
        log("in o^2, script alive, i= ", i)
time_end_o2 = time.time()
    

indexes_to_delete.sort(reverse=True)
log("deleting i= ",end='')
for index in indexes_to_delete:    
    log(index,", ",end ='', sep='')
    del measures[index]
    
    

output_filename_step2_csv = gpx_filename[:gpx_filename.index(".")] + "__2noDuplicates.csv" # add postfix and change extension
with open(path_to_file_dir + output_filename_step2_csv, 'w', newline='') as output_file: #  '' is imporant, beacuse else I get empty rows in csv every entry
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures)
            
time_end_everything_dupes = time.time()

# -------------------------------------------- populating missing data --------------------------------------------
# After effects expects data every second. I need data every second, even if data is empty or fake. We will copy previous values





# ------------------------------------------------------------------------
#with open(path_to_file_dir + output_filename, 'w') as f:
#  json.dump(measures, f, indent=2)
# divide for AE!

time_end = time.time()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
elapsed_time_gpx = timedelta(seconds=time_end_gpx - time_start_gpx)
elapsed_time_everything_dupes = timedelta(seconds=time_end_everything_dupes - time_start_collecting_dupes)
elapsed_time_collecting_dupes = timedelta(seconds=time_end_collecting_dupes - time_start_collecting_dupes)
elapsed_time_o2 = timedelta(seconds=time_end_o2 - time_start_o2)
log("\n\n\nFINISHED.")
# log("Elapsed time [s]: {:.2}s".format(elapsed_time_all), " and in it:", sep='')
# log("\tElapsed time parsing gpx: {:.2f}".format(elapsed_time_gpx))
# log("\tElapsed time processing duplicates: {:.2f}".format(elapsed_time_everything_dupes), " and in it:",sep='')
# log("\t\tElapsed time collecting duplicates: {:.2f}".format(elapsed_time_collecting_dupes))
# log("\t\tElapsed time printing o2: {:.2f}".format(elapsed_time_o2))

# this should be done differently probably, with constant widths etc - maybe.
log("                                                       [H:MM:SS.microsec]")
log("Elapsed time:__________________________________________", elapsed_time_all)
log("\tAnd in it:")
log("\tElapsed time parsing gpx:______________________",elapsed_time_gpx)
log("\tElapsed time processing duplicates:_____________ ",elapsed_time_everything_dupes)
log("\tAnd in it:")
log("\t\tElapsed time collecting duplicates:____",elapsed_time_collecting_dupes)
log("\t\tElapsed time printing o2:______________",elapsed_time_o2)

