import pandas as pd
import gpxpy
import gpxpy.gpx


path_to_file=  r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja"
filename = "\kubaORG.gpx"

# test_excel = pd.read_xml(r"E:\NOWE SERCE ŻYCIA\Menu życia\F Outdoorsy\zepp life i strava do after effects\kuby\podejscie 2 full automacja\kubaORG.gpx")
# test_excel.heaD

gpx_file = open(path_to_file+filename, 'r')
gpx = gpxpy.parse(gpx_file)

latitude_deg = []
longitude_deg = []
elevation_m = []
timeISO8601 = []


for track in gpx.tracks[:1]: # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forgot
    for segment in track.segments[:1]: # same as above
        for point in segment.points[:3]:
            latitude_deg.append(point.latitude)
            longitude_deg.append(point.longitude)
            elevation_m.append(point.elevation)
            timeISO8601.append(point.time)


# this into dataframe
# dataframe into csv (for comfortable peek inside)
# csv into json (for my needs)

s1 = pd.Series([1,2,3,4])
s2 = pd.Series(['a','b','c','d'])
df = pd.DataFrame(
    {
        "Cyferki": s1,
        "Literki": s2,
    }
)
print(df)