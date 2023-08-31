from auxiliary.utils import logger, nDigitsToWriteDownIndex
from auxiliary.constants import tab


#this is somewhat (very?) ugly - espacially the logic for checking keys and values. I just wanted to finish merging, tidying will be the next step (should that step occur)

indexes_to_delete = []
digs_del = nDigitsToWriteDownIndex(indexes_to_delete)
def collect(dictionaries_list):
  digs_msr = nDigitsToWriteDownIndex(dictionaries_list) #number of digits needed to write down the length of my list
  logger("~< what is added to deletion list", end = '',stream = "fileOnly")
  for i in range(len(dictionaries_list)-1):
      logger("\n{0}{1}/{2:<{3}}".format(tab,len(dictionaries_list) - 1, i, digs_msr*2), end="")
      if (dictionaries_list[i]["datetimeISO8601"] == dictionaries_list[i+1]["datetimeISO8601"]):                          # if this measure seems to be duplicate of the next one
          if (None in dictionaries_list[i].values() and not None in dictionaries_list[i+1].values()) or (not None in dictionaries_list[i].values() and None in dictionaries_list[i+1].values()): 
                                                                                  # only one of two dicts can have some None values.
              if not any([
                  dictionaries_list[i]["original_data"] == None,
                  dictionaries_list[i]["latitude_deg"] == None,
                  dictionaries_list[i]["longitude_deg"] == None,
                  dictionaries_list[i]["datetimeISO8601"] == None,
                  dictionaries_list[i+1]["original_data"] == None,
                  dictionaries_list[i+1]["latitude_deg"] == None,
                  dictionaries_list[i+1]["longitude_deg"] == None,
                  dictionaries_list[i+1]["datetimeISO8601"] == None,
              ]):                                                                 # the only key that has None value is Elevation (it's missing from the logic above, and we know that only one of two dicts have None as value)
                  if dictionaries_list[i]["elevation_m"] == None:                          # if the current measure has None in Elevation
                      indexes_to_delete.append(i)
                      logger (i,"(i) is added to deletion list.", end='', stream="fileOnly")
                  elif dictionaries_list[i+1]["elevation_m"] == None:                      # if the current measure has None in Elevation
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
  logger("\n~>",stream = "fileOnly")


def showIndexesToDelete(dictionaries_list):     # behaviour of this function is not entirely logical - it is not obvious that it depends on the collect(). It would be better to implement both collect and showIndextesToDelete as options for a bigger function process, or maybe make a class.
  if indexes_to_delete == []:
        logger("Run collect() first. Program will now quit")
        exit()
  logger("\n\nList of indexes to delete:\n",tab,indexes_to_delete, sep='')
  logger("\n~< Elevations \"of indexes\" TO DELETE (should ALL BE \"None\"):", stream="fileOnly")
  logger("{0}{1:<{2}}{3}".format(tab,"Index", 3*digs_del, "Elevation"), stream = "fileOnly")
  for index in indexes_to_delete:
      logger("{0}{1:<{2}}{3}".format(tab,index, 3*digs_del, dictionaries_list[index]['elevation_m']), stream="fileOnly")
  logger("\n~>",stream = "fileOnly")


def checkIndexesToDeleteAgainstOriginalList(dictionaries_list):  # name of this function is probably awful. 
  logger("\n~< Entering [almost] o^2 space. Be patient.", stream="fileOnly")    # I underestimated (even not so modern) CPU computational power.
  logger("Elevations \"of indexes\" NOT TO DELETE (should all HAVE VALUE):", stream="fileOnly")
  logger("{0}{1:<{2}}{3}".format(tab,"Index", 3*digs_del, "Elevation"), stream="fileOnly")    
  for i,measure in enumerate(dictionaries_list):
      matching_value = next((index for index in indexes_to_delete if index == i), None)   # list comprehension in next - generator expression is used (read more some time)
          # if this index IS EQUAL to any of the indexes to delete. 
          # USE WITH CAUTION, TIME HEAVY! (o^2 almost) - I could log these previously, but this serves as double-check.
      if matching_value == None:  # if no index is equal to current index = current index is not on a list to delete
          logger("{0}{1:<{2}}{3}".format(tab, i, 3*digs_del, measure["elevation_m"]), stream="fileOnly")    
              #this above will not work as expected    
  logger("~>",stream = "fileOnly")


def remove(dictionaries_list):
  indexes_to_delete.sort(reverse=True)
  logger("\nDeleting i:\n",tab, sep = '', end = '')
  for index in indexes_to_delete:    
      logger(index,end =', ')
      del dictionaries_list[index]
  logger(".", end = '') 
  logger("\n~>",stream = "fileOnly") # ~> is for my defined language in notepad++, which allows me to fold text