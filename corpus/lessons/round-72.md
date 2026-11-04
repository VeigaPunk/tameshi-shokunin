# tameshi round 72 — lesson

Round 72 (attempt 1), base `f20ba482c7441d4c75818e7cd8a3165fee7821a1`
(`= origin/master`, clean tree). Claims, counters, kill rules and arms are
frozen **before any claim data** in `plans/round-72.plan.md` (declaration
commit `dfb534ca`). Round shape: one v1 wave, 12 seats (3 executor · 2 scribe
· scout · reviewer · critic · mutation-tester · sentinel · revenger ·
connector), policy band 8–16.

## Declared claims (frozen pre-data)

- **R72-C1 — capability acquisition (operability): planning-time rekey-cost
  forecast.** `tools/rekey-cost.py` prices a planned edit set against the
  cold-read ledger's own input pins. Frozen arms: `corpus/SOURCES.md` 13,
  `PROVINCE.md` 6, `corpus/QUALITY.md` 6, `SCORECARD.md` 0,
  `tools/pointer-recheck.json` 0, both 17, empty set exit 2; each
  non-structural arm was re-driven on the guard itself in scratch clones
  before the freeze (`.ufo/evidence/round-72/reh/`).
- **R72-C2 — calibration (lowest scored axis, 8): the two routed defects from
  the round-71 non-author closure paid.** S302's `§4.3` label superseded by
  S303 (`§4.2 Selecting lines by numbers`, page line 2246; the §4.4 quote at
  page lines 2446–2449, not 2445–2448), the PROVINCE round-16 append's
  `:85-91` corrected by an appended block (`:88-94` seven-leg cut, `:88-97`
  ten-leg ledger), three new pointer-recheck rows, census exit 0, and the
  cold-read rekey paid (forecast 17 = the guard's measured loss at the edit
  commit).

## Gate — the corrections (sourced claim)

**S303 admitted (supersedes S302).** Source opened this round: GNU sed manual
(GNU sed 4.9), <https://www.gnu.org/software/sed/manual/sed.html>, fetched
2026-11-03 (HTTP date `Wed, 04 Nov 2026 00:21:37 GMT`; `Content-Length`
415310; sha256 `511edd60a6f5034d4f28ca1dbe0772bbfd4c9865aaf6c0f85e2f05d4294b6bac`;
extract `.ufo/evidence/round-72/sources/sed.html`). The fetched bytes are
byte-identical to the r71 snapshot `511edd60…`, so this round's corrections
are record corrections, not source drift.

- Located quote 1 (≤25 words, page line 2246 heading + 2255 sentence):
  "Specifying a line number will match only that line in the input." — 12
  words, §4.2 **Selecting lines by numbers** (the heading is at page line
  2246; S302 labelled it §4.3).
- Located quote 2 (§4.4 Range Addresses, first paragraph, page lines
  2446–2449): "An address range matches lines starting from where the first
  address matches, and continues until the second address matches
  (inclusively)" — 20 words; the row had pinned 2445–2448, off by one.
- Admitted under CORPUS.md rule 2 as a same-URL supersession (`teaches` opens
  `supersedes S302 —`), which the census exempts from E04; the row joins the
  registry as S303 with `used-by corpus/lessons/round-72.md`.
- **Rejected (standing, re-sampled this round): S293's standing rejection**
  (git-cat-file batch framing) — S289 already holds the same URL at tier A
  for the object-inspection ground; a second row would duplicate scope. The
  rejection keeps reason + flip; re-read at the tip, verdict unchanged.

## Gate — the PROVINCE correction

Measured, not recalled (`grep -n` over `tools/mutate-and-run.sh` at the base):
line 84 is the `--regression` header; 85–87 the narrative; legs 1–10 at
88–97 (leg 7 `js-round-gate` at 94, leg 10 `bash-drift-pins` at 97). The
round-16 append's `:85-91` therefore carries the narrative plus legs 1–4.
The correction is an **append** (PROVINCE.md is append-only; line 57 stands),
introducing the two measured spans as tokens the pointer rows resolve.
