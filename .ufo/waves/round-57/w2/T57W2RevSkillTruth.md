# T57W2RevSkillTruth — gate truth vs SKILL and registry rows at C0

Seat: T57W2RevSkillTruth (wave 2, falsify+repair). Milestone: gate truth vs SKILL and registry rows at C0.
Axis judged: operability.

Lane base `5e3569969b532310d2b8a3d130901757a3df356b`; content commit C0 `ca75c2674645ab6bdadeecb8584007c74342bfa9`.
No lane file was edited; no lane git command was mutating. Every command below ran in a scratch clone under
`/fast/scratch/hyaku/tameshi-r57/T57W2RevSkillTruth/` (deleted on exit). Tools used as found: Python 3.14.8,
git 2.56.0. No tool was installed or upgraded (nothing in this seat's scope needed one).

Verdict: **the three committed registry rows are TRUE at C0 and TRUE in every descendant I could build,
but the standing-rules table they certify is only half true, and the drift row does not discriminate the
case it is named for.** One finding is a repair the L1 can land in wave 3 (D2); two are honesty gaps that
must be written down rather than silently tolerated (D1, D3). Details, commands and outputs below.

---

## 1. What I ran (the sweep, with its output)

### 1.1 The gate truth table, re-run at C0 bytes

`tools/receipt-revision-gate.py` is byte-identical at base and C0 (`sha256 c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`
at both — measured). So the gate is unchanged; only its *documentation* and its *exercisers* changed.

Driver `T57W2RevSkillTruth-receipts/truth-table.py` (scratch fixture repo: c0 → c1 → c2 plus a side branch off c0;
`git rev-parse --show-toplevel` asserted equal to the fixture dir before every commit). Full output:
`T57W2RevSkillTruth-receipts/truth-table.txt`.

Result — every cell the w1 reports assert, re-measured at C0 bytes and **all agree**:

| role | `--paths` | certified | drift on the listed path | code | exit |
|---|---|---|---|---|---|
| verdict | absent | R2 | none | `RECEIPT_REV_MISMATCH` | 3 |
| verdict | absent | R3 | yes | `RECEIPT_REV_MISMATCH` | 3 |
| verdict | given | R2 | none | PASS | 0 |
| verdict | given | R3 | yes | `RECEIPT_REV_CONTENT_DRIFT` | 3 |
| positive | absent | R2/R3 | — | `RECEIPT_REV_MISMATCH` | 3 |
| positive | given | R2 | none | PASS | 0 |
| positive | given | R3 | yes | `RECEIPT_REV_CONTENT_DRIFT` | 3 |

`verdict` and `positive` gate **identically** in every cell (all 11 rows pair-for-pair), confirming w1's
finding (a) and the C0 edit to SKILL.md row 53 ("a positive receipt gates identically").

All 11 codes are reachable, none is dead; exits 0/1/2/3 all observed. `RECEIPT_REV_MISMATCH` fires **only**
without `--paths`; `RECEIPT_REV_CONTENT_DRIFT` **only** with `--paths`. This is the D1 finding from
`T57W1RevGateSurface` and it is confirmed, not refuted, at C0.

### 1.2 The registry check at C0

```
$ python3 tools/registry-check.py --rev ca75c2674645ab6bdadeecb8584007c74342bfa9 --tag new-r57
ROW receipt-gate-accept expect=0 got=0 held
ROW receipt-gate-content-drift expect=3 got=3 held
ROW receipt-gate-unresolvable-certified expect=2 got=2 held
REGISTRY_CHECK: held=3/3 superseded=0
rc=0
```

**held=3/3 as the milestone expects.** The same holds at the wave-1 evidence commit `06e9849` (3/3).

Full registry, base vs C0 (no tag): base `held=46/50`, C0 `held=49/53` — the same 4 pre-existing red rows
(`mutate-and-run-regression`, `sources-census`, `verify-round15`, `mte-interop-check`) at both revisions, so
C0 adds 3 rows and reddens nothing. That is the no-harm arm for the registry.

### 1.3 The C2 counter at C0

```
$ python3 .ufo/evidence/round-57/c2/measure.py --lane LANE --rev ca75c26 --work W --explain
EXPLAIN shortfall rows=0 / executed=0 / skill=0 / codes=0 / cell=0
EXPLAIN shortfall mutants=3
EXPLAIN mutants: mutants.json unavailable or pin mismatch
C2_R57: self=7d49e3c493b3 rev=ca75c2674645ab6bdadeecb8584007c74342bfa9 gate_rows=3 exits=0,2,3
         held=3/3 mutants=0/3 skill_row=1 codes_known=4/4 standing_cell=ok total=3 C2_R57_PASS=false
```

**The counter at C0 scores `C2_R57_PASS=false`, total=3, and the entire shortfall is the mutants arm.**
The reason is structural, not a defect in the rows: the counter reads its mutants from
`.ufo/evidence/round-57/c2/mutants.json` **at the measured revision**
(`measure.py`: `raw = show(lane, rev, MUTANTS_PATH)`), and that path is **not committed at C0** — the whole
`.ufo/evidence/round-57/c2/` tree is untracked in the lane (verified: `git ls-tree -r ca75c26 -- .ufo/evidence/round-57`
lists only `coldread-referent-r56.md`; the same holds at `06e9849`). When the same counter is run over a
scratch clone that *does* contain the tree — the L1's own `dry-c2.sh` — it passes:

```
$ bash .ufo/waves/round-57/dry-c2.sh
EXPLAIN mutants baseline-held=3/3
EXPLAIN mutant M1 accept-on-drift: killed by receipt-gate-content-drift(got=0)
EXPLAIN mutant M2 wrong-refusal-code: killed by receipt-gate-content-drift(got=3)
EXPLAIN mutant M3 exit-0-on-unresolvable: killed by receipt-gate-unresolvable-certified(got=0)
C2_R57: ... held=3/3 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R57_PASS=true
```

So the rows and the counter are sound; the *install* of `mutants.json` is what is missing from the tree.
This is the one concrete wave-3 action below (D2).

---

## 2. Findings, by severity

### D1 (medium) — SKILL.md's standing-rules table is true only for the `--paths`-given case; the row's own words describe a rule the gate does not implement

`SKILL.md:53` (the `## Standing rules` receipt table) now reads:

> | a verdict receipt names another revision (a positive receipt gates identically) | refused unless its bytes equal the certified revision on the declared `--paths` surface; with no `--paths` the code is `RECEIPT_REV_MISMATCH` | `RECEIPT_REV_CONTENT_DRIFT` |

This is a real repair of R56.2: the code cell now names `RECEIPT_REV_CONTENT_DRIFT`, the gate really emits
that (measured above), and the counter's `cell` arm recomputes it from the gate itself and agrees
(`standing_cell=ok`). Good.

But the **rule cell** is stated as a property of the situation, and it is not:

> "refused unless its bytes equal the certified revision on the declared `--paths` surface"

The rule presupposes a declared `--paths` surface. The situation cell says only "a verdict receipt names
another revision". Two situations satisfy that cell and neither is described correctly:

- **no `--paths` at all** → the gate refuses with `RECEIPT_REV_MISMATCH`, exit 3. The row's code cell says
  `RECEIPT_REV_CONTENT_DRIFT`. The rule cell mentions MISMATCH parenthetically, so the row is *internally*
  inconsistent: its own prose names a code its own code cell does not.
- **`--paths` present but the file lists nothing** (only comments) → measured:
  `GATE: ... codes=RECEIPT_REV_CONTENT_DRIFT ... detail='rev=... drift=<no --paths given: content identity is not checkable>'`, exit 3.
  The gate treats "a declared surface that is empty" as *drift*, with a message that says "no --paths given"
  although `--paths` **was** given. `SKILL.md:53` has no cell for this; the table offers a reader only
  CONTENT_DRIFT vs MISMATCH, and this third outcome matches neither reading.

Evidence (from `truth-table.txt`, rows `positive/old/no-paths` and `positive/old/paths-empty-file`):

```
positive/old/no-paths            positive  absent          3 RECEIPT_REV_MISMATCH       REFUSED
positive/old/paths-empty-file    positive  empty file      3 RECEIPT_REV_CONTENT_DRIFT  REFUSED
```

**Why this matters for operability (not pedantry):** SKILL.md is the page the round-21 cold-read monitor
grades and the page a consumer reads to know what the gate does. Row 53 is now the *only* place the lane
states this rule, and a reader who takes the code cell at face value will predict
`RECEIPT_REV_CONTENT_DRIFT` for a no-`--paths` verdict receipt and will be wrong. The row's own prose
contradicts its own code cell, which is the defect shape this round exists to remove.

**Repair (a staged diff, wave 3).** Two options; I recommend the first.

- (a) Split the row's situation so the code cell is unambiguous, and add the empty-`--paths` case:
  - row 53, situation → "a verdict receipt names another revision **and a `--paths` surface is declared**";
    code cell → `RECEIPT_REV_CONTENT_DRIFT`; rule cell keeps the MISMATCH parenthetical.
  - new row after 53: situation → "a verdict receipt names another revision **and no `--paths` surface is
    declared** (an absent file, or a file listing no path)"; rule → "refused: the receipt cannot be bound
    to the certified revision"; code → `RECEIPT_REV_MISMATCH` (with `--paths` absent) /
    `RECEIPT_REV_CONTENT_DRIFT` (with a declared-but-empty `--paths` file).
  This keeps every code the counter's `codes` arm checks (all four tokens stay members of `CODES`) and keeps
  the counter's `cell` arm satisfied — the counter looks up the row whose first cell starts
  `a verdict receipt names another revision` and compares the *last* cell's token set to the gate's emitted
  set. Adding a second row whose first cell starts with the same prefix would make `standing_cell` pick the
  wrong row, so the new row must NOT reuse that prefix — e.g. start it "a verdict receipt names another
  revision **with no declared surface**" and note in the report that the counter's `VERDICT_CELL_HEAD`
  prefix-matching means the *first* matching row wins (so the new row must come after and must differ in its
  first cell's leading text, or the counter needs a one-line amendment).
- (b) Amend the rule cell only, to state the three-way truth in one line:
  `refused unless its bytes equal the certified revision on the declared `--paths` surface; the code is
  `RECEIPT_REV_CONTENT_DRIFT` with a declared surface and `RECEIPT_REV_MISMATCH` without one; a declared but
  empty `--paths` file is refused as `RECEIPT_REV_CONTENT_DRIFT` (the gate cannot certify content identity
  on an empty surface)`.

Option (b) is a one-line edit and does not perturb the counter's row lookup. Option (a) is more faithful to
the table's shape but needs the counter's prefix guard checked. **I recommend (b) plus one extra table row
whose first cell does not collide with `a verdict receipt names another revision`.**

I did **not** stage the diff: the SKILL.md byte change is the L1's to install and it must be re-keyed under
`rekey-r57-<c0>` in wave 3 anyway (the cold-read monitor re-reads the headings C0 uncredited). The exact
wording above is the deliverable; the L1 lands it.

### D2 (medium, actionable, blocks C2 at C0) — the C2 counter's mutants arm is dead at every committed revision because `mutants.json` is not in the tree

The counter's mutants arm is the whole of C2's remaining shortfall at C0 (§1.3). It reads the mutants from
the **git object at the measured revision**:

```
measure.py:  raw = show(lane, rev, MUTANTS_PATH)     # MUTANTS_PATH = '.ufo/evidence/round-57/c2/mutants.json'
              if raw is None or sha256(raw) != MUTANTS_SHA256: raw = None
```

and `.ufo/evidence/round-57/c2/` is untracked in the lane (only `coldread-referent-r56.md` is committed
under `.ufo/evidence/round-57/` at both `ca75c26` and `06e9849`). So `C2_R57_PASS=false, total=3` at C0
**and** at the wave-1 commit, and the deciding run will score the same unless the file is committed.

The file exists and is correct — it is staged for install at
`.ufo/waves/round-57/w1/T57W1ExecC2Counter/stage/.ufo/evidence/round-57/c2/mutants.json`, and its sha256
equals the counter's pin `d51f558ca7a4f32c301eccd3bc5ce0814b11da8e16dac539058fbb843448e6de` (measured;
the working-tree copy at `.ufo/evidence/round-57/c2/mutants.json` has the same digest). `measure.py` itself
is likewise staged (`.../stage/.ufo/evidence/round-57/c2/measure.py`, sha256 `7d49e3c493b3…`, identical to the
working-tree copy).

**Action for the L1 (wave 3):** install `.ufo/evidence/round-57/c2/measure.py` and
`.ufo/evidence/round-57/c2/mutants.json` into the lane tree at the content commit the deciding run grades,
so the counter's mutants arm can read them at that revision. Verified end-to-end: with the tree present,
the same counter at the same bytes prints `mutants=3/3 … total=0 C2_R57_PASS=true` (`dry-c2.sh` output, §1.3).

### D3 (low-medium) — the committed drift row does not discriminate "the path was added" from "the path's bytes changed"; a gate mutant that breaks content-identity on an existing surface survives all three rows

This is the fuzzing the item asks for. The drift fixture is:

- `tools/fixtures/receipt-gate/drift.paths` → `corpus/lessons/round-56-verifier-spotcheck.md`
- `tools/fixtures/receipt-gate/drift.receipt` → `VERDICT: rev=c34e2b1486714ad6c1c6cbe706599ddfc9d60d55 …`
- certified → `5e3569969b532310d2b8a3d130901757a3df356b`

Measured: that path is **MISSING at the receipt rev `c34e2b1`** and **EXISTS at the certified rev `5e35699`**
(`git cat-file -e` on both). So the row's refusal is triggered by a path *added* between the two revisions,
never by a path whose bytes changed on a surface that existed at both.

I built the mutant that exploits this (**M4**: `drifted_paths()` returns only paths absent at `rev_a` and
present at `rev_b`, discarding the `git diff` output) and measured, in a scratch clone (`mutant-tests.txt`):

```
(a) the committed drift fixture still refuses:  codes=RECEIPT_REV_CONTENT_DRIFT   rc=3
(b) a path present in BOTH revs with DIFFERENT BYTES is now wrongly accepted:
    GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS   rc=0     (pristine gate: rc=3, CONTENT_DRIFT)
(c) the three registry rows against M4:  REGISTRY_CHECK: held=3/3 superseded=0
```

**M4 survives all three committed registry rows.** The positive control (the counter's own M1) *is* killed
by the same method (`held=2/3`), so the method is sound; the gap is the fixture's choice of surface.

The inverse mutant (M6: drift only for paths present at both revs) *is* killed (`held=2/3`) — because the
committed fixture also happens to trip the "added" branch. So the row is sensitive to the changed-bytes case
only incidentally; a gate implementing only the added-file case would pass.

The C2 counter's own `cell` arm **does** catch M4 — its fixture is rev A then B differing on one path listed
in `--paths`, i.e. a same-path byte change:

```
pristine     emitted=['RECEIPT_REV_CONTENT_DRIFT'] exit=3 verdict=REFUSED -> standing_cell=ok
M4-mutated   emitted=[] exit=0 verdict=PASS                          -> standing_cell=WRONG:fixture
```

So the *counter* is sound and the *row set* is the gap. Since the registry rows are what an operator
replays and what `registry-check --rev REV` reports to a reader, and since the round's claim is that the
gate is "operable from the entry registry", the drift row should exercise the case the gate exists for:
**content-identity on a surface that exists at both revisions**.

**Repair (wave 3), two parts:**
1. **Repoint the drift fixture at a same-path byte change.** No path in `corpus/` differs in bytes between
   `c34e2b1` and `5e35699` while existing at both (measured: `git diff --name-only c34e2b1 5e35699 -- corpus/`
   returns only added/modified-by-addition paths; the both-exist-and-differ set is empty). So the fixture
   needs a *new* pair of revisions, or a path whose bytes changed between `c34e2b1` and `5e35699`. The
   cheapest honest fix is to add a small dedicated fixture path to the gate fixture tree whose content
   differs across two named revs (e.g. commit a `tools/fixtures/receipt-gate/surface.txt` with different
   bytes at two of the lane's existing commits), and point `drift.paths` at it. That is a content change and
   belongs to the L1's installer.
2. **Add a fourth registry row** for the added-file case (or one row per case), so both drift shapes are
   pinned. The C2 counter's `rows` arm requires ≥3 gate rows and the exits {0,2,3}; a fourth row does not
   break it, and it raises the mutant-kill power from 3/3 to a set that includes M4's shape.

Until then, the honest statement of what the drift row proves is: *"the gate refuses a receipt that names a
revision at which the declared path did not exist."* It does **not** prove the content-identity rule on an
existing surface — which is exactly the rule SKILL.md:53 states.

### D4 (low) — the registry's `source` field is decorative

`registry-check.py` validates `source` only against `SOURCE_RE = ^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$`
(line 108) — the shape. It never resolves the revision and never checks that the cited line is the code the
row asserts. Measured: repointing `receipt-gate-content-drift`'s source to
`tools/receipt-revision-gate.py@5e3569969b532310d2b8a3d130901757a3df356b:1` (a line that is *not* the drift
branch) leaves `REGISTRY_CHECK: held=3/3 superseded=0`, rc=0.

For the three C0 rows the pins are, fortunately, *correct* (verified at the pinned rev `5e35699`):
`:220` is the `return 0 if verdict == 'PASS' else 3` verdict line; `:149-152` is the drift branch
(`drift = drifted_paths(...)`, `if drift:`, `codes.append('RECEIPT_REV_CONTENT_DRIFT')`, the detail line);
`:190-194` is the certified-resolution/`return 2` block. So the pins are accurate today — but nothing in
the lane would notice if they stopped being accurate. This is a lane-wide property of `registry-check`, not
a defect of the C0 rows; I record it as a residual risk, not a finding against C0.

### D5 (low) — the `--selftest` scratch-root claim in SKILL.md:1547 is narrower than the registry's own `scratch_root` cell

`SKILL.md:1547` says the gate's `--selftest` "writes one fixture repo under `$TMPDIR` (`tameshi-r56-gate-*`),
removed on exit". Measured: with `TMPDIR` set to a non-existent directory, Python's `tempfile.gettempdir()`
resolves to `/tmp` (measured: `gettempdir() -> /tmp`), the selftest runs `GATE_SELFTEST: 19/19 pass` and
exits 0, and **no** `could-not-evaluate` line is printed (`grep -c 'could-not-evaluate'` → 0). The registry's
`receipt-revision-gate-selftest` row says this plainly ("with TMPDIR unusable it falls back to the platform
default `/tmp` with no could-not-evaluate line and exit 0, so the round-55 scratch-root contract is NOT
implemented by this frozen instrument"). The SKILL cell omits the fallback clause.

Both are consistent with the gate being a *frozen* instrument (the registry row says so, and it is the
round-56-measured, deliberately-not-edited state). The finding is only that the SKILL cell is the weaker
statement. One clause fixes it: "…; with an unusable `TMPDIR` it falls back to `/tmp` and still exits 0 (the
round-55 scratch-root contract is not implemented by this frozen instrument — measured round 56)". Since
`SKILL.md:1547` was touched by C0, the L1 can add it in the same re-key pass.

Also observed (not a C0 defect): the selftest leaves **no** `/tmp` tree behind on a normal exit — the
pre-existing `/tmp/tameshi-r56-gate-ou1_0v2q` was there before my runs and the count was unchanged
(1 before, 1 after) across two selftest runs.

---

## 3. Shelf life of the three rows, and what makes them rot

Measured, each in its own scratch clone (`descendant-test.txt`, `rot-test.txt`):

| perturbation | result |
|---|---|
| baseline at C0 | held=3/3 |
| descendant commit touching an **unrelated** file (`corpus/UNRELATED-TOUCH.txt`) | held=3/3; certified rev `5e35699` and receipt rev `c34e2b1` both still resolve in the descendant |
| descendant commit **changing** the drift surface `corpus/lessons/round-56-verifier-spotcheck.md` | held=3/3 |
| descendant commit **deleting** the drift surface | held=3/3 |
| descendant commit **repointing** `drift.paths` at another path | held=3/3 |
| descendant commit **editing** `accept.receipt` to name an older rev | **held=2/3** — `receipt-gate-accept expect=0 got=3 differs` |
| descendant commit **renaming** `accept.receipt` | **held=2/3** — `receipt-gate-accept expect=0 got=3 differs` |
| descendant commit repointing `drift.paths` at a path that differs in *neither* pinned rev | **held=0/1** on that row (`expect=3 got=0 differs`) |
| history rewritten so the pinned revs are unreachable (orphan + ref delete + `gc --prune=now`) | **held=1/3** — `receipt-gate-accept expect=0 got=2 differs`, `receipt-gate-content-drift expect=3 got=2 differs` |
| live mode (no `--rev`) at C0 | held=3/3 |
| the real lane's wave-1 evidence commit `06e9849` | held=3/3 |

**The fuzz question the item asks directly — "does `receipt-gate-content-drift` still hold if
`corpus/lessons/round-56-verifier-spotcheck.md` changes later?"** — **YES, it holds.** The drift surface's
later content is irrelevant to the row: the gate compares the two *named historical revisions*, not the
working tree, so editing or even deleting that file in any descendant leaves the row at held=3/3. The row
is insensitive to the drift surface moving. That is the correct property and it is what makes the row safe
to keep.

**What actually rots the rows** (this is the shelf-life statement):

1. **The fixture files, not the surface.** `receipt-gate-accept` reads
   `tools/fixtures/receipt-gate/accept.receipt` from the working tree. Editing its `rev=` token or renaming
   the file turns the row red (`expect=0 got=3`) with no change to the gate. The `stdout_contains` needle
   `"GATE OK tools/fixtures/receipt-gate/accept.receipt role=positive"` also embeds the fixture *path*, so
   any move of the fixture directory breaks the row. The exit-2 row is the exception: it never reads the
   fixture (the certified revision fails first), so it survives the fixture being deleted — measured.
2. **`drift.paths` naming a path that does not differ between the two pinned revs.** The row then sees no
   drift and goes red (`expect=3 got=0`). A future round that repoints `drift.paths` at a "better" surface
   must pick one that actually differs between `c34e2b1` and `5e35699` — and today **no** path in `corpus/`
   does (measured: the both-exist-and-differ set over `corpus/lessons/`, `corpus/README.md`,
   `corpus/SOURCES.md` is empty), which is the concrete reason the fixture must be re-made (D3).
3. **A history rewrite that drops `5e35699` or `c34e2b1`.** Both rows then get `got=2`
   (`unresolvable-certified`) and the set drops to 1/3. The lane is append-only today, so this is a
   tail risk, but it is the one that ends the rows' life: they are pinned to two historical revisions by
   construction, and the *only* thing keeping them resolvable is that the lane never rewrites its history.
   The `source` field's rev (`5e35699`) is pinned to the same history.
4. **Nothing else I tried rots them.** Unrelated commits, changes to the drift surface, deletion of the
   drift surface, live mode, and the wave-1 descendant commit all keep held=3/3.

**Shelf-life statement for the L1:** the three rows are stable against everything the lane does
ordinarily (they survived every descendant I could construct, including the real wave-1 commit) and rot
only under (i) edits to `tools/fixtures/receipt-gate/`, (ii) a repoint of `drift.paths` at a non-drifting
path, or (iii) a history rewrite. (i) and (ii) are lane-internal and detectable by re-running
`registry-check --rev <rev> --tag new-r57` — which is exactly what the C2 counter's `executed` arm does on
every run, so a rot would be caught rather than silently tolerated. (iii) is the only silent one, and it
would show up as `got=2` in the same counter output.

---

## 4. Answers to the item's specific questions

**"every code/exit stated is true" (SKILL.md rows 53-56 and registry row 1547)**

- Rows 54, 55, 56: **true.** Row 54's "`RECEIPT_REV_CONTENT_DRIFT` (no `--paths`: `RECEIPT_REV_MISMATCH`)"
  is exactly the measured behaviour; row 55's "`RECEIPT_REV_UNRESOLVABLE` (exit 3; an unresolvable
  `--certified` itself exits 2)" is exactly measured; row 56's `RECEIPT_REV_ABSENT` is exact.
- Row 53: **true for the `--paths`-given case, and its code cell is contradicted by its own rule cell for the
  no-`--paths` case** (D1). The counter's `cell` arm passes only because it exercises the `--paths` case.
- Registry row 1547's Verdict map — "0 PASS; 2 certified revision unresolvable (`RECEIPT_REV_UNRESOLVABLE`);
  3 refused with a named code; 1 usage" — **is true as measured**: 0 for PASS, 2 for an unresolvable
  certified revision (and only that; a missing `--lane` also exits 2, which the map does not mention —
  the same "the lane is named as a revision" defect w1 flagged as D8, and the gate is frozen so it stands),
  3 for every named refusal, 1 for usage errors **and for uncaught tracebacks** (a missing `--paths` file
  exits 1 with a `FileNotFoundError` traceback and no `usage:` line — measured). The map's "1 usage" is
  therefore narrower than the truth: exit 1 also covers an uncaught exception. w1's D3 said the map "must
  add `1 usage or uncaught error (no named code)`"; C0's SKILL row 1547 did not adopt that wording, though
  `corpus/knowledge/gate-row-exit-map.md` (landed in the same commit) **does** say exactly that. So the
  lane now holds two documents with different exit maps: the knowledge doc is right and the SKILL cell is
  thin. One clause fixes the SKILL cell: "1 usage or uncaught error (no named code)".
  The counter's `skill_row` arm only requires the tokens 0, 2, 3 to be present in the cell, so it cannot see
  the thinning — hence the finding.
- The registry's own `receipt-revision-gate-selftest` `scratch_root` cell says "Refusal codes, each a named
  refusal at exit 3: … RECEIPT_REV_UNRESOLVABLE …" — but the *same* registry carries the exit-2 row, where
  `RECEIPT_REV_UNRESOLVABLE` is emitted at exit 2 (measured: rc=2 with
  `codes=RECEIPT_REV_UNRESOLVABLE`). The registry contradicts itself on that one code's exit class. The
  gate is frozen and the cell is round-56 text, but the cell is now wrong *because* C0 added the exit-2 row.

**"every code the gate can emit in a role × paths situation appears or is explicitly out of scope"**

All 11 codes are reachable (measured; `truth-table.txt` lists each with its case). Where each is scoped:

- SKILL.md `## Standing rules` names **4** of the 11 (`RECEIPT_REV_ABSENT`, `RECEIPT_REV_CONTENT_DRIFT`,
  `RECEIPT_REV_MISMATCH`, `RECEIPT_REV_UNRESOLVABLE`) — the counter's `codes` arm checks exactly this set
  (`codes_known=4/4`), and the standing-rules section carries no token outside `CODES`.
- The other **7** (`RECEIPT_MISSING`, `RECEIPT_EMPTY`, `RECEIPT_NOT_BLOB`, `RECEIPT_REV_AMBIGUOUS`,
  `RECEIPT_CONTROL_NOT_ANCESTOR`, `RECEIPT_DIGEST_MISMATCH`, `RECEIPT_REQUIRED_LINE_MISSING`) appear
  **nowhere in SKILL.md** (grep count 0 each, measured). They are scoped out of SKILL.md's receipt table and
  *in scope* of the gate's own header docstring, which lists all 11 by name, and of the registry's
  `receipt-revision-gate-selftest` row, whose `scratch_root` cell enumerates all 11. The lane-demo receipt
  confirms the same partition: "codes emitted by no registry row: 9 […]" — and the exit-2 row C0 added does
  not change that partition (the three C0 rows emit 2 of the 11: `RECEIPT_REV_CONTENT_DRIFT` and
  `RECEIPT_REV_UNRESOLVABLE`).
  **So the coverage statement is: no code the gate can emit is unscoped — 4 in SKILL.md, 7 in the tool header
  and the registry's selftest row.** The one thing that is *not* stated anywhere is the cross-reference from
  SKILL.md to the other seven; a reader of SKILL.md alone cannot learn that `RECEIPT_CONTROL_NOT_ANCESTOR`
  exists. Given the SKILL cell at 1547 now names `CODES` as the pinned value for the row, the cross-reference
  exists at the registry level. I record this as a low-severity gap, not a defect.

**"run the three rows again after a later descendant commit that touches an unrelated file"** — done, held=3/3
(§3), and the certified revision `5e35699` and the receipt revision `c34e2b1` both remain resolvable in that
descendant.

---

## 5. Residual risk and verification gaps

- **The gate's own header docstring is still the pre-C0 text** and still says "Codes (each a named refusal,
  exit 3)" and "Exit 0 iff PASS" — the exit-2 path and the exit-1 traceback path are undocumented there.
  The gate is byte-identical to base and the lane treats it as a frozen instrument (the registry row says so
  explicitly), so this is routed, not repaired, at C0. But SKILL.md:1547 and `corpus/knowledge/gate-row-exit-map.md`
  now disagree with the tool's own header about the exit map; a reader who opens the tool sees the older,
  thinner statement first. Worth one sentence in the knowledge doc pointing at the header's staleness.
- **The `source` field of the three C0 rows is correct today but unverified by any tool** (D4). A future
  edit of the gate that shifts the cited lines will not turn the row red.
- **`--paths` absent vs `--paths` given-but-empty are not distinguished by SKILL.md** (D1) and the gate's
  empty-surface message says "no --paths given" when `--paths` *was* given (`<no --paths given: content
  identity is not checkable>`) — a message bug in a frozen instrument, recorded not repaired.
- **Not measured by me:** the `--json` mode's schema on the exit-2 path (I confirmed only that `--json` is
  ignored there: `json=no`, text output instead — the same defect w1 recorded as D4); the `PermissionError`
  branch on an unreadable receipt (w1 also left it unmeasured); the `RECEIPT_REV_AMBIGUOUS` per-role
  asymmetry w1 recorded as D11 (I confirmed the positive/verdict pair is identical and that `control` with
  two revs passes — `control/two-revs` → exit 0 — which is the intended behaviour, not a defect).
- **The C2 counter's `mutants` arm** can only be exercised over a revision that *contains*
  `.ufo/evidence/round-57/c2/mutants.json` (D2). Until it is installed, `C2_R57_PASS=false, total=3` is the
  correct reading of the counter at every committed revision — not a claim about the rows.

## 6. Tools

No tool was installed, upgraded or removed in this seat; every measurement used the tools already present:
`python3` 3.14.8 (stdlib only) and `git` 2.56.0. No pacman transaction was run.

## 7. Receipts

`T57W2RevSkillTruth-receipts/`

| file | what it is |
|---|---|
| `truth-table.py` | the driver that re-ran the gate's role × paths matrix at C0 bytes on a scratch fixture repo |
| `truth-table.txt` | its full output — every code, every exit, the reachability census |
| `descendant-test.sh` / `.txt` | descendant-commit and fuzz perturbations (unrelated file, drift surface changed, drift surface deleted, paths fixture repointed, orphan history) |
| `rot-test.sh` / `.txt` | shelf-life perturbations (fixture edited, fixture renamed, paths fixture repointed at a non-drifting path, orphan-with-tree history rewrite, live mode) |
| `mutant-tests.txt` | the M1 positive control, the M4 survivor, the M6 kill, the counter's `cell` arm vs M4, and the `source`-field test |

Scratch `/fast/scratch/hyaku/tameshi-r57/T57W2RevSkillTruth` was removed on exit. The lane was not edited:
`git status --porcelain` in the lane shows only the pre-existing `M corpus/routed-defects.json` (the C1
ledger, another seat's work) and untracked files.
