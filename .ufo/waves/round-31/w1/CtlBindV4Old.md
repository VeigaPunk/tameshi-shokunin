# CtlBindV4Old — historical controls rejected by frozen v4

**Verdict: all seven assigned historical input mutants were killed (rejected); all five supplied controls were rejected.** Each measured v4 result was **0/32 kept, exit 1**. No forged shape in this assigned set survived. Every mutation store was restored byte for byte and scored again. No mutation probe was inconclusive under its expected negative-control outcome.

Assigned axis: **calibration**. Probe axes: false retention resistance, reproducibility, and exact restoration. This is a replay of historical negative controls, not a judgment of C1 or a claim that every v4 condition is independently covered.

## Evidence and commands

Paths below:

- `P=/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- `S=/fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old`
- `L=$S/lane`

### Isolation and frozen inputs

Observed `df -h /fast`: 804G total, 626G used, 178G available, 78% used. The following command ran from `S`:

```sh
timeout --signal=TERM --kill-after=5s 120s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -c core.hooksPath=/dev/null clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/lane && timeout --signal=TERM --kill-after=5s 60s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/lane -c core.hooksPath=/dev/null checkout --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Observed output:

```text
Cloning into '/fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/lane'...
done.
HEAD is now at c111dab round-31: freeze C1 counter, binding v4, contract, base receipts
```

The frozen docstring was read at `L/.ufo/evidence/round-31/coldread/bind-select-v4.py:2-47`. Its added requirements are at lines 7-19: an appropriate bash invocation, a unique call ID, a later non-error result, and matching trace receipt revision and argv.

The retained round-30 harness was copied, not edited, from the explicitly authorized read-only source:

```sh
cp /fast/scratch/hyaku/tameshi-r30a3-seats/CtlBindV3/probe-bind-v3.py /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v3.py && sha256sum /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v3.py /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v4-old.py
```

Observed SHA-256 values:

```text
a3ab565a9e374e6d6b61ce54be0b9a15fc48232833db6370513cc896b9773225  /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v3.py
59556d3cb1de140a7c330a561bd6c4409be31d52f41b2d4364048ecdea33f54e  /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v4-old.py
```

The new driver rebinds only the copied harness's detector path to frozen v4 (`S/probe-bind-v4-old.py:14-18`). It retains the original assembly `.ufo/evidence/round-29/coldread/assembled-w1.json`, registry `.ufo/waves/round-29/w1/swarm-registry.json`, prefix `TameshiR29.`, synthetic session IDs, and seven mutation builders. The deliberately missing script path naturally relocates into this seat's scratch directory. No v3 detector was rerun; its results below come from the historical report.

Both driver phases recorded identical before/after hashes for the five fingerprinted files (`S/results-shapes.json:11-25`; `S/results-controls.json:11-25`):

| File relative to `L` | Before = after SHA-256 |
|---|---|
| `.ufo/evidence/round-31/coldread/bind-select-v4.py` | `dd8bb39309cb337b4b0e6703657198fc88655ce4b498de2ad3f637e04030b87f` |
| `.ufo/evidence/round-29/coldread/assembled-w1.json` | `0ef402815708ca2233e6c52f36674345e8d98cc63c1ff2a2da4fef2213ad2731` |
| `.ufo/waves/round-29/w1/swarm-registry.json` | `08bae801bb4c35d34fbe3c95b5af5c4724574e35221d3ecb2a932e7c81ebf4b0` |
| `.ufo/evidence/round-30/attempt3/make-bind-controls.py` | `8780a8cd7c2f89ad576251cf8c03335829f85e201c556770b20856868942a6ab` |
| `.ufo/evidence/round-30/attempt3/bind-controls.txt` | `c70e796cf1ae7b47e22b332c371638a7309785d7d72623252b448e7feef60e1c` |

The unchanged assembly retains absolute paths to historical production trace receipts (`L/.ufo/evidence/round-29/coldread/assembled-w1.json:30-33`). V4 can read these paths; they were not rewritten or mutated. Thus this replay preserves the requested original assembly rather than claiming a fully hermetic receipt copy.

### Rebuilding and scoring

The following two bounded commands ran concurrently from `L`; each shape retained its own pristine → mutated → restored ordering:

```sh
timeout --signal=TERM --kill-after=5s 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 python3 .ufo/evidence/round-30/attempt3/make-bind-controls.py /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/controls && timeout --signal=TERM --kill-after=5s 90s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v4-old.py --phase controls
```

```sh
timeout --signal=TERM --kill-after=5s 90s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/probe-bind-v4-old.py --phase shapes
```

Both completed and printed `frozen_inputs_unchanged=true`. The controls phase also printed `control_bytes_unchanged=true`. Each shape line printed `verdict: killed`, pristine `[0, 1]`, restored `[0, 1]`, and `restored_exact: true`.

This is the exact mutated detector command for `different_tool`, recorded at `S/shapes/different_tool/result.json:20`:

```sh
timeout --signal=TERM --kill-after=2s 20s /usr/bin/python3 /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/lane/.ufo/evidence/round-31/coldread/bind-select-v4.py --repo /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/lane --assembled .ufo/evidence/round-29/coldread/assembled-w1.json --registry .ufo/waves/round-29/w1/swarm-registry.json --sessions /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/shapes/different_tool/sessions --prefix TameshiR29. --out /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/shapes/different_tool/mutated.assembled.json --receipt /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/shapes/different_tool/mutated.receipt.json
```

Every detector invocation, including pristine and restored phases and static controls, printed exactly:

```text
{"assembled": 32, "kept": 0, "excluded": 32}
```

Every detector exited **1**, with empty stderr. These are successful rejections against the expected negative-control outcome, not baseline execution failures. Exact expanded invocations and outputs are retained in `S/shapes/<shape>/{pristine,mutated,restored}.run.json` and `S/scores/controls/<control>.run.json`. For example: `S/shapes/different_tool/result.json:7-42` and `S/scores/controls/forged.run.json:2-11`. Static-control aggregate evidence is `S/results-controls.json:410-490`.

## Requested comparison

V3 source: `P/.ufo/waves/round-30/wC/CtlBindV3.md:55-61,77-85`, corroborated for supplied controls by `P/.ufo/evidence/round-30/attempt3/bind-controls.txt:6-14`. V4 figures are the observed replay above. All denominators are the unchanged pilot's 32 assembled entries.

| Shape or supplied control | Kept/N under v3 | Kept/N under v4 | V4 exit | Verdict |
|---|---:|---:|---:|---|
| `different_tool`: trace names in a read tool's intent | 31/32 | 0/32 | 1 | killed |
| `different_result_id`: call x1, result x2 | 0/32 | 0/32 | 1 | killed |
| `user_authored_call`: trace call in user message | 0/32 | 0/32 | 1 | killed |
| `error_result`: missing script, isError true, exit 2 | 31/32 | 0/32 | 1 | killed |
| `comment_only_shell`: trace names only in shell comment | 31/32 | 0/32 | 1 | killed |
| `result_before_call`: result before alleged call | 31/32 | 0/32 | 1 | killed |
| `reused_call_id`: read result borrowed by unresulted bash call | 31/32 | 0/32 | 1 | killed |
| Supplied `promptonly` | 0/32 | 0/32 | 1 | rejected |
| Supplied `donothing` | 0/32 | 0/32 | 1 | rejected |
| Supplied `textmention` | 0/32 | 0/32 | 1 | rejected |
| Supplied `noresult` | 0/32 | 0/32 | 1 | rejected |
| Supplied `forged`: echo-shaped call plus matching result | 30/32 | 0/32 | 1 | rejected |

The copied harness's `reference_match` field compares current results to historical v3, not to expected v4. Its `false` for supplied `forged` (`S/results-controls.json:487-490`) correctly records the change from 30/32 to 0/32; it is not a replay failure.

For `different_tool`, the first excluded entry names `Read01A` and records `trace-without-executed-bash-call:Read01A:Read01A-1.json,Read01A-2.json,Read01A-3.json` (`S/shapes/different_tool/mutated.receipt.json:11-23`). No kept entry exists in any assigned forged store, so there are no surviving transcript lines to exhibit. Exact mutated Read01A transcript lines remain in `S/shapes/<shape>/Read01A.mutated-lines.json`; generated controls remain in `S/controls/<control>/TameshiR29.Read01A.jsonl`.

### Expected detector and calibration executions

Each shape's pristine store is the original synthetic assistant trace-shaped call **without a result**, followed by its assistant COLDREAD line. Expected behavior is **0 kept, exit 1**, for pristine, mutated no-execution input, and restoration. All seven pristine and restored runs met this expectation. The supplied controls were rebuilt and scored as static negative stores; they were not presented as additional mutation/restoration sequences.

The reused harness also reproduced the two real bounded calibration executions. Missing-script invocation (`S/shapes/missing-script.run.json:2-7`):

```sh
timeout --signal=TERM --kill-after=1s 5s /usr/bin/python3 /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/missing/trace-inputs.py
```

Observed exit **2**, empty stdout, stderr:

```text
/usr/bin/python3: can't open file '/fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4Old/missing/trace-inputs.py': [Errno 2] No such file or directory
```

Harmless shell comment, Read01A example (`S/shapes/comment_only_shell/actual-noop-runs.json:2-8`):

```sh
timeout --signal=TERM --kill-after=1s 5s bash -c ': # trace-inputs.py Read01A-1.json Read01A-2.json Read01A-3.json'
```

Observed exit **0**, stdout and stderr empty. All 36 recorded no-op runs had these results. Neither calibration execution runs an existing trace script. The other transcript tool calls are explicitly synthetic and were never executed.

## Restoration evidence

For every shape, all **36** session files were restored from saved pristine bytes in the copied harness's `finally` block (`S/probe-bind-v3.py:192-215`). Its per-shape `result.json:43-54` records `error: null`, `restored_exact: true`, and before/mutated/restored hashes. Each directory also contains the full per-file maps `before-hashes.json`, `mutated-hashes.json`, and `restored-hashes.json`.

The common before **and** restored manifest SHA-256 for all seven shapes is:

```text
a2f48a62a4493e8bff0410ea07d306531340080b20f97992ba49ed0046253aa9
```

The manifest digest hashes the sorted compact JSON map of session filename to byte SHA-256 (`S/probe-bind-v3.py:103-108`). Mutated manifest digests:

| Shape | Mutated manifest SHA-256 |
|---|---|
| `different_tool` | `ff33b8d27777d1357c42c0d3f41cfb5fe28a3b8ac3663e37fd8aee488b0ed6a5` |
| `different_result_id` | `6e03b3aaaa8990837dbf77d20ba8d8760decdd4da52895175c418d3929014b92` |
| `user_authored_call` | `4494e48a4db8db34104349fce2eb6ec9f2b35562092f47e16cdd1076586fc53c` |
| `error_result` | `1319039ee5f1666b4f0f9da2b6011a29741b6d7f31109c0d2ee244bb1494d6d9` |
| `comment_only_shell` | `9124192ba2a41c102361cfc72beea8b047c3c9e1c40b52aa792fab4dff9abb87` |
| `result_before_call` | `c63275cc99be13dec72acac3116139d2652f01cfc65801e4b217ffa830f84c5e` |
| `reused_call_id` | `29f0059063da5f5d543cd5747c27bc425a561779a39d0355d2d21683e30ce9b9` |

For the Read01A sample, every before/restored SHA-256 is `e68ca55ea47542fb47cf21fa6349609ebf253542ba22193d88757de5eb2aba6e`. The different-tool mutant is `7ca9cfd70f47571b6b4007aed888cb9d0e63d7b88eeadc14a078c0c8eef44ec3` (`S/shapes/different_tool/result.json:47-54`). The relocated missing-script mutant is `89bc192f2440e16bd317eb28c3cb6d98fbdc8cc4476e063256deaaadc86b0071` (`S/shapes/error_result/result.json:47-54`).

All five static control stores remained byte-identical across scoring; full before/after per-file maps are in `S/results-controls.json:26-409`, with the equality result at line 410.

All launched commands were finite and completed; subprocesses were waited for. No background process was left running and no other seat's process was killed. Writes were confined to this seat's scratch tree and this report. The authorized prior harness was only read. No production source, index, sibling scratch tree, contract, counter, or frozen selector was edited. No subagent, alternate orchestration runtime, model, or `jj` command was invoked. No tools were installed or upgraded. Observed versions: Python **3.14.8**, Git **2.56.0**.

## Calibration limit and smallest safe correction

No correction to frozen v4 is indicated by these historical inputs. Preserve the freeze and record the narrower result: **v4 rejects this exact historical set**.

Do not turn the matrix into independent proof of each new v4 condition or universal resistance to forged transcripts. The retained builders intentionally use the old trace-shaped command with one `--out` followed by multiple names and no traced `--` argv (`S/probe-bind-v3.py:87-90`). For example, the unchanged first pilot receipt contains a nonempty recorded argv (`P/.ufo/evidence/round-29/coldread/traces/Read01A-1.json:3-12`), while that synthetic command yields an empty traced argv under v4. Rejection can therefore have multiple sufficient causes. This assigned replay did not construct a passing v4 positive fixture or isolate each check; the expected negative baseline still succeeded, and the full input-level rejections and restorations above are observed.
