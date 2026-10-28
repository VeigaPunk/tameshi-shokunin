#!/usr/bin/env bash
# Round-56 probe: the frozen C2 counter's arm 6 (`docs`) reads SOURCES.md status
# from cells[8], but every registry row carries status at cells[7]. Same bytes,
# one index changed: does the note arm pass?
# All commits happen in $C (a scratch clone); the lane is never written.
set -u
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
E=.ufo/evidence/round-56
BASE=${HYAKU_SCRATCH:?}/tameshi-r56/T56W1ScribeKnowledge
D=$(mktemp -d "$BASE/probe.XXXXXX") || exit 1
trap 'rm -rf -- "$D"' EXIT
for v in $(env | grep -o '^GIT_[A-Z_]*' ); do unset "$v"; done
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=f@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=f@example.invalid

git clone --shared --quiet "$L" "$D/clone" || exit 1
C=$D/clone
test "$(git -C "$C" rev-parse --show-toplevel)" = "$C" || { echo "TOPLEVEL MISMATCH"; exit 1; }
git -C "$C" checkout --quiet --detach c3e2ca9f020776b3d66c7af854fb82c834674fcf || exit 1

# the four docs surfaces arm 6 reads, minimally satisfied
cat >> "$C/corpus/QUALITY.md" <<'EOF'

### Probe 107 (scratch) — receipt binding
Run `tools/receipt-revision-gate.py`; a drifting receipt is refused `RECEIPT_REV_CONTENT_DRIFT`.
EOF
printf '\n<!-- probe: receipt-revision-gate binds a receipt to its revision -->\n' >> "$C/SKILL.md"
python3 - "$C/tools/registry.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
d['rows'].append({"name":"receipt-revision-gate-probe","kind":"gate",
  "argv":["python3","tools/receipt-revision-gate.py","--selftest"],
  "expect":{"exit":0},"timeout_s":120,
  "source":"tools/receipt-revision-gate.py","status":"active","tags":["receipt-binding"]})
json.dump(d,open(p,'w'),indent=1)
PY
cp "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/receipt-revision-binding.md.draft" \
   "$C/corpus/knowledge/receipt-revision-binding.md"
git -C "$C" add -A >/dev/null
git -C "$C" commit -q -m 'probe: docs surfaces for C2 arm 6' >/dev/null
REV=$(git -C "$C" rev-parse HEAD)
echo "REV=$REV"

git -C "$C" show "$REV:$E/c2/measure.py" > "$D/measure-frozen.py"
sed 's/and cells\[8\] == .mined./and cells[7] == "mined"/' "$D/measure-frozen.py" > "$D/measure-cells7.py"
echo "--- frozen counter bytes unchanged except the index:"
diff -u "$D/measure-frozen.py" "$D/measure-cells7.py" | sed -n '1,20p'

mkdir -p "$D/w-frozen" "$D/w-cells7"
echo "=== A. frozen counter (cells[8])"
TMPDIR=$D python3 "$D/measure-frozen.py" --lane "$C" --rev "$REV" --work "$D/w-frozen" --explain 2>&1 | tail -8
echo "=== B. same bytes with cells[7]"
TMPDIR=$D python3 "$D/measure-cells7.py" --lane "$C" --rev "$REV" --work "$D/w-cells7" --explain 2>&1 | tail -8
