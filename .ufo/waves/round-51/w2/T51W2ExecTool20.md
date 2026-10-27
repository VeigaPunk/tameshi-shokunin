# T51W2ExecTool20 — independent audit of the C3 registry row for `tools/tally-audit-v3.py`

Seat T51W2ExecTool20 (executor, round-51 wave 2). Item: falsify the round-51 SKILL.md registry row for
`tools/tally-audit-v3.py` at content candidate `6d8c11e378aa90b12650808e1b79270742935f15`.
Read-only on the lane; the only lane paths this seat wrote are this report and
`.ufo/waves/round-51/w2/T51W2ExecTool20/`. No source or row edit, no tool install, no git/jj mutation in
lane/fleet/sibling repos (the lane was exercised through a `git clone --shared` in scratch whose
`rev-parse --show-toplevel` printed the clone).

- Row audited: `SKILL.md:2161`, inside `#### Gate/probe registry — round 51` (`SKILL.md:2138`).
- Tool: `tools/tally-audit-v3.py` (946 lines, blob `2fcd41518af50200d41c33baf64e85ada4e1f4ce`, equal to the
  CAND blob). Audited runner `tools/mutate-and-run.sh` (blob `51fa5bc8ac2c863ec754ac87a1e3227a18c79d67`,
  equal to the CAND blob).
- Scratch: `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool20` (clone `$S/lane` at CAND, `TMPDIR=$S/tmp`),
  deleted before yield. Receipts retained in `.ufo/waves/round-51/w2/T51W2ExecTool20/`.

## 1. Verdict

**Every audited field of the row is true of the source at CAND; the row's self-test and usage probe behave
exactly as the row states.** The row is a gate, not a probe; its pinned values are load-bearing; its write
scope is accurate; its last-line marker is a computed diagnostic, not help text.

**One operability finding, measured, not repaired:** the row's self-test takes 577 s standalone against the
C3 counter's 900 s per-row cap, and a replay through the counter's own `run_row` at wave-level contention
returned `selftest-exit=124 last=timeout` (900.0 s). The row is therefore budget-critical: under a busy
deciding run the counter can score this tool `missing` while every row field remains true. Detail in §5.

## 2. Measurements (all from the CAND clone, stdin `/dev/null`)

| # | probe | exit | wall | last stdout line |
|---|---|---|---|---|
| 1 | `TMPDIR=$S/tmp python3 tools/tally-audit-v3.py --selftest` | **0** | **577 215 ms** | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` |
| 2 | `… --r51-no-such-flag` | **2** | instant | — (stderr: `tally-audit-v3.py: error: unrecognized arguments: --r51-no-such-flag`) |
| 3 | `… --runner tools/mutate-and-run.sh` (row entry command) | **0** | 26 705 ms (2nd run 24 859 ms) | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| 4 | `… --runner $S/base-runner.sh` (nine-leg base runner) | **1** | 18 613 ms | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` |
| 5 | `… --runner $S/broken.sh` (`not a runner`) | **2** | instant | `TALLY_AUDIT: SETUP (run_regression() not found)` |
| 6 | `… --runner $S/noharness.sh` (`local tblock` line removed) | **2** | ~26.1 s | `TALLY_AUDIT: SETUP (selftest tally harness (`local tblock`) not found)` |
| 7 | `… --help` | 0 | instant | `  --workdir WORKDIR` (marker absent) |

Run 1: stdout 1 453 B, 35 `CASE … PASS` lines, stderr 0 B. Run 3: `CHECK runtime PASS vectors=36576
mismatched=0`, `CHECK harness PASS reference cases=9; faults rejected=36/36`.

## 3. Field-by-field against source

**Kind `gate` — true.** The tool grades and fails: a foreign (nine-leg) runner is rejected with exit 1 and
`CHECK harness FAIL leg names differ from the reference panel (st_js … st_citecheck)` (probe 4). It is not a
probe: the four checks each produce PASS/FAIL and the verdict is their conjunction (`audit()`,
`tools/tally-audit-v3.py:759-780`).

**Entry command — true.** `python3 tools/tally-audit-v3.py --runner tools/mutate-and-run.sh` exits 0 with
`TALLY_AUDIT: PASS` on the candidate runner (probe 3), on the same runner the C2 ledger's tenth leg lives in
(the pin `local nlegs=10 … st_driftpins` is at `tools/mutate-and-run.sh:1510-1511`).

**Verdict map `0 clean; 1 failed; 2 could-not-evaluate (SETUP: runner unparsable, tally harness structure
missing, or argparse usage)` — true, and complete for the observed paths.**
- 0: probe 3. 1: probe 4. 2: probes 2, 5, 6, each with the parenthetical's own words
  (`run_regression() not found`; `selftest tally harness (`local tblock`) not found`; argparse
  `unrecognized arguments`). `main()` (`:926-946`) maps `CannotAudit`/`OSError`/`UnicodeDecodeError`/
  `ValueError` to 2 (`:937-939`); argparse itself exits 2; the only other published code,
  `--then-regression`'s 124, is folded to 2 (`:784-803`). No exit 64 exists in this tool, and the row does
  not claim one.

**Self-test cell — true.** Command `python3 tools/tally-audit-v3.py --selftest` has no shell metacharacter;
exit 0; the last non-empty stdout line is exactly the recorded marker. The panel is 33 runner-mutation cases
plus 2 `code_view` cases, `total = len(cases) + len(code_view_cases)` (`:921`), printed at `:922`; all 35 pass
and every case is named in the receipt (`selftest.out`). **The marker is a real diagnostic, not author help
text:** it is computed from `passed == total` and the function returns 1 when they differ (`:923`); `--help`
exits 0 with last line `  --workdir WORKDIR` and contains no occurrence of `TALLY_AUDIT_V3_SELFTEST` (probe
7). The counter's marker test (`last.split()[0]` = `TALLY_AUDIT_V3_SELFTEST:`) therefore cannot be satisfied
by the help path.

**Pinned values — true and load-bearing.**
- `REF_BLOCK` (`:102`) and `REF_NAMES` (`:142-143`) are the ten-leg reference block/panel, including
  `st_driftpins`. They are not decoration: `check_harness` rejects any runner whose leg names differ
  (`:741` — probe 4), and `REF_BLOCK` is the block injected into the runner's own harness as the case it
  must accept (`:714-735`, `check_harness` `:740-757`); the 36-fault panel is derived from it (`faults()`, `:645-693`, audit
  reported `faults rejected=36/36`). The nine→ten pin change is the only semantic change to the tool between
  base and CAND (diff confined to leg count and the seeds keyed on it).
- `.ufo/evidence/round-32/heldout/` exists at CAND (22 files; every held-out name the tool cites,
  e.g. `HeldOutPrintf-1`, `HeldOutGuard-1`, `HeldOutLoop-1/-3`, `HeldOutRefactor-a3/-a4`,
  `HeldOutTallyArms-01`, has a file). It is **not read at run time**: the strace of one audit contains no
  `openat` of that path, and the only lane file opened at all is the runner (75 opens), as the row says.

**Write scope — true, verified by syscall trace.** `strace -f` over one full audit (134 526 lines,
`audit.strace.gz`): the only lane paths opened are `tools/mutate-and-run.sh` (read, 75×), the tool itself and
`tools/`; **zero** `openat` with `O_CREAT|O_WRONLY|O_TRUNC` under the lane. Writes are all inside `TMPDIR`
(`audit()` scratch `:766`; one `stderr.N` side file per vector per config, ~36 576 files per audit, `:456`;
harness roots `$TMPDIR/h.XXXXXX`) plus the one hardcoded auto root the row discloses. The auto root's life is
`mkdir(/tmp/tameshi-r4-2-regression.OXOqs8)` → `unlinkat(…, AT_REMOVEDIR)` by the *audited* block's own
`rm -rf "$root"` under the auto/KEEP=0 config → re-`mkdir` → final `rmdir` at interpreter exit; the path is
gone afterwards. `auto_root()` is at `:407-433` (the `/tmp` literal at `:422`, the `atexit` removal at
`:427`), exactly as the row words it. The audited runner is never opened for write and `git status
--porcelain` in the clone stays empty after every run.

**Owner `tameshi`, 8 cells, row shape — accepted by the counter's own parser.** Importing
`.ufo/evidence/round-51/c3/measure.py` from the clone: `line 2161 cells=8 kind=gate owner=tameshi
row_reason=None argv=['python3','tools/tally-audit-v3.py','--selftest'] usage=[…,'--r51-no-such-flag']`
(`row-parse.txt`). Its pinned-path test passes: `git cat-file -e` returns 0 for `tools/mutate-and-run.sh`
and `.ufo/evidence/round-32/heldout/` (`pinned-paths.txt`).

## 4. What I could not falsify

- The row does not mislabel a probe as a gate, does not hide an exit code the tool can produce, does not
  claim a write outside the traced scope, and its self-test works from a fresh `--shared` clone with no
  sibling fleet repo (unlike the known `tools/round21-measure.py` clone-context blocker; this tool reads only
  its own sibling runner).
- Nothing in the row was amended by wave 1 and nothing here needs a row repair.

## 5. Operability finding the L1 should weigh before the deciding run

The C3 counter runs each row's self-test under `run_cmd(..., 900)` with
`concurrent.futures.ThreadPoolExecutor(max_workers=6)` (`.ufo/evidence/round-51/c3/measure.py`,
`run_row`/`measure`). This row's self-test is by far the heaviest thing it runs:

| condition | measurement |
|---|---|
| self-test, one at a time (`TMPDIR` on `/fast`, xfs) | exit 0 in **577.2 s** (64 % of the 900 s cap) |
| one audit, solo | 24.9 s / 26.7 s |
| six audits concurrently (counter's worker count) | 32.4 s each (1.30×) → a 6-worker self-test projects to ≈750 s [INFERENCE from the measured per-audit scaling] |
| **replay through the counter's own `run_row`** (23:32–23:47) | **`selftest-exit=124 last=timeout` at 900.0 s** |

The replay's timeout is contention, not row falsity: at that moment the host carried load ≈39–44 on 32 cores
and five other wave seats (`T51W2MutC3Counter` ×2, `T51W2ExecC2Replay`, `T51W2ExecFinalCounters`,
`T51W2ExecTool07`) were running the *same* self-test, each spawning its own audit children
(`counter-run-budget.txt`; my replay added one more such load). A quiet straightforward run is the 577 s
pass. Consequence: **a `124` on this row at the deciding run is a harness-budget artifact, not evidence that
the row is untrue**; the L1 should either run the C3 counter on a quiet host or expect this row to be the
first to hit the cap. I make no recommendation to change the row, the counter or the rule.

## 6. Disclosures and limits

- `/tmp/tameshi-r4-2-regression.*` showed 4→7 directories while the wave was busy. That residue is from
  concurrent or killed audits across seats, not from this tool's normal exit: the traced run's path was
  created and removed (`strace-autoroot-lifecycle.txt`), and an isolated `auto_root()` call created
  `/tmp/tameshi-r4-2-regression.b9oBje`, with the directory count unchanged after interpreter exit and the
  path absent. A SIGKILL (for example the counter's 900 s timeout) would leave one behind because `atexit`
  does not run — not exercised, [INFERENCE].
- Row wording nits, not mismatches: the "35 seeded-case panel" is 33 runner-mutation cases plus 2 extractor
  (`code_view`) cases; "one auto-root dir … allocated" is one *path*, allocated twice within a sweep because
  the audited block itself deletes it under the auto/KEEP=0 config (`:402`, `:407-433`, trace lines
  161/176/27602/134525).
- Self-test cost shape: each audit writes ~36 576 zero-byte `stderr.N` files in `TMPDIR` (`:456`); the
  self-test therefore creates and deletes ~1.2 M files. That is inside the declared scope and cleaned up,
  but it is the reason the row is filesystem-sensitive.
- At audit time the lane working tree carried an uncommitted `M SKILL.md` (not this seat's write; the wave's
  integration edits it). Every cited byte here comes from the `--shared` clone checked out at committed CAND,
  so the working-tree modification was never read and does not affect any measurement.
- No `## Reader` heading was assigned to this seat, so no cold-read section is re-keyed here.
- Scratch (`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool20`) removed after the receipts were copied; the
  full 13 MB strace is retained gzipped (604 kB) and every measurement is reproducible from `commands.txt`.

## Retained evidence (`.ufo/waves/round-51/w2/T51W2ExecTool20/`)

`selftest.out` (35 CASE lines), `selftest.err` (0 B), `usage.out/.err`, `entry.out/.err`,
`entry2.out`, `base-runner.out/.err`, `broken.out/.err`, `noharness.out/.err`, `help.out`,
`strace-entry.out/.err`, `audit.strace.gz` (full trace), `strace-lane-inputs.txt`,
`strace-lane-write-count.txt` (`0`), `strace-autoroot-lifecycle.txt`, `row-parse.txt`,
`pinned-paths.txt`, `blob-identity.txt`, `counter-replay.out/.err`, `counter-run-budget.txt`,
`measurements.txt`, `commands.txt`.

## Summary

The `tally audit v3` row is truthful in all eight cells: it is a gate, its entry command passes (exit 0,
26.7 s), its verdict map's 0/1/2 are the codes the tool emits with the stated meanings (verified on five
probes), its pins (`REF_BLOCK`/`REF_NAMES`, ten legs including `st_driftpins`) decide verdicts (nine-leg
runner → FAIL), its write scope is exactly `TMPDIR` scratch plus the disclosed `/tmp` auto root (strace, zero
lane writes, blobs unchanged), and its last-line marker is computed by the 35-case self-test and cannot be
produced by `--help`. The self-test exits 0 with `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` in 577 s. The one
operability risk is that 577 s against the counter's 900 s cap, six workers: a replay through the counter's
own `run_row` under wave contention timed out at 900 s (124), which would score the row `missing` for budget
reasons alone.
