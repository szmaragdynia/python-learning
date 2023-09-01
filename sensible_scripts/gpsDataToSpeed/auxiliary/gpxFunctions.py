import gpxpy
from auxiliary.constants import tab, path_to_files_dir, gpx_filename

with open(path_to_files_dir + gpx_filename, 'r') as gpx_file:       # this is executed at module import!
    gpx = gpxpy.parse(gpx_file)

def makeDictFromGpx(range=None):
    measures_list = []
    for track in gpx.tracks[:1]:                                        # we have only one, thus omitting rest of cases so that we don't bother in the future with undefined behaviour in case I forget about that assumption (I won't process data from another tracks, becasue I do not know nor need to know now about how that exactly works)
        for segment in track.segments[:1]: # same as above
            if range == None:
                for point in segment.points:                                
                    measures_list.append({
                                    "original_data": True, 
                                    "latitude_deg": point.latitude,
                                    "longitude_deg": point.longitude,
                                    "elevation_m": point.elevation,
                                    "datetimeISO8601": point.time.isoformat(),
                                    })
            else:
                s = slice(range)
                for point in segment.points[s]:                                
                    measures_list.append({
                                    "original_data": True, 
                                    "latitude_deg": point.latitude,
                                    "longitude_deg": point.longitude,
                                    "elevation_m": point.elevation,
                                    "datetimeISO8601": point.time.isoformat(),
                                    })

        
    return measures_list
