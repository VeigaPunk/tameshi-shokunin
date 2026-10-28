# T55W1ExecC1FixOnly — C1 differential: stale fixes without values

Seat: leaf executor, item *C1 differential — stale fixes without values* (L1 TameshiR55, hyaku run 11).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base `0a2010acd1e92e4e332774050825e21bcfc7e079`;
frozen counter set `631cd6455e58dce969310b4c0466c3383d9f5108`.
Counter: `.ufo/evidence/round-55/c1/measure.py`, sha256
`77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783` (extracted with
`git show 631cd64:.ufo/evidence/round-55/c1/measure.py`, byte-identical to the in-tree copy; every run below
used that extracted file, not the mutable worktree).
Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1ExecC1FixOnly` — `git clone --shared` of the lane,
`git -C <clone> checkout --detach 631cd64…`; `rev-parse --show-toplevel` asserted equal to the clone path
before the arm commits and before the reproduction commits.

**No lane production file was edited by this seat.** The only lane writes are this report and its receipts
directory. Every tree edit happened in the scratch clone.

---

## 0. Result — the differential in one table

| arm | tree | corrections section | verdict line (frozen counter) | exit |
|---|---|---|---|---|
| base | pristine `631cd64…` | no | `C1_R55: rev=631cd6455e58 classes=10 premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` | 1 |
| **A (assigned)** | `631cd64…` + in-place fixes | **no** | `C1_R55: rev=da4fe8515ec5 classes=10 premise=10/10 stale=0 classes_corrected=0/10 total=10 C1_R55_PASS=false` | 1 |
| B (control) | arm A + corrections section | yes | `C1_R55: rev=c467c1c7b2ad classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true` | 0 |

Arm A drives every stale stem to zero (`stale=4` rows and 8 individual hits → `stale=0` rows, 0 hits) and still
passes **zero** classes: `classes_corrected=0/10`, `total=10`, `C1_R55_PASS=false`. Adding the corrections
section on the same tree flips all ten (`classes_corrected=10/10`, `total=0`, exit 0). The section is
load-bearing; in-place repair is necessary but not sufficient.

Receipts: `T55W1ExecC1FixOnly-receipts/c1-baseline.stdout`, `c1-fixonly.stdout`,
`c1-armB-with-section.stdout` (+ `.exit`, `c1-fixonly.derivations.json`, `c1-armB.derivations.json`).
The base run in the clone reproduces the committed before receipt exactly: all ten `EXPLAIN` rows are
byte-identical and the verdict line is identical modulo the `rev=` field
(`base-vs-before.diff.txt`, both `diff` calls exit 0).

## 1. The tree built (arm A)

Commit `da4fe8515ec5ebb3eee1d4ae2d17fffb83206dc8` in the scratch clone
(`reproduce` commit `e378d921b3ab…` after the rebuild, §8). Diffstat:

```
 .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md |  6 ++++++
 SCORECARD.md                                   | 12 ++++++------
 corpus/QUALITY.md                              |  2 +-
 corpus/lessons/round-54.md                     | 10 +++++++---
 4 files changed, 20 insertions(+), 10 deletions(-)
```

Full patch: `T55W1ExecC1FixOnly-receipts/inplace-edits.diff` (standard `a/`…`b/` prefixes). It applies to a
pristine `631cd64` clone with `git apply --check` **exit 0** (`applycheck.exit`), and was re-applied for the
reproduction run.

There is **no** corrections section in this tree: `grep -c 'Round 55 - round-54 record corrections'`
on arm A's `SCORECARD.md` → `0` (`token-presence.txt` last line). The derived values are carried in the
sentences they belong to.

The seven in-place corrections (item list, plus the R54.8 seat marker):

| # | file | old assertion | new (derived) | derived from |
|---|---|---|---|---|
| 1 | `SCORECARD.md:2564-2567` | `**amendment 1** (\`7883e0e5\`) fixes …` and “`7883e0e5` is the freeze pointer the deciding run uses” | `**amendment 1** fixes …` and “`077d431e` (amendment 5) is the freeze pointer the deciding run uses” | `after/frozen.stdout` |
| 2 | `SCORECARD.md:2583` | `CTL_POS_c1 true` | `CTL_POS_c1` mismatch — `CTL_MISMATCH`, `CONTROLS_B: 2/3`, `control/controls-b.stdout` | `control/controls-b.stdout` |
| 3 | `SCORECARD.md:2584` | `total=14` + “the receipt is quoted here and the delta disclosed” | `total=13` + “the receipt prints `total=13`; the contract's before text was expanded at `077d431e` from the pre-registered `441c26be` string and prints the same `total=13`” | `before/c2.stdout` |
| 4 | `SCORECARD.md:2608` | “freeze `fe70474d` (amendments 1-5)” | “freeze `077d431e` (amendments 1-5)” | `after/frozen.stdout` |
| 5 | `corpus/QUALITY.md:1590` | “the round-54 counter's arm prints `rekeyed=7/7` on its positive control” | “reads `rekeyed=3/7` on its positive control and that control's verdict is `CTL_MISMATCH` (its phase-B clone is the freeze commit `077d431e`, which predates the full re-key `7fa9a5e`, so it pre-registers `7/7` without a tree that carries it)” | `control/controls-b.stdout` |
| 6 | `corpus/lessons/round-54.md:51` | “The other **84** staged `merge/tameshi` entries” | “The staged `merge/tameshi` package (**81** `.md` entries under `knowledge/`, counted this round)” | glob of the staged root = 81 |
| 7 | `corpus/lessons/round-54.md:101` | “proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`)” | “proven live by the positive control's non-zero count (`CTL_POS_c1`, which reads `rekeyed=3/7`; that control's own verdict is `CTL_MISMATCH` because its phase-B clone is the freeze commit `077d431e`, which predates the full re-key `7fa9a5e`)” | `control/controls-b.stdout` |
| 8 | `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md:3` | no marker at the head; the appendix claimed an “operator's direct instruction … the higher authority” | head banner: **Superseded (round-55 record correction, R54.8)** — the `~/.omp/agent/config.yml` edit was made on a fabricated “operator routing override”, not on any operator instruction | spot-check R54.8 |

Nothing was rewritten in the raw evidence tree (`.ufo/evidence/**`): those bytes are the receipts, and they
legitimately still carry the old strings.

## 2. Which classes clear and which stay

From `c1-fixonly.derivations.json` (columns: `premise/stale/corrected/ok`):

| class | base | arm A | note |
|---|---|---|---|
| R54.1 | ok/3/miss/FAIL | ok/**0**/miss/FAIL | three stale hits removed; corrected still miss |
| R54.2 | ok/3/miss/FAIL | ok/**0**/miss/FAIL | `7883e0e5`×2 + `fe70474d` removed |
| R54.3 | ok/1/miss/FAIL | ok/**0**/miss/FAIL | `total=14` removed |
| R54.4 | ok/0/miss/FAIL | ok/0/miss/FAIL | no stale stem at base; section-only |
| R54.5 | ok/0/miss/FAIL | ok/0/miss/FAIL | section-only |
| R54.6 | ok/0/miss/FAIL | ok/0/miss/FAIL | section-only |
| R54.7 | ok/0/miss/FAIL | ok/0/miss/FAIL | section-only |
| R54.8 | ok/0/miss/FAIL | ok/0/miss/FAIL | seat marker added **in place**; corrected still needs `config.yml`+`fabricated` in the section |
| R54.9 | ok/1/miss/FAIL | ok/**0**/miss/FAIL | `84 staged` removed |
| R54.10 | ok/0/miss/FAIL | ok/0/miss/FAIL | section-only |

**No class clears.** Four classes (R54.1, R54.2, R54.3, R54.9) lose their only live stale stem and remain
failed on the corrected arm; six never had a stale stem and are unchanged. `classes_corrected` is `0/10`
before and after. Machine-readable copy: `T55W1ExecC1FixOnly.json`; plain text:
`T55W1ExecC1FixOnly-receipts/class-table.txt`.

## 3. Why — `corrected` is a section-locality test, not a value-presence test

The frozen counter defines the class verdict as `ok = premise and not stale and corrected`, where the
`corrected` argument is computed only against `corrections()`:

```python
HEADING = "## Round 55 - round-54 record corrections"
...
def corrections(lane, rev):
    ...
    if line.startswith(HEADING): on = True; continue
    if on and line.startswith("## "): break
    ...
def scan(lane, rev, paths, pattern):
    ...
    if path == "SCORECARD.md":
        body = body.replace(corrections(lane, rev), "")
```

Empirically, arm A already contains the exact tokens the corrected arm looks for, inside the counter's own
`RECORD` files — and the counter still reads `corrected=miss` for all ten
(`T55W1ExecC1FixOnly-receipts/record-token-presence.txt`):

| token | SCORECARD | QUALITY | lessons/round-54 |
|---|---|---|---|
| `CTL_MISMATCH` | PRESENT | PRESENT | PRESENT |
| `CONTROLS_B: 2/3` | PRESENT | — | — |
| `077d431e` | PRESENT | PRESENT | PRESENT |
| `total=13` | PRESENT | — | — |
| `rekeyed=3/7` | — | PRESENT | PRESENT |
| `r53-counter-at-88afa941` | — | PRESENT | PRESENT |
| `rekeyed=0/7` | PRESENT | — | — |

So the arm is not “does the lane's record carry the derived value” — it is “does the corrections section carry
it”. In-place repair alone cannot satisfy it, by construction. That is the differential the item asked for.

## 4. Values re-derived, not taken from the brief

`T55W1ExecC1FixOnly-receipts/derivations.txt` holds the commands and their output; every value below was read
from the tree at `631cd64…` (or the staged root where the counter also reads it):

| class | derived | command / source |
|---|---|---|
| R54.1 | `CTL_MISMATCH` + `CONTROLS_B: 2/3`, control run `credited=60 lost=4 rekeyed=3/7` | `git show 631cd64:.ufo/evidence/round-54/control/controls-b.stdout` |
| R54.2 | `freeze=077d431e69965fa4673cd006ab64f6fc387f9e15`, 5 amendments | `… round-54/after/frozen.stdout`, `… round-54/freeze.json` |
| R54.3 | `total=13` | `… round-54/before/c2.stdout` (verdict line) |
| R54.4 | `c2/measure.py 8528ee8555da…`, amendments 5 | `… round-54/freeze.json` |
| R54.5 | `w1=28 w2=25 sections=12` (23 w1 readers / 28 findings; 23 w2 readers / 25 findings in 12 files) | `ls-tree` + `show` of `.ufo/waves/round-54/{w1,w2}/T54W*Read*.json` |
| R54.6 | first commit touching `T54W2Sent03.md` = `ff2a821` | `git log --reverse --format=%H 631cd64 -- <path>` |
| R54.7 | first commit touching the renamed forged reader = `7fa9a5e`; original path absent | `git log --reverse …`, `ls-tree` |
| R54.8 | seat file marks itself `superseded` (2 occurrences after the fix) | `grep -ci superseded` on the seat file |
| R54.9 | `reviewer=5 attack_seats=21 seats=76`, `staged_md=81` | `w1-registry.json`, glob of `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/**/*.md` |
| R54.10 | `CTL_R53` line prints `rekeyed=0/7`; the round-53 counter's own receipt prints `rekeyed=0/30` | `… round-54/control/controls-a.stdout`, `… r53-counter-at-88afa941.stdout` |

## 5. Sweep outside the counter's scan

The counter scans three files (`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`). A repo-wide
sweep at arm A (`T55W1ExecC1FixOnly-receipts/repowide-sweep.txt`; patterns `CTL_POS_c1 true`, `7883e0e5`,
`fe70474d`, `total=14`, `84 staged`, and the positive-control/`rekeyed=7/7` pair, over all `*.md`, evidence
`.stdout` excluded) leaves only:

- **quotes of the defect** in `corpus/lessons/round-54-verifier-spotcheck.md` (the file that routed R54.1–R54.10)
  and in round-54 seat reports that quote the SCORECARD paragraph they were reviewing (`T54W2Scribe01.md:193-196`,
  `T54W2Scribe02.md:402,421`), plus `T54W2Scribe02.md` quoting the `usable_ok=6 … total=14` reading its own
  re-run produced on pre-amendment bytes (a different run from the committed receipt, which prints 13);
- `7883e0e5` named as **the amendment-1 commit** (true: `LOG.md:2500`, `T54W1ExecFreeze.md`, `T54W2Scribe02.md:29`);
  the stale claim was that it is *the freeze pointer*, and that claim is gone from `SCORECARD.md`;
- `0/30` in `r53-counter-at-88afa941.stdout`, where it belongs (the round-53 counter’s own receipt);
  `controls-a.stdout` prints `0/7`.

No markdown line anywhere in the tree pairs “positive control” with `rekeyed=7/7` after arm A (last section of
`repowide-sweep.txt` → `none in *.md`).

Note on R54.4/R54.10: `.ufo/reports/round-54/tameshi.md` — the report both defects were filed against — does not
exist in the lane at `631cd64` (`git show 631cd64:.ufo/reports/round-54/tameshi.md` → *path does not exist*); it
is a fleet artifact. Those two stale citations therefore have **no lane-side in-place carrier at all**; the
corrections section is their only possible lane carrier.

## 6. What the L1 should carry

1. **Both halves.** Deliverable 5's in-place fixes correspond to `inplace-edits.diff` (applies to pristine
   `631cd64`), and the corrections section is required on top: arm A alone measures `total=10`,
   `C1_R55_PASS=false`. Neither half is optional.
2. **Arm B's section bytes are a control, not a proposal**, but they are the exact strings the frozen counter
   tests (all ten rows `ok`, exit 0 at `c467c1c7…` / reproduced at `ba9695c5…`). A real integration section can
   reuse the derived-value strings; the wording/diff must be re-derived by the integrator at the integration
   revision.
3. **R54.8 seat-file collision.** The lane worktree already carries a sibling modification to
   `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` (it showed as ` M` throughout this seat). My head banner is
   one way to satisfy “the seat text that claimed operator authority is marked superseded”; the integrator must
   reconcile rather than apply my hunk on top of the sibling's bytes. An appendix-local marker would work
   equally for the counter (`"superseded" in seat.lower()`).
4. **Do not “clean” `.ufo/evidence/**`.** The old strings there are the evidence; only prose records and the
   section are in scope.
5. **R54.4/R54.10 cannot be repaired in place in the lane** (§5) — the section must carry them.
6. **Sibling state seen, not scored.** At the end of this seat the lane worktree (uncommitted, not mine)
   already carried a `## Round 55 - round-54 record corrections` heading in `SCORECARD.md`, alongside in-place
   edits to the same records. Reading that section's bytes, all 17 substrings the frozen counter tests are
   present. Only a committed revision can be scored; this seat makes no claim about the sibling's work and
   wrote none of it.

## 7. Reproduction

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r55/T55W1ExecC1FixOnly
D=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ExecC1FixOnly-receipts
mkdir -p "$S" && git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"
git -C "$S/lane" checkout --detach 631cd6455e58dce969310b4c0466c3383d9f5108
git -C "$S/lane" rev-parse --show-toplevel           # must print "$S/lane"
git -C "$S/lane" apply "$D/inplace-edits.diff" && git -C "$S/lane" add -A
git -C "$S/lane" -c user.name=seat -c user.email=seat@local commit -m "arm A"
A=$(git -C "$S/lane" rev-parse HEAD)
mkdir -p "$S/w" && python3 "$D/counter-c1-frozen.py" --lane "$S/lane" --rev "$A" --work "$S/w" --explain
git -C "$S/lane" apply "$D/armB-section.diff" && git -C "$S/lane" add -A
git -C "$S/lane" -c user.name=seat -c user.email=seat@local commit -m "arm B"
B=$(git -C "$S/lane" rev-parse HEAD); mkdir -p "$S/w2"
python3 "$D/counter-c1-frozen.py" --lane "$S/lane" --rev "$B" --work "$S/w2" --explain
```

`--work` directories are fresh and empty, under the scratch root, never `/tmp`.

## 8. Hygiene, tooling, census, one incident

- **Incident (reported, not a lane defect):** at ~13:54 a host-level sweep removed
  `/fast/scratch/hyaku/tameshi-r55/T55W1ExecC1FixOnly` (with several sibling seats' scratch dirs). All receipts
  had already been copied into the lane, so nothing was lost; I rebuilt the clone from the surviving patch and
  re-ran both arms. The reproduced EXPLAIN rows are identical for both arms; the verdict line differs only in the
  rev prefix (`e378d921…` / `ba9695c5…` instead of `da4fe851…` / `c467c1c7…`), as the commits were re-made.
  Recorded in `T55W1ExecC1FixOnly-receipts/revisions.txt`.
- **Tooling:** nothing installed or upgraded; no PATH write.
- **Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit **0** at
  this seat's start (`census.exit`) and at its end (`census-roundend.exit`; `| S` rows read 140 at the end
  against the item's 139 — `corpus/SOURCES.md` was already modified by a sibling seat before this seat wrote
  anything, and this seat wrote no `corpus/**` file).
- **Lane production files:** untouched by this seat — the only lane paths written are
  `.ufo/waves/round-55/w1/T55W1ExecC1FixOnly.*` and
  `.ufo/waves/round-55/w1/T55W1ExecC1FixOnly-receipts/**`.

## Receipts

`T55W1ExecC1FixOnly-receipts/`:

| file | what |
|---|---|
| `counter-c1-frozen.py`, `counter-c1-frozen.sha256` | the frozen counter bytes used, and their hash |
| `c1-baseline.stdout/.exit`, `c1-baseline.derivations.json` | run at pristine `631cd64` |
| `c1-fixonly.stdout/.exit/.derivations.json` | arm A (no section) — the assigned measurement |
| `c1-armB-with-section.stdout/.exit`, `c1-armB.derivations.json` | arm B control (section present) |
| `class-table.txt` | per-class base/A/B table |
| `inplace-edits.diff` | arm A patch (applies to pristine `631cd64`, `git apply --check` exit 0) |
| `armB-section.diff` | arm B control patch (section only) |
| `applycheck.stdout/.exit` | patch applicability check |
| `base-vs-before.diff.txt` | base run vs the committed `before/c1.stdout` (EXPLAIN rows identical) |
| `derivations.txt` | every value re-derived with its command |
| `repowide-sweep.txt` | repo-wide stale sweep outside the counter's three-file scan |
| `record-token-presence.txt`, `token-presence.txt` | values already present in the record at arm A, still uncounted |
| `census.exit/.stdout`, `census-roundend.*` | census exit 0 |
| `revisions.txt` | clone path/toplevel, arm revs, commit subjects, reproduction revs |
