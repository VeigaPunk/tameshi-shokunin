# T58W2RevSrc1 — S286 independent source re-opener

## Findings by severity
None. Recommendation: verified record within this source-only scope, not admission.

Axes: source authenticity; quantitative fidelity; date/digest fidelity; interpretation boundaries.

## Exercised sweep and evidence
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3` returned C0 `8063d0a5` first, followed by `0fdb71d2`, `1d1f70d8`.
- Independent command: `curl --fail --location --silent --show-error --output /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevSrc1-receipts/arxiv-2406.09843.html --write-out 'http_code=%{http_code}\nsize_download=%{size_download}\nurl_effective=%{url_effective}\n' https://arxiv.org/abs/2406.09843`
  Output: `http_code=200`, `size_download=44019`, `url_effective=https://arxiv.org/abs/2406.09843`.
- SHA-256 of independently fetched HTML: `7af7e470fca3ef38e97d858b308dca20e815a4b919c9c235adae4d4f59c4a86e`; sha16 `7af7e470fca3ef38`. Both the 44,019-byte count and digest match S286 (`corpus/SOURCES.md:161`) and the entry's source header.
- Extracted abstract Gate quote: “the LLM-generated mutants have worse non-compilability, duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage points, respectively”. The whole abstract equals the L1 extract after HTML-entity decoding and whitespace normalization. `comparison.json` records `l1_extract_equal=true`, `gate_quote_present=true`.
- Committed entry inspected with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8063d0a551fc5b3cb5a2d397da7353af53444534:corpus/knowledge/llm-mutant-equivalence-cost.md`. All numerical claims (851, 111.29%, 26.60, 10.14, 3.51) appear in the independent abstract; entry lines 16–21 reproduce their roles and units correctly.
- Submission history independently gives v1 `Fri, 14 Jun 2024` and v5 `Thu, 22 Jan 2026`, matching entry line 1. The 2026-10-30 fetch date is consistent with this session but a present fetch cannot independently prove when the historical L1 fetch happened.
- Actual base→C0 diff reviewed; full output saved in `T58W2RevSrc1-receipts/scoped.diff`.
- Entry lines 30–32 correctly decline equivalence conditional on survival; lines 48–58 disclaim measured lane transfer and a completed pilot.

## Residual risk and verification gaps
This checks the abstract, not the paper body, S287, or pilot outcomes. LSP device was unavailable (`No such tool: xd://lsp`); direct Markdown/source comparison is not semantic-reference proof. Initial fetch failed locally with curl 23 because the output directory was missing; retry after creating it succeeded. Initial tag-stripping fused the Abstract label with text; correcting markup spacing produced exact equality, not a source discrepancy.

Receipts: independently fetched HTML, extracted abstract, `comparison.json`, and scoped diff beside this report. Machine-readable report includes commands and outputs.

Cleanup: no scratch/clone created; none remains to delete. No tools installed. No lane source edited.
