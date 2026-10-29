#!/bin/bash
# L1 dry run of the C1 counter on the working tree in a scratch clone (never commits in the lane).
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/L1-dry; rm -rf "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
git clone -q --shared "$LANE" "$S/c" && git -C "$S/c" rev-parse --show-toplevel >/dev/null || exit 2
HEAD=${DRYBASE:-$(git -C "$LANE" rev-parse master)}
git -C "$S/c" checkout -q --detach "$HEAD"
for p in corpus/routed-defects.json SCORECARD.md .ufo/evidence/round-57; do mkdir -p "$S/c/$(dirname $p)"; rm -rf "$S/c/$p"; cp -r "$LANE/$p" "$S/c/$p"; done
[ -n "${LEDGER:-}" ] && cp "$LEDGER" "$S/c/corpus/routed-defects.json"
OPEN=$(python3 -c "
import json;d=json.load(open('$S/c/corpus/routed-defects.json'))['defects'];print(', '.join(r['id'] for r in d[49:] if r['status']=='open'))")
printf '\n**Planned (round 58):** %s.\n' "$OPEN" >> "$S/c/SCORECARD.md"
git -C "$S/c" add -A && git -C "$S/c" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "dry" && REV=$(git -C "$S/c" rev-parse HEAD)
mkdir -p "$S/w"; python3 "$S/c/.ufo/evidence/round-57/c1/measure.py" --lane "$S/c" --rev "$REV" --work "$S/w" --explain 2>&1 | tail -${1:-40}
