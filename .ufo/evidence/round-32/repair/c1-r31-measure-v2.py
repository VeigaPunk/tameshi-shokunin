#!/usr/bin/env python3
"""Round 31 C1 counter (calibration), round-32 repair v2: standing SCORECARD self-assessment vs repo state.

v2 (round 32, routed defects 1-2 of corpus/lessons/round-31-verifier-spotcheck.md) changes exactly two
conditions of the frozen round-31 counter (.ufo/evidence/round-31/c1-measure.py, left unchanged):
  - axis tables: second header cell must equal `Score (0–10)` (was: starts with `Score`);
  - append-only: the base SCORECARD.md bytes must be a byte prefix of REV's bytes (was: decoded text).
It is a repair instrument, not a round-32 claim counter; its output label stays C1_R31.

Frozen predicate (same sentence in contract.json and in this docstring):
  C1 passes at REV iff, for each of the 12 frozen statements, the last row of its
  frozen table type in the committed SCORECARD.md at REV states values equal to the
  values its frozen command prints when run at REV, and the base SCORECARD.md is a
  byte prefix of REV's SCORECARD.md.

Statements: the ten rows of the `| Capability |` tables (first cell = capability
name) and the two rows of the `| Axis | Score (0–10) |` tables (first cell = axis).
A statement's row is the LAST data row in file order, among tables of its type,
whose first cell equals its id. Tables inside fenced code blocks or HTML comments
are ignored. A row whose claim pattern does not match is UNPARSED; a command whose
output pattern does not match is UNOBSERVABLE; both count as mismatches.

Usage: c1-measure.py --rev REV [--lane LANE_REPO] [--base BASE] --work EMPTY_DIR
Prints one STATEMENT line per statement and
  C1_R31: statements=12 mismatches=M unparsed=U unobservable=O append_only=0|1 rev=REV C1_R31_PASS=true|false
Exit 0 iff C1_R31_PASS=true; 1 otherwise; 2 on setup error.
"""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys

FLEET = '/home/vgpnk/Projects/shokunin'
LANE = FLEET + '/tameshi-shokunin'
BASE = '36c1d3933f680125aeefc447f07db0f03004901a'

# id, table type, claim regex (on the whole row line), command (argv, run in clone), observed regex, timeout
CMD_D = ('git show "$REV:tools/mutate-and-run.sh" | python3 -c \'import re,sys; '
         'n=len(re.findall(r"^#   (?:js|bash)-\\S+\\s+\\S+\\s+\\d+/\\d+",sys.stdin.read(),re.M)); '
         'print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))\'')
STATEMENTS = [
    ('sources-registry', 'cap', r'exit (\d+), (\d+) rows',
     ['bash', '.ufo/evidence/kaika-round-1/sources-census-v2.sh'], 'census', 900),
    ('mutation sweep runner', 'cap', r'MUTATE_SELFTEST: (\d+)/(\d+) pass`?, exit (\d+)',
     ['bash', 'tools/mutate-and-run.sh', '--selftest'], r'MUTATE_SELFTEST: (\d+)/(\d+) pass', 1800),
    ('six-leg regression ledger', 'cap', r'REGRESSION: (\w+) \(cases=(\d+) passed=(\d+)[^`]*`?, exit (\d+)',
     ['bash', 'tools/mutate-and-run.sh', '--regression', '--workdir', '{work}/regression-wd'],
     r'^REGRESSION: (\w+) \(cases=(\d+) passed=(\d+)', 2700),
    ('repeated pristine-control gate', 'cap', r'(PASS|FAIL) \((\d+) cases\), exit (\d+)',
     ['python3', 'tools/repeat-control.py', '--selftest'], r'^SELFTEST: (PASS|FAIL) \((\d+) cases\)', 900),
    ('six-leg content-disposition probe', 'cap', r'--selftest` → (\d+)/(\d+) PASS(\d+)',
     ['python3', 'tools/pin-disposition.py', '--selftest'], r'^SELFTEST: PASS \((\d+)/(\d+)\)', 900),
    ('exposed witness provenance correction', 'cap', r'metadata selftest(\d+)/(\d+) PASS(\d+)',
     ['python3', 'tools/witness-metadata.py', '--selftest'], r'^SELFTEST: PASS (\d+)/(\d+)', 900),
    ('effective expectation reconciliation', 'cap', r'PASS(\d+)/(\d+) exit(\d+)',
     ['python3', 'tools/evidence-disposition.py', '--selftest'], r'^SELFTEST: PASS \((\d+)/(\d+)\)', 900),
    ('retained invocation-context gate', 'cap', r'→ exit(\d+), copied-source CLI selftest(\d+)/(\d+)',
     ['python3', '.ufo/evidence/round-15/verify.py', '--rev', '7650fe4db89f3a706aed63d048ac47e02289cc72'],
     r'summary SELFTEST: PASS \((\d+)/(\d+)\)', 900),
    ('hermetic env-differential probe', 'cap', r'actual(\d+)/(\d+)',
     ['python3', 'tools/env-diff.py', '--selftest'], r'^ENVDIFF_SELFTEST: (\d+)/(\d+) pass', 900),
    ('callback-authoritative wave accounting', 'cap', r'frozen counter(\d+)/(\d+)',
     ['python3', 'tools/wave-accounting.py', '--selftest'], r'^ACCOUNTING_SELFTEST: (\d+)/(\d+) pass', 900),
    ('depth', 'axis', None, ['bash', '-c', CMD_D], r'depth_score=(\d+)', 300),
    ('calibration', 'axis', None,
     ['python3', '.ufo/evidence/round-21/coldread/measure.py', '--repo', '{clone}', '--rev', '{rev}'],
     'monitor', 900),
]


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e


def git(*args, **kw):
    return subprocess.run(['git'] + list(args), capture_output=True, text=True, env=env(), **kw)


def strip_hidden(text):
    """Blank fenced code blocks and HTML comments, keeping line numbering."""
    text = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    out, fenced = [], False
    for line in text.split('\n'):
        if line.lstrip().startswith('```'):
            fenced = not fenced
            out.append('')
            continue
        out.append('' if fenced else line)
    return out


def tables(lines):
    """Yield (header_cells, [row lines]) for maximal runs of lines starting with '|'."""
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                j += 1
            block = lines[i:j]
            header = [c.strip() for c in block[0].strip().strip('|').split('|')]
            yield header, block[2:]
            i = j
        else:
            i += 1


def first_cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def last_rows(text):
    rows = {}
    for header, body in tables(strip_hidden(text)):
        if header and header[0] == 'Capability':
            kind = 'cap'
        elif len(header) > 1 and header[1] == 'Score (0–10)':
            kind = 'axis'
        else:
            continue
        for line in body:
            cells = first_cells(line)
            rows[(kind, cells[0])] = line
    return rows


def claim_of(sid, kind, pattern, line):
    if line is None:
        return None
    if kind == 'axis':
        cells = first_cells(line)
        return (cells[1],) if len(cells) > 1 and re.fullmatch(r'\d+', cells[1]) else None
    m = re.search(pattern, line)
    return m.groups() if m else None


def observe(sid, argv, opattern, tmo, clone, mirror, rev, work):
    cwd = mirror if sid == 'six-leg regression ledger' else clone
    argv = [a.format(work=work, clone=clone, rev=rev) for a in argv]
    e = env()
    e['REV'] = rev
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=tmo, env=e)
        out, code = p.stdout, p.returncode
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    with open(os.path.join(work, 'obs-%s.stdout' % re.sub(r'\W+', '-', sid)), 'w') as f:
        f.write(out[-200000:])
    if opattern == 'census':
        m = re.search(r'^== A rows\n(\d+)$', out, re.M)
        return ((str(code), m.group(1)) if m else None), 'exit=%d' % code
    if opattern == 'monitor':
        try:
            return (str(json.loads(out)['calibration_restraint_score']),), 'exit=%d' % code
        except (ValueError, KeyError):
            return None, 'exit=%d' % code
    m = re.search(opattern, out, re.M)
    if not m:
        return None, 'exit=%d' % code
    g = m.groups()
    if sid == 'depth':
        return g, 'exit=%d' % code
    if sid == 'retained invocation-context gate':
        return (str(code),) + g, 'exit=%d' % code
    if sid in ('hermetic env-differential probe', 'callback-authoritative wave accounting'):
        return g, 'exit=%d' % code
    return g + (str(code),), 'exit=%d' % code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rev', required=True)
    ap.add_argument('--lane', default=LANE)
    ap.add_argument('--base', default=BASE)
    ap.add_argument('--work', required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    if os.path.exists(work) and os.listdir(work):
        print('C1_R31: --work must be empty or absent', file=sys.stderr)
        return 2
    os.makedirs(work + '/fleet', exist_ok=True)
    r = git('-C', a.lane, 'rev-parse', '--verify', a.rev + '^{commit}')
    if r.returncode:
        print('C1_R31: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.strip()
    for d in sorted(os.listdir(FLEET)):
        if d.endswith('-shokunin') and d != 'tameshi-shokunin' and os.path.isdir(os.path.join(FLEET, d)):
            os.symlink(os.path.join(FLEET, d), os.path.join(work, 'fleet', d))
    mirror = work + '/fleet/tameshi-shokunin'
    clone = work + '/clone'
    for dest in (mirror, clone):
        if git('clone', '-q', '--no-hardlinks', a.lane, dest).returncode or \
                git('-C', dest, 'checkout', '-q', '--detach', rev).returncode:
            print('C1_R31: clone/checkout failed', file=sys.stderr)
            return 2
    base_sc = git('-C', a.lane, 'show', a.base + ':SCORECARD.md')
    rev_sc = git('-C', a.lane, 'show', rev + ':SCORECARD.md')
    if base_sc.returncode or rev_sc.returncode:
        print('C1_R31: cannot read SCORECARD.md', file=sys.stderr)
        return 2
    base_b = subprocess.run(['git', '-C', a.lane, 'show', a.base + ':SCORECARD.md'], capture_output=True, env=env())
    rev_b = subprocess.run(['git', '-C', a.lane, 'show', rev + ':SCORECARD.md'], capture_output=True, env=env())
    append_only = int(base_b.returncode == 0 and rev_b.returncode == 0 and rev_b.stdout.startswith(base_b.stdout))
    rows = last_rows(rev_sc.stdout)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(STATEMENTS)) as ex:
        futs = {s[0]: ex.submit(observe, s[0], s[3], s[4], s[5], clone, mirror, rev, work) for s in STATEMENTS}
    mism = unparsed = unobs = 0
    for sid, kind, cpat, _argv, _op, _t in STATEMENTS:
        claimed = claim_of(sid, kind, cpat, rows.get((kind, sid)))
        observed, note = futs[sid].result()
        if claimed is None:
            verdict = 'UNPARSED'
            unparsed += 1
        elif observed is None:
            verdict = 'UNOBSERVABLE'
            unobs += 1
        else:
            verdict = 'MATCH' if tuple(claimed) == tuple(observed) else 'MISMATCH'
        if verdict != 'MATCH':
            mism += 1
        print('STATEMENT %s: claimed=%s observed=%s (%s) %s'
              % (sid, ','.join(claimed) if claimed else '-', ','.join(observed) if observed else '-', note, verdict))
    ok = mism == 0 and append_only == 1
    print('C1_R31: statements=%d mismatches=%d unparsed=%d unobservable=%d append_only=%d rev=%s C1_R31_PASS=%s'
          % (len(STATEMENTS), mism, unparsed, unobs, append_only, rev, 'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
