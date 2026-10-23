# Round 35 — residual contract critic
Advisory review only; no canonical judge or admission action invoked. Axes: **depth** (v3 audit detail), **calibration** (record fidelity), **operability** (runnable discrimination).
Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master` → `34fa5b0cfe909f3cde644676ead723256281dd05` (observed at start and before reporting).
No installs. No counter main/default-mode run, tool CLI run, canonical judge, or admission action performed; no repository write except this report. Evidence work used source/receipt inspection and isolated Python/Bash expression/lexer probes. An initial lexer-probe command had a Python SyntaxError; the corrected executed command is below.
## 1. MAJOR — PASS is weaker than the declared public target
Exact code: `c1/c1-measure.py:517`: `and pub_kill == pub_kill_slots and pub_accept == pub_accept_slots`; lines 516–520 never require public slot totals 6/3 or `pub_distinct == 9`. Contract line 32 requires `pub_kill=6/6 pub_accept=3/3 pub_distinct=9`. Thus an empty panel or duplicate bodies can satisfy the code but not the target. The predicate sentence at line 28 also omits these cardinality/distinctness requirements.
Executed command (AST RHS only; never invokes the counter):
```sh
python3 -c 'import ast,json,pathlib
p=pathlib.Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35")
t=ast.parse((p/"c1/c1-measure.py").read_text())
n=next(n for n in ast.walk(t) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=="ok" for x in n.targets))
c=json.loads((p/"contract.json").read_text())["claims"][0]
print("code L%d: %s"%(n.lineno,ast.unparse(n.value)))
print("target:",c["after_target"])
e=dict(runner_ok=True,tool_present=True,tool_sha_ok=True,pub_kill=6,pub_kill_slots=6,pub_accept=3,pub_accept_slots=3,pub_distinct=9,ho_kill_total=4,ho_accept_total=2,ho_kill=4,ho_accept=2,ho_invalid=0,sealed_ok=True)
x=compile(ast.Expression(n.value),"<frozen PASS RHS>","eval")
for label,patch in [("target with ho_accept=2",{}),("empty public panel",dict(pub_kill=0,pub_kill_slots=0,pub_accept=0,pub_accept_slots=0,pub_distinct=0)),("9 slots but duplicate bodies",dict(pub_distinct=2))]:
 print(label+": code_PASS="+str(eval(x,{},e|patch)))
print("counter_main_invoked=False")'
```
Observed output (selected):
```text
target with ho_accept=2: code_PASS=True
empty public panel: code_PASS=True
9 slots but duplicate bodies: code_PASS=True
counter_main_invoked=False
```
The receipt actually meets the stronger target: public 6/6 + 3/3, 9 distinct; sealed 4/4 + 3/3, invalid 0, both pins/provenance 1 (item 2). `ho_accept_total >= 2` at line 518 agrees with `a>=2`; the observed 3 is NOT a defect or a hidden threshold of 3. Kill rc/check and accept rc semantics match the sentence (lines 376–381).
Impacted axes: depth/calibration/operability. Smallest safe correction: disclose the mismatch and evaluate the existing receipt against the explicit target; prospectively assert public totals 6/3 and distinctness 9, and align the sentence. Do not silently amend frozen rules or rerun this round.
VERDICT: DEFECT — fixable predicate/contract divergence, despite a receipt satisfying the declared counts.
## 2. MINOR — stale control prose; the retained control really uses nine copies
Contract line 31 says “all three kill copies” and `pub_distinct=6`; lines 65/68 say “same public panel (8 copies at A4)” and `0/5 kill`. Both descriptions are stale, not the retained receipt.
Executed receipt-summary command:
```sh
python3 -c 'import json,pathlib
p=pathlib.Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35")
c=json.loads((p/"contract.json").read_text())
print("C1.control:",c["claims"][0]["control"])
print("C1.controls_before_data:",json.dumps(c["controls_before_data"][0],ensure_ascii=False,sort_keys=True))
for rel in ["control/c1-v2-control.stdout","control/c1-v3-public-rehearsal.stdout","after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout","after/c2-at-d16f9b5a.stdout"]:
 t=(p/rel).read_text().splitlines();print(rel+": "+t[-1])
print("deciding_exit="+(p/"after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.exit").read_text().strip())
print("control_exit_sidecars="+str([x.name for x in (p/"control").iterdir() if x.suffix==".exit"]))'
```
Observed output (receipt/exit lines only):
```text
control/c1-v2-control.stdout: C1_R35_CONTROL: mode=control tool_present=1 tool_sha=7b11ba25aead9367 tool_sha_ok=1 runner_sha_ok=1 pub_kill=0/6 pub_accept=0/3 pub_slots=9 pub_distinct=9 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=5829676d81859fffa739272b4d09f28d55123d45 C1_R35_CONTROL_PASS=false
control/c1-v3-public-rehearsal.stdout: C1_R35_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=5829676d81859fffa739272b4d09f28d55123d45 C1_R35_CONTROL_PASS=false
after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout: C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=34fa5b0cfe909f3cde644676ead723256281dd05 C1_R35_PASS=true
after/c2-at-d16f9b5a.stdout: C2_R35: m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 entries=40 sources_rows=99 rev=d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc C2_R35_PASS=true
deciding_exit=0
control_exit_sidecars=[]
```
Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show -s --format='%h %aI %cI %s' 7da6e07 68f2557 691bb51 3168749 5829676d81859fffa739272b4d09f28d55123d45 34fa5b0cfe909f3cde644676ead723256281dd05`.
Observed output (selected commit lines; commit subjects are not independent process-exit receipts):
```text
7da6e07 2026-10-23T18:26:38-03:00 2026-10-23T18:26:38-03:00 round-35: A4/A5 before + control receipts re-run (before tool absent, exit 1; v2 control 0/5 kill 0/3 accept on the 8-copy panel)
691bb51 2026-10-23T18:56:12-03:00 2026-10-23T18:56:12-03:00 round-35: A4-A7 pre-data apparatus (real auto-root value+shape witness, four-config whole-stdout sweep, ambiguity-refusing locator, comment-blind + leg-occurrence head rule, filesystem-safety gate) re-pinned; sealed set 4 kill + 3 accept with manifest; root-keyed-shape6 panel copy; lesson A4-A7
3168749 2026-10-23T18:57:14-03:00 2026-10-23T18:57:14-03:00 round-35: final before + v2 control receipts on the 9-copy panel (before exit 1; control 0/6 kill 0/3 accept exit 1) + tool selftest 33/33 under the final pins
34fa5b0 2026-10-23T19:36:46-03:00 2026-10-23T19:36:46-03:00 round-35 A8 receipts re-run from the final counter bytes: before exit 1 (tool absent at base) + v2 control 0/6 kill 0/3 accept at 5829676d + pre-data v3 public-panel rehearsal 6/6 kill 3/3 accept (no sealed scored)
```
Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --exit-code 5829676d81859fffa739272b4d09f28d55123d45 34fa5b0cfe909f3cde644676ead723256281dd05 -- /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c1/panel/` → no output, exit 0.
[INFERENCE] V2 cannot meet the public target even if sealed scoring were added: six kill false accepts and three accept kills/refusals. V3 rehearsal also prints CONTROL_PASS=false because sealed totals are zero: that boolean alone is not a discriminating control. Control exit 1 is recorded in history and follows code line 531 (`return 0 if ok else 1`), but no control exit sidecar exists; independent rerun: **not run**.
Impacted axis: calibration. Smallest correction: append reconciliation of 6→8→9-copy historical wording, identify the final receipt revision, and distinguish public-only rehearsal from deciding PASS.
VERDICT: CONFIRMED — do-nothing control fails on the CURRENT nine-copy panel; DEFECT in contract control narration, not control reach.
## 3. NOTE — one retained default receipt, not a proof of execution cardinality
Exact kill rule (contract line 33): “exactly ONE default-mode C1 run at the measurement revision, after the sealed set lands; no re-seed, no re-scale, no post-data rule change, no second default-mode run”.
Tool command `functions.grep({"i":"Confirming bounded default receipt census","pattern":"C1_R35: mode=deciding","path":"/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/","case":true,"gitignore":false,"skip":null})` → exactly one matched file: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout:17` (full matching line in item 2).
Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-files --error-unmatch -- /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout` → exit 1; `error: pathspec '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout' did not match any file(s) known to git`.
Impacted axis: calibration/evidence durability. No second deciding receipt at another revision was found. An untracked file cannot establish that an earlier run was never discarded/overwritten; actual execution count **cannot determine** from retained receipts alone. Smallest correction: preserve the existing receipt and exit/stderr durably, plus any already-existing invocation record; never manufacture evidence or rerun.
VERDICT: CONFIRMED — one retained deciding receipt at one revision; exactly one historical execution is not independently proven.
## 4. MAJOR — bounded specimens are soundly sized; unrestricted comment-blanking is not
Exact violating surface text (contract line 26, decoded JSON value): “tools/tally-audit-v3.py: (1) the runtime oracle sweeps all four (auto,KEEP) triples, not two; (2) the compared tuple is the FULL stdout, not the first line; (3) every structural scan runs on a quote-aware code view with comments blanked; (4) the auto triples run with the runner's REAL auto root (/tmp/tameshi-r4-2-regression.XXXXXX), so a copy keyed on the real root value is observable (amendment A4, pre-data, routed from round-35 seat RevengerRootShape CRITICAL).”
The universal in clause (3) does not enumerate supported Bash lexical forms. Strongest cheap local counterexample: a real comment following ANSI-C quoting is NOT blanked. This tests the surface assertion, not an unlisted specimen against the finite deciding set.
```sh
python3 -c 'import ast,pathlib,subprocess
p=pathlib.Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py")
f=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=="code_view")
ns={};exec(compile(ast.Module(body=[f],type_ignores=[]),str(p),"exec"),ns)
s="  : $"+chr(39)+"it"+chr(92)+chr(39)+"s"+chr(39)+" # st_tsu is counted by the loop below\n"
v=ns["code_view"](s)
print("input="+repr(s));print("view="+repr(v));print("comment_survives="+str("# st_tsu" in v))
r=subprocess.run(["bash","-c",s+"printf '"'"'bash_rc=%s\n'"'"' \"$?\""],capture_output=True,text=True)
print(r.stdout,end="");print("bash_exit="+str(r.returncode));print("tool_main_invoked=False")'
```
Observed output:
```text
input="  : $'it\\'s' # st_tsu is counted by the loop below\n"
view="  : $'it\\'s' # st_tsu is counted by the loop below\n"
comment_survives=True
bash_rc=0
bash_exit=0
tool_main_invoked=False
```
C1 “every kill specimen … on the public panel and on a sealed set” (line 28) is bounded by those directories, NOT a claim about every possible Bash program. The tested lexer failure therefore does not falsify the 16 listed COPY results. C2 names m1–m6 surfaces (line 48); neither claim uses an axis score as its surface. Behavior must stay explicitly scoped to extracted-block `(exit, FULL stdout)`, four CONFIGS and `vectors_for`; stderr, head execution and filesystem side effects are not observed (counter lines 194–244).
Impacted axes: depth/calibration. Smallest correction: disclose the unsupported lexical class and enumerate supported scans/forms in a future pre-data claim (or repair the lexer and independently remeasure in a new round). Do not silently narrow or redefine this frozen claim after seeing its result. The literal unrestricted clause is false; universal semantic correctness as declared is not established.
VERDICT: DEFECT — unenumerated/untrue blanket lexical assertion; finite panel claim remains bounded, not universally falsified.
## 5. NOTE — no round-35 credit; these receipts primarily support operability
Tool command `functions.grep({"i":"Confirming absent round credit section","pattern":"^#{1,6}.*[Rr]ound[ -]?35\b|^\|\s*(?:[Rr]ound\s*)?35\s*\|","path":"/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md","case":true,"gitignore":false,"skip":null})` → `No matches found`. Round-35 mentions in the old sources-registry cell (line 1609) and planned text (1666) are not a measured round-35 claim row.
Tool command `functions.read({"i":"Reading fleet axis definitions","path":"/home/vgpnk/Projects/shokunin/AXES.md:1-240"})` → line 11: `| **depth** | Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources | A reader can act on SKILL.md alone; no filler |`; line 13: `| **operability** | Runnable artifacts: checklists that are executable, commands that exist, scripts that run | A checklist item can be run and produces the stated outcome |`.
Tool command `functions.read({"i":"Reading declared depth rubric","path":"/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md:58-85,1528-1539"})` → line 1536: `| depth | 9 | One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D above prints `recorded_cases=9 depth_score=9` | round-31 measurement revision (measured-result row below) | 26 |`.
Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --exit-code 51d3f08073be65d3475cf0286042fc0dbe4c4a7d 34fa5b0cfe909f3cde644676ead723256281dd05 -- /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` → no output, exit 0.
[INFERENCE] Advisory: C1 demonstrates improved runnable discrimination (quality/operability capability), not a numeric depth increase under the unchanged ledger rubric. Non-numeric depth detail could be defensible if separately bound to actionable source-backed knowledge; these execution counts alone do not establish that move. C2's zero m1–m6 receipt supports bounded calibration repair, not universal record consistency or a scalar increase. Both credits remain unrecorded; the L1/canonical judge decides, with no axis trade silently accepted.
Smallest correction: record truthful per-claim rows and unchanged numeric rubrics. Describe the demonstrated operability/quality work while retaining the unsupported declared depth-credit status; route any new axis claim pre-data, never retrospectively substitute axes or predicates.
VERDICT: CONFIRMED — no round-35 measured credit yet; depth score credit is unsupported by these receipts alone.
ADMISSION: refuse — advisory recommendation for the two claims as declared: C1 has predicate/target divergence and an unrestricted false lexical clause; C2 has a passing bounded receipt, but the pair cannot be recommended unchanged. No admission/judge action performed.
SEAT: ResidualCriticPredicate model=openai-codex/gpt-6.1-sol
