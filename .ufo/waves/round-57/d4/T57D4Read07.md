# T57D4Read07 — bounded documentary agreement

## Scope and axes

Evidence fidelity; C0b identity; claim-to-receipt coverage; zero new execution/mutation. Audited `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read07.json`, its `.md`, and all eight retained receipt-directory files. Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`. This is a documentary recommendation, not admission. Current integration remains UNVERIFIED.

## Findings by severity

No concrete contradiction found between the assigned report, retained command results, and the checked committed blobs. In particular, no missing primary receipt or mismatched candidate/section digest was found. The evidence gaps below prevent treating historical execution statements as newly verified runtime guarantees.

## Documentary sweep — commands and observed output

Only inert JSON/source analysis and read-only `git show` were used; none of the retained Python drivers, candidate gates, selftests, or regression commands was executed.

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`, displaying the assigned lines 1421–1436 and precedence bullet 1334–1336. In-memory SHA256 calculation stripped trailing blank lines and joined with LF, following the read-only source definition at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py:209-251` (not imported/executed).

   Output: heading `### The map — where a reader enters, artifact by artifact`; next heading starts at 1437; normalized SHA256 `30d62e79a81d8e6dfcfc9076f0977b1e14016d527f5fd78e66aab407bd370bea`. The retained section text exactly matches the committed section under its driver's print formatting: `IDENTITY_EXACT_PYTHON_PRINT_MATCH True receipt_len 3778 committed_print_len 3778`. A preliminary comparison added one excess newline; the exact source-defined formatting resolved that comparison, with no content discrepancy. The precedence bullet is indeed in SKILL's runbook section, not required verbatim in the source runbook.

2. Inert Python JSON comparison: for every entry in `T57W3Read07.json.commands`, read its named receipt and compare `command`, `cwd`, `exit_code`, and `output` without executing the command string.

   Output: all four fields equal for each of `section-identity.json`, `pointer-audit.json`, `selftest.json`, and `regression.json`; all four retained exit codes are 0. Retained summary lines are exactly:

   ```text
   SWEEP PASS: all mapped pointers resolve and enumerated claims hold
   MUTATE_SELFTEST: 107/107 pass
   VERDICT: PASS
   REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
   ```

   These are historical retained outputs, not checks passed in this audit. Regression retains ten git target revision/digest pins and ten case PASS summaries, consistent with the report's explicitly historical replay scope.

3. For each `POINTER OK` path in the retained pointer output, execute `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:<path>` and hash the returned bytes. Compare each retained `ANCHOR` to the corresponding committed line. This is blob comparison, not running `pointer-audit.py`.

   Output: `C0B_POINTER_HASH ... True` for all 14 named paths; `ANCHOR_COMPARE ... exact=True` for all 12 anchors: README 125/326/614, operator-runbook 349/350/351, runner 149/150, ledger 439/441, LOG 316/317. Section SHA and all recorded pointer digests therefore bind to the stated C0b content. The ledger's 869-character line 441 is fully retained; UI display clipping is not missing receipt content.

4. Read both historical failed pointer receipts and the retained driver source. Output: first receipt exit 1 at the exact-bullet assertion against `runbook`; second receipt exit 1 with `LEDGER MEASURED ROWS 20`; corrected receipt exit 0 with `LEDGER MEASURED ROWS 8`. The retained corrected driver locates the bullet in SKILL and excludes non-measurement tick rows, matching the report's disclosed harness corrections. Neither failed output is concealed or represented as a successful run.

## Residual risk and verification gaps

- The historical claims of scratch-only execution, sibling symlink layout, absence of lane/sibling mutation, and scratch removal (`T57W3Read07.md:29-32`) are not independently demonstrated by before/after state captures or environment/filesystem-operation traces. Inventory output shows six receipt JSON files containing only `command`, `cwd`, `exit_code`, `output`, plus two driver sources. Cwd strings and git target pins support the stated context but do not establish those broader nonmutation/cleanup claims. Treat these statements as reported provenance, not independently verified guarantees.
- Selftest/regression results are retained stdout and exit-code records. No fresh runtime verification was authorized or performed; this audit does not authenticate the original process capture or recreate discarded per-leg work directories. Earlier driver versions corresponding to the two failed runs are not retained as separate source snapshots; the failures themselves are retained.
- Pointer existence/digest and explicit anchor checks are supported. The pointer driver's broad `SWEEP PASS` wording is not, by itself, semantic proof of every descriptive clause in every mapped artifact. The report's manual reading assertion is not independently replayed here.
- No 64/64 monitor run, C1/C2 admission, canonical-runtime/rerouting/saturation guarantee, or `resume_continuity_v1` behavior is established by this assigned artifact-map evidence. None is newly granted by this review.
- `read xd://lsp` returned `No such tool`; no semantic LSP evidence is claimed. No tools installed, delegation, tests, builds, gate execution, commits, production edits, or scratch writes occurred. Only this seat's two authorized d4 report files were written.

## Recommendation

Retain bounded agreement on candidate/section identity and report-to-receipt consistency. Preserve the provenance limitations above when binding the report; do not promote its historical `verified-record` label into current integration admission.

Self-evaluation: accuracy 4/5 (retained capture provenance cannot be authenticated); completeness 4/5 (documentary-only scope excludes runtime reproduction); clarity 5/5 (agreement separated from gaps); actionability 4/5 (additional provenance evidence is absent); conciseness 4/5 (explicit sweep retained for auditability). Overall 4.2/5. Highest-impact improvement would be independent original execution/state provenance, not an unauthorized rerun.
