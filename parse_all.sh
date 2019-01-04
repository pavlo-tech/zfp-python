#!/bin/bash
for i in {6..10}
do
tol=1E-$i
infile=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.1/20.txt
outfile=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.1/20
echo $infile
python parse_output.py $infile $outfile
echo $outfile
done



