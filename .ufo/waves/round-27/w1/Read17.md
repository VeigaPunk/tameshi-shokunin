# Read17: cold read of `### The tick, executed`

Verdict: **gap-minor**. Class: **record**. Section: SKILL.md:1164-1211 (the next heading is at 1212). Read rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. The clone's SKILL.md hashes to 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95, as given.

## What checks out

- Six-row table (SKILL.md:1171-1179): each recorded rev is an ancestor of the tip its row names, and each pin equals the blob at that rev. The two stale tips are bba6cdf6 at 72b038da and 7da4ec50 at 12c8f08a. The round-8 mado tip 0c20a76f has blob 90d50cdd. The counts 4 current, 2 stale, 0 drift match ER-4 (Read17-5, Read17-12).
- Harness: at the tick-era tool blob cf41efaa (commit 9f1d3c339a70), lines 511-518 hold the PIN and REV pairs for the four legs, and they match table rows 1-4 (Read17-8). The cases 5-6 pins match the r8 notes (kagi note line 22, kumitate note line 12; Read17-11) and the 2227d harness lines 611 and 613 (Read17-6).
- ER-4 (ledger 318-352, addendum 356-360): the same six readings, both drift chains, the second raw pass at 20:00:29Z, the tool cf41efaa at 1 341 L / 61 632 B and held, and a regression PASS with four legs (Read17-3). The addendum shas differ from the section's 20:03:34Z shas, and the section calls them then-current, which is honest.
- Corroborated by ER-4 but not re-observable: the four sibling trees were clean at the tick (ledger:352).
- Host: hostname is plazir27, as the section states (Read17-9). This is a weak check; the tick time cannot be re-observed.

## Minor gaps and smallest corrections

1. Line anchor tools/mutate-and-run.sh:511-518 (SKILL.md:1168-1169) resolves at blob cf41efaa (commit 9f1d3c339a70, 61632 bytes), where lines 511-518 hold PIN_JS through REV_MADO (Read17-8). It does not resolve at the pinned rev 2227d (blob fb91ef76); I checked only these two of the ten tool versions in history (Read17-4). At the pinned rev 2227d the tool is fb91ef76, the same eight values sit at lines 603-610, and lines 511-518 are loop code (Read17-2, Read17-6). The phrase 'the four embedded legs' is tick-scoped too, since 2227d defines nine PIN_ legs. Smallest correction: name blob cf41efaa, or cite the identifiers PIN_JS through REV_MADO instead of the line range.
2. Cited scratch is gone: /tmp/w9-tameshi-t93/pin-read-final.txt (SKILL.md:1167) and /tmp/w9-tameshi-t93/falsifier/ (SKILL.md:1191). ER-4's scratch /tmp/w9-tameshi-t91/ is gone too (Read17-7). The section names no script for the falsifier, and the round-8 reading rule it follows takes its branch name from ../scripts/hyaku/jj-lane.sh, which sits outside the lane (SKILL.md:1029). I reproduced the falsifier logic by hand against the git objects: the js-kimi-census row with pin 084951be has tip blob 83016d45, which differs, and its recorded rev is the tip, so the reading is stale. I did not execute it. Smallest correction: mark the scratch paths as gone at the record date and name the script.
3. Identity overstated for mado: 'that in-flight edit is now committed as 7da4ec50' (SKILL.md:1187). The round-8 in-flight file was dc864c6a at 99716 bytes (SKILL.md:1057), and the committed 7da4ec50 blob is 131612 bytes (Read17-12). The objects show a later commit superseded it, not that the in-flight bytes were committed as they stood. ER-4 line 338 says 'resolved into', which is also a lineage claim. Smallest correction: 'superseded by a later commit'.
4. 'The same regression receipt' (SKILL.md:1201) overstates identity. ER-4 records workdir /tmp/w9-tameshi-t91/regression and REGRESSION_DATE 2026-10-14T19:58:18Z (ledger:341). The receipt section records /tmp/w9-tameshi-t93 and 19:58:59Z (SKILL.md:1214-1215). Both show the same PASS result from separate runs. Smallest correction: 'the same result from two runs'.
5. Attribution stated without its label: 'the owners' own round-9 lanes are editing their gates' (SKILL.md:1205-1206) is an inference. ER-4 marks that attribution [I] (ledger:356). Smallest correction: restore the [I] label.
6. Interval misstated: 'six minutes later' (SKILL.md:1186). The round-8 stamps this section relies on are 19:15:14Z (SKILL.md:1038) and 19:20:29Z (SKILL.md:1055), which are 5 min 15 s apart. Smallest correction: 'about five minutes later', or give the stamps.
7. Tool clause is not time-scoped: 'tool held at cf41efaa' with the parenthetical sha256sum tools/mutate-and-run.sh (SKILL.md:1181-1182) returns fb91ef76 at 2227d (Read17-1). The held state is true at 2026-10-14T20:00Z only, which ER-4 lines 320 and 360 also say. Smallest correction: scope the tool clause 'at the tick', as the worktree clause already is.

## Residual risk and verification gaps

- Timestamped readings cannot be re-observed at 2227d: the 19:58Z and 20:00:34Z pin reads, the 'all four sibling trees clean at the tick' claim, and the 20:03:34Z worktree shas (b54f5732, 31364115). They rest on ER-4 and on git objects.
- The raw six-case read and the falsifier logs are gone (Read17-7). The worktree column and the falsifier reading are therefore not checked independently.
- The sibling trees have moved since the tick. Current tips and blobs differ from several pins (Read17-5, Read17-12). I made no current-state claim; any current reading would be a new timestamped observation.
- Not opened: the helper ../scripts/hyaku/jj-lane.sh (outside the lane). The fleet root was not touched.

## Process and disclosures

- Tools: none installed or updated. strace 7.2, Python 3.14 and git were already present.
- Receipt 13 is excluded at the L1's request and renamed to traces/EXCLUDED-Read17-13.json. It was my git status run on the fresh clone, made to confirm the clone was clean. On a fresh clone the index is racy, so git read the contents of the whole tree under the collector: 5,853 tracked files, including SKILL.md and the three L1-appended files (SCORECARD.md, LOG.md, .ufo/evidence/round-21/coldread/ledger.json). It is not in traces, commands_executed, inputs or opened, and no claim here uses it. The three appended files were opened only through that run; I read none of their contents by hand.
- Inputs are the union of the inputs of receipts 1-12 and 14, plus the lane files I read by hand. That gives five lane files: tools/trace-inputs.py (read by hand, and receipt 10), tools/mutate-and-run.sh, corpus/knowledge/fleet-kill-rate-ledger.md, corpus/knowledge/mutation-case-kagi-checklist.md and corpus/knowledge/mutation-case-kumitate-claims.md. SKILL.md is in opened, because I read it by hand, but not in inputs, as the rule requires. SCORECARD.md, LOG.md and the round-21 ledger appear in external_inputs only, through git show of their 2227d bytes (receipt 14). My read-backs of my own receipts and of this report sit in the live lane but are untracked at 2227d, so they are not lane inputs.
- Untraced setup, not cited as evidence: clone creation (git clone --no-hardlinks, detached checkout, sibling symlink mirror), listing probes (ls, which, strace -V, python3 --version), scratch-script writes, the rename of receipt 13, and read-backs of my own receipts after the traces finished. The clone's SKILL.md hash was checked during setup.
- Sibling reads were read-only git with GIT_OPTIONAL_LOCKS=0 or plain file reads. Nothing was written to a sibling repo. No jj command was run. All thirteen receipts in the record show rev 2227d and exit 0. Receipts 4, 5, 8 and 12 also count non-fleet /home opens (dropped_home_count, never hashed), and receipt 5 records the sibling worktree files it read. No receipt in the record shows a live-lane read.
- Receipt 14 ran git show of the three appended files under the collector, where the exception asks for it outside. Its receipt opens no working-tree file (empty inputs, external and live-lane maps), so the placement adds no lane read.
- The thirteen commands in commands_executed are the traced argv strings, one per receipt in the record.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read17",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1164,
      "heading": "### The tick, executed",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Line anchor tools/mutate-and-run.sh:511-518 (SKILL.md:1168-1169) resolves at blob cf41efaa (commit 9f1d3c339a70, 61632 bytes), where lines 511-518 hold PIN_JS through REV_MADO (Read17-8). It does not resolve at the pinned rev 2227d (blob fb91ef76); I checked only these two of the ten tool versions in history (Read17-4). At the pinned rev 2227d the tool is fb91ef76, the same eight values sit at lines 603-610, and lines 511-518 are loop code (Read17-2, Read17-6). The phrase 'the four embedded legs' is tick-scoped too, since 2227d defines nine PIN_ legs. Smallest correction: name blob cf41efaa, or cite the identifiers PIN_JS through REV_MADO instead of the line range.",
        "Cited scratch is gone: /tmp/w9-tameshi-t93/pin-read-final.txt (SKILL.md:1167) and /tmp/w9-tameshi-t93/falsifier/ (SKILL.md:1191). ER-4's scratch /tmp/w9-tameshi-t91/ is gone too (Read17-7). The section names no script for the falsifier, and the round-8 reading rule it follows takes its branch name from ../scripts/hyaku/jj-lane.sh, which sits outside the lane (SKILL.md:1029). I reproduced the falsifier logic by hand against the git objects: the js-kimi-census row with pin 084951be has tip blob 83016d45, which differs, and its recorded rev is the tip, so the reading is stale. I did not execute it. Smallest correction: mark the scratch paths as gone at the record date and name the script.",
        "Identity overstated for mado: 'that in-flight edit is now committed as 7da4ec50' (SKILL.md:1187). The round-8 in-flight file was dc864c6a at 99716 bytes (SKILL.md:1057), and the committed 7da4ec50 blob is 131612 bytes (Read17-12). The objects show a later commit superseded it, not that the in-flight bytes were committed as they stood. ER-4 line 338 says 'resolved into', which is also a lineage claim. Smallest correction: 'superseded by a later commit'.",
        "'The same regression receipt' (SKILL.md:1201) overstates identity. ER-4 records workdir /tmp/w9-tameshi-t91/regression and REGRESSION_DATE 2026-10-14T19:58:18Z (ledger:341). The receipt section records /tmp/w9-tameshi-t93 and 19:58:59Z (SKILL.md:1214-1215). Both show the same PASS result from separate runs. Smallest correction: 'the same result from two runs'.",
        "Attribution stated without its label: 'the owners' own round-9 lanes are editing their gates' (SKILL.md:1205-1206) is an inference. ER-4 marks that attribution [I] (ledger:356). Smallest correction: restore the [I] label.",
        "Interval misstated: 'six minutes later' (SKILL.md:1186). The round-8 stamps this section relies on are 19:15:14Z (SKILL.md:1038) and 19:20:29Z (SKILL.md:1055), which are 5 min 15 s apart. Smallest correction: 'about five minutes later', or give the stamps.",
        "Tool clause is not time-scoped: 'tool held at cf41efaa' with the parenthetical sha256sum tools/mutate-and-run.sh (SKILL.md:1181-1182) returns fb91ef76 at 2227d (Read17-1). The held state is true at 2026-10-14T20:00Z only, which ER-4 lines 320 and 360 also say. Smallest correction: scope the tool clause 'at the tick', as the worktree clause already is."
      ],
      "commands_executed": [
        "sha256sum tools/mutate-and-run.sh",
        "python3 -c import sys;L=open(sys.argv[1],encoding='utf-8',errors='replace').read().split(chr(10));[print(i+1,L[i]) for i in range(int(sys.argv[2])-1,min(int(sys.argv[3]),len(L)))] tools/mutate-and-run.sh 505 520",
        "python3 -c import sys;L=open(sys.argv[1],encoding='utf-8',errors='replace').read().split(chr(10));[print(i+1,L[i]) for i in range(int(sys.argv[2])-1,min(int(sys.argv[3]),len(L)))] corpus/knowledge/fleet-kill-rate-ledger.md 316 362",
        "python3 /tmp/read17-6cgX/scratch/toolhist.py",
        "python3 /tmp/read17-6cgX/scratch/sib.py",
        "python3 -c import sys,re;L=open(sys.argv[1],encoding='utf-8',errors='replace').read().split(chr(10));[print(i+1,L[i]) for i in range(len(L)) if re.search(sys.argv[2],L[i])] tools/mutate-and-run.sh PIN_|REV_",
        "python3 -c import os;[print(p, os.path.exists(p)) for p in ['/tmp/w9-tameshi-t91','/tmp/w9-tameshi-t93','/tmp/w8-tameshi-t84','/tmp/w9-tameshi-t91/pin-read.log','/tmp/w9-tameshi-t93/pin-read-final.txt']]",
        "python3 -c import subprocess,hashlib;b=subprocess.run(['git','show','9f1d3c339a70:tools/mutate-and-run.sh'],capture_output=True).stdout;t=b.decode('utf-8','replace').split(chr(10));print('commit 9f1d3c339a70 blob sha256',hashlib.sha256(b).hexdigest(),'lines',len(t),'bytes',len(b));[print(i+1,t[i]) for i in range(len(t)) if (504<=i<=519) or ('PIN_' in t[i]) or ('REV_' in t[i])]",
        "hostname",
        "sha256sum tools/trace-inputs.py tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md",
        "python3 -c import os;[print('FILE',p,os.path.exists(p),[(i+1,l[:200]) for i,l in enumerate(open(p,encoding='utf-8',errors='replace').read().split(chr(10))) if pat in l] if os.path.exists(p) else 'missing') for p,pat in [('corpus/knowledge/mutation-case-kagi-checklist.md','7e5ec98b'),('corpus/knowledge/mutation-case-kumitate-claims.md','e9a21b44')]]",
        "python3 /tmp/read17-6cgX/scratch/chk2.py",
        "python3 /tmp/read17-6cgX/scratch/special.py"
      ],
      "opened": [
        "SKILL.md",
        "corpus/knowledge/fleet-kill-rate-ledger.md",
        "corpus/knowledge/mutation-case-kagi-checklist.md",
        "corpus/knowledge/mutation-case-kumitate-claims.md",
        "tools/mutate-and-run.sh",
        "tools/trace-inputs.py"
      ],
      "inputs": {
        "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
        "corpus/knowledge/mutation-case-kagi-checklist.md": "43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7",
        "corpus/knowledge/mutation-case-kumitate-claims.md": "3da1312e0a624ca565dc243fd0cb6f19968c1672f57066fbd4d2ad2bdf8045d9",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
      },
      "external_inputs": {
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/.gitignore": "3767312444cc6425c133ea7e335892948272aa886559e4cc3d3e41a5394ce74e",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/.gitignore": "3767312444cc6425c133ea7e335892948272aa886559e4cc3d3e41a5394ce74e",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/.gitignore": "d949e4ef14286bcc34282c15538a4a023a6c74d436cba3dae0f5155239d8f817",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.gitignore": "65e9a6838b253022bd43ee70918dcf5f6d920cb9c2e80b91ccfb15e8e54ee027",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e",
        "kagi-shokunin@899c50b42634a3a4ad0b28ab7509786315e2fc2b:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "kagi-shokunin@899c50b42634a3a4ad0b28ab7509786315e2fc2b:corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs": "e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b",
        "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
        "kumitate-shokunin@f69817edf687c8ce4f87ed7953a353399232f69e:scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
        "kumitate-shokunin@f69817edf687c8ce4f87ed7953a353399232f69e:scripts/kimi-census.mjs": "7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156",
        "mado-shokunin@0c20a76fa5ff985047c8ca2d455c75179c3dd0d1:tools/mado-verify.sh": "90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd",
        "mado-shokunin@12c8f08a35537b7d53b8e0252459dec16e550079:tools/mado-verify.sh": "7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f",
        "mado-shokunin@8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122:tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh": "d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:.ufo/evidence/round-21/coldread/ledger.json": "1bd763a5899b28fa4515aaeb0e46ef206335620b97cc955cecce41ddfc697b21",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:LOG.md": "b28a2118a43b1ae50057b7a0239569ceeeda9781fa885eb92151dc0dd194ab9a",
        "tameshi-shokunin@2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SCORECARD.md": "a7aa9ab587fd19fd7af51381f2698d63019e7c3a513f57e5918e0d2003510c64",
        "tameshi-shokunin@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75",
        "tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh": "084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5",
        "tsukuroi-shokunin@72b038da9b2b1da2a37d35e3cce2d1d7650f70be:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
        "tsukuroi-shokunin@aa136d69e0e4666b86782152cd1d1fa00f90a0b3:tools/tsukuroi-census.sh": "bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55",
        "tsukuroi-shokunin@e9f5356cd68c9281d07a22e54d1bfd72b12306ac:tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-5.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-6.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-7.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-8.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-9.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-10.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-11.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-12.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read17-14.json"
      ]
    }
  ]
}
```

Note: I checked every pin, rev, ancestor and count the section gives against git objects in the sibling repos, the tick-era and pinned harness blobs, the ER-4 ledger block, and the r8 notes. They agree. The defects are in pointers and wording: one line anchor is stale at the pinned rev, the cited scratch is gone, and three phrases overstate identity or attribution. None of them blocks the record, so the verdict is gap-minor. The verdict rests on receipts 1-12 and on the external git objects; receipt 14 only records the bytes of the three appended files, and the excluded receipt 13 plays no part.

COLDREAD Read17: gap-minor
