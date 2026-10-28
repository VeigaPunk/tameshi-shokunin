# T55W1ExecRepPatch — C2 patch: repeat-control

Seat: `T55W1ExecRepPatch` (leaf executor). Round 55, wave 1. Judged on operability.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base revision measured: `631cd6455e58dce969310b4c0466c3383d9f5108`.

Everything below was measured in a `git clone --shared` of the lane checked out
`--detach` at the base revision, with the patch applied on top. The pristine base
tool and the frozen counter were extracted from the base revision into the receipts
directory, so both artefacts are attributable to that revision, not to the lane's
in-flight working tree:

- `repeat-control.base.py` sha256 `3f82aa5a97c4a67dd58e47aed10e0e2f0206bf65e306bcec80f57126f6309d51`
- `c2-measure.frozen.py` sha256 `9d076812d9c0fcd2d06dc7543e5a99bc2bfcdaf85f10ee6da9d0b5ea0b346dac`

No lane production file was edited (I write only this report and
`.ufo/waves/round-55/w1/T55W1ExecRepPatch-receipts/`). No tool was installed.

## The patch

`T55W1ExecRepPatch-receipts/patch.diff` (also `repeat-control.patched.py`), three
hunks, `tools/repeat-control.py`:

```diff
@@ -145,6 +145,14 @@ USAGE = (
 )
 
 
+class ScratchRootUnusable(RuntimeError):
+    """A set-but-unusable TMPDIR: could-not-evaluate, never a traceback (round 55).
+
+    A distinct type so main() can answer with the frozen grammar line instead of
+    the generic setup line that leaks the Python type name. The operator-visible
+    class is the line, not this class (scratch-root-contract §1)."""
+
+
 def strict_scratch_root():
     """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
     round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
@@ -153,7 +161,7 @@ def strict_scratch_root():
     t = _os.environ.get("TMPDIR")
     if t:
         if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
-            raise RuntimeError(
+            raise ScratchRootUnusable(
                 "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
         return t
     return tempfile.gettempdir()
@@ -904,6 +912,10 @@ def dispatch(argv):
 def main(argv):
     try:
         status = dispatch(argv)
+    except ScratchRootUnusable as exc:
+        emit_err(f"repeat-control: could-not-evaluate: {exc}")
+        emit("REPEAT_CONTROL: setup_error")
+        status = EXIT_BY_ID["setup_error"]
     except Exception as exc:  # noqa: BLE001 - never let a traceback exit 1
         status = setup_failure(f"{type(exc).__name__}: {exc}")
```

Notes on the shape:

- The existing message string is reused unchanged, so the value it carries is still
  `%r` of the operator's TMPDIR (single-quoted) and the trailing `(could-not-evaluate)`
  is the one already in the message. No new literal duplicates the grammar.
- The catch is placed **before** `except Exception`, so `ScratchRootUnusable` never
  reaches `setup_failure()`, which is what printed `setup: RuntimeError:`.
- Exit 2 is `EXIT_BY_ID["setup_error"]` (2), i.e. the round's existing setup class.
- The break-control anchor is present verbatim at `tools/repeat-control.py:916` of the
  patched file (`anchor.txt`):
  `emit_err(f"repeat-control: could-not-evaluate: {exc}")`
- Only `strict_scratch_root()` allocates scratch in this tool (grep: one call site,
  `selftest()` line 629 at base), so the typed refusal covers the allocating mode and
  leaves the lazy modes (`--snapshot`, `-h`) untouched.

## Receipts (all under `T55W1ExecRepPatch-receipts/`)

### Baseline — base revision, unpatched (`baseline.rc/.stdout/.stderr`)

```
$ TMPDIR=/nonexistent/x python3 tools/repeat-control.py --selftest
rc=2
stdout: REPEAT_CONTROL: setup_error
stderr: repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/x' (could-not-evaluate)
```

Exit code was already 2, but the class line carried the Python type name — the
round-54 defect the C2 counter names.

### (a) unusable TMPDIR, patched (`a.rc/.stdout/.stderr`)

```
$ TMPDIR=/nonexistent/x python3 tools/repeat-control.py --selftest
rc=2
stderr (exactly 1 line):
repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/x' (could-not-evaluate)
stdout: REPEAT_CONTROL: setup_error
```

`grammar-check.txt` replays the frozen counter's regex against those bytes:

```
stderr_lines=1
grammar_match=True
RuntimeError_token=False
Traceback_token=False
stdout='REPEAT_CONTROL: setup_error\n'
```

### (b) declared-unset TMPDIR (`TMPDIR=`) (`b.rc/.stdout/.stderr`)

```
$ TMPDIR= python3 tools/repeat-control.py --selftest
rc=0
last line: SELFTEST: PASS (29 cases)
stderr: empty
```

### (c) fresh usable TMPDIR (`c.rc/.stdout/.stderr`)

```
$ TMPDIR=$S/tmp python3 tools/repeat-control.py --selftest
rc=0
last line: SELFTEST: PASS (29 cases)
stderr: empty
```

### (d) TMPDIR unset (`d-default.*`)

```
$ env -u TMPDIR python3 tools/repeat-control.py --selftest
rc=0 ; SELFTEST: PASS (29 cases)
```

### (e) lazy mode is unchanged under an unusable TMPDIR (`e-lazy-snapshot.*`)

```
$ TMPDIR=/nonexistent/x python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
rc=0
SNAPSHOT_OBSERVED id=controls_match exit=0
REPEAT_CONTROL: controls_match
```

i.e. the refusal is only reachable on the allocating path; a non-allocating mode
still exits its verdict, which is the C2 `lazy` arm's expectation for this tool.

`py-compile.txt`: `python3 -m py_compile tools/repeat-control.py` → ok.
Patched file sha256 `3ec77e5c92081ecb88e39acb356e0a36a00ef8941f176f915b2218fb8f2f9a5d`.

## Frozen C2 counter, run against base and against the patch

Counter file = the base revision's `.ufo/evidence/round-55/c2/measure.py` (sha above),
run as `--lane <my clone> --rev <rev> --work <fresh empty dir> --explain`. The patch
was committed in my clone (`d348d832fc76d390b51a3d124992107c3b9878d9`; toplevel asserted
equal to the clone before the commit) so the counter could clone and check it out.

| rev | grammar | repeat-control grammar | lazy | empty | usable | total |
|---|---|---|---|---|---|---|
| base `631cd6455e58` | 6/8 | **FAIL** | 5/5 | 13/13 | 12/13 | 19 |
| patch `d348d832fc76` | 7/8 | **ok** | 4/5 | 12/13 | 11/13 | 21 |

Receipts `c2-at-base.stdout`, `c2-at-patch.stdout`. The grammar delta is one line and
it is mine: `EXPLAIN grammar repeat-control --selftest rc=2 FAIL` → `rc=2 ok`.
`context-capture --selftest` remains the only grammar failure (other seat's item).

The non-grammar differences between my two runs are **not** caused by this patch; both
were reproduced by hand and are counter-shape artefacts of measuring this clone:

- `evidence-disposition --json` rc=2 with `"kind": "historical_input_unavailable",
  "message": "detached HEAD ... is on no branch or remote-tracking branch"`
  (`evidence-disposition-detached-head.json`). It fired at the patched rev only because
  that rev exists only as a detached HEAD; the base rev is a branch tip.
- `registry-check --selftest` rc=1 under the counter's `strace -f` wrapper, same at both
  revs, with `SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe,
  timeout-kills-setpgid-pipe)` (`registry-check-under-strace.stdout`); run without the
  tracer it is `rc=0 SELFTEST: PASS (51 cases)`.

Both are exactly what the lane's in-flight working-tree amendments to `c2/measure.py`
(amendment 1: `checkout -B` instead of detached; amendment 4: plain run for the exit
code, strace only for the mkdir census) address; I did not rely on those amended copies.

## Findings for the L1 (report only, nothing fixed by me)

1. **Anchor mismatch in the lane working tree.** The working tree already carries an
   equivalent hunk for this tool, but its emit line is
   `emit_err(f"repeat-control: could-not-evaluate: {message}")` (inside a
   `could_not_evaluate(message)` helper, working tree line 233). The exact anchor string
   the round's break control rewrites,
   `emit_err(f"repeat-control: could-not-evaluate: {exc}")`, occurs **0** times in the
   lane working tree and **1** time in my patched file (`lane-working-tree-emit-lines.txt`,
   `anchor.txt`). If integration adopts the helper form, keep the anchor string verbatim
   — or take this patch's inline form in `main()`.
2. **Frozen set is modified in the lane working tree.** `git diff --name-status --
   .ufo/evidence/round-55/` shows `M before/c2.stdout`, `M c1/measure.py`,
   `M c2/measure.py`, `M contract.json`, `M freeze.json` (full diff in
   `frozen-set-drift.diff`, names in `frozen-set-drift.names.txt`). The assignment
   declares these frozen and says to report, not fix; I therefore measured the base
   revision's copies, never the working-tree ones. `before/c2.stdout` is now empty in the
   working tree (it was the `grammar=6/8 ... total=18` receipt this seat's item quotes).
3. **Scratch wipe.** My seat scratch directory was deleted by an external cleanup while a
   counter run was in flight (only my directory; sibling directories survived). I rebuilt
   from the base revision and from then on wrote every receipt straight into
   `.ufo/waves/round-55/w1/T55W1ExecRepPatch-receipts/`, so all evidence above is durable
   and none of it lives only in `/fast/scratch`.

## Suggested main-agent verification

```sh
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/rc-check
git -C /tmp/rc-check checkout --detach 631cd6455e58dce969310b4c0466c3383d9f5108
git -C /tmp/rc-check apply -p1 < .../T55W1ExecRepPatch-receipts/patch.diff
cd /tmp/rc-check
TMPDIR=/nonexistent/x python3 tools/repeat-control.py --selftest; echo rc=$?   # 2, one grammar line
TMPDIR=            python3 tools/repeat-control.py --selftest; echo rc=$?      # 0
mkdir -p /tmp/rc-ok && TMPDIR=/tmp/rc-ok python3 tools/repeat-control.py --selftest; echo rc=$?  # 0
```
