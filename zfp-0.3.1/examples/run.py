import numpy as np
import zfp_interface as ZFP

n=100
#a = np.ones(n, dtype=np.double)
a = np.random.rand(n)* (np.random.rand(n).reshape((1,n)))
print a.shape
a = a.reshape((n))
b = np.zeros(n)
Tc = Td = 0
ZFP_DOUBLE_TYPE = 2
ZFP_FLOAT_TYPE = 1  
ret = ZFP.zfp_compress_decompress(ZFP_DOUBLE_TYPE, a, b,
                    a.shape[0], 1, 1, # nx x ny x nz
                    1e-5, Tc, Td)
print ret
nBytes = ret[0]
print "Compression ratio: ", (8.*n)/nBytes*100. , "%"
diff = a-b
print "Inf-norm", np.linalg.norm(diff, np.inf) 
print "2-norm", np.linalg.norm(diff, 2) 
#print "A-norm", np.linalg.norm((A*a)-b, 2) 
