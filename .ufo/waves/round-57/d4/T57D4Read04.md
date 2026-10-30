# T57D4Read04 — documentary audit

## Findings by severity

None within the assigned documentary scope. **Bounded agreement**, not runtime admission: T57W3Read04's section metadata, retained command outputs and cited historical documents agree with committed C0b `adf87899c70d616140a81185a8f9acbbdfb30392`.

Axes: revision/section identity, receipt consistency, historical-claim support, read-only scope.

## Evidence and performed sweep

Inputs (absolute directory `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/`):

- `T57W3Read04.json`, SHA256 `8386fc4974d12972bf84ed98e709665579576071222af0dfb679f5e991f6c4d0`.
- `T57W3Read04.md`, SHA256 `299c26a249d5aac245f228e9130ffd4601adfd9e96dc95eab89e4a3c16a73026`.
- `T57W3Read04-receipts/commands.json`, SHA256 `682888e9461be23716aa0bfd41d34a8e94063697c51ff756cfcef3f50d23906b` and all six `command-NN.txt` files.

Performed read-only Git subprocess commands through Python analysis (no repository module imported or executed):

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5e3569969b532310d2b8a3d130901757a3df356b:SKILL.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- SKILL.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log adf87899c70d616140a81185a8f9acbbdfb30392 '--format=%H %aI %s' --reverse -- tools/mutate-and-run.sh
```

Observed analysis output:

```text
commands.json equals report commands: True
receipt 1 exit 0 output bytes 41 matches JSON True
receipt 2 exit 0 output bytes 4229 matches JSON True
receipt 3 exit 0 output bytes 771 matches JSON True
receipt 4 exit 0 output bytes 3318 matches JSON True
receipt 5 exit 0 output bytes 75 matches JSON True
receipt 6 exit 0 output bytes 13353 matches JSON True
C0b git show section 1100 1122 2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801 metadata matches True
section base unchanged True
retained diff matches C0b/base True
retained command-04 equals C0b-bounded history: True
```

The exits above are the **retained record's declared exits**, not independently re-executed commands 1–6. Section normalization was independently implemented from the read-only source description in `.ufo/evidence/round-18/measure.py:209–251`: heading block, trailing whitespace-only lines removed, LF-joined, no trailing newline. No frozen counter was imported.

Additional executed documentary commands were `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <revision>:<path>`, followed by in-memory SHA256 or line comparisons:

- At C0b, all five whole-file SHA256 values in command 3 matched: `corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/service-optin-protocol.md`, `corpus/knowledge/mutation-case-mado-verify.md`, `plans/round-8.plan.md`, `.ufo/waves/round-16/w2/RerunSweep.md`. Output for each: `matches True`.
- At the seven commits listed in retained command 6, `tools/mutate-and-run.sh` hashes matched every retained value. Output for each: `matches True`. Commit/hash-prefix pairs: `53e74a890c70…/d8abee52`, `b58b26fbeba8…/597e1419`, `44947154c237…/b56c6e57`, `9f1d3c339a70…/cf41efaa`, `606716f703f7…/75ed934d`, `c699c8c36d6e…/89722ddb`, `05a224754db3…/0673d2e5`.
- All eight retained pointer excerpts matched C0b line-for-line: ledger 297–312 and 318–341; service protocol 225–232; mado note 17–23; round-8 plan 69–76; RerunSweep 19–24; kumitate-claims note 315–323; round-6 draft 243–262. Output for each: `C0b excerpt <path> <lo> <hi> True`.
- Additional C0b Git-show reads checked ledger 170–173, 279–284 and RerunSweep 87–96. Observed ledger 281 explicitly records `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)` and `2026-10-14T19:14:16Z`; ledger 172–173 says `as an appended row, not an edit of §1–§4`; RerunSweep 93 records `75ed934d → 89722ddb`.

This supports the historical claims in report lines 13–17: four committed runner moves, separately documented working-tree transients, the later runner distinction, SCR-T6's 4/10 and preservation of the original mado note's U. The section has policy prose and historical result tokens, not a runnable command block.

## Residual risk and verification gaps

- Matching unsigned retained outputs to documents does not authenticate prior execution, scratch identity, exit status or absence of transient mutations. The original report already limits its claim to documentary consistency (lines 88–90).
- Historical scratch logs and uncommitted runner blobs were not reconstructed. C0b prose supports their reported history; no fresh historical replay is asserted.
- LSP unavailable: `read xd://lsp` returned `No such tool`. Source-text observations are not semantic caller/definition/diagnostic proof. This item changes no code and introduces no caller contract.
- No candidate gate, counter, test/build, security probe, credential operation, fixture or other runtime was executed. No runtime, saturation, same-identity routing or resume-continuity approval follows. Current integration remains **UNVERIFIED**.
- Only this seat's absolute d4 Markdown and JSON reports were written. No production/frozen files, commits, PATH directories or tools changed; no installs.

## Self-evaluation

Accuracy 4/5: unsigned historical execution cannot be authenticated. Completeness 5/5: both assigned reports, all six retained outputs, section metadata and every retained pointer excerpt compared. Clarity 4/5: historical hashes require the cited source context. Actionability 5/5: agreement and non-admission boundaries explicit. Conciseness 4/5: evidence inventory is necessarily longer than the finding. Overall 4.4/5. Highest-impact improvement would be authenticated original execution streams, unavailable to this documentary scope.
