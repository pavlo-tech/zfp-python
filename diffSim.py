import os
import sys



prefix = "RocFlo-CM"
suffix = ".q"
#BW#diffSoln = "/u/sciteam/jccalho2/plascomcm/utils/PLOT3D/diffSoln "
diffSoln = "/zfs/fthpc/plascomcm/utils/PLOT3D/diffsoln "


#verify input
if len(sys.argv) != 4:
    print "USAGE:\n\npython " + sys.argv[0] + " /gold/dir/ /lossy/dir/ /result/dir/"
    sys.exit(1)


# assumes dirs are made
goldDir = sys.argv[1]
lossyDir = sys.argv[2]
resultDir = sys.argv[3]

files = [f for f in os.listdir(goldDir) if os.path.isfile(os.path.join(goldDir, f))]
files.sort()


#diff the two simulations
for f in files:
    if prefix in f and f.endswith(suffix):
        print f
        print diffSoln + os.path.join(lossyDir, f) + " " + os.path.join(goldDir, f) + " " + os.path.join(resultDir, f)
        os.system(diffSoln + os.path.join(lossyDir, f) + " " + os.path.join(goldDir, f) + " " + os.path.join(resultDir, f))

