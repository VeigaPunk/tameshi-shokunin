# ColdB01 — cold read, SKILL.md sections 2 (375), 3 (827), 4 (858) at bb681566b18211adf8ae9c28df91e17678e3f545

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB01", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
  {"start": 375, "heading": "## Restore discipline — before/after identity, not continuous non-write proof", "class": "record", "verdict": "verified-record",
   "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
   "commands_executed": [
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-2-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/README.md tools/mutate-and-run.sh"
   ],
   "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/README.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/gates-survey-kagi.md", "tools/mutate-and-run.sh"],
   "inputs": {
     "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
     "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
     "corpus/README.md": "636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909",
     "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
     "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
     "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"},
   "external_inputs": {
     "tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:SCORECARD.md": "9ba015ca568db27e71dd35322884952c18f7be0e306667f35391da7174fd920a"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-2-1.json"]},
  {"start": 827, "heading": "### The protocol — ordered, fail-closed", "class": "instruction", "verdict": "gap-minor",
   "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": [
     "SKILL.md:845-846 defines KILLED as suite exit not equal to 0, overlapping INCONCLUSIVE's exits 124/126/127, which the tool classifies as INCONCLUSIVE (tools/mutate-and-run.sh header lines 59-61 and verdict semantics); the intended reading is exit not 0 and not in {124,126,127} (carried from round-27 seat Read08 minor gap).",
     "SKILL.md:839 under-specifies the write-to-target condition: the workdir clause says the original is a write target only when --workdir is its own directory, but round-27 measured a name clash inside --workdir (target named results.tsv) where the harness overwrote the target and reported DRIFT; the real trigger is an output-file name clash inside --workdir (carried Read08 minor gap).",
     "SKILL.md:847-848 prints only MUTATE_RESTORE: OK|DRIFT and does not state the DRIFT consequence; the tool code shows DRIFT is followed by MUTATE: SETUP (byte-identity proof failed) exit 2 with no headline (tools/mutate-and-run.sh:561-563) (carried Read08 minor gap).",
     "SKILL.md:830-831 says every run log carries its own MUTATE_TOOL pin; the pin prints on the run's stdout headline block, not inside evidence/<id>.out, which holds suite output only (observed in ColdB01-3-1: evidence/K1.out contains only the suite line; MUTATE_TOOL is a stdout line) (carried Read08 minor gap).",
     "SKILL.md:854-856 says T6-1 wrote six survivor classes first; the mado note says the same six survivors (mutation-case-mado-verify.md:187-188); the 10/10 prediction-holding claim matches :73 and :187-189 (carried Read08 minor gap)."
   ],
   "commands_executed": [
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-1.json -- bash tools/mutate-and-run.sh --target /tmp/ColdB01-sVBL/scratch/fake-gate.sh --defects /tmp/ColdB01-sVBL/scratch/spec-ok.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/ColdB01-sVBL/scratch/work-ok",
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-2.json -- bash tools/mutate-and-run.sh --target /tmp/ColdB01-sVBL/scratch/fake-gate.sh --defects /tmp/ColdB01-sVBL/scratch/spec-bad.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/ColdB01-sVBL/scratch/work-bad",
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-3.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-mado-verify.md tools/mutate-and-run.sh",
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-4.json -- bash tools/mutate-and-run.sh --target /tmp/ColdB01-sVBL/scratch/fake-gate.sh --defects /tmp/ColdB01-sVBL/scratch/spec-noop.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/ColdB01-sVBL/scratch/work-noop",
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-5.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/waves/round-27/w1/Read08.md"
   ],
   "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/mutation-case-mado-verify.md", ".ufo/waves/round-27/w1/Read08.md"],
   "inputs": {
     "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
     "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
     ".ufo/waves/round-27/w1/Read08.md": "c78ff31a836a746b86f1396d0efbe8aa0acbfea62928f670708829c4c45d27e2"},
   "external_inputs": {
     "tameshi-shokunin@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh": "597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b"},
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-3-5.json"]},
  {"start": 858, "heading": "### The boundaries — what a service run is not", "class": "record", "verdict": "gap-minor",
   "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": [
     "SKILL.md:879-881 cites mutation-case-mado-verify.md:229-230 for the sensitivity claim; the U2 line stating suite sensitivity is not gate truth spans :228-229, so the cited span starts one line late (carried from round-27 seat Read09, whose smallest-correction note said start the U2 cite at :228).",
     "SKILL.md:867-868 'a survivor is a gap named with its class' is stated inside the bullet whose only citation (SKILL.md:335) supports the companion clause; the named-with-class inventory lives at mutation-case-mado-verify.md:101-147 but is not cited here (Read09 had flagged this uncited clause as a minor gap at round 27)."
   ],
   "commands_executed": [
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-4-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/fleet-suite-census.md tools/mutate-and-run.sh",
    "python3 tools/trace-inputs.py --root /tmp/ColdB01-sVBL/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-4-2.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/waves/round-27/w1/Read09.md"
   ],
   "opened": ["corpus/knowledge/mutation-case-mado-verify.md", "corpus/knowledge/fleet-suite-census.md", "tools/mutate-and-run.sh", ".ufo/waves/round-27/w1/Read09.md"],
   "inputs": {
     "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
     "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
     "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
     ".ufo/waves/round-27/w1/Read09.md": "09a451900ef046840dedd799449521b0449b8b9a88c4bc94d9a5d868cf8e0f2e"},
   "external_inputs": {},
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-4-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB01-4-2.json"]}
 ]}
```

## What I checked

Section 2 (375-404, class `record`, **verified-record**). Every cited pointer resolves
to supporting text at bb681566. Item 1: `mutation-case-kimi-census.md:13-16` records
sha256 83016d45…4f426, 896 lines, 43273 B, mtime, repo rev `175de6ba…`, empty
porcelain; `mutation-case-kagi-census.md:13-17` likewise (sha 275d8294…53009f,
44212 B, mtime 09:47:15, mode 755, HEAD fecee87, status empty). Item 2: kagi :44-45
carries the `cp -p` byte copy and `cmp`-verified claim; kimi :4-7 carries
fresh-copy-only edits. Item 3: kimi :34-35 and kagi :54-56 both record sha
before = after with size/mtime unchanged and clean status, and neither records an
after-repo revision — matching "not established by those records". Item 6:
SCORECARD.md:13 (external input; one of the four post-append files, read via
`git show bb681566:SCORECARD.md`, sha256 9ba015ca…) records the round-2 probes
executed on fresh /tmp copies; kimi :174-175 shows the driver is unversioned
`/tmp/tameshi-r2-1-work/mutate_driver.py`, and `bash tools/mutate-and-run.sh
--regression` exists as the maintained replay path (usage :198; ledger dispatch
:1346+). Item 7: corpus/README.md:11 (round-2 addendum row) records G-R2-1 —
the surveyed 79294/357fb245 bytes were a dirty intermediate state never committed,
corrected to the committed 79301/93c58272 — exactly the "re-pin a committed
revision" lesson; corroborated at gates-survey-kagi.md:554-557.

Section 3 (827-857, class `instruction`, **gap-minor** — the named command ran as
written; wording gaps only). Executed `bash tools/mutate-and-run.sh --target
fake-gate.sh --defects spec-ok.spec --suite 'bash "$MUTANT" --selftest' --workdir
work-ok` (ColdB01-3-1): CONTROL GREEN, DEFECT K1 KILLED (exit=1), DEFECT S1
SURVIVED (exit=0), MUTATE_RESTORE: OK (sha before=after), MUTATE_EVIDENCE printed,
`MUTATE: DONE (… killed=1 survived=1 inconclusive=0 kill-rate=50%)`, exit 0; the
workdir keeps pristine + both mutants + `evidence/{control,K1,S1}.out` +
`results.tsv` + `defects.tsv` + `spec.copy` as step 6 lists. A no-op spec
(`@new == @old`) produced `spec: defect N1: @new equals @old (no-op mutation)` +
`MUTATE: SETUP (spec parse failed)`, receipt exit 2, zero suite runs and no
headline (ColdB01-3-4) — matching steps 2-3. A spec whose two defects share one
`@old` ran fine (ColdB01-3-2), confirming uniqueness is per-defect. The pinned
parenthetical verifies: `git show b58b26fbeba8fd972e1d31ac8a9175a81e333b32:
tools/mutate-and-run.sh` = sha256 597e1419…ff6331b, exactly 1001 lines; the path
at bb681566 is a7d3f2dd… (2080 lines), i.e. a later revision — the round-27
Read08 blocking gap is repaired. Remaining minors are carried Read08 items listed
in the JSON (KILLED/INCONCLUSIVE overlap at :845-846, the --workdir clause at
:839, unnamed DRIFT consequence at :847-848, MUTATE_TOOL lives on stdout not in
per-defect logs at :830-831, "six survivor classes" vs note's "six survivors" at
:854-856).

Section 4 (858-882, class `record`, **gap-minor**). The round-27 Read09
gap-blocking findings are repaired: the bullet now says the tool emits no
tree-clean check (my sweep outputs confirm — no porcelain line anywhere) and
`tools/mutate-and-run.sh:36-38` ("The target is never written…") verifies
verbatim; `mutation-case-mado-verify.md:57-59` holds the sha pair
(MUTATE_RESTORE OK, before=after=d7edaab4…d0e13); `fleet-suite-census.md:288-291`
is exactly the scope paragraph (single-edit, hermetic, per-revision/per-host);
SKILL.md:377-378, :808-809 and :335 all resolve (the <50 % "gap recorded in the
table, not softened" line sits at :335). `mutation-case-mado-verify.md:175-176`
("first below the 50–80 band"), :66-72 (4 in-surface 4/4 + 6 out-of-surface 0/6),
:237-238 + :240-260 (recommendations unabsorbed, §8 recommendation list), :17-23
(Incident I1, re-pin b56c6e57…2bcb) all verify. Two minors remain (cited span for
U2 starts one line late — it is :228-229, cited :229-230; and the
"survivor…named with its class" clause stays uncited — inventory at :101-147).

Tooling: strace (pre-installed, /usr/bin/strace) and python3 3.x used; nothing
installed. All traces ran inside the fleet-mirror clone detached at
bb681566b18211adf8ae9c28df91e17678e3f545; receipts record `rev` =
bb681566…f545 and `exit` = the child command's exit (0 for the reader/sweep
receipts, 2 for the SETUP refusal).

COLDREAD ColdB01: verified-record, gap-minor, gap-minor
