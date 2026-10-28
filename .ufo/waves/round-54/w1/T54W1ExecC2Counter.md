# T54W1ExecC2Counter — C2 verify (frozen counter), round 54

Seat: `T54W1ExecC2Counter` (executor, operability). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Every measurement below is pinned to `--rev 59c38109bf119d0e9d4f878644a82babc937bc1e` (C0) unless a line says otherwise.
Receipts (raw command output) live in `.ufo/waves/round-54/w1/T54W1ExecC2Counter-receipts/`.

## 1. Verdict

The **frozen** counter bytes are sha256 `b4684a3f555e8cbfda6fc9c7208827a3816a60cf53186269fdec41d5025e9e49`
(`.ufo/evidence/round-54/freeze.json` pins exactly this; the blob at HEAD `3146479` hashes to it; my clones checked out
at C0 carry the same bytes). Two independent full runs of those bytes at C0 both print:

```
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=6 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
EXIT=1
```

Run A (work dir 1, 28 Oct 11:26–11:30 local) and run B (work dir 2, 11:33–11:41 local) are byte-identical on that line.

**Named short arm: `usable`, tool `tools/registry-check.py`.** Its EXPLAIN line, verbatim, in both runs:

```
EXPLAIN usable registry-check rc=1 tmp_mkdirs=0
```

So the seat brief's expectation — `C2_R54_PASS=true` with `usable_ok=7` — does **not** hold for the frozen instrument on
this host. It holds only for a **modified, uncommitted working-tree copy** of the counter:

```
$ sha256sum .ufo/evidence/round-54/c2/measure.py
49280fe55bd9361c284ddb1b9e757fd3ec3267f60eed4ca587e1bfe446b718c8   # != pin b4684a3f…
$ git status --porcelain -- .ufo/evidence/round-54/c2/measure.py
 M .ufo/evidence/round-54/c2/measure.py

C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
EXIT=0
```

That copy self-describes as *"Amendment 2: the rc is the plain run and the traced run supplies only the mkdir census — under
`strace -f` one tool's own timeout tests fail from tracer overhead, so a traced rc measured the tracer."* The diagnosis in
that sentence is correct (see §4); the copy is nevertheless not the frozen instrument, and the file is modified in the lane's
working tree without a commit. A byte copy of it is preserved as `…-receipts/counter-worktree-modified.amendment2.py`, and the
exact diff against the pin is in §6/F3.

`docs=7 note=1 sources=3` in both cases. The brief's `sources=1` is a brief-side guess: the counter counts *each* cited-and-mined
S id (`sourced` is incremented per id), and C0 cites S277, S278 and S279, so `sources=3` is the correct value, not a shortfall.

## 2. Independent by-hand reproduction of the unusable arm (required paste)

Clone at C0: `git clone --shared` into scratch, `git -C <clone> rev-parse --show-toplevel` printed the clone (not the lane),
`rev-parse HEAD` printed `59c38109bf119d0e9d4f878644a82babc937bc1e`.

```
$ cd <clone-at-C0>
$ env TMPDIR=/nonexistent-x54 PYTHONDONTWRITEBYTECODE=1 python3 tools/registry-check.py --selftest
EXIT=2
--- stdout ---            (empty)
--- stderr ---
registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent-x54' (could-not-evaluate)

stdout lines=0  stderr lines=1
occurrences of 'could-not-evaluate': stdout 0, stderr 1
occurrences of 'Traceback (most recent call last)': stdout 0, stderr 0
```
(`…-receipts/hand-unusable-registry-check.stdout` is empty, `…-receipts/hand-unusable-registry-check.stderr` is that single line.)

The frozen counter's own line for the same tool and arm, pasted for comparison:

```
EXPLAIN unusable registry-check rc=2 line='registry-check: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory'
```

Both agree: exit 2, one naming line, the TMPDIR value is named, no traceback.

## 3. All seven tools × all three arms, by hand

`env TMPDIR=… python3 <tool> <selftest arg>` in the C0 clone, rc recorded:

| tool | unusable `/nonexistent-x54` | empty `TMPDIR=""` | usable fresh dir |
|---|---|---|---|
| registry-check | 2 (1 naming line, 0 tracebacks) | 0 | 0 |
| env-diff | 2 (1/0) | 0 | 0 |
| bash-witness-study | 2 (1/0) | 0 | 0 |
| evidence-disposition | 2 (1/0) | 0 | 0 |
| pin-disposition | 2 (1/0) | 0 | 0 |
| context-capture | 2 (1/0) | 0 | 0 |
| repeat-control | 2 (1/0) | 0 | 0 |

This matches the frozen counter's `unusable_exit2=7 naming=7 empty_ok=7`. The one arm that does not reproduce is the strace arm,
and only for registry-check — §4.

## 4. Why the usable arm is short: the traced rc measured the tracer

The frozen arm is `usable_ok += (proc.returncode == 0 and hits == 0)` where `proc` is `strace -f -e trace=mkdir,mkdirat … python3 <tool> <selftest>`.
For `tools/registry-check.py` the self-test has its own wall-clock assertions; under `strace -f` they trip:

Under strace (four independent runs — two driven by the counter, two by hand in two different C0 clones, one cold-cache):

```
SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=4.784s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=4.596s survivor=False marker=False)
SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)

(second clone, cold cache) timeout-kills-setsid-pipe FAIL elapsed=4.527s ; timeout-kills-setpgid-pipe FAIL elapsed=4.711s
(third, cold cache, later) elapsed=11.563s ; 12.792s
```

The bound they cross is the self-test's own, `tools/registry-check.py:1223` at C0: `and elapsed < 3.5`.
Same tool, same clone, **no strace** (two runs, exact C0):

```
SELFTEST_CASE timeout-kills-setsid-pipe PASS (exit=1 elapsed=1.701s survivor=False marker=False)
SELFTEST_CASE timeout-kills-setpgid-pipe PASS (exit=1 elapsed=1.701s survivor=False marker=False)
SELFTEST: PASS (51 cases)          rc=0
run 2: 2.033s / 2.037s, SELFTEST: PASS (51 cases), rc=0
```

Scratch behaviour under trace was correct in every failing case: `survivor=False marker=False`, i.e. the process-group kill the
case exists to prove did happen; and the `/tmp` census is zero:

```
mkdir/mkdirat lines in the counter's registry-check strace log: 238
of those, paths under /tmp:                                   0
```

So the failing rc is ptrace overhead (strace 7.2, Python 3.14.8), not the scratch-root contract.
The arm's outcome is a function of host contention, not of the tree: the contract's own C2 `before` line records
`usable_ok=7` at base `d33053f7` while `tools/registry-check.py` is byte-identical at base and C0
(sha256 `ade15cc008c07d54c77812d27b49079180168d843439b0b1c458292fa0f2a33f` both) and the counter bytes did not change either.
Same instrument, same tool, `7` before and `6` now — the only variable is the machine's load.

## 5. The other arms, and what I opened to check them

- **docs=7** — `tools/registry.json` at C0, the seven `*selftest` rows; every `scratch_root` cell is the same text and contains
  `TMPDIR`, `empty` and `could-not-evaluate`:
  `"TMPDIR set but unusable => exit 2, could-not-evaluate (the value is named, no traceback); TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp (round 54, corpus/knowledge/scratch-root-contract.md)"`.
- **note=1** — `corpus/knowledge/scratch-root-contract.md` exists at C0; its three-arm table, the S278 `:163-165` quote and the
  "the counter's blind spot is stated in the contract" paragraph are present.
- **sources=3** — `corpus/SOURCES.md` rows S277/S278/S279 are `mined` with `corpus/knowledge/scratch-root-contract.md` in the
  used-by cell; `corpus/lessons/round-54.md` `## Gate` names each of the three ids with `2026-10-28`, an `http` URL and a located quote.

## 6. Instrument / infrastructure observations (report-only; I changed nothing)

**F1 — unresolvable `--rev` exits 1 with a traceback, not the documented 2.** `measure.py` calls `git(..., check=True)` for
resolving `--rev`, outside the `Setup` handler, so a bad or momentarily-unavailable rev raises `subprocess.CalledProcessError`
instead of the documented `C2_R54: error=… total=1 C2_R54_PASS=false` + exit 2:

```
$ python3 .ufo/evidence/round-54/c2/measure.py --lane $PWD --rev deadbeef00 --work <empty> --explain
Traceback (most recent call last):
  ...
  File ".../c2/measure.py", line 96, in main
    rev = git(['rev-parse', '--verify', '%s^{commit}' % a.rev], lane).stdout.decode().strip()
subprocess.CalledProcessError: Command '[... 'rev-parse', '--verify', 'deadbeef00^{commit}']' returned non-zero exit status 128.
EXIT=1
```
(`…-receipts/counter-unresolvable-rev.txt`)

**F2 — the lane's object store intermittently cannot resolve C0 itself.** Observed at 14:47Z, 14:51Z and 14:53Z
(`git cat-file -t 59c38109bf119d0e9d4f878644a82babc937c1e` → `fatal: Not a valid object name`), resolvable again at 14:49Z and
14:54Z; `git rev-list --all | grep -c '^59c38109'` returned `1` throughout, so the commit is reachable in the graph.
During the same window the lane's HEAD advanced `59c3810 → 99c3bc8 → 7883e0e → 3146479` ("export from jj"). Any counter
invocation that lands in such a window dies with F1's traceback instead of a verdict. I lost one full run to this.
(`…-receipts/counter-run3.txt` is that run.)

**F3 — freeze bookkeeping already trips the round's own frozen gate.** `deciding-run.sh` diffs the freeze commit against REV
across the FROZEN list and forces `rc=1` on any difference. At HEAD that diff is non-empty:

```
 .ufo/evidence/round-54/c1/measure.py |  8 ++++++--
 .ufo/evidence/round-54/contract.json | 22 ++++++++++++++++++----
 .ufo/evidence/round-54/freeze.json   |  9 +++++++--
```
(amendment 1's own bookkeeping). `c2/measure.py` is still identical to the pin at HEAD, so the gate difference is not the C2
edit — but a second, committed C2 amendment would add to it unless the freeze commit itself is rewritten.

**F4 — the C2 "before" receipt is empty and untracked.** `contract.json` cites
`unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 … (measured at d33053f7, .ufo/evidence/round-54/before/c2.stdout)`, but:

```
$ ls -l .ufo/evidence/round-54/before/c2.stdout
-rw-r--r-- 1 vgpnk vgpnk 0 Oct 28 11:47 …/before/c2.stdout        # 0 bytes, sha256 e3b0c442… (empty)
$ git ls-files .ufo/evidence/round-54/before/
(no output)
```
The baseline that the C2 target is measured against has no receipt at any revision, and `usable_ok=7` in that line is exactly
the figure that the frozen counter no longer reproduces.

## 7. Bounds, tooling, cleanup

- Files written: this report and `.ufo/waves/round-54/w1/T54W1ExecC2Counter-receipts/` only. No lane file edited; the counter,
  registry, contract, freeze, ledger and wave spec untouched. No mutating git/jj command: clones were `git clone --shared`
  into scratch, every `git -C` named the fixture, `rev-parse --show-toplevel` asserted the clone before use.
- Fixtures and work dirs lived under `/fast/scratch/hyaku/tameshi-r54/T54W1ExecC2Counter/`; the tree was removed at the end.
- Tools installed or upgraded: none (nothing was needed; pacman is paused host-wide regardless).
- The census is round-start/end work for the L1, not this seat.
