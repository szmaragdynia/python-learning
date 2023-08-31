import gpxpy
from auxiliary.constants import tab, path_to_files_dir, gpx_filename

with open(path_to_files_dir + gpx_filename, 'r') as gpx_file:       # this is executed at module import!
    gpx = gpxpy.parse(gpx_file)

def makeDictFromGpx(range):
  s = slice(range)
  measures_list = []
  for track in gpx.tracks[:1]:                                        # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
      for segment in track.segments[:1]: # same as above
          for point in segment.points[s]:                                # --------- HERE CHANGE THE RANGE
              measures_list.append({
                              "original_data": True, 
                              "latitude_deg": point.latitude,
                              "longitude_deg": point.longitude,
                              "elevation_m": point.elevation,
                              "datetimeISO8601": point.time.isoformat(),
                              })
  return measures_list