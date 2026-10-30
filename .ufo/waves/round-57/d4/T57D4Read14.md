# T57D4Read14 — documentary audit

Axes: command/result fidelity; C0b/section binding; retained-evidence completeness; defensive scope.

## Findings (severity order)

### Low — retained evidence does not support every verification claim

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read14.md:9,25,43,54` claims a detached candidate clone, read-only sibling symlinks, resolved primary URLs, and no lane changes. The twelve indexed receipts do not retain checkout/HEAD identity, symlink setup or permissions, URL fetches, or before/after lane-state evidence. This is missing evidence, not proof those statements are false. Receipt 7 records only `rev-parse --show-toplevel`; recipe 4's retained read (receipt 8) uses `refs/remotes/origin/master`, not the documented `refs/heads/<branch>`. Its returned source does equal C0b's source, so no source-content contradiction was found. Narrow those assurances to retained evidence rather than treat them as independently certified.

Executed documentary sweep (Python Eval; no candidate execution):

```python
receipts = [json.loads(pathlib.Path(c['receipt']).read_text())
            for c in report['commands']]
for i, r in enumerate(receipts, 1):
    print(i, r['command'].split('\n')[0])
```

Output: twelve commands; 1–6 and 11–12 invoke the disposition/registry tools, 7 is `rev-parse --show-toplevel`, 8 is the remote-tracking source read, 9 computes section metadata, and 10 checks local file/source-ID existence. No checkout, `rev-parse HEAD`, symlink inspection, URL-fetch, or lane-state comparison is indexed. All twelve receipt command strings and exits match the JSON report exactly; all twelve cwd values name the reported clone.

## Bounded agreement

Read committed SKILL through `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md` only. Read lines 1857–1888 end to end. Documentary hashing (trim trailing blank lines, join with newline, no trailing newline; definition read at frozen measure.py:209–253) returned:

```text
1857 1888 6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac
next heading: ### Round-17 gate/probe registry — re-pin and monitor
```

This agrees with both reports and receipt 9. No frozen module was imported or executed in this audit.

All twelve retained outputs were inspected. Receipt 1 supports exit 1 / `producer_before` / `expected_contains_missing`; 2 supports clean exit 0, effective 11, superseded 1; 3 contains exactly three HISTORICAL lines; 4 records 49/53, seven superseded; 5 records 51/53, seven superseded and only sources-census/verify-round15 differing; 6 records `SELFTEST: PASS (66/66)`; 8 contains 60304 characters; 10 lists all named local pointers and S061–S063 as RESOLVES; 11–12 record exit 2 / expected_input_digest_mismatch. These are retained historical observations, not newly passed checks.

Read-only `git show C0b:<path>` and SHA256 yielded:

```text
tools/evidence-disposition.py f09d1e490b94edb75364825c3941eb88cfb88a76ae26a2b9257e923ac123ea93
tools/registry.json f1b67d2ad2a95a3fb606105e7b20c8bf00c098303085a635bc95a8ff5def205d
tools/bash-witness-study.py f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261
tools/pin-disposition.py c917bc41c3f40dae3eacea492d861211c2a4fe1e530cb9f22c5f8d6ff47d2988
receipt8_equals_C0b_source True
```

Disposition receipts' tool hashes, registry receipt 5's registry hash and rev_resolved, and receipts 11–12's observed instrument hash match these committed blobs. This provides partial candidate binding despite absent clone-HEAD attestation. The section explicitly allows registry exit 1 on differing rows and promises no numeric all-green tally; the two differing rows are not a contradiction of that contract.

## Residual risk and verification gaps

- Receipt 5 retains the registry CLI output, but row evidence uses `stdout_tail`/`stderr_tail`, not complete underlying child streams. Its verify-round15 cause cannot be reconstructed completely from these tails. Do not extend “unabridged output” to child processes.
- Local existence/source-ID checks do not prove URL reachability or every source-line interpretation. This audit does not independently certify historical causality, all cited source ranges, symlink properties, or absence of transient writes.
- `xd://lsp` returned `No such tool`; semantic references/definition/diagnostics were unavailable. Direct documentary reads are not semantic proof.
- No runtime, rerouting, saturation, or resume-continuity claim is established by this section. Candidate integration remains UNVERIFIED; this report grants no admission and does not establish 64/64 NO-HARM.

No gates, tests, builds, exploits, credential access, external targets, alternate runtimes, delegation, git mutations, production edits, or tool installs were performed. Only this seat's d4 report/JSON were written.

Self-evaluation: accuracy 4 (receipt provenance remains unauthenticated); completeness 4 (historical source interpretations intentionally not re-certified); clarity 4 (detailed evidence increases length); actionability 4 (missing original observations cannot be recovered here); conciseness 4 (hash detail retained for binding). Overall 4.0/5. Highest-impact improvement: qualify unsupported provenance/URL assurances. User-agreement check: documentary agreement is bounded, never a fresh execution pass.
