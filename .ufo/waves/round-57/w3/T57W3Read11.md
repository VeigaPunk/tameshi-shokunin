# T57W3Read11 — Round-13 gate/probe registry

- Heading: `### Round-13 gate/probe registry`; C0b `adf87899c70d616140a81185a8f9acbbdfb30392`.
- Frozen round-18 sectionize: lines **1590–1605**, SHA256 `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`.
- Recommendation: **verified-record**. No false statement or failing prescribed command found.
- Axes: calibration accuracy, command executability, pointer integrity, frozen-byte preservation.

## Executed sweep

All commands ran from the detached C0b scratch clone; `TMPDIR` was the seat scratch directory. Full commands, stdout, stderr and exits are retained in the JSON and numbered receipts.

| Command | Exit | Observed output |
|---|---:|---|
| `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 | six legs; one unchanged, five changed, zero unavailable; result_reuse=not_established |
| `python3 tools/pin-disposition.py --selftest` | 0 | SELFTEST: PASS (19/19) |
| `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 | metadata_consistent reason=ok; four frozen inputs |
| `python3 tools/witness-metadata.py --selftest` | 0 | SELFTEST: PASS 39/39; negative controls include exit-1 metadata failures and exit-2 unavailable/tampered cases |
| `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read11/pointer-sweep.py` | 0 | POINTER_AND_CLAIM_SWEEP_PASS |
| `python3 tools/pin-disposition.py` | 2 | invalid_input / invalid_usage (expected negative control) |
| `python3 tools/witness-metadata.py` | 2 | required mode usage error (expected negative control) |

The retained `T57W3Read11-receipts/pointer-sweep.py` loads the frozen sectionizer, fetches SKILL.md with `git -C ... show C0b:SKILL.md`, calls `m.sectionize(raw)`, and prints `sec['start'], sec['end'], sec['sha256']`. It checks every named path, the seventh-case heading, source supersession rows, retained PIT item-4/5 text, producer identity, and four frozen round-12 byte comparisons against the assigned base. It also executes witness-metadata against an isolated tree containing only the companion and four frozen inputs: exit 0 without expected.json, supporting the row's explicit nondependency.

Historical producer hash `249d9dcd…93d43f1a` matches the frozen summary/companion; current producer hash `f2bb50c7…978bf261` differs as documented. All four frozen inputs match the assigned base byte-for-byte. Source S048 supersedes S047 as stated; S266 now refreshes S048's anchor/quote only, retaining the same prioritisation distinction. No contradictory claim was found in the inspected neighboring section and seventh-case heading.

## Residual risk and verification gaps

The disposition entry's literal absolute --root intentionally reads live sibling files/git, not a fleet snapshot at C0b; the tool and manifest were read from C0b. It does not execute sibling gates or establish result reuse. Selftests exercise their bounded cases, not universal correctness. Frozen hashes establish preserved recorded identity, not producer authentication.

LSP was unavailable (`xd://lsp`: No such tool); definition and diagnostics review used source ranges and literal searches, not semantic proof. No runtime continuity or saturation claim is made by this scoped section. No tools installed/upgraded; no SKILL.md or frozen lane evidence modified.

## Self-evaluation

Accuracy 4/5: captured outputs and frozen hashes support the recommendation; live fleet observations are explicitly time-dependent. Completeness 4/5: all four prescribed commands and named pointers checked; no semantic LSP available. Clarity 4/5: summary table links to full receipts; raw JSON is verbose by design. Actionability 5/5: report and machine record are ready for L1 binding. Conciseness 4/5: evidence repeats select receipt summaries for independent reading. Overall 4.2/5. Highest-impact improvement would be an available semantic LSP; no missing prescribed command remains. The user should agree with the bounded assessment.
