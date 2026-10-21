# RowAudit02 — round24 replay: six-row requirement/receipt audit

**Verdict: no false acceptance found in any of the six assigned rows.** For each row the
requirement carried in `observations.json` is byte-identical to the round-23 freeze, the receipt
(`runner_result`) reports `got == expect`, `held: true` with no cleanup error and no missing
token, and every required stdout token is present. An independent gate (`command-binding.py`)
re-derives the same binding from the published bundle and returns `finding_ids: []` against a
digest-pinned bundle. Residual notes below are latent brittleness that this run did not exercise;
none of them changes today's acceptance.

Scope: rows `repeat-control-snapshot-mismatch`, `evidence-disposition-round18`,
`mutate-and-run-regression`, `measure-round17-selftest`, `receipt-window-selftest`,
`wave-accounting-selftest`. Replay revision `d2eaecd443bf5f4e387e7e5331282e3d11dea047`; delivered
revision `c8c5b88c8e961a929cdc351b95a7074c76958909`.

## Axes

1. Requirement fidelity — `observations.row.requirement` vs `.ufo/evidence/round-23/requirements.json`.
2. Receipt fidelity — `runner_result` exit / full stdout / held (and bundle receipt congruence).
3. Binding semantics — does `held: true` actually mean "exit matched and all tokens matched"?
4. Provenance — was the run made with the frozen inputs, on the pinned tool blobs, at the claimed revision?

## Method and provenance chain

- Frozen requirement file: `.ufo/evidence/round-23/requirements.json` sha256
  `cd5205be9e5843e956191f673e620875f6f9c65a4c8ed9f224e656601a25a1e3`; registry baseline
  `.ufo/evidence/round-23/registry-baseline.json` sha256
  `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a` — equals
  `requirements.json.registry_sha256`. Both files are byte-identical at `d2eaecd`,
  `c8c5b88` and in the worktree.
- `run_replay` refuses on a baseline digest mismatch and on `requirements != active baseline rows`
  (`tools/registry-replay.py:140`, `:145`), and re-checks clone HEAD (`:158`). The 43 frozen
  requirements equal the 43 `status=="active"` rows of `registry.json` at `source_revision`
  `28cae179e4dc2c1fa7f032a79cdddf0b5d862d76` and at `496d212bc46789cdf8cafab72978bdb7f4182963`
  (compared as full row dicts; zero differences).
- `d2eaecd` is an ancestor of `c8c5b88`; `git diff --name-only d2eaecd c8c5b88` lists only 26
  files, all under `.ufo/evidence/` (+6019/−0). No production file changed, so the replay at
  `d2eaecd` exercises the delivered code.
- Tool identity: self-reported banner digests match the `d2eaecd` blobs exactly — repeat-control
  `296fe566…`, mutate-and-run `d22c4025…`, evidence-disposition `39ee5c5e…`. The clone runner
  `tools/registry-check.py` `cba16646…` equals `observations.runner_sha256_clone_copy`; the replay
  instrument `9fcd2dbb…` equals `replay-command.json.instrument_sha256` and the `d2eaecd` blob.
- Every row interval equals its reported `elapsed_s` to 0.000 s, intervals do not overlap, and all
  sit inside the recorded run window 15:56:41–16:01:02Z. The clone path
  (`/tmp/tameshi-registry-replay-dzo3ypiq/...`) is unique to this run.

## Per-row result

| row | requirement (frozen) | got / held | tokens | decisive receipt evidence |
|---|---|---|---|---|
| `repeat-control-snapshot-mismatch` (`requirements.json:26`) | `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch`, exit 1 | 1 / true | 0 required | `SNAPSHOT_INPUTS 9 verified` ×1, `SNAPSHOT_EXPECTED id=controls_mismatch exit=1`, `SNAPSHOT_OBSERVED id=controls_mismatch exit=1`, final line `REPEAT_CONTROL: controls_mismatch` |
| `evidence-disposition-round18` (`requirements.json:149`) | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json`, exit 0 | 0 / true | 3/3 | `"status": "clean"` ×1, `"effective": 11` ×1, `"superseded": 1` ×1 (JSON `counts.effective=11`, `counts.superseded=1`); full 6909-byte stdout retained, stderr empty |
| `mutate-and-run-regression` (`requirements.json:273`) | `bash tools/mutate-and-run.sh --regression`, exit 0 | 0 / true | 1/1 | 8 `REGRESSION_CASE … PASS`, 0 `FAIL`; final `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`; measured-killed == recorded-killed for all eight legs (8/10, 8/10, 6/10, 4/10, 7/15, 7/10, 5/10, 5/10) |
| `measure-round17-selftest` (`requirements.json:389`) | `python3 .ufo/evidence/round-17/measure.py --selftest`, exit 0 | 0 / true | 1/1 | 94 `PASS` lines, 0 `FAIL`; tally `MEASURE_SELFTEST: 94/94 pass (scratch /tmp/tameshi-r17-MeasureV2-zrg9esoz)` |
| `receipt-window-selftest` (`requirements.json:501`) | `python3 tools/receipt-window.py --selftest`, exit 0 | 0 / true | 1/1 | 20 `PASS [` lines, 0 `FAIL [`; tally `RECEIPT_WINDOW_SELFTEST: 20/20 pass`. The 11 literal `FAIL` occurrences are expected-classification labels on PASS lines ("is refused — FAIL") |
| `wave-accounting-selftest` (`requirements.json:622`) | `python3 tools/wave-accounting.py --selftest`, exit 0 | 0 / true | 3/3 | `ACCOUNTING_SELFTEST: 8/8 pass`, `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`, `FINDING: SELFTEST_PASS`; 24 ` ok` case lines, 0 ` FAIL` |

Requirement equality was checked on the whole object (`argv`, `expect`, `name`), not just the name:
all six `observations.row.requirement` objects compare equal to their `requirements.json` entries
(observations rows at lines 116/125, 492/501, 870/879, 1229/1238, 1581/1590, 1946/1955).

## Binding semantics (why `held: true` is not self-vouching)

- `tools/registry-check.py:720`: `held = got == expected_exit and not missing and cleanup_ok`.
  Held therefore carries the **all-tokens** check (`missing` is every required token absent from
  stdout) plus descendant cleanup. For all six rows `cleanup_error` and `stdout_missing` are absent.
- `tools/registry-replay.py:89-91`: any `held is not True` becomes `RUNNER_NOT_HELD` and no bundle is
  published. The run reported `held True` for all 43 rows on the console receipt
  (`replay-command.json` stdout, 43 `name got True` lines, including all six).
- Independent re-binding: `tools/command-binding.py:104-112` recomputes
  `ARGV_MISMATCH`, `CWD_MISMATCH`, `REVISION_MISMATCH`, `EXIT_MISMATCH`, `STDOUT_MISMATCH`
  (`any(token not in stdout)`). `replay-gate.json` records exit 0, `finding_ids: []`,
  `bundle_sha256 4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`, identical to
  `replay/expected.json`. Bundle receipts match the observations byte-for-byte on `stdout`/`stderr`
  and on `exit == got` for the six rows.

## Falsification attempts

1. **Exit-only row could accept a crash (`repeat-control-snapshot-mismatch`).** Refuted:
   `tools/repeat-control.py:893` catches every exception and routes it to `setup_failure`
   (exit 2); `EXIT_BY_ID` (`:122-130`) reserves 1 for `controls_mismatch` alone. The receipt also
   shows the matched-record branch (`SNAPSHOT_EXPECTED`/`SNAPSHOT_OBSERVED` both
   `controls_mismatch/1`), so exit 1 is a genuine mechanism result, not a setup error.
2. **Weak prefix token could mask a partial selftest** (`measure-round17-selftest`). Refuted by
   exit coupling: `measure.py:1447` returns 1 when `passed != len(checks)`; the same holds for
   `receipt-window.py:348` and `wave-accounting.py:193` (non-zero frozen-measure code is preserved,
   extra-case failure returns 1 and prints `SELFTEST_FAIL` instead of the required token).
3. **Substring superset acceptance.** Real but unexercised: tokens are containment checks, so
   `"effective": 11` would also match `"effective": 110`, `"superseded": 1` would match
   `"superseded": 12`, and `"status": "clean"` would match `"status": "clean-room"`. The actual
   counts are exact (11 and 1) and appear once each, so no false acceptance here.
4. **Stale/forged receipts.** Refuted: clone path is per-run, per-row intervals match `elapsed_s`
   exactly, no overlaps, tool banner digests match the pinned blobs, and `replay-command.json`
   (exit 0) independently lists the same `got True` outcomes for all six.
5. **Substituted tool or revision.** Refuted: `d2eaecd` is an ancestor of the delivered revision and
   the only changes between them are `.ufo/evidence` files.
6. **Bundle vouching for itself.** The bundle is a projection of the same observations (receipts
   keep only `exit`/`stdout`/`stderr`; `expect`/`held` are dropped). Independence comes from the
   gate plus the digest pin, not from the bundle. Noted so the projection is not double-counted as
   separate evidence.

## Row-scope caveats (do not over-read this audit)

- These six rows are unchanged from the round-23 freeze, and all six tools are byte-identical
  between base `6a1821a` and delivered `c8c5b88` (`git diff --stat` over the six tool paths is
  empty). Their receipts are regression evidence (no drift), **not** new hardening and not
  calibration uplift. New hardening lives in `command-binding.py` / `registry-replay.py`.
- `mutate-and-run-regression` resolves its pins through the replay fleet's sibling symlinks, i.e.
  live lanes (`REGRESSION_PIN … repo=/tmp/tameshi-registry-replay-dzo3ypiq/fleet/<lane>`). Content
  is pinned by commit rev + sha256; availability is live. `replay/live-dependent.json` lists only
  `pin-disposition-read` and `verify-round15`, and this row is counted in `revision_pinned: 41`.
  That label is accurate as content pinning, but must not be read as "does not touch live lanes".
- The bundle `cwd` is the temp clone path, now deleted; `command-binding.py` `canonical_cwd`
  (`:58`) is lexical, so cwd binding is self-consistency, not existence. Reproducibility rests on
  the revision pin (`d2eaecd`), which is present in history.

## Smallest safe correction

None required for this wave's acceptance. The only latent gaps (superset token matching; exit-only
binding on `repeat-control-snapshot-mismatch`) do not fire on these receipts, and closing them
means editing the frozen round-23 requirements — a new requirements revision and a new contract,
not a round-24 patch. Do not change the freeze in place.

## Tooling / bounds

No installs or upgrades. Only read-only inspection: `read`, `grep`, and read-only
`git cat-file`/`log`/`diff` with `GIT_OPTIONAL_LOCKS=0`, plus in-memory Python over the evidence
JSON. No registry battery, gate, or selftest was executed in the repo; no writes outside this
report.
