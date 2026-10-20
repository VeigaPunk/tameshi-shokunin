author: tameshi-shokunin (lane L1, round 16)

# Round 16 — seventh recorded case and full-page cold-read

Claims: **C1 depth 6→7** (seventh recorded mutation case: kumitate
`round-gate.mjs`, leg `js-round-gate`); **C2 calibration 6→8** (full-page
cold-read of `SKILL.md` earns the box-3 lane assertion). Routed defects from
`round-15-verifier-spotcheck.md`: 1 (sibling-overlap scan) and 2 (usage
attribution) are done this round. Waves: `.ufo/waves/round-16/`.

## Gate

Candidates and decisions (admit = lands in corpus/registry/tooling; reject =
recorded, not landed):

| # | Candidate | Decision | Reason |
|---|---|---|---|
| G1 | `knowledge/mutation-case-kumitate-round-gate.md` (case 7) | admit | measured sweep, 10/10 predictions committed before it, receipts retained, ledger leg replays `cases=7` |
| G2 | the `INTERNAL_ERROR` token mutant (RGD-B3) as a case defect | reject | catch-all uninhabited by any input (SurvivorPrep P12); a survivor would be equivalent by unreachability and measure nothing |
| G3 | `REPORT_MIN_BYTES` 1024→512 (RGC-THIN-FLOOR) | reject | a midpoint of the projected interval cannot test the bound; replaced by the 1059/1060 edge pair (RGCritic F5) |
| G4 | `controls_match` as the round-gate control claim | reject | stdout carries `mkdtemp` names; `repeat-control.py` → `controls_mismatch` exit 1 (RGControl); verdicts are graded on exit only |
| G5 | the bare suite `node "$MUTANT" --selftest` for the leg | reject | exported `GIT_DIR` makes the pristine control commit into a foreign repo (RGSentinel canary); guarded `env -i` suite admitted instead |
| G6 | full-page cold-read ledger as box-3 evidence | admit | every bucket of the final page has a passing entry at its own section sha; repaired sections re-read in wave 2 |
| G7 | CR24's `verified-record` on snapshot section 1464 | reject (overridden stricter) | the section said "Box 3 remains `[ ]`" while `SHONEN.md:9` said `[~]` at the same HEAD (CRCritic1, CRCritic2); repaired and re-read |
| G8 | AttrFix's first "new rule" (`^[A-Z_]+: [A-Z_]+ \(id=… exit=…\)$`, stderr-first) | reject | returns null on real text verdicts with extra fields and drops verify.py's JSON branch (AttrCritic); repaired rule admitted |
| G9 | in-place SKILL repairs that keep every edited section's line count | admit | page self-anchors (`SKILL.md:<n>`) still resolve; old text recorded in the appended errata table and git |
| G10 | "50 sections" as the cold-read denominator | reject | 51 buckets: the preamble is a bucket (CRRevenger, CRCritic1, CRCritic2) |

Sources opened this round (rule 1 — URL, access date, quote ≤25 words with location):

| Row | URL | Accessed | Quote (location) |
|---|---|---|---|
| S052 | https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ | 2026-10-20 | "We've aligned on a standard naming scheme so it is easy to switch and compare implementations." (§Supported mutators, opening paragraph, sentence 2) |
| S053 | kumitate-shokunin `git show 364f1d5:scripts/round-gate.mjs` | 2026-10-20 | "a green verdict asserts nothing fleet-wide, and running the gate does not change mission completion" (header comment, :19-20) |
| S054 | https://diataxis.fr/compass/ | 2026-10-20 | "To use the compass, just two questions need to be asked: action or cognition? acquisition or application?" (§The compass ¶22) |
| S055 | https://docs.python.org/3/library/doctest.html | 2026-10-20 | "To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented." (module introduction, first bullet) |
| S056 | https://pitest.org/quickstart/mutators/ | 2026-10-20 | "The conditionals boundary mutator replaces the relational operators `<, <=, >, >=` with their boundary counterpart as per the table below." (§CONDITIONALS_BOUNDARY) |
| S057 | https://discovery.ucl.ac.uk/id/eprint/10056704/1/survey.pdf | 2026-10-20 | "Detecting equivalent mutants is a well-known undecidable problem" (§5.3.1, p. 29, preprint) |

Registry changes: rows S052–S057 added (status `mined`, used-by this lesson
or `knowledge/mutation-case-kumitate-round-gate.md`); no existing row's
status, recheck or used-by changed. Id-allocation footer: next unused
S052 → S058. Search-log entry appended (survey's published chapter 403;
preprint opened, tiered B).

Spot-check: the outside admit/reject sample is the separate non-author
closure's duty; not claimed here.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| attribution | `round-15-verifier-spotcheck.md`, Routed defects 2; `.ufo/evidence/round-15/verification-3.json` rows `usage-proof-new` and `gate-usage` record `observed_id: context_consistent` taken from help text by `verify.py:207-210` (first `id=` match) | none (QUALITY 17 covers the gate's own selftest, not the integration runner's parser) | QUALITY 18. `.ufo/evidence/round-16/attribution/reattribute.py --selftest`: on the same retained bytes and oracles the old rule fails 3/4 fixtures (both usage rows plus a forged-first-line fixture) and the repaired rule passes 4/4. `correction.json` names exactly the two rows; `verification-3.json` sha256 `3c419055…d8ce` unchanged. The same misattribution sits in `verification.json` (round-15 attempt 1) and is named here, not corrected. |
| attribution | this round's own AttrFix brief specified `^[A-Z_]+: [A-Z_]+ \(id=…\) exit=…\)$` stderr-first, dropping verify.py's JSON branch; AttrCritic (`w1/AttrCritic.md`) showed it nulls real verdicts with extra fields | AttrCritic (same-wave falsifier) | Rule repaired (JSON branch kept; last full-line `CONTEXT:` verdict whose `exit=` equals the process exit; both-stream verdicts → null). The seat's first output is kept as `correction-attrfix-draft.json` and is superseded, not cited. |
| landing | `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15`: a 605 B seat note written to the bare id `TameshiR15` landed as a file at the fleet root. Round-15 per-seat prompts said `Message only TameshiR15`, 66/66 without `agent://` (Misroot) | none | QUALITY 19. Round 16's wave contexts and every per-seat acceptance line name `agent://TameshiR16`. The detection is a no-pathspec fleet-root sweep plus a root-entry check. Misroot's replay of the archived bytes → rc 1 `STRAY [TameshiR15]`; the `.ufo/` pathspec arm → rc 0 (the historic miss). See `w1/Misroot.md`. |
| scope | wave 1: RGLeg was assigned to edit `tools/mutate-and-run.sh` in place while cold-read seats executed that file; the live file was `2e810b5d…` with placeholders at 10:27:20 and was restored to `75ed934d…` by 10:27:45 (RGCritic F10, CRSentinel). CR23's first regression attempt hit it and returned SETUP rc 2. | RGCritic (same-wave) | QUALITY 20. RGLeg was redirected to a staging path, and the staged copy was installed after the readers finished. CR23 re-ran on committed bytes and passed. No wave-1 verdict rests on the in-flight bytes. |

## Process disclosures

- Wave 1: 68 seats dispatched in one `task` call (validator `run`, policy v2),
  68 completed, 0 dead. Host-required `solutionSpace` was added to each task
  payload; names, roles and task text were passed unchanged.
- The pre-registration commit was rebased over a remote operator commit
  (`0baf52e`, `considerthese/2026-10-20.md`). The pushed commit `e69b488` has
  committer time 10:39:59-03:00, before the sweep at 10:40:15-03:00.
- The round's runner edit drifts round 15's retained integrity pin
  (`verification-3.json` pins the runner at `75ed934d…` and SHONEN at
  `3b1dc526…`). Round 15's receipt is not re-claimed green at this HEAD.
