# DriftSim — round-32 wave 1 (calibration no-harm drift simulation)

Seat: `TameshiR32.DriftSim`. L1: `TameshiR32`. Claim under no-harm: **C1 (operability,
capability acquisition)**. Frozen revision: `c31814978969a41a8e9b0f7d99fa308c5993c1b7`
("round-32: freeze — C1 counter + contract …").

Question answered: **which SKILL.md sections does each planned content edit drift, and
therefore how many cold reads wave 2 needs** to restore the calibration no-harm
(`covered=64/64 restraint=8 box3_mismatch=0`).

---

## Verdict (first)

1. **The calibration no-harm monitor is fragile to exactly four of the seven planned
   edits, and completely insensitive to three of them.** Measured on the frozen round-27
   counter, one commit per edit, each on top of `c318149`:

   | Planned content edit | `covered` | `restraint` | `box3_mismatch` | exit | sections drifted |
   |---|---|---|---|---|---|
   | baseline (frozen rev, no edit) | **64/64** | 8 | 0 | 0 | 0 |
   | (1) `corpus/SOURCES.md` registry row | 62/64 | 6 | 1 | 1 | **2** |
   | (2) `corpus/README.md` line | 61/64 | 6 | 1 | 1 | **3** |
   | (3) `SCORECARD.md` block | **64/64** | 8 | 0 | 0 | **0** |
   | (4) `LOG.md` block | **64/64** | 8 | 0 | 0 | **0** |
   | (5) new `corpus/knowledge/runner-tally-audit.md` | **64/64** | 8 | 0 | 0 | **0** |
   | (6) new `tools/tally-audit.py` | **64/64** | 8 | 0 | 0 | **0** |
   | (7) `corpus/QUALITY.md` line | 63/64 | 6 | 1 | 1 | **1** |
   | (8) all of 1–6 together | 59/64 | 6 | 1 | 1 | **5** |

   **Edits 3, 4, 5 and 6 are calibration-free** (append to `SCORECARD.md`, append to
   `LOG.md`, and both new files). **Edits 1, 2 and 7 are not.**

2. **The drift mechanism is byte-identity, not content.** The round-21 cold-read ledger
   records a sha256 per *input file* per entry (`.ufo/evidence/round-21/coldread/ledger.json`,
   480 entries, 7707 distinct input paths). The monitor credits a SKILL.md section when at
   least one ledger entry bound to that section still verifies every recorded input. Editing
   a file changes its sha256, so **every ledger entry that recorded that file as an input
   goes stale**; a section dies when *all* of its crediting entries recorded the edited file.
   Appending a row to `SCORESOURCES.md` kills a section for exactly the same reason as
   rewriting it. This is why edits 3 and 4 (which no ledger entry records as a required
   input of any crediting entry) cost nothing, and why edits 1, 2, 7 do.

3. **Wave-2 sizing.** For the eight assigned edits the drifted-section count is
   **0, 2, 3, 0, 0, 0, 1, 5** respectively; the union over all of them is **5 sections**.
   Round 31 needed **3 fresh readers per drifted section** (9 sections → 24 entries, groups
   A/B/C: `corpus/lessons/round-31.md:113-115`). So wave 2 needs
   **5 drifted sections × 3 readers = 15 fresh bound cold reads** for the full planned
   content revision — 15 seats, not 32, unless the L1's real revision drifts more.

4. **Two extra risks the L1 must plan for, both measured here.** A `tools/registry.json`
   edit (adding a row for the new tool) drifts **3 more** sections, and a **one-line
   `SKILL.md` edit drifts 1 section by a completely different mechanism** (`no-ledger-entry`
   — the section's sha256 changes, so its ledger entry no longer matches at all). See
   §"Supplementary variants" for the numbers. **If the L1's content revision touches
   `SKILL.md` or `tools/registry.json`, wave 2 must read 9 sections, not 5** — which is
   exactly what round 31 did (55/64 at its content revision, 9 drifted sections).

---

## Method

- Clone: `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin
  /fast/scratch/hyaku/tameshi-r32-seats/DriftSim/lane`, detached at `c31814978969a41a8e9b0f7d99fa308c5993c1b7`.
  Sandbox git only, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset. No `jj` command was
  run anywhere. Nothing in `/home/vgpnk/Projects/shokunin` or
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin` was modified.
- One `git worktree` per variant, each a **single sandbox commit whose parent is exactly
  `c318149`** (asserted in the generator for every variant).
- Frozen counter, run verbatim in each worktree:

  ```
  cd /fast/scratch/hyaku/tameshi-r32-seats/DriftSim/wt/<variant>
  timeout 900 python3 .ufo/evidence/round-27/c1-measure.py --repo <worktree> --rev HEAD
  ```

  (`--repo` points at the worktree, `--rev HEAD` at the variant commit. The round-27
  counter is the calibration no-harm instrument named in the round-32 contract
  `no_harm.calibration`; it drives the unchanged round-21 cold-read monitor.)
- Receipts: `/fast/scratch/hyaku/tameshi-r32-seats/DriftSim/results/<variant>.{stdout,stderr,exit}`.
- `tools/mutate-and-run.sh` is byte-identical (`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`)
  in **every** variant — the C1 predicate's runner pin holds through all of them.

### Method validation

The method reproduces a known historical number. Round 31's real content revision
`2da841bd` (SCORECARD rows, SOURCES, QUALITY 66-71, README row, knowledge entry, one
SKILL.md line) measured **55/64** at that revision, which is exactly what the lane
recorded at `SCORECARD.md` ("content revision `2da841bd`: 55/64, restraint 6"). This
seat's maximal variant `v13-everything` (all seven planned edits + a `tools/registry.json`
row + a one-line `SKILL.md` edit) also measures **55/64** with the same nine drifted
headings as round 31's historical list — eight by input drift on SOURCES/QUALITY/README,
one by the SKILL.md line edit. The instrument agrees with the lane's own history.

---

## Exact evidence

### Baseline (frozen revision, no edit)

```
$ cd /fast/scratch/hyaku/tameshi-r32-seats/DriftSim/lane
$ timeout 900 python3 .ufo/evidence/round-27/c1-measure.py --repo "$PWD" --rev HEAD
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7
exit 0
```

No `uncovered:` headings.

### (1) `corpus/SOURCES.md` — append one registry row (`| S097 |`)

```
C1_MONITOR: covered=62/64 restraint=6 box3_mismatch=1 depth_score=9 rev=d86d6f3ac5a1ccc275236aa86bc31051f39ba8b1
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ## Ninth recorded case — round 26
```
exit 1. Frozen monitor `--explain` reasons:
`input-drift:corpus/SOURCES.md` (both sections; the first also lists
`corpus/QUALITY.md`, `tools/registry.json`).

The appended row is a well-formed 11-column registry row: census at that revision
reads `rows=95 malformed=0` (base `rows=94 malformed=0`), so the row itself is not the
cause — its sha256 change is.

### (2) `corpus/README.md` — append one line

```
C1_MONITOR: covered=61/64 restraint=6 box3_mismatch=1 depth_score=9 rev=51cb4b61dc9bfffd587a61d7fc529c1e4b531e56
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
```
exit 1. Reasons: `input-drift:corpus/README.md` on every one.

### (3) `SCORECARD.md` — append a block

```
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=3444564e10ecf4d7aa4f1d1e1d8735a6bd120721
```
exit 0. **No drift.**

### (4) `LOG.md` — append a block

```
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=26dd8be0199238c27d109a9526f875767370fb87
```
exit 0. **No drift.**

### (5) new file `corpus/knowledge/runner-tally-audit.md`

```
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=d50e550b6d2eb2516d5965e6c992581c19ef6f22
```
exit 0. **No drift** — a file no ledger entry records cannot drift a recorded input.

### (6) new file `tools/tally-audit.py`

```
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=a86450251825a479b63303cd45c59edc36f764a6
```
exit 0. **No drift.** (Also: adding a file under `tools/` does not change
`tools/mutate-and-run.sh`, so the C1 predicate's runner pin is untouched.)

### (7) `corpus/QUALITY.md` — append one line

```
C1_MONITOR: covered=63/64 restraint=6 box3_mismatch=1 depth_score=9 rev=f407ff9dfab3b7be47e97ea2fc38bf08b0eaa6d5
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
```
exit 1. Reason: `input-drift:corpus/QUALITY.md`.

### (8) all of 1–6 together

```
C1_MONITOR: covered=59/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2762f7634ccd757fa85e0291c533d9451e0aa482
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ## Ninth recorded case — round 26
```
exit 1. **5 drifted sections** = the union of (1)'s 2 and (2)'s 3. (3)–(6) add nothing.

---

## Supplementary variants (beyond the eight assigned cases)

These are the shapes the L1's *real* content revision is most likely to take. Same
method, one commit each on top of `c318149`.

| Variant | Edits | `covered` | Drifted sections | New drifted headings vs. the eight assigned cases |
|---|---|---|---|---|
| `v9-all-seven` | (1)–(7) together | 59/64 | 5 | none — QUALITY adds no new section (its one killed section, "Round-20 gate/probe registry", is already killed by SOURCES) |
| `v10-all-seven-plus-registry` | (1)–(7) + a `tools/registry.json` row | 56/64 | **8** | `## Live-tree re-pin and entry-command monitor — round 17`, `### Round-21 gate/probe registry — finite environment differential`, `### Round-26 gate/probe registry — report interop` |
| `v14-registry-only` | `tools/registry.json` row alone | 61/64 | **3** | the same three as above |
| `v11-skill-line` | one-line `SKILL.md` edit alone | 63/64 | **1** | `## Input-keyed cold-read credit — round 17` — reason `no-ledger-entry`, **not** input drift |
| `v12-all-plus-skill` | (1)–(7) + one `SKILL.md` line | 58/64 | **6** | the `no-ledger-entry` one |
| `v13-everything` | (1)–(7) + registry row + `SKILL.md` line | **55/64** | **9** | all of the above — identical to round 31's historical content-revision shape |

Verbatim `v13-everything` (the worst case, and the one that matches round 31):

```
C1_MONITOR: covered=55/64 restraint=6 box3_mismatch=1 depth_score=9 rev=b6867610fdc92bd4a3b29da1119245243629d007
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ## Input-keyed cold-read credit — round 17
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
  uncovered: ## Ninth recorded case — round 26
  uncovered: ### Round-26 gate/probe registry — report interop
```

Verbatim `v11-skill-line` — note the reason is `no-ledger-entry`, a different failure mode
from input drift:

```
C1_MONITOR: covered=63/64 restraint=6 box3_mismatch=1 depth_score=9 rev=b2319b531a21719140f6e18dac37f8f19e66986b
  uncovered: ## Input-keyed cold-read credit — round 17
```
`--explain`: `reason: no-ledger-entry`. Editing `SKILL.md` changes the *section's own*
sha256, so the ledger entry keyed by the old section sha stops matching — the entry is
not stale, it is absent. One such section per edited `SKILL.md` section.

---

## Predictive map (so the L1 can size wave 2 without re-running anything)

Computed with the frozen monitor's own sectionizer and credit rule
(`.ufo/evidence/round-18/measure.py` `sectionize` + `entry_reason`, with the round-21
selector's module tweaks applied). **This predictor reproduces every measured variant
above exactly**, including the `tools/registry.json` case that a simpler
input-intersection rule gets wrong:

| Edited file | Sections it kills | Sections |
|---|---|---|
| `corpus/SOURCES.md` | **2** | `### Round-20 gate/probe registry — frozen receipt instruments`; `## Ninth recorded case — round 26` |
| `corpus/README.md` | **3** | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`; `## Restore discipline — before/after identity, not continuous non-write proof`; `### The map — where a reader enters, artifact by artifact` |
| `corpus/QUALITY.md` | **1** | `### Round-20 gate/probe registry — frozen receipt instruments` |
| `SCORECARD.md` | **0** | — |
| `LOG.md` | **0** | — |
| `tools/registry.json` | **3** | `## Live-tree re-pin and entry-command monitor — round 17`; `### Round-21 gate/probe registry — finite environment differential`; `### Round-26 gate/probe registry — report interop` |
| `tools/mutate-and-run.sh` | **19** | (must stay byte-identical — this is the C1 predicate's pin) |
| any **new** file | **0** | — |
| a `SKILL.md` section edit | **+1 per edited section** | `no-ledger-entry` (separate mechanism) |

Union over the seven assigned file edits: **5 sections**. Union including a registry-row
edit: **8 sections**. Union including a one-line `SKILL.md` edit: **6 sections**.
All three plus a registry row: **9 sections**.

### Why `SCORECARD.md` and `LOG.md` are free, and `tools/registry.json` is not

The ledger's input paths are counted per file over all 480 entries:

| input path | entries recording it |
|---|---|
| `tools/mutate-and-run.sh` | 282 |
| `tools/trace-inputs.py` | 156 |
| `corpus/SOURCES.md` | 149 |
| `tools/registry.json` | 107 |
| `corpus/README.md` | 80 |
| `corpus/QUALITY.md` | 46 |
| `SKILL.md` | 50 |
| `SCORECARD.md` | **3** |
| `LOG.md` | **3** |

`SCORECARD.md` and `LOG.md` are recorded by only 3 entries each, and in both cases the
sections they bound still have other crediting entries that do not record them — so the
section survives. `tools/registry.json` is recorded by 107 entries and *is* on the
critical path for three sections.

---

## Smallest safe correction

**The correction is in the L1's sequencing, not in the counter.** Nothing needs fixing in
the frozen instruments: the counter, the contract and `tools/mutate-and-run.sh` are all
byte-correct, and no drift was found in the monitor itself. The safe correction is:

1. **Land the content revision, then let wave 2 read exactly the drifted sections.** With
   the seven assigned edits, wave 2 needs **5 sections × 3 readers (groups A/B/C) = 15
   fresh bound cold reads**, matching round 31's binding-v5 practice
   (`corpus/lessons/round-31.md:113-115`: 9 sections → 3 readers each → 24 entries).
2. **Prefer the drift-free edits where they are available.** Edits 3, 4, 5 and 6 — the
   `SCORECARD.md` block, the `LOG.md` block, the new knowledge entry and the new tool —
   cost nothing. The L1 can, if it wants to keep wave 2 small, defer the `SOURCES.md`
   row, the `README.md` row and the `QUALITY.md` line to a later round. **But note the
   round-32 contract already commits to a SOURCES row** ("`sourced_on`: a SOURCES.md row
   opened this round (bash manual exit-status semantics)"), so the SOURCES row is
   expected to land in this round's content revision: **budget 2 sections for it**.
3. **Do not edit `SKILL.md` or `tools/registry.json` in the content revision unless wave 2
   is sized for them.** A `SKILL.md` line costs 1 section (`no-ledger-entry`); a registry
   row costs 3. Either one pushes the drifted set above the 5-section plan. Round 31's
   own content revision did both and needed 9 sections — wave 2 there had 32 seats.
   **For round 32, 15 seats cover the seven assigned edits; 27 cover the full shape
   (5 + 3 + 1).**
4. **Restore the no-harm by fresh bound reads, not by editing the ledger.** The contract's
   `no_harm.calibration` says the calibration is "restored at the measurement revision by
   fresh bound cold reads of any drifted section" — that is exactly the round-31 pattern
   (`ledger 456 → 480` at `83c001a5` after 24 fresh entries). Wave 2 must read at the
   measurement revision, with binding v5, and the L1 must then append the ledger entries.
5. **The measurement revision must carry the ledger append.** At the content revision the
   monitor will read 59/64 (five assigned edits), restraint 6, `box3_mismatch=1` — that
   is *by design*, exactly as round 31 recorded ("content revision `2da841bd`: 55/64,
   restraint 6, by design"). The C1 counter (`c1-measure.py`) is unaffected by all of
   this: it reads `tools/mutate-and-run.sh` and `tools/tally-audit.py` only, and the
   runner pin held in all 15 variants.

---

## Risks and blockers

- **Risk — the L1's real content revision may drift more than these fixtures.** The
  fixtures are the assigned seven edits; a real revision that also touches `SKILL.md`,
  `tools/registry.json`, `PROVINCE.md`, `SHONEN.md`, `tools/trace-inputs.py` or any of
  the ~40 `.ufo/evidence/**` files the ledger records will drift further. The predictive
  map in this report gives the per-file cost for the ones most likely to be touched; the
  L1 should run the frozen monitor on its own content revision before dispatching wave 2
  rather than trusting the fixture count.
- **Risk — the number is a floor, not a ceiling.** Round 31 read 9 drifted sections and
  assembled 24 entries (not 27): some reads do not produce a usable entry. Plan for
  ≥3 readers per drifted section and allow some attrition.
- **Blocker — none for this seat.** All assigned work is complete: 8 assigned variants
  measured, 6 supplementary variants measured, predictor cross-validated against all of
  them, runner pin verified byte-identical in all 15 variants.
- **Not claimed.** No claim is made about which exact byte-level edits the L1 will make,
  about the completeness of the ledger's input coverage, or about the C1 counter's
  correctness — this seat only measured the calibration monitor's drift behaviour.

---

## Files and commands

Sandbox (this seat's own scratch, nothing else was written):

```
/fast/scratch/hyaku/tameshi-r32-seats/DriftSim/
  lane/                  clone at c318149 (baseline)
  wt/<variant>/          15 worktrees, one sandbox commit each (removed after
                         measurement; the commits survive as refs
                         refs/drift-sim/v1..v14 in lane/, so any variant can be
                         re-checked with `git -C lane worktree add wt/x
                         refs/drift-sim/vN`)
  results/<variant>.{stdout,stderr,exit}   frozen-counter receipts
  gen.py gen2.py gen3.py gen4.py gen5.py    fixture generators
  run.sh                 parallel counter driver
  explain.py diag.py predict.py             attribution + predictor
```

Key commands:

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r32-seats/DriftSim/lane
git -C .../lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
cd .../wt/<variant> && timeout 900 python3 .ufo/evidence/round-27/c1-measure.py \
  --repo .../wt/<variant> --rev HEAD
```

**Tooling:** no tool was installed or upgraded by this seat; the frozen round-27 and
round-21/round-18 counters and stock `git`/`python3` were sufficient.
