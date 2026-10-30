# T57D4Read01 — documentary review of Standing rules

**Recommendation:** bounded agreement with retained evidence, with the gaps below. Current integration remains **UNVERIFIED**; this is not admission or a fresh runtime pass.

Axes: claim/receipt consistency; committed-byte identity; evidence completeness; no execution/admission.

## Findings by severity

### Medium — E1: execution-to-revision evidence is incomplete

T57W3Read01.md:3,15,20 describes C0b execution and says each command ran. All 19 records agree exactly with the individual retained JSON receipts (command, cwd, declared TMPDIR, exit, stdout, stderr), but none records a revision/hash field. `T57W3Read01-receipts/pointers.py:8-15` separately obtains C0b SKILL bytes, clone HEAD, and eight working-tree hashes; it does not retain a clean-tree observation or bind each command's executable bytes at execution time. The gate receipt contains 19 PASS summaries, not raw child-run records. These are consistent unsigned observations, not independent historical execution authentication. Do not elevate `verified-record` to clean-C0b runtime certification or current integration admission.

### Low — E2: prepared fixture input is unavailable in the retained bundle

`T57W3Read01.md:127-132,181` and `T57W3Read01-receipts/env-diff-contract-prepared.json` name `/fast/scratch/hyaku/tameshi-r57/T57W3Read01/env-contract.json`. Its content/digest is not retained among the 19 JSON receipts and pointers.py. The prepared output supports the claimed refusal as an observation, but not exact fixture-dependent reproduction. The earlier missing-fixture failure is honestly disclosed and is not the prepared scratch-refusal observation.

All source references above are under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/`.

## Bounded agreement and commands/output

No candidate code was executed. Read-only source command actually used:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Output: `## Standing rules` at lines 17–57, ending before `## Source notes`. Pure local data analysis of that output stripped trailing blank lines and joined with LF/no terminal newline, following the source-read definition at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py:209-251` (not imported/executed). Observed output:

```text
NORMALIZED_SECTION 17 57 d7042aa08484f1a8c72c7228dd668c0cb89baa83533b12b8b8f9839f0ef5093c MATCH True
```

An initial raw slice hash differed because it retained trailing newlines; that is not a report defect. Normalized hashing matches the report exactly.

Executed data-analysis sweep (Python Eval; `base` and `receipts` were the absolute assigned w3 directory and its T57W3Read01-receipts directory):

```python
for c in r['commands']:
    p = receipts / (c['name'] + '.json')
    d = json.loads(p.read_text())
    checks.append({'name': c['name'], 'equal': c == d, 'exit': d['exit'],
                   'stdout_lines': len(d['stdout'].splitlines()),
                   'stderr_lines': len(d['stderr'].splitlines())})
print(json.dumps(checks, indent=2))
```

Output: **19/19 equal=true**; the complete per-command results are in the sibling D4 JSON. The Markdown command/exit blocks were also compared with the JSON:

```text
MD_JSON_COMMAND_MATCH 19 True
ALLOCATING_REFUSALS 9
LAZY_MODES 5
```

The nine refusal records have exit 2 and one matching stderr line; repeat-control also has its disclosed setup-error stdout. The five lazy observations have exit 0. Corrected helper output has 21 PASS lines; the earlier helper assertion failure remains retained and disclosed. The gate receipt ends `GATE_SELFTEST: 19/19 pass`, exit 0; this review did not rerun it.

For each of the eight `POINTER` lines in the existing pointer stdout, the actual analysis invoked `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:<recorded-path>`, hashed its bytes and compared with the recorded digest. Output: **8/8 MATCH True**: PROVINCE.md, gate, registry, scratch-root contract, both mutation census notes, round-55 C2 counter, round-56 C2 counter. No mismatch was found.

Canonical source was read using:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:tools/receipt-revision-gate.py
```

Its `check` logic at lines 139–159 is consistent with the section's same-revision/content-equivalent positive/verdict and ancestor-control rules; `run` resolves the certified revision before checking receipts and returns 2 when unresolvable. This is source agreement only. No resume path or saturation assertion is certified by this assigned item.

## Residual risk and verification gaps

- Retained census output says 3202 files, dash=0, slash=7354, but its historical census was not independently rerun. The report correctly bounds this as a literal convention census.
- Helper-only usable/empty/unset observations do not establish all full-command success paths; the original report explicitly says so.
- External URL resolution, historical execution authenticity, allocation tracing and current integration were not tested.
- LSP unavailable: `read xd://lsp` returned `No such tool`. Literal source/data review is not semantic reference proof.
- No candidate gate, existing pointer script, counter, test, build, or frozen sectionizer was executed. No 64/64 monitor result or round C1/C2 admission is claimed. No tools installed, production edits, commits, or delegation.

## Self-evaluation

Accuracy 4/5: normalized committed hashes and all 19 receipt comparisons observed; historical execution authenticity remains unavailable. Completeness 4/5: assigned evidence covered, not rerun under the documentary-only restriction. Clarity 4/5: two gaps separated from matching observations. Actionability 4/5: explicitly limits downstream certification. Conciseness 4/5: command evidence retained for auditability. Overall 4.0/5. Improvement: retain prepared fixture bytes and execution-input bindings in future authorized records; no new execution is requested here. User-agreement self-check: the distinction between documentary agreement and admission is explicit.
