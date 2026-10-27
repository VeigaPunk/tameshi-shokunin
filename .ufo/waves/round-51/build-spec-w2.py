#!/usr/bin/env python3
"""Build round-51 wave-2 (64 v1 falsifiers) from the current candidate."""
import json, os, re, subprocess
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET='/home/vgpnk/Projects/shokunin'
E=LANE+'/.ufo/evidence/round-51'
W2=LANE+'/.ufo/waves/round-51/w2'
SCR='/fast/scratch/hyaku/tameshi-r51'
P='T51W2'
BASE='9962033fd7a75aa2f2847e979dd687a5d28505a1'
CAND=subprocess.run(['git','-C',LANE,'rev-parse','master'],capture_output=True,text=True,check=True).stdout.strip()
DIRECTIVE=open('/home/vgpnk/.agents/skills/godspeed/directive.md',encoding='utf-8').read().rstrip()
TEMPLATE='/skill:godspeed\n'+DIRECTIVE+'\n\n## Your item\n\n{{item}}\n\nWork the item end to end, then write your report file and return your findings.\n'

# Recompute the exact CAND sections whose cold-read credit fell from BASE. These readers
# provide the independent reads.json rows consumed by the already-tested re-key instrument.
cmd=['python3','-B',LANE+'/.ufo/evidence/round-21/coldread/measure.py','--repo',LANE,'--rev',CAND]
r=subprocess.run(cmd,capture_output=True,text=True,check=True)
mon=json.loads(r.stdout)
sections=[s for s in mon['coldread']['sections'] if not s['credited']]
if len(sections)<20: raise SystemExit('expected at least 20 cold-read losses; observed %d'%len(sections))

CONTEXT=f'''# Goal
Round 51, wave 2 (falsify). Lane `{LANE}`. Base `{BASE}`; content candidate `{CAND}`. Wave 1 returned 60/60 seats, no dead seats (orchestrator result `{LANE}/.ufo/waves/round-51/w1-results.json`). The round has three frozen claims and an amended freeze (`9d023aed5e71391c7819d1256e19a35b26fdcb31`); read `{E}/contract.json` and the C1/C2/C3 counters before your item. No claim rule, target, counter or spec was amended by wave 1. One seat discovered C3's base-scope narrative understated rows in other SKILL subsections (18 tools mentioned across sections; only 12 absent anywhere); the counter/predicate still tests the canonical table and every tool, so this is disclosed in `{E}/integrate/l1-notes.md`.

Known measured facts to attack, not decide: the C2 sweep was 2/10 KILLED under the exact registered runner suite and its committed table reproduces; independent neutral-path experiments turn exactly K_GONE_ARM/K_AMBIG_GT/K_SHAPE_OPTIN into KILLED (5/10), so those three are harness-masked, not equivalent. CritPrereg finds the suite is described only in spec prose, and the counter checks receipt consistency, not suite provenance. The counter mutation probe found 15 weakening mutants survive D1/D2/D3, each with a forge; these are disclosed, not concealed. C1 expectations matched in two independent re-derivations. C3 has a known blocker: the truthful `tools/round21-measure.py --selftest` exits 1 from the counter's fresh clone because its fixture expects sibling fleet repos; a row cannot make that true. Do not invent a shim or lie in a row. C3's frozen predicate may therefore fail honestly. W1 report: `{LANE}/.ufo/waves/round-51/w1/T51CritC3Counter.md`.

Cold-read: 20 sections lose credit at CAND (19 `input-drift:tools/mutate-and-run.sh`, 1 registry section `no-ledger-entry`). Their exact headings and pointers are in the fixture list `{LANE}/.ufo/waves/round-51/w1/T51ExecRekey.md` §3; the real list is dynamically recomputed by the L1 before re-key. Your `## Reader` item must verify the section's claims against candidate bytes, not just rephrase it. The L1's `refresh.py` requires one named reader per heading.

Seat bounds: read-only on lane/fleet/sibling repos except your own report/deliverables under `{W2}`. Use `git -C <repo> show <rev>:<path>` for repo reads. No git/jj mutations in lane/fleet/sibling repos; fixture git operations only in a `git clone --shared` or `mktemp -d -p "$S"`, with `rev-parse --show-toplevel` checked before any fixture commit. Every `Report:` path is relative to `{LANE}`; write at `{LANE}/<that path>`. Scratch root `{SCR}/<seat>/`, explicit TMPDIR/--work, delete before yield. No `/tmp` beyond <50MB. Never use agent://all. Pacman is paused. If installing/updating tools, first read `/home/vgpnk/.omp/agent/RULES.md` and record tool/version/channel/reason; no install is expected.
'''

ITEMS=[]
def add(name,role,axes,milestone,text): ITEMS.append({'name':P+name,'role':role,'axes':axes,'milestone':milestone,'item':text})

TOOLS=json.load(open(E+'/c3/tools-base.json'))['tools']
for i,t in enumerate(TOOLS,1):
 add('ExecTool%02d'%i,'executor',['operability'],'C3 row falsification',f'''Independently audit C3 registry row for `{t}` at candidate `{CAND}`. Read the canonical SKILL.md section `#### Gate/probe registry — round 51` and the tool at `{t}` at candidate. Run the row's exact backticked self-test from a `git clone --shared` at CAND with scratch TMPDIR and stdin /dev/null; run usage probe `--r51-no-such-flag`; record exits, last line and wall time. Check row fields against source: tool truly fails or is only a probe, exit codes and meanings, pinned values really affect expected behavior, write scope, and last-line marker is a meaningful diagnostic rather than author-chosen help text. Do NOT write source or repair the row. Report any mismatch, including row16's known clone-context failure if your tool is it; cite file:line and output. Deliverable `{W2}/@P@ExecTool{i:02d}.md` and raw receipts under `{W2}/@P@ExecTool{i:02d}/`.
''')

for i,s in enumerate(sections,1):
 head=s['heading']; start=s['start']
 add('Read%02d'%i,'reviewer',['calibration'],'cold-read rekey reader',f'''Read the SKILL.md section headed exactly `{head}` at candidate `{CAND}` (starts at line {start}; re-resolve the heading and read through the next heading at CAND), plus every cited file/pointer in the section against candidate bytes. Be adversarial: identify stale/moved pointers, statements made false by the tenth leg/runner TMPDIR change/four panel-tool updates, and any unsupported premise. Do not trust the old `READERS_JSON` or the fixture list; read the entire section and every cited non-record surface. Return one structured row for `reads.json`: heading, each pointer (raw text, file, ranges, verdict holds/absent, located excerpt), strongest possible falsifier checked, and seat name `{P}Read{i:02d}`. This row is consumed by the round-49-style trace-bound re-key, so it must reflect a real read, not a summary. Deliverable `{W2}/@P@Read{i:02d}.md`.\n''')

# Eight independent falsifiers, plus required second-round executors, connectors, scribe and scout.
critics=[
('CritC1Forgery','C1 counter false-positive search','Try to forge C1 on a scratch clone of CAND: preserve `C1_R51_PASS=true` while the status table is wrong, the pointer range is unsupported, a second/different table is appended, or SOURCES status/used-by is contradictory. Use at least 6 single-clause mutations of the frozen counter/statement set; show pristine rejects and mutant passes, or explain equivalent. Do not alter lane files. This is a critic attack, not a new C1 verdict.'),
('CritC2Registration','C2 receipt and suite binding','Adversarially review the C2 original sweep vs neutral-path reproduction, frozen spec, runner table and counter. Can the measured receipt be derived from committed bytes and the actual suite? Name exactly what is pre-registered, what is only prose/self-stamped, and whether the tenth-leg depth claim still verifies independent of kill-rate. Attack any attempt to change the suite/table after seeing data; use `T51CritPrereg.md`, `T51MutC2Counter.md`, and `T51LabSandboxLeak.md`.'),
('CritC3Truth','C3 registry row truth','Review all 30 consolidated rows at CAND against row-level executor evidence and the frozen C3 counter. Identify rows where kind, entry command, exit map, pinned values, write scope or marker are untrue, and the known round21-measure row whose fresh-clone selftest exits 1. Does a canonical table with one truthful failing tool meet the frozen predicate? State the resulting honest C3 verdict; never recommend --help aliasing.'),
('CritSourceEntry','S272/S273 and C2 entry fidelity','Reopen the actual pinned kagi blob and both source snapshots from W1 evidence; verify S272/S273 row anchors/quotes/tier/kind/URL and C2 knowledge entry source line/ground/recheck/claims against the original and neutral sweep evidence. Check census schema, 11 columns, W04/E04, opened date and used-by exactly; record any statement that should be softened.'),
('CritNoHarm','No-harm and re-key invariants','Independently run the no-harm script and coldread monitor on CAND in scratch. Confirm the four panel-tool scope amendment, S022 `73→74, fresh=71, score=9`, all other no-harm floors, and identify every lost section (expected 20). Inspect re-key trace and append-only logic. Never write the lane.'),
('CritC2Counter','C2 counter blind spots','Review `T51MutC2Counter.md` and its 17-mutant matrix. Check each surviving forge really violates exactly its named clause and that D1/D2/D3 do not cover it; independently attack at least one blind spot. Verify M16 equivalence reasoning and M17 kill. Name any overclaim.'),
('CritQualityMistake','QUALITY 102 and mistake proof','Review the round-51 mistake row and QUALITY criterion 102 against `T51LabSandboxLeak.md` raw A/B/C evidence. Does the check have a real red/green falsifier? Are the 3 path-masked mutants exact, and do negative controls stay unchanged? Challenge whether the criterion scope is too broad/narrow.'),
]
for name,title,body in critics:
 add(name,'critic',['calibration','depth','operability'],'cross-claim falsifier',body+f'''\nDeliverable `{W2}/@P@{name}.md`, findings F1… with exact commands and evidence pointers.''')

add('MutC3Counter','mutation-tester',['operability'],'C3 counter falsifier',f'''Mutation-test frozen `{E}/c3/measure.py` on scratch copies only. Build at least 10 one-edit mutants weakening one clause (tool-set deletion detection, row-heading containment, verdict tokens, selftest argv/marker, usage exit, pinned path existence, write scope/owner, return-on-failure, row duplication). Run its 10-case `--selftest` and test forged SKILL rows against scratch clones at CAND. Show any mutant that passes a tree the pristine counter rejects, or prove equivalent; include the round21-measure selftest failure as an input to the result, not a case to mask. Deliver `{W2}/@P@MutC3Counter.md` plus receipts.''')

# 32 executors total: the 30 row tools plus two direct final measurements.
add('ExecFinalCounters','executor',['calibration','depth','operability'],'candidate counter probes',f'''On one `git clone --shared` at CAND (toplevel checked; scratch under `$S`), run the three frozen counters once with explicit TMPDIR/--work and preserve each stdout/exit: C1 `--explain`, C2 `--explain` (its regression uses a local fleet layout with read-only sibling symlinks), C3 `--explain`. Also run the round-51 no-harm script and sources census, but label every invocation a probe, not deciding verdict. Confirm current tree hash at CAND and no writes to the clone. Copy all receipts to `{W2}/@P@ExecFinalCounters/`; report exact output lines, including any failure. Do not amend counters or predicates.''')
add('ExecC2Replay','executor',['depth','operability'],'runner 10-leg replay and dependent gates',f'''On a `git clone --shared` of the candidate at `{CAND}` placed in a scratch fleet layout with read-only sibling symlinks, run `bash tools/mutate-and-run.sh --selftest` and `--regression --workdir $S/reg`; then run `tools/tally-audit.py`, `tally-audit-v2.py`, `tally-audit-v3.py` in their documented audit modes and `mte-interop.py --check --regression-stdout regression.stdout --workdir ...` against the same ten-leg regression. Use `TMPDIR=$S/tmp`; record all exit codes, PASS/FAIL summaries and wall times. The runner selftest, exact 10-case regression and all four panel gates must be green; do not alter bytes. Deliver `{W2}/@P@ExecC2Replay.md` and raw receipts under `{W2}/@P@ExecC2Replay/`.''')

add('ConnSibling','connector',['adjacency','operability'],'registry and oracle sibling overlap',f'''Read-only scan of sibling lanes for (a) fragmented registry sections and gate/probe row contracts, (b) selftests with verdict text grepped from output that includes scratch paths, (c) runner-ledger references pinned to nine legs. Name actual files/lines, owner lane, and whether any observed pattern is genuinely cross-domain or belongs to that owner. Report only recommendations, never absorb or edit siblings. Deliver `{W2}/@P@ConnSibling.md`.''')
add('ConnCrossClaim','connector',['calibration','depth','operability'],'C1-C3 cross-claim pattern',f'''Read the frozen contract, all three counters, candidate changes and W1 attacks. Identify every shared surface/possible interference; judge causal separability; trace how C2's new mined source rows feed C1 and its runner changes feed C3; give the honest claim-level before/after dependency graph. Specifically address the fact the canonical C3 row set includes a truthful row whose selftest cannot pass in a fresh clone. Deliver `{W2}/@P@ConnCrossClaim.md` with a compact matrix and file:line evidence.''')
add('ScribeFinalLesson','scribe',['calibration','depth'],'final lesson fact check',f'''Read the integrated `corpus/lessons/round-51.md`, W1 source/entry/falsifier reports, W2 reviewer outputs and the candidate receipts. Draft a corrections block only for factual mismatches found; do not write lane files. Check the lesson's `## Gate` entries against the actual SOURCES rows and local/UTC dates, and `## Mistakes` against the captured-by and falsifier bytes. Deliver `{W2}/@P@ScribeFinalLesson.md` with exact replacements, or `no corrections` plus evidence.''')
add('ScoutC3Provenance','scout',['operability','calibration'],'C3 environment dependency',f'''Read-only inspect `tools/round21-measure.py` and its frozen delegates. Explain why `--selftest` passes with sibling lanes resolvable but exits 1 in the C3 counter's fresh clone; show exact repo-root calculation and hardcoded fleet dependency, and whether it is in province to fix in a later round. Do not modify files or suggest a row that aliases help output. Deliver `{W2}/@P@ScoutC3Provenance.md`.''')

assert len(ITEMS)==64,len(ITEMS)
roles={}
for x in ITEMS:roles[x['role']]=roles.get(x['role'],0)+1
assert roles=={'executor':32,'reviewer':20,'critic':7,'mutation-tester':1,'connector':2,'scribe':1,'scout':1},roles
spec={'wave':'round-51-w2','reportDir':'.ufo/waves/round-51/w2','template':TEMPLATE,'context':CONTEXT,'items':ITEMS}
path=LANE+'/.ufo/waves/round-51/spec-w2.json'
with open(path,'w',encoding='utf-8') as fh: json.dump(spec,fh,indent=2,ensure_ascii=False)
print('candidate',CAND,'targets',len(sections),'items',len(ITEMS),'roles',roles,'reportDir',spec['reportDir'])
for i,s in enumerate(sections,1): print('READ',i,s['heading'])
