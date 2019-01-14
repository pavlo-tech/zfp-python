from distutils.core import setup, Extension
import numpy


setup(ext_modules=[Extension("_zfp_interface",
      sources=["zfp_interface.cpp", "zfp_interface.i"],
      include_dirs=[numpy.get_include(), "/home/aperson40/research/zfp-0.3.1/inc/"],
        language='c++',
        swig_opts=["-c++"], library_dirs=["/home/aperson40/research/zfp-0.3.1/lib"],
        libraries=["zfp", "m", "stdc++"])])
