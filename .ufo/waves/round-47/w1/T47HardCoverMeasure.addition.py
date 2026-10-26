# T47HardCoverMeasure (round 47, C2 operability): selftest cases for the round-45 coverage
# counter's own `measure()` tally.  Each case builds one scratch lane and calls measure() in
# process (stdout captured), so a mutant that raises is reported as a named FAIL instead of a
# traceback, and the assertion is on a value the rule really returns: the exit code, the self-pin
# read, the REFUSED guard, the ENTRY index suffix and the row-id join each get an input that
# separates the pristine rule from one declared mutant.
# Mutants covered: measure:int:0, measure:int:1, measure:const:0, measure:cmp:6, measure:bool:5,
# measure:cmp:9.

import contextlib
import io
import shutil

_xT47HardCoverMeasure_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
_xT47HardCoverMeasure_IDX = '`knowledge/a.md` `knowledge/b.md`'
_xT47HardCoverMeasure_EA = 'corpus/knowledge/a.md'
_xT47HardCoverMeasure_EB = 'corpus/knowledge/b.md'
_xT47HardCoverMeasure_NOTE = 'corpus/knowledge/c.md'


def _xT47HardCoverMeasure_lane(files, reg, readme):
    """Create a scratch lane repo at rev `m`; the caller removes the returned directory."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    d = tempfile.mkdtemp(prefix='tameshi-r47-hcm-')

    def git(*a):
        out = subprocess.run(['git', '-C', d, *a], env=env, capture_output=True)
        if out.returncode != 0:
            raise RuntimeError('git %s: %s' % (' '.join(a), out.stderr.decode('utf-8', 'replace')))

    def put(p, t):
        full = os.path.join(d, p)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())

    git('init', '-q', '-b', 'm')
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], env=env,
                         capture_output=True).stdout.decode().strip()
    if top != os.path.realpath(d):
        raise RuntimeError('scratch toplevel %r != %r' % (top, os.path.realpath(d)))
    put(SNAP_PREFIX + 'advanced.md', _xT47HardCoverMeasure_SNAP)
    put(SNAP_PREFIX + 'primer.md', _xT47HardCoverMeasure_SNAP)
    put('corpus/SOURCES.md', reg)
    for p, t in files.items():
        put(p, t)
    put('corpus/README.md', readme)
    put(SELF_PATH, open(os.path.abspath(__file__), 'rb').read())
    git('add', '-A')
    git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
    return os.path.realpath(d)


def _xT47HardCoverMeasure_run(lane):
    """Call measure() in process; return (rc, captured stdout, exception name or '')."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = measure(lane, 'm')
    except Exception as exc:
        return None, buf.getvalue(), type(exc).__name__
    return rc, buf.getvalue(), ''


def _xT47HardCoverMeasure_case(name, lane, want_rc, wants, absent=()):
    """Assert the exit code (None = any), the wanted substrings and the forbidden ones."""
    rc, out, exc = _xT47HardCoverMeasure_run(lane)
    if exc:
        print('FAIL %s raised %s' % (name, exc))
        return 1
    summary = (out.strip().splitlines() or [''])[-1]
    ok = ((want_rc is None or rc == want_rc) and all(w in out for w in wants)
          and not any(a in out for a in absent))
    print('%s %s want=%r exit=%r got=%s' % ('PASS' if ok else 'FAIL', name,
                                            (want_rc,) + tuple(wants) + tuple('!' + a for a in absent),
                                            rc, summary))
    return 0 if ok else 1


def extra_T47HardCoverMeasure():
    digest = hashlib.sha256(_xT47HardCoverMeasure_SNAP).hexdigest()[:8]
    both = _xT47HardCoverMeasure_EA + ', ' + _xT47HardCoverMeasure_EB
    reg = (_xHardCover2_row('S256', 'advanced', both, digest)
           + _xHardCover2_row('S257', 'primer', both, digest))
    entry = _xHardCover2_ENTRY
    lanes = []
    failed = 0
    cases = 0
    try:
        # A passing lane: two googletest rows, two indexed entries, plus one knowledge note that
        # cites no row at all (it is refused silently by the pristine guard).
        good = _xT47HardCoverMeasure_lane(
            {_xT47HardCoverMeasure_EA: entry, _xT47HardCoverMeasure_EB: entry,
             _xT47HardCoverMeasure_NOTE: 'plain note, cites nothing\n'},
            reg, _xT47HardCoverMeasure_IDX)
        lanes.append(good)
        # A failing lane: one entry only, both rows and the index valid, so `passed` is false.
        split = _xT47HardCoverMeasure_lane({_xT47HardCoverMeasure_EA: entry}, reg,
                                           '`knowledge/a.md`')
        lanes.append(split)

        # measure:int:0 -> `return 0 if passed else 1` becomes `... 1 if passed else 1`: a passing
        # lane must still exit 0 (the mutant exits 1).
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_exit_zero_on_pass', good, 0,
                                             ('C2_R45_PASS=true',))
        # measure:int:1 -> the failing arm returns 2 instead of 1: a failing lane must exit 1.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_exit_one_on_fail', split, 1,
                                             ('C2_R45_PASS=false',))
        # measure:const:0 -> `tree.read(SELF_PATH, binary=True)` reads text instead of bytes and
        # hashing it raises; the pristine rule pins itself and passes.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_selfpin_binary', good, None,
                                             ('self_pin=1',))
        # measure:cmp:6 -> `why != 'cites no googletest row'` becomes `==`: the silent case (a
        # knowledge file citing no row) must stay silent.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_refused_only_for_other_reasons', good, None,
                                             ('C2_R45_PASS=true',), ('REFUSED ',))
        # measure:bool:5 -> `','.join(sorted(rows)) or '-'` becomes `and`: a non-empty row set
        # must print its ids, not the empty marker.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_row_ids_join', good, None,
                                             ('row_ids=S256,S257',))
        # measure:cmp:9 -> `'' if p in indexed else ' (not indexed)'` becomes `not in`: indexed
        # entries must carry no "(not indexed)" suffix.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_entry_index_suffix', good, None,
                                             ('ENTRY corpus/knowledge/a.md',), ('(not indexed)',))
    finally:
        for d in lanes:
            shutil.rmtree(d, ignore_errors=True)
    return cases, failed
