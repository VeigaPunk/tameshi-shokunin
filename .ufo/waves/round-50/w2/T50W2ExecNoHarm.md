# T50W2ExecNoHarm — round-50 no-harm monitors + QUALITY-98 cold-read precheck at candidate

Seat T50W2ExecNoHarm. Lane `tameshi-shokunin`, base `e3729de862f73ae080d98fcf522a7081ce16e40a`, candidate
`80ea77e99e239982ab0b93e416645ef2359725d3`, freeze `cdbf24c07f9be3a991997c25b1f1d4bb375014ae`.
Read-only on the lane: I wrote only this report and the receipt files below it, plus a scratch clone under
`/fast/scratch/hyaku/tameshi-r50/T50W2ExecNoHarm/` (deleted before yielding). No counter was run as a verdict; the
`--selftest`/scratch-clone runs below are probes and are labelled as such.

Verdict of the assignment's own question: **not no-harm at the candidate — one of ten monitor lines is RED**
(`r45-freshness`), and the deciding run would refuse on it. The cold-read precheck is **clean (0 lost)** and the census
is **byte-identical to the frozen start receipt**. One tree cell causes the RED; no instrument or frozen byte drifted.

## Commands run (verbatim, worktree bytes equal to candidate bytes)

```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/no-harm.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin 80ea77e99e239982ab0b93e416645ef2359725d3
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin e3729de862f73ae080d98fcf522a7081ce16e40a \
     80ea77e99e239982ab0b93e416645ef2359725d3
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```
each with `HYAKU_SCRATCH=/fast/scratch/hyaku/tameshi-r50/T50W2ExecNoHarm`.

Both instruments are byte-identical to the candidate's committed bytes, so these are the deciding bytes, not a
working-tree variant:
`git show 80ea77e9:.ufo/evidence/round-50/no-harm.sh | sha256sum` = `07fa428f72977210f2c8fbfcce71ccc719172b966e73a45c1e2906c092910a3f` = `sha256sum .ufo/evidence/round-50/no-harm.sh`;
`git show 80ea77e9:.ufo/evidence/round-48/quality/coldread-precheck.sh | sha256sum` = `3b07847afc86d0d6c14d2e6c20a6b3778da1798d9304204ec3a360a6301b2924` = worktree.

## Every no-harm line, at base and at the candidate

Base `e3729de8` (`.ufo/waves/round-50/w2/T50W2ExecNoHarm.no-harm-at-base.stdout`), all ten `ok`:

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-130 130 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
```

Candidate `80ea77e9` (`.ufo/waves/round-50/w2/T50W2ExecNoHarm.no-harm-at-candidate.stdout`), nine `ok`, one `RED`:

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=74 fresh=71 C1_R45_PASS=true RED      <-- the only RED
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-130 131 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/pbt-staged-id.py A:tools/shrink-case.py ] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
```

Two observations about the instrument itself, both reproduced twice:
- `no-harm.sh` **exits 0 while printing RED** (observed `EXIT=0` on the candidate run). Its exit status is therefore
  not the gate; the gate is in the deciding script (F3).
- The line is deterministically the same value in both runs; it reads git objects only, so there is no flake here.

## Cold-read precheck (QUALITY 98) — clean

`.ufo/waves/round-50/w2/T50W2ExecNoHarm.coldread-precheck.stdout`, exit 0:

```
COLDREAD_PRECHECK floor=e3729de862f7 floor_credited=64 cand=80ea77e99e23 cand_credited=64 lost=0 ok
```

No `LOST` line, so no section lost credit and no input path drifted. Both sides sit exactly on the monitor's floor
(`score=8`, `credited=64`, `no-harm.sh:17` requires `score>=8 and credited>=64`): zero margin, nothing lost.

## Census — byte-identical to the frozen start receipt

`.ufo/waves/round-50/w2/T50W2ExecNoHarm.census.stdout` (16 lines, exit 0, empty stderr) is **byte-equal** to
`.ufo/evidence/round-50/census-start.stdout`:
`cmp` silent, `sha256sum` both `335ced1d1561c76664f2026ca28fa0c8db154383536280eff96e77377a245999`.
Every warning line (15 W-code lines, `tameshi ok …/corpus/SOURCES.md`) is the same as at freeze, so the round's
`S022`/`S024`/`S271` edits add **no** census finding — in particular the census does not see the drift in F1.

## F1 — the RED, its exact cause, and why it is not cosmetic

The monitor compares an exact string, `.ufo/evidence/round-50/no-harm.sh:18`:

```
[ "$F" = "population=73 fresh=71 C1_R45_PASS=true " ] && s=ok || s=RED; echo "NOHARM r45-freshness $F$s"
```

At the candidate the round-45 counter prints `population=74`, so the literal fails. The population is defined at
`.ufo/evidence/round-45/freshness/measure.py:95-97` (`status == 'mined' and id <= S160 and url`). Diffing the
population sets at the two revisions (command in the transcript, `git show <rev>:corpus/SOURCES.md` through
`measure.py`'s own `parse_rows`/`population`) gives exactly one member added and none removed:

```
base 73 cand 74
added ['S022']
removed []
```

The cause is one cell in one row at one commit:

- file/line: `corpus/SOURCES.md:33` (same line number at both revisions)
- commit: `79f44b55b82d0d5137546be885f0b755a9730fb6` ("round-50: content — F6 entries …, S271 and S022/S024 cells, …")
- change (cell-by-cell, `.ufo/waves/round-50/w2/T50W2ExecNoHarm.s022-row.cells.txt`):
  `status` cell `queued` → `mined` (the population flip), and `used-by` cell `—` →
  `corpus/knowledge/fixture-shrinking-pilot.md` (inert for this monitor, see F2).

Command that shows it: `git diff e3729de8 80ea77e9 -- corpus/SOURCES.md` (one hunk at `@@ -30,9 +30,9`), or
`git show 79f44b5 -- corpus/SOURCES.md`.

Why it matters rather than being a stale literal:

1. **Pre-registered.** `.ufo/evidence/round-50/contract.json:69` pins the condition in words: "r45 freshness 71/73".
   `amendments` in that contract is `[]` — nothing legalises a population of 74 after the freeze.
2. **Frozen instruments are intact, so the tree must move.** Applying the deciding script's own frozen-path list
   read-only, `git diff --quiet cdbf24c0 80ea77e9 -- <15 frozen paths>` is silent → `FROZEN_UNCHANGED=1`. Editing
   `no-harm.sh` (or the contract) to accept 74 would turn that into `0` and fail the same run another way
   (`.ufo/evidence/round-50/deciding-run.sh:37-38`).
3. **It blocks the deciding run.** `.ufo/evidence/round-50/deciding-run.sh:39-40`:
   `grep -q RED … && rc=1` and `grep -c '^NOHARM .* ok$' = 10 || rc=1`. Applying exactly those two predicates to the
   candidate capture (`.ufo/waves/round-50/w2/T50W2ExecNoHarm.gate-predicates.stdout`):
   `grep -q RED -> MATCH (deciding-run sets rc=1)`, `grep -c '^NOHARM .* ok$' -> 9`. So the round's certification is
   refused while `corpus/SOURCES.md:33` reads `mined` — independent of how C1/C2 score.
4. **It is a real ledger gap, not only a literal.** The round-45 ledger holds 73 entries at both revisions and **no
   S022 entry** (`git show 80ea77e9:.ufo/evidence/round-45/freshness/ledger.json | python3 -c …` → `entries 73`,
   `has_S022 False`; identical at base). The flip therefore promotes S022 into the verified-population model with no
   snapshot quote, no reviewer, and no independent `agree` — the very thing the round-45 C1 axis measures.

## F2 — what the counter's own line hides, and what is *not* harm

The counter's predicate still passes at the candidate (`.ufo/waves/round-50/w2/T50W2ExecNoHarm.r45-freshness-at-candidate.stdout`):

```
C1_R45: self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=80ea77e9… C1_R45_PASS=true
```
(base for comparison: `population=73 entries=73 … fresh=71 score=9 … C1_R45_PASS=true` in
`T50W2ExecNoHarm.r45-freshness-at-base.stdout`.)

`fresh` and `score` are unchanged (`floor(10*71/74) = floor(10*71/73) = 9`). The sentence `unreviewed=0` is
misleading here: `.ufo/evidence/round-45/freshness/measure.py:252` computes `unreviewed = verified - agreed - disputed`,
i.e. over *entries*, so a population row with no entry cannot appear there. The only trace is
`population=74 entries=73`. This is why the RED looks cosmetic and is not.

Not harm, checked one by one (each is a candidate edit named in my assignment):

| candidate edit | monitor that would see it | observed |
|---|---|---|
| `S024` `used-by` cell (3 entries) | r45 freshness population | inert: population depends on `status` only; probe below shows restoring `status` alone returns 73 |
| `S271` added (registry 130 → 131) | `registry-rows-not-below-130` | `131 ok`; id > S160, so outside the r45 population |
| `tools/shrink-case.py` added | `tools-scope` | `[M:tools/pbt-staged-id.py A:tools/shrink-case.py ] ok` |
| `tools/pbt-staged-id.py` error-path fix (R49.1) | `r49-generator-capability` | line byte-equal to base output, `ok` |
| `corpus/lessons/round-46.md` append, `SOURCES.md` round-50 notes, README, QUALITY, LOG, SCORECARD, two knowledge entries | cold-read floor / census | `score=8 credited=64 ok`, precheck `lost=0`, census byte-equal |

The round logs the flip deliberately and does **not** log its monitor consequence:
`corpus/lessons/round-50.md:33-35` ("**S022** status `queued` → `mined`; used-by `—` → …"). No round-50 file
(LOG, SCORECARD, README, lesson) records a red r45-freshness line, and `.ufo/evidence/round-50/after/` is still empty.

## F3 — minimality: the single `status` cell is the sole cause (scratch probe, not a verdict)

Probe tree: `git clone -q --shared <lane> $S/probe`, `git -C $S/probe rev-parse --show-toplevel` = the clone, checked
out detached at `80ea77e9`, then one field restored in the clone only —
`corpus/SOURCES.md:33` `status` `mined` → `queued` (the `used-by` cell left as the candidate has it) — committed as
`10fac8fcc00f996d4fe1163e7e58309f35380279` (parent `80ea77e9`). Running the same monitor at that probe revision
(`.ufo/waves/round-50/w2/T50W2ExecNoHarm.no-harm-at-probe-S022-status-restored.stdout`) gives all ten `ok`:

```
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM registry-rows-not-below-130 131 ok
NOHARM tools-scope [M:tools/pbt-staged-id.py A:tools/shrink-case.py ] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: … map_inadmissible=31] ok
```

So the repair that keeps every other line green is one cell, and the `used-by` half of the flip can stay. A second,
text-level probe (same `measure.py` `population()` over candidate bytes with the cell restored, no clone) confirms the
mechanism directly: `cand population = 74`, `status restored to queued, used-by kept = 73`,
`status restored + used-by restored = 73` — the `used-by` cell is inert for this monitor.

**Decision for the L1, not taken here** (evidence, not a recommendation): the contract and monitors are frozen and
must stay byte-identical (`FROZEN_UNCHANGED=1` above), so the only green-preserving routes are in the tree — restore
`corpus/SOURCES.md:33` `status` to `queued` (probe shows 10/10 ok, `used-by` may keep pointing at the F6 pilot entry),
or add a round-45 ledger entry + independent `agree` review for S022 (the r45 counter grades entries against
`ledger.json`/`reviews.json`, whose reviewers must be round-45 wave seats —
`.ufo/evidence/round-45/freshness/measure.py:24-29`; that route edits a prior round's evidence and cannot be
satisfied by a round-50 seat).

## F4 — record staleness at the candidate (lower severity, same cell)

`SCORECARD.md:2424` restates the current counting rule as `floor(10 * fresh / 73)` with `population=73 fresh=71`, and
`:2418` says every value there is the monitor output at base `e3729de8`. That is true *of base*, but at the candidate
the same rule applied to the tree gives a denominator of 74, so a reader replaying the restated rule at the candidate
gets a different population than the table names. Score happens to be 9 either way, so no numeric claim moves — the
staleness is in the rule text, and it disappears with the same one-cell repair.

## Risks / limits of this report

- One live clone at most was used (`--shared` clone in scratch), and it was deleted; no `/tmp` or scratch path is
  cited as evidence — every receipt above is copied under
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-50/w2/`.
- The probe run is a probe: it shows the cause is the one cell, it does not decide the claim.
- I did not run the counters, the C1/C2 measures or `deciding-run.sh` (the last would write receipts inside the lane
  and cannot be re-run); I evaluated its two no-harm predicates on the captured stdout instead.
- Nothing under `~/.local/state/` was read; no hidden C2 panel byte, no control `c2-*.stdout` content is quoted.
- Tooling: none installed or upgraded (Python 3.14.8, git 2.56.0, GNU bash 5.3.20 were sufficient).

## Receipts in this directory

| file | what it is |
|---|---|
| `T50W2ExecNoHarm.no-harm-at-candidate.stdout` | ten monitor lines at `80ea77e9` (9 ok, 1 RED) |
| `T50W2ExecNoHarm.no-harm-at-base.stdout` | ten monitor lines at `e3729de8` (10 ok) |
| `T50W2ExecNoHarm.no-harm-at-probe-S022-status-restored.stdout` | ten monitor lines at probe commit `10fac8fc` (10 ok) |
| `T50W2ExecNoHarm.coldread-precheck.stdout` | `lost=0`, 64/64 credited, exit 0 |
| `T50W2ExecNoHarm.r45-freshness-at-base.stdout` / `…-at-candidate.stdout` | full r45 counter output, both revisions |
| `T50W2ExecNoHarm.census.stdout` / `.stderr` / `.exit` | census validate at the candidate tree |
| `T50W2ExecNoHarm.census-vs-start.sha256` | both digests `335ced1d…` (byte-equal to `census-start.stdout`) |
| `T50W2ExecNoHarm.s022-row.cells.txt` | S022 row exploded cell-by-cell at base and candidate |
| `T50W2ExecNoHarm.gate-predicates.stdout` | deciding-run's two no-harm predicates applied to the capture |
| `T50W2ExecNoHarm.sha256.txt` | digests of every receipt above and this report |

## Summary

Nine of ten no-harm lines are `ok` at `80ea77e9`; `NOHARM r45-freshness population=74 fresh=71` is RED (base: 73/71 ok).
The cold-read precheck is clean (`floor_credited=64 cand_credited=64 lost=0`) and the census is byte-identical to `census-start.stdout` (`335ced1d…`).
Cause: `corpus/SOURCES.md:33` `status` `queued`→`mined` in `79f44b55b82d0d5137546be885f0b755a9730fb6`, which adds S022 to the round-45 population while the frozen ledger still has 73 entries and none for S022.
The counter's own predicate survives (`C1_R45_PASS=true`, fresh=71, score=9) and its `unreviewed=0` hides the gap; the frozen literal the contract pins at `contract.json:69` ("71/73") does not.
The deciding run refuses on it: `deciding-run.sh:39-40` gives `grep -q RED` MATCH and an ok-count of 9 of 10; frozen instrument bytes are intact (`FROZEN_UNCHANGED=1`), so the fix must be the tree.
A scratch-clone probe with only that `status` cell restored prints ten `ok` (population=73, registry 131, tools-scope and generator-capability unchanged) — the `used-by` half is inert.
Not harm, verified: S024 `used-by`, S271 (row 131), both tools edits, the generator capability line, cold-read and census.
Open for the L1: restore the `status` cell, or supply the round-45 ledger entry and independent `agree` review that `mined` implies — I do not decide it.
