# CtlOldSelftest — round 32, wave 1

## Verdict

**The old-selftest control is rejected as expected: `C1_R32_PASS=false`, exit 1.** The
control (a tool that only re-runs the runner's own `--selftest` and passes its verdict
through) kills **2 of 18** must-kill copies and accepts **8 of 8** must-accept copies.

The two kills are exactly the two copies of the **per-leg operand family** — `D01` and
`gD01` — because the runner's tally harness (lines 1994-2032 of
`tools/mutate-and-run.sh`) rebuilds the tally block from `$SELF` and cross-checks the
leg-status names, so a duplicated/dropped loop operand is visible to it. The runner's
selftest kills **none** of the 8 frozen MutateHead survivors (`T08 N05 H03 H04 H05 N01
N02 N03`), and **none** of the 8 generated must-kill copies outside the D01 family
(`gT08 gN05 gH03 gH04 gH05 gN01 gN02 gN03`).

This is the expected control result. It shows the runner's existing selftest is a
strict, real gate (it is not a rubber stamp: it does catch the operand defect) but it
is **not** a tally auditor: 16 of the 18 must-kill copies sail straight through it.
The real `tools/tally-audit.py` therefore has to add (a) per-leg presence, (b) an
independent oracle over exit statuses 0-255 plus overcount/undercount stress, and
(c) a panel of known-faulty tally blocks — none of which the runner's selftest does.

**One seed-sensitivity caveat on the kill count.** The generated `gT08` family's arm is
drawn from 2..255 (`.ufo/evidence/round-32/c1-measure.py:98`). Arms 2 and 3 land
on statuses the runner's harness *does* drive (status 2 and status 3 are among its own
vectors, `tools/mutate-and-run.sh:2010-2027`), so a `gT08` copy with arm 2 or 3 is
caught by the selftest; arms 4 and above are not driven by any vector and survive.
Verified directly in this seat (three hand-built `gT08` copies, arm 2 / 3 / 4, run
through this control):

```text
arm=2 -> TALLY_AUDIT: FAIL selftest exit=1 VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.…)   (tool exit 1)
arm=3 -> TALLY_AUDIT: FAIL selftest exit=1 VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.…)   (tool exit 1)
arm=4 -> TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass …               (tool exit 0)
```

Both observed counter runs drew arms outside 2..3 (`gT08(arm=96)` then
`gT08(arm=235)`), so `gT08` survived in both. The control's kill count is therefore
**2 or 3 of 18 depending on the seed**, not a fixed 2. The frozen predicate is
unaffected either way — 18/18 is required and the control cannot reach it — but a
third-party reading "the old selftest kills exactly 2" should read "the old selftest
kills the D01 family plus, seed-dependently, a `gT08` copy whose arm happens to be 2 or
3." The frozen `T08` copy (arm 4) survives, as expected.

Axis: **operability**. The runner's bytes were preserved exactly
(`tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`,
unchanged); the counter's `runner_sha_ok=1` confirms it at the measurement revision.

## Setup and lane

Sandbox clone only; the fleet repo and sibling lanes were never written to.

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

Observed: no stdout; exit 0. `git log --oneline -1` → `c318149 round-32: freeze — C1 counter + contract (tally audit, 18 must-kill / 8 must-accept), base receipts, repair receipts (r31 base monitor, command D exits), counter v2 repair`.
`df -h /fast` → `/dev/nvme1n1p2 804G 691G 113G 86% /fast` (113G free before the run).

Frozen inputs read first, unmodified:

```text
ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca  .ufo/evidence/round-32/c1-measure.py
7f3d5d99a3da67ab7d03193ab5421e46e519f0de657d8168ab9727cd8ee7e583  .ufo/evidence/round-32/contract.json
```

## The control under test

`tools/tally-audit.py` (new file, committed in this seat's sandbox clone only). Its whole
audit is: copy the runner under test byte-for-byte into a fresh temporary directory,
run `timeout 900 bash <copy> --selftest` there, and pass the verdict through — runner
selftest exit 0 → `TALLY_AUDIT: PASS` and tool exit 0; anything else → `TALLY_AUDIT: FAIL`
and tool exit 1; the runner cannot be audited at all → exit 2.

The copy step matters: the runner resolves `SELF=$(readlink -f "${BASH_SOURCE[0]}")`
(`tools/mutate-and-run.sh:178`) and its tally harness reads `$SELF` back, so the
mutated copy — not a pristine checkout — is what the harness inspects.

### Full source of the control tool

`tools/tally-audit.py` as committed at `ea67817` (142 lines; blob sha256
`53b57e8a6aeaf63d6c59d29bd354857bc1f8982dfcb8f95caa388670549b6232`):

```python
#!/usr/bin/env python3
"""tally-audit.py — CONTROL SEAT (CtlOldSelftest, tameshi round 32 wave 1).

Control, not a candidate implementation. This file deliberately implements only the
weakest possible audit of the runner's `--regression` tally: it asks the runner's OWN
`--selftest` harness for the verdict.

    python3 tools/tally-audit.py --runner COPY

Behaviour:
  * COPY is copied byte-for-byte into a fresh temporary directory (the copy is what
    runs, so `$SELF` inside the runner resolves to the mutated copy, not to a pristine
    checkout).
  * `timeout 900 bash <copy> --selftest` runs in that fresh directory.
  * exit 0 of the runner's selftest  -> prints `TALLY_AUDIT: PASS` and exits 0.
  * any other exit status / timeout   -> prints `TALLY_AUDIT: FAIL` and exits 1.
  * the runner cannot be audited at all (missing/unreadable file, no interpreter)
    -> exits 2 without a verdict line.

Why this is a control and not the real tool: the real `tools/tally-audit.py` must
audit the tally block itself (per-leg presence, an independent oracle over exit
statuses 0-255, and a panel of known-faulty tally blocks). This control only
re-runs the runner's existing selftest, so whatever the runner's selftest already
catches is caught here and nothing more. The round-32 counter is expected to print
`C1_R32_PASS=false` for it.

Exit codes: 0 = PASS verdict, 1 = FAIL verdict, 2 = cannot audit.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

SELFTEST_TIMEOUT = 900  # seconds, the contract's ceiling for one selftest run
GUARD_TIMEOUT = 540     # seconds; below the counter's 600 s per-copy ceiling, so a
                        # hung runner is reaped here instead of by the counter


def audit(runner_path):
    """Return (verdict, detail). verdict is 'PASS', 'FAIL' or None (cannot audit)."""
    if not os.path.isfile(runner_path):
        return None, 'runner path is not a regular file: %s' % runner_path
    try:
        with open(runner_path, 'rb') as f:
            payload = f.read()
    except OSError as e:
        return None, 'cannot read runner: %s' % e

    work = tempfile.mkdtemp(prefix='tally-audit-')
    try:
        copy = os.path.join(work, 'mutate-and-run.sh')
        with open(copy, 'wb') as f:
            f.write(payload)
        os.chmod(copy, 0o755)

        env = {
            'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
            'HOME': work,
            'TMPDIR': work,
            'LANG': 'C.UTF-8',
            'LC_ALL': 'C.UTF-8',
        }
        cmd = ['timeout', str(SELFTEST_TIMEOUT), 'bash', copy, '--selftest']
        try:
            p = subprocess.Popen(cmd, cwd=work, env=env, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 start_new_session=True)
        except (FileNotFoundError, OSError) as e:
            return None, 'cannot launch the runner selftest: %s' % e
        try:
            out_b, err_b = p.communicate(timeout=GUARD_TIMEOUT)
        except subprocess.TimeoutExpired:
            _kill_group(p)
            try:
                out_b, err_b = p.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                out_b, err_b = b'', b''
            return 'FAIL', 'runner selftest exceeded the %d s guard timeout' % GUARD_TIMEOUT
        out = out_b.decode('utf-8', 'replace')
        err = err_b.decode('utf-8', 'replace')

        detail = _summarise(out, err, p.returncode)
        _reap(out)
        if p.returncode == 0:
            return 'PASS', detail
        return 'FAIL', detail
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _summarise(out, err, rc):
    lines = [x for x in out.splitlines() if x.strip()]
    verdict = next((x for x in reversed(lines) if x.startswith('VERDICT:')), '')
    tally = next((x for x in reversed(lines) if x.startswith('MUTATE_SELFTEST:')), '')
    failed = [x for x in lines if x.startswith('FAIL')][:5]
    tail = (err.splitlines() or [''])[-1]
    return 'selftest exit=%d %s %s failed=%r stderr_tail=%r' % (
        rc, verdict, tally, failed, tail[:200])


def _kill_group(p):
    """Kill the runner's whole process group (it was started with start_new_session)."""
    import signal
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        try:
            p.kill()
        except OSError:
            pass


def _reap(text):
    """Remove the scratch dir the runner keeps on a failing selftest."""
    if isinstance(text, bytes):
        text = text.decode('utf-8', 'replace')
    for line in text.splitlines():
        if 'scratch kept:' not in line:
            continue
        path = line.split('scratch kept:', 1)[1].strip()
        path = path.rstrip(')').rstrip()
        if path.startswith('/tmp/tameshi-r4-2-selftest.') and os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--runner', required=True, help='path to a runner copy to audit')
    a = ap.parse_args()
    verdict, detail = audit(a.runner)
    if verdict is None:
        print('TALLY_AUDIT: CANNOT AUDIT %s' % detail)
        return 2
    print('TALLY_AUDIT: %s %s' % (verdict, detail))
    return 0 if verdict == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
```

`import sys` is unused in the committed file; it was left in rather than churn the
control further — the control's behaviour is unaffected. (Recorded here as an
observation, not a defect that touches the verdict.)

### The exit-2 path, observed

```text
$ python3 lane/tools/tally-audit.py --runner /nonexistent/x.sh
TALLY_AUDIT: CANNOT AUDIT runner path is not a regular file: /nonexistent/x.sh
EXIT=2
```

Sandbox commit (one commit, on top of the frozen revision; `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE` unset, inside this seat's clone only):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/lane add tools/tally-audit.py && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/lane -c user.name=ctl -c user.email=ctl@sandbox commit -qm CtlOldSelftest
```

Observed: `ea67817 CtlOldSelftest`, parent `c318149`. `git show --stat HEAD` →
`tools/tally-audit.py | 142 +++...`, 1 file changed, 142 insertions. `git status --porcelain`
→ empty. Committed blobs:

```text
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  HEAD:tools/mutate-and-run.sh
53b57e8a6aeaf63d6c59d29bd354857bc1f8982dfcb8f95caa388670549b6232  HEAD:tools/tally-audit.py
```

The runner blob at the measurement revision is byte-identical to the pinned sha, so the
contract's byte-preservation half of the predicate holds for this control too.

## Exact measurement command and full counter stdout

```sh
timeout 2400 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py --lane /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/lane --rev HEAD --work /fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/w-CtlOldSelftest --jobs 4
```

Fresh empty `--work`; no `--seed` (the counter printed its own fresh seed
`76d49df214070e50`). Full stdout, verbatim (27 lines):

```text
COPY set=kill id=T08 outcome=ACCEPT exit=0 sha256=12ad1d9076a55050 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=N05 outcome=ACCEPT exit=0 sha256=e1ef181c1e621962 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=H03 outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=H04 outcome=ACCEPT exit=0 sha256=0dc1e6b07452f610 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=H05 outcome=ACCEPT exit=0 sha256=adf6763d6524f342 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=N01 outcome=ACCEPT exit=0 sha256=c0a32ec4e69d3cb0 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 105/105 pass failed=[] stderr_tail=''"
COPY set=kill id=N02 outcome=ACCEPT exit=0 sha256=31128639afc3e57a last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=N03 outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=D01 outcome=KILL exit=1 sha256=71a66c5a611d408f last="TALLY_AUDIT: FAIL selftest exit=1 VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.VPg9hw) MUTATE_SELFTEST: 100/106 pass failed=['FAIL tally harness: one"
COPY set=kill id=gT08(arm=235) outcome=ACCEPT exit=0 sha256=9850128ce400c66b last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gN05(<= nlegs - 1) outcome=ACCEPT exit=0 sha256=7184b157539cad8c last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gH03(form=0) outcome=ACCEPT exit=0 sha256=2ac4ce5344e6100a last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gH04(:) outcome=ACCEPT exit=0 sha256=fba8e1cf3e1bfd8b last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gH05(drop=5,dup=2) outcome=ACCEPT exit=0 sha256=d86385240455dbc0 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gN01(vector=3) outcome=ACCEPT exit=0 sha256=c66c1ca66cf8ae0f last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 105/105 pass failed=[] stderr_tail=''"
COPY set=kill id=gN02(true) outcome=ACCEPT exit=0 sha256=29d0e2b6649efed2 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gN03(or) outcome=ACCEPT exit=0 sha256=741907e82ca7e907 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=kill id=gD01(drop=st_claims,dup=st_js) outcome=KILL exit=1 sha256=d540e3a5f7e606de last="TALLY_AUDIT: FAIL selftest exit=1 VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.55vy77) MUTATE_SELFTEST: 100/106 pass failed=['FAIL tally harness: one"
COPY set=accept id=B0-pristine outcome=ACCEPT exit=0 sha256=a7d3f2dd7d47511a last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=B1-T07 outcome=ACCEPT exit=0 sha256=91066af826f69ecb last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=B2-reversed outcome=ACCEPT exit=0 sha256=7d3d5a5f34fe3595 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=B3-decoys outcome=ACCEPT exit=0 sha256=7c76617e87c11c49 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=B4-cosmetic outcome=ACCEPT exit=0 sha256=137a7ba8a58c5277 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=B5-renamed outcome=ACCEPT exit=0 sha256=f66fe32a4ea7ce76 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=gB6-permuted outcome=ACCEPT exit=0 sha256=6b84c6895aa3bb39 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
COPY set=accept id=gB7-nonce outcome=ACCEPT exit=0 sha256=dd29f82dca16fdc0 last="TALLY_AUDIT: PASS selftest exit=0 VERDICT: PASS MUTATE_SELFTEST: 106/106 pass failed=[] stderr_tail=''"
C1_R32: kill=2/18 accept=8/8 other=16 runner_sha_ok=1 tool_present=1 seed=76d49df214070e50 rev=ea67817dd79ffd48bb92efd1bd5a9f7f5e9cac60 C1_R32_PASS=false
```

**Observed exit code: 1.** The counter's stderr was empty (0 bytes). Wall clock 48 s for
all 26 copies at `--jobs 4`. Receipts kept at
`/fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/ctl-counter.stdout`,
`ctl-counter.stderr` (empty), `ctl-counter.exit` (`1`).

### A second observed run at the same measurement revision

Per the contract's `kill_rule`, a second observed run at the measurement revision is
reported beside the first. The control was amended once before the run above — the
scratch-reaping helper initially failed to strip the trailing `)` from the runner's
`VERDICT: FAIL (scratch kept: …)` line, so a failing selftest left its `/tmp` scratch
behind; that was fixed in the tool (not in the runner) and the commit was amended. The
first run, at commit `040c568` with the un-amended tool, printed the same verdict:

```text
C1_R32: kill=2/18 accept=8/8 other=16 runner_sha_ok=1 tool_present=1 seed=ce07a347b5496b83 rev=040c56845d5e0a4d62cd75d60fa0fdd36f9e82d2 C1_R32_PASS=false
```

Exit 1. Same kill set (`D01`, `gD01`), same accept set (8/8), different generated
families (`gT08(arm=96)`, `gN05(< nlegs + 0)`, `gH04(true)`, `gH05(drop=2,dup=8)`,
`gN01(vector=2)`, `gN02(true)`, `gN03(split)`, `gD01(drop=st_sourcescheck,dup=st_kagi)`)
— the seeds differ but the outcome does not.

Retained receipt: the amended run's stdout is kept at
`/fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/ctl-counter.stdout` (and
`ctl-counter.exit` = `1`, `ctl-counter.stderr` = 0 bytes); the file `ctl.stdout` in the
same directory is a byte-identical copy of it. The first run's **full** stdout was
written to the same `ctl.stdout` path and was overwritten by the second run before it
was copied aside, so only its final `C1_R32:` line is quoted above; the per-`COPY`
lines of that run are not retained on disk. The amend between the two runs touched
only the tool's `/tmp` scratch-reaping helper (a cleanup path, not a verdict path), so
the two runs are directly comparable.

## Why the runner's own selftest kills D01 and gD01 but nothing else

`tools/mutate-and-run.sh:1994-1995` (harness span 1994-2040) — the selftest extracts
the tally block out of `$SELF` and extracts the nine leg-status names out of
`run_regression`'s `st_*=$?` assignments:

```bash
tblock=$(awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' "$SELF")
mapfile -t tnames < <(awk '/^run_regression\(\) \{$/{f=1} /^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=0} f&&/^  st_[a-z]+=\$\?$/{sub(/^  /,""); sub(/=\$\?$/,""); print}' "$SELF")
```

Because the leg-status names come from the `st_*=$?` assignments and **not** from the
tally loop, a leg whose status is left out of the loop (or duplicated in it) is
detectable — and is detected, because the harness then drives nine positional status
vectors through the block and expects an exact first line each time. For `D01`
(`"$st_js"` duplicated, `"$st_citecheck"` dropped) the selftest reports
`MUTATE_SELFTEST: 100/106 pass`, with the failing cases named in the tool's own
summary:

```text
FAIL tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (7/9)
FAIL tally harness: one leg status 2 at each of 9 positions -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1) (7/9)
FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
```

The other eight families are invisible to the harness by construction (with the one
`gT08` arm-2/arm-3 exception noted above):

- `T08` / `gT08` — an extra `case` arm is added after the `0)`/`1)` arms: arm 4 in the
  frozen `T08` copy, a random arm in 2..255 in the generated one. The harness drives
  statuses 0, 1, 2 and 3 only (`tools/mutate-and-run.sh:2008`, `:2010-2011`,
  `:2024-2027`), so arm 4 is never reached and `T08` survives. A generated arm of 2 or
  3 *is* driven and is caught (see the seed-sensitivity caveat above).
- `N05` / `gN05` — the completeness guard's comparison is weakened (`!= nlegs` becomes
  `< nlegs`, `< nlegs + 0` or `<= nlegs - 1`). The harness's own stress case deletes
  the loop's last operand and expects `SETUP (case-tally mismatch: cases=9 counted=8)`;
  a guard that only trips on `<`/`>` still trips there, so the weakened guard is
  equivalent on every vector the harness runs.
- `H03` / `gH03` — the exact-line comparison is weakened or the status is swallowed.
  The harness's own expected lines are produced by the same code path it is checking, so
  the weakened comparison still agrees with itself.
- `H04` / `gH04` — a trailing `rc=$?` / `true` / `:` swallows the comparison status.
  The harness reads `$?` after the comparison in some places and tolerates the
  swallowed status.
- `H05` / `gH05` — one singleton position P in 0..8 is never exercised (the position
  list is `0 1 2 3 4 5 6 7 7`). The harness's per-position loop covers the same nine
  positions, so a position the block never sees is a position the harness also never
  probes.
- `N01` / `gN01` — one of the four multi-status vectors is deleted from the harness's
  own vector list. The selftest then has one vector fewer (`MUTATE_SELFTEST: 105/105`
  instead of `106/106`) and still passes: the harness grades itself.
- `N02` / `gN02` — the guard-stress case is skipped (`&&` becomes `||`, or the call is
  replaced by `true`). The skipped case is one the harness itself supplies.
- `N03` / `gN03` — line-or-exit instead of line-and-exit. Both sides still agree.

The pattern is the point of the control: **the runner's selftest grades the tally block
with the tally block's own logic.** Every mutant that weakens the logic weakens the
grader with it. Only the per-leg presence check (`D01`) is anchored outside the
block, and only that family dies.

## The must-accept side

All 8 must-accept copies were correctly accepted (exit 0, `TALLY_AUDIT: PASS`): the
pristine runner, the equivalent-guard rewrite `B1-T07`, the reversed-operand rewrite
`B2-reversed`, the decoy-comment copy `B3-decoys`, the cosmetic tally edit `B4-cosmetic`,
the harness-variable rename `B5-renamed`, the generated permutation `gB6-permuted` and
the nonce-comment copy `gB7-nonce`. This is the floor the real tool must also hold: a
tool that simply answered FAIL everywhere would score kill=18/18 but accept=0/8 and
still print `C1_R32_PASS=false`.

## Smallest safe correction

None to the control, the frozen counter or the frozen contract. The control is a
deliberately weak audit; its `C1_R32_PASS=false` is the correct outcome and is the
evidence that the runner's existing selftest is not a substitute for the required
`tools/tally-audit.py`.

The correction for the round is in the L1's real tool, and the control names exactly
what it must add. A tool that only re-runs `bash <runner> --selftest` cannot reach
kill=18/18. To close the gap the real tool needs, on top of any runtime check:

1. **Per-leg presence** — parse `run_regression`'s `st_*=$?` assignments and the tally
   loop's operand list out of the runner under test and require every leg status to be
   named exactly once (this is what kills `D01`/`gD01`, and the harness can also reach
   it, but it must not be the only gate).
2. **An independent oracle** — rebuild the expected first line and exit status from the
   nine statuses for every exit status 0..255 plus overcount/undercount stress, rather
   than grading the block with the block's own comparison. This is what is needed for
   `T08`, `H03`, `H04`, `H05`, `N03` and their generated variants.
3. **A panel of known-faulty tally blocks** — feed the runner's own harness (or an
   equivalent) a fixed set of deliberately broken tally blocks it must reject, so that
   weakening the harness's own vectors (`N01`, `N02`) is caught from outside.
4. **An independent guard check** — the completeness guard `npass + nfail + nsetup !=
   nlegs` must be verified against a summing oracle, not against a mutant of itself
   (`N05`).

## Housekeeping

- No production file was edited. `tools/mutate-and-run.sh` was never written; the
  counter's `runner_sha_ok=1` and the blob hash above confirm it.
- The frozen counter and contract were read only, never edited, never re-seeded, never
  amended.
- Only this seat's sandbox clone was written with git (`add` + `commit` inside
  `/fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest/lane`). No `jj` command was run
  anywhere. No git write command was run against the fleet repo or any sibling lane.
- The tool reaps the runner's own `/tmp/tameshi-r4-2-selftest.*` scratch after a failing
  selftest, and removes its own working directory in a `finally` block. Verified: no
  `/tmp/tameshi-r4-2-selftest.*` directory newer than the run remains that this seat
  created (the pre-existing ones under `/tmp` belong to other seats and were left
  alone).
- Every process this seat started finished; none remains. No process owned by another
  seat was signalled.
- Scratch footprint: `/fast/scratch/hyaku/tameshi-r32-seats/CtlOldSelftest` ≈ 165 MB
  (clone + the counter's copy set), well inside the 113 GB free on `/fast`.
- **No tools were installed or updated** for this seat: the control needed only
  `python3`, `bash`, `timeout` and `git`, all already present (`python3` 3.x, `bash`
  5.x, GNU coreutils `timeout`, `git`; `node` v24.21.0 was already on `PATH` because
  the runner's selftest drives the JS legs).
- This report is the only file written outside this seat's scratch directory.
