# T57W1ScribeItemsR56x1to4 — ledger rows R56.1-R56.4 (tameshi round 57, wave 1)

Lane base `5e3569969b532310d2b8a3d130901757a3df356b` (= the commit that added `corpus/lessons/round-56-verifier-spotcheck.md`; `git rev-list --count 5e35699..HEAD` = 0, so no later commit exists to fix anything).

## Verdicts

| id | status | fixability | one-line basis |
|---|---|---|---|
| R56.1 | open | fixable-costly (not staged) | SKILL.md:491 cites SKILL.md:335-339 for an 80 % passage; those lines hold other text. 167 bare SKILL line anchors across 32 corpus files. |
| R56.2 | open | fixable-costly (not staged) | SKILL.md:53 says RECEIPT_REV_MISMATCH for verdict + `--paths` drift; gate lines 148-151 emit RECEIPT_REV_CONTENT_DRIFT there. Fix uncredits `## Standing rules` (score 8→6). |
| R56.3 | open | fixable-cheap for the `recheck:` line (staged); README index line fixable-costly | knowledge file line 3 still requires `GATE_SELFTEST: 14/14 pass`; base gate and registry say 19/19. Entry indexed 0 times in corpus/README.md. |
| R56.4 | open | fixable-cheap via a recorded referent (staged note); ledger labels not re-bound | 13 of 18 bound ledger entries carry SOURCES/QUALITY labels that equal the blobs at 877eede, not C0. |

No row is `fixed` (nothing landed after base). No row is `declined`. No row is `unresolved`: every evidence excerpt was verified (below).

## Rows

`.ufo/waves/round-57/w1/T57W1ScribeItemsR56x1to4/rows.json` (4 rows; each has `keys`, `verdict_basis`, `fixability`, `fixability_detail`, `note`). The ledger schema fields are `id, status, evidence[{path,lines,excerpt}], seat, note` for `open`; `keys`, `verdict_basis` and `fixability*` are extra and are not ledger fields. Strip them before merging into `corpus/routed-defects.json`. The round-50 C1 rule ignores extra keys.

Each evidence excerpt was checked with the round-50 resolver, imported (not copied) from `.ufo/evidence/round-50/c1/measure.py`: `check_evidence(...)` returns `None` for all 13 items, and a separate direct check confirms each excerpt appears in the cited lines of the base blob (`receipts/r4-excerpt-verify.txt`, `ALL_EXCERPTS_OK True`). Every row has at least one keyed excerpt (`has_key`). Spans are at most 5 lines (`b - a <= 4`, limit 30) and excerpts are 15-400 characters.

Evidence paths: `SKILL.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/knowledge/receipt-revision-binding.md`, `tools/receipt-revision-gate.py`, `tools/registry.json`, `.ufo/evidence/round-21/coldread/ledger.json`. None is a spot-check, the ledger, or a round-50/57 C1/control file.

## Item detail

**R56.1 (open, costly).** Facts at base: `SKILL.md:491` reads "Band interiors were unprobed at round 3 (both at 80 %, SKILL.md:335-339)"; `sed -n 335,339p` holds "Shared survivor classes across the two cases…"; `grep -c '80 %'` on those lines = 0. `corpus/README.md:100` cites `SKILL.md:14-15` and `:133-135`. QUALITY criterion 34 (line 253) says a bare line anchor into a moving file expires with the next edit. Sweep: `git grep -E 'SKILL\.md:[0-9]+|SKILL:[0-9]+' 5e35699 -- corpus` = 167 lines in 32 files (`receipts/r3-skill-anchors.txt`). A fix is not cheap. Editing SKILL.md uncredits `## Standing rules` by one cell (measured below). Editing SKILL.md around line 491 touches `## Cross-language divergence — bash vs JS (round 3, measured)` (heading at SKILL.md:433). Editing the cited corpus files uncredits the headings that pin them (README: 6 headings measured below). Not staged.

**R56.2 (open, costly).** `SKILL.md:53` (row 53 of `## Standing rules`): "a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared `--paths` surface | `RECEIPT_REV_MISMATCH`". `tools/receipt-revision-gate.py:145-151`: `if paths is None:` gives MISMATCH; the `else:` branch gives `RECEIPT_REV_CONTENT_DRIFT` when the surface drifts. The one-cell fix is `RECEIPT_REV_CONTENT_DRIFT` (no `--paths`: `RECEIPT_REV_MISMATCH`), the same shape as row 54, with the same line count. Measured on probe rev `827e6554` (`receipts/r6-monitor-p1-skill-row53.json`): coverage 63/64, uncovered `## Standing rules`, score 8→6. Costly because SKILL.md is pinned. Not staged. The L1 should expect C2 to need this same `## Standing rules` re-key.

**R56.3 (open; split).**
- *Recheck line (cheap, staged).* `corpus/knowledge/receipt-revision-binding.md:3` says `python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 14/14 pass`. At base the selftest prints `GATE_SELFTEST: 19/19 pass`, exit 0 (`receipts/r2`). `tools/registry.json:1288` expects 19/19. The ER-R56-K2 errata (lines 224-229) says so but leaves line 3 unchanged. The staged line-3 edit (`… GATE_SELFTEST: 19/19 pass (ER-R56-K2)`) is at `stage/corpus/knowledge/receipt-revision-binding.md`. The patch is `stage-R56.3-recheck.patch` (1 line). No ledger entry pins this file (`receipts/r7`: 0 entries reference it). Measured on probe rev `585084b4`: 64/64, score 8 (`receipts/r6-monitor-p3-recheck-line.json`). Falsifier line 155 and the re-derive comment at line 166 still say 14/14. They are inside the entry body, so I left them for the L1.
- *README index (costly).* `corpus/README.md` has 0 lines naming the entry. A one-row insert after line 14 (probe rev `8f6a44d3`) gives 58/64, score 8→6. Six headings lose credit: `## Standing rules`, `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`, `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`, `### Triggers T1–T3 and the re-pin rule`, `### The map — where a reader enters, artifact by artifact`, `## Live-tree re-pin and entry-command monitor — round 17` (`receipts/r6-monitor-p2-readme-row.json`).

**R56.4 (open, cheap via referent).** `.ufo/evidence/round-21/coldread/ledger.json` entries 591-608 (18 entries, `external_inputs` labels `tameshi@c0137451…:corpus/SOURCES.md` and `…:corpus/QUALITY.md`). Mismatches: SOURCES 13 entries, QUALITY 6 entries; 13 of 18 entries carry at least one (`receipts/r5-referent.txt`). Every mismatched label equals `sha256(git show 877eedee:<path>)`: SOURCES `6c2096d8…a6d3`, QUALITY `54c49d38…aab7`. C0 is `c0137451` (ancestor of 877eede, which is an ancestor of the bind `c1dd23b3`; `receipts/r7`). Staged: `stage/.ufo/evidence/round-57/coldread-referent-r56.md`, which records the referent and does not change any pinned byte. Labels were not re-bound: `ledger.json` is pinned by 6 entries, so re-binding would uncredit those headings. The monitor does not verify `external_inputs` (round-18 `measure.py:605-608` only collects them), so the labels cost no credit.

## Monitor baseline and probes (round-21 cold-read monitor, `--rev` = the probe commit)

| probe | rev | coverage | score | note |
|---|---|---|---|---|
| base | 5e35699 | 64/64 | 8 | `receipts/r6-monitor-base.json` |
| p3 recheck line | 585084b4 | 64/64 | 8 | cheap |
| p1 SKILL row 53 | 827e6554 | 63/64 | 6 | `## Standing rules` lost |
| p2 README row | 8f6a44d3 | 58/64 | 6 | 6 headings lost |

The first p1/p2/p3 runs were made at base by mistake (`--rev` was the base). Their output is discarded and not cited. The repeat at each probe's own HEAD is the one reported.

## Staged (for the L1; copy under the lane, freeze after wave 1)

- `stage/corpus/knowledge/receipt-revision-binding.md` — full file, line 3 only changed (R56.3 recheck).
- `stage/.ufo/evidence/round-57/coldread-referent-r56.md` — new note (R56.4 referent).
- `stage-R56.3-recheck.patch` — diff of the knowledge file, against base bytes.

Nothing staged touches SKILL.md, README, QUALITY, SOURCES or any file pinned by a cold-read entry.

## Notes for the L1

1. `open` rows need R56.1-R56.4 named in the newest `**Planned (round 57)` paragraph of SCORECARD.md. The round-50 `planned_ids()` regex is `\bR4\d\.\d+\b`, so the round-57 counter must use R5x ids or the open rows fail `open_unplanned`.
2. Costs: R56.2 and R56.1 both need SKILL.md. Each costs `## Standing rules` (and R56.1 more) until the wave-3 re-key. R56.3's README line costs six headings. The three costly fixes are not staged; the L1 decides.
3. The C1 counter must treat `keys`/`verdict_basis`/`fixability*` as non-ledger fields (the round-50 code ignores them).

## Sweeps run (command → output)

- `git -C LANE rev-list --count 5e35699..HEAD` → `0` (`receipts/r1`).
- `git show 5e35699:tools/registry.json | sed -n 1288p` → `"GATE_SELFTEST: 19/19 pass",`.
- `TMPDIR=<scratch> python3 <clone>/tools/receipt-revision-gate.py --selftest` → `GATE_SELFTEST: 19/19 pass`, exit 0.
- Excerpt verification, round-50 resolver, all 13 items → `ALL_EXCERPTS_OK True`.
- Monitor (base, p1, p2, p3) → as in the table.
- Label/referent recount over the 18 bound entries → as above.

## Not run / unresolved

- The round-57 C1 counter was not run (not my artifact; it scores the whole ledger).
- `scripts/sources-census.sh validate` was not run on the probes. No probe changes SOURCES.md, so I expect no change, but this is not checked.
- No ledger row was written into the lane. `corpus/routed-defects.json` is unchanged.

## Installs / tools

None. Stdlib Python, git and the existing lane instruments only.

## Lane writes

Only `.ufo/waves/round-57/w1/T57W1ScribeItemsR56x1to4{.md,.json,/rows.json,/stage/,-receipts/}`. Scratch clones and fixtures were under `$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeItemsR56x1to4/` and are removed on exit. No mutating git call in the lane.
