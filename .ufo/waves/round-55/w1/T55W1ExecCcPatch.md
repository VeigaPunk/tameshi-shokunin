# T55W1ExecCcPatch - C2 patch: context-capture one-line grammar

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Patch base (frozen counter set): `631cd6455e58dce969310b4c0466c3383d9f5108`
- Contract base: `0a2010acd1e92e4e332774050825e21bcfc7e079`
- Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1ExecCcPatch` (`clone` at the frozen rev, `pristine` at the same rev, `no-such-tmpdir`, `tmp-usable`)
- Lane production files edited by this seat: **none** (patch demonstrated in the scratch clone only; L1 integrates)

## Item

`tools/context-capture.py` must turn a set-but-unusable `TMPDIR` into the frozen
class line on **stderr** with exit 2, with no `RuntimeError` token and no
traceback, while `--check` keeps its exit contract:

```
^[A-Za-z][A-Za-z0-9_.-]*(\.py)?: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' \(could-not-evaluate\)$
```

## Exact patch (against `631cd64`)

```diff
diff --git i/tools/context-capture.py w/tools/context-capture.py
index 9208999..6c1d18c 100755
--- i/tools/context-capture.py
+++ w/tools/context-capture.py
@@ -297,6 +297,10 @@ expected schema (exactly four keys):
 """
 
 
+class ScratchRootUnusable(RuntimeError):
+    """A set-but-unusable TMPDIR, reported as one operator-visible line (round 55)."""
+
+
 def strict_scratch_root():
     """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
     round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
@@ -305,7 +309,7 @@ def strict_scratch_root():
     t = _os.environ.get("TMPDIR")
     if t:
         if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
-            raise RuntimeError(
+            raise ScratchRootUnusable(
                 "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
         return t
     return tempfile.gettempdir()
@@ -2210,6 +2214,11 @@ def run_selftest():
         harness = SelftestHarness()
         run_selftest_cases(harness)
         return harness.finish()
+    except ScratchRootUnusable as exc:
+        # The class is one operator-visible line grammar: the exception type never
+        # appears, the line goes to stderr, and stdout carries no setup error.
+        sys.stderr.write("context-capture.py: could-not-evaluate: {}\n".format(exc))
+        return 2
     except Exception as exc:  # setup failure is loud but never a traceback
         sys.stdout.write(
             "SELFTEST: FAIL (setup error: {}: {})\n".format(
```

10 insertions, 1 deletion. Rejection-reason for the alternative designs:
- subclassing `RuntimeError` keeps every pre-existing `except RuntimeError` caller behaving as before, and the specific clause is ordered *before* the generic `except Exception`;
- the generic setup-error branch (stdout `SELFTEST: FAIL (setup error: ...)`) is intentionally left alone: it covers non-scratch setup failures, which the frozen grammar does not describe and the C2 counter does not measure.

`strict_scratch_root()` has exactly one call site - `SelftestHarness.__init__`
(`tempfile.mkdtemp(..., dir=strict_scratch_root())`) - reached only from
`run_selftest()`; `--check` never allocates, so its contract cannot move.

## Evidence (all commands run with `cwd=<clone>` at `631cd64`)

| # | Command (TMPDIR prefix) | Observed | Receipt |
|---|---|---|---|
| 1 | `TMPDIR=<nonexistent> python3 tools/context-capture.py --selftest` | rc=2, stdout 0 bytes, stderr exactly one line, `GRAMMAR.match` **True**, `RuntimeError`=0 `Traceback`=0 | `arm-unusable.{rc,stdout,stderr}`, `grammar-conformance.txt` |
| 2 | `TMPDIR="" python3 tools/context-capture.py --selftest` | rc=0, `SELFTEST: PASS (49/49)`, stderr 0 bytes (current expected exit = base rc 0) | `arm-empty.*` |
| 3 | `TMPDIR=<usable dir> python3 tools/context-capture.py --selftest` | rc=0, `SELFTEST: PASS (49/49)`, stderr 0 bytes | `arm-usable.*` |
| 4 | `TMPDIR=<usable dir> strace -f -e trace=mkdir,mkdirat ... --selftest` | rc=0, 48 `mkdir` calls, **0** under `/tmp`, all under the supplied TMPDIR | `strace-usable.log` |
| 5 | `TMPDIR=<nonexistent> python3 tools/context-capture.py --check --json` | rc=0, `"id": "context_consistent"`, `"status": "ok"`, stderr 0 bytes | `check-unusable-json.*` |
| 6 | `TMPDIR=<nonexistent> python3 tools/context-capture.py --check` | rc=0, `CONTEXT: OK (... exit=0 findings=0)` | `check-unusable.*` |
| 7 | `python3 tools/context-capture.py --check` (default env) | rc=0, same `CONTEXT: OK` line | `check-default.*` |
| 8 | `python3 tools/context-capture.py --help` | rc=0 | `help.*` |
| 9 | pre-patch blob at `631cd64`, `TMPDIR=<nonexistent> --selftest` | rc=2 but **stdout** `SELFTEST: FAIL (setup error: RuntimeError: ...)`, stderr 0 bytes | `base-unusable.*` |
| 10 | `git -C pristine apply --check context-capture.patch` | `APPLY_CHECK=ok` (pristine, `rev-parse --show-toplevel` = the fixture dir) | `apply-check.txt` |
| 11 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | rc=0, `ok .../corpus/SOURCES.md` | `census.txt` |

The frozen `GRAMMAR` object in `.ufo/evidence/round-55/c2/measure.py` was imported
directly (not re-typed) for row 1: `fullmatch=True`, one stderr line, empty stdout.

Self-consistency: the patched file's sha256 `cbf617b2dd2c8984da5b3eed44d242da5b3139256dba4f53dbe54d31f32b2975`
equals the `tool_sha256` the tool itself reported in row 5 - the run measured the patch, not stale bytes.

Patch sha256 `db8e421bdfc56d8fa04826dba0953f94ce68b2c3c2b15fc0fd40a4f01633dd12`; base blob sha256 `be539b4c...3183d`.

## Findings and risks (reported, not fixed)

1. **The lane worktree already carries an equivalent uncommitted edit.** At the
   time of work, `git status` showed `M tools/context-capture.py` with the same
   class, the same `raise ScratchRootUnusable(`, and the same stderr line
   (`sys.stderr.write("context-capture.py: could-not-evaluate: {}\n".format(exc))`,
   `return 2`). Differences are comment/docstring wording only. I ran the
   in-flight copy read-only (`TMPDIR=<nonexistent> python3 tools/context-capture.py --selftest`,
   receipt `lane-worktree-unusable.*`): rc=2, stdout 0 bytes, the exact grammar
   line on stderr. **L1 must not apply this patch on top of the in-flight edit** -
   one of the two is enough; the observable contract is identical.
2. **Residual `%r` quoting edge case (shared by all seven tools).** The message
   interpolates `%r`; a TMPDIR path containing a single quote reprs with double
   quotes and no longer matches the frozen `'.+'` grammar
   (`repr-edge-cases.txt`: `/tmp/a'b` -> `"/tmp/a'b"`, `grammar_match=False`).
   Ordinary paths, spaces, double quotes and non-ASCII all match. Every one of the
   seven `strict_scratch_root()` implementations uses the identical format string,
   so this is a property of the frozen grammar plus the round-53 message, not of
   this patch; the counter's arm uses a plain path. Not changed here.
3. **Module docstring untouched.** Header lines 12/27 still describe selftest
   scratch as `tempfile.mkdtemp(dir=tempfile.gettempdir())`. It does not affect the
   C2 counter and is outside this item; flagged as an optional L1 follow-up only.
4. **Full C2 counter not run here by design.** `measure.py` clones the lane and
   checks out `--rev`, so it cannot see an uncommitted patch. After L1 commits, the
   `context-capture --selftest` row should flip `grammar ... FAIL` -> ok and
   `lazy context-capture --check rc=0` should stay ok.
5. No tools were installed or upgraded for this item; no package manager channel
   was used. No fleet-root file, PATH directory, or lane production file was written.

## Receipts

All under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ExecCcPatch-receipts/`:
`arm-unusable.{rc,stdout,stderr}`, `arm-empty.*`, `arm-usable.*`,
`base-unusable.*`, `check-unusable-json.*`, `check-unusable.*`, `check-default.*`,
`help.*`, `lane-worktree-unusable.*`, `strace-usable.log`,
`grammar-conformance.txt`, `repr-edge-cases.txt`, `apply-check.txt`, `census.txt`,
`context-capture.patch`, `sha256.txt`.
