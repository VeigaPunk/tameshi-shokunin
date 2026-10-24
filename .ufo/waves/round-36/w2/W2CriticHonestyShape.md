# W2CriticHonestyShape — final honesty pass, round 36

Seat: critic, leaf (no subagents). Scope: unrun checks claimed passed, prettified
verdicts, duplicate deciding counter runs, receipts dated before the contract freeze.
Lane tip `fbb01cf46f8437fd1264c1a3acc053c882fa2164` at read time; contract
`.ufo/evidence/round-36/contract.json` (committed `e423c41b`, 2026-10-24 03:14:00 -0300).

## Verdict: one MINOR finding (unreceipted start census claimed "receipt kept"); no unrun-check fabrications defeating a claim; no prettified verdicts found; exactly one deciding v2 run at the measurement commit; no pre-freeze receipts. Not a defect the canonical judge must reject.

## Commands run (all read-only; repo = /home/vgpnk/Projects/shokunin/tameshi-shokunin)

- `git log --format='%H %ci %s' -25`; `git show --stat` on `e423c41b`, `b455001e`, `d9c496b1`, `fbb01cf4`; `git status --porcelain -uall` (twice).
- `sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-36/src/s103-git-hash-object.html` — every pinned hash matches (`6188db16…`, `a7d3f2dd…`, `9eb8944c…`, S103 `dd826dae…` = 29,933 B).
- Parsed every `.stdout` in `.ufo/evidence/round-36/{after,control}` with `json.load` (key fields: score, covered, rev_input, revision, uncovered_headings, sources.rows).
- Semantic ledger diff `git show e423c41b:…ledger.json` vs `b455001e:…ledger.json` (stdlib json): `entries` 493 → 497, **+4 / −0**; `schema`, `carried_from`, `provenance`, `round21_provenance` byte-equal. Kill rule for C1 holds at the object level.
- `stat`/epoch→`-0300` conversion over all round-36 evidence mtimes; `find .ufo/evidence/round-36 -name "*census*"`; `git ls-tree -r d9c496b1 --name-only | grep census`; `git cat-file -t 91373d55…`; `git check-ignore` on the `__pycache__` artifact.
- Read `LOG.md` (round-36 entry), `SCORECARD.md` (round-36 block) at `e423c41b`, `corpus/lessons/round-36.md`, `corpus/lessons/round-36-verifier-spotcheck.md`, `refresh-specs.json`, `refresh-receipts.json`, `affected-sections.json`, all four `traces/L1/source-*.json` (worktree + `git show` blob), the fleet report `.ufo/reports/round-36/tameshi.md`, both wave specs (39+39 seats), and the committed w1 seat reports (39 files).

## Checked claims vs receipts

| Claim | Receipt | Observed | Match |
|---|---|---|---|
| before monitor `796e08b` = 6, 60/64 | `after/monitor-at-796e08b.{stdout,stderr,exit}` | 6, 60/64, rev_input=796e08b, overrides_used=false, EXIT=0 | yes (filed under `after/` — cosmetic misnomer only) |
| do-nothing control `e423c41b` still 6 | `control/monitor-at-e423c41b.*` | 6, 60/64, same 4 uncovered headings, ledger_source=rev | yes |
| after `b455001e` = 8, 64/64 | `after/monitor-at-b455001e.*` | 8, 64/64, uncovered=[], EXIT=0 | yes |
| census end exit 0, 100 rows | `after/census-at-b455001e.{stdout,exit}` | CENSUS_EXIT=0, `sources-rows-at-b455001e.txt` = 100; stdout shows W04/W01 warnings (disclosed, not hidden) | yes |
| depth guard 9/9 | `after/depthD-at-b455001e.stdout` | `recorded_cases=9 depth_score=9`, runner sha `a7d3f2dd…` | yes (no `.exit`/`.stderr` twin — receipt-completeness nit) |
| v2 deciding at measurement commit | `after/c1v2-at-b455001e.{stdout,stderr,exit}` | `mode=deciding tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 sealed_after_freeze=1 rev=b455001e C1_R36V2_PASS=true`, EXIT=0 | yes — exactly ONE deciding v2 run at the measurement commit |
| v1 vacuous accept (before demo) | `control/v1-at-emptypanel.*` | `C1_R35 … pub_kill=0/0 pub_distinct=0 … PASS=true`, V1_EXIT=0, rev=91373d55 (scratch-clone mutant commit, absent from lane object DB — honestly disclosed in the fleet report) | yes |
| v2 rejects empty panel | `control/v2-at-emptypanel.*` | `C1_R36V2 … pub_slots=0 … PASS=false`, V2_EXIT=1 | yes |
| S103 row + snapshot | `src/s103-git-hash-object.html` | sha256 `dd826dae…` = contract value | yes |

## Freeze ordering

- Contract blob exists only in `e423c41b` (single-commit history); counter blob likewise — no post-freeze edits (`git log -- <path>` = one commit each).
- First data receipt mtime = `control/monitor-at-e423c41b.stderr` 03:14:34, after content commit 03:14:00; refresh traces' embedded `measurement_interval` = 03:16:00, before refresh commit 03:16:09; all receipt mtimes 03:14:34–03:20:58, before receipts commit 03:21:45. **No receipt predates the freeze.** (Corroborated by w1 `RevengerContractFreeze` and w2 `W2RevengerReceiptOrder`.)
- `.pyc` for `c1-measure-v2` compiled 03:05:46 (pre-freeze, benign byte-compile/import; gitignored — `__pycache__/` rule at `.gitignore:4`). Not a deciding-run signal.

## Findings

1. **MINOR — start census claimed with a receipt that does not exist.** Lesson `corpus/lessons/round-36.md` lines 48–49: "Census: round start (tip `796e08b`) `sources-census.sh validate` exit 0, 99 rows; round end … exit 0, 100 rows — **both receipts kept under `.ufo/evidence/round-36/`**." The fleet report repeats "census run at start (99 rows, exit 0)". No start-census receipt exists: `find .ufo/evidence/round-36 -name "*census*"` yields only `after/census-at-b455001e.{stdout,exit}`, and `git ls-tree -r d9c496b1` shows nothing else. Either the validate run never happened or its receipt was lost. The `exit 0` itself is unverifiable; the **99-row value is independently corroborated** by `after/monitor-at-796e08b.stdout` (`sources.rows=99`, malformed 0). Impact: none on C1/C2 — census is not a claim-bearing check; the false part is only the "receipt kept" wording. Smallest safe correction: rerun the start census hermetically at `796e08b`, commit the receipt, or amend the lesson/report wording on the next round's append.

2. **Observation — prospective outcome text committed before the runs.** The SCORECARD round-36 block (committed `e423c41b`, 03:14:00) names final values ("still prints 6", "PASS=true") and receipt paths that did not yet exist; LOG uses future-tense "After … target 8". Every prediction later matched measured output, so the record is true today — but the record was written before the data. Worth noting because the same pattern would conceal an error had any run disagreed.

3. **Observation — receipt argv replay hazard, self-corrected.** `refresh-receipts.json` embeds the live `--out` lane path in each recorded argv. During this wave a w2 seat (`W2ReviewFrontierSourced`) replayed that argv verbatim; the four committed `traces/L1/source-*.json` were transiently overwritten (~03:41–03:42) with seat-scratch-rooted JSON (I captured them: `root=/fast/scratch/hyaku/tameshi-r36-seats/W2ReviewFrontierSourced/lane`, `rev=null`), then the seat restored all four byte-exactly (current worktree sha256 = committed blobs; last write 03:42:12). Committed record unaffected — receipts are read at REV anyway. Suggest a `## Holds`-style note that receipt argv containing absolute `--out` paths are replayable landmines.

4. **Nit — missing exit/stderr companions.** `after/depthD-at-b455001e` has no `.exit`/`.stderr` files; `validate-w1/w2` have `.stdout`/`.stderr` but no `.exit` (LOG says "exit 0"). Exit status is asserted but not receipted for these; values are consistent with content.

## Cleared

- **Duplicate deciding runs**: exactly one `mode=deciding` v2 run at the measurement commit. The empty-panel v2 control also labels itself `mode=deciding` (no `--tool` flag = deciding in the counter's own labeling), but it is a contract-named control at a scratch rev, and the kill rule scopes "exactly one" to the measurement commit — no violation.
- **Prettified verdicts**: w1 reports include a real DEFECT (`CriticDeadPointerFix`), AGREE/PASS/KILLED verdicts with receipts; no suppressed failures. The earlier elision artifact in my `cat` output ("Command exited with code 1" after `depthD` stdout) was my own trailing `[ -f ]` test, not receipt content — the file is a clean 99-byte receipt.
- **Unrun checks**: every value-bearing claim has a committed receipt whose content matches, except the start census (finding 1). The report's "re-measured at final tip `d9c496b1`: 8, 64/64" also lacks a lane receipt but is independently corroborated by the non-author verifier spot-check (`round-36-verifier-spotcheck.md`, its own re-run printed 8, 64/64 at `d9c496b1`).
- **Ledger honesty**: +4/−0 append-only delta; new entries' `read_rev=e423c41b` matches `refresh-specs.json.planned_at_revision` and each trace's input set is a subset of its entry inputs with equal sha256 (w2 `W2LabratTraceSubset` independently verified 4/4).
- **Wave specs**: 39+39 = 78 prepared seats as reported; validator stdout is a full rendered taskCall, stderr empty.

Tool installs: none. Scratch use: none (all checks read-only against repo + committed receipts).
