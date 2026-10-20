# X12ToolPinMap — tools/* digest pin map at 98bea7da

Deliverable: `.ufo/evidence/round-17/tool-pin-map.json` (schema `tameshi-tool-pin-map-v1`, written).

## Method (all executed)

- `git ls-tree -r --name-only 98bea7da -- tools/` → 7 tools.
- `git show 98bea7da:<tool> | sha256sum` → current digests.
- `git log --format=%H 98bea7da -- tools/<f>` + `git show <c>:<f> | sha256sum` → 16 distinct digests; verified no digest is shared across tools.
- `git grep <64-hex> 98bea7da -- .ufo/evidence SKILL.md corpus SCORECARD.md` for each digest → 129 full-digest sites; plus an 8-hex prefix pass over SKILL.md/SCORECARD.md/corpus/** → 91 prose anchors (truncated `sha256 …` citations).
- Live classification by reading tool sources at the rev (grep `sha256`, `derived_from`, `RUNNER`, `REQUIRED_RECEIPTS`) and the SKILL.md registries (rounds 12, 13, 14-historical, 15, 16).

## Result — the only live-verified pins

Exactly **two** carriers pin tool digests that a registered command re-hashes against the live tree:

1. `.ufo/evidence/round-13/expected.json` `inputs{}` — consumed by registered gate
   `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
   (integrity-first `expected_inputs` pass, evidence-disposition.py:1186-1195; sorted order → tools/bash-witness-study.py, tools/mutate-and-run.sh, tools/pin-disposition.py, tools/witness-metadata.py).
   Pins: `49e9e5e2` (bash-witness), `29725397` (pin-disposition), `df339068` (witness-metadata) **current**, and `75ed934d` (mutate-and-run) **stale → exit 2 `expected_input_digest_mismatch`, by design since round 16** (SKILL.md round-15 registry, disposition row).
2. `.ufo/evidence/round-12/BashWitness/declaration.json` `inputs.runner.sha256` (`75ed934d`) — consumed by registered probe `python3 tools/bash-witness-study.py count` which live-hashes `tools/mutate-and-run.sh` (bash-witness-study.py:556-561) → currently refuses `Cannot 'runner-drift'`; it also asserts `PIN_BASH` read from live runner text (:563-566).

Everything else is **historical-receipt** (all other `.ufo/evidence/**` hits — receipts, harness scripts `verify.py`/`measure.py`, archived `capture-context.py`) or **prose** (SKILL.md/SCORECARD.md/corpus truncated anchors, and `.ufo/evidence/round-13/pin-manifest.json` `derived_from.sha256` — **informational only: `pin-disposition.py` has no code path that reads `derived_from`**).

## Acceptance: live verifiers per edited tool

| Tool | Live verifier whose verdict changes on edit | Effect at rev 98bea7da |
|---|---|---|
| `tools/mutate-and-run.sh` | `evidence-disposition … dispositions.json` (+ the `dispositions-before.json` recipe invocation); `bash-witness-study.py count` | **No verifier can flip on further edits** — both are already red on the stale `75ed934d` pin (exit 2 / `runner-drift`). Only a byte-revert to `75ed934d…` would change verdicts (to the next-ordered check). Editing is verdict-safe; the r17 v2 `historical_inputs` manifest is the designed repair. |
| `tools/pin-disposition.py` | `evidence-disposition … dispositions.json` via `expected.inputs` pin `29725397` (currently matching) | **No observable verdict change**: any edit makes the pin mismatch, but the gate already exits 2 on the earlier-sorted `tools/mutate-and-run.sh` input, so exit/id stay `2 expected_input_digest_mismatch` (only the embedded `observed/expects` path field would differ). |
| `tools/evidence-disposition.py` | **none** | No live pin anywhere; only historical receipts (`round-14/expected-runtime-final.json`, `verification-final.json`, corpus lesson prose). Byte changes flip no digest verdict. |

Not edited this wave but same exposure: `tools/witness-metadata.py`, `tools/bash-witness-study.py` — same `expected.inputs` live pin, masked the same way. `tools/context-capture.py`, `tools/repeat-control.py` — no live pin (`context-capture.py --check` compares receipt-embedded `tool_sha256` to a frozen constant, never live file bytes, context-capture.py:1212-1216).

## Risks / notes

- The `expected.inputs` verification order is sorted; `tools/mutate-and-run.sh` masks the other three tool pins. After v2 moves runner pins to `historical_inputs`, the three still-current pins become the first live check — editing pin-disposition.py/witness-metadata.py/bash-witness-study.py then WOULD flip the gate red unless v2 also historical-pins them. The builder of `.ufo/evidence/round-17/dispositions.json` must pin tool inputs at the post-edit digest (or move them to `historical_inputs` too).
- `repeat-control.py` has zero digest history beyond current and only receipt/prose pins — freest tool.
- 91 prose prefix anchors (`597e1419…`/`75ed934d…`/`b56c6e57`/`cf41efaa…`/`89722ddb…`/`0673d2e5…` etc.) mean runner edits routinely orphan prose anchors — consistent with the round-16 errata's own "anchors written as tool sha256 values" finding.

## Tooling installs

None (all read-only git/python3 on host).

Verdict: **built** — `.ufo/evidence/round-17/tool-pin-map.json` written; the only live pin carriers are `round-13/expected.json` (via the disposition gate) and `round-12/BashWitness/declaration.json` (via the witness probe); no edited tool can flip a digest verdict at the current rev.
