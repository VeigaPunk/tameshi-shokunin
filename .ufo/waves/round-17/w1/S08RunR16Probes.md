# S08 — round-16 probes re-run at the round-17 lane tip

Seat: `TameshiR17.S08RunR16Probes` (scout, wave 1, round 17). Lane root
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, tip read
`98bea7da5801f4bc58e4187690ee1687c8a5061f` (`git rev-parse HEAD`, branch master).
Scope: execute the four round-16 probes, record exits and key fields. No lane
file outside this report was written; no tool was installed.

Method: live-lane runs as specified, plus an independent clone of the lane at the
tip (`/tmp/tameshi-r17w1-S08RunR16Probes-SdcdEe/lane`, checked out at the tip) to
prove the results come from committed bytes rather than the working tree. The
live worktree has two sibling-owned modifications (`.gitignore`,
`.ufo/evidence/round-16/round-gate/runner-sha256.txt`), neither produced or touched
by this seat; `measure.py --rev` reads blobs via `git show REV:path` only
(`.ufo/evidence/round-16/measure.py:4`), so they cannot affect the measurement.

## 1. Required probes (primary table)

All four were run from the lane root, commands as registered.

| # | Probe | Exit | Key fields observed |
|---|---|---|---|
| 1 | `python3 .ufo/evidence/round-16/measure.py --selftest` | **0** | `MEASURE_SELFTEST: 38/38 pass`; no FAIL lines |
| 2 | `python3 .ufo/evidence/round-16/measure.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f` | **0** | `revision=98bea7da…`; `calibration_restraint_score=8`; `depth_score=7`; `recorded_cases=7`; `coldread={ledger_present:true, box3_full_page:true, sections_covered:54, sections_total:54, missing:[], uncovered_headings:[]}`; `shonen={boxes:4, asserted:4, checked:0, untouched:0, marks:[~,~,~,~], box3_marked:true, box3_points:true, box3_ledger_link:true}`; `ledger_guardrail={header_legs:7, regression_calls:7, selftest_tuples:7, unique_recorded_gates:7, lists_agree:true}`; `sources={rows:55, malformed:0, status:{mined:28, queued:24, rejected:3}, tiers:{A:47, B:6, C:2}}` |
| 3 | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | **0** | 38 `[ok]` checks, 0 `[FAIL]`; final line `SELFTEST: all checks passed`; expected negative fixtures print `REJECTED`/`SKIPPED`/`WARNING` (bad-sha report, missing JSON block, class disagreement) and two rejected overrides, all as designed |
| 4 | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | **0** | `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)`; receipt line `.ufo/evidence/round-15/verification-3.json sha256=3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` |

Receipt integrity check for #4: `sha256sum .ufo/evidence/round-15/verification-3.json`
and `git show 98bea7d:…/verification-3.json | sha256sum` both return
`3c419055…d8ce`, equal to the sha the selftest prints. The selftest only reads and
prints; `reattribute.py` writes `correction.json` solely in its non-selftest path.

## 2. Reproducibility (retained records and committed bytes)

| Check | Exit | Result |
|---|---|---|
| `measure.py --rev <09ee1d0>` vs `.ufo/evidence/round-16/measure-09ee1d0.json` | 0 | byte-identical (`diff` empty); depth 7, calibration 8, 54/54 |
| `measure.py --rev <3490708>` vs `.ufo/evidence/round-16/measure-3490708.json` | 0 | byte-identical; depth 7, calibration 8, 54/54 |
| `measure.py --rev <28aeef4>` vs `.ufo/evidence/round-16/measure-28aeef4.json` | 0 | byte-identical; depth 6, calibration 6, **0/51**, `box3_full_page:false`, `ledger_present:false` (the retained pre-round red state) |
| `measure.py --rev 017a2b0…` (claim rev, no retained file) | 0 | depth 7, calibration 8, 54/54, box3 true — matches spotcheck §2's re-derivation |
| clone-at-tip `measure.py --rev 98bea7d… --repo <clone>` | 0 | byte-identical to the live-lane output of probe #2 |
| clone-at-tip `measure.py --selftest` | 0 | `38/38 pass` |
| clone-at-tip `assemble.py --selftest` | 0 | 38 `[ok]`, `SELFTEST: all checks passed` |
| clone-at-tip `reattribute.py --selftest` | 0 | `PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` |

So the three retained `measure-*.json` records reproduce byte-for-byte under the
tip instrument, and the tip result is unchanged when derived from a clone at the
tip. None of the four probes is flaky on this surface.

## 3. Exit contract observed at the live lane (secondary)

| Invocation | Exit | Terminal field |
|---|---|---|
| `measure.py` (no `--rev`) | 64 | `measure.py: error: --rev is required` |
| `measure.py --rev 0000…0000` | 2 | `{"error": "rev-missing", …}` |
| `measure.py --rev <tip> --bogus` | 64 | `unrecognized arguments: --bogus` |
| `assemble.py --selftest --bogus` | 2 | plain-argparse usage error (its own CLI, not the 64 convention) |

## 4. Calibration finding — the 8 is a sha-only false green

Probe #2 is green (exit 0, `calibration_restraint_score=8`), but it measures with
the round-16 rule that round 16's spot-check rejected, and that rule cannot see the
one stale bucket. Evidence:

1. The credited entry is the round-14 bucket. Recomputed from the tip blob with
   `measure.py`'s own `sectionize()`: 54 sections; the section at start 1563,
   heading `## Effective expectation reconciliation — round 14`, has
   `sha256:e8720037…`. Exactly one of the 75 ledger entries
   (`tameshi-coldread-ledger-v1`) matches that sha — `start:1563, end:1596,
   class:"instruction", verdict:"gap-minor", commands_executed_count:4,
   minor_gaps:1, blocking_gaps:0, wrong_expectations:0, seats:["CR26"]` — and
   `entry_credit_reason(entry)` returns `None` (credits).
2. The bucket's declared recipe steps 2–3 (`SKILL.md:1581-1586` at the tip) are
   run against `tools/mutate-and-run.sh`, which `.ufo/evidence/round-13/expected.json`
   pins at `75ed934d…`, while the runner at the tip is `0673d2e5…`. The
   registry row at `SKILL.md:1681` notes the exit-2 and offers `git archive
   28aeef4` as the workaround (a frozen commit, not the shipped tree); the
   recipe bucket at 1581-1586 states no such annotation and still credits.
3. Executed at the tip, both commands exit **2**:
   `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json`
   and the same with `dispositions.json` each return
   `{"id":"expected_input_digest_mismatch","status":"could_not_evaluate",
   "detail":"tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…",
   "tool_sha256":"1609a9df…"}`.
   (Spotcheck §2 marked the step-2 case `[INFERENCE]`; this run observes it.)
4. The round-16 ledger is v1: the union of entry keys is
   `blocking_gaps, class, class_votes, commands_executed_count, end, heading,
   minor_gaps, positions, reports, seats, sha256, skill_sha256, start, verdict,
   wrong_expectations` — **no `inputs` key on any of the 75 entries**. An
   instruction entry with executed commands therefore has no input record to
   re-verify.
5. The 38-case selftest has no input-drift case. Its guards are
   `bytechange-*` (the section's own bytes change), `nocmd-*` (instruction entry
   with 0 executed commands), `instr-verified-nocredit`, `record-credited`,
   `wrongbox-*`, `nolink-*`; none models "section bytes stable, an executed lane
   input drifted".

Consequence: at the tip the round-16 instrument cannot distinguish the stale
round-14 bucket from a live one. Its `calibration_restraint_score: 8` and
`box3_full_page: true` must **not** be carried into round 17 as evidence for C1;
they are exactly the red-before material the round-17 input-keyed rule must turn
into an uncredited bucket (`inputs-unrecorded` for this v1 ledger, or
`input-drift:tools/mutate-and-run.sh` once inputs are recorded). Under the
corrected reading the round-16 restraint remains 6, as the spotcheck §2/§3 found.

## 5. Bounds and integrity

- Gate runs above are read-only (`run_mode` only emits); the gate's only
  `rmtree`/scratch use is in `--selftest` (`tools/evidence-disposition.py:1853-1855`).
- Post-run `git status --porcelain=v1 --untracked-files=no` shows only the two
  pre-existing sibling modifications; this seat added no tracked change.
- No `jj`, no git writes in the lane; the only clone is under
  `/tmp/tameshi-r17w1-S08RunR16Probes-SdcdEe` (checked out at the tip).
- Scratch: `/tmp/tameshi-r17w1-S08RunR16Probes-Rx3yLb/out/` (measure JSONs,
  clone outputs, gate JSONs) and the clone dir above.
- Tooling installed/updated: none.

**Verdict: holds — all four round-16 probes run and pass at the tip, but the `calibration_restraint_score: 8` they emit is a sha-only false green (R16-C2b), not evidence for round-17 C1.**
