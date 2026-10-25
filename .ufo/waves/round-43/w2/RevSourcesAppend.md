# RevSourcesAppend — round 43, wave 2

author: seat `L1Tameshi43.RevSourcesAppend` (reviewer, leaf member; no dispatch)
date: 2026-10-25
item: verify the round-43 append in `corpus/SOURCES.md` (S159 row shape, used-by
citations, the three extended used-by cells, the tail note's row count, the
`Next unused id` pointer).
milestone: registry append shape. judged on: calibration.

Axes named: (1) **shape** — cells per row and the absence of a cell-internal `|`;
(2) **citation closure** — every written `used-by` names a file that names the id;
(3) **count closure** — the note's arithmetic equals a mechanical recount;
(4) **append-only** — no cell outside `used-by` moved, no line deleted.

Rev discipline: every read used `487b8f0da89fa0e2b8bea6930068accbf36e70a9` (base)
or `3aee2c078f8976499b587086af3577fc94dc8cf1` (freeze) only. No counter was run;
`c5335c7` was never read or executed. Working tree `corpus/SOURCES.md` is
byte-identical to the freeze (`git diff --stat 3aee2c0 -- corpus/SOURCES.md`
prints nothing), so the freeze blob is what was audited.

## Verdicts against the five checks

| # | check | verdict |
|---|---|---|
| 1 | S159 has 11 cells, no `|` inside a cell | **PASS** |
| 2 | S159 `used-by` names a file that cites S159 | **PASS** |
| 3 | S089, S155, S158 `used-by` each name the new entry | **PASS** |
| 4 | tail note's 114 = `grep -cE '^ {0,3}\| S[0-9]{3} \|'` | **PASS** |
| 5 | `Next unused id` = the smallest unused id | **FAIL as worded**; PASS under the operative rule (F1) |

The append itself is clean: three `used-by` cells extended in place, one row
added, one note block added, nothing else touched.

## Findings

### F1 (medium, calibration) — "the smallest unused id" is false of this registry, so check 5 is unsatisfiable as worded

`corpus/SOURCES.md:456` says `- Next unused id: S160.` That is `max(id)+1`,
**not** the smallest unused id. The registry's smallest unused id is `S038`;
excluding the two ids the file itself retires (`:276-278`), it is `S098`;
excluding the round-32 id recorded as never written (`:406`), it is `S109`.
There are 45 gaps.

```bash
awk -F'|' '/^ {0,3}\| S[0-9]{3} \|/{gsub(/^ +| +$/,"",$2); sub(/^S/,"",$2); print $2+0}' \
  corpus/SOURCES.md | sort -n \
| awk 'BEGIN{e=1} {while(e<$1){printf "S%03d ",e; e++} if($1==e)e++} END{print ""}'
# → S038 S039 S098 S109 … S131 S133 … S151      (45 ids)
```

Both readings are load-bearing and they disagree:

- **Operative (PASS).** `CORPUS.md:89` — "`id` — `S` + 3 or more digits, the
  next unused; never reused". The corpus's own practice is that gaps are never
  backfilled (all 45 above predate later ids), and the lane's frozen guard
  computes the same number as a field: `python3 -I tools/staged-id-guard.py
  --registry corpus/SOURCES.md --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json`
  → `"registry_max": "S159", "next_free": "S160"`, `"registry_rows": 114`.
- **Literal (FAIL).** `S160 ≠ S038 ≠ S098 ≠ S109`.

The literal reading is not merely false, it is unsatisfiable: writing `S038`
would breach `CORPUS.md:89`'s "never reused" for a retired id, and writing
`S109` would backfill an id the append-only pointer history already skipped.
**Recommendation:** state the invariant as `max(id)+1`, which is what the
registry, the lesson (`corpus/lessons/round-43.md:78-80`: "S160 is the next
unused id") and the frozen guard all mean. If a wave-2 scorecard records
"`Next unused id` is the smallest unused id" as PASS, that cell is false and
must not be signed.

Severity is medium, not high: the append is correct under the contract; the
check's wording is the defect. No id was misallocated (`S159` is unused at base
and used exactly once at freeze — `grep -cE '^ {0,3}\| S159 \|' corpus/SOURCES.md`
→ 1).

### F2 (low, wave-1 artifact) — `CritC3Maps.md:175` counts 45 gaps but enumerates 44

`.ufo/waves/round-43/w1/CritC3Maps.md:175-176`:

> Local evidence for that reading: the registry's 45 gaps (S038, S039, S098,
> S109–S130, S133–S151) are never backfilled while later ids exist

`S131` is missing from the enumeration: `S109–S130` is 22 ids, so the list is
`2 + 1 + 22 + 19 = 44`, while the stated count 45 is the correct one (the
command in F1 emits `S131` as a gap; `S132` and `S152` are rows at `:121` and
`:122`). The file's conclusion is unaffected; its evidence list is off by one
and would not reproduce its own number.

```bash
awk -F'|' '/^ {0,3}\| S[0-9]{3} \|/{gsub(/^ +| +$/,"",$2); print $2}' corpus/SOURCES.md \
| grep -c '^S13[12]$'          # → 1  (only S132; S131 is a gap)
```

### F3 (low, documentation arithmetic) — the note's collision decomposition does not close after the append

`corpus/SOURCES.md:454` gives the pre-append breakdown and then the
post-append count, but leaves the post-append breakdown unstated:

> `tools/staged-id-guard.py` reports 6 collisions … `S153`–`S158` — of which 2
> are documents the registry already holds … and 4 are new documents. After
> this round's append the collision set is `S153`–`S159` (7 ids)

7 ids with "2 held + 4 new" accounts for 6. The seventh is `S159`, which the
append turns into a **third held document** (`staged:S159` → registry `S155`).
The lesson has it right (`corpus/lessons/round-43.md:82-86`: "**7 collisions**
`S153`–`S159`, of which **3 are documents the registry already holds** … and 4
are new"), so `SOURCES.md` and the lesson disagree in decomposition while
agreeing on 7. Not a false number — a reader-facing gap a falsifier will hit.

```bash
python3 -I tools/staged-id-guard.py --registry /tmp/SOURCES.base.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
#  base (113 rows): collision_count 6, held {S153:S105, S154:S106}            → 2 held + 4 new
python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
#  freeze (114 rows): collision_count 7, held {S153:S105, S154:S106, S159:S155} → 3 held + 4 new
```

(`/tmp/SOURCES.base.md` = `git show 487b8f0:corpus/SOURCES.md`.)

## Checks that pass, with the evidence

**P1 — 11 cells, no cell-internal `|`.** The row is one physical line of 670
bytes with 12 separators, 11 cells, zero empty cells, no `\|`, no trailing
whitespace; the header at `:11` has the same 11 columns in the same order.

```bash
awk -F'|' '/^ {0,3}\| S159 \|/{printf "line %d NF=%d cells=%d\n", NR, NF, NF-2}' corpus/SOURCES.md
# → line 129 NF=13 cells=11
awk -F'|' '/^ {0,3}\| S[0-9]{3} \|/{print NF-2}' corpus/SOURCES.md | sort | uniq -c
# → 114 11        (every row, not just S159: no row carries a 12th field, so no cell
#                  contains an unescaped `|` — awk -F does not honour `\|`)
```

Cells, in header order: `S159` / Wikipedia source+URL / `docs` / `A` / scope /
anchor (`snapshot … 170793 B sha256 6e4a06c0 revid 1373580212`) / teaches /
`mined` / `2026-10-25` / `180d` / `corpus/knowledge/r43-survivor-resolution-rule.md`.

**P2 — `used-by` names a file that cites S159.** The target exists in the freeze
tree and cites the id three times, twice with located bytes:

```bash
git show 3aee2c0:corpus/knowledge/r43-survivor-resolution-rule.md | grep -n 'S159'
# → 3:  source: S089 (held, re-opened), S159 (new); S155 (held), S158 (held)
# → 24: - Wikipedia (new S159, opened 2026-10-25): "Equivalent mutants detection is one
# → 103:- Not Wikipedia's taxonomy. S159 defines equivalence behaviourally and has no
```

The quoted sentence is in the committed snapshot, and the anchor's pin matches
the bytes on disk (`170793` B, `sha256 6e4a06c0…`), so this is a byte-backed
citation and not a bare id mention:

```bash
sha256sum .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html
# → 6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43
git cat-file -e 3aee2c0:.ufo/evidence/round-43/sources/wikipedia-mutation-testing.html && echo committed
grep -c 'Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing' \
  .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html        # → 1
```

The URL is carried by exactly one row (`grep -c 'en.wikipedia.org/wiki/Mutation_testing'
corpus/SOURCES.md` → 1), so the round-43 withdrawal of the Stryker row (whose
URL S089 already holds, `:98`) left no duplicate.

**P3 — the three extended cells each name the new entry, and only cell 11 moved.**
Cell-level diff of base→freeze:

```bash
git diff 487b8f0da89fa0e2b8bea6930068accbf36e70a9 3aee2c078f8976499b587086af3577fc94dc8cf1 \
  -- corpus/SOURCES.md | awk -F'|' '/^[-+]\| S(089|155|158) \|/{d=substr($0,1,1); id=$2; ub=$12;
  gsub(/^ +| +$/,"",id); gsub(/^ +| +$/,"",ub); printf "%s %s [%s]\n", d, id, ub}'
```

```
- S089 [corpus/knowledge/mutation-case-kumitate-cite-check.md]
+ S089 [corpus/knowledge/mutation-case-kumitate-cite-check.md, corpus/knowledge/r43-survivor-resolution-rule.md]
- S155 [corpus/knowledge/pit-outcome-vocabulary.md]
+ S155 [corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r43-survivor-resolution-rule.md]
- S158 [corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r42-attribute-and-outflag-destinations.md]
+ S158 [corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r42-attribute-and-outflag-destinations.md, corpus/knowledge/r43-survivor-resolution-rule.md]
```

This matches `corpus/SOURCES.md:453` and `corpus/lessons/round-43.md:89-93`
old→new word for word. `--numstat` is `9 3`, and a cell-wise comparison of each
`-` row against its `+` row reports **differing cell indexes `[11]`** for all
three — every other cell is byte-identical, so no status, recheck, anchor or
teaches cell was touched and no line was deleted except the three rewritten
rows. That is the append-only shape `QUALITY.md` criterion 35 asks for. The new
entry cites all three ids in the body as well as the `source:` trio
(`S089`×3, `S155`×2, `S158`×4, `S159`×3), and its S158 line numbers are exact
against the committed PIT bytes (`:71-72` the EQUIVALENT doc comment, `:75`
`EQUIVALENT(true);`).

**P4 — the note's count equals the mechanical count.**

```bash
grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md                 # → 114  (= note's 114)
git show 487b8f0:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3} \|'  # → 113  (= note's "Rows 113 → 114")
```

The census receipts corroborate the row-count claims without restating them
(both `.ufo/evidence/round-43/census-sources/start.stdout` and `after.stdout`
are byte-identical, 1015 B, `start.exit` = `start_exit=0`; code tally
`1 ok / 1 W01 / 9 W04`, zero E codes, matching `corpus/lessons/round-43.md:97-98`
and the note's "same warning set plus none new").

## Residual risk

- **R1 (medium, verification gap).** `S089`'s anchor still pins
  `html sha256 bc572676…e04d` (2026-10-22) while the round-43 entry quotes the
  2026-10-25 bytes `79f6501a…`; the entry discloses the drift inline
  (`r43-survivor-resolution-rule.md:18-22`) and the lesson defers the anchor
  move to the round-44 recheck. The `bc572676` bytes are not committed anywhere
  (`grep -rl bc572676 .ufo/evidence` → nothing; only
  `round-42/sources/stryker-mutant-states.html` and
  `round-43/sources/stryker-equivalent-mutants.html` exist), so "every quoted
  sentence survives at the same offset" **cannot be checked against the old
  bytes from this repo**. The used-by extension is honest; the row's anchor is
  now older than one of its own citations. Not a round-43 append defect — a
  falsifier's hole that round 44 inherits.
- **R2.** F1's wording defect is inherited by every future round that copies
  the "Next unused id" phrasing; the guard's `next_free` field is the only
  machine-readable definition and it is max+1.

## Verification gaps

- I did not run `scripts/sources-census.sh` (it is not at `scripts/` in this
  lane; the wave-1 seats used `./scripts/sources-census.sh`, so the path is
  fleet-relative). I relied on the committed receipts plus my own recomputation
  of every count they assert; the receipts' `ok` line and byte-identity are
  consistent, and no receipt claims a row count the note contradicts.
- I did not re-fetch either source; the append's claims are checked against the
  committed snapshots, which is what the anchor cells pin.
- "two fetches the same day were byte-identical" (`:453`) is not falsifiable from
  committed bytes; it rests on the L1's fetch record.

## Touched surfaces

Read-only on the lane checkout: no edit to `corpus/SOURCES.md`, no counter run,
no git/jj mutation (`git show`, `git diff`, `git cat-file -e` only), staged
package read only, no write to `shokuknow`. Scratch `/tmp/tameshi-r43-w2-RevSourcesAppend/`
held one base blob and nothing else. Only this file was written. No tool was
installed or upgraded (pacman paused host-wide; nothing was needed).
