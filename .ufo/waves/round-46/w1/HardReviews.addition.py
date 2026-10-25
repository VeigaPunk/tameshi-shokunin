def _xHardReviews_seats(*names):
    """Seats with non-empty output, as the orchestrator would write them."""
    return wave_seats(json.dumps({'results': [{'name': n, 'output': 'done'} for n in names]}))


def _xHardReviews_run(verified, reviews, authors, reports, seats):
    agreed, disputed = review_sets(verified, reviews, authors, reports.get, seats)
    return sorted(agreed), sorted(disputed)


def extra_HardReviews():
    """Cases F06/F07/F08/F09/F13: the review-admission gates of review_sets()/wave_seats().

    Each case pairs one review that must be refused with one independent agree that
    must be admitted, so a gate that silently stops counting anything fails too.
    """
    rep = '.ufo/waves/round-45/w2/R.md'
    ctl = '.ufo/waves/round-45/w2/C.md'
    cases = []

    # F06: a review whose reviewer IS the entry's author, with a report naming both
    # reviewer and id, must still be refused (self-review).
    reports = {rep: 'RevA re-checked S001 and agrees', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevA', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevA', 'verdict': 'agree', 'report': rep},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'RevA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F06_review_non_author', got == (['S002'], []), got))

    # F07: a seat whose output is only whitespace is not a seat.
    seats = wave_seats(json.dumps({'results': [
        {'name': 'RevW', 'output': ' \n\t '}, {'name': 'RevOK', 'output': 'done'}]}))
    cases.append(('F07_seat_output_nonempty', seats == {'RevOK'}, sorted(seats)))

    # F08: a readable report outside .ufo/waves/round-45/ does not admit a review.
    outside = '.ufo/waves/round-44/w1/R.md'
    reports = {outside: 'RevB re-checked S001 and agrees', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevB', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevB', 'verdict': 'agree', 'report': outside},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'ExecA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F08_report_outside_prefix', got == (['S002'], []), got))

    # F09: a report naming the id but not the reviewer does not admit a review.
    reports = {rep: 'S001 was re-checked against the ledger', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevC', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevC', 'verdict': 'agree', 'report': rep},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'ExecA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F09_report_names_reviewer', got == (['S002'], []), got))

    # F13: a verdict that is neither agree nor dispute admits nothing.
    reports = {rep: 'RevD re-checked S001 and is unsure', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevD', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevD', 'verdict': 'unsure', 'report': rep},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'ExecA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F13_verdict_only_agree', got == (['S002'], []), got))

    failed = 0
    for name, ok, got in cases:
        failed += not ok
        print('%s %s got=%r' % ('PASS' if ok else 'FAIL', name, got))
    return len(cases), failed
