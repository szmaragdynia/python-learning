# Adding one second to copied does not work.


#------------------
# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files
# this script is for cleaning up data from gps, in order for it to work somehow in after effects

# Todos not necessarily in any particular order
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now
# Todo: make it into separate modules. (this code begs refactorization)
# Todo: how I format indentation in print to file seems to be done in a bad manner. What is help of what I do, if I still need to calculate the length of string I want to indent? My design is probably choosen badly.
# Todo: replace "quit" with real error handling
# Todo: use next() or mere for loop - mixing measure with measures[i+1] is utterly poor style

# perhaps should have used virtual environment
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

tab = "    " # 4 spaces



# -------------------------------------------- reading and parsing gpx for further use --------------------------------------------
time_start_gpx = time.time()

gpx_filename = "kubaORG.gpx"
with open(path_to_files_dir + gpx_filename, 'r') as gpx_file:
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
logger("\n\n~< ------------------------REMOVING DUPLICATES------------------------") # ~<  is for my defined language in notepad++, which allows me to fold text

indexes_to_delete = []
digs_msr = len(str(len(measures_list))) #number of digits needed to write down the length of my list + tab for prettiness
logger("~< what is added to deletion list", end = '',stream = "fileOnly")
for i in range(len(measures_list)-1):
    logger("\n{0}{1}/{2:<{3}}".format(tab,len(measures_list) - 1, i, digs_msr*2), end="")
    
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
                    logger (i,"(i) is added to deletion list.", end='', stream="fileOnly")
                elif measures_list[i+1]["elevation_m"] == None:                      # if the current measure has None in Elevation
                    indexes_to_delete.append(i+1)
                    logger (i+1,"(i+1) is added to deletion list.", end='', stream="fileOnly")
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
logger("\n~>",stream = "fileOnly")

digs_del = len(str(len(indexes_to_delete)))
logger("\n\nList of indexes to delete:\n",tab,indexes_to_delete, sep='')
logger("\n~< Elevations \"of indexes\" TO DELETE (should ALL BE \"None\"):", stream="fileOnly")
logger("{0}{1:<{2}}{3}".format(tab,"Index", 3*digs_del, "Elevation"), stream = "fileOnly")
for index in indexes_to_delete:
    logger("{0}{1:<{2}}{3}".format(tab,index, 3*digs_del, measures_list[index]['elevation_m']), stream="fileOnly")
logger("\n~>",stream = "fileOnly")    

time_start_o2 = time.time()
logger("\n~< Entering [almost] o^2 space. Be patient.", stream="fileOnly")    # I underestimated (even not so modern) CPU computational power.
logger("Elevations \"of indexes\" NOT TO DELETE (should all HAVE VALUE):", stream="fileOnly")
logger("{0}{1:<{2}}{3}".format(tab,"Index", 3*digs_del, "Elevation"), stream="fileOnly")    
for i,measure in enumerate(measures_list):
    matching_value = next((index for index in indexes_to_delete if index == i), None)   # list comprehension in next - generator expression is used (read more some time)
        # if this index IS EQUAL to any of the indexes to delete. 
        # USE WITH CAUTION, TIME HEAVY! (o^2 almost) - I could log these previously, but this serves as double-check.
    if matching_value == None:  # if no index is equal to current index = current index is not on a list to delete
        logger("{0}{1:<{2}}{3}".format(tab, i, 3*digs_del, measure["elevation_m"]), stream="fileOnly")    
            #this above will not work as expected    
logger("~>",stream = "fileOnly")
time_end_o2 = time.time()
    

indexes_to_delete.sort(reverse=True)
logger("\nDeleting i:\n",tab, sep = '', end = '')
for index in indexes_to_delete:    
    logger(index,end =', ')
    del measures_list[index]
logger(".", end = '') 
logger("\n~>",stream = "fileOnly") # ~> is for my defined language in notepad++, which allows me to fold text
    
    

output_filename_step2_csv = gpx_filename[:gpx_filename.index(".")] + "__2no-duplicates.csv" 
with open(path_to_files_dir + output_filename_step2_csv, 'w', newline='') as output_file: 
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list)
            
time_end_everything_dupes = time.time()

# -------------------------------------------- populating missing data --------------------------------------------
# After effects expects data every second. I need data every second, even if data is empty or fake. We will copy previous values
logger("~< ------------POPULATING MISSING DATA------------") 

measures_list_populated = copy.copy(measures_list)
added_entries_so_far = 0                                            # necessary to know how many items were added so far, for keeping proper indexes in output dictionary
                                                                    # I could go backwards...but I had gone forwards previously and now I will just reuse the logic.                                                               
for i, measure in enumerate(measures_list[:-1]):                    # iterate over all except last, because it does not have the next element
    logger("{0}/{1:<{2}}/(new list index={3})".format(len(measures_list) - 1, i, digs_msr, i+added_entries_so_far))
    
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
    # these work
        #logger(next_datetime.date())
        #logger("{}".format(next_datetime.date()))
    # but neither of these do: 
        #logger(f"{next_datetime.date():>20}")
        #logger("{:>4}".format(next_datetime.date()))
    # I do not need now to inspect and explore this

    logger("{0}{1:<{2}}{3:<{4}} - current element datetime."
           .format(tab, current_datetime.date().isoformat(), 18, current_datetime.time().isoformat(),  16),
           stream="fileOnly") # magic numbers out of string lengths
    logger("{0}{1:<{2}}{3:<{4}} - next element datetime."
           .format(tab, next_datetime.date().isoformat(), 18, next_datetime.time().isoformat(), 16)
           ,stream="fileOnly")
    logger("{0:<{1}}{2} - number of entries added so far."
           .format('', 16, added_entries_so_far), stream="fileOnly") #tab and then the same amount of space as in previous line
    
    if time_difference_in_seconds > 1:
        n_missing_entries = time_difference_in_seconds - 1
        if n_missing_entries < 5:
            logger("{0:<{1}}{2} missing (Time difference bigger than 1 second occured)."
           .format('', 16, n_missing_entries), stream="fileOnly") 
        elif n_missing_entries >=5:
            logger("~< {0:<{1}}{2} missing (Time difference bigger than 1 second occured)."
           .format('', 16, n_missing_entries), stream="fileOnly") 
        for j in range(n_missing_entries):
            insert_before_index = (i + 1) + added_entries_so_far    # with every entries added previously, the index from the dictionary list python is reading from differs from the dictionary list python is writing to. 
            measure_copy = measure.copy()
            logger("~< {0:<{1}}{2}/{3}".format('',16, n_missing_entries, j+1))
            logger("{0:<{1}}Object to be inserted, BEFORE updating its data:".format('',16), stream = "fileOnly")
            logger("{0}{1:<{2}}{3}".format(tab,'', 16, measure_copy), stream = "fileOnly")
            measure_copy["datetimeISO8601"] = (datetime.fromisoformat(measure["datetimeISO8601"]) + timedelta(seconds=1+j)).isoformat()
            measure_copy["original_data"] = False
            logger("{0:<{1}}Object to be inserted, AFTER updating its data:".format('',16), stream = "fileOnly")
            logger("{0}{1:<{2}}{3}".format(tab,'', 16, measure_copy), stream = "fileOnly")
            logger("{0:<{1}}It will be insterted before index: {2}".format('',16, insert_before_index), stream = "fileOnly")
            logger("{0}{1:<{2}} which holds this object:".format(tab, '', 16, ), stream = "fileOnly")
            logger("{0}{1:<{2}}{3}".format(tab,'', 16, measures_list_populated[insert_before_index]), stream = "fileOnly")
            measures_list_populated.insert(insert_before_index, measure_copy)    #insert before (i+1)-th element
            logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index-1), stream="fileOnly" )
            logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index-1]), stream = "fileOnly")
            logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index), stream="fileOnly" )
            logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index]), stream = "fileOnly")
            logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index+1), stream="fileOnly" )
            logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index+1]), stream = "fileOnly")
            logger("~>")
            added_entries_so_far = added_entries_so_far + 1 #keeping track of how many more entries there are in the output dictionary list
        if n_missing_entries >= 5:
            logger("~>",stream = "fileOnly")
    elif time_difference_in_seconds == 0:                                   
            logger("\n\n\nBug, the previous step (deleting duplicates) seems to have failed. Program will now exit.")
            exit()
    elif time_difference_in_seconds < 0:                                   
            logger("\n\n\nSerious bug! Next time is earlier than previous time! Program will now exit.")
            exit()
logger("~>",stream = "fileOnly")

output_filename_step3_csv = gpx_filename[:gpx_filename.index(".")] + "__3no-missing-values.csv" 
with open(path_to_files_dir + output_filename_step3_csv, 'w', newline='') as output_file: 
   dict_writer = csv.DictWriter(output_file, fieldnames=csv_headers)
   dict_writer.writeheader()
   dict_writer.writerows(measures_list_populated)
            
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


logger("\n\n------------FINISHED------------") 

logger("{0:<{1}}{2}".format('', 40, "[H:MM:SS.microsec]")) 
logger("{0:<{1}}{2}".format("Elapsed time:", 40, elapsed_time_all)) 

logger("{0}{1:<{2}}{3}".format(tab, "....parsing gpx:", 36, elapsed_time_gpx)) 
logger("{0}{1:<{2}}{3}".format(tab, "....processing duplicates:", 36, elapsed_time_everything_dupes)) 
logger("{0}{1:<{2}}{3}".format(2*tab, "....collecting duplicates:", 32, elapsed_time_collecting_dupes)) 
logger("{0}{1:<{2}}{3}".format(2*tab, "....printing o2:", 32, elapsed_time_o2)) 
logger("{0}{1:<{2}}{3}".format(tab,"...populating missing:", 36, elapsed_time_populating_missing)) 
log_file.close()
