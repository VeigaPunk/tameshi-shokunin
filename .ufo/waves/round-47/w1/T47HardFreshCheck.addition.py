# --- T47HardFreshCheck (tameshi round 47, wave 1): selftest cases for check(), the
# `--check FRAGMENT.json` seat helper. check() is never reached by the round-45/46
# selftest, so every rule in it survives today. Each case below calls check() with a
# scratch git lane (one population row S001 at rev `m`) plus a snapshot directory and
# a fragment file, and asserts the printed CHECK line and the exact exit code:
#   check:cmp:0  `row is None` inverted -> a row that IS in the population is answered
#               'invalid not in population' with exit 1 instead of being graded.
#   check:bool:1 rev registry `or ''` -> `and ''`: the population is always empty, so
#               the same in-population row is answered 'not in population'.
#   check:bool:0 `entry.get('snapshot') or ''` -> `and ''`: the snapshot name becomes
#               '', the snapshot is never read and a valid entry grades 'invalid'.
#   check:cmp:1 / check:int:1  the final mapping `0 if state in (...) else 1`:
#               a verified entry must exit 0; the mutants exit 1.
#   check:int:0 the early `row is None` exit 1 must stay exactly 1 (mutant: 2).
#   check:int:2 the final `else 1` for an invalid state must stay exactly 1 (mutant: 2).
#   check:int:3 the `.gz` suffix strip drops 3 chars (`page.txt.gz` -> `page.txt`);
#               dropping 4 (`page.tx`) loses the snapshot the snapdir holds.
#   check:bool:2 `name and os.path.isfile(full)` -> `or`: a named-but-absent snapshot
#               must grade 'invalid snapshot absent' (exit 1), not raise FileNotFoundError.
# No case reads the counter's own bytes; every separating input is a value check() returns.
import contextlib
import shutil


def _xT47HardFreshCheck_row():
    """The one population row (13 pipe cells) the scratch lane commits."""
    return ('| S001 | x \u2014 https://example.org/a | docs | A | flaky failure reports | '
            'section Metrics | flaky failures cluster in the same job | mined | 2026-10-25 '
            '| 180d | p |\n')


def _xT47HardFreshCheck_page():
    return (b'<html><body><p>Flaky failures cluster inside the same job because the rerun '
            b'repeats one order of the tests only and the second attempt hides the ordering '
            b'defect entirely from the report.</p></body></html>')


def _xT47HardFreshCheck_quote():
    """10 tokens: verbatim in the page, absent from the row cells, 3 shared content words."""
    return 'Flaky failures cluster inside the same job because the rerun'


def _xT47HardFreshCheck_entry(**kw):
    e = dict(id='S001', url='https://example.org/a', opened='2026-10-25', verdict='holds',
             raw_sha256=hashlib.sha256(_xT47HardFreshCheck_page()).hexdigest(),
             snapshot='snap/page.txt', quote=_xT47HardFreshCheck_quote())
    e.update(kw)
    return e


def _xT47HardFreshCheck_lane():
    """Scratch git lane carrying corpus/SOURCES.md at branch `m`; built via _xHardMeasure_build."""
    d = tempfile.mkdtemp(prefix='tameshi-r47-t47fresh-')
    _xHardMeasure_build(d, {'corpus/SOURCES.md': _xT47HardFreshCheck_row()}, False)
    return d


def _xT47HardFreshCheck_snapdir(name):
    """Snapshot directory holding the raw page under `name` (the .gz-compat lookup name)."""
    d = tempfile.mkdtemp(prefix='tameshi-r47-t47snap-')
    with open(os.path.join(d, name), 'wb') as fh:
        fh.write(_xT47HardFreshCheck_page())
    return d


def _xT47HardFreshCheck_run(lane, entry, snapdir):
    """check(lane, 'm', fragment, snapdir) with stdout captured; ('raised', text) on an exception."""
    fd, frag = tempfile.mkstemp(suffix='.json', prefix='tameshi-r47-t47frag-')
    os.close(fd)
    try:
        with open(frag, 'w', encoding='utf-8') as fh:
            json.dump(entry, fh)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = check(lane, 'm', frag, snapdir)
        except Exception as exc:  # the mutant's observable, never a kill by itself
            return 'raised %s' % type(exc).__name__, buf.getvalue()
        return rc, buf.getvalue()
    finally:
        try:
            os.unlink(frag)
        except OSError:
            pass


def _xT47HardFreshCheck_case(name, lane, entry, snapdir, want_rc, want_text):
    """One case: exact exit code and the CHECK line substring check() must print."""
    rc, text = _xT47HardFreshCheck_run(lane, entry, snapdir)
    ok = rc == want_rc and want_text in text
    last = text.strip().splitlines()[-1] if text.strip() else ''
    print('%s %s exit=%r want_exit=%r want=%r got=%r' % (
        'PASS' if ok else 'FAIL', name, rc, want_rc, want_text, last[:120]))
    return int(not ok)


def extra_T47HardFreshCheck():
    """Cases for the check() lineages: row lookup, snapshot name, .gz strip, state->exit map."""
    cases = failed = 0
    lane = snapdir = None
    try:
        lane = _xT47HardFreshCheck_lane()
        snapdir = _xT47HardFreshCheck_snapdir('page.txt')

        # cmp:0 / bool:1 / bool:0 / cmp:1 / int:1: an in-population row with a readable
        # snapshot must be graded verified ('verified ok') and exit 0. Every one of those
        # mutants turns this either into 'invalid not in population' or into exit 1.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H01_row_in_population_verified', lane, _xT47HardFreshCheck_entry(), snapdir,
            0, 'CHECK S001 verified ok')

        # int:0: the early missing-row exit must be exactly 1 (mutant returns 2). The
        # mutant cmp:0 instead falls through to grade(None) and raises, also a named FAIL.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H02_row_absent_exit_1', lane, _xT47HardFreshCheck_entry(id='S999'), snapdir,
            1, 'CHECK S999 invalid not in population')

        # int:3: entry names snap/page.txt.gz, the snapdir holds the raw page as page.txt;
        # the 3-char strip finds it, the mutant's 4-char strip looks for page.tx and grades
        # 'invalid snapshot absent' with exit 1.
        gz = _xT47HardFreshCheck_snapdir('page.txt')
        try:
            cases += 1
            failed += _xT47HardFreshCheck_case(
                'H03_gz_suffix_strip', lane,
                _xT47HardFreshCheck_entry(snapshot='snap/page.txt.gz'), gz,
                0, 'CHECK S001 verified ok')
        finally:
            shutil.rmtree(gz, ignore_errors=True)

        # bool:2: a snapshot name whose file is absent must grade 'invalid snapshot absent'
        # with exit 1. The `or` mutant opens the missing path and raises FileNotFoundError.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H04_missing_snapshot_no_raise', lane,
            _xT47HardFreshCheck_entry(snapshot='snap/absent.txt'), snapdir,
            1, 'CHECK S001 invalid snapshot absent')

        # int:2: a present row whose bytes do not hash must grade invalid with exit exactly 1
        # (mutant: else 2). The other final-mapping mutants are pinned by H01.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H05_invalid_state_exit_1', lane,
            _xT47HardFreshCheck_entry(raw_sha256='0' * 64), snapdir,
            1, 'CHECK S001 invalid sha mismatch')
    except Exception as exc:
        cases += 1
        failed += 1
        print('FAIL T47HardFreshCheck_harness raised %s: %s' % (type(exc).__name__, exc))
    finally:
        for d in (lane, snapdir):
            if d:
                shutil.rmtree(d, ignore_errors=True)
    return cases, failed
