# ScoutCommandD — Command D / round-38 regex hit counts

## Scope
At rev `50aadd1bbd94e43cd3fcfb81459414394db2dc35`, ran the SCORECARD command D
pattern and the round-38 regex `^\s*leg` against `tools/mutate-and-run.sh`
(read via `git show`, no checkout mutation). Runner not edited.

## Findings

### 1. SCORECARD command D pattern (frozen in `.ufo/evidence/round-39/contract.json` → `no_harm_guard.depth_command_d`)

Command run (verbatim from contract `no_harm_guard.depth_command_d`):

```
git show 50aadd1bbd94e43cd3fcfb81459414394db2dc35:tools/mutate-and-run.sh | \
  python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases=%d depth_score=%d"%(n,min(10,n)))'
```

Output:

```
recorded_cases=9 depth_score=9
```

**Command D hit count: 9** (regex `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+`,
multiline; depth_score = min(10,9) = 9).

### 2. Round-38 regex `^\s*leg`

Command run:

```
git show 50aadd1bbd94e43cd3fcfb81459414394db2dc35:tools/mutate-and-run.sh | \
  python3 -c 'import re,sys; s=sys.stdin.read(); hits=[(i+1,l) for i,l in enumerate(s.splitlines()) if re.match(r"\s*leg",l)]; print("r38_leg_hits=%d"%len(hits))'
```

Output:

```
r38_leg_hits=0
```

**Round-38 `^\s*leg` hit count: 0** — vacuous control confirmed; zero matching
lines in `tools/mutate-and-run.sh` at the base rev.

## Consistency with contract

- Contract C1 `do_nothing_control` expects `^\s*leg` → 0 hits on the live/base
  runner ("0 vs 9"): observed 0, consistent.
- Contract C1 implies command D → 9 on the runner ("0 vs 9"): observed 9,
  consistent.

## Confidence
High — outputs observed directly; blob confirmed to exist
(`git cat-file -e 50aadd1bbd94e43cd3fcfb81459414394db2dc35:tools/mutate-and-run.sh`).

## Remaining unknowns
None for this question. The ledger-stripped-copy agreement and the guard
regex's placement in the round-39 contract are outside this ticket's scope.
