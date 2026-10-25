# HardGrade (tameshi round 46, wave 1): grade() rules F01, F02, F03.
# Each case is the smallest fixture that separates the pristine grade() rule
# from its declared mutant in .ufo/evidence/round-46/hardening/mutants.json:
#   F01 snapshot-absent reason  - a valid `drifted` entry whose snapshot is
#       absent must be refused as invalid 'snapshot absent'; with raw_sha256 of
#       the empty byte string the mutant (raw = b'') falls through the hash
#       check into the drifted return and states 'drifted'.
#   F02 quote upper bound 25    - a 26-token quote that IS present in the
#       snapshot, overlaps the row and is not copied from it is refused.
#   F03 quote presence          - a 6..25-token quote with real row overlap that
#       does NOT occur in the snapshot is refused, with no other rule masking it.


def _xHardGrade_row():
    return dict(id='S001', url='https://example.org/a', scope='flaky failure reports',
                anchor='section Metrics', teaches='flaky failures cluster in the same job',
                status='mined', source='x — https://example.org/a')


def _xHardGrade_page():
    return (b'<html><body><p>Flaky failures cluster inside the same job because the rerun '
            b'repeats one order of the tests only and the second attempt hides the ordering '
            b'defect entirely from the report.</p></body></html>')


def _xHardGrade_quote26():
    # 26 whitespace tokens, verbatim inside _xHardGrade_page().
    return ('Flaky failures cluster inside the same job because the rerun repeats one order of '
            'the tests only and the second attempt hides the ordering defect entirely')


def _xHardGrade_quote10_absent():
    # 10 whitespace tokens, shares 4 content words with the row, absent from the page.
    return 'Flaky failures never appear when the same job reruns alone'


def extra_HardGrade():
    row = _xHardGrade_row()
    page = _xHardGrade_page()
    sha = hashlib.sha256(page).hexdigest()
    good = dict(id='S001', url=row['url'], opened='2026-10-25', verdict='holds',
                raw_sha256=sha, quote=_xHardGrade_quote26())
    empty_sha = hashlib.sha256(b'').hexdigest()
    cases = [
        ('F01_snapshot_absent_reason',
         dict(good, verdict='drifted', raw_sha256=empty_sha), None,
         ('invalid', 'snapshot absent')),
        ('F02_quote_upper_bound_25', good, page, ('invalid', 'quote length 26')),
        ('F03_quote_absent_from_snapshot',
         dict(good, quote=_xHardGrade_quote10_absent()), page,
         ('invalid', 'quote absent')),
    ]
    failed = 0
    for name, entry, raw, want in cases:
        got = grade(entry, row, raw)
        ok = got == want
        failed += not ok
        print('%s %s got=%s want=%s' % ('PASS' if ok else 'FAIL', name, got, want))
    return len(cases), failed
