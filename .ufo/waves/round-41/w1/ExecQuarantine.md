# ExecQuarantine — tameshi quarantine slice re-derived with the item-10 awk recipe

Seat: `L1Tameshi41.ExecQuarantine` (read-only). The only lane file written is this report; all
derivation ran under `/tmp/tameshi-r41-execquarantine/` and `/tmp/tameshi-r41-execquarantine-slice`.
Register read-only; `renumber-staged.py`, `merge-plan.py`, `quote-lint.py` and
`absent-defect-register.py` were not run.

## Finding

**17 rows. Every line carries an S-id (17/17).**

Ids, in slice (register) order:

```
S105 S109 S110 S118 S119 S124 S126 S129 S131 S132 S137 S140 S141 S143 S113 S123 S134
```

Numeric order is the same 17: `S105 S109 S110 S113 S118 S119 S123 S124 S126 S129 S131 S132 S134
S137 S140 S141 S143`.

Slice artifact: `/tmp/tameshi-r41-execquarantine-slice`, 4374 B, **17 lines**, 17 S-ids,
sha256 `20042ec3d93aceb9eb3ce42eeadcf2dfd72fae04473fd49c2e6f3cb6a68e38ff`.

## Exact command — the item-10 recipe

Filter as written at `corpus/lessons/round-40.md:51`
(`awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/'`):

```
awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md \
  > /tmp/tameshi-r41-execquarantine-slice
```

Register at derivation time, before and after every read:
`5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
(`sha256sum -c /tmp/tameshi-r41-execquarantine/register.before.sha256` → `OK`). The register was
not edited.

## The 17 rows

| register line | id | round | source table |
|---|---|---|---|
| `absent-defect-register.md:215` | S105 | round1 | ABSENT (`payload-absent`) |
| `:216` | S109 | round1 | ABSENT |
| `:217` | S110 | round1 | ABSENT |
| `:218` | S118 | round1 | ABSENT |
| `:219` | S119 | round2 | ABSENT |
| `:220` | S124 | round2 | ABSENT |
| `:221` | S126 | round2 | ABSENT |
| `:222` | S129 | round3 | ABSENT |
| `:223` | S131 | round3 | ABSENT |
| `:224` | S132 | round3 | ABSENT |
| `:225` | S137 | round4 | ABSENT |
| `:226` | S140 | round5 | ABSENT |
| `:227` | S141 | round5 | ABSENT |
| `:228` | S143 | round5 | ABSENT |
| `:363` | S113 | round1 | NEVER CHECKED |
| `:364` | S123 | round2 | NEVER CHECKED |
| `:365` | S134 | round4 | NEVER CHECKED |

## Why 17 and not 14, and what "carries an S-id" means here

- The register's own by-lane table (`absent-defect-register.md:240`) says tameshi has **14** rows —
  that is the ABSENT table only. The item-10 filter also matches the `Rows whose quotes were NEVER
  CHECKED` table, whose tameshi rows are 3. 14 + 3 = **17**.
- No tameshi row is missed and none is spurious: every line in the register with `` `tameshi` `` in
  `$2` is `215–228`, `240` (the by-lane totals row, excluded because `$3` is ` 14 ` and fails
  `/round[0-9]+/`) and `363–365`.
- Shape: 14 lines are 9-field ABSENT rows, 3 lines are 7-field NEVER-CHECKED rows; no line wraps.
- S-id coverage: yes, on every line. Caveat worth carrying: the three NEVER-CHECKED rows have a
  malformed id cell in the register itself — `S113\``, `S123\``, `S134\`` (a stray backtick, a
  defect of that table's formatting). The recipe still matches `$4 ~ /S[0-9]+/`, and
  `grep -oE 'S[0-9]{3}'` yields exactly one clean S-id per line.

## The recipe is the round-40 recipe, byte-for-byte

Same filter with the round-40 projection `print $4, $5`:

```
awk -F'|' -v l='tameshi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md \
  | cmp - .ufo/waves/round-40/assimilation/quarantine-slice   # exit 0
```

`cmp` is silent: the derived projection is **byte-identical** to the committed round-40 artifact
(17 lines, 583 B, sha256 `cb8270615417d23454552f32edd0d3d57a0c4028b4a4180537d6c74fc7e796ad`), id set
included. The register's tameshi content has therefore not moved since round 40.

## Lane-registry standing of the 17 ids (and the one live C1 hazard)

Status is column **8** of the 11-column row (`corpus/SOURCES.md:10` header); read with the
counter's own `registry()` under the current pin (`5ccb42d8…`, amendment A1).

| registry | S105 | S132 | the other 15 |
|---|---|---|---|
| base `a3d6c690…` (107 rows, max S152) | present, `mined` | present, `mined` | **absent** |
| work tree now (109 rows, max S154) | present, `mined` | present, `mined` | **absent** |

Consequence for C1 (measured, not inferred): any round-41 record — `corpus/lessons/round-41.md`,
the `## Round 41` SCORECARD section, or the `## 2026-10-25 — round 41` LOG section — that lists
these ids as bare S-ids adds **one m7 mismatch per absent id**. A synthetic record carrying all 17
scores `m7=15`; carrying only `S105` and `S132` scores `m7=0`. Amendment A3 is the same class: the
lesson's sentence "beginning at S153" replaced a bare unmined id for exactly this reason. So the
round-41 record should describe the slice by count and by the artifact path, not by enumerating its
15 unmined ids.

## Scratch probes (pre-run checks, not measurements)

Scratch lane: `git -C <lane> archive a3d6c690… | tar -x -C /tmp/tameshi-r41-execquarantine/lane`
(no `.git`, no lane write). Counter invoked from its lane path with `--lane <scratch> --rev work`.

| Probe | Lesson-41 content | Counter tail | m7 |
|---|---|---|---|
| A | cites `S105` (mined) | `m6=1 m7=0 m8=0 m9=1 total=2 records=1 sources_rows=107 rev=work` | 0 |
| B | cites nothing | same | 0 |
| C | lists all 17 slice ids | `m6=1 m7=15 m8=0 m9=1 total=17 records=1 sources_rows=107 rev=work` | 15 |
| D | `round-40 … six refused … ten present` | `m6=1 m7=0 m8=0 m9=0 total=1 records=1` | 0 |
| E | cites `S152` only | `m6=1 m7=0 m8=0 m9=1` | 0 |
| F | cites `S105` and `S132` only | `m6=1 m7=0 m8=0 m9=1` | 0 |

Allowed base-rev control on the live lane (not the deciding run):

```
python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690… C1_R41_PASS=false   (exit 1)
```

That is `claims.C1.before` exactly. Probe D also pins the m9 clear condition to its literal triple
(`round-40` + `six refused` + `ten present`); no S-id is needed for it.

## Concurrent state observed while working (not touched by this seat)

- `.ufo/evidence/round-41/calibration/measure.py` was re-pinned at 03:40:20 (`cells[9]` → `cells[8]`);
  the work-tree file now hashes `5ccb42d8a60d6d1e5e509a1ddb954a602d7e46476ee0355084810b48b8f08553`
  and matches the contract pin (amendment A1, `found_by` ExecC1Base). The pre-amendment pin
  `f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2` is the version ExecC1Base read;
  all slice and probe runs above used the corrected counter.
- `.ufo/evidence/round-41/census/measure.py` now hashes
  `83268eff97048cd4223a6f015b901c5efbde15d7b0d506bd40e5611b373ce94c`, matching the C2 pin
  (amendment A2).
- Consequence, stated once: the deciding run must hash the counter it executes; the pinned hash is
  the work-tree hash, not `d4ee4e6`'s blob.

## Scope discipline

- Register: read-only, byte-identical before/after (`sha256sum -c` → `OK`). No forbidden script run.
- Lane checkout: no edit, no Git/jj index touch, no sibling lane touch. The single lane write is this
  report.
- No counter run against the current tip: only `--rev a3d6c690…` and scratch `--rev work`.

## Tooling

No install or upgrade; `awk`, `python3`, `git`, `sha256sum`, `cmp` were already present. pacman
untouched per the host-wide pause.

## Risks / blockers

None for the slice: the derivation is complete, reproducible, and reproduces the round-40 artifact
byte-for-byte. The material C1 risk is the m7 arithmetic above (`m7=15` if the round-41 record
enumerates the unmined slice ids); it is reported, not remediated.

Report: .ufo/waves/round-41/w1/ExecQuarantine.md
