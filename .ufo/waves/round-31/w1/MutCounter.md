# MutCounter — round 31 pre-data counter control

## Verdict

**Two mutants killed; six survived the three assigned fixtures.** All 24 mutant runs completed. The shared pristine and restored-byte matrices both returned the expected **false / true / false** for fixtures a / b / c. The survivors are gaps in these fixtures, not evidence that the frozen predicate should change. No judgment of the lane's eventual C1 result is made.

Axes: **calibration** (primary), coverage of detector branches, and operability of bounded, reproducible probes.

## Evidence

Paths used below:

- `L` = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- `S` = `/fast/scratch/hyaku/tameshi-r31-seats/MutCounter`.
- `R` = `S/isolated/results`.
- The frozen contract is `L/.ufo/evidence/round-31/contract.json:14-26`; the counter's row selection, observation, comparison and acceptance points are `L/.ufo/evidence/round-31/c1-measure.py:111-123,136-166,203-224`.
- Exact single-line edits are retained in `S/mutations.json:2-9`. The mutant source files have now been restored, so this manifest and the recorded mutant hashes describe the attacked bytes.

### Fixtures and expected detector

The detector is the frozen counter CLI itself, with its full 12-command observation set; no replacement observations or shortened regression run were used. A killed mutant must change an expected fixture verdict, not merely return a nonzero status on an intentionally negative fixture.

| Fixture | Sandbox revision | Construction | Expected result |
|---|---|---|---|
| a | `c111dab58b0a8d55e991bbd2efe3aad56717b95a` | Frozen revision, no changes | false, seven mismatches, exit 1 |
| b | `33f94236638e04399e38c5e5cbcfca69b2a08875` | Append correctly restated ten capability rows and two axis rows, using the frozen receipt's observed fields | true, zero mismatches, exit 0 |
| c | `68c9df57a724d2456fb13c57c06f103968c09794` | Child of b; change only the appended sources-registry row count from 92 to 93 | false, one mismatch, exit 1 |

Value source: `L/.ufo/evidence/round-31/before/c1-at-base.stdout:1-12`. Appended fixture tables occupy `S/lane/SCORECARD.md:1484-1500`; the deliberately wrong value in c is at line 1486. Revisions are retained in `S/fixtures.json:2-4`.

`F7`, `F5`, and `F1` below mean `C1_R31_PASS=false`, respectively seven, five, or one mismatches, exit 1. `T0` means `C1_R31_PASS=true`, zero mismatches, exit 0. Every accepted run reported 12 statements, `unparsed=0 unobservable=0 append_only=1`.

| Counter | a | b | c | Mutation verdict |
|---|---|---|---|---|
| Pristine frozen bytes | F7 | T0 | F1 | Expected baseline |
| M01: first row instead of last, line 122 | F7 | F7 | F7 | **Killed by b**: rejects a correct restatement |
| M02: ignore append-only condition, line 221 | F7 | T0 | F1 | **Survived** |
| M03: compare only first tuple value, line 216 | F5 | T0 | T0 | **Killed by c**: accepts the wrong row count |
| M04: UNPARSED becomes MATCH, line 210 | F7 | T0 | F1 | **Survived** |
| M05: Capability-prefixed header accepted, line 114 | F7 | T0 | F1 | **Survived** |
| M06: hidden-table stripping disabled, line 113 | F7 | T0 | F1 | **Survived** |
| M07: pass BASE rather than REV to observations, line 204 | F7 | T0 | F1 | **Survived** |
| M08: observed command exit forced to zero, line 143 | F7 | T0 | F1 | **Survived** |
| Shared restored bytes, executed as M01 | F7 | T0 | F1 | Matches pristine behavior |

Each result has its full output and exact executed command:

| Counter | a summary | b summary | c summary |
|---|---|---|---|
| Pristine | `R/pristine/c1-measure-a.stdout:13` | `R/pristine/c1-measure-b.stdout:13` | `R/pristine/c1-measure-c.stdout:13` |
| M01 | `R/mutated/M01-first-row-a.stdout:13` | `R/mutated/M01-first-row-b.stdout:13` | `R/mutated/M01-first-row-c.stdout:13` |
| M02 | `R/mutated/M02-ignore-append-only-a.stdout:13` | `R/mutated/M02-ignore-append-only-b.stdout:13` | `R/mutated/M02-ignore-append-only-c.stdout:13` |
| M03 | `R/mutated/M03-first-value-only-a.stdout:13` | `R/mutated/M03-first-value-only-b.stdout:13` | `R/mutated/M03-first-value-only-c.stdout:13` |
| M04 | `R/mutated/M04-unparsed-matches-a.stdout:13` | `R/mutated/M04-unparsed-matches-b.stdout:13` | `R/mutated/M04-unparsed-matches-c.stdout:13` |
| M05 | `R/mutated/M05-loose-capability-header-a.stdout:13` | `R/mutated/M05-loose-capability-header-b.stdout:13` | `R/mutated/M05-loose-capability-header-c.stdout:13` |
| M06 | `R/mutated/M06-include-hidden-tables-a.stdout:13` | `R/mutated/M06-include-hidden-tables-b.stdout:13` | `R/mutated/M06-include-hidden-tables-c.stdout:13` |
| M07 | `R/mutated/M07-observe-base-a.stdout:13` | `R/mutated/M07-observe-base-b.stdout:13` | `R/mutated/M07-observe-base-c.stdout:13` |
| M08 | `R/mutated/M08-ignore-command-exit-a.stdout:13` | `R/mutated/M08-ignore-command-exit-b.stdout:13` | `R/mutated/M08-ignore-command-exit-c.stdout:13` |
| Restored | `R/restored/M01-first-row-a.stdout:13` | `R/restored/M01-first-row-b.stdout:13` | `R/restored/M01-first-row-c.stdout:13` |

For every listed output, the adjacent same-stem `.json` records the **exact command at line 6**, executed counter SHA-256 at line 7, actual exit at line 8, elapsed seconds at line 9, and summary at line 10. Full matrix records are `R/pristine-matrix.json`, `R/mutated-matrix.json`, and `R/restored-matrix.json`. All 30 accepted runs had empty stderr.

### Commands and decisive actual output

The sandbox setup used the requested clone and detached checkout, with Git environment overrides unset. Sandbox commits likewise used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`, and only staged `S/lane/SCORECARD.md`. No production Git write command was run.

The matrix runner used fresh work directories, three concurrent counters for pristine/restored, and six for mutants. Accepted runs used a read-only host filesystem plus a writable seat directory; hard-coded `/tmp` writes were bound to `S/tmp`. The mutation matrix was invoked exactly as follows, from S:

```sh
timeout --kill-after=20s 1350 bwrap --ro-bind / / --bind /fast/scratch/hyaku/tameshi-r31-seats/MutCounter /fast/scratch/hyaku/tameshi-r31-seats/MutCounter --bind /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/tmp /tmp --unshare-pid --proc /proc --dev /dev --chdir /fast/scratch/hyaku/tameshi-r31-seats/MutCounter --die-with-parent python3 run-matrix.py --phase mutated
```

It completed normally in 844.65 seconds. Each inner command used `timeout --kill-after=15s 2700 python3 ... --lane S/lane --rev REV --work FRESH_DIR`. For example, the two decisive mutant commands and observed outputs were:

```sh
timeout --kill-after=15s 2700 python3 /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/M01-first-row.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/lane --rev 33f94236638e04399e38c5e5cbcfca69b2a08875 --work /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/isolated/work/mutated/M01-first-row-b
```

```text
STATEMENT sources-registry: claimed=0,44 observed=0,92 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=7 unparsed=0 unobservable=0 append_only=1 rev=33f94236638e04399e38c5e5cbcfca69b2a08875 C1_R31_PASS=false
exit 1
```

Evidence: `R/mutated/M01-first-row-b.stdout:1,13` and its `.json:6-10`. Pristine b returned true with zero mismatches: `R/pristine/c1-measure-b.stdout:13`.

```sh
timeout --kill-after=15s 2700 python3 /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/M03-first-value-only.py --lane /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/lane --rev 68c9df57a724d2456fb13c57c06f103968c09794 --work /fast/scratch/hyaku/tameshi-r31-seats/MutCounter/isolated/work/mutated/M03-first-value-only-c
```

```text
STATEMENT sources-registry: claimed=0,93 observed=0,92 (exit=0) MATCH
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=68c9df57a724d2456fb13c57c06f103968c09794 C1_R31_PASS=true
exit 0
```

Evidence: `R/mutated/M03-first-value-only-c.stdout:1,13` and its `.json:6-10`. Pristine c reported that same tuple difference as MISMATCH and returned false, exit 1: `R/pristine/c1-measure-c.stdout:1,13`.

### Restoration evidence

All eight mutations were reversed at their original single lines. The common pristine SHA-256 before mutation and **all eight** restored SHA-256 values are:

```text
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584
```

The unchanged production counter, the pristine scratch copy, and every restored mutant file returned that hash under `sha256sum`. Actual mutated hashes, also recorded by the detector runner before each run:

| Mutant | SHA-256 while mutated |
|---|---|
| M01 | `45081219bb414162d42c93c07e8ccf9b4132df44bbdfb20a95c4ec1b6529e7ed` |
| M02 | `39072b6d1d04b9eb339546793c7e95de376c50ae4528b35bdc3e9f6f197f9196` |
| M03 | `039684fbe4f4466ec45b14b1ac7aa2c6fbd3ec7da4acb049d30872c21c75a1ff` |
| M04 | `bfc1029237b695adcb370bc59da6a312f4003c089b505690762385d8fa596c14` |
| M05 | `55cad4fc71f9bdd1827e8076af209d58368825347387f5a80c06ee4ddfd1c0e6` |
| M06 | `1c287d082e248f0767522aede48b04dc1a6e3b3d207a5e6b5e73e952cbd93cf5` |
| M07 | `e25b5824514428156d154794a2bca5eb0e57567b385a77e573cbdebbb4f91f01` |
| M08 | `5635345c8b0eee69d101ba9668d8af1b738074477dd3c037177460e5107e7b56` |

Digest record: `S/hash-evidence.json:3-19`; each mutated run's `.json:7` independently records the executed file hash. One common pristine matrix and one common restored-byte matrix were executed, rather than repeating identical pristine/restored bytes at every filename. The restored matrix ran `M01-first-row.py` on all three fixtures and reproduced F7/T0/F1 in 139.73 seconds; the other seven restored files were checked by exact hash, not independently re-executed.

Final scoped process inventory command `python3 process-inventory.py` returned `[]`, retained at `S/final-process-inventory.json:1`. No remaining process had its cwd inside this seat directory.

### Execution caveat

An initial pristine launch was stopped after about 100 seconds when the frozen commands' hard-coded `/tmp` paths were noticed. These three attempts returned exit -15 with no counter summary; they are **inconclusive and excluded**, not kills. That initial launch did not satisfy the private temporary-path bound. The stop checked the runner's cwd first (`S/initial-stop.json`); accepted measurements were then rerun with `/tmp` physically backed by this seat's scratch directory and the host filesystem read-only. Initial attempt records remain under `S/results/pristine/`.

No tools were installed or updated. Existing `bubblewrap 0.13.1` provided filesystem and process isolation. `df -h /fast` reported 175 GiB available before cloning, and 143 GiB at completion.

## Smallest safe correction

**Do not change this round's frozen counter, predicate, statement set, or target.** Extend the fixture coverage with one independent fixture per surviving branch. The following are **[INFERENCE] proposed killing fixtures, not additional executed controls**:

| Survivor | Fixture that would kill it | Expected pristine / mutant difference |
|---|---|---|
| M02 | Correct last rows but a changed byte in the pre-existing SCORECARD prefix; keep every claim equal to its REV observation | Pristine rejects `append_only=0`; mutant accepts zero mismatches |
| M04 | Start from b and append a recognized Capability table containing a sources-registry row with no parseable claim | Pristine rejects one UNPARSED row; mutant accepts despite `unparsed=1` |
| M05 | Start from b and append an otherwise valid wrong sources-registry row beneath `Capability archive`, not the frozen `Capability` header | Pristine ignores that table and passes; mutant consumes it and rejects |
| M06 | Start from b and append a wrong sources-registry table inside an HTML comment or fenced code block | Pristine ignores the hidden table and passes; mutant consumes it and rejects |
| M07 | Make a comment-only change to the recorded-case list so command D prints depth 8 rather than base depth 9; append matching REV rows, including a remeasured calibration value if the input binding changes | Pristine matches REV; mutant observes base depth 9 and rejects |
| M08 | A sources-registry command that prints its normal 92-row output but exits 1, while the last row claims exit 0 and 92 rows; other rows match REV | Pristine catches the exit mismatch; mutant forces observed exit 0 and accepts |

These additions address the demonstrated three-fixture coverage limits without treating surviving mutants as permission to alter C1.
