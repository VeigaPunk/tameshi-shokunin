# Read08 cold read: "### The protocol — ordered, fail-closed" (SKILL.md:827, rev 2227d83)

Verdict: wrong-expectation. The named command runs, and the protocol steps I checked behave as the section describes; the wording gaps are listed in the JSON and the note. The one failing item is the pin named in the opening paragraph: at this path the harness is not the 597e1419…ff6331b (1001-line) revision the section names.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read08",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 827,
      "heading": "### The protocol \u2014 ordered, fail-closed",
      "class": "instruction",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": [
        "Opening paragraph (SKILL.md:829-831) names tools/mutate-and-run.sh as the pinned harness and identifies it as the mado run's revision 597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b, 1001 lines. At 2227d83 that path is sha256 fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de, 2016 lines (Read08-1, Read08-9), and each run prints that sha in its MUTATE_TOOL line (Read08-4). The 597e1419 bytes are commit b58b26fbeba8fd972e1d31ac8a9175a81e333b32 (Read08-3). The path last changed in commit a08e85c5d7f899e8a5992e20517edb1a380d79eb, which holds the 2016-line bytes. A reader who runs the named command gets a different harness from the one the paragraph names, and no step says how to get the older bytes. Smallest correction: name fb91ef76...9f9de (2016 lines) as the pin this path delivers at 2227d83; keep 597e1419...ff6331b (1001 lines) only as the historical mado revision, with git show b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh as the way to fetch it."
      ],
      "minor_gaps": [
        "KILLED is defined as suite exit not equal to 0 (line 845). That overlaps INCONCLUSIVE, which covers 124, 126 and 127. The code gives those three INCONCLUSIVE (tools/mutate-and-run.sh:543-549), and Read08-8 shows D2 with exit 127 as INCONCLUSIVE note=suite-not-found and D3 with exit 124 as INCONCLUSIVE note=timeout. Say: exit not 0, 124, 126 or 127.",
        "The workdir clause (line 839) reads inverted and names the wrong condition. Read08-12 (--workdir equal to the target directory, no name clash) ends DONE with the target sha unchanged (94b6019d...). Read08-15 (target named results.tsv inside --workdir) shows the harness overwriting the target at tools/mutate-and-run.sh:537 (sha 2c29813b... became 66bf2e8f...), the restore check reporting DRIFT, and exit 2. The harness neither refuses the clash nor restores the target. defects.tsv (:507) and spec.copy (:508) are written the same way by the code; I did not run those two. Reword to say the target is overwritten when a harness output name matches it inside --workdir, and keep --workdir apart from the target.",
        "Step 5 (lines 847-848) gives OK or DRIFT but not what DRIFT does. Read08-15 shows MUTATE_RESTORE: DRIFT followed by MUTATE: SETUP (byte-identity proof failed ...) and exit 2, with no headline (tools/mutate-and-run.sh:558-561).",
        "Step 5 names only the target sha. The check also compares the pristine copy (tools/mutate-and-run.sh:558).",
        "The opening paragraph (lines 830-831) says every run log carries its own MUTATE_TOOL pin. The pin prints on the run's stdout (tools/mutate-and-run.sh:495; Read08-4). The per-defect logs evidence/<id>.out and evidence/control.out hold suite output only (Read08-10). Say stdout.",
        "Lines 854-856 say six survivor classes. The mado note says same six survivors (corpus/knowledge/mutation-case-mado-verify.md:187-188; Read08-2). The 10/10 verdict claim matches :73 and :187-189.",
        "The evidence list (lines 851-852) omits defects.tsv (:507) and evidence/control.out (:525). The list is incomplete, not wrong."
      ],
      "commands_executed": [
        "python3 -c import re,sys,hashlib;p=sys.argv[1];d=open(p,'rb').read();print('sha256',hashlib.sha256(d).hexdigest(),'lines',d.count(b'\\n'));pat=re.compile(sys.argv[2]);[print(i,l) for i,l in enumerate(d.decode('utf-8','replace').splitlines(),1) if pat.search(l)] tools/mutate-and-run.sh ^[A-Za-z_][A-Za-z0-9_]*\\(\\) *\\{|SETUP|MUTATE_RESTORE|DEGRADED|MUTATE_TOOL|MUTATE_EVIDENCE|MUTATE: DONE|KILLED|INCONCLUSIVE|SURVIVED|124|126|127|mktemp|--workdir|--suite\\)|--target\\)|--defects\\)",
        "python3 -c import re,sys;L=open(sys.argv[1],encoding='utf-8').read().splitlines();print('lines',len(L));sel=set(i for a,b in [(1,30),(55,80),(180,196)] for i in range(a,b+1));pat=re.compile(r'597e1419|ff6331b|1001|10/10|predict|pre-?regist|survivor class|MUTATE_TOOL');sel|=set(i for i,l in enumerate(L,1) if pat.search(l));[print(i,L[i-1]) for i in sorted(sel)] corpus/knowledge/mutation-case-mado-verify.md",
        "bash -c for c in $(git log --format=%H -- tools/mutate-and-run.sh); do printf \"%s sha256=%s lines=%s\\n\" \"$c\" \"$(git show \"$c:tools/mutate-and-run.sh\" | sha256sum | cut -c1-64)\" \"$(git show \"$c:tools/mutate-and-run.sh\" | wc -l)\"; done; git cat-file -t 597e1419 2>&1; true",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/work/gate.sh --defects /tmp/Read08-8spe/work/spec.txt --suite bash \"$MUTANT\" --selftest --workdir /tmp/Read08-8spe/work/run1",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/work/gate.sh --defects /tmp/Read08-8spe/work/dup.txt --suite bash \"$MUTANT\" --selftest --workdir /tmp/Read08-8spe/work/run2",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/work/gate.sh --defects /tmp/Read08-8spe/work/same.txt --suite bash \"$MUTANT\" --selftest --workdir /tmp/Read08-8spe/work/run3",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/work/gate.sh --defects /tmp/Read08-8spe/work/spec.txt --suite exit 1 --workdir /tmp/Read08-8spe/work/run4",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/work/gate.sh --defects /tmp/Read08-8spe/work/spec.txt --suite case \"$DEFECT_ID\" in D2) exit 127 ;; D3) exit 124 ;; esac; bash \"$MUTANT\" --selftest --workdir /tmp/Read08-8spe/work/run5",
        "python3 -c import sys,hashlib;p=sys.argv[1];L=open(p,'rb').read().decode('utf-8','replace').splitlines();print('sha256',hashlib.sha256(open(p,'rb').read()).hexdigest(),'lines',len(L));[print(i,L[i-1]) for a,b in [(236,300),(450,600),(1985,2016)] for i in range(a,b+1)] tools/mutate-and-run.sh",
        "bash -c cd /tmp/Read08-8spe/work/run1 && find . | sort && echo ---- && cat results.tsv && echo ---- && cmp spec.copy /tmp/Read08-8spe/work/spec.txt && echo SPEC_COPY_IDENTICAL && echo ---- && for f in $(find . -name \"*.out\" | sort); do echo \"== $f\"; head -c 300 \"$f\"; echo; done",
        "python3 -c import sys,hashlib;p=sys.argv[1];d=open(p,'rb').read();L=d.decode('utf-8','replace').splitlines();print('sha256',hashlib.sha256(d).hexdigest(),'lines',len(L));[print(i,L[i-1]) for a,b in [(160,200),(312,450)] for i in range(a,b+1)] tools/mutate-and-run.sh",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/work/gate.sh --defects /tmp/Read08-8spe/work/spec.txt --suite bash \"$MUTANT\" --selftest --workdir /tmp/Read08-8spe/work",
        "bash -c cd /tmp/Read08-8spe/work/run1 && for m in mutant-*; do echo \"== $m\"; diff pristine.gate.sh \"$m\"; done; true",
        "python3 -c import sys,hashlib,re;p=sys.argv[1];d=open(p,'rb').read();L=d.decode('utf-8','replace').splitlines();print('sha256',hashlib.sha256(d).hexdigest(),'lines',len(L));[print(i,L[i-1]) for a,b in [(1,3),(54,56),(68,70),(1001,1003)] for i in range(a,b+1)] tools/trace-inputs.py",
        "bash tools/mutate-and-run.sh --target /tmp/Read08-8spe/collide/results.tsv --defects /tmp/Read08-8spe/work/spec.txt --suite bash \"$MUTANT\" --selftest --workdir /tmp/Read08-8spe/collide",
        "python3 -c import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));s=d['sections'][0];print('schema',d['schema'],'seat',d['seat'],'rev',d['read_rev'],'sections',len(d['sections']));print('verdict',s['verdict'],'class',s['class'],'start',s['start']);print('commands',len(s['commands_executed']),'traces',len(s['traces']),'opened',len(s['opened']),'inputs',len(s['inputs']));print('opened==inputs keys', sorted(s['opened'])==sorted(s['inputs']));print('blocking',len(s['blocking_gaps']),'wrong',len(s['wrong_expectations']),'minor',len(s['minor_gaps']));print('trace names ok', [t.rsplit('/',1)[1] for t in s['traces']]==['Read08-%d.json' % i for i in range(1,16)])" /tmp/Read08-8spe/work/report.json"
      ],
      "opened": [
        "tools/mutate-and-run.sh",
        "tools/trace-inputs.py",
        "corpus/knowledge/mutation-case-mado-verify.md"
      ],
      "inputs": {
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3"
      },
      "external_inputs": {
        "tameshi-shokunin@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh": "597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b",
        "tameshi-shokunin@a08e85c5d7f899e8a5992e20517edb1a380d79eb:tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read08-16.json"
      ]
    }
  ]
}
```

## Note: what I checked

Setup. Detached fleet-mirror clone at 2227d83 under /tmp/Read08-8spe. Its SKILL.md sha256 matches the assignment (386de44b...51e95). The section runs from line 827 to line 857; line 858 starts the next heading, "### The boundaries — what a service run is not". The bash fence at lines 833-836 holds no heading. Class: instruction, because it tells the reader to run tools/mutate-and-run.sh in ordered steps.

Named command. I ran the command the section names (Read08-4) against a fixture gate and a three-defect spec in /tmp/Read08-8spe/work, outside the clone. Output: CONTROL GREEN; D1 KILLED (exit 1); D2 SURVIVED (exit 0); D3 KILLED (exit 1); MUTATE_RESTORE: OK; MUTATE: DONE (killed=2 survived=1 inconclusive=0 kill-rate=67%); exit 0.

Protocol steps. Each step matched the code in tools/mutate-and-run.sh and the runs.
- Step 1 (lines 838-839): the pristine copy is WORKDIR/pristine.<name> (:489-490). Each mutant is a fresh cp of the pristine (:514), and each differs from the pristine in exactly one line (Read08-13). Target sha unchanged in Read08-4 and Read08-12.
- Step 2 (lines 840-842): every defect is applied before any suite run (:511-522). Read08-5 (duplicate @old) printed "APPLY FAIL id=E1 line=1 old-string-count=4 expected=1", then "MUTATE: SETUP (spec/preparation failed for 1 defect(s); no suite run)", exit 2, with no CONTROL line. Read08-6 (@new equal to @old) printed "MUTATE: SETUP (spec parse failed)", exit 2.
- Step 3 (lines 843-844): Read08-7 (suite exit 1) printed CONTROL: RED and SETUP "cannot attribute kills", exit 2. The control runs before the mutant loop (:525 before :538).
- Step 4 (lines 845-846): Read08-8 (suite exits 127 and 124 for two defects) gave INCONCLUSIVE with notes suite-not-found and timeout, then DEGRADED, exit 1.
- Step 5 (lines 847-848): Read08-4 printed MUTATE_RESTORE: OK. Read08-15 printed DRIFT.
- Step 6 (lines 849-852): DONE and exit 0 (Read08-4); DEGRADED and exit 1 (Read08-8); MUTATE_EVIDENCE printed. Read08-10 lists defects.tsv, evidence/control.out, evidence/D1.out to D3.out, mutant-D1 to D3, pristine.gate.sh, results.tsv and spec.copy; spec.copy is byte-identical to the spec.
- Mado citations: corpus/knowledge/mutation-case-mado-verify.md:73 says the pre-registration held 10/10 on verdicts, and :187-189 record predictions written before the sweep. Both match.

The failing item. Lines 829-831 name the pinned harness as the mado run's revision 597e1419…ff6331b, 1001 lines. That history is accurate: commit b58b26fb… holds those bytes (Read08-3). But at 2227d83 the path holds sha fb91ef76…, 2016 lines (Read08-1, Read08-9), and every run prints that sha (Read08-4). A reader who follows the paragraph expects a harness the path does not supply, and no step says how to fetch the older bytes. The wrong expectation is the pin identity, not the protocol.

Negative and edge paths. Read08-15 ran with the target named results.tsv inside --workdir. The harness overwrote the target, the restore check reported DRIFT, and the run ended with SETUP and exit 2. Read08-12 ran with --workdir equal to the target's directory and no name clash, and it ended DONE with the target unchanged. So the hazard is a name clash, not sharing a directory.

Smallest safe correction (for the owner; I edited nothing):
1. Name fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de (2016 lines) as the pin the path delivers at 2227d83. Move 597e1419…ff6331b (1001 lines) into a historical sentence with its git show command.
2. Define KILLED as exit not 0, 124, 126 or 127.
3. Reword the workdir clause to describe the name-clash overwrite and state that the harness detects it after writing and does not restore the target.
4. Add the DRIFT outcome (SETUP, exit 2, no headline) to step 5.
5. In the opening paragraph (lines 830-831), say the MUTATE_TOOL pin is on the run's stdout.
6. Change "survivor classes" to "survivors".

Verification gaps.
- I did not run the ten-defect mado sweep. The fixture used the section's command shape, not the mado target.
- DRIFT was reached only through a name clash, not a concurrent edit. The timeout branch was reached through the suite's own exit codes 124 and 127, not a 300-second timeout.
- Only results.tsv was tested as a clash name. defects.tsv and spec.copy follow the same code path and are untested.
- SKILL.md was read by hand from the clone. Its hash was checked untraced at setup. Receipts do not list SKILL.md, and the inputs field omits it as the assignment requires.

Untraced commands (not in commands_executed; no receipts).
- (a) The prescribed clone and symlinks, the detached checkout, the rev-parse, and a sha256sum of SKILL.md. The clone reads the live lane, and a trace must not read it.
- (b) A probe of sha256sum, wc, ls, git log and git status on the clone. Its hash and line-count facts are re-derived under Read08-1 and Read08-14. The git status probe printed no lines and was not re-derived.
- (c) A version probe for strace, python3, uv and git. The traces show strace working.

Other disclosures. I read the receipts with the read tool after the traces finished, to take exit codes and argv. They are outputs, not inputs. No lane file was read during a trace; live_lane_reads is empty in every receipt. I did not open SCORECARD.md, LOG.md or ledger.json. I wrote no lane file except this report and the traces. Read08-16 parsed a scratch copy of the JSON block (15 commands, before the Read08-16 entries were added) and confirmed its structure; the Read08-16 entries were then added to the two lists above.

Tooling. No installs or upgrades. Existing tools used: strace 7.2, git 2.56.0, Python 3.14.8. uv is present but unused. I did not read RULES.md because nothing was installed.

COLDREAD Read08: wrong-expectation
