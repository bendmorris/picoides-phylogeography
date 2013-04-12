import csv
import sys
from get_location import get_lat_lon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import csv


xs, ys, zs = [], [], []
with open('data/samples.csv') as input_file:
    reader = csv.reader(input_file)
    next(reader)
    for line in reader:
        y, x, size = [float(n) for n in line[3:6]]
        xs.append(x)
        ys.append(y)
        zs.append(size)


#zs = np.array(zs)
#zs /= max(zs)

plt.figure()

min_lon, max_lon = min(xs)-2, max(xs)+2
min_lat, max_lat = min(ys)-2, max(ys)+2

m = Basemap(projection='cyl',llcrnrlat=min_lat,urcrnrlat=max_lat,
            llcrnrlon=min_lon,urcrnrlon=max_lon,resolution='l')
m.drawmapboundary(linewidth=0.25)
m.drawcoastlines(color='#6D5F47', linewidth=.1)
m.drawcountries(color='#6D5F47', linewidth=.1)

m.scatter(xs, ys, c=zs, s=5, marker='+')
plt.colorbar()

if len(sys.argv) > 1: plt.savefig(sys.argv[1])
else: plt.show()
