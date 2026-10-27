# T51W2ExecTool28 — independent audit, C3 registry row `write-path census v3`

Round 51, wave 2 (falsify), seat T51W2ExecTool28. Lane `tameshi-shokunin` at
candidate `6d8c11e378aa90b12650808e1b79270742935f15`. Read-only on the lane: all
runs used `git clone --shared` fixtures under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool28/`, each fixture restored with
`git checkout --` and verified clean. No source edit and no row repair (seat bound).
Raw output: `.ufo/waves/round-51/w2/@P@ExecTool28/` (`audit.log` is the command log).

## Row under audit

`SKILL.md:2169` at CAND (section `#### Gate/probe registry — round 51`, 30-row
table, row 28 of that section; the section is the file tail, `SKILL.md` is 2171
lines and the table ends at 2171):

| field | cell text |
|---|---|
| Name | write-path census v3 |
| Kind | probe |
| Entry command | `python3 tools/write-path-census-v3.py --file FILE` |
| Verdict map | 0 clean (census printed); 1 failed (selftest mismatch or unreadable input); 2 could-not-evaluate (usage) |
| Self-test command | `python3 tools/write-path-census-v3.py --selftest` → WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0 |
| Pinned values | `.ufo/evidence/round-41/census/fixtures.json` plus literal expected counters in the tool EXPECT table |
| Write scope | stdout only; selftest reads the committed fixtures and writes nothing |
| Owner | tameshi |

Source is `tools/write-path-census-v3.py` (346 lines, blob
`84b4b43051d91504f59a362ce123b02474ee753c`, sha256 `095924a7…`); the committed
fixture is `.ufo/evidence/round-41/census/fixtures.json` (sha256 `20b6254d…`).
Both blobs are byte-identical at base and CAND (`git diff --stat base..CAND` over
the two paths is empty), and `SKILL.md` at base has zero occurrences of the tool
name: the row is new, the tool is not.

## Measured runs (candidate clone, stdin `/dev/null`, scratch TMPDIR)

| run | command (row-exact where marked) | exit | last stdout line | wall |
|---|---|---|---|---|
| self-test (row-exact) | `python3 tools/write-path-census-v3.py --selftest` | **0** | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` (single stdout line; stderr empty) | 34 ms (27 ms first run) |
| usage probe | `python3 tools/write-path-census-v3.py --r51-no-such-flag` | **2** | none (stdout 0 bytes; argparse error on stderr) | 33 ms (26 ms first run) |
| entry | `--file <source with an expected-value write>` | 0 | totals line, `expected=1 unflagged=1` | < 40 ms |

The row's recorded marker is byte-identical to the observed pass marker, and the
observed usage code `2` is a token in the row's verdict map. The frozen C3
counter's own helpers agree: with `measure.py` read from CAND and my clone as the
fixture, `row_reason(...) -> None` and `run_row(...) ->
(None, '<the same marker line>')`, i.e. the row is counter-covered
(`counter-row-check.txt`).

## Field-by-field check against source

1. **Kind `probe` — correct.** Run mode `--file` (src:313, 322-340) prints
   classification records plus a totals line and returns 0 for any readable file;
   a file with a syntax error still exits **0** with `parse_errors=1`
   (`file-broken.out`), so run mode expresses no verdict and has no failure
   surface. The only comparison against committed expected values is
   `--selftest` (src:276-306, `EXPECT` at 268-272). PROTOCOL.md:375-379: "A tool
   that cannot fail is a probe, and is registered as one." Lane convention is
   consistent (v1 `--census` is `gate` at SKILL.md:2171; v2/v4 are `probe`).
2. **Entry command exists and behaves as stated.** `--file` is src:313; a
   `open("expected.json","w")` source yields `expected=1 unflagged=1`
   (`open-w.out`) and a `Path(...).write_text` source the same
   (`open-sample.out`), both exit 0.
3. **Verdict map codes are all reachable and no undeclared code was found.**
   Measured 0 (self-test pass; census), 1 (self-test mismatch — `selftest-broken-pin.out`;
   unreadable input — `FileNotFoundError` traceback, `file-missing.err`), 2
   (unknown flag; no mode). `--help` exits 0 with usage text and
   `--file X --selftest` exits 0 by running the self-test (`help.out`,
   `mixed.out`); these are not the row's entry invocation, so the row's
   "0 clean (census printed)" is not contradicted. Caveat in F1.
4. **Pinned values exist and are load-bearing.** `FIXTURE_REL` (src:44) resolves
   from the repo root in `selftest()` (src:318-319), and the path exists at CAND;
   the `EXPECT` literals are src:268-272. Replacing the `var_unflagged` fixture
   body with a non-write source makes the self-test exit **1** with
   `FAIL planted var_unflagged: want unflagged=1 got 0` (`selftest-broken-pin.out`):
   the pin governs behaviour, it is not decorative.
5. **Write scope is true.** After the self-test, `git status --porcelain` in the
   clone was empty, no file under the clone was newer than a marker created
   before the run, and the supplied TMPDIR stayed empty (0 entries). The tool's
   only `open()` calls are read-mode (src:277, 322); there is no `tempfile`,
   `makedirs`, `json.dump` or write-mode open in the file. "stdout only" holds.
6. **The marker is a real diagnostic, not help text.** It is computed from
   `summarize(classify_source(body))` per fixture (src:295-301). A killed
   `os.symlink` arm changes it to `symlink_unflagged=0` and exits 1
   (`mut-symlink.out`). It is not an argparse string or an author-chosen label.
7. **Clone-safe, so row16's known blocker does not apply here.** The self-test
   passes from the `--shared` clone under `/fast` (outside the fleet), and also
   with cwd outside the clone (`selftest-outside.out`); the source has no
   `environ`/`getcwd`/`expanduser`/`fleet`/sibling/`../` path use (one comment
   line only, src:186). Row16 of this section is `round21 measure facade`
   (`SKILL.md:2157`), whose `round21-measure.py --selftest` is the known red row;
   my tool is row 28 and is not that row.

## Findings

**F1 — verdict-class precision: "unreadable input" is an uncaught traceback, not
a graded failure (low–medium).** The row maps unreadable input to code 1
("failed"), and the exit code does match (`--file` on a missing path →
`FileNotFoundError`, rc 1, `file-missing.out/.err`; `--selftest --fixtures` on a
missing JSON likewise, `fix-missing.out/.err`). But the tool's own docstring
(src:23) declares `1` as *selftest fail* only, and there is no designed message
or verdict on this path — the operator gets a Python traceback. PROTOCOL fixes
`1 = failed fleet-wide`, so an input/I-O error is classified as a content
failure rather than `could-not-evaluate`; a truthful row cannot declare `2` for
it. The row's parenthetical discloses the trigger, so this is a limitation the
row inherits from the tool, not a false cell — but it is the one place where a
reader of the row will expect a verdict and find a crash.

**F2 — the recorded self-test is weaker evidence than it appears: 5 of 6
documented behaviour arms regress green (medium, evidence strength).** Six
single-edit mutants of the tool, each run in the clone and restored, with the
row's exact self-test:

| mutant | exit | marker |
|---|---|---|
| `os.symlink` arm disabled | 1 | `symlink_unflagged=0` + FAIL — **caught** |
| `'scratch'` literal removed from `SCRATCH_MARKERS` (`'/tmp'` remains) | 0 | identical to row — **survived** |
| `EXPECTED_RE` narrowed to `expected\.json` | 0 | identical — **survived** |
| `FLAG_RE` replaced with a never-match | 0 | identical — **survived** |
| `open(...)` write branch disabled | 0 | identical — **survived** |
| `Path.write_text`/`write_bytes` branch disabled | 0 | identical — **survived** |

Consequences measured against the tool's documented scope (src:12-14: open with
write modes, `Path.write_text`/`write_bytes`, `os.replace`/`os.rename`,
`os.symlink`): **three of the advertised write forms (`open`, `write_text`,
`write_bytes`) have no fixture**, the update-flag rule (`FLAG_RE`, src:41, used
at src:218) has none, four of the five `EXPECTED_RE` alternatives (src:32) have
none, and the fixture named `scratch_var` pins scratch detection only through
`/tmp` — removing the `scratch` keyword itself does not fail it. The C3 predicate
only requires the self-test to exit 0 at REV, so the row still passes; the
finding is that this row's self-test cannot detect those regressions. Not
repaired (seat bound); disclosed for the claim's `cannot_see` surface.

**F3 — the marker is necessary but not sufficient; a failing self-test can print
the row's exact recorded line (low).** The marker prints only the per-fixture
`unflagged` counters, while `EXPECT` also asserts `expected_sites` (src:268-272).
Replacing the `scratch_var` fixture body with a non-write source exits **1**
with `FAIL planted scratch_var: want expected_sites=1 got 0` while printing the
row's recorded marker verbatim (`selftest-scratch-pin.out`). The counter is not
fooled (it requires exit 0), and the row's verdict map carries pass/fail, so no
false credit — but anyone comparing only the marker text sees no difference
between that failing run and the recorded pass.

**F4 — informational: no cell-level falsehood found.** Kind, entry command,
declared exit codes (as codes), pinned path + literals, write scope and the
self-test marker all verify against candidate bytes and clone runs. The defects
are F1's class semantics and F2/F3's evidence coverage, not a fabricated cell.

## Observations for the claim's limits (not decisions)

- The frozen counter parses **32** rows at CAND: both `### Gate/probe registry`
  (round 12, 2 rows) and `#### Gate/probe registry — round 51` (30 rows) match
  `HEAD_RE` (`measure.py:42`, `registry_rows` at 89-99). The v3 tool is counted
  once (only line 2169 names it), so this does not double-cover my row; it does
  mean the "30-row" section is not the only registry input.
- The round-51 registry section carries no prose scope paragraph (table only,
  file tail) — consistent with the wave-1 disclosure about the section's
  narrative, and not a row defect.
- C3's honest-failure risk is confined to row16 (`round21 measure facade`,
  `SKILL.md:2157`), not to this row; this audit adds no new blocker there.

## Receipts

`@P@ExecTool28/`: `audit.log` (commands + results), `selftest.out/.err`,
`usage.out/.err`, `timing.txt`, `status-before.txt`/`status-after.txt`,
`selftest-outside.out`, `file-missing.out/.err`, `fix-missing.out/.err`,
`file-broken.out/.err`, `help.out`, `mixed.out`, `noargs.out/.err`,
`open-w.out`, `open-w.py`, `open-sample.out`, `open-sample.py`, `sample.py`,
`selftest-broken-pin.out`, `selftest-scratch-pin.out`, `mut-symlink.out`,
`mut-scratch.out`, `mut-expected-re.out`, `mut-flag-re.out`, `mut-open-arm.out`,
`mut-write-text.out`, `counter-row-check.txt`, `counter-measure.py.copy`,
`refs.txt`.

## Verdict on the item

Row 28 is **runnable and counter-covering** at CAND: the row-exact self-test
exits 0 from a fresh `--shared` clone with the recorded last-line marker, the
usage probe exits 2 as declared, the pinned fixture exists and changes the
result, and the write scope is true. It is **not falsified**. Two precision
defects are disclosed: the unreadable-input path is a traceback classified as
`failed` (F1), and the self-test leaves the `open`/`write_text`/`write_bytes`
forms, the update-flag rule and most expected-value regex alternatives
unprotected (F2), with a marker that can be identical on a failing run (F3).
