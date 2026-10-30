# T57W3Read06 — verified-record

Heading: `## The operator's runbook and the six-leg regression (round 10, measured)`

Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`. Frozen round-18 sectionizer: lines **1312–1320**, SHA-256 `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7`.

## Findings

None. The assigned nine-line section is a dated introduction, not the following subsections. Its round-7 replay, round-8/9 four-leg debt, and round-10 runbook/embedding claims resolve in the C0b sources and committed round-10 artifacts. The current registry correctly invokes the canonical `tools/mutate-and-run.sh --regression`; the six-leg historical claim does not contradict today's ten legs.

## Executed sweep

Full commands, stdout, stderr and exit codes are recorded in the adjacent JSON and `T57W3Read06-receipts/`:

- `01-section-identity.json`: Python `importlib` loads the frozen round-18 measure, reads `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`, calls its `sectionize`; rc 0, printed the bounds/hash above and entire section.
- `02-regression.json`: `bash /fast/scratch/hyaku/tameshi-r57/T57W3Read06/clone/tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r57/T57W3Read06/regression`; rc 0, `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)`. All tables exact, no inconclusives; includes checklist and claims legs.
- `03-pointer-claim-sweep.json`: Python checks registry, runbook, round-10 lesson, tool embedding, earlier SKILL receipts; `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read06/clone show 606716f:<path>` reads historical tool/runbook; rc 0. Historical tool is r10-2 with recorded T8-1/T8-2 specs and legs 5/6; runbook identifies T10-1.
- `04-original-debt.json`: Python prints original ledger ER-2/ER-4 lines 281, 282, 318, 341, 350; rc 0. Original receipt says `cases=4 passed=4`; caveat (a) explicitly names missing cases 5/6 and forbids re-cutting.

## Limits and environment

LSP unavailable (`xd://lsp` not mounted); source checks are literal, not semantic-reference proof. Detached shared scratch clone at C0b; read-only symlinks supply sibling git object stores. No lane content edits, installations, or updates. No other section, resume route, saturation claim or admission is certified. Historical operator-discovery experience is supported by dated records rather than directly reproduced.

Axes: calibration, pointer validity, executable operability, historical fidelity, non-mutation. Self-evaluation: accuracy/completeness 4/5 because historical operator experience cannot be directly replayed; clarity/actionability/conciseness 4/5 because full command text is retained in JSON rather than duplicated here.
