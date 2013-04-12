import csv
import sys
from get_location import get_lat_lon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import cPickle as pkl
with open('data/clusters.pkl') as pkl_file:
    clusters = pkl.load(pkl_file)


xs, ys, zs = [], [], []
colors = ['grey',
          'red','blue','yellow','green','orange','purple','black','cyan',
          'indigo','brown','tan','violet','teal','red','blue','yellow','green']
with open('data/samples.csv') as input_file:
    reader = csv.reader(input_file)
    next(reader)
    for line in reader:
        accession = line[0]
        try: cluster_number = clusters[accession]
        except: continue#cluster_number = 0
        y, x = [float(n) for n in line[3:5]]
        xs.append(x-(random.random()-0.5)/10)
        ys.append(y-(random.random()-0.5)/10)
        zs.append(colors[cluster_number-1])


plt.figure(dpi=500)

min_lon, max_lon = min(xs)-2, max(xs)+2
min_lat, max_lat = min(ys)-2, max(ys)+2

m = Basemap(projection='cyl',llcrnrlat=min_lat,urcrnrlat=max_lat,
            llcrnrlon=min_lon,urcrnrlon=max_lon,resolution='l')
m.drawmapboundary(linewidth=0.25)
m.drawcoastlines(color='#6D5F47', linewidth=.1)
m.drawcountries(color='#6D5F47', linewidth=.1)

m.scatter(xs, ys, color=zs, s=5, marker='+')

if len(sys.argv) > 1: plt.savefig(sys.argv[1])
else: plt.show()
