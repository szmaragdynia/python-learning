import math, numpy as np
from geopy import distance
from auxiliary.utils import logger
from auxiliary.constants import tab

# Todo: 
#   j+1 should be renamed to "2nd_after_last_true" or something
#   current_now and prev should be renamed appropriately in cases, so their names match the situation
#   calculate_speeds should be renamed to calculate_distance, since this is what it does exactly. It is speed only when calculated measure-by-measure.
#       However then multiplying by m/s->km/h coefficient should be moved to other place (since however it will work, it is not semantically correct to keep it in distance calculation)


# latitude and longitude are given each second (Be they fake or real)
earth_radius_my_location_meters = 6365816 # 49.5 latitude north
def _haversine(lat1, lon1, lat2, lon2, lib=math):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(lib.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = lib.sin(delta_lat / 2) ** 2 + lib.cos(lat1) * lib.cos(lat2) * lib.sin(delta_lon / 2) ** 2
    if (lib == np):
        c = 2 * lib.arctan2(lib.sqrt(a), lib.sqrt(1 - a))
    else:
        c = 2 * lib.atan2(lib.sqrt(a), lib.sqrt(1 - a))
    distance_m_speed = c * earth_radius_my_location_meters # this is at the same time speed in m/s, because measures are taken every second
    speed_kmh = distance_m_speed * 3.6 # 3.6 is coefficient for transforming from m/s to km/h
    
    return speed_kmh

def _flatCartesianPlane(lat1, lon1, lat2, lon2, lib=math):
    lat1, lon1, lat2, lon2 = map(lib.radians, [lat1, lon1, lat2, lon2])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    mean_lat = (lat1 + lat2)/2

    return earth_radius_my_location_meters * lib.sqrt(delta_lat**2 + (lib.cos(mean_lat)*delta_lon)**2) * 3.6 #coefficient m/s->km/h
    

    

def _calculate_speeds(lat1, lon1, lat2, lon2):
    return {
        "haversine_math": round(_haversine(lat1, lon1, lat2, lon2, lib=math), 1),
        "haversine_numpy": round(_haversine(lat1, lon1, lat2, lon2, lib=np), 1),
        "geopy_geodesic": round(distance.distance((lat1, lon1),(lat2, lon2)).meters * 3.6, 1),    #coefficient m/s->kmh/h
        "geopy_great_circle": round(distance.great_circle((lat1, lon1),(lat2, lon2), radius=earth_radius_my_location_meters/1000).meters * 3.6, 1),
        "flat_cartesian_plane_math": round(_flatCartesianPlane(lat1, lon1, lat2, lon2, lib=math), 1),
        "flat_cartesian_plane_numpy": round(_flatCartesianPlane(lat1, lon1, lat2, lon2, lib=np), 1)
    }

def calculateAndAssign(dictionaries_list):
    n_entries = len(dictionaries_list)

    speeds = _calculate_speeds(0, 0, 0, 0) # dummy value
    for key in speeds:
        dictionaries_list[0]['speed_kmh'+'_'+key] = speeds[key]
    dictionaries_list[0]['speed_source'] = "dummy value"

    i=1
    while i < n_entries: #iterate from 2nd because we append speed to second element from pair it was calculated from, and it is convenient in code to look bacwards
        logger(n_entries-1,"/",i, sep='')

        # we need to take care of fake (copied) values, because they make speed constant and just before real value - very large. 
        # we have 3 cases, depending on how True and False values arrange (False being copied True, thus not real measures)
            # 1: T T T T ... - in that case we just calculate distance between this and previous point (treating it as distance/s, since measures are taken every second) and append to this measure
            # 2: T T F F F F {T T} - in that case we have real speed before a sequence of False values after which there are two real values. This means we have real speed before and after sequence of fake values. In this case, we interpolate lineraly from one speed to the next, assiging the appropriate values to the fake measures.
            # 3: T T F F F F T F - in this case, we cannot interpolate 
        
        # Case 1
        if dictionaries_list[i]['original_data'] == True:
            latitude_now = dictionaries_list[i]['latitude_deg']
            longitude_now = dictionaries_list[i]['longitude_deg']
            
            latitude_prev = dictionaries_list[i-1]['latitude_deg']
            longitude_prev = dictionaries_list[i-1]['longitude_deg']
            
            speeds = _calculate_speeds(latitude_prev, longitude_prev, latitude_now, longitude_now)
            for key in speeds:
                dictionaries_list[i]['speed_kmh'+'_'+key] = speeds[key]
            dictionaries_list[i]['speed_source'] = "[T->T->T...]"
            logger("{0}[T->T->T...]".format(tab),stream="fileOnly")
            logger("{0}{1}".format(tab,dictionaries_list[i]['datetimeISO8601']),stream="fileOnly")
        
        # Case 2 or 3
        elif (dictionaries_list[i])['original_data'] == False:
            #search for first not-fake and determine number of fakes
            j = i
            while (dictionaries_list[j]['original_data'] == False):
                j += 1 
            # after 'while' loop, j is first not-fake
            # if second element after TRUE exists and if that element is also TRUE  [T T F F F F {T T}] 
            
            # Case 2
            if (j + 1 < n_entries-1 and dictionaries_list[j+1]['original_data'] == True):
                # calculate the speed for the second original_data=True basing on first and second original_data=True and insert it into second
                latitude_now = (dictionaries_list[j+1])['latitude_deg']
                longitude_now = (dictionaries_list[j+1])['longitude_deg']
                
                latitude_prev = (dictionaries_list[j])['latitude_deg']
                longitude_prev = (dictionaries_list[j])['longitude_deg']

                speeds = _calculate_speeds(latitude_prev, longitude_prev, latitude_now, longitude_now)
                for key in speeds:
                    dictionaries_list[j+1]['speed_kmh'+'_'+key] = speeds[key]
                (dictionaries_list[j+1])['speed_source'] = "[T->T->T...]"
                logger("{0}Once for {1}/{2}: [T->T->T...]".format(tab,n_entries,j+1),stream="fileOnly")
                logger("{0}{1}".format(tab,dictionaries_list[j+1]['datetimeISO8601']),stream="fileOnly")

                # now lets interpolate speed for all fake values and first true value
                number_of_fakes = j-i # because j points at first TRUE after last fake [which does not hold instantenous speed value], and i points at first fake [which does not hold instantenous speed value]
                magic_number = 2 # well...it just should be like that.
                speed_change_every_second = {}
                for key in speeds:
                    speed_change_every_second['speed_kmh'+'_'+key] = ((dictionaries_list[j+1])['speed_kmh'+'_'+key] - (dictionaries_list[i-1])['speed_kmh'+'_'+key])/(number_of_fakes+magic_number)
                # now insert interpolated speeds
                k=0
                # while the main iterator (i) is not yet the same as  look-ahead-iterator (j), which (j) points to first not fake, which needs interpolated speed as well
                while i <= j:
                    logger(n_entries-1,"/",i, sep='')
                    for key in speeds:
                        (dictionaries_list[i])['speed_kmh'+'_'+key] = round((dictionaries_list[i-1])['speed_kmh'+'_'+key] + speed_change_every_second['speed_kmh'+'_'+key])
                    (dictionaries_list[i])['speed_source'] = "interpolated speed [T T->{F F F F T}-> T]"
                    logger("{0}interpolated speed [T T->{{F F F F T}}-> T]".format(tab),stream="fileOnly")
                    logger("{0}{1}".format(tab,dictionaries_list[i]['datetimeISO8601']),stream="fileOnly")
                    i += 1
                i -= 1 #compensation - we incremented once too much and thanks to that quit 'while', but we want to increment into the next (first unchecked so far) element at the end of the main loop
            # if second element after FALSE is FALSE, despite first being TRUE [t f f f f {T f}]
            # then we dont have enough data points to calculate speed for "T", and simpliest thing we can do is to use average speed throughout the entire false-scope, basing on difference in coordinates between 2 real measures
            # in the future I could interpolate speeds more properly - that is: maybe look at previous true speed values and use them to calculate the speed that must had been kept over the distance that is 'fake'
            
            # Case 3
            elif (j + 1 < n_entries-1 and dictionaries_list[j+1]['original_data'] == False): 
                # j is still first not-fake
                # i is first fake
                # calculate the AVERAGE speed basing on STRAIGHT LINE DISPLACEMENT for each missing element, basing on pre-fake realvalue and on post-fake realvalue and insert it into proper place
                latitude_now = (dictionaries_list[j])['latitude_deg']
                longitude_now = (dictionaries_list[j])['longitude_deg']
                
                latitude_prev = (dictionaries_list[i-1])['latitude_deg']
                longitude_prev = (dictionaries_list[i-1])['longitude_deg']
                
                number_of_entries = j - i + 1 # because j points at first TRUE after last fake [which does not hold instantenous speed value], and i points at first fake [which does not 
                wrong_speeds = _calculate_speeds(latitude_prev, longitude_prev, latitude_now, longitude_now) #these are distances really, beware (it's todo)
                correct_speeds = {key: round(value/number_of_entries, 1) for key, value in wrong_speeds.items()}
                
                while i <= j:
                    logger(n_entries-1,"/",i, sep='')
                    for key in correct_speeds:
                        dictionaries_list[i]['speed_kmh'+'_'+key] = correct_speeds[key]
                    (dictionaries_list[i])['speed_source'] = "average straight line displacement [{T->(F F F F)->T F}]"
                    logger("{0}average straight line displacement [{{T->(F F F F)->T F}}]".format(tab),stream="fileOnly")
                    logger("{0}{1}".format(tab,dictionaries_list[i]['datetimeISO8601']),stream="fileOnly")
                    i += 1
                i -= 1 #compensation - we incremented once too much and thanks to that quit 'while', but we want to increment into the next (first unchecked so far) element 
            #else:
            #    logger("Error in speec calculation, index + 1 is longer than number of entries (probably). Program will now quit")
            #    quit()
        i += 1
    return dictionaries_list