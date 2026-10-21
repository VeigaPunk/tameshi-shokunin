# RunRulerBase — round24 ruler reproduction at base rev

## Verdict

CONFIRMED. before.json reproduces exactly at REV=6a1821a8897eea6e7d9669292160ec9593669409:
`discriminated: 1 / total: 11`, ruler exit 1, and the only discriminating predicate is K4
(`stdout-any-token`, caught by selftest case `all-of-tokens`). No difference from the
recorded baseline: rerun stdout is **byte-identical** to `before.json`'s recorded stdout,
and all 11 rows compare equal field-for-field.

## Axes (godspeed)

- Reproducibility: same instrument bytes + same rev, independent lane.
- Determinism: row-level and byte-level equality across runs.
- Faithfulness: argv/cwd shape mirrors the recorded baseline procedure.

## Procedure (exact)

- Clone: `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/RunRulerBase-r24 && git -C /tmp/RunRulerBase-r24 checkout -q --detach 6a1821a8897eea6e7d9669292160ec9593669409`
  → `rev-parse HEAD` = `6a1821a8897eea6e7d9669292160ec9593669409`, `status -sb` = `## HEAD (no branch)` (clean).
- Instrument nuance: `.ufo/evidence/round-24/measure.py` is **not present in the base-rev tree**
  (`git cat-file -p 6a1821a…:.ufo/evidence/round-24/measure.py` → `fatal: path … does not exist`);
  the ruler is the frozen working-tree instrument. I copied it into my lane and verified bytes:
  `sha256sum` = `0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64`, equal to
  `before.json.instrument_sha256` and to the working-tree original (before.json argv used the
  shared-checkout instrument path; my lane path differs, bytes do not).
- Run 1 (bash): argv `python3 /tmp/RunRulerBase-r24/.ufo/evidence/round-24/measure.py --repo /tmp/RunRulerBase-r24`,
  cwd `/tmp/RunRulerBase-r24`, exit `1`, wall ~11.4 s.
- Run 2 (calibration compare, via eval kernel subprocess): same argv/cwd, exit `1`.

## Decisive output

- Summary: `"discriminated": 1`, `"total": 11`, `"schema": "tameshi-r24-hardening-v1"`; `EXIT=1`.
- K4 (only discriminated row): `"exit": 1`, `"failing_cases": ["CASE all-of-tokens FAIL"]`,
  tail `... CASE duplicate-json-key PASS\nCOMMAND_BINDING_SELFTEST: 37/38 pass\n`.
- K1–K3: `anchor_count: 1`, `control_exit: 0`, mutated selftest still `38/38 pass`, `discriminated: false`.
- K5 `frozen-clean-substitution` / K6 `source-read-red-substitution`: control and substituted both
  `held: true` (`command-binding-frozen-clean`, `command-binding-source-read-red`) → not discriminated.
- K7–K11: `"reason": "tool-absent"` — `tools/registry-replay.py` does not exist at base.

## Baseline cross-check

`python3` compare of parsed `before.json.stdout` vs rerun stdout:
`rows exactly identical (11/11): True`; `rerun stdout byte-equal to before stdout: True`;
per-row table shows K4 `before=True rerun=True`, all others `False/False` with `row_identical=True`.
Recorded baseline fields: exit 1, revision `6a1821a…`, note "K4 already discriminated at base
(selftest all-of-tokens case), so before is 1/11" — all consistent with observation.

## Tooling directive

No tools installed or upgraded (none needed; python3 present).

## Bounds kept

Writes: this report only. All execution (clone, instrument copy, both ruler runs, kernel compare)
inside `/tmp/RunRulerBase-r24`; nothing executed against the shared checkout; no git write
commands; no subagents; no labrat needed (no falsifiable defect surfaced — result is a clean
confirmation, not a counterexample hunt miss).
