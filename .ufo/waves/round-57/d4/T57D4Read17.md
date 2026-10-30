# T57D4Read17 — documentary audit

## Scope and axes
Axes: candidate/section fidelity; command-to-receipt consistency; claim restraint; read-only compliance. Reviewed the assigned W3 Markdown/JSON and all 22 numbered receipts plus section/environment/refusal sidecars. Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`. Recommendation: **bounded documentary agreement**, not admission. No actionable contradiction found in the assigned report.

## Evidence
All paths below are under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/` unless fully qualified.

- `T57W3Read17.json` candidate agrees with the report and revision-bearing C1/C2/coldread/refusal records. Every command record matches its retained numbered receipt on name, command, cwd, exit, stdout, stderr and seconds: **22/22**, no missing receipt.
- Read the corresponding SKILL section exclusively through `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md`. Lines 2007–2146 exactly equal `T57W3Read17-receipts/section.txt`; next heading is `## Ninth recorded case — round 26`. Raw retained bytes hash to `dcb4388c67b8c36832de0766d6508e6cd30ce40dada8a9ed77e69666dc2a64e2`. This is **not** a metadata discrepancy: the committed round-18 `measure.py` sectionize definition strips trailing blank lines and joins with no trailing newline. Independently applying that documented normalization gives the claimed `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06`.
- Receipts 01–07 retain the reported seven passing selftest summaries; 10/17 retain expected-red TOTAL_MISMATCH/ARGV_MISMATCH, while 11/12 retain clean exits. These are observations in existing files, not newly executed checks.
- Receipts 13/19 retain exits 1/0 and classified 0/9 versus 9/9. `env-default.json` has nine unavailable/PIN_UNREADABLE rows. `env-explicit-fleet.json` has nine classified rows (three invariant, five env-sensitive, one nondeterministic). Both instrument hashes equal the C0b `tools/env-diff.py` blob. Its committed source defines default fleet root as `Path(__file__).resolve().parents[2]`, supporting the reported clone-guidance gap at SKILL.md:2018.
- Receipt 08 records route concentration refusal (34/71), not a pass. Receipt 18 records projection of 43 historical rows with 41 not declared live and two declared live. Receipt 20 records exit 1/RUNNER_NOT_HELD with the three named refused rows and null bundle hash; its stdout contains runner progress before the final JSON object. No standalone-JSON guarantee is inferred.
- Receipts 14/16 support retained C2 9/9 and C1 18 killed/zero survived/zero inconclusive. Receipt 15 explicitly records 46/64 and `box3_full_page:false`, consistent with the report's refusal to claim 64/64. Receipts 21/22 retain pointer, frozen-input and prefix-population observations. The section's appended corrections match the report's caveats about live fleet reads, unsigned observations and non-isolation.

## Executed documentary sweep (command and output)
Only standard-library data processing and read-only git show were used; no candidate module was imported or executed. In Python Eval, `root = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')`, `r = root / '.ufo/waves/round-57/w3'`, and `j = json.loads((r / 'T57W3Read17.json').read_text())`:

```python
for c in j['commands']:
    d = json.loads(pathlib.Path(c['receipt']).read_text())
    print(pathlib.Path(c['receipt']).name, {
        k: [c[k], d.get(k)]
        for k in ['name', 'command', 'cwd', 'exit', 'stdout', 'stderr', 'seconds']
        if k in c and c[k] != d.get(k)
    })
```

Observed output: all 22 numbered receipt names printed `{}`; aggregate comparison printed `commands 22 matching 22`.

Additional executed read-only calculations printed:

```text
raw equality True
canonical section digest eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06 metadata match True
next heading ## Ninth recorded case — round 26
env-default.json rows 9 classes {'unavailable': 9} pin_unreadable 9 instrument matches C0b True
env-explicit-fleet.json rows 9 classes {'invariant': 3, 'env-sensitive': 5, 'nondeterministic': 1} pin_unreadable 0 instrument matches C0b True
coldread summary {'box3_full_page': False, 'inputs_overlay_merged': 0, 'ledger_present': True, 'sections_covered': 46, 'sections_total': 64}
```

The hash calculation reads the C0b SKILL blob with the git-show command above, slices `splitlines(keepends=True)[2006:2146]`, compares retained section bytes, removes trailing whitespace-only lines, joins remaining lines with `\n`, then uses `hashlib.sha256`. The normalizer's source was read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:.ufo/evidence/round-18/measure.py`; no frozen code execution occurred.

## Residual risk and verification gaps
- Retained receipts are unsigned local declarations; agreement does not authenticate their producer, establish original clone checkout/working-tree cleanliness, or prove absence of transient writes. The report already disclaims execution authentication. No independent execution verification is claimed here.
- Current candidate integration remains **UNVERIFIED**. No 64/64 repair, wave admission, runtime saturation, rerouting, or resume-continuity claim follows from this audit.
- LSP is unavailable (`read xd://lsp` returned `No such tool`); source inspection was used without semantic caller claims. This item is documentary, with no changed code requiring caller migration.
- An initial source lookup of round-18 `coldread/measure.py` failed (path absent); the retained metadata receipt identifies the correct `.ufo/evidence/round-18/measure.py`, which was then read. A whole-stdout JSON parse of receipt 20 failed because progress lines precede JSON; the raw retained receipt was inspected instead. Neither inspection error is attributed to the candidate.
- No gates, tests, builds, external targets, installs, commits, production edits, or runtime admission actions were performed. Only this seat's D4 report and JSON were written.

## Self-evaluation
Accuracy 4/5: retained evidence, not execution provenance. Completeness 4/5: all assigned commands and metadata compared; external producer identity deliberately unverified. Clarity 4/5: raw versus canonical hashes explicitly distinguished, but evidence is necessarily dense. Actionability 4/5: bounded recommendation supplies no new independent run receipt. Conciseness 4/5: full command streams remain in existing receipts. Overall 4.0/5. Highest-value improvement would be independently authenticated execution evidence, outside this documentary-only assignment. The bounds should make this assessment reproducible for the reader.
