# T56W1ScribeQuality — QUALITY criterion 107 draft (round 56, wave 1)

Seat: `T56W1ScribeQuality` (scribe, leaf — no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; frozen instrument set `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.
Item: draft **one** new `corpus/QUALITY.md` criterion stating C2's receipt-revision rule, append-only, numbered
after the current maximum, carrying the rule, its falsifier (exact command + exact refusal code on the real
round-54 receipt), the `corpus/lessons/round-56.md` pointer, and the `considerthese/2026-10-28.md` proposal 1
pointer with the scope statement.

No lane production file and no frozen instrument was edited. Everything below is either a read, a run of a
committed instrument, or a write under `.ufo/waves/round-56/w1/` and my scratch (`/fast/scratch/hyaku/tameshi-r56/T56W1ScribeQuality`).

## 1. Number derivation (derived, not assumed)

```
$ git -C "$L" show 981c5e8b:corpus/QUALITY.md | grep -oE '^### Criterion [0-9]+' | awk '{print $3}' | sort -n | tr '\n' ' '
76 77 78 79 80 81 82 83 83 84 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106
$ ... | sort -n | tail -1
106
```

Maximum is **106**, so the new criterion is **107**. Two facts the integrator must not re-derive differently:

- The file's criteria begin at 76 (1–75 are earlier history); the highest is 106.
- `### Criterion 83` occurs twice at base — the second is the erratum heading
  `### Criterion 83/84 — falsifier correction (round 43, appended)` at `corpus/QUALITY.md:1107`. **85 is absent.**
  So "next" is 107, not 86; the gap is not re-usable.
- Round 55 appended no criteria block (its tail is the erratum on 105), so the round-56 block header is new.

Receipt: `T56W1ScribeQuality-receipts/107-base-state.txt`.

## 2. Non-duplication against the last five criteria (read first)

| Criterion | What it already governs | Why 107 is not it |
|---|---|---|
| 102 | a selftest verdict is invariant under renaming its fixture (oracle inputs) | about mutation-suite oracle naming, not receipts |
| 103 | a tool change lands with its registered gate row and its SKILL statements | about *landing* a tool change; 107 is about the rule the tool enforces and its exercise on accepted receipts |
| 104 | a fix-pass hunk is re-read before commit (duplicate phrases, citations) | editorial hygiene of hunks; no receipt binding |
| 105 | a counter arm is proven on a positive control, not only the do-nothing tree | about *arms* firing; 107 is about a receipt's own `rev=` vs the certified revision |
| 106 | a pre-registered control is scored at the revision it certifies | about *where a control is run* (its clone target); 107 is about what the receipt **names** and whether a tool refuses it. 106's own falsifier is the same round-54 receipt, but 106 asks "was the control scored at C?" — 107 asks "does the certified receipt carry a checkable `rev=`, and does the gate refuse the real accepted ones?" |

Also cross-checked (not duplicated): 86 (when C is designated and what may lie between C and the tip), 97
(a cited evidence path resolves at the landing tip), 99 (a control is scored and committed before the deciding
run). 107 states its relation to 86 explicitly in the text; 97 is cited in the scope sentence for the existence
half. Criteria 1–75 live outside this file's tail and were not candidates for duplication (they predate the
receipt gate, which was frozen this round).

## 3. The exact criterion text (append this, verbatim)

Append after the current last line (`.ufo/evidence/round-54/after/deciding-run.exit` erratum block ends at
`corpus/QUALITY.md:1612` with `deleted.\n`). 62 added lines, one file touched:

````text

## Criteria appended — round 56 (2026-10-28)

### Criterion 107 — a certified receipt names the revision it was measured against, and the gate refuses the ones that do not

Every receipt a round certifies — a control, a positive control or a verdict — states in its
own bytes the revision it was measured against (`rev=<sha>` or `"rev": "<sha>"`), and the lane's
certification path runs `tools/receipt-revision-gate.py` over it. A receipt whose named revision
is content-identical to the certified revision on the surface the round declares with `--paths`
is accepted even when the two shas differ (the surface did not move); a receipt whose named
revision differs on that surface is refused `RECEIPT_REV_CONTENT_DRIFT`, one whose `rev=` does
not resolve in the lane is refused `RECEIPT_REV_UNRESOLVABLE`, one that names no revision at all
is refused `RECEIPT_REV_ABSENT`, and a receipt path that does not exist is refused
`RECEIPT_MISSING`. The rule is not satisfied by a record that cites a receipt in prose: the
receipt is refused or accepted on its own bytes, and a round that lands this rule also lands the
refusal of a receipt the lane already accepted. Distinct from criterion 86, which governs *when*
the content revision C is designated and what may lie between C and the landing tip; this
criterion governs the receipt's own binding, is enforced by a named tool with closed codes, and
is exercised on receipts accepted before the gate existed.

Check that can fail: over the real round-54 positive control
`.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout` — its only `rev=` is
`077d431e6996`, the round-54 freeze, while round 54 certified `c2108100` — run from any cwd:

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 "$L/tools/receipt-revision-gate.py" \
  --lane "$L" --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c \
  --paths "$L/.ufo/evidence/round-56/c2/red-before/round-54-surface.paths" \
  --receipt "$L/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout:positive"
echo "exit=$?"
```

It must print `code=RECEIPT_REV_CONTENT_DRIFT` on the `GATE REFUSED` line and
`codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED` on the summary line, and exit 3. The same
receipt with `--certified 077d431e69965fa4673cd006ab64f6fc387f9e15` — its own revision — must
print `verdict=PASS` and exit 0, so the refusal is a content comparison and not a constant. A
gate that passes this receipt, or that refuses it with a code other than the drift code, is the
failing instrument.

Lesson: `corpus/lessons/round-56.md` `## Gate` (the R55.5 disposition — round 55's deciding gate
could not compare the revision it certifies, and the round-54 control set the old path accepted
names `077d431e6996` on `CTL_POS_c1` and `7df0e0426c98` on `CTL_EXIT0` while the round measured
`c2108100`).

Motivation and scope: `considerthese/2026-10-28.md` (dated 2026-10-28) proposal 1,
"Receipt-existence linter for records". This criterion is that proposal's revision half, not its
quote half. Existence is checked — the receipt file (`RECEIPT_MISSING`) and the revision it
names (`RECEIPT_REV_UNRESOLVABLE`), with criterion 97 covering a cited evidence path at the
landing tip — and the receipt's own `rev=` is compared against the certified revision on the
declared surface. What this criterion does NOT cover is byte-for-byte matching of a quoted
counter line against committed stdout: a receipt naming the certified revision whose printed
numbers are fabricated still passes the gate
(`.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`, exit 0
on `rev=077d431e6996 credited=99 lost=0`). That half of the proposal stays unmined.

Falsifier that must fail: the command above at the round-56 freeze `c3e2ca9f`, where the gate
and the frozen receipt exist and the rule is stated nowhere a reader meets it —
`corpus/QUALITY.md` names neither `tools/receipt-revision-gate.py` nor any `RECEIPT_*` code (the
round-56 C2 counter's `docs=0/4` arm) — while round 54's deciding run accepted the set this
command refuses
(`.ufo/evidence/round-54/after/deciding-run.exit` reads `DECIDING_RUN_EXIT=0`).
````

Machine-readable copy: `.ufo/waves/round-56/w1/T56W1ScribeQuality.json` (`text` field is the same block).

## 4. The falsifier, run (both directions)

**Red — the real round-54 receipt, certified at `c2108100`** (`107-red-round54.txt`):

```
$ python3 tools/receipt-revision-gate.py --lane $L --certified c21081008adbb6b6fe4e58a0aeec4831b30e318c \
    --paths .ufo/evidence/round-56/c2/red-before/round-54-surface.paths \
    --receipt .ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout:positive
GATE REFUSED .../round-54-ctl-pos-c1.stdout role=positive revs=077d431e6996 code=RECEIPT_REV_CONTENT_DRIFT \
  rev=077d431e6996 drift=.ufo/evidence/round-21/coldread/ledger.json,.ufo/waves/round-54/w1/T54W1Crit02-receipts/coldread-at-base.json,...
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED
exit=3
```

Exact code: **`RECEIPT_REV_CONTENT_DRIFT`**, exit **3**. The drift list is non-empty on 68 paths
(`107-drift-count.txt`), so the refusal is not a vacuous comparison of two identical trees.

**Green control — the same receipt at its own revision** (`107-bound-control-round54.txt`):
`--certified 077d431e69965fa4673cd006ab64f6fc387f9e15` prints `GATE OK ... revs=077d431e6996`,
`codes=none verdict=PASS`, exit 0. The code is content-sensitive, not constant.

**The set the old path accepted** (`107-round54-accepted-set.txt`): `.ufo/evidence/round-54/control/controls-b.stdout`
names `rev=077d431e6996` (CTL_POS_c1, CTL_POS_c2) and `rev=7df0e0426c98` (CTL_EXIT0);
`git cat-file -t 7df0e0426c98` → `fatal: Not a valid object name` (exit 128); the gate refuses the file with
`codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED`, exit 3; and `.ufo/evidence/round-54/after/deciding-run.exit`
reads `DECIDING_RUN_EXIT=0`. Both facts the criterion's falsifier sentence cites are receipts, not assertions.

**Code vocabulary closed** (`107-gate-selftest.txt`): `GATE_SELFTEST: 14/14 pass`, exit 0, including
`CASE codes-closed PASS` — the criterion names 4 of the gate's 11 codes and cannot go stale by a code being
silently added.

## 5. Scratch-clone demonstration of the append

`git clone --shared` of the lane at base into scratch, `checkout --detach 981c5e8b…`, toplevel asserted
(`TOPLEVEL_ASSERT_OK`), the block appended, then (`107-scratch-clone-demo.txt`):

```
--- git -C $S/clone diff --stat
 corpus/QUALITY.md | 62 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 62 insertions(+)
--- git -C $S/clone diff --name-only
corpus/QUALITY.md
--- the C2 counter's arm-6 QUALITY sub-check, run over the patched file
arm6-quality gate_path_present=True code_present=True codes_in_text=RECEIPT_MISSING,RECEIPT_REV_ABSENT,RECEIPT_REV_UNRESOLVABLE,RECEIPT_REV_CONTENT_DRIFT
arm6-quality -> 1/1
```

So the criterion alone moves the C2 counter's arm 6 from `0/4` to `1/4` (the other three cells are the
knowledge note, the SKILL rule and the registry cell — other seats). No other path changes; the append cannot
touch a cold-read pinned section of `SKILL.md` because it touches no `SKILL.md` byte.

## 6. Findings

- **F107-1 (limit, not a defect): the `--paths` surface is the round's to declare, and a narrow surface makes
  the gate near-vacuous.** With `--paths`, a receipt whose rev differs but whose listed paths are identical is
  accepted by design ("the surface did not move"). Without `--paths` the same receipt reads
  `RECEIPT_REV_MISMATCH` (`107-red-round54-nopaths.txt`, exit 3). The criterion pins the `--paths` form with the
  frozen `.ufo/evidence/round-56/c2/red-before/round-54-surface.paths`, so the falsifier cannot be weakened by a
  seat choosing a one-file surface; but a future round could. Reported, not patched (instruments are frozen).
- **F107-2 (scope gap, demonstrated): proposal 1's quote half is unmined.** A receipt naming the certified
  revision `077d431e6996` with its numbers rewritten (`credited=60 lost=4` → `credited=99 lost=0`) prints
  `GATE OK ... verdict=PASS`, exit 0 (`107-scope-gap-fabricated-line.txt`). This is why the criterion says in
  terms what it does not cover; a reader must not read 107 as a byte-for-byte quote check.
- **F107-3 (numbering hazard for the integrator):** `### Criterion 83` appears twice at base
  (`corpus/QUALITY.md:1049` and the `83/84` erratum at `:1107`) and 85 is missing; any "next = max + 1"
  computation must use `sort -n | tail -1` over `^### Criterion [0-9]+`, which is 106 → 107.
- **F107-5 (hygiene note for the L1, outside my item):** at the freeze `.ufo/evidence/round-56/before/` and
  `census-start.{stdout,stderr}` are **untracked**, while the contract cites `before/c1.stdout` and
  `before/c2.stdout`. If C0 does not carry them, records citing those paths fail criterion 97
  (`107-pointer-resolution.txt`, last section). I did not touch them.
- **F107-4 (dependency, not a defect):** the criterion's own evidence pointer
  `.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt` must be **committed**
  in C0 or criterion 97 fails on this criterion. It lives under `.ufo/waves/round-56/w1/`, the same class of
  path round 54 and 55 committed.

## 7. Landing dependencies (what C0 must also contain for 107 to be true as written)

1. `corpus/lessons/round-56.md` must exist at C0 with a `## Gate` section carrying the R55.5 disposition (the
   lesson seat owns it). The criterion cites `## Gate`, not a row number, so it does not depend on row order.
2. `.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout`, `…/round-54-surface.paths` and
   `.ufo/evidence/round-54/after/deciding-run.exit` must be in C0's tree — all three are committed at the
   freeze `c3e2ca9f` (verified with `git cat-file -e`, `107-pointer-resolution.txt`). The gate and the
   red-before slice exist **only from the freeze**, not at base, which is why the falsifier sentence names
   `c3e2ca9f` and not `981c5e8b`.
3. My receipts directory must be committed (F107-4).
4. The rule sentence "the lane's certification path runs `tools/receipt-revision-gate.py`" is made true by the
   registry cell and the `## Standing rules` SKILL line — other wave-1 seats. 107 does not restate them.

## 8. Out of scope / not done by this seat

- No edit to `corpus/QUALITY.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`, or anything
  under `.ufo/evidence/round-56/`. The criterion exists only as text here and in the JSON, plus the scratch
  clone demonstration.
- No `corpus/knowledge/receipt-revision-binding.md`, no SOURCES row, no registry cell, no lesson, no SCORECARD
  or LOG block — other seats' items.
- No counter run beyond the gate itself: I did not run the C2 or C1 claim counters (they need C0's full
  content; running them here would only reproduce the `before/` receipts).
- No tool installed or upgraded (nothing was needed); `pacman` untouched.

## 9. Receipts index (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/`)

| File | What it shows |
|---|---|
| `107-base-state.txt` | base has no gate mention, no `RECEIPT_*` code, max criterion 106, 85 absent |
| `107-red-round54.txt` | the falsifier: `RECEIPT_REV_CONTENT_DRIFT`, exit 3 |
| `107-bound-control-round54.txt` | the same receipt at its own rev: `PASS`, exit 0 |
| `107-red-round54-nopaths.txt` | without `--paths`: `RECEIPT_REV_MISMATCH` (F107-1) |
| `107-drift-count.txt` | `drift_lines=68` between `077d431e6996` and `c2108100` on the declared surface |
| `107-round54-accepted-set.txt` | round-54's accepted controls, `7df0e0426c98` unresolvable, gate refuses, old run exit 0 |
| `107-gate-selftest.txt` | `GATE_SELFTEST: 14/14 pass`, `codes-closed` |
| `107-scratch-clone-demo.txt` | append at base: 62 insertions, one file, arm-6 quality cell 1/1 |
| `107-scope-gap-fabricated-line.txt` | fabricated counter line on the certified rev passes (F107-2) |
| `107-pointer-resolution.txt` | every pointer in the criterion resolves at the freeze; `round-56.md` and `before/` do not yet |

Census at round start (conformance): `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ final line `tameshi ok …/tameshi-shokunin/corpus/SOURCES.md`, `census_exit=0`.
