#!/bin/sh
# Round-86 final-tip standing sweeps (attempt 3, TameshiR86a3), run at the
# lane tip this receipt names. Each block prints the instrument's own verdict
# line and its exit code captured without a pipeline.
set -u
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
cd "$L" || exit 1
REV=$(git rev-parse refs/heads/master)
S=${S:-/fast/scratch/hyaku/tameshi-r86/l1/final}
mkdir -p "$S"
echo "REV=$REV"

run() {
  name=$1; shift
  "$@" > "$S/$name.out" 2>&1
  rc=$?
  tail -1 "$S/$name.out"
  printf '%s_EXIT=%s\n' "$name" "$rc"
}

echo "=== selfstate (doc figures) ==="
run selfstate python3 -I -B -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --manifest-rev "$REV" --doc-rev "$REV"
echo "=== selfstate pin audit ==="
run pins python3 -I -B -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --pin-audit --pin-rev "$REV"
echo "=== registry figures ==="
run registry python3 -I -B -X utf8 tools/registry-figure-bind.py --repo . --manifest tools/registry-figure-bind.json
echo "=== defect bind ==="
run defects python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json --manifest-rev "$REV"
echo "=== wave reconcile ==="
run wave python3 -I -X utf8 tools/wave-reconcile.py --repo . --manifest tools/wave-reconcile.json --extra-root fleet=/home/vgpnk/Projects/shokunin
echo "=== additivity ranges ==="
run ranges python3 -I -X utf8 tools/additivity-range.py --repo . --manifest tools/additivity-range.json
echo "=== arm liveness ==="
run arms python3 -I -X utf8 tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json
echo "=== count recheck ==="
run counts python3 -I -X utf8 tools/count-recheck.py --repo . --manifest tools/count-recheck.json
echo "=== pointer recheck ==="
run pointers python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json
echo "=== figure attribution ==="
run attribution python3 -I -X utf8 tools/figure-attribution.py --repo . --manifest tools/figure-attribution.json
echo "=== anchor drift ==="
run anchors python3 -I -X utf8 tools/anchor-drift-sweep.py --repo . --manifest tools/anchor-drift-sweep.json
echo "=== receipt bytes bind ==="
run receipts python3 -I -B -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence
echo "=== capability census ==="
run census python3 -I -X utf8 tools/capability-census.py --repo . --rev "$REV"
echo "=== frozen C1 counter (real instrument) ==="
rm -rf "$S/c1"; mkdir -p "$S/c1"
run c1 python3 -I .ufo/evidence/round-86/measure.py --repo . --rev "$REV" --work "$S/c1"
echo "=== coldread no-harm precheck (floor d10a9c66 -> cand REV) ==="
run coldread python3 -I -B -X utf8 tools/coldread-precheck-portable.py --repo . --floor d10a9c66d6181cddcad52cdbffd672beb886ff6c --cand "$REV" --work "$S/coldread" --out "$S/coldread.json"
echo "=== sources census (fleet root) ==="
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi > "$S/census-sources.out" 2>&1
printf 'sources_census_EXIT=%s\n' "$?"
tail -1 "$S/census-sources.out"
