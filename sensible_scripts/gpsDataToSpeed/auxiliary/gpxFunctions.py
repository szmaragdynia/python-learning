import gpxpy
from datetime import datetime
from auxiliary.constants import tab, path_to_files_dir, gpx_filename
from auxiliary.utils import logger

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

def _createGPX(measures_list):
    gpx_out = gpxpy.gpx.GPX()
    
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_out.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for measure in measures_list:
        time = datetime.fromisoformat(measure["datetimeISO8601"])
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(measure["latitude_deg"], measure["longitude_deg"], elevation=measure["elevation_m"], time=time))
    return gpx_out

def saveDictToGPX(measures_list, gpx_output_filename):
    gpx = _createGPX(measures_list)
    logger("Created GPX.")
    with open(path_to_files_dir + gpx_output_filename, 'w') as f: 
        f.write( gpx.to_xml())
