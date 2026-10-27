# T51W2ExecTool16 — C3 registry row audit: `tools/round21-measure.py`

Round 51 wave 2, lane `tameshi-shokunin`, base `9962033fd7a75aa2f2847e979dd687a5d28505a1`,
candidate `6d8c11e378aa90b12650808e1b79270742935f15`. Axis: operability. Milestone: C3 row
falsification. Scope: **one row**, read-only on the lane and the fleet; no source, row, counter or
spec was modified. Tool blob at CAND: `tools/round21-measure.py` sha256
`eda5490acd447cd9eeac3ab10a348565b34d8a6fa2800d66a4fb1c80c162758d` (162 lines). Row:
`SKILL.md:2157`, inside `#### Gate/probe registry — round 51` (`SKILL.md:2138`); the tool is
**row 16** of `tools-base.json`.

All bytes cited are `git show 6d8c11e…:<path>`, never the lane worktree. Every self-test run below is
from a `git clone --shared` of the lane checked out detached at CAND (`rev-parse --show-toplevel`
printed the scratch clone before any run), with `TMPDIR` under the seat scratch and stdin `/dev/null`.
Receipts: `.ufo/waves/round-51/w2/T51W2ExecTool16/`.

**Bottom line.** The row is **counter-conformant and, on every field I could falsify from source,
truthful** — kind `gate` (it really returns 0 clean and 1 failed), verdict map complete over
`{0,1,2,64}`, all three pinned paths load-bearing, write scope exactly as written. It is nevertheless
**red in the predicate's own execution context**: this is row16, the known clone-context blocker, and
I prove the failure is caused *solely* by five live sibling fleet repos that the self-test reads
through `ROOT.parent`. I also found a **verdict-map meaning mismatch** (a present-but-failing sandbox
is graded `1 failed` although no measurement was made and `2` is reserved for setup) and an
**incomplete pin set** for the entry command.

| id | severity | one line |
|---|---|---|
| F1 | **material** (known blocker, now isolated) | Row's self-test from a clone at CAND: **exit 1, zero stdout lines, 48 ms**, traceback at `tools/round21-measure.py:74`. Adding only sibling-repo symlinks makes it **13/13, exit 0**. Frozen counter's `run_row` returns `selftest-exit=1 last=` → the tool counts `missing` under C3. |
| F2 | **material** | A **present but failing** sandbox (`bwrap` exiting 1) is reported as **exit 1 "failed"** with 18/18 `INCONCLUSIVE` — a could-not-evaluate condition minted as a measured failure. With `bwrap` *absent* the same setup fault yields **exit 2**. The row's `2 could-not-evaluate (setup …)` therefore does not cover the setup class it names. |
| F3 | disclosure | The pinned cell is load-bearing but **incomplete for the entry command**: `.ufo/evidence/round-21/c1-mutants.json` (the `--claim c1` expectation set, `c1-survivors.py:20`, digest echoed as `spec_sha256`) is unpinned, as is the hard-coded fleet root (`c1-survivors.py:21`, `c2-count.py:19`) that decides whether the row runs at all. |
| F4 | disclosure | The recorded finding id `ROUND21_MEASURE_SELFTEST: 13/13 pass` is a real diagnostic (it morphs to `10/13` and `9/13` under pin mutations), but **no finding id exists on any abort path** (P3 `KeyError` at `measure.py:116`; the clone traceback). The row records only the pass form. |
| F5 | verified true | `gate`, not probe: `--claim c2` at CAND → **exit 0**, `classified=9/9 tool_selftest=pass f5_entry=True`; over a repo with no receipt → **exit 1**. Write scope exact: 1 326 write-mode `openat`s, **1 057 under TMPDIR**, the rest `/dev/*` and `/proc/<pid>/{uid_map,gid_map,setgroups}`. Usage probe **64**. |
| F6 | note | One `exited 2` observation during a combined shell command (output discarded) was **not reproduced in 13 later identical runs** (all 0). Disclosed, not claimed as a defect. |

---

## 0. The row under audit

```
| round21 measure facade | gate | `python3 tools/round21-measure.py --claim c1 --repo DIR --rev REV --json` | 0 clean; 1 failed; 2 could-not-evaluate (setup or unknown rev); 64 could-not-evaluate (usage) | `python3 tools/round21-measure.py --selftest` → ROUND21_MEASURE_SELFTEST: 13/13 pass | `.ufo/evidence/round-21/c1-survivors.py`, `.ufo/evidence/round-21/c2-count.py`, `.ufo/evidence/round-21/c2-contract.json` | TMPDIR only (selftest fixtures and delegated counter receipts); target repo read-only | tameshi |
```

Reused the counter's own predicate functions instead of re-implementing them
(`counter-row-acceptance.txt`). Structural acceptance is total:

```
rows in the registry sections the counter scans: 32; rows whose ENTRY cell names the tool: [2157]
row_reason('tools/round21-measure.py', row 2157) -> None
argv  = ['python3','tools/round21-measure.py','--selftest']
usage = ['python3','tools/round21-measure.py','--r51-no-such-flag']
pinned cell tokens exist at REV: 3/3 (all present)
```

So the row passes every static clause; its fate is decided entirely at execution time (§1). The argv
the counter builds is byte-for-byte what I ran.

## 1. F1 — the row's exact self-test in the predicate's clone

`git clone --shared` of the lane at CAND, `TMPDIR=<scratch>/tmp/f2`, stdin `/dev/null`:

```
EXIT=1  WALL_MS=48  stdout_lines=0  stderr_lines=17
subprocess.CalledProcessError: Command '['git','-C','<WORK>/kumitate-shokunin','show',
  '175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs']' returned non-zero exit status 128.
  File ".../tools/round21-measure.py", line 74, in selftest
    data = subprocess.run(["git", "-C", str(ROOT.parent / surface["repo"]),
```

The mechanism is a hard dependency on the fleet layout: `ROOT = Path(__file__).resolve().parents[1]`
(`:21`) and every frozen surface is read as `ROOT.parent / surface["repo"]` (`:74`); the contract's
nine surfaces name the five sibling repos (`tameshi-shokunin`, `kumitate-shokunin`, `kagi-shokunin`,
`tsukuroi-shokunin`, `mado-shokunin`), and the delegated counters do the same through a literal path
(`c1-survivors.py:21`, `c2-count.py:19`: `FLEET = Path("/home/vgpnk/Projects/shokunin")`). In a clone,
`ROOT.parent` holds only the clone, so surface 2 fails. Note that surface 1 (`tameshi-runner` at
`08175c62…`) *passes* in the clone — because `ROOT.parent/"tameshi-shokunin"` **is the clone itself**;
the self-test silently grades a superseded revision of the clone in place of the frozen sibling
instance. That is why the traceback names `kumitate` and not `tameshi`.

Sole-cause isolation (three layouts, same clone bytes, same TMPDIR discipline):

| layout | exit | wall | last stdout line |
|---|---|---|---|
| `--shared` clone, nothing beside it (the predicate's layout) | **1** | 48 ms | *(none — 0 stdout lines)* |
| same clone + 4 sibling repos symlinked beside it | **0** | 1 345 ms | `ROUND21_MEASURE_SELFTEST: 13/13 pass` |
| clone of the lane at CAND inside a 5-repo fleet layout | **0** | 860 ms | `ROUND21_MEASURE_SELFTEST: 13/13 pass` |

Through the frozen counter's own code path:

```
run_row(fresh-clone-no-siblings) -> ['selftest-exit=1 last=', '']        # tool graded missing
run_row(fleet-layout)            -> [None, 'ROUND21_MEASURE_SELFTEST: 13/13 pass']
```

`counter-run-row.txt`, `clone-selftest.stderr`, `selftest-symlink.stdout`, `selftest-fleet.stdout`.

The row's claim "13/13 pass" is **true and reproducible wherever the fleet layout exists** (4 further
consecutive runs, all 0); it is **false in the only context C3 executes it in**. A row cannot make the
clone contain five sibling repositories, and the tool is outside this round's no-harm tools-scope
(`.ufo/evidence/round-51/no-harm.sh:35` allows only `mutate-and-run.sh` plus the four runner-panel
tools), so nothing available to wave 2 or to a re-key can turn this row green without editing the
tool. The L1's C3 blocker statement is confirmed in full: this row is the blocker, and no shim, shell
wrapper or row text can substitute for it.

**PROTOCOL hooks** (`PROTOCOL.md:375-410`):

- *Self-test*: "a self-invocation mode over isolated fixtures (temp trees, no network, no live-tree
  write)". This self-test writes no live tree (verified, §5) but it **reads live fleet trees through a
  host-absolute path** and cannot run without them — "isolated fixtures" is not met.
- *Two evidences*: "a gate whose verdict depends on a mutable fleet artifact also ships a run over a
  committed input snapshot". The entry mode does verify blob digests (`c2-count.py` `frozen-blob-drift`,
  `pin-blob-mismatch`), so a rewrite is caught for `--claim c2`; but the **self-test mode** carries the
  live-repo dependency unrecorded, and the row's pinned cell names no such input.
- The lane already discloses this in `.ufo/evidence/round-51/integrate/l1-notes.md`; this seat adds
  the measurement and the isolation proof, not a new blocker.

## 2. Exit codes and meanings (F2)

| code | input | observed | row says |
|---|---|---|---|
| 0 | `--claim c2 --repo CLONE --rev CAND --json` | exit 0, `classified=9/9 tool_selftest=pass f5_entry=True`, 796 ms | `0 clean` ✓ |
| 1 | `--claim c2 --repo TINY_FIXTURE --rev HEAD --json` | exit 1, `classified=0/9 tool_selftest=fail f5_entry=False` | `1 failed` ✓ |
| 1 | `--claim c1 … --json` with `bwrap` present but exit-1 (stub first in PATH) | exit 1, `killed=0 survived=0 inconclusive=18/18`, every control exit 1, 838 ms | **not declared** — this is setup, which the row maps to `2` |
| 2 | `--claim c2 --repo CLONE --rev ffff…` | exit 2, `C2: cannot resolve rev`, 66 ms | `2 could-not-evaluate (unknown rev)` ✓ |
| 2 | `--claim c1 … --json` with `bwrap` absent from PATH | exit 2, `C1: setup failure: [Errno 2] No such file or directory: 'bwrap'` | `2 could-not-evaluate (setup)` ✓ |
| 64 | `--r51-no-such-flag` | exit 64, stderr `MEASURE_USAGE: unrecognized arguments: --r51-no-such-flag`, 39 ms | `64 could-not-evaluate (usage)` ✓ |

No undeclared code is reachable (both delegated counters return only 0/1/2/64 and pass-through is
literal, `:158`), but the **class** is wrong for one input family: a sandbox that exists and refuses to
run is a could-not-evaluate condition (nothing was measured; all 18 rows are `INCONCLUSIVE`), and it
reaches a reader as `1 failed` — "the claim did not verify". Under PROTOCOL's Verdict clause a
non-measurement must map to `could-not-evaluate`; a red row would here be read as a red claim. The
same absorption applies to a control timeout (`INCONCLUSIVE (timeout)` → exit 1).

## 3. Pins — listed ones are load-bearing, the set is short (F3)

Three probes against the fleet-layout clone, each mutated in place and restored from the clone
(`git -C <clone> rev-parse --show-toplevel` verified first; post-restore hashes equal CAND,
`pin-restore.txt`):

| probe | mutation | result |
|---|---|---|
| P1 | `c1-survivors.py:151` exit convention → `return 0` | `EXIT=1`, `MEASURE_CASE c1-survived/missing-anchor/pristine-red FAIL`, **10/13 pass** |
| P2 | `c2-count.py:173` exit convention → `return 0` | `EXIT=1`, 4 `FAIL` lines, **9/13 pass** |
| P3 | delete `"tz"` from `c2-contract.json` `required_profiles` | `EXIT=1`, uncaught `KeyError: 'tz'` at `measure.py:116`, 5 `MEASURE_CASE` lines, **no marker** |

So all three listed pins decide the self-test's verdict — the cell is true. What it omits:

- `.ufo/evidence/round-21/c1-mutants.json` — the actual expectation set for the entry command
  (`SPEC = HERE / "c1-mutants.json"`, `c1-survivors.py:20`; the gate prints its digest as
  `spec_sha256`). Editing it changes `--claim c1` verdicts without tripping any listed pin.
- The hard-coded fleet root `Path("/home/vgpnk/Projects/shokunin")` (`c1-survivors.py:21`,
  `c2-count.py:19`) and `ROOT.parent` (`measure.py:74`) — the unpinned, host-specific precondition that
  makes F1 possible.

Both are properties of the *entry* command's environment rather than of the self-test's expected
values, so this is a disclosure, not a false cell.

## 4. Kind, marker, write scope

**Kind = gate** (F5). A gate "reads surfaces, compares them against expected values persisted in its
own repo, and returns a verdict": the facade delegates to the frozen counters, which hold their
expectations in the lane (mutant spec, contract) and return 0/1/2 — and I measured both a real 0 and a
real 1 through the facade (§2). Not a probe.

**Marker** (F4). `ROUND21_MEASURE_SELFTEST: 13/13 pass` is printed at `:133` after all 13 named checks;
its count is `passed/len(checks)`, so it carries diagnostic signal — P1 and P2 moved it to `10/13` and
`9/13` with named `MEASURE_CASE … FAIL` lines. It is not author-chosen help text: the tool's help path
(`--help`, `--help --selftest`, `--selftest --help`) exits 0 but its last stdout line is
`  --selftest`, whose first token is `--selftest` — it can never produce `ROUND21_MEASURE_SELFTEST:`.
That matters because wave-1 seat `T51CritC3Counter` showed a loose row can cover this very tool with
`--help --selftest`; **this row does not take that escape**. The remaining gap is the abort path: on a
traceback (P3, and the clone in §1) stdout carries partial `MEASURE_CASE` lines and no marker at all,
so the row records a finding id that exists only when the run reaches the end.

**Write scope = "TMPDIR only …; target repo read-only"** (F5, exact). Full-tree `strace -f -y` of the
green self-test: 1 326 write-mode `openat`s, 1 057 under `TMPDIR`; the remainder are `/dev/null` (137),
`/dev/tty` (11), the sandbox's `/newroot/dev/*` (11 each) and `/proc/<pid>/{uid_map,gid_map,setgroups}`
(22/22/11) from `bwrap` setup — **zero** writes to the lane, the fleet or any target repo
(`write-scope.summary.txt`, `write-scope.outside-nondev.txt`). The clone's `.git/objects` count is
unchanged (1 → 1) across the run, `git status` is clean in the clone, the fleet-layout clone and the
target fixture, and no `tameshi-r21*` directory survives in `/tmp`. The delegated counters do honour
`TMPDIR` (`tempfile.mkdtemp`) and clone the target instead of mutating it (`c1-survivors.py:100-118`,
`c2-count.py:tool_selftest`). The cell's phrase "delegated counter receipts" is loose — those counters
write no file receipts, they print JSON — but no claim in the cell is false.

## 5. What this changes for C3

Nothing in the predicate, the counter, the row text or the spec was touched. The finding is that
**this row can only be red at REV, and honestly so**: exit 1, no finding id, tool counted `missing`,
`C3_R51_PASS=false`. Fixing it needs an edit to `tools/round21-measure.py` (make the self-test build
its cross-repo fixtures from committed bytes, or skip/`could-not-evaluate` when `ROOT.parent` lacks the
siblings), which this round's no-harm tools-scope forbids; and any row text that made the cell match
an abort traceback would be a lie. Wave-1's fixture-A route (`--help --selftest`) is a counter
weakness, not a row this seat may write.

## 6. Limits and hazards

- Lane worktree bytes are **not** the audit's source: sibling seats were editing `SKILL.md` and
  `tools/` concurrently. Everything cited is `git show` at CAND plus clones of it; the fleet-layout
  clone's frozen counters were hash-matched to CAND after every probe.
- The green runs depend on tools outside the lane (`bwrap` 0.13.1, `git`, `node` via the sibling
  repos). The self-test is not hermetic, which is exactly F1's standard hook.
- One unexplained `EXIT=2` was seen once with stdout/stderr discarded; 13 subsequent identical runs
  exited 0 (§F6). No claim rests on it.
- Seat scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool16/` (including the `--shared` clones and
  the probe mutations' backups) is deleted before yield; the report and its receipts are the only
  artefacts left behind.
