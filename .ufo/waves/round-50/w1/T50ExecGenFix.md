# T50ExecGenFix — routed defect R49.1 (round-49 generator error paths F1–F3)

Seat: T50ExecGenFix (leaf). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`e3729de862f73ae080d98fcf522a7081ce16e40a` (lane tip at round start, 4afb060c… in the working
tree). Scratch root `/fast/scratch/hyaku/tameshi-r50/T50ExecGenFix` (deleted before yield; every
figure below comes from a run listed here and copied into this directory).
Tool installs: none needed (pacman is paused host-wide; no install was attempted).

Item: close routed item R49.1 — the round-49 generator's error paths
(`.ufo/waves/round-49/w2/T49W2RevGenCode.md` F1–F3; `corpus/lessons/round-49-verifier-spotcheck.md:122`,
routed defect 1). Work was done on a copy, as the item directs; the L1 copies it to `tools/`.

## Deliverable

| Field | Value |
|---|---|
| file | `.ufo/waves/round-50/w1/T50ExecGenFix/pbt-staged-id.py` (1119 lines) |
| sha256 | `a6e1253ad3542303ca31d66de69ccaa1caf32576c128dc6756daa332b9c8561e` |
| base bytes | `git -C … show e3729de8…:tools/pbt-staged-id.py` → sha256 `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05` (= the round-49 review's `0cbee392a83e`) |
| install | `cp .ufo/waves/round-50/w1/T50ExecGenFix/pbt-staged-id.py tools/pbt-staged-id.py` (L1; a verbatim copy keeps every line number cited below) |
| receipts | this directory: `red-before.stdout`, `green-after.stdout`, `red-before-f1.stdout`, `green-after-f1.stdout`, `red-before-f2.stdout`, `green-after-f2.stdout`, `base-capability.stdout`, `green-capability.stdout`, `cli-surface.stdout`, `diff.patch` |

## Findings and fixes

Each finding is the review's, re-derived at the base bytes, then fixed on the copy. Line numbers
are the deliverable's (= `tools/pbt-staged-id.py` after a verbatim copy).

### F1 — unreadable guard minted a violation instead of a setup refusal

- Base code: `main()` checked only `os.path.isfile` (base `:982`); `run_guard` caught only
  `TimeoutExpired` (base `:773`). An unreadable guard passes `isfile`, `python3 -I` exits 2 with
  empty stdout, `check()` calls that "stdout is not one JSON object", and the run prints a
  fabricated counterexample.
- Observed at base (`red-before-f1.stdout`): `chmod 000` guard, seed 1, 1 case →
  `VIOLATION index=0 exit 2, oracle expects 1` and
  `PBT_STAGED_ID: cases=1 violations=1 counterexample=0 …`, exit 1, one dump line.
- Fix: new `guard_problem()` (deliverable `:878-889`) refuses a non-regular **or unreadable**
  guard with the docstring's exit class, wired in `main()` (`:1110-1113`); `run_guard` also maps an
  `OSError` from `subprocess.run` to setup (`:789-790`). The guard is still never opened — only its
  mode is consulted (`os.access(guard, os.R_OK)`), so the generator's "never reads the guard's
  source" property holds.
- Observed after (`green-after-f1.stdout`): exit 2, stdout empty, no dump written, no work root
  left, `pbt-staged-id: guard is not readable: …/noread.py`.
- New selftest case `unreadable-guard-is-setup` (deliverable `:1047-1049`), which also asserts
  `VIOLATION` never appears in stdout and skips under uid 0 (root can read a mode-000 file).

### F2 — a mid-run write failure escaped as a traceback (exit 1, no last line)

- Base code: only the dump **open** was guarded (base `:794-799`); `dump.write`/`dump.flush`
  (base `:803-806`) and the case-file `write_text` calls in `run_guard` (base `:760-761`, `:768`)
  could raise uncaught.
- Observed at base (`red-before-f2.stdout`): `--dump /dev/full` →
  `Traceback … line 806, in run / dump.flush()` , exit 1, no `PBT_STAGED_ID` last line, and a
  `pbt-staged-id-*` work root leaked (the `dump.close()` in the base `finally` raised again before
  `rmtree`).
- Fix: a `SetupProblem` class (`:81-86`) carries every setup failure to one exit path
  (`run()` `:858-859`); the loop's dump write is guarded (`:838-844`), case-file writes and the
  guard invocation are guarded in `run_guard` (`:773-783`, `:789-790`), and the dump close is now
  allowed to fail without replacing the setup message (`:853-857`).
- Observed after (`green-after-f2.stdout`): exit 2,
  `pbt-staged-id: cannot write dump /dev/full: [Errno 28] No space left on device`, no leak.
- New selftest cases `dump-write-failure-is-setup` (`:1071-1082`, real `/dev/full`, skipped where
  the device is absent) and `case-write-failure-is-setup` (`:1051-1057`, the case-file path).

### F3 — one hygiene gap between `mkdtemp` and the `try/finally`

- Base code: `os.makedirs(case_dir)` at base `:791` ran before the `try:` that owned
  `shutil.rmtree(work)` (base `:815-817`), so a failure there leaked the work root.
- Fix: `workspace()` context manager (`:799-818`) creates the temp root, creates the case
  directory and removes the root in one `finally` that covers every later failure (dump open, dump
  writes, guard calls). `run()` now opens it at `:829-830`; the removal is `:818`.
- New selftest case `case-dir-failure-removes-work-root` (`:1059-1069`): injects an impossible
  case-directory path (`/proc/self/…`), asserts the failure is raised **and** that no new
  `pbt-staged-id-*` root exists afterwards. The error-path cases run under a private
  `tempfile.tempdir` (`:1029-1031`) so the leak check can neither see nor delete another run's work
  root (the round-49 review lost a probe to exactly that interference).

Also changed, deliberately: the docstring's exit-2 line now names the error classes the code
actually refuses (`:40-42`), and the selftest section header no longer claims "no subprocess"
(`:897-900`) — the error cases drive `main()` end to end.

## Red before, green after

The red run is the **test-only port**: the base bytes plus exactly these four new cases
(two `import` lines and the case block; `diff base.py base-plus-tests.py` shows nothing else).
That makes the red receipt a statement about the base implementation, not about a rewritten test.

| run | command | result |
|---|---|---|
| red | `cd $S && TMPDIR=$S/tmp-base-plus-tests python3 -I base-plus-tests.py --selftest` | exit 1, `cases=35 failed=4` — the four new cases FAIL, the 31 pre-existing cases PASS (`red-before.stdout`) |
| green | `cd $S && TMPDIR=$S/tmp-fixed python3 -I fixed.py --selftest` | exit 0, `cases=35 failed=0` (`green-after.stdout`) |
| re-run | same command, fresh TMPDIR | `cases=35 failed=0`, 0 leftovers (determinism + hygiene) |

The four new case names: `unreadable-guard-is-setup`, `case-write-failure-is-setup`,
`case-dir-failure-removes-work-root`, `dump-write-failure-is-setup`.

## Hard constraint (no-harm monitor): the frozen capability line is byte-equal

```
$ G=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py   # sha256 03a796c5…
$ TMPDIR=$S/tmp-cap python3 -I fixed.py --guard "$G" --seed 4949 --cases 400 --dump $S/fixed.dump.jsonl
[exit 0]
PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31
```

This is character-for-character the base run's last line (`base-capacity.stdout`), i.e. the exact
string `no-harm.sh:34` demands. The dump is byte-identical too —
`ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28` for both base and fixed,
`cmp` silent — which is the same hash the round-49 review recorded for the frozen dump. Since the
dump is a per-case record of the drawn case and the class counts are per-case recounts, an
identical dump proves the RNG draw order and the recipe order are unchanged: `random.Random(seed)`,
one `shuffle(order)`, then `RECIPES[order[index % len]](rnd)` per index, in that order
(deliverable `:823-826`, `:836-837`; base `:785-788`, `:802`). The interface is untouched:
`--guard --seed --cases --dump --selftest`, the guard argv shape, the `PBT_STAGED_ID` last line and
the `CLASS`/`TIME` lines.

## Non-regression probes (`cli-surface.stdout`)

- Exit-2 surface unchanged: no arguments, `--cases 0`, missing `--cases`, missing guard, guard is a
  directory — all exit 2 with the base messages; the pre-existing "dump is a directory" path yields
  **byte-identical stderr** at base and fixed.
- A real oracle disagreement is still a violation: a stub guard answering
  `{"verdict": "answered", "collision_count": 999}` → exit 1, `VIOLATION index=0 field set
  mismatch…`, `counterexample=0`, one dump line. The fix does not route violations into setup.
- The module imports with no side effect and exposes `check`, `oracle_case`, `case_classes`, `run`,
  `run_guard`, `main`, plus the new `workspace`/`guard_problem`/`SetupProblem`; the round-50
  shrinker imports the REV copy, and `oracle_case`/`check` are untouched.
- `python3 -I <file> --selftest` is still the only selftest entry point; no new flags.

## Diff (base → deliverable)

```diff
@@ docstring, imports, SetupProblem
-2 = setup problem (bad arguments, unwritable dump, unreadable guard).  Last stdout
+2 = setup problem (bad arguments, unreadable guard, unwritable dump or case file,
+unusable work directory).  Last stdout
+import contextlib
+import io
+
+class SetupProblem(Exception):
+    """The run cannot start or continue: exit 2, never a violation (the docstring's exit class).
+
+    Raised for an unusable guard, an unwritable dump or case file, and an unusable work
+    directory, so a broken environment can never mint a counterexample.
+    """

@@ run_guard (case files + guard exec)
-    write_text(registry_path, case['registry'])
-    write_text(staged_path, case['staged'])
     argv = [sys.executable, '-I', guard, '--registry', registry_path,
             '--staged', staged_path]
-    if case['map'] is None:
-        if os.path.exists(map_path):
-            os.unlink(map_path)
-    else:
-        write_text(map_path, json.dumps(case['map']))
-        argv += ['--map', map_path]
+    try:
+        write_text(registry_path, case['registry'])
+        write_text(staged_path, case['staged'])
+        if case['map'] is None:
+            if os.path.exists(map_path):
+                os.unlink(map_path)
+        else:
+            write_text(map_path, json.dumps(case['map']))
+            argv += ['--map', map_path]
+    except OSError as exc:
+        raise SetupProblem('cannot write the case files in %s: %s' % (case_dir, exc))
     argv.append('--json')
     try:
         proc = subprocess.run(argv, capture_output=True, timeout=GUARD_TIMEOUT, cwd=case_dir)
     except subprocess.TimeoutExpired:
         return {'exit': 124, 'json': None, 'stdout': b'', 'stderr': b'timeout'}
+    except OSError as exc:
+        raise SetupProblem('cannot run guard %s: %s' % (guard, exc))

@@ workspace (new) — the temp root is removed on every exit
+@contextlib.contextmanager
+def workspace(case_dir_name='case'):
+    try:
+        work = tempfile.mkdtemp(prefix='pbt-staged-id-')
+    except OSError as exc:
+        raise SetupProblem('cannot create a work directory: %s' % exc)
+    try:
+        case_dir = os.path.join(work, case_dir_name)
+        try:
+            os.makedirs(case_dir, exist_ok=True)
+        except OSError as exc:
+            raise SetupProblem('cannot create the case directory: %s' % exc)
+        yield case_dir
+    finally:
+        shutil.rmtree(work, ignore_errors=True)

@@ run() — one setup exit path, guarded dump writes
-    work = tempfile.mkdtemp(prefix='pbt-staged-id-')
-    case_dir = os.path.join(work, 'case')
-    os.makedirs(case_dir, exist_ok=True)
+        with workspace() as case_dir:
+            try:
+                dump = open(dump_path, 'w', encoding='utf-8')
+            except OSError as exc:
+                raise SetupProblem('cannot write dump %s: %s' % (dump_path, exc))
+            try:
+                for index in range(cases):
+                    ...
+                    try:
+                        dump.write(json.dumps({...}, sort_keys=True) + '\n')
+                        dump.flush()
+                    except OSError as exc:
+                        raise SetupProblem('cannot write dump %s: %s' % (dump_path, exc))
+            finally:
+                try:
+                    dump.close()
+                except OSError:
+                    pass                  # a full disk must not replace the setup message
+    except SetupProblem as exc:
+        return _setup_error(str(exc))

@@ guard_problem (new) + main() wiring
+def guard_problem(guard):
+    """Why the guard cannot be used at all, or None (exit 2, never a violation).
+
+    ``os.path.isfile`` alone admits a file the interpreter cannot open: ``python3 -I`` then
+    exits 2 with empty stdout and the run used to report that as a violation with a made-up
+    counterexample.  The guard is still never opened here -- only its mode is consulted.
+    """
+    if not os.path.isfile(guard):
+        return 'guard is not a regular file: %s' % guard
+    if not os.access(guard, os.R_OK):
+        return 'guard is not readable: %s' % guard
+    return None
-    if not os.path.isfile(guard):
-        return _setup_error('guard is not a regular file: %s' % guard)
+    problem = guard_problem(guard)
+    if problem:
+        return _setup_error(problem)

@@ selftest: four new cases (block appended before the summary; summary format unchanged)
+    # ---- error paths (routed defect R49.1) …
+    def skip(name, why): …
+    def temp_roots(): …
+    scratch = tempfile.mkdtemp(prefix='pbt-selftest-')
+    saved_tempdir = tempfile.tempdir
+    tempfile.tempdir = os.path.join(scratch, 'tmp')   # private: a leak check must not see or
+    os.makedirs(tempfile.tempdir)                     # touch another run's work root
+    … unreadable-guard-is-setup / case-write-failure-is-setup /
+      case-dir-failure-removes-work-root / dump-write-failure-is-setup …
+    finally:
+        tempfile.tempdir = saved_tempdir
+        … chmod back, rmtree(scratch) …
```

The excerpt above abbreviates repetitive bodies with `…` and folds hunk headers; the unabridged
unified diff is `diff.patch` (286 lines, +156/−40, from `diff -u base.py fixed.py`, base = the blob
at `e3729de8…:tools/pbt-staged-id.py`). Every changed region of the file appears above at least
once, and the only non-comment deletions are the moved `write_text`/`makedirs`/dump-open block and
`main()`'s `isfile` check; no oracle, recipe, classifier, `check()` or CLI text was touched.

## Hand-off for the C1 row (R49.1) — for the L1 / wave-2 C1 seat

The row is `{"id": "R49.1", "status": "fixed", …}` only once the fix is **in the tree**: copy the
deliverable to `tools/pbt-staged-id.py` and commit it. The counter's `fixed` branch requires
`commit` to be a 40-hex commit that is an ancestor of REV, **not** an ancestor of
`e3729de8…` (i.e. post-base), and to *touch* every cited path. So cite the `tools/` path, not only
this escrow copy. A verbatim copy keeps these line numbers.

Three evidence items, each verified locally against the counter's rules (excerpt verbatim in the
cited lines at REV, span ≤ 30, 15–400 chars after whitespace collapse, no acknowledgement word in
the span, excerpt **absent** from `tools/pbt-staged-id.py` at `e3729de8…`):

1. `{"path": "tools/pbt-staged-id.py", "lines": "878-886", "excerpt": "``os.path.isfile`` alone admits a file the interpreter cannot open: ``python3 -I`` then exits 2 with empty stdout and the run used to report that as a violation with a made-up counterexample."}`
   — keyed by `os.path.isfile`; the F1 fix itself.
2. `{"path": "tools/pbt-staged-id.py", "lines": "40-42", "excerpt": "2 = setup problem (bad arguments, unreadable guard, unwritable dump or case file, unusable work directory)."}`
   — keyed by `unreadable guard`; the documented exit class now matches the code.
3. `{"path": "tools/pbt-staged-id.py", "lines": "799-803", "excerpt": "The run's temp root: created here, removed here, whatever happens next. The removal covers every failure after mkdtemp"}`
   — the F3 invariant (not keyed; the counter needs only one keyed item).

Suggested `note`: "F1/F2/F3 fixed with four new selftest cases (red on base: cases=35 failed=4; green: 35/0); capability line and dump byte-identical." Suggested `seat`: `T50ExecGenFix`.
`commit`: the post-base commit that adds `tools/pbt-staged-id.py` — not mine to make.

Semantic support (the counter cannot see it): every ask of the item is met in the tree —
F1 exits 2 for an unreadable guard (was exit 1 + a fabricated counterexample), F2's dump/case-file
write failures exit 2 instead of a traceback, F3's work root is removed on every failure after
`mkdtemp`, and each fix has a case that fails on the base bytes (`red-before.stdout`) and passes on
the deliverable (`green-after.stdout`).

## Risks and limits

- `/dev/full` is Linux-specific: the F2 end-to-end case prints `CASE … SKIP` elsewhere, and the
  case-file case still covers the same `SetupProblem` route. Under uid 0 the unreadable-guard case
  skips (root can read mode 000); here uid is 1000 and both cases ran.
- The selftest assigns `tempfile.tempdir` for the length of the error-path block and restores it;
  this keeps the leak check from observing or deleting a concurrent run's work root, but it is a
  module-global the selftest mutates. It is restored in a `finally`.
- `case-dir-failure-removes-work-root` relies on `mkdir` under `/proc/self` failing; that holds for
  uid 1000 and for root on this host, but it is an environment assumption (an unprivileged,
  non-Linux host could make the case fail rather than skip).
- The fix deliberately keeps `CLASS_MIN = 20` and every other frozen constant; F4/F5/F6 from the
  round-49 review were INFO and are untouched.
- Nothing here is a verdict: the deciding runs are the L1's. The receipts show what these
  commands printed, no more.
- Scratch `/fast/scratch/hyaku/tameshi-r50/T50ExecGenFix` removed; no writes outside this wave dir
  and the scratch root; no git/jj mutation in the lane or the fleet repo.

## Summary

- R49.1 closed on a copy: `pbt-staged-id.py` sha256 `a6e1253a…`, from base `0cbee392a83e`.
- F1: unreadable guard now exits 2 (`guard_problem`, `os.access R_OK` + `OSError` → setup), no fabricated counterexample.
- F2: dump/case-file write failures and the dump close are guarded; a traceback exit 1 becomes a setup exit 2.
- F3: `workspace()` removes the temp root on every failure after `mkdtemp`; leak check runs under a private TMPDIR.
- Four new selftest cases; red-before port fails exactly those four (`cases=35 failed=4`), deliverable `cases=35 failed=0`.
- Hard constraint met: base last line byte-equal, dump sha `ca62402b…` identical (RNG draw order unchanged).
- Interface, exit surface and violation path unchanged; `/dev/full` and uid-0 cases skip where the fixture cannot exist.
- L1 must copy the file to `tools/pbt-staged-id.py` and commit; the three cited evidence items then resolve for the C1 row.
