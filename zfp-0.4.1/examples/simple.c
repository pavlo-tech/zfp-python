/* minimal code example showing how to call the zfp (de)compressor */
#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "zfp.h"

double calculateAVG(double array[], int len);
double calculateSTDDEV(double array[], int len);

void print_3d_array(double* array, int nx, int ny, int nz)
{
	int i, j, k;
  for (k = 0; k < nz; k++)
  	for (j = 0; j < ny; j++)
    	for (i = 0; i < nx; i++)
			{
    		fprintf(stdout, "%lf\n", array[i + nx * (j + ny * k)]);
      }
}
void copy_doubles(double* iArray, int nx, int ny, int nz, double* oArray)
{
	int i, j, k;
  for (k = 0; k < nz; k++)
    for (j = 0; j < ny; j++)
      for (i = 0; i < nx; i++)
      {
        oArray[i + nx * (j + ny * k)] = iArray[i + nx * (j + ny * k)];
      }
}


/* compress and decompress iArray, place result into oArray, preserve iArray*/
void cycle(double* iArray, int nx, int ny, int nz, double tolerance, int iterations, double* oArray)
{

	int i;
  double cRatio;
  double cTimesAVG;
  double cTimesSTDDEV;
  double dTimesAVG;
  double dTimesSTDDEV;
	//double cTimes[iterations];
  //double dTimes[iterations];

	// store iArray in oArray
 	//fprintf(stdout, "copying iArray\n");
	//copy_doubles(iArray,nx,ny,nz,oArray);
	memcpy(oArray, iArray, nx * ny * nz * sizeof(double));
 	//fprintf(stdout, "copy successful\n");
	clock_t stime,etime;
	
	int status = 0;
  zfp_type type;     /* array scalar type */
  zfp_field* field;  /* array meta data */
  zfp_stream* zfp;   /* compressed stream */
  void* buffer;      /* storage for compressed stream */
  size_t bufsize;    /* byte size of compressed buffer */
  bitstream* stream; /* bit stream to write to or read from */
  size_t zfpsize;    /* byte size of compressed stream */

  /* allocate meta data for the 3D array a[nz][ny][nx] */
  type = zfp_type_double;
  field = zfp_field_3d(oArray, type, nx, ny, nz);
  /* allocate meta data for a compressed stream */
  zfp = zfp_stream_open(NULL);
//zfp_stream_set_accuracy(zfp_stream* zfp, double tolerance, zfp_type type)
  zfp_stream_set_accuracy(zfp, tolerance, type);
  /* allocate buffer for compressed data */
  bufsize = zfp_stream_maximum_size(zfp, field);
  buffer = malloc(bufsize);
  /* associate bit stream with allocated buffer */
  stream = stream_open(buffer, bufsize);
  zfp_stream_set_bit_stream(zfp, stream);


	stime = clock();
	for (i = 0; i < iterations; ++i)
  {
  	zfp_stream_rewind(zfp);
		zfpsize = zfp_compress(zfp, field);
	}
	etime = clock();
	cTimesAVG = (double)(etime - stime) / (CLOCKS_PER_SEC * iterations);
  
	if (!zfpsize)
	{
  	fprintf(stderr, "compression failed\n");
	}

	cRatio = ((double)nx) * ((double)ny) * ((double)nz) * sizeof(double) / zfpsize;

	stime = clock();
	for (i = 0; i < iterations; ++i)
 	{
		zfp_stream_rewind(zfp);
		status = zfp_decompress(zfp, field);	
	}
	etime = clock();  
  dTimesAVG =  (double)(etime - stime) / (CLOCKS_PER_SEC * iterations);

	if (!status)
	{
  	fprintf(stderr, "decompression failed\n");
  }		

  
	/* clean up */
  zfp_field_free(field);
  zfp_stream_close(zfp);
  stream_close(stream);
  free(buffer);
	
	/* calculate avg & stddev for cTime and dTime*/
  cTimesSTDDEV =  0;//calculateSTDDEV(cTimes, iterations);
  dTimesSTDDEV =  0;//calculateSTDDEV(dTimes, iterations);

  /* print stats to user */
  printf("Compression Factor =\t%lf\n",cRatio);
  printf("Time =\t%E\n",cTimesAVG);
  printf("STD_DEV =\t%E\n",cTimesSTDDEV);
  printf("Time =\t%E\n",dTimesAVG);
  printf("STD_DEV =\t%E\n",dTimesSTDDEV);

	//print_3d_array(iArray,nx,ny,nz);
	//fprintf(stdout,"----------\n");
	//print_3d_array(oArray,nx,ny,nz);
}

double calculateAVG(double array[], int len)
{
  int i;
  double avg = 0;

  for (i = 0; i < len; ++i)
  {
    avg += array[i];
  }

  return avg;
}

/* I did not know how to calculate this, I used the formula from:
 *  * https://www.mathsisfun.com/data/standard-deviation-formulas.html
 *   * */
double calculateSTDDEV(double array[], int len)
{
  int i;
  double stddev;
  double sumsq = 0;
  double mean = calculateAVG(array, len);

  for (i = 0; i < len; ++i)
  {
    sumsq += pow(array[i] - mean, 2);
  }

  stddev = sqrt(sumsq / len);

  return stddev;
}


int main1(int argc, char* argv[])
{
  /* allocate 100x100x100 array of doubles */
  int nx = 8;
  int ny = 8;
  int nz = 8;
  double* iArray = malloc(nx * ny * nz * sizeof(double));
  double* oArray = malloc(nx * ny * nz * sizeof(double));

  /* initialize array to be compressed */
  int i, j, k;
  for (k = 0; k < nz; k++)
    for (j = 0; j < ny; j++)
      for (i = 0; i < nx; i++)
      {
        double x = 2.0 * i / nx;
        double y = 2.0 * j / ny;
        double z = 2.0 * k / nz;
        iArray[i + nx * (j + ny * k)] = exp(-(x * x + y * y + z * z));
      }

  /* compress or decompress array */
  cycle(iArray, nx, ny, nz, 1e-4, 100, oArray);

 // print_3d_array(iArray, nx,ny,nz);
 // fprintf(stdout,"-----------\n");
 // print_3d_array(oArray,nx,ny,nz);
 // fprintf(stdout, "compression time: %lf\n", cTime);
 // fprintf(stdout, "decompression time: %lf\n", dTime);
 // fprintf(stdout, "compression ratio: %lf\n", cRatio);


  free(iArray);
  free(oArray);
  return 0;
}
