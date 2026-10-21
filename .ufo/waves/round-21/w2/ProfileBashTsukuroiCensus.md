done

# bash-tsukuroi-census — independent F5 reproduction

## Axes
- **Coverage:** materialized the contract-pinned blob and executed all seven required profiles, each in a fresh bubblewrap sandbox.
- **Freshness:** independently re-executed the target with a separate driver; did not invoke/import `tools/env-diff.py` or use its helpers.
- **Auditability:** saved the per-profile tuples and run metadata in `surfaces/bash-tsukuroi-census.json`, plus exact clean stdout in `surfaces/bash-tsukuroi-census.clean.stdout.txt`.

## Result / findings by severity
No actionable falsification found for this assigned surface. The independent result corroborates the producer's `invariant` classification and clean exit; this is a scoped recommendation, not admission of the complete C2 claim.

## Commands, pin, and runtime evidence
- Contract pin: `.ufo/evidence/round-21/c2-contract.json:28` declares repo `tsukuroi-shokunin`, revision `165307fe4746a8807b02ec4a7d7ecac0368454a6`, path `tools/tsukuroi-census.sh`, interpreter `bash`, SHA-256 `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`. Profile and tuple rules are at `c2-contract.json:1-22`.
- Read-only materialization used `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file blob 165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh`. The verified materialized bytes were 44,947 bytes and SHA-256 `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`, exactly matching the contract. `git rev-parse` resolved the revision to that commit; commit metadata: `2026-10-14T13:57:19-03:00`, “probation round 4 (training r3): see LOG — 32-lane wave, named verifiers, errata applied”.
- Actual independent command: `python3 /tmp/tameshi-r21-ProfileBashTsukuroiCensus-driver/f5_repro.py` — exit **0**. Its seven target invocations used `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind <fresh-R> /tmp/w --unshare-net --die-with-parent --chdir /tmp/w bash /tmp/w/target.sh --selftest`. Bubblewrap was `0.13.1`; Bash was `5.3.20(1)-release`; Python was `3.14.8`.
- Per contract `c2-contract.json:3-16`, environments were: host (invoking environment with all `GIT_*` removed); clean (`PATH` inherited, `HOME=/tmp/w/home`, `TMPDIR=/tmp/w/tmp`, `LANG=C`, `LC_ALL=C`, `TZ=UTC`); clean_repeat in a new sandbox; tz (clean plus `TZ=Pacific/Chatham`); locale (clean plus `LANG=LC_ALL=en_US.UTF-8`); home (clean plus `HOME=/nonexistent`); columns (clean plus `COLUMNS=20`, `LINES=5`, `TERM=dumb`). Each used a distinct fresh R with `home/`, `tmp/`, and the pinned `target.sh`.

All profiles completed with exit **0**, stdout length **1,597 bytes**, and empty stderr. Each raw tuple `(exit, stdout_sha256, stderr_sha256)` was identical:

`(0, 0d66197fafa83f5cf21ecd446d55c07bb2fbd382dd6b4d7ff0ef2250be8991bf, e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855)`

Thus clean equaled clean_repeat, all other profile tuples equaled clean, and the contract rules at `c2-contract.json:19-22` yield **`invariant`, `sensitive_to: []`**.

## Capability, producer comparison, and random paths
This was a real suite pass, not a uniform usage/setup response: the captured stdout has 26 individual `PASS` case lines and ends `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`; there are zero `FAIL` lines. The raw output includes healthy, degraded, and blocked fixture arms. The pinned implementation increments PASS/FAIL in `tools/tsukuroi-census.sh:692-694`, validates cases in `:744-788`, and emits the counted result at `:915-917`.

Producer receipt `.ufo/evidence/round-21/f5/receipt-final-production.json:313-380` reports `normalization: none`, `invariant`, seven exit-0 profile tuples, and `sensitive_to: []`. Its clean stdout and stderr hashes are exactly the same as this independent run (`:322-328`); its clean-repeat tuple at `:330-336` also matches. My JSON records `classification_agreement`, `sensitive_to_agreement`, `clean_exit_agreement`, and both clean stream hash matches as true.

The target does create a random fixture directory (`mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX`, pinned source line `:630`), but that path does not leak into successful stdout: the independent byte check found no fixture-template string. The result is therefore not raw-output-nondeterministic; there was no random-path variation to explain, and no normalization was applied. This exactly reproduces the producer's clean hash.

## Residual risk and verification gaps
The conclusion covers only this pinned surface and the seven finite profiles on this host; it does not establish universal environment invariance or independently remeasure the other eight C2 surfaces, the whole C2 counter, or the producer tool's own `--selftest`. Those are outside this seat's scope. No tools were installed or updated.