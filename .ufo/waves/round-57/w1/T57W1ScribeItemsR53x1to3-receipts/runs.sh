#!/bin/bash
S=/fast/scratch/hyaku/tameshi-r57/T57W1ScribeItemsR53x1to3; C=$S/clone; R=5e3569969b532310d2b8a3d130901757a3df356b; F88=88afa9415454
export TMPDIR=$S/tmp
( python3 $S/c1r53.py --lane $C --rev $F88 --work $S/runs/c1-88 --explain > $S/runs/c1-88.stdout 2> $S/runs/c1-88.stderr; echo $? > $S/runs/c1-88.exit ) &
( python3 $S/c2r53.py --lane $C --rev $F88 --work $S/runs/c2-88 --explain > $S/runs/c2-88.stdout 2> $S/runs/c2-88.stderr; echo $? > $S/runs/c2-88.exit ) &
( python3 $S/c1r53-patched.py --lane $C --rev $F88 --work $S/runs/c1p-88 --explain > $S/runs/c1p-88.stdout 2> $S/runs/c1p-88.stderr; echo $? > $S/runs/c1p-88.exit ) &
( python3 $S/bf-patched.py $C $F88 $R $S/runs/bf > $S/runs/bf.stdout 2> $S/runs/bf.stderr; echo $? > $S/runs/bf.exit ) &
wait
echo ALLDONE > $S/runs/done
