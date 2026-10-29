#!/usr/bin/env bash
# T57W2RevForecast — the three defect fixtures, reproduced end to end.
# Run from anywhere; writes only under $HYAKU_SCRATCH and /tmp.
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r57/T57W2RevForecast
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=5e3569969b532310d2b8a3d130901757a3df356b
OLD=$LANE/tools/cold-read-forecast.py
NEW=$LANE/.ufo/waves/round-57/w2/T57W2RevForecast/stage/tools/cold-read-forecast.py
MON=$LANE/.ufo/evidence/round-21/coldread/measure.py
mkdir -p "$S"
export TMPDIR="$S"

mk() {  # mk NAME  -> prints the fixture dir; the caller then edits + commits
  D="$S/fx-$1"; rm -rf "$D"
  git clone --shared -q "$LANE" "$D"
  git -C "$D" checkout --detach "$BASE" >/dev/null 2>&1
  [ "$(git -C "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" ] || {
    echo "toplevel mismatch" >&2; exit 1; }
  echo "$D"
}

commit() { git -C "$1" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -am "$2"; }

echo "=== fx1: a heading ADDED to SKILL.md ==="
D=$(mk 1)
printf '\n### Brand new section added by round 57\n\nbody text\n' >> "$D/SKILL.md"
commit "$D" "add SKILL heading"; R=$(git -C "$D" rev-parse HEAD)
echo "--- monitor (ground truth) ---"
python3 "$MON" --repo "$D" --rev "$R" --explain 2>/dev/null |
  python3 -c "import json,sys;d=json.load(sys.stdin);c=d['coldread'];print('covered',c['sections_covered'],'/',c['sections_total'],'uncovered',c['uncovered_headings'])"
echo "--- SHIPPED tool ---"; python3 "$OLD" --lane "$D" --rev "$BASE" --diff-to "$R" --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('readers',d['readers'],[l['heading'] for l in d['lost']])" || echo "exit=$?"
echo "--- STAGED tool ---";   python3 "$NEW" --lane "$D" --rev "$BASE" --diff-to "$R" --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('readers',d['readers'],[l['heading'] for l in d['lost']])"

echo
echo "=== fx3: the trailing SKILL.md section REMOVED ==="
D=$(mk 3)
python3 - "$D/SKILL.md" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read(); i=s.index('### Round-26 gate/probe registry')
open(p,'w').write(s[:i])
EOF
commit "$D" "delete SKILL tail"; R=$(git -C "$D" rev-parse HEAD)
echo "--- monitor (ground truth) ---"
python3 "$MON" --repo "$D" --rev "$R" --explain 2>/dev/null |
  python3 -c "import json,sys;d=json.load(sys.stdin);c=d['coldread'];print('covered',c['sections_covered'],'/',c['sections_total'],'uncovered',c['uncovered_headings'])"
echo "--- SHIPPED tool ---"; python3 "$OLD" --lane "$D" --rev "$BASE" --diff-to "$R" --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('readers',d['readers'],[l['heading'] for l in d['lost']])"
echo "--- STAGED tool ---";   python3 "$NEW" --lane "$D" --rev "$BASE" --diff-to "$R" --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('readers',d['readers'],[l['heading'] for l in d['lost']])"

echo
echo "=== fx4: a mid-file SKILL.md section REMOVED ==="
D=$(mk 4)
python3 - "$D/SKILL.md" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
a=s.index('### Round-13 gate/probe registry'); b=s.index('\n### ', a+5)
open(p,'w').write(s[:a]+s[b+1:])
EOF
commit "$D" "delete SKILL section"; R=$(git -C "$D" rev-parse HEAD)
echo "--- monitor (ground truth) ---"
python3 "$MON" --repo "$D" --rev "$R" --explain 2>/dev/null |
  python3 -c "import json,sys;d=json.load(sys.stdin);c=d['coldread'];print('covered',c['sections_covered'],'/',c['sections_total'],'uncovered',c['uncovered_headings'])"
echo "--- SHIPPED tool ---"; python3 "$OLD" --lane "$D" --rev "$BASE" --diff-to "$R" --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('readers',d['readers'],[l['heading'] for l in d['lost']])"
echo "--- STAGED tool ---";   python3 "$NEW" --lane "$D" --rev "$BASE" --diff-to "$R" --json | python3 -c "import json,sys;d=json.load(sys.stdin);print('readers',d['readers'],[l['heading'] for l in d['lost']])"

echo
echo "=== fx2: SKILL.md DELETED at the target rev ==="
D=$(mk 2)
git -C "$D" rm -q SKILL.md; commit "$D" "delete SKILL"; R=$(git -C "$D" rev-parse HEAD)
echo "--- SHIPPED tool ---"; python3 "$OLD" --lane "$D" --rev "$BASE" --diff-to "$R" >/dev/null 2>"$S/fx2-old.err"; echo "exit=$?"; tail -3 "$S/fx2-old.err"
echo "--- STAGED tool ---";   python3 "$NEW" --lane "$D" --rev "$BASE" --diff-to "$R" >/dev/null 2>"$S/fx2-new.err"; echo "exit=$?"; tail -3 "$S/fx2-new.err"

echo
echo "=== selftest: SHIPPED vs STAGED ==="
echo -n "SHIPPED: "; python3 "$OLD" --selftest 2>&1 | tail -1
echo -n "STAGED:  "; python3 "$NEW" --selftest 2>&1 | tail -1
