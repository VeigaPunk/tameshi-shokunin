# T48A2CritC1Emit — the 22 restated rows against the emit receipt

Seat: T48A2CritC1Emit (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, HEAD
`17cc5ce1` (SCORECARD.md is byte-identical at HEAD and at the content revision: `git diff --name-only
c7586b9a10effc63b4bd327f976edc094c1bdc17 17cc5ce141868454d05bf75ef5cd230e35f0cdf4` lists only
`.ufo/waves/round-48/{a2w1-dispatch.err,a2w1-dispatch.json,a2w1.ready,spec-a2w1.json}`).
Judged axis: calibration. I authored none of what I attack.

## Item, restated

For every one of the 22 rows in `SCORECARD.md:2330-2356` (section `### Standing self-assessment — re-stated
at round 48`, at content revision `c7586b9a`), is the row byte-for-byte the row the frozen counter emitted at
the salvage tip, receipt `.ufo/evidence/round-48/calibration/emit-15b1521.stdout` (command in
`SCORECARD.md:2326`)? Every difference must be disclosed with a reason in the same section; an undisclosed
edit, or a disclosed edit whose reason cites no receipt, is a finding. Second: list every statement whose
observed value could differ between `15b1521e` and `c7586b9a`.

## Method (all commands read-only; no counter invocation was needed)

1. Parsed the receipt's `EMIT_CAP`/`EMIT_AXIS` lines (fields: kind, id, what/score, evidence, first) and the
   SCORECARD tables with the counter's own parser (`last_rows`/`cells_of` imported from
   `.ufo/evidence/round-48/calibration/measure.py`), then compared cell by cell.
2. Replayed the counter's own `emit_row()` with `old` = the content row and `members`/`deps`/`sha` parsed
   from the content row, i.e. what `--emit` would print at `c7586b9a`.
3. Diffed the two trees and mapped every changed path against every statement's `argv` and every tool's
   runtime reads (`statements.json` argv/obs/sha_file, `tools/*`, the four `.ufo` counters).
4. Probed the four statements whose inputs are not pure-tool (census, depth, freshness, coldread) in two
   `git clone --shared` scratch checkouts (one at each revision), running the statement's exact argv.
   Probes are evidence only, never a verdict.

## Verdict

* 19/22 capability rows: the **evidence cell is byte-identical** to the receipt. Ids, observed line, exit,
  member count, class, tool sha256 and deps clause all match for 22/22 (the three axis rows differ only in
  their prose prefix, see F1).
* 3/22 axis rows (`depth`, `calibration`, `freshness`): the evidence cell is **not** the emitted cell. The
  receipt printed the placeholder `see the evidence pointer in the round-48 SCORECARD block` (lines
  115-117, a string that appears **nowhere** in SCORECARD.md); the rows print the round-47 prose plus the
  emitted tail. Disclosed in one sentence, contradicted by the sentence beside it, reason cites no
  receipt → **F1**.
* The row set is reproducible: replaying `emit_row()` with the content row as `old` reproduces **22/22
  rows byte-for-byte**. The claim would be true against a `--emit` at `c7586b9a`; it is false against the
  cited `15b1521e` receipt because `last_rows()` finds no `runs 3` row there (0 occurrences of `runs 3` in
  `SCORECARD.md` at `15b1521e`; 22 rows plus 2 prose mentions at `c7586b9a`).
* Two scored cells changed from the round-47 rows (`sources-registry` 124→128; `six-leg regression ledger`
  FAIL/1/{env,fleet-root,node} → PASS/0/{fleet-root,node}). The class/member change is disclosed; the
  **deps drop of `env` is not** → **F3**. Both values are attested by the receipt's own lines 5 and 7.
* The calibration row's carried prose says `60 of 64 sections credited`; at both trees the monitor prints
  **57 of 64** (score 6, unchanged). 60 was the round-28–round-45 reading → **F2**.
* Part B: **no statement's observed value can differ between the two trees through the tree content.** The
  only tree-dependent difference is the counter's emit-side carry (`what`/`first`/axis prose). Details,
  probes and the complete non-tree variance list below.

## Row-by-row

`E` = evidence cell. `what`/`first` are the receipt's fields 2/4 for `EMIT_CAP`; the receipt printed them
**empty** for all 19 rows (because `last_rows` skipped the round-47 rows, which carry no `runs 3` clause),
and the rows carry the round-47 text instead — byte-identical, verified, disclosed at `SCORECARD.md:2326`
("carried unchanged from the round-47 rows"), no receipt cited (folded into F1).

| # | statement (row line) | evidence cell | emitted what/first vs row |
|---|---|---|---|
| 1 | sources-registry (2332) | exact (receipt :96) | empty in receipt / round-47 text in row |
| 2 | mutation sweep runner (2333) | exact (:97) | as above |
| 3 | six-leg regression ledger (2334) | exact (:98) | as above; scored cell changed → F3 |
| 4 | repeated pristine-control gate (2335) | exact (:99) | as above |
| 5 | six-leg content-disposition probe (2336) | exact (:100) | as above |
| 6 | exposed witness provenance correction (2337) | exact (:101) | as above |
| 7 | effective expectation reconciliation (2338) | exact (:102) | as above |
| 8 | retained invocation-context gate (2339) | exact (:103) | as above |
| 9 | hermetic env-differential probe (2340) | exact (:104) | as above |
| 10 | callback-authoritative wave accounting (2341) | exact (:105) | as above |
| 11 | required-command-receipt-binding (2342) | exact (:106) | as above |
| 12 | refusing-registry-replay (2343) | exact (:107) | as above |
| 13 | mutation report interop (2344) | exact (:108) | as above |
| 14 | tally-audit-v2 runner audit (2345) | exact (:109) | as above |
| 15 | tally-audit-v3 runner audit (2346) | exact (:110) | as above |
| 16 | bounded ANSI-C code_view (2347) | exact (:111) | as above |
| 17 | write-path-census-v2 (2348) | exact (:112) | as above |
| 18 | write-path census destination resolution (2349) | exact (:113) | as above |
| 19 | staged-id adoption guard (2350) | exact (:114) | as above |
| 20 | depth (2354) | **differs** (:115) — F1 | score 9 = emitted 9 |
| 21 | calibration (2355) | **differs** (:116) — F1 | score 6 = emitted 6 |
| 22 | freshness (2356) | **differs** (:117) — F1 | score 9 = emitted 9 |

Comparison output (script described in Method): `evidence-cell mismatching rows: 3 of 22`; for every
capability row no evidence difference was printed. Axis difference form, verified exactly:
`row_cell == round47_cell + ", runs 3 stable"` (True for depth, calibration, freshness).

## Findings

### F1 — three of 22 rows are not the emitted row, and the sentence that says they are is false

**Attacks** the claim at `SCORECARD.md:2326`: "Every evidence cell below is the counter's own `--emit`
output, pasted byte-exact: `... --rev 15b1521ea... --emit` (receipt
`.ufo/evidence/round-48/calibration/emit-15b1521.stdout`, ...)".

**Evidence**

```
$ grep -c "see the evidence pointer in the round-48 SCORECARD block" SCORECARD.md
0
$ sed -n '115,117p' .ufo/evidence/round-48/calibration/emit-15b1521.stdout
EMIT_AXIS | depth | 9 | see the evidence pointer in the round-48 SCORECARD block, tool sha256 `a7d3f2dd7d47`, deps `none`, runs 3 stable |
EMIT_AXIS | calibration | 6 | see the evidence pointer in the round-48 SCORECARD block, tool sha256 `657f009bdf1c`, deps `none`, runs 3 stable |
EMIT_AXIS | freshness | 9 | see the evidence pointer in the round-48 SCORECARD block, tool sha256 `ba64041f49ff`, deps `none`, runs 3 stable |
```

The cause is mechanical: `measure.py:356` supplies that placeholder when the counter finds no prior `runs 3`
row (`rows = last_rows(rev_sc)`; `SCORECARD.md` at `15b1521e` contains zero `runs 3` strings). The
SCORECARD rows' cells are therefore *composed*: the round-47 cell (`SCORECARD.md:2290`, `:2291`, `:2292`)
verbatim, plus the emitted tail. That composition is disclosed — `SCORECARD.md:2326`, "the axis
counting-rule prose are carried unchanged from the round-47 rows" — but (a) it contradicts the byte-exact
sentence in the same line, (b) its reason is a lane file, not a receipt. Same defect class for the 19
`what`/`first` cells (empty in the receipt, round-47 text in the rows).

**Impact**: none on C1's arithmetic — the counter scores only id, score/members, exit, sha256, deps, class
(parses `status ok`, `class stable`, deps and sha correct for 22/22), so `C1_R48_PASS` is not put at risk by
F1. The damage is to verifiability: a reader who checks the cited receipt against the rows finds three
evidence cells that are not in the receipt, and the receipt text quoted above is absent from SCORECARD.md.

**Smallest safe correction** (one appended sentence in the same section): quote the three `EMIT_AXIS`
lines above, state that the axis prose prefix is `SCORECARD.md:2290-2292` verbatim and that `what`/`first`
are `SCORECARD.md:2268-2286`, and note that a `--emit` at the content revision reproduces all 22 rows
byte-for-byte (verified: `rows reproduced byte-for-byte by CONTENT emit: 22 / 22`). Alternative (costlier):
cite a `--emit` taken at `c7586b9a` instead of `15b1521e`.

### F2 — the calibration row's carried count is stale at the revision it is scored at (calibration axis)

**Attacks** `SCORECARD.md:2355` (same text carried at `:2291`): "(`calibration_restraint_score`;
`box3_full_page=false`, **60 of 64 sections credited**)".

**Evidence** (statement argv of `axis/calibration`, run in scratch clones at each revision):

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo $S/c1 --rev 15b1521ea... [--explain]
score 6 covered 57 total 64
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo $S/c2 --rev c7586b9a...
score 6 covered 57 total 64
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo $S/c1 --rev ea25e022...   # round-45 after
score 6 covered 60 total 64
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo $S/c1 --rev 8b0e15d2...   # round-47 content
score 6 covered (not printed by that run; score 6)
```

60-of-64 is real but historical: `.ufo/evidence/round-45/after/coldread.json` and the round-28/36/44
receipts print `sections_covered: 60, sections_total: 64, score 6`. Between `ea25e02` and `15b1521e`
three sections lost credit to `input-drift` in the monitor's ledger entries (the `--explain` reason strings
name `corpus/SOURCES.md`, `corpus/knowledge/incremental-pin-disposition.md`, `tools/mutate-and-run.sh`,
`LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md` — i.e. the lane's own rounds 46-48 edits). The monitor's
score is 6 at every revision tested (the score is the SHONEN marks, `measure.py:682`, not the coverage
count), so the *observed value* the counter reads is unaffected; the *prose in the evidence cell* is wrong
by three at both trees, and the cited `--emit` receipt does not print the count at all (it prints only the
score), so no receipt attests "60 of 64".

**Impact**: none on C1 (`pick_line` for `monitor` returns only `calibration_restraint_score`); the
restated calibration row nonetheless states a measurement that its own revision contradicts.

**Smallest safe correction**: replace with "`sections_covered=57` of `sections_total=64` at `15b1521e` and
`c7586b9a` (probe: `measure.py --repo CLONE --rev REV`; 60 was the round-45 reading)", or drop the count.

### F3 — a `deps` change is not disclosed (item's enumerated difference class)

**Attacks** `SCORECARD.md:2334` vs `SCORECARD.md:2270` (round-47 row), and the disclosure at
`SCORECARD.md:2328`.

**Evidence** — the scored cells changed as follows (script diff of the parsed standing rows at
`15b1521e` vs `c7586b9a`):

```
('cap','sources-registry')       rows=124 ...  ->  rows=128 ...
('cap','six-leg regression ledger') REGRESSION: FAIL (cases=9 passed=7, exit 1,
                                    deps `env,fleet-root,node`
                                 -> REGRESSION: PASS (cases=9 passed=9, exit 0,
                                    deps `fleet-root,node`
```

Receipt attestation: line 5 (`STATEMENT cap/sources-registry: ... r1=r2=r3=rows=128 ...`) and line 7
(`STATEMENT cap/six-leg regression ledger: ... r1=r2=r3=REGRESSION: PASS (cases=9 passed=9|0 DEPS
required=fleet-root,node unstable=none never=bwrap,env,jj`). The `six-leg` paragraph at
`SCORECARD.md:2328` discloses the member and the class (`stable`, one member) and cites
`w1/T48RevenRegression.md` and `w1/T48ExecObs2.md` — it never mentions that the declared dependence set
lost `env`. The `sources-registry` member change (`rows=124`→`128`; the four C2 rows S265-S268 at
`5054532`) has no row-specific sentence at all; only the blanket "these cells are emit output".

**Impact**: none on C1's pass condition (both cells are exactly the emitted ones and the receipt attests
them), but the item names "deps changed" as a difference that must carry its reason, and it does not.

**Smallest safe correction** (one clause each): at `SCORECARD.md:2328`, "the deps clause also drops `env`
(round-47 declared `env,fleet-root,node`); receipt line 7 records `required=fleet-root,node ...
never=bwrap,env,jj`, i.e. removing the environment changed nothing in any of the three rounds"; and for
`sources-registry`, "`rows=128` = the round-47 `124` plus the four C2 rows S265-S268 opened this round".

### F4 — the disclosed cause of `fleet_drift=1` is not in the receipt (minor)

**Attacks** `SCORECARD.md:2328`: "The emit's verdict line prints `fleet_drift=1` because the L1 edited
`corpus/lessons/round-48.md` in the worktree during it (FLEET points 2-4 `lane_clean=0`); ...".

**Evidence** — the receipt lines 1-4 are

```
FLEET point=1 ... lane_clean=1 ...
FLEET point=2 ... lane_clean=0 ...
FLEET point=3 ... lane_clean=0 ...
FLEET point=4 ... lane_clean=0 ...
```

`measure.py:fleet_state` reduces the dirtiness to one boolean over the paths `corpus`, `tools`,
`SCORECARD.md`; the FLEET line names no path. `git diff --name-status 15b1521e c7586b9a` modifies **five**
paths (`LOG.md`, `SCORECARD.md`, `considerthese/2026-10-26.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-48.md`), three of them inside the checked set, so `corpus/lessons/round-48.md` is a
plausible but unrecorded cause; the receipt cannot distinguish it from `SCORECARD.md` or `corpus/QUALITY.md`.
The disclosure itself (drift, points 2-4, values unaffected because observations are clones of REV) is
correct and is verified in the counter: `setup_profile()` clones the lane and `checkout --detach REV`;
`fleet_state()` reads only the live worktree.

**Impact**: none on values; the sentence presents an inference as the recorded cause.

**Smallest safe correction**: say "the FLEET line records only `lane_clean=0` at points 2-4 (worktree
dirty for corpus/, tools/ or SCORECARD.md during the 09:27:44-10:22:25 -03 run)" and, if the cause matters,
attach a dated `git status --porcelain -- corpus tools SCORECARD.md` receipt.

## Part B — statements whose observed value could differ between `15b1521e` and `c7586b9a`

Tree difference (`git diff --shortstat 15b1521e c7586b9a`): `23 files changed, 648 insertions(+), 25
deletions(-)`; outside `.ufo/evidence/round-48/*` and `.ufo/waves/*`:

```
 LOG.md                      | 11 ++++++
 SCORECARD.md                | 49 +++++++++++++++++++++++++
 considerthese/2026-10-26.md | 88 +++++++++++++++++++++++++++++++++++++++++++++
 corpus/QUALITY.md           |  8 +++++
 corpus/lessons/round-48.md  | 45 +++++++++++------------
 5 files changed, 176 insertions(+), 25 deletions(-)
```

**Answer: none of the 22 statements' observed values can differ because of this diff.** Every statement
resolves its value from a clone checked out at `REV` (`setup_profile`: `git clone` + `checkout --detach
REV`; `observe` runs with `cwd=clone|mirror`) or from `git show REV:...`; the changed paths are read by no
statement:

* 22/22 `sha_file`s are byte-identical at both revisions (script: no `SHA DIFF` lines), so every tool-sha
  clause is tree-insensitive; `tools/` is untouched by the diff.
* `corpus/SOURCES.md`, `corpus/knowledge/*`, `SKILL.md`, `SHONEN.md`, `.ufo/evidence/round-21/coldread/
  ledger.json` are untouched by the diff (`git diff --stat ea25e02 15b1521e -- SKILL.md SHONEN.md <ledger>`
  and `15b1521e c7586b9a -- ...` are both empty).
* No statement tool reads `corpus/QUALITY.md`, `corpus/lessons/round-48.md`, `LOG.md`, `SCORECARD.md`,
  `considerthese/` or `.ufo/evidence/round-48/` (`grep -n SCORECARD tools/*.py tools/*.sh
  .ufo/evidence/round-15/verify.py .ufo/evidence/round-21/coldread/measure.py
  .ufo/evidence/round-45/freshness/measure.py .ufo/evidence/round-18/measure.py` → no hits; the only
  `corpus/` hits in tools are docstrings, fixture text and leg paths in sibling lanes).

Probes (statement argv, scratch clones at each revision; probes, not verdicts):

| statement | command | 15b1521e | c7586b9a |
|---|---|---|---|
| sources-registry | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | `rows=128 ... CLEAN`, exit 0 | identical |
| depth | `git show "$REV:tools/mutate-and-run.sh" \| python3 -c ...` | `recorded_cases=9 depth_score=9` | identical |
| freshness | `python3 .ufo/evidence/round-45/freshness/measure.py --lane CLONE --rev REV` | `fresh=71 score=9`, exit 0 | identical |
| calibration | `python3 .ufo/evidence/round-21/coldread/measure.py --repo CLONE --rev REV` | score 6, covered 57/64 | score 6, covered 57/64 |

**What does differ between the trees is the counter's emit-side carry**, not an observation: at
`15b1521e` `last_rows()` finds no `runs 3` row (`grep -c "runs 3"` → 0), so `--emit` prints empty
`what`/`first` and the axis placeholder; at `c7586b9a` it finds the 22 rows and reproduces all of them
byte-for-byte (probe: `emit_row()` replayed with `old` = content row → 22/22). This is exactly F1.

**Statements that can differ for reasons outside the tree** (not caused by the diff, and declared):
`six-leg regression ledger` (one-sided PASS→FAIL SIGPIPE race; receipt repeats PASS/0 at P0 and P1 in all
three rounds; round-47 disclosed and w1 reports cited at `SCORECARD.md:2328`); `hermetic env-differential
probe` (P2 `2/9`, P4 `8/9` under the dependence-removing variants, receipt lines 36/59/82; round-47's P1
host-load instability is a prior round's disclosure); `retained invocation-context gate` (P5 exit 1 under
the decoy fleet-root — a declared dependence, not instability); and the live fleet itself: `sibling_moves=4`
in the receipt label, which amendment 5 says is disclosed but not drift (legs are pinned blobs).

## Verified, no finding

* All 22 rows parse `status ok`, `class stable`, with the receipt's members, sha256 prefixes and deps sets
  (script output; rows include `six-leg` `deps ['fleet-root','node']`, `hermetic` `['bwrap','node']`,
  `calibration` `[]`, `freshness` `[]`).
* P0 == P1 in every round for every statement (script: 0 rows with `P0!=P1`; one distinct P0 and one
  distinct P1 over three rounds for each of the 22) — supports the section's sentence at `:2326` about
  `runs 3 stable`.
* The receipt's metadata matches the section: `emit-15b1521.exit` = `1`, `emit-15b1521.time` =
  `real 54m41.058s`, `ROUND 1..3` of `PROFILES ... P0..P5`, `START 2026-10-26T09:27:44-03:00`, `END
  2026-10-26T10:22:25-03:00`.
* Counter and statements pins match `freeze-2.json`: `measure.py` sha256 `572a5670deb7...` and
  `statements.json` sha256 `924102dfbc...` at `7552984`, `15b1521e` and `c7586b9a`; the receipt prints
  `self_pin=1 stmts_pin=1`.
* `SCORECARD.md` is append-only `15b1521e → c7586b9a` (+49 lines, no deletions) and the round-47 rows
  remain as dated literals.
* The lane worktree is clean for the deciding run's checked paths: `git status --porcelain -- corpus tools
  SCORECARD.md` is empty and `git diff --quiet c7586b9a -- corpus tools SCORECARD.md` passes at HEAD
  `17cc5ce1`.
* `what`/`first` cells of all 19 capability rows are byte-identical to the round-47 rows
  (`SCORECARD.md:2268-2286`); the three axis cells are the round-47 cells (`SCORECARD.md:2290-2292`)
  plus `, runs 3 stable`.

## Tooling and scratch

No tool installs or upgrades. Scratch root
`/fast/scratch/hyaku/tameshi-r48/T48A2CritC1Emit` held two `git clone -q --shared` checkouts (`c1` at
`15b1521e`, `c2` at `c7586b9a`) and the probe `HOME`/`TMPDIR`; it is removed at the end of this seat (no
tree left on disk, nothing under `/tmp`, disk guard read before the pass: `/fast` 604.0G free). Receipts
cited in this report are committed lane files; probe outputs are quoted inline above so no scratch artifact
is needed.
