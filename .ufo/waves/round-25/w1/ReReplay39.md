# ReReplay39 — re-attack of round-23 Replay39 (row `round21-measure-selftest`)

## Verdict

AGREE. The frozen row `round21-measure-selftest` is statically and exactly bound in every round-23
artifact, and the retained evidence for it is actually present (full streams, newly retained invocation
metadata), not inferred or retrofilled. I found no field-level false acceptance in the retained
receipt. The adversarial deltas below get a CLEAN result only with a forged receipt whose stdout
contradicts itself. The real tool cannot print that stdout. Accepting such a receipt is the named
round-23 "loose substring tokens" limitation together with producer authenticity, which is out of
scope. It is not a new defect in this row's binding. The same holds at lane revision `c9ff09f`.

## Static binding (holds)

The comparison was done with a Python field-by-field script over the parsed JSON. It used full
streams, not tails.

- argv `["python3", "tools/round21-measure.py", "--selftest"]` and expect
  `{"exit": 0, "stdout_contains": ["ROUND21_MEASURE_SELFTEST: 13/13 pass"]}` are equal in all of these:
  - `round-23/requirements.json:560-571`
  - `round-23/registry-baseline.json:874-882` (sha256 `ebd2e69a…`, equal to `registry_sha256` and to
    `tools/registry.json` at both `28cae17` and `496d212`)
  - `replay/bundle.json` requirement `:1155-1167`
  - receipt `:524-536`
  - `observations.json` row `:1708-1749`

  Each artifact has exactly one row with this name.
- Baseline source `SKILL.md@370f2df:1977` is the `tools/round21-measure.py` registry line. Its
  self-invocation column is literally `python3 tools/round21-measure.py --selftest`, so the argv
  matches. The `13/13` token is not in SKILL.md. It comes from the tool: `round21-measure.py:93-131`
  registers 9 named checks plus 2×2 loop checks, which is 13. `:133-134` prints
  `ROUND21_MEASURE_SELFTEST: {passed}/{len(checks)} pass` and exits 0 only when passed == 13. For an
  honest producer, the token, exit 0 and "all checks passed" are therefore equivalent.
- `sha256(replay/bundle.json)` = `3d6c99b7…` = `replay/expected.json`. The receipt keys are exactly
  the seven required keys. cwd `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` equals the
  bundle and observation cwd. The revision `496d212…` is the same in the receipt, the bundle, the
  observation row and the observations top level. exit is an int `0`, equal to `runner_result.got`
  and `held: true`.
- Full output: the receipt stdout (461 bytes, 14 lines) is byte-equal to `runner_result.stdout`, and
  stderr is `''` in both. It has 13 `PASS` lines, 0 `FAIL` lines, the token once, and the token as the
  last line. The tail equals the full stdout because the output is short.
- Command: `python3 <command-binding.py> --bundle replay/bundle.json --expected replay/expected.json --json`
  run with both binding versions (`496d212`, sha256 `d533dc1e…`, and `c9ff09f`, sha256 `9230c68e…`)
  → `{"exit": 0, "finding_ids": [], "bundle_sha256": "3d6c99b7…"}`, exit 0.

## Evidence present vs inferred

- **Present, not retrofilled:** `496d212` was committed at 14:26:23Z. The replay ran from 14:42:22Z
  to 14:44:58Z (`observations.json:12-15`), and the row ran from 14:44:56.53Z to 14:44:57.23Z,
  consistent with `elapsed_s 0.707`. The results were retained in `8f66b5d` at 14:46:12Z.
  `replay.py:57-71` builds every receipt field from rows it executed itself. The historical
  `registry-C.json` run of the same row has `elapsed_s 0.737` and tails only, so it is a different
  run and was not copied in.
- **Inferred (instrument-asserted):**
  - The receipt `revision` is the pre-run `rev-parse` value (`replay.py:32`), copied into every
    receipt (`:63,66,69`). It is never re-read from the clone. This is the same generic gap
    ReReplay19 reports.
  - For this row the stdout cannot discriminate the revision. `tools/round21-measure.py` (sha256
    `eda5490a…`), `c1-survivors.py`, `c2-count.py` and `c2-contract.json` have had zero commits since
    `370f2df` through `c9ff09f`. Any revision in that range would produce byte-identical stdout, so
    the revision has no observable bearing on this receipt.
  - `expected.json` is written by the producer in the same process as the bundle
    (`replay.py:72-75`), not by an independent caller. The effective commitment is git commit
    `8f66b5d`.
  - `observations.runner_sha256` hashes the live `--repo` copy (`replay.py:78`), not the clone copy
    that ran (`:54`). The values coincide, because `registry-check.py` is `cba16646…` at `496d212`
    and `8f66b5d`. Round 24 already fixed this with `runner_sha256_clone_copy`
    (`tools/registry-replay.py:162-163,177`).
- No producer-authentication claim is made or accepted.

## Adversarial delta (executed, /tmp scratch only)

I rewrote only this row's receipt and re-pinned `expected.json` to each new digest, as the trusted
caller would. I ran both binding versions on each case:

| receipt edit | r23 binding | c9ff09f binding |
|---|---|---|
| none (control) | 0 `[]` | 0 `[]` |
| `MEASURE_CASE c2-wrong-pin FAIL`, summary kept | 0 `[]` | 0 `[]` |
| stdout = `ROUND21_MEASURE_SELFTEST: 12/13 pass\necho ROUND21_MEASURE_SELFTEST: 13/13 pass` | 0 `[]` | 0 `[]` |
| stdout = `ROUND21_MEASURE_SELFTEST: 13/13 passes were skipped` | 0 `[]` | 0 `[]` |
| stderr = Python traceback | 0 `[]` | 0 `[]` |
| `13/13` → `12/13` (negative control) | 1 `STDOUT_MISMATCH` | 1 `STDOUT_MISMATCH` |

The strongest delta is the second edit: a receipt whose full stdout reports a failed case is CLEAN.
Every accepted delta is self-contradictory output that `round21-measure.py:132-134` cannot emit, so
reaching it requires a forged receipt. That is the substring limitation named in
`corpus/lessons/round-23.md:110-112` ("loose substring tokens are named old limitations; frozen
argv/expect values are not silently strengthened"), and the binding docstring excludes producer
authenticity. I record it as a tradeoff, not a false acceptance of the retained evidence.

**Adjacent observation (does not flip the verdict):** the selftest reads four live sibling object
stores: kumitate, kagi, tsukuroi and mado. It does this through `ROOT.parent / surface["repo"]`
(`round21-measure.py:72-77`, `check=True`), and the replay symlinks those siblings live
(`replay.py:51-53`; `registry-replay.py:160-161`). Neither the receipt nor the bundle records that
input. Round 24's `replay/live-dependent.json` counts this row among `revision_pinned: 41`, because
`live_dependent` only considers `external` or argv-token hits (`registry-replay.py:99`,
`registry-check.py:632-645`).

The dependency is availability-only. The reads are `git show <pinned-sha>:<path>`, which is
content-addressed, and all six pinned commits are reachable from 139–324 refs in non-shallow
siblings. It can therefore only flip the row to a loud failure (traceback, exit 1), never to a false
pass.

## Status at lane revision c9ff09f

- `tools/registry.json` row `round21-measure-selftest` is field-identical at `496d212` and `c9ff09f`,
  and it is still `active` with the same `source` (`SKILL.md@370f2df:1977`). It has not been superseded.
- `command-binding.py` changed only in its selftest fixture loop, which now also loads
  `round-24/extra-cases.json`. `evaluate()` is unchanged, and the table above shows identical results.
- The round-24 replay (`d2eaecd`) shows the row with `got 0` and `held true`, the same last line, and
  `external false`. The substring and sibling-input observations still apply. The `runner_sha256`
  provenance issue is fixed in the successor `tools/registry-replay.py`.

## Smallest safe correction

None is required for this row's binding. For the adjacent observation, give the row an explicit
declaration so that `registry-replay` lists it under `live_dependent` instead of `revision_pinned`.
The declaration would be `external` with the four sibling repos and pinned SHAs from
`c2-contract.json`. Anchoring the token to a whole line, or rejecting any `FAIL` line, would close the
self-contradicting-stdout delta. That is a frozen-expect strengthening that round 23 deliberately
declined, so it is a judge tradeoff, not a repair.

## Tooling and bounds

- No tools were installed or updated.
- No registry command, suite, selftest or gate was run. The only command executed was the read-only
  `command-binding.py --bundle/--expected` check, on `/tmp` copies.
- No git or jj write commands were run in the lane. Only read-only git with `GIT_OPTIONAL_LOCKS=0`
  was used.
- The scratch directory `/tmp/rereplay39.*` was removed. Nothing was written except this report.

R23-REATTACK Replay39: AGREE
