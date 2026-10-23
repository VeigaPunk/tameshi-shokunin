# CtlStaticOnly

Verdict: the partial-work control did not satisfy C1, as expected. The frozen counter exited 1 with `kill=2/18 accept=8/8 other=16 C1_R32_PASS=false`. Only D01 and generated gD01 were killed. All sixteen runtime or harness defects survived, and all eight must-accept copies were accepted. This control produced no counter-bypass finding.

The separate single-point T08 mutation probe **survived** the static-only detector: pristine, mutated, and exactly restored bytes all produced PASS with exit 0. This is a coverage finding for the deliberately partial detector, not an inconclusive baseline or a contract change.

## Axes and scope

- Operability: distinguish defective runner copies from accepted equivalents through the required command interface.
- Preservation: leave the pinned runner, frozen counter, and frozen contract unchanged.

The control only compares the multisets of standalone `st_*=$?` assignments and quoted status-variable operands inside `run_regression`, and checks that `nlegs` equals the assignment count. It does not execute the runner or inspect tally-arm behavior or the selftest harness.

## Evidence

- Frozen contract: `.ufo/evidence/round-32/contract.json:12-20` defines the three audit components and the fixed predicate; lines 23-33 define the copy families and negative controls.
- Frozen detector: `.ufo/evidence/round-32/c1-measure.py:177-196` classifies tool outputs; lines 264-277 determine the final result.
- Control: `/fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/tally-audit.py:16-32` isolates `run_regression`, extracts assignments and tally operands, and performs only the static multiset/count comparison.
- Runner: `/fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/mutate-and-run.sh:1390-1433` contains the nine status assignments, `nlegs=9`, and the tally-loop operands.

### Sandbox setup and commit

The sources named in the assignment were read before setup. Initial disk observation from `df -h /fast`:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  691G  113G  87% /fast
```

The assigned directory was created with Python `Path.mkdir(parents=True, exist_ok=True)`. The following commands ran from `/fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly` and exited 0 with no stdout:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

After writing only the control tool in the clone, one sandbox commit was made:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlStaticOnly
```

This command exited 0 with no stdout. The counter resolved the resulting revision as `fb8f36dd5eda81886010e22d202175f83c96679e`.

### Frozen counter command and full stdout

Exactly one full counter run was performed, using the fresh work directory below and no `--seed`:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/w-CtlStaticOnly
```

Full stdout, verbatim:

```text
COPY set=kill id=T08 outcome=ACCEPT exit=0 sha256=12ad1d9076a55050 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=N05 outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=H04 outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=N01 outcome=ACCEPT exit=0 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL static per-leg presence'
COPY set=kill id=gT08(arm=118) outcome=ACCEPT exit=0 sha256=f79a0ba38a11d698 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gN05(< nlegs) outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gH03(form=2) outcome=ACCEPT exit=0 sha256=7f1787411f0ff16c last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gH04(rc=$?) outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gH05(drop=6,dup=0) outcome=ACCEPT exit=0 sha256=9a19d5dfd232ee8d last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gN01(vector=1) outcome=ACCEPT exit=0 sha256=ebf4a902638d568e last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gN02(true) outcome=ACCEPT exit=0 sha256=29d0e2b6649efed2 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gN03(split) outcome=ACCEPT exit=0 sha256=16566843890d60ab last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=kill id=gD01(drop=st_checklist,dup=st_mado) outcome=KILL exit=1 sha256=a3bfa92a1a4287b7 last='TALLY_AUDIT: FAIL static per-leg presence'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=547a74def6a85e8b last='TALLY_AUDIT: PASS static per-leg presence'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=dabb3f6922720174 last='TALLY_AUDIT: PASS static per-leg presence'
C1_R32: kill=2/18 accept=8/8 other=16 runner_sha_ok=1 tool_present=1 seed=2bd6ca13e5c232a5 rev=fb8f36dd5eda81886010e22d202175f83c96679e C1_R32_PASS=false
```

Exit code: **1**. No stderr was shown.

### One isolated mutation and exact restoration

Mutant: T08, a single added tally arm counting exit status 4 as a pass instead of setup. The added line was inserted only in `/fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/runner-probe.sh:1437`:

```sh
      4) npass=$((npass + 1)) ;;
```

Expected detector behavior for the complete C1 audit: PASS/0 on pristine and restored bytes; FAIL/1 on this known-faulty runner. The partial static-only detector was expected to miss it because neither the assignment multiset, tally operand multiset, nor `nlegs` changed.

The same bounded detector command was used at all three stages:

```sh
timeout 30 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/runner-probe.sh
```

Pristine command:

```sh
cp -- lane/tools/mutate-and-run.sh runner-probe.sh && sha256sum runner-probe.sh && timeout 30 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/runner-probe.sh
```

Observed stdout; exit 0:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  runner-probe.sh
TALLY_AUDIT: PASS static per-leg presence
```

The editor inserted the single arm after line 1436. Mutated command:

```sh
sha256sum runner-probe.sh && timeout 30 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/runner-probe.sh
```

Observed stdout; exit 0:

```text
12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b  runner-probe.sh
TALLY_AUDIT: PASS static per-leg presence
```

The editor then deleted exactly the inserted line 1437. Restored command:

```sh
sha256sum runner-probe.sh lane/tools/mutate-and-run.sh lane/tools/tally-audit.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json && cmp -s -- runner-probe.sh lane/tools/mutate-and-run.sh && printf 'restoration_cmp=exact\n' && timeout 30 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/runner-probe.sh
```

Observed stdout; exit 0:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  runner-probe.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
6737909570dcdf3d0cef8b3a5965e193a54006045ef6f2aaccc7c1f915306520  lane/tools/tally-audit.py
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
restoration_cmp=exact
TALLY_AUDIT: PASS static per-leg presence
```

The counter and contract hashes above exactly match their independently recorded pre-run hashes. The restored probe hash exactly matches the pre-mutation hash, and `cmp -s` confirmed byte equality with the unchanged sandbox runner. No production runner was edited. All started commands completed; no background process was launched.

### Full control tool source

Path: `/fast/scratch/hyaku/tameshi-r32-seats/CtlStaticOnly/lane/tools/tally-audit.py`.

SHA-256: `6737909570dcdf3d0cef8b3a5965e193a54006045ef6f2aaccc7c1f915306520`.

```python
#!/usr/bin/env python3
"""Pre-data control: audit static per-leg tally presence only."""

import argparse
from collections import Counter
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', required=True)
    args = parser.parse_args()
    try:
        text = Path(args.runner).read_text(encoding='utf-8')
        bodies = re.findall(
            r'(?ms)^run_regression\(\)[ \t]*\{[^\n]*\n(.*?)^\}', text)
        if len(bodies) != 1:
            raise ValueError('cannot isolate run_regression')
        body = bodies[0]
        legs = re.findall(
            r'(?m)^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*(?:#.*)?$', body)
        loops = re.findall(
            r'(?m)^[ \t]*for[ \t]+st[ \t]+in[ \t]+(.*?);[ \t]*do[ \t]*(?:#.*)?$',
            body)
        counts = re.findall(
            r'(?m)^[ \t]*local[ \t]+nlegs=([0-9]+)(?:[ \t]|$)', body)
        if not legs or len(loops) != 1 or len(counts) != 1:
            raise ValueError('cannot isolate leg assignments, tally loop, or nlegs')
        operands = re.findall(r'"\$(st_[A-Za-z0-9_]+)"', loops[0])
        if Counter(legs) != Counter(operands) or int(counts[0]) != len(legs):
            print('TALLY_AUDIT: FAIL static per-leg presence')
            return 1
    except (OSError, UnicodeError, ValueError) as error:
        print('TALLY_AUDIT: ERROR ' + str(error))
        return 2
    print('TALLY_AUDIT: PASS static per-leg presence')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

Tools installed or updated: none.

## Smallest safe correction

Keep this negative control unchanged. The real auditor must add the independent tally oracle over exit statuses 0-255 with count stress, and the selftest fault-panel checks, alongside the static comparison. Do not change the frozen predicate, counter, accepted-copy set, or pinned runner to accommodate the surviving defects.
