#!/bin/bash
for i in {6..10}
do
tol=1E-$i
file=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.1/20.txt
echo $file
python plot_zfp.py zfp-0.5.1 $tol 20
echo DONE
done



