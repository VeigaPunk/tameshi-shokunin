# T53W2Read20 — wave-2 re-read of `### Using the ledger`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (git objects only; working tree never read as evidence)
- Candidate: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C**)
- Frozen split (round-18 `sectionize`, extracted from the same commit, `.ufo/evidence/round-18/measure.py`): heading found at line 938, `start=938 end=969`, bytes 2504
- `section_sha256 = 355743ed274b576d6119665499c8771044b53297308b19822ba73bf0ef9be1d1` (identical from `sectionize` and from an independent re-slice `lines[937:969]` with trailing blank lines stripped, section = heading line 938 through content line 967; 968-969 blank, next heading at 970 `### Reading a receipt — the discipline`)
- Section text held in scratch for byte comparison; every quote below occurs byte-exact exactly once in it (`body.count(quote) == 1`).

```
$ git -C LANE show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md > SKILL_C**.md   # 2189 lines
$ sha256sum SKILL_C**.md
4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d  SKILL_C**.md
sectionize -> {'start': 938, 'end': 969, 'heading': '### Using the ledger', 'sha256': '355743ed…be1d1'}
```

## 1. Verification of the named wave-1 fix (first)

Named fix: `:614-643` attribution corrected to `(round-26 tool :603-629)`.

Diff C* → C** for this section:

```
$ git diff a41195dfc13a73958e4c5228ec196b28d03ded03 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e -- SKILL.md
-  Current anchors (round 52 re-anchor; round 26 recorded :614-643): pins/revisions/tables `tools/mutate-and-run.sh:614-643`,
+  Current anchors (round 52 re-anchor to the ten-leg table; the round-26 tool recorded :603-629): pins/revisions/tables `tools/mutate-and-run.sh:614-643`,
```

The fix is present in the C** bytes, and both halves of it verify:

1. Round-52 re-anchor to the ten-leg table — the literal `614-643` first enters SKILL.md at the round-52 wave-2 fix-reads commit, i.e. it is a round-52 re-anchor, not a round-26 one:
   ```
   $ git log --reverse --oneline -S"614-643" -- SKILL.md
   7ff81a5 round-52: wave-2 fix-reads applied in-line (59), round21 row cell, shrink-case scope; QUALITY 103; S274; lesson; wave-2 evidence
   ```
2. `the round-26 tool recorded :603-629` — at the round-26 content commit `40a12bf`, `tools/mutate-and-run.sh` carries the nine-leg pins/revisions/tables block exactly at 603-629 (`PIN_JS` 603 … `TABLE_CITECHECK` 629; `PIN_DRIFTPINS`/`TABLE_DRIFTPINS` do not exist yet):
   ```
   $ git show 40a12bf:tools/mutate-and-run.sh | grep -n "^PIN_JS\|^TABLE_SOURCESCHECK\|^TABLE_CITECHECK\|^TABLE_DRIFTPINS"
   603:PIN_JS=83016d45…
   628:TABLE_SOURCESCHECK='K_KIND:KILLED,…
   629:TABLE_CITECHECK='K_UNRESOLVED_SEV:KILLED,…
   ```

## 2. Checks run on every other claim in the section

All tool anchors were read from `git show C**:tools/mutate-and-run.sh` (2159 lines); the tool is byte-identical between C* and C** (fix pass 2 touched only `SKILL.md` and the seven python tools).

| claim in section | check | result |
|---|---|---|
| `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` default scratch, allocated after prerequisite checks | `mutate.sh:1421-1437`; prerequisite `command -v` checks 1423-1427 precede `mktemp -d` 1432 | holds |
| removed on PASS unless `--keep`, retained on FAIL/SETUP, caller workdirs never removed | `1519-1529` (FAIL/SETUP print "kept", no `rm`), `1542-1547` (`rm -rf` only when `auto=1 && KEEP=0`) | holds |
| "Pre-allocation SETUP has no root to retain" | `die_setup` at 1423-1427 and 1432 runs before any root exists | holds |
| exits 0/1/2 = PASS/FAIL/SETUP (`:139-143,1519-1548`) | comment 139-143; `exit 1` 1523, `exit 2` 1529/1538, `exit 0` 1548 | holds |
| legs materialize from the object store, mode mirrored, SHA pinned (`:1275-1317`) | `git show` 1276, `ls-tree` mode 1285-1300, pin compare 1312-1317 | holds |
| `REGRESSION_PIN` names repo/rev/path/mode/sha256 (`:1302-1306`) | `1302-1303` git form, `1304-1306` file form | holds |
| missing repo/rev/blob or pin mismatch refuses before the suite | `1267-1274` (rev/path), `1313-1317` (pin mismatch), both `return 2` before the sweep at 1320 | holds |
| `REGRESSION: PASS (cases=N passed=N; …)` plus `REGRESSION_TOOL` sha and per-leg `REGRESSION_PIN` | `1540-1541` PASS line, `1442` `REGRESSION_TOOL: %s sha256=%s`, `1302` per-leg PIN | holds |
| `N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26, 10 since round 51` | `nlegs=` at 9f1d3c3 (4), 05a2247 (7), 58e5d53 (8), a08e85c/40a12bf (9), 6d8c11e (10); tool comment :83 `r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten` | holds |
| one-edit defects, unique `@old`, `@new != @old` | `395` duplicate `@old`, `401` duplicate `@new`, `410` empty, `412` `@new equals @old`, `432-434` `count==1` | holds |
| no leg records a skipped count; report prints defects/killed/survived/inconclusive (`:78-79`) | `78` `MUTATE: DONE|DEGRADED (target=… defects=… killed=… survived=… inconclusive=… kill-rate=…%)`; emitted at 581/585 | holds |
| pins/revisions/tables `:614-643`; first-four specs `:671-849`; inventory `:83-108`; ten dispatches `:1459-1508` | 614 `PIN_JS` … 643 `TABLE_DRIFTPINS`; 671 `regression_specs()` … 849 leg-4 `EOT`; 83-108 leg inventory + sources; 1459-1508 exactly ten `regression_case_git` dispatches | holds |
| ten pins are real and match their pinned blobs | sha256 of each `git show REV:PATH` equals `PIN_*` for all ten (`kimi-census`, `surface-census`, `tsukuroi-census`, `mado-verify`, `checklist-run`, `claims-check`, `round-gate`, `sources-check`, `cite-check`, `drift-pins`) | holds |
| "old tsukuroi/mado pins are historical" | tsukuroi live file sha `adb1b4ce…` ≠ pin `084951be…`; mado live `050efc72…` ≠ pin `d7edaab4…` | holds |
| `(U) … tameshi-carried; no fleet-contributed leg` | all ten specs are embedded in `regression_specs()` (673-1210); legs 8/9/10 specs come from tameshi's own `.ufo/evidence/round-18|26|51` | holds |
| `${TMPDIR:-/tmp}` against the standing scratch rule (`SKILL.md:28`, `$HYAKU_SCRATCH`) | the runner honours `TMPDIR` (`r51`), the same default is documented at `SKILL.md:1336` and in the runner registry row `SKILL.md:2167` ("auto mktemp under ${TMPDIR:-/tmp}"), and C2's frozen predicate targets only `dir="/tmp"` hardcodes in `registry-check.py`/`env-diff.py` | holds as documented behaviour (not filed) |

## 3. Finding

### F1 — false provenance: `(:1247-1317,1459-1517 since round 26)`

Quote (byte-exact, one occurrence in the C** section bytes):

```
(:1247-1317,1459-1517 since round 26)
```

The anchors themselves hold at C**: 1247-1317 is the repo-identity/rev/path/pin refusal and materialize block (`1247` open `if [[ -n "$repo" ]]`, `1302` `REGRESSION_PIN`, `1313-1317` pin mismatch), and 1459-1508 are the ten dispatches with the status aggregation at 1510-1517. The date does not hold. Those ranges became the anchors at the round-51 ten-leg re-anchor; at the round-26 content commit `40a12bf` the same content sits elsewhere:

```
$ git show 40a12bf:tools/mutate-and-run.sh | grep -n "^  regression_case_git\|^  st_"
1384:  regression_case_git js-kimi-census \
1428:  st_citecheck=$?
1430:  local nlegs=9 npass=0 nfail=0 nsetup=0 st
1431:  for st in "$st_js" "$st_kagi" … "$st_citecheck"; do

$ git show 40a12bf:tools/mutate-and-run.sh | awk 'NR>=1245 && NR<=1250 {print NR": "$0}'
1245:   local rc
1246:   bash "$SELF" --target "$target" --defects "$spec" --suite "$suite" \
1247:     --workdir "$cwd" --label "$name" --timeout "$TIMEOUT_S" --tail "$TAIL_N" \
1248:     >"$cwd/sweep.log" 2>&1
1249:   rc=$?
1250:   printf 'REGRESSION_SWEEP %s: %s\n' "$name" \

$ git show 40a12bf:tools/mutate-and-run.sh | awk 'NR>=1455 && NR<=1462 {print NR": "$0}'
1455:     rm -rf "$root"
1459:   exit 0
1460: }
1462: # ------------------------------------------------------------------ selftest
```

So at round 26, :1247 was the sweep sub-invocation and :1459 was run_regression's closing `exit 0`; not the refusal block and not the dispatch/aggregate block. Round 26's own SKILL.md recorded the sentence with the round-26 ranges:

```
$ git show 40a12bf:SKILL.md | sed -n '948p'
  later legs still run and their statuses aggregate (:1384-1450 since round 26).
```

The date marker therefore survived the later re-anchors as a stale attribution: the ranges were replaced, `since round 26` was not. Reading `since round 26` as dating the behaviour instead does not save it either — per-leg SETUP refusal and later-leg status aggregation already exist in the round-18 tool:

```
$ git show 58e5d53:tools/mutate-and-run.sh | awk 'NR>=112 && NR<=130 && (/pin mismatch/||/repo\/rev\/blob/) {print NR": "$0}'
114: # a missing repo/rev/blob or a pin mismatch is a SETUP refusal, never a pass.
128: # repo/rev/blob, pin mismatch, sweep setup refusal — with no FAIL. Lines:

$ git show 58e5d53:tools/mutate-and-run.sh | awk 'NR>=1355 && NR<=1357 {print NR": "$0}'
1355:   local nlegs=8 npass=0 nfail=0 nsetup=0 st
1356:   for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck"; do
1357:     case $st in
```

Class: false provenance (stale date marker on live anchors). Same species as the wave-1 finding on the adjacent bullet, which the fix pass repaired by naming the round (`the round-26 tool recorded :603-629`); this parenthetical needs the same treatment (name the round the ranges belong to — round 51 introduces the ten-leg table, round 52 re-anchors — or drop the date).

## 4. Out of scope / notes

- The preceding section (`## The leg ledger …`) is a different section and was not graded here.
- No mutation, no tool run: all evidence is `git show`/`awk` output over objects; sibling repos were read read-only to verify the ten pins.
- Scratch used: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read20/` (deleted before yield). No `pacman`, no installs, no git/jj mutation in the lane or anywhere else.
- Observation, not a finding and outside this seat's write scope: at the end of this seat's read the lane working tree carries two uncommitted modifications not made by this seat — `git status --porcelain -- SKILL.md tools/ .ufo/evidence/` → ` M SKILL.md`, ` M tools/registry-check.py` (`git diff --stat`: SKILL.md 4 ++--, tools/registry-check.py 6 +++++-; both mtime 2026-10-27_10:58:00). All my reads were `git show C**:…` over objects, so they do not affect this report; the frozen deciding run requires a clean tree, so the L1 should account for them.
