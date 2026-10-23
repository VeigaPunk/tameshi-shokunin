# SentinelTool — containment and safety review

**Verdict: high risk for untrusted runner files outside the counter wrapper.** `tally-audit.py` is an executor, not a static-only auditor: it passes runner-derived Bash to the host shell, and `--then-regression` launches the entire runner. The counter's `bwrap` materially limits filesystem/network access, but does not impose explicit output, memory, or `/tmp` quotas and exposes host-readable `/etc` and `/usr` data. No production runner or v2 counter main was executed; all probes below ran from this seat's scratch directory.

Axes: host integrity, process/resource containment, confidentiality, evidence integrity.

| Risk | Path:line | Exploit or probe evidence | Severity | Smallest safe fix |
|---|---|---|---|---|
| Untrusted runner content executes as the caller. | `tools/tally-audit.py:156-165,313-327,357-371,380-393` | `audit()` reads the supplied file, then `bash()` executes the extracted tally and `run_harness()` executes the runner's harness section. A crafted runner can run shell commands during an ordinary audit with the invoking user's filesystem/network permissions. `--then-regression` additionally invokes `bash RUNNER --regression` directly, with inherited environment, no sandbox, and no timeout. Argument vectors avoid shell-argument injection; they do not contain the script source being interpreted. | **Critical** when the runner is untrusted | Put every runner-derived Bash execution, including `--then-regression`, inside the same filesystem/network sandbox; otherwise reject untrusted runner inputs and make the trusted-only contract explicit. |
| Timeout does not kill the shell's descendants; cleanup errors are suppressed. | `tools/tally-audit.py:162-165,363-371,380-384` | Scratch probe command/output below: `timeout_probe` returned after 0.11 s, but a background child wrote its marker later. A child can therefore continue after the nominal 120 s timeout and after `audit()` begins cleanup. `--then-regression` has no timeout at all. Separately, `shutil.rmtree(..., ignore_errors=True)` hides a failed cleanup; the cleanup probe left a chmod-000 directory behind until the probe restored permissions. | **High** | Start each subprocess in a new session and kill/reap its process group on timeout; give `--then-regression` a timeout too. Do not silently ignore cleanup failures; keep untrusted execution in a disposable sandbox. |
| Predictable helper-script paths follow attacker-created symlinks. | `tools/tally-audit.py:156-160,313-321` | The helper chooses `p%d.sh`/`h%d.sh` from `len(os.listdir(tmp))`, then opens with ordinary `open(..., 'w')`. Scratch probe: `symlink_probe: entries=1 chosen=p1.sh is_symlink=True victim='probe-generated script'`. The probe reproduced the helper naming and open sequence: a shell running as the same user removed `p0.sh`, made `p1.sh` point to a scratch victim outside the helper temp directory, and the next open truncated that victim. This is not a bwrap escape; under the counter wrapper the writable target is confined to the sandbox's writable mounts. | **High** standalone; **Medium** within the counter sandbox | Create each script with `tempfile.mkstemp()`/exclusive creation and execute that unique path; never derive a writable path from directory-entry count. |
| Captured output and writable tmpfs have no explicit resource cap. | `tools/tally-audit.py:162,325,384`; `.ufo/evidence/round-32/v2/c1-measure-v2.py:257-265,384-387` | Both audit subprocesses and the sandbox wrapper use `capture_output=True`; a runner can emit arbitrarily large stdout/stderr and Python buffers it. Scratch probe captured 1,048,576 bytes in one run. The sandbox has `timeout 600` but no byte/memory limit; `--tmpfs /tmp` has no `--size` argument, and `--jobs` is caller-settable. A hostile copy can exhaust host memory/tmpfs before the time limit. | **High** | Bound captured bytes (or stream to bounded files and terminate on overflow), set a `/tmp` size quota, and enforce per-run memory/CPU and a maximum worker count. |
| The advertised empty `--work` check accepts symlinks and writes through them. | `.ufo/evidence/round-32/v2/c1-measure-v2.py:292-296,320-324,361-379` | Scratch probe of the exact path check: `work_symlink_probe: supplied=True destination_validate_exists=True`. An empty symlink target passes `exists/listdir`; subsequent `os.makedirs(work/validate)` and tool/copy writes land in the target directory, outside the textual work path. This requires a caller/config to supply the symlink; it is not runner-controlled. | **Low** (operator path confusion) | Reject `--work` when `lstat()` says symlink, and validate the resolved destination against the intended scratch root before writing. |
| Host-readable configuration is exposed inside the sandbox; network isolation worked in the probe. | `.ufo/evidence/round-32/v2/c1-measure-v2.py:257-264` | Exact bwrap probe and output below. `/home/.../tameshi-shokunin` was absent; `/etc/passwd` and `/etc/hosts` were readable, `/etc/shadow` was not; tool/runner binds were readable but not writable. TCP `connect_ex` returned `101` (network unreachable). A follow-up write probe got `PermissionError` appending to `/etc/hosts`; writing `/tmp/<token>` succeeded inside and the host `/tmp` marker was absent afterward. Thus `--unshare-all`, read-only binds, and private `/tmp` worked for these checks, but the entire host `/etc` (and `/usr`) remains readable. | **Medium** (host metadata disclosure; no secret-file access observed) | Bind only the minimal host-independent `/etc` files needed by Python/runtime, rather than all of `/etc`; retain the read-only and network namespace settings. |
| Child Bash inherits caller stdin despite the cleared environment. | `tools/tally-audit.py:162,325`; `.ufo/evidence/round-32/v2/c1-measure-v2.py:265` | Scratch command/output below: piping `stdin-canary` into a Python process whose `subprocess.run(..., capture_output=True)` launched Bash produced `child_read=stdin-canary`. `capture_output` does not set `stdin`; `--clearenv` also does not close inherited file descriptors. A runner can consume piped secrets or interactive input. | **Medium** | Set `stdin=subprocess.DEVNULL` at the outer bwrap and every Bash/runner subprocess boundary. |
| Untrusted held-out metadata can forge log lines. | `.ufo/evidence/round-32/v2/c1-measure-v2.py:345-356,389-393` | `id`, `author`, and Git path are interpolated directly into `HELDOUT`/`COPY` output; the schema gate checks only the set and edits list before printing. A JSON string containing newline or terminal control characters can make evidence output appear to contain records/statuses that were not emitted by the counter. This does not alter the computed predicate. | **Low** | Validate metadata field types and escape/control-filter all record fields before printing (for example, use `repr`/JSON encoding). |

## Scratch probe transcript

Working directory for each command: `/fast/scratch/hyaku/tameshi-r32-seats/TameshiR32.SentinelTool`.

1. `timeout 15 python3 safety_probe.py`

```text
symlink_probe: entries=1 chosen=p1.sh is_symlink=True victim='probe-generated script'
timeout_probe: timeout_elapsed=0.11s marker_before_wait=False
timeout_probe: descendant_marker_after_wait=True
capture_probe: returncode=0 captured_stdout_bytes=1048576
```

2. Cleanup behavior, using the same `ignore_errors=True` operation as the tool:

```sh
python3 -c 'import os,shutil,tempfile; d=tempfile.mkdtemp(prefix="cleanup-probe-",dir="."); open(os.path.join(d,"residue"),"w").close(); os.chmod(d,0); shutil.rmtree(d,ignore_errors=True); survived=os.path.exists(d); print("ignore_errors_cleanup_dir_survived=%s"%survived); os.chmod(d,0o700) if survived else None; shutil.rmtree(d,ignore_errors=True)'
```

```text
ignore_errors_cleanup_dir_survived=True
```

3. `timeout 10 python3 path_probe.py`

```text
work_symlink_probe: supplied=True destination_validate_exists=True
```

4. Stdin inheritance probe:

```sh
printf 'stdin-canary\n' | python3 -c 'import subprocess; p=subprocess.run(["bash","-c","read -r line; printf \"child_read=%s\\n\" \"$line\""],capture_output=True); print(p.stdout.decode().strip())'
```

```text
child_read=stdin-canary
```

5. bwrap probe used the counter's namespace/mount/environment flags with harmless files from this scratch directory:

```sh
bwrap --version && timeout 10 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --ro-bind /fast/scratch/hyaku/tameshi-r32-seats/TameshiR32.SentinelTool/dummy-tool.py /t/tally-audit.py --ro-bind /fast/scratch/hyaku/tameshi-r32-seats/TameshiR32.SentinelTool/dummy-runner.sh /in/runner.sh --setenv PATH /usr/bin --setenv HOME /tmp --setenv TMPDIR /tmp --setenv LANG C.UTF-8 --chdir /tmp python3 -c 'import os,socket; print("home_lane_visible=%s" % os.path.exists("/home/vgpnk/Projects/shokunin/tameshi-shokunin")); print("etc_passwd_readable=%s" % os.access("/etc/passwd", os.R_OK)); print("etc_hosts_readable=%s" % os.access("/etc/hosts", os.R_OK)); print("etc_shadow_readable=%s" % os.access("/etc/shadow", os.R_OK)); print("tool_readable=%s runner_readable=%s" % (os.access("/t/tally-audit.py", os.R_OK), os.access("/in/runner.sh", os.R_OK))); print("tool_writable_access_check=%s" % os.access("/t/tally-audit.py", os.W_OK)); open("/tmp/private-probe", "w").write("scratch"); s=socket.socket(); s.settimeout(1); print("external_tcp_connect_ex=%s" % s.connect_ex(("1.1.1.1",443))); print("routes_bytes=%s" % len(open("/proc/net/route").read()))'
```

```text
bubblewrap 0.13.1
home_lane_visible=False
etc_passwd_readable=True
etc_hosts_readable=True
etc_shadow_readable=False
tool_readable=True runner_readable=True
tool_writable_access_check=False
external_tcp_connect_ex=101
routes_bytes=128
```

Follow-up command, with harmless scratch inputs:
```sh
token=sentinel-$$; timeout 10 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --ro-bind /fast/scratch/hyaku/tameshi-r32-seats/TameshiR32.SentinelTool/dummy-tool.py /t/tally-audit.py --ro-bind /fast/scratch/hyaku/tameshi-r32-seats/TameshiR32.SentinelTool/dummy-runner.sh /in/runner.sh --setenv PATH /usr/bin --setenv HOME /tmp --setenv TMPDIR /tmp --setenv TOKEN "$token" --chdir /tmp python3 -c 'import os
open("/tmp/"+os.environ["TOKEN"],"w").write("private")
print("tmp_write=True")
print("etc_hosts_readable=%s" % os.access("/etc/hosts",os.R_OK))
try:
 open("/etc/hosts","a").write("probe")
 print("etc_hosts_append=unexpected-success")
except OSError as e:
 print("etc_hosts_append=%s errno=%s" % (type(e).__name__,e.errno))'; if test -e "/tmp/$token"; then printf 'host_tmp_after=yes\n'; else printf 'host_tmp_after=no\n'; fi
```
Observed output:
```text
tmp_write=True
etc_hosts_readable=True
etc_hosts_append=PermissionError errno=13
host_tmp_after=no
```

`bwrap --help` reported `--die-with-parent` as killing the command when bwrap or its parent dies, and documents `--size BYTES` for `--tmpfs`; the counter uses the former but does not configure the latter. No tools were installed, and no production files were changed.
