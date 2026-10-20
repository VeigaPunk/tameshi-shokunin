# PinSelftest — read-only review, round 13 (wave tameshi-r13-w1)

Seat: `TameshiR13.PinSelftest` (reviewer). Advisory; no verdict authority. Static review only: no checks, tests, builds or gates were run. No files were edited.

## 1. Current state (after second landing)

- `tools/pin-disposition.py` (1247 lines): 18 selftest arms declared; `PinProbe.md` table (lines 119-156) lists 18 with expected `SELFTEST: PASS (18/18)`.
- Static review of the landed code only. Not executed.

## 2. Status of earlier findings

| ID | Finding | Status | Anchor |
|---|---|---|---|
| F-A | `mismatch` rows dropped `pinned.reason` | **Resolved.** `reason` is copied whenever status != verified, so `pinned_blob_mismatch` is emitted. | `pinned_observation` `:309-310`; arm `pinned-blob-mismatch` `:1035-1053`, fixture `:805-809` |
| F-B | Documented branches without an arm | **Resolved for the four named branches.** New arms cover `pinned-blob-mismatch`, `worktree-outside-repo`, `worktree-symlink`, `repo-symlink`. | arms `:1035-1123`; fixture mutation/restore `:1055-1124` |
| F-C | `dirty-worktree` shares the `changed` literal | Noted; unchanged. The arm asserts HEAD == pin, so it is not vacuous. | `:933-949` |

Pre-landing items 1-8 remain resolved as stated in my previous report.

## 3. Review of the new arms (static)

- **pinned-blob-mismatch:** `digest-mismatch` manifest sets `js-kimi-census` expected digest to V2. Observed blob at the pinned commit is V1. Code path: `:302-308` gives `status=mismatch`, reason `pinned_blob_mismatch`; `:309-310` copies it. Worktree is V1 but unverified, so content `unavailable` and worktree reason `pin_not_verified` (`evaluate_leg` path). Consistent with the assertions.
- **worktree-outside-repo:** `kumitate/scripts` is renamed to `.real` and replaced by a symlink to a temp directory. `lstat(repo/scripts/kimi-census.mjs)` follows the directory symlink and returns a regular file, so `S_ISREG` passes. The `realpath().startswith(repo_real + os.sep)` check at `:371-373` then returns `worktree_outside_repo`. Assertions match. Directory is restored at `:1080-1081`.
- **worktree-symlink:** `kimi-census.mjs` is replaced by a relative symlink. `lstat` returns `S_ISLNK` and `:365-367` returns `worktree_symlink`. Restored at `:1103-1104`.
- **repo-symlink:** `fleet/mado-shokunin` is replaced by a symlink to kumitate. `repo_identity` `lstat` gives `S_ISLNK` and returns `repo_symlink` (`:248-249`) before the toplevel check, so the symlink is not followed. Removed at `:1124`.

Arms run after all byte-comparison arms, and each mutation is reverted before the next arm. The ordering is correct.

## 4. Residual coverage gaps (low, not blocking)

- `worktree_not_regular`, `repo_not_directory`, `worktree_replaced`, `pinned_read_failed` and `head_read_failed` have no arm. They are reachable in code but not asserted.
- Fixture mutations at `:1055-1124` are not wrapped in try/finally. On an exception mid-arm, the `/tmp` scratch root is kept (the FAIL path already keeps it), so this affects only diagnostics.

## 5. Exact checks L1 should run (not run here)

1. `python3 -m py_compile /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py; echo exit=$?` → exit 0.
2. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py --selftest; echo exit=$?` → exit 0; 18 `SELFTEST_CASE … PASS` lines; `SELFTEST: PASS (18/18)`.
3. Discriminator for F-A: the `pinned-blob-mismatch` arm must FAIL on the pre-fix code and PASS on the current code.
4. Real-root read: `python3 .../pin-disposition.py --manifest .../.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin; echo exit=$?` → exit 0, six rows, `result_reuse=not_established` on every row. Expected content from read-only facts: kimi, tsukuroi, mado `changed`; surface, checklist, claims `unchanged`.
5. Sibling no-write: `git -C <kumitate|kagi|tsukuroi|mado> status --short` before and after steps 2-4 must be identical.
6. Scope: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --short` shows only owned paths and round-13 directories.

## 6. Tooling record

No tools installed or upgraded. Read-only source reads only.

## 7. Limits

- Not executed; the 18/18 claim is unverified by me.
- Symlink, outside-repo and mismatch behaviour is from code reading only.
