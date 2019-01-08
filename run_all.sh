#!/bin/bash
for i in {6..10}
do
tol=1E-$i
file=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.1/100.txt
echo $file
python compress_zfp.py $tol 100 > $file
echo DONE
done



