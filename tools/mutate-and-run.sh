#!/usr/bin/env bash
# mutate-and-run.sh — generic mutation runner (tameshi-shokunin, round 3, TAMESHI-R3-2).
#
# Plan anchor: plans/round-3.plan.md:6-7 — "the method ships as tameshi's own
# runnable tool (tools/mutate-and-run.sh: inject->run->restore with byte-identity
# proof)". Method provenance: corpus/knowledge/mutation-case-kimi-census.md
# §0-§1 — every mutant is a fresh copy of a pinned pristine; one exact edit per
# copy with a uniqueness assert; a green control run; killed/survived recorded
# per defect; sha256 before/after as the restore proof; a kill-rate headline.
#
# Inputs: a target file, a defect spec file, and a suite command. For each
# defect: if this one exact edit were present in the target, would the suite go
# red? Per-defect verdicts: KILLED (suite exit != 0) | SURVIVED (suite exit 0) |
# INCONCLUSIVE (timeout 124, or 126/127 = suite not runnable). The target is
# never written: every mutant is a fresh byte copy of the pinned pristine copy,
# and the target's sha256 before/after is the restore proof.
#
# Defect spec format v1 (one directive per line; '#' comments and blank lines
# ignored; LF endings only):
#
#   @defect <id> | <description>     id: [A-Za-z0-9._-]+; description optional
#   @old <text>                      exact string to find (required)
#   @new <text>                      exact replacement (may be empty to delete)
#
#   Escapes inside <text>: \n newline, \t tab, \r CR, \\ backslash. Any other
#   backslash sequence is refused (fail-closed against spec mistakes). Exactly
#   one separator space follows the directive; write a literal leading space in
#   the text as a second space (i.e. `@old ` + the text, spaces preserved).
#   The old string must occur exactly once (asserted before any suite run);
#   @new == @old (a no-op edit) is refused.
#
# Suite command contract: --suite CMD is run as `bash -c CMD` with stdin
# </dev/null, once per run, from the caller's CWD, with these exported:
#   MUTANT    absolute path of the artifact under test (the pristine copy for
#             the control run)          TARGET   absolute path of the original
#   PRISTINE  pinned pristine copy      WORKDIR  evidence/work directory
#   DEFECT_ID  defect id (CONTROL for the control run)
# Exit-code semantics: 0 = suite green; any non-zero = red, except
# 124 (timeout) / 126 / 127 (suite not runnable) = INCONCLUSIVE.
# Example: --suite 'node "$MUTANT" --selftest'
#
# Order of operations (fail-closed): (1) copy the target to a pinned pristine
# and pin both hashes; (2) parse the spec; (3) build every mutant and assert
# count==1 — any failure exits 2 before a single suite run; (4) control run on
# the pristine — a red control exits 2 (kills could not be attributed); (5)
# mutant runs with output tails; (6) re-check target+pristine sha256; (7)
# kill-rate report. A low kill count is a finding for the report, not a failure
# of this tool (bands are a report convention, not a gate — SKILL.md:127-133).
#
# Verdict lines (the last non-empty line is the verdict):
#   MUTATE_TOOL / MUTATE_DATE / MUTATE_TARGET / MUTATE_SPEC   — provenance
#   CONTROL: GREEN|RED (exit=… duration-ms=… pristine-sha256=…)
#   DEFECT <id>: KILLED|SURVIVED|INCONCLUSIVE (exit=… duration-ms=…)
#   MUTATE_RESTORE: OK|DRIFT (target-sha256 before=… after=… …)
#   MUTATE: DONE|DEGRADED (target=… defects=… killed=… survived=… inconclusive=… kill-rate=…%)
#   MUTATE: SETUP (<reason>)   — refused before/instead of a sweep
#
# Exit map: 0 done · 1 done-with-inconclusive (DEGRADED) · 2 setup/refusal ·
# 64 usage error.
#
# Evidence: workdir keeps pristine copy, mutant files, evidence/<id>.out full
# logs, evidence/control.out, defects.tsv (id/line/desc), results.tsv (per
# defect: verdict/exit/duration/mutant-sha256/desc), spec.copy; the path is
# printed as MUTATE_EVIDENCE. Default: mktemp -d /tmp/tameshi-r3-2-run.XXXXXX.
#
# --selftest is hermetic: it builds a tiny fixture target + mini-suite + four
# specs under /tmp/tameshi-r3-2-selftest.XXXXXX and self-checks control-green,
# one kill, one survivor, exact kill-rate line, restore proof, DEGRADED path,
# and refusal paths (duplicate old string, unknown escape, no-op edit, missing
# --target, usage). Scratch is removed on PASS, kept on FAIL for inspection.
#
# Dependencies: bash, python3 (byte-exact edit + spec parse), coreutils
# (sha256sum, mktemp, timeout, cp, date).

set -u -o pipefail

VERSION='mutate-and-run.sh r3-2 (tameshi-shokunin, 2026-10-14)'
SELF=$(readlink -f "${BASH_SOURCE[0]}")

MODE=run
TARGET=''
SPEC=''
SUITE=''
WORKDIR=''
LABEL=''
TIMEOUT_S=300
TAIL_N=8

usage() {
  cat <<'EOF'
mutate-and-run.sh — generic mutation runner (tameshi-shokunin)

Usage:
  mutate-and-run.sh --target FILE --defects SPEC --suite CMD [options]
  mutate-and-run.sh --selftest
  mutate-and-run.sh --help

Inputs:
  --target FILE    artifact to mutate (never written; sha256 pinned before/after)
  --defects SPEC   defect spec file (format below)
  --suite CMD      suite command, run as `bash -c CMD` with $MUTANT set to the
                   artifact under test (the pristine copy for the control run)

Options:
  --workdir DIR    evidence/work dir (default: mktemp -d /tmp/tameshi-r3-2-run.XXXXXX)
  --label NAME     name for the report (default: basename of the target)
  --timeout N      seconds per suite run (default: 300)
  --tail N         output tail lines shown per run (default: 8)

Spec format v1 (one directive per line; '#' comments; blank lines ignored):
  @defect <id> | <description>
  @old <text>          exact string to find (count==1 asserted before any run)
  @new <text>          exact replacement (may be empty)
  escapes: \n \t \r \\; any other backslash sequence is refused.

Verdicts per defect: KILLED | SURVIVED | INCONCLUSIVE. Exit map: 0 done ·
1 done-with-inconclusive · 2 setup/refusal · 64 usage. See the file header for
the full contract, evidence layout, and suite-command semantics.
EOF
}

usage_exit() {
  printf 'mutate-and-run: %s\n' "$1" >&2
  usage >&2
  exit 64
}

die_setup() {
  printf 'MUTATE: SETUP (%s)\n' "$1" >&2
  exit 2
}

need_val() {
  if [[ $# -lt 2 || -z "${2-}" ]]; then
    usage_exit "$1 needs a value"
  fi
}

sha_of() {
  local h
  h=$(sha256sum -- "$1" | cut -d' ' -f1) || die_setup "sha256sum failed for $1"
  printf '%s' "$h"
}

print_tail() {
  local f=$1 n
  n=$(wc -l < "$f")
  if [[ "$n" -eq 0 ]]; then
    printf '  | (no output)\n'
    return 0
  fi
  while IFS= read -r l; do printf '  | %s\n' "$l"; done < <(tail -n "$TAIL_N" "$f")
}

# ---------------------------------------------------------------- spec helper

py_helper() {
  python3 - "$@" <<'PYEOF'
"""Spec helper for mutate-and-run.sh: `list <spec>` | `apply <spec> <pristine>
<mutant> <id>`. Byte-exact single replace; count==1 asserted; refuses no-ops."""
import sys

ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}


def die(msg):
    sys.stderr.write('spec: %s\n' % msg)
    sys.exit(2)


def unescape(s, where):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            if i + 1 >= len(s):
                die('%s: trailing backslash' % where)
            n = s[i + 1]
            if n not in ESCAPES:
                die("%s: unknown escape '\\%s' (supported: \\n \\t \\r \\\\)" % (where, n))
            out.append(ESCAPES[n])
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def parse(path):
    try:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as e:
        die('cannot read spec file %s: %s' % (path, e))
    if '\r' in text:
        die('CR characters in spec (CRLF line endings are not supported)')
    defects = []
    cur = None

    def finish():
        nonlocal cur
        if cur is not None and ('old' not in cur or 'new' not in cur):
            die('line %d: defect %s incomplete (needs both @old and @new)' % (cur['line'], cur['id']))
        cur = None

    for no, line in enumerate(text.split('\n'), 1):
        if line.strip() == '':
            continue
        if line.lstrip().startswith('#'):
            continue
        if line == '@defect' or line.startswith('@defect '):
            finish()
            rest = line[len('@defect'):].lstrip(' ')
            idpart, sep, desc = rest.partition('|')
            idpart, desc = idpart.strip(), desc.strip()
            if not idpart or any(ch not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-' for ch in idpart):
                die('line %d: bad or missing defect id: %r' % (no, idpart))
            if any(d['id'] == idpart for d in defects):
                die('line %d: duplicate defect id %s' % (no, idpart))
            if '\t' in desc:
                die('line %d: description must not contain a tab' % no)
            cur = {'id': idpart, 'desc': desc, 'line': no}
            defects.append(cur)
        elif line == '@old' or line.startswith('@old '):
            if cur is None:
                die('line %d: @old outside a defect' % no)
            if 'old' in cur:
                die('line %d: duplicate @old for defect %s' % (no, cur['id']))
            cur['old'] = unescape('' if line == '@old' else line[len('@old '):], 'line %d' % no)
        elif line == '@new' or line.startswith('@new '):
            if cur is None:
                die('line %d: @new outside a defect' % no)
            if 'new' in cur:
                die('line %d: duplicate @new for defect %s' % (no, cur['id']))
            cur['new'] = unescape('' if line == '@new' else line[len('@new '):], 'line %d' % no)
        else:
            die('line %d: unrecognized line: %r' % (no, line[:80]))
    finish()
    if not defects:
        die('spec contains no defects')
    for d in defects:
        if d['old'] == '':
            die('defect %s: @old text is empty' % d['id'])
        if d['old'] == d['new']:
            die('defect %s: @new equals @old (no-op mutation)' % d['id'])
    return defects


def cmd_list(path):
    for d in parse(path):
        sys.stdout.write('%s\t%d\t%s\n' % (d['id'], d['line'], d['desc']))


def cmd_apply(path, pristine, mutant, did):
    hits = [d for d in parse(path) if d['id'] == did]
    if not hits:
        die('defect %s not found in spec' % did)
    d = hits[0]
    try:
        data = open(pristine, 'rb').read()
    except OSError as e:
        die('cannot read pristine %s: %s' % (pristine, e))
    old = d['old'].encode('utf-8')
    new = d['new'].encode('utf-8')
    count = data.count(old)
    if count != 1:
        sys.stderr.write('APPLY FAIL id=%s line=%d old-string-count=%d expected=1\n' % (did, d['line'], count))
        sys.exit(2)
    result = data.replace(old, new, 1)
    try:
        with open(mutant, 'wb') as fh:
            fh.write(result)
    except OSError as e:
        die('cannot write mutant %s: %s' % (mutant, e))
    sys.stdout.write('APPLY OK id=%s old-count=1 bytes-before=%d bytes-after=%d\n' % (did, len(data), len(result)))


if len(sys.argv) < 2 or sys.argv[1] not in ('list', 'apply'):
    sys.stderr.write('helper: usage: list <spec> | apply <spec> <pristine> <mutant> <id>\n')
    sys.exit(2)
if sys.argv[1] == 'list':
    if len(sys.argv) != 3:
        die('helper: list needs <spec>')
    cmd_list(sys.argv[2])
else:
    if len(sys.argv) != 6:
        die('helper: apply needs <spec> <pristine> <mutant> <id>')
    cmd_apply(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
PYEOF
}

# ------------------------------------------------------------------- sweep

run_one() { # $1 = artifact under test, $2 = evidence file, $3 = defect id
  local start now
  start=$(date +%s%N)
  MUTANT="$1" TARGET="$TARGET_ABS" PRISTINE="$PRISTINE" WORKDIR="$WORKDIR" DEFECT_ID="$3" \
    timeout "$TIMEOUT_S" bash -c "$SUITE" </dev/null >"$2" 2>&1
  RC=$?
  now=$(date +%s%N)
  DUR_MS=$(( (now - start) / 1000000 ))
}

run_sweep() {
  command -v python3 >/dev/null 2>&1 || die_setup 'python3 missing'
  command -v sha256sum >/dev/null 2>&1 || die_setup 'sha256sum missing'
  command -v timeout >/dev/null 2>&1 || die_setup 'timeout missing'
  command -v mktemp >/dev/null 2>&1 || die_setup 'mktemp missing'

  [[ -n "$TARGET" ]] || usage_exit 'missing --target'
  [[ -n "$SPEC" ]] || usage_exit 'missing --defects'
  [[ -n "$SUITE" ]] || usage_exit 'missing --suite'
  [[ -f "$TARGET" ]] || die_setup "target is not a regular file: $TARGET"
  [[ -r "$TARGET" ]] || die_setup "target is not readable: $TARGET"
  [[ -f "$SPEC" ]] || die_setup "spec is not a regular file: $SPEC"
  [[ -r "$SPEC" ]] || die_setup "spec is not readable: $SPEC"
  (( TIMEOUT_S > 0 )) || usage_exit '--timeout must be a positive integer'
  (( TAIL_N > 0 )) || usage_exit '--tail must be a positive integer'

  TARGET_ABS=$(readlink -f "$TARGET")
  SPEC_ABS=$(readlink -f "$SPEC")

  if [[ -z "$WORKDIR" ]]; then
    WORKDIR=$(mktemp -d /tmp/tameshi-r3-2-run.XXXXXX) || die_setup 'mktemp -d failed'
  else
    mkdir -p "$WORKDIR" || die_setup "cannot create workdir: $WORKDIR"
  fi
  EVID="$WORKDIR/evidence"
  mkdir -p "$EVID" || die_setup "cannot create evidence dir: $EVID"
  [[ -n "$LABEL" ]] || LABEL=$(basename "$TARGET_ABS")

  TARGET_SHA0=$(sha_of "$TARGET_ABS")
  PRISTINE="$WORKDIR/pristine.$(basename "$TARGET_ABS")"
  cp -p "$TARGET_ABS" "$PRISTINE" || die_setup "cannot copy target to pristine: $PRISTINE"
  PRISTINE_SHA=$(sha_of "$PRISTINE")
  PRISTINE_BYTES=$(wc -c < "$PRISTINE")
  [[ "$TARGET_SHA0" == "$PRISTINE_SHA" ]] || die_setup 'read race: target changed while copying'

  printf 'MUTATE_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"
  printf 'MUTATE_DATE: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'MUTATE_TARGET: %s sha256=%s bytes=%s\n' "$TARGET_ABS" "$TARGET_SHA0" "$PRISTINE_BYTES"

  local out
  if ! out=$(py_helper list "$SPEC_ABS" 2>&1); then
    printf '%s\n' "$out"
    die_setup 'spec parse failed'
  fi
  local total
  total=$(printf '%s\n' "$out" | wc -l)
  printf 'MUTATE_SPEC: %s defects=%s\n' "$SPEC_ABS" "$total"
  printf '%s\n' "$out" > "$WORKDIR/defects.tsv"
  [[ "$SPEC_ABS" == "$WORKDIR/spec.copy" ]] || cp -p "$SPEC_ABS" "$WORKDIR/spec.copy"

  local id line desc mutant aout fail=0
  while IFS=$'\t' read -r id line desc; do
    [[ -n "$id" ]] || continue
    mutant="$WORKDIR/mutant-$id.$(basename "$TARGET_ABS")"
    cp -p "$PRISTINE" "$mutant" || die_setup "cannot create mutant copy: $mutant"
    if ! aout=$(py_helper apply "$SPEC_ABS" "$PRISTINE" "$mutant" "$id" 2>&1); then
      printf '%s\n' "$aout"
      fail=$((fail + 1))
    fi
  done <<<"$out"
  if [[ "$fail" -gt 0 ]]; then
    die_setup "spec/preparation failed for $fail defect(s); no suite run"
  fi

  local ctl_rc ctl_ms
  run_one "$PRISTINE" "$EVID/control.out" CONTROL
  ctl_rc=$RC
  ctl_ms=$DUR_MS
  if [[ "$ctl_rc" -ne 0 ]]; then
    printf 'CONTROL: RED (exit=%s duration-ms=%s pristine-sha256=%s)\n' "$ctl_rc" "$ctl_ms" "$PRISTINE_SHA"
    print_tail "$EVID/control.out"
    die_setup "control run on the pristine copy is red (exit=$ctl_rc); cannot attribute kills; log: $EVID/control.out"
  fi
  printf 'CONTROL: GREEN (exit=0 duration-ms=%s pristine-sha256=%s)\n' "$ctl_ms" "$PRISTINE_SHA"
  print_tail "$EVID/control.out"

  local killed=0 survived=0 inconcl=0 v note
  printf 'id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc\n' > "$WORKDIR/results.tsv"
  while IFS=$'\t' read -r id line desc; do
    [[ -n "$id" ]] || continue
    mutant="$WORKDIR/mutant-$id.$(basename "$TARGET_ABS")"
    run_one "$mutant" "$EVID/$id.out" "$id"
    note=''
    case $RC in
      0) v=SURVIVED; survived=$((survived + 1)) ;;
      124) v=INCONCLUSIVE; inconcl=$((inconcl + 1)); note=' note=timeout' ;;
      126) v=INCONCLUSIVE; inconcl=$((inconcl + 1)); note=' note=suite-not-executable' ;;
      127) v=INCONCLUSIVE; inconcl=$((inconcl + 1)); note=' note=suite-not-found' ;;
      *) v=KILLED; killed=$((killed + 1)) ;;
    esac
    printf 'DEFECT %s: %s (exit=%s%s duration-ms=%s) %s\n' "$id" "$v" "$RC" "$note" "$DUR_MS" "$desc"
    print_tail "$EVID/$id.out"
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$id" "$v" "$RC" "$DUR_MS" "$(sha_of "$mutant")" "$desc" >> "$WORKDIR/results.tsv"
  done <<<"$out"

  local target_sha1 pristine_sha1
  target_sha1=$(sha_of "$TARGET_ABS")
  pristine_sha1=$(sha_of "$PRISTINE")
  if [[ "$TARGET_SHA0" != "$target_sha1" || "$PRISTINE_SHA" != "$pristine_sha1" ]]; then
    printf 'MUTATE_RESTORE: DRIFT (target-sha256 before=%s after=%s pristine-sha256-before=%s after=%s)\n' \
      "$TARGET_SHA0" "$target_sha1" "$PRISTINE_SHA" "$pristine_sha1"
    die_setup 'byte-identity proof failed: target or pristine changed during the sweep'
  fi
  printf 'MUTATE_RESTORE: OK (target-sha256 before=%s after=%s pristine-sha256=%s)\n' \
    "$TARGET_SHA0" "$target_sha1" "$pristine_sha1"
  printf 'MUTATE_EVIDENCE: %s\n' "$WORKDIR"

  local pct
  pct=$(( (200 * killed + total) / (2 * total) ))
  if [[ "$inconcl" -gt 0 ]]; then
    printf 'MUTATE: DEGRADED (target=%s defects=%s killed=%s survived=%s inconclusive=%s kill-rate=%s%%)\n' \
      "$LABEL" "$total" "$killed" "$survived" "$inconcl" "$pct"
    exit 1
  fi
  printf 'MUTATE: DONE (target=%s defects=%s killed=%s survived=%s inconclusive=%s kill-rate=%s%%)\n' \
    "$LABEL" "$total" "$killed" "$survived" "$inconcl" "$pct"
  exit 0
}

# ------------------------------------------------------------------ selftest

selftest() {
  local root
  root=$(mktemp -d /tmp/tameshi-r3-2-selftest.XXXXXX) || {
    printf 'MUTATE_SELFTEST: 0/1 pass\nVERDICT: FAIL (mktemp)\n'
    exit 1
  }
  local cases=0 failed=0
  st() { # st <name> <rc>
    cases=$((cases + 1))
    if [[ "$2" -eq 0 ]]; then
      printf 'PASS %s\n' "$1"
    else
      printf 'FAIL %s\n' "$1"
      failed=$((failed + 1))
    fi
  }

  local fx="$root/fixture"
  mkdir -p "$fx"

  cat >"$fx/target.sh" <<'EOT'
#!/usr/bin/env bash
# tiny fixture target — mutate-and-run.sh --selftest (never a live path)
banner() { printf 'fixture-target v1\n'; }
say_hello() { printf 'hello %s\n' "$1"; }
add() { printf '%s\n' "$(( $1 + $2 ))"; }
case "${1:-banner}" in
  banner) banner ;;
  hello) say_hello "${2:-world}" ;;
  add) add "${2:-0}" "${3:-0}" ;;
  *) banner ;;
esac
EOT
  chmod +x "$fx/target.sh"

  cat >"$fx/suite.sh" <<'EOT'
#!/usr/bin/env bash
# tiny mini-suite for the fixture target; $1 = path under test
set -u
t=${1:?suite: target path required}
cases=0; fails=0
chk() { cases=$((cases+1)); if [[ "$2" != "$3" ]]; then fails=$((fails+1)); printf 'FIXTURE FAIL %s: expected %q got %q\n' "$1" "$2" "$3"; fi; }
chk 'add(2,2)' 4 "$(bash "$t" add 2 2)"
chk 'add(1,4)' 5 "$(bash "$t" add 1 4)"
chk 'hello world' 'hello world' "$(bash "$t" hello world)"
chk 'hello kimi' 'hello kimi' "$(bash "$t" hello kimi)"
if [[ $fails -eq 0 ]]; then
  printf 'FIXTURE_SELFTEST: %s/%s pass\nVERDICT: PASS\n' "$cases" "$cases"; exit 0
fi
printf 'FIXTURE_SELFTEST: %s/%s pass\nVERDICT: FAIL\n' "$((cases-fails))" "$cases"; exit 1
EOT
  chmod +x "$fx/suite.sh"

  # hangs only when the add() operator mutant is present (its grep misses the
  # pristine); used to exercise the timeout -> INCONCLUSIVE -> DEGRADED path.
  cat >"$fx/suite-hang.sh" <<'EOT'
#!/usr/bin/env bash
if grep -qF -- '- $2' "$MUTANT"; then sleep 30; fi
exit 0
EOT
  chmod +x "$fx/suite-hang.sh"

  cat >"$fx/spec-ok.spec" <<'EOT'
# selftest spec — one mutant the mini-suite must catch, one it must not see
@defect K | mini-suite catches: add() operator + flipped to -
@old $(( $1 + $2 ))
@new $(( $1 - $2 ))
@defect S | survives: banner version string is reported, never asserted
@old fixture-target v1
@new fixture-target v2
EOT

  cat >"$fx/spec-dup.spec" <<'EOT'
# selftest spec — old string occurs twice: refuse before any suite run
@defect B | duplicate old string must refuse
@old say_hello
@new say_hello2
EOT

  cat >"$fx/spec-escape.spec" <<'EOT'
# selftest spec — unknown escape must refuse
@defect X | bad escape
@old \q
@new z
EOT

  cat >"$fx/spec-noop.spec" <<'EOT'
# selftest spec — new equals old must refuse
@defect N | no-op edit
@old add
@new add
EOT

  local s_before s_after rc1 rc2 rc3 rc4 rc5
  s_before=$(sha_of "$fx/target.sh")

  local suite_good suite_hang
  suite_good="bash '$fx/suite.sh' \"\$MUTANT\""
  suite_hang="bash '$fx/suite-hang.sh' \"\$MUTANT\""
  local out1="$root/run1.out" out2="$root/run2.out" out3="$root/run3.out" out4="$root/run4.out" out5="$root/run5.out"

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-ok.spec" \
    --suite "$suite_good" --workdir "$root/run1" --label fixture --tail 5 --timeout 30 >"$out1" 2>&1
  rc1=$?
  s_after=$(sha_of "$fx/target.sh")

  [[ $rc1 -eq 0 ]]; st 'sweep exits 0' $?
  grep -q '^CONTROL: GREEN (exit=0' "$out1"; st 'control green on pristine' $?
  grep -q '^DEFECT K: KILLED (exit=1' "$out1"; st 'kill classified (K)' $?
  grep -q '^DEFECT S: SURVIVED (exit=0' "$out1"; st 'survivor classified (S)' $?
  grep -q 'FIXTURE FAIL add(2,2)' "$out1"; st 'kill tail shows the failing case' $?
  grep -qxF 'MUTATE: DONE (target=fixture defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)' "$out1"; st 'kill-rate summary exact' $?
  grep -q '^MUTATE_RESTORE: OK ' "$out1"; st 'restore line OK' $?
  [[ "$s_before" == "$s_after" ]]; st 'fixture target byte-identical after sweep' $?
  [[ $(wc -l < "$root/run1/results.tsv") -eq 3 ]]; st 'results.tsv = header + one row per defect' $?

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-dup.spec" \
    --suite "$suite_good" --workdir "$root/run2" --timeout 30 >"$out2" 2>&1
  rc2=$?
  local exp_dup
  exp_dup=$(grep -cF 'say_hello' "$fx/target.sh")
  [[ $rc2 -eq 2 ]]; st 'duplicate old string refuses (exit 2)' $?
  grep -q 'APPLY FAIL id=B ' "$out2"; st 'refusal names the defect' $?
  grep -q "old-string-count=$exp_dup expected=1" "$out2"; st 'refusal reports the old-string count' $?
  grep -q '^MUTATE: SETUP ' "$out2"; st 'refusal is a SETUP verdict' $?
  if grep -q '^CONTROL:' "$out2" || grep -q '^DEFECT B:' "$out2"; then
    st 'no suite run before refusal' 1
  else
    st 'no suite run before refusal' 0
  fi

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-escape.spec" \
    --suite "$suite_good" --workdir "$root/run3" --timeout 30 >"$out3" 2>&1
  rc3=$?
  [[ $rc3 -eq 2 ]]; st 'unknown escape refuses (exit 2)' $?
  grep -q 'unknown escape' "$out3"; st 'unknown escape named' $?

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-noop.spec" \
    --suite "$suite_good" --workdir "$root/run4" --timeout 30 >"$out4" 2>&1
  rc4=$?
  [[ $rc4 -eq 2 ]]; st 'no-op edit refuses (exit 2)' $?
  grep -q 'no-op mutation' "$out4"; st 'no-op edit named' $?

  bash "$SELF" --target "$fx/target.sh" --defects "$fx/spec-ok.spec" \
    --suite "$suite_hang" --workdir "$root/run5" --label fixture --timeout 2 >"$out5" 2>&1
  rc5=$?
  [[ $rc5 -eq 1 ]]; st 'inconclusive run exits 1' $?
  grep -q '^DEFECT K: INCONCLUSIVE (exit=124 note=timeout' "$out5"; st 'timeout classified inconclusive' $?
  grep -q '^DEFECT S: SURVIVED (exit=0' "$out5"; st 'survivor still recorded under DEGRADED' $?
  grep -qxF 'MUTATE: DEGRADED (target=fixture defects=2 killed=0 survived=1 inconclusive=1 kill-rate=0%)' "$out5"; st 'degraded summary exact' $?

  bash "$SELF" --help >/dev/null 2>&1; [[ $? -eq 0 ]]; st 'help exits 0' $?
  bash "$SELF" --defects "$fx/spec-ok.spec" --suite true >/dev/null 2>&1; [[ $? -eq 64 ]]; st 'missing --target exits 64' $?

  printf 'MUTATE_SELFTEST: %s/%s pass\n' "$((cases - failed))" "$cases"
  if [[ "$failed" -eq 0 ]]; then
    printf 'VERDICT: PASS\n'
    rm -rf "$root"
    exit 0
  fi
  printf 'VERDICT: FAIL (scratch kept: %s)\n' "$root"
  exit 1
}

# -------------------------------------------------------------------- main

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) need_val "$@"; TARGET=$2; shift 2 ;;
    --defects) need_val "$@"; SPEC=$2; shift 2 ;;
    --suite) need_val "$@"; SUITE=$2; shift 2 ;;
    --workdir) need_val "$@"; WORKDIR=$2; shift 2 ;;
    --label) need_val "$@"; LABEL=$2; shift 2 ;;
    --timeout) need_val "$@"; TIMEOUT_S=$2; shift 2 ;;
    --tail) need_val "$@"; TAIL_N=$2; shift 2 ;;
    --selftest) MODE=selftest; shift ;;
    --help | -h) MODE=help; shift ;;
    *) usage_exit "unknown argument: $1" ;;
  esac
done

case "$MODE" in
  help) usage; exit 0 ;;
  selftest) selftest ;;
  run) run_sweep ;;
esac
