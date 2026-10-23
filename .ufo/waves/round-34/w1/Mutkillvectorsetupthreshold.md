# Mutkillvectorsetupthreshold — round-34 w1 (v2 wave), mutation seat

Seat: `tameshi-r34-w1-Mutkillvectorsetupthreshold`. Assigned probe: sealed kill copy
`ho-kill-vector-setup-threshold.json` (set=kill), plus one adversarial variant of the same
fault family against the amended witness gate (`ho_witness_ok`, amendment 6) and the frozen tool.
Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. All work in
`/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorsetupthreshold/`; lane read-only.

## 1. Pins verified before any run

```
mkdir -p .../Mutkillvectorsetupthreshold && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane        # rc=0
env -u GIT_DIR ... git -C .../lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7 # rc=0
git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py > tool.py                            # rc=0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh > pristine.sh                        # rc=0
sha256sum tool.py pristine.sh
```

| artifact | sha256 observed | expected pin | match |
|---|---|---|---|
| `tool.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | yes |
| `pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | yes |
| counter `lane/.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amendment-6 pin | yes |
| sealed `ho-kill-vector-setup-threshold.json` (fleet, read-only) | `4ed1632fac703845c91472e96acb614764d8bfe6e4e37be1fa3e0cc85fbe536e` | unchanged; never written | — |

Pointer: commands above; checkout/rev output in `head.txt`; `cmp -s tool.py lane/tools/tally-audit-v2.py` rc=0
and `cmp -s pristine.sh lane/tools/mutate-and-run.sh` rc=0 (final check, same shell).

## 2. Detector (same on pristine / mutated / restored)

The counter is imported as a module (never run in default mode; kill rule not used). Detector =
`c1r33.run_tool_sandboxed(tool, copy, work)` over the frozen tool: KILL iff `rc==1` and the last
`TALLY_AUDIT:` line starts `FAIL`; ACCEPT iff `rc==0` and it starts `PASS`. Witness detector =
`c1r33.ho_witness_ok(ho, pristine_text, mutated_text, work)` and `c1r33.block_run(block, vector, work)`
(real bwrap boundary). Script `run_sealed.log` exits 0; the tool run inside it exits 1.

## 3. Sealed copy: label KILL — KILLED

Build (each `old` occurs exactly once; `count_old=1`):
`old = "  if [[ $nsetup -gt 0 ]]; then\n"` → `new = "  if [[ $nsetup -gt 1 ]]; then\n"`.

- pristine sha `a7d3f2dd…12eb9`; mutant sha `44ae5f1e64e5adb7239f5456f821ea9d36be51176c8601e9c5f96045e40fe432`.
- `validate_ho` passes; `ho_witness_ok = True ('vector')`; blocks differ.
- Witness `[2,0,0,0,0,0,0,0,0]`: pristine `block_run = (2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')`;
  mutant `(0, 'REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)')`.
  The mutant reports PASS while one leg is unverified — the fault the label names.
- Tool on the mutant: `outcome=KILL rc=1 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'`.
- Counter-level `score_tool([('sealed','kill',body)])` = `1/1` hit.

Pristine → mutated → restored cycle through the same detector (`cycle/cycle.log`, script rc=0):

| step | sha256 | detector |
|---|---|---|
| PRISTINE | `a7d3f2dd…12eb9` | ACCEPT rc=0 `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| MUTATED | `44ae5f1e…e432` | KILL rc=1 `TALLY_AUDIT: FAIL (… runtime=fail …)` |
| RESTORED | `a7d3f2dd…12eb9` | ACCEPT rc=0 `TALLY_AUDIT: PASS (…)` |

`restored_equals_pristine=True`. Verdict on the assigned copy: **KILLED**, matching its label.
Baseline is deterministic and the restore is byte-exact.

## 4. Adversarial probe — FINDING (critical): gate-valid witnesses the tool ACCEPTs

### 4.1 Tool panel, instrumented (no reimplementation)

`adv/panel.log` / `adv2/panel2.log`: import `tool.py`, wrap its own `run_vectors` to record the
vectors `check_runtime` submits, call the real `check_runtime` (script rc=0).

```
check_runtime(pristine block): ok=True detail=vectors=15158 mismatched=0 vectors_seen=15158
[2,0,0,0,0,0,0,0,0]      in_panel=True    (sealed witness: covered)
[2,2,2,0,0,0,0,0,0]      in_panel=True    (count-cluster prefix: covered)
[0,2,2,2,0,0,0,0,0]      in_panel=False   (survivor D witness)
[200,2,0,0,0,0,0,0,0]    in_panel=False   (survivor B witness)
```

Panel shape (`tool.py:372-418`): 256 statuses at every position, every `(fail,setup)` count pair in
prefix placement (`count_vectors`), six count mixes at three placements, and every unordered position
pair over `CO=(1,2,3,4,5,7,9,120,126,127,128,255)` (`tool.py:407`). Consequences: a vector with three
setup legs in a non-prefix placement, or a two-leg vector with a status outside `CO`, is never run.
Gap (i) survives because `nfail=0` in these vectors, so the tally guard's `npass+nfail+nsetup != nlegs`
arm still sums to 9 and lets the mutant PASS.

### 4.2 Survivor D (tightest construction), exact JSON

```json
{
 "id": "D-min-placement",
 "author": "tameshi-r34 w1 mutation seat",
 "set": "kill",
 "edits": [
  {
   "old": "  if [[ $nsetup -gt 0 ]]; then\n",
   "new": "  if [[ $nsetup -gt 0 && ! ( $nsetup -eq 3 && $st_js -eq 0 ) ]]; then\n"
  }
 ],
 "witness": {
  "vector": [0, 2, 2, 2, 0, 0, 0, 0, 0]
 }
}
```

Same gate, same line, same fault (a SETUP run reports PASS); only construction differs.
`adv2/probe.log` (script rc=0):

```
D-min-placement witness_ok=True(vector)
  pristine=(2, 'REGRESSION: SETUP (cases=9 passed=6 cannot-verify=3)')
  mutant  =(0, 'REGRESSION: PASS (cases=9 passed=6; ledger legs exact: killed-delta<=0 flips<=0)')
  tool=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
  score_tool=0/1
D check_runtime: ok=True detail=vectors=15158 mismatched=0
```

`mutant.sh` sha `212b73b26c6c8d015ee7ec432942bbde2334117f67139ed84f1c519fd204fe47`;
`probe.json` sha `a3adf9c084af6b1deb01a4209981cb5ea564e6cb9bc1b772f18af7be11f79a4d`.

### 4.3 Survivor E (status-value gap), exact JSON

```json
{
 "id": "E-min-status6",
 "author": "tameshi-r34 w1 mutation seat",
 "set": "kill",
 "edits": [
  {
   "old": "  if [[ $nsetup -gt 0 ]]; then\n",
   "new": "  if [[ $nsetup -gt 0 && ! ( $st_js -eq 6 && $st_kagi -eq 2 ) ]]; then\n"
  }
 ],
 "witness": {
  "vector": [6, 2, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

`adv2/probe.log`: `witness_ok=True(vector)`; pristine `(2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')`
vs mutant `(0, '… PASS (cases=9 passed=7 …)')`; `tool=ACCEPT rc=0` with
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`; `score_tool=0/1`.
`mutant.sh` sha `5ab7043ead6088b89898f141ac5d7a9ead323d37356ba36c8dfbd5177435ad71`;
`probe.json` sha `457a14c714e5a73b07b74aed3d5dca91a8302b910c2b5bd917194006e1569952`.

Earlier, non-minimized forms of the same two constructions also survived (`adv/probe.log`, script rc=0):
A-placement3 `[0,2,2,2,0,…]` and B-status200 `[200,2,0,…]` → `tool=ACCEPT rc=0`, `score_tool 0/1`
(`adv/score.log`, rc=0). Status 6 in E is an ordinary exit code (126 is inside `CO`; 6 is not), so the
construction is not merely a fantasy value.

### 4.4 Boundary control: the gap is not "any conjunct"

`C-count3` = `if [[ $nsetup -gt 0 && $nsetup -ne 3 ]]; then` with witness `[2,2,2,0,…]`:
`witness_ok=True(vector)`, `tool=KILL rc=1 runtime=fail`, `score_tool=1/1` (`adv/probe.log`,
`adv/score.log`). Count-only weakenings are covered: `count_vectors` supplies a prefix cluster for
every `(fail,setup)` pair, so each `nsetup=s` cluster (`s=1..9`, including the `[2,2,2,…]` witness) is
in the panel, and the fail branch precedes setup for `nfail>0`. Only placement- or status-pair-selective
conjuncts survive.

### 4.5 What the finding does and does not establish

- It does **not** contradict the landed receipt: `C1_R33` measured the authored sealed set, whose
  eight kill copies (including this seat's) the tool killed; this seat re-verifies one of them KILLED
  (§3). The deciding output (`.ufo/evidence/round-34/measure/c1-deciding-run.stdout`, exit file `0`)
  matches the dispatch receipt line; this seat did not re-run the counter in default mode (consumed
  kill rule), only read the recorded stdout and exit file.
- What it does bound: `ho_witness_ok` kill+vector accepts any `a != b` on the *author-chosen* vector
  (`c1-measure.py:184-220`) without requiring that vector to be one the tool's runtime sweep covers.
  A copy can therefore pass the amendment-6 gate and still be invisible to the tool. The counter would
  fail closed (`ho_kill < ho_kt` → `C1_R33_PASS=false`) if such a copy were in the set, so there is no
  false PASS of the landed measurement; but "the tool kills the setup-threshold family" is established
  only for faults whose distinguishing vector lies in the 15,158-vector panel. The v3 residue classes
  should say that, not more.
- No tool edit is proposed (frozen artifact; contract unchanged). This is a coverage finding against
  the gate plus the panel, recorded for the round's residue list.

## 5. Reproduction (from the fleet root; no lane writes)

```bash
S=/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorsetupthreshold
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
mkdir -p "$S/repro" && cd "$S"
git -C "$L" show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > "$S/repro/pristine.sh"
git -C "$L" show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > "$S/repro/tool.py"
sha256sum "$S/repro/pristine.sh" "$S/repro/tool.py"   # pins from §1
python3 - "$S" "$L" <<'PY'
import importlib.util, json, os, sys
S, L = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('c', os.path.join(L, '.ufo/evidence/round-33/c1/c1-measure.py'))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
pristine = open(os.path.join(S, 'repro/pristine.sh'), encoding='utf-8').read()
new = '  if [[ $nsetup -gt 0 && ! ( $nsetup -eq 3 && $st_js -eq 0 ) ]]; then\n'
assert pristine.count('  if [[ $nsetup -gt 0 ]]; then\n') == 1
mut = pristine.replace('  if [[ $nsetup -gt 0 ]]; then\n', new, 1)
ho = {'id': 'D-min-placement', 'author': 'repro', 'set': 'kill',
      'edits': [{'old': '  if [[ $nsetup -gt 0 ]]; then\n', 'new': new}],
      'witness': {'vector': [0, 2, 2, 2, 0, 0, 0, 0, 0]}}
d = os.path.join(S, 'repro'); open(os.path.join(d, 'mutant.sh'), 'w').write(mut)
print('witness_ok', c.ho_witness_ok(ho, pristine, mut, d)[0])          # True
print('tool', c.run_tool_sandboxed(os.path.join(d, 'tool.py'), os.path.join(d, 'mutant.sh'), d))
print('score', c.score_tool(os.path.join(d, 'tool.py'), [('D', 'kill', mut.encode())], d))
PY
```

Observed on this seat: `witness_ok True`; `('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')`; `score (0, 1, 0, 0)`.
The same block with the sealed edit (`-gt 1`) yields `('KILL', 1, 'TALLY_AUDIT: FAIL (… runtime=fail …)')`.

## 6. Bounds compliance and restoration evidence

- Lane untouched: `git -C lane status --porcelain` empty (rc=0); `cmp` tool/runner against lane copies rc=0;
  no git/jj write commands anywhere; frozen tool, runner, counter and sealed JSON only read.
- Writes confined to the scratch dir and this report. Heldout JSON sha `4ed1632f…536e` observed, never written.
- Kill rule honored: the counter was only imported and its functions called on scratch copies; no default-mode run.
- No tool installs or upgrades; no pacman transactions; no subagents.
- Two caller-side setup errors (script rc=1) occurred before the sealed run and are not evidence:
  `tally_block_of` given bytes (`TypeError`) and `validate_ho` without an `author` (`CounterError`).
  Both were corrected; no artifact was at fault, and no result above depends on them.
- Incidental observation, not my assigned probe: `tool.tally_block` ends the block at `body.rfind('}')`
  (`tool.py:149-156`), so on this runner the audited "block" text is not byte-equal to `REF_BLOCK`
  (`adv2/refdiff.log`, script rc=0); `check_runtime` still executes the tally code first, so the
  panel results above are unaffected.
