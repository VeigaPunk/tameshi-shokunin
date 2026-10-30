# T58W2RevSrc2 — S287 independent re-open

Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`. Axes: source identity, quotation fidelity, semantic support, reproducibility.

## Findings

None in scope. Recommendation: verified-record (not an admission).

Independently fetched [the PDF](https://pdf.dfcfw.com/pdf/H3_AP202503221646031757_1.pdf) with curl and converted it with pdftotext 26.10.0. Download: **5,409,054 bytes**, SHA-256 `531abe11d23f2e3703925a98fabd52ade3793832c1959149d1a8fb8d7d5bd161`. These match S287 and the entry's recorded size/hash prefix. Title and author match extracted lines 1–2.

`cmp /fast/scratch/hyaku/tameshi-r58/T58W2RevSrc2/dfcfw-deck.txt /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/l1/sources/dfcfw-deck.txt` exited **0**, no output. Both extract SHA-256 values: `eaa3d03ac271569300d1417dae420555ce2fb1ecdb7fc4b18600f2692f6f5f7e`.

Reopened lines 230–241:

```text
230: 挑战3：等价变异体
231: • 等价变异体：变异后的程序与原始程序在功能上完全相同，即它
232: 们对所有可能的输入产生相同的输出。
233: • 等价变异的危害：
234: • 增加测试成本
235: 
236: for (int i = 0; i < 10; i++)
237: for (int i = 0; i != 10; i++)
238: 
239: • 影响变异分数计算的精确度
240: 
241: • 判断等价变异体是不可判定问题：不存在一个自动算法完美解决
```

All three Chinese quotations occur verbatim in the independently extracted text and C0 knowledge entry. The definition continues on line 232 with “same outputs for all possible inputs”; line 239 supports mutation-score precision harm; line 241 states general undecidability/no perfect automated algorithm. C0 `corpus/SOURCES.md:162` accurately scopes S287. C0 `corpus/knowledge/llm-mutant-equivalence-cost.md:22–26,42–44,52–56` preserves that general boundary and does not treat a distinguishing input as a general decision procedure.

## Sweep and receipts

Commands, exit codes and outputs: `T58W2RevSrc2-receipts/commands.json`. Download and independent conversion preserved as `dfcfw-deck.pdf` and `dfcfw-deck.txt`; pinned source documents and structured comparison are beside them. The accompanying report JSON includes the command records and full comparison. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3` showed C0 at HEAD; pinned `git show` reads, not live-tree assumptions, supply the reviewed row and entry. The base-to-C0 source diff was also inspected.

## Residual risk / verification gaps

The deck is a secondary talk source, not an independently checked proof of the undecidability theorem. This review verifies faithful citation, not the theorem itself. S286 and runtime gate behavior are outside this seat's scope. LSP was unavailable (`xd://lsp`: No such tool); literal document comparisons are not semantic caller proof.

No tools installed. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2RevSrc2` deleted before reporting; retained receipts are only in the assigned receipt directory. No lane content changed outside assigned report/receipt paths.

## Self-evaluation

Accuracy 4: quotations and byte identity observed; underlying theorem not independently proved. Completeness 5: independent fetch, conversion, exact line comparison, S287 and C0 entry all covered. Clarity 4: full command output is intentionally separated into receipts. Actionability 5: hashes, exact lines and retained source permit reinspection. Conciseness 4: JSON repeats evidence for machine use. Overall 4.4. Improvement: theorem-proof review would require a separate scope; user should agree the requested source re-open is complete.
