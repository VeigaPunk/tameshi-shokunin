# T47HardCoverGt (round 47, C2 operability): selftest additions for the round-45 coverage counter.
# The four mutants below sit in `Tree.read` (the `binary` flag) and in `gt_rows` (the snapshot read
# and the two `group(0)` indexes). Every one of them makes a counter run die inside `gt_rows`, and
# the round-46 suite reaches that path only through a subprocess whose last stdout line it indexes:
# the frozen case raises IndexError and the suite exits on a bare traceback, which the pool scores
# as `crashed`, not `killed`. So the probes here drive `gt_rows` on a scratch lane in process and
# report the raised call as a named FAIL, and `selftest()` below keeps the process alive after the
# frozen suite dies so those FAIL lines can be printed. The probes print nothing when they pass, so
# a crash outside their inputs stays an unlabelled crash exactly as without this addition.

_xT47HardCoverGt_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
_xT47HardCoverGt_ENTRY = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
                          'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
_xT47HardCoverGt_EA = 'corpus/knowledge/a.md'
_xT47HardCoverGt_EB = 'corpus/knowledge/b.md'
_xT47HardCoverGt_URL = 'https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md'
_xT47HardCoverGt_result = []


def _xT47HardCoverGt_row(rid, name, used, digest):
    return ('| %s | t — %s | docs | A | s | %s%s.md %s | t | mined | 2026-10-25 | 180d | %s |\n'
            % (rid, _xT47HardCoverGt_URL % name, SNAP_PREFIX, name, digest, used))


def _xT47HardCoverGt_lane(reg, entries, readme, probe):
    """Commit a scratch lane holding the registry, the snapshots and the running counter's bytes."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    with tempfile.TemporaryDirectory(prefix='tameshi-r47-hcgt-') as d:
        def git(*a):
            return subprocess.run(['git', '-C', d, *a], env=env, capture_output=True)

        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'wb') as fh:
                fh.write(t if isinstance(t, bytes) else t.encode())

        git('init', '-q', '-b', 'm')
        top = git('rev-parse', '--show-toplevel').stdout.decode().strip()
        assert top == os.path.realpath(d), 'scratch toplevel %r != %r' % (top, os.path.realpath(d))
        put(SNAP_PREFIX + 'advanced.md', _xT47HardCoverGt_SNAP)
        put(SNAP_PREFIX + 'primer.md', _xT47HardCoverGt_SNAP)
        put('corpus/SOURCES.md', reg)
        for p, t in entries.items():
            put(p, t)
        put('corpus/README.md', readme)
        with open(os.path.abspath(__file__), 'rb') as fh:
            put(SELF_PATH, fh.read())
        git('add', '-A')
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
        return probe(d, env)


def _xT47HardCoverGt_probe_rows(d, env):
    """Read the registry through the rule under test; returns (row ids, row table)."""
    rows = gt_rows(Tree(d, 'm'))
    return sorted(rows), rows


def _xT47HardCoverGt_probe_measure(d, env):
    """Run the counter under test over the lane; returns (exit code, last stdout line)."""
    out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                         capture_output=True, text=True, env=env)
    lines = out.stdout.strip().splitlines()
    return out.returncode, (lines[-1] if lines else '')


def extra_T47HardCoverGt():
    if _xT47HardCoverGt_result:
        return _xT47HardCoverGt_result[0]
    _xT47HardCoverGt_result.append((0, 1))  # re-entry guard: a raising probe never loops back here
    digest = hashlib.sha256(_xT47HardCoverGt_SNAP).hexdigest()[:8]
    both = _xT47HardCoverGt_EA + ', ' + _xT47HardCoverGt_EB
    ents = {_xT47HardCoverGt_EA: _xT47HardCoverGt_ENTRY, _xT47HardCoverGt_EB: _xT47HardCoverGt_ENTRY}
    idx = '`knowledge/a.md` `knowledge/b.md`'
    two_rows = (_xT47HardCoverGt_row('S256', 'advanced', both, digest)
                + _xT47HardCoverGt_row('S257', 'primer', both, digest))
    one_row = _xT47HardCoverGt_row('S256', 'advanced', both, digest)
    bad_rows = (_xT47HardCoverGt_row('S256', 'advanced', both, 'deadbeef')
                + _xT47HardCoverGt_row('S257', 'primer', both, 'deadbeef'))

    # G01: two mined googletest rows whose anchors name existing snapshots must be counted.
    # The registry is read with the default text mode and each snapshot with `binary=True`, and the
    # row id is taken from the regex match's group 0 (`SNAP_RE`/`URL_RE` have no capture groups, so
    # indexing group 1 raises instead of yielding a row).
    def g01():
        names, _rows = _xT47HardCoverGt_lane(two_rows, ents, idx, _xT47HardCoverGt_probe_rows)
        return names == ['S256', 'S257'], 'row_ids=%s' % (','.join(names) or '-')

    # G02: the snapshot must reach the row as bytes (its sha256 is checked and its text folded), and
    # the used-by cell must be split into the entry paths it names.
    def g02():
        _names, rows = _xT47HardCoverGt_lane(two_rows, ents, idx, _xT47HardCoverGt_probe_rows)
        row = rows['S256']
        ok = row['text'] == fold(_xT47HardCoverGt_SNAP.decode()) and row['used'] == set(ents)
        return ok, 'text=%r used=%s' % (row['text'][:40], ','.join(sorted(row['used'])) or '-')

    # G03: a row whose anchor digest cannot match any prefix of the snapshot bytes is dropped, and
    # dropping it must leave no row rather than raise on the way.
    def g03():
        names, _rows = _xT47HardCoverGt_lane(bad_rows, ents, idx, _xT47HardCoverGt_probe_rows)
        return names == [], 'row_ids=%s' % (','.join(names) or '-')

    # G04: the whole counter completes over the same fixture and reports the two rows and a pass.
    def g04():
        rc, line = _xT47HardCoverGt_lane(two_rows, ents, idx, _xT47HardCoverGt_probe_measure)
        return rc == 0 and 'rows=2' in line and 'C2_R45_PASS=true' in line, 'exit=%d %s' % (rc, line)

    # G05: with a single row the same read path still reaches a verdict (one row is too few).
    def g05():
        rc, line = _xT47HardCoverGt_lane(one_row, ents, idx, _xT47HardCoverGt_probe_measure)
        return rc == 1 and 'rows=1' in line and 'C2_R45_PASS=false' in line, 'exit=%d %s' % (rc, line)

    cases = [
        ('G01_gt_rows_reads_two_rows', g01),
        ('G02_gt_rows_snapshot_bytes_folded', g02),
        ('G03_gt_rows_mismatched_digest_dropped', g03),
        ('G04_measure_valid_fixture_passes', g04),
        ('G05_measure_single_row_completes', g05),
    ]
    failed = 0
    for name, fn in cases:
        try:
            ok, detail = fn()
        except Exception as exc:  # a mutant that makes the rule raise is a named failure, not a crash
            ok, detail = False, 'raised %s: %s' % (type(exc).__name__, exc)
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    _xT47HardCoverGt_result[0] = (len(cases), failed)
    return _xT47HardCoverGt_result[0]


_xT47HardCoverGt_frozen_selftest = selftest


def selftest():
    """Run the frozen case suite; if it dies, give the probes above the chance to name the crash.

    A round-46 case indexes the last stdout line of the counter run it launches, so a counter that
    dies on the way raises IndexError inside the suite and the process exits on a traceback. Here
    that exception is held, the probes run, and their FAIL lines carry the input separation; when
    every probe passes they print nothing and the run remains an unlabelled crash.
    """
    try:
        return _xT47HardCoverGt_frozen_selftest()
    except Exception:
        try:
            extra_T47HardCoverGt()
        except Exception as exc:
            print('T47HardCoverGt: probes raised %s: %s' % (type(exc).__name__, exc), file=sys.stderr)
        return 1
