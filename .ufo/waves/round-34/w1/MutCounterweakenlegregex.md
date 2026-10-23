# MutCounterweakenlegregex — C1 witness gate, X leg-assignment regex de-indented

Round 34 / wave 1 / mutation-tester seat. Lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`
(`lane_rev.txt`, `lane_rev.rc=0`). Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterweakenlegregex/`
— every write is here plus this report file. No tools installed or upgraded; no network fetch; lane
untouched (§8). The frozen default-mode kill rule was never invoked: the counter was only imported as a
module and its functions (`apply_edits`, `validate_ho`, `ho_witness_ok`, `run_tool_sandboxed`) called on
scratch copies.

## 1. Setup and pins

All commands run from the scratch root, every exit code captured with `cmd; echo $? > file`:

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/MutCounterweakenlegregex
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../MutCounterweakenlegregex/lane      # setup.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                            # setup.rc=0
git -C .../lane rev-parse HEAD -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7             # lane_rev.rc=0
git -C .../lane show <tip>:tools/tally-audit-v2.py                > tool.py            # tool_extract.rc=0
git -C .../lane show <tip>:tools/mutate-and-run.sh                 > pristine.sh       # runner_extract.rc=0
git -C .../lane show <tip>:.ufo/evidence/round-33/c1/c1-measure.py > counter_pristine.py # counter_extract.rc=0
git -C .../lane show <tip>:.ufo/evidence/round-32/c1-measure.py    > mod/round-32/c1-measure.py # v1_extract.rc=0
```

| artifact | sha256 (measured) | pin | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `.ufo/evidence/round-33/c1/c1-measure.py` (amend-6 rev) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `f6b8868c…a07f28c` | YES |

The counter copy is placed at `mod/round-33/c1/c1-measure.py` with its dependency at
`mod/round-32/c1-measure.py`, so the counter's own `HERE/../../round-32/c1-measure.py` import resolves;
import succeeds (`mechanism.rc=0`, `baseline.rc=0`).

Probe-battery bytes relied on (read-only from the lane): `witness-probes.json`
`0b2a6da5692a7e9dad98d362582ecfeeb857c2325ad6f7f75499b060ce3deca8`; sealed copy
`ho-kill-head-extra-assign.json` `9e7f9076c32e0f90a31f8c7e2929fccf4636bc68ede775d52afcaf2185895d40`;
`authoring-receipts.json` `5bec3e7927b6fd315d8a3214ce54e85afe96020a399ca2c584ade7c9cc6db798`.

## 2. The mutation (one semantic edit, one hunk)

`X = re.compile` occurs once in the counter (`grep -c 'X = re.compile'` → 1). The single hunk
(`mutant.diff`, sha256 `82fca663ab821ea93b738dcde3c3d40e18ced839e55b445575207069ce9d3a2f`,
`diff.rc=1` = differences present, `grep -c '^@@' mutant.diff` → 1):

```diff
-            X = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*=', re.M)
+            X = re.compile(r'^(st_[A-Za-z0-9_]+)[ \t]*=', re.M)
```

Effect: X no longer tolerates leading indentation, so `  st_js=0` / `  st_js=$?` inside the tally
function are invisible to it; only column-0 assignments match.

| stage | sha256 of `round-33/c1/c1-measure.py` |
|---|---|
| before (`mod/…`, lane bytes) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` |
| mutant (`mod-mut/…`) | `879b4383e3d08d7a1678f6a23cdb50b6fc615e39722613051efd991b593f35d3` |
| mutant archived (`mutant-counter.saved.py`) | `879b4383…f35d3` (`mutant.saved.sha`) |
| restored (`mod-mut/…` ← `mod/…`) | `f6b8868c…a07f28c` (`restored.sha`, `cmp.rc=0`) |

## 3. Detector: the committed 8-probe battery, rebuilt

The battery's generator was not committed (only its `json`/`stdout` verdicts), so the 8 probes are
reconstructed from the recorded labels and the amendment-6 rule (`corpus/knowledge/witness-equivalence-rule.md`)
in `probe.py` (sha256 `987908c0c4ac3ed14188e2c34001114beed10467d1142b2bf35de2dca4024efa`). Each probe's
mutated runner is rebuilt from `pristine.sh` with the counter's own `apply_edits` (same function the
measurement uses); each anchor occurs exactly once (`grep -c` → 1 for all five anchors). The pristine
counter must reproduce all 8 committed verdicts before any comparison is trusted — it does (§4).

| probe | set | witness | edits (all head, block-only for the two ride-alongs) | rebuilt runner sha256 |
|---|---|---|---|---|
| Q1-comment-accept | accept | vector `[1,2,0,0,0,0,0,0,0]` | inert head comment after `st_js=$?` | `354381cc…8ccde29` |
| Q3-inert-head-kill | kill | head | same inert head comment | `354381cc…8ccde29` |
| Q3b-ridealong-accept | accept | head | head comment + block arm `nfail+1`→`nfail+2` | `1ba21945…36cd5240` |
| K-extra-leg-assign-kill | kill | head | extra `st_js=0` after `st_js=$?` | `c8615c3e…7e7c8c5499` |
| K-nonbare-leg-kill | kill | head | `st_claims=$?` → `st_claims=0` | `bafb6e0d…6c2e6e3ebd9` |
| A-inert-head-accept | accept | head | `VERSION` string rename | `a0692e6b…ad26d8d59` |
| A-head-with-block | accept | head | `VERSION` rename + block arm edit | `8de88d76…ebb11dbf1d` |
| KV-block-identical | kill | vector `[1,0,0,0,0,0,0,0,0]` | `VERSION` rename (block byte-identical) | `a0692e6b…ad26d8d59` |

Full hashes in `runner-hashes.txt` (`runner-hashes.rc=0`); pristine runner sha
`a7d3f2dd…12eb9` is the first line there.

Run command (identical bytes for all three stages; only the counter module path changes):

```
python3 probe.py <counter.py> pristine.sh work-<stage> out-<stage>.json > <stage>.stdout 2>&1
```

## 4. Actual outputs

**Pristine counter** — `baseline.rc=0`, `out-baseline.json` sha `d3ae781dbd16d485d6d08e037ec75338d2df977f234cf81775d1f3579ebd210e`;
`compare.out` (`compare.rc=0`): `committed probes: 8`, `baseline matches committed 8/8: True`,
`baseline keys == committed keys: True`.

```
Q1-comment-accept -> (True, 'vector-equivalence')
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')
Q3b-ridealong-accept -> (False, 'head-with-block-edit')
K-extra-leg-assign-kill -> (True, 'head-leg-assignment')
K-nonbare-leg-kill -> (True, 'head-leg-assignment')
A-inert-head-accept -> (True, 'head')
A-head-with-block -> (False, 'head-with-block-edit')
KV-block-identical -> (False, 'block-identical')
```

**Mutant counter** — `mut.rc=0` (harness exit; the counter module's own predicates are what is being
observed), `out-mut.json` sha `4edaf44b993144d1665b6905a3d736f70c331c4e684583740a765af2191587f2`:

```
Q1-comment-accept -> (True, 'vector-equivalence')
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')
Q3b-ridealong-accept -> (False, 'head-with-block-edit')
K-extra-leg-assign-kill -> (False, 'head-edit-cannot-kill')   <-- flipped
K-nonbare-leg-kill -> (True, 'head-leg-assignment')
A-inert-head-accept -> (True, 'head')
A-head-with-block -> (False, 'head-with-block-edit')
KV-block-identical -> (False, 'block-identical')
```

`compare.out`: `FLIPS: 1 ['K-extra-leg-assign-kill']` —
`K-extra-leg-assign-kill: (True, 'head-leg-assignment') -> (False, 'head-edit-cannot-kill')`.

**Restored counter** — `restored.rc=0`, `out-restored.json` sha identical to baseline
`d3ae781d…bd210e`, `RESTORED matches committed 8/8: True`; restored `stdout` sha equals the baseline
`stdout` sha (`da72c2ed…dba9c5`).

## 5. Mechanism (measured, not inferred)

`mechanism.out` (`mechanism.rc=0`) extracts each module's own `X` pattern from source and applies it to
the heads of the pristine runner and of the `ho-kill-head-extra-assign` copy (runner sha
`c8615c3e…c5499`, text sha256 equal):

```
pristine-counter | X pattern = '^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*='
  X(pristine head) = 9 leg names
  X(mutated  head) = 10 entries (9 legs + a second 'st_js')
mutant-counter   | X pattern = '^(st_[A-Za-z0-9_]+)[ \t]*='
  X(pristine head) = []
  X(mutated  head) = []
  X(col0 probe "st_js=0\n")     = ['st_js']
  X(indented probe "  st_js=0\n") = []
```

The pristine `A` regex (bare `st_x=$?`) is untouched and matches all 9 indented captures in both heads.

## 6. Verdict

**KILLED — not a no-op mutant; 1/8 probe tuples flip and the flip is on the decision boolean**
(`True` → `False` for `K-extra-leg-assign-kill`). The recorded committed tuple for that probe is
`(True, 'head-leg-assignment')`; the mutant emits `(False, 'head-edit-cannot-kill')`.

Calibration detail worth recording: the weakening is **partial by construction** because the gate is an
`A or X` disjunction. The other head-surface class (`K-nonbare-leg-kill`, a removed bare capture) is still
caught by `A` and does **not** flip — measured above. X's unique contribution is exactly the
extra-assignment class (`st_js` assigned twice while still bare), and the mutant removes precisely that
contribution. So this is neither a no-op nor a silent semantics hole: it is a genuine, detected loss of one
of two redundant legs.

## 7. Effect on C1 had the mutant been undetected

**It could not have falsely passed C1; it would have voided a true PASS.**

- Measured, function-level simulation of the measurement's gate loop over the 14 sealed copies
  (`sealed_gate.py`, sha256 `6647dda30f647f46fabfd8dedbc068a5985fb8b96d7c5bea4c70755685e94717`;
  `sg-base.rc=0`, `sg-mut.rc=0`, `sg-restored.rc=0`):
  - pristine: `SEALED_GATE: ho_invalid=0 ho_kt=8 ho_at=6` — reproduces the deciding receipt's
    `ho_invalid=0` with 8/8 kill and 6/6 accept gates open
    (`.ufo/evidence/round-34/measure/c1-deciding-run.stdout`, `…exit` = 0).
  - mutant: `SEALED_GATE: ho_invalid=1 ho_kt=7 ho_at=6`; the invalidated copy is exactly
    `ho-kill-head-extra-assign` — `INVALID (witness does not demonstrate the fault)`.
  - restored: `ho_invalid=0 ho_kt=8 ho_at=6` (identical to pristine).
- `[INFERENCE]` (predicate read from `main()`, not executed — default mode is forbidden): with
  `ho_invalid=1` and `ho_kt=7`, `ok` requires `ho_invalid == 0` and `ho_kt >= 8`, so the deciding line
  would become `ho_kill=7/7 ho_accept=6/6 ho_invalid=1 … C1_R33_PASS=false` and exit 1.
- The voided copy is a **genuine must-kill**, not a defective authoring case: the frozen tool KILLs it.
  Measured via `run_tool_sandboxed` on the rebuilt copy with the pinned tool
  (`tool-observation.out`, `tool-observation.rc=0`):
  `('KILL', 1, 'TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)')`,
  matching `authoring-receipts.json` for `ho-kill-head-extra-assign`.
- Why no false PASS is possible, not just unobserved: dropping matches from X can only *remove*
  multiset differences, never create them. For a `kill+head` copy the gate accepts only when `A` or `X`
  differs; a weakened X is therefore monotone-stricter — it can only convert `VALID` to `INVALID`.
  Accept paths and vector paths do not consult X at all. So the mutant trades soundness for
  availability: it rejects a true witness, it never admits a false one.
- The landed deciding run stands unchanged. This seat's findings are observations: the battery is
  sensitive to this mutation, and the measurement layer (via `ho_invalid`) would also have caught it —
  in the fail-closed direction.

## 8. Restoration, containment, limits

- Mutant bytes archived at `mutant-counter.saved.py` (`879b4383…f35d3`); the working mutant mirror was
  restored from the pristine copy: `cmp.rc=0`, restored sha `f6b8868c…a07f28c`, and the detector re-ran
  green on restored bytes (§4, `out-restored.json` == `out-baseline.json` byte-for-byte). The pinned
  scratch primitives were re-hashed after all runs (`tool.py` `7b11ba25…8d10`, `pristine.sh`
  `a7d3f2dd…2eb9`, counter copy `f6b8868c…a07f28c`) — all equal their pins.
- `git -C lane status --porcelain` produced 0 bytes (`lane_status.rc=0`): the lane working tree is clean.
  No git/jj write command was run anywhere; the lane was read-only; all writes are under the scratch dir
  and this report.
- `main()` was never executed: both harnesses load the counter through `importlib` with module name
  `counter_under_test`, so the `__main__` guard never fires. Only the four module-level functions named in
  the tasking were called, on scratch copies.
- Limit: the probe battery's generator is not committed, so the 8 probe constructions here are a
  reconstruction whose equivalence check is the 8/8 exact baseline match against
  `dev/witness-probes.json`. Different constructions reach the same recorded tuples (corroborated by the
  sibling report `.ufo/waves/round-34/w1/MutCounterdropblockidentical.md`, which rebuilt the battery with
  different edits and also matched 8/8); the mutant comparison itself is run against identical harness
  bytes for pristine, mutant and restored stages, so the flip is attributable to the counter edit alone.
- Evidence files in the scratch root: `probe.py`, `sealed_gate.py`, `mutant.diff`, `hashes.txt`,
  `mutant.saved.sha`, `restored.sha`, `out-{baseline,mut,restored}.json`, `{baseline,mut,restored}.stdout`,
  `sg-{base,mut,restored}.stdout`, `mechanism.out`, `runner-hashes.txt`, `tool-observation.out`,
  `compare.out`, and the `*.rc` exit-code captures.
