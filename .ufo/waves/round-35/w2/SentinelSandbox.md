# Tameshi round 35 W2 — SentinelSandbox

## Axes attacked

- **Confinement:** do root values and the Bash block stay inside `--work` / assigned scratch?
- **Path resolution:** absolute roots, working directory, and symlinks.
- **Untrusted code and side effects:** can a specimen alter the cleanup operand or perform unobserved filesystem mutations?
- **Process and secret boundaries:** what identity, environment, and cleanup the subprocess receives.

## Pin and scope

The requested `lane` directory already existed; its HEAD was `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`. The prescribed clone to that occupied path failed with exit 128 (`fatal: destination path .../lane already exists and is not an empty directory`). I left it untouched and cloned/check-out the requested pin into the new scratch path `/fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/pinned/`.

`git -C /fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/pinned rev-parse HEAD` → `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (exit 0); checkout status was `## HEAD (no branch)`. `sha256sum` (exit 0) confirmed the pinned bytes:

- `.ufo/evidence/round-35/c1/c1-measure.py`: `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`
- `tools/tally-audit-v3.py`: `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`
- `tools/mutate-and-run.sh`: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`

No frozen artifact or checkout was edited. No tool was installed. The full C1 deciding counter was not run.

## CRITICAL — specimen shell can delete outside `--work`

**Finding.** The counter does not sandbox the extracted tally block. A fixture is parsed as JSON, its edits are applied to runner source, then the resulting block is embedded verbatim in a Bash function and executed with the counter's OS permissions. The candidate block can overwrite its local `root`, change directory, or run arbitrary shell commands. The pass branch runs `rm -rf "$root"` for `(auto,KEEP)=(1,0)`. There is no path containment check or filesystem namespace.

**Source evidence.** In the pinned counter, `CONFIGS` and `auto_root()` are at `c1-measure.py:48-75`; `run_block()` interpolates the config into a Bash script, writes it under `tmp`, sets `cwd=tmp`, and runs `bash` at `:163-177`. Its child environment is only `PATH` (inherited), `LC_ALL`, `HOME=tmp`, and `TMPDIR=tmp`; it does not drop privileges or restrict filesystem access. The counter loads committed fixture records and applies their text edits at `:248-263,285-303`. The runner's cleanup is `mutate-and-run.sh:1462-1470`; C1 compares only `(exit, FULL stdout)` at `c1-measure.py:179-186,204-217,296-310`, so filesystem side effects are not part of its behavior tuple.

**Contained reproduction.** Exact command: `python3 /fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/proof_probe.py` → exit 0; probe SHA-256 `6d2d535e95fdeadf21dc5e6cbdc71d09eabf5e3e537d962b68333fe51b5204f4`. It used the pinned counter's `apply_edits`, `tally_block`, and `run_block`, the real `CONFIGS[0] == (None,'1','0')`, and one all-zero 9-status vector. To keep all effects inside the assigned scratch area, the probe pre-seeded `AUTO_ROOT[0]` to a freshly created scratch-local directory; it did not create the counter's real `/tmp` root.

1. **Absolute operand:** inserted `root=<fresh scratch sibling victim>` immediately before the reference `rm -rf "$root"`. The child command was `bash /fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/contained-absolute-root-1tey0wb6/work/b1.sh`, `cwd=/fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/contained-absolute-root-1tey0wb6/work`, exit 0. `run_block` returned `(0, "REGRESSION: PASS ...")`; both victim directory and sentinel were gone. Driver SHA-256 `70818d94b6a71ee434fe4ba29e2e5120c24aacee89e4a69f4ea2d25746e6ee26`; mutated runner copy SHA-256 `7d6592a13e11eb70dd6ee0e551d95407ac352e8f7b1044f17154da803acfe595`.
2. **Relative operand through a symlinked cwd:** used `--work`-equivalent path `.../work-link` symlinked to `.../physical-work`, inserted `root=../victim` before the same cleanup. `pwd -P` inside the block printed `.../physical-work`; the child command was `bash /fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/contained-symlink-relative-root-m48j3dtu/work-link/b1.sh`, with `cwd` argument `.../work-link`, exit 0. The sibling victim and sentinel were gone. Driver SHA-256 `98951f3deda177dbf87a1fd3ad6f35a44f4e0fe7c6ab385475084d78f4361f80`; mutated runner copy SHA-256 `5f0cbdfe06a410778a36b283adf04bb5c1db0ee8b4197812853be838f4b8539c`.

In both probes the shell printed a PASS tuple. The inserted `root=` was after the `REGRESSION_WORKDIR` print, so that print still named the original scratch-local root while the following `rm` deleted the victim. The `rm` stderr is redirected away by `run_block`'s `2>/dev/null`. These controlled probes prove deletion outside the *work directory*, but not outside the overall assigned scratch tree; I did not target any host path.

**Actual config root inventory and deletion paths.** `c1-measure.py:52-75` defines:

| Config | Value used as `root` | Reference block cleanup |
|---|---|---|
| `(None,'1','0')` | Absolute `/tmp/tameshi-r4-2-regression.<random>` from `tempfile.mkdtemp(..., dir='/tmp')` | On PASS, `rm -rf "$root"`; C1 also registers `shutil.rmtree(AUTO_ROOT[0])` at process exit (`:66-70`). This path is outside both `--work` and `/fast/scratch/.../SentinelSandbox`. |
| `(None,'1','1')` | Same cached auto-root path | No runner `rm` because KEEP=1; C1's atexit cleanup still removes it. |
| `('tally-audit','0','1')` | Relative to `cwd=tmp`: normally `<work>/tally-audit` | No runner `rm` because auto=0. |
| `('tally-audit-explicit','0','0')` | Relative to `cwd=tmp`: normally `<work>/tally-audit-explicit` | No runner `rm` because auto=0. |

The relative roots are only normally under the lexical work path: `main()` checks `os.listdir(a.work)` then sets `tmp=os.path.abspath(a.work)` (`:346-350`), without `realpath`, symlink rejection, or containment checks. `subprocess.run(..., cwd=tmp)` follows a symlink, as the reproduction demonstrates. A specimen can also overwrite `root` or `cd` before the cleanup. Therefore the set of paths a malicious block can delete is not bounded to those four configured strings; it includes any path the invoking UID can remove. The two probes establish this only against self-created scratch victims.

The invoked tool adds its own normal cleanup targets: `tally-audit-v3.py:354-369` creates and atexit-removes another `/tmp/tameshi-r4-2-regression.*` root; `audit():690-699` creates then removes `tempfile.mkdtemp(prefix='tally-audit-v3.')` under Python's selected temp directory. C1 invokes the tool with `--runner` (`c1-measure.py:276-282`), so this audit cleanup is in the counting path; the tool's `--selftest` temp at `:801-819` is not. The C1 counter itself leaves its `--work` files in place on a normal run, but a specimen can delete them by changing the operand.

**Impact.** The requested confinement property is false. A sealed/public specimen can cause pre-measurement filesystem deletion before the tool runs; the C1 oracle observes only exit/stdout and will not report that side effect. The read-only lane does not sandbox the subprocess from other same-UID writable files.

**Smallest remediation.** Execute all candidate blocks in an OS-level disposable isolation boundary (unprivileged UID plus a namespace/container) that exposes only a per-run writable scratch mount and the required read-only inputs. Path checks and `realpath` validation for `--work` are worthwhile for accidental symlinks, but cannot contain arbitrary shell code. Keep deletion of the owned auto-root outside the candidate block or confine it to that namespace.

## HYGIENE — no explicit child-process-group cleanup

`c1-measure.py:176-177` gives `subprocess.run(['bash', path], ..., timeout=300)` a timeout but does not create/manage a process group. No persistent-child test was run, so this is a code-level cleanup gap, not a reproduced survivor. Smallest remediation: run each block in a new process group and terminate the group on timeout; the OS isolation above is still required.

## What I could not break / limits

- I did not target `/tmp`, the home directory, the fleet checkout, or any path outside `/fast/scratch/hyaku/tameshi-r35-seats/SentinelSandbox/`; both successful deletion probes used fresh victims inside that tree.
- I did not run the full C1 measurement, the tool's selftest, or the runner. The reported proof is limited to the pinned counter's block execution and cleanup path.
- The assigned counter/tool/runner files contain no `resume_continuity_v1` or continuity-rejection path (search returned no matches); this surface has no resume rejection to exercise, and no other runtime was invoked.
- No claim is made that the counter's normal atexit cleanup deletes a path other than its generated auto-root or tool temp. The unbounded deletion finding is specifically the untrusted specimen execution proven above.
