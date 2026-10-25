# HardCover1: selftest cases for the round-45 coverage counter's row/entry rules.
# Each case is the smallest fixture that separates the pristine rule from one declared mutant
# (mutants.json group `coverage`, ids C01..C05) and asserts the counter's printed tally fields.

_xHardCover1_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'


def _xHardCover1_sha():
    return hashlib.sha256(_xHardCover1_SNAP).hexdigest()[:8]


def _xHardCover1_row(rid, url, anchor, used, status='mined'):
    return ('| %s | t — %s | docs | A | s | %s | t | %s | 2026-10-25 | 180d | %s |\n'
            % (rid, url, anchor, status, used))


def _xHardCover1_last_line(files, reg, readme):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    with tempfile.TemporaryDirectory(prefix='tameshi-r46-hc1-') as d:
        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())
        subprocess.run(['git', '-C', d, 'init', '-q', '-b', 'm'], env=env, capture_output=True, check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, env=env).stdout.decode().strip()
        assert top == os.path.realpath(d), 'scratch toplevel %r != %r' % (top, os.path.realpath(d))
        put('corpus/SOURCES.md', reg)
        for p, t in files.items():
            put(p, t)
        put('corpus/README.md', readme)
        put(SELF_PATH, open(os.path.abspath(__file__), 'rb').read())
        subprocess.run(['git', '-C', d, 'add', '-A'], env=env, capture_output=True, check=True)
        subprocess.run(['git', '-C', d, '-c', 'user.name=t', '-c', 'user.email=t@t',
                        'commit', '-qm', 'x', '--allow-empty'], env=env, capture_output=True, check=True)
        out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                             capture_output=True, text=True)
        return (out.stdout.strip().splitlines() or [''])[-1]


def extra_HardCover1():
    ea, eb = 'corpus/knowledge/a.md', 'corpus/knowledge/b.md'
    idx = '`knowledge/a.md` `knowledge/b.md`'
    sha = _xHardCover1_sha()
    entry = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
             'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
    snap45 = SNAP_PREFIX + 'advanced.md'
    snap45b = SNAP_PREFIX + 'primer.md'
    gt_url = 'https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md'
    good_reg = (_xHardCover1_row('S256', gt_url % 'advanced', snap45 + ' ' + sha, ea + ', ' + eb) +
                _xHardCover1_row('S257', gt_url % 'primer', snap45b + ' ' + sha, ea + ', ' + eb))
    good_files = {snap45: _xHardCover1_SNAP, snap45b: _xHardCover1_SNAP, ea: entry, eb: entry}

    # C01: a github.com URL that is not under google/googletest must not count as a row.
    gh_url = 'https://github.com/example/notgoogletest/docs/%s.md'
    reg_c01 = (_xHardCover1_row('S256', gh_url % 'advanced', snap45 + ' ' + sha, ea + ', ' + eb) +
               _xHardCover1_row('S257', gh_url % 'primer', snap45b + ' ' + sha, ea + ', ' + eb))

    # C02: a snapshot anchored under round-44 must not count (the anchor prefix is round-45 only).
    snap44 = '.ufo/evidence/round-44/coverage/sources/advanced.md'
    snap44b = '.ufo/evidence/round-44/coverage/sources/primer.md'
    reg_c02 = (_xHardCover1_row('S256', gt_url % 'advanced', snap44 + ' ' + sha, ea + ', ' + eb) +
               _xHardCover1_row('S257', gt_url % 'primer', snap44b + ' ' + sha, ea + ', ' + eb))
    files_c02 = {snap44: _xHardCover1_SNAP, snap44b: _xHardCover1_SNAP, ea: entry, eb: entry}

    # C03: a snapshot absent at REV must skip its row even when the anchor names sha256(b'')'s prefix.
    reg_c03 = (_xHardCover1_row('S256', gt_url % 'advanced', SNAP_PREFIX + 'missing.md e3b0c442',
                                ea + ', ' + eb) +
               _xHardCover1_row('S257', gt_url % 'primer', SNAP_PREFIX + 'missing2.md e3b0c442',
                                ea + ', ' + eb))
    files_c03 = {ea: entry, eb: entry}

    cases = [
        ('C01_github_not_googletest', reg_c01, good_files, idx, 'rows=0 entries=0'),
        ('C02_round44_snapshot_path', reg_c02, files_c02, idx, 'rows=0 entries=0'),
        ('C03_missing_snapshot_empty_sha', reg_c03, files_c03, idx, 'rows=0 entries=0'),
        ('C04_entry_without_source_line1', good_reg,
         {snap45: _xHardCover1_SNAP, snap45b: _xHardCover1_SNAP,
          ea: entry, eb: entry.replace('source: ', '', 1)}, idx, 'entries=1 indexed=1'),
        ('C05_entry_without_recheck_line3', good_reg,
         {snap45: _xHardCover1_SNAP, snap45b: _xHardCover1_SNAP,
          ea: entry, eb: entry.replace('recheck:', 'review:', 1)}, idx, 'entries=1 indexed=1'),
    ]
    failed = 0
    for name, reg, files, readme, want in cases:
        line = _xHardCover1_last_line(files, reg, readme)
        ok = want in line
        failed += not ok
        print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, want, line))
    return len(cases), failed
