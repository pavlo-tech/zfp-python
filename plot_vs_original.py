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
OUTPUT_DIR = "/zfs/fthpc/plascomcm/inputs/pavlo_runs/Compressor Plots/plot_v_original_averaged/"

#CompressorNames = {"sz1.3":"SZ 1.3", "sz1.4.9":"SZ 1.4.9 Beta", "sz1.4.11":"SZ 1.4.11", "sz2.0": "SZ 2.0"}
CompressorNames = {"zfp-0.4.1":"ZFP 0.4.1", "zfp-0.5.1":"ZFP 0.5.1", "zfp-0.5.4": "ZFP 0.5.4"}
CVNames = ["Compression Factor", "Compression Time", "Compression Time STDDEV", "Decompression Time", "Decompression Time STDDEV"]

numPoints = 5000
numGrids = 2
numVals = 5
numCVs = 5

'''''
# get arguments
if len(sys.argv) != 3:
	printf("USAGE python plot_stats.py compressor iterations")
	sys.exit()

COMPRESSOR = sys.argv[1]
TOLERANCE = sys.argv[2]
ITERATIONS = sys.argv[3]


# set filenames
input_file = INPUT_DIR + TOLERANCE + "/" + COMPRESSOR + "/" +ITERATIONS + ".npy"
'''''

#set seaborn plotting options
sns.set()
sns.set_style({'axes.grid' : True, 'legend.frameon':True})
#sns.set_style("whitegrid", {'axes.grid' : True, 'legend.frameon':True})
sns.set_color_codes()
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 0.5, 'lines.markeredgewidth': 2., 'lines.markersize': 5})

#set matplotlib plotting options
colors = ["b", "g", "r", "y", "y"]
lines = ['-', '--', '-.', ':', '-']
font = {'family' : 'serif',
        #'weight' : 'bold',
        #'size'   : 14
        }
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True


labels = ["density", r"$x$-momenta", r"$y$-momenta", r"$z$-momenta", "energy", "pressure"]

def get_average(compressor, tolerance):
	fname = INPUT_DIR + tolerance + "/"+compressor+"/1000.npy"
	nparr = np.load(fname)
	# double check this: I think it is correct
	#return np.average(nparr,(1,2))
	return np.average(np.delete(nparr,3,2),(1,2))

def plot_v_original(compressors, tolerances, metric):

	xvals = [x * 20 for x in range(numPoints)]	

	if metric == 0:
		title = "ZFP "+CVNames[metric]+" Gain"
		ylabel = "Compression Factor Gain as of ZFP 0.4.1"
		plt.fill_between(xvals, [5 for x in xvals], [1 for x in xvals], color="g", alpha = .3)
		plt.fill_between(xvals, [1 for x in xvals], [0 for x in xvals], color="r", alpha = .3)
	else:
		title = CVNames[metric] + " Speedup"
		ylabel = CVNames[metric] + " Speedup as of ZFP 0.4.1 "
		plt.fill_between(xvals, [5 for x in xvals], [1 for x in xvals], color="g", alpha = .3)
		plt.fill_between(xvals, [1 for x in xvals], [0 for x in xvals], color="r", alpha = .3)
	
	output_file = OUTPUT_DIR + title + " " + CVNames[metric] + '.png'

	# generate all plotlines	
	for c,compressor in enumerate(compressors):
		for t, tolerance in enumerate(tolerances):

			other_y = get_average(compressor, tolerance)[metric]
			original_y = get_average("zfp-0.4.1", tolerance)[metric]

			if metric == 0:
				yvals = [o / s if s != 0 else 0 for s,o in zip(original_y, other_y)]
			else:
				yvals = [s / o if o != 0 else 0 for s,o in zip(original_y, other_y)]

			myLabel= CompressorNames[compressor] + " " + tolerance
			plt.plot(xvals, yvals, color=colors[c], linestyle=lines[t], label=myLabel)


	#plt.semilogy() 
	plt.xlim(0, numPoints*20)
	plt.title(title)
	plt.ylabel(ylabel, weight='bold')
	plt.xlabel("Time-step", weight='bold')
	plt.legend(loc='upper center', frameon=True, ncol=2, fontsize=12)
	#plt.tight_layout()
	plt.ylim(0.75,1.5)	
	#I save the figures rather than showing them, replace the bottom 2 lines with the third to show each figure
	print output_file
	plt.savefig(output_file)
	plt.gcf().clear()
	#plt.show()



# create plots for compressor & tolerance
tolerances = ["1E-6","1E-7","1E-8","1E-9","1E-10"]
for metric in [0,1,3]:
	plot_v_original(["zfp-0.5.1","zfp-0.5.4"],tolerances, metric)




