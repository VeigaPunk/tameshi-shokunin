# T57D4Read02 — documentary audit

Axes: claim/receipt agreement; pinned provenance; reproducibility; defensive scope.

## Findings, by severity

**Low — replay clone provenance is not retained.** `w3/T57W3Read02.md:20–21` and its JSON name C0b. The 46 retained commands never record creation/checkout or HEAD of the tameshi clone, nor the hash of its `SKILL.md` consumed by driver commands 17–20. Command 39 hashes a separate `git show C0b:SKILL.md`, not that clone input. Thus the assigned section pin is correct, but the replay manifests and pointer-source clone are not independently revision-bound by this receipt set. Missing provenance is not evidence that a wrong revision was used. Qualify the replay-to-C0b claim pending existing provenance evidence.

**Low — exact survivor fixture inputs are unavailable.** `w3/T57W3Read02.md:19,29,33` describes reconstructed survivor probes and scratch removal. Commands 22–28 retain commands/results, but the six retained files contain no probe/probe2 TSVs, host-file bytes/modes or construction recipe. The retained driver constructs mutants and runs selftests, not these off-suite fixtures. Output-level non-equivalence is supported; exact fixture reproducibility from these receipts alone is not. State that limit rather than treating the off-suite setup as fully retained.

These are evidence gaps, not demonstrated recipe failures. No high/medium defect established in this scope.

## Bounded agreement

- Read the corresponding committed section only through `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`. Lines 159–273 end before the taxonomy heading. Applying the documented frozen section normalization gives SHA-256 `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da`, exactly the JSON/Markdown metadata. Retained section matches after stripping trailing blank lines (its extra blank line is normalization, not drift).
- JSON command array equals retained `commands.json`: 46 records. Both sweep bundles contain 11 matching metadata/results rows and streams. JS: 8 killed, D2/D10 survived, no inconclusive; all summaries retain denominator 43. Bash: 8 killed, B5/B10 survived, no inconclusive; every stream has 16 enumerated rows, including 2 skips. Every retained failing label occurs in its stream. B4 explicitly reports expected/got exit 1 with the missing `SURFACE LINK` token.
- Commands 22–28 support the reported survivor output differences and exits. Before/after revision, porcelain, digest and stat output pairs all match; both cmp records exit 0. Those are endpoint observations only.
- Independent read-only `git show` of the two historical source blobs confirms the reported SHA-256/size: JS `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 43273 bytes; bash `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, 44212 bytes.
- Retained command 46 prints `POINTER SWEEP: PASS` and round-16 values: 18 commands, zero blocking gaps, seven minor gaps. Its path/range checks establish existence/bounds only, not semantic citation correctness.

## Audit commands and observed output

The sibling JSON preserves the exact documentary Python query used for the findings. Its observed output was:

```text
commands 46 match True
clone HEAD at cand False
files ['bash-sweep.json', 'commands.json', 'js-sweep.json', 'mutate_driver.py', 'section.txt', 'self-evaluation.json']
fixture construction candidates: command 40 mkdir js/copy-check/evidence; command 43 mkdir bash/copy-check/evidence
```

The complete command strings for those two mkdir operations are retained in the JSON. Findings also use direct source reading of retained `mutate_driver.py:1–35`, which contains no off-suite fixture construction. No historical command was replayed.

## Residual risk and verification gaps

Current candidate integration remains **UNVERIFIED**. This documentary comparison grants neither admission nor monitor credit and does not establish 64/64 NO-HARM, runtime routing/saturation, or resume continuity. The assigned section changes none of those mechanisms. No candidate gate, mutant, probe, test or build was executed; no credentials or external targets were used. No production/frozen file was edited. LSP is unavailable (`read xd://lsp`: `No such tool`); JSON/Markdown/source inspection is not semantic reference proof. Retained results are unauthenticated historical observations, not independent execution evidence. No tool installation/update.

Self-evaluation: accuracy 4/5 (historical execution cannot be authenticated); completeness 4/5 (input provenance and probe setup remain unavailable); clarity 4/5 (separates observations from gaps); actionability 4/5 (specific qualification requested, no prohibited rerun); conciseness 4/5 (evidence detail retained for audit). Overall 4.0/5. Main improvement is obtaining already-existing clone/input receipts, if any; no new execution authorized.
