# RunReplayGate — round24 W1 replay-gate + round23 pinned-row re-run

## Verdict
PASS — all three gated runs reproduce exactly. No defect found; no counterexample produced.
- Round-24 replay gate: exit 0, clean report, byte-identical stdout to the retained gate record.
- `command-binding-frozen-clean-pinned`: exit 0, `"finding_ids": []`, pinned `bundle_sha256` reproduced.
- `command-binding-source-read-red-pinned`: exit 1, `"finding_ids": ["ARGV_MISMATCH"]`, pinned `bundle_sha256` reproduced.
- No tool installs performed (python3 preexisting; directive recorded as no-op).

## Exact runs (cwd: /tmp/TameshiR24-2.RunReplayGate-r24, detached HEAD `c8c5b88c8e961a929cdc351b95a7074c76958909`, verified via `git rev-parse HEAD`)

### R1 — round-24 replay gate
- argv: `python3 tools/command-binding.py --bundle .ufo/evidence/round-24/replay/bundle.json --expected .ufo/evidence/round-24/replay/expected.json --json`
- exit: **0**
- stdout sha256: `1988a3256e8e4448771850956e563601e345a486ec72b51a68b1e373e8a345a3`
- decisive stdout (whole line): `{"bundle_sha256": "4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}`
- stderr: empty.

### R2 — pinned row `command-binding-frozen-clean-pinned` (tools/registry.json:971-978)
- argv: `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json`
- exit: **0** (pinned expect: exit 0)
- stdout sha256: `35b840a5ed3c4d04196c254fc9378bc3bff1a7eb061f7e3a6e506dcdf820ed90`
- decisive stdout: `{"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}` — both pinned `stdout_contains` needles present (`"finding_ids": []`, `"bundle_sha256": "3d6c99b7…"`).
- stderr: empty.

### R3 — pinned row `command-binding-source-read-red-pinned` (tools/registry.json:981-988)
- argv: `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/source-read-bundle.json --expected .ufo/evidence/round-23/source-read-expected.json --json`
- exit: **1** (pinned expect: exit 1)
- stdout sha256: `7314a8ee75104cebbfcb4d803cd313f2b245ee13d5f281efe6e1509a10cf4ea4`
- decisive stdout: `{"bundle_sha256": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf", "exit": 1, "finding_ids": ["ARGV_MISMATCH"], "schema": "command-binding-report-v1"}` — both pinned needles present.
- stderr: empty.

## Digests
Fixtures (clone, `sha256sum`):
- `.ufo/evidence/round-24/replay/bundle.json` = `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`
- `.ufo/evidence/round-24/replay/expected.json` = `8fc9342ed1f07beb0e930f7a46fb0081a825e35494f43608ea5c2396f13b0868`
- `.ufo/evidence/round-23/replay/bundle.json` = `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9` (== pinned expect)
- `.ufo/evidence/round-23/replay/expected.json` = `0831c9c820488dc9d9096c90aade44217b6b615501fae7810e6fce414cb2a0a1`
- `.ufo/evidence/round-23/source-read-bundle.json` = `db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf` (== pinned expect)
- `.ufo/evidence/round-23/source-read-expected.json` = `70f357e354c4badb22f974070ccf37dfda512103c3cf3ab93297a3ea27cb5dc8`

Tool blobs at REV (`sha256sum`):
- `tools/command-binding.py` = `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` (== retained `tool_sha256`)
- `tools/registry-replay.py` = `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` (== retained `instrument_sha256`)

## Falsification sweep — what I checked, none found
1. Byte-fidelity vs retained run: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-24/replay-gate.json` records stdout identical to my R1 stdout (same JSON + trailing newline) at exit 0, with `revision_of_tool: d2eaecd4…`; the tool blob at my REV c8c5b88c is sha256-identical (`9230c68e…`), so the retained gate run is faithfully reproduced. The original run's argv used absolute paths from the real repo cwd; I re-ran with repo-relative paths in a private clone — same bytes out.
2. Round-24 `expected.json` declares `bundle_sha256` `4f424023…`; observed report echo matches. No exit-declaration drift.
3. Both pinned rows' `expect` blocks (exit + both stdout needles) satisfied simultaneously in single runs; red row is genuinely red (exit 1) and clean row genuinely clean (exit 0) at the same tool blob — binding works in both directions, not just one.
4. Fixture digests equal the digest literals embedded in registry pins and expected files — no fixture/pin drift.
5. Superseded round23 rows (registry.json:941,952, status `superseded`) intentionally not executed; assignment names only the two pinned pairs.
6. No runs were executed in /home/vgpnk/Projects/shokunin/tameshi-shokunin; all execution inside the private clone only. No writes outside this report.

## Notes (observations, not defects)
- The wave card places `replay-command.json`/`replay-gate.json` under `.ufo/evidence/round-24/replay/`; they actually live one level up at `.ufo/evidence/round-24/replay-{command,gate}.json` (sibling of the `replay/` dir). Files exist and check out; path label only. Not corrected (bounds forbid production edits).
- Retained records pin revision `d2eaecd4…` vs assignment REV `c8c5b88c…`; tool blobs are identical so reproduction validity is unaffected.

## Smallest safe correction
None required. If the wave card is ever regenerated, fix the `replay-command.json`/`replay-gate.json` path to `.ufo/evidence/round-24/` (parent of `replay/`).
