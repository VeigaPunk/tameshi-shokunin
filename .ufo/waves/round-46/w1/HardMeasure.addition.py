"""Round-46 C2 seat HardMeasure: measure()-level cases for the round-45 freshness counter.

Four cases, each the smallest scratch-repo fixture that separates the pristine
counter from one declared mutant of mutants.json group `freshness`:

  F05_duplicate_entry_refused  two ledger entries for one population row: the
                               counter must print invalid=2 verified=0, not
                               grade the id twice (invalid=0 verified=1).
  F10_dispute_sinks_agree      one verified row with an agree and a dispute:
                               fresh/score must stay 0, not count the agree.
  F11_self_pin_gates_pass      50 verified+agreed rows with no counter bytes at
                               SELF_PATH (self_pin=0): PASS must stay false.
  F12_target_50_floor          one verified+agreed row with the counter bytes
                               pinned (self_pin=1): fresh=1 < 50, PASS false.

Every case runs the counter CLI as a subprocess in a scratch git repo
(`git init -q -b m`, toplevel asserted equal to the scratch dir, one commit
with `-c user.name=t -c user.email=t@t`, GIT_CONFIG_GLOBAL/SYSTEM=/dev/null)
and reads the counter's printed C1_R45 summary fields plus its exit code.
No case asserts on the counter's source bytes; the F11 fixture simply leaves
SELF_PATH uncommitted, which is the observable self_pin=0 input state.
"""


def _xHardMeasure_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_CONFIG_GLOBAL'] = '/dev/null'
    env['GIT_CONFIG_SYSTEM'] = '/dev/null'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def _xHardMeasure_git(d, *args):
    out = subprocess.run(['git', '-C', d, '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                         capture_output=True, env=_xHardMeasure_env())
    if out.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (' '.join(args),
                                                  out.stderr.decode('utf-8', 'replace').strip()))
    return out.stdout.decode('utf-8', 'replace')


def _xHardMeasure_build(d, files, pin_self):
    d = os.path.realpath(d)
    _xHardMeasure_git(d, 'init', '-q', '-b', 'm')
    top = _xHardMeasure_git(d, 'rev-parse', '--show-toplevel').strip()
    if os.path.realpath(top) != d:
        raise RuntimeError('repo toplevel %r != scratch dir %r' % (top, d))
    for rel, data in files.items():
        full = os.path.join(d, rel)
        if os.path.dirname(full):
            os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data.encode('utf-8') if isinstance(data, str) else data)
    if pin_self:
        full = os.path.join(d, SELF_PATH)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(open(os.path.abspath(__file__), 'rb').read())
    _xHardMeasure_git(d, 'add', '-A')
    _xHardMeasure_git(d, 'commit', '-q', '-m', 'fixture')
    return d


def _xHardMeasure_run(d):
    try:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                           capture_output=True, text=True, timeout=180, env=_xHardMeasure_env())
    except subprocess.TimeoutExpired:
        return 'timeout', '', 'timeout'
    return p.returncode, p.stdout, p.stderr


def _xHardMeasure_fields(out):
    m = re.search(r'^C1_R45: (.*)$', out, re.M)
    return dict(re.findall(r'(\w+)=(\S+)', m.group(1))) if m else {}


def _xHardMeasure_snapshot(n):
    return ''.join('q%03d marker%03d mutants detected valid alpha%03d\n' % (i, i, i)
                   for i in range(1, n + 1))


def _xHardMeasure_row(i):
    # 11 pipe cells: id | source | docs | A | scope | anchor | teaches | status | opened | ttl | x
    return ('| S%03d | doc%d \u2014 https://e.org/x%03d | docs | A | mutants detected | alpha%03d '
            '| valid | mined | 2026-10-25 | 180d | p |\n' % (i, i, i, i))


def _xHardMeasure_entry(i, sha):
    return dict(id='S%03d' % i, url='https://e.org/x%03d' % i, author='ExecA',
                opened='2026-10-25', verdict='holds', raw_sha256=sha, snapshot='snap/page.txt',
                quote='q%03d marker%03d mutants detected valid alpha%03d' % (i, i, i))


def _xHardMeasure_sha(n):
    return hashlib.sha256(_xHardMeasure_snapshot(n).encode('utf-8')).hexdigest()


def _xHardMeasure_fixture(n, entries, reviews):
    snap = _xHardMeasure_snapshot(n)
    files = {
        'corpus/SOURCES.md': ''.join(_xHardMeasure_row(i) for i in range(1, n + 1)),
        'snap/page.txt': snap,
        '.ufo/evidence/round-45/freshness/ledger.json': json.dumps({'entries': entries}),
        '.ufo/evidence/round-45/freshness/reviews.json': json.dumps({'reviews': reviews}),
        '.ufo/waves/round-45/w2-results.json': json.dumps(
            {'results': [{'name': 'RevX', 'output': 'done'}, {'name': 'RevY', 'output': 'done'}]}),
        '.ufo/waves/round-45/w2/Rev.md': 'RevX RevY ' + ' '.join(
            'S%03d' % i for i in range(1, n + 1)) + '\n',
    }
    return files, hashlib.sha256(snap.encode('utf-8')).hexdigest()


def _xHardMeasure_review(rid, who, verdict):
    return dict(id=rid, reviewer=who, verdict=verdict,
                report='.ufo/waves/round-45/w2/Rev.md', reason='fixture')


def _xHardMeasure_case(name, files, pin_self, want, want_rc):
    """Run one fixture; `want` maps C1_R45 summary field -> expected value."""
    try:
        with tempfile.TemporaryDirectory(prefix='tameshi-r46-hardmeasure-') as d:
            _xHardMeasure_build(d, files, pin_self)
            rc, out, err = _xHardMeasure_run(d)
    except Exception as exc:
        print('FAIL %s harness error: %s' % (name, exc))
        return 0
    fields = _xHardMeasure_fields(out)
    bad = []
    if rc != want_rc:
        bad.append('exit=%s want=%s' % (rc, want_rc))
    for key, val in want.items():
        if fields.get(key) != val:
            bad.append('%s=%s want=%s' % (key, fields.get(key), val))
    if bad:
        print('FAIL %s %s%s' % (name, ' '.join(bad), (' stderr=' + err.strip().splitlines()[-1]) if err.strip() else ''))
        return 0
    print('PASS %s' % name)
    return 1


def extra_HardMeasure():
    cases = failed = 0

    # F05: a second ledger entry for the same population row must be refused as
    # invalid (both copies), not graded twice into verified.
    e1 = _xHardMeasure_entry(1, _xHardMeasure_sha(1))
    files, _ = _xHardMeasure_fixture(1, [e1, dict(e1)], [])
    cases += 1
    failed += not _xHardMeasure_case('F05_duplicate_entry_refused', files, False,
                                     {'population': '1', 'entries': '2',
                                      'verified': '0', 'invalid': '2', 'fresh': '0',
                                      'C1_R45_PASS': 'false'}, 1)

    # F10: a dispute review on a verified id must sink its agree review.
    files, _ = _xHardMeasure_fixture(1, [_xHardMeasure_entry(1, _xHardMeasure_sha(1))],
                                     [_xHardMeasure_review('S001', 'RevX', 'agree'),
                                      _xHardMeasure_review('S001', 'RevY', 'dispute')])
    cases += 1
    failed += not _xHardMeasure_case('F10_dispute_sinks_agree', files, False,
                                     {'verified': '1', 'disputed': '1',
                                      'fresh': '0', 'score': '0', 'C1_R45_PASS': 'false'}, 1)

    # F11: with self_pin=0 the predicate must stay false even at fresh >= TARGET (50).
    n = TARGET
    files, _ = _xHardMeasure_fixture(
        n, [_xHardMeasure_entry(i, _xHardMeasure_sha(n)) for i in range(1, n + 1)],
        [_xHardMeasure_review('S%03d' % i, 'RevX', 'agree') for i in range(1, n + 1)])
    cases += 1
    failed += not _xHardMeasure_case('F11_self_pin_gates_pass', files, False,
                                     {'self_pin': '0', 'population': str(n), 'verified': str(n),
                                      'fresh': str(n), 'target': str(n),
                                      'C1_R45_PASS': 'false'}, 1)

    # F12: TARGET is a floor; fresh=1 with self_pin=1 must not pass.
    files, _ = _xHardMeasure_fixture(1, [_xHardMeasure_entry(1, _xHardMeasure_sha(1))],
                                     [_xHardMeasure_review('S001', 'RevX', 'agree')])
    cases += 1
    failed += not _xHardMeasure_case('F12_target_50_floor', files, True,
                                     {'self_pin': '1', 'verified': '1', 'fresh': '1',
                                      'score': '10', 'target': '50', 'C1_R45_PASS': 'false'}, 1)

    return cases, failed
