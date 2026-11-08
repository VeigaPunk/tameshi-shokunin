#!/usr/bin/env bash
# T92SN1 probe 2 — ambient GIT_DIR redirect against the REAL control driver.
#
# All writes stay under scratch: the "lane" the driver is pointed at is a
# scratch COPY of the lane repo (git clone --shared <lane>), and GIT_DIR points
# at that scratch copy's .git. Nothing touches the real lane or fleet repo.
#
# Hypothesis (H1): the driver's `git rev-parse --show-toplevel` assertion does
#   NOT defend against an ambient GIT_DIR, because with GIT_DIR set git uses
#   that repository while --show-toplevel reports the *current directory*.
#   Consequence: the driver's mutating calls (`add`, `commit`, `replace`) land
#   in the GIT_DIR repository instead of the asserted fixture clone — i.e. the
#   2026-11-06 fleet-root class (`git -C ""` fell back to the fleet root).
set -u
S=/fast/scratch/hyaku/tameshi-r92/T92SN1
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
W="$S/gitdirprobe"
mkdir -p "$W"
cd "$W" || exit 1
rm -rf lanecopy work out
git clone -q --shared "$LANE" lanecopy
git -C lanecopy checkout -q --detach 84904d41a31fb5ddde49e8bf1ad6fc2b489671a0
HEAD_BEFORE=$(git -C lanecopy rev-parse HEAD)
REFS_BEFORE=$(git -C lanecopy for-each-ref --format='%(refname)' | sort | md5sum)
echo "lanecopy HEAD before: $HEAD_BEFORE"

mkdir -p work out
echo "=== run driver with ambient GIT_DIR=<scratch lane copy>/.git ==="
GIT_DIR="$W/lanecopy/.git" timeout 120 python3 -I "$LANE/.ufo/evidence/round-92/c1/controls-v92.py" \
  --lane "$W/lanecopy" --rev 84904d41a31fb5ddde49e8bf1ad6fc2b489671a0 \
  --base 63172b9889475103aeca976d37389d204010dd11 \
  --work "$W/work" --outdir "$W/out" --only pos-real --jobs 1 2>&1 | tail -15
echo "driver rc=$?"

echo "=== did a commit land in the GIT_DIR repo (the lane copy)? ==="
git -C lanecopy log --oneline | head -5
echo "HEAD after : $(git -C lanecopy rev-parse HEAD)"
echo "changed: $([ "$(git -C lanecopy rev-parse HEAD)" != "$HEAD_BEFORE" ] && echo YES-COMMIT-LANDED || echo no)"
echo "=== replace refs created in the GIT_DIR repo? ==="
echo "lanecopy replace -l: [$(git -C lanecopy replace -l | tr '\n' ' ')]"
echo "=== refs md5 before/after ==="
echo "$REFS_BEFORE"
git -C lanecopy for-each-ref --format='%(refname)' | sort | md5sum
echo "=== lanecopy working tree status (index written?) ==="
git -C lanecopy status --porcelain | head -10
echo "=== scratch fixture clones (should have been the intended target) ==="
find "$W/work" -maxdepth 2 -name '.git' -type d 2>/dev/null | head -10
echo "=== driver receipts ==="
ls -1 "$W/out" 2>/dev/null | head -10
