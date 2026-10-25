# MutC2m13Prose — m13 command-cell attack (round 43, w2)

Seat: mutation-tester, calibration axis. Item: the m13 class gets the same treatment as
m12/m10 — a standing `sources-registry` row whose **backticked command is the column-zero
grep** while its prose says `0,3-space`, over a registry with **no indented rows**. Report
whether m13 fires, report the honest row, and report the `indent_mirror` probe counts
(column0 vs census-valid) on the real registry.

Counter under attack: `.ufo/evidence/round-43/calibration/measure.py`
sha256 `97609511bb77e97022d355c309a7bdc9ff7a2c74c48ac9622de600d1d28ef8d0`
= `claims.C2.counter_sha256` at the freeze (`self_pin=1` in every run below; selftest
`cases=12 failed=0`, `VERDICT: PASS`).

Revs used: `487b8f0da89fa0e2b8bea6930068accbf36e70a9` (base) and
`3aee2c078f8976499b587086af3577fc94dc8cf1` (freeze) only, plus **scratch commits** made in
`/tmp/tameshi-r43-w2-MutC2m13Prose-1` on top of the freeze. No counter was run at
`c5335c70bff750218b3a6db0a92daae76509a0de`; that tree is read only through `git show` for
row/count checks. The lane checkout was never written.

## 1. Baseline (pristine counter, unmodified bytes)

```
$ python3 .ufo/evidence/round-43/calibration/measure.py --lane . --rev 487b8f0 --freeze 3aee2c0
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=2 m13=1 total=3 records=3
sources_rows=113 standing=113 ... m13_probe=standing=6_column0=112_valid=113
rev=487b8f0... C2_R43_PASS=false first=m12:**Planned_(round_43):**
exit=1
```

```
$ python3 .ufo/evidence/round-43/calibration/measure.py --lane . --rev 3aee2c0 --freeze 3aee2c0
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 m13=0 total=8 records=4
sources_rows=114 standing=114 ... m13_probe=standing=7_column0=113_valid=114
rev=3aee2c0... C2_R43_PASS=false first=m7:corpus/lessons/round-43.md_unknown_S160
exit=1
```

Two things to read correctly: (a) at the freeze **m13=0** — the honest round-43 row is clean;
(b) `total` is non-zero at the freeze because m7/m8 fire on the freeze's record set, not
because of m13. The m13 field is the measured quantity throughout; the direct-call output
(`m13_standing_command(...)`) is printed beside each counter line so the m13 arm cannot be
read through the m7/m8 noise.

## 2. The shape the item names — **m13 FIRES** (mutant killed)

Scratch rev `9d90fc3ba2f0ec8291f6edbd69d97b65fcce14d0` (`M13-A`), newest standing row
(`SCORECARD.md:2081` equivalent) rewritten to carry the **column-zero** command in backticks
while the prose says `0,3-space`; registry unchanged, **0 indented rows**, 114 rows,
column0 = census-valid = 114:

```
| sources-registry | … `sources-census.sh validate --root … tameshi` → exit 0, zero E codes;
row count from the column-zero command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md`
→ 114 rows at round 43 (the census-valid 0,3-space pattern is the form the census accepts;
the counter reads the last standing row) ; `corpus/SOURCES.md` | … |
```

```
$ python3 .ufo/evidence/round-43/calibration/measure.py --lane . --rev 9d90fc3 --freeze 3aee2c0
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 **m13=1** total=9 …
m13_probe=standing=7_column0=113_valid=114 … C2_R43_PASS=false first=m7:…
exit=1
direct call: m13 hits = ['standing command is column-zero only']
```

`M13-A2` (`8355a6174cfe75790f41e57fd668da1ea1ebfbe8`) puts the same prose in its own
backticks *without* the word `grep` (`` `0,3-space` ``): also fires,
`m13=1`, hit `['standing command is column-zero only']`. So the item's shape is detected:
the extractor only ever treats a backticked span as a command when it contains `grep`
(`measure.py:186`), and the row's real command has no `0,3` (`measure.py:189`).
Verdict: **killed**. The registry's indent state is irrelevant to this arm.

## 3. Survivals — the counter's own comment claims this shape is caught, and it is not

`measure.py:183-185` states the intent: *"a row that carries the column-zero command and a
prose mention of `0,3` is the round-42 shape the class exists to catch"*. The predicate is
`any('0,3' in span for span in commands)` (`measure.py:189`) — existential over spans, and a
**substring** test. Two plausible defects survive:

**M13-B** (`36538e8da5bae3e633005e1c701c1a48ba9382a0`) — the load-bearing count is still the
column-zero command; a second backticked span merely *shows* the census-valid grep:

```
row count from the column-zero command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md`
→ 114 rows at round 43 (the census-valid 0,3-space form is
`grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md`; …)
```

```
spans = ["grep -cE '^\\| S[0-9]{3} \\|' corpus/SOURCES.md",
         "grep -cE '^ {0,3}\\| S[0-9]{3} \\|' corpus/SOURCES.md"]
counter: m13=0  (direct call: hits = [])
```

**M13-C** (`7c6906f5534886bd68d5de145fedf674aff430be`) — one span, column-zero grep with the
`0,3` only in a trailing comment:

```
`grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md  # 0,3-space form`
```

```
counter: m13=0  (direct call: hits = [])
```

Both are the class's stated hazard (a command cell that *mentions* the census-valid pattern
without using it) and both read as clean. Fix shape is small and mechanical: require the
span to carry the regex form (`\^ \{0,3\}\|` / `[ ]\{0,3\}`) as a *pattern*, or bind the check
to the span that actually produces the stated count, instead of the `'0,3' in span` substring
at `measure.py:189`.

## 4. False positives — the probe measures the live registry, not a mirror

The class sentence: *"an indented-row mirror proves the difference (column0 = N-1,
census-valid = N)"*. The implementation builds the mirror **from the live registry** and
requires `valid == column0 + 1` (`measure.py:191-194`). With k pre-existing census-valid
indented rows the mirror delta is `k+1`, so any k ≥ 1 fires:

**M13-D** (`188ddd25f26aa5ed9b3ba04da3d1212c1644ca53`) — one row (`S001`) indented two
spaces. That is a *census-valid* row: fleet `CORPUS.md:152-154` — *"The maintained
`scripts/sources-census.sh` CLI accepts 0–3 leading ASCII spaces before Markdown table rows
and headings"*. Standing row is the honest census-valid one.

```
real registry: column0=113, census-valid=114, rows()=114
counter: m6=0 m13=1 total=9
direct call: m13 hits = ['indent probe not load-bearing (column0=112 valid=114)']
m13_probe=standing=7_column0=112_valid=114
```

**M13-E** (`e2969c8668145e346afc7ec3f6679eb8d0e5f1ee`) — every row inside the legal 0–3 band
(2 spaces); still 114 census rows, still a census-valid document:

```
real registry: column0=0, census-valid=114 ; mirror: column0=0, valid=114
counter: m13=1   direct call: ['indent probe not load-bearing (column0=0 valid=114)']
```

The counter already knows how to do this correctly: selftest `T2_indent_probe_load_bearing`
(`measure.py:316-321`) builds a **synthetic two-row registry** and asserts 1/2. Running the
probe on that synthetic mirror (or on `registry_text` only after asserting zero indented
rows) removes both false positives without touching the class.

## 5. Blind spot — the newest standing row must start at column zero

**M13-G** (`30b2a643bcd609b1e2b1dab22a485df9da55d151`) — the honest round-43 row indented two
spaces (legal markdown, legal census; command unchanged):

```
standing rows visible to the counter: 6 (the round-43 row is invisible)
counter: m6=1 m13=1
direct call: m13 hits = ['standing command is column-zero only']
```

`standing_registry_rows` (`measure.py:143-149`) uses `line.startswith('| sources-registry |')`.
That contradicts the counter's own row scanner, which accepts 0-3 leading spaces
(`measure.py:99`, `measure.py:412-413`). So a census-valid round-43 row silently demotes m13
(and m6) to the round-42 column-zero row. Narrower than the class sentence ("the newest
standing row").

## 6. Class ceiling — the cited command is never executed or simulated

**M13-H** (`214399d11740ba60fa251489b01c2d53071f210d`) — honest row, plus one registry row
respaced to `|  S001 |` (two spaces after the pipe; intra-row whitespace, still one row):

```
honest cited grep  grep -cE '^ {0,3}\| S[0-9]{3} \|'          → 113
lane census v2     grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' → 114
counter: m6=0 m13=0 (sources_rows=114, m13 hits = [])
```

Both m6 and m13 agree with the row while the row's own command returns 113. m6 compares the
*stated* number to the counter's `\s*` count (`measure.py:412`), and m13 only greps the
literal text for `0,3`; neither re-derives the count from the cited command. So "census-valid
command" is a text property here, not a measured one. (Under the class sentence this is a
ceiling, not a violation — the sentence only asks the command to *name* the 0-3-space
pattern — but it is what "load-bearing" would have to mean.)

## 7. `indent_mirror` probe counts on the real registry

| text | column0 (`^\|\s*S\d{3}\s*\|`) | census-valid (`^ {0,3}\|\s*S\d{3}\s*\|`) | rows |
|---|---|---|---|
| live `corpus/SOURCES.md` @ freeze `3aee2c0` | **114** | **114** | 114 |
| live `corpus/SOURCES.md` @ `c5335c7` (read-only `git show`) | **114** | **114** | 114 |
| indented rows (1-3 spaces) in either | 0 | — | — |
| `indent_mirror(live)` (first column-zero row + 2 spaces) | **113** | **114** | 114 |

So on the real registry the two counts are **equal (114 = 114)**; the `+1` difference exists
only on the constructed mirror, and the counter prints it as
`m13_probe=standing=7_column0=113_valid=114`. That is the class as designed — but §4 shows
the probe is entangled with live registry shape, and §5 shows the standing-row extractor does
not honour the same 0-3-space rule the probe exists to defend.

## 8. The honest row

Byte-identical at the freeze and at the records commit (verified with `git show … | grep |
tail -1` on both; diff empty), `SCORECARD.md:2081`:

```
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows,
mined into admitted entries, census-gated | `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → exit 0, zero E codes; row count from the
census-valid command `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → 114 rows at
round 43 (the column-zero form of this command is what C2 class m13 replaced; the counter
reads the last standing row) ; `corpus/SOURCES.md` | fleet round 1 (kaika) |
```

Measured: m13 hits = `[]`, `standing=7 column0=113 valid=114`, stated 114 = census-valid 114
at `c5335c70` (read-only `git show` count: 114/114). The row is honest **for the current
registry**, which has no indented rows; its load-bearing sentence is exercised only by the
synthetic mirror, and per §6 it would still under-count a census row written with intra-row
spacing. The row is not changed by this seat; the recommendations below are for the L1.

## 9. Verdict table

| mutant | shape | expected detector | actual | verdict |
|---|---|---|---|---|
| M13-A `9d90fc3` | column-zero backticked command + unbackticked prose `0,3-space`, 0 indented rows | m13=1 | `m13=1`, `['standing command is column-zero only']` | **killed** |
| M13-A2 `8355a61` | same, prose in its own backticks without `grep` | m13=1 | `m13=1`, same hit | **killed** |
| M13-B `36538e8` | column-zero command load-bearing + decoy backticked census-valid grep | m13=1 | `m13=0`, `[]` | **SURVIVED** |
| M13-C `7c6906f` | one span: column-zero grep + `# 0,3-space form` | m13=1 | `m13=0`, `[]` | **SURVIVED** |
| M13-D `188ddd2` | honest row + one census-valid 2-space indented row | m13=0 | `m13=1`, `['indent probe not load-bearing (column0=112 valid=114)']` | **false positive** |
| M13-E `e2969c8` | honest row + all rows in the 0-3 band | m13=0 | `m13=1`, `['indent probe not load-bearing (column0=0 valid=114)']` | **false positive** |
| M13-G `30b2a64` | honest row itself indented 2 spaces (census- and markdown-valid) | m13=0 | `m13=1` (+`m6=1`), grades the round-42 row | **false positive / blind spot** |
| M13-H `214399d` | honest row + one row with two spaces after the pipe | m13=0 (and cited command re-derives 114) | `m13=0`, `m6=0`, cited command returns 113 | **ceiling** (class passes a command that under-counts) |

Root causes, all in one function: `measure.py:186` (`grep`-in-span classification),
`measure.py:189` (existential substring `'0,3'`), `measure.py:191-194` (probe over the live
registry), `measure.py:143-149` (column-zero-only standing-row scanner).

Minimal repairs (code, no contract change): (1) require the census-valid regex form in the
span that carries the designated command, not the substring `0,3`; (2) compute the probe on
the synthetic mirror already used by selftest T2, not on `registry_text`; (3) let
`standing_registry_rows` accept ` {0,3}` like the rest of the counter; (4) to close M13-H,
derive the count from the cited command (or its parsed pattern) and compare to `valid_count`.

## 10. Restoration / non-contamination evidence

- Lane checkout untouched. `git status --porcelain -- SCORECARD.md corpus/SOURCES.md
  .ufo/evidence/round-43/calibration/measure.py` in the lane → empty. sha256 before and
  after: `SCORECARD.md 98517d02d111188d544fbefb2a2014c12103ad2c6b960f59021437f41957a297`,
  `corpus/SOURCES.md c50ca1fbce6b1afb769735793d2ca520d05e5e8a830fd3ea88a7c48fb4c961fd`,
  counter `97609511bb77e97022d355c309a7bdc9ff7a2c74c48ac9622de600d1d28ef8d0` (all
  unchanged).
- All edits were commits in the disposable clone `/tmp/tameshi-r43-w2-MutC2m13Prose-1`
  (`git clone --shared`); the directory is deleted before this seat returns, per item.
- No counter run used `--rev c5335c70`; that tree was only read with `git show`.
- No tool installed or upgraded (python3 stdlib + git only); pacman not used.
