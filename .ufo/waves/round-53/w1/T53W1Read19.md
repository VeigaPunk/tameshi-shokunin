# T53W1Read19 — cold read of `### Round-26 gate/probe registry — report interop`

Seat: reader (leaf), round 53 wave 1, lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Subject: SKILL.md section at content commit `a41195dfc13a73958e4c5228ec196b28d03ded03` (C*), read through git objects only.

- Heading line: 2139; section line range: 2139–2178 (1-based, inclusive).
- Section bytes: 40 lines, 22 953 bytes; `section_sha256 = 5399e46663220dea7df1c4ae9dc1b2871150e73aabe007d1371aa2a80e1a8e93`.
- Extraction: `git -C <lane> show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` (whole file 2 178 lines, sha256 `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee`).

## Checks run

1. **Split reproduced against the frozen monitor.** Re-implemented the stated rule (`^#{1,3}(\s|$)` outside ``` fences; heading line to the line before the next heading; trailing whitespace-only lines stripped; joined with `\n`, no trailing newline; sha256 over UTF-8 with `surrogateescape`) → 63 heading lines, my target table is the last (line 2139), section ends at 2178. Then loaded the monitor actually used by the C1 counter, `.ufo/evidence/round-18/measure.py` at C*, via `importlib`, and ran its `sectionize()` over the same blob: it yields 64 sections (63 headings + the preamble before line 6), and for my heading reports `start=2139 end=2178` and `sha256=5399e46663220dea7df1c4ae9dc1b2871150e73aabe007d1371aa2a80e1a8e93` — identical to my own split. The `#### Gate/probe registry — round 51` line inside the section is 4 hashes and is correctly NOT a split point.
2. **Every repo path the section cites exists at C***. Extracted 78 backticked repo-path tokens (`.`/`..`, `<…>` and `…` placeholders excluded) and ran `git cat-file -e C*:<path>` for each: 0 missing (covers every `.ufo/evidence/…`, `.ufo/waves/…`, `tools/…`, `corpus/…` pin, including `tools/vendor/mutation-testing-report-schema-3.9.0.tgz`, `tools/vendor/mutation-testing-metrics-3.9.0.tgz`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`, `.ufo/evidence/round-49/c2/panel.json`, `.ufo/evidence/round-32/heldout/`, `.ufo/evidence/round-40/census/fixtures.json`, `.ufo/waves/round-40/settlement-receipt.json`, `.ufo/waves/round-41/settlement-receipt.json`). No dead receipts.
3. **Selftest tallies, re-executed with `TMPDIR` bound to the seat scratch** (`TMPDIR=/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read19/tmp`), from the lane with the lane's own tools (read-only invocations; all writes go under `TMPDIR`):
   - `registry-check.py --selftest` → `SELFTEST: PASS (51 cases)` (section: 51 cases) — holds.
   - `evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)` (section: 66/66) — holds.
   - `context-capture.py --selftest` → `SELFTEST: PASS (49/49)` (section says 49/49 **cases** — count holds, string does not; see finding 3).
   - `witness-metadata.py --selftest` → `SELFTEST: PASS 39/39` — holds.
   - `repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)` — holds.
   - `bash-witness-study.py selftest` → `WITNESS_SELFTEST: 51/51 pass` then terminal `VERDICT: PASS` — holds (both the tally and the "VERDICT: is the last line, preceded by WITNESS_SELFTEST" ordering).
   - `pbt-staged-id.py --selftest` → `PBT_STAGED_ID_SELFTEST: cases=35 failed=0` — holds.
   - `write-path-census-v4.py --selftest` → `cases=15 failed=0`; `-v2` → `bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`; `-v3` → `var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`; `write-path-census.py --selftest` → `planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1` — all hold, verbatim.
   - `env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`; `receipt-window.py --selftest` → `20/20 pass`; `receipt-measure.py --selftest` → `10/10 pass`; `wave-parent-settle.py --selftest` → `3/3 pass`; `wave-route-mix.py --selftest` → `8/8 pass`; `wave-accounting.py --selftest` → `8/8` + `16/16` + `FINDING: SELFTEST_PASS`; `golden-verdict.py --selftest` → `GOLDEN_VERDICT_SELFTEST: 3/3 pass`; `command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`; `pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`; `registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`; `round21-measure.py --selftest` → `ROUND21_MEASURE_SELFTEST: 13/13 pass`; `tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`; `tally-audit.py --selftest` → `TALLY_AUDIT_SELFTEST: 11/11 pass`; `tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` (315 s). All hold.
4. **Exit-code maps probed** (no-arg / unknown-flag invocations, nothing written): `wave-parent-settle` 2 / 2 (section: 2) · `wave-route-mix` no-arg 64 (section: 64) · `write-path-census-v4` no-arg 2 · `registry-check --bogus` 64, no-arg 2 · `receipt-measure --repo` (missing value) 2 (section: 2) · `staged-id-guard --bogus` 2 · `pbt-staged-id --bogus` 2 · `shrink-case --bogus` 2 · `trace-inputs --bogus` 64 · `command-binding --bogus` 64 · `wave-accounting --bogus` 64 · `receipt-window --bogus` 2 (section: usage folds to 2) · `env-diff --bogus` 64 · `tally-audit-v3 --bogus` 2 · `golden-verdict` no-arg 2. All hold.
5. **Round-26 row internals.** `tools/mte-interop.py` at C* accepts `--check`, `--selftest`, `--workdir`, `--regression-stdout`, `--fleet-root` (default: parent of the checkout), `--emit` (lines 456–461); the check exits `0 if conforming == len(legs) else 1` after raising Setup when `set(legs) != set(LEG_TABLE)` with the message "leg set … differs from the ten ledger legs"; `LEG_TABLE` has exactly 10 entries. `tools/registry.json` at C* carries rows `mte-interop-selftest` (expects `MTE_SELFTEST: 17/17 pass`) and `mte-interop-check` (expects `MTE_INTEROP: PASS legs_conforming=10/10`) — both match the section. `write-path-census.py`'s `GATES` tuple has 21 names — matches "21-name GATES list".
6. **Pinned values.** `tools/context-capture.py:153` carries the literal `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`, with `FROZEN_EXPECTED_ID = "context_consistent"` and `FROZEN_EXPECTED_EXIT = 0` — the section's "literal digest 05cb55b8… and id/exit pin inside the tool" holds. `tools/round21-measure.py:77` does read the `FLEET = Path("…")` literal out of the sibling `c2-count.py` — the "since round 52 … FLEET literal" clause holds.
7. **Settlement receipts replayed.** `wave-parent-settle.py --receipt .ufo/waves/round-40/settlement-receipt.json` → `WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal`, exit 0; `--receipt .ufo/waves/round-41/settlement-receipt.json` → `verdict=UNSETTLED detail=parent_exit_unix missing`, exit 1. Both match the section's recorded pins.
8. **Fix-pass provenance.** `git diff --name-only 6db1d220 C* -- tools/ SKILL.md` lists exactly `SKILL.md` and seven tools: `bash-witness-study.py`, `context-capture.py`, `env-diff.py`, `evidence-disposition.py`, `pin-disposition.py`, `registry-check.py`, `repeat-control.py`. `git diff -U0 6db1d220 C* -- tools/` shows every `dir="/tmp"` replaced by `dir=tempfile.gettempdir()` in those tools; `TMPDIR=<scratch> python3 -c "import tempfile;print(tempfile.gettempdir())"` prints the scratch root, i.e. `gettempdir()` honours `TMPDIR` on this host. This is the evidence behind findings 1, 2, 4, 5, 6, 7.

## Findings

### 1. bash-witness-study row claims the selftest ignores TMPDIR — false at C*

Quote: `selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored)`

At C* the selftest builds its tree with `tempfile.mkdtemp(prefix="bash-witness-selftest-private.", dir=tempfile.gettempdir())` and a contained child with `dir=private_root` (`tools/bash-witness-study.py:1240-1246`). The fix pass changed exactly this line from `dir="/tmp"`. Under `TMPDIR` set the tree is created under `TMPDIR`, so both "hardcoded /tmp" and "TMPDIR ignored" fail. The same row's neighbour statement stays true: the run above printed `WITNESS_SELFTEST: 51/51 pass` with `TMPDIR` bound outside `/tmp`.

### 2. context-capture row names a /tmp fixture path the tool no longer uses

Quote: `selftest fixtures under /tmp/context-capture-selftest-*, removed in finally`

`context-capture.py:1624-1625` at C*: `tempfile.mkdtemp(prefix="context-capture-selftest-", dir=tempfile.gettempdir())`; the tool's own docstring at C* says the scratch root is `tempfile.mkdtemp(dir=tempfile.gettempdir())`. The fix-pass diff shows the `dir="/tmp"` removal for this tool. The path is `${TMPDIR:-/tmp}/…`, not `/tmp/…`, so under the host scratch directive (TMPDIR bound to `$HYAKU_SCRATCH`) the named path is wrong. (The "removed in finally" clause holds: `shutil.rmtree(self.root, …)` runs at the harness teardown, `context-capture.py:1778`.)

### 3. context-capture selftest line documented with a word the tool never prints

Quote: `SELFTEST: PASS (49/49 cases)`

The tool at C* writes `"SELFTEST: PASS ({}/{})\n".format(self.passed, total)` (`context-capture.py:1785`), and the live run printed, verbatim, `SELFTEST: PASS (49/49)` — no `cases`. A reader grepping or asserting the documented string gets no match; the count (49) is right, the exact string is stale. Compare the neighbouring rows, whose shapes match their tools (`SELFTEST: PASS (29 cases)` for repeat-control, `SELFTEST: PASS 39/39` for witness-metadata).

### 4. evidence-disposition row names a /tmp fixture path the tool no longer uses

Quote: `selftest fixtures under /tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure`

`evidence-disposition.py:2351` at C*: `tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir=tempfile.gettempdir())` (fix-pass diff replaced `dir="/tmp"`). Only the `/tmp` clause fails: "removed on pass, kept on failure" holds — the FAIL branch prints `…; fixtures kept at {scratch}` and returns 1, while `shutil.rmtree(scratch, …)` runs only on the PASS path (`evidence-disposition.py:3112-3123`).

### 5. pin-disposition row names a /tmp fixture path the tool no longer uses

Quote: `selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures`

`pin-disposition.py:706` at C*: `tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir=tempfile.gettempdir())` (fix-pass diff removed the `dir="/tmp"`). The tree is `${TMPDIR:-/tmp}/tameshi-r13-pin-disposition-selftest.*`. The rest of the row holds: the live selftest printed `SELFTEST: PASS (19/19)`.

### 6. registry-check row asserts TMPDIR is ignored — false, and contradicted by the tool's own docstring at C*

Quote: `selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored)`

`registry-check.py:766` uses `tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=tempfile.gettempdir())` and the selftest scratch at `:916-918` uses `dir=tempfile.gettempdir()`. The tool's own `--selftest` help text at C* (line 78) reads "fixtures only under the scratch root (TMPDIR), never touches the lane" — so the section's row contradicts the tool it documents. The fix-pass diff shows both `dir="/tmp"` hits replaced, and the same selftest ran green here with `TMPDIR` bound to the seat scratch: `SELFTEST: PASS (51 cases)`.

### 7. repeat-control row names a /tmp selftest scratch the tool no longer uses

Quote: `selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass)`

`repeat-control.py:597` at C*: `tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=tempfile.gettempdir())` (fix-pass diff removed `dir="/tmp"`). "(removed on pass)" holds — `shutil.rmtree(scratch, …)` sits on the PASS path only, FAIL and COULD_NOT_EVALUATE keep the tree (`repeat-control.py:845-861`).

## Other observations (not findings)

- The heading is a round-26 label but the section now carries a `#### Gate/probe registry — round 51` table; that is a naming artefact of the registry refresh, not a false statement, and the 4-hash line is outside the monitor's split rule.
- `tally audit v3` row's `/tmp/tameshi-r4-2-regression.XXXXXX` holds as written: `tally-audit-v3.py:auto_root()` really does `os.makedirs('/tmp/tameshi-r4-2-regression.' + 6 chars)` and removes it via `atexit`; the runner's own auto root at C* is `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX`, but the row attributes the literal path to the audit tool, which is accurate.
- `tally audit v2` row's "/tmp/tally-audit-work" holds: it is a `CONFIGS` root literal in the tool (`tally-audit-v2.py:265`).

## Not independently verified in this seat

- `SHRINK_SELFTEST: cases=21 failed=0` — not executed: `shrink-case.py` imports the generator beside it and its docstring states it may write `tools/__pycache__`, which is outside this seat's write scope.
- The section's "writes only its own scratch" / "lane read-only" write-scope columns were checked only by reading the code paths named above; no fs-level write census was run from this seat.

## Scratch

All work under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read19/`; directory removed before yield (`trap 'rm -rf -- "$S"' EXIT`). No tool installed or upgraded for this seat.
