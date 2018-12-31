import sys
sys.path.insert(0, './fortranfile-0.2.1')
sys.path.insert(0, './PyPLOT3D')
import P3D
import numpy as np
import ctypes
import math

GOLD_DIR = "/zfs/fthpc/plascomcm/inputs/flowpastcylinder/palmetto_gold/"
TOL = float(1E-6)
ITER = 100

# https://stackoverflow.com/questions/5862915/passing-numpy-arrays-to-a-c-function-for-input-and-output
zfp_dll = ctypes.cdll.LoadLibrary('./zfp-0.5.1/examples/simple.dll')
cycle = zfp_dll.cycle
compress= zfp_dll.compress
'''
array = np.ones((8,8,8)).ravel()
for k in xrange(8):
	for j in xrange(8):
		for i in xrange(8):
			x = 2.0 * i / 8
			y = 2.0 * j / 8
			z = 2.0 * k / 8
			array[i+8*(j+8*k)] = math.exp(-(x * x + y * y + z * z))

array1 = np.zeros((8,8,8)).ravel()
cycle(ctypes.c_void_p(array.ctypes.data), 8,8,8,ctypes.c_double(TOL), 1, ctypes.c_void_p(array1.ctypes.data))

for k in xrange(8):
  for j in xrange(8):
    for i in xrange(8):
			print str(array[i+8*(j+8*k)])
print"\n--------------\n"
for k in xrange(8):
  for j in xrange(8):
    for i in xrange(8):
			print str(array1[i+8*(j+8*k)])
'''

'''
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

# test with grid0 var0
fname = GOLD_DIR + "/RocFlo-CM.00010000.q"
p3d.read_file(fname)
grid = p3d.get_var(0,0)


nx,ny,nz,iArr = copy_3d_array(grid)
oArr = np.zeros(nx*ny*nz)

#cycle(double* array, int nx, int ny, int nz, double tolerance, int iterations, double* output)
cycle(ctypes.c_void_p(iArr.ctypes.data), nx, ny, nz, ctypes.c_double(TOL), ITER, ctypes.c_void_p(oArr.ctypes.data))

print iArr
print "------------------"
print oArr


