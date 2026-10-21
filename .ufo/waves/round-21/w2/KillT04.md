done — genuinely discriminated. Frozen C1 mutant T04 is KILLED at `790abd2129f153c13b471e381d454186edbde65e`; the intended `pycache-prefix-private` behavioral case alone fails. Pristine and exact-restored controls are green.

# KillT04 — single-mutant falsification

## Axes and scope

- **Operability:** execute the frozen T04 detector against its exact owning tool and verify pristine/mutated/restored behavior in isolated scratch.
- **Calibration:** distinguish the intended runtime cache-isolation discriminator from incidental setup failures or source matching; do not infer security outcomes that were not exercised.
- Owning surface: `tools/trace-inputs.py`, measured revision `790abd2129f153c13b471e381d454186edbde65e`.
- This dispatched seat supplies author-side advisory evidence only. No overall round judgment, admission, integration, numeric expertise increase, or production fix is claimed.

## Mutant and expected detector

Frozen definition: `.ufo/evidence/round-21/c1-mutants.json:109-114`; selftest argv: lines 132-134.

```diff
-    cache = os.path.join(workdir, "pycache")
+    cache = os.path.join(tempfile.gettempdir(), "pycache")
```

The sole mutation is `tools/trace-inputs.py:514`. It redirects `PYTHONPYCACHEPREFIX` from the private per-trace workdir to a shared temporary-directory child. The old anchor occurs **exactly once**, as recorded by both the frozen receipt and the supplemental restoration receipt.

Expected detector: public `tools/trace-inputs.py --selftest`, case **`pycache-prefix-private`** at lines **928-934**. Lines **932-933** require the cache's immediate parent to be a `trace-inputs-run-*` directory directly below the fixture's scratch directory. `git blame -L 927,934 790abd2129f153c13b471e381d454186edbde65e -- tools/trace-inputs.py` exited 0 and attributes those two strengthened assertions to **`370f2df`**; the surrounding older check is attributed to `58e5d53`.

All tool source line references below are to the full measured revision above. A `git show 790abd2129f153c13b471e381d454186edbde65e:tools/trace-inputs.py` exited 0; its SHA-256 exactly matched the tool digest emitted by the frozen detector.

## Exact requested command and actual output

```text
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 790abd2129f153c13b471e381d454186edbde65e --only T04 --jobs 1 --json
```

**Exit: 0.** The invoking environment had inherited `GIT_*` variables removed. The command's full, unmodified JSON stdout is saved at `.ufo/waves/round-21/w2/mutations/T04.json`.

Actual complete command stderr, also saved at `.ufo/waves/round-21/w2/mutations/T04.stderr`:

```text
C1 T04 tools/trace-inputs.py KILLED
C1: killed=1 survived=0 inconclusive=0 total=1 rev=790abd2129f153c13b471e381d454186edbde65e
```

| Frozen measurement | Exit | Summary | Failure lines |
|---|---:|---|---|
| Pristine control | 0 | `SELFTEST: 30/30` | none |
| T04 mutant | 1 | `SELFTEST: 29/30` | `FAIL pycache-prefix-private` |

Frozen result: total 1, killed 1, survived 0, inconclusive 0, anchor_count 1; neither selftest timed out. The frozen instrument creates and deletes its own private clones (`c1-survivors.py:93-140`); it never edits the production lane.

Instrument provenance:

- Ruler SHA-256: `a0ec554735b13efa82b5c37534d8beb541204c0f9443d97a040cdd4e248e9396`.
- Frozen spec SHA-256: `670dd59b9b3d99ec24a6b87aedea531640d4167bb40b2c863066682cf6b3e85c`.
- Exact JSON stdout SHA-256: `3ba22f11cb740b2b7510c0637ff97d77aa0ec3d5b5e43cc9b3b18637f76f99ed`.
- Command stderr SHA-256: `be97ec239568553f2edc670c8b60748f2083494587b408119ef6c33e2002cdf4`.

## Why this is the intended discriminator

1. **Behavior-bearing mutation:** `scrubbed_env(workdir)` constructs the child environment at lines 509-517; `run_trace` obtains its private workdir at lines 612-617 and passes the resulting environment to an actual `strace` subprocess at lines 629-633. The payload records the chosen prefix at lines 674-679.
2. **Public CLI and actual child observation:** the fixture helper invokes the tool as a subprocess, pins `TMPDIR` to its scratch directory, and reads emitted JSON at lines 779-805. At lines 919-920 it runs an actual traced `bash -c env` and parses the captured child stdout. The failing case compares that runtime environment value with the emitted JSON and checks its directory placement at lines 927-934. This is not a source hash, source grep, or a mocked return value.
3. **Only the named isolation check fails:** complete mutant stdout contains 29 PASS lines and exactly `FAIL pycache-prefix-private`. In particular, `env-scrubbed`, `double-import-keeps-py`, `temp-workdirs-deleted`, and `no-artifacts-inside-root` all still pass. Both frozen and supplemental mutant runs reach `SELFTEST: 29/30` and exit 1. There is no syntax/import failure masquerading as a kill.
4. **Source-derived explanation, not a separately instrumented predicate trace:** [INFERENCE] with the helper's `TMPDIR=scratch`, the mutated prefix is `scratch/pycache` rather than `scratch/trace-inputs-run-*/pycache`; it violates the two assertions strengthened at lines 932-933. The run records the combined named assertion's failure, not individual boolean values. The mutation can still be absolute, outside the input root, and consistently reported, which explains why the older portions of the check are insufficient.
5. **Calibration boundary:** this measures runtime prefix isolation. `PYTHONDONTWRITEBYTECODE=1` remains set; this probe does not demonstrate a real cache collision, poisoned-bytecode execution, or an actual cache-file leak. It is not a witness Git hook/env-pin test, and no malicious hook was executed or claimed. It is not a registry-identity test; neither synthetic PID-race control nor real PID reuse was exercised.

The selftest helper suppresses nested stderr (`trace-inputs.py:798-800`), so empty outer stderr is not used alone as proof of fixture health. The preceding `env-scrubbed` case observes the same invocation's successful return and payload, and the full 30-case output confines the failure to cache-prefix privacy.

## Same detector on pristine, mutated, and exact-restored bytes

Supplemental scratch: `/tmp/tameshi-r21-KillT04-okzek963`. It contained a private clone checked out at the measured revision, with sibling symlinks beside it. The detector's `bwrap --ro-bind / /` made the symlink targets read-only; only this unique scratch root was rebound writable.

The frozen module's **unmodified `selftest()`** was invoked three times using the same arguments:

```text
c1.selftest(scratch_root, clone_path, "tools/trace-inputs.py", ["--selftest"])
```

Its `run()` wrapper only retained the existing subprocess result and argv for evidence; it did not change arguments, environment, exits, or output. Each expanded command was:

```text
bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind /tmp/tameshi-r21-KillT04-okzek963 /tmp/tameshi-r21-KillT04-okzek963 --unshare-net --die-with-parent --chdir /tmp/tameshi-r21-KillT04-okzek963/fleet/tameshi-shokunin env -i PATH=<invoking PATH, recorded verbatim in restoration JSON> HOME=/tmp/tameshi-r21-KillT04-okzek963/home TMPDIR=/tmp/tameshi-r21-KillT04-okzek963/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C python3 /tmp/tameshi-r21-KillT04-okzek963/fleet/tameshi-shokunin/tools/trace-inputs.py --selftest
```

The timeout was the frozen detector's 900 seconds (`c1-survivors.py:23,38-57`). The subprocess environment contained no inherited `GIT_*`; fixture Git configuration was pinned by the envelope above and `trace-inputs.py:744-758`.

| Bytes tested | Exit | Summary | Failing case | Timeout |
|---|---:|---|---|---|
| Pristine | 0 | `SELFTEST: 30/30` | none | false |
| T04 single-line mutation | 1 | `SELFTEST: 29/30` | `pycache-prefix-private` | false |
| Exact restored bytes | 0 | `SELFTEST: 30/30` | none | false |

Source SHA-256 evidence:

| State | SHA-256 |
|---|---|
| Before mutation / pinned Git blob | `f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4` |
| Mutated | `62c05b26e5761bc5f569cfd45c501a9f69872eea83cdb78925b467d084f32df8` |
| Restored | `f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4` |

The supplemental mutated digest exactly matches the frozen receipt. Exact byte equality with the pinned pre-mutation blob was **true** before the restored detector ran. Pristine and restored stdout hashes are both `fadbe2c9cb385eb4da8304cc8d1d7b6368bfdde82ee8a920696d23294feffda1`; mutant stdout is `c5b36ec7c40856f296cdbdbf548f4cb2f2231a89b4171fb14fa7cebc5c10f179`. All three selftest stderr streams are empty (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). These also match the corresponding frozen control/mutant hashes.

Full expanded argv, actual stdout/stderr, exits, hashes, and restoration equality are saved in `.ufo/waves/round-21/w2/mutations/T04.restoration.json`. Complete raw phase output is also saved under `mutations/T04.{pristine,mutated,restored}.{stdout,stderr}` in this report directory.

The restored private scratch was subsequently removed successfully; `.ufo/waves/round-21/w2/mutations/T04.cleanup.json` records `restored_before_removal: true` and `removed: true`. No production source, contracts, index, refs, corpus, routing, or sibling files were edited.

## Preserved non-detector observation

The first supplemental capture cell exited 1 **after** its pristine detector had already completed with exit 0 and `SELFTEST: 30/30`: an output-saving expression combined `PosixPath` and `str`, raising `TypeError: unsupported operand type(s) for +: 'PosixPath' and 'str'`. Only the failed output-path construction was corrected; the already-captured pristine bytes were saved without rerunning or relabeling that failure. This harness observation is retained in `T04.restoration.json` and is unrelated to the mutant's assertion failure.

## Agreement and limits

- **Agree:** the frozen T04 result is a genuine behavioral discrimination of the declared private-cache-prefix defect at the landed revision, not an incidental failure. Both controls are green and the single anchor is present once.
- **Disagreements:** none for this one-mutant claim. No conclusion about the other 17 C1 mutants, C2/F5, the broader calibration ledger, or overall round admission is made.
- **Installs/updates:** none. No full battery, build, lint, formatter, alternative runtime, or out-of-item probe was invoked.

Report: .ufo/waves/round-21/w2/KillT04.md
