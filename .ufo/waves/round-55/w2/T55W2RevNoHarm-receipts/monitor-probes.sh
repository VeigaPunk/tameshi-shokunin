#!/bin/bash
# T55W2RevNoHarm monitor-falsification probes. Reads the no-harm monitor lines
# verbatim against a scratch clone at C0 whose tree is mutated one monitor at a time.
S=/fast/scratch/hyaku/tameshi-r55/T55W2RevNoHarm
C=$S/clone
BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
cd "$C" || exit 2
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "TOPLEVEL MISMATCH"; exit 2; }
git checkout -q -f "$C0" || exit 2
git clean -qfd
export GIT_AUTHOR_NAME=probe GIT_AUTHOR_EMAIL=probe@example.invalid
export GIT_COMMITTER_NAME=probe GIT_COMMITTER_EMAIL=probe@example.invalid
commit() { git add -A >/dev/null && git commit -qm "$1" && git rev-parse --short HEAD; }

echo "=== PROBE A: drop the round's only new source row (S280) ==="
python3 - "$C/corpus/SOURCES.md" <<'EOF'
import re, sys
p = sys.argv[1]
lines = open(p, encoding='utf-8').read().split('\n')
kept = [l for l in lines if not re.match(r'^ {0,3}\| S280 ', l)]
print('dropped_rows=%d' % (len(lines) - len(kept)))
open(p, 'w', encoding='utf-8').write('\n'.join(kept))
EOF
RA=$(commit probe-a-drop-S280)
echo "clone_rev=$RA"
S1=$(git show "$RA:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ')
[ "$S1" = 1 ] && s=ok || s=RED; echo "NOHARM S160-count $S1 $s"
R1=$(git show "$RA:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$R1" -ge 139 ] && s=ok || s=RED; echo "NOHARM registry-rows-not-below-139 $R1 $s"
C0N=$(git show "$BASE:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
C1N=$(git show "$RA:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S[0-9]{3,} \|')
[ "$C1N" -ge "$C0N" ] && s=ok || s=RED; echo "NOHARM sources-not-shrunk base=$C0N rev=$C1N $s"

echo "=== PROBE B: rename one registry row ==="
git checkout -q -f "$C0"; git clean -qfd
python3 - "$C/tools/registry.json" <<'EOF'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d['rows'][0]['name'] = d['rows'][0]['name'] + '-renamed'
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
EOF
RB=$(commit probe-b-rename-row)
echo "clone_rev=$RB renamed_row=$(python3 -c "import json;print(json.load(open('$C/tools/registry.json'))['rows'][0]['name'])")"
N0=$(git show "$BASE:tools/registry.json" | python3 -c 'import json,sys; print(" ".join(sorted(r["name"] for r in json.load(sys.stdin)["rows"])))')
N1=$(git show "$RB:tools/registry.json" | python3 -c 'import json,sys; print(" ".join(sorted(r["name"] for r in json.load(sys.stdin)["rows"])))')
[ "$N0" = "$N1" ] && s=ok || s=RED; echo "NOHARM registry-row-names-unchanged count=$(echo "$N1" | wc -w) $s"

echo "=== PROBE C: touch a tool outside the tools-scope allowlist ==="
git checkout -q -f "$C0"; git clean -qfd
printf '\n# probe: an unlisted tool edit\n' >> "$C/tools/shrink-case.py"
RC=$(commit probe-c-touch-unlisted-tool)
echo "clone_rev=$RC"
T=$(git diff --name-status --no-renames "$BASE" "$RC" -- tools | tr '\t' ':' | tr '\n' ' ')
s=ok; for t in $T; do case "$t" in M:tools/registry.json|M:tools/registry-check.py|M:tools/env-diff.py|M:tools/bash-witness-study.py|M:tools/context-capture.py|M:tools/evidence-disposition.py|M:tools/pin-disposition.py|M:tools/repeat-control.py) ;; *) s=RED;; esac; done
echo "NOHARM tools-scope [${T}] $s"

echo "=== PROBE D: keep the ledger's entry count, destroy every entry ==="
git checkout -q -f "$C0"; git clean -qfd
python3 - "$C/.ufo/evidence/round-21/coldread/ledger.json" <<'EOF'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
n = len(d['entries'])
d['entries'] = [{} for _ in range(n)]   # same count, no content
open(p, 'w').write(json.dumps(d) + '\n')
print('entries_before=%d entries_after=%d' % (n, len(d['entries'])))
EOF
RD=$(commit probe-d-neuter-ledger)
echo "clone_rev=$RD"
L0=$(git show "$BASE:.ufo/evidence/round-21/coldread/ledger.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["entries"]))')
L1=$(git show "$RD:.ufo/evidence/round-21/coldread/ledger.json" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["entries"]))')
[ "$L1" -ge "$L0" ] && s=ok || s=RED; echo "NOHARM ledger-not-shrunk base=$L0 rev=$L1 $s"
CR=$(python3 "$C/.ufo/evidence/round-21/coldread/measure.py" --repo "$C" --rev "$RD" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print("score=%s credited=%d" % (d["calibration_restraint_score"], d["coldread"]["sections_covered"]))')
python3 -c 'import sys; s=dict(kv.split("=") for kv in sys.argv[1].split()); sys.exit(0 if int(s["score"])>=8 and int(s["credited"])>=64 else 1)' "$CR" && s=ok || s=RED; echo "NOHARM coldread-floor $CR $s"

echo "=== PROBE E: delete the S160 row ==="
git checkout -q -f "$C0"; git clean -qfd
python3 - "$C/corpus/SOURCES.md" <<'EOF'
import re, sys
p = sys.argv[1]
lines = open(p, encoding='utf-8').read().split('\n')
open(p, 'w', encoding='utf-8').write('\n'.join(l for l in lines if not re.match(r'^ {0,3}\| S160 ', l)))
EOF
RE=$(commit probe-e-drop-S160)
S1=$(git show "$RE:corpus/SOURCES.md" | grep -cE '^ {0,3}\| S160 ')
[ "$S1" = 1 ] && s=ok || s=RED; echo "NOHARM S160-count $S1 $s"
git checkout -q -f "$C0"; git clean -qfd
echo "restored clone rev=$(git rev-parse --short HEAD)"
