# CtlRuntimeOnly

**Verdict: expected negative control observed.** The unchanged frozen counter rejected the runtime-only control: `C1_R32_PASS=false`, exit **1**, `kill=6/18 accept=8/8 other=12`. The twelve harness-only defects survived this deliberately partial audit. The separate reversible T08 probe was **killed** after a passing pristine baseline; restoring the exact bytes restored the passing result.

Axis: **operability**. Bounds preserved: pinned runner bytes, frozen counter and contract, one sandbox commit, no production code edits. No score or admission claim is made.

## Evidence

- Frozen predicate and control expectation: `.ufo/evidence/round-32/contract.json:12-35`.
- Frozen copy construction: `.ufo/evidence/round-32/c1-measure.py:82-168`; result classification and predicate: lines 265-277.
- Sandbox tool: `/fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py:19` extracts only the runtime tally; line 36 defines its independent oracle; line 53 executes the extracted block with local status variables and `local root=x auto=0 KEEP=1`; lines 69-83 supply 256 first-leg statuses, 63 singleton-position probes, and two count stresses. Line 104 explicitly disclaims harness checking.
- Runner tally: `tools/mutate-and-run.sh:1432-1471`. The harness at lines 1989-2040 is neither executed nor checked by this control.
- Sandbox commit: **`fd11c84df30c7d1049cc69de139406f2f42d1243`**, directly on frozen commit `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. Its sole new file is `tools/tally-audit.py`.

### Setup and commit

Commands executed:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlRuntimeOnly && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane rev-parse HEAD
```

Setup exited 0 without output. Commit command exited 0 and printed:

```text
fd11c84df30c7d1049cc69de139406f2f42d1243
```

### Frozen counter run

Executed once, without `--seed`, from `/fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly`; the work directory was fresh:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/w-CtlRuntimeOnly
```

Exit code: **1**. Full stdout, verbatim (the counter itself truncates each `last` field to 160 characters):

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last="TALLY_AUDIT: FAIL runtime first-leg status=4 expected=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)') observed=(0, 'REGRESSION: PASS (cases=9 passed"
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last="TALLY_AUDIT: FAIL runtime overcount expected=(2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=10)') observed=(0, 'REGRESSION: PASS (cases=9 passed=1"
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=H04 outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=N01 outcome=ACCEPT exit=0 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last="TALLY_AUDIT: FAIL runtime first-leg status=1 expected=(1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)') observed=(1, 'REGRESSION: FAIL (cases=9 passed"
COPY set=kill id=gT08(arm=149) outcome=KILL exit=1 sha256=9f3137851942464e last="TALLY_AUDIT: FAIL runtime first-leg status=149 expected=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)') observed=(0, 'REGRESSION: PASS (cases=9 pass"
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last="TALLY_AUDIT: FAIL runtime overcount expected=(2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=10)') observed=(0, 'REGRESSION: PASS (cases=9 passed=1"
COPY set=kill id=gH03(form=1) outcome=ACCEPT exit=0 sha256=c307192c9c04517f last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=gH04(rc=$?) outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=gH05(drop=6,dup=7) outcome=ACCEPT exit=0 sha256=a77800f5a0aa0f57 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=gN01(vector=3) outcome=ACCEPT exit=0 sha256=c66c1ca66cf8ae0f last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=gN02(or) outcome=ACCEPT exit=0 sha256=31128639afc3e57a last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=gN03(or) outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=kill id=gD01(drop=st_tsu,dup=st_mado) outcome=KILL exit=1 sha256=c557f5cecb5bd9eb last="TALLY_AUDIT: FAIL runtime st_tsu status=1 expected=(1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)') observed=(0, 'REGRESSION: PASS (cases=9 passed=9;"
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=dbf5abafb33a05e3 last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=3094d5751bf5629f last='TALLY_AUDIT: PASS runtime-only checks=321; harness not checked'
C1_R32: kill=6/18 accept=8/8 other=12 runner_sha_ok=1 tool_present=1 seed=64e2c886c11cf165 rev=fd11c84df30c7d1049cc69de139406f2f42d1243 C1_R32_PASS=false
```

It got T08, N05, D01 and their generated variants right: nonzero-as-pass arms contradict the exhaustive first-leg oracle; the undercount-only guard misses the ten-operand stress; singleton probes expose replaced operands even when the total remains nine. All eight must-accept copies were accepted. H03, H04, H05, N01, N02, N03 and their generated variants only damage the unexamined selftest harness, so all twelve survived. This is the intended partial-work coverage gap, not a counter pass or permission to weaken the contract.

### Full control source

`/fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py`, SHA-256 `62155cfa5bd7885f2957f94622f522cb7015da96cdeae9f3690a88030a2b3731`:

```python
#!/usr/bin/env python3
"""Round 32 pre-data control: execute the tally, never test its selftest harness."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys


NAMES = (
    'st_js', 'st_kagi', 'st_tsu', 'st_mado', 'st_checklist',
    'st_claims', 'st_roundgate', 'st_sourcescheck', 'st_citecheck',
)
START = '  local nlegs=9 npass=0 nfail=0 nsetup=0 st'


def extract(text):
    lines = text.splitlines()
    begin = lines.index('run_regression() {')
    end = lines.index('}', begin + 1)
    start = lines.index(START, begin + 1, end)
    block = '\n'.join(lines[start:end]) + '\n'
    loops = [line for line in lines[start:end] if line.startswith('  for st in ')]
    if len(loops) != 1:
        raise ValueError('cannot identify one tally loop')
    loop = loops[0]
    match = re.fullmatch(r'  for st in ((?:"\$[A-Za-z_]\w*" ?)+); do', loop)
    if match is None:
        raise ValueError('cannot extract tally operands')
    operands = re.findall(r'"\$[A-Za-z_]\w*"', match.group(1))
    return block, loop, operands


def oracle(statuses):
    passed = statuses.count(0)
    failed = statuses.count(1)
    setup = len(statuses) - passed - failed
    if failed:
        return 1, ('REGRESSION: FAIL (cases=9 passed=%d failed=%d setup=%d)'
                   % (passed, failed, setup))
    if setup:
        return 2, ('REGRESSION: SETUP (cases=9 passed=%d cannot-verify=%d)'
                   % (passed, setup))
    if len(statuses) != 9:
        return 2, ('REGRESSION: SETUP (case-tally mismatch: cases=9 counted=%d)'
                   % len(statuses))
    return 0, ('REGRESSION: PASS (cases=9 passed=9; ledger legs exact: '
               'killed-delta<=0 flips<=0)')


def run_block(block, statuses):
    declarations = '  local root=x auto=0 KEEP=1\n'
    declarations += ''.join('  local %s=%d\n' % pair for pair in zip(NAMES, statuses))
    script = 'probe() {\n' + declarations + block + '}\nprobe\n'
    env = {
        'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
        'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
    }
    result = subprocess.run(
        ['bash', '--noprofile', '--norc'], input=script, text=True,
        capture_output=True, timeout=3, env=env,
    )
    lines = result.stdout.splitlines()
    return result.returncode, lines[0] if lines else ''


def cases(block, loop, operands):
    for status in range(256):
        values = [status] + [0] * 8
        yield 'first-leg status=%d' % status, block, values, values
    for position, name in enumerate(NAMES):
        for status in (1, 2, 3, 4, 126, 127, 255):
            values = [0] * 9
            values[position] = status
            yield '%s status=%d' % (name, status), block, values, values
    for label, changed in (
        ('overcount', operands + operands[-1:]),
        ('undercount', operands[:-1]),
    ):
        replacement = '  for st in ' + ' '.join(changed) + '; do'
        yield label, block.replace(loop, replacement, 1), [0] * 9, [0] * len(changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', required=True, type=Path)
    args = parser.parse_args()
    try:
        block, loop, operands = extract(args.runner.read_text(encoding='utf-8'))
        checked = 0
        for label, candidate, inputs, effective in cases(block, loop, operands):
            expected = oracle(effective)
            observed = run_block(candidate, inputs)
            checked += 1
            if observed != expected:
                print('TALLY_AUDIT: FAIL runtime %s expected=%r observed=%r'
                      % (label, expected, observed))
                return 1
    except (OSError, UnicodeError, ValueError, subprocess.TimeoutExpired) as error:
        print('TALLY_AUDIT: ERROR cannot audit: %s' % error)
        return 2
    print('TALLY_AUDIT: PASS runtime-only checks=%d; harness not checked' % checked)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

### Reversible mutation probe

Mutant: insert exactly `      4) npass=$((npass + 1)) ;;` immediately after the exit-1 case arm in the isolated `/fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh:1437`. This is T08, one behavior-bearing case arm. The production runner and the clone's runner were not edited.

Expected detector: the same runtime-only tool must accept pristine bytes, fail on status 4 being counted as a pass (expected SETUP/2, observed PASS/0), then accept the byte-restored file.

Preparation executed, exit 0:

```sh
cp /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh && sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
```

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
```

Pristine detector command, exit 0:

```sh
timeout 60 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
```

```text
TALLY_AUDIT: PASS runtime-only checks=321; harness not checked
```

After the one-line insertion, executed, exit 1:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh && timeout 60 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
```

```text
12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b  /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
TALLY_AUDIT: FAIL runtime first-leg status=4 expected=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)') observed=(0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
```

The inserted line was removed with a surgical edit. Restoration command, exit 0; `cmp` was silent and successful:

```sh
cmp /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/mutate-and-run.sh && sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json && timeout 60 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
```

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/probe-runner.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/mutate-and-run.sh
62155cfa5bd7885f2957f94622f522cb7015da96cdeae9f3690a88030a2b3731  /fast/scratch/hyaku/tameshi-r32-seats/CtlRuntimeOnly/lane/tools/tally-audit.py
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
TALLY_AUDIT: PASS runtime-only checks=321; harness not checked
```

The pristine, mutated and restored SHA-256 sequence is `a7d3f2dd…2eb9` → `12ad1d90…27b` → `a7d3f2dd…2eb9`. Verdict: **killed**, not inconclusive. The frozen counter and contract hashes above match their pristine sandbox copies recorded before tool creation. All started commands completed; no service or long-lived process was launched. No tools were installed or updated. No subagent was dispatched.

## Smallest safe correction

Do not change the frozen counter, runner, or this deliberately partial control. The real audit must include the already-planned independent tests of the runner's selftest harness against known-faulty tally blocks; runtime checks alone cannot detect the twelve surviving harness defects. No correction was integrated by this seat.
