# I merged files, now its time to check precisely whether it worked (see in log). Also make logging dictionaries better. Also change what and how is being logged in populating section.
    # also update logger so that I can choose whether I log to console, file, or both


#------------------
# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files

# this script is for cleaning up data from gps, in order for it to work somehow in after effects

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
from datetime import timedelta, datetime
import copy

time_start = time.time()

path_to_file_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"
gpx_filename = "kubaORG.gpx"

log_filename = "log.txt"
log_file = open(path_to_file_dir + log_filename, 'w')

def log(stream="both",*args_list, **keyword_args_dict):                          # names for future-me
    if stream == "both":
        print(*args_list, **keyword_args_dict)
        print(*args_list, file=log_file, **keyword_args_dict)
    elif stream == "console":
        print(*args_list, **keyword_args_dict)
    elif stream == "file":
        print(*args_list, file=log_file, **keyword_args_dict)

# -------------------------------------------- reading and parsing gpx for further use --------------------------------------------
time_start_gpx = time.time()
gpx_file = open(path_to_file_dir + gpx_filename, 'r')
gpx = gpxpy.parse(gpx_file)

measures_list = []
for track in gpx.tracks[:1]:                                        # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
    for segment in track.segments[:1]: # same as above
        for point in segment.points[:30]:                                # --------- BEWARE OF THE >TEMPORARY< RESTRICTION FOR TESTING-CODE PURPOSES
            measures_list.append({
                            "original_data": True, 
                            "latitude_deg": point.latitude,
                             "longitude_deg": point.longitude,
                             "elevation_m": point.elevation,
                             "datetimeISO8601": point.time.isoformat(),
                             "time": point.time.time().isoformat(),   # "time" is handy for 'debugging' in After Effects
                             "date": point.time.date().isoformat()    # "time" is handy for 'debugging' in After Effects
                             }) 



# saving at this stage, so that I can take a peek at what is going on
csv_headers = measures_list[0].keys()
output_filename_step1_csv = gpx_filename[:gpx_filename.index(".")] + "__1data-straight-from-gpx.csv" # add postfix and change extension
with open(path_to_file_dir + output_filename_step1_csv, 'w', newline='') as output_file:             #  '' is imporant, beacuse else I get empty rows in csv every entry
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)

time_end_gpx = time.time()


# -------------------------------------------- removing duplicates --------------------------------------------
#this is very, very, very ugly. I just wanted to finish merging, tidying will be the next step (should that step occur)
log("\n\n------------REMOVING DUPLICATES------------\n\n")

indexes_to_delete = []
for i in range(len(measures_list)-1):
    log("\n", len(measures_list)-1, "/", i,  end='\t')
    if (measures_list[i]["time"] == measures_list[i+1]["time"]):                          # if this measure seems to be duplicate of the next one
        if (None in measures_list[i].values() and not None in measures_list[i+1].values()) or (not None in measures_list[i].values() and None in measures_list[i+1].values()): 
                                                                                # only one of two dicts can have some None values.
            if not any([
                measures_list[i]["original_data"] == None,
                measures_list[i]["latitude_deg"] == None,
                measures_list[i]["longitude_deg"] == None,
                measures_list[i]["datetimeISO8601"] == None,
                measures_list[i]["time"] == None,
                measures_list[i]["date"] == None,
                measures_list[i+1]["original_data"] == None,
                measures_list[i+1]["latitude_deg"] == None,
                measures_list[i+1]["longitude_deg"] == None,
                measures_list[i+1]["datetimeISO8601"] == None,
                measures_list[i+1]["time"] == None,
                measures_list[i+1]["date"] == None,
            ]):                                                                 # the only key that has None value is Elevation (it's missing from the logic above, and we know that only one of two dicts have None as value)
                if measures_list[i]["elevation_m"] == None:                          # if the current measure has None in Elevation
                    indexes_to_delete.append(i)
                    log ("Adding index i to deletion list, i:",i, end='')
                elif measures_list[i+1]["elevation_m"] == None:                      # if the current measure has None in Elevation
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
    log(index,":",measures_list[index]["elevation_m"])

time_start_o2 = time.time()
log("\nEntering [almost] o^2 space. Be patient.")                                               # I underestimated (even not so modern) CPU computational power.
log("\nElevations \"of indexes\" NOT TO DELETE (should all HAVE VALUE):")
for i,measure in enumerate(measures_list):
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
    del measures_list[index]
    
    

output_filename_step2_csv = gpx_filename[:gpx_filename.index(".")] + "__2no-duplicates.csv" 
with open(path_to_file_dir + output_filename_step2_csv, 'w', newline='') as output_file: 
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)
            
time_end_everything_dupes = time.time()

# -------------------------------------------- populating missing data --------------------------------------------
# After effects expects data every second. I need data every second, even if data is empty or fake. We will copy previous values
log("\n\n------------POPULATING MISSING DATA------------\n\n")

measures_list_copy = copy.copy(measures_list)
added_entries_so_far = 0                                            # necessary to know how many items were added so far, for keeping proper indexes in output dictionary
                                                                    # I could go backwards...but I had gone forwards previously and now I will just reuse the logic.
for i, measure in enumerate(measures_list[:-1]):                         #iterate over all except last, because it does not have the next element
    log("\n", len(measures_list)-1, "/", i)
    current_time = datetime.strptime(measure["time"], "%H:%M:%S")
    next_time = datetime.strptime(measures_list[i+1]["time"], "%H:%M:%S")
    
    time_difference_in_seconds = (next_time - current_time).seconds
    
    log("\tadded_entries_so_far:", added_entries_so_far)
    log("\ti: ", i)
    log("\tCurrent element time:", current_time)
    log("\tNext element time:", next_time)

    if time_difference_in_seconds > 1:
        log("\t----------Time difference >1second occured")
        insert_before_index = (i + 1) + added_entries_so_far            # with every entries added previously, the index from the dictionary list python is reading from differs from the dictionary list python is writing to. 
        n_missing_entries = time_difference_in_seconds - 1
        log("\t\tNumber of missing entries:", n_missing_entries)

        for j in range(n_missing_entries):
            log("\t\t",n_missing_entries,"/",j)
            measure_copy = measure.copy()
            log("\t\t\t-measure_copy BEFORE modification\n","\t\t\t",json.dumps(measure_copy, indent=4))
            measure_copy["time"] = (datetime.strptime(measure["time"], "%H:%M:%S") + timedelta(seconds=1)).isoformat()
                                                                        # add one second to the time of the current measure
                                                                        # This loops will be run often, I don't want to make variable for "newtime" just for sake of it. It's readable!
                                                                        # BEWARE! NOT HANDLING CHANGING DATE NOR DATETIMEISOFORMAT, SHOULD TIME+1 CHANGE DAY!
            measure_copy["original_data"] = False

            log("\t\t\t-measure_copy AFTER modification\n","\t\t\t",json.dumps(measure_copy, indent=4))
            log("---------------------")
            log("\t\t\t\tInserting before index", insert_before_index, "which is", json.dumps(measures_list_copy[insert_before_index]))
            log("\t\t\t\tThe item inserted is:\n,","\t\t\t\t",json.dumps(measure_copy, indent=4))
            
            measures_list_copy.insert(insert_before_index, measure_copy)    #insert before (i+1)-th element
        added_entries_so_far += n_missing_entries                           #keeping track of how many more entries there are in the output dictionary list
    elif time_difference_in_seconds == 0:                                   
            log("\n\n\nBug, the previous step (deleting duplicates) seems to have failed. Program will now exit.")
            exit()
    elif time_difference_in_seconds < 0:                                   
            log("\n\n\nSerious bug! Next time is earlier than previous time! Program will now exit.")
            exit()

output_filename_step3_csv = gpx_filename[:gpx_filename.index(".")] + "__3no-missing-values.csv" 
with open(path_to_file_dir + output_filename_step3_csv, 'w', newline='') as output_file: 
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)
            
time_end_populating_missing = time.time()


# ------------------------------------------------------------------------
#with open(path_to_file_dir + output_filename, 'w') as f:
#  json.dump(measures_list, f, indent=2)
# divide for AE!

time_end = time.time()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
elapsed_time_gpx = timedelta(seconds=time_end_gpx - time_start_gpx)
elapsed_time_everything_dupes = timedelta(seconds=time_end_everything_dupes - time_end_gpx)
elapsed_time_collecting_dupes = timedelta(seconds=time_end_collecting_dupes - time_end_gpx)
elapsed_time_o2 = timedelta(seconds=time_end_o2 - time_start_o2)
elapsed_time_populating_missing = timedelta(seconds=time_end_populating_missing - time_end_everything_dupes)


log("\n\n\nFINISHED.")

# this should be done differently probably, with constant widths etc - maybe.
log("                                                       [H:MM:SS.microsec]")
log("Elapsed time:__________________________________________", elapsed_time_all)
log("\tAnd in it:")
log("\tElapsed time parsing gpx:______________________",elapsed_time_gpx)
log("\tElapsed time processing duplicates:___________ ",elapsed_time_everything_dupes)
log("\tAnd in it:")
log("\t\tElapsed time collecting duplicates:____",elapsed_time_collecting_dupes)
log("\t\tElapsed time printing o2:______________",elapsed_time_o2)
log("\tElapsed time populating missing:_______________",elapsed_time_populating_missing)

