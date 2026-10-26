# T47HardCoverEntry (round 47, C2 operability): selftest additions for the round-46 hardened
# coverage counter's entry_ok() rule.  Each case feeds entry_ok() the smallest in-memory fixture
# (a rows dict plus an entry text, no git repo, no network) that makes the pristine predicate and
# one frozen pool mutant (group coverage, function entry_ok) return different values.

_xT47HardCoverEntry_PATH = 'corpus/knowledge/a.md'
_xT47HardCoverEntry_SNAP = 'Remember that the test order is undefined, so your code cannot depend on it.'
_xT47HardCoverEntry_QUOTE = 'the test order is undefined, so your code cannot depend on it'


def _xT47HardCoverEntry_entry(quote, pad=0):
    """Provenance lines (source / verified-at / recheck) with `quote` on line 3, plus `pad` blanks."""
    return '\n'.join(['source: S256 — upstream',
                      'verified-at: 2026-10-25',
                      'recheck: 365d — %s' % quote] + [''] * pad) + '\n'


def _xT47HardCoverEntry_probe(text, snapshot):
    rows = {'S256': dict(text=fold(snapshot), used={_xT47HardCoverEntry_PATH})}
    return entry_ok(_xT47HardCoverEntry_PATH, text, rows)


def extra_T47HardCoverEntry():
    tokens6 = ' '.join('t%d' % i for i in range(1, 7))
    tokens26 = ' '.join('u%d' % i for i in range(1, 27))
    plan = [
        # exactly three provenance lines: the trio minimum is `len(lines) < 3`, so 3 lines is ok
        ('T47HE_three_line_entry_ok',
         _xT47HardCoverEntry_entry('upstream says "%s"' % _xT47HardCoverEntry_QUOTE),
         _xT47HardCoverEntry_SNAP, (True, 'ok')),
        # a located quote of exactly 6 tokens sits on the lower edge of the 6..25 window
        ('T47HE_six_token_quote_ok',
         _xT47HardCoverEntry_entry('note "%s" holds' % tokens6, pad=1),
         'Upstream note: "%s" ends here.' % tokens6, (True, 'ok')),
        # a located quote of exactly 26 tokens is outside the window, so the entry is refused
        ('T47HE_twenty_six_token_quote_refused',
         _xT47HardCoverEntry_entry('note "%s" holds' % tokens26, pad=1),
         'Upstream note: "%s" ends here.' % tokens26, (False, 'no located quote')),
        # curly quotes live in group 2, the fallback arm of `q.group(1) or q.group(2)`
        ('T47HE_curly_quote_fallback_ok',
         _xT47HardCoverEntry_entry('upstream says “%s”' % _xT47HardCoverEntry_QUOTE, pad=1),
         _xT47HardCoverEntry_SNAP, (True, 'ok')),
    ]
    failed = 0
    for name, text, snapshot, want in plan:
        try:
            got = _xT47HardCoverEntry_probe(text, snapshot)
            detail = 'got=%r' % (got,)
            ok = got == want
        except Exception as exc:  # a mutant that makes the rule raise is a named failure, not a crash
            detail = 'raised %s' % type(exc).__name__
            ok = False
        failed += not ok
        print('%s %s want=%r %s' % ('PASS' if ok else 'FAIL', name, want, detail))
    return len(plan), failed
