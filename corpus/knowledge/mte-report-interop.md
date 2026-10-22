source: S001 — https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ — §Mutant states and §Metrics, page fetched 2026-10-19; S002 — https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json — MutantStatus enum and MutantResult shape, master fetched 2026-10-19; S086 — npm mutation-testing-report-schema 3.9.0 (integrity-pinned tarball in tools/vendor/, `package/src/mutation-testing-report-schema.json` member); S087 — npm mutation-testing-metrics 3.9.0 (integrity-pinned tarball in tools/vendor/, `package/src/model/metrics.ts` and `package/src/calculateMetrics.ts` members)
verified-at: 2026-10-22; C2 counter executed at 09dc114 (tool sha256 8c24255c…): PASS 8/8, exit 0; selftest 16/16, exit 0; official metrics per leg observed (lines in `.ufo/waves/round-25/w1/DraftKnowledge.md`)
recheck: uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest; uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin; reopen S002, S086 and S087; compare the located quotes in lessons/round-25.md
ground: F1 — external mutation-score semantics + report interop; the report-interop half of F1 moves to Core (schema acceptance + official metrics scoring of emitted ledger-leg reports). The score equality is by construction and is a sanity check, not an independent measurement.

# MTE report interop — tameshi ledger legs as mutation-testing-elements reports

## What the interop does

`tools/mte-interop.py --check` replays the eight recorded mutation-ledger legs
via `tools/mutate-and-run.sh --regression` (at the committed revision, or an
existing kept workdir via `--workdir`), emits one mutation-testing-elements
report per leg, validates it against the vendored official schema 3.9.0
(draft-07, python `jsonschema`), computes the official metrics with the
vendored `mutation-testing-metrics` 3.9.0 library (node `calculateMetrics`),
and judges four checks per leg: `schema`, `ledger`, `per_mutant`, `score`.
`ledger` compares the official killed, survived, invalid and total counts with
the runner's own REGRESSION_TABLE line; `per_mutant` compares every emitted
status with the committed recorded verdict of the same defect id in the
runner's TABLE_* lines. Those two are the checks that can fail on real data;
`score` is a sanity check that holds by construction. The leg set must be
exactly the eight ledger legs, or the run is SETUP (exit 2).

### Mapping: tameshi verdict → MTE report fields

| tameshi verdict | MTE `status` | `statusReason` |
|---|---|---|
| KILLED | Killed | tameshi verdict KILLED |
| SURVIVED | Survived | tameshi verdict SURVIVED |
| INCONCLUSIVE | RuntimeError | tameshi verdict INCONCLUSIVE |

(`tools/mte-interop.py:69`, `:152-157`.) The report is emitted per leg as:

- `schemaVersion: "1"` (matches the schema pattern `^([1-2])(\.(([1-9]\d*)|0)){0,2}$`);
- `thresholds: {high: 80, low: 60}` — required by the schema; both are integers
  0..100 (`:159`);
- `framework: {name: "tameshi mutate-and-run.sh"}` (`:160`);
- `files: {<target-basename>: {language, source, mutants}}` where
  - `source` = the pristine pinned target bytes, materialized from the repo's
    git object store by the runner;
  - `language` = from the target suffix: `.mjs`/`.js` → `javascript`,
    `.sh` → `shell`, `.py` → `python`, else `plaintext` (`:70`, `:158`);
    the eight legs are 4 shell + 4 javascript;
  - one mutant per recorded defect: `id` = defect id, `mutatorName` =
    `tameshi-hand-seeded`, `description` = defect description, `replacement` =
    the `@new` string, `location` derived from the defect's unique `@old`
    string, `status`/`statusReason` per the table above (`:152-157`);
  - `location.start` = 1-based line/column of the first byte of `@old`;
    `location.end` = 1-based line/column just past it (end-exclusive, matching
    the schema's "Start is inclusive, end is exclusive"). The `@old` string
    must occur exactly once in the pristine target; otherwise the leg is
    refused as SETUP, not judged (`:149-150`, `:126-129`).

## What the official schema and metrics library check

### Schema (S086; vendored 3.9.0, member `package/src/mutation-testing-report-schema.json`)

Root requires `schemaVersion`, `thresholds`, `files`; `thresholds` requires
`high` and `low` (integers 0..100); each file entry requires `language`,
`source`, `mutants`; each mutant requires `id`, `mutatorName`, `location`,
`status`; `status` must be one of the eight-value enum
(Killed/Survived/NoCoverage/CompileError/RuntimeError/Timeout/Ignored/Pending);
`location` requires `start` and `end`, each a position whose `line` and
`column` are integers ≥ 1; the `mutants` array has `uniqueItems: true`. The
tool validates with `jsonschema.Draft7Validator` (no FormatChecker), so the
single `format: uri` in `framework.homepageUrl` is not enforced; the schema
does not check locations against `source` or the truth of `statusReason`.
`S002` is the same schema file on GitHub master (byte-identical to the
vendored src member: sha256 404575e926…); `S086` pins the released 3.9.0 npm
package, which is what the tool validates against.

### Metrics (S087; vendored 3.9.0, `mutation-testing-metrics`)

`calculateMetrics(report.files)` counts mutants by status and computes
(`package/src/model/metrics.ts:39-42,50-58,69-73`; `package/src/calculateMetrics.ts:234-255`):

- `totalDetected = timeout + killed`;
- `totalUndetected = survived + noCoverage`;
- `totalValid = totalUndetected + totalDetected`;
- `totalInvalid = runtimeErrors + compileErrors`;
- `mutationScore = totalValid > 0 ? totalDetected / totalValid * 100 : NaN`;
- `mutationScoreBasedOnCoveredCode = totalDetected / totalCovered * 100`
  (`totalCovered = totalDetected + survived`), `0` when no coverage;
- `totalMutants = totalValid + totalInvalid + ignored + pending`.

The tool reads `mutationScore`, `killed`, `survived`, `totalValid`,
`totalInvalid`, `totalMutants` (`:81-85`, `:85`). The library only scores; it
does not validate the report against the schema (that is the separate
`jsonschema` step).

## INCONCLUSIVE and Timeout semantics

Tameshi's INCONCLUSIVE is "no definitive verdict": runner exit 124 (timeout),
126 (suite not executable), or 127 (suite not found)
(`tools/mutate-and-run.sh:539-541`); per `SKILL.md:208-212` it is not a kill
and is excluded from the kill-rate denominator (`killed/(killed+survived)`).
Mapping it to MTE `RuntimeError` makes the official library count it as
`totalInvalid` and exclude it from `totalValid` and the score. With no Timeout
and no NoCoverage mutants, the official score then equals
`killed/(killed+survived)*100` — tameshi's rate — by construction. Mapping the
exit-124 sub-case to MTE `Timeout` instead would count it as *detected*
(`totalDetected = timeout + killed`; S001: Timeout "is counted as 'detected'"),
making the official score `(k+t)/(k+s+t)`, which diverges from tameshi's rule
whenever `t > 0` and `s > 0`. The INCONCLUSIVE→RuntimeError mapping is
therefore a convention that preserves tameshi's arithmetic, not an equivalence
to Stryker semantics: the bucket also includes 126/127, and the report cannot
distinguish the sub-cases (`results.tsv` columns 1–2 only).

## Integer-percent rounding of the ledger

The runner's headline kill-rate is an integer percent:
`pct=$(( (200 * killed + total) / (2 * total) ))` at
`tools/mutate-and-run.sh:562`, where `total` is the number of spec defects
(`:499`) — round-half-up of `100·killed/total`. The interop judge and
`SKILL.md:210` use `killed/(killed+survived)`; these coincide only when
`inconclusive = 0` (true for all eight ledger legs). The recorded ledger
percentages are integers, e.g. `bash-checklist-run` 7/15 = 46.67 % is recorded
as 47 % (runner header `:90`; `SKILL.md:1103,1316`). The official score is a
float — for `bash-checklist-run` it is `46.666666666666664` (observed) — so
"official score equals the ledger's recorded percentage" is false for such a
leg; equality holds only against the unrounded fraction. The tool prints
`runner_pct` and `official_rounded_half_up` side by side as information; at
09dc114 the half-up rounding is `(200*k + k + s) // (2*(k+s))`, i.e.
round-half-up of `100·k/(k+s)` (`:321-334`).

## Executed result

At `09dc114` (tool sha256 `8c24255c…`): `MTE_INTEROP: PASS legs_conforming=8/8`,
exit 0 (wall 122–128 s); selftest 16/16, exit 0. Official metrics observed
(killed/survived/score): js-kimi-census 8/2/80; bash-surface-census 8/2/80;
bash-tsukuroi-census 6/4/60; bash-mado-verify 4/6/40; bash-checklist-run
7/8/46.666666666666664; js-claims-check 7/3/70; js-round-gate 5/5/50;
js-sources-check 5/5/50. Every leg conformed on all four checks with
`per_mutant=ok` and `failed=none`.

## Reuse boundary

- The reports are validated against the *released* 3.9.0 schema and scored by
  the *released* 3.9.0 metrics library (sha512-pinned in `tools/vendor/`);
  a new release or an offset pin requires re-verification.
- The score equality is by construction under the 1:1 mapping; it is a sanity
  check, not an independent measurement (round-25 wave seat C2Tautology).
- The interop proves nothing about how Stryker would mutate these targets or
  score the same code; it is a format/score-semantics interop of tameshi's
  own ledger records.
- `INCONCLUSIVE→RuntimeError` is a tameshi convention, not a Stryker status
  equivalence; Timeout-as-detected is explicitly not adopted.
- No NoCoverage claim: the reports carry no `coveredBy`/`killedBy`, so
  `mutationScoreBasedOnCoveredCode` is not claimed; NoCoverage classification of
  the 35 recorded survivors stays open as frontier F1b. No producer
  authentication or promotion is claimed.
- The official web component (`mutation-testing-elements` 3.9.0) rendered all
  eight emitted reports headless with no errors and computed the same scores
  (round-25 seat C2HtmlRender). It is schema-lenient: a bogus status loads and
  is silently dropped from the tally. So the HTML consumer cannot replace the
  schema check; it only shows the reports are usable by the official viewer.

## Decision table — exporting a tameshi sweep as a report

| tameshi verdict | MTE status | in `valid`? | counts as detected? | why |
|---|---|---|---|---|
| KILLED | Killed | yes | yes | S001 Killed; S087 `totalDetected = timeout + killed` |
| SURVIVED | Survived | yes | no | S001 Survived; never NoCoverage without coverage data |
| INCONCLUSIVE (exit 124/126/127) | RuntimeError | no | no | keeps tameshi's `k/(k+s)`; Timeout would count as detected (S001) |

Error patterns the selftest pins (`tools/mte-interop.py --selftest`):
`tameshi-vocabulary-status` (KILLED is not a schema status), `line-zero-location`
(positions start at one, S086), `timeout-is-not-a-tameshi-kill`,
`balanced-flip-same-counts` (counts agree but ids are swapped: only the
per-defect check against the recorded table sees it), `survived-as-nocoverage`.
