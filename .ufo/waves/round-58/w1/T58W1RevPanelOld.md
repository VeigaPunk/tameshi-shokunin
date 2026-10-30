# T58W1RevPanelOld — old-panel cross-check

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Old panel base: `5e3569969b532310d2b8a3d130901757a3df356b`.

Axes: calibration correctness; evidence completeness; zero lane mutation. Recommendation only, not claim admission.

## Finding (low severity)

**R53.6 is only partially closed.** The four primary unusable-TMPDIR error paths now exit 2 (live commands below), but `tools/context-capture.py:27` still says `tempfile.mkdtemp(dir=tempfile.gettempdir())`; its actual selftest allocation at 1642–1643 uses `dir=strict_scratch_root()`. The item text explicitly includes this docstring nit. I therefore disagree with whole-item `fixed`, while agreeing that the main runtime defect was repaired. No primary runtime regression found.

## Sweep and command evidence

A shared clone was created in `/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone`; `git -C <clone> rev-parse --show-toplevel` printed exactly that clone before detached checkout. Checkout printed `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`.

For each fix commit C below, executed `git -C <clone> merge-base --is-ancestor C HEAD` (all exit 0, stdout empty), `git -C <clone> show --format=fuller --stat C`, and `git -C <clone> show --format= --no-ext-diff C -- SKILL.md SCORECARD.md LOG.md corpus tools`. Exact commands, stdout and stderr are retained in `<seat>-receipts/<C>.json`. The old panel base is also an ancestor (exit 0).

`git -C <clone> diff --name-status <old-panel-base> HEAD -- SKILL.md SCORECARD.md LOG.md corpus tools .ufo/evidence/round-21/coldread/ledger.json` identified the changed resolution surfaces; full output is `old-new-diff.json`, and per-item surface diffs are retained separately. Source and registry standing cells were read at the detached new base, not inferred solely from ancestry.

The `lsp` device is unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. References/definition/diagnostics could not be requested. Literal searches are cited as literal evidence only.

## Per-item rechecks

### R50.1 — old fixed; new fixed; agree

S022 is mined with the pilot used-by; round-51 lesson logs queued→mined and the later source record retains it.

Old resolving commit (ancestor, exit 0): `6d8c11e378aa90b12650808e1b79270742935f15`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/SOURCES.md", pattern="^\\| S022 ")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/SOURCES.md#7A57]
 32:| S021 | Agentic Property-Based Testing (Maaz, DeVoe, Hatfield-Dodds, Carlini; arXiv 2510.09907) — https://arxiv.org/abs/2510.09907 | paper | A | agentic PBT bug validity on real packages | Abstract, arXiv:2510.09907v1 (submitted 2025-10-10) | an LLM agent infers properties from code and docs, writes Hypothesis tests and reflects before reporting: 56% of reports were valid bugs; ranking lifts the top-21 validity to 86% | queued | 2026-10-19 | 180d | — |
*33:| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugg...
 34:| S023 | Shrink Ray README (DRMacIver/shrinkray) — https://github.com/DRMacIver/shrinkray | code | A | shrinkray's interestingness-driven reduction | README §Usage and §LLM mode @ page currentOid 5fe6ee135d732e4b7758b3dbe3d91428523018fb, fetched 2026-10-19 | a reducer driven by any executable interestingness test (exit 0 = interesting); parallel multi-format passes; local LLM proposals are accepted only when the interestingness test still passes | queued | 2026-10-19 | 90d | — |
 35:| S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | mined | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md, corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta...
 36:| S025 | An Empirical Analysis of Flaky Tests (Luo, Hariri, Eloussi, Marinov; FSE 2014) — https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf | paper | A | flaky test root causes and fixes | §Findings F.2, FSE 2014 PDF p.2 (fetched 2026-10-19) | 201 flaky-fix commits: top causes are Async Wait, Concurrency and Test Order Dependency; 78% of flaky tests are flaky when first written; 74% of order-dependency fixes clean shared state | queued | 2026-10-19 | 730d | — |

[Some lines truncated to 512 bytes]
```

### R50.2 — old fixed; new fixed; agree

Both generator and shrink-case have complete registry rows (entry, exits including 2, selftest, pins, scope).

Old resolving commit (ancestor, exit 0): `6d8c11e378aa90b12650808e1b79270742935f15`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SKILL.md", pattern="\\| pbt staged-id generator \\||\\| shrink-case \\|")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SKILL.md#36D1]
 2192:| fleet mutation runner | gate | `bash tools/mutate-and-run.sh --regression --workdir DIR` or `bash tools/mutate-and-run.sh --target FILE --defects SPEC --suite CMD --workdir DIR` | 0 clean; 1 failed (run mode prints DEGRADED when a suite is inconclusive); 2 could-not-evaluate (setup/refusal); 64 could-not-evaluate (usage) | `bash tools/mutate-and-run.sh --selftest` → finding id VERDICT: (terminal line VERDICT: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo...
*2193:| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root... [col 1]
 2194:| pin disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root FLEET` | 0 clean; 1 failed (selftest FAIL only); 2 could-not-evaluate (usage, invalid or mismatched manifest, fleet root not a directory) | `python3 tools/pin-disposition.py --selftest` → SELFTEST: PASS n/n finding id SELFTEST: | `.ufo/evidence/round-13/pin-manifest.json` | read-only over the named fleet root; selftest writes isolated `$TMPDIR` fixtures (`tameshi-r13-pin-disposition-...
 2195:| round-20 receipt-window measure | gate | `python3 tools/receipt-measure.py --repo REPO --rev REV --json` | 0 clean, six items PASS at REV; 1 failed, including an absent REPO or unresolvable REV which is graded as six FAIL items rather than could-not-evaluate; 2 could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other arguments | `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST: 10/10 pass | `.ufo/evidence/round-20/contract.js...
 2196:| receipt-window validity | gate | `python3 tools/receipt-window.py --contract CONTRACT_JSON --receipts RECEIPTS_JSON` (add --json for one machine-readable verdict object) | 0 clean; 1 failed (findings); 2 could-not-evaluate (contract or receipts invalid, also argparse usage); 64 usage (missing --contract or --receipts) | `python3 tools/receipt-window.py --selftest` → RECEIPT_WINDOW_SELFTEST: last non-empty stdout line reads RECEIPT_WINDOW_SELFTEST: 20/20 pass with exit 0 | `.ufo/evidence/round-20/cont...
...
 2200:| round21 measure facade | gate | `python3 tools/round21-measure.py --claim c1 --repo DIR --rev REV --json` | 0 clean; 1 failed; 2 could-not-evaluate (setup or unknown rev); 64 could-not-evaluate (usage) | `python3 tools/round21-measure.py --selftest` → ROUND21_MEASURE_SELFTEST: 13/13 pass; fleet-bound, not hermetic (since round 52 it reads the sibling blobs at the fleet root that its subject counter c2-count.py names in its FLEET literal, so it passes from a clone anywhere on this host and fails where...
*2201:| shrink-case | probe | `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json` | 0 shrunk (report written); 1 selftest checks failed; 2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill) | `python3 tools/shrink-case.py --selftest` → SHRINK_SELFTEST: cases=21 failed=0 | `tools/pbt-staged-id.py` generator imported beside the tool; `tools/staged-id-guard.py` and `.ufo/evidence/round-49/c2/panel.json` for the M02 leg; expected e... [col 1]
 2202:| staged-id adoption guard | gate | `python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged STAGED.md --json` (add `--map MAP.json` to validate a candidate adoption map) | 0 clean (answered, or admitted with `--map`); 1 failed (analysis refused, or map inadmissible); 2 could-not-evaluate (usage, missing flag, or setup refusal) | `python3 -I tools/staged-id-guard.py --selftest` → VERDICT: PASS at exit 0, FAIL at exit 1 (counter line STAGED_ID_GUARD_SELFTEST: cases=N failed=M) | none ...
 2203:| tally audit v2 (mutation runner tally) | gate | `python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh` (add `--then-regression --workdir DIR` to also require the runner's REGRESSION line to name cases=legs) | 0 clean; 1 failed (audit FAIL or a selftest case failure); 2 could-not-evaluate (cannot audit, setup, usage); a timed-out then-regression reports 124 and folds to 2 | `python3 tools/tally-audit-v2.py --selftest` → TALLY_AUDIT_V2_SELFTEST: 22/22 pass, one seeded-fault case per check |...
 2204:| tally audit v3 | gate | `python3 tools/tally-audit-v3.py --runner tools/mutate-and-run.sh` | 0 clean; 1 failed; 2 could-not-evaluate (SETUP: runner unparsable, tally harness structure missing, or argparse usage) | `python3 tools/tally-audit-v3.py --selftest` → TALLY_AUDIT_V3_SELFTEST: 35/35 pass | `tools/mutate-and-run.sh` is the only input read; expected REF_BLOCK, REF_NAMES and the 35 seeded-case panel are literals in the tool, and `.ufo/evidence/round-32/heldout/` is the committed provenance of th...

[Some lines truncated to 512 bytes]
```

### R50.3 — old fixed; new fixed; agree

Superseding round-51 table carries F6 held round 50 and F10 held round 49.

Old resolving commit (ancestor, exit 0): `6d8c11e378aa90b12650808e1b79270742935f15`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/README.md", pattern="^\\| F(6|10) .*held \\(round")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/README.md#892D]
 620:| F5 | hermetic environment normalization | S015, S016, S028, S079 | Core (round 21) — README.md:330-335; for the nine frozen files | before: runner selftest host vs env -i LANG=C TZ=UTC identical (H3, round 1) → after: the nine frozen files measured the same way (nine clean controls, round 21); the three kumitate gates cite-check, surface-probe and proxy-check stay unmeasured (README.md:335-336) |
*621:| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608 | before: B5 probe fixture size: unmeasured → after: held for the method on killing cases — one shrinker to a 1-minimal sub-case with a stated run cost (round 50); the round-29 B5 survivor is not discharged and stays masked → next: shrink on a second gate, or discharge B5 |
 622:| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041, S047 | open — README.md:255-256 | before: pin-level cadence only → after: per-leg reuse decisions classified: not reached; round 13 acquired only the content-disposition prerequisite and round 17 moved no row (README.md:255-256) |
 623:| F8 | oracle anchoring as a survivor class | S012, S090, S091 | partly held (round 27) — README.md:424-427 | before: 0 test-oracle lines → after: one survivor classified against an independently anchored expectation, one gate at one pin (round 27); bounded to 3 of 4 survivors anchored in the gate's header contract and 1 by convention only (round 29, README.md:433-437) → next: anchor the hole calls on the other eight recorded legs |
 624:| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open — README.md:86 | before: no LLM-specific search run yet (U) → after: bounded pilot with an independent outcome check: untouched; round 43 states F9 is not touched (README.md:555-556) |
*625:| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599 | before: no PBT fixture method → after: one generator against a named fixture gate, conditioned on the round-49 deciding receipt printing C2_R49_PASS=true; next: a second gate, or shrinking (README.md:599) |
 626:
 627:S022 (`queued` → `mined`): the row's used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`, which cites it (round 50), so the status column is corrected to CORPUS.md's own reading — mined = cited by at least one path in used-by.
 628:No other SOURCES row changes status here, and every used-by path of a mined row exists at this revision.
```

### R51.1 — old fixed; new fixed; agree

Registry expects legs_conforming=10/10; committed one-row receipt records held=1/1 and EXIT=0.

Old resolving commit (ancestor, exit 0): `bcba8924894216268afc4171f06eb8c28e912b46`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/registry.json", pattern="mte-interop-check|legs_conforming=10/10")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/registry.json#BC0A]
 1250:  {
*1251:   "name": "mte-interop-check",
 1252:   "kind": "gate",
 1253:   "argv": [
 1254:    "uv",
...
 1265:    "stdout_contains": [
*1266:     "MTE_INTEROP: PASS legs_conforming=10/10"
 1267:    ]
 1268:   },
 1269:   "timeout_s": 900,
```

### R51.2 — old fixed; new fixed; agree

SKILL names ten ledger legs, TMPDIR runner scope and corrected runner pointers; later re-key is committed.

Old resolving commit (ancestor, exit 0): `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SKILL.md", pattern="ten ledger legs|caller-chosen --workdir.*TMPDIR|434|579-583")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SKILL.md#36D1]
 201:   matching line (the kimi driver; the kagi note records the assert and `all unique` only), and require the literal line `all unique` — both lanes'
*202:   drivers did exactly this (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:434`) (mutation-case-kimi-census.md:22-25;
 203:   mutation-case-kagi-census.md:44-47). Require `new != old` in future drivers:
 204:   a no-op is a driver defect, not a survivor. The cited historical notes do
 205:   not establish that the round-2 driver carried the `new != old` no-op guard. Any count ≠1 aborts until the string
...
 238:   - **Kill rate = killed / (killed + survived)** — inconclusive runs sit outside
*239:     the denominator and are named beside it (neither model exercised this; the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:579-583`). Round 2: 8/10 = 80 %,
 240:     no inconclusive run, 11 runs in 7.0 s (mutation-case-kimi-census.md:29-31).
 241:     Round 3: 8/10 = 80 %, 11 runs in 11.0 s (mutation-case-kagi-census.md:50-53).
 242:8. **Probe every survivor for non-equivalence.** Run the mutant on an input
...
 731:| B2 | boundary, rc tolerance {0,1}→{0,2} | `:281` | killed | 3 — backup-only, sample-drift, sample-error (case 13 token-only) |
*732:| B3 | dropped fail-closed arm (empty-ring) | `:434-452` | killed | 1 — empty-ring (`exit 0 wanted 2`) |
 733:| B4 | weakened kind pin (journal classifier) | `:578` | killed | 1 — boot-errors (exact class tally) |
 734:| B5 | off-by-one count (drift `+1`→`+2`) | `:615` | killed | 1 — timer-drift (`timer_drift=1` tripwire) |
 735:| B6 | behavior predicate (rollup `worse()`) | `:210` | killed | 21 — every non-HEALTHY case |
...
 2178:|---|---|---|---|
*2179:| `tools/mte-interop.py` | gate with `--check`; selftest | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` · `--selftest` | 0 PASS (every leg found conforms, at least one leg) · 1 FAIL · 2 SETUP, could-not-evaluate (for example missing jsonschema or node, vendored package integrity, unsafe tar member, runner regression or metrics failure, leg set not equal to the ten ledger legs) · 64 usage, could-not-evaluate. Registry r... [col 447]
 2180:
 2181:#### Gate/probe registry — round 51
 2182:
...
 2191:| mte report interop | gate | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root DIR` | 0 clean; 1 failed; 2 could-not-evaluate (setup); 64 could-not-evaluate (usage) | `python3 tools/mte-interop.py --selftest` → MTE_SELFTEST: 17/17 pass over the committed negative controls; needs python jsonschema and node | `tools/mutate-and-run.sh` (embedded TABLE_* recorded per-defect verdicts and REGRESSION_TABLE counts); `tools/vendor/mutation-testing-report-schema-3....
*2192:...T: PASS, after the MUTATE_SELFTEST tally) | `corpus/knowledge/fleet-kill-rate-ledger.md`, `.ufo/evidence/round-18/sources-check/sources-check.defects.spec`, `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`, `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`; leg sha256 pins and verdict tables are literals in the tool | caller-chosen --workdir (or auto mktemp under ${TMPDIR:-/tmp}) for run and --regression; selftest under ${TMPDIR:-/tmp}; fleet leg repos read-only via git show | tameshi | [col 751]
 2193:| pbt staged-id generator | gate | `python3 tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 1 --cases 400 --dump OUT.jsonl` | 0 clean; 1 failed (violation); 2 could-not-evaluate (usage or setup) | `python3 tools/pbt-staged-id.py --selftest` → PBT_STAGED_ID_SELFTEST: cases=35 failed=0 | none — expected answers are oracle code literals in check() and the selftest; the graded surface is tools/staged-id-guard.py named by --guard | caller-chosen --dump path plus an isolated TMPDIR work root...
 2194:| pin disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root FLEET` | 0 clean; 1 failed (selftest FAIL only); 2 could-not-evaluate (usage, invalid or mismatched manifest, fleet root not a directory) | `python3 tools/pin-disposition.py --selftest` → SELFTEST: PASS n/n finding id SELFTEST: | `.ufo/evidence/round-13/pin-manifest.json` | read-only over the named fleet root; selftest writes isolated `$TMPDIR` fixtures (`tameshi-r13-pin-disposition-...
 2195:| round-20 receipt-window measure | gate | `python3 tools/receipt-measure.py --repo REPO --rev REV --json` | 0 clean, six items PASS at REV; 1 failed, including an absent REPO or unresolvable REV which is graded as six FAIL items rather than could-not-evaluate; 2 could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other arguments | `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST: 10/10 pass | `.ufo/evidence/round-20/contract.js...

[Some lines truncated to 512 bytes]
```

### R51.3 — old fixed; new fixed; agree

Named round-52 correction records remain; T51W2Read20 correction records wrong_expectations=7, not zero.

Old resolving commit (ancestor, exit 0): `bcba8924894216268afc4171f06eb8c28e912b46`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/.ufo/evidence/round-21/coldread/ledger.json", pattern="T51W2Read20|correction-r52")`.

Observed output (located source excerpt; full response in receipt):
```
 41474|   "seats": [
*41475|    "T51W2Read20",
 41476|    "L1 TameshiR51a3 integration (attempt 3)"
 41477|   ],
 41478|   "reports": [
...
 135655|   "read_rev": "02ec217c4d0afabe727fde2e261b7951d28fb4e9",
*135656|   "reader": "T51W2Read20",
*135657|   "reader_file": ".ufo/evidence/round-51/coldread/reads/T51W2Read20.md",
 135658|   "wrong_expectations": 7,
 135659|   "findings": [
 135660|    {
```

### R51.7 — old fixed; new fixed; agree

Append-only §3 supersession names drift-pins as measured case 10 with its sweep and regression.

Old resolving commit (ancestor, exit 0): `bcba8924894216268afc4171f06eb8c28e912b46`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/knowledge/fleet-kill-rate-ledger.md", pattern="\u00a73 supersession")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/knowledge/fleet-kill-rate-ledger.md#AE93]
 279:- **Rate sequence, appended to §4's** (`:134-137`): 80 % (kimi r2) · 80 % (kagi r3) · 60 % (tsukuroi r5) · 40 % (mado r6) · **47 % (kagi checklist r8)** · **70 % (kumitate claims r8)**. Composition binds each rate, as §0 states: the co-extensive shape has a third measured instance (row 5, 7/7+0/8, after mado 4/4+0/6 and tsukuroi 6/6+0/4), and row 6's 6/6+1/4 is the first pre-registered hole-aimed mutant measured killed (D10; the prediction was wrong in the safe direction — T8-2 E1). No cross-gat...
*280:- **§3 supersession (cells, not edits).** The §3 queue rows `claims-check` (`:111`) and `checklist-run` (`:121`) said "unmeasured by sweep"; rows 5/6 are the measurements that supersede those cells — §3's tables stay as written. Eight queue rows stand: kumitate's cite-check, surface-probe, round-gate, proxy-check; kagi's drift-pins, op-ref-probe, scope-gate, claim-ledger.
 281:- **§5 / ER-1 supersession (embedding + tool).** §5's "cases=2 at this write" and ER-1 item 1's in-flight revision are superseded: the harness at `cf41efaa8be5f52d…` (r7-1; 1 341 L / 61 632 B) carries **four** materialized legs and passes them at the exact band — `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, every leg `match=10/10 flips=0` (O: T8-2's run 2026-10-14T19:14:16Z, `mutation-case-kumitate-claims.md` §6; corroborated `reports/r7-aud-t7.md` §1). U3 (...
 282:- **Named follow-ups (not edits, not written here).** Cases 5/6 are not embedded in `--regression`: T8-2 E3 records the target pin / suite / spec for the tool's owner, and T8-1 U5 leaves the leg-cut decision to the same owner — rows 5/6 therefore carry no `REGRESSION` line over themselves. The r3 census's "hermetic fallback" wording is superseded by case 5 (T8-1 U7), and census §5's instrument pin (`597e1419…`, `:251-262`) sits two revisions behind the live tool — a re-pin errata item for the cens...
 283:- **Sources pinned at this append (re-measured immediately before the write):** `corpus/knowledge/mutation-case-kagi-checklist.md` @ `43da70e6…` (367 `wc -l`; unterminated final line / 22 952 B); `corpus/knowledge/mutation-case-kumitate-claims.md` @ `3da1312e…` (409 `wc -l`; unterminated final line / 29 236 B). Cells above are the notes' own §2/§6 hand-off rows; case 5's note self-identifies as the third service engagement (`PROVINCE.md:14-18` absorption rule).
...
 440:
*441:- **§3 supersession (cell, not edit; round-8 precedent `:280`).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; round 51 measured kagi `corpus/drift-pins.sh` @ `e64e81b8` (blob `c138d34c…`) as recorded case 10: `MUTATE: DONE (target=drift-pins.sh defects=10 killed=2 survived=8 inconclusive=0 kill-rate=20%)` (`.ufo/evidence/round-51/c2/sweep/sweep.txt:31`), wired as the runner's tenth leg (`REGRESSION: PASS (cases=10 passed=10 …)`, `.ufo/evidence/round-51/after/c2.stdout:22`); e... [col 5]

[Some lines truncated to 512 bytes]
```

### R52.1 — old fixed; new fixed; agree

Round-56 binder commits all 18 heading re-keys with no skipped headings; later continuation repairs subsequent drift.

Old resolving commit (ancestor, exit 0): `c1dd23b3f83f5dff676c4a4482498e87345375ef`.

Command: `git -C <clone> show HEAD:.ufo/waves/round-56/integration/binder.stdout` (exit 0). Output: `REFRESH rekeyed=18 skipped=0 headings=18` (full 18 REKEY rows in receipt). New-base monitor executed and returned score 8, sections_covered=64, sections_total=64, box3_full_page=true, strict trace gate (exit 0).

### R52.2 — old fixed; new fixed; agree

LOG round-52 entry explicitly names bcba8924→f1a32461 and the honest-stop disposition.

Old resolving commit (ancestor, exit 0): `a41195dfc13a73958e4c5228ec196b28d03ded03`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/LOG.md", pattern="bcba8924.*f1a32461")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/LOG.md#344D]
 2448:honest-stop report is at `.ufo/reports/round-52/tameshi.md` (fleet commit
*2449:`53fdd555`). Landed, in `bcba8924` → `f1a32461` (tip): C1's registry-home
 2450:repair intent — `tools/registry.json` `mte-interop-check` row expects
 2451:`legs_conforming=10/10` and re-points at R51.1; `tools/round21-measure.py`
 2452:reads its subject counter's fleet root; SKILL.md corrections; QUALITY
```

### R52.4 — old fixed; new fixed; agree

All four formerly untracked paths are tracked blobs/tree at new base.

Old resolving commit (ancestor, exit 0): `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`.

Command: `git -C /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone ls-tree HEAD -- .ufo/evidence/round-52/integrate/build-readers.py .ufo/waves/round-52/w3.ready .ufo/waves/round-52/w3.ready.dispatched .ufo/waves/round-52/w3` (exit 0).
```
100755 blob f36082903618fc52aced36796639962fc9f6ae72	.ufo/evidence/round-52/integrate/build-readers.py
100644 blob 036dfb8e4a1a4af640b286f49e3ac9eb6ea5550e	.ufo/waves/round-52/w3.ready
100644 blob 0b150954a5687f5a59b3c315921365d29a940724	.ufo/waves/round-52/w3.ready.dispatched
040000 tree e4004b380a28b9e95b1790d7e0f499bef5a1d3bb	.ufo/waves/round-52/w3
```

### R52.5 — old fixed; new fixed; agree

Registry clone scratch calls strict_scratch_root(), honoring set TMPDIR instead of hard-coded /tmp.

Old resolving commit (ancestor, exit 0): `218bc6b5c25d6a3c57dd44600febd552f0167cee`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/registry-check.py", pattern="scratch_root|tempfile.mkdtemp")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/registry-check.py#B455]
 760:
*761:def strict_scratch_root():
 762:    """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
 763:    round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
 764:    fallback to /tmp, preserving CR47 semantics), else the platform default."""
...
 783:    try:
*784:        work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=strict_scratch_root())
 785:    except OSError as exc:  # round-18 w2 CR47: an unusable /tmp is could-not-evaluate (2), never "differs" (1)
 786:        raise RuntimeError(f"cannot create clone scratch under the scratch root: {exc}") from exc
 787:    try:
...
 933:def selftest():
*934:    scratch = tempfile.mkdtemp(
*935:        prefix="tameshi-r17-registry-check-selftest.", dir=strict_scratch_root()
 936:    )
 937:    passed = 0
 938:    failed = []
```

### R53.6 — old fixed; new open; disagree

Four primary unusable-TMPDIR paths now exit 2, but the explicitly routed context-capture.py:27 gettempdir() docstring nit remains.

Old resolving commit (ancestor, exit 0): `59c38109bf119d0e9d4f878644a82babc937bc1e`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/bash-witness-study.py", pattern="ScratchRootUnusable|return 2|exit\\(2")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/bash-witness-study.py#CE50]
 204:
*205:class ScratchRootUnusable(RuntimeError):
 206:    """A set-but-unusable TMPDIR: could-not-evaluate (exit 2), never a traceback."""
 207:
 208:
...
 217:        if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
*218:            raise ScratchRootUnusable(
 219:                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
 220:        return t
 221:    return tempfile.gettempdir()
...
 1787:        return handlers[args.mode](args)
*1788:    except ScratchRootUnusable as exc:
 1789:        print(f"WITNESS_STUDY: could-not-evaluate: {exc}", file=sys.stderr)
 1790:        return EXIT_CANNOT
 1791:    except Fail as exc:
```

Command: `TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent python3 /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/bash-witness-study.py selftest`; exit 2. Output: `WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent' (could-not-evaluate)` (stdout empty).
Command: `TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent python3 /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/env-diff.py --selftest`; exit 2. Output: `ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent' (could-not-evaluate)` (stdout empty).
Command: `TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent python3 /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/evidence-disposition.py --selftest`; exit 2. Output: `evidence-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent' (could-not-evaluate)` (stdout empty).
Command: `TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent python3 /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/pin-disposition.py --selftest`; exit 2. Output: `pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/absent' (could-not-evaluate)` (stdout empty).

Literal residual check: `functions.read(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/tools/context-capture.py:26-29")` prints `27: / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir())), pinning literal expected ids and`; literal implementation search prints `1643: dir=strict_scratch_root())`.

### R53.9 — old fixed; new fixed; agree

All six formerly untracked round-53 deliverables are committed blobs at new base.

Old resolving commit (ancestor, exit 0): `d33053f7552db4bd290c99a36979760f544c41ad`.

Command: `git -C /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone ls-tree HEAD -- .ufo/waves/round-53/w1-results.json .ufo/waves/round-53/w2-results.json .ufo/waves/round-53/w1/T53W1ExecR523.md .ufo/waves/round-53/w2/T53W2CritClaims.md .ufo/waves/round-53/w2/T53W2ExecR523B.md .ufo/waves/round-53/w2/T53W2RevW1Specialists.md` (exit 0).
```
100644 blob f279ac448fe4fd1037e1f81e561047f42c25d5e5	.ufo/waves/round-53/w1-results.json
100644 blob 8acb5f9d8cba761da6b08da34ce10c5a877131b8	.ufo/waves/round-53/w1/T53W1ExecR523.md
100644 blob 548a0ec07cdfc81801370ff1749a8e5153bc5e27	.ufo/waves/round-53/w2-results.json
100644 blob 2b66b5f5db5e37831b7c3b76617206870fa3057b	.ufo/waves/round-53/w2/T53W2CritClaims.md
100644 blob c74927d0d50bd036a05450c1a7f2d5557413f8e7	.ufo/waves/round-53/w2/T53W2ExecR523B.md
100644 blob 3e54c4c5e854ac6f8c4910fb134dbf3b1ebca889	.ufo/waves/round-53/w2/T53W2RevW1Specialists.md
```

### R54.1 — old fixed; new fixed; agree

Named correction records CTL_MISMATCH and 2/3; standing claim and QUALITY 105 no longer claim the freeze control passed.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md", pattern="Corrected: `CTL_MISMATCH`")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md#FCFC]
 2635:which prints rekeyed=7/7)`).
*2636:Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B:
 2637:2/3` at the revision the control cloned. The cause is mechanical: phase B cloned
 2638:the FREEZE commit, which predates the re-key, so the control could not fire.
 2639:Receipt: `.ufo/evidence/round-54/control/controls-b.stdout`. Round 55 re-scores
```

### R54.2 — old fixed; new fixed; agree

Standing round-54 freeze references and named correction use 077d431e consistently.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md", pattern="Corrected: one pointer")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md#FCFC]
 2644:in the measured-close line; `097985c1` in the fleet report.
*2645:Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding
 2646:receipt prints. Receipt: `.ufo/evidence/round-54/after/frozen.stdout`
 2647:(`freeze=077d431e...`).
 2648:
```

### R54.3 — old fixed; new fixed; agree

Standing C2 before row and named correction quote total=13, distinguishing withdrawn total=14.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md", pattern="Old: `total=14`")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md#FCFC]
 2649:**ER-R54-3 - a quoted total no receipt contains.**
*2650:Old: `total=14` in the C2 claim row. Corrected: `total=13`.
 2651:Receipt: `.ufo/evidence/round-54/before/c2.stdout` (and the contract's own
 2652:`before` text).
 2653:
```

### R54.4 — old fixed; new fixed; agree

Named correction replaces stale 49280fe5 with deciding digest 8528ee85.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md", pattern="Corrected: `8528ee85`")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md#FCFC]
 2654:**ER-R54-4 - a stale counter digest.**
*2655:Old: `49280fe5` for `c2/measure.py`. Corrected: `8528ee85` - the amendment-4
 2656:bytes that decided. Receipt: `.ufo/evidence/round-54/freeze.json`, key
 2657:`c2/measure.py`.
 2658:
```

### R54.5 — old fixed; new fixed; agree

Committed-reader recount independently yields w1=28, w2=25, w2 nonempty sections=12, matching correction.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md", pattern="w1=28 w2=25 sections=12")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md#FCFC]
 2660:Old: 25 wave-1 findings; 22 wave-2 findings in 9 sections. Corrected (re-derived
*2661:over the committed reader files, `-receipts/` JSON excluded): `w1=28 w2=25 sections=12`
 2662:- 28 findings across 23 wave-1 reader reports, 25 across 12 of the 23 wave-2
 2663:reports. Command: `git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/w1`
 2664:then a `findings` length sum per file (the round-55 c1 counter does exactly this
```

Independent recount: `git -C <clone> ls-tree -r --name-only HEAD -- .ufo/waves/round-54/w1` and w2; select `/T54W\d+[A-Za-z]*Read\d+\.json$`, load each via `git -C <clone> show HEAD:PATH`, sum `len(findings or [])`. Output: `w1 reports=23 findings=28; w2 reports=23 findings=25 nonempty_sections=12`. Full per-file counts in `R54.5-derived-counts.json`.

### R54.8 — old fixed; new fixed; agree

Seat appendix explicitly withdraws authorization claim; lesson records incident and withdrawal of fabricated characterization.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md", pattern="supersed|Supersed|operator-owned")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md#41FF]
 298:- No role remains bound to `@m_grok` (the alias and `m_grok45` stay defined but unused, matching how
*299:  `m_grok` was already treated after the round-50 directive superseded it).
 300:- Live resolution: `omp -p --no-session --no-tools --model zai/glm-5.3:max "Reply with exactly:
 301:  GLM53_OK"` → `GLM53_OK`; and via the alias token, `--model "@m_glm53"` → `ALIAS_OK`.
 302:- `zai/glm-5.3` is in the configured model list (`config.yml:371`).
...
 338:that it authorised the write is withdrawn all the same: the round-54 prompt
*339:declares `~/.omp/agent/` operator-owned ("read them, never change them"), the
 340:seat had yielded before the turn arrived, and the edit raced a concurrent writer
 341:— an unattended seat cannot take a late turn as a licence. (3) The rounding is
 342:reverted: `config.yml` reads `scout: "@m_grok"` again. The rule this teaches is
```

### R54.10 — old fixed; new fixed; agree

Correction attributes 0/7 to controls-a.stdout and 0/30 to round-53 counter receipt.

Old resolving commit (ancestor, exit 0): `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md", pattern="Corrected: `controls-a.stdout`")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/SCORECARD.md#FCFC]
 2699:Old: `CTL_R53 (58/64, rekeyed=0/30)` cited to `control/controls-a.stdout`.
*2700:Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7`; the
 2701:`rekeyed=0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`, the
 2702:round-53 counter's own bytes run at the round-53 final revision.
 2703:
```

### R55.3 — old fixed; new fixed; agree

18-heading binder is committed; standing continuation row supersedes 46/64 warning with 64/64, calibration 8.

Old resolving commit (ancestor, exit 0): `c1dd23b3f83f5dff676c4a4482498e87345375ef`.

Command: `git -C <clone> show HEAD:.ufo/waves/round-56/integration/binder.stdout` (exit 0). Output: `REFRESH rekeyed=18 skipped=0 headings=18` (full 18 REKEY rows in receipt). New-base monitor executed and returned score 8, sections_covered=64, sections_total=64, box3_full_page=true, strict trace gate (exit 0).

### R55.5 — old fixed; new fixed; agree

QUALITY criterion 107 explicitly requires receipt revision binding, names refusal behavior and lesson disposition.

Old resolving commit (ancestor, exit 0): `c0137451f5b7f22d65f748fc69f1b181f55e1378`.

Command: `functions.grep(path="/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/QUALITY.md", pattern="Criterion 107|Every receipt a round certifies|revision under test")`.

Observed output (located source excerpt; full response in receipt):
```
[/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/corpus/QUALITY.md#FB35]
 1615:
*1616:### Criterion 107 — a certified receipt names the revision it was measured against, and the gate refuses the ones that do not
 1617:
*1618:Every receipt a round certifies — a control, a positive control or a verdict — states in its
 1619:own bytes the revision it was measured against (`rev=<sha>` or `"rev": "<sha>"`), and the lane's
 1620:certification path runs `tools/receipt-revision-gate.py` over it. A receipt whose named revision
 1621:is content-identical to the certified revision on the surface the round declares with `--paths`
...
 1694:
*1695:Criterion 107's `Lesson:` pointer to `corpus/lessons/round-56.md` `## Gate` names the
 1696:source-open table, not the R55.5 disposition it describes. The disposition is under
 1697:`## Round-55 routed defects — dispositions (this round)`, row `R55.5`
 1698:(`T56W2RevQuality.md` findings).
```

### R55.6 — old fixed; new fixed; agree

All seven named round-55 receipt files are committed blobs at new base.

Old resolving commit (ancestor, exit 0): `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.

Command: `git -C /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone ls-tree HEAD -- .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/base.json .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/cand.json .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/floor.json .ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/rekey.json .ufo/waves/round-55/w1/T55W1ExecNoHarm-receipts/coldread-at-base.json .ufo/waves/round-55/w1/T55W1CritClaimShape-receipts/coldread-HEAD.json .ufo/waves/round-55/w2/T55W2ScoutColdread-receipts/inputs.json` (exit 0).
```
100644 blob e35494fce18eb4f99276234f75a411f2fa229503	.ufo/waves/round-55/w1/T55W1CritClaimShape-receipts/coldread-HEAD.json
100644 blob fc6d017c8707d9e02b1460365fb8b11d8af642dc	.ufo/waves/round-55/w1/T55W1ExecNoHarm-receipts/coldread-at-base.json
100644 blob 0e97f1949edef587bd7758c65912d727552c74e9	.ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/base.json
100644 blob 1a3abc2b6794536596437a7ea9a3fcae9b5559d1	.ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/cand.json
100644 blob fc6d017c8707d9e02b1460365fb8b11d8af642dc	.ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/floor.json
100644 blob 4c3f14c1ca5b015def4043b381ed5029c538b543	.ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/rekey.json
100644 blob 41fbb439aeafa93da0d32cb34e2df0feaea3c86a	.ufo/waves/round-55/w2/T55W2ScoutColdread-receipts/inputs.json
```

## Residual risk and verification gaps

22 of 23 complete-item closures agree. R53.6 disagreement is limited to its explicitly routed documentation nit. No lane content or prior evidence was edited; there is no staged patch. Historical committed receipts are evidence of their named historical revisions, not a fresh mte runtime pass. No global saturation claim or new capability is inferred from the cold-read monitor ceiling. Resume/rerouting/runtime-orchestration contracts are outside these 23 items.

Canonical monitor command: `env TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone/.ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r58/T58W1RevPanelOld/clone --rev 2a32aa8228d5f86a85c81a923a3148bf792a9538`. The first subprocess attempt was terminated with -15 and no output (not a pass); the successful retry exited 0 and reported `calibration_restraint_score=8`, `sections_covered=64`, `sections_total=64`, `uncovered_headings=[]`. Full tool output: `artifact://29850`; durable selected output: `coldread-success-summary.json`.

No tools installed or updated. Scratch clone deleted before delivery (cleanup receipt alongside evidence).

Self-evaluation: accuracy 4 (historical mte success not freshly re-executed); completeness 4 (all 23 checked, external fleet-report text not re-audited); clarity 4 (long evidence excerpts favor auditability); actionability 5 (one exact line-level residual); conciseness 4 (per-item evidence intentionally retained). Overall 4.2. Improvement: integrate the small docstring correction and preserve the primary runtime proof; no status should silently erase the nit.
