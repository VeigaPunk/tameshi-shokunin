# R23-REATTACK Replay05 — exact row `bash-witness-selftest`

Re-attack of the round-23 wave-2 falsifier whose seat died unreported. Audited against the frozen round-23 artifacts only; no registry command or suite was executed, no production file was written, nothing outside this report was written in the repo.

Axes worked: (A1) evidence-present-vs-inferred in the frozen row; (A2) field-level argv/expect audit against baseline source (static, non-executing); (A3) currency at lane revision c9ff09f (supersession, tool drift); (A4) concrete adversarial delta; (A5) verdict calibration.

## The row

Frozen requirement (`.ufo/evidence/round-23/requirements.json:60-68`, identical in `replay/bundle.json:652-665` and `registry-baseline.json`):

- argv: `["python3", "tools/bash-witness-study.py", "selftest"]`
- expect: `exit 0`, `stdout_contains: ["WITNESS_SELFTEST:"]`
- registry row source anchor: `SKILL.md@98bea7d:1504`, status active, timeout_s 60

The item names `tools/command-binding.py` — it is the validator whose semantics define this binding (`evaluate()`, `tools/command-binding.py:68-121`); the row's argv targets `tools/bash-witness-study.py`, which is the baseline source the frozen run must be compared against.

## A2 — static exact binding: CONFIRMED

Baseline source at the receipt-pinned revision 496d212 (`git show 496d212:tools/bash-witness-study.py`):

- `cmd_selftest` at :1228; `check()` prints `f"  check {name:<44} ok"` / `FAIL` and counts failures (:1231-1237).
- Fixture-op loop expands one f-string check into `init`/`add`/`commit` (:1305-1311).
- Terminal block (:1711-1717): always prints `WITNESS_SELFTEST: {cases-failed}/{cases} pass`; prints `VERDICT: PASS` and returns `EXIT_OK` (0) only when `failed == 0`, else `VERDICT: FAIL` and `EXIT_FAIL` (1). Constants :119: `EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64`. Dispatch :1766 maps `selftest` to `cmd_selftest`; `main()` return becomes process exit (:1778).
- try/except check pairs: `runner_pins refuses a short PIN_BASH` (:1391-1395) and `planted tamper refuses` (:1526-1532) have distinct except-branch names and the try branch provably never executes (the probe call raises); same-name pairs (`duplicate spec id refuses` :1479-1484, `missing manifest refuses`, `usage error exits 64` :1508-1513) print exactly one line.

Mechanical reconstruction (script in /tmp, read-only): extracted the 51 check names in source order, applied the `<44` padding, modeled the try/except sites, expanded the fixture f-string, appended the terminal lines. Result: **byte-identical to the frozen receipt stdout** — all 51 `ok` lines plus `WITNESS_SELFTEST: 51/51 pass` and `VERDICT: PASS`. The frozen stdout is exactly what 496d212 source emits on a fully passing run; no fabricated or retrofitted check line, no ordering or padding deviation.

Binding fields verified on the frozen pair (`replay/bundle.json` receipt :58-71 vs requirement :652-665): argv equal, receipt cwd == bundle cwd (canonical absolute `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`), receipt revision == bundle revision `496d212b…`, exit 0 == expect.exit, token present in stdout. Ran the current read-only validator on the frozen pair:

```
$ python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json \
    --expected .ufo/evidence/round-23/replay/expected.json --json
{"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9",
 "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
```

`expected.json` pin matches bundle bytes; `evaluate()` returns CLEAN.

## A1 — evidence present, not inferred

For this row, `replay/observations.json:194-231` retains: exact requirement, argv, cwd, revision, `measurement_interval` (start 14:42:23.996602Z, end 14:42:24.156838Z; span 0.160236 s == `elapsed_s` 0.16) and `runner_result` with `got: 0`, `held: true`, `kind: selftest`, `status: active`, `stderr: ""`, full `stdout`, `stdout_tail`, `tags: ["baseline"]`. The bundle receipt `stdout` and the observations `stdout` are byte-equal; `stdout_tail == stdout` (complete capture, matching the declared `capture: "complete decoded stdout/stderr; original runner tails retained separately"`). Nothing needed for the row's claim is inferred.

Producer authenticity is NOT established and is not claimable (rejected per item): see F1.

## Findings (no High/Medium against the frozen row)

- **F1 (Low, by design, demonstrated) — field-level false acceptance exists for coherent fabricated bundles.** `evaluate()` cross-checks receipts only against requirements declared in the same producer-authored bundle; the sole external anchor, `expected.json` `bundle_sha256`, is computed by the same hand. Rotating the requirement's argv and the receipt's argv together (`sh -c 'echo fabricated'`) with a hand-written stdout and recomputing the pin yields validator CLEAN (exit 0, `finding_ids []`, synthetic sha256 `cac03d0398301a4e496eb2a26eec9be3c257fb11d8fc067c66db6d17c3b39540`, demonstrated in /tmp). Digest pins therefore catch post-hoc tampering, never original fabrication. This is the tool's documented boundary (`tools/command-binding.py:14-16`: "This validates retained declarations, not their producer authenticity"), so it is not a defect in the frozen evidence — but it means the artifacts cannot distinguish a real 496d212 run from a perfect fabrication. Receipt-only (incoherent) rotation IS caught: observed `exit=1, ["ARGV_MISMATCH","CWD_MISMATCH"]` on synthetic sha256 `a915f440…`.
- **F2 (Low) — expect token alone is non-discriminative.** `"WITNESS_SELFTEST:"` also matches the failure line (`WITNESS_SELFTEST: k/51 pass`); the row's discriminative power is exit-code-only. Sound at 496d212 because failures return `EXIT_FAIL` (:1711-1717), so a real failing selftest cannot satisfy `exit 0`.
- **F3 (Low, latent) — `runner_sha256` provenance imprecision.** `replay.py` hashes `args.repo / 'tools/registry-check.py'` (the outer lane worktree), not the clone that actually executed rows. Harmless here: `cba1664…` equals the hash at 496d212, d2eaecd, c9ff09f and HEAD (no drift), but the field would misattribute if the outer checkout had differed.
- **F4 (Info) — receipt cwd is an ephemeral destroyed tempdir** (`tempfile.TemporaryDirectory` in `replay.py`); `canonical_cwd` validates form only, never existence. Consistent with declarations-only semantics.

## A3 — still applies at c9ff09f?

Yes, unchanged:

- Row not superseded: `tools/registry.json:85-100` row is byte-identical to the baseline row (all fields incl. `source`, `tags`, `timeout_s`); `registry.json` has zero diff between 1f73157 (round-25 base) and c9ff09f; active rows grew 43 → 47 elsewhere in the file.
- `tools/bash-witness-study.py`: no commits since 496d212 — the audited baseline source is still current.
- `tools/registry-check.py`: identical sha256 at 496d212, d2eaecd, c9ff09f, HEAD.
- `tools/command-binding.py`: 496d212 → HEAD diff is 9 lines confined to `selftest()` supplemental-fixture loading (adds round-24 extra-cases); `evaluate()`/`check()` semantics are untouched, and the frozen pair validates CLEAN under the current tool (observed above).

## Retrofill rejection

- `registry_sha256` chain: `ebd2e69a…` == `registry-baseline.json` == `git show 496d212:tools/registry.json` == `git show 28cae179:tools/registry.json` (the requirements `source_revision`). The replay's equality gate (`replay.py`: frozen requirements vs registry-baseline, digest-checked) is consistent end to end.
- Source anchor resolves: commit `98bea7d` ("round-16 verifier spot-check"), `SKILL.md` line 1504 is the `bash declared-witness study` registry-table row containing exactly `python3 tools/bash-witness-study.py selftest`. Not retrofitted.
- Frozen artifacts unmodified since retention: worktree bytes == HEAD bytes for `replay/bundle.json` (`3d6c99b7…`), `replay/expected.json` (`0831c9c8…`), `replay/observations.json` (`a83d8a0b…`), `requirements.json` (`cd5205be…`), `registry-baseline.json` (`ebd2e69a…`); retention commit `8f66b5d` ("round-23: retain executed registry replay and exact binding falsifiers"). A second, empty-message commit `54c14ea` (same timestamp as `8f66b5d`, byte-identical bundle, not an ancestor of HEAD) is an off-history duplicate of the retention commit; it does not touch the retained chain.

## Residual risk and verification gaps

- Per the original item's bounds I did not re-execute the row, so "a real process produced this stdout at 14:42:24Z" is unfalsifiable from the artifacts — exactly the documented authenticity boundary (F1). `measurement_interval`/`elapsed_s` are producer-self-reported and carry no nonce.
- The static reconstruction proves shape-exactness against 496d212 source; it cannot prove the process ran, nor rule out a producer-side fabrication made before commit 8f66b5d (no independent witness exists for either).
- `stdout_contains` is substring matching (stderr can never satisfy it — covered by the tool's own `stderr-cannot-supply-token` case).

No tools were installed or updated for this item.

R23-REATTACK Replay05: AGREE
