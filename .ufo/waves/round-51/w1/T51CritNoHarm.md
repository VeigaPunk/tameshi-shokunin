# T51CritNoHarm — attack on round-51 no-harm.sh and deciding-run.sh

Seat: T51CritNoHarm (critic, no-harm/deciding). All runs below were executed read-only against base
`9962033fd7a75aa2f2847e979dd687a5d28505a1` or in scratch clones (`/fast/scratch/hyaku/tameshi-r51/T51CritNoHarm/`),
never in the lane. No tools installed (Python 3 + git only; no RULES.md install needed).

Evidence commands (all observed, verbatim):
- Baseline at base: `bash no-harm.sh <lane> 9962033…` → 11/11 ok (commandD=9, coldread 8/64, r45 pop=73 fresh=71 score=9, S160=1, registry=131, r46/r47 ok, scope [] ok, PBT string, shrinker failed=0).
- Fixture F1 (SOURCES-only: S022 `queued`→`mined`, + S272/S273 mined rows, id>160): `bash no-harm.sh <lane> F1` → all ok; r45 pop=74 fresh=71 score=9; registry=133; coldread 64/64 score=8; `coldread-precheck floor=base cand=F1` → lost=0 ok.
- Fixture F2 (runner tenth-leg header appended): coldread 44/64 (score 6); no-harm coldread-floor RED; `coldread-precheck` → 20 LOST, `drifted=tools/mutate-and-run.sh` (plus stale-entry paths from unrelated old ledger entries).
- deciding-run.sh gate tests in scratch clone `git clone --shared` at 9d023ae (script bytes at 9d023ae): see F6–F10.

## Findings

**F1. Re-base 1 (`commandD >= 9`) is justified; no harm hidden.** no-harm.sh:18 counts header ledger lines only
(`^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+`), identical to round-18 LEG_RE (round-18/measure.py:121,667). Base gives
recorded=9/depth=9; adding the tenth leg gives 10 (observed at F2); a drop below 9 still trips RED. The monitor does
not check wiring — an unwired tenth leg would pass no-harm but fail C2 (c2/measure.py `wiring()`), so no silent harm.

**F2. Re-base 2 (r45-freshness: `fresh >= 71 and floor(10*fresh/population) >= 9`, replacing `population == 73`) is
necessary and hides no harm.** Round-45 freshness measure population() counts mined rows with id ≤ S160 and a URL
(round-45/freshness/measure.py:95-97); S022's lawful queued→mined flip grows pop 73→74 (observed), which the old exact
pin would have flagged RED despite score remaining 9. The new pin keeps both guards: fresh=71, score=9 at pop=74
(observed); fresh<71 or pop>78 (10*71//79=8) → RED. Freshness axis still protected.

**F3. Re-base 3 (tools-scope allowlist of five paths) is justified; the four extra tools genuinely pin the runner's
nine-leg panel.** Verified at base: tools/tally-audit.py REF_BLOCK `nlegs=9` (:48), REF_NAMES (:88);
tools/tally-audit-v2.py (:67,:107); tools/tally-audit-v3.py (:102,:142); tools/mte-interop.py LEG_TABLE (:74-76) and
clones the runner (:280,:284). All four are in c3/tools-base.json and carry C3 self-test rows, so a broken update fails
C3 (amendment 2 rationale holds). Scope monitor otherwise closed: any M/A/D under tools/ outside these five goes RED
(no-harm.sh:34-36).

**F4. S022→mined plus new S272/S273 rows change exactly the monitors the re-bases anticipate, nothing else.**
At F1: r45-freshness pop 73→74 (score 9, ok via re-base 2); registry rows 131→133 (ok); S160-count stays 1; r45/r46/r47
coverage untouched; **coldread credited stays 64/64, score 8** — the SOURCES.md byte change drops no credited section
(no current-section ledger entry pins corpus/SOURCES.md at the live sha). So no monitor is harmed by the three rows.

**F5. Runner edit drops exactly 20 credited sections (64→44, score 8→6), confirming the contract's coldread_note;
the coldread-floor monitor therefore forces the re-key before the deciding run.** `coldread-precheck floor=base cand=F2`
names all 20 LOST sections (`drifted=tools/mutate-and-run.sh`). Without the round-49-style re-key, no-harm coldread-floor
goes RED and the deciding run exits 1. This is the designed gate, not a hidden harm.

**F6. deciding-run.sh refusal paths all verified (exit 3, nothing run):** outdir-missing (line 20); head-is-not-rev
(line 21); control-receipt-missing (lines 23-24, observed at base); control-receipt-not-after-freeze (lines 25-26,
observed with FREEZE=HEAD); second-invocation via any `$OUT/<k>.start` (line 28); dirty-tree with any tracked/untracked
change outside OUT (lines 29-30). Ordering note: outdir check precedes head check.

**F7. FROZEN covers every frozen file.** Parsed `FROZEN` (deciding-run.sh:35, 14 entries after `$E` expansion) vs
freeze.json `sha256` (13 entries): 13/13 frozen files present, plus freeze.json itself. No gap.

**F8. FREEZE-selection tension at current history (process finding, not a script defect).** With FREEZE=84aa673 and
REV=9d023ae (HEAD), gate 0 passes but `FROZEN_UNCHANGED=0` fires because the amendments changed contract.json/freeze.json/
no-harm.sh after 84aa673 (observed: `3 files changed, 14 insertions(+), 5 deletions(-)`). With FREEZE=9d023ae, gate 0
refuses (control receipts committed at f0129a5 do not descend from 9d023ae). As of HEAD no single commit satisfies both;
the L1 must move/amend the control-receipt commit after the final freeze (or pick the final freeze accordingly) before the
deciding run.

**F9. Minor: deciding-run.sh's docstring demands an EMPTY OUTDIR; the code only requires existence (`-d`, line 20) and
relies on leftover `cX.start` files for the second-invocation guard.** If OUT is emptied between runs, a second invocation
is not detected. Low severity; the contract's "one invocation" rule then rests on the L1 not clearing OUT.

**F10. Full deciding run in scratch (HEAD=REV=9d023ae, FREEZE=84aa673, clean tree) works end-to-end:** FROZEN_UNCHANGED=0
(as F8), no-harm 11/11 ok, coldread-precheck ok (lost=0), census exit=0, counters ran from REV bytes and printed the
expected pre-claim false verdicts (C1 total=11, C2 recorded=9/new=0, C3 covered=0/30); `DECIDING_RUN_EXIT=1`; receipts
(c*.start/end/exit/stdout, frozen.stdout, no-harm.*, coldread-precheck.*, census.*, clean-tree-before/after.txt) written.

## Summary
- Re-bases 1-3 (commandD>=9; r45 fresh>=71 & score>=9; tools-scope five-path allowlist) are each justified, minimal, and
  verified not to hide harm: the exact pins they replace would RED on the round's own lawful changes (S022 flip; tenth leg;
  leg-panel tool updates).
- S022→mined + S272/S273 affect only r45-freshness (pop 73→74, still score 9) and registry-row count; coldread credit,
  S160-count, r45/r46/r47 coverage are unaffected (measured, F1).
- Runner edit drops exactly 20 credited sections; coldread-floor/precheck correctly force the re-key before deciding.
- deciding-run.sh enforces HEAD==REV, clean tree, single invocation, and control-receipt descent; FROZEN covers 13/13
  freeze.json files plus freeze.json itself.
- One open process tension: no current commit satisfies both gate 0 and FROZEN quietness (F8); L1 must re-commit the
  control receipts after the final freeze.
- Minor: OUT emptiness/`-d` mismatch and second-invocation reliance on leftover start files (F9).
