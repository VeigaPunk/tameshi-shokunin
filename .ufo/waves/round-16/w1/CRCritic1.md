# CRCritic1 — falsifying C2's premise (round 16, wave 1)

Seat: `TameshiR16.CRCritic1` (critic). Read-only. No mutants run. No tools installed or upgraded.
Scratch: none on disk (in-memory Python only). Everything below was observed in this session
unless it is marked **[INFERENCE]**.

## Verdict in one paragraph

C2's premise holds **only in a narrower form**. A lane-dispatched full-page cold-read can earn the
box-3 `[~]` 2 points, which takes calibration to 8, the lane cap. It can never earn the last 2
points or an `[x]`. The planned scoring mechanism has four defects that would let a 6→8 pass
vacuously:

- (a) it accepts `verified-record` on instruction sections. This is the record/instruction loophole.
- (b) an author `--override` can turn a failing verdict into a pass.
- (c) it does not require the SHONEN box-3 line to link the new evidence.
- (d) the shared wave-1 context gave cold-read seats oral context that the page does not contain.

There is also a concrete wrong-expectation already on the page, at SKILL:1472. If any seat marks
that section as passing, the full-page claim fails. Smallest safe correction: fix (a)–(d) in
`measure.py`/`assemble.py` and in wave-2 briefs. Record 6→8 as a **lane-measured candidate pending
non-author closure**, not as a self-pinned score.

## Evidence base (commands, exits, anchors)

| # | Command / read | Exit | Key observation |
|---|---|---|---|
| E1 | `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md SKILL.md` | 0 | both `97cf436b…3623580`, so snapshot = current SKILL.md |
| E2 | Python partition of the snapshot (headings `#{1,3} ` outside ``` fences) | — | 1705 lines, 50 headings + preamble (lines 1–5 frontmatter) = **51 sections**; no `####`, no indented or `~~~` fences (`grep -nE '^\s+```\|^~~~'` → no hits); 18 fence lines; file has **no trailing newline** (`od -c` tail) |
| E3 | `SCORECARD.md:67` | — | rubric: "Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes" |
| E4 | `SCORECARD.md:209-220` | — | box-3 increment "not earned and scores 0 … carried as an unscored mark"; pinned 6 = boxes 1, 2, 4 × 2, "box 3 excluded" |
| E5 | `corpus/lessons/round-1-verifier-spotcheck.md:17` | — | exclusion reason: "cold-read covered Appendix A+B only, probes reconstructed"; "Debts: box 3 needs a fresh reader to run the full page-defined procedure" |
| E6 | `corpus/QUALITY.md:43-46` | — | criterion 13: "an Appendix A/B cold-read cannot earn full-page box-3 score credit" |
| E7 | `SHONEN.md:9-10` | — | box 3 is `[~]`; its only evidence link is `reports/round-1-kaika-coldread.md`; it lists "audit recipe, fail-closed taxonomy, service/cadence/runbook not exercised; lane-dispatched seat" |
| E8 | `.ufo/evidence/round-12/measure.py:29-31,44` | — | `# Fixed adjudication: round-1 outside review excludes box 3`; `scored_boxes = (1, 2, 4)`; `calibration_excluded_boxes: [3]` |
| E9 | `../PROTOCOL.md:62-70` (fleet root) | — | "a subagent the lane dispatched is still the lane … The lane's own assessment is `[~]` asserted (with its evidence pointer); only a non-author `<id>` may write `[x]`"; box 3 = "`SKILL.md`/`corpus/` instructions executable without oral context, self-contained, and with resolvable pointers" |
| E10 | snapshot `:1466-1469` | — | "Tameshi-dispatched reviewers remain part of tameshi for promotion authority (`../PROTOCOL.md:63–68`)" |
| E11 | snapshot `:1472` vs `SHONEN.md:9` | — | page says "**Box 3 remains `[ ]`**"; SHONEN carries `[~]`, so the page contradicts the checklist it describes |
| E12 | `dispatch1.json` `taskCall.context` (Python `'@defect' in ctx`) | — | True. The shared context gives every CR seat "Mutation spec format (tools/mutate-and-run.sh spec v1): `@defect <ID> \| <desc>` / `@old …` / `@new …`, escapes only \n \t \r \\" plus the C1 round-gate details |
| E13 | grep of snapshot for `@defect` | — | **0 hits**. The page has `@old`/`@new` (:840-841, :956-957) and `--defects <spec>` (:834) but never the `@defect` header grammar. The grammar is only in `tools/mutate-and-run.sh:40,208,211` |
| E14 | `dispatch1.json` `registry.members[*].role` + `~/.omp/agent/agents/scout.md:3` | — | scout = "Read-only codebase research". Instruction sections given to non-executor seats: CR02 decision table, CR03 mutation bar, CR05 templates, CR06 kill-rate bands, CR08, **CR10 fail-closed taxonomy**, **CR14 service protocol**, CR15, CR17, CR19–CR21, CR23. Round 1 explicitly left two of these unexercised (E7) |
| E15 | CRMeasure / CRLedger task text in `dispatch1.json` | — | `box3_full_page` = every section sha has an entry with verdict ∈ {executed-ok, verified-record, gap-minor}, blocking 0, wrong 0 (**no class check, no executed-command check, no SHONEN-link check**); assembler: strictest verdict wins "unless an `--override FILE` JSON supplies an L1 resolution with a reason" |
| E16 | pointer census over the snapshot (Python, lane `git ls-files` + fleet paths + `test -e`) | — | 225 unique resolved, 60 unresolved, 5 ambiguous bare names. The sibling/fleet paths all exist (`kumitate…/kimi-census.mjs`, `kagi…/surface-census.sh`, `tsukuroi…/tsukuroi-census.sh`, `mado…/mado-verify.sh`, `scripts/shokunin-watchdog.sh`, `PROTOCOL.md` → OK). **6 evidence pointers are dead /tmp paths**: :919 `/tmp/w6-aud-t6-work/presweep-174248.txt`, :1040 `/tmp/w8-tameshi-t84/pin-read.txt`, :1066 `…/drift-demo.txt`, :1167 `/tmp/w9-tameshi-t93/pin-read-final.txt`, :1215 `…/selftest.txt`, :1216 `…/regression.txt` → MISSING. No lane `path:N-M` reference was out of range |
| E17 | `wc -l tools/mutate-and-run.sh` → 1642; sha `75ed934d…`; history scan for a blob sha prefix `597e1419` | 0 | the protocol (:829-831) pins the harness at "`597e1419…ff6331b`, 1001 lines". That blob exists only at historical commit `e0c453e1…`, and the current tool is r10-2 |
| E18 | `git -C ../kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs \| sha256sum` | 0 | `83016d45049b009a…` = Appendix A pin (:533) |
| E19 | snapshot `:549-551, :568, :584-588` | — | Appendix A's route is "write driver + manifest" → `python3 mutate_driver.py --check/--run` with a written "Driver contract (write from this spec)". `reports/round-1-kaika-coldread.md` "Route" paragraph: round 1 used `tools/mutate-and-run.sh` "over the appendices' literal `python3 mutate_driver.py` route" and reconstructed the B probe fixtures instead of reading "note §7" (`corpus/knowledge/mutation-case-kagi-census.md:208` `## 7. Reproduce` exists) |

## Q1 — What must a full-page cold-read show for box 3 to earn the 2 points?

The rubric has three conjuncts (E3): `[~]` **correctly restrained**, **durable-evidence-linked**, and
evidence that matches the box. The outside exclusion was about scope (E4, E5, E6). So the evidence
must remove exactly the scope defects and introduce no new ones. Acceptance conditions, all required:

1. **A1 — Coverage bound to the final committed page.** Every one of the **51** sections (50
   headings + the frontmatter preamble, E2) of `SKILL.md` *at the measured REV* must have a ledger
   entry whose section sha256 equals that REV's section text. New round-16 sections appended after
   the snapshot, which earlier rounds always added (`## … — round 12/13/14/15`, snapshot :1479-1705),
   need their own wave-2 reads. C2's wording "50 sections" should become "51 (50 headings +
   preamble)".
2. **A2 — Instruction sections executed, not reviewed.** Every instruction-class section has
   verdict `executed-ok` or `gap-minor` *and* a non-empty `commands_executed` that really performs
   the section's prescription. `verified-record` is admissible **only** for `class == record`.
   `not-executed` on any instruction section defeats box 3.
3. **A3 — Round-1 scope debts discharged explicitly.** Each surface SHONEN:10 lists as unexercised
   must appear as executed: the audit recipe (:466), the fail-closed taxonomy (:497), the service
   protocol (:794-898), cadence/tick (:1010-1091) and the runbook (:1272-1301). The two survivor
   probe sets (:552-554, :621-623) must run without reconstructed fixtures. For Appendix B that
   means following "note §7" to `corpus/knowledge/mutation-case-kagi-census.md` §7 (a page-named
   file, so admissible now) or recording a gap. Reconstructing the fixtures repeats E5's rejected
   defect.
4. **A4 — Route fidelity.** Appendices A/B (:527-667) prescribe writing `mutate_driver.py` from the
   on-page driver contract. `executed-ok` requires taking that route. Substituting the runner, as
   round 1 did (E19), is at most `gap-minor` with the substitution named. The round-gate C1 sweep
   (L1, runner) cannot stand in for a cold-read of the protocol section.
5. **A5 — Zero unresolved wrong-expectations and blocking gaps on the final page.** This includes
   the known contradiction at :1472 ("Box 3 remains `[ ]`" vs `SHONEN.md:9` `[~]`, E11) and the
   self-scope statements at :14-15 and :134 ("Historical cold-read proof covers one JS mutant
   only"). These become false or stale the moment C2 lands. Fixes are repairs (new section sha) that
   need a wave-2 re-read, not ledger overrides.
6. **A6 — Resolvable pointers (PROTOCOL box-3 text, E9).** The 6 dead `/tmp` evidence pointers
   (E16) are either disclosed on the page as non-durable historical scratch (a repair → re-read) or
   counted in the box-3 line as a named minor gap. A record verdict must never cite a `/tmp` anchor
   as checked.
7. **A7 — Restrained, durable SHONEN line.**
   - The box wording "Instructions executable by an agent without oral context" stays byte-identical
     (falsifier at `SCORECARD.md:80`).
   - The mark stays `[~]`, never `[x]`.
   - The text keeps "lane-dispatched seats; no independent promotion verifier".
   - It links the committed ledger (`.ufo/evidence/round-16/coldread/ledger.json`) and the
     committed seat reports, not just `reports/round-1-kaika-coldread.md`.
   - It states counts: sections, gap-minor count, final SKILL sha.
   - It is scoped to "`SKILL.md` full page; `corpus/` instructions only as transitively named",
     because PROTOCOL's box 3 covers `SKILL.md`/`corpus/` (E9). Claiming all corpus instructions
     would overclaim.
8. **A8 — Scalar recorded as a candidate.** The before/after counting command runs on both
   revisions. The 6→8 move replaces an outside "Fixed adjudication" (E8). So the lane may report
   "lane-measured 8, box-3 predicate satisfied". The pin should read "pending non-author closure",
   the same pattern as the capability rows (`SCORECARD.md:243-247`). **[INFERENCE]** The integrator
   authored the exclusion and is the natural party to lift it.

## Q2 — Is a lane-dispatched cold-read admissible?

- **For the box-3 `[~]` 2 points: yes.** Boxes 1, 2 and 4 already score as "lane assertion, no
  independent promotion verifier" (`SHONEN.md:5-12`, `SCORECARD.md:217`). PROTOCOL makes the `[~]`
  the lane's own assessment (E9). The page says the same of tameshi-dispatched reviewers (E10).
  Round 1 was rejected for scope, not authorship (E5, E6).
- **For the remaining 2 points and any `[x]`: no.** "A subagent the lane dispatched is still the
  lane" (E9). The rubric reserves those 2 for independent review of all boxes (E3). Any C2 text
  implying >8, `[x]`, or "independent" fails.
- **Caveat: freshness.** The adjudication asks for "a fresh reader" (E5). CR seats are fresh agents
  but received oral context: the `@defect` spec grammar (absent from the page, E12/E13) and the C1
  round-gate details. That context is admissible only if each seat's `opened` shows it actually got
  the grammar from page-named material (`tools/mutate-and-run.sh --help`/header, reachable via
  :834/:1391).

## Q3 — Is the record/instruction split a loophole?

**Yes, as currently mechanized.**

1. **L1 — Class-blind pass set.** `box3_full_page` accepts `verified-record` on any section (E15).
   A seat that labels an instruction section "record" passes it after checking one anchor. In the
   snapshot, most "measured"-titled sections carry reader-directed rules or commands:
   - :314 kill-rate *admission* bands
   - :405 divergence rules
   - :668 third case
   - :1092 confidence statement
   - :1164/:1212/:1230 tick/receipt/re-pin "as executed"
   - :1302 "usage and this round's receipt" (12 backticked commands)
   - :1517/:1563/:1609 round 13–15 sections

   A deterministic tripwire (fences, backticked runnable commands, imperative bullets, must/never/stop,
   title cues recipe/decision/taxonomy/rule/protocol/contract/discipline/usage/limits/registry) flags
   **48 of 51** sections. Only :1 (preamble), :30 (Source notes) and :1464 have none.
   **Hard-instruction set** (never classable as record): 131, 246, 314, 375, 466, 497, 527, 594, 806,
   827, 858, 933, 965, 1021, 1069, 1246, 1302, 1499, 1548, 1676.
2. **L2 — "One anchor per claim cluster" is unbounded.** "Cluster" is undefined, so a 60-line
   record section can pass on one checked hash. It also lets a seat count a dead `/tmp` anchor (E16)
   as verified.
3. **L3 — Mixed sections.** Many sections are both: a recorded receipt plus the command to
   reproduce it. Without a "mixed → instruction" rule, the receipt half launders the instruction
   half.
4. **L4 — Author override.** CRLedger's `--override` lets L1, the page's author, resolve a seat
   disagreement "with a reason" (E15). Overriding a stricter verdict into a pass is self-attestation
   inside the ledger.

## Falsifiers (any one defeats C2's 6→8)

- **F1** A section of `SKILL.md`@REV (including any new round-16 section or a repaired section) has
  no ledger entry with an equal sha.
- **F2** An instruction-class section, or any section in the hard-instruction set above, passes via
  `verified-record`, `not-executed`, or empty `commands_executed`.
- **F3** The :1464 section (box 3 "remains `[ ]`") or the :6/:131 self-scope lines pass unchanged
  while SHONEN reads `[~]` with full-page evidence.
- **F4** An Appendix B probe passes with fixtures the seat built rather than took from the page or
  from page-named §7, or an Appendix A/B `executed-ok` used the runner without naming the
  substitution.
- **F5** A passing entry exists only because of an `--override` that relaxed a seat's stricter
  verdict.
- **F6** A seat's spec/commands use `@defect` syntax but its `opened` list lacks
  `tools/mutate-and-run.sh` (header/`--help`). That means the grammar came from the wave context, so
  the section is contaminated.
- **F7** SHONEN box 3 at REV still links only `reports/round-1-kaika-coldread.md`, changes the box
  wording, becomes `[x]`, drops "no independent promotion verifier", or claims `corpus/`-wide scope.
- **F8** A wave-2 re-read of a repaired section is done by the seat that reported the gap, or by a
  seat briefed with the gap text or fix rationale. That supplies the missing context orally.
- **F9** SCORECARD pins 8 as an admitted score in the lane's own row rather than a candidate pending
  non-author closure, or reports >8.
- **F10** `measure.py` and `assemble.py` partition differently. Test: a trailing-newline-only edit
  must change only the last section's sha consistently in both (the snapshot has no trailing
  newline, E2). The preamble must be counted in both.

## Smallest safe corrections (bounded; for L1 to apply)

1. **`measure.py` (CRMeasure) predicate:**
   - Pass iff the verdict is `executed-ok`/`gap-minor` for `class == instruction`, or
     `verified-record` for `class == record`.
   - The ledger entry carries `commands_executed:int > 0` for instruction passes.
   - The class is checked against the hard-instruction list above. A tripwire hit labelled
     `record` fails unless the entry cites a justification.
   - Entries resolved by an override that relaxed the verdict do not pass.
   - The box-3 2 points also require `SHONEN.md`@REV box-3 line to contain the ledger path.
   - Add the matching `--selftest` cases: instruction→verified-record ⇒ 6; relaxing override ⇒ 6;
     SHONEN link absent ⇒ 6; trailing-newline variance.
2. **`assemble.py` (CRLedger):**
   - `--override` may only pick among seat verdicts at least as strict as the strictest, or record a
     disagreement. Never relax.
   - Carry `class` disagreements: any seat saying instruction ⇒ instruction.
   - Count `commands_executed` per entry.
   - Emit `final_skill_sha256`.
3. **Wave-2 briefs:**
   - Strip the `@defect` grammar and the C1 details from the CR context.
   - Give executor seats (not scout/reviewer) any instruction section that came back
     `verified-record`/`not-executed`, prioritizing :497 and :794-898 (E14).
   - Re-readers of repaired sections get no gap text.
   - Appendix seats take the on-page driver route (A4).
   - The Appendix B seat uses `mutation-case-kagi-census.md` §7 for probe fixtures.
4. **Repairs expected regardless of seat output:**
   - :1472 contradiction (E11) and :14-15, :134 self-scope lines. Append-only supersession wording
     is fine; it still changes section sha, so re-read.
   - Disclose the 6 dead `/tmp` pointers (E16).
   - Name which harness revision a reader of :829-831 should use (E17).
5. **Records:** C2 text and SCORECARD say "51 sections", "lane-measured candidate 8 (lane cap),
   pending non-author closure", and "last 2 points require independent promotion review". Saturation
   follows: the lane can no longer move calibration (`SCORECARD.md:256-257`). That is a tradeoff to
   note, not a defect.

## Impacted axes

- **calibration:** the claim's subject. A1–A8 and F1–F10 apply.
- **quality:** :1472, :14 and :134 are on-page contradictions or staleness.
- **depth:** none (C1 untouched by this review).
- **operability:** only the measure/assembler predicates.
