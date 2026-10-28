# T56W2Read08 — cold-read re-read 8/18 (round 56, wave 2)

Heading: `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`
Candidate (content commit C0): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
Section sha256 (frozen round-18 sectionize, computed at C0): `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993`
Section extent at C0: lines 949–962 of `SKILL.md`.
Verdict: **verified-record** (no false statements; no failing commands).

Every command below was run in a scratch clone of the lane at C0
(`git clone --shared` then `git -C <clone> checkout --detach c0137451…`;
`git rev-parse --show-toplevel` printed the scratch clone path). Receipts are in
`.ufo/waves/round-56/w2/T56W2Read08-receipts/`. No lane production file was
edited; the clone's `git status --porcelain` was empty after every run and all
four owner repos reported 0 changed paths.

## How the sha256 was computed (frozen sectionize, never reimplemented)

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
```

loaded into `.ufo/evidence/round-18/measure.py` via `importlib`
(`m.sectionize(raw)`); that module's blob sha256 is
`7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`, identical at
base and at the round-56 freeze, and identical whether loaded from the worktree or
from the REV blob.

```
python3 -c "import importlib.util,subprocess;s=importlib.util.spec_from_file_location('r18','/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);raw=subprocess.run(['git','-C','/home/vgpnk/Projects/shokunin/tameshi-shokunin','show','c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md'],capture_output=True).stdout;print([(x['start'],x['end'],x['sha256']) for x in m.sectionize(raw) if 'leg ledger' in x['heading']])"
```

output:

```
[(949, 962, '430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993')]
```

The sectionize split yields 64 sections at C0, and this heading maps to exactly
one of them (no ambiguity). The sha was independently recomputed by re-deriving
the section bytes from the blob (heading line through the line before the next
heading, trailing blank lines stripped) and hashing them — same value.

## The section as read at C0 (lines 949–962)

> Round 7 turns `--regression` from the tool's two-case self-check into the
> fleet's **leg ledger**: every recorded mutation case is a leg of this ledger,
> replayed at its pinned original revision. Round 7 recorded four legs at
> r7-1 (dated milestones: seven from round 16, eight from round 18, nine from
> round 26, ten from round 51) — `js-kimi-census`
> (r2, killed 8/10 = 80 %), `bash-surface-census` (r3, 8/10 = 80 %),
> `bash-tsukuroi-census` (r5, 6/10 = 60 %), `bash-mado-verify` (r6, 4/10 = 40 %)
> — each with its recorded kill-rate as its expectation
> (`tools/mutate-and-run.sh@9f1d3c3:72-109`, `:511-522`; at round 18 (runner `4b7c682`) the recorded tables sit at `:597-620`). The ledger
> is the receipt tameshi's records cite for kill-rate claims; the standing per-gate rate rows
> are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight ledger rows — six in the §1/ER-2 table plus the round-16 and round-18 appends; the ninth and tenth cases, cite-check and drift-pins, are recorded in their own notes, not as ledger rows).

## Commands run, and their outputs

### 1. The section's own replay command — the ledger itself

```
bash tools/mutate-and-run.sh --regression --workdir $WORK/reg
```

run from the C0 scratch clone with the four owner repos symlinked beside it
(`kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`),
`TMPDIR=$WORK/tmp`. Exit 0, wall 168.26 s. Full stdout in
`T56W2Read08-receipts/01-regression-C0.stdout`.

```
REGRESSION_TOOL: …/tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
REGRESSION_DATE: 2026-10-28T19:41:46Z
REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=1 flips<=1
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10 js-sources-check=5/10 js-cite-check=5/10 bash-drift-pins=2/10
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

The four legs this section names, read off that stdout:

```
REGRESSION_PIN js-kimi-census: source=git repo=…/kumitate-shokunin rev=175de6ba2e9e904010411b19cab27e0af9aad3d4 path=scripts/kimi-census.mjs mode=100644 sha256=83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426
REGRESSION_SWEEP js-kimi-census: MUTATE: DONE (target=js-kimi-census defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)
REGRESSION_TABLE js-kimi-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION_SWEEP bash-surface-census: MUTATE: DONE (target=bash-surface-census defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)
REGRESSION_TABLE bash-surface-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_SWEEP bash-tsukuroi-census: MUTATE: DONE (target=bash-tsukuroi-census defects=10 killed=6 survived=4 inconclusive=0 kill-rate=60%)
REGRESSION_TABLE bash-tsukuroi-census: match=10/10 recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0
REGRESSION_SWEEP bash-mado-verify: MUTATE: DONE (target=bash-mado-verify defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)
REGRESSION_TABLE bash-mado-verify: match=10/10 recorded-killed=4 measured-killed=4 survived=6 inconclusive=0 flips=0
```

Every leg materialized from its owner repo's git object store (`source=git`) at
the recorded revision, with the recorded pin sha256 matching, and every leg
reproduced its recorded table exactly. "Replayed at its pinned original
revision" and "each with its recorded kill-rate as its expectation" are both
demonstrated, not just asserted.

### 2. The instrument's own gate

```
bash tools/mutate-and-run.sh --selftest
```

Exit 0 (5.68 s). `T56W2Read08-receipts/02-selftest-C0.stdout`:

```
MUTATE_SELFTEST: 107/107 pass
VERDICT: PASS
```

Its leg-count agreement arm independently asserts `calls=10 specs=10 nlegs=10`
at C0 and checks each of the ten leg tuples against its `TABLE_` constant — the
same bijection between recorded mutation cases and legs this section describes.

### 3. The r7-1 anchors the section cites

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 9f1d3c3:tools/mutate-and-run.sh | sed -n '72,109p'
```

`T56W2Read08-receipts/04-runner-9f1d3c3-72-109.txt` — the header comment
block. Lines 75-78 name exactly the four legs and rates the section quotes:

```
#   js-kimi-census       kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
#   bash-surface-census  kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
#   bash-tsukuroi-census tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
#   bash-mado-verify     mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
```

and the block states the exact expectation ("0 verdict flips … killed-delta 0,
defects exactly the recorded count, inconclusive 0 … Inside the stated
expectation is PASS; outside it is FAIL").

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 9f1d3c3:tools/mutate-and-run.sh | sed -n '511,522p'
```

`T56W2Read08-receipts/05-runner-9f1d3c3-511-522.txt` — exactly the 12 lines of
the pin/revision/table block for those four legs (511-518 `PIN_`/`REV_`,
519-522 `TABLE_JS`/`TABLE_BASH`/`TABLE_TSUKUROI`/`TABLE_MADO`); no fifth leg.

Identity of that revision (`T56W2Read08-receipts/09-anchor-identity.txt`):

```
sha256 of tools/mutate-and-run.sh at 9f1d3c3 = cf41efaa8be5f52d…   (61 632 B, 1 341 L)
legs at 9f1d3c3 = 4
```

That is the very pin the ledger's ER-2 names — "the harness at
`cf41efaa8be5f52d…` (r7-1; 1 341 L / 61 632 B) carries **four** materialized
legs" (`corpus/knowledge/fleet-kill-rate-ledger.md:281`) — so the section's
`@9f1d3c3` anchor and the ledger's r7-1 blob pin are the same artifact.

The pre-r7-1 runner (44947154) has 0 `regression_case_git` legs and its
`--regression` header reads "this tool's own gate: re-runs BOTH worked cases"
with `cases=2` in the summary printfs — confirming round 7 is the turn the
section describes.

### 4. The round-18 pointer

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 4b7c682:tools/mutate-and-run.sh | sed -n '597,620p'
```

`T56W2Read08-receipts/06-runner-4b7c682-597-620.txt` — the eight
`PIN_`/`REV_` pairs (597-612) and the eight `TABLE_` lines (613-620), ending
exactly at `TABLE_SOURCESCHECK`. The section's ":597-620" range resolves to the
recorded tables for the eight legs of that round.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
```

4b7c682 is the round-18 commit ("round-18: measured SCORECARD depth7→8, bounded
eleven-defect closure, strict60/60 calibration8"), its runner blob hashes to
`d22c4025e8ce38b8…` — the sha the round-18 receipt carries on its
`REGRESSION_TOOL` line (`.ufo/waves/round-18/w2/RerunC1.md:84`) — and it has 8
legs. The section names a commit rev where the ledger and receipt name a blob
sha256; the two agree because that commit is the one carrying that blob.

### 5. The milestone list

`T56W2Read08-receipts/08-milestone-receipts.txt` — the four committed receipts
the section's milestone list points at:

```
.ufo/evidence/round-16/round-gate/runner-regression.txt:41:REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)
.ufo/evidence/round-18/coldread/traces/CR18/2.out.txt:45:REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
.ufo/evidence/round-26/cite-check/regression-worktree.stdout:50:REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
.ufo/evidence/round-51/integrate/l1-probe-f133b47/c2.stdout:22:REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

### 6. The ledger pointer and its row arithmetic

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c0137451f5b7f22d65f748fc69f1b181f55e1378:corpus/knowledge/fleet-kill-rate-ledger.md
```

`T56W2Read08-receipts/07-fleet-kill-rate-ledger-C0.md`. The file exists at C0
(blob `1cc5f07b46a46b077f86a04b775b3713849ecc39b`) and is what tameshi's
records cite: at C0 it is cited from S031 and S034 in `corpus/SOURCES.md`, from
`corpus/README.md:49` and `:97`, and from 18 `SKILL.md` lines including the
registry row at :1426.

Row arithmetic, from the numbered rows in that file:

- §1 table — rows 1-4 (lines 45-48): kimi r2 8/10 80 %, surface r3 8/10 80 %,
  tsukuroi r5 6/10 60 %, mado r6 4/10 40 % — the same four rates and the same
  r2/r3/r5/r6 labels the section lists.
- ER-2 append table — rows 5-6 (lines 276-277).
- "Round 16 — seventh row appended" (line 403) — js-round-gate.
- "Round 18 — eighth row appended" (line 424) — js-sources-check.

Six in the §1/ER-2 table plus the two appends = eight ledger rows, as the
section states and as the registry row at SKILL.md:1426 repeats ("eight rows").

### 7. The ninth and tenth cases

Neither has a numbered rate row in the ledger: `grep -nE '^\| [0-9]+ \|'` over
the ledger yields rows 1-8 in the rate tables plus the ER-3/ER-4 pin-read
tables (numbered 1-6, but pin readings rather than rate rows). Both notes exist
at C0 and carry the recorded rates:

- `corpus/knowledge/mutation-case-kumitate-cite-check.md` (ninth) —
  "## 2. Result — 5/10 killed (50 %), 10/10 verdict predictions held".
- `corpus/knowledge/mutation-case-kagi-drift-pins.md` (tenth) —
  "## 2. Result — 2/10 killed (20 %), 7/10 verdict predictions held".

The ninth case has no ledger footprint at all (the ledger contains no round-26
cite-check block). The tenth does have one: the "Round 52 — §3 drift-pins cell
superseded" block at ledger line 439 records the case-10 measurement and the
note pointer. That block is a cell supersession, not a rate row, so the
section's sentence stands as written; SKILL.md:1426 already states the tenth's
only ledger footprint precisely.

### 8. Census (lane-level, reported for the L1)

```
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Exit 0 — warnings only, no E-codes (`T56W2Read08-receipts/10-census-validate.stdout`).
`census --root …` reports `tameshi rows 142`: the round-56 content commit added
two SOURCES rows (S281, S282) to a base of 140, so the tree carries 142 registry
rows, one more than the 141 the round-56 brief states. The census itself is
clean; the difference is a fact of the committed `SOURCES.md` and lies outside
this seat's section.

## Sweep run (an attack that finds nothing must show the sweep)

Every pointer and every numeric claim in lines 949-962 was resolved against the
tree at C0, by content, not by grepping for the claim's own words:

| Section element | How it was checked | Result |
|---|---|---|
| `tools/mutate-and-run.sh@9f1d3c3:72-109` | blob read at that rev; header lines 75-78 | resolves; names the same four legs and rates |
| `:511-522` at 9f1d3c3 | blob read; line range printed | resolves; 12 lines, four pins/revs/tables, no fifth leg |
| runner `4b7c682` | `git log -1`; blob sha; leg count; ancestry to C0 | round-18 commit, ancestor of C0, 8 legs, sha == round-18 receipt's `REGRESSION_TOOL` |
| `:597-620` at 4b7c682 | blob read; line range printed | resolves; pins/revs 597-612, tables 613-620 |
| "four legs at r7-1" | `grep -c` of `regression_case_git (js\|bash)-` at 9f1d3c3 | 4 |
| "two-case self-check" before round 7 | header of the pre-r7-1 runner 44947154 | "re-runs BOTH worked cases", `cases=2` |
| "every recorded mutation case is a leg" | 10 `mutation-case-*.md` notes at C0 vs 10 legs at C0 | bijection |
| four kill-rates and r2/r3/r5/r6 labels | ledger §1 rows 1-4; r7-1 header; live replay | all three agree |
| "pinned original revision" | `REGRESSION_PIN … source=git rev=…` for all 10 legs | all 10 materialized at their recorded revs |
| "recorded kill-rate as its expectation" | `REGRESSION_EXPECT` + per-leg `REGRESSION_TABLE` | all 10 exact, flips=0 |
| milestone list (7/8/9/10) | committed receipts of rounds 16/18/26/51 | cases=7/8/9/10 confirmed |
| "eight ledger rows" | numbered rows in the ledger's rate tables | 1-4 (§1), 5-6 (ER-2), +2 appends = 8 |
| "six in the §1/ER-2 table" | line ranges 45-48 and 276-277 | confirmed |
| "ninth and tenth … in their own notes" | note files at C0; numbered-row grep | both notes exist; neither has a rate row |
| ledger is "the receipt … records cite" | corpus-wide grep at C0 | cited from S031, S034, README ×2, 18 SKILL.md lines |
| no contradiction with other sections | compared against SKILL.md:980, :990, :1006, :1113-1118, :1401, :1426, :2192 | consistent; the same milestone list and the same eight-row count |

## Notes (improvements, stale-but-true, style — no false statements)

1. The r7-1 anchor and the ledger's r7-1 blob pin are the same artifact:
   `git show 9f1d3c3:tools/mutate-and-run.sh` hashes to
   `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`
   (61 632 B / 1 341 L), exactly the "cf41efaa… (r7-1; 1 341 L / 61 632 B)" the
   ledger's ER-2 names (`fleet-kill-rate-ledger.md:281`). Worth stating, because
   a reader could otherwise think the section and the ledger cite two different
   round-7 runners.
2. The section names a commit rev (`4b7c682`) where the ledger and the round-18
   receipt name a blob sha256 (`d22c4025…`). They agree — 4b7c682 is the commit
   carrying that blob — but a reader has to do the identity check the section
   leaves implicit. Naming the blob sha as well would close it.
3. The milestone enumeration lists 7/8/9/10 but not the intermediate 5-and-6
   milestone (the two legs embedded at r10-2). Each listed item is true, and the
   same enumeration is used at SKILL.md:980, :1006 and :1426, so it reads as a
   house convention. It is worth one clause, since a reader counting legs from
   "four at r7-1" jumps to "seven from round 16" with nothing in between.
4. "the ninth and tenth cases … are recorded in their own notes, not as ledger
   rows" is literally true but slightly understates the tenth's footprint: the
   tenth (drift-pins) also has the "Round 52 — §3 drift-pins cell superseded"
   block at `fleet-kill-rate-ledger.md:439`. SKILL.md:1426 states this precisely
   ("the tenth's only ledger footprint is the §3 cell supersession at
   `fleet-kill-rate-ledger.md:439`"); repeating that precision here would keep
   the two sections in step.
5. The ninth case (cite-check) has no ledger footprint at all, while the tenth
   has a supersession block — an asymmetry the section presents as uniform. Not
   a defect; worth a reader knowing.
6. The section is a dated round-7 record whose substantive claims are all still
   true at C0, but the leg count it names (four) is the r7-1 count; the current
   runner carries ten. The section does not claim otherwise, and the sibling
   "### Using the ledger" section carries the current ten-leg anchors
   (`:614-643`, `:1459-1508`). A one-clause pointer to the sibling would spare a
   reader the hunt.
7. Lane-level, outside this section: the census is clean
   (`validate … tameshi` exits 0, warnings only), but `census` reports
   `tameshi rows 142` — the round-56 content commit added two SOURCES rows
   (S281, S282) to a base of 140, so the tree carries 142 registry rows, one
   more than the 141 the round-56 brief states. Flagged for the L1's accounting;
   it is not a claim of this section and no text change is implied.

## Tools

No tool was installed, upgraded or modified by this seat; the work used only
`git`, `python3` and `bash` already present on the host. Nothing was written to
any PATH directory.

## Residual risk

The section is a dated historical record whose numbers I verified against the
committed tree at C0, the frozen round-18 sectionize, the committed receipts of
rounds 16/18/26/51, and a live ten-leg replay from a scratch clone at C0. The
one thing not exercised is the historical r7-1/round-18 runs themselves — those
are dated records whose receipts were read, not re-run, because the owner repos'
pinned revisions are what they are; the replay exercises the current ten-leg
state, which is what the section's reader will actually run. The section's
"no contradiction with another section" check was made against the eight
SKILL.md passages that touch the same ledger and the same anchors; a passage
outside that set could still disagree.
