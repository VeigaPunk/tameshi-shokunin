# C2 design review — round 29 control wave

## Scope and axes

Reviewed frozen lane commit **A = `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`** in private clone `/fast/scratch/hyaku/tameshi-r29-CriticC2Design`. All lane-relative citations below refer to A. Kagi citations refer to `fecee8743e52eb8fb5fbb40782934cb619a1a96e`, read with `git show`, not its current worktree. The axes under attack are **coverage** (does F6 acquire a new governed method?), **depth / operability** (does the fixture establish technical, reproducible reduction knowledge?), and **calibration** (does the receipt overstate what its predicate measures?). Quality is a learning trend, not a seventh axis (`AXES.md:9-23`, fleet root).

**Decisive finding: the unchanged frozen counter returns `C2_F6_PASS=true` for a no-reader handwritten fixture with nonsense knowledge, a fabricated source, an aliased host, and a one-unit fixture with no host file.** These are counter findings, not an admission decision. I did not invoke a judge, change the contract/counter, integrate a fix, or edit production files.

## Six question verdicts

### 1. Predicate identity: yes for contract, counter documentation and label; the README promises more

The contract predicate at `.ufo/evidence/round-29/contract.json:29` equals the counter docstring at `c2-measure.py:6-18` after removing Markdown backticks and normalizing whitespace. The comparison printed `contract_vs_doc_predicate_equal=True`. The label is `C2_F6_PASS` in `contract.json:28,31` and `c2-measure.py:206-208`. The Boolean conjunction implements present fixture, kill, one-minimal, source marker/row, and located quote (`c2-measure.py:164-178,182-208`).

However, `corpus/README.md:440-447` promises a probe **reduced by delta debugging**. Neither an initial larger fixture, a reduction operation, a size decrease nor a reduction trace is required by the predicate. `contract.json:35` explicitly allows a handwritten fixture and relegates a trace to method evidence. DESIGN-D2 passes while its entry literally says no reduction was performed. Thus literal predicate identity is not proof that the README's method claim is measured.

Smallest safe correction: before any data work, make the method promise and predicate agree, preserving A and these receipts. Do not retrospectively describe a handwritten witness as measured delta debugging.

### 2. Axis fit: F6 can name a coverage surface, but this predicate does not establish that move

The named frontier is real: `corpus/README.md:83` says F6 is fixture minimization, with the next move “unmeasured → reduced size + kill check.” The domain owns reusable craft, not a sibling gate's product behavior (`PROVINCE.md:3-17,40-42`). A newly demonstrated reduction operation could therefore be a bounded coverage move.

But the underlying B5 witness is already held: `corpus/knowledge/mutation-case-kagi-census.md:107-116` records the exact `asset exec -`, non-executable-file differential and both outcomes. DESIGN-D2 reproduces that known witness, adds no reduction method, supplies no useful sourced knowledge, and still passes. The counter's absence-of-file baseline is not an enumeration of a newly governed method. This is the precise quality-work failure mode of the round prompt at fleet `.ufo/prompts/tameshi-round-29.md:361-365`.

As measured, the defensible surface is quality work on an existing probe (potentially depth or operability if real technical knowledge or a runnable method is added), not established coverage of F6. This is a claim-fit issue for the canonical judge, not merely a label typo I can repair.

Smallest safe correction: retain coverage only if a real, source-supported minimization method is demonstrated and its absence is detected. Otherwise size and classify a new claim honestly; the current no-reader positive must not become coverage credit by renaming it.

### 3. One-minimality: a real local property, but trivial and identity-unsafe here

`c2-measure.py:67-77` counts TSV lines plus files found by `os.walk(host)`. It does not count directories or the `host` link itself. `:80-92` removes a named unit, and `:170-178` accepts one-minimality when no single deletion preserves the differential.

For an honest fixture, one census line plus one non-executable regular host file already satisfies the property (DESIGN-D2: two units). No reduction work is necessary. That is not a mathematical error: `contract.json:35` expressly allows handwritten witnesses and says line-internal bytes are outside the unit model. It is insufficient evidence for the stronger method claim.

The strongest concrete defect is **DESIGN-D7**: census is only `/etc/hostname<TAB>asset<TAB>exec<TAB>-<TAB>external`, shapes and baseline are empty, and `host` is a symlink to an empty private scratch directory. The counter reports **units=1, kill=1, one_minimal=1, PASS=true** with no host file. The gate only stats `/etc/hostname`; it does not read its contents. Absolute target paths are accepted by kagi `corpus/surface-census.sh:123-127`; `:130-138,184-217` tests the real path without containment. The counter only asks `isdir(host)`, which follows the symlink (`c2-measure.py:106-112`), and preserves links when copying (`:80-84`). The target is outside the declared unit set.

DESIGN-D6 is an independent identity counterexample: `host -> .` and census `$HOME/census.tsv<TAB>asset<TAB>exec<TAB>-<TAB>self` pass with four units. The three required TSV input files are recounted as “host files”; deleting empty shapes/baseline destroys a required-input precondition rather than any substantive host evidence. The same objects acquire duplicate authorities.

The naive empty-directory version, DESIGN-D3, did **not** pass. A committed empty host tree is omitted by `git archive`; I inspected the archive members and `host` was absent. This is why I do not claim that any one-line missing-file fixture passes: a missing declared executable produces GONE, not the required exec-bit DIVERGED (`kagi ...:190-217`). D7 is the measured successful no-host-file construction.

Smallest safe correction: require a real non-symlink host directory and an actual committed regular target beneath it after canonical path resolution; reject absolute/escaping targets and aliases to the three required input files. Count object identities once. Separately, require an initial larger witness and replayable reduction if the claim remains about minimization rather than existence of a small witness.

### 4. Quote discrimination: no; authentic off-topic and fabricated sources both pass

Entry checking only requires a `source:` line containing `S024` and the already-mined registry row (`c2-measure.py:182-188`; `corpus/SOURCES.md:35`). It reads no methodological assertion in the entry. Quote checking recomputes the digest of whatever snapshot is at REV, then accepts any nonempty quote of up to 25 words occurring anywhere in its normalized text (`c2-measure.py:190-202`). It does not compare that digest with the frozen source identity in `contract.json:34`, require the registered URL/section, or connect the quote to the entry's claim.

DESIGN-D2 keeps the authentic A snapshot unchanged, quotes only **“The Fuzzing Book”**, and adds the entry:

```text
source: S024

Bananas are triangular. No reduction was performed.
```

It passes. This alone demonstrates the no-reader/off-topic defect while respecting the contract's post-A add-only input ordering.

DESIGN-D4b additionally replaces the snapshot with `<html><body>Bananas are triangular.</body></html>` and cites its self-computed digest plus “Bananas are triangular.” It also passes. That replacement violates the declared add-only ordering (`contract.json:39`), so it is specifically evidence that the **quote checker** fails fabrication and does not enforce frozen provenance, not a claim that the complete contract permits snapshot replacement. The valid-additions-only D2 finding does not depend on this distinction.

A's actual source contains precise-error preservation at snapshot line 12075 and the character-level 1-minimality explanation at 13023. The counter requires neither. A generic title match is not evidence of learning either proposition.

Smallest safe correction: enforce A's declared snapshot digest, then require a located supporting passage and bounded method assertions that fabricated/off-topic negatives fail. Merely adding more source identifiers or requiring a longer arbitrary quotation does not fix relevance.

### 5. B5 construction: yes on these frozen bytes

The runner's B5 spec is `tools/mutate-and-run.sh:717-719`; it removes the exec-bit arm of the pinned gate. Its decoder supports exactly `\\n`, `\\t`, `\\r`, and `\\\\` (`:318-342`) and the apply operation requires one old occurrence (`:410-431`). The counter decoder and replacement are at `c2-measure.py:54-64`.

I decoded the actual embedded bash-surface-census spec using the runner helper's own definitions, compared its byte replacement with the counter's result, and observed:

```text
runner_B5_old_count=1
counter_B5_equals_runner=True
B5_sha256=1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c
```

The pristine digest was `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, matching `tools/mutate-and-run.sh:605-606`. There is no demonstrated B5 mutation-identity defect at A. The regex helper is not a complete substitute for the runner parser on malformed or rearranged future specs, but that is not the current counterexample.

Smallest safe correction: none required to the current B5 edit. Reusing the existing decoder would remove a duplicate authority if this becomes maintained tooling; do not confuse that maintenance choice with a present bad mutant.

### 6. Environment: partly normalized, not hermetic; janitor is irrelevant and sqlite is branch-dependent

`c2-measure.py:95-103` replaces the gate environment with inherited PATH, a fresh scratch HOME, `LC_ALL=C`, and `TZ=UTC`; it passes `verify` and an explicit fixture root. This usefully removes ambient locale/timezone/HOME variation and does not pass through `SQLITE3_BIN` or `THE_JANITOR_BIN`. It does **not** freeze PATH or executable identities. Git and the default kagi checkout are also external dependencies (`:44-46,126,134-147`); missing pinned objects correctly produce exit 2, not a passing result.

Missing **the-janitor does not affect this verify-mode counter**: its availability check is inside `verbs()` at kagi `corpus/surface-census.sh:465-469`, while verify dispatch is `:852-857`. Missing **sqlite3 matters only when a present SQLite shape needs tables/rows probing** (`:265-269,389-408`); it then becomes UNVERIFIED and fails closed. Empty shapes need neither tool.

DESIGN-D5b scored the genuine D2 control with a PATH containing only symlinks to `git`, `timeout`, `bash`, `dirname`, `stat`, `grep`, and `rm`. Neither `the-janitor` nor `sqlite3` is resolvable there. It still passes with exactly the same two units. This rules out a supposed janitor/sqlite prerequisite for the minimal honest B5 fixture, but does not establish invariance across other core-tool versions. D7 separately proves dependence on an undeclared host file's existence/mode.

Smallest safe correction: fix the fixture containment problem and declare/pin the actual verify-path tool environment instead of inheriting arbitrary PATH. Do not introduce unnecessary live janitor execution or install sqlite solely for an empty-shapes B5 witness.

## Counter receipts

Counter bytes were copied from A **before any control commit** to `/tmp/CriticC2Design-c2.py`; SHA-256 is `49173c02c663af8b4196bd166430252c7699fc5cba25d703091b821d80299694`, exactly the frozen contract value. C1 was also copied, but was not scored in this C2 design assignment. No counter, runner or contract bytes were altered.

Each control is an independent direct child of A in my private clone, except D0 which is A and environment-only controls which reuse the stated commit. Git tree plumbing was used only in this private clone to represent the failed empty-directory controls without adding a placeholder host file. No lane Git index or jj state was touched.

Common score command (at each stated private HEAD):

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  python3 /tmp/CriticC2Design-c2.py \
  --repo /fast/scratch/hyaku/tameshi-r29-CriticC2Design --rev HEAD
```

All counter stderr streams below were empty. All stdout is pasted in full. `meets` means only the frozen C2 predicate, not canonical claim admission.

### DESIGN-D0-do-nothing

Built nothing; HEAD is frozen A.

Commit: `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`.

```text
C2_F6: fixture=absent kill=0 units=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C2_F6_PASS=false
```

Exit code: `1`.

CONTROL DESIGN-D0-do-nothing: meets=no

### DESIGN-D1-junk-all-false

Added census `junk`, empty shapes/baseline and empty host tree, with the nonsense sourced entry and generic authentic title quote. The actual interestingness flags remain false.

Commit: `c0fc3207bc2f36bcb6e6d8462ead2128474886dc`.

```text
C2_F6: fixture=present kill=0 units=1 one_minimal=0 entry_sourced=1 quote_located=1 rev=c0fc3207bc2f36bcb6e6d8462ead2128474886dc
PREDICATE: C2_F6_PASS=false
```

Exit code: `1`.

CONTROL DESIGN-D1-junk-all-false: meets=no

### DESIGN-D2-no-reader-handwritten

Handwrote one `$HOME/p` asset/exec/unchecked-mode census row and one non-executable host/p file. Empty shapes/baseline; nonsense entry; authentic title quote. No reduction or methodological reading is represented.

Commit: `af694c1df7885487456c258f9a238d4dd377e9f3`.

```text
C2_F6: fixture=present kill=1 units=2 one_minimal=1 entry_sourced=1 quote_located=1 rev=af694c1df7885487456c258f9a238d4dd377e9f3
PREDICATE: C2_F6_PASS=true
```

Exit code: `0`.

CONTROL DESIGN-D2-no-reader-handwritten: meets=yes

### DESIGN-D3-one-line-no-host-file

Used `$HOME/../census.tsv` as the executable target, with empty shapes/baseline and an empty Git host tree. Archive omission of the empty host makes this fail.

Commit: `0e7b03cf8b3a3fdcb606e2efd273f207940abab1`.

```text
C2_F6: fixture=present kill=0 units=1 one_minimal=0 entry_sourced=1 quote_located=1 rev=0e7b03cf8b3a3fdcb606e2efd273f207940abab1
PREDICATE: C2_F6_PASS=false
```

Exit code: `1`.

CONTROL DESIGN-D3-one-line-no-host-file: meets=no

### DESIGN-D4-fabricated-off-topic-source

D3 plus the fabricated banana snapshot and matching digest/quote. Source flags pass, but the missing archived host still prevents a kill.

Commit: `589773818fae14793c0ccd8aabb1ad02f4e249b1`.

```text
C2_F6: fixture=present kill=0 units=1 one_minimal=0 entry_sourced=1 quote_located=1 rev=589773818fae14793c0ccd8aabb1ad02f4e249b1
PREDICATE: C2_F6_PASS=false
```

Exit code: `1`.

CONTROL DESIGN-D4-fabricated-off-topic-source: meets=no

### DESIGN-D5-no-janitor-no-sqlite3

Scored the failing D4 tree under the sparse PATH. This initial probe is confounded by its missing host; D5b below isolates the environment on D2.

Commit: `589773818fae14793c0ccd8aabb1ad02f4e249b1`.

```text
C2_F6: fixture=present kill=0 units=1 one_minimal=0 entry_sourced=1 quote_located=1 rev=589773818fae14793c0ccd8aabb1ad02f4e249b1
PREDICATE: C2_F6_PASS=false
```

Exit code: `1`.

CONTROL DESIGN-D5-no-janitor-no-sqlite3: meets=no

### DESIGN-D4b-fabricated-off-topic-source

D2 with a proper real host/p file, but replaced source snapshot and quote with the banana fabrication. This isolates source discrimination from D3's missing-host failure.

Commit: `109fe613b52cf6fdc1a60564e7439cdcd5ac09b4`.

```text
C2_F6: fixture=present kill=1 units=2 one_minimal=1 entry_sourced=1 quote_located=1 rev=109fe613b52cf6fdc1a60564e7439cdcd5ac09b4
PREDICATE: C2_F6_PASS=true
```

Exit code: `0`.

CONTROL DESIGN-D4b-fabricated-off-topic-source: meets=yes

### DESIGN-D6-host-alias

Starting from D2, replaced host with symlink `.` and census target with `$HOME/census.tsv`. No distinct host payload remains; the input TSVs are counted again as host files.

Commit: `8517d1efa33ab7e69b9941d45d260bd5202ffc83`.

```text
C2_F6: fixture=present kill=1 units=4 one_minimal=1 entry_sourced=1 quote_located=1 rev=8517d1efa33ab7e69b9941d45d260bd5202ffc83
PREDICATE: C2_F6_PASS=true
```

Exit code: `0`.

CONTROL DESIGN-D6-host-alias: meets=yes

### DESIGN-D7-one-unit-external-target

Starting from D2, replaced host with a symlink to empty `/tmp/CriticC2Design-empty-host`, and census with the one external `/etc/hostname` asset/exec row. No file exists under host. Only metadata of /etc/hostname is consulted.

Commit: `9ea4f2dfd6e61b02949ca7039741c5af88853c21`.

```text
C2_F6: fixture=present kill=1 units=1 one_minimal=1 entry_sourced=1 quote_located=1 rev=9ea4f2dfd6e61b02949ca7039741c5af88853c21
PREDICATE: C2_F6_PASS=true
```

Exit code: `0`.

CONTROL DESIGN-D7-one-unit-external-target: meets=yes

### DESIGN-D5b-no-janitor-no-sqlite3

Scored the passing D2 commit under the sparse PATH, excluding both janitor and sqlite3. No fixture/source changes.

Commit: `af694c1df7885487456c258f9a238d4dd377e9f3`.

```text
C2_F6: fixture=present kill=1 units=2 one_minimal=1 entry_sourced=1 quote_located=1 rev=af694c1df7885487456c258f9a238d4dd377e9f3
PREDICATE: C2_F6_PASS=true
```

Exit code: `0`.

CONTROL DESIGN-D5b-no-janitor-no-sqlite3: meets=yes

## Exact construction recipe

The initial setup was:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE sh -c '
  mkdir -p /fast/scratch/hyaku &&
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r29-CriticC2Design &&
  git -C /fast/scratch/hyaku/tameshi-r29-CriticC2Design checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 &&
  cp /fast/scratch/hyaku/tameshi-r29-CriticC2Design/.ufo/evidence/round-29/c1-measure.py /tmp/CriticC2Design-c1.py &&
  cp /fast/scratch/hyaku/tameshi-r29-CriticC2Design/.ufo/evidence/round-29/c2-measure.py /tmp/CriticC2Design-c2.py'
```

The following is the actual initial script, saved as `/tmp/CriticC2Design-controls.py` and run as `timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /tmp/CriticC2Design-controls.py`. Its commits use the authorized ctl identity; all Git writes address only REPO. Commit hashes include creation times, so rebuilding yields equivalent new hashes rather than promising identical identifiers.

```python
#!/usr/bin/env python3
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

REPO = '/fast/scratch/hyaku/tameshi-r29-CriticC2Design'
A = '9f3084bc60ad56aac01e4556ef4c7653df2f65e5'
COUNTER = '/tmp/CriticC2Design-c2.py'
FX = '.ufo/evidence/round-29/f6/minimized'
ENTRY = 'corpus/knowledge/survivor-fixture-minimization.md'
LESSON = 'corpus/lessons/round-29.md'
SNAP = '.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


def git(*args, data=None):
    p = subprocess.run(['timeout', '300', 'git', '-C', REPO, *args],
                       input=data, capture_output=True, env=ENV)
    if p.returncode:
        raise RuntimeError((args, p.returncode, p.stderr.decode()))
    return p.stdout


def blob(data):
    return ('100644', 'blob', git('hash-object', '-w', '--stdin', data=data).decode().strip())


EMPTY = git('mktree', data=b'').decode().strip()


def graft(tree, changes):
    entries = {}
    for row in git('ls-tree', '-z', tree).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            entries[name.decode()] = tuple(meta.decode().split())
    groups = {}
    for path, value in changes.items():
        first, sep, rest = path.partition('/')
        if sep:
            groups.setdefault(first, {})[rest] = value
        else:
            entries[first] = value
    for name, inner in groups.items():
        old = entries.get(name, ('040000', 'tree', EMPTY))
        entries[name] = ('040000', 'tree', graft(old[2], inner))
    payload = b''.join(('%s %s %s\t%s\0' % (*value, name)).encode()
                       for name, value in sorted(entries.items()))
    return git('mktree', '-z', data=payload).decode().strip()


snap = git('show', A + ':' + SNAP)
sha = hashlib.sha256(snap).hexdigest()
results = []


def score(label, env=ENV):
    p = subprocess.run(['timeout', '300', '/usr/bin/python3', COUNTER,
                        '--repo', REPO, '--rev', 'HEAD'],
                       capture_output=True, text=True, env=env)
    result = {'control': label, 'head': git('rev-parse', 'HEAD').decode().strip(),
              'stdout': p.stdout, 'stderr': p.stderr, 'exit': p.returncode,
              'meets': p.returncode == 0}
    results.append(result)
    print(json.dumps(result), flush=True)
    return result


def commit_control(label, census, real_host, fabricated=False):
    source = b'<html><body>Bananas are triangular.</body></html>\n' if fabricated else snap
    quote = 'Bananas are triangular.' if fabricated else 'The Fuzzing Book'
    changes = {
        FX + '/census.tsv': blob(census),
        FX + '/shapes.tsv': blob(b''),
        FX + '/baseline.tsv': blob(b''),
        FX + '/host': ('040000', 'tree', EMPTY),
        ENTRY: blob(b'source: S024\n\nBananas are triangular. No reduction was performed.\n'),
        LESSON: blob(('S024 sha256=' + hashlib.sha256(source).hexdigest()
                     + ' "' + quote + '"\n').encode()),
    }
    if real_host:
        changes[FX + '/host/p'] = blob(b'x\n')
    if fabricated:
        changes[SNAP] = blob(source)
    root = git('rev-parse', A + '^{tree}').decode().strip()
    tree = graft(root, changes)
    rev = git('-c', 'user.name=ctl', '-c', 'user.email=ctl@x',
              '-c', 'commit.gpgsign=false', 'commit-tree', tree, '-p', A,
              '-m', 'CONTROL ' + label).decode().strip()
    git('update-ref', 'HEAD', rev)
    return score(label)


score('DESIGN-D0-do-nothing')
commit_control('DESIGN-D1-junk-all-false', b'junk\n', False)
commit_control('DESIGN-D2-no-reader-handwritten', b'$HOME/p\tasset\texec\t-\tprobe\n', True)
commit_control('DESIGN-D3-one-line-no-host-file', b'$HOME/../census.tsv\tasset\texec\t-\tself\n', False)
commit_control('DESIGN-D4-fabricated-off-topic-source', b'$HOME/../census.tsv\tasset\texec\t-\tself\n', False, True)

sparse = Path('/tmp/CriticC2Design-sparse-bin')
sparse.mkdir(exist_ok=True)
for name in ('git', 'timeout', 'bash', 'dirname', 'stat', 'grep', 'rm'):
    target = sparse / name
    if not target.exists():
        target.symlink_to(shutil.which(name))
sparse_env = dict(ENV, PATH=str(sparse))
score('DESIGN-D5-no-janitor-no-sqlite3', sparse_env)

Path('/tmp/CriticC2Design-controls-results.json').write_text(json.dumps(results, indent=2) + '\n')
```

The follow-on construction, using the same helper functions and bounded counter commands:

```python
import os

# Executed after the initial script; the helper prefix defines functions only.
ns = {'__name__': 'review_control_helpers'}
exec(compile(open('/tmp/CriticC2Design-controls.py').read().split(
    "score('DESIGN-D0-do-nothing')")[0], 'controls-helper', 'exec'), ns)
ns['commit_control']('DESIGN-D4b-fabricated-off-topic-source',
    b'$HOME/p\tasset\texec\t-\tprobe\n', True, True)
g = ns['git']
fx = ns['FX']
d2 = 'af694c1df7885487456c258f9a238d4dd377e9f3'  # actual D2 receipt above

def tree_control(label, changes):
    root = g('rev-parse', d2 + '^{tree}').decode().strip()
    tree = ns['graft'](root, changes)
    rev = g('-c', 'user.name=ctl', '-c', 'user.email=ctl@x',
        '-c', 'commit.gpgsign=false', 'commit-tree', tree, '-p', ns['A'],
        '-m', 'CONTROL ' + label).decode().strip()
    g('update-ref', 'HEAD', rev)
    return ns['score'](label)

link = ('120000', 'blob', g('hash-object', '-w', '--stdin', data=b'.').decode().strip())
tree_control('DESIGN-D6-host-alias', {
    fx + '/host': link,
    fx + '/census.tsv': ns['blob'](b'$HOME/census.tsv\tasset\texec\t-\tself\n')})
os.makedirs('/tmp/CriticC2Design-empty-host', exist_ok=True)
link = ('120000', 'blob', g('hash-object', '-w', '--stdin',
    data=b'/tmp/CriticC2Design-empty-host').decode().strip())
tree_control('DESIGN-D7-one-unit-external-target', {
    fx + '/host': link,
    fx + '/census.tsv': ns['blob'](b'/etc/hostname\tasset\texec\t-\texternal\n')})
g('update-ref', 'HEAD', d2)
ns['score']('DESIGN-D5b-no-janitor-no-sqlite3',
    dict(ns['ENV'], PATH='/tmp/CriticC2Design-sparse-bin'))

```

The extension ran synchronously with a 300-second cell bound; every external command it uses is independently wrapped in `timeout 300` by the helper. To replay an existing control, change only this private clone's HEAD with `timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r29-CriticC2Design update-ref HEAD <control hash>`, then run the common score command. For D7 create its empty scratch directory first. For D5/D5b set PATH to the sparse directory and invoke `/usr/bin/python3` as the actual recipe does.

## Smallest safe disposition

This review supplies counterexamples and prospective corrections, not a judge verdict. Preserve the frozen counter and these failed-control receipts as evidence. Before data, the integrator must resolve source discrimination, fixture identity/containment, and the mismatch between a handwritten witness and the declared reduction-method surface. B5 identity itself needs no repair. Accepting the present controls merely because the literal contract allows handwritten fixtures would be a claim-sizing tradeoff for the canonical judge, not something this critic may silently integrate or admit.

Tool installs or updates: **none**. No services or background jobs were started. All started subprocesses completed synchronously under bounds; no process tree remains running. Only this report was written in the lane.

## Three requested standalone replays

These use the private clone and unchanged A counter prepared above. They write no lane state. Each block prints the full counter stdout and its exit code.

No-reader control `af694c1df7885487456c258f9a238d4dd377e9f3`:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE sh -c '
  git -C /fast/scratch/hyaku/tameshi-r29-CriticC2Design update-ref HEAD af694c1df7885487456c258f9a238d4dd377e9f3 &&
  /usr/bin/python3 /tmp/CriticC2Design-c2.py --repo /fast/scratch/hyaku/tameshi-r29-CriticC2Design --rev HEAD
  result=$?; printf "COUNTER_EXIT=%s\n" "$result"; exit "$result"'
```

One-unit external-target control `9ea4f2dfd6e61b02949ca7039741c5af88853c21`:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE sh -c '
  mkdir -p /tmp/CriticC2Design-empty-host &&
  git -C /fast/scratch/hyaku/tameshi-r29-CriticC2Design update-ref HEAD 9ea4f2dfd6e61b02949ca7039741c5af88853c21 &&
  /usr/bin/python3 /tmp/CriticC2Design-c2.py --repo /fast/scratch/hyaku/tameshi-r29-CriticC2Design --rev HEAD
  result=$?; printf "COUNTER_EXIT=%s\n" "$result"; exit "$result"'
```

Fabricated-source control `109fe613b52cf6fdc1a60564e7439cdcd5ac09b4`:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE sh -c '
  git -C /fast/scratch/hyaku/tameshi-r29-CriticC2Design update-ref HEAD 109fe613b52cf6fdc1a60564e7439cdcd5ac09b4 &&
  /usr/bin/python3 /tmp/CriticC2Design-c2.py --repo /fast/scratch/hyaku/tameshi-r29-CriticC2Design --rev HEAD
  result=$?; printf "COUNTER_EXIT=%s\n" "$result"; exit "$result"'
```

The three measured receipts above each returned `C2_F6_PASS=true`, exit 0. These replay blocks are provided as reproduction instructions, not additional claimed executions.

The integrator reports a pre-data v1 redesign addressing pinned source digest, pinned census declaration, a symlink-free host manifest, and counter-run delta debugging. That redesign was not reviewed or scored by this seat; these findings apply to A's frozen counter only.
