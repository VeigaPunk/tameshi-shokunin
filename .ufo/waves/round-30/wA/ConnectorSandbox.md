# ConnectorSandbox — cross-lane candidate-runner pattern scan

Seat: TameshiR30A2.ConnectorSandbox-7. Report-only. No production file was edited, no tools were installed, no gate or selftest was run. Report path: `.ufo/waves/round-30/wA/ConnectorSandbox.md`.

## Axes

- Operability (C1): whether the runner tests the tally block rather than side channels.
- Containment: whether the candidate can see job identity, host paths, environment, or counter source.
- Adjacency: whether the same isolation pattern is reusable across sibling lanes without importing their defects.

## Verdict

The useful pattern is not “bwrap exists”; it is the combination already present in tameshi v4: a fresh per-job directory, a constant in-sandbox mount point (`/w`), no semantic job label in argv or environment, and `/proc` only inside the new pid namespace. That combination prevents label-keyed classification. It does not, by itself, prevent the `/proc/1` supervisor disclosure found in kumitate r44 and reproduced in tameshi v4; that needs `--as-pid-1` plus a restricted spawn environment.

## Findings (path:line)

1. Tameshi v4 counter source:
   - `.ufo/evidence/round-30/c1-measure-v4.py:321-326` — `BWRAP` flags: `--unshare-all --die-with-parent --new-session --clearenv`, read-only `/usr` and `/etc`, procfs, dev, tmpfs, and only `PATH`, `HOME`, `LANG`, `TMPDIR` set.
   - `.ufo/evidence/round-30/c1-measure-v4.py:329-341` — `selftest()` makes a fresh `w...` directory, copies `tools/` into it, writes the candidate runner, runs it under bwrap bound at `/w`, then removes the directory.
   - `.ufo/evidence/round-30/c1-measure-v4.py:335-336` — `subprocess.run(BWRAP + ['--bind', d, '/w', '--chdir', '/w', 'bash', RUNNER, '--selftest'], ...)` with no `env=` restriction.
   - `.ufo/evidence/round-30/c1-measure-v4.py:351-356` — the scrubbed `env` is used only for Git commands, not for the selftest subprocess.
   - `.ufo/evidence/round-30/c1-measure-v4.py:418-420` — result mapping retains job `name`s in the counter, but `name` is not passed to the sandbox.
   - Net effect: the semantic job label is not in the sandbox path, argv, or environment; the mount source path is an opaque generated `w...` path.

2. Tameshi v4 already has a containment report for the same boundary:
   - `.ufo/waves/round-30/wA/SentinelBwrap.md` — confirms `/proc/1/environ` and `/proc/1/cmdline` are visible; `--clearenv` scrubs the child environment but not bwrap PID 1; `--as-pid-1` hides both while retaining procfs and the opaque `/w` mount source.

3. Sibling lane kumitate r44 uses the same bwrap family and has the same disclosure:
   - `kumitate-shokunin/.ufo/waves/round-44/controls/SentinelSandboxEscape.md:7` — counter argv under review: `bwrap --unshare-all --die-with-parent --new-session --clearenv ... --ro-bind <nodeRoot> /n --ro-bind <work>/c /c --ro-bind <mirror> /r ... --chdir /h /n/bin/node ...`.
   - `kumitate-shokunin/.ufo/waves/round-44/controls/SentinelSandboxEscape.md:14` — `/proc/1/environ` exposes 263 launcher variables, including credential-like names; `/proc/1/cmdline` and mountinfo expose host bind paths.
   - `kumitate-shokunin/.ufo/waves/round-44/controls/CtlEnvArgvCwd.md` — all 87 cases report the same fingerprint, PID 2, PPID 1, uid/gid 1000, cwd `/h`, root `/r`, hostname `plazir27`; no case-specific identity leaked.
   - `kumitate-shokunin/.ufo/waves/round-44/probe/p44b-count.mjs` (counter source, rev 292d9266) — `runCase()` builds the bwrap argv; work directory is `run-<pid>-<hex>`; census and work paths are job-specific on the host but are not mounted under those labels.

4. Other sibling lanes:
   - `kaidoku-shokunin/.ufo/waves/round-20/w1/ConnSandboxPatterns.md` — catalogues bwrap, `unshare`, and `systemd-run` usage; its conclusion is that write/net refusal comes from bwrap, not from `systemd-run` or a bare tmpfs.
   - No other sibling lane in the searched set runs candidate code under bwrap with a job label in the sandbox argv or environment. Most lanes run candidate code unsandboxed or under `unshare`/`systemd-run`.

## Pattern assessment

- Worth reporting to sibling lanes: yes. The reusable, non-obvious part is the combination of generic mount point plus per-job directory plus no job label in argv/env. It directly addresses the kumitate r44 lesson that label-keyed programs can meet a counter.
- Not yet worth reporting as a complete solution: no. The same bwrap invocation still exposes `/proc/1/environ` and `/proc/1/cmdline`/mountinfo. Those are host-path and secret-disclosure defects, not case labels, but they are real boundaries.
- Tameshi v4 is already better than kumitate r44 on job identity because its temp directory is `w...`, not the seat name, and `name` is not passed to the sandbox. The remaining gap is environmental, not nominal.

## Smallest safe correction (report-only recommendation)

1. Add `--as-pid-1` to `BWRAP` in `c1-measure-v4.py`, as the tameshi sentinel already verified.
2. Spawn bwrap with `env={'PATH': '/usr/bin:/bin'}` (or equivalent) so PID 1 cannot inherit launcher secrets.
3. Keep `/w` as the only job-specific bind and continue to remove the per-job directory after each run.
4. Report the same two changes to kumitate r44's p44b-count.mjs `runCase()`; do not change its frozen counter semantics or case generation.
5. Do not remove procfs without checking the runner's `/dev/fd` process-substitution use.

## Risks

- `--as-pid-1` changes PID 1 behavior and must be tested against the runner's process substitution.
- Restricting the spawn environment could hide variables the runner expects; only PATH, HOME, LANG, and TMPDIR are documented as needed.
- Reporting is not fixing: sibling lanes retain authority over their own frozen counters.

## Verification

- Tameshi sentinel: `.ufo/waves/round-30/wA/SentinelBwrap.md` (scratch probes, no production change).
- Kumitate sentinel: `kumitate-shokunin/.ufo/waves/round-44/controls/SentinelSandboxEscape.md` and `CtlEnvArgvCwd.md`.
- Source lines cited above were read directly. No gate, selftest, sweep, or build was run by this seat.
