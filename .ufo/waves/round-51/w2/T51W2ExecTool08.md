# T51W2ExecTool08 — C3 row audit: `tools/mutate-and-run.sh`

Seat: T51W2ExecTool08 (leaf executor) · round 51, wave 2 (falsify) · judged axis: operability · milestone: C3 row falsification.
Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`; candidate `6d8c11e378aa90b12650808e1b79270742935f15`; lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scope: audit only. No source file, row, counter, spec or fixture in the lane/fleet/sibling repos was written. Scratch: `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool08/` (deleted before yield).

## 1. The row under test

`SKILL.md:2138` `#### Gate/probe registry — round 51`, header `SKILL.md:2141`, row **`SKILL.md:2149`** (8 cells, verbatim):

| cell | content (abridged only where quoted below) |
|---|---|
| Name | `fleet mutation runner` |
| Kind | `gate` |
| Entry command | `` `bash tools/mutate-and-run.sh --regression --workdir DIR` `` or `` `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` `` |
| Verdict map | `0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage)` |
| Self-test command | `` `bash tools/mutate-and-run.sh --selftest` `` → finding id `VERDICT:` (terminal line `VERDICT: PASS, after the MUTATE_SELFTEST tally)` |
| Pinned values | `` `corpus/knowledge/fleet-kill-rate-ledger.md` ``, `` `.ufo/evidence/round-18/sources-check/sources-check.defects.spec` ``, `` `.ufo/evidence/round-26/cite-check/cite-check.defects.spec` ``; leg sha256 pins and verdict tables are literals in the tool |
| Write scope | `caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show` |
| Owner | `tameshi` |

Full cell text: `row-2149.txt`. Tool at candidate: `tools/mutate-and-run.sh`, 2159 lines (`VERSION='mutate-and-run.sh r10-2 …'`, `runner.sh:194`).

## 2. Method

- `git clone --shared --no-checkout` of the lane in scratch, `checkout --detach <CAND>`; `git rev-parse --show-toplevel` = `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool08/clone` asserted before every run (`fleet2/tameshi-shokunin` likewise for the fleet-layout run). All runs: `cwd` = that clone, `stdin = /dev/null`, `TMPDIR` = a seat scratch dir, `pty` off.
- The row's **exact backticked self-test** and the counter's usage probe (`--r51-no-such-flag`, counter form: interpreter prefix + tool + flag) were executed directly, then replayed through the frozen counter's own functions (`measure.py::row_reason` / `run_row`, imported read-only).
- Row fields checked against source (`git show <CAND>:tools/mutate-and-run.sh`), plus targeted run-mode probes to pin exit-code meaning.
- Repo reads via `git -C … show <rev>:<path>` only; sibling repos read-only.

## 3. Direct measurements (receipts in `T51W2ExecTool08/`)

| # | command | exit | last stdout line | wall |
|---|---|---|---|---|
| 1 | `bash tools/mutate-and-run.sh --selftest` (row's exact self-test) | **0** | `VERDICT: PASS` (preceded by `MUTATE_SELFTEST: 107/107 pass`) | **6.19 s** (precise timer; first, cold call 12.08 s) |
| 2 | `bash tools/mutate-and-run.sh --r51-no-such-flag` (usage probe) | **64** | (stdout empty) stderr first line `mutate-and-run: unknown argument: --r51-no-such-flag` | 0.01 s |

- `selftest.stdout` / `selftest.stderr` / `selftest.exit`; `usage.stdout` / `usage.stderr` / `usage.exit`; cold-run copy `selftest-coldrun.stdout`.
- First token of the terminal line is `VERDICT:`, which occurs in the row's Self-test cell ⇒ the counter's finding-id check passes. The marker is the tool's own verdict line (`runner.sh:2125-2127`), not help text, and the row also names the `MUTATE_SELFTEST` tally that immediately precedes it.
- After both runs the clone was clean (`git status --porcelain` → 0 lines): the selftest writes no lane path.
- Counter replay (`rowcheck.txt`): `row_reason` → `None`; `run_row` → `None`, `last: VERDICT: PASS`. **The frozen C3 predicate accepts this row.** Note the section has four rows whose Entry cell contains `tools/mutate-and-run.sh` (2149, 2160, 2161, 2162); only 2149 is accepted — 2160-2162 fail `selftest-argv-not-the-tool` (substring matching), which is harmless.
- The known C3 blocker in the brief (row16 `tools/round21-measure.py --selftest` exiting 1 from a fresh clone because its fixture expects sibling fleet repos) **does not apply to this row**: cell 1 above is clone-safe, exit 0, no sibling repos needed.

### 3.1 Exit-code audit (against `runner.sh:78-82, 250-256, 578-588, 1521-1549`)

| code | row says | measured | command |
|---|---|---|---|
| 0 | `clean` | run mode: `MUTATE: DONE (target=probeK defects=2 killed=2 survived=0 inconclusive=0 kill-rate=100%)`; **also** `MUTATE: DONE (target=probeS … killed=0 survived=2 … kill-rate=0%)` | `probes/A.out`, `probes/B.out` |
| 0 | `clean` | regression mode: `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0 | `probes/RgFleet.out` |
| 1 | `failed (run mode prints DEGRADED …)` | `MUTATE: DEGRADED (target=probeDg defects=2 killed=0 survived=1 inconclusive=1 kill-rate=0%)` (timeout → INCONCLUSIVE) | `probes/Dg.out` |
| 2 | `could-not-evaluate (setup/refusal)` | `MUTATE: SETUP (control run on the pristine copy is red (exit=124) …)`; `APPLY FAIL id=D line=1 old-string-count=3 expected=1` + `MUTATE: SETUP (spec/preparation failed for 1 defect(s); no suite run)` | `probes/C.out`, `probes/Dup.out` |
| 64 | `could-not-evaluate (usage)` | `--r51-no-such-flag` → 64; `missing --target` → 64 | `usage.exit`, `probes/E.out` |

No undeclared exit code was found: the tool's own exits are exactly `0/1/2/64` (`runner.sh:250,255,583,587,1523,1529,1548`), and suite-level `124/126/127` are folded into `INCONCLUSIVE` (`runner.sh:556-558`) rather than leaked. Regression-mode exit 1 (leg out of band) was not induced independently — it is asserted by the tool's own selftest (status-1 arms at all ten positions, `selftest.stdout`) and by `runner.sh:1521-1526`.

### 3.2 Entry-command operability (both cells)

- Run mode (`--target/--defects/--suite --workdir`) measured end-to-end: 100 % kill sweep, survivor sweep, DEGRADED sweep, refusal (`probes/A,B,Dg,Dup,E.out`). Target never written: mutants are copies in `--workdir` (`runner.sh:500-501,525-526`); `MUTATE_RESTORE: OK (target-sha256 before=… after=…)` reproduced.
- Regression mode in the intended layout (clone placed beside the four owner repos, exactly the layout `--regression` requires): **exit 0 in 214 s**, `REGRESSION: PASS (cases=10 passed=10 …)`, terminal line `REGRESSION_WORKDIR: … (kept)` (`probes/RgFleet.out`). Leg pins verified against owner-repo blobs: `PIN_DRIFTPINS=c138d34c…` = sha256 of `kagi-shokunin:corpus/drift-pins.sh@e64e81b8`, `PIN_SOURCESCHECK=6a293a72…` = sha256 of `kumitate-shokunin:scripts/sources-check.mjs@0acb7752` (`spec-and-pins.txt`).
- Regression mode from a **bare clone** (no fleet siblings): **exit 2**, `REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)`, ten `REGRESSION_CASE …: SETUP (repo_identity_mismatch: … is not its own repository; toplevel=unresolved)` lines (`probes/Rg.out`), because `FLEET_ROOT=$(dirname³ "$SELF")` (`runner.sh:1430`). See finding F3.

## 4. Row-field audit against source

| cell | verdict |
|---|---|
| Kind `gate` | Upheld for `--regression` (exits 1 when a leg is out of band, `runner.sh:1521-1526`). In **run mode**, exit 0 does not encode a verdict — a 0 %-kill sweep exits 0 (`probes/B.out`). See **F2**. |
| Entry command | Both forms exist and work as written; `--regression` additionally requires the fleet layout (**F3**). |
| Verdict map | Codes complete (`0,1,2,64`, no undeclared code). Semantics imprecise in run mode: the tool's own header says `0 done · 1 done-with-inconclusive (DEGRADED)` (`runner.sh:81`), not `0 clean / 1 failed` (**F2**). |
| Self-test command | Exact, metacharacter-free, single backticked command; exits 0 from a clone at CAND; terminal marker true (**§3**). |
| Pinned values | All three named paths exist at CAND; each is byte-identical to the corresponding embedded heredoc spec (`js-sources-check` = round-18 sha `c8d24cb4…`, `js-cite-check` = round-26 sha `969f50d6…`); the cell also discloses that the behaviour-bearing pins are literals. They are **provenance only** — no runtime read (only comment hits in `runner.sh`). The **tenth leg's spec source is missing** from the cell (**F1**). |
| Write scope | Substantially true: no lane write (clone porcelain 0); target never written; fleet repos touched only with read-only verbs through `git_clean` (`rev-parse`, `cat-file -e`, `show`, `ls-tree`; no checkout/clone/write). Two inaccuracies: `/tmp` vs honoured `TMPDIR` (**F4**), and it omits that the `--regression` scratch root is kept on FAIL/SETUP and whenever `--workdir` was given (`runner.sh:148-152,1541-1548`). |
| Owner `tameshi` | Correct. |

## 5. Findings (ranked; none block C3's frozen predicate for this row)

**F1 (medium, row content — stale by one leg).** The Pinned-values cell names the spec sources of legs 8 and 9 (round-18 `sources-check`, round-26 `cite-check`) but **not** the tenth leg's source, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`, which `runner.sh:104` names as leg 10 and which is byte-identical to the embedded spec (sha256 `a98271f6…`, exists at CAND). The leg C2 adds this round is the one the cell does not pin. A truthful cell would add that path (existence-verified), or say "legs 1-7 use inlined specs; legs 8/9/10 from these three paths".

**F2 (medium, verdict-map semantics).** `0 clean` is exact only for `--regression`. Measured run-mode result with a suite that asserts nothing: `killed=0 survived=2 inconclusive=0 kill-rate=0%`, **exit 0** (`probes/B.out`) — i.e. a sweep in which every mutant survives is "clean" under this row, while the tool's own header calls run-mode 0 `done` (`runner.sh:81`) and run-mode 1 `done-with-inconclusive (DEGRADED)`, not `failed`. The mutant verdicts live in the printed table, so the row should distinguish the two modes (regression: 0 all legs PASS · 1 leg out of band; run: 0 sweep done · 1 sweep done with an inconclusive).

**F3 (low-medium, operability, entry command).** `--regression --workdir DIR` is not clone-portable: `FLEET_ROOT` is derived positionally as `dirname³(SELF)` (`runner.sh:1430`), so from a clone at CAND all ten legs refuse `repo_identity_mismatch` and the mode exits 2 (`probes/Rg.out`); in the fleet layout it exits 0 with `REGRESSION: PASS (cases=10 passed=10)` in 214 s (`probes/RgFleet.out`). This is the same class as the known row16 clone-context failure, but limited to the entry command: the row's declared **self-test is clone-safe**, so C3's predicate is unaffected. The row does not state the precondition.

**F4 (low, write-scope precision).** The cell says "auto mktemp under /tmp" and "selftest under /tmp". The tool honours `TMPDIR` in all three scratch roots — `runner.sh:491` (run), `:1432` (regression), `:1555` (selftest) all use `${TMPDIR:-/tmp}`, and the r51 header states it (`runner.sh:148-150`). Measured: with a read-only `TMPDIR` the selftest refuses `mktemp: failed to create directory via template '…/tameshi-r4-2-selftest.XXXXXX': Permission denied` → `VERDICT: FAIL (mktemp)`, exit 1 (`probes/tmpdir-ro.out`), while successful runs wrote their scratch inside the seat `TMPDIR`. Since the counter itself runs the selftest with `TMPDIR=work/tmp`, the row's `/tmp` wording is contradicted by the invocation that grades it. Neighbouring rows in the same table distinguish "TMPDIR-respecting" from "hardcoded /tmp (TMPDIR ignored)".

**F5 (observation, not a mismatch).** `VERDICT:` is the genuine terminal line and is anchored by the row's own reference to the `MUTATE_SELFTEST: 107/107 pass` tally; it is nonetheless a generic token shared with other tools (e.g. `staged-id-guard`), so the marker alone would not identify the tool. Also: four rows in the section mention `tools/mutate-and-run.sh`; only `SKILL.md:2149` is accepted by the counter — the other three are rejected by `selftest-argv-not-the-tool`, which shows the row matcher is substring-based.

## 6. Limits of this audit

- Regression-mode exit 1 (a leg out of band) was not induced independently (would require doctoring the embedded table, i.e. editing the tool); it rests on the tool's own selftest arms and `runner.sh:1521-1526`.
- "Fleet leg repos read-only" was checked by source (read-only git verbs) and by layout, not by a before/after census of the sibling trees (they are concurrently used by other seats).
- No claim made about the correctness of the ten recorded verdict tables (C2's subject) beyond their reproduction here (`REGRESSION: PASS`, 10/10) and the pin checks.
- Three empty `/tmp/tameshi-r4-2-regression.*` dirs (23:03) were not created by this seat (all of my runs passed `--workdir`); left untouched.

## 7. Disposition

The row is **operable and truthful in the fields C3 tests**: self-test exits 0 from a clone at CAND with the declared marker, usage probe exits a declared code, kind/owner/pin-existence/write-scope hold, and no undeclared exit code exists. Four row-level mismatches are reported above (F1 stale pinned-values cell, F2 "0 clean" overstating run mode, F3 undocumented fleet-layout precondition of the entry command, F4 `/tmp` vs honoured `TMPDIR`); F1-F4 are disclosure/precision defects, not fabrications, and none makes the row fail the frozen counter. No repair was made (seat bounds: no source/row edits).
