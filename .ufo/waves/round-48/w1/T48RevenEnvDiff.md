# T48RevenEnvDiff — root cause: `env-diff` selftest `2/9` vs `9/9` under P1

Seat: T48RevenEnvDiff (round 48, w1, calibration axis / C1 feed). Read-only on the lane; three
scratch selftest runs under `/fast/scratch/hyaku/tameshi-r48/T48RevenEnvDiff` (deleted at exit).
Lane base `473336d9d789f6081195e7376d17836a24666bc3`, lane worktree at `f1cfaad360130933983cac19f7036a8151f9054b`.
Tool pin: `tools/env-diff.py` = `e8b47ab7cf23` at both `473336d` and `f1cfaad` (unchanged across round 47).

## 1. Verdict (short)

1. The `2/9` is **not** load-induced, **not** a bwrap/user-namespace shortage, **not** a timeout and
   **not** a missing bwrap binary in P1. It is a deterministic **harness × instrument** collision:
   the round-47 counter puts the profile `PATH` shim inside its `--work` directory
   (`.ufo/evidence/round-47/calibration/measure.py:182,188`) and `env-diff` replaces `/tmp` inside
   its sandbox (`tools/env-diff.py:69` `"--tmpfs", "/tmp"`). When `--work` is under `/tmp` the shim
   is masked, so bwrap cannot `execvp` the interpreter and **every** `execute()` row dies at once.
   Under `/var/tmp` (or any path outside `/tmp`) the same tool, same counter, same rev prints `9/9`.
2. The `8/9` without node is a real, thin, **required** dependence: the tool's public-CLI path runs
   `node --version` for the receipt's host block at `tools/env-diff.py:234-236`, *before* it writes
   the receipt at `:239`; a missing node raises `OSError`, is caught at `:240-242` as
   `ENVDIFF_SETUP` with exit 2, no receipt is written, and the ninth case
   (`env-diff.py:190-192`, which demands exit 1 + one record) fails.
3. The `2/9` under P2 (bwrap absent) is produced by a *different* branch (`tools/env-diff.py:58-60`,
   `BWRAP_UNAVAILABLE`) yet prints **the same number**: `2/9` cannot discriminate "no binary" from
   "binary masked". Because of that coincidence an archived `2/9` is not self-describing, and the
   round-47 record had no field that could tell the two apart.
4. `SCORECARD.md:2314` ("not stable across runs under host load") is a **misattribution**. Round 46
   already froze the same false set (`LOG.md:2339`, env-diff `{env, node}`), so the artifact is older
   than round 47.

## 2. Value sets, by placement of the counter's `--work`

| `--work` placement | P0 | P1 | P2 (no bwrap) | P3 (no jj) | P4 (no node) | P5 (decoy fleet root) | observed deps |
|---|---|---|---|---|---|---|---|
| **outside `/tmp`** (`/var/tmp`, `/fast/…`) | `9/9`,0 | `9/9`,0 | `2/9`,1 | `9/9`,0 | `8/9`,1 | `9/9`,0 | `bwrap,node` |
| **inside `/tmp`** | `9/9`,0 | `2/9`,1 | `2/9`,1 | `2/9`,1 | `1/9`,1 | `2/9`,1 | `env,node` |

Both rows are observed data, not construction:

* outside `/tmp` — `.ufo/evidence/round-47/after/c1.stdout:18` (deciding run,
  `.ufo/evidence/round-47/deciding-run.sh:19` default `--work /var/tmp/tameshi-r47-deciding`) and
  `.ufo/waves/round-47/w1/T47ExecObsC.md:85` (`--work /var/tmp/…`, `--only` this statement).
* inside `/tmp` — `.ufo/evidence/round-47/before/c1-at-freeze.stdout:18` and
  `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out:18` (identical five-tuple), and
  `.ufo/waves/round-47/w1/T47ExecObsC.md:54` (`--work /tmp/…`, same `--only`, same rev).

ObsC ran **both** placements at one rev with one counter: `/tmp` → `P1=2/9 P4=1/9`;
`/var/tmp` → `P1=9/9 P4=8/9`. Time, load and rev are held fixed; only the path string moves.

## 3. Mechanism, with path:line

1. **Shim inside the work dir.** `measure.py:182` `shim = os.path.join(work, prof, 'shim')`;
   `measure.py:188` exports it as the *whole* `PATH`. `build_shim` (`:156`) symlinks `/usr/bin`
   (`:159,166`) plus `node, jj, jq` from `shutil.which` (`:170`). So P1's only way to find `bash`
   is a path under `--work`.
2. **The sandbox re-mounts `/tmp`.** `tools/env-diff.py:68-71`:
   `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind <tmpdir> /tmp/w --unshare-net
   --die-with-parent --chdir /tmp/w <interp> /tmp/w/target.sh --selftest`.
   bwrap performs the `execvp` **after** it builds the mount namespace, so `<interp>` is resolved
   against the sandbox tree — where `/tmp` is a fresh tmpfs and the only survivor beneath it is the
   run's own temp dir bound at `/tmp/w`.
3. **Consequence.** With `--work` under `/tmp`: `bwrap: execvp bash: No such file or directory`,
   exit 1, in milliseconds — for all 42 probe invocations (six cases × seven profiles), and the
   `timeout` probe dies the same way.
4. **Scoring.** Each probe row now carries an int exit ≠ 0, so `classify()` returns `unavailable`
   (`tools/env-diff.py:101`), and each of the six probe cases fails (`:148-160`). The `timeout` case
   fails too (`:163-164`): it wants `TIMEOUT` and instead gets a fast exec failure. Two cases survive
   without a working sandbox — `missing-bwrap` (`:161-162`, passes a bogus path and expects
   `EXEC_UNAVAILABLE` from `:77`) and `pin-mismatch-public-cli` (`:185-192`, drives the public CLI over
   a local fixture repo) → **2/9, exit 1** (`:193-195`).
5. **One case fewer without node.** Under P4 the public-CLI child reaches
   `for command in ("node", "bash"): subprocess.run([command, "--version"], …)` at
   `tools/env-diff.py:234-236`, *before* `a.out.write_text(...)` at `:239`. Missing node raises
   `FileNotFoundError`, caught by `:240-242` → `ENVDIFF_SETUP`, exit 2, **no receipt file**; `:190`
   needs `returncode == 1` and one record → the ninth case also fails. Hence `1/9` when P1 is
   masked and `8/9` when P1 is healthy — exactly the two archived values.
6. **P2's identical `2/9` by another route.** `tools/env-diff.py:58-60`: `shutil.which("bwrap")` is
   `None` because the shim has no bwrap → `BWRAP_UNAVAILABLE` → the same `unavailable` path → the
   same 2/9. Two distinct causes, one printed number: the archived `2/9` is **not** self-describing.

Under `--work` outside `/tmp` the shim survives `--ro-bind / /` (it is not under `/tmp`), the six
probes run, `timeout` really times out, and P2/P4 diverge from P1 → `9/9` and `8/9`.

## 4. Reproductions (my three scratch runs)

Shim built with the round-47 `build_shim` semantics (all of `/usr/bin` + `node`, `jj`, `jq` from
`shutil.which`), each run under `env -i` with P1's key set (`PATH=shim HOME=… TMPDIR=… LANG=C
LC_ALL=C TZ=UTC`), `--selftest` on the tool as cloned (`/usr/bin/python3 lane/tools/env-diff.py`,
`sha256 e8b47ab7cf23…`, unmodified). Shims lived under `/fast/scratch/...` (outside `/tmp`).

```
===== P1  (shim: /usr/bin + node + jj + jq)
ENVDIFF_CASE invariant PASS      ENVDIFF_CASE tz PASS        ENVDIFF_CASE locale PASS
ENVDIFF_CASE home PASS           ENVDIFF_CASE columns PASS   ENVDIFF_CASE repeat PASS
ENVDIFF_CASE missing-bwrap PASS  ENVDIFF_CASE timeout PASS
ENVDIFF_CASE pin-mismatch-public-cli PASS
ENVDIFF_SELFTEST: 9/9 pass   exit=0
===== P4  (shim minus node)
ENVDIFF_CASE invariant PASS      ENVDIFF_CASE tz PASS        ENVDIFF_CASE locale PASS
ENVDIFF_CASE home PASS           ENVDIFF_CASE columns PASS   ENVDIFF_CASE repeat PASS
ENVDIFF_CASE missing-bwrap PASS  ENVDIFF_CASE timeout PASS
ENVDIFF_CASE pin-mismatch-public-cli FAIL
ENVDIFF_SELFTEST: 8/9 pass   exit=1
===== P2  (shim minus bwrap)
ENVDIFF_CASE invariant FAIL      ENVDIFF_CASE tz FAIL        ENVDIFF_CASE locale FAIL
ENVDIFF_CASE home FAIL           ENVDIFF_CASE columns FAIL   ENVDIFF_CASE repeat FAIL
ENVDIFF_CASE missing-bwrap PASS  ENVDIFF_CASE timeout FAIL
ENVDIFF_CASE pin-mismatch-public-cli PASS
ENVDIFF_SELFTEST: 2/9 pass   exit=1
```

(the P1/P4/P2 case lines are the printed order, one case per line; the block above is the same nine
results, three to a row, verbatim in verdict.)

These three runs isolate each cause independently of round 47's archive: P4's single failure is
`pin-mismatch-public-cli` (the node branch, §3.5), and P2's two survivors are `missing-bwrap` and
`pin-mismatch-public-cli` (§3.4/§3.6) — the same two that survived under `--work /tmp` at freeze.

**Load was not a factor in these runs**: three peer seats were running `bwrap` concurrently
(`pgrep -a bwrap` → `T48ExecObs1/2/3 …--bind <decoy> … tally-audit-v3.py --selftest`) and every
out-of-`/tmp` shim still scored `9/9`; host figures at the time: `max_user_namespaces 122865`,
`kernel.unprivileged_userns_clone 1`, pids cgroup `2676/81090`, `/tmp` 2.7 G/128 G used.

## 5. Why it is **not** load-induced (the decisive argument)

1. **Same run, same instant.** In both masked runs, P0 (host env, inherited `PATH`, bwrap on
   `/usr/bin`) printed `9/9`, exit 0 — that is 42 successful bwrap sandbox creations *while* P1 was
   printing `2/9` (`before/c1-at-freeze.stdout:18`). A user-namespace / `clone` EAGAIN shortage
   under load would have broken P0 as well. It did not.
2. **Controlled A/B at fixed rev, counter, statements, host.** `T47ExecObsC.md:54` vs `:85`: only
   the `--work` path string differs; `2/9` ↔ `9/9`, `1/9` ↔ `8/9`, both directions reproduced.
3. **Direct probe already in the record.** `T47ExecObsC.md:166-178`: `PATH=/tmp/<work>/P1/shim` +
   the tool's own argv → `bwrap: execvp bash: No such file or directory` (rc=1);
   `PATH=/usr/bin:/bin` → `INSIDE_OK` (rc=0).
4. **My three runs** reproduce the two other causes exactly while the host is under real (peer)
   bwrap load, and the out-of-`/tmp` shim stays `9/9`.

`[INFERENCE]` I did not spend a fourth scratch run on the `/tmp`-masking step itself (my runs all
kept the shim outside `/tmp`, which is why they are `9/9`/`8/9`/`2/9` and not `2/9`/`1/9`/`2/9`);
that step rests on (2) and (3) above plus §3's code path, which is a direct read of the argv at
`tools/env-diff.py:68-71`. Everything else in this report is observed.

## 6. What the R=3 C1 counter must expect for this statement

Statement: cap `hermetic env-differential probe`, command `python3 tools/env-diff.py --selftest`.

* **Value set V: `stable`, one member —** backticked `ENVDIFF_SELFTEST: 9/9 pass`, exit 0,
  tool sha256 `e8b47ab7cf23` (same at `473336d` and at the round-48 base of the counter).
  `9/9` is the only P0 value in every archived run (freeze, `--emit`, w1 probes, deciding run) and
  P0 is *structurally* immune to the masking bug because it inherits the real `PATH`. A row that
  declares two members (`9/9` or `2/9`, `nondeterministic`) would need a **P0** `2/9` tuple to
  attest the second member; none exists and none can be produced by this mechanism — under the
  round-48 grammar that is `unattested > 0`, i.e. a miss. **Do not emit `2/9` as a standing value.**
  (This is precisely the round-47 closure defect being fixed: a one-shot broken-harness
  observation restated as a standing value.)
* **Dependence classification:** `bwrap` **required**, `node` **required**, `env` **unstable**
  (may be declared or omitted — declare it *nowhere*), `jj` and `fleet-root` **never observed**.
  Concretely: `deps `bwrap,node``.
  * `bwrap` required: P2 = `2/9`,1 ≠ P1 in every functional-sandbox round.
  * `node` required but thin: it is used only for the receipt's host string
    (`tools/env-diff.py:234-236`), never for a measurement; P4 = `8/9`,1. It is sheddable only by
    making that probe tolerant, which would change the tool and its pin.
  * `env` unstable: it is observed **iff** the round's shim was masked, i.e. iff `--work` was under
    `/tmp`. Declaring it would assert that the tool's output changes with `HOME/LANG/LC_ALL/TZ/PATH
    content`, which is false — the shim was invisible, not effective.
* **Operational requirement on the round-48 counter (`.ufo/evidence/round-48/calibration/measure.py`,
  built this wave from the round-47 base) and on the deciding run:** every one of the three
  observation rounds must use a `--work` outside `/tmp` (the contract's own deciding shape,
  `/var/tmp/…`). Consequences of breaking that rule:
  * one `/tmp` round among three → `bwrap` observed in some rounds only → `unstable` → declaring it
    is still allowed, so a `deps `bwrap,node`` row survives; but V is untouched (`9/9`), so the row
    is still truthful. Tolerable, not preferred.
  * three `/tmp` rounds → `bwrap` observed in **no** round, which the contract forbids declaring →
    the only passable row becomes the false `deps `env,node``. That is a C1 miss created by harness
    placement, on the axis C1 exists to measure.
  * Permanent fix (one line, harness side, no tool edit): build the shim outside the paths the
    statement's own sandbox replaces — e.g. under `/run/user/<uid>/` or a fixed `/var/tmp` temp
    root — and/or have `measure()` refuse a `--work` whose realpath is under `/tmp`. Note
    `os.path.abspath` does **not** resolve symlinks, so the round-47 `/tmp → /var/tmp` symlink
    workaround (`.ufo/waves/round-47/w1/T47ExecObsA.md:47`) still left `/tmp/…` in `PATH` and was
    still masked; a guard must test the literal string, not just the bytes' home.

## 7. Second-order calibration hazard for C1 (independent of this tool)

`measure()` compares every variant only against **P1**. Whenever P1 is already broken, P2/P3/P5
collapse onto P1 and the statement's real dependences silently vanish from the deps set — here
`bwrap,node` degenerates to `env,node` (`T47ExecObsC.md:186-214`; visible in the two rows of §2).
So a deps clause is only an oracle about dependences **while P1 is functional for that statement**.
Since round 48's C1 rests on deps sets for all 22 statements, the counter should assert, per
statement per round, that P1's tuple is the *complete/clean* one before crediting variant
discrimination. Advisory shapes (harness side only, no tool edits): require the round's P1 tuple to
equal the statement's P0 tuple whenever P0's own working conditions are verified, and flag any
statement whose five variant comparisons **all** equal P1 as "P1 uninformative — deps unknown"
rather than emitting an empty or shrunken dependence set. Otherwise the same shape of false
dependence can be emitted for any statement whose clean profile is broken for environmental reasons.

## 8. Bounds and hygiene

* Lane untouched: no write outside this report; all experiments ran on a `--shared` clone under
  `/fast/scratch/hyaku/tameshi-r48/T48RevenEnvDiff` (the tool was executed from that clone, unmodified,
  `sha256 e8b47ab7cf23…`). No `git add/commit/checkout/reset/pull/push`, no `jj` command.
* Three scratch selftest runs (the item's limit), then the scratch dir was removed.
* Tooling: nothing installed or upgraded this seat (no pacman/uv/npx operation); the host's
  `bubblewrap 0.13.1` (`/usr/bin/bwrap`, non-setuid, userns) was used as found.
