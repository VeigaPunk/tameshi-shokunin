# MutCounterdropequivalencebytes — C1 witness gate, accept+vector `mutated != pristine` conjunct removed

Round 34 / wave 1 / mutation tester seat. Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropequivalencebytes/` (all writes there + this file).
No tool was installed or upgraded; no network fetch; the lane is byte-clean (§7).

## 1. Setup and pins

Every command ran from the scratch root with its exit code captured to a file:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropequivalencebytes
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane                    # 00-clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                  # 01-checkout.rc=0
git -C .../lane rev-parse HEAD -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7   # 02-head.rc=0, 02-head.txt
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py > tool.py           # 03-tool.rc=0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh  > pristine.sh      # 03-shell.rc=0
cp .ufo/evidence/round-33/c1/c1-measure.py counter.py                       # 05-counter.rc=0
```

`04-sha.txt` / `08-final-shas.txt`:

| artifact | sha256 | pin | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `counter.py` (round-33 c1-measure.py, amendment 6) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | same | YES |
| counter blob at measurement rev `c17e593b…` | `f6b8868c…a07f28c` (`09-rev-counter-sha.txt`) | same | YES |
| tool blob at measurement rev `c17e593b…` | `7b11ba25…8d10` (`10-rev-tool-sha.txt`) | same | YES |

The scratch mirror preserves the counter's relative import of `../../round-32/c1-measure.py`:
`tree/.ufo/evidence/round-33/c1/c1-measure.py` (pristine working copy) and
`tree/.ufo/evidence/round-33/c1/c1-measure-mut.py` (mutant), with
`tree/.ufo/evidence/round-32/c1-measure.py` (`ecb26529…faca`) beside them (`06-tree.rc=0`).

## 2. The mutation (one semantic edit)

Anchor `return a == b and mutated != pristine, 'vector-equivalence'` occurs exactly once
(`counter.py:215`). Applied to the scratch copy only:

```diff
--- counter.py
+++ tree/.ufo/evidence/round-33/c1/c1-measure-mut.py
@@ -212,7 +212,7 @@
     a = block_run(pb, vec, work)
     b = block_run(mb, vec, work)
     if ho['set'] == 'accept':
-        return a == b and mutated != pristine, 'vector-equivalence'
+        return a == b, 'vector-equivalence'
     if pb == mb:
         return False, 'block-identical'
     return a != b, 'vector'
```

`07-mutant.diff` = exactly this one hunk, one changed line; `07-mutant.diff.rc=1` (diff's
"files differ" status). The other accept/kill branches are untouched; the deciding-path guard at
`c1-measure.py:395-396` is byte-identical between the two copies (verified by the diff and by
`grep -n` on both files).

| stage | sha256 of the scratch counter |
|---|---|
| before (pristine copy) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` |
| mutated copy | `e55f73b212d8cb9952420b9452a4e67a21a5942300447329d8fa6363cf69afa2` |

The mutation was applied to a **copy**, so there is nothing to restore in place: the pristine
scratch copy and the rev blob still hash `f6b8868c…a07f28c` after every run (`08-final-shas.txt`,
`09-rev-counter-sha.txt`; `cmp counter.py tree/.../c1-measure.py` → 0).

## 3. Detector: the committed 8-probe battery, rebuilt

`.ufo/evidence/round-34/dev/witness-probes.json` records 8 probes as `name -> (bool, reason)` only
(no edits), so the runners were rebuilt from `pristine.sh` with one-anchor edits — every anchor is
asserted `count == 1` by `apply_edits` (it raises otherwise), and the reconstruction is validated
by reproducing all 8 recorded tuples exactly (§4). Vector witnesses are all-zero `[0]*9`.

| probe | set | witness | runner edit(s) |
|---|---|---|---|
| Q1-comment-accept | accept | vector | `# Q1 cosmetic comment` inserted between the tally `local` line and `for st in` |
| Q3-inert-head-kill | kill | head | `# Q3 inert head comment` inserted after `st_citecheck=$?` (head only) |
| Q3b-ridealong-accept | accept | head | same head comment + block `0) npass=$((npass + 1)) ;;` → `+ 2` |
| K-extra-leg-assign-kill | kill | head | extra `  st_js=$?` line after `st_citecheck=$?` |
| K-nonbare-leg-kill | kill | head | `  st_js=$?` → `  st_js=$?;` (leg assign no longer bare) |
| A-inert-head-accept | accept | head | Q3 bytes (head comment) |
| A-head-with-block | accept | head | Q3 head comment + Q1 block comment |
| KV-block-identical | kill | vector | K-extra head edit only, so the block is byte-identical |

Harness `probe.py` (sha256 `efee5c27…740e`) imports the pinned counter and the mutant as modules
(`importlib`), calls `ho_witness_ok` on both for each probe, and monkey-patches `block_run` to
record the actual `(rc, first-line)` pair of every witness run. No default-mode invocation.

## 4. Actual outputs

`python3 probe.py` → `probe.exit=0`, `probe.stdout` (sha256 `25fc8fc7…fbee`):

```
Q1-comment-accept          pristine=(True, 'vector-equivalence')   mutant=(True, 'vector-equivalence')   expected=(True, 'vector-equivalence')   match=True flip=False
Q3-inert-head-kill         pristine=(False, 'head-edit-cannot-kill') mutant=(False, 'head-edit-cannot-kill') expected=(False, 'head-edit-cannot-kill') match=True flip=False
Q3b-ridealong-accept       pristine=(False, 'head-with-block-edit') mutant=(False, 'head-with-block-edit') expected=(False, 'head-with-block-edit') match=True flip=False
K-extra-leg-assign-kill    pristine=(True, 'head-leg-assignment')  mutant=(True, 'head-leg-assignment')  expected=(True, 'head-leg-assignment')  match=True flip=False
K-nonbare-leg-kill         pristine=(True, 'head-leg-assignment')  mutant=(True, 'head-leg-assignment')  expected=(True, 'head-leg-assignment')  match=True flip=False
A-inert-head-accept        pristine=(True, 'head')                 mutant=(True, 'head')                 expected=(True, 'head')                 match=True flip=False
A-head-with-block          pristine=(False, 'head-with-block-edit') mutant=(False, 'head-with-block-edit') expected=(False, 'head-with-block-edit') match=True flip=False
KV-block-identical         pristine=(False, 'block-identical')     mutant=(False, 'block-identical')     expected=(False, 'block-identical')     match=True flip=False
BATTERY: probes=8 expected_mismatch=0 verdict_flips=0
```

Block-run evidence for the two probes that reach the mutated branch (`probe.stdout`, `probe-results.json`):

- Q1: both block runs returned `(0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')`, `same_bytes=False`.
- KV: both runs identical (same PASS line), `same_bytes=False`; the refusal comes from `pb == mb`.
- `VERSION in head: True`, `st_js line count: 1` — the rebuilt runner carries the expected head/leg surface and matches the battery's own diagnostic lines (`dev/witness-probes.stdout`).

**0/8 probes flip.** The mutant must therefore be classified.

### 4a. Why zero flips is structural, and the probe that does kill it

`mutated != pristine` can only change the accept+vector return when `a == b` **and**
`mutated == pristine`. All 8 rebuilt probes change bytes (`same_bytes=False` on every one,
`probe.stdout`), so the second conjunct is trivially true on all of them: the battery never
exercises the operand it is supposed to test.

A ninth, deliberately discriminating probe `D9-nodiff-accept` (accept + vector, edit is a
self-substitution `REGRESSION_BAND: ledger legs exact` → itself; anchor count 1, `apply_edits`
accepts it) distinguishes the versions (`probe.stdout`):

```
DISCRIMINATOR D9-nodiff-accept pristine=(False, 'vector-equivalence') mutant=(True, 'vector-equivalence') same_bytes=True
```

So the mutation is **semantically observable** (the conjunct is load-bearing for a zero-diff
accept witness) but **undetectable by the committed 8-probe battery** — a coverage gap in the
detector, not a defect in the counter's contract.

(Bookkeeping: the first D9 anchor, `#!/usr/bin/env bash`, was rejected because it occurs 7 times in
the runner's embedded fixtures — `anchor-counts.rc=0`; replaced with a count-1 anchor.)

## 5. Verdict

**SURVIVED — 0/8 committed probes flip; the mutant is a no-op mutant with respect to C1's deciding procedure.**

Two facts, both measured or read off the frozen bytes:

1. **Deciding-path reachability.** The only call site of `ho_witness_ok` is
   `c1-measure.py:397`, immediately after the guard at `:395-396`
   (`if mutated == pristine: raise CounterError('edits do not change the runner')`), which turns a
   zero-diff case into `ho_invalid += 1` at `:399-400` before the witness gate can run. The guard is
   outside the mutated line and byte-identical in both copies. Hence on every input `main()` can
   produce, `mutated != pristine` is `True`, and the two versions of `ho_witness_ok` agree.
2. **Sealed-set replay.** `heldout_diff.py` (sha256 `ba0dc31…6375`, `heldout.exit=0`,
   `heldout.stdout`, `heldout-diff.json` sha256 `353ae2c9…9ae0`) re-executes `main()`'s admission
   loop (`validate_ho` → `apply_edits` → guard → `ho_witness_ok`) for the 14 sealed held-out copies
   at the measurement rev `c17e593b…`, under both counters:

```
pristine: ho_kill=8 ho_accept=6 ho_invalid=0
mutant:   ho_kill=8 ho_accept=6 ho_invalid=0
DIFFERENTIAL: ho_kill 8/8, ho_accept 6/6, ho_invalid 0/0, decisions_identical=True
```

Per-copy `admitted`, `reason` (`head`, `head-leg-assignment`, `vector`, `vector-equivalence`) and
`mutated_sha` are identical in both columns; the aggregates match the landed receipt
(`ho_kill=8/8 ho_accept=6/6 ho_invalid=0`, `.ufo/evidence/round-34/measure/c1-deciding-run.stdout`).

**Classification:** no-op mutant (for C1) **plus** a surviving-semantics coverage hole of the
8-probe battery (for the standalone `ho_witness_ok` contract). It is not a hole in the counter's
deciding-path semantics; it is a hole in the detector's ability to see this edit.

## 6. Could this mutant, if undetected, have voided or falsely passed C1?

**It could not have falsely passed C1, and inside C1's deciding procedure it could not even void it.**

- Falsely pass: no. The only behaviour the mutation changes is admitting a zero-diff accept
  witness. `main()` rejects `mutated == pristine` at `c1-measure.py:395-396` before calling the
  gate, increments `ho_invalid`, and `ho_invalid == 0` is a conjunct of `ok` (`:424-427`). A
  zero-diff accept copy therefore makes C1 **fail**, never pass, under either counter version
  (demonstrated: D9 is `(True, …)` for the mutant's gate but is still refused by the caller's
  guard — the guard is identical in both files, `07-mutant.diff`).
- Void: only outside the deciding procedure. (a) A mutated counter committed **without**
  re-minting the controls receipt would hash `e55f73b2…` ≠ `controls-receipt.json`'s
  `counter_sha256 = f6b8868c…` and set `controls_ok=0` (`:367-368`), voiding the run — this is the
  receipt's sha linkage, not the mutation's semantics. (b) Re-minting is possible (`--write-controls`
  at `:298`, which scores control tools on the public panel and never calls `ho_witness_ok`), but
  after re-minting the sealed-set replay above shows identical admissions, so the measured line
  would be unchanged.
- The real exposure is authoring-time: if the **mutated** gate were used to vet a held-out set, it
  would bless a zero-diff accept copy, which the deciding run then counts `ho_invalid=1` →
  `C1_R33_PASS=false`. That is a void, again not a false pass.

Residual latent risk `[INFERENCE]`: removal of the caller guard in a future counter (or any new
caller of `ho_witness_ok` that skips it) would turn this conjunct into the sole backstop against
zero-diff "accept" fixtures; the 8-probe battery would not notice.

## 7. Restoration and containment evidence

- The lane clone was never written: `git -C lane status --porcelain` → `11-lane-status.txt`
  (0 bytes). No git/jj write command ran anywhere.
- The frozen artifacts re-hash to their pins after all runs (`08-final-shas.txt`): tool
  `7b11ba25…8d10`, runner `a7d3f2dd…2eb9`, counter `f6b8868c…a07f28c`; the counter blob at
  `c17e593b…` is `f6b8868c…a07f28c` (`09-rev-counter-sha.txt`).
- The mutation lives only in `tree/.ufo/evidence/round-33/c1/c1-measure-mut.py` (`e55f73b2…a2`);
  the pristine scratch copy is byte-identical to the pin (`cmp` exit 0, §2), so no restore was
  needed.
- The default-mode kill rule was never invoked: only imported functions (`validate_ho`,
  `apply_edits`, `ho_witness_ok`, `block_run`, `list_tree`, `show`) were called on scratch copies;
  `block_run` itself ran under the frozen bwrap boundary.
- Scratch evidence: `probe.py`, `probe.stdout`, `probe-results.json`, `heldout_diff.py`,
  `heldout.stdout`, `heldout-diff.json`, `07-mutant.diff`, `03-…`/`05-…` hashes and the `*.rc`
  exit captures listed in §1.
