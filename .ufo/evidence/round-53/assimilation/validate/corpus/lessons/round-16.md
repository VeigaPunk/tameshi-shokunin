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
| G6 | full-page cold-read ledger as box-3 evidence | admit | every bucket of the final page (54 at the landing sha) has a passing entry at its own section sha. Unchanged buckets carry wave-1 entries; buckets repaired after wave 1 were re-read in wave 2, and buckets repaired after wave 2 in the residual check (w3). The ledger is committed with the landing; at `c699c8c` it did not exist yet (see Mistakes) |
| G7 | CR24's `verified-record` on snapshot section 1464 | reject (overridden stricter) | the section said "Box 3 remains `[ ]`" while `SHONEN.md:9` said `[~]` at the same HEAD (CRCritic1, CRCritic2); repaired and re-read |
| G8 | AttrFix's first "new rule" (`^[A-Z_]+: [A-Z_]+ \(id=… exit=…\)$`, stderr-first) | reject | returns null on real text verdicts with extra fields and drops verify.py's JSON branch (AttrCritic); repaired rule admitted |
| G9 | in-place SKILL repairs that keep every edited section's line count | admit | page self-anchors (`SKILL.md:<n>`) still resolve; old text recorded in the appended errata table and git |
| G10 | "50 sections" as the cold-read denominator | reject | 51 buckets on the snapshot, counting the preamble (CRRevenger, CRCritic1, CRCritic2). The landing page has 54: three sections are appended |
| G11 | swapping in the `bwrap` suite after the sweep (GuardAudit) | reject this round | the suite string is part of the pre-registration; changing it post hoc would void the 10/10. Its limits are recorded in the note §6; confinement is next-round work |
| G12 | ledger `--override` entries | reject (none used) | every ledger verdict is a seat's own verdict, merged strictest-wins. CalibCritic showed replacement overrides bypass heading validation |
| G13 | leg-count agreement check in the runner selftest | admit | MutateLeg (b) survived a dropped tuple; the new check fails on that same mutant (`legcount-redbefore-mutant.txt`: 81/82, `selftest leg tuples=6`) and passes 83/83 on the landed runner |

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
| attribution | `round-15-verifier-spotcheck.md`, Routed defects 2; `.ufo/evidence/round-15/verification-3.json` rows `usage-proof-new` and `gate-usage` record `observed_id: context_consistent` taken from help text by `verify.py:207-210` (first `id=` match) | none (QUALITY 17 covers the gate's own selftest, not the integration runner's parser) | QUALITY 18, superseded in its proof clause by 22. `.ufo/evidence/round-16/attribution/reattribute.py --selftest`: on the same retained bytes and oracles the old rule fails 3/4 fixtures (both usage rows plus a forged-first-line fixture) and the repaired rule passes 4/4. `correction.json` names exactly the two rows; `verification-3.json` sha256 `3c419055…d8ce` unchanged. The same misattribution sits in `verification.json` (round-15 attempt 1) and is named here, not corrected. |
| attribution | this round's own AttrFix brief specified `^[A-Z_]+: [A-Z_]+ \(id=…\) exit=…\)$` stderr-first, dropping verify.py's JSON branch; AttrCritic (`w1/AttrCritic.md`) showed it nulls real verdicts with extra fields | none (found by AttrCritic, a same-wave seat) | Rule repaired: JSON branch kept; last full-line `CONTEXT:` verdict whose `exit=` equals the process exit; both-stream verdicts → null; lines split on `\n` only (AttrCritic2's VT forgery). The repaired selftest first passed six weaker rules (MutateReattribute, 6/6 survived). It now has eight fixtures, and five of the six weaker rules fail it (`selftest-mutants.json`). The survivor, stdout-first precedence, is equivalent once both-stream verdicts are null. QUALITY 22. The seat's first output is kept as `correction-attrfix-draft.json`, superseded and not cited. |
| landing | `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15`: a 605 B seat note written to the bare id `TameshiR15` landed as a file at the fleet root. Round-15 per-seat prompts said `Message only TameshiR15`, 66/66 without `agent://` (Misroot) | none | QUALITY 19. Round 16's wave contexts and every per-seat acceptance line name `agent://TameshiR16`. The detection is a no-pathspec fleet-root sweep plus a root-entry check. Misroot's replay of the archived bytes → rc 1 `STRAY [TameshiR15]`; the `.ufo/` pathspec arm → rc 0 (the historic miss). See `w1/Misroot.md`. |
| attribution (write scope) | wave 1: RGLeg was assigned to edit `tools/mutate-and-run.sh` in place while cold-read seats executed that file; the live file was `2e810b5d…` with placeholders at 10:27:20 and was restored to `75ed934d…` by 10:27:45 (RGCritic F10, CRSentinel). CR23's first regression attempt hit it and returned SETUP rc 2. | none (found by RGCritic, a same-wave seat) | QUALITY 20 and 21. RGLeg was redirected to a staging path, and the staged copy was installed after the readers finished. CR23 re-ran on committed bytes and passed. CR22 started (13:25:57Z) before the edit window and checked the runner sha only at start, so its regression run may have overlapped the edit; its receipt reports the committed six-leg result (`cases=6 passed=6`), which only the committed bytes produce. |
| vacuous | `.ufo/evidence/round-16/measure.py` at `c699c8c` read only the `- [~]` box line for the SHONEN box-3 ledger link, while SHONEN.md carries every box's link on the indented continuation line. Its 33-case selftest passed because each fixture put the link on the box line itself: the fixture shape matched the tool, not the real file. | none (L1 found it on the first real measurement) | Repaired `shonen_boxes` reads each box's block (box line plus indented continuation lines). Same command, same rev `c699c8c`: old tool `box3_ledger_link: false`, repaired tool `true` (`.ufo/evidence/round-16/measure-repair/`). Two new selftest cases, a continuation-line link (credited) and a link under box 4 only (not credited), bring the selftest to 35/35. |
| landing | at `c699c8c`, SHONEN box 3, the SKILL errata and the README append all cited `.ufo/evidence/round-16/coldread/ledger.json` before it existed. `measure.py --rev c699c8c` → restraint 6, `ledger_present: false` (MistakeAudit, ReadmeAppend, RoutedLedger, WholePage) | QUALITY 2 and 9 (claims carry a resolvable anchor) | The ledger is assembled from the w1/w2/w3 seat reports and committed in the landing commit. C2 is measured only at that commit; `c699c8c` is reported as 6. |
| stale-premise | the cold-read found 13 wrong or stale present-tense statements across SKILL.md (CR02, CR05, CR06, CR10, CR16, CR23, CR27, CRCritic1/2), plus 6 more in wave 2 (RR01, RR08, RR10, RR11, RR13, WholePage) | none (no prior round re-read the whole page) | Repaired in place with line counts kept, so self-anchors resolve (AnchorCheck). Each repair has a row in SKILL.md's errata table, and each repaired bucket was re-read by a fresh seat. |
| reference-drift | the runner edit moved a pinned input of the round-13/14 evidence gate: `evidence-disposition.py --root .` now returns 2 `expected_input_digest_mismatch` (RR10) | the gate itself (by design) | Correct fail-closed behaviour. The registry row now names the archived-root invocation (`git archive 28aeef4` → exit 0). Round 15's `verification-3.json` runner pin drift is disclosed below. |
| number-drift | the C2 denominator was stated as 50, then 51; the landing page has 54 buckets (G10) | CRRevenger, CRCritic1/2 (same wave) | The ledger and `measure.py` count buckets from the bytes at the measured revision; no fixed denominator is claimed. |
| vacuous | `.ufo/evidence/round-16/coldread/assemble.py` and `measure.py` selftests let survivors through: MutateMeasure 3/9 survived (unknown class, executed-ok record, whitespace-only trailing lines); MutateAssemble 2/8 survived (executed-ok downgrade, equal-rank override) | none | Cases added for each (`measure.py` 38/38, `assemble.py` all checks). Each new case asserts the exact behaviour its surviving mutant changed. |

## Same-round falsification (wave 2)

Wave 2: 67 seats, all completed. The attacks that held: RerunSweep
reproduced every verdict and mutant sha256. RerunRegression, RR07 and
Replica1021 each got `cases=7 passed=7`. PreregAudit confirmed the timing
and spec identity. KillWidthAudit, NoteClaims and CKINDCheck held, and
C1059Probe supplied the missing survivor witness. All six source re-opens
held, and the SourcesCensus manual commands came out clean.
EvidenceImmutable found 38 additions and 0 modifications; ToolsNoHarm found
all nine selftests green. The attacks that found defects are folded into
the Mistakes rows above, the SKILL errata rows, and the note §2/§5/§6
corrections: MutateLeg, MutateMeasure, MutateAssemble, MutateReattribute,
AttrCritic2, GuardAudit, RR01, RR08, RR10, RR11, RR13, WholePage,
MistakeAudit and ReadmeAppend. The residual re-read (w3, 8 reviewer seats,
one ordinary task call) covered the 9 buckets changed after wave 2.

## Process disclosures

- Wave 1: 68 seats dispatched in one `task` call (validator `run`, policy v2),
  68 completed, 0 dead. Wave 2: 67 seats, one call, 67 completed, 0 dead.
  Residual check: 8 reviewer seats, one ordinary call. Round total 143. Host-required `solutionSpace` was added to each task
  payload; names, roles and task text were passed unchanged.
- The pre-registration commit was rebased over a remote operator commit
  (`0baf52e`, `considerthese/2026-10-20.md`). The pushed commit `e69b488` has
  committer time 10:39:59-03:00, before the sweep at 10:40:15-03:00.
- The round's runner edit drifts round 15's retained integrity pin
  (`verification-3.json` pins the runner at `75ed934d…` and SHONEN at
  `3b1dc526…`). Round 15's receipt is not re-claimed green at this HEAD.
- The wave-1 report `w1/CRMeasure.md` was appended by its seat after the
  pre-registration commit (the seat reported its interface follow-up) and
  landed in `c699c8c`; `w1/Overlap1.md` carries an appended erratum at the
  L1's request (`:219`).
- Open debt, named: the six older ledger legs still run their suites with the
  inherited environment (only `js-round-gate` is scrubbed; MistakeAudit O7);
  the round-7 section's runner line anchors predate the tool's growth; the
  cold-read contract left "page-named but never-open" files to each seat's
  judgement (ContamA, ContamB), and seats split on it. No ledger verdict
  flips either way.
- The residual re-read found one more minor gap (RX9): the "line count of
  every edited section unchanged" statement is one section short, because
  `### Round-15 gate/probe registry` gained a trailing blank line when the
  round-16 sections were appended. Anchors are unaffected (AnchorCheck
  22/22).
- RX1 first labelled the preamble (a record) `executed-ok`. At the L1's
  request it appended a corrected block (`verified-record`) giving its
  reason. No other seat verdict was changed.
- The final errata re-read seat was refused once by the session job cap
  (100) and dispatched on the retry (`spawn4-errata.json`).
