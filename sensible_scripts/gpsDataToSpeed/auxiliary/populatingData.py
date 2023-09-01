import copy
from auxiliary.utils import logger, nDigitsToWriteDownIndex
from datetime import datetime, timedelta
from auxiliary.constants import tab

# I am not certain that is good practice, however the logging statement are really messing up the code. This works for me.
def debugLogger0(current_datetime, next_datetime, added_entries_so_far):
    logger("{0}{1:<{2}}{3:<{4}} - current element datetime."
        .format(tab, current_datetime.date().isoformat(), 18, current_datetime.time().isoformat(),  16),
        stream="fileOnly") # magic numbers out of string lengths
    logger("{0}{1:<{2}}{3:<{4}} - next element datetime."
        .format(tab, next_datetime.date().isoformat(), 18, next_datetime.time().isoformat(), 16)
        ,stream="fileOnly")
    logger("{0:<{1}}{2} - number of entries added so far."
        .format('', 16, added_entries_so_far), stream="fileOnly") #tab and then the same amount of space as in previous line

def debugLogger1(n_missing_entries):
    if n_missing_entries < 5:
        logger("{0:<{1}}{2} missing (Time difference bigger than 1 second occured)."
    .format('', 16, n_missing_entries), stream="fileOnly") 
    elif n_missing_entries >=5:
        logger("~< {0:<{1}}{2} missing (Time difference bigger than 1 second occured)."
    .format('', 16, n_missing_entries), stream="fileOnly") 

def debugLogger2(n_missing_entries, measure_copy,j):
    logger("~<", stream="fileOnly")
    logger("{0:<{1}}{2}/{3}".format('',16, n_missing_entries, j+1))
    logger("{0:<{1}}Object to be inserted, BEFORE updating its data:".format('',16), stream = "fileOnly")
    logger("{0}{1:<{2}}{3}".format(tab,'', 16, measure_copy), stream = "fileOnly")

def debugLogger3(insert_before_index, measure_copy,measures_list_populated):
    logger("{0:<{1}}Object to be inserted, AFTER updating its data:".format('',16), stream = "fileOnly")
    logger("{0}{1:<{2}}{3}".format(tab,'', 16, measure_copy), stream = "fileOnly")
    logger("{0:<{1}}It will be insterted before index: {2}".format('',16, insert_before_index), stream = "fileOnly")
    logger("{0}{1:<{2}} which holds this object:".format(tab, '', 16, ), stream = "fileOnly")
    logger("{0}{1:<{2}}{3}".format(tab,'', 16, measures_list_populated[insert_before_index]), stream = "fileOnly")

def debugLogger4(insert_before_index, measures_list_populated):
    logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index-1), stream="fileOnly" )
    logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index-1]), stream = "fileOnly")
    logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index), stream="fileOnly" )
    logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index]), stream = "fileOnly")
    logger("\n{0:<{1}}Now object in the index {2} is: ".format('', 16,insert_before_index+1), stream="fileOnly" )
    logger("{0}{1:<{2}}{3}".format(tab, '', 16, measures_list_populated[insert_before_index+1]), stream = "fileOnly")
    logger("~>", stream="fileOnly")

def debugLogger5(n_missing_entries):
    if n_missing_entries >= 5:
        logger("~>",stream = "fileOnly")

# After effects expects data every second. I need data every second, even if data is empty or fake. We will copy previous values
def populateMissingData(dictionaries_list):
    measures_list_populated = copy.copy(dictionaries_list)
    added_entries_so_far = 0                                            # necessary to know how many items were added so far, for keeping proper indexes in output dictionary - I could go backwards...but I had gone forwards previously and now I will just reuse the logic                                                             
    for i, measure in enumerate(dictionaries_list[:-1]):                # iterate over all except last, because it does not have the next element
        digs_msr = nDigitsToWriteDownIndex(dictionaries_list)
        logger("{0}/{1:<{2}}=new list index={3}".format(len(dictionaries_list) - 1, i, digs_msr, i+added_entries_so_far))
        current_datetime = datetime.fromisoformat(measure["datetimeISO8601"])
        next_datetime = datetime.fromisoformat(dictionaries_list[i+1]["datetimeISO8601"])
        time_difference_in_seconds = (next_datetime - current_datetime).total_seconds() #total seconds returns float (Because its datetime/timedelta(seconds=1) under the hood, so you could have ...seconds=3)
                                                                                        # mere (next_datetime - current_datetime) is of type timedelta, created from two datetime type objects
        if time_difference_in_seconds.is_integer():
                time_difference_in_seconds = int(time_difference_in_seconds)
        else:
            logger("\n\n\nGetting total seconds out of difference between two measures, total seconds resulting came out NOT TO BE integeres. Program will now quit.")
            exit()
        debugLogger0(current_datetime, next_datetime, added_entries_so_far)
        if time_difference_in_seconds > 1:
            n_missing_entries = time_difference_in_seconds - 1
            debugLogger1(n_missing_entries)
            for j in range(n_missing_entries):
                insert_before_index = (i + 1) + added_entries_so_far                 # with every entries added previously, the index from the dictionary list python is reading from differs from the dictionary list python is writing to. 
                measure_copy = measure.copy()
                debugLogger2(n_missing_entries, measure_copy, j)
                measure_copy["datetimeISO8601"] = (datetime.fromisoformat(measure["datetimeISO8601"]) + timedelta(seconds=1+j)).isoformat()
                measure_copy["original_data"] = False
                debugLogger3(insert_before_index, measure_copy,measures_list_populated)
                measures_list_populated.insert(insert_before_index, measure_copy)    # insert before (i+1)-th element
                debugLogger4(insert_before_index, measures_list_populated)
                added_entries_so_far = added_entries_so_far + 1                      # keeping track of how many more entries there are in the output dictionary list
            debugLogger5(n_missing_entries)
        elif time_difference_in_seconds == 0:                                   
                logger("\n\n\nBug, the previous step (deleting duplicates) seems to have failed. Program will now exit.")
                exit()
        elif time_difference_in_seconds < 0:                                   
                logger("\n\n\nSerious bug! Next time is earlier than previous time! Program will now exit.")
                exit()
    logger("~>",stream = "fileOnly")
    return measures_list_populated    
  