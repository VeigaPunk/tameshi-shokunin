# Report: BundleMeasureSelftest falsification

Date: 2026-10-21. Scope: assigned receipt, its cited sources, and C1 ruler comparison only; no selftest or suite executed.

## Strongest assertion tested
The R18 `measure-selftest` row is internally consistent with a successful `--selftest` invocation at its declared source revision, and is distinct from the failed `bash-witness-selftest` row.

## Finding: agree, bounded
- `.ufo/evidence/round-18/final/checks.json:65-73` declares argv `python3 .ufo/evidence/round-18/measure.py --selftest`, revision `921ef8077440f90d092aab4b9fdc750a45de1224`, exit 0, and stdout SHA-256 `110200649284aa1555a256bc53fbdf4438a6f944fa381b662afa76e3df241bdf`.
- Read-only byte/JSON arithmetic reproduces that digest; stdout is 3,566 bytes, has 98 `PASS ` records, and ends `MEASURE_SELFTEST: 98/98 pass`. Retained stderr is 0 bytes (empty SHA-256). No test was rerun.
- `.ufo/evidence/round-18/measure.py:1537-1541` defines `--selftest` and dispatches to `selftest()`. The Git blob at the declared revision hashes to `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`, matching the on-disk source and R19 `MEASURE_SHA18`. Revision `921...` is an ancestor of final R18 receipt commit `5923d89...`.
- `.ufo/evidence/round-18/coldread/traces/CR48-r3/5.json:3-25` is a different successful run (revision `4acdeac...`, temporary cwd) recording the same source digest but no output bytes. Spotcheck §5 item 4 instead identifies `bash-witness-selftest` at exit 64; `checks.json:45-53` confirms it is a different argv/row. Neither contradicts this receipt.
- C1 comparison: frozen revision `55e1d312...` carries R19 `measure.py` SHA-256 `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`; that ruler measures five routed corrections using `round18-final-measure.json`, not the old selftest row. The separate final R18 measure JSON/output records argv at revision `4b7c682...`, score 8 and 60/60 sections. It does not authenticate the selftest run's cwd.

## Concrete falsifier and residuals
A concrete falsifier of the tested byte/source assertion would be a stdout digest mismatch or a different source blob at `921...`; neither occurred. The row itself lacks cwd, stdout/stderr paths, stderr digest, and recorded time, so exact execution context remains declarative, as the build report already notes. No overlooked C1 correction to this selftest row was established; do not count it as an additional calibration correction.

At review time the live R19 `measure.py` has advanced from the frozen `55e...` blob (live SHA-256 `3f19a16b778242a1f83ba5a92b4b69798e56876003727757aa5497773a2e590f`; scoped diff adds checks). Treat that as post-freeze integration state, not as a change to the historical R18 helper or proof about the frozen C1 ruler. No admission authority is claimed.
