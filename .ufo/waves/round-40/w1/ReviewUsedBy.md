# ReviewUsedBy — S152 used-by cell

**Verdict: CONFIRMED** under the lane's operative convention; one residual noted below.

## The cell

`corpus/SOURCES.md:122` — S152 row, last field (used-by):

```
corpus/knowledge/r6-snapshot-practice-corpus.md, corpus/knowledge/r40-write-form-misses.md
```

Exactly two comma-separated entries. Verified raw via `read corpus/SOURCES.md:121-123:raw` (untruncated; row is well-formed, NF=13). The pre-append validated copy `.ufo/waves/round-40/assimilation/validate/corpus/SOURCES.md:122` is byte-identical.

## Both entries exist and cite S152

- `corpus/knowledge/r6-snapshot-practice-corpus.md` — exists; `source: S152 — …` at line 1, `S152 is the UFMG thesis PDF.` at line 10.
- `corpus/knowledge/r40-write-form-misses.md` — exists; `source: S152 — …` at line 1, `S152's abstract says fragility…` at line 14.

Command: `grep -rl 'S152' corpus/` → exactly five hits:
`corpus/SOURCES.md` (the registry row itself), the two used-by files above, `corpus/lessons/round-40.md`, `corpus/README.md`. Outside corpus: `LOG.md` only (verified `grep -rl 'S152' --exclude-dir=.jj --exclude-dir=.ufo .`). No `tools/` file cites S152.

So within the citing class that used-by enumerates (`corpus/knowledge/` entries; occasionally `tools/` and lessons), the cell lists exactly the two knowledge entries that cite S152, both exist, and both contain the `S152` token — the forward direction the lane validator checks (`sources-census.sh` H4: used-by path exists and contains the row id) passes.

## Residual (convention note, not a defect)

Three other files contain the `S152` token and are not in used-by:

- `corpus/lessons/round-40.md:10,37,45` — the admitting lesson. Precedent is split lane-wide: S104's used-by lists `corpus/lessons/round-37.md` (its admitting lesson), while S101's used-by omits `corpus/lessons/round-34.md` despite 9 cites there. S152's own admit-note (`round-40.md:15`) declares "used-by is the thesis entry and `corpus/knowledge/r40-write-form-misses.md`", and sibling admit S132 follows the same only-the-admitted-entry rule (`round-40.md:22`). Deliberate, logged, consistent with S101/S132.
- `corpus/README.md:507-508` — knowledge index. Checked all rows: no used-by cell in `corpus/SOURCES.md` ever lists README.md or LOG.md (`awk` scan, zero hits).
- `LOG.md:2077` — lane log; same, never a used-by entry.

Under a strict literal reading ("every file containing the token must be listed") the cell would be incomplete; under the lane's documented precedent it is exact. The validator checks only the forward direction and flagged nothing on the new rows (`.ufo/waves/round-40/assimilation/census-scratch.stdout`, `scratch_census_exit=0`; only pre-existing W01/W04 warnings unrelated to S152).

## Commands used

```
read corpus/SOURCES.md:121-123:raw
grep -rl 'S152' corpus/
grep -rl 'S152' --exclude-dir=.jj --exclude-dir=.ufo .
awk -F'|' '/^\|[[:space:]]*S[0-9]{3}/ {u=$12; if (u ~ /README|LOG\.md|lessons\/round-40/) print $2" => "u}' corpus/SOURCES.md   # zero hits
awk -F'|' '... $12 ~ /lessons/ ...' corpus/SOURCES.md   # 24 rows list lessons in used-by (S006–S104)
```

No lane checkout or shokuknow files were modified.
