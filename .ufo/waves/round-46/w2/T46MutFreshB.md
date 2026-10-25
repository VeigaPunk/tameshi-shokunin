seat: T46MutFreshB
item: generalization attack on the hardened freshness counter `.ufo/evidence/round-46/hardening/freshness-counter.py` (content rev `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`) with 18 NEW single-replacement mutants outside the declared F01-F15 manifest; 16 survivors, each classified and — where a real gap — paired with a run-verified killing case.

# Axes (godspeed)

1. **Coverage of undeclared rules** (primary): selftest kills the *declared* survivors; do rules nobody declared still mutate freely?
2. **Soundness of classification**: every survivor argued equivalent / dead-code / real gap; every claimed gap proven by a case that passes on pristine and fails on the mutant (not just asserted).
3. **Cost**: one driver + one kill-case harness, ~30 s total; all scratch under `/tmp/tameshi-r46-T46MutFreshB/`.

# Method

- Read `.ufo/evidence/round-46/contract.json` and `.ufo/waves/round-46/w1/HardMeasure.md` first; read `.ufo/evidence/round-46/hardening/mutants.json` (freshness group = F01-F15 + neutrals FN1-FN3) so no new mutant duplicates a declared replacement.
- Lane file untouched; worked on the copy `/tmp/tameshi-r46-T46MutFreshB/h.py`, sha256 `f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507`, byte-identical to the lane file (verified before and after all runs).
- Baseline: `python3 /tmp/tameshi-r46-T46MutFreshB/h.py --selftest` → exit=0, `C1_R45_SELFTEST: cases=34 failed=0`, `VERDICT: PASS`.
- Mutant detector (same for all): apply exactly one `old -> new` replacement (driver asserts `old` occurs exactly once and `ast.parse` accepts the result), write `mut_<id>.py`, run `python3 /tmp/tameshi-r46-T46MutFreshB/mut_<id>.py --selftest`. `VERDICT: PASS` = the mutant survives the selftest.

# Mutant matrix (18 new probes)

Line numbers are `.ufo/evidence/round-46/hardening/freshness-counter.py` lines (identical in the copy).

| id | file:line | old -> new | result |
|----|-----------|------------|--------|
| G01 | :85 | `if len(cells) != 13:` -> `if len(cells) < 13:` | SURVIVES |
| G02 | :63 | `r'^ {0,3}\|\s*(S\d{3,})\s*\|'` -> `r'^ {0,2}\|\s*(S\d{3,})\s*\|'` | SURVIVES |
| G03 | :187 | `else data` -> `else []` (wave_seats list-input branch) | SURVIVES |
| G04 | :187 | `data.get('results', [])` -> `data['results']` (same line) | SURVIVES |
| G05 | :209 | `r'\b%s\b' % re.escape(rid)` -> `r'%s' % re.escape(rid)` | SURVIVES |
| G06 | :287 | `name = name[:-3] if name.endswith('.gz') else name` -> `... if False else name` | SURVIVES |
| G07 | :288 | `full = os.path.join(snapdir, name)` -> `full = name` | SURVIVES |
| G08 | :297 | `return 0 if state in ('verified', 'drifted', 'unreachable') else 1` -> `return 0 if state == 'verified' else 1` | SURVIVES |
| G09 | :321 | live(): `return 0` -> `return 1` (after the `C1_R45_LIVE` print) | SURVIVES |
| G10 | :265 | `len(states['drifted']),` -> `0,` (measure print) | SURVIVES |
| G11 | :266 | `len(states['unreachable']),` -> `0,` (measure print) | SURVIVES |
| G12 | :255 | `score = ... if pop else 0` -> `... if pop else 1` | SURVIVES |
| G13 | :255 | `score = ... if pop else 0` -> `... if fresh else 0` | SURVIVES (equivalent) |
| G14 | :60 | `TARGET = 50` -> `TARGET = 40` | **KILLED** (`FAIL F12_target_50_floor target=40 want=50`) |
| G15 | :62 | `MIN_OPENED = '2026-10-25'` -> `MIN_OPENED = '2026-10-24'` | SURVIVES |
| G16 | :204 | `or who not in seats:` -> `or who not in str(seats):` | SURVIVES |
| G17 | :253 | `unreviewed = verified - agreed - disputed` -> `unreviewed = verified - disputed` | SURVIVES |
| G18 | :61 | `MAX_ID = 160` -> `MAX_ID = 161` | **KILLED** (`FAIL T15_population_bounds got=['S001', 'S161']`) |

All 16 survivors printed `C1_R45_SELFTEST: cases=34 failed=0` / `VERDICT: PASS` (exit 0). Every survivor was then subjected to a candidate killing case; the case ran against pristine **and** the mutant (`killcases.py`):

```
G01 pristine=PASS mutant=FAIL -> KILLS GAP   (same line for G02..G17)
G13: equivalence sweep 0/6 fixtures differ (n=0..5)
G14/G18: killed by the existing selftest, no case needed
```

G14/G18 are deliberate killed-controls: they show the harness reports kills when kills exist and that the `TARGET`/`MAX_ID` constants are already pinned (by `F12_target_50_floor`'s printed `target=` field and `T15_population_bounds` respectively).

# Survivor classification and killing cases

Severity is relative to the freshness counter's role as the round-45 C1 measurement (predicate `fresh >= 50`): HIGH = the mutant moves the predicate, LOW = it moves only helper/diagnostic behavior, INFO = no gap.

## G01 — HIGH — real gap (parse_rows 13-cell rule)

`< 13` admits 14-cell rows (a literal `|` inside a later cell), where `cells[8]` still lands on status, so a malformed row enters the population and can be graded verified+agreed — inflating `fresh`. No selftest fixture has more than 13 cells. Killing case (run-verified):

```python
text = ('| S050 | a \u2014 https://e.org/p | docs | A | s | a | t | mined '
        '| 2026-10-25 | 180d | p | q |\n')          # 14 pipe-split cells
assert sorted(population(parse_rows(text))) == []  # pristine: [] ; G01: ['S050']
```

## G02 — HIGH — real gap (0-3-space rule, upper bound)

`T15` pins the 4-space side (a 4-space row must be refused) but nothing pins the 3-space side, so `^ {0,2}` silently drops legal 3-space-indented rows from the population. Killing case:

```python
text = ('   | S070 | a \u2014 https://e.org/z | docs | A | s | a | t | mined '
        '| 2026-10-25 | 180d | p |\n')              # exactly 3 leading spaces
assert sorted(population(parse_rows(text))) == ['S070']  # G02: []
```

## G03 — LOW — real gap (wave_seats top-level list input)

The orchestrator writing a bare JSON list (not `{"results": [...]}`) must still yield its seat names; the mutant returns an empty seat set, silently refusing every review (fresh shrinks — false-negative direction only). Killing case:

```python
assert wave_seats('[{"name": "RevL", "output": "done"}]') == {'RevL'}  # G03: set()
```

## G04 — LOW — real gap (wave_seats dict without 'results')

A dict without `results` must give `set()`; the mutant raises `KeyError` (measure would crash instead of degrading). Killing case:

```python
assert wave_seats('{}') == set()   # G04: KeyError
```

## G05 — HIGH — real gap (report-names-id regex `\b`)

Without word boundaries a report naming only `S0010` admits a review for `S001` (substring match), inflating `agreed`/`fresh` — a false-PASS path into the predicate. `T17`'s report lists ids space-separated, so the boundary is never load-bearing. Killing case:

```python
rep = '.ufo/waves/round-45/w2/R.md'
agreed, _ = review_sets({'S001'},
    [{'id': 'S001', 'reviewer': 'RevX', 'verdict': 'agree', 'report': rep}],
    {'S001': 'ExecA'}, {rep: 'RevX re-checked S0010 and agrees'}.get, {'RevX'})
assert agreed == set()             # pristine: set() ; G05: {'S001'}
```

## G06 — LOW — real gap (check() snapdir `.gz` strip)

`check()`/`live()` are never invoked by the selftest (all 34 cases exercise `grade`/`population`/`review_sets`/`measure` only). With the strip disabled, a `.gz`-suffixed snapshot path misses the snapdir file and every such fragment is misreported `invalid 'snapshot absent'`. Killing case (fixture repo with row `S080`, fragment `snapshot='snap/page.txt.gz'`, snapdir holding uncompressed `page.txt`):

```
python3 <variant> --lane FIX --rev m --check frag_holds.json --snapdir SNAPDIR
pristine: exit 0, "CHECK S080 verified ok"   ; G06: exit 1, "CHECK S080 invalid snapshot absent"
```

## G07 — LOW — real gap (check() snapdir join dropped)

Same fixture as G06; with `full = name` the read is CWD-dependent, so a correct snapdir invocation fails when run from anywhere else. Observed identical separation: pristine `verified ok` / exit 0, mutant `snapshot absent` / exit 1.

## G08 — LOW — real gap (check() exit code for drifted/unreachable)

The helper's contract is exit 0 for `verified|drifted|unreachable`; narrowing to `verified` makes a correct `--check` on a drifted fragment exit 1. Killing case: same fixture with `verdict='drifted'` (sha ok) → pristine exit 0 / `CHECK S080 drifted ok`; mutant exit 1.

## G09 — LOW — real selftest gap, weak contract (live() exit code)

`--live` is documented "informational, outside the predicate", so exit 0 even with absents is the only sane reading — but the selftest never executes `live()` at all (killing case run-verified by monkeypatching the module's `subprocess.run` so `curl` writes a page containing the quote; pristine returns 0, G09 returns 1). If the lane considers `live()` out of the falsifiable surface, reclassify this one dead-code/INFO.

## G10 — LOW — real gap (measure() drifted accounting)

No measure-level fixture contains a drifted entry, so the printed `drifted=` field is unpinned (`HardMeasure` asserts only fields that are 0 or in the predicate). Killing case (1-row measure fixture, entry `verdict='drifted'` with correct sha):

```python
fields = measure_fields(variant, fix)          # parse C1_R45: line
assert fields['drifted'] == '1'                # G10 prints drifted=0
```

## G11 — LOW — real gap (measure() unreachable accounting)

Same shape; entry `verdict='unreachable'`, `evidence` non-empty → `assert fields['unreachable'] == '1'` (G11 prints 0). Run-verified.

## G12 — LOW — real gap (score formula, pop=0 branch)

An empty registry must print `score=0`; the mutant prints `score=1`. Killing case: measure fixture with empty `corpus/SOURCES.md` and empty ledger → `assert fields['population'] == '0' and fields['score'] == '0'` (G12: score=1). Run-verified.

## G13 — INFO — EQUIVALENT mutant (score guard `pop` vs `fresh`)

Argument: `agreed ⊆ verified ⊆ pop`, so `pop == ∅ ⇒ fresh == 0`; conversely `fresh > 0 ⇒ pop ≠ ∅`. Both guards therefore select the same branch on every input, and when `fresh == 0` the division `(10*0)//len(pop) == 0` equals the `else 0`. Sweep evidence: for n = 0..5 row fixtures (including the pop=0 fixture) the full `C1_R45:` line and exit code of pristine and mutant are identical — `0/6 fixtures differ`. No killing case exists; not a gap.

## G15 — HIGH — real gap (MIN_OPENED constant)

Loosening the constant by one day admits entries `opened 2026-10-24` as verified; `T7_old_opened` only probes `2026-10-19`, and every good fixture uses exactly `2026-10-25`, so the boundary `2026-10-24` is unpinned. Killing case:

```python
e = dict(id='S080', url=row['url'], opened='2026-10-24', verdict='holds',
         raw_sha256=sha(PAGE), quote=QUOTE)
assert grade(e, row, PAGE) == ('invalid', 'opened before round')  # G15: ('verified', 'ok')
```

## G16 — HIGH — real gap (seat membership via str())

`who not in str(seats)` is substring membership over the set's repr: reviewer `evX` passes because `'evX' in "{'RevX'}"`. A near-miss reviewer name can inject an agree that inflates `fresh` — false-PASS path. Killing case:

```python
rep = '.ufo/waves/round-45/w2/R.md'
agreed, _ = review_sets({'S009'},
    [{'id': 'S009', 'reviewer': 'evX', 'verdict': 'agree', 'report': rep}],
    {'S009': 'ExecB'}, {rep: 'evX re-checked S009 and agrees'}.get, {'RevX'})
assert agreed == set()             # pristine: set() ; G16: {'S009'}
```

## G17 — LOW — real gap (measure() unreviewed accounting)

Separating input is a verified row **with** an admitted agree (not a no-review row, where both variants print 1): pristine `unreviewed=0`, mutant `unreviewed=1`. Diagnostic field only, not in the predicate. Killing case: 1-row fixture + RevX agree → `assert fields['unreviewed'] == '0'`. Run-verified.

# Findings summary

- **No BLOCKING finding.** The declared C2 surface is untouched: all 25 declared survivors / 6 neutrals behave as the w1 receipts say, the 34-case selftest passes pristine, and TARGET/MAX_ID are demonstrably pinned (G14/G18 controls killed).
- **16/18 new mutants survive** the hardened selftest; 15 are real gaps (run-verified killing cases above), 1 (G13) is equivalent. The gaps cluster exactly where the w1 additions did not look: `parse_rows` cell/indent rules, the `\b` and set-membership semantics of review admission, the `MIN_OPENED` boundary, measure()'s non-predicate fields (`drifted`/`unreachable`/`unreviewed`/score edge), and the two helper paths `check()`/`live()` that no selftest case executes.
- The five HIGH gaps (G01, G02, G05, G15, G16) share one property: each can move `fresh` **upward** on a malformed input, i.e. they are false-PASS vectors for the round-45 freshness predicate if that rule ever regresses.
- Recommended (not applied — read-only seat): fold the 15 killing cases into the selftest as `extra_*` additions; they cost ~2 s (the `check`/`live`/`measure` ones reuse the HardMeasure scratch-repo pattern).

# Restoration evidence

- The lane file was never written; all mutants and fixtures live in `/tmp/tameshi-r46-T46MutFreshB/` (harness: `run_mutants.py`, `killcases.py`; variants `mut_G01.py`–`mut_G18.py`).
- `sha256sum` before any run: h.py = lane = `f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507`. After all runs, identical for both files (command and output above).
- Pristine selftest re-run after everything: exit=0, `C1_R45_SELFTEST: cases=34 failed=0`, `VERDICT: PASS`.
- Mutant variant hashes (sha256, first 12 hex; full digests in the transcript above and in `/tmp/tameshi-r46-T46MutFreshB/`): G01 `01a385165aa1`, G02 `ed2c712f4bb9`, G03 `cc0fbc6d21db`, G04 `7f70ecbe8009`, G05 `3ed4f4a440b3`, G06 `c7c6ac22022c`, G07 `a90ddfe82d79`, G08 `ea1f44956029`, G09 `dc3cb975f9bd`, G10 `e564393fe20c`, G11 `4ac3b02dc20c`, G12 `341a140d5b7c`, G13 `9432d13c5911`, G14 `5a7c2ab9cc1e`, G15 `e0705de64ed7`, G16 `e32d1e283cdc`, G17 `674e5533ec3e`, G18 `a49364df8507`. Each variant differs from `h.py` by exactly the one `old -> new` line listed in the matrix.

# Bounds, tooling, unrun

- No git/jj state-touching command was run anywhere in the lane; fixture repos were created with `git -C "$D" init -q` (toplevel asserted equal to `$D`) and committed only with the throwaway identity `-c user.name=t -c user.email=t@t` inside those scratch repos, with `GIT_CONFIG_GLOBAL=GIT_CONFIG_SYSTEM=/dev/null`.
- No tools installed or upgraded; no pacman.
- Unrun (not mine): the L1's deciding runs of all three counters; the C2 `mutate.py --targets hardened` verdict; counter runs against `--rev 6f2168e0…` in this seat were the selftest-internal fixtures only (the seat's own detectors were `--selftest` runs and scratch-repo `--lane/--rev m` invocations, never a lane verdict).
