# RevengerR38 — r38 contract regex `^\s*leg` still present (round 39, w1)

## Finding (claim holds)

`.ufo/evidence/round-38/contract.json:58` still contains the regex `^\s*leg`
(raw JSON source bytes: `r\"^\\s*leg\"`, two occurrences, inside
`no_harm_guard.depth_command_d`). The file was **not edited** by this seat.

Verbatim line 58 (of 61):

```
    "depth_command_d": "git show REV:tools/mutate-and-run.sh | python3 -c 'import sys,re;s=sys.stdin.read();print(\"recorded_cases=%d depth_score=%d\"%(len(re.findall(r\"^\\s*leg\",s,re.M)),min(10,len(re.findall(r\"^\\s*leg\",s,re.M)))))'",
```

## Evidence chain

1. **Presence** — `grep '\\s\*leg' .ufo/evidence/round-38/contract.json` → single hit, line 58 (context shows `no_harm_guard` block, lines 57–60).
2. **Integrity / no drift** — working tree is byte-identical to HEAD:
   - `sha256sum .ufo/evidence/round-38/contract.json`
     → `84863c8ee2fa55d7dc564d7953b2053cc8c995f34cd0fe921a8a6ad48e907fee`
   - `git show HEAD:.ufo/evidence/round-38/contract.json | sha256sum` → same hash.
   - Last commit touching the file: `e118024ae8c45862fa393a85bd29aa928ea80d3e` "round-38: self-assessment reconciliation (calibration) + golden-comparison three-outcome verdict (depth)". HEAD is `233077f88d7a8d142eff329202a120457a5d5258`.
3. **Cross-reference** — frozen `.ufo/evidence/round-39/contract.json` requires exactly this state: `notes` says "The r38 contract is not edited."; `no_harm_guard.note` says "The round-38 regex `^\s*leg` is left untouched and is the vacuous control."; C1 predicate pass condition includes "the round-38 guard regex `^\s*leg` matches 0 lines of the live runner".

## Divergence observed (ground truth, command + output)

The r38 contract's own `expectation` (line 59) — "recorded_cases=9 depth_score=9 at base and at the round commit" — does **not** hold for the recorded regex; the guard is vacuous on the live runner:

- `grep -P '^\s*leg' tools/mutate-and-run.sh` (grep tool, pattern `^\s*leg`) → **no matches**.
- The recorded command run verbatim (read-only `git show`):
  - `git show HEAD:tools/mutate-and-run.sh | python3 -c 'import sys,re;s=sys.stdin.read();print("recorded_cases=%d depth_score=%d"%(len(re.findall(r"^\s*leg",s,re.M)),min(10,len(re.findall(r"^\s*leg",s,re.M)))))'`
    → `recorded_cases=0 depth_score=0`
  - Same at `REV=50aadd1bbd94e43cd3fcfb81459414394db2dc35` (r39 `lane_base_rev`)
    → `recorded_cases=0 depth_score=0`

So `^\s*leg` matches 0 lines of `tools/mutate-and-run.sh` at both revs: the r38 line-58 regex is the vacuous control r39's C1 predicate demands (`r38_regex_hits=0`), while r38's line-59 expectation value (9) is not reproducible from that regex. [INFERENCE] the `9` in line 59 reflects the runner's true ledger-leg count as scored by the *correct* command-D regex (which r39 `no_harm_guard.depth_command_d_regex` now supplies: `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+`), not an output of the vacuous regex on line 58.

## Bounds compliance

- No edits to `.ufo/evidence/round-38/contract.json`, the live lane checkout, `.git`, `.ufo/state`, jj state, or any domain tree. Only reads, read-only `git show`/`sha256sum`, and this Report file.
- No tool installs performed (none needed; pacman paused per operator directive).
- Confidence: **high** — presence, hash equality, and 0-hit behavior all directly observed.
