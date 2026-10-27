# T51ExecS022Fresh — what C1's S022 status cell does to the freshness axis

Seat `T51ExecS022Fresh`. Lane `tameshi-shokunin`, base `9962033fd7a75aa2f2847e979dd687a5d28505a1`, fixture commit
`84aa673a1a476e48ccf239335696f0518d08bae7`. Read-only on the lane: I wrote only this report and
`T51ExecS022Fresh.rec/` under `.ufo/waves/round-51/w1/`, plus one scratch clone at
`/fast/scratch/hyaku/tameshi-r51/T51ExecS022Fresh/` (deleted before yielding). No counter was run as a verdict; every
run below is a probe on a scratch clone, reported as observed. No tool was installed or upgraded (nothing was needed).

## The change, and that it is one cell

```
git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/lane
git -C $S/lane rev-parse --show-toplevel          -> /fast/scratch/hyaku/tameshi-r51/T51ExecS022Fresh/lane
git -C $S/lane checkout -q 84aa673a1a476e48ccf239335696f0518d08bae7
# edit: corpus/SOURCES.md:33, status cell only  queued -> mined
git -C $S/lane commit  -> 7056e59d4a3ef14293275153ea02d3f78666945b (parent 84aa673)
```

- `git diff --numstat 84aa673 7056e59d` → `1 1 corpus/SOURCES.md` (`rec/numstat.txt`); `git diff --word-diff=plain`
  shows exactly `| [-queued-]{+mined+} |` and no other change in the row (`rec/sources-worddiff.txt`).
- sha256 `corpus/SOURCES.md`: base `b97dbc5768a476a23214280aa54ba372515e54178f304cecc955d3a10ae544ea` →
  after `1f88649cdb58510c764261c1c8a55d9b9630d3f088dd5a1211149212fd5f25b5` (`rec/pins.txt`).
- Row before/after (`rec/status-scan.txt`):
  `S022 status=queued used=corpus/knowledge/fixture-shrinking-pilot.md` → `S022 status=mined used=<same path>`.
- Append-only rule 2 (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49`: only `status`, `recheck`, `used-by` change in
  place, each logged old→new in the round lesson) is satisfied by this diff; the log line is drafted below.

## Freshness axis — round-45 monitor, base vs after

Command (each rev):
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --lane $S/lane --rev <rev>`
(`rec/freshness-base.txt`, `rec/freshness-after.txt`; exit 0 both).

| rev | observed line | population | entries | fresh | score | PASS |
|---|---|---|---|---|---|---|
| base `84aa673` | `C1_R45: self_pin=1 population=73 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=84aa673… C1_R45_PASS=true` | 73 | 73 | 71 | 9 | true |
| after `7056e59d` | `C1_R45: self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=7056e59d… C1_R45_PASS=true` | **74** | 73 | 71 | **9** | true |

`DISPUTED S048` and `DISPUTED S093` are the only state lines in both runs; S022 produces no state line and no
`INVALID` line. Population, fresh and score floor(10·fresh/population) = floor(710/74) = 9. The freshness axis value
(9 at base per the contract) is unchanged: this cell cannot raise or lower it.

Why S022 is invisible to the monitor: it is now in `population()` (`measure.py:95-97`: status `mined`, id ≤ 160,
http(s) URL) but has no round-45 ledger entry — `git show HEAD:.ufo/evidence/round-45/freshness/ledger.json | grep -c S022`
→ `0`, same for `reviews.json` — and the state loop visits ledger entries only (`measure.py:235-250`), so a population
row without an entry is never classified. It contributes to the denominator only.

## Round-51 no-harm — every line, base and after

Command (each rev):
`HYAKU_SCRATCH=$S bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/no-harm.sh $S/lane <rev>`
(`rec/noharm-base.txt`, `rec/noharm-after.txt`; exit 0 both, 11/11 `ok` both).

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=73 fresh=71 score=9 ok        <-- after: population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-131 131 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
```

At `7056e59d` the list is byte-identical except `NOHARM r45-freshness population=74 fresh=71 score=9 ok`. Two
consequences worth carrying: `coldread-floor score=8 credited=64` at both revs, so a one-cell `corpus/SOURCES.md`
change triggers **no** round-21 re-key (the re-key obligation the contract attaches to `tools/mutate-and-run.sh` and the
SKILL.md registry section does not reach this edit); and `tools-scope []` at both revs, no `tools/` byte changed.

## The C1 side-effect, measured

`python3 .ufo/evidence/round-51/c1/measure.py --lane $S/lane --rev <rev> --explain` (`rec/c1-base.txt`,
`rec/c1-after.txt`; exit 1 both — inside the counter's documented `1 not PASS`).

- base: `frontier_rows=10 table_rows=10 frontier_bad=10 readme_prefix=1 sources_rows=131 status_conflicts=1 usedby_missing=0 total=11 C1_R51_PASS=false`, with `SOURCES S022: queued-with-used-by corpus/knowledge/fixture-shrinking-pilot.md`.
- after: `… status_conflicts=0 usedby_missing=0 total=10 C1_R51_PASS=false`, no `SOURCES` line at all.

An independent scan of the same rule (`rec/status-scan.txt`) finds `queued_with_usedby=['S022']` at base and `[]`
after, `mined_without_usedby=[]` at both, 131 rows at both. So S022 was the entire `status_conflicts` term: the move
removes exactly 1 of C1's 11, and C1's remaining total is now purely the frontier table (untouched by this seat).

## Does S022's used-by really cite S022?

Yes, on live bytes at `7056e59d`:

- `corpus/knowledge/fixture-shrinking-pilot.md:2` — `source: S022 — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 — Abstract — MacIver & Donaldson, …`; the URL string is the row's own source URL (`grep -c` on that exact URL in the entry → 1) and it appears once, in the `source:` line.
- `corpus/knowledge/fixture-shrinking-pilot.md:32` — `- **A reduced case must still be a valid input.** S022, Abstract: …` (a second in-body citation).
- `git -C $S/lane cat-file -e HEAD:corpus/knowledge/fixture-shrinking-pilot.md` → exists, hence `usedby_missing=0`.
- Definition applied: `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:36` — `` `mined` (cited by ≥1 path in `used-by`) ``;
  routed as defect 1 at `corpus/lessons/round-50-verifier-spotcheck.md:98`.

Head of the entry, as requested (`head -5 corpus/knowledge/fixture-shrinking-pilot.md`, source lines abbreviated to
their `S-id — URL` heads): `source: S271 — …` / `source: S022 — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 — Abstract …` /
`source: S024 — …` / `verified-at: 2026-10-26` / `recheck: 365d — …`.

## Census on the scratch registry

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md`
(`rec/census-base.txt`, `rec/census-after.txt`) → exit 0 at both revs, last line
`file	ok	…/lane/corpus/SOURCES.md`. The warning sets are identical before and after (`diff` of the two, paths
normalized, prints nothing): 15 warnings, 14 × `W04 duplicate url … across scopes` (S047 S048 S075 S076 S077 S078 S081
S092 S104 S160 S265 S266 S267 S268) and 1 × `W01 S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md`
(`grep -c W04` → 14, `grep -c W01` → 1); none names S022, and the count is unchanged because no row was added or removed.

## Draft lesson-log line (for `corpus/lessons/round-51.md`, "rows touched old → new")

```
- **S022** status `queued` → `mined`; reason: contract v1 defines `mined` as cited by ≥1 path in `used-by`
  (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:36`), and S022's `used-by` has named
  `corpus/knowledge/fixture-shrinking-pilot.md` since round 50 (`corpus/SOURCES.md:33`), whose `source:` line cites
  S022 (`corpus/knowledge/fixture-shrinking-pilot.md:2`). Routed by
  `corpus/lessons/round-50-verifier-spotcheck.md:98` (defect 1). Measured consequence (seat T51ExecS022Fresh,
  `rec/freshness-*.txt`, `rec/noharm-*.txt`): round-45 freshness population 73 → 74, fresh 71 unchanged, score 9
  unchanged, `C1_R45_PASS=true` both; round-51 `NOHARM r45-freshness population=74 fresh=71 score=9 ok`; C1
  `status_conflicts` 1 → 0 (`total=11` → `total=10`). No freshness credit: S022 has no round-45 ledger entry, so the
  monitor counts it in the denominator only.
```

## Findings and risks (each with the command that shows it)

1. **The freshness denominator now contains a row the monitor cannot see.** `population=74 entries=73` with no state
   line for S022 (command above) follows from `measure.py:95-97` (population = mined + id ≤ 160 + URL) versus
   `measure.py:235-250` (states assigned only to ids present in the ledger). Nothing is red today (target is
   `fresh >= 50`, `measure.py:60,256`), but "fresh 71 of 73 checked" is no longer a description of the 74-row
   denominator. If a later round wants S022 counted, it needs a ledger entry (snapshot bytes + quote + author) plus an
   independent `agree` review (`measure.py:6,24-30` docstring and `review_sets` at `:192`) — arithmetic then still
   reads 10·72//74 = 9.
2. **The green depends on round-51's frozen re-base, not on the cell alone.** Round 50 tried the same cell and the
   then-frozen monitor printed `NOHARM r45-freshness population=74 fresh=71 C1_R45_PASS=true RED` (round-50 receipt
   `.ufo/waves/round-50/w2/T50W2ExecNoHarm.md`, "the only RED"; `corpus/lessons/round-50.md:148-149` records the cell
   being restored) because it pinned `population == 73` exactly. The green above holds only because
   `.ufo/evidence/round-51/no-harm.sh:5,23` now checks `fresh >= 71` and `floor(10·fresh/pop) >= 9`. That re-base is
   declared in the contract; it is disclosed here as the sole reason this edit is no-harm now.
3. **Score headroom is four rows.** With `fresh=71`, floor(10·71/pop) = 9 for pop ≤ 78 and 8 at pop 79
   (`python3 -c` ladder over 73…80). C2 adds one mined row (S272) → projected 75 → 9; three further mined rows with no
   agree review would take the freshness axis to 8.
4. **Axis value unchanged.** The S022 move is a calibration fix that the freshness axis tolerates, not a freshness
   gain: population grew, fresh did not, the score floor stayed 9. It also does not touch the coverage-map table, so
   C1's `frontier_bad=10` is untouched by this seat (`rec/c1-after.txt`).
5. **No cold-read or tooling impact.** `NOHARM coldread-floor score=8 credited=64 ok` and `NOHARM tools-scope [] ok` at
   both revs — this seat creates no re-key obligation and leaves `tools/` and every SKILL.md section as they were.

## Summary

S022's status cell `queued → mined` at `corpus/SOURCES.md:33` is a one-cell, append-only-rule-2-compliant change
(sha256 b97dbc57 → 1f88649c) whose used-by path genuinely cites it.
Freshness at base and after: population 73 → 74, fresh 71 both, score floor 9 both, `C1_R45_PASS=true` both.
All 11 round-51 no-harm lines `ok` at both revs; the only differing line is `r45-freshness population=74 … ok`.
C1 side-effect: `status_conflicts` 1 → 0, `total=11 → 10`; the rest of C1's total is the untested frontier table.
Census `validate --file` exits 0 before and after with identical warnings; none on S022.
Caveats: the green rests on the round-51 re-base (round 50's exact-population pin went RED on the same cell), the
population now holds one row with no ledger entry, and the freshness floor has four rows of headroom.
