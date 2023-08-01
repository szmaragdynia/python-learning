# checking this: https://stackoverflow.com/questions/45840118/how-do-i-calculate-speed-from-a-gpx-file-if-the-speed-tag-itself-is-not-given
# comparing with: https://www.omnicalculator.com/other/latitude-longitude-distance
# my original results from harvesine are in accordance with the 'omni'.

import numpy as np
from math import radians, sin, cos, sqrt, atan2
from haversine import haversine, Unit

# kuba, dla T08:36:31
latitude1 =49.565153
longitude1=20.628623

# kuba, dla T08:36:32
latitude2=49.565198
longitude2=20.628551
# #================================
# # ja, dla T08:36:31
latitude1 =49.565363
longitude1=20.628278

# # ja, dla T08:36:32
latitude2=49.565394
longitude2=20.62823

# r = 6371000 # radius of the Earth in meters
# theta1 = np.deg2rad(longitude1)
# phi1 = np.deg2rad(latitude1)
# x1 = r*np.cos(theta1)*np.sin(phi1)
# y1 = r*np.sin(theta1)*np.sin(phi1)
# z1 = r*np.cos(phi1)

# theta2 = np.deg2rad(longitude2)
# phi2 = np.deg2rad(latitude2)
# x2 = r*np.cos(theta2)*np.sin(phi2)
# y2 = r*np.sin(theta2)*np.sin(phi2)
# z2 = r*np.cos(phi2)

# distance= np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

# print("distance",distance)

# centralangle= np.arccos((x1*x2 + y1*y2 + z1*z2)/r**2)
# arclength = centralangle*r
# print("arclength",arclength)

# ------------


#for whatever reaseon the formula below does not work anymore, but that file is for experimenting, and I already have well-formatted files anyway. todo: replace hand-written formula with the one from library.
# Haversine formula
lat1, lon1, lat2, lon2 = map(radians, [latitude1, longitude1, latitude2, longitude1])

dlat = lat2 - lat1
dlon = lon2 - lon1
a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
c = 2 * atan2(sqrt(a), sqrt(1 - a))
r = 6371000 # Radius of the Earth in meters
#c*r is distance in meters, and it also is speed in meters/second because the values are measured one second apart
x=c*r
print ("haversince distance:",x)
print ("speed km/h",round((c * r * 3.6),1))

#----------------
print ("haversine lib, dist in meters:",haversine((latitude1, longitude1), (latitude2, longitude2),unit=Unit.METERS))
print ("haversine lib, speed km/h:",round(haversine((latitude1, longitude1), (latitude2, longitude2),unit=Unit.METERS)*3.6,1))


