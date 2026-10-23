# Mutkillvectorcountfieldswap — round-34 w1 mutation probe

Seat: mutation-tester (leaf, no dispatch). Claim under attack: C1 (operability capability
acquisition, `tools/tally-audit-v2.py`) MEASURED TRUE at revision
`c17e593b51802dd4ed568da3265f21c6d00c4273`; deciding receipt
`.ufo/evidence/round-34/measure/` → `ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true`,
exit 0. Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

Scratch root (every write except this report):
`/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorcountfieldswap/`.
Kill rule consumed: the counter CLI was **never** run in default mode. The counter was imported as a
module from the lane path and only its functions (`validate_ho`, `apply_edits`, `tally_block_of`,
`block_run`, `ho_witness_ok`, `run_tool_sandboxed`, `bwrap_argv`) were called on scratch copies.
No git/jj write command was run; the lane clone's `git status --porcelain` is empty and its HEAD is
still the tip.

## 1. Setup and pin verification (before any run)

```console
$ mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorcountfieldswap && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorcountfieldswap/lane; echo $? > clone.rc
$ cat clone.rc
0
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo $? > checkout.rc
$ cat checkout.rc
0
$ git -C lane rev-parse HEAD
0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
$ git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py; echo $? > tool.rc
$ git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh; echo $? > pristine.rc
$ cat tool.rc pristine.rc
0
0
$ sha256sum tool.py pristine.sh
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
$ git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum
f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c  -
$ git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:.ufo/evidence/round-33/heldout/ho-kill-vector-count-field-swap.json | sha256sum
566faacfe3552350f1e38718e261d013b1e5b019265fb50eea178762473d2bd6  -
$ sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/heldout/ho-kill-vector-count-field-swap.json
566faacfe3552350f1e38718e261d013b1e5b019265fb50eea178762473d2bd6  …
```

The tool, runner and counter shas match the frozen pins exactly; the sealed copy's working-tree bytes
equal the blob at the tip. `bwrap` 0.13.1 and Python 3.14.8 were used.

Detector (identical for pristine, mutated and restored bytes): the frozen counter's
`run_tool_sandboxed` (`lane/.ufo/evidence/round-33/c1/c1-measure.py:234-263`) — real
`python3 -I /w/tool.py --runner /w/copy.sh` under `bwrap --unshare-all` with `timeout` outside the
sandbox — classifying `KILL` iff `rc==1` and the last `TALLY_AUDIT:` line starts `FAIL`, `ACCEPT`
iff `rc==0` and it starts `PASS`. A supplementary re-invocation under the identical `bwrap` argv
(`counter.bwrap_argv`) captures the full `CHECK` lines; the classification always comes from
`run_tool_sandboxed`. Tool bytes in every run were
`7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`.

Driver: `probe.py` (sha256 `f48f7e076859e7141983e9d4b2ba57fd7343555e5fcc6816a723af906dfd15b7`),
modes `baseline`, `assigned`, `adversarial`, `accept-opposition`, `decoyshape`, `detail`,
`oracle-proof`; every mode exited 0 (`baseline.rc assigned.rc adversarial.rc accept-opposition.rc
decoyshape.rc oracle-proof.rc` all `0`).

## 2. Assigned copy: mutation, witness, verdict

The JSON's single edit, applied by the counter's own `apply_edits` (the old string occurs exactly
once in the tip bytes — asserted by the counter, measured `count: 1` at `pristine.sh:1443`):

```
-old  '      "$nlegs" "$npass" "$nfail" "$nsetup"\n'
+new  '      "$nlegs" "$nfail" "$npass" "$nsetup"\n'
```

Mutant `mutant-assigned.sh`, sha256
`38cdf560ae112929aa7e096d637baa66a6b117b2c97614ed09164d5ae2987d5b`, bytes delta 0 (an in-place
argument swap in the FAIL branch's `printf`). Witness gate — `ho_witness_ok` on the declared vector
`[1,0,0,0,0,0,0,0,0]`: **(True, 'vector')**, with

```
a (pristine block) = (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
b (mutant block)   = (1, 'REGRESSION: FAIL (cases=9 passed=1 failed=8 setup=0)')
```

Same detector, three byte states:

| bytes | sha256 | outcome | rc | last line |
|---|---|---|---|---|
| pristine `pristine.sh` (baseline, `baseline.out`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| sealed mutant (`assigned.out`) | `38cdf560ae112929aa7e096d637baa66a6b117b2c97614ed09164d5ae2987d5b` | **KILL** | **1** | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| restored = pristine bytes (`assigned.out` restore probe) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |

The kill lands on the intended surface (`detail-assigned.out`, identical argv/env to
`run_tool_sandboxed`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime FAIL vectors=15158 mismatched=1786; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0: got (1, 'REGRESSION: FAIL (cases=9 passed=1 failed=8 setup=0)'), want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
```

**Verdict for the assigned copy: KILLED, as its label demands** (rc 1, `TALLY_AUDIT: FAIL`, 1786
runtime mismatches). The deciding receipt's `ho_kill=8/8` is consistent with this copy.

Corroboration that the copy is a genuine defect, not a detector artefact: the mutant fails its own
runner harness — `bash mutant-assigned.sh --selftest` → rc **1**, `MUTATE_SELFTEST: 103/106 pass`,
`VERDICT: FAIL`, with exactly the three FAIL-line cases failing (`one leg status 1 at each of 9
positions` 0/9, `statuses 1 1 …`, `statuses 1 2 …`, `selftest-mutant.log`); the pristine runner is
rc 0, `MUTATE_SELFTEST: 106/106 pass`, `VERDICT: PASS` (`selftest-pristine.log`). The harness keeps
its scratch on FAIL; that directory (`/tmp/tameshi-r4-2-selftest.uHJPZI`) was removed.

Restoration: `pristine.sh` is byte-unchanged (`a7d3f2dd…` before and after — `assigned.out`
`restore-evidence`, plus the fleet copy's sha above), `tool.py` is `7b11ba25…`, the lane
`git status --porcelain` is empty and HEAD is still `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Nothing in the fleet tree or lane was written.

## 3. Adversarial: does a witness-valid, tool-opposite construction exist?

### 3.1 Live tally-block count-field swaps: none can survive — proof + measurement

For any argument permutation inside the three reachable `printf` calls of the live tally block, the
block's `(rc, first stdout line)` is a function of `(nlegs, p, f, s)` only. The tool's runtime oracle
executes the block against **every** count triple reachable from nine statuses: `count_vectors(9)`
enumerates all 55 `(failing, setup)` pairs with `f+s<=9` (`tool.py:362-370`), and `check_runtime`
compares the exact first line and exit code against `oracle` under both configs
(`tool.py:290-302`, `tool.py:372-438`, 15158 runs incl. operand stress). Therefore:

> if a mutant's first line differs from pristine for **any** status vector, it differs for some
> count triple in that sweep, and the tool's runtime check fails; and
> if the tool ACCEPTs, `block_run(pristine) == block_run(mutant)` at the witness vector, so a
> `kill`+`vector` witness returns False. The two instruments cannot disagree in the kill direction
> for a live-block swap.

Measured (`oracle-proof.out`): across the FAIL (4 args) and SETUP (3 args) printfs there are 28
non-identity permutations; **28/28** have a count triple whose line differs from the oracle, and
**0** are runtime identities (`{"permutations": 28, "permutations_with_count_triple_diff": 28,
"permutations_that_are_runtime_identity": 0, "identity_perms": []}`). Confirmations on real bytes:

| variant | construction | witness | tool outcome |
|---|---|---|---|
| V1 = assigned (`38cdf560…`) | FAIL: `npass`↔`nfail` | True `vector` | KILL rc=1, 1786 mismatches |
| V2 `v2-fail-setup-swap.sh` (`1880ce84333e581ac2764d5fce15b71bf1c8f68138be5e6c4081d3138815f460`) | FAIL: `nfail`↔`nsetup` (the tool's own panel shape, `tool.py:521-523`) | True `vector` | KILL rc=1, runtime fail |
| V3 `v3-setup-pass-swap.sh` (`db273a37d4c9d4a6d6e5f72c7979c17d3584489ee09a10dc7e3d99403ed450ce`) | SETUP: `npass`↔`nsetup` | True `vector` | KILL rc=1, runtime fail |
| V4 `v4-pass-count-swap.sh` (`502ed773d66f18b77949caa000518fbefede5b90a4cab19a63b188dcdb02bca4`) | PASS: `nlegs`↔`npass` | **False `vector`** (`a == b`, inert: PASS implies `p == nlegs`) | ACCEPT rc=0 |

So for live-block count-field swaps the witness gate and the tool agree, and **no kill-labelled
survivor exists**. The interesting constructions are structural, and they do exist.

### 3.2 Finding A (critical): count-field swap in a dead decoy block — witness VALID, real tool ACCEPTs

The counter's witness block lookup is **file-wide**: `tally_block_of` takes the *first*
`  local nlegs=9 …` anywhere in the file (`c1-measure.py:140-145`, used by `ho_witness_ok` at
`c1-measure.py:184-191`). The tool's block lookup is **scoped to `run_regression()`**
(`tool.py:117-128`, `tool.py:149-156`). A copy that plants the identical swapped block as a decoy
function *before* `run_regression`, leaving the live tally block untouched, is witness-valid and
tool-accepted. Exact JSON (`v6-decoy-swap.json`, sha256
`92f6d78da55cad69cddb63f9e616761b2b79b01eaa41d1f6dd203eb3ffba5005`; mutant bytes
`v6-decoy-swap.sh`, sha256 `2f12cd5f61ea83752945668b7aa58dff42bd245a62c461d3ce225ea747474c2d`):

```json
{
 "author": "probe",
 "edits": [
  {
   "new": "tally_decoy() {\n  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do\n    case $st in\n      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n    esac\n  done\n\n  if [[ $nfail -gt 0 ]]; then\n    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\\n' \\\n      \"$nlegs\" \"$nfail\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 1\n  fi\n  if [[ $nsetup -gt 0 ]]; then\n    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\\n' \\\n      \"$nlegs\" \"$npass\" \"$nsetup\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the\n  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals\n  # of a mutation report are sums of its per-state counts).\n  if (( npass + nfail + nsetup != nlegs )); then\n    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n    exit 2\n  fi\n  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n    \"$nlegs\" \"$npass\"\n  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then\n    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\\n' \"$root\"\n    rm -rf \"$root\"\n  else\n    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n  fi\n  exit 0\n}\n\nrun_regression() {\n",
   "old": "run_regression() {\n"
  }
 ],
 "id": "v6-decoy-swap",
 "set": "kill",
 "witness": {
  "vector": [
   1,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 }
}
```

Observed (`adversarial.out`, `witness-pairs.out`, `decoyshape.out`, `detail-decoy.out`):

- `validate_ho` clean; `apply_edits` old-count 1; bytes changed.
- Witness: **(True, 'vector')** — `a = (1, '… passed=8 failed=1 …')`,
  `b = (1, '… passed=1 failed=8 …')` — the counter reads the **decoy** block.
- Shape: counter's first `local nlegs=` is at offset 68441 in the mutant (the decoy, *not* inside
  `run_regression`) vs 73739 in pristine; `counter_block_is_run_regression_mutant: false`; the
  tool's live block is byte-identical between pristine and mutant (`tool_live_block_identical:
  true`); the swapped line occurs once (decoy) and the pristine line once (the live block).
- Real tool: **ACCEPT, rc 0**, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass
  harness=pass)`, `CHECK runtime PASS vectors=15158 mismatched=0`.

**Impact.** The tool's ACCEPT is semantically correct: the executed runner is pristine-equivalent.
The witness gate is wrong. Were this copy sealed as `must-kill`, the counter would count it into
`ho_kt` (`c1-measure.py:403`) and the tool would not kill it (`ho_k` unchanged, `c1-measure.py:420`),
so `ho_kill == ho_kt` would fail and C1 would be recorded **false**. The failure mode is therefore
self-inflicted, not a route to a false PASS — but it proves the amended `ho_witness_ok` does not
establish that the *executed* tally block is defective; it only establishes that the first block-shaped
text in the file differs. This is a different channel from the sibling seat's shim-variable findings
(`Mutkillvectorfailthreshold.md` §3.2): no environment or shim value is involved, and the tool cannot
see the divergence by construction. Fix direction (next wave, no edits this wave): bind the witness
block to `run_regression()` (reuse the tool's `regression_body`/`tally_block` extraction) and require
the mutation to be *inside* the executed block.

### 3.3 Finding B: guard-branch count-field swap — accept witness says equivalence, real tool KILLs

Same bytes, opposite label: swap the arguments of the unreachable completeness-guard `printf`
(`npass + nfail + nsetup` ↔ `nlegs`). The guard can never fire for a nine-status vector (counts
always sum to `nlegs`), so for every real run the copy is pristine-equivalent; the tool reaches the
branch only through its operand-stress arm (`with_operands`, `tool.py:246-249`, stress loop in
`check_runtime`). Exact JSON (`v5p-accept-guard-swap.json`, sha256
`e2104fc347c00afcadc433a81ab6f61456e3d61176533eba2c41cbb38885ad0f`; mutant bytes
`v5p-accept-guard-swap.sh`, sha256
`5aa9e8462cb381adf26cbd345e0911d8fdb9fafb980925d5bcc901c7e2332a64`):

```json
{
 "author": "probe",
 "edits": [
  {
   "new": "      \"$((npass + nfail + nsetup))\" \"$nlegs\"\n",
   "old": "      \"$nlegs\" \"$((npass + nfail + nsetup))\"\n"
  }
 ],
 "id": "v5p-accept-guard-swap",
 "set": "accept",
 "witness": {
  "vector": [
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0
  ]
 }
}
```

Observed (`accept-opposition.out`, `detail-v5p.out`, `witness-pairs.out`):

- `set=accept`: witness **(True, 'vector-equivalence')** — `a == b == (0, 'REGRESSION: PASS
  (cases=9 passed=9; …)')`, bytes changed.
- Real tool: **KILL, rc 1**, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`,
  `CHECK runtime FAIL vectors=15158 mismatched=36; first: stress dup operand 0 cfg(0,1): got (2,
  'REGRESSION: SETUP (case-tally mismatch: cases=10 counted=9)'), want (2, 'REGRESSION: SETUP
  (case-tally mismatch: cases=9 counted=10)')`.
- The same bytes under `set=kill` ({...`"set": "kill"`, vector `[1,0,…]`}; not a separate file)
  give witness **(False, 'vector')**: `a == b`, so the counter would refuse the copy as
  `ho_invalid`.

**Impact.** This construction is unsealable under either label: `kill` → witness refuses
(`ho_invalid != 0` breaks the C1 predicate); `accept` → witness validates but the tool kills
(`ho_a < ho_at`). The two instruments measure different things — the witness samples one real-run
vector, the tool audits the block's correctness under synthetic operand stress — and there is no
tie-break. It cannot manufacture a false PASS; it is a rejecting blind spot in the sealed-set gate
for the very fault class the guard exists to report.

## 4. Tooling

No installs or upgrades. `bwrap` 0.13.1, Python 3.14.8, git and coreutils were already present and
sufficient. No pacman transactions (guard respected).

## 5. Files (all in scratch unless noted)

- `probe.py` (`f48f7e076859e7141983e9d4b2ba57fd7343555e5fcc6816a723af906dfd15b7`) — the driver.
- `tool.py` (`7b11ba25…3598d10`), `pristine.sh` (`a7d3f2dd…912eb9`), `mutant-assigned.sh`
  (`38cdf560…987d5b`), `v2-fail-setup-swap.sh`, `v3-setup-pass-swap.sh`, `v4-pass-count-swap.sh`,
  `v5-guard-count-swap.sh`, `v6-decoy-swap.sh`, `v5p-accept-guard-swap.sh` (+ their shas in §3).
- `v6-decoy-swap.json` (`92f6d78d…ba5005`), `v5p-accept-guard-swap.json` (`e2104fc3…885ad0f`).
- `baseline.out/.rc`, `assigned.out/.rc`, `adversarial.out/.rc`, `accept-opposition.out/.rc`,
  `decoyshape.out/.rc`, `oracle-proof.out/.rc`, `detail-assigned.out`, `detail-decoy.out`,
  `detail-v5p.out`, `blockrun-evidence.out`, `witness-pairs.out`, `selftest-pristine.log`,
  `selftest-mutant.log`.

## 6. Reproduce

```console
S=/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorcountfieldswap
cd $S
python3 probe.py baseline;        echo baseline_rc=$?          # pristine  -> ACCEPT rc=0, all checks pass
python3 probe.py assigned;        echo assigned_rc=$?          # mutant    -> KILL rc=1, runtime=fail 1786/15158
python3 probe.py adversarial;     echo adversarial_rc=$?       # V2..V6
python3 probe.py accept-opposition; echo accept_opp_rc=$?      # V5' accept-labelled guard swap -> tool KILL
python3 probe.py oracle-proof;    echo oracle_rc=$?             # 28/28 permutations have a diff witness
python3 probe.py detail mutant-assigned.sh; echo detail_rc=$?   # exact failing CHECK line
```

Every invocation above exited 0 (the wrapper's exit code; the tool's own rc is inside each record).
The variants are built from the pinned `pristine.sh` with the counter's own `validate_ho` and
`apply_edits`; their exact edits and witness vectors are the JSON in §3.2/§3.3.

## 7. Verdict summary

| item | expected | actual | verdict |
|---|---|---|---|
| sealed `ho-kill-vector-count-field-swap` (kill) | rc 1, `TALLY_AUDIT: FAIL` | rc 1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`, 1786/15158 runtime mismatches, first at `[1,0,…,0]` | **KILLED** |
| pristine / restored bytes | rc 0, `TALLY_AUDIT: PASS` | rc 0, `TALLY_AUDIT: PASS`, mismatched=0, sha unchanged `a7d3f2dd…` | baseline green, restore exact |
| live-block count-field swap family (V1–V4) | no witness-valid survivor | V1–V3 witness-valid ⇒ KILL; V4 witness-invalid ⇒ ACCEPT; 28/28 permutations oracle-visible | **no survivor (proof in §3.1)** |
| V6 dead-decoy swap (`2f12cd5f…`, kill label) | (attack) | witness **(True,'vector')**, tool **ACCEPT rc 0** | **CRITICAL: witness-gate bypass, exact JSON §3.2** |
| V5' guard swap (`5aa9e846…`, accept label) | (attack) | witness **(True,'vector-equivalence')**, tool **KILL rc 1** | **finding: instruments disagree; unsealable either label, exact JSON §3.3** |

No landed artifact is shown wrong: the deciding run stands, all eight sealed kills (including this
one) are genuinely killed, and the receipt's `ho_kill=8/8` is consistent with this probe. The two
findings are coverage/soundness observations against the amended witness gate; both would surface
as a *miss* in a deciding run, never as a false PASS. Frozen artifacts were not edited.
