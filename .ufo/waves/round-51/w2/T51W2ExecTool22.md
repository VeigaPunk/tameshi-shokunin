# T51W2ExecTool22 — independent audit of the C3 registry row for `tools/trace-inputs.py`

Candidate `6d8c11e378aa90b12650808e1b79270742935f15`. Row audited: **SKILL.md:2163**, the
`traced input surface` row of the canonical section `#### Gate/probe registry — round 51`
(heading SKILL.md:2138). Lane read-only; `git clone --shared --no-checkout` at CAND in
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool22/c3/tameshi-shokunin`, `TMPDIR` under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool22/receipts/`, stdin `/dev/null`, `GIT_*` scrubbed as
`measure.py:env()` does. Raw receipts: `.ufo/waves/round-51/w2/@P@ExecTool22/receipts.txt`.
Audited tool blob: `598132df3e4046518851ec9482654828ded83723`, sha256
`f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4` (1003 lines).

## Verdict

**The row is operably true at CAND and would be credited by the C3 counter, but its verdict map
falsely narrows exit 1 to selftest failures, and its self-test cell pins no observable beyond a
marker string shared with two other tools.** Measured at CAND: the row's exact self-test exits 0 in
1.5 s and its last stdout line is `SELFTEST: 30/30`; the usage probe `--r51-no-such-flag` exits 64
(argparse `Parser.error`, `tools/trace-inputs.py:106-110`), which the map declares as usage; the
pinned cell's `none` claim holds for expectations; the write scope is accurate in every tested path.
The failures below are row-fidelity defects the counter cannot see (contract `cannot_see`), not
predicate failures: `row_reason` returns `None` for line 2163, and 2163 is the only 8-cell registry
row naming the tool (the round-18 row at SKILL.md:1933 is a 4-cell row the counter's
`registry_rows()` ignores by construction). This vector is **not** the known `round21-measure.py`
clone-context blocker: the self-test passed from the fresh shared clone with an empty scratch
TMPDIR and reads no sibling fleet repo (all roots are fixture paths, YAML below).

## What was run (counter-equivalent harness, cwd = clone root)

| probe | command | exit | wall | last line |
|---|---|---|---|---|
| row self-test | `python3 tools/trace-inputs.py --selftest` (stdin `/dev/null`) | **0** | 1509 ms | `SELFTEST: 30/30` (30 PASS, 0 FAIL, stderr empty) |
| usage probe | `python3 tools/trace-inputs.py --r51-no-such-flag` | **64** | 35 ms | stdout empty; stderr `trace-inputs.py: error: unrecognized arguments: --r51-no-such-flag` |
| entry, clean trace | `--root . --out <new 4-level parent>/r.json -- python3 -c "open('SKILL.md').read()"` | 0 | 191 ms | receipt `exit=0 inputs=['SKILL.md']`, parent dirs created |
| entry, traced cmd exits 3 | `--root . --out e2.json -- python3 -c "sys.exit(3)"` | **0** | — | receipt `exit=3` |
| entry, missing binary | `-- /no/such/binary` | 2 | — | `no successful execve for the root process` (source:646) |
| entry, `--root` not a dir | `--root /nonexistent-r51` | 2 | — | `root not a directory` (source:602) |
| entry, `--cwd` not a dir | `--cwd /nonexistent-cwd` | 2 | — | `cwd not a directory` (source:606) |
| usage, `--root` without `--out` / no args / `--selftest`+unknown flag | — | 64 / 64 / 64 | — | `--out is required` / `--root is required` / `unrecognized arguments` |
| **`--out` is an existing directory** | full trace, then `open(ns.out,'w')` | **1** | 187 ms | stderr traceback `IsADirectoryError ... line 690 in run_trace` |
| **`--out` parent uncreatable (`/proc/...`)** | full trace, then `os.makedirs` | **1** | — | stderr traceback `FileNotFoundError ... makedirs` |
| run mode, PATH without strace | `--root . --out n1.json -- true` | 2 | — | `strace not found in PATH` (source:610) |
| `--selftest`, PATH without strace | same argv | **1** | 1159 ms | `SELFTEST: 5/30` (25 FAIL; the 5 passes are vacuous: no workdir was ever made) |

Cleanliness after six run-mode invocations: TMPDIR scratch empty, clone `git status --porcelain`
empty, no `trace-inputs-run-*` and no `__pycache__` anywhere under the clone.

## Findings against the row's cells

**F1 — verdict-map mismatch (the one real falsification).** Cell 4 declares `1 failed (selftest
check)`. Run mode also exits **1** through an uncaught traceback whenever the receipt cannot be
written: `tools/trace-inputs.py:688-690` runs `os.makedirs(out_dir)` and `open(ns.out,"w")` outside
any handler, so `--out DIR` (`IsADirectoryError`) and an uncreatable parent (`FileNotFoundError`)
both exit 1 with empty stdout and no receipt. The tool's own docstring (`:50-54`) declares only
0/2/64 for run mode, so the row's `1` meaning is contradicted by the source, and the condition is a
setup/could-not-evaluate in PROTOCOL terms. Counter-invisible: `measure.py:181-183` only checks that
the *usage probe's* code is a token in the map; no write-failure exit is exercised, and 1 is present
as a token anyway.

**F2 — self-test marker is generic and the tally is unpinned (counter-blind).** Cell 5 records
`SELFTEST: n/n on exit 0`; the observed line is `SELFTEST: 30/30`. `measure.py:178-180` compares
only the first whitespace token by substring, and its own fixture accepts a tool printing
`T_SELFTEST: 1/1 pass` (`measure.py:255`). `SELFTEST:` is the last-line marker of at least two other
rows (`tools/pin-disposition.py:1329`, `tools/evidence-disposition.py:3123`, both
`SELFTEST: PASS (n/n)`), so the row records an observable that neither identifies this tool nor
pins its 30 checks: a suite that lost checks while still printing `SELFTEST: k/k` satisfies both the
row and the counter. It is a diagnostic tally rather than help text, so the predicate's wording is
met.

**F3 — `0 clean` conflates probe success with command success.** The measured exit is 0 whether the
traced command succeeded or exited 3 (`command-exit-recorded`, source:913-915). The round-17 row at
SKILL.md:1902 carries the parenthetical that makes this explicit ("the command's exit is in the
receipt"); the promoted round-51 row drops it, so a reader can take `0 clean` as "the command
passed". Documentation compression, not a false code.

**F4 — the three causes listed for 2 are not exhaustive.** Source also returns 2 for "no temp
directory outside root" (`:614`), "strace -y unusable (probe failed)" (`:621`) and "strace launch
failed" (`:635`). The code mapping is right; the enumeration reads as complete and is not.

**F5 — `Pinned values: none` is true, but only for expectation files.** Every expected value is a
literal in `check()`; the selftest tree is `tempfile.mkdtemp(prefix="trace-inputs-selftest-")`
(`:703`) under TMPDIR, and the fixture roots are passed explicitly (`:787-793`). The selftest body
never references `DEFAULT_*`. However `:70-72` hardcodes `DEFAULT_FLEET`, `DEFAULT_LANE` and
`DEFAULT_HOME` as absolute defaults that classify `external`/`live_lane_reads` whenever the caller
omits the flags, and no check exercises those defaults. Not false under the table's convention; an
undisclosed behavioural default.

**F6 — kind, entry and write scope are honest.** `probe` is correct: the tool never grades the
traced command (exit 0 with `exit=3` in the receipt). Entry command runs as written. Write scope
verified: `--out` parents created (`:688`), `trace-inputs-run-*` chosen outside `--root`
(`:575-596`) and deleted in the `finally` (`:693-694`), selftest tree under TMPDIR and removed on
pass. `make_workdir` may fall back to `~/.cache` when TMPDIR is unusable, but the cell only claims
"outside --root" for that dir, which holds.

**F7 — command-specific meaning of "strace missing".** The map's `2` for a missing strace is true in
run mode (measured; also asserted by the selftest check `missing-strace-exit2`, `:851-853`), but the
same condition under `--selftest` yields 1 with `SELFTEST: 5/30`. Two of those five passes
(`temp-workdirs-deleted`, `no-artifacts-inside-root`) are vacuous when no workdir is created. No
undeclared code appears; the row simply does not say its verdict map is command-specific.

## Predicate impact

None for this row. Exit 0 on the self-test, `SELFTEST:` present in the self-test cell, usage probe
64 declared, pinned `none`, 8 cells, `probe`, owner `tameshi` — every clause the counter tests is
satisfied at CAND. C3's overall outcome is unaffected by this vector either way; the known honest
failure belongs to `tools/round21-measure.py`, not here. If the L1 wants a row-quality disposition,
F1 is the only cell that states something false about the tool and should be widened to
`1 failed (selftest check) or the receipt could not be written`; F2 is the only clause that would
survive a suite-size regression, and pinning `30/30` plus a tool-specific id (`TRACE_INPUTS_SELFTEST:`)
would close it without touching the counter.
