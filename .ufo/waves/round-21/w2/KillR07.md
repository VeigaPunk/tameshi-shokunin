done — **R07 genuinely discriminated / KILLED**. The frozen probe returned 0 with pristine control green, anchor_count=1, and exactly the intended failing case. An additional same-detector pristine → mutated → exact-byte-restored run reproduced exits 0 → 1 → 0.

# R07 — post-pidfd ownership revalidation

- Axes: **operability** (the behavioral guard catches its assigned regression) and **calibration** (synthetic ownership-race coverage is not real PID-reuse evidence).
- Tested revision: `790abd2129f153c13b471e381d454186edbde65e`.
- Owning surface: `tools/registry-check.py`.
- Author-side advisory evidence only; no judgment, admission, integration, expertise score change, or production fix is claimed.

## Frozen command and actual result

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only R07 --jobs 1 --json
```

Invoked with inherited `GIT_*` variables removed. Exit **0**. Complete, unmodified JSON stdout: `.ufo/waves/round-21/w2/mutations/R07.json`.

Actual stderr:

```text
C1 R07 tools/registry-check.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

| Frozen observation | Actual output |
| --- | --- |
| Anchor occurrences | `1` |
| Pristine | exit `0`; `SELFTEST: PASS (51 cases)`; no fail lines; 8.441 s |
| Mutant | exit `1`; `SELFTEST: FAIL (1 of 51 cases: pidfd-revalidates-ownership)`; 8.522 s |
| Counts | killed `1`, survived `0`, inconclusive `0`, total `1` |
| Detector stderr | empty for both runs; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Exact mutant failure:

```text
SELFTEST_CASE pidfd-revalidates-ownership FAIL (ownership_change_rejected=False signals=1)
SELFTEST: FAIL (1 of 51 cases: pidfd-revalidates-ownership)
```

## Mutant and expected discriminator

Frozen definition: `.ufo/evidence/round-21/c1-mutants.json:104-107` (spec SHA-256 below). The exact old/new pair changes only the post-open condition at `tools/registry-check.py:516-517` in the tested revision:

```python
# old
        stat = read_stat(pid)
        if stat is None or stat[1] != starttime or not in_row_scope():
# new
        stat = read_stat(pid)
        if stat is None or stat[1] != starttime:
```

The initial ownership check at lines 508-510 is unchanged. `os.pidfd_open` happens at line 512; the removed second ownership check occurs before `signal.pidfd_send_signal` at line 519. The live caller constructs an ancestry/ownership predicate at lines 527-538; ownership resolution is at lines 468-489. Thus this is a behavior-bearing loss of the second scope check, not removal of the start-time check.

Expected detector: `pidfd-revalidates-ownership`, lines **1608-1620**. It must reject a process whose scope predicate changes from true to false between the two checks and must not call the signal operation. Actual fixture construction:

- `ownership = iter((True, False))` (1608).
- `os.pidfd_open` returns synthetic descriptor `999999`; `os.close` and `signal.pidfd_send_signal` are patched (1609-1611).
- The helper is called for synthetic PID `987654`, start time `1234`, `SIGKILL`, with a controlled ownership callback and constant synthetic stat tuple (1595, 1612-1615).
- The predicate under test is `scope_rejected and not sent.called` (1616-1619).

Pristine returns rejection with zero mocked signal calls. The mutant omits the second ownership callback, returns success, and makes one mocked signal call. This directly discriminates the removed behavior. The detector does not hash/grep source to choose its case verdict. Receipt hashes establish artifact identity only. Case recording at 919-926 and final failure aggregation at 1809-1814 turn this failed behavioral predicate into exit 1. All other 50 cases pass: this is not syntax/import/setup failure or an unrelated assertion.

All owning-tool source lines above refer to `tools/registry-check.py@790abd2129f153c13b471e381d454186edbde65e`; the pinned Git blob and inspected production bytes share the pristine SHA-256 below.

## Same-detector restoration control

To fulfill the three-phase mutation protocol, I also materialized a separate private clone at the tested revision in `/tmp/tameshi-r21-KillR07-_3vc_0b8/fleet/tameshi-shokunin`. Read-only sandbox access to sibling symlinks, fresh home/tmp, and the **unchanged frozen ruler's `selftest` function** were used. No other mutant or detector was run.

Actual setup commands (both exit 0; stdout/stderr empty):

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-KillR07-_3vc_0b8/fleet/tameshi-shokunin
git -C /tmp/tameshi-r21-KillR07-_3vc_0b8/fleet/tameshi-shokunin checkout -q --detach 790abd2129f153c13b471e381d454186edbde65e
```

Original bytes were obtained with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 790abd2129f153c13b471e381d454186edbde65e:tools/registry-check.py` (exit 0). Clone/source Git commands scrubbed inherited `GIT_*` and pinned `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. The scratch mutation was a one-line edit at 517, matching the frozen mutated SHA exactly. Exact original bytes were restored in a `finally` block before the third run.

Complete phase argv, raw stdout/stderr, summaries, source hashes, setup and hash command exits, and cleanup evidence are in `.ufo/waves/round-21/w2/mutations/R07-restoration.json`.

| Phase | Exit | Ownership case | Summary |
| --- | --- | --- | --- |
| Pristine | 0 | `PASS (ownership_change_rejected=True signals=0)` | `SELFTEST: PASS (51 cases)` |
| Mutated | 1 | `FAIL (ownership_change_rejected=False signals=1)` | `SELFTEST: FAIL (1 of 51 cases: pidfd-revalidates-ownership)` |
| Restored | 0 | `PASS (ownership_change_rejected=True signals=0)` | `SELFTEST: PASS (51 cases)` |

All three phase stderr streams were empty; no timeouts or probe errors occurred. `pidfd-revalidates-starttime` and `baseline-child-preserved` passed in all three phases. No byte-identical stdout claim is made; each raw output and its distinct hash is retained.

SHA-256 restoration evidence:

```text
pristine/pinned blob cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e
mutated             e3b2b671c56f12ff2ad1806d74bab7ddb0010f5ad00c1b18c52d96ec865ed3a3
restored            cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e
production after    cc4ed8e215f01a7ef3693f2f98b2973ad401047b473efb1e7b1fbea92a5d451e
frozen ruler        a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396
frozen mutant spec  670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c
```

Actual `sha256sum` commands (both exit 0, stderr empty):

```sh
sha256sum /tmp/tameshi-r21-KillR07-_3vc_0b8/fleet/tameshi-shokunin/tools/registry-check.py
sha256sum /tmp/tameshi-r21-KillR07-_3vc_0b8/fleet/tameshi-shokunin/tools/registry-check.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py
```

The first measured mutant bytes; the second measured restored scratch and untouched production bytes. After the restored detector completed, the owned scratch was removed (`scratch_removed: true`). The frozen ruler independently removes its own mutant clone and scratch at `c1-survivors.py:131,139-140`.

## Calibration, agreements, and boundaries

- **Agree:** the frozen `KILLED` result is a genuine intended-discriminator kill, not an incidental failure or an equivalent mutant. The restoration control ties the sole failure to the exact assigned edit.
- **Limit:** this is a deterministic **synthetic ownership-race control**. No real PID recycling, kernel scheduling race, or signal delivery to the synthetic PID was reproduced. The patched signal call count is the observation. The separate start-time race control at 1567-1589 is also synthetic and remains green under R07; it is not proof of real PID reuse. The source itself retains a same-tick PID-reuse residual at lines 39-44.
- **Environment/hook boundary:** the observed detector argv uses `bwrap`, network unsharing, a read-only host root, a writable private scratch bind, and `env -i` with PATH/HOME/TMPDIR/Git configuration/locale pins (`c1-survivors.py:38-45`). This establishes the constructed invocation contract, not malicious-hook execution. R07 did not attempt a hook attack. Owning selftest Git fixture pinning is defined at `registry-check.py:149-166`.
- **Disagreements:** none with the narrow R07 kill claim. No broader all-mutant tally, real-PID-reuse safety claim, admission, or numerical expertise increase follows from this single probe.
- Production tools/contracts/ledgers/corpus/index/refs and sibling sources were not edited. Writes were confined to the assigned report/evidence names and the owned scratch; no installs or updates were performed.

Report: `.ufo/waves/round-21/w2/KillR07.md`
