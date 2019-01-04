import os
import sys
sys.path.insert(0, './fortranfile-0.2.1')
sys.path.insert(0, './PyPLOT3D')
import P3D
import numpy as np
import ctypes
import math

GOLD_DIR = "/zfs/fthpc/plascomcm/inputs/flowpastcylinder/palmetto_gold/"
TOL = float(sys.argv[1])
ITER = 20


# https://stackoverflow.com/questions/5862915/passing-numpy-arrays-to-a-c-function-for-input-and-output
zfp_dll = ctypes.cdll.LoadLibrary('./zfp-0.5.1/examples/simple.dll')
cycle = zfp_dll.cycle

'''
[context deleted 12/31]
Above appears to work, below does not. 
I suspect this may be due to some sort of data organization concerning long arrays 

12/31: 
	I was able to get the bottom to work by copying the read data into a new array,
	I suppose that this indicates that my above hypothesis was correct.
'''

'''
	copies a 3d array and returns a new one
	I am unsure why this is necessary, I am
	guessing it has to fix the memory layout
'''
def copy_3d_array(a):
	nx, ny, nz = a.shape
	a = a.ravel()
	b = np.zeros(nx * ny * nz)
	for k in xrange(nz):
		for j in xrange(ny):
			for i in xrange(nx):
				b[i+ny*(j+nz*k)] = a[i+ny*(j+nz*k)]

	return nx,ny,nz,b



# create p3d reader
p3d = P3D.PLOT3D_FILE()

qfiles = [(GOLD_DIR + fileName) for fileName in os.listdir(GOLD_DIR) if fileName[-1] == "q" and fileName != "RocFlo-CM.00000000.q"]
qfiles.sort()

for fname in qfiles:
	p3d.read_file(fname)
	print "File: " + fname
	for g in xrange(2):
		for cv in xrange(5):
			print "\n============================="
			print "Compressing CV=           " + str(cv)
			grid = p3d.get_var(g,cv)
			nx,ny,nz,iArr = copy_3d_array(grid)
			print "Shape of array          " + str(nx) + "          " + str(ny) + "           " + str(nz)
			oArr = np.zeros(nx*ny*nz)
			cycle(ctypes.c_void_p(iArr.ctypes.data), nx, ny, nz, ctypes.c_double(TOL), ITER, ctypes.c_void_p(oArr.ctypes.data))
			#print iArr
			#print "------------------"
			#print oArr
			print "=============================\n"


