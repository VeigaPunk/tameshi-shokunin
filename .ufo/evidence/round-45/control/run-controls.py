#!/usr/bin/env python3
"""Round-45 pre-freeze controls: the cheapest ledgers/trees that skip the claimed work.

Each control is built in a fresh scratch Git repository (mktemp, `git -C "$D"`
only, toplevel verified before the first commit) seeded from the lane's
committed tree at --rev, then scored by the frozen counters. Nothing is written
into the lane except the printed receipts the caller redirects.

C1 controls (freshness):
  A  registry-derived ledger: every population row gets an entry whose
     "snapshot" is the row's own teaches cell and whose quote is that cell's
     first 6-25 tokens; no source is opened, no review exists.
  B  A plus a non-author `agree` review for every row, a committed report under
     .ufo/waves/round-45/ naming each id and the reviewer, but no
     orchestrator-written w2-results.json.
  C  B plus a forged w2-results.json naming the reviewer: the counter cannot
     tell forged orchestrator evidence from real, so this control shows the
     residual trust boundary (fresh counts only if quotes were located afresh,
     which A's registry-copied quotes are not).
C2 controls (coverage):
  D  package rows S202/S203 appended byte-exact, package entries copied
     byte-exact (no re-grounding, no lane snapshot anchor).
  E  rows normalized to lane ids S256/S257 with the round-45 snapshot anchors,
     package entries copied with only the `source:` id re-pointed (verified-at
     stays the campaign's 2026-10-24, nothing re-opened).
"""
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.abspath(sys.argv[sys.argv.index('--lane') + 1])
REV = sys.argv[sys.argv.index('--rev') + 1]
PKG = '/home/vgpnk/Projects/shokuknow/merge/tameshi'
C1 = '.ufo/evidence/round-45/freshness/measure.py'
C2 = '.ufo/evidence/round-45/coverage/measure.py'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def run(*args, cwd=None):
    return subprocess.run(list(args), cwd=cwd, env=ENV, capture_output=True, text=True)


def scratch():
    d = tempfile.mkdtemp(prefix='tameshi-r45-control-')
    run('git', '-C', d, 'init', '-q', '-b', 'm')
    top = run('git', '-C', d, 'rev-parse', '--show-toplevel').stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    archive = subprocess.run(['git', '-C', LANE, 'archive', REV], capture_output=True, check=True).stdout
    subprocess.run(['tar', '-x', '-C', d], input=archive, check=True)
    for p in (C1, C2):  # the counters under test, from the lane worktree (frozen bytes)
        os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
        shutil.copyfile(os.path.join(LANE, p), os.path.join(d, p))
    return d


def commit(d):
    run('git', '-C', d, 'add', '-A')
    r = run('git', '-C', d, '-c', 'user.name=control', '-c', 'user.email=control@scratch.invalid',
            'commit', '-qm', 'control')
    assert r.returncode == 0, r.stderr


def put(d, path, data):
    full = os.path.join(d, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'wb') as f:
        f.write(data if isinstance(data, bytes) else data.encode())


def score(d, counter):
    r = run(sys.executable, os.path.join(d, counter), '--lane', d, '--rev', 'm')
    lines = r.stdout.strip().splitlines()
    last = lines[-1] if lines else r.stderr.strip()
    why = {}
    for l in lines:
        if l.startswith('INVALID ') or l.startswith('REFUSED '):
            k = l.split(' ', 2)[2]
            why[k] = why.get(k, 0) + 1
    reasons = ' reasons=%s' % json.dumps(why, sort_keys=True) if why else ''
    return '%s exit=%d%s' % (last.replace('rev=m', 'rev=<scratch>'), r.returncode, reasons)


def c1_rows(d):
    sys.path.insert(0, os.path.join(d, os.path.dirname(C1)))
    import measure as m1
    text = open(os.path.join(d, 'corpus/SOURCES.md'), encoding='utf-8').read()
    return m1.population(m1.parse_rows(text))


def control_a(d):
    entries = []
    for rid, row in sorted(c1_rows(d).items()):
        snap = row['teaches'].encode()
        path = '.ufo/evidence/round-45/freshness/sources/%s.raw.gz' % rid
        put(d, path, gzip.compress(snap))
        entries.append(dict(id=rid, url=row['url'], opened='2026-10-25', verdict='holds',
                            raw_sha256=hashlib.sha256(snap).hexdigest(),
                            quote=' '.join(row['teaches'].split()[:12]),
                            snapshot=path, author='ControlAuthor'))
    put(d, '.ufo/evidence/round-45/freshness/ledger.json', json.dumps({'entries': entries}))
    return entries


def control_b(d, entries):
    rep = '.ufo/waves/round-45/w2/ControlReviewer.md'
    put(d, rep, 'ControlReviewer agrees: ' + ' '.join(e['id'] for e in entries) + '\n')
    put(d, '.ufo/evidence/round-45/freshness/reviews.json', json.dumps({'reviews': [
        dict(id=e['id'], reviewer='ControlReviewer', verdict='agree', report=rep) for e in entries]}))


def control_c(d):
    put(d, '.ufo/waves/round-45/w2-results.json', json.dumps({'results': [
        {'name': 'ControlReviewer', 'output': 'agree'}]}))


def pkg_row(rid):
    for line in open(os.path.join(PKG, 'SOURCES.append.md'), encoding='utf-8'):
        if re.match(r'^ {0,3}\|\s*%s\s*\|' % rid, line):
            return line
    raise SystemExit('package row %s missing' % rid)


def insert_rows(d, block):
    p = os.path.join(d, 'corpus/SOURCES.md')
    lines = open(p, encoding='utf-8').read().split('\n')
    last = max(i for i, l in enumerate(lines) if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', l))
    lines[last + 1:last + 1] = block.rstrip('\n').split('\n')
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))


ENTRIES = {'S202': 'r8-gtest-order-and-seed.md', 'S203': 'r8-gtest-primer-independence.md'}


def control_d(d):
    insert_rows(d, pkg_row('S202') + pkg_row('S203'))
    for name in ENTRIES.values():
        shutil.copyfile(os.path.join(PKG, 'knowledge/corpus/knowledge', name),
                        os.path.join(d, 'corpus/knowledge', name))


def control_e(d):
    snaps = {'S256': ('googletest-advanced.md', 'r8-gtest-order-and-seed.md'),
             'S257': ('googletest-primer.md', 'r8-gtest-primer-independence.md')}
    block = ''
    for new, (snap, entry) in snaps.items():
        data = open(os.path.join(LANE, '.ufo/evidence/round-45/coverage/sources', snap), 'rb').read()
        put(d, '.ufo/evidence/round-45/coverage/sources/' + snap, data)
        block += ('| %s | GoogleTest %s — https://raw.githubusercontent.com/google/googletest/'
                  'cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/%s | docs | A | control | '
                  '.ufo/evidence/round-45/coverage/sources/%s sha256 %s | control | mined | '
                  '2026-10-25 | 365d | corpus/knowledge/%s |\n' % (
                      new, snap, snap.replace('googletest-', ''), snap,
                      hashlib.sha256(data).hexdigest()[:8], entry))
        old = 'S202' if new == 'S256' else 'S203'
        text = open(os.path.join(PKG, 'knowledge/corpus/knowledge', entry), encoding='utf-8').read()
        text = text.lstrip('\n')
        first, rest = text.split('\n', 1)
        put(d, 'corpus/knowledge/' + entry, first.replace(old, new) + '\n' + rest)
    insert_rows(d, block)
    readme = os.path.join(d, 'corpus/README.md')
    open(readme, 'a', encoding='utf-8').write(
        '\n`knowledge/r8-gtest-order-and-seed.md` `knowledge/r8-gtest-primer-independence.md`\n')


def main():
    out = []
    d = scratch()
    commit(d)
    out.append('BASE  C1 ' + score(d, C1))
    out.append('BASE  C2 ' + score(d, C2))
    entries = control_a(d)
    commit(d)
    out.append('CTL_A C1 ' + score(d, C1))
    control_b(d, entries)
    commit(d)
    out.append('CTL_B C1 ' + score(d, C1))
    control_c(d)
    commit(d)
    out.append('CTL_C C1 ' + score(d, C1))
    shutil.rmtree(d)
    d = scratch()
    control_d(d)
    commit(d)
    out.append('CTL_D C2 ' + score(d, C2))
    shutil.rmtree(d)
    d = scratch()
    control_e(d)
    commit(d)
    out.append('CTL_E C2 ' + score(d, C2))
    shutil.rmtree(d)
    print('\n'.join(out))


if __name__ == '__main__':
    main()
