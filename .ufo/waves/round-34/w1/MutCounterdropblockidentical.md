# MutCounterdropblockidentical — C1 witness gate, block-identical refusal removed

Round 34 / wave 1 / mutation tester seat. Lane tip: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropblockidentical/` (all writes here + this file).
No tools installed or upgraded; no network fetch; lane untouched (see §7).

## 1. Setup and pins

Commands (scratch root, every exit code captured to a file):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropblockidentical
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../MutCounterdropblockidentical/lane   # clone.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                             # checkout.exit=0
git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7            # head.exit=0
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py  > tool.py                     # tool.exit=0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh   > pristine.sh                 # pristine.exit=0
```

| artifact | sha256 | pin | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | same (amend-6 rev) | YES |
| `.ufo/evidence/round-33/c1/controls-receipt.json` | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` | unmodified | — |

(`frozen.sha`, `frozen.exit=0`; the two `sha256sum` lines above are the file's own contents.)

## 2. The mutation (one semantic edit)

Scratch mirror keeps the counter's `../../round-32/c1-measure.py` import path intact:
`mut/.ufo/evidence/round-33/c1/c1-measure.py` + `mut/.ufo/evidence/round-32/c1-measure.py`.

Removed the kill+vector block-identical refusal in `ho_witness_ok` (counter lines 216-217, anchor count == 1):

```diff
--- lane/.ufo/evidence/round-33/c1/c1-measure.py
+++ mut/.ufo/evidence/round-33/c1/c1-measure.py
@@ -213,8 +213,6 @@
     b = block_run(mb, vec, work)
     if ho['set'] == 'accept':
         return a == b and mutated != pristine, 'vector-equivalence'
-    if pb == mb:
-        return False, 'block-identical'
     return a != b, 'vector'
```

`mut.diff` (`mutdiff.exit=diff_exit=1`, i.e. exactly this hunk); `py_compile` of the mutant: `compile_ok`, `mutcompile.exit=0`.

| stage | sha256 of `mut/.ufo/evidence/round-33/c1/c1-measure.py` |
|---|---|
| before | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` |
| mutated | `0519669b5efe5f2fb09dc9e13fccaf8216fac643c725bf57c530b5db5c5cb3ba` |
| restored | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` (byte-identical, `cmp.exit=cmp_exit=0`) |

## 3. Detector: the committed 8-probe battery, rebuilt

`probe.py` (sha256 `dbfb432ed4f8db1a778eade9f050d09242c28e09afefe5299ff4d7f3e0a51eab`) imports the counter under test as a module and calls `ho_witness_ok` on 8 runners rebuilt from `pristine.sh` with one-anchor edits (each anchor asserted count==1; edits constructed to match the committed probe names in `.ufo/evidence/round-34/dev/witness-probes.json`, sha256 `0b2a6da5...3deca8`):

| probe | set | witness | runner edit |
|---|---|---|---|
| Q1-comment-accept | accept | vector `[0,0,1,0,1,0,0,1,0]` | benign comment inside the tally block |
| Q3-inert-head-kill | kill | head | `# probe` comment appended to `VERSION` line (head only) |
| Q3b-ridealong-accept | accept | head | head comment + block comment |
| K-extra-leg-assign-kill | kill | head | extra `st_js=0` after `st_citecheck=$?` |
| K-nonbare-leg-kill | kill | head | `st_js=$?` with ` || true` appended (leg assign no longer bare) |
| A-inert-head-accept | accept | head | head comment (same bytes as Q3) |
| A-head-with-block | accept | head | head comment + block comment (same bytes as Q3b) |
| KV-block-identical | kill | vector (same 9-vector) | head comment only: block byte-identical |

The 8 rebuilt runner hashes are identical in all three stages (`mutated-runner bytes identical baseline vs mutant: True`, `... vs restored: True`). Edits touch only the head or only a comment line; no leg logic, no runner tooling.

## 4. Actual outputs

**Pristine counter** (`baseline.exit=0`): every tuple equals the committed expectation.

```
Q1-comment-accept -> (True, 'vector-equivalence')
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')
Q3b-ridealong-accept -> (False, 'head-with-block-edit')
K-extra-leg-assign-kill -> (True, 'head-leg-assignment')
K-nonbare-leg-kill -> (True, 'head-leg-assignment')
A-inert-head-accept -> (True, 'head')
A-head-with-block -> (False, 'head-with-block-edit')
KV-block-identical -> (False, 'block-identical')
BASELINE: all_expected=True mismatches=[]
```

**Mutant counter** (`mutant.exit=1`):

```
Q1-comment-accept -> (True, 'vector-equivalence')
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')
Q3b-ridealong-accept -> (False, 'head-with-block-edit')
K-extra-leg-assign-kill -> (True, 'head-leg-assignment')
K-nonbare-leg-kill -> (True, 'head-leg-assignment')
A-inert-head-accept -> (True, 'head')
A-head-with-block -> (False, 'head-with-block-edit')
KV-block-identical -> (False, 'vector')            <-- expected (False, 'block-identical')
MUTANT: all_expected=False mismatches=['KV-block-identical']
```

**Restored counter** (`restored.exit=0`): identical to the baseline block above, `RESTORED: all_expected=True mismatches=[]`.

## 5. Verdict

**KILLED at the battery's recorded level — 1/8 probe verdicts flip (KV-block-identical), 0/8 boolean decisions flip.**

- Not a no-op mutant: the committed battery compares the full `(bool, reason)` tuple, and the recorded string for KV-block-identical is `"KV-block-identical -> (False, 'block-identical')"`; the mutant emits `(False, 'vector')`. One probe is wrong, so the detector fires.
- The mutant is nevertheless **decision-inert**: `pb == mb` forces `a == b`, because `block_run` is a pure function of (block text, vector) — the harness sets `local root=r`, never the workdir, and each run only renders the same script. Measured: `block_run(pb) x3` and `block_run(mb) x3` all returned `(1, 'REGRESSION: FAIL (cases=9 passed=6 failed=3 setup=0)')`; `KV case: pb == mb = True`, `a == b = True`, deterministic. So the removed early return could only ever have printed a different reason; `a != b` still refuses.
- This is therefore a **coverage finding about the detector, not a surviving semantics hole**: the block-identical refusal is redundant for accept/refuse but load-bearing for diagnosis. A battery that compared only accept/refuse booleans (the shape of the deciding run's counters) would let this mutant survive and would lose the distinction "the block never changed" vs "the block changed but is behaviorally equivalent". `[INFERENCE]` on the counterfactual battery shape; the measured tuples above are the ground truth.

## 6. Effect on C1 had it been undetected

**Could not have voided or falsely passed C1.** Grounded on the sealed set at tip (`analyse.py`, `analysis.exit=0`, `analysis.json`):

- All 14 sealed held-out cases scored under both counters: `heldout witness booleans differing under mutant: []`, `heldout reason strings differing under mutant: []`.
- `heldout kill+vector with block_identical: []` — no sealed case exercises the removed branch at all; the 8 kill cases are 2 head-witness and 6 vector-witness cases whose edits do change the block.
- Hence the deciding-run line would be byte-identical: `ho_kill=8/8 ho_accept=6/6 ho_invalid=0` and `C1_R33_PASS=true` are unchanged by this mutant. It neither inflates a must-kill (no case becomes witness-valid) nor voids one (no case becomes `ho_invalid`).
- Residual, latent only: if `block_run` ever became nondeterministic (a block reading time/urandom), the removed guard would be the sole backstop against admitting a head-only edit as a kill+vector witness (`a != b` could then hold by flakiness). `[INFERENCE]`; today's block is deterministic under 3 repetitions.

## 7. Restoration and containment evidence

- Scratch counter restored from the lane bytes; `restore.exit=0`, `cmp.exit=cmp_exit=0`, restored sha256 `f6b8868c...a07f28c`, then the battery re-ran green (§4). No mutant bytes remain in the scratch mirror.
- Frozen artifacts re-hashed after all runs (`frozen.sha`, `frozen.exit=0`): tool `7b11ba25...8d10`, runner `a7d3f2dd...2eb9`, counter `f6b8868c...a07f28c` — all equal their pins.
- `git -C lane status --porcelain` empty, `lane-status.exit=status_exit=0`: the clone working tree carries no changes. No git/jj write command was run anywhere; the default-mode kill rule was never invoked (only module-level `ho_witness_ok` / `block_run` / `apply_edits` / `tally_block_of` calls on scratch copies).
- Scratch evidence files: `pins.txt`, `frozen.sha`, `mut.diff`, `baseline.{stdout,json,exit}`, `mutant.{stdout,json,exit}`, `restored.{stdout,json,exit}`, `analysis.stdout`, `analysis.json`, `probe.py`, `analyse.py`, all hash/exit captures listed in §1/§2.
