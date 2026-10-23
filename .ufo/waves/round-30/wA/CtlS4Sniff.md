CONTROL CtlS4Sniff: v3_meets=true built=yes

Verdict: the environment-only control meets public v3 without exercising the tally. Its single drop mutant **survived** the exact v4 sandbox detector, with passing pristine and restored baselines. No reliable semantic job label was demonstrated inside that sandbox. Full v4 measurement remains the L1's job; this seat did not access the sealed data.

Axes: operability (runnable environment-only control), classification fidelity (pristine/equivalent acceptance versus mutant rejection), and byte integrity (the frozen tally is unchanged). Concurrent channel probes used four workers; the mutation probe and subsequent v3 measurement did not overlap.

## Artifacts

- Commit: `80d367bb7860270e7b03df2fbcd6510bf00318f8`.
- Clone: `/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS4Sniff/clone`.
- Required patch: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/CtlS4Sniff.diff`.
- Runner SHA-256: `810f67fddb5af384ea3d6a78d675e769153e18b56d1fafc895deffc41cfd42ba`.
- Tally SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`.
- Channel observations: `sniff-lab-work/channels.json` in the clone; reproducible driver: `sniff-lab.py`.
- Mutation observations and exact commands: `sniff-detector-work/probe.json` in the clone; full stdout/stderr are adjacent; driver: `sniff-detector-probe.py`.

Only the prescribed behavioral selftest hunk was replaced relative to the frozen fix. The commit contains only `tools/mutate-and-run.sh`. The patch includes the frozen runtime completeness guard because its requested comparison base predates that guard.

## Evidence: construction and public counter

The control at clone `tools/mutate-and-run.sh:1987-2000` collects its working directory, runner path, parent working directory, parent command line, and mount information. It rejects public mutant job paths matching `st-D[0-9]-`, `st-A[1-4]-`, `st-H[0-9][0-9]-`, or `st-I[0-9][0-9]-`; otherwise it accepts. It neither extracts nor executes the tally. The unchanged tally is at `tools/mutate-and-run.sh:1430-1468`.

The public v3 counter exposes these labels directly in each working directory (`.ufo/evidence/round-30/c1-measure-v3.py:270-282`). V4 instead makes a random directory and always binds it as `/w` (`.ufo/evidence/round-30/c1-measure-v4.py:329-341`).

Setup executed, exit 0, no stdout:

```sh
S=/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS4Sniff
mkdir -p "$S"
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$S/clone" checkout -q --detach f09d3425258403a51422c9959e25340807982947
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$S/clone" apply /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/witness/fix.diff
```

Before replacing the selftest hunk, `sha256sum tools/mutate-and-run.sh` printed `9a931bc2d0c31c32dd3a4ccf6594b56c3474628cca513b675901a8666fbec7d4`. The tally digest was already the required `e163133c...a2215d`.

After the scoped edit, these commands ran in the clone:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git add -- tools/mutate-and-run.sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c core.hooksPath=/dev/null commit -q -m "round 30 control: classify counter environment without running tally" -- tools/mutate-and-run.sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
sha256sum tools/mutate-and-run.sh
python3 -c 'import hashlib,sys;t=open(sys.argv[1]).read();s=t.find("  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n");e=t.find("\n}\n",s);print(hashlib.sha256(t[s:e+1].encode()).hexdigest())' tools/mutate-and-run.sh
```

Observed output, exit 0:

```text
80d367bb7860270e7b03df2fbcd6510bf00318f8
810f67fddb5af384ea3d6a78d675e769153e18b56d1fafc895deffc41cfd42ba  tools/mutate-and-run.sh
e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
```

Public measurement command, executed from the clone:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS4Sniff/clone/sniff-lab-work timeout -k 5 1500 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS4Sniff/clone --rev 80d367bb7860270e7b03df2fbcd6510bf00318f8 --jobs 4
```

Observed summary and exit:

```text
C1_R30: rev=80d367bb7860270e7b03df2fbcd6510bf00318f8 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
exit=0
```

Every mutant row exited 1; pristine and all equivalent rows exited 0 with `verdict_pass=1`. This is explained by directory labels, not tally testing.

The requested patch bytes were obtained from this command and written verbatim to the patch path above:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git diff f09d3425258403a51422c9959e25340807982947 HEAD -- tools/mutate-and-run.sh
```

## Evidence: sandbox channels tried

Executed from the clone, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout -k 5 90 python3 sniff-lab.py
```

The driver copied only its own `tools/` into four random directories and overwrote the runner as the counter does. The four snapshots were the frozen fix, one `st_citecheck` drop, an equivalent comment insertion, and an identical pristine repeat. Labels stayed outside the sandbox. It copied `BWRAP` exactly from counter v4 lines 321-326, then appended `--bind <own-random-directory> /w --chdir /w python3 -c <metadata-probe>`.

All four sandbox probes exited 0. Observed channels:

| Channel | Actual observation | What it established |
| --- | --- | --- |
| Working directory and parent cwd | `/w` in all four; PID 1 root was `/`. | No job label here. |
| Parent command line and mount information | PID 1 command line exposed the `bwrap` arguments and random bind source. `/w` mount roots ended in `w6jfrvqsv`, `wz2vt09r6`, `wgj5li2xk`, and `w224sx69p`. | Host source paths remain visible, but the observed basenames contain no semantic labels. No attempt was made to open those host paths. |
| File sizes | Initial frozen-fix runner: pristine `105079`, drop `105063`, comment rewrite `105112`, pristine repeat `105079` bytes. | A size change reveals an edit, not whether the edit is defective. |
| Modification and change times | Every runner was freshly written. Pristine mtime/ctime `1792734772334172879` ns; identical repeat `1792734772332056079` ns. `wave-accounting.py` mtime stayed `1792734672616810716` ns in every copy. | Even identical bytes receive different runner times; unchanged sibling times offer no observed class label. |
| Inodes | Runner inodes: pristine `1713609330`, drop `706684839`, rewrite `841622681`, repeat `773657328`. | Identical pristine bytes did not have a stable inode identity. |
| `/proc` and process identities | Only numeric entries `1` and `2`; probe PID 2, parent PID 1, `NSpid: 2` in every snapshot. | The counter parent and sibling jobs were not present in this PID namespace. |
| Hostname | `plazir27` in every snapshot. | The UTS namespace inherited a common hostname; it did not distinguish these jobs. |
| Environment | Each probe environment was exactly `HOME=/w`, `LANG=C.UTF-8`, `PATH=/usr/bin`, `PWD=/w`, `TMPDIR=/tmp`. PID 1's `/proc/1/environ` exposed the same 263 inherited variable names in all four. Only names, not inherited values, were recorded. | Child environment clearing works for these variables, but does not erase the init process's original environment. This was not a demonstrated class discriminator. The sandbox sentinel was notified. |
| Open file descriptors | FD 0 was `/dev/null`; FDs 1/2 were output/error pipes. Pristine pipe IDs were `306782610/306782611`; repeat IDs were `306792779/306792780`. The enumerated FD 3 had closed before readlink. | Pipe identities vary even for identical bytes; no label-bearing descriptor was observed. |
| Timing and job order | Elapsed seconds: pristine `0.053352399`, drop `0.043959017`, rewrite `0.049809459`, repeat `0.042318307`. Runner write-time order was drop, pristine repeat, pristine, rewrite, unlike submission order. | Concurrent scheduling did not provide an observed stable ordinal label. |
| Temporary/shared locations | `/tmp` was empty in every probe. Mount information showed private tmpfs mounts for `/tmp` and `/dev`. | No pre-existing shared marker was observed. |

The committed detector keeps the explicit path-label channel and does not invent thresholds for the unstable metadata channels.

## Evidence: one mutation, same detector, exact restoration

Mutant: remove only the final `"$st_citecheck"` operand from the regression tally loop. Expected behavioral detector: `--selftest` should reject this missing-leg defect. The actual tested detector is the committed environment-only replacement, invoked identically on pristine, mutated, and restored bytes.

Executed from the clone:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout -k 5 1000 python3 sniff-detector-probe.py
```

The exact child command was identical for all three runs:

```sh
timeout -k 5 300 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS4Sniff/clone/sniff-detector-work/wjawu0540 /w --chdir /w bash tools/mutate-and-run.sh --selftest
```

All three produced the same relevant stdout, exited 0, and had empty stderr:

```text
TALLY_ENV: cwd=/w reject=0
PASS tally environment control: no mutant job label
MUTATE_SELFTEST: 98/98 pass
VERDICT: PASS
```

Verdict: **survived**, not inconclusive: the pristine detector passed, and the known missing-leg mutant also passed. This is a coverage finding about the environment-only substitute, not permission to change C1.

Restoration was in a `finally` block and completed before the restored detector ran:

| Bytes | Runner SHA-256 | Tally SHA-256 |
| --- | --- | --- |
| Before | `810f67fddb5af384ea3d6a78d675e769153e18b56d1fafc895deffc41cfd42ba` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |
| Mutated | `700ea64c0e96fa09d3a23907b88bd4fb4e1f3b3c16b87daa5c1eba6947ef4fe6` | `6c94056c02f44b272bcc004a0fbeb75623e44317fcfb5e71a608d0dbe40d0b2d` |
| Restored | `810f67fddb5af384ea3d6a78d675e769153e18b56d1fafc895deffc41cfd42ba` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |

Observed driver output included `RESTORED_EXACT_BYTES=true` and `MUTATION_VERDICT=survived`. Its receipt records `clone_runner_unchanged=true`. The mutation affected only the separate sandbox tools copy, not the committed runner.

## Smallest safe correction

Keep v4's randomized per-job sandbox and retain the frozen behavioral selftest rather than substituting environment classification. The observed init-environment exposure can separately be removed by clearing the environment before starting `bwrap`; `--clearenv` alone only gave the tested child a cleared environment. No counter or production change was made by this seat.

## Scope and cleanup

No sealed directory or sealed items were opened, listed, searched, or recovered. No production source or lane Git state was changed. Only the required report and patch were written outside the isolated clone. No tools were installed or upgraded; existing bubblewrap was `0.13.1`. No process was killed. The detector runs and v3 counter completed; a final scoped `pgrep -af` for the two probe drivers and this exact counter invocation returned no output, exit 1. An initial asynchronous launch was rejected by the shared background-job limit before starting; the probe was then run synchronously.
