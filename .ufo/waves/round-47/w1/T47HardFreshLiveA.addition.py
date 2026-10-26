# --- HardFreshLive (tameshi round 47, wave 1, seat T47HardFreshLiveA): live() cases.
# live() (the --live re-fetch mode) runs outside selftest() today, so the seven pool
# survivors below had no case at all. Every case here drives live() through a fixture
# git lane (corpus/SOURCES.md + the round-45 ledger at LEDGER) and a stub `curl` placed
# first on PATH inside the case: no network is touched, and the stub's exit code plus
# the bytes it writes to the `-o` target are the only inputs. Each assertion reads the
# rule's own observable output (the `LIVE <id> present|absent` lines and the
# `C1_R45_LIVE: present=N absent=M` summary) and its return code, never the source text.
#   L01 present fetch        - one `holds` entry in the population, stub exits 0 with a
#       body containing the quote: summary must be present=1 absent=0 and one
#       `LIVE S001 present` line. Separates live:int:0 (`ok = bad = 1` -> 2/1),
#       live:int:1 (`return 1`), live:bool:0 (`or`->`and` empties the population ->
#       0/0 and no LIVE line), live:cmp:0 (`returncode != 0` skips the body check ->
#       0/1) and live:not:0 (`bad += present` -> 1/1).
#   L02 fetch failure        - stub exits 22 and writes nothing: a non-zero fetch is
#       `absent`, not `present`. Separates live:const:0 (`present = True` survives the
#       skipped body check -> present=1 absent=0).
#   L03 non-holds skipped    - the only ledger entry is `drifted` and IS in the
#       population: the gate `verdict != 'holds' or id not in pop` must skip it, so no
#       LIVE line and present=0 absent=0. Separates live:bool:1 (`or`->`and` makes the
#       gate False for `drifted`-in-population, so the entry is fetched -> 1/0).
#   L04 unreadable target    - stub exits 0 but writes no target: the body read raises
#       and the entry is `absent`. Separates live:const:2 (`present = True` in the
#       except arm -> present=1 absent=0).
_xT47HardFreshLiveA_QUOTE = 'Flaky failure reports are retained only when the rerun reproduces them'

# The fetched body: plain text (no tags), so extract() only folds it and the quote is present.
_xT47HardFreshLiveA_PAGE = (_xT47HardFreshLiveA_QUOTE
                            + ' verbatim inside the fetched body.\n').encode('utf-8')

# Stub `curl`: copy the body to the path after `-o`, then exit with the wanted code.
# Both are handed over through the environment so one stub serves every case.
_xT47HardFreshLiveA_STUB = '''#!/bin/sh
out=''
prev=''
for a in "$@"; do
  if [ "$prev" = '-o' ]; then out="$a"; fi
  prev="$a"
done
if [ -n "$out" ] && [ -n "$X47LIVE_BODY" ] && [ -f "$X47LIVE_BODY" ]; then
  cp "$X47LIVE_BODY" "$out" || exit 99
fi
exit "${X47LIVE_RC:-0}"
'''


def _xT47HardFreshLiveA_row(rid, url, status):
    """One registry line with the 13 pipe-split cells parse_rows() requires."""
    return '| %s | doc \u2014 %s | docs | A | s | a | t | %s | 2026-10-25 | 180d | p |\n' % (rid, url, status)


def _xT47HardFreshLiveA_lane(entries):
    """A throwaway git lane holding corpus/SOURCES.md and the ledger; returns (dir, rev)."""
    d = os.path.realpath(tempfile.mkdtemp(prefix='t47-freshlive-lane-'))
    subprocess.run(['git', '-C', d, 'init', '-q'], capture_output=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != d:
        raise RuntimeError('fixture toplevel %r != %r' % (top, d))
    os.makedirs(os.path.join(d, 'corpus'))
    with open(os.path.join(d, 'corpus', 'SOURCES.md'), 'w', encoding='utf-8') as fh:
        fh.write(''.join(_xT47HardFreshLiveA_row(e['id'], e['url'], 'mined') for e in entries))
    led = os.path.join(d, *LEDGER.split('/'))
    os.makedirs(os.path.dirname(led))
    with open(led, 'w', encoding='utf-8') as fh:
        json.dump({'entries': entries}, fh)
    for args in (('add', '-A'), ('commit', '-q', '-m', 'fixture')):
        subprocess.run(['git', '-C', d, '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                       capture_output=True)
    rev = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    if not rev:
        raise RuntimeError('fixture lane has no commit')
    return d, rev


def _xT47HardFreshLiveA_run(lane, rev, body, rc):
    """Run live() with a stub curl first on PATH; returns (returncode, captured stdout)."""
    import contextlib
    buf = io.StringIO()
    with tempfile.TemporaryDirectory(prefix='t47-freshlive-bin-') as bin_dir:
        exe = os.path.join(bin_dir, 'curl')
        with open(exe, 'w', encoding='utf-8') as fh:
            fh.write(_xT47HardFreshLiveA_STUB)
        os.chmod(exe, 0o755)
        bodyfile = os.path.join(bin_dir, 'body')
        with open(bodyfile, 'wb') as fh:
            fh.write(body or b'')
        saved = dict(os.environ)
        os.environ['PATH'] = bin_dir + os.pathsep + saved.get('PATH', '')
        os.environ['X47LIVE_BODY'] = bodyfile if body is not None else ''
        os.environ['X47LIVE_RC'] = str(rc)
        try:
            with contextlib.redirect_stdout(buf):
                code = live(lane, rev)
        finally:
            os.environ.clear()
            os.environ.update(saved)
    return code, buf.getvalue()


def _xT47HardFreshLiveA_summary(out):
    m = re.search(r'^C1_R45_LIVE: present=(\d+) absent=(\d+) ', out, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else None


def _xT47HardFreshLiveA_probe(entries, body, rc, want, want_live, want_code=0):
    """Run one fixture lane through live(); returns (ok, detail)."""
    import shutil
    d = None
    try:
        d, rev = _xT47HardFreshLiveA_lane(entries)
        code, out = _xT47HardFreshLiveA_run(d, rev, body, rc)
        got = _xT47HardFreshLiveA_summary(out)
        lines = [l for l in out.splitlines() if l.startswith('LIVE ')]
        ok = got == want and code == want_code and lines == want_live
        detail = 'summary=%s rc=%d live=%s' % (got, code, lines)
    except Exception as exc:
        ok = False
        detail = 'raised %s' % type(exc).__name__
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
    return ok, detail


def extra_T47HardFreshLiveA():
    """Cases L01-L04: the live() re-fetch rules, driven by a stub curl and a fixture lane."""
    holds = dict(id='S001', url='https://e.org/x', verdict='holds', quote=_xT47HardFreshLiveA_QUOTE)
    page = _xT47HardFreshLiveA_PAGE
    cases = [
        ('L01_live_fetch_present', [dict(holds)], page, 0, (1, 0), ['LIVE S001 present']),
        ('L02_live_fetch_error_absent', [dict(holds)], b'ignored\n', 22, (0, 1), ['LIVE S001 absent']),
        ('L03_live_non_holds_skipped', [dict(holds, verdict='drifted')], page, 0, (0, 0), []),
        ('L04_live_unreadable_target_absent', [dict(holds)], None, 0, (0, 1), ['LIVE S001 absent']),
    ]
    failed = 0
    for name, entries, body, rc, want, want_live in cases:
        ok, detail = _xT47HardFreshLiveA_probe(entries, body, rc, want, want_live)
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    return len(cases), failed
