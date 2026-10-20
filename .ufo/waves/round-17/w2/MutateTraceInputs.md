# MutateTraceInputs — round 17, wave 2

## Scope and axes

- **Depth:** six independent, one-line/token behavior-bearing mutants of `.ufo/evidence/round-17/coldread/trace-inputs.py` at `eb7838b16490ca7ba17ea3242ade76a61f744af2`.
- **Calibration:** run the unchanged `--selftest` on pristine, mutated, and exactly restored bytes; distinguish surviving mutants from demonstrated production failures.
- Seat: `TameshiR17.MutateTraceInputs-2`. This is a scoped mutation report, not a judgment of the round or either round-level claim.
- **Result: 3 killed, 3 survived, 0 inconclusive.** Every pristine/restored run exited 0 with `SELFTEST: 27/27`. Two survivors have direct behavioral witnesses; the third is a guard-removal coverage finding without a demonstrated bad receipt.

## Isolation, commands, and environment

All execution used six independent fleet-mirror clones, detached at the assigned landing. Only this report was written in the live lane. Target mutations were restricted to each clone; sibling symlinks were not modified. No delegation, background jobs, git writes in live repositories, or tool installations were performed.

Each clone used this setup (exit 0 for all six), with inherited `GIT_*` variables removed from the setup process environment, not exported into the session:

```sh
W=$(mktemp -d /tmp/tameshi-r17w2-MutateTraceInputs-XXXXXX)
mkdir "$W/fleet"
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" "$W/fleet/"
done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$W/fleet/tameshi-shokunin"
git -C "$W/fleet/tameshi-shokunin" checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
C=$W/fleet/tameshi-shokunin
T=$C/.ufo/evidence/round-17/coldread/trace-inputs.py
```

| Mutant | Absolute scratch root `W` |
|---|---|
| M01 | `/tmp/tameshi-r17w2-MutateTraceInputs-rVJpDr` |
| M02 | `/tmp/tameshi-r17w2-MutateTraceInputs-Zr3JCu` |
| M03 | `/tmp/tameshi-r17w2-MutateTraceInputs-tEunkZ` |
| M04 | `/tmp/tameshi-r17w2-MutateTraceInputs-yflcdI` |
| M05 | `/tmp/tameshi-r17w2-MutateTraceInputs-DJPBtG` |
| M06 | `/tmp/tameshi-r17w2-MutateTraceInputs-qYzEWK` |

For **each** row, the identical primary detector was executed once at each of the three stages, with process cwd set to that row's absolute `C`:

```sh
TMPDIR="$W" python3 "$T" --selftest
sha256sum "$T"
```

Detector invocations had a 60-second process deadline; none timed out. `TMPDIR` confined the selftest's own synthetic fixtures and trace workdirs beneath the assigned scratch root. Independent runs were batched concurrently. All primary detector stderr was empty. Observed tools: Python 3.14.8, strace 7.2, git 2.56.0. Neither `PYTHONPYCACHEPREFIX` nor `PYTHONDONTWRITEBYTECODE` was inherited by the outer test process.

## Kill table

`T:<line>` below means `.ufo/evidence/round-17/coldread/trace-inputs.py:<line>` at the pinned landing; one line was changed in each isolated clone. Results are `exit / SELFTEST count`.

| ID / source | Exact mutant | Expected/nearest named detector | Pristine | Mutated | Restored | Verdict |
|---|---|---|---|---|---|---|
| M01, `T:82` | Delete `RDWR\|` from `WRITE_FLAGS_RE` | `write-open-excluded`, `read-then-rewrite-excluded`; contract also requires O_RDWR exclusion | 0 / 27/27 | 0 / 27/27 | 0 / 27/27 | **Survived** |
| M02, `T:298` | `resolved not in self.tracked` → `resolved in self.tracked` | `git-tracked-filter`, `subdir-root-rev-null` | 0 / 27/27 | 1 / 25/27 | 0 / 27/27 | **Killed** |
| M03, `T:516` | `env["PYTHONPYCACHEPREFIX"] = cache` → `env["PYTHONPYCACHEPREFIX"] = "."` | `env-scrubbed`, `double-import-keeps-py`, `no-artifacts-inside-root` | 0 / 27/27 | 0 / 27/27 | 0 / 27/27 | **Survived** |
| M04, `T:644` | `if tracer.first_pid is None or tracer.first_pid not in tracer.exec_ok:` → `if tracer.first_pid is None:` | `missing-command-exit2` | 0 / 27/27 | 0 / 27/27 | 0 / 27/27 | **Survived** |
| M05, `T:303` | `self.lane_reads.add(resolved)` → `self.external.add(resolved)` | `live-lane-flagged` | 0 / 27/27 | 1 / 26/27 | 0 / 27/27 | **Killed** |
| M06, `T:304` | `elif under(resolved, self.fleet):` → `elif under(resolved, os.sep):` | Intended widening detector: `non-fleet-home-counted` / `non-home-outside-dropped`; actual killer: `fleet-external` | 0 / 27/27 | 1 / 26/27 | 0 / 27/27 | **Killed** |

Actual failing output, with all other named checks PASS:

```text
M02 (exit 1):
FAIL git-tracked-filter
FAIL subdir-root-rev-null
SELFTEST: 25/27
M05 (exit 1):
FAIL live-lane-flagged
SELFTEST: 26/27
M06 (exit 1):
FAIL fleet-external
SELFTEST: 26/27
```

M06 did **not** widen the accepted external set as initially intended. `under()` at `T:253-254` appends `os.sep`; a `/` prefix therefore tests ordinary absolute paths against `//`. The mutation drops ordinary fleet-external inputs, and `fleet-external` detects that regression. It does not establish sensitivity to every unsafe external-prefix widening.

## Survivors and behavioral evidence

The following supplementary witnesses were also run unchanged on pristine, mutated, and restored bytes for M01 and M03. They do not replace the primary `--selftest` verdict. All six witness wrapper invocations exited 0 with empty stderr and no timeout; each receipt recorded child exit 0. A wrapper exit 0 means successful tracing, not that the contract held.

Common witness command, executed with cwd `C`, using that mutant's absolute paths:

```sh
TMPDIR="$W" python3 "$T" --root "$C" --fleet-root "$W/fleet" \
  --live-lane "$C" --home-prefix "$W/synthetic-home" \
  --out "$W/witness.json" -- python3 -c "$CODE"
```

### M01 — O_RDWR is not exercised by the write fixtures

`CODE` was exactly:

```python
import os; fd=os.open('README.md',os.O_RDWR); os.close(fd); print('opened README.md with O_RDWR; no writes performed')
```

The child opened an existing tracked file without changing its contents. The stated contract excludes the **open mode**, even when no write follows (`T:33-36`). Receipt fields were opened and inspected after each stage:

| Stage | `inputs` | `untracked` | `tracked_filter` |
|---|---|---|---|
| Pristine | `{}` | `{}` | `true` |
| Mutated | `{"README.md":"39dae024da44d28889c5d934e12ae1f3331706b183d0bccdb69b702ebd239e0b"}` | `{}` | `true` |
| Restored | `{}` | `{}` | `true` |

Thus the surviving mutant demonstrably grants input credit to an O_RDWR open. Existing write fixtures at `T:816-821` use Python `'w'` opens and pass after this narrower regex omission. This is a demonstrated detector gap, not evidence that pristine code mishandles O_RDWR.

### M03 — prefix presence is checked, private/outside-root placement is not

`CODE` was exactly:

```python
import os,sys; p=sys.pycache_prefix; print('prefix_env='+os.environ.get('PYTHONPYCACHEPREFIX','<missing>')); print('prefix_runtime='+str(p)); print('prefix_in_root='+str(p is not None and os.path.commonpath([os.getcwd(),os.path.abspath(p)])==os.getcwd()))
```

Actual child output:

```text
Pristine:
prefix_env=/tmp/tameshi-r17w2-MutateTraceInputs-tEunkZ/trace-inputs-run-hmfh86gz/pycache
prefix_runtime=/tmp/tameshi-r17w2-MutateTraceInputs-tEunkZ/trace-inputs-run-hmfh86gz/pycache
prefix_in_root=False
Mutated:
prefix_env=.
prefix_runtime=.
prefix_in_root=True
Restored:
prefix_env=/tmp/tameshi-r17w2-MutateTraceInputs-tEunkZ/trace-inputs-run-u214tde7/pycache
prefix_runtime=/tmp/tameshi-r17w2-MutateTraceInputs-tEunkZ/trace-inputs-run-u214tde7/pycache
prefix_in_root=False
```

The mutated receipt nevertheless advertised `env_overrides.set.PYTHONPYCACHEPREFIX` as `/tmp/tameshi-r17w2-MutateTraceInputs-tEunkZ/trace-inputs-run-2gt0on0u/pycache`, not the actual `.`. The return value at `T:517` and receipt construction at `T:674-679` still use `cache`, independently of the mutated environment assignment. `env-scrubbed` at `T:891-898` checks prefix truthiness rather than equality, containment, or privacy. The import/artifact fixtures do not contain a pre-existing pyc cache. The private/outside-root environment guarantee is demonstrably violated while all 27 checks pass; no claim is made that this probe observed pyc credit or a cache write.

### M04 — missing-command fixture does not isolate the successful-root-exec guard

Removing successful-root-exec membership validation leaves every selftest assertion PASS, including `missing-command-exit2` (`T:846-847`). A bounded direct diagnostic, cwd M04's `C`, used the same strace syscall selection and supported flags:

```sh
strace -f -q -z -s 4096 -o "$W/missing-command.strace" \
  -e trace=open,openat,openat2,creat,execve,execveat,chdir,fchdir,fork,vfork,clone,clone3,dup,dup2,dup3,close \
  -y --seccomp-bpf --kill-on-exit --strings-in-hex=non-ascii -- ./no-such-command-xyz
wc -c "$W/missing-command.strace"
```

Observed strace exit 1, empty stdout, stderr `strace: Cannot stat './no-such-command-xyz': No such file or directory`; `wc` exited 0 and reported **0 bytes**. The missing-command case therefore produces no successful-root-exec evidence to distinguish from the still-present empty-log/`first_pid is None` guard. [INFERENCE] A fixture with a nonempty parseable trace but no successful root exec would be needed to isolate the removed conjunct. This survivor establishes selftest insensitivity to deleting that conjunct; it is **not** a demonstrated acceptance of a bad real-command trace.

## Hashes and exact restoration

`H0 = 521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070`.

`sha256sum "$T"` exited 0 before mutation, while mutated, and after restoring the original line in every clone:

| ID | Before | Mutated SHA-256 | After |
|---|---|---|---|
| M01 | H0 | `12194d0e323d748bd42aed675d6a27013fb13e691b408f8beb7eb48fdf0b5125` | H0 |
| M02 | H0 | `10b1ad1ad13723447129dd235435a10b48216d962846048cf141c1ef40ca033c` | H0 |
| M03 | H0 | `686a0fcd18313188e7df9822ac403f2f650993e56761ff8777f6065f907009f7` | H0 |
| M04 | H0 | `25fa1839663ad919b9e5d24030f5901a0b96af0f22d12d2c4316c71b4de62897` | H0 |
| M05 | H0 | `1984a53553604b58f460c7928929139485377c4b7eaf7c284dea67ddac91bdc6` | H0 |
| M06 | H0 | `c227519584e641f2a1580e0238179e99744449544d78e57c1d4fb0d8e0bef23b` | H0 |

The restored detector was executed for every row and returned `SELFTEST: 27/27`, exit 0. Both direct witnesses returned to their pristine behavior. No production fixes, contract changes, integrations, or round-level verdicts were made.

Verdict on the six trace-inputs.py selftest mutation probes: **partial — 3 killed, 3 survived, 0 inconclusive; all six targets restored byte-for-byte.**
