# Round 36 W1 — mid-round census finding

**Attack:** depth axis; checked the registry-row cardinality at the CONTENT commit, which is the parent of the round-36 cold-read refresh commit.

Revision resolution command:
```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show -s --format='%H%n%P%n%s' b455001e
```
Output:
```text
b455001e2589b3f4f471d94a3de7e5e549b9f54c
e423c41ba253357ab8c8513f0376dad9d38ab248
round-36: cold-read refresh — four L1 author source re-anchor entries (recipe/restore-discipline/map/where-to-enter) with trace receipts, refresh specs+receipts citing S103
```

Registry-row grep command at CONTENT commit `e423c41ba253357ab8c8513f0376dad9d38ab248`:
```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show e423c41ba253357ab8c8513f0376dad9d38ab248:corpus/SOURCES.md | grep -Ec '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
```
Output:
```text
100
```

The lane worktree was not checked out at that revision, and no mutating git command was run. The full `sources-census.sh validate` was not run; this finding is the requested historical registry-row count, not a full validation result.

**Verdict: PASS — 100 registry rows at the CONTENT commit.**
