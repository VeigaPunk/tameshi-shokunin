# ExecEmptyPanelReplay — r37 C1 replay input (calibration)

**Seat:** `L1-tameshi-r37-attempt2.ExecEmptyPanelReplay` (executor, leaf)
**Milestone:** Replay input. **Judged on:** calibration.
**Scope:** run the committed empty-panel replay adapter in a separate worktree against the frozen
source/counter revision and the frozen manifest revision; record v1/v2 labels, exit codes, tree
identities, and whether any input path falls outside the lane object database.
No counter, contract, tool, receipt or panel byte was edited. No tool install/update performed.

## Environment (observed, not assumed)

| item | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/tameshi-shokunin` |
| lane HEAD at read time | `e6185d5f0b63a6963205110cb098f2f1eca27622` (detached) |
| lane branch `master` | also contains `e6185d5` |
| separate worktree | `/tmp/tameshi-r37-w1-execpanel` |
| worktree registration | `git worktree add --detach <path> e6185d5…` → `HEAD is now at e6185d5` |
| worktree HEAD / base | `e6185d5f0b63a6963205110cb098f2f1eca27622`, `rev-parse --abbrev-ref HEAD` = `HEAD`, clean (0 dirty paths) |
| live checkout | never written except this report; `git status --porcelain` shows only untracked sibling wave reports under `.ufo/waves/round-37/w1/` (23 at check time, all `??`) plus this report; HEAD unchanged `e6185d5` |
| scratch work roots | `/tmp/tameshi-r37-w1-execpanel-workroot`, `…-workroot2` (write-only, fresh) |

Disclosure: `git worktree add` registers `.git/worktrees/tameshi-r37-w1-execpanel` (additive
metadata only). No object, ref, index, jj state, or working-tree byte of the lane was mutated.
Two pre-existing worktrees were already registered in this lane before my run
(`/fast/scratch/hyaku/s3-ready66/tameshi-shokunin`, `/fast/scratch/hyaku/tameshi-r25-author`)
plus one sibling r37 worktree (`/tmp/tameshi-r37-exec-codeview`).

## Frozen revisions used (from `contract.json:frozen_control_input` and the manifest)

| role | revision | provenance |
|---|---|---|
| source / counter revision | `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` | `contract.json` `frozen_control_input.source_revision`; `manifest.json:source_revision`; `counter_rev=` in receipts |
| manifest / panel revision | `c2b08d70427921998677c780930c448a4ecefcf1` | commit `round-37: freeze claims and empty-panel input`; carries `panel_rev=` in the committed receipts |
| manifest revision ancestry | `merge-base --is-ancestor c2b08d7 e6185d5` → exit 0 | required by `calibration/measure.py:receipt_ok` |
| prior unreachable mutant | `91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` | `git cat-file -e` exit 1; `git cat-file -t` → `could not get object info` |

Manifest blob `.ufo/evidence/round-37/control/empty-panel/manifest.json` is **identical** at
`c2b08d7` and `e6185d5` (`dce2e57c9c1372c8f1e9991afb63b4b386d90a9d`), so the panel revision is not
sensitive to choosing either commit; `c2b08d7` is the freeze commit and was used.

## Exact command (committed adapter, unmodified)

Adapter identity: worktree file `.ufo/evidence/round-37/control/replay-empty-panel.py`,
sha256 `f5b30f06d0b8b4d87d6322ca2d22b2895efadf06c20ad865dbbe9f8e234b46af`, identical to
`git show e6185d5:.ufo/evidence/round-37/control/replay-empty-panel.py` (blob `bade1d8e`).

```
cd /tmp/tameshi-r37-w1-execpanel
python3 .ufo/evidence/round-37/control/replay-empty-panel.py \
  --lane /tmp/tameshi-r37-w1-execpanel \
  --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d \
  --panel-rev c2b08d70427921998677c780930c448a4ecefcf1 \
  --work-root /tmp/tameshi-r37-w1-execpanel-workroot
```

### Result

```
ADAPTER_EXIT=0
stderr: empty (e3b0c442…, zero bytes)
COUNTER_SOURCE v1 sha256=d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3
C1_R35_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R35_CONTROL_PASS=true
COUNTER_SOURCE v2 sha256=9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53
C1_R36V2_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R36V2_CONTROL_PASS=false
EMPTY_PANEL_REPLAY: source_tree=4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e source_specimens=9 empty_specimens=0 counter_rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d panel_rev=c2b08d70427921998677c780930c448a4ecefcf1 v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true
```

Full retained stdout (identical in both runs; `COPY` rows are the sealed-set copies, `div=` is the
observed/expected divergence shape, `rc` the mutant-tool exit):

```
COPY accept accept-trailing-comments           accept-trailing-comments.json div=- rc=0 checks=- pass=True
COPY kill  cfg00-setup-as-pass                cfg00-setup-as-pass.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-workdir-wording              cfg11-workdir-wording.json div=(1,1) rc=1 checks=runtime pass=True
COPY accept comment-head-comment-quoted-legnames comment-head-comment-quoted-legnames.json div=- rc=0 checks=- pass=True
COPY accept inert-heredoc-apostrophe-comment   inert-heredoc-apostrophe-comment.json div=- rc=0 checks=- pass=True
COPY kill  workdir-branch-keep-swap           workdir-branch-keep-swap.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-keep-cleanup-nested-config workdir-keep-cleanup-nested-config.json div=(1,1) rc=1 checks=runtime pass=True
```
(each block of 7 repeats once under `COUNTER_SOURCE v1` and once under `COUNTER_SOURCE v2`.)

**Retained stdout is byte-identical to the committed receipt** that
`calibration/measure.py` reads (`REPLAY_RECEIPT = .ufo/evidence/round-37/control/replay-at-final-control.stdout`):

```
sha256(/tmp/tameshi-r37-w1-execpanel.stdout)          = 8468af55fd66afb83d0b191f7a56b6b06c21273fb4a5982c85ff1136068ca57b
sha256(replay-at-final-control.stdout)                 = 8468af55fd66afb83d0b191f7a56b6b06c21273fb4a5982c85ff1136068ca57b
diff → IDENTICAL
```

## v1/v2 labels and exit codes

| counter | label | printed verdict | counter rc | basis |
|---|---|---|---|---|
| v1 (`round-35/c1/c1-measure.py`) | `C1_R35_CONTROL` | `C1_R35_CONTROL_PASS=true` | **0** | adapter predicate requires `results["v1"][0] == 0` (`replay-empty-panel.py:146`) |
| v2 (`round-36/c1/c1-measure-v2.py`) | `C1_R36V2_CONTROL` | `C1_R36V2_CONTROL_PASS=false` | **1** | adapter predicate requires `results["v2"][0] == 1` (`replay-empty-panel.py:149`) |
| adapter aggregate | — | `EMPTY_PANEL_REPLAY_PASS=true` | **0** | `ok = v1_ok and v2_ok` (`:153-155`); exit 0 iff ok (`return 0 if ok else 1`) |

Counter rcs are enforced, not printed, by the adapter; because `EMPTY_PANEL_REPLAY_PASS=true` was
emitted, both `v1_ok` and `v2_ok` held, hence rc(v1)=0 and rc(v2)=1 exactly as tabulated.
Why v2 rejects on the same run that v1 passes: v1 compares counts only to the manifest's own slots
(`c1-measure.py:519-522`, so 0/0 is vacuous), while v2 freezes `PUB_KILL_SLOTS_TARGET=6`,
`PUB_ACCEPT_SLOTS_TARGET=3`, `PUB_DISTINCT_TARGET=9` and requires slot counts to equal them
(`c1-measure-v2.py:68-70,538-545`). The empty panel reports `pub_kill=0/0 pub_accept=0/0
pub_slots=0 pub_distinct=0`, so v2's `pub_kill_slots == 6` arm fails → `_PASS=false`, rc 1. This is
the intended v1 PASS / v2 FAIL control.

## Tree and byte identities

| identity | value |
|---|---|
| source panel tree, manifest and `git rev-parse d9c496b:.ufo/evidence/round-35/c1/panel` | `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e` |
| source specimen count at `d9c496b` (adapter `ls-tree`) | 9, names equal manifest `source_specimens` |
| empty-panel tree at `c2b08d7` (and at `e6185d5`) | `50e588b6f53b479b71a828c3e3c9cbb1743ae56c` |
| empty-panel entries at `c2b08d7` | exactly `.ufo/evidence/round-37/control/empty-panel/manifest.json` (0 specimens) |
| manifest blob | `dce2e57c9c1372c8f1e9991afb63b4b386d90a9d` |
| adapter blob / sha256 | `bade1d8e…` / `f5b30f06d0b8b4d87d6322ca2d22b2895efadf06c20ad865dbbe9f8e234b46af` |
| counter v1 blob / sha256 | `ede608ea229bd84c1e8e85b72671b637120c0490` / `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3` |
| counter v2 blob / sha256 | `5f1c2047ce533182a8938cb2b44d73938a54c153` / `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` |
| tool at `d9c496b` (frozen pin) | `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354` |
| tool at `e6185d5` (live HEAD, post-C2) | `da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede` |

The replay reads the tool at `--rev` (`replay-empty-panel.py:90-95`), and `d9c496b` still carries
the frozen `6188db16…` bytes, so the control receipts are unaffected by the current tool bytes.
`--tool tools/tally-audit-v3.py` is lane-relative and resolved from git at `REV`
(`c1-measure.py:440-446`, `c1-measure-v2.py:457-462`).

## Does any input path fall outside the lane object database?

**No — measured, not inferred.** Every lane input resolves as a Git object; the working tree is
never consulted for panel, sealed, counter, runner, or tool bytes.

Enumerated inputs, each verified with `git cat-file -e <rev>:<path>` in the lane object database:

| input | rev | result |
|---|---|---|
| `.ufo/evidence/round-35/c1/c1-measure.py` | `d9c496b` | present (read via `git show`, `replay:103`) |
| `.ufo/evidence/round-36/c1/c1-measure-v2.py` | `d9c496b` | present (`replay:103`) |
| `tools/tally-audit-v3.py` | `d9c496b` | present (`replay:90`) |
| `tools/mutate-and-run.sh` | `d9c496b` | present (`c1-measure.py:422`, `v2:439`) |
| `.ufo/evidence/round-35/c1/sealed/manifest.json` + 7 specimens | `d9c496b` | present (8/8; read via `git_show`, `c1-measure.py:470-471`, `v2:487-488`) |
| `.ufo/evidence/round-35/c1/panel` tree + 9 specimens | `d9c496b` (redirected to `c2b08d7` empty panel) | present; `load_copies_rev` → `git ls-tree`/`git show` (`c1-measure.py:279-299`) |
| `.ufo/evidence/round-37/control/empty-panel/manifest.json` | `c2b08d7` | present (`replay:37-42`) |
| `.ufo/evidence/round-37/control/empty-panel/` listing | `c2b08d7` | exactly the manifest (`replay:85-88`) |
| `.ufo/evidence/round-35/contract.json` (freeze commit lookup) | `d9c496b` | present (`c1-measure.py:475-480`) |

`--sealed` is used only for path normalization (`sdir`/`srel`), then the copies and their manifest
are fetched with `git_show(lane, rev, …)` (`c1-measure.py:467-472`, `c1-measure-v2.py:484-490`);
`load_copies()` (the disk reader) has no call site in either `main`.

### Falsification: replay with the on-disk inputs deleted

Renamed `…/round-35/c1/sealed` and `…/round-35/c1/panel` out of the worktree, ran the same
command from `cwd=/tmp` with a fresh `--work-root`, then restored them (`git status` back to 0):

```
NO_DISK_ADAPTER_EXIT=0
C1_R35_CONTROL: … C1_R35_CONTROL_PASS=true
C1_R36V2_CONTROL: … C1_R36V2_CONTROL_PASS=false
EMPTY_PANEL_REPLAY: … v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true
stdout sha256 = 8468af55… (identical to the normal run; diff → IDENTICAL)
```

With the panel and sealed directories absent from disk and no repository cwd, the replay still
reproduced the receipt byte-for-byte. Only these are not lane-object inputs: the adapter script
itself (run from the worktree; digest equal to its committed blob), the `--work-root` scratch
directories (write-only), and host tooling (`git`, `python3`, `bash`, `mktemp` inside the committed
runner, which runs its mutants under `env -i … HOME/TMPDIR` sandboxes).

## Negative controls (setup gates fire; no false pass)

| control | exit | output |
|---|---|---|
| `--rev 91373d5…` (unreachable prior mutant) | 2 | `EMPTY_PANEL_REPLAY: SETUP tool_pin_mismatch=missing` |
| `--panel-rev d9c496b…` (no manifest there) | 2 | `EMPTY_PANEL_REPLAY: SETUP manifest_error=RuntimeError` |
| `--rev e6185d5…` (live HEAD, new tool bytes) | 2 | `EMPTY_PANEL_REPLAY: SETUP tool_pin_mismatch=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede` |

## Risks / notes (reported, not repaired — outside this item's predicate)

1. **Adapter `rev_unresolved` gate is dead for full 40-hex names.** On this git,
   `git rev-parse --verify 91373d5…` exits **0** (prints the name) and only
   `…^{commit}` exits 128; `git cat-file -e` exits 1. The adapter's first gate (`replay:53-57`)
   therefore does not reject a full-SHA non-existent revision; the run falls through to the tool
   read and fails as `SETUP tool_pin_mismatch=missing` (exit 2) instead of `SETUP rev_unresolved`.
   No false pass results (all later reads are object reads), but the diagnostic is mislabeled, and
   the calibration counter's own `cat-file -e` (`calibration/measure.py`, `OLD_MUTANT`) is the
   check that actually detects unreachability.
2. **Worktree metadata.** `git worktree add` wrote `.git/worktrees/tameshi-r37-w1-execpanel`; no
   refs, objects, index, or jj state changed. The evidence tree is retained at
   `/tmp/tameshi-r37-w1-execpanel` (detached at `e6185d5`, clean).
3. **Live checkout was not used as an input.** It stays at `e6185d5`; its concurrent untracked
   wave reports are sibling output, not mine. Only the assigned report file was written by me.
4. C2/tool-pin work is untouched here: the frozen `6188db16…` pin matched at `d9c496b`, while
   HEAD carries `da8c1ef4…`; this replay is independent of that pin state by construction.

## Verdict for this item

The committed empty-panel replay adapter, run from a separate detached worktree at observed base
`e6185d5`, against source/counter rev `d9c496b` and manifest rev `c2b08d7`, exits **0** with
`C1_R35_CONTROL_PASS=true` (rc 0) and `C1_R36V2_CONTROL_PASS=false` (rc 1), tree
`source_tree=4f3d8af5…`, `panel_rev=c2b08d7…`, `v1_pass=1 v2_reject=1
EMPTY_PANEL_REPLAY_PASS=true`, byte-identical to `replay-at-final-control.stdout`
(`8468af55…`), and every input path resolves inside the lane object database.
