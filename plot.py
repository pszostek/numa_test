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

files = ["e5-2699v3_cod_on.csv",
         "e5-2699v3_cod_off.csv",
         "e5-2697v3_cod_on.csv",
         "e5-2697v3_cod_off.csv",
         "e5-2695v2_numa_on.csv",
         "e5-2695v2_numa_off.csv",
         "e5-2690_numa_on.csv",
         "e5-2690_numa_off.csv"]
plt.close('all')

def decrypt_filename(filename):
    parts = filename.split('.')
    experiment = parts[0]
    experiment = experiment.replace('_', ' ')
    return experiment

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

fig, axarr = plt.subplots(len(files)/2, 2)
for file_idx, filename in enumerate(files):
    subplot = axarr[file_idx/2, file_idx%2]
    times = get_bandwidth_from_csv(filename)
    nr_cores = len(times[0])
    times_array = array([times[core_from].values() for core_from in sorted(times.keys())])
    norm = colors.Normalize(vmin=VMIN, vmax=VMAX)
    im = subplot.imshow(times_array, interpolation='nearest', norm=norm, cmap="hot")
    #grid(True)
    subplot.set_title(decrypt_filename(filename))
    subplot.set_xlabel('destination core')
    subplot.set_ylabel('source core')
#colorbar()

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cb = fig.colorbar(im, cax=cbar_ax)
cb.set_label("Bandwidth GB/s")

show()
