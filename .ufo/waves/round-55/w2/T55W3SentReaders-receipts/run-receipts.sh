#!/usr/bin/env bash
# T55W3SentReaders — runnable receipt driver (round 55, wave 3).
# Recomputes the 18 section shas with the frozen round-18 sectionizer, audits
# the 18 reader deliverables, and exercises the round-55 re-key binder against
# the lane's own adjudication file and against the round-54 schema witness.
# Writes nothing in the lane: every git mutation happens in a --shared clone
# under HYAKU_SCRATCH.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S=$HYAKU_SCRATCH/tameshi-r55/T55W3SentReaders
R=$LANE/.ufo/waves/round-55/w2/T55W3SentReaders-receipts
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S"

echo "## 01 — the 18 lost headings' section shas at C0 (frozen round-18 sectionizer)"
python3 "$R/shas.py" | tee "$R/01-section-sha-recompute.txt"

echo
echo "## 02 — deliverable audit (heading / cand / sha / findings shape)"
python3 "$R/audit.py" | tee "$R/02-deliverable-audit.json"

echo
echo "## 03 — findings quotes resolve inside the section they are bound to"
python3 "$R/quotes.py" | tee "$R/03-quote-presence.txt"

echo
echo "## 04 — binder against the lane's adjudication file (worktree and HEAD)"
git clone -q --shared "$LANE" "$S/clone"
git -C "$S/clone" checkout -q "$C0"
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone" || { echo "clone toplevel mismatch"; exit 1; }
mkdir -p "$S/clone/.ufo/evidence/round-55/integrate" \
         "$S/clone/.ufo/waves/round-55/w2" "$S/clone/.ufo/waves/round-55/w3"
cp "$LANE"/.ufo/evidence/round-55/integrate/{binder.py,resolutions.json} \
   "$S/clone/.ufo/evidence/round-55/integrate/"
cp "$LANE"/.ufo/evidence/round-55/c1/lost-headings-at-c0.json \
   "$S/clone/.ufo/evidence/round-55/c1/"
cp "$LANE"/.ufo/waves/round-55/w2/T55W3R*.json "$LANE"/.ufo/waves/round-55/w2/T55W3R*.md \
   "$S/clone/.ufo/waves/round-55/w2/" 2>/dev/null
cp "$LANE"/.ufo/waves/round-55/w3/T55W3R*.json "$LANE"/.ufo/waves/round-55/w3/T55W3R*.md \
   "$S/clone/.ufo/waves/round-55/w3/" 2>/dev/null
mkdir -p "$S/tmp"
for arm in worktree HEAD; do
  if [ "$arm" = HEAD ]; then
    git -C "$LANE" show HEAD:.ufo/evidence/round-55/integrate/resolutions.json \
      > "$S/clone/.ufo/evidence/round-55/integrate/resolutions.json"
  fi
  echo "--- arm: resolutions.json as at $arm"
  rm -rf "$S/out"; mkdir "$S/out"
  TMPDIR="$S/tmp" python3 "$S/clone/.ufo/evidence/round-55/integrate/binder.py" \
    "$S/clone" "$C0" "$C0" "$S/out"
  echo "exit=$?"
done | tee "$R/04-binder-crash.txt"

echo
echo "## 05 — binder with the round-54 adjudication schema (heading+n rows)"
cp "$LANE/.ufo/evidence/round-54/integrate/resolutions.json" \
   "$S/clone/.ufo/evidence/round-55/integrate/resolutions.json"
rm -rf "$S/out"; mkdir "$S/out"
TMPDIR="$S/tmp" python3 "$S/clone/.ufo/evidence/round-55/integrate/binder.py" \
  "$S/clone" "$C0" "$C0" "$S/out" > "$S/b5.out" 2>&1
echo "exit=$?"
cat "$S/b5.out" | tee "$R/05-binder-round54-schema.txt"

echo
echo "## 06 — worktree-only phrases (post-C0 F1/F2 repairs) in reader artifacts"
grep -rn "the token this tool actually prints\|REPEAT_CONTROL: setup_error\|wave-2 F1\|wave-2 F2" \
  "$LANE"/.ufo/waves/round-55/w2/T55W3R* "$LANE"/.ufo/waves/round-55/w3/T55W3R* \
  > "$S/g6.out" 2>&1
echo "grep-exit=$? (1 = no match)"
cat "$S/g6.out" | tee "$R/06-worktree-read-sweep.txt"

echo
echo "## 07 — every reader JSON has its report next to it (binder's md check)"
cat > "$S/pairing.py" <<'PY'
import os, re, sys
lane = sys.argv[1]
for d in ('w2', 'w3'):
    p = os.path.join(lane, '.ufo/waves/round-55', d)
    for f in sorted(os.listdir(p)):
        if re.fullmatch(r'T55W3R\d\d\.json', f):
            md = f[:-5] + '.md'
            print(d, f, 'md_next_to_json=%s' % os.path.exists(os.path.join(p, md)))
PY
python3 "$S/pairing.py" "$LANE" | tee "$R/07-md-pairing.txt"

echo
echo "## 08 — credit at C0 with the round-21 ledger: the lost set is exactly 18"
TMPDIR="$S/tmp" python3 "$LANE/.ufo/evidence/round-18/measure.py" --repo "$LANE" --rev "$C0" \
  --ledger-rev "$C0:.ufo/evidence/round-21/coldread/ledger.json" > "$S/r18-c0-r21ledger.json"
cat > "$S/lostset.py" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
c = d['coldread']
lost = set(json.load(open(sys.argv[2])))
unc = set(c['uncovered_headings'])
print('sections_covered=%d/%d credited=%d' % (c['sections_covered'], c['sections_total'], c['reasons']['credited']))
print('uncovered=%d lost-headings-at-c0.json=%d set_equal=%s' % (len(unc), len(lost), unc == lost))
print('uncovered minus lost:', sorted(unc - lost))
print('lost minus uncovered:', sorted(lost - unc))
PY
python3 "$S/lostset.py" "$S/r18-c0-r21ledger.json" \
  "$LANE/.ufo/evidence/round-55/c1/lost-headings-at-c0.json" | tee "$R/08-credit-at-c0-46of64.txt"
