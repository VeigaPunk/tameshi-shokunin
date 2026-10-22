#!/usr/bin/env python3
"""Round 29 C2 counter (coverage, frontier F6: fixture minimization for survivors), frozen before data.

Usage: c2-measure.py --repo LANE_CLONE [--rev REV] [--kagi KAGI_REPO]

Predicate C2_F6_PASS (same sentence in contract.json): PASS iff the committed
fixture `.ufo/evidence/round-29/f6/minimized/` at REV kills survivor B5 (the
pinned kagi `corpus/surface-census.sh`, sha256 = PIN_BASH of
`tools/mutate-and-run.sh` at REV, exits 1 and prints a `SURFACE DIVERGED` line
with `(declared exec, no execute bit)`, while the B5 mutant built from the
runner's own `@defect B5` spec exits 0) AND the fixture is 1-minimal (removing
any one unit, i.e. one line of census.tsv, shapes.tsv or baseline.tsv or one
file under host/, loses that kill) AND `corpus/knowledge/survivor-fixture-minimization.md`
has a `source:` line citing S024, row S024 of corpus/SOURCES.md is `mined` with
that entry path in `used-by`, and a double-quoted string of at most 25 words on a
`corpus/lessons/round-29.md` line naming S024 occurs in the normalized text of
the committed snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`,
whose sha256 that line also names.

Prints `C2_F6: fixture=present|absent kill=0|1 units=N one_minimal=0|1 entry_sourced=0|1 quote_located=0|1 rev=REV`
then `PREDICATE: C2_F6_PASS=true|false`. Exit 0 iff PASS; 1 otherwise; 2 when
REV, the runner pins or the pinned gate bytes cannot be resolved.
"""
import argparse
import hashlib
import html
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

F6 = '.ufo/evidence/round-29/f6/minimized'
ENTRY = 'corpus/knowledge/survivor-fixture-minimization.md'
LESSON = 'corpus/lessons/round-29.md'
SNAP = '.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html'
TSV = ('census.tsv', 'shapes.tsv', 'baseline.tsv')
EXEC_LINE = '(declared exec, no execute bit)'


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)


def show(repo, rev, path):
    p = git(repo, 'show', '%s:%s' % (rev, path))
    return p.stdout if p.returncode == 0 else None


def b5_mutant(runner, pristine):
    m = re.search(r'^@defect B5 \|[^\n]*\n@old (.*?)\n@new (.*?)\n', runner, re.M | re.S)
    if not m:
        return None

    def dec(s):
        return re.sub(r'\\(.)', lambda x: {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}[x.group(1)], s)
    old, new = dec(m.group(1)), dec(m.group(2))
    if pristine.count(old) != 1:
        return None
    return pristine.replace(old, new)


def units(fx):
    out = []
    for name in TSV:
        lines = open(os.path.join(fx, name), encoding='utf-8', errors='surrogateescape').read().split('\n')
        if lines and lines[-1] == '':
            lines.pop()
        out += [('line', name, i) for i in range(len(lines))]
    for d, _, fs in os.walk(os.path.join(fx, 'host')):
        for f in sorted(fs):
            out.append(('file', os.path.relpath(os.path.join(d, f), fx), None))
    return out


def drop(fx, unit, dst):
    shutil.copytree(fx, dst, symlinks=True)
    kind, name, i = unit
    if kind == 'file':
        os.remove(os.path.join(dst, name))
    else:
        p = os.path.join(dst, name)
        lines = open(p, encoding='utf-8', errors='surrogateescape').read().split('\n')
        trail = lines and lines[-1] == ''
        if trail:
            lines.pop()
        del lines[i]
        open(p, 'w', encoding='utf-8', errors='surrogateescape').write('\n'.join(lines) + ('\n' if lines else ''))


def run(gate, fx, scratch):
    home = os.path.join(scratch, 'home')
    os.makedirs(home, exist_ok=True)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': home, 'LC_ALL': 'C', 'TZ': 'UTC'}
    p = subprocess.run(['timeout', '60', 'bash', gate, 'verify', '--root', os.path.join(fx, 'host'),
                        '--census', os.path.join(fx, 'census.tsv'), '--shapes', os.path.join(fx, 'shapes.tsv'),
                        '--baseline', os.path.join(fx, 'baseline.tsv')],
                       capture_output=True, text=True, env=env, cwd=scratch)
    return p.returncode, p.stdout


def interesting(pristine, mutant, fx, scratch):
    if not all(os.path.isfile(os.path.join(fx, n)) for n in TSV) or not os.path.isdir(os.path.join(fx, 'host')):
        return False
    pe, po = run(pristine, fx, scratch)
    me, _ = run(mutant, fx, scratch)
    hit = any(l.startswith('SURFACE DIVERGED ') and EXEC_LINE in l for l in po.splitlines())
    return pe == 1 and hit and me == 0


def norm(text):
    text = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', ' ', text)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    text = re.sub(r'\s+', ' ', text)
    return re.sub(r' ([,;:.)])', r'\1', text).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', default='HEAD')
    ap.add_argument('--kagi', default='/home/vgpnk/Projects/shokunin/kagi-shokunin')
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    r = git(repo, 'rev-parse', '--verify', '--quiet', a.rev + '^{commit}')
    if r.returncode:
        print('C2_F6: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    runner = (show(repo, rev, 'tools/mutate-and-run.sh') or b'').decode('utf-8', 'surrogateescape')
    pin = re.search(r'^PIN_BASH=([0-9a-f]{64})$', runner, re.M)
    prev = re.search(r'^REV_BASH=([0-9a-f]{40})$', runner, re.M)
    if not (pin and prev):
        print('C2_F6: runner pins unreadable at rev', file=sys.stderr)
        return 2
    gate = show(a.kagi, prev.group(1), 'corpus/surface-census.sh')
    if gate is None or hashlib.sha256(gate).hexdigest() != pin.group(1):
        print('C2_F6: pinned gate bytes unavailable or digest mismatch', file=sys.stderr)
        return 2
    mutant = b5_mutant(runner, gate.decode('utf-8', 'surrogateescape'))
    if mutant is None:
        print('C2_F6: B5 spec not applicable exactly once', file=sys.stderr)
        return 2

    work = tempfile.mkdtemp(prefix='c2r29-')
    try:
        pristine_p, mutant_p = os.path.join(work, 'pristine.sh'), os.path.join(work, 'mutant-B5.sh')
        open(pristine_p, 'wb').write(gate)
        open(mutant_p, 'w', encoding='utf-8', errors='surrogateescape').write(mutant)
        tree = os.path.join(work, 'tree')
        os.makedirs(tree)
        arc = git(repo, 'archive', '--format=tar', rev, '--', F6)
        present = 0
        if arc.returncode == 0 and arc.stdout:
            tarfile.open(fileobj=io.BytesIO(arc.stdout)).extractall(tree, filter='tar')
            present = int(os.path.isdir(os.path.join(tree, F6)))
        fx = os.path.join(tree, F6)
        kill = one_min = 0
        n = 0
        if present:
            scratch = os.path.join(work, 's')
            os.makedirs(scratch)
            kill = int(interesting(pristine_p, mutant_p, fx, scratch))
            us = units(fx) if all(os.path.isfile(os.path.join(fx, t)) for t in TSV) else []
            n = len(us)
            if kill:
                one_min = 1
                for k, u in enumerate(us):
                    dst = os.path.join(work, 'drop%d' % k)
                    drop(fx, u, dst)
                    if interesting(pristine_p, mutant_p, dst, scratch):
                        one_min = 0
                        print('  not-minimal: removable %s %s %s' % u)
                    shutil.rmtree(dst)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    entry = (show(repo, rev, ENTRY) or b'').decode('utf-8', 'replace')
    src_ok = any(l.lower().startswith('source:') and re.search(r'\bS024\b', l) for l in entry.splitlines())
    sources = (show(repo, rev, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    row = [l for l in sources.splitlines() if l.startswith('| S024 |')]
    cells = [c.strip() for c in row[0].strip().strip('|').split('|')] if len(row) == 1 else []
    row_ok = len(cells) == 11 and cells[7] == 'mined' and ENTRY in cells[10]
    entry_sourced = int(bool(entry) and src_ok and row_ok)

    snap = show(repo, rev, SNAP)
    quote_located = 0
    if snap is not None:
        sha = hashlib.sha256(snap).hexdigest()
        page = norm(snap.decode('utf-8', 'replace'))
        lesson = (show(repo, rev, LESSON) or b'').decode('utf-8', 'replace')
        for line in lesson.splitlines():
            if not re.search(r'\bS024\b', line) or sha not in line:
                continue
            for q in re.findall(r'"([^"]+)"|\u201c([^\u201d]+)\u201d', line):
                q = norm(q[0] or q[1])
                if q and len(q.split()) <= 25 and q in page:
                    quote_located = 1

    print('C2_F6: fixture=%s kill=%d units=%d one_minimal=%d entry_sourced=%d quote_located=%d rev=%s'
          % ('present' if present else 'absent', kill, n, one_min, entry_sourced, quote_located, rev))
    passed = bool(present and kill and one_min and entry_sourced and quote_located)
    print('PREDICATE: C2_F6_PASS=%s' % ('true' if passed else 'false'))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
