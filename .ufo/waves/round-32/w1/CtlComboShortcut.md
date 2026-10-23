# CtlComboShortcut

## Verdict

**KILLED negative control: expected rejection.** The frozen counter printed `C1_R32_PASS=false`, exited **1**, killed **13/18** must-kill copies, and accepted **8/8** must-accept copies. Five must-kill copies survived as ACCEPT; none returned OTHER. The summary's `other=5` counts those wrong ACCEPT outcomes, not five tool errors (counter lines 264–277).

Axes: **operability** is measured; **calibration** is protected by reporting the five misses without extrapolating. Runner byte preservation is the no-harm constraint. This is a pre-data control result, not a judgment on the unwritten real auditor.

The control substitutes static leg multiplicity/nlegs checks, a frozen SHA-256 rejection table, and exact frozen active-text signatures for behavioral auditing. It never executes the runner, its tally block, or its selftest harness.

## Evidence

All relative sandbox paths below are under `/fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/`. Only this scratch directory and this assigned report were written. No sibling scratch directory was opened; no subagent was dispatched.

The counter and contract were opened first. Relevant frozen definitions:

- `.ufo/evidence/round-32/contract.json:11-35`: operability surface, immutable predicate, all kill/accept families, and expected control rejection.
- `.ufo/evidence/round-32/c1-measure.py:82-93`: nine frozen must-kill recipes; `:96-137`: generated variants; `:140-168`: accept variants; `:177-196`: outcome classification; `:240-277`: committed-tool extraction and final predicate.
- `.ufo/evidence/round-32/before/mutant-fidelity.txt:1-12`: pinned runner and eight frozen mutant hashes. D01's full hash was computed from the pinned runner's exact duplicated-operand replacement, without executing Bash.
- `lane/tools/mutate-and-run.sh:1385-1433`: nine captured leg statuses and tally operands; `:1434-1438`: tally case arms; `:1998-2040`: harness comparison, positions, vectors, and stress.
- Measured committed source: `w-CtlComboShortcut/tool/tally-audit.py:10-36` (frozen tables), `:55-73` (comment filtering/static check), `:75-82` (hash/text decisions). Full source is reproduced below.

### Setup and single sandbox commit

The first setup attempt could not start because its requested working directory did not yet exist; it made no changes. A small manifest created the permitted scratch directory, then the setup below succeeded. The setup-only manifest was removed before completion.

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed setup output: empty.

Static behavior was coordinated by a short message with `TameshiR32.CtlStaticOnly`: extract standalone `st_*=$?` assignments within `run_regression`, compare their Counter to the tally operands, and compare integer nlegs to the assignment count. The combined control retains this check, then adds the two frozen-signature mechanisms requested here. Comment-only lines are discarded before text matching, so the B3 decoys do not reject.

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlComboShortcut && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/lane rev-parse HEAD
```

Observed output, exit 0:

```text
6162637468aed0dcec961a94a28f6f0e464e88d1
```

Exactly one sandbox commit was made on the assigned frozen base, carrying only `tools/tally-audit.py`. No production Git write command, jj command, push, or production source edit was performed.

### Frozen counter command and full stdout

This was the only full counter run; `--work` was absent beforehand and no `--seed` was supplied. Raw receipts: `counter.stdout`, `counter.stderr` (empty), and `counter.exit` (`1`).

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlComboShortcut/w-CtlComboShortcut
```

Full stdout, verbatim:

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL frozen hash T08'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL frozen hash N05'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL frozen hash H03'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL frozen hash H04'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL frozen hash H05'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL frozen hash N01'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL frozen hash N02'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL frozen hash N03'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL static leg multiplicity or nlegs mismatch'
COPY set=kill id=gT08(arm=78) outcome=ACCEPT exit=0 sha256=7f36cc455a94b6b0 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL frozen hash N05'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL frozen hash H03'
COPY set=kill id=gH04(true) outcome=ACCEPT exit=0 sha256=eceff075da31e6d4 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=kill id=gH05(drop=4,dup=3) outcome=ACCEPT exit=0 sha256=bb24d5e8128bd3e2 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=kill id=gN01(vector=3) outcome=ACCEPT exit=0 sha256=c66c1ca66cf8ae0f last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=kill id=gN02(or) outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL frozen hash N02'
COPY set=kill id=gN03(split) outcome=ACCEPT exit=0 sha256=16566843890d60ab last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=kill id=gD01(drop=st_mado,dup=st_tsu) outcome=KILL exit=1 sha256=6ba0d4e0cb3d2cd1 last='TALLY_AUDIT: FAIL static leg multiplicity or nlegs mismatch'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=72bab6b5ff910cc6 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=1d80480386522545 last='TALLY_AUDIT: PASS static legs and frozen signatures only'
C1_R32: kill=13/18 accept=8/8 other=5 runner_sha_ok=1 tool_present=1 seed=b5197ba6f10320ef rev=6162637468aed0dcec961a94a28f6f0e464e88d1 C1_R32_PASS=false
```

**Counter exit code: 1. Stderr: empty.**

### Copies missed and why

| Must-kill copy incorrectly accepted | Defect | Why this shortcut missed it |
| --- | --- | --- |
| `gT08(arm=78)` | Exit 78 counted as pass | Frozen signature and hash cover exit 4, not exit 78. |
| `gH04(true)` | Appended `true` swallows comparison failure | Frozen signature and hash cover appended `rc=$?`, not `true`. |
| `gH05(drop=4,dup=3)` | Singleton position 4 omitted, position 3 duplicated | Frozen signature covers omitting 8 and duplicating 7. Static leg parsing does not inspect harness position coverage. |
| `gN01(vector=3)` | Unknown-status-3 multi-status vector deleted | Frozen N01 removes the mixed 1/2 vector, yielding a different active-text adjacency and hash. |
| `gN03(split)` | Separate exit/line comparisons joined with OR | Frozen N03 uses OR inside one `[[ ... ]]`; the whole-line signatures do not match the split form. |

Correct must-kill results were all nine frozen copies plus `gN05(< nlegs)`, `gH03(form=0)`, `gN02(or)`, and `gD01(drop=st_mado,dup=st_tsu)`. The first three generated successes are byte-identical to frozen N05, H03, and N02 respectively; their receipts explicitly say `frozen hash`. D01 and generated D01 were rejected by static leg multiplicity. No generated kill in this draw independently exercised the text matcher.

Every must-accept copy was accepted: pristine, equivalent T07 guard, reversed operands, comment decoys, cosmetic pass arm, renamed harness variable, generated operand permutation, and generated nonce comments. There was no false rejection in this draw. This observed false result does not establish that all possible seeds reject this control.

### One bounded pristine / mutated / restored probe

The isolated `probe.sh` began as the exact pinned runner bytes. The only mutation inserted `4) npass=$((npass + 1)) ;;` immediately after the exit-1 arm, at mutated `probe.sh:1437`. This is the frozen T08 behavior-bearing point. Expected detector result: pristine PASS/0, mutant FAIL/1, restored PASS/0.

The same command was run for all three states, from the seat directory:

```sh
sha256sum probe.sh && timeout 15 python3 lane/tools/tally-audit.py --runner probe.sh
```

Pristine stdout, exit 0:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  probe.sh
TALLY_AUDIT: PASS static legs and frozen signatures only
```

Mutated stdout, exit 1:

```text
12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b  probe.sh
TALLY_AUDIT: FAIL frozen hash T08
```

The inserted line was removed with a surgical edit. Restored stdout, exit 0:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  probe.sh
TALLY_AUDIT: PASS static legs and frozen signatures only
```

**Probe verdict: killed, not inconclusive.** Baseline passed. The before/restored SHA-256 values are identical; the restored probe remains available. The sandbox runner itself was never mutated.

### Preservation hashes

Before scoring, this command was run from the seat directory:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh lane/.ufo/evidence/round-32/c1-measure.py lane/.ufo/evidence/round-32/contract.json lane/tools/mutate-and-run.sh
```

Observed stdout:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  lane/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  lane/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
```

After scoring and restoring the probe, the same command with these two final arguments was run:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh lane/.ufo/evidence/round-32/c1-measure.py lane/.ufo/evidence/round-32/contract.json lane/tools/mutate-and-run.sh lane/tools/tally-audit.py w-CtlComboShortcut/tool/tally-audit.py
```

Observed stdout:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  lane/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  lane/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
87ee699c88cf37056ab92eca1b290446afd92466a727f83f9b37e49d6d4acefc  lane/tools/tally-audit.py
87ee699c88cf37056ab92eca1b290446afd92466a727f83f9b37e49d6d4acefc  w-CtlComboShortcut/tool/tally-audit.py
```

Both hash commands exited 0. The frozen counter, frozen contract, and production/sandbox runners retained identical before/after hashes. All commands returned; no long-lived process or service was started, and no process kill was needed. No tools were installed or updated.

## Smallest safe correction

Do not change the frozen counter, contract, target, or runner. Keep the static leg/nlegs check, but replace frozen text/hash recognition with the intended independent exit-status tally oracle and harness fault-injection checks. The five concrete survivors show why recognizing frozen exemplars is not behavioral auditing. This recommendation was not implemented: the assigned control stops after this probe.

## Full control source

Committed `lane/tools/tally-audit.py`, reproduced from the frozen counter's extracted committed tool:

```python
#!/usr/bin/env python3
"""Negative control: static leg checks plus frozen text and hash signatures only."""
import argparse
from collections import Counter
import hashlib
from pathlib import Path
import re


FROZEN_BAD_SHA = {
    '12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b': 'T08',
    'e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe': 'N05',
    '2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c': 'H03',
    '0dc1e6b07452f6108f9dd7f99050aa0d8b8450456c3424f22da1a7fc54e5d6cd': 'H04',
    'adf6763d6524f342b5496ff52f0fce96e0b4a00b5ab26cfa43be2001654b36d0': 'H05',
    'c0a32ec4e69d3cb07a7949efb7c9a83ac2b4b431f6e4da3f8bd76a1cd0d4cb34': 'N01',
    '31128639afc3e57a0d68f0abe94cc5038954ff41d6f9949da4fa903331f56250': 'N02',
    '741907e82ca7e907881cb985b7a504771de78d14b1179530661066a8f22a5b6f': 'N03',
    '71a66c5a611d408fe08c3618a18f30fe6d4e43308e36ee1f074420547c4f695c': 'D01',
}

# Exact active-line signatures of the frozen mutations, not a Bash interpreter.
# N01 is the new adjacency left when the frozen mixed-status vector is deleted.
FROZEN_BAD_TEXT = {
    'T08': r'4) npass=$((npass + 1)) ;;',
    'N05': r'if (( npass + nfail + nsetup < nlegs )); then',
    'H03': r'[[ $rc -eq $want_rc ]]',
    'H04': r'''[[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
rc=$?''',
    'H05': r'for ti in 0 1 2 3 4 5 6 7 7; do',
    'N01': r''''2 2 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)' \
'3 0 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)'; do''',
    'N02': r'[[ "$tblock" != "$tblock_full" ]] ||',
    'N03': r'''[[ $rc -eq $want_rc || "${out%%$'\n'*}" == "$want_line" ]]''',
    'D01': r'for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_js"; do',
}


def result(passed, reason):
    print('TALLY_AUDIT: ' + ('PASS ' if passed else 'FAIL ') + reason)
    return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', required=True)
    args = parser.parse_args()
    try:
        data = Path(args.runner).read_bytes()
        text = data.decode('utf-8')
    except (OSError, UnicodeError) as exc:
        print('TALLY_AUDIT: CANNOT_AUDIT ' + str(exc))
        return 2

    # A comment-only decoy is not executable source and must not trigger a match.
    code = '\n'.join(line for line in text.splitlines()
                     if not line.lstrip().startswith('#'))
    function = re.search(r'^run_regression\(\) \{\n(.*?)^\}', code, re.M | re.S)
    if function is None:
        print('TALLY_AUDIT: CANNOT_AUDIT missing run_regression')
        return 2
    block = function.group(1)
    assigned = re.findall(r'^\s*(st_[a-z_]+)=\$\?\s*$', block, re.M)
    loops = re.findall(r'^ *for st in (.*); do$', block, re.M)
    nlegs = re.findall(r'^ *local nlegs=([0-9]+)(?: |$)', block, re.M)
    if not assigned or len(loops) != 1 or len(nlegs) != 1:
        print('TALLY_AUDIT: CANNOT_AUDIT missing static anchors')
        return 2
    operands = re.findall(r'"\$(st_[a-z_]+)"', loops[0])
    counts = Counter(assigned)
    if (any(count != 1 for count in counts.values())
            or counts != Counter(operands) or int(nlegs[0]) != len(assigned)):
        return result(False, 'static leg multiplicity or nlegs mismatch')

    known = FROZEN_BAD_SHA.get(hashlib.sha256(data).hexdigest())
    if known is not None:
        return result(False, 'frozen hash ' + known)
    active_lines = '\n'.join(line.strip() for line in code.splitlines())
    for label, signature in FROZEN_BAD_TEXT.items():
        if '\n' + signature + '\n' in '\n' + active_lines + '\n':
            return result(False, 'frozen text ' + label)
    return result(True, 'static legs and frozen signatures only')


if __name__ == '__main__':
    raise SystemExit(main())
```
