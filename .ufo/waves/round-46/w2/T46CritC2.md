seat: T46CritC2

item: attacked C2 (operability) as declared in `.ufo/evidence/round-46/contract.json` — the before cell, the after cell at CONTENT, the axis name, the `floor(10*killed/25)` score rule, the do-nothing controls, and universal wording.

Scratch: `/tmp/tameshi-r46-T46CritC2/` (created). Lane checkout read-only; the only file I wrote is this report. No tool installed (nothing needed).

# What I ran (all runs are observations, not verdicts; the deciding run is the L1's)

| # | command | output |
|---|---|---|
| R1 | `python3 .ufo/evidence/round-46/hardening/mutate.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --targets hardened` | exit 0; `C2_R46: self_pin=1 targets=hardened declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C2_R46_PASS=true` |
| R2 | same driver `--rev 745a583181648cfc7f9c1b476cd1be7dc68f7433 --targets orig` | exit 1; `C2_R46: self_pin=1 targets=orig declared=25 killed=0 survived=25 inapplicable=0 neutral_killed=0 pristine=1 equivalence=-1 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C2_R46_PASS=false`; `diff` against the committed `before/c2-at-freeze.stdout` is empty → the before receipt reproduces byte-for-byte |
| R3 | same driver `--rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --targets orig` | exit 1; `killed=0 survived=25 … C2_R46_PASS=false` — the round-45 counters are still at the before state at CONTENT |
| R4 | `python3 .ufo/evidence/round-46/hardening/mutate.py --selftest` | exit 0; `C2_R46_SELFTEST: cases=8 failed=0` / `VERDICT: PASS` |
| R5 | `.ufo/evidence/round-46/hardening/freshness-counter.py --lane LANE --rev ea25e0224fc81060414b27301c27bd1344669165` (and the coverage twin) | `C1_R45: self_pin=0 … C1_R45_PASS=false` / `C2_R45: self_pin=0 … C2_R45_PASS=false` |
| R6 | `git show ea25e0…:.ufo/evidence/round-45/freshness/measure.py` run with the same args (and coverage twin) | `C1_R45: self_pin=1 … C1_R45_PASS=true` / `C2_R45: self_pin=1 … C2_R45_PASS=true` |
| R7 | R5/R6 repeated at base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d` | originals `self_pin=1 … PASS=true`; hardened copies `self_pin=0 … PASS=false` (both groups) |
| R8 | AST-pin do-nothing control `/tmp/tameshi-r46-T46CritC2/astpin_control.py` (reuses the driver's own `run_selftest`, `judge`, `equivalence` over all 31 manifest mutants) | `PRISTINE freshness pass`, `EQUIVALENCE freshness 1`, same for coverage; `ASTPIN_CONTROL: killed=25 survived=0 neutral_killed=0 neutral_survived=6 inapplicable=0` |
| R9 | `/tmp/tameshi-r46-T46CritC2/eqmask.py` — hardened copy with `'true' if passed else 'false'` forced to `'false'`, passed to the driver's `equivalence()` | `freshness equivalence_with_flipped_PASS=1`, `coverage equivalence_with_flipped_PASS=1`; the two last lines differ only in the masked tokens and `masked_equal=True` |
| R10 | F02 applied to the hardened freshness counter, `--selftest`; C07 applied to the hardened coverage counter, `--selftest` | `FAIL F02_quote_upper_bound_25 got=('verified', 'ok') want=('invalid', 'quote length 26')` / `FAIL C07_rows_one_fails … want=('rows=1', 'C2_R45_PASS=false')` — the kills come from named rule cases |
| R11 | `git diff a6892b196f923efbed242ce9ea599a3f745b2138 6f2168e0… -- .ufo/evidence/round-46/hardening/` | empty → the hardened counters are the bytes the after cell was read from |

# Findings

## F1 — HIGH — the frozen `equivalence` guard is vacuous: it masks exactly the field on which the hardened copy and the original disagree

Attacks: C2's target token `equivalence=1` and the sentence "print the same fields as the round-45 counters (self_pin and the PASS token masked) when run over the round-45 data revision".

R5 vs R6: at the round-45 data revision `ea25e0…` the original prints `self_pin=1 … C1_R45_PASS=true`; the hardened copy prints `self_pin=0 … C1_R45_PASS=false`. `mask()` (mutate.py:87-92) drops every token starting `self_pin=` and every token containing `_PASS=`, i.e. both differing tokens, so the masked lines are equal and `equivalence()` returns 1 (R1 prints `EQUIVALENCE freshness 1`, `EQUIVALENCE coverage 1`). R7 shows the same at base `683eedde`.

Consequences:
- `equivalence=1` is not evidence that the hardening preserved the measurement. The hardened copy **fails its own predicate** (`C1_R45_PASS=false`, `C2_R45_PASS=false`) at every revision before round 46, while the original passes. The check cannot fail on a verdict regression — R9 flips the hardened copy's PASS token to `false` and `equivalence()` still returns 1.
- The copies therefore cannot be substituted into the lane's frozen no-harm monitors (`no-harm.sh` runs `--rev "$REV"` at base and at the deciding rev): doing so turns `NOHARM r45-freshness` and `NOHARM r45-coverage` RED, because those monitors require `C1_R45_PASS=true` / `C2_R45_PASS=true`. So the credited artifact is not adoptable as the lane's counter without breaking a frozen monitor.

Cause: the hardened copy's `SELF_PATH` (`.ufo/evidence/round-46/hardening/freshness-counter.py`) does not exist at `ea25e0…` or `683eedde`, so its self-pin is 0 by construction.

Smallest safe correction: mask `self_pin=` only; give the hardened counter a pin-free verdict field (or a `--pin-rev` so it pins against the round-45 path's blob when its own path is absent) and require that field to equal the original's PASS token. With that, `equivalence` becomes able to fail, and the hardened copies become drop-in for the no-harm monitors.

Severity rationale: the frozen predicate as written is satisfied (the mask is declared in the contract), so this does **not** falsify C2. It falsifies the *value* of the `equivalence=1` cell.

## F2 — HIGH — the frozen target is reachable by a do-nothing control the declared controls do not cover

Attacks: "is the claim sized so a do-nothing control cannot reach it (CTL_E/F/G)?" (prompt §9, phase-4 closure rule).

R8: I replaced each hardened counter's `selftest()` with an **AST pin** — `sha256(ast.dump(ast.parse(source)))` compared against a literal, with the pin literal normalised to avoid circularity — and wrote **no rule assertion at all**. Result over the driver's own functions: `pristine=pass`, `killed=25 survived=0`, `neutral_killed=0 neutral_survived=6`, `equivalence=1` for both groups. That is exactly the frozen target line (`killed>=23, neutral_killed=0, pristine=1, equivalence=1`). It passes because the six declared neutrals are all AST-identical (`13`→`0xD`, trailing comments, an appended comment) and every mutant changes the AST.

The declared controls do not cover this: `CTL_E` pins *byte length* only (`controls-at-freeze.stdout`: `killed=21 survived=4 neutral_killed=6` — length-preserving mutants survive, neutrals die), `CTL_F` is always-fail (`pristine=0`), `CTL_G` is the unchanged original (`killed=0`). None of them normalises source identity.

The delivered artifacts are honest: neither hardened counter imports `ast` and their kills come from named rule cases (R10). So this is a **target-sizing defect, not a false claim**: `killed=25` proves the selftests detect these 25 edits, not that the selftest is a rule test. Smallest safe correction for a successor claim: add the AST-pin (or any source-normalisation) control to the frozen control set, and count a mutant as killed only when a *named rule case* fails (the selftests already print `FAIL <case>`; the driver could require one).

## F3 — HIGH as an argument, LOW as a defect (disclosed) — the 0→10 score is a definitional jump on a set the test authors were given

Attacks: `score_rule` `floor(10*killed/25)` and the round-45 freshness precedent.

- The rule yields the scale ceiling at the target: `floor(10*25/25) = 10`, above the lane's saturation line 8, in the axis's first scored round. The contract states "`>=9` at the target" and the SCORECARD writes 10 (`SCORECARD.md:2212`) — both are arithmetically right, but a first score of 10 means the axis has no headroom and no history.
- The precedent invoked is weaker here. Round 45: `floor(10*71/73) = 9` over a *live* population of 73 registry rows with 2 disputed by a non-author re-fetch (`corpus/lessons/round-45-verifier-spotcheck.md:37,87`, which calls it "a definitional change" and relies on the count). Round 46: `25/25` over a set **published to the authors before the tests were written** — `contract.json` `frozen_before` commits the manifest at the freeze, the hardened counters land later at `a6892b1`, and the wave-1 seat items name the ids outright (`w1/HardPopulation.md:3`: "kill the three declared survivors F04 … F14 … F15"). The case names mirror the mutant ids (`F06_review_non_author` … `F13_verdict_only_agree`, `C01_github_not_googletest`, `C07_rows_one_fails`).
- The lane's own bar for mutant-kill claims is a sealed held-out set (rounds 32/33: `heldout_after_freeze=1`, `ho_kill=8/8`). C2 has none, and the L1's own wave-2 spec now dispatches generalization attacks on both counters (`spec-w2.json` items "Generalization attack on the hardened … counter"), i.e. the closed set is known to be insufficient.

Disclosure: `SCORECARD.md:2212` and `corpus/lessons/round-46.md` (Mistakes, "a score defined this round jumps from 0 to a high value") both name it and point at the count `killed 0 → 25 of 25`. So the honesty requirement is met; what does not hold is the claim that a 0→10 on this axis is comparable to depth/freshness units. Honest reading: operability credit should be the count plus a capability row, with the score labelled definitional (as the round-45 spot-check forced), not a 10.

## F4 — HIGH as an argument, no contract violation — the lane's operative counters are untouched; the credit lands on copies

Attacks: the axis credit ("operability … improved (measured)").

- R3: at CONTENT the round-45 counters still print `killed=0 survived=25` against the same manifest. The lane's live instruments therefore have exactly the before state the claim starts from.
- Nothing in the lane runs the hardened copies except the driver, the assembler, the control builder and the SCORECARD text (`grep -rn "hardening/freshness-counter\|hardening/coverage-counter"` over the lane: `mutate.py:34-35`, `assemble.py:23,30`, `control/run-controls.py:126-127`, the two counters' own `SELF_PATH`, plus wave reports). `no-harm.sh` still runs `.ufo/evidence/round-45/{freshness,coverage}/measure.py`, and the standing freshness row still names the round-45 path (`SCORECARD.md:2200`).
- F1 shows the copies cannot simply be wired in: they print `PASS=false` at base, so substituting them makes two frozen monitors RED.

So the claim's surface ("the selftests of the two round-45 claim counters") was met by writing *new* selftests in *copies*; the runnable artifact the lane actually operates is unchanged. Two divergent copies of one counter, one strictly stronger on tests and strictly weaker on pinning, is a duplicate-authority hazard, not an operability raise of the lane's instrument.

## F5 — INFO — the axis name holds by AXES.md, but only if the copy is treated as the lane's artifact

`AXES.md` defines operability as "Runnable artifacts: checklists that are executable, commands that exist, scripts that run … A checklist item can be run and produces the stated outcome". A selftest that fails when a rule is broken is an executable-outcome property, so operability is the right *kind* of axis for a selftest change; depth would be wrong (no new technical detail enters the knowledge) and calibration would collide with C1's axis (the distinctness rule). Prompt §9's test ("name the axis by the surface the round changes") is met only in the copy sense — which is exactly F4's defect.

## F6 — INFO — "25 declared survivors" is 23 survivor sites, expanded to 25 mutants

`grep -c SURVIVED` on the round-45 audits: `MutC1Counter.md` 12, `MutC1Reviews.md` 9, `MutC2Counter.md` 8. Six of `MutC1Reviews`' nine repeat `MutC1Counter` sites (1,3,5,7,11,13) and three are new (6,9,10), so distinct freshness sites = 15; coverage = 8; total **23**. The manifest's 25 come from splitting one coverage audit row (M13, `rows>=2/entries>=2/indexed==entries`, `MutC2Counter.md:29`) into `C07`/`C08`/`C09`. Contract and SCORECARD say "25 declared survivors"; "25 declared mutants (23 survivor sites)" would be exact. Harmless at 25/25 (`floor(10*23/25) = 9` would still clear the target), but the label should not overstate the audit's yield.

## F7 — INFO — universal words: none found

The statement's bounds are all explicit and finite: "at least 23 of the 25 declared survivors", "none of the 6 declared neutral mutants", "the two round-45 claim counters". No "all/every/complete/no harm anywhere". The only open-ended phrase is "print the same fields", which is bounded by the declared mask — and that mask is F1.

# The strongest argument that C2 is not an improvement, and whether it holds

**The argument.** C2 measures a copy while the lane's instrument stands still, and the copy is not adoptable: at the content revision the round-45 counters still kill 0/25 (R3); the credited copies fail their own verdict at base and at the round-45 data revision (R7, R5) so they cannot replace those counters without reddening frozen monitors; the frozen `equivalence` guard masks precisely the verdict token that distinguishes them (R1, R9); the target is reachable with no rule assertion at all (R8); and the 0→10 is a rule written in the round it scores, over a set the test authors were handed before writing the tests, landing above the saturation line (F3). Under AXES.md's "a trade anywhere is not an improvement", a stronger selftest bought with a counter that no longer passes at older revisions is a trade, not a move.

**Does it hold?**
- As a **falsification**: no. The frozen predicate is satisfied as written — `C2_R46_PASS=true`, exit 0 (R1), `killed=25/25`, `neutral_killed=0`, `pristine=1`, `inapplicable=0` (no mutant silently dropped), and the before receipt reproduces byte-for-byte (R2). Every clause of the statement is true of the delivered bytes.
- As a **critique of the credit**: yes, leg by leg. F4 (operative artifact unchanged) and F1 (the copies are not adoptable and the guard hides it) are reproduced facts, not readings; F2 (a do-nothing control reaches the target) is reproduced with the driver's own functions; F3 is disclosed but the precedent it invokes does not carry a ceiling score.
- **Honest verdict I would put on the row**: `improved (demonstration, measured)` — count `killed 0 → 25 of 25` and the capability row "declared-mutant driver with neutral controls" — with operability credited at the count, not at 10, until the hardened copies are the lane's counters (F4) and a held-out set exists (F3). The claim's own kill rule and the freeze forbid editing the predicate now; this routes to round 47.

# Smallest safe corrections (for round 47, not for this frozen round)

1. `mutate.py::mask` → drop `self_pin=` only; add a pin-free verdict token to both hardened counters (or `--pin-rev`), so `equivalence` can fail on a verdict regression (F1).
2. Add the AST-pin / source-normalisation control to the frozen control set, and require a named rule case to fail before a mutant counts as killed (F2).
3. Point `no-harm.sh` and the standing freshness/coverage counting rules at the hardened copies once (1) makes them pass at base, then retire the round-45 copies (F4).
4. Author a sealed held-out mutant set after the freeze (the round-32/33 pattern) and score against it (F3).
5. Add an operability row to the standing axes table so C1's 22 statements re-derive it; today the 10 lives only in prose (`SCORECARD.md:2212`) and is outside C1's frozen statement list (F5, INFO).

# Unrun / limits

- The L1's deciding run has not been executed at CONTENT: `.ufo/evidence/round-46/after/` is empty (0 files, `ls -la` at 18:59), so the SCORECARD after cells cite receipts that do not exist yet. My R1 reproduces the target line independently; it is not a verdict.
- I did not run `no-harm.sh` (another seat's item) and did not re-run C1/C3.
- F2's control is a demonstration against the driver's functions, not a committed control receipt; the script is in scratch only.
