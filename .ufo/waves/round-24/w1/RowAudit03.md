# RowAudit03 — round24 replay: six-row requirement / receipt / token audit

**Verdict: no false acceptance found in any of the six assigned rows.** Every requirement carried in
`observations.json` is exactly the round-23 frozen requirement; every published bundle receipt is
equal to the corresponding `runner_result` (exit, full stdout, stderr, argv, cwd, revision); every
required stdout token is present; `held: true` is justified by the runner's own formula. Two of the
six are red-by-design (exit 1 expected) and hold for the correct, specific reason — see the caveat.
No correction is required for these rows.

Scope: `repeat-control-selftest`, `evidence-disposition-round18-before`, `measure-round16-rev`,
`assemble-round17-selftest`, `receipt-measure-selftest`, `wave-accounting-wrong-count-entry`.
Replay revision `d2eaecd443bf5f4e387e7e5331282e3d11dea047` (clone
`/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`); delivered revision
`c8c5b88c8e961a929cdc351b95a7074c76958909`.

## Axes

1. Requirement fidelity — `observations.row.requirement` vs `.ufo/evidence/round-23/requirements.json`.
2. Receipt fidelity — `runner_result` exit / full stdout / held vs the published bundle receipt.
3. Token truth — do the required literals appear in the retained stdout, and do they mean what the
   row claims (not a banner on a failure path, not a different field)?
4. Execution provenance — pinned tools/inputs at the claimed revision.

## Method

Read-only. I did not execute any registry row, gate or selftest (lane bounds). Checks were: exact JSON
comparison, digest recomputation, static replication of `command-binding.py:evaluate`, and independent
recomputation of the two data-producing rows (`measure-round16-rev`, `wave-accounting-wrong-count-entry`)
from the `d2eaecd` blobs.

## Requirement fidelity (axis 1)

- `.ufo/evidence/round-23/requirements.json` blob sha256
  `cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3` is **identical** at
  `496d212`, `d2eaecd` and `HEAD` — the freeze was not touched in round 24.
- `.ufo/evidence/round-23/registry-baseline.json` sha256
  `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a` equals
  `requirements.registry_sha256`, equals `observations.registry_sha256`, and is byte-identical at all
  three revisions.
- The 43 frozen requirements equal, in order, the `status=="active"` rows of `tools/registry.json` at
  `source_revision` `28cae179e4dc2c1fa7f032a79cdddf0b5d862d76` (compared as full
  `{name,argv,expect}` dicts; 43/43 equal).
- `observations.rows[*].requirement` equals `requirements.json` **exactly for all 43 rows** (order
  preserved, zero diffs). For the six rows, the baseline row also equals the live `tools/registry.json`
  row and the `tools/registry.json` blob at `d2eaecd` on `argv`, `expect`, `kind`, `status`,
  `timeout_s` — the rows were neither superseded nor rewritten between the freeze and the run.

The six frozen requirements (verbatim):

| row | expect exit | required stdout literals |
|---|---|---|
| `repeat-control-selftest` | 0 | `SELFTEST: PASS` |
| `evidence-disposition-round18-before` | 1 | `"expectation": "producer_before"`, `"status": "failed"` |
| `measure-round16-rev` | 0 | `"calibration_restraint_score":`, `"coldread":` |
| `assemble-round17-selftest` | 0 | `SELFTEST: all checks passed` |
| `receipt-measure-selftest` | 0 | `RECEIPT_MEASURE_SELFTEST: 10/10 pass` |
| `wave-accounting-wrong-count-entry` | 1 | `TOTAL_MISMATCH`, `"completed": 66`, `"dead": 80` |

## Receipt fidelity and held (axis 2)

`registry-check.run_row` computes `held = got == expected_exit and not missing and cleanup_ok`
(`tools/registry-check.py:720`), where `missing` is the literal case-sensitive `stdout_contains`
set difference (`:718`). `registry-replay.project` refuses to publish on `cleanup_error`
(`tools/registry-replay.py:86`), on `held is not True` (`:89`) and on any stream over
`--max-stream-bytes` (`:96`, default 1 MiB; the largest retained stream here is 8,110 bytes).

Observed per row (from `observations.json` / `bundle.json`):

| row | expect | got | held | tokens present | full stdout | elapsed vs interval |
|---|---|---|---|---|---|---|
| `repeat-control-selftest` | 0 | 0 | true | 1/1 | 2,936 B | 1.374 s = 1.374 s |
| `evidence-disposition-round18-before` | 1 | 1 | true | 2/2 | 6,312 B | 0.327 s = 0.327 s |
| `measure-round16-rev` | 0 | 0 | true | 2/2 | 8,110 B | 0.326 s = 0.326 s |
| `assemble-round17-selftest` | 0 | 0 | true | 1/1 | 7,280 B | 0.555 s = 0.555 s |
| `receipt-measure-selftest` | 0 | 0 | true | 1/1 | 985 B | 1.933 s = 1.933 s |
| `wave-accounting-wrong-count-entry` | 1 | 1 | true | 3/3 | 965 B | 0.398 s ≈ 0.399 s |

Cross-checks over **all 43** rows, not only the six:

- Bundle receipt `stdout`/`stderr`/`argv`/`cwd`/`revision` are byte/field-identical to
  `runner_result`, and receipt `exit` equals `got`. Zero mismatches.
- All required tokens are present for all 43 rows; no row has `stdout_missing`, `cleanup_error` or
  `non_hermetic_argv`; `held` is true 43/43; exit distribution is 38×0, 5×1.
- I statically replicated `command-binding.py:evaluate` (`tools/command-binding.py:65-113`) against
  `bundle.json`: exact key sets, canonical absolute cwd, 40-hex revision, unique names, membership
  equality, and per-row argv/cwd/revision/exit/stdout-token equality all pass — the pristine gate's
  green is not an artifact of a skipped check. `bundle.json` sha256
  `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6` equals
  `replay/expected.json` and the `replay-gate.json` stdout; `replay-gate.json` exit 0,
  `finding_ids: []`.
- `replay-command.json` lists 43 per-row `name got held` lines that match the observations exactly;
  the 44th line is the report object. `replay-command.json` exit 0.

## Token truth per row (axis 3)

- **repeat-control-selftest** — stdout has 29 `SELFTEST_CASE … PASS` lines, 0 FAIL, then
  `SELFTEST: PASS (29 cases)`. The banner is conditional on `failed` being empty
  (`tools/repeat-control.py:854-860`). Its self-reported `tool-sha256=296fe566…bc25` equals
  `sha256(tools/repeat-control.py)` at `d2eaecd` and `HEAD`.
- **evidence-disposition-round18-before** — exit 1, top-level `"status": "failed"`, exactly one
  finding: `{ "id": "expected_contains_missing", "expectation": "producer_before" }`. The cause is
  genuine and specific: `round-13/expected.json.expected_checks.producer_before` requires the literal
  `summary preserves top-level exposed declaration kind`, and the frozen round-13 `producer_before`
  receipt's 1,938-byte stdout does not contain it (that run crashed: stderr ends in
  `FileNotFoundError … .ufo/evidence/tools/mutate-and-run.sh`). All 4 `dispositions-before.json`
  input digests match their `d2eaecd` blobs, and all 13 `round-13/expected.json` input digests match
  (`d2eaecd` for round-13 files, `4acc607d…` for the three historical tools). Self-reported
  `tool_sha256=39ee5c5e…51c8` equals `sha256(tools/evidence-disposition.py)` at `d2eaecd`. The
  round-18 `registry-full-e08271a.json` receipt for this same row also records `got 1, held true`,
  so this is the historical before-state failure, not a round-24 regression.
- **measure-round16-rev** — I recomputed the instrument from `git show d2eaecd:<path>` blobs by
  importing the tool's own functions and calling `measure('.', d2eaecd)`. Every field of the observed
  JSON is identical: `recorded_cases 8`, `depth_score 8`, 8 `ledger_legs`, `ledger_guardrail`,
  `shonen` (4 boxes, all `~`, `box3_full_page false`), `coldread` (28/62 covered, 34 uncovered
  headings), `calibration_restraint_score 6`, `sources` (83 rows: mined 54 / queued 23 / rejected 6;
  tiers A 74 / B 7 / C 2). Only `revision` differs — observed `"HEAD"`, recomputed `d2eaecd…` —
  because the row passes `--rev HEAD` and the tool echoes the argument. The row genuinely measured
  the `d2eaecd` tree, not a fixture.
- **assemble-round17-selftest** — 77 `[ok]` lines, no `FAIL`, final `SELFTEST: all checks passed`;
  the banner is conditional on an empty `failures` list (`.ufo/evidence/round-17/coldread/assemble.py:1792-1796`).
  All rejection cases carry their expected reason strings (`page-sha-mismatch`, `trace-rev-mismatch`,
  `external-input-lane`, `noncanonical-input`, …), and `check()` records any false condition as a
  failure before printing the banner (`:1008-1015`).
- **receipt-measure-selftest** — 10 `PASS [n/10]` lines, 0 FAIL, final `10/10 pass`; banner is
  conditional on `passed == total` (`tools/receipt-measure.py:299-300`). Self-reported
  `RECEIPT_MEASURE_RUNNER_SHA256 a67bffa9…1afa` equals `sha256(tools/receipt-measure.py)` at
  `d2eaecd`; `ROUND20_MEASURE_INSTRUMENT_SHA256 f34dc233…4e2d` equals
  `sha256(.ufo/evidence/round-20/stage/measure.py)` at `d2eaecd`.
- **wave-accounting-wrong-count-entry** — exit 1 with exactly one finding id, `TOTAL_MISMATCH`
  (`tools/wave-accounting.py:117` compares per-wave `claimed` vs observed counts). Recomputed from
  the bundle's own `outcomes`: wave1 28 completed / 43 dead / 71 seats, wave2 38/37/75, total
  66/80/146 — exactly the emitted `total`. The fixture is genuinely wrong by design: wave2 claims
  40/35/75 vs observed 38/37/75. `bundle_sha256 d984c49c…a17e` equals both the expected file and
  `sha256(.ufo/evidence/round-22/wrong-count-bundle.json)` at `d2eaecd`; the tool refuses on a
  digest mismatch before evaluating (`tools/wave-accounting.py:125-137`), so the `66`/`80` tokens
  are the observed totals, not an echo of the expected file.

## Execution provenance (axis 4)

- Every row's recorded `cwd` is the clone (`/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`)
  and every row's `revision` is `d2eaecd…`; `run_replay` verifies the clone's `HEAD` equals the
  requested revision and aborts otherwise (`tools/registry-replay.py:154-159`).
- `observations.runner_sha256_clone_copy cba16646…44ad` equals `sha256(tools/registry-check.py)` at
  `d2eaecd`. `replay-command.json` instrument digest `9fcd2dbb…8714` equals
  `sha256(tools/registry-replay.py)` at `d2eaecd` **and** `HEAD`. `replay-gate.json` tool digest
  `9230c68e…1d0d` equals `sha256(tools/command-binding.py)` at `d2eaecd` and `HEAD`.
- `live-dependent.json` = `["pin-disposition-read","verify-round15"]`, exactly the rows flagged
  `external: true` or `non_hermetic_argv` in the observations. None of the six is flagged, and none
  of the six carries an absolute fleet path in argv; the only hard-coded lane path reached by any of
  them is `assemble.py:569 LIVE_LANE_ROOT`, which is used for path classification and a
  clone-repo blob lookup, not a live-content read.
- `d2eaecd` is an ancestor of `c8c5b88`; `git diff --name-only d2eaecd c8c5b88` is 26 files,
  +6,019/−0, all under `.ufo/evidence/` (no tool, no `SKILL.md`/`SOURCES.md`, none of the six rows'
  input fixtures). Tool blobs are identical at both revisions, so the replay's tool bytes are the
  delivered bytes. [INFERENCE] the six rows would still hold at `c8c5b88` because each input path and
  tool blob is unchanged; their stdout is not all byte-identical across runs (`assemble-round17-selftest`
  generates fixture commits at run time), so only the acceptance — not the exact bytes — is claimed
  to transfer. The replay was not re-run at `c8c5b88`.

## Caveat — read `held` correctly

Two of the six expect a **nonzero** exit: `evidence-disposition-round18-before` and
`wave-accounting-wrong-count-entry`. `held: true` and the gate's `finding_ids: []` mean "matched the
declared expected failure", not "the command succeeded". Across the replay, 38 rows exit 0 and 5
exit 1: `repeat-control-snapshot-mismatch`, `evidence-disposition-round18-before`,
`context-capture-missing-env`, `context-capture-mapping-suffix`, `wave-accounting-wrong-count-entry`.
That is the frozen contract's semantics, not a false acceptance.

## Commands and observed output (read-only)

```
$ sha256sum .ufo/evidence/round-23/requirements.json
cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3
$ for rev in 496d212 d2eaecd HEAD; do git show $rev:.ufo/evidence/round-23/requirements.json | sha256sum; done
cd5205be…a1e3  (x3, identical)
$ python3  # requirement equality
requirements_equal_order: True ; n_rows: 43
$ python3  # receipt vs runner_result, all rows
receipt/observation mismatches: none ; all-token misses: none ; held: Counter({True: 43})
$ python3  # recompute round-16 measure from d2eaecd blobs via the tool's own functions
recorded_cases identical; depth_score identical; ledger_legs identical; ledger_guardrail identical;
shonen identical; coldread identical; calibration_restraint_score identical; sources identical;
revision: observed "HEAD" vs recomputed "d2eaecd…"
$ python3  # recompute wave-accounting totals from bundle outcomes
wave1 28/43/71 ; wave2 38/37/75 ; total 66/80/146  == emitted `total`
$ sha256sum .ufo/evidence/round-24/replay/bundle.json
4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6  == expected.json == replay-gate stdout
$ sha256sum tools/repeat-control.py tools/evidence-disposition.py tools/receipt-measure.py
296fe566…bc25 ; 39ee5c5e…51c8 ; a67bffa9…1afa  (equal to the tools' own banner digests)
$ git show d2eaecd:.ufo/evidence/round-20/stage/measure.py | sha256sum
f34dc233…4e2d  (equal to the receipt-measure banner constant)
$ git diff --name-only d2eaecd..c8c5b88 | wc -l
26  (all under .ufo/evidence/, +6019/-0)
```

## Residual limits / unresolved gaps

- Receipts are **declarations**: argv/cwd/revision are the invocation parameters the instrument passed
  to the runner, not observed process metadata, and neither tool authenticates a producer
  (`tools/registry-replay.py:17-21`, `tools/command-binding.py:8-15`). The independent digest and
  recomputation checks above raise confidence for these six but do not establish producer authenticity.
- `measure-round16-rev` echoes `--rev HEAD` instead of a resolved commit; its pinned-ness rests on
  the clone-checkout discipline in code (verified by reading, not re-observed). The recomputation
  against `d2eaecd` blobs matches the observed output, so the row read that tree.
- `assemble-round17-selftest` stdout is not byte-reproducible: its fixture commits are created at run
  time (`.ufo/evidence/round-17/coldread/assemble.py:1077-1084`) with current timestamps, so the revs
  differ between the round-23 run (`4fad5d40…`/`0e5efdab…`) and this one
  (`2ae68937…`/`14ad198b…`), as do tmpdir names. The bundle hash is therefore a per-run artifact; the
  required banner and its condition remain valid.
- No row, gate or selftest was executed by this audit; everything above is static comparison and
  independent recomputation over retained/git blobs.

## Smallest safe correction

None for these six rows. The only avoidable ambiguity is the `HEAD` echo in `measure-round16-rev`;
changing the frozen requirement to a resolved sha would be a new contract revision, not a round-24
correction, and is not needed for acceptance. Do not edit `requirements.json`, the observations, the
bundle or the expected file in this wave.
