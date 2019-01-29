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




if len(sys.argv) != 3:
	print("USAGE python " + sys.argv[0] + " qfile1 qfile2")
	sys.exit()

qfile1 = sys.argv[1]
qfile2 = sys.argv[2]

def copy_1d_array(a,nx,ny,nz):
	b = np.zeros((nx, ny, nz))
	for k in xrange(nz):
		for j in xrange(ny):
			for i in xrange(nx):
				b[i][j][k] = a[i+ny*(j+nz*k)]

	return b

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
for g in xrange(2):
	for cv in xrange(5):
		p3d.read_file(qfile1)
		grid1 = p3d.get_var(g,cv)
		
		p3d.read_file(qfile2)
		grid2 = p3d.get_var(g,cv)

		print "Grid " + str(g) + " Variable "+str(cv)
		print grid1 - grid2






