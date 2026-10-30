# Fixed-at-base sample B

Axes: calibration (primary), evidence completeness, scope/no-harm. Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Recommendations only; no admission, integration, production edits, or new runtime invocation.

## Findings, severity ordered

**Medium — R56.3 remains open under the item's explicit discoverability condition.** `corpus/knowledge/receipt-revision-binding.md:3` still requires `GATE_SELFTEST: 14/14 pass` and points nowhere to the governing errata. Lines 251–259 add ER-R57-K1 with the 19/19 command and declare it governing; `corpus/README.md:653` indexes that correction. This is substantial partial remediation, introduced by `ca75c2674645ab6bdadeecb8584007c74342bfa9`, but the item specifically allows a replacement superseding entry or errata the `recheck:` line itself points to. An unlinked errata in the same old entry does not meet that literal condition. The original line therefore remains a wrong executable instruction. Recommendation: authorized owner supplies a superseding replacement entry or a pointer from the recheck line. No file change proposed/staged by this reviewer.

Interpretation risk: if the canonical adjudicator treats the in-file errata itself as the allowed “new superseding entry,” the substantive correction supports fixed. This review does not silently broaden the explicit pointer condition.

## Resolved items

- **R56.4 — fixed**, commit `ca75c2674645ab6bdadeecb8584007c74342bfa9`. `.ufo/evidence/round-57/coldread-referent-r56.md:6–11` records the misleading `external_inputs` labels and identifies their actual referent as `877eedee3ddb7fe25d7a6a09922b04ba13e5a99b`. The item expressly permits recording the referent instead of rebinding. Independent blob SHA256 comparison of ledger entries 591–608 confirms all 13 SOURCES labels equal `6c2096d8091f5d5be87a638f1a90ab6322a203c2be516d59dcfb970d4f55a6d3`, and all six QUALITY labels equal `54c49d3873b03acfa5ac4db7e0b7e6621808d80eee3b5ae60b90ad0fa2e2aab7`, both from that referent. All 19 differ from their labelled C0 blobs. No claim that labels were rebound or that the monitor validates them.
- **R56.6 — fixed**, same commit. `tools/registry.json:1309–1390` adds three `kind: gate` rows with actual argv and expected exits: accept `0`/PASS; content drift `3`/REFUSED; unresolvable certified revision `2`/REFUSED. Keyed excerpt at 1381: `GATE: error=unresolvable-certified receipts=1 verdict=REFUSED codes=RECEIPT_REV_UNRESOLVABLE`. Canonical definition `tools/receipt-revision-gate.py:190–194` returns 2 for failed certified-revision resolution; `:201–220` accumulates receipt refusals and returns 0 for PASS, otherwise 3; `:144–152` defines content drift. These are declaration/implementation comparisons, not a claimed live execution. Round-58's separate bare-token equality debt does not negate the original gate-row/exit-map repair.
- **R56.7 — fixed**, final correction commit `adf87899c70d616140a81185a8f9acbbdfb30392` (initial correction in `ca75c26`). `corpus/lessons/round-57.md:27–36`: `"no byte changed after C0/PIN" holds from 877eedee to base only`; the paragraph names exact endpoints, records QUALITY +31, SOURCES +2, knowledge +39 before the bind input, and explicitly supersedes the earlier sentence. Independent diffs reproduce both interval claims.

## Commands and observed outputs

All git calls used `-C /fast/scratch/hyaku/tameshi-r58/T58W1RevFixOld2/clone`. Complete commands, stdout, exit codes, base excerpts and introducing diffs are retained in the absolute receipt path:

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1RevFixOld2-receipts/review.json`

Executed sweep:

1. Shared clone into the named scratch path; assert `rev-parse --show-toplevel` equals that clone before `checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538`. Subsequent `rev-parse HEAD` printed the complete base hash (exit 0).
2. `log --format='%H %s' 5e3569969b532310d2b8a3d130901757a3df356b..2a32aa8228d5f86a85c81a923a3148bf792a9538 -- corpus tools/registry.json QUALITY.md` located ca75c26 and adf8789; `show --format= --unified=3 <commit> -- <affected paths>` displayed the actual additions/corrections, retained in receipts.
3. `merge-base --is-ancestor <commit> <base>` for each resolving commit: exit 0, empty stdout/stderr for both.
4. `show <base>:<path>` with receipt-selected line windows gives the original recheck and superseding/index/registry/referent/interval excerpts cited above. Tool read/grep independently located these same base files. These are literal content observations, not semantic-reference claims.
5. Python SHA256 of `git show <rev>:<path>`, compared against parsed `git show <base>:.ufo/evidence/round-21/coldread/ledger.json` entries `[591:609]`: SOURCES `labels=13 mismatch_C0=13 matches_referent=13`; QUALITY `labels=6 mismatch_C0=6 matches_referent=6`. C0 hashes respectively `11c5682902d5564e5f0982d3be904f35c39c5520e288fcae14cfc7288baa8be2` and `80792b7d466dfd2126ea5fd00ff08e7be292a69bea0f7ec45e329bf0860fb60c`.
6. `diff --stat 877eedee3ddb7fe25d7a6a09922b04ba13e5a99b 5e3569969b532310d2b8a3d130901757a3df356b -- SKILL.md corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge tools`: exit 0, empty stdout.
7. `diff --stat c0137451f5b7 877eedee3ddb -- corpus SKILL.md tools`: exit 0; QUALITY 31 additions, SOURCES 2, knowledge/receipt-revision-binding 39, lesson 144; four files, 216 insertions.

## Residual risk and verification gaps

`read(xd://lsp)` returned `No such tool`; no LSP server/device was available for references, definitions or diagnostics. Literal read/grep fallback is explicitly not semantic proof. Gate definitions and registry callers were examined directly. No other runtime, gate/selftest, monitor, counter, or saturation measurement was invoked; none is asserted passed. No resume path is changed or assessed by this scoped historical sample. No claim about global calibration saturation or all-round C1/C2 admission follows from this sample.

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W1RevFixOld2` was removed; `test ! -e` returned exit 0. No tools installed/upgraded. No production/prior-evidence files modified; only this seat's report, JSON and receipt were written.

Self-evaluation: accuracy 4/5 (R56.3 language interpretation explicitly exposed); completeness 4/5 (all four reviewed; runtime execution intentionally not performed); clarity 4/5 (full commands in receipt rather than repeated inline); actionability 4/5 (one precise unresolved pointer condition, owner must adjudicate interpretation); conciseness 4/5 (command evidence adds length). Overall 4.0/5. Highest-value improvement is an explicit canonical interpretation of “new superseding entry,” not an unsupported runtime claim. User agreement: expected on evidence, interpretation reserved.
