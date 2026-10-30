# T57D4Read13 — documentary audit

## Findings by severity

No actionable contradiction found within the assigned report/receipt comparison. **Bounded documentary agreement only; candidate integration remains UNVERIFIED.** This is not admission or fresh runtime verification.

Axes: claim/receipt consistency, committed-content binding, evidence completeness, zero production mutation.

## Evidence and observed outputs

Reviewed `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read13.md` (especially lines 5–28), its adjacent JSON, and all nine numbered JSON receipts in the adjacent `T57W3Read13-receipts` directory.

Commands used for committed source reads:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:.ufo/evidence/round-18/measure.py
```

Both returned source (exit 0), not an executed gate. The corresponding SKILL section is lines 1652–1718; line 1719 begins `### Round-15 gate/probe registry`. The frozen sectionizer source specifies trimming trailing whitespace-only lines and joining with newline without a final newline. Independent data-only SHA-256 calculation using that rule returned:

```text
NORMALIZED_SECTION 132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6 MATCH True
```

Data-only Eval sweep: parse assigned JSON; for each command load its absolute `receipt` and compare the entire parsed object; for each `inputs` item read `git -C <absolute lane> show <C0b>:<path>` and compare SHA-256. Output: commands 1–9 each `equal_full=True`; all 19 input hashes `MATCH`, including whole SKILL, both active gates, frozen sectionizer, three historical verification files and clean/missing-environment expected pins. No candidate module was imported or run.

Retained results agree with the report table: exits `[0,0,0,64,64,0,1,0,0]`; receipts 02/03 end `SELFTEST: PASS (49/49)` / `SELFTEST: PASS (66/66)`. Receipt 07 records `missing_injected_environment`, exit 1, `verdict_matches_expected=true`, and an additional `receipt_verdict_mismatch` finding; the report explicitly preserves that negative outcome. Receipt 08 records clean/exit 0. These are recorded results, not newly reproduced results.

Committed historical JSON parsing returned:

```text
verification.json: checks=44 failed_checks=['selftest-new','selftest-new-full-count']
verification-2.json: checks=18 failed_checks=['runner-internal-error']
verification-3.json: checks=44 failed_checks=[]
```

This supports the report's distinction between effective evidence and retained failed history. The committed section explicitly archives the historical producer, forbids regenerating receipts and disclaims authentication, live capture and environment independence; the report preserves those limitations.

## Residual risk and verification gaps

- All nine receipts are unsigned local documentary records. Their exact duplication in the assigned JSON is consistency evidence, not independent execution authentication. They contain cwd/environment but no independently retained clone-HEAD attestation; report candidate metadata and matching committed hashes do not by themselves prove the historical process checkout.
- The fleet `../PROTOCOL.md` pointer is explicitly external; no fleet content digest is bound in this report's `inputs`. No committed fleet-byte or revision-independence claim is established by this audit.
- `read xd://lsp` returned `No such tool`; semantic definitions/references/diagnostics were unavailable. Only literal documentary/source evidence is claimed.
- No candidate gate, selftest, build, monitor or counter executed. No 64/64 NO-HARM result, canonical runtime/reroute behavior, resume-continuity preflight or saturation result is established here; those are outside this assigned section/receipt audit.
- No production edits, staging, delegation, installs, commits or push.

## Self-evaluation

Accuracy 4/5 (unsigned history cannot authenticate execution); completeness 4/5 (external fleet pointer is unpinned); clarity 4/5 (long stdout remains in original receipts); actionability 4/5 (integration decision requires separate evidence); conciseness 4/5 (MD/JSON intentionally overlap). Overall 4.0/5. Highest-impact improvement: retain independently bound checkout identity with execution receipts when authorized; do not infer it here. User agreement expected because the result is explicitly documentary and bounded.
