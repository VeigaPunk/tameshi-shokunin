# T55W2SimplDiff — wave 2 simplifier: is the C0 diff minimal?

Seat T55W2SimplDiff (leaf). Lane `tameshi-shokunin`. Base `0a2010acd1e92e4e332774050825e21bcfc7e079`,
counter freeze `e2979f277138da503af27b263b783f626f109be4`, content commit C0
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`. Read-only on the lane; every edit happened on
`git clone --shared` copies at C0 under `/fast/scratch/hyaku/tameshi-r55/T55W2SimplDiff/`.
No lane production file, frozen file or wave spec was modified. Nothing installed: `git 2.56.0`,
`python3 3.14.8`, `strace` were already present, so no tool channel was used.

## 1. Axes I worked on

1. **Semantic load** — how many of the changed lines carry meaning.
2. **Operability** — does the reduced file still satisfy C2's docs arm (7/7) and the full counter?
3. **Calibration** — does the reduced file still satisfy C1 (the record against the tree)?
4. **Reviewability / provenance** — `git blame`, later rounds' "record must agree with tree" checks,
   and the evidence a reader can still open.

## 2. Verdict

**`tools/registry.json` must be reduced to seven changed lines before the round is called minimal.**
Of the C0 diff's production churn, this one file is `+1275/-1026` of `+1596/-1050` (80 % of the
lines, 1 of 12 files) and **2,287 of its 2,301 changed lines are layout** — a whole-file
re-serialization (`json.dumps(indent=1)`, everything expanded) for exactly **seven changed cells**.
The reduction costs nothing measured: with it, C2 reads `total=0 C2_R55_PASS=true docs=7/7` and C1
reads `total=0 C1_R55_PASS=true`, identical to C0.

The remaining 11 production files are minimal: `+321/-24`, no whitespace-only hunk, no mode change,
no rename, no delete.

## 3. Receipts (all runnable; `REC` = `.ufo/waves/round-55/w2/T55W2SimplDiff-receipts/`)

### R1 — what the registry diff actually contains (`REC/measure-churn.py`, output `REC/churn.txt`)

```
$ python3 REC/measure-churn.py /home/vgpnk/Projects/shokunin/tameshi-shokunin
rows base/c0: 56/56
schema equal: True
payload identical outside scratch_root: True
changed cells: 7
  repeat-control-selftest -> scratch_root
  bash-witness-selftest -> scratch_root
  pin-disposition-selftest -> scratch_root
  evidence-disposition-selftest -> scratch_root
  context-capture-selftest -> scratch_root
  registry-check-selftest -> scratch_root
  env-diff-selftest -> scratch_root
diff lines: +1275 -1026 (semantic +7/-7, layout +1268/-1019)
file lines base/c0: 1028/1277 (+249 from re-serialization)
whitespace-collapsed bytes identical except the seven cells: True
```

Exit 0. Verdict: **seven cells, nothing else**. The `+249` lines come from expansion: the base
carries 57 inline arrays/objects — every one of them after line 833, i.e. the rows added from
round-20 on were written compactly on purpose — and C0 expands all 57 one element per line (C0
retains 0). Every remaining line is re-indented 2 → 1 spaces. No duplicate key was collapsed
(checked with an `object_pairs_hook`), file mode stayed `100644`, both files end with `]\n}\n`, no
BOM, no CRLF.

### R2 — the minimal patch (`REC/make-minimal.py`), regenerated and byte-compared

```
$ python3 REC/make-minimal.py /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/regenerated.json
patched cells: 7 (bash-witness-selftest,context-capture-selftest,env-diff-selftest,evidence-disposition-selftest,pin-disposition-selftest,registry-check-selftest,repeat-control-selftest)
lines base/out: 1028/1028
payload == C0: True
$ cmp $S/regenerated.json $S/lane/tools/registry.json
BYTE-IDENTICAL to the committed minimal file
```

Exit 0. The generator reads the **base** bytes, substitutes the seven `scratch_root` values C0 wrote
(`json.dumps` of C0's parsed values, so escaping cannot drift), and leaves every other byte as the
base had it. Output: 1028 lines, i.e. the base layout, not the reformat.

### R3 — the patch the L1 can apply at C0 (`REC/registry-c0-to-minimal.diff`, `REC/patch-stat.txt`)

```
$ git -C $S/lane diff --stat 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb minimal-registry -- tools/registry.json
 tools/registry.json | 2301 ++++++++++++++++++++++----------------------------
 1 file changed, 1026 insertions(+), 1275 deletions(-)
$ git -C $S/lane diff --numstat 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb minimal-registry -- tools/registry.json
1026	1275	tools/registry.json
```

i.e. the undo of the reformat on one path. `REC/registry.minimal.json` is the resulting file.

### R4 — the patch applies at C0 and leaves a 7-line diff (`REC/patch-applies.txt`)

```
$ git clone --shared <lane> applytest; git -C applytest checkout 9cf0146b94
$ git apply --check REC/registry-c0-to-minimal.diff
APPLIES_CLEANLY_AT_C0
$ git apply REC/registry-c0-to-minimal.diff
$ git diff --numstat 0a2010acd1 -- tools/registry.json
7	7	tools/registry.json
$ cmp tools/registry.json REC/registry.minimal.json
BYTES == registry.minimal.json
```

Verdict: applying the receipt at C0 turns the file into seven insertions / seven deletions against
base. No other path is touched.

### R5 — C2's docs arm and the whole frozen counter at the reduced file (`REC/c2-minimal.stdout`)

Run at the reduced commit `7cc824b4ecdb5cc3e62cab48a52a1cb5748fc74d` (C0 + `registry.minimal.json`,
scratch clone only), frozen counter `.ufo/evidence/round-55/c2/measure.py`, empty `--work`:

```
$ python3 .ufo/evidence/round-55/c2/measure.py --lane $S/lane --rev 7cc824b4 --work $S/c2work --explain
EXPLAIN grammar <9 modes>            rc=2  ok          (9/9)
EXPLAIN lazy    <5 modes>            rc=0  ok          (5/5)
EXPLAIN empty   <13 modes>           rc=0  ok          (13/13)
EXPLAIN usable  <13 modes>           rc=0  ok          (13/13, tmp_mkdirs=0)
EXPLAIN docs                                      7/7 ok
EXPLAIN note                                      9/9 ok
EXPLAIN skill                                     1/1 ok
C2_R55: rev=7cc824b4ecdb grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
EXIT=0
```

Verdict: **the docs arm is 7/7 on the reduced file and the full counter passes with `total=0`** —
the reduction repeats C0's own verdict exactly.

### R6 — C1 unaffected (`REC/c1-minimal.stdout`)

```
$ python3 .ufo/evidence/round-55/c1/measure.py --lane $S/lane --rev 7cc824b4 --work $S/c1work2 --explain
EXPLAIN R54.1 .. R54.10   ok premise=ok corrected=ok stale=0
C1_R55: rev=7cc824b4ecdb classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

Exit 0. Neither frozen counter opens `tools/registry.json` except C2's docs arm, which `json.load`s
it (`c2/measure.py:244`); C1 reads `.ufo/waves/round-54/w1-registry.json`, never this file.

### R7 — `registry-check` on the reduced file

```
$ python3 tools/registry-check.py --selftest      (cwd = reduced clone, usable TMPDIR)
SELFTEST: PASS (51 cases)
EXIT=0
```

### R8 — the cost the reformat pays in blame (`REC/blame-cost.py`, output `REC/blame.txt`)

```
base            rev=0a2010acd1 lines=1028 distinct-owner-commits=17 top=636, 140, 46, 40
C0              rev=9cf0146b94 lines=1277 distinct-owner-commits=2  top=1275, 2
counterfactual  rev=b6a5b31ffa lines=1028 distinct-owner-commits=17 top=636, 140, 46, 40
```

The counterfactual is a child of base carrying only the seven replacements. At C0 **1,275 of 1,277
lines are owned by the C0 commit** — every row's history (round-17 x636, round-18 x140, round-24,
round-21, ...) is gone; the seven-line patch changes seven lines' ownership and leaves the other
1,021 attributions intact. Verdict: the reformat destroys the registry's audit trail, which is the
exact artifact later rounds' "record must agree with tree" checks read.

## 4. Composition with the cells' final text (the worktree is moving)

While I measured, a wave-2 sibling had `tools/registry.json` modified in the lane worktree —
`7/7` against **C0's reformatted file**, rewriting the seven cell strings again (the tool token each
tool actually prints, and the dropped per-row mode claim). So the reformat is still there and the
cell text is not C0's. The reduction is a *layout* operation and must compose with whatever cell text
lands, so the generator takes the value source as an argument (default C0) and I proved both cases:

- `REC/registry.minimal.json` — C0's values, base layout, payload == C0 (R2).
- `REC/registry.minimal-with-w2-cells.json` — the sibling's cell text (`REC/worktree-cells-source.json`,
  snapshot), base layout, payload identical to their file:

```
$ python3 REC/make-minimal.py <lane> REC/registry.minimal-with-w2-cells.json REC/worktree-cells-source.json
patched cells: 7 (...)
lines base/out: 1028/1028
payload == source(REC/worktree-cells-source.json): True
$ git apply --check REC/registry-w2cells-to-minimal.diff     # clone at C0 carrying those cells
APPLIES_CLEANLY_ON_W2_CELLS
$ git diff --numstat 0a2010acd1 -- tools/registry.json       # after apply
7	7	tools/registry.json
```

(`REC/compose-w2cells.txt`.) Conclusion: **one lane step, not two** — land the final cell text, then
run `make-minimal.py` with that file as the source and commit the resulting file. If the cells change
again, re-run; the generator is value-agnostic. My C1/C2 receipts (R5, R6) are at C0's cell text;
`docs=7/7` depends only on the grammar marker, which every version of the cells carries, but the
counters should be re-run once the cell text is final (cheap: 7 min for C2).

## 5. Other production churn — swept, none avoidable

```
$ git diff --numstat 0a2010acd1 9cf0146b -- <path>  vs  git diff -w --numstat ...
LOG.md                                    all=36+3  -w=36+3
SCORECARD.md                              all=90+6  -w=90+6
corpus/knowledge/scratch-root-contract.md all=37+1  -w=37+1
corpus/lessons/round-54.md                all=10+6  -w=10+6
corpus/QUALITY.md                         all=1+1   -w=1+1
corpus/SOURCES.md                         all=4+1   -w=3+0
SKILL.md                                  all=7+3   -w=7+3
tools/repeat-control.py                   target edit only (class, could_not_evaluate, one except arm)
tools/context-capture.py                  target edit only (class, raise, one except arm)
tools/registry-check.py                   target edit only (class, raise, two except arms)
```

- No whitespace-only hunk anywhere: `-w` equals the plain numstat for every file. The only
  whitespace line is `corpus/SOURCES.md`, whose base blob was the sole file in the change set with
  **no newline at EOF** (`BASE-NO-EOF-NEWLINE: corpus/SOURCES.md`); C0 ends it with `\n`. That is a
  defect fix worth its one line, not churn.
- No `mode change`, `rename`, or `delete` in the whole base→C0 diff (`git diff --summary`).
- `LOG.md`'s edits to the round-54 entry (`7883e0e5` → one pointer `077d431e`; `25` → `28` wave-1
  findings) are **ER-R54-2** and **ER-R54-5** of the corrections section, i.e. routed C1 work, not
  drive-by rewriting.

## 6. Evidence churn — named, not removable by this seat

`REC/evidence-census.txt` (`.ufo/waves/round-55/w1/`, 1,260 files, 7,380,369 bytes):

```
duplicate blob groups (non-empty): 39, redundant bytes: 184607
   2 copies x  59251 bytes  .../T55W1ScribeSources-receipts/sources/sysexits.html
  19 copies x   1604 bytes  .../census-start.stdout (the same census output in 19 seats)
   3 copies x   7147 bytes  .../page-text/gnu-errors-2026-10-28.html
   7 copies x   2276 bytes  .../c1-base.stdout
   2 copies x  11908 bytes  .../T55W1ExecRekeyPrep.json
zero-byte receipts: 108
```

Verdicts:
- **Keep the zero-byte receipts.** 108 files with no stderr are the observation "this arm printed
  nothing"; deleting them deletes the evidence, not the weight.
- **Keep the duplicated per-seat receipts**, even the 19 identical census outputs: each is the
  observation of *that* seat's run, and a consolidated copy would break the `Report:` path each seat
  cites. 184 KB of 7.4 MB (2.5 %) is the price of per-seat provenance; reducing it would harm the
  provenance axis, so I stopped there.
- **Name one accuracy hazard**: `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/skill-after.md` is a
  whole-file copy (2,201 lines) of `SKILL.md` taken **before** the `## Standing rules` bullet was
  rewritten for the ninth mode; it differs from `SKILL.md@C0` in exactly that bullet
  (`Measured on each allocating mode the counter runs — the seven self-tests plus env-diff --contract`
  vs C0's `... plus env-diff --contract and registry-check --rev`). A reader who opens it as "the
  section after the edit" is reading a superseded wording of the very section this round re-keys.
  It is evidence, so it stays; the L1 should not cite it for the section's C0 bytes.

## 7. Tradeoffs / what I did not do

- My patch is **value-preserving**: it copies C0's seven strings verbatim, so it neither fixes nor
  worsens the wave-1 finding `T55W1ScribeCells.md` **F6** (four of the seven landed cells quote a
  line shape the tool does not print) or **F2** (`repeat-control` still writes
  `REPEAT_CONTROL: setup_error` to stdout beside the stderr class line). Those are content defects
  of the cells and of the tool, not minimality defects, and fixing them here would have changed what
  the frozen counters score.
- I did not normalize the file to one convention. The base is itself mixed (2-space rows, then
  hand-compacted inline rows from round-24 on); the reduced patch keeps that mix and introduces
  nothing new. If the round wants one canonical serialization, that is a separate no-semantic-change
  commit that must re-establish blame afterwards — it must not ride on a seven-cell edit.
- Reduction stops here: with the registry at seven lines, the next-largest avoidable item is the
  184 KB of duplicated evidence, and deleting it would break per-seat provenance.

## 8. Integration artifacts for the L1

| artifact | what it is |
|---|---|
| `REC/registry.minimal.json` | the reduced `tools/registry.json` (1,028 lines, 7 cells changed vs base, payload == C0) |
| `REC/registry-c0-to-minimal.diff` | the patch that takes C0's file to that state (`git apply` at C0, proven) |
| `REC/registry.minimal-with-w2-cells.json`, `REC/registry-w2cells-to-minimal.diff`, `REC/compose-w2cells.txt` | the same reduction over the sibling's corrected cell text (§4) — the file/diff to use if the cell rewrite lands |
| `REC/worktree-cells-source.json` | the lane worktree snapshot those were built from (re-run the generator if the cells change again) |
| `REC/churn.txt`, `REC/blame.txt`, `REC/evidence-census.txt`, `REC/patch-applies.txt` | measured outputs quoted above |
| `REC/c2-minimal.stdout`, `REC/c1-minimal.stdout` | both frozen counters at the reduced commit |
| `REC/measure-churn.py`, `REC/make-minimal.py`, `REC/blame-cost.py`, `REC/evidence-census.py` | the runnable receipts |

Scratch (`/fast/scratch/hyaku/tameshi-r55/T55W2SimplDiff/`) is removed on exit; every number above
is reproducible from the lane plus `REC/*.py`.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → `CENSUS_EXIT=0` (15 pre-existing `W04` duplicate-url
warnings, final row `tameshi ok`), unchanged by this seat.

Report: .ufo/waves/round-55/w2/T55W2SimplDiff.md
