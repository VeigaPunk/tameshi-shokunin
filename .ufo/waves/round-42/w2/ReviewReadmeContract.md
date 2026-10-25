# ReviewReadmeContract — round 42 wave 2 (FALSIFY)

Attacked: (a) the `## Round 42` section of `corpus/README.md` at `a21845f523b75adbd3e3f7a62af91294db224ad9`
(README lines 526–539 at that rev); (b) contract `post_freeze_amendments` P1–P4 and byte-stability of
`claims.*` since freeze `322b5cd32b4319a05340d249ae752d12a9e6b19f`. Read-only on the lane; one scratch clone
`/tmp/tameshi-r42w2-ReviewReadmeContract-clone` (checked out at `a21845f`, deleted before return). No counter
was run in default mode; no counter was run at all.

## Findings

### F1 [MEDIUM — record accuracy] README:533–535 states that F1's report interop is not held, which the README's own Round 25/26 sections contradict

README at `a21845f`, lines 533–535:
"F1 stays partly held, because no ledger leg has been emitted as a schema report."

The same file at the same revision says otherwise:
- `corpus/README.md:385-391` (Round 25): "**F1 status correction** … Report interop is now held for the eight recorded ledger legs: each leg is emitted as a mutation-testing-elements report that the official 3.9.0 schema accepts". F1b (NoCoverage) stays open.
- `corpus/README.md:413` (Round 26): "F1 stays held and F1b open".
- `LOG.md:1660`: "F1 report interop moves to Core, F1b NoCoverage stays open."
- `corpus/knowledge/mte-report-interop.md:4`: "the report-interop half of F1 moves to Core (schema acceptance + official metrics scoring of emitted ledger-leg reports)".
- Committed emitted reports: `git ls-files | grep round-25/mte-reports` lists `.ufo/evidence/round-25/mte-reports/*.mte.json` (bash-checklist-run, bash-mado-verify, bash-surface-census, bash-tsukuroi-census, js-claims-check, …).
- No round after 26 changes F1 back: README:456, 464, 472, 485 each say "No frontier row changes status".

Round 42 restates round 1's reason (README:111-114, which Round 25 explicitly superseded for the interop half), so the new section reverts a recorded frontier correction. A related overstatement: README:533–534 says the report-interop half "gains ground the lane did not hold". The PIT vocabulary is new ground, but the interop half was already held for the recorded legs. The right status is: F1 held for report interop, with F1b open (NoCoverage, other formats). PIT's vocabulary adds cross-tool scoring ground. The README is not one of the C1 records (`measure.py:71-73`: lesson, SCORECARD, LOG), so no counter detects this. It is a record defect for the L1 to correct, not a predicate miss.

### README claims that hold at `a21845f`

| Claim (README line) | Evidence |
|---|---|
| PIT seven outcomes, No coverage/Survived split, timeout instability (531) | `corpus/knowledge/pit-outcome-vocabulary.md:16-30`; snapshot shas recomputed equal to the headers: pit-basic-concepts.html `c51d8423…`, pit-faq.html `ccf6ac49…` |
| PIT's code scores run error as detected (531) | `git show a21845f:.ufo/evidence/round-42/sources/pit-DetectionStatus.java \| sed -n 63p` → `  RUN_ERROR(true),` (sha `3bf295ad…` matches) |
| Stryker (held S001) leaves it out of the score (531) | snapshot `stryker-mutant-states.html` line 26, under the "Runtime error" heading (lines 23–26): "It is not represented in your mutation score." `corpus/SOURCES.md:12` = S001 row |
| Assimilated from shokuknow, re-grounded (531) | `pit-outcome-vocabulary.md:10-12` (`staged:S159`, `staged:S160` → S155, S156) |
| Sources column S155, S156, S158, S001 / S157, S153, S001, S158 (531, 532) | all rows present: `corpus/SOURCES.md:12,123,125,126,127,128`; entry headers list the same ids |
| v3 three unflagged sites: scratch 1682/1685, operator-named 123 (532) | scratch clone: `python3 -I tools/write-path-census-v3.py --file tools/context-capture.py` → `:1682 … unflagged=1`, `:1685 … unflagged=1`; `--file tools/registry-replay.py` → `:123 write_bytes expected=1 scratch=0 unflagged=1`. v4 `--json`: 1682/1685 `unflagged False scratch True`, resolved contains `mkdtemp` (True); 123 `unflagged False explicit_out True`, resolved ends `argparse --out`. Source lines: context-capture.py:1624 `self.root = tempfile.mkdtemp(`, :1631-1635 `case_dir` returns `os.path.join(self.root, …)`; registry-replay.py:259 `p.add_argument('--out')`, :181/:185/:282 |
| Lane-wide v4 census 0 unflagged over every tracked `tools/*.py` (538) | scratch clone loop over `git ls-files 'tools/*.py'` with `python3 -I tools/write-path-census-v4.py --file F --json` → `files=26 unflagged_total=0 errors=0`; `--selftest` → `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`, exit 0 |
| Aliases, inheritance, class attributes, `parse_known_args`, sub-parsers named in "What is not claimed" (539–540) | `corpus/knowledge/r42-attribute-and-outflag-destinations.md:70-72` names all five |

### Contract: `claims.*` byte-unchanged since freeze — SURVIVES

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 322b5cd32b4319a05340d249ae752d12a9e6b19f a21845f523b75adbd3e3f7a62af91294db224ad9 -- .ufo/evidence/round-42/contract.json`
Output: one hunk `@@ -61,5 +61,42 @@`. The only change is `"post_freeze_amendments": []` → the P1–P4 array. `claims` ends at line 51 of the file, so the hunk does not touch it.

Semantic cross-check, parsing both revisions' JSON:
`claims_equal True`. Each of predicate, counter_sha256, target, kill_rule, kill_oracle, statement, do_nothing_control and counting_command compares `True` for C1 and C2. `other_keys_changed ['post_freeze_amendments']`.
Counter bytes: `git show REV:<counter> | sha256sum` at both revs gives calibration `9782a5a0…4c0e` and census `3c3727ec…f2`, equal to the contract's `counter_sha256`. `git diff --stat 322b5cd a21845f -- <both counters>` is empty.
History: `git log 322b5cd..a21845f -- contract.json` → only `5f739ac`, which adds all four P entries (`grep -c '"id": "P'` = 4).

### P1–P4 truth at `a21845f` — all SURVIVE

- **P1** (citation only). `SKILL.md:208-209`: "**Inconclusive** = no definitive verdict (timeout, crash before the summary …). Not a kill." S001 snapshot line 26, under Runtime error: "not represented in your mutation score". S158 line 63: `RUN_ERROR(true)`. The counter docstring still carries the old wording at `census/measure.py:19-20` ("PIT's \"Run error\" and Stryker's RuntimeError, which neither tool counts as …"). P1's statement that this wording stays unedited because the bytes are pinned is accurate. found_by `w1/CriticOracleSource.md:9-11,50-70` exists and makes this finding.
- **P2** (disclosure). `calibration/measure.py:236-243`: m7 loops `for _name, text in rec42` only, while m8/m11 use `rec41 + rec42` (:244, :249). The "checked by hand" claim is present at `corpus/lessons/round-42.md:138-139`. found_by `w1/ReviewContract.md:8` (F1) and `w1/ExecC1Falsify.md:35` (row 8, `f8_m7_r41_sid`) both exist.
- **P3** (wording). `.ufo/evidence/round-42/control/c2-junk.stdout`: FAIL F01–F09 and the three live sites, `fixtures_pass=1/10`, exit file `1`. That matches P3, and the contract's original list (F02 F03 F05–F09) did understate it. found_by `w1/ReviewContract.md:17` (F2).
- **P4** (authorship). `w1/ExecV4Tool.md:3,5`: sha256 `eaf67995010c…`, `fixtures_pass=3/10 … live_unflagged_v4=24 … C2_R42_PASS=false`. The tip v4 differs (prerun receipt `prerun/c2-at-5f739acf.stdout` shows tool_sha256 `784de4c0…`). `mutants.json` is absent at the tip, consistent with the unchanged non-author protocol.
- `rule_changed:false` holds for all four, because no predicate, target, kill_rule or counter byte moved. `before_data:true` holds: no deciding-run receipt is tracked at the tip. The only runs are under `.ufo/evidence/round-42/prerun/` (added in `a21845f`), labelled pre-run by path.

Nit (no action): `pit-outcome-vocabulary.md:51` cites `SKILL.md:208-212` where P1 cites `:208-209`. Both ranges hold (210–212 is the kill-rate denominator rule).

## Residual risk / gaps
- v3 has no `--json`, so a lane-wide v3 count was not re-derived here. The three v3 sites were confirmed per file from text output.
- I did not re-locate the PIT and argparse quotes word by word. Only the sha pins and the S001/S158 lines were checked.

## Tooling
No installs or updates.

BROKEN: README Round 42 (corpus/README.md:533–535) says F1 report interop is not held because "no ledger leg has been emitted as a schema report", which contradicts README:385-391 and :413 and the committed round-25 MTE reports. Contract claims.* byte-unchanged and P1–P4 SURVIVE.
