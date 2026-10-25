# ScribeQuality — round 42 wave 1

Seat: L1Tameshi42.ScribeQuality. Findings first; drafts verbatim; evidence paths exact.

## 1. Findings

1. **Format/numbering confirmed.** `corpus/QUALITY.md` ends at criterion 80
   (line 967, `### Criterion 80 — name the pins a tool edit breaks, before the edit`).
   The last three criteria are 78 (`corpus/QUALITY.md:931`), 79 (`:944`), 80 (`:967`);
   criteria 76+ use `### Criterion N — <title>` headings with a rule block,
   `Lesson:` pointer, and `Falsifier that must fail:` cheque. Drafts 81/82 below
   follow that shape. No committed criterion 81/82 exists (round-41 w1 ScribeQuality's
   draft 81 was proposed, never committed; see `.ufo/waves/round-41/w1/ScribeQuality.md:44`).
2. **Criterion 81 evidence.** The frozen calibration counter prints
   `MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for
   .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true` at the base
   (`.ufo/evidence/round-42/before/c1-at-base.stdout:1`) — the live stale receipt.
   The do-nothing control shows the mismatch persists with all six round-41/42 records
   present (`records=6`) when no covering superseding receipt exists
   (`.ufo/evidence/round-42/control/c1-do-nothing.stdout:1-2`), i.e. a superseding
   receipt that repeats `present=false` or omits the path keeps `m10>=1`.
3. **Criterion 82 evidence.** The census counter commits the oracle in its docstring
   (`.ufo/evidence/round-42/census/measure.py:16-21`: "a mutant is `killed` only when
   every run exits 0 with parseable output AND at least one battery case differs … a
   mutant whose run exits non-zero, prints a Traceback or unparseable output is
   `runtime_error` — PIT's "Run error" and Stryker's RuntimeError, which neither tool
   counts as a kill — and a mutant with no differing case is `survived`") and implements
   it at `measure.py:313-317` (`errors → runtime_error`; `fails → killed`; else survived).
   Source rows: S001 Stryker (score excludes compile/runtime errors) at
   `corpus/SOURCES.md:12`; S155 = adopted PIT basic-concepts row (staged:S159), which
   carries PIT's "Run error" outcome class.
4. **Dependencies to note.** (a) `corpus/lessons/round-42.md` does not yet exist
   (read: not found) — both lesson pointers target it; consistent with how each round's
   criteria point at that round's lessons file, but the file must land this round or the
   pointers dangle. (b) S155 is staged (`staged:S159`; `.ufo/waves/round-42/assimilation/staged-ids:5`),
   not yet a row of `corpus/SOURCES.md` (grep `| S155 |` → no match; registry holds
   S001–S154, `reg-ids` 109 rows) — criterion 82's S155 citation requires the adoption
   to land in-round or m7 fires. (c) `mutants.json` does not exist yet; the mutation-
   tester seat writes it per the contract's mutant_protocol.
5. No tools installed (nothing needed); no lane files edited — drafts below are proposed
   text for `corpus/QUALITY.md`, not applied.

## 2. Draft criterion 81

```markdown
### Criterion 81 — a receipt that asserts file presence is written after the last write it describes

A receipt that asserts `present=<bool>` for a report path is written after the last
write of that path it describes; if it is not, an appended receipt supersedes it,
re-asserting every path of the superseded receipt, its own assertions agreeing with
the tree at the revision it is read against. A stale receipt — an assertion that
disagrees with the tree and is covered by no such superseding receipt — is a
calibration mismatch, not a dated restatement.
Lesson: `corpus/lessons/round-42.md`.
Falsifier that must fail: `python3 .ufo/evidence/round-42/calibration/measure.py
--lane LANE --rev c77c2b7e64d2e356381441ecf94abac03e984606
--freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f` must print
`m10=1 ... C1_R42_PASS=false` and exit 1 while
`.ufo/waves/round-41/residual/receipt.json` asserts `present=false` for
`.ufo/waves/round-41/residual/ResidualReceipts.md` (which the tree holds), and a
superseding receipt that repeats `present=false` or omits that path keeps `m10>=1`
(receipts: `.ufo/evidence/round-42/before/c1-at-base.stdout`;
`.ufo/evidence/round-42/control/c1-do-nothing.stdout`, records=6 yet m10=1).
```

## 3. Draft criterion 82

```markdown
### Criterion 82 — a kill oracle counts a mutant killed only when the run completes and a declared check fails

A kill oracle counts a mutant `killed` only when its run completes — every battery
run exits 0 with parseable output — and at least one declared battery case differs
from its declared classification. A run that exits non-zero, prints a Traceback or
prints unparseable output is a run error, not a kill (PIT's "Run error", S155;
Stryker's RuntimeError, which S001's score excludes); a mutant whose runs complete
with no differing case is survived.
Lesson: `corpus/lessons/round-42.md`.
Falsifier that must fail: `.ufo/evidence/round-42/census/measure.py` must classify a
mutant whose battery exits non-zero, Tracebacks or prints unparseable output as
`runtime_error` (outcome verb at `measure.py:313-317`) and never count it killed, and
a completed battery with no differing case as `survived`; `mutants_killed` equals
`mutants_declared` only when every declared mutant (>= 3, covering classes attr,
method, outflag) is killed with no run error and no survivor. The oracle vocabulary is
committed in the measure's docstring (`measure.py:16-21`), citing PIT's "Run error"
(S155, staged:S159) and Stryker's score excluding runtime errors (S001,
`corpus/SOURCES.md:12`).
```

## 4. Verification notes

- QUALITY.md read at `corpus/QUALITY.md` (997 lines; criteria 1–80; last three 78/79/80).
- Contract read at `.ufo/evidence/round-42/contract.json` (C1 m10 definition at
  `:28`; C2 kill_oracle at `:46`; adopted rows S155/S156/S157 at `:23-24` narrative).
- Evidence read: `.ufo/evidence/round-42/before/c1-at-base.stdout`,
  `.ufo/evidence/round-42/before/c2-at-base.stdout`,
  `.ufo/evidence/round-42/control/c1-do-nothing.stdout`,
  `.ufo/evidence/round-42/control/c2-junk.stdout`,
  `.ufo/evidence/round-42/control/c2-v3-in-slot.stdout`,
  `.ufo/evidence/round-42/census/measure.py`.
- Not checked: the counter's deciding run (only the L1 runs it; base/control receipts
  are the pre-run evidence), and the round-42 lessons file content (does not exist yet).

Report: `.ufo/waves/round-42/w1/ScribeQuality.md` (this file, relative to the lane root).
