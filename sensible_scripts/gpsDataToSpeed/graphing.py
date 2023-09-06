# this code is a result of me using chatGPT heavily, this shouldn't be considered my job so far - I have not yet had time to understand the library well enough to consider that code "mine"

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from auxiliary import utils
from auxiliary import constants
from datetime import datetime
mycalc_data = [] # my speed calculation
gpseditor_populated_data = [] #gps track editor speed calculation, basing on original data without duplicates and with populated fake measures

utils.readCsv(mycalc_data, constants.output_filename_step4_csv)
utils.readCsv(gpseditor_populated_data, "output_gpx_3no-missing-values.csv")


# I am not importing time from gps track editor, because it did not export seconds. I hope that program have not messed up times or inserted measures etc.
# row is a dictionary, mycalc_data is a list of dictionaries
x_labels = [str(datetime.strptime(row["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").time()) for row in mycalc_data]
mycalc_values = []
str
for row in mycalc_data:
  if row["speed_kmh_haversine_math"] == '':
    mycalc_values.append(0)
  else:
    mycalc_values.append(float(row["speed_kmh_haversine_math"]))

# gpseditor_populated_values = []
# for row in gpseditor_populated_data:
#   if row["Speed (km/h)"] == '':
#     gpseditor_populated_values.append(0)
#   else:
#     gpseditor_populated_values.append(float(row["Speed (km/h)"]))

  
#plt.scatter(x_labels, mycalc_values, label="Speed-mycalc", c="blue", marker="o")
#plt.scatter(x_labels, gpseditor_populated_values, label="Speed-populated-trackeditor", c="red", marker="D")


# plt.xlabel("DateTime")
# plt.ylabel("Speed km/h")
# plt.legend()

# plt.show()

def update(val):
  start_index = int(slider.val)
  end_index = start_index + num_points_to_display
  x_values = x_labels[start_index:end_index]
  y_values = mycalc_values[start_index:end_index]
  ax.clear()
  ax.scatter(x_values, y_values, label='Speed', c='blue', marker='o')
  #ax.legend()

  # Set new x-axis tick positions for every value
  ax.set_xticks(x_values, minor=True)  # Show minor ticks for every value

  # Set x-axis tick labels only for every 15th tick
  x_shown_labels = ['' if i % 15 != 0 else str(x_values[i]) for i in range(len(x_values))]
  ax.set_xticklabels(x_shown_labels, rotation=45)  # Rotate the labels by 90 degrees

  # Keep y-axis limits fixed
  ax.set_ylim(0, 80)
  ax.autoscale(enable=False, axis='y')
  
  # Update y-axis tick labels with both fixed values and current data values
  y_ticks = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80]  # Adjust these to your desired fixed values
  y_values_displayed = y_values[:5]  # Display up to 5 y-values for context
  y_tick_labels = [str(val) for val in y_ticks + y_values_displayed]
  ax.set_yticks(y_ticks + y_values_displayed)
  ax.set_yticklabels(y_tick_labels)

  ax.grid(True, alpha=0.5)
  
  fig.canvas.draw_idle()


# Create the main figure
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.30)

# Set the number of points to display at once
num_points_to_display = 30

# Create a slider for horizontal scrolling
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Data Range', 0, len(mycalc_data) - num_points_to_display, valinit=0, valstep=1)
slider.on_changed(update)


# Initial plot display
update(0)

# Show the plot
plt.show()



'''
'o': Circle marker
's': Square marker
'D': Diamond marker
'^': Upward-pointing triangle marker
'v': Downward-pointing triangle marker
'>': Right-pointing triangle marker
'<': Left-pointing triangle marker
'p': Pentagram marker
'h': Hexagon marker
'+': Plus marker
'*': Asterisk marker
'x': Cross marker
'''