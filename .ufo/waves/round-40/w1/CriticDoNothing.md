# CriticDoNothing — C1 do-nothing falsification attempt (round 40, w1)

## Verdict
Predicate HOLDS. A tree without `tools/write-path-census-v2.py` cannot pass C1;
absence is an unconditional early fail, unreachable by any other field.

## Structural evidence (path:line)
- `.ufo/evidence/round-40/census/measure.py:120-121` — `blob = git_show(...)`,
  `if blob is None: return emit('C1_R40', [...tool_absent=1...], False)`.
  The pass conjunction (`ok = ...`, measure.py:222-230) sits after this early
  return; a missing blob never reaches `sha_ok`, `planted_ok`, `live_ok`, or the
  mutant kills. No other code path emits `C1_R40_PASS=true`.
- `git_show` (measure.py:45-52) returns `None` iff `git show REV:path` exits
  non-zero — i.e., the path is absent from the tree. No fallback exists.
- `sha_ok` (measure.py:130-138) also cannot be satisfied without the blob:
  `digest` is computed from the blob itself, so the contract pin
  `40228532…878b` is unforgeable by omission.

## Empirical evidence
- Before receipt (authoritative): `.ufo/evidence/round-40/before/c1-at-base.stdout:1`
  `C1_R40: tool_absent=1 bytes_unflagged=0 replace_unflagged=0 v1_bytes_unflagged=0
  v1_replace_writes=0 rev=304e3355705640af2879c772fc9a5c2902c61763 C1_R40_PASS=false`
  exit file `before/c1-at-base.exit` = `1`.
- Path absent at base, independently confirmed:
  `git -C $LANE show 304e3355…:tools/write-path-census-v2.py` →
  `fatal: path 'tools/write-path-census-v2.py' exists on disk, but not in '304e3355…'`.
- Isolation run on a scratch copy (freeze rev NOT run in default mode): scratch
  lane `/tmp/tameshi-r40-CriticDoNothing/lane`, rev
  `88609684a8258e0924158660c51bc7e768d060df`, containing every input a passing
  tree needs from freeze rev `5641ed84…` — contract.json (with the pin),
  census/fixtures.json, write-path-census.py (sha `bc8c660c…`, matches v1 pin),
  registry-replay.py, bash-witness-study.py — but NO v2 tool. Command:
  `python3 .ufo/evidence/round-40/census/measure.py --lane /tmp/tameshi-r40-CriticDoNothing/lane --rev 88609684a8258e0924158660c51bc7e768d060df`
  → `C1_R40: tool_absent=1 … C1_R40_PASS=false`, exit 1.
  Absence alone kills the run even with all other evidence present.
- Second do-nothing branch also closed (allowed `--control`):
  `python3 .ufo/evidence/round-40/census/measure.py --lane $LANE --control`
  → `C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0
  v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false`, exit 1 — embedded v1
  patterns on the planted fixtures cannot reach the v2 target.

## Impact on axes
- depth (C1): do-nothing disjunction in contract.json:28 is airtight on both
  branches; no counterexample found. No fix needed.
- Nothing observed that the canonical judge must reject.

## Constraints honored
- No default-mode counter run on freeze rev `5641ed84c8dc148c34c8dd83f062279ddf06b4af`.
- No edits to contract.json, live lane checkout, .git, .ufo/state, or domain trees.
- No planner/model added; no installs performed.
