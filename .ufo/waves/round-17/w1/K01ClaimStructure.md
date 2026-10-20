# K01ClaimStructure — critic, tameshi r17 wave 1

Attack target: the declared claims C1 (calibration) and C2 (operability), checked against
`/home/vgpnk/Projects/shokunin/AXES.md:25-38` (1–3 claims, distinct axes, causally separable,
lowest axis, no axis harmed) and the round prompt `.ufo/prompts/tameshi-round-17.md` §2 (:9-40) and
§2b (:42-78). Read-only. All lane bytes were read at `98bea7da5801f4bc58e4187690ee1687c8a5061f`
with `git show 98bea7d:<path>`, together with the live wave-1 specs and evidence under
`.ufo/waves/round-17/` and `.ufo/evidence/round-17/`. I executed no lane gate. I installed no tools.

## Summary

| # | Objection | Verdict | Axes |
|---|---|---|---|
| O1 | Count, distinct axes, lowest axis | **holds** (with one caveat: operability has no score) | calibration, operability |
| O2 | Is C1 verifiable without C2? | **falls as drafted** (fixable) | calibration |
| O3 | Is C2 verifiable without C1? | **falls as drafted** (fixable) | operability |
| O4 | Can C2's metric see the harm it repairs? | **falls** (fixable) | operability, calibration |
| O5 | Is a repair of a harm an improvement? | **holds conditionally** | operability (quality trend) |
| O6 | jj fixes ride inside C2 without being measured | **partial**: unmeasured scope plus a harm risk | operability, depth |
| O7 | Which claim is sourced? | **C1 only**, and no S### is cited yet | — |
| O8 | Box 3 is a whole-page property, so a C2 failure also fails C1 | **tradeoff**: disclose it, do not fix it | calibration |

Overall: the claim *selection* holds. As currently drafted, the two claims are coupled in both
directions, and C2's counting rule cannot tell a repair apart from re-registering a broken command.

---

## O1 — count, distinct axes, lowest axis: holds

- There are two claims on two axes: calibration and operability. That satisfies AXES:27-33.
- Lowest owned axis:
  - SCORECARD@98bea7d scores only depth and calibration (`SCORECARD.md:66-67`, round-16 row `:585-586`).
  - The closure (`corpus/lessons/round-16-verifier-spotcheck.md:127-128`) leaves depth at 7 and calibration at 6.
  - So C1 works the lowest axis, calibration 6. If the r16 rejection also reverts depth to 6, the two tie and C1 still satisfies the rule.
- The trend furthest behind is quality, which r16 harmed (spotcheck:201). C2's axis, operability, sits in quality (AXES:21-23), so the choice is consistent.
- **Caveat.** Operability is unscored in this lane: the "Current axes" table has no row for it. AXES:28-29 and §SCORECARD contract (:79) want a before→after recorded as a score. Lane precedent records unscored verdicts (`SCORECARD.md:385,442,537`).
- **Fix.** Pre-register C2's unit before measuring, for example "pre-existing registered rows held K/M; operability unscored in this lane". Never convert it to a 0–10 score afterwards.

## O2 — C1 is not verifiable without C2 as drafted: falls

**Counterexample A: the recipe text.**
- R08's assignment (`spec1.json`, item R08R14RecipeRepair) drafts SKILL.md:1579-1586 (the round-14 recipe) to point at `.ufo/evidence/round-17/dispositions-before.json` (→ 1) and `dispositions.json` (→ 0) from the lane root.
- Those outcomes exist only if C2's v2 manifests (X02) and the staged v2 `tools/evidence-disposition.py` (X01) land.
- Remove C2 and the repaired bucket states wrong expectations, so it fails. Under the measure's credit rule that is `wrong_expectations>0` (round-16 `measure.py:181-196`, `FAIL_VERDICTS` :65), so `box3_full_page` is false (:265) and the restraint score stays 6 (:287-288).

**Counterexample B: the traced inputs.** This is mechanical and does not depend on wording.
- X10's red-before traces of recipe steps 2–3 open these lane files: `tools/evidence-disposition.py`, `tools/mutate-and-run.sh` and `tools/pin-disposition.py`, plus `tools/bash-witness-study.py`, `tools/witness-metadata.py` and the round-12/13 evidence.
  - Command: `grep -oE 'open(at)?\([^"]*"[^"]+"' .ufo/evidence/round-17/redbefore/logs/e69b488-before.strace …`
- Those first three files are exactly the files C2 rewrites: v2 disposition (X01), the runner repo-identity guard (X05) and pin-disposition branch-tip resolution (X06).
- Under contract C, a bucket that executed commands credits at REV only if every traced input's blob at REV equals the recorded sha.
- So a re-read taken at the joint rev credits there and nowhere C2's bytes are absent, and the reverse also holds. **C1's after-number is fixed by C2's final bytes.**
- Also, X02 puts every `tools/` pin of `.ufo/evidence/round-13/expected.json` under `historical_inputs`; those pins are listed at 98bea7d. Those reads then go through `git cat-file` into `.git/`, which trace-inputs excludes. **C2's implementation therefore changes what C1's input key can see.**

**Smallest safe correction.**
1. The round-14 bucket states only the C2-independent working invocation, with its outcomes:
   - `--root` on an extracted `git archive 28aeef4` → 1, then 0.
   - The spotcheck (§3, :143) and the SKILL.md:1681 annotation already name this form, and R08 executes it.
   - Any mention of the round-17 live form is a bare pointer to C2's own section, with no stated exit.
2. Install the staged C2 tool bytes in a commit *before* any wave-2 traced re-read. Record that commit as the rev every C1 trace ran against.
3. Add a separability table to the report: every SKILL bucket whose traced inputs include a C2-edited file (expect at least the round-14 recipe, the runner sections and the pin-disposition sections), plus the statement that C1 is measured at the joint rev with C2 bytes frozen.

Without this table the judge cannot see that C1's 8 is conditional on C2's bytes.

## O3 — C2 is not verifiable without C1 as drafted: falls

**Counterexample.**
- X04 (`spec1.json`, X04RegistryRows) registers `active` rows, expecting 0, for:
  - `python3 .ufo/evidence/round-17/measure.py --selftest`
  - `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest`
  - `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest`
- All three are C1 instruments. Without C1 the files are absent, the rows return non-0, and `registry-check.py` exits 1. **C2's after count fails if C1 has not landed.**
- These rows also inflate C2's delta. At 98bea7d they fail only because the files do not exist, not because of any harm. The same applies to the two round-17 manifest rows and to `registry-check.py --selftest` itself.
- So `--rev 98bea7d --registry <after>` will show about six "differs → held" flips. Only one of them, the round-14 gate, is the repair.

**Smallest safe correction.**
- Define C2's claimed before→after over the **row set registered at 98bea7d**: the SKILL registry tables for rounds 12, 13, 15 and 16, plus `SCORECARD.md:236-246` Capabilities.
- Grade it with one registry file at both revs.
- Report new round-17 rows separately as "held at after", outside N/M. Tag each row with its owning claim (for example `"claim": "C1"`), or keep C1's selftest rows in a second registry.

## O4 — C2's metric cannot see the r16 harm: falls

**Counterexample: anchoring of the expected outcome.**
- At 98bea7d, the active round-15 registry row for this gate (`SKILL.md:1681`) already states that `--root .` "returns 2 `expected_input_digest_mismatch` by design".
- X04 is told to "use the registered verdict maps for `expect`", and X13 to run "the round-15 disposition row as written". Read as written, the registered outcome for that row at 98bea7d is 2, and the observed result is 2. **The before measurement scores it *held*.**
- So a monitor that grades against current registry text would have **passed round 16's harm**. The harm was exactly a registry edit that annotated the breakage instead of fixing it (spotcheck:113-114, 148-150).
- The outcome in force when the capability entered was clean 0:
  - `SCORECARD.md:246` ("before FAIL1 → after CLEAN0")
  - `SCORECARD.md:413` ("after exit0")
  - `SKILL.md:1601` (round-14 row, no annotation)

**Counterexample: identity change.**
- At after, the registered *command* changes from `…/round-14/dispositions.json` to `…/round-17/dispositions.json`.
- The round-14 manifest is v1 and immutable, and contract A keeps v1 behaviour byte-identical. So the old command still exits 2 at after. [INFERENCE from contract A; the v2 tool was not yet staged, so I could not run it.]
- Observed at 98bea7d: `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt` shows `exit=2`, `expected_input_digest_mismatch`, `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`.
- "Held" at after is therefore reached by **re-registering**, not by the old entry returning its outcome. Silently swapping the row is the closure's own legitimate repair option ("appended superseding pin or disposition", spotcheck:217-220) only if the swap is visible.

**Smallest safe correction.**
1. Each registry row carries `expect` anchored to the outcome at admission, plus the rev or line it came from (for this row: 0, from SCORECARD:246 / SKILL:1601). A later outcome change is never taken from annotation text.
2. Keep the old row with `"status": "superseded", "superseded_by": "<new row>"`. `registry-check` lists it and runs it as information, so the denominator change is visible and it never drops out silently.
3. Prove MON1 is a harm detector with a red-before:
   - `registry-check.py --rev 98bea7d --registry <anchored pre-existing rows>` must exit **1** on the round-14 gate row. If it reports held, the monitor does not catch the r16 class.
   - The after run must exit 0 with the supersession declared.

## O5 — is a repair of a harm an improvement? Holds conditionally

**Why it holds.**
- Admission is per round, measured from that round's before: AXES:28-30, 34-36; MISSION.md:47-48.
- At 98bea7d the round-14 entry command fails its stated outcome. LEARNING.md:34 defines quality `improved` as "stale entries re-verify, with no admitted entry failing its re-check".
- PROTOCOL.md:243-248 makes this repair an owed routed defect, and the closure marks it "blocking for re-admission" (spotcheck:216).
- So restoring a clean live-tree verdict is a genuine improvement against r17's baseline.

**Conditions.**
- **(a) Label it a restoration.** Over r16+r17 the gate returns to its pre-r16 state, so on that row the net is zero. Only MON1 (an in-round entry-command monitor) and the v2 `historical_inputs` mechanism (which prevents recurrence for lane-instrument pins) are new beyond restoration. The report should say so, and C2's "improved" should rest on the O4 red-before.
- **(b) No double credit.** One root cause, the runner moving under a pinned gate, is repaired from two sides: C1 corrects the recipe bucket and C2 restores the gate row.
  - It must flip each measurement through a *different* cause. C1 flips through the corrected text and re-read against the archived invocation (O2 fix). C2 flips through the v2 manifest.
  - If the recipe states the v2 outcomes, both flips have one cause and the claims are not causally separable (AXES:30-31).
- **(c) No re-entry of the capability row.** "Effective expectation reconciliation" was acquired in round 14 as a *calibration* capability (`SCORECARD.md:413`). Re-entering it, or crediting its return to calibration as well, would pre-claim.
- **(d) Restoration does not excuse new harm.** See O6.

## O6 — jj fixes ride inside C2 unmeasured: partial

**Unmeasured scope.**
- X05 (runner repo-identity guard) and X06 (pin-disposition branch-tip) change two tools whose registered selftests expect 0 both before and after. They contribute **0** to C2's count and have no before→after of their own.
- **Fix:** give each one a red-before fixture that fails at 98bea7d and passes after, and register it (X11 JjHeadFixture is the natural carrier). Otherwise report them as non-claim maintenance.

**Harm risk.**
- X05 edits `tools/mutate-and-run.sh`, the file whose r16 edit caused the harm. Command D reads its header for depth (`SCORECARD.md:73`).
- X06 changes the meaning of "committed-HEAD" in the six-leg content-disposition capability (`SCORECARD.md:245`, `pin-disposition.py:42,64-65,315-318`). That is an identity change in a capability's stated output.
- It also moves `tools/pin-disposition.py` off its round-13 pin `29725397…`, which currently matches. Under v1 that creates a second `expected_input_digest_mismatch`, rescued only by v2 `historical_inputs`.
- **Required no-harm receipts at the after rev:**
  - command D → `recorded_cases=7`
  - `--regression` → 7/7 PASS
  - runner and pin-disposition selftests green
  - X12's pin map showing no live-verified pin of either file outside v2 `historical_inputs`
  - an appended note on the capability row recording the HEAD→branch-tip semantics

## O7 — which claim is sourced: C1

- SOURCES ends at S057 at 98bea7d: `git show 98bea7d:corpus/SOURCES.md | grep -oE '^\| S[0-9]+' | tail -1`.
- Source rows opened this round:

  | Wave-1 scout | Source | Supports |
  |---|---|---|
  | S14 | Build Systems à la Carte, verifying traces | contract C itself: record the hashes of the dependencies a run actually read; invalidate on any difference |
  | S15 | Bazel action cache | contract C |
  | S16 | strace | contract C (the tracing method) |
  | S19 | Bazel hermeticity | the limit: undeclared inputs |
  | S17 | jj colocation | only the unmeasured X06 fix (O6) |
  | S18 | `rev-parse --show-toplevel` | the contract-A identity guard, a mechanism C2 does not count |

- **C1 is therefore the cleanly sourceable claim.** C2 counts as sourced only if its evidence cites S18 for the v2 identity guard and that guard is shown able to fail (`historical_input_unavailable` on mismatch).
- Currently neither claim cites any S###: W02's knowledge draft leaves `S0xx` markers.
- **Fix:** mint the rows only after the scout opens them, with `## Gate` URL, date and a ≤25-word quote (§2b.1). Cite the minted ids in `corpus/knowledge/input-keyed-coldread-credit.md` and in C1's SCORECARD evidence cell (§2b.4).

## O8 — box 3 makes C1 inherit C2's failures: tradeoff

- `box3_full_page` requires every bucket to be credited (round-16 measure.py:19-29, 265).
- W03 drafts **one** combined section, `## Live-tree re-pin, entry-command monitor and input-keyed cold-read — round 17`, documenting both claims' tools. If C2's commands fail to produce their stated outcomes in wave 2, that bucket fails and C1 falls at the joint rev.
- This is correct behaviour for a whole-page assertion, not a defect, but the judge must see it.
- **Smallest correction:**
  - Split W03 into two headings, one per claim, so a failure is attributed to one bucket.
  - If C2 falls, revert or mark its section rather than let box 3 overclaim.
  - State in the report that the C1 verdict covers C2-authored text.

## Evidence commands (all read-only, exit 0)

- `git -C …/tameshi-shokunin show 98bea7d:SCORECARD.md` (lines 66-67, 73, 236-246, 413, 553-594)
- `git show 98bea7d:SKILL.md | sed -n '1563,1603p;1676,1686p'`
- `git show 98bea7d:.ufo/evidence/round-13/expected.json`: 13 inputs, including `tools/{pin-disposition.py 29725397…, mutate-and-run.sh 75ed934d…, witness-metadata.py, bash-witness-study.py}`
- `git show 98bea7d:tools/<f> | sha256sum`: runner `0673d2e5…`, which differs from its pin; pin-disposition `29725397…`, which matches its pin
- `git show 98bea7d:.ufo/evidence/round-16/measure.py | grep -n box3_full_page…`
- The X10 strace logs under `.ufo/evidence/round-17/redbefore/logs/`: the opens listed in O2 B, with exits e69b488 1/0 and 09ee1d0 2/2
- `.ufo/waves/round-17/spec1.json` item targets for X02, X04, X10, X12, X13, R06, R08, W02, W03 and S14-S19

Verdict: **partial.** C1/C2 selection holds (O1, O5). Separability and C2's metric fall as drafted (O2, O3, O4). Each is fixable with the corrections above before wave-2 measurement.
