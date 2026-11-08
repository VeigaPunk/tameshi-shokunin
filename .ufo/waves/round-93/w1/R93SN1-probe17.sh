#!/usr/bin/env bash
# R93SN1 probe 17: last two path-resolution instances.
#   S1 counter --repo "" from the FLEET ROOT cwd: is the fleet root read as the lane?
#   S2 driver --rev "": does it extract the counter from the INDEX, not the commit?
set -u
S="$(mktemp -d -p /fast/scratch/hyaku/tameshi-r93/R93SN1 probe17.XXXXXX)"
trap 'rm -rf -- "$S"' EXIT
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
CTRL="$LANE/.ufo/evidence/round-93/c1/controls-v93.py"
MEAS="$LANE/.ufo/evidence/round-93/c1/measure-v93.py"
REV=855f0c1c59ee2af7f184d8de62d02cdd576eb94e
probe() { printf 'PROBE %-56s %s\n' "$1" "${2:-}"; }
sec() { printf '\n===== %s =====\n' "$1"; }

sec "S1 counter --repo '' with cwd = the FLEET ROOT"
mkdir -p "$S/wS1"
( cd "$FLEET" && python3 -I "$MEAS" --repo "" --rev "$REV" --work "$S/wS1" ) >"$S/s1.log" 2>&1
probe "S1.rc" "$?"
probe "S1.first-line" "$(head -1 "$S/s1.log")"
probe "S1.meaning" "realpath('') == cwd, so the FLEET ROOT was passed to git -C as the lane"

sec "S2 driver --rev '' : is the counter blob taken from the INDEX?"
git clone -q --shared --no-checkout "$LANE" "$S/lane" 2>/dev/null
git -C "$S/lane" checkout -q --detach "$REV" 2>/dev/null
# stage a MODIFIED counter in the index (working tree matches, but the INDEX differs)
python3 - "$S/lane/.ufo/evidence/round-93/c1/measure-v93.py" <<'PY'
import sys
p = sys.argv[1]
b = open(p, "rb").read()
open(p, "wb").write(b + b"\n# INDEX-ONLY-MARKER-S2\n")
PY
git -C "$S/lane" add .ufo/evidence/round-93/c1/measure-v93.py
probe "S2.index-counter-has-marker" "$(git -C "$S/lane" show :.ufo/evidence/round-93/c1/measure-v93.py | grep -c 'INDEX-ONLY-MARKER-S2')"
probe "S2.commit-counter-has-marker" "$(git -C "$S/lane" show "$REV:.ufo/evidence/round-93/c1/measure-v93.py" | grep -c 'INDEX-ONLY-MARKER-S2')"
mkdir -p "$S/wS2" "$S/oS2"
python3 -I "$CTRL" --lane "$S/lane" --rev "" --base "$REV" \
  --work "$S/wS2" --outdir "$S/oS2" --only nowork-base --jobs 1 >"$S/s2.log" 2>&1
probe "S2.driver-rc" "$?"
probe "S2.driver-saw-the-INDEX-counter" "$(grep -m1 'CONTROL_INSTRUMENT' "$S/s2.log")"
probe "S2.expected-if-commit" "18903602aa040b7e258fd6c81491cfee4ea7bb0575784fe27e351587fe094c2d"
probe "S2.receipt-exit" "$(grep -m1 '^exit=' "$S/oS2/nowork-base.out" 2>/dev/null)"

sec "S3 make-pins.py write mode: does it overwrite the FROZEN pins.json in place?"
git clone -q --shared --no-checkout "$LANE" "$S/lane3" 2>/dev/null
git -C "$S/lane3" checkout -q --detach "$REV" 2>/dev/null
before=$(sha256sum "$S/lane3/.ufo/evidence/round-93/c1/pins.json" | cut -d' ' -f1)
python3 -I "$LANE/.ufo/evidence/round-93/c1/make-pins.py" --lane "$S/lane3" --rev "$REV" >/dev/null 2>&1
after=$(sha256sum "$S/lane3/.ufo/evidence/round-93/c1/pins.json" | cut -d' ' -f1)
probe "S3.pins-before" "${before:0:16}"
probe "S3.pins-after" "${after:0:16}"
probe "S3.wrote-in-place-without-a-check" "$( [ "$before" = "$after" ] && echo 'bytes identical here, but the write happened in place with NO --check gate' || echo CHANGED )"
probe "S3.check-mode-refuses-drift" "$(python3 -I "$LANE/.ufo/evidence/round-93/c1/make-pins.py" --lane "$S/lane3" --rev "$REV" --check 2>&1 | grep -m1 PINS_CHECK)"

printf '\n===== done =====\n'
