# C1/C2 separability critique — wave 2, read rev 01d586ddbc5fcd78659557c4e93a6ee8517b87d1

Axes: **depth (C1)** vs **operability (C2)**. Question under attack: does C1's
measurement verify with C2's commits reverted, and does C2's verify with C1's
reverted? Builds on `.ufo/waves/round-18/w1/R08Separability.md` (verdict: falls,
one-way coupling — C2's registry no-harm re-runs C1). All work in
`/tmp/tameshi-r18w2-CriticSeparability-UNgBbd/fleet/tameshi-shokunin` (clone at
read rev); lane tree untouched.

## Commit ownership map (who owns which blob)

| Commit | C1 content | C2 content | shared files? |
|---|---|---|---|
| 93d22aa | C1 pre-registration (spec, predictions, control, suite) | — | no |
| aee4f36 | — | C2 ruler v1 (`defect-probes.py`, base receipt) | no |
| 58e5d53 | leg 8 in `tools/mutate-and-run.sh`, `mutation-case-kumitate-sources-check.md`, SKILL entry, spec/sweep evidence | fixes in `tools/evidence-disposition.py`, `tools/registry-check.py`, `tools/bash-witness-study.py`; promoted `tools/trace-inputs.py`; `dispositions*.json`; SKILL probe table | **no** — both land in `SKILL.md` but disjoint sections; no file carries both claims' bytes |
| e08271a | — | `tools/registry.json` rows only | no |
| 01d586d | — | ruler v2 + receipts (8-line diff to `defect-probes.py`) | no |

Key fact: `tools/mutate-and-run.sh` changed **once** between `183f87b` and tip —
blob `980d9551` → `fd1a63a3` in `58e5d53`, unchanged at `e08271a`/`01d586d`.
All 14 hunks of that diff are leg-8 only: header ledger line (`#   js-sources-check
… 5/10`), `PIN/REV_SOURCESCHECK`, `TABLE_SOURCESCHECK`, the verbatim
pre-registered spec heredoc, the eighth `regression_case_git` call,
`nlegs` 7→8, and selftest leg-count arms 7→8. No C2 fix touches the runner
(`git diff 58e5d53^ 58e5d53 -- tools/mutate-and-run.sh`, 14 `@@` hunks inspected).

## Direction 1 — C1 with C2 reverted: VERIFIED, measured

Command D (`SCORECARD.md:72-73`) is a pure function of one blob:
`git show $REV:tools/mutate-and-run.sh | regex-count`. Reverting C2 changes
zero bytes of that blob.

Measured — synthetic commit `c787b37226a32ec74ef40403eff52009f27c2d10` in the
/tmp clone: restored `tools/registry-check.py`, `tools/evidence-disposition.py`,
`tools/bash-witness-study.py`, `tools/registry.json` to `183f87b` blobs and
removed `tools/trace-inputs.py`, `defect-probes.py`, `measure.py`,
`git-env-canary.py`, `coldread/` (all C2/kit files), keeping leg 8:

```
git show c787b372:tools/mutate-and-run.sh | python3 -c '<command-D regex>'
→ recorded_cases=8 depth_score=8          (exit 0)
git rev-parse c787b372:tools/mutate-and-run.sh = fd1a63a3 = tip blob
```

`--regression` likewise: `mutate-and-run.sh` contains no reference to any C2
tool (grep `trace-inputs|registry-check|evidence-disposition|bash-witness|
defect-probes` → only the literal `python3` interpreter at `:307,455,1280` and
two spec-comment mentions). Leg 8 replays `node sources-check.mjs --selftest`
against the kumitate object store — fully inside C1's own machinery.

## Direction 2 — C2 with C1 reverted: VERIFIED, input-identical

The C2 ruler probes exactly five lane files: `evidence-disposition.py` (P01,
P02, P08), `registry-check.py` (P03, P04, P09, P10), `trace-inputs.py` (P05,
P06, P07), `bash-witness-study.py` (P11), plus the round-17 trace-inputs copy
as a fallback anchor (`defect-probes.py:53-103, 335-401`). The only runner
touch is `runner_rev()` at `defect-probes.py:809-815,831` reading the
`REV_BASH=` pin for the P11 kagi fixture — and `REV_BASH` is
`fecee8743e52eb8fb5fbb40782934cb619a1a96e` at `183f87b`, `58e5d53`, and tip
(runner `:595`/`:600`; leg 8 did not move it).

Measured — synthetic commit `e0c1b2d26e8415de55288372499784c71fa241cb` (runner
restored to `183f87b`, case-8 corpus entry removed, everything else kept):
all five probe-input blobs **byte-identical** to tip
(`git rev-parse $SYN:$f == 01d586d:$f` for each; `grep` for
`sources-check|TABLE_SOURCESCHECK` in every probe-read file → no hits).
`command D` correctly reads `7` at that commit. Guard probes mutate the tool
under test and run **its own** `--selftest`; P08/P09/P10 fixtures are synthetic
(manifest written into the jj fixture, registry rows fabricated by
`registry_text`/`timeout_row`); P11 recomputes the runner sha into a *fresh*
declaration each run. With inputs byte-identical and no probe reading
leg-8 state, `open=0/11` is unchanged at the synthetic revert — deterministic,
not [INFERENCE], modulo environment (jj on PATH; P11 kagi clone source).

Also checked and dismissed: the stale-looking `runner` sha in
`.ufo/evidence/round-12/BashWitness/declaration.json`
(`75ed934…` vs actual `d22c4025…`) — but `cmd_count`
(`bash-witness-study.py:1051-1128`) never reads the live runner; only
`cmd_check`/`facts` do (`:569,1156`), and no active registry row runs `check`.
`dispositions.json` mentions "mutate-and-run" only in prose, not a pinned row.

## Finding 1 — commit-level non-separability (fixable attribution defect)

C1 and C2 share `58e5d53`. `git revert 58e5d53` removes **both** claims'
payloads, so strictly commit-level "C1 verifies with C2's commits reverted" is
unsatisfiable — the wave can only answer at hunk level. This is exactly what my
synthetic commits did, so the evidence above stands; but the round's own
narrative ("C1 measured by command D; C2 by defect-probes") should note the two
claims share a landing commit, since a judge that reverts commits cannot
isolate them. Fixable next round: land claim-scoped commits.

## Finding 2 — R08's one-way coupling confirmed at landing rev (tradeoff, not a defect)

C2's cited no-harm evidence (`registry full 32/32 held at e08271a`) still runs
`mutate-and-run-selftest` and `mutate-and-run-regression` (tip
`tools/registry.json`, argv `bash tools/mutate-and-run.sh --selftest` /
`--regression`, 180s/900s — rows byte-identical to `183f87b`). So C2's "no
harm" result **bundles C1's machinery**: a broken leg-8 pin/table would turn
the no-harm monitor red even with all 11 probes closed. The ruler itself
(`defect-probes`) is separable; the no-harm aggregate is not, by design.
R08 called this correctly and it persists at tip — it is a monitoring tradeoff
(registry covers the runner it must also protect), not a ruler defect. One new
data point: the regression row's 900s timeout was not raised when leg 8 was
added — it passed (32/32 at e08271a) but the budget now absorbs a 10-mutant
ninth-ish leg's worth of extra runtime.

## Verdict

partial — measurement-level separability holds both directions (command D=8
survives full C2 reversion, measured at synthetic c787b372; all defect-probes
inputs byte-identical under C1 reversion at synthetic e0c1b2d), but C1 and C2
are not commit-separable (shared landing 58e5d53) and C2's no-harm claim
remains coupled to C1 through the registry's mutate-and-run rows, exactly as
R08 found.
