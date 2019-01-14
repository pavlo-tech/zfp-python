/*  Example of wrapping a C function that takes a C double array as input using
 *  numpy typemaps for SWIG. */

%module zfp_interface
%{
    /* the resulting C file should be built as a python extension */
    #define SWIG_FILE_WITH_INIT
    /*  Includes the header in the wrapper code */
    #include "zfp_interface.h"
%}

/*  include the numpy typemaps */
%include "numpy.i"
/*  need this for correct module initialization */
%init %{
    import_array();
%}

/*  typemaps for the two arrays, the second will be modified in-place */
%apply (double* IN_ARRAY1, int DIM1) {(double* data_in, int data_in_size)}
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* data_out, int data_out_size)}
%apply (double& INOUT) {(double& comp_time)}
%apply (double& INOUT) {(double& decomp_time)}

/*  Wrapper for cos_doubles that massages the types */
%inline %{
int zfp_compress_decompress(int ZFP_datatype, double* data_in, int data_in_size,
                            double* data_out, int data_out_size,
                            int nx, int ny, int nz, double abs_tol,
                            double& comp_time, double& decomp_time)
    
    {
        return zfp_shrink_expand_interface(ZFP_datatype, data_in, data_out, data_in_size,
                                    nx, ny, nz, abs_tol, comp_time, decomp_time);
    }
%}
