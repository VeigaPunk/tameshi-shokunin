# T57D4Read18 — documentary audit

## Scope and axes

Axes: command/result fidelity, candidate/section identity, retained-evidence completeness, non-execution. Reviewed T57W3Read18.md/.json and all 57 retained JSON files. Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392` (C0b). SKILL source was read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`, not executed.

## Findings by severity

### Low — individual selftest receipts lack candidate binding

`w3/T57W3Read18.json:4,31-38` attributes the sweep to C0b, but every `T57W3Read18-receipts/selftest-*.json` contains only `command`, `cwd`, `exit`, `stdout`, `stderr`, and `seconds`. No retained clone-checkout/HEAD or tool-digest observation accompanies those receipts. A scratch pathname is not revision evidence. The two registry observations do embed `rev_resolved=C0b`; that supports those observations, not independently the earlier standalone selftests. This is missing provenance, not evidence that the commands were run against a different revision or fabricated. Preserve that distinction; do not promote the sweep into independently revision-bound proof without retained identity evidence.

Audit command: Python Eval over the existing JSON only:

```python
print(sorted(set().union(*(set(r) for n,r in receipts.items() if n.startswith('selftest-')))))
```

Output:

```text
['command', 'cwd', 'exit', 'seconds', 'stderr', 'stdout']
```

## Bounded agreement

- All 56 command objects match a retained receipt on command, cwd, exit, full stdout/stderr and seconds (including the sectionize object, whose omitted fields match omission). Audit: Python Eval compares these six fields for every report command against all receipts. Output: `COMMAND_RECEIPT_MATCH 56 / 56`.
- Thirty distinct documented selftests have retained success after the tally-v3 retry. The timeout is preserved, not hidden: `selftest-20.json` exit 124 at 240.01 s; `extended-01.json` exit 0 at 332.1 s, ending `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`. Context 49/49, MTE 17/17, registry 51 cases, repeat-control 29 cases and standalone MTE 10/10 match their retained summaries.
- Section lines 2175–2214 and SHA `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52` agree with C0b after the documented round-18 canonicalization (strip trailing blank lines; join with LF; no trailing newline). Audit: hash that slice of the `git show` bytes in Python Eval. Output: `CANONICAL_SECTION_SHA256 cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`. No candidate counter was imported or executed.
- `entry-01.json` records exit 1, held 51/53, superseded 7, C0b `rev_resolved`; its active failed rows are exactly `sources-census` and `verify-round15`, each expect 0/got 1. Both MTE rows are held. The earlier `extended-02.json` records 49/53 and the two additional setup failures, consistent with the narrative's distinction.
- `entry-02.json` exactly supports the reported witness drift and exit 1. Reading the committed runner via `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:tools/mutate-and-run.sh` and hashing its bytes in the audit process yields `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`, matching the observed runner digest. The committed SKILL cells document failure exit 1 for both entries, so these reds do not contradict those exit maps.
- Pointer receipt lists 90 paths, all recorded present. A read-only `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only adf87899c70d616140a81185a8f9acbbdfb30392` comparison resolves 89 as committed files/directories. The sole exception, `tools/__pycache__`, is explicitly a possible runtime-created write location in the shrink-case cell, not a missing required committed input. Path existence alone does not establish pointer content integrity.

## Residual risk and verification gaps

These are unsigned retained observations, not execution authentication. Read-only sibling-link setup and endpoint immutability are asserted but not independently proven by the listed command receipts. Fleet-dependent checks do not prove hermeticity; the report appropriately makes no such claim. No saturation, canonical-runtime, rerouting or resume-continuity conclusion is established by this scoped evidence. No fresh runtime, gate, test, build, candidate measure, or exploit was executed. No production or frozen evidence was modified. No tooling was installed. LSP device unavailable (`xd://lsp`: `No such tool`); documentary/byte inspection is fallback, not semantic caller proof.

Recommendation: bounded documentary agreement with the provenance gap above. Current integration remains **UNVERIFIED**; this is not admission and does not establish the round-wide 64/64 monitor.

Self-evaluation: accuracy/completeness/clarity/actionability/conciseness 4/4/4/4/4 (4.0). Evidence is internally consistent; missing standalone revision observations limit certainty, and aggregate comparison details are summarized rather than attaching duplicate receipts. Improvement: retain identity observations with future execution receipts. The user should accept the bounded, non-admission characterization.
