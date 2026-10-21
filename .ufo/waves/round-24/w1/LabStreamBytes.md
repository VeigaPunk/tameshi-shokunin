# LabStreamBytes — STREAM_LIMIT: bytes or characters?

## Verdict

Hypothesis **CONFIRMED, no defect found**. `tools/registry-replay.py --project` enforces
STREAM_LIMIT on the **UTF-8 byte length** of retained stdout/stderr, not the character
count, with a strict `>` comparison (a stream of exactly `--max-stream-bytes` bytes
passes). This is the documented intent of the flag name (`--max-stream-bytes`,
docstring line "each retained stdout/stderr is bounded by --max-stream-bytes"), so no
correction is proposed. The falsification attempt (5 chars must pass a limit of 12 if
counting characters) failed, as it should under byte semantics.

Godspeed axes: decisive named runs at limits 12 and 15; cheap discriminators at 4/5/14;
boundary semantics (strict `>`); write-surface of refused projections.

## Evidence

Instrument identity — clone at rev `c8c5b88c8e961a929cdc351b95a7074c76958909`:

```
$ sha256sum /tmp/LabStreamBytes-r24/tools/registry-replay.py
9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714
```

equals `instrument_sha256["tools/registry-replay.py(live tree, equals rev blob)"]` in
`.ufo/evidence/round-24/replay/replay-command.json`.

Code under test — `tools/registry-replay.py:96-98` (in `project()`):

```python
if len(text.encode('utf-8', 'surrogateescape')) > max_bytes:
    findings.add('STREAM_LIMIT')
    refused.append(name)
```

applied per stream in `('stdout', 'stderr')`. `max_bytes` comes straight from
`--max-stream-bytes` (default `1 << 20`, `registry-replay.py:260`, positive-only check
`:263`).

Fixture — `/tmp/LabStreamBytes-lab/kana.json`, one row `kana-five`
(`held: true`, `got: 0`, `stderr: ""`), `stdout` = `あああああ`:

```
chars 5 bytes 15      # U+3042 = E3 81 82, 3 bytes each
```

Runs (all inside /tmp; command form
`python3 tools/registry-replay.py --project kana.json --out outN --max-stream-bytes N --json`):

| limit | exit | finding_ids | refused_rows | bundle published |
|------:|-----:|-------------|--------------|------------------|
| 12 (named) | 1 | `['STREAM_LIMIT']` | `['kana-five']` | no |
| 15 (named) | 0 | `[]` | `[]` | yes |
| 4 | 1 | `['STREAM_LIMIT']` | `['kana-five']` | no |
| 5 | 1 | `['STREAM_LIMIT']` | `['kana-five']` | no |
| 14 | 1 | `['STREAM_LIMIT']` | `['kana-five']` | no |

Readings:

- **limit 12 → refused.** If STREAM_LIMIT counted characters, 5 chars ≤ 12 would
  publish; it refused, so counting is bytes. (Also limit 5 → refused, ruling out
  character semantics a second way.)
- **limit 15 → exit 0, bundle published**, retained stdout in
  `out15/bundle.json` is intact `'あああああ'` (5 chars / 15 bytes). 15 bytes == limit
  passes ⇒ strict `>`, matching the selftest's `stream-at-limit` case (8 ASCII bytes at
  limit 8 → exit 0, `registry-replay.py:203`) and `measure.py` K9
  `stream-limit-refused` (67-byte stdout at limit 16 → STREAM_LOCK refusal expectation,
  `.ufo/evidence/round-24/measure.py:175`).
- **Refused projections write nothing**: only `out15/` exists
  (`bundle.json`, `expected.json`, `live-dependent.json`); `out4/5/12/14/` were never
  created — consistent with `publish()` returning the report unchanged when `bundle is
  None`.

## Smallest safe correction

None. Byte-counting is the named, documented behavior; the boundary and refusal path
behave exactly as the code and selftests specify. A character-based limit would be a
contract change, not a fix, and is out of scope for this wave.

## Limits of what was checked

- Exercised stdout; stderr shares the identical loop body (`registry-replay.py:93-98`)
  and the `stream` selftest case covers it with ASCII [code-cited, not re-run].
- `surrogateescape` at `:96` means lone surrogates from invalid-byte decoding
  (U+DC80–DCFF) also encode to 3 bytes each under this limit [code-cited inference;
  not empirically probed — outside the named fixture].

## Compliance

Runs executed only in `/tmp/LabStreamBytes-r24` (clone) and `/tmp/LabStreamBytes-lab`
(fixtures/outputs). Only file written outside /tmp: this report. No git write
commands in the lane; no tools installed (nothing to record). No selftest, gate, or
registry battery was run in the lane repo.
