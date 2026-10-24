# MutatePanelContent — panel-content mutant (round 37, w1)

Verdict: **KILLED**. One specimen JSON added beside the empty-panel manifest is rejected
explicitly by the replay adapter (`SETUP mutant_tree_not_empty paths=2`, exit 2). The
adapter never reports zero specimens over a panel holding an extra file. The mutant is
caught by a pure path-set equality guard before any counter executes.

## Setup (no live-lane writes)

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, HEAD
  `e6185d5f0b63a6963205110cb098f2f1eca27622` (unchanged through the probe; lane index
  empty; empty-panel dir tree at HEAD `50e588b6f53b479b71a828c3e3c9cbb1743ae56c`).
- Scratch: fresh `git clone --no-hardlinks` of the lane into
  `/tmp/tameshi-r37-mut-panel`, working tree clean at HEAD. The lane was never used as
  the `--lane` argument. Scratch clone, mutant commit and work roots removed afterward.
- Detector: `.ufo/evidence/round-37/control/replay-empty-panel.py`. Guard under test:
  lines 85-89 —
  `git ls-tree -r --name-only <panel_rev> -- <empty-panel>` must equal exactly
  `[EMPTY_PANEL + "/manifest.json"]`, else
  `print("EMPTY_PANEL_REPLAY: SETUP mutant_tree_not_empty paths=%d")`, `return 2`.
- Frozen configuration used: `--rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d`
  (counter rev; this is the only revision where the wrapper's tool pin
  `6188db16de045f29...` matches) and `--panel-rev <panel commit>` varied by arm.
  The committed receipt `.ufo/evidence/round-37/control/replay-at-final-control.stdout`
  uses the same `counter_rev=d9c496b...` / `panel_rev=c2b08d70427921998677c780930c448a4ecefcf1`.

## Detector invocation (identical in all three arms)

```
python3 .ufo/evidence/round-37/control/replay-empty-panel.py \
  --lane /tmp/tameshi-r37-mut-panel \
  --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d \
  --panel-rev <panel commit> \
  --work-root <fresh empty dir>
```

## Arm 1 — pristine panel (`panel_rev=c2b08d7...`)

Exit 0; tail:

```
C1_R35_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R35_CONTROL_PASS=true
C1_R36V2_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R36V2_CONTROL_PASS=false
EMPTY_PANEL_REPLAY: source_tree=4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e source_specimens=9 empty_specimens=0 counter_rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d panel_rev=c2b08d70427921998677c780930c448a4ecefcf1 v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true
```

Full stdout `diff` against the committed `replay-at-final-control.stdout`: identical
(no diff lines). Baseline is green, so a failing mutant arm is a kill, not a baseline
artifact.

## Arm 2 — one specimen added beside the manifest

Mutant produced with plumbing on top of the committed panel revision (no checkout, no
lane index touched):

```
GIT_INDEX_FILE=/tmp/tameshi-r37-mut-index git read-tree c2b08d7...
blob=$(git hash-object -w /tmp/panel-mutant-specimen.json)      # eb04b5c9717b9ce03dd99c8a7c502c97c5cb6d57
GIT_INDEX_FILE=... git update-index --add --cacheinfo 100644,$blob,.ufo/evidence/round-37/control/empty-panel/mutant-specimen.json
tree=$(GIT_INDEX_FILE=... git write-tree)                       # 4fa038bbf0cdbadf0ff7c85ad778c8d51ecd8ab9
git commit-tree $tree -p c2b08d7... -m "probe: one specimen JSON beside empty-panel manifest"   # f091a574473dd1d1f4eedf9816b481f61f2396b5
```

Mutant bytes (valid JSON, same specimen shape as the public panel; sha256
`f249dcca6abafd73d8bce4060570277d756a2b972dffbbf79a4c4fea1a7f4a0b`):

```json
{
 "copies": [
  {
   "class": "mutant-panel-content",
   "set": "kill",
   "edits": [["  nfail=0\n", "  nfail=1\n", 1]]
  }
 ]
}
```

Panel contents at the mutant commit (`git ls-tree -r --name-only f091a57 -- .ufo/evidence/round-37/control/empty-panel`):

```
.ufo/evidence/round-37/control/empty-panel/manifest.json
.ufo/evidence/round-37/control/empty-panel/mutant-specimen.json
```

Manifest itself is byte-identical (sha256 `e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13`);
only the panel content changed.

Mutant run (`--panel-rev f091a574473dd1d1f4eedf9816b481f61f2396b5`, fresh work root):

```
EMPTY_PANEL_REPLAY: SETUP mutant_tree_not_empty paths=2
RC=2
```

No `COUNTER_SOURCE` line appears: the guard at line 85-89 fires before counter
loading, so the adapter fails explicitly rather than reporting a zero count.

## Arm 3 — restored bytes (`panel_rev=c2b08d7...` again)

Exit 0; final line:

```
EMPTY_PANEL_REPLAY: source_tree=4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e source_specimens=9 empty_specimens=0 counter_rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d panel_rev=c2b08d70427921998677c780930c448a4ecefcf1 v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true
```

Full stdout is byte-identical to the Arm 1 / committed receipt. Panel dir tree hash after
restore: `50e588b6f53b479b71a828c3e3c9cbb1743ae56c` (equals the before hash);
scratch working tree `git status --porcelain` returned 0 lines.

## Hash ledger

| point | object | hash |
|---|---|---|
| panel tree before | `c2b08d7:.../empty-panel` | `50e588b6f53b479b71a828c3e3c9cbb1743ae56c` |
| mutant panel tree | `f091a57:.../empty-panel` | `4fa038bbf0cdbadf0ff7c85ad778c8d51ecd8ab9` |
| mutant specimen blob | added file | `eb04b5c9717b9ce03dd99c8a7c502c97c5cb6d57` |
| manifest | unchanged both arms | `e0c06148c71e6c4f02fde85d04a0e9d6ca87f5862227f4cb11578497a945bd13` |
| panel tree after restore | `c2b08d7:.../empty-panel` | `50e588b6f53b479b71a828c3e3c9cbb1743ae56c` |
| lane HEAD before/after | commit | `e6185d5f0b63a6963205110cb098f2f1eca27622` |

## Verdict

**Killed.** The empty-panel specification is enforced structurally: any addition under
`.ufo/evidence/round-37/control/empty-panel` (recursively, since `ls-tree -r` is used)
makes the replay exit 2 with `mutant_tree_not_empty`. The adapter cannot silently read
zero specimens from a panel that gained content. The zero-specimen claim therefore
depends on the guard, not merely on the counters happening to read zero.

## Observations (adverse, not repaired here)

1. **Replay at HEAD is red for a non-panel reason.** Running the same adapter with
   `--rev e6185d5...` (HEAD, after the C2 tool edit) and default `--panel-rev` exits 2
   with
   `EMPTY_PANEL_REPLAY: SETUP tool_pin_mismatch=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`
   (guard at lines 91-93). The wrapper's hard-coded tool pin matches the tool at
   `d9c496b` only; the committed green receipt is reproducible only with
   `--rev d9c496b` and an explicit `--panel-rev`. Anyone replaying against HEAD gets an
   explicit SETUP failure, not a zero-specimen pass. Whether the C1 evidence should
   carry a post-C2 replay is outside this seat's claim and is left to the L1.
2. The guard compares the *set* of paths, so it does not check that the manifest is
   semantically the sole artifact beyond its filename; a replaced manifest with one
   specimen (2 paths) is also rejected, and a manifest-only tree whose manifest content
   changed is not part of this probe.

## Hygiene

- No lane index/`.git`/jj/`.ufo/state` writes; lane HEAD and panel tree re-verified
  unchanged after the probe, lane index empty.
- Scratch clone `/tmp/tameshi-r37-mut-panel`, temporary index
  `/tmp/tameshi-r37-mut-index`, specimen file, work roots and captured stdout/stderr
  deleted after the restore run.
- No tool installs or updates were performed (none needed).
