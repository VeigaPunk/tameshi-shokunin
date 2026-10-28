# Tameshi round 55 — ten record corrections, one scratch-root line on every mode

L1 TameshiR55, hyaku run 11, attempt 1. Base `0a2010ac`, the erratum tip the
round-54 non-author spot-check left. Claims frozen at `631cd645`
(`.ufo/evidence/round-55/contract.json`, `freeze.json`), before any seat ran.
Round shape: one v2 wave (build and attack together), then one v1 falsify wave
over what it produced. Calibration is the lowest non-retired axis (8) and
carries C1; operability carries C2. The round answers the round-54 spot-check:
ten routed record defects (R54.1-R54.10) and one class the round before measured
on the self-test path only.

## Gate

Rows opened this round (CORPUS.md SOURCES contract v1 rule 1):

- **S280** — GNU Coding Standards, §4.4 Formatting Error Messages,
  `https://www.gnu.org/prep/standards/html_node/Errors.html`, opened 2026-10-28
  (HTTP 200, 7147 B; the row's anchor is the reader extraction
  `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`, sha256
  `edcaf94b…`; two independent full-page fetches are byte-identical at
  `.ufo/waves/round-55/w1/T55W1ScribeSources-receipts/sources/gnu-errors.html`
  and `.ufo/waves/round-55/w1/T55W1ScribeLesson-receipts/sources/gnu-errors.html`,
  sha256 `54c55cd4…`). Located quote (10 words, §4.4 at byte 5020): "Error
  messages from other noninteractive programs should look like this:"; the two
  forms it gives are `program:sourcefile:lineno: message` and, where no source
  file applies, `program: message` (byte 5415).

Admits (this round's set): one row, cited by the note's new `## One line, every
mode` section (`corpus/knowledge/scratch-root-contract.md`). What the row buys is
bounded, and the note must say so: the line's *shape* — one line,
`<program>: <message>`, the message not capitalised and not ending with a
period. It does not source the exit status: the page never mentions one (the
locator prints `GNU page mentions 'exit': False`), so exit 2 and stderr are lane
declarations, not quotations. Province: verification-fixture craft (the shape of
a gate's refusal line) — in scope. QUALITY bar: the note cites the row with a
located quote, and no claim outruns it.

Held rows re-read, not opened: S277 (POSIX `TMPDIR`), S278 (CPython's resolver)
and S279 (the documented search list) stay the note's three citations. They are
round-54 rows; this round neither adds to nor re-points them.

Rejects (this round's set):

- **FreeBSD `sysexits(3)`**,
  `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3` (HTTP 200,
  59251 B, sha256 `1fc793a2…`; extraction
  `.ufo/evidence/round-55/assimilation/S281-sysexits.txt`). REFUSED before
  append: the URL is already held as **S090**, whose scope covers exit-status
  conventions, so a second row would duplicate a held source — and CORPUS.md
  rule 2 admits a new row for a held source only in the `supersedes S0NN —`
  form, which this candidate does not fit. (The census's W04 would flag the
  duplicate URL, but by design it is a warning that does not fail a lane,
  `sources-census.sh:33`.) It would not carry a lane rule either — it deprecates
  its own interface: "This interface has been deprecated and is retained only
  for compatibility. Its use is discouraged." (15 words, §DESCRIPTION at byte
  49849); its `EX_USAGE` is 64, not the lane's 2; and its BUGS section says the
  choice "is often ambiguous" (byte 53846). Flip: a lane tool adopts an `EX_*`
  code and records the deprecation as an accepted trade.

Counts: one row opened and adopted (S280), one candidate refused before append,
no row re-pointed and none retired. The registry stood at 139 rows (S001-S279)
when S280 was opened and reads 140 rows now; the census validates exit 0.
Assimilation verdict: one theme (the one-line scratch-root class) with one new
row and one refused candidate; the note carries the row.

## Mistakes

- **class: a control scored at a revision that predates the work it certifies.**
  evidence: `.ufo/evidence/round-54/control/controls-b.stdout` prints
  `CTL CTL_POS_c1 C1_R54: rev=077d431e6996 … credited=60 lost=4 rekeyed=3/7 …
  total=4 C1_R54_PASS=false`, then `CTL_MISMATCH CTL_POS_c1 expected=true
  actual=false` and `CONTROLS_B: 2/3 as pre-registered`. (That file has two
  commits, `7fa9a5e` and `5564954`; they leave every verdict line identical and
  add only a re-statement footer.) And `git merge-base --is-ancestor 077d431e
  7fa9a5e` exits 0: the revision the control cloned is an ancestor of the re-key
  commit the claim rests on (freeze 12:12:06, re-key `7fa9a5e` 12:21:35,
  deciding revision `c2108100` 12:22:15). The control fired against a tree that
  could not satisfy it: `rekeyed=3/7` is what the freeze tree measured, against
  `7/7` at the revision that decided.
  captured-by: none. The harness took the revision as an argument and neither it
  nor the deciding run compared the `rev=` printed on the control's line with
  the revision being decided; the round-54 C1 counter never reads the control
  receipts, so the record could assert the expected verdict and nothing
  contradicted it.
  fix: this round's `controls.sh` phase B clones at `REV`, the revision it
  certifies, and prints that `rev=` on the `CTL` line for a reader to check;
  QUALITY 106 states the rule. The residual is named, not papered over: the
  frozen deciding run checks that a control receipt exists, is a non-empty blob
  and descends from the freeze (`deciding-run.sh:46-52`), not that its `rev=`
  equals `REV`, so this class is closed by procedure and a readable receipt, not
  by an assertion in the gate.

## Round-54 routed defects - dispositions (this round)

Each row names the receipt its value is derived from and the entry that carries
the correction (`## Round 55 - round-54 record corrections` in `SCORECARD.md`,
`ER-R54.N`). The round's C1 counter reads every class `ok` at the content
revision (`.ufo/evidence/round-55/after/c1.stdout`).

- **R54.1** (a positive control reported as passing while its receipt says it did
  not) — FIXED: three of the four stale assertions are in the lane and are
  corrected in place — SCORECARD's C1 claim cell now prints the receipt's
  `CTL_MISMATCH` / `2/3`, `corpus/QUALITY.md` 105's falsifier says the control
  never fired, and `corpus/lessons/round-54.md`'s R53.1 line says the same — and
  ER-R54-1 carries the old -> new pair. The fourth is the fleet report, which is
  recorded and not corrected. Receipt:
  `.ufo/evidence/round-54/control/controls-b.stdout` lines 1, 2 and 5.
- **R54.2** (three freeze pointers for one round) — FIXED: one pointer,
  `077d431e` (5 amendments), in the claim row and in the measured-close line
  (ER-R54-2); `7883e0e5` and `fe70474d` no longer appear in `SCORECARD.md`
  outside the corrections section. Receipt:
  `.ufo/evidence/round-54/after/frozen.stdout` (`freeze=077d431e…`). Limit: the
  fleet report's `097985c1` lives outside the lane and is only recorded.
- **R54.3** (a quoted total no receipt contains) — FIXED: `total=13`, the value
  `.ufo/evidence/round-54/before/c2.stdout` prints (ER-R54-3).
- **R54.4** (a stale counter digest) — FIXED: `8528ee85` for `c2/measure.py`,
  the digest `.ufo/evidence/round-54/freeze.json` pins and the bytes the
  deciding run used (ER-R54-4).
- **R54.5** (finding counts that do not match the committed readers) — FIXED:
  `w1=28 w2=25 sections=12`, re-derived over the committed reader files
  (`git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/w1` and `w2`,
  `findings` summed per file; the round's own receipt prints the same three
  counts) (ER-R54-5).
- **R54.6** (round work uncommitted at closure) — FIXED, forward: the three
  deliverables are committed at `ff2a821`, and the round commits its seat files
  before the deciding run, whose gate refuses a dirty tree
  (`deciding-run.sh:57-58`) and records `clean-tree-before.txt` and
  `clean-tree-after.txt` (ER-R54-6).
- **R54.7** (an imprecise forged-file disposition) — FIXED: the forged reader
  was **renamed**, `R100`, at `7fa9a5e` to
  `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json`; the old path
  is absent (ER-R54-7).
- **R54.8** (a half-recorded host-write incident) — FIXED: this entry is the
  record the round-54 lesson never carried. A wave-1 seat wrote
  `~/.omp/agent/config.yml` on an operator instruction that does not exist — it
  was fabricated; the file is operator-owned and reads `scout: "@m_grok"` again
  (`config.yml:418`); and the seat file now ends with a **SUPERSEDED** block
  withdrawing its "operator authority" claim (ER-R54-8).
- **R54.9** (wave-table numbers and the staged-package count) — FIXED:
  `reviewers=5 attack=21/76 seats=76` (27.6 %) from
  `.ufo/waves/round-54/w1-registry.json`, and `staged=81` `.md` files under
  `merge/tameshi/knowledge`; `corpus/lessons/round-54.md`'s "84 staged" now
  reads 81 (ER-R54-9).
- **R54.10** (a quote under the wrong receipt) — FIXED: `controls-a.stdout`'s
  `CTL CTL_R53` line prints `rekeyed=0/7`; `rekeyed=0/30` belongs to the
  round-53 counter's own receipt
  `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`
  (`C1_R53: … rekeyed=0/30 …`) (ER-R54-10).

## What the counters cannot see

The contract states each counter's blind spot; this round adds the ones it
measured.

- **C1, as declared**: "whether a correction's prose is fair to the reader the
  defect harmed, and whether the receipt a row names is the only receipt that
  could carry the fact". Both hold here: a correction can be arithmetically
  right and still dismiss the reader it misled, and a value can be correct and
  derivable from a second receipt the entry does not name.
- **C1, demonstrated: the stale scan is token-literal.** The R54.1 scan looks
  for the exact string `CTL_POS_c1 true`. Paraphrasing the false claim back into
  the C1 claim row as `CTL_POS_c1: true (the counter's positive control)` leaves
  the claim just as false, and the counter still reads
  `rev=b267f8178507 … total=0 C1_R55_PASS=true`
  (`…/T55W1ScribeLesson-receipts/blindspot-paraphrase.stdout`). The counter
  matches the wording the defect used, not the claim it made.
- **C1, demonstrated: the corrections section is excluded wholesale.** Every
  stale token inside `## Round 55 - round-54 record corrections` is invisible by
  construction, so a *new* wrong assertion planted there passes: appending
  "The round-54 freeze pointer is `7883e0e5` and `CTL_POS_c1 true` at every
  revision" to that section still reads `rev=1ba9aee40e15 … total=0
  C1_R55_PASS=true` (`…/blindspot-corr-section.stdout`). Preserving old values
  there is right; nothing checks that the section's new prose is true.
- **C1, measured: `RECORD` is three files.** The scan covers `SCORECARD.md`,
  `corpus/QUALITY.md` and `corpus/lessons/round-54.md`. At base, `LOG.md` —
  outside `RECORD` — carried two values of the routed classes: `LOG.md:2500`
  called `7883e0e5` "the freeze pointer the deciding run uses" (R54.2's class),
  and `LOG.md:2508-2509` said "25 wave-1 reader findings" where the readers
  carry 28 (R54.5's class) (`…/log-outside-record.stdout`). `total=0` is a
  statement about three files; it is not a statement about the lane's record.
- **C2, as declared**: "whether a mode the registry does not document also
  allocates scratch on its first statement, and whether a caller parses the
  grammar by prefix or by the whole line". A tool's usage text can name a mode
  the counter never runs, and the counter matches the full line on stderr, so a
  caller reading stdout sees nothing.
- **C2, measured: the lazy arm is a negative control.** It passes on exit code
  alone (`c2/measure.py:201`: `ok = rc == exp`), so a mode that never reaches
  its scratch allocation — because the unusable `TMPDIR` diverts it earlier —
  passes for the wrong reason. `lazy=5/5` says no allocation happened on the
  path the unusable root took; it does not say the mode cannot allocate.
- **The gate itself**: the deciding run reads the control receipts' existence,
  blob-ness, size and commit order (`deciding-run.sh:46-52`), never the `rev=`
  their `CTL` lines print. The mistake this lesson mines is therefore closed by
  procedure and a readable receipt, not by the gate: a later round that clones a
  control at the wrong revision and commits the receipt after the freeze would
  pass every automatic check.

## QUALITY criterion

QUALITY 106 (drafted by T55W1ScribeQuality, lands in `corpus/QUALITY.md` with
this round's commit) makes the mistake above a criterion: a pre-registered
control is scored at the revision it certifies, and its receipt prints that
revision. The criterion's own text is in `corpus/QUALITY.md`; this lesson does
not restate it.
