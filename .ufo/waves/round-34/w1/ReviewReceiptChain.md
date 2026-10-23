# ReviewReceiptChain — tameshi round-34 w1 receipt-chain audit

Scope: verify the C1_R33 receipt chain byte-exact against the lane at dispatch tip
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (the clone is detached at it; all `git show` /
`git grep` reads below are against that tree unless a rev is named).

**Verdict: PASS — zero findings.** Every scoped check and every corroboration probe agrees
with the pinned bytes and the claim under attack.

## Setup

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ReviewReceiptChain \
 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
      /home/vgpnk/Projects/shokunin/tameshi-shokunin <scratch>/lane \
 && git -C <scratch>/lane checkout -q --detach 0b99d48e... \
 && git -C <scratch>/lane rev-parse HEAD          ->  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7  (rc 0)
```

## Byte pins (precondition)

`sha256sum` on extracted blobs and on the fleet-root working copies, exit 0 each:

| bytes | observed sha256 | pin | match |
|---|---|---|---|
| `git show 0b99d48e:tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | 7b11ba25…8d10 | ✓ |
| `git show 0b99d48e:tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | a7d3f2dd…12eb9 | ✓ |
| fleet-root `tools/tally-audit-v2.py` | `7b11ba25…8d10` | pin | ✓ |
| fleet-root `tools/mutate-and-run.sh` | `a7d3f2dd…12eb9` | pin | ✓ |
| `git show c17e593b:tools/tally-audit-v2.py` | `7b11ba25…8d10` | pin | ✓ |
| `git show c17e593b:tools/mutate-and-run.sh` | `a7d3f2dd…12eb9` | pin | ✓ |

So the bytes the deciding run attested (`tool_sha_ok=1 runner_sha_ok=1`) are byte-identical
at the measurement rev `c17e593b`, at tip `0b99d48e`, and in the fleet working tree.

## Check 1 — controls receipt

Command: `git -C lane show 0b99d48e:.ufo/evidence/round-33/c1/controls-receipt.json` (rc 0).

- `counter_sha256` field = `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`.
  Independently recomputed: `git -C lane show 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum`
  → `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — equal, and matches the
  frozen pin prefix `f6b8868c…a07f28c`. ✓
- `all_false` = `true`; all four rows `predicate_pass: false`
  (CtlDoNothing 0/18,8/8; CtlAlwaysPass 0/18,8/8; CtlAlwaysFail 18/18,0/8; CtlShaOnly 18/18,1/8). ✓
- `runner_sha256` = `a7d3f2dd…12eb9` = runner pin. ✓
- Integrity: receipt blob is byte-identical at mint commit and tip —
  `git show 9dd3174c:.../controls-receipt.json | sha256sum` = `git show 0b99d48e:.../controls-receipt.json | sha256sum`
  = `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa`. ✓
- Mint provenance: `git show 9dd3174c:.ufo/evidence/round-34/controls/mint.exit` → `0`;
  `mint.stdout` → `C1_R33_CONTROLS: controls=4 all_false=True …` with the same four tallies. ✓

## Check 2 — deciding receipt

Commands (each rc 0):

```
git -C lane show 0b99d48e:.ufo/evidence/round-34/measure/c1-deciding-run.exit   ->  0
git -C lane show 0b99d48e:.ufo/evidence/round-34/measure/c1-deciding-run.stdout ->  C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true
```

- exit file = `0` ✓; printed `rev=c17e593b51802dd4ed568da3265f21c6d00c4273` = measurement rev ✓;
  label `C1_R33_PASS=true` present, and the full line is byte-identical to the claim. ✓
- Uniqueness: `git -C lane grep -l -F 'C1_R33_PASS=true' 0b99d48e -- .ufo/` (rc 0) returns exactly:
  - `.ufo/evidence/round-33/contract.json` — predicate text only: `"label": "C1_R33_PASS"`,
    `"target": "C1_R33_PASS=true with ho_invalid=0 and every valid sealed copy right"` (context lines 20–23).
    Excluded per assignment; not a counter-run transcript. ✓
  - `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` — the deciding run itself. ✓
  No other committed `.ufo/` file carries the label.
- Broader sweep `git grep -l -F 'PASS=true' 0b99d48e -- .ufo/` (rc 0): 100+ hits, all
  prior-round (r29–r33) contracts, counter source, controls/witness transcripts, and wave
  reports — none contain the `C1_R33_PASS=true` string except the two files above.
- Receipt commit: `git log --oneline 0b99d48e -- .ufo/evidence/round-34/measure/` → single
  entry `0b99d48 round-34: C1 measured true at c17e593b (deciding run receipt) + SCORECARD
  capability row + lesson + knowledge entry + S101 row + census end exit 0 (98 rows)` —
  the receipt was minted in the tip commit itself.

## Check 3 — mint precedes sealed set

```
git -C lane merge-base --is-ancestor 9dd3174c c17e593b51802dd4ed568da3265f21c6d00c4273; echo rc=$?  ->  0
```
`9dd3174c` is a strict ancestor of `c17e593b`. ✓

Commit stats corroborate the chronology:
- `git show --stat 9dd3174c` — "controls receipt minted at the amended rev 6aaad5b3
  (receipt-attestation rule; four seat controls all predicate_pass=false)": adds
  controls-receipt.json + 4 control tools + mint.{exit,stderr,stdout} (8 files, +175).
- `git show --stat c17e593b` — "sealed held-out set authored after the amendment-6 counter
  freeze (8 must-kill + 6 must-accept, set-aware witnesses, per-copy authoring receipts)":
  adds exactly 14 files under `.ufo/evidence/round-33/heldout/`.

`git ls-tree -r --name-only c17e593b -- .ufo/evidence/round-33/heldout/` lists 8 `ho-kill-*.json`
+ 6 `ho-accept-*.json` — consistent with `ho_kill=8/8 ho_accept=6/6` and `heldout_after_freeze=1`. ✓

## Frozen-surface diff

`git -C lane diff --stat c17e593b 0b99d48e -- .ufo/evidence/round-33/heldout/
.ufo/evidence/round-33/c1/controls-receipt.json .ufo/evidence/round-33/c1/c1-measure.py tools/`
(rc 0, empty output): every receipt-chain input is byte-identical between the measurement
rev and the dispatch tip. ✓

## Findings

None. The receipt chain is byte-exact: counter pin ↔ receipt `counter_sha256` ↔ runner pin ↔
deciding-run `rev=` field ↔ heldout commit ↔ mint→heldout ancestry, all consistent.

## Residual risk / verification gaps

- The deciding `.stdout` is a committed transcript; the kill rule is consumed so it cannot be
  re-derived by a fresh default-mode run. Its trust rests on the controls receipt, the byte
  pins, and the commit chronology — all verified — not on an independent re-execution.
- Different seeds (`a7acbc0e…` in controls receipt vs `685f63bd…` in deciding run) are expected:
  separate counter runs. Not a defect.
- I audited receipt bytes, labels, and git chronology only; the semantics of the counter's
  per-copy scoring are the wave's mutation-seat problem, out of scope here.
- Tooling: no installs performed; `git`, `sha256sum`, coreutils sufficient (pacman guard noted).
