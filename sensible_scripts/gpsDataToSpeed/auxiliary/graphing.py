# offset x labels to the left
# make it so that I can plot several things
  # beware of time! time must be in right place


import matplotlib.pyplot as plt
from auxiliary import utils
from auxiliary import constants
from datetime import datetime, timedelta
import json
from math import ceil
import numpy as np

def save_speeds_graph(path_to_json):
  with open(path_to_json, 'r') as file:
    json_list_full = json.load(file)

  #with default dpi, the number of jsons in one json list (10799) results in 179900 width, when only 65536 is allowed. Since this is 3 hours, I divide it by 3 to make each for one hour
  dividor = 1800 # half an hour in seconds
  n_parts = ceil((len(json_list_full) / dividor))  # how many images is needed - one for each started half an hour. Half an hour becase rendering data for an hours does not work (corrupted image)
  utils.logger("len json list full", len(json_list_full))
  utils.logger("n_parts:", n_parts)

  for i in range(n_parts):
    range_start = 0 + dividor * i # 
    range_end = dividor + dividor * i # range_end is not inclusive
    json_list = json_list_full[range_start : range_end]
    y_speeds = []
    j = 0
    for entry in json_list:
      #utils.logger("save graph, entry no.:",j)
      if "speed_kmh_haversine_math" in entry:
        if entry["speed_kmh_haversine_math"] == '':
          y_speeds.append(0)
        else:
          y_speeds.append(float(entry["speed_kmh_haversine_math"]))
      else:
        y_speeds.append(0)
      j+=1
    x_labels = [str(datetime.strptime(entry["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").time()) for entry in json_list]

    x_figSize = len(x_labels)//6 # x size should be 6 times smaller than amout of x data. This looks good for pdf/image.
    Plot, Axis = plt.subplots(figsize=(x_figSize, 6)) 
    plt.subplots_adjust(top=1)

    Axis.set_rasterized(True)
    
    
    color_map = {
      "dummy value": "pink",
      "[T->T->T...]": "black",
      "interpolated speed [T T->{F F F F T}-> T]": "orange",
      "average straight line displacement [{T->(F F F F)->T F}]": "red"
    }
    # map based on speed_source key, unles data is original, then "overwrite", so that we have color based on value source, not just the method it was connected with
    speed_sources = ["[T->T->T...]" if entry['original_data'] == True else entry['speed_source'] for entry in json_list]
    colors = [color_map[source] for source in speed_sources]

    plt.plot(x_labels, y_speeds, color="blue", zorder=1)
    plt.plot(x_labels, y_speeds, color="blue", zorder=2)
    plt.scatter(x_labels, y_speeds, c=colors, s=4, marker="o", zorder=3)
    x_shown_labels = ['' if i % 2 != 0 else str(x_labels[i]) for i in range(len(x_labels))]
    # Rotate the labels
    Axis.set_xticklabels(x_shown_labels, fontsize=7, rotation=90) 
    Axis.xaxis.set_tick_params(labelsize=8)

    Axis.grid(True, alpha=0.5)

    plt.ylim(-1, 75)

    for x, y in zip(x_labels, y_speeds):
        Axis.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 40), ha='center', fontsize=7, rotation=80)
        Axis.plot([x, x], [y, y+8], color='pink', linewidth=0.5)  # Add a line pointing to the annotation
        Axis.annotate('', xy=(x, 0), xytext=(x, - 3), arrowprops={'arrowstyle': '-', 'color': 'pink', 'linewidth': 0.5})


    from_time = datetime.strptime(json_list_full[range_start]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z")
    from_time_formatted = f"{from_time.hour};{from_time.minute};{from_time.second}"
    to_time = datetime.strptime(json_list_full[range_end-1]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z")
    to_time_formatted = f"{to_time.hour};{to_time.minute};{to_time.second}"


    plt.savefig(f"{constants.path_to_files_dir}{from_time_formatted} -- {to_time_formatted} --- {constants.image_filename}")
    plt.close()

    # Display the plot
    #plt.show()
    
    utils.logger(f"finished saving speed graph image {i+1} of {n_parts}")


_get_color = {
  0: "blue",
  1: "green",
}

#this ofc will crash if more than 23 files
_get_marker = {
    0: 'o',
    1: 'D',
    2: 'v',
    3: '^',
    4: '<',
    5: '>',
    6: '1',
    7: '2',
    8: '3',
    9: '4',
    10: 's',
    11: 'p',
    12: 'P',
    13: '*',
    14: 'h',
    15: 'H',
    16: '+',
    17: 'x',
    18: 'X',
    19: '.',
    20: 'd',
    21: '|',
    22: '_'
}

# code for the below is bad, it needs refactorization, I could be doing some things differently. It is the way it is, because I am in a hurry and I need this feature working ASAP and for one set of files now, and it shall not be used soon, so I prioritise making it working.
def save_speeds_graphs(*paths_to_jsons):
  # utils.logger(1)
  json_list_full_list = []
  for i, path in enumerate(paths_to_jsons):
    # utils.logger(2)
    with open(path, 'r') as file:
      json_list_full_list.append(json.load(file))

  # utils.logger(3)
  global_min_time = 4102444800 # January 1, 2100 12:00:00 AM
  global_max_time = 0          # January 1, 1970 12:00:00 AM
  min_time = 4102444800 # January 1, 2100 12:00:00 AM
  max_time = 0          # January 1, 1970 12:00:00 AM
  from_time = 0
  to_time = 0

  for json_list_full in json_list_full_list:
    # utils.logger(4)
    start_time = datetime.strptime(json_list_full[0]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()
    end_time = datetime.strptime(json_list_full[-1]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()
    if start_time < global_min_time:
      min_time = start_time
    if end_time > global_max_time:
      max_time = end_time
    
  # utils.logger(max_time)
  # utils.logger(min_time)
  # utils.logger(5)
  x_length_global = (datetime.fromtimestamp(max_time) - datetime.fromtimestamp(min_time)).total_seconds() + 1 # +1 because if 2 measures exist 1 second aparat, total seconds is equal to 1, but I want to have number of measures
  
  utils.logger("x_length_global:", x_length_global)
  if ceil(x_length_global) != x_length_global:
      utils.logger("something is wrong, total n of seconds is not integer! I will quit since I do not handle these.")
      quit()
  x_length_global = int(x_length_global)
  #with default dpi, the number of jsons in one json list (10799) results in 179900 width, when only 65536 is allowed. Since this is 3 hours, I divide it by 3 to make each for one hour
  dividor = 1800 # half an hour in seconds
  n_parts = ceil(((x_length_global - 1) / dividor))  # how many images is needed - one for each started half an hour. Half an hour becase rendering data for an hours does not work (corrupted image)
  
  utils.logger("n_parts:", n_parts)
  utils.logger("n files:", len(json_list_full_list))
  
  # sort so that we can easily calculate time differences
  json_list_full_list_sorted = sorted(json_list_full_list, key=lambda json_list_full: json_list_full[0]["datetimeISO8601"]) # sort by first entry time

  if len(json_list_full_list) > 1: # if more than one file path was given
    start_times = []
    for json_list_full in json_list_full_list_sorted:
      start_times.append(datetime.strptime(json_list_full[0]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp())

    range_differences = []
    for i in range(len(json_list_full_list_sorted) - 1, -1, -1): # from the last index to 0, backwards
      #utils.logger("i",i)
      if i == 0:
        range_differences.append(0)
        continue
      this_time = datetime.strptime(json_list_full_list_sorted[i][0]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()
      prv_time = datetime.strptime(json_list_full_list_sorted[i-1][0]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()
      #utils.logger(f"this time: {this_time}, prv_time: {prv_time}")
      range_difference = (datetime.fromtimestamp(this_time) - datetime.fromtimestamp(prv_time)).total_seconds() + 1 # +1 because if 2 measures exist 1 second aparat, total seconds is equal
      #utils.logger(f"range_difference: {range_difference}")
      range_differences.append(range_difference) 
    #utils.logger("range dif bf sort:",range_differences)
    range_differences = sorted(range_differences) 
    #utils.logger("after sort",range_differences)

  for i in range(n_parts):
    utils.logger("making part:", i+1)

    x_figSize = dividor//6 # x size should be 6 times smaller than amout of x data. This looks good for pdf/image.
    Plot, Axis = plt.subplots(figsize=(x_figSize, 6)) 
    plt.subplots_adjust(top=1)
    Axis.set_rasterized(True)

    labels_set = False
    for j, json_list_full in enumerate(json_list_full_list_sorted):
      y_speeds = []
      
      utils.logger("working on file:", j+1)
      utils.logger("len json list full sorted:", len(json_list_full_list_sorted))

      if len(json_list_full_list) > 1: # if more than one file path was given
        if j == 1 and index_of_the_later == 1 and first_time_here:
          range_start = 0 
          range_end = dividor - range_difference # range_end is not inclusive
          first_time_here = False
        elif j == 1 and index_of_the_later == 1 and not first_time_here:
          range_start = (dividor - range_difference) + dividor*(i-1)
          range_end = (dividor - range_difference) + dividor*i
        else:
          range_start = 0 + dividor * i # 
          range_end = dividor + dividor * i # range_end is not inclusive
      
      json_list_part = json_list_full[range_start : range_end]
      
      for entry in json_list_part:
        if "speed_kmh_haversine_math" in entry:
          if entry["speed_kmh_haversine_math"] == '':
            y_speeds.append(0)
          else:
            y_speeds.append(float(entry["speed_kmh_haversine_math"]))
        else:
          y_speeds.append(0)
      x_labels = [str(datetime.strptime(entry["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").time()) for entry in json_list_part]

      color_marker_map = {
        "dummy value": "pink",
        "[T->T->T...]": "black",
        "interpolated speed [T T->{F F F F T}-> T]": "orange",
        "average straight line displacement [{T->(F F F F)->T F}]": "red"
      }
      # map based on speed_source key, unles data is original, then "overwrite", so that we have color based on value source, not just the method it was connected with
      speed_sources = ["[T->T->T...]" if entry['original_data'] == True else entry['speed_source'] for entry in json_list_part]
      colors = [color_marker_map[source] for source in speed_sources]

      ax = plt.subplot()
      ax.plot(x_labels, y_speeds, color=_get_color[j], zorder=1)
      plt.scatter(x_labels, y_speeds, c=colors, s=4, marker=_get_marker[j], zorder=2)
      if not labels_set:
        x_shown_labels = ['' if i % 2 != 0 else str(x_labels[i]) for i in range(len(x_labels))]
        labels_set = True
      # Rotate the labels
      Axis.set_xticklabels(x_shown_labels, fontsize=7, rotation=90) 
      Axis.xaxis.set_tick_params(labelsize=8)
      Axis.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, labeltop=False, pad=5)
      Axis.grid(True, alpha=0.5)
      plt.ylim(-1, 75)

      for x, y in zip(x_labels, y_speeds):
          Axis.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 40+j*30), ha='center', fontsize=7, rotation=80, color = _get_color[j])
          Axis.plot([x, x], [y, y+8+j*6], color='pink', linewidth=0.5)  # Add a line pointing to the annotation
          Axis.annotate('', xy=(x, 0), xytext=(x, - 3), arrowprops={'arrowstyle': '-', 'color': _get_color[j], 'linewidth': 0.5})
      
      this_part_start_time = datetime.strptime(json_list_part[0]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp() # this should always be the same
      this_part_end_time = datetime.strptime(json_list_part[-1]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()
      if this_part_start_time < global_min_time:
        from_time = this_part_start_time
      if this_part_end_time > global_max_time:
        to_time = this_part_end_time
    from_time = datetime.fromtimestamp(from_time)
    to_time = datetime.fromtimestamp(to_time)
    from_time_formatted = f"{from_time.hour};{from_time.minute};{from_time.second}"
    to_time_formatted = f"{to_time.hour};{to_time.minute};{to_time.second}"
    plt.savefig(f"{constants.path_to_files_dir}{from_time_formatted} -- {to_time_formatted} --- {len(json_list_full_list)}files --- {constants.image_filename}")
    plt.close()

    # Display the plot
    #plt.show()
    
    utils.logger(f"finished saving speed graph image {i+1} of {n_parts}")