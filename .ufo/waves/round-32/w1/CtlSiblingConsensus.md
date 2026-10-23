# CtlSiblingConsensus — round 32, wave 1

## Verdict

**The sibling consensus control did not meet the frozen counter.** The one unseeded counter run exited **1**, with `kill=18/18 accept=3/8 other=5` and `C1_R32_PASS=false`. Reading siblings exposed enough common text to reject every must-kill copy, but exact non-comment text comparison also rejected five required benign variants. This is not a finding that the control meets C1, nor a conclusion about every possible sibling-reading tool.

Axis: **operability**. The control, frozen counter, and bounded pristine/mutated/restored probe all ran. No other axis improvement is claimed.

## Evidence and scope

- Frozen contract: `.ufo/evidence/round-32/contract.json:12-20` defines the surface and exact predicate; `:23-26` lists both copy classes.
- Sibling visibility: `.ufo/evidence/round-32/c1-measure.py:243-250` writes all 26 copies to the same `copies` directory before any tool invocation. `:177-184` changes environment and working directory, but does not isolate the input directory. `:258-263` starts the tool calls only after every copy exists.
- Classification and final predicate: `.ufo/evidence/round-32/c1-measure.py:265-277`.
- Tool: `/fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane/tools/tally-audit.py`, full source below.
- Exactly one sandbox commit: `c65bf0b3769723d2e30efdcd1ffe0e910cc734d7`, on detached base `c31814978969a41a8e9b0f7d99fa308c5993c1b7`.
- Full receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/counter.stdout`, `counter.stderr`, `counter.exit`, and `mutation-probe.stdout`.
- All code ran with working directory `/fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus`. No production source, frozen counter, contract, or runner was edited. No tools were installed or upgraded. All started commands completed; no background process remains from this probe.

The control reads every regular file in the runner's parent directory, including the candidate itself. It discards blank lines and comment-only lines before aligning source lines, preserves indentation and inline comments, and takes a strict majority at each remaining line position. Missing trailing positions vote as absent. A missing strict majority gives exit 2. Any non-comment source difference from the reconstructed majority gives FAIL. It neither executes the runner nor checks tally semantics.

### Setup and commit commands

The setup script ran the following commands, exiting successfully with no stdout:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

After writing the tool, the exact commit command was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlSiblingConsensus && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane rev-parse HEAD
```

Observed stdout:

```text
c65bf0b3769723d2e30efdcd1ffe0e910cc734d7
```

### Frozen counter command and full stdout

`python3 score.py` invoked exactly the command below once, captured its stdout/stderr without modification, and recorded its return code. No `--seed` was supplied; the work directory was fresh and absent before this run.

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/w-CtlSiblingConsensus
```

Full counter stdout, verbatim:

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gT08(arm=30) outcome=KILL exit=1 sha256=fe36ad42615b3f14 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gN05(< nlegs) outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gH03(form=2) outcome=KILL exit=1 sha256=7f1787411f0ff16c last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gH04(rc=$?) outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gH05(drop=4,dup=5) outcome=KILL exit=1 sha256=4903e55b6ad2322b last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gN01(vector=2) outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gN02(or) outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gN03(split) outcome=KILL exit=1 sha256=16566843890d60ab last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=kill id=gD01(drop=st_js,dup=st_checklist) outcome=KILL exit=1 sha256=8245c8b1d0151fd1 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS (non-comment lines match sibling majority)'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=accept id=B2-reversed outcome=KILL exit=1 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS (non-comment lines match sibling majority)'
COPY set=accept id=B4-cosmetic outcome=KILL exit=1 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=accept id=gB6-permuted outcome=KILL exit=1 sha256=e131e79e2d1c36f6 last='TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=011aeddd1c003ee3 last='TALLY_AUDIT: PASS (non-comment lines match sibling majority)'
C1_R32: kill=18/18 accept=3/8 other=5 runner_sha_ok=1 tool_present=1 seed=50b24410ec5b30f4 rev=c65bf0b3769723d2e30efdcd1ffe0e910cc734d7 C1_R32_PASS=false
```

Counter exit code: **1**. Counter stderr: empty. The receipt wrapper additionally printed `COUNTER_EXIT: 1`; that wrapper line is not part of counter stdout.

Correct copies: all nine frozen and all nine generated must-kill copies, plus `B0-pristine`, `B3-decoys`, and `gB7-nonce`. Incorrect copies: `B1-T07`, `B2-reversed`, `B4-cosmetic`, `B5-renamed`, and `gB6-permuted`, all false rejections. Their source differences are explicitly permitted by `.ufo/evidence/round-32/c1-measure.py:140-168`. The counter's `other=5` counts incorrect required outcomes; these five tool invocations themselves returned KILL, not OTHER.

## Full control tool source

```python
#!/usr/bin/env python3
"""Pre-data control: compare non-comment source lines with sibling consensus."""
import argparse
from collections import Counter
from itertools import zip_longest
from pathlib import Path


def code_lines(path):
    return tuple(
        line for line in path.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.lstrip().startswith('#')
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', required=True, type=Path)
    runner = parser.parse_args().runner
    try:
        siblings = sorted(path for path in runner.parent.iterdir() if path.is_file())
        texts = [code_lines(path) for path in siblings]
        if not texts:
            print('TALLY_AUDIT: CANNOT AUDIT (no sibling files)')
            return 2
        majority = []
        for column in zip_longest(*texts, fillvalue=None):
            line, count = Counter(column).most_common(1)[0]
            if count * 2 <= len(texts):
                print('TALLY_AUDIT: CANNOT AUDIT (no strict line majority)')
                return 2
            if line is not None:
                majority.append(line)
        different = code_lines(runner) != tuple(majority)
    except (OSError, UnicodeError) as error:
        print('TALLY_AUDIT: CANNOT AUDIT (' + str(error) + ')')
        return 2
    if different:
        print('TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)')
        return 1
    print('TALLY_AUDIT: PASS (non-comment lines match sibling majority)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## One bounded mutation and exact restoration

Mutant: **T08**, insert `      4) npass=$((npass + 1)) ;;` immediately after the one `1) nfail=$((nfail + 1)) ;;` arm at `lane/tools/mutate-and-run.sh:1436`, but only in the isolated `mutation-probe-copies/target.sh`. This makes exit 4 count as pass instead of setup. Three other files in that probe directory retained pristine runner bytes throughout.

Expected detector: the same control command must return PASS/0 on pristine, FAIL/1 on the T08 target, then PASS/0 after restoring the exact original bytes. This is a separate bounded restoration probe, not another counter run or another mutation family. The command `timeout 90 python3 mutation-probe.py` exited 0; each detector call below had its own 15-second bound. The probe restored the target in a `finally` block.

Actual complete probe stdout:

```text
source_before_sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
tool_sha256=183c77a8ffacd7219547a04c73d26209627f318f80a26794a8e2f24392bb20c4
PRISTINE sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 expected_exit=0 exit=0
command: timeout 15 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/mutation-probe-copies/target.sh
TALLY_AUDIT: PASS (non-comment lines match sibling majority)
MUTATED_T08 sha256=12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b expected_exit=1 exit=1
command: timeout 15 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/mutation-probe-copies/target.sh
TALLY_AUDIT: FAIL (non-comment lines differ from sibling majority)
RESTORED sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 expected_exit=0 exit=0
command: timeout 15 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/mutation-probe-copies/target.sh
TALLY_AUDIT: PASS (non-comment lines match sibling majority)
restored_exact_bytes=true
source_after_sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
MUTATION_VERDICT: killed
```

Mutation verdict: **killed**, with a passing pristine baseline and passing restored detector. Exact restored target bytes equaled the saved original; the source runner was never mutated.

## Before/after integrity

Before setup and after both runs, `sha256sum` over the production frozen counter, contract, and runner returned the following unchanged hashes:

| File, relative to the production lane | Before SHA-256 = after SHA-256 |
| --- | --- |
| `.ufo/evidence/round-32/c1-measure.py` | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` |
| `.ufo/evidence/round-32/contract.json` | `7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |

The sandbox runner had that same pinned hash. Control tool SHA-256: `183c77a8ffacd7219547a04c73d26209627f318f80a26794a8e2f24392bb20c4`.

Exact initial integrity command:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
```

Exact final integrity command, with the sandbox source and tool appended:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlSiblingConsensus/lane/tools/tally-audit.py
```

## Smallest safe correction

No correction was applied to the frozen counter, predicate, or runner. The required benign variants already prevent this exact consensus control from meeting C1. The sibling-read channel nevertheless exists: a future, separately versioned counter could expose only one runner copy per filesystem-isolated invocation rather than all copies in a shared readable directory. Merely changing the current working directory does not close that channel. The production audit should test tally behavior rather than interpret textual disagreement as a defect.
