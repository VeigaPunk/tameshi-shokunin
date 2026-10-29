#!/bin/bash
# Reproduces every attempt in T57W2SentC1. Each run builds a fresh scratch clone at C0 (under $S/a), commits the
# attacker ledger, and scores it with the lane's amended counter (or the candidate arm copy when ARMS=1).
set -u
S=/fast/scratch/hyaku/tameshi-r57/T57W2SentC1; R="$1"; cd "$S" || exit 2
export TAIL=400
run(){ name=$1; shift; { echo "### $name"; "$@" 2>&1; } > "$R/$name.stdout"; echo "$name exit=$?"; }
run honest-baseline-unpatched python3 h/armrun.py honest
run A1-allfixed-probe-forgedpanel python3 h/armrun.py A1
run A1t-allfixed-probe-truthpanel python3 h/A.py A1t
run A2-6probe-45open-forgedpanel python3 h/armrun.py A2
run A2t-6probe-45open-truthpanel python3 h/A.py A2t
run B-namedpath-prose-noid-forgedpanel python3 h/armrun.py B
run C-sab-declined-guess-forgedpanel python3 h/BCDE.py C
run D-planned-prose-fixed-forgedpanel python3 h/BCDE.py D
run E-dotslash-open-selfcite-forgedpanel python3 h/armrun.py E
ARMS=1 run honest-arms python3 h/armrun.py honest
ARMS=1 run A1-arms python3 h/armrun.py A1
ARMS=1 run A2-arms python3 h/armrun.py A2
ARMS=1 run B-arms python3 h/armrun.py B
ARMS=1 run B3-copy3words-arms python3 h/armrun.py B3
ARMS=1 run E-arms python3 h/armrun.py E
run arms-false-rejects-analysis python3 h/arms.py
run arms2-probe-stop-analysis python3 h/arms2.py
echo MATRIX_DONE
