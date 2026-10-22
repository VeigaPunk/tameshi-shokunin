# ReRead06 cold read: SKILL.md:883-898

Section: "### The report shape — what the opting-in lane receives" (start 883; the next heading, "### The mado run", is at 899).
Read revision: b1cc95e1fb62532646d74e2863770c4fed0851cc. SKILL.md sha256: fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f.

Class: record. Verdict: wrong-expectation. Blocking gaps: none.

## Verdict

The section is accurate except for one clause. It says the tool does not print target size. It does: `tools/mutate-and-run.sh:497` prints `bytes=` on the `MUTATE_TARGET` line. So the section asks the lane to supply a value the tool already prints. Under the cold-read rules this keeps the section uncovered. The other checkable claims hold, apart from the minor wording gaps listed below. The smallest correction is one phrase.

## Evidence

Line numbers are newline counts from the trace receipts. Receipts are named `ReRead06-<n>`.

1. Wrong expectation, SKILL.md:885-886. The text reads "supplied by the lane in the note (the tool does not print them): target size/lines, suite command, spec clause map". The tool's line `printf 'MUTATE_TARGET: %s sha256=%s bytes=%s\n'` (tools/mutate-and-run.sh:497) prints the byte size. A toy run under the collector printed `MUTATE_TARGET: /tmp/ReRead06-OqQr/scratch/toy.sh sha256=043449c4… bytes=393` (ReRead06-18). The mado-run revision, `597e1419…`, which is commit `b58b26fb` (ReRead06-25), prints the same field (ReRead06-23). The tool prints no line count. The note gives a line count, "1099-line" at note line 37 (ReRead06-14). Its only byte figure is 46850 B for the tool itself, at note line 21, so the note never gives the target's byte size. If "size" was meant as line count only, the claim holds and the fix is a wording change.
2. Holds: pins printed by the tool, SKILL.md:885. `MUTATE_TOOL: … sha256=` (tools/mutate-and-run.sh:495), `MUTATE_TARGET: … sha256=` (:497) and `CONTROL: GREEN (… pristine-sha256=…)` (:533). The toy run shows all three (ReRead06-18).
3. Holds: suite command and clause map, SKILL.md:886. `$SUITE` runs the suite at :454 and is only checked or parsed elsewhere (:468, :1344, :1998); no printf emits it (ReRead06-15). `MUTATE_SPEC` prints the spec path and the defect count only (:506). The note gives the suite command at note line 52.
4. Holds: kill-rate rows, SKILL.md:887-889. Each row is `DEFECT <id>: <verdict> (exit=… duration-ms=…) <desc>` (:550). Tail lines of `evidence/<id>.out` follow each row (:300-308 and :551), and the file is written at :541. The toy file `evidence/D1.out` contains the same label the tool printed as a tail, `A: greeting check (got 'hullo' want 'hello')` (ReRead06-19).
5. Holds: restore proof, SKILL.md:893-894. `MUTATE_RESTORE: OK (target-sha256 before=… after=… pristine-sha256=…)` is printed at :563-564 (ReRead06-18). The run path (:460-577) makes no git or status call (ReRead06-15), so the tool emits no tree-clean check.
6. Holds: probe citations, SKILL.md:890-892. Note lines 103-115 are the §2 intro and table. Line 110 is P3 and line 113 is P8, and both are "clean fixture" rows. Lines 274-275 define `probe/fixture-A` as the suite's own clean fixture (ReRead06-5, -6). That matches the section's exception.
7. Holds: only fleet file, SKILL.md:895-896. Note lines 8-9 say "this note is the only fleet file written by this run" (ReRead06-5, -6).
8. Holds: reproduce block, SKILL.md:896. §9 starts at note line 262, and the commands fence runs 279-293. Line 285 names the live target `mado-shokunin/tools/mado-verify.sh`, so the block replays whatever is live, not the pin. Rows D1, D3, D6, D7 and R1 (note lines 299, 301, 304, 305, 308) carry `…` elisions; D2, D4, D5, D8 and D9 are whole (ReRead06-13). That is 5 of 10, as stated.
9. Holds: spec under /tmp gone, SKILL.md:897. On this host `/tmp/w6-tameshi-mado-verify`, its spec file and `sweep/evidence` all report absent (ReRead06-12).
10. Ambiguous, not wrong, SKILL.md:897 "corrected in round 27". The SKILL.md page has a round-27 commit, `b1cc95e` ("SKILL corrections of the 12 sections the cold reads failed"; ReRead06-17). The note has one commit, `4494715`, from 2026-10-14 (ReRead06-11). So the note was not changed in round 27; the wording about its limits was. The seat name "Read10" lives in the round-21 ledger, which this seat may not open.

## Smallest safe correction

- SKILL.md:886: replace "target size/lines" with "target line count". Optionally add: "byte size is already on the MUTATE_TARGET line."

If "size" was meant as line count only, the claim holds and the replacement is only a clarity fix. As written, it reads as byte size, and the tool prints bytes.

Optional clarity fixes, none of which changes the verdict:
- SKILL.md:889: "the edit site comes from the spec" becomes "the @old anchor comes from the spec; any :NNN line numbers come from the lane, because the tool prints neither."
- SKILL.md:894: add the pointer "(SKILL.md:375-403, Restore discipline)".
- SKILL.md:897: say which file the round-27 correction touched (the SKILL.md wording, commit b1cc95e).

## Residual risk and verification gaps

- The mado evidence directory is absent on this host (ReRead06-12). The failing labels and kill rows in the mado table cannot be compared with source files here. The mechanism is confirmed only by a toy target (ReRead06-18, -19).
- The read tool numbers this note two lines higher than newline counting: its "Run date" line shows as 5, and the file has it on 3. Every citation here uses the newline counts from the receipts, which match the section's own citations.
- "round-18 correction" and seat "Read10" cannot be reached by path from the section. The lane ledger and LOG are off-limits to this seat.
- Commands before the collector: the clone (assignment step 1) and my first exploratory reads (awk, sed, sha256sum, git rev-parse) ran before the collector. The same reads were repeated under it (ReRead06-2, -3, -4), and every receipt records rev b1cc95e1. The early commands have no receipts, so they are left out of commands_executed.

## Residual observations for the lane (not defects in this section)

- Note line 104 says each probe "constructs an input the suite's fixtures do not". P3 (line 110) and P8 (line 113) use the suite's own clean fixture, so line 104 is wrong for those two rows. SKILL.md:891-892 handles this correctly.
- The note header (lines 1-23) records no pre-sweep `git status`, substrate size, mtime or revision. SKILL.md:380-382 asks for all four (ReRead06-24).

## Tooling

No tools were installed or upgraded. The harness tool ran only inside my /tmp clone and only against a two-defect toy target in /tmp/ReRead06-OqQr/scratch. No command ran in the live lane. Receipts went only to the coldread traces directory. Nothing in the lane was edited.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ReRead06",
  "skill_sha256": "fce549773fe4eb82111f16199d059cd9c7ef46495633a71f441b46b7b981924f",
  "read_rev": "b1cc95e1fb62532646d74e2863770c4fed0851cc",
  "sections": [
    {
      "start": 883,
      "heading": "### The report shape — what the opting-in lane receives",
      "class": "record",
      "verdict": "wrong-expectation",
      "blocking_gaps": [],
      "wrong_expectations": [
        "SKILL.md:885-886 says the tool does not print target size, so the lane must supply 'target size/lines' in the note. tools/mutate-and-run.sh:497 prints 'MUTATE_TARGET: <path> sha256=<sha> bytes=<N>'; the toy run printed bytes=393 (ReRead06-18). The mado-run revision 597e1419 (commit b58b26fb) prints the same bytes= field (ReRead06-23, ReRead06-25). The tool prints no line count. Smallest fix: write 'target line count' and note that byte size is already on the MUTATE_TARGET line."
      ],
      "minor_gaps": [
        "SKILL.md:889 says the edit site comes from the spec. The spec's @old text identifies the site, but the :NNN line numbers in the mado table (note lines 299-308) appear in neither the tool output nor the embedded spec (tools/mutate-and-run.sh:790-835). The lane adds them; say so.",
        "SKILL.md:894 cites 'round-18 correction' with no path. SKILL.md:375-403 (Restore discipline, before/after identity) states the same policy and is the nearest pointer; add it.",
        "SKILL.md:897 says the reproduce block was 'corrected in round 27'. Read literally that describes the note, but the note has one commit (4494715, 2026-10-14; ReRead06-11). The round-27 change is the SKILL.md wording (b1cc95e; ReRead06-17). Seat Read10 lives in the round-21 ledger, which this seat may not open, so that part stays unverified.",
        "SKILL.md:887-888 lets a clause label reach a kill-rate row, but the tool prints a clause only when the spec description carries one (toy DEFECT line 'clause A: ...', ReRead06-18). The clause map itself is never printed. Say that the row clause comes from the spec text."
      ],
      "commands_executed": [
        "python3 -c import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]] corpus/knowledge/mutation-case-mado-verify.md",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,repr(L[i-1])) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] SKILL.md 881-901",
        "sha256sum SKILL.md",
        "python3 -c import sys,re;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');pat=re.compile(sys.argv[2]);print('split_lines',len(L));[print(i,L[i-1]) for i in range(1,len(L)+1) if pat.search(L[i-1])] SKILL.md ^\u0060\u0060\u0060|^#{1,3} |temporary shell|session variables|nothing set here",
        "python3 -c import sys,re;p=sys.argv[1];t=open(p,encoding='utf-8').read();L=t.split('\\n');print('split_lines',len(L),'final_newline',t.endswith('\\n'));print('specials',[(c,t.count(c)) for c in ['\\r','\\x0b','\\x0c','\\x1c','\\x1d','\\x1e','\\x85','\\u2028','\\u2029']]);pat=re.compile(sys.argv[2]);[print(i,L[i-1]) for i in range(1,len(L)+1) if pat.search(L[i-1])] corpus/knowledge/mutation-case-mado-verify.md fixture|only fleet|fleet file|spec under|elided|Read10|round-18|round 27|round-27|/tmp|MUTATE_RESTORE|Reproduce|reproduce|sweep.log",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] corpus/knowledge/mutation-case-mado-verify.md 1-12 40-70 96-124 255-300",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] tools/mutate-and-run.sh 1-250",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] tools/mutate-and-run.sh 251-500",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] tools/mutate-and-run.sh 501-750",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] tools/mutate-and-run.sh 751-1000",
        "git log --format=%h_%ad_%s --date=short -- corpus/knowledge/mutation-case-mado-verify.md",
        "python3 -c import os;[print(p,os.path.exists(p)) for p in ['/tmp/w6-tameshi-mado-verify','/tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec','/tmp/w6-tameshi-mado-verify/sweep/evidence','/tmp/w5-mado-m52-selftest']]",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] corpus/knowledge/mutation-case-mado-verify.md 296-312",
        "python3 -c import sys,re;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');pat=re.compile(sys.argv[2]);print('split_lines',len(L));[print(i,L[i-1]) for i in range(1,len(L)+1) if pat.search(L[i-1])] corpus/knowledge/mutation-case-mado-verify.md bytes|1099|size|[0-9] B\\b|mado-verify.sh.*sha|sha256",
        "python3 -c import sys,re;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');pat=re.compile(sys.argv[2]);print('split_lines',len(L));[print(i,L[i-1]) for i in range(1,len(L)+1) if pat.search(L[i-1])] tools/mutate-and-run.sh SUITE|MUTATE_[A-Z]+|CONTROL:|DEFECT |tree|git status|MUTATE_TARGET|bytes=",
        "python3 -c import sys;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');print('split_lines',len(L));[print(i,L[i-1]) for s in sys.argv[2:] for i in range(int(s.partition('-')[0]),min(int(s.partition('-')[2] or s.partition('-')[0]),len(L))+1)] SKILL.md 375-404",
        "git log --format=%h_%ad_%s --date=short -6 -- SKILL.md",
        "bash tools/mutate-and-run.sh --target /tmp/ReRead06-OqQr/scratch/toy.sh --defects /tmp/ReRead06-OqQr/scratch/toy.spec --suite bash \"$MUTANT\" --selftest --workdir /tmp/ReRead06-OqQr/scratch/work --label toy --tail 3",
        "python3 -c import sys;[print('==',p,'\\n'+open(p,encoding='utf-8').read()) for p in sys.argv[1:]] /tmp/ReRead06-OqQr/scratch/work/evidence/D1.out /tmp/ReRead06-OqQr/scratch/work/evidence/control.out /tmp/ReRead06-OqQr/scratch/work/results.tsv",
        "sha256sum tools/mutate-and-run.sh corpus/knowledge/mutation-case-mado-verify.md",
        "sha256sum /tmp/ReRead06-OqQr/scratch/toy.sh /tmp/ReRead06-OqQr/scratch/toy.spec",
        "python3 -c import subprocess,hashlib;g=lambda *a:subprocess.run(['git',*a],capture_output=True).stdout;revs=g('log','--format=%H','--','tools/mutate-and-run.sh').decode().split();[print(r[:8],hashlib.sha256(g('show',r+':tools/mutate-and-run.sh')).hexdigest()[:16],b'bytes=%s' in g('show',r+':tools/mutate-and-run.sh'),[l for l in g('show',r+':tools/mutate-and-run.sh').decode('utf-8','replace').split('\\n') if l.startswith('VERSION=')][:1]) for r in revs]",
        "python3 -c import subprocess;[print(r,[l for l in subprocess.run(['git','show',r+':tools/mutate-and-run.sh'],capture_output=True,text=True).stdout.split('\\n') if 'MUTATE_TARGET:' in l and 'printf' in l]) for r in ['b58b26fb','53e74a89','a08e85c5']]",
        "python3 -c import sys,re;p=sys.argv[1];L=open(p,encoding='utf-8').read().split('\\n');pat=re.compile(sys.argv[2]);print('split_lines',len(L));[print(i,L[i-1]) for i in range(1,len(L)+1) if pat.search(L[i-1])] corpus/knowledge/mutation-case-mado-verify.md mtime|porcelain|git status|repo revision|git rev|revision",
        "python3 -c import subprocess,hashlib;g=lambda *a:subprocess.run(['git',*a],capture_output=True).stdout;revs=g('log','--format=%H','--','tools/mutate-and-run.sh').decode().split();[print(r,hashlib.sha256(g('show',r+':tools/mutate-and-run.sh')).hexdigest()) for r in revs]",
        "sha256sum /tmp/ReRead06-OqQr/scratch/work/evidence/D1.out /tmp/ReRead06-OqQr/scratch/work/evidence/control.out /tmp/ReRead06-OqQr/scratch/work/results.tsv"
      ],
      "opened": [
        "corpus/knowledge/mutation-case-mado-verify.md",
        "tools/mutate-and-run.sh"
      ],
      "inputs": {
        "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de"
      },
      "external_inputs": {
        "/tmp/ReRead06-OqQr/scratch/toy.sh": "043449c4775d5bb086a72f1c3baad37baa983a39f50fec2a93012f8190acc2b5",
        "/tmp/ReRead06-OqQr/scratch/toy.spec": "73d3310a6745d5066417c99e0fae6ead0d5d6a927503689548f50c6ab0277736",
        "/tmp/ReRead06-OqQr/scratch/work/evidence/D1.out": "88a7db1afb5573297afb1a765d732ee3559106a3c34be5c80b96b977712ec4d2",
        "/tmp/ReRead06-OqQr/scratch/work/evidence/control.out": "af31f06c477026a8e3b2167b165f2ceb66f16e38ccae30c6a3dea03c25aae982",
        "/tmp/ReRead06-OqQr/scratch/work/results.tsv": "c545ca17b6a6f3a0a58f2feeee2b790ab7536a251caeb4336ea6f9c0e4fd0da3",
        "tameshi-shokunin@a08e85c5d7f899e8a5992e20517edb1a380d79eb:tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tameshi-shokunin@58e5d53d6a638fb72042d1f6607b24018aa299a8:tools/mutate-and-run.sh": "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b",
        "tameshi-shokunin@2a22adeb7d1de5e7189e62ce41ac679d71a97b44:tools/mutate-and-run.sh": "fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a",
        "tameshi-shokunin@05a224754db3c6fce18f5ec1816a6873bffe3d0e:tools/mutate-and-run.sh": "0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa",
        "tameshi-shokunin@c699c8c36d6e4eca4b796b81a8247904aa145ec8:tools/mutate-and-run.sh": "89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594",
        "tameshi-shokunin@606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
        "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
        "tameshi-shokunin@44947154c23772f766f9f5439090fb5c7ad76e46:tools/mutate-and-run.sh": "b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb",
        "tameshi-shokunin@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh": "597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b",
        "tameshi-shokunin@53e74a890c70fdcb97487eadb67c2e36faf7bb7b:tools/mutate-and-run.sh": "d8abee522efbf27c3570acd68d7bc4b9dd30a3888f6e9c2359020e179a7eda68"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-13.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-14.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-15.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-16.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-17.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-18.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-19.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-20.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-21.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-22.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-23.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-24.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-25.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/ReRead06-26.json"
      ]
    }
  ]
}
```

## What I checked

I read the section (SKILL.md:883-898) and the mado note it cites, under the trace collector. I then read the harness tool that the section describes (tools/mutate-and-run.sh, 2017 lines) and checked each claim about its printed output against its source. I ran the tool once on a two-defect toy target in /tmp to see its real output. I checked each line citation by newline count, went through the reproduce block row by row, and checked the spec path and the note history with receipts. One claim is wrong: target byte size. The rest hold, with the wording gaps and residual observations listed above.

COLDREAD ReRead06: wrong-expectation
