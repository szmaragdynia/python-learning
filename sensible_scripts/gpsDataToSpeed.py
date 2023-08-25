# I merged files, now its time to check precisely whether it worked (see in log). Also make logging dictionaries better. Also change what and how is being logged in populating section.
    # also update logger so that I can choose whether I log to console, file, or both
    # make these widths proper
#use next() or mere for loop - mixing measure with measures[i+1] is utterly poor style



#------------------
# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files

# this script is for cleaning up data from gps, in order for it to work somehow in after effects

# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now
# Todo: make it into separate modules...or am I biased?
# Todo: swap tabs with constant widths wherever appropriate
# Todo: replace "quit" with real error handling

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
path_to_files_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\\"


log_filename = "log.txt"
log_file = open(path_to_files_dir + log_filename, 'w')

def logger(*args_list, **keyword_args_dict):                          # names for future-me
    if "stream" in keyword_args_dict:
        if keyword_args_dict["stream"] == "consoleOnly":
            del keyword_args_dict["stream"]                           # so it's not "used" (and crashed) by print
            print(*args_list, **keyword_args_dict)
        elif keyword_args_dict["stream"] == "fileOnly":
            del keyword_args_dict["stream"] 
            print(*args_list, file=log_file, **keyword_args_dict)
    else:
        print(*args_list, **keyword_args_dict)
        print(*args_list, file=log_file, **keyword_args_dict)

tab_width = 4 # used in string formatting for prettiness


# -------------------------------------------- reading and parsing gpx for further use --------------------------------------------
time_start_gpx = time.time()

gpx_filename = "kubaORG.gpx"
with open(path_to_files_dir + gpx_filename, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

measures_list = []
for track in gpx.tracks[:1]:                                        # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
    for segment in track.segments[:1]: # same as above
        for point in segment.points[:10]:                                # --------- BEWARE OF THE >TEMPORARY< RESTRICTION FOR TESTING-CODE PURPOSES
            measures_list.append({
                            "original_data": True, 
                            "latitude_deg": point.latitude,
                             "longitude_deg": point.longitude,
                             "elevation_m": point.elevation,
                             "datetimeISO8601": point.time.isoformat(),
                             }) 

# saving at this stage, so that I can take a peek at what is going on
csv_headers = measures_list[0].keys()
output_filename_step1_csv = gpx_filename[:gpx_filename.index(".")] + "__1data-straight-from-gpx.csv" # add postfix and change extension
with open(path_to_files_dir + output_filename_step1_csv, 'w', newline='') as output_file:             #  '' is imporant, beacuse else I get empty rows in csv every entry
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)

time_end_gpx = time.time()


# -------------------------------------------- removing duplicates --------------------------------------------
#this is somewhat (very?) ugly - espacially the logic for checking keys and values. I just wanted to finish merging, tidying will be the next step (should that step occur)
logger("\n\n~< ------------------------REMOVING DUPLICATES------------------------", end='') # ~<  is for my defined language in notepad++, which allows me to fold text

indexes_to_delete = []
digs_msr = len(str(len(measures_list))) + tab_width #number of digits needed to write down the length of my list + tab for prettiness
for i in range(len(measures_list)-1):
    logger("\n{0}/{1:<{2}}".format(len(measures_list) - 1, i, digs_msr), end="")
    
    if (measures_list[i]["datetimeISO8601"] == measures_list[i+1]["datetimeISO8601"]):                          # if this measure seems to be duplicate of the next one
        if (None in measures_list[i].values() and not None in measures_list[i+1].values()) or (not None in measures_list[i].values() and None in measures_list[i+1].values()): 
                                                                                # only one of two dicts can have some None values.
            if not any([
                measures_list[i]["original_data"] == None,
                measures_list[i]["latitude_deg"] == None,
                measures_list[i]["longitude_deg"] == None,
                measures_list[i]["datetimeISO8601"] == None,
                measures_list[i+1]["original_data"] == None,
                measures_list[i+1]["latitude_deg"] == None,
                measures_list[i+1]["longitude_deg"] == None,
                measures_list[i+1]["datetimeISO8601"] == None,
            ]):                                                                 # the only key that has None value is Elevation (it's missing from the logic above, and we know that only one of two dicts have None as value)
                if measures_list[i]["elevation_m"] == None:                          # if the current measure has None in Elevation
                    indexes_to_delete.append(i)
                    logger (i,"is added to deletion list.", end='')
                elif measures_list[i+1]["elevation_m"] == None:                      # if the current measure has None in Elevation
                    indexes_to_delete.append(i+1)
                    logger (i+1,"is added to deletion list.", end='')
                else:
                    logger("\n\n\nBug, program will now exit. 1.")
                    exit()
            else:
                logger("\n\n\n1This case is not handled. Program will now exit (so you can upgrade the code or manually modify the files).")
                exit()
        else:
            logger("\n\n\n2This case is not handled. Program will now exit (so you can upgrade the code or manually modify the files).")
            exit()
time_end_collecting_dupes = time.time()

digs_del = len(str(len(indexes_to_delete))) + tab_width
logger("\n\nList of indexes to delete:\n",indexes_to_delete, sep='')
logger("\nElevations \"of indexes\" TO DELETE (should ALL BE \"None\"):")
for index in indexes_to_delete:
    logger("{0}:{1:<{2}}{3}".format(index, "", digs_del, measures_list[index]['elevation_m']))
    

time_start_o2 = time.time()
logger("\nEntering [almost] o^2 space. Be patient.")    # I underestimated (even not so modern) CPU computational power.
logger("Elevations \"of indexes\" NOT TO DELETE (should all HAVE VALUE):")
for i,measure in enumerate(measures_list):
    matching_value = next((index for index in indexes_to_delete if index == i), None)   # list comprehension in next - generator expression is used (read more some time)
        # if this index IS EQUAL to any of the indexes to delete. 
        # USE WITH CAUTION, TIME HEAVY! (o^2 almost) - I could log these previously, but this serves as double-check.
    if matching_value == None:  # if no index is equal to current index = current index is not on a list to delete
        logger("{0}:{1:<{2}}{3}".format(index, "", digs_del, measure["elevation_m"]))        

time_end_o2 = time.time()
    

indexes_to_delete.sort(reverse=True)
logger("\nDeleting i: ")
for index in indexes_to_delete:    
    logger(index,end =', ')
    del measures_list[index]
logger(".\n~>") # ~> is for my defined language in notepad++, which allows me to fold text
    
    

output_filename_step2_csv = gpx_filename[:gpx_filename.index(".")] + "__2no-duplicates.csv" 
with open(path_to_files_dir + output_filename_step2_csv, 'w', newline='') as output_file: 
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)
            
time_end_everything_dupes = time.time()

# -------------------------------------------- populating missing data --------------------------------------------
# After effects expects data every second. I need data every second, even if data is empty or fake. We will copy previous values
logger("\n\n~<------------POPULATING MISSING DATA------------", end ='') 

measures_list_copy = copy.copy(measures_list)
added_entries_so_far = 0                                            # necessary to know how many items were added so far, for keeping proper indexes in output dictionary
                                                                    # I could go backwards...but I had gone forwards previously and now I will just reuse the logic.
for i, measure in enumerate(measures_list[:-1]):                    # iterate over all except last, because it does not have the next element
    logger("\n{0}/{1:<{2}}".format(len(measures_list) - 1, i, digs_msr))
    current_datetime = datetime.fromisoformat(measure["datetimeISO8601"])
    next_datetime = datetime.fromisoformat(measures_list[i+1]["datetimeISO8601"])
    time_difference_in_seconds = (next_datetime - current_datetime).total_seconds()
        #total seconds returns float (Because its datetime/timedelta(seconds=1) under the hood, so you could have ...seconds=3)
        # mere (next_datetime - current_datetime) is of type timedelta, created from two datetime type objects
    if time_difference_in_seconds.is_integer():
            time_difference_in_seconds = int(time_difference_in_seconds)
    else:
        logger("\n\n\nGetting total seconds out of difference between two measures, total seconds resulting came out NOT TO BE integeres. Program will now quit.")
        exit()
    #logger("current datetime:",current_datetime)
    #logger("next datetime:",next_datetime)
    #logger(f"{current_datetime} - current element datetime.".rjust(tab_width,"*"))
    logger("----")
    logger(next_datetime.date())
    logger("----")
    logger("{:>4} {:>13} {:>17}".format('',next_datetime.date().isoformat(), next_datetime.time().isoformat()))
    #logger(f'{next_datetime.date():>30} {next_datetime.time():>30}', end='')
    #logger(" - next element time and date")


    #logger("{0:<{1}} - next element datetime.".format(next_datetime, tab_width))
    #logger("{0:<{1}} - number of entries added so far.".format(added_entries_so_far, tab_width))




    if time_difference_in_seconds > 1:
        logger("\t----------Time difference >1second occured")
        insert_before_index = (i + 1) + added_entries_so_far            # with every entries added previously, the index from the dictionary list python is reading from differs from the dictionary list python is writing to. 
        n_missing_entries = time_difference_in_seconds - 1
        logger("\t\tNumber of missing entries:", n_missing_entries)

        for j in range(n_missing_entries):
            logger("\t\t",n_missing_entries,"/",j)
            measure_copy = measure.copy()
            logger("\t\t\t-measure_copy BEFORE modification\n","\t\t\t",json.dumps(measure_copy, indent=4))
            measure_copy["datetimeISO8601"] = (datetime.fromisoformat(measure["datetimeISO8601"]) + timedelta(seconds=1)).isoformat()
                                                                        # add one second to the time of the current measure
                                                                        # This loops will be run often, I don't want to make variable for "newtime" just for sake of it. It's readable!
                                                                        # BEWARE! NOT HANDLING CHANGING DATE NOR DATETIMEISOFORMAT, SHOULD TIME+1 CHANGE DAY!
            measure_copy["original_data"] = False

            logger("\t\t\t-measure_copy AFTER modification\n","\t\t\t",json.dumps(measure_copy, indent=4))
            logger("---------------------")
            logger("\t\t\t\tInserting before index", insert_before_index, "which is", json.dumps(measures_list_copy[insert_before_index]))
            logger("\t\t\t\tThe item inserted is:\n,","\t\t\t\t",json.dumps(measure_copy, indent=4))
            
            measures_list_copy.insert(insert_before_index, measure_copy)    #insert before (i+1)-th element
        added_entries_so_far += n_missing_entries                           #keeping track of how many more entries there are in the output dictionary list
    elif time_difference_in_seconds == 0:                                   
            logger("\n\n\nBug, the previous step (deleting duplicates) seems to have failed. Program will now exit.")
            exit()
    elif time_difference_in_seconds < 0:                                   
            logger("\n\n\nSerious bug! Next time is earlier than previous time! Program will now exit.")
            exit()

output_filename_step3_csv = gpx_filename[:gpx_filename.index(".")] + "__3no-missing-values.csv" 
with open(path_to_files_dir + output_filename_step3_csv, 'w', newline='') as output_file: 
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)
            
time_end_populating_missing = time.time()


# ------------------------------------------------------------------------
#with open(path_to_files_dir + output_filename, 'w') as f:
#  json.dump(measures_list, f, indent=2)
# divide for AE!

time_end = time.time()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
elapsed_time_gpx = timedelta(seconds=time_end_gpx - time_start_gpx)
elapsed_time_everything_dupes = timedelta(seconds=time_end_everything_dupes - time_end_gpx)
elapsed_time_collecting_dupes = timedelta(seconds=time_end_collecting_dupes - time_end_gpx)
elapsed_time_o2 = timedelta(seconds=time_end_o2 - time_start_o2)
elapsed_time_populating_missing = timedelta(seconds=time_end_populating_missing - time_end_everything_dupes)


logger("\n\n\nFINISHED.")

# this should be done differently probably, with constant widths etc - maybe.
logger("                                                       [H:MM:SS.microsec]")
logger("Elapsed time:__________________________________________", elapsed_time_all)
logger("\tAnd in it:")
logger("\tElapsed time parsing gpx:______________________",elapsed_time_gpx)
logger("\tElapsed time processing duplicates:___________ ",elapsed_time_everything_dupes)
logger("\tAnd in it:")
logger("\t\tElapsed time collecting duplicates:____",elapsed_time_collecting_dupes)
logger("\t\tElapsed time printing o2:______________",elapsed_time_o2)
logger("\tElapsed time populating missing:_______________",elapsed_time_populating_missing)
log_file.close()
