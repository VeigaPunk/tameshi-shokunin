# T57W3RowAttack1 — semantic ledger attack

Lane tip inspected: `2c51affd37e15cd7cd258d76ba0f5f73ff235924`. Assigned ledger snapshot: attack-ledger.json. Axes: calibration truth, fix-commit identity, present-tip persistence. Recommendations only; no admission/judgment or lane edits.

## Findings by severity

**Medium — R52.1 wrong fixing-commit attribution.** The cited script-introduction header does not discharge the re-key debt. The actual deciding receipt arrived in a later commit.

**Low — R50.4 and R51.2 weak support.** The former only cites old carry-forward statements; the latter omits completion-commit/fresh-reader evidence.

## Per-row results and exercised evidence

### R50.1: supported
6d8c11e changes S022 queued -> mined and the lesson logs old -> new. Tip preserves both. Additional git-show evidence from round-51/no-harm.sh explicitly names R50.1 and rebases the 73 population pin to score>=9/fresh>=71 (population 74); the ledger note unnecessarily leaves this part unverified.

Proposed fix: Add round-51/no-harm.sh:5-7 as evidence and remove the unverified-monitor caveat.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/SOURCES.md` (exit 0); output lines 33-33:
```
| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51.md` (exit 0); output lines 12-12:
```
Rows touched: S022 status `queued` → `mined` (used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`; mined means cited by at least one used-by path under CORPUS.md); no other existing row status changed. Appended S272 and S273; the registry has 133 rows and the next allocated id is S274. Census start exit 0; round-end census receipt is in `.ufo/evidence/round-51/census-end.*`.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-50-verifier-spotcheck.md` (exit 0), output:
```
1. **S022 status contradicts its used-by cell.** `corpus/SOURCES.md` S022 is `queued` while `used-by` now names `corpus/knowledge/fixture-shrinking-pilot.md`; contract v1 defines `mined` as cited by ≥ 1 used-by path. The status was held back to keep the frozen round-45 freshness monitor at population 73. Fix the cell to `mined` and re-base or supersede that monitor (or record the exception as a named correction), logged old → new in the lesson.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- corpus/SOURCES.md corpus/lessons/round-51.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/corpus/SOURCES.md b/corpus/SOURCES.md
index 368f65e7..6d2f634f 100644
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -31,5 +31,5 @@ rows only, and a row is a claim opened in the round that writes it.
 | S020 | Property-based testing in Python: empirical insights (de Oliveira, Corgozinho, Rocha, Valente; EMSE 2026) — https://doi.org/10.1007/s10664-026-10953-w | paper | A | PBT usage in 244 Python projects | Abstract; §6.2 and Table 2 (author copy https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf, fetched 2026-10-19; Springer served an anti-bot challenge) | 367 PBTs from 244 projects in nine categories with Test Oracle at 29.97%; data generation is the main challenge (36.62% of SO questions); Ghostwriter fully automates only 18.23% | queued | 2026-10-19 | 365d | — |
 | S021 | Agentic Property-Based Testing (Maaz, DeVoe, Hatfield-Dodds, Carlini; arXiv 2510.09907) — https://arxiv.org/abs/2510.09907 | paper | A | agentic PBT bug validity on real packages | Abstract, arXiv:2510.09907v1 (submitted 2025-10-10) | an LLM agent infers properties from code and docs, writes Hypothesis tests and reflects before reporting: 56% of reports were valid bugs; ranking lifts the top-21 validity to 86% | queued | 2026-10-19 | 180d | — |
-| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | queued | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
+| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
 | S023 | Shrink Ray README (DRMacIver/shrinkray) — https://github.com/DRMacIver/shrinkray | code | A | shrinkray's interestingness-driven reduction | README §Usage and §LLM mode @ page currentOid 5fe6ee135d732e4b7758b3dbe3d91428523018fb, fetched 2026-10-19 | a reducer driven by any executable interestingness test (exit 0 = interesting); parallel multi-format passes; local LLM proposals are accepted only when the interestingness test still passes | queued | 2026-10-19 | 90d | — |
 | S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | mined | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md, corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
@@ -145,4 +145,6 @@ rows only, and a row is a claim opened in the round that writes it.
 | S270 | Property-based testing for functional programs (Smallbone; Chalmers University of Technology Technical Report 76L, ISSN 1652-876X, 2011) — https://smallbone.se/papers/lic.pdf | paper | B | F10 generator craft — the generator bounds which laws a random search can reach, an author's own report on QuickCheck-family generator quality and distribution | §2.10 Generating Test Data, p. 34 @ Technical Report 76L, 2011, author-served PDF 116 pp fetched 2026-10-26, sha256 eaee48f9, snapshot .ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf | generator quality bounds the search: an ill-fitting list generator never produces the cases that separate two functions, and drawing elements from a small domain fixes it | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
 | S271 | Simplifying and Isolating Failure-Inducing Input (Zeller, Hildebrandt; IEEE TSE 28(2):183-200, 2002; DOI 10.1109/32.988498) — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf | paper | A | F6 fixture shrinking — the 1-minimal sub-case criterion for a reduced fixture and the test-run cost of reaching it | §I Introduction, Simplification of test cases paragraph (mirror PDF p. 1); §III-A Minimal Test Cases, Definition 10 (mirror PDF p. 4); §III-C Properties of ddmin, Propositions 11 and 12 (mirror PDF p. 6); §IV-B Figs. 11-12 @ IEEE TSE vol. 28 no. 2, February 2002, DOI 10.1109/32.988498 (running head on the carrier; the mirror carries no journal folios); course-mirror PDF fetched 2026-10-26, sha256 7ed0c812, 247738 bytes, snapshot .ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf | a failing test case is 1-minimal when removing any single change makes the failure disappear, ddmin returns such a case, and the reduction is itself a cost measured in test runs | mined | 2026-10-26 | 730d | corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
+| S272 | kagi `corpus/drift-pins.sh` (fleet gate, read-only) — kagi-shokunin/corpus/drift-pins.sh | code | A | the gate's own verdict vocabulary, exit map and hermetic scratch-tree selftest at the measured revision | :19 (exit map), :118-259 (verify), :374-446 (selftest), :400-405 (the exit-and-grep assertion) @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb, 451 lines, mode 100755; unchanged at kagi HEAD 69b61db46be4ed955994f6f1d1cba522bc5f4e97) | a host-drift gate anchors on committed baselines instead of live fingerprints and proves each verdict class in a scratch tree; its 13-case `--selftest` prints `DRIFT_SELFTEST: PASS (13 cases)` and asserts exit code plus an unanchored `grep -q` for the verdict word, not its position in the output | mined | 2026-10-26 | 180d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
+| S273 | GNU Bash Reference Manual, The Set Builtin (author copy of the manual, Edition 5.3, last updated 18 May 2025) — https://tiswww.case.edu/php/chet/bash/bashref.html (the gnu.org node page https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html was unreachable on 2026-10-27 UTC: eight attempts, HTTP 000, 0 bytes, connect timeouts — https and http, with and without www, IPv4-forced, and the single-page manual alike) | docs | A | Bash `errexit` (`-e`) and `pipefail`: which failing commands end a non-interactive shell, the listed non-exits, and a pipeline's return value | §The Set Builtin `-e` item (single-page copy lines 6547-6570) and `pipefail` item (lines 6706-6710); same text in the Savannah texi pinned by S097 at `@item -e` lines 5929-5948 and `@item pipefail` lines 6062-6066 (re-fetched 2026-10-27, sha256 f3d37d57, byte-identical to S097); a command of assignments only takes its status at §Simple Commands lines 3675-3677 (copy lines 4172-4173) @ author copy fetched 2026-10-27T00:22Z UTC, two fetches byte-identical (1040870 bytes; SHA-256 b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4), snapshot .ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html | Quotes (each at most 25 words), `-e`: "Exit immediately if a pipeline ... returns a non-zero status"; non-exits: "The shell does not exit if the command that fails is ... any command in a pipeline but the last"; the parenthetical tying that to pipefail: "any command in a pipeline but the last (subject to the state of the pipefail shell option)"; `pipefail`: "the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status"; assignments-only status: "the exit status of the last command substitution performed" | mined | 2026-10-26 | 365d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
 
 ## Paths
@@ -497,2 +499,4 @@ Round 46: three rows added, S258 (arXiv 2504.16777, Systemic Flakiness), S259 (t
 - Round 50: one row added by document from the shokuknow `corpus-expansion-1` package (theme F6), S271 (Zeller & Hildebrandt, IEEE TSE 2002, DOI 10.1109/32.988498; staged S167, which collides with nothing and is not reused), re-opened 2026-10-26 from the course mirror (HTTP 200, sha256 7ed0c812) with the snapshot under `.ufo/waves/round-50/w1/T50ScribeRows.src/`; the Zeller lead in the leads list above now has this row, and the earlier stop note (author PDFs timed out, ResearchGate 403, DOI metadata only) is superseded by the mirror fetch. S022 used-by — → the F6 pilot entry (its status stays queued: promoting it would move the frozen round-45 freshness population, a no-harm monitor); S024 used-by gains the two round-50 F6 entries (logged old → new in `corpus/lessons/round-50.md` `## Gate`). Id collision check: `reg-ids` 130, `staged-ids` 103, collisions 8 (S153-S160) (`.ufo/waves/round-50/w1/T50ExecIdGuard/`).
 - Next unused id: S272 (staged ids S161-S255 stay reserved by document for the package).
+Round 51: two tier-A rows added on the core tenth-leg case, S272 (kagi `corpus/drift-pins.sh`, code, pinned rev `e64e81b8`) and S273 (GNU Bash Reference Manual, §The Set Builtin, author copy, docs; gnu.org page was unreachable and the opened carrier is named in the row), both mined and opened this round; snapshots / fetch receipts under `.ufo/waves/round-51/w1/T51ScribeRowGate*` and `T51ScribeRowBash/`. Used by `corpus/knowledge/mutation-case-kagi-drift-pins.md`. S022 status `queued` → `mined` (used-by already cited `corpus/knowledge/fixture-shrinking-pilot.md`; reason: CORPUS.md defines mined as cited by ≥1 used-by path); logged in `corpus/lessons/round-51.md`. Registry rows 131 → 133.
+- Next unused id: S274 (staged ids S161-S255 stay reserved by document for the package).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- SKILL.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/SKILL.md b/SKILL.md
index 5f985e2f..e97f350c 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -2135,2 +2135,37 @@ the kill came from an absolute assert on the masked region.
 |---|---|---|---|
 | `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+
+#### Gate/probe registry — round 51
+
+| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
+|---|---|---|---|---|---|---|---|
+| bash declared-witness study | probe | `python3 tools/bash-witness-study.py check` (add --evidence DIR to grade another copy of the frozen evidence) | 0 clean; 1 failed (tamper, digest drift, summary/raw mismatch, unresolved sweep); 2 could-not-evaluate (missing input, pin mismatch, runner SETUP); 64 could-not-evaluate (usage) | `python3 tools/bash-witness-study.py selftest` → VERDICT: is the last line, preceded by WITNESS_SELFTEST: 51/51 pass | `.ufo/evidence/round-12/BashWitness/declaration.json` (frozen target, spec and runner sha256), `.ufo/evidence/round-12/BashWitness/declared.tsv` (declared-witness rows, sha pinned in declaration.json), `.ufo/evidence/round-12/BashWitness/summary.json`, `.ufo/evidence/round-12/BashWitness/manifest.json`, `tools/mutate-and-run.sh` (pinned runner digest, the spec is extracted from its heredoc); the DECLARED_WITNESSES rows are literals in the tool | caller-chosen --evidence DIR for declare, run and rerun plus the extended manifest; check and count read-only; selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored); sibling kagi object store read-only | tameshi |
+| command binding receipts | gate | `python3 tools/command-binding.py --bundle BUNDLE.json --expected EXPECTED.json --json` | 0 clean; 1 failed binding or outcome; 2 could-not-evaluate (invalid shape or integrity); 64 could-not-evaluate (usage) | `python3 tools/command-binding.py --selftest` → finding id COMMAND_BINDING_SELFTEST: in the last stdout line | `.ufo/evidence/round-23/extra-cases.json`, `.ufo/evidence/round-24/extra-cases.json`; literal expected exits and finding IDs in the tool selftest | read-only over the lane; selftest writes one isolated bundle/expected pair under TMPDIR | tameshi |
+| context receipt replay | gate | `python3 tools/context-capture.py --check` (frozen pin) or the same invocation with --receipt FILE --expected FILE | 0 clean; 1 failed; 2 could-not-evaluate; 64 could-not-evaluate (usage) | `python3 tools/context-capture.py --selftest` → SELFTEST: PASS (49/49 cases) | `.ufo/evidence/round-14/context-receipt.json`; literal digest 05cb55b8… and id/exit pin inside the tool | none during --check; selftest fixtures under /tmp/context-capture-selftest-*, removed in finally | tameshi |
+| environment-profile differential | gate | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out DIR/receipt.json --jobs 3` | 0 clean; 1 failed; 2 and 64 could-not-evaluate | `python3 tools/env-diff.py --selftest` → exit 0, last line ENVDIFF_SELFTEST: 9/9 pass | `.ufo/evidence/round-21/c2-contract.json`, `.ufo/evidence/round-21/f5/receipt.json`; literal expected classifications in the tool selftest | caller-chosen `--out` FILE plus sandboxes under `/tmp/tameshi-r21-envdiff.*` and TMPDIR-respecting selftest trees; lane trees read-only | tameshi |
+| evidence disposition accounting | gate | `python3 tools/evidence-disposition.py --root LANE --dispositions FILE` (lane run: --root . --dispositions .ufo/evidence/round-18/dispositions.json) | 0 clean; 1 failed semantic expectation; 2 could-not-evaluate (missing, unreadable, malformed, tampered or path-invalid input, invalid schema, internal failure); 64 could-not-evaluate (usage) | `python3 tools/evidence-disposition.py --selftest` → finding id SELFTEST: exit 0, 66/66 cases in about 3 s at rev 84aa673a; needs jj on PATH | `.ufo/evidence/round-13/expected.json`, `.ufo/evidence/round-13/verification.json`, `.ufo/evidence/round-13/producer-oracle-repair.json`, `.ufo/evidence/round-18/dispositions.json`; expected ids and exits are literals in the tool selftest | none in the lane — read-only over --root; selftest fixtures under /tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure | tameshi |
+| golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
+| mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root (pbt-staged-id-); selftest scratch under TMPDIR | tameshi |
+| pin disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root FLEET` | 0 clean; 1 failed (selftest FAIL only); 2 could-not-evaluate (usage, invalid or mismatched manifest, fleet root not a directory) | `python3 tools/pin-disposition.py --selftest` → SELFTEST: PASS n/n finding id SELFTEST: | `.ufo/evidence/round-13/pin-manifest.json` | read-only over the named fleet root; selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures, removed on PASS | tameshi |
+| round-20 receipt-window measure | gate | `python3 tools/receipt-measure.py --repo REPO --rev REV --json` | 0 clean, six items PASS at REV; 1 failed, including an absent REPO or unresolvable REV which is graded as six FAIL items rather than could-not-evaluate; 2 could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other arguments | `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST: 10/10 pass | `.ufo/evidence/round-20/contract.json`, `.ufo/evidence/round-20/stage/measure.py`, `.ufo/evidence/round-20/stage/receipt-window.py`, `tools/receipt-window.py`, `.ufo/evidence/round-20/final/receipts.json`, `.ufo/evidence/round-20/final/historical-receipts.json`, `.ufo/evidence/round-20/final/receipt-window-selftest.json`, `.ufo/waves/round-20/dispatch.json` | reads REPO at REV; no repo writes; scratch fixture trees under TMPDIR only, prefixes `receipt-measure-selftest.*` and `tameshi-r20-measure.*` | tameshi |
+| receipt-window validity | gate | `python3 tools/receipt-window.py --contract CONTRACT_JSON --receipts RECEIPTS_JSON` (add --json for one machine-readable verdict object) | 0 clean; 1 failed (findings); 2 could-not-evaluate (contract or receipts invalid, also argparse usage); 64 usage (missing --contract or --receipts) | `python3 tools/receipt-window.py --selftest` → RECEIPT_WINDOW_SELFTEST: last non-empty stdout line reads RECEIPT_WINDOW_SELFTEST: 20/20 pass with exit 0 | `.ufo/evidence/round-20/contract.json` expectations and instrument shas; `.ufo/evidence/round-20/public-cli-cases.json` synthetic cases; `.ufo/evidence/round-20/final/receipts.json`; `.ufo/evidence/round-20/final/receipt-window-selftest.json` recorded 20/20 exit 0 | reads caller-chosen CONTRACT_JSON and RECEIPTS_JSON without writing; selftest writes only its TMPDIR temp tree | tameshi |
+| entry-registry walk | gate | `python3 tools/registry-check.py --rev HEAD` (add `--only NAME` to grade one row) | 0 clean; 1 failed; 2 could-not-evaluate (registry unreadable or invalid, root/rev/clone failure, only or tag miss); 64 usage | `python3 tools/registry-check.py --selftest` → finding id SELFTEST: last line SELFTEST: PASS (51 cases) at 84aa673 | `tools/registry.json`, `tools/registry-check.py` | selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored), removed afterwards; live --root mode runs registry rows inside LANE so rows may write there | tameshi |
+| frozen registry replay | gate | `python3 tools/registry-replay.py --run --repo . --rev REV --requirements .ufo/evidence/round-23/requirements.json --registry-baseline .ufo/evidence/round-23/registry-baseline.json --out DIR` | 0 clean; 1 failed (refused rows: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT; an uncaught traceback also exits 1); 2 could-not-evaluate (registry digest mismatch, frozen requirements drift, clone HEAD mismatch, INVALID_OBSERVATIONS); 64 could-not-evaluate (usage) | `python3 tools/registry-replay.py --selftest` → REGISTRY_REPLAY_SELFTEST: 10/10 pass | `.ufo/evidence/round-23/requirements.json`, `.ufo/evidence/round-23/registry-baseline.json`, `tools/registry-check.py` (runner digest taken from the clone copy that runs) | caller-selected `--out` DIR (observations.json, bundle.json, expected.json, live-dependent.json) plus a private clone under TMPDIR; row commands run inside that clone, whose fleet mirror symlinks the live siblings, so the run is not write-isolated from them; selftest under TMPDIR | tameshi |
+| repeated control agreement | gate | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`, or --snapshot DIR over a committed control snapshot | 0 clean (controls_match); 1 failed (controls_mismatch); 2 could-not-evaluate (baseline_nonzero, command_unavailable, snapshot_tampered, setup_error); 64 could-not-evaluate (invalid_usage) | `python3 tools/repeat-control.py --selftest` → SELFTEST: PASS (29 cases) at exit 0 | `.ufo/evidence/round-12/ControlGate/expected.json`, `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` | caller-chosen --out DIR, created fresh and never deleted; --snapshot DIR read-only; selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass) | tameshi |
+| round21 measure facade | gate | `python3 tools/round21-measure.py --claim c1 --repo DIR --rev REV --json` | 0 clean; 1 failed; 2 could-not-evaluate (setup or unknown rev); 64 could-not-evaluate (usage) | `python3 tools/round21-measure.py --selftest` → ROUND21_MEASURE_SELFTEST: 13/13 pass | `.ufo/evidence/round-21/c1-survivors.py`, `.ufo/evidence/round-21/c2-count.py`, `.ufo/evidence/round-21/c2-contract.json` | TMPDIR only (selftest fixtures and delegated counter receipts); target repo read-only | tameshi |
+| shrink-case | probe | `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json` | 0 shrunk (report written); 1 selftest checks failed; 2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill) | `python3 tools/shrink-case.py --selftest` → SHRINK_SELFTEST: cases=21 failed=0 | `tools/pbt-staged-id.py` generator imported beside the tool; `tools/staged-id-guard.py` and `.ufo/evidence/round-49/c2/panel.json` for the M02 leg; expected edit literals in the tool source | caller-chosen --out FILE; tempfile.mkdtemp roots under TMPDIR for guard runs and selftest; lane read-only | tameshi |
+| staged-id adoption guard | gate | `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged STAGED.md --json` (add `--map MAP.json` to validate a candidate adoption map) | 0 clean (answered, or admitted with `--map`); 1 failed (analysis refused, or map inadmissible); 2 could-not-evaluate (usage, missing flag, or setup refusal) | `python3 -I tools/staged-id-guard.py --selftest` → VERDICT: PASS at exit 0, FAIL at exit 1 (counter line STAGED_ID_GUARD_SELFTEST: cases=N failed=M) | none — expected values are the fixture literals SELFTEST_REGISTRY and SELFTEST_STAGED_* committed inside tools/staged-id-guard.py; no expected file on disk | read-only: no writes, no temp files, no lane writes; caller names the registry, staged and map paths and stdout/stderr is the whole output | tameshi |
+| tally audit v2 (mutation runner tally) | gate | `python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh` (add `--then-regression --workdir DIR` to also require the runner's REGRESSION line to name cases=legs) | 0 clean; 1 failed (audit FAIL or a selftest case failure); 2 could-not-evaluate (cannot audit, setup, usage); a timed-out then-regression reports 124 and folds to 2 | `python3 tools/tally-audit-v2.py --selftest` → TALLY_AUDIT_V2_SELFTEST: 22/22 pass, one seeded-fault case per check | none — expected tallies are literals of the tool's independent oracle and its 22 selftest seeds; audited surface defaults to `tools/mutate-and-run.sh` | lane read-only; scratch under TMPDIR (tally-audit-v2.*, removed in finally); the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires; --then-regression writes only the runner's caller-named --workdir | tameshi |
+| tally audit v3 | gate | `python3 tools/tally-audit-v3.py --runner tools/mutate-and-run.sh` | 0 clean; 1 failed; 2 could-not-evaluate (SETUP: runner unparsable, tally harness structure missing, or argparse usage) | `python3 tools/tally-audit-v3.py --selftest` → TALLY_AUDIT_V3_SELFTEST: 35/35 pass | `tools/mutate-and-run.sh` is the only input read; expected REF_BLOCK, REF_NAMES and the 35 seeded-case panel are literals in the tool, and `.ufo/evidence/round-32/heldout/` is the committed provenance of those seeds (not read at run time) | audit and selftest scratch under TMPDIR, plus one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX allocated to witness the runner shape and removed at exit; the audited runner is never edited; `--then-regression` lets the runner create its own auto root or caller-chosen --workdir DIR | tameshi |
+| tally audit undercount guard | gate | `python3 tools/tally-audit.py` audits the runner `tools/mutate-and-run.sh` beside it; `--runner PATH`, `--then-regression --workdir DIR` accepted | 0 clean; 1 failed; 2 could-not-evaluate (cannot audit, usage, or regression SETUP); 64 could-not-evaluate (runner usage error surfaced through --then-regression) | `python3 tools/tally-audit.py --selftest` → TALLY_AUDIT_SELFTEST: 11/11 pass | `tools/tally-audit.py` REF_BLOCK reference tally block and leg-name panel are literals in the tool; audited `tools/mutate-and-run.sh` read-only | TMPDIR scratch dirs with prefix tally-audit, removed on exit; --then-regression hands its workdir to the runner | tameshi |
+| traced input surface | probe | `python3 tools/trace-inputs.py --root LANE --out RECEIPT.json -- COMMAND ARG...` | 0 clean; 1 failed (selftest check); 2 could-not-evaluate (setup: root or cwd not a directory, strace missing, no successful root execve); 64 could-not-evaluate (usage) | `python3 tools/trace-inputs.py --selftest` → SELFTEST: n/n on exit 0 | none — expected values are literals in the selftest | caller-chosen --out FILE (parent directories created); private trace-inputs-run-* tempdir outside --root, deleted on exit; selftest tree under TMPDIR | tameshi |
+| wave accounting | gate | `python3 tools/wave-accounting.py --bundle BUNDLE.json --expected EXPECTED.json` | 0 clean; 1 failed invariant; 2 could-not-evaluate (invalid, unavailable or tampered input); 64 could-not-evaluate (usage) | `python3 tools/wave-accounting.py --selftest` → FINDING: SELFTEST_PASS, 8/8 frozen plus 16/16 supplemental cases | `.ufo/evidence/round-22/measure.py`, `.ufo/evidence/round-22/accounting-extra-cases.json` | stdout only; caller-chosen `--bundle`/`--expected` read-only, selftest fixtures under isolated TMPDIR | tameshi |
+| wave parent settlement | gate | `python3 tools/wave-parent-settle.py --receipt RECEIPT.json` | 0 clean (SETTLED); 1 failed (UNSETTLED); 2 could-not-evaluate (usage, or --receipt not supplied) | `python3 tools/wave-parent-settle.py --selftest` → WAVE_PARENT_SELFTEST: 3/3 pass, exit 0 | `.ufo/waves/round-40/settlement-receipt.json` records SETTLED exit 0; `.ufo/waves/round-41/settlement-receipt.json` records UNSETTLED exit 1; red and green receipt literals live in the tool selftest | caller-chosen receipt is read only; verdict on stdout; nothing written, no TMPDIR use | tameshi |
+| wave-route-mix | gate | `python3 tools/wave-route-mix.py --spec SPEC.json --config CONFIG.yml --max-share 0.40` | 0 clean (no provider above the bound, every role routed, at least one seat); 1 failed (a provider above --max-share, an unrouted role, or an empty seat list); 2 could-not-evaluate (unreadable spec or config); 64 could-not-evaluate (usage: unknown flag, missing --spec, --max-share outside (0,1]) | `python3 tools/wave-route-mix.py --selftest` → ROUTEMIX_SELFTEST: 8/8 pass | none — the expected case verdicts are literals in the selftest; no repo file is read | nothing — read-only: JSON on stdout under --json plus one ROUTEMIX summary line on stderr; selftest writes no files | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- corpus/README.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/corpus/README.md b/corpus/README.md
index a1857733..c10d1bd5 100644
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -607,2 +607,28 @@ F10 (PBT generators for gate fixtures): open → **held (round 49)** for its sta
 
 F6 (fixture minimization for survivors): open → **held (round 50)** for the method on killing cases — one shrinker that reduces a gate's killing case to a 1-minimal sub-case and states its run cost — conditioned on the round-50 deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; the round-29 B5 survivor is not discharged (it stays masked, `knowledge/survivor-fixture-minimization.md:53,57`), and if that receipt prints anything else this line is void as of round 50
+
+## Round 51 — frontier status table re-stated (calibration)
+
+The status table at `corpus/README.md:76-87` is superseded as a whole: its status cells were never re-stated after the rounds that moved them (rounds 1, 21, 25, 27, 38, 49, 50), so seven of the ten cells no longer read what the lane later declared. Nothing above this line is rewritten — the coverage map is corrected by appending only — and each row below carries the latest wording with a pointer to the lines that declare its status.
+
+| id | ground | candidate sources | status | next falsifiable move (before → after) |
+|---|---|---|---|---|
+| F1 | external mutation-score semantics + report interop | S001, S002, S086, S087 | held (round 25) — README.md:385-390; F1b open | before: emit one ledger leg as schema JSON and validate it (validator unavailable in round 1) → after: held for the eight recorded ledger legs (round 25, README.md:386-390); remaining: the emitted report names a target by basename with no lane or revision pin (round 26, README.md:412-413) and the 35 recorded survivors stay unclassified for NoCoverage (README.md:396) |
+| F2 | witness-scoped kill verdicts / bash mutation tooling | S006, S257 | partly held (round 1) — README.md:115 | before: the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8 → after: still unmeasured; the existing bash leg's declared-witness study is retained separately (README.md:128) and round 45 adds GoogleTest's primer as an upstream instance of the split (README.md:563) |
+| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040, S256, S258-S264 | open — README.md:589 | before: one control per sweep → after: N ≥ 3 byte-identical controls, or a named mismatch: still unmeasured; the rounds 45-47 entries add upstream statements and published measurements only (README.md:558-589) |
+| F4 | golden / snapshot fixture discipline | S013, S014, S015, S016, S017, S045, S105-S108, S132, S152, S153, S154 | partly held (round 38) — README.md:492-495 | before: update paths that write expected values without an explicit flag: unmeasured → after: the write-path census counted 99 live write sites with 0 unflagged (round 39, README.md:503), and rounds 40-41 added two successor tools; remaining: the cmp and git diff --exit-code lattices, and the shutil.* and handle.write classes outside v2's pattern (README.md:511, README.md:521-523) |
+| F5 | hermetic environment normalization | S015, S016, S028, S079 | Core (round 21) — README.md:330-335; for the nine frozen files | before: runner selftest host vs env -i LANG=C TZ=UTC identical (H3, round 1) → after: the nine frozen files measured the same way (nine clean controls, round 21); the three kumitate gates cite-check, surface-probe and proxy-check stay unmeasured (README.md:335-336) |
+| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608 | before: B5 probe fixture size: unmeasured → after: held for the method on killing cases — one shrinker to a 1-minimal sub-case with a stated run cost (round 50); the round-29 B5 survivor is not discharged and stays masked → next: shrink on a second gate, or discharge B5 |
+| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041, S047 | open — README.md:255-256 | before: pin-level cadence only → after: per-leg reuse decisions classified: not reached; round 13 acquired only the content-disposition prerequisite and round 17 moved no row (README.md:255-256) |
+| F8 | oracle anchoring as a survivor class | S012, S090, S091 | partly held (round 27) — README.md:424-427 | before: 0 test-oracle lines → after: one survivor classified against an independently anchored expectation, one gate at one pin (round 27); bounded to 3 of 4 survivors anchored in the gate's header contract and 1 by convention only (round 29, README.md:433-437) → next: anchor the hole calls on the other eight recorded legs |
+| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open — README.md:86 | before: no LLM-specific search run yet (U) → after: bounded pilot with an independent outcome check: untouched; round 43 states F9 is not touched (README.md:555-556) |
+| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599 | before: no PBT fixture method → after: one generator against a named fixture gate, conditioned on the round-49 deciding receipt printing C2_R49_PASS=true; next: a second gate, or shrinking (README.md:599) |
+
+S022 (`queued` → `mined`): the row's used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`, which cites it (round 50), so the status column is corrected to CORPUS.md's own reading — mined = cited by at least one path in used-by.
+No other SOURCES row changes status here, and every used-by path of a mined row exists at this revision.
+
+## Round 51 — tenth recorded mutation case (depth)
+
+| Entry / ground | Admission and exact scope | Evidence |
+|---|---|---|
+| `knowledge/mutation-case-kagi-drift-pins.md` / Core (recorded legs) | source-headed entry citing mined S272 (the pinned kagi host-drift gate) and S273 (Bash `errexit`/`pipefail` semantics), new this round; tenth ledger leg `bash-drift-pins`, 2/10 killed on the 13-case selftest under the recorded `sandbox-$DEFECT_ID` suite; independent A/B probe shows K_GONE_ARM, K_AMBIG_GT and K_SHAPE_OPTIN are environment-masked and become killed under a neutral sandbox (5/10), so the reported 20% must not be read as gate kill strength; seven of ten predictions held, five other survivors have off-suite witnesses | `.ufo/evidence/round-51/c2/`; `.ufo/waves/round-51/w1/T51LabSandboxLeak.md`, `T51ScribeEntry/` |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-51/no-harm.sh` (exit 0), output:
```
#!/bin/bash
# Round-51 no-harm monitors. Usage: no-harm.sh LANE REV. Every line prints "NOHARM <name> <observed> <ok|RED>".
# Eleven monitors, carried from round 50 with three declared re-bases (frozen before any seat ran):
#  - commandD: depth_score >= 9 (C2 may raise it to 10; below 9 is harm);
#  - r45-freshness: the axis score floor(10*fresh/population) >= 9 with fresh >= 71. Round 50 pinned the exact
#    population 73; routed defect R50.1 (S022 queued -> mined) lawfully grows the population to 74, which leaves the
#    score at 9 (71/74), so the exact-population pin is replaced by the score it guarded;
#  - tools-scope: only M:tools/mutate-and-run.sh (C2's tenth leg) may change under tools/, plus (amendment 2) the four
```

### R50.2: supported
6d8c11e adds full shrink-case and pbt-staged-id rows, including exits, selftests, pins and write scope; both remain at tip. The round-12 scope sentence is local to its historical block, not evidence these later rows are absent.

Proposed fix: No status change.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SKILL.md` (exit 0); output lines 2201-2201:
```
| shrink-case | probe | `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json` | 0 shrunk (report written); 1 selftest checks failed; 2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill) | `python3 tools/shrink-case.py --selftest` → SHRINK_SELFTEST: cases=21 failed=0 | `tools/pbt-staged-id.py` generator imported beside the tool; `tools/staged-id-guard.py` and `.ufo/evidence/round-49/c2/panel.json` for the M02 leg; expected edit literals in the tool source | caller-chosen --out FILE; tempfile.mkdtemp roots under TMPDIR for guard runs and selftest; lane read-only except the CPython bytecode cache (tools/__pycache__) the import of the generator may write | tameshi |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SKILL.md` (exit 0); output lines 2193-2193:
```
| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root (pbt-staged-id-); selftest scratch under TMPDIR | tameshi |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-50-verifier-spotcheck.md` (exit 0), output:
```
2. **Gate/probe registry gap.** `tools/shrink-case.py` (round 50) and `tools/pbt-staged-id.py` (round 49) both expose selftests but have no row in `SKILL.md` `### Gate/probe registry` (`:1499-1509`, whose scope sentence still reads "these round-12 instruments"); `git diff --quiet e3729de8 616dee67 -- SKILL.md` → unchanged. Add rows (kind, entry command, verdict map incl. exit 2, selftest spelling, pinned values, write scope) per PROTOCOL §Gate standard, Registry.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- corpus/SOURCES.md corpus/lessons/round-51.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/corpus/SOURCES.md b/corpus/SOURCES.md
index 368f65e7..6d2f634f 100644
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -31,5 +31,5 @@ rows only, and a row is a claim opened in the round that writes it.
 | S020 | Property-based testing in Python: empirical insights (de Oliveira, Corgozinho, Rocha, Valente; EMSE 2026) — https://doi.org/10.1007/s10664-026-10953-w | paper | A | PBT usage in 244 Python projects | Abstract; §6.2 and Table 2 (author copy https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf, fetched 2026-10-19; Springer served an anti-bot challenge) | 367 PBTs from 244 projects in nine categories with Test Oracle at 29.97%; data generation is the main challenge (36.62% of SO questions); Ghostwriter fully automates only 18.23% | queued | 2026-10-19 | 365d | — |
 | S021 | Agentic Property-Based Testing (Maaz, DeVoe, Hatfield-Dodds, Carlini; arXiv 2510.09907) — https://arxiv.org/abs/2510.09907 | paper | A | agentic PBT bug validity on real packages | Abstract, arXiv:2510.09907v1 (submitted 2025-10-10) | an LLM agent infers properties from code and docs, writes Hypothesis tests and reflects before reporting: 56% of reports were valid bugs; ranking lifts the top-21 validity to 86% | queued | 2026-10-19 | 180d | — |
-| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | queued | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
+| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
 | S023 | Shrink Ray README (DRMacIver/shrinkray) — https://github.com/DRMacIver/shrinkray | code | A | shrinkray's interestingness-driven reduction | README §Usage and §LLM mode @ page currentOid 5fe6ee135d732e4b7758b3dbe3d91428523018fb, fetched 2026-10-19 | a reducer driven by any executable interestingness test (exit 0 = interesting); parallel multi-format passes; local LLM proposals are accepted only when the interestingness test still passes | queued | 2026-10-19 | 90d | — |
 | S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | mined | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md, corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
@@ -145,4 +145,6 @@ rows only, and a row is a claim opened in the round that writes it.
 | S270 | Property-based testing for functional programs (Smallbone; Chalmers University of Technology Technical Report 76L, ISSN 1652-876X, 2011) — https://smallbone.se/papers/lic.pdf | paper | B | F10 generator craft — the generator bounds which laws a random search can reach, an author's own report on QuickCheck-family generator quality and distribution | §2.10 Generating Test Data, p. 34 @ Technical Report 76L, 2011, author-served PDF 116 pp fetched 2026-10-26, sha256 eaee48f9, snapshot .ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf | generator quality bounds the search: an ill-fitting list generator never produces the cases that separate two functions, and drawing elements from a small domain fixes it | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
 | S271 | Simplifying and Isolating Failure-Inducing Input (Zeller, Hildebrandt; IEEE TSE 28(2):183-200, 2002; DOI 10.1109/32.988498) — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf | paper | A | F6 fixture shrinking — the 1-minimal sub-case criterion for a reduced fixture and the test-run cost of reaching it | §I Introduction, Simplification of test cases paragraph (mirror PDF p. 1); §III-A Minimal Test Cases, Definition 10 (mirror PDF p. 4); §III-C Properties of ddmin, Propositions 11 and 12 (mirror PDF p. 6); §IV-B Figs. 11-12 @ IEEE TSE vol. 28 no. 2, February 2002, DOI 10.1109/32.988498 (running head on the carrier; the mirror carries no journal folios); course-mirror PDF fetched 2026-10-26, sha256 7ed0c812, 247738 bytes, snapshot .ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf | a failing test case is 1-minimal when removing any single change makes the failure disappear, ddmin returns such a case, and the reduction is itself a cost measured in test runs | mined | 2026-10-26 | 730d | corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
+| S272 | kagi `corpus/drift-pins.sh` (fleet gate, read-only) — kagi-shokunin/corpus/drift-pins.sh | code | A | the gate's own verdict vocabulary, exit map and hermetic scratch-tree selftest at the measured revision | :19 (exit map), :118-259 (verify), :374-446 (selftest), :400-405 (the exit-and-grep assertion) @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb, 451 lines, mode 100755; unchanged at kagi HEAD 69b61db46be4ed955994f6f1d1cba522bc5f4e97) | a host-drift gate anchors on committed baselines instead of live fingerprints and proves each verdict class in a scratch tree; its 13-case `--selftest` prints `DRIFT_SELFTEST: PASS (13 cases)` and asserts exit code plus an unanchored `grep -q` for the verdict word, not its position in the output | mined | 2026-10-26 | 180d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
+| S273 | GNU Bash Reference Manual, The Set Builtin (author copy of the manual, Edition 5.3, last updated 18 May 2025) — https://tiswww.case.edu/php/chet/bash/bashref.html (the gnu.org node page https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html was unreachable on 2026-10-27 UTC: eight attempts, HTTP 000, 0 bytes, connect timeouts — https and http, with and without www, IPv4-forced, and the single-page manual alike) | docs | A | Bash `errexit` (`-e`) and `pipefail`: which failing commands end a non-interactive shell, the listed non-exits, and a pipeline's return value | §The Set Builtin `-e` item (single-page copy lines 6547-6570) and `pipefail` item (lines 6706-6710); same text in the Savannah texi pinned by S097 at `@item -e` lines 5929-5948 and `@item pipefail` lines 6062-6066 (re-fetched 2026-10-27, sha256 f3d37d57, byte-identical to S097); a command of assignments only takes its status at §Simple Commands lines 3675-3677 (copy lines 4172-4173) @ author copy fetched 2026-10-27T00:22Z UTC, two fetches byte-identical (1040870 bytes; SHA-256 b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4), snapshot .ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html | Quotes (each at most 25 words), `-e`: "Exit immediately if a pipeline ... returns a non-zero status"; non-exits: "The shell does not exit if the command that fails is ... any command in a pipeline but the last"; the parenthetical tying that to pipefail: "any command in a pipeline but the last (subject to the state of the pipefail shell option)"; `pipefail`: "the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status"; assignments-only status: "the exit status of the last command substitution performed" | mined | 2026-10-26 | 365d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
 
 ## Paths
@@ -497,2 +499,4 @@ Round 46: three rows added, S258 (arXiv 2504.16777, Systemic Flakiness), S259 (t
 - Round 50: one row added by document from the shokuknow `corpus-expansion-1` package (theme F6), S271 (Zeller & Hildebrandt, IEEE TSE 2002, DOI 10.1109/32.988498; staged S167, which collides with nothing and is not reused), re-opened 2026-10-26 from the course mirror (HTTP 200, sha256 7ed0c812) with the snapshot under `.ufo/waves/round-50/w1/T50ScribeRows.src/`; the Zeller lead in the leads list above now has this row, and the earlier stop note (author PDFs timed out, ResearchGate 403, DOI metadata only) is superseded by the mirror fetch. S022 used-by — → the F6 pilot entry (its status stays queued: promoting it would move the frozen round-45 freshness population, a no-harm monitor); S024 used-by gains the two round-50 F6 entries (logged old → new in `corpus/lessons/round-50.md` `## Gate`). Id collision check: `reg-ids` 130, `staged-ids` 103, collisions 8 (S153-S160) (`.ufo/waves/round-50/w1/T50ExecIdGuard/`).
 - Next unused id: S272 (staged ids S161-S255 stay reserved by document for the package).
+Round 51: two tier-A rows added on the core tenth-leg case, S272 (kagi `corpus/drift-pins.sh`, code, pinned rev `e64e81b8`) and S273 (GNU Bash Reference Manual, §The Set Builtin, author copy, docs; gnu.org page was unreachable and the opened carrier is named in the row), both mined and opened this round; snapshots / fetch receipts under `.ufo/waves/round-51/w1/T51ScribeRowGate*` and `T51ScribeRowBash/`. Used by `corpus/knowledge/mutation-case-kagi-drift-pins.md`. S022 status `queued` → `mined` (used-by already cited `corpus/knowledge/fixture-shrinking-pilot.md`; reason: CORPUS.md defines mined as cited by ≥1 used-by path); logged in `corpus/lessons/round-51.md`. Registry rows 131 → 133.
+- Next unused id: S274 (staged ids S161-S255 stay reserved by document for the package).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- SKILL.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/SKILL.md b/SKILL.md
index 5f985e2f..e97f350c 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -2135,2 +2135,37 @@ the kill came from an absolute assert on the masked region.
 |---|---|---|---|
 | `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+
+#### Gate/probe registry — round 51
+
+| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
+|---|---|---|---|---|---|---|---|
+| bash declared-witness study | probe | `python3 tools/bash-witness-study.py check` (add --evidence DIR to grade another copy of the frozen evidence) | 0 clean; 1 failed (tamper, digest drift, summary/raw mismatch, unresolved sweep); 2 could-not-evaluate (missing input, pin mismatch, runner SETUP); 64 could-not-evaluate (usage) | `python3 tools/bash-witness-study.py selftest` → VERDICT: is the last line, preceded by WITNESS_SELFTEST: 51/51 pass | `.ufo/evidence/round-12/BashWitness/declaration.json` (frozen target, spec and runner sha256), `.ufo/evidence/round-12/BashWitness/declared.tsv` (declared-witness rows, sha pinned in declaration.json), `.ufo/evidence/round-12/BashWitness/summary.json`, `.ufo/evidence/round-12/BashWitness/manifest.json`, `tools/mutate-and-run.sh` (pinned runner digest, the spec is extracted from its heredoc); the DECLARED_WITNESSES rows are literals in the tool | caller-chosen --evidence DIR for declare, run and rerun plus the extended manifest; check and count read-only; selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored); sibling kagi object store read-only | tameshi |
+| command binding receipts | gate | `python3 tools/command-binding.py --bundle BUNDLE.json --expected EXPECTED.json --json` | 0 clean; 1 failed binding or outcome; 2 could-not-evaluate (invalid shape or integrity); 64 could-not-evaluate (usage) | `python3 tools/command-binding.py --selftest` → finding id COMMAND_BINDING_SELFTEST: in the last stdout line | `.ufo/evidence/round-23/extra-cases.json`, `.ufo/evidence/round-24/extra-cases.json`; literal expected exits and finding IDs in the tool selftest | read-only over the lane; selftest writes one isolated bundle/expected pair under TMPDIR | tameshi |
+| context receipt replay | gate | `python3 tools/context-capture.py --check` (frozen pin) or the same invocation with --receipt FILE --expected FILE | 0 clean; 1 failed; 2 could-not-evaluate; 64 could-not-evaluate (usage) | `python3 tools/context-capture.py --selftest` → SELFTEST: PASS (49/49 cases) | `.ufo/evidence/round-14/context-receipt.json`; literal digest 05cb55b8… and id/exit pin inside the tool | none during --check; selftest fixtures under /tmp/context-capture-selftest-*, removed in finally | tameshi |
+| environment-profile differential | gate | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out DIR/receipt.json --jobs 3` | 0 clean; 1 failed; 2 and 64 could-not-evaluate | `python3 tools/env-diff.py --selftest` → exit 0, last line ENVDIFF_SELFTEST: 9/9 pass | `.ufo/evidence/round-21/c2-contract.json`, `.ufo/evidence/round-21/f5/receipt.json`; literal expected classifications in the tool selftest | caller-chosen `--out` FILE plus sandboxes under `/tmp/tameshi-r21-envdiff.*` and TMPDIR-respecting selftest trees; lane trees read-only | tameshi |
+| evidence disposition accounting | gate | `python3 tools/evidence-disposition.py --root LANE --dispositions FILE` (lane run: --root . --dispositions .ufo/evidence/round-18/dispositions.json) | 0 clean; 1 failed semantic expectation; 2 could-not-evaluate (missing, unreadable, malformed, tampered or path-invalid input, invalid schema, internal failure); 64 could-not-evaluate (usage) | `python3 tools/evidence-disposition.py --selftest` → finding id SELFTEST: exit 0, 66/66 cases in about 3 s at rev 84aa673a; needs jj on PATH | `.ufo/evidence/round-13/expected.json`, `.ufo/evidence/round-13/verification.json`, `.ufo/evidence/round-13/producer-oracle-repair.json`, `.ufo/evidence/round-18/dispositions.json`; expected ids and exits are literals in the tool selftest | none in the lane — read-only over --root; selftest fixtures under /tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure | tameshi |
+| golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
+| mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root (pbt-staged-id-); selftest scratch under TMPDIR | tameshi |
+| pin disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root FLEET` | 0 clean; 1 failed (selftest FAIL only); 2 could-not-evaluate (usage, invalid or mismatched manifest, fleet root not a directory) | `python3 tools/pin-disposition.py --selftest` → SELFTEST: PASS n/n finding id SELFTEST: | `.ufo/evidence/round-13/pin-manifest.json` | read-only over the named fleet root; selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures, removed on PASS | tameshi |
+| round-20 receipt-window measure | gate | `python3 tools/receipt-measure.py --repo REPO --rev REV --json` | 0 clean, six items PASS at REV; 1 failed, including an absent REPO or unresolvable REV which is graded as six FAIL items rather than could-not-evaluate; 2 could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other arguments | `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST: 10/10 pass | `.ufo/evidence/round-20/contract.json`, `.ufo/evidence/round-20/stage/measure.py`, `.ufo/evidence/round-20/stage/receipt-window.py`, `tools/receipt-window.py`, `.ufo/evidence/round-20/final/receipts.json`, `.ufo/evidence/round-20/final/historical-receipts.json`, `.ufo/evidence/round-20/final/receipt-window-selftest.json`, `.ufo/waves/round-20/dispatch.json` | reads REPO at REV; no repo writes; scratch fixture trees under TMPDIR only, prefixes `receipt-measure-selftest.*` and `tameshi-r20-measure.*` | tameshi |
+| receipt-window validity | gate | `python3 tools/receipt-window.py --contract CONTRACT_JSON --receipts RECEIPTS_JSON` (add --json for one machine-readable verdict object) | 0 clean; 1 failed (findings); 2 could-not-evaluate (contract or receipts invalid, also argparse usage); 64 usage (missing --contract or --receipts) | `python3 tools/receipt-window.py --selftest` → RECEIPT_WINDOW_SELFTEST: last non-empty stdout line reads RECEIPT_WINDOW_SELFTEST: 20/20 pass with exit 0 | `.ufo/evidence/round-20/contract.json` expectations and instrument shas; `.ufo/evidence/round-20/public-cli-cases.json` synthetic cases; `.ufo/evidence/round-20/final/receipts.json`; `.ufo/evidence/round-20/final/receipt-window-selftest.json` recorded 20/20 exit 0 | reads caller-chosen CONTRACT_JSON and RECEIPTS_JSON without writing; selftest writes only its TMPDIR temp tree | tameshi |
+| entry-registry walk | gate | `python3 tools/registry-check.py --rev HEAD` (add `--only NAME` to grade one row) | 0 clean; 1 failed; 2 could-not-evaluate (registry unreadable or invalid, root/rev/clone failure, only or tag miss); 64 usage | `python3 tools/registry-check.py --selftest` → finding id SELFTEST: last line SELFTEST: PASS (51 cases) at 84aa673 | `tools/registry.json`, `tools/registry-check.py` | selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored), removed afterwards; live --root mode runs registry rows inside LANE so rows may write there | tameshi |
+| frozen registry replay | gate | `python3 tools/registry-replay.py --run --repo . --rev REV --requirements .ufo/evidence/round-23/requirements.json --registry-baseline .ufo/evidence/round-23/registry-baseline.json --out DIR` | 0 clean; 1 failed (refused rows: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT; an uncaught traceback also exits 1); 2 could-not-evaluate (registry digest mismatch, frozen requirements drift, clone HEAD mismatch, INVALID_OBSERVATIONS); 64 could-not-evaluate (usage) | `python3 tools/registry-replay.py --selftest` → REGISTRY_REPLAY_SELFTEST: 10/10 pass | `.ufo/evidence/round-23/requirements.json`, `.ufo/evidence/round-23/registry-baseline.json`, `tools/registry-check.py` (runner digest taken from the clone copy that runs) | caller-selected `--out` DIR (observations.json, bundle.json, expected.json, live-dependent.json) plus a private clone under TMPDIR; row commands run inside that clone, whose fleet mirror symlinks the live siblings, so the run is not write-isolated from them; selftest under TMPDIR | tameshi |
+| repeated control agreement | gate | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`, or --snapshot DIR over a committed control snapshot | 0 clean (controls_match); 1 failed (controls_mismatch); 2 could-not-evaluate (baseline_nonzero, command_unavailable, snapshot_tampered, setup_error); 64 could-not-evaluate (invalid_usage) | `python3 tools/repeat-control.py --selftest` → SELFTEST: PASS (29 cases) at exit 0 | `.ufo/evidence/round-12/ControlGate/expected.json`, `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` | caller-chosen --out DIR, created fresh and never deleted; --snapshot DIR read-only; selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass) | tameshi |
+| round21 measure facade | gate | `python3 tools/round21-measure.py --claim c1 --repo DIR --rev REV --json` | 0 clean; 1 failed; 2 could-not-evaluate (setup or unknown rev); 64 could-not-evaluate (usage) | `python3 tools/round21-measure.py --selftest` → ROUND21_MEASURE_SELFTEST: 13/13 pass | `.ufo/evidence/round-21/c1-survivors.py`, `.ufo/evidence/round-21/c2-count.py`, `.ufo/evidence/round-21/c2-contract.json` | TMPDIR only (selftest fixtures and delegated counter receipts); target repo read-only | tameshi |
+| shrink-case | probe | `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json` | 0 shrunk (report written); 1 selftest checks failed; 2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill) | `python3 tools/shrink-case.py --selftest` → SHRINK_SELFTEST: cases=21 failed=0 | `tools/pbt-staged-id.py` generator imported beside the tool; `tools/staged-id-guard.py` and `.ufo/evidence/round-49/c2/panel.json` for the M02 leg; expected edit literals in the tool source | caller-chosen --out FILE; tempfile.mkdtemp roots under TMPDIR for guard runs and selftest; lane read-only | tameshi |
+| staged-id adoption guard | gate | `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged STAGED.md --json` (add `--map MAP.json` to validate a candidate adoption map) | 0 clean (answered, or admitted with `--map`); 1 failed (analysis refused, or map inadmissible); 2 could-not-evaluate (usage, missing flag, or setup refusal) | `python3 -I tools/staged-id-guard.py --selftest` → VERDICT: PASS at exit 0, FAIL at exit 1 (counter line STAGED_ID_GUARD_SELFTEST: cases=N failed=M) | none — expected values are the fixture literals SELFTEST_REGISTRY and SELFTEST_STAGED_* committed inside tools/staged-id-guard.py; no expected file on disk | read-only: no writes, no temp files, no lane writes; caller names the registry, staged and map paths and stdout/stderr is the whole output | tameshi |
+| tally audit v2 (mutation runner tally) | gate | `python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh` (add `--then-regression --workdir DIR` to also require the runner's REGRESSION line to name cases=legs) | 0 clean; 1 failed (audit FAIL or a selftest case failure); 2 could-not-evaluate (cannot audit, setup, usage); a timed-out then-regression reports 124 and folds to 2 | `python3 tools/tally-audit-v2.py --selftest` → TALLY_AUDIT_V2_SELFTEST: 22/22 pass, one seeded-fault case per check | none — expected tallies are literals of the tool's independent oracle and its 22 selftest seeds; audited surface defaults to `tools/mutate-and-run.sh` | lane read-only; scratch under TMPDIR (tally-audit-v2.*, removed in finally); the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires; --then-regression writes only the runner's caller-named --workdir | tameshi |
+| tally audit v3 | gate | `python3 tools/tally-audit-v3.py --runner tools/mutate-and-run.sh` | 0 clean; 1 failed; 2 could-not-evaluate (SETUP: runner unparsable, tally harness structure missing, or argparse usage) | `python3 tools/tally-audit-v3.py --selftest` → TALLY_AUDIT_V3_SELFTEST: 35/35 pass | `tools/mutate-and-run.sh` is the only input read; expected REF_BLOCK, REF_NAMES and the 35 seeded-case panel are literals in the tool, and `.ufo/evidence/round-32/heldout/` is the committed provenance of those seeds (not read at run time) | audit and selftest scratch under TMPDIR, plus one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX allocated to witness the runner shape and removed at exit; the audited runner is never edited; `--then-regression` lets the runner create its own auto root or caller-chosen --workdir DIR | tameshi |
+| tally audit undercount guard | gate | `python3 tools/tally-audit.py` audits the runner `tools/mutate-and-run.sh` beside it; `--runner PATH`, `--then-regression --workdir DIR` accepted | 0 clean; 1 failed; 2 could-not-evaluate (cannot audit, usage, or regression SETUP); 64 could-not-evaluate (runner usage error surfaced through --then-regression) | `python3 tools/tally-audit.py --selftest` → TALLY_AUDIT_SELFTEST: 11/11 pass | `tools/tally-audit.py` REF_BLOCK reference tally block and leg-name panel are literals in the tool; audited `tools/mutate-and-run.sh` read-only | TMPDIR scratch dirs with prefix tally-audit, removed on exit; --then-regression hands its workdir to the runner | tameshi |
+| traced input surface | probe | `python3 tools/trace-inputs.py --root LANE --out RECEIPT.json -- COMMAND ARG...` | 0 clean; 1 failed (selftest check); 2 could-not-evaluate (setup: root or cwd not a directory, strace missing, no successful root execve); 64 could-not-evaluate (usage) | `python3 tools/trace-inputs.py --selftest` → SELFTEST: n/n on exit 0 | none — expected values are literals in the selftest | caller-chosen --out FILE (parent directories created); private trace-inputs-run-* tempdir outside --root, deleted on exit; selftest tree under TMPDIR | tameshi |
+| wave accounting | gate | `python3 tools/wave-accounting.py --bundle BUNDLE.json --expected EXPECTED.json` | 0 clean; 1 failed invariant; 2 could-not-evaluate (invalid, unavailable or tampered input); 64 could-not-evaluate (usage) | `python3 tools/wave-accounting.py --selftest` → FINDING: SELFTEST_PASS, 8/8 frozen plus 16/16 supplemental cases | `.ufo/evidence/round-22/measure.py`, `.ufo/evidence/round-22/accounting-extra-cases.json` | stdout only; caller-chosen `--bundle`/`--expected` read-only, selftest fixtures under isolated TMPDIR | tameshi |
+| wave parent settlement | gate | `python3 tools/wave-parent-settle.py --receipt RECEIPT.json` | 0 clean (SETTLED); 1 failed (UNSETTLED); 2 could-not-evaluate (usage, or --receipt not supplied) | `python3 tools/wave-parent-settle.py --selftest` → WAVE_PARENT_SELFTEST: 3/3 pass, exit 0 | `.ufo/waves/round-40/settlement-receipt.json` records SETTLED exit 0; `.ufo/waves/round-41/settlement-receipt.json` records UNSETTLED exit 1; red and green receipt literals live in the tool selftest | caller-chosen receipt is read only; verdict on stdout; nothing written, no TMPDIR use | tameshi |
+| wave-route-mix | gate | `python3 tools/wave-route-mix.py --spec SPEC.json --config CONFIG.yml --max-share 0.40` | 0 clean (no provider above the bound, every role routed, at least one seat); 1 failed (a provider above --max-share, an unrouted role, or an empty seat list); 2 could-not-evaluate (unreadable spec or config); 64 could-not-evaluate (usage: unknown flag, missing --spec, --max-share outside (0,1]) | `python3 tools/wave-route-mix.py --selftest` → ROUTEMIX_SELFTEST: 8/8 pass | none — the expected case verdicts are literals in the selftest; no repo file is read | nothing — read-only: JSON on stdout under --json plus one ROUTEMIX summary line on stderr; selftest writes no files | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- corpus/README.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/corpus/README.md b/corpus/README.md
index a1857733..c10d1bd5 100644
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -607,2 +607,28 @@ F10 (PBT generators for gate fixtures): open → **held (round 49)** for its sta
 
 F6 (fixture minimization for survivors): open → **held (round 50)** for the method on killing cases — one shrinker that reduces a gate's killing case to a 1-minimal sub-case and states its run cost — conditioned on the round-50 deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; the round-29 B5 survivor is not discharged (it stays masked, `knowledge/survivor-fixture-minimization.md:53,57`), and if that receipt prints anything else this line is void as of round 50
+
+## Round 51 — frontier status table re-stated (calibration)
+
+The status table at `corpus/README.md:76-87` is superseded as a whole: its status cells were never re-stated after the rounds that moved them (rounds 1, 21, 25, 27, 38, 49, 50), so seven of the ten cells no longer read what the lane later declared. Nothing above this line is rewritten — the coverage map is corrected by appending only — and each row below carries the latest wording with a pointer to the lines that declare its status.
+
+| id | ground | candidate sources | status | next falsifiable move (before → after) |
+|---|---|---|---|---|
+| F1 | external mutation-score semantics + report interop | S001, S002, S086, S087 | held (round 25) — README.md:385-390; F1b open | before: emit one ledger leg as schema JSON and validate it (validator unavailable in round 1) → after: held for the eight recorded ledger legs (round 25, README.md:386-390); remaining: the emitted report names a target by basename with no lane or revision pin (round 26, README.md:412-413) and the 35 recorded survivors stay unclassified for NoCoverage (README.md:396) |
+| F2 | witness-scoped kill verdicts / bash mutation tooling | S006, S257 | partly held (round 1) — README.md:115 | before: the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8 → after: still unmeasured; the existing bash leg's declared-witness study is retained separately (README.md:128) and round 45 adds GoogleTest's primer as an upstream instance of the split (README.md:563) |
+| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040, S256, S258-S264 | open — README.md:589 | before: one control per sweep → after: N ≥ 3 byte-identical controls, or a named mismatch: still unmeasured; the rounds 45-47 entries add upstream statements and published measurements only (README.md:558-589) |
+| F4 | golden / snapshot fixture discipline | S013, S014, S015, S016, S017, S045, S105-S108, S132, S152, S153, S154 | partly held (round 38) — README.md:492-495 | before: update paths that write expected values without an explicit flag: unmeasured → after: the write-path census counted 99 live write sites with 0 unflagged (round 39, README.md:503), and rounds 40-41 added two successor tools; remaining: the cmp and git diff --exit-code lattices, and the shutil.* and handle.write classes outside v2's pattern (README.md:511, README.md:521-523) |
+| F5 | hermetic environment normalization | S015, S016, S028, S079 | Core (round 21) — README.md:330-335; for the nine frozen files | before: runner selftest host vs env -i LANG=C TZ=UTC identical (H3, round 1) → after: the nine frozen files measured the same way (nine clean controls, round 21); the three kumitate gates cite-check, surface-probe and proxy-check stay unmeasured (README.md:335-336) |
+| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608 | before: B5 probe fixture size: unmeasured → after: held for the method on killing cases — one shrinker to a 1-minimal sub-case with a stated run cost (round 50); the round-29 B5 survivor is not discharged and stays masked → next: shrink on a second gate, or discharge B5 |
+| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041, S047 | open — README.md:255-256 | before: pin-level cadence only → after: per-leg reuse decisions classified: not reached; round 13 acquired only the content-disposition prerequisite and round 17 moved no row (README.md:255-256) |
+| F8 | oracle anchoring as a survivor class | S012, S090, S091 | partly held (round 27) — README.md:424-427 | before: 0 test-oracle lines → after: one survivor classified against an independently anchored expectation, one gate at one pin (round 27); bounded to 3 of 4 survivors anchored in the gate's header contract and 1 by convention only (round 29, README.md:433-437) → next: anchor the hole calls on the other eight recorded legs |
+| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open — README.md:86 | before: no LLM-specific search run yet (U) → after: bounded pilot with an independent outcome check: untouched; round 43 states F9 is not touched (README.md:555-556) |
+| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599 | before: no PBT fixture method → after: one generator against a named fixture gate, conditioned on the round-49 deciding receipt printing C2_R49_PASS=true; next: a second gate, or shrinking (README.md:599) |
+
+S022 (`queued` → `mined`): the row's used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`, which cites it (round 50), so the status column is corrected to CORPUS.md's own reading — mined = cited by at least one path in used-by.
+No other SOURCES row changes status here, and every used-by path of a mined row exists at this revision.
+
+## Round 51 — tenth recorded mutation case (depth)
+
+| Entry / ground | Admission and exact scope | Evidence |
+|---|---|---|
+| `knowledge/mutation-case-kagi-drift-pins.md` / Core (recorded legs) | source-headed entry citing mined S272 (the pinned kagi host-drift gate) and S273 (Bash `errexit`/`pipefail` semantics), new this round; tenth ledger leg `bash-drift-pins`, 2/10 killed on the 13-case selftest under the recorded `sandbox-$DEFECT_ID` suite; independent A/B probe shows K_GONE_ARM, K_AMBIG_GT and K_SHAPE_OPTIN are environment-masked and become killed under a neutral sandbox (5/10), so the reported 20% must not be read as gate kill strength; seven of ten predictions held, five other survivors have off-suite witnesses | `.ufo/evidence/round-51/c2/`; `.ufo/waves/round-51/w1/T51LabSandboxLeak.md`, `T51ScribeEntry/` |
```

### R50.3: supported
6d8c11e adds the superseding frontier table; tip README:621 and :625 explicitly say F6 held round 50 and F10 held round 49. A superseding table was expressly accepted by the routed item.

Proposed fix: No status change.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/README.md` (exit 0); output lines 621-621:
```
| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608 | before: B5 probe fixture size: unmeasured → after: held for the method on killing cases — one shrinker to a 1-minimal sub-case with a stated run cost (round 50); the round-29 B5 survivor is not discharged and stays masked → next: shrink on a second gate, or discharge B5 |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/README.md` (exit 0); output lines 625-625:
```
| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599 | before: no PBT fixture method → after: one generator against a named fixture gate, conditioned on the round-49 deciding receipt printing C2_R49_PASS=true; next: a second gate, or shrinking (README.md:599) |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-50-verifier-spotcheck.md` (exit 0), output:
```
3. **Frontier table stale.** `corpus/README.md:83` (F6) and `:87` (F10) still read `open`, while the appended sections at `:599` and `:608` declare them held (round 49, round 50). Append a superseding table or a note so the coverage map's table agrees with its own sections (PROTOCOL §Evidence standard, corrections sweep every mention).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- corpus/SOURCES.md corpus/lessons/round-51.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/corpus/SOURCES.md b/corpus/SOURCES.md
index 368f65e7..6d2f634f 100644
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -31,5 +31,5 @@ rows only, and a row is a claim opened in the round that writes it.
 | S020 | Property-based testing in Python: empirical insights (de Oliveira, Corgozinho, Rocha, Valente; EMSE 2026) — https://doi.org/10.1007/s10664-026-10953-w | paper | A | PBT usage in 244 Python projects | Abstract; §6.2 and Table 2 (author copy https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf, fetched 2026-10-19; Springer served an anti-bot challenge) | 367 PBTs from 244 projects in nine categories with Test Oracle at 29.97%; data generation is the main challenge (36.62% of SO questions); Ghostwriter fully automates only 18.23% | queued | 2026-10-19 | 365d | — |
 | S021 | Agentic Property-Based Testing (Maaz, DeVoe, Hatfield-Dodds, Carlini; arXiv 2510.09907) — https://arxiv.org/abs/2510.09907 | paper | A | agentic PBT bug validity on real packages | Abstract, arXiv:2510.09907v1 (submitted 2025-10-10) | an LLM agent infers properties from code and docs, writes Hypothesis tests and reflects before reporting: 56% of reports were valid bugs; ranking lifts the top-21 validity to 86% | queued | 2026-10-19 | 180d | — |
-| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | queued | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
+| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
 | S023 | Shrink Ray README (DRMacIver/shrinkray) — https://github.com/DRMacIver/shrinkray | code | A | shrinkray's interestingness-driven reduction | README §Usage and §LLM mode @ page currentOid 5fe6ee135d732e4b7758b3dbe3d91428523018fb, fetched 2026-10-19 | a reducer driven by any executable interestingness test (exit 0 = interesting); parallel multi-format passes; local LLM proposals are accepted only when the interestingness test still passes | queued | 2026-10-19 | 90d | — |
 | S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | mined | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md, corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
@@ -145,4 +145,6 @@ rows only, and a row is a claim opened in the round that writes it.
 | S270 | Property-based testing for functional programs (Smallbone; Chalmers University of Technology Technical Report 76L, ISSN 1652-876X, 2011) — https://smallbone.se/papers/lic.pdf | paper | B | F10 generator craft — the generator bounds which laws a random search can reach, an author's own report on QuickCheck-family generator quality and distribution | §2.10 Generating Test Data, p. 34 @ Technical Report 76L, 2011, author-served PDF 116 pp fetched 2026-10-26, sha256 eaee48f9, snapshot .ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf | generator quality bounds the search: an ill-fitting list generator never produces the cases that separate two functions, and drawing elements from a small domain fixes it | mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md |
 | S271 | Simplifying and Isolating Failure-Inducing Input (Zeller, Hildebrandt; IEEE TSE 28(2):183-200, 2002; DOI 10.1109/32.988498) — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf | paper | A | F6 fixture shrinking — the 1-minimal sub-case criterion for a reduced fixture and the test-run cost of reaching it | §I Introduction, Simplification of test cases paragraph (mirror PDF p. 1); §III-A Minimal Test Cases, Definition 10 (mirror PDF p. 4); §III-C Properties of ddmin, Propositions 11 and 12 (mirror PDF p. 6); §IV-B Figs. 11-12 @ IEEE TSE vol. 28 no. 2, February 2002, DOI 10.1109/32.988498 (running head on the carrier; the mirror carries no journal folios); course-mirror PDF fetched 2026-10-26, sha256 7ed0c812, 247738 bytes, snapshot .ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf | a failing test case is 1-minimal when removing any single change makes the failure disappear, ddmin returns such a case, and the reduction is itself a cost measured in test runs | mined | 2026-10-26 | 730d | corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
+| S272 | kagi `corpus/drift-pins.sh` (fleet gate, read-only) — kagi-shokunin/corpus/drift-pins.sh | code | A | the gate's own verdict vocabulary, exit map and hermetic scratch-tree selftest at the measured revision | :19 (exit map), :118-259 (verify), :374-446 (selftest), :400-405 (the exit-and-grep assertion) @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb, 451 lines, mode 100755; unchanged at kagi HEAD 69b61db46be4ed955994f6f1d1cba522bc5f4e97) | a host-drift gate anchors on committed baselines instead of live fingerprints and proves each verdict class in a scratch tree; its 13-case `--selftest` prints `DRIFT_SELFTEST: PASS (13 cases)` and asserts exit code plus an unanchored `grep -q` for the verdict word, not its position in the output | mined | 2026-10-26 | 180d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
+| S273 | GNU Bash Reference Manual, The Set Builtin (author copy of the manual, Edition 5.3, last updated 18 May 2025) — https://tiswww.case.edu/php/chet/bash/bashref.html (the gnu.org node page https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html was unreachable on 2026-10-27 UTC: eight attempts, HTTP 000, 0 bytes, connect timeouts — https and http, with and without www, IPv4-forced, and the single-page manual alike) | docs | A | Bash `errexit` (`-e`) and `pipefail`: which failing commands end a non-interactive shell, the listed non-exits, and a pipeline's return value | §The Set Builtin `-e` item (single-page copy lines 6547-6570) and `pipefail` item (lines 6706-6710); same text in the Savannah texi pinned by S097 at `@item -e` lines 5929-5948 and `@item pipefail` lines 6062-6066 (re-fetched 2026-10-27, sha256 f3d37d57, byte-identical to S097); a command of assignments only takes its status at §Simple Commands lines 3675-3677 (copy lines 4172-4173) @ author copy fetched 2026-10-27T00:22Z UTC, two fetches byte-identical (1040870 bytes; SHA-256 b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4), snapshot .ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html | Quotes (each at most 25 words), `-e`: "Exit immediately if a pipeline ... returns a non-zero status"; non-exits: "The shell does not exit if the command that fails is ... any command in a pipeline but the last"; the parenthetical tying that to pipefail: "any command in a pipeline but the last (subject to the state of the pipefail shell option)"; `pipefail`: "the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status"; assignments-only status: "the exit status of the last command substitution performed" | mined | 2026-10-26 | 365d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
 
 ## Paths
@@ -497,2 +499,4 @@ Round 46: three rows added, S258 (arXiv 2504.16777, Systemic Flakiness), S259 (t
 - Round 50: one row added by document from the shokuknow `corpus-expansion-1` package (theme F6), S271 (Zeller & Hildebrandt, IEEE TSE 2002, DOI 10.1109/32.988498; staged S167, which collides with nothing and is not reused), re-opened 2026-10-26 from the course mirror (HTTP 200, sha256 7ed0c812) with the snapshot under `.ufo/waves/round-50/w1/T50ScribeRows.src/`; the Zeller lead in the leads list above now has this row, and the earlier stop note (author PDFs timed out, ResearchGate 403, DOI metadata only) is superseded by the mirror fetch. S022 used-by — → the F6 pilot entry (its status stays queued: promoting it would move the frozen round-45 freshness population, a no-harm monitor); S024 used-by gains the two round-50 F6 entries (logged old → new in `corpus/lessons/round-50.md` `## Gate`). Id collision check: `reg-ids` 130, `staged-ids` 103, collisions 8 (S153-S160) (`.ufo/waves/round-50/w1/T50ExecIdGuard/`).
 - Next unused id: S272 (staged ids S161-S255 stay reserved by document for the package).
+Round 51: two tier-A rows added on the core tenth-leg case, S272 (kagi `corpus/drift-pins.sh`, code, pinned rev `e64e81b8`) and S273 (GNU Bash Reference Manual, §The Set Builtin, author copy, docs; gnu.org page was unreachable and the opened carrier is named in the row), both mined and opened this round; snapshots / fetch receipts under `.ufo/waves/round-51/w1/T51ScribeRowGate*` and `T51ScribeRowBash/`. Used by `corpus/knowledge/mutation-case-kagi-drift-pins.md`. S022 status `queued` → `mined` (used-by already cited `corpus/knowledge/fixture-shrinking-pilot.md`; reason: CORPUS.md defines mined as cited by ≥1 used-by path); logged in `corpus/lessons/round-51.md`. Registry rows 131 → 133.
+- Next unused id: S274 (staged ids S161-S255 stay reserved by document for the package).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- SKILL.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/SKILL.md b/SKILL.md
index 5f985e2f..e97f350c 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -2135,2 +2135,37 @@ the kill came from an absolute assert on the masked region.
 |---|---|---|---|
 | `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+
+#### Gate/probe registry — round 51
+
+| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
+|---|---|---|---|---|---|---|---|
+| bash declared-witness study | probe | `python3 tools/bash-witness-study.py check` (add --evidence DIR to grade another copy of the frozen evidence) | 0 clean; 1 failed (tamper, digest drift, summary/raw mismatch, unresolved sweep); 2 could-not-evaluate (missing input, pin mismatch, runner SETUP); 64 could-not-evaluate (usage) | `python3 tools/bash-witness-study.py selftest` → VERDICT: is the last line, preceded by WITNESS_SELFTEST: 51/51 pass | `.ufo/evidence/round-12/BashWitness/declaration.json` (frozen target, spec and runner sha256), `.ufo/evidence/round-12/BashWitness/declared.tsv` (declared-witness rows, sha pinned in declaration.json), `.ufo/evidence/round-12/BashWitness/summary.json`, `.ufo/evidence/round-12/BashWitness/manifest.json`, `tools/mutate-and-run.sh` (pinned runner digest, the spec is extracted from its heredoc); the DECLARED_WITNESSES rows are literals in the tool | caller-chosen --evidence DIR for declare, run and rerun plus the extended manifest; check and count read-only; selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored); sibling kagi object store read-only | tameshi |
+| command binding receipts | gate | `python3 tools/command-binding.py --bundle BUNDLE.json --expected EXPECTED.json --json` | 0 clean; 1 failed binding or outcome; 2 could-not-evaluate (invalid shape or integrity); 64 could-not-evaluate (usage) | `python3 tools/command-binding.py --selftest` → finding id COMMAND_BINDING_SELFTEST: in the last stdout line | `.ufo/evidence/round-23/extra-cases.json`, `.ufo/evidence/round-24/extra-cases.json`; literal expected exits and finding IDs in the tool selftest | read-only over the lane; selftest writes one isolated bundle/expected pair under TMPDIR | tameshi |
+| context receipt replay | gate | `python3 tools/context-capture.py --check` (frozen pin) or the same invocation with --receipt FILE --expected FILE | 0 clean; 1 failed; 2 could-not-evaluate; 64 could-not-evaluate (usage) | `python3 tools/context-capture.py --selftest` → SELFTEST: PASS (49/49 cases) | `.ufo/evidence/round-14/context-receipt.json`; literal digest 05cb55b8… and id/exit pin inside the tool | none during --check; selftest fixtures under /tmp/context-capture-selftest-*, removed in finally | tameshi |
+| environment-profile differential | gate | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out DIR/receipt.json --jobs 3` | 0 clean; 1 failed; 2 and 64 could-not-evaluate | `python3 tools/env-diff.py --selftest` → exit 0, last line ENVDIFF_SELFTEST: 9/9 pass | `.ufo/evidence/round-21/c2-contract.json`, `.ufo/evidence/round-21/f5/receipt.json`; literal expected classifications in the tool selftest | caller-chosen `--out` FILE plus sandboxes under `/tmp/tameshi-r21-envdiff.*` and TMPDIR-respecting selftest trees; lane trees read-only | tameshi |
+| evidence disposition accounting | gate | `python3 tools/evidence-disposition.py --root LANE --dispositions FILE` (lane run: --root . --dispositions .ufo/evidence/round-18/dispositions.json) | 0 clean; 1 failed semantic expectation; 2 could-not-evaluate (missing, unreadable, malformed, tampered or path-invalid input, invalid schema, internal failure); 64 could-not-evaluate (usage) | `python3 tools/evidence-disposition.py --selftest` → finding id SELFTEST: exit 0, 66/66 cases in about 3 s at rev 84aa673a; needs jj on PATH | `.ufo/evidence/round-13/expected.json`, `.ufo/evidence/round-13/verification.json`, `.ufo/evidence/round-13/producer-oracle-repair.json`, `.ufo/evidence/round-18/dispositions.json`; expected ids and exits are literals in the tool selftest | none in the lane — read-only over --root; selftest fixtures under /tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure | tameshi |
+| golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
+| mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root (pbt-staged-id-); selftest scratch under TMPDIR | tameshi |
+| pin disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root FLEET` | 0 clean; 1 failed (selftest FAIL only); 2 could-not-evaluate (usage, invalid or mismatched manifest, fleet root not a directory) | `python3 tools/pin-disposition.py --selftest` → SELFTEST: PASS n/n finding id SELFTEST: | `.ufo/evidence/round-13/pin-manifest.json` | read-only over the named fleet root; selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures, removed on PASS | tameshi |
+| round-20 receipt-window measure | gate | `python3 tools/receipt-measure.py --repo REPO --rev REV --json` | 0 clean, six items PASS at REV; 1 failed, including an absent REPO or unresolvable REV which is graded as six FAIL items rather than could-not-evaluate; 2 could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other arguments | `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST: 10/10 pass | `.ufo/evidence/round-20/contract.json`, `.ufo/evidence/round-20/stage/measure.py`, `.ufo/evidence/round-20/stage/receipt-window.py`, `tools/receipt-window.py`, `.ufo/evidence/round-20/final/receipts.json`, `.ufo/evidence/round-20/final/historical-receipts.json`, `.ufo/evidence/round-20/final/receipt-window-selftest.json`, `.ufo/waves/round-20/dispatch.json` | reads REPO at REV; no repo writes; scratch fixture trees under TMPDIR only, prefixes `receipt-measure-selftest.*` and `tameshi-r20-measure.*` | tameshi |
+| receipt-window validity | gate | `python3 tools/receipt-window.py --contract CONTRACT_JSON --receipts RECEIPTS_JSON` (add --json for one machine-readable verdict object) | 0 clean; 1 failed (findings); 2 could-not-evaluate (contract or receipts invalid, also argparse usage); 64 usage (missing --contract or --receipts) | `python3 tools/receipt-window.py --selftest` → RECEIPT_WINDOW_SELFTEST: last non-empty stdout line reads RECEIPT_WINDOW_SELFTEST: 20/20 pass with exit 0 | `.ufo/evidence/round-20/contract.json` expectations and instrument shas; `.ufo/evidence/round-20/public-cli-cases.json` synthetic cases; `.ufo/evidence/round-20/final/receipts.json`; `.ufo/evidence/round-20/final/receipt-window-selftest.json` recorded 20/20 exit 0 | reads caller-chosen CONTRACT_JSON and RECEIPTS_JSON without writing; selftest writes only its TMPDIR temp tree | tameshi |
+| entry-registry walk | gate | `python3 tools/registry-check.py --rev HEAD` (add `--only NAME` to grade one row) | 0 clean; 1 failed; 2 could-not-evaluate (registry unreadable or invalid, root/rev/clone failure, only or tag miss); 64 usage | `python3 tools/registry-check.py --selftest` → finding id SELFTEST: last line SELFTEST: PASS (51 cases) at 84aa673 | `tools/registry.json`, `tools/registry-check.py` | selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored), removed afterwards; live --root mode runs registry rows inside LANE so rows may write there | tameshi |
+| frozen registry replay | gate | `python3 tools/registry-replay.py --run --repo . --rev REV --requirements .ufo/evidence/round-23/requirements.json --registry-baseline .ufo/evidence/round-23/registry-baseline.json --out DIR` | 0 clean; 1 failed (refused rows: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT; an uncaught traceback also exits 1); 2 could-not-evaluate (registry digest mismatch, frozen requirements drift, clone HEAD mismatch, INVALID_OBSERVATIONS); 64 could-not-evaluate (usage) | `python3 tools/registry-replay.py --selftest` → REGISTRY_REPLAY_SELFTEST: 10/10 pass | `.ufo/evidence/round-23/requirements.json`, `.ufo/evidence/round-23/registry-baseline.json`, `tools/registry-check.py` (runner digest taken from the clone copy that runs) | caller-selected `--out` DIR (observations.json, bundle.json, expected.json, live-dependent.json) plus a private clone under TMPDIR; row commands run inside that clone, whose fleet mirror symlinks the live siblings, so the run is not write-isolated from them; selftest under TMPDIR | tameshi |
+| repeated control agreement | gate | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`, or --snapshot DIR over a committed control snapshot | 0 clean (controls_match); 1 failed (controls_mismatch); 2 could-not-evaluate (baseline_nonzero, command_unavailable, snapshot_tampered, setup_error); 64 could-not-evaluate (invalid_usage) | `python3 tools/repeat-control.py --selftest` → SELFTEST: PASS (29 cases) at exit 0 | `.ufo/evidence/round-12/ControlGate/expected.json`, `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` | caller-chosen --out DIR, created fresh and never deleted; --snapshot DIR read-only; selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass) | tameshi |
+| round21 measure facade | gate | `python3 tools/round21-measure.py --claim c1 --repo DIR --rev REV --json` | 0 clean; 1 failed; 2 could-not-evaluate (setup or unknown rev); 64 could-not-evaluate (usage) | `python3 tools/round21-measure.py --selftest` → ROUND21_MEASURE_SELFTEST: 13/13 pass | `.ufo/evidence/round-21/c1-survivors.py`, `.ufo/evidence/round-21/c2-count.py`, `.ufo/evidence/round-21/c2-contract.json` | TMPDIR only (selftest fixtures and delegated counter receipts); target repo read-only | tameshi |
+| shrink-case | probe | `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json` | 0 shrunk (report written); 1 selftest checks failed; 2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill) | `python3 tools/shrink-case.py --selftest` → SHRINK_SELFTEST: cases=21 failed=0 | `tools/pbt-staged-id.py` generator imported beside the tool; `tools/staged-id-guard.py` and `.ufo/evidence/round-49/c2/panel.json` for the M02 leg; expected edit literals in the tool source | caller-chosen --out FILE; tempfile.mkdtemp roots under TMPDIR for guard runs and selftest; lane read-only | tameshi |
+| staged-id adoption guard | gate | `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged STAGED.md --json` (add `--map MAP.json` to validate a candidate adoption map) | 0 clean (answered, or admitted with `--map`); 1 failed (analysis refused, or map inadmissible); 2 could-not-evaluate (usage, missing flag, or setup refusal) | `python3 -I tools/staged-id-guard.py --selftest` → VERDICT: PASS at exit 0, FAIL at exit 1 (counter line STAGED_ID_GUARD_SELFTEST: cases=N failed=M) | none — expected values are the fixture literals SELFTEST_REGISTRY and SELFTEST_STAGED_* committed inside tools/staged-id-guard.py; no expected file on disk | read-only: no writes, no temp files, no lane writes; caller names the registry, staged and map paths and stdout/stderr is the whole output | tameshi |
+| tally audit v2 (mutation runner tally) | gate | `python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh` (add `--then-regression --workdir DIR` to also require the runner's REGRESSION line to name cases=legs) | 0 clean; 1 failed (audit FAIL or a selftest case failure); 2 could-not-evaluate (cannot audit, setup, usage); a timed-out then-regression reports 124 and folds to 2 | `python3 tools/tally-audit-v2.py --selftest` → TALLY_AUDIT_V2_SELFTEST: 22/22 pass, one seeded-fault case per check | none — expected tallies are literals of the tool's independent oracle and its 22 selftest seeds; audited surface defaults to `tools/mutate-and-run.sh` | lane read-only; scratch under TMPDIR (tally-audit-v2.*, removed in finally); the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires; --then-regression writes only the runner's caller-named --workdir | tameshi |
+| tally audit v3 | gate | `python3 tools/tally-audit-v3.py --runner tools/mutate-and-run.sh` | 0 clean; 1 failed; 2 could-not-evaluate (SETUP: runner unparsable, tally harness structure missing, or argparse usage) | `python3 tools/tally-audit-v3.py --selftest` → TALLY_AUDIT_V3_SELFTEST: 35/35 pass | `tools/mutate-and-run.sh` is the only input read; expected REF_BLOCK, REF_NAMES and the 35 seeded-case panel are literals in the tool, and `.ufo/evidence/round-32/heldout/` is the committed provenance of those seeds (not read at run time) | audit and selftest scratch under TMPDIR, plus one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX allocated to witness the runner shape and removed at exit; the audited runner is never edited; `--then-regression` lets the runner create its own auto root or caller-chosen --workdir DIR | tameshi |
+| tally audit undercount guard | gate | `python3 tools/tally-audit.py` audits the runner `tools/mutate-and-run.sh` beside it; `--runner PATH`, `--then-regression --workdir DIR` accepted | 0 clean; 1 failed; 2 could-not-evaluate (cannot audit, usage, or regression SETUP); 64 could-not-evaluate (runner usage error surfaced through --then-regression) | `python3 tools/tally-audit.py --selftest` → TALLY_AUDIT_SELFTEST: 11/11 pass | `tools/tally-audit.py` REF_BLOCK reference tally block and leg-name panel are literals in the tool; audited `tools/mutate-and-run.sh` read-only | TMPDIR scratch dirs with prefix tally-audit, removed on exit; --then-regression hands its workdir to the runner | tameshi |
+| traced input surface | probe | `python3 tools/trace-inputs.py --root LANE --out RECEIPT.json -- COMMAND ARG...` | 0 clean; 1 failed (selftest check); 2 could-not-evaluate (setup: root or cwd not a directory, strace missing, no successful root execve); 64 could-not-evaluate (usage) | `python3 tools/trace-inputs.py --selftest` → SELFTEST: n/n on exit 0 | none — expected values are literals in the selftest | caller-chosen --out FILE (parent directories created); private trace-inputs-run-* tempdir outside --root, deleted on exit; selftest tree under TMPDIR | tameshi |
+| wave accounting | gate | `python3 tools/wave-accounting.py --bundle BUNDLE.json --expected EXPECTED.json` | 0 clean; 1 failed invariant; 2 could-not-evaluate (invalid, unavailable or tampered input); 64 could-not-evaluate (usage) | `python3 tools/wave-accounting.py --selftest` → FINDING: SELFTEST_PASS, 8/8 frozen plus 16/16 supplemental cases | `.ufo/evidence/round-22/measure.py`, `.ufo/evidence/round-22/accounting-extra-cases.json` | stdout only; caller-chosen `--bundle`/`--expected` read-only, selftest fixtures under isolated TMPDIR | tameshi |
+| wave parent settlement | gate | `python3 tools/wave-parent-settle.py --receipt RECEIPT.json` | 0 clean (SETTLED); 1 failed (UNSETTLED); 2 could-not-evaluate (usage, or --receipt not supplied) | `python3 tools/wave-parent-settle.py --selftest` → WAVE_PARENT_SELFTEST: 3/3 pass, exit 0 | `.ufo/waves/round-40/settlement-receipt.json` records SETTLED exit 0; `.ufo/waves/round-41/settlement-receipt.json` records UNSETTLED exit 1; red and green receipt literals live in the tool selftest | caller-chosen receipt is read only; verdict on stdout; nothing written, no TMPDIR use | tameshi |
+| wave-route-mix | gate | `python3 tools/wave-route-mix.py --spec SPEC.json --config CONFIG.yml --max-share 0.40` | 0 clean (no provider above the bound, every role routed, at least one seat); 1 failed (a provider above --max-share, an unrouted role, or an empty seat list); 2 could-not-evaluate (unreadable spec or config); 64 could-not-evaluate (usage: unknown flag, missing --spec, --max-share outside (0,1]) | `python3 tools/wave-route-mix.py --selftest` → ROUTEMIX_SELFTEST: 8/8 pass | none — the expected case verdicts are literals in the selftest; no repo file is read | nothing — read-only: JSON on stdout under --json plus one ROUTEMIX summary line on stderr; selftest writes no files | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 6d8c11e378aa90b12650808e1b79270742935f15 -- corpus/README.md` (exit 0), output:
```
commit 6d8c11e378aa90b12650808e1b79270742935f15
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Mon Oct 26 21:56:21 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Mon Oct 26 22:32:17 2026 -0300

    round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls

diff --git a/corpus/README.md b/corpus/README.md
index a1857733..c10d1bd5 100644
--- a/corpus/README.md
+++ b/corpus/README.md
@@ -607,2 +607,28 @@ F10 (PBT generators for gate fixtures): open → **held (round 49)** for its sta
 
 F6 (fixture minimization for survivors): open → **held (round 50)** for the method on killing cases — one shrinker that reduces a gate's killing case to a 1-minimal sub-case and states its run cost — conditioned on the round-50 deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; the round-29 B5 survivor is not discharged (it stays masked, `knowledge/survivor-fixture-minimization.md:53,57`), and if that receipt prints anything else this line is void as of round 50
+
+## Round 51 — frontier status table re-stated (calibration)
+
+The status table at `corpus/README.md:76-87` is superseded as a whole: its status cells were never re-stated after the rounds that moved them (rounds 1, 21, 25, 27, 38, 49, 50), so seven of the ten cells no longer read what the lane later declared. Nothing above this line is rewritten — the coverage map is corrected by appending only — and each row below carries the latest wording with a pointer to the lines that declare its status.
+
+| id | ground | candidate sources | status | next falsifiable move (before → after) |
+|---|---|---|---|---|
+| F1 | external mutation-score semantics + report interop | S001, S002, S086, S087 | held (round 25) — README.md:385-390; F1b open | before: emit one ledger leg as schema JSON and validate it (validator unavailable in round 1) → after: held for the eight recorded ledger legs (round 25, README.md:386-390); remaining: the emitted report names a target by basename with no lane or revision pin (round 26, README.md:412-413) and the 35 recorded survivors stay unclassified for NoCoverage (README.md:396) |
+| F2 | witness-scoped kill verdicts / bash mutation tooling | S006, S257 | partly held (round 1) — README.md:115 | before: the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8 → after: still unmeasured; the existing bash leg's declared-witness study is retained separately (README.md:128) and round 45 adds GoogleTest's primer as an upstream instance of the split (README.md:563) |
+| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040, S256, S258-S264 | open — README.md:589 | before: one control per sweep → after: N ≥ 3 byte-identical controls, or a named mismatch: still unmeasured; the rounds 45-47 entries add upstream statements and published measurements only (README.md:558-589) |
+| F4 | golden / snapshot fixture discipline | S013, S014, S015, S016, S017, S045, S105-S108, S132, S152, S153, S154 | partly held (round 38) — README.md:492-495 | before: update paths that write expected values without an explicit flag: unmeasured → after: the write-path census counted 99 live write sites with 0 unflagged (round 39, README.md:503), and rounds 40-41 added two successor tools; remaining: the cmp and git diff --exit-code lattices, and the shutil.* and handle.write classes outside v2's pattern (README.md:511, README.md:521-523) |
+| F5 | hermetic environment normalization | S015, S016, S028, S079 | Core (round 21) — README.md:330-335; for the nine frozen files | before: runner selftest host vs env -i LANG=C TZ=UTC identical (H3, round 1) → after: the nine frozen files measured the same way (nine clean controls, round 21); the three kumitate gates cite-check, surface-probe and proxy-check stay unmeasured (README.md:335-336) |
+| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608 | before: B5 probe fixture size: unmeasured → after: held for the method on killing cases — one shrinker to a 1-minimal sub-case with a stated run cost (round 50); the round-29 B5 survivor is not discharged and stays masked → next: shrink on a second gate, or discharge B5 |
+| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041, S047 | open — README.md:255-256 | before: pin-level cadence only → after: per-leg reuse decisions classified: not reached; round 13 acquired only the content-disposition prerequisite and round 17 moved no row (README.md:255-256) |
+| F8 | oracle anchoring as a survivor class | S012, S090, S091 | partly held (round 27) — README.md:424-427 | before: 0 test-oracle lines → after: one survivor classified against an independently anchored expectation, one gate at one pin (round 27); bounded to 3 of 4 survivors anchored in the gate's header contract and 1 by convention only (round 29, README.md:433-437) → next: anchor the hole calls on the other eight recorded legs |
+| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open — README.md:86 | before: no LLM-specific search run yet (U) → after: bounded pilot with an independent outcome check: untouched; round 43 states F9 is not touched (README.md:555-556) |
+| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599 | before: no PBT fixture method → after: one generator against a named fixture gate, conditioned on the round-49 deciding receipt printing C2_R49_PASS=true; next: a second gate, or shrinking (README.md:599) |
+
+S022 (`queued` → `mined`): the row's used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`, which cites it (round 50), so the status column is corrected to CORPUS.md's own reading — mined = cited by at least one path in used-by.
+No other SOURCES row changes status here, and every used-by path of a mined row exists at this revision.
+
+## Round 51 — tenth recorded mutation case (depth)
+
+| Entry / ground | Admission and exact scope | Evidence |
+|---|---|---|
+| `knowledge/mutation-case-kagi-drift-pins.md` / Core (recorded legs) | source-headed entry citing mined S272 (the pinned kagi host-drift gate) and S273 (Bash `errexit`/`pipefail` semantics), new this round; tenth ledger leg `bash-drift-pins`, 2/10 killed on the 13-case selftest under the recorded `sandbox-$DEFECT_ID` suite; independent A/B probe shows K_GONE_ARM, K_AMBIG_GT and K_SHAPE_OPTIN are environment-masked and become killed under a neutral sandbox (5/10), so the reported 20% must not be read as gate kill strength; seven of ten predictions held, five other survivors have off-suite witnesses | `.ufo/evidence/round-51/c2/`; `.ufo/waves/round-51/w1/T51LabSandboxLeak.md`, `T51ScribeEntry/` |
```

### R50.4: weak
The cited SCORECARD Planned round 51 and lesson round 50 prove historical carry-forward, not whether its seven constituent defects and successor-counter work remain outstanding at the current tip. This is a bundle, and no current per-constituent reconciliation is supplied.

Proposed fix: Replace historical-only support with a current per-constituent disposition, retaining open for any named residual; do not count it as an independently resolved defect.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SCORECARD.md` (exit 0); output lines 2433-2433:
```
**Planned (round 51):** the seven routed items the round-50 ledger leaves open — R45.1 (exempt pinned external hashes in the round-44 record counter and make it round-parametric), R45.4 (the five remaining anchor-refresh candidates), R46.2 (adopt the round-47 hardened counters as the operative ones), R47.5 and R48.4 (dead `brace_depth_at` helpers, round-47 counter survivor cases, the S205 / F7 package candidates, a declared class for `six-leg regression ledger`, the located-name check), R49.3 (SKILL.md:1503/1509/1555 outside-section sentences, with a re-key), R49.5 (the same carried list); successor C1/C2 counters that close the forgery routes disclosed in round 50 (judge bytes out of the shrinker's reach, run log outside its directory, typed and bounded output reads; per-row disposition attested by a seat other than the ledger's author); the 19 citation forms the successor read counter finds unread at `bda60768`; a class field and recurrence clause for the ledger (considerthese 2026-10-26 proposal 3, recurrence half); wave-2 carry-overs: a per-row executable check in the ledger (the sibling element that closes the C1 forgery routes), the shrinker's lone-surrogate exit code and its selftest kill rate (5 of 15), QUALITY 100's three wording defects, the deciding script's working-tree children (`.ufo/waves/round-50/w1/T50RevDeciding.md` F1), generator reach (5-cell rows, duplicate map keys, the digit boundary).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SCORECARD.md` (exit 0); output lines 2433-2433:
```
**Planned (round 51):** the seven routed items the round-50 ledger leaves open — R45.1 (exempt pinned external hashes in the round-44 record counter and make it round-parametric), R45.4 (the five remaining anchor-refresh candidates), R46.2 (adopt the round-47 hardened counters as the operative ones), R47.5 and R48.4 (dead `brace_depth_at` helpers, round-47 counter survivor cases, the S205 / F7 package candidates, a declared class for `six-leg regression ledger`, the located-name check), R49.3 (SKILL.md:1503/1509/1555 outside-section sentences, with a re-key), R49.5 (the same carried list); successor C1/C2 counters that close the forgery routes disclosed in round 50 (judge bytes out of the shrinker's reach, run log outside its directory, typed and bounded output reads; per-row disposition attested by a seat other than the ledger's author); the 19 citation forms the successor read counter finds unread at `bda60768`; a class field and recurrence clause for the ledger (considerthese 2026-10-26 proposal 3, recurrence half); wave-2 carry-overs: a per-row executable check in the ledger (the sibling element that closes the C1 forgery routes), the shrinker's lone-surrogate exit code and its selftest kill rate (5 of 15), QUALITY 100's three wording defects, the deciding script's working-tree children (`.ufo/waves/round-50/w1/T50RevDeciding.md` F1), generator reach (5-cell rows, duplicate map keys, the digit boundary).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-50.md` (exit 0); output lines 121-121:
```
| 3 | instrument-design (found this round, not fixed): both round-50 frozen counters admit forgeries a mechanical check cannot see — a fabricated ledger passes C1, and a shrinker can rewrite C2's judge copies and its own run log | `T50CritC1Contract.md` F1-F2, `T50SentinelShrink.md` F1-F2, `T50CritC2Contract.md` F1-F2 | none | not fixed: the counters are frozen. Routed to round 51 as successor counters (judge from bytes the shrinker never saw, run log outside its reach, output read with a type and size check; per-row disposition attested by a seat other than the ledger's author). This round's defence is the wave-2 per-row and per-source review, named in the report |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-50-verifier-spotcheck.md` (exit 0), output:
```
4. Carried (lane-acknowledged): the seven open ledger items and the successor counters for the forgery routes disclosed in `## C1`/`## C2` (SCORECARD `Planned (round 51)`).
```

### R51.1: supported
bcba892 changes the actual mte-interop-check expectation 9/9 -> 10/10 and source to this exact routed item; tip still expects 10/10. round-52/no-harm.sh allows registry.json. A committed standalone receipt exists: ROW mte-interop-check expect=0 got=0 held; REGISTRY_CHECK: held=1/1 superseded=0; EXIT=0. Its committed probe report identifies bcba892 as CAND0.

Proposed fix: Add .ufo/waves/round-52/w2/T52W2ExecC1Probe/registry-check-only-mte.stdout and the probe report to the ledger evidence.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:tools/registry.json` (exit 0); output lines 1266-1266:
```
     "MTE_INTEROP: PASS legs_conforming=10/10"
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:tools/mte-interop.py` (exit 0); output lines 343-343:
```
    print('MTE_INTEROP: %s legs_conforming=%d/%d' % ('PASS' if conforming == len(legs) else 'FAIL',
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51-verifier-spotcheck.md` (exit 0), output:
```
1. **R51.1, registry gate made unsatisfiable.** Update the `mte-interop-check` row in `tools/registry.json` to the ten-leg panel and record the change in a scope monitor that allows it. Show `registry-check --only mte-interop-check` green at the fix revision with a committed receipt.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- tools/registry.json tools/mte-interop.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/tools/registry.json b/tools/registry.json
index 3e852fd1..aaf37cb3 100644
--- a/tools/registry.json
+++ b/tools/registry.json
@@ -1012,9 +1012,9 @@
       "kind": "gate",
       "argv": ["uv", "run", "--no-project", "--with", "jsonschema==4.25.1", "python3", "tools/mte-interop.py", "--check"],
-      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]},
+      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=10/10"]},
       "timeout_s": 900,
       "status": "active",
       "tags": ["new-r26"],
-      "source": "corpus/lessons/round-25-verifier-spotcheck.md@d4140796f4e48e8ec81b793facba73fbd03b4443:189-192"
+      "source": "corpus/lessons/round-51-verifier-spotcheck.md@ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:126"
     }
   ]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- SKILL.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/SKILL.md b/SKILL.md
index 009096a7..30c11ae3 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -172,5 +172,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
    assert `count(old) == 1` in the pristine copy, print the first
    matching line (the kimi driver; the kagi note records the assert and `all unique` only), and require the literal line `all unique` — both lanes'
-   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`) (mutation-case-kimi-census.md:22-25;
+   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25;
    mutation-case-kagi-census.md:44-47). Require `new != old` in future drivers:
    a no-op is a driver defect, not a survivor. The cited historical notes do
@@ -209,5 +209,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
      summary, count not enumerated). Not a kill. Re-run it; keep every record.
    - **Kill rate = killed / (killed + survived)** — inconclusive runs sit outside
-     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`). Round 2: 8/10 = 80 %,
+     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:579-583`). Round 2: 8/10 = 80 %,
      no inconclusive run, 11 runs in 7.0 s (mutation-case-kimi-census.md:29-31).
      Round 3: 8/10 = 80 %, 11 runs in 11.0 s (mutation-case-kagi-census.md:50-53).
@@ -935,5 +935,5 @@ are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight rows since its round-18
 - **One command replays every leg.** `bash tools/mutate-and-run.sh
   --regression [--workdir DIR] [--keep]` allocates a fresh default scratch
-  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
+  `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
   it is removed on PASS unless `--keep`, retained on FAIL/SETUP; caller workdirs
   are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
@@ -2134,5 +2134,5 @@ the kill came from an absolute assert on the masked region.
 | Name | Kind | Command | Exits / rule |
 |---|---|---|---|
-| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the ten ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (10/10). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
 
 #### Gate/probe registry — round 51
@@ -2147,5 +2147,5 @@ the kill came from an absolute assert on the masked region.
 | golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
 | mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
-| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-52/coldread/refresh.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 348ee62c..5b5c9b80 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -41488,4 +41488,608 @@
   "source_read_entries": 34,
   "read_rev": "8eaae28ec4a3aadcd0b2ef86f7cb0a27a2ffa378"
- }
+ },
+ "corrections": [
+  {
+   "heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence",
+   "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9",
+   "reader": "T51W2Read01",
+   "reader_file": ".ufo/evidence/round-51/coldread/reads/T51W2Read01.md",
+   "wrong_expectations": 3,
+   "findings": [
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:425`: CAND line 425 is `d = hits[0]`; the `APPLY FAIL \u2026 old-string-count=%d expected=1` print is at 433-435",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`"
+    },
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:569-574`: CAND lines 569-574 are the restore-drift check and `MUTATE_RESTORE: OK`, not the cited division/DEGRADED behavior",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`"
+    },
+    {
+     "quote": "Section says 'corrected in round 27, seat Read03'; the claimed report path does not exist in the CAND tree",
+     "class": "unsupported",
+     "skill_statement": "this shows endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)"
+    }
+   ],
+   "corrects": "ledger entry ## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence @ 02ec217c: wrong_expectations 0 was written from code (round-51 refresh.py:227)",
+   "source": ".ufo/waves/round-52/w1/T52W1Corr01.json",
+   "routed_by": "corpus/lessons/round-51-verifier-spotcheck.md routed defect 3"
+  },
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- corpus/knowledge/fleet-kill-rate-ledger.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/corpus/knowledge/fleet-kill-rate-ledger.md b/corpus/knowledge/fleet-kill-rate-ledger.md
index bd6aae4e..1ccf25fe 100644
--- a/corpus/knowledge/fleet-kill-rate-ledger.md
+++ b/corpus/knowledge/fleet-kill-rate-ledger.md
@@ -436,2 +436,6 @@ its ER8-2). Receipt: `REGRESSION: PASS (cases=8 passed=8 …)` at the landed
 runner (`.ufo/waves/round-18/w2/RerunC1.md`). Tameshi's own read-only case; it
 did not drain the service queue.
+
+## Round 52 — §3 drift-pins cell superseded (2026-10-27)
+
+- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`REGRESSION: PASS (cases=10 passed=10 …)`, `.ufo/evidence/round-51/after/c2.stdout:22`); entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`. That case 10 measurement supersedes the cell; §3's table stays as written. Three of the eight survivors are harness-masked by the gate's own unanchored verdict grep (`corpus/lessons/round-51.md`), so 2/10 is a floor on the gate's detecting power, not its ceiling. Routed by the round-51 spot-check, defect 7.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/waves/round-52/w2/T52W2ExecC1Probe/registry-check-only-mte.stdout` (exit 0), output:
```
ROW mte-interop-check expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
EXIT=0
```

### R51.2: weak
The substantive statements and pointer targets are correct at tip, but bcba892 only fixes part of the item; git show 7ff81a5b contains the regression-pointer repair. The requested fresh-reader re-key is not established by the four cited prose excerpts. The row itself acknowledges the second commit.

Proposed fix: Bind the completion to 7ff81a5b (or explicitly name the multi-commit repair) and cite actual fresh-reader/re-key receipts; keep the current 46/64 no-harm loss distinct from historical textual repair.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SKILL.md` (exit 0); output lines 2179-2179:
```
| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the ten ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (10/10). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SKILL.md` (exit 0); output lines 2192-2192:
```
| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show | tameshi |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SKILL.md` (exit 0); output lines 202-202:
```
   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25;
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:SKILL.md` (exit 0); output lines 970-970:
```
  PASS/FAIL/SETUP (`tools/mutate-and-run.sh:139-143,1519-1548`).
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51-verifier-spotcheck.md` (exit 0), output:
```
2. **Stale SKILL statements.** Correct SKILL.md `:2136` "nine ledger legs", the runner row's `/tmp` write scope (the runner honours TMPDIR), and the runner line pointers at `:174`, `:211` and `:937-950` (R51.2/R51.3). Then re-key with fresh readers.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- tools/registry.json tools/mte-interop.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/tools/registry.json b/tools/registry.json
index 3e852fd1..aaf37cb3 100644
--- a/tools/registry.json
+++ b/tools/registry.json
@@ -1012,9 +1012,9 @@
       "kind": "gate",
       "argv": ["uv", "run", "--no-project", "--with", "jsonschema==4.25.1", "python3", "tools/mte-interop.py", "--check"],
-      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]},
+      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=10/10"]},
       "timeout_s": 900,
       "status": "active",
       "tags": ["new-r26"],
-      "source": "corpus/lessons/round-25-verifier-spotcheck.md@d4140796f4e48e8ec81b793facba73fbd03b4443:189-192"
+      "source": "corpus/lessons/round-51-verifier-spotcheck.md@ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:126"
     }
   ]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- SKILL.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/SKILL.md b/SKILL.md
index 009096a7..30c11ae3 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -172,5 +172,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
    assert `count(old) == 1` in the pristine copy, print the first
    matching line (the kimi driver; the kagi note records the assert and `all unique` only), and require the literal line `all unique` — both lanes'
-   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`) (mutation-case-kimi-census.md:22-25;
+   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25;
    mutation-case-kagi-census.md:44-47). Require `new != old` in future drivers:
    a no-op is a driver defect, not a survivor. The cited historical notes do
@@ -209,5 +209,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
      summary, count not enumerated). Not a kill. Re-run it; keep every record.
    - **Kill rate = killed / (killed + survived)** — inconclusive runs sit outside
-     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`). Round 2: 8/10 = 80 %,
+     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:579-583`). Round 2: 8/10 = 80 %,
      no inconclusive run, 11 runs in 7.0 s (mutation-case-kimi-census.md:29-31).
      Round 3: 8/10 = 80 %, 11 runs in 11.0 s (mutation-case-kagi-census.md:50-53).
@@ -935,5 +935,5 @@ are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight rows since its round-18
 - **One command replays every leg.** `bash tools/mutate-and-run.sh
   --regression [--workdir DIR] [--keep]` allocates a fresh default scratch
-  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
+  `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
   it is removed on PASS unless `--keep`, retained on FAIL/SETUP; caller workdirs
   are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
@@ -2134,5 +2134,5 @@ the kill came from an absolute assert on the masked region.
 | Name | Kind | Command | Exits / rule |
 |---|---|---|---|
-| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the ten ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (10/10). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
 
 #### Gate/probe registry — round 51
@@ -2147,5 +2147,5 @@ the kill came from an absolute assert on the masked region.
 | golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
 | mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
-| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-52/coldread/refresh.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 348ee62c..5b5c9b80 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -41488,4 +41488,608 @@
   "source_read_entries": 34,
   "read_rev": "8eaae28ec4a3aadcd0b2ef86f7cb0a27a2ffa378"
- }
+ },
+ "corrections": [
+  {
+   "heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence",
+   "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9",
+   "reader": "T51W2Read01",
+   "reader_file": ".ufo/evidence/round-51/coldread/reads/T51W2Read01.md",
+   "wrong_expectations": 3,
+   "findings": [
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:425`: CAND line 425 is `d = hits[0]`; the `APPLY FAIL \u2026 old-string-count=%d expected=1` print is at 433-435",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`"
+    },
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:569-574`: CAND lines 569-574 are the restore-drift check and `MUTATE_RESTORE: OK`, not the cited division/DEGRADED behavior",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`"
+    },
+    {
+     "quote": "Section says 'corrected in round 27, seat Read03'; the claimed report path does not exist in the CAND tree",
+     "class": "unsupported",
+     "skill_statement": "this shows endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)"
+    }
+   ],
+   "corrects": "ledger entry ## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence @ 02ec217c: wrong_expectations 0 was written from code (round-51 refresh.py:227)",
+   "source": ".ufo/waves/round-52/w1/T52W1Corr01.json",
+   "routed_by": "corpus/lessons/round-51-verifier-spotcheck.md routed defect 3"
+  },
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- corpus/knowledge/fleet-kill-rate-ledger.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/corpus/knowledge/fleet-kill-rate-ledger.md b/corpus/knowledge/fleet-kill-rate-ledger.md
index bd6aae4e..1ccf25fe 100644
--- a/corpus/knowledge/fleet-kill-rate-ledger.md
+++ b/corpus/knowledge/fleet-kill-rate-ledger.md
@@ -436,2 +436,6 @@ its ER8-2). Receipt: `REGRESSION: PASS (cases=8 passed=8 …)` at the landed
 runner (`.ufo/waves/round-18/w2/RerunC1.md`). Tameshi's own read-only case; it
 did not drain the service queue.
+
+## Round 52 — §3 drift-pins cell superseded (2026-10-27)
+
+- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`REGRESSION: PASS (cases=10 passed=10 …)`, `.ufo/evidence/round-51/after/c2.stdout:22`); entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`. That case 10 measurement supersedes the cell; §3's table stays as written. Three of the eight survivors are harness-masked by the gate's own unanchored verdict grep (`corpus/lessons/round-51.md`), so 2/10 is a floor on the gate's detecting power, not its ceiling. Routed by the round-51 spot-check, defect 7.
```

### R51.3: supported
bcba892 appends the named corrections array to the round-21 ledger. It remains at tip, including T51W2Read20 wrong_expectations=7, so the specific fabricated zero is corrected. This is the exact append-only branch the routed item permits; separate R52.3 disputes over-count accuracy.

Proposed fix: No status change; do not describe every corrected count as independently re-derived.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-21/coldread/ledger.json` (exit 0); output lines 112211-112211:
```
   "corrects": "ledger entry ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence @ 02ec217c: wrong_expectations 0 was written from code (round-51 refresh.py:227)",
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-21/coldread/ledger.json` (exit 0); output lines 112193-112193:
```
   "wrong_expectations": 3,
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-52/coldread/refresh.py` (exit 0); output lines 216-216:
```
                     'blocking_gaps': 0, 'wrong_expectations': len(reader['findings']), 'minor_gaps': 0,
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51-verifier-spotcheck.md` (exit 0), output:
```
3. **Cold-read re-key overstates.** `coldread/refresh.py:224-227` writes `wrong_expectations: 0` for every re-keyed section, but T51W2Read20 recorded false statements. Append a named correction to the round-21 ledger, or supersede those entries with the recorded counts, so the calibration record does not claim zero wrong expectations where a reader found some.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- tools/registry.json tools/mte-interop.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/tools/registry.json b/tools/registry.json
index 3e852fd1..aaf37cb3 100644
--- a/tools/registry.json
+++ b/tools/registry.json
@@ -1012,9 +1012,9 @@
       "kind": "gate",
       "argv": ["uv", "run", "--no-project", "--with", "jsonschema==4.25.1", "python3", "tools/mte-interop.py", "--check"],
-      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]},
+      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=10/10"]},
       "timeout_s": 900,
       "status": "active",
       "tags": ["new-r26"],
-      "source": "corpus/lessons/round-25-verifier-spotcheck.md@d4140796f4e48e8ec81b793facba73fbd03b4443:189-192"
+      "source": "corpus/lessons/round-51-verifier-spotcheck.md@ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:126"
     }
   ]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- SKILL.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/SKILL.md b/SKILL.md
index 009096a7..30c11ae3 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -172,5 +172,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
    assert `count(old) == 1` in the pristine copy, print the first
    matching line (the kimi driver; the kagi note records the assert and `all unique` only), and require the literal line `all unique` — both lanes'
-   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`) (mutation-case-kimi-census.md:22-25;
+   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25;
    mutation-case-kagi-census.md:44-47). Require `new != old` in future drivers:
    a no-op is a driver defect, not a survivor. The cited historical notes do
@@ -209,5 +209,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
      summary, count not enumerated). Not a kill. Re-run it; keep every record.
    - **Kill rate = killed / (killed + survived)** — inconclusive runs sit outside
-     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`). Round 2: 8/10 = 80 %,
+     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:579-583`). Round 2: 8/10 = 80 %,
      no inconclusive run, 11 runs in 7.0 s (mutation-case-kimi-census.md:29-31).
      Round 3: 8/10 = 80 %, 11 runs in 11.0 s (mutation-case-kagi-census.md:50-53).
@@ -935,5 +935,5 @@ are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight rows since its round-18
 - **One command replays every leg.** `bash tools/mutate-and-run.sh
   --regression [--workdir DIR] [--keep]` allocates a fresh default scratch
-  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
+  `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
   it is removed on PASS unless `--keep`, retained on FAIL/SETUP; caller workdirs
   are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
@@ -2134,5 +2134,5 @@ the kill came from an absolute assert on the masked region.
 | Name | Kind | Command | Exits / rule |
 |---|---|---|---|
-| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the ten ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (10/10). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
 
 #### Gate/probe registry — round 51
@@ -2147,5 +2147,5 @@ the kill came from an absolute assert on the masked region.
 | golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
 | mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
-| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-52/coldread/refresh.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 348ee62c..5b5c9b80 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -41488,4 +41488,608 @@
   "source_read_entries": 34,
   "read_rev": "8eaae28ec4a3aadcd0b2ef86f7cb0a27a2ffa378"
- }
+ },
+ "corrections": [
+  {
+   "heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence",
+   "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9",
+   "reader": "T51W2Read01",
+   "reader_file": ".ufo/evidence/round-51/coldread/reads/T51W2Read01.md",
+   "wrong_expectations": 3,
+   "findings": [
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:425`: CAND line 425 is `d = hits[0]`; the `APPLY FAIL \u2026 old-string-count=%d expected=1` print is at 433-435",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`"
+    },
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:569-574`: CAND lines 569-574 are the restore-drift check and `MUTATE_RESTORE: OK`, not the cited division/DEGRADED behavior",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`"
+    },
+    {
+     "quote": "Section says 'corrected in round 27, seat Read03'; the claimed report path does not exist in the CAND tree",
+     "class": "unsupported",
+     "skill_statement": "this shows endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)"
+    }
+   ],
+   "corrects": "ledger entry ## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence @ 02ec217c: wrong_expectations 0 was written from code (round-51 refresh.py:227)",
+   "source": ".ufo/waves/round-52/w1/T52W1Corr01.json",
+   "routed_by": "corpus/lessons/round-51-verifier-spotcheck.md routed defect 3"
+  },
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- corpus/knowledge/fleet-kill-rate-ledger.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/corpus/knowledge/fleet-kill-rate-ledger.md b/corpus/knowledge/fleet-kill-rate-ledger.md
index bd6aae4e..1ccf25fe 100644
--- a/corpus/knowledge/fleet-kill-rate-ledger.md
+++ b/corpus/knowledge/fleet-kill-rate-ledger.md
@@ -436,2 +436,6 @@ its ER8-2). Receipt: `REGRESSION: PASS (cases=8 passed=8 …)` at the landed
 runner (`.ufo/waves/round-18/w2/RerunC1.md`). Tameshi's own read-only case; it
 did not drain the service queue.
+
+## Round 52 — §3 drift-pins cell superseded (2026-10-27)
+
+- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`REGRESSION: PASS (cases=10 passed=10 …)`, `.ufo/evidence/round-51/after/c2.stdout:22`); entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`. That case 10 measurement supersedes the cell; §3's table stays as written. Three of the eight survivors are harness-masked by the gate's own unanchored verdict grep (`corpus/lessons/round-51.md`), so 2/10 is a floor on the gate's detecting power, not its ceiling. Routed by the round-51 spot-check, defect 7.
```

### R51.5: supported
Open is supported: the promised route remains in the knowledge entry while the round-52 lesson says the routing draft was rejected. Search of fleet round-52..57 tameshi reports found no drift-pins route. Later lane history for both cited paths stops at round 52/51. This is a report obligation, not permission to edit kagi.

Proposed fix: Keep open until the owning report actually files the cross-domain evidence; do not accept the promise or seat draft as delivery.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/knowledge/mutation-case-kagi-drift-pins.md` (exit 0); output lines 222-222:
```
right. Findings on the gate travel to kagi in the round report.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/knowledge/mutation-case-kagi-drift-pins.md` (exit 0); output lines 201-201:
```
  travels to kagi as a report line (adjacency), never as an edit here: tameshi
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-52.md` (exit 0); output lines 15-15:
```
- **The kagi routing draft's `grep -qxF "$3"` fix** (`.ufo/waves/round-52/w1/T52W1ScribeKagiRoute.md`). Rejected after T52W2RevRouting: the combined output carries more than the verdict line; the report recommends comparing an extracted verdict field instead.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51-verifier-spotcheck.md` (exit 0), output:
```
5. **Cross-domain routing owed to kagi.** File the `drift-pins.sh --selftest` unanchored verdict-word grep (`:400`, `:403`, plus the path-printing DRIFT line `:158`) as cross-domain evidence for kagi in the next report, as the entry promises. Do not edit kagi.
```

### R51.7: supported
bcba892 appends precisely the requested supersession note and tip retains it. Its exact case-10 sweep summary and ten-case regression PASS are corroborated by committed round-51 sweep/sweep.txt and after/c2.stdout.

Proposed fix: No status change.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/knowledge/fleet-kill-rate-ledger.md` (exit 0); output lines 439-439:
```
## Round 52 — §3 drift-pins cell superseded (2026-10-27)
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/knowledge/fleet-kill-rate-ledger.md` (exit 0); output lines 441-441:
```
- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`REGRESSION: PASS (cases=10 passed=10 …)`, `.ufo/evidence/round-51/after/c2.stdout:22`); entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`. That case 10 measurement supersedes the cell; §3's table stays as written. Three of the eight survivors are harness-masked by the gate's own unanchored verdict grep (`corpus/lessons/round-51.md`), so 2/10 is a floor on the gate's detecting power, not its ceiling. Routed by the round-51 spot-check, defect 7.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51-verifier-spotcheck.md` (exit 0), output:
```
7. **Ledger cell.** `corpus/knowledge/fleet-kill-rate-ledger.md:119` still reads "unmeasured by sweep" for drift-pins. Append a supersession note pointing at case 10, following the round-8 precedent at `:280`.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- tools/registry.json tools/mte-interop.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/tools/registry.json b/tools/registry.json
index 3e852fd1..aaf37cb3 100644
--- a/tools/registry.json
+++ b/tools/registry.json
@@ -1012,9 +1012,9 @@
       "kind": "gate",
       "argv": ["uv", "run", "--no-project", "--with", "jsonschema==4.25.1", "python3", "tools/mte-interop.py", "--check"],
-      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]},
+      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=10/10"]},
       "timeout_s": 900,
       "status": "active",
       "tags": ["new-r26"],
-      "source": "corpus/lessons/round-25-verifier-spotcheck.md@d4140796f4e48e8ec81b793facba73fbd03b4443:189-192"
+      "source": "corpus/lessons/round-51-verifier-spotcheck.md@ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4:126"
     }
   ]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- SKILL.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/SKILL.md b/SKILL.md
index 009096a7..30c11ae3 100644
--- a/SKILL.md
+++ b/SKILL.md
@@ -172,5 +172,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
    assert `count(old) == 1` in the pristine copy, print the first
    matching line (the kimi driver; the kagi note records the assert and `all unique` only), and require the literal line `all unique` — both lanes'
-   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`) (mutation-case-kimi-census.md:22-25;
+   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25;
    mutation-case-kagi-census.md:44-47). Require `new != old` in future drivers:
    a no-op is a driver defect, not a survivor. The cited historical notes do
@@ -209,5 +209,5 @@ Scratch for a sweep: `/tmp/<lane>-r<round>-<n>-work/` (Standing rules).
      summary, count not enumerated). Not a kill. Re-run it; keep every record.
    - **Kill rate = killed / (killed + survived)** — inconclusive runs sit outside
-     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`). Round 2: 8/10 = 80 %,
+     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:579-583`). Round 2: 8/10 = 80 %,
      no inconclusive run, 11 runs in 7.0 s (mutation-case-kimi-census.md:29-31).
      Round 3: 8/10 = 80 %, 11 runs in 11.0 s (mutation-case-kagi-census.md:50-53).
@@ -935,5 +935,5 @@ are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight rows since its round-18
 - **One command replays every leg.** `bash tools/mutate-and-run.sh
   --regression [--workdir DIR] [--keep]` allocates a fresh default scratch
-  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
+  `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
   it is removed on PASS unless `--keep`, retained on FAIL/SETUP; caller workdirs
   are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
@@ -2134,5 +2134,5 @@ the kill came from an absolute assert on the masked region.
 | Name | Kind | Command | Exits / rule |
 |---|---|---|---|
-| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the nine ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
+| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the ten ledger legs) · 64 usage, could-not-evaluate. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (10/10). Reads the runner's committed tables; writes only its own scratch and `--emit DIR`. The check replays live sibling object stores, so it is not hermetic. Owner tameshi. |
 
 #### Gate/probe registry — round 51
@@ -2147,5 +2147,5 @@ the kill came from an absolute assert on the masked region.
 | golden verdict classes | gate | `python3 tools/golden-verdict.py --check-entry PATH` | 0 clean; 1 failed; 2 could-not-evaluate (usage) | `python3 tools/golden-verdict.py --selftest` → GOLDEN_VERDICT_SELFTEST: | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool | no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir | tameshi |
 | mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3.9.0.tgz` and `tools/vendor/mutation-testing-metrics-3.9.0.tgz` (npm dist.integrity sha512 literals in the tool) | caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only | tameshi |
-| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under /tmp) for run and --regression; selftest under /tmp; fleet leg repos read-only via git show | tameshi |
+| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show | tameshi |
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- .ufo/evidence/round-21/coldread/ledger.json .ufo/evidence/round-52/coldread/refresh.py` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/.ufo/evidence/round-21/coldread/ledger.json b/.ufo/evidence/round-21/coldread/ledger.json
index 348ee62c..5b5c9b80 100644
--- a/.ufo/evidence/round-21/coldread/ledger.json
+++ b/.ufo/evidence/round-21/coldread/ledger.json
@@ -41488,4 +41488,608 @@
   "source_read_entries": 34,
   "read_rev": "8eaae28ec4a3aadcd0b2ef86f7cb0a27a2ffa378"
- }
+ },
+ "corrections": [
+  {
+   "heading": "## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence",
+   "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9",
+   "reader": "T51W2Read01",
+   "reader_file": ".ufo/evidence/round-51/coldread/reads/T51W2Read01.md",
+   "wrong_expectations": 3,
+   "findings": [
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:425`: CAND line 425 is `d = hits[0]`; the `APPLY FAIL \u2026 old-string-count=%d expected=1` print is at 433-435",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`"
+    },
+    {
+     "quote": "raw pointer `tools/mutate-and-run.sh:569-574`: CAND lines 569-574 are the restore-drift check and `MUTATE_RESTORE: OK`, not the cited division/DEGRADED behavior",
+     "class": "stale-pointer",
+     "skill_statement": "the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`"
+    },
+    {
+     "quote": "Section says 'corrected in round 27, seat Read03'; the claimed report path does not exist in the CAND tree",
+     "class": "unsupported",
+     "skill_statement": "this shows endpoint identity, not the absence of a transient write (SKILL.md:377-378; corrected in round 27, seat Read03)"
+    }
+   ],
+   "corrects": "ledger entry ## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence @ 02ec217c: wrong_expectations 0 was written from code (round-51 refresh.py:227)",
+   "source": ".ufo/waves/round-52/w1/T52W1Corr01.json",
+   "routed_by": "corpus/lessons/round-51-verifier-spotcheck.md routed defect 3"
+  },
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 bcba8924894216268afc4171f06eb8c28e912b46 -- corpus/knowledge/fleet-kill-rate-ledger.md` (exit 0), output:
```
commit bcba8924894216268afc4171f06eb8c28e912b46
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 01:42:33 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 02:39:44 2026 -0300

    round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections, kill-rate supersession, 20 ledger correction records; SCORECARD pre-registration

diff --git a/corpus/knowledge/fleet-kill-rate-ledger.md b/corpus/knowledge/fleet-kill-rate-ledger.md
index bd6aae4e..1ccf25fe 100644
--- a/corpus/knowledge/fleet-kill-rate-ledger.md
+++ b/corpus/knowledge/fleet-kill-rate-ledger.md
@@ -436,2 +436,6 @@ its ER8-2). Receipt: `REGRESSION: PASS (cases=8 passed=8 …)` at the landed
 runner (`.ufo/waves/round-18/w2/RerunC1.md`). Tameshi's own read-only case; it
 did not drain the service queue.
+
+## Round 52 — §3 drift-pins cell superseded (2026-10-27)
+
+- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`REGRESSION: PASS (cases=10 passed=10 …)`, `.ufo/evidence/round-51/after/c2.stdout:22`); entry `corpus/knowledge/mutation-case-kagi-drift-pins.md`. That case 10 measurement supersedes the cell; §3's table stays as written. Three of the eight survivors are harness-masked by the gate's own unanchored verdict grep (`corpus/lessons/round-51.md`), so 2/10 is a floor on the gate's detecting power, not its ceiling. Routed by the round-51 spot-check, defect 7.
```

### R51.8: supported
Open still holds in the current round-57 canonical deciding script: lines 143-144 derive the receipt date from git log -1 and compare it to FREEZE. It does not bind control receipts through a FREEZE=<sha> header. The ledger cited the older round-56 script, but the latest script confirms the same defect.

Proposed fix: Add .ufo/evidence/round-57/deciding-run.sh:136-145 as current evidence; retain open.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-56/deciding-run.sh` (exit 0); output lines 99-100:
```
  c=$(git log -1 --format=%H "$REV" -- "$f")
  git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51.md` (exit 0); output lines 88-88:
```
| `receipt-recency-by-last-touch` — the deciding gate dates a receipt by the last commit that changed its bytes, so a byte-identical re-score after an amendment reads as "not after freeze" | `integrate/a3/deciding-invocation-1-refused.txt`; `git log --format=%h 7e548bee -- .ufo/evidence/round-51/control/controls.exit` → `f0129a55` only; `controls.stdout` at `6d8c11e3` names rev `9d023aed` | QUALITY 99 (deciding-run gate 0) covers missing receipts, not re-scored identical ones | Routed, not fixed: the round-52 deciding gate should bind each control receipt to a freeze-stamped header line (`FREEZE=<sha>` inside the receipt) rather than to git last-touch. Not yet shown able to fail. |
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-51-verifier-spotcheck.md` (exit 0), output:
```
8. **Freeze-stamped control receipts** (lane mistake `receipt-recency-by-last-touch`). Not yet shown able to fail.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-57/deciding-run.sh` (exit 0), output:
```
PYV
# controls: committed at REV, after the freeze, with their verdict line. The gate is NOT consulted here.
for f in controls-a.stdout controls-a.exit controls-a.stdout.sha256 controls-b.stdout controls-b.exit controls-b.stdout.sha256; do
  p="$E/control/$f"
  git -C "$CL" cat-file -e "$REV:$p" 2>/dev/null || refuse control-receipt-missing "$p"
  [ "$(git -C "$CL" cat-file -t "$REV:$p")" = blob ] || refuse control-receipt-not-a-blob "$p"
  [ "$(git -C "$CL" cat-file -s "$REV:$p")" -gt 0 ] || refuse control-receipt-empty "$p"
  c=$(git -C "$CL" log -1 --format=%H "$REV" -- "$p")
  git -C "$CL" merge-base --is-ancestor "$FREEZE" "$c" || refuse control-receipt-not-after-freeze "$p"
done
```

### R52.1: wrong
The claimed fixing commit 441c26b only introduces the round-54 deciding script, including its usage header; that is preparation, not completion of the re-key/deciding run. git show of 441c26b is a new-script diff; git ls-tree at that commit has no round-54/after receipts. The cited 64/64 receipt is introduced by 4fe57df5, not 441c26b. Thus the exact fixing-commit attribution is wrong, independently of whether historical debt was eventually discharged. Current 46/64 is not proof the historical re-key never occurred.

Proposed fix: Use the actual historical completion and receipt commit (4fe57df5 with the corresponding re-key provenance), or the permitted honest-stop disposition with its actual commit. Do not choose a basename-keyed setup commit to satisfy the keying check. Separately disclose current no-harm loss.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-54/deciding-run.sh` (exit 0); output lines 2-2:
```
# Round-54 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:.ufo/evidence/round-54/after/c1.stdout` (exit 0); output lines 5-5:
```
C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-52-verifier-spotcheck.md` (exit 0), output:
```
1. **R52.1 coldread re-key debt.** 19 sections lost credit at the tip; 18/19 reader JSONs committed (Read18 missing), no T52 ledger entries, no frozen deciding receipts. Re-run the frozen re-key/deciding pipeline per `.ufo/evidence/round-52/deciding-run.sh` and the contract kill rule, or record an honest stop again.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 441c26bec5e4c1cc31bc2a840f311cb8d1965259 -- .ufo/evidence/round-54/deciding-run.sh .ufo/evidence/round-54/after/c1.stdout` (exit 0), output:
```
commit 441c26bec5e4c1cc31bc2a840f311cb8d1965259
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Wed Oct 28 11:19:07 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Wed Oct 28 11:19:07 2026 -0300

    round-54: claim contract, both counters, no-harm monitors, controls harness and freeze manifest (pre-seat)

diff --git a/.ufo/evidence/round-54/deciding-run.sh b/.ufo/evidence/round-54/deciding-run.sh
new file mode 100755
index 00000000..36beb593
--- /dev/null
+++ b/.ufo/evidence/round-54/deciding-run.sh
@@ -0,0 +1,58 @@
+#!/bin/bash
+# Round-54 deciding run. Usage: deciding-run.sh LANE REV FREEZE OUTDIR
+#   LANE    absolute path of the lane repo        REV     the content revision
+#   FREEZE  the counter-freeze commit             OUTDIR  an existing, EMPTY directory inside LANE for receipts
+# Carried from rounds 49-53 (QUALITY 99): gate 0 refuses (exit 3, nothing run) unless every pre-registered control
+# receipt is committed at REV in a commit that descends from FREEZE; a second invocation is refused; each counter
+# gets a start receipt before it runs and an exit receipt after; the counters, no-harm and the precheck run from
+# the bytes committed at REV (git show into scratch), never from the working tree; the working tree must be clean
+# (witness files before and after). Work dirs live under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r54/deciding.
+set -u
+LANE=$1; REV=$2; FREEZE=$3; OUT=$4
+case "$LANE" in /*) ;; *) echo "LANE must be absolute"; exit 2;; esac
+BASE=d33053f7552db4bd290c99a36979760f544c41ad
+FLEET=/home/vgpnk/Projects/shokunin
+E=.ufo/evidence/round-54
+SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r54/deciding
+cd "$LANE" || exit 2
+REV=$(git rev-parse --verify "$REV^{commit}") || exit 2
+FREEZE=$(git rev-parse --verify "$FREEZE^{commit}") || exit 2
+[ -d "$OUT" ] || { echo "DECIDING_REFUSED outdir-missing"; exit 3; }
+[ "$(git rev-parse HEAD)" = "$REV" ] || { echo "DECIDING_REFUSED head-is-not-rev"; exit 3; }
+CONTROLS="$E/control/controls-a.stdout $E/control/controls-a.exit $E/control/controls-b.stdout $E/control/controls-b.exit"
+for f in $CONTROLS; do
+  git cat-file -e "$REV:$f" 2>/dev/null || { echo "DECIDING_REFUSED control-receipt-missing $f"; exit 3; }
+  c=$(git log -1 --format=%H "$REV" -- "$f")
+  git merge-base --is-ancestor "$FREEZE" "$c" || { echo "DECIDING_REFUSED control-receipt-not-after-freeze $f"; exit 3; }
+done
+for k in c1 c2; do [ -e "$OUT/$k.start" ] && { echo "DECIDING_REFUSED second-invocation $k"; exit 3; }; done
+git status --porcelain > "$OUT/clean-tree-before.txt"
+[ "$(grep -vc "^?? ${OUT#$LANE/}" "$OUT/clean-tree-before.txt")" = 0 ] || { echo "DECIDING_REFUSED dirty-tree"; cat "$OUT/clean-tree-before.txt"; exit 3; }
+rm -rf "$SCR"; mkdir -p "$SCR/code" "$SCR/c1" "$SCR/c2"; export TMPDIR="$SCR"
[Full output in receipts/sweep.json]
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 441c26bec5e4c1cc31bc2a840f311cb8d1965259 -- .ufo/evidence/round-54/after .ufo/evidence/round-21/coldread` (exit 0), output:
```
(no round-54/after paths; complete listing in sweep.json)
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format= --name-only 4fe57df5` (exit 0), output:
```
.ufo/evidence/round-54/after/c1.end
.ufo/evidence/round-54/after/c1.exit
.ufo/evidence/round-54/after/c1.start
.ufo/evidence/round-54/after/c1.stdout
.ufo/evidence/round-54/after/c2.end
.ufo/evidence/round-54/after/c2.exit
.ufo/evidence/round-54/after/c2.start
.ufo/evidence/round-54/after/c2.stdout
.ufo/evidence/round-54/after/census.exit
.ufo/evidence/round-54/after/census.stderr
.ufo/evidence/round-54/after/census.stdout
.ufo/evidence/round-54/after/clean-tree-after.txt
.ufo/evidence/round-54/after/clean-tree-before.txt
.ufo/evidence/round-54/after/coldread-precheck.exit
.ufo/evidence/round-54/after/coldread-precheck.stdout
.ufo/evidence/round-54/after/deciding-run.exit
.ufo/evidence/round-54/after/frozen.stdout
.ufo/evidence/round-54/after/no-harm.exit
.ufo/evidence/round-54/after/no-harm.stdout
```

### R52.2: supported
a41195df adds the missing round-52 LOG heading and entry with bcba8924 -> f1a32461 and honest-stop disposition. Full entry remains at tip; this is the exact requested append.

Proposed fix: No status change.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:LOG.md` (exit 0); output lines 2444-2444:
```
## 2026-10-27 — round 52 (honest stop, run wrap-up)
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:LOG.md` (exit 0); output lines 2448-2448:
```
honest-stop report is at `.ufo/reports/round-52/tameshi.md` (fleet commit
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-52-verifier-spotcheck.md` (exit 0), output:
```
2. **R52.2 LOG.md round-52 entry missing.** The round's landed changes are not tied to a LOG.md entry (report contract). Append (never rewrite) the round-52 entry naming the commits bcba892 → f1a3246 and the wrap-up disposition.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=fuller --unified=2 a41195dfc13a73958e4c5228ec196b28d03ded03 -- LOG.md` (exit 0), output:
```
commit a41195dfc13a73958e4c5228ec196b28d03ded03
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 10:24:16 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Tue Oct 27 10:24:16 2026 -0300

    round-53: C* content commit — fix pass, S275/S276 assimilation (re-opened this round), round-53 lesson, QUALITY 104, LOG r52+r53 entries, README F7 note

diff --git a/LOG.md b/LOG.md
index 3bab5edb..bd04b1be 100644
--- a/LOG.md
+++ b/LOG.md
@@ -2441,2 +2441,38 @@ Motivating evidence: the w2 reader rows existed, but no re-key had landed. The c
 
 Evidence: `.ufo/evidence/round-51/after/`, `.ufo/evidence/round-51/integrate/a3/`, `corpus/lessons/round-51.md`; SCORECARD § Round 51 deciding results.
+
+## 2026-10-27 — round 52 (honest stop, run wrap-up)
+
+L1 TameshiR52. Base `ef19d8e1`. Round 52 stopped at the operator's
+run-wrap-up directive before wave 3 settled and before a deciding run; the
+honest-stop report is at `.ufo/reports/round-52/tameshi.md` (fleet commit
+`53fdd555`). Landed, in `bcba8924` → `f1a32461` (tip): C1's registry-home
+repair intent — `tools/registry.json` `mte-interop-check` row expects
+`legs_conforming=10/10` and re-points at R51.1; `tools/round21-measure.py`
+reads its subject counter's fleet root; SKILL.md corrections; QUALITY
+criterion 103; S274; `corpus/lessons/round-52.md`. The round-52 closure
+(`c1d49d7`, committed by protocol-shokunin) re-measured both frozen counters
+at the tip — C1 `total=0 C1_R52_PASS=true`, C2 `total=0 C2_R52_PASS=true` —
+but rejected-harmed: the frozen cold-read floor read RED (64 → 45 credited,
+19 sections lost by the round's own edits; the re-key never landed) and
+routed R52.1–R52.6. The closure salvage commit `6db1d220` committed the
+untracked wave-3 leftovers (R52.4). C1/C2 verify on the frozen counters at
+the tip by the closure's own measurement; the calibration axis stood harmed
+until round 53's repair. No claim is admitted by the round-52 report itself;
+the closure's per-claim grades (operability improved; calibration harmed)
+are the round's verdicts.
+
+## 2026-10-27 — round 53, attempt 2 (this round)
+
+L1 TameshiR53a2. Attempt 1 died at its first model call on a provider quota
+limit; nothing to inherit. Base `6db1d220`; freeze `e62d9971` (amendments
+1–5, all disclosed in `freeze.json`). Claims: C1 calibration — the
+cold-read floor re-key over the 30 headings the round inherited or drifted
+(R52.1); C2 operability — `tools/` scratch hygiene (R52.5). Worked:
+21 T52W3 reader findings fixed L1-inline (`218bc6b5`); scratch-directive
[Full output in receipts/sweep.json]
```

### R52.3: supported
Open remains supported: tip lesson:27 still says 8 over-count and Corr12 0 of 14. Path history has no edits after 7ff81a5b; git log -S Corr12 identifies that original statement, not a later re-derivation/correction. The ledger does not claim the expensive re-derivation was performed.

Proposed fix: Retain open; do not treat the disputed example as proof that all eight reviewer judgments were correct.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-52.md` (exit 0); output lines 27-27:
```
- 8 over-count (01, 02, 06, 09-13). Example: Corr12, where the reviewer found 0 of 14 findings to be statements the reader marked as not holding.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2c51affd37e15cd7cd258d76ba0f5f73ff235924:corpus/lessons/round-52-verifier-spotcheck.md` (exit 0), output:
```
3. **R52.3 over-count review overstated (this closure's finding).** `T52W2RevCorr0912.md` claims "0 of 14" reader-marked failures for Corr12; independent re-derivation found ≥2–6 with selectively truncated citations. Re-derive the "8 over-count" verdict for records 01, 02, 06, 09–13 under one written counting rule (reader-marked drift at CAND; exclude `holds-hist` rows per the record's own §3) and correct the lesson row if warranted; consider a QUALITY criterion for reviewer-seat quote truncation.
```

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log "--format=%h %s" -S Corr12 2c51affd37e15cd7cd258d76ba0f5f73ff235924 -- corpus/lessons/round-52.md` (exit 0), output:
```
7ff81a5b round-52: wave-2 fix-reads applied in-line (59), round21 row cell, shrink-case scope; QUALITY 103; S274; lesson; wave-2 evidence
```

## Sweep and verification gaps

Executed 97 read-only git commands. Complete commands, exit codes and outputs: `T57W3RowAttack1-receipts/sweep.json`; per-commit diffs also attached. Each assigned spot-check was read from the pinned tip, each evidence path inspected there, every cited commit diff inspected and ancestry checked, and recent cited-path history read. No tests or counters were re-run; committed receipts are corroboration, not new runtime verification. No clone or git mutation was needed. No tools installed.

LSP device unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; fallback was literal inspection of git object bytes and path histories, not semantic reference proof. Fleet-report text search covered round-52 through round-57 reports and found no drift-pins routing. This absence is bounded to those reports.

Residual risk: R50.4 is a bundled obligation without a current sub-item reconciliation. R51.2 fresh-reader provenance is insufficient in the cited evidence. New no-harm loss (46/64, supplied by the assignment and reiterated in the round-57 report) is not confused with absence of a historical re-key. No conclusion about unseen future commits or uncommitted work.

Self-evaluation (1–5): accuracy 4 (static/committed evidence, no live runtime replay); completeness 4 (13/13 rows, bundled R50.4 cannot be reduced from its old excerpts); clarity 4 (long command appendix retained for auditability); actionability 4 (specific replacement evidence/commits, not executable patch); conciseness 4 (full byte outputs externalized). Overall 4.0. Priority improvement: bind R52.1 to the actual receipt/completion commit, then add R51.2 reader provenance. User agreement expected: no green claims for unrun checks.
