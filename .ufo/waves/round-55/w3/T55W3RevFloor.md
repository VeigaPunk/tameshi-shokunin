# T55W3RevFloor — floor re-derivation at base and C0

Seat `T55W3RevFloor` (reviewer, L1 `TameshiR55`), wave 3, axis calibration, milestone "floor arithmetic".
Read-only over the lane: every number below comes from git objects at the named revision; no lane
production file, frozen file or wave spec was edited. Receipts:
`.ufo/waves/round-55/w3/T55W3RevFloor-receipts/`.

## Verdict

| revision | sections | credited | `calibration_restraint_score` | `box3_full_page` | depth | cases |
|---|---|---|---|---|---|---|
| base `0a2010acd1e9` | 64 | **64** | 8 | true | 10 | 10 |
| C0 `9cf0146b94dd` | 64 | **46** | 6 | false | 10 | 10 |
| HEAD `4f7a7040a57e` | 64 | **46** | 6 | false | 10 | 10 |

- The floor drops **64 → 46 (−18, 0 gained)**; the round-48 precheck exits **1 (`RED`)**, `lost=18`.
- The lost set is **set-equal** to `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` (18 headings,
  no measured-only and no recorded-only heading).
- **Every loss is attributable to a file this round changed.** 17 losses are `input-drift` and every
  newly drifted path is one of the six content files in `git diff --name-only base C0` that the
  round edited (`corpus/SOURCES.md`, `tools/registry.json`, `tools/context-capture.py`,
  `tools/registry-check.py`, `tools/repeat-control.py`, `corpus/QUALITY.md`); the 18th
  (`## Standing rules`) is `no-ledger-entry`, caused by the round's own `SKILL.md` byte change.
  No loss traces to an unchanged file, and no loss carries a non-`input-drift` failure token
  (no `trace-*`, `input-missing`, `input-not-blob`, `commands-*`, `verdict:*`).
- The floor at HEAD equals the floor at C0 exactly (same 18 headings, same per-section `reason`
  strings). Post-C0 commits changed only `.ufo/evidence/round-55/**` (frozen counters, binder,
  resolutions, `lost-headings-at-c0.json`), none of which any credit-carrying ledger entry pins.
- The 18 wave-3 reader seats `T55W3R01`–`T55W3R18` name exactly the 18 lost headings (set-equal,
  no duplicates, no reader without a loss, no loss without a reader).

No attribution finding. Two record-wording observations and the verification gaps are below.

## Commands and output

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; scratch
`$HYAKU_SCRATCH/tameshi-r55/T55W3RevFloor` (removed on exit, `trap` on that directory only).

```
python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 0a2010acd1e92e4e332774050825e21bcfc7e079
# exit 0: sections_total=64 sections_covered=64 score=8 box3_full_page=true
#         reasons={"credited": 64} missing=[]
python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
# exit 0: sections_total=64 sections_covered=46 score=6 box3_full_page=false
#         18 uncovered (1 no-ledger-entry, 17 input-drift)
python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4f7a7040a57e7aed17db941be9c27b300aafb783
# exit 0: sections_total=64 sections_covered=46 score=6 box3_full_page=false
#         lost set and every per-section reason identical to C0

bash .ufo/evidence/round-48/quality/coldread-precheck.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 0a2010acd1e92e4e332774050825e21bcfc7e079 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
# exit 1
# COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=9cf0146b94dd cand_credited=46 lost=18 RED
```

Full precheck output (18 `LOST` lines with the union drift set): `T55W3RevFloor-receipts/precheck.stdout`.
Summary of the three measure runs: `T55W3RevFloor-receipts/measure-summary.txt`.
The ledger blob is byte-identical at base and C0
(`sha256 24dbe99a57880705313a8ddc05ddcdc05c57754903822912c0dbd7480499a5c7`, 10572761 bytes at both),
so no entry changed between the revisions — only the tree did.

## The lost set (18) and the recorded file

`## Context gate classification and explicit exit classes — round 15`,
`## Effective expectation reconciliation — round 14`,
`## Live-tree re-pin and entry-command monitor — round 17`,
`## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`,
`## Pin disposition and provenance correction — round 13`,
`## Repeated controls and gate registry — round 12`,
`## Standing rules`,
`## The leg ledger — replay, receipt, and how it is read (round 7, measured)`,
`## The operator's runbook and the six-leg regression (round 10, measured)`,
`### Gate/probe registry`,
`### Round-13 gate/probe registry`,
`### Round-15 gate/probe registry`,
`### Round-17 gate/probe registry — re-pin and monitor`,
`### Round-18 gate/probe registry — routed-defect closure`,
`### Round-21 gate/probe registry — finite environment differential`,
`### Round-26 gate/probe registry — report interop`,
`### The service's limits — what tameshi refuses to mutation-test`,
`### Triggers T1–T3 and the re-pin rule`.

Comparison with `.ufo/evidence/round-55/c1/lost-headings-at-c0.json`: `measured_lost=18
recorded_lost=18 measured-only=[] recorded-only=[] SET_EQUAL True`. It also equals
`coldread.uncovered_headings` and the heading set of `coldread.missing` at C0.

## Attribution — which entry stopped crediting, and why

The precheck's `drifted=` list is the **union over every matching entry**, so it names paths from
older entries that were already stale at the floor (`tools/bash-witness-study.py`,
`tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`,
`tools/trace-inputs.py`, `tools/env-diff.py`, `.ufo/evidence/round-15/verify.py`,
`corpus/knowledge/service-limits.md`) — those are **not** why credit was lost, and none of them
changed base→C0. Attribution therefore runs per entry: for each lost section, the entries whose
section `sha256` matches, evaluated with the frozen `entry_reason()` at base and at C0
(`T55W3RevFloor-receipts/attribute.py`; result table `T55W3RevFloor-receipts/attribution.txt`).

Result: **exactly one entry per lost section was clean at base and fails at C0**, and it is always
the round-54 re-key entry (seat `T54W2ReadNN`, `read_rev=99c3bc88d704` = round-54's C1 fix pass,
`"L1 TameshiR54a2 re-key (round 54)"`), failing with `input-drift` only. Per-heading causal inputs
(all in the base→C0 diff):

| lost heading | causal (newly drifted) inputs |
|---|---|
| `## Context gate classification … round 15` | `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry.json` |
| `## Effective expectation reconciliation — round 14` | `corpus/SOURCES.md`, `tools/context-capture.py` |
| `## Live-tree re-pin … round 17` | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| `## Mutation-sweep recipe …` | same six |
| `## Pin disposition … round 13` | `corpus/SOURCES.md` |
| `## Repeated controls … round 12` | `corpus/SOURCES.md`, `tools/repeat-control.py` |
| `## The leg ledger … (round 7)` | `corpus/SOURCES.md` |
| `## The operator's runbook … (round 10)` | `tools/registry.json` |
| `### Gate/probe registry` | `tools/repeat-control.py` |
| `### Round-13 gate/probe registry` | `corpus/SOURCES.md` |
| `### Round-15 gate/probe registry` | `tools/context-capture.py` |
| `### Round-17 gate/probe registry …` | `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| `### Round-18 gate/probe registry …` | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry-check.py`, `tools/registry.json` |
| `### Round-21 gate/probe registry …` | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry-check.py`, `tools/registry.json` |
| `### Round-26 gate/probe registry …` | `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| `### The service's limits …` | `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| `### Triggers T1–T3 and the re-pin rule` | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py` |
| `## Standing rules` | none — `no-ledger-entry`: 0 entries at the C0 section sha; the round's `SKILL.md` edit changed the section bytes (`61736dce…` start 17 end 40 → `acfb671a…` start 17 end 44) |

Frequency over the 17 input-drift losses (`T55W3RevFloor-receipts/causal-paths.txt`):
`corpus/SOURCES.md` 12, `tools/registry.json` 10, `tools/context-capture.py` 9,
`tools/registry-check.py` 8, `tools/repeat-control.py` 8, `corpus/QUALITY.md` 5.
`LOG.md`, `SCORECARD.md`, `corpus/knowledge/scratch-root-contract.md`, `corpus/lessons/round-54.md`
and `corpus/lessons/round-55.md` also changed this round and are pinned by no clean entry of the 18,
so they cost no credit (neither cause nor protection for the floor).

Only one `SKILL.md` section changed bytes (`T55W3RevFloor-receipts/section-delta.txt`:
`sections base=64 c0=64`, `sections whose bytes changed: 1`), so the `no-ledger-entry` loss is the
round's own edit and not an unrelated drift.

## Score arithmetic

`calibration_restraint_score` is `2·(boxes 1,2,4 marked ~) + 2·(box3 ~ and full page)`; `SHONEN.md`
marks are `['~','~','~','~']` at both revisions. The 8→6 drop is **only** the box-3 term
(`box3_full_page` = `sections_covered == sections_total`): 6 + 2 → 6 + 0. It carries no information
beyond the coverage drop, and it returns with the 18 re-keys. `depth_score`/`recorded_cases` (10/10)
are untouched by the round.

## Observations (no attribution finding)

1. **Low — the round's floor sentence understates the obligation it created.** `LOG.md` at C0
   (line ~2550) says "The one SKILL.md section the edit drifts (`## Standing rules`) is re-keyed with
   a fresh reader at C0", and `no-harm.sh`'s header says "the cold-read floor … the re-key obligation
   this round carries for the one SKILL.md section its edit drifts". Both are literally true about
   `SKILL.md` bytes (exactly one section changed), but the round's operative floor obligation is
   **18** sections: 17 more forfeited because their round-54 entries pin the tool/registry/corpus
   files this round edited. The operational arms are right — `no-harm.sh` requires
   `score>=8 credited>=64`, and wave 3 stands up 18 readers that match the lost set exactly — so this
   is wording, not a missed obligation. Recommendation: the round report state the three numbers
   plainly (1 section's bytes changed, 18 sections forfeited, 18 re-keyed) and not repeat "one
   section" as if it were the whole obligation. `no-harm.sh` is frozen; if the wording matters, it
   needs an amendment, not an edit.
2. **Informational — the recorded lost-set file is not revision-bound.** `.ufo/evidence/round-55/c1/lost-headings-at-c0.json`
   is tracked at HEAD (`4f7a704`, added by amendment 9) but **absent at C0** (`git cat-file -t
   9cf0146:.ufo/evidence/round-55/c1/lost-headings-at-c0.json` → `exists on disk, but not in
   9cf0146`), so a reader pinned at C0 cannot open the file the wave-3 spec asks seats to compare
   against. Its content is correct (set-equal to the measurement above), and the contract does not
   list it among the C1 frozen paths, so nothing in this round's claims depends on it; a future seat
   that re-derives from C0 alone must recompute the set rather than read that file.
3. **Checked and clean — reader coverage.** 18 wave-3 reader seats, 18 distinct headings, set-equal
   to the lost set: no heading is re-read that did not lose credit and none lost credit without a
   reader. The three wave-2 readers and `T55W3R07` all read `## Standing rules`; that redundancy is
   the wave spec's design, not double-counting of the loss.

## Verification gaps / residual risk

- The measure reads git objects only, so the numbers are reproducible exactly; but credit is an
  *input-drift* signal. It cannot certify that the other 46 sections' statements remain **true**
  after this round's edits: five changed content files (`LOG.md`, `SCORECARD.md`,
  `corpus/knowledge/scratch-root-contract.md`, `corpus/lessons/round-54.md`,
  `corpus/lessons/round-55.md`) are pinned by no clean entry of the 18, so their edits neither cost
  nor restore credit. Truth of those records is the job of the record/attribution seats, not of the
  floor.
- Base `64/64` is carried by round-54 entries (`read_rev 99c3bc88d704`). The floor therefore
  measures ledger maintenance as much as reading; that is the mechanism question owned by the
  re-key-mechanism seat and is not re-argued here.
- I measured at C0 and HEAD; I did not measure the eventual PIN (it does not exist yet). If the PIN
  edits any of the six causal paths again, this table's causal sets go stale and the binder's
  re-keyed entries drop with them.
- This task needed no semantic code navigation: the sources are git objects, the frozen measure, and
  the precheck script; no LSP server was consulted and none would add evidence about object bytes.
  Shell text search was used only for locating record sentences, never as proof of a credit verdict.

## Artifacts opened

- `.ufo/evidence/round-21/coldread/measure.py` (selector; `LEDGER`, `FORBIDDEN_OVERRIDES`, selftest)
- `.ufo/evidence/round-18/measure.py` (`sectionize`, `coldread`, `entry_reason`, `entry_is_stale`,
  `input_failures`, `input_reason`, `trace_reason`, `measure`)
- `.ufo/evidence/round-48/quality/coldread-precheck.sh`
- `.ufo/evidence/round-21/coldread/ledger.json` (blob at base, C0 and HEAD)
- `.ufo/evidence/round-55/contract.json`, `no-harm.sh`, `c1/lost-headings-at-c0.json`
- `.ufo/waves/round-55/spec-w2.json`, `spec-w3.json`, `w1/T55W1Er10.json`, `w1/T55W1Er10.md`,
  `w2/T55W2ScoutColdread.md`
- `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
  `tools/registry.json` (blobs at base / C0 as needed)

No tools installed or upgraded (no channel used; nothing was missing).

Receipts: `T55W3RevFloor-receipts/{measure-summary.txt, precheck.stdout, attribution.txt,
causal-paths.txt, section-delta.txt, attribute.py}`. The measure JSONs (3 MB each) stay out of the
lane; they are regenerated by the commands above.
