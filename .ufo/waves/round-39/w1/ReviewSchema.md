# ReviewSchema — round-39 row schema check

Scope: corpus/SOURCES.md rows S107 and S108. Confirm 11 cells per row and no
literal pipe characters inside cells. No edits made to the live lane checkout.

## Command

```
awk -F'|' 'NR==119 || NR==120 {n=0; for(i=2;i<=NF-1;i++) n++; printf "line %d: fields=%d pipes=%d id=%s\n", NR, n, NF-1, $2}' corpus/SOURCES.md
```

Output:

```
line 119: fields=11 pipes=12 id= S107
line 120: fields=11 pipes=12 id= S108
```

Escaped-pipe check: `grep -c '\\|'` over lines 119–120 → `0` (no `\|` escapes
present or needed; the awk split already proves no stray `|` inside a cell,
since a literal pipe would inflate the field count past 11).

## Findings

- **S107 (corpus/SOURCES.md:119): NF.** 11 cells, exactly 12 pipe delimiters,
  no literal pipe inside any cell. Schema order (id | source | type | grade |
  relevance | pinpoint | content note | status | date | TTL | knowledge paths)
  matches surrounding rows.
- **S108 (corpus/SOURCES.md:120): NF.** 11 cells, exactly 12 pipe delimiters,
  no literal pipe inside any cell. Same schema conformance.

## Residual risk

None within scope. Cell-content semantics (URL reachability, sha256 accuracy)
were not in scope for this schema check.

## Verification gaps

None for the assigned predicate; both checks are mechanical and reproducible
with the command above.
