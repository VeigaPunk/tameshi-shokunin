# Verdict

**9 killed, 3 survived, 0 inconclusive** under the two required detectors. The survivors are M04 (named-target boundary), M05 (target extraction), and M12 (target case folding). All 12 pristine baselines and all 12 restored copies produced the required outputs. These are coverage findings, not a judgment of C1 or the round.

Seat: `MutDeadSeatCheck`.

Axes: **quality** (behavioral defect detection), **calibration** (baseline-valid verdicts and explicit survivors), and **isolation** (single edits and exact byte restoration). No production behavior or contract was changed.

# Evidence

- Frozen revision: `2da841bd9913a2037d2bf612793382e572c9d205`; sandbox `git rev-parse HEAD` printed that exact revision.
- All code ran with cwd `/fast/scratch/hyaku/tameshi-r31-seats/MutDeadSeatCheck/c`; every mutant was a separate copy at `/fast/scratch/hyaku/tameshi-r31-seats/MutDeadSeatCheck/c/.mutation-probe/M01.py` through `M12.py`.
- Each copy received exactly one one-line edit, independently from the pristine source. The original clone target was not edited. All 12 copies were restored after the mutation run.
- Source contract at this revision: `.ufo/evidence/round-31/dead-seat-check.py:26-35` specifies target boundaries, lowercase tokens, inclusive Jaccard, and name normalization; `:49-52` specifies exit status and nonempty inputs.
- Implementation anchors: `.ufo/evidence/round-31/dead-seat-check.py:67`, `:101`, `:121`, `:163-176`, `:181-186`, `:213-217`, and `:248-257`. The table below identifies each exact edited line.
- Detector anchors: `.ufo/evidence/round-31/dead-seat-check.py:269-277` compares exit status and stdout; `:287-288` computes expected similarities through the same helpers being tested; `:306-337` also uses `target_of()` to build fixtures or expected values.
- The real dead-seat list is name-only (`.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt:2-10`); `ConnectorOverlap` is at line 7. Consequently this case exercises name reuse and exit status, not target similarity.

## Commands and pristine output

Clone commands executed from the seat directory, both without output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/MutDeadSeatCheck/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/MutDeadSeatCheck/c checkout -q --detach 2da841bd9913a2037d2bf612793382e572c9d205
```

Bounded batch commands executed from the clone:

```sh
timeout 60s python3 .mutation-probe/probe.py pristine
timeout 60s python3 .mutation-probe/probe.py mutated
timeout 60s python3 .mutation-probe/probe.py restored
```

Each batch used at most six concurrent subjects. Every child had a 15-second timeout and 128 KiB captured-output bound. No timeout occurred. Children inherited `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=/fast/scratch/hyaku/tameshi-r31-seats/MutDeadSeatCheck/c/.mutation-probe/tmp`, keeping temporary selftest files inside this seat. All child processes completed synchronously; no process kill or background service was used.

The driver executed these exact child argument vectors in **each** of the pristine, mutated, and restored phases:

```sh
timeout 15s python3 .mutation-probe/M01.py --selftest
timeout 15s python3 .mutation-probe/M01.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M02.py --selftest
timeout 15s python3 .mutation-probe/M02.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M03.py --selftest
timeout 15s python3 .mutation-probe/M03.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M04.py --selftest
timeout 15s python3 .mutation-probe/M04.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M05.py --selftest
timeout 15s python3 .mutation-probe/M05.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M06.py --selftest
timeout 15s python3 .mutation-probe/M06.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M07.py --selftest
timeout 15s python3 .mutation-probe/M07.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M08.py --selftest
timeout 15s python3 .mutation-probe/M08.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M09.py --selftest
timeout 15s python3 .mutation-probe/M09.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M10.py --selftest
timeout 15s python3 .mutation-probe/M10.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M11.py --selftest
timeout 15s python3 .mutation-probe/M11.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
timeout 15s python3 .mutation-probe/M12.py --selftest
timeout 15s python3 .mutation-probe/M12.py --dead .ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt --spec .ufo/waves/round-30/spec-wC.json
```

Expected and observed pristine selftest on every copy: exit **0**, stdout empty, stderr:

```text
DEAD_SEAT_CHECK_SELFTEST: ok=17
```

Expected and observed pristine real case on every copy: exit **1**, exactly this stdout:

```text
FLAG item=ConnectorOverlap dead=ConnectorOverlap reason=name-reuse jaccard=-
```

And exactly this stderr:

```text
DEAD_SEAT_CHECK: dead=9 items=38 flagged=1 threshold=0.60
```

Call those exact real-case streams **F**. All restored copies returned the same selftest result and F/exit 1. There were 72 required detector invocations, plus nine separately labeled diagnostic witness invocations.

## Required mutant table

`fail=N` is the emitted assertion-failure count, not a count of distinct cases. Every selftest stdout was empty. A mutant is killed only if a required detector differs from its passing pristine baseline; an expected real-case exit 1 is not itself a detector failure.

| Mutant | Single edit at frozen source line | Selftest result | Real-case result | Verdict |
|---|---|---|---|---|
| M01 | `.ufo/evidence/round-31/dead-seat-check.py:182`: `name.lower()` → `name` | exit 1; `fail=1` | F; exit 1 | **killed** |
| M02 | `.ufo/evidence/round-31/dead-seat-check.py:67`: `[^a-z0-9]` → `[^a-z0-9_]` | exit 1; `fail=1` | F; exit 1 | **killed** |
| M03 | `.ufo/evidence/round-31/dead-seat-check.py:213`: Target-only comparison `score >= threshold` → `score > threshold` | exit 1; `fail=2` | F; exit 1 | **killed** |
| M04 | `.ufo/evidence/round-31/dead-seat-check.py:216`: Named-target comparison `named_score >= threshold` → `named_score > threshold` | exit 0; `ok=17` | F; exit 1 | **survived** |
| M05 | `.ufo/evidence/round-31/dead-seat-check.py:101`: `return rest[:end.start()] if end else rest` → `return rest` | exit 0; `ok=17` | F; exit 1 | **survived** |
| M06 | `.ufo/evidence/round-31/dead-seat-check.py:121`: Explicit `item["target"]` → extracted prompt target | exit 1; `fail=7` | F; exit 1 | **killed** |
| M07 | `.ufo/evidence/round-31/dead-seat-check.py:257`: `return 1 if lines else 0` → `return 0` | exit 1; `fail=6` | F; exit 0 | **killed** |
| M08 | `.ufo/evidence/round-31/dead-seat-check.py:257`: `return 1 if lines else 0` → `return 1` | exit 1; `fail=3` | F; exit 1 | **killed** |
| M09 | `.ufo/evidence/round-31/dead-seat-check.py:250`: Caught bad input: `return 2` → `return 0` | exit 1; `fail=7` | F; exit 1 | **killed** |
| M10 | `.ufo/evidence/round-31/dead-seat-check.py:163`: `if not dead:` → `if dead is None:` | exit 1; `fail=1` | F; exit 1 | **killed** |
| M11 | `.ufo/evidence/round-31/dead-seat-check.py:175`: `if not items:` → `if items is None:` | exit 1; `fail=1` | F; exit 1 | **killed** |
| M12 | `.ufo/evidence/round-31/dead-seat-check.py:186`: `TOKEN.findall(target.lower())` → `TOKEN.findall(target)` | exit 0; `ok=17` | F; exit 1 | **survived** |

The real-case streams remained F for all mutants; only M07 changed the real-case exit status to 0. Thus the real fixture detected one of these defects independently; the selftest detected the other eight killed mutants as well as M07.

### Actual mutated selftest stderr

These are the complete captured stderr streams. The raw stream files and JSON receipts retain the same output without summarization.

#### M01 — exit 1

```text
SELFTEST FAIL name-reuse+target/stdout: stdout ['FLAG item=SeatCopy dead=seat_copy reason=target-similar jaccard=0.88'] != ['FLAG item=SeatCopy dead=seat_copy reason=name-reuse+target-similar jaccard=0.88']
DEAD_SEAT_CHECK_SELFTEST: fail=1
```

#### M02 — exit 1

```text
SELFTEST FAIL name-reuse+target/stdout: stdout ['FLAG item=SeatCopy dead=seat_copy reason=target-similar jaccard=0.88'] != ['FLAG item=SeatCopy dead=seat_copy reason=name-reuse+target-similar jaccard=0.88']
DEAD_SEAT_CHECK_SELFTEST: fail=1
```

#### M03 — exit 1

```text
SELFTEST FAIL boundary-inclusive: exit 0 != 1
SELFTEST FAIL boundary-inclusive/stdout: stdout [] != ['FLAG item=Elsewhere dead=Low reason=target-similar jaccard=0.60']
DEAD_SEAT_CHECK_SELFTEST: fail=2
```

#### M04 — exit 0

```text
DEAD_SEAT_CHECK_SELFTEST: ok=17
```

#### M05 — exit 0

```text
DEAD_SEAT_CHECK_SELFTEST: ok=17
```

#### M06 — exit 1

```text
SELFTEST FAIL name-reuse+target/stdout: stdout ['FLAG item=SeatCopy dead=seat_copy reason=name-reuse jaccard=-'] != ['FLAG item=SeatCopy dead=seat_copy reason=name-reuse+target-similar jaccard=0.88']
SELFTEST FAIL target-copy: exit 0 != 1
SELFTEST FAIL target-copy/stdout: stdout [] != ['FLAG item=SeatCopy dead=SeatA reason=target-similar jaccard=0.88']
SELFTEST FAIL boundary-inclusive: exit 0 != 1
SELFTEST FAIL boundary-inclusive/stdout: stdout [] != ['FLAG item=Elsewhere dead=Low reason=target-similar jaccard=0.60']
SELFTEST FAIL above-threshold: exit 0 != 1
SELFTEST FAIL above-threshold/stdout: stdout [] != ['FLAG item=Elsewhere dead=Low reason=target-similar jaccard=0.43']
DEAD_SEAT_CHECK_SELFTEST: fail=7
```

#### M07 — exit 1

```text
SELFTEST FAIL name-reuse+target: exit 0 != 1
SELFTEST FAIL target-copy: exit 0 != 1
SELFTEST FAIL boundary-inclusive: exit 0 != 1
SELFTEST FAIL above-threshold: exit 0 != 1
SELFTEST FAIL dead-from-spec: exit 0 != 1
SELFTEST FAIL dead-text=target: exit 0 != 1
DEAD_SEAT_CHECK_SELFTEST: fail=6
```

#### M08 — exit 1

```text
SELFTEST FAIL clean: exit 1 != 0
SELFTEST FAIL below-threshold: exit 1 != 0
SELFTEST FAIL dead-text: exit 1 != 0
DEAD_SEAT_CHECK_SELFTEST: fail=3
```

#### M09 — exit 1

```text
SELFTEST FAIL non-utf8: exit 0 != 2
SELFTEST FAIL space-in-name: exit 0 != 2
SELFTEST FAIL empty-items: exit 0 != 2
SELFTEST FAIL bad-json: exit 0 != 2
SELFTEST FAIL nameless-item: exit 0 != 2
SELFTEST FAIL empty-dead: exit 0 != 2
SELFTEST FAIL missing-file: exit 0 != 2
DEAD_SEAT_CHECK_SELFTEST: fail=7
```

#### M10 — exit 1

```text
SELFTEST FAIL empty-dead: exit 0 != 2
DEAD_SEAT_CHECK_SELFTEST: fail=1
```

#### M11 — exit 1

```text
SELFTEST FAIL empty-items: exit 0 != 2
DEAD_SEAT_CHECK_SELFTEST: fail=1
```

#### M12 — exit 0

```text
DEAD_SEAT_CHECK_SELFTEST: ok=17
```

## Surviving mutants are not equivalent behavior

These supplemental witnesses were also run on pristine, mutated, and restored bytes. They demonstrate the missed behavior but **do not reclassify the survivors in the required-detector table**. Each command ran in all three phases with the same cwd, environment, and timeout as above:

```sh
timeout 15s python3 .mutation-probe/M04.py --dead .mutation-probe/M04-dead.json --spec .mutation-probe/M04-spec.json
timeout 15s python3 .mutation-probe/M05.py --dead .mutation-probe/M05-dead.json --spec .mutation-probe/M05-spec.json
timeout 15s python3 .mutation-probe/M12.py --dead .mutation-probe/M12-dead.json --spec .mutation-probe/M12-spec.json
```

### M04

Both entries are named `Same`; dead target `alpha beta gamma`, new target `alpha beta gamma delta epsilon`. Their Jaccard is exactly 0.60. The existing boundary case uses different names, leaving the named-target branch at line 216 uncovered.

**pristine, exit 1**

stdout:

```text
FLAG item=Same dead=Same reason=name-reuse+target-similar jaccard=0.60
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=1 threshold=0.60
```

**mutated, exit 1**

stdout:

```text
FLAG item=Same dead=Same reason=name-reuse jaccard=0.60
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=1 threshold=0.60
```

**restored, exit 1**

stdout:

```text
FLAG item=Same dead=Same reason=name-reuse+target-similar jaccard=0.60
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=1 threshold=0.60
```

### M05

Different names and disjoint targets (`alpha beta` / `gamma delta`) share the same `# Acceptance` text (`shared words one two three four five six seven eight nine ten`). The contract excludes this section. The mutant includes it and emits a spurious 0.76 similarity. Existing selftest expectations are coupled to `target_of()` and therefore accept the defect.

**pristine, exit 0**

stdout:

```text
(empty)
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=0 threshold=0.60
```

**mutated, exit 1**

stdout:

```text
FLAG item=New dead=Old reason=target-similar jaccard=0.76
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=1 threshold=0.60
```

**restored, exit 0**

stdout:

```text
(empty)
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=0 threshold=0.60
```

### M12

Different names use explicit targets `Alpha Beta Gamma` / `alpha beta gamma`. Lowercasing makes them identical under the contract. The mutant loses the match. Existing hard-coded boundary fixtures are lowercase; the other expected similarities are computed through `tokens_of()` itself.

**pristine, exit 1**

stdout:

```text
FLAG item=New dead=Old reason=target-similar jaccard=1.00
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=1 threshold=0.60
```

**mutated, exit 0**

stdout:

```text
(empty)
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=0 threshold=0.60
```

**restored, exit 1**

stdout:

```text
FLAG item=New dead=Old reason=target-similar jaccard=1.00
```

stderr:

```text
DEAD_SEAT_CHECK: dead=1 items=1 flagged=1 threshold=0.60
```

## Hashes and restoration

SHA-256 of the original target before, during, and after the probe was unchanged:

```text
6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36
```

For each independent copy, the receipt records its hash immediately before and after the commands in that phase; those within-phase hashes were equal. The complete before/mutated/restored identities are:

| Mutant | Pristine SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| M01 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `933c491746a266a0018ad4b232e4b0261485404636e28533823bef2aaf271de3` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M02 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `5589eb46d3f6c9a7e1723e54eeee6de28d93e8bef5a9c11e70514dc2689a8eed` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M03 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `45f16cf494f5e1a111b568529d00e48334d189924f8f7e54f7b481093ae13fd8` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M04 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `2f4ba00548f4391dd005d8aba81a3a984e9da93994ccc901382100c67a0f8586` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M05 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `ba7b0dbd303e598903ba5ec604d4cc9dbcef9f02dd498e25a8544512a3180a7b` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M06 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `0311c306259cf1fe3a30eb7f353f5c799030c191d9313417538922cd1e98b7b0` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M07 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `de0ef28a07b98c90aeaf6f26fcc589b96dbfe4551754df9c8e53c656e4acd267` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M08 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `1b8dfc7ea96d79e0d2c4f939aed58c32ee524dc9389e869b6e9a265cbb9392a4` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M09 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `684e965fb3eb589f33416c95ae7dadae049be5741a1dabaa49778af42252422a` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M10 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `808288338db34268fd6ce4950e0dd5f7d94e448039ceb030c53950c6f061b884` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M11 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `dc0145b72c2f3a992ad51d86a1ab4138f482559b0a22f62e434767accc319148` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |
| M12 | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` | `7d2e7586f54566af4e1ed6ccd1b15f3aac104f4fdc0eadaac42a19e8ae821c93` | `6883c6f4e86c4b432aecf3a5b6f8b8de37cab5a34733e602a1c5dcc136713b36` |

Restoration used the captured pristine UTF-8 text for every copy. The restored byte hashes equal the initial hash, and all restored detector and supplemental outputs equal their pristine results. No production file was mutated.

### Preserved receipts

All artifacts are under `/fast/scratch/hyaku/tameshi-r31-seats/MutDeadSeatCheck/c/.mutation-probe/`:

- `manifest.json`: exact frozen line, before text, and after text for every single edit.
- `probe.py`: bounded behavioral driver used for all three phases.
- `receipts/pristine.json`, `receipts/mutated.json`, `receipts/restored.json`: exact child argv, cwd, stdout, stderr, exits, expected results, and before/after hashes.
- `receipts/<phase>/M<nn>-selftest.stdout`, `.stderr`, `M<nn>-real.stdout`, `.stderr`: full raw streams; the three diagnostic witnesses also have `-supplemental` streams.
- `M04-dead.json` / `M04-spec.json`, `M05-dead.json` / `M05-spec.json`, `M12-dead.json` / `M12-spec.json`: diagnostic fixtures.
- `summary.json`: required-detector verdicts and restoration identities. Every JSON seat field is exactly `MutDeadSeatCheck`.

Tool installations or updates: **none**.

# Smallest safe correction

Add three selftest cases without changing the stated contract or production logic:

1. Same normalized name and target Jaccard exactly 0.60; require the literal `name-reuse+target-similar` stdout and exit 1 (M04).
2. Disjoint `# Target` sections with identical long `# Acceptance` sections; require empty stdout and exit 0 (M05).
3. Differently cased but otherwise identical explicit targets under distinct names; require a literal `target-similar jaccard=1.00` flag and exit 1 (M12).

Keep these expected strings and outcomes independent of `target_of()`, `tokens_of()`, and `score()` so a mutated helper cannot rewrite its own oracle. These corrections are recommendations only; no source or selftest changes were applied.
