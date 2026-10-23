# CtlShaTable

**Verdict: the fixture-keyed control was rejected as expected.** The committed exact-byte plus comment-stripped hash-table control returned `C1_R32_PASS=false`, exit 1: kill=12/18, accept=8/8, other=6. This run does not produce a counter-passing control finding. Formal pristine/mutated/restored mutation-test verdict: **inconclusive**, not killed, because the pristine revision has no audit tool and its detector already fails.

Axis: **operability**. No numeric axis assessment or round-admission judgment is made. The no-harm boundary is exact runner-byte preservation.

## Evidence

### Contract and mutation point

- `.ufo/evidence/round-32/contract.json:12-20` defines the audit surface, exact pass predicate and immutable runner hash; `:23-26` enumerates the copy families.
- `.ufo/evidence/round-32/c1-measure.py:82-93` supplies the nine frozen must-kill bodies; `:140-158` supplies the six frozen must-accept bodies. The module was imported from that production path at control-build time using `importlib`, with `sys.dont_write_bytecode = True` set before import, so no import cache was written there.
- The pinned runner bytes were read through the counter's read-only `git` helper from this seat's clone using `git show e24688b2ff6cca1c9ad20e112f02c629b8597ff8:tools/mutate-and-run.sh`. Its full SHA-256 matched the pin before table construction.
- The sole defect is replacing semantic auditing with fixture membership. At sandbox commit `5d22bc41f5d0259e64703c065a21b5dd53b35707`, `tools/tally-audit.py:13-38` embeds all nine kill hashes, all six accept hashes, and the nine normalized kill hashes. Lines 41-45 delete every line whose left-stripped bytes begin with `#`, including the shebang. Lines 57-64 return FAIL only for an exact kill hash **or** a comment-stripped kill hash; every other readable input passes. The accept table is embedded as requested, not used as a whitelist.
- Both requested lookup shapes are present in this one tool and one sandbox commit. The frozen counter scored their union, not two separately seeded tool revisions.
- Expected detector: the frozen counter must reject this fixture-only shortcut because nonmatching generated must-kill copies pass. Its condition is at `c1-measure.py:264-277`.

### Isolated setup and single sandbox commit

All table construction, control execution and detector runs used working directories under `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/`. Setup deviation: the initial `mkdir`/clone/checkout command and concurrent `df` command used its parent `/fast/scratch/hyaku/tameshi-r32-seats` as cwd while the seat directory was being created; their writes were limited to this seat's absolute clone path. This did not comply literally with the seat-only working-directory bound. No sibling scratch directory was opened. No production Git write command, `jj` command, or subagent dispatch was used.

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed: exit 0, no stdout or stderr.

The build used these actual operations in the Python cell, then generated the full source below and wrote it with the file-writing tool:

```python
os.chdir(seat)
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('r32_frozen_counter', counter_path)
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)
pinned_result = counter.git(str(seat / 'lane'), 'show', counter.PIN_REV + ':' + counter.RUNNER)
runner_bytes = pinned_result.stdout
runner_text = runner_bytes.decode('utf-8')
frozen_kill = counter.frozen_kill(runner_text)
frozen_accept = counter.frozen_accept(runner_text)
def no_comment_lines(data):
    return b''.join(line for line in data.splitlines(keepends=True) if not line.lstrip().startswith(b'#'))
kill_sha = {label: hashlib.sha256(body.encode('utf-8')).hexdigest() for label, body in frozen_kill}
accept_sha = {label: hashlib.sha256(body.encode('utf-8')).hexdigest() for label, body in frozen_accept}
kill_normalized_sha = {label: hashlib.sha256(no_comment_lines(body.encode('utf-8'))).hexdigest() for label, body in frozen_kill}
```

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlShaTable
```

Observed: exit 0, no stdout or stderr. Commit receipt command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane show --stat --format='%H%n%P%n%an <%ae>%n%s' HEAD
```

Observed stdout, exit 0:

```text
5d22bc41f5d0259e64703c065a21b5dd53b35707
c31814978969a41a8e9b0f7d99fa308c5993c1b7
ctl <ctl@sandbox>
CtlShaTable

 tools/tally-audit.py | 68 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 68 insertions(+)
```

### Frozen counter on the committed control

Exact command, no `--seed`, fresh absent work directory:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/w-CtlShaTable
```

Full stdout verbatim:

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
COPY set=kill id=gT08(arm=72) outcome=ACCEPT exit=0 sha256=69b67cb178fcefe5 last='TALLY_AUDIT: PASS'
COPY set=kill id=gN05(<= nlegs - 1) outcome=ACCEPT exit=0 sha256=7184b157539cad8c last='TALLY_AUDIT: PASS'
COPY set=kill id=gH03(form=0) outcome=KILL exit=1 sha256=2ac4ce5344e6100a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gH04(true) outcome=ACCEPT exit=0 sha256=eceff075da31e6d4 last='TALLY_AUDIT: PASS'
COPY set=kill id=gH05(drop=8,dup=0) outcome=ACCEPT exit=0 sha256=e2e6fdd9e8a34891 last='TALLY_AUDIT: PASS'
COPY set=kill id=gN01(vector=3) outcome=ACCEPT exit=0 sha256=c66c1ca66cf8ae0f last='TALLY_AUDIT: PASS'
COPY set=kill id=gN02(or) outcome=KILL exit=1 sha256=31128639afc3e57a last='TALLY_AUDIT: FAIL'
COPY set=kill id=gN03(or) outcome=KILL exit=1 sha256=741907e82ca7e907 last='TALLY_AUDIT: FAIL'
COPY set=kill id=gD01(drop=st_tsu,dup=st_checklist) outcome=ACCEPT exit=0 sha256=6439a35d27eb7221 last='TALLY_AUDIT: PASS'
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last='TALLY_AUDIT: PASS'
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last='TALLY_AUDIT: PASS'
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last='TALLY_AUDIT: PASS'
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last='TALLY_AUDIT: PASS'
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last='TALLY_AUDIT: PASS'
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=337ef4ee5a830543 last='TALLY_AUDIT: PASS'
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=1eabf4db8f0392fd last='TALLY_AUDIT: PASS'
C1_R32: kill=12/18 accept=8/8 other=6 runner_sha_ok=1 tool_present=1 seed=d9fb80b855f4d754 rev=5d22bc41f5d0259e64703c065a21b5dd53b35707 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty. Raw receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/control.stdout`, `control.stderr`, and `control.exit`.

The copies it got right were all nine frozen must-kills (T08, N05, H03, H04, H05, N01, N02, N03, D01), the three generated exact aliases `gH03(form=0)`, `gN02(or)`, `gN03(or)`, and all eight must-accept copies. The three generated kills have the same printed SHA-256 prefixes as their frozen counterparts and are the identical edits defined by `c1-measure.py:102-106,124-129`.

Six generated faulty copies survived the control: `gT08(arm=72)`, `gN05(<= nlegs - 1)`, `gH04(true)`, `gH05(drop=8,dup=0)`, `gN01(vector=3)`, and `gD01(drop=st_tsu,dup=st_checklist)`. Adding comment-line normalization did not reject these variants. In the counter's summary, `other=6` counts these wrong ACCEPT outcomes; it does not mean six executions crashed or produced outcome OTHER.

### Pristine detector run

Exact command, fresh absent work directory, no `--seed`:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane --rev c31814978969a41a8e9b0f7d99fa308c5993c1b7 --work /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/w-CtlShaTable-pristine
```

Full stdout verbatim:

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
COPY set=kill id=gT08(arm=148) outcome=OTHER exit=no-tool sha256=15af4dc6f2a57917 last=''
COPY set=kill id=gN05(<= nlegs - 1) outcome=OTHER exit=no-tool sha256=7184b157539cad8c last=''
COPY set=kill id=gH03(form=0) outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=gH04(rc=$?) outcome=OTHER exit=no-tool sha256=0dc1e6b07452f610 last=''
COPY set=kill id=gH05(drop=0,dup=2) outcome=OTHER exit=no-tool sha256=45d9362b5c0544a8 last=''
COPY set=kill id=gN01(vector=1) outcome=OTHER exit=no-tool sha256=ebf4a902638d568e last=''
COPY set=kill id=gN02(or) outcome=OTHER exit=no-tool sha256=31128639afc3e57a last=''
COPY set=kill id=gN03(split) outcome=OTHER exit=no-tool sha256=16566843890d60ab last=''
COPY set=kill id=gD01(drop=st_js,dup=st_roundgate) outcome=OTHER exit=no-tool sha256=1a1f88fb935d5073 last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=eca99f2c16ffb376 last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=e7e33c92000bc789 last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=c00ca33765d67e94 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty. Raw receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/pristine.stdout`, `pristine.stderr`, and `pristine.exit`. The absence of a baseline tool makes a conventional killed-mutant assertion inconclusive.

### Exact restoration and restored detector run

The only added working-tree file was `lane/tools/tally-audit.py`. The edit tool deleted that seat-owned file after scoring, restoring its original absent state. The one sandbox commit remains at HEAD for reproducibility; its committed source is unchanged and is included in full below. The sandbox intentionally has the working-tree deletion, not a second commit. No runner bytes were ever edited. The restored detector explicitly addresses the original revision because the counter reads committed blobs, not working-tree files.

Exact command, fresh absent work directory, no `--seed`:

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane --rev c31814978969a41a8e9b0f7d99fa308c5993c1b7 --work /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/w-CtlShaTable-restored
```

Full stdout verbatim:

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
COPY set=kill id=gT08(arm=66) outcome=OTHER exit=no-tool sha256=78c5368d065ecb84 last=''
COPY set=kill id=gN05(< nlegs) outcome=OTHER exit=no-tool sha256=e1ef181c1e621962 last=''
COPY set=kill id=gH03(form=0) outcome=OTHER exit=no-tool sha256=2ac4ce5344e6100a last=''
COPY set=kill id=gH04(true) outcome=OTHER exit=no-tool sha256=eceff075da31e6d4 last=''
COPY set=kill id=gH05(drop=6,dup=2) outcome=OTHER exit=no-tool sha256=98a176d2b683ff00 last=''
COPY set=kill id=gN01(vector=3) outcome=OTHER exit=no-tool sha256=c66c1ca66cf8ae0f last=''
COPY set=kill id=gN02(true) outcome=OTHER exit=no-tool sha256=29d0e2b6649efed2 last=''
COPY set=kill id=gN03(or) outcome=OTHER exit=no-tool sha256=741907e82ca7e907 last=''
COPY set=kill id=gD01(drop=st_kagi,dup=st_checklist) outcome=OTHER exit=no-tool sha256=a9a380c96c715cdd last=''
COPY set=accept id=B0-pristine outcome=OTHER exit=no-tool sha256=a7d3f2dd7d47511a last=''
COPY set=accept id=B1-T07 outcome=OTHER exit=no-tool sha256=91066af826f69ecb last=''
COPY set=accept id=B2-reversed outcome=OTHER exit=no-tool sha256=7d3d5a5f34fe3595 last=''
COPY set=accept id=B3-decoys outcome=OTHER exit=no-tool sha256=7c76617e87c11c49 last=''
COPY set=accept id=B4-cosmetic outcome=OTHER exit=no-tool sha256=137a7ba8a58c5277 last=''
COPY set=accept id=B5-renamed outcome=OTHER exit=no-tool sha256=f66fe32a4ea7ce76 last=''
COPY set=accept id=gB6-permuted outcome=OTHER exit=no-tool sha256=621e99c9d04c3d32 last=''
COPY set=accept id=gB7-nonce outcome=OTHER exit=no-tool sha256=4b815c6439656c48 last=''
C1_R32: kill=0/18 accept=0/8 other=26 runner_sha_ok=1 tool_present=0 seed=69663977756fe857 rev=c31814978969a41a8e9b0f7d99fa308c5993c1b7 C1_R32_PASS=false
```

Exit code: `1`. Stderr: empty. The Python existence observation after deletion was `RESTORED_TOOL_PRESENT=False`, matching `PRISTINE_TOOL_PRESENT=False`. Raw receipts: `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/restored.stdout`, `restored.stderr`, and `restored.exit`. Each run used a fresh random seed as instructed; these are not identical random panels or attempted reseed repairs of the control result.

### Before, mutated and restored hashes

The added tool was absent before, had SHA-256 `92e3d3591dfc78ed5cae38b384e69e2a8e22cee104609e0c52f0899fa2dcb3d4` while scored, and is absent again in the restored working tree. The immutable sandbox commit preserves exactly those 3,180 source bytes.

The following command was run before construction and again after restoration; both outputs were identical and both exits were 0:

```sh
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane/tools/mutate-and-run.sh
```

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/contract.json
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane/tools/mutate-and-run.sh
```

Immediately after scoring and before deletion the same hash command, with the tool path appended, also observed the unchanged four hashes and:

```text
92e3d3591dfc78ed5cae38b384e69e2a8e22cee104609e0c52f0899fa2dcb3d4  /fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane/tools/tally-audit.py
```

### Full committed control source

Path: `/fast/scratch/hyaku/tameshi-r32-seats/CtlShaTable/lane/tools/tally-audit.py` at commit `5d22bc41f5d0259e64703c065a21b5dd53b35707`. Full source, verbatim:

```python
#!/usr/bin/env python3
"""Pre-data control: fixture hashes, not a semantic runner audit.

The exact-byte table is the first shape. The additional comment-stripped
lookup is the second shape. Accept hashes are embedded as a build receipt;
all inputs not matching a kill table pass, including unknown inputs.
"""
import argparse
import hashlib
import sys
from pathlib import Path

MUST_KILL_SHA256 = {'T08': '12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b',
 'N05': 'e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe',
 'H03': '2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c',
 'H04': '0dc1e6b07452f6108f9dd7f99050aa0d8b8450456c3424f22da1a7fc54e5d6cd',
 'H05': 'adf6763d6524f342b5496ff52f0fce96e0b4a00b5ab26cfa43be2001654b36d0',
 'N01': 'c0a32ec4e69d3cb07a7949efb7c9a83ac2b4b431f6e4da3f8bd76a1cd0d4cb34',
 'N02': '31128639afc3e57a0d68f0abe94cc5038954ff41d6f9949da4fa903331f56250',
 'N03': '741907e82ca7e907881cb985b7a504771de78d14b1179530661066a8f22a5b6f',
 'D01': '71a66c5a611d408fe08c3618a18f30fe6d4e43308e36ee1f074420547c4f695c'}

MUST_ACCEPT_SHA256 = {'B0-pristine': 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9',
 'B1-T07': '91066af826f69ecb6e6ccb0e837b3e2a37c1edfc6bf0aefb0c78e378bb1eeb28',
 'B2-reversed': '7d3d5a5f34fe3595d85ebcc06e657a814b7c86dcf285032e585b533d1c627874',
 'B3-decoys': '7c76617e87c11c49ffc4ff4145b7d1afeea6bdd9373b9cc8cae2ac39322d03c2',
 'B4-cosmetic': '137a7ba8a58c52772963560b3666ba22edc917bfc0836aa20bc74c89e0341695',
 'B5-renamed': 'f66fe32a4ea7ce7630820241dc484b902679ac1caa2b88410222855ad7b2abae'}

COMMENT_STRIPPED_KILL_SHA256 = {'T08': 'eb8db9cbb12af0f4e59bdf82a945df6ddcfcb5489a3c446bdf71402c3d96f161',
 'N05': 'b158153da308aa703783e5e7159f215cf464f7fa7a490b00174b7d7b047b8318',
 'H03': '74aa24c6a8c3fbe7cc71ece39b892b9a6e491d75d25d62ce22631dd5ca095653',
 'H04': '0acd8412200dc532085a7d2da9c7bcc4b277b6b6a6cdc7c718a0e1dbcc25a427',
 'H05': 'acf6db26b5c78deb3332da9839e4f4fe9ab3fc67d29e2d725a8921680c667bb1',
 'N01': '12493997ebb8b0ab9b803d47ce85a46bd88b4da8765602066691a22b510d119d',
 'N02': '732eb803ff0c4276f746e10446fd53009041d3bd6a89002995f93ba9857447f5',
 'N03': '74a74824bcb50459aaae26db6e6ab8268e64a165a3dfdf9ee6cb53d7f258222c',
 'D01': 'bc372bb214734dd04c55ccc955a8efb0f89590cde4b713e914e1692bf59bcb05'}


def without_comment_lines(data):
    return b"".join(
        line for line in data.splitlines(keepends=True)
        if not line.lstrip().startswith(b"#")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True)
    args = parser.parse_args()
    try:
        data = Path(args.runner).read_bytes()
    except OSError as error:
        print("TALLY_AUDIT: cannot audit: " + str(error), file=sys.stderr)
        return 2
    exact = hashlib.sha256(data).hexdigest()
    stripped = hashlib.sha256(without_comment_lines(data)).hexdigest()
    fail = (
        exact in MUST_KILL_SHA256.values()
        or stripped in COMMENT_STRIPPED_KILL_SHA256.values()
    )
    print("TALLY_AUDIT: FAIL" if fail else "TALLY_AUDIT: PASS")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Smallest safe correction

No change to the frozen counter or contract follows from this rejected control. For the eventual audit tool, replace fixture membership with the declared semantic checks; accepting six nonmatching generated defects is the precise failure this control exposes. No production correction was attempted by this seat.

No tools were installed or upgraded. The concurrent setup check `df -h /fast` reported 112G available. No `--regression` run was made. All started commands returned, all bounded detector subprocesses completed, and no long-lived process was started or left to kill. No build, lint, formatter, or unrelated verification was run.
