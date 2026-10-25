#!/usr/bin/env python3
"""Round-46 C1 (calibration) counter: the standing SCORECARD self-assessment vs the repo at REV.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C1_R46_PASS=true iff self_pin=1, stmts_pin=1, statements=22, append_only=1 and
  mismatches=0, where mismatches = statements whose standing row is absent or unparseable
  (`unparsed`), whose frozen command printed no matching line (`unobservable`), or whose
  standing row states a value different from what the command prints at REV (`mismatch`).
  A statement's standing row is the LAST data row, in file order, of any SCORECARD.md table of
  its kind whose first cell equals the statement id (kind `cap`: header cell 1 `Capability`;
  kind `axis`: header cell 2 begins `Score`); tables inside fenced code blocks or HTML comments
  are ignored. For a `cap` row the claim is the evidence cell's
      `CMD` -> `PRINTED LINE`, exit N[, tool sha256 `12 hex`]
  (the arrow `→`), compared whole with (printed line, exit code[, sha256 prefix of the tool
  file at REV]); for an `axis` row the claim is the integer in the score cell, compared with
  the integer the command prints. statements.json at REV must hash to STATEMENTS_SHA256
  (stmts_pin) and the base SCORECARD.md must be a byte prefix of REV's (append_only).
Modes: --lane L --rev R --base B --work EMPTY_DIR (deciding); --emit (same, prints the standing rows
the observed values imply, for the L1 to append); --selftest.
"""
import argparse
import concurrent.futures
import contextlib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-46/calibration/measure.py'
STATEMENTS_PATH = '.ufo/evidence/round-46/calibration/statements.json'
STATEMENTS_SHA256 = 'a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9'
N_STATEMENTS = 22
FLEET = '/home/vgpnk/Projects/shokunin'
ARROW = '\u2192'
CLAIM_BASE = r'%s\s*`([^`]+)`,\s*exit (\d+)' % ARROW
CLAIM_SHA = CLAIM_BASE + r',\s*tool sha256 `([0-9a-f]{12})`'


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e


def git(*args, binary=False):
    out = subprocess.run(['git'] + list(args), capture_output=True, env=env())
    if out.returncode != 0:
        return None
    return out.stdout if binary else out.stdout.decode('utf-8', 'replace')


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


def cells_of(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def last_rows(text):
    rows = {}
    for header, body in tables(strip_hidden(text)):
        if header and header[0] == 'Capability':
            kind = 'cap'
        elif len(header) > 1 and header[1].startswith('Score'):
            kind = 'axis'
        else:
            continue
        for line in body:
            cells = cells_of(line)
            rows[(kind, cells[0])] = cells
    return rows


def claim_of(stmt, cells):
    if cells is None:
        return None
    if stmt['kind'] == 'axis':
        return (cells[1],) if len(cells) > 1 and re.fullmatch(r'\d+', cells[1]) else None
    evidence = cells[2] if len(cells) > 2 else ''
    m = re.search(CLAIM_SHA if stmt.get('sha_file') else CLAIM_BASE, evidence)
    return tuple(m.groups()) if m else None


def pick_line(stmt, out, code):
    pat = stmt['obs']
    if pat == 'census':
        rows = re.search(r'^== A rows\n(\d+)$', out, re.M)
        ok = re.search(r'^(SOURCES_CENSUS: CLEAN \(contract v1 \+ H4 id-or-path\))$', out, re.M)
        return ('rows=%s %s' % (rows.group(1), ok.group(1))) if rows and ok else None
    if pat == 'monitor':
        try:
            return str(json.loads(out)['calibration_restraint_score'])
        except (ValueError, KeyError, TypeError):
            return None
    m = re.search(pat, out, re.M)
    return m.group(1) if m else None


def observe(stmt, clone, mirror, rev, work):
    cwd = mirror if stmt['cwd'] == 'mirror' else clone
    argv = [a.format(work=work, clone=clone, rev=rev) for a in stmt['argv']]
    e = env()
    e['REV'] = rev
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=stmt['timeout'], env=e)
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    out = p.stdout + ('\n' + p.stderr if p.stderr else '')
    name = re.sub(r'\W+', '-', stmt['id'])
    with open(os.path.join(work, 'obs-%s.stdout' % name), 'w') as fh:
        fh.write(out[-200000:])
    line = pick_line(stmt, out, p.returncode)
    if line is None:
        return None, 'exit=%d' % p.returncode
    if stmt['kind'] == 'axis':
        return (line,), 'exit=%d' % p.returncode
    obs = [line, str(p.returncode)]
    if stmt.get('sha_file'):
        data = git('-C', clone, 'show', 'HEAD:%s' % stmt['sha_file'], binary=True)
        obs.append(hashlib.sha256(data).hexdigest()[:12] if data is not None else 'absent')
    return tuple(obs), 'exit=%d' % p.returncode


def setup(lane, rev, work):
    for sub in ('fleet',):
        os.makedirs(os.path.join(work, sub), exist_ok=True)
    for d in sorted(os.listdir(FLEET)):
        if d.endswith('-shokunin') and d != os.path.basename(lane) and os.path.isdir(os.path.join(FLEET, d)):
            os.symlink(os.path.join(FLEET, d), os.path.join(work, 'fleet', d))
    mirror = os.path.join(work, 'fleet', os.path.basename(lane))
    clone = os.path.join(work, 'clone')
    for dest in (mirror, clone):
        if subprocess.run(['git', 'clone', '-q', '--no-hardlinks', lane, dest], capture_output=True, env=env()).returncode \
                or subprocess.run(['git', '-C', dest, 'checkout', '-q', '--detach', rev], capture_output=True, env=env()).returncode:
            return None, None
    return clone, mirror


def measure(lane, rev, base, work, emit=False, pin=STATEMENTS_SHA256, n_expected=N_STATEMENTS):
    work = os.path.abspath(work)
    if os.path.exists(work) and os.listdir(work):
        print('C1_R46: --work must be empty or absent', file=sys.stderr)
        return 2
    os.makedirs(work, exist_ok=True)
    r = git('-C', lane, 'rev-parse', '--verify', rev + '^{commit}')
    if r is None:
        print('C1_R46: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.strip()
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = git('-C', lane, 'show', '%s:%s' % (rev, SELF_PATH), binary=True)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    raw = git('-C', lane, 'show', '%s:%s' % (rev, STATEMENTS_PATH), binary=True)
    stmts_pin = int(raw is not None and hashlib.sha256(raw).hexdigest() == pin)
    if raw is None:
        print('C1_R46: statements.json absent at rev', file=sys.stderr)
        return 2
    statements = json.loads(raw)['statements']
    clone, mirror = setup(lane, rev, work)
    if clone is None:
        print('C1_R46: clone/checkout failed', file=sys.stderr)
        return 2
    base_sc = git('-C', lane, 'show', '%s:SCORECARD.md' % base)
    rev_sc = git('-C', lane, 'show', '%s:SCORECARD.md' % rev)
    if base_sc is None or rev_sc is None:
        print('C1_R46: cannot read SCORECARD.md', file=sys.stderr)
        return 2
    append_only = int(rev_sc.startswith(base_sc))
    rows = last_rows(rev_sc)
    cache = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(statements)) as pool:
        futs = {}
        for s in statements:
            key = (tuple(s['argv']), s['cwd'], s['obs'], s.get('sha_file'), s['kind'])
            if key not in cache:
                cache[key] = pool.submit(observe, s, clone, mirror, rev, work)
            futs[s['id']] = cache[key]
    mism = unparsed = unobs = 0
    emitted = []
    for s in statements:
        claimed = claim_of(s, rows.get((s['kind'], s['id'])))
        observed, note = futs[s['id']].result()
        if observed is None:
            verdict = 'UNOBSERVABLE'
            unobs += 1
        elif claimed is None:
            verdict = 'UNPARSED'
            unparsed += 1
        else:
            verdict = 'MATCH' if tuple(claimed) == tuple(observed) else 'MISMATCH'
            mism += verdict == 'MISMATCH'
        print('STATEMENT %s/%s: claimed=%s observed=%s (%s) %s' % (
            s['kind'], s['id'], '|'.join(claimed) if claimed else '-', '|'.join(observed) if observed else '-', note, verdict))
        if emit and observed is not None:
            emitted.append((s, observed, rows.get((s['kind'], s['id']))))
    total = mism + unparsed + unobs
    passed = (self_pin == 1 and stmts_pin == 1 and len(statements) == n_expected and append_only == 1 and total == 0)
    if emit:
        for s, observed, old in emitted:
            print(emit_row(s, observed, old))
    print('C1_R46: self_pin=%d stmts_pin=%d statements=%d mismatches=%d unparsed=%d unobservable=%d append_only=%d '
          'total=%d rev=%s C1_R46_PASS=%s' % (self_pin, stmts_pin, len(statements), mism, unparsed, unobs, append_only,
                                              total, rev, 'true' if passed else 'false'))
    return 0 if passed else 1


def emit_row(stmt, observed, old):
    if stmt['kind'] == 'axis':
        what = old[2] if old and len(old) > 2 else 'see the evidence pointer in the round-46 SCORECARD block'
        return 'EMIT_AXIS | %s | %s | %s |' % (stmt['id'], observed[0], what)
    evidence = '`%s` %s `%s`, exit %s' % (stmt['cmd_text'], ARROW, observed[0], observed[1])
    if stmt.get('sha_file'):
        evidence += ', tool sha256 `%s`' % observed[2]
    what = old[1] if old and len(old) > 1 else (stmt.get('what') or '')
    first = old[3] if old and len(old) > 3 else (stmt.get('first') or '')
    return 'EMIT_CAP | %s | %s | %s | %s |' % (stmt['id'], what, evidence, first)


def selftest():
    env0 = env()
    env0.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    me = os.path.abspath(__file__)
    results = []
    cap_hdr = '| Capability | What | Evidence | First |\n|---|---|---|---|\n'
    axis_hdr = '\n| Axis | Score (0\u201310) | Rule | Commit | Round |\n|---|---|---|---|---|\n'
    base_sc = '# S\n\nintro\n'
    stmts = [
        dict(id='alpha', kind='cap', argv=['echo', 'ALPHA: 3/3 pass'], obs=r'^(ALPHA: \d+/\d+ pass)', cmd_text='echo alpha',
             sha_file=None, cwd='clone', timeout=60),
        dict(id='beta', kind='cap', argv=['sh', '-c', 'echo BETA: 5/5 pass; exit 3'], obs=r'^(BETA: \d+/\d+ pass)', cmd_text='beta',
             sha_file='tool.txt', cwd='clone', timeout=60),
        dict(id='score', kind='axis', argv=['echo', 'value=7'], obs=r'value=(\d+)', cmd_text='echo', sha_file=None, cwd='clone', timeout=60),
    ]

    def row_alpha(line='ALPHA: 3/3 pass', code=0):
        return '| alpha | w | `echo alpha` %s `%s`, exit %d | r1 |\n' % (ARROW, line, code)

    def row_beta(line='BETA: 5/5 pass', code=3, sha=None):
        sha = sha or hashlib.sha256(b'tool\n').hexdigest()[:12]
        return '| beta | w | `beta` %s `%s`, exit %d, tool sha256 `%s` | r1 |\n' % (ARROW, line, code, sha)

    def row_score(v='7'):
        return '| score | %s | rule | c | r |\n' % v

    good = base_sc + '\n' + cap_hdr + row_alpha() + row_beta() + '\n' + axis_hdr + row_score()
    cases = [
        ('T1_all_match', good, {}, 'total=0'),
        ('T2_value_mismatch', base_sc + cap_hdr + row_alpha('ALPHA: 2/3 pass') + row_beta() + axis_hdr + row_score(), {}, 'mismatches=1'),
        ('T3_exit_mismatch', base_sc + cap_hdr + row_alpha(code=1) + row_beta() + axis_hdr + row_score(), {}, 'mismatches=1'),
        ('T4_sha_mismatch', base_sc + cap_hdr + row_alpha() + row_beta(sha='0' * 12) + axis_hdr + row_score(), {}, 'mismatches=1'),
        ('T5_axis_mismatch', base_sc + cap_hdr + row_alpha() + row_beta() + axis_hdr + row_score('6'), {}, 'mismatches=1'),
        ('T6_absent_row_unparsed', base_sc + cap_hdr + row_alpha() + axis_hdr + row_score(), {}, 'unparsed=1'),
        ('T7_prose_claim_unparsed', base_sc + cap_hdr + '| alpha | w | it passes 3/3 | r1 |\n' + row_beta() + axis_hdr + row_score(), {}, 'unparsed=1'),
        ('T8_last_row_wins_stale_first', base_sc + cap_hdr + row_alpha('ALPHA: 1/3 pass') + row_beta() + '\n' + cap_hdr
         + row_alpha() + '\n' + axis_hdr + row_score(), {}, 'total=0'),
        ('T9_last_row_wins_stale_last', base_sc + cap_hdr + row_alpha() + row_beta() + '\n' + cap_hdr
         + row_alpha('ALPHA: 1/3 pass') + '\n' + axis_hdr + row_score(), {}, 'mismatches=1'),
        ('T10_fenced_table_ignored', base_sc + '```\n' + cap_hdr + row_alpha('ALPHA: 9/9 pass') + '```\n' + cap_hdr + row_alpha()
         + row_beta() + axis_hdr + row_score(), {}, 'total=0'),
        ('T11_html_comment_table_ignored', base_sc + '<!--\n' + cap_hdr + row_alpha('ALPHA: 9/9 pass') + '-->\n' + cap_hdr + row_alpha()
         + row_beta() + axis_hdr + row_score(), {}, 'total=0'),
        ('T12_unobservable_command', base_sc + cap_hdr + row_alpha() + row_beta() + axis_hdr + row_score(),
         {'argv0': ['sh', '-c', 'echo nothing useful']}, 'unobservable=1'),
        ('T13_append_only_broken', good, {'base_override': '# other base\n'}, 'append_only=0'),
        ('T14_statements_tampered_is_false', good, {'tamper': True}, 'C1_R46_PASS=false'),
        ('T15_self_pin_broken', good, {'selfbytes': b'# not the counter\n'}, 'self_pin=0'),
        ('T16_wrong_statement_count_is_false', good, {'drop': True}, 'C1_R46_PASS=false'),
        ('T17_axis_noninteger_unparsed', base_sc + cap_hdr + row_alpha() + row_beta() + axis_hdr + row_score('seven'), {}, 'unparsed=1'),
        ('T18_match_is_true', good, {}, 'C1_R46_PASS=true'),
    ]
    failed = 0
    for name, scorecard, opt, want in cases:
        with tempfile.TemporaryDirectory(prefix='tameshi-r46-c1-') as d:
            lane = os.path.join(d, 'lane')
            os.makedirs(lane)

            def g(*a):
                subprocess.run(['git', '-C', lane, *a], env=env0, capture_output=True, check=True)
            g('init', '-q', '-b', 'm')
            assert subprocess.run(['git', '-C', lane, 'rev-parse', '--show-toplevel'], capture_output=True,
                                  env=env0).stdout.decode().strip() == os.path.realpath(lane)
            st = [dict(s) for s in stmts]
            if 'argv0' in opt:
                st[0]['argv'] = opt['argv0']
            if opt.get('drop'):
                st = st[:2]
            payload = json.dumps(dict(statements=st), indent=1).encode()
            os.makedirs(os.path.join(lane, os.path.dirname(SELF_PATH)))
            with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
                fh.write(base_sc)
            with open(os.path.join(lane, 'tool.txt'), 'wb') as fh:
                fh.write(b'tool\n')
            with open(os.path.join(lane, STATEMENTS_PATH), 'wb') as fh:
                fh.write(payload)
            with open(os.path.join(lane, SELF_PATH), 'wb') as fh:
                fh.write(opt.get('selfbytes') or open(me, 'rb').read())
            g('add', '-A')
            g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base')
            base_arg = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            if 'base_override' in opt:
                with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
                    fh.write(opt['base_override'])
                g('add', '-A')
                g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'other base')
                base_arg = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
                fh.write(scorecard)
            if opt.get('tamper'):
                with open(os.path.join(lane, STATEMENTS_PATH), 'ab') as fh:
                    fh.write(b' ')
            g('add', '-A')
            g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'rev')
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                measure(lane, 'HEAD', base_arg, os.path.join(d, 'work'), pin=hashlib.sha256(payload).hexdigest(),
                        n_expected=len(st) if not opt.get('drop') else 3)
            lines = [l for l in buf.getvalue().splitlines() if l.startswith('C1_R46:')]
            line = lines[-1] if lines else 'NO-C1-LINE'
            ok = want in line
            failed += not ok
            print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, want, line))
    print('C1_R46_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--base')
    ap.add_argument('--work')
    ap.add_argument('--emit', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.base and a.work):
        ap.error('--lane, --rev, --base and --work are required')
    return measure(a.lane, a.rev, a.base, a.work, emit=a.emit)


if __name__ == '__main__':
    sys.exit(main())
