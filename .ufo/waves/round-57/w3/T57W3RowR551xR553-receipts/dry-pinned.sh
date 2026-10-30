#!/bin/bash
# Scratch replica of .ufo/waves/round-57/dry-c1.sh with the panel PINNED (the lane's measure.py still
# carries PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL). Nothing in the lane is modified: the pin is set
# in a scratch copy of the counter inside a scratch clone.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/T57W3RowR551xR553/dry-pinned
rm -rf "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
git clone -q --shared "$LANE" "$S/c" && git -C "$S/c" rev-parse --show-toplevel >/dev/null || exit 2
HEAD=${DRYBASE:-$(git -C "$LANE" rev-parse master)}
git -C "$S/c" checkout -q --detach "$HEAD"
for p in corpus/routed-defects.json SCORECARD.md .ufo/evidence/round-57; do mkdir -p "$S/c/$(dirname $p)"; rm -rf "$S/c/$p"; cp -r "$LANE/$p" "$S/c/$p"; done
[ -n "${LEDGER:-}" ] && cp "$LEDGER" "$S/c/corpus/routed-defects.json"
OPEN=$(python3 -c "
import json;d=json.load(open('$S/c/corpus/routed-defects.json'))['defects'];print(', '.join(r['id'] for r in d[49:] if r['status']=='open'))")
printf '\n**Planned (round 58):** %s.\n' "$OPEN" >> "$S/c/SCORECARD.md"
git -C "$S/c" add -A && git -C "$S/c" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "dry" && REV=$(git -C "$S/c" rev-parse HEAD)
PANEL_SHA=$(sha256sum "$S/c/.ufo/evidence/round-57/c1/panel.json" | cut -d' ' -f1)
python3 - "$S/c/.ufo/evidence/round-57/c1/measure.py" "$PANEL_SHA" <<'PY'
import sys
p, sha = sys.argv[1], sys.argv[2]
s = open(p, encoding='utf-8').read()
old = "PANEL_SHA256 = 'PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL'"
assert old in s, 'pin marker not found'
open(p, 'w', encoding='utf-8').write(s.replace(old, "PANEL_SHA256 = '%s'" % sha))
print('pinned panel sha256 =', sha)
PY
mkdir -p "$S/w"
python3 "$S/c/.ufo/evidence/round-57/c1/measure.py" --lane "$S/c" --rev "$REV" --work "$S/w" --explain 2>&1 | tail -${1:-60}
