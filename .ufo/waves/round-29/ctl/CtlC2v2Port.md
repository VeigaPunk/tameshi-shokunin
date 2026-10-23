# C2 v2 control port — round 29

## Scope, axes and result

Frozen B: `6ab11a6274d6111deb2b31b2ba6b4f742603bd49`. Private clone: `/fast/scratch/hyaku/tameshi-r29-CtlC2v2Port`. The claim axis is **coverage**, frontier F6. The probe axes are **detector discrimination**, **source provenance**, and **exact restoration**; these are control dimensions, not additional round claims.

**No assigned control reached `C2_F6_V2_PASS=true`.** Every detector invocation exited 1, with empty stderr. Both the short authentic title quote and rewritten snapshot were rejected. No judgment, integration, model call, seat spawn, contract edit or production change was performed.

**Single-check coverage findings:** V4, V5, V7a and V7b achieved `kill_original=1`, `ddmin_match=1`, `kill=1` and `one_minimal=1` without building on the pinned declaration or performing a participant-side reduction. V5 did this with one external absolute census row and no host nodes. V7a and V7b also achieved `entry_sourced=1` using nonsense prose and count/source markers alone. No tested control achieved `anchored=1` or `quote_located=1`. These are component results, **not a bypass of the v2 conjunction**: `anchored=0` blocks all of these controls. The counter did run its own ddmin on the trivial killing inputs; this report does not claim otherwise.

Mutation interpretation: the mutant is an evidence-only shortcut substitution, not a change to the frozen counter. Expected whole-detector result is FAIL for each shortcut. Pristine B itself fails, so the classic mutation-testing verdict is **inconclusive**, not “killed.” Observed component acceptance is a coverage finding and does not change the contract. Claim admission remains solely with L1 TameshiR29.

## Isolation and exact construction

Only the private clone and this lane report were written. Kagi was read-only. No `jj` command or lane Git write command was run. The three required Git environment variables were removed from every subprocess environment; the counter itself removes all `GIT_*` variables for its Git reads. No tools were installed or updated.

Initial commands actually run:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE mkdir -p /fast/scratch/hyaku
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r29-CtlC2v2Port
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r29-CtlC2v2Port checkout -q --detach 6ab11a6274d6111deb2b31b2ba6b4f742603bd49
cp /fast/scratch/hyaku/tameshi-r29-CtlC2v2Port/.ufo/evidence/round-29/c2-measure-v2.py /tmp/CtlC2v2Port-c2v2.py
```

V2 through V7b are successive private commits. The clone was then restored to B and scored; V2r is an independent child of B with genuinely seeded random junk; the clone was restored to B and scored again. Each private control commit is retained by `ctl-C2v2-<id>`.

File construction used the write tool through these exact Eval helpers (writes in a fixture batch ran concurrently):

```python
import asyncio, random
from pathlib import Path
root = Path('/fast/scratch/hyaku/tameshi-r29-CtlC2v2Port')
files = ('census.tsv', 'shapes.tsv', 'baseline.tsv', 'host.tsv')
f6 = '.ufo/evidence/round-29/f6'
entry_path = 'corpus/knowledge/survivor-fixture-minimization.md'
lesson_path = 'corpus/lessons/round-29.md'
snap_path = '.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html'
async def put(path, content):
    return await tool.write({'i': 'Writing isolated control fixture', 'path': str(root/path), 'content': content})
async def fixture(census='', shapes='', baseline='', host=''):
    data = dict(zip(files, (census, shapes, baseline, host)))
    return await asyncio.gather(*(put(f'{f6}/{sub}/{f}', content)
        for sub in ('original', 'minimized') for f, content in data.items()))
```

Every fixture call overwrites all eight files. Both layouts therefore have identical bytes. Empty means zero bytes, not a blank line. All new fixture/entry/lesson lines end in one newline. The content field `x` in `host.tsv` creates a one-byte non-executable file when materialized; there is no real host tree committed.

All Git and detector commands below ran with cwd `/fast/scratch/hyaku/tameshi-r29-CtlC2v2Port`. Common detector command, unchanged for pristine, variants and restored B:

```sh
timeout 900 python3 /tmp/CtlC2v2Port-c2v2.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC2v2Port --rev HEAD
```

The initial V1 call additionally used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` between timeout and python3. All subsequent calls used the equivalently stripped subprocess environment. No detector timed out.

## Full per-control receipts

### V1

Built: B unchanged; built nothing.

Expected detector: FAIL: fixture absent.

Exact construction call/command:

```sh
# No construction: frozen B unchanged.
```

Private commit: `6ab11a6274d6111deb2b31b2ba6b4f742603bd49`.

Full counter stdout:

```text
C2_F6_V2: fixture=absent anchored=0 kill_original=0 units_original=0 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=6ab11a6274d6111deb2b31b2ba6b4f742603bd49
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V1: meets=no

### V2

Built: All eight fixture files contain one deterministic arbitrary junk line; no source entry or lesson.

Expected detector: FAIL: malformed host manifest and unanchored census.

Exact construction call/command:

```python
await fixture('X-92 random nonsense\n', 'Q-17 non-tsv random line\n', 'M-83 random baseline rubbish\n', 'P-41 random host manifest rubbish\n')
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V2'
git branch ctl-C2v2-V2
```

Private commit: `6c005f26b0d59caf7e1d97b7af24ef8abf516d6f`.

Full counter stdout:

```text
  oracle tests run: 0
C2_F6_V2: fixture=invalid anchored=0 kill_original=0 units_original=4 units_minimized=4 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=6c005f26b0d59caf7e1d97b7af24ef8abf516d6f
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V2: meets=no

### V3

Built: All eight fixture files are empty bytes; no source entry or lesson.

Expected detector: FAIL: empty census is not pinned and cannot kill B5.

Exact construction call/command:

```python
await fixture()
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V3'
git branch ctl-C2v2-V3
```

Private commit: `272098a1ae485c81fe03f5233bae96c0d8f0a48d`.

Full counter stdout:

```text
  oracle tests run: 1
C2_F6_V2: fixture=present anchored=0 kill_original=0 units_original=0 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=272098a1ae485c81fe03f5233bae96c0d8f0a48d
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V3: meets=no

### V4

Built: Handwritten census $HOME/p\tasset\texec\t-\tx; host manifest p\tfile\t644\tx; empty shapes/baseline; original=minimized.

Expected detector: FAIL: handwritten census is not pinned, and source/quote absent; genuine kill/minimality bits may be true.

Exact construction call/command:

```python
await fixture(census='$HOME/p\tasset\texec\t-\tx\n', host='p\tfile\t644\tx\n')
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V4'
git branch ctl-C2v2-V4
```

Private commit: `c96d69c5fed72e0903916fd5467e33ceed5e8cfa`.

Full counter stdout:

```text
  oracle tests run: 3
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=2 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=0 quote_located=0 rev=c96d69c5fed72e0903916fd5467e33ceed5e8cfa
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V4: meets=no

### V5

Built: External absolute census /etc/hostname\tasset\texec\t-\tx; all other files empty; original=minimized.

Expected detector: FAIL: external one-line census is not pinned, and source/quote absent; individual kill/minimality checks must be reported separately.

Exact construction call/command:

```python
await fixture(census='/etc/hostname\tasset\texec\t-\tx\n')
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V5'
git branch ctl-C2v2-V5
```

Private commit: `7e23bc420e36df6cb691c3ca98749f6cfb5fe1fb`.

Full counter stdout:

```text
  oracle tests run: 2
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=1 units_minimized=1 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=0 quote_located=0 rev=7e23bc420e36df6cb691c3ca98749f6cfb5fe1fb
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V5: meets=no

### V6a

Built: Handwritten census $HOME/p\tasset\texec\t-\tx; malformed/escaping host line '../p\tfile\t644\tx\n'; original=minimized.

Expected detector: FAIL: host manifest contains a parent traversal.

Exact construction call/command:

```python
await fixture(census='$HOME/p\tasset\texec\t-\tx\n', host='../p\tfile\t644\tx\n')
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V6a'
git branch ctl-C2v2-V6a
```

Private commit: `7561b66590482d31671892460a64bf97c87474d1`.

Full counter stdout:

```text
  oracle tests run: 0
C2_F6_V2: fixture=invalid anchored=0 kill_original=0 units_original=2 units_minimized=2 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=7561b66590482d31671892460a64bf97c87474d1
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V6a: meets=no

### V6b

Built: Handwritten census $HOME/p\tasset\texec\t-\tx; malformed/escaping host line '/tmp/CtlC2v2Port-p\tfile\t644\tx\n'; original=minimized.

Expected detector: FAIL: host manifest contains an absolute path.

Exact construction call/command:

```python
await fixture(census='$HOME/p\tasset\texec\t-\tx\n', host='/tmp/CtlC2v2Port-p\tfile\t644\tx\n')
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V6b'
git branch ctl-C2v2-V6b
```

Private commit: `4829028b43f47f44cafee4341b083c0af6632a04`.

Full counter stdout:

```text
  oracle tests run: 0
C2_F6_V2: fixture=invalid anchored=0 kill_original=0 units_original=2 units_minimized=2 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=4829028b43f47f44cafee4341b083c0af6632a04
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V6b: meets=no

### V6c

Built: Handwritten census $HOME/p\tasset\texec\t-\tx; malformed/escaping host line 'p\tlink\t644\tx\n'; original=minimized.

Expected detector: FAIL: host manifest kind link is forbidden.

Exact construction call/command:

```python
await fixture(census='$HOME/p\tasset\texec\t-\tx\n', host='p\tlink\t644\tx\n')
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V6c'
git branch ctl-C2v2-V6c
```

Private commit: `7fb43e8fae5081a1c41aee71635c4e2575023c35`.

Full counter stdout:

```text
  oracle tests run: 0
C2_F6_V2: fixture=invalid anchored=0 kill_original=0 units_original=2 units_minimized=2 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=7fb43e8fae5081a1c41aee71635c4e2575023c35
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V6c: meets=no

### V7a

Built: V4 two-unit handwritten fixture; source S024 with correct units_original=2/units_minimized=2 and nonsense body; lesson quotes only The Fuzzing Book against frozen digest.

Expected detector: FAIL: unanchored census and three-word quote; entry markers may pass despite nonsense prose.

Exact construction call/command:

```python
await fixture(census='$HOME/p\tasset\texec\t-\tx\n', host='p\tfile\t644\tx\n')
await asyncio.gather(put(entry_path, 'source: S024\nunits_original=2\nunits_minimized=2\n\nBananas are triangular. No reduction was performed.\n'), put(lesson_path, 'S024 3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99 "The Fuzzing Book"\n'))
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6 corpus/knowledge/survivor-fixture-minimization.md corpus/lessons/round-29.md
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V7a'
git branch ctl-C2v2-V7a
```

Private commit: `1c3563d500c6407feae1da365a668d379205441a`.

Full counter stdout:

```text
  oracle tests run: 3
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=2 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=1 quote_located=0 rev=1c3563d500c6407feae1da365a668d379205441a
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V7a: meets=no

### V7b

Built: V7a but rewritten snapshot and matching digest/quote; fabricated quote is ten words and contains minimal to isolate the frozen digest requirement.

Expected detector: FAIL: unanchored census and rewritten source snapshot digest, even with a matching ten-word fake quote.

Exact construction call/command:

```python
await asyncio.gather(put(snap_path, '<html><body>This minimal example proves absolutely nothing about actual reduction work.</body></html>\n'), put(lesson_path, 'S024 4cbcd9ab82d4d4b81046f52b6c0703cdee2249b89a199faeefd3ecb7537f1f76 "This minimal example proves absolutely nothing about actual reduction work."\n'))
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html corpus/lessons/round-29.md
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V7b'
git branch ctl-C2v2-V7b
```

Private commit: `c945be98c75b285ecf6ea2682a222550065ad939`.

Full counter stdout:

```text
  oracle tests run: 3
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=2 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=1 quote_located=0 rev=c945be98c75b285ecf6ea2682a222550065ad939
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V7b: meets=no

### RESTORE-1

Built: Restore frozen B after V2-V7b.

Expected detector: Same output as pristine B.

Exact construction call/command:

```sh
git checkout -q --detach 6ab11a6274d6111deb2b31b2ba6b4f742603bd49
```

Private commit: `6ab11a6274d6111deb2b31b2ba6b4f742603bd49`.

Full counter stdout:

```text
C2_F6_V2: fixture=absent anchored=0 kill_original=0 units_original=0 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=6ab11a6274d6111deb2b31b2ba6b4f742603bd49
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL RESTORE-1: meets=no

### V2r

Built: Actual seeded random junk: random.Random(29), four 48-character alphanumeric lines, copied to both fixture layouts; no source entry or lesson.

Expected detector: FAIL: malformed host manifest and unanchored census.

Exact construction call/command:

```python
rng = random.Random(29)
random_junk = {f: ''.join(rng.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(48))+'\n' for f in files}
await asyncio.gather(*(put(f'{f6}/{sub}/{f}', content) for sub in ('original', 'minimized') for f, content in random_junk.items()))
```

Exact commit commands:

```sh
git add -f .ufo/evidence/round-29/f6
git -c user.name=ctl -c user.email=ctl@x commit -q -m 'ctl C2 v2 V2r'
git branch ctl-C2v2-V2r
```

Private commit: `9115014031d83eed5f4a6d671464fa581f5673d6`.

Full counter stdout:

```text
  oracle tests run: 0
C2_F6_V2: fixture=invalid anchored=0 kill_original=0 units_original=4 units_minimized=4 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=9115014031d83eed5f4a6d671464fa581f5673d6
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL V2r: meets=no

### RESTORE-FINAL

Built: Restore frozen B after the additional seeded-junk control.

Expected detector: Same output as pristine B.

Exact construction call/command:

```sh
git checkout -q --detach 6ab11a6274d6111deb2b31b2ba6b4f742603bd49
```

Private commit: `6ab11a6274d6111deb2b31b2ba6b4f742603bd49`.

Full counter stdout:

```text
C2_F6_V2: fixture=absent anchored=0 kill_original=0 units_original=0 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=6ab11a6274d6111deb2b31b2ba6b4f742603bd49
PREDICATE: C2_F6_V2_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL RESTORE-FINAL: meets=no

## Before/after hashes and exact restoration

Git tree object hashes below bind all committed path names, modes and bytes. “Before” follows the actual chronological mutation/restoration sequence, not a synthetic baseline. All variant commits are retained in the private clone.

| Step | Before tree | After tree |
|---|---|---|
| V1 | `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c` | `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c` |
| V2 | `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c` | `cb458107b51f88f0f052d55f0d55c1a5ece085ba` |
| V3 | `cb458107b51f88f0f052d55f0d55c1a5ece085ba` | `945c3002326c8f845be996805e3278a3ee90091a` |
| V4 | `945c3002326c8f845be996805e3278a3ee90091a` | `fa12b5c15e2dce636ebd41643c355d650206cd6c` |
| V5 | `fa12b5c15e2dce636ebd41643c355d650206cd6c` | `b91cd26e26ad82f94ec3a0d6993f7b7e113c0ce8` |
| V6a | `b91cd26e26ad82f94ec3a0d6993f7b7e113c0ce8` | `a5e49641278160976c19658c143eca0dcc86b9ae` |
| V6b | `a5e49641278160976c19658c143eca0dcc86b9ae` | `a0c15f3b6787f40fe87d1eb241d5ef7266622ff2` |
| V6c | `a0c15f3b6787f40fe87d1eb241d5ef7266622ff2` | `d3e0c6dd1b1f5a6d8af195dbf2c795f9d9a9fd48` |
| V7a | `d3e0c6dd1b1f5a6d8af195dbf2c795f9d9a9fd48` | `9ab27cc20c2d1ecd53f61f59c67368e090f3e74f` |
| V7b | `9ab27cc20c2d1ecd53f61f59c67368e090f3e74f` | `b605d1583b5474cf69e1234d2950645b59c7375d` |
| RESTORE-1 | `b605d1583b5474cf69e1234d2950645b59c7375d` | `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c` |
| V2r | `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c` | `7f297ff99dc943c1439724c720689faa4570ca6b` |
| RESTORE-FINAL | `7f297ff99dc943c1439724c720689faa4570ca6b` | `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c` |

SHA-256 before the first mutation and after the final restoration:

| File | Before | After |
|---|---|---|
| `.ufo/evidence/round-29/c2-measure-v2.py` | `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c` | `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c` |
| `.ufo/evidence/round-29/contract-amendment-1.json` | `50585bc82b81cc19422ba5dcf100ec12ddc22456fe9561b408ea7bb022b3dca4` | `50585bc82b81cc19422ba5dcf100ec12ddc22456fe9561b408ea7bb022b3dca4` |
| `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` | `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` | `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` |
| `/tmp/CtlC2v2Port-c2v2.py` | `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c` | `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c` |

The only source-snapshot mutation was V7b: SHA-256 changed from `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` to `4cbcd9ab82d4d4b81046f52b6c0703cdee2249b89a199faeefd3ecb7537f1f76`, then returned exactly to `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99`. The lesson carried the fake digest and the matching ten-word quote, so failure is not confounded by the earlier short-quote control.

Final HEAD is B and the before/after Git tree is exactly `2d1f4fe2732bc0b0cf805ee63a251869eecb2a8c`. The eight fixture files, source entry and lesson are all absent again, as at B. Both restored detector receipts reproduce the pristine B stdout and exit 1. A final process-table scan found **0** matching private detector processes; all bounded runs had already terminated, and no long-lived service was started. No process needed killing.

### Per-file mutation hashes

Both fixture layouts have the same bytes, so one SHA-256 row per filename represents original/ and minimized/. The snapshot hashes above cover the only overwritten pre-existing source. At B all fixture files, entry and lesson were absent.

| Control | census.tsv | shapes.tsv | baseline.tsv | host.tsv |
|---|---|---|---|---|
| V2 | `911d20cea77e521b82f7864286e2846aa9125831c1421af9c269640544319d82` | `997cb574ee0ab42352a508facc0255439e063347942b11b7b08d28739dfc79c2` | `c9df1d6ebf3cf636eca89f7b4ec4756d0c8081c0e9a8349e71b8de54f2a0aa96` | `3896b0acf0e15f8fa45fb8febbb9572589aa61171fbe191ef7a6a688a452aa60` |
| V3 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| V4 | `11e8fa92995dfb8869643a25f3553054ac8dd89f5d847170be63b2ea466f3f2e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `985b20b6889016b2f74ed0116d1feeb8cdd4c1991890aba8f45bf9a56d20b213` |
| V5 | `af142e5f93ead054a816587363c90e6a3df79fba0aca29fa36fe56957375745e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| V6a | `11e8fa92995dfb8869643a25f3553054ac8dd89f5d847170be63b2ea466f3f2e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `f7e395a2beb6310cd4e4ec92ac93445ff99b00b9046dd69e723bfd5c9e1e86fb` |
| V6b | `11e8fa92995dfb8869643a25f3553054ac8dd89f5d847170be63b2ea466f3f2e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `148d6100faac38e96402968be0ad051657817e346176b6b6e28799c4ab4ee45f` |
| V6c | `11e8fa92995dfb8869643a25f3553054ac8dd89f5d847170be63b2ea466f3f2e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `bec7d39b12235ee124af0b293d69d3fa5a5885e9ec16cdfc8c616039e7f65fc1` |
| V7a | `11e8fa92995dfb8869643a25f3553054ac8dd89f5d847170be63b2ea466f3f2e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `985b20b6889016b2f74ed0116d1feeb8cdd4c1991890aba8f45bf9a56d20b213` |
| V7b | `11e8fa92995dfb8869643a25f3553054ac8dd89f5d847170be63b2ea466f3f2e` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `985b20b6889016b2f74ed0116d1feeb8cdd4c1991890aba8f45bf9a56d20b213` |
| V2r | `906d0523d2953466c70a497e89b8e67c805240474a057f8f5b5d3bf29121a75b` | `088dea5e7c79c21b2ec30181773901e170d170de8843448b62cc589402733ce7` | `9d15d117d4498411dc7103c140435c2fd27ea37b92e41b31ba0ba6335da4f16f` | `7e9e5572e9ffd7b02417e3d67a37a0d1aaa6f368f9d917b136aac9213a310154` |

Entry and lesson SHA-256:

| Control | Entry | Lesson | Snapshot |
|---|---|---|---|
| V7a | `b4433744d7b5dab9e1821990c4b3c236d82b3c68185281b2726fdce40fa3841c` | `b1bc89db9e9cd8e1fa186aee62e8abc57822ac9b611db3520b8817f80cef3c86` | `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99` |
| V7b | `b4433744d7b5dab9e1821990c4b3c236d82b3c68185281b2726fdce40fa3841c` | `cebb063aa50f146fc52fc7703a2c4d1175006f518bf9738ecdcbc31e2f599fdc` | `4cbcd9ab82d4d4b81046f52b6c0703cdee2249b89a199faeefd3ecb7537f1f76` |

## Reading the findings against v2

- The frozen counter checks declaration anchoring separately at lines 249–251, not as a prerequisite for the individual oracle bits at lines 260–270. Thus external/handwritten inputs can light those bits without meeting the complete predicate at lines 302–303.
- Manifest validation rejects parent traversal, absolute paths and link nodes at lines 124–132. All three isolated V6 controls report `fixture=invalid` and zero oracle runs.
- Entry checking at lines 277–284 intentionally checks source/count/registry markers, not prose quality; the amended contract explicitly leaves prose quality to review. The V7 entry finding is therefore a bounded discrimination result, not a newly asserted contract violation.
- Quote checking at lines 286–297 fixes the snapshot digest and requires 8–25 words including “minimal.” The authentic three-word title and self-consistent rewritten snapshot each fail the measured bit.

No code, counter, predicate or claim was repaired or re-scoped by this control probe.
