# CtlHeaderV2

**Verdict: the expected all-reject v2 pattern was not established.** Shape B survived v2. Shapes C and D were killed by v2's byte-prefix check. Shape A's v2 rejection is **inconclusive for the header repair**: its sole mismatch was a regression-leg result, not an axis row. Both pristine and restored controls passed both counters. No failed shape was rerun.

Axis under examination: **calibration**. The depth and calibration values in the appended rows are test inputs, not new axis-improvement claims.

| Shape | v1 verdict | v2 verdict |
|---|---|---|
| A: appended second header cell `Score` | PASS, exit 0 | FAIL, exit 1; unrelated regression mismatch, not a header kill |
| B: appended `Score (0-10)`, ASCII hyphen-minus | FAIL, exit 1; unrelated regression mismatch | PASS, exit 0; **SURVIVED** |
| C: first ten original lines CRLF, plus canonical appended rows | PASS, exit 0 | FAIL, exit 1; **KILLED**, `append_only=0` |
| D: U+200B inserted at the end of original line 1 | FAIL, exit 1; **KILLED**, `append_only=0` | FAIL, exit 1; **KILLED**, `append_only=0` |

The requested v1 acceptance of A was observed, as was v1 acceptance of C. The requested v2 rejection of B was not observed. A's observed v2 failure must not be credited to the header change.

## Evidence

All scratch paths below are relative to `/fast/scratch/hyaku/tameshi-r32-seats/CtlHeaderV2/`. Production files were read-only except this assigned report. No sibling scratch directory was opened. No tools were installed or upgraded.

### Isolation, detector and commands

The lane was cloned at exactly `08125328f87df92d3f25d0034ee792253ecbcbd9` with:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout --quiet --detach 08125328f87df92d3f25d0034ee792253ecbcbd9
python3 make-shapes.py
```

The first two commands exited 0 without output. The third exited 0 and printed the four commits and byte hashes below. `make-shapes.py:28-67` constructs all four documents from the same backed-up bytes, creates one independent sandbox commit per shape, each parented directly to the requested revision, and restores the sandbox index to that revision. Only the SCORECARD blob differs in those commits. The main sandbox worktree remained pristine.

Unmodified counter copies:

| Counter | Original path within the production lane | Scratch copy SHA-256 |
|---|---|---|
| v1 | `.ufo/evidence/round-31/c1-measure.py` | `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` |
| v2 | `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py` | `e49b00de184ecb4c3a94b49b9d89a13650b13bc8ca6cd57c1a5f68c971f713b7` |

Each detector invocation used the same `run-detector.py:17-33` wrapper. It runs the entire frozen counter, not a substituted parser check, with `timeout 2700`, a fresh `--work`, and `--lane` pointing to this seat's clone. `bwrap` makes the host read-only, binds this seat writable, maps `/tmp` into this seat's `tmp/`, and places HOME here. Thus literal `/tmp` writes by the frozen selftests stay inside the seat. Every regression receives the counter's `{work}/regression-wd` argument. Disk was checked before cloning: `/fast` had 114G available.

Exact detector argv, including the sandbox options, are in each `logs/<phase>-<version>.json:5-44`; process exit is at line 47. The common inner command is:

```sh
timeout 2700 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlHeaderV2/counters/VERSION.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlHeaderV2/lane --rev REV --work /fast/scratch/hyaku/tameshi-r32-seats/CtlHeaderV2/work-PHASE-VERSION
```

The actual outer commands, all run from this seat, were:

```sh
python3 run-detector.py pristine v1 08125328f87df92d3f25d0034ee792253ecbcbd9
python3 run-detector.py pristine v2 08125328f87df92d3f25d0034ee792253ecbcbd9
python3 run-detector.py A v1 cc0bc7f626d6c7fe43e7d33f5f9db4f4c8d16132
python3 run-detector.py A v2 cc0bc7f626d6c7fe43e7d33f5f9db4f4c8d16132
python3 run-detector.py B v1 0aa6385d1a89f4686cbdbdc7239e6b8fd13bafcd
python3 run-detector.py B v2 0aa6385d1a89f4686cbdbdc7239e6b8fd13bafcd
python3 run-detector.py C v1 3ad5a86d501f81d2811b1686837bfa761390214e
python3 run-detector.py C v2 3ad5a86d501f81d2811b1686837bfa761390214e
python3 run-detector.py D v1 5dcad0d3c2d6c30c103bfa0e43c9c391e5e78c6f
python3 run-detector.py D v2 5dcad0d3c2d6c30c103bfa0e43c9c391e5e78c6f
python3 run-detector.py restored v1 08125328f87df92d3f25d0034ee792253ecbcbd9
python3 run-detector.py restored v2 08125328f87df92d3f25d0034ee792253ecbcbd9
```

The v1/v2 runs and shape runs were launched concurrently. The restored pair was launched after the mutation runs had completed. All twelve calls finished without an outer timeout or setup exit. All twelve counter stderr logs are empty. Pristine calls took 542.714s/v1 and 526.723s/v2; mutation calls took 540.416–547.745s; restored calls took 185.676s/v1 and 185.542s/v2.

### Mutations and hashes

A and B append exactly the same two rows, `depth | 9` and `calibration | 8`, differing only in the second header cell. See `fixtures/A/SCORECARD.md:1557-1560` and `fixtures/B/SCORECARD.md:1557-1560`. C appends those rows under the canonical `Score (0–10)` header after converting only the first ten old line endings. D changes only original line 1. Construction is at `make-shapes.py:34-46`.

| Bytes | Sandbox commit | SCORECARD SHA-256 |
|---|---|---|
| Pristine | `08125328f87df92d3f25d0034ee792253ecbcbd9` | `798e814e45810009c0067a097743aa467c740c9e55b5a460820dea896df71b47` |
| A | `cc0bc7f626d6c7fe43e7d33f5f9db4f4c8d16132` | `c62dbc505b66eeee17d6fcd1bef8821bdc7f45d2163b85d06a0c45e7fabceb28` |
| B | `0aa6385d1a89f4686cbdbdc7239e6b8fd13bafcd` | `f8cde4088ad25edc948e670fd9b541c243359068e5c64609df255d12b109ac40` |
| C | `3ad5a86d501f81d2811b1686837bfa761390214e` | `a705ddf981a5155bf4d316a14ef473e1a0556dae4b953398f430cf61374f725f` |
| D | `5dcad0d3c2d6c30c103bfa0e43c9c391e5e78c6f` | `65d7117bd5361051b4bac0b890ce3dbb5caceeb6c90da1e0206f635e0b1b6aa9` |
| Restored | original bytes at the pristine revision | `798e814e45810009c0067a097743aa467c740c9e55b5a460820dea896df71b47` |

`shape-manifest.json:2-46` records the commit and hash results. `byte-properties.json:2-12` records exactly ten CRLF endings for C, and one U+200B for D. U+200B is one code point but **three UTF-8 bytes**, `e2 80 8b`; removing it reproduces the original bytes exactly.

### Observed stdout

Each full counter stdout has twelve STATEMENT lines followed by its summary at `logs/<phase>-<version>.stdout:13`. Actual mutation summaries:

```text
A v1: C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=cc0bc7f626d6c7fe43e7d33f5f9db4f4c8d16132 C1_R31_PASS=true
A v2: C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=cc0bc7f626d6c7fe43e7d33f5f9db4f4c8d16132 C1_R31_PASS=false
B v1: C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=0aa6385d1a89f4686cbdbdc7239e6b8fd13bafcd C1_R31_PASS=false
B v2: C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=0aa6385d1a89f4686cbdbdc7239e6b8fd13bafcd C1_R31_PASS=true
C v1: C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=3ad5a86d501f81d2811b1686837bfa761390214e C1_R31_PASS=true
C v2: C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=0 rev=3ad5a86d501f81d2811b1686837bfa761390214e C1_R31_PASS=false
D v1: C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=0 rev=5dcad0d3c2d6c30c103bfa0e43c9c391e5e78c6f C1_R31_PASS=false
D v2: C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=0 rev=5dcad0d3c2d6c30c103bfa0e43c9c391e5e78c6f C1_R31_PASS=false
```

Both pristine stdout files and both restored stdout files end with exactly:

```text
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=08125328f87df92d3f25d0034ee792253ecbcbd9 C1_R31_PASS=true
```

Their corresponding JSON receipts record exit 0 at line 47.

### Header-control limitation and confounded failures

The successful starting revision already has a canonical table at `lane/SCORECARD.md:1534-1537` with the same values, 9 and 8, as the appended rows. v2's `counters/v2.py:117-129` **ignores** an unrecognized table; it does not reject the whole document merely for containing one. Therefore the old canonical rows remain available. The frozen predicate concerns the last row of the frozen table type, not a blanket prohibition on other headers (`lane/.ufo/evidence/round-31/contract.json:14`). B's acceptance does not establish that v2 incorrectly recognized its malformed header.

In both confounded calls, the two axis statements still MATCH (`logs/A-v2.stdout:11-12`, `logs/B-v1.stdout:11-12`). The sole mismatch was:

```text
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=FAIL,9,8,1 (exit=1) MISMATCH
```

At `work-A-v2/obs-six-leg-regression-ledger.stdout:17-20,51`:

```text
REGRESSION_DEFECT bash-tsukuroi-census B9: measured=KILLED recorded=SURVIVED
REGRESSION_TABLE bash-tsukuroi-census: match=9/10 recorded-killed=6 measured-killed=7 survived=3 inconclusive=0 flips=1
REGRESSION_CASE bash-tsukuroi-census: FAIL (out of band: killed-delta=1 flips=1; log: /fast/scratch/hyaku/tameshi-r32-seats/CtlHeaderV2/work-A-v2/regression-wd/bash-tsukuroi-census/sweep.log)
REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
```

The paired B/v1 log at `work-B-v1/obs-six-leg-regression-ledger.stdout:17-20,51` reports the same out-of-band result, with **B7** rather than B9 flipped. These observed failures were retained, not rerun or relabeled as header detections. Their underlying cause was not investigated in this assigned probe.

C is the discriminating repair control: all twelve statements MATCH, but the old counter reports `append_only=1` while v2 reports 0. v1's text-mode prefix check is at `counters/v1.py:196-201`; v2's raw-byte check is at `counters/v2.py:202-209`. D verifies that both counters reject a substantive old-prefix edit even when it is invisible.

### Restoration and process closure

The four mutants are independent committed blobs; they never replaced the main sandbox worktree. Before the restored pair, `SCORECARD.pristine` was explicitly copied back over `lane/SCORECARD.md`. `restoration.json:4-7` records identical before, after and backup hashes and `exact_equal=true`. The restored counter outputs above confirm the pristine behavior returned. `restoration.json:8-11` also records the runner hash `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` and unchanged counter hashes.

All detector jobs completed. A final `/proc` scan, restricted by this seat's cwd and detector command markers, found no remaining owned detector processes; no kills were needed (`process-cleanup.json`). No production runner, counter, contract, Git index or other seat was edited. Only this report was written outside the scratch seat.

## Smallest safe correction

Correct the **header-control design or its expected result**, not the frozen predicate. At this requested starting revision, appending the same values under an ignored header is not a discriminating negative control because an already-correct eligible table remains. Do not credit A's regression failure as a kill, and do not broaden v2 into rejecting every noncanonical table just to force the expected outcome.

[INFERENCE] A future discriminating A/B pair could make only the post-base canonical header at line 1534 ineligible before appending the malformed-header rows, leaving the original base prefix intact. Then v2 would fall back to the stale baseline table at lines 64-67, while v1 could select the new rows. That amended fixture was not exercised here; the four assigned shapes and their observed outcomes above are unchanged.
