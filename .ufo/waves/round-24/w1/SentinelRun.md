# SentinelRun — `registry-replay.py --run` static review

**Verdict: material containment and data-exposure defects found.** The selected revision's runner and command rows execute with host access; the “private clone” is not a write sandbox. The output-size check is post-capture, and the output path is not symlink-safe. Static review only: no replay, runner, gate, or selftest was executed.

## Findings

### High — row commands can mutate live siblings (and other host paths)

**Exploit path:** A caller replays a revision whose row command writes to `../<sibling-shokunin>/...` from the clone, or to an absolute host path. The temporary `fleet` contains symlinks to the real sibling repositories; row execution uses the clone as cwd but does not sandbox filesystem access. Relative sibling traversal is not caught by the runner's absolute-argv check. An `external` row with an absolute fleet path is also still executed: it is marked non-hermetic, not refused.

**Evidence:** `tools/registry-replay.py:149-170` creates the temporary clone, symlinks each real sibling at lines 160-161, and calls `run_row` with the clone cwd at lines 167-170. `tools/registry-check.py:632-671` checks only absolute argv tokens; `external` bypasses the refusal at lines 662-671. `tools/registry-check.py:676-684` launches the row with `cwd=cwd` and no filesystem isolation. The checked-in registry already declares an external row using `/home/vgpnk/Projects/shokunin` (`tools/registry.json:107-129`).

**Impact:** A replay can modify or delete data in live sibling repositories despite its throwaway clone and can write anywhere the invoking user can access. `live_dependent` is a reporting label, not a containment control.

**Smallest safe correction:** Do not link live siblings into the replay fleet. If sibling access is required, provide immutable/read-only snapshots inside a real OS sandbox; otherwise fail closed for non-hermetic rows. Do not describe the clone as write-isolated.

### High — selected revision code runs with the caller's authority and secrets

**Exploit path:** Point `--rev` at an untrusted or compromised commit. `registry-replay.py` imports that revision's `tools/registry-check.py` into the replay process, executing its module code in-process, then runs its registered programs. Neither path has a privilege or filesystem boundary. The runner environment is inherited wholesale except for `GIT_*`; therefore any set credentials or agent handles (for example `AWS_*`, `GH_TOKEN`, `SSH_AUTH_SOCK`, or proxy variables) are available to row code.

**Evidence:** `tools/registry-replay.py:162-170` hashes and imports the clone's runner before invoking it. `tools/registry-replay.py:57-60` removes only `GIT_*`. `tools/registry-check.py:149-174` likewise builds the row environment from every inherited non-`GIT_*` variable, and `tools/registry-check.py:676-684` passes it to the child process.

**Impact:** A revision under test can read credentials, use the caller's network/agent access, or directly alter caller-readable/writable files. The `GIT_*` filter is not a general secret scrub or sandbox.

**Smallest safe correction:** Treat `--rev` as code execution. For untrusted revisions, run both the imported runner and rows in an OS-isolated, least-privileged environment with no host secrets/network and an explicit minimal environment allowlist. If that is not provided, state and enforce a trusted-revision-only boundary.

### High (conditional on a pre-existing symlink in `--out`) — output writes follow symlinks

**Exploit path:** Pre-create `--out/observations.json` as a symlink to a writable file outside the output directory, then invoke `--run`. The unconditional observations write follows that symlink. A symlinked `--out` directory likewise redirects all output. Bundle/expected/live-dependent writes also follow pre-existing leaf symlinks on successful projection.

**Evidence:** `tools/registry-replay.py:181-185` creates the requested directory and unconditionally calls `write_bytes` for `observations.json`; `tools/registry-replay.py:116-127` writes the remaining artifacts with the same follow-symlink behavior. No realpath, no-follow open, or trusted-directory check is present.

**Impact:** Arbitrary overwrite of files writable by the replay process, contradicting the “writes only under --out” claim (`tools/registry-replay.py:18-20`).

**Smallest safe correction:** Require a trusted non-symlink output directory and create/write files relative to a directory fd with no-follow semantics (or safely write temporary files and atomically replace leaf names); reject symlinked output leaves.

### High — stream limit is post-hoc; full, potentially secret output is persisted

**Exploit path:** A row prints an arbitrarily large stream or emits credentials. The runner's `communicate()` buffers the complete stdout/stderr, and `retain_streams=True` keeps both complete decoded streams. Replay writes those streams to `observations.json` before calling `project()`, where `--max-stream-bytes` is checked. A limit violation refuses bundle publication but does not bound capture or remove the already-written observations.

**Evidence:** `tools/registry-check.py:648-649, 693-726` captures via `communicate()` and retains complete stdout/stderr when requested. `tools/registry-replay.py:167-184` requests retention, embeds results in `rows`, writes `observations.json` at line 183, and only then calls `project` at line 184. The cap check is `project` lines 92-98; `DEFAULT_MAX` is 1 MiB at line 43.

**Impact:** Memory/disk exhaustion from large output; secrets in stdout/stderr are stored unredacted in `observations.json` and, on success, `bundle.json`. Output file modes are left to the caller's umask, so local readability is not constrained here.

**Smallest safe correction:** Enforce a byte bound while draining output, not after `communicate()`; retain only bounded/redacted excerpts (or avoid retaining streams by default) and ensure output files use restrictive permissions. Keep a truncation/limit finding so a truncated stream cannot be treated as a complete receipt.

### Medium — interruption can bypass row cleanup

**Exploit path:** Send SIGTERM to the replay process, or interrupt it while a row is running. The child starts a separate session, but cleanup is reached only after `communicate()` returns or raises `TimeoutExpired`; there is no `finally`/signal cleanup around the wait. The row can outlive the replay command and continue accessing host paths.

**Evidence:** `tools/registry-check.py:672-684` starts the child with `start_new_session=True`; cleanup appears on the normal/timeout paths at `tools/registry-check.py:693-716`, with no enclosing cleanup guard in `run_row:648-733`. `tools/registry-replay.py:167-175` calls this directly.

**Impact:** Orphaned commands may continue writing after the replay exits, including through the live-sibling links while the temporary fleet remains available.

**Smallest safe correction:** Put child cleanup in a `finally`/signal-safe lifecycle, terminate and reap the tracked row process tree before allowing replay teardown, and preserve cleanup failure in the result.

## Scope / evidence

Reviewed `tools/registry-replay.py`, the called `tools/registry-check.py` runner paths, and relevant `tools/registry.json` rows with read-only source inspection. No commands were executed and no production files were changed; this report is the only written file.