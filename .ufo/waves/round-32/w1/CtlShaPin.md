# CtlShaPin — round 32, wave 1

Verdict: **control rejected as expected**. The first and only frozen-counter run exited **1** with `C1_R32_PASS=false`: `kill=18/18 accept=1/8 other=7 runner_sha_ok=1 tool_present=1`. This is not a counter-bypass finding. The separate reversible T08 probe was **killed**, with passing pristine and restored baselines.

Axis: **operability**. Probe dimensions: fixture discrimination and byte preservation. This report does not adjudicate the real tool or the round.

## Evidence and scope

- Read the frozen contract and counter before creating the control. Contract `.ufo/evidence/round-32/contract.json:13-20` requires both rejection of all must-kill copies and acceptance of all must-accept copies. Lines 23-26 enumerate the families.
- The control's only decision is byte-hash equality at `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/tally-audit.py:14-16`. It does not inspect tally behavior.
- Frozen counter `.ufo/evidence/round-32/c1-measure.py:189-196` classifies the tool's exit and stdout. Lines 267-277 count correctness against each copy's set and compute the final predicate. An `outcome=KILL` on an accept copy is an incorrect answer and contributes to `other`.
- The single sandbox commit is `128bd271563cb87d6b60a061c725374137c07bf7`, created on detached `c31814978969a41a8e9b0f7d99fa308c5993c1b7`. Its only staged path was `tools/tally-audit.py`. No production source, counter, contract, lane index, or sibling scratch directory was edited.

All commands below ran with working directory `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin`.

### Setup and commit

The seat directory was created by the file-writing tool when recording `probe-scope.txt`. Then:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed: no stdout; exit 0.

After creating the control source shown below:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlShaPin && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane rev-parse HEAD
```

Observed stdout, exit 0:

```text
128bd271563cb87d6b60a061c725374137c07bf7
```

### Frozen-counter command

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/w-CtlShaPin
```

Fresh work directory; no `--seed`; no rerun. Exit code: **1**. Full stdout verbatim:

```text
COPY set=kill id=T08 outcome=KILL exit=1 sha256=12ad1d9076a55050 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N05 outcome=KILL exit=1 sha256=e1ef181c1e621962 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H03 outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=H04 outcome=KILL exit=1 sha256=0dc1e6b07452f610 last='TALLY_AUDIT: FAIL'
COPY set=kill id=H05 outcome=KILL exit=1 sha256=adf6763d6524f342 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N01 outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=N02 outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=N03 outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gT08(arm=20) outcome=KILL exit=1 sha256=45d85ff737dac94f last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN05(<= nlegs - 1) outcome=KILL exit=1 sha256=7184b157539cad8c last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(:) outcome=KILL exit=1 sha256=fba8e1cf3e1bfd8b last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH05(drop=4,dup=1) outcome=KILL exit=1 sha256=76ebad9ba6973c8c last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN01(vector=2) outcome=KILL exit=1 sha256=c0a32ec4e69d3cb0 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN02(or) outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_roundgate,dup=st_claims) outcome=KILL exit=1 sha256=f3ff71fbe9d61ab9 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=KILL exit=1 sha256=91066af826f69ecb last='TALLY_AUDIT: FAIL'
COPY set=accept id=B2-reversed outcome=KILL exit=1 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B3-decoys outcome=KILL exit=1 sha256=7c76617e87c11c49 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B4-cosmetic outcome=KILL exit=1 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: FAIL'
COPY set=accept id=B5-renamed outcome=KILL exit=1 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB6-permuted outcome=KILL exit=1 sha256=8b7db1481d58b29f last='TALLY_AUDIT: FAIL'
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=de74eadb945ce6fb last='TALLY_AUDIT: FAIL'
C1_R32: kill=18/18 accept=1/8 other=7 runner_sha_ok=1 tool_present=1 seed=0ab67597353f4d5e rev=128bd271563cb87d6b60a061c725374137c07bf7 C1_R32_PASS=false
```

The control got all 18 must-kill copies and `B0-pristine` right. It falsely rejected `B1-T07`, `B2-reversed`, `B3-decoys`, `B4-cosmetic`, `B5-renamed`, `gB6-permuted`, and `gB7-nonce`. Only the pristine accept copy has the pinned hash; every other supplied copy differs in bytes. This explains the result without treating hash rejection as behavioral auditing.

## Full control source

Path: `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/tally-audit.py`.
SHA-256: `fc3b88a19078977d906066b320c792f94ec66d48b328a76e715a7d41fcc5dd15`.

```python
#!/usr/bin/env python3
import argparse
import hashlib

PINNED_RUNNER_SHA = 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', required=True)
    args = parser.parse_args()
    with open(args.runner, 'rb') as runner:
        digest = hashlib.sha256(runner.read()).hexdigest()
    accepted = digest == PINNED_RUNNER_SHA
    print('TALLY_AUDIT: PASS' if accepted else 'TALLY_AUDIT: FAIL')
    return 0 if accepted else 1


if __name__ == '__main__':
    raise SystemExit(main())
```

## Reversible mutation probe and restoration

Mutant: frozen T08, a single added case arm that counts status 4 as a pass instead of setup. The mutation was confined to `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh:1437`, immediately after the existing status-1 arm. Expected detector: this sha-pin control accepts the pristine bytes, rejects the T08 bytes, and accepts the exact restored bytes. This is a hash-sensitivity probe, not evidence of semantic coverage.

Preparation command, exit 0, no stdout:

```sh
cp /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh
```

The same bounded detector command was used for pristine and mutated states:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh && timeout 10 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh
```

Pristine stdout, exit **0**:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh
TALLY_AUDIT: PASS
```

Using the surgical edit tool, inserted exactly this line after line 1436:

```bash
      4) npass=$((npass + 1)) ;;
```

Mutated stdout, exit **1**:

```text
12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh
TALLY_AUDIT: FAIL
```

Removed only that inserted line using the surgical edit tool. The restored command reused the identical detector and then compared full bytes:

```sh
sha256sum /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh && timeout 10 python3 /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/tally-audit.py --runner /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh && cmp /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/mutate-and-run.sh && printf 'RESTORE_CMP: identical\n'
```

Restored stdout, exit **0**:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/runner-probe.sh
TALLY_AUDIT: PASS
RESTORE_CMP: identical
```

Verdict for this mutation: **killed**, not inconclusive; the pristine baseline passed. Before and restored SHA-256 are identical, and `cmp` independently confirmed restoration to the clone's untouched runner bytes. The committed control remains available in the isolated clone.

## Frozen-input preservation

Before the counter and mutation probe, ran:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/mutate-and-run.sh
```

Observed stdout, exit 0:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/mutate-and-run.sh
```

After restoration, ran:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/tally-audit.py
```

Observed stdout, exit 0:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/mutate-and-run.sh
fc3b88a19078977d906066b320c792f94ec66d48b328a76e715a7d41fcc5dd15  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaPin/lane/tools/tally-audit.py
```

Storage check `df -h /fast` reported 110G available during setup. No tool installations or updates were needed. All started commands completed; no service or background process was left running.

## Smallest safe correction

No counter or contract change is indicated by this control. Keep sha pinning as the unchanged-production-runner check only; do not use it as the audit decision for supplied copies. The real tool must implement the frozen per-leg, independent-oracle, and harness checks so that behavior-preserving byte edits can be accepted. No production correction was made by this seat.
