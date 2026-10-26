#!/bin/bash
# Round-48 QUALITY criteria 94-96: each block must FAIL its bad input and pass its good input; prints CRITERION-NN-FALSIFIER-OK.
# Usage: falsifiers.sh   (needs the lane checkout; scratch under $HYAKU_SCRATCH, never /tmp)
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
E=$L/.ufo/evidence/round-48
T=$(mktemp -d -p "${HYAKU_SCRATCH:-/fast/scratch/hyaku}")
trap 'rm -rf -- "$T"' EXIT
# reject_check FILE: every `### Reject` block names a QUALITY criterion or a CORPUS.md rule AND a `Flip:` clause
reject_check() {
python3 - "$1" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=### )', text)
rej = [b for b in blocks if b.startswith('### Reject')]
bad = [b.split('\n', 1)[0] for b in rej if not (re.search(r'QUALITY \d+|CORPUS\.md rule \d+', b) and 'Flip:' in b)]
for b in bad:
    print('WEAK-CITE ' + b)
print('rejects=%d weak=%d' % (len(rej), len(bad)))
sys.exit(1 if (bad or not rej) else 0)
PY
}
# ---- 94: a refusal that cites only a scope line (the round-47 form) is WEAK-CITE; the round-48 lesson's refusals pass
cat > "$T/bad.md" <<'EOF'
### Reject — package entry `r8-predictive-test-selection-cost.md`

Refused: out of province (`PROVINCE.md:14-18`).
EOF
reject_check "$T/bad.md" > "$T/94-bad.out"; b=$?
reject_check "$L/corpus/lessons/round-48.md" > "$T/94-good.out"; g=$?
cat "$T/94-bad.out" "$T/94-good.out"
if [ "$b" = 1 ] && grep -q '^WEAK-CITE' "$T/94-bad.out" && [ "$g" = 0 ]; then echo CRITERION-94-FALSIFIER-OK; else echo CRITERION-94-FALSIFIER-VACUOUS; fi
# ---- 95: the round-47 rows relabelled `runs 3 stable` without re-observation (CTL_B) fail; the controls receipt must show it
R=$E/control/c1-controls.stdout
grep -E '^CTL_B ' "$R"
if grep -E '^CTL_B .*C1_R48(_PARTIAL)?: ' "$R" | grep -qE ' total=[1-9]' && grep -E '^CTL_E .*C1_R48(_PARTIAL)?: ' "$R" | grep -q ' total=0 '; then echo CRITERION-95-FALSIFIER-OK; else echo CRITERION-95-FALSIFIER-VACUOUS; fi
# ---- 96: one statement, one revision, one counter: only the --work placement differs, and P1 differs with it
A=$L/.ufo/evidence/round-47/before/c1-at-freeze.stdout   # --work under /tmp
B=$L/.ufo/evidence/round-47/after/c1.stdout              # --work under /var/tmp
pa=$(grep '^PROFILES hermetic env-differential probe:' "$A" | grep -oE 'P1=[^|]*\|[0-9]+')
pb=$(grep '^PROFILES hermetic env-differential probe:' "$B" | grep -oE 'P1=[^|]*\|[0-9]+')
echo "tmp-work $pa"; echo "var-tmp-work $pb"
if [ -n "$pa" ] && [ -n "$pb" ] && [ "$pa" != "$pb" ] && grep -q 'under_tmp' "$E/calibration/measure.py"; then echo CRITERION-96-FALSIFIER-OK; else echo CRITERION-96-FALSIFIER-VACUOUS; fi
