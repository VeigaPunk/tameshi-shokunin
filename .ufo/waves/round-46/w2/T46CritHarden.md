seat: T46CritHarden
item: attacked the C2 hardening harness — can the hardened selftests report kills without testing a rule? (text-grep cases, crash/timeout kills, self-fulfilling expectations, fixture nondeterminism, wall time vs TIMEOUT)

# T46CritHarden — C2 hardened selftests: kills for the wrong reason

Scope: the two hardened counters `.ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py`, the
driver `.ufo/evidence/round-46/hardening/mutate.py` and the frozen manifest
`.ufo/evidence/round-46/hardening/mutants.json` as committed at the content revision
`6f2168e028ce7ff6e82ac92093ac05dd1f147c32`. Everything I ran was read from that revision into
`/tmp/tameshi-r46-T46CritHarden/` (`git -C LANE show 6f2168e…:<path>`); I wrote nothing in the lane except
this report. The deciding run is the L1's; nothing here is a verdict.

## Bottom line

- **No mutant of the 25 is killed by a crash or a timeout.** All 25 fail on a `FAIL` line that names the case
  built for that mutant and prints the rule's own changed value. 0/25 HIGH crash-kills.
- The shipped copies contain **no assertion on the mutated source text** (only `__file__` byte *writes* into
  the `self_pin` fixtures). But the driver cannot tell such an assertion apart from a rule test: a scratch
  copy whose only F02 test is a runtime-built source needle kills F02 while all three neutral controls survive
  and the pristine passes — the exact output the driver accepts as a legitimate kill.
- Every extra case is confined to its scratch repo except one: a mutant that makes `SELF_PATH` absolute makes
  the fixture write the running counter's bytes **outside** the temp dir (verified). Latent — the frozen
  manifest has no `SELF_PATH` mutant.
- Timing, determinism, self-fulfilling expectations: measured, no defect found that affects the shipped copy.

## Commands run (all at 6f2168e)

1. The committed driver, both groups, hardened targets:
   `python3 .ufo/evidence/round-46/hardening/mutate.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --targets hardened`
   → `rc=0`, `PRISTINE freshness pass`, `PRISTINE coverage pass`, `EQUIVALENCE freshness 1`,
   `EQUIVALENCE coverage 1`, all 15 F-mutants `killed`, all 10 C-mutants `killed`, all 6 neutrals `survived`, and
   `C2_R46: self_pin=1 targets=hardened declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 rev=6f2168e… C2_R46_PASS=true`
   (full stdout `/tmp/tameshi-r46-T46CritHarden/driver-hardened.out`; 13.24 s wall for the whole run).
2. Per-mutant probe `/tmp/tameshi-r46-T46CritHarden/matrix.py`: apply each declared replacement to the
   extracted copy, run `python3 <copy> --selftest` with cwd=temp dir, record rc, every `FAIL` line, stderr
   traceback, wall time. Output `/tmp/tameshi-r46-T46CritHarden/matrix.json`.
3. Control: the same probe against the **round-45** originals (`src/r45-{freshness,coverage}.py`) → all 25
   `survived`, all 6 neutrals `survived`, both pristines `VERDICT: PASS`. This reproduces the contract's
   before-state (`killed=0 survived=25`).
4. `diff` of the hardened copies against the round-45 originals: the base section (lines 1–324 freshness,
   1–141 coverage) differs **only** in the `SELF_PATH` repoint; everything else is appended before
   `def main():`. No hidden edit to the base cases.
5. Scratch-copy attacks `/tmp/tameshi-r46-T46CritHarden/gaming.py` (details below), each judged through the
   committed driver's own `run_selftest()` / `judge()` predicate (imported read-only from the lane).
6. Determinism: pristine selftest run under `TMPDIR` default / a symlink / a path with spaces, `TZ=Pacific/Kiritimati`,
   and `cwd=/` → identical case lines in all 5 variants, both counters (36 freshness cases, 22 coverage cases).
7. Timings: pristine freshness 0.48 s, pristine coverage 1.54 s, slowest mutant run 3.02 s (CN3), slowest
   declared-mutant run 1.99 s (C06). `TIMEOUT = 300` → ≈99× headroom on the slowest observed run.

## Per-mutant first failing case line (item requirement)

| group | mutant | kill signal | wall | first FAIL line (verbatim, truncated) |
|---|---|---|---|---|
| freshness | F01 | own-case | 0.49 s | `FAIL F01_snapshot_absent_reason got=('drifted', 'ok') want=('invalid', 'snapshot absent')` |
| freshness | F02 | own-case | 0.46 s | `FAIL F02_quote_upper_bound_25 got=('verified', 'ok') want=('invalid', 'quote length 26')` |
| freshness | F03 | own-case | 0.48 s | `FAIL F03_quote_absent_from_snapshot got=('verified', 'ok') want=('invalid', 'quote absent')` |
| freshness | F04 | own-case | 0.53 s | `FAIL F04_population_requires_url got=['S100', 'S101'] want=['S100'] (F04)` |
| freshness | F05 | own-case | 0.48 s | `FAIL F05_duplicate_entry_refused verified=1 want=0 invalid=0 want=2` |
| freshness | F06 | own-case | 0.48 s | `FAIL F06_review_non_author got=(['S001', 'S002'], [])` |
| freshness | F07 | own-case | 0.45 s | `FAIL F07_seat_output_nonempty got=['RevOK', 'RevW']` |
| freshness | F08 | own-case | 0.42 s | `FAIL F08_report_outside_prefix got=(['S001', 'S002'], [])` |
| freshness | F09 | own-case | 0.42 s | `FAIL F09_report_names_reviewer got=(['S001', 'S002'], [])` |
| freshness | F10 | own-case | 0.42 s | `FAIL F10_dispute_sinks_agree fresh=1 want=0 score=10 want=0` |
| freshness | F11 | own-case | 0.42 s | `FAIL F11_self_pin_gates_pass exit=0 want=1 C1_R45_PASS=true want=false` |
| freshness | F12 | own-case | 0.42 s | `FAIL F12_target_50_floor exit=0 want=1 C1_R45_PASS=true want=false` |
| freshness | F13 | own-case | 0.45 s | `FAIL F13_verdict_only_agree got=(['S001', 'S002'], [])` |
| freshness | F14 | own-case | 0.46 s | `FAIL F14_population_status_exactly_mined got=['S100', 'S101'] want=['S100'] (F14)` |
| freshness | F15 | own-case | 0.48 s | `FAIL F15_population_id_bound_inclusive got=['S100'] want=['S100', 'S160'] (F15)` |
| coverage | C01 | own-case | 1.49 s | `FAIL C01_github_not_googletest want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 …` |
| coverage | C02 | own-case | 1.52 s | `FAIL C02_round44_snapshot_path want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 …` |
| coverage | C03 | own-case | 1.78 s | `FAIL C03_missing_snapshot_empty_sha want='rows=0 entries=0' got=C2_R45: self_pin=1 rows=2 entries=0 indexed=0 …` |
| coverage | C04 | own-case | 1.57 s | `FAIL C04_entry_without_source_line1 want='entries=1 indexed=1' got=C2_R45: … entries=2 indexed=2 …` |
| coverage | C05 | own-case | 1.58 s | `FAIL C05_entry_without_recheck_line3 want='entries=1 indexed=1' got=C2_R45: … entries=2 indexed=2 …` |
| coverage | C06 | own-case | 1.99 s | `FAIL C06_readme_fullpath_index want=('indexed=2', 'C2_R45_PASS=true') got=… indexed=0 …` |
| coverage | C07 | own-case | 1.35 s | `FAIL C07_rows_one_fails want=('rows=1', 'C2_R45_PASS=false') got=… rows=1 … C2_R45_PASS=true` |
| coverage | C08 | own-case | 1.46 s | `FAIL C08_entries_one_fails want=('entries=1', 'C2_R45_PASS=false') got=… entries=1 … C2_R45_PASS=false` |
| coverage | C09 | own-case | 1.50 s | `FAIL C09_indexed_lt_entries_fails want=('indexed=1', 'C2_R45_PASS=false') got=… indexed=1 …` |
| coverage | C10 | own-case | 1.59 s | `FAIL C10_self_pin_zero_fails want=('self_pin=0', 'C2_R45_PASS=false') got=C2_R45: self_pin=0 …` |

Each mutant produced **exactly one** FAIL line (`n_fails=1` for all 25): no cross-kill, no cascade, no
traceback (`Traceback (most recent call last)` absent from every stderr), no timeout. Neutral mutants FN1–FN3,
CN1–CN3 all `VERDICT: PASS` (0 FAIL lines). **Mutants killed only by a traceback or a timeout: none (0/25).**

## Findings

### 1. HIGH (latent mechanism, not present in the shipped copies) — a source-text assertion is accepted as a kill

The driver's kill predicate is `returncode != 0 or 'VERDICT: PASS' not in stdout`. Nothing in it distinguishes
a case that fails because the *rule's behaviour* changed from a case that fails because the *source text* the
mutant removed is no longer in the file.

Reproduction (`gaming.py`): take the hardened freshness copy, delete the behavioural F02 case, and add one case
that greps its own file for a needle built at runtime (so the needle itself is not in the literal):

```python
needle = 'if n < 6 or n > ' + '25:'
body = open(os.path.abspath(__file__), encoding='utf-8').read()
ok = needle in body
```

Judged through the committed driver's `judge()`:
`pristine: pass VERDICT: PASS`; `F02 killed VERDICT: FAIL`; `FN1 survived`; `FN2 survived`; `FN3 survived`.
That is byte-for-byte the verdict shape the driver accepts for a legitimate kill, and the neutral controls
(`FN1` comment, `FN2` hex literal, `FN3` trailing comment) do not catch it because they do not touch that line.

Boundary of the neutral defence, measured: a **line-count pin** (`len(body.splitlines()) == 819`, fixed point so
the pristine passes) kills `FN1` (`neutral_killed>0` → the driver would refuse the round), and `FN2`/`FN3`
survive; a per-line needle kills no neutral. So the controls catch append/byte pins and cannot catch a needle
keyed on the exact text one mutant removes.

Why this is *latent* and not a defect of the artifact: I grepped both shipped copies for text assertions
(`in body`, `in src`, `read()) ==`, `SELF_PATH` assertions) — the only self-reads are
`open(os.path.abspath(__file__), 'rb').read()` at coverage-counter.py:116,171,249 and
freshness-counter.py:219,658,666, and every one of them **writes** those bytes into the `self_pin` fixture
(`put(SELF_PATH, …)` / `fh.write(...)`); none compares them to an expected string. The 25 kills are therefore
behavioural, per the table above. Smallest safe correction (for a future round, not this one): make the
manifest carry one *text-needle* mutant (a no-op behaviour change that removes a distinctive token) and require
it to survive — a neutral of the same shape as the vector would have caught it here.

### 2. LOW (latent) — the fixture is not confined to its scratch repo when `SELF_PATH` is not relative

`_xHardCover1_last_line` / `_xHardCover2_build` / the coverage base `build()` do
`put(SELF_PATH, open(os.path.abspath(__file__),'rb').read())` and `put()` is
`os.path.join(d, p)` — an absolute `p` discards `d`. Reproduced with a mutant
`SELF_PATH = '/tmp/tameshi-r46-T46CritHarden/escape-probe/OUTSIDE.py'`:
coverage `selftest=fail wrote_outside=True size=26`, freshness `selftest=fail wrote_outside=True size=38483`.
The selftest (and therefore the driver, which runs mutated copies) will write the counter's bytes to any
absolute path a mutation names — including the lane's own committed counter. The frozen manifest has no
`SELF_PATH` mutant, so C2 is not affected; the hazard exists only for future mutants. Smallest correction:
reject a `SELF_PATH` that is absolute or escapes `d` (`os.path.realpath(os.path.join(d, SELF_PATH))` must start
with `realpath(d)+os.sep`).

### 3. LOW (mechanism only) — crash kills are accepted and one of them is even reported as a case FAIL

Synthetic mutants on the hardened freshness copy, judged with the driver's `run_selftest()`:

| scratch mutation | result | tail |
|---|---|---|
| `MAX_ID = 160` → `MAX_ID = 160 +` (SyntaxError at import) | killed | `''` (no output at all) |
| `MIN_OPENED = '2026-10-25'` → `MIN_OPENED = 1 / 0` | killed | `''` |
| `if n < 6 or n > 25:` → `if n < 6 or n > int('x'):` (rule line raises) | killed | `''` |
| `TARGET = 50` → `TARGET = '50'` | killed | `FAIL F10_dispute_sinks_agree verified=None want=1 … stderr=TypeError: %d format: a real number is required, not str` |

The last row is the worst shape: the mutated counter crashes inside the F10 fixture and the selftest reports it
as a FAIL of **F10**, a case that has nothing to do with the mutation. None of the 25 declared mutants behaves
this way (finding 0/25 above), so C2 is unaffected; the point is that `killed` in this driver means "the
selftest did not pass", not "a case observed the rule change".

### 4. LOW (present in the shipped copy, harmless) — two extra cases derive their fixture *and* their expected value from the constant under test

- `extra_HardPopulation` F15: probe id `'S%03d' % MAX_ID` and expected `['S100', 'S%03d' % MAX_ID]` — both from
  `MAX_ID`, so the case cannot detect a wrong `MAX_ID` by construction.
- `extra_HardMeasure` F11: `n = TARGET`, and the expectation is `population/verified/fresh/target = str(n)` — the
  same self-reference for `TARGET`.

Measured coverage: both are nevertheless killed by a sibling hardcoded case. `MAX_ID = 160` → `161` gives
`KILLED rc=1 fails=['T15_population_bounds']`; `TARGET = 50` → `40` gives
`KILLED rc=1 fails=['F12_target_50_floor']`. So the round's kill count does not rest on these two, but they are
self-fulfilling in isolation (item candidate (c)). Counterfactual shape confirmed: replacing F04's hardcoded
`want=['S100']` with `_xHardPopulation_ids('S101', 'a — this cell carries no link', 'mined')` gives
`pristine=pass VERDICT: PASS`, `F04 survived` — a case that can never kill. The shipped copy hardcodes every
`want` (F04 is `killed`, see table).

### 5. INFO — timeout counts as killed; headroom is ≈99×

`run_selftest` maps `TimeoutExpired` to `'timeout'`, and `judge()` maps anything that is not `'pass'` to
`killed`, so a slow mutation is a kill without any rule being tested. Demonstrated cheaply by patching the
driver's module constant in-process (`mut.TIMEOUT = 3`) and judging a copy with `time.sleep(5)` at import:
`pristine=timeout tail='timeout' (TIMEOUT patched 300->3)` → killed. Against the real bound: pristine 0.48 s /
1.54 s, slowest declared-mutant run 1.99 s, slowest run overall 3.02 s (neutral CN3) vs `TIMEOUT = 300`
(≈99× headroom); the driver's full 25-mutant run took 13.24 s at `max_workers=8`. No declared mutant is near
the bound, so the timeout path cannot be what produced any of the 25 kills.

### 6. INFO — no fixture nondeterminism found (path, clock, cwd)

Pristine selftest, 5 environment variants each, both counters: `TMPDIR` default, `TMPDIR` a symlink
(`/tmp/t46-link`), `TMPDIR` a directory with spaces, `TZ=Pacific/Kiritimati`, `cwd=/` → all 10 runs
`rc=0` with identical PASS/FAIL/VERDICT lines and identical case counts (freshness 36 cases, coverage 22 cases);
`identical_to_default=True` in every variant. Neither counter imports `datetime`, `time` or `random`, and every
date in the fixtures is compared against the string constants `MIN_OPENED`/`MIN_VERIFIED` (`'2026-10-25'`), not
against the wall clock. The temp path never reaches an asserted value: the coverage assertions read the
counter's summary line (`rev=m`, no path) and the freshness ones read `C1_R45` fields only.

### 7. INFO — reproducibility and control

- Driver at 6f2168e: `killed=25 neutral_killed=0 pristine=1 equivalence=1 self_pin=1 C2_R46_PASS=true`.
- Same 25 replacements against the round-45 originals: `killed=0` (all `survived`), pristines `PASS` — the
  contract's before-state reproduces.
- The hardened copies' base sections are byte-identical to the round-45 originals apart from the `SELF_PATH`
  repoint, so the base cases were not edited to help the count.

### 8. INFO — the hardened target files do not exist at the freeze revision

`git -C LANE show 745a583181648cfc7f9c1b476cd1be7dc68f7433:.ufo/evidence/round-46/hardening/freshness-counter.py`
→ `fatal: path … exists on disk, but not in '745a583…'` (same for coverage-counter.py). `mutate.py` and
`mutants.json` are identical at the freeze and at 6f2168e (`sha256 999e0a4b…`, `bd21304a…`). C2's counter and
manifest are frozen; C2's *targets* are wave-1 build products that first appear at the content revision. This
matches wave-1 authorship of the additions, but the contract's freeze sentence ("the three claim counters with
their selftests … committed there before any seat") does not cover these two files — recorded so the L1 can
decide whether the freeze list or the sentence should be corrected.

## Unrun / out of scope

- The deciding run at the L1's revision was not run by me; I only re-ran the driver against
  `--rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32` as wave 2 permits.
- C1 and C3 counters were not touched.
- No tool installs were needed (Python 3.14.8, git 2.56.0 present); nothing was installed, upgraded or fetched.
- Scratch: `/tmp/tameshi-r46-T46CritHarden/{src,matrix.py,matrix.json,gaming.py,driver-hardened.out,escape-probe}`.
  No git/jj command was run in the lane; no fixture repo was created outside `mktemp`/`TemporaryDirectory`
  scratch dirs.
