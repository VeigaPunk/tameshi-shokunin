# Verdict: survived the prescribed probe; broader unreachability is inconclusive

The probe exited 0 and printed `COUNT: 0`, with no pathnames and no stderr. It did not falsify the hypothesis. This is not proof that no matching path is reachable: the requested `-xdev` traversal does not descend into other filesystems, `-name` tests basenames rather than full paths, errors are suppressed, and output is capped at 20 paths.

Axis: operability. Probe constraints: exact sandbox arguments, bounded execution, isolated writes, and byte-exact restoration. No C1 measurement or counter score was attempted.

## Evidence

### Source and isolated copy

- Public sandbox definition: `.ufo/evidence/round-30/c1-measure-v4.py:321-326`; tools-only materialization and invocation: lines 329-336.
- Public counter SHA-256: `cccae0bd984a7c67c22d83a1e67d19e3ebc76c015094106a1370d330030a5f07`.
- Scratch clone: `/fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ProbeSealedReach-11/clone`.
- Clone was detached at `f09d3425258403a51422c9959e25340807982947` using the requested no-hardlinks clone. Clone and checkout both exited 0 without output.
- `probe-w/tools` was copied from that clone's `tools` with symlinks preserved. Only `probe-w`, containing the tools copy, was bound at `/w`; the complete clone and its Git metadata were not bound.

Exact clone command executed:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ProbeSealedReach-11 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 90s git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ProbeSealedReach-11/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30s git -C /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ProbeSealedReach-11/clone checkout -q --detach f09d3425258403a51422c9959e25340807982947
```

### Probe runner and single-point mutation

Retained runner: `/fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ProbeSealedReach-11/clone/probe-w/tools/probe-sealed-reach.sh:1-11`.

```bash
#!/usr/bin/env bash
set -u
if [[ ${1:-} != --selftest ]]; then
  printf 'Usage: probe-sealed-reach.sh --selftest\n' >&2
  exit 2
fi
mapfile -t paths < <(find / -xdev -path /proc -prune -o \( -name '*tameshi*' -o -name '*c1-sealed*' \) -print 2>/dev/null | head -20)
if ((${#paths[@]})); then
  printf '%s\n' "${paths[@]}"
fi
printf 'COUNT: %s\n' "${#paths[@]}"
```

The count is the number of captured paths, not an uncapped filesystem census. Probe SHA-256: `135857a9b862f3181c119a2d64e2fb38fc730450722e029746472d82fa9d5741`.

The only existing-source mutation was the selftest dispatch at `clone/probe-w/tools/mutate-and-run.sh:2013`:

```diff
-  selftest) selftest ;;
+  selftest) bash /w/tools/probe-sealed-reach.sh --selftest ;;
```

Expected detector: a pathname from the prescribed find command would falsify the hypothesis. This is a sandbox diagnostic, not a tally-block mutant or a claim that the counter accepts this runner.

### Exact bounded invocation and observed output

The following argv was run with the working directory set to the scratch clone and `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed from the launch environment. The `BWRAP` list was obtained by parsing the public Python assignment with `ast.literal_eval`, without executing the counter or loading sealed inputs. One job ran at a time.

```sh
timeout --kill-after=5s 120s bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.ProbeSealedReach-11/clone/probe-w /w --chdir /w bash tools/mutate-and-run.sh --selftest
```

Complete probe stdout:

```text
COUNT: 0
```

Exit: `0`. Stderr: empty. No discovered path was opened; there were no discovered pathnames. The forbidden sealed directory was not opened, listed, searched, or read.

### Pristine, mutated, and restored runs

The same bounded invocation above was used for all three states:

| State | Exit | Observed stdout |
| --- | --- | --- |
| Pristine | 0 | Final lines: `MUTATE_SELFTEST: 97/97 pass`, `VERDICT: PASS` |
| Mutated dispatch | 0 | Complete output: `COUNT: 0` |
| Restored | 0 | Final lines: `MUTATE_SELFTEST: 97/97 pass`, `VERDICT: PASS` |

All three stderr streams were empty. The complete pristine and restored stdout streams compared equal. Thus the baseline did not fail. The hypothesis survived this detector; the stronger reachability claim remains inconclusive because of the detector's stated traversal limits. No tally-mutant killed/survived classification is implied.

## Restoration evidence

| Runner state | SHA-256 |
| --- | --- |
| Before mutation | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Mutated dispatch | `e6de78c2ea22accf39eac89176d679f037714a43a9b852f71bb879daf2f3e2d6` |
| After restoration | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| Unmodified clone's original tools runner | `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |

The restored runner also compared byte-for-byte equal to the saved pristine bytes. The one-line dispatch change was removed; the standalone probe runner remains available. No production source was edited and no Git write command ran outside the isolated clone.

All bounded subprocesses returned. A final `/proc/*/cwd` check found no other process with a working directory in this clone; no process needed killing. Bubblewrap reported `bubblewrap 0.13.1`. No tools were installed or updated.

## Smallest safe correction

Limit the conclusion to the actual observation: the prescribed bounded root-device traversal emitted zero matching basenames in this sandbox invocation. Do not describe that result as universal path unreachability. No production correction was made or inferred from this probe.
