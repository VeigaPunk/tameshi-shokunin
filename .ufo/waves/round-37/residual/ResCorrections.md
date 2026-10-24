# ResCorrections — residual falsification of attempt-3 corrections

Seat: residual critic (read-only). Target: tip `ba3c35fb6c9582fcf2351c59c61661dd7a8e7400`
(branch master). Corrections landed in `583909a` over base `e6185d5f`; `ba3c35fb` adds only
the end-census receipt.

## Verdict

**All three corrections SURVIVE the attack.** Append-only form holds, every named
attribution and receipt citation resolves to real committed bytes, no correction claims
independent verification, and the one row edit (S104) touches exactly the two fields the
correction names. One LOW nit and one residual citation-inconsistency recorded below —
neither is a defect in the corrections themselves.

## Attack 1 — append-only form

```
git diff e6185d5f..ba3c35fb --numstat  (non-wave paths)
5 0 LOG.md | 12 0 corpus/QUALITY.md | 1 0 corpus/lessons/round-37.md
9 0 reports/round-1-calibration.md | 1 1 corpus/SOURCES.md
```

- `reports/round-1-calibration.md`: +9/−0. The erratum block is inserted at
  `round-1-calibration.md:167-175`, between the box-3 "remain unearned" paragraph and the
  `## box-4` heading — pure insertion, surrounding text byte-identical.
- `corpus/QUALITY.md`: +12/−0. Note appended after the last criterion-75 falsifier line
  (`QUALITY.md:891-902`), inside the append-only corrections convention.
- `corpus/lessons/round-37.md`: +1/−0. One bullet inserted before the Outside spot-check
  bullet; the original S104 admit Gate bullet (which intentionally still reads
  `lines 489–493` / `#L489-L493`) is unmodified — consistent with the correction bullet's
  own statement "the original admit bullet above stays as written." Honest: the stale
  numbers are retained *and flagged* by both the new bullet and `LOG.md:1996-1999`.
- `corpus/SOURCES.md`: +1/−1 = the S104 row. Field-wise diff
  (`git show e6185d5f|ba3c35fb:corpus/SOURCES.md | grep '^| S104'`, split on `|`):
  13 fields both sides; **only field 2 (URL fragment `#L489-L493`→`#L494-L495`) and
  field 6 (`lines 489–493`→`lines 494–495`) changed**. Title, kind, tier, teaches, status,
  opened, recheck, used-by all identical — matches the correction bullet's claim that
  "quote text, node anchor, pin and word count (15) are unchanged."
- Zero deletions anywhere else in the range (`git diff --numstat`: the only `1 1` is
  the S104 row; all wave files are additions).

## Attack 2 — honesty (no false provenance)

- Box-3 erratum: "no `[x]` is claimed" and "remains a lane assertion with no independent
  promotion verifier" — matches `SHONEN.md:10` (`[lane assertion, input-keyed monitor
  only; no independent promotion verifier]`). Erratum attributes the find to "wave-1 seat
  CriticSHONENRestraint" — `w1/CriticSHONENRestraint.md` Finding 2 names exactly this
  stale-trail defect and prescribes exactly this fix ("one append-only erratum"). True.
- QUALITY note: attributes to ReviewQualityCriterion — `w1/ReviewQualityCriterion.md`
  Findings 1 and 3 name both the falsifier-pointer ambiguity and the missing committed
  mutation receipt. True. The note asserts no independent re-derivation; it is a
  pointer clarification, self-labeled "Read the falsifier as:".
- S104 bullet: does not claim a non-author verifier; "re-opening the pinned bytes" is
  honest — no committed snapshot exists for S104 (unlike S102/S103; verified
  `.ufo/evidence/round-37/` contains no `src/` snapshot), and the re-fetch digest
  `f3d37d57…2be32d5` is the reproducibility anchor. Attribution chain consistent with
  `LOG.md:1996-1999` ("Wave-1 seat ReviewSourceScope found it").

## Attack 3 — consistency with cited files (first-hand re-verification)

**S104 line-window — independently verified against origin, not just seat reports:**

```
curl -fsSL 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303'
wc -lc      → 11553 lines, 415804 bytes          (matches bullet's "11,553 lines")
sha256sum   → f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5
awk NR 487–498:
489: @node ANSI-C Quoting
490: @subsubsection ANSI-C Quoting
491-492: @cindex lines
493: (blank)
494-495: Character sequences of the form @code{$'@var{string}'} are treated as /
         a special kind of single quotes.    ← the located quote
```

The correction's every numeric claim is exact: node block at L489–493, quote at L494–495.
Word count re-derived: `printf` of the plain-text quote → **15** — matches "word count
(15) unchanged" and the admit bullet's `(15 words)`.

**QUALITY criterion 73 mapping — verified against committed receipts:**

- `calibration/before-final-control.stdout`: `unresolved_control_inputs=1 …
  C1_R37_PASS=false` — before-state correct.
- `control/replay-at-final-control.stdout`: contains `mode=control` on both the
  `C1_R35_CONTROL … PASS=true` (v1) and `C1_R36V2_CONTROL … PASS=false` (v2) lines, plus
  `EMPTY_PANEL_REPLAY … v1_pass=1 v2_reject=1 … PASS=true` — the note's "`mode=control`,
  v1 PASS / v2 FAIL" is exact.
- `calibration/after-control-final.stdout`: `unresolved_control_inputs=0 correction=1 …
  C1_R37_PASS=true` — after-state correct.
- `grep -n 'mode=' .ufo/evidence/round-37/calibration/*.stdout` → no matches (exit 1):
  "no calibration/ receipt carries a mode label" is literally true.
- Original falsifier's `mode=deciding` half: `control/replay-at-final.stdout:9,18` shows
  `mode=deciding … C1_R35_PASS=true / C1_R36V2_PASS=false` — the mislabeled state the
  criterion kills. Consistent.

**QUALITY criterion 74 mutation-path note — verified:**

- `.ufo/evidence/round-37/mutation/branch-removal.stdout` (committed, exit 1):
  `CASE ansi-c-escaped-quote-trailing-comment FAIL`, `C2_R37_PASS=false`,
  `tool_sha256=835a0673…` = mutant digest in `digests.txt`; pristine control
  `pristine-frozen-predicate.stdout` shows both cases PASS at pin `da8c1ef4…` (matches
  `counter-pin.json` tool_sha256). The escaped-quote case fails on ANSI-C branch removal —
  exactly what criterion 74's anti-hardcoding clause demands. "The gap the same seat named
  is closed" is accurate (ReviewQualityCriterion Finding 3: "no committed falsifier
  path" — now there is one).

**Box-3 erratum vs `round-1-calibration.md` — verified:**

- The box-3 section records `[ ] (assertion rejected)` (`:217` disposition row) and
  "no lane assertion at all … does not qualify even for `[~]`" (`:160`) — erratum's
  "records an `[ ]` (assertion rejected)" is exact.
- `SHONEN.md:9` now carries `[~]` with pointer
  `.ufo/evidence/round-21/coldread/ledger.json` — file exists, valid JSON
  (`schema: tameshi-coldread-ledger-v2`, 497 entries, keyed by `skill_sha256`).
  "Ledger-keyed pointer / input-keyed monitor credit" matches the pointer's own label.
- "Written at the fleet round-1 blocked attempt": consistent — the file is the round-1
  audit; `[~]` landed later (`git log d9c496b..HEAD -- SHONEN.md` empty, so the mark
  predates r37 and the erratum's "later … supersedes … without rewriting" framing is
  accurate rather than claiming an r37 flip).

## Findings

1. **LOW — residual stale `489–493` citations outside the corrected row.** The correction
   deliberately preserves the Gate bullet's old range (flagged, per append-only
   convention) and `LOG.md:1983-1984` retains `#L489-L493` in the original frontier note —
   but `LOG.md:1996-1999` explicitly marks it stale and points to the correction. A reader
   grepping `#L489` still finds three hits (Gate bullet, LOG frontier note, URL inside the
   old row in history) — all disclaimed in-file. No action required; append-only
   convention working as designed.
2. **NIT — erratum phrase "a later, narrower lane assertion" could misread as a
   round-37 mark change.** `SHONEN.md` was not touched in r37 (`git log
   d9c496b..ba3c35fb -- SHONEN.md` → empty); the `[~]` predates this round. The erratum
   says "now carries," which is temporally true; no correction needed.

## Counterexample tried and failed

Strongest available attack: assume the off-by-five correction is itself wrong (line drift
between the wave-1 fetch and now). Re-fetching the exact pinned bytes (sha256 identical to
the S097/S104 pin) shows the quote at L494–495 and the node block ending at L493 —
the correction's old→new values are byte-exact. Second attack: assume the QUALITY note
invents the calibration/control receipt split — `grep mode=` proves the split is real and
the falsifier-as-written genuinely could not be satisfied by the single calibration file
it named for `mode=control`. Third attack: assume the mutation receipt is a sham control —
pristine PASS vs branch-removal FAIL receipts at distinct committed sha256s with a
documented disposable scratch lane (`scratch-revs.txt`, `scratch-dir.txt`) refute it.

## Tooling

No installs performed; all checks used git/curl/sha256sum/wc/awk/python3 already present.
Network: one outbound `curl` to `cgit.git.savannah.gnu.org` (200, 1.9 s).
