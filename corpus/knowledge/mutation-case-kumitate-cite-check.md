source: S088 — kumitate `scripts/cite-check.mjs` @ 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a (blob sha256 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f, 2537 lines, mode 100755), read-only, opened 2026-10-22; S089 — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ — page body after the `10 ** 0` example, fetched 2026-10-22; S052 (Stryker supported mutators, round 16, unchanged); procedure: `corpus/knowledge/mutation-case-kumitate-round-gate.md` (case 7) and `corpus/knowledge/mutation-case-kumitate-sources-check.md` (case 8)
verified-at: 2026-10-22; pre-registration `622d31d90b1fbc55c56e91a2b012bc18d6f1421a` (10:01:47Z), sweep 10:02:07Z, regression replay at the landed runner `a08e85c5d7f899e8a5992e20517edb1a380d79eb`; receipts under `.ufo/evidence/round-26/cite-check/`; survivor probes `.ufo/waves/round-26/w1/Probe*.md`, equivalence argument `.ufo/waves/round-26/w1/CriticEquivalence.md`
recheck: `git -C kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum` → `40573448…c10c9f`; `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-cite-check: PASS` and `REGRESSION: PASS (cases=9 passed=9 …)`; reopen S088 and S089
ground: Core — the ninth recorded mutation case on a kumitate `scripts/*` gate (PROVINCE recorded legs). No `corpus/README.md` frontier row moves; F3 (repeated controls) stays open: one control per sweep.

# Mutation case 9 — kumitate `scripts/cite-check.mjs` (round 26)

The ninth recorded case and the fourth kumitate gate in the ledger. Like cases
7 and 8, the target is a kumitate `scripts/*` primary surface
(`PROVINCE.md:7-11`). Kumitate's tree stayed read-only: the target is a byte
copy materialized from its git object store, and no opt-in was needed.
Kumitate owns the gate; tameshi owns the method and this measurement only. This
is not a service run.

## 0. Pin and suite

- Target: rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` (the file's
  last-modifying commit; the blob is unchanged at kumitate master), blob sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 126,735
  bytes, 2,537 lines, mode 100755 (S088).
- Suite: the hermetic `env -i` form of cases 7 and 8,
  `node "$MUTANT" --selftest`, with a private `HOME` and `TMPDIR` per defect.
  `--selftest` runs the gate's hermetic group only: 62 cases, control
  `62/62 cases passed (hermetic)`, `VERDICT: PASS`, exit 0
  (`sweep/evidence/control.out`). The gate's header says the hermetic group
  "Never reads --src or --self; MUST PASS in any repo state" (S088 `:75-76`).
- The gate's integration group (9 `checkI(` cases, run only by
  `--integrations`) did not run. Every number here is hermetic-scoped.
- One pristine control per sweep, GREEN, `MUTATE_RESTORE: OK`. No repeated
  controls, so byte-determinism is not established here; verdicts use exit
  status only.

## 1. Pre-registration

Ten defects and their predictions were committed in `622d31d` at 10:01:47Z
before any mutant ran; the sweep is stamped `MUTATE_DATE: 2026-10-22T10:02:07Z`.
The sweep's `spec.copy` is byte-identical to the committed spec, and the spec
and predictions are unchanged at `a08e85c`
(`.ufo/waves/round-26/w1/ReviewPreregTiming.md`). Each `@old` occurs once in
the pinned bytes. Composition: 5 kill-aimed (K_*) and 5 hole-aimed (S_*). The
ten edits were chosen by hand from the suite's predicates, not by a mutation
operator catalogue.

## 2. Result — 5/10 killed (50 %), 10/10 verdict predictions held

| id | edit (pinned line) | predicted | measured | cases passed | killing case (evidence/*.out) |
|---|---|---|---|---|---|
| K_UNRESOLVED_SEV | `UNRESOLVED: 'error'` → `'warn'` in SEVERITY (:221) | KILLED | KILLED | 55/62 | `bogus-path → UNRESOLVED error`, plus six more cases that assert UNRESOLVED severity |
| K_PIN_KIND | sha256-marked pins classified as `rev` (:1127) | KILLED | KILLED | 61/62 | `content pin match → OK; mismatch → PIN_MISMATCH` — `match=yes mismatch=no` |
| K_FENCE_TILDE | `~{3,}` → `~{4,}` in the fence-line regex (:471) | KILLED | KILLED | 60/62 | `fence content is never tokenized (by design, kept)` and `R16 regression: fence content is never tokenized under line-local pairing` |
| K_MISSING_WORD | fail-closed stderr `missing` → `absent` (:2519) | KILLED | KILLED | 61/62 | `bare run (no --src): both candidates absent keeps the --src fail-closed arm (exit 2)` |
| K_EMPTY_VERDICT | verdict drops both guards (:1590) | KILLED | KILLED | 61/62 | `fail-closed: empty scan set → exit-2 condition` — `filesScanned=0 verdict=PASS` |
| S_OOR_EDGE | line-range check `> n` → `> n + 1` (:1312) | SURVIVED | SURVIVED | 62/62 | none |
| S_STRICT | strict promotes warnings only when there are two or more (:1589) | SURVIVED | SURVIVED | 62/62 | none |
| S_EMPTY_GUARD | verdict drops only the `filesScanned` guard (:1590) | SURVIVED | SURVIVED | 62/62 | none |
| S_USAGE | usage exit `64` → `65` (:2512) | SURVIVED | SURVIVED | 62/62 | none |
| S_PIN_INCLUDES | content pin `startsWith` → `includes` (:1195) | SURVIVED | SURVIVED | 62/62 | none |

Recorded table: `TABLE_CITECHECK` in `tools/mutate-and-run.sh`. The landed
runner replays the leg from its embedded spec and reproduces the table exactly
(`REGRESSION_TABLE js-cite-check: match=10/10`,
`.ufo/evidence/round-26/cite-check/regression-worktree.stdout`).
`tools/mte-interop.py` reads the leg as official score 50, killed 5, survived 5,
per-mutant equal to the table
(`.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`).

## 3. Prediction versus killing case

A verdict prediction and the case named as its witness are separate readings.
Verdicts: 10/10. Named witness: 4/5 kills.

- **K_FENCE_TILDE — verdict held, witness wrong.** The named case
  (`~~~ fence gives the same result as ``` (marker-symmetric)`) passed under the
  mutant: it asserts equality between the backtick and tilde fixtures, and the
  mutant makes both sides report the same `UNRESOLVED/error@line7`. The mutant
  died on the two cases that assert fence content is never tokenized
  (`insideFence=1`, `fenceSpans=1`). **Error pattern:** an equality assert
  between two fixtures cannot see a one-sided regression that makes the two
  sides agree; only an absolute assert on one side does.
- **K_PIN_KIND — witness right, reason half wrong.** The matching pin still came
  back OK, because the rev branch has its own content-hash fallback
  (`cite-check.mjs:1219`); only the mismatch half turned into REV_UNKNOWN.
- **K_UNRESOLVED_SEV — wider than predicted.** Seven cases failed, not one.

## 4. Survivors — four suite holes, one equivalent mutant

| survivor | off-suite witness | status | what the suite does not pin |
|---|---|---|---|
| S_OOR_EDGE | citing `scripts/real.mjs:21` of a 20-line file: pristine `LINE_OOR`, exit 1; mutant clean, exit 0 (`ProbeSOOREDGE.md`) | hole | the LINE_OOR edge at exactly n+1 |
| S_STRICT | `--strict` over a tree with exactly one warning: pristine DRIFT, mutant CLEAN (`ProbeSSTRICT.md`; `CriticEquivalence.md`) | hole | strict promotion; no hermetic case passes `--strict` |
| S_USAGE | an unknown flag: pristine exit 64, mutant exit 65 (`ProbeSUSAGE.md`) | hole | the usage exit code |
| S_PIN_INCLUDES | a sha256 pin that is an interior slice of the file digest: pristine PIN_MISMATCH, exit 1; mutant OK, exit 0 (`ProbeSPININCLUDES.md`) | hole | prefix versus substring direction of the content-pin compare |
| S_EMPTY_GUARD | none exists: an unreadable document `continue`s before either counter moves (`:1555`), and `filesScanned++` (`:1556`) always runs before `resolved++` (`:1583`), so `resolved > 0` implies `filesScanned > 0`; 316/316 differential runs identical (`CriticEquivalence.md`) | **equivalent** | nothing — the dropped guard is redundant code |

**Decision for equivalent mutants (S089).** Stryker states "There is no
definitive way for Stryker to find and ignore them" and "There is currently
also no way yet to mark them to be ignored" (S089). So the recorded table and
the 5/10 stay as pre-registered: an equivalent mutant stays a survivor in the
score. The entry, not the table, records which survivors are holes. Two
consequences:

- Holes in this suite: 4, not 5. The hole-aimed prediction for S_EMPTY_GUARD
  could not have failed, so only 9 of the 10 verdict predictions were at risk.
- Excluding the equivalent mutant the kill rate would read 5/9; this is a side
  reading, never the ledger value.

A hole found next to the equivalent one: dropping only the `resolved` guard
(not in this spec) survives all 62 cases and is not equivalent — on a scanned
document with zero citations the `VERDICT:` line flips from FAIL to PASS while
the exit stays 2 (`CriticEquivalence.md`). It belongs in a later spec.

## 5. Limits

- One revision, one host (node v24.21.0, Linux), one control per sweep. The
  50 % is a property of this hermetic suite at this pin, not of kumitate's
  gates in general, and its composition is 5/5 by design, like cases 7 and 8.
- The integration group did not run, so the rate is for the hermetic group
  only.
- The oracle is the exit status. A mutant that keeps exit 0 while changing a
  finding's text is a survivor by this measurement.
- Suite sensitivity is not gate truth: nothing here measures whether
  cite-check's verdicts about real citations are right.
- The standing ledger `fleet-kill-rate-ledger.md` still lists cite-check as a
  four-defect probe (1/4) and a queue row; this case is that full sweep. The
  ledger file is not edited this round; `corpus/README.md` round 26 records the
  supersession.
- Recommendations travel to kumitate in the round report; tameshi never edits
  the gate.
