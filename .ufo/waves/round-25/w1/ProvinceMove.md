# F1 report interop: what must land for "held", and what stays open

Seat: TameshiR25.ProvinceMove (reviewer, leaf; no subagents). Judged on: coverage.
Scope: the planned frontier move F1 in `corpus/README.md:78` and `:111-114`, and the Core gate in `PROVINCE.md:40-42`.

Pins observed (read-only):
- Contract revision `c9ff09fb` is an ancestor of git HEAD `5b69fb2` (`git merge-base --is-ancestor`: yes). The lane is a colocated jj workspace, so git HEAD is not authoritative (`corpus/SOURCES.md` S061, S076). I did not run jj, because jj snapshots write.
- `tools/mte-interop.py` committed blob: `311448d9…` (same at `c9ff09f` and `5b69fb2`; equals contract amendment-1 `tool_sha256_now`).
- `tools/mte-interop.py` working tree: UNCOMMITTED (`git status`: ` M`). Its sha changed three times during this review: `26e17116…`, then `e0c5f2f3…`, then `8c24255c…` (latest; `git diff --stat` against `c9ff09f`: +121/-42). Figures below are pinned to the sha stated.
- Frozen contract tool `58a5ae92…` is the blob at `2a97ec1` (verified).

## Verdict

F1 is partly held today. The planned counter alone does not make it held.

F1 can be read as held this round only for a narrowed claim: tameshi's recorded verdicts serialize into schema-valid mutation-testing-elements reports, and the official 3.9.0 scorer reproduces their killed, valid and invalid counts. That claim is reachable only after the seven items in section 2 land at one committed tool revision.

NoCoverage stays open under every outcome. It is outside the frozen C2 statement (`contract.json`, claim C2), the ledger cannot measure it, and it does not change the C2 score. I recommend rewriting the F1 row so its next move is the NoCoverage measurement (call it F1b). If the planner keeps NoCoverage inside F1, F1 stays partly held.

## 1. What the frontier text says now

- `corpus/README.md:78` (F1 row): status `held (round 1) — knowledge/mutation-score-semantics.md`; next move "emit one ledger leg as schema JSON and validate it (validator unavailable this round: U)".
- `corpus/README.md:111-114` (correction): "F1 — partly held", because no leg was emitted or validated and "NoCoverage candidates stay U".
- `corpus/README.md:60` (coverage map): the entry is listed with "NoCoverage candidates left U".
- `PROVINCE.md:40-42`: ground moves to Core only through an admitted, source-headed `knowledge/` entry whose `source:` cites a `mined` `SOURCES.md` row. There is no round-25 Core append yet (`grep -n 'round 25\|round-25\|Round 25' PROVINCE.md` returns nothing). The round-21 Core append is the pattern to copy.
- The README rule says a ground reads `held` only when its next move is measured. The minimum bar is therefore one leg emitted and validated. The frozen C2 bar is stronger: 8/8 legs, score, and counts. I treat the C2 bar as the admitted scope.
- `corpus/knowledge/mutation-score-semantics.md:73-77` (O/I/U): U says "No report JSON was emitted or schema validation claimed". The errata block at `:79-81` says "none". Its header cites S001, S002, S004, S005, S006 (all mined).

Note: the score formulas at `mutation-score-semantics.md:23` and `:29` now have source-level confirmation (section 5, scorer arithmetic).

## 2. What must land this round for "held"

1. **One committed tool revision, one pin.** Committed `311448d9` has a count-only judge (`tools/mte-interop.py:203-219`). The working tree adds identity checks (`per_mutant`, `:249`) and runner-measured ledger checks (`:243-247`). Amendment-1 says "judge logic and the selftest are unchanged". That is true for `c9ff09f` against `2a97ec1` (verified by diff: only `--fleet-root` plumbing changed), but it is false for the working tree. Either commit the hardening under a new amendment (new sha, judge and selftest changes named) or revert it. The counter and selftest must run on the admitted sha only.
2. **Counter PASS at that sha.** `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` must print `MTE_INTEROP: PASS legs_conforming=8/8` with exit 0. The `--emit` output and stdout must be retained under `.ufo/evidence/round-25/` and cited as evidence ids. Nothing like that exists yet (`round-25/` has only `c2-before.json` for C2). I did not run it (section 6).
3. **Selftest PASS at the same sha, retained.** Observed by me in `/tmp` scratch: committed `311448d9` gives `MTE_SELFTEST: 10/10 pass`, exit 0. Working tree `8c24255c…` (latest) gives `MTE_SELFTEST: 16/16 pass`, exit 0; the same 16/16 was observed at `e0c5f2f3…`.
4. **Scorer provenance row.** Open S086 (the next unused id, `corpus/SOURCES.md:307`) for `mutation-testing-metrics` 3.9.0. Anchor: tarball sha256 `ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548`; sha512 as pinned in the tool's `PACKAGES`; quoted lines `dist/src/calculateMetrics.js:169-193` (`toMetrics`). Today no row mentions the library (`grep -rn 'mutation-testing-metrics' corpus/` returns nothing). The row may be `mined` only after the quotes are retained.
5. **Schema identity recorded.** S002 (mined; master, fetched 2026-10-19) is byte-identical to the vendored 3.9.0 `package/src/mutation-testing-report-schema.json`: both sha256 `404575e9264686dbf85c399f6531fdb489bebc3146e7e1d793b8083bc6a041ae` (`cmp`: IDENTICAL). The entry should state this. No new row is needed for the schema bytes.
6. **Admission.** A new knowledge entry (preferred), or an append-only round-25 block in `mutation-score-semantics.md`. Its `source:` header cites S002, S086 and S001. It needs `verified-at:` and `recheck:` lines (QUALITY rule 10). Its O/I/U section must be updated, the U text removed, and the NoCoverage list of section 3.1 included. Re-run `.ufo/evidence/kaika-round-1/sources-census-v2.sh` from the lane root; it must print `SOURCES_CENSUS: CLEAN`. S086's `used-by` must name the entry, and the entry must contain the string "S086".
7. **Status surfaces.** Rewrite the `corpus/README.md:78` row so it no longer says "held (round 1)" with a stale U next move. Add a round-25 coverage-map row, as rounds 12 to 24 did. Supersede `:111-114` with an appended line. Add a "## Core — round 25 append" to `PROVINCE.md`, naming the entry and its scope, and stating that NoCoverage and universal interop are excluded (round-21 pattern).

## 3. What stays open

### 3.1 NoCoverage (the open part asked about)

- **Scope.** The eight committed legs record 85 verdicts: 50 KILLED and 35 SURVIVED (`tools/mutate-and-run.sh:613-620`, the `TABLE_*` lines). All 35 survivors stay U:
  - js-kimi-census (2): D2, D10
  - bash-surface-census (2): B5, B10
  - bash-tsukuroi-census (4): B7, B8, B9, B10
  - bash-mado-verify (6): D3, D5, D7, D8, D9, R1
  - bash-checklist-run (8): A1, B1, B3, C1, D1, E2, F2, G1
  - js-claims-check (3): D7, D8, D9
  - js-round-gate (5): C1059, A2, B2, CKIND, E1
  - js-sources-check (5): S_KIND, S_VERDICT, S_DUP_LINE, S_ENTRY_COUNT, S_FILE_READ
- **Named candidates today.** The entry names 8 (`mutation-score-semantics.md:55-67`, table rows at `:61-65`): B5; B8, B10; D5, R1; F2, G1; D9. It does not mention legs 7 and 8 (js-round-gate, js-sources-check), and it omits kimi D10. As written it under-lists the open set by 27 survivors. Legs 7 and 8 also lack a recompute; from their `TABLE_*` lines each is 5/10 (50%), which the counter will reproduce.
- **Why it is open.** No leg has coverage traces. The emitter already records each mutant's 1-based span (`leg_report` location), so the join is mechanical once coverage exists. A survivor is NoCoverage only if its mutated span is never executed by the leg's suite on the pristine target. The granularity must be stated: line or statement, with bash traced and JS covered with node coverage.
- **Why it does not block the C2 score.** The library counts NoCoverage in the undetected total (`calculateMetrics.js:171`). A Survived-to-NoCoverage relabel therefore leaves `mutationScore` unchanged (`:189`). Only the covered-code score (`:191`) and the survived and NoCoverage counts move. The frozen C2 statement does not mention NoCoverage.
- **Guards.** The working-tree ledger arm compares survived counts (`:243-247`), so an unevidenced relabel would be caught there. The committed judge compares only killed and valid counts (`:211-212`), so it cannot see Survived-to-NoCoverage. A sibling note (`C2Tautology.md:71`) reports the same.

### 3.2 Other parts that stay open after "held"

- **Covered-code score** (`mutationScoreBasedOnCoveredCode`): needs n NoCoverage. Open.
- **Timeout.** Tameshi never emits `Timeout`. A suite timeout (exit 124, `mutate-and-run.sh:539`) becomes INCONCLUSIVE and is emitted as `RuntimeError`, which the library excludes from the score (`calculateMetrics.js:174`). Stryker counts Timeout as detected (`:170`). So the emitted report follows tameshi's policy for timeouts, not Stryker's. The rejected rule "timeout counts as a kill" stays rejected.
- **INCONCLUSIVE mapping.** The mapping collapses exit 124 (timeout), 126 (not executable) and 127 (not found) (`mutate-and-run.sh:539-541`). `leg_report` keeps only `tameshi verdict INCONCLUSIVE` in `statusReason` (committed `tools/mte-interop.py:140`; working tree `:157`), so the exit code is lost. None of the 85 recorded verdicts is INCONCLUSIVE, so the mapping is exercised only by a synthetic selftest case.
- **Pending, Ignored, CompileError.** No tameshi verdict maps to them. Open.
- **killedBy, coveredBy, testsCompleted.** Not emitted. Open.
- **Other tools' formats** (mutmut, cargo-mutants, shmutant): no report is emitted. Open and out of C2.
- **Scope bound.** Tameshi's eight hand-seeded legs only. No Stryker run, no producer authentication, no general interop claim.

## 4. Findings by severity

**F-1. Blocker for "held": the tool pin is moving.** The working tree differs from the committed revision, and its sha changed three times during review (`26e17116`, `e0c5f2f3`, `8c24255c`). Remedy: section 2 item 1.

**F-2. Blocker for "held": the scorer has no SOURCES row.** No row covers `mutation-testing-metrics` 3.9.0, and the entry cannot cite it. Remedy: S086 (section 2 item 4).

**F-3. High: the committed judge accepts a balanced identity swap.** I built a probe (`/tmp/r25-f1/balanced_probe.py`). It takes a report in which two mutants' statuses are swapped, so the counts are unchanged but the identities are wrong. This is what a mapping bug would produce.
- Committed `311448d9`: `judge_ok=True`, official killed 2, survived 1.
- Working tree `8c24255c…` (and `e0c5f2f3…` earlier): `judge_ok=False`, `failed=['per_mutant']`.
Remedy: the `per_mutant` arm at the admitted sha.

**F-4. High (claim scope): score agreement is an identity by construction.** The emitter maps each tameshi verdict one-to-one onto a Stryker status. With no timeouts or NoCoverage, the library's score is killed/(killed+survived), which is tameshi's rate (`calculateMetrics.js:169-189`). The committed judge presents this as a check (`tools/mte-interop.py:209-210`). The working tree labels it "sanity only" (`:239`). The admitted text must say so and must not describe it as corroboration.

**F-5. Medium: the NoCoverage open set is under-listed.** See section 3.1: 35 survivors, not 8, and not 6 legs.

**F-6. Medium: stale frontier status and next move.** `corpus/README.md:78` says "held (round 1)", while `:111-114` says "partly held". The next-move cell says "validator unavailable: U", which is no longer true. jsonschema 4.25.1 ran under `uv` in this review (section 5).

**F-7. Medium: the INCONCLUSIVE policy conflates setup failures with timeouts.** See section 3.2. Remedy: state the policy in the entry. Smallest code change: put `exit=<rc>` into `statusReason` before the verdict word, keeping the verdict as the last token so `tameshi_counts` still works.

**F-8. Low: the leg count is not pinned in the tool.** `legs` comes from a glob (`tools/mte-interop.py:263` committed; `:305` working tree). The runner hard-codes `nlegs=8` and returns SETUP or FAIL when a leg is missing (`mutate-and-run.sh:1355-1376`), so the risk is low. Defence in depth: `if len(legs) != 8: raise Setup(...)`.

**F-9. Low: S002 line citations differ across documents.** The registry row cites master `:64-98`. The entry cites `:6-8, :19-27, :41-46, :88-100, :152-172`. `lessons/round-1.md` cites `:92`. All of these match the byte-identical file (checked: `:7` root required, `:41` mutant required, `:92` status enum, `:156` thresholds, `:203` framework). No change is needed beyond recording the identity.

**F-10. Info: sibling-repo safety.** The runner materializes pinned blobs with `git show`, `ls-tree`, `cat-file` and `rev-parse` only (`mutate-and-run.sh:1079-1160`), and writes into its own workdir. The tool stages siblings as read-only symlinks. I found no code path that writes into a sibling repo.

## 5. Evidence (commands and observed output)

- Vendored hashes: `sha256sum tools/vendor/*.tgz` gives schema `adb78e13…7280` and metrics `ce17812b…7838`. Both match contract `vendor_sha256`. `openssl dgst -sha512 -binary <tgz> | base64` gives schema `28CobrcLd…FSJQ==` and metrics `E2i+8bXo…xC7hw==`. Both match the `PACKAGES` pins in the tool.
- Freeze check: `git show 2a97ec1:tools/mte-interop.py | sha256sum` gives `58a5ae92…`. `git diff 2a97ec1 c9ff09f -- tools/mte-interop.py` changes only the usage line, `run_regression(…, fleet_root)` with staging, and the `--fleet-root` argument check. The judge is unchanged.
- Schema bytes: `cmp` of `.ufo/evidence/kaika-round-1/score-semantics/S002.json` against the extracted 3.9.0 `src` schema: IDENTICAL, sha256 `404575e9…`.
- Scorer arithmetic (`dist/src/calculateMetrics.js:169-193`): `totalDetected = timeout + killed`; `totalUndetected = survived + noCoverage`; `totalCovered = detected + survived`; `totalValid = undetected + detected`; `totalInvalid = runtimeErrors + compileErrors`; `mutationScore = detected / valid × 100`; `mutationScoreBasedOnCoveredCode = detected / covered × 100`. These match the formulas at `mutation-score-semantics.md:23` and `:29`.
- Probe (balanced swap), run twice: committed `judge_ok=True`; working tree `judge_ok=False failed=['per_mutant']` at both `e0c5f2f3…` and `8c24255c…` (section 4, F-3).
- Selftests, scratch only: committed `MTE_SELFTEST: 10/10 pass` (exit 0); working tree `8c24255c…` `MTE_SELFTEST: 16/16 pass` (exit 0, 16 CASE PASS lines). Output: `/tmp/r25-f1/selftest-committed.txt`, `/tmp/r25-f1/selftest-worktree2.txt`.
- Verdict tallies: `TABLE_*` at `mutate-and-run.sh:613-620` gives 85 verdicts (killed 8+8+6+4+7+7+5+5 = 50; survived 2+2+4+6+8+3+5+5 = 35).
- Prior regression (not re-run): `.ufo/evidence/round-24/noharm-c8c5b88.json` records `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`.

## 6. Residual risk and verification gaps

- **Counter not observed.** I did not run the 8/8 counter. The sweep is heavy on a shared host, and the integrator owns the counter. The round-24 PASS was at an earlier revision.
- **Moving target.** The working tree changed three times during review, and its latest sha is `8c24255c…`. The admitted sha is not yet chosen. Any figure above that names a working-tree sha is pinned to that sha.
- **lsp device not mounted.** `read xd://lsp` returned "No such tool: xd://lsp. Mounted devices: ast_edit, debug." Caller and definition checks were literal text reads, not semantic references.
- **Not verified:** emitted location spans beyond the selftest case; column semantics for non-ASCII text (the emitter counts Python code points); whether any pristine target contains non-BMP characters.
- **Sibling concurrence.** `.ufo/waves/round-25/w1/C2Tautology.md` independently reaches the same tautology verdict. I did not rely on it for any number above.
- **Tooling record (RULES.md).** Nothing was installed or upgraded by me. Pre-existing: uv 0.13.0 at `~/.local/bin/uv`; node v24.21.0 via fnm; system `python3` without jsonschema. Used: `uv run --no-project --with jsonschema==4.25.1` (ephemeral environment from PyPI via uv, reason: the F1 validator; resolved jsonschema 4.25.1 on Python 3.15.0). No pacman, no sudo, no permanent install.
- **Scratch files** are under `/tmp/r25-f1/` (`committed/`, `worktree/`, `worktree2/`, `metrics/`, `schema/`, `balanced_probe.py`, selftest outputs). They are outside the lane and were left in place.

## 7. Smallest safe correction (first step)

1. Choose one tool sha: commit the hardened judge under a new amendment, or revert the working tree.
2. Run the counter and selftest at that sha, and retain the output as evidence.
3. Open S086 with quotes.
4. Write the entry, the README row, and the PROVINCE append.
5. Keep NoCoverage as F1b with the 35-survivor list.
