# PinGit — read-only review: pin-disposition git subprocess construction

Seat: TameshiR13.PinGit (reviewer, leaf). Read-only. No checks, builds, or edits run. Installs: none.

## Scope state at review time

- `tools/pin-disposition.py` does **not** exist. `git status --short` at tameshi root shows only `?? .ufo/waves/round-13/`. `tools/` holds `bash-witness-study.py`, `mutate-and-run.sh`, `repeat-control.py` (all committed at 546b371). No implementation to review yet; findings below are pre-implementation requirements grounded in existing code and live git probes.
- Owning executor: `TameshiR13.PinProbe` (dispatch.json:232, spec.json:10). Findings sent to `agent://TameshiR13.PinProbe`.

## Observations (live read-only git probes)

1. **Fleet root is a git repo; non-repo sibling directories resolve to it.** `git -C /home/vgpnk/Projects/shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin` (HEAD `a53aad8`). `git -C reports rev-parse --show-toplevel` → the fleet root, exit 0. `git -C reports cat-file -e HEAD:AXES.md` → exit 0. So a pin repo directory that exists without its own `.git` silently reads the fleet-root object store. Sibling repos with their own `.git` resolve correctly (kumitate `1770305`, kagi `c2cab35`, tsukuroi `9574a18`, mado `95cbc41`).
2. **Missing directory is exit 128, not a missing blob.** `git -C /home/vgpnk/Projects/shokunin/does-not-exist rev-parse HEAD` → `fatal: cannot change to …`, exit 128.
3. **Exit codes do not separate missing path from missing rev.** In tameshi: `git cat-file -e HEAD:no/such` → 128. `git show HEAD:no/such` → 128. `git show 0000…:LOG.md` → 128 with "exists on disk, but not in '0000…'". `git rev-parse --verify --quiet 0000…^{commit}` → exit 1, silent. Classification must come from pre-checks (`rev-parse --verify --quiet <rev>^{commit}`, then `cat-file -t <rev>:<path>`), not from one exit code.
4. **`git show rev:<dir>` succeeds with a tree listing.** `git cat-file -t HEAD:tools` → `tree`; `git show HEAD:tools` → listing, exit 0. A pin path that names a directory or symlink would hash the wrong bytes unless type is checked (`cat-file -t` == `blob`; `ls-tree` mode for 120000 symlinks).
5. **Env inheritance.** Current shell has `GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT` only; no `GIT_DIR`/`GIT_WORK_TREE`. A caller that exports `GIT_DIR` would override `git -C` silently.
6. **Existing argv pattern (reference, committed).** `tools/bash-witness-study.py:332-344` validates rev with `re.fullmatch(r"[0-9a-f]{40}")`, checks `.git`/`.jj` existence, uses list argv, and passes `--end-of-options` before `rev:path`. This is the pattern to copy.
7. **Existing shell runner has weaker classification.** `tools/mutate-and-run.sh:919-951` (`regression_case`) uses `git -C "$repo"` with `rev-parse --verify`, `cat-file -e`, `show`, `ls-tree`. It has no `--end-of-options`, no 40-hex check, no repo-toplevel check, and no blob-type check. Its failures are all SETUP (fail-closed, rc 2), so the risk is a wrong-repo read in case (1), not a false PASS. Out of scope to edit; cite only.
8. **Working-tree side.** `git show` yields blob bytes without worktree filters or smudge. A worktree comparison must read the file's raw bytes and compare sha256 to `git show HEAD:path`. Do not use `git diff --quiet` as the disposition signal; it misses cases where the path is deleted or untracked. Worktree `FileNotFoundError` is a distinct state from blob-missing.

## Findings for the owning executor (PinProbe), by severity

- **P1 (wrong-repo silent read).** Before any `git -C <repo>` call, require `git -C <repo> rev-parse --show-toplevel` to equal `<repo>` (resolved). Otherwise classify `repo-not-a-git-repo`. Evidence: observation 1.
- **P1 (rev/path classification).** Pre-check `rev-parse --verify --quiet <rev>^{commit}` (→ `rev-missing`), then `cat-file -t <rev>:<path>` (→ `path-missing` on 128, `not-blob` unless `blob`). Do not map any single exit code to one category. Evidence: observations 3–4.
- **P2 (argv hardening).** Use list argv, validate `rev` as `[0-9a-f]{40}`, pass `--end-of-options` before `rev:path`. Evidence: observation 6.
- **P2 (env scrub).** Build the subprocess env without `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`. Evidence: observation 5.
- **P2 (repo mapping).** Map each leg to its own repo directory (top path component, as `mutate-and-run.sh:1112-1140` does: `kumitate-shokunin/...`, `kagi-shokunin/...`), never to the fleet root. The fleet root has its own HEAD and would not contain these pins. Evidence: observation 1.
- **P3 (worktree).** Read worktree bytes raw; map `FileNotFoundError` to `worktree-missing`, distinct from `blob-missing`. Evidence: observation 8.

## Checks L1 should run after the implementation lands (not run here)

1. `git -C /home/vgpnk/Projects/shokunin/reports rev-parse --show-toplevel` → expect the tool to refuse this dir as a repo (`repo-not-a-git-repo`), not to resolve the fleet root.
2. Fixture: `repo` pointing to a non-repo dir with a path that exists in the fleet root (e.g. `AXES.md`) → must not PASS.
3. Fixture: `rev` = `0000…` → `rev-missing`; real commit + absent path → `path-missing`; path naming `tools` → `not-blob`.
4. Fixture: rev with leading `-` or non-40-hex → refuse before subprocess.
5. Run with `GIT_DIR` exported to a different repo → output must not change.
6. Worktree arm: deleted worktree file → `worktree-missing`; modified file → `dirty` with HEAD sha ≠ worktree sha; identical bytes → `current`.
7. Inspect source for `shell=True`, `os.system`, or `sh -c` in subprocess calls (none expected).

## Residual risk / verification gaps

- No implementation existed at review time; all findings are pre-implementation. Re-check against the landed file.
- Not tested: `safe.directory`/dubious-ownership exit 128 path (cannot be reproduced read-only). Classify it as `git-unusable`, not `path-missing`.
- Not checked: `.gitattributes` filters/eol in the six pin repos (`git check-attr`). Matters only for the worktree arm.
- Existing `mutate-and-run.sh` weaknesses (observation 7) are cited, not reviewed as defects of this round.

## Verdict

Non-blocking for the owning executor; no implementation defect can be confirmed because no implementation file is on disk. Priority if the implementation lands unchanged: P1 items 1–2.
