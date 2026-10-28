# T54W1ExecNoHarm — no-harm suite at C0 (round 54, wave w1)

Seat item: run the round-54 no-harm suite at the content commit and report every monitor with
`ok`/`RED`, attributing each RED to the C1 miss or to a new harm.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Base (round-53 freeze): `d33053f7552db4bd290c99a36979760f544c41ad`
- C0 (round-54 content commit): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1ExecNoHarm` (removed on exit via `trap`; no
  files left in `/tmp`, nothing written outside this seat's `w1/` scope).

## 1. Command and exit code

```
export HYAKU_SCRATCH=/fast/scratch/hyaku/tameshi-r54/T54W1ExecNoHarm
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/no-harm.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e
EXIT=0
```

`HYAKU_SCRATCH` was redirected to this seat's tree so the suite's own scratch
(`$HYAKU_SCRATCH/tameshi-r54/no-harm`) could not collide with a sibling run.

## 2. All 14 NOHARM lines, verbatim stdout

```
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=6 credited=41 RED
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-134 139 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [M:tools/bash-witness-study.py M:tools/env-diff.py M:tools/evidence-disposition.py M:tools/pin-disposition.py M:tools/registry.json ] ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=568 rev=568 ok
NOHARM sources-not-shrunk base=136 rev=139 ok
```

Verbatim copy also stored at `T54W1ExecNoHarm-receipts/noharm-at-c0.out`.

## 3. Count and tally verification

| Check | Command | Output |
|---|---|---|
| lines emitted | `grep -c '^NOHARM' noharm.out` | `14` |
| monitors declared in script | `grep -c 'echo "NOHARM' .ufo/evidence/round-54/no-harm.sh` | `14` |
| `ok` lines | `grep -c ' ok$' noharm-at-c0.out` | `13` |
| `RED` lines | `grep -c ' RED$' noharm-at-c0.out` | `1` |
| stderr | `cat noharm.err` | empty |
| exit code | `echo $?` | `0` |

14 emitted = 14 declared; 13 `ok` + 1 `RED` = 14. **Count is 14, exit code 0.**

### Exit code is structurally uninformative (checked, not assumed)

`no-harm.sh` has exactly one `exit` statement, `cd "$LANE" || exit 2` (line 11). Every monitor ends
in `echo`, which returns 0, so the script exits 0 whenever the lane directory exists — a `RED` never
propagates. Proven by probe:

```
bash .ufo/evidence/round-54/no-harm.sh /nonexistent/lane 59c38109bf11...
no-harm.sh: line 11: cd: /nonexistent/lane: No such file or directory
MISSING_LANE_EXIT=2
```

So `EXIT=0` at C0 certifies only "the lane path exists", not "no harm". The verdict lives entirely
in the printed tokens (13 `ok`, 1 `RED`). This is a property of the harness, not a lane defect, and
is recorded as a caution for anyone grepping the exit code.

## 4. The one RED: `coldread-floor`

Observed: `score=6 credited=41`.

Threshold in the script (line 16): `int(s["score"])>=8 and int(s["credited"])>=64` — i.e. score ≥ 8
and 64/64 credited.

**Verdict: this is the C1 miss itself (coldread-floor at 41), not a new harm.**

Evidence chain, all opened:

1. **It was already RED at base, one monitor earlier.** Running the identical suite at
   `d33053f7552d` gives `NOHARM coldread-floor score=6 credited=57 RED`
   (`T54W1ExecNoHarm-receipts/noharm-at-base.out`). The floor target was missed before this round
   (57 < 64); C0 did not flip this monitor from `ok`.
2. **The independent C1 counter reports the same numbers at C0.**
   ```
   python3 .ufo/evidence/round-54/c1/measure.py --lane <lane> --rev 59c38109bf11 \
       --work <scratch>/w-c1b --explain
   EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=59c38109bf11 cand_credited=41 lost=23 RED
   EXPLAIN arm2-monitor exit=0 covered=41 score=6
   C1_R54: rev=59c38109bf11 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
   ```
   `score=6`/`credited=41` match the no-harm line exactly, and at base the same counter reads
   `cand_credited=57 lost=7` — matching `credited=57` from the base no-harm run. Two independent
   entry points agree.
3. **The arithmetic closes against the frozen claim.** `floor_credited=64`; the C0 lost set is
   `c1/lost-headings-at-c0.json`, `len == 23`; `64 − 23 = 41`. The base lost set
   `c1/lost-headings-at-base.json` has `len == 7`; `64 − 7 = 57`.
4. **The lost sets are nested, and only 16 are new drift.** `set(lost@base) ⊆ set(lost@c0) == True`;
   `len(c0 − base) == 16`, `len(c0 ∩ base) == 7`. So the 41 is exactly 64 minus (7 headings that
   were already uncredited at base + 16 headings this round's own edits drifted away). The drift is
   the round's own input edits, i.e. the C1 defect, not a second, independent failure. Sample of the
   16 newly-lost headings: `### The tick and the pin read`,
   `### Round-13 gate/probe registry`, `### Triggers T1–T3 and the re-pin rule`,
   `### Round-18 gate/probe registry — routed-defect closure`,
   `## Pin disposition and provenance correction — round 13`.

No monitor other than `coldread-floor` is RED, so `coldread-floor` is the only candidate, and it is
fully explained by the C1 drift.

## 5. New-harm sweep: 13/13 remaining monitors compared against base

Same suite run at base: `T54W1ExecNoHarm-receipts/noharm-at-base.out`. Field-by-field delta:

| Monitor | base | C0 | delta status |
|---|---|---|---|
| commandD | `recorded_cases=10 depth_score=10 ok` | identical | unchanged ok |
| coldread-floor | `score=6 credited=57 RED` | `score=6 credited=41 RED` | RED→RED, **the C1 miss** (§4) |
| r45-freshness | `population=74 fresh=71 score=9 ok` | identical | unchanged ok |
| r45-coverage | `rows=2 entries=2 C2_R45_PASS=true ok` | identical | unchanged ok |
| S160-count | `1 ok` | identical | unchanged ok |
| registry-rows-not-below-134 | `136 ok` | `139 ok` | grew by the 3 declared rows, still ok |
| r46-coverage | `rows=3 entries=3 C3_R46_PASS=true ok` | identical | unchanged ok |
| r47-coverage | `rows=3 entries=3 C3_R47_PASS=true ok` | identical | unchanged ok |
| tools-scope | `[] ok` | `[M:tools/bash-witness-study.py M:tools/env-diff.py M:tools/evidence-disposition.py M:tools/pin-disposition.py M:tools/registry.json ] ok` | exactly the 5 declared C0 tool edits, ok |
| r49-generator-capability | full PBT line | identical | unchanged ok |
| r50-shrinker-selftest | `cases=14 failed=0 ok` | identical | unchanged ok |
| r53-scratch-hygiene | `tmp_hits=0 ok` | identical | unchanged ok |
| ledger-not-shrunk | `base=568 rev=568 ok` | identical | unchanged ok |
| sources-not-shrunk | `base=136 rev=136 ok` | `base=136 rev=139 ok` | grew, ok |

**Result: 0 monitors flipped `ok`→`RED`. No new harm.** The only value changes at C0 are the C1
coldread deficit and the three declared additive changes (`registry-rows` 136→139, `sources-not-shrunk`
136→139, `tools-scope` empty→the 5 declared edits).

Boundary note (checked, not a failure): `r45-freshness fresh=71` sits exactly on its floor (`f>=71`),
identical at base and C0 — passing but with zero margin, so any single stale row turns it RED.

## 6. Corroborating operability facts observed while attributing

These were read at C0 to confirm nothing this round touched has silently emptied:

- `tools/registry.json` at C0: `rows_total=56`, `with_scratch_root=7`, and the seven are
  `repeat-control-selftest, bash-witness-selftest, pin-disposition-selftest,
  evidence-disposition-selftest, context-capture-selftest, registry-check-selftest, env-diff-selftest`
  — the C2 `scratch_root` cell claim holds (7/7).
- `corpus/SOURCES.md` at C0: 139 rows by the same regex the monitor uses;
  `S277`, `S278`, `S279` present (TMPDIR / CPython tempfile / tempfile docs).
- Census conformance: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  → `CENSUS_EXIT=0` with trailing `tameshi ok .../corpus/SOURCES.md`; 139 rows as expected.

## 7. Structural observations (reported, not fixed — seat is read-only on the lane)

1. `tools-scope` passes **vacuously** when the diff is empty: `for t in $T; do ... done` leaves `s=ok`
   when `$T` is blank, which is exactly the base case (`[] ok`). At C0 the list is non-empty, so the
   C0 `ok` is a real check of 5 entries; the base `ok` is not a check at all.
2. The `coldread-floor` monitor duplicates the C1 counter's arm1/arm2 measurement through a different
   script. They agree here (6/41), which is good, but a divergence would be invisible to the monitor
   because the suite never cross-checks the two.
3. The suite's exit status carries no verdict (§3) — in pointed contrast to the C1 counter, which does
   propagate failure: the same C0 measurement through `.ufo/evidence/round-54/c1/measure.py` exits
   `C1_EXIT=1`, while `no-harm.sh` exits 0 with a RED in its output.

## 8. Receipts

All under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ExecNoHarm-receipts/`:

| file | what it is |
|---|---|
| `noharm-at-c0.out` | verbatim stdout of the suite at C0 (14 lines, 1 RED) |
| `noharm-at-base.out` | verbatim stdout of the same suite at base (14 lines, 1 RED) |
| `c1-counter-at-c0.out` | C1 `measure.py --explain` output at C0 (arm1/arm2/last line) |

Raw run outputs kept in scratch during the run: `noharm.out`, `noharm.err` (empty),
`noharm-base.out` under `/fast/scratch/hyaku/tameshi-r54/T54W1ExecNoHarm/`.

## 9. Verdict

- 14/14 NOHARM lines present, 13 `ok`, 1 `RED`, exit 0 (exit verified structurally uninformative).
- Only RED is `coldread-floor score=6 credited=41`, and it **is** the C1 miss: floor 64, 23 lost =
  7 pre-existing + 16 drifted by this round's own edits, reaching 41 — the same number the C1 counter
  reports at C0 (`credited=41 lost=23`).
- **No new harm** introduced by C0 in any other monitor; all 13 others are `ok` and match base except
  the three declared additive changes.

## 10. Environment / tooling

- No tool installed or upgraded: the run needed only `python3` and `git`, both already present.
  No `pacman` transaction was attempted (host-wide pause respected).
- No mutating git command was run anywhere; no clone was needed for this item (the suite reads
  objects from the lane with `git show`/`git diff` only).
