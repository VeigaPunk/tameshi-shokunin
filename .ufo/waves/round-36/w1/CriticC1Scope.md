# CriticC1Scope — r36 w1 review of claim C1 (refresh-scope honesty)

Seat: critic (calibration axis). Attack target: whether the SCORECARD "restores
credit" wording for the 6 → 8 calibration move is consistent with the refresh
receipts' scope line and the lesson `## Holds`, or whether a reader could take
the printed 8 for a fresh blind cold-read.

## The scope line and the Holds

- `refresh-receipts.json:3` (top level), `:33,:61,:89,:117` (per receipt) and
  `:124` (`round36_provenance.scope`) all carry verbatim:
  `"L1-author input-keyed source reads only; not independent/blind cold-read,
  recipe re-execution or required-command coverage"`. `refresh-specs.json:3`
  (the pre-data spec) carries the same line.
- `corpus/lessons/round-36.md:75-78` (`## Holds` second filing): "the four
  re-anchored headings are credited by L1 author source reads (byte-consumption
  observations), not by a fresh blind cold-read; a future round that wants the
  stronger credit re-reads the sections independently." — an open hold, not a
  claim to the stronger credit.
- Trace receipts execute the same scope: `traces/L1/source-1.json` argv prints
  `"SOURCE-READS: byte-consuming SHA-256 observations; not recipe execution"`;
  new ledger entries 494–497 carry `seats: ["L1 TameshiR36 author source
  re-anchor"]` and `commands_executed_count: 1` (the read itself), matching
  `previous_class: "record"` in the specs.

## What the claim actually says

- `SCORECARD.md:1731` heading: "cold-read refresh (calibration 6 → 8)…" —
  "cold-read" modifies the monitor/ledger artifact, not a method; identical
  usage at `:598` (round-17 section titled "input-keyed cold-read") where the
  credit was explicitly non-blind.
- `SCORECARD.md:1743` claim row: "cold-read **monitor refresh** of the four
  round-35-drifted headings"; before `6, 60/64` at `796e08b`, after `8, 64/64`
  at the refresh commit, counting command = the frozen round-21 monitor.
- `SCORECARD.md:1756-1762`: "calibration 6 → 8: the strict cold-read monitor
  prints … 6, 60/64 at base 796e08b and 8, 64/64 at the refresh commit — the
  four … headings are re-anchored by **L1 author source reads** … the scope
  line of that protocol ('input-keyed source reads only; not
  independent/blind cold-read, recipe re-execution or required-command
  coverage') is carried verbatim in the round-36 refresh receipts."
- `contract.json:10` summary: "cold-read monitor refresh … restores credit";
  `:18` kill rule scopes the delta to "the refresh ledger entries and trace
  receipts … no monitor, ledger-algorithm or SCORECARD rubric change."
- `LOG.md:1909-1920` round-36 entry: "cold-read monitor refresh … per the
  round-21 **L1 author re-anchor protocol**: trace receipts …, four new ledger
  entries … (read_rev = the round-36 content commit)."

## Measured receipts (verified)

- `after/monitor-at-796e08b.stdout`: rev 796e08b… → score 6, 60/64, box3 false.
- `after/monitor-at-b455001e.stdout`: rev b455001e… (refresh commit) → 8, 64/64,
  box3 true.
- `control/monitor-at-e423c41b.stdout`: rev e423c41b… (content commit, all
  record edits, no ledger refresh) → 6, 60/64 — the do-nothing control holds.

## Counterexample tested (strongest available)

A reader skimming `SCORECARD.md:1731` sees "cold-read refresh (6 → 8)" and the
`8` — identical scalar to the round-16/17 `8` — and may take it as a fresh
blind read. This fails on the lane's own credit definition:

1. "Credit" is the ledger's input-keyed `credited` classification, never a
   blind-read bit. The monitor (`round-21/coldread/measure.py`, selector over
   the unchanged round-18 algorithm) counts sections credited under stable
   input digests; blindness is not a field it reads.
2. The 8-band never signified blindness: round-17 8 was "input-keyed" (LOG
   :1114), round-18 8 explicitly "not an independent or entirely blind
   cold-read … verifies the narrower input-keyed predicate" (SCORECARD
   :671-673). Round-36's 8 stands in the same scalar series under the same
   instrument; it neither upgrades nor dilutes provenance.
3. "Restores" is the accurate verb: credit of the same class, lost to
   input-drift, is recovered by re-keying entries to current bytes. No
   sentence in the round-36 record asserts blind/independent reads — the
   scope denial is present in every surface (receipts ×6, specs, SCORECARD
   prose, LOG entry, lesson Holds).
4. The misread path requires stopping at the heading; the very next row cell
   says "monitor refresh", and the numeric paragraph ~15 lines later quotes
   the scope denial verbatim. Established convention (round 17 onward) names
   "cold-read" the artifact, not the method.

## Adjacent observation (out of this ticket's scope, noted for the ledger)

New ledger entries record `read_rev: e423c41b` (content commit) and were read
in a scratch checkout at that rev, while the four input SHAs bind to bytes at
the refresh commit `b455001e` — consistent (the monitor confirms byte-identity
at b455001e), but `read_rev` is metadata a future reader could misread as the
measurement rev. Receipts' `round36_provenance.read_rev` repeats it. Fixable
by convention note; not a defect under the kill rule.

## Verdict

**Defensible.** "Restores credit" claims exactly what the instrument measured
(6 → 8, 60/64 → 64/64) under the credit rule the lane has used since round 17,
and the record disclaims blind/independent reads in five places including the
receipts' scope line and the lesson Holds. No overclaim of a cold-read.

Smallest safe correction (optional polish, not required): change the
`SCORECARD.md:1731` heading to "cold-read **monitor** refresh" to match the
claim-row wording and remove the last surface where "cold-read" could be
misread as a method before the prose arrives.

## Commands run (read-only analysis)

- `find .ufo/evidence/round-36 -type f` and same for round-21/coldread (lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)
- `grep -n -i 'cold\|credit\|calibration\|refresh\|restores' SCORECARD.md`
- `read` of contract.json, refresh-receipts.json, refresh-specs.json, affected-sections.json, SCORECARD.md:1731-1776 + :630-680, corpus/lessons/round-36.md, LOG.md:1898-1942, round-21/coldread/measure.py, traces/L1/source-1.json
- `python3` JSON extraction of `calibration_restraint_score`, `sections_covered`, `box3_full_page`, `missing` from the three committed monitor receipts (revs 796e08b, b455001e, e423c41b); tail-4 of the 497-entry ledger
- `grep -n -i 'blind\|independent' LOG.md` — verified no round-36 sentence asserts blind/independent reads; every mention is a disclaimer
- No tools installed or updated; no git/jj commands; no monitor re-execution (committed receipts used).
