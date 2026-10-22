# Read09 cold read: SKILL.md "### The boundaries — what a service run is not" (lines 858-882, revision 2227d8338c02aa9a5fd7d95c1a41b76865ad7647)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read09", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 858, "heading": "### The boundaries \u2014 what a service run is not", "class": "record", "verdict": "gap-blocking",
  "blocking_gaps": [
   "SKILL.md:864-866 Read-only bullet: the clause 'the sibling tree stays porcelain-clean' is not in its cited span corpus/knowledge/mutation-case-mado-verify.md:57-59. Those lines hold the control line, the MUTATE_RESTORE sha pair, and 'the fleet file was re-hashed after the probes too: unchanged'. The mado note has no porcelain, git-status, or tree-clean measurement (grep of the note; its reproduce block at :281-293 runs sha256sum only). The sweep path of tools/mutate-and-run.sh makes no git call (receipt 8: git appears only in helpers at :260-297, regression materialization at :1152-1228 and :1330-1424, and self-test canaries at :1727-1897). The protocol restore re-check covers the target sha alone (SKILL.md:847-848), and the report shape says the tool emits no separate tree-clean check, round-18 correction (SKILL.md:893-894). The only porcelain-clean claim for the mado run on the page is SKILL.md:916-917, which cites an external scratch file, /tmp/w6-aud-t6-work/presweep-174248.txt. I did not open that file, and this bullet does not cite it.",
   "SKILL.md:865-866 Read-only bullet: the clause 'the provable negative is the service's writes never touched the gate' is not in its cited span. The mado note lacks the phrase, and :57-59 supports endpoint sha identity only. The page's restore discipline says before/after fingerprints establish 'endpoint identity, not that no transient write occurred' (SKILL.md:377-378). The phrase appears adapted from the tsukuroi case (SKILL.md:692-693, 'this lane's writes never touched the substrate') [I]. A design basis exists at 2227d83 but the section does not cite it: every TARGET token in tools/mutate-and-run.sh is a read (:476, :488, :490, :556, :558), mutants are written only under $WORKDIR (:513, :540), and the header says 'The target is never written' (:36-38). [INFERENCE: token grep, not a full dataflow proof.] The mado run used tool 597e1419 (SKILL.md:829-831; mado note :17-19), which I did not locate in lane history, so the design basis is verified only for 2227d83."
  ],
  "wrong_expectations": [],
  "minor_gaps": [
   "Bullet 1: 'matrix row F' names no file. Row F lives in corpus/knowledge/arm-class-matrix.md (table :44; section 7 at :206-215; admission table :242) and in the page's matrix table (SKILL.md:728). The claim itself checks out.",
   "Bullet 1: 'a rate is bounded by its defect vocabulary' has no pointer. Page support is SKILL.md:248 ('The classes are the injection vocabulary').",
   "Bullet 4: 'the first point below the 50-80 band' is cited to mado :66-72, which does not contain it. The statement is at mado :175-176 and in ledger :138.",
   "Bullet 4: 'a low kill rate is a report, not a service failure' has no pointer. Page support is SKILL.md:335 ('Bands are a report convention, not a pass/fail gate').",
   "Bullet 4: 'a survivor is a gap named with its class' is not in the cited span. The classes are at mado :101-147.",
   "Bullet 7: the cited range :229-230 starts one line after the U2 statement, which begins at :228."
  ],
  "commands_executed": [
   "python3 -c \"import sys;[print(f'{n}|{l}') for p in sys.argv[1:] for n,l in enumerate(open(p).read().splitlines(),1)]\" corpus/knowledge/mutation-case-mado-verify.md",
   "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(f'{n}|{l}') for n,l in enumerate(L,1) if l.startswith('#') or 276<=n<=304]\" corpus/knowledge/fleet-suite-census.md",
   "python3 -c \"import sys;[print(f'{n}|{l}') for p in sys.argv[1:] for n,l in enumerate(open(p).read().splitlines(),1)]\" corpus/knowledge/fleet-kill-rate-ledger.md",
   "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(f'{n}|{l}') for n,l in enumerate(L,1) if n<=40 or 'VERSION=' in l]\" tools/mutate-and-run.sh",
   "python3 -c \"import sys;[print(f'{n}|{l}') for p in sys.argv[1:] for n,l in enumerate(open(p).read().splitlines(),1)]\" corpus/knowledge/arm-class-matrix.md",
   "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(f'{n}|{l}') for n,l in enumerate(L,1) if 'porcelain' in l or 'MUTATE_TOOL' in l or 'REGRESSION_TOOL' in l or 'git status' in l or 'tree-clean' in l or 'RESTORE' in l]\" tools/mutate-and-run.sh",
   "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(f'{n}|{l}') for n,l in enumerate(L,1) if 'TARGET' in l]\" tools/mutate-and-run.sh",
   "python3 -c \"import sys;L=open(sys.argv[1]).read().splitlines();[print(f'{n}|{l}') for n,l in enumerate(L,1) if 'git' in l]\" tools/mutate-and-run.sh",
   "sha256sum corpus/knowledge/mutation-case-mado-verify.md corpus/knowledge/fleet-suite-census.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/arm-class-matrix.md tools/mutate-and-run.sh tools/trace-inputs.py"
  ],
  "opened": [
   "corpus/knowledge/mutation-case-mado-verify.md",
   "corpus/knowledge/fleet-suite-census.md",
   "corpus/knowledge/fleet-kill-rate-ledger.md",
   "corpus/knowledge/arm-class-matrix.md",
   "tools/mutate-and-run.sh",
   "tools/trace-inputs.py"
  ],
  "inputs": {
   "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
   "corpus/knowledge/fleet-suite-census.md": "ec1c2d8d2877a21df9752a7b20e6c307a144442a583ec6e6e03349d98ac94e4f",
   "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
   "corpus/knowledge/arm-class-matrix.md": "bd4f4a02eb66f4e25e67a1518108d1f11c45b4edf2355d1901ec54ce55359088",
   "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
  },
  "external_inputs": {},
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read09-9.json"
  ]}]}
```

Verdict: gap-blocking. Class: record. The section states boundaries with pointers and tells no reader to run anything. Six of its seven bullets check out against what I opened. The Read-only bullet does not. Two of its three clauses are not in the span it cites, and the porcelain-clean clause describes a state the run never checks or emits.

Checked and verified:
- Bullet 2, hermetic suites only: census :288-291 matches. Those lines sit inside section 5 (heading :249, next heading :293).
- Bullet 1, single-edit mutants, row F unmeasured: confirmed in arm-class-matrix.md (:44, :206-215, :242) and in SKILL.md:728.
- Bullet 4, 40 % and composition: mado :60-61 (4/10), :66-72 (4 in-surface at 4/4, 6 out-of-surface at 0/6).
- Bullet 5, recommendations only: mado :237-238 (U6) and :240-260 (section 8).
- Bullet 6, harness pinned per run and the re-pin: mado :17-23 (re-pin b56c6e57...2bcb). The tool prints MUTATE_TOOL with its sha256 at :495 and REGRESSION_TOOL at :1368 (receipt 6).
- Bullet 7, sensitivity not truth: mado :228-230 (U2).
- Bullet 3, first clause only: target sha before equals after (mado :57-59, MUTATE_RESTORE OK).

Failed:
- The porcelain-clean clause (blocking gap 1). The cited span has no porcelain evidence, the sweep path runs no git call, and the page says the tool emits no tree-clean check.
- The provable-negative clause (blocking gap 2). The cited span does not contain it, and the restore discipline limits what fingerprints can prove.

Smallest safe correction:
- Rewrite bullet 3 as: "target sha before = after (MUTATE_RESTORE, SKILL.md:847-848; mutation-case-mado-verify.md:57-59). The run makes no git call and emits no tree-clean check (SKILL.md:893-894). Porcelain-clean is an opt-in precondition at open (SKILL.md:808-809), not a run receipt. The no-write-to-target design is stated in the tool header (tools/mutate-and-run.sh:36-38). Fingerprints establish endpoint identity only (SKILL.md:377-378)."
- Name corpus/knowledge/arm-class-matrix.md for row F. Cite mado :175-176 for the first point below the band. Cite SKILL.md:335 for "a report, not a service failure". Cite mado :101-147 for the classes. Start the U2 cite at :228.
- Reader expectation: a reader who believes a service run certifies a porcelain-clean sibling tree, or proves that no write touched the gate, will find neither in the run's own receipt. The receipt carries the sha pair only.

Setup and non-collector steps (not in commands_executed; none read section evidence):
- Clone and detached checkout from the lane at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, with GIT_OPTIONAL_LOCKS=0. The sibling symlinks and the clone live under /tmp/Read09-zTuN.
- SKILL.md sha256 check: 386de44b... matches.
- Version checks: strace 7.2 at /usr/bin/strace, Python 3.14.8, git 2.56.0.
- wc -l on the cited files, and a read-only listing of the traces folder.
- Receipts 1-9 were read back after the traces finished.
- No tools were installed or updated.

Monitor-named inputs: fleet-kill-rate-ledger.md (receipt 3, sha 13a11e46...) and tools/mutate-and-run.sh (receipts 4, 6, 7, 8, and the hash in 9, sha fb91ef76...) were opened under the collector. Ledger :138-141 and :153-158 agree with bullets 1, 2, 4, and 7. Ledger :352 (sibling trees clean) describes the ER-4 tick, not the mado run.

Residual risk and verification gaps:
- The mado run's tool (597e1419..., SKILL.md:829-831) was not located in lane history. The design claim is verified at 2227d83 only.
- The TARGET token grep is not a full dataflow proof.
- The scratch file cited at SKILL.md:916-919 belongs to another lane and was not opened.
- No sibling-repo state was checked. Sibling trees have moved since 2026-10-14 (ledger ER-1), so they cannot evidence the mado run.
- No harness or suite was run. The section is a record and contains no instruction to run.

COLDREAD Read09: gap-blocking
