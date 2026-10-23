# Mutkillheadextraassign — round 34 w1 mutation probe

Seat: `tameshi-r34-w1-Mutkillheadextraassign` (mutation-tester, leaf).
Claim under attack: C1 operability (tools/tally-audit-v2.py) at rev `c17e593b51802dd4ed568da3265f21c6d00c4273`.
Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch root: `/fast/scratch/hyaku/tameshi-r34-seats/Mutkillheadextraassign/` (lane clone `lane/`, all writes here).
Report path relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

## 0. Pins verified before any run

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
sha256sum tools/tally-audit-v2.py tools/mutate-and-run.sh .ufo/evidence/round-33/c1/c1-measure.py
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tools/tally-audit-v2.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c  .ufo/evidence/round-33/c1/c1-measure.py
```
All three equal the task pins. Second hash check after all runs (same output) confirms the fleet tree was not written.

Setup (one command, `clone_rc=0`, `co_rc=0`):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutkillheadextraassign
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/Mutkillheadextraassign/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
git -C .../lane rev-parse HEAD   -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
```

Pinned bytes materialized from the commit (not the worktree) and hashed:

```
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py > tool.py      # rc 0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh > pristine.sh  # rc 0
sha256sum tool.py pristine.sh
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Detector: the frozen counter was **imported as a module from the lane path**
(`lane/.ufo/evidence/round-33/c1/c1-measure.py`, sha `f6b8868c…a07f28c`); `validate_ho`,
`apply_edits`, `ho_witness_ok`, `run_tool_sandboxed` were called from it. The kill rule
(default CLI mode) was never invoked. The real tool ran as `python3 -I /w/tool.py --runner
/w/copy.sh` under the counter's own bwrap argv (`bwrap_argv`, c1-measure.py:228) with
`timeout 600` outside the sandbox.

## 1. Assigned probe — `ho-kill-head-extra-assign.json` (set=kill)

Sealed bytes: `.ufo/evidence/round-33/heldout/ho-kill-head-extra-assign.json`,
sha256 `9e7f9076c32e0f90a31f8c7e2929fccf4636bc68ede775d52afcaf2185895d40`
(scratch copy `ho.json`, same hash).

```
id=ho-kill-head-extra-assign  set=kill  witness={kind: head}
edits: old "  st_js=$?\n" -> new "  st_js=$?\n  st_js=0\n"
```

Derivation (counter `apply_edits`, which asserts `count==1` per old string):

| artifact | sha256 | size |
|---|---|---|
| pristine.sh / pristine-copy.sh | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | 106218 B |
| mutant.sh (derived) | `c8615c3e092a0a904b429194f5bcba4a53da7ec54bdb4a51bbeb977e7c8c5499` | 106228 B (+1 line) |

Old string count in pristine: 1; new two-line pair count in mutant: 1
(`python3` probe, `probe.out`). `validate_ho` accepted the JSON.

Witness gate (amended amendment 6):

```
ho_witness_ok -> True 'head-leg-assignment'
```
(`probe.out`; gate code c1-measure.py:184-207.)

Bounded detector on pristine and mutated bytes — identical invocation, scratch workdir:

```
baseline (pristine-copy.sh): ('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')
mutant   (mutant.sh):        ('KILL',   1, 'TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)')
```

Full CHECK lines (`capture.py` -> `capture.out`, same bwrap boundary):

```
pristine-copy.sh rc=0
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)

mutant.sh rc=1
CHECK head FAIL legs=9; non-bare leg assignment(s) in the head: st_js=0; leg st_js assigned 2 times in the head; leg st_js appears 3 times in the head (want exactly 2: the local declaration and its bare st_x=$?)
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)
```

Restoration: `run_tool_sandboxed` copies tool and runner into the per-run sandbox and never
writes its inputs. Hashes before/after are identical (`probe.out`):

```
pristine_copy_sha   a7d3f2dd…12eb9   pristine_after_sha   a7d3f2dd…12eb9   pristine_final_sha a7d3f2dd…12eb9
mutant_copy_sha     c8615c3e…c5499   mutant_after_sha     c8615c3e…c5499
```

**Verdict: KILLED** (rc 1, `TALLY_AUDIT: FAIL`, head check; baseline green, so the kill is
attributable to the mutation). This matches the sealed label and the deciding-run receipt.

## 2. Adversarial — same fault family, different construction

Family: an extra assignment to the `st_js` leg status after its capture in `run_regression`'s
head, i.e. the js leg is masked to 0. Three constructions were built from the same pristine
bytes with the counter's `apply_edits` and scored with the same gate and the same sandboxed
tool (`adversary.py` -> `adversary.out`, `capture.py` -> `capture.out`).

| # | construction | json sha256 | derived sha256 | `ho_witness_ok` | tool |
|---|---|---|---|---|---|
| V1 | remove `st_js` from the `local` decl; append `st_js =$?` (spaced) | `8435b82a…0cb54` | `54585d7e…98810` | True `head-leg-assignment` | ACCEPT rc 0 PASS |
| **V2** | **V1 + top-level `st_js() { st_js=0; }` before `run_regression`** | **`e365ab5f…5a7a3`** | **`2e61a4a3…ecee6f`** | **True `head-leg-assignment`** | **ACCEPT rc 0 PASS** |
| V3 | remove decl; append `st_js[0]=0` | `797dda1a…b53d4` | `1cfb0fa9…988f56` | False `head-edit-cannot-kill` | ACCEPT rc 0 PASS |

V2 JSON (content; file `/fast/scratch/hyaku/tameshi-r34-seats/Mutkillheadextraassign/V2-function-mask.json`, pretty-printed on disk):

```json
{
 "id": "V2-function-mask",
 "author": "tameshi-r34-w1-Mutkillheadextraassign",
 "set": "kill",
 "edits": [
  {"old": "  local st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck\n",
   "new": "  local st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck\n"},
  {"old": "run_regression() {\n",
   "new": "st_js() {\n  st_js=0\n}\n\nrun_regression() {\n"},
  {"old": "  st_js=$?\n",
   "new": "  st_js=$?\n  st_js =$?\n"}
 ],
 "witness": {"kind": "head"}
}
```

Full CHECK lines for V2 are identical to pristine (`capture.out`): `head PASS legs=9`,
`static PASS`, `runtime PASS vectors=15158`, `harness PASS 34/34`, `TALLY_AUDIT: PASS`, rc 0.

### 2a. V2 is a real mask, proved behaviorally

The mask is executed by three exact head constructs; a minimal bash trace of them
(`demo-V2.sh`) shows the status flips 1 -> 0, while V1 (same line without the function) leaves it
at 1 and errors "st_js: command not found" (`demo-V1.sh`), and V3 (array subscript on a scalar,
`demo-V3.sh`) also flips 1 -> 0:

```
== V1  status_after_head=[1]   (st_js: command not found)
== V2  status_after_head=[0]
== V3  status_after_head=[0]
```

End-to-end A/B on the **exact mutated `run_regression` body** with the nine fleet legs stubbed to
one fixed status program (leg 1 = 1, all others = 0) and the runner's own `TABLE_*/PIN_*/REV_*`
prelude copied verbatim (`ab.py` -> `ab/pristine.driver.sh`, `ab/V2-function-mask.driver.sh`):

```
pristine       exit=1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
V2-function-mask exit=0 REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

The same failing leg is reported as a pass. This is precisely the defect class the tool's head
check exists to catch ("out-of-block masking/overwrites of leg statuses", tally-audit-v2.py:37-38).

### 2b. Why the tool passes V2

`check_head` scans only `run_regression`'s head (`body[:START]`, tally-audit-v2.py:307-334).
The actual `st_js=0` assignment sits in a top-level helper function outside that span, and the
call line `  st_js =$?` evades both head regexes: it does not match `all_assigns`
`^[ \t]*(st_[A-Za-z0-9_]+)=` (space before `=`; :309), does not match the non-bare probe `(.*)`
fullmatch `\$\?` because it is never collected (:315-317), and it is not a bare leg assignment
(`ASSIGN_RE`, tally-audit-v2.py:166). The twice-only rule is satisfied by counting the call line as the
second occurrence of the name (:326-334), because the declaration occurrence was removed — the
rule's comment says "the local declaration and its bare st_x=$?", but only the count is enforced.

### 2c. Why the gate validates V2

`ho_witness_ok`'s kill+head arm (:199-207) accepts when the head text differs, the block is
identical, and either multiset differs:
`A = ^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*$` or `X = ^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*=`.
V2 changes X: the whole-file head (before the tally start, c1-measure.py:147-152) now contains
`st_js=0` (helper body) and `st_js =$?` (call) in addition to the bare capture, so
`sorted(X)` differs -> `True 'head-leg-assignment'`. A is unchanged (all nine bare captures
remain, same order). The gate's admission is correct here — V2 is a lethal edit, not an inert
one — but its stated assumption that a diff touching the A/X leg-assignment surface is one the
tool will catch ("never as a must-kill the tool would blamelessly pass", c1-measure.py:198-201)
is falsified: the tool passes V2.

## 3. Findings

**F1 (critical) — a genuine must-kill that the amended gate validates but the tool ACCEPTs.**
Variant `V2-function-mask` (json sha `e365ab5f…5a7a3`, derived sha `2e61a4a3…ecee6f`) masks the
`st_js` leg status exactly as the sealed copy does, yet the frozen tool prints
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` with exit 0 while
`ho_witness_ok` returns `True 'head-leg-assignment'`. Behavioral proof: with identical stub
statuses the pristine runner reports `REGRESSION: FAIL (passed=8 failed=1)` (exit 1) and V2
reports `REGRESSION: PASS (passed=9)` (exit 0). Had this construction been in the sealed set, the
deciding run's `score_tool` would have counted it as a missed kill, taking the held-out kill rate
below 8/8. Reproduce:

```
cd /fast/scratch/hyaku/tameshi-r34-seats/Mutkillheadextraassign
python3 adversary.py     # V2: gate=True(head-leg-assignment) tool=('ACCEPT', 0, 'TALLY_AUDIT: PASS …')
python3 capture.py       # V2: CHECK head PASS legs=9 … TALLY_AUDIT: PASS
python3 ab.py            # pristine FAIL exit 1 vs V2 PASS exit 0, same status program
```

**F2 — the gate admits a non-defect as a must-kill.** V1 (`st_js =$?` with no `st_js` function)
is validated as `head-leg-assignment` and PASSed by the tool, but it is inert: bash treats
`st_js =$?` as a command named `st_js`, the status stays 1 (`demo-V1.sh`). A sealed copy built
this way would be scored as an unfair kill miss against a tool that is behaving correctly.
Same reproduction as F1 (`V1-spaced-inert.json`, json sha `8435b82a…0cb54`).

**F3 — the gate refuses, and the tool misses, a third genuine mask.** V3 uses
`st_js[0]=0` after the capture (bash assigns a scalar through subscript 0: status 1 -> 0,
`demo-V3.sh`). The tool PASSes it (`CHECK head PASS legs=9`), and `ho_witness_ok` returns
`False 'head-edit-cannot-kill'` because the line is invisible to both A and X. So V3 is a real
defect admitted by neither artifact; it is a coverage finding on amendment 6's literal-surface
requirement, not an admission hole. Reproduce with the same three commands
(`V3-array-subscript-mask.json`, json sha `797dda1a…b53d4`).

Scope note: the deciding run stands. The assigned sealed copy is correctly KILLED by the tool
and correctly validated by the gate; F1-F3 concern the *discrimination boundary* of the
amended witness rule against constructions absent from the sealed set. They do not reverse
`C1_R33_PASS`; they identify how a future sealed set can make the measurement unfair in either
direction.

## 4. Evidence inventory (scratch, absolute paths)

| path | sha256 / note |
|---|---|
| `lane/` | detached checkout of `0b99d48…` (clone), read-only |
| `tool.py` | `7b11ba25…598d10` (pin) |
| `pristine.sh`, `pristine-copy.sh` | `a7d3f2dd…12eb9` (pin), unchanged before/after |
| `ho.json` | `9e7f9076…95d40` (sealed JSON copy) |
| `mutant.sh` | `c8615c3e…c5499` (assigned mutant) |
| `V1-spaced-inert.sh/.json` | `54585d7e…98810` / `8435b82a…0cb54` |
| `V2-function-mask.sh/.json` | `2e61a4a3…ecee6f` / `e365ab5f…5a7a3` |
| `V3-array-subscript-mask.sh/.json` | `1cfb0fa9…988f56` / `797dda1a…b53d4` |
| `probe.py/.out`, `adversary.py/.out`, `capture.py/.out`, `ab.py` + `ab/` | probe drivers and raw outputs (`probe.out` sha `afca0506…a92f`, `adversary.out` sha `572d6f3d…737e`, `capture.out` sha `bd0141fe…e90d4`) |
| `demo-V1.sh`, `demo-V2.sh`, `demo-V3.sh` | three-line bash traces of the head constructs |

## 5. Bounds / tooling

- Fleet repo, lane clone, jj state and git index: never written; no `git`/`jj` write command was
  run; only `git clone/show/checkout/rev-parse` in the scratch clone. Fleet tool/runner/counter
  hashes identical before and after (section 0).
- No `pacman`/`uv`/`npx` install; no tool install or update to record. No model parameter.
  No `agent://all`, no subagent dispatch.
- Every command above exited 0 unless an exit code is stated (`probe_rc=0`, `adv_rc=0`,
  `ab_rc=0`, `cap_rc=0`; the tool's own rc is reported per run: pristine 0, mutant 1, V1/V2/V3 0).
