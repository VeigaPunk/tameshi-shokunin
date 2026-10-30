# T57D4Read15 — documentary audit

## Recommendation
Bounded documentary agreement; no contradictory command/result or section metadata found. Candidate integration remains **UNVERIFIED**; this is not admission or a fresh runtime result.

Axes: claim/receipt consistency, committed-content identity, provenance completeness, defensive read-only scope.

## Findings by severity
No concrete result contradiction established. The reported registry failure is supported, not a falsely claimed pass: retained `registry-current.json` reports exit 1, held 51/53, superseded 7; `sources-census` and `verify-round15` each expect 0 and return 1. Their retained tails include S280's missing id-or-path citation and the context-capture source-pin mismatch exactly as quoted in the report.

## Documentary sweep and output
Read `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read15.json`, its `.md`, and all 17 referenced JSON receipts. No candidate code, gate, test, build, or imported counter was executed.

Committed source command (exit 0):

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Output at lines 1889–1897: the heading `### Round-17 gate/probe registry — re-pin and monitor`, its four tool rows, and trailing blank line; next heading starts at 1898. Independently hashing those section bytes after removing trailing blank lines and the final newline yields:

```text
309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c
```

This matches both report formats and `frozen-sectionize.json`. Normalization is supported by the source-only read of `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py:209–251`; the counter was not imported or run. Hashing the unnormalized slice is not the section-hash contract.

Read-only Python Eval sweep (not a candidate invocation): for each report command, `x=json.loads(Path(c['receipt']).read_text()); all(x[k]==c[k] for k in ['command','cwd','exit'])`. Output:

```text
AUDIT_SWEEP: receipts=17 missing=0 command/cwd/exit_mismatches=0
SECTION normalized_sha256=309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c
```

Retained summaries support all four selftest claims: evidence 66/66, registry 51 cases, runner 107/107 and VERDICT PASS, pin 19/19. Regression receipt records ten PASS legs and `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)`. Current evidence disposition is clean (11 effective passes, one superseded); old manifest is could-not-evaluate/exit 2. Negative invocation exits match the narrative (2, 64, and unusable-TMPDIR 2). Pointer sweep reports all eight pointers present.

Additional read-only `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:<path>` calls and SHA256 calculations returned:

| Path | SHA256 |
|---|---|
| tools/registry.json | f1b67d2ad2a95a3fb606105e7b20c8bf00c098303085a635bc95a8ff5def205d |
| tools/context-capture.py | 831b781054d701d7347df62c4044eb274a775967aaf0ce3d49bef4056b111d8d |
| tools/mutate-and-run.sh | 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda |
| tools/evidence-disposition.py | f09d1e490b94edb75364825c3941eb88cfb88a76ae26a2b9257e923ac123ea93 |
| tools/pin-disposition.py | c917bc41c3f40dae3eacea492d861211c2a4fe1e530cb9f22c5f8d6ff47d2988 |

These match the corresponding digests retained in the registry, regression, evidence and pin outputs. Registry stdout explicitly names and resolves C0b.

## Residual risk and missing evidence
- The 17 receipt envelopes contain command, cwd, exit and streams, but no universal clone HEAD/cleanliness capture. C0b identity is explicit for the registry revision mode and section read; matching tool digests strengthens selected other anchors, not complete tree/dependency identity for every invocation. A scratch cwd string alone is not proof of a pristine checkout.
- `registry-current.json` retains the full outer CLI JSON, but nested registry rows retain `stdout_tail`/`stderr_tail`, not complete child streams. The verify-round15 tail starts mid-line. Read the report's “full stdout/stderr” as outer-command retention only; complete child-output reconstruction is unsupported. The reported failure diagnostics are nevertheless present.
- Pin output is live fleet-dependent and explicitly says result reuse is not established; it reports one unchanged and five changed legs. The report discloses that limitation. Regression summaries do not independently establish the claimed read-only sibling-link setup or absence of transient writes. No separate setup/cleanup receipt is referenced.
- No authentication of execution, exhaustive error-map coverage, current 64/64 monitor result, saturation, same-identity rerouting, or resume-continuity guarantee follows from this documentary sweep. Runtime routing/resume changes are outside the assigned section; no such validation was performed.
- LSP device unavailable: `read xd://lsp` returned `No such tool`. Source-text fallback located hash normalization only, not semantic caller proof.

Only this seat's two d4 report files were written. No tools installed, production edits, delegation, commits, or runtime verification.

## Self-evaluation
Accuracy 4/5: unsigned historical evidence cannot authenticate execution. Completeness 4/5: all assigned receipts inspected, but historical checkout/setup provenance is incomplete. Clarity 4/5: separates outer streams from bounded child tails. Actionability 4/5: identifies exactly which provenance cannot be inferred. Conciseness 4/5: hash anchors add necessary length. Overall 4.0/5. Highest-impact improvement: retain explicit checkout identity and complete child streams in future authorized measurements; do not retrofit historical observations. User agreement expected because no unrun pass or admission is claimed.
