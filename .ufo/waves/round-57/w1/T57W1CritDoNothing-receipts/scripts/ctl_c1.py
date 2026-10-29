#!/usr/bin/env python3
"""Do-nothing controls for the round-57 C1 counter (scratch only; never writes the lane).

Each control = clone of the lane at BASE, plus commit A (frozen defects.json + a scratch copy of the
staged counter with its PIN_PENDING marker replaced by the defects.json sha256), plus commit B (the
ledger edit under test and, for CTL_OPEN, a Planned (round 58) paragraph). The counter then runs at B.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = os.environ['S']
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
WAVE = LANE + '/.ufo/waves/round-57/w1'
DEF_BYTES = open(WAVE + '/T57W1ExecExtract/stage/.ufo/evidence/round-57/c1/defects.json', 'rb').read()
DEF_SHA = hashlib.sha256(DEF_BYTES).hexdigest()
CTR_SRC = open(WAVE + '/T57W1ExecC1Counter/stage/.ufo/evidence/round-57/c1/measure.py', encoding='utf-8').read()
PIN_LINE = "DEFECTS_SHA256 = 'PIN_PENDING_SET_BY_L1_AFTER_THE_EXTRACTOR_SEAT_STAGES_DEFECTS_JSON'"
assert CTR_SRC.count(PIN_LINE) == 1, 'pin marker not found'
CTR_PINNED = CTR_SRC.replace(PIN_LINE, "DEFECTS_SHA256 = '%s'" % DEF_SHA)
DEFECTS = json.loads(DEF_BYTES.decode('utf-8'))['defects']
SPOTS = {'corpus/lessons/round-%d-verifier-spotcheck.md' % r for r in range(50, 57)}
LEDGER = 'corpus/routed-defects.json'
HARD = ('.ufo/evidence/round-57/c1/', '.ufo/evidence/round-57/control/', '.ufo/evidence/round-57/contract.json',
        '.ufo/evidence/round-57/freeze.json')
SOFT = ('.ufo/waves/', '.ufo/reports/')
ACK = ('planned', 'carried', 'still open', 'not worked', 'stay open', 'stays open', 'remain open',
       'remains open', 'routed to round', 'not fixed', 'unfixed', 'not landed')
IDENT = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid']
REASON = ('do-nothing control: the item was declined without any work on the tree; no fix is claimed')


def git(repo, *a, check=True):
    p = subprocess.run(['git', '-C', repo] + list(a), capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(a), p.stderr.decode('utf-8', 'replace')))
    return p


def norm(t):
    return ' '.join(t.split())



def is_anc(repo, a, b):
    return git(repo, 'merge-base', '--is-ancestor', a, b, check=False).returncode == 0


def show(repo, rev, path):
    p = git(repo, 'show', '%s:%s' % (rev, path), check=False)
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None


def make_clone(name):
    dest = os.path.join(S, 'c1', name)
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, dest], check=True, capture_output=True)
    git(dest, 'checkout', '-q', '--detach', BASE)
    assert git(dest, 'rev-parse', '--show-toplevel').stdout.decode().strip() == os.path.realpath(dest)
    return dest


def commit_all(repo, msg):
    git(repo, 'add', '-A')
    subprocess.run(['git', '-C', repo] + IDENT + ['commit', '-q', '--allow-empty', '-m', msg], check=True, capture_output=True)
    return git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()


def stage_commit_a(repo):
    d = os.path.join(repo, '.ufo/evidence/round-57/c1')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'defects.json'), 'wb').write(DEF_BYTES)
    open(os.path.join(d, 'measure.py'), 'w', encoding='utf-8').write(CTR_PINNED)
    os.chmod(os.path.join(d, 'measure.py'), 0o755)
    return commit_all(repo, 'control: staged defects.json and pinned counter copy')


def candidates(repo, key):
    """Lines (path, lineno, text) of BASE that contain KEY, case-insensitively, on admissible paths."""
    p = git(repo, 'grep', '-n', '-i', '-F', '-e', key, BASE, '--', '.', check=False)
    out = []
    for raw in p.stdout.decode('utf-8', 'replace').split('\n'):
        if not raw.startswith(BASE + ':'):
            continue
        rest = raw[len(BASE) + 1:]
        m = re.match(r'^(.*?):(\d+):(.*)$', rest)
        if not m:
            continue
        path, lineno, text = m.group(1), int(m.group(2)), m.group(3)
        if path in SPOTS or path == LEDGER or path.startswith(HARD) or path.startswith('/') or '..' in path.split('/'):
            continue
        if path.startswith(SOFT) and not path.endswith(key):
            continue
        out.append((path, lineno, text))
    return out


def excerpt_at(repo, path, lineno, key):
    """Lines a..b at BASE and a 15-400 char normalised excerpt containing KEY (taken from the file itself)."""
    text = show(repo, BASE, path)
    if text is None:
        return None
    lines = text.split('\n')
    a = b = lineno
    ex = norm(lines[a - 1])
    while len(ex) < 15 and b < len(lines) and b - a < 30:
        b += 1
        ex = norm('\n'.join(lines[a - 1:b]))
    if len(ex) > 400:
        pos = ex.lower().find(key.lower())
        if pos < 0:
            return None
        start = max(0, min(pos - 60, pos + len(key) - 400))
        ex = ex[start:start + 400]
    if not (15 <= len(ex) <= 400) or key.lower() not in ex.lower():
        return None
    if ex not in norm('\n'.join(lines[a - 1:b])):
        return None
    return {'path': path, 'lines': '%d-%d' % (a, b), 'excerpt': ex, '_a': a, '_b': b}


def first_evidence(repo, d):
    """The first admissible line (in grep order) of any key whose excerpt resolves: the literal arm."""
    for key in d['keys']:
        for path, lineno, _ in candidates(repo, key):
            ev = excerpt_at(repo, path, lineno, key)
            if ev:
                ev.pop('_a'), ev.pop('_b')
                return ev, key
    return None, None


def newest_commit(repo, path):
    p = git(repo, 'log', '-1', '--format=%H', BASE, '--', path, check=False)
    return p.stdout.decode().strip() or None


def fresh_search(repo, d):
    """Adversarial arm: for each admissible key-line, the newest commit after routed_at that touches the path
    and whose excerpt is absent at routed_at and carries no ACK words (what the counter's fixed arm checks)."""
    routed = d['routed_at']
    for key in d['keys']:
        for path, lineno, _ in candidates(repo, key):
            ev = excerpt_at(repo, path, lineno, key)
            if not ev:
                continue
            then = show(repo, routed, path)
            if then is not None and norm(ev['excerpt']) in norm(then):
                continue
            span = ' '.join((show(repo, BASE, path) or '').split('\n')[ev['_a'] - 1:ev['_b']]).lower()
            if any(w in span for w in ACK):
                continue
            commits = git(repo, 'log', '--format=%H', BASE, '--', path, check=False).stdout.decode().split()
            for c in commits:
                if is_anc(repo, c, routed):
                    break
                ev2 = dict((k, v) for k, v in ev.items() if not k.startswith('_'))
                return ev2, c, key
    return None, None, None


def write_ledger(repo, rows):
    base_doc = json.loads(show(repo, BASE, LEDGER))
    base_doc['defects'] = base_doc['defects'] + rows
    open(os.path.join(repo, LEDGER), 'w', encoding='utf-8').write(json.dumps(base_doc, indent=2, ensure_ascii=False) + '\n')


def run_counter(repo, rev, name):
    work = os.path.join(S, 'c1', 'work-' + name)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    p = subprocess.run([sys.executable, os.path.join(repo, '.ufo/evidence/round-57/c1/measure.py'), '--lane', repo,
                        '--rev', rev, '--work', work, '--explain'], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def build(name, mode):
    repo = make_clone(name)
    stage_commit_a(repo)
    rows, notes, missing = [], [], []
    quote_commit = None
    quote_lines = {}
    if mode in ('CTL_FAB_TEXT', 'CTL_FAB_TEXT_APPEND'):
        # probe (not do-nothing): one commit after BASE that only QUOTES each literal excerpt into a new lane file
        qpath = 'LOG.md' if mode == 'CTL_FAB_TEXT_APPEND' else 'corpus/lessons/round-57-quotes.md'
        body = []
        for d in DEFECTS:
            ev, key = first_evidence(repo, d)
            if ev is None:
                # probe-only fallback: quote the item's own line from its round's spot-check
                rnd = d['id'][1:].split('.')[0]
                spot = 'corpus/lessons/round-%s-verifier-spotcheck.md' % rnd
                for n, line in enumerate((show(repo, BASE, spot) or '').split('\n'), 1):
                    if d['id'] and ('**%s**' % d['id']) in line:
                        ev = {'path': spot, 'lines': '%d-%d' % (n, n), 'excerpt': norm(line)[:400]}
                        key = d['keys'][0]
                        break
                if ev is None:
                    continue
            body.append(ev['excerpt'])
            quote_lines[d['id']] = (len(body), ev, key)
        os.makedirs(os.path.dirname(os.path.join(repo, qpath)), exist_ok=True)
        prior = show(repo, BASE, qpath) or ''
        if mode == 'CTL_FAB_TEXT_APPEND':
            start = prior.count('\n')
            for i, k in enumerate(quote_lines):
                n, ev0, key = quote_lines[k]
                quote_lines[k] = (start + n, ev0, key)
        open(os.path.join(repo, qpath), 'w', encoding='utf-8').write(prior + '\n'.join(body) + '\n')
        quote_commit = commit_all(repo, 'control CTL_FAB_TEXT: quote excerpts into a new file (no repair)')
    for d in DEFECTS:
        if mode == 'CTL_0':
            continue
        if mode in ('CTL_FAB_TEXT', 'CTL_FAB_TEXT_APPEND'):
            if d['id'] not in quote_lines:
                missing.append(d['id'])
                continue
            n, ev0, key = quote_lines[d['id']]
            ev = {'path': qpath, 'lines': '%d-%d' % (n, n), 'excerpt': ev0['excerpt']}
            rows.append({'id': d['id'], 'status': 'fixed', 'commit': quote_commit, 'evidence': [ev],
                         'seat': name, 'note': 'probe: quoted excerpt, no repair'})
            continue
        ev, key = first_evidence(repo, d)
        if ev is None:
            missing.append(d['id'])
            continue
        row = {'id': d['id'], 'evidence': [ev], 'seat': name, 'note': 'do-nothing control %s' % name}
        if mode == 'CTL_DECLINE':
            row.update(status='declined', reason=REASON)
        elif mode == 'CTL_OPEN':
            row.update(status='open')
        elif mode == 'CTL_FAB':
            c = newest_commit(repo, ev['path'])
            row.update(status='fixed', commit=c)
            notes.append('%s literal key=%s commit=%s' % (d['id'], key, c))
        elif mode == 'CTL_FAB_SEARCH':
            ev2, c, key2 = fresh_search(repo, d)
            if ev2 is None:
                ev2, key2 = ev, key
                c = newest_commit(repo, ev['path'])
                notes.append('%s search: no fresh candidate, literal fallback' % d['id'])
            else:
                notes.append('%s search: path=%s key=%s commit=%s' % (d['id'], ev2['path'], key2, c))
            ev = ev2
            row.update(evidence=[ev], status='fixed', commit=c)
        rows.append(row)
    if mode != 'CTL_0':
        write_ledger(repo, rows)
    if mode == 'CTL_OPEN':
        sc = show(repo, BASE, 'SCORECARD.md')
        ids = ' '.join(d['id'] for d in DEFECTS)
        open(os.path.join(repo, 'SCORECARD.md'), 'w', encoding='utf-8').write(
            sc + '\n**Planned (round 58):** the open routed items of rounds 50-56: ' + ids + '\n')
    rev = commit_all(repo, 'control %s: ledger edit' % name)
    rc, out = run_counter(repo, rev, name)
    return {'name': name, 'mode': mode, 'rev': rev, 'rows': len(rows), 'missing_evidence': missing,
            'notes': notes, 'exit': rc, 'out': out}


if __name__ == '__main__':
    modes = sys.argv[1:] or ['CTL_0', 'CTL_DECLINE', 'CTL_OPEN', 'CTL_FAB', 'CTL_FAB_SEARCH', 'CTL_FAB_TEXT']
    res = []
    for m in modes:
        r = build('C1_' + m, m)
        res.append(r)
        print('=== %s rows=%d missing_evidence=%s exit=%d rev=%s' % (r['name'], r['rows'], r['missing_evidence'] or 'none',
                                                                 r['exit'], r['rev'][:12]))
        print(r['out'])
        for n in r['notes'][:60]:
            print('NOTE', n)
    json.dump(res, open(os.path.join(S, 'c1', 'results.json'), 'w'), indent=1)
