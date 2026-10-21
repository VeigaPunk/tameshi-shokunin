# PredK9 — falsification of K9 `stream-limit-refused`

Reviewer: TameshiR24-2.PredK9 · revision c8c5b88c8e961a929cdc351b95a7074c76958909 · base 6a1821a8897eea6e7d9669292160ec9593669409

## Verdict

**K9 is weak: it does not pass vacuously, but it fails to discriminate plausible weaker implementations.** It tests the real code path, and it passes for the right reason on the delivered tool (static trace; see below). But it uses one oversized ASCII stdout far above one limit, with no negative control under the flag. So it accepts at least five weaker implementations. One of them, counting characters instead of bytes, is also missed by the tool's own selftest (`registry-replay-selftest`), so no frozen surface in round 24 kills it.

**The base result in `before.json` is honest.** K9 is `discriminated: false, reason: tool-absent` because `tools/registry-replay.py` does not exist at the base revision. That is a correct baseline, but it is a presence check, not a discrimination check.

This is a fixable test-coverage defect, not a tradeoff the judge must reject. It does not support any numeric uplift, producer authentication or R17-CMD-BIND closure, and none is claimed here.

## What I checked (read-only)

| Check | Observed |
|---|---|
| `git cat-file -e 6a1821a…:tools/registry-replay.py` | `fatal: path 'tools/registry-replay.py' exists on disk, but not in '6a1821a…'` → absent |
| sha256 of `measure.py` at e338f1b, at c8c5b88, and in the live tree | all `0a7f6daa…57daa64`, equal to `before.json` `instrument_sha256` |
| commits touching `measure.py`, `contract.json`, `before.json` | only e338f1b (frozen before the implementation) |
| sha256 of `tools/registry-replay.py`, c8c5b88 blob vs live tree | both `9fcd2dbb…5208714` |
| `after.json` / recorded post-implementation measurement in `.ufo/evidence/round-24/` | none present |

I did not run `measure.py`, the selftest or any mutant: my item does not say "Run". The claims about outcomes below come from tracing the code and are marked [INFERENCE].

## How K9 measures

- **Fixture** (`measure.py:147-157,175`): one row with `held: True`, `got: 0`, no `cleanup_error`, and stdout `'OK\n' + 'x'*64` (67 ASCII bytes). The extra argv is `--max-stream-bytes 16`.
- **Pass condition** (`measure.py:170,179-180`):
  - the control passes: run without the flag, it exits 0, reports `finding_ids == []`, and writes a bundle;
  - the K9 run exits 1;
  - `'STREAM_LIMIT' in finding_ids` (membership, not equality);
  - no `bundle.json` is written.
- **Base** (`measure.py:143-144`): the tool is missing, so the row is `tool-absent`. This matches the `before.json` row byte for byte.

## Delivered implementation trace [INFERENCE: static]

The relevant code is `registry-replay.py:92-98,108-110,116-118`.

- **K9 run:** \(67 > 16\), so `STREAM_LIMIT` is the only finding (the row holds and has no cleanup error). `project` returns exit 1 with `bundle=None`, `publish` writes nothing, and K9 is True.
- **Control:** \(3 \le 2^{20}\), so it exits 0, reports `[]` and writes `bundle.json`. `control_ok` is True.

**Not vacuous.** If the flag were missing, argparse would exit 64. If the tool crashed, there would be no report, so `finding_ids` would be `[]` and K9 would be False. A tool that always refuses fails `control_ok`.

## Counterexamples: weaker implementations K9 accepts [INFERENCE: static]

Each is a one-line change to `project()`. The fixture and pass condition are as above.

| # | Weaker implementation | K9 | Tool selftest (`registry-replay.py:199-206`) |
|---|---|---|---|
| A | **Counts characters, not bytes:** `len(text) > max_bytes` | **pass** (fixture is ASCII) | **pass**: every stream case is ASCII (`'e'*9`, `'12345678'`, `'ok'`) |
| B | Refuses whenever the flag is given: `if max_bytes != DEFAULT_MAX: STREAM_LIMIT` | pass (control omits the flag) | fail (`stream-at-limit` expects 0) |
| C | Off by one: `>=` | pass (\(67 \ge 16\)) | fail (`stream-at-limit`) |
| D | Checks stdout only, ignores stderr | pass (stdout is the oversized stream) | fail (`stream` case oversizes stderr) |
| E | Ignores the flag value and uses a fixed threshold \(t\) | pass for any \(t \in [3,66]\) | passes only at \(t = 8\) |
| F | Checks only the first row, or breaks out of the loop early | pass (single-row fixture) | pass (every selftest case is single-row) |

Counterexample A, concretely: an observation with stdout `'€'*6` and `--max-stream-bytes 16`.

- The stdout is 6 characters but 18 UTF-8 bytes.
- The delivered tool refuses it with `STREAM_LIMIT`, exit 1.
- Implementation A computes \(6 \le 16\) and publishes the bundle, exit 0.
- Neither K9 nor the selftest contains a non-ASCII stream, so neither notices.

The flag is named `--max-stream-bytes`, and `ScribeLimits.md`/`SimplifyReplay.md` describe it as a UTF-8 byte bound. So A breaks the stated contract while every round-24 check stays green.

Counterexample F, concretely: two rows where only the second is oversized. Implementation F publishes. The actual replay (43 rows, all under 1 MiB, `refused_rows: []` in `replay-command.json`) cannot catch it either.

Counterexample E at \(t = 8\) would be caught only by the actual default-limit replay as separate evidence, not by K9.

## Overclaims next to K9

1. **The bound applies to the published bundle only, not to what is retained.** The docstring at `registry-replay.py:9` says "each retained stdout/stderr is bounded by --max-stream-bytes". However:
   - `--run` writes `observations.json` with the full streams before projecting (`registry-replay.py:181-184`);
   - the runner captures without a bound, via `proc.communicate()` and `retain_streams` (`registry-check.py:693,724-726`).

   So when a row produces an oversized stream, the bundle is refused but the full stream still lands under `--out`, and a huge stream is fully buffered in memory first. Because K9 runs `--project` only, it cannot see this. A K9 pass is evidence of projection refusal, not of bounded retention.

2. **A lone high surrogate crashes the tool with an exit code that reads as "refused".** Input: `--project` observations whose stdout contains the JSON escape `"\ud800"`. Python's `json.loads` accepts the lone surrogate. `encode('utf-8', 'surrogateescape')` only maps U+DC80–U+DCFF, so it raises `UnicodeEncodeError` (`registry-replay.py:96`). The uncaught traceback exits 1, which is the exit code for "refused (findings)", with no report. The documented exit for invalid input is 2. The failure is safe (no bundle is written), and the runner never produces surrogates because it decodes with `errors="replace"`. But a consumer that reads only the exit code misclassifies it. K9 is unaffected: there is no report, so K9 is False.

## Impacted axes

- **Calibration:** K9's discrimination power is overstated. Weaker implementations A–F all count as "hardened".
- **False provenance:** low risk. `before.json` is honest. The docstring "retained … bounded" is an overclaim.
- **Duplicate authorities:** none found. `project()` is the only place a bundle gets published.

## Smallest safe correction

The ruler is frozen, so do not edit `measure.py`. Put the fix on the production selftest, which the `registry-replay-selftest` row already enforces. Then carry the same shape into the next contract's K9.

1. Add a multibyte case: `obs(stdout='€'*3)` with `--max-stream-bytes 8` (3 characters, 9 bytes) must give exit 1 with `STREAM_LIMIT`. Its pair, `obs(stdout='€'*2)` at limit 8 (6 bytes), must give exit 0 and write a bundle. This kills A.
2. Add a two-row case where only row `two` is oversized: expect `refused_rows == ['two']`. This kills F.
3. Bump the `stdout_contains` count in `tools/registry.json` (`registry-replay-selftest`, line 994) to match.
4. In `project()`, return `INVALID_OBSERVATIONS` (exit 2) on `UnicodeEncodeError`, or measure with `'surrogatepass'`.
5. Reword the docstring at line 9 to say "each stream projected into the bundle". Also state that `observations.json` and the runner capture keep the full streams.

For a future K9: add a same-flag negative control (a stream exactly at the limit must publish). This kills B, C and E inside K9 itself, and a multibyte fixture kills A.

## Tooling

No tools installed or updated.
