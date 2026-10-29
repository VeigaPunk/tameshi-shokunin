#!/bin/bash
# Round-57 deciding run. Usage: deciding-run.sh LANE BASE REV OUTDIR
#   LANE    absolute path of the lane repo          BASE  the round's base commit (contract.json "base")
#   REV     the content revision to certify         OUTDIR  an existing, EMPTY directory inside LANE for receipts
# Carried from round 56 with five re-designs (round-56 lesson: CONTROLS_B read 1/2 on its first run because the
# receipt gate was a precondition of the controls, and the freeze commit was an argument):
#  * the freeze commit is DERIVED (the last commit touching freeze.json at REV), never passed;
#  * everything runs in a FRESH `git clone --shared` of LANE, and REV must be that clone's HEAD (a lane whose
#    HEAD moved, or whose REV is an ancestor, is refused); the lane's own working tree must also be clean;
#  * the receipt gate is NOT a precondition of the controls: controls-a/b are only required to exist at REV, to be
#    committed after the freeze, to carry their verdict line and no CTL_MISMATCH. The gate runs LAST and certifies
#    only the receipts this script just produced (c1.stdout, c2.stdout);
#  * the freeze manifest (tameshi-freeze-v1) digests are re-derived at the freeze commit AND at REV (a frozen file
#    edited after the freeze is a refusal here, not a late note) and this script's own bytes must equal the
#    committed .ufo/evidence/round-57/deciding-run.sh at REV;
#  * the cold-read precheck runs BEFORE any counter and a RED (or an error) refuses the run.
# Gate-0 refusals print `DECIDING_REFUSED <reason>`, exit 3 and write nothing to OUTDIR (a retry stays possible);
# once the first counter starts, a second invocation is refused. A run that reaches the end prints
# `DECIDING_RUN_EXIT=<n>` (0 only when every counter prints its PASS=true, no-harm has no RED, precheck is ok and
# the final gate passes). Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r57/deciding, removed on
# exit; counters get --work dirs inside it and TMPDIR points there. DECIDING_FLEET overrides the fleet root that
# holds scripts/sources-census.sh (default /home/vgpnk/Projects/shokunin); it exists so the script can be proven on
# a stub fleet and is echoed into census.stdout.
set -u
for v in $(compgen -e | grep '^GIT_'); do unset "$v"; done
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
[ $# = 4 ] || { echo "usage: deciding-run.sh LANE BASE REV OUTDIR" >&2; exit 2; }
LANE=$1; BASE=$2; REV=$3; OUT=$4
case "$LANE" in /*) ;; *) echo "LANE must be absolute" >&2; exit 2;; esac
case "$OUT" in /*) ;; *) echo "OUTDIR must be absolute" >&2; exit 2;; esac
NOHARM_MIN=18
FLEET=${DECIDING_FLEET:-/home/vgpnk/Projects/shokunin}
E=.ufo/evidence/round-57
SELF=$(readlink -f "${BASH_SOURCE[0]}")
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r57/deciding
refuse() { echo "DECIDING_REFUSED $*"; exit 3; }
cd "$LANE" || exit 2
LANE=$(git rev-parse --show-toplevel) || exit 2
[ -d "$OUT" ] || refuse outdir-missing
OUT=$(readlink -f "$OUT")
case "$OUT" in "$LANE"/*) ;; *) refuse outdir-not-in-lane "$OUT";; esac
OUTREL=${OUT#"$LANE"/}
REV=$(git rev-parse --verify --quiet "$REV^{commit}") || refuse rev-unresolvable
BASE=$(git rev-parse --verify --quiet "$BASE^{commit}") || refuse base-unresolvable
[ "$BASE" != "$REV" ] && git merge-base --is-ancestor "$BASE" "$REV" || refuse base-not-proper-ancestor-of-rev
for k in c1 c2; do [ -e "$OUT/$k.start" ] && refuse second-invocation "$k"; done
[ -z "$(ls -A "$OUT" 2>/dev/null)" ] || refuse outdir-not-empty
# the lane working tree must carry nothing the commits do not (r55.6): only untracked files under OUTDIR are allowed.
DIRT=$(git status --porcelain | grep -v "^?? $OUTREL/" || true)
[ -z "$DIRT" ] || { echo "$DIRT"; refuse dirty-tree; }
rm -rf "$SCR"; mkdir -p "$SCR/c1" "$SCR/c2" "$SCR/gate"; trap 'rm -rf -- "$SCR"' EXIT; export TMPDIR="$SCR"
# fresh clone: REV must be its HEAD. Every counter below reads this clone, never the lane's working tree.
git clone --shared --quiet "$LANE" "$SCR/clone" 2>"$SCR/clone.stderr" || { cat "$SCR/clone.stderr"; refuse fresh-clone-failed; }
CL=$SCR/clone
[ "$(git -C "$CL" rev-parse HEAD)" = "$REV" ] || refuse rev-is-not-head-of-fresh-clone "rev=$REV head=$(git -C "$CL" rev-parse HEAD)"
# this script must be the committed one
git -C "$CL" cat-file -e "$REV:$E/deciding-run.sh" 2>/dev/null || refuse counter-missing "$E/deciding-run.sh"
cmp -s "$SELF" "$CL/$E/deciding-run.sh" || refuse script-not-committed-bytes "$E/deciding-run.sh"
# every instrument the run executes must exist at REV as a non-empty blob
for f in "$E/c1/measure.py" "$E/c2/measure.py" "$E/no-harm.sh" "$E/contract.json" "$E/freeze.json" \
         tools/receipt-revision-gate.py .ufo/evidence/round-48/quality/coldread-precheck.sh; do
  git -C "$CL" cat-file -e "$REV:$f" 2>/dev/null || refuse counter-missing "$f"
  [ "$(git -C "$CL" cat-file -t "$REV:$f")" = blob ] || refuse counter-not-a-blob "$f"
  [ "$(git -C "$CL" cat-file -s "$REV:$f")" -gt 0 ] || refuse counter-empty "$f"
done
# the freeze commit is the last one that touched freeze.json at REV
FREEZE=$(git -C "$CL" log -1 --format=%H "$REV" -- "$E/freeze.json")
[ -n "$FREEZE" ] || refuse freeze-commit-not-found
git -C "$CL" merge-base --is-ancestor "$BASE" "$FREEZE" || refuse freeze-not-after-base
python3 - "$CL" "$FREEZE" "$REV" "$BASE" "$E" <<'PYV' || refuse freeze-integrity
import hashlib, json, os, subprocess, sys
lane, freeze, rev, base, E = sys.argv[1:6]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
def show(r, path):
    p = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (r, path)], capture_output=True, env=env)
    return p.stdout if p.returncode == 0 else None
bad = []
try:
    fr = json.loads(show(freeze, '%s/freeze.json' % E))
    co = json.loads(show(freeze, '%s/contract.json' % E))
except Exception as e:
    print('FREEZE_INTEGRITY: MISMATCH'); print('FREEZE_MISMATCH unreadable manifest/contract: %r' % e); sys.exit(1)
if fr.get('schema') != 'tameshi-freeze-v1':
    bad.append('schema %r != tameshi-freeze-v1' % fr.get('schema'))
if fr.get('round') != 57 or co.get('round') != 57:
    bad.append('round freeze=%r contract=%r != 57' % (fr.get('round'), co.get('round')))
if fr.get('base') != base or co.get('base') != base:
    bad.append('base freeze=%s contract=%s != argument %s' % (str(fr.get('base'))[:12], str(co.get('base'))[:12], base[:12]))
# a manifest key is relative to E, except tools/ paths which are their own keys; freeze.json is listed in the
# contract and skipped (a file cannot carry its own digest).
def key(p):
    if p.startswith('tools/'):
        return p
    if p.startswith(E + '/'):
        return p[len(E) + 1:]
    return None
def path_of(rel):
    return rel if rel.startswith('tools/') else '%s/%s' % (E, rel)
want_keys = set()
for p in co.get('frozen_paths', []):
    k = key(p)
    if k is None:
        bad.append('unmappable frozen path %s' % p)
    elif k != 'freeze.json':
        want_keys.add(k)
files = fr.get('files', {})
if set(files) != want_keys:
    bad.append('manifest keys %s != contract surface %s' % (sorted(files), sorted(want_keys)))
for rel, want in sorted(files.items()):
    for where, label in ((freeze, 'freeze'), (rev, 'rev')):
        r = show(where, path_of(rel))
        if r is None:
            bad.append('%s unreadable at %s' % (rel, label)); continue
        got = hashlib.sha256(r).hexdigest()
        if got != want:
            bad.append('%s %s != %s at %s' % (rel, got[:12], want[:12], label))
am = fr.get('amendments') or []
# amendment entries are {n, what}: n counts from 1 and the number of commits that ever touched freeze.json
# must be len(am)+1 (the original freeze), so a re-frozen instrument with no amendment entry is refused.
t = subprocess.run(['git', '-C', lane, 'rev-list', '--count', freeze, '--', '%s/freeze.json' % E],
                   capture_output=True, env=env)
try:
    n_touches = int(t.stdout.decode().strip())
except ValueError:
    n_touches = -1
shape_ok = all(isinstance(a, dict) and a.get('n') == i + 1 and isinstance(a.get('what'), str) for i, a in enumerate(am))
if not (shape_ok and n_touches == len(am) + 1):
    bad.append('amendments=%d inconsistent with %d manifest commits or record shape' % (len(am), n_touches))
if (co.get('amendments') or []) != am:
    bad.append('contract.json amendments do not mirror freeze.json amendments')
print('FREEZE_INTEGRITY: %s files=%d amendments=%d freeze=%s' % ('OK' if not bad else 'MISMATCH', len(files), len(am), freeze[:12]))
for b in bad:
    print('FREEZE_MISMATCH', b)
sys.exit(0 if not bad else 1)
PYV
# controls: committed at REV, after the freeze, with their verdict line. The gate is NOT consulted here.
for f in controls-a.stdout controls-a.exit controls-a.stdout.sha256 controls-b.stdout controls-b.exit controls-b.stdout.sha256; do
  p="$E/control/$f"
  git -C "$CL" cat-file -e "$REV:$p" 2>/dev/null || refuse control-receipt-missing "$p"
  [ "$(git -C "$CL" cat-file -t "$REV:$p")" = blob ] || refuse control-receipt-not-a-blob "$p"
  [ "$(git -C "$CL" cat-file -s "$REV:$p")" -gt 0 ] || refuse control-receipt-empty "$p"
  c=$(git -C "$CL" log -1 --format=%H "$REV" -- "$p")
  git -C "$CL" merge-base --is-ancestor "$FREEZE" "$c" || refuse control-receipt-not-after-freeze "$p"
done
for ab in a b; do
  A=$(git -C "$CL" show "$REV:$E/control/controls-$ab.stdout")
  printf '%s\n' "$A" | grep -Eq "^CONTROLS_${ab^^}: ([0-9]+)/\1 as pre-registered" || refuse "controls-$ab-verdict-missing"
  printf '%s\n' "$A" | grep -q 'CTL_MISMATCH' && refuse "controls-$ab-mismatch-lines"
  [ "$(git -C "$CL" show "$REV:$E/control/controls-$ab.exit" | tr -d '[:space:]')" = 0 ] || refuse "controls-$ab-exit-nonzero"
  want=$(git -C "$CL" show "$REV:$E/control/controls-$ab.stdout.sha256" | awk '{print $1; exit}')
  got=$(git -C "$CL" show "$REV:$E/control/controls-$ab.stdout" | sha256sum | awk '{print $1}')
  [ "$want" = "$got" ] || refuse "controls-$ab-digest-mismatch"
done
# cold-read precheck BEFORE any counter: a section that lost credit between BASE and REV (RED), or a precheck
# that could not measure, refuses the run.
git -C "$CL" show "$REV:.ufo/evidence/round-48/quality/coldread-precheck.sh" > "$SCR/precheck.sh"
bash "$SCR/precheck.sh" "$CL" "$BASE" "$REV" > "$SCR/precheck.stdout" 2>&1; prc=$?
if [ "$prc" != 0 ] || grep -q ' RED$' "$SCR/precheck.stdout" || ! tail -1 "$SCR/precheck.stdout" | grep -Eq '^COLDREAD_PRECHECK .* ok$'; then
  cat "$SCR/precheck.stdout"; refuse "coldread-precheck-red exit=$prc"
fi
# ---- gate 0 passed: from here every stdout and exit is captured under OUTDIR ----
say() { echo "$@" | tee -a "$OUT/deciding-run.stdout"; }
cp "$SCR/precheck.stdout" "$OUT/coldread-precheck.stdout"; echo 0 > "$OUT/coldread-precheck.exit"
say "FREEZE_DERIVED freeze=$FREEZE rev=$REV base=$BASE noharm_min=$NOHARM_MIN"
tail -1 "$OUT/coldread-precheck.stdout" | tee -a "$OUT/deciding-run.stdout"
git -C "$CL" show "$REV:tools/receipt-revision-gate.py" > "$SCR/gate/gate.py"
for f in c1/measure.py c2/measure.py no-harm.sh; do
  mkdir -p "$SCR/code/$(dirname "$f")"; git -C "$CL" show "$REV:$E/$f" > "$SCR/code/$f"
done
rc=0
for k in c1 c2; do
  date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/$k.start"
  python3 "$SCR/code/$k/measure.py" --lane "$CL" --rev "$REV" --work "$SCR/$k" --explain > "$OUT/$k.stdout" 2>&1
  echo $? > "$OUT/$k.exit"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$OUT/$k.end"
  tail -1 "$OUT/$k.stdout" | tee -a "$OUT/deciding-run.stdout"
  [ "$(cat "$OUT/$k.exit")" = 0 ] || { say "COUNTER_EXIT_NONZERO $k"; rc=1; }
  K=${k^^}
  grep -q "${K}_R57_PASS=true" "$OUT/$k.stdout" || { say "COUNTER_NOT_PASS $k"; rc=1; }
  grep -q "${K}_R57_PASS=false" "$OUT/$k.stdout" && { say "COUNTER_PASS_FALSE_LINE $k"; rc=1; }
done
bash "$SCR/code/no-harm.sh" "$CL" "$BASE" "$REV" > "$OUT/no-harm.stdout" 2>&1; echo $? > "$OUT/no-harm.exit"
tee -a "$OUT/deciding-run.stdout" < "$OUT/no-harm.stdout" > /dev/null; cat "$OUT/no-harm.stdout"
[ "$(cat "$OUT/no-harm.exit")" = 0 ] || { say "NOHARM_EXIT_NONZERO"; rc=1; }
grep -q 'RED' "$OUT/no-harm.stdout" && { say "NOHARM_RED"; rc=1; }
NH_TOTAL=$(grep -c '^NOHARM ' "$OUT/no-harm.stdout"); NH_OK=$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")
{ [ "$NH_OK" = "$NH_TOTAL" ] && [ "$NH_OK" -ge "$NOHARM_MIN" ]; } || { say "NOHARM_OK_COUNT ok=$NH_OK total=$NH_TOTAL min=$NOHARM_MIN"; rc=1; }
{ echo "FLEET=$FLEET"; "$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi; } > "$OUT/census.stdout" 2> "$OUT/census.stderr"; echo $? > "$OUT/census.exit"
say "CENSUS exit=$(cat "$OUT/census.exit")"; [ "$(cat "$OUT/census.exit")" = 0 ] || rc=1
# gate LAST: it certifies only the verdict receipts this script just produced, at the certified revision.
python3 "$SCR/gate/gate.py" --lane "$CL" --certified "$REV" \
  --receipt "$OUT/c1.stdout:verdict:C1_R57_PASS=" \
  --receipt "$OUT/c2.stdout:verdict:C2_R57_PASS=" \
  > "$OUT/receipt-gate-verdicts.stdout" 2>&1
echo $? > "$OUT/receipt-gate-verdicts.exit"
tail -1 "$OUT/receipt-gate-verdicts.stdout" | tee -a "$OUT/deciding-run.stdout"
[ "$(cat "$OUT/receipt-gate-verdicts.exit")" = 0 ] || rc=1
git status --porcelain | grep -v "^?? $OUTREL/" > "$OUT/clean-tree-after.txt"
[ ! -s "$OUT/clean-tree-after.txt" ] || { say "DECIDING_REFUSED dirty-tree-after"; cat "$OUT/clean-tree-after.txt"; rc=1; }
say "DECIDING_RUN_EXIT=$rc"
echo "DECIDING_RUN_EXIT=$rc" > "$OUT/deciding-run.exit"
exit $rc
