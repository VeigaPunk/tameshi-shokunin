seat: ExecRows04

# C1 row re-verification — S024, S026, S028, S081 (author of these ledger entries)

Round-45 C1 freshness sweep, four population rows. Each row was opened live on 2026-10-25 from the row's own URL — the first http(s) URL of the source cell, byte-exact as the counter compares it (`measure.py:78-93` `parse_rows`, `URL_RE`). Each quote was located afresh in the `--extract` normalized text of the fetched bytes (never copied from the row's own source/scope/anchor/teaches cells; the counter's own `quote copied from row` guard at `measure.py:159-161` passes for all four).

Registry rows read at the freeze revision: `corpus/SOURCES.md:35` (S024), `:37` (S026), `:39` (S028), `:90` (S081) — all `mined`, ids <= S160, http(s) URL, so all four are inside the C1 population.

## Fetch evidence (two independent fetches per row, byte-identical)

| row | URL | curl exit | bytes | sha256 | refetch (no `-A`) |
|---|---|---|---|---|---|
| S024 | `https://www.fuzzingbook.org/html/Reducer.html` | 0 | 496906 | `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` | exit 0, same bytes, `cmp` equal |
| S026 | `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html` | 0 | 236387 | `5d74dd1c3c75d5ec1b8d53d6a518b4b01ae085f03006f1f44febbb8143e92296` | exit 0, same bytes, `cmp` equal |
| S028 | `https://bazel.build/reference/test-encyclopedia` | 0 | 221292 | `d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a` | exit 0, same bytes, `cmp` equal |
| S081 | `https://bazel.build/reference/test-encyclopedia` | 0 | 221292 | `d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a` | exit 0, same bytes, `cmp` equal |

Command shape (per row): `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows04/S###.raw '<url>'`, then a second fetch without `-A` compared with `cmp -s`. S028 and S081 share one URL and therefore one byte-identical snapshot content; they keep separate fragment/snapshot basenames so each id has its own committed blob.

Snapshots for integration: `/tmp/tameshi-r45-ExecRows04/S0{24,26,28,81}.raw` and pre-made `S0{24,26,28,81}.raw.gz` (gzip `-9 -n`). `gzip -dc | sha256sum` round-trips to the sha256 above for all four, so the `.gz` blobs satisfy `load_snapshot` (`measure.py:168-179`) once copied to `.ufo/evidence/round-45/freshness/sources/`.

## S024 — fuzzingbook, Reducing Failure-Inducing Inputs
- Anchor §Delta Debugging. Live normalized text still carries the whole runnable-reducer passage: "To use a Reducer, one first has to build a Runner whose outcome is FAIL if the precise error occurs. We therefore build a ZeroDivisionRunner whose run() method will specifically return a FAIL outcome if a ZeroDivisionError occurs", then `dd . reduce ( python_input ) '3/0'` followed by "The input is reduced to the minimum: We get the essence of the division by zero."
- Verdict `holds`: teaches = "a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it" — both clauses still stated by the live page.
- CHECK: `CHECK S024 verified ok` (exit 0)
```json
{"id":"S024","url":"https://www.fuzzingbook.org/html/Reducer.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99","quote":"Delta Debugging is a simple and robust reduction algorithm. We can tie a DeltaDebuggingReducer to this runner","snapshot":".ufo/evidence/round-45/freshness/sources/S024.raw.gz","author":"ExecRows04","note":"Live Reducer.html still has the §Delta Debugging passage: a DeltaDebuggingReducer tied to a ZeroDivisionRunner (FAIL only on ZeroDivisionError) yields '3/0' and 'The input is reduced to the minimum', grounding the runnable-reducer teaches cell."}
```

## S026 — Google Testing Blog, Flaky Tests at Google (Micco, 2016-05-27)
- Live post body still states all three teaches clauses: "we see a continual rate of about 1.5% of all test runs reporting a \"flaky\" result"; "about 84% of the transitions we observe from pass to fail involve a flaky test"; and "causing it to report a failure only if it fails 3 times in a row. This reduces false positives, but encourages developers to ignore flakiness in their own tests".
- Verdict `holds`.
- CHECK: `CHECK S026 verified ok` (exit 0)
```json
{"id":"S026","url":"https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"5d74dd1c3c75d5ec1b8d53d6a518b4b01ae085f03006f1f44febbb8143e92296","quote":"about 84% of the transitions we observe from pass to fail involve a flaky test","snapshot":".ufo/evidence/round-45/freshness/sources/S026.raw.gz","author":"ExecRows04","note":"Live post body still states 'about 84% of the transitions we observe from pass to fail involve a flaky test', matching the teaches clause on pass-to-fail transitions; the 1.5% rate and the fail-3-in-a-row / ignore-flakiness clause are also still present."}
```

## S028 — Bazel test encyclopedia (hermetic contract)
- §Role of the test runner still reads: "If a test process runs to completion and terminates normally with an exit code of zero, the test has passed. Any other result is considered a test failure. In particular, writing any of the strings PASS or FAIL to stdout has no significance to the test runner."
- §Initial conditions env table still lists `LANG unset required` and `TZ UTC required`; the `TEST_PREMATURE_EXIT_FILE` row still reads "absolute path to a private file in a writable directory (used for catching calls to exit())" with status `optional`.
- Verdict `holds`: every clause of teaches (exit code alone decides, stdout PASS/FAIL means nothing, LANG unset, TZ=UTC, premature-exit file) is still on the live page. The "outcome depends only on declared inputs" framing remains the page's hermetic premise.
- CHECK: `CHECK S028 verified ok` (exit 0)
```json
{"id":"S028","url":"https://bazel.build/reference/test-encyclopedia","opened":"2026-10-25","verdict":"holds","raw_sha256":"d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a","quote":"If a test process runs to completion and terminates normally with an exit code of zero, the test has passed","snapshot":".ufo/evidence/round-45/freshness/sources/S028.raw.gz","author":"ExecRows04","note":"Live test encyclopedia still has the Role-of-the-test-runner normal-completion paragraph (exit code zero alone passes, any other result fails, stdout PASS/FAIL has no significance) and the Initial conditions table still requires LANG unset and TZ=UTC with optional TEST_PREMATURE_EXIT_FILE."}
```

## S081 — Bazel test encyclopedia (reopened, precise wording superseding S028)
- Normal-completion paragraph and `TEST_PREMATURE_EXIT_FILE` row are unchanged from the S028 reading above, so the superseding claim ("passing requires normal completion with exit zero; PASS/FAIL stdout is irrelevant; optional TEST_PREMATURE_EXIT_FILE is documented for catching calls to exit(), not every early termination") is still exactly what the live page says: the row's parenthetical is "used for catching calls to exit()" and its status is `optional`, and the separate §early-exit paragraph scopes it to a file the test creates "upon start and remove[s] upon exit" (a cooperative hook, not a universal early-termination detector).
- Verdict `holds`.
- CHECK: `CHECK S081 verified ok` (exit 0)
```json
{"id":"S081","url":"https://bazel.build/reference/test-encyclopedia","opened":"2026-10-25","verdict":"holds","raw_sha256":"d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a","quote":"In particular, writing any of the strings PASS or FAIL to stdout has no significance to the test runner.","snapshot":".ufo/evidence/round-45/freshness/sources/S081.raw.gz","author":"ExecRows04","note":"Live normal-completion paragraph still says the PASS/FAIL strings on stdout have no significance to the test runner, and the TEST_PREMATURE_EXIT_FILE row is still optional and documented as 'used for catching calls to exit()', matching the superseding teaches cell."}
```

## Commands actually run
```
python3 .ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecRows04/S###.raw
python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows04/S###.json \
  --snapdir /tmp/tameshi-r45-ExecRows04        # exit 0 for all four
python3 .ufo/evidence/round-45/freshness/measure.py --selftest   # C1_R45_SELFTEST: cases=19 failed=0, VERDICT: PASS
```
No deciding measurement was run by this seat (`--lane/--rev` without `--check` was never invoked); the only `--rev` use is the `--check` helper, as allowed.

## Result
Verdicts: S024 holds, S026 holds, S028 holds, S081 holds. Four `CHECK ... verified ok` lines at `--rev 3310e7be803516ca5934b4e949d91bcec824b179`, no drifted/unreachable/invalid. No blockers. Tooling: nothing installed (curl and python3 already present; pacman transactions are host-paused and were not used).

Artifacts kept for L1 integration in `/tmp/tameshi-r45-ExecRows04/`: `S024.raw`, `S026.raw`, `S028.raw`, `S081.raw`, the matching `*.raw.gz`, the `*.txt` normalized extracts, and the four fragment JSONs.
