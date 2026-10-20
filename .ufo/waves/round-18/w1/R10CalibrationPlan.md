# R10 — Calibration no-harm review

## Findings

### High — Carry coverage is page-keyed, so a page edit invalidates unchanged carried buckets

The round-18 measure correctly indexes entries by section `sha256` and looks up each current section by that digest (`.ufo/evidence/round-18/measure.py:601-611`). Therefore a carried entry whose section text changed is not matched; the ordinary byte-change fixture also expects `no-ledger-entry` (`measure.py:1033-1041`). Likewise every candidate entry still passes the input gate: the carried-input fixture expects `input-drift:<path>` and no credit (`measure.py:1229-1240`). I found no credit bypass keyed on `carried_from`.

The assembler’s completeness gate does not use that same identity. `load_carry()` copies each entry and adds only `carried_from` (`.ufo/evidence/round-18/coldread/assemble.py:928-982`); `coverage()` recognizes entries only by `(skill_sha256, start)` (`assemble.py:987-995`), and `_finish()` checks that against the expected page SHA (`assemble.py:1971-1987`). Consequently, after any `SKILL.md` edit changes the full-page SHA, old carried entries cannot cover even unchanged sections. With new reports for only the changed section(s), the assembler will still report the unchanged sections uncovered and exit 1. **[INFERENCE from those code paths; not executed.]** This defeats the section-level no-harm plan: the measure can credit unchanged section/input evidence, but the assembler blocks producing a complete current-page ledger from it.

The carry selftest only carries a ledger back onto its same page SHA (`assemble.py:1292-1312`), so it cannot catch this. Add a synthetic integration case: carry a prior full-page ledger, edit one section (thereby changing the page SHA), add a report for that changed section, and assemble with the new expected page SHA. Require success while retaining old entries; then measure the result and require unchanged sections with stable inputs credited, the edited section uncredited until re-read, and drifted inputs uncredited. Coverage should be keyed consistently with the section-level credit rule, not merely the old page identity.

### Medium — The requested base restraint score of 8 is incompatible with the round-18 link rule

The round-18 measure sets `BOX3_LINK` to `.ufo/evidence/round-18/coldread/ledger.json` (`measure.py:113-136`) and awards box 3 only when that path appears in its box-3 block (`measure.py:678-682`). At the pinned base, `SHONEN.md:10` still links the round-16 ledger; it does not contain the round-18 path. The round-18 selftest explicitly checks that an old-round link yields restraint 6 (`measure.py:992-998`). Thus the task’s requested base-revision carry measurement can establish a section count, but its restraint score is 6, not 8. **[INFERENCE from the pinned base bytes and score rule; not executed.]** The staged round-18 SHONEN pointer must be tested at a revision that actually contains it; do not require score 8 at `183f87b...`.

Also, the planned command passes `--ledger-file`; that sets `overrides_used: true` and selects the legacy trace gate (`measure.py:66-71, 1572-1573`). The source explicitly says an override run is a measurement aid and “A claim must never use overrides” (`measure.py:67-71`). Keep the base run as a comparison/test only, not the strict calibration claim.

### Medium — Carry-specific veto behavior is not exercised end-to-end

The current implementation appears fail-closed for an intact carried veto: `load_carry()` preserves the source entry fields and adds only provenance (`assemble.py:979-981`); measurement still detects a failing entry and vetoes when its inputs verify (`measure.py:634-637`). Existing synthetic measure cases cover ordinary duplicate failures, clean-twin veto, and stale-failure non-veto (`measure.py:1300-1324`). So I found no current path by which merely adding `carried_from` launders a fresh veto.

But the assembler carry selftest covers only clean entries (`assemble.py:1292-1312`), and the measure’s “carried round-17” drift case is a synthetic clean entry with a manually added `carried_from` marker, not output from `load_carry()` (`measure.py:1229-1240`). Add composed carry/measure cases to lock down: (1) a carried `wrong-expectation`/`gap-blocking` entry with verified inputs plus a clean twin remains vetoed and uncovered; (2) a carried failing entry with drifted inputs does not itself credit or veto, while a separate fresh clean read may credit; and (3) a carried failure with absent/empty effective inputs remains fail-closed and vetoes. Preserve the failure fields in the carried JSON and assert `vetoed`/reason, not just assembler exit status.

## Direct answers / required selftest failure modes

- **Changed section:** with verbatim `sha256`, no credit: the current measure matches on section digest (`measure.py:601-611`). The existing basic byte-change case is useful, but the carry integration/page-change case above is missing.
- **Drifted input:** no credit: current-input verification remains active for carried entries (`measure.py:1229-1240`). Also cover missing/renamed/non-blob input and the case where ignoring both ledger paths leaves no non-ignored input; the latter is already tested as `inputs-unrecorded` (`measure.py:1212-1228`).
- **Veto laundering:** no, not for an intact carried failure with current inputs; copy preserves the failure and measurement vetoes it (`assemble.py:979-981`; `measure.py:634-637`). Test carried+clean twins and stale-veto behavior through the composed path, because current tests exercise those rules separately.
- **Page-key mismatch:** carry old entries across a changed page and prove unchanged sections stay reusable while only the changed section requires a new read; current assembler coverage will fail this case (`assemble.py:987-995`).

## Evidence and verification gaps

- Extracted the pinned round-17 `measure.py`, assembler, ledger, SKILL, lesson, and base `SHONEN.md` with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 183f87b899e6cae46be98d251cbc87fb5118f6ca:<path>` into `/tmp/tameshi-r18w1-R10CalibrationPlan-A6ZwF6/`; each requested blob returned `OK` (exit 0). Pinned measure SHA-256: `d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3`.
- Base `SHONEN.md` extraction and `sha256sum` completed successfully (exit 0); its box-3 text is at lines 9-11, with the old round-16 pointer at line 10.
- LSP unavailable: attempted `read xd://lsp`; tool returned `No such tool: xd://lsp` and the mounted-tool list contains no LSP device. Therefore no references/definition/diagnostics were available; findings are based on direct source reads, not grep as semantic proof.
- No selftests/builds were run for this review. The round-18 scripts were untracked working-tree files during inspection; main should run the planned checks after integration.

## Residual risk

`--carry PATH` accepts caller-selected JSON; this review assumes the specified prior ledger is intact. The current tests establish copied-entry equality but do not authenticate that the supplied carry file is the canonical latest ledger. No runtime/routing/saturation behavior was in this scoped change.

**Verdict: partial — section-hash and input gates resist stale credit and intact veto laundering, but carry coverage is page-keyed and the base restraint-8 acceptance is impossible as specified.**