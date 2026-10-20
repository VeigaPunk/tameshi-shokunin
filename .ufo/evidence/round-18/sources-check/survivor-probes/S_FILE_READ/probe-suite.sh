#!/usr/bin/env bash
# probe-suite.sh — off-suite input probe for tameshi round-18 C1 defect S_FILE_READ:
# kumitate scripts/sources-check.mjs @ 0acb7752, the per-entry knowledge read
# catch at :355-357 (`return failClosed('READ_FAILED', `cannot read ${relPath} ...`)`).
#
# Usage: bash probe-suite.sh ARTIFACT
#   under mutate-and-run.sh: --suite 'bash <this file> "$MUTANT"'
# SHOW=1 also prints every run's full stdout.
# Exit: 0 = ARTIFACT keeps the pristine observable outputs on every witness;
#       1 = it does not; 125 = a witness precondition failed. Preconditions do not
#       depend on ARTIFACT, so under mutate-and-run.sh a 125 turns the control run
#       red (SETUP) and can never be attributed as a kill.
#
# Witnesses: each starts from ./fixture (byte-identical to the selftest's own
# `clean` fixture: SOURCES.md row S001 mined, used-by corpus/knowledge/alpha.md,
# knowledge/alpha.md = BASE_ENTRY) and adds exactly one direct
# corpus/knowledge/*.md regular-file entry that readdirSync lists
# (Dirent.isFile(), name ends with .md) but readFileSync cannot open:
#   clean         the unmodified fixture (expected CLEAN, exit 0)
#   eacces        alpha.md chmod 000 (needs a reader without root / CAP_DAC_*)
#   enoent        extra regular file named b'\xff.md'; readdirSync decodes the name
#                 to U+FFFD + '.md', whose UTF-8 re-encoding names no file
#   enametoolong  the fixture under a 3883-byte --self; an extra entry with a
#                 253-byte name puts join(knowledgeDir, name) past PATH_MAX
# Pristine expectation per failing witness: exit 2 (text and --json), first line
# `SOURCES  fail-closed  READ_FAILED  <detail>`, final line
# `SOURCES_CHECK: FAIL-CLOSED (READ_FAILED)`, --json verdict FAIL-CLOSED,
# exitCode 2, failClosed.kind READ_FAILED, failClosed.detail <detail>.
set -u -o pipefail

art=${1:?usage: probe-suite.sh ARTIFACT}
here=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
fx="$here/fixture/corpus"
today=2026-10-19
tmp=$(mktemp -d "${TMPDIR:-/tmp}/s-file-read-probe.XXXXXX") || exit 125
trap 'rm -rf "$tmp"' EXIT

if ! table=$(python3 - "$tmp" "$fx" <<'PYEOF'
import os, shutil, sys

tmp, fx = sys.argv[1], sys.argv[2]
alpha = open(os.path.join(fx, 'knowledge', 'alpha.md'), 'rb').read()


def fail(msg):
    sys.stderr.write('precondition: %s\n' % msg)
    sys.exit(125)


def fixture(root):
    os.makedirs(root)
    shutil.copytree(fx, os.path.join(root, 'corpus'))
    return root


rows = [('clean', fixture(os.path.join(tmp, 'clean')), '')]

root = fixture(os.path.join(tmp, 'eacces'))
path = os.path.join(root, 'corpus', 'knowledge', 'alpha.md')
os.chmod(path, 0)
if os.access(path, os.R_OK):
    fail('eacces: alpha.md mode 000 is still readable (root or CAP_DAC_* reader)')
rows.append(('eacces', root, 'cannot read corpus/knowledge/alpha.md (EACCES)'))

root = fixture(os.path.join(tmp, 'enoent'))
kdir = os.fsencode(os.path.join(root, 'corpus', 'knowledge'))
with open(os.path.join(kdir, b'\xff.md'), 'wb') as fh:
    fh.write(alpha)
if os.path.lexists(os.path.join(kdir, '\ufffd.md'.encode('utf-8'))):
    fail('enoent: U+FFFD.md exists')
if sorted(os.listdir(kdir)) != [b'alpha.md', b'\xff.md']:
    fail('enoent: unexpected entries %r' % sorted(os.listdir(kdir)))
rows.append(('enoent', root, 'cannot read corpus/knowledge/\ufffd.md (ENOENT)'))

deep = os.path.join(tmp, 'enametoolong')
tail = len('/corpus/knowledge')
while len(deep) + 1 + 200 + tail <= 3900:
    deep = os.path.join(deep, 'd' * 200)
pad = 3900 - tail - len(deep) - 1
if pad > 0:
    deep = os.path.join(deep, 'p' * pad)
root = fixture(deep)
kdir = os.path.join(root, 'corpus', 'knowledge')
name = 'z' * 250 + '.md'
dfd = os.open(kdir, os.O_RDONLY | os.O_DIRECTORY)
try:
    with open(os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644, dir_fd=dfd), 'wb') as fh:
        fh.write(alpha)
finally:
    os.close(dfd)
pmax = os.pathconf(kdir, 'PC_PATH_MAX')
if not (len(os.path.join(root, 'corpus', 'SOURCES.md')) < pmax
        and len(os.path.join(kdir, 'alpha.md')) < pmax <= len(os.path.join(kdir, name))):
    fail('enametoolong: path geometry does not straddle PATH_MAX=%d' % pmax)
rows.append(('enametoolong', root, 'cannot read corpus/knowledge/%s (ENAMETOOLONG)' % name))

for row in rows:
    print('\t'.join(row))
PYEOF
); then
  printf 'PROBE_VERDICT: PRECONDITION (witness build failed)\n'
  exit 125
fi

jsonFields='const j = JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"));
const fc = j.failClosed ?? { kind: "-", detail: "-" };
process.stdout.write([j.verdict, j.exitCode, fc.kind, fc.detail].join("\t"));'

total=0
passed=0
while IFS=$'\t' read -r name self detail; do
  [[ -n "$name" ]] || continue
  total=$((total + 1))
  out="$tmp/$name.out"
  jout="$tmp/$name.json"
  node "$art" --self "$self" --today "$today" >"$out" 2>"$tmp/$name.err"
  rc=$?
  node "$art" --self "$self" --today "$today" --json >"$jout" 2>"$tmp/$name.json.err"
  jrc=$?
  first=$(sed -n '1p' "$out")
  last=$(sed -n '$p' "$out")
  if ! jf=$(node -e "$jsonFields" "$jout" 2>&1); then printf -v jf 'UNPARSEABLE\t-\t-\t%s' "${jf//$'\n'/ }"; fi
  IFS=$'\t' read -r jverdict jexit jkind jdetail <<<"$jf"
  if [[ "$name" == clean ]]; then
    want='exit=0 final=SOURCES_CHECK: CLEAN (rows=1 ...) json=CLEAN/0'
    [[ $rc -eq 0 && $jrc -eq 0 && "$last" == 'SOURCES_CHECK: CLEAN (rows=1 '* \
      && "$jverdict" == CLEAN && "$jexit" == 0 ]]
  else
    want="exit=2 final=SOURCES_CHECK: FAIL-CLOSED (READ_FAILED) json=FAIL-CLOSED/2/READ_FAILED"
    [[ $rc -eq 2 && $jrc -eq 2 && "$first" == "SOURCES  fail-closed  READ_FAILED  $detail" \
      && "$last" == 'SOURCES_CHECK: FAIL-CLOSED (READ_FAILED)' && "$jverdict" == FAIL-CLOSED \
      && "$jexit" == 2 && "$jkind" == READ_FAILED && "$jdetail" == "$detail" ]]
  fi
  ok=$?
  printf 'PROBE %s text: exit=%s stdout-sha256=%s stderr-bytes=%s final=%s\n' "$name" "$rc" \
    "$(sha256sum <"$out" | cut -d' ' -f1)" "$(wc -c <"$tmp/$name.err")" "$last"
  printf 'PROBE %s json: exit=%s stdout-sha256=%s verdict=%s exitCode=%s failClosed.kind=%s\n' "$name" "$jrc" \
    "$(sha256sum <"$jout" | cut -d' ' -f1)" "$jverdict" "$jexit" "$jkind"
  if [[ "${SHOW:-0}" == 1 ]]; then
    while IFS= read -r l; do printf '  text | %s\n' "$l"; done <"$out"
    while IFS= read -r l; do printf '  json | %s\n' "$l"; done <"$jout"
  fi
  if [[ $ok -eq 0 ]]; then
    passed=$((passed + 1))
    printf 'PROBE %s: PASS (pristine expectation %s)\n' "$name" "$want"
  else
    printf 'PROBE %s: FAIL (pristine expectation %s)\n' "$name" "$want"
  fi
done <<<"$table"

if [[ $total -eq 4 && $passed -eq 4 ]]; then
  printf 'PROBE_VERDICT: PASS (%s/%s witnesses keep the pristine outputs)\n' "$passed" "$total"
  exit 0
fi
printf 'PROBE_VERDICT: FAIL (%s/%s witnesses keep the pristine outputs)\n' "$passed" "$total"
exit 1
