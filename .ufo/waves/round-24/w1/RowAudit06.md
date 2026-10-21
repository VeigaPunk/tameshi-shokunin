# RowAudit06 — round-24 replay row audit (5 rows)

## Verdict

**No false acceptance found in the five assigned rows.** Every row's expectation in
`.ufo/evidence/round-23/requirements.json` is met by the retained runner result in
`.ufo/evidence/round-24/replay/observations.json`: exit matches, every required stdout token is
literally present, `held` is `True` with no `stdout_missing`/`cleanup_error`, and the published
`.ufo/evidence/round-24/replay/bundle.json` receipts are byte-identical to the observations. The
separate binding gate (`.ufo/evidence/round-24/replay-gate.json`) independently re-checked exit and
tokens and returned `exit: 0`, `finding_ids: []`.

Residual (inherited, non-blocking) weaknesses are recorded below — none of them is exercised by the
current evidence; they are expectation-design gaps, not observed passes.

Scope note: no producer authentication, promotion, historical R17-CMD-BIND closure or numeric
calibration uplift is claimed here. Nothing was executed in the lane repo; no tools installed.

## Row-by-row comparison

Requirement text: `.ufo/evidence/round-23/requirements.json:85` (pin), `:215` (context),
`:333` (reattribute), `:445` (assemble), `:557` (wave). Registry rows (identical bytes):
`tools/registry.json:106,372,550,741,865` and `.ufo/evidence/round-23/registry-baseline.json`
same lines.

| row | required exit | observed `got` | `held` | required token | token present | stdout bytes |
|---|---|---|---|---|---|---|
| pin-disposition-read | 0 | 0 (int) | True | `"unavailable": 0` | yes (in `counts`) | 7457 |
| context-capture-missing-env | 1 | 1 (int) | True | `missing_injected_environment` | yes (header `id=` and `FINDING` line) | 474 |
| reattribute-round16-selftest | 0 | 0 (int) | True | `SELFTEST: PASS` | yes (final line) | 1044 |
| assemble-round18-selftest | 0 | 0 (int) | True | `SELFTEST: ` | yes (final line `SELFTEST: 80/80 pass`) | 7930 |
| wave-route-mix-selftest | 0 | 0 (int) | True | `ROUTEMIX_SELFTEST: 8/8 pass` | yes (final line) | 291 |

Per-row `revision` is `d2eaecd443bf5f4e387e7e5331282e3d11dea047` (the run revision), `cwd` is the
private clone `/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`, argv equals the
requirement argv exactly, `measurement_interval.start <= end`, and no sentinel `got`
(`timeout`/`unavailable`/`non-hermetic`) appears. `replay-command.json` stdout also prints
`<name> 0 True` / `1 True` for all five.

Internal consistency of each stdout (beyond the literal token):

* pin-disposition-read — parsed JSON: `counts {legs 6, unchanged 1, changed 5, unavailable 0}`,
  `1+5+0 == 6`, and the six legs' `content_status` agree with those counts; `status: ok`,
  `result_reuse: not_established`. It is declared `external: true`, and is correctly listed live
  (`replay/live-dependent.json`: `["pin-disposition-read","verify-round15"]`, `revision_pinned 41/43`),
  so it is not claimed as revision-pinned.
* context-capture-missing-env — negative expectation, genuine recompute: the frozen receipt
  `.ufo/evidence/round-15/frozen/context-missing-env/receipt.json` has **no** `injected_env` key
  (`recompute_environment`, `tools/context-capture.py:833-843`), and the tool also reports
  `receipt_verdict_mismatch` because that receipt records `status ok`/`exit 0` while raw fields
  recompute mismatch (`tools/context-capture.py:1145-1166`). `expected.json` pins
  `receipt_sha256 1ee9d09b…aa208`, which equals the on-disk receipt digest (computed), and
  `apply_expected` (`:1306-1332`) only ever *upgrades* a non-matching verdict to exit 1 — it can
  never turn a mismatch into a pass. A crash/usage error would fail the token check.
* reattribute-round16-selftest — all 8 new-rule cases print `PASS`, `old-rule fidelity 14/14`,
  `old rule fails 5/8` by design; success requires `failures == 0 and old_fails >= 1 and not
  fidelity` and returns 0 only then (`reattribute.py:310-333`).
* assemble-round18-selftest — 80 `[ok]` lines, zero `[FAIL]`, final `SELFTEST: 80/80 pass`; exit 0 is
  returned only when the failures list is empty (`assemble.py:1921-1925`).
* wave-route-mix-selftest — 8 `ROUTEMIX_CASE … ok` lines, no `FAIL`, exit = `0 if not bad else 1`
  (`tools/wave-route-mix.py:89-90`).

## Evidence chain checks (all pass)

1. **Frozen binding is real, not decorative.** `registry-replay.py:138-146` re-hashes
   `--registry-baseline` against `requirements['registry_sha256']` and rebuilds the requirement set
   from the baseline's active rows, refusing (exit 2) on any difference. Observed:
   `sha256(.ufo/evidence/round-23/registry-baseline.json) = ebd2e69a…fec92a` = the value pinned in
   `requirements.json` and in `observations.registry_sha256`; rebuilt active rows `== frozen
   requirements` (43/43, order preserved).
2. **Baseline is a faithful round-23 projection.** Compared with `6a1821a:tools/registry.json`
   (50 rows, 46 active): 47 shared names, **0 field diffs** on argv/expect/kind/status/tags/source/
   timeout/external/superseded_by. The 3 round-23 rows not in the baseline are the
   `command-binding-*` trio, added at `8f66b5d` *after* the freeze commit `496d212` (history of
   `.ufo/evidence/round-23/requirements.json`), then superseded in round-24.
3. **Runner strictness.** `held = got == expected_exit and not missing and cleanup_ok`
   (`tools/registry-check.py:717-721`), `missing` is the **all-of** token test (`:718`), and
   non-int/garbage expectations are refused upstream (`command-binding.py` requires
   `type(expect['exit']) is int`, and `strings(..., nonempty=True)` for argv).
   `registry-replay.project` refuses to publish on any `held is not True`, `cleanup_error`, or
   stream over `max_stream_bytes` (`registry-replay.py:84-104`); none of the five rows shows
   `stdout_missing`/`cleanup_error`, and the largest retained stream is 7930 B vs the 1 MiB cap.
4. **Independent second audit.** `command-binding.evaluate` re-derives `EXIT_MISMATCH` and
   `STDOUT_MISMATCH` from the receipts and requirement tokens (`tools/command-binding.py:98-113`)
   and recomputes the bundle digest (`:115-128`). `replay-gate.json`: exit 0, `finding_ids: []`,
   `bundle_sha256 4f424023…a722a9c6`, which equals `sha256(replay/bundle.json)` (recomputed) and
   `replay/expected.json`. `tool_sha256 9230c68e…061d0d` equals `sha256(tools/command-binding.py)`
   at `d2eaecd`, at `c8c5b88` and live.
5. **Receipts == observations for the five rows.** For each: exit, stdout, stderr, argv, cwd and
   revision are identical between `bundle.json` receipts and `observations.json` runner results;
   `bundle.requirements == requirements.json` (43/43, same order).
6. **Replay is a fresh execution, not a copied artifact.** Round-23's replay used clone
   `/tmp/tameshi-r23-replay-naxu6fzi` and pin `observed_at 2026-10-21T14:42:24Z`; round-24 used
   `/tmp/tameshi-registry-replay-dzo3ypiq` and `2026-10-21T15:56:45Z`. Identical selftest totals
   (80/80, 8/8, 14/14) are expected: the five backing tools plus `registry-check.py`, the frozen
   fixture directory and the requirement/baseline files are byte-identical between `496d212`,
   `6a1821a`, `d2eaecd`, `c8c5b88` and the live tree (`git diff --stat` for those paths is empty;
   per-file sha256 compared).
7. **Delivered revision is covered.** Replay ran at `d2eaecd`, which is an ancestor of the delivered
   `c8c5b88` (2 commits). All five backing tools and `tools/registry-check.py` have identical
   sha256 at `d2eaecd`, `c8c5b88` and live, so the replay result carries to the delivered revision
   for these rows.

## Residual findings (inherited; no observed false acceptance)

Token/requirement design gaps, all present byte-identically in the round-23 frozen pair, therefore
not round-24 regressions. Counterexamples below are derived from source reading only ([INFERENCE] —
not executed; running them would require a new frozen requirements pair).

* **D1 (medium) `assemble-round18-selftest` token cannot distinguish success from failure, and does
  not pin the count.** Requirement token is `"SELFTEST: "`; the failure line is also prefixed
  `SELFTEST: ` (`"SELFTEST: %d/%d pass (%d fail)"`, `assemble.py:1921-1923`) and the total is
  dynamic (`check_count[0]`, `assemble.py:1072-1078`, printed as `total` on both branches).
  [INFERENCE] Delete 40 `check(...)` calls: output becomes `SELFTEST: 40/40 pass`, exit 0, token
  still matched → row still `held`. Discrimination is 100 % exit code; the token adds none.
* **D2 (medium) `reattribute-round16-selftest` does not pin its case count.** Token
  `"SELFTEST: PASS"` matches the line `SELFTEST: PASS (new rule {n}/{n}; …)` where `n = len(cases)`
  is dynamic (`reattribute.py:325-329`). [INFERENCE] Deleting 5 of 8 cases while keeping ≥1
  old-rule failure yields `SELFTEST: PASS (new rule 3/3; old rule fails 1/3; old-rule fidelity
  14/14)` with exit 0 → still `held`.
* **D3 (low) `wave-route-mix-selftest` pins the aggregate `8/8`, not case identity.** Removing a
  case is caught (`7/7` ≠ token) but [INFERENCE] replacing a predicate with `True`
  (`tools/wave-route-mix.py:73-88`) keeps `ROUTEMIX_SELFTEST: 8/8 pass` and exit 0.
* **D4 (low) `pin-disposition-read` does not pin the leg count or the manifest digest.** Token
  `"unavailable": 0` plus exit 0 would still hold for a 2-leg manifest
  [INFERENCE]; in this run counts are 6 legs / 1+5+0 and all six legs carry a verdict.
* **D5 (low) Two of five required commands are not literally sourced by their registry anchor.**
  `wave-route-mix-selftest` cites `SKILL.md@370f2dffe66f…:1976`, whose row documents only
  `python3 tools/wave-route-mix.py --spec .ufo/waves/round-21/spec1.json --json`; the string
  `--selftest` for this tool appears nowhere in `SKILL.md` (grep at delivered `c8c5b88` returns only
  line 1976). `assemble-round18-selftest` cites `SKILL.md@58e5d53:1923-1932`; that range is the
  round-18 registry section and the assemble line reads “as round 17, default ledger …; `--carry` …
  `--explain`” without `--selftest`; only the round-17 row (`SKILL.md:1903`) shows `--selftest`.
  The other three anchors do contain the executed shape: pin `98bea7d:1552` (exact command incl.
  `--manifest`/`--root`), context `98bea7d:1680` (`--check --receipt FILE --expected FILE`),
  reattribute `98bea7d:1813` (exact `--selftest`). Consequence: for D5's two rows the binding chain
  is registry-row → frozen requirements copy, not source text; the argv is still pinned, but its
  provenance is weaker than the other rows.
* **D6 (informational) Frozen set lag.** The battery covers 43 active rows; `tools/registry.json`
  currently has 47 active. The 4 uncovered rows are the round-24 additions
  (`command-binding-selftest-r24`, `command-binding-frozen-clean-pinned`,
  `command-binding-source-read-red-pinned`, `registry-replay-selftest`), which is expected for a
  round-23-frozen battery. No assigned row is uncovered.

## Smallest safe correction

None required for the five rows' current acceptance. If a future round opens the frozen pair, the
minimal tightening is: (a) replace the two aggregate/prefix tokens with count-bearing literals
(`SELFTEST: 80/80 pass`, `SELFTEST: PASS (new rule 8/8`), and (b) extend the two anchor gaps so
the source line literally contains the executed `--selftest` invocation
(`wave-route-mix-selftest`, `assemble-round18-selftest`). Both are battery/registry changes that a
round-24 edit must not make in place — they belong to a new `requirements.json` +
`registry-baseline.json` pair.

## What was checked / not checked

Checked read-only: requirement vs frozen requirements, registry-baseline fidelity against the
round-23 base registry, per-row argv/exit/token/held/interval, bundle-vs-observations equality,
bundle digest recomputation, tool/instrument/runner digests at `d2eaecd`/`c8c5b88`/live,
fixture receipt digest, selftest internal success markers, anchor resolution in the pinned SKILL.md
blobs, and round-23-vs-round-24 replay freshness. Not checked: metric-level K1–K11 calibration
(other lanes), the 38 non-assigned rows beyond the aggregate gate, and any re-execution (prohibited
outside a designated Run item).
