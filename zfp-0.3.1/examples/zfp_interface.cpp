#include "zfp_interface.h"

/*
void usage()
{
  std::cerr << "Usage: zfp [options] <nx> [ny nz infile outfile]" << std::endl;
  std::cerr << "  nx, ny, nz : grid dimensions (set nz = 0 for 2D, ny = nz = 0 for 1D)" << std::endl;
  std::cerr << "  infile : optional floating-point input file to compress" << std::endl;
  std::cerr << "  outfile : optional output file for reconstructed data" << std::endl;
  std::cerr << "Options:" << std::endl;
  std::cerr << "  -f : single precision (float type)" << std::endl;
  std::cerr << "  -d : double precision (double type)" << std::endl;
  std::cerr << "  -r <rate> : fixed rate (# compressed bits per floating-point value)" << std::endl;
  std::cerr << "  -p <precision> : fixed precision (# uncompressed bits per value)" << std::endl;
  std::cerr << "  -a <tolerance> : fixed accuracy (absolute error tolerance)" << std::endl;
  std::cerr << "  -c <minbits> <maxbits> <maxprec> <minexp> : advanced usage" << std::endl;
  std::cerr << "      minbits : min # bits per 4^d values in d dimensions" << std::endl;
  std::cerr << "      maxbits : max # bits per 4^d values in d dimensions" << std::endl;
  std::cerr << "      maxprec : max # bits of precision per value (0 for full)" << std::endl;
  std::cerr << "      minexp : min bit plane # coded (-1074 for all bit planes)" << std::endl;
  std::cerr << "Examples:" << std::endl;
  std::cerr << "  zfp -f -r 16 100 100 100 : 2x fixed-rate compression of 100x100x100 floats" << std::endl;
  std::cerr << "  zfp -d -r 32 1000000 : 2x fixed-rate compression of stream of 1M doubles" << std::endl;
  std::cerr << "  zfp -d -p 32 1000 1000 : 32-bit precision compression of 1000x1000 doubles" << std::endl;
  std::cerr << "  zfp -d -a 1e-9 1000000 : compression of 1M doubles with < 1e-9 error" << std::endl;
  std::cerr << "  zfp -d -c 64 64 0 -1074 1000000 : 4x fixed-rate compression of 1M doubles" << std::endl;
  exit(EXIT_FAILURE);
}
*/

int zfp_shrink_expand_interface(int ZFP_datatype, double* in, double* out, int size,
    int nx, int ny, int nz, double abs_tol, double& comp_time, double& decomp_time)
{
    struct timeval begin, end;
  // default settings
  uint type = ZFP_datatype;
  double rate = 0;
  uint precision = 0;



  // set array type and size
  zfp_params params;
  zfp_init(&params);
  params.type = type;
  params.nx = nx;
  params.ny = ny;
  params.nz = nz;

    zfp_set_accuracy(&params, abs_tol);

  // effective array dimensions
  uint mx = std::max((uint)nx, 1u);
  uint my = std::max((uint) ny, 1u);
  uint mz = std::max((uint) nz, 1u);


  // allocate space for uncompressed and compressed fields
  size_t outsize = zfp_estimate_compressed_size(&params);
  assert(outsize != 0 && "invalid compression parameters\n");
  

  unsigned char* zip = new unsigned char[outsize];


    // compress data
    gettimeofday(&begin, NULL);
    outsize = zfp_compress(&params, (unsigned char*) in, zip, outsize);
    gettimeofday(&end, NULL);
    comp_time = (end.tv_sec - begin.tv_sec) + 
              ((end.tv_usec - begin.tv_usec)/1000000.0);
  assert(outsize != 0 && "Compression failed\n");
  rate = CHAR_BIT * double(outsize) / (mx * my * mz);
  
    // decompress
    gettimeofday(&begin, NULL);
    int result = zfp_decompress(&params, out, zip, outsize); 
    gettimeofday(&end, NULL);
    decomp_time = (end.tv_sec - begin.tv_sec) + 
              ((end.tv_usec - begin.tv_usec)/1000000.0);
    assert(result != 0 && "decompression failed\n");

  // compute error
/*
  double e = 0;
  double fmin = dp ? fd[0] : ff[0];
  double fmax = fmin;
  double emax = 0;
  for (uint i = 0; i < mx * my * mz; i++) {
    double d = fabs(dp ? fd[i] - gd[i] : ff[i] - gf[i]);
    emax = std::max(emax, d);
    e += d * d;
    double val = dp ? fd[i] : ff[i];
    fmin = std::min(fmin, val);
    fmax = std::max(fmax, val);
  }
  e = sqrt(e / (mx * my * mz));
  double nrmse = e / (fmax - fmin);
  double psnr = 20 * log10((fmax - fmin) / (2 * e));
  
  std::cerr << "in=" << insize << " out=" << outsize << " ratio=" << std::setprecision(3) << double(insize) / outsize << " rate=" << std::setprecision(4) << rate << " rmse=" << e << " nrmse=" << nrmse << " maxe=" << emax << " psnr=" << std::fixed << std::setprecision(2) << psnr << std::endl;
*/
  // clean up
  delete[] zip;

  return outsize;
}
