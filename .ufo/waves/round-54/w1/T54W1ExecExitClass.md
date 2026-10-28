# T54W1ExecExitClass — exit-class differential across the four C0-edited tools

Seat: T54W1ExecExitClass (leaf executor, L1 TameshiR54a2), round 54 wave 1.
Attack item: diff `env-diff.py`, `bash-witness-study.py`, `evidence-disposition.py`,
`pin-disposition.py` between base `d33053f7552db4bd290c99a36979760f544c41ad` and
C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`, and prove with commands that the
usage (64), FAIL (1) and SETUP (2) arms still return their old codes.
Judged axis: operability. Milestone: **no exit-class regression in the four tools**.

## Verdict

**PASS on the milestone, with three residual findings (§5), none of them a
regression.**

- 34 arms × 2 revisions = 68 invocations, **0 exit-code disagreements** except the
  one arm C0 intends to change: `--selftest` under a set-but-unusable `TMPDIR`
  moved `1 (traceback)` → `2 (one naming could-not-evaluate line)` in all four tools.
- No removed or modified line in the diff touches an exit-code arm. The only
  executable changes are (a) a `ScratchRootUnusable(RuntimeError)` subclass per
  tool, (b) the raise site now raising it, (c) a `try/except` wrapping **only** the
  self-test call at the entry point.
- The wrapper is value-transparent: for stub self-test returns 0/1/2 the entry
  point returns 0/1/2 unchanged at both revisions, and a raised
  `ScratchRootUnusable` escapes at base and maps to 2 at C0 (`wrapper-probe.py`).
- Residual F1: `env-diff.py`'s **non-selftest** path allocates scratch through the
  same helper and still dies with a traceback and exit **1** at C0 — same code as
  base, so not a regression, but it contradicts the note's universal "never 1 …
  and never a traceback".
- Residual F2 (**blocks the wave's C2 claim, not this milestone**): the frozen C2
  counter at C0 prints `C2_R54_PASS=false total=1`, because its `strace -f` usable
  arm makes `registry-check.py --selftest` fail 2 of its own timeout-kill cases.
  Identical at base (`usable_ok=6` in the retained before artifact and in my rerun),
  so C0 did not cause it; the counter's instrument faults the tool under test.

Working copies are `git clone --shared` of the lane at each revision; the lane was
read-only throughout. No tool was installed; no pacman transaction was attempted.

## 1. What C0 changed, byte inventory

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git diff --stat d33053f7552db4bd290c99a36979760f544c41ad 59c38109bf119d0e9d4f878644a82babc937bc1e -- tools/
```
```
 tools/bash-witness-study.py   | 12 ++++++++++--
 tools/env-diff.py             | 15 ++++++++++++---
 tools/evidence-disposition.py | 15 ++++++++++++---
 tools/pin-disposition.py      | 15 ++++++++++++---
 tools/registry.json           |  7 +++++++
 5 files changed, 53 insertions(+), 11 deletions(-)
```

Tool content digests (`git show REV:tools/X | sha256sum`):

| tool | base d33053f7 | C0 59c3810 |
|---|---|---|
| `tools/env-diff.py` | `b4253922f8546430c1f524c6f48005552714f61697bb31b0a54901c01406faa0` | `ab193692d78d591fa7c9e55ba9c53cbe88376354adf548cd9d5034ce722bfe56` |
| `tools/bash-witness-study.py` | `4e999ff4553948e4fffdbc55f7a18c3d41604af4acb3292a8499fb6cb4557142` | `f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261` |
| `tools/evidence-disposition.py` | `4573b51ee19fbc483af5bc4805e40675d1c029630e612dde7a042a8f4c4b01d6` | `f09d1e490b94edb75364825c3941eb88cfb88a76ae26a2b9257e923ac123ea93` |
| `tools/pin-disposition.py` | `07a3e0411dd6916ed706153c4eb64f3d203f8ac865eab0396887f5cad7b815a9` | `c917bc41c3f40dae3eacea492d861211c2a4fe1e530cb9f22c5f8d6ff47d2988` |

Every changed line (`git diff -U0 base c0 -- tools/{env-diff,bash-witness-study,evidence-disposition,pin-disposition}.py`,
`+`/`-` lines only, repeated once per tool):

```
+class ScratchRootUnusable(RuntimeError):
+    """A set-but-unusable TMPDIR: could-not-evaluate (exit 2), never a traceback."""
-    fallback to /tmp, preserving CR47 semantics), else the platform default."""
+    fallback to /tmp, preserving CR47 semantics), else the platform default.
+    An empty TMPDIR is unset (round 54, corpus/knowledge/scratch-root-contract.md)."""
-            raise RuntimeError(
+            raise ScratchRootUnusable(
+    except ScratchRootUnusable as exc:
+        <one naming could-not-evaluate line>
+        return <2>
```

The only removed lines, per tool (three each, twelve in all), are
`raise RuntimeError(`, the old docstring terminator
(`    fallback to /tmp, …else the platform default."""`), and `return selftest()`,
which the same hunk re-adds verbatim inside the new `try`. **No removed line
carries an exit constant, and no arm's return value changes: the self-test's
return is passed through unchanged (proven in §3).**

Call sites and handlers at C0 (proves the change cannot reach another arm):

```
for f in tools/{env-diff,bash-witness-study,evidence-disposition,pin-disposition}.py; do
  echo "=== $f"; grep -n "strict_scratch_root()\|raise ScratchRootUnusable\|except ScratchRootUnusable" "$f"; done
```
```
=== tools/env-diff.py
36:def strict_scratch_root():
45:            raise ScratchRootUnusable(
80:    with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=strict_scratch_root()) as tmp:
234:        except ScratchRootUnusable as exc:
=== tools/bash-witness-study.py
209:def strict_scratch_root():
218:            raise ScratchRootUnusable(
1260:        prefix="bash-witness-selftest-private.", dir=strict_scratch_root()))
1788:    except ScratchRootUnusable as exc:
=== tools/evidence-disposition.py
195:def strict_scratch_root():
204:            raise ScratchRootUnusable(
2370:    scratch = Path(tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir=strict_scratch_root()))
3231:        except ScratchRootUnusable as exc:
=== tools/pin-disposition.py
165:def strict_scratch_root():
174:            raise ScratchRootUnusable(
725:    scratch = tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir=strict_scratch_root())
1399:        except ScratchRootUnusable as exc:
```
Each tool raises the class at exactly one line (`grep -c "raise ScratchRootUnusable"` = 1)
and defines it once. Line 80 in `env-diff.py` is inside `execute()`, which the run
path reaches as well as the self-test — see F1.

Ordering check, because the subclass is a `RuntimeError`: the pre-existing broad
handlers are `except (OSError, ValueError, subprocess.TimeoutExpired)` (env-diff
:157) and `except (OSError, ValueError, KeyError, TypeError)` (:263), neither of
which names `RuntimeError`; pin-disposition :1335 `except (OSError, RuntimeError,
subprocess.SubprocessError)` sits **inside** `selftest()` after the
`strict_scratch_root()` call at :725, so the helper's exception cannot be swallowed
there. No new handler shadows a pre-existing one.

## 2. Differential matrix (the receipt)

Harness: `T54W1ExecExitClass-receipts/matrix.py` (replay commands in §6). It clones
the lane at both revisions, runs the same argv with the same cwd, and varies only
`TMPDIR`. It records exit code, traceback presence, last line, and the full
stdout/stderr pair per arm.

```
REV  TOOL                        ARM                        RC   TB   LAST_LINE
base tools/env-diff.py           selftest-usable             0    -   ENVDIFF_SELFTEST: 9/9 pass
base tools/env-diff.py           selftest-empty              0    -   ENVDIFF_SELFTEST: 9/9 pass
base tools/env-diff.py           selftest-unusable           1   tb   RuntimeError: cannot create clone scratch … TMPDIR is not a usable directory
base tools/env-diff.py           usage-missing-out          64    -   ENVDIFF_USAGE: --contract and --out are required; --jobs must be 1..3
base tools/env-diff.py           usage-unknown-flag         64    -   ENVDIFF_USAGE: unrecognized arguments: --bogus
base tools/env-diff.py           help                        0    -     --selftest
base tools/env-diff.py           setup-missing-contract      2    -   ENVDIFF_SETUP: [Errno 2] … '/nonexistent/c.json'
base tools/env-diff.py           fail-unavailable-surface    1    -   ENVDIFF: classified=0/1 out=…
base tools/env-diff.py           runpath-unusable            1   tb   RuntimeError: … TMPDIR is not a usable directory
base tools/bash-witness-study.py selftest-usable             0    -   VERDICT: PASS
base tools/bash-witness-study.py selftest-empty              0    -   VERDICT: PASS
base tools/bash-witness-study.py selftest-unusable           1   tb   RuntimeError: … TMPDIR is not a usable directory
base tools/bash-witness-study.py usage-no-args              64    -   bash-witness-study.py: error: the following arguments are required: mode
base tools/bash-witness-study.py usage-unknown-mode         64    -   …invalid choice: 'bogusmode'
base tools/bash-witness-study.py help                        0    -   (…)
base tools/bash-witness-study.py check-default-evidence    1    -   WITNESS_CHECK: FAIL (1 problems; 96 files covered)
base tools/bash-witness-study.py setup-missing-evidence     2    -   WITNESS_STUDY: CANNOT-EVALUATE (missing /nonexistent/BW/declaration.json)
base tools/bash-witness-study.py fail-tampered-evidence     1    -   WITNESS_STUDY: TAMPER declared.tsv sha256=6ba4dabb… committed=0def0d3b…
base tools/evidence-disposition.py selftest-usable          0    -   SELFTEST: PASS (66/66)
base tools/evidence-disposition.py selftest-empty           0    -   SELFTEST: PASS (66/66)
base tools/evidence-disposition.py selftest-unusable        1   tb   RuntimeError: … TMPDIR is not a usable directory
base tools/evidence-disposition.py usage-no-args           64    -   (USAGE text)
base tools/evidence-disposition.py usage-unknown-flag      64    -   (USAGE text)
base tools/evidence-disposition.py usage-selftest-extra    64    -   (USAGE text)
base tools/evidence-disposition.py help                     0    -   (USAGE text)
base tools/evidence-disposition.py setup-missing-inputs     2    -   EVIDENCE_DISPOSITION: could_not_evaluate exit=2 id=root_unavailable …
base tools/pin-disposition.py     selftest-usable            0    -   SELFTEST: PASS (19/19)
base tools/pin-disposition.py     selftest-empty             0    -   SELFTEST: PASS (19/19)
base tools/pin-disposition.py     selftest-unusable          1   tb   RuntimeError: … TMPDIR is not a usable directory
base tools/pin-disposition.py     usage-no-args              2    -   (invalid_input JSON)
base tools/pin-disposition.py     usage-unknown-flag         2    -   (invalid_input JSON)
base tools/pin-disposition.py     usage-selftest-extra       2    -   (invalid_input JSON)
base tools/pin-disposition.py     help                       0    -   exit 2  could-not-evaluate invalid input (usage, manifest, fleet root)
base tools/pin-disposition.py     setup-missing-manifest     2    -   (invalid_input JSON)
```
The C0 half reproduces every row with the **same exit code**; the only rows whose
streams are not identical are enumerated below (full table:
`T54W1ExecExitClass-receipts/matrix.out`), and only the four `INTENDED` rows
change by design:

```
INTENDED tools/env-diff.py            selftest-unusable  base=1(tb) c0=2(-) OK
INTENDED tools/bash-witness-study.py  selftest-unusable  base=1(tb) c0=2(-) OK
INTENDED tools/evidence-disposition.py selftest-unusable base=1(tb) c0=2(-) OK
INTENDED tools/pin-disposition.py     selftest-unusable  base=1(tb) c0=2(-) OK
```

Aggregate: `MATRIX: 74 rows, 1 disagreements` — the single disagreement is
`env-diff`'s `runpath-unusable` stream (F1), whose exit code is equal (1/1) and
whose only textual difference is the raise site and the exception class:

```
$ diff <(sed -E 's#…/(base|c0)#CLONE#g; s#line [0-9]+, in#line N, in#g' base--env-diff--runpath-unusable.stderr) \
       <(sed -E 's#…/(base|c0)#CLONE#g; s#line [0-9]+, in#line N, in#g' c0--env-diff--runpath-unusable.stderr)
<     raise RuntimeError(
>     raise ScratchRootUnusable(
< RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '…/tmp-missing' (could-not-evaluate)
> ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '…/tmp-missing' (could-not-evaluate)
```

The unusable arm's C0 line, per tool — exactly one line, names the value, no
traceback, empty stdout (receipts `selftest-unusable--<tool>.c0.stderr`):

```
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/…/tmp-missing' (could-not-evaluate)
WITNESS_STUDY: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/…/tmp-missing' (could-not-evaluate)
evidence-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/…/tmp-missing' (could-not-evaluate)
pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/…/tmp-missing' (could-not-evaluate)
```

Raw stream comparison per arm (`STREAMS … raw=… normalized=…` in `matrix.out`): 30
pairs, 23 byte-identical raw, 7 raw-different, 6 of which are identical after
folding my own path/out-name (and the tool's self-digest in pin's JSON payload,
which must change); the seventh is `env-diff runpath-unusable` above.

## 3. Wrapper transparency (FAIL 1 / SETUP 2 arms that only a self-test can reach)

`evidence-disposition.py` and `pin-disposition.py` have **no** top-level exit-1
path outside `selftest()` (`grep -n "return 1"` → only inside the self-test, plus
pin's `invalid_input` fixed at 2). Their FAIL arm therefore cannot be exercised
without editing tool bytes, so it is proven by substituting only the self-test
callable in the harness namespace and calling the real entry point:

```
$ TMPDIR=$S/tmp-use python3 wrapper-probe.py $S/base     # WRAPPER_PROBE: ALL PASS
$ TMPDIR=$S/tmp-use python3 wrapper-probe.py $S/c0       # WRAPPER_PROBE: ALL PASS
```
```
TOOL                              STUB                      base      c0
env-diff.py                       returns 0/1/2             0/1/2     0/1/2
env-diff.py                       raises ScratchRootUnusable escaped  → 2
bash-witness-study.py             returns 0/1/2             0/1/2     0/1/2
bash-witness-study.py             raises ScratchRootUnusable escaped  → 2
evidence-disposition.py           returns 0/1/2             0/1/2     0/1/2
evidence-disposition.py           raises ScratchRootUnusable escaped  → 2
pin-disposition.py                returns 0/1/2             0/1/2     0/1/2
pin-disposition.py                raises ScratchRootUnusable escaped  → 2
```
`returns 1` is the FAIL(1) arm and `returns 2` the SETUP(2) arm at the self-test
entry: both pass through untouched at both revisions, and only the raised class
changes (escape → 2). Receipts: `wrapper-probe-base.out`, `wrapper-probe-c0.out`.

## 4. Usage (64) and SETUP (2) arms against each tool's own contract

| tool | documented usage class | observed 64/2 arm at base and C0 |
|---|---|---|
| `env-diff.py` | "64 usage" (docstring), `Parser.exit(64, "ENVDIFF_USAGE: …")` | 64 ×2 arms, both revs |
| `bash-witness-study.py` | `EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64`; `UsageParser` | 64 ×2 arms, both revs |
| `evidence-disposition.py` | `return 64` at :3218 and :3227 | 64 ×3 arms, both revs |
| `pin-disposition.py` | `exit 2 could-not-evaluate invalid input (usage, manifest, fleet root)` | 2 ×3 arms, both revs |

`pin-disposition.py`'s usage class is **2, not 64, by its own frozen usage text**;
that is base behaviour, not a regression, and the diff does not touch
`invalid_input`. SETUP(2) is exercised on a real non-scratch input in all four
tools (missing contract, missing evidence dir, missing dispositions root, missing
manifest) and reads 2 at both revisions.

The FAIL(1) arms actually exercised end to end: `env-diff` unavailable surface
(`ENVDIFF: classified=0/1`), `bash-witness-study` `check` on drifted evidence
(`WITNESS_CHECK: DRIFT tools/mutate-and-run.sh … FAIL (1 problems; 96 files
covered)`) and on a tampered copy (`WITNESS_STUDY: TAMPER declared.tsv …`) — all
1 at both revisions. The `check` DRIFT is a pre-existing lane fact (round-12
evidence pins an older `mutate-and-run.sh` digest), identical at both revisions.

## 5. Findings

### F1 — `env-diff.py` still prints a traceback and exits 1 on its non-selftest path (unchanged; contradicts the note's universal claim)

`env-diff.py`'s only scratch allocation (:80, `execute()`) is on the measurement
path, not only in the self-test. The new `except ScratchRootUnusable` sits in the
`--selftest` branch of `main` (:231-236); the measurement path's handlers
(`:157`, `:263`) do not name `RuntimeError`. Receipt: matrix arm
`runpath-unusable`, rc **1** at base *and* C0, with a traceback
(`runpath-unusable--env-diff.{base,c0}.stderr`).

Verdict: **no regression** (1 → 1), and the C2 contract explicitly discloses the
blind spot ("it sees the self-test path, not every branch a tool might use to
allocate scratch"). But `corpus/knowledge/scratch-root-contract.md` states as a
rule that such a `TMPDIR` "is could-not-evaluate (2), never 1 (a verdict of
'differs'/'failed') and never a traceback"; on this path it is 1 with a traceback,
so the sentence is false as written. It is a report-only defect: the C2 `note`
arm only checks the note's existence and its S-row citation, so the counter cannot
see it. Not fixed here (lane files are read-only for this seat).

### F2 — the frozen C2 counter cannot pass at C0 in this environment, from an arm C0 did not touch

```
$ python3 .ufo/evidence/round-54/c2/measure.py --lane <lane> --rev 59c38109bf11 --work $S/c2c0 --explain
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false

$ python3 .ufo/evidence/round-54/c2/measure.py --lane <lane> --rev d33053f7552d --work $S/c2base --explain
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=0 note=0 sources=0 total=14 C2_R54_PASS=false
```

The retained baseline `.ufo/evidence/round-54/before/c2.stdout` carries the same
`usable registry-check rc=1 / usable_ok=6 / total=14`, so the arm is pre-existing.
All six other tools pass the usable arm at C0 (`tmp_mkdirs=0`). Cause, isolated:

```
$ cd <c0 clone>; TMPDIR=<usable> strace -f -e trace=mkdir,mkdirat -o log python3 tools/registry-check.py --selftest
SELFTEST_CASE timeout-kills-setsid-pipe  FAIL (exit=1 elapsed=9.578s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=9.555s survivor=False marker=False)
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)   rc=1

$ cd <base clone>; same command
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)   rc=1

$ cd <c0 clone>; TMPDIR=<usable> strace -e trace=mkdir,mkdirat … python3 tools/registry-check.py --selftest
SELFTEST: PASS (51 cases)   rc=0                  # no -f
$ cd <clone>; TMPDIR=<usable> python3 tools/registry-check.py --selftest
SELFTEST: PASS (51 cases)   rc=0 at BOTH revisions # no strace
```

So `strace -f` alone breaks `registry-check`'s own timeout-kill self-test cases,
identically at base and C0; the counter's `usable_ok` arm can therefore never be
7/7 with `-f`, and the frozen target "7/7 exit 0 on a usable one" is unreachable
for reasons outside the four tools I was asked about. Report only: the counter is
frozen, and `registry-check.py` is not one of the C0-edited files.

### F3 — the frozen contract's C2 "before" cell disagrees with the artifact it cites

`contract.json` → `claims.C2.before` says `… sources=0 total=13 C2_R54_PASS=false
(measured at d33053f7, .ufo/evidence/round-54/before/c2.stdout)`, but that file
says `total=14`, and my rerun of the frozen counter at base also prints `total=14`
(`4 + 0 + 0 + 1 + 7 + 1 + 1 = 14` term by term). The verdict is unchanged
(false before, false at C0), but the number is wrong by one. Report-only.

## 6. Reproduction

All work under `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r54/T54W1ExecExitClass`
(this seat's tree is removed on exit; the harnesses below are copied into
`T54W1ExecExitClass-receipts/` so the receipts stay replayable):

```sh
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
mkdir -p "$S"; cd "$S"
for r in base:d33053f7552db4bd290c99a36979760f544c41ad c0:59c38109bf119d0e9d4f878644a82babc937bc1e; do
  n=${r%%:*}; v=${r#*:}
  git clone --shared --quiet "$L" "$S/$n"
  git -C "$S/$n" -c advice.detachedHead=false checkout --quiet "$v"
  git -C "$S/$n" rev-parse --show-toplevel        # asserts the fixture root
done
mkdir -p "$S/tmp-use"
# "$S/tmp-missing" must stay ABSENT: it is the set-but-unusable TMPDIR arm.
cp T54W1ExecExitClass-receipts/contract.json "$S/contract.json"
TMPDIR=$S/tmp-use python3 T54W1ExecExitClass-receipts/matrix.py               # 74 rows; expected 1 (F1)
TMPDIR=$S/tmp-use python3 T54W1ExecExitClass-receipts/wrapper-probe.py "$S/base"
TMPDIR=$S/tmp-use python3 T54W1ExecExitClass-receipts/wrapper-probe.py "$S/c0"
```

The receipt harnesses pin the seat scratch path (`/fast/scratch/hyaku/tameshi-r54/
T54W1ExecExitClass`) for `base/`, `c0/`, `tmp-use/` and the absent `tmp-missing/`;
they are the fixture, not a general driver.

Receipts directory contents (`./.ufo/waves/round-54/w1/T54W1ExecExitClass-receipts/`):
`matrix.py`, `wrapper-probe.py`, `contract.json`, `matrix.out`,
`wrapper-probe-{base,c0}.out`, `selftest-unusable--<tool>.{base,c0}.stderr` (8),
`runpath-unusable--env-diff.{base,c0}.stderr`, `witness-fail-tampered.c0.stderr`,
`witness-check-drift.c0.stdout`.

## 7. Risks and blockers

- None for the milestone. The four tools' exit classes are unchanged outside the
  intended self-test arm; the intended arm is uniform (2, one naming line, no
  traceback) in all four.
- F2 is a **C2 blocker for the wave**, not for this item: with the frozen counter
  and `strace -f`, `usable_ok` is 6/7 at both revisions, so the deciding invocation
  cannot print `C2_R54_PASS=true` here regardless of these four tools.
- F1/F3 are report-only text/claim defects in `corpus/knowledge/scratch-root-contract.md`
  and `contract.json`; both files were read, never edited.

## 8. Tooling record

No installs or upgrades; no pacman transaction attempted (host pause respected).
Tools used as present: `git`, `python3` (3.14), `strace`.

Round conformance, read-only: `bash scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → exit **0** (final line
`tameshi  ok  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`;
the W01/W04 lines are the lane's pre-existing warnings).

Lane write check: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status
--porcelain` lists only untracked artifacts that predate this seat
(`.ufo/evidence/round-54/{before,c1,control,integrate}/`, `.ufo/waves/round-54/`);
no tracked lane file was modified, and nothing outside
`.ufo/waves/round-54/w1/T54W1ExecExitClass*` was written by this seat.
