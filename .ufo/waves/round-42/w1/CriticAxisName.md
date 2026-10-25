# CriticAxisName — round-42 w1 — axis-label attack (C1, C2)

seat: `L1Tameshi42.CriticAxisName` · role: critic · date 2026-10-25
scope: the axis labels in `.ufo/evidence/round-42/contract.json` only. Read-only; no edits to the
lane, no counter runs consumed (`--rev base`/control receipts were read from committed bytes; the
kill rules' one deciding run stands un-run — this is wave 1 build).

Rule applied (located): `scripts/hyaku/lane-addendum.md:233-237` — "Name the axis by the surface
the round changes, not by the number it produces (kaidoku r29). Re-scoring a rule the lane
already holds on new inputs, or counting rows a sourceless fixture also counts, is quality work,
never coverage or depth. A coverage claim names the surface it moves (frontier → core, a new
tool, operation or edge class) and the command that would show it unmoved." (accessed 2026-10-25)

---

## Verdict C1 — **calibration, AGREE** (not quality)

The claimed surface is the lane's self-assessment record layer agreeing with the tree — the
calibration axis's definition verbatim: `AXES.md:15` "**calibration** | Self-assessment quality:
gaps named honestly, confidence graded, overreach caught | SHONEN.md/SCORECARD entries match
observed repo state". The contract statement (`contract.json:15`) restates exactly that
("the lane's self-assessment records agree with observed repo state…").

Evidence:

- The live mismatch is real and present at the base. Verified: `git -C tameshi-shokunin
  ls-tree -r --name-only c77c2b7e64d2e356381441ecf94abac03e984606 -- .ufo/waves/round-41/residual/`
  lists `.ufo/waves/round-41/residual/ResidualReceipts.md`, while `receipt.json:16` asserts
  `"present": false` for it — the m10 disagreement the round must repair (superseding receipt).
  `before/c1-at-base.stdout` shows `m10=1 records=3 total=1 C1_R42_PASS=false`.
- Not quality: the round does not re-score a held rule on new inputs; it *changes* the record
  layer (the superseding receipt must re-assert the path truthfully, and the round-42 records
  must exist). The do-nothing control proves the target is unreachable without the repair:
  `control/c1-do-nothing.stdout` (records=6, no superseding receipt) keeps `m10=1`.
- The low-axis routing is coherent with the same definition: `contract.json:10` stagnation nudge
  names calibration as the lowest non-retired axis; round-41's C1 (`contract.json` r41:13-15)
  worked the same axis with the same statement shape, and m6/m7/m8/m10/m11 all audit the
  self-assessment records (SCORECARD standing row, S-id citations, path citations, wave-receipt
  presence, revision reachability) against observed repo state.

## Verdict C2 — **depth, AGREE** (not quality; not coverage)

The changed surface is the write-path census's *resolution model* — what it can decide about a
write destination — plus the knowledge entry carrying the mechanism. That is the depth axis's
domain: `AXES.md:11` "**depth** | Verifiable technical detail — decision tables with real
thresholds, named error signatures, cited sources". The round's own `surface` field
(`contract.json:35`) is the successor vertex of a documented gap, not a new province surface:

- The three live false positives C2 must resolve were disclosed in the round-41 knowledge entry
  as resolution-mechanics gaps: `corpus/knowledge/r41-variable-destination-writes.md:48-63`
  — `tools/context-capture.py:1682/:1685` are "scratch in fact" but `_bind` records plain
  `Name` targets only, so `self.root` never enters the environment ("the fix (dotted-attribute
  binding plus a completeness flag…)"); `tools/registry-replay.py:123` is "a real non-scratch
  write … explicit output flag is not in the update-flag pattern". C2's predicate measures the
  mechanics: resolved text naming `mkdtemp`/`--out` (constant tables cannot satisfy), 10/10
  fixtures, mutant classes attr/method/outflag each killed (census/measure.py:35-40).
- Not quality: the controls show the target cannot be met by re-scoring or sourceless counting —
  `control/c2-v3-in-slot.stdout` fails F01/F04 and all three live sites under the unchanged v3
  (fixtures_pass=8/10); `control/c2-junk.stdout` fails F02/F03/F05–F09 for a junk tool.
- Not coverage: no PROVINCE frontier→core movement is claimed; the round deepens the analysis
  *within* the existing F4 write-path ground (the lane's own coverage-map rows already bookkeep
  v2/v3 under F4, `corpus/README.md:519-523`). Lane precedent rules this depth: round 12's
  closure — "reanalysis of the same bash target is depth within a case, not a new independent
  case" (`SCORECARD.md:291`); round-36's critic — a change to "what it checks — the decision
  content" is depth (`round-36/w1/CriticC2Scope.md:33-36`). Lineage is consistent: r40 C1
  (v2), r41 C2 (v3) and r42 C2 (v4) all tag this family depth + capability acquisition.

## Honest limits

- The deciding runs have not happened (wave 1 build): `tools/write-path-census-v4.py`,
  `corpus/knowledge/r42-attribute-and-outflag-destinations.md`, the argparse SOURCES row and
  `mutants.json` do not exist yet at the tip; axis labels are judged on the frozen contract and
  committed evidence only.
- The only contestable reading is C2-as-coverage via the literal "new tool / edge class"
  phrase in the addendum. Rejected on the surface rule because the round claims no province
  movement and its measurement is entirely resolution detail; if a judge insisted on that
  reading, the smallest safe correction would be retagging C2 `coverage` and naming the F4
  move explicitly — but that would require a post-freeze amendment and would break the lane's
  consistent v2/v3/v4 convention without changing the work.

## Commands / reads

- `read` `.ufo/evidence/round-42/contract.json`; `before/{c1-at-base,c2-at-base}.stdout`;
  `control/{c1-do-nothing,c2-v3-in-slot}.stdout`; `census/measure.py`, `calibration/measure.py`
  (headers); `.ufo/evidence/round-41/contract.json`; `SCORECARD.md`; `corpus/README.md:513-523`;
  `corpus/knowledge/r41-variable-destination-writes.md:48-63`; `AXES.md`; `scripts/hyaku/lane-addendum.md:233-237`.
- `git -C tameshi-shokunin ls-tree -r --name-only c77c2b7… -- .ufo/waves/round-41/residual/`
  → lists `ResidualReceipts.md` (present at base) alongside `receipt.json` asserting false.
- `git -C tameshi-shokunin ls-tree -r --name-only c77c2b7… -- tools/ | grep -i census`
  → v1/v2/v3 only (v4 absent at base, as expected for build).
