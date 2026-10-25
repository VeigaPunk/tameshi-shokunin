# Round 44 m7 landing-block token pre-scan

Axes: calibration (C1/m7) and freshness (S160). Read-only pre-scan; draft files are not yet the landing block/lesson.

## Tokens and disposition

- SCORECARD draft: S089, S159, S160, S256. Lesson draft: S089, S159, S160; `safe_floor=S256` appears in the round-43 record quoted in its Mistakes row.
- Registry evidence: `corpus/SOURCES.md:98` S089 is mined; `:129` S159 is mined and used by `corpus/knowledge/r43-survivor-resolution-rule.md`; tail `:456` declares Next unused id S160. S160 has no registry row at pre-scan time (the round-44 row is intended to be appended, not present yet). S256 has no registry row and is an assignment-bound value, not a citation.
- `key=S###`-form value explicitly present in the drafts: `safe_floor=S256` (also rendered with backticks in SCORECARD). The round-44 counter defines `ASSIGN_ID` at `.ufo/evidence/round-44/calibration/measure.py:89`, applies it before the citation scan at `:109-110`; therefore this assignment value is masked. Its T6 fixture at `:412-423` covers `safe_floor=S256` and spaced assignment syntax. The scorecard's quoted round-43 receipt is historical text, but the value remains masked wherever scanned.

## Actionable landing condition

S160 is the only draft token not currently represented by a mined registry row. It is intended to be a citation of the new source, not an assignment value. Before landing, append the planned S160 registry row with status `mined` and a used-by knowledge entry, as required by contract C2; otherwise the lesson/SCORECARD references to S160 would be unknown/unmined m7 citations. Do not treat the `Next unused id: S160` declaration at SOURCES.md:456 as a registry row.

No other draft S-token is neither a mined row nor an assignment value. No tools installed.
