# T53W2CritTools — wave-2 critic: attack on the 7 tool patches at C**

- Seat: T53W2CritTools (wave 2 of 2, tameshi round 53, hyaku run 10)
- Target revision: C** = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`
- All runs executed in a `--shared` clone of the lane at C** under
  `/fast/scratch/hyaku/tameshi-r53/w2/T53W2CritTools/lane-cxx`
  (`git rev-parse HEAD` = C**, tree clean); clone deleted after the runs.
- Host note: uid 1000 (vgpnk), not root — chmod 555 write tests are meaningful.
  `/tmp` on this host is shared with ~40 live sibling seats; all /tmp
  attributions below were proven by strict before/after listings plus an
  idle control, not assumed.

## (a) strict_scratch_root semantics — VERIFIED

All 7 tools carry a byte-identical helper (md5 `fcf865d69a394f8d55a337ec9004c0c3`
of the function body extracted via `git show C**:tools/<tool>.py` for all 7).

Unit harness (function copied verbatim from the C** bytes, run in clean
subprocesses):

```
TMPDIR=<missing dir>   → RuntimeError: ... TMPDIR is not a usable directory: '<missing>' (could-not-evaluate)   [isdir branch]
TMPDIR=<chmod 555 dir> → RuntimeError: ... (could-not-evaluate)                                                [access W_OK branch]
TMPDIR=<regular file>  → RuntimeError: ... (could-not-evaluate)                                                [isdir branch]
TMPDIR=""              → root='/tmp'  → mkdtemp created under /tmp     [empty string hits the falsy `if t:` branch → return tempfile.gettempdir() → platform default]
TMPDIR unset           → root='/tmp'  → mkdtemp created under /tmp     [same branch: platform default]
TMPDIR=<valid dir>     → root=<that dir> → created there               [positive control]
```

Branch documentation for the empty-string case: `t = _os.environ.get("TMPDIR")`
returns `""`, which is falsy, so the empty-string case takes the
`return tempfile.gettempdir()` branch — i.e. it is treated exactly as unset.
Observed platform default on this host is `/tmp` (gettempdir honors TMPDIR,
falling back to /tmp).

Behavioral confirmation through the real tools:

```
registry-check --selftest, TMPDIR=<missing>   → exit 1, traceback naming
  "cannot create clone scratch under the scratch root: TMPDIR is not a usable
  directory: ... (could-not-evaluate)"; grep -c REGISTRY_CHECK = 0 verdict lines
  (CTL_CR47 shape exactly as the contract requires)
registry-check --selftest, TMPDIR=<chmod 555> → exit 1, same message
registry-check --selftest, TMPDIR=""          → exit 0, SELFTEST: PASS (51 cases)
registry-check --selftest, TMPDIR unset       → exit 0, SELFTEST: PASS (51 cases)
```

## (b) tempfile.gettempdir() cache — VERIFIED, no split-root in practice

Call-site inventory at C** (grep over all 7 tools for
mkdtemp/TemporaryDirectory/NamedTemporaryFile/gettempdir):

- bash-witness-study.py: two mkdtemp calls in `cmd_selftest` — the second is
  `dir=private_root`, i.e. nested inside the first (strict) dir. Same effective
  root. No divergence.
- env-diff.py: `execute()` uses `TemporaryDirectory(dir=strict_scratch_root())`
  (line 75); `selftest()`'s pin fixture uses `TemporaryDirectory(prefix=
  "tameshi-r21-envdiff-pin.")` with NO dir= (line 181) → gettempdir(). Under a
  stable process env both resolve to the same root.
- context-capture / evidence-disposition / pin-disposition / repeat-control: one
  mkdtemp each, all strict.
- registry-check.py: two strict sites (selftest + clone_lane_at_rev).

Hazard demonstration: gettempdir() caches its first result
(`tempfile.tempdir`); a micro-demo showed first==second even after mutating
os.environ["TMPDIR"] mid-process. That divergence would matter only if a tool
changed TMPDIR mid-run — `grep` over tools/*.py for environ writes/putenv on
TMPDIR finds nothing, so no in-tool divergence is possible. env-diff --selftest
with TMPDIR redirected landed BOTH `tameshi-r21-envdiff.*` (strict) and
`tameshi-r21-envdiff-pin.*` (gettempdir) under the redirected scratch
(witnessed live by polling the scratch during the run).

## (c) env-diff --selftest with TMPDIR redirected — VERIFIED

```
ENVDIFF_SELFTEST: 9/9 pass (exit 0)
scratch during run: tameshi-r21-envdiff.* (x2), tameshi-r21-envdiff-pin.* (x1)
/tmp before-vs-after diff during the same run: only mori-r56-c1-* entries,
which belong to sibling seat MoriR56 (visible in my peer roster) — nothing
from env-diff.
```

The probe sandboxes are bwrap `--tmpfs /tmp --bind <tmp> /tmp/w`; the sandbox
/tmp is a tmpfs, the host /tmp is untouched.

## (d) all 6 selftests with TMPDIR=redirected scratch — VERIFIED, all pass

TMPDIR=/fast/scratch/hyaku/tameshi-r53/w2/T53W2CritTools/selftest-tmp:

| tool | exit | verdict |
|---|---|---|
| registry-check.py --selftest | 0 | SELFTEST: PASS (51 cases) |
| env-diff.py --selftest | 0 | ENVDIFF_SELFTEST: 9/9 pass |
| evidence-disposition.py --selftest | 0 | SELFTEST: PASS (66/66) |
| pin-disposition.py --selftest | 0 | SELFTEST: PASS (19/19) |
| repeat-control.py --selftest | 0 | SELFTEST: PASS (29 cases) |
| context-capture.py --selftest | 0 | SELFTEST: PASS (49/49) |

Fixture placement witnessed under the redirected scratch:
`tameshi-r17-registry-check-selftest.*`, `tameshi-registry-check-*` (clone
dirs), `tameshi-r13-pin-disposition-selftest.*`, `tameshi-r21-envdiff.*`,
`tameshi-r21-envdiff-pin.*`. selftest-tmp was empty after each run — the
selftests clean up their own trees.

C2 regex sanity at C**: `git grep -E 'dir\s*=\s*["'"'"']/tmp' C** -- tools/`
→ 0 matches.

Could-not-evaluate sweep (TMPDIR=<missing dir>) for all 6 selftests plus the
witness subcommand: every one exits non-zero, prints a message naming scratch
creation with "(could-not-evaluate)", and prints zero verdict lines:

```
env-diff.py               exit=1 (uncaught RuntimeError traceback)
evidence-disposition.py   exit=1 (uncaught RuntimeError traceback)
pin-disposition.py        exit=1 (uncaught RuntimeError traceback)
registry-check.py         exit=1 (uncaught RuntimeError traceback)
repeat-control.py         exit=2 (caught: "REPEAT_CONTROL: setup_error")
context-capture.py        exit=2 (caught: "SELFTEST: FAIL (setup error: ...)")
bash-witness-study.py selftest exit=1 (uncaught RuntimeError traceback)
```

## (e) bash-witness-study reachability — VERIFIED: reachable, not dead code

The tool has no `--selftest` flag: `python3 tools/bash-witness-study.py
--selftest` → exit 64 usage error ("the following arguments are required:
mode"; choices `{declare,run,rerun,count,check,selftest}`). The patched line
sits in `cmd_selftest`, dispatched from the `selftest` subcommand
(`handlers = {..., "selftest": cmd_selftest}` at line 1780):

```
TMPDIR=<scratch> python3 tools/bash-witness-study.py selftest
  → exit 0, WITNESS_SELFTEST: 51/51 pass, VERDICT: PASS
TMPDIR=<missing> ... selftest
  → exit 1, RuntimeError ... (could-not-evaluate)
```

The second mkdtemp in cmd_selftest (`dir=private_root`) nests inside the strict
root, so both trees honor TMPDIR.

## Per-tool verdicts

- tools/registry-check.py — VERIFIED
- tools/env-diff.py — VERIFIED
- tools/evidence-disposition.py — VERIFIED
- tools/pin-disposition.py — VERIFIED
- tools/repeat-control.py — VERIFIED
- tools/context-capture.py — VERIFIED
- tools/bash-witness-study.py — VERIFIED (reachable via `selftest` subcommand)

## Observations outside the C2 contract (calibration, not ISSUEs)

1. Stale /tmp wording in usage docs (behavior honors TMPDIR; docs predate it;
   none matches the C2 regex; SKILL.md's tool rows already say `$TMPDIR`):
   - tools/evidence-disposition.py:181 "`--selftest` builds isolated /tmp fixtures."
   - tools/pin-disposition.py:36 "isolated /tmp git fixtures"
   - tools/repeat-control.py:66-67 "under `/tmp/tameshi-r12-repeat-control-selftest.*`"
2. could-not-evaluate surfacing is inconsistent: uncaught RuntimeError
   traceback (exit 1) in 5 tools vs. caught setup_error (exit 2) in
   repeat-control/context-capture. The contract's CTL_CR47 predicate (non-zero,
   names scratch creation, no verdict lines) is met by both shapes.
3. Host noise attribution: `/tmp/tameshi-r4-2-regression.*` dirs appear and
   vanish continuously — proven by an idle 40 s control (no selftest of mine
   running) + full ps snapshot to come from sibling seat T53W2Read14 running
   `tools/tally-audit-v3.py --selftest`. tally-audit-v3.py is NOT one of the 7
   patched tools; its `/tmp/...` fixture strings do not match
   `dir\s*=\s*["']/tmp`. Any future /tmp-isolation check on this host must
   account for concurrent peers.

## Bottom line

The strict_scratch_root patch holds at C** on every attacked axis: semantics
(missing/readonly/file → could-not-evaluate; empty/unset → platform default),
no gettempdir split-root, env-diff fully TMPDIR-contained, 6/6 selftests pass
under redirection, and the bash-witness patched line is live code reachable
via its `selftest` subcommand. No ISSUE against the 7 patches. The only
defects found are three stale `/tmp` doc lines in tool usage text — cosmetic,
outside the C2 predicate.
