# use GrADS to get temperature and NDVI data from NetCDF files
import os
import urllib
import cPickle as pickle
import json
import time

last_read = time.time()

try:
    with open('latlons.pkl') as pkl_file:
        latlons = pickle.load(pkl_file)
except: latlons = {}



def save_lat_lons():
    with open('latlons.pkl', 'w') as pkl_file:
        pickle.dump(latlons, pkl_file, -1)


def get_lat_lon(location, throttle=0.5):
    global last_read

    if location in latlons.keys():
        return latlons[location]

    while time.time() - last_read < throttle:
        pass
    last_read = time.time()

    try:
        url = "http://maps.google.com/maps/api/geocode/json?address=%s&sensor=false" % location.replace(' ', '+')
        data = json.loads(urllib.urlopen(url).read())
        if data['status'] == 'OVER_QUERY_LIMIT':
            raise Exception('Google Maps API query limit exceeded. (Use the throttle keyword to control the request rate.')
            
        try:
            bounds = data['results'][0]['geometry']['bounds']
            result1 = bounds['northeast']
            lat1, lon1 = result1['lat'], result1['lng']
            result2 = bounds['southwest']
            lat2, lon2 = result2['lat'], result2['lng']        
        except KeyError:
            bounds = data['results'][0]['geometry']['location']
            lat1 = bounds['lat']
            lon1 = bounds['lng']
            lat2 = lat1
            lon2 = lon1
        lat1, lon1, lat2, lon2 = (round(lat1, 2), round(lon1, 2), round(lat2, 2), round(lon2, 2))
        latlons[location] = (lat1, lon1, lat2, lon2)
        save_lat_lons()
        return (lat1, lon1, lat2, lon2)
        
    except Exception as e:
        raise
        return None
