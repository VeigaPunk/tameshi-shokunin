# T54W2Scribe01 — round-54 report draft: Work performed (final) and Landed changes

Seat `T54W2Scribe01` · role scribe · axis **calibration** · item: *"Draft the report's **Work performed** and **Landed changes** sections from the contract, the freeze, the base/controls receipts, C0, C1 and the wave-1/2 seat dirs."*
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only for this seat) · scratch `$HYAKU_SCRATCH/tameshi-r54/T54W2Scribe01` · written 2026-10-28T15:08Z.

**Revision pins.** base `d33053f7552db4bd290c99a36979760f544c41ad`; freeze `441c26bec5e4c1cc31bc2a840f311cb8d1965259`; C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`; C1 `99c3bc88d704566197783f66b211ee0a830e0330` (C1's parent is C0: `git rev-list --parents -n1 99c3bc8` → `99c3bc88… 59c38109…`). HEAD moved three times during this seat (`097985c` → `8da3539` → `4e2de73`, amendment 3 → `fe70474`, amendment 4, the write-time HEAD); the states named below are those four. The counter-status line was measured at `4e2de73`; the freeze gate was re-run at `fe70474` (`FREEZE_INTEGRITY: OK files=10 amendments=4`). Instrument bytes executed for the status line: `.ufo/evidence/round-54/c1/measure.py` sha256 `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812` (frozen at `4e2de73`), sha identical before and after the run.

**Live-tree note.** The lane changed while this seat read it: HEAD advanced from `097985c` to `8da3539` to `4e2de73` (amendment 3) to `fe70474` (amendment 4); at `2026-10-28T15:06:33Z` the working tree additionally carried an uncommitted binder edit (`M .ufo/evidence/round-54/integrate/binder.py`, worktree sha256 `f9f4217d842e2ae67d2a9c1bfba1bccf8e01bad919e39db16408f7ea03db11b1`), a new `?? .ufo/evidence/round-54/integrate/resolutions.json`, and a re-key directory being written (`?? .ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/` with `traces/section-01..03.json` at that instant while `ledger.json` still held 568 entries with 0 re-key-bound). Every statement below is pinned to the revision or timestamp it names; the bind counts are a moving target and the report must quote `refresh-receipts.json` once it exists.

**Status is not a verdict.** The frozen C1 counter prints `C1_R54_PASS=false total=4` at C1 (`99c3bc88d704`) and at `4e2de73`: `credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41`. At the time of that measurement no re-key directory existed (`ls -d .ufo/evidence/round-21/coldread/rekey-r54-*` → none), no reader report is committed (`git ls-tree -r --name-only HEAD .ufo/waves/round-54/w1` and `…/w2` → 0 entries each), `control/controls-b.stdout` and `.ufo/evidence/round-54/after/` do not exist, and the deciding run has not been invoked. Everything below is therefore *work performed*, never a claim outcome; the only C1/C2 PASS/FAIL lines this round may print are the deciding run's own.

---

## Work performed

### W0 — Instruments frozen before any seat ran (`441c26b`, 2026-10-28T11:19:07-0300)

- Eight files, `+790/-0` (`git show --numstat --format='' 441c26b`): `.ufo/evidence/round-54/contract.json` (47), `c1/measure.py` (255), `c1/lost-headings-at-base.json` (9), `c2/measure.py` (191), `control/controls.sh` (171), `deciding-run.sh` (58), `freeze.json` (13), `no-harm.sh` (46).
- `.ufo/evidence/round-54/contract.json`: `"frozen_paths"` 11 entries, `"no_harm_monitors"` 14, `"deciding_invocations"` 1, `"lowest_axis"` `"calibration (8; the round-53 closure rejected-honest-stop on it)"`. C1 carries five counter arms (precheck / monitor / rekey / readers / stable) and controls `CTL_0, CTL_FAB, CTL_LOGINPUT, CTL_POS`; C2 carries five arms (unusable / empty / usable / docs / note) and controls `CTL_0, CTL_EXIT0, CTL_POS`.
- `freeze.json` at the freeze commit lists **7** hashed files and `"amendments": []` (`git show 441c26b:.ufo/evidence/round-54/freeze.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['files']), len(d['amendments']))"` → `7 0`). At `4e2de73` it lists **10** hashed files and 3 amendments; at the write-time HEAD `fe70474`, 10 files and 4 amendments. The gate re-derives both: `FREEZE_INTEGRITY: OK files=10 amendments=3` at `4e2de73` and `… amendments=4` at `fe70474` (the `deciding-run.sh` gate block run read-only).
- `no-harm.sh` declares 14 monitors (`grep -o 'NOHARM [a-z0-9-]*' .ufo/evidence/round-54/no-harm.sh | sort -u | wc -l` → `14`): `commandD`, `coldread-floor`, `r45-freshness`, `r45-coverage`, `S160-count`, `registry-rows-not-below-134`, `r46-coverage`, `r47-coverage`, `tools-scope`, `r49-generator-capability`, `r50-shrinker-selftest`, `r53-scratch-hygiene`, `ledger-not-shrunk`, `sources-not-shrunk`.
- `deciding-run.sh` gates, in order: freeze-digest integrity (refuses `exit 3`, nothing run); `outdir` exists; `HEAD == REV`; all four control receipts present at `REV` and each in a commit that descends from `FREEZE`; no `$OUT/{c1,c2}.start` (a second invocation is refused); clean tree witness before; counters, no-harm and precheck run from `git show REV:…` bytes, never the working tree; `FROZEN_UNCHANGED`; 14 `NOHARM … ok`; precheck; census; both counters; clean tree witness after.

### W1 — Base receipts at `d33053f7`

- C1 before: `C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false` (`.ufo/evidence/round-54/before/c1.stdout`).
- C2 before: `C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false` (`.ufo/evidence/round-54/before/c2.stdout`). The contract's C2 `before` text quotes the same `total=13`.
- Phase-A controls: `CTL CTL_0_c1 … total=4 C1_R54_PASS=false`, `CTL CTL_0_c2 … total=13 C2_R54_PASS=false`, `CTL CTL_R53 … rev=88afa9415454 credited=58 lost=6 …`, `CTL CTL_FAB … credited=58 lost=6 …`, `CTL CTL_LOGINPUT … credited=57 lost=7 …`, then `CONTROLS_A: 5/5 as pre-registered` with exit `0` (`.ufo/evidence/round-54/control/controls-a.stdout`, `controls-a.exit`).
- Round-53 negative control kept as a receipt: `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout` ends `C1_R53: rev=88afa9415454 credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false`, with 37 `PROBLEM` lines (the dead pathspec arm QUALITY 105 is written against).

### W2 — Content commit C0 (`59c3810`, 11:23:06-0300)

Twelve files, `+2866/-11` (`git show --numstat --format='' 59c3810`): `SKILL.md` 8/0; `corpus/SOURCES.md` 5/0; `corpus/knowledge/scratch-root-contract.md` 60/0; `corpus/lessons/round-54.md` 94/0; `tools/bash-witness-study.py` 10/2; `tools/env-diff.py` 12/3; `tools/evidence-disposition.py` 12/3; `tools/pin-disposition.py` 12/3; `tools/registry.json` 7/0; and the three mined snapshots `.ufo/evidence/round-54/assimilation/S277-posix-env.html` (872), `S278-tempfile.py` (952), `S279-tempfile-docs.html` (822).

- `SKILL.md` adds one bullet under `## Standing rules` (`git diff 441c26b 59c3810 -- SKILL.md`): `+- **The scratch root has three arms.** A tool that allocates scratch through`, through `… never a traceback, never exit 1 (corpus/knowledge/scratch-root-contract.md; the`.
- The four tools gain the declared class and the exit-2 mapping; at C1 the class name occurs `env-diff` 4×, `bash-witness-study` 3×, `evidence-disposition` 3×, `pin-disposition` 3× (`git show 99c3bc8:tools/<tool>.py | grep -c ScratchRootUnusable`). `env-diff`'s added catch, quoted from `git diff 59c3810 99c3bc8 -- tools/env-diff.py`:
  ```
  +    except ScratchRootUnusable as exc:
  +        print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
  +        return 2
  ```
- `tools/registry.json` gains exactly seven `scratch_root` cells (`git show 99c3bc8:tools/registry.json | grep -c '"scratch_root"'` → `7`), one per selftest row; the cell text is one line, quoted from `git diff 441c26b 59c3810 -- tools/registry.json`: `"TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)"`.
- `corpus/SOURCES.md` gains S277–S279 and keeps 139 rows at C1 (`git show 99c3bc8:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'` → `139`); S277 begins ``| S277 | POSIX.1-2024, Base Definitions §8.1 Environment Variables (TMPDIR) — https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html |``.
- `corpus/lessons/round-54.md` `## Gate` names S277–S279 with URLs and `opened 2026-10-28 by L1 TameshiR54a2` (`git show 99c3bc8:corpus/lessons/round-54.md | sed -n '11,17p'`).
- The re-read set is recorded, not inferred: `.ufo/evidence/round-54/c1/lost-headings-at-c0.json` holds 23 headings (`len(...)` → `23`), the frozen seven plus 16 headings C0's own edits moved.

### W3 — Wave 1: 76 seats reading C0

- `.ufo/waves/round-54/w1-registry.json`: `"seats": 76`, `"attack_seats": 21`, role mix scribe 27 / executor 13 / scout 4 / connector 2 / mutation-tester 12 / critic 4 / reviewer 5 / sentinel 4 / revenger 3 / simplifier 2.
- Reader outputs as of `2026-10-28T15:01:13Z`: 23 `*Read*.json` (each `cand = 59c38109bf11…`), 27 JSONs total, 76 MDs, 54 `*-receipts/` directories (`ls` counts under `.ufo/waves/round-54/w1/`). The 23 reader JSONs carry **28** findings, all distinct as `(heading, quote)` pairs, spread over 15 headings; 8 readers returned an empty list (command in §Commands, `C4`).
- Three attack receipts became the round's two disclosed instrument amendments, both landed before any control score or deciding invocation:
  - amendment 1 (C1 arm 3 basename→directory match): `.ufo/waves/round-54/w1/T54W1ExecDryBinder.md` (the binder dry run) — `freeze.json` amendment 1, commit `7883e0e`.
  - amendment 2 (`strace -f` rc measured the tracer): `.ufo/waves/round-54/w1/T54W1ExecExitClass.md` F2 — `$ python3 .ufo/evidence/round-54/c2/measure.py … --rev 59c38109bf11 …` → `C2_R54: … usable_ok=6 tmp_mkdirs=0 … total=1 C2_R54_PASS=false` — corroborated by `.ufo/waves/round-54/w1/T54W1ExecEmptyStrace.md`:
    ```
    **No, for all seven, in the declaring environment (`/tmp` usable).**
    ```
    landed in `19c7558`.
- The commit message of C1 counts **26** adjudicated findings; the wave context states **25** genuine. The raw count above is 28 distinct entries. This draft does not reconcile the three numbers — the adjudication record owns that — but the report must not quote a count without one of these sources.

### W4 — Fix pass C1 (`99c3bc8`, 11:38:37-0300)

Six files, `+82/-32` (`git show --numstat --format='' 99c3bc8`): `SKILL.md` 30/30 (18 hunks), `corpus/QUALITY.md` 10/0, `corpus/SOURCES.md` 1/1, `corpus/knowledge/change-aware-resweep-cadence.md` 1/1, `corpus/lessons/round-54.md` 37/0, `tools/env-diff.py` 3/0.

- `SKILL.md`: the three-arm bullet is re-cut so the measurement's scope is stated and the `C**`-class placeholder is gone. The C0 and C1 forms, quoted from `git diff 59c3810 99c3bc8 -- SKILL.md`:
  ```
  -  (`TMPDIR=""`) → unset, because the resolver skips an empty candidate
  +  (`TMPDIR=""`) → unset (the resolver skips an empty candidate, S278:163-165; the
  ```
  and the added scope sentence, quoted from the same diff:
  ```
  +  1. Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter);
  ```
- `tools/env-diff.py` gains the `ScratchRootUnusable` catch above (the env-diff run-path class: the class was declared but a non-selftest path fell through to `ENVDIFF_SETUP` with exit 2 and no naming line).
- `corpus/QUALITY.md` appends criterion 105: *"A counter arm that reads a directory, a revision or a manifest is proven by a positive control in which that arm must fire"*; its falsifier cites the round-53 `rekeyed=0/30` receipt and the round-54 positive control (line 1590 at HEAD reads, in part: "the round-54 counter's arm prints `rekeyed=7/7` on its positive control … both are committed.").
- `corpus/lessons/round-54.md` appends the R53.1–R53.9 disposition block, including R53.8 (the S275 quote "was located this round on physical page 3"; the `p. 4` cells in `corpus/SOURCES.md` and `corpus/knowledge/change-aware-resweep-cadence.md` now read `p. 3 (physical)`) — the one-line SOURCES and cadence edits above.
- Counter state at C1, instrument `63f5f881…` (the then-current bytes, before amendments 2/3): `C1_R54: rev=99c3bc88d704 c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false`, `EXPLAIN arm3-rekey dirs=[] c0=None`, `EXPLAIN arm4-readers 0/7`. The fix pass repairs bytes; it does not (and cannot) create credit — credit needs the re-key entries.

### W5 — Post-C1 instrument and record commits

| commit | time (-0300) | files | effect |
|---|---|---|---|
| `7883e0e` | 11:44:51 | 3, `+31/-8` | amendment 1: `c1/measure.py` re-key directory discovered from each traced path's directory component; `contract.json`, `freeze.json` updated |
| `3146479` | 11:45:34 | 2, `+66/-0` | round record: `LOG.md` +20, `SCORECARD.md` +46 (round-54 block, standings, both claim rows, planned round 55) |
| `19c7558` | 11:51:50 | 21, `+3666/-17` | re-freeze (amendment 2), base receipts, phase-A control receipts, section manifest, binder, `reader-section.py`, both wave specs, both dispatches, wave registries and `.ready` markers |
| `097985c` | 11:52:14 | 2, `+3/-2` | freeze-digest gate resolves the three inherited counter bodies by repo path; manifest re-hashed |
| `8da3539` | 11:56:38 | 3, `+11/-5` | wave-1 correction pass: QUALITY 105 falsifier de-inverted and receipt names fixed; note records the `context-capture` vocabulary residue; lesson falsifier de-inverted |
| `4e2de73` | 12:00:39 | 3, `+16/-7` | amendment 3: C1 arm 4 scans both `w1/` and `w2/` (`WAVE_DIRS`); manifest re-hashed, integrity OK |
| `fe70474` | after 12:00 | 3, `+12/-4` | amendment 4: C2 `/tmp` census regex accepts plain `mkdir(` as well as `mkdirat(` (the frozen suffix made the arm unable to fire); `contract.json`, `freeze.json` re-hashed |

Counts are `git show --numstat --format='' <commit>` sums. Amendment texts are in `.ufo/evidence/round-54/freeze.json` (`files` 10, `amendments` 4 at `fe70474`) and mirrored in `contract.json`.

### W6 — Wave 2: 47 seats reading C1

- `.ufo/waves/round-54/w2-registry.json`: `"seats": 47`, `"attack_seats": 12`, role mix scribe 25 / reviewer 6 / critic 4 / sentinel 4 / mutation-tester 2 / executor 4 / scout 2. `c1` is pinned to `99c3bc88d704566197783f66b211ee0a830e0330`.
- The 23 `T54W2Read*` items name exactly the 23 headings of `lost-headings-at-c0.json`, in order (`python3` extraction over `spec-w2.json`; set equality checked). Two sampled deliverables were verified against the instrument: `w2/T54W2Read11.json` pins `section_sha256` `3a78cbfc…` and `w2/T54W2Read20.json` pins `309f8328…`; `reader-section.py … 99c3bc88… "<heading>"` returns the same two shas (`start=1504 end=1523` and `start=1872 end=1880`).
- Wave-2 outputs as of `2026-10-28T15:01:13Z`: 21 JSONs, 32 MDs, 16 `*-receipts/` directories under `.ufo/waves/round-54/w2/`.
- The L1's adjudication of wave-2 findings is in progress in the worktree: `.ufo/evidence/round-54/integrate/resolutions.json` (untracked at `15:05:38Z`) lists 9 headings / 22 findings as `minor-gap` routed to round 55, and `binder.py` is edited (uncommitted) to bind a report with up to that many findings as `verdict = 'gap-minor'` with `minor_gaps` counted. The frozen credit algorithm admits that verdict (see F10).
- `.ufo/waves/round-54/reader-section.py` is the shared sectioning instrument: it prints `{"heading": …, "cand": …, "start": …, "end": …, "section_sha256": …}` from the frozen round-18 `sectionize` at the named revision.

### W7 — Census and integrity checks run this seat

- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → last line `tameshi\tok\t…/tameshi-shokunin/corpus/SOURCES.md`, exit `0`, with W01/W04 notes on pre-existing duplicate URLs; 139 S-rows at HEAD.
- Freeze integrity (the `deciding-run.sh` gate logic, run read-only): at `4e2de73` → `FREEZE_INTEGRITY: OK files=10 amendments=3`; at `fe70474` → `FREEZE_INTEGRITY: OK files=10 amendments=4`.
- Counter at `4e2de73`, instrument sha `d7749f84…` unchanged before/after:
  ```
  EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=4e2de731b52d cand_credited=41 lost=23 RED
  EXPLAIN arm2-monitor exit=0 covered=41 score=6
  EXPLAIN arm3-rekey dirs=[] c0=None
  EXPLAIN arm4-readers 0/7
  C1_R54: rev=4e2de731b52d c0=none credited=41 lost=23 rekeyed=0/7 readers=0/7 monitor=6/41 unstable=0 total=4 C1_R54_PASS=false
  ```

---

## Landed changes

Everything below is committed at the named revision. The working tree at `2026-10-28T15:05:38Z` also carries the live integration edits (`git status --porcelain`): `?? .ufo/waves/round-54/w1-run.out`, `?? .ufo/waves/round-54/w1/`, `?? .ufo/waves/round-54/w2-run.out`, `?? .ufo/waves/round-54/w2.ready.dispatched`, `?? .ufo/waves/round-54/w2/`, `M .ufo/evidence/round-54/integrate/binder.py`, `?? .ufo/evidence/round-54/integrate/resolutions.json`.

### Claim instruments — `441c26b` (+790)

| path | lines | what landed |
|---|---|---|
| `.ufo/evidence/round-54/contract.json` | 47 | two claims with before/target/counter/kill-rule/controls/cannot-see, 11 frozen paths, 14 no-harm monitors, one deciding invocation |
| `.ufo/evidence/round-54/c1/measure.py` | 255 | five arms: frozen precheck (floor `ef19d8e1e7ba`, requires `cand_credited=64 lost=0 ok`), unchanged round-21 monitor (`covered == 64 and score == 8`), re-key (`rekey-r54-<12hex>` resolved, entries `read_rev == c0`, round-18 credit algorithm), readers (`cand == c0` and section sha at REV), stable (no `LOG.md`/`SCORECARD.md` input) |
| `.ufo/evidence/round-54/c1/lost-headings-at-base.json` | 9 | the frozen seven base-lost headings |
| `.ufo/evidence/round-54/c2/measure.py` | 191 | five arms: unusable (exit 2 + naming line + no traceback), empty (`TMPDIR=""` → exit 0), usable (exit 0, zero mkdir under `/tmp`), docs (seven `scratch_root` cells), note (S-row mined + lesson Gate with URL and 2026-10-28) |
| `.ufo/evidence/round-54/control/controls.sh` | 171 | phase A: CTL_0 (both counters false), CTL_R53, CTL_FAB (valid trace, no reader → false), CTL_LOGINPUT (`LOG.md` pinned then changed → false); phase B: CTL_POS (both true), CTL_EXIT0 (class printed, rc 0 → false) |
| `.ufo/evidence/round-54/deciding-run.sh` | 58 | the gate chain listed in W0 |
| `.ufo/evidence/round-54/freeze.json` | 13 | 7 sha256 entries, `amendments: []` |
| `.ufo/evidence/round-54/no-harm.sh` | 46 | 14 monitors, twelve carried from round 53 and two new (`ledger-not-shrunk`, `sources-not-shrunk`) |

### C0 — one scratch-root exit class and its documentation — `59c3810` (+2866/-11)

| path | +/− | what landed |
|---|---|---|
| `SKILL.md` | 8/0 | `## Standing rules` gains "**The scratch root has three arms.**" (unset → platform default; `TMPDIR=""` → unset; set-but-unusable → exit 2, could-not-evaluate, naming the value) |
| `tools/env-diff.py` | 12/3 | `ScratchRootUnusable` class + raise + `ENVDIFF_SETUP: could-not-evaluate:` mapping |
| `tools/bash-witness-study.py` | 10/2 | same class; `WITNESS_STUDY: could-not-evaluate:` |
| `tools/evidence-disposition.py` | 12/3 | same class; `evidence-disposition.py: could-not-evaluate:` |
| `tools/pin-disposition.py` | 12/3 | same class; `pin-disposition.py: could-not-evaluate:` |
| `tools/registry.json` | 7/0 | `scratch_root` cell on the seven selftest rows (TMPDIR, empty arm, exit class) |
| `corpus/SOURCES.md` | 5/0 | S277 (POSIX TMPDIR), S278 (CPython `tempfile._candidate_tempdir_list`), S279 (tempfile docs), footer `Next unused id: S280` |
| `corpus/knowledge/scratch-root-contract.md` | 60/0 | three-arm table, "why the class is uniform", "what measures it", "## Falsifier" |
| `corpus/lessons/round-54.md` | 94/0 | `## Gate` (S277–S279, URLs, 2026-10-28), `## Mistakes`, QUALITY criterion 105, method note |
| `.ufo/evidence/round-54/assimilation/S27{7,8,9}*` | 872/952/822 | the mined source snapshots |

### C1 — wave-1 findings adjudicated and fixed — `99c3bc8` (+82/-32)

| path | +/− | what landed |
|---|---|---|
| `SKILL.md` | 30/30, 18 hunks | stale line anchors re-resolved, the `C**` placeholder replaced, the exit-arm cell re-scoped to the measured `--selftest`/`selftest` path, the runbook pin corrected, the S275 page locator corrected |
| `corpus/QUALITY.md` | 10/0 | criterion 105 (positive control for a counter arm); falsifier names the `rekeyed=0/30` receipt |
| `corpus/SOURCES.md` | 1/1 | S275 locator `p. 4` → `p. 3 (physical)` |
| `corpus/knowledge/change-aware-resweep-cadence.md` | 1/1 | same locator |
| `corpus/lessons/round-54.md` | 37/0 | R53.1–R53.9 dispositions |
| `tools/env-diff.py` | 3/0 | `ScratchRootUnusable` catch on the non-selftest path (the env-diff run-path class) |

### Records and instruments after C1

| commit | files | what landed |
|---|---|---|
| `7883e0e` | 3 | amendment 1 in `c1/measure.py` (directory-component discovery), `contract.json`, `freeze.json` |
| `3146479` | 2 | `LOG.md` round-54 entry (+20); `SCORECARD.md` round-54 block (+46: standings, both claim rows with before/target/counter/controls, planned round 55) |
| `19c7558` | 21 | amendment 2 in `c2/measure.py` (plain-run rc; traced run only for the mkdir census); `before/c1.stdout`, `before/c2.stdout`, `control/controls-a.{stdout,exit}`, `control/r53-counter-at-88afa941.stdout`, `c1/lost-headings-at-c0.json`, `integrate/binder.py`, `.ufo/waves/round-54/reader-section.py`, `spec-w1.json`, `spec-w2.json`, `w1-dispatch.json`, `w1-registry.json`, `w1.ready`, `w2-dispatch.json`, `w2-registry.json`, `w2.ready`; `deciding-run.sh` +26 (freeze-digest gate), `freeze.json` re-cut (10 files, amendments 1–2) |
| `097985c` | 2 | `deciding-run.sh`: the three inherited counter bodies resolve by repo path before hashing; `freeze.json` re-hashed |
| `8da3539` | 3 | `corpus/QUALITY.md` falsifier de-inverted + receipts named (line 1590); `corpus/lessons/round-54.md` falsifier de-inverted (reads zero); `corpus/knowledge/scratch-root-contract.md` +6 (disclosed `context-capture` `SELFTEST: FAIL` vocabulary residue → round 55) |
| `4e2de73` | 3 | amendment 3: `c1/measure.py` `WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')`; `contract.json` +4 (amendment 3); `freeze.json` re-hashed (10 files, 3 amendments) |
| `fe70474` | 3 | amendment 4: `c2/measure.py` `/tmp` census regex accepts `mkdir(` and `mkdirat(`; `contract.json` +4; `freeze.json` re-hashed (`FREEZE_INTEGRITY: OK files=10 amendments=4`) |

### Not landed (as of the status run, `4e2de73` / 15:02Z)

- `.ufo/evidence/round-21/coldread/rekey-r54-<c0>/`: **absent at 15:02Z** (0 directories). At `15:06:33Z` the bind has begun in the working tree: `?? .ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/` holds `traces/section-01..03.json`, and `ledger.json` is unchanged at 568 entries with 0 re-key-bound — so no entry credits yet, and the counts are a moving target.
- Committed reader reports: **absent** (`git ls-tree -r --name-only HEAD .ufo/waves/round-54/w1` → 0; `…/w2` → 0). The seat deliverables exist only as untracked files.
- `control/controls-b.stdout` / `controls-b.exit`: **absent** (`git cat-file -e HEAD:.ufo/evidence/round-54/control/controls-b.stdout` fails; not in the worktree either).
- `.ufo/evidence/round-54/after/` (deciding receipts): **absent**; no `c1.start`/`c2.start`.
- `LOG.md`/`SCORECARD.md` text for amendments 2, 3 and 4: **absent** — the round-54 SCORECARD block names only amendment 1 (see F3/F5).

---

## Scriber's notes — limits the final report must carry

Each item below is a byte-exact observation with a command; none is a verdict on a claim.

**F1 — the binder still reads only `w1/`, while the round's reader work lands in `w2/`.**
`binder.py:48` `WAVE = '.ufo/waves/round-54/w1'`; `c1/measure.py:54` `WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')  # amendment 3: both waves' reader reports`. Amendment 3 fixed the counter, not the binder (the binder is not in `contract.frozen_paths`). Consequence for the bind step: wave-2 reports must be made visible to `binder.py`'s glob (copy into `w1/`, or amend the binder before the bind), or every heading returns `SKIP … no-clean-reader` and the ledger gains no re-key entry. At `2026-10-28T15:05:38Z` the binder is being edited live (`M …/integrate/binder.py`): the worktree adds a `resolutions.json`-driven allowance so a report with up to `n` adjudicated findings is bound with `verdict = 'gap-minor'` and `minor_gaps = len(findings)` — but `WAVE` is still `.ufo/waves/round-54/w1` at line 48. Receipt: `grep -n "^WAVE\|Read.*json\|d.get('cand')" .ufo/evidence/round-54/c1/measure.py .ufo/evidence/round-54/integrate/binder.py`.

**F2 — 13 of 23 sections changed between C0 and C1 (5 of the frozen seven), so wave-1 reports cannot satisfy C1 arm 4 at REV ≥ C1.**
Arm 4 (`.ufo/evidence/round-54/c1/measure.py:241`) requires `d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']`, where `sec` is the section at `REV`. Measured with the frozen round-18 `sectionize` at both revisions: 13 sections differ, including `## Standing rules`, `## Mutation-sweep recipe …`, `### The boundaries …`, `### Using the ledger`, `### The operator's runbook — …`. A wave-1 report pins `cand = C0` and the C0 sha, so it fails either the `cand` or the sha test once the bind is at C1. The bind therefore has to be `rekey-r54-99c3bc88d704` (C1) with the wave-2 reports (`cand = C1`, C1 sha); that is what the wave-2 deliverables pin.

**F3 — the round record's freeze pointer is stale by two amendments.**
`SCORECARD.md:2564-2567` (HEAD):
```
frozen at `441c26be` before any seat ran; **amendment 1** (`7883e0e5`) fixes
one mechanical discovery bug in the C1 counter's re-key arm, found by the binder
dry run before any control was scored and before any deciding invocation —
predicate, target and arms unchanged, and `7883e0e5` is the freeze pointer the
deciding run uses.
```
At the write-time HEAD (`fe70474`) `freeze.json` has 10 files and 4 amendments, and `git diff --quiet 7883e0e HEAD -- .ufo/evidence/round-54/c1/measure.py; echo $?` → `1` (also `1` for `441c26b`). Since `deciding-run.sh` sets `rc=1` when `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` fails, the deciding run's `FREEZE` argument must be the commit that carries the current manifest (`4e2de73` or later), not the one the SCORECARD names. The report must state the pointer it actually used.

**F4 — the SCORECARD's C2 "before" cell is stale against the receipt it cites.**
`SCORECARD.md:2584`: `` `unusable_exit2=3 docs=0 note=0 sources=0 total=14` false (`.ufo/evidence/round-54/before/c2.stdout`; the contract's before text quotes the pre-freeze smoke run `total=13`, the recorded receipt is quoted here and the delta disclosed) ``. The receipt and the contract both say 13: `tail -1 .ufo/evidence/round-54/before/c2.stdout` → `… total=13 C2_R54_PASS=false`; `contract.json` C2 `before` → `… total=13 C2_R54_PASS=false`. The parenthetical inverts which artifact says 13.

**F5 — the lesson's R53.5 disposition is true at C1 and false at HEAD.**
`corpus/lessons/round-54.md:114-116` (HEAD): `` - **R53.5** (stale freeze receipts) — FIXED: `freeze.json` is regenerated at freeze time and the deciding run prints `FROZEN_UNCHANGED=1` against it; no amendment is recorded. `` At C1 this held (`git show 99c3bc8:.ufo/evidence/round-54/freeze.json` → 7 files, 0 amendments). At the write-time HEAD the same file records 4 amendments and 10 files. The report must not quote the sentence as current; it must disclose amendments 2, 3 and 4 itself, because the round-54 SCORECARD block names only amendment 1 and the lesson has no other mention of "amendment" (`grep -c amendment corpus/lessons/round-54.md` → `1`).

**F6 — a falsifier names a receipt that does not exist.**
`corpus/QUALITY.md:1590` (HEAD):
```
… the round-54 counter's arm prints `rekeyed=7/7` on its positive control; the two receipts are
`.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout` (the round-53 counter's bytes run at
`88afa941`) and `.ufo/evidence/round-54/control/controls-b.stdout` (the round-54 positive control);
both are committed.
```
`git cat-file -e HEAD:.ufo/evidence/round-54/control/controls-b.stdout` fails and the worktree has no such file (`ls .ufo/evidence/round-54/control/` → `controls-a.exit controls-a.stdout controls.sh r53-counter-at-88afa941.stdout`). The claim is true only after phase-B controls are committed; the report must not print `FROZEN_UNCHANGED=1` or `rekeyed=7/7` before then.

**F7 — three different counts for wave-1 findings are on record.**
23 reader JSONs, 28 findings entries, 28 distinct `(heading, quote)` pairs, 15 headings, 8 empty lists (command `C4`). The wave context says 25 genuine; the C1 commit message says 26 adjudicated. The report must attribute whichever number it uses and must not present the raw 28 as "adjudicated".

**F8 — the credit arithmetic needs all 23 re-key entries; arm 3 checks only 7.**
Arm 1 at C1 reads `credited=41 lost=23`; the 23 lost headings are exactly `lost-headings-at-c0.json` (`len` → 23); arm 3 iterates only `lost-headings-at-base.json` (`len` → 7). 41 + 23 = 64, so a bind of the seven alone satisfies arm 3 and still fails arm 1. The report must state that the bind covers the 23-heading union (`binder.py` `HEADINGS = sorted(set(HEADINGS) | set(BASE7))`).

**F9 — the binder's input set is the historical union, which the wave-1 pre-bind map told the L1 not to use.**
`binder.py` builds `inputs` by unioning every prior entry's `inputs` for the heading (skipping `LOG.md`, `SCORECARD.md`, `SKILL.md`) and keeping paths that exist at PIN; measured at PIN `8da3539` every one of the 23 headings has at least one surviving input (minimum 3, maximum 7703 for `## Mutation-sweep recipe …`). `.ufo/waves/round-54/w1/T54W1ConnPreBind.md` rule 3 reads:
```
3. **Never fabricate an input** — admissible pins are only paths the C0 section body byte-cites (or that the bound cold-read actually opened for that heading). Do **not** union historical `.ufo/evidence/round-21/coldread/ledger.json` `inputs` for the same heading; those unions drag in C0 tools and LOG/SCORECARD the live section does not name.
```
Both positions are on record; the binder's own `refresh-receipts.json` will show which was applied, and the report must quote that receipt rather than either design note.

**F10 — the minor-gap path credits under the frozen algorithm; the in-progress adjudication covers 9 headings and 22 findings.**
`.ufo/evidence/round-18/measure.py:125-128` defines `FAIL_VERDICTS` (three) and puts `gap-minor` in `VALID_VERDICTS`, `EXEC_VERDICTS` and `REC_VERDICTS`; `entry_failure` (459-474) and `entry_credit_reason` (477-511) veto on `blocking_gaps` and `wrong_expectations` only — `minor_gaps` is never consulted. The live binder's `verdict = 'gap-minor'` with `minor_gaps = len(findings)` therefore credits. As of `2026-10-28T15:05:38Z`, `.ufo/evidence/round-54/integrate/resolutions.json` (untracked) adjudicates 9 headings / 22 findings as `minor-gap` routed to round 55, the largest being `### Round-21 gate/probe registry — finite environment differential` with 11. The report must state that such a credit carries named findings rather than a clean read, and must quote the final `refresh-receipts.json` for the headings actually bound.

**Not observed, therefore not asserted:** whether the deciding run has been invoked at any revision other than `4e2de73`; whether `controls-b` was run elsewhere; whether any wave-2 reader's judgment is fair. No tool was installed or upgraded for this seat (no `pacman`, no `uv`, no `npx`, no binary added).

---

## Commands run (all read-only against the lane; scratch only)

```
C1  cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
    git log --oneline -12
    git log -1 --format='%H %ci %s' 59c38109bf119d0e9d4f878644a82babc937bc1e   # C0
    git log -1 --format='%H %ci %s' 99c3bc88d704566197783f66b211ee0a830e0330   # C1
    git rev-list --parents -n1 99c3bc8                                          # C1 parent = C0

C2  for c in 441c26b 59c3810 99c3bc8 7883e0e 3146479 19c7558 097985c 8da3539 4e2de73; do
      git show --numstat --format='' $c | awk '{a+=$1;d+=$2;n++} END {printf "files=%d +%d -%d\n",n,a,d}'
    done
    # 441c26b files=8 +790 -0 / 59c3810 files=12 +2866 -11 / 99c3bc8 files=6 +82 -32
    # 7883e0e files=3 +31 -8 / 3146479 files=2 +66 -0 / 19c7558 files=21 +3666 -17
    # 097985c files=2 +3 -2 / 8da3539 files=3 +11 -5 / 4e2de73 files=3 +16 -7

C3  cat .ufo/evidence/round-54/before/c1.stdout .ufo/evidence/round-54/before/c2.stdout \
        .ufo/evidence/round-54/control/controls-a.stdout .ufo/evidence/round-54/control/controls-a.exit
    cat .ufo/evidence/round-54/contract.json .ufo/evidence/round-54/freeze.json

C4  python3 - <<'PY'
    import json,glob,collections
    rows=[]; readers=0; empty=0
    for f in sorted(glob.glob('.ufo/waves/round-54/w1/*Read*.json')):
        d=json.load(open(f)); readers+=1
        n=len(d.get('findings') or [])
        if n==0: empty+=1
        for x in d.get('findings') or []:
            rows.append((d['heading'], x['quote'], f))
    print('readers', readers, 'raw', len(rows),
          'unique (heading,quote)', len({(h,q) for h,q,_ in rows}),
          'headings with findings', len({h for h,_,_ in rows}), 'clean', empty)
    PY
    # readers 23 raw 28 unique (heading,quote) 28 headings with findings 15 clean 8

C5  python3 - <<'PY'    # section bytes at C0 vs C1, frozen round-18 sectionize
    # (r18 extracted with: git show 99c3bc8:.ufo/evidence/round-18/measure.py > $S/an/r18.py)
    # result: all sections 64 changed 13; base7 changed 5
    #   ## Standing rules / ## Mutation-sweep recipe … / ### The boundaries … /
    #   ### Using the ledger / ### The operator's runbook — `corpus/knowledge/operator-runbook.md`
    PY

C6  python3 .ufo/evidence/round-54/c1/measure.py --lane <lane> --rev 99c3bc88d704 --work $S/w1 --explain
    python3 .ufo/evidence/round-54/c1/measure.py --lane <lane> --rev 097985c --work $S/whead --explain
    python3 .ufo/evidence/round-54/c1/measure.py --lane <lane> --rev 8da3539 --work $S/whead2 --explain
    python3 .ufo/evidence/round-54/c1/measure.py --lane <lane> --rev 4e2de73 --work $S/wfinal --explain
    # every line: credited=41 lost=23 rekeyed=0/7 readers=0/7 total=4 C1_R54_PASS=false (exit 1)

C7  python3 .ufo/waves/round-54/reader-section.py <lane> 99c3bc88d704 "<heading>"
    # "## Repeated controls and gate registry — round 12" -> start 1504 end 1523 sha 3a78cbfc…
    # "### Round-17 gate/probe registry — re-pin and monitor" -> start 1872 end 1880 sha 309f8328…

C8  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
    # exit 0; last line: tameshi  ok  …/corpus/SOURCES.md

C9  python3 - <<'PY'    # freeze-digest gate block of deciding-run.sh, run read-only at 4e2de73
    # FREEZE_INTEGRITY: OK files=10 amendments=3
    PY

C10 git status --porcelain
C11 sed -n '1,220p' .ufo/evidence/round-54/integrate/binder.py   # read only; the binder was never executed
```

## Artifacts opened

`.ufo/evidence/round-54/{contract.json,freeze.json,deciding-run.sh,no-harm.sh}`; `.ufo/evidence/round-54/c1/{measure.py,lost-headings-at-base.json,lost-headings-at-c0.json}`; `.ufo/evidence/round-54/c2/measure.py`; `.ufo/evidence/round-54/integrate/binder.py`; `.ufo/evidence/round-54/before/{c1.stdout,c2.stdout}`; `.ufo/evidence/round-54/control/{controls.sh,controls-a.stdout,controls-a.exit,r53-counter-at-88afa941.stdout}`; `.ufo/evidence/round-54/assimilation/S277-posix-env.html` (name/size only); `.ufo/waves/round-54/{reader-section.py,spec-w1.json,spec-w2.json,w1-registry.json,w2-registry.json}`; `.ufo/waves/round-54/w1/{T54W1ScribeWork.md,T54W1ConnPreBind.md,T54W1ConnPreBind.json,T54W1ExecC1Counter.md,T54W1ExecDryBinder.md,T54W1ExecExitClass.md,T54W1ExecEmptyStrace.md,T54W1Read01.json,swarm-registry.json}` plus directory counts; `.ufo/waves/round-54/w2/{T54W2Read11.json,T54W2Read20.json}`; lane `SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-54.md`, `corpus/knowledge/scratch-root-contract.md`, `tools/registry.json`, `tools/env-diff.py`.

**Report path:** `.ufo/waves/round-54/w2/T54W2Scribe01.md` (this file). No file outside `.ufo/waves/round-54/w2/` was created or edited by this seat; the lane's uncommitted binder edit and `resolutions.json` are other seats' work, read but not touched.
