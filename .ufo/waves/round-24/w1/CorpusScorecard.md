# CorpusScorecard — round-24 W1 critic (calibration)

Verdict: **two fixable defects, no blocking tradeoff.**

- The before→after claim is falsifiable and frozen before dispatch. The before receipt is byte-genuine.
- **D1 (premature capability row).** The capability row's "First-working round 24" landed before any after-measurement existed. Its evidence pointer, "`.ufo/evidence/round-24/` final receipts", names no file at the delivered revision.
- **D2 (numeric "stays 8" is unbacked at the delivered revision).** The only retained strict monitor measurement for round 24 shows calibration restraint **6** (47/62). The SCORECARD round-24 section neither records that harmed intermediate nor carries a restoring measurement.

The capability itself is demonstrated, but only by wave reports from other reviewers: RunRulerAfter measured 11/11 with exit 0, and RunSelftests measured 44/44 and 10/10. That is evidence from this wave, not a retained receipt.

## Axes named

1. Falsifiable before→after.
2. Frozen before dispatch.
3. Numeric score not inflated.
4. Capability demonstrated.
5. Provenance of the SCORECARD text itself.

## Evidence

### Axis 1 — falsifiable before→after: HOLDS

- `SCORECARD.md:1139-1143` states before 1/11, exit 1, at `6a1821a`, and gives the counting command `python3 .ufo/evidence/round-24/measure.py --repo CLONE_AT_REV`.
- `contract.json:7-14` fixes before 1/11 and target 11/11.
- `before.json` records `instrument_sha256 0a7f6daa…aa64`. The same hash comes from `sha256sum` of the working tree, `git show e338f1b:` and `git show c8c5b88:` for `measure.py`. `git diff --stat e338f1b c8c5b88` over `contract.json`, `before.json` and `measure.py` is empty, so the ruler is unchanged since freeze.
- **Strongest counterexample tried: was the before receipt hand-assembled?** It was not.
  - `/tmp/tameshi-r24-before-YdP3/lane` still exists. `git rev-parse HEAD` returns `6a1821a8897eea6e7d9669292160ec9593669409`, and `git status --short` is empty.
  - `jq -j .stdout before.json | cmp - /tmp/tameshi-r24-before-YdP3/out.json` prints `identical`, with sha256 `d7cf520e…5b5c`.
  - `out.json` mtime is 12:47:22 -0300, 18 s before the freeze commit `e338f1b` (12:47:40).
- The before rows are internally consistent with base:
  - K1–K4 have `anchor_count 1` at base, so the mutant anchors are base strings and were not fitted to the later implementation.
  - K5 and K6 have substituted `true` (no pins at base).
  - K7–K11 are `tool-absent`.
- After state: RunRulerAfter.md ran a private clone at `c8c5b88` with the same argv shape and got `discriminated 11, total 11`, exit 0, with every control and restored exit at 0.
- **Minor reproducibility gap (no axis harmed).** The counting command is written relative to the clone. At base the clone contains no `measure.py`: `git show 6a1821a:.ufo/evidence/round-24/measure.py` gives `fatal: … not in '6a1821a'`. Both before and after actually ran the frozen absolute-path blob against the clone. The instrument SHA pins it, but the SCORECARD wording does not say so.
- **Framing note.** K4 is counted in both the before and the target, so 1/11 → 11/11 is ten newly discriminated predicates plus one already-satisfied predicate. `SCORECARD.md:1140-1141` discloses this. The word "control" is loose, because the ruler's real controls are `control_exit` and `control_ok`. This is not an inflation.

### Axis 2 — frozen before dispatch: HOLDS for the claim; partial for the SCORECARD text

Order from `git log` and `stat`, all on 2026-10-21 (-0300):

| Time | Event |
|---|---|
| 12:47:40 | `e338f1b` freezes `before.json`, `contract.json` and `measure.py` (3 files) |
| 12:56:27 | `d2eaecd` implementation |
| 13:01:23 | `bd38c02` replay |
| 13:02:37 | `c8c5b88` re-anchors |
| 13:05:40 | `spec1.json` |
| 13:06:30 | `dispatch1-attempt1.json` |

`git merge-base --is-ancestor e338f1b c8c5b88` succeeds.

**Provenance asymmetry: the SCORECARD round-24 section was not part of the freeze.** `git show --stat e338f1b` touches no `SCORECARD.md`. The section (`SCORECARD.md:1127-1150`) was added in `d2eaecd` together with `tools/registry-replay.py`, the fixtures and the registry edits. Round 23's freeze commit `15ae602` did include `SCORECARD.md | 18 +`.

The section's substance matches the frozen contract: claim text, eleven predicate names, before, target and bounds. So this is a provenance-wording gap, not a moved goalpost. The sentence "landed at e338f1bd… before any build seat" is true of `contract.json` only.

### Axis 3 — numeric score not inflated: DEFECT D2

- `SCORECARD.md:1144`: "Numeric expertise stays 8 (delta 0)". No uplift is claimed (good).
- The lane's calibration scalar has been the strict cold-read monitor's `calibration_restraint_score` since round 17 (`SCORECARD.md:610`, "restraint 6 → … restraint 8").
- `.ufo/evidence/round-24/monitor-intermediate-A.json` was measured at `bd38c02` with `round-21/coldread/measure.py --rev bd38c02… --explain`.
  - Its stdout gives `"calibration_restraint_score": 6`.
  - Its note reads "harmed intermediate 47/62, restraint6 after round24 implementation edits".
- `c8c5b88` then appends 15 re-anchors: `source-prefix-preservation.json` shows 267 → 282 entries, prefix unchanged. But `.ufo/evidence/round-24/` has no post-re-anchor monitor receipt (no `monitor-current-*`, no `final-verification`).
- Counterexample:
  - The text "stays 8" was committed at `d2eaecd`. That is before the edits were re-anchored, when the monitor was (by the note's own attribution) harmed [INFERENCE: not separately measured at `d2eaecd`].
  - At the delivered revision the last retained measurement of the claimed axis is 6, not 8.
- Round 23 recorded every harmed intermediate in SCORECARD (`SCORECARD.md:1060-1063`, `:1100-1102`) and asserted "numeric 8→8" only beside a measured 62/62 (`:1105-1114`). Round 24 omits the intermediate and asserts 8 without a final measurement.
- The RunMonitor seat, assigned `--rev c8c5b88`, had not written `RunMonitor.md` when this report was written. If it measures 62/62 with restraint 8, D2 reduces to a missing retained receipt plus the unrecorded intermediate.

### Axis 4 — capability demonstrated: DEMONSTRATED (by wave), but row is DEFECT D1

The row is at `SCORECARD.md:1150`: `refusing-registry-replay | … | tools/registry-replay.py; .ufo/evidence/round-24/ final receipts | 24`.

**Premature.** The row was committed in `d2eaecd` (12:56:27), before the actual replay `bd38c02` and before any K1–K11 after-run. `.ufo/evidence/round-24/` at `c8c5b88` holds:
- `before.json`, `contract.json`, `measure.py`, `extra-cases.json`;
- `monitor-intermediate-A.json`;
- `replay-command.json`, `replay-gate.json` and `replay/*`;
- `source-*` files.

There is no after or final receipt for the eleven predicates.

The section itself says "Measured results are recorded below only after execution" (`:1145-1146`), and nothing is recorded below. Round 23's capability row was added only at `8f66b5d` ("retain executed registry replay…"), after execution. Round 24 inverts that convention.

**What is actually demonstrated:**
- RunRulerAfter.md at `c8c5b88`:
  - K7, K8 and K9 each exit 1 with `RUNNER_NOT_HELD`, `RUNNER_CLEANUP_FAILED` and `STREAM_LIMIT` respectively, with `bundle_written=false`.
  - K10 gives `live_dependent=["one"]`.
  - K11 has a realpath `fleet_root`.
- RunSelftests.md: `REGISTRY_REPLAY_SELFTEST: 10/10 pass` and `COMMAND_BINDING_SELFTEST: 44/44 pass`.
- `replay-command.json` (actual 43-row replay at `d2eaecd`) shows exit 0 with `refused_rows: []`, `live_dependent: ["pin-disposition-read","verify-round15"]`, `revision_pinned: 41`. `replay-gate.json` shows `finding_ids: []`, exit 0.

**Bound.** Refusal ("refuse to publish … from rejected/cleanup-failed/over-limit rows") is shown only on synthetic fixtures. The actual replay refused nothing. That matches `contract.json:63` ("K7-K11 test … synthetic fixtures; an actual replay run is separate evidence"), but the capability row does not state it. Live-dependent listing and fleet-plan identity are exercised on actual data.

## Impacted axes

- Numeric honesty (D2).
- Capability provenance (D1).
- SCORECARD↔freeze provenance wording (minor).

None of these move the frozen denominator or the 1/11 before.

## Smallest safe correction (append-only; routed to L1, not edited here)

1. Retain the after-run as a receipt in `.ufo/evidence/round-24/` with argv, cwd, revision `c8c5b88…`, exit, full stdout and `instrument_sha256 0a7f6daa…`. Append a "Round24 measured outcome" subsection under `SCORECARD.md:1146` recording 11/11 and exit 0.
2. Retain the strict monitor measurement at the final revision. Record both the harmed intermediate (47/62, restraint 6 at `bd38c02`, `monitor-intermediate-A.json`) and the final value. Assert "numeric 8→8" only beside a measured restraint 8, as round 23 did. If the final value is below 8, record a harmed axis rather than "stays 8".
3. Repoint the capability row's Evidence cell from "final receipts" to the concrete retained files. Add "refusal shown on synthetic fixtures; actual replay refused 0/43".
4. Optionally state that the counting command runs the frozen `e338f1b` blob by absolute path (`sha256 0a7f6daa…`) against `CLONE_AT_REV`, and that the SCORECARD section itself landed at `d2eaecd`, after the freeze.

## Scope and bounds compliance

- Read-only inspection only: `git log`, `show`, `diff`, `rev-parse`, `merge-base` and `status` with `GIT_OPTIONAL_LOCKS=0`, plus `sha256sum`, `jq`, `cmp` and `stat`. No ruler, selftest, registry battery or monitor was executed, because my item has no "Run".
- Wrote only this file. No production edits and no git or jj writes.
- No tools were installed or updated.
- Not claimed: producer authentication, promotion, historical R17-CMD-BIND closure, numeric uplift.
