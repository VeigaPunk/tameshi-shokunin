# T57D4Read05 — documentary audit

Axes: candidate/section identity; retained-output fidelity; command provenance; claim bounds.

Scope: T57W3Read05.md/.json and retained audit.py/audit.out, compared with committed C0b `adf87899c70d616140a81185a8f9acbbdfb30392`. Documentary analysis only; no candidate gate, retained program, tests, builds, clone, or mutation executed. No admission is recommended: candidate integration remains UNVERIFIED.

## Findings by severity

**Low — execution-provenance gap, not a contradictory result.** `T57W3Read05.json:25-34` records an abbreviated sectionizer snippet and a clone/assert/checkout sequence with exit 0. The retained receipt directory contains only `audit.py` and `audit.out`; neither contains the original clone/assert/checkout transcript or independent snippet transcript. `audit.out:1-3` reports the resulting section and clone identity, and `:140` records `exit=0`, but cannot independently establish that entire preceding command sequence or its exit status. Likewise `audit.py:49-54` compares row IDs, not row semantics; its terminal summary is not an automated proof of the report's human semantic comparison. Preserve these as author-reported execution and documentary inspection, not authenticated execution. No new run is requested under this recovery directive.

Evidence command: read `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read05-receipts`.
Output: `audit.out 11.0KB`, `audit.py 2.7KB`; source lines 14-19 print section/clone state, lines 49-53 compare a-j IDs, line 54 prints the sweep summary. The original snippet and clone sequence have no separately retained transcript in that directory.

## Bounded agreement

- `cand`, heading, inclusive section bounds 1282–1311, and normalized SHA-256 `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6` agree with C0b.
- Retained section text agrees after removing output-separator trailing newlines. All **17/17** retained anchor blocks match their named C0b file/line bytes.
- The reported citation defect is supported: C0b SKILL.md:1299,1300,1303 directs b/c/f to unrelated or insufficient ranges. Proposed locations b 841–845 and 868–872, c 851–853 with re-pin context 840, f 907–909 contain the asserted policies. No policy divergence was identified in the committed a-j compact/detail table comparison; matching IDs alone was not treated as semantic proof.
- Literal searches of the specified cadence span and ledger both return false for `service-limits`, as reported. This is not semantic-reference proof.

### Read-only sweep and output

Command used for committed inputs: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:<path>` for SKILL.md, service-limits.md, and every retained anchor's file. Python stdlib documentary comparison (not importing candidate code) trimmed trailing whitespace-only section lines, joined with `\n`, and calculated `hashlib.sha256`; normalization was read from frozen round-18 measure.py:209–253. Each anchor compared retained numbered text against `"\n".join(f"{n}: {committed[n-1]}" ...)` for its declared range.

Observed output:
```text
NORMALIZED_SECTION_SHA256 7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6
NEXT_HEADING ## The operator's runbook and the six-leg regression (round 10, measured)
ANCHOR_COMMITTED_MATCH [each of 17 declared blocks] True
ANCHOR_BLOCK_COUNT 17
CADENCE_NAMES_SERVICE_LIMITS False
LEDGER_NAMES_SERVICE_LIMITS False
RECEIPT_SECTION_NORMALIZED_MATCH True
PAGE_ROW_IDS a,b,c,d,e,f,g,h,i,j
NOTE_ROW_IDS a,b,c,d,e,f,g,h,i,j
```
The first local comparison parser accidentally allowed multiline anchor paths and raised IndexError; it was corrected to `[^\n]+`, then all 17 comparisons completed. A raw-section digest differed because it included trailing newlines; that is expected, not a report defect. An initial unnormalized section comparison returned false from separator newlines; normalized comparison above returned true.

## Residual risk / verification gaps

`read xd://lsp` returned `No such tool`; semantic references/definitions/diagnostics were unavailable. No execution authenticity, current runtime behavior, NO-HARM 64/64, canonical-runtime identity, rerouting, saturation, or resume preflight guarantees are established by this section or this audit. Existing outputs are unsigned retained observations. The claimed removed scratch clone was not recreated. No tools installed/updated; only this seat's d4 report pair written.

Recommendation: bounded documentary agreement, with the existing citation defect and execution-provenance qualification retained; no integration/admission conclusion.

Self-evaluation: accuracy 4 (retained execution cannot be authenticated); completeness 4 (no independent historical command transcript exists in the assigned receipt directory); clarity 4 (explicit separator/parser caveats add detail); actionability 4 (provenance qualification is actionable, historical receipt recovery is not established); conciseness 4 (sweep evidence retained inline). Overall 4.0. Highest-impact improvement: distinguish author-reported exit status from retained command transcripts. Would the user agree? Expected, within the documentary-only scope.
