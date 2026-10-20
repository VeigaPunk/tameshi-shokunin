# X06PinBranchTip — pin-disposition.py branch-tip observation (staged)

## Files changed
- `.ufo/waves/round-17/staged/tools/pin-disposition.py` (staged copy of committed
  `tools/pin-disposition.py` at lane tip 98bea7da5801f4bc58e4187690ee1687c8a5061f)

## Behavior
- `head_observation` no longer reads `<HEAD-commit>:<path>`. New `detect_branch`
  mirrors `scripts/hyaku/jj-lane.sh` `detect_branch` (:53-65), read-only:
  attached `HEAD` short name → `symbolic-ref refs/remotes/origin/HEAD` branch →
  `refs/heads/master` → `refs/heads/main` → first `for-each-ref refs/heads/`
  entry. The blob observation then reads `refs/heads/<branch>^{commit}:<path>`.
- `head` row gains: `branch` (resolved name, `null` when no local branch
  exists — then `commit` falls back to raw HEAD), `commit` = branch tip,
  `head_differs_from_branch` (`null` when `branch` is `null`). The repo-missing
  placeholder row carries the same shape. Docstring, plumbing list
  (`symbolic-ref`, `show-ref`, `for-each-ref` added) and VERSION updated to r17.
- New selftest case `detached-head-uses-branch-tip`: `mado-shokunin` fixture on
  `master` (V1 bytes), HEAD detached one commit ahead with V2 bytes;
  asserts `branch=master`, `commit=master_tip`, `blob_sha256=V1`,
  `head_differs_from_branch=true`.

## Evidence
- Before: committed tool `python3 tools/pin-disposition.py --selftest` →
  `SELFTEST: PASS (18/18)`, exit 0.
- After: staged tool `--selftest` → `SELFTEST: PASS (19/19)`, exit 0;
  `detached-head-uses-branch-tip PASS (exit=0 expects=0 14 literal checks)`.
- Red-before on the new fixture (isolated `/tmp` repo, detached HEAD one
  commit ahead of master with different bytes), calling `head_observation`
  directly on committed vs staged source:
  - OLD `{"commit": "e340acb2…detached", "blob_sha256": "d459d283…(V2)"}`
  - NEW `{"branch": "master", "commit": "26ad9a2c…master_tip",
    "blob_sha256": "0b09cbb5…(V1)", "head_differs_from_branch": true}`
  → committed tool observed HEAD's bytes; staged observes master's bytes.
- Live run: `python3 <tool> --manifest .ufo/evidence/round-13/pin-manifest.json
  --root /home/vgpnk/Projects/shokunin`, both exit 0. Recursive field-by-field
  diff (ignoring `tool`, `tool_sha256`, `observed_at`): 12 diffs total, all
  additions — each of the 6 legs gains `head.branch="master"` and
  `head.head_differs_from_branch=false`. No existing field changed value.
  Cross-check: `git symbolic-ref` shows kumitate/kagi/tsukuroi attached to
  `master`, mado detached with `origin/HEAD→refs/remotes/origin/master`;
  HEAD == master tip in all four (`head_differs_from_branch=false` correct).
- Evidence basis honored: JjAuditTameshi.md §1.2 (:317 row), §2.3, §5 R2 —
  jj colocated detached HEAD was borrowing the working-copy commit; the
  observation now reports the lane branch tip.

## Risks / notes
- `head.commit` semantics change from "raw HEAD" to "branch tip"; consumers
  diffing on that field see a value change only when HEAD diverges from the
  tip (no value change in the live run above). `head_differs_from_branch`
  preserves the divergence signal the raw-HEAD value used to imply.
- Repo with zero local branches: `branch=null`, `commit`=raw HEAD,
  `head_differs_from_branch=null` (probe degrades instead of failing).
- Installs: none (stdlib + git only).

## Verdict
built
