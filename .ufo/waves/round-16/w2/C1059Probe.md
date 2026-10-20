# C1059Probe — wave-2 falsification: survivor C1059 (REPORT_MIN_BYTES 1024→1059)

**Verdict: C1059 holds as a *real* survivor — a suite blind spot, not an equivalent mutant.** A 1,040-byte report (inside [1024, 1058]) is CLEAN under the pristine gate and DRIFT/REPORT_THIN under the mutant: observable divergence, killable by a fixture the suite never builds.

## What was attacked

Sweep `results.tsv` (C1059 = SURVIVED, exit 0, predicted SURVIVED per spec line 35-37: "a single edit to any integer in [26,1059] changes no fixture verdict"). The suite's thinnest passing report is the selftest's big fixture (fxBigReport ≈ >1059 B) and its thinnest failing report is 25 B (`(bytes=25)` in check [4]); nothing lands in [1024, 1058], where the floor move flips `bytes >= REPORT_MIN_BYTES` (round-gate.mjs:345 vs :167).

## Method (all commands exercised, exits shown)

1. **Pristine materialization** — `git -C kumitate-shokunin show 364f1d59…:scripts/round-gate.mjs | sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` = pinned blob (spec header :2). PASS.
2. **Mutant re-cut** — `@old`/`@new` extracted from the C1059 block of `round-gate.defects.spec` at `c699c8c3` and applied by exact single-occurrence literal replacement (node; asserts hits==1). Mutant line: `167:const REPORT_MIN_BYTES = 1059;`.
3. **Fixture** — hermetic audit fixture (git identity/dates pinned, `env -i`): lane repo with SCORECARD.md (rows for round 5, `## Planned` round 6), LOG.md (`- 2026-01-02 — round 5 …`), commit `round-5 fixture seed`; main + origin repos; report `reports/round-5/kumitate.md` padded to exactly **1040 B** (verified `wc -c`).
4. **Runs** — `node <gate> --round 5 --repo lane --reports-dir reports --main-repo main --origin origin`.

## Results

| run | exit | finding lines |
|---|---|---|
| pristine (floor 1024) | 0 | `ROUND_GATE: CLEAN (round=5 lane=kumitate checks=10 errors=0 warnings=0)` — no REPORT_THIN |
| C1059 mutant (floor 1059) | 1 | `ROUND_GATE  error  REPORT_THIN  (bytes=1040)` + `ROUND_GATE: DRIFT (round=5 lane=kumitate checks=10 errors=1 warnings=0)` |

stderr empty in both runs. The mutant fails only the thin-report arm; all other 9 checks stay green — the edit is semantically reachable and distinguishable.

## Interpretation

- Survival is a **one-sided fixture-size hole**: the suite probes bytes ∈ {25, ~1560+} but never [1024, 1058]. The predicted interval [26,1059] (spec :34) is confirmed correct — 1059 survives only because no fixture report sits in the flipped band; the companion C1060 (floor 1060) dies on the same fixture at 1059 B. Adding one fixture with report ∈ [1024,1058] B kills C1059.
- Contrast with genuinely-equivalent arms (A2 reported-unread, B2 unreached species): C1059 is *reachable* behavior — the floor constant is consulted on every audit with a present report.

## Artifacts (lane paths)

- Probe script: `.ufo/evidence/round-16/round-gate/survivor-probes/c1059-probe.sh`
- Pristine log: `.ufo/evidence/round-16/round-gate/survivor-probes/c1059-pristine.log`
- Mutant log: `.ufo/evidence/round-16/round-gate/survivor-probes/c1059-mutant.log`
- Source lines: `round-gate.mjs:167` (floor), `:345` (`bytes >= REPORT_MIN_BYTES` → REPORT_THIN), spec `round-gate.defects.spec:35-37`.

Environment: node v24.21.0 (same as sweep); no installs needed; no blockers.
