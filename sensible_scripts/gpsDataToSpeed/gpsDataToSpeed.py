# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files

# this script is for cleaning up data from gps and calculating speed, so its useful in After Effects
# CSVs are saved after every stage, so that I can take a peek at what is going on

# Todos not necessarily in any particular order
# Todo: code in seperate modules needs further refactorization
# Todo: how I format indentation in print to file seems to be done in a bad manner. What is help of what I do, if I still need to calculate the length of string I want to indent? My design is probably choosen badly.
# Todo: replace "quit" with real error handling
# Todo: use next() or mere for loop - mixing measure with measures[i+1] is utterly poor style
# Todo: either look-ahead or look-backwards. I am mixing approaches with no reason (maybe there will come out one, but as of now, this is by accident (as far as I remember))
# Todo: do this using pandas. I tried to do that, but it was overkill, I prioretise finishing this, and I already have "classic" logic - no need to waste time for learning pandas right now

import time
from datetime import timedelta, datetime
# ----------------
from auxiliary import utils
from auxiliary.utils import logger
from auxiliary import constants
import auxiliary.gpxFunctions as gpxFunctions
from auxiliary import duplicatesProcessingFunctions as duplicates
from auxiliary.populatingData import populateMissingData
from auxiliary.speedCalculation import calculateAndAssign

time_start = time.perf_counter()
logger(datetime.fromtimestamp(time.time()))

logger("\n\n~< ------READING AND PARSING GPX-----") # ~<  is for my defined language in notepad++, which allows me to fold text
measures_list = gpxFunctions.makeDictFromGpx(1000)  #input range end or leave empty for all
utils.saveDictListAsCsv(measures_list, constants.output_filename_step1_csv)




# this is separetely from gpx, because of semantics
logger("\n\n ------OFFSETTING TIME-----") #
utils.offsetTime(measures_list, delta_hours=3, delta_minutes=0, delta_seconds = 0) # writing arguments with zero as reminder for future myself that I made these possible to set up



logger("\n\n~< -----REMOVING DUPLICATES-----")
duplicates.collect(measures_list)
duplicates.showIndexesToDelete(measures_list)
duplicates.checkIndexesToDeleteAgainstOriginalList(measures_list)   
duplicates.remove(measures_list)
utils.saveDictListAsCsv(measures_list, constants.output_filename_step2_csv)

gpxFunctions.saveDictToGPX(measures_list, constants.gpx_out_file_no_duplicates)


logger("~< -----POPULATING MISSING DATA-----") 
measures_list_populated = populateMissingData(measures_list)
utils.saveDictListAsCsv(measures_list_populated, constants.output_filename_step3_csv)

gpxFunctions.saveDictToGPX(measures_list_populated, constants.gpx_out_file_populated)
                           
           
logger("~< -----CALCULATING SPEED-----")
measures_list_populated = calculateAndAssign(measures_list_populated)

utils.saveDictListAsCsv(measures_list_populated, constants.output_filename_step4_csv)
# ------------------------------------------------------------------------
#with open(path_to_files_dir + output_filename, 'w') as f:
#  json.dump(measures_list, f, indent=2)
# divide for AE!

logger("\n\n------------FINISHED------------") 
time_end = time.perf_counter()
elapsed_time_all =  timedelta(seconds=time_end - time_start)
logger("{0:<{1}}{2}".format('', 40, "[H:MM:SS.microsec]")) 
logger("{0:<{1}}{2}".format("Elapsed time:", 40, elapsed_time_all)) 



