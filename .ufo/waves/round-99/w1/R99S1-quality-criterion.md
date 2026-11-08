# QUALITY criterion 178 — draft by seat R99S1 (scribe), round 99 wave w1

> Draft for the L1's integration. Next free number is **178** (the highest criterion
> currently in `corpus/QUALITY.md` is 177; `grep -c '^178\.' corpus/QUALITY.md` prints 0).
> Appended under a new `## Criteria appended — round 99` heading, or as the next
> numbered item after 177 under the existing section, per the L1's call. The criterion
> follows the format of the last three criteria (175, 176, 177): one numbered rule, the
> failure it captures, and an "Able to fail:" block naming commands, observed output and
> exit codes, with a source list in parentheses.

---

178. A record line that states a selftest tally **cites a receipt that
    `tools/tally-reconcile.py` can resolve**, and the citation resolves to exactly one
    receipt blob at the revision the record names. A tally with no citation on its line
    is counted, never graded; a citation that resolves to no path, or to more than one,
    is `unbound` and makes the reconciler exit nonzero — neither is a silent pass. A
    recorded tally whose cited receipt prints a different n/m is a **mismatch the round
    must route**, not a formatting detail: the record's operative value is the receipt's,
    and the correction is an append-only erratum (criterion 169), never an edit of the
    frozen line. The check that can fail is the reconciler itself, run over the round's
    records at the records revision: `python3 -I tools/tally-reconcile.py --repo . --rev
    RECORDS_REV --record corpus/lessons/round-93.md --record plans/round-93.plan.md
    --record corpus/lessons/round-94.md --record plans/round-94.plan.md --record
    corpus/lessons/round-95.md --record plans/round-95.plan.md --record
    corpus/lessons/round-96.md --record plans/round-96.plan.md --record
    corpus/lessons/round-97.md --record plans/round-97.plan.md --record
    corpus/lessons/round-98.md --record plans/round-98.plan.md` must print
    `TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6
    uncited=19` and exit 1, naming exactly one `TALLY mismatched` line —
    `corpus/lessons/round-94.md:66 token DISPOSITION_SELFTEST claimed=8/8
    receipt=.ufo/evidence/round-94/pre-freeze/c2-selftest.out observed=9/9` — and
    `--selftest` must print `TALLY_RECONCILE_SELFTEST: 17/17 pass` and exit 0. The
    receipt pointer is able to fail: the round-94 lesson line reads
    `DISPOSITION_SELFTEST: 8/8 pass` while the receipt it cites prints
    `DISPOSITION_SELFTEST: 9/9 pass`
    (`.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10`), so the same command run
    over that one record prints `TALLY_RECONCILE records=1 tallies=1 pairs=1 matched=0
    mismatched=1 unbound=0 uncited=0` and exits 1 — the mismatch is named by the
    command, not left to a reader
    (`.ufo/evidence/round-99/pre-freeze/c1-population.out`,
    `c1-r94-only.out`, `c1-selftest.out`). The rule covers the lane's own records
    only; a fleet-repo sentence is outside it, because the reconciler reads one
    repository. (`lessons/round-99.md`; round-94 closure routed defect 1; round-98
    spot-check D2; S324, S325; `tools/tally-reconcile.py` at `46651051`.)

---

## Notes for the L1 (not part of the criterion text)

- **Next number.** `177` is the highest criterion in `corpus/QUALITY.md`; `178` is free.
  The file's section headings stop at `## Criteria appended — round 95` (line 2686);
  rounds 96–98 appended bare numbered criteria under it (round 98's `177` was appended
  at the end of the file with no new heading — `git show 3b7ae127 -- corpus/QUALITY.md`).
  This draft therefore does not presume a heading; the L1 chooses.
- **Relationship to criterion 169.** 169 requires the *remedy* (an append-only erratum
  naming the superseded sentence). This criterion requires the *detection and the
  pointer*: a recorded tally cites a resolvable receipt, the reconciler grades it, and a
  disagreement is a routed mismatch. The two are complementary, not competing; 178 names
  169 rather than restating it.
- **Relationship to criterion 175.** 175 requires a record's verdict to be re-derived from
  committed bytes by a committed reader. 178 names the reader for the specific case of a
  self-assessment tally.
- **The wording stays inside what the instrument enforces.** The criterion asserts that
  the command prints the stated line and exits 1, and that the receipt pointer is able to
  fail — both verified against the frozen instrument bytes
  (`60d59bead569157fb888dbb68301e290522e5837a482e84f36f858d2566bf40c` at `46651051`).
  It does not assert that every unbound pair is a record error, which the frozen wording
  explicitly declines (`plans/round-99.plan.md` C1 declared limits; `claims.json` C1
  `limits`).
- **The instrument is being amended in the worktree.** During wave w1 the L1 amended
  `tools/tally-reconcile.py` in place (worktree sha256
  `c78e0c630aeda375dae0e6a3c9c9a75ec90356756ed2238f2526562a77f70f56`, `--selftest`
  prints `24/24 pass` instead of the frozen `17/17`). The criterion's figures are the
  **frozen** ones, measured against the committed bytes at `46651051` extracted with
  `git show` (`R99S1-c1-population.txt`, `R99S1-c1-selftest.txt`). If the amended
  instrument lands, the selftest tally in this criterion must be re-derived from the
  amended tool's own receipt and this criterion re-checked — the criterion is written
  against the freeze, as the round's own record requires.
- **Receipt pointers used.** `.ufo/evidence/round-99/pre-freeze/c1-population.out`,
  `c1-r94-only.out`, `c1-selftest.out` (committed at the freeze `ab598d03`), and
  `.ufo/evidence/round-94/pre-freeze/c2-selftest.out:10`. The seat's own re-derivations
  of the same figures, run against the committed instrument bytes rather than the
  worktree copy, are at `.ufo/waves/round-99/w1/R99S1-c1-population.txt`,
  `R99S1-c1-population-freeze.txt`, `R99S1-c1-r94-only.txt`, `R99S1-c1-selftest.txt`.
