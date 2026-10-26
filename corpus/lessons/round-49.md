# Round 49 lesson

L1 TameshiR49 (hyaku run 9, attempt 1). Two claims on distinct axes, pre-registered before any seat with both counters, the
controls harnesses, the no-harm monitors and the deciding script (`.ufo/evidence/round-49/contract.json`, freeze
`14d03ea4270c6904064022b62b6faf467e5c0968`, `amendments: []`); controls scored at freeze bytes and committed at `6885adb4`
before wave 1. C1 calibration: the seven SKILL.md sections whose cold-read credit had lapsed are read pointer by pointer,
corrected and re-credited so that a record append cannot lapse them. C2 coverage (sourced, capability): the F10 pilot, one
property-based generator against `tools/staged-id-guard.py`, scored against a hidden mutant panel. Frontier step: rows S269
and S270, the mistake below, sourced claim C2. Assimilation: theme F10 from `merge/tameshi/` (rows admitted, two entries
refused, one deferred). considerthese: `considerthese/2026-10-26.md` proposal 3 mined (section below).

## Gate

Rows opened this round (contract v1 rule 1: URL, access date, ≤ 25-word located quote). Snapshots and fetch receipts:
`.ufo/waves/round-49/w1/T49ScribeRows.src/` (`fetch-receipts.json`), corroborated by `.ufo/waves/round-49/w1/T49ExecSrcQuickCheck/`
and `.ufo/waves/round-49/w1/T49ExecSrcSmallbone/` (independent fetches, identical sha256).

- **S269** — QuickCheck, Claessen & Hughes, ICFP 2000, DOI 10.1145/351240.351266 —
  `https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf`, accessed 2026-10-26, HTTP 200, 194,315 B, sha256
  `bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172`. The carrier is the article text (ACM ICFP '00 block,
  Crossref pages 268-279) on a course mirror; the ACM DL answered 302 → 403, so the publisher's own bytes are not the pin.
  Tier A for content. Quote (20 words), §2.4 Monitoring Test Data, p. 270: "The combinator collect will gather all values
  that are passed to it, and print out a histogram of these values". Second quote (14 words), Abstract, p. 268: "Properties
  are described as Haskell functions, and can be automatically tested on random input".
- **S270** — Smallbone, "Property-based testing for functional programs", Chalmers TR 76L, 2011 —
  `https://smallbone.se/papers/lic.pdf`, accessed 2026-10-26, HTTP 200, 1,269,821 B, sha256
  `eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08`. Tier B (the author's own report). Quote (19 words),
  §2.10 Generating Test Data, printed p. 34 (PDF p. 39): "As always with random testing tools, the quality of the test data
  determines the quality of the generated equations".

Recheck cells: both `365d` (valid cadence); no prose was stripped. Rows touched old → new: none (the two rows are new;
no held row's status, recheck or used-by changed). The two stale "Next unused id: S265" lines of the registry's notes are
corrected by an appended note (round 48 added S265-S268 without updating them).

### Assimilation (theme F10, `/home/vgpnk/Projects/shokuknow/merge/tameshi/`, read-only)

Id collision check in scratch (`.ufo/waves/round-49/w1/T49ExecIdGuard/`): `reg-ids` 128, `staged-ids` 103, `collisions` 8
(S153-S160, all known from rounds 45-47); none on S182/S183. Guard proof: a scratch registry with a 2-space `  | S182 |`
row yields a nonempty collision set (9 under `^ {0,3}`, 8 at column zero). Adopted ids continue the registry by document:
staged S182 → **S269**, staged S183 → **S270** (two non-colliding rows need no map; the guard's whole-package map rule
applies only to adopting colliding rows). Quarantine slice: neither S182 nor S183 is a row of the register's tameshi slice
by id; S182's DOI appears once as a never-checked line, S183's document not at all (`T49ExecIdGuard.md`).

- **Admit — staged S182 → S269** (re-grounded: own fetch, own quotes; the package's location "§Abstract and §1" missed
  where the generator material sits, so S269's anchor names §2.4 and §3.2 as well).
- **Admit — staged S183 → S270**, with its anchor **corrected**: the package places "good test data generators, that fit
  the program at hand" at §4.1, p. 44; it is at §2.10, printed p. 34 (p. 44 is §3.4 "Problems with Partiality", zero
  generator mentions; `T49ExecSrcSmallbone.md`). The package's presence-only recheck still returns 1 over the whole PDF,
  so it could not catch the wrong page.
- **Reject — `r4-quickcheck-primary-correction.md`.** Decisive reason (QUALITY 2, the claim must be true): the entry's
  identifying claim is that the lane's lead list carried DOI `10.1145/1660572.1660575`; the DOI occurs nowhere in the lane
  at base or in its history, and doi.org/Crossref answer 404 for it (`T49ScribePkgQuickCheckCorr.md`). Flip: none — the
  premise is false, not unverified.
- **Reject — `pbt-generator-craft-author.md`.** Decisive reason (QUALITY 2/3): it calls its source "not toy examples"
  where S170's abstract says "via a toy example in C", cites an `S116` that resolves to no tameshi row, and asserts a
  generator library is interchangeable against held tier-A S019/S020 (`T49ScribePkgCraftAuthor.md`). Flip: a corrected
  premise, a resolvable anchor and a reason to exist beside the pilot entry.
- **Deferred — `pbt-generator-as-fixture.md`.** The triage seat would admit it narrowly with nine edits and two more rows
  (JOSS Hypothesis, a Zenn case report), both re-opened 2026-10-26 (`T49ScribePkgAsFixture.md`). Not adopted this round:
  the round's claim does not rest on it, and admitting it means two more registry rows and their Gate. Flip: a round that
  opens and appends those two rows and lands the nine edits.

## C1 — what the reading found

Ninety pointers in the seven sections at base (`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`), read by
eighteen seats (`.ufo/waves/round-49/w1/T49Read01`-`18`): 80 hold, 2 stale, 5 unresolved, 3 absent by design. Seven
section critics audited every non-pointer statement (`T49Sec*.findings.json`): 12 false, 6 unverifiable. Three executors
re-ran the round-12/13/14 recipes in scratch clones (`T49ExecR1{2,3,4}Cmd.md`): every exit reproduces; the decision-table
wording drifted from the tools' printed ids in two places.

Forty-five corrections landed (`.ufo/evidence/round-49/c1/corrections.json`, each with its seat and reason; all
line-neutral, so no SKILL.md line pointer moved): 12 false statements, 6 unverifiable ones narrowed, 2 stale and 1
off-by-one pointer re-aimed (`mutation-case-kagi-census.md:251-253` → `:252-254`, line 251 is blank;
`T49ScoutRecipeLines.md`), 2 bare map pointers and 3 bare file names qualified, 2 placeholder paths explained, 9 whitespace
repairs, and 8 precision edits. Not applied: two true-but-stale sentences outside the seven sections (SKILL.md:1509, 1555),
because editing them would lapse a credited section; routed below. The re-key reads every cited record file (LOG.md,
SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md) through a git blob, so the seven entries' inputs are
cited notes and tools only (`.ufo/evidence/round-49/c1/refresh.py`); the revenger's lapse archaeology
(`T49RevengerLapse.md`) is why: 88 of 94 earlier entries carried a record file and lapsed within a median of one round,
while the six record-free entries survived 17-20 rounds.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| 1 | landing (evidence order): round 48's pre-registered control order was kept only in prose; CTL_B-CTL_E were scored eight seconds after the C1 deciding run ended, and partial counter invocations at the deciding revision were not named in the report | `.ufo/evidence/round-48/contract.json` `freeze_plan` step 2; `.ufo/evidence/round-48/after/c1-a3.start`/`.end` (15:34:20Z-16:20:54Z) vs `.ufo/evidence/round-48/control/c1-controls-a3.start`/`.end` (16:21:02Z-19:35:25Z); `corpus/lessons/round-48-verifier-spotcheck.md` defects 2-3 | none (QUALITY 69 and 88 do not reach a claim counter's control order) | `.ufo/evidence/round-49/deciding-run.sh` gate 0: it refuses (exit 3, no counter started) when a control receipt is absent at REV, when its last commit does not descend from the freeze, or when a start receipt already exists; QUALITY criterion 99. Shown able to fail: `.ufo/waves/round-49/w1/T49ExecMistakeGate.md` (three refusals, exit 3, empty receipt dirs) and `T49ScribeMistake.gate0-{a,c}.stdout` |
| 2 | scope: round 48's C2 record edits lapsed three cold-read sections, first seen at the deciding run | `.ufo/evidence/round-48/quality/coldread-precheck-red-c7586b9.stdout` | QUALITY 98 (precheck before freezing) | this round: the three sections are restored by C1, and their new entries read record files through git blobs so a record append cannot lapse them again (C1 durability predicate); the precheck runs on the candidate (`.ufo/waves/round-49/w2/T49W2ExecPrecheck.*`) and in the deciding run |
| 3 | reference drift: SCORECARD's round-48 standing section said every evidence cell was the `--emit` output "pasted byte-exact"; 19 capability rows were, the 3 axis rows carried lane prose before the emitted clause | `SCORECARD.md:2326`; `.ufo/evidence/round-48/calibration/emit-15b1521.stdout:115-117` | none | appended correction in SCORECARD.md (`### Round 48 — correction (appended in round 49)`); the checker `T49ScribeMistake.emit-verbatim.stdout` reads `ok=19 mismatch=3` on round 48's bytes |

Found this round (wave-1 attacks), routed, not claimed as fixed:

- The C2 counter cannot tell a property-based generator from a differential one: during each mutant run the generator's
  working directory holds the pristine guard, and a generator that diffs the mutant against it is "confirmed" without an
  oracle (`.ufo/waves/round-49/w1/T49CritC2Contract.md` F1-F2, probe receipts beside it). The counter is frozen and stays
  unchanged; the round's generator is checked for this outside the counter (wave-2 access trace and oracle mutation).
  Class floors count dump lines, not distinct cases (F3; the round's dump has 393 distinct cases of 400).
- The C1 counter's selftest never calls `measure()`, so the pins, the durability probe, the floors and the total are not
  exercised by it (`T49MutC1Counter.md`: 14 of 28 mutants survive); the deciding line prints every term, so the total is
  re-derivable from the receipt.
- `deciding-run.sh` runs working-tree code (`T49RevDeciding.md` F1) — the deciding run is taken only on a clean tree at
  REV, and the panel sha is checked before the run (F2).
- One ledger entry records a digest that never matched its input (`.ufo/evidence/round-21/coldread/ledger.json:24170`,
  `.ufo/evidence/round-14/context-missing-env.json`; `T49RevengerLapse.md`); it credits nothing and is left as written.
- `tools/staged-id-guard.py`'s module docstring names exit 1 only for an inadmissible map; analysis mode also exits 1 when
  `refused` (unmapped or cascade) — confirmed (`T49RevGuardExit.md`). The guard is a pinned capability and is not edited.

## considerthese

`considerthese/2026-10-26.md` (operator reflection, 2026-10-26), proposal 3, "Recurring-defect tracker for closures",
grounded through the lane's own closure records (`.ufo/waves/round-49/w1/T49ScribeConsider.md`): rounds 40-48's nine
non-author spot-checks carry 44 status-neutral defects in 26 classes; 10 classes recur in a later round and carry 24 of the
44 rows. Four classes recurred after a QUALITY criterion had been written for them (pointer-unresolvable under 72, 81 and
97; record-drift after 35; monitor-false-red after 88; standing-row-unreproducible after 92), and the operator's own
example — selftest tallies cited but not committed (round 45, fixed in 46, back in 47) — recurred with no criterion behind
it (`.ufo/evidence/round-47/` at `03facb22` has no `selftest/` directory). The two criteria written as measured rules
(87, 91) show no recurrence. Lesson: a routed defect is not a closed defect; a class that returns needs a check that can
fail, not another note. This round commits its counters' selftest receipts (`.ufo/evidence/round-49/control/c{1,2}-selftest.{stdout,exit}`)
before any wave; a recurrence criterion is left for a round that can give it a falsifier over all nine spot-checks.
