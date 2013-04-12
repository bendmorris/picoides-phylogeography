from get_location import get_lat_lon
import csv
import cPickle as pkl
import scipy.stats as s
with open('data/accessions.pkl') as pkl_file:
    accessions = pkl.load(pkl_file)
    
body_size_data = [
    (48, 76.59, 2.32),
    (45, 78.80, 4.28),
    (41, 73.73, 4.05),
    (38, 67.61, 2.79),
    (31, 58.75, 2.66),
    (17, 47.14, 3.26),
]
lats, means, sds = [[p[n] for p in body_size_data] for n in range(3)]
mean_m, mean_b, r, p, se = s.linregress(lats, means)
sd_m, sd_b, r, p, se = s.linregress(lats, sds)
    
with open('data/samples.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(('id','species','location','lat','lon','body_size'))
    for key, value in accessions.items():
        accession, (location, species) = key, value
        species = species.strip()
        location = location.replace('.', ', ')
        row = (accession, species, location)
        try:
            lat1, lon1, lat2, lon2 = get_lat_lon(location)
        except: continue
        lat = round((lat1+lat2)/2, 2)
        lon = round((lon1+lon2)/2, 2)
        
        size = round(s.norm.rvs(mean_b + mean_m*lat, sd_b + sd_m*lat), 2)
        
        row += (lat, lon, size)
        
        writer.writerow(row)
