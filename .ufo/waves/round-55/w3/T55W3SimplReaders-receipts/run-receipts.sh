#!/bin/bash
# T55W3SimplReaders receipts: does the credit rule/binder need one reader per section?
# Runs on git-clone --shared copies only; never touches the lane.
set -u
S=${1:?scratch dir}
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
CL=$S/clone
rm -rf "$CL" "$S/bindout" "$S/tmp"; mkdir -p "$S/tmp"
git clone --shared -q "$LANE" "$CL" && git -C "$CL" checkout -q --detach "$C0"
test "$(git -C "$CL" rev-parse --show-toplevel)" = "$CL" || { echo "NOT-A-CLONE"; exit 2; }
mkdir -p "$CL/.ufo/evidence/round-55/integrate" "$CL/.ufo/evidence/round-55/c1" \
         "$CL/.ufo/waves/round-55/w2" "$CL/.ufo/waves/round-55/w3"
cp "$LANE/.ufo/evidence/round-55/integrate/binder.py" "$CL/.ufo/evidence/round-55/integrate/binder.py"
cp "$LANE/.ufo/evidence/round-55/c1/lost-headings-at-c0.json" "$CL/.ufo/evidence/round-55/c1/"

# ONE scripted author writes three single-heading deliverables + one multi-heading attempt.
python3 - "$S" "$LANE" "$C0" <<'PY'
import importlib.util, json, subprocess, sys
from pathlib import Path
S, LANE, C0 = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
spec = importlib.util.spec_from_file_location('r18', LANE/'.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
secs = {s['heading']: s for s in m.sectionize(
    subprocess.run(['git','-C',str(LANE),'show',C0+':SKILL.md'],capture_output=True).stdout)}
w2, w3 = S/'clone/.ufo/waves/round-55/w2', S/'clone/.ufo/waves/round-55/w3'
heads = ['## Standing rules', '### Gate/probe registry', '### Round-13 gate/probe registry']
for h in heads:
    d = {'heading': h, 'cand': C0, 'section_sha256': secs[h]['sha256'], 'findings': []}
    (w3/('T55W3Test' + str(heads.index(h)) + '.json')).write_text(json.dumps(d))
    (w3/('T55W3Test' + str(heads.index(h)) + '.md')).write_text('# one deliverable\n')
print('sections scanned', len(secs))
print(json.dumps({h: secs[h]['sha256'] for h in heads}, indent=1))
PY
printf '{"heading":["### Gate/probe registry","### Round-13 gate/probe registry"],"cand":"%s","section_sha256":"99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77","findings":[]}\n' "$C0" > "$CL/.ufo/waves/round-55/w3/T55W3TestMulti.json"
printf '# one deliverable naming two headings\n' > "$CL/.ufo/waves/round-55/w3/T55W3TestMulti.md"

B=$CL/.ufo/evidence/round-55/integrate/binder.py
OUT=$CL/.ufo/evidence/round-21/coldread/rekey-r55-test
mkdir -p "$OUT"
echo "=== RUN 1: three single-heading deliverables from one author + one two-heading file"
TMPDIR=$S/tmp python3 "$B" "$CL" "$C0" "$C0" "$OUT" | grep -E "REKEY|REFRESH"; echo "exit=${PIPESTATUS[0]}"

echo "=== RUN 2: add a findings-bearing w2 report for ## Standing rules (as T55W2Read01 has 2 findings)"
printf '{"heading":"## Standing rules","cand":"%s","section_sha256":"acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767","findings":[{"quote":"q1","why":"w1"},{"quote":"q2","why":"w2"}]}\n' "$C0" > "$CL/.ufo/waves/round-55/w2/T55W2TestA.json"
printf '# findings-bearing w2 reader\n' > "$CL/.ufo/waves/round-55/w2/T55W2TestA.md"
TMPDIR=$S/tmp python3 "$B" "$CL" "$C0" "$C0" "$OUT" | grep -E "Standing|REFRESH"; echo "exit=${PIPESTATUS[0]}"

echo "=== RUN 3: adjudicate 2 findings for ## Standing rules"
printf '[{"heading":"## Standing rules","n":2,"id":"FIXTURE","decision":"allow two findings"}]\n' > "$CL/.ufo/evidence/round-55/integrate/resolutions.json"
TMPDIR=$S/tmp python3 "$B" "$CL" "$C0" "$C0" "$OUT" | grep -E "Standing|REFRESH"; echo "exit=${PIPESTATUS[0]}"

echo "=== floor: commit the clone ledger, measure with the round-21 selector"
git -C "$CL" add -A
git -C "$CL" -c user.name=fixture -c user.email=f@x.invalid commit -qm "rekey fixture ledger"
REV=$(git -C "$CL" rev-parse HEAD)
cd "$CL" && TMPDIR=$S/tmp python3 "$CL/.ufo/evidence/round-21/coldread/measure.py" --rev "$REV" \
 | python3 -c 'import json,sys
o=json.load(sys.stdin); c=o["coldread"]
print("rev", o["revision"][:12], "sections", c["sections_total"], "covered", c["sections_covered"], "restraint", o["calibration_restraint_score"])
for s in c["sections"]:
    if s["heading"] in ("## Standing rules","### Gate/probe registry","### Round-13 gate/probe registry"):
        print(" ", s["heading"], "->", s["credited"], s["reason"])'
echo "=== baseline floor at C0 with the unmodified ledger"
cd "$CL" && TMPDIR=$S/tmp python3 "$CL/.ufo/evidence/round-21/coldread/measure.py" --rev "$C0" \
 | python3 -c 'import json,sys
o=json.load(sys.stdin); c=o["coldread"]
print("rev", o["revision"][:12], "sections", c["sections_total"], "covered", c["sections_covered"])'
