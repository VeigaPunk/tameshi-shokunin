# T53W1ScoutAssim — assimilation-gate audit for `corpus/knowledge/change-aware-resweep-cadence.md`

Seat: T53W1ScoutAssim (wave 1 scout, round 53, hyaku run 10, L1 TameshiR53a2)
Item: independently audit the five assimilation gates for the round-53 entry
`corpus/knowledge/change-aware-resweep-cadence.md` (assimilated from the
shokuknow `merge/tameshi` package, staged S161/S162 → adopted S275/S276).
Work was read-only; no lane file was edited. All commands were run against
the working tree at the wave-1 tip; the entry bytes audited are the current
lane corpus bytes.

## Audit table

| # | Gate | Verdict | Evidence (command → result) |
|---|------|---------|------------------------------|
| 1 | PROVINCE scope — mutation cadence is verification-fixture craft, in scope | **HOLD** | `PROVINCE.md` Domain names "verification-fixture craft — the reusable method of honest checks: hermetic suites, **mutation testing**, fail-closed arms, verdict-line discipline…"; the Frontier clause names exactly this entry form ("ground moves to Core only through an admitted, source-headed `knowledge/` entry whose `source:` cites a `mined` `SOURCES.md` row"). The entry is a re-sweep-cadence (when to recompute vs pin a mutant suite) policy entry for the lane's own gates — craft, not product domain. No sibling gate code is touched; no product clause absorbed. |
| 2 | QUALITY bar — every claim cites a source, boundaries stated | **HOLD with one minor finding** (see F1) | Every evidential claim carries a source; quotes re-verified verbatim against the round's snapshots (below). Boundary section states: both sources are Java studies (numbers not transferred); ACM copy access-controlled so camera-ready is the opened artefact; staged-id provenance; "What is still open" names the unmeasured F7 classification. One citation does not establish its clause: the `(S101)` cross-reference (finding F1). |
| 3 | Coverage ground — README F7 row was open; entry's ground reads F7 | **HOLD** | `grep -n "F7" corpus/README.md` → frontier table row (line 84) and round-51 restated table (line 622) both read `open` (`before: pin-level cadence only → after: per-leg reuse decisions classified: not reached`); the round-53 addendum (`README.md:636-646`) records the acquisition with "The frontier row stays `open`". Entry front-matter: `ground: F7 (incremental re-sweep granularity)`. Row was and remains open; the entry records policy ground, not the classification. |
| 4 | id renumber — staged S161/S162 re-pointed to S275/S276 by document (URL identical, id follows); no other staged id appears in the lane corpus | **HOLD** (with documented history note) | Staged package rows (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:15-16`): staged S161 = DOI `10.1145/3540250.3558911`, staged S162 = `arxiv.org/abs/2212.11762`. Adopted rows (`corpus/SOURCES.md:150-151`): S275 = same DOI, S276 = same arXiv URL. URLs identical, ids follow the registry continuation (`SOURCES.md:508` next-unused S275 → `:509` next-unused S277). Collision census (`.ufo/evidence/round-53/assimilation/collisions`) lists only S153–S160; S161/S162 were free. Both sources re-opened by the L1 this round: snapshot sha256 `4d755c4e…` (S161-camera-ready.pdf, 131622 B) and `d6dc4cf6…` (S162-arxiv.html, 41423 B) match the registry rows. Corpus-wide grep for the staged range `S1[6-9][0-9]\|S2[0-4][0-9]\|S25[0-5]` finds staged ids only as provenance tokens (`staged:S159/S160`, `staged S167`, `staged S203`, `staged:S166/S156/S163-S165`, round-38/39/42/44 lesson history) and in this entry's adoption note — never as a source citation in any knowledge entry. **History note (not a defect):** `lessons/round-39.md:18` records an earlier package state where staged S161/S162 were the TensorFlow Federated golden_tests documents, re-pointed then to S107/S108; the staged namespace was re-issued in a later package regeneration (round-44 census already covers a different S153–S255 content map). The map is by document, so both records stand; the round-53 adoption note ("staged as S161 by corpus-expansion-1, re-pointed by document") is accurate for the package as it stands. |
| 5 | Entry cites ONLY S275/S276 | **HOLD** (nuance recorded) | Front-matter `source:` rows: S275, S276 only. Body: all quoted spans attribute to S275 or S276. No other registry source is cited as evidence. Two non-evidential appearances: `S101` inside the Inference clause "the lane's pin-level cadence (S101)" (cross-reference, flagged in F1), and staged ids `S161`/`S162`/`S161–S255` in the boundary adoption note (provenance, not citations). No other staged id is cited anywhere in the entry. |

## Quote verification (gate 2 evidence)

S276 against `.ufo/evidence/round-53/assimilation/S162-arxiv.html`:

- "Much previous work implicitly assumed it to be sufficient to re-compute
  mutant suites per release. Sadly, this makes mutation results inconsistent;
  mutant scores from each release cannot be directly compared" — present,
  abstract, verbatim (3 hits for the "re-compute mutant suites per release"
  tail).
- "will naturally degrade over time" — present, verbatim.
- "143,500 mutants in 4 non-trivial systems finding that, on overage, 52%
  degrade" — present, verbatim. Note: "on overage" is the **paper's own
  typo** in the arXiv v1 abstract; the entry is byte-faithful to the source.

S275 against `.ufo/evidence/round-53/assimilation/S161-camera-ready.txt`:

- "by selecting only subsuming commit relevant mutants, we reduce the number
  of mutants requiring analysis by around 93% on average" — present,
  verbatim, abstract.
- "around 30% of mutants are commit-relevant" — the paper prints this; the
  pdftotext extraction drops the line-break hyphen ("commitrelevant" in the
  raw txt). Extraction artifact; the entry's quote is faithful to the
  printed form.
- "69% of the mutants" / "outside the changed methods" — present, verbatim
  ("69% of the mutants are located outside the changed methods").

## Findings

**F1 (minor, class: imprecise cross-reference / citation-not-establishing).**
The entry's inference clause states:

> "Inference: the lane's pin-level cadence (S101) is the 'stable suite'
> branch; its cost is that relevance decays silently, and its benefit is
> that scores stay comparable."

S101 (`corpus/SOURCES.md:109`) is the Major Mutation Framework
(mutation-testing.org) overview; its `teaches` is "mutation-framework
feature set incl. equivalent-mutant handling", and its pinned snapshot
(`.ufo/evidence/round-34/src/s101-mutation-testing.html`, 4341 B) contains
**zero** occurrences of `incremental`, `cadence`, `pin`, `re-run`, `rerun`,
or `suite` (word counts over the extracted text: all 0). S101 does not
establish the lane's pin-level cadence. The cadence ground the README F7 row
actually names is S003 (StrykerJS incremental verdict reuse; used by
`knowledge/incremental-pin-disposition.md`), with S008 (Google diff-scoped
mutation) as the other F7 candidate. The inference itself stands without the
parenthetical; the citation is the wrong pointer and is exactly the class
the round's drafted QUALITY 104 targets ("a citation whose receipt does not
establish the cited clause"). Suggested repair (L1's call, not applied by
this seat): re-point `(S101)` → `(S003)` or to the round-13 disposition
entry.

## Checks run

1. Read the entry and its front-matter (`corpus/knowledge/change-aware-resweep-cadence.md`).
2. Located the F7 row and the round-53 addendum in `corpus/README.md` (lines 84, 622, 636–646).
3. Read `PROVINCE.md` Domain/Owns/Refuses/Core/Frontier clauses.
4. Verified all quoted spans against the round's snapshots under `.ufo/evidence/round-53/assimilation/` (S161-camera-ready.txt, S162-arxiv.html), including the source-typo nuance and the pdftotext hyphen-drop artifact.
5. Recomputed snapshot sha256 and byte sizes; matched `corpus/SOURCES.md:150-151` (S275 `4d755c4e…` 131622 B; S276 `d6dc4cf6…` 41423 B).
6. Read the staged rows at `shokuknow merge/tameshi/SOURCES.append.md:15-16`; confirmed URL identity with the adopted rows.
7. Read the round-53 id census artefacts (`staged-ids` = S153–S255; `reg-ids`; `collisions` = S153–S160 only) and the SOURCES.md next-unused-id progression (line 508 → 509).
8. Greped the whole lane `corpus/` for the staged-id range; classified every hit as provenance token / lesson history / explicit non-citation (e.g. `r8-flaky-cost-baseline.md:44` drops "S205" with no such registry row).
9. Checked the S101 pinned snapshot content for cadence vocabulary (zero hits).
10. Read `corpus/lessons/round-53.md` (the L1's own assimilation record) and `lessons/round-39.md:18` (staged-id history note).

## Remaining unknowns

- Whether the L1 wants the F1 pointer repaired in wave 2 (edit scope is the
  L1's; this seat is read-only over the corpus).
- The ACM 403 re-open receipt is recorded only as prose in
  `corpus/lessons/round-53.md:18-19` (no curl output file under
  `.ufo/evidence/round-53/assimilation/`); the claim is plausible and
  consistent with the camera-ready being the opened artefact, but this seat
  did not re-run the ACM fetch (lane is the mutating party's; seat stays
  read-only).

## Verdict

Gates 1, 3, 4, 5 HOLD. Gate 2 HOLDS with one minor finding (F1: the `(S101)`
cross-reference does not establish "pin-level cadence"; S003 is the registry
ground). The assimilation is otherwise honest: verbatim quotes, URL-identical
id renumber, staged namespace otherwise clean, boundary section complete.
