# Verdict

Expected negative control result: **C1_R32_PASS=false**, counter exit **1**. The text-keyed tool killed all 9 frozen copies and 2 generated copies, accepted all 8 required benign copies, and missed 7 generated defects. This control did not meet the frozen predicate.

Axis: **operability**. Preservation constraint: the runner remained byte-identical. This report does not judge or integrate the real implementation.

Sandbox commit: `83db799300f068477ee55ddbba898b424b02ceed`, one control commit on top of `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. Tool: `/fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/lane/tools/tally-audit.py`.

# Evidence

## Scope and detector

The frozen definition is `.ufo/evidence/round-32/contract.json:12-35`; frozen edit spellings are `.ufo/evidence/round-32/c1-measure.py:82-93`, generated variants are at `:96-137`, benign transformations at `:140-168`, and counting/output logic at `:264-277`.

The control matches exact non-comment source lines against the frozen edit spellings, not runner behavior. It ignores blank lines and full-line comments. H04 requires the exact comparison followed by `rc=$?`, because the legitimate pre-comparison capture already contains that line (`tools/mutate-and-run.sh:2004-2007`). N01 matches the two-line adjacency created by deletion of the mixed fail/setup vector (`tools/mutate-and-run.sh:2025-2027`). These contextual matches prevent a trivial false rejection of pristine bytes. There is no shell execution, oracle, status-name accounting, generated-family recognition, filename inspection, seed inspection, or hash lookup in this tool.

## Setup and sandbox commit

Commands executed:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlTextKeyed
```

Both commands exited 0 with no stdout. No production Git write command was run.

## Frozen counter, full stdout

One run only, without `--seed`, with a fresh absent work directory. Working directory: `/fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed`.

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlTextKeyed/w-CtlTextKeyed
```

Observed stdout, verbatim:

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL text-keyed control: matched T08'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL text-keyed control: matched N05'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL text-keyed control: matched H03'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL text-keyed control: matched H04'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL text-keyed control: matched H05'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL text-keyed control: matched N01'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL text-keyed control: matched N02'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL text-keyed control: matched N03'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL text-keyed control: matched D01'
COPY set=kill id=gT08(arm=60) outcome=ACCEPT exit=0 sha256=e219f8a5f3e428b1 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL text-keyed control: matched N05'
COPY set=kill id=gH03(form=2) outcome=ACCEPT exit=0 sha256=7f1787411f0ff16c last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=kill id=gH04(true) outcome=ACCEPT exit=0 sha256=eceff075da31e6d4 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=kill id=gH05(drop=3,dup=2) outcome=ACCEPT exit=0 sha256=5acba43d09b03e0e last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=kill id=gN01(vector=1) outcome=ACCEPT exit=0 sha256=ebf4a902638d568e last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=kill id=gN02(or) outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL text-keyed control: matched N02'
COPY set=kill id=gN03(split) outcome=ACCEPT exit=0 sha256=16566843890d60ab last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=kill id=gD01(drop=st_roundgate,dup=st_mado) outcome=ACCEPT exit=0 sha256=b3a19e03cfee609f last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=2efc0a91d2f9f7b6 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=2e1e6924a132af50 last='TALLY_AUDIT: PASS text-keyed control: no frozen edit matched'
C1_R32: kill=11/18 accept=8/8 other=7 runner_sha_ok=1 tool_present=1 seed=e07b47c7fe6efc03 rev=83db799300f068477ee55ddbba898b424b02ceed C1_R32_PASS=false
```

Counter exit code: **1**. Observed duration: 2.38 seconds. The seven `other` results are incorrect ACCEPTs of must-kill copies, not tool execution errors.

## Generated copies missed

| Copy | Why the frozen text matcher misses it | Counter source |
|---|---|---|
| `gT08(arm=60)` | Added pass arm is 60, not frozen arm 4. | `c1-measure.py:98-99` |
| `gH03(form=2)` | Prefix-only output comparison is not the frozen exit-only comparison. | `c1-measure.py:102-106` |
| `gH04(true)` | Comparison status is swallowed by `true`, not `rc=$?`. | `c1-measure.py:107-108` |
| `gH05(drop=3,dup=2)` | Singleton position list differs from the frozen drop-8/duplicate-7 list. | `c1-measure.py:109-113` |
| `gN01(vector=1)` | Deletes the two-setup vector, not the frozen mixed vector; the frozen adjacency is absent. | `c1-measure.py:114-123` |
| `gN03(split)` | Split comparisons joined by `||` differ from the frozen single-comparison `||` form. | `c1-measure.py:128-131` |
| `gD01(drop=st_roundgate,dup=st_mado)` | Different duplicated and dropped operands than the frozen loop. | `c1-measure.py:132-136` |

The two generated kills, `gN05(< nlegs)` and `gN02(or)`, choose the same text as their frozen counterparts. Their matching SHA-256 prefixes are visible in the receipt. All nine frozen copies were rejected, including contextual H04 and deletion N01. All eight benign copies were accepted, including comment decoys, operand reversal/permutation, cosmetic arm formatting, variable renaming, and nonce comments.

## One minimal mutation probe and exact restoration

Mutant: H04, insert one `    rc=$?` immediately after the exact comparison in an isolated `probe-runner.sh:2007`. This assignment masks the comparison's failure status. Expected detector: the control tool must PASS pristine bytes, FAIL this frozen text pattern with exit 1, then PASS exact restored bytes. The tool does not execute the runner, so this probe establishes text detection only.

Prepared inside the seat directory:

```sh
cp lane/tools/mutate-and-run.sh probe-runner.sh
```

The same bounded command was run at all three stages:

```sh
timeout 30 python3 lane/tools/tally-audit.py --runner probe-runner.sh
```

| Stage | Actual stdout | Exit | SHA-256 of `probe-runner.sh` |
|---|---|---|---|
| Pristine | `TALLY_AUDIT: PASS text-keyed control: no frozen edit matched` | 0 | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| H04 inserted | `TALLY_AUDIT: FAIL text-keyed control: matched H04` | 1 | `0dc1e6b07452f6108f9dd7f99050aa0d8b8450456c3424f22da1a7fc54e5d6cd` |
| Inserted line removed | `TALLY_AUDIT: PASS text-keyed control: no frozen edit matched` | 0 | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |

Probe verdict: **killed**, with a passing baseline and restored result. The insertion and removal used surgical edits only on the scratch probe. No lane or production runner was edited.

Hash commands before mutation and while mutated:

```sh
sha256sum probe-runner.sh lane/tools/tally-audit.py
sha256sum probe-runner.sh
```

Final restoration/preservation command, exit 0; `cmp` produced no output:

```sh
sha256sum probe-runner.sh lane/tools/mutate-and-run.sh lane/tools/tally-audit.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json && cmp probe-runner.sh lane/tools/mutate-and-run.sh
```

Observed stdout:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  probe-runner.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
6f926755f362c9281e140b7857df9562da0be53fa6aa4a485c2ead8638febb98  lane/tools/tally-audit.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
```

Counter and contract hashes match the values recorded before tool creation. The tool hash also matches its pre-probe value. All commands completed; no started process tree remains. No tools were installed or updated. `df -h /fast` reported 112G available before the small scratch work.

## Full control source

```python
#!/usr/bin/env python3
"""Pre-data text-keyed control: recognize only the nine frozen edit spellings.

This is deliberately not a behavioral tally audit. Full-line comments and blank
lines are ignored. H04 needs its comparison context because rc=$? is also valid
before that comparison; N01 is represented by the adjacency its deletion creates.
"""
import argparse
from pathlib import Path

CMP = '    [[ $rc -eq $want_rc && "${out%%$\'\\n\'*}" == "$want_line" ]]'
V22 = "    '2 2 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)' \\"
V30 = "    '3 0 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)'; do"

FROZEN_PATTERNS = (
    ('T08', ('      4) npass=$((npass + 1)) ;;',)),
    ('N05', ('  if (( npass + nfail + nsetup < nlegs )); then',)),
    ('H03', ('    [[ $rc -eq $want_rc ]]',)),
    ('H04', (CMP, '    rc=$?')),
    ('H05', ('    for ti in 0 1 2 3 4 5 6 7 7; do',)),
    ('N01', (V22, V30)),
    ('N02', ('  [[ "$tblock" != "$tblock_full" ]] ||',)),
    ('N03', (CMP.replace(' && ', ' || '),)),
    ('D01', ('  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_js"; do',)),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', required=True)
    args = parser.parse_args()
    try:
        text = Path(args.runner).read_text(encoding='utf-8')
    except (OSError, UnicodeError) as error:
        print('TALLY_AUDIT: ERROR text-keyed control: ' + str(error))
        return 2
    lines = [line for line in text.splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    for label, pattern in FROZEN_PATTERNS:
        size = len(pattern)
        if any(tuple(lines[i:i + size]) == pattern
               for i in range(len(lines) - size + 1)):
            print('TALLY_AUDIT: FAIL text-keyed control: matched ' + label)
            return 1
    print('TALLY_AUDIT: PASS text-keyed control: no frozen edit matched')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

# Smallest safe correction

No correction to the frozen counter or contract is warranted by this run. Keep this deliberately incomplete control sandbox-only. The real tool must audit the required per-leg, oracle, and harness behavior rather than recognize frozen spellings. No production implementation was changed.
