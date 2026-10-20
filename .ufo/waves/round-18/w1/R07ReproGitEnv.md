# R07 — P11 GIT environment reproduction at base

## Finding

P11 is **open** at base `183f87b899e6cae46be98d251cbc87fb5118f6ca`: `bash-witness-study.py declare` inherits `GIT_DIR`/`GIT_WORK_TREE`, and its `git show` runs against the `/tmp` canary instead of the isolated kagi checkout. The canary lacks the pinned revision, so the command fails there. No tested git subprocess targeted a real repository.

## Evidence

- Created the lane clone at `/tmp/tameshi-r18w1-R07ReproGitEnv-axHTrT/fleet/tameshi-shokunin`; `git rev-parse HEAD` returned the requested base revision.
- Read CLI help first: `python3 tools/bash-witness-study.py --help` exited 0 and listed `declare` and `selftest`. Then `python3 tools/bash-witness-study.py selftest` exited 0: `WITNESS_SELFTEST: 41/41 pass`, `VERDICT: PASS`.
- Source path: `tools/bash-witness-study.py:332-344` defines `materialize_target()` and runs `subprocess.run(["git", "-C", str(kagi), "show", "--end-of-options", f"{rev}:{TARGET_GIT_PATH}"])` without an explicit subprocess environment. Its caller `cmd_declare()` obtains the pinned revision and invokes it at `:836-857`. The base runner pins `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e` at `tools/mutate-and-run.sh:594-595`.
- Prepared an independent kagi clone and canary under the same `/tmp` scratch directory. The independent kagi copy returned the pinned target with SHA-256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` (matching `PIN_BASH` at `tools/mutate-and-run.sh:594`). The canary's own commit was `d099946de9e2298a8c4756460480de58c767ab1d` and had only `marker.txt`.
- Clean control invocation, from the base lane clone:

  ```sh
  W=/tmp/tameshi-r18w1-R07ReproGitEnv-axHTrT
  cd "$W/fleet/tameshi-shokunin"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
    python3 tools/bash-witness-study.py --evidence "$W/control-evidence" --kagi "$W/kagi" declare
  ```

  Exit 0; output included `WITNESS_DECLARE: target sha256=275d8294... (pin 275d8294...)`.
- P11 invocation (same clone and isolated `--kagi`; only the requested GIT_DIR/GIT_WORK_TREE are set; Trace2 records the actual child git process):

  ```sh
  W=/tmp/tameshi-r18w1-R07ReproGitEnv-axHTrT
  cd "$W/fleet/tameshi-shokunin"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
    GIT_DIR="$W/canary/.git" GIT_WORK_TREE="$W/canary" \
    GIT_TRACE2_EVENT="$W/p11-trace.json" \
    python3 tools/bash-witness-study.py --evidence "$W/p11-evidence" --kagi "$W/kagi" declare
  ```

  Exit 2. Output: `WITNESS_STUDY: CANNOT-EVALUATE (git show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh failed: fatal: path 'corpus/surface-census.sh' exists on disk, but not in 'fecee8743e52eb8fb5fbb40782934cb619a1a96e')`.
- Actual child trace at `/tmp/tameshi-r18w1-R07ReproGitEnv-axHTrT/p11-trace.json`: line 2 records `git -C /tmp/.../kagi show ...`; line 4 records `"worktree":"/tmp/.../canary"`; lines 6-7 record the error and Git exit 128. As an additional route check, the same GIT_DIR/GIT_WORK_TREE with `git -C "$W/kagi" rev-parse --git-dir --show-toplevel HEAD` returned `$W/canary/.git`, `$W/canary`, and canary HEAD `d099946...`.

The clean control confirms the fixture revision and path are valid in the isolated kagi clone. The instrumented failure and Trace2 worktree establish that the tool's git subprocess honored the exported canary environment; it did not read from the real sibling or lane repository. The original sibling was used only as the read-only source for making the independent `/tmp/kagi` clone, with GIT variables scrubbed; all test commands and writes were in `/tmp`.

## Residual risk / verification gap

No LSP device/server route was exposed in this session, so the source references are textual (`read`/search), not LSP semantic checks. The execution trace and clean control directly establish the scoped runtime behavior; no broader caller review was attempted.

**Verdict: falls — P11 is open at base; the actual `git show` resolved to the `/tmp` canary and failed there.**
