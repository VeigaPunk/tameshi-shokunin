#!/bin/bash
# Round-56 controls. Usage: controls.sh LANE BASE PIN FREEZE OUTDIR
#   Phase A (before the deciding run): every control must reach its pre-registered verdict.
#   Phase B (after the ledger bind): the positive controls are scored AT the revision they
#   certify (PIN, the content-final revision) in a fresh clone - the round-54 lesson, where
#   CTL_POS_c1 was scored at the freeze and reported as a pass it could not be.
# Every CTL line names the revision the counter printed; CTL_MISMATCH means the counter did
# not reach the pre-registered boolean and the round must stop.
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r56/controls, removed on exit.
set -u
LANE=$1; BASE=$2; PIN=$3; FREEZE=$4; OUT=$5
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r56/controls
E=.ufo/evidence/round-56
cd "$LANE" || exit 2
rm -rf "$SCR"; mkdir -p "$SCR" "$OUT"; trap 'rm -rf -- "$SCR"' EXIT; export TMPDIR="$SCR"
C1="$E/c1/measure.py"; C2="$E/c2/measure.py"
A_ok=0; A_n=0

emit() { # emit NAME EXPECTED ACTUAL VERDICT_LINE
  local name=$1 want=$2 got=$3 line=$4
  echo "CTL $name $line"
  if [ "$want" = "$got" ]; then echo "CTL_MATCH $name expected=$want actual=$got"; echo 1 >> "$SCR/matches"
  else echo "CTL_MISMATCH $name expected=$want actual=$got"; fi
}

verdict_of() { grep -oE 'C[12]_R56_PASS=(true|false)' | tail -1 | cut -d= -f2; }

clone_at() { # clone_at DIR REV
  git clone --quiet --shared "$LANE" "$1" || return 2
  git -C "$1" checkout --quiet --detach "$2" || return 2
  [ "$(git -C "$1" rev-parse --show-toplevel)" = "$(cd "$1" && pwd -P)" ] || return 2
}

run_c1() { local repo=$1 work=$2; mkdir -p "$work"; python3 "$repo/$C1" --lane "$repo" --rev "$(git -C "$repo" rev-parse HEAD)" --work "$work" --explain 2>&1 | tail -1; }
run_c2() { local repo=$1 work=$2; mkdir -p "$work"; python3 "$repo/$C2" --lane "$repo" --rev "$(git -C "$repo" rev-parse HEAD)" --work "$work" --explain 2>&1 | tail -1; }

echo "# phase A: do-nothing and mutation controls (expected false unless stated)"
A_n=$((A_n+1)); L=$(mkdir -p "$SCR/w-ctl0c1"; python3 "$LANE/$C1" --lane "$LANE" --rev "$BASE" --work "$SCR/w-ctl0c1" 2>&1 | tail -1); V=$(echo "$L" | verdict_of); emit CTL_0_c1 false "$V" "$L"
A_n=$((A_n+1)); L=$(mkdir -p "$SCR/w-ctl0c2"; python3 "$LANE/$C2" --lane "$LANE" --rev "$FREEZE" --work "$SCR/w-ctl0c2" 2>&1 | tail -1); V=$(echo "$L" | verdict_of); emit CTL_0_c2 false "$V" "$L"

# CTL_SKIP_c1: the re-key entries removed from the ledger - values without the bind
D=$SCR/skip-c1; clone_at "$D" "$PIN" || exit 2
python3 - "$D" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1], '.ufo/evidence/round-21/coldread/ledger.json')
d = json.loads(p.read_text('utf-8'))
d['entries'] = [e for e in d['entries'] if not any(
    isinstance(t, str) and '/rekey-r56-' in t for t in (e.get('traces') or []))]
p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + '\n', 'utf-8')
PY
git -C "$D" -c user.name=control -c user.email=control@invalid add -A >/dev/null
git -C "$D" -c user.name=control -c user.email=control@invalid commit --quiet -m 'control: rekey removed' >/dev/null
A_n=$((A_n+1)); L=$(run_c1 "$D" "$SCR/w-skipc1"); V=$(echo "$L" | verdict_of); emit CTL_SKIP_c1 false "$V" "$L"

# CTL_FAB_c1: one reader's section hash fabricated
D=$SCR/fab-c1; clone_at "$D" "$PIN" || exit 2
python3 - "$D" <<'PY'
import json, sys
from pathlib import Path
hits = sorted(Path(sys.argv[1], '.ufo/waves/round-56').glob('w[23]/*Read*.json'))
if not hits:
    sys.exit('no reader report found')
p = hits[0]
d = json.loads(p.read_text('utf-8'))
d['section_sha256'] = '0' * 64
p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + '\n', 'utf-8')
print('fabricated', p.name)
PY
git -C "$D" -c user.name=control -c user.email=control@invalid add -A >/dev/null
git -C "$D" -c user.name=control -c user.email=control@invalid commit --quiet -m 'control: fabricated section hash' >/dev/null
A_n=$((A_n+1)); L=$(run_c1 "$D" "$SCR/w-fabc1"); V=$(echo "$L" | verdict_of); emit CTL_FAB_c1 false "$V" "$L"

# CTL_RESTATE_c1: the standing row asserts a score the monitor does not read
D=$SCR/restate-c1; clone_at "$D" "$PIN" || exit 2
python3 - "$D" <<'PY'
import re, sys
from pathlib import Path
p = Path(sys.argv[1], 'SCORECARD.md')
lines = p.read_text('utf-8').splitlines()
idx = [i for i, ln in enumerate(lines)
       if ln.strip().startswith('| calibration |') and re.match(r'^\|\s*calibration\s*\|\s*\d+\s*\|', ln.strip())]
if not idx:
    sys.exit('no calibration row')
cells = lines[idx[-1]].split('|')
cells[2] = ' 9 '
lines[idx[-1]] = '|'.join(cells)
p.write_text('\n'.join(lines) + '\n', 'utf-8')
print('row', lines[idx[-1]][:120])
PY
git -C "$D" -c user.name=control -c user.email=control@invalid add -A >/dev/null
git -C "$D" -c user.name=control -c user.email=control@invalid commit --quiet -m 'control: row asserts 9' >/dev/null
A_n=$((A_n+1)); L=$(run_c1 "$D" "$SCR/w-restate"); V=$(echo "$L" | verdict_of); emit CTL_RESTATE_c1 false "$V" "$L"

# CTL_SKIP_c2: the gate's binding arm removed (any resolvable rev accepted)
D=$SCR/skip-c2; clone_at "$D" "$PIN" || exit 2
python3 - "$D" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1], 'tools/receipt-revision-gate.py')
text = p.read_text('utf-8')
needle = "            if paths is None:\n                codes.append('RECEIPT_REV_MISMATCH')"
if needle not in text:
    sys.exit('gate needle absent')
text = text.replace(needle, "            if False:\n                codes.append('RECEIPT_REV_MISMATCH')", 1)
p.write_text(text, 'utf-8')
PY
git -C "$D" -c user.name=control -c user.email=control@invalid add -A >/dev/null
git -C "$D" -c user.name=control -c user.email=control@invalid commit --quiet -m 'control: binding arm removed' >/dev/null
A_n=$((A_n+1)); L=$(run_c2 "$D" "$SCR/w-skipc2"); V=$(echo "$L" | verdict_of); emit CTL_SKIP_c2 false "$V" "$L"

# CTL_FAB_c2: the real round-54 slice replaced by a receipt that only names the certified rev
D=$SCR/fab-c2; clone_at "$D" "$PIN" || exit 2
printf 'CTL CTL_POS_c1 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c fabricated=1\n' \
  > "$D/$E/c2/red-before/round-54-ctl-pos-c1.stdout"
git -C "$D" -c user.name=control -c user.email=control@invalid add -A >/dev/null
git -C "$D" -c user.name=control -c user.email=control@invalid commit --quiet -m 'control: fabricated red-before receipt' >/dev/null
A_n=$((A_n+1)); L=$(run_c2 "$D" "$SCR/w-fabc2"); V=$(echo "$L" | verdict_of); emit CTL_FAB_c2 false "$V" "$L"

A_ok=$(grep -c . "$SCR/matches" 2>/dev/null || echo 0)
echo "CONTROLS_A: $A_ok/$A_n as pre-registered"

echo "# phase B: the positive controls scored at the revision they certify (PIN=$PIN)"
B_ok=0; B_n=0
D=$SCR/pos; clone_at "$D" "$PIN" || exit 2
B_n=$((B_n+1)); L=$(run_c1 "$D" "$SCR/w-posc1"); V=$(echo "$L" | verdict_of); emit CTL_POS_c1 true "$V" "$L"; [ "$V" = true ] && B_ok=$((B_ok+1))
B_n=$((B_n+1)); L=$(run_c2 "$D" "$SCR/w-posc2"); V=$(echo "$L" | verdict_of); emit CTL_POS_c2 true "$V" "$L"; [ "$V" = true ] && B_ok=$((B_ok+1))
echo "CONTROLS_B: $B_ok/$B_n as pre-registered"
