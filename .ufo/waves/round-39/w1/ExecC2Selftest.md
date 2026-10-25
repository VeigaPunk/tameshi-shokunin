# ExecC2Selftest — C2 write-path census selftest (round 39, w1)

Seat: leaf executor, milestone C2 selftest. Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
No live-lane edit was made. All mutation work ran in `/tmp/tameshi-r39-ExecC2Selftest/`.

## Assigned command — result

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 tools/write-path-census.py --selftest
WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1
EXIT_CODE=0
```

All four contract-named fields are exact: `planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1`.

Tool pin check (`tools/write-path-census.py`):

```
$ sha256sum tools/write-path-census.py
bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62  tools/write-path-census.py
```

Matches `claims.C2.tool_sha256` in `.ufo/evidence/round-39/contract.json` byte-for-byte. `tool_sha_ok=1`.

## Mutant kill (the C2 discriminator) — holds

Contract: "the same selftest fails after the FLAG_GATE early-return is removed."

Removal mutant (`tools/write-path-census.py:80` guard deleted on a scratch copy):

```
$ cp tools/write-path-census.py /tmp/tameshi-r39-ExecC2Selftest/m0.py   # then delete the 2 guard lines
$ python3 /tmp/tameshi-r39-ExecC2Selftest/m1.py --selftest
WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=0 noflag_unchanged=0
FAIL no-flag path wrote or changed the expected file
MUTANT_EXIT=1
```

The harness's own mutant form (`.ufo/evidence/round-39/census/measure.py:119`, `return False  # FLAG_GATE` -> `update = True  # FLAG_GATE`) also kills: `mutant_killed=1`. Both mutants fail for the right reason — the no-flag path writes the expected file.

## Counter at both revisions

```
$ python3 .ufo/evidence/round-39/census/measure.py --lane . --rev 50aadd1bbd94e43cd3fcfb81459414394db2dc35
C2_R39: tool_absent=1 gates=0/21 planted_unflagged=0 planted_flagged=0 planted_scratch=0 fixture_wrote=0 mutant_killed=0 rev=50aadd1... C2_R39_PASS=false
BASE_EXIT=1

$ python3 .ufo/evidence/round-39/census/measure.py --lane . --rev HEAD
C2_R39: tool_absent=0 tool_sha_ok=1 gates=21/21 live_write_sites=99 live_unflagged=0 planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 mutant_killed=1 rev=HEAD C2_R39_PASS=true
HEAD_EXIT=0
```

Base stays false (do-nothing control intact), HEAD converges true. C1 base control also re-checked and unchanged:

```
C1_R39: guard_absent=1 live_d=9/9 strip_d=0/0 live_agree=0 stripped_agree=0 r38_regex_hits=0 mismatches=1 ... C1_R39_PASS=false   (exit 1)
```

`measure.py` classifies the 21 gates from REV bytes, not the worktree: it `git show`s each `tools/<gate>` at `--rev` into a temp root before running `--census` (`measure.py:104-112`). That conjunct is genuinely met.

## Findings (depth axis) — predicate not falsified, measurement depth is thinner than the field line suggests

1. **`noflag_unchanged` is not an independent measurement; it is `fixture_wrote` re-printed.** `tools/write-path-census.py:107` computes `fixture_wrote = 0 if any('update flag' in item or 'no-flag' in item for item in failed) else 1`; line 109 prints `noflag_unchanged=%d` as `1 if fixture_wrote else 0`. The two columns are the same bit, so the six-number line carries five independent numbers, not six. It is mislabeled on update-only failures:

   ```
   $ # mutant2: update_expected returns True without writing; the no-flag path is untouched, hence CORRECT
   $ python3 /tmp/tameshi-r39-ExecC2Selftest/m2.py --selftest
   WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=0 noflag_unchanged=0
   FAIL update flag did not write the expected file
   EXIT=1
   ```

   `noflag_unchanged=0` printed while the no-flag behaviour was in fact correct. The name promises per-branch reporting the code does not implement.

2. **The live axis is empty: `live_unflagged=0` out of `live_write_sites=99` is not a clean result, it is a no-observation result.** No gate in the 21-set writes a path matching `EXPECTED_RE` (`.expected|expected.txt|golden|snapshot`). Verified by re-running the module's own classifier over all 21 gates: every gate reports `file_global_bare=0` and `perline_bare=0`. The 49 "expectedish" lines in `tools/repeat-control.py` and the 17 in `tools/golden-verdict.py` are prose and verdict identifiers, not write targets. Consequence: all C2 discrimination comes from the three synthetic `PLANTED` strings; the 21-gate corpus — the actual subject of the claim — contributes zero positive signal. A census reporting `0` here cannot be distinguished from a census that looked at nothing, except through the plantings.

3. **The highest-write gate is the least covered.** `tools/mutate-and-run.sh` contains 231 shell `>`/`>>` redirects; the census sees exactly one "write site" in it, and that one is Python embedded in a heredoc (`tools/mutate-and-run.sh:429`, `with open(mutant, 'wb')`). The docstring discloses that shell redirects are outside the frozen patterns, but the effect is that the shell gate's real write surface is ~100% invisible while the tool prints `gates=21/21`.

4. **`WRITE_RE` is blind to nested-call `open()`.** `tools/write-path-census.py:46-50` uses `open\s*\([^)]*['"](?:w|...)['"]`, and `[^)]*` cannot cross the inner `)`. Verified:

   ```
   nested-open detected: False      # open(os.path.join(tmp, "case.expected"), "w")
   flat-open  detected: True        # open("case.expected","w")
   ```

   Live impact is one line: `tools/registry-check.py:1099` — `with open(os.path.join(fixture_repo, "seed.txt"), "w",`. Small, but it is the most common Python write idiom and the miss is structural, not incidental.

5. **Scope note (not a defect):** `GATES` excludes `tools/round21-measure.py` and `tools/wave-parent-settle.py`. The 21-set is frozen by contract, so this is declared scope, recorded only so no one reads `21/21` as "all lane gate tools". `tools/` holds 27 entries.

## Verdict on the C2 predicate as frozen

C2_R39_PASS=true at HEAD is **supported**: pin matches, the four planted fields are exact, the FLAG_GATE removal kills the selftest, and all 21 gates are read from REV bytes. No predicate conjunct is falsified and no predicate was rewritten.

Residual risk the parent should weigh: findings 1 and 2 mean the PASS rests entirely on three synthetic strings plus the sha pin. The live classification number (`live_unflagged=0`) should not be quoted as evidence of good write hygiene in the gate corpus; it is evidence that the frozen pattern set does not match the corpus.

## Installs

None. No pacman, no uv/cargo/npm, no new tool. Only `python3`, `sha256sum`, `cp`, `grep` from the base system.
