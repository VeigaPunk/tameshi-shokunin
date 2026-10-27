# Round 25 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)
Runtime model as exposed to this session: `anthropic/claude-opus-5-5`.
Date: 2026-10-22. Base `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`, head
`f4e8f7d835a8e33c64a87ff93e79da32264f031c`. Report
`.ufo/reports/round-25/tameshi.md` (fleet `0888a12dd3c37366940aea08db820c09cd9a299f`).
I did not author round 25. The attempt-1 private trees under
`/fast/scratch/hyaku/tameshi-r25-author*` were not read. Only committed bytes
were judged. No reviewer seats were dispatched: every check below was run by me.

Driver digest (copied from `.ufo/watchdog.log`):

```
2026-10-21T20:38:07-03:00 launch tameshi round=25 pgid=2906730 driver=hyaku-inline attempt=1
2026-10-22T04:58:59-03:00 lane-dead-no-report tameshi round=25; retry same round (hyaku-inline attempt=1: superseded at 2026-10-22T04:56:36-03:00: stale 2026-10-21/22 author; fresh attempt)
2026-10-22T05:02:58-03:00 launch tameshi round=25 pgid=7349 driver=hyaku-inline attempt=2
2026-10-22T06:42:00-03:00 complete tameshi round=25; hyaku-inline attempt=2
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-25/tameshi.md` (fleet) | `tameshi-shokunin 0888a12d…` | pass |
| `SHONEN` heading, one line per box | report `## SHONEN`; `grep -cE '^- \[[ x~]\]' SHONEN.md` | 4 report lines, 4 boxes, all `[~]` | pass |
| cited hashes exist and are ancestors | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for the 9 round commits + base | 10/10 ok | pass |
| lane pushed, clean | `jj-lane.sh state`; `git status --porcelain` | `local=remote=f4e8f7d… ahead=0 behind=0 tracked=0 untracked=0`; 0 lines | pass |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/tameshi-round-25.md) templates/round-prompt.md` | only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions; §6 hyaku addendum follows | pass |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | exit 0; `ok`; seven W04 duplicate-url warnings (S047, S048, S075–S078, S081), all older rows | pass |

Report is real (9 commits, receipts). Status `ok`.

## Claims — re-check

### C1 calibration — routed-item dispositions, 0/3 → 3/3 (record repair)

Re-measured by plain counts. The kill tallies are verified from evidence, not
re-run: they execute the lane gate `tools/command-binding.py`
(§Gate standard, Closure consequence).

| What | Command (lane repo) | Observed |
|---|---|---|
| record rows, base vs head | `git show <rev>:SCORECARD.md \| grep -cE '^\| R23-ROUTED-[123] \| dispositioned \|'` | base 0, head 3 |
| routing source | `jq -r '.rounds[421].notes' MANIFEST.json` (fleet) | contains "multi-token stdout fixture in the ruler, re-run guard sweep, and dead-falsifier coverage gap" (tameshi r23, admitted) |
| R3 population identity | dead seats in `.ufo/waves/round-23/original-outcomes2.json` (`status!="completed"`) vs `dead-falsifier-disposition.json` names | 30 completed / 34 failed; name sets equal (34) |
| R3 statuses and reports | `jq -r '.rows[].status'`; each `report` exists at head and holds `R23-REATTACK <name>: AGREE\|FINDING` matching its status | 20 agree, 14 finding; 34/34 report tokens match |
| R2 anchors verbatim | `@old` lines of G1–G4, G9–G14 vs `.ufo/evidence/round-23/mutate.py:13-22` | 10/10 round-23 anchors present verbatim |
| defect ids | `grep -oE '^@defect [MG][0-9]+'` both specs | M1–M10, G1–G14 (24) |
| frozen counter unchanged | `git log --format=%h 1f73157..f4e8f7d -- .ufo/evidence/round-25/c1-measure.py`; sha256 | only `2a97ec1`; `b18460c7…` = contract `measure_sha256` |
| evidence: kills | `after/c1-measure.stdout` tail | `C1_ROUTED: dispositioned=3/3`; R1 `defects=10 killed=10`, R2 `defects=14 killed=14`, control green, restore OK; R3 negative controls both fail as required |
| evidence: pins | `after/c1-pins.stdout` | `C1_PINS: HOLD (0 failures)`, 10 pinned files |

Verdict: **verified, calibration improved** (three record-vs-routed-state
mismatches → 0). The numeric score stays 8, as declared. Known bound, disclosed
by the lane: the frozen counter accepts a row that reads "NOT dispositioned".
At head every row reads exactly `| dispositioned |`, so the bound does not
affect this measurement.

### C2 coverage capability — `tools/mte-interop.py` absent → PASS 8/8, selftest 17/17

The C2 counter replays sibling gates, so I did not run it. I re-derived its
after-state from the committed emitted reports with my own validator.

| What | Command | Observed |
|---|---|---|
| before | `git cat-file -e 1f73157:tools/mte-interop.py` | `exists on disk, but not in '1f73157'` |
| reports present | `ls .ufo/evidence/round-25/mte-reports/*.mte.json \| wc -l` | 8 |
| schema acceptance | registry-downloaded 3.9.0 schema, `uv run --no-project --with jsonschema==4.25.1` + `validator_for` (Draft7) over the 8 committed reports | `errors=0` ×8, `VALID 8/8` |
| per-mutant identity | per leg, sorted `id:status` from the report vs `TABLE_*` in `tools/mutate-and-run.sh:613-620` (KILLED→Killed, SURVIVED→Survived) | 8/8 legs `per_mutant=equal`; 85 mutants (15 + 7×10) |
| official score arithmetic | (Killed+Timeout)/(valid)·100 per S087 | 46.67, 40, 80, 60, 70, 80, 50, 50, equal to `after/c2-check.stdout` |
| tool frozen since measurement | `git log 1f73157..f4e8f7d -- tools/mte-interop.py`; sha256 | last change `77302fa`; `8269b82f…` = amendment-3 `tool_sha256` |
| evidence: counter and selftest | `after/c2-check.stdout`, `after/c2-selftest.stdout` | `MTE_INTEROP: PASS legs_conforming=8/8`; `MTE_SELFTEST: 17/17 pass` |
| capability row | SCORECARD round-25 section | `mutation report interop` row, first-working round 25 |

Verdict: **verified, coverage improved** (capability acquisition; frontier F1
report interop moves to Core). Re-measured: schema 8/8, per-mutant 8/8, scores.
Evidence-verified only: the live replay counter and the 17/17 selftest.

### Amendments versus the after-measurement

- Amendment 2 is `09dc114` (05:35 −03). Amendment 3 lands in `77302fa`
  (06:26), the measured commit itself. The recorded after receipts arrive in
  `154bf4d` (06:35). They were produced by the amendment-3 bytes: the
  `MTE_WORKDIR` line, the 17th selftest case `narrow-score-delta`, and c1-pins
  P5's exact row shape are all amendment-3 additions. **Both amendments precede
  the recorded after-measurement.**
- Wave seats had already run the C2 counter at PASS 8/8 at `c9ff09f` and
  `09dc114` (`w1/C2LiveCheck.md`, `w1/DraftKnowledge.md:168`). That was before
  amendments 2 and 3, under the weaker ruler. For C1, every pre-amendment run
  read 0/3 (`w1/C1BeforeRerun.md`, `w1/MeasureMutants.md`). Neither amendment
  moved a target, a population or the frozen counter's bytes. Each one only
  adds refusals, which makes a pass harder. So this is not post-hoc narrowing.
  The JSON flag `before_any_after_measurement: true` is accurate for the L1's
  recorded measurement but not for seat probes (routed item 2).

## No-harm at head

`git diff 1f73157 f4e8f7d -- SCORECARD.md`: append-only (+56/−0), and no axis
score row changed. The lane's other edits are also append-only (`--numstat`):
LOG +19, PROVINCE +10, QUALITY +20, README +22, SOURCES +16, all −0. SKILL.md
is untouched.

**Cold-read monitor harm and restore — ruling.** The retained receipts show
62/62 restraint 8 at base. They show 45/62 restraint 6 at `77302fa` and at
`154bf4d`, and 62/62 restraint 8, depth 8, overrides false at `3b20f07`. I
re-derived the restore by plain checks:

- The ledger diff is append-only (768 insertions, 0 deletions). Its first 287
  entries equal base as data, and its other keys are unchanged (`jq -S` diff).
- The 17 appended headings equal the 17 `uncovered_headings` of
  `monitor-harmed-154bf4d.json`.
- All 162 (path, sha256) inputs recorded by the 17 entries match the bytes at
  head.
- No file changed between `3b20f07` and head (7 paths) is a traced input of any
  ledger entry, so the 62/62 carries to head.

Ruling: the restore is **valid no-harm evidence for the input-keyed monitor**.
It is the same instrument, under the same credit rule, as the base 62/62. That
base itself carries earlier author re-anchors (precedent:
`round-19-verifier-spotcheck.md:133`), and the drift came from pure appends.
It is **not** evidence of independent comprehension. The 17 entries are the
author's scripted byte reads under `strace`, not cold reads. SHONEN box 3
therefore stays `[~]`. No owned axis is harmed at head.

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured (record 0→3, population identity 34/34) |
| coverage | improved | C2 re-derived (schema 8/8, per-mutant 8/8) |
| depth | unchanged | monitor depth 8 = base; no new recorded case; SKILL.md untouched |
| operability | unchanged | `registry-final-3b20f07.json` held 47/47, superseded 7; the new tool is unregistered (routed item 1) |
| freshness | unchanged | S002 master bytes re-verified today (below); no re-pin claimed |
| adjacency | unchanged | `w1/SiblingOverlap.md` reports no contested scope; sibling repos read-only |

## Discernment spot-check

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| `corpus/knowledge/mte-report-interop.md` (decision table: INCONCLUSIVE→RuntimeError, outside `valid`; Timeout would count as detected) | admit | registry tarball `mutation-testing-metrics-3.9.0.tgz`, `package/src/model/metrics.ts:39-58`, `calculateMetrics.ts:237-253` | agree | `totalInvalid = runtimeErrors + transpileErrors` and `totalDetected = killed + timed out`, so mapping INCONCLUSIVE to RuntimeError keeps k/(k+s). My scores equal the entry's. |
| `dead-falsifier-disposition.json` | admit | `.ufo/waves/round-23/original-outcomes2.json`, 34 `w1/Re*.md` reports | agree | Name sets are equal (34), and every status matches its report's `R23-REATTACK` token. |
| "guard sweep 14/14 = guard adequacy" | reject | `w1/MtGuardGaps.md:1-20`; `guard-mutants.spec` | agree | The spec's 14 defects are guard-disable edits (`if False:` / `pass`). The seat reports 17 of 64 semantic weakenings surviving the 44-case selftest at target sha `9230c68e…`, so 14/14 cannot measure guard strictness. |
| "official score = tameshi kill rate as independent measurement" | reject | `tools/mte-interop.py` mapping; my per-mutant comparison | agree | A 1:1 status map makes score equality hold by construction. The informative checks are `ledger` and `per_mutant`, and I re-derived per-mutant independently. |

New SOURCES rows (83 → 85; S086, S087, tier A, mined, used by the new entry):

- **S086.** I fetched `https://registry.npmjs.org/mutation-testing-report-schema/3.9.0`
  and the tarball. The download's sha512 equals `dist.integrity`, and that
  equals the vendored `tools/vendor/…-3.9.0.tgz`. The quote at
  `package/src/mutation-testing-report-schema.json:92`
  (`"enum": ["Killed", … "Pending"]`, 9 tokens) is exact. The second quote,
  "Position of a mutation. Both line and column start at one." (11 words), is
  at `:309`, not cited by line in the lesson. The schema sha256 `404575e9…`
  equals the GitHub master file that S002 tracks (fetched today).
  **Agree.**
- **S087.** Same procedure, and the integrity check is equal. Both quotes,
  `metrics.ts:70-71` (17 words; the source has a trailing comma after the
  formula) and `:40-41` (15 words), are exact and ≤25 words. **Agree.**

## Trend verdicts

- **expansion: improved.** One new admitted entry on frontier ground F1 (README
  F1 status correction, PROVINCE Core append). It cites two new mined tier-A
  rows whose integrity and quotes I re-opened, and a capability row entered
  SCORECARD with a passing demonstration that I re-derived.
- **quality: improved (narrow).** The README F1 status is superseded by a
  stronger held statement. The S002 ground of `mutation-score-semantics.md`
  re-verifies (byte-identical today). 34 dead round-23 falsifiers were re-run:
  20 agree, and the 14 findings are marked in the lesson. Rulers gained
  M7–M10 and the ten verbatim round-23 anchors. No admitted entry failed my
  re-check.
- **discernment: improved.** My spot-check agrees with both admits and both
  rejects. The round-24 outside disagreement
  (`round-24-verifier-spotcheck.md:34,37`) became the lesson-cited QUALITY 50,
  and its fix is shown able to fail (c1-pins drop-one-row → FAIL).

Claim sizing: 2 claims on distinct axes. Each after-state is one value from
one command over an enumerated population (3 labels; 8 legs, with leg-set
equality enforced by amendment 3). The calibration claim counts mismatches
rather than asserting. No universal clause is unenumerated. No target was
narrowed after landing. **Compliant.** The learning claim (C2 plus an admitted
entry) is met.

SHONEN: all four boxes `[~]`. None is fully checkable by a non-author yet. Box 3
rests on author re-anchors, and boxes 1, 2 and 4 lack an independent promotion
review. Promotion is operator-owned.

## Routed defects — the lane fixes these next round

1. `tools/mte-interop.py` is a verdict tool (exit 0 PASS, 1 FAIL, 2 SETUP;
   `--selftest`) with no registry row at its registry home (`SKILL.md`; also
   absent from `tools/registry.json`). This is a §Gate standard Registry
   conformance defect and is status-neutral.
2. The SCORECARD round-25 header and the lesson's `## Claims` name only
   amendments 1–2. Amendment 3 (in `77302fa`) appears only in its JSON and the
   report. Its `before_any_after_measurement` flag also omits that seats saw
   C2 PASS 8/8 at `c9ff09f`/`09dc114`. Append a correction; do not rewrite.
3. `knowledge/mte-report-interop.md` `verified-at` records the `09dc114` run
   (tool `8c24255c…`, selftest 16/16), not the measured tool `8269b82f…`
   (17/17). Refresh it.
4. Still open from the lane's own routing: MtGuardGaps' 17 surviving
   weakenings, 14 re-attack FINDINGs, round-24 spot-check items 2–4, and
   emitted reports that name targets without a lane/revision pin
   (SiblingOverlap).
5. Seat bounds: ReReplay14 ran `jj log` at the fleet root, and ReOutputComplete
   ran `jj st` in the lane. Wave contexts must name `jj` beside git.

Installs: none. Ephemeral `uv run --no-project --with jsonschema==4.25.1`
(PyPI, uv cache) for the schema check. The npm tarballs were fetched into
`/fast/scratch/hyaku/r25close-c2/` for re-opening only.
