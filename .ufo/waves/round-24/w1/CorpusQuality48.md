# CorpusQuality48 — critic attack on QUALITY48 (round24 W1, calibration)

Seat: TameshiR24-2.CorpusQuality48 (critic, static read-only). Revision inspected: `c8c5b88c8e961a929cdc351b95a7074c76958909`; base `6a1821a8897eea6e7d9669292160ec9593669409`.

## Verdict

**Admit only with narrowing.** QUALITY48 (`corpus/QUALITY.md:487-502`) is lesson-backed and does not contradict QUALITY46 or QUALITY47. All the defects below are fixable; none forces a reject.

- **Not yet falsified-and-recorded.** The falsifier is a prediction ("is expected to give 11/11"). No executed outcome is in the repo, which violates QUALITY6.
- **Partly a second authority.** Two of its three bullets restate QUALITY29 and QUALITY25.
- **Its own detector list excludes 2 of its 11 predicates.**
- **"Fails at base" is met vacuously** for the 5 new-tool predicates.
- **The "routed" denominator is neither complete nor purely routed.**

## Findings (counterexample → evidence → smallest safe correction)

### D1 (high; impacts calibration and provenance). The falsifier is a pre-registration with no recorded outcome

**Counterexample.** QUALITY48 ends with "the round24 ruler gives 1/11 at 6a1821a and is expected to give 11/11 after the change" (`QUALITY.md:501-502`). QUALITY6 (`QUALITY.md:14-16`) requires that "a pre-registered prediction carries its executed outcome in the same entry".

**Evidence.** At c8c5b88 no after-measurement exists anywhere in the repo:
- The lesson's Mistakes row says "The after measurement is recorded below once executed" (`lessons/round-24.md:53`), and the file ends there.
- `SCORECARD.md:1144-1146` says "Measured results are recorded below only after execution", with nothing below.
- The knowledge entry's `verified-at` line (`knowledge/replay-projection-hardening.md:2`) also defers.
- No `after.json` exists under `.ufo/evidence/round-24/`.
- The only after-result is the untracked seat report `.ufo/waves/round-24/w1/RunRulerAfter.md`: 11/11, exit 0 at c8c5b88. `git status` shows `?? .ufo/waves/round-24/`. Under QUALITY8 it is not yet citable as a pass.

**Correction.**
1. Commit an after receipt beside `before.json`: argv, revision c8c5b88, exit 0, stdout, and `instrument_sha256` 0a7f6daa….
2. Fill in the lesson row and the SCORECARD.
3. Append a dated outcome line under QUALITY48 (append-only, the same pattern QUALITY47 used for QUALITY46), stating "executed: 11/11 exit 0 at c8c5b88". Do not edit 48's text.

### D2 (medium; impacts duplicate authority and lesson grounding). Two bullets restate earlier criteria, and the lesson's "gap" claim is false

**Counterexample.** QUALITY48 bullet 1 accepts "a selftest kill of a named mutant". QUALITY29 (`QUALITY.md:175-187`) already defines a surviving mutant as a weakening that leaves the owning `--selftest` at exit 0, and obliges the owner to add a killing case the next round. QUALITY48 bullet 3 (supersession is `superseded` plus `superseded_by` plus a new active row) restates QUALITY25 (`QUALITY.md:143-147`). It drops 25's clause "and still runs", although the knowledge entry repeats that clause (`knowledge/replay-projection-hardening.md:23-26`).

**Evidence.**
- **The lesson's "gap" claim.** The lesson's Captured-by cell says "no criterion required routed gaps to become failing predicates" (`lessons/round-24.md:53`). The round-18 preamble already says "Each criterion turns one routed item … into a falsifiable rule … the check that can fail" (`QUALITY.md:171-173`). Combined with QUALITY6, QUALITY11 ("trigger the same committed mismatch oracle after the repair", `:34-37`) and QUALITY29, the fail-before/hold-after obligation already exists.
- **What is new in 48.** Only the counting rule is novel: a predicate already discriminated at base is a control, not a repair, and "repaired" requires a base failure.
- **"Append-only" is not literally true.** QUALITY48 calls supersession "append-only". `git diff --numstat 6a1821a c8c5b88 -- tools/registry.json` gives `46 3`: three `"status": "active"` lines were replaced in place. QUALITY35 (`:276-277`) defines append-only as zero deleted lines.
- **Mechanics are otherwise sound.** Every `superseded_by` target is active, and `registry-check.py:277-297` enforces that.

**Correction.** In an appended narrowing (do not edit 48):
- Cite QUALITY25 and QUALITY29 as the governing rules for the mutant and supersession mechanics, and keep "still runs".
- Call the registry change "supersession (QUALITY25)" rather than "append-only".
- State 48's own contribution as the counting rule.

### D3 (medium; impacts falsifiability). The closed detector list excludes K10 and K11

**Counterexample.** "The predicate must use the public detector: a selftest kill of a named mutant, a pinned registry row failing on a self-consistent substituted bundle, or a refusing CLI projection" (`QUALITY.md:491-493`). Two of the ruler's predicates fit none of these:
- K10 discriminates on exit 0 with `live_dependent == ['one']`, which is a listing, not a refusal (`measure.py:181-184`).
- K11 discriminates on `--plan` exit 0 with realpath fields (`measure.py:190-200`).

So either the list is closed and 2/11 of the round's own predicates are non-conforming, or it is illustrative and "must" is unenforceable.

**Correction.** Append a narrowing: "…or a public CLI output assertion with a passing control on the same fixture". Alternatively, name K10 and K11 as conforming listing and plan assertions.

### D4 (medium; impacts calibration). "Fails at the base revision" is satisfied vacuously by tool absence

**Counterexample.** `before.json` K7–K11 fail at base only with `"reason": "tool-absent"` (`measure.py:143-144`). Any predicate written against a new tool flips from 0 to 1, including one for a gap that never existed. The base failure therefore shows absence, not the routed defect.

**Evidence.** The routed defects were in the round23 `replay.py`: it drops held/cleanup/external fields, compares siblings by string, and has unbounded streams (`fresh-adjudication.json:69-94`). `SKILL.md:2045` says "The round23 replay instrument stays unchanged". The repair is a successor tool, `tools/registry-replay.py`, not a change to the defective artifact. Contrast K1–K3 and K5–K6, whose base failures do exhibit the defect: mutants survive 38/38, and substituted bundles still hold.

**Correction.** Append a split:
- **"Repair":** the base failure exhibits the defect on the base artifact.
- **"New capability":** the base failure is tool-absent. Report it separately, here 5/11.

Neither requires re-freezing the ruler.

### D5 (medium; impacts the provenance of "routed" and denominator completeness). The 11 are not all routed, and routed gaps are missing

**Counterexample A: K2 was never routed.** K2 `argv-casefold` has no routing source:
- No match for casefold/case-fold/`.lower()`/case-insensitive anywhere in `.ufo/waves/round-23/`.
- None in fleet `MANIFEST.json` rounds[421].
- None in the round23 routed list (`lessons/round-23.md:170-180`).

Yet the contract says all eleven are "routed by round23 critics and closure" (`contract.json:3`).

**Counterexample B: routed gaps with no predicate and no stated disposition.**
- **Runner digest from the clone copy.** It is routed (`lessons/round-23.md:178`, `SCORECARD.md:1123`, MANIFEST "hash clone runner copy"). It is implemented (`registry-replay.py:162-163,177`) but no selftest case or ruler predicate covers it: the selftest cases are at `:199-206` and `:242` and none checks `runner_sha256_clone_copy`. The knowledge table still lists it in the "Hardened rule" column (`knowledge/replay-projection-hardening.md:21`). Under 48's own rule it "does not count as repaired".
- **Multi-token stdout fixture in the ruler.** The round23 ten-case ruler still has only a single-token `missing-stdout-token` case (`RunR23Ruler.md`).
- **Others.** "Re-run guard sweep", "dead-falsifier coverage gap" and "loose stdout tokens" are absent from the round24 lesson and contract.

QUALITY48 has no clause requiring every routed gap to enter the denominator or carry an explicit disposition. Compare QUALITY44 ("never dropped from the denominator", `:432-439`) and QUALITY12 ("Report all declared defects, unresolved denominators", `:39-41`).

**Correction.**
- Append a clause: every item of the routed inventory gets one disposition (predicate / control / declined / implemented-unmeasured). Unrouted predicates are labeled author-added.
- Report the result as 9 routed repairs, 1 author-added (K2), 1 control (K4), plus the named unmeasured or declined items.
- Re-label knowledge row 21 as "implemented, unmeasured (not repaired under QUALITY48)".

### D6 (low; impacts calibration). The K4 example depends on which detector is chosen

The closure note says the all-vs-any mutant "survives the ten-case ruler (single-token fixtures) but is killed by selftest all-of-tokens". It routes "multi-token stdout fixture in the ruler" (MANIFEST rounds[421]). QUALITY48 calls it "a gap already caught at the base". That holds for the selftest detector, but not for the detector the routing named. Because 48 lets the author pick the detector, a routed gap can be reclassified as a control.

**Correction.** The predicate's detector should be the one named by the routing. Otherwise, state the reclassification explicitly.

### D7 (low; impacts grounding)

- **The Captured-by link is verified but weak.** `original-outcomes2.json` gives seats 64, completed 30, dead 34. All 20 reviewers are dead (dead by role: reviewer 20, connector 10, revenger 2, scout 2). However, the failure that QUALITY48 captures is "routed yet unexecuted (seat inference)" (`fresh-adjudication.json:48-105`, deferral_reason). The reviewer deaths are context for "no fresh falsifier", not the mistake itself.
- **One pointer lacks a path.** The lesson pointer "Closure rounds[421]" points into the fleet-owned `/home/vgpnk/Projects/shokunin/MANIFEST.json` without a path or revision (QUALITY34).

## Consistency with QUALITY46/47: no contradiction found

- **47's argv rule.** 47 says argv discrimination must cite a real substituted-command pair. K1 and K2 kill mutants with synthetic fixture pairs (`extra-cases.json` `argv-swapped-between-names`, `argv-case-only`). Round23 Erratum A already accepts "the synthetic cases" alongside the source-read pair (`lessons/round-23.md:148-150`). Consistent, provided K1/K2 are not cited as replay-level argv discrimination.
- **46/47 falsifier rows survive supersession.** `command-binding-source-read-red-pinned` still expects exit 1 `["ARGV_MISMATCH"]`, now plus the exact `bundle_sha256` (`tools/registry.json`). QUALITY47's retained-pair falsifier remains executable.
- **47's live/external separation** is operationalized by K10 and `replay/live-dependent.json`. The knowledge Bounds keep "not write isolation" (`:35-37`).
- **Producer authentication.** 46's "pins declarations, not producer authenticity" is not restated in 48, but the lesson Reject list covers it (`lessons/round-24.md:26`) and so does the knowledge entry (`:32-34`).
- **The round24 replay still copies argv from the row** (`registry-replay.py:172-173`). So, as 47 says of round23, its 0/[] binding verdict (`replay-gate.json`) tests only exit and stdout. The knowledge Bounds state this (`:30-31`).

## Verified as stated

- `before.json` gives 1/11, exit 1. Only K4 is discriminated, with `CASE all-of-tokens FAIL`. K1–K3 survive 38/38, K5–K6 hold after substitution, and K7–K11 are tool-absent.
- `sha256sum measure.py` = `0a7f6daa…7daa64`, which equals `before.json` `instrument_sha256`. The ruler was frozen in e338f1b before the implementation commit d2eaecd (`git log`).
- `fresh-adjudication.json` is unchanged from 6a1821a to c8c5b88. Its line 66 quote matches lesson S085.

## Commands run (read-only)

- `GIT_OPTIONAL_LOCKS=0 git log/diff --stat/--numstat/rev-parse/status`
- `sha256sum`
- Inline Python JSON reads of `original-outcomes2.json`, `tools/registry.json` and fleet `MANIFEST.json` rounds[421]

No selftests, gates or battery were run, and nothing was written except this report. No tools were installed or updated.
