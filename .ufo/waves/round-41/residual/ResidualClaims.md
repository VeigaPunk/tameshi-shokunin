# ResidualClaims — claim audit of round 41

Seat: `L1Tameshi41.ResidualClaims` (read-only). Lane checkout, report, fleet repo, sibling lanes, jj
state and Git index were not modified; the only write is this report. No tool installs or upgrades.

Audited: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/tameshi.md` sections `## Work performed`
(lines 8–67), `## Before → after measurements` (69–129), `## Trend verdicts` (174+), and the claim
statements in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/contract.json`
(`claims.C1.statement`, `claims.C2.statement`, predicates, targets, `do_nothing_control`, kill rules).

Revisions used by every command below (each command names its `--rev`):

- base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`
- history `b37ce974b6efb8c465626d7346149549a3300a4b`, deciding `baa18b7bdd637ff175255e82b6bee3c85df0881e`
- measured `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`, tip `812ee0d11d267e131be3dc8db0b71253cbae9234`

Replays were run at all four revisions plus `--control`. All quotes below are byte-compared against the
committed receipts, not eyeballed.

---

## 1. Support table — every sentence that asserts a measured improvement

`PASS` = the named receipt contains exactly the asserted value. `DEFECT` = the receipt does not carry
the assertion (wrong revision, missing artifact, contradicted wording), with the correction in §5.

| # | Sentence (report §, line) | Receipt | Verdict |
|---|---|---|---|
| 1 | "Calibration (measured 6) is the lane's lowest non-retired axis" (Work, 10) | `.ufo/evidence/round-41/census/command-d.stdout` → `coldread score at a3d6c690 = 6`, `coldread score at b37ce974 = 6`; replay of command C at `2ae00eb7` → `boxes=4 checked=0 asserted=4 untouched=0` and `SHONEN.md` byte-unchanged `b37ce974..2ae00eb7..812ee0d1` | PASS for `6`. "lowest" is decided only against depth: command D replay at `2ae00eb7` → `recorded_cases=9 depth_score=9`. Note §2 F2: three artifacts still say 8. |
| 2 | C1 class list: "m6 the standing `sources-registry` count, m7 …, m8 …, m9 the round-40 quarantine-summary contradiction" (Work, 13–15) | counter `.ufo/evidence/round-41/calibration/measure.py` (sha `9aaa99ac…` = pin) | DEFECT (wording). m9 as written is *not* the measured class; see §3 D1 and §5 R2. |
| 3 | "the base receipt … (`m6=1 m9=1 total=2`, exit 1)" (Work, 17) | `before/c1-at-base.stdout` (all three lines byte-equal to the report block) + `before/c1-at-base.exit` = `1` | PASS |
| 4 | "the deciding receipt `.ufo/evidence/round-41/after/c1-at-baa18b7b.stdout` (`total=0`, exit 0)" (Work, 20) | file prints `… total=0 records=3 sources_rows=109 rev=baa18b7b… C1_R41_PASS=true`; `after/c1-at-baa18b7b.exit` = `0` | PASS |
| 5 | "the tool at `095924a7…`, fixtures `…/census/fixtures.json`, counter `…/census/measure.py`, deciding receipt `after/c2-at-baa18b7b.stdout`" (Work, 26–31) | `git show 2ae00eb7:tools/write-path-census-v3.py \| sha256sum` → `095924a7…0279` (= pin); fixtures → `20b6254d…6329` (= pin); counter → `83268eff…94c` (= pin); v2 → `40228532…878b` (= pin); receipt byte-equal to report | PASS |
| 6 | "`:811` (a variable destination that v2 records as a write site with no expected-value destination) and `:820` (`os.symlink`, which v2 does not see at all)" (Work, 33–34) | `after/c2-at-2ae00eb7.stdout` → `live_var_lineno=811 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820 live_symlink_sites_v2=0` | PASS ("does not see at all" = no write site under v2's patterns; `git show 2ae00eb7:tools/write-path-census-v2.py \| grep -c 'os\.symlink'` → `0`) |
| 7 | "Both are scratch fixtures, so the round claims visibility of the destination, not a new open write path" (Work, 34–35) | counter fields `live_var_scratch_v3=1 live_symlink_scratch_v3=1`; *content* checked by running v3 on `2ae00eb7:tools/repeat-control.py`: line 811 → `resolved` = `os.path.join(tamper_duplicate_key, "expected.json")…tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")`, `expected=True scratch=True`; line 820 likewise | PASS on content; the *counter* does not decide it — see §4 D4. |
| 8 | "the standing `sources-registry` row restated to the registry's real count (`SCORECARD.md`)" (Work, 37) | `SCORECARD.md:1851` → "→ 109 rows at round 41 (restated from 103 by the round-41 C1 claim…)"; registry at `2ae00eb7` = 109 S-rows | PASS |
| 9 | "the round-40 quarantine-summary correction appended to `corpus/lessons/round-41.md` — the round-40 file itself is untouched" (Work, 37–38) | lesson §`### Correction — the round-40 quarantine summary` (lines 51–58) states "one adopted, six refused, ten present-but-not-appended" and "The round-40 file is unchanged"; `git diff --stat a3d6c690..812ee0d1 -- corpus/lessons/round-40.md` → empty | PASS |
| 10 | "S153 (`ast`) and S154 (`Path.write_text`) opened 2026-10-25, each pinned to a committed snapshot …" (Work, 40–43) | `wc -c` → 362029 / 271189 B; `sha256sum` → `183a4f8c…5317` / `0044cae6…4f093`; titles `Python 3.15.1 documentation`; rows at `corpus/SOURCES.md:123–124` = 13 `\|`-fields, tier A / docs / mined / 2026-10-25 / 180d | PASS |
| 11 | "one knowledge entry admitted … with a `corpus/README.md` coverage row and `corpus/QUALITY.md` criterion 80" (Work, 44–46) | `corpus/knowledge/r41-variable-destination-writes.md` (7724 B); `corpus/README.md:517`; `corpus/QUALITY.md:967` `### Criterion 80` | PASS |
| 12 | "Wave 1: one v1 wave, 40 seats, dispatched as exactly one batched `task` call from the validator's `taskCall` … attack roles 18/40 = 45 %. Dead seats: 0" (Work, 48–54) | `dispatch-w1.json`: `taskCall.tasks` = 40, `resumeSends` = `[]`, `counts {spawn:40, resume:0}`; `w1/swarm-registry.json` roles reviewer 10 / executor 8 / scribe 7 / scout 6 / critic 5 / mutation-tester 3 / connector 1 (= 40; attack 18 = 45 %); `ls w1/*.md` → 40 non-empty; `settlement-receipt.json` reports 40/40, empty `[]`, dead `[]` | PASS |
| 13 | "Residual call: one ordinary `task` call of 8 reviewer/critic seats … wave 1's output yielded 8 further distinct attack items, fewer than the 32 a wave 2 requires … Round total 48 seats, inside the 32–128 band" (Work, 56–60) | thresholds: round prompt (`.ufo/prompts/tameshi-round-41.md`, lines 179–196) — round total 32–128, wave 2 only at ≥32 distinct attack items, residual ≤8 counted in the round total | Thresholds PASS. DEFECT for the *enumeration*: no committed file lists the 8 items and `.ufo/waves/round-41/residual/` does not exist at the tip (`find .ufo/waves/round-41 -maxdepth 1 -type f` → dispatch-w1, spec-w1, settlement ×2 only). See §5 R11. |
| 14 | "Attempt 1 ended `lane-dead-no-report tameshi round=41` (watchdog, 2026-10-25T03:23:08-03:00)" (Work, 65) | `.ufo/watchdog.log:1247` → `2026-10-25T03:23:08-03:00 lane-dead-no-report tameshi round=41; retry same round (hyaku-inline attempt=1: run-6: attempt-1 orphan — no report, session died 2026-10-24 ~23:30 -03)` | PASS for the report. Contract metadata is wrong (§5 R13). |
| 15 | C1 before block (Before→after, 71–79) | identical to `before/c1-at-base.stdout` (three lines) + `.exit` 1; my replay at `a3d6c690` with the pinned counter bytes reproduces it byte-for-byte | PASS (also closes the "which counter bytes produced the before run" gap: the final bytes reproduce it) |
| 16 | "After, at `2ae00eb750…`" (Before→after, 85–89) | `after/c1-at-2ae00eb7.stdout` byte-equal, `.exit` `0`, committed in `0c8e1be` | PASS |
| 17 | "Delta: two live mismatches → zero, and the two record-audit classes (m7, m8) measured at zero on this round's three records" (Before→after, 91–93) | `records=3`; m7 audit: cited S-ids are lesson `S001 S153 S154`, SCORECARD `S153 S154`, LOG `S153 S154` — every one `mined` in the 109-row registry; m8 audit: every backticked path-shaped token in the three records resolves at `2ae00eb7` | PASS, with two scope notes (§3 D2/D3). |
| 18 | "Do-nothing control: the base run itself — m6 and m9 survive any edit that does not touch them, so no do-nothing path reaches total=0" (Before→after, 94–96; contract `claims.C1.do_nothing_control`) | counter code read; base receipt | DEFECT (universal, falsified — §2 F3, §5 R5). |
| 19 | C2 before / control / after blocks (Before→after, 98–118) | `before/c2-at-base.stdout`, `control/c2-control.stdout` (`.exit` 1), `after/c2-at-2ae00eb7.stdout` (`.exit` 0) — all three byte-equal to the report | PASS |
| 20 | "Both counters were run again at the lane tip `812ee0d1…` and printed the same two lines, exit 0 each; … the second run is the same measurement" (Before→after, 118–121) | no receipt exists at `812ee0d1` (`grep -rl 812ee0d1 .ufo/evidence/` → empty; `find .ufo/evidence/round-41 -type f` shows only `a3d6c690`, `b37ce974`, `baa18b7b`, `2ae00eb7`) | DEFECT (evidence gap). Replay at the tip prints the same field values with `rev=812ee0d1…`, exit 0 each (§5 R8). |
| 21 | "**Numeric guardrails at the measured commit** (`.ufo/evidence/round-41/census/command-d.stdout`)" (Before→after, 121–123) | the receipt's own first line: `# command D at b37ce974b6ef…`; its coldread lines are `at a3d6c690` and `at b37ce974` — not the measured commit | DEFECT (label). Values hold at `2ae00eb7` by replay + byte-invariance (§5 R6). |
| 22 | "the carried `8` is superseded as an upper bound and calibration is 6 → 6" (Before→after, 123) | `SCORECARD.md:1900` "Calibration (8) is the lane's lowest non-retired axis"; `LOG.md:2119` "the lane's lowest non-retired axis at 8"; `contract.json.stagnation_nudge` "calibration (8) is the lowest non-retired axis"; receipted value is 6 | DEFECT (§2 F2, §5 R7) |
| 23 | "No axis is harmed" (Before→after, 123) | command D and command C receipts cover depth and calibration only | DEFECT (universal over six axes — §2 F4, §5 R9) |
| 24 | "Negative control for the C1 parse, receipted in `.ufo/waves/round-41/w1/CriticR40Discharge.md`: the round-40 table counts `(1, 6, 10)` while its summary says `(1, 7, 9)`" (Before→after, 125–128) | re-derived: 17 rows; adopted 1 (S132); refused 6 (S109 S131 S137 S140 S141 S143); present/misbound 10; round-40 closing sentence says "seven refused … nine present-but-not-appended" | PASS |
| 25 | "expansion: improved … Two registry rows added" (Trend, 176–181) | `before/c1-at-base.stdout` `sources_rows=107`; `after/c1-at-2ae00eb7.stdout` `sources_rows=109`; `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi` at the tip → `tameshi rows 109`, `status.mined 81` | PASS on artifacts. The verdict word "improved" is not computed by any counter (§3 V1). |
| 26 | "quality: improved … v3's selftest fails when name resolution, the symlink branch or the symlink destination argument is removed" (Trend, 182–189) | reproduced all three mutants from the pinned tool bytes at `2ae00eb7`: `resolve` exit 1 with `FAIL planted var_unflagged: want unflagged=1 got 0`; `symlink` and `symlink_arg` exit 1 with `FAIL planted symlink_unflagged: want unflagged=1 got 0` — assertion FAILs, not tracebacks | PASS |
| 27 | "discernment: improved. One admit, three refuses and one prior-art citation" (Trend, 190–196) | lesson blocks `### Admit`, `### Reject` (package; round-40 row), `### Adjacency` (sibling code refused by `PROVINCE.md`) | PASS on counts; verdict not counter-decided (§3 V3). |
| 28 | "Round start: exit 0, 107 rows, 9 × W04 + 1 × W01, zero E codes" / "Round end: exit 0, 109 rows" (Sources & frontier, 132–138) | `census/start.stdout` and `census/end.stdout` are **byte-identical** (`md5 12d1004ffa553a5825bfb426f31f06f0`, 11 lines each) and print **no row count** — 9 W04 + 1 W01 + one `ok` line | DEFECT as cited (§5 R10). The counts are true elsewhere: `sources_rows=107` at base, `109` at `2ae00eb7`/tip, and `census` mode prints `rows 109`. |

---

## 2. Universal wording (flagged)

**F1 — contract C1 statement, clause 1:** "the lane's self-assessment records agree with observed repo
state". The counter audits exactly three records, and the clause is contradicted *inside* two of them
by the calibration number (next item). Narrow form in §5 R1.

**F2 — the calibration 8 / 6 contradiction is live in the audited records.** The report says "measured
6" and "calibration is 6 → 6", but:

```
$ grep -n "Calibration (8) is the lane's lowest" SCORECARD.md      → 1900   (inside `## Round 41`)
$ grep -n "lowest non-retired axis at 8" LOG.md                    → 2119   (inside `## 2026-10-25 — round 41`, head at 2092)
$ python3 -c "import json;print(json.load(open('.ufo/evidence/round-41/contract.json'))['stagnation_nudge'])"
  does not fire: … calibration (8) is the lowest non-retired axis and carries C1
```

while the receipted value is 6 (`command-d.stdout` `coldread score … = 6` at base and `b37ce974`;
`SHONEN.md` unchanged to `2ae00eb7`, so command C still prints `boxes=4 checked=0 asserted=4`).
The same SCORECARD section says "Calibration remains the lowest axis at 6" (line 1926). So the round
repaired the registry cell but left the axis score unreconciled in three artifacts — precisely the
class C1 is named for, and no m-class measures it. "Superseded as an upper bound" is asserted, not
applied. This is the strongest residual defect: the C1 claim's general clause is false at the measured
revision even though all four declared classes are 0.

**F3 — m6/m9 do-nothing wording.** "m6 and m9 survive any edit that does not touch them" is false as a
universal, from the counter's own code:

- m6 compares `SCORECARD`'s last `| sources-registry |` cell against the `SOURCES.md` S-row count, so
  changing **SOURCES.md** (the other side of the comparison — this round moved it 107 → 109) clears or
  breaks m6 without touching the SCORECARD cell. Additionally `if standing:` means **deleting** the
  standing row suppresses the class entirely (no standing row → no check).
- m9's mismatch is between two texts inside `corpus/lessons/round-40.md`; editing that file's summary
  to agree with its table clears m9 with no round-41 correction.

The conclusion ("no do-nothing path reaches total=0") survives; the justification does not.

**F4 — "No axis is harmed."** Six axes are named in `AXES.md`'s vocabulary; receipts exist for depth
(command D) and calibration (command C) only. This round edited no other axis surface, but that is an
inspection, not a measurement.

**F5 — contract C2 statement.** "resolves a write destination held in a variable" reads universal; the
same contract's `declared_scope_limit` says "aliases, closures over reassigned names, attribute
reassignment, conditional assignment and any path computed by a non-folding call are not resolved; no
universality is claimed", and the report's own open items name the false-positive class
(`tools/context-capture.py:1682/1685`, destination base `self.case_dir(name)` → `unflagged`). The
`v2 can only match a literal on the same line` half is sound: `git show 2ae00eb7:tools/write-path-census-v2.py | grep -c 'os\.symlink'` → `0`, and `V2_EXPECTED_RE` requires a quoted literal on the write line.

**F6 — "both counters were run again at the lane tip … the second run is the same measurement"**
conflates a replay with a measurement at three revisions; the contract's kill rule names one
default-mode run *at the measurement revision*. The measured revision's run is unique and receipted
(`after/*-at-2ae00eb7.*`); the `b37ce974`, `baa18b7b` and (unreceipted) tip runs are replays and should
be labelled as such (the report does label `b37ce974` as history; it does not label the tip run).

---

## 3. Verdicts the receipts do not decide

- **V1 expansion "improved"** — the artifacts are receipted (one entry, one README row, criterion 80,
  107 → 109 registry rows, census `rows 109`), but no instrument computes an expansion delta. What the
  receipts decide is "one entry admitted and two rows opened"; "improved" is the lane's judgment.
- **V2 quality "improved"** — the mutant kills are real and I reproduced them (PASS above), but
  `C2_R41_PASS` is a capability predicate, not a quality score. The seat's
  `MutConstantClassifier.md` claim is not replayed by me and no counter reads it.
- **V3 discernment "improved"** — admit/refuse counts are decided by the lesson text; the axis verdict
  is not.
- **V4 "the stagnation nudge does not fire because round 40 added a capability inside the window N=2"**
  — a policy reading with no receipt in the round; nothing in the evidence fixes N or the table's
  round-40 cell.

None of these is a false measurement; each is a verdict word laid on top of true artifact counts. The
narrowest honest form keeps the counts and drops the implied measurement ("one entry and two rows
added; three instrument properties demonstrated; three refusals recorded").

---

## 4. Claims that depend on a defect the round disclosed

- **D1 — m9 is not "the round-40 quarantine-summary contradiction".** The class fires only when the
  contradiction exists **and** no round-41 correction supplies the table's counts. At the measured
  revision the contradiction still exists (round-40 file untouched: summary `(1,7,9)`, table
  `(1,6,10)`), and m9 reads 0 because of the appended correction. So "two live mismatches → zero"
  means: m6 was repaired, m9 was **annotated**. The report discloses the correction elsewhere; the
  class gloss and the delta sentence do not carry it.
- **D2 — m6's surface is one row of four.** `SCORECARD.md` carries four `| sources-registry |` standing
  rows (lines 240, 1514, 1609, 1851) stating 44, 94, 99 and 109 rows; the counter reads
  `standing[-1]`. "The standing sources-registry count matches the registry" is true for the last row
  only, and the report does not say so.
- **D3 — m8's surface is four prefixes plus seven root files.** No live counterexample exists (every
  path-shaped citation in the three records resolves, including `considerthese/2026-10-24.md`), but the
  class does not see paths outside `corpus/`, `tools/`, `.ufo/evidence/round-41/`,
  `.ufo/waves/round-41/`. The class as worded ("cited repo paths") is wider than the audit.
- **D4 — "the round claims visibility of the destination" is not receipted by `C2_R41_PASS`.** The
  counter reads `expected`/`scratch`/`kind`/`lineno` and never `resolved` (disclosed in
  `SCORECARD.md`). I closed the content question by running v3 directly (line 811/820 `resolved` shows
  the tmp-dir `expected.json` destination), but a constant `{811: open, 820: symlink}` table would still
  satisfy the predicate. The claim is true; the receipt does not carry it.
- **D5 — the three-mutant kill oracle is `returncode != 0`.** For *these* mutants the oracle is not
  load-bearing: each dies on its own fixture class with an explicit `FAIL planted …` line (I reproduced
  all three). A successor oracle (exit + FAIL line) would prove the same thing more tightly; nothing in
  this round depends on the weak form.

---

## 5. Narrowest honest replacements

**R1 — contract `claims.C1.statement` (and every paraphrase of it):**
> the three round-41 records (the lesson, `SCORECARD.md` §Round 41, `LOG.md` §2026-10-25 — round 41)
> score 0 on four declared classes: the last standing `sources-registry` row matches the registry's 109
> rows, no cited S-id is unmined, every path-shaped citation under the four audited prefixes resolves
> at the measured revision, and the round-40 quarantine summary — which still contradicts its own
> table — is corrected in the round-41 lesson. The records do not agree with observed state on the
> calibration score: `SCORECARD.md:1900`, `LOG.md:2119` and `contract.json.stagnation_nudge` say 8 where
> command C reads 6, and no m-class measures that.

**R2 — m9 gloss (report line 15):**
> m9 an *uncorrected* round-40 quarantine-summary contradiction: that file still says seven refused /
> nine present against its table's six / ten, and m9 counts 0 only because the round-41 lesson appends
> the table's counts.

**R3 — m6 gloss (report line 13):**
> m6 the count in the last standing `sources-registry` row (`SCORECARD.md:1851`) against the registry's
> S-row count; the three earlier standing rows (44, 94, 99) are outside the class.

**R4 — m8 gloss (report line 14):**
> m8 path-shaped citations under `corpus/`, `tools/`, `.ufo/evidence/round-41/`,
> `.ufo/waves/round-41/` and seven root files that do not resolve at the measured revision.

**R5 — do-nothing control (report line 94; contract `claims.C1.do_nothing_control`):**
> Do-nothing control: no do-nothing path reaches `total=0`. The base prints both mismatches; clearing
> m6 requires changing the SCORECARD cell *or* SOURCES.md's row count, clearing m9 requires a round-41
> correction *or* an edit inside round-40, and the counter cannot tell which side of either comparison
> moved; deleting the standing row suppresses m6 by construction (`if standing:` guard).

**R6 — guardrail label (report line 121):**
> **Numeric guardrails at `b37ce974`** (`.ufo/evidence/round-41/census/command-d.stdout`): command D
> `recorded_cases=9 depth_score=9`, command C `boxes=4 checked=0 asserted=4 untouched=0`, coldread 6 at
> the base and at `b37ce974`; `SHONEN.md` and `tools/mutate-and-run.sh` are byte-unchanged through the
> measured commit and the tip, and a replay at `2ae00eb7` prints the same two lines.

**R7 — "superseded as an upper bound" (report line 123):**
> the numeric block supersedes the carried 8 as an upper bound; three artifacts still state calibration
> 8 (`SCORECARD.md:1900`, `LOG.md:2119`, `contract.json.stagnation_nudge`) and the round did not
> restate them.

**R8 — tip re-run (report lines 3 and 118):**
> the two counters were replayed at the tip `812ee0d11d267e131be3dc8db0b71253cbae9234` and printed the
> same field values with `rev=812ee0d1…`, exit 0 each. (This review's replay; no receipt for the tip run
> is committed.)

**R9 — "No axis is harmed" (report line 123):**
> depth 9 → 9 and calibration 6 → 6 are receipted; the other four axes carry no measurement this round,
> so no harm is claimed beyond those two.

**R10 — census row counts (report lines 132, 138, 170):**
> `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi` prints
> `tameshi rows 109` (`status.mined 81`) at the tip; the two `validate` receipts are byte-identical and
> carry the same ten warnings (9 W04, 1 W01) with no row count; the base count of 107 is receipted by
> `before/c1-at-base.stdout` (`sources_rows=107`).

**R11 — residual call (report lines 56–60):**
> the round routed 8 distinct attack items into one ordinary `task` call of 8 reviewer/critic seats (the
> round prompt's residual ceiling, lines 195–196); their reports land under
> `.ufo/waves/round-41/residual/` and were not committed at the tip, so the 8 items are enumerated
> nowhere in the committed tree.

**R12 — C2 capability sentence (report line 25; contract `claims.C2.statement`):**
> `tools/write-path-census-v3.py` resolves a write destination bound by up to four
> assignment/`os.path.join`/`+`/`/`/f-string hops over literal, name and attribute nodes, for `open`,
> `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`, and classifies the resolved
> text as expected-value, scratch or update-flagged; aliases, closures over reassigned names, attribute
> reassignment, conditional assignment and non-folding call bases are not resolved (the disclosed
> `unflagged` false-positive class, e.g. `tools/context-capture.py:1682/1685`).

**R13 — contract `inherited_state` (metadata, not a claim statement):** "attempt 1 `2026-10-24T23:07
-03`" is the launch line (`.ufo/watchdog.log:1236`); the death line is `:1247` at
`2026-10-25T03:23:08-03:00`, session died `2026-10-24 ~23:30 -03`. The report's version is right.

---

## 6. Findings, PASS or DEFECT

**DEFECT 1 — records still disagree on the calibration score (F2).**
Command: `grep -n "Calibration (8) is the lane's lowest" /home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md`
→ `1900:Two claims on distinct axes. Calibration (8) is the lane's lowest non-retired axis and carries C1;`
`grep -n "lowest non-retired axis at 8" …/LOG.md` → `2119`. Receipt for the observed value:
`python3 .ufo/evidence/round-41/census/measure.py`-side command C replay at `2ae00eb7` →
`boxes=4 checked=0 asserted=4 untouched=0` (coldread 6). Three artifacts vs one receipt, inside the
records the C1 claim audits. Fix: restate the three cells or scope the claim to m6–m9 (R1).

**DEFECT 2 — the do-nothing control's universal wording is falsified by its own counter (F3).**
`sed -n '250,275p' .ufo/evidence/round-41/calibration/measure.py` shows m6 compares two files
(`if standing:` … `int(match.group(1)) != observed_rows`) and m9 compares two texts inside round-40.
Fix: R5.

**DEFECT 3 — "numeric guardrails at the measured commit" cites a receipt produced at `b37ce974`
(report line 121).** The receipt's header is `# command D at b37ce974b6ef…`. Fix: R6 (values hold by
replay: `recorded_cases=9 depth_score=9`, `boxes=4 checked=0 asserted=4 untouched=0` at `2ae00eb7`).

**DEFECT 4 — the tip re-run has no receipt (report lines 3, 118).**
`grep -rl 812ee0d1 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/` → no output. Replay at
the tip reproduces both lines with `rev=812ee0d1…`, exit 0 each. Fix: R8 or commit the two files.

**DEFECT 5 — the census "107 rows" / "109 rows" claims cite receipts that print no row count and are
byte-identical** (`md5sum` both `12d1004ffa553a5825bfb426f31f06f0`). Fix: R10.

**DEFECT 6 — m9 gloss and the delta sentence overstate what closed (D1).** Fix: R2.

**DEFECT 7 — the residual 8 items and their reports are not in the committed tree at the tip (D2 of
§1 item 13).** `find .ufo/waves/round-41 -maxdepth 1 -type f` → four files, no `residual/`. Fix: R11
(the round is not closed until the 8 reports land).

**DEFECT 8 — contract C2 statement reads as a universal resolution rule (F5).** Contract's own
`declared_scope_limit` and `tools/context-capture.py:1682/1685` are the counterexample. Fix: R12.

**DEFECT 9 — "No axis is harmed" is universal over six axes, receipted for two (F4).** Fix: R9.

**PASS 1 — C1 receipts.** `before/c1-at-base.stdout` (exit 1) and `after/c1-at-2ae00eb7.stdout`
(exit 0) are byte-equal to the report; counter sha `9aaa99ac…` equals the pin; my base replay with the
pinned bytes reproduces the before block exactly; `records=3`, `sources_rows=107 → 109`.

**PASS 2 — m7 is not vacuous and is clean.** The three records cite `S001 S153 S154` (lesson) and
`S153 S154` (SCORECARD, LOG); all are `mined` in the 109-row registry at `2ae00eb7`.

**PASS 3 — m8 has no live counterexample.** Every backticked path-shaped token in the three records
resolves at `2ae00eb7` (`git cat-file -e` per token), including `considerthese/2026-10-24.md`.

**PASS 4 — C2 receipts and pins.** Tool `095924a7…`, fixtures `20b6254d…`, both counters and v2 match
their pins at `2ae00eb7`; the after/control/base lines are byte-equal to the report; `--control` exits 1
with the declared value.

**PASS 5 — mutant sensitivity.** All three mutants exit 1 on `FAIL planted …` assertion lines of their
own fixture class (not tracebacks), so the capability is load-bearing under this round's oracle.

**PASS 6 — live sites are as described.** 811: v2 site 1 / expected 0; 820: v2 site 0; both
`resolved_v3=1 scratch_v3=1`; direct v3 run shows the tmp-dir `expected.json` destination.

**PASS 7 — wave 1 shape.** `taskCall.tasks` 40, one batched call, `resumeSends []`, roles 1/6/8/7/10/5/3,
attack 18/40, 40 non-empty reports, settlement 40/40 with the `UNSETTLED detail=no seats` classification
reported as it stands.

**PASS 8 — sources and corpus artifacts.** S153/S154 rows (13 fields, tier A / docs / mined /
2026-10-25 / 180d), snapshot bytes and sha prefixes, titles, knowledge entry, README row, criterion 80,
quarantine slice (17 rows, 17 distinct ids, 15 not registry rows), round-40 lesson byte-untouched.

**PASS 9 — attempt-1 provenance as the report states it.** `.ufo/watchdog.log:1247` carries the exact
line and timestamp quoted.

No tool was installed or upgraded for this review (pacman paused host-wide; nothing needed).
