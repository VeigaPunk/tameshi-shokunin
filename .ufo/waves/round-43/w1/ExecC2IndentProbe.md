# ExecC2IndentProbe — independent reproduction of the m13 indent probe

Scope: reproduce, outside the lane tree, the load-bearing half of m13 — on a registry
mirror in which one data row is indented two spaces, the column-zero pattern counts N-1
while the census-valid 0-3-space pattern counts N. No lane file was written.

## Probe

Primary probe reads the **immutable freeze blob**, not the volatile working tree:
`git -C LANE show 17f6ef0c72ec27e1aea305b5c95806b43bb2caef:corpus/SOURCES.md`
(450 lines, 113 rows) into `/tmp/tameshi-r43-ExecC2IndentProbe-/`.

Row indented: **S001**, line 12 — `| S001 | Mutant states and metrics (Stryker Mutator docs) …`
became `  | S001 | …` (exactly two leading ASCII spaces).

```
$ diff pristine.md SOURCES.md            # pristine.md = the freeze blob
12c12
< | S001 | Mutant states and metrics (Stryker Mutator docs) …
>   | S001 | Mutant states and metrics (Stryker Mutator docs) …
$ diff <(grep -oE '^\| S[0-9]{3} \|' pristine.md) <(grep -oE '^\| S[0-9]{3} \|' SOURCES.md)
1d0
< | S001 |
```

## Counts

| file | (a) `grep -cE '^\| S[0-9]{3} \|'` | (b) `grep -cE '^ {0,3}\| S[0-9]{3} \|'` |
|---|---|---|
| pristine freeze blob (`17f6ef0:corpus/SOURCES.md`) | 113 | 113 |
| 2-space mirror (S001 indented two spaces) | **112** | **113** |
| 4-space control mirror (S001 at four spaces) | 112 | 112 |

- **Delta** on the 2-space mirror: (b) − (a) = **+1** (113 vs 112) — N vs N-1, exactly the
  m13 shape. The only row (a) loses is `| S001 |`.
- **Delta** on the 4-space control: **0** (112 vs 112) — four spaces is indented code and is
  ignored by *both* patterns, which is the documented boundary.

Replicated with the counter's own regexes
(`.ufo/evidence/round-43/calibration/measure.py:140-145`, `count_patterns`; the mirror is
built the way `indent_mirror` does at `measure.py:148-155`):
`pristine (113, 113)` → `2-space (112, 113)` → `4-space (112, 112)` — the same N-1/N split
`T2_indent_probe_load_bearing` (`measure.py:290-291`) asserts on its synthetic table.

Maintained CLI boundary check, read-only:
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh <dir> --file …/corpus/SOURCES.md`
prints `file rows 113` / `FLEET rows 113` (exit 0) on the 2-space mirror and `file rows 112`
on the 4-space mirror — two spaces accepted, four treated as indented code.

### Concurrent working-tree observation (risk, not the probe's baseline)

The lane's working-tree registry was being appended by a sibling seat during this seat's run.
A 07:53 snapshot of it carried **115** rows and reproduced the same invariant:
(a) = 114, (b) = 115, delta **+1**; `sources-census.sh` on that mirror reported `rows 115`.
That file is currently mid-flight (S159 present, S160 not yet written; mtime 07:53:57), which
is why the reported probe is pinned to the freeze blob instead of the working tree.

The standing command is accurate only because the committed registry is column-zero: the last
standing `sources-registry` row (`SCORECARD.md:2020`) reads
`` row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md`
→ 113 rows at round 42 `` and 113 is what (a) returns on the unindented freeze blob — the same
command under-counts the moment one row gains two spaces.

## What must not be edited

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/scripts/…` is **not to be edited — it does
not exist**. The lane has no `scripts/` directory at all:

```
$ ls -la /home/vgpnk/Projects/shokunin/tameshi-shokunin/scripts/
ls: cannot access '/home/vgpnk/Projects/shokunin/tameshi-shokunin/scripts/': No such file or directory   (exit 2)
```

The maintained census parser is a fleet-root file, outside the lane checkout and outside every
seat's writable lanes: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(35466 bytes, mtime 2026-10-19 21:22). It was only executed (`--file`, stdout) — nothing was
written to it, and no file under `/home/vgpnk/Projects/shokunin` was modified by this seat.

## Census clause accepting 0–3 leading spaces

`/home/vgpnk/Projects/shokunin/CORPUS.md:152-153`, under "Maintained parser note
(outside frozen v1)":

> The maintained `scripts/sources-census.sh` CLI accepts 0–3 leading ASCII spaces before
> Markdown table rows and headings; 4 or more spaces are indented code and are ignored.

Followed at `CORPUS.md:154` by: "The frozen manual census examples above assume column-zero
input and remain unchanged." The same rule is stated in the parser source,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:40-42`:

> `# Maintained parser accepts 0–3 leading ASCII spaces before Markdown rows/headings;`
> `# 4 or more spaces are indented code and ignored. Frozen manual examples assume`
> `# column-zero input.`

## Verification exercised

- `grep -cE` both patterns on the pristine freeze blob, the 2-space mirror and the 4-space
  control: `113/113`, `112/113`, `112/112`.
- `diff` pristine↔mirror: exactly line 12 (`12c12`), the S001 row; pattern-extract diff: only
  `| S001 |` is dropped by the column-zero pattern.
- Counter's own `count_patterns` regexes re-run over the three files: `(113,113)`,
  `(112,113)`, `(112,112)`.
- Maintained `sources-census.sh` on the 2-space and 4-space mirrors: `rows 113` / `rows 112`,
  exit 0.
- Working-tree snapshot at 07:53 (115 rows): `114/115`, CLI `rows 115` — same delta.

## Risks / limits

- Reproduction is on the real lane registry (113 rows at the freeze revision), not a synthetic
  table; the shape (one indented row, N-1 vs N) matches `T2_indent_probe_load_bearing`, so it
  corroborates that selftest rather than substituting for it.
- It says nothing about whether the standing command *text* is fixed at the deciding revision —
  that half of m13 belongs to the L1's deciding run.
- The lane registry is being mutated concurrently (see above); any measurement that reads the
  working tree rather than a revision is racy.
- Scratch `/tmp/tameshi-r43-ExecC2IndentProbe-/` deleted after measurement; no lane file, no
  jj/git index state and no fleet-repo file was touched. No tools installed or upgraded.
