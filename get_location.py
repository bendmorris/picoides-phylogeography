# use GrADS to get temperature and NDVI data from NetCDF files
import os
import urllib
import cPickle as pickle
try: latlons = pickle.load(open('latlons.pkl'))
except: latlons = {}



def save_lat_lons():
    f = open("latlons.py", "w")
    f.write("latlons = %s" % latlons)
    f.close()


def get_lat_lon(location):
    if location in latlons.keys():
        return latlons[location]
    true = True
    false = False
    try:
        url = "http://maps.google.com/maps/api/geocode/json?address=%s&sensor=false" % location.replace(' ', '+')
        data = eval(urllib.urlopen(url).read())
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
        return None
