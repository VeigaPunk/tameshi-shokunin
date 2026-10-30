# C3 per-entry gate — reject as written (recommendation)

Axes: province scope; source fidelity/QUALITY; incremental coverage; boundary honesty.

Reviewed `/fast/scratch/hyaku/tameshi-r58/c0-drafts/entry-llm-mutant-equivalence-cost.md`, SHA256 `1083344a32f3bc357445fe95059b68b8e716b9161037e427d01f3a37d1ec1671`. No lane content edited. This is a review recommendation, not admission.

## Findings, by severity

**Medium — unsupported conditional-rate claim (draft 32–33).** “S286 shows … a materially larger share of un-killed mutants are equivalent” changes the denominator. The retained abstract reports equivalent-mutant rates worse by 3.51 percentage points, but does not give the conditional share among survivors. Higher overall equivalence alone does not determine equivalent/surviving when the survivor population also changes. QUALITY 1–3 require falsifiable sourced observations distinct from inference. Replace this with the actual reported equivalent-mutant-rate comparison and retain survivor classification as a lane inference. The exact source excerpt and draft are in receipt `summary.source_abstract` / `summary.draft`.

**Low — two-gate sample presented as whole lane (draft 48–49).** “the lane's legs are one JavaScript gate and one bash gate” conflicts with the base coverage map's round-51 tenth recorded leg. Name the original B5/D2/D10 sample instead. Executed command:

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/README.md`

Output lines 630/634: `## Round 51 — tenth recorded mutation case (depth)` and `tenth ledger leg bash-drift-pins`. Full output retained in the receipt's commands array.

## Per-entry gates

- **PROVINCE: pass.** PROVINCE lines 3–5 explicitly own mutation-testing method. Survivor counting and invalid-mutant accounting are reusable fixture craft; no product ownership or sibling edit is claimed.
- **QUALITY: reject as written.** The provenance trio is present, both source quotes match the retained extracts, and observations/inferences generally separate. The medium finding is nevertheless an ungrounded empirical assertion. QUALITY 7/10/79 also require the installed coverage row, mined source rows and committed quote snapshots; this draft alone does not establish final installation.
- **Expansion: genuinely new, narrowly scoped.** At the pinned base, 66 knowledge files contain zero matches for `2406\.09843|\bLLMs?\b|\bF9\b|large[ -]language` (case insensitive). SOURCES S007/S009/S043/S044 are queued, not held entries. README line 624 leaves F9 open and the pilot untouched. S001 already supplies invalid-mutant denominator rules; S007 already queues LLM mutation/equivalence-agent results; S009 queues compiler equivalence; S030 rejects visual snapshot triage as adjacent. Thus neither generic equivalence nor error exclusions earn fresh credit. The new ground is the specific empirical LLM generation tradeoff (fault detection versus non-compilability, duplication, equivalence), not a new general survivor rule. The held round-43 `r43-survivor-resolution-rule.md` already covers the generic equivalence hazard.
- **CANNOT-ANSWER/boundary: substantially honest.** Draft 48–58 explicitly leave cross-language transfer and the independently checked F9 pilot unmeasured. An input exhibiting a difference is a non-equivalence witness, not an equivalence proof; 52–56 correctly deny a general decision procedure. For clarity, replace “equivalence witness” at 34 with “non-equivalence witness or unresolved classification”; lack of a difference must never be presented as universal equivalence.

## Executed sweep and retained evidence

Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevC3Gate-receipts/sweep.json`.

Executed through Python subprocess, every git command used the absolute lane path:

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 2a32aa8228d5f86a85c81a923a3148bf792a9538 -- corpus/knowledge` → 66 paths, exit 0.
2. For every returned path, `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:PATH`; case-insensitive Python regex search over these exact blob bytes → `{"files":66,"patterns":"2406\\.09843|\\bLLMs?\\b|\\bF9\\b|large[ -]language","hits":{}}`. An initial unbounded F9 pattern hit hex digests; the precise token-boundary sweep removed those false hits. Every command's exit/stdout/stderr is retained, not only its summary.
3. Same `git show` for `corpus/SOURCES.md`, `corpus/README.md`, and `corpus/knowledge/r43-survivor-resolution-rule.md` → exit 0 each. Source rows S001–S030 inspected directly; F9 rows 86/624 and round-43 boundary inspected.
4. Read tool inspected draft 1–58, PROVINCE 1–118, QUALITY 1–240 and 930–960, the round-58 contract, the retained abstract, and deck extract 220–245. Deck 231–232 defines all-input equivalence; 239 names score imprecision; 241 states undecidability. The abstract's exact numerical comparisons are retained in the receipt.

## Residual risk and verification gaps

- F9 gains sourced ground, not completion of its pilot. No saturation or universal equivalence claim is supported.
- Final installed source rows, coverage-map row, census, and no-harm at deciding REV were not run in this per-entry review. No live re-fetch performed; comparison used the L1 extracts. They need committed snapshots before final citation (QUALITY79).
- `read xd://lsp` returned `No such tool`; semantic references/definition/diagnostics unavailable. The fallback here is literal pinned-blob inspection, not semantic proof. No runtime, rerouting or resume code is changed by this entry, so those reviewer checks do not apply.
- No tools installed. No seat scratch directory/clone created; no scratch remains. Shared draft was not modified or deleted.

Self-evaluation: accuracy 4 (source checks limited to retained extracts); completeness 4 (final installation deliberately outside per-entry scope); clarity 4 (receipt retains full command outputs); actionability 4 (two precise draft corrections); conciseness 4 (full sweep retained separately). Overall 4.0. Highest-impact improvement is correcting the conditional-rate claim before admission; independent live re-opening belongs to the assigned wave-2 source review. User agreement is an inference, not measured.
