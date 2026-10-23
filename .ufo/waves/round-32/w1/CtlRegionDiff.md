# Verdict: both region diff controls are rejected

Axis: **operability**. Calibration safeguard: report the observed negative results without changing the frozen predicate.

- Exact regions: `kill=18/18 accept=2/8 other=6`, `C1_R32_PASS=false`, counter exit **1**.
- Ignoring comment-only lines and whitespace: `kill=18/18 accept=3/8 other=5`, `C1_R32_PASS=false`, counter exit **1**.
- Neither control meets C1. Every frozen and generated must-kill copy was correctly rejected in its observed run. The acceptance panel prevents region identity from satisfying the claim.
- Single behavior-bearing mutation probe: **N05 killed** by both shapes, with passing pristine and restored baselines and exact byte restoration.

## Evidence and scope

Read first: `.ufo/evidence/round-32/c1-measure.py:1-281` and `.ufo/evidence/round-32/contract.json:1-49`.
The predicate is at `contract.json:13-20`; acceptance transformations are at `c1-measure.py:140-168`; classification and final predicate are at `c1-measure.py:265-277`.

The control embeds all 106538 pinned runner bytes, compressed with zlib and encoded as Base85, obtained by this command in the isolated clone with Git environment variables removed:

````````sh
git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh
````````
Observed pinned SHA-256: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`.

Only these pinned regions are compared: `tools/mutate-and-run.sh:1432-1471` (from `  local nlegs=9` through the closing function brace), and `tools/mutate-and-run.sh:1989-2040` (the tally selftest harness, located by content rather than candidate line numbers).
Comparison code is at `lane/tools/tally-audit.py:422-457`; embedded bytes are at lines 9-419; shape selection is line 8.
The normalized shape removes comment-only lines and all whitespace, but deliberately does not remove inline comments. Neither shape runs Bash, checks the status-leg contract, evaluates an independent tally oracle, or tests harness rejection behavior.

Setup command, completed with no output:

````````sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
````````

Raw shape sandbox commit command and observed output:

````````sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlRegionDiff && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane rev-parse HEAD
````````
````````text
b6011246cf35ecd75ab18b2a2645e1a086cb1a0c
````````

After the raw run, the only source change was line 8, `IGNORE_NONCODE = False` to `IGNORE_NONCODE = True`. The sandbox commit was amended before this report was written, leaving exactly one final sandbox commit above the required frozen parent. Command and observed output:

````````sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane -c user.name=ctl -c user.email=ctl@sandbox commit --amend -qm CtlRegionDiff && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane show -s --format='%H %P' HEAD
````````
````````text
4d6b2b62aa9ed424d4eb2ec17d7e0d3ea68ed43f c31814978969a41a8e9b0f7d99fa308c5993c1b7
````````
The raw receipt records its actual earlier revision `b6011246cf35ecd75ab18b2a2645e1a086cb1a0c`; its full source is retained below and at `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-raw.py`. The final normalized revision is `4d6b2b62aa9ed424d4eb2ec17d7e0d3ea68ed43f`.

No production files were edited. All executable probes and counter work directories were inside `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff`. No seat or model was spawned, and no tool was installed or upgraded.

## Exact region comparison: complete frozen counter receipt

Fresh work directory; no `--seed` supplied. Exact command:

````````sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/w-CtlRegionDiff
````````

Full stdout, verbatim:

````````text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=163) outcome=KILL exit=1 sha256=00f79f6a90cb003f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(rc=$?) outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=1,dup=6) outcome=KILL exit=1 sha256=3b06db937e2c19fb last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN01(vector=0) outcome=KILL exit=1 sha256=71d7c5f20bfccac6 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=KILL exit=1 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(split) outcome=KILL exit=1 sha256=16566843890d60ab last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_sourcescheck,dup=st_citecheck) outcome=KILL exit=1 sha256=80ba88fdc1323039 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL'
COPY set=accept id=B2-reversed outcome=KILL exit=1 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS'
COPY set=accept id=B4-cosmetic outcome=KILL exit=1 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB6-permuted outcome=KILL exit=1 sha256=52973e0f63d2c4be last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=98bc08a4d6b7b94b last='TALLY_AUDIT: FAIL'
C1_R32: kill=18/18 accept=2/8 other=6 runner_sha_ok=1 tool_present=1 seed=f5699ccfb6642f7e rev=b6011246cf35ecd75ab18b2a2645e1a086cb1a0c C1_R32_PASS=false
````````

Exit code: **1**. Stderr: empty.

Correct acceptances: `B0-pristine`, `B3-decoys`. False rejections: `B1-T07`, `B2-reversed`, `B4-cosmetic`, `B5-renamed`, `gB6-permuted`, `gB7-nonce`. All 18 must-kill copies were rejected. These labels are copied from the receipt, not exposed to the control.

## Comment-only and whitespace normalization: complete frozen counter receipt

Separate fresh work directory; no `--seed` supplied. Exact command:

````````sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/w-CtlRegionDiff-normalized
````````

Full stdout, verbatim:

````````text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=187) outcome=KILL exit=1 sha256=0f415395b7c7eb29 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=1) outcome=KILL exit=1 sha256=c307192c9c04517f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(:) outcome=KILL exit=1 sha256=fba8e1cf3e1bfd8b last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=7,dup=4) outcome=KILL exit=1 sha256=2ef092a7a155792d last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN01(vector=1) outcome=KILL exit=1 sha256=ebf4a902638d568e last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=KILL exit=1 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_citecheck,dup=st_mado) outcome=KILL exit=1 sha256=0859ac3c1305902b last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL'
COPY set=accept id=B2-reversed outcome=KILL exit=1 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS'
COPY set=accept id=B4-cosmetic outcome=KILL exit=1 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB6-permuted outcome=KILL exit=1 sha256=808760d3416ccf05 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=80e3d81bffa4b5f5 last='TALLY_AUDIT: PASS'
C1_R32: kill=18/18 accept=3/8 other=5 runner_sha_ok=1 tool_present=1 seed=9fa174eaa05e1a71 rev=4d6b2b62aa9ed424d4eb2ec17d7e0d3ea68ed43f C1_R32_PASS=false
````````

Exit code: **1**. Stderr: empty.

Correct acceptances: `B0-pristine`, `B3-decoys`, `gB7-nonce`. False rejections: `B1-T07`, `B2-reversed`, `B4-cosmetic`, `B5-renamed`, `gB6-permuted`. `B4-cosmetic` adds an inline `# pass` comment, so deleting only comment-only lines does not make its region identical. All 18 must-kill copies were rejected.

The two runs used independently generated fresh seeds; their generated copy bytes are not claimed to match each other. Normalization accepted its nonce-comment copy, which the exact shape rejected in its own run.

## Bounded mutation probe and restoration

Mutant: at `probe-runner.sh:1456`, change exactly one operator from `!= nlegs` to `< nlegs`. This weakens the completeness guard by failing to reject overcounts; it is the frozen N05 edit at `c1-measure.py:85`.

Expected detector: the same `timeout 15 python3 -I CONTROL --runner probe-runner.sh` command for each shape must print `TALLY_AUDIT: PASS` and exit 0 on pristine/restored bytes, and print `TALLY_AUDIT: FAIL` and exit 1 on the changed bytes. Observed commands and outputs:

### raw: pristine

````````sh
timeout 15 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-raw.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
````````
````````text
TALLY_AUDIT: PASS
````````
Exit: **0**. Stderr: empty.

### normalized: pristine

````````sh
timeout 15 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-normalized.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
````````
````````text
TALLY_AUDIT: PASS
````````
Exit: **0**. Stderr: empty.

### raw: mutated-N05

````````sh
timeout 15 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-raw.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
````````
````````text
TALLY_AUDIT: FAIL
````````
Exit: **1**. Stderr: empty.

### normalized: mutated-N05

````````sh
timeout 15 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-normalized.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
````````
````````text
TALLY_AUDIT: FAIL
````````
Exit: **1**. Stderr: empty.

### raw: restored

````````sh
timeout 15 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-raw.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
````````
````````text
TALLY_AUDIT: PASS
````````
Exit: **0**. Stderr: empty.

### normalized: restored

````````sh
timeout 15 python3 -I /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-normalized.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
````````
````````text
TALLY_AUDIT: PASS
````````
Exit: **0**. Stderr: empty.

Verdict: **killed**, not inconclusive: both pristine baselines exited 0, both mutated runs exited 1 with the required failure line, and both restored runs exited 0. The fixture edit was reversed before the restored runs.

| Bytes | SHA-256 |
| --- | --- |
| Pristine probe runner | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| N05 mutated probe runner | `e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe` |
| Restored probe runner | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| Unedited clone runner, before and after | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| Raw control source | `8a35d69b6f2c3a6658ef08695f362c067568643d626ff5743ef9c45338a0ad57` |
| Normalized control source | `d5c101e6e2381dd84d7bd494c1af54eba8d3010a2a6378ab5213b881ec8cd69c` |

The exact restoration hash was observed with:

````````sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane/tools/tally-audit.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
````````
````````text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/probe-runner.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane/tools/mutate-and-run.sh
d5c101e6e2381dd84d7bd494c1af54eba8d3010a2a6378ab5213b881ec8cd69c  /fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane/tools/tally-audit.py
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
````````
The counter and contract hashes above match their observed pre-run hashes. Both frozen counter receipts also report `runner_sha_ok=1`. All subprocess calls completed; no long-lived service was started and no process was killed.

Retained bounded receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/raw-counter.{stdout,stderr,exit}`, `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/normalized-counter.{stdout,stderr,exit}`, and `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/mutation-probe.json`.

## Smallest safe correction

No change to the frozen counter, contract or runner is warranted by this probe. Keep both controls rejected. A region comparison cannot replace the planned independent behavioral audit: equivalent guard expressions, operand order changes and variable renaming must remain accepted.

## Full source: exact region shape

File: `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/control-raw.py`; committed in the observed raw revision. Full source, including the complete encoded pinned runner:

````````python
#!/usr/bin/env python3
"""Pre-data control: compare only two pinned runner regions, without executing Bash."""
import argparse
import base64
from pathlib import Path
import zlib

IGNORE_NONCODE = False
PINNED_RUNNER = zlib.decompress(base64.b85decode(
    b'c-rK>?RpwXk|_LNSCNh70c;8=z9f+Gj6SeiV_EVm<nHOQy|{ovDjNY!fn<%XdG;RO_ZrS#!v3F2*(-VDE3>kSLXx|C&)MfW-knxa'
    b'l^Gcs85tQ785#NLhte{fm-@k^<WH_t-wQ7`9;wUa!dv)`HyJwf<)j#1sQ>!+|4*I!6Mr5I_-inoDEJ0%RBqv2`r$?3gcsA#%SkXP'
    b'sJUBqDg|}6`?}Np@z6QLpZVg(BY?es;X$o&*i!SVQ&Blx<`jPA6@Zz|{GnQ0_yT@M&1<o8H7w^1hamuSoVkBK_rnm-DL|zlREz0!'
    b'oDJ3VdZIoD<FPY`o~WplI>+C+!E~~idxM4Q`{U_#eg|O98&M-?4X2h@7v6m6PeN!V^v9!xA1>5&u()948tT$tcusij`!i@ST+Xk8'
    b't6*{tkOtGsnFsAo=R~W?BE$ygvt?NNJegjP{o%P^LXZx(0JWTXqj)*YLua=f7eGXq!0)_TEa!xW)sJAZm=Y$VvF|U`*gsbUcur&G'
    b'U-|PJ=r%Mv^oM##vEIN7ksh<LcLQ|x7AgSrW&x0TsHXGaJeYW6_<j{IO)r65^S~Pi|A6nK`ScRYBene56uNyLEY!6B$p=b?&|jeJ'
    b'M|=gGaIKyJl;^EyGjDP6{9{1{mzT?l596b*r}NL)=f&Lj0n~6Fj28I<)7JL}7uXqqt+BVp(F+M(|H}+or2gzMuf<44+y>Rd>G;YI'
    b'dAO!aVCHQi(_pzE8X+Y@RWHG~fA-D;0P#^qX>j2WK97TNA?y#>e_mb&I4RV}a4-*M3n(=9g3HjMvc=0!;m5r4FZ=!wG4_x|G&s<;'
    b'3k4HNg~68v^(;h`EnYiy8_dsCA%u~eK*3Aj1C|0%$gc%}W)RTrbC>Wlwq8Kmd<vcDEjF_q0rrFQ3kxnl1Y8QMV8iKhKJcx6X~?k;'
    b'0KC$OfCCFJNN{MZ(_s$+kSZ&Ht+ym0-i*BokZf=<oogx4R=}?l-REi%f5CidHJmLP$_yd_^YLOjBoPuKXc0?U919c&C{Mip*e4MI'
    b'QVaeYmR3Yv3uYGbv-2E&!+(6{Yh+G<)4zej0nFJ&u((mP`E)wUXGBEBk*pacn~qy%ELR!>i057aQ`?JA?#t;ArqbNUVyZudabsrn'
    b'u;hBNHk!_b@2HC~RY1rPemErnL2D|MnrZ?B8iJIApVQGOBpk7Xo+Kg2E)ugw>JeC=B}#pgJB~rdVd(=MR-IF5jDe4)W00@Tau)7b'
    b'Lde11I5_DXGu5!-+xkwjjIfZyvyGrvNm^4cnj$1XhIpezOJ$-tJ@+qxvI<0wo|M=<#%k#I7nwXw%YcO$i3*^FKPMpr49L|$Ocm5*'
    b'x&X4nXaG@)>NT?&j6KX$U{k+EB0nMC6Ws_dp{uZ#EU63s`j4{num5l@NzLm7U;_<}0G$hhIlEEQ5xf!cJevcZf(gv*DF{;k3$9=O'
    b'5X9{a#)C@JKzY#V;MXOr)**6C=+75B%0pHIc?$~wE`2bJz*;-ROa8FLs~0q3WG;dn`XiVKJ20cXO1%L~CGeMD0z$(#BjNM}p}DXV'
    b'W6ulU8;${Ap4Nwx*>V9B+JlKXKZhl26pVe40n&^LL8j|>Ffbl0sUR3|F};M}MfC!fQ(PTz#h@B6Q%Ah!C&+Q_6Fz?EBS|OBxzr{s'
    b'GSlUl)e8oHKBe&={#m{8=Z>HPLoy5oi0rGwqodA&%5h=;3qb#&t;%`zO?BU%{&e_L;v;^+z8>$N9Pb~!?Lq;NG{L1mh56)GY6Vzh'
    b';cuhlR<>Y1a!uqfEu8X2b!O0I?wlZtsOx#KSoo9HI))+9WOxQUnBW@vhARnDHzEn@E-B+1gsY>=<9J{X*K`gFg1T~54#!{^0RJq2'
    b'k%)c9#H!gxSsFth)gWxT4`T5%eZ<ZM=M#WG+)+m_lt01whQm3&$+xI6rT!vg@+=rW2dY0C`n;OJ+<LC?UodQ`ce~EtJ?9@~r&;Vd'
    b'AD-?gtCX73A8*XyrZD`^7XFt7*IxO@d=xI`fC?%rqX2LQQT*!?IycNSkcof&03f7g4Sejn%3XRlKw%IoGgvqP?$96m3qLQt?1Tev'
    b'29gWb0$5!Hc1yjV!02BitqSV>0!FM4f9God6#l#iZGG@L9D~YURJ#)xb{McZK{Fpfoj^e_@Nqon{%9EjL*zzYFb07-#UCE6KQf$`'
    b'z$xBmKLjT1U=PMO1P+Hb^tDPG&Y({s*qKSpu<sC;f&_)(1ttPTattB>3CWd$3Be=ggAVd?7J|q@{fJ8Bf}&qkA8C|6s;8!Cfxm}5'
    b't>+-B(3}8RI9af;4A|uo`Z661mUAA1F^~njpJO=)9cC^EPP~!X2Q!cKe;L+xn|UPX!Mt>)GZHCzi+(%{y0&mq+MH;itw3M)Ums8%'
    b'Sihl{AJMQ<&H!J3WGNjkhD45MrJ;XSnk>iT0;7sk2dWiV+eQKmJP^`zn5g?d9~8`D9HPjXO|ergLjU#Kv)$t}WIwMD>)8^pK;2u5'
    b'18=?vM#z@1a6%Jg&g4i=*aAXy2>TzQ5G@+{=*!ve>C4X9x(2m1LEzq;9(K<Tk2@+=EHSvBPflMQ9G=4Txk43d;Fr)+5cZnRnHdi{'
    b'FFN~Yy~6{g7mff13&ic&>B$jdzk)AR>ws)_2B=hppca7gHUQaPHUgLy#vS5`2`t(F@aI$b2GhL&Bp&#)1%LqIZ6tYKl~9P&f48*!'
    b'k4bT;Zm$7F!oj<ojs1v4vJ*rov&rL@vCPaYvDnER#|elz1(qOXB8<)5d`soPHYEB*@*HK$ipC&PAKtPyc>(O`gCUXwI|=4BuoA6^'
    b'AOqlCHLv>10H#1}rJ*&MCK0J7%gLhMW(@|(hG>D}Pm5rvDrS~}*)usG`_WVb__e$}Jizp#Nf?eGph$jGPJ_*%auH(lfF2SYB&xT7'
    b'sow|YL-RRT&x@Wpq0tC=y1<x$@&ObI#@Opdp0qhsJ%wsdP2;>6LZK~$Wb4{E*Fe%LkbCr=sUS;mKx>!bKQ66RN1+bdA*0Akp>loH'
    b'uVG^P)LpEBJw^kNY;Ueinmv-Fi^>QZ6u@+jTdj&i<tJ8FctzzI4WfTRoXo2Ye$flMs5bdXWSn(+XD2XqO8VCU{3rS)bKLyyzUk~k'
    b'O++YCfeDz*!IpY?+UXpBJ4Mw92d@2J|Ng(!aLFv}T!!>p)7xQs<GZ{yziGMG>en}|YJH3ARqKG~?Y^CMx@RY+ot8Rz_3hyF@WmPW'
    b't8mDjnA$^dNcEwo1eBIKI63ZoJLtST-95m5F$iv)q!9Ot)oFUvDmDEGCNQpp@iK%rrXcYZ{(2m5s@pkx`$pxS&B2%kB_}V`*2}l3'
    b'X}D^`;>rdBd7+3KP|~SOZw4w0h&~i@LtMW9^`FY6CkN+)W8<T8x?6cHRsj*YSk6k+9IW8~`cHt`s44hy4)c3HpU#=@Vg_ptEnxOu'
    b'S*|E;c!t3j%kx1l4)#uvQ-Xa76JUnCF+s_=B+EVKxC#rF>nbFepsI+=2ujT7fzK`?W5{S%779NRgR$>2AyBs(g95{ocg67}vxgj0'
    b'0L5}Z@kII*+BTkEAC2{@J)<S<35gkmpRmGq$t|ngc3BBGpvC|T#T=GwKLSfOvw<d7XS@`;Yw2Gq#6`ILyqr%XOw9`el^r9Af&{fe'
    b'5F2rbm)>yd02PCgEaUVd0nI98@WX#Kf>?_~jJe;`x?U%pbOLd!<kkV=mWGH9Cd*TI@5m(GdIS-0+$viTBQKk}f2`w<IxJf!h;<uc'
    b'%)53U#1$W18pO!0_5d8?p1D;VyWC>yyB!^FVU6D>Rwhv*$$RS{*<6(lY1PN{um7l|ptR~{N&}`#*&}LDD=tUVlF?kbh`SvhtHj93'
    b'(orPiD~BR%JHHN8rC|+{JzlFonq(UtAvm<|@qJ*s!9noO(6{KH15M^4UBQw;2g48@Ce7-wQt>=lYDj7tJ#g-U>_!Pn0#gGvj^9eT'
    b'(r{4dmw8bF6}8!_xqp8+g|HU?x48HMi-TK6P6UKeOp_9P;g5%=i_O$7!h&*l7aNtzu<8zfR~IX$i{)0i^7n_0+?xLBWhk|uyP$01'
    b'`e?h#SZ_4WP1?tz;SZJjU;qC9*2se^CL~x3s7(4H7#6^;Tcv;f$2R;Ay{DkV4VPebf>jiZ!1O?`JhTQ9`7e=Kjmss^vw)OxR{oJ_'
    b';ytk3P3VRS4UOE|4z1Fv4mdRk<=6^)w(Ynj_z!O27zbd8TX}vkSC#txSft>9e){pWAL8y7DIkP{+DdRr#2`KntMFrk%RoDQV4F)z'
    b'Wq26Fb6eY>bbt1*gAnXJd*T7OM6<EhOj`y#bJ&7igXpRR4Xb6Fdw|dJ$r+Hw8%7=j-V>C4Hii3amYPIP#ngShwYz$#maW;?qi-R4'
    b'QN37$fCrEt3{BqOLu1sFQCii_a$4de0SLR{v?WY1qx}(b*$l`V8KTbnV`mriRj{_S(zl#M^BY|@U?qAJV0wfGW(r$apgFRCHP(H!'
    b'pd&XZxsd!{m!SK`kOe$;sF#;Ph*m8T3)JMR5;7a2LS{F92IxR*G7MRn7iGF2zFZG!5z=syeta3ATFs1wzyKNA0Rr90+ED$--nEdY'
    b'7@LP!ECe;5-214GT+?JX`_;f}{udM$yceW$D_Rp7$(hY==jcTy5BT}KrAJ<I={Z7B{Q#YCQxI3>t$JNgFc_A>1t6iGe#s8mezIsw'
    b'a+iD`n)d+mgqtMa-)IT4X8-6Atff8}C0Ek{i|Uw}JVlZ*N-M**W3fAO9itTUm}C20T(*ZXwO#L)lXSvLw6!Nfj9De54l@^8Rnco5'
    b'ii;PSKN8-fF>XEP#BZXf@EoSh8m2<e2TkpQn2yfSA1^#rE@-pTxG`hANW!lWGb^DEIcC^lLLRL`iVe){Py3aN>DZrp<Q@Gct?LH9'
    b'sb_8FitO`{%>aEj*3Z1`u!#%UA9>61g8Uz&;L8F!?hp&hzNOx216G<30y1N7EQeQ79kSz_+)yinh4g;2+wJb4BZtZbvN!T#_wcA_'
    b'8NIeqO4ctfW{d*@U_1CZ^o`>nu)4}wd*UqPqgG<E24Ww3TsP)~GRqP&ga`<Uk}x8o5EBmt5$$AcYXL#k$zwH{5^}U(l$%$}d6@w;'
    b'@+?fl68e=&3;>C?#BL6!>^B+?6}*-h5sffzM36)RNEueOfj~C~smzWY>_YRDml`YteE?g6y~i-dxHw6p`Jy^P?-Sa>r=6F;Zr#I^'
    b'W9?S5-iT|-db78Cd=P)r`P&<G0F~mf-W(qD9@C8HY>O5tRvpz-t$fIusC{_EO&p*jF#xv1i`-&*`7pcN04X0wsQYuL^CpSU+3wy^'
    b'qATLLGFT3S(a5J=36KB@nESik4gie3)9!EkWsBJM8?wST8n~kB4(7DH%%{^uOI?0m_?I)~AoG?Mm$Q-%#=<FXO@`v%=pRlynX5ZE'
    b'fv33X3loec$8s{pEn~;|3?!qN6MweAuh@Kvn%66su6m8~+;MQ>AA*#;_E34a0-*~NnngHD0rD2{*pwXEWDQH=2Zz6757bu@!e)=k'
    b'ayN;evm;t{OX=1S%`maQsdaeKBaJGK{=_0~!s3#H!7tNu`?JVREMY`%aS>jrTreylqm*z*F^}%25NIdgX0+d?ccVo*me4I((k{so'
    b'<0H;S4F#3HVzhqIt_jIA=nPG7prf#A=cmJi&hdVyh#RjsZq}HmjrdXzwf54P=^UU%F~9T|!Jvf#l$`vy3Ip|SwA9v9=qbpANx&l%'
    b'!mkm`Gytbdu?51iU=;}?)`jUP{t4sVNc#w*b;^--3a1P%LHxw7)9Jh*i)`eE<DJmhrZn=Y@yjA13r3jYFIbL;%h@;>VD-qBC;;y0'
    b'!<Z<ac3um-*@r9C5EUJ*<7u`nu>Uh(FuUh5_oqKOM-H5FtU(C0uxOPFCJuV~X_6HbK02s-@TBt=@ulB|`OkWU3!FH`jW26u;x)m;'
    b'xRyx2FnSu$^u{h?zSz2mteO~kVd#eH7cWP&B2svv<*{}PqO09Fv`ipnU`cQoaf2N9FQx-yw>2$=vq+AJs~7{w3asFHv<n3IdDq?z'
    b'33psP3*vSqRgI}klHZAGf~>A_`#PY|k$6M-7LSSG<rx24T0s}dhT%ZiC0fG8MiKd^$Ddf!iF7D$eu>g>?h^~+2+mf<Mo1rOzjzd!'
    b'CuY0^QE9&dddvMUpu-MPfyc$1eCO;-C+lH5@tqv%1#+mvFY>9kOiWkgHW1aAHwAJ3Z^#{^=*y&X3f4$~!?c)!9zex-+(n^a8vy1t'
    b')zH>Bs!lk)uub3zU?icMKXCe}t&z!tR10ydolL06fMX*Adq}1N3lB0wNFeQ)X(sN5Sj|SQ7F$ca1?%t}=%Yms?=@(Fi1S~}2olC<'
    b'PUoYwmUjPRi)C_oB+VCkj>;k%JrpW4gRy}HCP3FI`nG`-H;aquq^fdcZ&*=FPuUef!vS&zXFyDyjhR2J7C)7cQQ0*PWuiDDj!5qX'
    b'P%xbSauJMy(!30X%S-Zs(mDbI%e&f85Pl4y4OnqEK&@2HQaMwYGczAG&5ezpI;W_Vw6m)L;>^$~q2Q4xD4*RxE3>_sn{!~;XXT8*'
    b'^!&QF+x@ZEJ$ZY&-+5R5aGS|*Y`i`>=(GX!25&#Mvrre*Li+pm@T`LmqA%g&(e7U72p`T4Uw2O4p7pxzYPk%R5084s?d=WJGJCw4'
    b'*mjjt@!hMI68lFvDzbpg)Gly*9T1b@yf`|1(<Lw~a4x+s#z<oI54DR>U4?P`jpo(HE6^+3<!Cb`3GFkvel93})~I|Sc)=(YF5K9l'
    b'Whs|eUpEw>xKPiYWjiM?vKzlMgdc|BEkbSq*i}$^Ra7qyK?yb*oua*AI|Ak%$6kdW)_}2=(07p*34{6pe`EjG)znPC=JSO=o^5PM'
    b'$RU)8V~i0iIvNJVBm+>nnA^aFJ?bUHijK<@#8|J@N*JTcNpu_^F`z0DW$0fl!m)5iu#m)vps^?>-9}2(*~24zR%2u~PI#o4Sk_2T'
    b'I9oCv2b8MsQ%1S_tmhx^zNR6dVBAE+gasI=;8O`%x_JN@kdCN47CKT0SxEELM4DKjKo&?n5M#O$2DU|EArd};ezu7Y!LlH1bA6hT'
    b'(Z3i2W7Oiq=4`B*xSA3tHWKGG$XSL~??x`Z(_Bc~CoZIJ^%hpPYYQ8z+pUG<hG`+b-&t7MtSrPg8}soqB^!4gCDG%4_d$}4Rey8('
    b'SrS(KcJ6i2ZrtIb&0CIga@s{(B<sTlw3Dv2@qqAwm}4u)s(yLJ|F^-)RjT(-Bu%;#FzEsmV`<~$Rh}JX+ABtm&xBJ9dyVr7rW{!;'
    b'<nLlXx{@vaoc3<TX<Lfx{iV2H3z~j$w~w~#`*L7r%z@+RWD?OpUSe}%i}X|xND8J7;0x+X_cw$i@7S@(IubdL67a5|<Bc^z#OZ;<'
    b'(Kb~|04hn|HQ~hfgb-srHeEvs6MnzIz~J}qIf{`&f$t6j2AWCaSZD?Nn}~NSzWrM~lyQBC(Z<>kqtv(}6IE2)0F`CqR+O0@`cFio'
    b'A$Q0~CG^dfdK|u=WI=UwGwS)DDo~K!Mf^;G_>CF@90q=mnoYn<gjzig^9gtaqk<rCN2GV<jRit5Qt#fWO;FXwP(XeArksDE4qI_<'
    b'GwQ<!vP>qlI7gj9z_PRADFC(fGf-j_Ab3zRdee~rA5RBBnG1Nj04>?*>afl*Zr^BA*BNG27F1_9kIkDds!UV?)pa_3Ggna0>iFXj'
    b'yLpkprqO=fvd^Jy<<-l>v)&V2yOw>GJ1)EGg<E=oo4BXt8i+2p(yBCJ(xEB=v%U|i5by)8T)6)PJ;hLEK60UVZ_cOWU4<3o`~r*g'
    b'24mlww8)E&Va<*XVy3pq{|T`08TI?#*=YyetoZxz_@MK*9w~4+Z0lk={S2$xNA?w<x}cmd9}8qnLC4|$KYhZzn#lrITaKU2^UT0~'
    b'S+oU7K7<Ux*;miRWAohXw3$PeIs{vM`XRP(Q$(s@w1E03xVN7nZJw8k2$9sdHK)vCp1F_4si0j(AA?D-D0#zSi7nfY(G0eu7zDX7'
    b'Ofht6;;<m3xqm&ME_lHLA>@DIO&>6&@t|nHu0Rm5bmGS>!~(^iTm|##1SJk_f3aS|d_n3M)FuAtqthV3DNd2EQ<R~&PJjYTwiL)^'
    b'07o8?999Pr^5XDi?@57x?Y=$x@#IwhIy>Fn@4z#LT^2VCm&B%p<8iy~T;9Axgy6^Z1+E&0FS>2s2Y2T5We3C&O+}co&II@#U*arP'
    b'fBF-{dfLu`jVm7zEJ?Cw>RAp?Lw{4~K7g9pu=H>5sT0vblir6X@AK{AlhS*)G|T2A(eU*VfqwUw54XxWUx0Xwi3J1<^1_tK(7efP'
    b'{spJ0KMq;5x8AXwFz&=2GXQSF&!*4SGf=lt&^%Y~SV1ZliyurFrR5sXtOXNOV(H2M>(BAPBl;R(MZKH>+f48*Znz-#JC6N=+<iG&'
    b'i}?T@c~;4@K)A@^NSlN88OZ{R9x*tmbTBMZL`%3p_x<^FRXP+npdir$&_g_6MRc^mqmt8+Bx&^83%WPkK6rpHAy;$^JO(W*5>=$u'
    b'jPa%3@MEGDH{!I8vEjT8!u&EkZ*Sr{0jACf7YY?2kCG&_InOXzonKK%&wV_>t=!lGvdSB)FmM}>r2k(s2{<;Zq*dBYlm|9SD+^{O'
    b'Xan;ij%!<tH}euVc*pwfU(7}Vd}hKF&u8Z$=uPbr7&yLqPx#0vL&u#<Xah)<M12(tP$L~ahk$V%$nV58J+#bX)E^=BkysO0Ag>3o'
    b'3d3y8Y>qO~1cccP-SU4;5?3#Q3g&fgG8N+w7k>II_?0!OQe?^)1xgH#)<edbok(<$IZ5({{ZAP|kY=&-JO8nN0o@z^9H?~D<43LE'
    b'h;vam=Gn9Cn_tKsl*weeQAJV=Qcga9q{ZPGHUVqkH}%n*&A|BJ7wVaIBRt=D#=Bb2NkRTtRC|#xQx1HH;<}?&6yP1vKttYg35$T+'
    b'MsP{ie|QsaY;?N&yKg#O)mC4#lWa?6fyM=uUC`qKALsNq$H({Y>G^#YsJj6=Eb2o!;5ky`6#^`V3y=u&A}#5;EcQh!kdJX9=S@LU'
    b'JS%wt1O_JQ*E!HJ$gwXV(LQRccOU3S0FPyQVtxsL1IGR&7fNB85O~h$UGTxY06rbyIWs~&=E#9BfqKf;SQ3o>haChxt_8LfFdE8c'
    b'qvvCf7}Z#<2_t}jKO~!*(3%Yzn@~Nyy$rS&-!Vh%QJc(#%bA=)1M>q65wt|e6nXzXp8<q&gi%3F@^P%tZUg@EC&Qey{ciFhUIb8X'
    b'lW-N22!u>)9gIOrRo9-`*=+ICG??V@{FV$ciJTlRW<ux1{3dFEPYwa_9B(Uv`ZYyWr=49cM$UFNk8YXKMI0kK*Vu;FMU)yjMv4!S'
    b'soY7ogS#FD^>z~AX|w|$|4Z)(nAJNPWm%#~{zQI791Em8kX8^A%EEBstRVdx&`1E=KUISZ4^3!)j(Q<O%<Z2Zz2Hy?ef*ZJb5!K?'
    b'z~-|IUpqVv_v10kwmJsEx1kH5*&BoxIg4>8(+LZ2C?1;wOFCwZO(6(copV_*t+SdZu>?q}EZE2PyTqiR-cb)80}qPj{x~GZ2%flO'
    b'*DhLLboPymcWevI?mUqZV7?;=*$)LpKZ0TQgT=4Oj-vdWObc?d3ip4Pmv~0c&mrN9;cN_&1mza!NUnu0^qLODqn7|}QWOFS5rBS<'
    b'V6yaA>WrllRQBeJ5V<p#eU!~VtU5I%ZjCGwRq%*FX`e?Dq8`xLOY|xMMG(k46jTOuzV$(43RY@jP7Yzhp;h7IJ`;!$I%F9xiugJ}'
    b'11*>Rwx*60=bxH>{96B75pBpYRGvJ4lbhV&LUU1ecW?io^Wx=?hkt!_^!oVZ&Hr=SJ$w7p&wu;n?_PfZeL24fK7AfvPNuV8=iy>`'
    b'b^Yb$A7!^vt<@V_+jz=6OH6=1#EG=BPF5S%?Bj8*xp7XK<Et>8=fsD|QUYtGH;Dg`8574+I)*q<JiE-zdvS<@A)?c>B24aT9T#41'
    b'CLG+`gmw0wT&PHM<V(!Qf!QDW*xY0qZ-l4VSL|TRjCvMfWf>&=qAA*fs<&|gAn`hSC0Ne$)|wHU03=;fxgVuMlJz4Yg;W2&eiI07'
    b'N$9i|X<bEn5+W?l9zJB$0u8wqa%SMtq?VBN9W@4A6R9-WtXd@tF0b~C7K(fj!UHbJ&LoISVmg($=-~XF#6=JfB`zWI-NeNfegko_'
    b'u{()N*d&Q76uFbQNo^;NIfwV0PiQ-3Oo1_$7@?+G+hvV%Op1$elzEfT6G$zP>58kfE+&FGDRE+p+tBdZ>cU3A4Q*w*kh+8hJo>Z|'
    b'c@c5>bx?;w@Oxk*c`4jFlxz;1%R%p|<yV>#B~dyh`r+Vm*h7=ZRuN7ASCmJ~-ax%n><zFq7LSMUKe0Hp5HDc+TIYaAl5{v)QPX67'
    b'iH@gjFCE|rb%LQZd=aoxHcUlMD5w_>sP@5T0<4_ifJlYH0wdh})A}OO4H{;34;sbl@5&!mwdbL?@ZdY^&j$JIyr0ddsK%lh-=_qd'
    b'jci*7Ho&zWj04^_TvH^y9RP{ePDLowhhe7FBD?|Drj8WpM-Jeb3B;d&03%~%^et<1_syH5UpPQ07`B0;IO6TcL&VYHy&{J#<i|SV'
    b'-5<7H%__k##wJwKl0ml7Dq0x^;S0`Uf+N-#wtJ1L=v`KhW~}UWKi#$gqlUZ1?R@6|a%va}&$Y%+H>*c)bqX;NPhJTLk#tNmm&3mt'
    b'Il})~PM<k^jvr>7MMf06NR~W5N*8Fpp|nP08yfcJ=T~{K;VZa~=@;+Z4_a?T`5TfCf+lBnt($=zEiK*!YAMUHqQ0p$ZWR@CtDyC;'
    b';+g<dZLCnt5<)G_mhp}NdsY*pp%EjD*eqg1G}~*LXWFTNh>RAav^E-R+TecLjjZjh)jEqktNB9I=c@gqX8))ImgMaEWBhF7YNM<Q'
    b'8}sF)2O0{x*wiDn>B9U<iL@!GP0X-ocBVO#*=7}Iqt>*I8<UhH;HhhLA>(s<6PeRjPalVmkC7A{@YAMkKZ$`ue<D8gcK5m&lTZg<'
    b'>&J}FpabvZDHG+(ftS^c_-J+f41m-Da~Y+>jxw7RVwbT}6RGE!%}Pd9p8pA5DyRGH%|D|Lc6z;n_rcrK-s>*B&f%JStsL$jWy~ql'
    b'Kb0p}C{mROtb^Aim6CI1yqM3U_Oa#oZf91P5_2jWhY{_C-VG%xmkvi$>TW2yR5}a^k-8g%6fzJtqHQZ4cG|dtI@Z2&HW{X#wQ6Bl'
    b'+TC@uVrN(4k-w`J1z71iqZRb5{pjd~s?MNzz8rgVni?&o>j|X!!y%z6fMGW)Fh+@P+k4}3@HZ6`s$=2t02meyx;C)9nN8}sLPk$g'
    b'F^XIx!x*y{DcViOAPL&2_UBmvMSBP9;ov62T|hQ;dM*?fD>1i1H=MDEerg%&SAN56tWcnXkt?yi6)kr*a}Nv$OlN+m#gPkHdxPte'
    b'LJ^&r-FkdrM8g;W{&)nIgBM|BbaB0>gJ)?X*=Ww`<9DkOEOmDaM#ytBRKc1=6pgI;heMM$b0(ZICdTvDICX#AEpymMZ#qgAQ?|g@'
    b'9nfoOaV>a6YcS(}*{g@WXr%X)vWl6EV!9>ht*L0?gt*(Nn=&@yy}e(~I$hbf8_>R8tQ_s#S+vNYdJ~nwcdL^!OLoEB!*gMR?%=|k'
    b'oYUDf^p;~sv_OrA|IjHwR6}L4XzSfPItvYdqyF&e=*%jJ0}3P36?rXmmarWD;yk`|9uLnR|JZu`y7jpG_q5vF**FTU!WvxSgBGKX'
    b'MH-@PX2a+g7<)m}_6K|flADb}*86yJGgMrQ@+teI8Up~3*$~yvteWPef;C}jigEjNR0Mv}Uu-@FCg{Pmftz2Y3nE8U(YdwE$QZ0M'
    b'n*=)^+hhTM9!ZOmb)GMy`7DA&Os0#PgL#_M^yINyUM(C^K44!A`>S>8JUVxXTj}N4#_}e4RrT(&U2`RJB^VlnYzIF#U`YfyZ3yM>'
    b'mI;wmh~z+KlWX5C`=n3UZ4d@hLt6$vP+w#G#x_8lfN5=VACt_uI=Y_WN5wP+RTKZ>?xyi|nMj^z&kO_W=m0F7NsGQntn?sVIp-<*'
    b'vF(65YK?g+7Xq@AX%uuWOO0WN!D8H-59rTj2yexfNYDTm5c>#fM(5H)=}i#Yo2UEo<1%b-vX*Uiic3Ma0QQ==2a}#JO3a5d%u1d2'
    b'I9y4~XCfnY1N?LuW|ERQYKx*a(t4Goay$#9T0N;i(W*m1R!{(f3qzX3j}$u{?%<hTS&fs;5=X2Mg7Op!^zwI6BEA3j^xiOqWC<)s'
    b'IReW%iW{D;C{>SzZ!mnnkZ|+&3q<z)!ov0aB6h+UzJdHeOl=8hom$TP&k;e<WQc?Skqzt8G@w@5VFxt9170M$Fw_$!1m+WFK~T=C'
    b'tF{hU-ihc6vcaS_C;6aucBG11sbM8Mw0Xyj0@Ra7uC^oX^B>XSvo^5CZv{r8!+}RS-?-!xmp0_B-w&BwxE9bS2$BQ6bqaWdC5PZ*'
    b'gz`gg5ECPk<$xV{MvkmVlDtuhkZ&@ZSNNaPef%#Xhksd!;S=)PIsu}2A*q`zQvR3TUer#c&<VrkP3!9U9rGozmPBd}DV#lk>Kb`L'
    b'zfkpwzTKhJ$7-$BptY2bseeD9-eR>v%XU&-rb4ksGU=;BGE>Z5sZwFE#lyNHCY{wHBsSj*=dGx)u?{4$PokbwLsM?!kd@jP1F&F6'
    b'Yl;{Kz^Qab!(<0Zt`MtfbH1Mv@t)t;@0ETgP|;Z+B3r}QwuT#L162CqzwCXhl*{UgGIN^LWpu;kD)3r<<!$Z~QIe_~B@a%lWWtRp'
    b'>sqEf4kJ-40XZh8fRy4SxFA3tC-_8+XszeN0|Uh;4K!n84MZG>m>?&Kn?9<X%J;tq@85$pUmx*@IIpdHVG!DBl*h{)JPS#cO{DNm'
    b'Pu?rH!PwWN#BWd1$qVv$4FTWU^BZnNaaHaUUqO>Nz-E$69Jqyps&mjRn88s8mBN85hv)dD9j3d*6Ns%!Gyjm(qnLzS4o9c9tM*)H'
    b'uU6P=ID1WmXPVxt7xvaPT`xQJYD(+rX-yx5K_lMwmXm0^q1$dWovm{IA*oXDZ5Qbc^sN;R;;kQ43kUVW!4?k1scU0VGg!Dzqq3I%'
    b'iFB;@BC=a4?7{!n3j3706_Dz<g%_^H2fHo|Mq#g7*aw{5LZ?!AQ7OEH5|j<NtuP%hA?8-gj$3u}4^07kH&X(M93T#|V2nUpg@f$^'
    b'GAgAGZmTUrm#WjK%M~x2je`z{x0IE))1!2xcGAxKQg+f!QFkWB#LPlb<`cYO#m>v{z!aTUf=;|{jr_aU+m3eeF1Fn$Cv%bS5-??;'
    b'x)7GUCV0dvmT1{dVoO<;9+c?Qr1{jD6eZCoj+%95IZt`1Ob(o2!s$4b+u*~*i&$RJds1{3tX!b6M4+6~6|C!@dQar4Ek2nh`D3h`'
    b'?Ko)(5A@2ZXr%2*u1!3bqWA!GzPRz`@VNKaZhO00b{oT5y<BVd%jKrm7&NyV+rvS%Ss9HQet+N(`qlc@py~BTeyvg+)wUY7dUI6S'
    b's?<icN@D|Y1vu_jedss(Ud3<v&2p{mmTRutcbfyRU)l1@-l*w$!|Jd`?P9Wyb_Hr|SDH1iS%W(Lt=hozwkqXXwNc*ko1>9i@u~o%'
    b'HmD36mFBir-5T`aX*lfHtAOc<S|&&^?7qLfRjc~-ir?QJ_3NX4zgFG?=+)Yw-*B6r>oprbwSCro`|9oK$zi*^U2E3ezF#l*2hcaa'
    b'?pH^Z%FwS4DqH2@_7+U>dcEv>?!e!!G-_VGzU2Y9`gXZF*xDY{seJ>@Z2(qVK%%W$!`t32Z}rO+e^B$bhFku?8<eY!?OMI&H3)~-'
    b'y9Xz2_%QUmeyu-p%iE1geOPg;)n>K71s$mjw+2W;DB#t$w+7o~chnzj_xqmP@ZoFOcdOJsLGr=$t~dIXvNx>sE70qv=hsGFqf#B#'
    b'D_*nNuhj+sbU<zI|Jd1obp#r6dkeY@qup=%?hpnDS{l}d<xzRqbVu9GtxC1wZ+qK)sM~ZagMl|})`r`S8ZgGNzSZdS07T%vYZUg6'
    b'b`M{7+kVrlxPYDuqwNC7nmcr%rE+zv4{T6zf!eMQ)NWRWqiTQD+^SZZ^-;45mCB=r+h-IQ)^~B>>B-yUgO{MnwV|tJzp}OEjkc@a'
    b'*7gV(tkS6awOVBWgA6^#xv*9Ds*S$8?fJkkP2i78#oMmdhE=~wC`90@joQc^)|>U3Ti^Ca+uOBTf8YW4jQmj@m;#1*R2g`6!h-YF'
    b'bcu%Th6jX#8L(Z(7-6ph$hg}zzvef97&UJjM!8?{t99S44+g-qRbaSEbI=@BxBN<dn};I?vFr_io9dOJ+bq{%oa<G;-}iw+^=jV*'
    b'NTWu*wmtM2m;J-D4p*y{>s!@YZM#}6kLs0Ce+$F|P-4(8_nYnz*rMMcf>r7;P3mQ@jLp}*;b3dvmIpF1BXDk|Tpu(V6&FTkFz5qk'
    b'j0V2vZ#RZbf2+UM^tPJKa=+?rP&!1ECD{YF#hwLF9$MNZ1B#n@TQg5}^VBd;TjpuoJT=XeTQ(rG(k4lf?4D_LuVS7|n|r3sy?TVx'
    b'o@sT@w7O?n-7~H3rL<~f$M>|XpX_!cY__fEruCfCI!TT=rS((QqPb1!=&eob=&jZIfz|q{yV7_hHL|<W*TQbpd+TkCCed4i*}heF'
    b'Kk9|`HtJi)^tWSi)(i9Yh4uDj3f?Sg){*U@?0GNAkV(0?ZaI=LNHGDmTeaw=`&EtTQf`#3AN6L8(l&h~`n@_lK8SvHR!I<(Fxgi<'
    b'svwPYd-3Y8dY!)=o<(1O>YN@N?w{EOx@V{OMvA-w3ZHa42hs1-lb^d0fP=ShdPj%Hod`m=*Ev2r{iU}L^f|L%;~D?nX=nFfbr6kc'
    b'0`%V=pLV(@NAS7V?fewAiz3nP+N<6R^qut14v!8x(aYC|-R|M>OUyH1745u!bM}krt-=1}<h0j0cp1Z9`fvA#D!+WYdwO8Me%sxR'
    b'*F+2t(Vu(J=~{h!an$LY0ohJ4;Ta_a!xQ^`N)*zIO!Xbh!0(~)(qlza?mMOg1v;nu#s;aXz43JVnbTkZ)Mu=|9v-xQDin)Fj=)pS'
    b'bDh<OvJPjRET?xxO*R-(uADwzsTnz(yZ{e$p(g<!QL*0q>Xu4{lDak92im*z6^lH6+<I~=TdtLaCo-9&f+{?E(z?~VebxzGYmYCH'
    b'+ybyh9}0Jxqjv2+LszAb)L+!FFEL>Xrf0-7z?csBhEvx|xma)2gtl<MqsP>Nl@8PK<=jMj?bme%k1|KSA(v93H_(U4^0LqO#7QT<'
    b'3*!VPcOYT$9GR{flVLD_&UvdTz*nw=wyvh2?Ha0LFdMcvT}fE?JhM40#gkf*6`0{vc4yfQeK767Ro_(N;-nUc#tn+_{~Sz)EtLgq'
    b'vIU(byQSQ1bz9h=;{a<4Y+-?@jY>)z)vaxALvDEk1joU^&y@?RkuP3)Gj3q@Yn{JF(5q?Cs}+WB&O79O@QZ_sU_6}rlOku>@Wb3B'
    b'kAafZQdDw%!Kl$%TBCK>0VPy7jO>vcOwqcg<okGM%1sDh-qZa{{(PRxzCFf8AH-BaO$zGc=GV!s3egt!<W>htbViBZ<#Y*H_;b$m'
    b'PMIO*(|-Wxzd|p^t2#=ykNF*hfBSyI-Li15r{G+v*KI;Ey84>mHs&@Ai(`LszPP}sxgDES$+C<2(%-R~You{jr558XbbMs-@Ztaj'
    b'QHwwnD7*CwkgfBUDo-2ba+2E~P^ngnbKq9maFrX3OOBH2|4CgI4G@gLZrd*yfz*=iHXc`x+S*QQtJ%<G7KvNg(IaGDx%euA(@Yz#'
    b'W{j_u`ZM5EM7j_fG!fxl;zbMC=g9X)Ieeeb+k^OE2+<27f8IjWEvJoiO&E*W<i+X9-#f>67!jDYrK$z>s?t)GI{dA+R1^Nx_)i@^'
    b'f)r&O@2p!}TNfmpEeKPx`K^(LdngT8ZhmW3YOba_C!^`^?;d0N6V68?X)!PXj#*BH#A(GPnj}^{!l06hL9JSkkGnZ3NUP%cbb&ie'
    b'xa&VcrnDACz3Oy-+<nu*O*j7cIK;HoA^wH`f8NF|Fx~^3(N0UBwowSKh8bs@R0J0Py$D29s-}-qrJ0cWI?m$Sn=E=bXER9l*l*g+'
    b'<wv7B#TSGJ0BNTHiLkAuV_U`xj%pFcnwXe0ia~}qml!%60p+D5(j`F6eX+aWQD6hS(qzq<MFMwAEt=vK&S(h7Xg9n<J%yjNvVzB|'
    b'Frlw5r{hxi_b6ChSN7`Z-E(VB#obzATir{-hI)xH8bs0`l=B6n(fZ+Pk5zid4?xL3ec3sPcN`&7_Gu3P@bRLZh!hEsI5imvQ^SBv'
    b'P-G`T3v-lT?O3wh{M(61^SwqYk*Zs6oIpUG3kn><BO|#SN)JkIcS{*e@)TP^^!cU+7~CCFTAJ6pFAw+Sl8?+P4=2ECkPn9ybz>`C'
    b'JeBKCt=w1@QSr(D_82I8_~MX<3r8%$p`6YJv|;@56->X=)86j8&Dn?B#GoDbB3L|X7VN~ht;((cLs(T}SVc75PNnI#NPIl}g;s$^'
    b'I$p9B$xY6)xFcy6choI+{I}J2v3`VNGZjU*>8{G#%;sPm^27!U8^gNp60BBfB=aIwev*QbLZL=N8OkKqS{$$A-pMQeySvxz;FaL`'
    b'+<kTUCb6KUSGFsy0$@esQFKKw=p*LVwY68i{zd7{5tYLPuX^L<zyAGy(MC$Xz(Dn8A>9zmo1;6NZJh3Mva<c^tKVpMu8t{tujtM&'
    b'-peFtvb9(@TZ=9wq?Rm-J+4xm-N@Ot?hY)nC8Rv=U19*EGsi$5!OSF3#e{X7&5%aod-fQMD>~W=t=21Pt7L7}wyN>96vIO<16tvy'
    b'pVbNr+C|#2B5`djrK!rcVSEk6jughVEdJ6>Hvh0{l@ye!YkFU;Ikmc(5O|Toe2)DpqwR=!wB?38Y?`=+b2-y3RCJ@DxA1l-#~<Bq'
    b'PM;+xxQ|(($3ql$kCewbQjqyP#Tn<Ocu<^fC85kDl!O@S{JNaVwL5rQ`)A5ScXamSFGU0-1VAiJW;uJsm+y!M43Elwnu4b6jR%Xd'
    b'^Es;$%E7?HsQbU3ygfbMJ=#Az0*IfL)5nVzK7~`fOldN8X5P6!*EIzE{_dL|1~lps`1Xxn=O&!Km<yb|J;R{J6eRKA!Rb%EpW1sz'
    b'C;P8D2l3a(C+MDrE>8S06O?FM!YmVf(oN-}ehJRF(@!ZPq@FmS^4SPBn+^Im>SQ{%MVuf9uRGnBng4NJ9)bWmkNU~t>j53)zo{x{'
    b'EqzkdwUdeel``F5x<@B3dl>h3hRgD4rj=o2Gv6|pG4;6n=H&D&dRu~(^YhcEJHXXn7J5n5&>m7Dt|q78*l=T}9i>}G<$)gL0EX4-'
    b'%J)h>pHMT?1eRM)2&~*3vvi{aHLoo<{mR8xN%M`pmKD$lDeFr7wVNS-Yh1R)TNwW#EyNYkl#aR$>1cQN^_!zk@3_7BRqreI^t+a`'
    b'EhBk%spf4$OG|068Mn-z<PGA9!cne2Z+^bSwKGNcGAXyU8iyg{*69Di;9UeC*YeW3*s!cP5XsXq+2(Ivz3lyj4=}0tf#d={{Ppx0'
    b'9wNk}N~Wx-ovf5l`_h)W?JcL)G>d&C_hKtLE$Dhl1=Bn<F}QJYHo0nN#fh1l4FVNRuHbPB8cig#v~03PY^o51cKEcwoBhL7NVH6X'
    b'&@*R?Cs)BR@S@YN90tl~aX=vsLpn&}-~yga+Tb=q*bUxF!d~>;^3ZRW5${zcwbr7$fOQ&eD~OSlQ;D8o-BbtVfNn}bHc8#IX6vRY'
    b'%4oyNv1l%2W?hs3T{nzEY9Ye$Y&K?zShh&z6m))%+8LujOyztOyMX4(rO`QS03E?1yb1;q>t4`-@dQa<_ftxvF9!{_^gTGgJLZW('
    b'{+1yIF3wtNH@ZS&`WZy)zy4G0fqnbx_~hqfhx9UM|ERNjj34${1mK+m@aw>AEjTkyMNiWW;M@N?h&N_o039$u#R_V^AO^+!x1dU5'
    b'*3^yo=91vI+ae|q=!``i*}2bouyg#;d9F@g<$020Y(|eP>0eq>H;1PKV1^VVrIH`+Fqd%yIA3^@#OmUqg9lWMZ(T_b_F9^h>U`<V'
    b'!7`su={`DRh%sh#gA$=F@(4|S6iAkeFM#B&Z5piBNm>B3;T7Q&e&$>8&})cSci=TU(`&i<M=m45d4TSp=}4jB8cB03d2utFJ6s$7'
    b'Q)Dt=F_p1k>Sl7}p6tob9*lj6m-ynuNKny||7)8e?0#=E@m)Eg%zi8K4bts%$nBvL?En@ef(Xj7oNFLlldsE(-LnYxNYVt`H~W&('
    b'8p5KA!n=~(?@4a<BzDRK^g&B~8O|<NdCRRhgXv_XPekjbMRu@|xRi9gFZ-oX0&iiuoK6C|-5o;}CL<q|ax5AQ@j@7^gSQXkL&z5y'
    b'c!9$@g11~uIiZd}xe5s<QA7W`+sY@l?IOa+W~_5Q_kcp2D~xle11o^IKpis&TKC-3cNnut!<Wus&fVCw{QBs8x?oR_LkA|mK4PyY'
    b'ze}5yb`?@+)2qby0;L0;meQ0f(nz8x#U<7fr{4G)udT|^eLsGfiQx<7Q6gk&qk3h#Uh}F0x0Z$`?Nw0WReYK;e2iwH`nXu*MF6YF'
    b'U?GmKmQ!KCe=)r1uohvq$tSqhA|)kP&^oo&i5D#xugmc`=sU}acLmdo)u#ESU_v4TXPC&)xG=l+#-H&DB>F>i4$h6(&gk?;(t@&E'
    b'uoN#&!f<x-`Y0j8QlYa9`wgItVrGs6)msWrbLewEu}j2QInzPKtexqIWxV1ep_tJjja0=9&mN>`Www{_t^)}7JNyXJgSD?jClmS?'
    b'A#3h!Bdn2{bmqk<T5HHfcde3MhO`om>vsov1Ci?GhQdqOE44;*OYL#+f!eCq;Rzky(K(Q+avQC>+bVA<r(7+UcVL>(2;-FudN7GF'
    b'`IsuFa(Kof8%6;i`l_yiN_MkVaT=Hp8&$Pk6)gNqMM7}Em!X0A=D2Pn&l=nw^0C8EnWnSpI2hbOIky4`Z&mUHXdn2|LlOVU*KjK3'
    b'x>Koc37`W-^%ZT+V(qP3LA5H?rUO)A7#*53yagv9>J6u|)f5n*I%*A&1$8M>Npt99bt=s*2K5qjt3x7l2%ol^PSY*mnK0LZvB>l3'
    b'5(Gr2@De9Y_Bt<4PCL=b)E)H-bIQ@VJ-L~ypt{j39Xg2D&1wm?OMwAG3U+V~##213r*DPHK6<3Gc+K8S^<k!6;#ri5+@Z3#o;sK&'
    b'Uf;o{48G8A?gEyld?dwW3wXj?zy$V*gbVaR0)CDpQcB5KK@0uL3i_CxGQwUEL#D$ZB3#n(64eOLSGJR5wc&jzhHHa2b}nwt1ApR2'
    b'Y^sq0kg>hE-wdT}^^7(Hf+1z$r<<6jFe)f)7E|?ac(Krjr|-&6^TX3kOo};P1kTuB0AJwk%gP&InoZCP?j8}|sro^V!MFb@fHm9?'
    b'sXGfP6`rotcog4h=-)UO>>rpo;mpH?hcvq?WmIp<cr^h9|FM#~27ha$a=8hGR#eKI?aYdF)1S<jNAVp77>659YlNC;s6GO|&L@vF'
    b'JmT_?c*8W5LcuRvbGR4~Tirp=I2h3Rz9j+2Uf^xTg!A3?u-K!xH<%|gr*>mH(Vf?Pk%}aA<82Y)3o1z=DLjAGo0Fr%{a@D6mbe#W'
    b'8`P2^roqj<fB%i2@=tJ}6SH--0u_pI-$#Cad;EI$Z2!m3fpd7)c`Xx`4LYB$KLov-rZVw`<K98<T#geN^GL(|k#;iiHbk{Ig&p_K'
    b'(iXnRw+C<E0I7D*I*jk)Vh*|kX$M|_w|%*YCSGKHJ=F^u-Ijre_|UtSLSjMXxk?}sZz_iNb99B@QT9>XFF{ia^Fl0udoWpfXq(9c'
    b'pY6NcbU5TSm9(3?SX%>(?Y6V`ItTwYUG-GGIKr6sgU+#XsAr|<O+KG7d-ivO+H}(@K8iancy)#eI=u`g9!`=9j)IG~qoPb{ix!7{'
    b'OB(<KzFnd1L|qFBlfz133<t(Ls^mVXQiOBIr8yfc9F*dh80S0({WDrj<x+P{KaP1Ra=YL5_@aBB9ruYso`2scX6qX*I8Wf$eDE#v'
    b'L=y0PU0Iv1DSZxwcHxGsE@mN3gq~jOJC6t6Y(d9XG5<5>C*$<RDo3eF#iYMyvEfu-19VZ~nFWfAiZaWdp8VXCe3*7_*{`R3g6Q35'
    b'fOaS){G$882AEXV^y?3RZGnyG@WQ1PgPzIPqFo_nQZV*TPhJ7XhYPSqv>Rs4FlpzA-sp?P-<=#E{gMm}Gx?|V0V+HoBR)dQc9S^E'
    b'KL)JTaby68O=#&Q<$9v(p`=ZTD^l?hU(=4j%5iRP0rOa^YeC3&EbCjrrq=~Bi0L{&tuN^aChi?)X!D0+&wfv{<v*g;h-5F3SCU&*'
    b')E4Ou)R=62k<N4HWU;oxVph?EHp5aj*nU5}GQwLm>>FU%OD+V(7rB7BYM<4={1jqb5FgoP<6fTyPB-q$YmNKL{l<MVbHH6`1OBM3'
    b'mc$k4X_kH^&C-7W*(^%&Ew*%f_Q>;V{r&)78p@)n*ri)&pQ+jwXw+ag1d}|TxzK6H>AuZ5bVlF46sq(2bU70nDcs?t1AOC^zJJ<K'
    b'0?%b^_bNR`Z+25m?1sd)JX(shD&FeQ+4}fMWy~^GIb39Rh4DXf30)b#h3(C+bdo77;xEx6OhMfBNGlcB7_{xJ^Hjwp`G&ZANRVpe'
    b'=sW<SfoBHFs-;|+O<LmaB=#+MF2i`X)U`LCn7h%$*~mc+Ii!O_S2^H{GM`>fi7E67DuIz$wuR?t(CLh_0+y!S-gHX0+;U~o2Temz'
    b'MiiCQx^}t5rh@j5wiE`q^mbqG9lm^f^0sT~x)r`M1jbT!rYVX6&lBPM=n#zyC@~Ui3RJK_eBS}x{laIW`r}>Cv~A*1b|6d}4>bRE'
    b'82~zR1G_&N&Zf8yF*-m9^0K`1Q1|>$1o~X&_?$~N8-4Ake9g<Ct^v`$6GU5si0^k8a|R^Ic-T^Z?Vf;&0Mq8uLwi2F#*3$hj5@z='
    b'aRSfX{j-AchFR|zMO`#&iwWndoK3Hj*lO@*yj2gihI$&v2{iiHz~Pm656mPou@9{Y0`b@Nd}22sVwmMbi;tEHZ!Y`OvFOWHHkZhy'
    b'Va9G@7^JPL)_~aWD={iJX`z+gpsq~!gHNx>DK_vy7vpP6P<eqlh9Nh2yA(zzjHeSck9m3+6o{n$P&fD#ZEWagu!!DZdz{ZozoXMp'
    b'=8)Y(pqLto6Gj6M27;17<5D-*ECMnd&q7i{OdfQwX$m5mwc9=P@p@tr9CTyl1y~isV2=0QW#7!FpD1ZRJTFI6XA}+{Z#=v3viSn)'
    b'gLhV#&V%z{Lcz3Y^|{}_2g1D=tTY+v9}UjklcIe@nS5jsl|&t^d*~z}81_;1o1%Y&*LW)pse+vBhZqP3hjl^+FNv4jrJ>5zBPFE('
    b'h47c<r6qtDF!ebzF-X|q4JU4rltF0;g9-_SrU+d(8Rw--Zo}%E-A!AsDd_D0zuD|>Z~3@`!hMXcg7+KEer<bO(h^4g<9tzdF$-vm'
    b'(-C1P0G6IyDJM`NFlm4KC8_yXXe9L>eLu9u9$i4F_`EsoIH#SLcsvx73&%AhJX?CtkWy~BEA`O)D;UZ_YLgJ=_ojhCcy8Twc}+mI'
    b'i_$sggkA-8`m&3@-ibfXw`hJ+YSrT63&tDMjda9lsKyr6Poi*4L4bo=+h%1YgzhgnxEZ%)*q5(A%H={|%LTVmga0+)e_OY}ZF~=s'
    b'K2b{>n?oOX>=JKtTLc4@yZk()s}oSBgox=rCo0Pqp_w<<P6KK#qu>h+KVHYHcN*~QyJYkR+hK?HR4LpGMvwR891?-51V7QD;hzY+'
    b'OZ(PgYc<m!$Zyo2!_c|(U}gOxxzwt7SJzZFX$mqeYk3f>*WQ&+fl3}mYkTJut-qls4So%y8FTHHU_5}czU~(G3j2l5Evx@Ubuz=f'
    b'bG(&vOz~(f)h*X6D%V}iZ*VWvTxiQ23hM<>3CRRZd$@ll8!W`pwD+k;a<l|8kaEi!47s(>{VxiSbvWCN?H$kw$0%F|_%|e_U4;4-'
    b's3mmeOO9zlgeZau#(h9V+1|I&+A1ovum&zcN|k8$#(W_iB*bg$ecnaHZEsp-aD8btwzl#}XK`0hkF<Z4NC=8G{k<g+@M}6ljSik~'
    b'*)~SioBUt0$ccuYteswV73dlQ&lj$0xiy${xQj4fRPa}&VbPjM?6YmZ10}Xm$^r*#+Pk%F7pK)t$VvGgK;h~Ng;C4;41_bb4rU%^'
    b'U7}=kY@5FIt-4d+YOJF%NsuB;hl|`tO8e4#NjXP1ze)?Yd@#GM8zwSh`sJ_kbo)^UXg*aR1r_+p54T3~hgbUXHvds8S$}l%X|1i`'
    b'M9rs<@@TLN1LeZXG{egzbEh4QK=0zYC7pf+q}-<$11MG5u5u}zN8w%h10VK|4Qy2p>|Q>;vqpXynkz$XvR;D0?2v7k(lE_a<zJ#D'
    b'^m-Tbia{AX6wrHlc!o2nwst0o#fUBLQ-e9=civkEB`2k^Y$0ZAuB*9%2h>|Pf2ueIsuc(Rv&~r<+3^f2@|30z$~u}|L{)JiJ(UQ?'
    b'I896RXIqoDgA2)PE^ttd=-i2!#W72ha`qhbr0bUHfS4H#`Wd^*o}q8QRj=095g0AaWJRNxr+jot2Tv!|wk8FvqL@fY?ZrD^<IaQh'
    b'enh;*{VoV8_JKb!7ZdQ(XWVunopOSm0KmkZwDZWRr9*3P4C{Q8$gdG6dtl-KOC0lsEdaPuqn!>YT%b{#dD=C_D<!3?ga!Y~8>@Gy'
    b'7eEI-U<gBFEpu`rf|a(~)LJZAL28*sIX0PfgaOeqMz&VuU?pXGF(qw6?^gnmB7}uJXs>|;$BhRgadW1p1@-2wo3}|=Z+-^}>&*gD'
    b'4i<T|2SE|R&9U#MrS9+_L(O_~JvG@|X^Sn<8EC#D;<+<)a_8y#a=J!Qa*oPENJjzYnDQyU^f5!%)gw1;5v*7q4Tq!sTXfXd;rv|+'
    b'G)!Ct7kteLXm@mklkBGqe`~1>3P|@3y4kCb4LpZ_JrF>*d03PfnkX0#sG(brYObR#Fq-4&MNYFEb-^?Duj{a5y!b0F4h#IZp&nJz'
    b'R+~!9TY<`FfXb#c=TL;zZ&+~Zl{@IUZsEvEtJ&YS?%37uS$yJ>0O-#SD+zV<Cv=741Z|u?apjPV9k5|8=E3B%PPk9y#M40+>44;j'
    b'i({074jNVBs@^e@I1&w*-3<o8!lDnV&k&R!7>BddP6ugl_Dei8`2|$Md~aB}OJQL3_4HOM8^J;9ygh#Nw)-QcKN3Rs-jZwX6~5E^'
    b'GWQi*M^8GO+5x+K=#PCgAKtz=>2*){cQo^clnRa<VDhPz$;2rK>{>S~cs{;eop7!R2!!cSf(6x|qiqu<k)y3LZ!(<(bd8bmXX&^D'
    b'6r0t%$cL-+;%4SkUb3t1e8ApSzVnzou>3mVzSW#6h~&6Xe#bhn_eX$*&iD3rfgkV!w=QU!d3!5tn_N-bt^0jD7~!IwFwN?)Qt`Ze'
    b'(xJiu-s|>~5<Zpf-|kb1w-dQl9-2xv=~nr@No^6{c5_PtCgBGOMz>tvs@JuXrDdE_7ycZkb1+aJCs-`A$v5C;tYZrwcZ}As*13{&'
    b'dtCd*?;*~yxXYuc_9K@^>pq`{=)~R^l=ot%IHU!Vv)VhyTgYW^su0^3D=6OOA*(XlC&Ik(wg!O4O2`M)N%)ocY!mt;g2hcyb<BR='
    b'bTC-XZIyq3lQXuhiCM<iIXKP^JEy(Q@!Qwg(5#QFe(>D)g{k$H0(BD6!tND~aN!)HsHKsH7lB0pe6IxPg;<8(8gV8uZ(&q{<%TyL'
    b'=CWj0q5zGMgdgH&k{qVROI)+&)9WHr_hW!YY%si4i@=|go8r2NkGIA+j>9%M{a)DXL^?@O;R?31F@R}K(OV?Pu|Sjt2-Zc+>v=i7'
    b'LUMc27oz-d>a!0}=&XmQ?_YRV!E_#tNLP;tu6>|}P~1fC1QVLR?L=pEtgz}GYsHQ6GNOZ<<?LTE>tX_?EPiYFESSLh5)4aP=>oNb'
    b'?$gt&ny9>_xYG$6nmz**0gal?XPAvveba^Lu6ZijsF}E{Mm?r0HEQt<-bQ`>VCns{I942yIf>7LD3k==!rEwDNB)<EJq(gU7O#6B'
    b'FU)Q|*5JlsyXGL(#~8#X2f~>TIhe`Z#ROU}ZUw&r9Ks^)vSbU{{H<)}rPg`3rp|{oqb1we;_F$NtZzXd2jix<+x_MB>(1HfFRW7Y'
    b'u{3+II5RE=ax=hapN=ITkeKA4cJ-i;uy^pJ8m#70q8OsJgwb@g++*deY+~M1lqdX}{?Y{w%$bf5&~%!tFilmh!c%_B1$$GRiXKC|'
    b'>teNhGiF94RB%<Gu41#-^C?o;lKseB>y-U$0+Cdq6{YAk+u$jXFt2itQ#(BX${N2O=koNfKdaaRC1<ikfBb8ggOug?8}~cB!0lW)'
    b'A#c$QlSN}>2QF|VGW5Z?Id8KKr^`Mp#ge#H8|N73N)aOJY1;&JBwkn6Py68#_j6H+GMtF}B+^Jh^_RrE=G>&ULI!i5xtxC2p7=V^'
    b'wXw6UW)2TR^7ByDF}z7z_6`qvCLVa*>ICTeUoho{wLGm^>AnYCB>`@&?}9VE{0!5d_kr-9SKp&hX=7L?sYf#kXOGD!K!mnwXC(y3'
    b'C5*;gR#N04OifG8IdTd_r#!aVVHLMk-bgJ|xqC6EBZ&GUSP>EwM?>prFozyY=Qj>rra8b<k$R;7?w$E_hoao*E7)Lmr%k$ZK3WK3'
    b'V?-H{pbp}Bqs-PCS4SLJUrWlTwc;Z_=|74APS8M|@yBmG+`P$&Pyf$FT7dujXO-2#gv?FWR>Om2)bDI4ksKAn^6*N_hZs_o-?2Gu'
    b'H4<4-54{Q_X+{0s8#xdjSZaTy8KrWj6o(6<I$BVTid^dEndr#;|168ktn8Hiyue42dBUK0rETRAr6xI_dzY8qybxPpucvdA@o01D'
    b'UJ=>A;EJ-wnOzNSv028NrJ{0-7EDhkIv4FD!he{B#*rrH%aC`lC~`=zKcuEd*B`JNW~f6`2#twBE-&u6ZU@s!oc&_2xbf=~=q!%`'
    b'IP@>4CUGBY+pvC<&L&-mkA*f4Kr!4qIU)(r5;d)$PEOzaxQnjE7tuTT(L4G180<R=P=pVd-vT~FNVK%_X1r^EFmx__2l-<|jP%!v'
    b'@X0HZ9G;@n@2KU;Y{!zQBhpP#hg}YP<)W<c!Q#Jzf*VDO_VeGUbIfp~%q<Rl231^b_K@kDEl{)O`&NO;(Zx-mNOh6vz{%`%E3pHD'
    b'xf0hc1w|AGIRY`K(-Mg<=iV%zmvq`H%ipp)vBQJE6&PTa-MLFECpb=ca|wb9rXkaRwxpwR|NQ4aWu9vZqXvP9b@oy4FcF_(upQs$'
    b'ixm0z@uN*p>tYZz)M($*cNW2TC^}kT2N`<ODkCRR6(7G=3%B3?iT}-)ggEA9jbGk1!xtBhaj%9BYu@qME?c+QGdZP$j0u)GGF}D*'
    b'`+OkRFaWk<c4X{c+BcmfcFF}{h+!1cwso{jfJJ%mQU3FqO~zH{_yjaI45-dZQOv)djdDn7Zn?Xzm>Vlq*OQGh^*JFBjt*hP$fadF'
    b'syjO@8j;E(>tU`@AP<8maCo&df?=n7=w}o;6mvY-7s60fY_xgF2Tln(@fxZ-{?OswcnWNh5K~9<XDDds8OeKxCP-aL&^tlsGB}F)'
    b'#_(B*hu62T%IhCE5FN;f*&T?8*z;(fCYxAa;V$i$Tvlk-;8i$A{~b`QQ>)o*;=16eN|}Rq5P!UloJWRBvAOirwN+nztq#!DT7ubI'
    b'rjNoJd&z8$`xD|$Y$TFw+|9m+d^Yz-MNZT5Tuta07`(t*@Y9lC>#JY}>v%PMwR6{gqtU6T%fL$^^PWB&0Q!WipwTG-n6FW2wN00#'
    b'1BG<HnD2y)RT>n1Ne{|F4F0^H;)d}h$i+C5@vs{f<5gXsMWBGK$d@8z2wgmikYJ|Y4$8g5s5A*(aURir7gU^5#@B!N^J#Sdu$fFm'
    b'Q?||I6Q{fK#>g~$iVvk71#aX9Q^)@T3p(E8%mwo?+cUbnDRr6~r)_+i6QKWt)A_sMJeY@B7UHmI<7_nc&JE3z{@S(7OxIsM(06Mc'
    b'fi(VG`(6ERDFv$#sbrCX?tjtYvz`i<ecmY4ks-t298?qPk^NQFd0`-vp3Kte?C#l@c~QIyDUGZO%28i5fv#zW!s5#D!cpUh8z((R'
    b'-G*a3?9;%v(diqm!g7k77Z?Fwggz$k23oCSt_QMfuz`)IOEH`7ntPalndI~O+ezf!_C(S2B-x2Vt0@iBfu$wiiHf8j*;|2>7T+HG'
    b'nzmV+24%$&@!><_k}RA;cqpFsl%HXI_H(?p3zPi71B`+L`Y}9Vb^L>N{BykTmybs}`o1!{of;2ZpoT}lV8rM`;OBfhFaQGs(E)(;'
    b'@&kP3qYTbsI)<;KaWD(%`2$t|8P^L2P$B>&0`Qzxk8_ZXau<A_<EbPs5lo`vlQY@Hz${mst6le~l{`>Mx@hulW4>7po5rJxAOWWR'
    b'Pn5HAfvXjrlUTX>SZ+PW*sW=T8YOPL_zW1tX9|=0kAYQuLV{yM=%@x8!fabuXbq;b8xa5`F)?msj_y2Ihp-(ATmkKn;jugGa(bmN'
    b'$)1h9o1)q^b+KrySg_cU!?m=ST?V|(fzU|*2T}noXnoJIQwPJ@o_@)rXrvrVh9V!WZ9uxGPIjj}f<_5(guV`DG9q8AKORx!SQtNh'
    b'i{J64k)rxp&i@NX`HMl(AQuh&lEc$9duZv3XybL}l(h~mBM^!nSXyS6V_tJA1g?*W=Js}v4|<}?mlXYaadh~mD+g=H$2sTQ$SMDO'
    b'88gX{1Epn+s=0C-w+1MWJLOu4_mHL!;PwIoQTa3sN`0Abatb)vQ!xLg%kvBN*^=dmiBU0q492BXVkcN7V5(hB+26!-WFkXgWu%h@'
    b'#-JJnm{W>4>kx7rW6~Lei9rk<Z4}Tf6ovtt^P%AQOyJwc$J6toIyD&$DBT+#ZXs~E{DXD|CbV9G*iPn-ke^X?J7;g-;4w8~V3x`h'
    b'(89SKagMb&T_IO{vw}0ey;&t^YJ0QB2V>fsb?!`iv!Mpp!}jKufq-1r-u$}l+@f;=o|^E4Qyd;)mfWh(&{ceP;dvy_73Wr#DNKTZ'
    b'C3K1lE^V=uRc>UJ8%5=a;h@+h5>7dod>(MjaKa2bp~7kB<!J{D=ab{!{%*IU9^-+M7<~pHQx-leOEMBIy2*$R+as|u0)0c-=`~?}'
    b'-iYOOK&m9J!^F5EoHNc93CicCp?_7PlO&X(!(jU$d=Y{e=sQL_MN-g~-TJ<IyA$yXI4kt?mi~*;Qd=r_w)?u%{qfK_#gI_!jO1Sg'
    b'8OjPdovFdCFq{{ZYZw>6VGwFZaB+5{0Ydejsh(?9s&%K*sKZnyLFnv%RD*GF*(Vu;_e9K5+oDTP1Il2n?ID3j*;jF>(T)Hew@B;G'
    b'h&G~7r==6zqp|NV_zJ_o$W2c?a<ge3R|tW}VY@)4mYh1r+;g<TTu+y{cMYrK1RcJjksF8U5;t^s?GsS;>WA}|&P40&q%5Pin9jz~'
    b'<d}omeQ!*yf`lQj15V{I!p&214HvGr)Fmp-daT)-Woe1<EC)Sw$nl0l)L#6d847P$RJl)|96E`lPTiLJ>!)3OKI7dMIoefpF=Vz<'
    b'tl*z|F;DfQ36D8(<q5hYb3tCWH*=;}dLmRJZs#N}rf@bJ)do;d8HT9GS9>`71^{-3(^oo}dhyyZR7?epkOZ<!%6|wbYL#R|^a@JT'
    b'o6HL4{K;-Y?rgI_t-15|j>#LF5It?-prFx~jb`O&66_ehX^T7(C6+SWYstjK%HYNvBj0kOQ_;7n)1I!XB{Kb>?j=31AMgN-?Ju~Y'
    b'tJ{D3$}y9-8B3~tKT%jrQU6D%(j!6svLbwS7oq%b>kq8+ymRaLx&tk|+IMkr8yo8H?EtZj9Q@RskuJ3E>;+!+1$FQ0ja;%DF50yE'
    b'Xf=5=r}bnF1NajaP`VlL9y*XpzCr-pmkk$42yW>dvtmI>bO~j?mn25>=S}vA8as68_5qA+(?_LXbO+5O1x_ncx7Bm9bUyOM#;ico'
    b'j-3QHERqU5+5w=u3b^YFJhn+%c~T+ICG(<Y!zfCEJcpUhZs+JlCNHq=(BR2-VXFe|0TbYdc(s&mQ4|Ciyu(Xp`RF99iP*h`KPjp`'
    b'>Rb-Bj>W|?)LH>sQF$^CmlJO^qO&x`h+hl~trN#%Fh9{Qk^yoYGe+MihA8`$xI=Bax7qyna*Z8gpgT^(k(f;n<(s>ugkBs>pMQ%)'
    b'XD{b}JEAcx+ilGZ348|^PypCN$yBy9%kQH<sWD<#FmIxovLef{k&XE6NrJpqDy0+J$QY8HmWs=p!(&2)y*6#Fu3<_rv@YoS1TZZg'
    b'^ZdlWyeA1yHl^<sBo-avWiY`Gpo8s!c+vVH-AUpQwao>r7Kjck%NI~*Bg)q5jI8pp@qEC5=?g&E9!N1*1aQ)3A#@NCnC9?b%tvX;'
    b'<~JgyTTnuG(tEHY-;E!NoJh;j0*?mKa@-IhnY@X46Lo}|*9hI!ugE+dz#}CT6bX#S$e3Oc!5v5Pb71m%a{hsqNhu@XH~!TwLr2@^'
    b'+QxL8u?Mz-K@otPoQ9Imu-D}_11xn0CVTH#gOfGZnEISO5k7H}!&KsSf9`bN5Ow41#t=b;JqMOo&ZVoe|AwJLc=|4@RvP;D%>V}z'
    b'iVI4<FLte<KOYAo%NZ#18N(3plP+hgd^aO7<hegW@6!&9(0RIbZ6TV<vlbq7k=&pDWPZ30M~dAivECNMg96KO8NG&X9LW^%GPoOM'
    b'H$Lm<i||TRIF4Wli|{6s6a-i-^SvFR+w4O2)uFFuN5#7K2ld2sB^atJS|b#uDn)&60wx!4UbS`Z9e4<r^Q+*B9)rnXIvL<s@?f{i'
    b'O75CymkroqFdBsjXy(Bz^8>V8uP;#C9=_<dH?!{-S=J1kd4$4_8nVHx-7lE>n*Buj+T;zBSvBCBpR>U*%U5Y%@o#bH>0IBsqS(!5'
    b'uynfe`Sh9>HR|wYE=Lb?XC8haih%sUOcvNEJAu%%w0Wfhy;#dhZ%r?N!%qwd6FPD^a~v-sD3sOD$<j~qhS*R_9^-}l&>PSL4j+^v'
    b'p6TKBDa#p&M);Xwa^+(xh{;Twb+Sp-gU1z`qz8)_iU;;-J7Y00-}b7A1(8H8<6UiUUPbGKTzv~;KVg$Ty84}Qp_S<>^S=cdZqmj@'
    b'lm=y(8CsM_t4$IDL)^rECi5HT6Nnh%b66lZzY@tyr9w&F8iw{Mb{oq)e%yL;8}U#^F=u5WR(b;OpuEaFiE)Ba&F-Mb11RFhNWx=c'
    b'k%e%4^rUrb(S~m#x48`o5Qz|wwLP9S_#}KkSfGFq<&y-1DQ38oD`_UpOBpkTxDW@J8&1|K6_nxy@>f_NDHq?#QA<IeJI86uBnkpR'
    b'$c<Iw)v^b4Iy*V-P>Rd+s=60$)aRi;UU=3tcP!NNd7WLKomaTVQF*%Xr!0cWKqy0H`a#2(%kd8|a?yvbI32l$r!SWZMbJ0`h5lr?'
    b'I<v)da;>keE=)v!q@ETp7^kqVnv_{$q(*yFeo1{E%^%tpKdb{IYFc}fia8PcnW`C~8{KION{TD%z$&Z(=hbq+)^X@OoUW=3pS!C|'
    b'DXKpGoY}DUDQGTbWVqrP)cI4oW_Px`cf<=ii4Rz_OJw%Q_OY-xYRxhWtygAIc$}d1V?AWHffTL!`m!gw9zc^&elT?W6+P*8Xl0O5'
    b'#GM(<4k_LG`Q-G~!Qp9&%4&8}Vm?|T?{{cFv?rFs?Z{S)xu2Q7KU<+n*>KWYeTX-u^rllL&S6njZ>`_mub-h&02US@npDSZdsX_M'
    b'qKg?#Y&9;S2bS_mYyxc<z$6)acs9qeLlsP<!QH_M5}l9|vT$T}b|to;MTR<tFPYufEbi#c9QM<j^E8s{_{CADgQ>qy&N%lWxlh|V'
    b'_G_W{TjPD8Qblz}Tg&INTTka3&||KVXLzuta()nf6OOexs&Y1`fZQsH^egi<e;%ji;~li<+W8yh4Jq3P=-Lz?u)2{7m|DB2v?E%R'
    b'&D6TyOl|1R)Ggjj-HvajW;P?*l<17j<Hw~Zw;6VQkjHlX=t=38St7;;79-g(pn_#RvxRFcTT9m?lU9p}RL@BnI3BrgIq5}B3*%Ya'
    b'pJ%(LFFR+O-8Y^6&F<U7v(Dzx?q268F{>$jjBiQFI!*)+$n%+V3u#-uWGwWOSmq_Myt8@&!a`yUZoL$J`<7@!8|M^b(8n-yb8=16'
    b'9AyO*+3D-ypf!It5No?vU(c4Z<vR@gUI^2Arn0(}j=PS-U>8%kyu1fWR4yIP<!8z+c{dO#lnx<n^O|`k4#e7`R=L>lT3(-!&xhh<'
    b'CPz0<V~`{EPHH}D`Ezhb7dbejs~br{j94AiB9Jq(A(H;cZg~8^_`)O0RDwmZIRGjIafXW0*y{`GFc`+_Sn+T4FP~0LXDHhstQ-^e'
    b'uI+Z@wgeA)V?{LJ$4ne>CLXk4;uW~8o)<)`HUpr9`?OA5kon!6pqbtb+<>q|4}VVwl@(C5=OUs0eV?w9B8f$HXn@mHq7&54S3Ruk'
    b'$;()7OBvR5FbCuX)0K0S_r_VOr;mSe9$z|-hi8v}Y(0M6dfff{ItUnO(u##M@tTs0YaC^*aFo~S8&oZC(q?dODG9Q=Lw&JzH!C<M'
    b'qkmEi%o^PJme9!Y%IEVqZv`%P@fcB2J5wS<?JtQyQ2Ub={%OCC?U2cbM2u(jHVWyC-o*krEdVBNli%5tN?3xVVE6voHO62jDx*zG'
    b'QzoCe8_eEr_s9DIQK|btops;7dV6|uct1E(@;;Dw@$~)RsMLL+%snml!;6aE3zTk$cmPB$cON)PHHVqz?uQr^y$`6Iex^>{4>wl&'
    b'-tL1+^gy^#(R?Oa2E#?~Q;7ei3q9d4Oi28LlMnxz*+xG&Gd(=fyyA-%7d@F!98!zLU?$OzRlO3;i-eqz4rcXX>*z*Qed^i{Jiq)z'
    b'<}XIp<NV8Po_2nsCru_=2GYaTvuh7NXJeDvD6Y8D#UY_&B$DyAN?Pwy1fJ<)+J&#lsQC-sKNbw!Lw=6;aed5vR`#jx>S!Dybu|T`'
    b'^cNAor^g9FuDfhrn{IQE-^u|1)9pxzao3~YDcw&$NAQsTuY!$ekbo*gfVcP1z*@0%|LIkt@3C_Yrr#`SxzGHZ(%;o15fABW99+~-'
    b'3!3y1-`vy5*!p`XXRpMvNKdVWfV*qGNa=Ih@s5Y|It6Of^%zj;ym_~t0trRqe%Y10=*iGP)-54`{8|xWDJNGRBE^#Mv?Q~^=}yzD'
    b'J9``{QTO*Zetm=Pt+lLjhpiVYeO@_+lSOBRm@_50o5I=TU4`D^L1xFcLM}>p!$^jnz{FzDJ6;xeL5~!GBG+8J***IaAmg8m`tjs-'
    b'ryW&4d;JDlYa1v>`@P+xqxQafd3e^_KRJGJ__B9=(*31-)_L7_`EBR$2+vYOJwWW_^sv)yQ?m~kuoQaeF^k9{BWBj#I|nVM<=#JT'
    b'D=8xN(8ZM(9=-Uxl>tmUDfNHB7^YK24`YldGLp99bhpegw#fq|PAo@_kvEZ|C?Y3%u_|?vN7()^7`+sF7^!K<p=G94aB<Kg&n=qs'
    b'?WUUG0VS~1C+MZYzvREb2!@4h)rJ(?3j{|^GQ$tJg32Q(8uEn8u{@f^N&hCfEkBG%kl!|A>GB%qjM)?B7y?2@b}h<z!G1HBqlaWX'
    b'fSZ?YVFAk0yc#ed{lyaOxk(Eb&>OfCfy1zzbKaf2bHhe&gHT2y4&=jw3Gq8d8HLq785|-c2z8Dguns*?mCU+bB4K{=A>}^%vxRK8'
    b'Xcw81T!)FsBB8(oJ7(f0S9-?2ugDv6f4}~a?wCNSM`~Uzw-nfuV@~CVxu`Lzw%q>WRGOGx3*(&t6$jnM?5N6P=rirCailVzk-_i<'
    b'-j^ZRguY~s@<W|uZ%0zH@zF&vN9hhUfV`MW4GsXKY-dclZh3o)&zthucY;2}^ExKEm%jZ14{<NSn3eNBcmjt`)afg-i#&+AoYE6P'
    b'^Sg}c4{gCBpMUtUI!wVRh|!F-bo!35jizKAlYIUU8|F0Zd0TXqCwEr8n8|(9$cvee?HR|pHJUBx%9h=7jKq6|0gCwZ-l-GsDCNqf'
    b'Ec1l?4#@k@950Beal#cE%rBKQA6c*N3gEquq(n!)MR$X4A#i^8KXU?LV?#g5PFb{-vGJfS23_6WV2B@Wl#mqkf}eG|XDwAOxiseQ'
    b'Cz9w!%U^CMZ{nA<_`5ZDG0&9E9n7?N(rxgMa0%4A%k#l=vmDXN!@1_7up%9#Rmr4rLxekVs&>x1nPga%E=K4liYbjGMm2FF$3)20'
    b'ZM4vjzUXZbalR)uLPlT6!6w-WM_=?QoAAQQO87%*8O}?6P~1=#LYovb6$X<Vlb}MPi|JB@CFy#gc!?=(sW2)hm&fx}s<^$H-{@mP'
    b'kvY*?cUx~12-qtZ2(Sa)3cZ^iW?r4fO4A#QN>~z;huUS#K1fb&x<IeZ3dlk#DO<>2-Il|c+)8*E|H{i>)(NPoyfS!T#YzjK1ja+C'
    b'M`fVtJpM<%m2c^AT9u!u#1k7RDH)O@GCIT%8;SS`@wI&q93Z@7Pr|xUo8!a>_L%J;J=z?JAQv*@?8Uq_&T?ac2bWua4(0kq9u7G%'
    b'O6NR>OhA}AJDj5irq1BvGtoXiNuIj6_*nCUA{eXD-lNnPu9os<A{_qh?Cohs$%JS{G0TsCRp+qSKK|8Q4o=V!H10Uj5MO*&S>%XH'
    b'p_0$48uEcSWk5y6p{l3~tW2hyTc|;~`f52>)pR)?e;WC0;#aJi^(9^vUA5WxkCck|0qV)B!)bt4Buj!ymPq6+ql8dI;ltFTk;#|`'
    b'eW&^ch>`Dvi36jj7y+Xsvtd5J0^LpJcEi;hd{L>lk{L?zoSy3Y5hWQX=B33egy1oU+7X2;;vPI7cH_91IbJk5@qwY1e6t#wcJo0H'
    b'^6sn-k#L@?!(*`5_K)6n4}a?5?*mv)cMm!T9EGzw5go+z-q{GlC!v%t@Zeb10RfbatUQ?j;TV_xDo&+fLq=jPtxUrS=>XHhnXV?5'
    b'H6qwt^p1+H(2$c38A(Aw9+LbQO9c`<A{YBcY2_$ExT!YaxVlzypq`RyHDkIvoD?W7h&kzxymRzBotp>~h;axWz!t#?s|bZvNUozG'
    b'G`B$&l&mq5!-?BlSy8yj<m(F2dzGNW<?JC8m89>Onu*h<F0O-t-_pvzbx@rt1`A|#Arq#GHYv6(P(*r$AbI8W>La=1_0M(4gK_Q6'
    b'{0HD~vKLc@c*BC_-|%jBZzx3=pZC8qBL7&^{$x6R2=(ZOc0AM{Qt#7RKZe#PQ)fD(%i2uVag#4xBOv>QJt275^G0}i!F=Gt|0?jm'
    b'D*Ueo|Er^(C&laoVX@^mZ-K;N>zz+wGV&u%LWE)7w=*Qcv$jkFb0YIz=KA|g#+1j(E9LdPUaiC^fShu*P6zzs7U4w(-&U-*74x=g'
    b'y{($JHS2B7yscYr>-2Wxj)P=zWzjxPwjze~L9*ESG9p(dcD&4VDmrAQwH1j!t6Qhds%7Ldq=$8e%w^}K4Efz-%IB$EYdr;)%SI=N'
    b'LRHQx0=G7NK1U~w$|%bT5e6Y))^ermbYd2u6>xIi;8jcK24#S50^ny#eGz5F&ArO61J!Ls3FXqUV_~Xq7#4ut6@W37E7G1;@uGpj'
    b'v*vu*8rOZwKL?9`9Ojo7+GuO3gOlTqKE>JAgRBFFD*9-U8wGj0$><^z(bKM%AEzNkAJKDi>CJE0>R%z+nqv(XBpn$~=LAn)2?SDN'
    b'wdA0aLHLt+E@L<;VI5I;?f>82wQjd<B<cTtiXK`H35O6bx<jUC97j%k?2L14@0s0+6PY3*nHELr5TxX+t>@YI*eBb%_5}cMmNJ<i'
    b'JDDSs1khdRuCA)CuBwkqVBkV#nMB;?8r`T}_e?xAkNnjT<jqCIu3NSfKTWHniCW(>dg}NZokcRN)XA;Zv(tj>F6efpY~8lKb=&53'
    b'>yl)kGs$u3lZTe)tOqP)6<)Qts&!Gfy=+Y!rBcnx+9l&<V%mij@Z{&8U;Y>K|DfObPC27(IRhS-FlfO~a0Bg{sX&i0_sGB>oVfuM'
    b'*-cD`b}c1MYt=@oU2B_R2izQ9Rv+FRVi6Zb?y$*!)Q&SzJt=1!LGMdJ)O?qComeLa_J)8NYT>BaBNS9k5CFRL?xxMb{CdU>ETDCH'
    b'cdL|lw>;k6>e%IrrbWnkIiqSB&xN<k_-<87+d{_c-+ozp_Sw2)vt2qi+uqo0`(v}68yjcKEgcuWRbAsUF58ttJ9jiDOH3EE(aJ|;'
    b'r_^+j5o*f-?RW#U;}6h|O~B$8^Hm<L4mL|#3+#ws11r`<dmHy|X-DXg(c6*HQ|df(!0&f`Lt`gzXlMyqiN$3<lkTh+*a*7!UTP;a'
    b'=h_J^&rWb=f>PK|&n8_Ysc0pT;~)s(Pe*5H17NNOR#sGEsPr0Dh8&2X9@&bAQZ<cge3M&))N_=;g_s^eS4`dX$CxEVb?f|8BvL&L'
    b'5YkX1f<(7V!I_*{o81yxp~#D~l1v#TIllsYQ>J7MgmOSm^<N}xvDV)t$_8|{aMs{+y~j$|nQT#n<B2xM^Yk@mffvWz6>-*qlUE6u'
    b'=UFiqP3~KiGS||hpVqtpcD8$i*STl%r0U>OM`SIQn4F)Um83sf8aW5D-DnpwAX|k5$VH~Hlp0urXy&&Z)qgk#DdPYSF*6AVA^koF'
    b'wO8Yy)&dS<&uP~!HG1Pk>?2}M-}r@>2`+mzn~EDO0H0(T@UT-c7+;v0E3E1g`Jy#wdgIY#WwE8o8`4#2dh-=Dh0Cm%_bJ@io<|6L'
    b'jK`<Es_AJa#XhwjBQ|gOKYQ}KgohW&KTJ7v%)7N3^R~;F*RLXk>P1U$mDxy(W~HnskvAV({(J;|2IkcKIiPmH3d?4_53wr&b(dO2'
    b'Az{3c-M+=hYL=d>4t>k9%@w5bMt9pE-CVzJe8s0Q&tGMI3_7CgI2lR=J{IV6cFttimA`$v8*fME10t~zHjhOP+-0bG_E>28J-U(T'
    b'47|o?2^ghf>ppX_RyqXeo{X<j43nX7Yl{WgKtFJ7JBuf~Qj9hJ-~ZW)i2wBvhXe#Z!=N<X9_@k&XLxdv*+Sh8|CY}I^q{A2jV^9Y'
    b'0Mc?<(Jh-5-4d%6)p=A0&Ebj`5}cuuCGzqD51@wK-Z=tahsC`)Ih^#XUbmJl7UHG><+|~c9x8JwW)w@UTLJ5xq#wyy5HYegSM&Zo'
    b'w%}b|Fmw4`c>JlyTF#K*lag-Vl~@#A)*BCJ7bCAqHZM*_K(QWc{#x`|^Y5iz>->3{y>;37wRf^~)twB0w-SqvWWkE~s7aBrMp8VH'
    b'&xqJrvd&R941e=p;bhoY*T*NbO@%RFmb}}fJMXSy07KP2NAd->dJ9hW+z{RS*BSAF0fx)Wm$W<Un(%h9ni`weu&%;|7J2I{&He;C'
    b'e#aNf*j`NZ-r9U`m6-4CuQ1<R%W3^{to9ts)c+as&TORb>T}TU`X+o{+!jSG*^Aj42J=4`lyfSW%e(%dySK_K0#f15ZkBd$XEFx`'
    b'i`r@nJ3e+*fVK{oQ!D_y)X$&8ES5EtZl5*w)@6-F+I4M~SiFbg$@GSJFC1da3js~S61i5QuaPCKJ8=cHmcKzvgIOj}zLtqgxV3e-'
    b'A|Z2lRh?eP;<N0yf}?QNe(tpIp0C;EyL6kP9z~zQ_vbOVBY4BT(*njXnvHBSMn#+PD?J;5_jtZ&+z&hn)`?0Kx#O_Vdp*9s6*q-m'
    b'-NR+X$nZEmVzR<k?nb#67vv&$ba6p0qW@o{;o0I`Y8JXJhR@yy>l%ly8QrB2Fwq4^oDoVQjZ#!<9Dc0}wP=I2OA58lccC8m(^Pl`'
    b'H${a#S7#k>!kwA7^T;i?Z~r*ogSZZyKY`o@p6g*RZh6iJEUTv38tl4FFkC!6E5TvwdgyD^7DsA0j5H6)t!}Xnd^|K$W8~by#l>ut'
    b'!p@qqmIi4EZ5AM1L7Th*NA$7*A4(K!t!aRzL_Sh;Y=u#ZPYy1NozuhdtdB_as^-q5G8%{PV@<fmY4<$k8f9mQik)?VcaP~(7}igZ'
    b'((e1RL?qBvKfate^QyC<kZ8w@ZDJd;(R#7mfPofX=N+%|T3DOPr@m}AOIf43Tc*$QhK{_P3_GLRY`6E)BBVy)q^h~DD06v52{L0G'
    b'FsanfV<CnG`<PEG4B8^8fW`N{aq-as{9~P_zsemk<T&%x9x^T=f>0x?N+a%gzC>DH`6)a&n@6k@NiK@4Y^c0Q_xrkx8IyxyVx7Q&'
    b'*T-P=$B#>y{ojfQiS&R8*FG;**v3GzS(HTra3oPFwH<NH^DI!2Vq?K;`V@v$IsIO72I1o6v;dyTI5RaByhv6w$ADR74tTt8eZX_a'
    b'A|yQQX|>lqlgKUF+n@IEs$Fv8(`qje94npvth;K~o4q@l9hzuwcD8OYI|?dB8rvdw-OV(W0D<|FwKZq5^f1Xi?oXJ2L3zd%evPQA'
    b'L3~1$DiLrA?JFvn!dOoZ!b$L+sHFl3tA`j>N3a6mmiZ8`dW6KdQup;tUSMPce5XzGYJ?E*7YG!8g=&*1B2u{iEh0-{rVm?ubUuJk'
    b'rdU1Il}+HvyTjiFla(`;Co#6mwhg}pp`((RqSm^Z;!2@`Cj<zRA?6=A$W%T@Axsa1Wan^iI;uf7pvGG5-MVavX_mRluE359)|J$W'
    b'^w1V*jWH-BMYVY;N36+kAXYd%af4>J7L4C0ah90|F%45YSeTxv^Q-7b(cwKg%fo^UDDI(w30S9?!HN56^V5?bo<G(1dcje66ca^D'
    b'fQ3P%XEV^)8}AlU=cq0u*OCgOBBqx?z8<DA<<U%1MCHX6M&nU@)$Ps3vuyJob=;{EJL^v5s#U#5dl}5<yrGSYmww81%_R%X>AnqW'
    b'2}Mh@;@zOO#?gNsJw29ac$+*oH$N+!CEu98I_7#J@aLG3knE3ZnBK8%1lng90B)~{TXq(J-r3F)%R*ng61!ha4>RB}nbE|jttdFU'
    b'<0pa?9zO|;I13q$>%NSjKkQpLiEzS*(O5=8+myMpbOI=?r+AmE!|UDZC5vIF&ZMM;N^+65fP7Rc$B3Fkv|y%js)>&BdtSYuJD3X='
    b'X-Hm*sv>0usKh$YUd5lGz&P>7zFJ-vW{DEy7CkMvbDLd`g+*f#hVswJ8U_jk=~7gKgk8px-dAnG$(Gej!4^h0+Cd8|Dp}%pn#t8V'
    b'b$hi1n~*>rkH-Hmk^gNaGOF_8M1?|`e>eP(FPQn4bwqQ}l!#~7?n(lhZ%;g~S|X$u2_2!wiXGc37Bm?bL=XRTx57u;^u*8Zx<)t{'
    b'Ld^WQsbpKP@0Q4N3tR;UaDy)eg40s%W1-}s26ByC<8L<N(D2k|`+=!>`8zA1z756SEeuX^YwZ(L%re5(v{&0|<Xio#fSK16$-ET9'
    b'JcnR@Xgv7r`aJmT2BBxe-<=3I6%_<6CsUjnBwz}KE+32#^jkc*4piLY3y5vaUR%#R?y@V@Mlbnz<OL*hYywUG#P7j#NVYj9A1r{('
    b'xJ@gsa+HA}=D&OO_D30Xc$NzBv(y8+8=(2dZr3BDc9qzs-orv1Dda6aN({`%ZuFQ!%AzkfjvWo}86JeURlq+_|M9(r1F1`+OoDwR'
    b'lAy3`c7k4DArQx$j}-6oxHJBGcy@F-W|7~W@?(-@(x#`2ykNn*H_bn|d3G-nSJ_P!h}U5VdY}Pw!IZIUo)$pH>9XuxrvNXC>!aFR'
    b'gN!S{p`(10T6xmzrI%BlU6pU9hRIR*o&+jIXk?BA-nU(LGoM}<52+9Vd%Y2C1q)6rik8b}&>bjAv>j>sosR?sg&#EsFBf>d+YR~+'
    b'q&&=W4ut?OG-%A{`s(?fz<s&kz8q7KJelL!SE^Kp(RUohXu<hn%nUNGyAp@bZ9F(UGOp&MH(dCYoI7saHcivlGJER>2N#57f_rdU'
    b'H+=%EBbnvN66*n2*Y`s&;dy_`mRH~b+6(hHN+=EWM0t}-PLE?)KJ;EiulXI%taRj>I#cAGv&FNzzkV)J$ynh5oMhK(Y7tLibM+~d'
    b'SGddbk^QBU+$E_ePIuUo%s*7}E6!BsaYMfATo&(g5>iEm3dCVaitpDq<??^aEE_DP`p{&($qdv;uRFqsZgle1{@!evXRXGw*7l)!'
    b'-P{IM(`qN}1A{gRwbcXRenPo;T;~y2IV&wRK?Y|dD%C<i!E#SOadjE$@cZYlu~Z~?XB8wW>JzM+Xbp%um1|^s2g?ph6WvT(soRic'
    b'nnX5jgug^ke@KUz!cRtIEH-8r>>n_^P$+GhA5du~L1iykI_TSwl9HejL4OhonfAt%!<hVd^yK>nNRF(*6)maO<ZRT#V5hW?HWY5}'
    b'adhQ1sajzab|;j=$o4bMc$BF?a|6c!`=Q>kFFKK`t6LeK=%=3=cy>j$(AgN@Yx=tz8=Lisb`8b!pQO+y`G#@eH@zx;*sH2v{#G%)'
    b'{v`Y<_G;nz4<2KBrhX<$<+BV<uTOV`N?dyJ&L;U6I)Bv5jf?ICY!r@%w_TN~WhL6`W&R;@Pa<K(t)xB&5;{iH2NcvP*p%=U7E`DC'
    b'0F=xrs)oossIi?)->P22{Fd{ZmQjdf;Nu=xqk~bD8;btK9|w6i9f<y<F$Pm<`iVqbP1b`hg^nF6TrU+17UYdg-#1r)ymKFtD-yBk'
    b'34|oip`3S2@fzW3R{KsPjbx%rh5~5-4HaK@C!jZpt=o<YDpIKrE1W5T!^w{oMqjqys0N<L5g1yt=tZt4V?6G_EE~71gAkrMa~IOA'
    b'5j`vPEDM?5)Cz`GdR&_kLz<Awm(WBjw1g&tHVb%KhJ6jj4vEoL7Lt>bV<BNA?OxMX0&Pf9Pun0#-^W-N{W_kGF9|gAz3C1ya>zSE'
    b'LuH6DP_WJ6?XR*e3}BW{t|+%@YP0NJ$q<hi<ox()R9Ckk(GF@wHkx2ZoYNi*8Kv9rqj^XXEL|tlF;51T9tXCJ8Ie+UO1Oaq11eLU'
    b'gLV55-<iz1L*DwkUgaoIOs~4`Qt=(Q9~dUpCN7sulshXCsucl>^nLN<^u4LEUEQW^rX_+#fKAKo;dFEr6E#Z=;<<Gr%<3kw_T@ji'
    b's#WYoV2U7IY8M9_TsrAu0hLJ0wQXg6x4Sf!gZReaZLl|7jF;&M4Nm5#1;%ndV$BO|tNdB{S4d{eY4Fvm{69D8+v}!H6rvOpKSa^E'
    b'BoPfo{NpmwTif9YOg?;)GRB<8Q%SsS40(`NV?(hI*Ck9vY<Y9}@C%L_N&5i~WGqK&z1j2-?%Ty&!;FODULC&g)5m?5cI{pIcEFA='
    b'l)57d-&IISEKy!ne9%!p7hIb0hNg?oH5SBlq%#I;CeHmuropQhb(c;9yMsZWHUu29fkQE5_ZW7?mz|OBIwd4G&Gyr}__(i-+9)oz'
    b'mLkW}sk+%W&5!BiBApI;iR}i9&0nPI@5L;K@pxDz^G9|hAt2`=?jULDa&D)lyVkh!7R*vEmY4i|HUI>xV@cgms+@)tg4Do$7iMSF'
    b'*+JN)vqGjqB0MgECot0)2=Q`ghXD{NPr2ZcnjvMe!5|Pu>yVE9hSQTF{W-qs4qYoSq{qO7W{6|TpVH&;Ieb4RxI6e4rwabTN8w{='
    b'mJb)fm&!#DBLS5${k)k@CUz}&?8Z}*Fdri289|*+(~&Gs<o(?S@Nq&I3k(EEEJ(?FwV$X+_)BQ%x@{B5Gf)gsqt=ULe`(K{cy6%Y'
    b'=?sjdtS%g9liF$Do`H0gOF|6S7G?VMv=dwEr@bNO$OtF`uMcS9Bz6Al(G1>qLgo^OpZ6zYl0h7KJ|bWUrVFQlBe-EnVK5TdNWgL+'
    b'b+Qkz72=Rg?|tlfhQ}!Q1{re!{6lo%Mf%wlzdJJ3-^x$?Y9F&Nc+MQf7Ah7E0dA1?nWMfp+wn#B6DUYnAT8LR;QLk|lAfxXFNP`*'
    b'($fqRvr$8<0JbsJtnpijAoH&FOEW(BmHs?@7n#k6jd!iaWk3V%68KHHDE<Lk<4jxllfW(TPik#fN?0f{GBh%BywIdgAx@ezwQH<#'
    b'd;m5*ml%Y{J2lq7A!1@u0>zjp)?(6XCi{#ZP%S|pOy)rxCJw`}&_oWrFPV!In1n!p*wC)ukcW<!l!EUi4qXo)-u533@a2*@ICe=6'
    b's4i*kBzsjmiauIfQU(T>_-JoPg7>h44NHocYDo@t44>U`&jwgkNhzXNQpCK<HR4c{k|Ly3k^^0`&uX>F&-am~e)-$4H!Cr&6$4J7'
    b'b^JDR?22Xkhbe<Feb$>CFw*m9Z#oI<xOh^gObWW=(W6JO(o){}kRl;SZetY>=&R3v!7n!z#kBZ~>KYIRmsEX|v?EGB6)Fv0d~A?L'
    b'0q6yH(sTe77Da{im@`xThe)Yme>n&Tp`@b05T`8+k-#0^7c-rhD&AGCS0mSsXvLDYKI=O-8uf;`sYny}AKswh7Rl0HSjZ8{;yQ5s'
    b'RwT;B9|m=vEO<E<!z>Kpf=uM1#zH7veYMJ0w4unowhaf_D@`doeN9`sL9ngWYK~E3k5v&ppxC^y5b|DNlxz_9C#?00hA^)|MkhkG'
    b'Cq@)Q5-G-)fJX&&|2#0Hlk`LPYA~K`n%5Yx1;X*z-B`^8bm|0D<T*wHPbXc%sIca%c=(54NwP}@b}MR938WPJRopMK4RU61q0{%U'
    b'*?S0EzxNWuoWa%|MNP)h6E;?Yi5rf`mtxjP2gCGqYGj{8W;xtp=)`??_F?LblqtQJnIhcA^a{p!Ixy3Z_Hx`c<jTXB<Xd6Eb+6A&'
    b'HE%U6#GTt{d_L{8Zp`U7-!y)^fp6$+fUki~anZdb85d8bPxHt;($2yGdRGIx<lSd&c70l!LJRG&f9b~m{p+`#cN_2i3Kz54NewSF'
    b'>XizJJo+lv_!nB<H+gf2Ji<Ig<e3EN&u>wtLwMFcbSDU5mN0KQ)~Xjcr4zQ6(<ao~F`ldmxRLw8Ji=RJ9PY>R`E)QrS36vUU$~RU'
    b'o12?-tkVP;e#&tgbX><Oghm#hJ)ZPB8!i5b4RkizWOsL}RdbGmOB^@p@lyVP>051H-B>S_)!pAn&Cz4uqEeFA+BpC9rn3Q?mqUXr'
    b'Ry$|>qeEWAK70~O)hbs2GVvHTe3vOsGyF&|j)MTRql9l@SIz-f^--%j_UM6U1OdR{JrMYdv$=Ibt2f$u)w*lws{~{iLxl?z=_S0*'
    b'+LN7<J$C14ZCGNA4H;Xump?;G4<2lwGJ1F;ddH5qxT|l1S%+zxi<owxfN2No;ia)>D)>+Kj5*%LJr->lsaXPuiyt!y+H+kHXsXWm'
    b'AyEVTP;DixWFEGnrF~z~v04JGi1dlKt(~-!xfq6C3n7AGE2>&+3uT{bAtY^pgf&5%w9S^;Halk5?3sOgyDu8ScB&P|NzDhi`pb0i'
    b'E3937+XoMlhc|lVqx^XPVPb!C(}}C%Bi&!&&v+Yu%-B*yP9d^krI6@$U}1K>AcN60Pxh2bpYbSAO&+=ATqVcSDYT%$gfziQmZ`xf'
    b'=;fwi#Zg~3(V%rvR9&U<6T{Adx7hO$$~osCK*zxK*dh!d8`bF-hB@T#U2{Q774Q0%E>I6ZDAu8?5!YNJwjM{!jV$bmywsMQA4GM2'
    b'p%bYJY)Be%U?^3$0!G~|@F?&?FvF|x?4I&$yM$+fwZaBh;o-d;54T-|twMwAP^hb_<r>_|GxhCPS%K&8gNjIpLryR04>GjpI&Yq~'
    b'oBO-sOH^BCK#(#+4lF?QO`5LB*^DeA!s3`sfIXS<m#?J!iY!?a77Wy14j$j<dHt<aMzpx39E!*(c8QmlMylSPouOF<*4_{U7zta6'
    b'EL?_<L>HF$Lvt{rB}kqT+l8bgS^BbDcmUR(VtdkB%A0=2Sf-;Riq5z4^1B%Cc8Xs|_tBB5HtT3CIaJ|B)-aWK8`i8Mb-&TTzm2MO'
    b'9jRWWv+|&2*cyEEO@1ER>jIh{SUl7H)m0hU$eMmh5V0~NFz?)DNspr3+M?Wa_`G*2DO!(vZ9mWf4TM9I*niC(>Cv4bZcVPO1$FMV'
    b'!u@nIOBZ#wyY0$w$?My~`rP;Kc6sOCj%scx{?$4T+S0>d+a{k*?rul<ngIp8P#?(7L#~6ZAxk?SyzZXE_T-C|MR2cqsJ(LRRtvtG'
    b'gS5?|mu9^Qg#aLeD-xYUah2SdI|6WxV=(6jqkH!_OdZGnzK01-5?UZLTNOp)*0GN$K^QmrV!gk8^7@CPw_y7ps*SJM+Ljp$&%F8h'
    b'=xO;A#G%Fe|Ks`Fqw)s?o}uuF0OOWFMBojDM_xYp?&xLt15&rE`0}p0SLtKGMkNFG{N?fA%OAi1jYu{edfAPQ>`o%{)2r`~>}I8K'
    b'pIbR{r~9FBFA0<{CjKC|;`iK54<j?nx@YMzabZPGDOI?MK`x<t3FnmEEW$t7rmzsUEG;PpB|qg}%eqbJcmFlQ{k~kE$pt>1Q=HZR'
    b'0~4_aIR'
))


def normalize(data):
    return b''.join(b''.join(line.split()) for line in data.splitlines()
                    if not line.lstrip().startswith(b'#'))


def regions(data):
    if IGNORE_NONCODE:
        data = normalize(data)
        start = data.index(b'localnlegs=9', data.index(b'run_regression(){'))
        stop = data.index(b'selftest(){', start)
        hstart = data.index(b'localtblock', stop)
        hend = data.index(b'tblock=$tblock_full', hstart) + len(b'tblock=$tblock_full')
    else:
        start = data.index(b'  local nlegs=9', data.index(b'run_regression() {\n'))
        stop = data.index(b'\n}\n', start) + len(b'\n}\n')
        pinned_lines = PINNED_RUNNER.splitlines(keepends=True)
        hstart = data.index(pinned_lines[1988])
        hend = data.index(pinned_lines[2039], hstart) + len(pinned_lines[2039])
    return data[start:stop], data[hstart:hend]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', required=True)
    args = parser.parse_args()
    try:
        candidate = Path(args.runner).read_bytes()
    except OSError as error:
        print('TALLY_AUDIT: CANNOT_AUDIT ' + str(error))
        return 2
    try:
        same = regions(candidate) == regions(PINNED_RUNNER)
    except ValueError:
        same = False
    print('TALLY_AUDIT: PASS' if same else 'TALLY_AUDIT: FAIL')
    return 0 if same else 1


if __name__ == '__main__':
    raise SystemExit(main())
````````

## Full source: comment-only and whitespace-normalized shape

File: `/fast/scratch/hyaku/tameshi-r32-seats/CtlRegionDiff/lane/tools/tally-audit.py`; final sandbox commit `4d6b2b62aa9ed424d4eb2ec17d7e0d3ea68ed43f` with parent `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. Full source, including the complete encoded pinned runner:

````````python
#!/usr/bin/env python3
"""Pre-data control: compare only two pinned runner regions, without executing Bash."""
import argparse
import base64
from pathlib import Path
import zlib

IGNORE_NONCODE = True
PINNED_RUNNER = zlib.decompress(base64.b85decode(
    b'c-rK>?RpwXk|_LNSCNh70c;8=z9f+Gj6SeiV_EVm<nHOQy|{ovDjNY!fn<%XdG;RO_ZrS#!v3F2*(-VDE3>kSLXx|C&)MfW-knxa'
    b'l^Gcs85tQ785#NLhte{fm-@k^<WH_t-wQ7`9;wUa!dv)`HyJwf<)j#1sQ>!+|4*I!6Mr5I_-inoDEJ0%RBqv2`r$?3gcsA#%SkXP'
    b'sJUBqDg|}6`?}Np@z6QLpZVg(BY?es;X$o&*i!SVQ&Blx<`jPA6@Zz|{GnQ0_yT@M&1<o8H7w^1hamuSoVkBK_rnm-DL|zlREz0!'
    b'oDJ3VdZIoD<FPY`o~WplI>+C+!E~~idxM4Q`{U_#eg|O98&M-?4X2h@7v6m6PeN!V^v9!xA1>5&u()948tT$tcusij`!i@ST+Xk8'
    b't6*{tkOtGsnFsAo=R~W?BE$ygvt?NNJegjP{o%P^LXZx(0JWTXqj)*YLua=f7eGXq!0)_TEa!xW)sJAZm=Y$VvF|U`*gsbUcur&G'
    b'U-|PJ=r%Mv^oM##vEIN7ksh<LcLQ|x7AgSrW&x0TsHXGaJeYW6_<j{IO)r65^S~Pi|A6nK`ScRYBene56uNyLEY!6B$p=b?&|jeJ'
    b'M|=gGaIKyJl;^EyGjDP6{9{1{mzT?l596b*r}NL)=f&Lj0n~6Fj28I<)7JL}7uXqqt+BVp(F+M(|H}+or2gzMuf<44+y>Rd>G;YI'
    b'dAO!aVCHQi(_pzE8X+Y@RWHG~fA-D;0P#^qX>j2WK97TNA?y#>e_mb&I4RV}a4-*M3n(=9g3HjMvc=0!;m5r4FZ=!wG4_x|G&s<;'
    b'3k4HNg~68v^(;h`EnYiy8_dsCA%u~eK*3Aj1C|0%$gc%}W)RTrbC>Wlwq8Kmd<vcDEjF_q0rrFQ3kxnl1Y8QMV8iKhKJcx6X~?k;'
    b'0KC$OfCCFJNN{MZ(_s$+kSZ&Ht+ym0-i*BokZf=<oogx4R=}?l-REi%f5CidHJmLP$_yd_^YLOjBoPuKXc0?U919c&C{Mip*e4MI'
    b'QVaeYmR3Yv3uYGbv-2E&!+(6{Yh+G<)4zej0nFJ&u((mP`E)wUXGBEBk*pacn~qy%ELR!>i057aQ`?JA?#t;ArqbNUVyZudabsrn'
    b'u;hBNHk!_b@2HC~RY1rPemErnL2D|MnrZ?B8iJIApVQGOBpk7Xo+Kg2E)ugw>JeC=B}#pgJB~rdVd(=MR-IF5jDe4)W00@Tau)7b'
    b'Lde11I5_DXGu5!-+xkwjjIfZyvyGrvNm^4cnj$1XhIpezOJ$-tJ@+qxvI<0wo|M=<#%k#I7nwXw%YcO$i3*^FKPMpr49L|$Ocm5*'
    b'x&X4nXaG@)>NT?&j6KX$U{k+EB0nMC6Ws_dp{uZ#EU63s`j4{num5l@NzLm7U;_<}0G$hhIlEEQ5xf!cJevcZf(gv*DF{;k3$9=O'
    b'5X9{a#)C@JKzY#V;MXOr)**6C=+75B%0pHIc?$~wE`2bJz*;-ROa8FLs~0q3WG;dn`XiVKJ20cXO1%L~CGeMD0z$(#BjNM}p}DXV'
    b'W6ulU8;${Ap4Nwx*>V9B+JlKXKZhl26pVe40n&^LL8j|>Ffbl0sUR3|F};M}MfC!fQ(PTz#h@B6Q%Ah!C&+Q_6Fz?EBS|OBxzr{s'
    b'GSlUl)e8oHKBe&={#m{8=Z>HPLoy5oi0rGwqodA&%5h=;3qb#&t;%`zO?BU%{&e_L;v;^+z8>$N9Pb~!?Lq;NG{L1mh56)GY6Vzh'
    b';cuhlR<>Y1a!uqfEu8X2b!O0I?wlZtsOx#KSoo9HI))+9WOxQUnBW@vhARnDHzEn@E-B+1gsY>=<9J{X*K`gFg1T~54#!{^0RJq2'
    b'k%)c9#H!gxSsFth)gWxT4`T5%eZ<ZM=M#WG+)+m_lt01whQm3&$+xI6rT!vg@+=rW2dY0C`n;OJ+<LC?UodQ`ce~EtJ?9@~r&;Vd'
    b'AD-?gtCX73A8*XyrZD`^7XFt7*IxO@d=xI`fC?%rqX2LQQT*!?IycNSkcof&03f7g4Sejn%3XRlKw%IoGgvqP?$96m3qLQt?1Tev'
    b'29gWb0$5!Hc1yjV!02BitqSV>0!FM4f9God6#l#iZGG@L9D~YURJ#)xb{McZK{Fpfoj^e_@Nqon{%9EjL*zzYFb07-#UCE6KQf$`'
    b'z$xBmKLjT1U=PMO1P+Hb^tDPG&Y({s*qKSpu<sC;f&_)(1ttPTattB>3CWd$3Be=ggAVd?7J|q@{fJ8Bf}&qkA8C|6s;8!Cfxm}5'
    b't>+-B(3}8RI9af;4A|uo`Z661mUAA1F^~njpJO=)9cC^EPP~!X2Q!cKe;L+xn|UPX!Mt>)GZHCzi+(%{y0&mq+MH;itw3M)Ums8%'
    b'Sihl{AJMQ<&H!J3WGNjkhD45MrJ;XSnk>iT0;7sk2dWiV+eQKmJP^`zn5g?d9~8`D9HPjXO|ergLjU#Kv)$t}WIwMD>)8^pK;2u5'
    b'18=?vM#z@1a6%Jg&g4i=*aAXy2>TzQ5G@+{=*!ve>C4X9x(2m1LEzq;9(K<Tk2@+=EHSvBPflMQ9G=4Txk43d;Fr)+5cZnRnHdi{'
    b'FFN~Yy~6{g7mff13&ic&>B$jdzk)AR>ws)_2B=hppca7gHUQaPHUgLy#vS5`2`t(F@aI$b2GhL&Bp&#)1%LqIZ6tYKl~9P&f48*!'
    b'k4bT;Zm$7F!oj<ojs1v4vJ*rov&rL@vCPaYvDnER#|elz1(qOXB8<)5d`soPHYEB*@*HK$ipC&PAKtPyc>(O`gCUXwI|=4BuoA6^'
    b'AOqlCHLv>10H#1}rJ*&MCK0J7%gLhMW(@|(hG>D}Pm5rvDrS~}*)usG`_WVb__e$}Jizp#Nf?eGph$jGPJ_*%auH(lfF2SYB&xT7'
    b'sow|YL-RRT&x@Wpq0tC=y1<x$@&ObI#@Opdp0qhsJ%wsdP2;>6LZK~$Wb4{E*Fe%LkbCr=sUS;mKx>!bKQ66RN1+bdA*0Akp>loH'
    b'uVG^P)LpEBJw^kNY;Ueinmv-Fi^>QZ6u@+jTdj&i<tJ8FctzzI4WfTRoXo2Ye$flMs5bdXWSn(+XD2XqO8VCU{3rS)bKLyyzUk~k'
    b'O++YCfeDz*!IpY?+UXpBJ4Mw92d@2J|Ng(!aLFv}T!!>p)7xQs<GZ{yziGMG>en}|YJH3ARqKG~?Y^CMx@RY+ot8Rz_3hyF@WmPW'
    b't8mDjnA$^dNcEwo1eBIKI63ZoJLtST-95m5F$iv)q!9Ot)oFUvDmDEGCNQpp@iK%rrXcYZ{(2m5s@pkx`$pxS&B2%kB_}V`*2}l3'
    b'X}D^`;>rdBd7+3KP|~SOZw4w0h&~i@LtMW9^`FY6CkN+)W8<T8x?6cHRsj*YSk6k+9IW8~`cHt`s44hy4)c3HpU#=@Vg_ptEnxOu'
    b'S*|E;c!t3j%kx1l4)#uvQ-Xa76JUnCF+s_=B+EVKxC#rF>nbFepsI+=2ujT7fzK`?W5{S%779NRgR$>2AyBs(g95{ocg67}vxgj0'
    b'0L5}Z@kII*+BTkEAC2{@J)<S<35gkmpRmGq$t|ngc3BBGpvC|T#T=GwKLSfOvw<d7XS@`;Yw2Gq#6`ILyqr%XOw9`el^r9Af&{fe'
    b'5F2rbm)>yd02PCgEaUVd0nI98@WX#Kf>?_~jJe;`x?U%pbOLd!<kkV=mWGH9Cd*TI@5m(GdIS-0+$viTBQKk}f2`w<IxJf!h;<uc'
    b'%)53U#1$W18pO!0_5d8?p1D;VyWC>yyB!^FVU6D>Rwhv*$$RS{*<6(lY1PN{um7l|ptR~{N&}`#*&}LDD=tUVlF?kbh`SvhtHj93'
    b'(orPiD~BR%JHHN8rC|+{JzlFonq(UtAvm<|@qJ*s!9noO(6{KH15M^4UBQw;2g48@Ce7-wQt>=lYDj7tJ#g-U>_!Pn0#gGvj^9eT'
    b'(r{4dmw8bF6}8!_xqp8+g|HU?x48HMi-TK6P6UKeOp_9P;g5%=i_O$7!h&*l7aNtzu<8zfR~IX$i{)0i^7n_0+?xLBWhk|uyP$01'
    b'`e?h#SZ_4WP1?tz;SZJjU;qC9*2se^CL~x3s7(4H7#6^;Tcv;f$2R;Ay{DkV4VPebf>jiZ!1O?`JhTQ9`7e=Kjmss^vw)OxR{oJ_'
    b';ytk3P3VRS4UOE|4z1Fv4mdRk<=6^)w(Ynj_z!O27zbd8TX}vkSC#txSft>9e){pWAL8y7DIkP{+DdRr#2`KntMFrk%RoDQV4F)z'
    b'Wq26Fb6eY>bbt1*gAnXJd*T7OM6<EhOj`y#bJ&7igXpRR4Xb6Fdw|dJ$r+Hw8%7=j-V>C4Hii3amYPIP#ngShwYz$#maW;?qi-R4'
    b'QN37$fCrEt3{BqOLu1sFQCii_a$4de0SLR{v?WY1qx}(b*$l`V8KTbnV`mriRj{_S(zl#M^BY|@U?qAJV0wfGW(r$apgFRCHP(H!'
    b'pd&XZxsd!{m!SK`kOe$;sF#;Ph*m8T3)JMR5;7a2LS{F92IxR*G7MRn7iGF2zFZG!5z=syeta3ATFs1wzyKNA0Rr90+ED$--nEdY'
    b'7@LP!ECe;5-214GT+?JX`_;f}{udM$yceW$D_Rp7$(hY==jcTy5BT}KrAJ<I={Z7B{Q#YCQxI3>t$JNgFc_A>1t6iGe#s8mezIsw'
    b'a+iD`n)d+mgqtMa-)IT4X8-6Atff8}C0Ek{i|Uw}JVlZ*N-M**W3fAO9itTUm}C20T(*ZXwO#L)lXSvLw6!Nfj9De54l@^8Rnco5'
    b'ii;PSKN8-fF>XEP#BZXf@EoSh8m2<e2TkpQn2yfSA1^#rE@-pTxG`hANW!lWGb^DEIcC^lLLRL`iVe){Py3aN>DZrp<Q@Gct?LH9'
    b'sb_8FitO`{%>aEj*3Z1`u!#%UA9>61g8Uz&;L8F!?hp&hzNOx216G<30y1N7EQeQ79kSz_+)yinh4g;2+wJb4BZtZbvN!T#_wcA_'
    b'8NIeqO4ctfW{d*@U_1CZ^o`>nu)4}wd*UqPqgG<E24Ww3TsP)~GRqP&ga`<Uk}x8o5EBmt5$$AcYXL#k$zwH{5^}U(l$%$}d6@w;'
    b'@+?fl68e=&3;>C?#BL6!>^B+?6}*-h5sffzM36)RNEueOfj~C~smzWY>_YRDml`YteE?g6y~i-dxHw6p`Jy^P?-Sa>r=6F;Zr#I^'
    b'W9?S5-iT|-db78Cd=P)r`P&<G0F~mf-W(qD9@C8HY>O5tRvpz-t$fIusC{_EO&p*jF#xv1i`-&*`7pcN04X0wsQYuL^CpSU+3wy^'
    b'qATLLGFT3S(a5J=36KB@nESik4gie3)9!EkWsBJM8?wST8n~kB4(7DH%%{^uOI?0m_?I)~AoG?Mm$Q-%#=<FXO@`v%=pRlynX5ZE'
    b'fv33X3loec$8s{pEn~;|3?!qN6MweAuh@Kvn%66su6m8~+;MQ>AA*#;_E34a0-*~NnngHD0rD2{*pwXEWDQH=2Zz6757bu@!e)=k'
    b'ayN;evm;t{OX=1S%`maQsdaeKBaJGK{=_0~!s3#H!7tNu`?JVREMY`%aS>jrTreylqm*z*F^}%25NIdgX0+d?ccVo*me4I((k{so'
    b'<0H;S4F#3HVzhqIt_jIA=nPG7prf#A=cmJi&hdVyh#RjsZq}HmjrdXzwf54P=^UU%F~9T|!Jvf#l$`vy3Ip|SwA9v9=qbpANx&l%'
    b'!mkm`Gytbdu?51iU=;}?)`jUP{t4sVNc#w*b;^--3a1P%LHxw7)9Jh*i)`eE<DJmhrZn=Y@yjA13r3jYFIbL;%h@;>VD-qBC;;y0'
    b'!<Z<ac3um-*@r9C5EUJ*<7u`nu>Uh(FuUh5_oqKOM-H5FtU(C0uxOPFCJuV~X_6HbK02s-@TBt=@ulB|`OkWU3!FH`jW26u;x)m;'
    b'xRyx2FnSu$^u{h?zSz2mteO~kVd#eH7cWP&B2svv<*{}PqO09Fv`ipnU`cQoaf2N9FQx-yw>2$=vq+AJs~7{w3asFHv<n3IdDq?z'
    b'33psP3*vSqRgI}klHZAGf~>A_`#PY|k$6M-7LSSG<rx24T0s}dhT%ZiC0fG8MiKd^$Ddf!iF7D$eu>g>?h^~+2+mf<Mo1rOzjzd!'
    b'CuY0^QE9&dddvMUpu-MPfyc$1eCO;-C+lH5@tqv%1#+mvFY>9kOiWkgHW1aAHwAJ3Z^#{^=*y&X3f4$~!?c)!9zex-+(n^a8vy1t'
    b')zH>Bs!lk)uub3zU?icMKXCe}t&z!tR10ydolL06fMX*Adq}1N3lB0wNFeQ)X(sN5Sj|SQ7F$ca1?%t}=%Yms?=@(Fi1S~}2olC<'
    b'PUoYwmUjPRi)C_oB+VCkj>;k%JrpW4gRy}HCP3FI`nG`-H;aquq^fdcZ&*=FPuUef!vS&zXFyDyjhR2J7C)7cQQ0*PWuiDDj!5qX'
    b'P%xbSauJMy(!30X%S-Zs(mDbI%e&f85Pl4y4OnqEK&@2HQaMwYGczAG&5ezpI;W_Vw6m)L;>^$~q2Q4xD4*RxE3>_sn{!~;XXT8*'
    b'^!&QF+x@ZEJ$ZY&-+5R5aGS|*Y`i`>=(GX!25&#Mvrre*Li+pm@T`LmqA%g&(e7U72p`T4Uw2O4p7pxzYPk%R5084s?d=WJGJCw4'
    b'*mjjt@!hMI68lFvDzbpg)Gly*9T1b@yf`|1(<Lw~a4x+s#z<oI54DR>U4?P`jpo(HE6^+3<!Cb`3GFkvel93})~I|Sc)=(YF5K9l'
    b'Whs|eUpEw>xKPiYWjiM?vKzlMgdc|BEkbSq*i}$^Ra7qyK?yb*oua*AI|Ak%$6kdW)_}2=(07p*34{6pe`EjG)znPC=JSO=o^5PM'
    b'$RU)8V~i0iIvNJVBm+>nnA^aFJ?bUHijK<@#8|J@N*JTcNpu_^F`z0DW$0fl!m)5iu#m)vps^?>-9}2(*~24zR%2u~PI#o4Sk_2T'
    b'I9oCv2b8MsQ%1S_tmhx^zNR6dVBAE+gasI=;8O`%x_JN@kdCN47CKT0SxEELM4DKjKo&?n5M#O$2DU|EArd};ezu7Y!LlH1bA6hT'
    b'(Z3i2W7Oiq=4`B*xSA3tHWKGG$XSL~??x`Z(_Bc~CoZIJ^%hpPYYQ8z+pUG<hG`+b-&t7MtSrPg8}soqB^!4gCDG%4_d$}4Rey8('
    b'SrS(KcJ6i2ZrtIb&0CIga@s{(B<sTlw3Dv2@qqAwm}4u)s(yLJ|F^-)RjT(-Bu%;#FzEsmV`<~$Rh}JX+ABtm&xBJ9dyVr7rW{!;'
    b'<nLlXx{@vaoc3<TX<Lfx{iV2H3z~j$w~w~#`*L7r%z@+RWD?OpUSe}%i}X|xND8J7;0x+X_cw$i@7S@(IubdL67a5|<Bc^z#OZ;<'
    b'(Kb~|04hn|HQ~hfgb-srHeEvs6MnzIz~J}qIf{`&f$t6j2AWCaSZD?Nn}~NSzWrM~lyQBC(Z<>kqtv(}6IE2)0F`CqR+O0@`cFio'
    b'A$Q0~CG^dfdK|u=WI=UwGwS)DDo~K!Mf^;G_>CF@90q=mnoYn<gjzig^9gtaqk<rCN2GV<jRit5Qt#fWO;FXwP(XeArksDE4qI_<'
    b'GwQ<!vP>qlI7gj9z_PRADFC(fGf-j_Ab3zRdee~rA5RBBnG1Nj04>?*>afl*Zr^BA*BNG27F1_9kIkDds!UV?)pa_3Ggna0>iFXj'
    b'yLpkprqO=fvd^Jy<<-l>v)&V2yOw>GJ1)EGg<E=oo4BXt8i+2p(yBCJ(xEB=v%U|i5by)8T)6)PJ;hLEK60UVZ_cOWU4<3o`~r*g'
    b'24mlww8)E&Va<*XVy3pq{|T`08TI?#*=YyetoZxz_@MK*9w~4+Z0lk={S2$xNA?w<x}cmd9}8qnLC4|$KYhZzn#lrITaKU2^UT0~'
    b'S+oU7K7<Ux*;miRWAohXw3$PeIs{vM`XRP(Q$(s@w1E03xVN7nZJw8k2$9sdHK)vCp1F_4si0j(AA?D-D0#zSi7nfY(G0eu7zDX7'
    b'Ofht6;;<m3xqm&ME_lHLA>@DIO&>6&@t|nHu0Rm5bmGS>!~(^iTm|##1SJk_f3aS|d_n3M)FuAtqthV3DNd2EQ<R~&PJjYTwiL)^'
    b'07o8?999Pr^5XDi?@57x?Y=$x@#IwhIy>Fn@4z#LT^2VCm&B%p<8iy~T;9Axgy6^Z1+E&0FS>2s2Y2T5We3C&O+}co&II@#U*arP'
    b'fBF-{dfLu`jVm7zEJ?Cw>RAp?Lw{4~K7g9pu=H>5sT0vblir6X@AK{AlhS*)G|T2A(eU*VfqwUw54XxWUx0Xwi3J1<^1_tK(7efP'
    b'{spJ0KMq;5x8AXwFz&=2GXQSF&!*4SGf=lt&^%Y~SV1ZliyurFrR5sXtOXNOV(H2M>(BAPBl;R(MZKH>+f48*Znz-#JC6N=+<iG&'
    b'i}?T@c~;4@K)A@^NSlN88OZ{R9x*tmbTBMZL`%3p_x<^FRXP+npdir$&_g_6MRc^mqmt8+Bx&^83%WPkK6rpHAy;$^JO(W*5>=$u'
    b'jPa%3@MEGDH{!I8vEjT8!u&EkZ*Sr{0jACf7YY?2kCG&_InOXzonKK%&wV_>t=!lGvdSB)FmM}>r2k(s2{<;Zq*dBYlm|9SD+^{O'
    b'Xan;ij%!<tH}euVc*pwfU(7}Vd}hKF&u8Z$=uPbr7&yLqPx#0vL&u#<Xah)<M12(tP$L~ahk$V%$nV58J+#bX)E^=BkysO0Ag>3o'
    b'3d3y8Y>qO~1cccP-SU4;5?3#Q3g&fgG8N+w7k>II_?0!OQe?^)1xgH#)<edbok(<$IZ5({{ZAP|kY=&-JO8nN0o@z^9H?~D<43LE'
    b'h;vam=Gn9Cn_tKsl*weeQAJV=Qcga9q{ZPGHUVqkH}%n*&A|BJ7wVaIBRt=D#=Bb2NkRTtRC|#xQx1HH;<}?&6yP1vKttYg35$T+'
    b'MsP{ie|QsaY;?N&yKg#O)mC4#lWa?6fyM=uUC`qKALsNq$H({Y>G^#YsJj6=Eb2o!;5ky`6#^`V3y=u&A}#5;EcQh!kdJX9=S@LU'
    b'JS%wt1O_JQ*E!HJ$gwXV(LQRccOU3S0FPyQVtxsL1IGR&7fNB85O~h$UGTxY06rbyIWs~&=E#9BfqKf;SQ3o>haChxt_8LfFdE8c'
    b'qvvCf7}Z#<2_t}jKO~!*(3%Yzn@~Nyy$rS&-!Vh%QJc(#%bA=)1M>q65wt|e6nXzXp8<q&gi%3F@^P%tZUg@EC&Qey{ciFhUIb8X'
    b'lW-N22!u>)9gIOrRo9-`*=+ICG??V@{FV$ciJTlRW<ux1{3dFEPYwa_9B(Uv`ZYyWr=49cM$UFNk8YXKMI0kK*Vu;FMU)yjMv4!S'
    b'soY7ogS#FD^>z~AX|w|$|4Z)(nAJNPWm%#~{zQI791Em8kX8^A%EEBstRVdx&`1E=KUISZ4^3!)j(Q<O%<Z2Zz2Hy?ef*ZJb5!K?'
    b'z~-|IUpqVv_v10kwmJsEx1kH5*&BoxIg4>8(+LZ2C?1;wOFCwZO(6(copV_*t+SdZu>?q}EZE2PyTqiR-cb)80}qPj{x~GZ2%flO'
    b'*DhLLboPymcWevI?mUqZV7?;=*$)LpKZ0TQgT=4Oj-vdWObc?d3ip4Pmv~0c&mrN9;cN_&1mza!NUnu0^qLODqn7|}QWOFS5rBS<'
    b'V6yaA>WrllRQBeJ5V<p#eU!~VtU5I%ZjCGwRq%*FX`e?Dq8`xLOY|xMMG(k46jTOuzV$(43RY@jP7Yzhp;h7IJ`;!$I%F9xiugJ}'
    b'11*>Rwx*60=bxH>{96B75pBpYRGvJ4lbhV&LUU1ecW?io^Wx=?hkt!_^!oVZ&Hr=SJ$w7p&wu;n?_PfZeL24fK7AfvPNuV8=iy>`'
    b'b^Yb$A7!^vt<@V_+jz=6OH6=1#EG=BPF5S%?Bj8*xp7XK<Et>8=fsD|QUYtGH;Dg`8574+I)*q<JiE-zdvS<@A)?c>B24aT9T#41'
    b'CLG+`gmw0wT&PHM<V(!Qf!QDW*xY0qZ-l4VSL|TRjCvMfWf>&=qAA*fs<&|gAn`hSC0Ne$)|wHU03=;fxgVuMlJz4Yg;W2&eiI07'
    b'N$9i|X<bEn5+W?l9zJB$0u8wqa%SMtq?VBN9W@4A6R9-WtXd@tF0b~C7K(fj!UHbJ&LoISVmg($=-~XF#6=JfB`zWI-NeNfegko_'
    b'u{()N*d&Q76uFbQNo^;NIfwV0PiQ-3Oo1_$7@?+G+hvV%Op1$elzEfT6G$zP>58kfE+&FGDRE+p+tBdZ>cU3A4Q*w*kh+8hJo>Z|'
    b'c@c5>bx?;w@Oxk*c`4jFlxz;1%R%p|<yV>#B~dyh`r+Vm*h7=ZRuN7ASCmJ~-ax%n><zFq7LSMUKe0Hp5HDc+TIYaAl5{v)QPX67'
    b'iH@gjFCE|rb%LQZd=aoxHcUlMD5w_>sP@5T0<4_ifJlYH0wdh})A}OO4H{;34;sbl@5&!mwdbL?@ZdY^&j$JIyr0ddsK%lh-=_qd'
    b'jci*7Ho&zWj04^_TvH^y9RP{ePDLowhhe7FBD?|Drj8WpM-Jeb3B;d&03%~%^et<1_syH5UpPQ07`B0;IO6TcL&VYHy&{J#<i|SV'
    b'-5<7H%__k##wJwKl0ml7Dq0x^;S0`Uf+N-#wtJ1L=v`KhW~}UWKi#$gqlUZ1?R@6|a%va}&$Y%+H>*c)bqX;NPhJTLk#tNmm&3mt'
    b'Il})~PM<k^jvr>7MMf06NR~W5N*8Fpp|nP08yfcJ=T~{K;VZa~=@;+Z4_a?T`5TfCf+lBnt($=zEiK*!YAMUHqQ0p$ZWR@CtDyC;'
    b';+g<dZLCnt5<)G_mhp}NdsY*pp%EjD*eqg1G}~*LXWFTNh>RAav^E-R+TecLjjZjh)jEqktNB9I=c@gqX8))ImgMaEWBhF7YNM<Q'
    b'8}sF)2O0{x*wiDn>B9U<iL@!GP0X-ocBVO#*=7}Iqt>*I8<UhH;HhhLA>(s<6PeRjPalVmkC7A{@YAMkKZ$`ue<D8gcK5m&lTZg<'
    b'>&J}FpabvZDHG+(ftS^c_-J+f41m-Da~Y+>jxw7RVwbT}6RGE!%}Pd9p8pA5DyRGH%|D|Lc6z;n_rcrK-s>*B&f%JStsL$jWy~ql'
    b'Kb0p}C{mROtb^Aim6CI1yqM3U_Oa#oZf91P5_2jWhY{_C-VG%xmkvi$>TW2yR5}a^k-8g%6fzJtqHQZ4cG|dtI@Z2&HW{X#wQ6Bl'
    b'+TC@uVrN(4k-w`J1z71iqZRb5{pjd~s?MNzz8rgVni?&o>j|X!!y%z6fMGW)Fh+@P+k4}3@HZ6`s$=2t02meyx;C)9nN8}sLPk$g'
    b'F^XIx!x*y{DcViOAPL&2_UBmvMSBP9;ov62T|hQ;dM*?fD>1i1H=MDEerg%&SAN56tWcnXkt?yi6)kr*a}Nv$OlN+m#gPkHdxPte'
    b'LJ^&r-FkdrM8g;W{&)nIgBM|BbaB0>gJ)?X*=Ww`<9DkOEOmDaM#ytBRKc1=6pgI;heMM$b0(ZICdTvDICX#AEpymMZ#qgAQ?|g@'
    b'9nfoOaV>a6YcS(}*{g@WXr%X)vWl6EV!9>ht*L0?gt*(Nn=&@yy}e(~I$hbf8_>R8tQ_s#S+vNYdJ~nwcdL^!OLoEB!*gMR?%=|k'
    b'oYUDf^p;~sv_OrA|IjHwR6}L4XzSfPItvYdqyF&e=*%jJ0}3P36?rXmmarWD;yk`|9uLnR|JZu`y7jpG_q5vF**FTU!WvxSgBGKX'
    b'MH-@PX2a+g7<)m}_6K|flADb}*86yJGgMrQ@+teI8Up~3*$~yvteWPef;C}jigEjNR0Mv}Uu-@FCg{Pmftz2Y3nE8U(YdwE$QZ0M'
    b'n*=)^+hhTM9!ZOmb)GMy`7DA&Os0#PgL#_M^yINyUM(C^K44!A`>S>8JUVxXTj}N4#_}e4RrT(&U2`RJB^VlnYzIF#U`YfyZ3yM>'
    b'mI;wmh~z+KlWX5C`=n3UZ4d@hLt6$vP+w#G#x_8lfN5=VACt_uI=Y_WN5wP+RTKZ>?xyi|nMj^z&kO_W=m0F7NsGQntn?sVIp-<*'
    b'vF(65YK?g+7Xq@AX%uuWOO0WN!D8H-59rTj2yexfNYDTm5c>#fM(5H)=}i#Yo2UEo<1%b-vX*Uiic3Ma0QQ==2a}#JO3a5d%u1d2'
    b'I9y4~XCfnY1N?LuW|ERQYKx*a(t4Goay$#9T0N;i(W*m1R!{(f3qzX3j}$u{?%<hTS&fs;5=X2Mg7Op!^zwI6BEA3j^xiOqWC<)s'
    b'IReW%iW{D;C{>SzZ!mnnkZ|+&3q<z)!ov0aB6h+UzJdHeOl=8hom$TP&k;e<WQc?Skqzt8G@w@5VFxt9170M$Fw_$!1m+WFK~T=C'
    b'tF{hU-ihc6vcaS_C;6aucBG11sbM8Mw0Xyj0@Ra7uC^oX^B>XSvo^5CZv{r8!+}RS-?-!xmp0_B-w&BwxE9bS2$BQ6bqaWdC5PZ*'
    b'gz`gg5ECPk<$xV{MvkmVlDtuhkZ&@ZSNNaPef%#Xhksd!;S=)PIsu}2A*q`zQvR3TUer#c&<VrkP3!9U9rGozmPBd}DV#lk>Kb`L'
    b'zfkpwzTKhJ$7-$BptY2bseeD9-eR>v%XU&-rb4ksGU=;BGE>Z5sZwFE#lyNHCY{wHBsSj*=dGx)u?{4$PokbwLsM?!kd@jP1F&F6'
    b'Yl;{Kz^Qab!(<0Zt`MtfbH1Mv@t)t;@0ETgP|;Z+B3r}QwuT#L162CqzwCXhl*{UgGIN^LWpu;kD)3r<<!$Z~QIe_~B@a%lWWtRp'
    b'>sqEf4kJ-40XZh8fRy4SxFA3tC-_8+XszeN0|Uh;4K!n84MZG>m>?&Kn?9<X%J;tq@85$pUmx*@IIpdHVG!DBl*h{)JPS#cO{DNm'
    b'Pu?rH!PwWN#BWd1$qVv$4FTWU^BZnNaaHaUUqO>Nz-E$69Jqyps&mjRn88s8mBN85hv)dD9j3d*6Ns%!Gyjm(qnLzS4o9c9tM*)H'
    b'uU6P=ID1WmXPVxt7xvaPT`xQJYD(+rX-yx5K_lMwmXm0^q1$dWovm{IA*oXDZ5Qbc^sN;R;;kQ43kUVW!4?k1scU0VGg!Dzqq3I%'
    b'iFB;@BC=a4?7{!n3j3706_Dz<g%_^H2fHo|Mq#g7*aw{5LZ?!AQ7OEH5|j<NtuP%hA?8-gj$3u}4^07kH&X(M93T#|V2nUpg@f$^'
    b'GAgAGZmTUrm#WjK%M~x2je`z{x0IE))1!2xcGAxKQg+f!QFkWB#LPlb<`cYO#m>v{z!aTUf=;|{jr_aU+m3eeF1Fn$Cv%bS5-??;'
    b'x)7GUCV0dvmT1{dVoO<;9+c?Qr1{jD6eZCoj+%95IZt`1Ob(o2!s$4b+u*~*i&$RJds1{3tX!b6M4+6~6|C!@dQar4Ek2nh`D3h`'
    b'?Ko)(5A@2ZXr%2*u1!3bqWA!GzPRz`@VNKaZhO00b{oT5y<BVd%jKrm7&NyV+rvS%Ss9HQet+N(`qlc@py~BTeyvg+)wUY7dUI6S'
    b's?<icN@D|Y1vu_jedss(Ud3<v&2p{mmTRutcbfyRU)l1@-l*w$!|Jd`?P9Wyb_Hr|SDH1iS%W(Lt=hozwkqXXwNc*ko1>9i@u~o%'
    b'HmD36mFBir-5T`aX*lfHtAOc<S|&&^?7qLfRjc~-ir?QJ_3NX4zgFG?=+)Yw-*B6r>oprbwSCro`|9oK$zi*^U2E3ezF#l*2hcaa'
    b'?pH^Z%FwS4DqH2@_7+U>dcEv>?!e!!G-_VGzU2Y9`gXZF*xDY{seJ>@Z2(qVK%%W$!`t32Z}rO+e^B$bhFku?8<eY!?OMI&H3)~-'
    b'y9Xz2_%QUmeyu-p%iE1geOPg;)n>K71s$mjw+2W;DB#t$w+7o~chnzj_xqmP@ZoFOcdOJsLGr=$t~dIXvNx>sE70qv=hsGFqf#B#'
    b'D_*nNuhj+sbU<zI|Jd1obp#r6dkeY@qup=%?hpnDS{l}d<xzRqbVu9GtxC1wZ+qK)sM~ZagMl|})`r`S8ZgGNzSZdS07T%vYZUg6'
    b'b`M{7+kVrlxPYDuqwNC7nmcr%rE+zv4{T6zf!eMQ)NWRWqiTQD+^SZZ^-;45mCB=r+h-IQ)^~B>>B-yUgO{MnwV|tJzp}OEjkc@a'
    b'*7gV(tkS6awOVBWgA6^#xv*9Ds*S$8?fJkkP2i78#oMmdhE=~wC`90@joQc^)|>U3Ti^Ca+uOBTf8YW4jQmj@m;#1*R2g`6!h-YF'
    b'bcu%Th6jX#8L(Z(7-6ph$hg}zzvef97&UJjM!8?{t99S44+g-qRbaSEbI=@BxBN<dn};I?vFr_io9dOJ+bq{%oa<G;-}iw+^=jV*'
    b'NTWu*wmtM2m;J-D4p*y{>s!@YZM#}6kLs0Ce+$F|P-4(8_nYnz*rMMcf>r7;P3mQ@jLp}*;b3dvmIpF1BXDk|Tpu(V6&FTkFz5qk'
    b'j0V2vZ#RZbf2+UM^tPJKa=+?rP&!1ECD{YF#hwLF9$MNZ1B#n@TQg5}^VBd;TjpuoJT=XeTQ(rG(k4lf?4D_LuVS7|n|r3sy?TVx'
    b'o@sT@w7O?n-7~H3rL<~f$M>|XpX_!cY__fEruCfCI!TT=rS((QqPb1!=&eob=&jZIfz|q{yV7_hHL|<W*TQbpd+TkCCed4i*}heF'
    b'Kk9|`HtJi)^tWSi)(i9Yh4uDj3f?Sg){*U@?0GNAkV(0?ZaI=LNHGDmTeaw=`&EtTQf`#3AN6L8(l&h~`n@_lK8SvHR!I<(Fxgi<'
    b'svwPYd-3Y8dY!)=o<(1O>YN@N?w{EOx@V{OMvA-w3ZHa42hs1-lb^d0fP=ShdPj%Hod`m=*Ev2r{iU}L^f|L%;~D?nX=nFfbr6kc'
    b'0`%V=pLV(@NAS7V?fewAiz3nP+N<6R^qut14v!8x(aYC|-R|M>OUyH1745u!bM}krt-=1}<h0j0cp1Z9`fvA#D!+WYdwO8Me%sxR'
    b'*F+2t(Vu(J=~{h!an$LY0ohJ4;Ta_a!xQ^`N)*zIO!Xbh!0(~)(qlza?mMOg1v;nu#s;aXz43JVnbTkZ)Mu=|9v-xQDin)Fj=)pS'
    b'bDh<OvJPjRET?xxO*R-(uADwzsTnz(yZ{e$p(g<!QL*0q>Xu4{lDak92im*z6^lH6+<I~=TdtLaCo-9&f+{?E(z?~VebxzGYmYCH'
    b'+ybyh9}0Jxqjv2+LszAb)L+!FFEL>Xrf0-7z?csBhEvx|xma)2gtl<MqsP>Nl@8PK<=jMj?bme%k1|KSA(v93H_(U4^0LqO#7QT<'
    b'3*!VPcOYT$9GR{flVLD_&UvdTz*nw=wyvh2?Ha0LFdMcvT}fE?JhM40#gkf*6`0{vc4yfQeK767Ro_(N;-nUc#tn+_{~Sz)EtLgq'
    b'vIU(byQSQ1bz9h=;{a<4Y+-?@jY>)z)vaxALvDEk1joU^&y@?RkuP3)Gj3q@Yn{JF(5q?Cs}+WB&O79O@QZ_sU_6}rlOku>@Wb3B'
    b'kAafZQdDw%!Kl$%TBCK>0VPy7jO>vcOwqcg<okGM%1sDh-qZa{{(PRxzCFf8AH-BaO$zGc=GV!s3egt!<W>htbViBZ<#Y*H_;b$m'
    b'PMIO*(|-Wxzd|p^t2#=ykNF*hfBSyI-Li15r{G+v*KI;Ey84>mHs&@Ai(`LszPP}sxgDES$+C<2(%-R~You{jr558XbbMs-@Ztaj'
    b'QHwwnD7*CwkgfBUDo-2ba+2E~P^ngnbKq9maFrX3OOBH2|4CgI4G@gLZrd*yfz*=iHXc`x+S*QQtJ%<G7KvNg(IaGDx%euA(@Yz#'
    b'W{j_u`ZM5EM7j_fG!fxl;zbMC=g9X)Ieeeb+k^OE2+<27f8IjWEvJoiO&E*W<i+X9-#f>67!jDYrK$z>s?t)GI{dA+R1^Nx_)i@^'
    b'f)r&O@2p!}TNfmpEeKPx`K^(LdngT8ZhmW3YOba_C!^`^?;d0N6V68?X)!PXj#*BH#A(GPnj}^{!l06hL9JSkkGnZ3NUP%cbb&ie'
    b'xa&VcrnDACz3Oy-+<nu*O*j7cIK;HoA^wH`f8NF|Fx~^3(N0UBwowSKh8bs@R0J0Py$D29s-}-qrJ0cWI?m$Sn=E=bXER9l*l*g+'
    b'<wv7B#TSGJ0BNTHiLkAuV_U`xj%pFcnwXe0ia~}qml!%60p+D5(j`F6eX+aWQD6hS(qzq<MFMwAEt=vK&S(h7Xg9n<J%yjNvVzB|'
    b'Frlw5r{hxi_b6ChSN7`Z-E(VB#obzATir{-hI)xH8bs0`l=B6n(fZ+Pk5zid4?xL3ec3sPcN`&7_Gu3P@bRLZh!hEsI5imvQ^SBv'
    b'P-G`T3v-lT?O3wh{M(61^SwqYk*Zs6oIpUG3kn><BO|#SN)JkIcS{*e@)TP^^!cU+7~CCFTAJ6pFAw+Sl8?+P4=2ECkPn9ybz>`C'
    b'JeBKCt=w1@QSr(D_82I8_~MX<3r8%$p`6YJv|;@56->X=)86j8&Dn?B#GoDbB3L|X7VN~ht;((cLs(T}SVc75PNnI#NPIl}g;s$^'
    b'I$p9B$xY6)xFcy6choI+{I}J2v3`VNGZjU*>8{G#%;sPm^27!U8^gNp60BBfB=aIwev*QbLZL=N8OkKqS{$$A-pMQeySvxz;FaL`'
    b'+<kTUCb6KUSGFsy0$@esQFKKw=p*LVwY68i{zd7{5tYLPuX^L<zyAGy(MC$Xz(Dn8A>9zmo1;6NZJh3Mva<c^tKVpMu8t{tujtM&'
    b'-peFtvb9(@TZ=9wq?Rm-J+4xm-N@Ot?hY)nC8Rv=U19*EGsi$5!OSF3#e{X7&5%aod-fQMD>~W=t=21Pt7L7}wyN>96vIO<16tvy'
    b'pVbNr+C|#2B5`djrK!rcVSEk6jughVEdJ6>Hvh0{l@ye!YkFU;Ikmc(5O|Toe2)DpqwR=!wB?38Y?`=+b2-y3RCJ@DxA1l-#~<Bq'
    b'PM;+xxQ|(($3ql$kCewbQjqyP#Tn<Ocu<^fC85kDl!O@S{JNaVwL5rQ`)A5ScXamSFGU0-1VAiJW;uJsm+y!M43Elwnu4b6jR%Xd'
    b'^Es;$%E7?HsQbU3ygfbMJ=#Az0*IfL)5nVzK7~`fOldN8X5P6!*EIzE{_dL|1~lps`1Xxn=O&!Km<yb|J;R{J6eRKA!Rb%EpW1sz'
    b'C;P8D2l3a(C+MDrE>8S06O?FM!YmVf(oN-}ehJRF(@!ZPq@FmS^4SPBn+^Im>SQ{%MVuf9uRGnBng4NJ9)bWmkNU~t>j53)zo{x{'
    b'EqzkdwUdeel``F5x<@B3dl>h3hRgD4rj=o2Gv6|pG4;6n=H&D&dRu~(^YhcEJHXXn7J5n5&>m7Dt|q78*l=T}9i>}G<$)gL0EX4-'
    b'%J)h>pHMT?1eRM)2&~*3vvi{aHLoo<{mR8xN%M`pmKD$lDeFr7wVNS-Yh1R)TNwW#EyNYkl#aR$>1cQN^_!zk@3_7BRqreI^t+a`'
    b'EhBk%spf4$OG|068Mn-z<PGA9!cne2Z+^bSwKGNcGAXyU8iyg{*69Di;9UeC*YeW3*s!cP5XsXq+2(Ivz3lyj4=}0tf#d={{Ppx0'
    b'9wNk}N~Wx-ovf5l`_h)W?JcL)G>d&C_hKtLE$Dhl1=Bn<F}QJYHo0nN#fh1l4FVNRuHbPB8cig#v~03PY^o51cKEcwoBhL7NVH6X'
    b'&@*R?Cs)BR@S@YN90tl~aX=vsLpn&}-~yga+Tb=q*bUxF!d~>;^3ZRW5${zcwbr7$fOQ&eD~OSlQ;D8o-BbtVfNn}bHc8#IX6vRY'
    b'%4oyNv1l%2W?hs3T{nzEY9Ye$Y&K?zShh&z6m))%+8LujOyztOyMX4(rO`QS03E?1yb1;q>t4`-@dQa<_ftxvF9!{_^gTGgJLZW('
    b'{+1yIF3wtNH@ZS&`WZy)zy4G0fqnbx_~hqfhx9UM|ERNjj34${1mK+m@aw>AEjTkyMNiWW;M@N?h&N_o039$u#R_V^AO^+!x1dU5'
    b'*3^yo=91vI+ae|q=!``i*}2bouyg#;d9F@g<$020Y(|eP>0eq>H;1PKV1^VVrIH`+Fqd%yIA3^@#OmUqg9lWMZ(T_b_F9^h>U`<V'
    b'!7`su={`DRh%sh#gA$=F@(4|S6iAkeFM#B&Z5piBNm>B3;T7Q&e&$>8&})cSci=TU(`&i<M=m45d4TSp=}4jB8cB03d2utFJ6s$7'
    b'Q)Dt=F_p1k>Sl7}p6tob9*lj6m-ynuNKny||7)8e?0#=E@m)Eg%zi8K4bts%$nBvL?En@ef(Xj7oNFLlldsE(-LnYxNYVt`H~W&('
    b'8p5KA!n=~(?@4a<BzDRK^g&B~8O|<NdCRRhgXv_XPekjbMRu@|xRi9gFZ-oX0&iiuoK6C|-5o;}CL<q|ax5AQ@j@7^gSQXkL&z5y'
    b'c!9$@g11~uIiZd}xe5s<QA7W`+sY@l?IOa+W~_5Q_kcp2D~xle11o^IKpis&TKC-3cNnut!<Wus&fVCw{QBs8x?oR_LkA|mK4PyY'
    b'ze}5yb`?@+)2qby0;L0;meQ0f(nz8x#U<7fr{4G)udT|^eLsGfiQx<7Q6gk&qk3h#Uh}F0x0Z$`?Nw0WReYK;e2iwH`nXu*MF6YF'
    b'U?GmKmQ!KCe=)r1uohvq$tSqhA|)kP&^oo&i5D#xugmc`=sU}acLmdo)u#ESU_v4TXPC&)xG=l+#-H&DB>F>i4$h6(&gk?;(t@&E'
    b'uoN#&!f<x-`Y0j8QlYa9`wgItVrGs6)msWrbLewEu}j2QInzPKtexqIWxV1ep_tJjja0=9&mN>`Www{_t^)}7JNyXJgSD?jClmS?'
    b'A#3h!Bdn2{bmqk<T5HHfcde3MhO`om>vsov1Ci?GhQdqOE44;*OYL#+f!eCq;Rzky(K(Q+avQC>+bVA<r(7+UcVL>(2;-FudN7GF'
    b'`IsuFa(Kof8%6;i`l_yiN_MkVaT=Hp8&$Pk6)gNqMM7}Em!X0A=D2Pn&l=nw^0C8EnWnSpI2hbOIky4`Z&mUHXdn2|LlOVU*KjK3'
    b'x>Koc37`W-^%ZT+V(qP3LA5H?rUO)A7#*53yagv9>J6u|)f5n*I%*A&1$8M>Npt99bt=s*2K5qjt3x7l2%ol^PSY*mnK0LZvB>l3'
    b'5(Gr2@De9Y_Bt<4PCL=b)E)H-bIQ@VJ-L~ypt{j39Xg2D&1wm?OMwAG3U+V~##213r*DPHK6<3Gc+K8S^<k!6;#ri5+@Z3#o;sK&'
    b'Uf;o{48G8A?gEyld?dwW3wXj?zy$V*gbVaR0)CDpQcB5KK@0uL3i_CxGQwUEL#D$ZB3#n(64eOLSGJR5wc&jzhHHa2b}nwt1ApR2'
    b'Y^sq0kg>hE-wdT}^^7(Hf+1z$r<<6jFe)f)7E|?ac(Krjr|-&6^TX3kOo};P1kTuB0AJwk%gP&InoZCP?j8}|sro^V!MFb@fHm9?'
    b'sXGfP6`rotcog4h=-)UO>>rpo;mpH?hcvq?WmIp<cr^h9|FM#~27ha$a=8hGR#eKI?aYdF)1S<jNAVp77>659YlNC;s6GO|&L@vF'
    b'JmT_?c*8W5LcuRvbGR4~Tirp=I2h3Rz9j+2Uf^xTg!A3?u-K!xH<%|gr*>mH(Vf?Pk%}aA<82Y)3o1z=DLjAGo0Fr%{a@D6mbe#W'
    b'8`P2^roqj<fB%i2@=tJ}6SH--0u_pI-$#Cad;EI$Z2!m3fpd7)c`Xx`4LYB$KLov-rZVw`<K98<T#geN^GL(|k#;iiHbk{Ig&p_K'
    b'(iXnRw+C<E0I7D*I*jk)Vh*|kX$M|_w|%*YCSGKHJ=F^u-Ijre_|UtSLSjMXxk?}sZz_iNb99B@QT9>XFF{ia^Fl0udoWpfXq(9c'
    b'pY6NcbU5TSm9(3?SX%>(?Y6V`ItTwYUG-GGIKr6sgU+#XsAr|<O+KG7d-ivO+H}(@K8iancy)#eI=u`g9!`=9j)IG~qoPb{ix!7{'
    b'OB(<KzFnd1L|qFBlfz133<t(Ls^mVXQiOBIr8yfc9F*dh80S0({WDrj<x+P{KaP1Ra=YL5_@aBB9ruYso`2scX6qX*I8Wf$eDE#v'
    b'L=y0PU0Iv1DSZxwcHxGsE@mN3gq~jOJC6t6Y(d9XG5<5>C*$<RDo3eF#iYMyvEfu-19VZ~nFWfAiZaWdp8VXCe3*7_*{`R3g6Q35'
    b'fOaS){G$882AEXV^y?3RZGnyG@WQ1PgPzIPqFo_nQZV*TPhJ7XhYPSqv>Rs4FlpzA-sp?P-<=#E{gMm}Gx?|V0V+HoBR)dQc9S^E'
    b'KL)JTaby68O=#&Q<$9v(p`=ZTD^l?hU(=4j%5iRP0rOa^YeC3&EbCjrrq=~Bi0L{&tuN^aChi?)X!D0+&wfv{<v*g;h-5F3SCU&*'
    b')E4Ou)R=62k<N4HWU;oxVph?EHp5aj*nU5}GQwLm>>FU%OD+V(7rB7BYM<4={1jqb5FgoP<6fTyPB-q$YmNKL{l<MVbHH6`1OBM3'
    b'mc$k4X_kH^&C-7W*(^%&Ew*%f_Q>;V{r&)78p@)n*ri)&pQ+jwXw+ag1d}|TxzK6H>AuZ5bVlF46sq(2bU70nDcs?t1AOC^zJJ<K'
    b'0?%b^_bNR`Z+25m?1sd)JX(shD&FeQ+4}fMWy~^GIb39Rh4DXf30)b#h3(C+bdo77;xEx6OhMfBNGlcB7_{xJ^Hjwp`G&ZANRVpe'
    b'=sW<SfoBHFs-;|+O<LmaB=#+MF2i`X)U`LCn7h%$*~mc+Ii!O_S2^H{GM`>fi7E67DuIz$wuR?t(CLh_0+y!S-gHX0+;U~o2Temz'
    b'MiiCQx^}t5rh@j5wiE`q^mbqG9lm^f^0sT~x)r`M1jbT!rYVX6&lBPM=n#zyC@~Ui3RJK_eBS}x{laIW`r}>Cv~A*1b|6d}4>bRE'
    b'82~zR1G_&N&Zf8yF*-m9^0K`1Q1|>$1o~X&_?$~N8-4Ake9g<Ct^v`$6GU5si0^k8a|R^Ic-T^Z?Vf;&0Mq8uLwi2F#*3$hj5@z='
    b'aRSfX{j-AchFR|zMO`#&iwWndoK3Hj*lO@*yj2gihI$&v2{iiHz~Pm656mPou@9{Y0`b@Nd}22sVwmMbi;tEHZ!Y`OvFOWHHkZhy'
    b'Va9G@7^JPL)_~aWD={iJX`z+gpsq~!gHNx>DK_vy7vpP6P<eqlh9Nh2yA(zzjHeSck9m3+6o{n$P&fD#ZEWagu!!DZdz{ZozoXMp'
    b'=8)Y(pqLto6Gj6M27;17<5D-*ECMnd&q7i{OdfQwX$m5mwc9=P@p@tr9CTyl1y~isV2=0QW#7!FpD1ZRJTFI6XA}+{Z#=v3viSn)'
    b'gLhV#&V%z{Lcz3Y^|{}_2g1D=tTY+v9}UjklcIe@nS5jsl|&t^d*~z}81_;1o1%Y&*LW)pse+vBhZqP3hjl^+FNv4jrJ>5zBPFE('
    b'h47c<r6qtDF!ebzF-X|q4JU4rltF0;g9-_SrU+d(8Rw--Zo}%E-A!AsDd_D0zuD|>Z~3@`!hMXcg7+KEer<bO(h^4g<9tzdF$-vm'
    b'(-C1P0G6IyDJM`NFlm4KC8_yXXe9L>eLu9u9$i4F_`EsoIH#SLcsvx73&%AhJX?CtkWy~BEA`O)D;UZ_YLgJ=_ojhCcy8Twc}+mI'
    b'i_$sggkA-8`m&3@-ibfXw`hJ+YSrT63&tDMjda9lsKyr6Poi*4L4bo=+h%1YgzhgnxEZ%)*q5(A%H={|%LTVmga0+)e_OY}ZF~=s'
    b'K2b{>n?oOX>=JKtTLc4@yZk()s}oSBgox=rCo0Pqp_w<<P6KK#qu>h+KVHYHcN*~QyJYkR+hK?HR4LpGMvwR891?-51V7QD;hzY+'
    b'OZ(PgYc<m!$Zyo2!_c|(U}gOxxzwt7SJzZFX$mqeYk3f>*WQ&+fl3}mYkTJut-qls4So%y8FTHHU_5}czU~(G3j2l5Evx@Ubuz=f'
    b'bG(&vOz~(f)h*X6D%V}iZ*VWvTxiQ23hM<>3CRRZd$@ll8!W`pwD+k;a<l|8kaEi!47s(>{VxiSbvWCN?H$kw$0%F|_%|e_U4;4-'
    b's3mmeOO9zlgeZau#(h9V+1|I&+A1ovum&zcN|k8$#(W_iB*bg$ecnaHZEsp-aD8btwzl#}XK`0hkF<Z4NC=8G{k<g+@M}6ljSik~'
    b'*)~SioBUt0$ccuYteswV73dlQ&lj$0xiy${xQj4fRPa}&VbPjM?6YmZ10}Xm$^r*#+Pk%F7pK)t$VvGgK;h~Ng;C4;41_bb4rU%^'
    b'U7}=kY@5FIt-4d+YOJF%NsuB;hl|`tO8e4#NjXP1ze)?Yd@#GM8zwSh`sJ_kbo)^UXg*aR1r_+p54T3~hgbUXHvds8S$}l%X|1i`'
    b'M9rs<@@TLN1LeZXG{egzbEh4QK=0zYC7pf+q}-<$11MG5u5u}zN8w%h10VK|4Qy2p>|Q>;vqpXynkz$XvR;D0?2v7k(lE_a<zJ#D'
    b'^m-Tbia{AX6wrHlc!o2nwst0o#fUBLQ-e9=civkEB`2k^Y$0ZAuB*9%2h>|Pf2ueIsuc(Rv&~r<+3^f2@|30z$~u}|L{)JiJ(UQ?'
    b'I896RXIqoDgA2)PE^ttd=-i2!#W72ha`qhbr0bUHfS4H#`Wd^*o}q8QRj=095g0AaWJRNxr+jot2Tv!|wk8FvqL@fY?ZrD^<IaQh'
    b'enh;*{VoV8_JKb!7ZdQ(XWVunopOSm0KmkZwDZWRr9*3P4C{Q8$gdG6dtl-KOC0lsEdaPuqn!>YT%b{#dD=C_D<!3?ga!Y~8>@Gy'
    b'7eEI-U<gBFEpu`rf|a(~)LJZAL28*sIX0PfgaOeqMz&VuU?pXGF(qw6?^gnmB7}uJXs>|;$BhRgadW1p1@-2wo3}|=Z+-^}>&*gD'
    b'4i<T|2SE|R&9U#MrS9+_L(O_~JvG@|X^Sn<8EC#D;<+<)a_8y#a=J!Qa*oPENJjzYnDQyU^f5!%)gw1;5v*7q4Tq!sTXfXd;rv|+'
    b'G)!Ct7kteLXm@mklkBGqe`~1>3P|@3y4kCb4LpZ_JrF>*d03PfnkX0#sG(brYObR#Fq-4&MNYFEb-^?Duj{a5y!b0F4h#IZp&nJz'
    b'R+~!9TY<`FfXb#c=TL;zZ&+~Zl{@IUZsEvEtJ&YS?%37uS$yJ>0O-#SD+zV<Cv=741Z|u?apjPV9k5|8=E3B%PPk9y#M40+>44;j'
    b'i({074jNVBs@^e@I1&w*-3<o8!lDnV&k&R!7>BddP6ugl_Dei8`2|$Md~aB}OJQL3_4HOM8^J;9ygh#Nw)-QcKN3Rs-jZwX6~5E^'
    b'GWQi*M^8GO+5x+K=#PCgAKtz=>2*){cQo^clnRa<VDhPz$;2rK>{>S~cs{;eop7!R2!!cSf(6x|qiqu<k)y3LZ!(<(bd8bmXX&^D'
    b'6r0t%$cL-+;%4SkUb3t1e8ApSzVnzou>3mVzSW#6h~&6Xe#bhn_eX$*&iD3rfgkV!w=QU!d3!5tn_N-bt^0jD7~!IwFwN?)Qt`Ze'
    b'(xJiu-s|>~5<Zpf-|kb1w-dQl9-2xv=~nr@No^6{c5_PtCgBGOMz>tvs@JuXrDdE_7ycZkb1+aJCs-`A$v5C;tYZrwcZ}As*13{&'
    b'dtCd*?;*~yxXYuc_9K@^>pq`{=)~R^l=ot%IHU!Vv)VhyTgYW^su0^3D=6OOA*(XlC&Ik(wg!O4O2`M)N%)ocY!mt;g2hcyb<BR='
    b'bTC-XZIyq3lQXuhiCM<iIXKP^JEy(Q@!Qwg(5#QFe(>D)g{k$H0(BD6!tND~aN!)HsHKsH7lB0pe6IxPg;<8(8gV8uZ(&q{<%TyL'
    b'=CWj0q5zGMgdgH&k{qVROI)+&)9WHr_hW!YY%si4i@=|go8r2NkGIA+j>9%M{a)DXL^?@O;R?31F@R}K(OV?Pu|Sjt2-Zc+>v=i7'
    b'LUMc27oz-d>a!0}=&XmQ?_YRV!E_#tNLP;tu6>|}P~1fC1QVLR?L=pEtgz}GYsHQ6GNOZ<<?LTE>tX_?EPiYFESSLh5)4aP=>oNb'
    b'?$gt&ny9>_xYG$6nmz**0gal?XPAvveba^Lu6ZijsF}E{Mm?r0HEQt<-bQ`>VCns{I942yIf>7LD3k==!rEwDNB)<EJq(gU7O#6B'
    b'FU)Q|*5JlsyXGL(#~8#X2f~>TIhe`Z#ROU}ZUw&r9Ks^)vSbU{{H<)}rPg`3rp|{oqb1we;_F$NtZzXd2jix<+x_MB>(1HfFRW7Y'
    b'u{3+II5RE=ax=hapN=ITkeKA4cJ-i;uy^pJ8m#70q8OsJgwb@g++*deY+~M1lqdX}{?Y{w%$bf5&~%!tFilmh!c%_B1$$GRiXKC|'
    b'>teNhGiF94RB%<Gu41#-^C?o;lKseB>y-U$0+Cdq6{YAk+u$jXFt2itQ#(BX${N2O=koNfKdaaRC1<ikfBb8ggOug?8}~cB!0lW)'
    b'A#c$QlSN}>2QF|VGW5Z?Id8KKr^`Mp#ge#H8|N73N)aOJY1;&JBwkn6Py68#_j6H+GMtF}B+^Jh^_RrE=G>&ULI!i5xtxC2p7=V^'
    b'wXw6UW)2TR^7ByDF}z7z_6`qvCLVa*>ICTeUoho{wLGm^>AnYCB>`@&?}9VE{0!5d_kr-9SKp&hX=7L?sYf#kXOGD!K!mnwXC(y3'
    b'C5*;gR#N04OifG8IdTd_r#!aVVHLMk-bgJ|xqC6EBZ&GUSP>EwM?>prFozyY=Qj>rra8b<k$R;7?w$E_hoao*E7)Lmr%k$ZK3WK3'
    b'V?-H{pbp}Bqs-PCS4SLJUrWlTwc;Z_=|74APS8M|@yBmG+`P$&Pyf$FT7dujXO-2#gv?FWR>Om2)bDI4ksKAn^6*N_hZs_o-?2Gu'
    b'H4<4-54{Q_X+{0s8#xdjSZaTy8KrWj6o(6<I$BVTid^dEndr#;|168ktn8Hiyue42dBUK0rETRAr6xI_dzY8qybxPpucvdA@o01D'
    b'UJ=>A;EJ-wnOzNSv028NrJ{0-7EDhkIv4FD!he{B#*rrH%aC`lC~`=zKcuEd*B`JNW~f6`2#twBE-&u6ZU@s!oc&_2xbf=~=q!%`'
    b'IP@>4CUGBY+pvC<&L&-mkA*f4Kr!4qIU)(r5;d)$PEOzaxQnjE7tuTT(L4G180<R=P=pVd-vT~FNVK%_X1r^EFmx__2l-<|jP%!v'
    b'@X0HZ9G;@n@2KU;Y{!zQBhpP#hg}YP<)W<c!Q#Jzf*VDO_VeGUbIfp~%q<Rl231^b_K@kDEl{)O`&NO;(Zx-mNOh6vz{%`%E3pHD'
    b'xf0hc1w|AGIRY`K(-Mg<=iV%zmvq`H%ipp)vBQJE6&PTa-MLFECpb=ca|wb9rXkaRwxpwR|NQ4aWu9vZqXvP9b@oy4FcF_(upQs$'
    b'ixm0z@uN*p>tYZz)M($*cNW2TC^}kT2N`<ODkCRR6(7G=3%B3?iT}-)ggEA9jbGk1!xtBhaj%9BYu@qME?c+QGdZP$j0u)GGF}D*'
    b'`+OkRFaWk<c4X{c+BcmfcFF}{h+!1cwso{jfJJ%mQU3FqO~zH{_yjaI45-dZQOv)djdDn7Zn?Xzm>Vlq*OQGh^*JFBjt*hP$fadF'
    b'syjO@8j;E(>tU`@AP<8maCo&df?=n7=w}o;6mvY-7s60fY_xgF2Tln(@fxZ-{?OswcnWNh5K~9<XDDds8OeKxCP-aL&^tlsGB}F)'
    b'#_(B*hu62T%IhCE5FN;f*&T?8*z;(fCYxAa;V$i$Tvlk-;8i$A{~b`QQ>)o*;=16eN|}Rq5P!UloJWRBvAOirwN+nztq#!DT7ubI'
    b'rjNoJd&z8$`xD|$Y$TFw+|9m+d^Yz-MNZT5Tuta07`(t*@Y9lC>#JY}>v%PMwR6{gqtU6T%fL$^^PWB&0Q!WipwTG-n6FW2wN00#'
    b'1BG<HnD2y)RT>n1Ne{|F4F0^H;)d}h$i+C5@vs{f<5gXsMWBGK$d@8z2wgmikYJ|Y4$8g5s5A*(aURir7gU^5#@B!N^J#Sdu$fFm'
    b'Q?||I6Q{fK#>g~$iVvk71#aX9Q^)@T3p(E8%mwo?+cUbnDRr6~r)_+i6QKWt)A_sMJeY@B7UHmI<7_nc&JE3z{@S(7OxIsM(06Mc'
    b'fi(VG`(6ERDFv$#sbrCX?tjtYvz`i<ecmY4ks-t298?qPk^NQFd0`-vp3Kte?C#l@c~QIyDUGZO%28i5fv#zW!s5#D!cpUh8z((R'
    b'-G*a3?9;%v(diqm!g7k77Z?Fwggz$k23oCSt_QMfuz`)IOEH`7ntPalndI~O+ezf!_C(S2B-x2Vt0@iBfu$wiiHf8j*;|2>7T+HG'
    b'nzmV+24%$&@!><_k}RA;cqpFsl%HXI_H(?p3zPi71B`+L`Y}9Vb^L>N{BykTmybs}`o1!{of;2ZpoT}lV8rM`;OBfhFaQGs(E)(;'
    b'@&kP3qYTbsI)<;KaWD(%`2$t|8P^L2P$B>&0`Qzxk8_ZXau<A_<EbPs5lo`vlQY@Hz${mst6le~l{`>Mx@hulW4>7po5rJxAOWWR'
    b'Pn5HAfvXjrlUTX>SZ+PW*sW=T8YOPL_zW1tX9|=0kAYQuLV{yM=%@x8!fabuXbq;b8xa5`F)?msj_y2Ihp-(ATmkKn;jugGa(bmN'
    b'$)1h9o1)q^b+KrySg_cU!?m=ST?V|(fzU|*2T}noXnoJIQwPJ@o_@)rXrvrVh9V!WZ9uxGPIjj}f<_5(guV`DG9q8AKORx!SQtNh'
    b'i{J64k)rxp&i@NX`HMl(AQuh&lEc$9duZv3XybL}l(h~mBM^!nSXyS6V_tJA1g?*W=Js}v4|<}?mlXYaadh~mD+g=H$2sTQ$SMDO'
    b'88gX{1Epn+s=0C-w+1MWJLOu4_mHL!;PwIoQTa3sN`0Abatb)vQ!xLg%kvBN*^=dmiBU0q492BXVkcN7V5(hB+26!-WFkXgWu%h@'
    b'#-JJnm{W>4>kx7rW6~Lei9rk<Z4}Tf6ovtt^P%AQOyJwc$J6toIyD&$DBT+#ZXs~E{DXD|CbV9G*iPn-ke^X?J7;g-;4w8~V3x`h'
    b'(89SKagMb&T_IO{vw}0ey;&t^YJ0QB2V>fsb?!`iv!Mpp!}jKufq-1r-u$}l+@f;=o|^E4Qyd;)mfWh(&{ceP;dvy_73Wr#DNKTZ'
    b'C3K1lE^V=uRc>UJ8%5=a;h@+h5>7dod>(MjaKa2bp~7kB<!J{D=ab{!{%*IU9^-+M7<~pHQx-leOEMBIy2*$R+as|u0)0c-=`~?}'
    b'-iYOOK&m9J!^F5EoHNc93CicCp?_7PlO&X(!(jU$d=Y{e=sQL_MN-g~-TJ<IyA$yXI4kt?mi~*;Qd=r_w)?u%{qfK_#gI_!jO1Sg'
    b'8OjPdovFdCFq{{ZYZw>6VGwFZaB+5{0Ydejsh(?9s&%K*sKZnyLFnv%RD*GF*(Vu;_e9K5+oDTP1Il2n?ID3j*;jF>(T)Hew@B;G'
    b'h&G~7r==6zqp|NV_zJ_o$W2c?a<ge3R|tW}VY@)4mYh1r+;g<TTu+y{cMYrK1RcJjksF8U5;t^s?GsS;>WA}|&P40&q%5Pin9jz~'
    b'<d}omeQ!*yf`lQj15V{I!p&214HvGr)Fmp-daT)-Woe1<EC)Sw$nl0l)L#6d847P$RJl)|96E`lPTiLJ>!)3OKI7dMIoefpF=Vz<'
    b'tl*z|F;DfQ36D8(<q5hYb3tCWH*=;}dLmRJZs#N}rf@bJ)do;d8HT9GS9>`71^{-3(^oo}dhyyZR7?epkOZ<!%6|wbYL#R|^a@JT'
    b'o6HL4{K;-Y?rgI_t-15|j>#LF5It?-prFx~jb`O&66_ehX^T7(C6+SWYstjK%HYNvBj0kOQ_;7n)1I!XB{Kb>?j=31AMgN-?Ju~Y'
    b'tJ{D3$}y9-8B3~tKT%jrQU6D%(j!6svLbwS7oq%b>kq8+ymRaLx&tk|+IMkr8yo8H?EtZj9Q@RskuJ3E>;+!+1$FQ0ja;%DF50yE'
    b'Xf=5=r}bnF1NajaP`VlL9y*XpzCr-pmkk$42yW>dvtmI>bO~j?mn25>=S}vA8as68_5qA+(?_LXbO+5O1x_ncx7Bm9bUyOM#;ico'
    b'j-3QHERqU5+5w=u3b^YFJhn+%c~T+ICG(<Y!zfCEJcpUhZs+JlCNHq=(BR2-VXFe|0TbYdc(s&mQ4|Ciyu(Xp`RF99iP*h`KPjp`'
    b'>Rb-Bj>W|?)LH>sQF$^CmlJO^qO&x`h+hl~trN#%Fh9{Qk^yoYGe+MihA8`$xI=Bax7qyna*Z8gpgT^(k(f;n<(s>ugkBs>pMQ%)'
    b'XD{b}JEAcx+ilGZ348|^PypCN$yBy9%kQH<sWD<#FmIxovLef{k&XE6NrJpqDy0+J$QY8HmWs=p!(&2)y*6#Fu3<_rv@YoS1TZZg'
    b'^ZdlWyeA1yHl^<sBo-avWiY`Gpo8s!c+vVH-AUpQwao>r7Kjck%NI~*Bg)q5jI8pp@qEC5=?g&E9!N1*1aQ)3A#@NCnC9?b%tvX;'
    b'<~JgyTTnuG(tEHY-;E!NoJh;j0*?mKa@-IhnY@X46Lo}|*9hI!ugE+dz#}CT6bX#S$e3Oc!5v5Pb71m%a{hsqNhu@XH~!TwLr2@^'
    b'+QxL8u?Mz-K@otPoQ9Imu-D}_11xn0CVTH#gOfGZnEISO5k7H}!&KsSf9`bN5Ow41#t=b;JqMOo&ZVoe|AwJLc=|4@RvP;D%>V}z'
    b'iVI4<FLte<KOYAo%NZ#18N(3plP+hgd^aO7<hegW@6!&9(0RIbZ6TV<vlbq7k=&pDWPZ30M~dAivECNMg96KO8NG&X9LW^%GPoOM'
    b'H$Lm<i||TRIF4Wli|{6s6a-i-^SvFR+w4O2)uFFuN5#7K2ld2sB^atJS|b#uDn)&60wx!4UbS`Z9e4<r^Q+*B9)rnXIvL<s@?f{i'
    b'O75CymkroqFdBsjXy(Bz^8>V8uP;#C9=_<dH?!{-S=J1kd4$4_8nVHx-7lE>n*Buj+T;zBSvBCBpR>U*%U5Y%@o#bH>0IBsqS(!5'
    b'uynfe`Sh9>HR|wYE=Lb?XC8haih%sUOcvNEJAu%%w0Wfhy;#dhZ%r?N!%qwd6FPD^a~v-sD3sOD$<j~qhS*R_9^-}l&>PSL4j+^v'
    b'p6TKBDa#p&M);Xwa^+(xh{;Twb+Sp-gU1z`qz8)_iU;;-J7Y00-}b7A1(8H8<6UiUUPbGKTzv~;KVg$Ty84}Qp_S<>^S=cdZqmj@'
    b'lm=y(8CsM_t4$IDL)^rECi5HT6Nnh%b66lZzY@tyr9w&F8iw{Mb{oq)e%yL;8}U#^F=u5WR(b;OpuEaFiE)Ba&F-Mb11RFhNWx=c'
    b'k%e%4^rUrb(S~m#x48`o5Qz|wwLP9S_#}KkSfGFq<&y-1DQ38oD`_UpOBpkTxDW@J8&1|K6_nxy@>f_NDHq?#QA<IeJI86uBnkpR'
    b'$c<Iw)v^b4Iy*V-P>Rd+s=60$)aRi;UU=3tcP!NNd7WLKomaTVQF*%Xr!0cWKqy0H`a#2(%kd8|a?yvbI32l$r!SWZMbJ0`h5lr?'
    b'I<v)da;>keE=)v!q@ETp7^kqVnv_{$q(*yFeo1{E%^%tpKdb{IYFc}fia8PcnW`C~8{KION{TD%z$&Z(=hbq+)^X@OoUW=3pS!C|'
    b'DXKpGoY}DUDQGTbWVqrP)cI4oW_Px`cf<=ii4Rz_OJw%Q_OY-xYRxhWtygAIc$}d1V?AWHffTL!`m!gw9zc^&elT?W6+P*8Xl0O5'
    b'#GM(<4k_LG`Q-G~!Qp9&%4&8}Vm?|T?{{cFv?rFs?Z{S)xu2Q7KU<+n*>KWYeTX-u^rllL&S6njZ>`_mub-h&02US@npDSZdsX_M'
    b'qKg?#Y&9;S2bS_mYyxc<z$6)acs9qeLlsP<!QH_M5}l9|vT$T}b|to;MTR<tFPYufEbi#c9QM<j^E8s{_{CADgQ>qy&N%lWxlh|V'
    b'_G_W{TjPD8Qblz}Tg&INTTka3&||KVXLzuta()nf6OOexs&Y1`fZQsH^egi<e;%ji;~li<+W8yh4Jq3P=-Lz?u)2{7m|DB2v?E%R'
    b'&D6TyOl|1R)Ggjj-HvajW;P?*l<17j<Hw~Zw;6VQkjHlX=t=38St7;;79-g(pn_#RvxRFcTT9m?lU9p}RL@BnI3BrgIq5}B3*%Ya'
    b'pJ%(LFFR+O-8Y^6&F<U7v(Dzx?q268F{>$jjBiQFI!*)+$n%+V3u#-uWGwWOSmq_Myt8@&!a`yUZoL$J`<7@!8|M^b(8n-yb8=16'
    b'9AyO*+3D-ypf!It5No?vU(c4Z<vR@gUI^2Arn0(}j=PS-U>8%kyu1fWR4yIP<!8z+c{dO#lnx<n^O|`k4#e7`R=L>lT3(-!&xhh<'
    b'CPz0<V~`{EPHH}D`Ezhb7dbejs~br{j94AiB9Jq(A(H;cZg~8^_`)O0RDwmZIRGjIafXW0*y{`GFc`+_Sn+T4FP~0LXDHhstQ-^e'
    b'uI+Z@wgeA)V?{LJ$4ne>CLXk4;uW~8o)<)`HUpr9`?OA5kon!6pqbtb+<>q|4}VVwl@(C5=OUs0eV?w9B8f$HXn@mHq7&54S3Ruk'
    b'$;()7OBvR5FbCuX)0K0S_r_VOr;mSe9$z|-hi8v}Y(0M6dfff{ItUnO(u##M@tTs0YaC^*aFo~S8&oZC(q?dODG9Q=Lw&JzH!C<M'
    b'qkmEi%o^PJme9!Y%IEVqZv`%P@fcB2J5wS<?JtQyQ2Ub={%OCC?U2cbM2u(jHVWyC-o*krEdVBNli%5tN?3xVVE6voHO62jDx*zG'
    b'QzoCe8_eEr_s9DIQK|btops;7dV6|uct1E(@;;Dw@$~)RsMLL+%snml!;6aE3zTk$cmPB$cON)PHHVqz?uQr^y$`6Iex^>{4>wl&'
    b'-tL1+^gy^#(R?Oa2E#?~Q;7ei3q9d4Oi28LlMnxz*+xG&Gd(=fyyA-%7d@F!98!zLU?$OzRlO3;i-eqz4rcXX>*z*Qed^i{Jiq)z'
    b'<}XIp<NV8Po_2nsCru_=2GYaTvuh7NXJeDvD6Y8D#UY_&B$DyAN?Pwy1fJ<)+J&#lsQC-sKNbw!Lw=6;aed5vR`#jx>S!Dybu|T`'
    b'^cNAor^g9FuDfhrn{IQE-^u|1)9pxzao3~YDcw&$NAQsTuY!$ekbo*gfVcP1z*@0%|LIkt@3C_Yrr#`SxzGHZ(%;o15fABW99+~-'
    b'3!3y1-`vy5*!p`XXRpMvNKdVWfV*qGNa=Ih@s5Y|It6Of^%zj;ym_~t0trRqe%Y10=*iGP)-54`{8|xWDJNGRBE^#Mv?Q~^=}yzD'
    b'J9``{QTO*Zetm=Pt+lLjhpiVYeO@_+lSOBRm@_50o5I=TU4`D^L1xFcLM}>p!$^jnz{FzDJ6;xeL5~!GBG+8J***IaAmg8m`tjs-'
    b'ryW&4d;JDlYa1v>`@P+xqxQafd3e^_KRJGJ__B9=(*31-)_L7_`EBR$2+vYOJwWW_^sv)yQ?m~kuoQaeF^k9{BWBj#I|nVM<=#JT'
    b'D=8xN(8ZM(9=-Uxl>tmUDfNHB7^YK24`YldGLp99bhpegw#fq|PAo@_kvEZ|C?Y3%u_|?vN7()^7`+sF7^!K<p=G94aB<Kg&n=qs'
    b'?WUUG0VS~1C+MZYzvREb2!@4h)rJ(?3j{|^GQ$tJg32Q(8uEn8u{@f^N&hCfEkBG%kl!|A>GB%qjM)?B7y?2@b}h<z!G1HBqlaWX'
    b'fSZ?YVFAk0yc#ed{lyaOxk(Eb&>OfCfy1zzbKaf2bHhe&gHT2y4&=jw3Gq8d8HLq785|-c2z8Dguns*?mCU+bB4K{=A>}^%vxRK8'
    b'Xcw81T!)FsBB8(oJ7(f0S9-?2ugDv6f4}~a?wCNSM`~Uzw-nfuV@~CVxu`Lzw%q>WRGOGx3*(&t6$jnM?5N6P=rirCailVzk-_i<'
    b'-j^ZRguY~s@<W|uZ%0zH@zF&vN9hhUfV`MW4GsXKY-dclZh3o)&zthucY;2}^ExKEm%jZ14{<NSn3eNBcmjt`)afg-i#&+AoYE6P'
    b'^Sg}c4{gCBpMUtUI!wVRh|!F-bo!35jizKAlYIUU8|F0Zd0TXqCwEr8n8|(9$cvee?HR|pHJUBx%9h=7jKq6|0gCwZ-l-GsDCNqf'
    b'Ec1l?4#@k@950Beal#cE%rBKQA6c*N3gEquq(n!)MR$X4A#i^8KXU?LV?#g5PFb{-vGJfS23_6WV2B@Wl#mqkf}eG|XDwAOxiseQ'
    b'Cz9w!%U^CMZ{nA<_`5ZDG0&9E9n7?N(rxgMa0%4A%k#l=vmDXN!@1_7up%9#Rmr4rLxekVs&>x1nPga%E=K4liYbjGMm2FF$3)20'
    b'ZM4vjzUXZbalR)uLPlT6!6w-WM_=?QoAAQQO87%*8O}?6P~1=#LYovb6$X<Vlb}MPi|JB@CFy#gc!?=(sW2)hm&fx}s<^$H-{@mP'
    b'kvY*?cUx~12-qtZ2(Sa)3cZ^iW?r4fO4A#QN>~z;huUS#K1fb&x<IeZ3dlk#DO<>2-Il|c+)8*E|H{i>)(NPoyfS!T#YzjK1ja+C'
    b'M`fVtJpM<%m2c^AT9u!u#1k7RDH)O@GCIT%8;SS`@wI&q93Z@7Pr|xUo8!a>_L%J;J=z?JAQv*@?8Uq_&T?ac2bWua4(0kq9u7G%'
    b'O6NR>OhA}AJDj5irq1BvGtoXiNuIj6_*nCUA{eXD-lNnPu9os<A{_qh?Cohs$%JS{G0TsCRp+qSKK|8Q4o=V!H10Uj5MO*&S>%XH'
    b'p_0$48uEcSWk5y6p{l3~tW2hyTc|;~`f52>)pR)?e;WC0;#aJi^(9^vUA5WxkCck|0qV)B!)bt4Buj!ymPq6+ql8dI;ltFTk;#|`'
    b'eW&^ch>`Dvi36jj7y+Xsvtd5J0^LpJcEi;hd{L>lk{L?zoSy3Y5hWQX=B33egy1oU+7X2;;vPI7cH_91IbJk5@qwY1e6t#wcJo0H'
    b'^6sn-k#L@?!(*`5_K)6n4}a?5?*mv)cMm!T9EGzw5go+z-q{GlC!v%t@Zeb10RfbatUQ?j;TV_xDo&+fLq=jPtxUrS=>XHhnXV?5'
    b'H6qwt^p1+H(2$c38A(Aw9+LbQO9c`<A{YBcY2_$ExT!YaxVlzypq`RyHDkIvoD?W7h&kzxymRzBotp>~h;axWz!t#?s|bZvNUozG'
    b'G`B$&l&mq5!-?BlSy8yj<m(F2dzGNW<?JC8m89>Onu*h<F0O-t-_pvzbx@rt1`A|#Arq#GHYv6(P(*r$AbI8W>La=1_0M(4gK_Q6'
    b'{0HD~vKLc@c*BC_-|%jBZzx3=pZC8qBL7&^{$x6R2=(ZOc0AM{Qt#7RKZe#PQ)fD(%i2uVag#4xBOv>QJt275^G0}i!F=Gt|0?jm'
    b'D*Ueo|Er^(C&laoVX@^mZ-K;N>zz+wGV&u%LWE)7w=*Qcv$jkFb0YIz=KA|g#+1j(E9LdPUaiC^fShu*P6zzs7U4w(-&U-*74x=g'
    b'y{($JHS2B7yscYr>-2Wxj)P=zWzjxPwjze~L9*ESG9p(dcD&4VDmrAQwH1j!t6Qhds%7Ldq=$8e%w^}K4Efz-%IB$EYdr;)%SI=N'
    b'LRHQx0=G7NK1U~w$|%bT5e6Y))^ermbYd2u6>xIi;8jcK24#S50^ny#eGz5F&ArO61J!Ls3FXqUV_~Xq7#4ut6@W37E7G1;@uGpj'
    b'v*vu*8rOZwKL?9`9Ojo7+GuO3gOlTqKE>JAgRBFFD*9-U8wGj0$><^z(bKM%AEzNkAJKDi>CJE0>R%z+nqv(XBpn$~=LAn)2?SDN'
    b'wdA0aLHLt+E@L<;VI5I;?f>82wQjd<B<cTtiXK`H35O6bx<jUC97j%k?2L14@0s0+6PY3*nHELr5TxX+t>@YI*eBb%_5}cMmNJ<i'
    b'JDDSs1khdRuCA)CuBwkqVBkV#nMB;?8r`T}_e?xAkNnjT<jqCIu3NSfKTWHniCW(>dg}NZokcRN)XA;Zv(tj>F6efpY~8lKb=&53'
    b'>yl)kGs$u3lZTe)tOqP)6<)Qts&!Gfy=+Y!rBcnx+9l&<V%mij@Z{&8U;Y>K|DfObPC27(IRhS-FlfO~a0Bg{sX&i0_sGB>oVfuM'
    b'*-cD`b}c1MYt=@oU2B_R2izQ9Rv+FRVi6Zb?y$*!)Q&SzJt=1!LGMdJ)O?qComeLa_J)8NYT>BaBNS9k5CFRL?xxMb{CdU>ETDCH'
    b'cdL|lw>;k6>e%IrrbWnkIiqSB&xN<k_-<87+d{_c-+ozp_Sw2)vt2qi+uqo0`(v}68yjcKEgcuWRbAsUF58ttJ9jiDOH3EE(aJ|;'
    b'r_^+j5o*f-?RW#U;}6h|O~B$8^Hm<L4mL|#3+#ws11r`<dmHy|X-DXg(c6*HQ|df(!0&f`Lt`gzXlMyqiN$3<lkTh+*a*7!UTP;a'
    b'=h_J^&rWb=f>PK|&n8_Ysc0pT;~)s(Pe*5H17NNOR#sGEsPr0Dh8&2X9@&bAQZ<cge3M&))N_=;g_s^eS4`dX$CxEVb?f|8BvL&L'
    b'5YkX1f<(7V!I_*{o81yxp~#D~l1v#TIllsYQ>J7MgmOSm^<N}xvDV)t$_8|{aMs{+y~j$|nQT#n<B2xM^Yk@mffvWz6>-*qlUE6u'
    b'=UFiqP3~KiGS||hpVqtpcD8$i*STl%r0U>OM`SIQn4F)Um83sf8aW5D-DnpwAX|k5$VH~Hlp0urXy&&Z)qgk#DdPYSF*6AVA^koF'
    b'wO8Yy)&dS<&uP~!HG1Pk>?2}M-}r@>2`+mzn~EDO0H0(T@UT-c7+;v0E3E1g`Jy#wdgIY#WwE8o8`4#2dh-=Dh0Cm%_bJ@io<|6L'
    b'jK`<Es_AJa#XhwjBQ|gOKYQ}KgohW&KTJ7v%)7N3^R~;F*RLXk>P1U$mDxy(W~HnskvAV({(J;|2IkcKIiPmH3d?4_53wr&b(dO2'
    b'Az{3c-M+=hYL=d>4t>k9%@w5bMt9pE-CVzJe8s0Q&tGMI3_7CgI2lR=J{IV6cFttimA`$v8*fME10t~zHjhOP+-0bG_E>28J-U(T'
    b'47|o?2^ghf>ppX_RyqXeo{X<j43nX7Yl{WgKtFJ7JBuf~Qj9hJ-~ZW)i2wBvhXe#Z!=N<X9_@k&XLxdv*+Sh8|CY}I^q{A2jV^9Y'
    b'0Mc?<(Jh-5-4d%6)p=A0&Ebj`5}cuuCGzqD51@wK-Z=tahsC`)Ih^#XUbmJl7UHG><+|~c9x8JwW)w@UTLJ5xq#wyy5HYegSM&Zo'
    b'w%}b|Fmw4`c>JlyTF#K*lag-Vl~@#A)*BCJ7bCAqHZM*_K(QWc{#x`|^Y5iz>->3{y>;37wRf^~)twB0w-SqvWWkE~s7aBrMp8VH'
    b'&xqJrvd&R941e=p;bhoY*T*NbO@%RFmb}}fJMXSy07KP2NAd->dJ9hW+z{RS*BSAF0fx)Wm$W<Un(%h9ni`weu&%;|7J2I{&He;C'
    b'e#aNf*j`NZ-r9U`m6-4CuQ1<R%W3^{to9ts)c+as&TORb>T}TU`X+o{+!jSG*^Aj42J=4`lyfSW%e(%dySK_K0#f15ZkBd$XEFx`'
    b'i`r@nJ3e+*fVK{oQ!D_y)X$&8ES5EtZl5*w)@6-F+I4M~SiFbg$@GSJFC1da3js~S61i5QuaPCKJ8=cHmcKzvgIOj}zLtqgxV3e-'
    b'A|Z2lRh?eP;<N0yf}?QNe(tpIp0C;EyL6kP9z~zQ_vbOVBY4BT(*njXnvHBSMn#+PD?J;5_jtZ&+z&hn)`?0Kx#O_Vdp*9s6*q-m'
    b'-NR+X$nZEmVzR<k?nb#67vv&$ba6p0qW@o{;o0I`Y8JXJhR@yy>l%ly8QrB2Fwq4^oDoVQjZ#!<9Dc0}wP=I2OA58lccC8m(^Pl`'
    b'H${a#S7#k>!kwA7^T;i?Z~r*ogSZZyKY`o@p6g*RZh6iJEUTv38tl4FFkC!6E5TvwdgyD^7DsA0j5H6)t!}Xnd^|K$W8~by#l>ut'
    b'!p@qqmIi4EZ5AM1L7Th*NA$7*A4(K!t!aRzL_Sh;Y=u#ZPYy1NozuhdtdB_as^-q5G8%{PV@<fmY4<$k8f9mQik)?VcaP~(7}igZ'
    b'((e1RL?qBvKfate^QyC<kZ8w@ZDJd;(R#7mfPofX=N+%|T3DOPr@m}AOIf43Tc*$QhK{_P3_GLRY`6E)BBVy)q^h~DD06v52{L0G'
    b'FsanfV<CnG`<PEG4B8^8fW`N{aq-as{9~P_zsemk<T&%x9x^T=f>0x?N+a%gzC>DH`6)a&n@6k@NiK@4Y^c0Q_xrkx8IyxyVx7Q&'
    b'*T-P=$B#>y{ojfQiS&R8*FG;**v3GzS(HTra3oPFwH<NH^DI!2Vq?K;`V@v$IsIO72I1o6v;dyTI5RaByhv6w$ADR74tTt8eZX_a'
    b'A|yQQX|>lqlgKUF+n@IEs$Fv8(`qje94npvth;K~o4q@l9hzuwcD8OYI|?dB8rvdw-OV(W0D<|FwKZq5^f1Xi?oXJ2L3zd%evPQA'
    b'L3~1$DiLrA?JFvn!dOoZ!b$L+sHFl3tA`j>N3a6mmiZ8`dW6KdQup;tUSMPce5XzGYJ?E*7YG!8g=&*1B2u{iEh0-{rVm?ubUuJk'
    b'rdU1Il}+HvyTjiFla(`;Co#6mwhg}pp`((RqSm^Z;!2@`Cj<zRA?6=A$W%T@Axsa1Wan^iI;uf7pvGG5-MVavX_mRluE359)|J$W'
    b'^w1V*jWH-BMYVY;N36+kAXYd%af4>J7L4C0ah90|F%45YSeTxv^Q-7b(cwKg%fo^UDDI(w30S9?!HN56^V5?bo<G(1dcje66ca^D'
    b'fQ3P%XEV^)8}AlU=cq0u*OCgOBBqx?z8<DA<<U%1MCHX6M&nU@)$Ps3vuyJob=;{EJL^v5s#U#5dl}5<yrGSYmww81%_R%X>AnqW'
    b'2}Mh@;@zOO#?gNsJw29ac$+*oH$N+!CEu98I_7#J@aLG3knE3ZnBK8%1lng90B)~{TXq(J-r3F)%R*ng61!ha4>RB}nbE|jttdFU'
    b'<0pa?9zO|;I13q$>%NSjKkQpLiEzS*(O5=8+myMpbOI=?r+AmE!|UDZC5vIF&ZMM;N^+65fP7Rc$B3Fkv|y%js)>&BdtSYuJD3X='
    b'X-Hm*sv>0usKh$YUd5lGz&P>7zFJ-vW{DEy7CkMvbDLd`g+*f#hVswJ8U_jk=~7gKgk8px-dAnG$(Gej!4^h0+Cd8|Dp}%pn#t8V'
    b'b$hi1n~*>rkH-Hmk^gNaGOF_8M1?|`e>eP(FPQn4bwqQ}l!#~7?n(lhZ%;g~S|X$u2_2!wiXGc37Bm?bL=XRTx57u;^u*8Zx<)t{'
    b'Ld^WQsbpKP@0Q4N3tR;UaDy)eg40s%W1-}s26ByC<8L<N(D2k|`+=!>`8zA1z756SEeuX^YwZ(L%re5(v{&0|<Xio#fSK16$-ET9'
    b'JcnR@Xgv7r`aJmT2BBxe-<=3I6%_<6CsUjnBwz}KE+32#^jkc*4piLY3y5vaUR%#R?y@V@Mlbnz<OL*hYywUG#P7j#NVYj9A1r{('
    b'xJ@gsa+HA}=D&OO_D30Xc$NzBv(y8+8=(2dZr3BDc9qzs-orv1Dda6aN({`%ZuFQ!%AzkfjvWo}86JeURlq+_|M9(r1F1`+OoDwR'
    b'lAy3`c7k4DArQx$j}-6oxHJBGcy@F-W|7~W@?(-@(x#`2ykNn*H_bn|d3G-nSJ_P!h}U5VdY}Pw!IZIUo)$pH>9XuxrvNXC>!aFR'
    b'gN!S{p`(10T6xmzrI%BlU6pU9hRIR*o&+jIXk?BA-nU(LGoM}<52+9Vd%Y2C1q)6rik8b}&>bjAv>j>sosR?sg&#EsFBf>d+YR~+'
    b'q&&=W4ut?OG-%A{`s(?fz<s&kz8q7KJelL!SE^Kp(RUohXu<hn%nUNGyAp@bZ9F(UGOp&MH(dCYoI7saHcivlGJER>2N#57f_rdU'
    b'H+=%EBbnvN66*n2*Y`s&;dy_`mRH~b+6(hHN+=EWM0t}-PLE?)KJ;EiulXI%taRj>I#cAGv&FNzzkV)J$ynh5oMhK(Y7tLibM+~d'
    b'SGddbk^QBU+$E_ePIuUo%s*7}E6!BsaYMfATo&(g5>iEm3dCVaitpDq<??^aEE_DP`p{&($qdv;uRFqsZgle1{@!evXRXGw*7l)!'
    b'-P{IM(`qN}1A{gRwbcXRenPo;T;~y2IV&wRK?Y|dD%C<i!E#SOadjE$@cZYlu~Z~?XB8wW>JzM+Xbp%um1|^s2g?ph6WvT(soRic'
    b'nnX5jgug^ke@KUz!cRtIEH-8r>>n_^P$+GhA5du~L1iykI_TSwl9HejL4OhonfAt%!<hVd^yK>nNRF(*6)maO<ZRT#V5hW?HWY5}'
    b'adhQ1sajzab|;j=$o4bMc$BF?a|6c!`=Q>kFFKK`t6LeK=%=3=cy>j$(AgN@Yx=tz8=Lisb`8b!pQO+y`G#@eH@zx;*sH2v{#G%)'
    b'{v`Y<_G;nz4<2KBrhX<$<+BV<uTOV`N?dyJ&L;U6I)Bv5jf?ICY!r@%w_TN~WhL6`W&R;@Pa<K(t)xB&5;{iH2NcvP*p%=U7E`DC'
    b'0F=xrs)oossIi?)->P22{Fd{ZmQjdf;Nu=xqk~bD8;btK9|w6i9f<y<F$Pm<`iVqbP1b`hg^nF6TrU+17UYdg-#1r)ymKFtD-yBk'
    b'34|oip`3S2@fzW3R{KsPjbx%rh5~5-4HaK@C!jZpt=o<YDpIKrE1W5T!^w{oMqjqys0N<L5g1yt=tZt4V?6G_EE~71gAkrMa~IOA'
    b'5j`vPEDM?5)Cz`GdR&_kLz<Awm(WBjw1g&tHVb%KhJ6jj4vEoL7Lt>bV<BNA?OxMX0&Pf9Pun0#-^W-N{W_kGF9|gAz3C1ya>zSE'
    b'LuH6DP_WJ6?XR*e3}BW{t|+%@YP0NJ$q<hi<ox()R9Ckk(GF@wHkx2ZoYNi*8Kv9rqj^XXEL|tlF;51T9tXCJ8Ie+UO1Oaq11eLU'
    b'gLV55-<iz1L*DwkUgaoIOs~4`Qt=(Q9~dUpCN7sulshXCsucl>^nLN<^u4LEUEQW^rX_+#fKAKo;dFEr6E#Z=;<<Gr%<3kw_T@ji'
    b's#WYoV2U7IY8M9_TsrAu0hLJ0wQXg6x4Sf!gZReaZLl|7jF;&M4Nm5#1;%ndV$BO|tNdB{S4d{eY4Fvm{69D8+v}!H6rvOpKSa^E'
    b'BoPfo{NpmwTif9YOg?;)GRB<8Q%SsS40(`NV?(hI*Ck9vY<Y9}@C%L_N&5i~WGqK&z1j2-?%Ty&!;FODULC&g)5m?5cI{pIcEFA='
    b'l)57d-&IISEKy!ne9%!p7hIb0hNg?oH5SBlq%#I;CeHmuropQhb(c;9yMsZWHUu29fkQE5_ZW7?mz|OBIwd4G&Gyr}__(i-+9)oz'
    b'mLkW}sk+%W&5!BiBApI;iR}i9&0nPI@5L;K@pxDz^G9|hAt2`=?jULDa&D)lyVkh!7R*vEmY4i|HUI>xV@cgms+@)tg4Do$7iMSF'
    b'*+JN)vqGjqB0MgECot0)2=Q`ghXD{NPr2ZcnjvMe!5|Pu>yVE9hSQTF{W-qs4qYoSq{qO7W{6|TpVH&;Ieb4RxI6e4rwabTN8w{='
    b'mJb)fm&!#DBLS5${k)k@CUz}&?8Z}*Fdri289|*+(~&Gs<o(?S@Nq&I3k(EEEJ(?FwV$X+_)BQ%x@{B5Gf)gsqt=ULe`(K{cy6%Y'
    b'=?sjdtS%g9liF$Do`H0gOF|6S7G?VMv=dwEr@bNO$OtF`uMcS9Bz6Al(G1>qLgo^OpZ6zYl0h7KJ|bWUrVFQlBe-EnVK5TdNWgL+'
    b'b+Qkz72=Rg?|tlfhQ}!Q1{re!{6lo%Mf%wlzdJJ3-^x$?Y9F&Nc+MQf7Ah7E0dA1?nWMfp+wn#B6DUYnAT8LR;QLk|lAfxXFNP`*'
    b'($fqRvr$8<0JbsJtnpijAoH&FOEW(BmHs?@7n#k6jd!iaWk3V%68KHHDE<Lk<4jxllfW(TPik#fN?0f{GBh%BywIdgAx@ezwQH<#'
    b'd;m5*ml%Y{J2lq7A!1@u0>zjp)?(6XCi{#ZP%S|pOy)rxCJw`}&_oWrFPV!In1n!p*wC)ukcW<!l!EUi4qXo)-u533@a2*@ICe=6'
    b's4i*kBzsjmiauIfQU(T>_-JoPg7>h44NHocYDo@t44>U`&jwgkNhzXNQpCK<HR4c{k|Ly3k^^0`&uX>F&-am~e)-$4H!Cr&6$4J7'
    b'b^JDR?22Xkhbe<Feb$>CFw*m9Z#oI<xOh^gObWW=(W6JO(o){}kRl;SZetY>=&R3v!7n!z#kBZ~>KYIRmsEX|v?EGB6)Fv0d~A?L'
    b'0q6yH(sTe77Da{im@`xThe)Yme>n&Tp`@b05T`8+k-#0^7c-rhD&AGCS0mSsXvLDYKI=O-8uf;`sYny}AKswh7Rl0HSjZ8{;yQ5s'
    b'RwT;B9|m=vEO<E<!z>Kpf=uM1#zH7veYMJ0w4unowhaf_D@`doeN9`sL9ngWYK~E3k5v&ppxC^y5b|DNlxz_9C#?00hA^)|MkhkG'
    b'Cq@)Q5-G-)fJX&&|2#0Hlk`LPYA~K`n%5Yx1;X*z-B`^8bm|0D<T*wHPbXc%sIca%c=(54NwP}@b}MR938WPJRopMK4RU61q0{%U'
    b'*?S0EzxNWuoWa%|MNP)h6E;?Yi5rf`mtxjP2gCGqYGj{8W;xtp=)`??_F?LblqtQJnIhcA^a{p!Ixy3Z_Hx`c<jTXB<Xd6Eb+6A&'
    b'HE%U6#GTt{d_L{8Zp`U7-!y)^fp6$+fUki~anZdb85d8bPxHt;($2yGdRGIx<lSd&c70l!LJRG&f9b~m{p+`#cN_2i3Kz54NewSF'
    b'>XizJJo+lv_!nB<H+gf2Ji<Ig<e3EN&u>wtLwMFcbSDU5mN0KQ)~Xjcr4zQ6(<ao~F`ldmxRLw8Ji=RJ9PY>R`E)QrS36vUU$~RU'
    b'o12?-tkVP;e#&tgbX><Oghm#hJ)ZPB8!i5b4RkizWOsL}RdbGmOB^@p@lyVP>051H-B>S_)!pAn&Cz4uqEeFA+BpC9rn3Q?mqUXr'
    b'Ry$|>qeEWAK70~O)hbs2GVvHTe3vOsGyF&|j)MTRql9l@SIz-f^--%j_UM6U1OdR{JrMYdv$=Ibt2f$u)w*lws{~{iLxl?z=_S0*'
    b'+LN7<J$C14ZCGNA4H;Xump?;G4<2lwGJ1F;ddH5qxT|l1S%+zxi<owxfN2No;ia)>D)>+Kj5*%LJr->lsaXPuiyt!y+H+kHXsXWm'
    b'AyEVTP;DixWFEGnrF~z~v04JGi1dlKt(~-!xfq6C3n7AGE2>&+3uT{bAtY^pgf&5%w9S^;Halk5?3sOgyDu8ScB&P|NzDhi`pb0i'
    b'E3937+XoMlhc|lVqx^XPVPb!C(}}C%Bi&!&&v+Yu%-B*yP9d^krI6@$U}1K>AcN60Pxh2bpYbSAO&+=ATqVcSDYT%$gfziQmZ`xf'
    b'=;fwi#Zg~3(V%rvR9&U<6T{Adx7hO$$~osCK*zxK*dh!d8`bF-hB@T#U2{Q774Q0%E>I6ZDAu8?5!YNJwjM{!jV$bmywsMQA4GM2'
    b'p%bYJY)Be%U?^3$0!G~|@F?&?FvF|x?4I&$yM$+fwZaBh;o-d;54T-|twMwAP^hb_<r>_|GxhCPS%K&8gNjIpLryR04>GjpI&Yq~'
    b'oBO-sOH^BCK#(#+4lF?QO`5LB*^DeA!s3`sfIXS<m#?J!iY!?a77Wy14j$j<dHt<aMzpx39E!*(c8QmlMylSPouOF<*4_{U7zta6'
    b'EL?_<L>HF$Lvt{rB}kqT+l8bgS^BbDcmUR(VtdkB%A0=2Sf-;Riq5z4^1B%Cc8Xs|_tBB5HtT3CIaJ|B)-aWK8`i8Mb-&TTzm2MO'
    b'9jRWWv+|&2*cyEEO@1ER>jIh{SUl7H)m0hU$eMmh5V0~NFz?)DNspr3+M?Wa_`G*2DO!(vZ9mWf4TM9I*niC(>Cv4bZcVPO1$FMV'
    b'!u@nIOBZ#wyY0$w$?My~`rP;Kc6sOCj%scx{?$4T+S0>d+a{k*?rul<ngIp8P#?(7L#~6ZAxk?SyzZXE_T-C|MR2cqsJ(LRRtvtG'
    b'gS5?|mu9^Qg#aLeD-xYUah2SdI|6WxV=(6jqkH!_OdZGnzK01-5?UZLTNOp)*0GN$K^QmrV!gk8^7@CPw_y7ps*SJM+Ljp$&%F8h'
    b'=xO;A#G%Fe|Ks`Fqw)s?o}uuF0OOWFMBojDM_xYp?&xLt15&rE`0}p0SLtKGMkNFG{N?fA%OAi1jYu{edfAPQ>`o%{)2r`~>}I8K'
    b'pIbR{r~9FBFA0<{CjKC|;`iK54<j?nx@YMzabZPGDOI?MK`x<t3FnmEEW$t7rmzsUEG;PpB|qg}%eqbJcmFlQ{k~kE$pt>1Q=HZR'
    b'0~4_aIR'
))


def normalize(data):
    return b''.join(b''.join(line.split()) for line in data.splitlines()
                    if not line.lstrip().startswith(b'#'))


def regions(data):
    if IGNORE_NONCODE:
        data = normalize(data)
        start = data.index(b'localnlegs=9', data.index(b'run_regression(){'))
        stop = data.index(b'selftest(){', start)
        hstart = data.index(b'localtblock', stop)
        hend = data.index(b'tblock=$tblock_full', hstart) + len(b'tblock=$tblock_full')
    else:
        start = data.index(b'  local nlegs=9', data.index(b'run_regression() {\n'))
        stop = data.index(b'\n}\n', start) + len(b'\n}\n')
        pinned_lines = PINNED_RUNNER.splitlines(keepends=True)
        hstart = data.index(pinned_lines[1988])
        hend = data.index(pinned_lines[2039], hstart) + len(pinned_lines[2039])
    return data[start:stop], data[hstart:hend]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', required=True)
    args = parser.parse_args()
    try:
        candidate = Path(args.runner).read_bytes()
    except OSError as error:
        print('TALLY_AUDIT: CANNOT_AUDIT ' + str(error))
        return 2
    try:
        same = regions(candidate) == regions(PINNED_RUNNER)
    except ValueError:
        same = False
    print('TALLY_AUDIT: PASS' if same else 'TALLY_AUDIT: FAIL')
    return 0 if same else 1


if __name__ == '__main__':
    raise SystemExit(main())
````````
