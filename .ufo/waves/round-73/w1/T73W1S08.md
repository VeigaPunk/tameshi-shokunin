# T73W1S08 — independent committed-byte facts

Axes: calibration and re-derivation. Recommendation only; TameshiR73 retains judgment.

## Findings (severity first)

No disagreement with the six rows' expected **fact-comparison statuses**. Two standing red findings are independently reproduced:

1. **Report-count drift:** fleet `.ufo/reports/round-72/tameshi.md:56` at `3664a6d30051410c3d2bb8c32926d13e284a5118` prints `11 reports`; lane `.ufo/waves/round-72/w1` at `a3dd35742eee608d1205843dacebc461b4242b9e` contains twelve top-level Markdown blobs.
2. **Role drift:** `plans/round-72.plan.md:132-133` at the lane revision declares one `labrat`; `.ufo/waves/round-72/w1-results.json` has `{"name": "T72W1S11", "agent": "revenger", "note": null}` (identity-field excerpt of the actual results record). The spec independently assigns that seat `revenger`. No executed record has agent `labrat`.

### Spot-check evidence

The committed plan says exactly:

```text
132:- Wave `w1`: 12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,
133:  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.
```

The committed result identity excerpt is:

```json
{"name": "T72W1S11", "agent": "revenger", "note": null}
```

The full record also contains an `output` string; that string was not interpreted as evidence of successful execution. The finding is about committed recorded agents, not independent observation of runtime activity.

## Method and limits

Only `git show` and `git ls-tree` committed objects supply the population facts; no lane instrument was imported or executed. Python's standard-library JSON decoder, Counter, and byte operations perform the independent census. Named attacks are exactly reviewer, critic, mutation-tester, labrat (not revenger). Top-level counts do not include nested Markdown files. The manifest is also read from a committed object; its observed commit appears below.

LSP device discovery (`read xd://lsp`) returned `No such tool: xd://lsp`; semantic caller/definition/diagnostic queries were unavailable. This is a data census, not a semantic code review; no grep output is offered as semantic proof. Tool installation: none. No fixtures or Git mutations were needed.

Initial command (both requested revisions exist; the moving origin/master has advanced, so all facts remain pinned to the assigned revision):

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r73/T73W1S08 && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -t a3dd35742eee608d1205843dacebc461b4242b9e && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse origin/master && git -C /home/vgpnk/Projects/shokunin cat-file -t 3664a6d30051410c3d2bb8c32926d13e284a5118
```

```text
commit
17cd19396b36d4c15f1bce1bbdb7c42346f1df76
commit
```

Exit 0.

## Re-runnable commands and pasted outputs

### (a,c) Results counts and executed-agent multiset

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
d=json.loads(blob(L,R,'"'"'.ufo/waves/round-72/w1-results.json'"'"'))
print('"'"'seats='"'"'+str(d['"'"'seats'"'"']))
print('"'"'records='"'"'+str(len(d['"'"'results'"'"'])))
print('"'"'agents='"'"'+json.dumps(dict(sorted(collections.Counter(x['"'"'agent'"'"'] for x in d['"'"'results'"'"']).items()))))
for x in d['"'"'results'"'"']: print(x['"'"'name'"'"']+'"'"' '"'"'+x['"'"'agent'"'"'])
print('"'"'revenger_record_identity='"'"'+json.dumps([{k:x[k] for k in ['"'"'name'"'"','"'"'agent'"'"','"'"'note'"'"']} for x in d['"'"'results'"'"'] if x['"'"'agent'"'"']=='"'"'revenger'"'"']))'
```

```text
seats=12
records=12
agents={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
T72W1S01 executor
T72W1S02 executor
T72W1S03 executor
T72W1S04 scribe
T72W1S05 scribe
T72W1S06 scout
T72W1S07 reviewer
T72W1S08 critic
T72W1S09 mutation-tester
T72W1S10 sentinel
T72W1S11 revenger
T72W1S12 connector
revenger_record_identity=[{"name": "T72W1S11", "agent": "revenger", "note": null}]
```

Exit 0.

### (b) Top-level committed Markdown report files

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
b=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',L,'"'"'ls-tree'"'"','"'"'-z'"'"',R+'"'"':.ufo/waves/round-72/w1'"'"'])
a=[x.split(b'"'"'\t'"'"',1) for x in b.split(b'"'"'\0'"'"') if x]
names=[name.decode() for meta,name in a if meta.split()[1]==b'"'"'blob'"'"' and name.endswith(b'"'"'.md'"'"')]
print('"'"'\n'"'"'.join(names));print('"'"'top_level_md='"'"'+str(len(names)))'
```

```text
T72W1S01.md
T72W1S02.md
T72W1S03.md
T72W1S04.md
T72W1S05.md
T72W1S06.md
T72W1S07.md
T72W1S08.md
T72W1S09.md
T72W1S10.md
T72W1S11.md
T72W1S12.md
top_level_md=12
```

Exit 0.

### (d) Spec role multiset

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
d=json.loads(blob(L,R,'"'"'.ufo/waves/round-72/w1-spec.json'"'"'))
print('"'"'items='"'"'+str(len(d['"'"'items'"'"'])))
print('"'"'roles='"'"'+json.dumps(dict(sorted(collections.Counter(x['"'"'role'"'"'] for x in d['"'"'items'"'"']).items()))))
for x in d['"'"'items'"'"']: print(x['"'"'name'"'"']+'"'"' '"'"'+x['"'"'role'"'"'])'
```

```text
items=12
roles={"connector": 1, "critic": 1, "executor": 3, "mutation-tester": 1, "revenger": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
T72W1S01 executor
T72W1S02 executor
T72W1S03 executor
T72W1S04 scribe
T72W1S05 scribe
T72W1S06 scout
T72W1S07 reviewer
T72W1S08 critic
T72W1S09 mutation-tester
T72W1S10 sentinel
T72W1S11 revenger
T72W1S12 connector
```

Exit 0.

### (e) Frozen plan role declaration and seat span

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
b=blob(L,R,'"'"'plans/round-72.plan.md'"'"');lines=b.decode().splitlines()
for i in [132,133]: print(str(i)+'"'"':'"'"'+lines[i-1])
s='"'"'\n'"'"'.join(lines[131:133]);roles={role:int(n) for n,role in re.findall(r'"'"'(\d+) (executor|scribe|scout|connector|reviewer|critic|mutation-tester|sentinel|labrat)\b'"'"',s)}
print('"'"'roles='"'"'+json.dumps(dict(sorted(roles.items()))));print('"'"'role_sum='"'"'+str(sum(roles.values())))
span=b'"'"'**one v1 wave, 12 seats**'"'"';print('"'"'seat_span_occurrences='"'"'+str(b.count(span)))'
```

```text
132:- Wave `w1`: 12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,
133:  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.
roles={"connector": 1, "critic": 1, "executor": 3, "labrat": 1, "mutation-tester": 1, "reviewer": 1, "scout": 1, "scribe": 2, "sentinel": 1}
role_sum=12
seat_span_occurrences=1
```

Exit 0.

### (f) Attack share under manifest named set

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
d=json.loads(blob(L,R,'"'"'.ufo/waves/round-72/w1-results.json'"'"'));c=collections.Counter(x['"'"'agent'"'"'] for x in d['"'"'results'"'"']);named=['"'"'reviewer'"'"','"'"'critic'"'"','"'"'mutation-tester'"'"','"'"'labrat'"'"'];n=sum(c[r] for r in named);total=len(d['"'"'results'"'"'])
print('"'"'named='"'"'+json.dumps({r:c[r] for r in named}));print(f'"'"'attack_share={n}/{total}={100*n/total:g}%'"'"');print('"'"'floor=25%'"'"');print('"'"'at_or_above_floor='"'"'+str(n*100>=25*total))'
```

```text
named={"reviewer": 1, "critic": 1, "mutation-tester": 1, "labrat": 0}
attack_share=3/12=25%
floor=25%
at_or_above_floor=True
```

Exit 0.

### (g) Report exact span bytes

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
b=blob(F,FR,'"'"'.ufo/reports/round-72/tameshi.md'"'"');span=b'"'"'12 seats, 11 reports'"'"';i=b.index(span)
print('"'"'occurrences='"'"'+str(b.count(span)));print('"'"'byte_offset_zero_based='"'"'+str(i));print('"'"'byte_length='"'"'+str(len(span)));print('"'"'repr='"'"'+repr(b[i:i+len(span)]));print('"'"'hex='"'"'+span.hex('"'"' '"'"'));print('"'"'line_number='"'"'+str(b[:i].count(b'"'"'\n'"'"')+1));print('"'"'line='"'"'+next(x for x in b.decode().splitlines() if span.decode() in x))'
```

```text
occurrences=1
byte_offset_zero_based=3618
byte_length=20
repr=b'12 seats, 11 reports'
hex=31 32 20 73 65 61 74 73 2c 20 31 31 20 72 65 70 6f 72 74 73
line_number=56
line=- **The wave** (see "Wave" below): 12 seats, 11 reports; three seats found real
```

Exit 0.

### Committed manifest identity and row expectations

```sh
python3 -I -X utf8 -c 'import subprocess,json,collections,re
L='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'
F='"'"'/home/vgpnk/Projects/shokunin'"'"'
R='"'"'a3dd35742eee608d1205843dacebc461b4242b9e'"'"'
FR='"'"'3664a6d30051410c3d2bb8c32926d13e284a5118'"'"'
def blob(repo,rev,path): return subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',repo,'"'"'show'"'"',rev+'"'"':'"'"'+path])
h=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',L,'"'"'rev-parse'"'"','"'"'HEAD'"'"']).decode().strip();print('"'"'manifest_commit='"'"'+h);m=json.loads(blob(L,h,'"'"'tools/wave-reconcile.json'"'"'));print('"'"'schema='"'"'+m['"'"'schema'"'"']);print('"'"'rows='"'"'+str(len(m['"'"'rows'"'"'])))
for row in m['"'"'rows'"'"']:
 rec=row['"'"'record'"'"'];repo=F if rec['"'"'root'"'"']=='"'"'fleet'"'"' else L;b=blob(repo,rec['"'"'rev'"'"'],rec['"'"'path'"'"']);print(row['"'"'id'"'"']+'"'"' kind='"'"'+row['"'"'kind'"'"']+'"'"' expect='"'"'+row['"'"'expect'"'"']+'"'"' record_span_occurrences='"'"'+str(b.count(rec['"'"'span'"'"'].encode())))
 if '"'"'declaration'"'"' in row:
  d=row['"'"'declaration'"'"'];print('"'"'declaration_form='"'"'+d['"'"'form'"'"'])
  if d['"'"'form'"'"']=='"'"'text-tokens'"'"': print('"'"'declaration_span_occurrences='"'"'+str(blob(L,d['"'"'rev'"'"'],d['"'"'path'"'"']).count(d['"'"'span'"'"'].encode())))'
```

```text
manifest_commit=2e89e539770bc9f2ab8728233cad86f808399a22
schema=tameshi-wave-reconcile-v1
rows=6
r72-report-seats kind=seats expect=meet record_span_occurrences=1
r72-report-seatreports kind=seat_reports expect=drift record_span_occurrences=1
r72-plan-seats kind=seats expect=meet record_span_occurrences=1
r72-spec-roles kind=roles expect=meet record_span_occurrences=1
declaration_form=spec-items
r72-plan-roles kind=roles expect=drift record_span_occurrences=1
declaration_form=text-tokens
declaration_span_occurrences=1
r72-attack-share kind=attack_share expect=meet record_span_occurrences=1
```

Exit 0.

## Per-row closure from the facts alone

| Row | Independently derived fact comparison | Fact status | Manifest expect | Agreement |
|---|---|---|---|---|
| r72-report-seats | Report 12 = results.seats 12 = records 12 | meet | meet | yes |
| r72-report-seatreports | Report 11 ≠ top-level Markdown reports 12 | drift | drift | yes |
| r72-plan-seats | Plan 12 = results.seats 12 = records 12 | meet | meet | yes |
| r72-spec-roles | Spec roles equal executed agents in every multiplicity | meet | meet | yes |
| r72-plan-roles | Plan labrat 1/revenger 0 ≠ executed labrat 0/revenger 1; every other multiplicity agrees | drift | drift | yes |
| r72-attack-share | reviewer 1 + critic 1 + mutation-tester 1 + labrat 0 = 3; 3/12 = 25%, at floor | meet | meet | yes |

Report span exact bytes: `b'12 seats, 11 reports'`, 20 ASCII/UTF-8 bytes, hex `31 32 20 73 65 61 74 73 2c 20 31 31 20 72 65 70 6f 72 74 73`; unique occurrence at zero-based byte offset 3618, line 56.

## Residual risk and verification gaps

These are independent fact-comparison recommendations, not an implementation verdict. No selftest, manifest sweep, C2 battery, mutation control, resume path or runtime routing check was run; none is claimed passed. This seat does not establish that the reconciler implements the frozen binding/error rules. A literal record-span occurrence was checked independently for all six committed rows. The committed agent records prove the recorded wave composition, not external runtime execution.

## Cleanup

```sh
rmdir /fast/scratch/hyaku/tameshi-r73/T73W1S08 && printf 'SCRATCH_REMOVED /fast/scratch/hyaku/tameshi-r73/T73W1S08\n'
```

```text
SCRATCH_REMOVED /fast/scratch/hyaku/tameshi-r73/T73W1S08
```

Exit 0. The scratch directory is deleted; no scratch files remain.

## Self-evaluation

Accuracy 4/5: direct committed bytes and exact numeric/byte outputs; runtime behavior deliberately unverified. Completeness 5/5: (a)–(g), spot-check identities, and six-row status table included. Clarity 4/5: executable shell quoting is verbose; facts and comparison table are separated. Actionability 5/5: pinned artifact revisions and rerunnable independent commands included. Conciseness 4/5: command preludes repeat to make each fact independently reproducible. Overall 4.4/5. Highest-impact improvement for a future implementation-review assignment: pair this census with instrument/error-path evidence, without confusing the two. Self-check: the user should agree that this meets the independent-facts scope rather than granting admission.

AGREE rows=6/6
