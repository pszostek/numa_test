#!/usr/bin/env python

#from pylab import figure, grid, imshow, show, colorbar
from matplotlib.pyplot import figure, grid, imshow, show, colorbar
import matplotlib.pyplot as plt
from numpy import array
from matplotlib import colors
from collections import defaultdict
import sys

VMIN = 40
VMAX = 120

def get_bandwidth_from_csv(csv_path):
    times = defaultdict(dict)
    csv_lines = open(csv_path, 'r').readlines()
    for line in csv_lines:
        line = line.strip()
        parts = line.split(',')
        from_core = int(parts[0])
        to_core = int(parts[1])
        time = float(parts[2])
        times[from_core][to_core] = 120/(time/1000)
    return times

times = get_bandwidth_from_csv(sys.argv[1])
nr_cores = len(times[0])
times_array = array([times[core_from].values() for core_from in sorted(times.keys())])
norm = colors.Normalize(vmin=VMIN, vmax=VMAX)
im = plt.imshow(times_array, interpolation='nearest', norm=norm, cmap="hot")
#grid(True)
cb = colorbar(im)

cb.set_label("Bandwidth GB/s")

show()
