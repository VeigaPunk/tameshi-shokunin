#!/usr/bin/env bash
# T92SN1 probe 4 — can the driver's summary count a receipt the run never wrote?
#
# H4: the driver re-derives `results` from every *.out file already present in
#     --outdir (controls-v92.py:355-362).  --outdir is not required to be empty
#     and is never cleaned, so a stale/foreign receipt is scored MATCH and
#     counted in states=/matched=.  The plan asserts "a receipt the run never
#     wrote cannot be counted as matched".
#
# Demonstration: pre-seed the outdir with a hand-written receipt for a state
# the run will NOT execute (--only selects nothing), then read the driver's
# own summary derivation.  Everything is under scratch; no lane/fleet write.
set -u
S=/fast/scratch/hyaku/tameshi-r92/T92SN1
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
W="$S/staleprobe"
rm -rf "$W"; mkdir -p "$W/work" "$W/out"
cd "$W" || exit 1

# hand-written receipt, exactly the shape the summary parser expects
cat > "$W/out/pos-real.out" <<'EOF'
control=pos-real clone_rev=deadbeef parent=84904d41
exit=0
C1_R92_PASS=true
EOF
echo "seeded outdir:"; ls -1 "$W/out"

echo "=== run the driver with --only (a state that does not exist) --states-only ==="
python3 -I "$LANE/.ufo/evidence/round-92/c1/controls-v92.py" \
  --lane "$LANE" --rev 84904d41a31fb5ddde49e8bf1ad6fc2b489671a0 \
  --base 63172b9889475103aeca976d37389d204010dd11 \
  --work "$W/work" --outdir "$W/out" --only no-such-state --states-only 2>&1 | tail -8
echo "driver rc=$?"
echo "=== driver-written summary ==="
cat "$W/out/C1-summary.txt" 2>/dev/null
echo "=== files in outdir after the run ==="
ls -1 "$W/out"
