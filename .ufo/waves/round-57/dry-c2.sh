#!/bin/bash
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/L1-dry2; rm -rf "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
git clone -q --shared "$LANE" "$S/c" && git -C "$S/c" rev-parse --show-toplevel >/dev/null || exit 2
git -C "$S/c" checkout -q --detach "$(git -C "$LANE" rev-parse master)"
rm -rf "$S/c/.ufo/evidence/round-57"; cp -r "$LANE/.ufo/evidence/round-57" "$S/c/.ufo/evidence/round-57"
git -C "$S/c" add -A && git -C "$S/c" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m dry && REV=$(git -C "$S/c" rev-parse HEAD)
mkdir -p "$S/w"; TMPDIR="$S/w" python3 "$S/c/.ufo/evidence/round-57/c2/measure.py" --lane "$S/c" --rev "$REV" --work "$S/w/x" --explain 2>&1 | tail -${1:-30}
