# S10 — mention sweep: round-14 recipe, disposition gate, box-3 full-page claim

Seat: `TameshiR17.S10MentionSweep` (scout, leaf). Rev under sweep:
`98bea7da5801f4bc58e4187690ee1687c8a5061f` (`git rev-parse` == the dispatch tip;
`git --no-optional-locks status --porcelain` shows only untracked `.ufo/` round-16/17
artifacts). Scope: `SKILL.md`, `SCORECARD.md`, `LOG.md`, `README.md`, `PROVINCE.md`,
`corpus/**` — plus `SHONEN.md` because the box-3 cluster lives there (not in the
listed six, flagged as such). No tool installed or updated; no lane file edited.

Method: read committed bytes from `git archive 98bea7da` extracted under
`/tmp/tameshi-r17w1-S10MentionSweep-5GpqZe`; ran the cited commands in a
fleet-mirror clone of the same rev (siblings symlinked) so every exit below is an
observed run, not a reading of prose.

## 1. Ground truth (executed at `98bea7d` unless stated)

| # | Command | Observed |
|---|---|---|
| G1 | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json` | **exit 2**, `id=expected_input_digest_mismatch`, `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`, `status=could_not_evaluate` |
| G2 | same with `…/dispositions.json` | **exit 2**, identical finding |
| G3 | `git archive 28aeef4 \| tar -x` into `/tmp`, then from the **lane root** `--root /tmp/…/ar28 --dispositions .ufo/evidence/round-14/dispositions.json` | **exit 0**, `status=clean`, `effective 11`, `superseded 1`, `failed 0`, `findings 0` |
| G4 | `git show <rev>:tools/mutate-and-run.sh \| sha256sum` at 28aeef4 / 09ee1d0 / 05a2247 / 98bea7d | `75ed934d…` / `0673d2e5…` / `0673d2e5…` / `0673d2e5…`; `expected.json:inputs["tools/mutate-and-run.sh"]` pins `75ed934d…` |
| G5 | `python3 .ufo/evidence/round-16/measure.py --rev 09ee1d0…` | **exit 0**; `coldread {box3_full_page: true, sections_covered: 54, sections_total: 54}`; `shonen.box3_ledger_link: true` |
| G6 | own sectionizer over `coldread/SKILL.snapshot.md` vs `SKILL.md` | `### Round-15 gate/probe registry` body: **30 lines** (1676-1705) at the snapshot, **31** (1676-1706) now |
| G7 | `ledger.json` query | entry `start 1563` (`## Effective expectation reconciliation — round 14`) is `verdict: gap-minor`, one seat (`CR26`), sha `97cf436b`, `commands_executed_count: 4`, **no `inputs` map (v1 schema)** |

**The decisive fact.** G1 and G2 are both exit 2. Every predicate in the round-14
recipe is unreachable at the tip, because `evidence-disposition.py:1182-1192`
verifies pinned inputs before it evaluates anything. `54/54` is still literally
what the round-16 counter prints (G5) — the surplus credit is a property of the
v1 sha-only rule, not a numerical error in the ledger. Corrections must therefore
say "the page no longer earns full-page credit", never "the ledger counted wrong".

## 2. Stale outcome statements (the acceptance list)

Classification: **F** = states an outcome that is false now and must be corrected;
**F-r** = false only under the round-17 input-keyed rule (the old counter still
reproduces the number — rewrite must name the rule, not change the count);
**M** = entry point whose stated/implied outcome is no longer reachable though its
exit map still matches; **C** = contested judgement, appended erratum only.

| # | path:line | quoted statement | now true | class |
|---|---|---|---|---|
| 1 | `SKILL.md:1581-1583` | "`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json` must fail the unresolved producer_before assertion. A matching exit1 is insufficient." | exit **2** `expected_input_digest_mismatch` (G1); no `producer_before` finding is emitted at all | **F** (R16-C2a) |
| 2 | `SKILL.md:1584-1586` | "Run the same command with `dispositions.json`: the only repair is that row's explicit supersession…" | exit **2**, same finding (G2); the clean ledger is reached only at the archived root (G3) | **F** (R16-C2a) |
| 3 | `SKILL.md:1601` | round-14 registry row: entry "`… --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`"; map "…2 could-not-evaluate invalid/missing/tampered inputs…" | the registered entry now returns 2 for a **non-tampered, by-design** reason; the row's 2-class no longer means what it says | **M** |
| 4 | `SKILL.md:1512` | "`SHONEN.md` box 3 currently carries a scope-bounded `[~]`, not `[ ]`" | box 3 now carries a **full-page** claim (`SHONEN.md:9-10`); "scope-bounded" is false | **F** |
| 5 | `SKILL.md:1717-1718` | "Wrong expectations were repaired in place with the line count of every edited section unchanged, so every `SKILL.md:<line>` self-anchor still resolves" | false for `### Round-15 gate/probe registry`: **30 → 31** lines (G6); anchors do still resolve (that half holds) | **F** (RX9, disclosed only in the lesson) |
| 6 | `SKILL.md:1798-1804` | "Every bucket of this page was read by a seat… this earns the box-3 lane assertion (`[~]`)" | read = yes; **earns = no**: one credited instruction bucket (`:1563-1596`) executes to exit 2 | **F** (R16-C2c) |
| 7 | `SHONEN.md:10` | "…round-16 cold-read of every SKILL.md bucket…, instructions executed in /tmp, records re-anchored, **wrong expectations repaired and re-read**…" | not repaired on `:1563-1596`; box 3 is open on that bucket | **F** (R16-C2c) |
| 8 | `SCORECARD.md:246` | capability "effective expectation reconciliation": "same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded" | true at `6431478`; **not re-runnable at HEAD** — both forms exit 2 (G1/G2) | **F** (R16-OP1) |
| 9 | `SCORECARD.md:571` | "0/51 (no ledger) → **54/54 buckets** at the measured page sha `906fb649…`… **calibration 6 → 8** (lane cap…)" | credit is **53/54**; calibration stayed **6** (non-author closure) | **F-r** |
| 10 | `SCORECARD.md:586` | "calibration \| improved, 6 → 8 (pending non-author)" | non-author returned: **6** | **F** |
| 11 | `SCORECARD.md:588` | "operability \| **unchanged** \| … The round-14 disposition gate now exits 2 at `--root .` by design… its archived-root form exits 0" | the two gate facts are true (G1-G3); "unchanged" is false — the axis was graded **harmed** | **F** |
| 12 | `LOG.md:1036` | "C2 calibration 6→8: every bucket of SKILL.md was cold-read by lane seats" | read = yes; the **8** does not hold | **F** |
| 13 | `LOG.md:1041-1042` | "ledger …: 75 entries, **54/54 buckets** of the measured page" | 53/54 credited under the corrected rule | **F-r** |
| 14 | `LOG.md:1044` | "`--rev 09ee1d0` → cases 7, **restraint 8**, coldread 54/54" | restraint **6** | **F** |
| 15 | `corpus/README.md:231-233` | "the four 'full-page cold-read / box 3 open' sentences at lines 143-146, 160, 190 and 207 **are superseded** by … ledger.json" | only partly: box 3 remains open on one bucket, so those sentences are still owed | **F** |
| 16 | `corpus/lessons/round-16.md:6` | "**C2 calibration 6→8** (full-page cold-read…)" | false as a claim; keep as history, append the non-author result | **C** (append-only record) |
| 17 | `corpus/lessons/round-16.md:23` | G6 "**admit** \| every bucket of the final page (54…) has a passing entry at its own section sha" | the reason is literally true; the **admit** is falsified | **C** (append-only record) |
| 18 | `corpus/lessons/round-16.md:63` | "Correct fail-closed behaviour. The registry row now names the archived-root invocation (`git archive 28aeef4` → exit 0)" | exit 0 at the archive is true (G3); "correct" is disputed for operability and is what R16-OP1 repairs | **C** |
| 19 | `corpus/knowledge/incremental-pin-disposition.md:362` | "Read `.ufo/evidence/round-14/dispositions.json` and its checker receipt…; **exit1** alone does not make its FileNotFoundError the intended mechanism failure." | a live re-run now yields 2, not 1 | **M** (minor) |

Closure count: 19 statements across 7 files (SKILL 6, SCORECARD 4, LOG 3,
SHONEN 1, corpus/README 1, corpus/lessons 3, corpus/knowledge 1).

## 3. Statements verified TRUE — do not "correct" these

| path:line | statement | verification |
|---|---|---|
| `SKILL.md:1681` | "since round 16 the runner input moved, so `--root .` returns 2 `expected_input_digest_mismatch` by design; use `--root` on `git archive 28aeef4` extracted to /tmp → 0 clean" | G1/G2 = 2 with that exact id; G3 = 0 clean, 11 effective + 1 superseded, findings 0 |
| `SKILL.md:1741` | errata row restating the same | same runs |
| `SKILL.md:1568` | "These instructions add no full-page cold-read or independent promotion credit." | still true of the round-14 section |
| `SKILL.md:15` | "round 16 adds a full-page cold-read (Errata — round 16)" | the read happened; the *credit* is what fails (§2 #6) |
| `SKILL.md:134-135` | "round 16's full-page cold-read executed it end to end (two seats…)" | refers to the **mutation-sweep** recipe; errata row `:1726` and `w1/CR04a|b` support it |
| `SCORECARD.md:565` | "the intermediate `measure-3490708.json`: 53/54 buckets before the errata re-read" | true as history; ironically the same 53 the corrected rule now yields |
| `corpus/README.md:184` | "Complete twelve-row effective/superseded ledger…" | describes ledger contents at r14; still accurate |
| `corpus/lessons/round-14-verifier-spotcheck.md:90-92` | `--root .` → exit1 / exit0 receipts | true at that revision; historical record, not a current claim |

One reproducibility gap in an otherwise true statement: `SKILL.md:1681`/`:1741` omit
that `--dispositions` resolves against **CWD**, so the archived form only reaches 0
when run **from the lane root** (RX6 §2.4). I reproduced RX6's `dispositions_missing`
from the parent directory. Adding "run from the lane root" is a clarification, not a
repair of a false outcome.

## 4. Adjacent findings the sweep produced (not in the routed list)

- **`SKILL.md:1512` is an uncaught box-3 state statement** (§2 #4). Round 16's errata
  table dated `:1472` "Box 3 remains `[ ]`" but never touched `:1512`. The bucket
  containing it (`start 1499`, `### Gate/probe registry`, class `record`) is credited
  `gap-minor` from `CR24`/`Replica1499` at `97cf436b`, so the v2 rule will also require
  `inputs` for a bucket whose text is stale in the present tense.
- **`SKILL.md:1717-1718` is undisclosed on the page.** The contradiction is recorded
  only in `corpus/lessons/round-16.md` §Process disclosures ("one section short…
  `### Round-15 gate/probe registry` gained a trailing blank line"). The page itself
  still asserts the invariant flatly, which is exactly the "corrections sweep every
  mention" obligation.
- **The ledger's `1563` entry has no `inputs`.** Under the v2 credit rule it fails
  with `inputs-unrecorded` before any drift check — that is the red-before C1 needs,
  and it is independent of whether the recipe text is later repaired.
- **`corpus/lessons/round-16.md:64`** ("the landing page has 54 buckets… no fixed
  denominator is claimed") is true and should survive correction untouched; it is the
  cleanest place to anchor the distinction between "54 buckets counted" and
  "54 buckets credited".

## 5. Correction map (what the L1 must touch, by surface)

| Surface | Action |
|---|---|
| `SKILL.md:1581-1586` | repair steps 2-3 for the moved runner, or mark the recipe historical with the working archived-root invocation **and** "run from the lane root" (R16-C2a). |
| `SKILL.md:1601` | annotate the round-14 registry row (or fold it into `:1681`) so its `--root .` entry carries the same note. |
| `SKILL.md:1512` | date the box-3 state ("scope-bounded at this write; full-page claim since round 16, one bucket re-opened"). |
| `SKILL.md:1717-1718` | qualify "line count unchanged" with the one-section exception, or drop the invariant to "anchors resolve". |
| `SKILL.md:1798-1804` | qualify the box-3 credit: one credited bucket was left stale by the round itself (R16-C2c). |
| `SHONEN.md:10` | append (never rewrite) the open-bucket fact and the pending non-author status. |
| `SCORECARD.md:246,571,586,588` | 246 re-pin to the live-tree path once C2 lands; 571/586/588 carry the non-author outcome (calibration 6, operability harmed/restored). |
| `LOG.md:1036,1041-1044` | append the corrected reading (restraint 6, 53/54 under the input-keyed rule) rather than editing the round record. |
| `corpus/README.md:231-233` | narrow "are superseded" to "are superseded for the buckets that passed; box 3 open on `SKILL.md:1563-1596`". |
| `corpus/lessons/round-16.md:6,23,63` | append a dated errata block; leave the rows as written. |
| `corpus/knowledge/incremental-pin-disposition.md:362` | optional: note the checker's live-tree form now returns 2 and the read is via the archived root. |

## 6. Remaining unknowns

- I did not run the round-17 `measure.py` (not yet at the swept rev), so "53/54"
  is derived from the R16 spotcheck's independent re-derivation plus the
  `inputs-unrecorded` rule, not from an executed v2 count. [INFERENCE]
- `corpus/lessons/round-14.md:139` and `:35` were read as history; neither states a
  current-run outcome.
- No mention of the round-14 recipe, the gate, or the box-3 claim exists in
  `README.md` or `PROVINCE.md` (grep: zero hits for all six clusters); `PROVINCE.md`
  only carries the round-16 Core append and its wave-2 correction, both unaffected.

## 7. Environment note (observed, not mine)

The live worktree moved while this sweep ran; I wrote only my report and reverted
nothing. `git --no-optional-locks status --porcelain` at start showed only untracked
`.ufo/` artifacts; at close it also shows ` M .gitignore` (`+ .ufo/state/`,
`+ .ufo/watchdog.log`) and ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`.
The latter is a **4-line append** (dated round-17 correction of R16-EV1, citing
`0673d2e5…` at `05a2247/09ee1d0/017a2b0/98bea7d`) — append-only as routed, and at
the swept rev the committed blob is still the stale `89722ddb…`. Neither change
altered any byte I swept: every finding above is against `git archive 98bea7da`.
Seats that assert a clean worktree should expect these two paths.

Verdict: **partial** — 19 stale outcome statements located (12 false outright,
2 counter-reproducible but false under the input-keyed rule, 2 misleading entry
points, 3 append-only records), and the two statements a careless sweep would
"fix" (`SKILL.md:1681`, `:1741`) reproduce exactly as written.
