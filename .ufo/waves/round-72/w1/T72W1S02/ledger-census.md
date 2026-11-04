# T72W1S02 — round-21 cold-read ledger census (round 72, w1)

Read-only census. Generator (this directory):
`python3 -I -X utf8 .ufo/waves/round-72/w1/T72W1S02/ledger-census.py --out .ufo/waves/round-72/w1/T72W1S02/ledger-census.json`
run from the lane root; stdout `CENSUS base_entries=797 live_entries=820 sections=64 out=…`.
Every number below is in `ledger-census.json` (machine data; the 64-row section table is
`snapshots.base.sections.rows`).

## Snapshots

- **base** — `git show f20ba48…:.ufo/evidence/round-21/coldread/ledger.json`,
  sha256 `35dff71c502d251cb2bdd41c539912941a765a2f110e18b8d9f7e0e2a3bd61e2`,
  36,388,098 B, schema `tameshi-coldread-ledger-v2`, 20 `corrections`, **797 entries**.
- **live** — working-tree ledger at run time, sha256
  `193dd0fa55c764099c242016d503bd0860d3df2283d834e1892f212823f8c6e3`, **820 entries**,
  HEAD `d8e7f337` at run. The file is rewritten by the round's own rekey while the wave
  runs: 797 → 814 → 820 during this census (`r72-batch-1` 17 entries, then `r72-batch-2`
  6 entries), and HEAD moved
  `dfb534ca → bc7dc2fb → b611e763 → d7eb02c2 → a533d7d3 → ebad004b → d8e7f337`. Census
  numbers are citable only against a blob sha; the base blob is the frozen one.
- **SKILL.md** — base blob and worktree both sha256 `b56c0252…`; the frozen sectionizer
  `.ufo/evidence/round-18/measure.py` yields **64 sections** (preamble `""` + the
  `# tameshi-shokunin` title + 62 `##`/`###` headings), matching the plan's
  `REKEY_COST sections=64`.

## 1. Totals

- entries **797**; distinct heading keys **65** = 64 non-empty + preamble `""` (3 entries).
- entries per heading: **min 1, median 8, max 43** (65 keys; non-empty: min 1,
  median 8.0, max 43).
- max: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (43).
- five 1-entry headings: `## Appendix A…`, `## Final pointers…`, `## The mutation bar…`,
  `### The mado run (T6-1, 2026-10-14) — measured`, `### The opt-in contract…`.
- histogram (count:headings): 1:5, 2:7, 3:4, 4:4, 5:5, 6:2, 7:2, 8:10, 9:2, 10:3, 11:1,
  15:1, 16:1, 17:1, 19:2, 20:1, 22:1, 25:1, 26:1, 29:1, 31:2, 33:1, 34:2, 35:1, 36:2,
  39:1, 43:1.

## 2. `rekey_batch`

**153 / 797** entries carry `rekey_batch` (19.2 %), **11 batches**, all contiguous at
indices 644–796, one `read_rev` per batch:

| batch | n | index range | read_rev |
|---|---|---|---|
| r61-batch-1 | 18 | 644–661 | 19d7e996 |
| r61-batch-2 | 18 | 662–679 | 0a29e3cf |
| r63-batch-1 | 13 | 680–692 | 8616d47e |
| r64-batch-1 | 13 | 693–705 | b31e8145 |
| r65-batch-1 | 13 | 706–718 | 3fa08b2c |
| r66-batch-1 | 13 | 719–731 | e8e0f0e9 |
| r67-batch-1 | 13 | 732–744 | ab67ddd6 |
| r68-batch-1 | 13 | 745–757 | dcd10cc5 |
| r69-batch-1 | 13 | 758–770 | cf5570d3 |
| r70-batch-1 | 13 | 771–783 | 910a3c35 |
| r71-batch-1 | 13 | 784–796 | 1b9a0293 |

Live adds `r72-batch-1` (17 entries, 797–813, rev `d618518a`) and `r72-batch-2`
(6 entries, 814–819, rev `b7b98375`; the 6 PROVINCE-pinning sections rekeyed a second
time) → **176** rekey entries in the live snapshot. Both r72 batches also carry
`rekey_round: 61`.

**Flag:** every rekey entry carries `"rekey_round": 61`, including r63…r72. The field is
a constant, not the batch's round; nothing in the census can recover the batch round from it.

## 3. Section coverage (64 sections)

**64/64** sections have a newest heading-keyed entry. Newest-entry input counts
(raw `inputs` / `inputs_view` with the self-referential keys removed): **min 1 / 1,
median 6 / 6, max 7702 / 7702**; sum of views 11,514. External inputs are separate and
recorded per row.

- min-1: `### The mado run…` (idx 21), `## Final pointers…` (37), `### The report shape…`
  (355), `## The re-sweep cadence…` (549).
- max: `## Mutation-sweep recipe…` (785, 7,702 inputs; `## Standing rules` 784 has 2,497).

No newest entry has 0 inputs. No newest entry pins a path absent at base.

## 4. Per-path membership (newest-entry pins, self-referential keys excluded)

7,721 distinct paths across the 64 newest views. Top 20 (`path`: sections):

```
35 tools/trace-inputs.py                 35 tools/mutate-and-run.sh
20 corpus/knowledge/fleet-kill-rate-ledger.md
16 tools/bash-witness-study.py           15 .ufo/evidence/round-17/coldread/trace-inputs.py
15 tools/pin-disposition.py
14 corpus/knowledge/mutation-case-kimi-census.md
14 corpus/knowledge/mutation-case-kagi-census.md
14 .ufo/evidence/round-12/BashWitness/declaration.json
14 .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json
14 .ufo/evidence/round-12/BashWitness/summary.json
14 tools/witness-metadata.py
13 .ufo/evidence/round-12/BashWitness/declared.tsv
13 .ufo/evidence/round-13/pin-manifest.json
13 corpus/SOURCES.md
13 corpus/knowledge/gates-survey-kagi.md
13 corpus/knowledge/mutation-case-mado-verify.md
13 corpus/knowledge/operator-runbook.md
13 .ufo/evidence/round-18/final/before.stdout
13 .ufo/evidence/round-18/final/case7.stdout
```

Requested paths:

| path | membership | note |
|---|---|---|
| `corpus/SOURCES.md` | **13** | set-equal to the guard's 13 LOST headings in `reh-sources-only.out` |
| `PROVINCE.md` | **6** | |
| `corpus/QUALITY.md` | **6** | |
| `README.md` | **2** | |
| `SCORECARD.md` | **0** | |
| `LOG.md` | **0** | |
| `tools/pointer-recheck.json` | **0** | no section pins it (structural) |
| `tools/mutate-and-run.sh` | **35** | |

Overlap `SOURCES ∩ PROVINCE` = **2** → union **17** = the frozen C1 forecast for the
round's edit set. `QUALITY ∩ SOURCES` = 6, `QUALITY ∩ PROVINCE` = 2.
Self-referential keys: `SKILL.md` is pinned raw by 9 newest entries (excluded by the credit
rule); the round-17 and round-21 ledgers are pinned by 0 newest entries (the rekey drops them).

The five frozen rehearsal arms re-checked structurally from the base ledger — newest-pin
set vs the `LOST` headings in `.ufo/evidence/round-72/reh/*.out` (no guard run here):

| receipt | planned edit | guard `lost` | newest-pin | set equal |
|---|---|---|---|---|
| `reh-sources-only.out` | `corpus/SOURCES.md` | 13 | 13 | yes |
| `reh-province-only.out` | `PROVINCE.md` | 6 | 6 | yes |
| `reh-quality-only.out` | `corpus/QUALITY.md` | 6 | 6 | yes |
| `reh-scorecard-only.out` | `SCORECARD.md` | 0 | 0 | yes |
| `reh-province-sources.out` | `PROVINCE.md`+`corpus/SOURCES.md` | 17 | 17 | yes |

Symmetric difference empty for all five at both snapshots (`rehearsal_set_check`).

## 5. Append order vs `read_rev` order

**No append inversions.** For all 65 heading keys the last appended entry carries the
newest `read_rev` commit time (0 pairs *i<j* with `commit(rev_i) > commit(rev_j)`).
Three headings tie the max commit time between an earlier entry and the newest, all with
the *same* rev (ties, not inversions):

- `## Input-keyed cold-read credit — round 17`: entries 462 / 470, rev `2da841bd`;
- `### Round-20 gate/probe registry — frozen receipt instruments`: 481 / 489, `a4f71813`;
- `## Ninth recorded case — round 26`: 482 / 491, `a4f71813`.

## Pathology flags

1. **40/64 newest entries carry stale `start`/`end`** while their `sha256` still matches
   the base section (line shifts from later inserts). Worst: `## Restore discipline —
   before/after identity…` entry 512 stores span 375–404; the base section is 403–432.
   Consumer impact: the frozen module's overlay index keys on `(skill_sha256, start)`, but
   the round-21 selector forbids overlay and the guard's own section spans come from the
   sectionizer, so no measured effect — any future span-keyed consumer would mis-map.
2. **1 malformed input key**: entry 97 (`### The six-leg regression — usage and this
   round's receipt`) pins `tools/mutate-and-run.sh@75ed934d…` — no such path; the same entry
   also pins `tools/mutate-and-run.sh` with the same digest. Entry 97's section sha no
   longer matches (inert at base), so the guard never sees it.
3. **1 orphan heading key**: `## Restore discipline — proof the substrate never moved`,
   5 entries, every stored span 375–404, newest idx 186; no base section has that heading.
   The "64 non-empty heading keys" therefore coincide with the 64 sections for the wrong
   reason (63 live heading strings + 1 stale).
4. **10 sections whose newest entry does not cover every path pinned by older same-sha
   entries** (max 88, `## The cadence's first scheduled tick…`). Dead credit surface, not
   forecast risk at base: the newest entry omits those paths, so a single-path edit to one
   forecasts 0 and the newest entry stays fresh.
5. **Pin freshness at base**: 80/797 entries verify; **all 64 newest entries verify**.
   For each of the 8 requested paths, **0** older input-verifying same-sha entries in
   newest-pinned sections omit the path — no credit shadow, so the newest-entry forecast's
   predicted-loss set is exact for single-path edits at base.
6. **The ledger is a moving target** during the wave (in-place rekey). Any census,
   forecast or verdict must cite a blob sha; `tools/rekey-cost.py` reads the working-tree
   file, so its forecast is only reproducible against the blob it happened to read.
