# MutCounterdropsetbranch — C1 witness gate, accept+vector equivalence flip removed

Round 34 / wave 1 (v2, build+attack) / mutation tester seat. Claim under attack: **C1** (operability
capability acquisition, `tools/tally-audit-v2.py`), measured TRUE at revision
`c17e593b51802dd4ed568da3265f21c6d00c4273`. Lane tip at dispatch:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropsetbranch/` (all writes here + this file).
No tools installed or upgraded; no pacman; lane untouched (see §8).

**Verdict: KILLED.** The mutant flips `Q1-comment-accept` from `(True, 'vector-equivalence')` to
`(False, 'vector')` (**1/8 probe verdicts changed**, `BASELINE_EXACT 7/8`), and, independently, the
committed sealed set drops from `ho_accept=6/6, ho_invalid=0` to `ho_accept=2/6, ho_invalid=4`.
Undetected, this mutant **would have voided C1** (false negative), never falsely passed it (§7).

## 1. Setup and pins

Commands (scratch root; every exit code captured to a file, never `&&`):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropsetbranch                    # mkdir.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../MutCounterdropsetbranch/lane          # clone.exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                                # checkout.exit=0
git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7               # head.txt
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py  > tool.py                        # tool_extract.exit=0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh   > pristine.sh                    # pristine_extract.exit=0
```

| artifact | sha256 observed | pin | match |
|---|---|---|---|
| `tool.py` (`tools/tally-audit-v2.py`) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (`tools/mutate-and-run.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| counter `.ufo/evidence/round-33/c1/c1-measure.py` (at lane tip) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amend-6 pin `f6b8868c…a07f28c` | YES |
| v1 import `.ufo/evidence/round-32/c1-measure.py` (at lane tip) | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | — | — |

The counter is loaded from a mirrored scratch tree so its `../../round-32/c1-measure.py` import path
stays intact — `pris/.ufo/evidence/round-33/c1/` + `pris/.ufo/evidence/round-32/`, likewise `mut/`
and `rest/` (copies `cp_pris.exit=0`, `cp_pris_v1.exit=0`, `cp_mut_v1.exit=0`, `cp_mut.exit=0`,
`rest_cp.exit=0`, `rest_v1.exit=0`).

## 2. The mutation (one semantic edit)

Removed the accept+vector equivalence flip in `ho_witness_ok` (pristine counter lines 214–215; anchor
count == 1 enforced by `probes.py`'s exact-uniqueness `replace`):

```diff
--- pris/.ufo/evidence/round-33/c1/c1-measure.py
+++ mut/.ufo/evidence/round-33/c1/c1-measure.py
@@ -211,8 +211,6 @@
     a = block_run(pb, vec, work)
     b = block_run(mb, vec, work)
-    if ho['set'] == 'accept':
-        return a == b and mutated != pristine, 'vector-equivalence'
     if pb == mb:
         return False, 'block-identical'
     return a != b, 'vector'
```

`mutant.diff` sha256 `b0f8659228f6f24c78bf147dd6e4a11a952db12865f101e8698c19f9777363ac`
(`mutant.diff.exit=1` = differences present; exactly this one hunk). No other byte differs.

| stage | sha256 of `mut/.ufo/evidence/round-33/c1/c1-measure.py` |
|---|---|
| before | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` (`mut.sha.before`) |
| mutated | `17750058aa0e9734036677368dfbf3e4158530e622367c1cf58b582acf7d9868` (`mut.sha.after`) |
| restored | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`; `cmp` vs pristine exit `cmp_restored.exit=0` |

The mutant bytes are preserved as `mutant-counter.py` (sha256 `17750058…f7d9868`,
`preserve_mutant.exit=0`) before the `mut/` path was restored (`restore_mut.exit=0`).

## 3. Detector: the committed 8-probe battery, rebuilt from `pristine.sh`

`probes.py` (sha256 `1be20427fd4acdfcf0e2d9d44cec5132f2bfcee0703b9318f9c3d3862ae68316`) imports the
counter under test as a module (`block_run`, `ho_witness_ok`, `validate_ho`, `apply_edits`), applies
one-anchor edits to `pristine.sh` (each anchor asserted count == 1), and runs the gate.

Fixture provenance: the L1 did not persist its probe builder, so the 8 runners are **reconstructed**
from the probe names and the recorded tuples in
`.ufo/evidence/round-34/dev/witness-probes.json` (copied to `stored/witness-probes.json`, sha256
`0b2a6da5692a7e9dad98d362582ecfeeb857c2325ad6f7f75499b060ce3deca8`; recorded stdout
`stored/witness-probes.stdout` sha256 `b82a57bc1ab2cb9247b765f00fc482129bca69167c78f1eb7c51c3965415bec9`).
The reconstruction is accepted as the same probes because, run through the pristine counter bytes, it
reproduces the stored oracle **8/8 exact** including the reason strings (§4) — a different fixture
would not.

Runner geometry (same `tally_block_of`/`head_of` boundary the gate uses): head 73739 bytes, tally
block 1562 bytes (`head_counts.exit=0`). Head leg-capture multisets under the gate's own regexes:
pristine A = 9 bare `st_x=$?`, X = 9 `st_*=` assignments.

| probe | set | witness | runner edit (from pristine `pristine.sh`) | stored expectation |
|---|---|---|---|---|
| `Q1-comment-accept` | accept | vector `[0,1,0,2,0,0,0,0,0]` | insert `    # decoy comment` before `    case $st in` (block bytes change, behavior identical) | `(True, 'vector-equivalence')` |
| `Q3-inert-head-kill` | kill | kind=head | insert `  # inert comment` after `  st_citecheck=$?` (A/X unchanged) | `(False, 'head-edit-cannot-kill')` |
| `Q3b-ridealong-accept` | accept | kind=head | inert head comment + lethal ride-along `      1) nfail=$((nfail + 1)) ;;` → `((nfail + 0))` | `(False, 'head-with-block-edit')` |
| `K-extra-leg-assign-kill` | kill | kind=head | duplicate `  st_js=$?` (A 9→10, X 9→10) | `(True, 'head-leg-assignment')` |
| `K-nonbare-leg-kill` | kill | kind=head | `  st_js=$?` → `  st_js=${?}` (A 9→8, X 9→9) | `(True, 'head-leg-assignment')` |
| `A-inert-head-accept` | accept | kind=head | inert head comment | `(True, 'head')` |
| `A-head-with-block` | accept | kind=head | inert head comment + `npass=$((npass + 1))` → `npass=$(( npass + 1 ))` | `(False, 'head-with-block-edit')` |
| `KV-block-identical` | kill | vector `[0,1,0,2,0,0,0,0,0]` | inert head comment only (tally block byte-identical) | `(False, 'block-identical')` |

## 4. Results — pristine, mutant, restored (identical detector, identical bytes)

Commands (exit codes captured):

```
python3 probes.py pris/.ufo/evidence/round-33/c1/c1-measure.py pristine  > pristine-probes.out  2> pristine-probes.err   # pristine-probes.exit=0
python3 probes.py mut/.ufo/evidence/round-33/c1/c1-measure.py  mutant    > mutant-probes.out    2> mutant-probes.err     # mutant-probes.exit=0
python3 probes.py rest/.ufo/evidence/round-33/c1/c1-measure.py restored  > restored-probes.out  2> restored-probes.err   # restored-probes.exit=0
```

| probe | pristine `f6b8868c` | mutant `17750058` | restored `f6b8868c` | flip? |
|---|---|---|---|---|
| `Q1-comment-accept` | `(True, 'vector-equivalence')` | **`(False, 'vector')`** | `(True, 'vector-equivalence')` | **YES** |
| `Q3-inert-head-kill` | `(False, 'head-edit-cannot-kill')` | `(False, 'head-edit-cannot-kill')` | same | no |
| `Q3b-ridealong-accept` | `(False, 'head-with-block-edit')` | `(False, 'head-with-block-edit')` | same | no |
| `K-extra-leg-assign-kill` | `(True, 'head-leg-assignment')` | `(True, 'head-leg-assignment')` | same | no |
| `K-nonbare-leg-kill` | `(True, 'head-leg-assignment')` | `(True, 'head-leg-assignment')` | same | no |
| `A-inert-head-accept` | `(True, 'head')` | `(True, 'head')` | same | no |
| `A-head-with-block` | `(False, 'head-with-block-edit')` | `(False, 'head-with-block-edit')` | same | no |
| `KV-block-identical` | `(False, 'block-identical')` | `(False, 'block-identical')` | same | no |

- pristine: `BASELINE_EXACT: 8/8` (`pristine-probes.out:11`) — the rebuilt battery equals the stored oracle.
- mutant: `MISMATCH Q1-comment-accept stored=(True, 'vector-equivalence') got=(False, 'vector')`
  (`mutant-probes.out:11`), `BASELINE_EXACT: 7/8` (`mutant-probes.out:12`) → **one probe verdict flipped**.
- restored: `BASELINE_EXACT: 8/8` (`restored-probes.out:11`), byte-identical results JSON (§8).

Behavioral grounding of the flip (same `block_run`, vector `[0,1,0,2,0,0,0,0,0]`, `vector_tuples.exit=0`):

```
pristine a= (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
         b= (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')   a==b True  pb==mb False
pristine gate= (True, 'vector-equivalence')
mutant   a= (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
         b= (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')   a==b True  pb==mb False
mutant   gate= (False, 'vector')
```

The clone is behaviorally identical (`a == b`); the mutant demands `a != b` and therefore refuses a
witness the pristine gate validates.

## 5. Independent second detector: the committed sealed set

Same module load, `validate_ho` + `apply_edits` + `ho_witness_ok` over the 14 committed copies in
`.ufo/evidence/round-33/heldout/` (read from the scratch clone, read-only):

| counter bytes | `ho_kill` valid | `ho_accept` valid | `ho_invalid` |
|---|---|---|---|
| pristine `f6b8868c` | 8/8 | 6/6 | 0 |
| mutant `17750058` | 8/8 | **2/6** | **4** |
| restored `f6b8868c` | 8/8 | 6/6 | 0 |

Mutant-invalid copies (all `why=vector`, full list in `results-mutant.json`):
`ho-accept-vector-arith-space`, `ho-accept-vector-block-comment`, `ho-accept-vector-inert-line`,
`ho-accept-vector-tail-comment`. The 2 accept+head copies and all 8 kill copies stay valid — the
mutation touches exactly the accept+vector surface.

## 6. Verdict

**KILLED** — not survived, not inconclusive.

- Probe battery: 1 of 8 verdicts flipped (`Q1-comment-accept`), so this is not a no-op mutant.
- Sealed set: 4 of 6 must-accept copies become invalid, so the sealed-set gate is a second,
  independent detector of the same defect.

## 7. Could the mutant have voided or falsely passed C1, if undetected?

**It would have voided C1, never falsely passed it.**

Mechanics in the frozen counter (`.ufo/evidence/round-33/c1/c1-measure.py` at `f6b8868c`):

- line 397–400: a copy whose `ho_witness_ok` is false raises `CounterError`, increments `ho_invalid`,
  and the copy is dropped before any tool scoring;
- lines 424–427: `ok = (… and ho_invalid == 0 and ho_kt >= 8 and ho_at >= 6 and …)`;
- line 434: `return 0 if ok else 1`, i.e. `C1_R33_PASS=false`, exit 1, when `ok` is false.

With the observed mutant tallies the deciding line would have read `ho_kill=8/8 ho_accept=2/2
ho_invalid=4`: `ho_invalid == 0` is false and `ho_at >= 6` is false → `ok` false → **PASS=false,
exit 1**. The 4 affected copies are accepted by the tool (authoring receipts
`.ufo/evidence/round-34/dev/authoring-receipts.json` rows `ho-accept-vector-*`: `tool=["ACCEPT",0,…
TALLY_AUDIT: PASS…]`; deciding receipt `ho_accept=6/6`), so the void is pure witness-gate false
negativism — a blameless tool plus a valid sealed set rejected as invalid.

It cannot falsely pass: the deleted hunk is the only behavioral change (`mutant.diff`), it governs
only `ho['set'] == 'accept'` with a vector witness, and it can only (a) refuse block-equivalent
accept clones (`a == b`, `pb != mb`) and (b) refuse accept+vector copies with an identical block,
which the mutant now routes into `block-identical`. Kill+vector (`a != b`), kill+head and accept+head
paths are byte-identical to pristine, so no kill copy becomes valid and no accept copy becomes
scorable that was not already. This is exactly the round-33 hazard class recorded in
`corpus/knowledge/witness-equivalence-rule.md` §"Why the set-blind predecessor was voidable", third
bullet: a cosmetic clone carrying no valid witness "voided the whole claim".

The landed deciding run stands: it scored counter bytes `f6b8868c…` at `c17e593b`
(`.ufo/evidence/round-34/measure/`, `ho_accept=6/6 ho_invalid=0 C1_R33_PASS=true`, exit 0). This seat
only shows the committed battery and sealed set would have caught the defect had it been present.

## 8. Restoration and read-only evidence

- Lane tip unchanged: `git -C lane rev-parse HEAD` → `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`;
  `git -C lane status --porcelain | wc -l` → `0` (scratch clone; no writes to the real lane).
- After every run: `pristine.sh` = `a7d3f2dd…2eb9`, `tool.py` = `7b11ba25…8d10`,
  `lane/.ufo/evidence/round-33/c1/c1-measure.py` = `f6b8868c…a07f28c` (pins intact).
- Counter under test restored: `mut/…/c1-measure.py` = `f6b8868c…a07f28c`, `cmp` vs pristine exit
  `cmp_restored.exit=0`; mutant bytes retained separately at `mutant-counter.py` (`17750058…`).
- Restored-bytes detector run: exit 0, `BASELINE_EXACT 8/8`, `HELDOUT_TALLY ho_kill=8 ho_accept=6
  ho_invalid=0`; `results-restored.json` sha256
  `546dedd43c0d2eba57d4207a25a1c5c9c265aa26b8f09f768535409e89e87c5a` is byte-identical to
  `results-pristine.json` (same sha256); `results-mutant.json` sha256
  `0654da23c03e4f3cf8c2adefacc28054a72811ef0300c68d3915dd795352493f`.
- Writes: scratch dir + this report only. No git/jj write commands outside the scratch clone; no
  pacman; no tool installs; no network fetch.

## 9. Reproduce (scratch root = `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropsetbranch`)

```
mkdir -p . && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin lane; echo $? > clone.exit
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo $? > checkout.exit
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh
mkdir -p pris/.ufo/evidence/round-33/c1 pris/.ufo/evidence/round-32 mut/.ufo/evidence/round-33/c1 mut/.ufo/evidence/round-32
cp lane/.ufo/evidence/round-33/c1/c1-measure.py pris/.ufo/evidence/round-33/c1/c1-measure.py
cp lane/.ufo/evidence/round-32/c1-measure.py          pris/.ufo/evidence/round-32/c1-measure.py
cp lane/.ufo/evidence/round-32/c1-measure.py          mut/.ufo/evidence/round-32/c1-measure.py
cp pris/.ufo/evidence/round-33/c1/c1-measure.py       mut/.ufo/evidence/round-33/c1/c1-measure.py
# apply the 2-line deletion from §2 (exact anchors; my probes.py also asserts count==1)
python3 probes.py pris/.ufo/evidence/round-33/c1/c1-measure.py pristine; echo $? > pristine-probes.exit
python3 probes.py mut/.ufo/evidence/round-33/c1/c1-measure.py  mutant;   echo $? > mutant-probes.exit
cp pris/.ufo/evidence/round-33/c1/c1-measure.py mut/.ufo/evidence/round-33/c1/c1-measure.py
python3 probes.py mut/.ufo/evidence/round-33/c1/c1-measure.py  restored; echo $? > restored-probes.exit
```

`probes.py` flags and expected outputs: `BASELINE_EXACT 8/8` + `HELDOUT_TALLY ho_kill=8 ho_accept=6
ho_invalid=0` for pristine/restored; `MISMATCH Q1-comment-accept … got=(False, 'vector')`,
`BASELINE_EXACT 7/8`, `HELDOUT_TALLY ho_kill=8 ho_accept=2 ho_invalid=4` for the mutant.
