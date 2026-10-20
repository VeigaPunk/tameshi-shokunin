# R01 — round-16 debts: inventory and end-of-round acceptance checklist

Seat: `TameshiR17.R01R16Debts` (reviewer, wave 1). Date 2026-10-20.
Baseline read: `98bea7da5801f4bc58e4187690ee1687c8a5061f` (lane tip at dispatch:
round-16 lesson `017a2b0` + non-author spotcheck `98bea7d`).

Sources of record:
- `corpus/lessons/round-16-verifier-spotcheck.md` §2, §3, §5, §6, §7.
- `corpus/lessons/round-16.md` §Gate G11, §Mistakes, §Process disclosures
  (`:94`, `:99-104`).

Method: committed bytes read only with `git show 98bea7d:<path>`; read-only
lane commands executed from the lane root; scratch under `/tmp` only. This
report is the only lane write. Tags: **[OBSERVED]** = I ran it at `98bea7d`;
**[READ]** = committed bytes; **[INFERENCE]** = contract-derived, not run
because the tool/manifest does not exist at `98bea7d`.

## 1. Inventory — every routed defect and every lesson-named open debt

| # | ID | Class | Source | Obligation |
|---|---|---|---|---|
| 1 | R16-OP1 | routed, blocking (spotcheck §3, §6.1) | live-tree `evidence-disposition.py` returns 2 at HEAD | restore clean-capable live-tree verdict without touching round-13/14 bytes; ship red-before and green-after |
| 2 | R16-C2a | routed (§6.2) | SKILL.md:1581-1586 recipe steps 2-3 pre-round outcomes | correct them (or mark historical with the working invocation), sweep every mention, re-read the bucket at the new sha with a fresh seat |
| 3 | R16-C2b | routed (§2 "Why C2 still fails", §6.3) | cold-read credit is sha-only | make credit input-keyed: record the inputs each executing entry ran against; re-verify their blobs at the measured rev; red-before on the round-14 bucket |
| 4 | R16-C2c | routed (§2, §6.4) | SHONEN box-3 overclaims "every bucket … wrong expectations repaired" | correct by append, never by rewriting evidence; point box 3 at the round-17 ledger |
| 5 | R16-EV1 | routed (§2 minor defect, §6.5) | `.ufo/evidence/round-16/round-gate/runner-sha256.txt` still reads `89722ddb…` | append a dated correction; do not rewrite the file |
| 6 | R16-MON1 | routed (§6.6) | ToolsNoHarm ran selftests only | monitor registered entry commands (`--root .` forms) so a live-tree verdict change is caught inside the round |
| 7 | D1 | lesson "Open debt, named" (`round-16.md:99`) | six older ledger legs inherit the suite environment; only `js-round-gate` is scrubbed (MistakeAudit O7) | scrub all seven leg suites, or name the residual explicitly |
| 8 | D2 | lesson "Open debt, named" (`:100-101`) | round-7 section's `tools/mutate-and-run.sh:<line>` anchors predate the tool's growth | re-anchor or mark historical |
| 9 | D3 | lesson "Open debt, named" (`:101-103`) | cold-read contract left "page-named but never-open" files to each seat's judgement; ContamA/ContamB show a 2–2 split | state one precedence rule for page-named files; apply it in the round-17 cold-read |
| 10 | D4 | lesson "Process disclosures" RX9 (`:105-109`) | "line count of every edited section unchanged" is one section short (`### Round-15 gate/probe registry` gained a trailing blank line) | append the correction; anchors unaffected |
| 11 | D5 | lesson "Process disclosures" (`:92-94`) | round-15 `verification-3.json` pins runner `75ed934d…` and SHONEN `3b1dc526…`; round 15's receipt is not re-claimed green at this HEAD | keep the receipt historical and say so with current digests, or re-pin without rewriting |
| 12 | D6 | lesson Mistake row (`round-16.md:56`) | "The same misattribution sits in `verification.json` (round-15 attempt 1) and is named here, not corrected" | append a correction naming the two rows and the repaired id |
| 13 | D7 | lesson Gate G11 (`round-16.md:28`) | `bwrap` confinement "is next-round work"; note §6 records that a hostile mutant can write outside its directory | land confinement or re-name it with an owner and a date |

Items 7–9 are the lesson's single "Open debt, named:" sentence; 10 is the RX9
residual; 11–12 are the two process disclosures; 13 is the G11 deferral. No
other debt language exists in `round-16.md` (grep for
`open debt|debt|deferred|next[- ]round|not re-claimed|unresolved`).

**Wave-discovered additions (not named by the round-16 lesson; they belong to
MON1's own acceptance).**
- **X1 — the runner selftest moves the caller's HEAD under an exported
  `GIT_DIR` (observed, critical).** In a throwaway clone,
  `GIT_DIR="$PWD/.git" bash tools/mutate-and-run.sh --selftest` exits 0
  (`VERDICT: PASS`) and moves HEAD `98bea7d → 7c8bbc0` through three
  `selftest-fixture*` commits in 5 s. The fixture commits are
  `tools/mutate-and-run.sh:1532/1590/1625` (`git -C "$grepo" -c
  user.email=tameshi@selftest commit`); `GIT_DIR` overrides `-C`. The live
  lane suffered the same chain at 12:29:33 (`98bea7d → f8832ef → 0559c60 →
  e16adb7`, author `tameshi <tameshi@selftest>`); the L1 restored HEAD to
  `98bea7d` with the reflog message "restore HEAD after R04 seat fixture
  commits (GIT_DIR leak)". The live registry has a `mutate-and-run-selftest`
  row, and `registry-check.run_row` (`tools/registry-check.py:211-220`)
  passes the caller's environment unchanged, so the monitor reproduces this
  with `exit=0` and its `stdout_contains` satisfied — a pass while damaging
  the repo.
- **X2 — the registry's `verify-round15` row writes evidence (observed).**
  The row runs `.ufo/evidence/round-15/verify.py --rev 7650fe4…`, which is a
  create-only harness: it writes `verification-N.json` and `attempt-N/` under
  `.ufo/evidence/round-15/`. Observed `verification-5.json` + `attempt-5/`
  (12:36:46); an earlier `attempt-4` pair was also written, then removed.
  A no-harm monitor must not add evidence files on every run.

## 2. End-of-round checklist (primary deliverable)

Run from the lane root with `export BASE=98bea7da5801f4bc58e4187690ee1687c8a5061f`
and `export REV=<landing commit>`. The command bank is §3.

| # | ID | Pass at `REV` (one observable) | Red at `BASE` (observed/read) | Bank |
|---|---|---|---|---|
| 1 | OP1 | `--root .` on `.ufo/evidence/round-17/dispositions.json` → 0 clean, counts `12/11/1/11/0/0` (equal to the observed v1 run at `28aeef4`), `expected_inputs_historical={tools/mutate-and-run.sh}`; before manifest → 1 failed, counts `12/12/0/11/1/1`, `producer_before` unresolved; four negatives → 2 with their exact ids; v1 manifest still → 2; v1 selftest ≥34/34 | both round-14 live-tree runs → 2 `expected_input_digest_mismatch` (`tools/mutate-and-run.sh` observed `0673d2e5…` expects `75ed934d…`); **[OBSERVED]** | OP1-R1..R2, G1..G7 |
| 2 | C2a | the recipe's two commands, run as written, exit 1 (before) and 0 (after); every `--dispositions` mention in SKILL.md is consistent with its observed exit; the new section sha is credited with non-empty `inputs` | steps 2 and 3 both exit 2; the bucket is still credited by the old measure → 8/true; **[OBSERVED]** | C2a-R1, G1..G3 |
| 3 | C2b | `round-17/measure.py --rev REV` → 8, `box3_full_page` true, `sections_covered==sections_total`; a tampered ledger → `input-drift:<path>` + false; a deleted input → `input-missing:<path>` + false; selftest includes the drift-red case | old measure at `BASE` → 8, 54/54, true; v2 on the round-16 ledger → false with `inputs-unrecorded` on the round-14 heading; **[OBSERVED for old measure; INFERENCE for v2]** | C2b-R1..R3, G1..G4 |
| 4 | C2c | box-3 block contains the round-17 ledger path **and** an appended correction sentence; measure v2 reports `box3_ledger_link` and `box3_points` true | block links only the round-16 ledger and repeats the overclaim; v2 `box3_ledger_link` false (score 6); **[READ + INFERENCE]** | C2c-R1, G1 |
| 5 | EV1 | new bytes `startswith(old bytes)`; contain `0673d2e5…`; every rev named in the correction digests to `0673d2e5…` | first line `89722ddb…`; live runner `0673d2e5…`; **[OBSERVED]** | EV1-R1, G1 |
| 6 | MON1 | `registry-check --rev REV --registry tools/registry.json --json` → 0, `held=N/N`; same registry at `BASE` (or the round-14 fixture row) → 1, one `differs` with `expect=0 got=2`; selftest covers held/differs/invalid-registry/usage | `tools/registry.json` and `tools/registry-check.py` absent; the round-16 monitor could not see the exit-2 harm; **[OBSERVED absence]** | MON1-R1..R2, G1..G2 |
| 7 | D1 | `--regression` under the `BASH_ENV` canary leaves **no** marker; all seven legs PASS; one selftest case asserts the scrub | only `js-round-gate` is scrubbed (`grep -c 'env -i'` = 1; **[OBSERVED]**); the canary is inherited by the other six suites **[INFERENCE]** | D1-R1..R2, G1 |
| 8 | D2 | every round-7 runner anchor span contains its claim marker and starts at the claimed construct | 4 of 6 anchors fail (`:511-522`, `:733-791`, `:891-975`, `:927-944`); `:550-728` starts 49 lines before `regression_specs()`; **[OBSERVED]** | D2-R1, G1 |
| 9 | D3 | the round-17 cold-read contract states exactly one page-named precedence rule; the new ledger shows no 2–2 split on the `plans/` files the reports name (`round-2`, `-3`, `-5`, `-6`, `-7`, `-11`) | ContamA §"Rule conflict" (`w2/ContamA.md:126-138`): 2–2 split; no rule in SKILL.md; **[READ]** | D3-R1, G1 |
| 10 | D4 | an appended correction names `### Round-15 gate/probe registry` and the trailing blank line; anchor check at `REV` reports 0 `STALE-QUOTE` | SKILL.md:1718 claims every edited section kept its line count; the section is +1 line; **[READ]** | D4-R1, G1 |
| 11 | D5 | a round-17 record names the round-15 pins and the digests at `REV`, and marks the receipt historical; no registry row runs `verify.py`; round-15 bytes unchanged | pins `75ed934d…`/`3b1dc526…`; at `BASE` runner `0673d2e5…`, SHONEN `4a11ade5…`; **[OBSERVED]** | D5-R1, G1 |
| 12 | D6 | an appended correction names `usage-proof-new`/`gate-usage` with `recorded=context_consistent`, `rederived=usage_error`, verdict line and source sha `4d2fb03f…`; `verification.json` sha unchanged | both rows record `observed_id=context_consistent` at exit 64 while their stderr tail carries `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`; **[OBSERVED]** | D6-R1, G1 |
| 13 | D7 | if landed: an escape canary is blocked and the leg's table is unchanged; else the round record re-names G11 with owner and round | note §6: GuardAudit showed the write/network escape; confinement not in the runner; **[READ]** | D7-R1, G1 |
| 14 | X1 | in a throwaway clone, `GIT_DIR="$PWD/.git" bash tools/mutate-and-run.sh --selftest` leaves HEAD unchanged and no `selftest-fixture*` reflog entry; the selftest still exits 0 with its declared count (registry `stdout_contains` updated in lockstep with D1) | **[OBSERVED]** clone `98bea7d → 7c8bbc0`, rc 0, `VERDICT: PASS`; live lane reflog `98bea7d → f8832ef → 0559c60 → e16adb7`, L1-restored | X1-R1, G1 |
| 15 | X2 | two consecutive `registry-check --only verify-round15` runs in a clone add **no** file under `.ufo/evidence/round-15/`; the row is removed or marked historical | **[OBSERVED]** `verification-5.json` + `attempt-5/` (12:36:46), earlier `attempt-4` pair also written | X2-R1, G1 |

## 3. Command bank

### OP1 — live-tree disposition gate

R1 (red-before, run at `BASE`; both **[OBSERVED]**):
```sh
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-14/dispositions.json --json >/tmp/op1-base.json; echo exit=$?
# exit=2 .error.kind=expected_input_digest_mismatch
# message: tools/mutate-and-run.sh observed 0673d2e5… expects 75ed934d…
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-14/dispositions-before.json --json >/tmp/op1-base-before.json; echo exit=$?
# exit=2 same id — NOT the recipe's expected 1 (this was [INFERENCE] in the spotcheck; executed here)
```

G1 (green, after manifest; **[INFERENCE]** until landed). The expected counts
are calibrated by running the v1 manifests at their matching root
`28aeef4` (**[OBSERVED]**): clean `{'expected_checks':12,'effective':11,
'superseded':1,'passed':11,'failed':0,'findings':0}`; before
`{'expected_checks':12,'effective':12,'superseded':0,'passed':11,'failed':1,
'findings':1}`, `producer_before` outcome `fail`, mismatches
`['expected_contains_missing']`. The v2 manifests at `REV` must reproduce
those counts; only the `expected_inputs_historical` payload is new.
```sh
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-17/dispositions.json --json >/tmp/op1.json; echo exit=$?
python3 - <<'PY'
import json
d=json.load(open('/tmp/op1.json'))
assert d['status']=='clean' and d['exit']==0, d
assert d['counts']=={'expected_checks':12,'effective':11,'superseded':1,
                     'passed':11,'failed':0,'findings':0}, d['counts']
assert set(d['expected_inputs_historical'])=={'tools/mutate-and-run.sh'}, d.get('expected_inputs_historical')
print('OP1 GREEN', d['expected_inputs_historical'])
PY
```

G2 (before manifest; **[INFERENCE]**):
```sh
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-17/dispositions-before.json --json >/tmp/op1b.json; echo exit=$?   # 1
python3 - <<'PY'
import json
d=json.load(open('/tmp/op1b.json'))
assert d['status']=='failed' and d['counts']['failed']==1 and d['counts']['passed']==11, d['counts']
r=[x for x in d['rows'] if x['name']=='producer_before'][0]
assert r['outcome']=='fail' and r['state']=='effective', r
print('OP1 BEFORE RED OK', r['mismatches'])
PY
```

G3 (v1 unchanged; **[INFERENCE]** for the extended tool):
```sh
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-14/dispositions.json --json >/tmp/op1-v1.json; echo exit=$?
# still 2: a v1 manifest must not gain historical-input behaviour
python3 -c 'import json;d=json.load(open("/tmp/op1-v1.json"));assert d["id"]=="expected_input_digest_mismatch",d["id"]'
python3 tools/evidence-disposition.py --selftest | tail -1
# SELFTEST: PASS (>=34/34; the 34 v1 cases unchanged)
```

G4 (schema gating; **[INFERENCE]**): relabel the v2 manifest as v1 and confirm
`historical_inputs` is ignored:
```sh
python3 - <<'PY'
import json
d=json.load(open('.ufo/evidence/round-17/dispositions.json'))
d['schema']='evidence-dispositions-v1'
json.dump(d,open('/tmp/op1-v1-schema.json','w'),indent=2,sort_keys=True)
PY
python3 tools/evidence-disposition.py --root . --dispositions /tmp/op1-v1-schema.json --json >/dev/null; echo exit=$?
# 2 expected_input_digest_mismatch
```

G5 (v2 negatives; **[INFERENCE]**):
```sh
python3 - <<'PY'
import copy,json
d=json.load(open('.ufo/evidence/round-17/dispositions.json'))
f=copy.deepcopy(d); f['historical_inputs']={'.ufo/evidence/round-13/expected.json':{'rev':'0'*40,'reason':'x'}}
json.dump(f,open('/tmp/op1-forbidden.json','w'))
u=copy.deepcopy(d); u['historical_inputs']={'tools/nope.py':{'rev':'0'*40,'reason':'x'}}
json.dump(u,open('/tmp/op1-unknown.json','w'))
m=copy.deepcopy(d); m['historical_inputs']['tools/mutate-and-run.sh']['rev']='98bea7da5801f4bc58e4187690ee1687c8a5061f'
json.dump(m,open('/tmp/op1-mismatch.json','w'))
PY
for f in forbidden unknown mismatch; do
  python3 tools/evidence-disposition.py --root . --dispositions /tmp/op1-$f.json --json >/tmp/o.json 2>/dev/null
  echo "$f exit=$? id=$(python3 -c 'import json;print(json.load(open("/tmp/o.json"))["id"])')"
done
# forbidden exit=2 id=historical_input_forbidden
# unknown   exit=2 id=historical_input_unknown
# mismatch  exit=2 id=expected_input_digest_mismatch
```

G6 (identity/unavailable; **[INFERENCE]**):
```sh
# (a) root is a git subdirectory, not the toplevel -> identity guard
python3 tools/evidence-disposition.py --root tools \
  --dispositions "$PWD/.ufo/evidence/round-17/dispositions.json" --json; echo exit=$?   # 2 historical_input_unavailable
# (b) no git at root at all
tmp=$(mktemp -d); mkdir "$tmp/lane"; git archive "$REV" | tar -x -C "$tmp/lane"
(cd "$tmp/lane" && python3 tools/evidence-disposition.py --root . \
   --dispositions .ufo/evidence/round-17/dispositions.json --json); echo exit=$?      # 2 historical_input_unavailable
```
(a) also probes the repo-identity guard named in the interface contract: if it
returns `input_unreadable` instead, the guard is missing.

G7 (immutability; **[READ]** at `BASE`, re-run at `REV`):
```sh
git diff --name-status "$BASE" "$REV" -- .ufo/evidence/round-13 .ufo/evidence/round-14 \
  | grep -vE '^A' || true
# expected empty: no M/D/R under the historical evidence dirs
```
(The one permitted edit elsewhere is EV1's append to
`.ufo/evidence/round-16/round-gate/runner-sha256.txt`, checked separately.)

### C2a — stale round-14 recipe

R1 (red-before; **[OBSERVED]**):
`git show "$BASE:SKILL.md" | sed -n '1578,1587p'` shows steps 2–3 on the
round-14 manifests; both exit 2 (OP1-R1).

G1 (green; **[INFERENCE]** until the text lands). Extract and execute both
commands as written:
```sh
python3 - <<'PY'
import os,re,subprocess
rev=os.environ['REV']
t=subprocess.run(['git','show',rev+':SKILL.md'],capture_output=True,text=True,check=True).stdout
sec=t.split('## Effective expectation reconciliation — round 14',1)[1].split('\n## ',1)[0]
body='\n'.join(l for l in sec.split('\n') if not l.lstrip().startswith('|'))
cmds=re.findall(r'`(python3 tools/evidence-disposition\.py [^`]+--json)`',body)
assert cmds, 'no recipe command'
before=' '.join(cmds[0].split())
after=before.replace('dispositions-before.json','dispositions.json')
assert after!=before, 'step 2 must name the before manifest'
print('before:',before); print('after :',after)
exits=[subprocess.run(c,shell=True,cwd='.').returncode for c in (before,after)]
print('exits',exits)
assert exits==[1,0], exits
PY
```

G2 (sweep every mention; **[INFERENCE]**): list every executable mention and
compare it with its stated outcome:
```sh
python3 - <<'PY'
import os,re,subprocess
rev=os.environ['REV']
t=subprocess.run(['git','show',rev+':SKILL.md'],capture_output=True,text=True).stdout
for m in re.finditer(r'`(python3 tools/evidence-disposition\.py [^`]*--json)`',t):
    line=t[:m.start()].count('\n')+1
    cmd=' '.join(m.group(1).split())
    rc=subprocess.run(cmd,shell=True,capture_output=True,text=True).returncode
    print('SKILL:%d exit=%d | %s' % (line,rc,cmd[:110]))
PY
```
At `BASE` this prints 2 for `:1581` (recipe step 2, whose text states exit 1),
`:1601` (round-14 registry, whose verdict map states 0 clean) and `:1681`
(round-15 registry, whose text states 2 by design but whose live-tree entry
command is the failing form; its 0-clean path is the archived-root workaround).
At `REV`, the two recipe steps and the active registry row must point at
round-17 manifests (step 2 → 1, step 3/registry → 0); `:1601` may remain a
dated historical row only if it states the observed v1 exit 2.

G3 (bucket re-read; covered by measure in C2b): the current section sha
(`e8720037…` at `BASE`; it will change with the text) must have a v2 ledger
entry with `class=instruction`, `verdict=executed-ok|gap-minor`,
`commands_executed_count>0`, and non-empty `inputs`.

### C2b — input-keyed credit

R1 (old rule; **[OBSERVED]**):
```sh
python3 .ufo/evidence/round-16/measure.py --rev "$BASE" | python3 -c \
 'import json,sys;d=json.load(sys.stdin);print(d["calibration_restraint_score"],d["coldread"]["sections_covered"],d["coldread"]["sections_total"],d["coldread"]["box3_full_page"])'
# 8 54 54 True — credits the round-14 bucket whose two recipe commands exit 2 at the same rev
```

R2 (new rule on the old ledger; **[INFERENCE]**):
```sh
python3 .ufo/evidence/round-17/measure.py --rev "$BASE" \
  --ledger-file .ufo/evidence/round-16/coldread/ledger.json >/tmp/m2-old.json; echo exit=$?
python3 - <<'PY'
import json
d=json.load(open('/tmp/m2-old.json'))
assert d['coldread']['box3_full_page'] is False
m={x['heading']:x['reason'] for x in d['coldread']['missing']}
r=m.get('## Effective expectation reconciliation — round 14')
assert r=='inputs-unrecorded', (r,m)
print('C2b RED OK', r)
PY
```

R2b (drift red via `--inputs-overlay`; **[INFERENCE]**; the overlay file shape
is the L1's interface choice — the observable is the reason string). Overlay
the round-14 entry with the digest its commands actually ran against
(`tools/mutate-and-run.sh = 75ed934d…`). The live blob at `BASE` is
`0673d2e5…`, so measure v2 must report
`input-drift:tools/mutate-and-run.sh` and `box3_full_page=false`. This is the
spotcheck's exact red-before: sha-only credit kept the bucket; the input rule
uncredits it on drift.

R3: `python3 .ufo/evidence/round-17/measure.py --selftest` — must include the
drift-red case (recorded inputs match → credit; blob changed at the measured
rev → `input-drift:<path>` → no credit).

G1 (green; **[INFERENCE]** until landed):
```sh
python3 .ufo/evidence/round-17/measure.py --rev "$REV" >/tmp/m2.json; echo exit=$?   # process exit 0
python3 - <<'PY'
import json
d=json.load(open('/tmp/m2.json'))
assert d.get('exit', 0)==0
assert d['calibration_restraint_score']==8, d
c=d['coldread']; assert c['box3_full_page'] and c['sections_covered']==c['sections_total'], c
assert '## Effective expectation reconciliation — round 14' not in c['uncovered_headings']
print('C2b GREEN', c['sections_covered'],'/',c['sections_total'],'depth',d['depth_score'])
PY
```

G2 (real-data falsifier — tampered digest; **[INFERENCE]**):
```sh
python3 - <<'PY'
import json
d=json.load(open('.ufo/evidence/round-17/coldread/ledger.json'))
e=[x for x in d['entries'] if x.get('heading','').startswith('## Effective expectation reconciliation')][0]
k=sorted(e['inputs'])[0]; e['inputs'][k]='0'*64
json.dump(d,open('/tmp/ledger-drift.json','w'))
print('tampered',k)
PY
python3 .ufo/evidence/round-17/measure.py --rev "$REV" \
  --ledger-file /tmp/ledger-drift.json >/tmp/m2-drift.json; echo exit=$?
python3 - <<'PY'
import json
d=json.load(open('/tmp/m2-drift.json'))
m={x['heading']:x['reason'] for x in d['coldread']['missing']}
r=m['## Effective expectation reconciliation — round 14']
assert r.startswith('input-drift:'), r
assert d['coldread']['box3_full_page'] is False
print(r)
PY
# repeat with the key deleted -> input-missing:<path>
```

G3 (trace/assemble; **[INFERENCE]**):
```sh
python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest
python3 .ufo/evidence/round-17/coldread/assemble.py --selftest
python3 .ufo/evidence/round-17/coldread/trace-inputs.py --root . --cwd . \
  --out /tmp/trace-smoke.json -- python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-17/dispositions.json --json
python3 -c 'import json;d=json.load(open("/tmp/trace-smoke.json"));assert d["exit"]==0 and d["inputs"];print(len(d["inputs"]),"inputs")'
```

G4 (v1 no-regression): `depth_score` stays 7 and the `sources` census is
unchanged (`measure.py` v2 keeps the round-16 sectionizer, LEG_RE, SOURCE_ROW_RE).

### C2c — box-3 text

R1 (red; **[READ]** + **[INFERENCE]** for measure v2):
```sh
git show "$BASE:SHONEN.md" | sed -n '/^- \[~\] Instructions executable/,/^- \[~\] No cross-domain/p'
# links .ufo/evidence/round-16/coldread/ledger.json; claims every bucket repaired and re-read
python3 .ufo/evidence/round-17/measure.py --rev "$BASE" | python3 -c \
 'import json,sys;d=json.load(sys.stdin);print(d["shonen"]["box3_ledger_link"],d["calibration_restraint_score"])'
# False 6
```

G1 (green; **[INFERENCE]**):
```sh
git show "$REV:SHONEN.md" | sed -n '/^- \[~\] Instructions executable/,/^- \[~\] No cross-domain/p' >/tmp/box3.txt
grep -q '.ufo/evidence/round-17/coldread/ledger.json' /tmp/box3.txt
grep -q 'input-keyed' /tmp/box3.txt
grep -qE 'superseded|corrected' /tmp/box3.txt
python3 .ufo/evidence/round-17/measure.py --rev "$REV" | python3 -c \
 'import json,sys;d=json.load(sys.stdin);assert d["shonen"]["box3_ledger_link"] and d["shonen"]["box3_points"] and d["calibration_restraint_score"]==8'
```
The grep is the mechanical floor; the human read must confirm the round-16
claim is scoped/superseded, not repeated as current. Appending is the method
(the old sentence stays; the correction follows it).

### EV1 — stale runner receipt

R1 (red; **[OBSERVED]**):
```sh
git show "$BASE:.ufo/evidence/round-16/round-gate/runner-sha256.txt" | head -1   # 89722ddb… (c699c8c runner)
git show "$BASE:tools/mutate-and-run.sh" | sha256sum                             # 0673d2e5…
git show c699c8c:tools/mutate-and-run.sh | sha256sum                             # 89722ddb…
```

G1 (green; prefix + claim):
```sh
git show "$BASE:.ufo/evidence/round-16/round-gate/runner-sha256.txt" >/tmp/old-sha.txt
git show "$REV:.ufo/evidence/round-16/round-gate/runner-sha256.txt" >/tmp/new-sha.txt
python3 -c 'assert open("/tmp/new-sha.txt","rb").read().startswith(open("/tmp/old-sha.txt","rb").read())'
grep -q '^0673d2e5' /tmp/new-sha.txt
for r in 05a2247 09ee1d0 017a2b0 98bea7da5801f4bc58e4187690ee1687c8a5061f "$REV"; do
  git show "$r:tools/mutate-and-run.sh" | sha256sum; done
# every listed rev 0673d2e5…; the four named in the correction are
# 05a2247, 09ee1d0, 017a2b0, 98bea7d (all four verified at BASE)
```
The live worktree already carries the append; the check is at `REV`, and the
prefix assertion is the "do not rewrite" proof.

### MON1 — entry-command monitor

R1 (red; **[OBSERVED]**): `test -e tools/registry.json` → 1;
`test -e tools/registry-check.py` → 1. The round-16 monitor ran selftests only,
so the OP1 exit-2 change was invisible.

R2 (harm visibility; **[INFERENCE]**):
```sh
cat > /tmp/r14-row.json <<'JSON'
{"schema":"tameshi-entry-registry-v1","rows":[
 {"name":"effective-expectation-disposition","kind":"gate",
  "argv":["python3","tools/evidence-disposition.py","--root",".",
          "--dispositions",".ufo/evidence/round-14/dispositions.json","--json"],
  "expect":{"exit":0},"timeout_s":120,
  "source":"SKILL.md round-15 gate registry","status":"active"}]}
JSON
python3 tools/registry-check.py --rev "$BASE" --registry /tmp/r14-row.json --json >/tmp/mon1.json
echo exit=$?    # 1
# ROW effective-expectation-disposition expect=0 got=2 differs
# REGISTRY_CHECK: held=0/1
```

G1 (green; **[INFERENCE]**):
```sh
python3 tools/registry-check.py --rev "$REV" --registry tools/registry.json --json >/tmp/mon.json; echo exit=$?
python3 tools/registry-check.py --rev "$REV" | tail -1        # REGISTRY_CHECK: held=N/N
python3 tools/registry-check.py --registry tools/registry.json | tail -1   # live tree, same
python3 - <<'PY'
import json
d=json.load(open('/tmp/mon.json'))
print({k:d[k] for k in ('held','total') if k in d})
PY
```
Minimum row set: the two active gates — `tools/context-capture.py --check`
(`--json` → exit 0, `id=context_consistent`; **[OBSERVED]** at `BASE`, selftest
49/49) and the round-17 disposition gate (G1). Selftest/`--only`/usage:
```sh
python3 tools/registry-check.py --selftest; echo exit=$?                    # 0
python3 tools/registry-check.py --bogus; echo exit=$?                       # 64
python3 tools/registry-check.py --rev deadbeef --registry tools/registry.json; echo exit=$?   # 2
python3 tools/registry-check.py --only effective-expectation-disposition --rev "$REV"   # one ROW, exit 0
```

### X1/X2 — monitor rows must be observation-only

X1-R1 (red; **[OBSERVED]**, in a throwaway clone — never the lane):
```sh
W=$(mktemp -d /tmp/tameshi-r17w1-R01R16Debts-XXXXXX); mkdir -p "$W/fleet"
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" "$W/fleet/"; done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$W/fleet/tameshi-shokunin"
cd "$W/fleet/tameshi-shokunin"
before=$(git rev-parse HEAD)
GIT_DIR="$PWD/.git" bash tools/mutate-and-run.sh --selftest >/tmp/x1.out 2>&1; echo rc=$?
after=$(git rev-parse HEAD)
echo "before=$before after=$after"; git reflog -4 --format='%h %gs'
# BASE (observed): rc=0, after=7c8bbc0 != before=98bea7d,
# reflog: selftest-fixture{,-exec,-noexec}; tail -1 = VERDICT: PASS
```

X1-G1 (green): the same command leaves `before == after` and the reflog has no
`selftest-fixture*` entry; the selftest keeps its count. Fix in the runner
(scrub `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/
`GIT_ALTERNATE_OBJECT_DIRECTORIES` around the fixture `git` calls) and, for
defence in depth, in `registry-check.run_row` (a scrubbed child env), since the
monitor must not depend on the caller's shell.

X2-R1 (red; use a clone, not the lane):
```sh
cd "$W/fleet/tameshi-shokunin"
n0=$(git status --porcelain --untracked-files=all | grep -c '^?? .ufo/evidence/round-15/' || true)
python3 tools/registry-check.py --only verify-round15 --registry tools/registry.json >/tmp/x2.out 2>&1
n1=$(git status --porcelain --untracked-files=all | grep -c '^?? .ufo/evidence/round-15/' || true)
echo "before=$n0 after=$n1"; tail -2 /tmp/x2.out
# BASE (observed in the live lane): a new verification-N.json + attempt-N/ appears (attempt-5 at 12:36:46)
```

X2-G1 (green): `n1 == n0` and no new file under `.ufo/evidence/round-15/`
after two consecutive runs. The row is either removed from the registry, marked
`status: historical`, or replaced by a read-only replay (the retained-receipt
gate is the read-only instrument; `verify.py` is the harness that writes).

Cross-item: D1's new selftest case changes
`MUTATE_SELFTEST: 83/83 pass`; the registry row's `stdout_contains` must be
updated in the same landing, otherwise MON1's own counting command drops a row.

### D1 — six older legs inherit the environment

R1 (static; **[OBSERVED]**):
```sh
git show "$BASE:tools/mutate-and-run.sh" | grep -c 'env -i'   # 1 (js-round-gate only)
```
`regression_case()` runs `timeout "$TIMEOUT_S" bash -c "$SUITE"` with the
inherited environment; only the js-round-gate suite string wraps its target in
`exec env -i` (`tools/mutate-and-run.sh:402`, `:1222` at `BASE`).

R2 (dynamic canary; **[INFERENCE]** — not executed, full regression):
```sh
printf 'echo POISON >> /tmp/r01-marker.log\n' > /tmp/r01-poison.sh
rm -f /tmp/r01-marker.log
BASH_ENV=/tmp/r01-poison.sh bash tools/mutate-and-run.sh --regression \
  --workdir /tmp/r01-reg >/tmp/r01-reg.out 2>&1; echo rc=$?
grep -c POISON /tmp/r01-marker.log    # BASE: >0 (the suite's bash sources BASH_ENV)
tail -1 /tmp/r01-reg.out              # REGRESSION: PASS (...)
```

G1: same command → marker absent (count 0), all seven legs PASS, and one
selftest case asserts the scrub. The fix may scrub the suite invocation
(`env -i bash -c "$SUITE"` with PATH/HOME/TMPDIR) or each target; the canary is
the acceptance, not the literal `env -i` count.

### D2 — round-7 runner anchors

R1 (red; **[OBSERVED]**):
```sh
python3 - <<'PY'
import os,subprocess
lines=subprocess.run(['git','show',os.environ['BASE']+':tools/mutate-and-run.sh'],
                     capture_output=True,text=True).stdout.split('\n')
claims=[(72,109,'--regression'),(72,109,'ledger'),(511,522,'PIN_JS='),
        (733,791,'regression_case'),(891,975,'Exit map (--regression)'),
        (927,944,'regression_case_git'),(927,944,'run_regression')]
for a,b,m in claims:
    print(a,b,m,any(m in l for l in lines[a-1:b]))
print('line 550:',lines[549])
PY
# 511-522 PIN_JS= False; 733-791 regression_case False; 891-975 exit map False;
# 927-944 both False; 550 is a leg comment, not `regression_specs() {` (that is :599)
```

G1 (green): the same markers all True, and each span's first line is the
claimed construct: pins `:529-568` (`PIN_JS=` at 551, ends `FLEET_ROOT=''`),
specs starting at `regression_specs() {` (`:599-970`),
`regression_case()` (`:971-1137`), `run_regression()` (`:1151-1240`), exit map
at `:121-122`. If the section is
marked historical instead, the marker test is replaced by an explicit dated
note and the anchors removed from present-tense claims.

### D3 — page-named never-open rule

R1 (red; **[READ]**): `ContamA.md:126-138` records the 2–2 split on
`plans/round-3.plan.md`, `round-5`, `round-7`, `round-11`; `git show
"$BASE:SKILL.md" | grep -c 'page-named'` → 0.

G1 (green; **[INFERENCE]**): the round-17 cold-read contract (the L1-owned
dispatch/spec text) contains exactly one directive, e.g. "page-named files are
read targets and must be listed in `opened`" or "page-named files are not read
targets; record a minor gap naming the rule". Acceptance: the directive exists
once; for each `plans/` file named in ContamA/ContamB (`round-2`, `-3`, `-5`,
`-6`, `-7`, `-11`), all v2 reports for the sections that name it agree (file in
`opened`, or a rule-citing gap — not both across replicas).

### D4 — RX9 line-count claim

R1 (red; **[READ]**): `SKILL.md:1718` says "the line count of every edited
section unchanged"; `### Round-15 gate/probe registry` gained one trailing
blank line when the round-16 sections were appended (RX9), so the statement is
one section short. Anchors are unaffected.

G1: an appended correction (round-17 errata) names that section and the
trailing blank line; the anchor check at `REV` reports 0 `STALE-QUOTE` and
every `SKILL.md:<n>` self-anchor resolves. Mechanical floor:
```sh
git show "$REV:SKILL.md" | grep -n "Round-15 gate/probe registry"
git show "$REV:SKILL.md" | grep -n "trailing blank line"
```

### D5 — round-15 receipt pin drift

R1 (red; **[OBSERVED]**):
```sh
git show "$BASE:.ufo/evidence/round-15/verification-3.json" | \
  python3 -c 'import json,sys;d=json.load(sys.stdin);print([c for c in d["checks"] if c["name"] in ("integrity-tools/mutate-and-run.sh","integrity-SHONEN.md")])'
# baseline=rev: runner 75ed934d…, SHONEN 3b1dc526…
git show "$BASE:tools/mutate-and-run.sh" | sha256sum   # 0673d2e5…
git show "$BASE:SHONEN.md" | sha256sum                # 4a11ade5…
```

G1: a round-17 record (e.g. `.ufo/evidence/round-17/round15-pin-drift.json`)
names the round-15 pins and the current digests, marks the receipt historical
at its baseline, and no active registry row runs `verify.py`/`verification-3.json`:
```sh
git diff --name-status "$BASE" "$REV" -- .ufo/evidence/round-15   # empty
python3 - <<'PY'
import json
d=json.load(open('tools/registry.json'))
bad=[r['name'] for r in d['rows'] if any('verify.py' in a or 'verification-3.json' in a for a in r['argv'])]
assert not bad, bad
PY
```
(The record's "current" digests must be computed at `REV`, not copied from
`BASE`; SHONEN changes again with C2c.)

### D6 — round-15 attempt-1 misattribution

R1 (red; **[OBSERVED]**):
```sh
git show "$BASE:.ufo/evidence/round-15/verification.json" | python3 -c '
import json,sys
d=json.load(sys.stdin)
for c in d["checks"]:
  if c["name"] in ("usage-proof-new","gate-usage"):
    print(c["name"], c["observed_exit"], c["observed_id"], repr(c["stderr"][-60:]))'
# both: exit 64 observed_id=context_consistent; stderr tail CONTEXT: USAGE_ERROR (id=usage_error exit=64)
# source sha256 4d2fb03f81df6aa92574187614a2a9ece5b3e928a03170f1e34809109428352d
```

G1: an appended round-17 correction (e.g.
`.ufo/evidence/round-17/attribution/round15-attempt1-correction.json`) names
both rows with `recorded=context_consistent`, `rederived=usage_error`, the
retained verdict line, and the source sha; `verification.json` is unchanged.
`reattribute.py` is hardcoded to `verification-3.json` at `BASE`; the L1 either
parameterises a copy or derives the same two ids with the repaired rule. The
`verification-3.json` correction (`round-16/attribution/correction.json`) is
the precedent: `rederived_new_id=usage_error`, `verdict_line=CONTEXT:
USAGE_ERROR (id=usage_error exit=64)`.

### D7 — confinement (deferred)

R1 (red; **[READ]**): note §6 (`corpus/knowledge/mutation-case-kumitate-round-gate.md:141-145`):
"the guard scrubs the environment; it does not confine … a hostile mutant can
still write outside its directory, overwrite a sibling mutant, or reach the
network."

G1 (if landed): a canary mutant whose suite writes `../escaped-r01` and dials a
loopback port is denied under the confinement wrapper; the leg's
`REGRESSION_TABLE` is unchanged and a selftest case asserts containment. If
not landed, the round-17 record must re-name G11 with an owner and a round; the
lesson's "next-round work" is then not silently dropped.

## 4. Secondary observations (page errata, not lesson-named — not owed here)

The round-16 page errata's minor-gaps paragraph also names: dead `/tmp`
evidence paths in rounds 6–9 records; anchors written as tool sha256 rather
than revisions; Appendix B survivor-probe fixture contents; the
`git status --porcelain` index-lock note; nested `round-gate` check [51]
recording skip-as-pass. These are not in the round-16 lesson's debt list and
are not acceptance items for this ticket; they stay visible if the L1 wants to
sweep them.

## 5. Verification gaps and residual risk

- Green-after commands for OP1-v2, measure-v2, registry-check, and the cold-read
  tooling are contract-derived **[INFERENCE]**: none of those files exists at
  `98bea7d`. The L1 must run them at `REV`; an unrun check has not passed.
- I did not run `--regression`; the D1 canary count and the full-leg run are
  **[INFERENCE]**. The static fact (only leg 7 is scrubbed) is observed.
- The C2b `inputs-unrecorded` reason assumes the v2 measure applies the input
  rule to entries whose `commands_executed_count>0` and whose `inputs` is
  absent; that is the stated interface. A v2 that treats missing `inputs` as
  "no executed commands" would be a defect and would make the red pass.
- C2c and D3/D4 have semantic limbs that a grep cannot prove; the mechanical
  floors are listed and marked.
- D7 is outside the round's declared claims; treat its row as a
  disclosure/naming obligation, not a build gate, unless the L1 chooses to
  land confinement this round.
- X1 and X2 were found by this seat, not by the round-16 lesson. X1's red is
  first-hand (clone reproduction, 5 s, rc 0, HEAD moved); the live-lane chain
  is recorded in the reflog and was restored by the L1. If the registry keeps
  `mutate-and-run-selftest` and `verify-round15` in their current form, the
  monitor is not a no-harm monitor, and `held=N/N` can be true while the lane
  or its evidence moves.

## 6. Verdict

**built** — 6 routed defects + 7 lesson-named open debts + 2 wave-discovered
monitor defects inventoried; every red-before is executable at `98bea7d` (the
OP1 step-2 and step-3 failures were re-executed and are stronger than the
spotcheck's inference; X1 was reproduced in a clone: rc 0 while HEAD moved),
and every green-after is stated as a copy-pasteable end-of-round check with
its expected exit/ids; items that cannot be run before landing are labelled
`[INFERENCE]`.
