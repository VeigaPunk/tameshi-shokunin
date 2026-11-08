# Round 99 — tally-receipt reconciliation (C1, calibration) and recorder-alias sites (C2, coverage)

Lane `tameshi`, L1 TameshiR99, attempt 1. Base `ff93fa16a1f65e66385b7c7f564f03b218d91ea2`;
instruments `466510515d02759427158a9b16e9daa889d44907`; freeze
`ab598d03da34bbaffc35010b4e0f7c33ed0a18ae`; wave spec `27a5e49e`; records revision R
`808a43778701cf1b05762584954d435481dc6fa2` (`.ufo/waves/round-99/records-rev.txt`). Plan
`plans/round-99.plan.md` (amendments A1-A11); claims `.ufo/waves/round-99/claims.json`.

## Gate

Sources opened this round, all fetched live by the L1 on 2026-11-08; snapshots under
`.ufo/evidence/round-99/sources/`. Word counts are `len(quote.split())`. The scout seat R99SC1
re-fetched S324/S325/S326 independently (`.ufo/waves/round-99/w1/R99SC1-*.txt`).

- **S324 (new, tier A, admit)** — Nuijten et al. 2016, Europe PMC REST record
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.3758/s13428-015-0664-2&resultType=core&format=json`,
  accessed 2026-11-08 (HTTP date `Sun, 08 Nov 2026 22:55:22 GMT`; 6409 B; `s324.json` sha256
  `346dcf46d3e6ccfe20d269b5b74ca4d21df98c8731c57858808d4c856d0f0349`), field `abstractText`:
  "half of all published psychology papers that use NHST contained at least one p-value that was
  inconsistent with its test statistic and degrees of freedom" (25 words). Grounds C1: a reported
  figure drifts from the computation it came from often enough that recomputing it pays. The
  publisher landing page (`link.springer.com/article/10.3758/s13428-015-0664-2`) first returned a
  3038 B JavaScript "Client Challenge" page to curl; a second fetch with redirects followed served
  the article (467714 B). The Europe PMC record is the row's anchor because it is a stable JSON
  field; no row was written for the landing page (same work).
- **S325 (new, tier A, admit)** — statcheck web FAQ `http://statcheck.io/`, accessed 2026-11-08
  (HTTP date `Sun, 08 Nov 2026 22:55:32 GMT`; 27778 B; `s325.html` sha256
  `477e0088c987eabd845a81bd38e716959296c2a691b0ae57d9df45e66cb3e9a7`), lane renderer
  (`.ufo/waves/round-93/w1/R93S1-tagstrip.py`) lines 135-137: "statcheck is a "spellchecker" for
  statistics. It checks whether your p -values match their accompanying test statistic and
  degrees of freedom." (21 words), and line 163: "Statcheck usually can't find statistics in
  tables." (7 words). Grounds C1's declared grammar limits: silence outside the grammar is not
  agreement.
- **S326 (new, tier A, REJECT)** — Brown & Heathers 2016, "The GRIM Test", Crossref record
  `https://api.crossref.org/works/10.1177/1948550616673876`, accessed 2026-11-08 (HTTP date
  `Sun, 08 Nov 2026 23:03:48 GMT`; 4679 B; `s326.json` sha256
  `4bfd47c2baad3e68d2765f58909b53993287dd1ef07fdbe4baa6353a772b7b0c`), field `abstract`: "This
  technique evaluates whether the reported means of integer data such as Likert-type scales are
  consistent with the given sample size and number of items." (25 words). Rejected: a
  feasibility test on a reported statistic with no binding to the artifact that produced it; the
  lane's tallies are integer counts copied from receipts. Flip: a lane record that reports
  averaged or derived figures (means of integer scores) without their raw counts. (A first
  Europe PMC query for this DOI returned zero results, 191 B — the Crossref record is the
  anchor.)

Registry changes (old → new): three rows appended (S324 `mined`, S325 `mined`, S326
`rejected`); no existing row touched. `used-by` of S324/S325:
`corpus/knowledge/tally-receipt-reconciliation.md, corpus/lessons/round-99.md`; S326:
`corpus/lessons/round-99.md`. Recheck: S324/S325 `365d`, S326 `180d`.

Assimilation: none (no `merge/tameshi/` package adopted this round). considerthese:
`considerthese/2026-11-08.md` idea 1 ("Frozen-tally reconciler", proposals only, not acted on)
is mined as C1; the pointer was grounded by re-reading the two cited closures
(`corpus/lessons/round-94-verifier-spotcheck.md:102`, round-98 spot-check D2).

Census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → exit 0, 183 rows (`.ufo/waves/round-99/census-before.txt`).
Census after: exit 0, 186 rows (`.ufo/waves/round-99/census-after.txt`).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **a selftest arm bound to its fixture by list position** (mined from round 98): the round-98 audit's `loop-site-count` arm reads `SELFTEST_CASES[7]`; the records commit `3b7ae127` inserted five cases before `loop-site`, so from then on the arm audits `augassign` (no loop) and passes while exercising nothing about loops — kill rule (d) went unexercised at the round-98 records revision. At `6b1428c8`/`764aca97`/`d32043ec` index 7 was `loop-site` (index drift, A7). | `w1/R99RV1.md`, `R99RV1-c2-loop-arm-history.txt`; `w1/R99M1.md` (`R99M1-mined-log.txt`: v1 augassign fixture site count 1, arm ok) | none — R98M1's mutation matrix and the round-98 closure both missed it | v2 binds the arm by name (`CASE["loop-site"]`) and asserts the fixture contains `for `; shown able to fail: R99M1's positional mutant prints `SELFTEST loop-site-count FAIL` and `CONTROL_ASSERT_V2_SELFTEST: 26/27 pass`, rc 1 (`R99M1-mined-log.txt`). |
| M2 | **a recorded tally that its cited receipt contradicts** (mined from round 98, D2; same class as round 94): the round-98 report said the C1 selftest was `18/18` "at the freeze" citing a receipt that prints `12/12`. | spot-check D2; `w1/R99RV1.md` (`R99RV1-d2-freeze-receipt.txt`) | QUALITY 169 states the remedy, no instrument detected it | C1's `tools/tally-reconcile.py`; shown able to fail on the exact D2 line shape: `R99RV1-d2-fixture-relpaths.txt` → `TALLY mismatched … observed=12/12`, exit 1; on the round-94 lesson: `records/c1-r94-only.out` → `mismatched=1`, exit 1. Erratum below. |
| M3 | **the frozen C2 sentence was wider than the binding walker** (this round; the autopsy class): "bound … only by a plain or annotated assignment", "any other binding … counted and graded unresolved" and "partial(…)" were each defeated by spellings the walker did not see (walrus, tuple, `del`, match capture, alias of an ambiguous name, alias of a partial, `from functools import partial as p`, two-name conditional). | `w1/R99R2.md` S5-S8; `w1/R99E2.md`; `w1/R99M1.md` v10/v11 | Amendment-59 ledger (the round's own wave) | A1 repair + exact binding sentence; `records-aux/a1-a9-discrimination.out`: 9 of 11 new v2 arms fail under the frozen v2 (`DISCRIM_V2 discriminates=9 armour=2`). |
| M4 | **the frozen C1 grading sentence was wider than the regexes**: "every line of the receipt carrying the claimed token" while the grader read only lines ending `pass`; a contradicting `9/9 fail` line, a bare `9/9`, and a `\xff` inside the digits were invisible; `a.out.bak` was cited as `a.out`. | `w1/R99R1.md` F1/F3; `w1/R99SN1.md` F3 | Amendment-59 ledger | A2/A3/A9 repairs; `records-aux/a1-a9-discrimination.out`: 4 of 8 new tally arms fail under the frozen tool (`DISCRIM_TALLY discriminates=4 armour=4`). |
| M5 | **an instrument edited in the worktree while the wave re-derived it**: the L1 began the A1-A3 repairs in place during the wave; R99E2 first ran the edited worktree tool, caught the sha mismatch and re-ran from the frozen blob; R99SN1 F1 showed the pre-freeze runner names a blob digest but executes the worktree file. | `w1/R99E2.md` line 5; `w1/R99SN1.md` F1 | the seats' own sha checks | records runner executes `git show R:<tool>` bytes and writes the round-78 header triple (A11); `records-aux/receipt-bytes-bind.out` → `RECEIPT_BIND: receipts=16 bound=16 corrected=0 design=0 unbound=0`, exit 0. Next round: stage repairs in scratch until the records revision. |
| M6 | **a do-nothing taxonomy that named one do-nothing shape**: the plan said the predicate fails a reconciler that grades nothing; a 25-line verbatim-print forgery meets every frozen C1 invocation, and a name-special-cased v2 meets every frozen C2 conjunct. | `w1/R99C1.md` F1/F2 (`R99C1-forgery-f1-hardcode.py`, `R99C1-forgery-f2-record-specialcase.py`) | the critic seat | A5: out-of-set controls in the records run — `records/c1-r93-only.out` (`matched=1`, exit 0, the forgery prints the twelve-record line), `records/c2-v2-alias-driver-renamed.out` (`names=add,log_entry`, the forgery prints `sites=2`), `records/c2-v2-alias-driver-chain.out` (`aliases=2`). |

## Errata

- **Round-98 report (spot-check D2).** `.ufo/reports/round-98/tameshi.md` lines 31-32 say the C1
  selftest is "`18/18` (`pre-freeze/c1-audit-selftest.out` at the freeze; …)". The freeze
  receipt `.ufo/evidence/round-98/pre-freeze/c1-audit-selftest.out` prints
  `CONTROL_ASSERT_SELFTEST: 12/12 pass` (v1 audit, the frozen `battery_predicate`); `18/18` is
  the records receipt `.ufo/evidence/round-98/records/c1-audit-selftest.out` (A5). The
  sentence's operative values are 12/12 at the freeze and 18/18 at R.
- **Round-98 SCORECARD R94-C1 cell (spot-check D1).** Corrected append-only in SCORECARD's
  round-99 section (the round-94 text is `**verified under the amended wording**`; round 94 had
  amendments A1-A8 only).
- **This round's plan, A1 row.** It points to `records/c2-a1-discrimination.out`; the receipt
  landed as `.ufo/evidence/round-99/records-aux/a1-a9-discrimination.out` (tool-less receipts
  live in `records-aux/`, A11).

## Registry changes

S324, S325, S326 appended (see Gate); no in-place edit. Registry immutability over the round
range: `python3 -I tools/registry-cell-immutability.py --repo . --from ff93fa16… --to <landing>`
(run at landing; `records-aux/` and the report carry the line).

## Measurements

At R `808a4377` (tool bytes executed from `git show R:<tool>`; `.ufo/evidence/round-99/records/`):

```
c1-population   TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19   rc=1
                TALLY mismatched corpus/lessons/round-94.md:66 token DISPOSITION_SELFTEST claimed=8/8 receipt=.ufo/evidence/round-94/pre-freeze/c2-selftest.out observed=9/9 detail=differs
c1-r94-only     TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0   rc=1
c1-r93-only     TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=1 mismatched=0 unbound=0 uncited=0   rc=0
c1-selftest     TALLY_RECONCILE_SELFTEST: 25/25 pass   rc=0
c2-v2-alias-driver          RECORDERS aliases=1 … names=add,record;      CONTROL_ASSERT sites=4 measured=3 literal=1 unmeasured=1   rc=1
c2-v1-alias-driver          CONTROL_ASSERT sites=2 measured=2 literal=0 unmeasured=0   rc=0
c2-v2-alias-driver-renamed  RECORDERS aliases=1 … names=add,log_entry;   sites=4 measured=3 literal=1 unmeasured=1   rc=1   (v1: sites=2 rc=0)
c2-v2-alias-driver-chain    RECORDERS aliases=2 … names=add,rec2,record; sites=4 measured=3 literal=1 unmeasured=1   rc=1   (v1: sites=2 rc=0)
c2-v1/v2-controls98         CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0   rc=0 each; site+summary diff empty (records-aux/c2-site-diff-controls98.out)
c2-v1/v2-controls97         CONTROL_ASSERT sites=15 measured=14 literal=1 unmeasured=1   rc=1 each; site+summary diff empty
c2-v2-selftest  CONTROL_ASSERT_V2_SELFTEST: 38/38 pass   rc=0
c2-v1-selftest  CONTROL_ASSERT_SELFTEST: 18/18 pass   rc=0
before tokens   git grep TALLY_RECONCILE / CONTROL_ASSERT_RECORDERS at ff93fa16: rc=1 each (records-aux/)
A10             both tools without -I: rc=64 (records-aux/a10-no-isolation-c{1,2}.out)
A11             RECEIPT_BIND: receipts=16 bound=16 corrected=0 design=0 unbound=0   rc=0
```

What the C1 numbers say about the lane (R99L1, R99E1): all six unbound pairs have a confirming
receipt under the same round's dirs (four cited by basename under a sub-directory, two citing a
red/green run receipt on the same line as the selftest figure); 16 of the 19 uncited tallies have
a confirming receipt somewhere in their round's dirs; the 3 without are the superseded
`DISPOSITION_SELFTEST: 8/8` echoes (round-94 plan:165, round-95 lesson:29/37). Only 2 of 28
recorded tallies are confirmed by the instrument as written — a statement about how the lane
cites, not about wrong numbers.

## Wave

One v1 wave `w1`, 13 seats (executor 3, reviewer 2, critic 2, mutation-tester 1, sentinel 1,
connector 1, revenger 1, scout 1, scribe 1). Reports and receipts under
`.ufo/waves/round-99/w1/`. E1 re-derived C1 with an independent reconciler (zero per-pair
disagreements); E2 re-derived C2 and probed 16 alias spellings (IfExp and `del` findings → A1);
E3 re-ran the round-98 registry red/green pairs as a non-author (byte-identical; D4 closed) and
a new green pair over `3b7ae127..ab598d03`; R1 falsified C1's grading/citation sentences
(A2-A4); R2 falsified C2's binding/fixpoint/partial sentences (A1); C1 built both forgeries
(A5) and upheld both axis attributions; L1 confirmed H (the six unbound pairs are limits)
6/6; M1 ran 24 mutants (`MUTANTS tally=9/12 audit2=8/12`) and proved the mined fix able to
fail; SN1 found the provenance gap (A11), the isolation gap (A10), the non-UTF-8 digit residual
(A9) and the tree dependence; CN1 found no prior reconciler with the same-line pairing rule
(F1), the two-grammar and two-walker duplication (A8) and the `add`-rebinding asymmetry (A1
limit); RV1 timed D2 (12→18 at `3b7ae127`) and corrected the mined mistake's history (A7).
