# RoutingCarry — round 25 W1 (connector)

Seat `TameshiR25.RoutingCarry`. Revision under review `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` (base `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`). The lane HEAD has since moved to `5b69fb2`, which adds only `contract-amendment-1.json` (an `mte-interop.py --fleet-root` change) and the wave spec. That does not change any mapping below. Read-only throughout: no clone, no gate/selftest/sweep run, nothing written except this file. No tools installed or upgraded.

## Verdict

Only routing item 1 is handled this round, and it is handled by C1. C2 handles none of the five items: it is the frontier F1 interop capability. Items 2, 3 and 4 are not handled at `c9ff09f`, and the round report **must** say why each is deferred. Item 5 is not handled either, but it is not lane work: the round report should carry it forward as still open in one line, and does not need a deferral reason.

| # | Routing item (spot-check line) | Round-25 handling at `c9ff09f` | Report must say why? |
|---|---|---|---|
| 1 | Adjudicate the three round-23 closure-routed items, with a retained negative control that can fail; old snapshots immutable (`:63`) | **C1** — R23-ROUTED-1/2/3 in `contract.json:9,15`; counter `c1-measure.py` | n/a (claimed) |
| 2 | Register the ruler's bounded output contract and the replay-bundle row; retain MutPins survivors/inconclusive outcomes instead of counting aggregate process failure as a kill (`:64`) | **Not handled.** C2 and the C1 witness rule are next to this item but do not discharge it (see below) | **Yes** |
| 3 | Mark the stronger `registry-replay.py` docstring promises at the consumer entrypoint; declare input validation, surrogate crash, stale-pair/publication atomicity, hooks/out-of-output writes, unbounded/unredacted streams and live-sibling dependency as separate problems (`:65`) | **Not handled** | **Yes** |
| 4 | Keep live/dependency labels distinct from structured revision binding; fix stale consumer locators and superseded expectations without rewriting receipt bytes (`:66`) | **Not handled** | **Yes** |
| 5 | The round-18 helper-recovery L0 question stays open; this note authorizes nothing (`:67`) | **Not handled — out of lane scope** (fleet/L0) | **No reason needed**, but the report should list it as still open |

## Evidence

**Line anchors.** `git show c9ff09f:corpus/lessons/round-24-verifier-spotcheck.md | cat -n`: line 61 is the routing header ("Route to the next authorized tameshi round, with new claims rather than retroactive edits"), and items 1–5 are on lines 63–67. The file is byte-identical in the working tree (`git diff --quiet c9ff09f -- <file>` → `SAME_AS_WT`).

**What changed base→`c9ff09f`.** `git diff --stat 1f73157 c9ff09f` lists only the eight files under `.ufo/evidence/round-25/`, `tools/mte-interop.py` and the two `tools/vendor/*.tgz`. The same diff limited to `tools/registry.json SKILL.md SCORECARD.md tools/registry-replay.py tools/mutate-and-run.sh corpus` is empty. So nothing that items 2, 3, 4 or 5 point at was touched.

**Item 1 → C1.**
- `contract.json:9` sets `"kind": "repair-first (round-24 verifier spot-check routing item 1)"`. `contract.json:15` names the three items and requires "including negative controls that can fail". The counter's docstring (`c1-measure.py:1-3`) cites spot-check `:37,63`.
- "Negative control that can fail" has a concrete form for each item:
  - R1 and R2: a kill counts only with an explicit `FIXTURE … FAIL` or `CASE … FAIL` witness in the evidence log (`c1-measure.py:60-63,68-69`; `c1-suite.py:12-15`).
  - R3: two doctored copies, one with a row dropped and one with a status flipped, must each fail (`c1-measure.py:106-113`).
- "Old snapshots immutable" holds at `c9ff09f`: no round-24 or earlier evidence file is in the diff.
- State at `c9ff09f`: the item is claimed but not yet satisfied. `dead-falsifier-disposition.json` is absent (`git cat-file -e` → `DISPO_ABSENT`), and `SCORECARD.md` has 0 `R23-ROUTED` rows. This matches the recorded 0/3 in `c1-before.json`.
- "Retained" means the after-measure output, including `negative_controls_fail_as_required`, has to be committed as a receipt. At this revision only the before receipt exists.
- R3 population check (read-only parse): `.ufo/waves/round-23/original-outcomes2.json` has 34 `failed` and 30 `completed` rows. The 34 dead names match the 34 `Re*` seats of this wave exactly, with an empty set difference in both directions.

**C2 → no routing item.** C2's eight legs are the runner's embedded regression tables (`mutate-and-run.sh:613-620`: JS, BASH, TSUKUROI, MADO, CHECKLIST, CLAIMS, ROUNDGATE, SOURCESCHECK), not MutPins. The contract calls C2 a "capability acquisition; frontier F1" (`contract.json:22`).

**Item 2 — open, with two adjacent pieces that must not be credited to it.**
- *Registration:* `tools/registry.json` at `c9ff09f` has 54 rows. None references `.ufo/evidence/round-24/` or a round-24 ruler or replay-bundle row. The only registry-replay row is `registry-replay-selftest`.
- *Adjacency 1, C1 witness rule:* it applies "an aggregate nonzero exit is not a kill" only to C1's own two sweeps (`c1-suite.py:12-15`). It does not touch MutPins.
- *Adjacency 2, C2 INCONCLUSIVE mapping:* C2 maps `INCONCLUSIVE→RuntimeError` (`mte-interop.py:13,58`). That keeps runner-classified inconclusives out of the scored denominator. But the runner still classifies every exit outside {0,124,126,127} as KILLED (`mutate-and-run.sh:538-542`), so aggregate process failure is still counted as a kill.
- *MutPins outcomes:* the outcomes item 2 asks to retain sit in `.ufo/waves/round-24/w1/MutPins.md:73-80`: four "survives direct --only" rows and two "K5/K6 substitution test internally inconclusive" rows. No round-25 artifact references them (`git grep -i mutpins c9ff09f -- .ufo/evidence/round-25 tools/mte-interop.py` → no hits).

**Item 3 — open.** `tools/registry-replay.py` is unchanged base→`c9ff09f`. Its docstring (lines 1-21) still makes the bounded-stream, refuse-on-not-held and live-dependent promises, and it is not marked at any consumer entrypoint. No round-25 file mentions `registry-replay`.
- Adjacent but not handling: `ReOutputComplete` re-attacks the round-23 stream-capture item. That is a dead-falsifier disposition under C1 R3, not the separate declared problem item 3 asks for.

**Item 4 — open.** No round-25 file touches live/dependency labels, revision binding, consumer locators or superseded expectations (`git grep -i -E 'free-text|locator|…' c9ff09f -- .ufo/evidence/round-25 tools/mte-interop.py` → no hits). The `ReReplay*` seats are told the row "may be superseded in tools/registry.json". They may surface stale locators as findings, but that is disposition evidence, not a fix.

**Item 5 — out of scope.** `SCORECARD.md:688`: "Helper-owned live-Git recovery is fleet scope, routed in L0 (fleet `36500aa`)." Spot-check `:67` explicitly authorizes no action. There is nothing to defer, so the report only needs to say it stays open at L0.

## Why "must say why" for items 2–4

The round-24 rejection rested on routed items being left unrecorded: "three closure-routed items remain unrecorded … Do not silently shorten it" (`:34`), and "omitted dispositions" (`:59`). The routing header asks for "new claims rather than retroactive edits" (`:61`). If round 25 claims item 1 and stays silent on items 2–4, it repeats the same failure, one level up.

[INFERENCE] No existing `corpus/QUALITY.md` criterion codifies this rule. Criterion 48 (`QUALITY.md:489-502`) covers when a routed gap counts as repaired, not when a deferral has to be recorded. The obligation therefore comes from the spot-check text, not from a gate.

## Contradiction with a sibling seat

`SpotRouting2`'s target (spec item `SpotRouting2`) says items 2–4 are at `:64-66`, which is correct. Its parenthetical, however, lists them as "ruler output contract registration, MutPins survivors, registry-replay docstring promises". That splits item 2 into two and leaves out item 4 entirely (live/dependency labels, stale locators). If that seat follows its own gloss, item 4 has no deferral evidence from any seat this wave. No wave item names item 5 at all, which is acceptable only because item 5 needs no reason.

## Named gaps (named only, no new work proposed)

- The round report needs one deferral line each for items 2, 3 and 4, plus one carried-open line for item 5.
- Item 4's deferral evidence must not depend on `SpotRouting2` alone.
- C1's after receipt must be committed so that item 1's "retained negative control" is actually retained.

## Commands run (all read-only, `GIT_OPTIONAL_LOCKS=0`)

- `git log --oneline -3 c9ff09f`; `git diff --stat 1f73157 c9ff09f` (11 files, all round-25/C2); `git show --stat 5b69fb2`.
- `git diff --stat 1f73157 c9ff09f -- tools/registry.json SKILL.md SCORECARD.md tools/registry-replay.py tools/mutate-and-run.sh corpus` → empty.
- `git grep -n -i <MutPins|INCONCLUSIVE|registry-replay|locator|helper-recovery|…> c9ff09f -- .ufo/evidence/round-25 tools/mte-interop.py`.
- `git show c9ff09f:tools/registry.json | python3 …` (54 rows; none for round-24 ruler or replay bundle).
- `git cat-file -e c9ff09f:.ufo/evidence/round-25/dead-falsifier-disposition.json` → absent; `git show c9ff09f:SCORECARD.md | grep -c R23-ROUTED` → 0.
- Python parse of `original-outcomes2.json` against `.ufo/waves/round-25/spec.json` → dead 34, re-attack 34, set differences empty.
- Scratch used: `/tmp/routingcarry-r25/` (extracted targets and outcomes copy, both read-only derivatives).
