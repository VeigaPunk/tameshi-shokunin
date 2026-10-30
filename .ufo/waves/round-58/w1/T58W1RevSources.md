# T58W1RevSources — independent source sample

Axes: source fidelity; metadata reproducibility; sample coverage.

## Findings by severity

None in the independently reopened S286 sample. Recommendation only; no admission or integration action.

Opened https://arxiv.org/abs/2406.09843 independently on **2026-10-30**. Agree with the L1 abstract extract and the S286 draft row at `/fast/scratch/hyaku/tameshi-r58/c0-drafts/sources-append.md:1`.

## Executed sweep and output

All command paths below are absolute. Receipt directory:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevSources-receipts`.

1. `read https://arxiv.org/abs/2406.09843` independently returned the title, seven authors, original publication date 2024-06-14, and the abstract with all four claimed statistics. This reader uses the arXiv API, so raw-byte comparison used a separate fetch:

```sh
mkdir -p /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevSources-receipts
curl --fail --location --silent --show-error https://arxiv.org/abs/2406.09843 --output /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevSources-receipts/arxiv.html
```

Output: exit 0, no stdout. The first fetch before directory creation failed with curl exit 23; the successful fetch above is the evidence used.

2. `wc -c /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevSources-receipts/arxiv.html`

Output: `44019` bytes.

3. `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevSources-receipts/arxiv.html`

Output: `7af7e470fca3ef38e97d858b308dca20e815a4b919c9c235adae4d4f59c4a86e`.

4. Text grep over the fetched receipt for `111\.29|26\.60|10\.14|3\.51|Submitted on|last revised|2026|2024|v5` located:

- line 115: `[Submitted on 14 Jun 2024 ... last revised 22 Jan 2026 (this version, v5)]`;
- line 124: `with 111.29% higher fault detection` and the Gate quote: **“LLM-generated mutants have worse non-compilability, duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage points, respectively.”**

5. Executed Python Eval extraction: select `<blockquote class="abstract mathjax">`, remove HTML tags, HTML-unescape, collapse whitespace, and compare with the L1 file `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/l1/sources/arxiv-2406.09843-abstract.txt`. Output in `T58W1RevSources-receipts/comparison.json`:

```text
bytes: 44019
sha prefix equal: true
v5/revision date present: true
original date present: true
111.29% claim present: true
Gate quote present: true
abstract body equal after whitespace normalization: true
```

Initial whole-extract equality was false solely because removing HTML tags joins `Abstract:Large`, whereas the L1 extract has `Abstract: Large`. Removing the label resolves the difference; no substantive disagreement.

Thus the reopened page corroborates every S286 numerical/date/hash claim tested: 111.29%, 26.60/10.14/3.51 percentage points, v5, 2024-06-14, 2026-01-22, 44019 bytes, and SHA prefix `7af7e470fca3ef38`. Access date is this seat's own 2026-10-30 fetch. Title and author list also agree.

## Residual risk and verification gaps

- Assignment requests one source: S287/S288 were read as draft rows but not independently fetched. Their metadata are unverified by this seat, not asserted correct.
- The lane's equivalence-witness prescription is INFERENCE/policy, not a verbatim abstract claim.
- `read xd://lsp` returned `No such tool: xd://lsp`; no semantic server was available. Text searches here are literal source evidence, not semantic proof. No code/caller changes are in scope.
- No lane content was edited; no build, test, runtime, integration, or judgment was invoked.

## Cleanup and tooling

No scratch directory or clone was created; no scratch remains. No tools installed or updated. Only this seat's requested report, JSON and receipt files were written.

Self-evaluation: accuracy 4 (one-source scope leaves other rows unverified), completeness 5 (requested sample, quote, byte/date/hash comparison and receipts supplied), clarity 4 (raw/API distinction requires explanation), actionability 5 (exact evidence paths and commands), conciseness 4 (commands retained for audit). Overall 4.4. Improvement: broader source sampling would reduce residual risk but is outside this seat's one-source milestone. User agreement is INFERENCE.
