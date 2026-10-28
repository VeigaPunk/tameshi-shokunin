#!/usr/bin/env bash
# Positive control for the C2 `tmp_mkdirs` arm: can the arm fire at all?
#
# 1. run a fixture that really allocates one directory under /tmp, under the
#    counter's OWN strace vector (`strace -f -e trace=mkdir,mkdirat -o LOG`);
# 2. lift the census regex LITERAL out of the frozen counter (no paraphrase);
# 3. count with the frozen literal and with the repaired literal.
#
# Expect on a working arm: frozen==1.  Observed: frozen==0, repaired==1.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
MEASURE="$LANE/.ufo/evidence/round-54/c2/measure.py"
HERE=$(cd "$(dirname "$0")" && pwd)
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r54/T54W2Exec02
mkdir -p "$S"
LOG="$S/ctl-pos-strace.log"
TARGET="/tmp/T54W2Exec02-probe-$$"
rm -rf -- "$TARGET"

strace -f -e trace=mkdir,mkdirat -o "$LOG" \
    python3 "$HERE/probe-mkdir-tmp.py" "$TARGET" >/dev/null
echo "strace_rc=$? target=$TARGET"
echo "--- strace log ---"
cat "$LOG"
echo "--- census ---"
python3 - "$MEASURE" "$LOG" <<'PY'
import re, sys
src = open(sys.argv[1]).read()
line = [l for l in src.splitlines() if 'findall' in l and 'mkdir' in l][0]
print('FROZEN LINE:', line.strip())
frozen = re.search(r"re\.findall\((r'[^']*')", line).group(1)
repaired = r'mkdir(?:at)?\([^)]*"/tmp'  # what the source comment intends
log = open(sys.argv[2]).read()
print('EXTRACTED REGEX:', frozen)
print('FROZEN HITS  :', len(re.findall(eval(frozen), log)))
print('REPAIRED     :', repaired, '->', len(re.findall(repaired, log)))
PY
rmdir -- "$TARGET" 2>/dev/null || true
