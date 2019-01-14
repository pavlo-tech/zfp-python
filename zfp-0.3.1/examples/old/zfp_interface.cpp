#include <algorithm>
#include <cmath>
#include <ctime>
#include <cstdio>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <sstream>
#include <string>
#include "zfp.h"
#include "zfparray1.h"
#include "zfparray2.h"
#include "zfparray3.h"


typedef unsigned char uchar;
typedef unsigned long long uint64;

int width = 72; // characters per line

{
  // volatile used to ensure bit-for-bit reproducibility across compilers
  volatile Scalar xx = x * x;
  volatile Scalar yy = 4 * xx - 3;
  volatile Scalar p = x + xx * yy;
  return p;
}

// initialize array
template <typename Scalar>
inline void
initialize(Scalar* p, int nx, int ny, int nz, Scalar (*f)(Scalar))
{
  nx = std::max(nx, 1);
  ny = std::max(ny, 1);
  nz = std::max(nz, 1);
#if TEST_SIZE == 4
  // use precomputed small arrays for portability
  uint d = nz == 1 ? ny == 1 ? 0 : 1 : 2;
  std::copy(&Field<Scalar>::array[d][0], &Field<Scalar>::array[d][0] + nx * ny * nz, p);
#else
  for (int k = 0; k < nz; k++) {
    volatile Scalar z = Scalar(2 * k - nz + 1) / nz;
    volatile Scalar fz = nz > 1 ? f(z) : Scalar(1);
    for (int j = 0; j < ny; j++) {
      volatile Scalar y = Scalar(2 * j - ny + 1) / ny;
      volatile Scalar fy = ny > 1 ? f(y) : Scalar(1);
      for (int i = 0; i < nx; i++) {
        volatile Scalar x = Scalar(2 * i - nx + 1) / nx;
        volatile Scalar fx = nx > 1 ? f(x) : Scalar(1);
        *p++ = fx * fy * fz;
      }
    }
  }
#endif
}

// compute checksum
inline uint32
hash(const void* p, size_t n)
{
  uint32 h = 0;
  for (const uchar* q = static_cast<const uchar*>(p); n; q++, n--) {
    // Jenkins one-at-a-time hash; see http://www.burtleburtle.net/bob/hash/doobs.html
    h += *q;
    h += h << 10;
    h ^= h >>  6;
  }
  h += h <<  3;
  h ^= h >> 11;
  h += h << 15;
  return h;
}

template <typename Scalar>
inline uint zfp_type();

template <>
inline uint zfp_type<float>() { return ZFP_TYPE_FLOAT; }

template <>
inline uint zfp_type<double>() { return ZFP_TYPE_DOUBLE; }



// test fixed-accuracy mode
template <typename Scalar>
inline uint
test_accuracy(zfp_params* p, Scalar tolerance, const Scalar* f, uint n, size_t bytes)
{
  uint failures = 0;

  // allocate memory for compressed data
  tolerance = zfp_set_accuracy(p, tolerance);
  size_t bufsize = zfp_estimate_compressed_size(p);
  uchar* buffer = new uchar[bufsize];

  // perform compression test
  std::ostringstream status;
  status << "  compress:  ";
  status << " tolerance=" << std::scientific << std::setprecision(3) << tolerance;
  size_t outsize = zfp_compress(p, f, buffer, bufsize);
  double ratio = double(n * sizeof(Scalar)) / outsize;
  status << " ratio=" << std::fixed << std::setprecision(3) << std::setw(7) << ratio;
  bool pass = true;
  // make sure compressed size agrees
  if (outsize != bytes) {
    status << " [" << outsize << " != " << bytes << "]";
    pass = false;
  }
  std::cout << std::setw(width) << std::left << status.str() << (pass ? " OK " : "FAIL") << std::endl;
  if (!pass)
    failures++;

  // perform decompression test
  status.str("");
  status << "  decompress:";
  status << " tolerance=" << std::scientific << std::setprecision(3) << tolerance;
  Scalar* g = new Scalar[n];
  pass = zfp_decompress(p, g, buffer, outsize);
  if (!pass)
    status << " [decompression failed]";
  else {
    // compute max error
    Scalar emax = 0;
    for (uint i = 0; i < n; i++)
      emax = std::max(emax, std::abs(f[i] - g[i]));
    status << std::scientific << std::setprecision(3) << " ";
    // make sure max error is within tolerance
    if (emax <= tolerance)
      status << emax << " <= " << tolerance;
    else if (tolerance == 0)
      status << "(" << emax << " > 0)";
    else {
      status << "[" << emax << " > " << tolerance << "]";
      pass = false;
    }
  }
  delete[] g;
  delete[] buffer;
  std::cout << std::setw(width) << std::left << status.str() << (pass ? " OK " : "FAIL") << std::endl;
  if (!pass)
    failures++;

  return failures;
}

// perform 1D differencing
template <typename Scalar>
inline void
update_array1(ZFP::Array1<Scalar>& a)
{
  for (uint i = 0; i < a.size() - 1; i++)
    a(i) -= a(i + 1);
  for (uint i = 0; i < a.size() - 1; i++)
    a(0) = std::max(a(0), a(i));
}


template <class Array>
inline void update_array(Array& a);

template <>
inline void
update_array(ZFP::Array1<float>& a) { update_array1(a); }

template <>
inline void
update_array(ZFP::Array1<double>& a) { update_array1(a); }


// test random-accessible array primitive
template <class Array, typename Scalar>
inline uint
test_array(Array& a, const Scalar* f, uint n, double tolerance, double dfmax)
{
  uint failures = 0;

  // test construction
  std::ostringstream status;
  status << "  construct: ";
  Scalar emax = 0;
  for (uint i = 0; i < n; i++)
    emax = std::max(emax, std::abs(f[i] - a[i]));
  status << std::scientific;
  status.precision(3);
  // make sure max error is within tolerance
  bool pass = true;
  if (emax <= tolerance)
    status << " " << emax << " <= " << tolerance;
  else {
    status << " [" << emax << " > " << tolerance << "]";
    pass = false;
  }

  std::cout << std::setw(width) << std::left << status.str() << (pass ? " OK " : "FAIL") << std::endl;
  if (!pass)
    failures++;

  // test array updates
  status.str("");
  status << "  update:    ";
  update_array(a);
  Scalar amax = a[0];
  pass = true;
  if (std::abs(amax - dfmax) <= 1e-3 * dfmax)
    status << " " << amax << " ~ " << dfmax;
  else {
    status << " [" << amax << " != " << dfmax << "]";
    pass = false;
  }

  std::cout << std::setw(width) << std::left << status.str() << (pass ? " OK " : "FAIL") << std::endl;
  if (!pass)
    failures++;

  return failures;
}

// test arrays with m^6 scalars
template <typename Scalar>
inline uint
test(uint m)
{
  uint failures = 0;
  uint n = m * m * m * m * m * m;
  Scalar* f = new Scalar[n];
  // test 1D, 2D, and 3D arrays
  for (uint d = 1; d <= 3; d++) {
    // determine array size
    uint nx, ny, nz;
    switch (d) {
      case 1:
        nx = n;
        ny = 0;
        nz = 0;
        break;
      case 2:
        nx = m * m * m;
        ny = m * m * m;
        nz = 0;
        break;
      case 3:
        nx = m * m;
        ny = m * m;
        nz = m * m;
        break;
    }
    initialize<Scalar>(f, nx, ny, nz, polynomial);
    zfp_params p;
    zfp_init(&p);
    uint t = zfp_set_type(&p, zfp_type<Scalar>()) - 1;
    p.nx = nx;
    p.ny = ny;
    p.nz = nz;
    std::cout << "testing " << d << "D array of " << (p.type == ZFP_TYPE_FLOAT ? "floats" : "doubles") << std::endl;

    // test data integrity
    uint32 checksum[2][3] = {
#if TEST_SIZE == 4
      { 0xdad6fd69u, 0x000f8df1u, 0x60993f48u },
      { 0x8d95b1fdu, 0x96a0e601u, 0x66e77c83u },
#elif TEST_SIZE == 8
      { 0x269fb420u, 0xfc4fd405u, 0x733b9643u },
      { 0x3321e28bu, 0xfcb8f0f0u, 0xd0f6d6adu },
#elif TEST_SIZE == 16
      { 0x62d6c2b5u, 0x88aa838eu, 0x84f98253u },
      { 0xf2bd03a4u, 0x10084595u, 0xb8df0e02u },
#endif
    };
    uint32 h = hash(f, n * sizeof(Scalar));
    if (h != checksum[t][d - 1])
{
printf("%#010x\n", h);
      std::cout << "warning: array checksum mismatch; tests below may fail" << std::endl;
}

    // test fixed rate
    for (uint rate = 4u >> p.type, i = 0; rate <= 32 * p.type; rate *= 4, i++) {
      // expected max errors
#if TEST_SIZE == 4
      Scalar emax[2][3][4] = {
        {
          {1.998e+00, 7.694e-03, 0.000e+00},
          {2.981e-01, 1.154e-03, 7.451e-09},
          {2.990e-01, 6.333e-03, 7.451e-08},
        },
        {
          {1.998e+00, 9.974e-01, 1.904e-05},
          {3.361e+00, 3.833e-02, 3.330e-06},
          {1.128e+00, 8.706e-02, 2.583e-05},
        }
      };
#elif TEST_SIZE == 8
      Scalar emax[2][3][4] = {
        {
          {2.000e+00, 2.073e-03, 0.000e+00},
          {9.910e-02, 2.790e-05, 2.329e-10},
          {6.881e-02, 1.836e-04, 1.193e-07},
        },
        {
          {2.000e+00, 1.000e+00, 3.790e-06, 0.000e+00},
          {2.079e+00, 4.166e-03, 4.043e-08, 0.000e+00},
          {2.935e-01, 6.633e-03, 3.213e-07, 3.470e-18},
        }
      };
#elif TEST_SIZE == 16
      Scalar emax[2][3][4] = {
        {
          {2.000e+00, 1.955e-03, 0.000e+00},
          {3.752e-02, 9.537e-07, 2.911e-11},
          {5.576e-03, 2.385e-06, 2.385e-07},
        },
        {
          {2.000e+00, 2.000e+00, 1.011e-06, 0.000e+00},
          {3.990e+00, 4.782e-04, 3.459e-10, 5.294e-23},
          {7.913e-02, 1.522e-04, 3.072e-09, 8.674e-19},
        }
      };
#endif
      failures += test_rate(&p, rate, f, n, emax[t][d - 1][i]);
    }

    // test fixed precision
    for (uint prec = 2u << p.type, i = 0; i < 3; prec *= 2, i++) {
      // expected compressed sizes
#if TEST_SIZE == 4
      size_t bytes[2][3][3] = {
        {
          {2045, 3107, 6130},
          { 477, 1212, 4207},
          {  97,  580, 4200},
        },
        {
          {3491, 6514, 14510},
          {1308, 4303, 12483},
          { 604, 4224, 12451},
        },
      };
#elif TEST_SIZE == 8
      size_t bytes[2][3][3] = {
        {
          {131067, 196650, 337770},
          { 32351,  59658, 162297},
          {  7023,  24105, 138810},
        },
        {
          {221221, 362067, 774806},
          { 65802, 168442, 574288},
          { 25641, 140346, 610379},
        },
      };
#elif TEST_SIZE == 16
      size_t bytes[2][3][3] = {
        {
          {8388427, 12582605, 20986156},
          {2092252,  3254295,  7653793},
          { 502812,  1196739,  4941325},
        },
        {
          {14155812, 22555255, 45432484},
          { 3647497,  8038375, 25569052},
          { 1295043,  5039644, 25621059},
        },
      };
#endif
      failures += test_precision(&p, prec, f, n, bytes[t][d - 1][i]);
    }

    // test fixed accuracy
    for (uint i = 0; i < 3; i++) {
      Scalar tol[] = { 1e-3, 2 * std::numeric_limits<Scalar>::epsilon(), 0 };
      // expected compressed sizes
#if TEST_SIZE == 4
      size_t bytes[2][3][3] = {
        {
          {4582, 10048, 14155},
          {2920,  8876, 12387},
          {4365, 10555, 12427},
        },
        {
          {4966, 25408, 30953},
          {3016, 23833, 28867},
          {4389, 25427, 28835},
        },
      };
#elif TEST_SIZE == 8
      size_t bytes[2][3][3] = {
        {
          {264596, 543194, 793515},
          {101443, 334356, 585634},
          { 92328, 399624, 611273},
        },
        {
          {289172, 1478240, 1834179},
          {107587, 1263509, 1623179},
          { 93864, 1350443, 1660067},
        },
      };
#elif TEST_SIZE == 16
      size_t bytes[2][3][3] = {
        {
          {16933954, 31484816, 47539984},
          { 5160031, 14566330, 29177076},
          { 2673814, 13226122, 27426704},
        },
        {
          {18506815, 84659489, 107808298},
          { 5553248, 64162158,  87851011},
          { 2772118, 68112040,  90936514},
        },
      };
#endif
      failures += test_accuracy(&p, tol[i], f, n, bytes[t][d - 1][i]);
    }

    // test compressed array support
#if TEST_SIZE == 4
    Scalar emax[2][3] = {
      {2.981e-08, 7.451e-09, 7.451e-08},
      {9.100e-08, 1.804e-08, 9.261e-08},
    };
    Scalar dfmax[2][3] = {
      {4.385e-03, 9.260e-02, 3.760e-01},
      {4.385e-03, 9.260e-02, 3.760e-01},
    };
#elif TEST_SIZE == 8
    Scalar emax[2][3] = {
      {0.000e+00, 2.329e-10, 1.193e-07},
      {3.440e-09, 1.421e-10, 1.681e-09},
    };
    Scalar dfmax[2][3] = {
      {6.866e-05, 1.791e-03, 2.239e-02},
      {6.866e-05, 1.792e-03, 2.239e-02},
    };
#elif TEST_SIZE == 16
    Scalar emax[2][3] = {
      {3.553e-15, 2.911e-11, 2.385e-07},
      {5.808e-10, 6.942e-13, 6.740e-12},
    };
    Scalar dfmax[2][3] = {
      {1.073e-06, 2.879e-05, 4.714e-04},
      {1.073e-06, 2.889e-05, 4.714e-04},
    };
#endif
    double rate = 24;
    switch (d) {
      case 1: {
          ZFP::Array1<Scalar> a(nx, rate, f);
          failures += test_array(a, f, n, emax[t][d - 1], dfmax[t][d - 1]);
        }
        break;
      case 2: {
          ZFP::Array2<Scalar> a(nx, ny, rate, f);
          failures += test_array(a, f, n, emax[t][d - 1], dfmax[t][d - 1]);
        }
        break;
      case 3: {
          ZFP::Array3<Scalar> a(nx, ny, nz, rate, f);
          failures += test_array(a, f, n, emax[t][d - 1], dfmax[t][d - 1]);
        }
        break;
    }

    std::cout << std::endl;
  }

  delete[] f;
  return failures;
}

