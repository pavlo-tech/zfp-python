#ifndef ZFP_INTERFACE_H
#define ZFP_INTERFACE_H


#include <algorithm>
#include <climits>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <sys/time.h>
#include <assert.h>

#include "zfp.h"

int zfp_shrink_expand_interface(int ZFP_datatype, double* in, double* out, int size,
    int nx, int ny, int nz, double abs_tol, double& comp_time, double& decomp_time);

#endif

