# CriticRecordNoHarm — round 27 records and no-harm

Seat: TameshiR27.CriticRecordNoHarm (critic, leaf). Range attacked:
`91edf9cd82ccc72e10f62f81d37181f549d593b8..2227d8338c02aa9a5fd7d95c1a41b76865ad7647`.
All code ran in my own clone `/tmp/crnh/clone` (cloned from the lane, checked
out at `2227d83`). Nothing in the lane was run or written except this file.
Tools installed or updated: none.

## Verdict

1. **Records: numbers are correct, but one citation is wrong and one record
   is missing.** Every number in the two SCORECARD sections matches the
   receipts and my own re-runs. Two problems are fixable:
   - The correction says restraint 6 at `40a12bf` and backs it with
     "committed receipts `monitor-harmed-*.json`". No such receipt exists for
     `40a12bf`. The receipts cover `a08e85c`, `d2206cd` and `2b064cf`, and
     `a08e85c` is not named in the text. The value is still true: I re-measured
     `40a12bf` at 25/64, restraint 6. Only the cited source is wrong.
   - The SCORECARD round-27 block says both counters were frozen at
     pre-registration. It never mentions contract amendment 1, which landed in
     `2227d83` and decides whether C2 reaches its target. This is the same
     defect the round-26 closure routed for round 25 (a SCORECARD block that
     left out amendment 3).
   - **Append-only rule: kept.** Every changed file has 0 deleted lines except
     `corpus/SOURCES.md`, which has 1 line deleted and 3 added. That one change
     is the S012 row, and only its `status` and `used-by` cells changed, which
     CORPUS.md rule 2 allows.
2. **No-harm: no harm at `2227d83`, but there is a landing-order risk for C1.**
   The runner, the registry, SKILL.md and the monitor code did not change. The
   monitor reads the same 25/64, restraint 6, depth 9 at base, at `70df8d6` and
   at `2227d83`, with the same list of uncovered sections. The risk is that
   some record files are inputs that the cold-read monitor checks. Two of this
   round's cold-read traces already record `SHONEN.md` and `corpus/README.md`
   at their `2227d83` bytes. Any record edit to those files after the cold
   reads will drift those sections at the landed head. The `not_claimed`
   rationale only names runner edits as a drift source.
3. **Amendment 1 is a contract-legal correction, not a narrowing of the C2
   target.** The target (`classified=4`), the population (four survivors) and
   checks 1 and 2 are byte-identical to the frozen counter. Only the S012
   precondition in check 3 changed, and the frozen version could not be met
   without breaking CORPUS.md rule 2. However, the amendment decides the C2
   outcome: the frozen counter reads `classified=0` at `2227d83`, and the
   amended counter reads `classified=4`. It also drops the only machine check
   that S012 was re-opened this round. Its stated replacement,
   `corpus/lessons/round-27.md ## Gate`, is not committed at `2227d83`.

## Evidence

### 1. SCORECARD numbers against receipts

Commands, all run in `/tmp/crnh/clone`:
`python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev R`.

| rev | observed first line | rc |
|---|---|---|
| d4140796 | `covered=62/62 restraint=8 box3_mismatch=0 depth_score=8` | 0 |
| 40a12bf | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| a08e85c | `covered=32/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| d2206cd | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| 2b064cf | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| e08444d3 | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| 91edf9cd | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| 70df8d6 | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| 06a6707 | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| 2227d83 | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |

- Round-26 receipts. I read them with
  `jq '{r:.calibration_restraint_score, ...}'`:
  - `monitor-harmed-a08e85c.json`: restraint 6, 32/64, `box3_full_page` false.
  - `-d2206cd.json`: restraint 6, 25/64, `box3_full_page` false.
  - `-2b064cf.json`: restraint 6, 25/64, `box3_full_page` false.
  - **No `monitor-harmed-40a12bf.json` exists.** The directory
    `.ufo/evidence/round-26/after/` holds only the `c1-measure`, `c2-measure`,
    `commandD` and `registry` files for `40a12bf`.
- Closure citations all check out:
  - `corpus/lessons/round-26-verifier-spotcheck.md:120-123` is the monitor
    table: d4140796 is 62/62, restraint 8; e08444d3 is 25/64, restraint 6. This
    matches the SCORECARD citation.
  - `:130-135` is the per-axis ruling "calibration — harmed", matching the LOG
    citation.
  - `:112-135`, cited by QUALITY 53, is correct.
  - `:225-228` is routed item 4, matching the QUALITY 54 citation.
- `SCORECARD.md:1325-1328` (at `2227d83`) says "restraint 6 at `40a12bf`,
  `d2206cd`, `2b064cf` and the landed head `e08444d3` (committed receipts
  `.ufo/evidence/round-26/after/monitor-harmed-*.json` …)". For two of these
  revisions the evidence is elsewhere: e08444d3 is backed only by the closure
  table, and 40a12bf by nothing committed. `40a12bf` is the measured commit of
  the round-26 C2 row being corrected, so it is the revision the correction
  depends on most.
- "Calibration was harmed in round 26, 8 → 6" matches closure `:131-135` and
  the table above.
- C1 before-value at base (SCORECARD round-27 block and LOG):
  `covered=25/64 restraint=6 box3_mismatch=1`, exit 1. This equals
  `c1-before.stdout` line 1 and `c1-before.exit` = `1`. My re-run at `91edf9cd`
  has an identical uncovered list (`diff` against `c1-before.stdout` lines 2+
  is empty).
- C2 before-value: `survivors=4 classified=0 anchored_holes=0`, exit 1. This
  equals `c2-before.stdout`, `c2-before-amended.stdout` and both `.exit` files
  (`1`), and it matches my re-runs of both the frozen and the amended counter
  at `91edf9cd`.
- The amendment is missing from the SCORECARD round-27 block.
  `SCORECARD.md:1336-1338` says "frozen in `.ufo/evidence/round-27/contract.json`
  with both counters before any content edit". That block landed in `70df8d6`.
  The `2227d83` diff to SCORECARD is empty: `git diff --numstat` lists SCORECARD
  48/0 for the whole range, and all 48 lines came from `70df8d6` per
  `git log -- SCORECARD.md`. LOG.md does not name the amendment either. Only
  the commit subject, the counter docstring and the uncommitted lesson do.
- Append-only check. Command:
  `git diff --numstat 91edf9cd… 2227d83…`. Deleted-line column:
  - `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md` and `corpus/README.md`: 0.
  - `corpus/SOURCES.md`: 1. The deleted line is S012, and only `queued → mined`
    and `— → corpus/knowledge/oracle-anchored-survivors.md` changed. `opened`
    (2026-10-19) and `recheck` (90d) are unchanged.
  - All 18 `.ufo/evidence/round-27/**` files and the new entry are added files.
  - The SCORECARD additions are at end of file.

### 2. Changed files and the axis each could harm

Read-only `git diff --name-status` for the range, all under the lane root.
`tools/mutate-and-run.sh` (the runner), `tools/registry*`, `SKILL.md`,
`.ufo/evidence/round-18/measure.py` and `.ufo/evidence/round-21/coldread/*`
are **not** in the diff.

| file | change | axis it could harm | observed |
|---|---|---|---|
| `.ufo/evidence/round-27/c1-measure.py` | A | calibration (counter wraps the monitor) | Runs the round-21 monitor unchanged, with no override flag. Refuses non-strict or override output (`:40-42`). |
| `.ufo/evidence/round-27/c2-measure.py` | A, then edited in `2227d83` | coverage (C2 ruler) | See section 3. |
| `.ufo/evidence/round-27/contract.json`, `contract-amendment-1.json` | A | calibration (record) | Amendment not reflected in SCORECARD. |
| `.ufo/evidence/round-27/{before-rev.txt,c1-before.*,c2-before*.*,census-start.*}` | A | none (receipts) | Values reproduced. |
| `.ufo/evidence/round-27/f8/{anchor-probe.py,anchors.json,receipt.json,probe.*}` | A | coverage (C2 inputs) | Anchors were committed in `06a6707` (09:17:23). The receipt mtime is 09:17:25, so the probe ran after the anchors were committed. |
| `SCORECARD.md` | +48/0 | calibration (record); monitor (traced input) | Citation and omission defects above. |
| `LOG.md` | +15/0 | monitor (traced input) | No drift at `2227d83`. |
| `corpus/QUALITY.md` | +22/0 | discernment; monitor (traced input) | No drift at `2227d83`. |
| `corpus/README.md` | +13/0 | coverage (F8 status); monitor (traced input) | No drift at `2227d83`. |
| `corpus/SOURCES.md` | +3/-1 | freshness, sourcing; monitor (traced input) | Rule-2-legal change. |
| `corpus/knowledge/oracle-anchored-survivors.md` | A | coverage, quality | Not traced by the ledger. |

No-harm readings:
- **Monitor and calibration.** No new drift: 25/64, restraint 6 at base, at
  `70df8d6` and at `2227d83`, with an identical uncovered list
  (`diff` of `mon-91edf9cd.txt` against `mon-2227d83.txt` is empty).
- **Depth.** Holds at 9 on the same monitor.
- **Registry and runner.** Their bytes are unchanged in the range, so the
  operability inputs are unchanged. I did not run `registry-check.py`. The
  lesson's own `held=46/49` reading comes from a clone outside a fleet mirror,
  which is a setup issue it already records.
- **Census.** Only the start receipt exists (`census-start.stdout`). There is
  no end receipt yet, so there is no no-harm reading for it.
- **Ordering risk for C1** (the strongest counterexample I found).
  - The monitor drops a section's credit when any of its traced inputs (a
    whole-file sha256) differs at the measured revision. The only ignored keys
    are `SKILL.md` and the ledger files
    (`.ufo/evidence/round-18/measure.py:135,321-327`).
  - In the ledger at `2227d83`, record files are traced inputs:
    - `corpus/SOURCES.md` by 16 headings, `corpus/README.md` by 9,
      `corpus/QUALITY.md` by 6 and `SHONEN.md` by 4.
    - `SCORECARD.md` and `LOG.md` by 2 each, including `## Standing rules`
      (entry read at `01d586dd`), which is uncovered now.
  - This round's uncommitted traces already include two record files:
    - `coldread/traces/Read25-7.json` reads `SHONEN.md` (sha256 `55a4fceb…`).
    - `coldread/traces/Read23-7.json` reads `corpus/README.md` (`33915658…`).
    - Both equal the `2227d83` bytes.
  - The lesson says every cold read is made at `2227d83`. The SCORECARD says
    "Measured results are appended below only after execution". If that
    append, a SHONEN box edit, a README closure or a SOURCES or QUALITY edit
    lands after the cold reads, the sections whose new entries trace that file
    lose credit at the landed head. C1 would then miss `covered=T/T`, and the
    reason would be the round's own record writes, not the runner.

### 3. Amendment 1: narrowing or correction

- **The diff is only check 3.** `diff` of the `70df8d6` version against the
  `2227d83` version of `c2-measure.py` shows three hunks: the docstring for
  check 3 (`:22`), the parser now keeps the `used-by` cell (`:53`), and the
  check itself (`:79`):
  `s012.get('opened') == OPENED` became `ENTRY in s012.get('used_by', '')`.
  - The survivor IDs, the anchor check (check 1, which still requires
    external rows opened 2026-10-22) and the digest-bound receipt check
    (check 2) are unchanged.
  - The target `classified=4, exit 0` is unchanged in `contract.json`.
- **The frozen check was unreachable legally.** CORPUS.md
  (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-117`) says: "Only `status`,
  `recheck` and `used-by` change in place". S012's `opened` cell has read
  2026-10-19 since round 1. The frozen counter could therefore only pass by
  breaking the SOURCES contract.
- **The amendment decides the outcome.**

  | counter | rev | result | rc |
  |---|---|---|---|
  | frozen | `2227d83` | `classified=0 anchored_holes=0` (all four `F8 entry or mined S012 missing`) | 1 |
  | amended | `2227d83` | `classified=4 anchored_holes=4` | 0 |
  | both | `91edf9cd`, `70df8d6`, `06a6707` | `classified=0` | 1 |

  The before-value with the amended counter (`c2-before-amended.stdout`) is
  correct.
- **Neither precondition is stronger.** The old one required "re-opened this
  round" (the date). The new one requires "linked to the entry" (`used-by`).
  The new check accepts a row nobody re-opened, as long as `used-by` names the
  entry. So this is a substitution of the precondition, not a narrowing of the
  target or the population.
- **The stated replacement is not in the committed bytes.** Rule 2 also
  requires each in-place change to be "logged old→new in the round lesson".
  The amendment says the re-open "is recorded with its quote in
  corpus/lessons/round-27.md ## Gate". At `2227d83` that file is untracked
  (`git status --short`: `?? corpus/lessons/round-27.md`;
  `git ls-tree 2227d83 corpus/lessons` does not list it). So at the content
  revision, the S012 change is unlogged and the re-open has no committed
  record. This is false provenance until the lesson lands.
- **Timing.** `git log` puts the amendment and the S012 edit in the same commit
  (`2227d83`, 09:19:08), so git cannot prove "before the S012 row was edited".
  Working-tree mtimes are consistent with the claim:
  - `c2-measure.py` 09:17:52, before `corpus/SOURCES.md` 09:18:08.
  - The amendment was written after the probe receipt (09:17:25).

  [INFERENCE] Mtimes record only the last write, and the probe outcome could
  not steer this change, because check 3 does not touch classification logic.

## Smallest safe corrections

1. Add one appended sentence to SCORECARD (for example, in the round-27
   measured-results block) that does two things:
   - Cites the real evidence for `40a12bf`. Either commit
     `c1-measure.py --rev 40a12bf` output as a receipt (observed:
     `covered=25/64 restraint=6 box3_mismatch=1`), or replace `40a12bf` with
     `a08e85c` in the receipt claim and name the closure table for `e08444d3`.
   - Names contract amendment 1, its commit `2227d83`, and that the frozen
     counter reads `classified=0` at `2227d83` while the amended counter reads
     `classified=4`.
2. Commit `corpus/lessons/round-27.md` with its `## Gate` S012 old→new log
   before the C2 after-measurement is recorded, so both the amendment's
   provenance and CORPUS.md rule 2 hold in committed bytes.
3. Land every record edit to `SCORECARD.md`, `LOG.md`, `SHONEN.md`,
   `corpus/README.md`, `corpus/SOURCES.md` and `corpus/QUALITY.md` before the
   cold-read content revision is frozen. Otherwise, re-read the sections whose
   traces name them. Then measure C1 at the actual landed head, as the
   contract already requires. Extend the `not_claimed` drift rationale from
   the runner to these record files.

Checks for the integrator:
- `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev LANDED_HEAD`
- `python3 .ufo/evidence/round-27/c2-measure.py --repo CLONE --rev LANDED_HEAD`
- `GIT_OPTIONAL_LOCKS=0 git ls-tree LANDED_HEAD corpus/lessons/round-27.md`
