#!/bin/bash
for i in {6..10}
do
iter=1000
tol=1E-$i
infile=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.1/$iter.txt
outfile=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.1/$iter
echo $infile
python parse_output.py $infile $outfile
echo $outfile
done



