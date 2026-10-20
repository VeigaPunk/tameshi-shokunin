# FrontierMap — corpus/README touch map for round 16 C1 (round-gate case 7) and C2 (full-page SKILL cold-read)

Read-only scout. Question: which `corpus/README.md` rows and `## Frontier` items do
the two declared claims touch, which new coverage-map rows `QUALITY.md` 7 requires
this round, and whether any frontier item moves to Core.

## 0. Method and executed evidence

Commands run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`:

| Command | Exit | Key output |
|---|---|---|
| `wc -l corpus/README.md` | 0 | `217 corpus/README.md` (headings: `3` Coverage map, `68` Frontier, `89` Known gaps, `105` Frontier status correction, `123` Round 12, `148` Round 13, `180` Round 14, `195` Round 15; no Round 16 section yet) |
| `git show HEAD:tools/mutate-and-run.sh \| python3 -c '<command D regex>'` | 0 | `HEAD recorded_cases=6 depth_score=6` |
| worktree leg enumeration (`^#   (js\|bash)-…`) | 0 | legs at lines 84–89: `js-kimi-census 8/10`, `bash-surface-census 8/10`, `bash-tsukuroi-census 6/10`, `bash-mado-verify 4/10`, `bash-checklist-run 7/15`, `js-claims-check 7/10` |
| `git -C kumitate-shokunin cat-file -p 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -` — C1 pin **holds** |
| README's own coverage check (`for f in corpus/knowledge/*.md; …`) | 0 | `0` missing rows; `23` knowledge notes |
| `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md` | 0 | `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` — matches C2 |
| regex probe on the RGLeg template comment line | 0 | unsubstituted `@@RG_KILLED@@/10` → `False`; substituted `8/10 (80 %)` → `True` |
| `ls .ufo/evidence/round-16/coldread/` | 0 | only `SKILL.snapshot.md` — no `ledger.json` yet, so `box3_full_page=false` today |

Files read: `corpus/README.md` (all 217 lines, key rows re-read raw), `corpus/QUALITY.md`,
`PROVINCE.md`, `SCORECARD.md` (lines 60–76, 180–186, 284–312), `SHONEN.md:5-34`,
`tools/mutate-and-run.sh:60-120`, `corpus/knowledge/arm-class-matrix.md:298-340,470-500`,
wave `spec1.json` context and dispatch/registry entries (to identify planned artifacts, not
as evidence of outcomes).

## 1. C1 — round-gate as the seventh recorded mutation case

Depth is defined at `SCORECARD.md:66`:
> `| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. tools/mutate-and-run.sh:84-89; command D below. This measures documented case depth, not newly executed cases. |`

Command D is `SCORECARD.md:72-73`; the strictest precedent is `SCORECARD.md:286-289`:
> `The old round-2 plan above supplied F3/F2 starting points, not permission to add a seventh ledger leg. … The “6 → 7” prediction is rejected and superseded: reanalysis of the same bash target is depth within a case, not a new independent case.`

Round-gate is a **different target file and suite** from all six legs, so it passes that
precedent's test; it is not a re-analysis. But depth 7 needs the new ledger comment line,
which must be substituted (see §5, item 2).

### 1.1 Rows touched (line numbers in `corpus/README.md`)

| Line | Existing row / text (quoted) | Why C1 touches it | Required round-16 action |
|---|---|---|---|
| 7 | `` … fail-closed arm inventories (proxy 12/12 arms fired, claims 5/5, kimi-census 1 token ×3 cases, round-gate 7 declared/6 fired with `INTERNAL_ERROR` uncovered, … `` | The sweep's 10 mutants target these arms. A survivor on the uncovered token confirms the static claim; a kill falsifies it. Executed count `60` for round-gate in the same cell. | Appended correction **only if** the sweep changes the arm statement; otherwise cite as unchanged. |
| 10 | `` … round-gate `f890e277…`, proxy-check `a052ddb9…` … `` | Byte anchor row for the same pin C1 sweeps. Verified full sha equals `f890e277…a834d3e9` at rev `364f1d5`. | Cite; no edit. |
| 47 | `` | `knowledge/arm-class-matrix.md` | JS + bash mutation-case arm-completeness matrix (round 4) | `mutation-case-kimi-census.md`; `mutation-case-kagi-census.md` | `` | §13 is the pre-registration source and says of itself: “no mutant was cut, no gate mode was executed, no `--selftest` pulse was taken” (`arm-class-matrix.md:300-303`); PU1 says it is “a hypothesis until a mutant” (`:475`). C1 converts projection to measurement. | Appended round-16 addendum/correction (“§13 measured, not projected”); row itself stays. |
| 49 | `` | `knowledge/fleet-kill-rate-ledger.md` | standing per-gate view: suite size, kill rate, survivor classes, sweep date, pin; stale successor rows open | the six mutation-case notes; S031 | `` | New leg `js-round-gate` must enter the standing view; “the six mutation-case notes” becomes seven. | Appended correction **six → seven**; do not edit the row in place (`README.md:40`: “Appended, not inserted: the rows above keep their line numbers.”). |
| 13, 14, 51, 52, 53, 54 | `mutation-case-kimi-census.md` (“first measured kill-rate”), `mutation-case-kagi-census.md` (“second measured”), and `case 3` tsukuroi / `case 4` mado / `case 5` kagi checklist / `case 6` kumitate claims | The numbering and method the seventh case joins; row 49's “six mutation-case notes” is the only cross-reference that changes. | No edit to these six; they remain the prior-case ledger. |
| 55 | `` | `knowledge/operator-runbook.md` | operator runbook … (four-leg lines: ER-R3 open) | `` | Leg count grows again; the runbook was already stale at six (gap at line 98). | No new obligation; do not claim the runbook current. |
| 96–97 | `` - **Stale ledger successors** — tsukuroi and mado legs read `stale` … re-sweeps owed (freshness). `` | A fresh seventh leg exists but does not discharge the two stale successors. | Not discharged; freshness remains open. |

**New row required by QUALITY 7:** a case-7 note row does not exist in any current row
(none of lines 7–15, 47–61 names round-gate as a mutation case). See §3.

### 1.2 Anchors outside README that the same change touches (L1-owned, cited for integration)

- `PROVINCE.md:29` — “the six recorded mutation legs' gates as read-only primary surfaces” → seven.
- `SCORECARD.md:66` — supporting range `tools/mutate-and-run.sh:84-89` goes stale when a
  seventh leg lands at line 90; re-cite as `:84-90` or the exact new range.
- `SCORECARD.md:310-312` — “Scalar commands D and C remain historical: D prints `recorded_cases=6`”;
  the round-16 claims row must carry the measured post-substitution value, not this sentence.

## 2. C2 — full-page SKILL cold-read

| Line | Existing text (quoted) | Why C2 touches it | Required round-16 action |
|---|---|---|---|
| 15 | `` | `knowledge/executor-test-sufficiency.md` — round 3 (TAMESHI-R3-4) | The no-oral-context executor test (SHONEN box 3 evidence): an executor with no tameshi context beyond `SKILL.md` @ `dd2f4dee…3753` reproduced **one killed mutant end-to-end** … `` | Prior box-3 evidence is a one-mutant executor test at a different SKILL pin. `QUALITY.md:43-46` (criterion 13) says an Appendix A/B read cannot earn full-page credit; the full-page ledger at `97cf436b…` is the new coverage evidence. | Appended correction linking box-3 coverage to the full-page ledger; row stays. |
| 26 | `` … rejected: same-lane promotion authority and broad current cold-read credit from one historical JS mutant. … `` | The precedent that cold-read credit is scope- and pin-bound; the full-page read must be keyed to the snapshot sha, not “current SKILL”. | Cite as the restraint anchor; no edit. |
| 99–103 | `` - **`SKILL.md` status sentences stale** … Left unedited so the cold-read stays bound to the executed bytes; the next `SKILL.md` edit re-runs it. `` | C2 plans L1 to repair blocking gaps in SKILL.md and re-read in wave 2 — this gap's trigger fires. | Bind box-3 credit to the **repaired** sha if SKILL.md changes; otherwise to `97cf436b…`. Do not mix sections from two shas in one ledger entry set. |
| 143–146 | `` Full-page box-3 sufficiency is still unearned; historical cold-read receipts apply only to their pinned SKILL bytes. `` | Directly superseded **iff** every section has a ledger entry at one sha (CRMeasure's `box3_full_page`). | One appended round-16 status correction supersedes this sentence, conditionally. |
| 160 | `` … F1 interop, legacy provenance headers, runbook corrections and current full-page cold-read/box3 remain debt. `` | Same. | Superseded only on complete ledger. |
| 190 | `` This round does not complete … any successor mutation sweep, legacy provenance-header repair, runbook repair or current full-page cold-read/box3. `` | Same. | Same. |
| 207 | `` Legacy provenance headers, runbook corrections and current-page cold-read/box3 remain open. `` | Same. | Same. |

No `## Frontier` row is touched by C2; the cold-read is calibration evidence
(`SCORECARD.md:67` + command C at `:74-75`), not frontier ground.

## 3. QUALITY criterion 7 — exactly what must land this round

`corpus/QUALITY.md:18-20`:
> `7. A knowledge file lands with its coverage-map row in the same round, or the missing row is named as debt in LOG.md with an owner. (MK-4)`

Institutional reading (same file, `README.md:40-43`): rows are **appended, not inserted**,
and this criterion was the one that closed the lagging-index debt
(`` `QUALITY.md` 7 `` cited explicitly at line 41). Fleet rule `CORPUS.md:46-48`:
“**An index row is a claim.** Write the row when the file exists, not before.”

Applying it to round 16:

1. **Required: one row for the round-gate case note** — `corpus/knowledge/mutation-case-kumitate-round-gate.md`
   (name to be fixed by L1). PlannerWalk's integration target names “knowledge entry for the
   round-gate case” + “corpus/README coverage map + Frontier”; no spawned seat owns the
   write, so **L1 must append it**. The established artifact pattern is one note per case
   (rows 13/14/51/52/53/54), and §1 shows no existing row can stand in for it.
2. **Conditional: one row for any new cold-read knowledge file.** If C2 lands a new
   `corpus/knowledge/*.md`, it needs a row. If instead the result is appended to
   `knowledge/executor-test-sufficiency.md` (row 15), **no new row is due** — an appended
   correction to row 15 is (see §2).
3. **Conditional: one row for a forked arm-class-matrix round-16 note.** If §13's measurement
   is appended to the existing file, row 47 already exists and no new row is due; a new
   `arm-class-matrix-*` file would require its own row.
4. **No rows due** for `corpus/lessons/round-16.md` (lessons have their own table at
   `README.md:22-27`) or for `corpus/SOURCES.md` rows (registry, not `knowledge/`).
5. **Alternative is not silence:** the second clause allows a `LOG.md` debt line with an
   owner; LOG.md is L1/operator-owned, not a leaf write.

Mechanical falsifier: `README.md:43`'s own check
`for f in corpus/knowledge/*.md; do b=${f##*/}; grep -qF "knowledge/$b" corpus/README.md || echo "$b"; done | wc -l`
must print `0` at the round commit (it prints `0` now, over 23 notes).

## 4. Frontier F1–F10 — touch matrix

Rows quoted from `README.md:78-87`; statuses per the table plus the status corrections at
`:105-121` and the round-12/13/15 paragraphs.

| id | Row status (line) | Next falsifiable move (quoted) | Touched by C1/C2? | Verdict |
|---|---|---|---|---|
| F1 (78) | held (round 1) → corrected “partly held” at `:109-113` | “emit one ledger leg as schema JSON and validate it (validator unavailable this round: U)” | No. The seventh leg is a `#   js-round-gate …` comment line plus an embedded shell spec/table in `mutate-and-run.sh`, not schema JSON, and no validator is in the round plan. | Not advanced. Do not cite the new leg as F1 interop. |
| F2 (79) | held → “partly held” at `:114-118` | “the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8” | No. Round-gate is JS and C1 declares no witness split. | Not advanced. |
| F3 (80) | open | “one control per sweep … → N ≥ 3 byte-identical controls, or a named mismatch” | No. `mutate-and-run.sh` runs one control. | Not advanced. |
| F4 (81) | open | “update paths that write expected values without an explicit flag: unmeasured → counted per surveyed gate” | No. | Not advanced. |
| F5 (82) | open | “runner selftest host vs `env -i LANG=C TZ=UTC`: identical … → the six gate selftests measured the same way” | No. Not the env-normalization experiment. | Not advanced. |
| F6 (83) | open | “B5 probe fixture size: unmeasured → reduced size + kill check” | No. SurvivorPrep writes off-suite probes, not a minimized fixture, and no kill check on a reduced fixture. | Not advanced. |
| F7 (84) | open | “pin-level cadence only → per-leg reuse decisions classified” | No. | Not advanced. |
| **F8 (86)** | open | “0 test-oracle lines → **one survivor classified against an independently anchored expectation**” | **Conditionally.** SurvivorPrep prepares off-suite probes with pristine expectations for the arms §13.5/§13.6 predict will survive. F8's stated move is discharged only if (i) at least one predicted survivor actually survives, (ii) the probe is run against the **mutant** (wave 1 verifies pristine only), and (iii) the result lands in an admitted source-headed note. | **At most conditional; not “held” from wave 1.** |
| F9 (87) | open | “no LLM-specific search run yet (U) → bounded pilot with an independent outcome check” | No. New Stryker/PIT/survey rows are operator-class sources, not an LLM search. | Not advanced. |
| F10 (88) | open | “no PBT fixture method → one generator against a named fixture gate” | No. | Not advanced. |

Rule applied (`README.md:70-71`, `:120-121`, `PROVINCE.md:40-42`): “A ground moves to
`held` only through an admitted `knowledge/` entry with a `source:` header citing a `mined`
`SOURCES.md` row”, and “A ground reads `held` only when its next move in the table is
measured.” C1's case note, even if admitted, measures F8's move only under the three
conditions above; it measures none of F1–F7, F9, F10.

## 5. Core verdict

**No F1–F10 item moves to Core this round.** Two distinct changes are in play, and neither is
a frontier→Core move:

1. **Core surface list (PROVINCE).** `PROVINCE.md:28-38`: “the six recorded mutation legs'
   gates as read-only primary surfaces — kumitate `scripts/kimi-census.mjs` and
   `scripts/claims-check.mjs`, kagi `corpus/surface-census.sh` and `corpus/checklist-run.sh`,
   tsukuroi `tools/tsukuroi-census.sh`, mado `tools/mado-verify.sh`”. A seventh recorded leg
   (`kumitate scripts/round-gate.mjs`) makes this list seven and must be amended by L1/the
   operator — PROVINCE.md is outside every leaf's write scope. This is a **measured-surface
   amendment**, governed by “every surface the lane has actually measured”, not by the
   frontier rule.
2. **Calibration (C2) is not Core at all.** Box 3 is a SHONEN/SCORECARD matter
   (`SCORECARD.md:67`, `:74-75`); `QUALITY.md:43-46` keeps promotion restraint separate from
   the exercise, and `SCORECARD.md:310-312` says the outside adjudication excludes box 3 and
   `measure.py` reports `calibration_restraint_score=6` until `box3_full_page`. C2 can take
   the lane-side score to its cap 8; the final 2 still require independent promotion review.

Frontier rule to cite against any overclaim: `PROVINCE.md:40-42` — “Frontier — F1–F10 in
`corpus/README.md` `## Frontier`; ground moves to Core only through an admitted,
source-headed `knowledge/` entry whose `source:` cites a `mined` `SOURCES.md` row.”
Precedent for the same restraint: `README.md:161` “No frontier is moved wholesale to
province Core.”

## 6. Bounded recommendations

1. **Append one `## Round 16` section to `corpus/README.md`** (never insert; `:40`). It needs:
   (a) the case-7 note row required by `QUALITY.md:7`; (b) a correction to `:49` “six → seven”
   mutation-case notes; (c) a correction to `:47` marking §13 projection→measurement;
   (d) one status correction that supersedes `:143-146`, `:160`, `:190`, `:207` **only if**
   the cold-read ledger is complete at one sha; (e) a pointer from `:15` to the full-page
   ledger if box-3 coverage credit is claimed.
2. **Ledger plumbing gate:** the new line must be substituted before command D counts it —
   verified: `@@RG_KILLED@@/10` **fails** the `\d+/\d+` regex, `8/10 (80 %)` passes. Then
   update `SCORECARD.md:66`'s `:84-89` citation to include the new line, and `PROVINCE.md:29`
   six → seven.
3. **Pin the cold-read to one sha.** Snapshot `97cf436b…` is present and matches C2. If L1
   repairs SKILL.md for blocking gaps, the box-3 ledger must be keyed to the repaired sha and
   the re-read recorded; mixing shas invalidates the full-page claim (README `:99-103`,
   `QUALITY.md:13`).
4. **Run the coverage check at the round commit** (`README.md:43`); require `0`.
5. **Do not claim** F1 (interop), F2 (witness), F3 (determinism), F6 (minimization) from this
   round. Claim F8 only if the mutant-side off-suite probe is executed and recorded; a
   complete ledger alone moves no frontier item.

## 7. Remaining unknowns

- Exact filename/owner of the case-7 knowledge note: no wave-1 seat prompt fixes it; only
  PlannerWalk's checklist names “knowledge entry for the round-gate case”.
- Whether wave 2 repairs SKILL.md (C2 says blocking gaps are repaired by L1 and re-read), which
  would change the snapshot sha and re-key the box-3 ledger.
- Whether the 10-mutant sweep yields any survivor at all; F8's conditional move depends on it.
- Whether `arm-class-matrix` is appended to or forked into a new knowledge file — decides 0 vs
  1 extra QUALITY-7 row.
