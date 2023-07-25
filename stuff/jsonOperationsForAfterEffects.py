# this file is for cleaning up data from gps, in order for it to work somehow in after effects
# I need a record every second, even if it would be empty.

import json
import copy

# Load the data from the file
with open(r'E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\moje, strava\Przehyba_z_Kuba_rower_.json', 'r') as f:
    json_array_read = json.load(f)
json_array_write = copy.deepcopy(json_array_read)

added_entries_so_far = 0 #necessary to know how many items were added so far, for keeping right indexes in output json array (write)
n_entries = len(json_array_read)

for i, read_entry in enumerate(json_array_read[:-1]): #iterate over all except last, because it does not have the next element
    print(n_entries-2,"/",i)
    curr_entry_nrml_time = read_entry['normalized time in seconds']
    nxt_entry_nrml_time = (json_array_read[i + 1])['normalized time in seconds']
    
    n_missing_entries = nxt_entry_nrml_time - curr_entry_nrml_time - 1 #if 3 exists and the next is 6, we need 4,5 - two elements 
    
    # print("added_entries_so_far:", added_entries_so_far)
    # print("i: ", i)
    # print("this_elem_normalized_time:", curr_entry_nrml_time)
    # print("next_elem_normalized_time:", nxt_entry_nrml_time)
    # print("n_missing_entries:", n_missing_entries)
    
    if n_missing_entries > 0:
        insert_before_index = (i + 1) + added_entries_so_far
        for j in range(n_missing_entries):
            # print("\tj=", j, "out of ", n_missing_entries)
            entry_updated_copy = read_entry.copy()
            # print("\n-entry_updated_copy_BEFORE_for_j-\n",entry_updated_copy)
            entry_updated_copy['normalized time in seconds'] += n_missing_entries - j 
            entry_updated_copy['real values'] = "FALSE"
            # print("\n-entry_updated_copy_AFTER_CHANGES-\n",entry_updated_copy)

            # print("\n----\ninserting before index: ", insert_before_index, "\nwhich is\n:", json_array_write[insert_before_index],"\nand I am inserting this:\n",entry_updated_copy)
            
            json_array_write.insert(insert_before_index, entry_updated_copy) #insert before (i+1)-th element
        added_entries_so_far += n_missing_entries #keep track of how many more entries there are in the output file
    
    if n_missing_entries == -1: #they have the same time
        del json_array_write[i + added_entries_so_far]
        added_entries_so_far += n_missing_entries
        # I am not setting any flag for pointing out deleting some data. Well, meh. Too much hassle for almost(or literaly) no value (no pun intended[really]).

# Save the modified data to the file
with open(r'E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\moje, strava\Przehyba_z_Kuba_rower_cleanUp.json', 'w') as f:
    json.dump(json_array_write, f, indent=2)
