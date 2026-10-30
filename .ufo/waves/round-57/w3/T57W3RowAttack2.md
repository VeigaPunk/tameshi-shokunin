# T57W3RowAttack2 — semantic ledger attack

Axes: semantic status accuracy; item-specific fix provenance; tip persistence; evidence completeness.

Examined all 13 assigned rows against master `2c51affd37e15cd7cd258d76ba0f5f73ff235924`. **11 supported, 2 weak, 0 wrong.** Recommendations only; no ledger/content edits or integration.

## Findings (evidence weakness, not demonstrated false status)

### R52.6 — weak report-specific support

The cited SCORECARD vocabulary, SHONEN box and round-42 table do not establish whether round-52's report meets its contract. The row already admits this weakness. Original report defects remain, but belong to a fleet-owned report.

Command: `git -C /home/vgpnk/Projects/shokunin show HEAD:.ufo/reports/round-52/tameshi.md` (exit 0).
Output includes `## Work performed`, `## Trend verdicts`, discernment `unprovable`, the sentence `This honest-stop report is written but not committed/pushed to the fleet repository`, and aggregate `[~] Four boxes remain as in SHONEN.md`. There is no Before/after section or per-box enumeration in the complete 36-line output.

Recommendation: keep status open with explicit ownership; actual report evidence must accompany the generic lane key, which cannot prove this defect alone.

### R53.8 — weak composite fix provenance

The primary routed item is the physical-page locator in SOURCES and the knowledge entry. The sole row excerpt and commit ca75c267 only support the later word-count correction. Status fixed is correct, but provenance/evidence is incomplete.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=short 99c3bc88 -- corpus/SOURCES.md corpus/knowledge/change-aware-resweep-cadence.md` (exit 0).
Output directly replaces `p. 4` with `p. 3 (physical; printed footer 1787)` in SOURCES and with `p. 3 (physical)` in the knowledge frontmatter. The ca75c267 diff creates round-57's correction with counts 20 and 20, not these locator changes.

Recommendation: add SOURCES:150 and knowledge/change-aware-resweep-cadence.md:2, and name 99c3bc88d704566197783f66b211ee0a830e0330 alongside ca75c267 for the two different repairs.

## Row conclusions

- **R52.4 — supported**: 6db1d220 adds the integrate script, both w3 markers and the w3 directory; all remain tracked at master. Prose excerpts alone do not prove tracking, but the cited commit does.
- **R52.5 — supported**: 218bc6b5 replaces both literal /tmp allocation roots with tempfile.gettempdir(); master uses strict_scratch_root() at both sites. The commit directly fixes this item.
- **R52.6 — weak**: Open original report defects persist, but the evidence excerpts describe generic standing rules and round-42 checkability, not the round-52 report. The original report is fleet-owned; git show fleet HEAD:.ufo/reports/round-52/tameshi.md still shows aggregate SHONEN, no Before -> after section and the stale not-committed sentence.
- **R53.1 — supported**: Frozen measure.py unchanged since routing. master ls-tree with its exact pathspec returns only the directory, incompatible with the bare rekey-name fullmatch; SCORECARD still quotes total=6 while the historical counter receipt says total=37.
- **R53.2 — supported**: master has no round-53/after tree; cited LOG and SCORECARD past-tense pointers remain. Later log history did not repair these statements.
- **R53.3 — supported**: Phase-B script remains unchanged, indexes [0] into a bare-name match of the directory-only ls-tree result, and has no phase-B tally receipt in its control directory. The original unbacked claim persists.
- **R53.4 — supported**: Exact receipt still names 9c6ef7bc80c0 and cr47=rc=1; git cat-file -t on that revision exits 128, Not a valid object name. No subsequent path commit re-anchors it.
- **R53.5 — supported**: Receipt still says amendments=5 and e62d99711a0d; LOG still pins amendments 1-5; freeze.json lists amendment 7. These paths have not acquired the proposed repair.
- **R53.6 — supported**: 59c38109 introduces ScratchRootUnusable and the correct catches in all four tools. At master, all four allocating selftests with TMPDIR=/nonexistent exit 2 with could-not-evaluate, without traceback.
- **R53.8 — weak**: Status fixed is substantively correct: page locators are physical page 3 and the quote counts have an append-only 20/20 correction. However ca75c267 and the sole excerpt prove only the word-count subpart, not the primary S275 locator repair. That repair was committed separately by 99c3bc88.
- **R53.9 — supported**: d33053f7 adds exactly the six routed files; each remains tracked at master. Results JSON excerpts are indirect but the cited commit is precisely the requested tracking repair.
- **R54.1 — supported**: 9cf0146b directly corrects SCORECARD, QUALITY and lesson claims to CTL_MISMATCH and 2/3; master retains the corrections and the underlying receipt confirms them. The row explicitly scopes out the unchanged fleet report.
- **R54.5 — supported**: 9cf0146b adds the explicit count correction. Re-derived master counts are w1=23 files/28 findings, w2=23 files/25 findings/12 nonempty sections, matching cited lane evidence. Fleet report and historical commit subject are not rewritten and are disclosed.

## Executed sweep and outputs

Full commands, return codes, stdout and stderr are in `T57W3RowAttack2-receipts/commands.json`; the exact reviewed rows/definitions are in `input-rows.json`. No unrun check is counted as passing.

- For every row: `git -C LANE show TIP:SPOTCHECK` read the routed line(s); `git -C LANE show TIP:EVIDENCE_PATH` read each cited evidence blob; `git -C LANE log --format='%h %s' ROUTED_AT..TIP -- EVIDENCE_PATH` checked later modifications. Full outputs saved. R53.1 counter, R53.3 script, R53.4 receipt and R53.5 verify-freeze receipt have no later modifying commit.
- For every fixed row: `git -C LANE merge-base --is-ancestor FIX TIP` exited 0. Item-scoped diffs were inspected for R52.5, R53.6, R53.8, R54.1 and R54.5; additions were inspected for R52.4/R53.9.
- R52.4: `git -C LANE show --format=fuller --stat 6db1d220...` lists the integrate script, w3.ready, w3.ready.dispatched and w3 reports. `git -C LANE ls-tree --name-only TIP -- PATHS` still lists all those tracking categories.
- R52.5: cited 218bc6b5 diff changes both `dir="/tmp"` to `dir=tempfile.gettempdir()`. Tip blob shows allocation sites at 784 and 934-935 use `strict_scratch_root()`.
- R53.1/R53.3: `git -C LANE ls-tree --name-only TIP .ufo/evidence/round-21/coldread` outputs exactly `.ufo/evidence/round-21/coldread`, not a `rekey-r53-*` basename. The unchanged fullmatch in counter 96-97 and script 99 cannot match it. Counter historical receipt: `rekeyed=0/30 ... total=37 C1_R53_PASS=false`; SCORECARD: `total=6`.
- R53.2: `git -C LANE ls-tree --name-only TIP .ufo/evidence/round-53/after/` exits 0 with empty stdout. LOG 2489-2490 and SCORECARD 2526/2543 still point there in past tense.
- R53.3: `git -C LANE ls-tree -r --name-only TIP -- .ufo/evidence/round-53/control/` lists only break-fixtures.py, controls.py, controls.exit, controls.stderr and controls.stdout, no phase-B output file. The phase-B script was not executed because its static discovery failure suffices and running its fixture writer is unnecessary.
- R53.4: `git -C LANE cat-file -t 9c6ef7bc80c0` exits 128: `fatal: Not a valid object name 9c6ef7bc80c0`. The receipt still has `rev=9c6ef7bc80c0 ... cr47=rc=1`.
- R53.5: tip verify-freeze blob prints `FREEZE e62d99711a0d files=8 amendments=5`; tip freeze.json has amendment `n: 7`; LOG still names e62d9971/amendments 1-5.
- R53.6: isolated shared clone checked out at TIP. Each `env TMPDIR=/nonexistent python3 ABS_CLONE/tools/TOOL --selftest` (bash-witness-study uses `selftest`) exits **2**, stdout empty, stderr a single `could-not-evaluate` line; all four full outputs saved. No traceback. These are unusable-root probes, not full successful selftest runs.
- R53.9: `git -C LANE show d33053f... --format=short --name-status -- .ufo/waves/round-53` prints **A** for exactly the six named files; tip ls-tree still lists all six.
- R54.1: tip controls-b.stdout prints `CTL_MISMATCH CTL_POS_c1 expected=true actual=false` and `CONTROLS_B: 2/3 as pre-registered`; 9cf0146b's scoped diff corrects the lane records to match.
- R54.5: immediate `*Read*.json` children selected from `git ls-tree -r --name-only TIP -- .ufo/waves/round-54/w1/` and w2, loaded with `git show TIP:path`; Python summed `len(findings)`: **w1 files=23 findings=28 nonempty=15; w2 files=23 findings=25 nonempty=12**. These equal the correction, not the old report. Raw input blobs and enumeration commands are saved; derivation summary is in summary.json.

`LANE` above is `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; `TIP` is the full master hash at the top. Full receipts use expanded arguments, not these abbreviations.

## Residual risk and verification gaps

- LSP unavailable: reading `xd://lsp` returned `No such tool`. No references/definition/diagnostics server was available. Text and Git evidence are not presented as semantic LSP proof.
- No entire frozen counter/control reruns or no-harm monitor runs performed. Static counter failure, recorded outputs, commit diffs and four targeted exit probes establish the scoped conclusions; no calibration score or admission is claimed.
- R54.1 and R54.5 are supported as **lane-record corrections**. Fleet-report edits are outside lane scope and remain disclosed residuals, not magically repaired original report bytes. No canonical-runtime, rerouting, saturation or resume changes occur in this evidence-only review.
- Master was pinned once for a reproducible sweep. No post-sweep master re-read is claimed.
- No tools installed/updated; no lane content edited; no frozen evidence edited; only the named seat outputs and own scratch were written.

## Self-evaluation

Accuracy 4/5: evidence separates true fixed status from incomplete locator provenance; no full control rerun is claimed. Completeness 4/5: all 13 rows covered; fleet-side report repairs remain outside scope. Clarity 4/5: report distinguishes status from excerpt support; full raw outputs are intentionally separate. Actionability 4/5: both weak rows have specific evidence repairs, but R52.6 needs external ownership. Conciseness 4/5: raw history is relegated to receipts. Overall 4.0; user should agree the narrow recommendation is auditable without claiming admission.
