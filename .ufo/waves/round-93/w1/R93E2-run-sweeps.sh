#!/bin/bash
# R93E2 no-harm baseline sweeps: base vs landing clones
set -u
for CLONE in base land; do
  R=/fast/scratch/hyaku/tameshi-r93/R93E2/$CLONE
  cd "$R" || exit 99
  echo "### CLONE=$CLONE HEAD=$(git -C "$R" rev-parse HEAD)"
  run() {
    echo "--- CMD: $*"
    "$@" > "/fast/scratch/hyaku/tameshi-r93/R93E2/$CLONE-$idx.out" 2> "/fast/scratch/hyaku/tameshi-r93/R93E2/$CLONE-$idx.err"
    ec=$?
    echo "exit=$ec"
    echo "stdout tail:"; tail -20 "/fast/scratch/hyaku/tameshi-r93/R93E2/$CLONE-$idx.out"
    echo "stderr tail:"; tail -5 "/fast/scratch/hyaku/tameshi-r93/R93E2/$CLONE-$idx.err"
    echo
  }
  idx=1; run python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json
  idx=2; run python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence/round-78
  idx=3; run python3 -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json
  idx=4; run python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
  idx=5; run python3 -I tools/registry-check.py --root .
done
# hardening-lint against the frozen counter (lane bytes, read-only); run from land clone root context
cd /fast/scratch/hyaku/tameshi-r93/R93E2/land
echo "### hardening-lint (from land; counter extracted at land bytes)"
for args in "tools/hardening-lint.py --selftest" "tools/hardening-lint.py --counter /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-93/c1/measure-v93.py"; do
  echo "--- CMD: python3 -I $args"
  python3 -I $args; echo "exit=$?"
  echo
done
