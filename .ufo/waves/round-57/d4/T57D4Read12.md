# T57D4Read12 — documentary audit

## Findings by severity

No concrete contradiction found in the assigned report/receipt comparison. **Bounded documentary agreement only; current candidate integration remains UNVERIFIED. No admission recommendation.**

Axes: command/result fidelity; candidate/section identity; historical-evidence preservation; scope honesty.

## Scope and evidence

Reviewed the absolute paths `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12.json`, its `.md` companion, and all eight JSON files in its `T57W3Read12-receipts/` directory. SKILL content was read only through `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`. No candidate gate, recorded command, selftest, build, archived capture script, external request, or other runtime was executed.

1. **Identity agrees.** C0b lines 1606–1639 contain `## Effective expectation reconciliation — round 14`; line 1640 begins the next heading. Applying the documented trailing-blank-line/no-terminal-newline normalization gives SHA256 `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe`, exactly matching report metadata and `frozen-sectionize.json`.
2. **All eight retained command records agree exactly.** Static JSON object equality, including name, command, cwd, exit, stdout and stderr, was true for frozen-sectionize, live-before, live-after, archive-before, archive-after, retained-context, current-repin and record-pointer-audit. Exit sequence: `0,2,2,1,0,0,0,0`. Every command name appears in the Markdown sweep. Nonzero outcomes are explicitly disclosed rather than relabeled as successful evaluation.
3. **Results preserve distinctions.** Live-before/after both record `could_not_evaluate` / `expected_input_digest_mismatch`. Archive-before records one `expected_contains_missing` for `producer_before`; archive-after and current-repin retain its raw failed expectation with explicit supersession and both named replacements, rather than silently dropping it. Recorded counts agree with Markdown: 12 expected, 11 effective passing, one superseded after reconciliation.
4. **Committed bytes corroborate retained metadata.** C0b `tools/evidence-disposition.py` SHA256 is `f09d1e490b94edb75364825c3941eb88cfb88a76ae26a2b9257e923ac123ea93`; archive `28aeef498cc070c3183271b709bc79d344ff547a` tool SHA256 is `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`. These match corresponding receipt payloads. Committed context receipt SHA256 is `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`, matching retained-context stdout.
5. **Historical claims agree with committed records.** Static C0b blob reads show 12 expected checks, 13 pinned inputs, and precisely three stale paths: tools/pin-disposition.py, tools/bash-witness-study.py, tools/mutate-and-run.sh. `verification-final.json` records measured commit `64314783836bb0d05ad06a774d7310fd3a23b5bd` and `SELFTEST: PASS (34/34)`; initial `verification.json` records measured commit `0c6e36d0bd2fd98077de4cff4c90c6f467c2e1fb` and 18/34 failed. All seven historical check stdout strings occur unchanged in the pointer-audit receipt. These are historical records, not fresh selftest results.

## Documentary sweep: commands and observed output

The companion JSON embeds the static inspection operations and their observed summaries. Operations used Python standard-library JSON/hash comparisons plus read-only `git -C <absolute lane> show <rev>:<path>` and `rev-parse`; no repository Python was imported or executed.

- Section read/hash: `1606 1639 6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe`; next heading at 1640.
- Eight full-object comparisons: all `True`; command/cwd/exit/stdout/stderr mismatches: none.
- C0b expected checks/inputs: `12 13`; stale inputs: exactly the three paths listed above.
- Historical stdout inclusion comparisons: all seven `True`.

## Residual risk and verification gaps

- Receipts are retained assertions, not independent proof of subprocess execution or an attested clean detached checkout. Their cwd paths and self-reported tool hashes cannot establish complete input-tree identity. No retained checkout/clean-tree receipt is present among the eight supplied files. This bounds agreement, rather than contradicting a recorded result.
- No fresh execution was authorized. Runtime correctness, the integrated deciding revision, round-21 64/64 NO-HARM, C1/C2 and general saturation are **not established** by this review. The assigned report itself disclaims broad promotion, hermeticity and saturation claims.
- External source pages were not fetched; upstream validity and independent promotion are not assessed.
- `read xd://lsp` returned `No such tool`; no LSP server/status/references/definition/diagnostics were available. Static inspection is not semantic caller proof. This assignment reviews documentary metadata, not a production code change.
- No files changed outside this seat's two d4 reports; no installs, delegation, commits, fixture creation or production edits.

Self-evaluation: accuracy 4/5 (retained executions cannot be independently attested); completeness 4/5 (bounded to supplied documentary evidence); clarity 4/5 (companion JSON carries detailed operations); actionability 4/5 (missing checkout attestation explicitly identified); conciseness 4/5 (hash detail retained for reproducibility). Overall 4.0. Improvement: retain original clean-checkout provenance if broader execution attribution is required; do not infer admission from this audit. User agreement expected only within the stated documentary boundary.
