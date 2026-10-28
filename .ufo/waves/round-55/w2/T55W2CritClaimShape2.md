# T55W2CritClaimShape2 — claim shape at C0

Critic seat, wave 2. Target: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0).
Base `0a2010acd1e92e4e332774050825e21bcfc7e079`. Lane read-only throughout; every run below
happens on `git clone --shared` copies under
`/fast/scratch/hyaku/tameshi-r55/T55W2CritClaimShape2/`. Receipts copied to
`.ufo/waves/round-55/w2/T55W2CritClaimShape2-receipts/`.

No tool was installed or upgraded (nothing was needed; `pacman` untouched).

**A fact that moved under me:** during this seat the lane advanced from C0 to
`133b2ce` (amendment 8) and then to `4f7a704` (F5, amendment 9). The wave-2 spec
committed at C0 names freeze `e2979f2` with 7 amendments; `freeze.json` at HEAD has
9. I scored C0 with **both** generations and report the difference — it is not
cosmetic (Verdict 5).

## Frozen bytes used

```
$ git show 133b2ce:.ufo/evidence/round-55/c1/measure.py > c1f.py   # 5e8f50d1… (= freeze.json at C0's generation, +amend 8 for c2)
$ git show 133b2ce:.ufo/evidence/round-55/c2/measure.py > c2f.py   # 0458f632… (= freeze.json current sha)
$ git show 9cf0146:.ufo/evidence/round-55/c2/measure.py > c2-at-C0.py # 36ca47d3… (bytes committed AT C0)
$ git show 4f7a704:.ufo/evidence/round-55/c1/measure.py > c1f-head.py # 83dfbbb0… (freeze at HEAD, amendment 9)
```

## Verdict 1 — Causal separability: **YES, both directions** (but not in cost)

The two claims touch disjoint files, so I built the two hybrids and scored each
claim with the other side reverted to base:

```
C1-side files: SCORECARD.md corpus/QUALITY.md corpus/lessons/round-54.md LOG.md
               .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md
C2-side files: tools/repeat-control.py tools/context-capture.py tools/registry-check.py
               tools/registry.json corpus/knowledge/scratch-root-contract.md SKILL.md
```

`git diff --name-only 9cf0146 <hybrid HEAD>` printed exactly the reverted set for each
hybrid (no accidental cross-contamination), then:

```
$ python3 c1f.py --lane <h1: C0 − C2 side> --rev $(git -C <h1> rev-parse HEAD) --work <empty> --explain
C1_R55: rev=bb860990b9eb classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true

$ python3 c2f.py --lane <h2: C0 − C1 side> --rev $(git -C <h2> rev-parse HEAD) --work <empty> --explain
C2_R55: rev=4a356ad93fc5 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```
receipts: `c1-h1-c2-unlanded.out`, `c2-h2-c1-unlanded.out`.

Static corroboration: `grep -nE 'tools/|SKILL\.md|scratch-root-contract|registry\.json' c1f.py`
hits only `.ufo/waves/round-54/w1-registry.json`; `grep -nE 'SCORECARD|QUALITY|lessons/round-54|LOG\.md' c2f.py`
is empty. Neither counter reads the other's surface.

**But the two claims are not separable in *cost*.** Both land on calibration, and
the loss sets overlap: at C0 the cold-read floor reads 46/64 with both landed; with
C2 reverted alone it is 51/64; with C1 reverted alone it is 46/64. Reverting C1
recovers nothing, because C2's loss set is a superset (Verdict 2b).

## Verdict 2 — Harm to an axis

### 2a. Freshness, from the C1 record edit: **NO harm**

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev <rev> | tail -1
0a2010ac: C1_R45: self_pin=1 population=74 entries=73 verified=73 … disputed=2 fresh=71 score=9 target=50 … C1_R45_PASS=true
9cf0146b: C1_R45: self_pin=1 population=74 entries=73 verified=73 … disputed=2 fresh=71 score=9 target=50 … C1_R45_PASS=true
```
receipts: `fresh-0a2010ac….out`, `fresh-9cf0146b….out`. Identical; the no-harm
monitor's `fresh>=71, score>=9` condition is met at C0. The C1 edit touches no
`corpus/SOURCES.md` *row* (only the C2-surface S280 row is new there — see 2b), so
freshness cannot move.

### 2b. Calibration, from the C2 SKILL.md edit: **YES — 1 section by its own bytes, 18 for the C2 surface**

```
$ bash .ufo/evidence/round-48/quality/coldread-precheck.sh CLONE ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 <rev>
C0:        COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=9cf0146b94dd cand_credited=46 lost=18 RED   (18 LOST lines)
C0−C2side: COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=bb860990b9eb cand_credited=51 lost=13 RED
C0−C1side: COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=4a356ad93fc5 cand_credited=46 lost=18 RED
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev <rev>
0a2010ac: calibration_restraint_score=8  sections_covered=64/64
9cf0146b: calibration_restraint_score=6  sections_covered=46/64
```
receipts: `precheck-c0.out`, `precheck-h1-c2-unlanded.out`, `precheck-h2-c1-unlanded.out`,
`r21-*.json`.

Attribution, by reverting one edit at a time inside each hybrid (same precheck command):

| candidate | lost | reading |
|---|---|---|
| C0 | 18 | total debt at the content commit |
| C0 − C2 files (H1) | 13 | C0's non-C2 edits |
| H1 − `corpus/SOURCES.md` | 6 | S280 row costs **7** |
| H1 − `corpus/QUALITY.md` | 13 | QUALITY line costs **0 here** (masked by SOURCES) |
| H1 − {SCORECARD, LOG, lessons/round-54} | 13 | **0** |
| C0 − C1 files (H2) | 18 | C2 surface costs **18** |
| C0 − `corpus/SOURCES.md` | 15 | S280 row is inside C2's 18 |
| C0 − `corpus/QUALITY.md` | 18 | masked, as above |
| C0 − {SCORECARD, LOG, lessons/round-54} | 18 | **0** |

And the causally isolated set: with SOURCES reverted the six survivors all name
`corpus/QUALITY.md` as their drift (`precheck-attr2-hs.out`), so the ER-R54-1
one-line correction to QUALITY 105 costs **6** sections. Exactly one loss of the 18
carries an empty drift list — `## Standing rules` — i.e. **the SKILL.md edit costs
exactly one section by its own bytes**:

```
$ python3 - <<'PY'   # sha-only losses in precheck-h2-c1-unlanded.out
sha-only losses: 1 ['## Standing rules']
```

Consequences the round must carry:
- Calibration, the axis C1 is on, is **lower at C0 (6) than at base (8)** on the
  standing table's own instrument (SCORECARD:2579). The round harms its claimed axis
  at its content commit and repays later — a debt, not a graduation.
- The C0 record understates it: the wave-2 spec committed at C0 says "One SKILL.md
  section drifted … three seats read it at C0" and `no-harm.sh`'s header says "the
  one SKILL.md section its edit drifts". The measured debt is **18**.
- The obligation is already known at HEAD: `.ufo/evidence/round-55/c1/lost-headings-at-c0.json`
  (added by F5) lists **exactly my 18** (set equality verified), and `binder.py`'s
  `WAVE_DIRS` says "w3 carries the 18 re-key readers". So the wave-2 text is the
  stale artifact, not the plan.
- The deciding run's no-harm monitor requires `credited>=64, score>=8`
  (`no-harm.sh` coldread-floor), so an unrepaired debt refuses the deciding run —
  the safety net works; the cost is that the round cannot close as "one section".

## Verdict 3 — At least one claim on calibration, axis named by the surface: **YES**

```
$ git show 9cf0146:SCORECARD.md | grep -n '^| depth | 10\|^| calibration | 8\|^| freshness | 9'
2578:| depth | 10 | …
2579:| calibration | 8 | … at base the **floor** reads 57/64 credited …
2580:| freshness | 9 | …
```
8 is the unique numeric minimum of the three scored axes; operability and coverage
carry no numeric score, so "lowest non-retired" resolves to calibration. That is the
*obligation* test, and it is met.

The axis is not named by that number, it is named by the surface:
- `corpus/QUALITY.md:1008` (criterion 81) defines the class: "A receipt that
  the tree contradicts and that nothing supersedes **is a calibration mismatch**,
  whatever the round report says about it." C1's surface is precisely a set of
  tree-contradicted records.
- Lane precedent scores the same surface under calibration with the numeric
  unchanged: `SCORECARD.md:2428` (round-50 C1, "calibration (8; surface: routed-defect
  dispositions)"), `SCORECARD.md:2497` (round-52 C2 on "closure-found false records"),
  and rounds 25/26 ("numeric 8→8; surface moved").
- The contract carries the surface as a first-class field (`claims.C1.surface`), and
  the counter measures that surface, not the monitor.

So: C1 is a calibration claim because a record that the tree contradicts is defined
as a calibration defect — and, separately, calibration happens to be the lowest axis.
Both statements hold; neither substitutes for the other.

## Verdict 4 — Do-nothing control cannot reach either target: **YES**

```
$ python3 c1f.py --lane <base clone> --rev 0a2010ac… --work <empty> --explain
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false

$ python3 c2f.py --lane <base clone> --rev 0a2010ac… --work <empty> --explain
C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false
```
receipts: `c1-donothing-base.out`, `c2-donothing-base.out`.

Cheaper-than-work fakes also fail (each clone starts at C0, the named surface reverted):
- values-pasted corrections block, stale assertions untouched → `total=7 C1_R55_PASS=false` (`c1-ctl-skip1.out`)
- invented values in the corrections block → `corrected=0/10 total=10 C1_R55_PASS=false` (`c1-ctl-fab1.out`)
- documentation-only C2 (tools at base, cells/note/SKILL carrying the grammar) → `grammar=6/9 docs=7/7 note=9/9 skill=1/1 total=3 C2_R55_PASS=false` (`c2-skip2-docs-only.out`)

The C2 target is additionally unreachable by doing nothing *and then only writing docs*:
17 of its 20 base points are the three documentation arms, and they are worth 0 while
the grammar arm still reads 6/9.

## Verdict 5 — Claim-shape defect: the C2 target is **false under the bytes committed at C0**

```
$ python3 c2-at-C0.py --lane <C0 clone> --rev 9cf0146b… --work <empty> --explain
C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```
receipt: `c2-c0-intree-counter.out`. Cause: the counter committed at C0 still sums
`+ (8 - note)` and `(len(table) - empty_ok)` while the arms measure 9 and 13, so the
all-green state prints `total=1` with an empty `bad` map. Amendment 8 (133b2ce),
committed **after** C0, changes only those two terms and the same tree then reads
`total=0 C2_R55_PASS=true` (`c2-c0.out`).

This matters because the deciding run extracts the counters **from REV**
(`deciding-run.sh`: `git show "$REV:$E/$f"`), and `FROZEN_UNCHANGED` compares
FREEZE..REV. Therefore:
- the wave-2 spec's stated freeze (`e2979f2`, 7 amendments) scores C2 false at C0;
- the target is reachable only by a REV that already contains amendment 8 — i.e. the
  content commit alone does not satisfy its own claim;
- a second post-C0 amendment (9, at `4f7a704`) also lands after C0 and **widens C1's
  predicate** ("the whitespace-collapsed stale pass runs for every C1 row"). I
  re-scored C0 with HEAD's frozen c1 bytes (83dfbbb0…) to check it was not tuned to
  fit: C0 `total=0 C1_R55_PASS=true`, H1 `total=0 true`, base `total=10 C1_R55_PASS=false`
  (`c1-head-c0.out`, `c1-head-h1.out`, `c1-head-base.out`) — the verdict does not
  flip. The amendment is honest; the *sequencing* is still a fact the judge must see:
  two amendments that change how C0 scores landed after C0.

## Verdict 6 — Two smaller defects found while sweeping

1. **One mode names a second class on stdout.** The claim is "one line, one exit class,
   every mode"; the frozen arms check stderr only. At C0 under an unusable `TMPDIR`:
   ```
   rc=2  stdout: REPEAT_CONTROL: setup_error
         stderr: repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/…/does-not-exist' (could-not-evaluate)
   rc=2  stdout: (empty)  stderr: context-capture.py: could-not-evaluate: …
   rc=2  stdout: (empty)  stderr: registry-check: could-not-evaluate: …
   ```
   receipt: `streams.out`/`streams.err`. A caller that parses the tool's own verdict
   line (the lane's convention) reads `setup_error` for a could-not-evaluate case; the
   uniformity the round claims is a stderr property only. Not a target failure —
   `cannot_see` covers "a caller that parses by prefix" but not "a caller that reads
   stdout".
2. **R54.9's value is not re-derivable.** `c1/staged-at-freeze.txt` carries
   `command=find … -name '*.md' | wc -l` and `output=81`, taken at 14:30Z from the
   mutable sibling package `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge`
   (I re-ran the command: still 81). Nothing pins the file *list*, so a later reader
   cannot re-derive the number if the package moves; a count of a mutable tree is
   trusted, not derived. The contract discloses that this premise is created by the
   round, which is honest — but the arm "the corrected value is derived FROM THE TREE"
   is weaker here than for the other nine.

Also checked and *not* findings: `tools/registry.json`'s 1275/1026-line diff is a
reformat (`indent=1`) — parsed, it is name-for-name, field-for-field identical to base
except the seven `scratch_root` cells, 56 rows both sides; and the correction rows I
spot-checked independently all hold (R54.1 `CTL_MISMATCH`/`2/3`, R54.2 `freeze=077d431e`,
R54.3 `total=13`, R54.7 `R100` at `7fa9a5e` under `--follow`, R54.10 `rekeyed=0/7`).

## Smallest safe corrections

1. **State 18, not 1, and attribute it.** The round's close must say: C0's own edits
   drop the cold-read floor 64→46 (8→6); C2's surface costs 18 (1 by section sha,
   17 by input drift on `tools/*` + `registry.json`); C1's ER-R54-1 line costs 6 of
   those through `corpus/QUALITY.md`; the S280 row costs 7 through `corpus/SOURCES.md`.
   The w3 re-key of the 18 already exists — the C0-era text ("one section") must not
   survive as the record, or C1's own class of defect reappears in round-55 prose.
2. **Name the counter generation that scores C0.** The record must carry: under C0's
   committed bytes `C2_R55_PASS=false (total=1)`; the pass exists only at
   ≥ amendment 8; the freeze is `4f7a704`, not `e2979f2`, and amendments 8–9 postdate
   C0. Otherwise the first auditor who replays the wave-2 spec gets false.
3. **Make `repeat-control`'s stdout verdict token agree with stderr** (or drop the
   stdout line), so "one class" is true of the whole invocation, not of stderr; the
   frozen arms cannot see it either way.
4. **Pin R54.9's denominator**: add `find … -printf '%P\n' | sort | sha256sum` to
   `staged-at-freeze.txt` so the count is re-derivable, not trusted.

## Artifacts opened

`.ufo/evidence/round-55/{contract.json,freeze.json,controls.sh,deciding-run.sh,no-harm.sh}`,
`c1/measure.py`, `c1/staged-at-freeze.txt`, `c1/lost-headings-at-c0.json`,
`c2/measure.py`, `before/{c1,c2}.stdout`, `integrate/{binder.py,resolutions.json}`;
`.ufo/evidence/round-48/quality/coldread-precheck.sh`,
`.ufo/evidence/round-21/coldread/{measure.py,ledger.json}`,
`.ufo/evidence/round-18/measure.py`, `.ufo/evidence/round-45/freshness/measure.py`,
`.ufo/evidence/round-54/{c1/measure.py,control/*,after/frozen.stdout,before/c2.stdout}`;
`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-54.md`,
`corpus/lessons/round-55.md`, `corpus/knowledge/{scratch-root-contract.md,input-keyed-coldread-credit.md}`,
`SKILL.md`, `tools/{repeat-control,context-capture,registry-check}.py`, `tools/registry.json`,
`.ufo/waves/round-55/{spec-w1,spec-w2,spec-w3}.json`,
`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`.

## Reproduce (scratch is disposable; each command names its clone)

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r55/T55W2CritClaimShape2
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
git -C $L show 133b2ce:.ufo/evidence/round-55/c1/measure.py > $S/c1f.py
git -C $L show 133b2ce:.ufo/evidence/round-55/c2/measure.py > $S/c2f.py
git -C $L show 9cf0146:.ufo/evidence/round-55/c2/measure.py > $S/c2-at-C0.py
git clone --shared $L $S/lane
for r in c0 base h1 h2; do git clone --shared $S/lane $S/$r; done
git -C $S/c0   checkout -q -B x 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
git -C $S/base checkout -q -B x 0a2010acd1e92e4e332774050825e21bcfc7e079
git -C $S/h1 checkout -q -B x 9cf0146; git -C $S/h1 checkout -q 0a2010ac -- \
  tools/repeat-control.py tools/context-capture.py tools/registry-check.py tools/registry.json \
  corpus/knowledge/scratch-root-contract.md SKILL.md; git -C $S/h1 commit -qam h1
git -C $S/h2 checkout -q -B x 9cf0146; git -C $S/h2 checkout -q 0a2010ac -- \
  SCORECARD.md corpus/QUALITY.md corpus/lessons/round-54.md LOG.md \
  .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md; git -C $S/h2 commit -qam h2
for r in c0 h1 base; do m=$(mktemp -d); python3 $S/c1f.py --lane $S/$r --rev $(git -C $S/$r rev-parse HEAD) --work $m; rm -rf $m; done
for r in c0 h2 base; do m=$(mktemp -d); python3 $S/c2f.py --lane $S/$r --rev $(git -C $S/$r rev-parse HEAD) --work $m; rm -rf $m; done
m=$(mktemp -d); python3 $S/c2-at-C0.py --lane $S/c0 --rev $(git -C $S/c0 rev-parse HEAD) --work $m; rm -rf $m
bash $L/.ufo/evidence/round-48/quality/coldread-precheck.sh $S/c0 ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 $(git -C $S/c0 rev-parse HEAD)
python3 $L/.ufo/evidence/round-21/coldread/measure.py --repo $L --rev 9cf0146
python3 $L/.ufo/evidence/round-45/freshness/measure.py --lane $L --rev 9cf0146 | tail -1
```
