# RerunPinBranch — round 17 wave 2, FALSIFY

Seat scope: re-run the two pin-disposition discriminator checks at the landing
rev, run the same jj fixture against the pre-fix tool, and compare the two live
reads field by field. No subagent dispatch; no lane writes outside this report.

Clone: `W=/tmp/tameshi-r17w2-RerunPinBranch-5P1D75`, `C=$W/fleet/tameshi-shokunin`
(fleet-mirror symlinks + `git clone` + `git checkout --detach eb7838b1…`).
Clone stayed clean at `eb7838b16490ca7ba17ea3242ade76a61f744af2`
(`git status --porcelain` empty after all runs).

Artifacts under test (lane-relative, digest at the landing rev):

| path | mode/blob | sha256 |
|---|---|---|
| `tools/pin-disposition.py` | 100755, blob `89a6ca3` | `331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c` |
| `.ufo/evidence/round-17/jj/head-vs-branch.sh` | 100755, blob `369469d` | `15d4fdfb543e8e48f5633b306ba933b8a9078b515365f68a34ac096cc16db0e1` |
| `.ufo/evidence/round-13/pin-manifest.json` | unchanged between `98bea7d` and `eb7838b` | `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` |
| pre-fix tool at `98bea7da5801f4bc58e4187690ee1687c8a5061f:tools/pin-disposition.py` | blob `6339347` | `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` |

## Commands, exits, key output

1. **Selftest, landing rev** — `cd $C && python3 tools/pin-disposition.py --selftest`
   → **exit 0**, `SELFTEST: PASS (19/19)`. All 19 `SELFTEST_CASE … PASS` lines;
   the claimed number is exact (`19/19`, not "about 19"). The added case is
   `detached-head-uses-branch-tip` (`tools/pin-disposition.py:1299`), which builds
   a detached commit one ahead of `master` (`:1273-1315`) and asserts
   `head.branch=master`, `head.commit=master_tip`, `head.blob_sha256=V1`,
   `head_differs_from_branch=true`, `detached != master_tip`, `worktree.sha256=V2`.

2. **jj fixture, landing tool** —
   `cd $C && bash .ufo/evidence/round-17/jj/head-vs-branch.sh $C/tools/pin-disposition.py`
   → **exit 0**. Key lines:
   ```
   FIXTURE head_detached=c7a5451… (master..HEAD = 1, symbolic-ref HEAD = detached)
   OBSERVED head.commit=6fdb355deb2594facbc7abfc61f41b42a399ab9e head.status=present head.blob_sha256=78e89b5b…
   OBSERVED pinned.commit=6fdb355d… worktree.sha256=a0b7c69a…
   VERDICT: head observation used master's tip (6fdb355d…, v1 bytes) — branch-safe
   ```
   `head.commit` equals the `master` tip, `head.blob_sha256` equals the v1
   (master) blob, `worktree.sha256` equals the v2 (detached-only) bytes.

3. **Same fixture, pre-fix tool (98bea7d)** —
   `bash .ufo/evidence/round-17/jj/head-vs-branch.sh <old>/pin-disposition.py`
   → **exit 1**, as the claim states:
   ```
   OBSERVED head.commit=13b9a623… head.status=present head.blob_sha256=a0b7c69a…
   VERDICT: head observation used detached HEAD (13b9a623…, v2 bytes) — jj @- snapshot reported as repo head
   ```
   The pre-fix tool reports the detached jj-snapshot commit and the v2 blob as
   the repo head; the landing tool reports the branch tip and the v1 blob. The
   fixture discriminates the two tools exactly as stated.

4. **Pre-fix selftest control** — `python3 <old>/pin-disposition.py --selftest`
   → exit 0, `SELFTEST: PASS (18/18)`. The 19th case is new; the 18 pre-existing
   cases still pass in both tools.

5. **Live read, landing tool** — exact form from the clone:
   `cd $C && python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
   → **exit 0**, `status=ok`, `counts={"legs":6,"unchanged":3,"changed":3,"unavailable":0}`.
   Rows: `bash-surface-census` and `bash-checklist-run` unchanged,
   `js-kimi-census`/`bash-tsukuroi-census`/`bash-mado-verify` changed,
   `js-claims-check` unchanged — all six `pinned.status=verified`,
   every `result_reuse=not_established`.

6. **Live read, pre-fix tool** — same argv with the `98bea7d` tool → **exit 0**,
   same counts and same six rows.

## Field-by-field live comparison (landing vs 98bea7d)

Diff computed by loading both JSON documents and walking every key; results:

- **Top-level**: only `tool` (`pin-disposition.py r13…` → `r17…`) and
  `tool_sha256` (`2972539…` → `331529e…`) differ. `schema`, `manifest`, `root`,
  `status`, `counts`, `observed_at`, `result_reuse`, `result_reuse_reason`, and
  `not_compared` are value-identical (the two runs happened in the same UTC
  second, `2026-10-20T16:03:37Z`).
- **Per-leg `pinned`**: identical for all six rows (commit, expected/blob digest,
  `status=verified`, `reason=null`).
- **Per-leg `worktree`**: identical (path, sha256, `status`, `reason`);
  `content_status` identical.
- **Per-leg `head`**: every pre-existing key (`commit`, `blob_sha256`, `status`,
  `reason`) identical on all six rows; the landing document **adds**
  `head.branch="master"` and `head.head_differs_from_branch=false` on every row
  (`tools/pin-disposition.py:374-433`). No pre-existing field changed value.
- Net: the live read is a strict superset on this fleet; the new capability
  only shows up where raw HEAD != branch tip, which the live fleet does not
  have (see residual risk).

## Deeper checks (what the claims rest on)

- **`detect_branch` mirror claim** (`tools/pin-disposition.py:324-372`,
  docstring cites `scripts/hyaku/jj-lane.sh:53-65`): verified against the fleet
  root's **committed** blob (`git show HEAD:scripts/hyaku/jj-lane.sh`,
  sha256 `2479041653c6a77c6cca099a37948d6c16361173c68fb14c8c2e2feae9dc2b1d`):
  `detect_branch` is exactly lines 53-65, and its order (attached short name →
  `refs/remotes/origin/HEAD` → `master` → `main` → first local branch) matches
  the tool's `symbolic-ref -q --short HEAD` → `symbolic-ref -q
  refs/remotes/origin/HEAD` → `show-ref master` → `show-ref main` →
  `for-each-ref refs/heads/` order.
- **Branch-resolution fallbacks, probed directly** with three hand-built
  fleets (manifest = the canonical six legs, one leg exercised):
  - only `trunk`, detached: `head.branch=trunk`, `head.commit`=trunk tip,
    `status=present`;
  - only `main`, detached: `head.branch=main`, `status=present`;
  - `origin/HEAD → origin/release` (no local `release`) with local `master`
    present, detached: `head.branch=release`, `head.commit=null`,
    `status=unavailable`, `reason=branch_tip_missing`, exit 0.
  All three match the documented order; the third is a documented degradation
  (reason surfaced, not a silent wrong value).
- **Tool `GIT_*` scrub claim** (`tools/pin-disposition.py:207-222`,
  "Inherited GIT_* variables are scrubbed"): ran the live read with
  `env GIT_DIR=<tmp victim>/.git`; output identical to the clean run after
  dropping `observed_at`. Scrub verified empirically.
- **Selftest hermeticity**: the selftest's `git()` helper passes a filtered
  `env` (`tools/pin-disposition.py:751`, `:780-787`) and `HOME=<scratch>`;
  no fleet/sibling repo path is referenced.

## Findings

### Blocking

None.

### Minor

1. **`head-vs-branch.sh` heredoc claim of `GIT_*` hermeticity is false; the
   fixture writes into an inherited `GIT_DIR`.** Comment at
   `.ufo/evidence/round-17/jj/head-vs-branch.sh:79-80`: "no host hooks,
   templates, global/system config, or inherited GIT_* state leaks into the
   fixture repo." The export block at `:81-83` sets only `GIT_CONFIG_NOSYSTEM`,
   `GIT_CONFIG_GLOBAL`, `GIT_TERMINAL_PROMPT` and author/committer; it never
   unsets `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`,
   `GIT_COMMON_DIR`. Demonstration (all paths under `/tmp`, lane clone
   unaffected):
   ```
   env GIT_DIR=$VICTIM/.git bash .ufo/evidence/round-17/jj/head-vs-branch.sh $C/tools/pin-disposition.py
   → exit 2 (SETUP-FAIL: head.commit=null …)
   victim log: 5731c70 jj working-copy snapshot (@- emulation)
               555ee55 v1: master tip
               309d69e victim base
   victim status: " D corpus/surface-census.sh", "?? v.txt"
   ```
   i.e. both fixture setup commits landed in the inherited `GIT_DIR` and its
   index/worktree were clobbered, before `SETUP-FAIL`. This is the exact
   wave-1 clobber vector (contract: never export `GIT_DIR`); the fixture cannot
   produce a false 0/1 under it (it exits 2), but it does write outside its own
   `$SCRATCH`. Fix: unset the six vars next to the existing export block (or
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE …` on the fixture's git
   calls). Severity: minor for verdict integrity, medium for harness hygiene.

2. **Fixture pass criterion is `head.commit` only.** `head-vs-branch.sh:187-190`
   returns 0 solely on `HEAD_COMMIT == MASTER_TIP` (and 1 on
   `== HEAD_DETACHED`). It prints but never asserts `head.status=present`,
   `head.blob_sha256 = v1_sha`, `worktree.sha256 = v2_sha`, or
   `head.branch=master` (all present in the tool's output at `:374-433`). A
   future tool that reported the branch-tip commit but hashed the *HEAD* blob
   would pass this fixture. Non-blocking: the tool's own selftest asserts
   `head.blob_sha256` and `worktree.sha256` (`tools/pin-disposition.py:1309`,
   `:1312`), so the composite evidence still pins the bytes; tightening the
   fixture would make it self-sufficient.

3. **Selftest does not cover the remaining `detect_branch` paths.** Only
   attached HEAD and detached-with-local-`master` are exercised
   (`tools/pin-disposition.py:1273-1315`). The `origin/HEAD`, `main`-only,
   first-local-branch and no-branch raw-HEAD fallbacks are untested (I probed
   them manually above; all behave as documented). Calibration note, not a
   defect in the claim under test.

### Observation (external, not a lane defect)

- The fleet root's working tree has an **uncommitted** `scripts/hyaku/jj-lane.sh`
  (`git -C /home/vgpnk/Projects/shokunin status --porcelain` → ` M`; sha256
  `3369dc27…` vs committed `24790416…`): that variant moves `detect_branch` to
  lines 115-126 with only attached + `origin/HEAD` and relocates the
  master/main fallback into `lane_branch` (gated on exactly one candidate).
  The tool's `:53-65` citation is accurate to the committed fleet HEAD; if the
  working-tree edit lands, the citation and the "mirror" claim would drift.
  [INFERENCE] The edit predates/postdates this lane's work; I did not touch it.

## Residual risk

- The live read cannot discriminate old vs new by value: all six live legs'
  repos resolve to the master tip (`kumitate`, `kagi`, `tsukuroi` attached on
  `master`; `mado` is **detached at exactly `refs/heads/master`**), so
  `head_differs_from_branch=false` everywhere and both tools emit the same
  `head.commit`. The old/new difference is demonstrated only by the fixture and
  the selftest, which both do so unambiguously.
- When `origin/HEAD` names a branch that does not exist locally, the new tool
  degrades to `head.status=unavailable`/`branch_tip_missing` where the old tool
  reported raw HEAD (`detect_branch` order is deliberate; reason is explicit
  and exit stays 0). No live leg hits this.
- A tool that moved the branch-tip commit but kept the HEAD blob would pass
  `head-vs-branch.sh` (finding 2); only combined with the selftest is byte
  identity pinned.

## Verification gaps

- Did not run `tools/registry-check.py`, `measure.py` or `tools/evidence-disposition.py`
  (other seats); the "every baseline row holds / round-14 command superseded"
  half of C2 is out of this seat's scope.
- Did not reproduce with a real `jj`-colocated repo; the fixture emulates the
  observable git state (`master..HEAD = 1`, detached HEAD, HEAD blob = v2),
  which is the state the tool consumes.
- The `GIT_DIR` hazard was demonstrated against a `/tmp` victim repo; the lane
  clone is unchanged (`rev-parse HEAD` = `eb7838b…`, clean status).

## Verdict

**Holds:** at `eb7838b1…` the tool is `19/19` selftest-green and the jj fixture
flips from red on the `98bea7d` tool (exit 1, detached snapshot reported as
head) to green on the landing tool (exit 0, master-tip commit and v1 blob),
while the live read is identical to the pre-fix tool except the two added
`head.branch`/`head_differs_from_branch` fields — the only defect found is the
fixture's unfulfilled claim that it isolates inherited `GIT_*` (it commits into
an inherited `GIT_DIR` before exiting 2).

No tool installs or updates were performed.
