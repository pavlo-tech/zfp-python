#!/bin/bash
for t in {1..5}
do
for d in {4.1,5.1,5.4}
do

# cycle_zfp parameters
f=RocFlo-CM.00015000.q
inp=./lossy/gold/$f
out=./lossy/$d/$t/$f
tol=1E-$t
cyc=./zfp-0.$d/examples/simple.dll

echo python cycle_zfp.py $inp $out $tol 1 $cyc
python cycle_zfp.py $inp $out $tol 1 $cyc

#diffsim parameters
diffsim=/zfs/fthpc/plascomcm/utils/PLOT3D/diffSim.py
gold=./lossy/gold
lossy=./lossy/$d/$t
result=./results/$d/$t

python $diffsim $gold $lossy $result

done
done





