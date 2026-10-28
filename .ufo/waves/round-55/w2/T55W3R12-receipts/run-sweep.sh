#!/usr/bin/env bash
# T55W3R12 — read the SKILL.md section `### Round-15 gate/probe registry` at C0
# and judge it against the tree at C0. Every block below is one receipt file.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
REV=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
R="$(cd "$(dirname "$0")" && pwd)"
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r55/T55W3R12
mkdir -p "$S"; export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"
C=$S/clone
[ -d "$C/.git" ] || { git clone --shared --quiet "$LANE" "$C" && git -C "$C" checkout --quiet --detach "$REV"; }
echo "clone toplevel: $(git -C "$C" rev-parse --show-toplevel)"
echo "clone HEAD: $(git -C "$C" rev-parse HEAD)"
cd "$C" || exit 1

{
  echo "## command: frozen sectionizer .ufo/evidence/round-18/measure.py -> sectionize(SKILL.md@$REV)"
  python3 - "$LANE" "$REV" <<'PY'
import importlib.util, subprocess, sys, hashlib
lane, rev = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('m18', lane + '/.ufo/evidence/round-18/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw = subprocess.run(['git','-C',lane,'show',rev+':SKILL.md'],capture_output=True,check=True).stdout
secs = m.sectionize(raw)
hit = [s for s in secs if s['heading'] == '### Round-15 gate/probe registry']
print('sections =', len(secs), 'matches for heading =', len(hit))
for s in hit: print('sectionize:', s)
s = hit[0]
lines = raw.decode('utf-8','surrogateescape').split('\n')
body = lines[s['start']-1:s['end']]
while body and body[-1].strip() == '': body.pop()
joined = '\n'.join(body)
print('independent re-derivation equal:', 'yes' if hashlib.sha256(joined.encode('utf-8','surrogateescape')).hexdigest() == s['sha256'] else 'NO')
print('body lines =', len(body), 'body bytes =', len(joined.encode('utf-8','surrogateescape')))
PY
} > "$R/01-section-sha.txt" 2>&1

{
  echo "## command: path sweep of every backticked path token in the section, resolved at $REV"
  python3 - "$REV" <<'PY'
import re, subprocess, sys
rev = sys.argv[1]
out = subprocess.run(['git','show',rev+':SKILL.md'],capture_output=True,check=True).stdout.decode('utf-8','surrogateescape').split('\n')
text = '\n'.join(out[1705:1736])
cand = set()
for span in re.findall(r'`([^`]+)`', text):
    for tok in span.split():
        tok = tok.strip('(),;')
        if re.match(r'^(\.ufo|tools|corpus)/[A-Za-z0-9._/-]+$', tok): cand.add(tok)
for p in sorted(cand):
    r = subprocess.run(['git','cat-file','-t',rev+':'+p],capture_output=True)
    print(('OK   ' + r.stdout.decode().strip()) if r.returncode == 0 else 'MISS', p)
print('--- command spans in the section ---')
for c in dict.fromkeys(s for s in re.findall(r'`([^`]+)`', text) if s.startswith('python3 ') or s.startswith('git ')):
    print(c)
PY
} > "$R/02-path-sweep.txt" 2>&1

{
  echo "## command: sha256 of every pinned evidence file at $REV (section pins 05cb... and 1ee9...)"
  for f in .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/context-missing-env.json .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-18/dispositions.json; do
    printf '%s  %s\n' "$(git show "$REV:$f" | sha256sum | cut -d' ' -f1)" "$f"
  done
  echo "## section claim 'historical expected pins 13 original inputs':"
  git show "$REV:.ufo/evidence/round-13/expected.json" | python3 -c 'import json,sys; d=json.load(sys.stdin); print("inputs entries =", len(d["inputs"]))'
  echo "## section claim 'its built-in id/exit pin in tool' — literal receipt digest in the tool:"
  git show "$REV:tools/context-capture.py" | grep -n "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a" | head -2
} > "$R/03-pinned-values.txt" 2>&1

{
  echo "## command: python3 tools/context-capture.py --check"; python3 tools/context-capture.py --check; echo "rc=$?"
  echo; echo "## command: python3 tools/context-capture.py --selftest | tail -1"; python3 tools/context-capture.py --selftest | tail -1
  echo "## command: python3 tools/context-capture.py --selftest >/dev/null"; python3 tools/context-capture.py --selftest >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: python3 tools/context-capture.py --help   (section: help exits0, non-verdict informational mode)"; python3 tools/context-capture.py --help >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: python3 tools/context-capture.py --check --receipt   (section: 64 usage, no receipt)"; python3 tools/context-capture.py --check --receipt >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: TMPDIR=/nonexistent-r55 python3 tools/context-capture.py --selftest   (section: 2 could-not-evaluate, named, never a traceback)"
  TMPDIR=/nonexistent-r55 python3 tools/context-capture.py --selftest 2>&1 | head -3
  TMPDIR=/nonexistent-r55 python3 tools/context-capture.py --selftest >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: TMPDIR= python3 tools/context-capture.py --selftest   (empty TMPDIR reads as unset)"; TMPDIR= python3 tools/context-capture.py --selftest >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: --check --receipt FILE --expected FILE with a valid expected pin   (section: 0 clean)"
  U="$S/unread2"; mkdir -p "$U"; cp .ufo/evidence/round-14/context-receipt.json "$U/receipt.json"
  sha=$(sha256sum .ufo/evidence/round-14/context-receipt.json | cut -d' ' -f1)
  printf '{"schema":"tameshi-context-expected-v1","receipt_sha256":"%s","id":"context_consistent","exit":0}\n' "$sha" > "$U/expected.json"
  python3 tools/context-capture.py --check --receipt "$U/receipt.json" --expected "$U/expected.json"; echo "rc=$?"
  echo; echo "## command: same, receipt chmod 000   (section: unavailable input stays could-not-evaluate)"; chmod 000 "$U/receipt.json"
  python3 tools/context-capture.py --check --receipt "$U/receipt.json" --expected "$U/expected.json" 2>&1 | head -3
  python3 tools/context-capture.py --check --receipt "$U/receipt.json" --expected "$U/expected.json" >/dev/null 2>&1; echo "rc=$?"; chmod 644 "$U/receipt.json"
  echo; echo "## command: same, valid-but-different exit pin (exit 1) on a clean result   (section: failed/exit1)"
  printf '{"schema":"tameshi-context-expected-v1","receipt_sha256":"%s","id":"context_consistent","exit":1}\n' "$sha" > "$U/expected-wrong.json"
  python3 tools/context-capture.py --check --receipt "$U/receipt.json" --expected "$U/expected-wrong.json" 2>&1 | head -3
  python3 tools/context-capture.py --check --receipt "$U/receipt.json" --expected "$U/expected-wrong.json" >/dev/null 2>&1; echo "rc=$?"
} > "$R/04-arms-context-capture.txt" 2>&1

{
  echo "## the section's disposition entry commands, at C0"
  for d in .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-17/dispositions.json .ufo/evidence/round-18/dispositions.json; do
    echo; echo "## command: python3 tools/evidence-disposition.py --root . --dispositions $d --json"
    python3 tools/evidence-disposition.py --root . --dispositions "$d" --json > "$S/out.json" 2>&1; rc=$?
    python3 - "$S/out.json" "$rc" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
    print("exit =", d.get("exit"), "| status =", d.get("status"), "| id =", d.get("id"),
          "| first finding =", (d.get("findings") or [{}])[0].get("id"), "| counts =", d.get("counts"))
except Exception as exc:
    print("unparseable:", exc); print(open(sys.argv[1]).read()[:300])
print("process rc =", sys.argv[2])
PY
  done
  echo; echo "## command: python3 tools/evidence-disposition.py --selftest | tail -1"; python3 tools/evidence-disposition.py --selftest | tail -1
  echo "## command: python3 tools/evidence-disposition.py --selftest >/dev/null"; python3 tools/evidence-disposition.py --selftest >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: python3 tools/evidence-disposition.py --help"; python3 tools/evidence-disposition.py --help >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: python3 tools/evidence-disposition.py --selftest --json   (section: 64 usage)"; python3 tools/evidence-disposition.py --selftest --json >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: TMPDIR=/nonexistent-r55 python3 tools/evidence-disposition.py --selftest   (section: 2, named, no traceback)"
  TMPDIR=/nonexistent-r55 python3 tools/evidence-disposition.py --selftest 2>&1 | head -3
  TMPDIR=/nonexistent-r55 python3 tools/evidence-disposition.py --selftest >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: TMPDIR= python3 tools/evidence-disposition.py --selftest"; TMPDIR= python3 tools/evidence-disposition.py --selftest >/dev/null 2>&1; echo "rc=$?"
  echo; echo "## command: --dispositions <chmod 000 file>   (section: an unreadable input is named, never a traceback)"
  D="$S/unread3"; mkdir -p "$D"; cp .ufo/evidence/round-18/dispositions.json "$D/dispositions.json"; chmod 000 "$D/dispositions.json"
  python3 tools/evidence-disposition.py --root . --dispositions "$D/dispositions.json" --json 2>&1 | head -5
  python3 tools/evidence-disposition.py --root . --dispositions "$D/dispositions.json" --json >/dev/null 2>&1; echo "rc=$?"; chmod 644 "$D/dispositions.json"
} > "$R/05-arms-disposition.txt" 2>&1

{
  echo "## command: cwd = extracted 'git archive 28aeef4'   (section: frozen replay -> 0)"
  F="$S/frozen"; rm -rf "$F"; mkdir -p "$F"; git archive 28aeef4 | tar -x -C "$F"
  echo "archive commit = $(git rev-parse 28aeef4^{commit})"
  cd "$F" || exit 1
  python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json > "$S/frozen.json" 2>&1; rc=$?
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print("status =",d.get("status"),"| exit =",d.get("exit"),"| counts =",d.get("counts"))' "$S/frozen.json"
  echo "rc=$rc"
} > "$R/06-frozen-replay.txt" 2>&1
cd "$C" || exit 1

{
  echo "## section states: 'the six recorded cases at this write (seven since round 16)'"
  echo "## measured with the frozen round-18 counter pattern  ^#   (js|bash)-<name> <path> n/m  in tools/mutate-and-run.sh"
  echo
  for r in 9f2c86f 0494c24 017a2b0 9ee1c80 5b703c6 99c3bc8 0a2010ac 9cf0146b; do
    n=$(git show "$r":tools/mutate-and-run.sh 2>/dev/null | grep -cE '^#   (js|bash)-[^ ]+[[:space:]]+[^ ]+[[:space:]]+[0-9]+/[0-9]+')
    what=$(git log -1 --format=%s "$r" | cut -c1-56)
    printf '%-10s recorded_cases=%-3s %s\n' "$r" "$n" "$what"
  done
  echo
  echo "## frozen counter on the C0 blob:"
  python3 - "$LANE" "$REV" <<'PY'
import subprocess, sys, re
lane, rev = sys.argv[1], sys.argv[2]
raw = subprocess.run(['git','-C',lane,'cat-file','blob',rev+':tools/mutate-and-run.sh'],capture_output=True,check=True).stdout.decode('utf-8','surrogateescape')
hits = re.compile(r'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', re.MULTILINE).findall(raw)
print('recorded_cases =', len(hits), '(depth_score =', min(10, len(hits)), ')')
print('legs:', [h.split()[1] for h in hits])
PY
} > "$R/07-case-counts.txt" 2>&1

{
  echo "## command: inspect tools/registry.json for the two registered gates   (section: no sibling gate registered or executed)"
  python3 - <<'PY'
import json
rows = json.load(open('tools/registry.json'))['rows']
print('registry rows =', len(rows), '| kinds =', sorted({r['kind'] for r in rows}))
for r in rows:
    blob = json.dumps({k: v for k, v in r.items() if k != 'scratch_root'})
    if 'context-capture' in blob or 'evidence-disposition' in blob:
        print('-', r['name'], '| kind', r['kind'], '| status', r.get('status'), '| expect', r.get('expect'))
        print('  source', r.get('source'), '| superseded_by', r.get('superseded_by'))
print('rows whose argv names another lane:',
      [r['name'] for r in rows if any('/' in a and a.split('/')[0].endswith('-shokunin') for a in r.get('argv', []))])
PY
} > "$R/08-registry-rows.txt" 2>&1

{
  echo "## section row write scope: 'writes nothing' / 'stdout only'"
  before_c=$(git status --porcelain | wc -l); before_t=$(find "$TMPDIR" -mindepth 1 | wc -l)
  python3 tools/context-capture.py --check >/dev/null 2>&1; r1=$?
  python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json >/dev/null 2>&1; r2=$?
  after_c=$(git status --porcelain | wc -l); after_t=$(find "$TMPDIR" -mindepth 1 | wc -l)
  echo "rcs: context-capture=$r1 disposition=$r2"
  echo "clone dirty count: $before_c -> $after_c"
  echo "TMPDIR entries: $before_t -> $after_t"
} > "$R/09-writes-nothing.txt" 2>&1

{
  echo "## section tail: 'the disposition selftest: 0 pass, 1 case failure, 2 could-not-evaluate'"
  echo "## exit 0 = clean run (05-arms-disposition), exit 2 = unusable root (05-arms-disposition), exit 1 proved by injection:"
  M="$S/clone-mut"; rm -rf "$M"; cp -a "$C" "$M"; cd "$M" || exit 1
  python3 - <<'PY'
p = 'tools/evidence-disposition.py'; s = open(p, encoding='utf-8').read()
old = 'record(usage_name, proc.returncode == 64, "exit={} expects=64".format(proc.returncode))'
assert old in s, 'anchor missing'
s = s.replace(old, 'record(usage_name, proc.returncode == 65, "exit={} expects=65 (r55-injected)".format(proc.returncode))', 1)
open(p, 'w', encoding='utf-8').write(s)
print('injected: usage-arm expectation 64 -> 65 (scratch clone only; the lane file is untouched)')
PY
  echo "## command: python3 tools/evidence-disposition.py --selftest   (mutated scratch copy)"
  python3 tools/evidence-disposition.py --selftest 2>&1 | tail -3
  python3 tools/evidence-disposition.py --selftest >/dev/null 2>&1; echo "rc=$?"
} > "$R/10-selftest-fail-arm.txt" 2>&1

cd "$R" || exit 1
echo "receipts in $R:"; ls -1 "$R"
