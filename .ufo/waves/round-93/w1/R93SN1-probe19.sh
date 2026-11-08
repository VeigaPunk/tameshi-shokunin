#!/usr/bin/env bash
# R93SN1 probe 19: does the summary-scan loop prefer a PLANTED receipt over the
# driver's own fresh receipt?  (summary loop: controls-v93.py lines 426-434)
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe19.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
BASE=4a7e259b407d582d2010197f32d7524d6bed5370
probe() { printf 'PROBE %-56s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "T1 plant pos-real.rerun-1.out (forged) BEFORE the run; run only nowork-base"
mkdir -p "$S/o" "$S/w"
printf 'control=pos-real exit=0\nC1_R93_PASS=true\n' > "$S/o/pos-real.rerun-1.out"
probe "T1.planted" "$(cat "$S/o/pos-real.rerun-1.out" | tr '\n' '|')"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/w" --outdir "$S/o" --only nowork-base --jobs 1 >"$S/t1.log" 2>&1
probe "T1.driver-rc" "$?"
probe "T1.summary" "$(cat "$S/o/C1-summary.txt" | tr '\n' '|')"
probe "T1.drivers-own-receipt-written" "$( [ -f "$S/o/nowork-base.out" ] && echo yes || echo no )"

sec "T2 the scan prefers the HIGHEST rerun index over the plain .out"
python3 - <<'PY'
import os
d = os.environ["S"] + "/o"
def scan(outdir, n):
    found = None
    for cand in [n + ".out"] + ["%s.rerun-%d.out" % (n, i) for i in range(1, 50)]:
        p = os.path.join(outdir, cand)
        if os.path.exists(p):
            found = p
    return found
open(os.path.join(d, "nowork-base.out"), "w").write("REAL receipt from the driver\n")
open(os.path.join(d, "nowork-base.rerun-7.out"), "w").write("PLANTED receipt\n")
print("PROBE T2.chosen-for-nowork-base      %s" % os.path.basename(scan(d, "nowork-base")))
PY

sec "T3 planted symlink to an EXISTING file: which receipt is graded?"
mkdir -p "$S/o3" "$S/w3"
printf 'PLANTED VIA SYMLINK\n' > "$S/attacker-target.txt"
ln -s "$S/attacker-target.txt" "$S/o3/nowork-base.out"
python3 -I "$CTRL" --lane "$LANE" --rev "$REV" --base "$BASE" \
  --work "$S/w3" --outdir "$S/o3" --only nowork-base --jobs 1 >"$S/t3.log" 2>&1
probe "T3.driver-rc" "$?"
probe "T3.outdir-listing" "$(ls -A "$S/o3" | tr '\n' ' ')"
probe "T3.attacker-target-content" "$(cat "$S/attacker-target.txt" | tr '\n' '|')"
probe "T3.summary" "$(cat "$S/o3/C1-summary.txt" | tr '\n' '|')"

printf '\n===== done =====\n'
