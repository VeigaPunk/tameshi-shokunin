# ExecRowFormat — format of the two round-41 draft rows (S153, S154)

Seat: `L1Tameshi41.ExecRowFormat` (executor, read-only). Milestone: Row format.
Axes walked: (1) column arity + pipe safety, (2) temporal-cell grammar (`opened`
ISO, `recheck` NNd/ISO/symbolic), (3) `used-by` naming only admitted files.

## What I actually checked

At check time (`2026-10-25T03:42:42-03:00`) neither `.ufo/waves/round-41/w1/ExecScratchValidate.md`
nor `ScribeSources.md` existed, so I checked the rows as they stand in the lane
working tree — which is the draft the ExecScratchValidate item asks for, byte for byte:

- `corpus/SOURCES.md:123` (S153), `corpus/SOURCES.md:124` (S154)
- `corpus/SOURCES.md` sha256 `9b73ec116913d73e85ec65197c39bc95d25ce6edb349cf40bbe96450cbecb705`
  (unchanged before and after every command below; snapshot copy
  `/tmp/tameshi-r41-execrowformat-snap/SOURCES.md` has the same sha)
- the two-line pair alone: sha256 `d6855fe3c96ea566a24963b2f020aa2912852bb780f03825d43b3dcd2c8cfb6b`

Print-ready text as landed (one line each; line numbers on the left are mine, not the file's):

```markdown
| S153 | ast — Abstract Syntax Trees (Python 3.14 documentation) — https://docs.python.org/3/library/ast.html | docs | A | CPython's own ast module: node types and source recovery for a parsed module | §Abstract Syntax Trees and §ast.get_source_segment @ docs page fetched 2026-10-25, snapshot .ufo/evidence/round-41/sources/ast.html | a parsed tree exposes Name, Assign, Call and attribute nodes; ast.get_source_segment recovers a node's source; iter_child_nodes and NodeVisitor walk the tree | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |
| S154 | pathlib — Object-oriented filesystem paths, Path.write_text (Python 3.14 documentation) — https://docs.python.org/3/library/pathlib.html | docs | A | Path.write_text and write_bytes: the file the method is called on is the destination | §Path.write_text @ docs page fetched 2026-10-25, snapshot .ufo/evidence/round-41/sources/pathlib.html | write_text opens the file pointed to in text mode, writes the data and closes the file, so the receiver expression is the destination path | mined | 2026-10-25 | 180d | corpus/knowledge/r41-variable-destination-writes.md |
```

## Checks, observed values

| # | check | command | observed | verdict |
|---|---|---|---|---|
| 1 | `awk -F'\|'` field count 13, each | `awk -F'\|' '/^\|[:space:]*S15[34][[:space:]]*\|/ {printf "%s NF=%d\n",$2,NF}' corpus/SOURCES.md` (snapshot copy) | `S153 NF=13`, `S154 NF=13` | **PASS** |
| 2 | no literal pipe inside a cell | `awk '/^\|…S15[34]…/ {print gsub(/\|/,"\|")}' ` | 12 pipes per row = 1 leading + 10 separators + 1 trailing; 11 content cells, `empty=0` each | **PASS** |
| 3 | no escaped pipe | `grep -E '…S15[34]…' \| grep -cF '\|'` | `0` escaped pipes | **PASS** |
| 4 | no entity/fullwidth pipe standing in for one | `grep -E '…S15[34]…' \| grep -cE '&#124;\|&vert;\|｜'` | `0` | **PASS** |
| 5 | `opened` is ISO | cell 10 = `2026-10-25`; `^\d{4}-\d{2}-\d{2}$` → 1; `>= "2026-10-19"` (round-start guard carried from `sources-census.sh`) → 1 | both rows `iso=1 ge_round_start=1` | **PASS** |
| 6 | `recheck` is ISO / `NNd` / symbolic | cell 11 = `180d`; `^\d+d$` → 1; ISO → 0; symbolic `on-(release\|change)` → 0 | both rows `recheck=[180d] nnd=1` | **PASS** |
| 6b | `NNd`/symbolic vocabulary in use across the registry | `awk -F'\|'` tally of cell 11 over all 109 rows | `90d=11 180d=36 365d=25 730d=12 on-change=3 on-release=22` — `180d` is the largest admitted class, so the token is not invented | **PASS** |
| 7 | `used-by` shape | cell 12 = `corpus/knowledge/r41-variable-destination-writes.md`; `split(/[,;]/)` → 1 token, no wildcard/glob/space | both rows `tokens=1` | **PASS** |
| 8 | `used-by` names an admitted file | see "Admission" below | worktree file exists, coverage-map row present, note cites both ids; file is **untracked** and **absent at both frozen revs** | **PASS only once committed** (see F2) |
| 9 | E03 / E04 cross-check (informational, not my milestone) | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` from the lane root | exit `0`, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `A rows` 109, `A malformed` 0, `A tiers` A=97 B=9 C=3, `A status` mined=81 queued=22 rejected=6, dup ids empty, enum/tier-inflation empty, mined used-by missing empty, B2 empty; `SOURCES.md` sha identical before/after (the census wrote nothing) | **PASS** |
| 9b | no reopen of an existing id (E04) | `git show <rev>:corpus/SOURCES.md \| grep -cE '^\|[:space:]*S15[34][[:space:]]*\|'` for `a3d6c69` and `d4ee4e6` | `0` at both revs → S153/S154 are unused ids at base and freeze | **PASS** |
| 10 | rows sit inside the Registry table and look like its rows | `sed -n '122,128p' corpus/SOURCES.md \| cat -A`; `grep -n '^## Paths' corpus/SOURCES.md` | `:122` S152, `:123` S153, `:124` S154, blank, `## Paths` at `:126` — appended after the last existing row, no row displaced, no trailing space (`sed -n '123,124p' … \| grep -c ' $'` → `0`), em-dash bytes `M-bM-^@M-^T` intact in both `source` cells | **PASS** |

B1 (informational, strict id-cite) lists 25 legacy rows `S031`–`S037`; **neither S153
nor S154 appears**, so the two new rows carry an id-cite in their `used-by` file under
both the strict (B1) and the id-or-path (B2, exit-gating) rule.

## Admission (check 8, observed)

```
worktree: corpus/knowledge/r41-variable-destination-writes.md EXISTS   (git: untracked)
rev a3d6c69: ABSENT    rev d4ee4e6: ABSENT
coverage-map row: PRESENT at corpus/README.md:517  (NF=5 → 3 cells; Sources cell = "S153, S154")
H4 id-cite S153+S154 in the note: yes   (note lines 1-2 are `source: S153 …` / `source: S154 …`)
corpus/README.md sha256 b7e26a9b444675e90c46cfeb0d15ba288fedf4cf3c45bf26314f2e6a5b3c31ed
```

`corpus/README.md:517` was mid-write when I first read it (only two content cells,
`S153, S154` missing); re-read seconds later it is complete. The value above is the
complete one.

## Verdict

**Format: PASS on every check I was given.** No cell in either row contains a literal
pipe (`|`), an escaped pipe (`\|`), or a pipe entity; both rows carry exactly 11
non-empty content cells (`awk -F'|'` NF=13 with the two empty edge fields); `opened` is
ISO `2026-10-25`; `recheck` is `180d`, a member of the registry's own `NNd` class;
`used-by` names exactly one path.

**Admission: conditional PASS.** The `used-by` path resolves in the working tree and is
indexed in the coverage map, but the note is untracked, so at the base (`a3d6c69`) and
freeze (`d4ee4e6`) revisions the cell names a file that does not exist. The row is
correct only if the note lands in the same commit as the rows.

## Findings

**F1 (in scope): no row-format defect.** The two rows are print-ready as they stand.

**F2 (in scope, dependency for C1):** `used-by` is only true once
`corpus/knowledge/r41-variable-destination-writes.md` is committed with the rows.
If it is not, two instruments fire at the measurement revision: the `SOURCES` census
`A mined used-by missing` check (`[ -e "$p" ]`), and C1 `m8`, whose scanned path prefixes
include `corpus/` (`.ufo/evidence/round-41/calibration/measure.py:41-45`, `PATH_PREFIXES`).
The round-41 lesson already cites the note path, so a commit that omits the note fails `m8`.

**F3 (out of my milestone, decisive for C1's deciding run — route to L1):** the pinned C1
counter reads the **wrong column** for row status.

- Frozen bytes (`d4ee4e6`, sha256 `f00917dd…` = the contract's `counter_sha256`):
  `.ufo/evidence/round-41/calibration/measure.py:137`
  `status = cells[9].strip() if len(cells) > 9 else ''`, on `cells = line.split('|')`.
- `cells[0]` is the empty field before the leading pipe, so the header order
  `id source kind tier scope anchor teaches status opened recheck used-by` maps to
  `cells[1]…cells[11]`: `cells[8]` is **status**, `cells[9]` is **opened**.
- Replicated in scratch (no counter run): with `cells[9]`, `S153='2026-10-25'`,
  `S154='2026-10-25'`, and `mined` count = **0 of 109**; with `cells[8]`,
  `S153='mined'`, `S154='mined'`, `mined` count = **81 of 109**.
- Consequence: `m7` (".ufo/…/measure.py:226-235") flags every S-id cited by a round-41
  record as `status=<opened-date>`. Against the current round-41 lesson the replication
  yields **m7 = 3** (`S001`, `S153`, `S154`) with `cells[9]`, and **m7 = 0** with
  `cells[8]`.
- The working tree already carries an uncommitted fix (`cells[8]`, same line 137,
  sha256 `5ccb42d8…`), plus two more dirty counter artifacts:
  `.ufo/evidence/round-41/census/measure.py` `83268eff…` vs pinned `5d57c709…`
  (adds a `symlink_arg` mutant term at `:36-37`, `:188`, `:257`, `:285`), and
  `.ufo/evidence/round-41/census/fixtures.json` `20b6254d…` vs pinned `a4123ce3…`.
  So the deciding run must choose between *pinned-but-off-by-one* and
  *fixed-but-unpinned* — a contract decision, not a seat edit. Nothing was changed by
  this seat.

## Touched surfaces

- Written: this report only. Scratch: `/tmp/tameshi-r41-execrowformat-snap/`
  (`SOURCES.md` sha `9b73ec11…`, `rows.txt` sha `d6855fe3…`, `check.sh` sha
  `ad7ef122827c1a8bec9fdf875d574ed12c72ae4b6249c45dd438311fa79f1e25`, present at `03:46`);
  it is a convenience copy only — every observed value, both row texts and every command
  are inlined above, and no `.ufo/waves/round-35/` path is cited, so this report does not
  depend on that lane's scratch tree in either location.
- Read: `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/r41-variable-destination-writes.md`,
  `corpus/lessons/round-41.md`, `.ufo/evidence/round-41/contract.json`,
  `.ufo/evidence/round-41/{calibration,census}/measure.py`, `census/fixtures.json`,
  `.ufo/evidence/kaika-round-1/sources-census{,-v2}.sh`, `.ufo/waves/round-41/{spec,dispatch}-w1.json`.
- Not edited: the lane checkout (`corpus/SOURCES.md` sha unchanged), the fleet repo, sibling
  lanes, jj or the Git index. Neither counter was run in any mode (`--rev`, `--control`,
  `--selftest`, `--rev work`); the m7/m6 numbers above come from a scratch replication of
  `registry()`'s own two lines.
- Installs/upgrades: none.

## Reproduction

```bash
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
# 1-4 field count and pipe safety
awk -F'|' '/^\|[[:space:]]*S15[34][[:space:]]*\|/ {printf "%s NF=%d pipes=%d\n",$2,NF,NF-1}' corpus/SOURCES.md
grep -E '^\|[[:space:]]*S15[34][[:space:]]*\|' corpus/SOURCES.md | grep -cF '\|'   # want 0
# 5-6 temporal cells
awk -F'|' '/^\|[[:space:]]*S15[34][[:space:]]*\|/ {o=$10;r=$11;gsub(/[[:space:]]/,"",o);gsub(/[[:space:]]/,"",r);print $2,o,r,(r ~ /^[0-9]+d$/)}' corpus/SOURCES.md
# 7-8 used-by
awk -F'|' '/^\|[[:space:]]*S15[34][[:space:]]*\|/ {u=$12;gsub(/^[[:space:]]+|[[:space:]]+$/,"",u);print $2, split(u,a,/[,;]/), a[1]}' corpus/SOURCES.md
git cat-file -e d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937:corpus/knowledge/r41-variable-destination-writes.md || echo "ABSENT at freeze"
# 9 census (read-only; sha unchanged after)
sha256sum corpus/SOURCES.md && bash .ufo/evidence/kaika-round-1/sources-census-v2.sh; sha256sum corpus/SOURCES.md
# F3 column off-by-one
git show d4ee4e6:.ufo/evidence/round-41/calibration/measure.py | sed -n '137p'
```

Report: .ufo/waves/round-41/w1/ExecRowFormat.md
