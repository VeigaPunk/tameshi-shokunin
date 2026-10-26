"""Round-47 C2 seat T47HardFreshMeasure: measure()-level cases for the round-45 freshness counter.

Three cases, each the smallest scratch-repo fixture that separates the pristine
measure() from one declared round-47 pool mutant of group `freshness`:

  F20_invalid_reason_routing   measure:cmp:2   `if state == 'invalid':` -> `!=`
      One population row with a verified entry (S001) and one with a mismatched
      URL (S002, `url mismatch`).  The reason loop must name exactly S002 on an
      `INVALID` line.  With the operator flipped the loop appends a reason for
      the verified row instead ('S001 ok') and drops the genuine invalid reason,
      so the printed INVALID id set becomes ['S001'].

  F21_empty_population_score   measure:int:0   the `else 0` of the score formula -> 1
      SOURCES.md with no population rows and an empty ledger: the summary must
      report score=0.  With the mutated constant the empty-population branch
      reports score=1.

  F22_target_equality_passes   measure:cmp:4   (`fresh >= TARGET` -> `>`)
                               measure:int:5   (`self_pin == 1` -> `self_pin == 2`)
                               measure:int:1   (`return 0 if passed else 1` -> always 1)
      TARGET valid+agreed rows with the counter bytes pinned at SELF_PATH, so
      fresh equals TARGET exactly: the declared floor must admit that boundary
      (PASS, exit 0), the self pin must read 1, and a passing measurement must
      exit 0.

Every case reuses the round-46 HardMeasure scratch-repo builders read-only and
prints `PASS <case> ...` / `FAIL <case> ...`; no case reads or pins the
counter's source bytes, and none of them fails for a behaviour-equal neutral
(commute) mutant.
"""


def _xT47HardFreshMeasure_invalid_ids(out):
    return sorted(set(re.findall(r'^INVALID (\S+)', out, re.M)))


def _xT47HardFreshMeasure_case(name, files, pin_self, want, want_rc, invalid_ids):
    """Run one fixture; check summary fields, exit code and the INVALID id set."""
    try:
        with tempfile.TemporaryDirectory(prefix='tameshi-r47-hardfresh-') as d:
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
    if invalid_ids is not None:
        got = _xT47HardFreshMeasure_invalid_ids(out)
        if got != list(invalid_ids):
            bad.append('INVALID ids=%s want=%s' % (got, list(invalid_ids)))
    if bad:
        tail = (' stderr=' + err.strip().splitlines()[-1]) if err.strip() else ''
        print('FAIL %s %s%s' % (name, ' '.join(bad), tail))
        return 0
    print('PASS %s' % name)
    return 1


def extra_T47HardFreshMeasure():
    cases = failed = 0

    # F20: INVALID lines must be routed by the graded state, not its complement.
    sha2 = _xHardMeasure_sha(2)
    files, _ = _xHardMeasure_fixture(
        2,
        [_xHardMeasure_entry(1, sha2),
         dict(_xHardMeasure_entry(2, sha2), url='https://e.org/other')],
        [])
    cases += 1
    failed += not _xT47HardFreshMeasure_case(
        'F20_invalid_reason_routing', files, False,
        {'population': '2', 'entries': '2', 'verified': '1', 'invalid': '1',
         'fresh': '0', 'score': '0', 'C1_R45_PASS': 'false'}, 1, ['S002'])

    # F21: with no population the score formula's else branch must stay 0.
    files, _ = _xHardMeasure_fixture(0, [], [])
    cases += 1
    failed += not _xT47HardFreshMeasure_case(
        'F21_empty_population_score', files, False,
        {'population': '0', 'entries': '0', 'verified': '0', 'fresh': '0',
         'score': '0', 'C1_R45_PASS': 'false'}, 1, [])

    # F22: fresh == TARGET exactly, self_pin=1, must PASS and exit 0.
    n = TARGET
    files, _ = _xHardMeasure_fixture(
        n, [_xHardMeasure_entry(i, _xHardMeasure_sha(n)) for i in range(1, n + 1)],
        [_xHardMeasure_review('S%03d' % i, 'RevX', 'agree') for i in range(1, n + 1)])
    cases += 1
    failed += not _xT47HardFreshMeasure_case(
        'F22_target_equality_passes', files, True,
        {'self_pin': '1', 'population': str(n), 'entries': str(n), 'verified': str(n),
         'fresh': str(n), 'score': '10', 'target': str(n), 'C1_R45_PASS': 'true'}, 0, [])

    return cases, failed
