# MutCounter — counter mutation probe

## Verdict

Eight single-line counter mutants were exercised on all five assigned fixtures. **Five were killed by complete receipt comparison; three survived:** M02 (label only), M05 (runner SHA gate removed), and M07 (copy label leaked through the filename). **If the detector checks only the C1 verdict and process exit, only M04 is killed and seven survive.** These are fixture coverage findings, not permission to change the frozen contract or counter.

The pristine detector matched all five expected negative fixtures. There were 40 mutated runs and 40 restored runs; every restored stdout, stderr, and exit matched its pristine fixture exactly. No run was inconclusive.

Axes: operability (assigned), observable discrimination (verdict versus complete receipt), reproducibility (seed, revisions, hashes), and isolation (scratch-only execution). Four independent fixture processes ran concurrently; no seats or other runtimes were dispatched.

## Evidence

All scratch paths below are relative to `/fast/scratch/hyaku/tameshi-r32-seats/MutCounter/` unless absolute. The only write outside that directory is this report.

### Frozen specification and setup

Read first: `.ufo/evidence/round-32/c1-measure.py` and `.ufo/evidence/round-32/contract.json` in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/`.

Relevant specification: `contract.json:13` defines the predicate; `:17-20` specifies the conjuncts; `:33` requires the negative controls to fail. Counter anchors: `c1-measure.py:189-194` classifies tool outcomes, `:224-225` checks the committed runner, `:240` selects the committed tool, `:245-250` materializes copies, and `:267-277` aggregates and decides.

Executed in the seat directory, with Git environment overrides unset:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/MutCounter/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/MutCounter/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /fast/scratch/hyaku/tameshi-r32-seats/MutCounter/pristine.py
cp pristine.py c1-measure.py
df -h /fast
```

Clone and checkout exited 0 without output. Storage receipt: `/dev/nvme1n1p2`, 804G total, 692G used, 112G available, 87% used. No tools were installed or updated.

### Fixtures

All fixture commits exist only in the scratch clone. The tool bodies consist of a Python shebang followed by the indicated statements.

| Fixture | Revision | Tool behavior |
|---|---|---|
| a | `c31814978969a41a8e9b0f7d99fa308c5993c1b7` | No tool |
| b | `2ed14237e59709a1e677171c8c5d40b4d33a6679` | Print `TALLY_AUDIT: FAIL`, exit 1 |
| c | `70e5b3a75634b67a976f910e5db847bdf3e3e440` | Print `TALLY_AUDIT: PASS`, exit 0 |
| d | `4790423efa28358690853a526ff1a5a4ea91648c` | Print nothing, exit 1 |
| e | `1ae584bd52fa64e1ea057348e4134674bebb1da9` | Same tool as b; runner comment has one changed byte |

Fixture e changes byte offset 22 (zero-based), `m` to `M`, in `tools/mutate-and-run.sh:2`. Byte comparison observed exactly one difference, with unchanged length. Its runner SHA-256 is `137fb5e6200df85af66022aca0c88336f60c1d37692cd716d35a23fe6910bf18`; a–d have the pinned runner SHA. During all detector phases the clone working tree stayed at fixture e, including its always-FAIL tool. This deliberately makes the working tree disagree with a, c, and d for M08.

### Mutants

Each changes exactly one behavior-bearing line in a separate copy of the frozen counter. Exact old/new lines and mutated hashes are retained in `mutation-edits.json`; the revision and file manifest is `probe-manifest.json`.

| Mutant | Frozen counter line | Single edit |
|---|---:|---|
| M01-exit-only | 189 | Kill classification requires `rc == 1` only |
| M02-label-only | 189 | Kill classification requires the FAIL prefix only |
| M03-other-is-kill | 267 | Kill aggregation accepts both `KILL` and `OTHER` |
| M04-ignore-accept | 274 | Remove `acc == N_ACCEPT` from the predicate |
| M05-drop-runner-sha | 274 | Remove `runner_sha_ok == 1` from the predicate |
| M06-skip-generated | 246 | Filter out labels starting with `g` before materialization |
| M07-leak-label | 247 | Prefix the random copy filename with its case label |
| M08-working-tree-tool | 240 | Read `lane/tools/tally-audit.py` using `cat`, instead of `git show REV:...` |

### Detector and actual commands

`run-probe.py` executes the requested `timeout 1200 python3 COUNTER --lane ... --rev ... --work FRESH_DIR --seed 1` command for every fixture, at concurrency four. Each counter retains its default four tool workers. It stores unedited stdout, stderr, exit, and exact command in `receipts/PHASE/PROGRAM--FIXTURE.{stdout,stderr,exit,command}`. All work directories are fresh and inside this seat.

Executed, in order, with an exact byte restoration of all eight counter copies before the third command:

```sh
timeout 1200 python3 run-probe.py --phase pristine
timeout 1200 python3 run-probe.py --phase mutated
timeout 1200 python3 run-probe.py --phase restored
timeout 60 python3 classify-results.py
```

All four driver commands exited 0. The last command observed:

```text
DETECTOR_RESULT: baseline=5/5 mutated=40 restored_exact=40/40 inconclusive=0 verdict_killed=1/8 full_receipt_killed=5/8
```

The verdict detector compares `(process exit, C1_R32_PASS)`. The complete receipt detector compares the entire stdout, stderr, and exit; no normalization is required because copy outcomes are printed in deterministic order and the random filenames are not printed. Both comparisons use the same five pristine runs and all 40 mutated/restored runs. Expected pristine rejections were checked before classification; an expected rejection is not a baseline failure.

An exact individual invocation, retained at `receipts/mutated/M04-ignore-accept--b.command:1`, was:

```sh
timeout 1200 python3 /fast/scratch/hyaku/tameshi-r32-seats/MutCounter/M04-ignore-accept.py --lane /fast/scratch/hyaku/tameshi-r32-seats/MutCounter/lane --rev 2ed14237e59709a1e677171c8c5d40b4d33a6679 --work /fast/scratch/hyaku/tameshi-r32-seats/MutCounter/work/mutated/M04-ignore-accept--b --seed 1
```

Observed stdout at `receipts/mutated/M04-ignore-accept--b.stdout:27`, exit 0:

```text
C1_R32: kill=18/18 accept=0/8 other=8 runner_sha_ok=1 tool_present=1 seed=1 rev=2ed14237e59709a1e677171c8c5d40b4d33a6679 C1_R32_PASS=true
```

The corresponding pristine and restored runs exit 1 with the same counts and `C1_R32_PASS=false`.

### Full five-fixture result table

Each cell is `verdict kill/accept/other`. `F` means exit 1 and `C1_R32_PASS=false`; `T` means exit 0 and `C1_R32_PASS=true`. Denominators remain 18 kills and 8 accepts. Normally each receipt has 26 COPY lines; M06 has only 15. Runner SHA is valid for a–d and invalid for e throughout. Tool presence is 0 for a and 1 otherwise, except M08 reports presence 1 for a.

| Counter | a | b | c | d | e | Verdict detector | Complete receipt detector |
|---|---|---|---|---|---|---|---|
| Pristine | F 0/0/26 | F 18/0/8 | F 0/8/18 | F 0/0/26 | F 18/0/8 | Expected baseline | Expected baseline |
| M01-exit-only | F 0/0/26 | F 18/0/8 | F 0/8/18 | F 18/0/8 | F 18/0/8 | Survived | Killed: d |
| M02-label-only | F 0/0/26 | F 18/0/8 | F 0/8/18 | F 0/0/26 | F 18/0/8 | Survived | Survived |
| M03-other-is-kill | F 18/0/8 | F 18/0/8 | F 0/8/18 | F 18/0/8 | F 18/0/8 | Survived | Killed: a, d |
| M04-ignore-accept | F 0/0/26 | T 18/0/8 | F 0/8/18 | F 0/0/26 | F 18/0/8 | Killed: b | Killed: b |
| M05-drop-runner-sha | F 0/0/26 | F 18/0/8 | F 0/8/18 | F 0/0/26 | F 18/0/8 | Survived | Survived |
| M06-skip-generated | F 0/0/15 | F 9/0/6 | F 0/6/9 | F 0/0/15 | F 9/0/6 | Survived | Killed: a–e |
| M07-leak-label | F 0/0/26 | F 18/0/8 | F 0/8/18 | F 0/0/26 | F 18/0/8 | Survived | Survived |
| M08-working-tree-tool | F 18/0/8 | F 18/0/8 | F 18/0/8 | F 18/0/8 | F 18/0/8 | Survived | Killed: a, c, d |

Additional concrete witnesses:

- `receipts/mutated/M01-exit-only--d.stdout:1` prints `COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last=''`. It counts silent failure as a kill; `:27` reports 18 kills instead of zero.
- `receipts/mutated/M06-skip-generated--b.stdout:16` reports `kill=9/18 accept=0/8 other=6`; only 15 COPY lines precede it.
- `receipts/mutated/M08-working-tree-tool--a.stdout:27` reports `kill=18/18 accept=0/8 other=8 runner_sha_ok=1 tool_present=1` despite the selected revision containing no tool.
- `receipts/classification.json` records all killed/survived classifications and witness fixture IDs. Every individual run has a saved exact invocation and exit receipt.

### Restoration and hashes

The counter copies were restored with the inverse single-line edits before the restored phase. The common before and restored SHA-256 is:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca
```

`sha256sum pristine.py c1-measure.py M01-exit-only.py M02-label-only.py M03-other-is-kill.py M04-ignore-accept.py M05-drop-runner-sha.py M06-skip-generated.py M07-leak-label.py M08-working-tree-tool.py` observed that exact hash for every file after restoration. The files named M01–M08 now contain pristine bytes, not active mutants.

| Mutant | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|
| M01 | `86b66b9e8d5413a8ea9f36bceaa22f89418be908c85c3695d2496905397106e2` | Common restored hash above |
| M02 | `73ebee09f31bbb6a7a596b0f5940333c4aa1224b717aeb14d5688f73a5c0803f` | Common restored hash above |
| M03 | `67864fc6592d88089adb4b08f629f8ffd2cb91455b935252e10aa2cefa0fac5d` | Common restored hash above |
| M04 | `c3178908538b6842ccdd793f3fc38a60d12d6e8f7324a83006db377b07cbf29d` | Common restored hash above |
| M05 | `05f3fda4936457393533ef6d50e532e33023174e06c66561e6a83af8ca3d2f91` | Common restored hash above |
| M06 | `4b3740a459962823da1809bc00072c17ee7bae732d0712985ebb8ebf1fe6c197` | Common restored hash above |
| M07 | `395fc7b73a296e18903c9d3ff58fc897e2493df4cac37748b5df46db92f6a5db` | Common restored hash above |
| M08 | `7f8af15cc74dd29bbba89fb5ede58b3bd1984a7fdbb4ff9bab0b63bb1635f642` | Common restored hash above |

Production source hashes observed before and after the probe are identical: counter `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca`; runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`. The production contract and its frozen committed blob both hash to `7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583`.

All 85 counter processes and all driver processes completed; no service or live detector was left running. Scratch fixture commits, their deliberate runner edit, and bounded evidence artifacts are retained for reproduction. No production source or frozen evidence was edited.

## Smallest safe correction: supplemental fixtures, not a contract change

Keep the frozen counter and contract unchanged. A separate counter regression suite should assert full receipts, not only the final false verdict: this immediately exposes M01, M03, M06, and M08 in the existing fixture panel.

For the remaining coverage gaps, the following fixture descriptions name distinguishing tests. **[INFERENCE] These additional fixtures were not executed in this assignment.** A shared seed-1 selective oracle can recognize the exact 26 fixture bodies by SHA-256 and return the contract's expected status and label; that is a test fixture, not a proposed audit implementation or a claim about other seeds.

| Verdict survivor | Fixture that would kill it | Expected pristine versus mutant verdict |
|---|---|---|
| M01-exit-only | Selective silent-fail tool: accept all eight accept bodies correctly; for the 18 kill bodies exit 1 without output; pinned runner | False versus true |
| M02-label-only | Selective wrong-status tool: accept the eight accept bodies correctly; print FAIL but exit 0 for all 18 kill bodies; pinned runner | False versus true |
| M03-other-is-kill | Selective OTHER tool: accept the eight accept bodies correctly; exit 2 without a label for all 18 kill bodies; pinned runner | False versus true |
| M05-drop-runner-sha | Complete seed-1 oracle tool, committed with the one-byte runner change from e | False versus true; all 26 classifications otherwise correct |
| M06-skip-generated | Complete seed-1 oracle tool with the pinned runner | True versus false; mutant runs only 9 kill and 6 accept copies |
| M07-leak-label | Path-aware tool: accept only basenames starting with uppercase `B` or `gB`; otherwise fail; pinned runner | False versus true; opaque lowercase-hex names never expose those prefixes |
| M08-working-tree-tool | Commit the complete seed-1 oracle with the pinned runner, then replace only its working-tree tool with the always-FAIL body | True versus false |

M02, M05, and M07 also kill the complete-receipt survivors. Fixture e alone cannot test the SHA conjunct decisively: its always-FAIL tool already fails the accept conjunct, masking removal of the SHA gate. No changes to the claimed invariant, generated families, frozen predicate, or target are proposed.
