# T56W3ExecC2Run — C2 counter at PIN

Tools installed: none. Repo mutations: none. Scratch `/fast/scratch/hyaku/tameshi-r56/T56W3ExecC2Run` (removed on exit).
`c2/measure.py` in the live tree is byte-identical to the one at PIN and at the amended freeze 21eb3c63 (`cmp` clean).
`total` in the verdict line counts FAILED arms.

## 1. Amended counter at PIN 2f5512a8ab0771fb2eee463ec16db359174f5edd (exit 1)

Command (work dir empty, fresh):
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work <empty dir> --explain`

```
EXPLAIN arm1-selftest exit=0 19/19
EXPLAIN arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True
EXPLAIN arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm6-docs 4/4
C2_R56: rev=2f5512a8ab07 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false
```

Only arm 5 (`own`) fails: `own-receipts-missing`. Cause: `git ls-tree -r 2f5512a8 -- .ufo/evidence/round-56/control` lists only `frozen-surface.paths`; `control/controls-a.stdout` and `controls-b.stdout` are not committed at PIN (nor present in the live tree: `ls control/` = `frozen-surface.paths`). This is the documented bootstrap state, not a gate defect. Arms 1,2,3,4,6 pass (selftest 19/19, red54/red54b/red55 refused with the contract's codes, old round-54 gate accepted the real receipts, docs 4/4 — docs arm now passes because the PIN carries QUALITY/knowledge/SKILL/registry text).

## 2. Reproduction of committed `before/c2.stdout` at the ORIGINAL freeze c3e2ca9f020776b3d66c7af854fb82c834674fcf

The counter bytes used are the original-freeze ones (`git show c3e2ca9f:.ufo/evidence/round-56/c2/measure.py`, 14-case gate), run with `--rev c3e2ca9f020776b3d66c7af854fb82c834674fcf`, `--explain`:

```
EXPLAIN arm1-selftest exit=0 14/14
EXPLAIN arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True
EXPLAIN arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm6-docs 0/4
C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false
```
`diff` against `.ufo/evidence/round-56/before/c2.stdout`: IDENTICAL (byte-for-byte). before/c2.stdout reproduces; red is 2 failing arms (own, docs) before, 1 (own) at PIN.

(Side check, amended counter at the amended freeze 21eb3c63: `selftest=19/19 ... own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` — shows the 14→19 case growth is the freeze amendment, not a regression.)

## 3. What closes arm 5
Commit real `controls.sh` output as `.ufo/evidence/round-56/control/controls-a.stdout` and `controls-b.stdout` (bootstrap two-pass; only the second run's outputs feed the deciding run) at the certified revision, then rerun the same command above at that revision; arm 5 gates a as `control` (all CTL revs ancestors) and b as `positive` (names the certified revision or content-identical on the frozen surface). Expected after that: `own=` pass, `total=0`, `C2_R56_PASS=true` — subject to the known provenance blind spot (arm 5 accepts hand-written receipts naming the certified revision; not admission evidence per T56W2CritDoNothingC2.md).

Files changed: this report only. Blockers: none for this item; arm 5 depends on L1's controls commit.
