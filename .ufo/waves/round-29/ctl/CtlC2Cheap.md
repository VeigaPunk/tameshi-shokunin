# C2 cheap controls — frozen round 29 counter
## Scope and result

All seven scored controls returned `C2_F6_PASS=false` (exit 1). **No cheap control reached PASS=true.** This is control evidence, not admission or a claim judgment.

Axes: counter discrimination; fixture specificity; source binding; scratch isolation; exact restoration.

Only the private clone was mutated. Kagi was read-only at `fecee8743e52eb8fb5fbb40782934cb619a1a96e`; no sibling source, lane index, jj state, or fleet-root file was written. No seat or other agent runtime was invoked. The only lane write is this report.

Counter frozen from A before edits: `/tmp/CtlC2Cheap-c2.py`

- A: `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`
- Counter SHA-256 before and after: `49173c02c663af8b4196bd166430252c7699fc5cba25d703091b821d80299694`
- Pinned gate SHA-256 before and after: `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`
- S024 snapshot SHA-256: `3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99`

## Build and detector reproduction

Setup commands (all exited 0):

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
timeout 300 mkdir -p /fast/scratch/hyaku
timeout 300 git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
```

The following short Python helper reproduces the exact per-control file bytes and bounded command sequence. Save it outside the lane, append the desired `build(...)` call below, and run it with `timeout 300 python3 SCRIPT`. The counter is never edited. Commit hashes can differ when replayed because of commit timestamps. Each control starts from A, not the preceding control.

```python
import os, pathlib, subprocess
A = "9f3084bc60ad56aac01e4556ef4c7653df2f65e5"
R = "/fast/scratch/hyaku/tameshi-r29-CtlC2Cheap"
C = "/tmp/CtlC2Cheap-c2.py"
env = {k: v for k, v in os.environ.items()
       if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
def run(*args, check=True):
    return subprocess.run(["timeout", "300", *args], cwd=R, env=env,
                          timeout=300, check=check)
# Freeze before making any control edits.
frozen = subprocess.run(["timeout", "300", "git", "-C", R, "show",
    A + ":.ufo/evidence/round-29/c2-measure.py"], env=env,
    capture_output=True, check=True, timeout=300).stdout
pathlib.Path(C).write_bytes(frozen)
def build(control, files):
    run("git", "-C", R, "checkout", "-q", "--detach", A)
    # These paths are absent at A; do not touch any other paths.
    for rel, text in files.items():
        p = pathlib.Path(R) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    if files:
        run("git", "-C", R, "add", "--", *files.keys())
    message = "control " + control
    if control == "C2-K1":
        message += ": unchanged A tree"
    run("git", "-C", R, "-c", "user.name=ctl", "-c", "user.email=ctl@x",
        "commit", "-q", "--allow-empty", "-m", message)
    p = run("python3", C, "--repo", R, "--rev", "HEAD", check=False)
    print("COUNTER_EXIT=" + str(p.returncode))
```

The scored command for every pristine/control/restored measurement was:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /tmp/CtlC2Cheap-c2.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap --rev HEAD
```

## Pristine baseline at A

Full counter stdout:

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

For the mutation-tester classification, a baseline failure cannot establish a killed mutant: the pristine-versus-mutated-versus-restored comparison is **inconclusive as a kill test**. The separate control verdict below records only whether each control met the frozen PASS predicate.

## C2-K1

Do nothing: an empty commit preserves A exactly.

**Expected detector:** Expect fixture=absent and PASS=false.

Build:

```python
build('C2-K1', {})
```

Commit: `1c051b5f5bab3019cc6197f9566f0f114496e4ec`

Full counter stdout:

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=1c051b5f5bab3019cc6197f9566f0f114496e4ec
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K1: meets=no

## C2-K2

Junk: one deterministic random line in each TSV and two random host files. Random seed 2902; exact bytes below.

**Expected detector:** Expect no B5 kill and PASS=false; malformed rows are not survivor evidence.

Build:

```python
build('C2-K2', {'.ufo/evidence/round-29/f6/minimized/census.tsv': 'o9nr0t9i488l8d6h5s07js8xjfkfschh\n', '.ufo/evidence/round-29/f6/minimized/shapes.tsv': 'grv59ka6ep9kaignq39hpfx2i7wogi7s\n', '.ufo/evidence/round-29/f6/minimized/baseline.tsv': 'eps8wyj876j9lxsn6ealgzuen7fmhufg\n', '.ufo/evidence/round-29/f6/minimized/host/junk-a.txt': '5dbbmatu4sb7f0jvx119sga0z1flnn8h\n', '.ufo/evidence/round-29/f6/minimized/host/junk-b.txt': '0bozq51nsuyb5am7buw5kjggx89ldyck\n'})
```

Commit: `1b94c014d7ff4b1a305eebd7a96059b94a61b551`

Full counter stdout:

```text
C2_F6: fixture=present kill=0 units=5 one_minimal=0 entry_sourced=0 quote_located=0 rev=1b94c014d7ff4b1a305eebd7a96059b94a61b551
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K2: meets=no

## C2-K3

All false: three zero-byte TSV files, with only a zero-byte host/.keep to retain the directory.

**Expected detector:** Expect no B5 kill and PASS=false. The .keep counts as one host-file unit.

Build:

```python
build('C2-K3', {'.ufo/evidence/round-29/f6/minimized/census.tsv': '', '.ufo/evidence/round-29/f6/minimized/shapes.tsv': '', '.ufo/evidence/round-29/f6/minimized/baseline.tsv': '', '.ufo/evidence/round-29/f6/minimized/host/.keep': ''})
```

Commit: `5430a4a3963e6c040e36ff73c57cabbada837231`

Full counter stdout:

```text
C2_F6: fixture=present kill=0 units=1 one_minimal=0 entry_sourced=0 quote_located=0 rev=5430a4a3963e6c040e36ff73c57cabbada837231
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K3: meets=no

## C2-K4

Wrong reason: an asset/file row declares a nonexistent file. No row declares exec; this fixture cannot exercise the exec x-bit arm.

**Expected detector:** Expect the pristine gate to exit 1 with SURFACE GONE, not the exec diagnostic; the counter must report kill=0 and PASS=false.

Build:

```python
build('C2-K4', {'.ufo/evidence/round-29/f6/minimized/census.tsv': '$HOME/missing-declared-file\tasset\tfile\t-\twrong-reason control\n', '.ufo/evidence/round-29/f6/minimized/shapes.tsv': '', '.ufo/evidence/round-29/f6/minimized/baseline.tsv': '', '.ufo/evidence/round-29/f6/minimized/host/.keep': ''})
```

Commit: `3dcb7727ea161b1cd58029adc1379e57c932a85a`

Full counter stdout:

```text
C2_F6: fixture=present kill=0 units=2 one_minimal=0 entry_sourced=0 quote_located=0 rev=3dcb7727ea161b1cd58029adc1379e57c932a85a
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K4: meets=no

### Wrong-reason behavioral witness

The unmodified pinned gate was copied to `/tmp/CtlC2Cheap-surface-census.sh` using `git show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh` from kagi. Only gate lines 60–100, 103–179 (row syntax), and 180–260 were inspected.

With an isolated temporary HOME, PATH inherited, LC_ALL=C, TZ=UTC, and cwd in that temporary directory:

```sh
timeout 300 bash /tmp/CtlC2Cheap-surface-census.sh verify --root /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap/.ufo/evidence/round-29/f6/minimized/host --census /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap/.ufo/evidence/round-29/f6/minimized/census.tsv --shapes /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap/.ufo/evidence/round-29/f6/minimized/shapes.tsv --baseline /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap/.ufo/evidence/round-29/f6/minimized/baseline.tsv
```

Full gate stdout:

```text
SURFACE GONE     $HOME/missing-declared-file (file expected)
SURFACE_CENSUS: DRIFT (diverged=0 gone=1 link=0 unlisted=0 crosscheck=0 shape=0 unverified=0 ok=0 absent=0 skipped=0)
```

Gate exit: `1`. Stderr: empty. This proves a missing-file failure (`gone=1`, `diverged=0`), not an exec x-bit failure. The frozen counter rejects it (`kill=0`).

## C2-K5a

No fixture. A source-only entry cites S024; its lesson names the correct snapshot hash but quotes fabricated text absent from the page.

**Expected detector:** Expect entry_sourced=1, quote_located=0, and PASS=false.

Build:

```python
build('C2-K5a', {'corpus/knowledge/survivor-fixture-minimization.md': 'source: S024\n', 'corpus/lessons/round-29.md': 'S024 sha256=3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99 "CtlC2Cheap fabricated quote absent from the frozen reducer page."\n'})
```

Commit: `cefc02456f2645e014805919e26b2fc289955707`

Full counter stdout:

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=1 quote_located=0 rev=cefc02456f2645e014805919e26b2fc289955707
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K5a: meets=no

## C2-K5b

No fixture. A source-only entry cites S024; its lesson quotes a real page sentence but names the wrong hash (64 zeroes).

**Expected detector:** Expect entry_sourced=1, quote_located=0, and PASS=false.

Build:

```python
build('C2-K5b', {'corpus/knowledge/survivor-fixture-minimization.md': 'source: S024\n', 'corpus/lessons/round-29.md': 'S024 sha256=0000000000000000000000000000000000000000000000000000000000000000 "Delta Debugging is a simple and robust reduction algorithm."\n'})
```

Commit: `6b9dbe8a8c6d6e82fbf778b1e5ca9115c6301b34`

Full counter stdout:

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=1 quote_located=0 rev=6b9dbe8a8c6d6e82fbf778b1e5ca9115c6301b34
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K5b: meets=no

## C2-K5c

No fixture. The entry cites S022 instead of S024; the lesson retains S024, the correct hash, and the real quote to isolate the entry-source check.

**Expected detector:** Expect entry_sourced=0, quote_located=1, and PASS=false.

Build:

```python
build('C2-K5c', {'corpus/knowledge/survivor-fixture-minimization.md': 'source: S022\n', 'corpus/lessons/round-29.md': 'S024 sha256=3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99 "Delta Debugging is a simple and robust reduction algorithm."\n'})
```

Commit: `aadbefb7c1cc1e6166ba9ece33997f62dcf65b4b`

Full counter stdout:

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=0 quote_located=1 rev=aadbefb7c1cc1e6166ba9ece33997f62dcf65b4b
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty.

CONTROL C2-K5c: meets=no

CONTROL C2-K5: meets=no

## Source shortcut observations

| Control | entry_sourced | quote_located | Fixture | PASS |
|---|---:|---:|---|---|
| C2-K5a fabricated quote | 1 | 0 | absent | false |
| C2-K5b wrong hash | 1 | 0 | absent | false |
| C2-K5c wrong entry source | 0 | 1 | absent | false |

`entry_sourced=1` alone is syntactic: the 13-byte `source: S024` entry suffices because A already marks S024 mined and names the entry in used-by. That is a limited no-reader observation, not a full-predicate bypass. The quote check rejected both fabricated text and a wrong digest. A valid S024 lesson quote did not compensate for an S022 entry or a missing fixture.

## Before, control, and restored hashes

The tree ID binds all committed modes, paths, and bytes. Manifest SHA-256 is computed over the exact binary output of `timeout 300 git -C CLONE ls-tree -rz REV`; it also binds all mode/path/blob identities. No counter or gate bytes changed.

| State | Commit | Git tree | Manifest SHA-256 |
|---|---|---|---|
| baseline-A | `9f3084bc60ad56aac01e4556ef4c7653df2f65e5` | `ab7481598027f2dc5195ec52af4c6b8bca4182a9` | `9b9fb10742d20385b552a44688b5d54c4ed3fa9cbee520b69f41d4a11643573c` |
| C2-K1 | `1c051b5f5bab3019cc6197f9566f0f114496e4ec` | `ab7481598027f2dc5195ec52af4c6b8bca4182a9` | `9b9fb10742d20385b552a44688b5d54c4ed3fa9cbee520b69f41d4a11643573c` |
| C2-K2 | `1b94c014d7ff4b1a305eebd7a96059b94a61b551` | `2fb14ceed6cf3b53d0faf60d49c152bb1a2a1046` | `c69517ccd726aa6508765e2cec787f009461aef179189fcada1343f77cf5b70e` |
| C2-K3 | `5430a4a3963e6c040e36ff73c57cabbada837231` | `d1d352654c06bdfecd3101bb97c7ec324cc35a28` | `23307709c73028af8de9457b6e3104eb6bc055b4b7218a4cf3a54262006ca3f1` |
| C2-K4 | `3dcb7727ea161b1cd58029adc1379e57c932a85a` | `9a685a3d860078d957fecb059927e48725b376b9` | `80110b810f11c8749604cb65813dbbe8e5308d3a0d81cb3c1f5ed67ec46338d3` |
| C2-K5a | `cefc02456f2645e014805919e26b2fc289955707` | `a6659120eeaba2369c1abe4493b5c6fa2fa3c16f` | `674aa97e0b40fffb5f3b19880d108b874793066b90f56d248ff73bee374aec60` |
| C2-K5b | `6b9dbe8a8c6d6e82fbf778b1e5ca9115c6301b34` | `e826d8a1fb4605326e47bdefbba6e2d1a527655e` | `47df275e89f7de2324bbb55484b9fda01ad888935fa8405ceb596035ed48e8c9` |
| C2-K5c | `aadbefb7c1cc1e6166ba9ece33997f62dcf65b4b` | `1deffe8469f33c5c681dc8212e2bf289ac41ec6a` | `27d3f47504595a049f0fdba6c26f454cb2603f16b9b3dbd98e7822d22ee7ab31` |
| restored-A | `9f3084bc60ad56aac01e4556ef4c7653df2f65e5` | `ab7481598027f2dc5195ec52af4c6b8bca4182a9` | `9b9fb10742d20385b552a44688b5d54c4ed3fa9cbee520b69f41d4a11643573c` |

## Exact restoration

After scoring C2-K5c, the clone was restored with:

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
```

Checkout exit: `0`; stdout and stderr empty. Restored HEAD is exactly A. Its tree and manifest hashes equal the pristine hashes in the table.

Additional working-byte evidence (each exit `0`, stdout and stderr empty):

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap diff --quiet 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC2Cheap ls-files --others --exclude-standard
```

The same frozen detector was then run on restored bytes. Full stdout:

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C2_F6_PASS=false
```

Counter exit: `1`. Stderr: empty. This matches the pristine baseline exactly.

Final frozen-byte hash command:

```sh
timeout 300 sha256sum /tmp/CtlC2Cheap-c2.py /tmp/CtlC2Cheap-surface-census.sh
```

Full stdout (exit `0`; stderr empty):

```text
49173c02c663af8b4196bd166430252c7699fc5cba25d703091b821d80299694  /tmp/CtlC2Cheap-c2.py
275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f  /tmp/CtlC2Cheap-surface-census.sh
```

All launched commands were synchronous, bounded by `timeout 300`, and returned; no background job or service was launched. The counter independently bounds each gate run with `timeout 60`. No timeout exit was observed. Temporary gate HOME was removed after use. Control commits remain only in this private clone; its checkout is restored to A.

Tool installs or updates: none.

## Verdict

Controls C2-K1, C2-K2, C2-K3, C2-K4, C2-K5a, C2-K5b, and C2-K5c all failed to meet the frozen claim predicate. No killed-mutant claim is made from the already-failing pristine claim counter. No contract, counter, production source, or acceptance criterion was changed.
