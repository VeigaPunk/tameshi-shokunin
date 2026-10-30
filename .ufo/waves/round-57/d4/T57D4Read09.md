# T57D4Read09 — documentary audit

Recommendation: bounded documentary agreement, with one low-severity wording finding. Candidate integration remains **UNVERIFIED**; no admission is recommended.

Axes: claim precision, retained-evidence consistency, committed-byte identity, scope restraint.

## Findings by severity

### Low — “Every entry mode … ran” exceeds the retained command inventory

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read09.md:12` says “Every entry mode and selftest ran.” Its retained `witness-usage.json` lists the modes `{declare,run,rerun,count,check,selftest}`, but the 20-command aggregate and individual receipts contain no `declare` invocation. Thus the blanket all-modes execution claim is unsupported. This is not evidence that declaration failed, nor a request to execute it. Narrow the sentence to the documented entry commands and retained checks.

Documentary command executed in Python Eval (not a candidate invocation), with `report` loaded from the absolute assigned JSON:

```python
[e['name'] for e in report['commands']
 if 'bash-witness-study.py declare' in e['command']]
```

Output: `[]`. The retained usage receipt's stderr reads `choose from 'declare', 'run', 'rerun', 'count', 'check', 'selftest'`.

## Bounded agreement and sweep evidence

All paths below are beneath `/home/vgpnk/Projects/shokunin/tameshi-shokunin/`; all actual tool path arguments were absolute.

1. Parsed `.ufo/waves/round-57/w3/T57W3Read09.json` and all 20 adjacent `T57W3Read09-receipts/<name>.json`. Compared `command`, integer `exit`, `stdout`, and `stderr` per entry using:

   ```python
   [key for key in ('command','exit','stdout','stderr')
    if receipt.get(key) != entry.get(key)]
   ```

   Output: `[]` for every one of 20 entries; no missing receipt. Reported exits match retained records: repeat selftest/run/clean 0, mismatch 1; witness selftest/count 0, check 1, run/rerun 2, usage 64; receipt selftest/accept/verdict/control 0, content drift 3, unresolvable certified 2, usage 1. These are documentary matches, not newly executed results.

2. Read SKILL exclusively through:

   ```sh
   git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
   ```

   Exit 0. Independently sliced lines 1541–1558 and SHA-256 hashed newline-joined text after stripping trailing whitespace-only lines, following the source algorithm at `.ufo/evidence/round-18/measure.py:209–253` without importing or executing it. Output: `1dcb4f7f561650a558fc7218316725ececa9af65955338ba78f96e1820564fa9`; metadata hash match `true`; retained frozen-sectionize header match `true`; retained section text match `true`.

3. Documentary Git-blob sweep used `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show REV:PATH` and `hashlib.sha256(blob).hexdigest()` for the 14 `POINTER_OK` entries retained in `pointers-history-integrity.json`. Output: all 14 `matches_C0b: true`. Recomputed hashes for the C0b manifest's listed blobs: `manifest_files: 95`, `manifest_mismatches: []`. The manifest itself remains unpinned by that manifest; no stronger provenance is inferred.

4. The same Git-blob sweep produced runner SHA-256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`, matching retained witness drift diagnostics. Historical command:

   ```sh
   git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md
   ```

   Retrieved through the documentary analysis subprocess; retained complete stdout comparison: `historical_checklist_matches: true`. Box 3 is scope-bounded `[~]`, as claimed.

5. Compared corresponding section text from `git show 5e3569969b532310d2b8a3d130901757a3df356b:SKILL.md` against C0b using `difflib.unified_diff`. Output adds the receipt-revision registry row and widens registry scope to include that gate; other substantive section claims are unchanged.

## Residual risks and verification gaps

- Receipts have only `name`, `command`, `exit`, `stdout`, `stderr`. A command string naming a clone directory is not an independently captured clone HEAD or cleanliness observation. The source hashes and section bytes agree with C0b, but the report's claim that every command ran in a detached C0b clone is not independently authenticated by these files. No allegation of fabrication follows.
- Existing stdout selftest tallies (29, 51, 19) are retained observations only. No test, build, candidate gate, declaration, mutation sweep, external target, or security bypass was executed in this audit.
- No canonical-runtime, same-identity rerouting, saturation, global 64/64 NO-HARM, or resume-continuity claim is established by this assigned pair. The report explicitly disclaims those broader conclusions. Resume paths were not exercised or audited here.
- `xd://lsp` returned `No such tool`; no semantic caller/definition/diagnostic proof is claimed. This task compared documentary artifacts and committed blobs, not changed runtime callers.
- No tools installed or updated. No production, frozen, stage, or receipt files written; only this seat's two d4 reports.

## Self-evaluation

Accuracy 4/5: static byte matches cannot authenticate execution. Completeness 4/5: all 20 receipts compared; runtime verification deliberately prohibited. Clarity 4/5: documentary commands require the stated Eval context. Actionability 5/5: narrow the one overbroad sentence without rerunning anything. Conciseness 4/5: full evidence inventory retained for auditability. Overall 4.2/5. Highest-impact improvement: distinguish listed commands from all supported modes; retain revision observations in future authorized runs. The bounded assessment should match the requested documentary scope.
