# CtlDoNothing — round 32, wave 1

## Verdict

**The do-nothing control is rejected as expected. A round that lands no tool cannot meet C1's target.** The frozen revision returned exit 1 and `C1_R32_PASS=false`: `kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0`.

Axis: **operability**. The runner byte-preservation constraint was maintained. No other axis was assessed.

Control: no change to frozen revision `c31814978969a41a8e9b0f7d99fa308c5993c1b7`; no audit tool added and no commit made. This is a negative control, not a killed-mutant claim. No baseline/mutant/restored comparison is claimed because this assigned control makes no mutation.

## Evidence

Read the frozen counter and contract before setup and execution.

- `.ufo/evidence/round-32/contract.json:13` requires the committed audit tool's correct outcomes on all copies and the pinned runner hash; `:19` explicitly requires `tool_present == 1`; `:30` states the target.
- `.ufo/evidence/round-32/c1-measure.py:240-241` detects the committed tool. At `:252-263`, only a present tool is executed. At `:265-273`, copies without tool results are reported as `OTHER`, `exit=no-tool`. At `:274-277`, the complete predicate is evaluated and a non-passing evaluation exits 1.
- Expected detector: the frozen counter, run once with the assigned frozen revision and a fresh empty work directory. Expected rejection with no tool, not a counter error.

All shell commands after directory creation used working directory `/fast/scratch/hyaku/tameshi-r32-seats/CtlDoNothing`. No sibling scratch directory was opened.

### Setup

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlDoNothing && df -h /fast
```

Observed stdout; exit 0:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  691G  113G  87% /fast
```

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlDoNothing/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlDoNothing/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed: no stdout; exit 0. Checkout occurred only in this seat's clone.

### Exact measurement command

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlDoNothing/lane --rev c31814978969a41a8e9b0f7d99fa308c5993c1b7 --work /fast/scratch/hyaku/tameshi-r32-seats/CtlDoNothing/w-nothing
```

Full observed stdout:

```text
COPY set=kill id=T08 outcome=OTHER exit=no-tool sha256=12ad1d9076a55050 last=''
COPY set=kill id=N05 outcome=OTHER exit=no-tool sha256=e1ef181c1e621962 last=''
COPY set=kill id=H03 outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=H04 outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=H05 outcome=OTHER exit=no-tool sha256=adf6763d6524f342 last=''
COPY set=kill id=N01 outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=N02 outcome=OTHER exit=no-tool sha256=31128639afc3e57a last=''
COPY set=kill id=N03 outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=D01 outcome=OTHER exit=no-tool sha256=71a66c5a611d408f last=''
COPY set=kill id=gT08(arm=190) outcome=OTHER exit=no-tool sha256=979be515eb300af9 last=''
COPY set=kill id=gN05(< nlegs + 0) outcome=OTHER exit=no-tool sha256=461cdc5f098398c4 last=''
COPY set=kill id=gH03(form=2) outcome=OTHER exit=no-tool sha256=7f1787411f0ff16c last=''
COPY set=kill id=gH04(rc=$?) outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=gH05(drop=5,dup=7) outcome=OTHER exit=no-tool sha256=b8c94ec0d07e28b5 last=''
COPY set=kill id=gN01(vector=2) outcome=OTHER exit=no-tool sha256=c0a32ec4e69d3cb0 last=''
COPY set=kill id=gN02(true) outcome=OTHER exit=no-tool sha256=29d0e2b6649efed2 last=''
COPY set=kill id=gN03(or) outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=gD01(drop=st_sourcescheck,dup=st_js) outcome=OTHER exit=no-tool sha256=8331cf69e0006c12 last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=bff28c5c2480f19a last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=fd8d901d929b4f1c last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=52f768d936c9e434 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

**Observed exit: 1.** One counter invocation; no retry or reseeding.

### Before and after hashes / restoration evidence

The following command ran once before and once after the measurement:

```sh
sha256sum lane/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

Both invocations returned exit 0 with this identical full stdout:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

No runner, counter or contract bytes were edited; no restoration was necessary. The counter completed synchronously and no audit-tool process was launched (`tool_present=0`); no started process remains to terminate. No production source was edited. This report is the only written artifact outside this seat's scratch directory. No tools were installed or updated.

## Smallest safe correction

None to the control or the frozen predicate. To meet the target, the L1 must land the real versioned `tools/tally-audit.py` satisfying all frozen kill and accept conditions while retaining the pinned runner bytes. That implementation is outside this no-change control's assignment.
