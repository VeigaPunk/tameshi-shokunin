# C2 v2 pre-data design review

## Scope and axes

Frozen B: `6ab11a6274d6111deb2b31b2ba6b4f742603bd49`. Private clone: `/fast/scratch/hyaku/tameshi-r29-critic-c2v2`. Counter copied before control commits to `/tmp/critic-c2v2-c2v2.py`; its SHA-256 matches the amendment's `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c`. Kagi was read only at `fecee8743e52eb8fb5fbb40782934cb619a1a96e`.

Axes: **coverage** (does this establish F6 rather than another small B5 witness?), **depth** (is the sourced reduction method actually demonstrated?), **operability** (can an honest fixture reach the target reproducibly?), and **calibration** (do individual flags mean what they print?). No judgment, admission, integration, counter amendment, model call, seat spawn, or other OMP runtime was performed.

**Result:** none of five counter controls reached PASS. Nevertheless, all six requested individual checks can be satisfied without building and reducing a host fixture on the pinned declaration. More seriously, the minimized-fixture oracle cache confuses different contents, the frozen reducer is not equal to S024's algorithm, and the full pinned original cannot kill B5 on this ordinary executable scratch filesystem because every declared executable also requires mode 755. No full host fixture was built.

All lane-relative citations below refer to B unless explicitly marked as a private control. Kagi citations are at the pinned revision, not its current worktree.

## Verdicts per question

### 1. Contract, implementation and label: intended identity yes; exact implementation fidelity no

The amendment's label is `C2_F6_V2_PASS` (`.ufo/evidence/round-29/contract-amendment-1.json:15-18`), matching the counter docstring and printed predicate (`.ufo/evidence/round-29/c2-measure-v2.py:10-27,299-305`). The final conjunction includes present, anchored, original kill, ddmin equality, minimized kill, 1-minimality, source markers, and located quote (`:302-303`). The counter digest matches the amended digest. Whitespace/backtick-normalized docstring and contract sentences differ only by the docstring's extra words `corpus/surface-census.sh's declaration`; this is not a changed condition.

However, code is not a faithful independent implementation of all those conditions:

* **Wrong oracle identity:** the cache key contains only `(file, line-index)`, omitting line contents (`c2-measure-v2.py:164-179`). `to_units()` independently renumbers original and minimized fixtures (`:103-105,260`). Control V2-D3 reports `kill=1 one_minimal=1` for a minimized fixture for which independent fresh executions return pristine=0 and mutant=0, and a fresh oracle returns False. `ddmin_match=0` prevents full PASS for this particular control; this is a real individual-check defect, not a demonstrated full-PASS bypass. A genuine reduction can also collide with an earlier differently populated original subset, so this is not merely permissive output on unrelated data.
* **Count tokens are not parsed:** `:279` uses substring membership. V2-D4 says `units_original=20` and `units_minimized=20`, although the counter reports 2 and 2; `entry_sourced=1`. This is weaker than checking numerical values. The amendment intentionally leaves prose quality to review (`contract-amendment-1.json:21`), but that does not explain incorrect count tokens.
* The implementation accepts curly as well as straight double quotation marks (`:294`). This is compatible with an ordinary reading of “double-quoted,” but it is broader than an ASCII-only interpretation.

Smallest safe corrections: key the oracle by complete immutable unit contents (for example `(file,index,line)`), preserving distinct original/minimized identities; parse bounded count tokens and compare integer values. Keep the current label only for its frozen predicate; do not portray a label match as validation of its faulty subchecks.

### 2. Anchoring and containment: census is byte-checked; no outside-path smuggling found within the anchored B inputs

`anchored` compares the original census **bytes**, including order, comments, duplicates and final newline (`c2-measure-v2.py:249`), not just its line set. Shapes and baseline deliberately use subset-of-line-set tests (`:250-251`); empty files and repeated/reordered permitted lines satisfy this condition. V2-D1 gets `anchored=1` simply by copying the 55-line declaration and leaving both supporting files and host manifest empty. It is not a usable pinned host fixture.

All non-comment paths in the pinned census, shape and baseline data begin with `$HOME/` or `$STATE/` and contain no `..` component. The four actual census scan directives are `$HOME`-rooted (`kagi corpus/surface-census.tsv:17-20`). Its three executable rows are at `:22,30-31`. The pinned shapes' `$STATE` paths are at `corpus/state-shape.tsv:27-44`; baseline paths are `$HOME`-rooted (`corpus/drift-baseline.tsv:1-15`). A subset cannot introduce a new absolute or escaping row. The original census cannot acquire a malicious `# scan` without failing byte identity. The minimized fixture must equal the counter's selected original lines to satisfy `ddmin_match` (`c2-measure-v2.py:263-264`), so a passing equality check cannot introduce a new scan or `$STATE` path either.

Manifest paths are normalized, absolute/escaping/root/duplicate normalized paths rejected, and only directory/file nodes created under a fresh scratch host (`c2-measure-v2.py:114-147`). There is no manifest symlink type. Internal `a/../b` spelling can normalize to safe `b`; that is not an escape. No execution of manifest file contents occurs on this verify path.

The underlying gate's `resolve()` itself performs substitutions, **not containment enforcement** (`kagi corpus/surface-census.sh:121-128`), and scan paths pass directly to `find` (`:151-160,239-259`). Thus arbitrary unanchored census inputs remain unsafe as a general fixture format, but I did not find an anchored-B path escape. I did not build an outside-path exploit or rely on host files.

Smallest safe correction: preserve byte identity and manifest restrictions; do not mistake `anchored=1` alone for building a fixture. If this becomes a general-purpose runner, validate canonical resolved targets beneath its root rather than depending solely on these particular pinned strings. No new containment bypass is claimed here.

### 3. ddmin: deterministic for a fixed oracle, but not equal to S024's complement form

Unit ordering is fixed by `FILES` and file line order (`c2-measure-v2.py:56,103-110`), and the reducer's iteration order is deterministic (`:183-202`). Conditional on stable oracle results, repeated computation follows the same path. Host dependence and the wrong cache key qualify that statement.

The snapshot uses `start = 0.0`, `subset_length = len(inp) / n`, endpoints `int(start)` and `int(start + subset_length)`, and increments by that fractional length (`sources/S024-fuzzingbook-Reducer.html:12919-12935`). The frozen counter instead uses integer `len(units) // n`, integer endpoints, and integer increments (`c2-measure-v2.py:187-197`). These are not the same partition policy when lengths are indivisible; the counter can try an additional short tail.

Observed pure-algorithm counterexample, using S024's extracted Python class and a stable monotone interestingness predicate:

```text
input = [0,1,2,3,4]
interesting(x) = ({0,1} <= set(x)) OR ({0,4} <= set(x))
v2 result   = [0,4]
S024 result = [0,1]
v2 tested:   [2,3,4], [0,1,4], [1,4], [0,4], [4], [0]
S024 tested: [0,1,2,3,4], [2,3,4], [0,1], [1], [0]
```

The S024 trace includes its initial interestingness assertion. Both outputs are legitimately 1-minimal. This is **not** a proof the v2 reducer cannot reduce: the contract explicitly selects “this counter's own frozen ddmin.” It is a fixable attribution/implementation discrepancy if equality with S024 is claimed, not license to reject one valid minimum because another implementation chose a different one.

Smallest safe correction: either implement S024's exact partition schedule in a prospective, explicitly re-frozen counter, or describe the existing code honestly as an integer-partition complement variant. Do not silently replace the frozen algorithm after data.

### 4. Oracle environment: more normalized than v1, still host-dependent

The gate gets `PATH=/usr/bin:/bin`, scratch HOME, C locale and UTC, and explicit root/census/shapes/baseline (`c2-measure-v2.py:154-162`). This removes arbitrary inherited gate PATH, locale and HOME. It does not pin Bash, GNU tools, Python/sqlite versions, filesystem mount semantics, permissions or execution policy. Counter-side `git`, `timeout` and cleanup `chmod` still resolve in its process environment (`:62-64,158,177,274`). Scratch selection is `tempfile.mkdtemp()` in the counter, so outer temp-directory environment can change its filesystem (`:246`).

Verify uses `stat`, `awk`, `find`, `sort` and shell access tests (`kagi corpus/surface-census.sh:130-141,178-181,239-259`). Selected present JSON key assertions invoke system `python3` (`:377-386`); selected present SQLite table/row assertions invoke system sqlite3 and scratch-copy helpers (`:265-308,388-408`). Missing sqlite3 fails closed only on that branch. The `the-janitor` binary is not invoked by the verify dispatch (`:852-857`; verbs is a separate arm at `:869-870`).

Observed host facts: `/tmp` is XFS with `rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota` and **without noexec**; no TMPDIR/TMP/TEMP override was set. Effective user is vgpnk uid 1000. Bash is 5.3.20; GNU stat/coreutils is 9.12. `/usr/bin/sqlite3` resolves; `the-janitor` does not resolve in the probed PATH. No tool was installed or updated.

Smallest safe correction: declare the executable/mount/tool assumptions and run in a pinned verify environment if results must be portable. A scratch HOME and fixed directory names in PATH are not a hermetic environment. This environment issue matters directly to reachability below.

### 5. Full pinned original reachability: no ordinary exec-bit-only kill on this host

All three pinned census executable rows demand `755` (`kagi corpus/surface-census.tsv:22,30-31`). Pristine first checks regular-file identity, then the executable access bit condition (`corpus/surface-census.sh:184-217`), and afterwards checks exact stat mode (`:219-223`). B5 removes **only** the executable-condition arm (`tools/mutate-and-run.sh:717-719`), leaving that exact-mode failure and the shared FAILED accumulator. Verify exits 0 only when FAILED remains zero (`kagi corpus/surface-census.sh:852-867`).

For a static regular file created and owned by the counter on the observed ordinary executable scratch filesystem:

* If its mode is 755, executable access succeeds, so pristine emits no required exec-bit divergence.
* If it lacks execution permission, pristine can emit the required divergence, but B5 still rejects the non-755 mode.
* Making it missing, a symlink, the wrong kind, or allowing other drift does not help: B5 retains those failures.
* Removing baseline/shapes rows cannot remove the census's own 755 constraint.

V2-D4 confirms this with just **one pinned census row**, not a full fixture: pristine exits 1 for the exec bit; B5 exits 1 for mode 644 versus 755. Therefore adding the remaining pinned surfaces cannot turn that residual mode drift into B5 exit 0. This is a structural impossibility argument under the observed execution semantics, not an empirical claim to have built all 55 lines' host surfaces.

Caveat: on a `noexec` mount, execution access can fail while stat still reports 755; access-control/security-policy differences can also separate the tests. Such a result would be environment-dependent, not the intended missing-exec-bit witness. No such mount or policy was created or used. The predicate does not constrain this distinction.

Smallest safe correction: do not send data work to an unreachable target. Preserve B and these receipts; the integrator must explicitly resolve the conflict before data, for example by choosing a genuinely distinguishing allowed probe/pinned target or by expressly defining and re-freezing a declaration-derived fixture transformation that removes the redundant exact-mode condition for the probe. Silently changing 755 to `-`, changing B5, or moving the goalposts after data would violate the current frozen predicate. Whether the remaining source-marker/two-unit result warrants coverage is the canonical Rust judge's decision, not this review's.

## Counter controls and receipts

All commands below ran only in the private clone. All full counter runs used the unchanged copied counter with `--rev HEAD`, were wrapped in `timeout 900`, exited **1**, and emitted no stderr except the tool's exit-status annotation. `meets` refers only to `C2_F6_V2_PASS`, not claim admission. Variant commits form a linear chain in the clone; no lane Git write occurred. Only this report was written in the lane.

Exact setup command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 sh -c 'mkdir -p /fast/scratch/hyaku && git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r29-critic-c2v2 && git -C /fast/scratch/hyaku/tameshi-r29-critic-c2v2 checkout -q --detach 6ab11a6274d6111deb2b31b2ba6b4f742603bd49 && cp /fast/scratch/hyaku/tameshi-r29-critic-c2v2/.ufo/evidence/round-29/c2-measure-v2.py /tmp/critic-c2v2-c2v2.py'
```

Pinned evidence files were extracted using `subprocess.run(['timeout','900','git','-C',KAGI,'show',PIN+':corpus/'+NAME], env=environment_without_GIT_variables, capture_output=True, check=True)`, then their returned bytes saved as `/tmp/critic-c2v2-NAME`. NAME was `surface-census.sh`, `surface-census.tsv`, `state-shape.tsv`, or `drift-baseline.tsv`. These are evidence copies, not kagi edits. Pinned gate SHA-256: `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`.

The exact common scoring command, working directory the private clone, was:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 python3 /tmp/critic-c2v2-c2v2.py --repo /fast/scratch/hyaku/tameshi-r29-critic-c2v2 --rev HEAD
```

For committed variants the actual shell command used the same env/timeout wrapper around `sh -c 'BUILD_AND_COMMIT && git rev-parse HEAD && python3 /tmp/critic-c2v2-c2v2.py --repo /fast/scratch/hyaku/tameshi-r29-critic-c2v2 --rev HEAD'`. Exact BUILD_AND_COMMIT sequences are given below. File content creation/replacement before those commands used the write/edit tools, not unrecorded shell commands. Escapes in the content descriptions denote literal tabs/newlines.

### V2-D0 — unchanged frozen B

Built nothing. Commit: `6ab11a6274d6111deb2b31b2ba6b4f742603bd49`. Ran the common score command.

```text
C2_F6_V2: fixture=absent anchored=0 kill_original=0 units_original=0 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=6ab11a6274d6111deb2b31b2ba6b4f742603bd49
PREDICATE: C2_F6_V2_PASS=false
```

Exit: 1. **CONTROL V2-D0: meets=no**

### V2-D1 — byte-copied census, empty host, nonsense source markers

Created original/shapes.tsv, original/baseline.tsv, original/host.tsv and all four minimized TSVs as zero bytes. Copied pinned census to original/census.tsv. Created entry as these exact five lines:

```text
source: S024

Bananas are triangular. No minimization method was read or performed.
units_original=55
units_minimized=0
```

Created lesson as this single line, keeping the frozen snapshot and existing mined S024 registry row unchanged:

```text
S024 snapshot sha256=3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99: “Its result is 1-minimal, meaning that every character contained is required to produce the error”
```

BUILD_AND_COMMIT:

```sh
cp /tmp/critic-c2v2-surface-census.tsv .ufo/evidence/round-29/f6/original/census.tsv && git add -f .ufo/evidence/round-29/f6 corpus/knowledge/survivor-fixture-minimization.md corpus/lessons/round-29.md && git -c user.name=ctl -c user.email=ctl@x commit -qm "control: declaration copy and no-reader markers only"
```

Commit: `90c7c36fca6ef63acf9837114f1f95b72a30ec61`.

```text
  oracle tests run: 2
C2_F6_V2: fixture=present anchored=1 kill_original=0 units_original=55 units_minimized=0 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=1 quote_located=1 rev=90c7c36fca6ef63acf9837114f1f95b72a30ec61
PREDICATE: C2_F6_V2_PASS=false
```

Exit: 1. **CONTROL V2-D1: meets=no**. Individual `anchored`, `entry_sourced`, and `quote_located` checks met without a constructed host or reduction. The quote was found mechanically; no assertion of reader learning follows from it.

### V2-D2 — handwritten two-unit witness, no pinned original or reduction

Replaced original and minimized census.tsv with identical bytes `$HOME/p\tasset\texec\t-\thandwritten no-reader control\n`; replaced both host.tsv with `p\tfile\t644\tx\n`. Shapes/baseline stay empty. Edited entry counts to 2 and 2; nonsense and lesson remain. This is an already minimal witness, not a fixture built from the pinned declaration, and ddmin removes nothing.

BUILD_AND_COMMIT:

```sh
git add -f .ufo/evidence/round-29/f6 corpus/knowledge/survivor-fixture-minimization.md && git -c user.name=ctl -c user.email=ctl@x commit -qm "control: handwritten two-unit fixture without pinned declaration"
```

Commit: `f9f3ed00f1190e79e6a81a442cec3ab8ec986c6a`.

```text
  oracle tests run: 3
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=2 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=1 quote_located=1 rev=f9f3ed00f1190e79e6a81a442cec3ab8ec986c6a
PREDICATE: C2_F6_V2_PASS=false
```

Exit: 1. **CONTROL V2-D2: meets=no**. `kill_original`, `ddmin_match`, and `one_minimal` met without the claimed work. `anchored=0` correctly blocks complete PASS. Zero size reduction is allowed by the frozen code; requiring an actual reduction would be a contract change, not something this reviewer may impose.

### V2-D3 — same indices, different minimized semantics

Edited only minimized/census.tsv, replacing `exec` with `file`. Original remains V2-D2's exec witness. Minimized now has no executable declaration at all. BUILD_AND_COMMIT:

```sh
git add -f .ufo/evidence/round-29/f6/minimized/census.tsv && git -c user.name=ctl -c user.email=ctl@x commit -qm "control: same unit indexes but minimized fixture cannot kill B5"
```

Commit: `d4dd0646f77be053ad89d3a80f982391901fbd51`.

```text
  oracle tests run: 3
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=2 units_minimized=2 ddmin_match=0 kill=1 one_minimal=1 entry_sourced=1 quote_located=1 rev=d4dd0646f77be053ad89d3a80f982391901fbd51
PREDICATE: C2_F6_V2_PASS=false
```

Exit: 1. **CONTROL V2-D3: meets=no**. False positive `kill` and `one_minimal` flags are confirmed, not inferred.

Independent probe used a fresh scratch directory, the extracted pristine bytes, `b5_mutant()` from the copied counter, `materialize()` on the minimized working-tree contents, and a new `Oracle`; the unchanged `Oracle.run()` invokes its timeout-60 Bash verify command. The evaluation cell itself had a 900-second deadline. Full probe stdout:

```text
INDEPENDENT_MINIMIZED pristine exit=0
SURFACE OK       $HOME/p (file 644)
SURFACE_CENSUS: CLEAN (assets=1 runtime=0 scanned=0 ok=1 absent=0 skipped=0)
INDEPENDENT_MINIMIZED mutant exit=0
SURFACE OK       $HOME/p (file 644)
SURFACE_CENSUS: CLEAN (assets=1 runtime=0 scanned=0 ok=1 absent=0 skipped=0)
fresh_oracle_kill=False
```

The evaluation completed normally. Its scratch directory was chmod-restored and removed in `finally`.

### V2-D4 — one pinned exec row exposes residual mode check; wrong count prefixes

Replaced both census files with pinned census line 22, exact text `$HOME/.config/the-janitor/client.py\tasset\texec\t755\tHTTP client: session-id, request timeout (the flock is in the CLI)\n`. Both host manifests became `.config/the-janitor/client.py\tfile\t644\tx\n`. Supporting TSVs remain empty. Edited entry counts from 2 to **20** and from 2 to **20**. No full fixture was constructed.

BUILD_AND_COMMIT:

```sh
git add -f .ufo/evidence/round-29/f6 corpus/knowledge/survivor-fixture-minimization.md && git -c user.name=ctl -c user.email=ctl@x commit -qm "control: pinned exec mode conflicts with B5 kill; wrong count prefixes"
```

Commit: `fb8054a795e696a719e74bb915ed7d9da62f8f58`.

```text
  oracle tests run: 1
C2_F6_V2: fixture=present anchored=0 kill_original=0 units_original=2 units_minimized=2 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=1 quote_located=1 rev=fb8054a795e696a719e74bb915ed7d9da62f8f58
PREDICATE: C2_F6_V2_PASS=false
```

Exit: 1. **CONTROL V2-D4: meets=no**. `entry_sourced=1` despite numerically incorrect counts. The independent gate probe used the same extraction/materialization/new-oracle procedure as V2-D3, with this original fixture:

```text
SINGLE_PINNED_ROW pristine exit=1
SURFACE DIVERGED $HOME/.config/the-janitor/client.py (declared exec, no execute bit)
SURFACE_CENSUS: DRIFT (diverged=1 gone=0 link=0 unlisted=0 crosscheck=0 shape=0 unverified=0 ok=0 absent=0 skipped=0)
SINGLE_PINNED_ROW mutant exit=1
SURFACE DIVERGED $HOME/.config/the-janitor/client.py (mode 644, declared 755)
SURFACE_CENSUS: DRIFT (diverged=1 gone=0 link=0 unlisted=0 crosscheck=0 shape=0 unverified=0 ok=0 absent=0 skipped=0)
```

The evaluation completed normally and removed its scratch directory in `finally`.

## Corrections versus judgment

Fixable defects: cache keys omit data identity; count checks accept prefixes; S024 attribution promises stronger algorithm equality than implemented; the target conflicts with its pinned executable-mode requirements on the observed filesystem. Environment normalization is a useful improvement, not hermeticity. Anchored containment improved materially over v1; no anchored escape was demonstrated.

Judgment/tradeoff: the contract explicitly leaves prose quality to review and permits a zero-change ddmin result. Thus nonsense plus a real mechanically located quote, or a correct two-unit local witness, is not itself a coding defect in those narrowly defined markers. It still does not establish reader learning or coverage. Only the canonical Rust judge can accept or reject that axis fit; no such judgment was run here.

No processes were intentionally left running; all launched commands and probes completed synchronously. No tools installed/updated. No production code, contract, counter, runner, sibling lane, lane index, or jj state changed. No jj command was invoked.
