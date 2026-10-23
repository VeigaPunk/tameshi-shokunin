# RevengerIndependentSet — independent sealed-set revenger (round 34, wave 1)

Seat: `tameshi-r34-w1-RevengerIndependentSet` (leaf member, no subagents).
Date: 2026-10-23. Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (clone detached at it, verified by `git rev-parse HEAD` = `0b99d48e…`, clone.exit=0, checkout.exit=0).
Claim under attack: C1 (operability, tool `tools/tally-audit-v2.py`), MEASURED TRUE at `c17e593b…`, receipt `C1_R33 … C1_R33_PASS=true`, exit 0. **The deciding run stands; everything below is observation.**

## Pins (verified before any run)

| artifact | sha256 | how |
|---|---|---|
| `tools/tally-audit-v2.py` @ tip | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | `git -C $SCR/lane show 0b99d48e…:tools/tally-audit-v2.py > tool.py`; `sha256sum` — matches pin |
| `tools/mutate-and-run.sh` @ tip | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `git show …:tools/mutate-and-run.sh > pristine.sh`; `sha256sum` — matches pin |
| counter (amendment 6) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | copied to `$SCR/.ufo/evidence/round-33/c1/c1-measure.py` |
| round-32 counter (v1, import dep) | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | copied to `$SCR/.ufo/evidence/round-32/c1-measure.py` |

Environment: bwrap 0.13.1 (`/usr/bin/bwrap`), Python 3.14.8. The 14 landed seals under `.ufo/evidence/round-33/heldout/` are byte-identical between the tip commit and the live tree (14× `cmp` SAME).
Tooling installs: none (no install needed; bwrap/python3 already present — operator rule satisfied vacuously).
Kill rule: consumed, never invoked — the counter was only `import`ed as a module; `main()`/`write_controls` never called. All runs: `cmd; echo $? > file`, no `&&`.

## Method

`author_seals.py` + `author_seals_extra.py` (scratch) replicate the counter's own seal pipeline from `main()`'s held-out loop, per seal: `json` → `validate_ho` → `apply_edits(pristine, edits)` (asserts each `old` occurs exactly 1×, asserts `mutated != pristine`) → `ho_witness_ok(ho, pristine, mutated, work)` → `run_tool_sandboxed(TOOL, copy, work)` with the pinned tool bytes. KILL = tool exit 1 + last line `TALLY_AUDIT: FAIL`; ACCEPT = exit 0 + `TALLY_AUDIT: PASS`. Driver exits: `driver.exit=0`, `driver2.exit=0`.

## Authored seals (scratch-only, never committed)

### Seal 1 — must-kill, NEW family `head-missing-assign` (vs landed: nonbare-rebind, extra-assign, 6 block families)

Edit: `  st_citecheck=$?\n` → `` (delete the leg capture; count 1). Witness `{"kind":"head"}`.
Seal `seals/rev-kill-head-missing-assign.json` sha256 `4d0afc608d5aa606c49d3baf9aa10a9f393c4a2c50bd2b42c802942b39de011b`; mutant copy sha256 `0f95a4d2c9b6f8dbad6437d7d5c451aacc3783484114fba5de62793ff0d3768d`.

- `validate_ho` ✓; `ho_witness_ok` → **True** (`head-leg-assignment` — the bare-assignment multiset A changes 9→8).
- Tool: **KILL**, rc=1, last line `TALLY_AUDIT: FAIL (head=pass static=fail runtime=fail harness=fail)`.
- **Label agrees.** The claim generalizes to this independent kill family.

### Seal 2 — must-accept, NEW family `operand-reorder` (vs landed: comments/whitespace/inert-line/head-cosmetics)

Edit: the tally loop `for st in "$st_js" … "$st_citecheck"; do\n` → operand list fully reversed (count 1). Witness `{"vector":[1,2,3,0,0,0,0,2,1]}`.
Seal sha256 `e5e1f0bfb1125b070f868c6f6a58a205fa9f5b5fb5d8f478952ccf5a6d987186`; mutant copy sha256 `7d3d5a5f34fe3595d85ebcc06e657a814b7c86dcf285032e585b533d1c627874`.

- `validate_ho` ✓; `ho_witness_ok` → **True** (`vector-equivalence`, a == b, bytes differ).
- Tool: **ACCEPT**, rc=0, last line `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.
- **Label agrees.** The dataflow-identified tally loop tolerates an operand reorder no landed accept seal exercises.

### Baseline

Pinned pristine runner → **ACCEPT**, rc=0, `TALLY_AUDIT: PASS (…all pass…)` — my sandbox reproduction of the accept arm agrees with the deciding run.

## FINDING R1 (critical): the amendment-6 witness gate certifies a label the tool rejects — `accept+head` is label-blind

### Seal 3 — mislabel attempt, SUCCEEDED

`rev-accept-head-leg-rename`: two head edits, count 1 each —
`  local st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck\n` → `st_claims`→`st_claimz`, and `  st_claims=$?\n` → `  st_claimz=$?\n`. Tally block byte-identical. Witness `{"kind":"head"}`, **set: accept**.
Seal sha256 `ccf8cad3f8fb7909cdac276fdefdce92517b715a167626f9d3633ab3e837bb87`; mutant copy sha256 `11b73e4098befac5d25a90bf60cc0abeb196798bca03d7a10fb8bb7384bfdfa0`.

- `validate_ho` ✓; `ho_witness_ok` → **True**, reason `head` — the accept+head arm requires only `head_of(mutated) != head_of(pristine)` and identical block; no behavioral check.
- Tool: **KILL**, rc=1, `TALLY_AUDIT: FAIL (head=pass static=fail runtime=fail harness=fail)` (the loop still reads `$st_claims`; names ≠ REF panel ⇒ static/harness fail; the mutant runner is genuinely broken under `set -u`).
- **Gate-valid, label wrong.** Had this seal been committed under `.ufo/evidence/round-33/heldout/`, the deciding run would have scored `ho_accept=6/7` and printed `C1_R33_PASS=false`.

### R1b — the same hole admits LANDED kill bytes under an accept label

Scratch copy of landed `ho-kill-head-extra-assign.json` with only `"set": "kill"` → `"accept"` (seal `seals/relabel-exp.json` sha256 `a4f72d54a083016e7b02046a24af96b947f17a9fd95930b021b8909c768a36b8`):
`validate_ho` ✓, `ho_witness_ok` → **True** (`head`), tool → **KILL**, rc=1, `TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)`. The gate accepts the *same mutant bytes* as must-kill and as must-accept; nothing in amendment 6's accept+head arm constrains the label. Its stated intent — "a lethal ride-along behind a benign head edit is refused" — only refuses ride-alongs *inside the block*; a head-native lethal edit sails through.

## FINDING R2 (critical): `accept+vector` equivalence on one vector is strictly weaker than the tool's stress surface

`rev-accept-vector-guard-undercount-only`: `  if (( npass + nfail + nsetup != nlegs )); then\n` → `… < nlegs …` (count 1), witness `{"vector":[0,0,0,0,0,0,0,0,0]}`, **set: accept**.
Seal sha256 `3391002c63d93b9db1ad94d0ca4806d1177f27ba792f7748e8cbd4f28f08a1ad`; mutant copy sha256 `e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe`.

- `block_run` proof: pristine `(0, "REGRESSION: PASS (cases=9 passed=9; …)")` == mutated — identical on the witness vector (indeed on every well-formed 9-leg vector; the guard never fires there).
- `validate_ho` ✓; `ho_witness_ok` → **True** (`vector-equivalence`).
- Tool: **KILL**, rc=1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` — the operand drop-stress (sum 8 < 9) diverges: `!=` refuses SETUP, `<` passes.
- **Gate-valid, label wrong, in a second, independent gate arm.** No single-vector witness can certify equivalence for a fault that only the dup/drop stress sees.

## Bound of the findings (analytical, [INFERENCE] — not measured)

No *kill-labeled* mislabel was constructed, and I argue none exists at this tool pin: kill+head gate-validation requires an A/X leg-assignment-line diff, which is exactly `check_head`/`check_static`/`check_harness`'s detection surface (add/remove/rename of a bare `st_x=$?` always breaks names-vs-REF or the twice-only rule → KILL); kill+vector requires a real `a != b` on some witness vector, and `check_runtime` sweeps every status 0..255 at every position, every (failing, setup) pair, co-occurrence pairs, and operand dup/drop stress, so any such vector lies inside the sweep. Both demonstrated mislabels are accept-labeled-but-killed, i.e. the failure direction is conservative: a poisoned seal would have made the deciding run print `C1_R33_PASS=false`, never a false PASS.

## Impact

- Deciding receipt `C1_R33 … PASS=true`: **stands**. All 14 landed labels are tool-agreeing in the deciding run; my two valid independent seals (R: kill/accept agreement on new families) extend the same behavior.
- What the gate actually certifies: witness **self-consistency**, not label correctness. `ho_invalid=0` in the receipt must not be read as "labels are sound". Any future claim or band keyed to "gate-valid ⇒ label-correct" is unsound at this pin.
- Repair direction (NOT applied — tool and counter bytes are frozen this wave; v3 residue classes are routed to round 35 Holds): require per-seal tool-agreement evidence inside the witness (a recorded `run_tool_sandboxed` verdict matching the label), or replace single-vector accept equivalence with the full public vector set plus operand stress. This belongs in a round-35 amendment, pre-data.

## Artifact inventory (all under `$SCR` = `/fast/scratch/hyaku/tameshi-r34-seats/RevengerIndependentSet`)

- `seals/rev-kill-head-missing-assign.json` `4d0afc60…` · `seals/rev-accept-vector-operand-reorder.json` `e5e1f0bf…` · `seals/rev-accept-head-leg-rename.json` `ccf8cad3…` · `seals/rev-accept-vector-guard-undercount-only.json` `3391002c…` · `seals/relabel-exp.json` `a4f72d54…`
- `copies/<id>.sh` mutants: `0f95a4d2…`, `7d3d5a5f…`, `11b73e40…`, `e1ef181c…`
- `results/{seals,extra,baseline,relabel}.json`; drivers `author_seals.py` (`driver.exit=0`), `author_seals_extra.py` (`driver2.exit=0`); `tool.py`, `pristine.sh`, `lane/` (read-only clone at `0b99d48e…`).

## Reproduction

```bash
SCR=/fast/scratch/hyaku/tameshi-r34-seats/RevengerIndependentSet
mkdir -p $SCR && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $SCR/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $SCR/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo $?
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $SCR/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > $SCR/tool.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $SCR/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > $SCR/pristine.sh
sha256sum $SCR/tool.py $SCR/pristine.sh   # 7b11ba25…8d10 / a7d3f2dd…2eb9
mkdir -p $SCR/.ufo/evidence/round-33/c1 $SCR/.ufo/evidence/round-32
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c1/c1-measure.py $SCR/.ufo/evidence/round-33/c1/
cp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32/c1-measure.py $SCR/.ufo/evidence/round-32/
cd $SCR && python3 author_seals.py; echo $?        # → 0; per-seal records + baseline + relabel probe
python3 author_seals_extra.py; echo $?             # → 0; R2 guard-undercount mislabel
```

No default-mode counter invocation anywhere; the kill rule stays consumed. No frozen artifact was edited; all writes stayed in `$SCR` and this report file.
