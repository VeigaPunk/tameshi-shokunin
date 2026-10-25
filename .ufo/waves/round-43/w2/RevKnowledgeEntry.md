# RevKnowledgeEntry — r43-survivor-resolution-rule.md vs the counter and the tool

Scope: `corpus/knowledge/r43-survivor-resolution-rule.md` checked against
`.ufo/evidence/round-43/mutants/measure.py` and `tools/write-path-census-v4.py`,
plus the committed source snapshots it cites. Every command below ran in a
read-only scratch clone (`/tmp/tameshi-r43-w2-RevKnowledgeEntry-clone`,
`git clone --shared`) or against the freeze bytes copied to `/tmp`; the lane was
never written. The counter file itself is read-only evidence; the scratch copy
at `/tmp/rke/measure-freeze.py` is the 3aee2c0 bytes and reproduces
`self_pin=1 … C1_R43_PASS=true`.

**Revision drift during review.** The lane moved five times while this review
ran: `3aee2c0` (freeze of record, counter `0d0f81…`) → `b510ad1` (A11) →
`bb36f80` (A12) → `f551ca6` (A13) → `6b83a11` (A14, HEAD). The knowledge entry
itself changed at A11 (the S089 byte-identity sentence). All findings below name
which state they hold at; where HEAD now repairs a frozen defect, the repair is
post-records-commit and post-dispatch.

## What checks out (no finding)

- **Freeze run reproduces the verdicts.** `python3 measure-freeze.py --lane
  … --rev 3aee2c0 --freeze 3aee2c0` → `self_pin=1 … mutants_declared=6
  mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0
  dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 C1_R43_PASS=true`,
  exit 0. Matches the receipt `.ufo/evidence/round-43/prerun/c1-at-freeze.stdout`.
- **`survived (4/6)` rows.** `--control` prints `battery=round42_ten_fixtures
  fixtures_pass=10/10 mutants_killed=4 C1_R43_CONTROL_PASS=false`; MutantAuthor's
  round-42 receipt confirms 2 survivors.
- **Outflag row mechanics.** `--probe-mutant` on the declared edit →
  `verdict=killed failures=1 first=['F11_outflag_namespace explicit_out=1 want
  0']`; pristine `explicit_out: False`, mutant `explicit_out: True` on
  `resolved='expected.json argparse --out'`. The kill is bound to F11 exactly.
- **Method row mostly.** Probe → `verdict=dead_code_only failures=1
  first=['F12_method_two_returns expected=1 want 0']`; pristine
  `resolved='self.destination()'`, `expected: False`. Mutation strings in the
  table are verbatim `mutants.json` find/replace.
- **Stryker citation.** `stryker-equivalent-mutants.html` line 16 carries the
  "It is called *equivalent mutant*. There is no definitive way for Stryker to
  find and ignore them." sentence; file is 38687 B, sha256 `79f6501a` — all as
  cited.
- **Wikipedia citations.** Line 794 `<p id="mw-Q">` and line 796 `<p id="mw-w">`
  carry the two quoted sentences inside `## Mutation testing overview`
  (span 762–800); no h2/h3 contains "equivalent"; zero hits for
  `surviv`/`unkilled`/`unreachable` — stronger than the entry's word-level claim.
- **PIT lines.** `.ufo/evidence/round-42/sources/pit-DetectionStatus.java`
  (sha256 `3bf295ad…`, matching SOURCES.md:128) has the quoted sentence at
  lines 71–72 and `EQUIVALENT(true);` at line 75.
- **Declaration set.** `mutants.json` at 3aee2c0: six mutants, classes
  attr/method/outflag, sha256 `b3abab06…` (the pin A11 added).

## Findings, by severity

### F1 — S158 paraphrase converts "cannot be *detected*" into "no test can *reach* it" (medium)

Entry (frozen lines 37–39): "…so a vendor that knows the class scores it as
detected **while stating that no test can reach it**." The snapshot at
`.ufo/evidence/round-42/sources/pit-DetectionStatus.java:71–72` says "Treated as
detected although by definition **it cannot be**." — the elided antecedent is
*detected*, not *reached*. An equivalent mutant is by definition reachable: it
runs under tests and simply never changes the outcome. The paraphrase reverses
the semantics, and it is load-bearing: the entry's own D/E split hinges on
exactly this distinction (an E mutant is one no test can *distinguish*, not one
no test reaches). Falsifier: `sed -n '68,76p'
.ufo/evidence/round-42/sources/pit-DetectionStatus.java`. Still wrong at HEAD.

### F2 — "Applied in order" (K first) is not what the code does (medium)

Entry line 50: "Applied in order to each survivor of the frozen mutant set:",
and the table lists K before D/E/U. The counter (`measure.py:573–578`, identical
at freeze bytes and HEAD) checks `me` **first**:
`if me: runtime_error.append(name); continue` — a runtime_error verdict preempts
K. Demonstrated: a mutant that drops the `parse_args` check (kills F11) **and**
crashes on `'--update'` (F10) produces
`fails=['F11_outflag_namespace explicit_out=1 want 0']` plus `errors=['F10_update_flag
exit=1 ZeroDivisionError']`. The stated order says K (the battery produced a
reachable FAIL); the code says `runtime_error` (U). The set under test never
hits the collision, so `C1_R43_PASS` is unaffected; the table's ordering claim
is what is falsified.

### F3 — "declared corpus" and "every case" were measured over 12 fixtures only at the frozen bytes (medium; repaired at HEAD by A14)

The E row (line 56) reads "The mutant differs from the pristine tool on no case
in the declared corpus"; the K row's battery is defined (contract `rule.K_kill`)
as 12 fixtures **+ 3 live sites**. At the freeze-of-record bytes, `differential()`
iterated `FIXTURES` only. Demonstrated: a mutant adding `'live-dependent'` to
`SCRATCH_MARKERS` flips `scratch` on `tools/registry-replay.py` site 125
(pinned live sites are 122/123 only) — battery 0 fails, `differential` `[]` →
the main loop would classify it `equivalent` although it visibly differs on a
live case. At HEAD (6b83a11, A14) `differential` now also fingerprints the three
live files (`measure.py:469–479`, comment "wave-2 RevC1Predicate F6"), so the
blind spot is repaired post-dispatch. The frozen artifact the entry claims
against did not test the "every case"/"declared corpus" quantifier; a wave-2
adjudication should record that the fix lands after the record.

### F4 — The reachability gate is fixture-scoped, not construct-scoped (low)

Consequence 2 (lines 64–68): "the lane still refuses to count it as a kill,
because no runtime path reaches **the construct that distinguishes the
mutant**." The code computes `detail[name] = bool(unreachable_statements(src))`
over the whole fixture source (`measure.py:352`): a kill on a fixture whose
discriminating construct is reachable but which contains an unrelated
`return`-followed statement would still be refused. The entry describes
construct-level attribution; the counter implements existence-in-file. For F12
they coincide; the general claim is untested.

### F5 — The PIT quote carries no resolvable path (low)

Lines 34–37 cite "line 71–72 of the committed snapshot; the enum constant is
line 75" without naming `.ufo/evidence/round-42/sources/pit-DetectionStatus.java`.
The S155/S158/Stryker cites name their files (registry row for S158 exists at
`corpus/SOURCES.md:128`, so a determined reader can find it — but the entry's
own convention is to name the snapshot, and C2's m8 only resolves backticked
paths, so nothing machine-checks this cite).

### F6 — Cosmetic misstatements (low)

- Line 79: "the mutant folds the first return (`tmp/expected.json`)". The
  mutant's emitted `resolved` is
  `"os.path.join('tmp', 'expected.json')tmp'tmp'expected.json'expected.json'"`
  (run census on F12 against the declared mutant); `tmp/expected.json` is the
  folded *value*, not the tool's resolved text. The parenthetical next to
  "(resolved text `self.destination()`)" invites a false literal comparison.
- Line 79: "the first is `os.path.join('tmp', 'expected.json')`" — the fixture's
  first return is `return first` bound to that call; minor.
- Line 8: "only by the **three** verdicts the rule defines" — the table defines
  four (K/D/E/U); if meant as survivor verdicts, say so.
- Line 14: "**Both vendors** say the tool cannot make that call" — one cited
  source is Wikipedia, not a vendor, and the paragraph then says PIT "answers
  differently".
- Line 100–102: "the lane has no detector for it" (E). The counter's
  `equivalent` list *is* a detector (an imperfect, fixtures-only one at the
  frozen bytes — see F3); "no detector" overstates the absence.

## Claims the counter does not test

- The "so" in the D row — that F12's divergence is *caused by* the unreachable
  second return, not merely that F12 contains one. `dead_code_arg_ok` only
  requires `dead_code_cases == ['F12_method_two_returns']`; any mutant differing
  on F12 for any reason satisfies it. The construction argument (the mutation
  only changes `len(returns)` handling, so only len≥2 discriminates) holds by
  inspection, not by counter.
- `C2_R42_PASS stays false` (line 74) — asserted, not re-measured (by design).
- "Six declared mutants, five kills, one named survivor" (line 94) is tested;
  "the numbers describe this set at this revision" is a disclaimer, correctly
  unmeasured.
- The K/D/E/U table's *meaning column* ("counted as a kill", "not a kill, not
  equivalence", "does not count toward resolution") is prose; the score
  consequence is only enforced through the aggregate `passed` predicate.

## Residual risk and verification gaps

- **The artifact under attack was amended while under attack.** The knowledge
  entry's S089 "byte-identical to S089's 2026-10-22 anchor" claim (present at
  records commit c5335c7 and freeze 3aee2c0) was false — anchor is `bc572676…`,
  new bytes `79f6501a…` (ScribeLessonGate D1, wave 1). A11 corrected the entry
  mid-wave-2. The corrected claim "every quoted sentence survives at the same
  offset" is itself unverifiable in-lane: the old snapshot bytes are not
  committed anywhere (only truncated hashes at `corpus/SOURCES.md:98` and
  `corpus/lessons/round-26.md:56`); the claim rests on the L1's word.
- **The contract's own `amendments_note` is stale at HEAD:** it still claims
  "A4-A7 change two counters … No amendment changes claims.* … the predicate,
  the target" while A9–A14 changed both counters, the guard, and the C1/C3
  `target` strings (kill_fixture_reachable→kill_binding, +held_refused/naive_agree/
  substitute). Not a knowledge-entry defect, but it means wave-2 reviews of
  "the frozen artifact" must now state rev explicitly.
- The F3 blind spot and the F11 binding are only *repaired* post-dispatch
  (A14, A11); anyone re-running the records-commit counter gets `kill_fixture_
  reachable=1` — a constant — as the sole evidence for "K — F11". The true
  binding (`kill_cases == ['F11_outflag_namespace']`) is only observable under
  A11+ bytes.

## Method record

- `git clone --shared` → `/tmp/tameshi-r43-w2-RevKnowledgeEntry-clone`; freeze
  counter copied to `/tmp/rke/measure-freeze.py`; measurement, `--control`, and
  `--probe-mutant` run at `rev=freeze=3aee2c0` (receipts above).
- `tools/write-path-census-v4.py` (sha `784de4c0…`, identical at
  base/records/freeze/HEAD) run `--json` on extracted F11/F12 for pristine and
  both declared mutants.
- Fabricated `/tmp/rke/mut_livediff.py` (SCRATCH_MARKERS +`'live-dependent'`)
  and `/tmp/rke/mut_errkill.py` (`_ = 1/0 if '--update' in text`) and drove the
  imported `battery`/`differential`/`main`-loop logic directly for F2/F3.
- No pacman transactions (pause honored); no tool installs needed.

Report: .ufo/waves/round-43/w2/RevKnowledgeEntry.md
