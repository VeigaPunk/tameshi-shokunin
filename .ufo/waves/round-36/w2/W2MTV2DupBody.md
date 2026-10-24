# W2MTV2DupBody — v2 public-slot distinctness probe (round 36, wave 2)

Seat: W2MTV2DupBody (mutation tester). Lane tip under attack: `fbb01cf46f8437fd1264c1a3acc053c882fa2164`
(`round-36 verifier spot-check (integrator, hyaku)`). Scratch-only work; lane/fleet/frozen artifacts untouched.
Probe: `replace one public accept copy's body with a byte-copy of another accept copy (distinct bodies 9->8)`;
expected detector: v2 `PUB_DISTINCT_TARGET` (9) fails while frozen v1 still passes.

## Mutant

Scratch lane clone: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2DupBody/lane`
(clone of `master` at `fbb01cf`, `--single-branch`; all frozen pins re-verified in the clone:
`tools/tally-audit-v3.py` 6188db16…, `tools/mutate-and-run.sh` a7d3f2dd…, `c1-measure-v2.py` 9eb8944c…).

One public accept copy, `comment-esac.json`, replaced by a byte-copy of the other public accept copy
`comment-brace.json` (same file bytes, same edit pair → identical resulting runner body):

| | path | file sha256 | git blob |
|---|---|---|---|
| before | `.ufo/evidence/round-35/c1/panel/comment-esac.json` | `2f10fb95d209f9c2a9492282424fe764b8c5e1b2e0c5e6d5a81deb6c2e25b276` | `ff9965696b1b9e7586452788eb02eabfd48a2e38` |
| mutant | same path @ `0fb1770` | `8fbf2436fce2172dda4485851b838ec036ee10e242b0dfe7df4c38d08b8e9f33` (= `comment-brace.json`) | `c2fb6a314ca26ebb970307d3257659ebbe633b72` |
| restored | same path @ `fbb01cf` | `2f10fb95d209f9c2a9492282424fe764b8c5e1b2e0c5e6d5a81deb6c2e25b276` | `ff9965696b1b9e7586452788eb02eabfd48a2e38` |

Mutant commit (scratch clone only, parent `fbb01cf`):
`0fb1770e04e546b4d51f0576aa7e1c334f1e75ad` — "MUTANT: comment-esac body replaced by byte-copy of
comment-brace accept copy", 1 file / 3 insertions / 3 deletions. Slot shape unchanged (6 kill, 3 accept);
only the applied-body hash set changed: 9 distinct → 8, duplicate hash `b9eb589a3ee0…` =
`comment-brace.json` + `comment-esac.json`, both `set=accept`. Independent pre-check reproduced 9→8.

## Exact commands (all counters read the panel at `--rev` via `git show`, so the mutant had to be committed
in the scratch clone; nothing was committed anywhere else)

Driver: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2DupBody/run_detectors.sh`; each run:

```sh
python3 <lane>/.ufo/evidence/round-{35,36}/c1/c1-measure{,-v2}.py \
  --lane /fast/scratch/hyaku/tameshi-r36-seats/W2MTV2DupBody/lane \
  --rev <fbb01cf|0fb1770> \
  --work /fast/scratch/hyaku/tameshi-r36-seats/W2MTV2DupBody/work/<run> \
  --sealed .ufo/evidence/round-35/c1/sealed
```

(order: v1 base, v2 base, v1 mutant, v2 mutant; then `git checkout -q fbb01cf`; then v2 restored)

## Detector output (verbatim verdict lines, fresh empty `--work` per run)

- v1 base @ `fbb01cf` (189 s, exit 0):
  `C1_R35: mode=deciding … pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=fbb01cf… C1_R35_PASS=true`
- v2 base @ `fbb01cf` (167 s, exit 0):
  `C1_R36V2: mode=deciding … pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 … C1_R36V2_PASS=true`
- v1 mutant @ `0fb1770` (166 s, exit 0):
  `C1_R35: mode=deciding … pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=8 … C1_R35_PASS=true`
- v2 mutant @ `0fb1770` (159 s, **exit 1**):
  `C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=8 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=0fb1770e04e546b4d51f0576aa7e1c334f1e75ad C1_R36V2_PASS=false`
- v2 restored @ `fbb01cf` (146 s, exit 0):
  `C1_R36V2: mode=deciding … pub_distinct=9 … C1_R36V2_PASS=true`

Copy-level rows were identical across all five runs (16 copies scored: 6/6 public kill, 3/3 public accept,
4/4 sealed kill, 3/3 sealed accept, 0 invalid, no `PUB_DISTINCT`-adjacent change). The **only** term that
differs between the v2 base and v2 mutant lines is `pub_distinct` 9→8; every pin/slot/sealed term is equal
(`tool_sha_ok=1 runner_sha_ok=1 sealed_after_freeze=1 ho_invalid=0 pub_kill=6/6 pub_accept=3/3`).
So v2's failure is attributable to `PUB_DISTINCT_TARGET` alone.

## Verdict

**KILLED by v2.** Expected detector `PUB_DISTINCT_TARGET=9` fired exactly: `pub_distinct=8` ⇒
`C1_R36V2_PASS=false`, exit 1, with all other conjuncts at their pristine values. **Survived by frozen v1**
(`C1_R35_PASS=true`, exit 0, same `pub_distinct=8`): v1 has no distinctness conjunct, so it prints the field
but does not predicate on it — this is the known round-35 closure defect 2 that v2 was frozen to close, and it
is *not* a v1 regression or a baseline failure. The mutation is therefore detected only by the successor
counter, which is exactly the claimed delta between C2's counter and its parent.

No calibration anomaly: pristine baseline passes both counters (a baseline failure would have made the kill
inconclusive), the mutant is byte-identical-body only (no kill/accept slot reclassification, no tool/runner/
sealed change), and the restored run returns the pristine verdict.

## Restoration evidence

- `git -C <scratch>/lane checkout -q fbb01cf` ⇒ `HEAD = fbb01cf46f8437fd1264c1a3acc053c882fa2164`,
  `git status --porcelain` empty.
- `sha256(comment-esac.json) = 2f10fb95…e25b276` = pre-mutation byte hash; `git hash-object` =
  `ff9965696b1b9e7586452788eb02eabfd48a2e38` = `git rev-parse fbb01cf:…/comment-esac.json`; v2 re-run on the
  restored bytes: `pub_distinct=9`, `C1_R36V2_PASS=true`.

Scratch artifacts retained: `out/summary.txt`, `out/{v1_base,v2_base,v1_mutant,v2_mutant,v2_restored}.log`,
`out/restore_evidence.txt`, `run_detectors.sh`.

## Bounds / hygiene

- Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` still at `fbb01cf`, `comment-esac.json`
  `2f10fb95…`, `comment-brace.json` `8fbf2436…`, `c1-measure-v2.py` `9eb8944c…`, `tally-audit-v3.py`
  `6188db16…`, `mutate-and-run.sh` `a7d3f2dd…` — all identical to the frozen pins; no lane edits.
- Only lane write: this report (`.ufo/waves/round-36/w2/`); all mutation work under
  `/fast/scratch/hyaku/tameshi-r36-seats/W2MTV2DupBody/`. No `pacman`, no installs, no subagents,
  no edits to frozen artifacts, `.git` directories of the lane/fleet, or `.ufo/state/`.
