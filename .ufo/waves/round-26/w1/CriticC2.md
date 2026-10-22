# CriticC2 — round 26, wave 1: attack on claim C2 (calibration)

Seat: TameshiR26.CriticC2 (critic, leaf). Access date for every source below: 2026-10-22.
Measured revisions: integration `a08e85c5d7f899e8a5992e20517edb1a380d79eb`, base `d4140796f4e48e8ec81b793facba73fbd03b4443`.
Counter bytes: `.ufo/evidence/round-26/c2-measure.py` sha256 `be14cc45baacbe39d115b44f6d6acbe17db7298d9938bd2766a5269b359630af`, unchanged between `622d31d` and `a08e85c`.
All runs happened in the scratch clone `/tmp/criticc2-r26/lane` (plus copies `ce1`, `ce2`, `ce2b`, `ce3`, `ce3b`). Nothing in the lane was run or written apart from this report.

## Verdict

1. **C2 is mostly a record chore that carries a calibration label.** Under prompt section 6.9 and AXES.md, only one of its three labels (R25-SPOT-2) is a mismatch between the lane's self-assessment (SCORECARD) and repo state. R25-SPOT-1 is a registry-conformance item, which belongs to operability. R25-SPOT-3 is a stale verified-at line, which belongs to freshness. A reading of `3/3 → 0/3` as three calibration mismatches overstates its calibration content by a factor of three. The contract itself concedes the point: "this is a record repair".
2. **The population is honestly fixed.** The three labels were frozen at `622d31d`, before the edits at `a08e85c`, and they were chosen by an outside spot-check, not by the author. **The population is not the defect class, though.** The registry-gap class that R25-SPOT-1 names is still live in the record at `a08e85c`: 16 round counters that exit with verdicts, including the round-24 ruler that the round-24 spot-check routed, have no registry row. `0/3` will be reported while that class is still open.
3. **c2-measure.py has three fixable holes that cause false RESOLVED results.** I reproduced each one. Item 3 accepts a receipt from a different tool, which is exactly the defect class that item 3 names. Item 2 accepts text that only restates or negates the defect, and one of its three tokens (`77302fa`) is already satisfied at base. Item 1 accepts any active row whose argv merely mentions the path.
4. **The drift sentinel trips at this closure.** Calibration has been the claimed axis for five rounds running (rounds 22 to 26), each with the numeric score at 8→8. Three of those rounds in a row (24, 25, 26) took the previous closure's routed items as the claim population. Round 27 must work a different frontier area. C1 (depth) satisfies that requirement this round; C2 does not.
5. **The contract's separability sentence is false for one file.** C2 item 3 hashes `tools/mte-interop.py`. C1's commit `a08e85c` edited that file, which moved C2's target hash from `8269b82f…` to `193ea6e3…`.

None of these findings is fabrication. The current drafts are substantive (see the item 2 note below). The defects are in what the frozen counter can see, and in how the claim is labelled.

## Evidence

### Counter runs (scratch clone)

```
$ python3 .ufo/evidence/round-26/c2-measure.py --repo ../base        # d414079
C2_ITEM R25-SPOT-1: MISMATCH (no active registry.json row runs tools/mte-interop.py; no SKILL.md table row for tools/mte-interop.py)
C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks 'amendment 3'; SCORECARD after round-25 results lacks 'before_any_after_measurement'; lesson after ## Claims lacks 'amendment 3')
C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=8269b82f213e; ...)
C2_RECORD: mismatches=3/3                                             exit 1
$ python3 .ufo/evidence/round-26/c2-measure.py --repo .             # a08e85c
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: MISMATCH (... same three reasons ...)
C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=193ea6e32f89; ...)
C2_RECORD: mismatches=2/3                                             exit 1
```

The base run matches the committed `.ufo/evidence/round-26/c2-before.stdout`.

### Claim type versus the round-26 prompt section 6.9 and AXES.md

- `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-26.md:347-348`: "A calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state."
- `/home/vgpnk/Projects/shokunin/AXES.md:15`, calibration: "SHONEN.md/SCORECARD entries match observed repo state". `AXES.md:14`, freshness: "Drift detection — skill claims re-verified against live surfaces; stale items flagged or fixed".
- `corpus/lessons/round-25-verifier-spotcheck.md:191-192` classifies item 1 itself: "a §Gate standard Registry conformance defect and is status-neutral". Item 1 concerns `tools/registry.json` and the SKILL.md gate table. Neither file is SCORECARD or SHONEN, so this is operability.
- Item 3 (`:197-199`, "`verified-at` records the `09dc114` run … not the measured tool … Refresh it.") is a knowledge-entry drift refresh. That is the definition of freshness.
- Item 2 (`:193-196`) is a SCORECARD and lesson record that omits amendment 3. It is a real self-assessment mismatch. Calibration content: **1 of 3**.
- `.ufo/evidence/round-26/contract.json:41`: "calibration stays 8 (lane cap); this is a record repair".
- The labels were found by the outside spot-check, not by the lane's own self-assessment. Fixing them shows that the lane responds to routing. It does not show that its self-assessment caught an overreach.

### Item 3 hole: the counter accepts a receipt from a different tool (CE-3, CE-3b)

The counter (`c2-measure.py:86-93`) passes item 3 if *any* backticked `.stdout` named on the line contains `MTE_SELFTEST: N/N pass`. It never checks that the receipt was produced by the tool whose hash the line names.

- `.ufo/evidence/round-25/after/c2-selftest.stdout:18` reads `MTE_SELFTEST: 17/17 pass`. That run used tool `8269b82f…`.
- I counted tool-hash strings in the receipts with `grep -c '193ea6e'` and `grep -c '8269b82f\|193ea6e'`. Every receipt returned 0: both round-26 `after/*.stdout` files, and the round-25 receipt. No receipt binds the hash of the tool that produced it.
- CE-3b: I set the clone's line 2 to ``verified-at: 2026-10-22; tool sha256 193ea6e3; selftest 17/17 (`.ufo/evidence/round-25/after/c2-selftest.stdout`)``. Result: `C2_ITEM R25-SPOT-3: RESOLVED`. The line names the new tool and cites a run of the old one, which is the exact defect R25-SPOT-3 routes.
- CE-3: I copied the lane's uncommitted draft line (`corpus/knowledge/mte-report-interop.md:2` in the lane working copy) into a clone where `.ufo/evidence/round-26/after/` does not exist. Result: `RESOLVED`. The draft also names the round-25 receipt, and that receipt alone satisfies the check. The round-26 receipts are therefore not load-bearing for the frozen counter, and an uncommitted round-26 `after/` directory would go unnoticed.

### Item 2 hole: the counter matches tokens, not a correction (CE-2a, CE-2b)

The counter (`c2-measure.py:50-69`) searches the *whole* SCORECARD tail after the round-25 measured-results heading, which includes any round-26 section. It also searches the whole lesson after `## Claims`, through EOF, rather than the Claims section itself. It looks only for the presence of tokens.

- `77302fa` is vacuous: it is already present at base, at `SCORECARD.md:1242` (the measured-commit cell) and at lesson `round-25.md:105,136` after `## Claims`. The base output lists no `77302fa` reason.
- CE-2a appended a round-26 declaration line that only *restates* the open defect ("…counts R25-SPOT-2 (round-25 record omits amendment 3 and the before_any_after_measurement caveat) as an open mismatch"), plus "amendment 3 is not reconciled here" to the lesson. Result: `C2_ITEM R25-SPOT-2: RESOLVED`. The round-26 SCORECARD declaration of C2 would naturally carry this text.
- CE-2b appended "amendment 3 (77302fa) also carries before_any_after_measurement: true". This repeats the very flag the spot-check disputes, and does not mention that seats saw C2 PASS 8/8 at `c9ff09f`/`09dc114`. Result: `RESOLVED`.
- Mitigation that I observed: the current draft `.ufo/waves/round-26/w1/DraftLesson25Correction.md:100,164-169` does state that seats ran the C2 counter "at PASS 8/8 at `c9ff09f` and `09dc114`". The delivered content is substantive, but the frozen counter cannot tell it apart from CE-2a or CE-2b.

### Item 1 hole: the counter matches the argv token, not a working row (CE-1)

The counter (`c2-measure.py:36-47`) accepts any active row whose argv contains the path string, and any SKILL line that begins ``| `tools/mte-interop.py` |``.

- CE-1 restored the base `registry.json` and `SKILL.md`, then added `{"status":"active","argv":["true","tools/mte-interop.py"]}` and the line ``| `tools/mte-interop.py` | not a gate |``. Result: `RESOLVED`.
- This hole has low impact this round. The real rows at `a08e85c` run `--selftest` (expecting `MTE_SELFTEST: 17/17 pass`) and `--check` (expecting `MTE_INTEROP: PASS legs_conforming=9/9`), and they sit at SKILL.md:2101. The rows are real; the counter just could not tell if they were not.

### Population: the same class is still live outside the three labels

- At `a08e85c`, every file in `tools/` has at least one active registry row, so the R25-SPOT-1 instance is the last one under `tools/`. Item 3 is likewise the only knowledge-entry `verified-at` line that names a tool hash.
- Every verdict-exiting round counter under `.ufo/evidence/round-2*/` has **0** active registry rows: 16 files, including `round-24/measure.py`, whose exit is `return 0 if n == len(rows) else 1` (`:215`), and C2's own `round-26/c2-measure.py`.
- `corpus/lessons/round-24-verifier-spotcheck.md:64`, routing item 2: "Register the ruler's bounded output contract and the replay-bundle row". Spot-check line 56 also lists the "unregistered ruler".
- Items 4 and 5 are excluded from the population (`contract.json:42`). Item 4 includes "round-24 spot-check items 2–4" (`round-25-verifier-spotcheck.md:200-203`). The excluded set therefore holds an older, still-open instance of the very class that R25-SPOT-1 counts.
- The exclusion is defensible, because the lane's record already calls item 4 open, so record and repo agree. It does mean that `0/3` must not be read as "the registry-gap class is closed".

### Drift sentinel: "same axis+surface claim or same routed defect class in a lane 3 rounds running"

Source: `/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:173`. Action: "The lane's next round must work a different frontier area."

- Calibration has been the claimed axis for five rounds running, all at numeric 8→8:
  - round 22: `SCORECARD.md:968`, "C1 calibration"
  - round 23: `:1029`
  - round 24: `:1129`
  - round 25: `:1210`
  - round 26: `contract.json:35`
  - Round 21 was the last round without one (`:865`, "Depth 8 and calibration 8 are no-harm monitors, not claimed").
- The same surface, the previous closure's routed items, held for three rounds in a row:
  - round 24: predicates "routed by round23 critics and closure" (`round-24-verifier-spotcheck.md:18`)
  - round 25: "round-23 closure items with no SCORECARD disposition" (`SCORECARD.md:1211-1213`)
  - round 26: round-25 spot-check routed items 1-3
- The same routed defect class recurs:
  - Registry gaps: round 23 (registry rows not pinning their bundle, `round-23.md:174`), round 24 (unregistered ruler and replay rows, spot-check `:64`), round 25 (unregistered mte-interop, `R25-SPOT-1`).
  - Stale `verified-at` tool revision: rounds 19 (`round-19-verifier-spotcheck.md:57`), 22 (`round-22.md:108`) and 25.
- Effect: the sentinel trips at the round-26 closure. Round 27 must not declare another calibration claim whose population is the previous closure's routed items. This round's C1 (the depth leg on a new gate) already does what the sentinel asks; C2 is the repeat.

### Separability statement is false for `tools/mte-interop.py`

- `contract.json:45`: "C2 on registry, SKILL, SCORECARD, lesson and knowledge-entry bytes. Either counter can move with the other's edits absent."
- `c2-measure.py:78` hashes `tools/mte-interop.py`. `git diff 622d31d a08e85c -- tools/mte-interop.py` shows C1's edit adding `'js-cite-check': 'TABLE_CITECHECK'` and changing "eight" to "nine". That edit moved item 3's target from `8269b82f213e` to `193ea6e32f89`, as the two counter runs above show.
- The R25-SPOT-1 fix (registry and SKILL rows) also landed inside the C1 commit `a08e85c`.
- C2 can still be measured with C1 absent, but any later wave-2 edit to `tools/mte-interop.py` turns item 3 back to MISMATCH. C2 must be re-measured at the final tip.

## Impacted axes

- **calibration:** the claim's label and content. Counting the three labels as calibration mismatches overstates it (1 of 3 is calibration-shaped), and the frozen counter yields false RESOLVED results on items 2 and 3.
- **operability:** R25-SPOT-1 is really operability work. The registry gap for 16 round counters is still open.
- **freshness:** R25-SPOT-3 is really freshness work, and the receipt-to-tool binding is unverified.
- **discernment** (trend): a closure that reads `0/3` as "the record matches the repo" would admit the CE-3b state.

## Smallest safe correction (no post-landing narrowing; frozen bytes untouched)

1. **Label honestly in the report and SCORECARD row.** Keep the frozen target `0/3`. State that R25-SPOT-2 is the calibration mismatch, that R25-SPOT-1 is an operability or registry repair, and that R25-SPOT-3 is a freshness refresh. Numeric calibration stays 8→8, and nothing is credited beyond a record repair. This qualifies the claim; it does not shrink the target.
2. **Item 3:** bind each receipt to a hash. Commit `.ufo/evidence/round-26/after/mte-{check,selftest}-a08e85c.stdout` together with a sibling `.sha256` or `.json` that records `sha256(tools/mte-interop.py)` at run time. In the `verified-at` line, label the round-25 receipt as history, outside the current-run clause. Add a companion (not frozen) check, in the style of round 25's `c1-pins.py`, that fails CE-3b. Disclose CE-3b in the lesson.
3. **Item 2:** add a companion check that requires `c9ff09f` or `09dc114` and `8/8` in the appended correction, so that CE-2a and CE-2b fail. In the lesson, disclose that the frozen `77302fa` token was already satisfied at base.
4. **Separability:** add an erratum that C2 item 3 also reads `tools/mte-interop.py`. Re-run `c2-measure.py` at the final lane tip after wave 2, not at an intermediate commit.
5. **Sentinel:** record the trip (calibration claimed in rounds 22 to 26; routed-item population in rounds 24 to 26). Route the 16 unregistered round counters, including the round-24 ruler, as an open item of the R25-SPOT-1 class, so that `0/3` is not read as the class being closed. Round 27 works a different frontier area.

Tradeoff that the canonical judge must rule on (not fixable by this seat): whether a record repair whose population is mostly operability and freshness items can be admitted as a calibration axis move at all. On this evidence: admissible only as "improved (record repair), 1/3 calibration-shaped", and never as a calibration uplift.

## Installs

None. Tools used: system `python3`, `git` (read-only on the lane with `GIT_OPTIONAL_LOCKS=0`; clone, checkout and worktree only in `/tmp/criticc2-r26`), and `grep`/`sed`/`awk` for reads. No `jj` command was run.
