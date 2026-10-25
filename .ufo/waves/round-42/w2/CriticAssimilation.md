# Critic — round-42 assimilation decisions (wave 2, FALSIFY)

Seat: `L1Tameshi42.CriticAssimilation` · access date 2026-10-25 · read-only (only write: this file).
Attacked: the `## Gate` block of `corpus/lessons/round-42.md` (integration tip
`a21845f523b75adbd3e3f7a62af91294db224ad9`), against addendum §10
(`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:238-337`) and the frozen contract
(`.ufo/evidence/round-42/contract.json:52-61`). No counter was run. No tools were installed.

## D1 — refusing `survivor-classification.md`: the outcome holds, but two of its three reasons do not

**Counterexample: the same Gate block repairs larger defects in the entry it admitted.**

- Reason (1) is the quote drift (lesson :51-53). Re-fetch:
  `curl -fsSL -m 60 'https://zenn.dev/seckeyjp/articles/j-six-mutation-testing' -o /tmp/tameshi-r42w2-CriticAssimilation-zenn.html`
  returned exit 0, 171806 B, sha256 `f7063c33…` (the page is dynamic: same size as the wave-1
  fetches, different hash). Counts: `grep -c 'テストの穴とは当たりません'` → 0, `grep -c 'テストの穴とは限りません'` → 2.
  So the drift is real. But the addendum makes it irrelevant as a refusal ground. It says "your
  Gate block carries YOUR access date and ≤25-word located quote — the campaign's `opened` date
  and quote prove nothing about this lane" (lane-addendum.md:256-258). The process the addendum
  requires replaces the staged quote with the lane's own quote. A drifted staged quote is
  therefore an expected repair, not a defect of the entry.
- Reason (2) is the recheck count. `grep -c '168 killed'` → 2, which confirms lesson :54. But the
  same lesson rewrites the admitted entry's staged recheck cells (`365d — curl …` → `180d`,
  lesson :85-88). The addendum orders that normalization for every adopted row: "recheck becomes
  a valid ISO date, `NNd`, or symbolic cadence" (lane-addendum.md:297-298). A wrong count in a
  recheck cell is the class of fault the round repaired in the entry it admitted.
- What the admitted entry had repaired, by contrast (lesson :38-45):
  - E1: a false claim about the lane's own convention (timeout as detection).
  - E2: a miscounted list of factors.
  - Its headline was cut, and a new headline now "rests on S158 and S001" (lesson :44).

  A false claim about the lane is worse than a one-character drift that keeps the meaning, yet
  the first was repaired and admitted while the second counts as a refusal reason.
- Reason (3) does hold. Compare the staged thesis, "A surviving mutant is a candidate hole; it
  becomes a hole only after it is classified" (package entry :8), with the held recipe "a hole
  call needs an expectation the mutant cannot move. Before calling a survivor a hole, name its
  anchor" (`corpus/knowledge/oracle-anchored-survivors.md:90-92`). They make the same rule. What
  the staged entry adds:
  - a 3-of-15 yield figure from one small tier-B system;
  - an arXiv equivalence rate that the package already carries in `llm-mutant-equivalence-cost.md`.

  The entry itself says "the lane's own classification is **not performed**" (package entry
  :47). Under "expansion credit only on coverage-map ground the lane did not hold"
  (lane-addendum.md:264-265), that is enough to refuse.
- Side defect in the record the lesson relies on: `ReviewSurvivorGate.md` suggests
  `grep -c '168 killed / 15 survived'` → 1 as the fixed recheck. On the bytes fetched today it
  returns **2**, so following that suggestion would leave the recheck false again.
- The two scouts disagreed on duplication. `ScoutSurvivorEntry.md` §4 says "No duplication …
  (different scope: rule vs executed classification)" and votes ADMIT, while
  `ReviewSurvivorGate.md` votes REFUSE. The lesson cites only the refusing gate (:56) and does
  not record the disagreement.

**Verdict D1:** the refusal itself SURVIVES, on reason (3). Reasons (1) and (2) are BROKEN as
refusal grounds: they are repairs that the addendum itself requires and that this round
performed on the admitted entry. The flip condition (lesson :56-58) should rest on reason (3)
alone, meaning a stated addition beyond the held F8 entry, not on a re-quote or a recheck fix.

## D2 — leaving the cjk entry unadopted for being off-theme: BROKEN

- The stated reason (lesson :63-64) is that "a round takes one theme and the entry's ground is
  the score denominator, not which outcomes count as a kill". Three records contradict it:
  1. The frozen contract lists this entry as a candidate under this very theme
     (`contract.json:53-58`: `"theme": "mutant outcome vocabulary …"`, `"candidates": [ … "mutation-score-semantics-cjk.md", …]`).
     The theme was frozen with the entry inside it.
  2. The wave-1 theme scout ranks it second best for this theme and marks it `central`
     (`.ufo/waves/round-42/w1/ScoutPackageTheme.md:34`, `:96`).
  3. The admitted entry stands on the same denominator ground. Its body says "say how each class
     enters the denominator" (`corpus/knowledge/pit-outcome-vocabulary.md:56-57`) and that
     runtime errors fall "outside `detected / valid`" (`:38`). The line drawn between the
     admitted entry and the cjk entry does not exist in the text.
- Adoption was not forced. The addendum sets "ONE theme and 1–3 knowledge entries"
  (lane-addendum.md:253-254), and one admit is within that range. Choosing not to adopt is
  allowed; giving a false reason for it is not.
- The flip condition (lesson :65) asks only that the three sources be re-opened and
  snapshotted. It leaves out the admission conditions the positive gate made binding: the
  dangling `CANNOT-ANSWER.md §3.7` pointer, which `ReviewCjkGate.md` finding 4 and flip (c) call
  "a condition of admission, not a waiver", and the entry's internal citations of
  `S159` and `S156` (package cjk entry :40, :46), which must be re-pointed by document. That
  flip condition shows the real blocker is missing snapshots and repair work, not the theme.
- The addendum has only admit and refuse ("Refused entries keep reason + flip condition",
  lane-addendum.md:259-260). "Not adopted, sibling theme" is a third state that the addendum does
  not define, and LOG.md:2205 repeats the same reason.

**Verdict D2:** BROKEN. Leaving the entry out is permitted, but the reason recorded is
contradicted by the frozen contract, the round's own theme scout, and the admitted entry's text.
Smallest safe correction: an appended note that names the real reason (sources not snapshotted;
two admission repairs pending) and lists the complete flip conditions.

## D3 — S158 (not from the package) inside an assimilated entry: disclosed, but the admit credit is overstated

- The append is allowed: "Append only the rows the admitted entries cite"
  (lane-addendum.md:258), and S158 is cited at `pit-outcome-vocabulary.md:3`. The snapshot
  verifies: `sha256sum .ufo/evidence/round-42/sources/pit-DetectionStatus.java` →
  `3bf295ad…c419c6`, which matches lesson :31, and line 63 reads `RUN_ERROR(true),`.
- Row-level provenance is disclosed in five places:
  - entry :10-12 ("S158 is new this round");
  - lesson :33-34 and :76 ("S157 and S158 are new rows, not from the package");
  - `corpus/SOURCES.md:446`;
  - `LOG.md:2198` ("S155, S156 (assimilated, re-grounded), S157, S158 (new)").

  No reader would take S158 for a package row.
- The blur is at the entry level, not the row level. The staged headline, "A mutation score's
  denominator is a choice of outcome class, and one of those classes is not stable across runs"
  (package entry :8), was replaced by "PIT and Stryker name the same outcomes and score them
  differently" (admitted :8). The lesson concedes "The new headline rests on S158 and S001"
  (:44), and neither of those is a package row. Yet the entry header calls itself "Assimilated
  … re-grounded" (:10-11), and the Gate counts it as the round's single admit (lesson :10, :19).
  The thesis that carries the admit is lane-authored work from a critic's discovery
  (`CriticOracleSource.md` F3). "Re-grounded" understates a thesis replacement.
- Adjacent, outside this seat's scope: the contract's C2 `sourced` clause (`contract.json:49`)
  requires the kill oracle to cite "the PIT outcome vocabulary row adopted this round". After
  P1, PIT is withdrawn as support (`contract.json:71`), so the assimilated entry now argues
  against the oracle's PIT citation rather than backing it. Routed to the C2 critics.

**Verdict D3:** row provenance SURVIVES. The entry's label is overstated: it should read
"package entry rewritten; headline replaced on S158/S001", so the admit is not read as uptake
of the package's thesis.

## Scratch and tooling

- Scratch file: `/tmp/tameshi-r42w2-CriticAssimilation-zenn.html`, deleted before return.
- No installs or updates. Used curl, grep and sha256sum, all already present.

BROKEN: the cjk "sibling theme" reason is contradicted by the frozen candidate list (contract.json:53-58) and by the admitted entry's denominator text; the survivor refusal holds only on duplication, since its quote-drift and recheck reasons are repairs the round made on the admitted entry; S158 is disclosed, but "assimilated" overstates an entry whose headline rests on non-package S158.
