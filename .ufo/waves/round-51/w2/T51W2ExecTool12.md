# T51W2ExecTool12 — C3 row falsification: `tools/receipt-window.py`

Seat: T51W2ExecTool12 (executor, leaf). Item: independently audit the C3 registry row for
`tools/receipt-window.py` at content candidate `6d8c11e378aa90b12650808e1b79270742935f15`
(base `9962033fd7a75aa2f2847e979dd687a5d28505a1`, amended freeze `9d023aed…`).
Judged on: operability. Milestone: C3 row falsification.

**Result: no mismatch found in the row.** Every cell of the row is true of the candidate
bytes, the registered self-test exits 0 with the stated last line, and the
`--r51-no-such-flag` probe exits 2, a code the verdict map declares. Three tool-level
warts exist and are already disclosed by the drafting seat (`w1/T51Row12.md`, findings 1–3);
none of them contradicts a row claim. Two documentation nuances are recorded in §5 without
being row defects. This row is **row 12** of the section; the item's "row16 clone-context
failure" is the `round21 measure facade` row (row 16), not this one — this row's self-test is
hermetic and passes from a cold clone.

Method: read-only on the lane and fleet. All execution happened in
`git clone --shared` fixtures under `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool12/`
(`rev-parse --show-toplevel` asserted on each fixture before any fixture git command;
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool12/clone/lane3` was the only fixture that made
a commit, for the single-row counter probe in §8). Explicit scratch `TMPDIR`, stdin
`/dev/null`, wall clock measured around each child. Scratch deleted before yield.

## 0. The row under test — `SKILL.md:2153` at CAND (section heading `#### Gate/probe registry — round 51`, `SKILL.md:2138`)

```text
| receipt-window validity | gate | `python3 tools/receipt-window.py --contract CONTRACT_JSON --receipts RECEIPTS_JSON` (add --json for one machine-readable verdict object) | 0 clean; 1 failed (findings); 2 could-not-evaluate (contract or receipts invalid, also argparse usage); 64 usage (missing --contract or --receipts) | `python3 tools/receipt-window.py --selftest` → RECEIPT_WINDOW_SELFTEST: last non-empty stdout line reads RECEIPT_WINDOW_SELFTEST: 20/20 pass with exit 0 | `.ufo/evidence/round-20/contract.json` expectations and instrument shas; `.ufo/evidence/round-20/public-cli-cases.json` synthetic cases; `.ufo/evidence/round-20/final/receipts.json`; `.ufo/evidence/round-20/final/receipt-window-selftest.json` recorded 20/20 exit 0 | reads caller-chosen CONTRACT_JSON and RECEIPTS_JSON without writing; selftest writes only its TMPDIR temp tree | tameshi |
```

Eight cells, no `|` inside a cell. Tool at CAND: `tools/receipt-window.py`, 367 lines,
sha256 `f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc`. Natural row
number in the frozen 30-row order: **12** (row 11 is `round-20 receipt-window measure`, a
different tool, `tools/receipt-measure.py`; row 16 is `round21 measure facade`).

## 1. Self-test, run exactly as registered, from a cold clone at CAND

Clone: `git clone --shared` → checkout `6d8c11e3…`, `HEAD=6d8c11e3…`, toplevel asserted.
`TMPDIR=/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool12/tmp`. Command as backticked in the row:

```text
$ cd <clone>/lane && python3 tools/receipt-window.py --selftest </dev/null
exit 0 · wall 0.0299 s · 21 stdout lines · stderr 0 bytes
last non-empty stdout line: RECEIPT_WINDOW_SELFTEST: 20/20 pass
line 20 of 21:              PASS [20/20] malformed receipts is refused — RECEIPTS_INVALID
```

Receipts: `t_selftest.{json,out,err}`. The row's self-test cell is exactly this — command,
marker `RECEIPT_WINDOW_SELFTEST:`, tally `20/20 pass`, exit 0 — no overclaim.

Additional checks on the same evidence path:

- **Deterministic**: three consecutive runs produced byte-identical stdout,
  sha256 `84cbec1d30c951c5cec35e87a7e498b4488864dc7ff8a9701d542e72c98541c9`.
- **Clone-context independent**: run from outside the clone with an absolute tool path
  (`python3 <clone>/lane/tools/receipt-window.py --selftest`) → exit 0, same 21 lines,
  0.0289 s (`t_cwd_outside.json`). Source confirms it: the selftest reads no repo file; its
  only two files are fixtures written into
  `tempfile.TemporaryDirectory(prefix="tameshi-r20-rw-selftest.")` (`tools/receipt-window.py:327`,
  writes at `:329-330`, `:338-339`). This is the opposite of the row-16
  (`tools/round21-measure.py`) fixture dependency recorded in the round briefing.
- **No residue**: after the run the scratch `TMPDIR` contained no `tameshi-r20-rw-selftest.*`
  directory (see §6).

## 2. Usage probe, exactly as the frozen counter issues it

```text
$ python3 tools/receipt-window.py --r51-no-such-flag </dev/null
exit 2 · wall 0.0263 s · stdout empty
stderr: python3 tools/receipt-window.py --r51-no-such-flag
        usage: receipt-window.py [-h] [--contract CONTRACT] [--receipts RECEIPTS]
                                 [--json] [--selftest]
        receipt-window.py: error: unrecognized arguments: --r51-no-such-flag
```

Receipt `t_usage.{json,out,err}`. The verdict map contains the token `2` ("2 could-not-evaluate
(contract or receipts invalid, also argparse usage)"), so the counter's
`usage-exit-2-undeclared` branch is not taken. Same exit 2 for a missing flag value
(`--contract` with no argument, `t_contract_no_value`) and for an unknown flag combined with
`--selftest` (`t_selftest_plus_unknown`).

## 3. Exit codes and meanings vs the verdict map

Every code the tool can return is `0/1/2/64` (`tools/receipt-window.py:23`), plus the
uncaught-exception path (Python exits 1) and argparse's own 2. Observed at CAND:

| code | row's meaning | source | observed run | receipt |
|---|---|---|---|---|
| 0 | clean | `:232 return EXIT_CLEAN`; `:347-348` selftest pass | pinned round-20 contract+receipts → `RECEIPT_WINDOW: CLEAN (receipts=2 historical=0)` + 2 `INSTALL_IDENTITY` infos, 0.0366 s; `--json` → one-line `{"verdict": "CLEAN", …}` | `t_entry_pinned`, `t_entry_pinned_json` |
| 1 | failed (findings) | `:222 return EXIT_FAIL` | scratch receipt with unknown sha → `RECEIPT_WINDOW: FAIL (findings=1 receipts=1) finding=UNKNOWN_INSTRUMENT`, 0.0284 s | `t_fail` |
| 2 | could-not-evaluate: contract or receipts invalid | `:207` / `:211` → `emit_ce` (`:235-241`) | `{not json` as contract → `COULD_NOT_EVALUATE (CONTRACT_INVALID: cannot read contract: …)`; `{}` as contract → `CONTRACT_INVALID: contract.instruments must be a nonempty object`; `{"receipts": 5}` → `RECEIPTS_INVALID: receipts must be an object with a receipts array`; a directory as `--receipts` → `RECEIPTS_INVALID: … Is a directory` | `t_badcontract`, `t_schema_bad_contract`, `t_badreceipts`, `t_dir_receipts` |
| 2 | … also argparse usage | argparse at `:352` (`:357` in the w1 citation) | `--r51-no-such-flag`; `--contract` with no value; `--selftest --r51-no-such-flag` | `t_usage`, `t_contract_no_value`, `t_selftest_plus_unknown` |
| 64 | usage: missing `--contract` or `--receipts` | `:361-362` | no arguments (0.0397 s); `--contract` alone; `--receipts` alone — usage printed to stderr, stdout empty | `t_noargs`, `t_contract_only`, `t_receipts_only` |

No undeclared nonzero code was reachable. The map is a superset of the tool's own docstring
(`:12` declares `0 clean, 1 findings, 2 could-not-evaluate, 64 usage`) and, unlike the
older 7-cell round-20 row (`SKILL.md:1949`, which merges "64 usage/could-not-evaluate"),
separates 2 from 64 — which is what makes the registered `--r51-no-such-flag` probe land on a
declared code.

Two classification nuances, both benign for the counter and visible in the map's
wording rather than contradicted by it:

- `--help` exits 0 (`t_help`: stdout usage, 0.0x s). The map says `0 clean`; help is not a
  clean evaluation. This is the gate's wart, already reported as `w1/T51Row12.md` finding 2.
  The row does not claim `--help` is nonzero, and the counter's own `help-not-selftest`
  mutant targets rows that substitute `--help` for the self-test, which this row does not.
- A failing selftest case exits 1 (`RECEIPT_WINDOW_SELFTEST: 19/20 pass`), which the map
  files under "1 failed (findings)" although it is a selftest case, not a receipt finding.
  Same code, slightly narrower label.

## 4. Kind: gate, not probe

The tool can and does fail on real inputs: `t_fail` returns 1 with a named finding on a
receipt whose sha is neither frozen/installed nor historical. It is not a tool that merely
observes (the PROTOCOL test "a tool that cannot fail is a probe"). `gate` is correct.

## 5. Pinned values — all four exist at CAND, and the pins do affect the verdict

Existence at CAND (`git cat-file -e`): all four present.

- `.ufo/evidence/round-20/contract.json` — its `instruments["receipt-window"]`
  `frozen_sha256` = `installed_sha256` = `f03ae7e9…dcf7cc`, **equal to the sha256 of
  `tools/receipt-window.py` at CAND**. The pin therefore still describes the shipped bytes.
- `.ufo/evidence/round-20/public-cli-cases.json` — sha256
  `590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2`, equal to
  `fixture_sha256` recorded in `.ufo/evidence/round-20/final/public-cli-results.json`
  (`held: 20, total: 20`). That results file's `argv` are
  `python3 …/tools/receipt-window.py --contract … --receipts … --json`, i.e. the manifest is
  an independent expectation set **for this tool**, with expected exits {0, 1} and expected
  ids inside the tool's own vocabulary (`WINDOW_OK`, `HISTORICAL_INSTRUMENT`,
  `INSTALL_IDENTITY`, `FROZEN_AFTER_EDIT`, `INSTALLED_BEFORE_INSTALL`, `BAD_INTERVAL`, …).
  The row's "synthetic cases" is accurate.
- `.ufo/evidence/round-20/final/receipts.json` — the input that yields CLEAN (`t_entry_pinned`).
- `.ufo/evidence/round-20/final/receipt-window-selftest.json` — `exit: 0`,
  `instrument_sha256: f03ae7e9…` (the tool's sha), stdout 21 lines, last line
  `RECEIPT_WINDOW_SELFTEST: 20/20 pass`, stderr empty. The row's "recorded 20/20 exit 0" is
  exact.

**The pin binds the verdict** (experiment): copy the contract to scratch and replace
`instruments["receipt-window"]`'s two shas with `1`×64; the otherwise-clean pinned receipts
run then returns `exit 1`, `RECEIPT_WINDOW: FAIL (findings=1 receipts=2)`,
`finding=UNKNOWN_INSTRUMENT receipt=installed-gate-selftest …` (`t_altered_contract`,
0.0308 s). Restoring the shas restores exit 0. So the pinned instrument shas are load-bearing
for this gate's expected behaviour, not decorative.

Nuance (not a defect): the pinned contract carries only identity instruments — two entries,
`frozen == installed`, no `edit_interval`, no `historical` map. The tool's window branches
(`FROZEN_AFTER_EDIT` `:190-192`, `INSTALLED_BEFORE_INSTALL` `:193-195`) are therefore never
exercised by the pinned run (which prints two `INSTALL_IDENTITY` infos); they are exercised
only inside the selftest and by `public-cli-cases.json`. The row claims only that the file
holds "expectations and instrument shas", which is true.

Limits worth knowing for readers (both under this section): the tool itself never reads
`public-cli-cases.json` or the recorded selftest receipt (`grep` at CAND → no match inside `tools/receipt-window.py`);
those are external harness evidence. And the recorded selftest receipt's `argv` names
`.ufo/evidence/round-20/stage/receipt-window.py`, which is byte-identical to
`tools/receipt-window.py` (both sha `f03ae7e9…`, `diff` empty), so the record still describes
the shipped bytes.

## 6. Write scope — accurate

- Source scan at CAND: the only `open()` calls are `:63` and `:125` (mode `"r"`, encoding
  utf-8) and the two selftest fixture writes under the `TemporaryDirectory` at `:327`.
  No `os.remove`/`unlink`/`rename`/`makedirs`; **no `/tmp` literal anywhere**
  (`grep -n /tmp tools/receipt-window.py` → no match), so nothing escapes `TMPDIR` in the
  selftest.
- Empirically: after 19 tool invocations in the clone, `git status --porcelain` was empty —
  no lane file created or modified by `--contract/--receipts`, `--json`, `--selftest`, or any
  probe. Scratch `TMPDIR` held only the fixtures this seat wrote; the selftest's
  `tameshi-r20-rw-selftest.*` tree was gone.

The row's "reads caller-chosen CONTRACT_JSON and RECEIPTS_JSON without writing; selftest
writes only its TMPDIR temp tree" is exactly what the bytes do.

## 7. Is the last-line marker a meaningful diagnostic, or author-chosen help text?

Meaningful. The marker is a computed tally, and it moves with the tool's own logic:

- Unmodified: `RECEIPT_WINDOW_SELFTEST: 20/20 pass`, exit 0.
- One expectation broken in a scratch copy only (`frozen-sha receipt ending exactly at edit
  start`: interval end moved 10:00:00→10:00:01, so the case must now fail): last line
  `RECEIPT_WINDOW_SELFTEST: 19/20 pass`, **exit 1**, preceding line
  `PASS [20/20] malformed receipts is refused` (the per-case index denominators are
  `len(cases)`=18 for the 18 table cases and 20 for the two loader cases; the tally is the
  grader). Receipt `t_mut_broken`. The scratch mutation was `/fast/scratch/.../tmp/mut-tool.py`;
  no lane source was written or repaired.

So a green marker cannot be produced by text alone: it requires 20 passing comparisons over
the contract index, the receipt checks, and both file loaders. The marker is also the
counter's `finding-id` requirement (`RECEIPT_WINDOW_SELFTEST:` appears verbatim in the row).

## 8. Counter credit, in situ, at CAND

Two independent checks:

1. **Counter's own parser**, imported from `.ufo/evidence/round-51/c3/measure.py` and run
   against CAND: the section yields 32 eight-cell rows; exactly one row's entry names
   `tools/receipt-window.py` — line 2153, 8 cells; `row_reason(…) → None`, with the registered
   argv `['python3','tools/receipt-window.py','--selftest']` and usage argv
   `['python3','tools/receipt-window.py','--r51-no-such-flag']`. All four pinned paths resolve
   at CAND, so no `pinned-path-missing`.
2. **Counter run on a single-row probe clone** (`clone/lane3`: CAND bytes, other round-51
   table rows removed, one fixture commit `462859f`):

```text
C3_TOOL tools/receipt-window.py: covered line 2143 selftest exit=0 last=RECEIPT_WINDOW_SELFTEST: 20/20 pass
C3_R51: rev=462859f0… tools=30 rows=4 covered=2 missing=28 deleted=0 selftest_fail_rows=1 total=28 C3_R51_PASS=false
```

(Receipt `c3-counter-single-row-probe.txt`.) The nonzero total is the expected shape of a
single-row probe — only this seat's row (and the receipt-measure row, whose pinned cell also
names this tool's file) survived the filter; the other 28 tools have no row there. The
`C3_TOOL` line for this row is `covered … exit=0 last=RECEIPT_WINDOW_SELFTEST: 20/20 pass`,
exactly the row's claim.

A full 30-row counter run at CAND also completed (853 s wall, 6 workers, stdout only,
stderr 0 bytes; exit 1 = "not PASS", not a crash). Its line:

```text
C3_TOOL tools/receipt-window.py: covered line 2153 selftest exit=0 last=RECEIPT_WINDOW_SELFTEST: 20/20 pass
C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false
```

Receipt `c3-counter-full-explain-at-CAND.txt`. In the real table this row is credited at its
own line (2153) on the first attempt; no other row of the section competes for
`tools/receipt-window.py`. The run's single `missing` tool is `tools/round21-measure.py`
(`line 2157 selftest-exit=1 last=`), the known clone-context blocker this seat does not own;
`selftest_fail_rows=2` is that row plus the pre-existing base row for
`tools/bash-witness-study.py` at `SKILL.md:1504`, whose job exits 0 but does not print the
`VERDICT:` marker its row names — the round-51 row at 2142 covers that tool, so the count is
2 while `missing` stays 1. Neither figure involves this row.

## 9. Mismatches found

**None in the row.** Every cell survives falsification:

| cell | claim | verdict |
|---|---|---|
| Name | "receipt-window validity" | accurate; unique in the section |
| Kind | gate | tool returns 1 on findings (`t_fail`) — gate, not probe |
| Entry command | `--contract C --receipts R` (+`--json`) | runs, exits 0 CLEAN on the pinned pair; `--json` emits one JSON object |
| Verdict map | 0 / 1 / 2 / 64 with stated meanings | all four observed, no undeclared nonzero code reachable |
| Self-test command | `python3 tools/receipt-window.py --selftest` → `RECEIPT_WINDOW_SELFTEST: 20/20 pass`, exit 0 | exact, from a cold clone at CAND, 0.0299 s |
| Pinned values | 4 lane-relative paths, "expectations and instrument shas", "synthetic cases", "recorded 20/20 exit 0" | all exist; shas match the candidate bytes; pins are load-bearing; record matches |
| Write scope | reads two inputs without writing; selftest writes only its TMPDIR tree | confirmed by source scan, clean `git status`, empty TMPDIR residue, no `/tmp` literal |
| Owner | tameshi | correct |

Compared with the drafting seat's report (`w1/T51Row12.md`), my independent probes reproduce
its observations (argparse 2 vs the docstring's 64 promise; `--help` exits 0; selftest
re-implements `load_contract`'s index instead of loading it, so `load_contract` drift would
stay green; the gate never hashes its own bytes). None of these is a row falsehood: the row
declares 2 for argparse usage — so a reader is told the truth — and the three remaining
points are tool properties the row neither asserts nor needs.

## 10. Risks, limits and blockers (for the L1)

1. **Row credit is not the claim.** This row credits, and the full counter run at CAND shows
   `covered=29 missing=1`: the only absent tool is `tools/round21-measure.py`, whose
   `--selftest` exits 1 from a clone because its fixture expects sibling fleet repos — the
   known blocker owned elsewhere, and the reason `C3_R51_PASS=false` stands at CAND. Nothing
   in this report changes that; no row can make that suite green without a shim or a false row.
2. **Section-level cold-read loss is unaffected by this audit.** `#### Gate/probe registry —
   round 51` is the section that loses cold-read credit (registry section,
   `no-ledger-entry`); the row is truthful but the section still needs the L1's re-key/reader.
3. **Full counter run at CAND is slow but finished here.** 853 s wall for 30 tools at 6
   workers (per-tool selftest limit 900 s). The deciding run should budget for that; a timeout
   at a few hundred seconds would look like a row failure but is a runtime property.
   `C3_R51_PASS=false` at CAND comes only from `tools/round21-measure.py` (`missing=1`,
   `total=1`), not from any other row — all 29 other tools credit.
4. **Pinned contract exercises only the identity path.** The window semantics the tool exists
   for (`FROZEN_AFTER_EDIT` / `INSTALLED_BEFORE_INSTALL`) are not exercised by the committed
   round-20 contract; they live in the selftest and in `public-cli-cases.json`. A future round
   that wants a window-bearing contract on disk will need a new pin; this row does not claim
   otherwise.
5. **`public-cli-cases.json` is external evidence.** The tool never reads it, so the pin's
   truth is the harness's (`public-cli-results.json` 20/20), not the tool's. Anyone reading
   "pinned values" as "files the tool consumes" would over-read the cell by one file; the cell
   wording ("synthetic cases") does not say the tool reads it.

## 11. Cleanup and bounds

- Lane, fleet and sibling repos: read-only (`git show`, `git cat-file`, `git grep`). No git/jj
  mutation in any of them.
- Fixtures: `clone/lane` (CAND checkout, all probes), `clone/lane3` (single-row probe, one
  commit `462859f`, toplevel asserted). Scratch root
  `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool12/` deleted before yield; nothing under
  `/tmp` was written by this seat.
- No tool install or upgrade; pacman untouched.
- No claim decision, no counter/spec/target amendment; no lane source repaired.

## 12. Receipts

`.ufo/waves/round-51/w2/T51W2ExecTool12/` (`MANIFEST.sha256` lists every file):

- `summary.json` — all 19 tool-invocation receipts (argv, exit, wall_s, stdout line count,
  last line, first stderr line).
- `t_selftest.*` (exit 0, 0.0299 s, 21 lines, `RECEIPT_WINDOW_SELFTEST: 20/20 pass`),
  `t_cwd_outside.*` (outside-cwd run, exit 0), `t_mut_broken.*` (one broken case → 19/20,
  exit 1).
- `t_usage.*` (exit 2, argparse error), `t_noargs.*` (64), `t_contract_only.*` (64),
  `t_receipts_only.*` (64), `t_contract_no_value.*` (2), `t_selftest_plus_unknown.*` (2).
- `t_entry_pinned.*` (0, CLEAN receipts=2), `t_entry_pinned_json.*` (0, one JSON line),
  `t_window.*` (0), `t_fail.*` (1, UNKNOWN_INSTRUMENT), `t_altered_contract.*` (1 after
  pin substitution — the pin-binds-verdict experiment).
- `t_badcontract.*` (2 CONTRACT_INVALID), `t_schema_bad_contract.*` (2), `t_badreceipts.*`
  (2 RECEIPTS_INVALID), `t_dir_receipts.*` (2), `t_help.*` (0 — the documented wart).
- `c3-counter-single-row-probe.txt` — the frozen counter's own `--explain` output on the
  single-row probe clone, including
  `C3_TOOL tools/receipt-window.py: covered line 2143 selftest exit=0 last=RECEIPT_WINDOW_SELFTEST: 20/20 pass`.
- `c3-counter-full-explain-at-CAND.txt` — the same counter's complete 30-tool run at CAND
  (`covered=29 missing=1`, this row `covered line 2153`), exit 1 with `total=1` from
  `tools/round21-measure.py` alone.

## Summary

The `receipt-window validity` row (row 12) is truthful at candidate `6d8c11e3…`: registered
self-test exits 0 in a cold clone with the exact stated last line (`RECEIPT_WINDOW_SELFTEST:
20/20 pass`, 21 lines, 0.0299 s), the `--r51-no-such-flag` probe exits 2 which the verdict map
declares, all four pinned paths exist and the instrument shas equal the shipped tool bytes
(altered pins flip the verdict to FAIL, so the pins are load-bearing), the write scope is
exactly "read two inputs, write nothing but the selftest's TMPDIR tree", and the last-line
marker is a real tally (a single broken case prints 19/20 and exits 1). No mismatch found; no
row, source or lane file was modified.
