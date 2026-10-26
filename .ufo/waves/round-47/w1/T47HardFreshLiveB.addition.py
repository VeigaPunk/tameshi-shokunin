# --- T47HardFreshLiveB: selftest cases for six live() pool survivors of the round-46
# hardened freshness counter (live:cmp:1, live:cmp:2, live:int:2, live:const:1, live:cmp:3,
# live:const:2).  live() is never called from the round-46 selftest, so every case builds a
# scratch git lane (corpus/SOURCES.md + the round-45 ledger) and puts a stub `curl` first on
# PATH: no case touches the network, none reads the counter's own bytes, and the stub never
# writes outside the scratch directory.
#
# One fixture, one population (S001, S002, S004, S005 mined; S003 queued) and five entries:
#   S001 holds, in population, page HAS the quote, curl exits 0   -> present
#   S002 holds, in population, page LACKS the quote, curl exits 0 -> absent
#   S003 holds, NOT in population (queued row), page has quote    -> skipped by the gate
#   S004 drifted, in population, page has the quote               -> skipped by the gate
#   S005 holds, in population, page has the quote, curl exits 1   -> absent
#
# Separations (original value vs mutant value on the same input):
#   live:cmp:1   `verdict != 'holds'` -> `==`: S004 (drifted) is measured and the three
#                holdings rows are skipped, so the LIVE line set becomes {S004}.
#   live:cmp:2   `id not in pop` -> `in`: S003 (unregistered) is measured and every registered
#                row is skipped, so S003 appears in the output.
#   live:int:2   `res.returncode == 0` -> `== 1`: S001 (exit 0) drops to absent and S005
#                (exit 1, page on disk) turns present.
#   live:const:1 `capture_output=True` -> False: curl's own stdout leaks into the counter's
#                stdout; the stub marker is absent when the call captures, present when not.
#   live:cmp:3   quote `in` -> `not in`: S001 flips present->absent, S002 flips absent->present.
#   live:const:2 except-branch `present = False` -> True: a download that wrote no file makes
#                open() raise; the original reports absent, the mutant reports present.


def _xT47HardFreshLiveB_pages():
    return (b'<html><body><p>alpha present quote and beta marker</p></body></html>',
            b'<html><body><p>gamma unrelated sentence only</p></body></html>')


def _xT47HardFreshLiveB_stub(binp):
    """Write the executable `curl` the fixture puts first on PATH."""
    good, other = _xT47HardFreshLiveB_pages()
    script = '\n'.join([
        '#!' + sys.executable,
        'import os',
        'import sys',
        'args = sys.argv[1:]',
        'out = args[args.index("-o") + 1] if "-o" in args else ""',
        'url = args[-1]',
        'sys.stdout.write("CURL_STUB_STDOUT_MARKER\\n")',
        'sys.stdout.flush()',
        'if os.environ.get("T47FSLB_MODE") == "nofile":',
        '    sys.exit(0)',
        'page = %r' % good,
        'status = 0',
        'if url.endswith("/absent"):',
        '    page = %r' % other,
        'elif url.endswith("/error"):',
        '    status = 1',
        'if out:',
        '    fh = open(out, "wb")',
        '    fh.write(page)',
        '    fh.close()',
        'sys.exit(status)',
        ''])
    path = os.path.join(binp, 'curl')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(script)
    os.chmod(path, 0o755)


def _xT47HardFreshLiveB_row(rid, slug, status):
    # 11 pipe cells: id | source | docs | A | scope | anchor | teaches | status | opened | ttl | x
    return ('| %s | doc %s - http://fleet.invalid/%s | docs | A | mutants detected | section | '
            'valid | %s | 2026-10-25 | 180d | p |\n' % (rid, rid.lower(), slug, status))


def _xT47HardFreshLiveB_entries():
    quote = 'alpha present quote'
    absent = 'alpha missing quote'
    return [
        dict(id='S001', url='http://fleet.invalid/present', verdict='holds', quote=quote),
        dict(id='S002', url='http://fleet.invalid/absent', verdict='holds', quote=absent),
        dict(id='S003', url='http://fleet.invalid/present', verdict='holds', quote=quote),
        dict(id='S004', url='http://fleet.invalid/present', verdict='drifted', quote=quote),
        dict(id='S005', url='http://fleet.invalid/error', verdict='holds', quote=quote),
    ]


def _xT47HardFreshLiveB_lane(work):
    d = os.path.realpath(os.path.join(work, 'lane'))
    os.makedirs(d)
    _xHardMeasure_git(d, 'init', '-q', '-b', 'm')
    top = _xHardMeasure_git(d, 'rev-parse', '--show-toplevel').strip()
    if os.path.realpath(top) != d:
        raise RuntimeError('fixture toplevel %r != scratch dir %r' % (top, d))
    files = {
        'corpus/SOURCES.md': ''.join([
            _xT47HardFreshLiveB_row('S001', 'present', 'mined'),
            _xT47HardFreshLiveB_row('S002', 'absent', 'mined'),
            _xT47HardFreshLiveB_row('S003', 'present', 'queued'),
            _xT47HardFreshLiveB_row('S004', 'present', 'mined'),
            _xT47HardFreshLiveB_row('S005', 'error', 'mined')]),
        LEDGER: json.dumps({'entries': _xT47HardFreshLiveB_entries()}),
    }
    for rel, text in files.items():
        full = os.path.join(d, rel)
        if os.path.dirname(full):
            os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(text)
    _xHardMeasure_git(d, 'add', '-A')
    _xHardMeasure_git(d, 'commit', '-q', '-m', 'fixture')
    return d


def _xT47HardFreshLiveB_env(binp):
    """Put the stub first on PATH and isolate git; return the environment to restore."""
    saved = dict(os.environ)
    for key in [k for k in os.environ if k.startswith('GIT_')]:
        del os.environ[key]
    os.environ['GIT_CONFIG_GLOBAL'] = '/dev/null'
    os.environ['GIT_CONFIG_SYSTEM'] = '/dev/null'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.environ['PATH'] = binp + os.pathsep + saved.get('PATH', '')
    os.environ.pop('T47FSLB_MODE', None)
    return saved


def _xT47HardFreshLiveB_restore(saved):
    os.environ.clear()
    os.environ.update(saved)


def _xT47HardFreshLiveB_run(lane, mode):
    """Call live() in-process with its prints captured; `mode` selects the stub behaviour."""
    saved_mode = os.environ.get('T47FSLB_MODE')
    if mode:
        os.environ['T47FSLB_MODE'] = mode
    else:
        os.environ.pop('T47FSLB_MODE', None)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        live(lane, 'm')
    finally:
        sys.stdout = old
        if saved_mode is None:
            os.environ.pop('T47FSLB_MODE', None)
        else:
            os.environ['T47FSLB_MODE'] = saved_mode
    return buf.getvalue()


def _xT47HardFreshLiveB_child(lane):
    """Run live() from a child interpreter: a non-capturing call leaks curl's stdout to it."""
    code = '\n'.join([
        'import importlib.util',
        'spec = importlib.util.spec_from_file_location("t47fslb", %r)' % os.path.abspath(__file__),
        'mod = importlib.util.module_from_spec(spec)',
        'spec.loader.exec_module(mod)',
        'mod.live(%r, "m")' % lane,
        ''])
    p = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True,
                       timeout=180, env=dict(os.environ))
    return p.returncode, p.stdout


def _xT47HardFreshLiveB_lines(out):
    return [line for line in out.splitlines() if line.startswith('LIVE ')]


def _xT47HardFreshLiveB_fields(out):
    m = re.search(r'^C1_R45_LIVE: (.*)$', out, re.M)
    return dict(re.findall(r'(\w+)=(\S+)', m.group(1))) if m else {}


def _xT47HardFreshLiveB_rmtree(path):
    import shutil
    shutil.rmtree(path, ignore_errors=True)


def extra_T47HardFreshLiveB():
    cases = []

    def check(name, ok, detail=''):
        cases.append(bool(ok))
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))

    work = tempfile.mkdtemp(prefix='tameshi-r47-fslb-work-')
    saved = None
    try:
        binp = os.path.join(work, 'bin')
        os.makedirs(binp)
        _xT47HardFreshLiveB_stub(binp)
        saved = _xT47HardFreshLiveB_env(binp)
        lane = _xT47HardFreshLiveB_lane(work)

        want = ['LIVE S001 present', 'LIVE S002 absent', 'LIVE S005 absent']
        out = _xT47HardFreshLiveB_run(lane, None)
        lines = _xT47HardFreshLiveB_lines(out)
        fields = _xT47HardFreshLiveB_fields(out)
        detail = '%r %r' % (lines, fields)

        # live:cmp:1 -- the verdict gate skips a `drifted` entry that is in the population.
        check('T47FSLB01_live_holds_verdict_gate', lines == want, detail)
        # live:cmp:2 -- the membership gate skips a `holds` entry that is not in the population.
        check('T47FSLB02_live_population_gate',
              lines == want and 'LIVE S003' not in out, detail)
        # live:int:2 -- exit 0 means "downloaded"; exit 1 means "do not read the target".
        check('T47FSLB03_live_returncode_gate',
              lines == want and fields.get('present') == '1' and fields.get('absent') == '2',
              detail)
        # live:cmp:3 -- a quote present in the page is reported present, not the reverse.
        check('T47FSLB04_live_quote_presence', lines == want, detail)

        # live:const:1 -- curl's own stdout is captured by the call, not inherited.
        rc, child_out = _xT47HardFreshLiveB_child(lane)
        check('T47FSLB05_live_captures_child_stdout',
              rc == 0 and 'CURL_STUB_STDOUT_MARKER' not in child_out
              and 'LIVE ' in child_out,
              'rc=%d marker=%s live=%s' % (rc, 'CURL_STUB_STDOUT_MARKER' in child_out,
                                          'LIVE ' in child_out))

        # live:const:2 -- a target that cannot be read is absent, not present.
        nofile = _xT47HardFreshLiveB_run(lane, 'nofile')
        nlines = _xT47HardFreshLiveB_lines(nofile)
        nfields = _xT47HardFreshLiveB_fields(nofile)
        check('T47FSLB06_live_unreadable_is_absent',
              nlines == ['LIVE S001 absent', 'LIVE S002 absent', 'LIVE S005 absent']
              and nfields.get('present') == '0' and nfields.get('absent') == '3',
              '%r %r' % (nlines, nfields))
    except Exception as exc:
        check('T47FSLB00_fixture_ran', False, 'raised %s: %s' % (type(exc).__name__, exc))
    finally:
        if saved is not None:
            _xT47HardFreshLiveB_restore(saved)
        _xT47HardFreshLiveB_rmtree(work)
    return len(cases), cases.count(False)
