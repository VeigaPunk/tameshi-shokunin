# T51W2ExecTool03 — falsify the C3 registry row for `tools/context-capture.py`

Seat: `T51W2ExecTool03` (executor, leaf). Axes: operability. Milestone: C3 row falsification.
Candidate: `6d8c11e378aa90b12650808e1b79270742935f15` (`git rev-parse HEAD` in the lane).
Row under audit: `SKILL.md:2144`, the 3rd of 30 data rows in `#### Gate/probe registry — round 51`
(section opens `SKILL.md:2138`; the counter counts it as row 5 of 32 because it also parses the two
rows under the older `### Gate/probe registry` heading at `SKILL.md:1499`).

Raw receipts: `./T51W2ExecTool03/` beside this file (`row-2144.txt`, `row-and-pins.txt`,
`selftest.stdout|stderr|exit`, `usage.stdout|stderr|exit`, `check.stdout`, `tamper-frozen.stdout`,
`timings.json`, `probes.txt`, `c3-counter-explain.stdout`, `round21-contrast.*`,
`base-row-1680.txt`, `selftest-lastline.txt`).

## Verdict

**No predicate falsifier. The row is covered by the frozen counter and its self-test is real,
hermetic and reproducible.** Four row-text fidelity defects were found (M1–M4 below); none of them
is visible to the frozen predicate, and none of them makes the row's operative claims false. Two of
the four are the kind of defect wave 2 exists to find: an inexact quote of the last line (M1) and an
under-described pinned-values cell that omits a live third pin (M2).

Frozen counter, full run at CAND (`.ufo/evidence/round-51/c3/measure.py --lane … --rev CAND
--work <scratch emptydir> --explain`, 696 s, exit 1):

```
C3_TOOL tools/context-capture.py: covered line 2144 selftest exit=0 last=SELFTEST: PASS (49/49)
C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false
```

`missing=1` is not this row: it is `C3_TOOL tools/round21-measure.py: MISSING (line 2157
selftest-exit=1 last=)`, the known blocker disclosed in `l1-notes.md` and `T51CritC3Counter.md`. My
row is row 3 of the canonical table; row 16 (`SKILL.md:2157`) is the blocked one.

## Measured, from a `git clone --shared` at CAND

Clone toplevel asserted (`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool03/clone`), every run with
`stdin=/dev/null`, `env -i PATH=/usr/bin:/bin HOME=… TMPDIR=<scratch>/tmp`, `cwd` = clone root.

| command | exit | last stdout line | wall |
|---|---|---|---|
| `python3 tools/context-capture.py --selftest` (row's exact backticked command) | **0** | `SELFTEST: PASS (49/49)` | **1.48 s** (cold 2.05 s; 3/3 identical) |
| `python3 tools/context-capture.py --r51-no-such-flag` (usage probe) | **64** | *(stdout empty; stderr ends `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`)* | 0.03 s |
| `python3 tools/context-capture.py --check` (row's entry command) | **0** | `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8…c1a exit=0 findings=0)` | 0.03 s |
| `--help` / `-h` | 0 | usage text, **no** `CONTEXT:` verdict line | 0.03 s |
| no arguments | 64 | *(stdout empty)* | 0.03 s |

The counter's own `run_cmd`/`run_row` were also driven directly (`measure.py:160-184`) and returned
`row_reason=None`, `run_row verdict=None`, `last='SELFTEST: PASS (49/49)'`.

## Predicate clause by clause

| frozen clause (`contract.json` C3) | result | evidence |
|---|---|---|
| tool exists at REV and carries `selftest` | holds | in `tools-base.json`; `git show CAND:tools/context-capture.py` sha256 `c4a1d165…` identical at base and CAND |
| has a SKILL.md registry row, 8 cells | holds | `SKILL.md:2144`, 8 cells |
| kind `gate`/`probe` and it is the truth | **holds: it is a gate** | forced failure → exit 1 `comparison_mismatch`, exit 2 `snapshot_tampered` (`probes.txt` A) |
| entry command names the tool | holds | `--check` and `--check --receipt … --expected …` both exercised |
| verdict map names 0 and 1, and every other code | **holds and is complete** | observed 0/1/2/64 only; `main()` returns 64, 0, or `run_selftest()`∈{0,1,2}; `emit()` returns `result["exit"]`∈{0,1,2} |
| one backticked self-test command, `python3|bash`, no shell metacharacters | holds | `row_reason` returned None; exactly one backtick pair in the cell |
| pinned-value paths exist | holds | `.ufo/evidence/round-14/context-receipt.json` present at REV, sha256 `05cb55b8…c1a` |
| write scope present | holds | "none during `--check`; selftest fixtures under `/tmp/context-capture-selftest-*`, removed in finally" — all three facts verified |
| owner `tameshi` | holds | — |
| self-test exits 0 **from a clone at REV** | **holds** | exit 0, 49/49, 1.48 s, from `git clone --shared` at CAND |
| prints a last-line finding id recorded in the row | holds (`SELFTEST:`) | but see M1 — the quoted *rest* of the line is wrong |
| usage probe exits with a declared code | **holds** | exit 64, and `64` is in the verdict map |

## Mismatches (row text vs candidate bytes)

### M1 — the row's quoted last line is not what the tool prints

Row cell: `` `python3 tools/context-capture.py --selftest` → SELFTEST: PASS (49/49 cases) ``.

`tools/context-capture.py:1785` prints

```python
sys.stdout.write("SELFTEST: PASS ({}/{})\n".format(self.passed, total))
```

so the emitted line is `SELFTEST: PASS (49/49)` — the word `cases` never appears.
`grep -c 'SELFTEST: PASS (49/49 cases)'` against the real 50-line stdout returns **0**.

This is not the house convention for this table. Rows whose tools *do* print the word quote it
exactly: `SKILL.md:2154` (`tools/registry-check.py` emits `f"SELFTEST: PASS ({passed} cases)"`,
source `:1816`) and `SKILL.md:2156` (`tools/repeat-control.py` emits
`f"SELFTEST: PASS ({total} cases)"`, source `:858`). The round-51 row for `context-capture.py`
carries a neighbour's phrasing. A reader who greps the row's own string against tool output gets a
miss.

Why the counter cannot see it: `measure.py:178-180` takes only the **first whitespace token** of the
last line (`marker = last.split()[0]` → `SELFTEST:`) and tests substring membership in the cell.
`SELFTEST:` is present, so the row is credited. The count 49/49 is correct, and the tool's total is
`40 check_case + 7 usage_case + 2` hermetic records added in `finish()` = 49, so only the trailing
noun is fabricated.

### M2 — Pinned values names 2 of the tool's 3 live literals, and truncates the one it names

Row cell: `` `.ufo/evidence/round-14/context-receipt.json`; literal digest 05cb55b8… and id/exit pin
inside the tool ``.

The tool carries three pinned literals (`tools/context-capture.py:152-159`):

| literal | value | where it bites |
|---|---|---|
| `FROZEN_RECEIPT_SHA256` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` | `:1367` → `snapshot_tampered` exit 2 (verified) |
| `FROZEN_EXPECTED_ID` / `FROZEN_EXPECTED_EXIT` | `context_consistent` / `0` | `:1348-1350` → `expected_verdict_mismatch` exit 1 (verified) |
| **`FROZEN_TOOL_SHA256`** | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | `:1212` → `tool_declaration_mismatch` **exit 1** |

The third is live, not dead code. Probe: a scratch copy of the tool with `FROZEN_RECEIPT_SHA256`
repinned to a receipt whose own `tool_sha256` is `'0'*64` (digest gate satisfied, so the check is
reached) produced:

```
CONTEXT: MISMATCH (id=missing_injected_environment … exit=1 findings=4)
FINDING tool_declaration_mismatch retained tool_sha256 '0000…' is not the pinned historical declaration
```

With the committed receipt bytes the pin is inert, because the receipt digest pin already fixes
`tool_sha256` to `7313e9a2…`; it is a second-order consistency pin. It is still a pinned literal that
flips a frozen 0 to a 1, and the row does not mention it. The row also writes the digest as
`05cb55b8…`, i.e. a truncated prefix, so the row alone cannot be used to verify the pin; the
`PATHISH` test at `measure.py:146-151` (regex defined `:44`) never looks at it because it is not
path-shaped.

Regression against the row it supersedes: the base `### Round-15 gate/probe registry` row at
`SKILL.md:1680` gave the **full** 64-hex digest, the negative fixture
`.ufo/evidence/round-14/context-missing-env.json` (sha256 `1ee9d09b…`, verified present at CAND),
the `tameshi-context-expected-v1` schema and "literal selftest exit/finding pairs in tool". The
round-51 row keeps less of that. It is not false, but it is a fidelity loss for the same tool.

### M3 — "0 clean" also covers `--help`, which is not a verdict

`--help` and `-h` exit **0** and print usage text with no `CONTEXT:` line (verified: `HELP_EXIT=0`,
`grep -c 'CONTEXT:'` → 0). The row's map says `0 clean`. The base round-15 prose for this same gate
disclosed the distinction — `SKILL.md:1704`: *"Help exits0 only as a non-verdict informational
mode"* — and the round-51 row drops it. This is a lane-wide convention rather than a defect unique
to this row: `command-binding`, `env-diff`, `golden-verdict`, `receipt-window`, `registry-check` and
`pin-disposition` all exit 0 on `--help` too. Recorded because the row's class text is what a caller
reads.

### M4 — the write-scope cell is truthful, and that truth defeats the counter's TMPDIR containment

Row: *"selftest fixtures under `/tmp/context-capture-selftest-*`, removed in finally"*. Accurate on
all three counts:

* `tools/context-capture.py:1624-1625` — `tempfile.mkdtemp(prefix="context-capture-selftest-",
  dir="/tmp")`; **`dir` is hardcoded, so `TMPDIR` is ignored**.
* measured peak footprint **534 488 bytes**, 47 case dirs, gone afterwards.
* removal holds on both paths: PASS → no leftovers; forced FAIL (injected failing case → exit 1,
  `SELFTEST: FAIL (1/49 failed: …)`) → no leftovers either (`:1778` in `finish()`, plus the
  `finally` at `:2204-2206`).

`--check` writes nothing: a 12 500-file tree hash is byte-identical before and after `--check` +
`--selftest`, and `--check` still works in an isolated tree holding only the tool and the receipt,
with `receipt_missing` (exit 2) when the receipt is hidden.

The operability consequence is on the counter, not the row: `measure.py:160-171` sets
`TMPDIR=<work>/tmp` for every row expecting containment. This row's cell says `/tmp`, which is the
honest description, and the tool then writes to the real `/tmp` regardless of the counter's TMPDIR.
So the counter's per-row scratch isolation does not bind this tool, and a truthful row is exactly
what makes that visible.

## The known C3 blocker is not this row

`tools/round21-measure.py` (row 16, `SKILL.md:2157`) is the row whose `--selftest` cannot pass in a
fresh clone. Reproduced here for contrast from the same clone:

```
subprocess.CalledProcessError: Command '['git', '-C', '/fast/scratch/…/tameshi-shokunin', 'show', '08175c62…:tools/mutate-and-run.sh']' returned non-zero exit status 128.
ROUND21_EXIT=1
```

`tools/context-capture.py` is the opposite case and this is the seat's cleanest positive result:
its 49-case self-test passes in a tree containing **only** `tools/context-capture.py`, with no lane
tree and no sibling fleet repos (`probes.txt` E2). Nothing about this row can make C3 fail.

## Scope note: this tool already had a base registry row under an unparsed heading

At base, `SKILL.md:1680` carried `| retained invocation-context gate | gate |` for the same tool,
under the heading `### Round-15 gate/probe registry` (`SKILL.md:1676`). The counter's
`HEAD_RE` (`measure.py:42`, `^#{2,4} Gate/probe registry`) does not match that heading, so the row
was invisible and the tool counted as uncovered at base. The round-51 row at `:2144` is therefore a
re-registration into the parsed table, not a first registration. This corroborates, with a concrete
`file:line`, the wave-1 finding recorded in `l1-notes.md` that C3's base-scope narrative understates
existing rows.

## Handoff observation outside this row (not judged here)

While checking M4 I measured the real `/tmp` after the full C3 counter run. This row's tool left
**0 bytes and 0 directories**, which is what its cell promises. A sibling row's tool did not:

```
112 MB  tameshi-r14-evidence-disposition-selftest.*      (tools/evidence-disposition.py, row SKILL.md:2146)
  3 MB  tameshi-r12-repeat-control-selftest.*            (tools/repeat-control.py, rows SKILL.md:2156 / :1503)
  0 MB  tameshi-r4-2-regression.*                        (tally-audit-v3.py, row SKILL.md:2161)
```

112 MB of retained `/tmp` fixtures also shows that the counter's per-row `TMPDIR` containment
(`measure.py:164`) does not bind `evidence-disposition.py` either. Not this seat's item, no source
touched; offered to whoever audits `SKILL.md:2146`'s write-scope cell.

## Risks / limits of this audit

* M1 and M2 are text-fidelity findings. They do not falsify C3's predicate, which only requires a
  recorded finding id and a declared usage code. Reporting them as row defects, not as predicate
  failures.
* M2's third pin is unreachable with the committed receipt unless the receipt digest pin is also
  edited; I labelled it a second-order pin rather than an ordinary expectation.
* M4 is a counter-isolation observation. The row's text is correct; I did not treat it as a row lie.
* I did not audit the row's `--receipt/--expected` explicit path beyond the four pin probes above,
  nor any sibling row. Nothing was written to the lane except this report and its receipts.
* Run artifacts left in the real `/tmp` by this tool are transient and self-removed; nothing was
  installed or updated, so no tool/version/channel record is owed. Seat scratch
  `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool03/` is deleted before yield.
* Working-tree note for the parent, not a finding: while this seat ran, the lane worktree showed
  ` M SKILL.md` and ` M tools/tally-audit-v3.py` from other seats. Neither was touched here; every
  byte I audited came from `git show 6d8c11e…:<path>` and from a `git clone --shared` checked out at
  CAND, so no audit result depends on those in-flight edits.

## Checks the main agent should run

* `python3 .ufo/evidence/round-51/c3/measure.py --lane . --rev 6d8c11e… --work <emptydir> --explain`
  → expect `covered line 2144 selftest exit=0 last=SELFTEST: PASS (49/49)`, and `missing=1` to remain
  `tools/round21-measure.py`.
* If M1 is accepted as a row defect: the minimal correction is the row cell, replacing
  `SELFTEST: PASS (49/49 cases)` with `SELFTEST: PASS (49/49)`. Not applied by this seat.
