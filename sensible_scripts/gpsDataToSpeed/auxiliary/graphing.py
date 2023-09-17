# Todo: change library!
  # "Just a quick note, depending on your exact use case, matplotlib may not be a great choice. It's oriented towards publication-quality figures, not real-time display."

import matplotlib.pyplot as plt
from auxiliary import utils
from auxiliary import constants
from datetime import datetime
import json
from math import ceil
import numpy as np

def _get_color(value):
  cmap = plt.get_cmap('viridis')
  if value == 1:
    return "blue"
  elif value == 2:
    return "green"
  else:
    return cmap(value)

_get_marker = {
    1: 'o',
    2: 'D',
    3: 'v',
    4: '^',
    5: '<',
    6: '>',
    7: '1',
    8: '2',
    9: '3',
    10: '4',
    11: 's',
    12: 'p',
    13: 'P',
    14: '*',
    15: 'h',
    16: 'H',
    17: '+',
    18: 'x',
    19: 'X',
    20: '.',
    21: 'd',
    22: '|',
    23: '_'
}

def save_speeds_graph(*paths_to_jsons):
  json_list_full_list = []
  for path, i in enumerate(paths_to_jsons):
    with open(path, 'r') as file:
      json_list_full_list[i] = json.load(file)

  # from given files, finding which one is the longest (should be the same, anyway... [in my case])
  index_max = np.argmax([len(json_list_full) for json_list_full in json_list_full_list])
  utils.logger("index max", index_max)
  #with default dpi, the number of jsons in one json list (10799) results in 179900 width, when only 65536 is allowed. Since this is 3 hours, I divide it by 3 to make each for one hour
  dividor = 1800 # half an hour in seconds
  n_parts = ceil((len(json_list_full_list[index_max]) / dividor))  # how many images is needed - one for each started half an hour. Half an hour becase rendering data for an hours does not work (corrupted image)

  json_list = []
  x_labels = [[]]
  x_shown_labels = [[]]
  y_speeds = [[]]
  for json_list_full, i in enumerate(json_list_full_list): # I know it's not pythonic, but I used that previously (due to need/lack of knowledge) and I want to be consistent here
    for i in range(n_parts):
      range_start = 0 + dividor * i # 
      range_end = dividor + dividor * i # range_end is not inclusive
      json_list[i] = json_list_full[range_start : range_end]
      for entry in json_list[i]:
        if "speed_kmh_haversine_math" in entry:
          if entry["speed_kmh_haversine_math"] == '':
            y_speeds[i].append(0)
          else:
            y_speeds[i].append(float(entry["speed_kmh_haversine_math"]))
        else:
          y_speeds[i].append(0)
        j+=1
      x_labels[i] = [str(datetime.strptime(entry["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").time()) for entry in json_list[i]]

      x_figSize = len(x_labels[i])//6 # x size should be 6 times smaller than amout of x data. This looks good for pdf/image.
      Plot, Axis = plt.subplots(figsize=(x_figSize, 6)) 
      plt.subplots_adjust(top=1)
      Axis.set_rasterized(True)
      
      color_marker_map = {
        "dummy value": "pink",
        "[T->T->T...]": "black",
        "interpolated speed [T T->{F F F F T}-> T]": "orange",
        "average straight line displacement [{T->(F F F F)->T F}]": "red"
      }
      # map based on speed_source key, unles data is original, then "overwrite", so that we have color based on value source, not just the method it was connected with
      speed_sources = ["[T->T->T...]" if entry['original_data'] == True else entry['speed_source'] for entry in json_list[i]]
      colors = [color_marker_map[source] for source in speed_sources]
      plt.plot(x_labels[i], y_speeds[i], color=_get_color(i), zorder=1)
      plt.scatter(x_labels[i], y_speeds[i], c=colors, s=4, marker=_get_marker[i], zorder=2)

    


      # ----------------- todo -------------- i should show, just in case, labels from other files! below them!
       
      x_shown_labels[i] = ['' if i % 2 != 0 else str(x_labels[i][j]) for j in range(len(x_labels[i]))]
      # Rotate the labels
      Axis.set_xticklabels(x_shown_labels[i], fontsize=7, rotation=60, va='top') 
      Axis.xaxis.set_tick_params(labelsize=8)

      Axis.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, labeltop=False, pad=5)

      # moving x-labels slightly to the left, because due to rotation, they look misplaced
      x_positions = Axis.get_xticks() - 0.2  
      Axis.set_xticks(x_positions)


      Axis.grid(True, alpha=0.5)

      plt.ylim(-1, 75)

      for x, y in zip(x_labels[i], y_speeds[i]):
          Axis.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 40), ha='center', fontsize=7, rotation=80)
          Axis.plot([x, x], [y, y+8], color='pink', linewidth=0.5)  # Add a line pointing to the annotation
          Axis.annotate('', xy=(x, 0), xytext=(x, - 3), arrowprops={'arrowstyle': '-', 'color': 'pink', 'linewidth': 0.5})

    #--------------------------------- FINISHED HERE, REALIZING IT';S ALLL WRONG BECAUSE STARTING TIMES ARE DIFFERENT XDD=--================================
      from_time = datetime.strptime(json_list_full[range_start]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z")
      from_time_formatted = f"{from_time.hour};{from_time.minute};{from_time.second}"
      to_time = datetime.strptime(json_list_full[range_end-1]["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z")
      to_time_formatted = f"{to_time.hour};{to_time.minute};{to_time.second}"


    plt.savefig(f"{constants.path_to_files_dir}{from_time_formatted} -- {to_time_formatted} --- {constants.image_filename}")
    plt.close()

    # Display the plot
    #plt.show()
    
    utils.logger(f"finished saving speed graph image {i+1} of {n_parts}")

