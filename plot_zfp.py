import sys
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import os

#plt.ioff()

# static parameters
INPUT_DIR = "/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/"
OUTPUT_DIR = "/zfs/fthpc/plascomcm/inputs/pavlo_runs/Compressor Plots/"

CompressorNames = {"sz1.3":"SZ 1.3","sz1.4.9":"SZ 1.4.9 Beta",
"sz1.4.11":"SZ 1.4.11", "sz2.0": "SZ 2.0", 
"zfp-0.5.1":"ZFP 0.5.1"}
CVNames = ["Compression Factor", "Compression Time", "Compression Time STDDEV", "Decompression Time", "Decompression Time STDDEV"]

numPoints = 5000
numGrids = 2
numVals = 5
numCVs = 5


# get arguments
if len(sys.argv) != 4:
	printf("USAGE python plot_stats.py compressor tolerance iterations")
	sys.exit()

COMPRESSOR = sys.argv[1]
TOLERANCE = sys.argv[2]
ITERATIONS = sys.argv[3]

# set filenames
input_file = INPUT_DIR + TOLERANCE + "/" + COMPRESSOR + "/" +ITERATIONS + ".npy"


#set seaborn plotting options
sns.set()
sns.set_style({'axes.grid' : True, 'legend.frameon':True})
#sns.set_style("whitegrid", {'axes.grid' : True, 'legend.frameon':True})
sns.set_color_codes()
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 0.5, 'lines.markeredgewidth': 2., 'lines.markersize': 5})

#set matplotlib plotting options
colors = ["b", "g", "r", "y", "y"]
font = {'family' : 'serif',
        #'weight' : 'bold',
        #'size'   : 14
        }
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True


'''
avg = [[[[ np.mean(val) for val in grid ] for grid in compressor ] for compressor in cv ] for cv in CompressionValues]
std = [[[[ np.std(val) for val in grid ] for grid in compressor ] for compressor in cv ] for cv in CompressionValues]
var = [[[[ np.var(val) for val in grid ] for grid in compressor ] for compressor in cv ] for cv in CompressionValues]

for cv in xrange(numCVs):
  for compressor in xrange(numCompressors):
    for grid in xrange(numGrids):
      for val in xrange(numVals):
        print(CVNames[cv]+" "+CompressorNames[compressor]+" Grid "+str(grid)+" Val "+str(val)+" Average: "+str(avg[cv][compressor][grid][val]))
        print(CVNames[cv]+" "+CompressorNames[compressor]+" Grid "+str(grid)+" Val "+str(val)+" Standard Deviation: "+str(std[cv][compressor][grid][val]))
        print(CVNames[cv]+" "+CompressorNames[compressor]+" Grid "+str(grid)+" Val "+str(val)+" Variance: "+str(var[cv][compressor][grid][val]))
'''
labels = ["density", r"$x$-momenta", r"$y$-momenta", r"$z$-momenta", "energy", "pressure"]


def plot(CompressionValues, cv, compressor, grid, tolerance):
	 
  xvals = [x for x in range(numPoints)]
  ysets = CompressionValues[cv][grid]
	
  title = CompressorNames[compressor]+" "+tolerance+" Grid "+str(grid)
  ylabel = CVNames[cv] 
  output_file = OUTPUT_DIR + title + " " + CVNames[cv] + '.png'
	
  for val in xrange(numVals):
    if val != 3:
      plt.plot(xvals, ysets[val], color=colors[val], label=labels[val])

   
  if cv == 1 or  cv == 3:
    ylabel += " (s)"
    ystds = CompressionValues[cv+1][grid]
    for val in xrange(numVals):
      if val != 3:
        upper = [ y + std for y, std in zip(ysets[val], ystds[val]) ]
        lower = [ y - std for y, std in zip(ysets[val], ystds[val]) ]
        plt.fill_between(xvals, upper, lower, color=colors[val], alpha = .3) 

  plt.semilogy() 
  plt.xlim(0, numPoints)
  plt.title(title)
  plt.ylabel(ylabel, weight='bold')
  plt.xlabel("Time-step", weight='bold')
  plt.legend(loc='upper center', frameon=True, ncol=2, fontsize=12)
  plt.tight_layout()

  #I save the figures rather than showing them, replace the bottom 2 lines with the third to show each figure
  plt.savefig(output_file)
  plt.gcf().clear()
  #plt.show()


# create plots for compressor & tolerance
CompressionValues = np.load(input_file)
for cv in [0,1,3]:
	for grid in xrange(numGrids):
		plot(CompressionValues, cv, COMPRESSOR, grid, TOLERANCE)


