# HardCover2 (round 46, C2 operability): selftest additions for the round-45 coverage counter.
# Each case is the smallest scratch repo that separates the pristine predicate from one declared
# survivor (C06..C10 in hardening/mutants.json, group coverage); the assertion is on the PASS token.

_xHardCover2_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
_xHardCover2_ENTRY = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
                      'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
_xHardCover2_EA = 'corpus/knowledge/a.md'
_xHardCover2_EB = 'corpus/knowledge/b.md'
_xHardCover2_URL = 'https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md'


def _xHardCover2_row(i, name, used, digest):
    return ('| %s | t — %s | docs | A | s | %s%s.md %s | t | mined | 2026-10-25 | 180d | %s |\n'
            % (i, _xHardCover2_URL % name, SNAP_PREFIX, name, digest, used))


def _xHardCover2_build(reg, entries, readme, self_bytes=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')

    with tempfile.TemporaryDirectory(prefix='tameshi-r46-hc2-') as d:
        def git(*a):
            subprocess.run(['git', '-C', d, *a], env=env, capture_output=True, check=True)

        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())

        git('init', '-q', '-b', 'm')
        assert subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True,
                              env=env).stdout.decode().strip() == os.path.realpath(d)
        put(SNAP_PREFIX + 'advanced.md', _xHardCover2_SNAP)
        put(SNAP_PREFIX + 'primer.md', _xHardCover2_SNAP)
        put('corpus/SOURCES.md', reg)
        for p, t in entries.items():
            put(p, t)
        put('corpus/README.md', readme)
        me = open(os.path.abspath(__file__), 'rb').read()
        put(SELF_PATH, me if self_bytes is None else self_bytes)
        git('add', '-A')
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
        out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                             capture_output=True, text=True, env=env)
        return out.stdout.strip().splitlines()


def extra_HardCover2():
    digest = hashlib.sha256(_xHardCover2_SNAP).hexdigest()[:8]
    both = _xHardCover2_EA + ', ' + _xHardCover2_EB
    good = (_xHardCover2_row('S256', 'advanced', both, digest)
            + _xHardCover2_row('S257', 'primer', both, digest))
    ents = {_xHardCover2_EA: _xHardCover2_ENTRY, _xHardCover2_EB: _xHardCover2_ENTRY}
    idx = '`knowledge/a.md` `knowledge/b.md`'
    cases = [
        # C06: README may index by the full repo path; the mutant only accepts the short form.
        ('C06_readme_fullpath_index',
         lambda: _xHardCover2_build(good, ents, '`corpus/knowledge/a.md` `corpus/knowledge/b.md`'),
         ('indexed=2', 'C2_R45_PASS=true')),
        # C07: one googletest row must not be enough even when both entries are otherwise valid.
        ('C07_rows_one_fails',
         lambda: _xHardCover2_build(_xHardCover2_row('S256', 'advanced', both, digest), ents, idx),
         ('rows=1', 'C2_R45_PASS=false')),
        # C08: one entry must not be enough even with two rows and a matching index.
        ('C08_entries_one_fails',
         lambda: _xHardCover2_build(good, {_xHardCover2_EA: _xHardCover2_ENTRY}, idx),
         ('entries=1', 'C2_R45_PASS=false')),
        # C09: an unindexed entry must fail even when another entry is indexed.
        ('C09_indexed_lt_entries_fails',
         lambda: _xHardCover2_build(good, ents, '`knowledge/a.md`'),
         ('indexed=1', 'C2_R45_PASS=false')),
        # C10: a counter committed with different bytes at SELF_PATH must fail on self_pin.
        ('C10_self_pin_zero_fails',
         lambda: _xHardCover2_build(good, ents, idx, self_bytes=b'# not the running counter\n'),
         ('self_pin=0', 'C2_R45_PASS=false')),
    ]
    failed = 0
    for name, run, wants in cases:
        lines = run()
        summary = lines[-1] if lines else ''
        ok = all(w in summary for w in wants)
        failed += not ok
        print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, wants, summary))
    return len(cases), failed
