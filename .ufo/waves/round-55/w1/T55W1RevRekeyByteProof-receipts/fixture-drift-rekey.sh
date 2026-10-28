#!/bin/bash
# T55W1RevRekeyByteProof fixture: prove the drift/re-key/coverage mechanics with the
# FROZEN credit code, in a scratch clone only. Every git mutation names $CL.
set -u
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r55/T55W1RevRekeyByteProof
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CL=$S/clone
test "$(git -C "$CL" rev-parse --show-toplevel)" = "$CL" || exit 9

cov() { # cov REV -> covered/total + the Standing-rules record
  python3 - "$CL" "$1" "$S" <<'PY'
import importlib.util, os, subprocess, sys, tempfile
lane, rev, S = sys.argv[1:4]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
def git(*a): return subprocess.run(['git', '-C', lane, *a], capture_output=True, env=env)
work = tempfile.mkdtemp(dir=S + '/tmp')
p = os.path.join(work, 'r18.py')
open(p, 'wb').write(git('show', rev + ':.ufo/evidence/round-18/measure.py').stdout)
spec = importlib.util.spec_from_file_location('r18', p); m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
skill = git('show', rev + ':SKILL.md').stdout
ledger = git('show', rev + ':.ufo/evidence/round-21/coldread/ledger.json').stdout
out = m.coldread(lane, rev, skill, ledger, strict=True)
st = [(s['credited'], s['reason']) for s in out['sections'] if s['heading'] == '## Standing rules']
print('COVERAGE rev=%s covered=%d/%d standing=%s' % (rev[:12], out['sections_covered'],
      out['sections_total'], st))
PY
}

commit() { git -C "$CL" add -A && git -C "$CL" -c user.email=f@invalid -c user.name=f \
  commit -q -m "$1" && git -C "$CL" rev-parse HEAD; }

echo "== 0. baseline"
cov "$(git -C "$CL" rev-parse HEAD)"

echo "== 1. content commit C55: replace the round-54 C2 sentence in ## Standing rules"
python3 - "$CL" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / 'SKILL.md'
t = p.read_text(encoding='utf-8')
old = ("  1. Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter);\n"
       "  other modes are outside that measurement.")
new = ("  1. Measured on every documented allocating mode (round-55 C2 counter): one\n"
       "  stderr line, exit 2. FIXTURE BYTES, not the round-55 wording.")
if old in t:
    p.write_text(t.replace(old, new), encoding='utf-8')
    print('replaced the C54 sentence verbatim')
else:
    # fall back to the subsection rewrite: append a marker line inside the section
    marker = '  `--selftest`/`selftest` path'
    lines = t.split('\n')
    for i, line in enumerate(lines):
        if marker in line:
            lines[i] = '  FIXTURE-SENTENCE round-55 (no selftest-scope claim).'
            print('replaced line %d containing %r' % (i + 1, marker))
            break
    else:
        # last resort: same effect, different anchor - the section must change
        for i, line in enumerate(lines):
            if line.startswith('- **The scratch root has three arms.**'):
                lines[i] = line + ' FIXTURE-R55'
                print('marker appended at line %d' % (i + 1))
                break
    p.write_text('\n'.join(lines), encoding='utf-8')
PY
C55=$(commit "fixture: round-55 standing-rules drift")
echo "C55=$C55"
cov "$C55" | tee "$S/receipts/coverage-after-drift.txt"

echo "== 2. freeze reader: reader-section.py at C55"
python3 "$LANE/.ufo/waves/round-54/reader-section.py" "$CL" "$C55" "## Standing rules" \
  | tee "$S/receipts/reader-section-at-c55.json"

echo "== 3. genuinely read the new section (empty findings) and commit the report"
python3 - "$CL" "$C55" "$LANE" <<'PY'
import json, subprocess, sys
cl, c55, lane = sys.argv[1:4]
d = json.loads(subprocess.run(['python3', lane + '/.ufo/waves/round-54/reader-section.py',
                               cl, c55, '## Standing rules'],
                              capture_output=True, text=True, check=True).stdout)
rep = {'heading': d['heading'], 'cand': d['cand'], 'section_sha256': d['section_sha256'],
       'findings': []}
base = cl + '/.ufo/waves/round-54/w1/T55W1ReadBYTEPROOF'
json.dump(rep, open(base + '.json', 'w'))
open(base + '.md', 'w').write('# %s re-read at %s\n' % (d['heading'], c55[:12]))
print(json.dumps(rep))
PY

echo "== 4. frozen round-54 binder, C0=PIN=C55"
OUT="$CL/.ufo/evidence/round-21/coldread/rekey-r55-$(echo "$C55" | cut -c1-12)"
mkdir -p "$OUT"
python3 "$LANE/.ufo/evidence/round-54/integrate/binder.py" "$CL" "$C55" "$C55" "$OUT" 2>&1 | tail -8
C55B=$(commit "fixture: bind the re-keyed entry")
echo "C55B=$C55B"
cov "$C55B" | tee "$S/receipts/coverage-after-rekey.txt"

echo "== 5. a LATER SKILL.md edit (C56) with the C55 reader in place"
python3 - "$CL" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / 'SKILL.md'
t = p.read_text(encoding='utf-8')
t = t.replace('FIXTURE-SENTENCE round-55 (no selftest-scope claim).',
              'FIXTURE-SENTENCE round-55 v2 (edited AFTER the reader read).')
t = t.replace('FIXTURE BYTES, not the round-55 wording.',
              'FIXTURE BYTES v2, edited AFTER the reader read.')
p.write_text(t, encoding='utf-8')
PY
C56=$(commit "fixture: a later standing-rules edit")
echo "C56=$C56"
cov "$C56" | tee "$S/receipts/coverage-after-later-edit.txt"

echo "== 6. the same reader judged at C56 (section-at-own-cand vs section-at-REV)"
python3 "$S/validate-reader.py" --lane "$CL" --rev "$C56" --c0 "$C55" --mode all \
  "$CL/.ufo/waves/round-54/w1/T55W1ReadBYTEPROOF.json" | tee "$S/receipts/reader-at-c55-judged-at-c56.txt"
