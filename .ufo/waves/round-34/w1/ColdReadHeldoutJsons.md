# ColdReadHeldoutJsons — cold-read re-credit of the 14 sealed heldout JSONs

Seat: `tameshi-r34-w1-ColdReadHeldoutJsons` (wave r34/w1, policy v2). Scope: re-verify the
14 sealed JSONs under `.ufo/evidence/round-33/heldout/` against the frozen-order contract
implemented by the amendment-6 counter (`validate_ho` schema, single-occurrence edits,
mutated-differs, `git log --diff-filter=A` ancestry). Verdicts are observations; the
deciding run stands.

## Setup (all in /fast/scratch/hyaku/tameshi-r34-seats/ColdReadHeldoutJsons)

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin lane            # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                      # exit 0
git -C lane show 0b99d48e...:tools/tally-audit-v2.py > tool.py    # exit 0
git -C lane show 0b99d48e...:tools/mutate-and-run.sh > pristine.sh # exit 0
sha256sum tool.py pristine.sh
#   7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py   == pin
#   a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh == pin
git -C lane rev-parse HEAD  ->  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7 (tip confirmed)
```

Counter module imported, never executed in kill mode: the frozen counter
`.ufo/evidence/round-33/c1/c1-measure.py` (sha256
`f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`, byte-identical to the
pin) was copied to `mod/.ufo/evidence/round-33/c1/c1-measure.py` beside a tip copy of
`.ufo/evidence/round-32/c1-measure.py` (its self-import `v1` resolves through `HERE/../..`),
then loaded with `importlib.util.spec_from_file_location`. The script `recheck.py` calls
the counter's own `validate_ho`, `apply_edits`, `ho_witness_ok` (which internally uses
`tally_block_of`, `head_of`, `block_run` under real `bwrap` 0.13.1), `adding_commit`,
`is_ancestor`, `list_tree`, `show`, `sha256`. Run: `timeout 900 python3 recheck.py` →
exit 0, stderr empty, full machine-readable output in `recheck.json` (596 lines, in scratch).

## Result: NO FINDINGS — all gates hold on all 14 files

### Tree and byte identity

- `git ls-tree -r --name-only 0b99d48e -- .ufo/evidence/round-33/heldout` → exactly 14
  `.json` entries, names matching the disk set (8 `ho-kill-*`, 6 `ho-accept-*`). No
  non-JSON or extra files.
- For every file: sha256(blob at tip `0b99d48e`) == sha256(blob at measurement rev
  `c17e593b`) == sha256(fleet working-tree copy). `tip_eq_meas=True`,
  `tip_eq_disk=True` on all 14 rows — the sealed set is untouched since commit at
  `c17e593b` and the on-disk copies are the committed bytes.

### Schema (counter `validate_ho`, real code)

All 14 parse as JSON objects and pass `validate_ho`: `id`/`author` strings
(`author='tameshi-shokunin L1 (TameshiR34)'` on all 14, `id` matches filename stem),
`set` ∈ {kill×8, accept×6}, `edits` nonempty with string `old`/`new`, witness either
`kind=head` (4 files: both head-accepts, both head-kills) or `vector` of 9 ints in
0..255 (10 files: 4 accept + 6 kill). All pass — no `CounterError`.

### Single-occurrence old-strings and mutation-differs

`apply_edits` succeeded on all 14 (`apply_edits='ok'`); each edit's `old` occurs
exactly once both in `pristine.sh` (`all_pristine_once=True`) and in the
sequentially-mutated text (`all_seq_once=True`), and `mutated != pristine`
(`mutated_differs=True`) on all 14. Edit surface: head edits touch `st_js`/`st_claims`
assignment lines, `VERSION=`, or insert inert lines/comments; vector edits touch the
tally block's `npass/nfail/nsetup` arms, the `exit`/`if` thresholds, or the quoted
field order in the FAIL print.

### Supplemental: `ho_witness_ok` re-run (amendment-6 set-aware gate)

Re-ran the deciding run's validity gate so `ho_invalid=0` is re-credited end-to-end.
Under real `bwrap` sandboxes (`block_run`, timeout 90s, RO runtime mounts):
- head accepts → `True ('head')`; head kills → `True ('head-leg-assignment')`;
- vector accepts → `True ('vector-equivalence')` (block outputs equal, bytes differ);
- vector kills → `True ('vector')` (pristine vs mutated block output differs).
All 14 `witness_ok=True` — consistent with receipt `ho_kill=8/8 ho_accept=6/6 ho_invalid=0`.

### Frozen-order ancestry (`git log --diff-filter=A` + `merge-base --is-ancestor`)

- `adding_commit(lane, rev, SELF_PATH)` == `adding_commit(lane, rev, TOOL)` ==
  `f6d8a891f1d966c5c3cdda385090da3a6e804675` at both revs (counter and tool were added
  in the same commit, which predates the seal).
- `adding_commit` for every one of the 14 heldout files ==
  `c17e593b51802dd4ed568da3265f21c6d00c4273` (the sealing commit) — at both
  `rev=c17e593b` and `rev=0b99d48e`.
- `merge-base --is-ancestor f6d8a891 c17e593b` → exit 0; the stronger chain
  `merge-base --is-ancestor 6aaad5b3 c17e593b` (amendment-6 rev → sealing commit) →
  exit 0; `merge-base --is-ancestor c17e593b 0b99d48e` (measurement rev → tip) →
  exit 0. So sealing is strictly after the amendment-6 counter freeze and after the
  tool add, on first-parent history reachable from tip. `heldout_after_freeze=1`
  re-credited.

### Method notes (observations, not findings)

- The counter's ancestry gate skips a file silently if any of `add`, `self_add`,
  `tool_add` is `None` (`if add and self_add and tool_add:`); here all are non-None
  and I checked the ancestor relations directly, so no reliance on the skip path.
- `apply_edits` counts occurrences on progressively-mutated text; for these 14 files
  pristine and sequential counts agree (all == 1), so the two readings coincide.

## Commands relied on

| Command | Exit | Evidence |
|---|---|---|
| `git clone --no-hardlinks …` + `checkout --detach 0b99d48e` | 0 | scratch lane at tip |
| `git show 0b99d48e:tools/{tally-audit-v2.py,mutate-and-run.sh}` + `sha256sum` | 0 | both sha256 == pins |
| `python3 recheck.py` (counter module import; no kill-run) | 0 | `recheck.json` in scratch; tables above |
| `git ls-tree -r --name-only 0b99d48e -- .ufo/evidence/round-33/heldout` | 0 | exactly the 14 sealed names |
| `git log --diff-filter=A --format=%H <rev> -- <path>` (via `adding_commit`) | 0 | all adds = `c17e593b`; counter/tool add = `f6d8a891` |
| `git merge-base --is-ancestor` ×3 | 0 each | `f6d8a891`, `6aaad5b3`, `c17e593b` ancestor chain to tip |

Per-file blob sha256 (tip, first 16 hex): `a08f7e21a9d74f5f` head-comment,
`2e600127ab1d86f7` head-version-rename, `3f8ad257fd11a132` arith-space,
`3da5127049bcc371` block-comment, `edc3c69f519058f1` inert-line, `d23afb234c4a0dd6`
tail-comment, `9e7f9076c32e0f90` extra-assign, `32c69340eda67f57` nonbare,
`aa5e12e33effebf4` arm-swap, `566faacfe3552350` count-field-swap,
`9724e0c273c35fad` fail-exit-swap, `5d8cea2eddafc49e` fail-threshold,
`633ba5b68b77833f` setup-arm-skip, `4ed1632fac703845` setup-threshold (full shas in
`recheck.json` under `bytes.tip_sha`).

## Verdict

The sealed set re-credits cleanly: 14/14 schema-valid, every `old` unique under both
count readings, every mutation differs, ancestry holds at measurement rev and tip, and
the amendment-6 witness gate re-passes 14/14 under real `bwrap`. The deciding-run
receipt's `ho_*` and `heldout_after_freeze=1` fields are consistent with what is on the
lane. No installs performed (all tools present: python3, bwrap 0.13.1, git); lane and
`.ufo/` untouched except this report.
