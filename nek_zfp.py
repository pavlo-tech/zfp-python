'''
Author: Pavlo Triantafyllides
Purpose: Reads a nek5000 file, runs cycle at several iterations and outputs a file with the lossy data
USAGE: python nek_zfp.py input_file output_file tolerance iterations"
'''
import os
import sys
sys.path.insert(0, './fortranfile-0.2.1')
sys.path.insert(0, './PyPLOT3D')
import NEK_DATA as nek
import neksuite
import exadata
import numpy as np
import ctypes
import math


if len(sys.argv) != 6:
	print("USAGE python nek_zfp.py input_file output_file tolerance iterations cycle_path")
	sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
TOL = float(sys.argv[3])
ITER = int(sys.argv[4])
cycle_path = sys.argv[5]
print cycle_path

# ex: './zfp-0.5.1/examples/simple.dll'
zfp_dll = ctypes.cdll.LoadLibrary(cycle_path)
cycle = zfp_dll.cycle


# read in nek data
data = neksuite.readnek(input_file)
v, p = nek.unpack(data)

print "File: " + input_file
arrs = [v[:,0], v[:,1], v[:,2], p]

for i, arr in enumerate(arrs):
		
		print "\n============================="
		print "Compressing Array=           " + str(i)
		
		n = arr.shape[0]
		rArr = np.zeros(n)
		
		p = 0
		for k in xrange(n):
			rArr[p] = arr[k]
			p += 1
		
		iArr = rArr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

		nArr = np.zeros(n)
		oArr = nArr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

		# THE BUG IS PROBABLY IN ONE OF THESE POINTERS OR .ctypes.data		
		print "Shape of array          " + str(n) + "          " + str(1) + "           " + str(1)
		cycle(iArr,n, 1, 1, ctypes.c_double(TOL), ITER, oArr)
		print "=============================\n"
		print np.max(np.abs(rArr-nArr))
		# nArr contains compression results
		#repack_data = repack()
		
#writenek(output_file, repack_data)


