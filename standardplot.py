

import matplotlib.pyplot as mplt
import numpy as nmp

x = nmp.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
mplt.plot(x, nmp.sin(x))       # Plot the sine of each x point
mplt.show()                   # Display the plot