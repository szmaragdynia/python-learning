# this code is a result of me using chatGPT heavily, this shouldn't be considered my job so far - I have not yet had time to understand the library well enough to consider that code "mine"



# Todo: change library!
# "Just a quick note, depending on your exact use case, matplotlib may not be a great choice. It's oriented towards publication-quality figures, not real-time display."





import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
from auxiliary import utils
from auxiliary import constants
from datetime import datetime
import matplotlib.style as mplstyle
mplstyle.use('fast')

mycalc_data = [] # my speed calculation
gpseditor_populated_data = [] #gps track editor speed calculation, basing on original data without duplicates and with populated fake measures
utils.readCsv(mycalc_data, constants.output_filename_step4_csv)
utils.readCsv(gpseditor_populated_data, "output_gpx_3no-missing-values.csv")

# I am not importing time from gps track editor, because it did not export seconds. I hope that program have not messed up times or inserted measures etc.
# row is a dictionary, mycalc_data is a list of dictionaries
x_labels = [str(datetime.strptime(row["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").time()) for row in mycalc_data]
x_values = [str(datetime.strptime(row["datetimeISO8601"],"%Y-%m-%dT%H:%M:%S%z").timestamp()) for row in mycalc_data]
mycalc_values = []

for row in mycalc_data:
  if row["speed_kmh_haversine_math"] == '':
    mycalc_values.append(0)
  else:
    mycalc_values.append(float(row["speed_kmh_haversine_math"]))

gpseditor_populated_values = []
for row in gpseditor_populated_data:
  if row["Speed (km/h)"] == '':
    gpseditor_populated_values.append(0)
  else:
    gpseditor_populated_values.append(float(row["Speed (km/h)"]))

# use different backend
plt.switch_backend('Qt5Agg')

# Create the main figure
fig = plt.figure()
ax = fig.subplots()
plt.subplots_adjust(bottom=0.30)

num_points_to_display = 120 # Set the number of points to display at once

# Create a slider for horizontal scrolling
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03]) #xposition, yposition, width, height
slider = RangeSlider(ax_slider, 'Data Range', 0, len(mycalc_data), valinit=(0, 10))

def update(val):
  start_index = int(val[0])
  end_index = int(val[1])
  x_plot = x_values[start_index:end_index]
  y_plot = mycalc_values[start_index:end_index]
  ax.clear()
  ax.plot(x_plot, y_plot, color="blue", marker="o", markerfacecolor="red", markeredgecolor="red", markersize=1, label="Speed")

  # # This sets the x-axis ticks to the values in x_values, indicating that ticks should be displayed at those positions.
  ax.set_xticks(x_plot, minor=True)  # Show minor ticks for every value

  x_shown_labels = ['' if i % 5 != 0 else str(x_labels[i]) for i in range(len(x_labels))]

  # # Rotate the labels
  ax.set_xticklabels(x_shown_labels, rotation=60) 

  ax.xaxis.set_tick_params(labelsize=8)

  ax.grid(True, alpha=0.5)
  fig.canvas.draw_idle()



slider.on_changed(update)
init = 0,10
update(init)
# Show the plot
plt.show()