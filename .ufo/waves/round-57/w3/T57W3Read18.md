# T57W3Read18 — ### Round-26 gate/probe registry — report interop

Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`

Frozen round-18 sectionize: lines 2175–2214, SHA256 `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`.

## Findings (minor; operational reds)

- **ENTRY_WITNESS_CHECK_DRIFT** (`SKILL.md:2185`): The documented bash-witness-study check command returns FAIL at C0b because the current runner differs from the frozen declaration. This is an operational red entry, not an incorrect exit-map claim; frozen evidence must not be rewritten.
  Command: `python3 tools/bash-witness-study.py check`
  Exit: 1
  Output:

```text
WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
WITNESS_CHECK: FAIL (1 problems; 96 files covered)

```
Receipt: `T57W3Read18-receipts/entry-02.json`.

- **ENTRY_REGISTRY_NOT_ALL_HELD** (`SKILL.md:2197`): The documented registry walk runs but returns failed: 51/53 active rows held. sources-census and verify-round15 each return 1 rather than expected 0. Both MTE rows hold in a correctly named fleet mirror. The section correctly documents exit 1 as failed; this is not evidence of a registry-check implementation defect.
  Command: `python3 tools/registry-check.py --rev HEAD --json`
  Exit: 1
  Output:

```text
REGISTRY_CHECK: held=51/53 superseded=7
ROW sources-census expect=0 got=1 differs
ROW verify-round15 expect=0 got=1 differs
```
Receipt: `T57W3Read18-receipts/entry-01.json`.

## Sweep and limits

- Axes: factual calibration, runnable commands, pointer integrity, lane immutability.
- All 30 documented selftests passed, including the exact context 49/49, registry 51 cases, repeat-control 29 cases, MTE 17/17 and tally-v3 35/35 claims. Initial tally-v3 timeout at 240s was a reviewer timeout; retry completed successfully in 332.1s.
- Standalone pinned-jsonschema MTE check passed 10/10 against the specified fleet root. No unsupported hermeticity or saturation claim is made.
- All literal file/directory pointers resolved. Frozen sectionize produced lines 2175–2214 and the recorded SHA.
- Initial registry sweep from a scratch directory named clone lacked the fleet sibling layout (49/53). Retried from a correctly named tameshi-shokunin clone with read-only sibling links: 51/53. Initial MTE/setup failures are not attributed to C0b.
- Settlement round-41 returns 1 exactly as documented (UNSETTLED); not a finding. Pin-disposition returning changed/not_established is also a supported outcome, not a false claim.
- LSP unavailable: xd://lsp returned No such tool. Text inspection is fallback, not semantic proof.
- Parameterized APIs were exercised by their committed selftests; concrete entry checks additionally covered registry, witness check, context, disposition, golden, pbt 400 cases, pin disposition, receipt measure/window, repeated controls, round21 c1, three tally audits, trace inputs, settlement both outcomes, witness metadata, census v3/v4/base, and env-diff 9/9. Registry sweep also exercised its committed binding/accounting entry fixtures.
- No tooling installed or upgraded. No lane monitored files, frozen evidence or SKILL.md changed. No staged content fixes: the two operational reds are for L1 adjudication, not automatic repinning.

## Commands run

Full stdout/stderr, exit codes and cwd are in the adjacent JSON and receipt files.

| Command | Exit |
|---|---|
| `python3 tools/bash-witness-study.py selftest` | 0 |
| `python3 tools/command-binding.py --selftest` | 0 |
| `python3 tools/context-capture.py --selftest` | 0 |
| `python3 tools/env-diff.py --selftest` | 0 |
| `python3 tools/evidence-disposition.py --selftest` | 0 |
| `python3 tools/golden-verdict.py --selftest` | 0 |
| `python3 tools/mte-interop.py --selftest` | 0 |
| `bash tools/mutate-and-run.sh --selftest` | 0 |
| `python3 tools/pbt-staged-id.py --selftest` | 0 |
| `python3 tools/pin-disposition.py --selftest` | 0 |
| `python3 tools/receipt-measure.py --selftest` | 0 |
| `python3 tools/receipt-window.py --selftest` | 0 |
| `python3 tools/registry-check.py --selftest` | 0 |
| `python3 tools/registry-replay.py --selftest` | 0 |
| `python3 tools/repeat-control.py --selftest` | 0 |
| `python3 tools/round21-measure.py --selftest` | 0 |
| `python3 tools/shrink-case.py --selftest` | 0 |
| `python3 -I tools/staged-id-guard.py --selftest` | 0 |
| `python3 tools/tally-audit-v2.py --selftest` | 0 |
| `python3 tools/tally-audit-v3.py --selftest` | 124 |
| `python3 tools/tally-audit.py --selftest` | 0 |
| `python3 tools/trace-inputs.py --selftest` | 0 |
| `python3 tools/wave-accounting.py --selftest` | 0 |
| `python3 tools/wave-parent-settle.py --selftest` | 0 |
| `python3 tools/wave-route-mix.py --selftest` | 0 |
| `python3 tools/witness-metadata.py --selftest` | 0 |
| `python3 tools/write-path-census-v2.py --selftest` | 0 |
| `python3 tools/write-path-census-v3.py --selftest` | 0 |
| `python3 tools/write-path-census-v4.py --selftest` | 0 |
| `python3 tools/write-path-census.py --selftest` | 0 |
| `python3 tools/tally-audit-v3.py --selftest` | 0 |
| `python3 tools/registry-check.py --rev HEAD --json` | 1 |
| `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` | 0 |
| `python3 tools/registry-check.py --rev HEAD --json` | 1 |
| `python3 tools/bash-witness-study.py check` | 1 |
| `python3 tools/context-capture.py --check` | 0 |
| `python3 tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/evidence/round-18/dispositions.json` | 0 |
| `python3 tools/golden-verdict.py --check-entry /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/corpus/knowledge/golden-comparison-verdict.md` | 0 |
| `python3 tools/pbt-staged-id.py --guard /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/tools/staged-id-guard.py --seed 1 --cases 400 --dump /fast/scratch/hyaku/tameshi-r57/T57W3Read18/pbt.jsonl` | 0 |
| `python3 tools/pin-disposition.py --manifest /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 |
| `python3 tools/receipt-measure.py --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin --rev adf87899c70d616140a81185a8f9acbbdfb30392 --json` | 0 |
| `python3 tools/receipt-window.py --contract /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/evidence/round-20/contract.json --receipts /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/evidence/round-20/final/receipts.json` | 0 |
| `python3 tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read18/repeat -- python3 -c 'print("stable")'` | 0 |
| `python3 tools/round21-measure.py --claim c1 --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin --rev adf87899c70d616140a81185a8f9acbbdfb30392 --json` | 0 |
| `python3 tools/tally-audit-v2.py --runner /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/tools/mutate-and-run.sh` | 0 |
| `python3 tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/tools/mutate-and-run.sh` | 0 |
| `python3 tools/tally-audit.py` | 0 |
| `python3 tools/trace-inputs.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin --out /fast/scratch/hyaku/tameshi-r57/T57W3Read18/trace.json -- python3 -c 'print("trace")'` | 0 |
| `python3 tools/wave-parent-settle.py --receipt /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/waves/round-40/settlement-receipt.json` | 0 |
| `python3 tools/wave-parent-settle.py --receipt /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/waves/round-41/settlement-receipt.json` | 1 |
| `python3 tools/witness-metadata.py --check --lane-root /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin --companion /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json` | 0 |
| `python3 tools/write-path-census-v3.py --file /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/tools/context-capture.py` | 0 |
| `python3 tools/write-path-census-v4.py --file /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/tools/context-capture.py` | 0 |
| `python3 tools/write-path-census.py --census /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin` | 0 |
| `python3 tools/env-diff.py --contract /fast/scratch/hyaku/tameshi-r57/T57W3Read18/tameshi-shokunin/.ufo/evidence/round-21/c2-contract.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read18/envdiff/receipt.json --jobs 3` | 0 |

Frozen sectionization command and output: `T57W3Read18-receipts/sectionize.json`. Pointer results: `T57W3Read18-receipts/pointers.json`.

Recommendation: **gap-minor**; adjudicate the two red entries, do not rewrite historical pins. This report is not an admission or runtime verdict.

Self-evaluation: accuracy 4/5 (captured outputs; red entries do not prove incorrect exit maps); completeness 4/5 (all selftests and broad entry sweep, parameterized modes use committed fixtures); clarity 4/5 (reds separated from environment effects); actionability 4/5 (exact commands and receipts, no speculative fix); conciseness 4/5 (long command inventory is audit evidence). Overall 4.0. Improvement: maintain the fleet-mirror layout from the first sweep.
