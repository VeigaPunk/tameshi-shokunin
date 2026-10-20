# GateSecurity — round-12 w1 — repeat-control design boundary (sentinel, read-only on production)

Seat: GateSecurity (sentinel, leaf). This review is advisory and stays inside the lane. It is not an independent non-author promotion, admission or pass.

## Scope and basis

- Target: the contract for `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` (`.ufo/waves/round-12/spec.json` `context`; the ControlGate item at `spec.json:10`).
- `tools/repeat-control.py` was **absent** both times I checked (glob `tools/*` → only `mutate-and-run.sh`; `.ufo/evidence/round-12/ControlGate/` did not exist). I reviewed the **contract** plus the stdlib behaviour a straightforward Python implementation would inherit. **I ran no gate and claim no pass.**
- I followed the precedent in `tools/mutate-and-run.sh`. Lines 391-399 run the suite through `bash -c` with stdin `</dev/null`, under `timeout "$TIMEOUT_S"` (default 300 at :166). Line 33 maps exit 124/126/127 to INCONCLUSIVE.
- Evidence probes are hermetic fixtures under `mktemp` `/tmp/tameshi-r12-gatesec.*`. Interpreter: Python 3.14.7. Repo HEAD: `18ad5d0`.
  - `.ufo/evidence/round-12/GateSecurity/probes.py` (sha256 `4dda972f…a5b`)
  - `.ufo/evidence/round-12/GateSecurity/probes.out` (sha256 `40a8a066…b76`, probe exit 0)
  - `.ufo/evidence/round-12/GateSecurity/tty_probe.py` / `tty_probe.out`: **no result.** No pty was available, so the tty path was not exercised.
- Reproduce: `python3 .ufo/evidence/round-12/GateSecurity/probes.py`.
- Exit precedence (`[0,1,0]` and so on) belongs to ExitReview (`ExitReview.md` H1/M1/M2/M4). I do not repeat it here. I only add exec-failure cases that ExitReview does not cover.
- Tools installed or updated: **none**. I read `/home/vgpnk/.omp/agent/RULES.md`, and nothing needed installing.

## Findings (severity · exploit path · evidence · impact · smallest remediation)

### A. argv vs shell

**A1 — HIGH — `argparse.REMAINDER` keeps the `--` separator, so every valid call executes `--`.**
- Path: `--runs 3 --out d -- echo hi`.
- Evidence (P2): `cmd=['--', 'echo', '--out', 'x']`. On 3.14.7 the leading `--` is kept in the REMAINDER list.
- Impact: argv[0] becomes `--`, which raises ENOENT. Every valid invocation would then report `command_unavailable` (exit 2), and the selftest's stable arm would be wrong for every input.
- Remediation: split `sys.argv` by hand at the first literal `--` and take the command as everything after it. Do not let argparse own the command tail. An empty tail exits 64.

**A2 — MEDIUM — the `--` separator can be skipped, and argparse accepts option prefixes.**
- Evidence: (P2) `--runs 3 --out d echo --runs 9` parses as `cmd=['echo','--runs','9']`. (P1c) `--ru 3` is accepted as `--runs`.
- Impact: a command whose own arguments look like gate options becomes ambiguous. The contract writes `--` as part of the interface.
- Remediation: require the literal `--` (exit 64 without it). Use `allow_abbrev=False`, or no argparse for the gate head.

**A3 — LOW (correctness, if violated) — shell joining changes the command.**
- Evidence (P12): argv `printf '%s|' 'a b' '$HOME' '*'` prints `a b|$HOME|*|`. The same argv joined into a string and run with `shell=True` prints `b''`, because `|` became a pipe.
- Remediation: run `subprocess.run(argv_list, shell=False, stdin=DEVNULL)` with the list unchanged. Never `" ".join`.

### B. Child-process failures

**B1 — HIGH — any uncaught exception exits 1, which is `controls_mismatch` ("failed").**
- Evidence (P4a/P4b): an uncaught `FileNotFoundError` exits 1, and an uncaught `json` decode error exits 1.
- Impact: any crash in the gate (exec error, unreadable snapshot, full disk on `--out`) shows up as a determinism failure in the exit-only class. That is a fabricated verdict.
- Remediation: one top-level `except BaseException` that maps to exit 2 with a could-not-evaluate ID (or 64 for usage). The gate's exit must only ever come from its own map (agrees with ExitReview M4).

**B2 — HIGH — the exec-failure set is wider than `FileNotFoundError`/`PermissionError`.**
- Evidence (P5): with `shell=False` on this host:

| case | observed |
|---|---|
| missing binary | `FileNotFoundError` errno 2 |
| file not executable | `PermissionError` errno 13 |
| executable with no shebang | **plain `OSError` errno 8 (ENOEXEC)** |
| a directory as the command | `PermissionError` 13 |
| empty argv0 `""` | `PermissionError` 13 |

- Exploit: `-- ./script-without-shebang`. An implementation that catches only the two subclasses crashes, and per B1 reports exit 1 "failed".
- Remediation: catch `OSError` around `Popen`/`run` and map it to `command_unavailable`, exit 2.

**B3 — MEDIUM — the command can disappear partway through the series.**
- Evidence (P5m): a self-deleting script gives runs `[0, FileNotFoundError, FileNotFoundError]`.
- Impact: the contract has no ID for "run 1 executed, run 2 could not". If unhandled, this is B1. If handled per-run, there are no stdout/stderr/exit files for runs 2-3.
- Remediation: any exec error on any run gives `command_unavailable` exit 2 (ExitReview M1.3 makes the same recommendation). Record which run failed.

**B4 — LOW (documentation) — wrapper exit codes and signal deaths.**
- Evidence: (P5w) `-- env nosuch` exits 127, which becomes `baseline_nonzero`, not `command_unavailable`. (P6) a child killed by SIGKILL has `returncode=-9`; the shell form would be 137.
- Impact: two IDs for one cause, depending on whether a wrapper is used. The value saved in the exit file differs between the Python form and the shell form.
- Remediation: state the saved exit format, e.g. Python's signed `returncode`, written as decimal plus LF. Do not map 126/127 (ExitReview M2).

### C. Timeout, interrupt, and leftover processes

**C1 — HIGH — a background grandchild that keeps the output pipe open blocks the gate.**
- Evidence (P7a): `sh -c 'sleep 4 & echo hi'`, run with `capture_output` and no timeout, returned after **4.0s**. The direct child exited at once.
- Impact: a command that leaves a daemon or background job blocks the gate for that process's whole lifetime, possibly forever. The contract has no timeout, so this means no verdict at all.
- With a `timeout`, 3.14.7 returned promptly (P7b, 1.0s), but the grandchild was left running.

**C2 — HIGH — leftover writers change evidence after a run counts as finished.**
- Evidence (P8): run with stdout redirected to a file. The file held `b'hi\n'` when the run ended and `b'hi\nlate\n'` 1.5s later.
- Impact: run *k*'s leftover process writes into run-*k*'s file (or the shared tree) during run *k+1* or after comparison. The result is a false `controls_mismatch`, or committed evidence that no longer matches its digests.
- Remediation for C1+C2 together: write stdout/stderr straight to the numbered files (no in-memory pipes, which also removes memory blow-up on large output). Use `start_new_session=True` and, after each `wait()`, `os.killpg(pgid, SIGKILL)`. That is per-run cleanup only, not extra hardening. Compute digests only after the group kill.

**C3 — MEDIUM — no timeout ID exists, and an external `timeout` lands in the wrong class.**
- Path: the caller adds `-- timeout 10 cmd`. A hang on run 2 exits 124, which per contract is `controls_mismatch` exit 1 ("failed").
- Conflict: in `mutate-and-run.sh:33,57-58`, 124 is INCONCLUSIVE.
- Other path: the caller wraps the gate itself (`timeout 60 python3 tools/repeat-control.py …`). That exits 124, which is outside the 0/1/2/64 map, and leaves `--out` partly written.
- Remediation (smallest; L1 decides): either state "no timeout; a hang is no verdict" in the registry row, or add `--timeout S` with a contract ID in the could-not-evaluate class. Do not invent an undeclared ID.

**C4 — MEDIUM — an interrupt leaves a partly written `--out`.**
- Evidence (P4c): an uncaught `KeyboardInterrupt` gives `returncode=-2` (130 in the shell), outside the exit map.
- Impact: the run directory holds run-1 and run-2 files and no verdict. A consumer or `--snapshot` that only checks the files present can treat it as complete (see E2).
- Remediation: write the verdict/manifest last via temp file plus `os.replace`. `--snapshot` refuses any directory without it. On `KeyboardInterrupt`, kill the child group (C2).

**C5 — not observed: a command that reads the tty.**
- [INFERENCE] `stdin=DEVNULL` does not stop a child from opening `/dev/tty` (password prompts, `read </dev/tty`) when the gate runs in a terminal, so the gate would hang waiting for input. `start_new_session=True` (C2's fix) removes the controlling tty.
- P15 could not test this: no pty in this harness, and `tty_probe.out` records that.

### D. Output-path clobbering

**D1 — HIGH — a reused `--out` follows planted symlinks and overwrites files outside the run directory.**
- Evidence (P10a): with `DIR/run-1.stdout -> victim` planted, `open(...,'wb')` overwrote the victim with `'gate bytes\n'`. (P10b) `open(...,'xb')` refused with `FileExistsError`.
- Impact: running in a reused or attacker-staged `--out` overwrites any file the user can write.
- Remediation: create `--out` with `os.mkdir` and refuse if it exists (P10c), with exit 64. Open each file with `'xb'`.

**D2 — HIGH (if implemented) — clearing `--out` with `rmtree` is catastrophic.**
- Path: `--out .`, `--out ~`, or `--out corpus` combined with a "clean the output directory first" rmtree deletes the repo or home directory.
- Remediation: never delete a path the caller supplied. D1's refusal makes deletion unnecessary.

**D3 — MEDIUM — stale files in a reused `--out` mix two runs' evidence.**
- Evidence (P10d): a leftover `run-4.stdout` and `verdict.json` sit next to a new `--runs 3` set.
- Impact: the snapshot inventory includes stale runs, or a stale verdict is read as current.
- Remediation: D1's refusal.

**D4 — HIGH — `--out` inside the tree the command inspects makes a pristine command mismatch with itself.**
- Evidence (P11): a deterministic `find . -type f` in a cwd that contains `--out` gave **3 different stdouts in 3 runs**, because run *k* sees the files written by runs 1..k-1.
- Exploit path: this lane's own convention puts `--out` at `.ufo/evidence/round-12/<seat>/` inside the repo. A repo-scanning control (a census-style gate, `git status --porcelain`, `find`) run from the repo root therefore gets `controls_mismatch` from the gate's own writes. That is a fabricated "failed" verdict.
- Remediation: write runs to a scratch `--out` outside the observed tree, e.g. `mktemp -d`, then copy into `.ufo/evidence` after the verdict (QUALITY.md:24-25, criterion 9 already calls for scratch-then-copy). State this in the registry row. The selftest could add one `--out`-outside arm; L1 decides.

**D5 — LOW — secrets in persisted evidence.**
- Saved stdout/stderr and recorded argv go into repo evidence paths. A command that prints the environment or takes a token argument stores them.
- Remediation: state in the registry row that saved files are committed evidence. No extra hardening is requested.

**D6 — LOW — `--runs` parsing is too lenient.**
- Evidence (P3): `int()` accepts `' 3 '`, `'+3'`, `'3_0'` (=30) and the Arabic-Indic digit `'\u0663'` (=3).
- Impact: low, but a "stable usage contract" accepts surprising spellings. An unbounded `--runs` also lets one call write an unbounded number of files.
- Remediation: `re.fullmatch(r'[0-9]+', s)`, then `>= 3`. Anything else exits 64.

**D7 — comparison must use bytes.**
- Evidence (P9): `filecmp.cmp(a,b)` with the default `shallow=True` returned **True** for `AAAA` vs `BBBB` with the same size and mtime. `shallow=False` returned False.
- Impact: fast runs within mtime granularity produce a false `controls_match`, i.e. a fabricated clean verdict. **Severity: HIGH if used.**
- Remediation: compare `read_bytes()` directly or by full sha256.

### E. Snapshot digest validation

**E1 — CRITICAL (if implemented) — `--snapshot` must never execute anything taken from snapshot data.**
- Path: a snapshot manifest that records `argv` is edited to `["sh","-c","…"]`. A validator that "re-runs to confirm" runs an arbitrary command.
- Remediation: `--snapshot` only reads: it hashes files and recomputes the finding from the stored files. No `subprocess` call is reachable from that mode. Selftest or L1 can confirm by grep.

**E2 — HIGH — digests stored inside the same directory are self-referential.**
- Evidence (P14): when a run file and its manifest digest are edited together, the in-directory digest check still passes (`True`).
- Impact: the "tamper → `snapshot_tampered`" claim only covers edits that forget to update the manifest.
- Remediation: anchor the expected digests outside the directory under test:
  - Option (a): read the committed blobs and manifest from the git object store (`git show HEAD:<path>`), which is the precedent at `mutate-and-run.sh:98-103`, and compare the working tree against them.
  - Option (b): pin the manifest's own sha256 in a second committed location (e.g. ControlGate's `expected.json`).
  - Otherwise, state the limit: the check catches accidental drift, not deliberate coordinated edits.

**E3 — HIGH — manifest file names can escape `DIR`.**
- Evidence (P13): `os.path.join('SNAP','/etc/hostname')` gives `/etc/hostname`. `'../outside'` normalizes to a sibling of SNAP. Git can commit a symlink `run-1.stdout -> /etc/hostname`, and `open()` follows it (P13s).
- Impact: the tool reads, and acts as a digest oracle for, files outside the snapshot. This brushes against "no secret content reads".
- Remediation: names must `fullmatch` a fixed grammar (e.g. `run-[1-9][0-9]*\.(stdout|stderr|exit)` plus the manifest name). Use `os.lstat`, reject anything that is not a regular file, and refuse if `realpath` leaves `DIR`.

**E4 — MEDIUM — the snapshot's file set must match exactly, and every malformation must count as tampering, not a crash.**
- Path 1: an extra unlisted `run-4.stdout`, or a run count different from the `runs` field, slips through a subset check.
- Path 2: a missing file, malformed JSON, a missing digest key, or a non-hex digest raises → exit 1 (B1, P4b).
- Remediation: require `set(listdir) == set(manifest) ∪ {manifest}`. Any parse or shape error gives `snapshot_tampered` exit 2. Compare full lowercase 64-hex digests with `==`, never a prefix.

**E5 — MEDIUM — the expected ID/exit must be recomputed, not trusted.**
- `--snapshot` should recompute the finding from the stored stdout/stderr/exit bytes and require it to equal the recorded expected ID and exit. Otherwise an edited `expected` field alone passes.
- Overlap: ExitReview H2 and SnapshotReview. Here this is only the security side: without the recomputation the recorded ID is just an assertion.

## Smallest remediation set

This is not a request for unrelated hardening. Each item closes one finding above.

1. Split argv by hand at the first `--`, with exit 64 when it is missing or the command is empty. Reject options without the `--`, and require `--runs` to be ASCII digits and `>= 3` (A1, A2, D6).
2. `shell=False`, list argv, `stdin=DEVNULL`, stdout/stderr written straight to `'xb'` files in a fresh `os.mkdir` `--out` (A3, C1, D1, D3).
3. `start_new_session=True` plus `killpg` after each run (C1, C2, C5).
4. `OSError` on any run gives `command_unavailable` 2. A top-level catch-all gives a mapped could-not-evaluate result and never Python's default exit 1 (B1-B3).
5. Compare bytes or full sha256, never `filecmp` with shallow (D7).
6. Write the verdict/manifest last and atomically (C4).
7. Snapshot mode never runs anything; it validates a strict name grammar, regular files only, exact set equality, and a digest anchor outside `DIR` (or states the limit); every malformation gives `snapshot_tampered` 2; the finding is recomputed (E1-E5).
8. Contract or registry text from L1: timeout policy (C3), keeping `--out` outside the observed tree (D4), the saved exit format (B4), and that saved evidence is committed (D5).

## Checks L1 can run once `tools/repeat-control.py` lands

These are suggestions. I have not run them and no output is claimed.

- `python3 tools/repeat-control.py --runs 3 --out "$(mktemp -u)" -- echo hi` → `controls_match` 0. Catches A1.
- `--runs 3 --out D echo hi` (no `--`) → 64. `--runs ' 3'` and `--runs 2` → 64. `--help` → state its class explicitly.
- `--out D -- ./noshebang`, where the file is mode 755 and holds `echo hi` with no `#!` → `command_unavailable` 2, not exit 1 (B2).
- A self-deleting script → `command_unavailable` 2 (B3).
- `mkdir D; ln -s /tmp/victim D/run-1.stdout; … --out D …` → 64, and the victim is unchanged (D1).
- `-- sh -c 'echo hi; (sleep 2; echo late) &'` → exits within about a second with `controls_match`, and the run files do not change 3s later (C1, C2).
- From the repo root, `--out .ufo/evidence/x -- git status --porcelain` → shows the D4 self-mismatch. That is a documented limitation, not a gate bug.
- `--snapshot` on a copy where the manifest names `../x` or `/etc/hostname`, contains a symlinked run file, has an extra `run-4.stdout`, or holds truncated JSON → each gives `snapshot_tampered` 2 with no traceback. Separately, `grep -n subprocess` limited to the snapshot code path finds nothing reachable (E1, E3, E4).

## Exact owned paths (written by this seat)

- `.ufo/waves/round-12/w1/GateSecurity.md` (this report)
- `.ufo/evidence/round-12/GateSecurity/probes.py`, `probes.out`
- `.ufo/evidence/round-12/GateSecurity/tty_probe.py`, `tty_probe.out`

No production file, no file owned by another seat, and no fleet path was written. No commits. Scratch left at `/tmp/tameshi-r12-gatesec.3jjxrxn9`. One coordination message went to `ControlGate` with the top risks (A1, B1, B2, D7, D1, E1, E3, E2).

## Remaining risk

All findings are against the contract plus stdlib behaviour, because the implementation did not exist at review time. The risks marked "if implemented" (D2, D7, E1) apply only if the implementer takes that route. C5 is not observed. Every severity here is this seat's judgment and inside the lane only.
