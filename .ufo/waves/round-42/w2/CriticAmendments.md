# CriticAmendments — are post-freeze amendments P1–P4 rule changes dressed as citation fixes?

Seat: L1Tameshi42.CriticAmendments (critic, wave 2, round 42). Date 2026-10-25. Axes: calibration, depth.
Read-only. No counter was run in default mode. One scratch dir `/tmp/tameshi-r42w2-CriticAmendments-*` held probe
inputs and was deleted (`ls` afterwards: "No such file or directory").

Test applied (kumitate `corpus/knowledge/counter-amendment-discipline.md:66-67`, C14): "The counter, predicate, site
list and target are frozen against later disagreement; a rule rewritten after a seat scored is not the claim's rule".

## F0. No frozen rule byte moved between freeze and the integration tip (shared evidence)

- `git log -- .ufo/evidence/round-42/contract.json` gives only `322b5cd` (freeze) and `5f739ac` (wave-1 integration).
- `git diff 322b5cd a21845f -- .ufo/evidence/round-42/contract.json` has one hunk, `@@ -61,5 +61,42 @@`.
  It changes `"post_freeze_amendments": []` and adds the four P entries. `claims`, `predicate`, `kill_oracle`,
  `mutant_protocol`, `do_nothing_control` and `sourced` are byte-identical.
- `sha256sum` of both counters at the working tree: C2 `3c3727ec…890ff2` and C1 `9782a5a0…914c0e`. Both equal the
  contract's `counter_sha256` values. The fixtures, the m7 loop and the oracle are the frozen bytes.

So no amendment rewrites the counter, the predicate, the site list or the target. Each verdict below asks whether the
amendment changes what the claim means, or whether its labels (`before_data`, `rule_changed`) are calibrated.

## P1 — kill-oracle citation (claims.C2.kill_oracle): SURVIVES, with one calibration nit

- The rule is unchanged: runtime_error is not killed (measure.py, frozen sha above).
- The withdrawn support really contradicts the rule. In `.ufo/evidence/round-42/sources/pit-DetectionStatus.java:63`,
  `RUN_ERROR(true)` marks the status as detected. Line 37, `TIMED_OUT(true)`, does the same for timeouts.
- The withdrawal can only make the claim harder to pass, never easier. Under PIT's scoring a crashing mutant would
  count as a kill. The oracle keeps it as not killed, which is the strict direction.
- Replacement support checks out:
  - `SKILL.md:208-209`: "**Inconclusive** = no definitive verdict (timeout, crash before the summary, count not
    enumerated). Not a kill."
  - This line also covers the timeout divergence that `w1/CriticOracleSource.md` F5.3 called un-sourced.
  - The S001 snapshot (`.ufo/evidence/round-42/sources/stryker-mutant-states.html`, under "Runtime error") reads: "It
    is not represented in your mutation score." P1 paraphrases this as "Runtime error is not represented in the
    mutation score". The meaning matches; the wording is not verbatim.
- Calibration nit: `claims.C2.sourced` says "the kill oracle cites the PIT outcome vocabulary row adopted this round".
  After P1 the oracle cites PIT only as a divergence: S158 as contrary evidence, and S155 for the label alone.
  - The clause is still met as written. But its meaning moved from "supports" to "mentions", and P1 does not list the
    `sourced` field.
  - `contract.json` line 46 and the counter docstring at `census/measure.py:16-21` still state the false attribution.
    P1 discloses this.
- Smallest fix: P1 should also name `claims.C2.sourced`. It should say that PIT's vocabulary (S155) is cited for the
  label only, and that PIT's scoring (S158) is cited as a divergence.

## P2 — C1 statement vs m7 scope: SURVIVES (disclosed narrowing, not a rule change)

- The m7 loop was round-42-only at the freeze. `calibration/measure.py:236` reads `for _name, text in rec42:`, while
  the m8 and m11 loops at `:244` and `:249` read `rec41 + rec42`. The file's sha is unchanged since freeze.
- The predicate's class text was always round-42-only: "a round-42 record cites an S-id the registry does not hold as
  mined".
- P2 narrows the statement to match the frozen rule. It does not change the rule. The SCORECARD row says so: "cite no
  unmined S-id (round 42)" (`SCORECARD.md`, round-42 block, C1 row).
- Hand check reproduced at `a21845f`. I loaded the frozen `RECORDS[41]`, `section` and `S_CITE_RE` from the counter,
  plus a looser `S ?0*\d{3,}` pattern. Round-41 records (lesson, SCORECARD block, LOG section) cite S001, S153 and
  S154, all `mined`; the looser pattern finds nothing more. This matches `corpus/lessons/round-42.md:138-140`.
- Residual: the hand check names no revision. Round-42 work can still edit the round-41 SCORECARD and LOG sections
  before the deciding run.
- Smallest fix: pin the hand check to the measurement revision, or repeat it there.

## P3 — junk-control wording (claims.C2.do_nothing_control): SURVIVES

- `.ufo/evidence/round-42/control/c2-junk.stdout` shows `fixtures_pass=1/10` and `live_1682_ok=0 live_1685_ok=0
  live_123_ok=0`, with FAIL lines for F01, F04 and the three live sites. The contract text named only F02, F03 and
  F05–F09.
- The control is not part of the predicate, and the receipt shows the control is stronger than the text claimed. No
  rule effect.

## P4 — L1 authored `tools/write-path-census-v4.py`: not a rule change, but it weakens the claim and its labels are miscalibrated

What holds:

- No frozen field names who authors the tool. A grep of the contract for
  `executor|author|seat writes|L1 writes|L1 commits` matches only line 45, which is `mutant_protocol` ("a non-author
  mutation-tester seat writes …").
- The counter reads tool bytes at REV whoever wrote them. Swapping in a new tool changes the candidate, not the rule,
  so C14 is not violated.
- The L1's v4 (sha `784de4c0…`) contains no line-number or fixture-name literals. A grep for
  `1682|1685|123|case_dir|publish|mkdtemp|--out` hits only the docstring (lines 7-12, 24-25), the `mkdtemp`/`OUTPUT_FLAGS`
  tables (63, 68) and the selftest (470-605).

What does not hold:

1. **`before_data: true` is wrong for P4.** P4 responds to a candidate score under the frozen counter.
   `w1/ExecV4Tool.md` reports `fixtures_pass=3/10 … C2_R42_PASS=false`, and the commit was made after that score.
   - Calibrated label: "after a candidate score; no frozen rule changed".
   - `SCORECARD.md` (round-42 block, line 7 of the block, around line 2001) says "Post-freeze amendments P1–P4 change
     citations and disclosures only". P4 is neither a citation nor a disclosure; it changes who built the tool.
2. **"The mutant protocol is unchanged" is true of the text, but the separation behind it is gone.**
   - Before P4, the L1 authored the counter and fixtures, a seat authored the tool, and the L1 integrated as a
     non-author.
   - After P4, the L1 authored the counter, all 10 fixtures and the tool. It also wrote the mutant brief: `spec-w2.json`
     item MutantAuthor names the exact targets (`ClassInfo.method_return`, `Module.out_dests`, `_param_args`,
     `_parse_args_ns`, `_out_flag`).
   - The L1 also commits `mutants.json` "unchanged" and makes the deciding run. "Non-author" now covers only the bytes
     of `mutants.json`; the tool's author chose the targets.
3. **The predicate cannot tell a fixture-tuned tool from a real one, so P4's weakening lands on depth.**
   - `w1/CriticFixtureOverfit.md` Finding 1 shows a tool that special-cases names and line numbers (sha `63f688fe…`)
     scoring `fixtures_pass=10/10 … live_*_ok=1`.
   - The same report shows a mutant of that literal-table tool being `killed`. So the ≥3-killed-mutant gate also passes
     on a literal table.
   - With one author for battery and tool, every independent check sits outside the predicate, in wave-2 seats
     (ReviewV4Source, LabRenamedBattery, CriticV4Wrong, MutProbeAttr).
4. **No wave-1 seat attacked the L1's bytes.**
   - `grep -l 'eaf67995\|784de4c0\|write-path-census-v4' w1/*.md` finds no report quoting `784de4c0`.
   - The v4-facing reports were written between 06:28:03 and 06:29:23 (`ls --time-style=full-iso`). The integration
     commit `5f739ac` is at 06:41:37.
   - The only receipt on `784de4c0` is the L1's own labelled pre-run, `.ufo/evidence/round-42/prerun/c2-at-5f739acf.stdout`
     (`fixtures_pass=10/10 … C2_R42_PASS=false`).
5. **Probe: one wave-2 lab cannot see a known limit of the outflag class.**
   - v4 recognises only four flag spellings: `tools/write-path-census-v4.py:68`
     `OUTPUT_FLAGS = ('--out', '--output', '--out-dir', '--output-dir')`.
   - I ran the frozen `FIXTURES['F04_outflag']` with the flag renamed, through
     `python3 -I tools/write-path-census-v4.py --file F --json`:
     - `--out` gives `(7, True, False, 'expected.json argparse --out')`
     - `--output-dir` gives `(7, True, False, 'expected.json argparse --output-dir')`
     - `--target-dir` gives `(7, False, True, 'expected.json')`
     - `--dest` gives `(7, False, True, 'expected.json')`
   - The miss is conservative: the site stays flagged, so no write is hidden. It is disclosed at
     `corpus/lessons/round-42.md:172` ("four output-flag spellings") and in the knowledge entry at line 41.
   - But LabRenamedBattery's brief renames `--out` to `--output-dir`, which is on the list. That lab therefore cannot
     show whether the outflag class works by structure or by a name table. Only an off-list spelling can.

Smallest safe correction for P4. This needs no rule change and must happen before the deciding run:

- (a) Relabel P4 `before_data: false`, with the note "candidate swapped after a seat score; counter, predicate,
  fixtures and target unchanged". Change the SCORECARD wording to "citations, disclosures and one authorship change".
- (b) Record in the lesson and SCORECARD that C2's independent evidence is the non-author wave-2 seats, not the
  predicate. Name them, and admit C2 only if they pass.
- (c) Have a non-author seat check the MutantAuthor brief's targets against v4. Add at least one off-list-flag probe,
  and record its outcome as "stays flagged, disclosed limit".

## Verdicts per amendment

| id | rule changed? | label calibrated? | verdict |
|---|---|---|---|
| P1 | no (oracle bytes frozen; withdrawal only makes the claim stricter) | mostly; does not name the `sourced` clause it affects | SURVIVES |
| P2 | no (m7 was round-42-only at freeze; narrowing is disclosed) | yes; the hand check names no revision | SURVIVES |
| P3 | no (control is outside the predicate; receipt is stronger) | yes | SURVIVES |
| P4 | no (no frozen field names the tool author) | no: `before_data: true` and "citations and disclosures only" are false | weakens C2's independence |

## Tooling

No tools installed or updated. Only git, python3 and sha256sum were used.

BROKEN: P4's labels. It is not a rule change, but `before_data: true` and SCORECARD's "citations and disclosures only" are false. With one author for counter, fixtures, tool and mutant brief, C2's independence rests entirely on wave-2 non-author seats, because the predicate is known to be gameable. P1–P3 survive.
