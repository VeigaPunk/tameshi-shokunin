# Verdict — High potential disclosure

A selftest can read the bubblewrap supervisor's command line and inherited environment through `/proc/1`. The command line identifies its unique `/w` source path, but not the semantic job name: `name` is not included in the invocation and is unused in `selftest()`. The selftest can read its own fixed `tools/mutate-and-run.sh --selftest` argv, but not the counter's outer argv, the counter file, or the lane. No host network, `/sys`, or other job tree was visible in the probe.

Severity is conditional on secrets being present in the counter's invoking environment. The environment-read boundary failure itself is confirmed.

## Evidence

Source: `.ufo/evidence/round-30/c1-measure-v4.py`:

- Lines 321–326 mount `/proc`, `/dev`, and private `/tmp`; `/usr` and `/etc` are read-only; `--clearenv` applies to the sandbox command.
- Lines 329–341 create a fresh `w...` directory, bind it read-write at `/w`, invoke `bash tools/mutate-and-run.sh --selftest`, then remove the directory. `name` is not used in this body.
- Lines 335–336 launch bubblewrap without a restricted `env=` argument. Lines 351–356 use the scrubbed `env` only for Git commands, not for the selftest subprocess.
- Lines 418–420 keep job names in the counter's result mapping; they are not passed in the command or environment.

In my scratch clone, I ran the source BWRAP flags with a probe bound as `/w` (the only substituted input was the private scratch directory):

```text
timeout 40 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.SentinelBwrap-11/clone/lab/job1 /w --chdir /w bash tools/mutate-and-run.sh --selftest
```

Observed output (the `/fast/scratch/hyaku/tameshi-r30a2` check was existence-only):

```text
runner_argv=tools/mutate-and-run.sh --selftest
proc_numeric_pids=['1', '2', '3']
proc1_status_ppid='PPid:\t0'
proc1_cmdline='bwrap ... --bind /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.SentinelBwrap-11/clone/lab/job1 /w ...'
parent_cmdline='bash tools/mutate-and-run.sh --selftest'
env={'HOME': '/w', 'LANG': 'C.UTF-8', 'PATH': '/usr/bin', 'PWD': '/w', 'SHLVL': '1', 'TMPDIR': '/tmp', '_': '/usr/bin/python3'}
root_entries=['bin', 'dev', 'etc', 'lib', 'lib64', 'proc', 'sbin', 'tmp', 'usr', 'w']
path=/home exists=False ...
path=/var exists=False ...
path=/sys exists=False ...
/sys_list_error=FileNotFoundError
/dev_entries=['core', 'fd', 'full', 'null', 'ptmx', 'pts', 'random', 'shm', 'stderr', 'stdin', 'stdout', 'tty', 'urandom', 'zero']
network_interfaces=[(1, 'lo')]
/proc/net/route='Iface ...'  # header only; no routes
other_job_exists=False
sealed_dir_exists=False
counter_read=NO FileNotFoundError
lane_list_read=NO FileNotFoundError
host_tools_read=NO FileNotFoundError
wrote=/tmp/probe-marker,/w/probe-marker
```

I then ran the same BWRAP invocation with the harmless host-side test variable `SENTINEL_PROBE_CANARY=visible-only`. I printed no host environment values other than that canary:
Exact invocation:

```text
SENTINEL_PROBE_CANARY=visible-only timeout 40 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.SentinelBwrap-11/clone/lab/job3 /w --chdir /w bash tools/mutate-and-run.sh --selftest
```


```text
proc1_environ_read=True count=264 error=None
proc1_canary=b'visible-only'
proc1_known_vars={'PATH': True, 'HOME': True, 'LANG': True, 'TMPDIR': False, 'SENTINEL_PROBE_CANARY': True}
proc2_environ_read=True count=5 error=None canary_present=False
proc3_environ_read=True count=7 error=None canary_present=False
```

Thus `--clearenv` scrubs the command's environment but not the visible bubblewrap process's environment. `/proc/1/cmdline` also exposes the full BWRAP argv and its host bind-source path. The counter's own argv is not that process's argv and was not present in the sandbox.

For job isolation, job 1 wrote markers to `/tmp` and `/w`; a host-side check saw `host_job1_w_marker=present`. A second invocation bound to a different scratch job directory observed:
Second-job invocation:

```text
timeout 40 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.SentinelBwrap-11/clone/lab/job2 /w --chdir /w bash tools/mutate-and-run.sh --selftest
```


```text
tmp_marker_from_previous_job=False
w_marker_from_previous_job=False
tmp_write=True w_write=True
```

`/tmp` is a fresh tmpfs per invocation; `/w` is writable but each invocation gets its own host temp directory, removed at source line 340. The `/w` mount's `/proc/self/mountinfo` entry also names its source path. In the actual counter that path is a generated `w...` child of the counter temp tree, not the job label.

I confirmed a one-flag mitigation in scratch only: adding bubblewrap's supported `--as-pid-1` made `/proc/1/cmdline` be `bash tools/mutate-and-run.sh --selftest`, with a five-entry environment and no test canary. Its mountinfo still exposed the unique `/w` source path.
Exact scratch-only mitigation probe:

```text
SENTINEL_PROBE_CANARY=visible-only timeout 40 bwrap --unshare-all --die-with-parent --new-session --as-pid-1 --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.SentinelBwrap-11/clone/lab/job4 /w --chdir /w bash tools/mutate-and-run.sh --selftest
```

Observed:

```text
pid=1 cmdline='bash tools/mutate-and-run.sh --selftest' env_count=5 canary=None
mountinfo_w=['... /scratch/hyaku/tameshi-r30a2-seats/TameshiR30A2.SentinelBwrap-11/clone/lab/job4 /w rw ...']
proc1_status_ppid='PPid:\\t0'
```


## Exploit path and impact

A selftest can read `/proc/1/environ` and `/proc/1/cmdline`. The former exposes values inherited by bubblewrap from the counter's caller; any secrets in that environment are readable by the untrusted selftest despite `--clearenv`. The latter reveals the BWRAP arguments and unique temporary bind path, allowing the run to be distinguished by that opaque path, but not mapped directly to the counter's `name` label. `/proc` contains only namespace processes; PID 1 has `PPid: 0`, and the host counter process is not visible.

The sandbox otherwise has no mounted lane/counter filesystem, no `/sys`, only loopback and no routes, and a private `/dev`. The counter captures stdout and only retains the exit code and whether `VERDICT: PASS` appeared, so this probe did not demonstrate direct raw-output or network exfiltration. A malicious selftest can still make its recorded result depend on readable environment values.

## Smallest safe correction

Add `--as-pid-1` to `BWRAP`. The scratch probe confirmed it hides the bubblewrap supervisor's command line and inherited environment while retaining procfs for the child. The remaining mountinfo path is an opaque per-invocation path, not the semantic job name. If policy requires hiding even that identifier, the `/proc` view must also be redesigned; simply removing procfs should be checked against the runner's `/dev/fd` process-substitution use before adoption.
