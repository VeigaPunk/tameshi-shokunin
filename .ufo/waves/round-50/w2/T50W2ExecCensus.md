# T50W2ExecCensus — registry checks at 80ea77e9 (wave 2, round 50)

Seat: `T50W2ExecCensus` (executor, leaf). Item: registry checks at
`80ea77e99e239982ab0b93e416645ef2359725d3` — (1) census validate at fleet root and via `--file` on a
scratch copy of the revision, (2) S271 row structure/status/used-by, (3) S022 and S024 used-by, (4)
0-3-space id census before/after 130→131 with no duplicate id or within-scope duplicate URL, (5) the
registry notes' `Next unused id` line.

Bounds honoured: lane checkout read-only (only `git show`/`git archive`/`git cat-file`); writes went to
`/fast/scratch/hyaku/tameshi-r50/T50W2ExecCensus/` and to this file plus my `.stdout` receipts in the
same `w2/` directory; no git/jj mutation, no fleet-root track, no `~/.local/state/` read, no control
`c2-*` material touched. Scratch deleted before yield. No tool installed or upgraded (nothing needed:
bash 5.3.20, gawk 5.4.1, python 3.14.8, pdftotext 26.08.0, git 2.56.0 were already present; pacman is
paused host-wide and was not invoked).

Scratch material used (all under `$S=/fast/scratch/hyaku/tameshi-r50/T50W2ExecCensus`):
`git -C LANE archive 80ea77e9 | tar -x -C "$S/rev"`, `git -C LANE archive e3729de8 | tar -x -C "$S/base-tree"`,
`git show 80ea77e9:corpus/SOURCES.md > "$S/rev-SOURCES.md"`, same for base. No clone was made; no
fixture repo needed a git mutation.

---

## 1. Census — fleet root (read-only) and the revision's corpus via `--file`

### 1a. Fleet root, live lane (exit 0)

```
$ cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
tameshi	W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
tameshi	W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
tameshi	W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
tameshi	W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```
Receipt: `T50W2ExecCensus.validate-live.stdout`. 14 × W04 + 1 × W01, zero E-codes, exit 0.

The live lane tree at HEAD `4efa5cf` differs from `80ea77e9` only in untracked `.ufo/waves/round-50/w2*`
paths plus tracked `.ufo/waves/round-50/{build-spec-w2.py,spec-w2.json,w2-dispatch.err,w2-dispatch.json,w2.ready}`
(`git -C LANE diff --stat 80ea77e9 4efa5cf`), and `corpus/SOURCES.md` is byte-identical between the live
tree and the revision:
```
$ sha256sum "$S/rev/corpus/SOURCES.md" /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
dbc0a8da9701e95f457bc44936ad39eca0e28f3e4d589db2ed46fae28c8ea0f3  $S/rev/corpus/SOURCES.md
dbc0a8da9701e95f457bc44936ad39eca0e28f3e4d589db2ed46fae28c8ea0f3  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```
So the fleet-root run is a validate of the revision's registry, not of drifted working-tree bytes.

### 1b. Scratch copy of `80ea77e9` via `--file` (exit 0)

```
$ ./scripts/sources-census.sh validate --file "$S/rev/corpus/SOURCES.md" --root /home/vgpnk/Projects/shokunin --today 2026-10-26 tameshi
file	W04	S047 … (same 14 W04 lines as 1a)
file	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file	ok	$S/rev/corpus/SOURCES.md
EXIT=0
```
Receipt: `T50W2ExecCensus.validate-file-rev.stdout`. Warning set identical to 1a; the only textual
difference is the `ok` path line:
```
$ diff <(sed 's/^file\t//' …validate-file-rev.stdout) <(sed 's/^tameshi\t//' …validate-live.stdout)
16c16
< ok	$S/rev/corpus/SOURCES.md
---
> ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Method note (`scripts/sources-census.sh:501-504`): with `--file`, the registry's base dir for E11
resolution is `realpath(dirname(FILE)/..)`. A corpus-only extract therefore produces three bogus E11
lines (`S097/S102/S104 missing used-by tools/tally-audit*.py`) — I hit that on the first, corpus-only
extract and discarded it; the receipt above is from the full-tree extract, which has `tools/` and is E11-clean.

Base for comparison (`e3729de8`), same command shape: exit 0, same 14 W04 + 1 W01
(`T50W2ExecCensus.validate-file-base.stdout`).

### 1c. Census totals (base → revision → live)

```
$ ./scripts/sources-census.sh census --file "$S/base-tree/corpus/SOURCES.md" --today 2026-10-26 tameshi
file	rows	130   tier.A 115  tier.B 12  tier.C 3   mined 102  queued 22  rejected 6
$ ./scripts/sources-census.sh census --file "$S/rev/corpus/SOURCES.md" --today 2026-10-26 tameshi
file	rows	131   tier.A 116  tier.B 12  tier.C 3   mined 104  queued 21  rejected 6
$ ./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi
tameshi	rows	131   tier.A 116  tier.B 12  tier.C 3   mined 104  queued 21  rejected 6
```
Receipts: `T50W2ExecCensus.census-file-base.stdout`, `.census-file-rev.stdout`, `.census-live.stdout`.
Delta is exactly the intended one: +1 tier.A row (S271, mined) and one queued→mined transition (S022).

---

## 2. S271 row: 11 cells, no pipe in a cell, mined / 2026-10-26 / valid cadence, used-by exact

`corpus/SOURCES.md:146` (revision `80ea77e9`) is the S271 row; `:147` is blank and `:148` is `## Paths`,
so the row sits inside `## Registry`.

```
$ awk -F'|' '/^ {0,3}\| S271 /{printf "NF=%d cells=%d\n", NF, NF-2; …}' "$S/rev/corpus/SOURCES.md"
NF=13 cells=11
cell[1]= S271
cell[2]= Simplifying and Isolating Failure-Inducing Input (Zeller, Hildebrandt; IEEE TSE 28(2):183-200, 2002; DOI 10.1109/32.988498) — https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf
cell[3]= paper   cell[4]= A
cell[5]= F6 fixture shrinking — the 1-minimal sub-case criterion for a reduced fixture and the test-run cost of reaching it
cell[6]= §I Introduction, Simplification of test cases paragraph (mirror PDF p. 1); §III-A Minimal Test Cases, Definition 10 (mirror PDF p. 4); §III-C Properties of ddmin, Propositions 11 and 12 (mirror PDF p. 6); §IV-B Figs. 11-12 @ IEEE TSE vol. 28 no. 2, February 2002, DOI 10.1109/32.988498 …
cell[7]= a failing test case is 1-minimal when removing any single change makes the failure disappear, ddmin returns such a case …
cell[8]= mined   cell[9]= 2026-10-26   cell[10]= 730d
cell[11]= corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md
```
Cell-level probe (raw split, empty cells, embedded pipes, URL count):
```
$ python3 - "$S/rev-SOURCES.md"   # probe printed in this session
raw split NF: 13 cells: 11
empty cells: []
http occurrences per cell: [(2, 1)]
cells containing backslash-pipe: []
cell lengths: [4, 199, 5, 1, 114, 504, 177, 5, 10, 4, 102]
row char length: 1159
```
So: 11 cells, no `|` inside any cell (NF=13; a smuggled pipe makes it 12 cells — see §6 M1), no empty
cell, exactly one URL (in cell 2), status `mined`, opened `2026-10-26` (= today, not future), recheck
`730d` — a valid `NNd` cadence under `scripts/sources-census.sh:662-665` and no E09 emitted.

Used-by cell vs. the entries whose `source:` lines cite S271 in `corpus/knowledge` at the revision:
```
$ grep -rlE '^source: *S271([ (—,-]|$)' corpus/knowledge/ | sort
corpus/knowledge/delta-debugging-minimization-contract.md
corpus/knowledge/fixture-shrinking-pilot.md
$ grep -rniE '^[[:space:]>-]*source[[:space:]]*:' corpus/knowledge/ | grep -E 'S271|S022|S024'
corpus/knowledge/survivor-fixture-minimization.md:3:source: S024 (https://www.fuzzingbook.org/html/Reducer.htm…
corpus/knowledge/delta-debugging-minimization-contract.md:1:source: S271 — https://www.cs.purdue.edu/homes/x…
corpus/knowledge/delta-debugging-minimization-contract.md:2:source: S024 — https://www.fuzzingbook.org/html/…
corpus/knowledge/fixture-shrinking-pilot.md:1:source: S271 — https://www.cs.purdue.edu/homes/xyzhang/fall07/…
corpus/knowledge/fixture-shrinking-pilot.md:2:source: S022 — https://drops.dagstuhl.de/entities/document/10.…
corpus/knowledge/fixture-shrinking-pilot.md:3:source: S024 — https://www.fuzzingbook.org/html/Reducer.html …
```
The loose scan (any line beginning `source:` with or without a leading list marker, id anywhere in the
line) finds exactly those 5 lines; no `^source:` line in `corpus/lessons/` cites any of the three ids
(`grep -rn '^source:' corpus/lessons/` → no match). Set equality, both directions:

| id | used-by cell (SOURCES.md) | entries with a `source:` line citing it | equal |
|---|---|---|---|
| S271 (`:146` cell 11) | `fixture-shrinking-pilot.md`, `delta-debugging-minimization-contract.md` | same 2 (`pilot:1`, `contract:1`) | yes (set; listed order differs from sorted order) |
| S022 (`:33` cell 11) | `fixture-shrinking-pilot.md` | same 1 (`pilot:2`) | yes (set and order) |
| S024 (`:35` cell 11) | `survivor-fixture-minimization.md`, `fixture-shrinking-pilot.md`, `delta-debugging-minimization-contract.md` | same 3 (`survivor:3`, `pilot:3`, `contract:2`) | yes (set; listed order is append order, not sorted) |

All four/eight used-by paths resolve on disk at the revision (`os.path.exists` → all `True`), which is
also what the clean E11 run in §1b says. Row-level independence check: the S271 URL occurs once in the
file (`grep -c 'cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf'` → `1`), so no W04/E04.

Ancillary (the row's own note claims): the cited snapshot exists at the revision and matches its quoted
digest —
```
$ git -C LANE cat-file -s 80ea77e9:.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf
247738
$ git -C LANE show 80ea77e9:.ufo/waves/round-50/w1/T50ScribeRows.src/zeller-hildebrandt-tse2002.pdf | sha256sum
7ed0c812e1b3212f3956f5a624ac9103a00468ab665cae00784520d866e1c8aa  -
```
and the page locators in cell 6 resolve in that PDF (`pdftotext -f N -l N`): p.1 has "Simplification of
test cases", p.4 has "Definition 10" (and "removing any single"), p.6 has "Proposition 11" and
"Proposition 12". 17 pages total.

---

## 3. S022 / S024 used-by vs. citing entries

Covered by the table in §2; S022 `corpus/SOURCES.md:33` and S024 `:35` carry exactly the cited sets, no
missing and no extra entry. Base→revision transition matches the round-50 note: base `S022` was
`status=queued … usedby=—` (base `SOURCES.md:33`), base `S024` used-by was
`corpus/knowledge/survivor-fixture-minimization.md` only (base `:35`); at the revision S022 is mined with
the pilot entry and S024 gains the two round-50 F6 entries. Both remain W01/W03-clean (mined with a
non-`—` used-by), which §1a/§1b confirm (the only W01 is S101, unrelated).

## 4. 0-3-space id census before/after, duplicate id, within-scope duplicate URL

```
$ awk -F'|' '/^ {0,3}\| S[0-9][0-9][0-9]/{gsub(/ /,"",$2); print $2}' …/corpus/SOURCES.md | sort -u | wc -l
base-tree: 130      rev: 131        (column-zero-only pattern: base 130, rev 131 — identical)
indented (1-3 spaces) data rows: base 0, rev 0
duplicate ids: (none) at both revisions
$ comm -13 <base ids> <rev ids>   ->  S271
$ comm -23 <base ids> <rev ids>   ->  (empty)
```
Receipt: `T50W2ExecCensus.ids.stdout`. Exactly one id entered (S271), none left, no duplicate id, and no
indented row that only the 0-3-space extractor would see (which is why the 0-3 and column-zero counts
agree; the guard is present and exercised — see §6 M7 for its section scope).

Within-scope duplicate URL: the tool reports zero E04 at the revision (§1b). Independent re-derivation
(scheme/`www`/trailing-slash-normalized URL, grouped with scope) over the revision's 131 data rows:
```
$ python3 dupgroups.py    # receipt: T50W2ExecCensus.dup.url-groups.stdout
duplicate URL groups: 11  lines involved: 24
groups with a repeated scope (should be 0): 0
```
Cross-check of the tool's 14 W04 lines against that: W04 fires on each *redundant* row (the later row of
a pair, and rows 2..n of a group) with a new scope, so 11 groups — one of them `pitest.org/quickstart/
incremental_analysis` with 4 members (S041/S047/S048/S266) — yield 13 redundant rows inside my groups;
the 14th, S104, sits in a bashref.texi group whose URL carries a `?id=` query that my normalizer keeps
(the tool's `url_of` strips it), so its partner (S097, `SOURCES.md:106`) normalizes equal for the tool.
Both views agree on the claim that matters: **no within-scope duplicate URL**, only cross-scope
supersede pairs, which is exactly what `scripts/sources-census.sh:645-651` classifies as W04, not E04.

## 5. `Next unused id` line

```
$ tail -1 "$S/rev-SOURCES.md"
- Next unused id: S272 (staged ids S161-S255 stay reserved by document for the package).
$ wc -l < "$S/rev-SOURCES.md"   ->  498
$ grep -c '^ {0,3}| S272 ' "$S/rev-SOURCES.md"   ->  0
$ grep -n 'Next unused id' "$S/rev-SOURCES.md" | tail -3
496:- Next unused id: S271 (staged ids S161-S255 stay reserved by document for the package).
497:- Round 50: one row added by document … S271 … S022 queued → mined … S024 used-by gains the two round-50 F6 entries …
498:- Next unused id: S272 (staged ids S161-S255 stay reserved by document for the package).
```
Max registry id at the revision is S271, so the last note (line 498, the file's last line) is correct and
append-only: the round-49 note (line 496) said S271, the round-50 paragraph (497) appends S271, and the
new note says S272 with no S272 row anywhere. Base ends with `- Next unused id: S271 …` (max id S270),
so the chain 496→497→498 is coherent.

---

## 6. Mutant probe — are these checks live on *this* row? (scratch copies only)

Each mutant is a copy of the revision's `corpus/` + `tools/` under `$S/mut/<M>`, one targeted edit to the
S271 row, then the same `--file` validate. Receipt: `T50W2ExecCensus.mutants.stdout`.

```
M0-pristine         exit=0 codes=W01,W04
M1-pipe-in-cell     exit=1 codes=E01,W01,W04   file  E01  S271 fields=12
M2-status-watch     exit=1 codes=E07,W01,W04   file  E07  S271 status=watch
M3-future-opened    exit=1 codes=E08,W01,W04   file  E08  S271 opened=2026-12-31
M4-duplicate-id     exit=1 codes=E03,W01,W04   file  E03  S270 duplicate id
M5-missing-usedby   exit=1 codes=E11,W01,W04   file  E11  S271 missing used-by corpus/knowledge/does-not-exist.md
M6-bad-recheck      exit=1 codes=E09,W01,W04   file  E09  S271 recheck=2y
M7-row-outside-reg  exit=1 codes=E12,W01,W04   file  E12  S271 row outside Registry section
M8-underlisted-usedby exit=0 codes=W01,W04    (S271 used-by cell reduced to the pilot entry only)
```
M0 (byte copy) reproduces the real verdict exactly, so the kills are attributable to the edits, not the
copy. Seven of eight registry invariants I checked are enforced by the shipped tool on this row.

M8 is the documented blind spot: the tool checks that each used-by path **exists** (E11) and that a mined
row is not **empty** (W03), never that the cell is **complete**. The S271/S022/S024 completeness result in
§2-§3 therefore rests on my independent `source:`-line scan, not on the census tool.

---

## Findings

F1 (pass). Census validate is clean at `80ea77e9` both ways — fleet root on the byte-identical live
registry (exit 0) and `--file` on a full-tree scratch extract (exit 0): 14 × W04 + 1 × W01, zero E-codes.
Command: §1a/§1b. Receipts `T50W2ExecCensus.validate-{live,file-rev}.stdout`.

F2 (pass). `corpus/SOURCES.md:146` S271 parses as 11 cells (NF=13), no `|` inside a cell, no empty cell,
one URL, `status=mined`, `opened=2026-10-26`, `recheck=730d` (valid `NNd`; no E09). Command: §2 awk +
cell probe.

F3 (pass). S271 used-by names exactly the two entries with a `source:` line citing S271
(`corpus/knowledge/fixture-shrinking-pilot.md:1`, `corpus/knowledge/delta-debugging-minimization-contract.md:1`),
both paths present. Command: §2 `grep -rlE '^source: *S271…'`.

F4 (pass). S022 (`:33`) and S024 (`:35`) used-by name exactly their citing entries (1 and 3 respectively;
`pilot:2`, `survivor:3`, `pilot:3`, `contract:2`). Command: §2 loose `source:` scan; base→rev transition
matches the round-50 note.

F5 (pass). Id census 130 (`e3729de8`) → 131 (`80ea77e9`) under both the 0-3-space and column-zero
patterns, with `+S271` as the only addition, no removals, no duplicate id, and zero within-scope duplicate
URLs (E04 empty; independent URL+scope grouping also empty). Command: §4.

F6 (pass). `Next unused id: S272` at `corpus/SOURCES.md:498` (last line) is max-id+1 and no S272 row
exists. Command: §5.

F7 (low, documentation; registry self-consistency). `corpus/SOURCES.md:274` heads a section
`## Leads (unopened)` whose own rule at `:276-277` reads "a lead is not evidence and never a row … the six
opened this round moved to rows S040–S046 and left this list", yet the Zeller & Hildebrandt bullet is still
there at `:279` although S271 (`:146`) is now a mined row. Every other lead bullet is the single occurrence
of its document in the file (`grep -c` = 1 for Regehr/PLOS-style leads, `Hypothesis: A new approach`,
`2406.09843`, `2506.02954`, `Detecting Trivial Mutant`, `10993/31623`); Zeller is the only lead that now
appears both as a bullet and as a row. The round-50 note at `:497` records that "the Zeller lead in the
leads list above now has this row" but does not retire the bullet, and no validator covers this list.
Command:
```
$ awk 'NR>274 && NR<=296 && /^- /{print NR": "substr($0,1,90)}' corpus/SOURCES.md   # bullet still at 279
$ for k in Regehr 'Hypothesis: A new approach' 2406.09843; do grep -c -- "$k" corpus/SOURCES.md; done   # 1 each
```
Impact: cosmetic; no census code, row cell, id, or counter term depends on `## Leads`. Fix (next content
round): delete the bullet or mark it `→ S271` under the section's stated retirement rule.

F8 (low, tool message wording; `scripts/sources-census.sh:636`). E01 prints `%s fields=%d` with `NF-2`,
i.e. it labels a **cell count** as "fields" — the header comment at `:24` says "malformed row (NF!=13)" and
the lane's own notes use "13 awk fields" for NF, so the emitted `fields=12` for a 12-cell row is one off
from both. The check itself fires correctly (M1); only the label misleads. Command: §6 M1, then
`sed -n '626,640p' scripts/sources-census.sh`. This is an observation about the census tool, not about the
revision's registry — the tool is the lane's, unchanged by this round.

F9 (limit, stated not repaired). Used-by *completeness* is unenforced by the census tool (M8: exit 0 with
the S271 cell truncated to one entry). My F3/F4 results are independent-scan results; anyone re-running
only `sources-census.sh validate` would not see an under-listed cell.

## Risks / blockers

- None blocking. F7 and F8 are documentation/wording defects; neither changes a claim term (this seat
  decides nothing) and neither is visible to `sources-census.sh validate`.
- E11 with `--file` is base-dir-sensitive (see §1b method note): a corpus-only extract manufactures three
  false E11 lines. Any wave-2 seat re-checking with `--file` must extract the full tree (`git archive`
  without pathspec), else the receipt is invalid — I discarded exactly such a first run.
- F3/F4 rest on my script; receipts are in `T50W2ExecCensus.consistency.stdout` (the check that produced
  the set-equality table) so the finding can be re-run without me.

## Summary

All five assigned registry checks pass at `80ea77e99e239982ab0b93e416645ef2359725d3`; nothing contradicts
the round-50 registry notes. Census validate exit 0 both from the fleet root (live registry byte-identical
to the revision, `dbc0a8da…`) and from a full-tree scratch `--file` extract: 14 W04 + 1 W01, zero E. S271
(`corpus/SOURCES.md:146`) is a clean 11-cell row, mined, opened 2026-10-26, recheck 730d, its used-by
naming exactly the two entries whose `source:` lines cite it; S022 (1) and S024 (3) used-by cells are
likewise exact. Id census 130 → 131 with S271 the only addition, no duplicate id, no within-scope duplicate
URL; `Next unused id: S272` at `:498` is max-id+1. Eight-mutant probe kills 7 of 8 invariants on this row
(M0 byte copy reproduces the clean verdict). Two low findings: the `## Leads (unopened)` list still carries
the now-rowed Zeller bullet (`:279` vs `:146`), and E01's "fields=" label prints a cell count
(`scripts/sources-census.sh:636`). Stated limit: used-by completeness is not tool-enforced (M8 silent).
