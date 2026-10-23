# Mutkillvectorfailexitswap — sealed kill copy `ho-kill-vector-fail-exit-swap`: KILLED; three witness-valid / audit-clean escape constructions found

Round 34 / wave 1 / mutation-tester seat (v2 policy). Lane tip at dispatch and at every run below:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailexitswap/` — every write below is there
(or is this file). No tool was installed or upgraded (bwrap 0.13.1 and Python 3.14.8 were already present);
no network access; the lane was never written to (§7). The default-mode kill rule was never invoked: the
counter was only imported as a module from the lane path and its functions were called on scratch copies.

## 1. Setup and pins

Commands (scratch root; every exit code captured to a file, never chained with `&&`):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailexitswap
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin .../Mutkillvectorfailexitswap/lane   # clone_rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                            # checkout_rc=0
env ... git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7        # rev_rc=0
env ... git -C .../lane show 0b99d48...:tools/tally-audit-v2.py  > tool.py                 # tool_extract_rc=0
env ... git -C .../lane show 0b99d48...:tools/mutate-and-run.sh  > pristine.sh             # runner_extract_rc=0
```

| artifact | sha256 (measured) | required pin | match |
|---|---|---|---|
| `tool.py` ← `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` ← `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `.ufo/evidence/round-33/c1/c1-measure.py` (imported from lane) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | same (amend-6 rev) | YES |
| `.ufo/evidence/round-33/heldout/ho-kill-vector-fail-exit-swap.json` | `9724e0c273c35fad3af2c14aa8d376845d51038a47126097766d0d58ff3ec88c` | lane copy identical | YES |

The lane clone carries the counter's `../../round-32/c1-measure.py` dependency
(`lane/.ufo/evidence/round-32/c1-measure.py`, sha256 `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca`),
so the counter imported from the lane path resolves its v1 module exactly as committed.
Deciding-run receipt read for context: `.ufo/evidence/round-34/measure/c1-deciding-run.stdout`
(`... ho_kill=8/8 ho_accept=6/6 ho_invalid=0 ... C1_R33_PASS=true`), `c1-deciding-run.exit` = `0`.

## 2. Baseline: the detector on pristine bytes

`run_tool_sandboxed(tool.py, copies/pristine.sh, work/pristine-baseline)` (`probe.py`, `probe.rc=0`):

```
outcome=ACCEPT  rc=0  last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
```

So the audit's accept side is live on these bytes; a subsequent KILL is attributable to the edit, not to
environment breakage.

## 3. The assigned mutation: `ho-kill-vector-fail-exit-swap` (set=kill)

Sealed JSON (raw file sha `9724e0c2…3ec88c`; `probe.py` prints a *normalised re-serialisation* hash
`80c21cf3…` — the on-disk file hash is the one to compare):

```json
{
 "id": "ho-kill-vector-fail-exit-swap",
 "author": "tameshi-shokunin L1 (TameshiR34)",
 "set": "kill",
 "edits": [
  {
   "old": "    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n",
   "new": "    exit 2\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n"
  }
 ],
 "witness": { "vector": [1,0,0,0,0,0,0,0,0] }
}
```

- Anchor count in `pristine.sh`: **1** (`SEALED_EDIT_OLD_OCCURS_IN_PRISTINE 1`); the site is
  `pristine.sh:1441-1447` — the FAIL branch of `run_regression`, whose `exit 1` sits at `pristine.sh:1445`.
- Derived mutant: sha256 `82edd80ed2c4d32d09fd2cc24e503e57992617f691b50e6e8c2ffad8d7ff314a`
  (`copies/sealed-target.sh`); tally-block sha256 `e163133c…a2215d` → `b71837b0…e8786b`.
- Witness run (`block_run`, counter line 154; vector `[1,0,0,0,0,0,0,0,0]`):
  pristine `(1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')`,
  mutant `(2, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')`.
  `ho_witness_ok` → `(True, 'vector')`.
- Real tool, via the counter's `run_tool_sandboxed` (bwrap; stdout-only):

```
outcome=KILL  rc=1  last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'
```

- Direct run `TMPDIR=$PWD/tmp-direct python3 -I tool.py --runner copies/sealed-target.sh`
  (`direct-target.rc=1`), full stdout (`direct-target.out`, sha `2d16a852…471c32`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime FAIL vectors=15158 mismatched=1800; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0: got (2, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)'), want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
```

**Verdict: KILLED.** The label is honoured: the tool exits 1 with `TALLY_AUDIT: FAIL`, and the failing
check is `runtime` on exactly the witness vector.

## 4. CRITICAL FINDING — three constructions of the same fault the amended witness VALIDATES and the tool ACCEPTS

Fault family (as labelled): the FAIL branch at `pristine.sh:1441` exits **2** instead of **1** on a failing
tally, i.e. the runner mislabels a regression FAIL as SETUP in its exit code while printing the FAIL line.
The amended `ho_witness_ok` (counter:184-218) validates a kill+vector copy iff the block bytes changed and
`a != b` on the submitted 9-vector (`return a != b, 'vector'`, counter:218) — **stdout and exit code are
compared as a tuple, and only the rc needs to differ.**

Findings (all four rows measured with the same driver, `probe.py`, `probe.rc=0`; the three variants are
written to `copies/adv-*.sh`):

| case | witness vector | `block_run` pristine → mutant | `ho_witness_ok` | `run_tool_sandboxed` | direct tool exit |
|---|---|---|---|---|---|
| sealed target | `1 0 0 0 0 0 0 0 0` | `(1,FAIL)` → `(2,FAIL)` | `(True,'vector')` | **KILL** rc 1, `runtime=fail` | 1 |
| **V1 root-gated** | `1 0 0 0 0 0 0 0 0` | `(1,FAIL)` → `(2,FAIL)` | `(True,'vector')` | **ACCEPT** rc 0, `runtime=pass` | 0 |
| **V2 triple-gated** | `3 5 0 1 0 0 0 0 0` | `(1,FAIL …1 setup)` → `(2,FAIL …1 setup)` | `(True,'vector')` | **ACCEPT** rc 0, `runtime=pass` | 0 |
| **V3 status-6-gated** | `6 0 0 1 0 0 0 0 0` | `(1,FAIL …1 setup)` → `(2,FAIL …1 setup)` | `(True,'vector')` | **ACCEPT** rc 0, `runtime=pass` | 0 |

Direct tool stdout is byte-identical for V1/V2/V3 (`e9444d03…fae0f0`), rc 0, per variant:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Each variant is a different construction of the *same* exit-code swap at the same statement, accepted by
`validate_ho` and `apply_edits` (anchor count asserted == 1), and each is validated as a must-kill witness
by the amended counter rule. The exact JSONs (the shape that would be committed under
`.ufo/evidence/round-33/heldout/`; blocks below are reflowed for width — the `edits` strings and
`witness.vector` values are verbatim):

```json
{
 "id": "adv-status6-gated-fail-exit-swap",
 "author": "Mutkillvectorfailexitswap (adversarial probe)",
 "set": "kill",
 "edits": [
  {
   "old": "    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n",
   "new": "    if [[ $st_js == 6 && $st_mado == 1 ]]; then\n      exit 2\n    fi\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n"
  }
 ],
 "witness": { "vector": [6,0,0,1,0,0,0,0,0] }
}
```

```json
{
 "id": "adv-triple-gated-fail-exit-swap",
 "author": "Mutkillvectorfailexitswap (adversarial probe)",
 "set": "kill",
 "edits": [
  {
   "old": "    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n",
   "new": "    if [[ $st_js == 3 && $st_kagi == 5 && $st_mado == 1 ]]; then\n      exit 2\n    fi\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n"
  }
 ],
 "witness": { "vector": [3,5,0,1,0,0,0,0,0] }
}
```

```json
{
 "id": "adv-root-gated-fail-exit-swap",
 "author": "Mutkillvectorfailexitswap (adversarial probe)",
 "set": "kill",
 "edits": [
  {
   "old": "    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n",
   "new": "    if [[ $root == r ]]; then\n      exit 2\n    fi\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n"
  }
 ],
 "witness": { "vector": [1,0,0,0,0,0,0,0,0] }
}
```

Mutant runner hashes: V1 `70170a42…164c1a`, V2 `49275482…e2c301`, V3 `243a159c…dd978e`
(`copies/adv-v1-root.sh`, `copies/adv-v2-triple.sh`, `copies/adv-v3-status6.sh`).

### 4.1 Why the tool misses them (its own vector panel, enumerated without editing it)

`probe2.py` imports the pinned `tool.py` as a module (bytes unmodified), wraps the module's own
`run_vectors` to record every vector it is handed, and calls `tool.check_runtime` on each variant block.
`probe2.rc=0`, `probe2.out` sha `0dc9b70e…43be9`:

| case | main-block vector executions (2 configs) | gate-true vectors | `check_runtime` |
|---|---|---|---|
| V1 root-gated | 15122 (+36 stress) | 296 (vector side; gate is on `$root`, not the vector) | `ok=True`, `mismatched=0` |
| V2 triple-gated | 15122 | **0** | `ok=True`, `mismatched=0` |
| V3 status-6-gated | 15122 | **0** | `ok=True`, `mismatched=0` |

The panel is: every status 0..255 alone at every position (`tool.py:381`), every (failing,setup) count pair
whose statuses are only `1`/`2` (`count_vectors`, `tool.py:362`), placement variants of those, and
co-occurrence vectors over **exactly two legs** with statuses from
`CO = (1,2,3,4,5,7,9,120,126,127,128,255)` (`tool.py:407-408`). Total 7561 vectors/config × 2 configs
= 15122, plus 36 operand-stress runs = 15158, matching the tool's own `vectors=15158`.

- **V3** needs status **6**; 6 is not in `CO`, and no count/mix vector contains a 6, so the pair
  (`st_js=6`, `st_mado=1`) is never executed. In runner semantics this is a real defect: one leg exits 6
  (a legal suite status → SETUP) and one leg fails → the copy prints `REGRESSION: FAIL … failed=1 setup=1`
  but exits 2, so the failing verdict is reported as SETUP to the caller.
- **V2** needs three non-zero legs (`3,5,1`); co-occurrence holds exactly two, and counts/mixes use only
  1/2, so it is never executed.
- **V1** needs `$root == r`. The witness harness hard-codes `local root=r auto=0 KEEP=1`
  (counter:167); the tool pins `CONFIGS = (('tally-audit','0','1'), ('/tmp/tally-audit-work','1','0'))`
  (`tool.py:265`, spliced at `tool.py:279`). The roots the audit uses are never `r`, so the swap never
  fires under audit. V1 is the weakest construction semantically (in a production run `root` is a scratch
  path, so it would not misfire); it matters because the *witness that authorises the must-kill label* runs
  in the one environment that triggers it.
- The tool's harness check cannot see any of them: it splices its internal `REF_BLOCK` after the runner's
  last `tblock=$(awk …)` line (`run_harness`, `tool.py:510-521`; splice at `tool.py:512`:
  `sec = section[:last.end()] + '  tblock=$AUDIT_INJECT\n' + …`), so the runner's own tally block is never
  executed by the harness panel.

### 4.2 Why the unconditional construction cannot escape (scope of the hole)

The sealed copy itself is caught because the FAIL-branch swap is unconditional: the witness vector
`[1,0,…]` is a member of the single-status sweep, and its `(rc, first line)` diverges there — the tool's
first mismatch is exactly that vector (`direct-target.out`, `mismatched=1800`). More generally, the amended
witness rule and the tool's runtime check agree on `(rc, first stdout line)` for the witness vector, so any
*unconditional* divergence visible to the witness is visible to the audit at that vector. **The escape is
only possible when the fault is gated on a condition the panel never forms** — a status value outside `CO`
(V3), more than two non-zero legs (V2), or the harness's private environment (V1). For this family the
unconditional form is proved detectible; the gated forms are demonstrated undetected.

### 4.3 Consequence for the claim (observation, not an overturn)

- The landed receipt stands: the committed sealed set contains none of these shapes, and the assigned copy
  is killed (§3). Nothing here changes `ho_kill=8/8 ho_accept=6/6 ho_invalid=0` or `C1_R33_PASS=true`.
- The counter would **fail closed**: had any of V1–V3 been committed to
  `.ufo/evidence/round-33/heldout/`, `validate_ho`, `apply_edits` and `ho_witness_ok` all pass, so
  `ho_kt` increments and `ho_k` does not — `ho_kill != ho_kt` → `C1_R33_PASS=false`. So this is not a
  false-pass path; it is a **coverage gap in the statement "exits 1 on every must-kill runner copy"** and in
  the sealed-set gate (a copy the witness certifies as must-kill can be one the tool literally cannot see).
- Two of the three escapes (V2, V3) are ordinary runner defects — statuses 3/5/6 are legal exit codes — so
  the gap is reachable without any knowledge of harness internals, while V1 additionally shows the audit's
  config pinning differs from the witness's environment.

## 5. Reproduction

Scratch is `.../Mutkillvectorfailexitswap/`; `probe.py` sha `65c10760…3cf77`, `probe2.py` sha
`6dc48117…929cd`. Each command's exit code is captured separately (no chaining):

```
cd /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorfailexitswap
python3 probe.py  > probe.out  2> probe.err ; echo $? > probe.rc     # probe.rc=0
python3 probe2.py > probe2.out 2> probe2.err; echo $? > probe2.rc    # probe2.rc=0
TMPDIR="$PWD/tmp-direct" python3 -I tool.py --runner copies/sealed-target.sh   > direct-target.out 2> direct-target.err; echo $? > direct-target.rc   # rc=1
TMPDIR="$PWD/tmp-direct" python3 -I tool.py --runner copies/adv-v3-status6.sh  > direct-v3.out     2> direct-v3.err;     echo $? > direct-v3.rc       # rc=0
TMPDIR="$PWD/tmp-direct" python3 -I tool.py --runner copies/adv-v1-root.sh     > direct-adv-v1-root.out 2>&1;            echo $? > direct-adv-v1-root.rc  # rc=0
TMPDIR="$PWD/tmp-direct" python3 -I tool.py --runner copies/adv-v2-triple.sh   > direct-adv-v2-triple.out 2>&1;          echo $? > direct-adv-v2-triple.rc # rc=0
```

`probe.py` performs, per case, exactly the counter's per-copy path: `validate_ho` → `apply_edits`
(anchor count == 1 enforced by the counter) → `tally_block_of`/`block_run` → `ho_witness_ok` →
`run_tool_sandboxed(tool.py, copy, scratch-workdir)`. Counter functions are imported from the lane copy
(`lane/.ufo/evidence/round-33/c1/c1-measure.py`, sha `f6b8868c…a07f28c`); no default-mode counter run was
made.

## 6. Actual-output summary (all from the files named above)

- pristine baseline: `ACCEPT rc=0` `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.
- sealed target: `KILL rc=1` `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`;
  direct run 1800/15158 mismatches, first mismatch on the witness vector (`got` rc 2, `want` rc 1).
- V1/V2/V3: witness `(True,'vector')`; `run_tool_sandboxed` `ACCEPT rc=0`
  `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`; direct runs 0/15158 mismatches.

## 7. Restoration and containment

Literal mutate → restore on a scratch mirror of the runner (`restore-demo.sh`), edit taken from the sealed
JSON:

| stage | sha256 |
|---|---|
| before (`cp pristine.sh restore-demo.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| mutated | `82edd80ed2c4d32d09fd2cc24e503e57992617f691b50e6e8c2ffad8d7ff314a` |
| restored (`cp pristine.sh restore-demo.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |

(The mutated hash equals `copies/sealed-target.sh`, i.e. the derived copy and the in-place mutation are the
same bytes.) After all runs:

- `sha256sum pristine.sh` = pin `a7d3f2dd…2eb9`; `tool.py` = pin `7b11ba25…8d10`;
  `lane/tools/mutate-and-run.sh` and `lane/tools/tally-audit-v2.py` still hash to their pins.
- `git -C lane rev-parse HEAD` = `0b99d48…68b7`; `git -C lane status --porcelain` empty (`status_rc=0`).
- No git/jj write command was run anywhere; `tmp-direct/` is empty after the direct runs (the tool removes
  its temp trees), and the sandboxed runs wrote only under `work/`.
- Files written outside scratch: this report only.

## 8. Evidence index (scratch, all sha256 recorded in §3–§5)

`probe.py`, `probe2.py`, `probe.out`, `probe2.out`, `probe.rc`, `probe2.rc`,
`copies/pristine.sh`, `copies/sealed-target.sh`, `copies/adv-v1-root.sh`, `copies/adv-v2-triple.sh`,
`copies/adv-v3-status6.sh`, `direct-target.{out,err,rc}`, `direct-v3.{out,err,rc}`,
`direct-adv-v1-root.{out,rc}`, `direct-adv-v2-triple.{out,rc}`, `restore-demo.sh`,
`work/` (per-case block-run and sandbox workdirs).

**Bottom line.** The assigned sealed copy `ho-kill-vector-fail-exit-swap` is **KILLED** exactly as labelled
(runtime check, rc 2 vs 1, `TALLY_AUDIT: FAIL`, exit 1), and pristine bytes are accept-clean. Three
constructions of the same FAIL-exit swap — gated on `$root == r`, on a three-leg `3/5/1` state, and on a
two-leg `6/1` state — each pass `validate_ho`/`apply_edits`/`ho_witness_ok` as a must-kill witness while
`tally-audit-v2` returns `TALLY_AUDIT: PASS`, exit 0: a critical, reproducible coverage gap between the
sealed-set witness gate and the audit's runtime panel within this fault family.
