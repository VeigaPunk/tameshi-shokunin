Verdict: Expected control rejection observed. The committed junk control returned `C1_R32_PASS=false`; the counter exited 1 with `kill=4/18 accept=4/8 other=18`. No full-pass control finding occurred. Strict mutation-kill attribution is **inconclusive**, not killed: the pristine revision also failed because the audit tool did not exist.

## Evidence

Axis: **operability**, claim C1. This probe tests whether runner-independent random output satisfies the frozen counter. It does not assess the eventual real audit tool.

- Frozen predicate: `.ufo/evidence/round-32/contract.json:13-20`; required control expectation: line 33.
- Detector: `.ufo/evidence/round-32/c1-measure.py:177-196` classifies each invocation; lines 264-277 require every copy to be correct.
- Mutant: one new `tools/tally-audit.py`, committed only in `/fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane` as `f17cd55fca98e6fc140eb9f154a62631418358b8`, directly atop `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. Its lines 6-14 seed from `os.urandom`, shuffle both labels and random noise, and choose an independent exit code from 0, 1, 2. It never reads the runner.
- Exactly one counter run evaluated the junk revision. No `--seed` argument was supplied. Pristine and restored baseline runs are separately disclosed below; neither evaluates the junk revision again.

### Setup and the single sandbox commit

All shell commands ran with working directory `/fast/scratch/hyaku/tameshi-r32-seats/CtlJunk`.

```sh
df -h /fast && mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed output, exit 0:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  701G  103G  88% /fast
```

After writing the source below:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlJunk && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane rev-parse HEAD HEAD^ && sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/tally-audit.py /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/mutate-and-run.sh
```

Observed output, exit 0:

```text
f17cd55fca98e6fc140eb9f154a62631418358b8
c31814978969a41a8e9b0f7d99fa308c5993c1b7
35fc35280bba2fdc6bd245bb13cea6a34a69e4b944214610790ce4f4406d7239  /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/tally-audit.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/mutate-and-run.sh
```

### Full control source

The complete 346-byte source at sandbox commit `f17cd55fca98e6fc140eb9f154a62631418358b8:tools/tally-audit.py`:

```python
#!/usr/bin/env python3
"""Junk control: labels and exit status are independent of the runner."""
import os
import random

rng = random.Random(os.urandom(32))
lines = [
    "TALLY_AUDIT: PASS",
    "TALLY_AUDIT: FAIL",
    "noise: %032x" % rng.getrandbits(128),
]
rng.shuffle(lines)
print("\n".join(lines))
raise SystemExit(rng.choice((0, 1, 2)))
```

### Junk counter command and complete stdout

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/w-CtlJunk
```

Observed exit code: **1**. No stderr was observed. Full stdout, verbatim, also retained at `/fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/CtlJunk.stdout:1-27`:

```text
COPY set=kill id=T08 outcome=OTHER exit=2 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=OTHER exit=2 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=OTHER exit=2 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS'
COPY set=kill id=H05 outcome=OTHER exit=2 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: PASS'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS'
COPY set=kill id=D01 outcome=OTHER exit=2 sha256=71a66c5a611d408f last='TALLY_AUDIT: PASS'
COPY set=kill id=gT08(arm=83) outcome=KILL exit=1 sha256=515b7c481b468be9 last='TALLY_AUDIT: PASS'
COPY set=kill id=gN05(<= nlegs - 1) outcome=OTHER exit=2 sha256=7184b157539cad8c last='TALLY_AUDIT: PASS'
COPY set=kill id=gH03(form=2) outcome=KILL exit=1 sha256=7f1787411f0ff16c last='TALLY_AUDIT: PASS'
COPY set=kill id=gH04(rc=$?) outcome=OTHER exit=2 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=0,dup=6) outcome=ACCEPT exit=0 sha256=9f9e3feebe8d3b7e last='TALLY_AUDIT: PASS'
COPY set=kill id=gN01(vector=3) outcome=OTHER exit=2 sha256=c66c1ca66cf8ae0f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(true) outcome=ACCEPT exit=0 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_js,dup=st_tsu) outcome=OTHER exit=2 sha256=48bae77fd4a45c60 last='TALLY_AUDIT: PASS'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: FAIL'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B4-cosmetic outcome=OTHER exit=2 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB6-permuted outcome=KILL exit=1 sha256=4b83b0a25e141210 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=255e01a435438fec last='TALLY_AUDIT: FAIL'
C1_R32: kill=4/18 accept=4/8 other=18 runner_sha_ok=1 tool_present=1 seed=24da774111d05591 rev=f17cd55fca98e6fc140eb9f154a62631418358b8 C1_R32_PASS=false
```

Correct classifications happened on `N01`, `gT08(arm=83)`, `gH03(form=2)`, `gN03(or)`, `B0-pristine`, `B2-reversed`, `B3-decoys`, and `gB7-nonce`. The other 18 copies did not satisfy their required classification. The counter's `other` total includes incorrect classifications, not only lines with `outcome=OTHER` (`c1-measure.py:265-272`).

Both labels appear on every invocation, so label order cannot rescue a wrong exit code. The frozen counter checks any matching prefix plus the exit code, not consistency with the last label (`c1-measure.py:188-196`). This explains, for example, `B0-pristine` being ACCEPT with last label FAIL; it is not a full-pass finding or a request to change the predicate.

### Pristine and restored detector runs

Pristine command, before creating the control tool:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/w-pristine
```

Observed exit 1; full stdout is `/fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/pristine.stdout:1-27`. Every COPY had `outcome=OTHER exit=no-tool`. Final line:

```text
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=706e5e8a75d5c978 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

After the junk run, the edit tool removed only the newly created sandbox working-tree `tools/tally-audit.py`, restoring its original absence. The required sandbox commit remains retained at HEAD; no second commit, reset, or checkout was used for restoration. Because the frozen counter reads committed blobs rather than the working tree (`c1-measure.py:224,240-257`), the restoration run explicitly selects the original committed bytes:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane --rev c31814978969a41a8e9b0f7d99fa308c5993c1b7 --work /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/w-restored
```

Observed exit 1; full stdout is `/fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/restored.stdout:1-27`. Every COPY again had `outcome=OTHER exit=no-tool`. Final line:

```text
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=693c6663d9d8c23c rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Each run used its own initially absent work directory and a fresh counter-generated seed. No stderr was observed in any run. Exact commands, exit codes, revisions, seeds, and stdout paths are also recorded in `/fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/receipts.json`.

### Restoration and before/after hashes

The tool state was **absent → SHA-256 `35fc35280bba2fdc6bd245bb13cea6a34a69e4b944214610790ce4f4406d7239` → absent** in the sandbox working tree. The control's committed blob and counter-extracted copy remain available as evidence.

The following hashes were observed before creating the control and after restoring it, with identical values in production and the sandbox clone:

| File | SHA-256 before and after |
| --- | --- |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `.ufo/evidence/round-32/c1-measure.py` | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` |
| `.ufo/evidence/round-32/contract.json` | `7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583` |

Exact final restoration command:

```sh
test ! -e /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/tally-audit.py && printf 'Restored working-tree tools/tally-audit.py: absent\n' && sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/.ufo/evidence/round-32/c1-measure.py /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
```

Observed output, exit 0:

```text
Restored working-tree tools/tally-audit.py: absent
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /fast/scratch/hyaku/tameshi-r32-seats/CtlJunk/lane/.ufo/evidence/round-32/contract.json
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
```

No production source or frozen input was edited. All started commands completed; no process tree remains running from this probe. No tools were installed or updated. No other runtime, subagent, build, formatter, or regression suite was invoked.

## Smallest safe correction

None to the frozen counter or runner. Do not use this junk control as the audit implementation. Its observed rejection matches the assigned pre-data expectation; keep the frozen predicate unchanged.
