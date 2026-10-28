#!/bin/bash
# Round-54 controls. Phase A is scored at the FREEZE bytes, before any round work;
# phase B at the final content revision, before the deciding run.
#
#   controls.sh a LANE FREEZE BASE OUTDIR
#   controls.sh b LANE FREEZE REV  OUTDIR
#
# Every control runs the FROZEN counter bytes (extracted from FREEZE into scratch),
# never the working tree, over a `git clone --shared` of the lane at the revision the
# control names. Prints "CTL <name> <counter line>" and "CONTROLS_A: <n>/<n> as
# pre-registered" (exit 0 iff every control printed the pre-registered verdict).
# Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r54/controls, removed on exit.
set -u
PHASE=$1; LANE=$2; FREEZE=$3; REV=$4; OUT=$5
case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
E=.ufo/evidence/round-54
SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r54/controls-$PHASE
rm -rf "$SCR"; mkdir -p "$SCR/code" "$SCR/clones"; trap 'rm -rf -- "$SCR"' EXIT
export TMPDIR="$SCR"
cd "$LANE" || exit 2
FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
for f in c1/measure.py c1/lost-headings-at-base.json c2/measure.py; do mkdir -p "$SCR/code/$(dirname $f)"; git show "$FREEZE:$E/$f" > "$SCR/code/$f" || exit 2; done
git show "$FREEZE:.ufo/evidence/round-48/quality/coldread-precheck.sh" > "$SCR/code/precheck.sh"
git show "$FREEZE:.ufo/evidence/round-21/coldread/measure.py" > "$SCR/code/measure-r21.py"
git show "$FREEZE:.ufo/evidence/round-18/measure.py" > "$SCR/code/measure-r18.py"
mkdir -p "$SCR/code/.ufo/evidence/round-21/coldread" "$SCR/code/.ufo/evidence/round-18"
cp "$SCR/code/measure-r21.py" "$SCR/code/.ufo/evidence/round-21/coldread/measure.py"
cp "$SCR/code/measure-r18.py" "$SCR/code/.ufo/evidence/round-18/measure.py"
C1="$SCR/code/c1/measure.py"; C2="$SCR/code/c2/measure.py"
pass=0; fail=0
check () {  # check NAME EXPECTED ACTUAL
  if [ "$2" = "$3" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "CTL_MISMATCH $1 expected=$2 actual=$3"; fi
}
clone_at () {  # clone_at SRC REV NAME -> path
  local d="$SCR/clones/$3"; git clone --shared --quiet "$1" "$d" >/dev/null 2>&1 || return 1
  git -C "$d" -c advice.detachedHead=false checkout --quiet "$2" >/dev/null 2>&1 || return 1
  printf '%s' "$d"
}
verdict () {  # verdict FILE NAMEPASS
  grep -oE "$2=(true|false)" "$1" | tail -1 | cut -d= -f2
}

if [ "$PHASE" = a ]; then
  # CTL_0 — do nothing: the base tree must fail both counters.
  d=$(clone_at "$LANE" "$REV" base) || exit 2
  python3 "$C1" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/w0a" > "$SCR/c0a" 2>&1; v=$(verdict "$SCR/c0a" C1_R54_PASS)
  echo "CTL CTL_0_c1 $(tail -1 "$SCR/c0a")"; check CTL_0_c1 false "$v"
  python3 "$C2" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/w0b" > "$SCR/c0b" 2>&1; v=$(verdict "$SCR/c0b" C2_R54_PASS)
  echo "CTL CTL_0_c2 $(tail -1 "$SCR/c0b")"; check CTL_0_c2 false "$v"

  # CTL_R53 — the round-53 final tree (58/64 credited, a rekey-r53 directory): a prior
  # round's shape must not reach this round's target.
  d=$(clone_at "$LANE" 88afa941545469457c78c7f4014bcda1afdee52c r53 2>/dev/null) || d=""
  if [ -z "$d" ]; then echo "CTL CTL_R53 SKIPPED-unresolvable-ancestor"; else
    python3 "$C1" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/wr53" > "$SCR/cr53" 2>&1; v=$(verdict "$SCR/cr53" C1_R54_PASS)
    echo "CTL CTL_R53 $(tail -1 "$SCR/cr53")"; check CTL_R53 false "$v"
  fi

  # CTL_FAB — a hand-bound entry with a valid trace and no reader: credit alone is not the claim.
  d=$(clone_at "$LANE" "$REV" fab) || exit 2
  python3 - "$d" <<'PY'
import json, subprocess, sys, hashlib, os
lane = sys.argv[1]
E = '.ufo/evidence/round-54'
ledger_path = '.ufo/evidence/round-21/coldread/ledger.json'
ledger = json.loads(subprocess.run(['git', '-C', lane, 'show', 'HEAD:' + ledger_path], capture_output=True, check=True).stdout)
skill = subprocess.run(['git', '-C', lane, 'show', 'HEAD:SKILL.md'], capture_output=True, check=True).stdout
import importlib.util
spec = importlib.util.spec_from_file_location('r18fab', os.path.join(os.environ['TMPDIR'], 'code/measure-r18.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sec = next(s for s in m.sectionize(skill) if s['heading'] == '## Standing rules')
rev = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, check=True).stdout.decode().strip()
inp = 'PROVINCE.md'
blob = subprocess.run(['git', '-C', lane, 'show', 'HEAD:' + inp], capture_output=True, check=True).stdout
sha = hashlib.sha256(blob).hexdigest()
d = os.path.join(lane, E, 'fab', 'traces'); os.makedirs(d, exist_ok=True)
trace_rel = '.ufo/evidence/round-54/fab/traces/fabricated.json'
json.dump({'schema': 'tameshi-trace-inputs-v1', 'argv': ['true'], 'cwd': lane, 'root': lane,
           'rev': rev, 'exit': 0, 'inputs': {inp: sha}, 'external': {},
           'live_lane_reads': {}, 'untracked': []}, open(os.path.join(lane, trace_rel), 'w'))
ledger['entries'].append({'skill_sha256': hashlib.sha256(skill).hexdigest(), 'start': sec['start'],
                          'end': sec['end'], 'heading': sec['heading'], 'sha256': sec['sha256'],
                          'class': 'record', 'verdict': 'verified-record', 'blocking_gaps': 0,
                          'wrong_expectations': 0, 'minor_gaps': 0, 'commands_executed_count': 2,
                          'read_rev': rev, 'inputs': {inp: sha}, 'traces': [trace_rel],
                          'seats': ['fabricated-control']})
open(os.path.join(lane, ledger_path), 'w').write(json.dumps(ledger, indent=1) + '\n')
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
subprocess.run(['git', '-C', lane, 'add', '-A'], check=True, env=env)
subprocess.run(['git', '-C', lane, '-c', 'user.name=fab', '-c', 'user.email=fab@invalid',
                'commit', '--quiet', '-m', 'fabricated control'], check=True, env=env)
PY
  python3 "$C1" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/wfab" > "$SCR/cfab" 2>&1; v=$(verdict "$SCR/cfab" C1_R54_PASS)
  echo "CTL CTL_FAB $(tail -1 "$SCR/cfab")"; check CTL_FAB false "$v"

  # CTL_LOGINPUT — the round-53 failure mode: entries that pin LOG.md, then LOG.md changes.
  d=$(clone_at "$LANE" "$REV" loginput) || exit 2
  python3 - "$d" <<'PY'
import json, subprocess, sys, hashlib, os, importlib.util
lane = sys.argv[1]
ledger_path = '.ufo/evidence/round-21/coldread/ledger.json'
ledger = json.loads(subprocess.run(['git', '-C', lane, 'show', 'HEAD:' + ledger_path], capture_output=True, check=True).stdout)
skill = subprocess.run(['git', '-C', lane, 'show', 'HEAD:SKILL.md'], capture_output=True, check=True).stdout
spec = importlib.util.spec_from_file_location('r18li', os.path.join(os.environ['TMPDIR'], 'code/measure-r18.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
secs = m.sectionize(skill)
rev = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, check=True).stdout.decode().strip()
log_sha = hashlib.sha256(subprocess.run(['git', '-C', lane, 'show', 'HEAD:LOG.md'], capture_output=True, check=True).stdout).hexdigest()
os.makedirs(os.path.join(lane, '.ufo/evidence/round-54', 'loginput', 'traces'), exist_ok=True)
frozen = json.load(open(os.path.join(os.environ['TMPDIR'], 'code/c1/lost-headings-at-base.json')))
for i, h in enumerate(h for h in frozen if any(s['heading'] == h for s in secs)):
    sec = next(s for s in secs if s['heading'] == h)
    trace_rel = '.ufo/evidence/round-54/loginput/traces/%02d.json' % i
    json.dump({'schema': 'tameshi-trace-inputs-v1', 'argv': ['true'], 'cwd': lane, 'root': lane,
               'rev': rev, 'exit': 0, 'inputs': {'LOG.md': log_sha}, 'external': {},
               'live_lane_reads': {}, 'untracked': []}, open(os.path.join(lane, trace_rel), 'w'))
    ledger['entries'].append({'skill_sha256': hashlib.sha256(skill).hexdigest(), 'start': sec['start'],
                              'end': sec['end'], 'heading': sec['heading'], 'sha256': sec['sha256'],
                              'class': 'record', 'verdict': 'verified-record', 'blocking_gaps': 0,
                              'wrong_expectations': 0, 'minor_gaps': 0, 'commands_executed_count': 2,
                              'read_rev': rev, 'inputs': {'LOG.md': log_sha}, 'traces': [trace_rel],
                              'seats': ['loginput-control']})
open(os.path.join(lane, ledger_path), 'w').write(json.dumps(ledger, indent=1) + '\n')
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
with open(os.path.join(lane, 'LOG.md'), 'a') as fh:
    fh.write('\nloginput control tail\n')
subprocess.run(['git', '-C', lane, 'add', '-A'], check=True, env=env)
subprocess.run(['git', '-C', lane, '-c', 'user.name=li', '-c', 'user.email=li@invalid',
                'commit', '--quiet', '-m', 'loginput control'], check=True, env=env)
PY
  python3 "$C1" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/wli" > "$SCR/cli" 2>&1; v=$(verdict "$SCR/cli" C1_R54_PASS)
  echo "CTL CTL_LOGINPUT $(tail -1 "$SCR/cli")"; check CTL_LOGINPUT false "$v"
  echo "CONTROLS_A: $pass/$((pass+fail)) as pre-registered"
  [ "$fail" = 0 ] || exit 1
  exit 0
fi

if [ "$PHASE" = b ]; then
  # CTL_POS — the real repair at REV must pass both counters.
  d=$(clone_at "$LANE" "$REV" pos) || exit 2
  python3 "$C1" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/wposa" > "$SCR/cposa" 2>&1; v=$(verdict "$SCR/cposa" C1_R54_PASS)
  echo "CTL CTL_POS_c1 $(tail -1 "$SCR/cposa")"; check CTL_POS_c1 true "$v"
  python3 "$C2" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/wposb" > "$SCR/cposb" 2>&1; v=$(verdict "$SCR/cposb" C2_R54_PASS)
  echo "CTL CTL_POS_c2 $(tail -1 "$SCR/cposb")"; check CTL_POS_c2 true "$v"

  # CTL_EXIT0 — a tool made to print the class line but return 0 must fail C2.
  d=$(clone_at "$LANE" "$REV" exit0) || exit 2
  python3 - "$d" <<'PY'
import subprocess, sys
lane = sys.argv[1]
path = lane + '/tools/registry-check.py'
src = open(path).read()
old = '            print(f"registry-check: could-not-evaluate: {exc}", file=sys.stderr)\n            return 2'
assert src.count(old) == 1, 'anchor not unique'
src = src.replace(old, '            print(f"registry-check: could-not-evaluate: {exc}", file=sys.stderr)\n            return 0')
open(path, 'w').write(src)
env = {k: v for k, v in __import__('os').environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
subprocess.run(['git', '-C', lane, 'add', '-A'], check=True, env=env)
subprocess.run(['git', '-C', lane, '-c', 'user.name=e0', '-c', 'user.email=e0@invalid',
                'commit', '--quiet', '-m', 'exit0 control'], check=True, env=env)
PY
  python3 "$C2" --lane "$d" --rev "$(git -C "$d" rev-parse HEAD)" --work "$SCR/we0" > "$SCR/ce0" 2>&1; v=$(verdict "$SCR/ce0" C2_R54_PASS)
  echo "CTL CTL_EXIT0 $(tail -1 "$SCR/ce0")"; check CTL_EXIT0 false "$v"
  echo "CONTROLS_B: $pass/$((pass+fail)) as pre-registered"
  [ "$fail" = 0 ] || exit 1
  exit 0
fi
echo "phase must be a or b"; exit 2
