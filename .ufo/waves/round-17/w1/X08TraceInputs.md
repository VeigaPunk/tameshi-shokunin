# X08TraceInputs — build `.ufo/evidence/round-17/coldread/trace-inputs.py`

## Files changed
- `.ufo/evidence/round-17/coldread/trace-inputs.py` (new, sole owned path). Python stdlib only.

## Behavior
Runs `ARGV` under `strace -f -qq -s 4096 -o <log> -e trace=open,openat,openat2,creat,execve,execveat,chdir,fchdir,fork,vfork,clone,clone3,dup,dup2,dup3,close`, passes the command's stdout/stderr through, writes `{"schema":"tameshi-trace-inputs-v1","argv","cwd","root","rev","exit","inputs","external"}`.

- `strace -y` support is probe-checked (`strace -y -e trace=none true`); host strace 7.2 supports it. With `-y`, `AT_FDCWD</cwd>`/dirfd annotations and return-fd `= 3</resolved/path>` provide per-pid cwd and kernel-resolved paths; without it a per-pid cwd map (chdir/fchdir, inherited across fork/clone) plus an fd table (open/dup/close) provide the resolution base, then `realpath` canonicalises.
- Recorded: successful opens of regular files realpath-resolved under `--root` → `inputs` (lane-relative, `.git/` excluded); resolved under `/home` outside root → `external` (abs paths); everything else dropped. `execve`'d files recorded like opens (script under root = input).
- Excluded: failed opens (`= -1`/`?`), `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND|O_TMPFILE` opens (so all `creat`), `O_DIRECTORY`, non-regular files, ` (deleted)` fd targets, pipe/socket annotations.
- Unfinished/resumed syscall lines are stitched per-pid (fragment or reprint styles both handled). `git rev-parse HEAD` of root → `rev` (null outside a repo). Exit codes: 0 traced (command exit in JSON), 2 strace-missing/setup, 64 usage (argparse subclass exits 64).

## Evidence
- `python3 trace-inputs.py --selftest` → `SELFTEST: 16/16` exit 0. Checks: python read, bash `source`, child `cd`+relative open, write-mode opens excluded (`open('w.txt','w')`, `open(...,'r+')`), `/home` external-only (tool source), non-`/home` outside file dropped, missing strace → 2 via `env={"PATH":"/nonexistent"}`, `.git/` excluded, symlink-in resolved to target, symlink-out not an input, failed open excluded, execve'd `./run.sh` input, `os.listdir` dir open excluded, `sys.exit(3)` → `"exit":3`, `rev:null` outside a git repo, `--cwd` honored.
- Acceptance trace (live lane, read-only command):
  `trace-inputs.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --out $W/t.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
  → tool exit 0; JSON `exit=2` (matches the recorded `expected_input_digest_mismatch` on tools/mutate-and-run.sh, same as `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt`); `rev=e16adb7d8f4f8756b6ece293fe4bfcb8c2a813e2`; 16 inputs including all four required: `tools/evidence-disposition.py`, `.ufo/evidence/round-14/dispositions.json`, `.ufo/evidence/round-13/expected.json`, `tools/mutate-and-run.sh`. `external` empty on this run.
- Exit codes observed: no-args→64, missing `--out`/argv→64, bad root→2.
- Notable during dev: `dup4` is not an x86-64 syscall; including it made strace reject the whole `-e trace=` spec → removed (dup/dup2/dup3 kept).

## Risks / limits
- `rev` is live `git rev-parse HEAD` of `--root` per contract; on the live lane today it is `e16adb7…`, not the dispatch tip — correct per spec, noted for graders.
- External bucket only counts files under realpath(`/home`); `/tmp`, `/usr`, `/etc` reads are dropped by design.
- Inputs hashed post-run; a file deleted before digest is dropped from the map (recorded only if still a regular file).
- If `-y` were absent the fd-table fallback covers dirfd-relative opens but not `AT_EMPTY_PATH` execveat edge; host has `-y` so untested path in practice [INFERENCE: fallback exercises only its cwd/chdir half in selftest].

No tools installed (strace 7.2, python3 already present). No blockers.

Verdict: built

## Follow-up

Read at the L1's direction: `K02InputCreditHoles.md` (holes 7–8), `K05SpotcheckCoverage.md` (H1), `S12StraceFeasibility.md` (§1 flag table, §3 cwd attribution), `S16SrcStrace.md`, `N01TraceGitSafety.md` (F4–F6, F11–F12), plus the two IRC addenda. Same owned path only; no staged copies needed (the file is evidence-new, not an installed instrument).

### Changes (all in `trace-inputs.py`, sha256 `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070`)
1. **Child env** (`scrubbed_env`): every `GIT_*` removed, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPYCACHEPREFIX=<workdir>/pycache` (outside root). Recorded as `env_overrides.{git_vars_removed,set}`. Fixes K02 hole 8 / K05 H1 / N01 F1: a lane-module import opens the `.py`, never credits a `__pycache__/.pyc`, and no stray `GIT_DIR` can rewrite another repo's index.
2. **Tracked-at-HEAD filter** (`repo_filter`): `git -C root ls-files -z --cached --full-name` intersected with HEAD (`--no-optional-locks`, scrubbed env). Untracked regular-file opens go to `untracked`; non-repo root → `tracked_filter:false`, `inputs` unfiltered. Added test-or-non-default overrides `--fleet-root`, `--live-lane`, `--home-prefix` (defaults are the contract constants).
3. **`live_lane_reads`**: opens under the live lane when `realpath(root) != realpath(lane)`, symlink-resolved, kept out of `external`.
4. **`--seccomp-bpf`** (plus `--kill-on-exit`, `--strings-in-hex=non-ascii`) used after a probe; probe chain falls back to `-y`-only, and a failed `-y` probe is exit 2 (N01 F4), not a silent downgrade. `-f`/`-y` kept; `-z` added.
5. **No writes inside root**: strace log, probes and pycache live in `mkdtemp` chosen from candidate dirs outside `realpath(root)`; `try/finally: shutil.rmtree` (N01 F12).
6. **Addendum 1**: exit 2 unless the first pid in the log has a successful execve/execveat (N01 F4); C-unescape of both quoted args and `-y` annotations (`\xNN`, octal, `\"`; greedy `<...>` annotation capture) so `héllo`, `we"ird`, `ang<le>` names survive (N01 F5); any path opened write-mode at any point is removed from every bucket (read-then-rewrite, N01 F5); `rev` only when `realpath(rev-parse --show-toplevel) == realpath(root)` else null with `rev_reason` (N01 F6); `external` restricted to fleet root minus `.git` components, other `/home` opens only counted in `dropped_home_count`, never hashed/named (N01 F11).
7. **Addendum 2**: selftest is location-independent — the external/live/home fixtures are built under a synthetic `--fleet-root`/`--live-lane`/`--home-prefix` under the test tmpdir. Observed from a `/tmp` copy of the tool (no `/home` dependency).

### Evidence (commands and exits)
All `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-17/coldread/trace-inputs.py ...`
- `--selftest` → `SELFTEST: 27/27`, exit 0 (1.30 s). Cases: python-read, bash-source, cd-relative, write-open-excluded, read-then-rewrite-excluded, fleet-external, live-lane-flagged, non-fleet-home-counted, non-home-outside-dropped, missing-strace-exit2, missing-command-exit2, dotgit-excluded, symlink-in-resolves, symlink-out-not-input, failed-open-excluded, execve-script-input, directory-open-excluded, command-exit-recorded, nongit-root-unfiltered, git-tracked-filter (`untracked.txt` excluded from `inputs`, in `untracked`; `rev`=fixture HEAD), subdir-root-rev-null (`repo_identity_mismatch`, filter still on), env-scrubbed (`GIT_DIR` absent from child `env`, recorded removed; both overrides present), double-import-keeps-py (`mod.py` in `inputs`, no `__pycache__` key), escaped-names-recorded (all three names), cwd-option-input, temp-workdirs-deleted, no-artifacts-inside-root.
- Same selftest from `cp trace-inputs.py $TMP/tool.py; python3 $TMP/tool.py --selftest` → `27/27`, exit 0 (addendum 2 proof).
- Acceptance trace on the live lane:
  `--root /home/vgpnk/Projects/shokunin/tameshi-shokunin --out $W/t.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
  → tool exit 0; JSON `exit=2` (same `expected_input_digest_mismatch` on tools/mutate-and-run.sh as `op1-redbefore-98bea7d.txt`), `rev=98bea7da5801f4bc58e4187690ee1687c8a5061f`, `rev_reason=null`, `tracked_filter=true`, `inputs`=16 including all four required (`tools/evidence-disposition.py`, `.ufo/evidence/round-14/dispositions.json`, `.ufo/evidence/round-13/expected.json`, `tools/mutate-and-run.sh`), `untracked={}`, `external=0`, `live_lane_reads=0`, `dropped_home_count=0`; `env_overrides.git_vars_removed=[GIT_EDITOR,GIT_PAGER,GIT_TERMINAL_PROMPT]`.
- Exit codes: no-args → 64; bad root → 2.
- Pre-fix leftovers: 175 `/tmp/trace-inputs-run-*` from the earlier build (newest 12:44:00, all predating the hardened build) removed with `find /tmp -maxdepth 1 -name 'trace-inputs-run-*' ! -newermt '2026-10-20 12:45:00' -exec rm -rf {} +`; after=0. The fixed tool leaves none (`temp-workdirs-deleted`).

### Remaining limits
- `PYTHONPYCACHEPREFIX` in the receipt names the deleted private workdir (ephemeral by design).
- `ls-files` is index-based; the addendum's named command is used verbatim. A dirty index could classify a staged-but-uncommitted path as tracked; `rev` remains HEAD and consumers compare digests at REV.
- Git-object reads (`.git/`) remain invisible; hole 6's rev-pinning limit unchanged.
- `dirty_inputs` (N01 F6's optional extra) not emitted: would need content hashes of every input at HEAD; digest mismatch already surfaces at measure.

Verdict: built (hardened)
