# Round 50 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26
lane HEAD measured: `616dee6709a99c20d362ae099c50e537dd1957c2` (base `e3729de862f73ae080d98fcf522a7081ce16e40a`; counter freeze `cdbf24c07f9be3a991997c25b1f1d4bb375014ae`; content (deciding) revision `b28a9780098ec3fe69d58e257ad0d2af6323eeb0`)
driver lines (`.ufo/watchdog.log`, digest copied at closure; verified present at log lines 1574 and 1591 at closure time):
- `2026-10-26T18:31:02-03:00 launch tameshi round=50 pgid=667330 driver=hyaku-inline attempt=1`
- `2026-10-26T20:14:13-03:00 complete tameshi round=50; hyaku-inline attempt=1`

Lane gates (the round's frozen C1/C2 counters, `deciding-run.sh`, `no-harm.sh`, the round-21 cold-read monitor, `tools/shrink-case.py --selftest`) were not executed here (PROTOCOL §Gate standard, Closure consequence); their committed evidence was verified. Every other number below comes from a plain command run at closure over committed bytes (git/jq/grep/sha256sum/pdftotext).

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-50/tameshi.md` (fleet repo) | `tameshi-shokunin <tameshi@shokunin.local> 9c4be4fe… 2026-10-26 20:13:21 -0300` | ok |
| Report after its last cited commit | `git -C tameshi-shokunin log -1 --format=%ci 616dee67` | `2026-10-26 20:12:07 -0300` (< 20:13:21) | ok |
| `SHONEN` heading, one line per box | `grep -c '^- \[' report` vs `SHONEN.md` | 4 = 4 (all `[~]`) | ok |
| Cited lane commits exist and are ancestors of `master` | every 8–40-hex token in the report → `rev-parse --verify` + `merge-base --is-ancestor <h> master` | 14 commit tokens, 14 ancestors; `5c14e9a6` is the hidden-panel sha256 prefix, not a commit | ok |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain` | `local=remote=616dee67… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty | ok |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/tameshi-round-50.md) templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions differ; §6 hyaku addendum and §7 scratch follow; prompt committed by lane identity `3ce1efc3` at 18:31:00 | ok |
| Round commits by lane identity | `git log --format='%h %an' e3729de8..616dee67` | 9 commits, all `tameshi-shokunin` | ok |
| Final commit is receipts only | `git diff --stat b28a9780 616dee67` | 23 files, +93/−0: `.ufo/evidence/round-50/after/*`, `census-end.*`, `SCORECARD.md` | ok |

Not a marker: real committed round work. Status `ok`. No conformance defect found in step 1.

## Claims

### C1 — calibration (measured; gate evidence verified, inputs re-measured)

Claim: each of the 49 items routed by round-40..49 closures has one ledger row in `corpus/routed-defects.json` whose status the tree supports, fixed ≥ 20, declined ≤ 12, ≥ 5 fixes landed after base.

Committed gate evidence (verified, not executed):
- Freeze integrity: `jq -r '.sha256|to_entries[]|"\(.value)  \(.key)"' .ufo/evidence/round-50/freeze.json | sha256sum -c -` → `14 OK`; `git diff --quiet cdbf24c0 616dee67 -- contract.json c1/measure.py c2/measure.py c1/defects.json deciding-run.sh no-harm.sh` → identical; `contract.json .amendments|length` → `0`.
- Controls committed at `f87910fe` (before the wave-1 dispatch commit `65a2215b`): CTL_0 `total=74`, CTL_OPEN `74`, CTL_PLANOPEN `27`, CTL_DECLINE `64`, CTL_FAB `total=5`, all `C1_R50_PASS=false`; selftest `C1_R50_SELFTEST: cases=25 failed=0`.
- Deciding receipt `after/c1.stdout`: `rev=b28a9780… defects=49 rows=49 fixed=31 open=7 declined=11 fixed_this_round=9 … total=0 C1_R50_PASS=true`, `c1.exit` 0; `after/frozen.stdout` `FROZEN_UNCHANGED=1`; clean-tree witnesses `porcelain_lines=1` (the witness itself) / `0`.

Re-measured at closure over committed bytes at `616dee67` (ledger byte-identical to `b28a9780`: `git diff --quiet b28a9780 616dee67 -- corpus/routed-defects.json` → 0):
- `jq '.defects|length'` → 49; status split `declined=11 fixed=31 open=7`; 49 unique ids; id set equals the frozen `c1/defects.json` set (49 = 49, `count` 49).
- fixed-this-round: fixed rows whose `commit` is not an ancestor of base and is an ancestor of `b28a9780` → 9: R40.2, R40.3, R40.4, R45.2, R46.4, R47.2, R49.1, R49.2, R49.4 (matches the report).
- Every fixed row's evidence excerpt, whitespace-normalised, is found inside its cited `path:lines` range at `616dee67`: 66 of 66 excerpts.
- Declined reasons: minimum length 136 characters (≥ 40).
- All 7 open ids (R45.1, R45.4, R46.2, R47.5, R48.4, R49.3, R49.5) are named in SCORECARD `**Planned (round 51)**`.
- Cross-coding: `integrate/agreement.json` → 44 items with a cross code, 30 agree (report: 30 of 44). The five R40.x items lack a cross code because T50Cross40 wrote no json; its returned output is preserved in `.ufo/waves/round-50/w1-results.json` (its counterexample on R40.5 matches the ledger's `declined`).
- Semantic sample (the counter cannot see this; disclosed in the report): R40.4 (correction at `corpus/lessons/round-50.md:133` resolves the "11 words" → 13 tokens slip), R43.1 (m7 reconciliation and a `total=0` re-run at `ef990aa`), R47.1 (superseding SCORECARD rows), R49.2 (successor counters `successor/reads-v2.py`, `sandboxed-confirm.py` with committed selftest and panel receipts). All four rows support their status; R49.2's successor counters exist with receipts but are not yet operative (R46.2-style adoption stays open, consistent with the ledger).

Verdict: **verifies**. Axis calibration: score 8 → 8 (monitor ceiling), counter `total` 74 → 0 on the pre-registered surface. Graded `improved` (the routed-defect dispositions are now a checkable record matching repo state; that is the axis definition).

### C2 — coverage (F6 open → held; capability; measured, reproduced from receipts)

Committed gate evidence (verified, not executed):
- Controls at `f87910fe`: CTL_ABSENT `total=23` false, CTL_IDENTITY `total=20` false, CTL_REF `total=0` true (positive control: the claim is the capability with stated cost, not search efficiency — disclosed); selftest `C2_R50_SELFTEST: cases=9 failed=0`.
- Deciding receipt `after/c2.stdout`: `SELFTEST exit=0 last=SHRINK_SELFTEST: cases=14 failed=0`; 20 `MUTANT … OK` lines (12 public, 8 hidden); `C2_R50: … mutants=20 ok=20 units_before=164 units_after=43 entry=1 readme_f6=1 … total=0 C2_R50_PASS=true`; `c2.exit` 0.
- Hidden panel pin: `sha256sum .ufo/evidence/round-50/c2/panel-hidden.json` → `5c14e9a6843b3aae…cc6`, equal to `freeze.json .hidden_panel_sha256` frozen at `cdbf24c0`; the reveal landed in `b28a9780` (20:09:41), after the shrinker landed in `43bfa7ae`.

Re-measured at closure:
- `grep -oE 'units=[0-9]+->[0-9]+' after/c2.stdout | awk …` → `164->43` over 20 lines; `grep -c ' OK$'` → 20; in every line `runs` = `logged`.
- `tools/shrink-case.py` 632 lines at `616dee67`; unchanged since `43bfa7ae` (`git diff --quiet`).
- SOURCES rows `grep -cE '^ {0,3}\| S[0-9]{3,} \|'`: base 130 → 131. S271 at `corpus/SOURCES.md:146`: tier A, status `mined`, opened 2026-10-26, used-by the two F6 entries. The only changed cells in S022/S024 are `used-by` (field-wise diff); append-only rule 2 respected.
- Both F6 entries open with the provenance trio and `source: S271 …`; `ground: F6`.
- `corpus/README.md:608` appends `F6 … open → held (round 50)`, conditioned on the receipt, which prints `C2_R50_PASS=true`.

Verdict: **verifies**. Axis coverage: frontier F6 open → held, capability row added (`SCORECARD.md`, round-50 deciding section). Graded `improved`.

### No-harm (owned axes)

- `git diff e3729de8 616dee67 -- SCORECARD.md`: additions only (+36/−0); standing table re-stated with depth 9, calibration 8, freshness 9; deciding section says unchanged.
- `after/no-harm.stdout` (committed, at `b28a9780`): commandD `depth_score=9`; coldread `score=8 credited=64`; r45 freshness `population=73 fresh=71`; registry rows 131; r45/r46/r47 coverage PASS; r49 generator capability `cases=400 violations=0`; tools-scope `M:tools/pbt-staged-id.py A:tools/shrink-case.py`. Coldread precheck `64 → 64 lost=0`.
- Modified (non-added) lane files `e3729de8..616dee67`: LOG.md +13/−0, QUALITY.md +82/−0, README.md +9/−0, lessons/round-46.md +9/−0, SOURCES.md +5/−2 (two used-by cells), tools/pbt-staged-id.py +170/−40 (R49.1 error-path fix, red-before/green-after receipts in `.ufo/waves/round-50/w1/T50ExecGenFix/`). SKILL.md unchanged.
- QUALITY 101 falsifier: `quality/reach-r49.exit` 1 (`calls_measure=0 FAIL`), `reach-r50.exit` 0.

Per-axis verdicts: calibration `improved`; coverage `improved`; depth `unchanged`; freshness `unchanged`. No axis harmed.

## Discernment spot-check (LEARNING.md)

Source re-opened at closure: `curl -fsSL https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf` → 247,738 B, sha256 `7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa` (equals the row and the lesson), `pdfinfo` 17 pages; `pdftotext - - | tr -s ' \n' ' '`.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| `corpus/knowledge/delta-debugging-minimization-contract.md` (assimilated package, admitted with edits) | admit | S271 PDF (above); staged original at `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/delta-debugging-minimization-contract.md` | agree | Quote "removing any single input entity would cause the failure to disappear" → 1 hit (§I); "After 57 tests, the original 896-line HTML input is reduced to the minimal failing test case" → 1 hit; "After 82 test runs (or 21 minutes), only 3 out of 95 user actions are left" present. The admitted entry ties 57 to the HTML reduction and marks 82 + 57 = 139 as inference (`:19-25`); the staged version's errors are gone. |
| Staged S167 row and the package's "139 automated test runs" cost for the 896-line reduction | reject | same PDF; staged row at `merge/tameshi/SOURCES.append.md:21` | agree | The Abstract reads "The case study required 139 automated test runs" after naming both the 95-action and the 896-line reduction; §I gives 57 for the HTML run, so attributing 139 to that one reduction misreads the source. Anchor "p. 183-184" does not resolve: the carrier is 17 pages with no journal folios (extract opens with running head and page "1"). The staged recheck `grep -c 'minimal test case'` on the raw compressed PDF → 0 at closure. |
| `r7-ieice-mutant-abstraction-authority.md` | defer | lesson `## Gate` reasoning only (not re-fetched) | agree (reasoning) | It reduces mutant sets, not fixtures; filing it as F6 would misplace it. Graded on the stated reason, not a re-opened source. |

New SOURCES row re-opened: **S271** (`corpus/SOURCES.md:146`). Lesson quote (21 words, §I): "It stops when a minimal test case is reached, where removing any single input entity would cause the failure to disappear." → the phrase is present (1 hit), ≤ 25 words, location §I matches the extract's position (before §II). Second quote (16 words) present. Anchor names sections, definitions and figures, not printed pages: consistent with the carrier.

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, `tameshi ok …/corpus/SOURCES.md`; 15 W04 duplicate-URL warnings and 1 W01 (S101 tier C mined) all on earlier rows; none on S271, S022 or S024.

Result: agree on 1 admit and 1 reject (plus the defer). Discernment `improved`.

## Trend verdicts

- **expansion: improved** — two admitted `knowledge/` entries on F6 ground the coverage map held `open`, each `source:` citing S271 (`mined`, opened this round, quote verified above); capability row demonstrated by the deciding receipt (20/20, hidden 8/8).
- **quality: improved** — nine routed defects closed with located evidence (66/66 excerpts resolve; four rows sampled semantically); generator error paths fixed with red-before/green-after receipts; S024 re-fetched byte-identical; three named corrections to round-40 records; no admitted entry failed its re-check here.
- **discernment: improved** — the outside spot-check agrees with the gate on the admit and the reject; QUALITY 100/101 each carry a falsifier receipt (101: red at round 49, green at round 50).

## Routed defects for the lane next round

1. **S022 status contradicts its used-by cell.** `corpus/SOURCES.md` S022 is `queued` while `used-by` now names `corpus/knowledge/fixture-shrinking-pilot.md`; contract v1 defines `mined` as cited by ≥ 1 used-by path. The status was held back to keep the frozen round-45 freshness monitor at population 73. Fix the cell to `mined` and re-base or supersede that monitor (or record the exception as a named correction), logged old → new in the lesson.
2. **Gate/probe registry gap.** `tools/shrink-case.py` (round 50) and `tools/pbt-staged-id.py` (round 49) both expose selftests but have no row in `SKILL.md` `### Gate/probe registry` (`:1499-1509`, whose scope sentence still reads "these round-12 instruments"); `git diff --quiet e3729de8 616dee67 -- SKILL.md` → unchanged. Add rows (kind, entry command, verdict map incl. exit 2, selftest spelling, pinned values, write scope) per PROTOCOL §Gate standard, Registry.
3. **Frontier table stale.** `corpus/README.md:83` (F6) and `:87` (F10) still read `open`, while the appended sections at `:599` and `:608` declare them held (round 49, round 50). Append a superseding table or a note so the coverage map's table agrees with its own sections (PROTOCOL §Evidence standard, corrections sweep every mention).
4. Carried (lane-acknowledged): the seven open ledger items and the successor counters for the forgery routes disclosed in `## C1`/`## C2` (SCORECARD `Planned (round 51)`).

Operator note: SHONEN box 2 (end-to-end task logged in LOG.md) looks checkable by a non-author from the round-50 LOG entry plus `after/c2.stdout`; boxes 1, 3 and 4 still rest on lane assertion or lane-dispatched readers. Promotion stays operator-owned.
