# CtlLineCount: pre-data controls

## Verdict

Both prescribed controls were rejected by the unchanged frozen counter: every run exited 1 and printed `C1_R32_PASS=false`. No control bypass was observed.

| Probe | Must-kill correct | Must-accept correct | Other | Exit |
|---|---|---|---|---|
| Initial line-count control | 6/18 | 6/8 | 14 | 1 |
| Byte-size control | 13/18 | 3/8 | 10 | 1 |
| Restored line-count control | 5/18 | 6/8 | 15 | 1 |

Axis: **operability**. No other axis or learning-trend change is claimed.

Mutation: the single behavior-bearing expression at sandbox `lane/tools/tally-audit.py:16` changed from `data.count(b"\n") == 2080` to `len(data) == 106538`, then returned to its exact original bytes. Expected detector: the frozen C1 counter must reject each shape. Mutation-testing classification: **inconclusive as a killed-mutant claim**, because the deliberately inadequate line-count baseline itself failed C1. The observations establish rejected negative controls, not a killed mutation of a working semantic auditor.

## Evidence and scope

Read first: `.ufo/evidence/round-32/c1-measure.py:6-32,82-168,177-196,264-277` and `.ufo/evidence/round-32/contract.json:9-35`. The predicate requires all 18 kills and all 8 accepts; contract line 33 names line-count as a pre-data control. No runner, counter, contract, production tool, sibling scratch directory, or production Git index was edited.

All executed code had its working directory inside `/fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/`. No subagents were dispatched, no other model/runtime was invoked, no tools were installed or updated, and no started command remains running. The only write outside that scratch directory is this requested report.

### Setup and pinned measurements

The scratch directory was created with `os.makedirs('/fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount', exist_ok=True)`. Executed clone command (exit 0; no stdout or stderr):

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

```sh
df -h /fast
```

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  694G  110G  87% /fast
```

```sh
wc -lc /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/mutate-and-run.sh && sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

```text
  2080 106538 /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/mutate-and-run.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

### Sandbox commit sequence

Initial control commit (exit 0; no stdout or stderr):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlLineCount
```

Line-count revision: `b5b9bbbc0191e379f9e1d77dcfe1f1313ff95e12`, one sandbox commit on `c31814978969a41a8e9b0f7d99fa308c5993c1b7`.

For the second shape, only source line 16 changed. The sandbox commit was amended, keeping that scored revision one commit on the frozen parent (exit 0; no stdout or stderr):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane -c user.name=ctl -c user.email=ctl@sandbox commit --amend -qm CtlLineCountSize
```

Byte-size revision: `fdfba90e13c7c1086aa63c4518e06c5d685bfe44`. After measurement, the original line-count commit was restored; final sandbox HEAD is `b5b9bbbc0191e379f9e1d77dcfe1f1313ff95e12`.

### Full control sources

Each source below was extracted from its scored commit by the displayed command, exit 0.

#### Line-count control

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane show b5b9bbbc0191e379f9e1d77dcfe1f1313ff95e12:tools/tally-audit.py
```

```python
#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True)
    args = parser.parse_args()
    try:
        data = Path(args.runner).read_bytes()
    except OSError as error:
        print(f"TALLY_AUDIT: ERROR {error}", file=sys.stderr)
        return 2
    ok = data.count(b"\n") == 2080
    print("TALLY_AUDIT: PASS" if ok else "TALLY_AUDIT: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

#### Byte-size control

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane show fdfba90e13c7c1086aa63c4518e06c5d685bfe44:tools/tally-audit.py
```

```python
#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True)
    args = parser.parse_args()
    try:
        data = Path(args.runner).read_bytes()
    except OSError as error:
        print(f"TALLY_AUDIT: ERROR {error}", file=sys.stderr)
        return 2
    ok = len(data) == 106538
    print("TALLY_AUDIT: PASS" if ok else "TALLY_AUDIT: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

### Full counter receipts

The counter was invoked unchanged with a fresh empty/absent work directory for each run and no `--seed`. The complete stdout follows for every run. `other` counts incorrect classifications as well as nonstandard outcomes; it is not a tool crash count (`c1-measure.py:264-273`).

#### line-count

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/w-CtlLineCount
```

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS'
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: PASS'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=D01 outcome=ACCEPT exit=0 sha256=71a66c5a611d408f last='TALLY_AUDIT: PASS'
COPY set=kill id=gT08(arm=93) outcome=KILL exit=1 sha256=f232726a1d189b31 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs + 0) outcome=ACCEPT exit=0 sha256=461cdc5f098398c4 last='TALLY_AUDIT: PASS'
COPY set=kill id=gH03(form=2) outcome=ACCEPT exit=0 sha256=7f1787411f0ff16c last='TALLY_AUDIT: PASS'
COPY set=kill id=gH04(true) outcome=KILL exit=1 sha256=eceff075da31e6d4 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=7,dup=3) outcome=ACCEPT exit=0 sha256=9ce93fd5f77f434b last='TALLY_AUDIT: PASS'
COPY set=kill id=gN01(vector=1) outcome=KILL exit=1 sha256=ebf4a902638d568e last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(or) outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=gN03(or) outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=gD01(drop=st_roundgate,dup=st_checklist) outcome=ACCEPT exit=0 sha256=51ce396a6cfe842f last='TALLY_AUDIT: PASS'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=KILL exit=1 sha256=7c76617e87c11c49 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=f6908f8b4c83fa77 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=b79aa21e9dbe03de last='TALLY_AUDIT: FAIL'
C1_R32: kill=6/18 accept=6/8 other=14 runner_sha_ok=1 tool_present=1 seed=9bf38b035dec2f79 rev=b5b9bbbc0191e379f9e1d77dcfe1f1313ff95e12 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty.

Raw receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/line-count.stdout`, `.stderr`, `.exit`.

#### byte-size

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/w-CtlByteSize
```

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=180) outcome=KILL exit=1 sha256=23352e6ba8d8795d last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(:) outcome=KILL exit=1 sha256=fba8e1cf3e1bfd8b last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=8,dup=2) outcome=ACCEPT exit=0 sha256=f810276f5503017a last='TALLY_AUDIT: PASS'
COPY set=kill id=gN01(vector=0) outcome=KILL exit=1 sha256=71d7c5f20bfccac6 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=KILL exit=1 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=gD01(drop=st_kagi,dup=st_citecheck) outcome=KILL exit=1 sha256=9743dd25cf925879 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=KILL exit=1 sha256=7c76617e87c11c49 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B4-cosmetic outcome=KILL exit=1 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=e8db80beba474362 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=17edeff5b4391532 last='TALLY_AUDIT: FAIL'
C1_R32: kill=13/18 accept=3/8 other=10 runner_sha_ok=1 tool_present=1 seed=6230c16c326b4817 rev=fdfba90e13c7c1086aa63c4518e06c5d685bfe44 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty.

Raw receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/byte-size.stdout`, `.stderr`, `.exit`.

#### restored-line-count

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/w-CtlLineCount-restored
```

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS'
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: PASS'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=D01 outcome=ACCEPT exit=0 sha256=71a66c5a611d408f last='TALLY_AUDIT: PASS'
COPY set=kill id=gT08(arm=17) outcome=KILL exit=1 sha256=cdfcfd67ce94f377 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(<= nlegs - 1) outcome=ACCEPT exit=0 sha256=7184b157539cad8c last='TALLY_AUDIT: PASS'
COPY set=kill id=gH03(form=0) outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: PASS'
COPY set=kill id=gH04(:) outcome=KILL exit=1 sha256=fba8e1cf3e1bfd8b last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=7,dup=4) outcome=ACCEPT exit=0 sha256=2ef092a7a155792d last='TALLY_AUDIT: PASS'
COPY set=kill id=gN01(vector=0) outcome=ACCEPT exit=0 sha256=71d7c5f20bfccac6 last='TALLY_AUDIT: PASS'
COPY set=kill id=gN02(or) outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=gN03(or) outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=gD01(drop=st_roundgate,dup=st_checklist) outcome=ACCEPT exit=0 sha256=51ce396a6cfe842f last='TALLY_AUDIT: PASS'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=KILL exit=1 sha256=7c76617e87c11c49 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=56fccc40393f580b last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=90127a37b0e4f931 last='TALLY_AUDIT: FAIL'
C1_R32: kill=5/18 accept=6/8 other=15 runner_sha_ok=1 tool_present=1 seed=4feda7ff46cad070 rev=b5b9bbbc0191e379f9e1d77dcfe1f1313ff95e12 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty.

Raw receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/restored-line-count.stdout`, `.stderr`, `.exit`.

### What the controls missed

- Line count initially killed only T08, H04, N01 and their three generated counterparts. It accepted the other twelve faulty copies because their newline count stayed 2080. It wrongly rejected valid B3 decoy comments and gB7 nonce comments. On restoration the generated N01 choice was vector 0, which preserves newline count, so the restored result was 5/18 rather than 6/18. These were independent fresh-seed runs, not a replay.
- Byte size missed H05, N02, N03, gH05 and gN03: those faulty copies retained 106538 bytes. It wrongly rejected B1-T07, B3-decoys, B4-cosmetic, B5-renamed and gB7-nonce. It accepted only B0-pristine, B2-reversed and gB6-permuted among the valid copies.

Neither size statistic captures the required tally or harness semantics. The complete per-copy receipts above show which cases each shape got right and wrong; there was no `C1_R32_PASS=true` finding.

### Restoration evidence

Original source hash (command below, before the one-line substitution):

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/tally-audit.py
```

```text
9dd3ea3bd76f1795dbb25f19cd802e3c72cfad1d200e69dd6deb57000b1201e5  /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/tally-audit.py
```

The same command on the byte-size variant produced:

```text
0e6525423dad64b0131b393b3a105280601fd4cd04040b71fd82071aea447bd6  /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/tally-audit.py
```

Exact sandbox restoration command (exit 0; no stdout or stderr):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane checkout -q --detach b5b9bbbc0191e379f9e1d77dcfe1f1313ff95e12
```

Final measured hashes, after restoration:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/tally-audit.py /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

```text
9dd3ea3bd76f1795dbb25f19cd802e3c72cfad1d200e69dd6deb57000b1201e5  /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/tally-audit.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlLineCount/lane/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

Original and restored control SHA-256 match exactly. The runner, frozen counter and contract hashes also match their before values. The restored counter receipt independently reads the original committed control revision.

## Smallest safe correction

No counter or contract correction is indicated by these controls. Do not replace the planned semantic audit with a file-length statistic. Implement the frozen per-leg, independent-oracle and harness-rejection checks in the real auditor, leaving the runner and frozen measurement inputs unchanged. This seat made no production correction.
