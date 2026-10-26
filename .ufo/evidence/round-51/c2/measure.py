#!/usr/bin/env python3
"""Round-51 C2 (depth) counter: a tenth recorded mutation case, pre-registered, swept, wired, replayed and sourced.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C2_R51_PASS=true iff, at REV,
  * command D's ledger regex finds 10 recorded legs in tools/mutate-and-run.sh and all 10 are wired (round-26 rule:
    embedded spec heredoc, `regression_case_git <leg> \\` call, leg-check entry, TABLE line with the entry's defect
    and KILLED counts), depth_score = min(10, recorded, wired) = 10;
  * exactly one leg is new against the nine frozen base legs, its call targets a fleet path none of the nine
    targets, and its PIN/REV variables name a blob at that rev in the owner repo whose sha256 equals the PIN;
  * the new leg's embedded spec equals, byte for byte, .ufo/evidence/round-51/c2/<leg>.defects.spec, whose sha256
    equals the value frozen in this counter (SPEC_SHA);
  * the sweep receipt .ufo/evidence/round-51/c2/sweep/sweep.txt shows CONTROL: GREEN with pristine-sha256 = PIN,
    one DEFECT line per spec defect (KILLED or SURVIVED), MUTATE_RESTORE: OK, MUTATE: DONE, and a MUTATE_DATE later
    than the commit time of the commit that first added the spec (pre-registration before any mutant ran);
  * the new leg's TABLE equals the sweep's verdicts in spec order;
  * `bash tools/mutate-and-run.sh --regression` run from a --shared clone of the lane at REV (placed beside
    read-only symlinks to the owner repos) exits 0 and prints `REGRESSION: PASS (cases=10 passed=10`;
  * a knowledge entry added after base names the target path in its `source:` line together with an S-id whose
    corpus/SOURCES.md row at REV is status `mined`, opened 2026-10-26, with the entry in used-by; and
    corpus/README.md at REV, beyond its base bytes, names the entry.
  Verdict predictions (`# PREDICT KILLED|SURVIVED` before each @defect) are counted and printed, outside the predicate.
Usage: measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain] | --selftest
Exit: 0 PASS · 1 not PASS · 2 setup error · 64 usage.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

sys.dont_write_bytecode = True
BASE = '9962033fd7a75aa2f2847e979dd687a5d28505a1'
FLEET = '/home/vgpnk/Projects/shokunin'
SPEC_SHA = 'a98271f639bc520f7052e63efaaa0b560cda959d3122d9c6921dcd1b9b61a602'
SPEC_DIR = '.ufo/evidence/round-51/c2'
SWEEP = '.ufo/evidence/round-51/c2/sweep/sweep.txt'
BASE_LEGS = {
    'js-kimi-census': 'kumitate-shokunin/scripts/kimi-census.mjs',
    'bash-surface-census': 'kagi-shokunin/corpus/surface-census.sh',
    'bash-tsukuroi-census': 'tsukuroi-shokunin/tools/tsukuroi-census.sh',
    'bash-mado-verify': 'mado-shokunin/tools/mado-verify.sh',
    'bash-checklist-run': 'kagi-shokunin/corpus/checklist-run.sh',
    'js-claims-check': 'kumitate-shokunin/scripts/claims-check.mjs',
    'js-round-gate': 'kumitate-shokunin/scripts/round-gate.mjs',
    'js-sources-check': 'kumitate-shokunin/scripts/sources-check.mjs',
    'js-cite-check': 'kumitate-shokunin/scripts/cite-check.mjs',
}
LEDGER_RE = re.compile(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+", re.M)
LEG_RE = re.compile(r"^#   ((?:js|bash)-\S+)\s+\S+\s+\d+/\d+", re.M)
ROW_RE = re.compile(r'^ {0,3}\|\s*(S[0-9]{3,})\s*\|')


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return e


def git(repo, *args, check=True):
    r = subprocess.run(['git', '-C', repo, *args], capture_output=True, env=env())
    if check and r.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(args), r.stderr.decode(errors='replace').strip()))
    return r


def show(repo, rev, path):
    r = git(repo, 'show', '%s:%s' % (rev, path), check=False)
    return r.stdout if r.returncode == 0 else None


def wiring(text):
    recorded = len(LEDGER_RE.findall(text))
    legs = LEG_RE.findall(text)
    wired, info = [], {}
    for leg in legs:
        missing = []
        if ('cat >"$d/%s.spec"' % leg) not in text:
            missing.append('spec-heredoc')
        if not re.search(r"^\s*regression_case_git %s \\$" % re.escape(leg), text, re.M):
            missing.append('regression-call')
        m = re.search(r"'%s:%s\.spec:(TABLE_[A-Z0-9_]+):(\d+):(\d+)'" % (re.escape(leg), re.escape(leg)), text)
        table = None
        if not m:
            missing.append('leg-check-entry')
        else:
            var, n, k = m.group(1), int(m.group(2)), int(m.group(3))
            t = re.search(r"^%s='([^']*)'$" % var, text, re.M)
            if not t:
                missing.append('table-line')
            else:
                table = t.group(1)
                pairs = [p.split(':', 1) for p in table.split(',') if p]
                if len(pairs) != n or sum(1 for p in pairs if p[-1] == 'KILLED') != k:
                    missing.append('table-counts')
        info[leg] = {'missing': missing, 'table': table}
        if not missing:
            wired.append(leg)
    return recorded, legs, wired, info


def leg_call(text, leg):
    m = re.search(r"^\s*regression_case_git %s \\\n\s*'([^']+)' \"\$(PIN_[A-Z0-9_]+)\" \"\$(REV_[A-Z0-9_]+)\"" % re.escape(leg), text, re.M)
    if not m:
        return None
    rel, pv, rv = m.groups()
    pin = re.search(r'^%s=([0-9a-f]{64})$' % pv, text, re.M)
    rev = re.search(r'^%s=([0-9a-f]{40})$' % rv, text, re.M)
    return rel, (pin.group(1) if pin else None), (rev.group(1) if rev else None)


def heredoc(text, leg):
    m = re.search(r"^  cat >\"\$d/%s\.spec\" <<'EOT'\n(.*?)^EOT$" % re.escape(leg), text, re.M | re.S)
    return m.group(1).encode('utf-8', 'surrogateescape') if m else None


def spec_defects(spec):
    preds, ids, cur = {}, [], None
    for line in spec.decode('utf-8', 'surrogateescape').split('\n'):
        p = re.match(r'^# PREDICT (KILLED|SURVIVED)\b', line)
        if p:
            cur = p.group(1)
        d = re.match(r'^@defect ([A-Za-z0-9._-]+)', line)
        if d:
            ids.append(d.group(1))
            preds[d.group(1)] = cur
            cur = None
    return ids, preds


def sweep_check(sweep, ids, pin, freeze_ts, explain):
    text = sweep.decode('utf-8', 'surrogateescape')
    ok = True
    if not re.search(r'^CONTROL: GREEN \(exit=0 duration-ms=\d+ pristine-sha256=%s\)$' % pin, text, re.M):
        ok = False
        explain.append('SWEEP control-not-green-or-pin-mismatch')
    if not re.search(r'^MUTATE_RESTORE: OK ', text, re.M):
        ok = False
        explain.append('SWEEP restore-not-ok')
    if not re.search(r'^MUTATE: DONE ', text, re.M):
        ok = False
        explain.append('SWEEP not-done')
    verdicts = {}
    for m in re.finditer(r'^DEFECT ([A-Za-z0-9._-]+): (KILLED|SURVIVED|INCONCLUSIVE) ', text, re.M):
        verdicts.setdefault(m.group(1), []).append(m.group(2))
    if sorted(verdicts) != sorted(ids) or any(len(v) != 1 or v[0] == 'INCONCLUSIVE' for v in verdicts.values()):
        ok = False
        explain.append('SWEEP defect-lines-do-not-match-spec')
    dates = re.findall(r'^MUTATE_DATE: (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)$', text, re.M)
    after = 0
    if len(dates) == 1:
        ts = datetime.strptime(dates[0], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).timestamp()
        after = 1 if freeze_ts is not None and ts > freeze_ts else 0
    if not after:
        explain.append('SWEEP date-not-after-preregistration (%s vs %s)' % (dates, freeze_ts))
    return ok, after, {k: v[0] for k, v in verdicts.items()}


def regression(lane, rev, work, owner_repos, explain):
    fleet = os.path.join(work, 'fleet')
    os.makedirs(fleet)
    for r in sorted(owner_repos):
        os.symlink(os.path.join(FLEET, r), os.path.join(fleet, r))
    clone = os.path.join(fleet, 'tameshi-shokunin')
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', lane, clone], check=True, env=env(), capture_output=True)
    subprocess.run(['git', '-C', clone, 'checkout', '-q', '--detach', rev], check=True, env=env(), capture_output=True)
    tmp = os.path.join(work, 'tmp')
    os.makedirs(tmp)
    e = env()
    e['TMPDIR'] = tmp
    try:
        r = subprocess.run(['bash', 'tools/mutate-and-run.sh', '--regression', '--workdir', os.path.join(work, 'reg')],
                           cwd=clone, stdin=subprocess.DEVNULL, capture_output=True, env=e, timeout=3600)
    except subprocess.TimeoutExpired:
        explain.append('REGRESSION timeout')
        return 0, 'timeout'
    out = r.stdout.decode(errors='replace')
    for line in out.split('\n'):
        if line.startswith('REGRESSION_CASE '):
            explain.append(line)
    last = [l for l in out.split('\n') if l.startswith('REGRESSION: ')]
    last = last[-1] if last else 'REGRESSION: (none) exit=%d' % r.returncode
    explain.append(last)
    return (1 if r.returncode == 0 and last.startswith('REGRESSION: PASS (cases=10 passed=10') else 0), last


def sourced_entry(lane, rev, rel, explain):
    added = git(lane, 'diff', '--name-only', '--diff-filter=A', BASE, rev, '--', 'corpus/knowledge/').stdout.decode().split()
    src = (show(lane, rev, 'corpus/SOURCES.md') or b'').decode('utf-8', 'surrogateescape')
    rows = {}
    for line in src.split('\n'):
        m = ROW_RE.match(line)
        if m:
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            if len(c) == 11:
                rows[m.group(1)] = c
    tail = rel.split('/', 1)[1]
    readme = show(lane, rev, 'corpus/README.md') or b''
    base_readme = show(lane, BASE, 'corpus/README.md') or b''
    new_readme = readme[len(base_readme):].decode('utf-8', 'surrogateescape') if readme.startswith(base_readme) else ''
    for path in added:
        head = (show(lane, rev, path) or b'').decode('utf-8', 'surrogateescape').split('\n')[:8]
        srcl = [l for l in head if l.startswith('source:')]
        if not srcl or tail not in srcl[0]:
            continue
        for sid in re.findall(r'\bS[0-9]{3,}\b', srcl[0]):
            c = rows.get(sid)
            if c and c[7] == 'mined' and c[8] == '2026-10-26' and path in [p.strip() for p in re.split(r'[,;]', c[10])]:
                name = path.split('corpus/', 1)[1]
                readme_ok = 1 if name in new_readme else 0
                explain.append('ENTRY %s source=%s readme=%d' % (path, sid, readme_ok))
                return 1, 1, readme_ok
        explain.append('ENTRY %s names the target but cites no mined row opened 2026-10-26 that lists it' % path)
        return 1, 0, 0
    explain.append('ENTRY none added after base names %s in its source: line' % tail)
    return 0, 0, 0


def measure(lane, rev, work):
    explain = []
    rev = git(lane, 'rev-parse', '--verify', rev + '^{commit}').stdout.decode().strip()
    raw = show(lane, rev, 'tools/mutate-and-run.sh')
    if raw is None:
        raise RuntimeError('runner missing at REV')
    text = raw.decode('utf-8', 'surrogateescape')
    recorded, legs, wired, info = wiring(text)
    for leg in legs:
        explain.append('C2_LEG %s: %s' % (leg, 'WIRED' if leg in wired else 'UNWIRED (%s)' % ','.join(info[leg]['missing'])))
    new = [l for l in legs if l not in BASE_LEGS]
    base_present = all(l in legs for l in BASE_LEGS)
    f = dict(new_legs=len(new), target_new=0, pin_ok=0, spec_prereg=0, sweep_ok=0, sweep_after_freeze=0,
             table_match=0, regression=0, entry=0, sourced=0, readme=0, predictions_held=0, predictions=0)
    owner_repos = set(v.split('/', 1)[0] for v in BASE_LEGS.values())
    if len(new) == 1 and base_present:
        leg = new[0]
        call = leg_call(text, leg)
        if call:
            rel, pin, lrev = call
            owner_repos.add(rel.split('/', 1)[0])
            f['target_new'] = 1 if rel not in BASE_LEGS.values() else 0
            if pin and lrev:
                blob = show(os.path.join(FLEET, rel.split('/', 1)[0]), lrev, rel.split('/', 1)[1])
                f['pin_ok'] = 1 if blob is not None and hashlib.sha256(blob).hexdigest() == pin else 0
            spec_path = '%s/%s.defects.spec' % (SPEC_DIR, leg)
            spec = show(lane, rev, spec_path)
            emb = heredoc(text, leg)
            if spec is not None and hashlib.sha256(spec).hexdigest() == SPEC_SHA and emb == spec:
                f['spec_prereg'] = 1
            else:
                explain.append('SPEC %s: sha-or-embedding-mismatch' % spec_path)
            if spec is not None:
                ids, preds = spec_defects(spec)
                first = git(lane, 'log', '--diff-filter=A', '--format=%ct', rev, '--', spec_path).stdout.decode().split()
                freeze_ts = int(first[-1]) if first else None
                sweep = show(lane, rev, SWEEP)
                if sweep is not None:
                    ok, after, verdicts = sweep_check(sweep, ids, pin or '-', freeze_ts, explain)
                    f['sweep_ok'], f['sweep_after_freeze'] = int(ok), after
                    want_table = ','.join('%s:%s' % (i, verdicts.get(i, '?')) for i in ids)
                    f['table_match'] = 1 if info[leg]['table'] == want_table else 0
                    f['predictions'] = len(ids)
                    f['predictions_held'] = sum(1 for i in ids if preds.get(i) == verdicts.get(i))
                else:
                    explain.append('SWEEP receipt missing at REV')
            f['entry'], f['sourced'], f['readme'] = sourced_entry(lane, rev, rel, explain)
        else:
            explain.append('LEG %s: regression call or PIN/REV variables unparsable' % leg)
    f['regression'], _ = regression(lane, rev, work, owner_repos, explain)
    depth = min(10, recorded, len(wired))
    need = ['target_new', 'pin_ok', 'spec_prereg', 'sweep_ok', 'sweep_after_freeze', 'table_match', 'regression',
            'entry', 'sourced', 'readme']
    passed = recorded == 10 and len(wired) == 10 and f['new_legs'] == 1 and all(f[k] == 1 for k in need)
    line = ('C2_R51: rev=%s recorded_cases=%d wired_legs=%d depth_score=%d new_legs=%d %s predictions_held=%d/%d '
            'C2_R51_PASS=%s' % (rev, recorded, len(wired), depth, f['new_legs'],
                                ' '.join('%s=%d' % (k, f[k]) for k in need), f['predictions_held'], f['predictions'],
                                'true' if passed else 'false'))
    return (0 if passed else 1), line, explain


def selftest():
    """Parser cases plus one end-to-end measure() on a throwaway repo (no ledger legs: must be false, no crash)."""
    cases = failed = 0

    def check(name, cond):
        nonlocal cases, failed
        cases += 1
        if not cond:
            failed += 1
            print('C2_R51_SELFTEST FAIL %s' % name)
    runner = ("#   js-a  r/a.mjs 1/2 (50 %)\nPIN_A=" + 'a' * 64 + "\nREV_A=" + 'b' * 40 + "\nTABLE_A='X:KILLED,Y:SURVIVED'\n"
              "  cat >\"$d/js-a.spec\" <<'EOT'\n@defect X\nEOT\n"
              "  regression_case_git js-a \\\n    'r/a.mjs' \"$PIN_A\" \"$REV_A\" \\\n"
              "    'js-a:js-a.spec:TABLE_A:2:1'\n")
    rec, legs, wired, info = wiring(runner)
    check('wired-one', rec == 1 and wired == ['js-a'])
    check('call-parse', leg_call(runner, 'js-a') == ('r/a.mjs', 'a' * 64, 'b' * 40))
    check('heredoc', heredoc(runner, 'js-a') == b'@defect X\n')
    rec2, _, wired2, _ = wiring(runner.replace("TABLE_A:2:1", "TABLE_A:2:2"))
    check('table-count-mismatch-unwired', rec2 == 1 and wired2 == [])
    rec3, _, wired3, _ = wiring(runner + "#   js-b  r/b.mjs 1/2 (50 %)\n")
    check('comment-only-leg-unwired', rec3 == 2 and wired3 == ['js-a'])
    ids, preds = spec_defects(b'# PREDICT KILLED - x\n@defect K1 | a\n@old a\n@new b\n# PREDICT SURVIVED\n@defect S1\n')
    check('predictions', ids == ['K1', 'S1'] and preds == {'K1': 'KILLED', 'S1': 'SURVIVED'})
    sweep = ('MUTATE_DATE: 2026-10-26T10:00:00Z\nCONTROL: GREEN (exit=0 duration-ms=5 pristine-sha256=%s)\n'
             'DEFECT K1: KILLED (exit=1 duration-ms=1) a\nDEFECT S1: SURVIVED (exit=0 duration-ms=1) b\n'
             'MUTATE_RESTORE: OK (x)\nMUTATE: DONE (x)\n' % ('c' * 64)).encode()
    ex = []
    ok, after, v = sweep_check(sweep, ids, 'c' * 64, 1000, ex)
    check('sweep-ok', ok and after == 1 and v == {'K1': 'KILLED', 'S1': 'SURVIVED'})
    ok, after, v = sweep_check(sweep, ids, 'c' * 64, 4e9, [])
    check('sweep-before-prereg', after == 0)
    ok, after, v = sweep_check(sweep.replace(b'GREEN', b'RED'), ids, 'c' * 64, 1000, [])
    check('sweep-red-control', not ok)
    root = tempfile.mkdtemp(prefix='tameshi-r51-c2-selftest-', dir=os.environ.get('TMPDIR') or None)
    try:
        d = os.path.join(root, 'lane')
        os.makedirs(os.path.join(d, 'tools'))
        g = lambda *a: subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, env=env())
        g('init', '-q')
        check('fixture-toplevel', g('rev-parse', '--show-toplevel').stdout.decode().strip() == os.path.realpath(d))
        open(os.path.join(d, 'tools/mutate-and-run.sh'), 'w').write('#!/bin/bash\necho "REGRESSION: FAIL (none)"; exit 1\n')
        g('add', '-A')
        g('-c', 'user.name=selftest', '-c', 'user.email=selftest@invalid', 'commit', '-qm', 'x')
        w = os.path.join(root, 'w')
        os.makedirs(w)
        global BASE
        saved, BASE = BASE, g('rev-parse', 'HEAD').stdout.decode().strip()
        try:
            rc, line, _ = measure(d, 'HEAD', w)
        finally:
            BASE = saved
        check('e2e-empty-ledger-false', rc == 1 and 'recorded_cases=0' in line and 'C2_R51_PASS=false' in line)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print('C2_R51_SELFTEST: cases=%d failed=%d' % (cases, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if argv == ['--selftest']:
        return selftest()
    ok = len(argv) in (6, 7) and argv[0] == '--lane' and argv[2] == '--rev' and argv[4] == '--work' \
        and (len(argv) == 6 or argv[6] == '--explain')
    if not ok:
        print('usage: measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain] | --selftest', file=sys.stderr)
        return 64
    work = os.path.realpath(argv[5])
    if not os.path.isdir(work) or os.listdir(work):
        print('C2_R51: SETUP (--work must be an existing empty directory)')
        return 2
    try:
        rc, line, explain = measure(os.path.realpath(argv[1]), argv[3], work)
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print('C2_R51: SETUP (%s)' % exc)
        return 2
    if len(argv) == 7:
        for e in explain:
            print(e)
    print(line)
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
