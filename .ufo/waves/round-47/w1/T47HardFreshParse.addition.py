"""Round-47 C2 seat T47HardFreshParse: named cases for the parse_rows() cell indexes.

parse_rows() (round-46 hardened freshness counter) turns one 13-cell registry line
into ``{id: dict(id, source, scope, anchor, teaches, status, url)}`` by indexing the
`|`-split cells: id=1, source=2, scope=5, anchor=6, teaches=7, status=8, and
`url=URL_RE.search(cells[2]).group(0)`. The six cases here pin the six dimensions this
seat owns (id, source, scope, anchor, teaches, url) with ONE fixture row whose cells are
all distinguishable, so each mutant is separated by a field value and not by a crash.

Why an import-time tripwire is part of the file
-----------------------------------------------
The round-46 selftest feeds parse_rows() its first registry fixture inside selftest()
itself (the T15 block: `rows = parse_rows(...)` then `pop = sorted(population(rows))`),
i.e. BEFORE any `extra_*()` runs -- the assembler appends the extra calls only before
the tally print. Two of the mutants owned here make that pristine call site raise:

  * parse_rows:int:1 (`rid = cells[1]` -> cells[2]) keys the dict by the source cell, so
    population()'s `int(rid[1:])` raises ValueError; the run is `crashed`, and no
    `FAIL ` line would ever be printed by a case that runs later.
  * parse_rows:int:8 (`url.group(0)` -> group(1)) asks the group-less URL_RE for group 1,
    raising IndexError at the same call site; again `crashed`.

The pool counts a kill only on a named `FAIL ` line, so those two dimensions can only be
killed by a named case that runs before selftest() reaches that call site. The tripwire
below is that early case: it evaluates exactly the same behavioural fixture and the same
field comparison as extra_T47HardFreshParse(), prints nothing when every case holds, and
runs only under `--selftest`, so the pristine counter and the --lane/--check/--live modes
print no additional bytes. It never reads the counter's own source, so the neutral
mutants and CTL_E are unaffected.
"""

# Cell layout of the fixture line (index -> meaning), for the reader:
#   0 '' | 1 id | 2 source | 3 docs | 4 A | 5 scope | 6 anchor | 7 teaches |
#   8 status | 9 opened | 10 ttl | 11 p | 12 ''
_XT47TEXT = ('| S100 | srcT47 \u2014 https://e.org/t47 | docs | A | scopeT47 | anchorT47 | '
             'teachesT47 | mined | 2026-10-25 | 180d | p |\n')

# (case name, dict field, expected value, mutant address this case separates)
_XT47CASES = (
    ('R47F01_parse_rows_id_is_cell_1', 'id', 'S100', 'parse_rows:int:1'),
    ('R47F02_parse_rows_source_is_cell_2', 'source', 'srcT47 \u2014 https://e.org/t47',
     'parse_rows:int:3'),
    ('R47F03_parse_rows_scope_is_cell_5', 'scope', 'scopeT47', 'parse_rows:int:4'),
    ('R47F04_parse_rows_anchor_is_cell_6', 'anchor', 'anchorT47', 'parse_rows:int:5'),
    ('R47F05_parse_rows_teaches_is_cell_7', 'teaches', 'teachesT47', 'parse_rows:int:6'),
    ('R47F06_parse_rows_url_is_full_match', 'url', 'https://e.org/t47', 'parse_rows:int:8'),
)


def _xT47HardFreshParse_parse():
    """parse_rows() on the fixture line; (rows, None) or ({}, 'ExcName: message')."""
    try:
        return parse_rows(_XT47TEXT), None
    except Exception as exc:  # a mutated index that raises must still yield a named FAIL
        return {}, '%s: %s' % (type(exc).__name__, exc)


def _xT47HardFreshParse_check(field, want):
    """(ok, detail) for one field of the S100 row; a different key or a raise is a miss."""
    rows, err = _xT47HardFreshParse_parse()
    if err:
        return False, 'raised %s' % err
    row = rows.get('S100')
    if row is None:
        return False, 'keys=%s' % sorted(rows)
    got = row.get(field)
    return got == want, '%s=%r' % (field, got)


def _xT47HardFreshParse_run():
    """Yield (case name, ok, detail, mutant address) for every case."""
    for name, field, want, mid in _XT47CASES:
        ok, detail = _xT47HardFreshParse_check(field, want)
        yield name, ok, detail, mid


def _xT47HardFreshParse_tripwire():
    """Pre-selftest named case for the two mutants whose crash precedes every extra_*()."""
    if '--selftest' not in sys.argv:
        return 0
    bad = 0
    for name, ok, detail, mid in _xT47HardFreshParse_run():
        if not ok:
            bad += 1
            print('FAIL %s early %s (%s)' % (name, detail, mid))
    return bad


_XT47EARLY = _xT47HardFreshParse_tripwire()


def extra_T47HardFreshParse():
    """Return (cases, failed): one field-pinning case per parse_rows cell index."""
    cases = failed = 0
    for name, ok, detail, mid in _xT47HardFreshParse_run():
        cases += 1
        failed += not ok
        print('%s %s %s (%s)' % ('PASS' if ok else 'FAIL', name, detail, mid))
    return cases, failed
