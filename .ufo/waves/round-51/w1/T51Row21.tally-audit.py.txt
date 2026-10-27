#!/usr/bin/env python3
"""tally-audit.py — audit the mutation runner's --regression tally without editing the runner.

Usage:
  python3 tools/tally-audit.py [--runner PATH]            audit (default: tools/mutate-and-run.sh beside this file)
  python3 tools/tally-audit.py --runner PATH --then-regression [--workdir DIR]
                                                         audit, and only on PASS run `bash PATH --regression`, then
                                                         check its REGRESSION line names cases=<legs found>
  python3 tools/tally-audit.py --selftest                show every check able to fail on seeded faults

Round 32 (tameshi). The runner `tools/mutate-and-run.sh` is an input of most credited cold-read
sections, so its fixes live here, in a new versioned tool, and the runner stays byte-identical.
Three checks, each independent of the others:

  static   per-leg presence: the `st_*=$?` leg statuses assigned in run_regression() and the
           operands of the tally loop `for st in ...; do` are equal as multisets (each leg counted
           exactly once) and `local nlegs=N` equals the leg count. A sum-preserving miscount
           (one operand duplicated, another dropped) passes the runner's own run-time guard; it
           fails here.
  runtime  the runner's tally block, run in bash, against an independent oracle: every exit
           status 0..255 at the first leg (bash exit statuses are 0..255; S097), statuses
           1 2 3 4 126 127 255 at every leg, multi-status vectors, and stress with one operand
           duplicated (overcount) or removed (undercount) at every position. Exact first line
           and exit code are both compared.
  harness  the runner's own tally selftest harness (`  local tblock ` .. `  tblock=$tblock_full`)
           run against a panel of known-faulty tally blocks built from the pinned reference block:
           it must accept the reference block and reject every fault. A weakened harness (exit
           only, swallowed status, a skipped position or vector, a skipped guard stress) accepts
           at least one fault.

Prints one `CHECK <name> PASS|FAIL ...` line per check and a final
`TALLY_AUDIT: PASS|FAIL (static=.. runtime=.. harness=..)`. Exit 0 PASS, 1 FAIL, 2 cannot audit.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 120
START = '  local nlegs='

# Reference tally block of the runner at sha256 a7d3f2dd…2eb9 (round 30, lines 1432-1472). Faults for
# the harness panel are built from this text, never from the audited file.
REF_BLOCK = r'''  local nlegs=9 npass=0 nfail=0 nsetup=0 st
  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
  done

  if [[ $nfail -gt 0 ]]; then
    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
      "$nlegs" "$npass" "$nfail" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 1
  fi
  if [[ $nsetup -gt 0 ]]; then
    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
      "$nlegs" "$npass" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the
  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals
  # of a mutation report are sums of its per-state counts).
  if (( npass + nfail + nsetup != nlegs )); then
    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
      "$nlegs" "$((npass + nfail + nsetup))"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
    "$nlegs" "$npass"
  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
    rm -rf "$root"
  else
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
  fi
  exit 0
'''
REF_NAMES = ['st_js', 'st_kagi', 'st_tsu', 'st_mado', 'st_checklist', 'st_claims', 'st_roundgate',
             'st_sourcescheck', 'st_citecheck']


class CannotAudit(Exception):
    pass


# ---------------------------------------------------------------- parsing

def regression_body(text):
    m = re.search(r'^run_regression\s*\(\)\s*\{[ \t]*\n', text, re.M)
    if not m:
        raise CannotAudit('run_regression() not found')
    b = text.find('\n}\n', m.end() - 1)
    if b < 0:
        raise CannotAudit('run_regression() has no closing brace')
    return text[m.start():b + 3]


START_RE = re.compile(r'^[ \t]*local nlegs=', re.M)


def tally_block(body):
    m = START_RE.search(body)
    if not m:
        raise CannotAudit('tally start `local nlegs=` not found')
    return body[m.start():body.rindex('\n}\n') + 1]


def leg_names(body):
    m = START_RE.search(body)
    head = body[:m.start()] if m else body
    return re.findall(r'^[ \t]+(st_[A-Za-z0-9_]+)=\$\?[ \t]*$', head, re.M)


# `for VAR in OPERANDS; do` or `... \n do`, OPERANDS possibly continued with backslash-newline.
LOOP_RE = re.compile(r'^([ \t]*for[ \t]+([A-Za-z_][A-Za-z0-9_]*)[ \t]+in[ \t]+)((?:[^;\n\\]|\\\n)*?)([ \t]*(?:;[ \t]*|\n[ \t]*)do\b)', re.M)
OPERAND_RE = re.compile(r'"?\$\{?(st_[A-Za-z0-9_]+)\}?"?')


def tally_loop(block):
    """The first `for` loop of the tally block whose operands are all leg statuses."""
    for m in LOOP_RE.finditer(block):
        toks = m.group(3).replace('\\\n', ' ').split()
        ops = []
        for t in toks:
            mm = OPERAND_RE.fullmatch(t)
            if not mm:
                break
            ops.append(mm.group(1))
        else:
            if ops:
                return m, ops
    raise CannotAudit('tally loop `for VAR in "$st_..." ...; do` not found')


def loop_operands(block):
    return tally_loop(block)[1]


def with_operands(block, ops):
    m = tally_loop(block)[0]
    return block[:m.start(3)] + ' '.join('"$%s"' % o for o in ops) + block[m.end(3):]


# ---------------------------------------------------------------- bash runs

def bash(script, tmp):
    path = os.path.join(tmp, 'p%d.sh' % len(os.listdir(tmp)))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(script)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp}
    try:
        p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        raise CannotAudit('bash run timed out after %ds' % TIMEOUT)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def run_vectors(block, names, vectors, tmp):
    """Run the tally block once per status vector in one bash process; return [(rc, first line)]."""
    decl = ' '.join('%s=${%d}' % (n, i + 1) for i, n in enumerate(names))
    lines = ['set -u -o pipefail', 'tally() {', '  local ' + decl,
             '  local root=tally-audit auto=0 KEEP=1', block.rstrip('\n'), '}']
    for v in vectors:
        lines.append('out=$(tally %s 2>&1); rc=$?; printf "R\\t%%s\\t%%s\\n" "$rc" "${out%%%%$\'\\n\'*}"'
                     % ' '.join(str(s) for s in v))
    rc, out, err = bash('\n'.join(lines) + '\n', tmp)
    got = [ln.split('\t', 2) for ln in out.splitlines() if ln.startswith('R\t')]
    if rc != 0 or len(got) != len(vectors):
        raise CannotAudit('tally driver failed (exit %s, %d/%d results): %s' % (rc, len(got), len(vectors), err[:200]))
    return [(int(g[1]), g[2] if len(g) > 2 else '') for g in got]


def oracle(statuses_by_leg, counted_ops, nlegs):
    """Expected (exit, first line) for one run: statuses keyed by leg, operands as the loop counts them."""
    vals = [statuses_by_leg[o] for o in counted_ops]
    p = sum(1 for s in vals if s == 0)
    f = sum(1 for s in vals if s == 1)
    s_ = len(vals) - p - f
    if f:
        return 1, 'REGRESSION: FAIL (cases=%d passed=%d failed=%d setup=%d)' % (nlegs, p, f, s_)
    if s_:
        return 2, 'REGRESSION: SETUP (cases=%d passed=%d cannot-verify=%d)' % (nlegs, p, s_)
    if p != nlegs:
        return 2, 'REGRESSION: SETUP (case-tally mismatch: cases=%d counted=%d)' % (nlegs, p)
    return 0, 'REGRESSION: PASS (cases=%d passed=%d; ledger legs exact: killed-delta<=0 flips<=0)' % (nlegs, p)


# ---------------------------------------------------------------- checks

def check_static(body, block):
    names = leg_names(body)
    ops = loop_operands(block)
    m = re.match(r'[ \t]*local nlegs=(\d+)\b', block)
    nlegs = int(m.group(1)) if m else None
    problems = []
    if not names:
        problems.append('no st_*=$? leg assignments')
    if sorted(ops) != sorted(names):
        missing = sorted(set(names) - set(ops))
        extra = sorted(o for o in set(ops) if ops.count(o) != names.count(o))
        problems.append('loop operands != legs (missing %s; miscounted %s)' % (missing or '-', extra or '-'))
    if nlegs != len(names):
        problems.append('nlegs=%s but %d legs assigned' % (nlegs, len(names)))
    return (not problems), 'legs=%d operands=%d nlegs=%s%s' % (len(names), len(ops), nlegs,
                                                                '; ' + '; '.join(problems) if problems else '')


def check_runtime(block, names, tmp):
    n = len(names)
    ops = loop_operands(block)
    vectors = [[0] * n]
    for s in range(1, 256):
        vectors.append([s] + [0] * (n - 1))
    for pos in range(n):
        for s in (1, 2, 3, 4, 126, 127, 255):
            v = [0] * n
            v[pos] = s
            vectors.append(v)
    for a, b in ((0, n - 1), (n // 2, n // 2 + 1)):
        for sa, sb in ((1, 1), (2, 2), (1, 2), (2, 1), (3, 4)):
            v = [0] * n
            v[a], v[b] = sa, sb
            vectors.append(v)
    vectors.append([1] * n)
    vectors.append([2] * n)
    got = run_vectors(block, names, vectors, tmp)
    bad = []
    for v, g in zip(vectors, got):
        exp = oracle(dict(zip(names, v)), ops, n)
        if g != exp:
            bad.append('statuses %s: got %s, want %s' % (' '.join(map(str, v)), g, exp))
    # stress: the loop with one operand duplicated (overcount) or removed (undercount), all legs passing
    stress = 0
    for i in range(len(ops)):
        for kind, new in (('dup', ops[:i + 1] + ops[i:]), ('drop', ops[:i] + ops[i + 1:])):
            sb = with_operands(block, new)
            g = run_vectors(sb, names, [[0] * n], tmp)[0]
            exp = oracle(dict(zip(names, [0] * n)), new, n)
            stress += 1
            if g != exp:
                bad.append('stress %s operand %d: got %s, want %s' % (kind, i, g, exp))
    total = len(vectors) + stress
    return (not bad), 'vectors=%d mismatched=%d%s' % (total, len(bad), ('; first: ' + bad[0]) if bad else '')


def faults():
    """Known-faulty tally blocks built from REF_BLOCK; each must be rejected by a sound harness."""
    b = REF_BLOCK
    out = []
    def f(name, new):
        if new == b:
            raise CannotAudit('fault %s did not change the reference block' % name)
        out.append((name, new))
    f('label', b.replace('passed=%s', 'passing=%s'))
    f('fail-exits-0', b.replace('    exit 1\n', '    exit 0\n', 1))
    f('drop-last-operand', b.replace(' "$st_citecheck"; do\n', '; do\n', 1))
    start = b.split('\n', 1)[0] + '\n'
    for nm in REF_NAMES:
        f('ignore-' + nm, b.replace(start, start + '  %s=0\n' % nm, 1))
    # Position-only faults: leg NM is ignored only when it is the single failing (1) or setup (2)
    # leg, so only the harness's one-leg-at-each-position loop can see it; the multi-status vectors
    # (two non-zero legs, or status 3) never trigger it. A harness that skips a position accepts it.
    for nm in REF_NAMES:
        others = ' + '.join('$%s' % o for o in REF_NAMES if o != nm)
        f('ignore-alone-' + nm, b.replace(start, start + '  if (( %s == 0 )) && [[ $%s == 1 || $%s == 2 ]]; then %s=0; fi\n'
                                          % (others, nm, nm, nm), 1))
    guard = ('  if (( npass + nfail + nsetup != nlegs )); then\n'
             "    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n"
             '      "$nlegs" "$((npass + nfail + nsetup))"\n'
             "    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n"
             '    exit 2\n  fi\n')
    if guard not in b:
        raise CannotAudit('reference guard not found')
    f('guard-removed', b.replace(guard, ''))
    f('guard-overcount-only', b.replace('!= nlegs', '> nlegs'))
    fail_if = b[b.index('  if [[ $nfail -gt 0 ]]'):b.index('  if [[ $nsetup -gt 0 ]]')]
    setup_if = b[b.index('  if [[ $nsetup -gt 0 ]]'):b.index('  if (( npass')]
    f('setup-before-fail', b.replace(fail_if + setup_if, setup_if + fail_if))
    f('fail-needs-exactly-one', b.replace('$nfail -gt 0', '$nfail -eq 1'))
    f('setup-needs-exactly-one', b.replace('$nsetup -gt 0', '$nsetup -eq 1'))
    f('status-3-passes', b.replace('      *) nsetup', '      3) npass=$((npass + 1)) ;;\n      *) nsetup', 1))
    return out


HARNESS_START = re.compile(r'^[ \t]*local tblock\b.*$', re.M)
HARNESS_END = re.compile(r'^[ \t]*tblock=\$tblock_full[ \t]*\n', re.M)
EXTRACT_RE = re.compile(r'^[ \t]*tblock=\$\(awk .*"\$SELF"\)[ \t]*\n', re.M)


def harness_section(text):
    m = HARNESS_START.search(text)
    if not m:
        raise CannotAudit('selftest tally harness (`local tblock`) not found')
    e = HARNESS_END.search(text, m.start())
    if not e:
        raise CannotAudit('selftest tally harness end (`tblock=$tblock_full`) not found')
    sec = text[m.start():e.end()]
    if len(EXTRACT_RE.findall(sec)) != 1:
        raise CannotAudit('harness block extraction line not found exactly once')
    return sec


def run_harness(runner_path, section, injected, tmp):
    sec = EXTRACT_RE.sub(lambda m: m.group(0) + '  tblock=$AUDIT_INJECT\n', section, count=1)
    script = ('set -u -o pipefail\nSELF=%s\n' % shquote(runner_path) +
              'audit_harness() {\n  local root cases=0 failed=0\n  root=$(mktemp -d "$TMPDIR/h.XXXXXX")\n'
              '  st() { cases=$((cases + 1)); if [[ $2 -ne 0 ]]; then failed=$((failed + 1)); fi; }\n' +
              sec + '  printf "HARNESS cases=%s failed=%s\\n" "$cases" "$failed"\n}\naudit_harness\n')
    path = os.path.join(tmp, 'h%d.sh' % len(os.listdir(tmp)))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(script)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp,
           'AUDIT_INJECT': injected.rstrip('\n')}
    try:
        p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        raise CannotAudit('harness run timed out')
    m = re.search(r'^HARNESS cases=(\d+) failed=(\d+)$', p.stdout.decode('utf-8', 'replace'), re.M)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def shquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def check_harness(runner_path, text, names, tmp):
    if names != REF_NAMES:
        return False, 'leg names differ from the reference panel (%s)' % ' '.join(names)
    sec = harness_section(text)
    good = run_harness(runner_path, sec, REF_BLOCK, tmp)
    if good is None or good[0] == 0 or good[1] != 0:
        return False, 'harness rejects or cannot run the reference block (%s)' % (good,)
    accepted = []
    panel = faults()
    for name, block in panel:
        r = run_harness(runner_path, sec, block, tmp)
        if r is None:
            continue  # harness aborted on the fault: counted as rejected
        if r[1] == 0:
            accepted.append(name)
    return (not accepted), 'reference cases=%d; faults rejected=%d/%d%s' % (
        good[0], len(panel) - len(accepted), len(panel), ('; accepted: ' + ' '.join(accepted)) if accepted else '')


def audit(runner_path):
    with open(runner_path, 'r', encoding='utf-8') as f:
        text = f.read()
    body = regression_body(text)
    block = tally_block(body)
    names = leg_names(body)
    tmp = tempfile.mkdtemp(prefix='tally-audit.')
    try:
        rtmp = os.path.join(tmp, 'r')
        os.mkdir(rtmp)
        results = [('static',) + check_static(body, block),
                   ('runtime',) + check_runtime(block, names, rtmp),
                   ('harness',) + check_harness(runner_path, text, names, tmp)]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, ok, detail in results:
        print('CHECK %s %s %s' % (name, 'PASS' if ok else 'FAIL', detail))
    verdict = all(ok for _, ok, _ in results)
    print('TALLY_AUDIT: %s (%s)' % ('PASS' if verdict else 'FAIL',
                                    ' '.join('%s=%s' % (n, 'pass' if ok else 'fail') for n, ok, _ in results)))
    return 0 if verdict else 1, len(names)


def then_regression(runner_path, nlegs, workdir):
    argv = ['bash', runner_path, '--regression']
    if workdir:
        argv += ['--workdir', workdir]
    p = subprocess.run(argv, capture_output=True)
    out = p.stdout.decode('utf-8', 'replace')
    sys.stdout.write(out)
    sys.stderr.write(p.stderr.decode('utf-8', 'replace'))
    m = re.search(r'^REGRESSION: (PASS|FAIL|SETUP) \(cases=(\d+)', out, re.M)
    if not m or int(m.group(2)) != nlegs:
        print('TALLY_AUDIT_REGRESSION: SETUP (REGRESSION line missing or cases != %d legs found)' % nlegs)
        return 2
    print('TALLY_AUDIT_REGRESSION: %s (cases=%s legs=%d exit=%d)' % (m.group(1), m.group(2), nlegs, p.returncode))
    return p.returncode


# ---------------------------------------------------------------- selftest

def selftest():
    runner = os.path.join(HERE, 'mutate-and-run.sh')
    with open(runner, encoding='utf-8') as f:
        text = f.read()
    loop = '  for st in ' + ' '.join('"$%s"' % n for n in REF_NAMES) + '; do\n'
    cmp_line = '    [[ $rc -eq $want_rc && "${out%%$\'\\n\'*}" == "$want_line" ]]\n'
    cases = [
        ('pristine', text, 0, None),
        ('dup-drop operand', text.replace(loop, loop.replace('"$st_citecheck"', '"$st_js"')), 1, 'static'),
        ('nlegs wrong', text.replace('  local nlegs=9 ', '  local nlegs=8 ', 1), 1, 'static'),
        ('status 4 passes', text.replace('      1) nfail=$((nfail + 1)) ;;\n',
                                         '      1) nfail=$((nfail + 1)) ;;\n      4) npass=$((npass + 1)) ;;\n', 1), 1, 'runtime'),
        ('guard undercount only', text.replace('npass + nfail + nsetup != nlegs', 'npass + nfail + nsetup < nlegs', 1), 1, 'runtime'),
        ('harness exit-only', text.replace(cmp_line, '    [[ $rc -eq $want_rc ]]\n', 1), 1, 'harness'),
        ('harness swallowed', text.replace(cmp_line, cmp_line + '    rc=$?\n', 1), 1, 'harness'),
        ('harness position 8 skipped', text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 0 1 2 3 4 5 6 7 7; do', 1), 1, 'harness'),
        ('harness position 0 skipped', text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 6 1 2 3 4 5 6 7 8; do', 1), 1, 'harness'),
        ('harness position 1 skipped', text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 0 3 2 3 4 5 6 7 8; do', 1), 1, 'harness'),
        ('reversed operands', text.replace(loop, '  for st in ' + ' '.join('"$%s"' % n for n in reversed(REF_NAMES)) + '; do\n'), 0, None),
    ]
    tmp = tempfile.mkdtemp(prefix='tally-audit-selftest.')
    passed = 0
    try:
        for i, (name, body, want, check) in enumerate(cases):
            if name != 'pristine' and body == text:
                print('CASE %s FAIL (edit did not apply)' % name)
                continue
            path = os.path.join(tmp, 'c%d.sh' % i)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(body)
            p = subprocess.run([sys.executable, os.path.abspath(__file__), '--runner', path], capture_output=True, timeout=600)
            out = p.stdout.decode()
            ok = p.returncode == want and (check is None or re.search(r'^CHECK %s FAIL' % check, out, re.M))
            passed += bool(ok)
            print('CASE %s %s (exit %d)' % (name, 'PASS' if ok else 'FAIL', p.returncode))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('TALLY_AUDIT_SELFTEST: %d/%d pass' % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', default=os.path.join(HERE, 'mutate-and-run.sh'))
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--then-regression', action='store_true')
    ap.add_argument('--workdir')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        rc, nlegs = audit(os.path.abspath(a.runner))
    except (CannotAudit, OSError, UnicodeDecodeError, ValueError) as e:
        print('TALLY_AUDIT: SETUP (%s)' % e)
        return 2
    if rc == 0 and a.then_regression:
        return then_regression(os.path.abspath(a.runner), nlegs, a.workdir)
    return rc


if __name__ == '__main__':
    sys.exit(main())
