# CtlReceiptCopy — round 31 C1 route control (receipt copy, zero command executions)

## Verdict

**The route control prints `C1_R31_PASS=true`, exit 0, with none of the twelve frozen commands
executed.** Every one of the 12 claimed values was copied from a receipt already committed in the
lane; the last missing value (the census count) is published by the freeze's own before receipt.
This is the finding case named in the assignment, and it is a property of the predicate, not a
counter defect.

Two variants were measured, one commit apart (both are the same single appended block on
`c111dab`, differing only in the census row):

| Variant | Control commit | Census value and source | Result |
|---|---|---|---|
| V1 | `aebfdc874ebcf716e10d14ef29013550017e8ae3` | 89, latest-dated `== A rows` receipt (`.ufo/evidence/round-27/after/registry-2227d83.json:385`); **out of scope at REV** — it observed `corpus/SOURCES.md` blob `6aa0dc84…`, REV is `c845c6ba…` | `mismatches=1 ... C1_R31_PASS=false`, exit 1 |
| V2 (final) | `47ee5b6276da0c4429aee546e063d1b34699cc33` | 92, the frozen counter's own observed value at base (`.ufo/evidence/round-31/before/c1-at-base.stdout:1`); **in scope at REV** — base observed the REV blob `c845c6ba…` | `mismatches=0 ... C1_R31_PASS=true`, exit 0 |

V1 is a **stale-source injection**, not a "latest receipt" reading: it authors a current-state row
from an observation taken over different `corpus/SOURCES.md` bytes. It fails only on that statement. V2 copies the value the freeze itself
committed; `corpus/SOURCES.md` did not change between the base commit `36c1d39` and `c111dab`
(its last change, `bb68156`, is an ancestor of the base), so 92 is current at `c111dab` and the row
matches.

Correction to my earlier message to the critic: my claim that "no committed receipt states 92" was
too narrow — I had enumerated only receipts containing the `== A rows` census text and had excluded
the round-31 before receipt, which records `observed=0,92` in its first `STATEMENT` line. The
critic's qualification is correct and is the pivot of this result.

## Setup and frozen inputs (unchanged)

- Counter hash verified: `sha256sum .ufo/evidence/round-31/c1-measure.py` →
  `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584`, equal to
  `contract.json` `counter_sha256`.
- Base `36c1d3933f680125aeefc447f07db0f03004901a`; the before receipt
  `.ufo/evidence/round-31/before/c1-at-base.stdout` was read, never rerun or modified. The contract
  discloses that the L1 ran each command once at base pre-freeze (`prefreeze_disclosure`).
- Sandbox clone and commit:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane
git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane checkout -q --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
# ... append receipt-derived tables to SCORECARD.md ...
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane \
  -c user.name=ctl -c user.email=ctl@sandbox commit -qam receipts
```

Final clone history: `47ee5b6 receipts` on `c111dab`. The commit touches only `SCORECARD.md`
(1 file changed, 25 insertions). No production file, lane repo, fleet repo or `jj` state was
touched; all git writes are inside the seat scratch clone.

## Route control construction

Rule applied: for each of the 12 frozen statements, take the value stated by a committed receipt in
the lane; execute none of the 12 commands. Receipt sources (all committed at `c111dab`):

| Statement | Receipt copied | Value copied |
|---|---|---|
| sources-registry | `.ufo/evidence/round-31/before/c1-at-base.stdout:1` (observed at base) | exit 0, 92 rows |
| mutation sweep runner | `.ufo/waves/round-30/wC/MutateHead.md:36-37` | 106/106, exit 0 |
| six-leg regression ledger | `.ufo/waves/round-30/wC/RegressionReplayHead.md:11` | PASS cases=9 passed=9, exit 0 |
| repeated pristine-control gate | `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:60` | PASS (29 cases), exit 0 |
| six-leg content-disposition probe | `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:55` | 19/19 PASS0 |
| exposed witness provenance correction | `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:65` | 39/39 PASS0 |
| effective expectation reconciliation | `.ufo/evidence/round-30/attempt3/evidence-disposition-selftest.txt:4-5` | 66/66, exit 0 |
| retained invocation-context gate | `.ufo/evidence/round-15/verification-3.json:162` | exit 0, 49/49 |
| hermetic env-differential probe | `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:52` | 9/9, exit 0 |
| callback-authoritative wave accounting | `.ufo/evidence/round-22/final/gate-selftest.json:14` | 8/8, exit 0 |
| depth (axis) | `.ufo/evidence/round-30/head/depth-shonen-at-65b6e84f.stdout:1` | 9 |
| calibration (axis) | `.ufo/evidence/round-30/head/c1monitor-at-4df5107f.stdout:1` | 8 |

The rows are two appended tables (one `| Capability |`, one `| Axis | Score (0–10) |`) after the
last line of `SCORECARD.md`, so the base file stays a byte prefix (`append_only=1` observed).

## Frozen counter runs (verbatim)

Command, run twice with a fresh empty `--work` each time (V1 then V2; both `--rev HEAD`):

```sh
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py \
  --lane /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane --rev HEAD \
  --work /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/w-receipts4
```

V1 stdout (commit `aebfdc8`, census 89), full:

```text
STATEMENT sources-registry: claimed=0,89 observed=0,92 (exit=0) MISMATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=aebfdc874ebcf716e10d14ef29013550017e8ae3 C1_R31_PASS=false
```

V1 process exit: **1** (wall 247.77 s).

V2 stdout (commit `47ee5b6`, census 92 from the before receipt), full:

```text
STATEMENT sources-registry: claimed=0,92 observed=0,92 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=8 (exit=0) MATCH
C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 rev=47ee5b6276da0c4429aee546e063d1b34699cc33 C1_R31_PASS=true
```

V2 process exit: **0** (wall 204.56 s). Both runs used a fresh empty `--work`; every observation
line reports `exit=0`.

Captured stdout files:
`/fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/receipts-control-final.stdout` (V1) and
`/fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/receipts-control-pass.stdout` (V2).

## Scored control diff (V2, one commit on `c111dab`)

```text
$ git -C /fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/lane diff HEAD~1 HEAD -- SCORECARD.md | head -80
diff --git a/SCORECARD.md b/SCORECARD.md
index 8c32413..74d1739 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -1478,3 +1478,28 @@ cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 tr
 depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
 verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
 selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.
+
+## Round-31 C1 route control — rows re-stated from committed receipts only
+
+Calibration control, not a lane claim. Every value below was copied from a receipt already
+committed in this lane at `c111dab58b0a8d55e991bbd2efe3aad56717b95a`; none of the twelve
+frozen C1 commands was executed to produce this block. The base `SCORECARD.md` stays a byte
+prefix of this revision because the block is appended.
+
+| Capability | What it can now do | Evidence pointer (value copied from a committed receipt, no command run) | First-working round |
+|---|---|---|---|
+| sources-registry | control re-statement from receipts only | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 92 rows; copied from `.ufo/evidence/round-31/before/c1-at-base.stdout:1` (the frozen counter's own observed value at base; `corpus/SOURCES.md` unchanged between base and `c111dab`) | control |
+| mutation sweep runner | control re-statement from receipts only | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0; copied from `.ufo/waves/round-30/wC/MutateHead.md:36` | control |
+| six-leg regression ledger | control re-statement from receipts only | `bash tools/mutate-and-run.sh --regression` → REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0), exit 0; copied from `.ufo/waves/round-30/wC/RegressionReplayHead.md:11` | control |
+| repeated pristine-control gate | control re-statement from receipts only | `python3 tools/repeat-control.py --selftest` → SELFTEST: PASS (29 cases), exit 0; copied from `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:60` | control |
+| six-leg content-disposition probe | control re-statement from receipts only | `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0; copied from `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:55` | control |
+| exposed witness provenance correction | control re-statement from receipts only | `python3 tools/witness-metadata.py --selftest`: metadata selftest39/39 PASS0; copied from `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:65` | control |
+| effective expectation reconciliation | control re-statement from receipts only | `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0; copied from `.ufo/evidence/round-30/attempt3/evidence-disposition-selftest.txt:4-5` | control |
+| retained invocation-context gate | control re-statement from receipts only | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49; copied from `.ufo/evidence/round-15/verification-3.json:162` | control |
+| hermetic env-differential probe | control re-statement from receipts only | `python3 tools/env-diff.py --selftest` first actual9/9; copied from `.ufo/waves/round-30/wC/SelftestsNoHarmHead.md:52` | control |
+| callback-authoritative wave accounting | control re-statement from receipts only | `python3 tools/wave-accounting.py --selftest` → frozen counter8/8; copied from `.ufo/evidence/round-22/final/gate-selftest.json:14` | control |
+
+| Axis | Score (0–10) | Evidence pointer (value copied from a committed receipt, no command run) | Measured commit | Last-change round |
+|---|---|---|---|---|
+| depth | 9 | `depth_score=9` in `.ufo/evidence/round-30/head/depth-shonen-at-65b6e84f.stdout:1`; no command run | `4df5107fb429376cdf80a7a277ea88eb4459451b` | control |
+| calibration | 8 | `calibration_restraint_score: 8` in `.ufo/evidence/round-30/head/c1monitor-at-4df5107f.stdout:1`; no command run | `4df5107fb429376cdf80a7a277ea88eb4459451b` | control |
```

V1's only difference from this diff is the `sources-registry` row: `exit 0, 89 rows; copied from
the latest committed == A rows receipt, .ufo/evidence/round-27/after/registry-2227d83.json:385`.

## Which values the receipts gave right and wrong

Right at `c111dab` (all 11 non-census statements, copied from round-30 or later receipts): mutation
`106/106` exit 0; regression `PASS (cases=9 passed=9)` exit 0; repeat-control `PASS (29 cases)`
exit 0; pin-disposition `19/19` exit 0; witness-metadata `39/39` exit 0; evidence-disposition
`66/66` exit 0; verify.py `exit 0, 49/49`; env-diff `9/9`; wave-accounting `8/8`; depth `9`;
calibration `8`. Their inputs are unchanged since round 30 (`tools/mutate-and-run.sh` at `bb68156`;
`repeat-control.py` `9df9212`; `pin-disposition.py` `2a22ade`; `witness-metadata.py` `4acc607`;
`evidence-disposition.py` and `env-diff.py` `370f2df`; `wave-accounting.py` `6b6a3ea`;
`.ufo/evidence/round-15/verify.py` `7650fe4`; `SHONEN.md` `370f2df`), so the receipts describe the
bytes the counter reads at `c111dab`.

Stale at REV (not wrong when written):

- `sources-registry` from the `== A rows` receipt series: 89 at rev `2227d83` (round 27) versus 92 at
  `c111dab`. Receipt counts across the lane run 44 (kaika), 76 (round 20), 79 (21), 81 (23), 83 (24),
  85 (25), 87 (26), 89 (27); `corpus/SOURCES.md` last changed at `bb68156` (round-30 content added
  S092–S094), after every one of those receipts. The receipt was true at its own revision and makes
  no claim about `c111dab`; it is the **row** built from it that would be wrong at REV. This is input
  drift, not a misread, and the census is the only statement where a round-30 receipt reader lands
  stale.
- The current value exists only because the freeze published it: `.ufo/evidence/round-31/before/c1-at-base.stdout:1`
  records `observed=0,92` at base, and no content change separates base from `c111dab`.

## What the PASS means (finding)

- A PASS from this control means the re-stated rows **agree with repo state at REV**. It does not
  mean any of the twelve commands was executed, and the counter cannot tell the difference: it
  selects the last row per frozen table type and compares tiered value tuples with observed output
  (`c1-measure.py:206-218`). There is no provenance field, timestamp check or execution marker in the
  predicate.
- Concretely, this round's freeze supplied every needed value: 11 statements from round-30 receipts,
  the census from the before receipt. Result: `C1_R31_PASS=true`, exit 0, zero executions by this
  seat. If the before receipt had not carried 92, the same method tops out at 11/12 and prints
  `C1_R31_PASS=false` (V1), failing only on the input that changed after the last `== A rows` receipt.
- The discriminating power of a receipts-only producer is therefore exactly the gap between its
  receipt and the last edit of each input — it is not a guard against copying. That is consistent
  with the contract's own labelling of this route ("the counter measures the outcome property
  itself, so this is not a skip of the claimed property"): the claimed property is row agreement,
  and the control confirms the counter measures it without asking how the row was produced.
- Calibration reading for C1: a `C1_R31_PASS=true` at the round-31 revision is evidence that the
  12 rows agree with repo state, and no evidence about command execution. The claim label should be
  read exactly that narrowly.

### The critic's objection, answered

Objection raised by `TameshiR31.CriticC1`: V1 treats a historical receipt's value as a current
calibration error, so the route control re-measures receipt age rather than the counter's
measurement. Conceded in the part that matters, with its boundary stated:

- **A receipt states what was true at its revision.** `2227d83`'s 89 was correct when written and
  makes no claim about `c111dab`. Only the SCORECARD row is a current-state assertion, because the
  frozen statement set is defined as the last row of each table type in the committed SCORECARD at
  REV. The V1 mismatch is therefore a true statement about the **row** and says nothing about the
  receipt's quality; calling the receipt "wrong" would be a category error. The report now labels
  it stale-at-REV, and V1 is not evidence that receipt-copying is unsafe.
- **More strongly, this control does not calibrate measurement at all.** Its outcome is fully
  determined by whether some committed receipt carries each current value: 12 available → PASS (V2);
  11 available → exactly one mismatch (V1). It exercises the counter's table selection, row parsing
  and append detection (12 parsed, 0 unparsed, `append_only=1`) and nothing about provenance. It is
  an availability probe for values, not a measurement-quality control.
- **What it does establish is narrow and usable:** the counter's verdict is sensitive to one stale
  value and tolerant of nothing else; and `C1_R31_PASS=true` at this revision is reachable with no
  command execution, so PASS cannot be read as execution evidence.
- **What would discriminate provenance is outside the frozen predicate:** a receipt bound to the
  command's own stdout at REV (hash or byte equality), or a counter that runs the command and
  compares it with a committed observation stamped at REV. The contract deliberately chose outcome
  equality instead and discloses that choice for this route. Any demand for execution evidence is a
  predicate change, not a counter repair.

### Authority resolved by input-blob scope

The objection's residue is a selection rule: "latest dated receipt" is not "authoritative receipt".
Authority for a current-state row is a verifiable scope test — a receipt's observation extends to
REV iff the bytes it observed are the bytes at REV. Tested directly with git blob identity:

| Input | Receipt revision → blob | REV (`c111dab`) blob | Scope |
|---|---|---|---|
| `corpus/SOURCES.md` | `2227d83` → `6aa0dc84fd844b29cf13c9c714081f2ccdfd6038` | `c845c6baa6d1321ece53bc2dd1e3ca0f801aa81a` | **out** for the round-27 census receipt |
| `corpus/SOURCES.md` | `36c1d39` (base) → `c845c6ba…` | same | **in** for the before receipt |
| `tools/mutate-and-run.sh` | `bb68156` → `2d81b929…` | same | in |
| `tools/repeat-control.py` | `9df9212` → `70c91e7e…` | same | in |
| `tools/pin-disposition.py` | `2a22ade` → `89a6ca38…` | same | in |
| `tools/witness-metadata.py` | `4acc607` → `b38bec3c…` | same | in |
| `tools/evidence-disposition.py` | `370f2df` → `123b8f1c…` | same | in |
| `tools/env-diff.py` | `370f2df` → `3a48aecc…` | same | in |
| `tools/wave-accounting.py` | `6b6a3ea` → `4245d195…` | same | in |
| `.ufo/evidence/round-15/verify.py` | `7650fe4` → `b38cbf4c…` | same | in |
| `SHONEN.md` | `370f2df` → `253f3c05…` | same | in |
| round-21 cold-read `ledger.json` | `4df5107f` → `dba8d1e2…` | same | in for the calibration receipt |

Consequences, which close the objection:

- The round-27 census receipt is not "wrong"; it is **out of scope** for a row asserting `c111dab`,
  and the counter correctly refuses the row built from it. The before receipt is **in scope** because
  the input bytes are identical from base to REV; its 92 is licensed at REV. Recency of the receipt
  file is irrelevant; blob identity decides.
- On that rule, V1 is a stale-source injection control (out-of-scope source, one localized mismatch)
  and V2 is the authoritative-source control (all sources in scope, PASS). Neither verdict is a
  statement about the repository's self-assessment being "historically wrong": the counter's verdict
  is about the row at REV, and both verdicts are the correct ones for the rows submitted.
- Scope tested here covers each statement's primary input file. Auxiliary inputs that the tools read
  themselves (pinned sibling revs for the regression, hash-pinned receipts for `verify.py`, knowledge
  files for the census B1/B2 legs) were not individually blob-tested; the counter's observed lines
  are the check on those, and every one exited 0.

## Risks and notes for the integrator

- The C1 target (0 mismatches at the round-31 revision) is reachable by copying 12 committed values;
  the wave-1 control demonstrates this end to end. No amendment is implied — the predicate is
  outcome-only by design — but producers and reviewers should not cite C1 PASS as execution proof.
- The round-31 no-harm `drift_plan` schedules an edit to `corpus/SOURCES.md` in wave 2. That will move
  the census count and stale every existing A-rows receipt **and** the before receipt's 92. After that
  edit the census row must be re-derived from the post-edit state; copying any receipt will fail as
  V1 did.
- `append_only=1` held in both measured variants; the base file remains a byte prefix.
- No tools were installed or upgraded. No processes from this seat remain (all four counter runs
  completed; work dirs `w-receipts`, `w-receipts2`, `w-receipts3`, `w-receipts4` are under this
  seat's scratch).
- Sandbox git writes (clone, commit, amend) occurred only under
  `/fast/scratch/hyaku/tameshi-r31-seats/CtlReceiptCopy/`; no `jj` command and no write to the lane
  or fleet repos.
