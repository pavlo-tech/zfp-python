import sys
import numpy as np


'''
if len(sys.argv) != 3:
	print("USAGE: python parse_output.py input_file output_file");
	exit()

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

'''

def parse_output(inputFileName, outputFileName):
	numPoints = 5000
	numGrids = 2
	numVars = 5
	numCVs = 5

	CompressionValues = np.zeros((numCVs, numGrids, numVars, numPoints))

	i = 0
	point = 0
	grid = 0
	val = 0
	cv = 0

	for line in open(inputFileName).readlines():

		cv = i % numCVs
		var = (i // numCVs) % numVars
		grid = (i // (numCVs * numVars)) % numGrids
		point = (i // (numCVs * numVars * numGrids)) % numPoints
     
		if "Compression Factor =" in line or "Time =" in line or "STD_DEV =" in line:
			CompressionValues[cv][grid][var][point] = float(line.split("=")[1])
 			i += 1

	np.save(outputFileName, CompressionValues)


