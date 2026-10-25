# ScoutLedgerUnchanged — No-harm depth monitor (round 39)

## Question
Run the canonical SCORECARD command D one-liner at rev `50aadd1bbd94e43cd3fcfb81459414394db2dc35` and report `recorded_cases` and `depth_score`.

## Command (exact)
```
git show 50aadd1bbd94e43cd3fcfb81459414394db2dc35:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases=%d depth_score=%d"%(n,min(10,n)))'
```
Run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (lane checkout, read-only `git show`; no writes to index, tree, or `.ufo/state`).

## Observed output
```
recorded_cases=9 depth_score=9
```

## Facts
- Contract source of the command and regex: `.ufo/evidence/round-39/contract.json:34-37` (`no_harm_guard.depth_command_d` / `depth_command_d_regex`).
- The regex `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` matches 9 recorded-case header lines in `tools/mutate-and-run.sh` at the base rev; `depth_score = min(10, 9) = 9`.
- This is consistent with the contract's control expectation ("A vacuous `^\s*leg` guard disagrees on the live runner (0 vs 9)", `contract.json:17`): the true live-runner count is 9, confirming 0-vs-9 disagreement for the vacuous r38 regex and 9-vs-0 for a constant-9 guard on a ledger-stripped copy.
- Depth axis unchanged: base rev holds `recorded_cases=9`, `depth_score=9`; this is the no-harm monitor, not a new leg.

## Confidence
High — single deterministic read-only command, output reproduced verbatim above.

## Remaining unknowns
None for this scoped question.
