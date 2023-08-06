# this file shall merge (or improve and merge) previous approaches, and be used as one standalone script,without demanding from user any previous action on the gpx files

# perhaps should have used virtual environment
import pandas as pd
import gpxpy
import gpxpy.gpx
import re

path_to_file_dir=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja"
input_filename = "\kubaORG.gpx"

# -------------------------------------------- reading and parsing gpx for further use --------------------------------------------
gpx_file = open(path_to_file_dir+input_filename, 'r')
gpx = gpxpy.parse(gpx_file)

latitude_deg = []
longitude_deg = []
elevation_m = []
timeISO8601 = []
for track in gpx.tracks[:1]: # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
    for segment in track.segments[:1]: # same as above
        for point in segment.points[:30]:
            latitude_deg.append(point.latitude)
            longitude_deg.append(point.longitude)
            elevation_m.append(point.elevation)
            timeISO8601.append(point.time)

df = pd.DataFrame(
    {
        "real values": True,
        "latitude_deg": pd.Series(latitude_deg),
        "longitude_deg": pd.Series(longitude_deg),
        "elevation_m": pd.Series(elevation_m),
        "timeISO8601": pd.Series(timeISO8601),
    }
)

#swap regex for the below 
#def get_file_ext(filename):
#   return filename[filename.index(".") + 1:]

output_filename = re.sub("\..*$", "_dataFromGpx.csv", input_filename) # this catches what I want, but also probably catches what I would not want - irrelevant for now.
df.to_csv(path_to_file_dir+output_filename,index=False)

#check for doubles (zepp life have doubles, one without elevation)
#check for missing


# dataframe into csv (for comfortable peek inside)
# csv into json (for my needs)