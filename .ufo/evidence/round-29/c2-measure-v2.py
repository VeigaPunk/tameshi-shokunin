#!/usr/bin/env python3
"""Round 29 C2 counter v2 (coverage, frontier F6), re-frozen before data after the control wave.

Supersedes c2-measure.py (v1): seat CriticC2Design met v1 with a handwritten
fixture, an external absolute census row, a host symlink and a rewritten
snapshot (.ufo/waves/round-29/ctl/CriticC2Design.md). No data seat ran before v2.

Usage: c2-measure-v2.py --repo LANE_CLONE [--rev REV] [--kagi KAGI_REPO]

Predicate C2_F6_V2_PASS (same sentence in contract-amendment-1.json): PASS iff at REV
(1) `.ufo/evidence/round-29/f6/original/census.tsv` is byte-identical to the pinned
kagi `corpus/surface-census.sh`'s declaration `corpus/surface-census.tsv` at REV_BASH,
and every line of original `shapes.tsv` / `baseline.tsv` is a line of the pinned
`state-shape.tsv` / `drift-baseline.tsv`; (2) the original fixture kills survivor B5
(pinned gate, sha256 = PIN_BASH, exits 1 with a `SURFACE DIVERGED` line containing
`(declared exec, no execute bit)`, and the B5 mutant built from the runner's own
`@defect B5` spec exits 0); (3) this counter's own frozen ddmin, run on the original's
units, yields exactly the committed `.ufo/evidence/round-29/f6/minimized/` units, and
the minimized fixture kills B5 and is 1-minimal (removing any one unit loses the kill);
(4) `corpus/knowledge/survivor-fixture-minimization.md` has a `source:` line citing S024
and contains `units_original=N` and `units_minimized=M` with this counter's values,
and row S024 of corpus/SOURCES.md is `mined` with that entry path in `used-by`;
(5) the committed snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`
has sha256 3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99 (frozen at
commit 9f3084bc, before data), and a double-quoted string of 8 to 25 words containing
"minimal", on a `corpus/lessons/round-29.md` line naming S024 and that sha256, occurs
in the snapshot's normalized text.

Fixture layout (both original/ and minimized/): census.tsv, shapes.tsv, baseline.tsv
and host.tsv. host.tsv is a manifest, one node per line:
`<relative path>\t<dir|file>\t<octal mode>\t<content>`; the counter materializes it under
a scratch root (no symlinks; `..`, absolute paths and duplicate paths make the fixture
invalid). A unit is one line of any of the four files (blank lines included).

Prints `C2_F6_V2: fixture=present|absent|invalid anchored=0|1 kill_original=0|1 units_original=N
units_minimized=M ddmin_match=0|1 kill=0|1 one_minimal=0|1 entry_sourced=0|1
quote_located=0|1 rev=REV` then `PREDICATE: C2_F6_V2_PASS=true|false`.
Exit 0 iff PASS; 1 otherwise; 2 when REV, the runner pins or the pinned gate bytes
cannot be resolved.
"""
import argparse
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

F6 = '.ufo/evidence/round-29/f6'
ENTRY = 'corpus/knowledge/survivor-fixture-minimization.md'
LESSON = 'corpus/lessons/round-29.md'
SNAP = '.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html'
SNAP_SHA = '3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99'
FILES = ('census.tsv', 'shapes.tsv', 'baseline.tsv', 'host.tsv')
PINNED = {'census.tsv': 'corpus/surface-census.tsv', 'shapes.tsv': 'corpus/state-shape.tsv',
          'baseline.tsv': 'corpus/drift-baseline.tsv'}
EXEC_LINE = '(declared exec, no execute bit)'


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=env)


def show(repo, rev, path):
    p = git(repo, 'show', '%s:%s' % (rev, path))
    return p.stdout if p.returncode == 0 else None


def lines_of(raw):
    ls = raw.decode('utf-8', 'surrogateescape').split('\n')
    if ls and ls[-1] == '':
        ls.pop()
    return ls


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


def load_fixture(repo, rev, sub):
    """Return {file: [lines]} or None if absent; raises ValueError if invalid."""
    out = {}
    for f in FILES:
        raw = show(repo, rev, '%s/%s/%s' % (F6, sub, f))
        if raw is None:
            return None
        out[f] = lines_of(raw)
    return out


def to_units(fx):
    return [(f, i, line) for f in FILES for i, line in enumerate(fx[f])]


def from_units(units):
    fx = {f: [] for f in FILES}
    for f, _, line in units:
        fx[f].append(line)
    return fx


def materialize(fx, d):
    """Write a fixture dict to directory d; return False when host.tsv is invalid."""
    os.makedirs(d)
    for f in FILES[:3]:
        with open(os.path.join(d, f), 'w', encoding='utf-8', errors='surrogateescape') as h:
            h.write(''.join(l + '\n' for l in fx[f]))
    root = os.path.join(d, 'host')
    os.makedirs(root)
    seen = set()
    nodes = []
    for line in fx['host.tsv']:
        parts = line.split('\t', 3)
        if len(parts) != 4:
            return False
        rel, kind, mode, content = parts
        norm = os.path.normpath(rel)
        if (not rel or rel.startswith('/') or norm.startswith('..') or norm == '.' or norm in seen
                or kind not in ('dir', 'file') or not re.fullmatch(r'[0-7]{3,4}', mode)):
            return False
        seen.add(norm)
        nodes.append((norm, kind, int(mode, 8), content))
    for norm, kind, mode, content in sorted(nodes, key=lambda n: n[0].count('/')):
        p = os.path.join(root, norm)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if kind == 'dir':
            os.makedirs(p, exist_ok=True)
        else:
            if os.path.isdir(p):
                return False
            with open(p, 'w', encoding='utf-8', errors='surrogateescape') as h:
                h.write(content)
    for norm, kind, mode, content in sorted(nodes, key=lambda n: -n[0].count('/')):
        os.chmod(os.path.join(root, norm), mode)
    return True


class Oracle:
    def __init__(self, pristine, mutant, work):
        self.pristine, self.mutant, self.work, self.n, self.cache = pristine, mutant, work, 0, {}

    def run(self, gate, d):
        home = os.path.join(self.work, 'home')
        os.makedirs(home, exist_ok=True)
        env = {'PATH': '/usr/bin:/bin', 'HOME': home, 'LC_ALL': 'C', 'TZ': 'UTC'}
        p = subprocess.run(['timeout', '60', 'bash', gate, 'verify', '--root', os.path.join(d, 'host'),
                            '--census', os.path.join(d, 'census.tsv'), '--shapes', os.path.join(d, 'shapes.tsv'),
                            '--baseline', os.path.join(d, 'baseline.tsv')],
                           capture_output=True, text=True, env=env, cwd=self.work)
        return p.returncode, p.stdout

    def kills(self, units):
        key = tuple((f, i) for f, i, _ in units)
        if key in self.cache:
            return self.cache[key]
        self.n += 1
        d = os.path.join(self.work, 't%d' % self.n)
        ok = False
        if materialize(from_units(units), d):
            pe, po = self.run(self.pristine, d)
            hit = any(l.startswith('SURFACE DIVERGED ') and EXEC_LINE in l for l in po.splitlines())
            if pe == 1 and hit:
                me, _ = self.run(self.mutant, d)
                ok = me == 0
        subprocess.run(['chmod', '-R', 'u+rwx', d])
        shutil.rmtree(d, ignore_errors=True)
        self.cache[key] = ok
        return ok


def ddmin(units, test):
    """Delta debugging (complement form, as in S024's DeltaDebuggingReducer), frozen."""
    n = 2
    while len(units) >= 2:
        start = 0
        size = len(units) // n
        reduced = False
        while start < len(units):
            complement = units[:start] + units[start + size:]
            if test(complement):
                units = complement
                n = max(n - 1, 2)
                reduced = True
                break
            start += size
        if not reduced:
            if n == len(units):
                break
            n = min(n * 2, len(units))
    return units


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
        print('C2_F6_V2: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    runner = (show(repo, rev, 'tools/mutate-and-run.sh') or b'').decode('utf-8', 'surrogateescape')
    pin = re.search(r'^PIN_BASH=([0-9a-f]{64})$', runner, re.M)
    prev = re.search(r'^REV_BASH=([0-9a-f]{40})$', runner, re.M)
    if not (pin and prev):
        print('C2_F6_V2: runner pins unreadable at rev', file=sys.stderr)
        return 2
    gate = show(a.kagi, prev.group(1), 'corpus/surface-census.sh')
    if gate is None or hashlib.sha256(gate).hexdigest() != pin.group(1):
        print('C2_F6_V2: pinned gate bytes unavailable or digest mismatch', file=sys.stderr)
        return 2
    mutant = b5_mutant(runner, gate.decode('utf-8', 'surrogateescape'))
    pinned = {f: show(a.kagi, prev.group(1), p) for f, p in PINNED.items()}
    if mutant is None or None in pinned.values():
        print('C2_F6_V2: B5 spec or pinned declarations unavailable', file=sys.stderr)
        return 2

    orig = load_fixture(repo, rev, 'original')
    mini = load_fixture(repo, rev, 'minimized')
    state = 'present' if orig is not None and mini is not None else 'absent'
    anchored = kill_o = ddmin_match = kill = one_min = 0
    n_o = len(to_units(orig)) if orig else 0
    n_m = len(to_units(mini)) if mini else 0
    work = tempfile.mkdtemp(prefix='c2v2r29-')
    try:
        if state == 'present':
            anchored = int(show(repo, rev, '%s/original/census.tsv' % F6) == pinned['census.tsv']
                           and set(orig['shapes.tsv']) <= set(lines_of(pinned['shapes.tsv']))
                           and set(orig['baseline.tsv']) <= set(lines_of(pinned['baseline.tsv'])))
            pg, mg = os.path.join(work, 'pristine.sh'), os.path.join(work, 'mutant-B5.sh')
            open(pg, 'wb').write(gate)
            open(mg, 'w', encoding='utf-8', errors='surrogateescape').write(mutant)
            orc = Oracle(pg, mg, work)
            probe = os.path.join(work, 'probe')
            if not materialize(orig, probe) or not materialize(mini, probe + 'm'):
                state = 'invalid'
            else:
                ou, mu = to_units(orig), to_units(mini)
                kill_o = int(orc.kills(ou))
                if kill_o:
                    got = ddmin(ou, orc.kills)
                    ddmin_match = int([(f, l) for f, _, l in got] == [(f, l) for f, _, l in mu])
                kill = int(orc.kills(mu))
                if kill:
                    one_min = 1
                    for k in range(len(mu)):
                        if orc.kills(mu[:k] + mu[k + 1:]):
                            one_min = 0
                            print('  not-minimal: removable %s line %d' % (mu[k][0], mu[k][1] + 1))
            print('  oracle tests run: %d' % orc.n)
    finally:
        subprocess.run(['chmod', '-R', 'u+rwx', work])
        shutil.rmtree(work, ignore_errors=True)

    entry = (show(repo, rev, ENTRY) or b'').decode('utf-8', 'replace')
    src_ok = any(l.lower().startswith('source:') and re.search(r'\bS024\b', l) for l in entry.splitlines())
    nums_ok = ('units_original=%d' % n_o) in entry and ('units_minimized=%d' % n_m) in entry
    sources = (show(repo, rev, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    row = [l for l in sources.splitlines() if l.startswith('| S024 |')]
    cells = [c.strip() for c in row[0].strip().strip('|').split('|')] if len(row) == 1 else []
    row_ok = len(cells) == 11 and cells[7] == 'mined' and ENTRY in cells[10]
    entry_sourced = int(bool(entry) and src_ok and nums_ok and row_ok)

    snap = show(repo, rev, SNAP)
    quote_located = 0
    if snap is not None and hashlib.sha256(snap).hexdigest() == SNAP_SHA:
        page = norm(snap.decode('utf-8', 'replace'))
        lesson = (show(repo, rev, LESSON) or b'').decode('utf-8', 'replace')
        for line in lesson.splitlines():
            if not re.search(r'\bS024\b', line) or SNAP_SHA not in line:
                continue
            for q in re.findall(r'"([^"]+)"|\u201c([^\u201d]+)\u201d', line):
                q = norm(q[0] or q[1])
                if 8 <= len(q.split()) <= 25 and 'minimal' in q.lower() and q in page:
                    quote_located = 1

    print('C2_F6_V2: fixture=%s anchored=%d kill_original=%d units_original=%d units_minimized=%d ddmin_match=%d '
          'kill=%d one_minimal=%d entry_sourced=%d quote_located=%d rev=%s'
          % (state, anchored, kill_o, n_o, n_m, ddmin_match, kill, one_min, entry_sourced, quote_located, rev))
    passed = (state == 'present' and anchored and kill_o and ddmin_match and kill and one_min
              and entry_sourced and quote_located)
    print('PREDICATE: C2_F6_V2_PASS=%s' % ('true' if passed else 'false'))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
