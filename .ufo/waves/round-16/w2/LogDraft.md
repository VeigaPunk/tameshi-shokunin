# LogDraft — round 16 wave 2 (depth + calibration; LOG entry falsification)

Lane: tameshi-shokunin · Subject commit: `c699c8c36d6e4eca4b796b81a8247904aa145ec8` · Chain: `28aeef4` → `0baf52e` → `e69b488` → `c699c8c`
Scratch: `/tmp/tameshi-r16w2-LogDraft-4wrZpD` (all runs below are from committed bytes copied there; no lane file written except this report)
Tooling: no installs or updates. Used pre-existing `python3` and `node v24.21.0`, `git`, `bash`.

## Verdict

**PARTIAL.** The depth/source/sweep claims hold on re-execution. The cold-read box-3 claim (SHONEN "full page") falls: the ledger it cites is absent at every commit. Calibration does not move (6 → 6).

## Draft LOG.md entry (for the integrator; not written to LOG.md)

```markdown
## Round 16 — seventh recorded case; cold-read ledger not yet committed (2026-10-20)

- Pre-registration precedes execution: `e69b488` (10:39:59 -0300) commits
  `.ufo/evidence/round-16/round-gate/predictions.json` (`registered_at_utc`
  2026-10-20T13:39:42Z), `round-gate.defects.spec` and `suite.txt` before the
  sweep (`MUTATE_DATE` 13:40:15Z) and the regression (`REGRESSION_DATE`
  13:41:49Z). `c699c8c` (10:49:37 -0300) lands the results.
- Seventh measured mutation leg: kumitate `scripts/round-gate.mjs` at
  `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` (blob sha256 `f890e277…d3e9`),
  10 defects, KILLED 5 / SURVIVED 5, kill-rate 50%. All 10 predictions match
  `sweep/results.tsv`. Ledger comment `tools/mutate-and-run.sh:85-91`.
- Counts, same command before and after
  (`python3 .ufo/evidence/round-16/measure.py --rev REV`, exit 0 each):
  recorded cases / depth 6 → 7; calibration restraint 6 → 6; sources rows
  49 → 55 (tier A 42 → 47, B 5 → 6, C 2 stable; mined 22 → 28, queued 24,
  rejected 3; malformed 0). `SOURCES.md:61-66` are S052–S057 (S057 tier B).
- Cold-read box 3 is NOT credited. `.ufo/evidence/round-16/coldread/ledger.json`
  is not in any commit; `measure` reports `ledger_present: false`,
  `sections_covered: 0/54`. SHONEN box 3 stays `[~]`. Pending: run
  `assemble.py` over committed seat reports and commit `ledger.json`; the
  dry run below shows partial coverage.
- Tool bytes changed after the sweep: the sweep receipt names
  `mutate-and-run.sh` sha256 `75ed934…` (the `e69b488` bytes); `c699c8c` edits
  the tool to `89722ddb…` to add the js-round-gate leg. Re-execution under
  `89722…` reproduces the same 5/10 verdicts.
- Lane verdicts: depth improved (+1 measured leg); calibration unchanged
  (scalar 6); sources expanded (+6 rows, all mined). No promotion, no SHONEN
  box changed.
```

## Claims checked and evidence

| # | Claim in draft | Re-execution / evidence | Result |
|---|---|---|---|
| C1 | seventh leg, 10 defects, 5/10 killed | `bash mutate-and-run.sh --target round-gate.mjs --defects round-gate.defects.spec --suite "$(cat suite.txt)"` on the pinned blob → exit 0, `CONTROL: GREEN`, `MUTATE: DONE (target=round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)`, `MUTATE_RESTORE: OK` | HOLDS |
| C1a | predictions precede execution | `predictions.json` `registered_at_utc` 13:39:42Z < `e69b488` commit 10:39:59 -0300 (=13:39:59Z) < sweep `MUTATE_DATE` 13:40:15Z (`sweep/sweep.log:2`) | HOLDS |
| C1b | 10/10 predictions match | python compare of `predictions.json` vs `sweep/results.tsv` → `predictions_matched 10 killed 5 kill_rate 5/10` | HOLDS |
| C1c | pins | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| sha256sum` = `f890e277…d3e9` (matches `runner-regression.txt` `REGRESSION_PIN` and `round-gate.defects.spec` header) | HOLDS |
| C1d | regression replay | committed `round-gate/runner-regression.txt`: `REGRESSION: PASS (cases=7 passed=7 …)`, `rc=0`. Re-run (fleet-layout scratch, see note): `regression exit=0`, `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`, 133.7 s | HOLDS |
| C1e | tool selftest | committed `runner-selftest.txt`: `MUTATE_SELFTEST: 81/81 pass`. Re-run: `selftest exit=0`, `MUTATE_SELFTEST: 81/81 pass`, `VERDICT: PASS` | HOLDS |
| C1f | sweep receipt names the tool that ran | committed `sweep/sweep.log:1` `MUTATE_TOOL … sha256=75ed934…`; `git show e69b488:tools/mutate-and-run.sh \| sha256sum` = `75ed934…`; `git show c699c8c:tools/mutate-and-run.sh \| sha256sum` = `89722ddb…` (matches `runner-sha256.txt`). The sweep receipt is faithful to the bytes it ran; the tool changed later in the same landing commit | HOLDS as receipt; tool changed post-sweep (see F2) |
| D1 | depth 6 → 7 | `measure.py --rev 28aeef4` → `depth_score 6, recorded_cases 6`; `--rev c699c8c…` → `depth_score 7, recorded_cases 7, ledger_legs [..., 'js-round-gate']`; both exit 0 | HOLDS |
| D2 | calibration unchanged | both revs `calibration_restraint_score 6` | HOLDS (no gain) |
| S1 | sources +6 (S052–S057) | `measure` rows 49 → 55; A 42 → 47; B 5 → 6; C 2; mined 22 → 28; `git diff e69b488 c699c8c -- corpus/SOURCES.md` shows 16 insertions and 1 deletion (`--stat`); the six new rows are `SOURCES.md:61-66` | HOLDS |
| M1 | measure self-test | `python3 measure.py --selftest` → `MEASURE_SELFTEST: 33/33 pass`, exit 0 | HOLDS |
| B3 | cold-read box 3 full-page ledger | `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` → `does not exist` (exit 128); `git log --all --diff-filter=A -- .ufo/evidence/round-16/coldread/ledger.json` → 0 commits; `measure` → `ledger_present false`, `sections_covered 0/54`, `box3_full_page false` | FALLS (F1) |
| B4 | SHONEN box-3 link | `SHONEN.md:9` box line `- [~] Instructions executable…`; `SHONEN.md:10` continuation carries `(.ufo/evidence/round-16/coldread/ledger.json)`; the link target does not exist | FALLS (F1) |
| B5 | assembler selftest | scratch copy of `coldread/assemble.py` → `--selftest` exit 0, `SELFTEST: all checks passed` | HOLDS (tool only) |
| B6 | assembler on committed seat reports | dry run only (scratch, not committed): `assemble.py --skill .ufo/evidence/round-16/coldread/SKILL.snapshot.md --skill SKILL.md '.ufo/waves/round-16/w1/*.md' --out …/ledger-dryrun2.json` → exit 1, `coverage: 51/65 sections covered`, 36 `SKIPPED … no closing ```json block found` lines on stderr. Uncovered headings include post-page round-16 sections: `## Context gate classification … round 15`, `## Errata — round 16 full-page cold-read (append-only)`, `## Seventh recorded case and full-page cold-read — round 16`, `### Round-16 gate/probe registry` | PENDING / PARTIAL (not a commit; see F1) |

## Findings

**F1 — cold-read box-3 claim is unsupported at `c699c8c` (falls).**
SHONEN box 3 (`SHONEN.md:9-10`) and `measure.py` both point at `.ufo/evidence/round-16/coldread/ledger.json`. That file is absent from every commit. `CRLedger.md` (w1) describes `assemble.py` as writing it on run, and no run output is committed. `measure.py` gives `box3_full_page: false`, `sections_covered: 0/54` on the committed SKILL.md (sha256 `3d8a1edb…`). The scratch dry run covers 51 of 65 combined buckets from the committed w1 reports with no w2 reports committed (`w2/` is untracked in the working tree, `git status` `?? .ufo/waves/round-16/w2/`). Round-16 post-page sections have no covering entry. The draft entry must not claim full-page coverage.

**F2 — sweep receipt and tool bytes differ by one commit (holds as receipt; disclosed in draft).**
`sweep/sweep.log` names tool `75ed934…`, the `e69b488` bytes. `c699c8c` changes the tool (`git diff e69b488 c699c8c -- tools/mutate-and-run.sh`: header lines 11-14, 85-91 ledger comment, `--regression` leg list, embedded js-round-gate spec). Criterion 20 in `corpus/QUALITY.md` (round-16 append) says an instrument is not edited during the wave that uses it. This is inference from the bytes: the edit lands in the same commit as the results, after the sweep ran. Re-execution under `89722…` gives the same verdicts, so the measured result does not depend on which bytes ran. The draft discloses the difference.

**F3 — `measure.py` `box3_ledger_link` is line-based (measurement limitation, inference).**
`BOX_RE` matches one line (`measure.py` `shonen_boxes`, `box3_link = BOX3_LINK in boxes[2][1]`). The link sits on `SHONEN.md:10`, not on the box line, so `box3_ledger_link` and `box3_points` read false even when the ledger exists. Even with the ledger, the restraint score would not rise until this is fixed. Not changed by me (out of lane, read-only).

**F4 — regression run exit 2 on first attempt (scratch layout, resolved; not a finding against c699c8c).**
The tool derives `FLEET_ROOT` from three `dirname`s of its own path (`mutate-and-run.sh:1163`). Running from `/tmp/…/mutate-and-run.sh` resolved to `//kumitate-shokunin@…` and returned `REGRESSION: SETUP (cases=7 passed=0 cannot-verify=7)`, exit 2. Re-run with the tool at `<scratch>/fleet/tameshi-shokunin/tools/` and read-only symlinks to the four sibling repos (`kumitate`, `kagi`, `tsukuroi`, `mado`) gave exit 0, `PASS (cases=7 passed=7)`. Symlinks were used only for `git show` reads; no fleet tree was written.

## Commands and key outputs (condensed)

```
python3 measure.py --rev 28aeef4            -> exit 0  depth 6  recorded 6  restraint 6  sources 49 (A42 B5 C2; mined22 queued24 rejected3)  ledger_present false  sections 0/51
python3 measure.py --rev c699c8c…           -> exit 0  depth 7  recorded 7  restraint 6  sources 55 (A47 B6 C2; mined28 queued24 rejected3)  ledger_present false  sections 0/54
python3 measure.py --selftest               -> exit 0  MEASURE_SELFTEST: 33/33 pass
bash mutate-and-run.sh --selftest           -> exit 0  MUTATE_SELFTEST: 81/81 pass  VERDICT: PASS
bash mutate-and-run.sh --target round-gate.mjs --defects round-gate.defects.spec --suite "$(cat suite.txt)" -> exit 0
   CONTROL: GREEN; A1 K, A3 K, B1 K, E3 K, C1060 K, C1059 S, A2 S, B2 S, CKIND S, E1 S
   MUTATE: DONE (target=round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
   MUTATE_RESTORE: OK
bash mutate-and-run.sh --regression --workdir … (fleet layout) -> exit 0  REGRESSION: PASS (cases=7 passed=7)
node round-gate.mjs (pinned) --selftest     -> ROUND_GATE_SELFTEST 60/60 (per sweep.log)   [not separately re-run]
assemble.py --selftest                      -> exit 0  SELFTEST: all checks passed
assemble.py … w1 glob (scratch dry run)     -> exit 1  coverage 51/65  (not committed)
```

Pins verified: `SKILL.md@c699c8c` sha256 `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (matches the page pin); `SKILL.md@e69b488` = `SKILL.snapshot.md` = `97cf436b…` (the pre-page in `assemble.py`'s `skill_pins`); `round-gate.mjs@364f1d5` = `f890e277…`; `tools/mutate-and-run.sh@c699c8c` = `89722ddb…`; `tools/mutate-and-run.sh@e69b488` = `75ed934…`.

Committed-file evidence pointers:
- Draft entry facts: `e69b488` (predictions, spec, suite, w1 reports), `c699c8c` (results, sweep log, regression, tool edit, SOURCES S052–S057, PROVINCE.md round-16 append, QUALITY.md criteria 18–20, `corpus/lessons/round-16.md` present, 68 lines).
- Sweep: `.ufo/evidence/round-16/round-gate/sweep/{sweep.log,results.tsv,defects.tsv}`, `round-gate/predictions.json:1-80`.
- Regression: `.ufo/evidence/round-16/round-gate/runner-regression.txt` (9 lines of PASS, `rc=0`), `runner-sha256.txt`.
- Counting: `.ufo/evidence/round-16/measure.py` (`BOX_RE`, `box3_points` at :263), `.ufo/waves/round-16/w1/CRMeasure.md`.
- Cold read: `.ufo/evidence/round-16/coldread/{assemble.py,SKILL.snapshot.md}`, `.ufo/waves/round-16/w1/CRLedger.md`; no `ledger.json`.
- Attribution: `.ufo/evidence/round-16/attribution/{correction.json,correction-attrfix-draft.json,reattribute.py}` present; **not re-verified here** (pending).

## Pending / not measured

- `coldread/ledger.json`: not produced or committed; full-page coverage unmeasured in committed bytes.
- Attribution correction (`reattribute.py`, `correction.json`): not re-executed.
- Round-16 `w2/` seat reports: untracked in the lane working tree, not in any commit; not used.
- Node pinned selftest and `round-gate` ROUND_GATE 60/60 not re-run separately (taken from committed `sweep.log`).
- Lane working tree is dirty (`M .ufo/waves/round-16/w1/Overlap1.md`, untracked `w2/`, `.ufo/evidence/round-16/Overlap1/`); not part of any cited claim.

## Contract notes

- No commits, no `git add`, no edits to lane files. Writes: this report only. Scratch under `/tmp/tameshi-r16w2-LogDraft-4wrZpD`.
- Sibling repos read via `git -C … show` only (kumitate). Symlinks in scratch only.
- No messages sent to `agent://TameshiR16` (no blockers beyond F1, which is a finding for the integrator, not a blocker to this task).
