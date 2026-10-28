# tameshi round 55 — lesson (hyaku run 11, 2026-10-28)

Base `0a2010ac`; counter freeze `631cd645` + amendments 1-4 (all in `freeze.json`,
all before any control score or deciding invocation); content commit C0 (this
commit's parent chain); deciding receipts under `.ufo/evidence/round-55/after/`.

## Gate (sources opened this round)

| S | URL | opened | quote (<=25 words, located) | verdict |
|---|---|---|---|---|
| S280 | https://www.gnu.org/prep/standards/html_node/Errors.html | 2026-10-28 | §4.4 "Formatting Error Messages": "Error messages from other noninteractive programs should look like this: program:sourcefile:lineno: message" ... "program: message" (17 words; the page's next paragraph adds the lower-case/no-period rule) | **admit, mined** — `corpus/knowledge/scratch-root-contract.md` cites it for the "one program-prefixed line" shape; it is a normative standard (tier A) and it says nothing about the exit code, so the round's exit-2 class is a lane declaration, quoted as such |
| (no row) | https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | 2026-10-28 | §DESCRIPTION: "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." (15 words) | **reject before append** — the document is already held as **S090**, so a new row would be a within-scope duplicate URL (CORPUS.md rule 2, census W04); and it cannot ground a lane rule to *adopt* sysexits codes: it deprecates its own interface and its BUGS section warns "The choice of an appropriate exit value is often ambiguous". Flip: a lane rule that actually adopts an EX_* code and records the deprecation as an accepted trade |

Snapshot/extraction receipts: `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`
(sha256 `edcaf94b…`), `S281-sysexits.txt` (sha256 `0bf02057…`, kept as the
rejection's evidence). Census at round end: exit 0, 140 rows (`grep -cE '^ {0,3}\| S[0-9]{3,} \|'` on the committed registry).

## Mistakes

- **class: a control scored at a revision that predates the work it certifies.**
  evidence: round 54's phase-B positive control (`CTL_POS_c1`) cloned the
  FREEZE commit `077d431e`, which predates the re-key `7fa9a5e`, so it printed
  `CTL_MISMATCH CTL_POS_c1 expected=true actual=false` / `CONTROLS_B: 2/3`
  (`.ufo/evidence/round-54/control/controls-b.stdout`), while four lane records —
  including a QUALITY criterion written in the same round — asserted it passed
  (`corpus/lessons/round-54-verifier-spotcheck.md`, R54.1). captured-by: none —
  the phase-B harness had no arm requiring that its clone match the revision it
  scores, so a control that could not fire looked like a pass that did.
  fix: round 55's `controls.sh` phase B clones the revision it certifies and its
  `deciding-run.sh` gate refuses any control receipt not descending from the
  freeze; QUALITY 106 states the rule and its falsifier is that same receipt.
  The counter for this class is C1's `R54.1` row, which now requires the receipt's
  `CTL_MISMATCH`/`2/3` to appear in the corrections section.

- **class: a predicate that counted a document as stating a rule when a line
  break had split it.** evidence: this round's own C2 arm 7 matched the grammar
  marker against raw `SKILL.md` text, so a marker wrapped at 78 columns read as
  absent (`skill=0/1` on a correct edit); the note arm had the same shape for
  the `bash-witness-study selftest` label, which the counter itself spelled
  `--selftest`. captured-by: the freeze-time dry run on an edited clone (no
  prior round had a dry run *before* the controls). fix: amendments 2 and 3
  normalize whitespace before matching and label the mode as invoked — the
  predicate is unchanged ("the document states the grammar and names every
  allocating mode"), only the comparison is honest about typography.

## Round-54 routed defects — dispositions (this round)

All ten are FIXED in `SCORECARD.md` `## Round 55 - round-54 record corrections`
(old value quoted there, corrected value in place, receipt named) and re-derived
by the frozen C1 counter. `T55W1*` seat reports under `.ufo/waves/round-55/w1/`
re-derived each value independently.

| id | disposition | evidence |
|---|---|---|
| R54.1 | FIXED — the positive-control claim is corrected to the receipt's `CTL_MISMATCH` / `2/3`, and round 55 re-scores its own control at the revision it certifies | `SCORECARD.md` ER-R54-1; `.ufo/evidence/round-54/control/controls-b.stdout`; QUALITY 106 |
| R54.2 | FIXED — one freeze pointer (`077d431e`) for round 54; the two stale ids moved into the corrections section | `.ufo/evidence/round-54/after/frozen.stdout` |
| R54.3 | FIXED — `total=13`, the receipt's value | `.ufo/evidence/round-54/before/c2.stdout` |
| R54.4 | FIXED — the deciding c2 digest is `8528ee85` | `.ufo/evidence/round-54/freeze.json` |
| R54.5 | FIXED — `w1=28 w2=25 sections=12`, re-derived from the committed reader files | `.ufo/waves/round-54/w1|w2/*Read*.json` |
| R54.6 | FIXED — the three swept deliverables are committed at `ff2a821` | `.ufo/waves/round-54/w2/T54W2Sent03*` |
| R54.7 | FIXED — "renamed into the receipts dir" at `7fa9a5e` | `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` |
| R54.8 | FIXED, with a withdrawal — the seat file is marked superseded and the incident is recorded here; the report's word *fabricated* is withdrawn too: the operator turn exists in `~/.omp/agent/history.db` (row 690) and reached the seat after it yielded, so the write was wrong because `config.yml` is operator-owned and the seat had stopped serving | `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`; `T55W1ScribeSeat-receipts/` |
| R54.9 | FIXED — `reviewers=5 attack=21/76 seats=76` and `staged=81` | `.ufo/waves/round-54/w1-registry.json`; the package count |
| R54.10 | FIXED — `controls-a.stdout` prints `rekeyed=0/7`; `0/30` belongs to `r53-counter-at-88afa941.stdout` | `.ufo/evidence/round-54/control/` |

Also corrected in place: `corpus/QUALITY.md` 105's falsifier (its own receipt
refutes the claim it was written to support) carries an erratum rather than a
deletion; criterion 106 is appended.

## What the counters cannot see

- C1: whether a correction's prose is fair to the reader the defect harmed, and
  whether the receipt a row names is the only receipt that could carry the fact.
  Ten wave reviewers re-derived the values; their disagreements are adjudicated
  in the round report.
- C1, demonstrated by wave-1 seats (receipts under `.ufo/waves/round-55/w1/`):
  a *paraphrased* false claim scores `total=0` (`CTL_POS_c1: true`, no backticks,
  no exact token match); an unrelated wrong assertion planted INSIDE the
  corrections section is exempt by construction; and a stale assertion in a file
  outside the record set is invisible. The round answered the third by adding
  `LOG.md` and a whitespace-collapsed span scan (amendments 5), and the first two
  are named here rather than fixed — the predicate is "no stale assertion outside
  the corrections section", not "no false sentence anywhere".
- C2: whether a documented mode outside `tools/registry.json` and the tools'
  usage text allocates scratch (a wave item inventories the difference), and
  whether a caller parses the grammar by prefix or by the whole line. The lazy
  arm also cannot distinguish "allocates nothing" from "allocates only after its
  preconditions fail" — the wave's probes push two lazy modes with failing inputs.
- Neither counter sees the deciding gate's own blind spots: `deciding-run.sh`
  checks each control receipt's existence, blob-ness, size and commit order, but
  never compares the `rev=` a `CTL` line names with the revision under test (wave
  seat T55W1ScribeLesson). Recorded as a residual, not fixed: the gate is frozen.
