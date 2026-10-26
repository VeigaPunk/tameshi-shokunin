# T47ExecObsC — C1 dependence observation (4 statements, two runs + placement control)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
REV `9acfbe21435e1976636a276448dee1d5e7155915`, base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`.
Read-only on the lane; the only file written is this report. No git/jj mutating command, no
install, no pacman transaction, no write to `shokuknow` or the fleet repo.

## 0. Environment blocker that changed the run shape (read first)

First attempt at the literal item command died **before any statement ran**:

```
C1_R47: clone/checkout failed          # both work dirs, exit 2
```

Cause: host-wide ENOSPC. `/tmp` is its own 128G fs and was at 100% (64M free); the counter's
`setup_profile` clones the lane twice per profile (12 clones/run, ~2.3G/run) and `git checkout`
aborted with `No space left on device`. I removed my own aborted clones (3.4G), then, per the L1's
mid-wave note, moved the work trees off `/tmp`:

```
/tmp/tameshi-r47-T47ExecObsC/w1,w2  ->  /home/vgpnk/scratch-t47c/w1,w2   (root fs, 573G free)
```

The literal item paths still resolve; the bytes live on the root fs. All four runs below completed
with `total` accounting intact (no clone error, `unobservable=0`).

## 1. Exact commands

Run 1 (`w1`) and run 2 (`w2`), identical but for `--work` — these are the literal item commands:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /tmp/tameshi-r47-T47ExecObsC/w1 \
  --only "effective expectation reconciliation,retained invocation-context gate,hermetic env-differential probe,callback-authoritative wave accounting" \
  --emit
```

Run 3 (`w3`) and run 4 (`w4`), same statement list, `--work /var/tmp/tameshi-r47-T47ExecObsC/w{3,4}`
(placement control, see §5). Single-statement placement probes `v1`,`v2`:
`--only "hermetic env-differential probe"` into `/var/tmp/tameshi-r47-T47ExecObsC/v{1,2}`.

Runs were launched two-at-a-time in one shell and waited on. Seat probes only; `C1_R47_PARTIAL`
was the only verdict line produced, and it is never a pass.

## 2. PROFILES lines, both runs (byte-identical)

```
PROFILES effective expectation reconciliation: P0=SELFTEST: PASS (66/66)|0 P1=SELFTEST: PASS (66/66)|0 P2=SELFTEST: PASS (66/66)|0 P3=UNOBSERVABLE|exit=1 P4=SELFTEST: PASS (66/66)|0 P5=SELFTEST: PASS (66/66)|0
PROFILES retained invocation-context gate: P0=SELFTEST: PASS (49/49)|0 P1=SELFTEST: PASS (49/49)|0 P2=SELFTEST: PASS (49/49)|0 P3=SELFTEST: PASS (49/49)|0 P4=SELFTEST: PASS (49/49)|0 P5=SELFTEST: PASS (49/49)|1
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 2/9 pass|1 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 2/9 pass|1 P4=ENVDIFF_SELFTEST: 1/9 pass|1 P5=ENVDIFF_SELFTEST: 2/9 pass|1
PROFILES callback-authoritative wave accounting: P0=ACCOUNTING_SELFTEST: 8/8 pass|0 P1=ACCOUNTING_SELFTEST: 8/8 pass|0 P2=ACCOUNTING_SELFTEST: 8/8 pass|0 P3=ACCOUNTING_SELFTEST: 8/8 pass|0 P4=ACCOUNTING_SELFTEST: 8/8 pass|0 P5=ACCOUNTING_SELFTEST: 8/8 pass|0
C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=4 mismatches=0 unparsed=4 unobservable=0 dep_mismatch=0 unpinned=0 append_only=1 total=4 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
```

`w1.log` and `w2.log` are byte-identical (`diff` empty); `w3.log` and `w4.log` are byte-identical.
`unparsed=4` is expected at the freeze (no `deps` clause in the standing rows).

## 3. Per-statement observation (run1 = run2 = w3 = w4 unless noted)

Tuples are `(picked line, exit[, tool sha256])` as `comparable()` reads them for `kind=cap`
(`line, exit`).

| statement | P0 | P1 | P2 −bwrap | P3 −jj | P4 −node | P5 decoy fleet-root | deps observed |
|---|---|---|---|---|---|---|---|
| effective expectation reconciliation | `SELFTEST: PASS (66/66)`, 0 | same, 0 | same, 0 | **UNOBSERVABLE**, 1 | same, 0 | same, 0 | `jj` |
| retained invocation-context gate | `selftest-new-full-count: PASS summary (SELFTEST: PASS (49/49))`, 0 | same, 0 | same, 0 | same, 0 | same, 0 | **same line**, **1** | `fleet-root` |
| hermetic env-differential probe | `ENVDIFF_SELFTEST: 9/9 pass`, 0 | 9/9, 0 | **2/9**, 1 | 9/9, 0 | **8/9**, 1 | 9/9, 0 | `bwrap,node` |
| callback-authoritative wave accounting | `ACCOUNTING_SELFTEST: 8/8 pass`, 0 | same, 0 | same, 0 | same, 0 | same, 0 | same, 0 | `none` |

Tool sha256 prefixes emitted (identical in all runs): `39ee5c5effd9`, `7e4519d9a0ea`,
`e8b47ab7cf23`, `96b3038a77f8`.

**Run 1 vs run 2:** no tuple differs. No nondeterministic statement, no profile-specific
instability, across six profiles × four statements × two runs (and again at a second placement).
The `P3` `UNOBSERVABLE` for statement 1 is deterministic, not flaky.

Note the row for statement 3 in §2 is the **`/tmp` placement** (2/9 at P1). At the `/var/tmp`
placement the same statement reads:

```
PROFILES hermetic env-differential probe: P0=ENVDIFF_SELFTEST: 9/9 pass|0 P1=ENVDIFF_SELFTEST: 9/9 pass|0 P2=ENVDIFF_SELFTEST: 2/9 pass|1 P3=ENVDIFF_SELFTEST: 9/9 pass|0 P4=ENVDIFF_SELFTEST: 8/9 pass|1 P5=ENVDIFF_SELFTEST: 9/9 pass|0
```

and the counter emits `deps bwrap,node` there instead of `deps env,node`. §5 explains why.

## 4. Root causes (path:line)

### 4.1 effective expectation reconciliation — `deps jj` (legitimate, declare)

`python3 tools/evidence-disposition.py --selftest`, P3 (jj dropped from the shim PATH):

```
SELFTEST_CASE v2-jj-prebookmark-branch-tip FAIL (setup/process error: FileNotFoundError: [Errno 2] No such file or directory: 'jj')
SELFTEST_CASE v2-jj-branch-tip FAIL (setup/process error: FileNotFoundError: ... 'jj')
SELFTEST_CASE v2-jj-without-lane-branch FAIL (setup/process error: FileNotFoundError: ... 'jj')
SELFTEST: FAIL (3/66 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch; ...)
```

* `tools/evidence-disposition.py:2035` `def _jj(lane, *argv)`, the exec at **:2041**
  `["jj"] + list(argv)` — resolved through PATH, so an absent `jj` raises `FileNotFoundError`
  inside the case body and is rendered by the per-case handler at **:2409**
  (`"setup/process error: {}: {}"`). The tool itself ran to completion (exit 1, full case list).
* Fixtures that need it: `:2162` `_jj_init_fixture_repo`, `:2168-2185`, `:2190-2223`, `:2247-2250`;
  cases registered at `:2879-2889`.
* The requirement is already declared by the tool: docstring **:121**
  “Selftest also requires `jj` for its isolated colocated-repository cases.”
* Verdict: **legitimate prerequisite — declare `jj`.** Shedding it would delete the
  jj-workspace binding cases (`:492-495`), i.e. the tool's own subject matter.

### 4.2 retained invocation-context gate — `deps fleet-root` (legitimate, brittle)

`python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…`, P5 (decoy fleet root bound over
`/home/vgpnk/Projects/shokunin`, containing only a `scripts/sources-census.sh` stub that exits 7):

```
sources-census: FAIL exit=7 (expected 0)
sources-census-ok-line: FAIL ok line absent
```

— everything else PASS; picked line unchanged, exit 1.

* `.ufo/evidence/round-15/verify.py:105`
  `CENSUS_TOOL = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` (absolute, outside the
  repo); argv built at **:835-836** with a second hardcoded root
  (`--root /home/vgpnk/Projects/shokunin`), invoked at **:837**.
* Verdict: **legitimate prerequisite — declare `fleet-root`.** The census subject lives in the
  fleet root, not in the clone, so a bare clone cannot satisfy it. It is however an *accident of
  binding*: the statement reaches outside its own checkout by absolute path instead of taking a
  root argument. Not sheddable without changing the runner's subject; note the brittleness.

### 4.3 hermetic env-differential probe — `deps bwrap,node` (declare); `env` seen only under `/tmp` is a harness artifact

`python3 tools/env-diff.py --selftest`.

**(a) `bwrap`** — P2 (bwrap dropped): `2/9 pass`, all seven sandbox cases FAIL, exit 1.

* `tools/env-diff.py:58` `bwrap = bwrap or shutil.which("bwrap")`, returning
  `{"error": "BWRAP_UNAVAILABLE"}` at **:59**; every `probe()` case goes through `execute()`
  (`:110`, `:57-90`) and is classified `unavailable` (`:98-101`).
* The two survivors are `missing-bwrap` (`:162`, names a nonexistent binary explicitly) and
  `pin-mismatch-public-cli` (`:185-190`, launches no sandbox).
* Verdict: **legitimate prerequisite — declare `bwrap`**; the tool's whole method is a sandboxed
  profile matrix.

**(b) `node`** — P4 (node dropped): `8/9 pass`, only `pin-mismatch-public-cli` FAILs, exit 1.

* The selftest’s public-CLI case (`:185`) runs the tool non-selftest; that path probes the report’s
  host block at **:234-236** `for command in ("node", "bash"): subprocess.run([command, "--version"], …)`,
  reached **before** `a.out.write_text(...)` at `:239`. With `node` absent this raises
  `FileNotFoundError` (`OSError`), caught at **:240-242** → `ENVDIFF_SETUP: …` and **exit 2**,
  while the case demands `child.returncode == 1` and a written receipt (`:190`) → FAIL.
  Reproduced directly: `OSError: [Errno 2] No such file or directory: 'node'`.
* Verdict: **legitimate but thin — declare `node`.** `node` is used only for the report’s
  `host.node` string, never for a measurement; the dependence is sheddable by making the version
  probe tolerant (catch `OSError` per command), at the cost of a weaker receipt. As the tool
  stands, declare it.

**(c) `env`, only under the `/tmp` placement — harness artifact, not a statement property.**

P1 at `--work /tmp/...`: `ENVDIFF_CASE invariant|tz|locale|home|columns|repeat|timeout FAIL`,
`2/9 pass`. Mechanism:

* the counter builds the profile PATH shim **inside the work dir**:
  `.ufo/evidence/round-47/calibration/measure.py:182-183` `shim = os.path.join(work, prof, 'shim')`,
  exported as `PATH` at `:188`;
* the tool under test replaces `/tmp` inside its sandbox:
  `tools/env-diff.py:69` `"--tmpfs", "/tmp"`.

With `--work` under `/tmp`, the shim path is masked by the tmpfs, so `bash` cannot be exec’d
inside the sandbox. Proven with the counter’s own P1 shim and the tool’s own argv:

```
env -i PATH=/tmp/tameshi-r47-T47ExecObsC/w1/P1/shim … bwrap --ro-bind / / --dev /dev --proc /proc \
    --tmpfs /tmp --bind $T /tmp/w --unshare-net --die-with-parent --chdir /tmp/w bash -c 'echo INSIDE_OK'
  -> bwrap: execvp bash: No such file or directory     (rc=1)
env -i PATH=/usr/bin:/bin … same argv ->
  -> INSIDE_OK                                          (rc=0)
```

Every `execute()`-based case then classifies `unavailable`, `timeout` included (`:163` expects a
`TIMEOUT`, gets a fast exec failure). Under `--work /var/tmp/...` the shim survives `--ro-bind / /`
and P1 is `9/9`, so **the statement does not intrinsically need `env`** — it passes under a clean
`PATH/HOME/LANG/LC_ALL/TZ/TMPDIR` environment whenever `bash` resolves.

* Verdict: **`env` is an accident of harness placement; do not declare it if the deciding run uses
  a work dir outside `/tmp`.** Declare `bwrap,node`.

### 4.4 callback-authoritative wave accounting — `deps none` (correct)

All six profiles `8/8 pass`, exit 0; `FINDING: SELFTEST_PASS`. Only externals are children launched
with the absolute `sys.executable` (`tools/wave-accounting.py:169`) under a `GIT_`-stripped copy of
the inherited env (`:155`); no `jj`, `bwrap`, `node`, no absolute fleet path. `none` is accurate.

## 5. Differential-masking defect found in the counter (advisory, no edit made)

`measure()` compares each variant only against P1. When a statement is **already broken in P1**
(the `/tmp` placement), P2/P3/P5 collapse onto P1 and their real dependences vanish from the
deps set — the observed set shrinks from the truthful `bwrap,node` to `env,node`, and `bwrap` is
under-reported by construction. Evidence: at the `/tmp` placement, statement 3’s P2/P3/P5 obs
files are **byte-identical to P1** (`diff` → identical for all three), and the deps set differs
from the `/var/tmp` placement of the same rev, same counter, same statements.

Consequence for C1: the deps clause for `hermetic env-differential probe` is a function of the
deciding run’s `--work` location.

* `--work` outside `/tmp` → truthful `deps bwrap,node` (P1 healthy, all four variants informative).
* `--work` inside `/tmp` → `deps env,node`, which asserts the tool does *not* need bwrap — false
  (P2 is 2/9).

Recommendation to the L1: decide with `--work` outside `/tmp` (as the L1’s own note directs), i.e.
write `deps jj` / `deps fleet-root` / `deps bwrap,node` / `deps none`; and, if the counter is to be
trusted as a deps oracle rather than a one-off, either (i) place the shim outside the paths the
statement may mask (not inside `work/<prof>/shim`), or (ii) make `measure.py` refuse a work dir that
the statement’s own sandbox would mask. That is a harness seam, not a statement or SCORECARD edit.

## 6. Flags requested by the item

* **P1 differing from P0 only by a path/timestamp inside the picked line:** none. Statements 1, 2
  and 4 have `P0 == P1` exactly; statement 3 differs by case counts, not by formatting. (Statement
  1’s *failing* P3 output does leak a fixture path, `fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.…`,
  but that line is not the picked line.)
* **Statement that times out in a profile:** none. `grep TIMEOUT|Traceback` over all 24 obs files
  (w1, six profiles, four statements) → 0 matches; every profile returned an `exit=` note.
* **Profile whose command crashed before reaching the tool:** none. Statement 1’s P3 failure is
  raised *inside* the tool (its own case body, reported as `setup/process error`) and the tool still
  prints its summary and exits 1.
* **Instability between runs:** none anywhere (w1≡w2, w3≡w4, plus v1≡v2), including the P3
  `UNOBSERVABLE` and the P5 exit-1 tuple.

## 7. Retained evidence

Exact `obs-*.stdout` for every profile of every run, plus the six run logs, kept at
`/var/tmp/tameshi-r47-T47ExecObsC/evidence/{w1,w2,w3,w4,v1}/{P0..P5}/obs-*.stdout` (644K).
The clone/mirror trees (~9G) and the `/tmp` symlinks were deleted after the report was written;
`/tmp/tameshi-r47-T47ExecObsC` now holds only the two logs.

Tooling: nothing installed or upgraded (no pacman; the host’s `python3`, `git`, `/usr/bin/bwrap`,
`/usr/bin/node`, `~/.local/bin/jj`, `~/.local/bin/jq` sufficed).

## 8. Risks / blockers

1. **ENOSPC is live host-wide** (`/tmp` 92-100% while other seats run). The counter clones 12 repos
   per run (~2.3G); a `/tmp` work dir will keep failing intermittently. This seat’s first attempt
   died exactly that way with the misleading message `C1_R47: clone/checkout failed`. The deciding
   run should not share a nearly-full fs.
2. **deps clause depends on `--work` placement** (§5) — the single highest-risk item for C1.
3. `fleet-root` dependence rests on a hardcoded absolute path (`.ufo/evidence/round-15/verify.py:105`,
   `:836`); the statement can never pass from a clone without the sibling fleet root present.
4. This seat observed only its four assigned statements; the remaining 18 were not probed here.
