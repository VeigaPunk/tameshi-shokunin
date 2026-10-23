# ResiduePreambleSeeding — C1 preamble seeding: head-local rename of `auto`

Round 34 / wave 1 (v2, build+attack) / mutation-tester seat. Claim under attack: **C1** (operability
capability acquisition, `tools/tally-audit-v2.py`), measured TRUE at revision
`c17e593b51802dd4ed568da3265f21c6d00c4273`. Lane tip at dispatch:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ResiduePreambleSeeding/`. All writes are inside that
scratch dir plus this one report file (the sanctioned exception); no other lane path was written (§6).
No tools installed or upgraded; no pacman; no network.

**Verdict: SURVIVED, and witness-blessed.** A head-local rename of `auto` (one rename refactor, two
lines, head only; tally block byte-identical) turns the runner's PASS path into `auto: unbound
variable` + exit 1 + leaked workdir, in **both** runner configs. The frozen tool returns
`TALLY_AUDIT: PASS`, exit 0, with stdout **byte-identical** to the pristine run (same sha256
`e9444d03…26fae0f0`); the counter's set-aware witness gate returns `(True, 'head')`, and the exact
sandboxed counter path scores the copy as an accept hit. This is a **coverage finding** (§5, rides to
round 35 as a Hold) — the landed deciding run stands: no such copy exists in the sealed set, so
`ho_accept=6/6 ho_invalid=0 C1_R33_PASS=true` is untouched.

## 1. Setup and pins

Commands (scratch root; every exit code captured to a file, never `&&`):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ResiduePreambleSeeding                                    # clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../ResiduePreambleSeeding/lane                          # clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                                               # checkout.rc=0
git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                              # head.rc=0, head.txt
git -C .../lane show 0b99d48…:tools/tally-audit-v2.py  > tool.py                                         # tool.rc=0
git -C .../lane show 0b99d48…:tools/mutate-and-run.sh   > pristine.sh                                    # runner.rc=0
```

| artifact | sha256 observed | pin / expectation | match |
|---|---|---|---|
| `tool.py` (`tools/tally-audit-v2.py` at `0b99d48`) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same (byte-pinned) | YES |
| `pristine.sh` (`tools/mutate-and-run.sh` at `0b99d48`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same (byte-pinned) | YES |
| counter `.ufo/evidence/round-33/c1/c1-measure.py` (at lane tip) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amend-6 pin `f6b8868c…a07f28c` | YES |
| `lane/tools/tally-audit-v2.py` (worktree copy) | `7b11ba25…8d10` | tool pin | YES |

The counter is imported **as a module** from the lane clone (read-only) — `importlib` load of
`lane/.ufo/evidence/round-33/c1/c1-measure.py`; its `../round-32/c1-measure.py` import resolves inside
the clone. Default mode was **never** invoked (kill rule consumed). Only `block_run`, `ho_witness_ok`,
`validate_ho`, `apply_edits`, `tally_block_of`, `head_of`, `run_tool_sandboxed` are called.

Read-only observation: the live lane HEAD read as `a5b1936425d3533b2ce280b16208386dcb0dc4ee`
(`merge-base --is-ancestor 0b99d48 a5b1936` → exit 0; parent of `a5b1936` is the dispatch tip). All
verification here is pinned to `0b99d48`; the advance is the L1's post-dispatch evidence commit, not
this seat (this seat wrote only inside scratch + this file).

## 2. The mutation (one rename refactor, two head lines)

Applied to the pristine runner with the counter's `apply_edits` (each anchor asserted count == 1;
`probe/mutate.rc=0`). `mutant.diff` sha256 `7f1c2350d18845d87873739b4d674ff4395309cd9be2b09f7384b49982fc2323`,
`diff` exit 1 (differences present), exactly this one hunk:

```diff
--- pristine.sh
+++ mut/runner-auto-rename.sh
@@ -1354,11 +1354,11 @@
-  local root specs auto=0
+  local root specs autodirs=0
   FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")
   if [[ -z "$WORKDIR" ]]; then
     root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX) || die_setup 'mktemp -d failed'
-    auto=1
+    autodirs=1
   else
```

The head-local is renamed **consistently** (`local … auto=0` at `pristine.sh:1357` and `auto=1` at
`pristine.sh:1361`); the tally block is untouched, so its one read site `if [[ $auto -eq 1 && $KEEP
-eq 0 ]]` (`pristine.sh:1464`) now names a variable nothing assigns. `set -u -o pipefail` is active
globally (`pristine.sh:175`), so the read aborts.

| artifact | sha256 |
|---|---|
| `mut/runner-auto-rename.sh` (mutant) | `c915eedd0ffb4af018c51483ec0ca975a8171c8fb0bfd81a649e1354cadf0418` |
| tally block, pristine vs mutant | **byte-identical**, `tally_block_of` equality `True`, block sha256 `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |
| `head_of` differs | `True` (the diff is entirely outside the block) |

The copy used inside the counter sandbox (`work/ho/copy/m.sh`) is byte-identical to the mutant:
sha256 `c915eedd…f0418`.

## 3. Detectors and results

### 3.1 The claim's own predicate — the frozen tool

```
python3 -I tool.py --runner pristine.sh                 > probe/tool-pristine.out   # probe/tool-pristine.rc=0
python3 -I tool.py --runner mut/runner-auto-rename.sh   > probe/tool-mutant.out     # probe/tool-mutant.rc=0
python3 -I tool.py --runner restored.sh                 > probe/tool-restored.out   # probe/tool-restored.rc=0
```

| bytes | exit | last line | stdout sha256 |
|---|---|---|---|
| pristine `a7d3f2dd` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `e9444d03cf653fd28076078fbb22d03d83a0e870a1487069f0f869af26fae0f0` |
| mutant `c915eedd` | **0** | **`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`** | **`e9444d03…26fae0f0` (identical)** |
| restored `a7d3f2dd` | 0 | `TALLY_AUDIT: PASS (…)` | `e9444d03…26fae0f0` (identical) |

All four checks pass with the same counters (`CHECK runtime PASS vectors=15158 mismatched=0`,
`CHECK harness PASS reference cases=9; faults rejected=34/34`). Mechanism: `check_head` inspects only
`st_*` leg names (`tool.py:307-342`); `check_runtime` splices the block into a synthetic driver that
**declares the block's free variables itself** — `local root=%s auto=%s KEEP=%s` (`tool.py:279`) —
so the mutant's missing head definition is supplied by the harness, not by the runner.

### 3.2 The counter's witness gate (`probe/witness.out`, sha256 `1b9e5390…30bdc3ec`; `probe/witness.rc=0`)

| authored witness for the same mutant bytes | `ho_witness_ok` verdict |
|---|---|
| `accept` + `kind: head` | **`(True, 'head')`** — blessed |
| `accept` + `vector [0]*9` | `(True, 'vector-equivalence')` |
| `accept` + `vector [1,0,…]` | `(True, 'vector-equivalence')` |
| `kill` + `kind: head` | `(False, 'head-edit-cannot-kill')` — class unauthorable as kill |
| `kill` + `vector [0]*9` | `(False, 'block-identical')` — class unauthorable as kill |

`block_run` equality is vacuous here (`probe/block-run-eq.out`, `probe/block-run-eq.rc=0`): `pb == mb
= True` and, for vectors `[0]*9`, `[1,0,…]`, `[0,1,0,2,0,0,0,0,0]`, `block_run(pb) == block_run(mb)`
with identical tuples. The head branch of `ho_witness_ok` (`c1-measure.py:192-207`) returns **before**
the two `block_run` calls at `c1-measure.py:212-213`; the vector branch compares only the two blocks.

### 3.3 Exact counter path, sandboxed (one-copy simulation of `main()`'s held-out loop)

`probe/ho-copy-sim.out`, sha256 `060e2dc3…a9bb897a`; `probe/ho-copy-sim.rc=0`:

```
witness=(True, 'head')
run_tool_sandboxed outcome=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
counter would count this accept copy as ho_a hit: True
```

Same calls the deciding run makes (`validate_ho` → `apply_edits` → `ho_witness_ok` →
`run_tool_sandboxed` under bwrap, `c1-measure.py:234-263`). If this copy had existed in
`.ufo/evidence/round-33/heldout/`, `ho_invalid` stays 0 and `ho_accept` increments — with a
behaviorally lethal member.

### 3.4 Ground truth — the runner's own code path (not the seeded harness)

Built from the **actual bytes** of each runner: the head's local-declaration line and its
`auto=1` assignment, followed by the extracted tally block, executed under the runner's own
`set -u -o pipefail` with the runner's default `KEEP=0` (`pristine.sh:190`).
`probe/groundtruth.out` sha256 `aaaed454…abdb7067`, `probe/groundtruth.rc=0`:

```
==== pristine (head var=auto)     exit=0
GT rc=0
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: …/gt.wi2Pg1 (removed on PASS; --keep retains)
leftover workdirs: []
==== mutant (head var=autodirs)   exit=0
GT rc=1
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
work/gt/mutant.sh: line 40: auto: unbound variable
leftover workdirs: ['gt.F6loM3']
```

(`exit=` in those headers is the wrapper script's status; `GT rc=` is the tally's own status, captured
inside the wrapper.)

The `--workdir` branch (`auto` never assigned) reproduces the same abort — `probe/gt-workdir-config.out`
sha256 `ff7e9c9d…35b93574`, `probe/gt-workdir-config.rc=0`: pristine rc 0 `(kept)`, mutant rc 1
`auto: unbound variable`. So the mutant is broken in **both** configs; the defect is dormant only on
FAIL/SETUP paths (which `exit` before the PASS branch). `probe/restored-row.out`
(`probe/restored-row.rc=0`) replays the auto=1 path on the restored bytes: rc 0, `(removed on PASS)`,
`leftover: []`; witness on `(pristine, restored)` → `(False, 'head')` (heads identical).

`probe/no-seed.out` (`probe/no-seed.rc=0`) shows the block genuinely depends on the head for `auto`:
the pristine block run under a driver that seeds `root`/`KEEP` but not `auto` also aborts with
`auto: unbound variable`. Seeding is structurally necessary to isolate the block — the missing step
is that nothing checks the head still supplies what the block reads.

### 3.5 Sensitivity controls — is the detector live?

| control (block-side edit to the same file) | sha256 | tool exit | verdict |
|---|---|---|---|
| `ctl1` `$nfail -gt 0` → `-gt 1` (`mut/ctl1-fail-threshold.sh`) | `17496eb0…62fcdb7e` | **1** | `CHECK runtime FAIL … mismatched=1638` → `TALLY_AUDIT: FAIL` (`probe/tool-ctl1.rc=1`, out sha `b3a6d36a…65843294`) — detector is live |
| `ctl2` `$auto -eq 1` → `$auto -eq 2` (`mut/ctl2-auto-guard.sh`) | `47787880…dc7653ca` | 0 | `TALLY_AUDIT: PASS` (`probe/tool-ctl2.rc=0`) — the `auto` guard is unobservable even block-side |
| `ctl3` workdir line text `(removed on PASS; --keep retains)` → `(dropped)` (`mut/ctl3-workdir-line.sh`) | `4dc96750…ea21f249` | 0 | `TALLY_AUDIT: PASS` (`probe/tool-ctl3.rc=0`) — a second-line-only edit survives |

`probe/second-line.out` (sha `ead3baaf…df1bc7d6`, rc 0) shows why: under the runner's real default
(`auto=1 KEEP=0`) the pristine block prints `(removed on PASS…)` while `ctl2` prints `(kept)` — same
rc 0, same **first** line. The oracle compares `${out%%$'\n'*}` only (`tool.py:281`, `oracle` at
`tool.py:290-302`), so line 2 and the `rm` never reach the compared tuple.

## 4. Verdict

**SURVIVED.** Not killed, not inconclusive.

- Expected detector: `python3 -I tools/tally-audit-v2.py --runner COPY` exits 1 with
  `TALLY_AUDIT: FAIL` on a runner whose regression tally path is broken.
- Observed: exit 0, stdout byte-identical to pristine on the lethal copy.
- The witness gate and the exact sandboxed counter path both bless the copy as a valid accept.
- Ground truth proves a real regression (rc 1 after emitting `PASS`, leaked workdir, both configs),
  so this is not an equivalent-mutant artifact.
- Baseline is healthy: pristine and restored both PASS; `ctl1` is killed with 1,638 oracle
  mismatches, so the detector is not vacuous.

## 5. Findings (measurement-only; round-35 Holds — no tool edit proposed as landed work)

**F1 — preamble seeding leaves the head unaudited.** The audit (`tool.py:279`), the counter's witness
(`c1-measure.py:167`) and the runner's own selftest harness (`pristine.sh:2003`) each supply `root`,
`auto`, `KEEP` from a synthetic preamble and never require the head to define them, although the block
reads `$auto` and `$root`. A head-local rename of `auto` therefore passes all four checks while the
runner dies at `pristine.sh:1464`. Reproduce: §2, §3.1, §3.4. This is the assigned class and the reason
the mutant survives.

**F2 — `accept+head` is behavior-blind.** `ho_witness_ok` returns at `c1-measure.py:192-207`
without any `block_run`; the only head requirement is "block unchanged". The two sealed accept+head
copies are inert (`ho-accept-head-comment`: a comment; `ho-accept-head-version-rename`: the `VERSION`
string), so no behavior-bearing head edit is exercised. Reproduce: `probe/witness.out` row 1, §3.2.

**F3 — `accept+vector` equivalence is vacuous for head-only edits.** With an identical block,
`pb == mb`, so `a == b` holds by construction (`c1-measure.py:212-215`). The witness cannot
distinguish a benign head edit from a lethal one. Reproduce: `probe/block-run-eq.out`, §3.2.

**F4 — the witness pins one config; the guard surface is unobservable.** `block_run` hardcodes
`local root=r auto=0 KEEP=1` (`c1-measure.py:167`) — the *non-default* runner config — while the tool's
runtime oracle compares only the first stdout line. Any change confined to the workdir-removal branch,
including a guard over `$auto`, is invisible to both: `ctl2` and `ctl3` both survive (§3.5). The
DevGuard rationale recorded at `tool.py:272-275` ("the sweep must run under both") is not connected to
the compared tuple for this guard. Reproduce: `probe/tool-ctl2.out`, `probe/tool-ctl3.out`,
`probe/second-line.out`.

**F5 — landed-doc discrepancy on "whole-stdout comparison".** `corpus/lessons/round-34.md` Holds says
"whole-stdout comparison already landed as the r33 DevPrintf fix" (round-33.md instead records it as
the *ninth measured v3 fix*, i.e. routed, not adopted). At the measured rev the runtime oracles compare
only the first line (`tool.py:281`; `lane/tools/tally-audit.py:174`), and so does the runner's own
harness comparator (`pristine.sh:2006`, mirrored by the tool's selftest seed at `tool.py:606`).
`ctl3` — a `REGRESSION_WORKDIR` line edit, the exact DevPrintf survivor class — is accepted. Either the
Holds sentence or the artifact is wrong; the bytes say first-line-only.
Reproduce: §3.5 ctl3, plus the cited lines.

Direction for round 35 (not adopted here): a head-definition coverage check (every non-leg name the
block reads must be declared/assigned before the block, or the seeded names must be verified against
the head's own declarations), a behavior-bearing accept+head rule, whole-stdout comparison, and a
witness config set that includes the runner's real default `auto=1 KEEP=0`.

## 6. Restoration and read-only evidence

- `restored.sh` re-extracted from `git show 0b99d48…:tools/mutate-and-run.sh` (`probe/restore.rc=0`):
  sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` = pin; `cmp restored.sh
  pristine.sh` exit 0 (`cmp_rc=0`). `pristine.sh` was never modified (it is a separate file from the
  mutant copy); its pin hash holds after all runs (§1 table, re-checked at the end).
- Restored-bytes detector run: `python3 -I tool.py --runner restored.sh` exit 0, `TALLY_AUDIT: PASS`,
  stdout sha256 `e9444d03…26fae0f0` — byte-identical to the pristine run; restored ground truth rc 0,
  workdir removed, no leak (§3.4).
- Tool bytes untouched: `tool.py` = `7b11ba25…8d10` after every run; lane clone worktree clean
  (`git -C lane status --porcelain | wc -l` → `0`), HEAD still `0b99d48…`.
- No `git`/`jj` write command anywhere; no writes to any lane path other than this report, and none to
  `.ufo/state/`, `MANIFEST.json`, fleet templates/scripts, or sibling repos. Writes: scratch dir + this
  report.
- No tool installs/upgrades (nothing needed; `python3`, `bash`, `bwrap`, `sha256sum` were present).

## 7. Reproduce

Scratch root = `/fast/scratch/hyaku/tameshi-r34-seats/ResiduePreambleSeeding`.

```
mkdir -p .; env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin lane; echo $? > clone.rc
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo $? > checkout.rc
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh  > pristine.sh
sha256sum tool.py pristine.sh   # 7b11ba25…8d10 / a7d3f2dd…2eb9
# mutant = the two-line rename in §2 (anchors unique); then:
python3 -I tool.py --runner pristine.sh;                 echo $?   # 0, TALLY_AUDIT: PASS
python3 -I tool.py --runner mut/runner-auto-rename.sh;   echo $?   # 0, TALLY_AUDIT: PASS  (survives)
python3 -I tool.py --runner mut/ctl1-fail-threshold.sh;  echo $?   # 1, TALLY_AUDIT: FAIL  (detector live)
python3 -I tool.py --runner mut/ctl3-workdir-line.sh;    echo $?   # 0, TALLY_AUDIT: PASS  (F5)
# witness rows: import the counter as a module, call validate_ho + ho_witness_ok (accept+head,
# accept+vector, kill+head, kill+vector) and block_run on the equality vectors — see §3.2/§3.3.
# ground truth: declare the head's local line, assign it as the auto branch does, splice
# tally_block_of(runner) under `set -u -o pipefail` with KEEP=0 — see §3.4 (scripts kept in work/).
```

Expected: pristine/restored PASS; mutant PASS (survived); witness `(True, 'head')` and
`(True, 'vector-equivalence')`, kill forms refused; ground truth mutant rc 1 `auto: unbound variable`
with a leaked workdir; `ctl1` FAIL; `ctl2`/`ctl3` PASS.
