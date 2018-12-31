import os
import sys
import compress_gold_objects as cgo
import parse_output as parse
import subprocess

GOLD_DIR = "/zfs/fthpc/plascomcm/inputs/flowpastcylinder/palmetto_gold/"

PRINT_OUTPUT_DIR = "./"

COMPRESSOR_DIR = "./"

DUMMY_FILE = "dummy.q"


if len(sys.argv) != 4:
	print("USAGE python compress_gold_zfp.py compressor tolerance iterations")
	sys.exit()

COMPRESSOR = sys.argv[1]
TOLERANCE = sys.argv[2]
ITERATIONS = sys.argv[3]

# create file names
output_dir = PRINT_OUTPUT_DIR + TOLERANCE + "/" + COMPRESSOR + "/"
text_file =	output_dir + ITERATIONS + ".txt"
error_file = output_dir + ITERATIONS + ".err"
data_file = output_dir + ITERATIONS
dummy_file = output_dir + DUMMY_FILE

# remove previous instances of files
os.system("rm -f " + text_file)
os.system("rm -f " + error_file)
os.system("rm -f " + data_file)

# get all files from gold directory ending in .q
qfiles = [(GOLD_DIR + fileName) for fileName in os.listdir(GOLD_DIR) if fileName[-1] == "q" and fileName != "RocFlo-CM.00000000.q"]
qfiles.sort()

# create output file pointers
out = open(text_file, "w")
err = open(error_file, "w")

# compress each file
for file_name in qfiles:
	executable = COMPRESSOR_DIR + COMPRESSOR + "/_compress" 
	#parameters = file_name + " " + dummy_file + " " + TOLERANCE + " " + ITERATIONS
	#output = ">> " + text_file + " 2>> " + error_file
	#output_2 = ">> " + text_file
	#command = executable + " " + parameters + " " + output_2
	#os.system(command)

	proc = subprocess.Popen([executable, file_name, dummy_file, TOLERANCE, ITERATIONS], stdout=out, stderr=err)
	proc.wait()

# close output files
#out.close()
#err.close()

# write output to npy array
parse.parse_output(text_file, data_file)


