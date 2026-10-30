# T57W3Read12 — verified-record

## Effective expectation reconciliation — round 14

Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`. Frozen sectionizer: lines 1606–1639, SHA256 `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe`. Read end to end in detached C0b clone.

## Findings

None. Expected nonzero outcomes matched the documentation; no failed command was represented as a clean result.

## Executed sweep

- `frozen-sectionize`: exit 0; command `python3 -c 'import importlib.util,subprocess; p='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'"'"'; s=importlib.util.spec_from_file_location('"'"'frozen'"'"',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); raw=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"','"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"','"'"'show'"'"','"'"'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'"'"']); sec=next(x for x in m.sectionize(raw) if x['"'"'heading'"'"']=='"'"'## Effective expectation reconciliation — round 14'"'"'); print(sec['"'"'start'"'"'],sec['"'"'end'"'"'],sec['"'"'sha256'"'"'])'`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/frozen-sectionize.json`.
- `live-before`: exit 2; command `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/.ufo/evidence/round-14/dispositions-before.json --json`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/live-before.json`.
- `live-after`: exit 2; command `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/.ufo/evidence/round-14/dispositions.json --json`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/live-after.json`.
- `archive-before`: exit 1; command `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read12/archive-28aeef4/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read12/archive-28aeef4 --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read12/archive-28aeef4/.ufo/evidence/round-14/dispositions-before.json --json`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/archive-before.json`.
- `archive-after`: exit 0; command `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read12/archive-28aeef4/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read12/archive-28aeef4 --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read12/archive-28aeef4/.ufo/evidence/round-14/dispositions.json --json`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/archive-after.json`.
- `retained-context`: exit 0; command `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/tools/context-capture.py --check`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/retained-context.json`.
- `current-repin`: exit 0; command `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone/.ufo/evidence/round-18/dispositions.json --json`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/current-repin.json`.
- `record-pointer-audit`: exit 0; command `python3 -c 'import pathlib,json,hashlib,re
p=pathlib.Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read12/clone'"'"')
e=json.loads((p/'"'"'.ufo/evidence/round-13/expected.json'"'"').read_text())
print('"'"'expected_checks'"'"',len(e['"'"'expected_checks'"'"']),'"'"'inputs'"'"',len(e['"'"'inputs'"'"']))
print('"'"'stale_inputs'"'"', [k for k,v in e['"'"'inputs'"'"'].items() if hashlib.sha256((p/k).read_bytes()).hexdigest()!=v])
b=json.loads((p/'"'"'.ufo/evidence/round-14/dispositions-before.json'"'"').read_text()); a=json.loads((p/'"'"'.ufo/evidence/round-14/dispositions.json'"'"').read_text())
print('"'"'manifest_difference'"'"', {k:[b.get(k),a.get(k)] for k in set(a)|set(b) if a.get(k)!=b.get(k)})
for f in ['"'"'verification-final.json'"'"','"'"'verification.json'"'"']:
 d=json.loads((p/'"'"'.ufo/evidence/round-14'"'"'/f).read_text());print(f,'"'"'measured_commit'"'"',d.get('"'"'measured_commit'"'"'))
 for c in d['"'"'checks'"'"']:
  print(c['"'"'name'"'"'],'"'"'exit'"'"',c['"'"'exit'"'"'],'"'"'stdout'"'"',c['"'"'stdout'"'"'])
text=(p/'"'"'SKILL.md'"'"').read_text().splitlines(); section='"'"'\n'"'"'.join(text[1605:1639]); refs=sorted(set(re.findall(r'"'"'\`([^\`]+)\`'"'"',section)))
for ref in refs:
 if ref.startswith(('"'"'corpus/'"'"','"'"'.ufo/'"'"','"'"'tools/'"'"')) and not '"'"' '"'"' in ref: print('"'"'pointer'"'"',ref,'"'"'exists'"'"',(p/ref).is_file())
print('"'"'source_rows'"'"', [line for line in (p/'"'"'corpus/SOURCES.md'"'"').read_text().splitlines() if re.match(r'"'"'\| S00[3] |\| S049 '"'"',line)])
'`. Complete stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read12-receipts/record-pointer-audit.json`.

Results: live before/after both 2 `expected_input_digest_mismatch`; extracted `git archive 28aeef4` before 1 with only `producer_before` missing assertion, after 0 with 11 passing effective rows and one explicit supersession retaining raw mismatch and both passing oracle replacements. Current round-18 re-pin returned 0; maintained retained-context gate returned 0 `context_consistent`. Static audit confirmed twelve expected checks, thirteen inputs, precisely three stale inputs, all named file pointers, and both retained verification histories. Corrected historical selftest is 34/34; initial record retains 18/34 failures and separate measured revision.

## Residual risk and verification gaps

- Axes: calibration, executable accuracy, pointer integrity, historical-evidence preservation.
- LSP unavailable: xd://lsp returned No such tool; text inspection and executable receipts are fallback evidence, not semantic reference proof.
- Live manifests returning 2 and archived before returning 1 are documented expected outcomes, not new findings.
- Archived capture-context.py was inspected but deliberately not executed; maintained retained-only --check returned 0.
- Historical corrected 34/34 and initial 18/34 failures were inspected as retained records, not claimed as newly executed selftests.
- No full-page, independent promotion, target execution, safe reuse, general hermeticity or saturation claim. External vendor pages were not freshly fetched; source rows and retained quotations were checked locally.
- No tools installed or updated. No content edits staged or applied.
