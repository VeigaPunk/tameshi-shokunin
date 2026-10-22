# DraftKnowledge — scribe seat report (round 25 wave 1)

Seat: TameshiR25.DraftKnowledge (scribe, leaf — no subagent dispatch).
Scope: draft the knowledge entry for `corpus/knowledge/mte-report-interop.md`
following the shape of `corpus/knowledge/hermetic-env-differential.md`
(`source:` header, `verified-at:`, `recheck:`, scope, bounds). Per bounds, only
this report file is written; the drafted entry text below is the DRAFT to be
landed by the L1 (TameshiR25) — not created by this seat.

Evidence surface: `tools/mte-interop.py` at committed revision `09dc114`
(tool sha256 `8c24255c9e482751772e958e5ba9a615891ca7e5dfc9426d2fb5667ceae65552`; the
working tree has uncommitted peer edits per `git status`, this report cites the
committed bytes).

## Executed evidence (this seat)

- Live C2 counter in a /tmp clone at `09dc114` (tool bytes `8c24255c…`):
  `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin`
  → `MTE_INTEROP: PASS legs_conforming=8/8`, exit 0, wall 122 s (first run) and
  128 s (second run, adding `--emit /tmp/dk-emit`). Per-leg lines (verbatim):
  - `bash-checklist-run`: CONFORMS, official_score=46.666666666666664,
    official_killed=7 official_survived=8 official_invalid=0 recorded=7/15,
    per_mutant=ok failed=none, runner_pct=47 official_rounded_half_up=47
  - `bash-mado-verify`: CONFORMS official_score=40 killed=4 survived=6 invalid=0 recorded=4/10 runner_pct=40 half_up=40
  - `bash-surface-census`: CONFORMS official_score=80 killed=8 survived=2 invalid=0 recorded=8/10 runner_pct=80 half_up=80
  - `bash-tsukuroi-census`: CONFORMS official_score=60 killed=6 survived=4 invalid=0 recorded=6/10 runner_pct=60 half_up=60
  - `js-claims-check`: CONFORMS official_score=70 killed=7 survived=3 invalid=0 recorded=7/10 runner_pct=70 half_up=70
  - `js-kimi-census`: CONFORMS official_score=80 killed=8 survived=2 invalid=0 recorded=8/10 runner_pct=80 half_up=80
  - `js-round-gate`: CONFORMS official_score=50 killed=5 survived=5 invalid=0 recorded=5/10 runner_pct=50 half_up=50
  - `js-sources-check`: CONFORMS official_score=50 killed=5 survived=5 invalid=0 recorded=5/10 runner_pct=50 half_up=50
- Selftest at the same committed bytes (copy + vendored tarballs in /tmp scratch):
  `MTE_SELFTEST: 16/16 pass`, exit 0.
- Emitted artifacts (`--emit`): 8 `<leg>.mte.json` (4 shell: checklist-run.sh,
  mado-verify.sh, surface-census.sh, tsukuroi-census.sh; 4 javascript:
  claims-check.mjs, kimi-census.mjs, round-gate.mjs, sources-check.mjs),
  8 `<leg>.spec` copies, `official-metrics.json`.
- Vendored integrity: schema package `package/src/mutation-testing-report-schema.json`
  byte-identical to GitHub master (sha256 `404575e926…`); both tarballs match
  `PACKAGES` sha512 pins and npm `dist.integrity` (verified this seat via `cmp`
  and `sha512sum`; corroborated by peer C2Integrity/C2SchemaSource).

---

# DRAFT — `corpus/knowledge/mte-report-interop.md`

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
and judges four checks per leg: `schema`, `ledger`, `per_mutant`, `score`
(`tools/mte-interop.py:230-258`).

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
  `mutationScoreBasedOnCoveredCode` is not claimed. No HTML report elements are
  validated. No producer authentication or promotion is claimed.

---

# Findings for the L1 (landing prerequisites)

1. The draft's `source:` header cites S001, S002, S086 and S087. The
   SOURCES.md rows S086/S087 (drafted by peer DraftSources, uncommitted) already
   set used-by = `corpus/knowledge/mte-report-interop.md`. Rows S001/S002 have
   used-by without that path; the kumitate sources-check will report
   `USED_BY_ASYMMETRY` (advisory) for S001/S002 unless their used-by cells are
   extended with `corpus/knowledge/mte-report-interop.md` in the same landing.
2. The S086/S087 used-by path does not exist on disk until the entry lands;
   the sources-check flags `USED_BY_MISSING` (error) in the interim. Land the
   knowledge file and the SOURCES.md rows together.
3. QUALITY 7 requires the new entry to land with its coverage-map row in
   `corpus/README.md` in the same round; the L1 should append the row (e.g.
   `| knowledge/mte-report-interop.md | F1 report interop; schema 3.9.0 + metrics 3.9.0 legal; 8/8 legs conform | tool sha256 8c24255c… |`).
4. The working tree `tools/mte-interop.py` currently differs from the committed
   `09dc114` (uncommitted peer edits: node check, leg-set check, MTE_WORKDIR
   print, tar member hardening). Receipts here cite the committed bytes; re-run
   the counter at the revision that lands.

Tooling record: no installs or upgrades performed (read-only tool runs via
`uv run --no-project --with jsonschema==4.25.1` in /tmp clones/scratch).
