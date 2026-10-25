# --- HardPopulation: selftest cases for the three population() survivors F04, F14, F15.
# The round-45 selftest T15 pins only three dimensions of population(): the id above
# MAX_ID (S161), a non-`mined` status that happens to be `queued`, and a row that is
# not indented as a registry row at all. The three cases below pin the remaining
# dimensions, each as the smallest fixture that separates the pristine rule from one
# declared mutant: a control row S100 (URL present, status mined, id <= MAX_ID, so every
# variant includes it) plus exactly one probe row that differs from that control in the
# single dimension under test. No case reads the counter's own bytes.


def _xHardPopulation_row(rid, source, status):
    """One registry line with the 13 pipe-split cells parse_rows() requires."""
    return '| %s | %s | docs | A | s | a | t | %s | 2026-10-19 | 180d | p |\n' % (rid, source, status)


def _xHardPopulation_ids(probe_id, probe_source, probe_status):
    """Sorted population ids of the S100 control row plus one probe row."""
    text = (_xHardPopulation_row('S100', 'a — https://e.org/control', 'mined')
            + _xHardPopulation_row(probe_id, probe_source, probe_status))
    return sorted(population(parse_rows(text)))


def extra_HardPopulation():
    """Return (cases, failed): F04 needs a URL, F14 needs status exactly `mined`,
    F15 needs the MAX_ID bound to be inclusive."""
    cases = failed = 0
    probes = [
        # mutant id, case name, probe id, probe source cell, probe status, expected ids
        ('F04', 'F04_population_requires_url',
         'S101', 'a — this cell carries no link', 'mined', ['S100']),
        ('F14', 'F14_population_status_exactly_mined',
         'S101', 'a — https://e.org/rejected', 'rejected', ['S100']),
        ('F15', 'F15_population_id_bound_inclusive',
         'S%03d' % MAX_ID, 'a — https://e.org/boundary', 'mined',
         sorted(['S100', 'S%03d' % MAX_ID])),
    ]
    for mid, name, pid, src, status, want in probes:
        got = _xHardPopulation_ids(pid, src, status)
        ok = got == want
        cases += 1
        failed += not ok
        print('%s %s got=%s want=%s (%s)' % ('PASS' if ok else 'FAIL', name, got, want, mid))
    return cases, failed
