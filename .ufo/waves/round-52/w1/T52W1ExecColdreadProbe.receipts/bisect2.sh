#!/bin/bash
# Round-52 cold-read probe, part 2: fixed (b), full stack, floor, tolerance.
set -u
S=/fast/scratch/hyaku/tameshi-r52/T52W1ExecColdreadProbe
C=$S/clone
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
M=$C/.ufo/evidence/round-21/coldread/measure.py
OUT=$S/out
mkdir -p "$OUT"
top=$(git -C "$C" rev-parse --show-toplevel) || exit 2
[ "$top" = "$C" ] || { echo "ABORT toplevel=$top"; exit 2; }

commit_variant() {  # name
  local v=$1
  git -C "$C" add -A >/dev/null 2>&1
  git -C "$C" -c user.name='hyaku-fixture' -c user.email='fixture@tameshi.invalid' \
      commit -q -m "fixture: round-52 coldread probe variant $v" || return 2
}

run_variant() {  # name edits...
  local v=$1; shift
  git -C "$C" checkout -q -B "$v" "$BASE" || return 2
  git -C "$C" reset -q --hard "$BASE" || return 2
  if [ "$#" -gt 0 ] && [ "$1" != "-" ]; then
    python3 "$S/apply_edits.py" "$C" "$@" >> "$OUT/edits-$v.log" 2>&1 || {
      echo "VARIANT $v EDIT-FAIL"; return 2; }
  fi
  local msg="fixture: round-52 coldread probe variant $v"
  git -C "$C" add -A >/dev/null 2>&1
  git -C "$C" -c user.name='hyaku-fixture' -c user.email='fixture@tameshi.invalid' \
      commit -q --allow-empty -m "$msg" || { echo "VARIANT $v COMMIT-FAIL"; return 2; }
  local sha; sha=$(git -C "$C" rev-parse HEAD)
  printf '%s %s\n' "$v" "$sha" >> "$OUT/shAs2.txt"
  local pre pstat meas mstat
  HYAKU_SCRATCH="$S" bash "$LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh" \
      "$C" "$BASE" "$sha" > "$OUT/precheck-$v.txt" 2>&1
  pstat=$?
  python3 "$M" --repo "$C" --rev "$sha" --explain > "$OUT/measure-$v.json" 2> "$OUT/measure-$v.err"
  mstat=$?
  echo "VARIANT $v sha=$sha precheck_exit=$pstat measure_exit=$mstat"
}

run_variant vbase -              # empty commit: floor self-check
run_variant vb b
run_variant vall a b c d e

# tolerance: synthetic entry carrying extra keys findings/reader_files
git -C "$C" checkout -q -B vtol "$BASE"; git -C "$C" reset -q --hard "$BASE"
python3 - "$C" <<'PY' >> "$OUT/tolerance.log" 2>&1
import json, sys
p = sys.argv[1] + '/.ufo/evidence/round-21/coldread/ledger.json'
d = json.load(open(p))
entry = {
    'skill_sha256': 'synthetic-probe-sha',
    'start': 1,
    'end': 1,
    'heading': '# synthetic probe entry (not a SKILL.md section)',
    'sha256': '0' * 64,
    'class': 'record',
    'verdict': 'verified-record',
    'blocking_gaps': 0,
    'wrong_expectations': 0,
    'minor_gaps': 0,
    'commands_executed_count': 1,
    'read_rev': None,
    'inputs': {},
    'seats': ['T52W1ExecColdreadProbe'],
    'reports': [],
    'findings': ['synthetic finding: monitor must ignore unknown entry keys'],
    'reader_files': ['corpus/knowledge/fleet-kill-rate-ledger.md'],
}
d['entries'].append(entry)
json.dump(d, open(p, 'w'), indent=2)
print('tolerance: appended synthetic entry with findings+reader_files; entries=%d' % len(d['entries']))
PY
commit_variant vtol || exit 2
sha=$(git -C "$C" rev-parse HEAD); echo "VARIANT vtol sha=$sha" >> "$OUT/shAs2.txt"
python3 "$M" --repo "$C" --rev "$sha" --explain > "$OUT/measure-vtol.json" 2> "$OUT/measure-vtol.err"
echo "VARIANT vtol measure_exit=$?"

# tolerance 2: extra keys on an existing credited entry (section 1964 creditor)
git -C "$C" checkout -q -B vtol2 "$BASE"; git -C "$C" reset -q --hard "$BASE"
python3 - "$C" "$LANE" <<'PY' >> "$OUT/tolerance.log" 2>&1
import json, subprocess, sys
clone, lane = sys.argv[1], sys.argv[2]
p = clone + '/.ufo/evidence/round-21/coldread/ledger.json'
d = json.load(open(p))
base_ledger = json.loads(subprocess.run(['git','-C',lane,'show',
    'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:.ufo/evidence/round-21/coldread/ledger.json'],
    capture_output=True, check=True).stdout)
skill = subprocess.run(['git','-C',lane,'show',
    'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:SKILL.md'],
    capture_output=True, check=True).stdout
hits = 0
for e in d['entries']:
    if e.get('inputs') and 'tools/registry.json' in e['inputs'] and 'tools/round21-measure.py' in e['inputs']:
        e['findings'] = ['reader finding recorded for tolerance probe']
        e['reader_files'] = ['tools/registry.json', 'tools/round21-measure.py']
        hits += 1
json.dump(d, open(p, 'w'), indent=2)
print('tolerance2: added findings/reader_files to %d entries' % hits)
PY
commit_variant vtol2 || exit 2
sha=$(git -C "$C" rev-parse HEAD); echo "VARIANT vtol2 sha=$sha" >> "$OUT/shAs2.txt"
python3 "$M" --repo "$C" --rev "$sha" --explain > "$OUT/measure-vtol2.json" 2> "$OUT/measure-vtol2.err"
echo "VARIANT vtol2 measure_exit=$?"

echo "--- precheck summaries part 2 ---"
for v in vbase vb vall; do echo "## $v"; cat "$OUT/precheck-$v.txt"; done
