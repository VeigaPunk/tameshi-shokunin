# RevengerEmptyPanel — empty-panel control, reproduced end to end from outside

## What was attacked

C2's depth surface (round-36 contract, `.ufo/evidence/round-36/contract.json`): the claim that the
frozen v2 successor counter `c1-measure-v2.py` (sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`)
closes round-35 closure routed defect 2 — v1's predicate compared kill/accept counts only against the
panel's own slot counts, so a zero-slot (empty) public panel satisfied it vacuously. The control is the
empty-panel mutant: v1 must still print `C1_R35_PASS=true` on it; v2 must print `C1_R36V2_PASS=false`.

Both counters were executed from their canonical frozen lane paths (never copied, never edited);
all specimen/panel/sealed bytes were read from COMMITTED history at the mutant rev inside my own clone.

## Preconditions verified (read-only, before any run)

- Lane tip: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` — "round-36: receipts — monitor before(796e08b)=6 / control(e423c41b)=6 / after(b455001e)=8 64-64, census exit 0 at b455001e (100 rows), depth guard 9/9, v2 deciding PASS at b455001e, empty-panel mutant v1 PASS / v2 FAIL".
- Frozen pins matched at source: `tools/tally-audit-v3.py` = `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`, `tools/mutate-and-run.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, `.ufo/evidence/round-36/c1/c1-measure-v2.py` = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`.
- No tool installs needed (system git + system python3); no pacman use.

## Reproduction steps and exact commands

1. Clone (git writes confined to the clone; source lane untouched, clone clean at 0 dirty files):

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/lane
# clone HEAD = d9c496b19371b779ce0eec6dfee1b049b27a3a2d
```

2. Mutant commit — empty the public panel (9 JSON copies, 135 deletions; sealed/ untouched):

```
git -C /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/lane rm -r -q .ufo/evidence/round-35/c1/panel
git -C /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/lane -c user.name='RevengerEmptyPanel' -c user.email='revenger-empty-panel@tameshi-shokunin.local' commit -q -m 'empty-panel control: remove the round-35 public panel (zero-slot mutant, RevengerEmptyPanel)'
```

Mutant rev: **`09c047f707f0a17043d15c073548ee60f201c2c0`** (parent `d9c496b1`, exactly one commit on the lane tip).

3. Run frozen v1, then frozen v2, against that commit (runs executed sequentially — both counters drive the same shared `/tmp/tally-audit-explicit` specimen path, so concurrent runs would race and could taint the verdicts):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/lane \
  --rev 09c047f707f0a17043d15c073548ee60f201c2c0 \
  --work /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/work-v1 \
  --sealed .ufo/evidence/round-35/c1/sealed

python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/c1/c1-measure-v2.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/lane \
  --rev 09c047f707f0a17043d15c073548ee60f201c2c0 \
  --work /fast/scratch/hyaku/tameshi-r36-seats/RevengerEmptyPanel/work-v2 \
  --sealed .ufo/evidence/round-35/c1/sealed
```

Both `--work` dirs were freshly created and empty (the counters abort with `work_not_empty` otherwise).

## Captured predicate lines (verbatim)

v1 (exit 0, ~96 s):

```
C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=09c047f707f0a17043d15c073548ee60f201c2c0 C1_R35_PASS=true
```

v2 (exit 1, ~73 s):

```
C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=09c047f707f0a17043d15c073548ee60f201c2c0 C1_R36V2_PASS=false
```

## Evidence chain

- Every shared input is identical between the two runs (same lane, same rev `09c047f7`, same sealed set, same runner/tool pins — `tool_sha=6188db16…`, `runner_sha_ok=1` in both lines, committed bytes read at rev via `git show`). The only delta is the predicate.
- On the zero-slot panel v1 sees `pub_kill=0/0 pub_accept=0/0` — pass conditions `pub_kill == pub_kill_slots` and `pub_accept == pub_accept_slots` hold vacuously (0==0), so v1 accepts. v2 additionally requires `pub_kill_slots==6 ∧ pub_accept_slots==3 ∧ pub_kill==6 ∧ pub_accept==3 ∧ pub_distinct==9`; observed `pub_slots=0 pub_distinct=0` fails all five frozen-surface conjuncts → reject.
- Sealed set unaffected and fully green in both runs (`ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1`): provenance gates held at the mutant rev — manifest `freeze_rev` `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` equals the commit that first added `.ufo/evidence/round-35/contract.json` (verified in-clone), which is an ancestor of the mutant rev. So the verdict flip is attributable solely to the public-slot cardinality + distinctness asserts — precisely the r35 routed-defect-2 fix v2 freezes.
- Both runs emitted identical per-copy COPY lines (7 sealed copies: 4 kill diverge-and-are-caught, 3 accept inert), confirming deterministic behavior across the two independent executions.

## Verdict

VERDICT: REPRODUCED — empty-panel control at mutant commit `09c047f707f0a17043d15c073548ee60f201c2c0` (parent = lane tip `d9c496b1`): frozen v1 prints `C1_R35_PASS=true` (exit 0, vacuous 0/0 accept) while frozen v2 prints `C1_R36V2_PASS=false` (exit 1, frozen 6/3/9 public-slot cardinality + distinctness asserts reject the zero-slot panel). C2's routed-defect-2 closure demonstrably kills the vacuous accept; no defect found in either counter.
