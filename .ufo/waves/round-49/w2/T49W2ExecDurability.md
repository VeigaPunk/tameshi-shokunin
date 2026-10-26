# T49W2ExecDurability — C1 durability probe at `f181a961`

Attacks the durability clause of C1's predicate (`contract.json`, C1.predicate):

> "At REV the unchanged round-21 cold-read monitor credits every section with
> calibration_restraint_score 8, still credits every section after one line is appended to each
> of the five record files …"

and the work-plan sentence that the re-key makes the seven sections' credit survive a later
record append ("record files are read through git blobs, so a later record append does not lapse
them"). No counter was run; every number below is a monitor reading, not a verdict.

## Method (exact)

Scratch clone of the lane at the candidate revision; no write to the lane checkout except this
report and the receipts directory.

```
S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecDurability
git clone --shared -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"
git -C "$S/lane" checkout -q f181a961ae44061af486f600e5ea257d2baf78f8
git -C "$S/lane" rev-parse --show-toplevel      ->  $S/lane      (asserted before every commit)
cd "$S/lane" && TMPDIR="$S" python3 .ufo/evidence/round-21/coldread/measure.py --repo "$S/lane" --rev HEAD
```

Commits used only `git -c user.name=durability-probe -c user.email=probe@invalid commit`; no
config file was written. Every run exited 0 with `"overrides_used": false` and
`"trace_gate": "strict"` (receipts `monitor-*.json`).

The monitor is the round-21 selector over the round-18 algorithm: it pins the ledger and adds it
to the ignored inputs (`.ufo/evidence/round-21/coldread/measure.py:109-113`), then delegates
(`.ufo/evidence/round-18/measure.py:1-88`). Credit is resolved per section by section-body
sha256 → matching ledger entries (`.ufo/evidence/round-18/measure.py:602-612`), each entry's
`inputs` (minus `IGNORED_INPUTS`, `.ufo/evidence/round-18/measure.py:135`) must all hash-match at
REV (`.ufo/evidence/round-18/measure.py:321-370`), and the section is covered iff at least one
entry credits and no non-stale failure vetoes (`.ufo/evidence/round-18/measure.py:627-638`).
`LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md` and `corpus/README.md` are not
ignored — durability therefore hangs on whether each crediting entry records them.

## Results per case

| case | tree (clone commit) | covered | score | lapsed sections |
|---|---|---|---|---|
| base | `f181a961ae44061af486f600e5ea257d2baf78f8` | **64/64** | **8** | none |
| A: +1 appended line to each of the five records | `2e825e920f9351c1a5c2e11b4993f7e9669c2351` | **64/64** | **8** | none |
| A+D: a second appended line to each of the five records | `a627d6049c1b19cf0f3b231f9b285ea2acb10c50` | **64/64** | **8** | none |
| B: edit the recipe's cited note `corpus/knowledge/mutation-case-kimi-census.md` | `8389d56172b5d36830fd33ecb68a4bead71ce277` | **54/64** | **6** | 10 (below) |
| C: edit `corpus/knowledge/mte-report-interop.md` (recorded by one section only) | `7f3d758fe71d23e3744aa15a2ff6ff63d2d8933d` | **64/64** | **8** | none |
| F: edit `corpus/knowledge/service-limits.md` (extra probe) | `6f31e2dd04809c4c475464facb5960c2c5160ec2` | **60/64** | **6** | 4 (below) |
| base 8ca67421, no append | `8ca67421111fa354b47b803358391d0b07fc6db9` | **57/64** | **6** | 7 (the seven targets) |
| base 8ca67421 + one append per record | `4227bc1de299f4be2ab6ef58981de0c0b5ca20b7` | **57/64** | **6** | same 7 |

All case receipts: `.ufo/waves/round-49/w2/receipts-T49W2ExecDurability/` (`monitor-base.json`,
`monitor-caseA.json`, `monitor-caseB.json`, `monitor-caseC.json`, `monitor-caseD.json`,
`monitor-caseF.json`, `monitor-base8ca.json`, `monitor-baseAppend.json`, the four case commit
diffs, `seven-entries-at-f181a96.txt`, `escape-analysis-at-f181a96.txt`, `commands.txt`).

## Case A / D — a record append lapses nothing (the expected half holds)

Observed, after committing one appended line to each of `LOG.md`, `SCORECARD.md`,
`corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`:

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo "$S/lane" --rev HEAD
coldread covered 64 / 64  score 8  reasons {"credited": 64}     monitor-caseA.json
coldread covered 64 / 64  score 8  reasons {"credited": 64}     monitor-caseD.json (second append)
```

All seven target sections are `credited` in both runs: starts 131, 375, 1380, 1464, 1479, 1517,
1563 (per-section rows in the receipts). Ancillary blocks are byte-identical across A and D:
`sources` rows 130, malformed 0; `shonen` unchanged; `depth_score` 9.

Structural reason, not an accident of this append:

* Each of the seven sections has **exactly one** matching ledger entry, the round-49 re-key entry
  at `.ufo/evidence/round-21/coldread/ledger.json:40299` (recipe, `skill_sha256` line 40300),
  `:40339`/40340 (restore), `:40372`/40373 (map), `:40413`/40414 (promotion),
  `:40446`/40447 (r12), `:40478`/40479 (r13), `:40514`/40515 (r14) (`seven-entries-at-f181a96.txt`).
* None of those seven `inputs` maps contains any of the five record files — verified by set
  intersection on the ledger at `f181a96`: `records=[]` for all seven. All non-record inputs
  verify at every probed REV (that is what the 64/64 says at entry level).
* The re-key therefore does what it claims: the seven sections' credit is *structurally* immune
  to record drift, not merely currently lucky.

The flip side, observed and worth stating: three of the seven still cite records in prose while
no longer recording them — `SKILL.md:156` (recipe: `corpus/README.md`), `SKILL.md:397-398`
(restore: `SCORECARD.md:13`, `SCORECARD.md:16`), `SKILL.md:403` (restore: `corpus/README.md`),
`SKILL.md:1392-1394` (map: `corpus/README.md`, `LOG.md`, `SCORECARD.md`). After the re-key a
rotten README/LOG/SCORECARD can no longer lapse these sections at all; the only remaining tie is
`reads.json`. That is the intended trade, but it means "durable" here == "record edits are
invisible to the credit mechanism".

## Case B — the recipe's cited note edit lapses the recipe and restore (expected)

Edit committed: one appended line to `corpus/knowledge/mutation-case-kimi-census.md`.

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo "$S/lane" --rev HEAD
coldread covered 54 / 64  score 6      monitor-caseB.json
```

Lapsed headings (start, heading, first reason token; full reason lists in the receipt):

| start | heading | reason (first) |
|---|---|---|
| 6 | `# tameshi-shokunin` | `input-drift:corpus/knowledge/mutation-case-kimi-census.md` |
| 17 | `## Standing rules` | `input-drift:.ufo/evidence/round-18/measure.py;…` |
| 30 | `## Source notes` | `input-drift:corpus/knowledge/mutation-case-kagi-census.md;…` |
| 131 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | `input-drift:corpus/knowledge/mutation-case-kimi-census.md` |
| 246 | `## Defect-taxonomy templates and exact-string guidance` | `input-drift:corpus/knowledge/mutation-case-kagi-census.md;…` |
| 314 | `## Kill-rate bands — admission readings (rounds 2–3, measured)` | `input-drift:PROVINCE.md;…` |
| 375 | `## Restore discipline — before/after identity, not continuous non-write proof` | `input-drift:corpus/knowledge/mutation-case-kimi-census.md` |
| 405 | `## Cross-language divergence — bash vs JS (round 3, measured)` | `input-drift:corpus/knowledge/mutation-case-kimi-census.md` |
| 527 | `## Appendix A — worked example: JS case …` | `input-drift:corpus/knowledge/mutation-case-kimi-census.md` |
| 1092 | `### Six-case confidence statement (round 8, measured)` | `input-drift:corpus/knowledge/closeout-r11.md;…` |

Reconciliation with the ledger (`escape-analysis-at-f181a96.txt`): 12 sections record this note
as an input — 6, 17, 30, 131, 246, 314, 375, 405, 527, 1092, 1155, 1814. Ten lapsed; **1155 and
1814 escaped** because each has a non-citing matching entry whose *whole* input set still verifies
(1155: `tools/trace-inputs.py`; 1814: a 26-input set that excludes the note). So the exact
relation is not "every section citing it lapses" but:

> a cited-file edit lapses exactly those citing sections that have no non-citing crediting entry
> whose full recorded input set still verifies at REV.

Eight of the twelve cite the note in prose (17, 30, 131, 246, 314, 375, 405, 527) and all eight
lapsed; 6 and 1092 lapsed on the recorded input alone.

## Case C — an edit that lapses nothing (counter-example to the naive expectation)

`corpus/knowledge/mte-report-interop.md` is recorded by exactly one section (2132) and is not
cited in prose. After the edit: `covered 64 / 64 score 8`, section 2132 still `credited`
(`monitor-caseC.json`). Section 2132 has three matching entries; only one records the note, and a
`tools/*`-only entry fully verifies, so the edit is invisible to credit. Same mechanism as the
1155/1814 escapes.

## Case F — prose-cited note edit, extra probe

`corpus/knowledge/service-limits.md` (prose-cited by 1246, 1281, 1380 and 1449; recorded by the
map's round-49 entry and by earlier entries). Observed: `covered 60 / 64 score 6`; lapsed 1246,
1281, **1380 (the map)**, 1449 (`monitor-caseF.json`) — i.e. all four prose-citers. Escapes: 17,
921, 1092, 1155. This confirms (a) the map's re-keyed entry is tied to its cited notes and lapses
when one changes, and (b) the escape model predicts the lapse set exactly for a second,
independent note.

## Case E-base — what the re-key bought (before/after at the same append)

```
base 8ca67421                : covered 57 / 64  score 6   monitor-base8ca.json
base 8ca67421 + one append   : covered 57 / 64  score 6   monitor-baseAppend.json
```

The append changed nothing at base (lapsed set identical before and after). The base seven were
already uncovered, and their `missing` reasons at base are record/tool drift
(`monitor-base8ca.json`, starts 131/375/1380/1464/1479/1517/1563, e.g. 131:
`input-drift:LOG.md;input-drift:SCORECARD.md;input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;…`).
So the round's durability increment is: seven sections that carried live-and-lapsing record-keyed
entries at base now carry record-free entries and credit through appends (57/64 → 64/64 at the
same probe).

## Risks and limits

1. **Single-entry credit is brittle in the other direction.** Each of the seven has exactly one
   entry, so any edit to a recorded non-record input lapses it (Cases B, F). "Durable" must be
   read as record-durability only; a cited-note edit still lapses, as the item expected.
2. **Fail-open escapes exist outside the seven.** Sections 2132 (C), 1155/1814 (B) and
   17/921/1092/1155 (F) keep credit while a file their prose or a sibling entry cites changes,
   because a non-citing entry fully verifies. This is the same mechanism the re-key relies on,
   and it means the monitor under-reports staleness for those sections. Model and instance list:
   `escape-analysis-at-f181a96.txt`; counts derived from the ledger at `f181a96` only.
3. **Record prose citations in the seven are now outside the ledger gate** (`SKILL.md:156`,
   `:397-398`, `:403`, `:1392-1394`); a future record rot in those files cannot surface here.
4. Appends were committed; the monitor reads REV blobs, so an uncommitted append cannot move any
   number (not probed, implied by `.ufo/evidence/round-18/measure.py:44-56` `git ls-tree REV`).
5. Scope: monitor probes only. No `c1/measure.py` invocation, no controls scored, no `--explain`
   runs; the rounds' deciding run is the L1's.
6. No tools installed or upgraded.

## Summary

- Durability holds at `f181a961`: base 64/64 score 8; after one committed line appended to each of the five record files 64/64 score 8; after a second round of appends still 64/64 score 8 — all seven targets credited.
- Mechanism is structural: each of the seven sections has exactly one round-49 entry, and none of those `inputs` maps contains a record file (`ledger.json:40299-40559`).
- A cited-note edit still lapses: `mutation-case-kimi-census.md` → 54/64 score 6, losing 131 recipe and 375 restore as expected, plus 8 other citing sections.
- The "exactly the sections citing it" shape needs one qualifier: 1155 and 1814 cite the note yet keep credit through a fully-verifying non-citing entry; same mechanism makes case C a 64/64 no-op.
- Case F (`service-limits.md`) → 60/64, lapsing the map (1380) plus 1246/1281/1449 and escaping 17/921/1092/1155, matching the escape model exactly.
- At base the same five-record append was inert (57/64 → 57/64); the seven were already lapsed on record/tool drift, so the re-key is what converts them to record-immune credit.
- Residual risk: three of the seven still cite records in prose without recording them, and the fail-open escape paths sit outside the seven; both are recorded above with coordinates.
