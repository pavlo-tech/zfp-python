#!/bin/bash
for i in {6..10}
do
iter=1000
tol=1E-$i
file=/zfs/fthpc/plascomcm/inputs/pavlo_runs/plascomcm_run_data/$tol/zfp-0.5.4/$iter.txt
echo $file
python plot_zfp.py zfp-0.5.4 $tol $iter
echo DONE
done



