#!/usr/bin/env bash
# Independent arm census for the C2 claim at C1 — every arm measured without the
# counter's aggregation, plus the /tmp census under BOTH the frozen and the
# repaired regex. Read-only on the lane: the tree comes from a scratch clone.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=99c3bc88d704566197783f66b211ee0a830e0330
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r54/T54W2Exec02
CLONE=$S/census-clone
USABLE=$S/census-usable
BAD=$S/census-unusable-never-created
rm -rf -- "$CLONE" "$USABLE" "$BAD"; mkdir -p -- "$USABLE"

git clone --shared --quiet "$LANE" "$CLONE"
git -C "$CLONE" checkout --quiet "$REV"
TOP=$(git -C "$CLONE" rev-parse --show-toplevel)
if [ "$TOP" != "$CLONE" ]; then echo "REFUSE: toplevel is $TOP"; exit 1; fi
echo "fixture-toplevel-ok: $TOP"
echo "rev: $(git -C "$CLONE" rev-parse HEAD)"
echo "unusable path exists: $([ -e "$BAD" ] && echo YES-BAD || echo no-good)"

TOOLS=(
  "registry-check.py --selftest"
  "env-diff.py --selftest"
  "bash-witness-study.py selftest"
  "evidence-disposition.py --selftest"
  "pin-disposition.py --selftest"
  "context-capture.py --selftest"
  "repeat-control.py --selftest"
)

echo "tool | unusable_rc | names_value | tracebacks | empty_rc | usable_rc"
for t in "${TOOLS[@]}"; do
  set -- $t; p=$1; shift
  u_out=$( cd "$CLONE" && TMPDIR="$BAD" PYTHONDONTWRITEBYTECODE=1 python3 "tools/$p" "$@" 2>&1 ); u_rc=$?
  ( cd "$CLONE" && TMPDIR="" PYTHONDONTWRITEBYTECODE=1 python3 "tools/$p" "$@" >/dev/null 2>&1 ); e_rc=$?
  ( cd "$CLONE" && TMPDIR="$USABLE" PYTHONDONTWRITEBYTECODE=1 python3 "tools/$p" "$@" >/dev/null 2>&1 ); ok_rc=$?
  printf '%-26s | %s | %s | %s | %s | %s\n' "$p" "$u_rc" \
    "$(printf '%s' "$u_out" | grep -c -F "$BAD")" \
    "$(printf '%s' "$u_out" | grep -c 'Traceback (most recent call last)')" "$e_rc" "$ok_rc"
done

echo "--- /tmp census, counter's own strace vector, frozen vs repaired regex ---"
for t in "${TOOLS[@]}"; do
  set -- $t; p=$1; shift
  lg=$S/census-strace-$p.log
  ( cd "$CLONE" && TMPDIR="$USABLE" strace -f -e trace=mkdir,mkdirat -o "$lg" \
      python3 "tools/$p" "$@" >/dev/null 2>&1 )
done
python3 - "$LANE/.ufo/evidence/round-54/c2/measure.py" "$S" <<'PY'
import glob, re, sys
src = open(sys.argv[1]).read()
line = [l for l in src.splitlines() if 'findall' in l and 'mkdir' in l][0]
frozen = re.search(r"re\.findall\((r'[^']*')", line).group(1)
repaired = r'mkdir(?:at)?\([^)]*"/tmp'
print('frozen regex  :', frozen)
print('repaired regex:', repaired)
tot = 0
for f in sorted(glob.glob(sys.argv[2] + '/census-strace-*.log')):
    t = open(f, errors='replace').read()
    tot += len(re.findall(eval(frozen), t))
    print('%-46s frozen=%-3d repaired=%-3d' % (
        f.rsplit('/', 1)[1], len(re.findall(eval(frozen), t)), len(re.findall(repaired, t))))
print('frozen total across seven logs:', tot)
PY
