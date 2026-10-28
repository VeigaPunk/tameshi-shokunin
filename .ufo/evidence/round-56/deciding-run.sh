#!/bin/bash
# Round-56 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR
#   LANE    absolute path of the lane repo        REV     the content revision
#   FREEZE  the counter-freeze commit             OUTDIR  an existing, EMPTY directory inside LANE for receipts
# Carried from rounds 49-55 (QUALITY 99/105/107): gate 0 refuses (exit 3, nothing run) unless the freeze
# manifest re-derives from the bytes at FREEZE, every pre-registered control receipt is committed at REV in
# a commit that descends from FREEZE, and - this round's C2 - tools/receipt-revision-gate.py accepts the
# round's own receipts at REV (the gate binds a receipt to the revision it certifies). A second invocation
# is refused; each counter gets a start receipt before it runs and an exit receipt after; the counters,
# no-harm and the precheck run from the bytes committed at REV, never from the working tree; the working
# tree must be clean. Work dirs: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r56/deciding.
set -u
LANE=$1; REV=$2; FREEZE=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
BASE=981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1
FLEET=/home/vgpnk/Projects/shokunin
E=.ufo/evidence/round-56
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r56/deciding
cd "$LANE" || exit 2
REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
python3 - "$LANE" "$FREEZE" "$E" <<'PYV' || { echo "DECIDING_REFUSED freeze-integrity"; exit 3; }
import hashlib, json, os, subprocess, sys
lane, freeze, E = sys.argv[1], sys.argv[2], sys.argv[3]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
def show(rev, path):
    r = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
                       capture_output=True, env=env)
    return r.stdout if r.returncode == 0 else None
fr = json.loads(show(freeze, '%s/freeze.json' % E))
co = json.loads(show(freeze, '%s/contract.json' % E))
bad = []
# manifest key of a contract frozen path: tools/ and .ufo/evidence/round-(21|48)/
# paths are their own keys; everything else is relative to E; freeze.json is
# listed and skipped (a file cannot carry its own digest).
def key(p):
    if p.startswith(('tools/', '.ufo/evidence/round-21/', '.ufo/evidence/round-48/')):
        return p
    if p.startswith(E + '/'):
        return p[len(E) + 1:]
    return None
want_keys = set()
for p in co.get('frozen_paths', []):
    k = key(p)
    if k is None:
        bad.append('unmappable frozen path %s' % p)
        continue
    if k != 'freeze.json':
        want_keys.add(k)
if set(fr.get('files', {})) != want_keys:
    bad.append('manifest keys %s != contract surface %s'
               % (sorted(fr.get('files', {})), sorted(want_keys)))
for rel, want in sorted(fr['files'].items()):
    path = rel if rel.startswith(('tools/', '.ufo/evidence/round-21/', '.ufo/evidence/round-48/')) else '%s/%s' % (E, rel)
    r = show(freeze, path)
    if r is None:
        bad.append('%s unreadable' % rel)
        continue
    got = hashlib.sha256(r).hexdigest()
    if got != want:
        bad.append('%s %s != %s' % (rel, got[:12], want[:12]))
am = fr.get('amendments') or []
# an amendment entry is {n, what, prior_freeze}: n counts from 1 and the count
# of commits that ever touched freeze.json must be len(am)+1 (the original
# freeze), so a re-frozen instrument without an amendment entry is refused.
touches = subprocess.run(['git', '-C', lane, 'rev-list', '--count', freeze, '--',
                          '%s/freeze.json' % E], capture_output=True, env=env)
try:
    n_touches = int(touches.stdout.decode().strip())
except ValueError:
    n_touches = -1
shape_ok = all(isinstance(a, dict) and a.get('n') == i + 1 and isinstance(a.get('what'), str)
               for i, a in enumerate(am))
if not (shape_ok and n_touches == len(am) + 1):
    bad.append('amendments=%d inconsistent with %d manifest commits or record shape' % (len(am), n_touches))
if co.get('amendments') != am:
    bad.append('contract.json amendments do not mirror freeze.json amendments')
print('FREEZE_INTEGRITY: %s files=%d amendments=%d'
      % ('OK' if not bad else 'MISMATCH', len(fr['files']), len(am)))
for b in bad:
    print('FREEZE_MISMATCH', b)
sys.exit(0 if not bad else 1)
PYV
[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
for k in c1 c2; do [ -e "$OUT/$k.start" ] && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done
[ -z "$(ls -A "$OUT" 2>/dev/null)" ] || { echo "DECIDING_REFUSED outdir-not-empty"; exit 3; }
[ "$(git rev-parse HEAD)" = "$REV" ] || { echo "DECIDING_REFUSED head-is-not-rev"; exit 3; }
# the freeze argument must be the last commit that touched freeze.json at REV:
# freeze.json changes only at the original freeze and at amendment commits, so
# a revision whose manifest is honest names that commit (H2, T56W1RevFreeze).
FREEZE_LAST=$(git log -1 --format=%H "$REV" -- "$E/freeze.json")
[ -n "$FREEZE_LAST" ] && [ "$FREEZE" = "$FREEZE_LAST" ] || { echo "DECIDING_REFUSED freeze-not-last-manifest-commit $FREEZE"; exit 3; }
CONTROLS="$E/control/controls-a.stdout $E/control/controls-a.exit $E/control/controls-a.stdout.sha256 $E/control/controls-b.stdout $E/control/controls-b.exit $E/control/controls-b.stdout.sha256"
for f in $CONTROLS; do
  git cat-file -e "$REV:$f" 2>/dev/null || { echo "DECIDING_REFUSED control-receipt-missing $f"; exit 3; }
  [ "$(git cat-file -t "$REV:$f")" = blob ] || { echo "DECIDING_REFUSED control-receipt-not-a-blob $f"; exit 3; }
  [ "$(git cat-file -s "$REV:$f")" -gt 0 ] || { echo "DECIDING_REFUSED control-receipt-empty $f"; exit 3; }
  c=$(git log -1 --format=%H "$REV" -- "$f")
  git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
done
grep -Eq '^CONTROLS_A: ([0-9]+)/\1 as pre-registered' <(git show "$REV:$E/control/controls-a.stdout") || { echo "DECIDING_REFUSED controls-a-verdict-missing"; exit 3; }
grep -q 'CTL_MISMATCH' <(git show "$REV:$E/control/controls-a.stdout") && { echo "DECIDING_REFUSED controls-a-mismatch-lines"; exit 3; }
grep -Eq '^CONTROLS_B: ([0-9]+)/\1 as pre-registered' <(git show "$REV:$E/control/controls-b.stdout") || { echo "DECIDING_REFUSED controls-b-verdict-missing"; exit 3; }
grep -q 'CTL_MISMATCH' <(git show "$REV:$E/control/controls-b.stdout") && { echo "DECIDING_REFUSED controls-b-mismatch-lines"; exit 3; }
rm -rf "$SCR"; mkdir -p "$SCR/code" "$SCR/c1" "$SCR/c2" "$SCR/gate"; export TMPDIR="$SCR"
for f in c1/measure.py c2/measure.py no-harm.sh; do
  mkdir -p "$SCR/code/$(dirname $f)"; git show "$REV:$E/$f" > "$SCR/code/$f" || exit 2
done
git show "$REV:$E/c1/lost-headings-at-base.json" > "$SCR/code/c1/lost-headings-at-base.json" || exit 2
git show "$REV:tools/receipt-revision-gate.py" > "$SCR/gate/gate.py" || exit 2
git show "$REV:.ufo/evidence/round-48/quality/coldread-precheck.sh" > "$SCR/code/precheck.sh" || exit 2

# gate 0b (this round's C2): the lane's own receipts must pass the binding gate.
# The receipts are read from the bytes committed at REV, never the worktree (F-3).
mkdir -p "$SCR/rcpt"
for f in controls-a.stdout controls-a.stdout.sha256 controls-b.stdout controls-b.stdout.sha256 frozen-surface.paths; do
  git show "$REV:$E/control/$f" > "$SCR/rcpt/$f" || exit 2
done
python3 "$SCR/gate/gate.py" --lane "$LANE" --certified "$REV" \
  --paths "$SCR/rcpt/frozen-surface.paths" \
  --receipt "$SCR/rcpt/controls-a.stdout:control" \
  --receipt "$SCR/rcpt/controls-b.stdout:positive" \
  > "$OUT/receipt-gate.stdout" 2>&1
echo $? > "$OUT/receipt-gate.exit"
tail -1 "$OUT/receipt-gate.stdout"
[ "$(cat "$OUT/receipt-gate.exit")" = 0 ] || { echo "DECIDING_REFUSED receipt-binding $(tail -1 "$OUT/receipt-gate.stdout")"; exit 3; }

git status --porcelain > "$OUT/clean-tree-before.txt"
# untracked OUTDIR receipts are excluded by anchored prefix: a foreign file whose
# name merely EXTENDS the outdir's relative path is still dirt (F-2).
[ "$(grep -vc "^?? ${OUT#$LANE/}/" "$OUT/clean-tree-before.txt")" = 0 ] || { echo "DECIDING_REFUSED dirty-tree"; cat "$OUT/clean-tree-before.txt"; exit 3; }
rc=0
# the frozen surface is the contract's own list, expanded under E (H3).
FROZEN=$(python3 -c 'import json,sys; c=json.load(open(sys.argv[1])); print(" ".join(c["frozen_paths"]))' "$E/contract.json") || exit 2
if git diff --quiet "$FREEZE" "$REV" -- $FROZEN; then echo "FROZEN_UNCHANGED=1 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; else echo "FROZEN_UNCHANGED=0 freeze=$FREEZE rev=$REV" | tee "$OUT/frozen.stdout"; git diff --stat "$FREEZE" "$REV" -- $FROZEN | tee -a "$OUT/frozen.stdout"; rc=1; fi
bash "$SCR/code/no-harm.sh" "$LANE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
cat "$OUT/no-harm.stdout"; grep -q RED "$OUT/no-harm.stdout" && rc=1
[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 15 ] || { echo "NOHARM_OK_COUNT!=15"; rc=1; }
bash "$SCR/code/precheck.sh" "$LANE" "$BASE" "$REV" > "$OUT/coldread-precheck.stdout" 2>&1; echo $? > "$OUT/coldread-precheck.exit"
tail -1 "$OUT/coldread-precheck.stdout"; [ "$(cat "$OUT/coldread-precheck.exit")" = 0 ] || rc=1
"$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"
echo "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
for k in c1 c2; do
  date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/$k.start"
  case $k in
    c1) python3 "$SCR/code/c1/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c1" --explain > "$OUT/c1.stdout" 2>&1 ;;
    c2) python3 "$SCR/code/c2/measure.py" --lane "$LANE" --rev "$REV" --work "$SCR/c2" --explain > "$OUT/c2.stdout" 2>&1 ;;
  esac
  echo $? > "$OUT/$k.exit"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/$k.end"
  tail -1 "$OUT/$k.stdout"
  [ "$(cat "$OUT/$k.exit")" = 0 ] || rc=1
  grep -q "${k^^}_R56_PASS=true" "$OUT/$k.stdout" || rc=1
done
# gate 0c: the verdicts this run just produced must name the certified revision.
python3 "$SCR/gate/gate.py" --lane "$LANE" --certified "$REV" \
  --receipt "$OUT/c1.stdout:verdict:C1_R56_PASS=" \
  --receipt "$OUT/c2.stdout:verdict:C2_R56_PASS=" \
  > "$OUT/receipt-gate-verdicts.stdout" 2>&1
echo $? > "$OUT/receipt-gate-verdicts.exit"
tail -1 "$OUT/receipt-gate-verdicts.stdout"
[ "$(cat "$OUT/receipt-gate-verdicts.exit")" = 0 ] || rc=1
git status --porcelain > "$OUT/clean-tree-after.txt"
[ "$(grep -vc "^?? ${OUT#$LANE/}/" "$OUT/clean-tree-after.txt")" = 0 ] || { echo "DECIDING_REFUSED dirty-tree-after"; cat "$OUT/clean-tree-after.txt"; rc=1; }
echo "DECIDING_RUN_EXIT=$rc" | tee "$OUT/deciding-run.exit"
exit $rc
