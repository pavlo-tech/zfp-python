'''
Author: Pavlo Triantafyllides
Purpose: Reads a file, runs cycle at several iterations and outputs a file with the lossy data
USAGE: python cycle_zfp.py input_file output_file tolerance iterations"
BUGS: I have not tested the output file.
	I am uncertain that I am correctly copying the 1d array into a new np array.
	If there is a bug with the format of the output file, I will consider using np.reshape() rather than my
	copy function, or reordering the indeces of the array.
'''
import os
import sys
sys.path.insert(0, './fortranfile-0.2.1')
sys.path.insert(0, './PyPLOT3D')
import P3D
import numpy as np
import ctypes
import math




if len(sys.argv) != 6:
	print("USAGE python cycle_zfp.py input_file output_file tolerance iterations cycle_path")
	sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]
TOL = float(sys.argv[3])
ITER = int(sys.argv[4])
cycle_path = sys.argv[5]

# ex: './zfp-0.5.1/examples/simple.dll'
zfp_dll = ctypes.cdll.LoadLibrary(cycle_path)
cycle = zfp_dll.cycle

def copy_3d_array(a):
	nx, ny, nz = a.shape
	a = a.flatten()#a.ravel()
	b = np.zeros(nx * ny * nz)
	for k in xrange(nz):
		for j in xrange(ny):
			for i in xrange(nx):
				b[i+ny*(j+nz*k)] = a[i+ny*(j+nz*k)]

	return nx,ny,nz,b

# I don't know if this is working correctly
def copy_1d_array(a,nx,ny,nz):
	a = a.reshape((nx,ny,nz))
	b = np.zeros((nx, ny, nz))
	for k in xrange(nz):
		for j in xrange(ny):
			for i in xrange(nx):
				b[i][j][k] = a[i][j][k]#a[i+ny*(j+nz*k)]

	return np.reshape(b,(nx,ny,nz))

# prints if the values are different
def print_difference(a,b,nx,ny,nz):
	for k in xrange(nz):
		for j in xrange(ny):
			for i in xrange(nx):
				x = a[i+ny*(j+nz*k)]
				x_err = b[i][j][k]	
				v = abs(x - x_err)
				if v > TOL:
					print "ERROR: " + str(v)



# create p3d reader
p3d = P3D.PLOT3D_FILE()

p3d.read_file(input_file)
print "File: " + input_file
for g in xrange(2):
	for cv in xrange(5):
		print "\n============================="
		print "Compressing CV=           " + str(cv)
		grid = p3d.get_var(g,cv)
		'''
		grid = np.zeros((3,3,1))
		k=1
		for i in [0,1,2]:
			for j in [0,1,2]:
				grid[i][j][0] = k
				k += 1
		print grid
		'''
		#nx,ny,nz,rArr=copy_3d_array(grid) 
		nx,ny,nz = grid.shape
		rArr = np.zeros(nx*ny*nz)
		p = 0
		for k in xrange(nz):
			for j in xrange(ny):
				for i in xrange(nx):
					rArr[p] = grid[i][j][k]
					p += 1
		print rArr
		#rArr = rArr.astype(np.float64)		# VERIFY 64 bit
		iArr = rArr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

		#nx,ny,nz,nArr=copy_3d_array(np.zeros((nx,ny,nz)))
		nArr = np.zeros(nx*ny*nz)
		#nArr = nArr.astype(np.float64) 
		oArr = nArr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

		# THE BUG IS PROBABLY IN ONE OF THESE POINTERS OR .ctypes.data		
		print "Shape of array          " + str(nx) + "          " + str(ny) + "           " + str(nz)
		cycle(iArr,nx,ny,nz, ctypes.c_double(TOL), ITER, oArr)
		print "=============================\n"
		print nArr
		grid1= np.copy(grid)
		#print "\n\nlossy: " , np.max(np.abs(iArr-oArr))
		p = 0
		for k in xrange(nz):
			for j in xrange(ny):
				for i in xrange(nx):
					grid[i][j][k] = nArr[p]
					p += 1
	
		#wArr = copy_1d_array(oArr,nx,ny,nz)
		#wArr = np.copy(np.reshape(oArr, (nx,ny,nz), order='C'), order='F')
		
		#wArr = np.reshape(oArr, (nx,ny,nz),order='F')
		#wArr = copy_1d_array(oArr,nx,ny,nz)

		#print np.max(np.abs(iArr-oArr))
		#print type(iArr)
		print np.max(np.abs(grid-grid1))
		p3d.set_var(grid,g,cv)

p3d.write_file(output_file)



