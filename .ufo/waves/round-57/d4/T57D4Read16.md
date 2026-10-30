# T57D4Read16 — bounded documentary agreement

## Findings by severity

No concrete contradiction found within the assigned report/receipt/C0b comparison. This is documentary agreement, not runtime verification or admission. Current integration remains **UNVERIFIED**.

Axes: command/result consistency; committed section identity; retained pointer integrity; provenance limits.

## Evidence sweep (analysis only)

Inputs: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16.json`, matching `.md`, and the adjacent `T57W3Read16-receipts/` directory. All 17 command records were compared field-for-field to their named retained JSON receipts, including command, cwd, integer exit, stdout, stderr, and elapsed_s. Output: `COMMAND_METADATA_AND_STREAM_COMPARISON 17 records all equal retained JSON`; every record's `REPORT_DIFFERENCES` was `[]`. Narrative command strings and exits agree with those records.

Read-only command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Read the complete assigned section, lines 1968–1980, containing eight rows. Independently hashed these committed lines using the documented sectionizer convention: remove trailing whitespace-only lines, join by newline, no terminal newline. Output: `CANONICAL_SECTION_HASH 661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e MATCH True`. The normalization rule was source-read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:.ufo/evidence/round-18/measure.py` (sectionize definition); no candidate code was imported or executed. Hashing the unnormalized line slice initially differs because it includes trailing newlines; that is not a report defect.

For each of the 22 `POINTER OK` lines retained in `T57W3Read16-receipts/section-audit.json`, ran the same read-only `git show` command with that exact repo-relative path in place of `SKILL.md`, then compared SHA-256 of returned bytes against the retained digest. Output: `POINTER_HASH_COMPARISONS 22`, all `True`. The retained collector's `inputs.SKILL.md` also equals C0b's complete SKILL blob digest: `TRACE_SKILL_HASH_MATCH True`. Thus both section and retained pointer digests agree with committed C0b, rather than merely with each other.

Retained output supports the narrative counts: registry `SELFTEST: PASS (51 cases)`; evidence `SELFTEST: PASS (66/66)`; witness `WITNESS_SELFTEST: 51/51 pass` and `VERDICT: PASS`; trace `SELFTEST: 30/30`; round-18 `MEASURE_SELFTEST: 98/98 pass`; assembler `SELFTEST: 80/80 pass`; round-19 correction `SELFTEST: 43/43`; selector `SELECTOR_SELFTEST: 3/3 pass`.

The initial defect-probes receipt records exit 2 and `PROBE P11 error ProbeError: read-only kagi-shokunin source is unavailable for the P11 fixture`; its later fleet-layout receipt records exit 0 and `DEFECT_PROBES: open=0 closed=11 total=11`. Both attempts remain disclosed. `r19-check.json` stdout names C0b and reports corrected=5, open=0, total=5. `witness-count.json` ends `unresolved\tnone`. The collector example is retained separately as `example-trace.json`, names C0b, and records exit 0.

Both retained historical cold-read measurements name C0b and report `sections_covered: 11`, `sections_total: 64`, `box3_full_page: false`; their assigned section has `credited: false`, reason `no-ledger-entry`. This does not contradict the reader report, which explicitly distinguishes historical input-keyed measurements from required-command coverage. It cannot establish the deciding round-21 64/64 monitor requirement.

## Residual risk and verification gaps

- Receipts are retained observations, not independent execution authentication. No commands claimed by the old report were rerun; no candidate gate, test, build, exploit, credential, or external target was exercised.
- Ordinary command receipts lack an environment snapshot. The report's scrubbed inherited GIT_* / TMPDIR claim and scratch sibling-symlink setup are not independently proven by those records. The collector retains its own environment overrides, but that does not attest every other invocation's environment.
- Clone HEAD is asserted by the retained section-audit source, and its 22 printed file hashes agree with C0b. That does not prove transient cleanliness of every clone file throughout every earlier run. The live sibling dependency remains a provenance limitation, not a newly reproduced result.
- Source-only review does not establish universal process cleanup, UID-transition handling, same-tick PID reuse safety, or adopted-orphan safety. Those limits are expressly named in the committed section and original report.
- LSP discovery returned `No such tool: xd://lsp`; semantic references/definition/diagnostics were unavailable. This audit uses committed bytes and documentary comparisons, not semantic caller proof. Canonical runtime/rerouting, saturation, resume continuity, and candidate integration acceptance are not established by this scoped section audit.

No production/frozen files edited; no tools installed or upgraded. Only this seat's d4 report and JSON written.

## Self-evaluation

Accuracy 4/5: byte identity and retained comparisons observed; execution provenance remains unattested. Completeness 4/5: all 17 commands and 22 pointer digests covered; environment claims cannot be independently recovered from these receipts. Clarity 4/5: summarized outputs require following the named originals for full streams. Actionability 4/5: identifies exactly which claims cannot support admission, without supplying new runtime evidence. Conciseness 4/5: evidence inventory is longer than the conclusion. Overall 4.0/5. Highest-impact improvement: preserve per-invocation environment/provenance alongside future observations. Self-check: the bounded result should be distinguishable from an acceptance decision.
