# T57D4Read08 — documentary audit

Bounded documentary agreement; clone execution provenance remains unverified. No admission.

Axes: revision/section identity; receipt consistency; evidence completeness; finite-sample honesty; non-mutation.

## Findings by severity

### Medium — D4-08-1

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read08.md:29`

Retained records do not independently establish the clone revision. The 12 command records contain no clone/checkout/rev-parse or clean-tree observation. All six decoded command.txt files record tool, tool-sha256, interpreter, python, cwd, runs and argv, but no revision. Candidate metadata and all four input hashes agree with C0b; this is documentary consistency, not proof that every command ran in that revision state.

Keep revision provenance unverified; retain an existing checkout/HEAD and relevant-input identity receipt if available. Do not rerun the candidate under this recovery assignment.

### Minor — D4-08-2

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md:1523 at adf87899c70d616140a81185a8f9acbbdfb30392`

The original minor source-pointer finding is confirmed: SOURCES.md:503 is the next-unused-id entry; S265 is at line 140 and explicitly supersedes S026. This is an existing documented defect, not a new runtime discrepancy.

Preserve the original gap-minor qualification; route correction outside this documentary seat.

## Bounded agreement

C0b section 1521–1540 hashes to `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831`, matching both reports. All four declared input hashes equal their C0b blobs. The 12 command records exactly equal commands.json; Markdown contains their commands and stdout/stderr. The eleven records declaring expected exits match those exits (sectionizer separately records exit 0). The nine primary runtime records plus existing-output refusal are therefore internally consistent. The 29 selftest case lines match its retained summary.

All six base64 raw observation groups decode cleanly. Their argv, cwd and tool digest match command records; observed exits and byte counts match their summaries. Matching fixture records contain stdout `ok\x00\n` and stderr `notice\n`; mismatch fixtures vary the stated stream or exit. No contradictory result found. These are comparisons of retained data, not fresh execution passes. The section explicitly bounds agreement to finite controls and calls the six-leg runner historical round 12.

## Documentary sweep: command and observed output

Executed via Python Eval (standard library; no candidate imports). Equivalent shell command:

```sh
python3 - <<'PY'
import base64, hashlib, json, subprocess
from pathlib import Path
r=Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
b=r/'.ufo/waves/round-57/w3'
j=json.loads((b/'T57W3Read08.json').read_text())
c=json.loads((b/'T57W3Read08-receipts/commands.json').read_text())
a=json.loads((b/'T57W3Read08-receipts/raw-observations-base64.json').read_text())
def blob(p): return subprocess.check_output(['git','-C',str(r),'show',j['cand']+':'+p])
s=blob('SKILL.md').decode().split('\n')[1520:1540]
while s and not s[-1].strip(): s.pop()
print('candidate:',j['cand'])
print('section:',1521,1540,hashlib.sha256('\n'.join(s).encode()).hexdigest())
print('command copies equal:',j['commands']==c,'records:',len(c))
print('recorded expected exits match:',all(x['exit']==x['expected_exit'] for x in c if 'expected_exit' in x))
print('input hashes match:',sum(hashlib.sha256(blob(p)).hexdigest()==h for p,h in j['inputs'].items()),'of',len(j['inputs']))
ls=blob('corpus/SOURCES.md').decode().splitlines()
print('SOURCES:503:',ls[502])
print('S265 lines:',[i for i,l in enumerate(ls,1) if l.startswith('| S265 |')])
print('retained command names:',','.join(x['name'] for x in c))
print('raw groups:',','.join(a))
for n,fs in a.items():
 t=base64.b64decode(fs['command.txt'],validate=True).decode()
 print(n,'command metadata keys:',','.join(l.split('=',1)[0] for l in t.splitlines()))
PY
```

Observed output (metadata rows identical for all six groups):

```text
candidate: adf87899c70d616140a81185a8f9acbbdfb30392
section: 1521 1540 3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831
command copies equal: True records: 12
recorded expected exits match: True
input hashes match: 4 of 4
SOURCES:503: - Next unused id: S161.
S265 lines: [140]
All six raw command metadata key sets: tool,tool-sha256,interpreter,python,cwd,runs,argv
```

Retained command names: frozen-sectionizer, recipe-match, baseline-nonzero, command-unavailable, selftest, frozen-match, frozen-mismatch, mismatch-stdout, mismatch-stderr, mismatch-exit, source-pointer, existing-output-refusal.

## Residual risk and verification gaps

- No candidate gate, test, build, frozen counter or runtime replay executed. Historical outputs are retained claims, not freshly authenticated executions.
- Only six direct-command raw observation groups retained; selftest and frozen snapshots have textual command outputs, not per-case raw observations in this bundle.
- No independent cleanup or lane non-mutation receipt retained in this bundle.
- LSP device unavailable: read xd://lsp returned No such tool; documentary analysis is not semantic caller/definition proof.
- No whole-monitor 64/64 or candidate-integration verification; resume/rerouting/runtime uniqueness outside assigned section.

No candidate execution, exploits, credentials, external targets, tests/builds, clone/commit, production edits, installations or delegation. Only this seat’s two d4 reports written. Recommendation only; current integration remains UNVERIFIED.

## Self-evaluation

Accuracy 4/5: retained consistency is separated from execution provenance; authenticity cannot be established here. Completeness 4/5: all assigned artifacts and hashes compared; historical execution state is not recoverable from this bundle. Clarity 4/5: findings and bounds explicit, with a lengthy reproducible command. Actionability 4/5: names missing revision receipt without authorizing a rerun. Conciseness 4/5: reproduction block adds necessary evidence length. Overall 4.0/5; user agreement expected within the documentary-only scope.
