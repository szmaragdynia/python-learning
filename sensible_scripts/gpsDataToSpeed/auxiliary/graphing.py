# offset x labels to the left
# make it so that I can plot several things
  # beware of time! time must be in right place


import matplotlib.pyplot as plt
from auxiliary import utils
from auxiliary import constants
from datetime import datetime
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
    #x_values = [str(datetime.strptime(row["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()) for row in mycalc_data]

    #utils.logger("len x labels:", len(x_labels))
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

    #col = np.where([entry['speed_source'] for entry in json_list] == "interpolated speed [T T->{F F F F T}-> T]", "black","red")
    #plt.plot(x_labels, y_speeds, color="blue", marker="o", markerfacecolor=col, markeredgecolor="red", markersize=1, label="Speed")
    plt.plot(x_labels, y_speeds, color="blue", zorder=1)
    plt.scatter(x_labels, y_speeds, c=colors, s=4, marker="o", zorder=2)
    #plt.plot(x_labels[20:], y_speeds[20:], color="blue", marker="o", markerfacecolor="yellow", markeredgecolor="yellow", markersize=1, label="Speed")
    #fig.set_xticks(x_labels, minor=True)  # Show minor ticks for every value
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

