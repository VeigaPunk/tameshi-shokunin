# Read05 — cold read of SKILL.md:375-404

**Verdict: gap-minor.** Class: `instruction`.

Section: `## Restore discipline — before/after identity, not continuous non-write proof` at SKILL.md:375. It runs to :404; the next heading is `## Cross-language divergence` at :405. There are no code fences inside the section. Read rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. The fleet-mirror clone is detached there, and its SKILL.md sha256 is 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95, which matches.

## Evidence

- **Named regression, run under the collector (Read05-3):** `bash tools/mutate-and-run.sh --regression` exited 0 and printed `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`. The two legs the section names both replayed exactly: `REGRESSION_CASE js-kimi-census: PASS` (measured-killed=8, match=10/10, flips=0) and `REGRESSION_CASE bash-surface-census: PASS` (measured-killed=8, match=10/10, flips=0). Wall time was 276.66 s, under the 6-minute bound. The tool sha was fb91ef76… and was unchanged.
- **Before/after identity (Read05-1, Read05-4):** the sha256 values of tools/mutate-and-run.sh, tools/trace-inputs.py, and both case notes were identical before and after the sweep.
- **Status:** `git status --porcelain` printed nothing after the sweep (Read05-5, exit 0). The before-sweep status also printed nothing with exit 0. Its receipt is excluded; see Receipt handling.
- **Named cp -p and cmp (Read05-16):** a `cp -p` of tools/mutate-and-run.sh into /tmp scratch followed by `cmp` printed `CMP_IDENTICAL`.
- **Step 1 header facts (step 1, SKILL.md:380-382):** mutation-case-kimi-census.md:13-16 gives sha 83016d45…4f426, 896 lines, 43273 B, mtime 2026-10-13 18:53:12, kumitate 175de6ba…, and an empty porcelain status. mutation-case-kagi-census.md:13-17 gives sha 275d8294…53009f, 44212 B, mtime 09:47:15, HEAD fecee874…, and an empty porcelain status. Both match the step.
- **Step 3 (SKILL.md:386-391):** kimi:34-35 and kagi:54-56 match the restore proofs. Neither note records an after-repo revision. A grep for after, HEAD, and similar terms across both notes found no after-revision (Read05-13).
- **Step 6 (SKILL.md:396-400):** kagi:271-272 says the old commands `do not by themselves recreate that driver after scratch loss`. tools/mutate-and-run.sh:1384-1393 contains the js-kimi-census and bash-surface-census legs and does not call mutate_driver.py.
- **Step 7 (SKILL.md:401-403):** the G-R2-1 text at knowledge/gates-survey-kagi.md:554-560 supports the dirty-pin lesson. corpus/README.md:11 is the index row for that addendum.
- **Pins:** I recomputed the nine sibling blobs the regression replayed with `git show <rev>:<path> | sha256sum`. All nine match the REGRESSION_PIN values, and they are recorded in external_inputs.

## Smallest safe correction (wording only; no command changes)

1. Step 2 (SKILL.md:383-385) says `cp -p` the artifact "into the lane namespace". The cited lines (mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:44-45) put the copies under /tmp scratch. Use "into the /tmp scratch directory" or define "lane namespace". The cp -p command itself is confirmed at kimi:172 and kagi:243.
2. Step 3 (SKILL.md:386-391) has run-together tokens: `hash83016d45…4f426,43273B` and `unchanged09:47:15`. Add spaces. The values are correct.
3. Step 6 (SKILL.md:396): "The historical probes reran from scratch (SCORECARD.md:13)". SCORECARD.md:13 says the sensitivity re-runs used "the lane's retained scratch". Read literally the sentence says the inverse. Change it to "reran from the retained scratch (SCORECARD.md:13)".
4. Step 6 (SKILL.md:398-399): "do not directly rebuild after scratch loss" has no pointer. Cite mutation-case-kagi-census.md:271-272. Also name the rebuild route: both notes publish the driver spec "so the run can be rebuilt from the note alone" (kimi:152-153 and :155-165; kagi:215-216 and :218-236), and SKILL.md:557-563 gives a driver contract.
5. Step 7 (SKILL.md:401-403) cites "corpus/README.md round-2 addendum". corpus/README.md:11 is only an index row. The G-R2-1 text is knowledge/gates-survey-kagi.md:554-566. Cite that.

## Receipt handling (disclosure)

- **Excluded receipt Read05-2.** The command was `git status --porcelain -- tools/mutate-and-run.sh <kimi note> <kagi note>`, run before the sweep. It exited 0 with empty stdout. Inside the collector, git re-hashed the clone's tracked tree because the fresh clone's index was racy. The receipt lists 5,853 inputs. That set included the clone's SCORECARD.md (sha a7aa9ab5…), LOG.md (sha b28a2118…), and .ufo/evidence/round-21/coldread/ledger.json (sha 1bd763a5…). The bound says never to open those three under the collector, and I breached it through git's index refresh. I did not open the live lane path, and the receipt's live_lane_reads is empty. I renamed the receipt to traces/EXCLUDED-Read05-2.json so no glob or merge picks it up, and I did not list it in traces or commands_executed. L1 should decide whether to keep it. The later status (Read05-5) read only .gitignore, because the index had been refreshed.
- **Setup outside the collector:** the clone and checkout, one sha256sum of the clone's SKILL.md, and the git show reads of SCORECARD.md and the nine sibling pins. The sibling and SCORECARD reads are in external_inputs. The rest are setup steps and are not in commands_executed.
- **Tools:** none installed or upgraded. The regression removed its own scratch on PASS.

## Residual risk and verification gaps

- Steps 4 and 5 are policy statements with no checkable claim.
- The before-sweep status has no clean receipt. The clone was a fresh checkout at the rev, and the status output was empty.
- I did not rebuild the mutate driver from the spec tables, so the rebuild route is untested.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read05", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 375, "heading": "## Restore discipline \u2014 before/after identity, not continuous non-write proof", "class": "instruction", "verdict": "gap-minor",
  "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
   "SKILL.md:383-385 step 2 says cp -p the artifact 'into the lane namespace'. The cited lines (mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:44-45) put the copies under /tmp scratch (/tmp/tameshi-r2-1-work, /tmp/tameshi-r3-1-work); 'lane namespace' is undefined. cp -p itself is confirmed at kimi:172 and kagi:243.",
   "SKILL.md:386-391 step 3 has run-together tokens 'hash83016d45…4f426,43273B' and 'unchanged09:47:15'; add spaces. The values match kimi:14 and :34-35 and kagi:14-15 and :54-56.",
   "SKILL.md:396 step 6 says 'The historical probes reran from scratch (SCORECARD.md:13)'. SCORECARD.md:13 says the sensitivity re-runs used 'the lane's retained scratch' (the /tmp/tameshi-r2-1-work mutant files); read literally the sentence states the inverse. Fix: 'reran from the retained scratch (SCORECARD.md:13)'.",
   "SKILL.md:398-399 step 6 says the case-note commands 'do not directly rebuild after scratch loss' with no pointer. Support is mutation-case-kagi-census.md:271-272. The section omits the rebuild route: kimi:152-153 and kagi:215-216 publish the ten-edit driver spec 'so the run can be rebuilt from the note alone', and SKILL.md:557-563 gives a driver contract. Fix: cite kagi:271-272 and name the spec route.",
   "SKILL.md:401-403 step 7 cites 'corpus/README.md round-2 addendum'. corpus/README.md:11 is only an index row; the G-R2-1 text is knowledge/gates-survey-kagi.md:554-566 (section 10, 'Errata (round 2)', starting at :545). Fix: cite gates-survey-kagi.md:554-566."
  ],
  "commands_executed": [
   "sha256sum tools/mutate-and-run.sh tools/trace-inputs.py corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md",
   "bash tools/mutate-and-run.sh --regression",
   "sha256sum tools/mutate-and-run.sh tools/trace-inputs.py corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md",
   "git status --porcelain",
   "sh -c 'cp -p tools/mutate-and-run.sh /tmp/Read05-gveQ/scratch/mutate-and-run.copy.sh && cmp /tmp/Read05-gveQ/scratch/mutate-and-run.copy.sh tools/mutate-and-run.sh && echo CMP_IDENTICAL && ls -l /tmp/Read05-gveQ/scratch/mutate-and-run.copy.sh'",
   "python3 -c \"import sys;[print(f'{p}:{i+1}: {l}') for p in sys.argv[1:] for i,l in enumerate(open(p).read().splitlines())]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md",
   "python3 -c \"import re,sys;pat=re.compile(sys.argv[1]);[print(f'{p}:{i+1}: {l[:900]}') for p in sys.argv[2:] for i,l in enumerate(open(p).read().splitlines()) if pat.search(l)]\" 'kimi|kagi|G-R2-1|addendum' corpus/README.md",
   "python3 -c \"import re,sys;pat=re.compile(sys.argv[1]);[print(f'{p}:{i+1}: {l[:900]}') for p in sys.argv[2:] for i,l in enumerate(open(p).read().splitlines()) if pat.search(l)]\" '^#|G-R2-1' corpus/knowledge/gates-survey-kagi.md",
   "python3 -c \"import re,sys;pat=re.compile(sys.argv[1]);[print(f'{p}:{i+1}: {l[:900]}') for p in sys.argv[2:] for i,l in enumerate(open(p).read().splitlines()) if pat.search(l)]\" 'mutate_driver|--regression|REGRESSION|kimi|kagi|workdir' tools/mutate-and-run.sh",
   "python3 -c \"import sys;p=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);L=open(p).read().splitlines();[print(f'{p}:{i}: {L[i-1]}') for i in range(a,min(b,len(L))+1)]\" corpus/knowledge/mutation-case-kimi-census.md 150 222",
   "python3 -c \"import sys;p=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);L=open(p).read().splitlines();[print(f'{p}:{i}: {L[i-1]}') for i in range(a,min(b,len(L))+1)]\" corpus/knowledge/mutation-case-kagi-census.md 18 72",
   "python3 -c \"import sys;p=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);L=open(p).read().splitlines();[print(f'{p}:{i}: {L[i-1]}') for i in range(a,min(b,len(L))+1)]\" corpus/knowledge/gates-survey-kagi.md 545 580",
   "python3 -c \"import re,sys;pat=re.compile(sys.argv[1]);[print(f'{p}:{i+1}: {l[:700]}') for p in sys.argv[2:] for i,l in enumerate(open(p).read().splitlines()) if pat.search(l)]\" 'after|HEAD|rebuil|scratch|driver|unversion|rerun|reran|re-run' corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md",
   "python3 -c \"import sys;p=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);L=open(p).read().splitlines();[print(f'{p}:{i}: {L[i-1]}') for i in range(a,min(b,len(L))+1)]\" .ufo/waves/round-26/w1/ColdreadPilot.md 214 224",
   "python3 -c \"import sys;p=sys.argv[1];a=int(sys.argv[2]);b=int(sys.argv[3]);L=open(p).read().splitlines();[print(f'{p}:{i}: {L[i-1]}') for i in range(a,min(b,len(L))+1)]\" corpus/knowledge/mutation-case-kagi-census.md 206 276"
  ],
  "opened": ["tools/trace-inputs.py", "tools/mutate-and-run.sh", "corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/gates-survey-kagi.md", "corpus/README.md", ".ufo/waves/round-26/w1/ColdreadPilot.md"],
  "inputs": {
   "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
   "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
   "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
   "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
   "corpus/README.md": "33915658d9ef1ed3b93ed0cf58ba5b341bc58facc5d1ff73574e6ddd297dcb79",
   ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
   ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116"
  },
  "external_inputs": {
   "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SCORECARD.md": "a7aa9ab587fd19fd7af51381f2698d63019e7c3a513f57e5918e0d2003510c64",
   "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
   "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
   "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
   "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
   "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
   "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
   "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
   "kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs": "6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f",
   "kumitate-shokunin@1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"
  },
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-16.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-9.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-10.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-11.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-12.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-13.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-14.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read05-15.json"
  ]
 }]}
```

Note: I classed the section as an instruction, because it tells a reader to apply a policy in order and to run `--regression`. I ran the named regression and the named sha256, git status, cp -p, and cmp steps in the fleet-mirror clone. I checked every number in steps 1 to 3 against the cited notes at the rev, and I read the SKILL.md page only for its structure and its Appendix A driver contract. I read SCORECARD.md only as git show bytes, with sha a7aa9ab5…, and I did not open the three appended lane files by path. The one breach is the excluded Read05-2 receipt, described above. I recomputed the nine sibling pin blobs with git show, and all nine match the regression's own pin lines. I did not rebuild the mutate driver, so the rebuild route is untested.

COLDREAD Read05: gap-minor
