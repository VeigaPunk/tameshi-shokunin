# T58W2Read09 — verified-record

C0: `8063d0a551fc5b3cb5a2d397da7353af53444534`

Section: **Round-26 gate/probe registry — report interop**, lines 2175–2214.
SHA256: `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`.

## Findings

No new false statement or unexpected command failure found. All 30 listed selftests passed with their documented tallies. Every extracted concrete pointer resolved. MTE live check passed 10/10, without implying hermeticity or admission of C2.

## Calibration and residual risk

- `bash-witness-study.py check` returns 1: runner digest drift. This is explicitly disclosed at SKILL.md:1550 and is consistent with the table's verdict map, not a new defect.
- First tally-v3 selftest exceeded the review harness's 300-second timeout; a 1200-second allowance completed 35/35. Both receipts retained.
- A reviewer-invented registry selector returned 2; corrected to an installed row and obtained 0. Not a documentation defect.
- Negative controls returned their documented 1 exits.
- Full replay `--run` was not executed because it can reach writable live sibling symlinks; its selftest passed 10/10. Registry walk used one installed row. Alternative runner target mode and optional argument combinations were not separately exercised; no claim that all combinations passed.
- LSP device unavailable (`No such tool: xd://lsp`); text searches were not treated as semantic proof.

## Reproduction / evidence

Run `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read09-receipts/sectionize.py`.
Output: `2175 2214 cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`.

All command strings, cwd, exact stdout/stderr and exits are in the adjacent JSON and `T58W2Read09-receipts/commands.json`. Full section text, pointer sweep and synthetic entry fixtures are also preserved there. The supplied base-to-C0 SKILL.md diff was empty.

No tools installed; no source edits. Seat scratch deleted.

Self-evaluation: accuracy 4/5 (live sibling state is not frozen); completeness 4/5 (unsafe full replay intentionally unrun); clarity 5/5 (expected failures separated); actionability 5/5 (commands and exact outputs retained); conciseness 4/5 (full receipts intentionally verbose). Overall 4.4/5. No admission judgment made.
