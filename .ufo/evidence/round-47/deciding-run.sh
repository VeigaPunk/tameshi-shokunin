#!/bin/bash
# Round-47 deciding run. Usage: deciding-run.sh LANE REV OUTDIR [WORKROOT]
#   LANE    absolute path of the lane repo (the counters read git objects at REV, never the worktree)
#   REV     the content revision that carries the records (QUALITY criterion 86): the deciding receipts are
#           taken here and committed afterwards in a receipts-only commit.
#   OUTDIR  an existing directory inside LANE (receipts are written as files there).
# Every step reads REV (git show / ls-tree / archive), not the worktree:
#   0  FROZEN_UNCHANGED   git diff FREEZE..REV over the frozen counters, statements, pool, snapshots, package copies,
#                         controls, assembler, no-harm script and contract is empty
#   0b HARDENED_REBUILD   the two v2 counters at REV are byte-identical to assemble.py over the wave-1 additions at REV
#   1  no-harm monitors   .ufo/evidence/round-47/no-harm.sh taken FROM REV (seven monitors), plus the cold-read
#                         monitor's credited-section count (>= 60)
#   2  C1, C2, C3         the three frozen counters at REV
#   3  ENTRY_NAMES_OK     every admitted C3 entry basename is one of the three package basenames AT REV
#   4  census             sources-census.sh validate --root FLEET tameshi, exit 0
set -u
LANE=$1; REV=$2; OUT=$3; WORK=${4:-/var/tmp/tameshi-r47-deciding}
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
FREEZE=9acfbe21435e1976636a276448dee1d5e7155915
BASE=0b5b7cd2b2c15d23086e811a0f0348d84261277b
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-47
W1=.ufo/waves/round-47/w1
cd "$LANE" || exit 2
REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
rc=0
FROZEN="$E/contract.json $E/calibration/measure.py $E/calibration/statements.json $E/coverage/measure.py $E/coverage/sources $E/assimilation/package $E/hardening/pool.py $E/hardening/pool.json $E/hardening/assemble.py $E/control $E/no-harm.sh $E/before/base-freshness.txt $E/before/base-coverage.txt .ufo/waves/round-47/hard-brief.md"
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
for f in calibration/measure.py calibration/statements.json coverage/measure.py hardening/pool.py hardening/pool.json hardening/freshness-counter.py hardening/coverage-counter.py; do echo "COUNTER_SHA256 $f $(git show "$REV:$E/$f" | sha256sum | cut -c1-64)" | tee -a "$OUT/frozen.stdout"; done
T=$(mktemp -d)
git archive "$REV" .ufo/evidence/round-46/hardening "$E/hardening" "$W1" | tar -x -C "$T"
FADD=$(cd "$T/$W1" && ls *.addition.py | grep -E '^T47HardFresh' | sort | sed "s#^#--add $T/$W1/#" | tr '\n' ' ')
CADD=$(cd "$T/$W1" && ls *.addition.py | grep -E '^T47HardCover' | sort | sed "s#^#--add $T/$W1/#" | tr '\n' ' ')
# the assembler reads its base relative to the lane root: point it at the extracted tree
python3 - "$T" "$FADD" "$CADD" <<'PYEOF' > "$T/rebuild.out" 2>&1
import importlib.util, shlex, sys
t, fadd, cadd = sys.argv[1], shlex.split(sys.argv[2]), shlex.split(sys.argv[3])
spec = importlib.util.spec_from_file_location('asm', t + '/.ufo/evidence/round-47/hardening/assemble.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
adds = lambda xs: [xs[i + 1] for i in range(0, len(xs), 2)]
open(t + '/f.py', 'w', encoding='utf-8').write(m.assemble('freshness', adds(fadd), base_dir=t))
open(t + '/c.py', 'w', encoding='utf-8').write(m.assemble('coverage', adds(cadd), base_dir=t))
print('rebuilt')
PYEOF
if git show "$REV:$E/hardening/freshness-counter.py" | cmp -s - "$T/f.py" && git show "$REV:$E/hardening/coverage-counter.py" | cmp -s - "$T/c.py"; then echo "HARDENED_REBUILD=1" | tee -a "$OUT/frozen.stdout"; else echo "HARDENED_REBUILD=0 ($(tr '\n' ' ' < "$T/rebuild.out"))" | tee -a "$OUT/frozen.stdout"; rc=1; fi
rm -rf "$T"
git show "$REV:$E/no-harm.sh" > "$OUT/no-harm.sh.copy"
bash "$OUT/no-harm.sh.copy" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; nh=$?; echo "$nh" > "$OUT/no-harm.exit"; rm -f "$OUT/no-harm.sh.copy"
cat "$OUT/no-harm.stdout"; echo "NOHARM_EXIT=$nh"
[ "$nh" = 0 ] || rc=1
grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 7 ] || { echo "NOHARM_OK_COUNT!=7"; rc=1; }
sections=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(1 for s in d["coldread"]["sections"] if s["credited"]))')
echo "COLDREAD_SECTIONS_CREDITED=$sections (base 60)" | tee "$OUT/coldread-sections.stdout"
[ "$sections" -ge 60 ] || rc=1
python3 "$E/hardening/pool.py" --lane "$LANE" --rev "$REV" --targets v2 > "$OUT/c2.stdout" 2>&1; echo $? > "$OUT/c2.exit"; tail -1 "$OUT/c2.stdout"; [ "$(cat "$OUT/c2.exit")" = 0 ] || rc=1
python3 "$E/coverage/measure.py" --lane "$LANE" --rev "$REV" > "$OUT/c3.stdout" 2>&1; echo $? > "$OUT/c3.exit"; tail -1 "$OUT/c3.stdout"; [ "$(cat "$OUT/c3.exit")" = 0 ] || rc=1
names=$(grep '^ENTRY ' "$OUT/c3.stdout" | sed 's#^ENTRY .*/##; s# (not indexed)$##' | sort | tr '\n' ' ')
want=$(git ls-tree --name-only "$REV" -- "$E/assimilation/package/" | sed 's#.*/##' | sort | tr '\n' ' ')
[ "$names" = "$want" ] && echo "ENTRY_NAMES_OK=1 $names" || { echo "ENTRY_NAMES_OK=0 got=[$names] want=[$want]"; rc=1; }
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"; echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
cp "$OUT/census.stdout" "$E/census-end.stdout"; cp "$OUT/census.stderr" "$E/census-end.stderr"; cp "$OUT/census.exit" "$E/census-end.exit"
rm -rf "$WORK"
python3 "$E/calibration/measure.py" --lane "$LANE" --rev "$REV" --base "$BASE" --work "$WORK" > "$OUT/c1.stdout" 2>&1; echo $? > "$OUT/c1.exit"; tail -1 "$OUT/c1.stdout"; [ "$(cat "$OUT/c1.exit")" = 0 ] || rc=1
echo "DECIDING_RUN_EXIT=$rc"
exit $rc
