# ReceiptProvenance — round 14, wave w1

Seat: `TameshiR14.ReceiptProvenance` (reviewer, leaf). Read-only. No checks, selftests, probes, or target runs were executed; no hashes were recomputed (deferred to L1). Only retained JSON/markdown and `git log`/`git show --stat` metadata were read. Tool installs/updates: none.

Baseline `d6809df7775338f000e44c8a916067b8866867fb`; delivered round-13 lane commit `7dd16d9`, measured-content commit `4acc607`.

## Code state

- `.ufo/evidence/round-14/capture-context.py`: **absent**. `.ufo/evidence/round-14/` contains only `claims.json`. Anything about the prospective context receipt is **contract-only** (spec.json ReceiptHarness item).
- `tools/pin-disposition.py` (present, sha `297253971dab…`, matches `tool_sha256` in every retained pin row): `git_env()` at lines 197–211 drops every inherited `GIT_*` key; `git_run()` at 214–225 passes `env=git_env()`; the selftest fixture env at 648–685 also drops `GIT_*`. The scrub is **static code**, not an asserted behavior: `--selftest` has no GIT_DIR arm (confirmed by `.ufo/waves/round-13/w1/PinProbe.md:213`, `PinSecurity.md` L2).
- `tools/mutate-and-run.sh`: unchanged for round 14; not read further here (RunnerMappings seat owns it).

## Historical receipt inventory (round 13)

Source: `.ufo/evidence/round-13/verification.json` (schema `tameshi-round13-verification-v1`, 13 checks). Each check records only: `name`, `argv`, `started_at` (UTC µs), `exit`, `expected_exit`, `stdout`, `stderr`, `exit_matches`. **No check records `cwd`, `env`, injected env, `ended_at`, duration, pid, interpreter path/version, or lane HEAD.**

| check | argv (as retained) | started_at (UTC) | exit / expected |
|---|---|---|---|
| pin_selftest | `python3 tools/pin-disposition.py --selftest` | 04:59:24.860762 | 0 / 0 |
| metadata_selftest | `python3 tools/witness-metadata.py --selftest` | 04:59:25.476822 | 0 / 0 |
| metadata_old_null | `… --check --companion …/witness-metadata-old-null.json --json` | 04:59:26.691795 | 1 / 1 |
| metadata_corrected | `… --check --companion …/witness-metadata.json --json` | 04:59:26.722946 | 0 / 0 |
| producer_before | `python3 .ufo/evidence/round-13/producer-before.py selftest` | 04:59:26.753309 | 1 / 1 — **FileNotFoundError** on `.ufo/evidence/tools/mutate-and-run.sh` (path-layout crash; superseded) |
| producer_after | `python3 tools/bash-witness-study.py selftest` | 04:59:26.790845 | 0 / 0 |
| witness_check | `python3 tools/bash-witness-study.py check` | 04:59:26.831323 | 0 / 0 |
| witness_count | `python3 tools/bash-witness-study.py count` | 04:59:26.869571 | 0 / 0 |
| pin_live | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 04:59:26.903956 | 0 / 0 |
| pin_env_scrub | **identical argv to pin_live** | 04:59:26.952682 | 0 / 0 |
| metadata_emit | `python3 tools/witness-metadata.py --emit` | 04:59:27.000994 | 0 / 0 |
| source_census | `…/sources-census.sh validate --root … tameshi` | 04:59:27.030119 | 0 / 0 |
| frozen_and_guardrail_unchanged | `git diff --quiet 546b371… -- .ufo/evidence/round-12 tools/mutate-and-run.sh SHONEN.md` | 04:59:27.087540 | 0 / 0 |

Timing: the window 04:59:24–04:59:27 UTC equals 01:59:24–01:59:27 local (-03:00), consistent with `verification.json` mtime 01:59 and the closure note. Repair receipt `producer-oracle-repair.json` starts at 05:00:00 UTC (02:00 local) and uses relative argv `.ufo/evidence/round-13/producer-oracle.py --source … --runner tools/mutate-and-run.sh`.

Hashes present in receipts: `tool_sha256` `297253…` (inside each pin stdout; matches `expected.json` input pin); `measured_input_sha256` (12 entries); `expected.json` `inputs` (13 entries). No hash of the lane commit, interpreter, or working tree is recorded in the receipt itself.

## Finding of the pin_env_scrub check

- `pin_live` and `pin_env_scrub` have **byte-identical argv**, and their `stdout` is **byte-identical** (both 7025 bytes, sha256 `210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637`). Both embed `observed_at: 2026-10-20T04:59:26Z`, second precision, so equality is also what a plain rerun within the same second produces.
- `pin_env_scrub` retains no injected variable name, no value, no cwd, and no ambient env. Nothing in the row distinguishes it from a plain rerun. Its name asserts an env scrub; the row does not carry one.
- `expected.json` has no `pin_env_scrub` expectation. `verification-verdict.json` marks it `matched: true` and sets `git_environment_scrub_equal: true`. That boolean has no retained source beyond this pair of equal rows.

## Prospective vs retrospective proof

- **Impossible retrospectively:** the round-13 `pin_env_scrub` GIT_DIR poison setup cannot be proven from retained artifacts. The ambient env at 04:59Z was never dumped; the `GIT_*` names present then are unrecorded. Current shell env (`GIT_EDITOR`, `GIT_PAGER`, `GIT_TERMINAL_PROMPT`, no `GIT_DIR`) is a 2026-10-20 observation of the present shell and says nothing about the historical run. `/tmp` top-level scan found no injection transcript: `tameshi-round13-closure-d6809df.json` only repeats the claim in prose, and `/tmp/_c2_census.sh` contains `GIT_DIR` literals that were not inspected (scratch, non-durable under QUALITY 9).
- **Admissible retrospective claim (only):** `pin_env_scrub` is a same-argv rerun whose stdout equals `pin_live`. The scrub itself is static code at `pin-disposition.py:197–211`.
- **Prospective (ReceiptHarness, not yet existing):** `capture-context.py` can produce a *new* receipt in round 14 that records argv, absolute cwd, an explicit `injected_env={"GIT_DIR":"/nonexistent/tameshi-round14-poison"}`, baseline and injected stdout/exit, and comparisons. It proves only its own run. Its results must not be cited as repair of round-13's omitted setup (spec.json says the same).
- **Discriminating power:** `/nonexistent` is a good probe. An unscrubbed `GIT_DIR` would make every `git -C` fail and rows would turn `git_unavailable`/`unavailable`, so identical rows are meaningful. The injected run only proves something if the baseline is also recorded with its GIT_* key names.

## Findings (ordered by severity)

1. **High — pin_env_scrub is not an injection receipt.** Same argv and byte-identical stdout as `pin_live`; no injected/ambient env field. Its `matched: true` and `git_environment_scrub_equal: true` must not be read as an observed poisoning run. Mistake class: name asserts a control the row does not carry.
2. **High — historical GIT_DIR setup is unrecoverable.** Any claim that round 13 ran with `GIT_DIR` poisoned is `[INFERENCE]`, not evidence. The only admissible claim is the one in finding 1. Fix must be new prospective evidence (`capture-context.py` in round 14), not reinterpretation.
3. **Medium — narrative vs bytes.** `corpus/lessons/round-13.md:120` says "Injecting GIT_DIR did not change probe data except the observation time"; `LOG.md:815` says "GIT_DIR poisoning leaves observations equal." The retained `pin_env_scrub` stdout equals `pin_live` including `observed_at`, so no observation-time difference is visible. Narrative is consistent only with equality, and the "except the observation time" phrase is not reflected in the retained bytes. Correction belongs in a new round-14 errata row, not an edit of the frozen lesson.
4. **Medium — measured input coverage is 12 of 13.** `verification.json` `measured_input_sha256` omits `.ufo/evidence/round-13/producer-oracle.py`; that digest is pinned only in `expected.json` and `producer-oracle-repair.json`. The receipt does not self-verify its full input set.
5. **Medium — implicit cwd and relative argv.** Every round-13 argv is relative (`tools/…`, `.ufo/evidence/round-13/…`) and no `cwd` is recorded. The `producer_before` crash shows a relative runner path resolving against the script's location (`.ufo/evidence/tools/mutate-and-run.sh`). Retained exit/stdout/stderr are authentic records, but the command is not reproducible without the undeclared cwd.
6. **Low — no end time, interpreter, or lane HEAD in the receipt.** `started_at` only. Tool identity is provided by `tool_sha256` inside pin stdout, not for the other tools (`witness-metadata.py`, `bash-witness-study.py`, `sources-census.sh` have no recorded sha in the receipt; they are present only in `expected.json` inputs). Lane HEAD was recovered from `git log` (4acc607 committed 02:02:45 -03:00, after the run), not from the receipt.
7. **Low — observed_at precision.** Second-resolution `observed_at` makes equality checks coarse. A round-14 harness should normalize only `observed_at` and record its own µs timestamps.

Positive observations (kept): each round-13 check retains full stdout/stderr and an exit match; `verification.json` appears in commit `4acc607` as a creation (+266 lines, no earlier version); `tool_sha256` in pin stdout matches the expected pin; sibling index size/mtime/sha are recorded before and after with `sibling_indexes_unchanged: true`.

## Recommendations for the round-14 contract (no edits made)

- Keep `expected.json` (frozen) and the new disposition file separate; do not add `pin_env_scrub` to `expected_checks` retroactively.
- `capture-context.py` (ReceiptHarness, prospective only) should record: absolute `cwd`; argv; `injected_env` exactly `{"GIT_DIR":"/nonexistent/tameshi-round14-poison"}`; the **names** (not values) of any ambient `GIT_*` keys in both baseline and injected runs; baseline/injected stdout, stderr, exit; a comparison that normalizes only `observed_at`; sha256 of `tools/pin-disposition.py`, `tools/mutate-and-run.sh`, `pin-manifest.json`; interpreter path and version; lane HEAD; µs start and end timestamps.
- If baseline inherits `GIT_DIR`, the receipt must mark the baseline contaminated rather than compare it silently.
- Manifest-vs-runner mapping: record the explicit booleans as data, not only as reader-reconstructed checks (round-13 lesson item 2).

## Checks for L1 (not executed here)

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --follow --format='%H %aI' -- .ufo/evidence/round-13/verification.json` — confirm one creation commit and no later edits.
2. `git -C … diff --quiet 4acc607 -- .ufo/evidence/round-13` — frozen round-13 bytes unchanged after the 7dd16d9 closure commit (or name the diff).
3. Recompute sha256 of the 13 `expected.json` inputs and `producer-oracle.py`; compare to `expected.json` and `producer-oracle-repair.json` (checks coverage gap in finding 4).
4. After `capture-context.py` lands and is run by L1: confirm `context-receipt.json` has `injected_env` exactly equal to the spec value, no ambient env values, baseline and injected exit codes equal, and comparable JSON equal after removing only `observed_at`.
5. Confirm `pin_env_scrub` in round-13 is still labelled a same-argv rerun in any new evidence that cites it; no new evidence may cite it as poisoning proof.

## Residual risk / unknowns

- Round-13 ambient env at 04:59Z: **unknowable** from retained bytes.
- `/tmp/_c2_census.sh` `GIT_DIR` references: not inspected; scratch only.
- Hash recomputation: not run by this seat (no checks mid-flight).
