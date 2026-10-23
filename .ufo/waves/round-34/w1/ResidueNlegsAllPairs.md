# ResidueNlegsAllPairs — round 34 w1: the all-pairs `nlegs`-recompute class vs frozen tally-audit v2

Seat: mutation-tester (leaf). Measurement-only; the tool pin `7b11ba25…8d10` was never edited.
Fourteen single-edit `nlegs`-formula mutants on `run_regression`'s tally block were audited by the
frozen tool, and every verdict below is a measurement, not an amendment.

## Verdict

**8 of 14 mutants KILLED (exit 1, `runtime=FAIL`); 6 SURVIVED (exit 0, `TALLY_AUDIT: PASS`).**
All 6 survivors are behaviourally distinct from pristine on a len-9 status vector
(`block_run` pristine ≠ mutant) and all 6 validate as must-kill copies under the frozen
amendment-6 gate (`ho_witness_ok` → `True 'vector'`; `out/validity.json`). The residue is two-dimensional:

| boundary | measured | mutants |
|---|---|---|
| status alphabet | the co-occurrence panel pairs only over `{1,2,3,4,5,7,9,120,126,127,128,255}` (`tool.py:407-414`); a pair with any status outside that set is never generated | `nl-status-pair-6`, `nl-status-pair-8`, `nl-status-pair-200`, `nl-status-pair-6-6`, `nl-arith-pair-5-121` |
| arity | no vector carrying a status ≥3 has more than two non-zero legs (`max_nonzero_when_ge3=2`, `out/panel-invariants.json`) | `nl-triple-in-CO` |

The **landed fix itself is confirmed**: both round-33 DevNlegs survivors replay as **KILL**
(`replay-pair3-r33`, `replay-pair127-r33`), and count-pair, in-alphabet pair, zero+status and
sum-formula recomputes all die — 8 kills, none of them a false reject (the seven status-vector
kills all show `flips=True`; the sum-formula kill is proven behaviour-bearing by the operand-drop
witness below).

C1 (deciding run) stands unchanged: none of the 8 sealed must-kill copies is an `nlegs`
recompute (all 14 sealed JSONs were read: 8 kill + 6 accept), so the deciding receipt is not touched by this
class. This is a round-35 routing item under the same freeze-before-data discipline, not a
contract change.

## Pins and setup

```
$ mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ResidueNlegsAllPairs
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane          # clone.rc=0
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                        # checkout.rc=0
$ git -C .../lane rev-parse HEAD
0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
$ git -C .../lane status --porcelain                                # empty
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show \
    0b99d48e…:tools/tally-audit-v2.py > tool.py                     # show-tool.rc=0
$ … :tools/mutate-and-run.sh > pristine.sh                          # show-runner.rc=0
$ … :.ufo/evidence/round-33/c1/c1-measure.py > counter.py           # show-counter.rc=0
$ sha256sum tool.py pristine.sh counter.py
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c  counter.py
```

All three match the assignment pins (tool `7b11ba25…8d10`, runner `a7d3f2dd…2eb9`, counter
`f6b8868c…a07f28c`). `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` were unset for every git invocation;
no git/jj write ran; nothing outside the scratch dir was written except this report.

Scratch tree: `probe/.ufo/evidence/round-32/c1-measure.py` (extracted at the tip,
sha `ecb26529…faca`) and `probe/.ufo/evidence/round-33/c1/c1-measure.py` (the frozen counter) exist
only so the counter's own relative import of v1 resolves; the probe import is
`probe_run.py:106-107`.

## Instrument and method

* **Frozen tool as detector.** `tool.py` is imported as a module (`probe_run.py:106-111`). The
  exact runtime panel is captured by spying on `tool.run_vectors` and calling `tool.check_runtime`
  on each block — no reimplementation of the vector list. `tool.check_runtime` is the same code path
  `audit()` uses (`tool.py:555-570`).
* **Behavioural detector.** The round-33 counter is imported as a module; `block_run(block, vector,
  work)` runs a tally block under the counter's bwrap boundary and returns `(rc, first stdout line)`.
  `run_tool_sandboxed(tool, copy, work)` supplies the decision instrument's outcome labels
  (`KILL` = rc 1 + `TALLY_AUDIT: FAIL`; `ACCEPT` = rc 0 + `TALLY_AUDIT: PASS`; `tool.py` copy and
  runner copy are the only files visible). The counter's **default mode was never invoked** — no
  `--lane/--rev/--work` command exists in this seat (the kill rule is consumed); only
  `validate_ho`, `ho_witness_ok`, `block_run`, `run_tool_sandboxed` were called.
* **Mutant construction.** Each mutant is `pristine.sh` with one exact-string insertion between the
  counting loop's `done` and the FAIL branch. The anchor occurs exactly once (asserted in
  `probe_run.py:104-105`); `diff pristine.sh mut/nl-status-pair-in-CO.sh` shows the single line
  (`1440c1440`). Mutants are separate files; `pristine.sh` was never edited.
* **Per-mutant commands.** Direct: `python3 -I tool.py --runner mut/<id>.sh` (the argv is
  `probe_run.py:167-168`; rc recorded as `tool_direct_rc`). Sandboxed: `run_tool_sandboxed` with a
  copy of the same bytes (`probe_run.py:178-179`). Witness: `block_run` on pristine and mutant
  blocks at the recorded 9-status vector (`probe_run.py:153-159`), labelled with whether that
  vector is in the captured panel (`probe_run.py:125`).

## Commands actually run (exit codes as captured)

```
$ timeout 900 python3 -I tool.py --runner pristine.sh > out/pristine.tool.txt 2> out/pristine.tool.err
$ echo $? > out/pristine.tool.rc                     # 0
$ timeout 1500 python3 -I probe_run.py > out/probe.log 2>&1; echo $? > out/probe.rc          # 0
$ timeout 600  python3 -I probe_add.py > out/probe-add.log 2>&1; echo $? > out/probe-add.rc   # 0
$ timeout 300  python3 -I validity.py  > out/validity.log 2>&1; echo $? > out/validity.rc     # 0
$ timeout 300  python3 -I panel_invariants.py; echo $? > out/panel-invariants.rc              # 0
$ timeout 900  python3 -I tool.py --runner mut/<id>.sh        # per mutant, issued by probe_run.py:167-168
```

`probe_run.py` was executed with the 11-mutant list and its receipts are `out/receipts.json`; the
three rows added afterwards are measured by `probe_add.py` through the same code path and recorded
in `out/receipts-add.json`. Every per-mutant direct command ran under `timeout 900` with the exit
code stored in `tool_direct_rc`; every sandboxed command ran under the counter's `timeout 600`
inside `run_tool_sandboxed` (`counter.py:234-263`).

## Baseline control (pristine)

`timeout 900 python3 -I tool.py --runner pristine.sh` → exit **0** (`out/pristine.tool.rc`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

The baseline passes, so no mutant verdict below is inconclusive for baseline reasons.

## Panel facts (captured from the frozen bytes, not re-derived)

`out/receipts.json` (`panel_vectors`, `one_nonzero_panel_statuses`, `two_nonzero_panel_statuses`):

* **7 561 vectors per config**; the tool's log line `vectors=15158` = 7 561 × 2 configs +
  18 operand-stress blocks × 2 configs (`tool.py:417-437`).
* single-non-zero vectors cover **all 255 non-zero statuses** (`tool.py:381-388`), so every non-CO
  status appears somewhere — but **`max_nonzero_when_nonCO = 1`**: a vector containing any status
  outside the 12-status co-occurrence alphabet `{1,2,3,4,5,7,9,120,126,127,128,255}`
  (`tool.py:407-414`) has exactly one non-zero leg;
* vectors with exactly two non-zero legs use **exactly** that 12-status alphabet
  (`two_nonzero_statuses`, `out/panel-invariants.json`);
* **`max_nonzero_when_ge3 = 2`**: a vector containing any status ≥3 has at most two non-zero legs;
  the count/mix vectors that do carry up to nine non-zero legs use only statuses 0/1/2;
* the harness check splices `tblock=$AUDIT_INJECT` into the copy's harness (`tool.py:512`), so a
  copy's own tally-block edit is invisible to it.

Consequence: a block whose only defect needs (non-CO status at leg *i*) ∧ (any non-zero status at
leg *j* ≠ *i*), or (a status ≥3) ∧ (two other non-zero legs), is not distinguishable by the sweep.
The six survivors instantiate exactly those cells; `out/panel-invariants.json` holds the measured
counts (`n=7561`, `max_anomalous=2`, `max_nonzero_when_nonCO=1`, `max_nonzero_when_ge3=2`).

## Per-mutant receipts

Witnesses are 9-status vectors in leg order `st_js st_kagi st_tsu st_mado st_checklist st_claims
st_roundgate st_sourcescheck st_citecheck`. "in panel" is membership in the captured 7 561-vector
list. "tool" is the sandboxed decision-instrument outcome; every direct rc agrees.

| mutant | inserted line (after the counting loop) | witness | pristine → mutant first line | in panel | tool | failing check |
|---|---|---|---|---|---|---|
| `nl-count-pair-sub1` | `if (( nfail == 1 && nsetup == 1 )); then nlegs=$((nlegs - 1)); fi` | 1 2 0 0 0 0 0 0 0 | FAIL cases=9… → FAIL cases=8… | yes | **KILL** (1) | runtime (1592 mismatches) |
| `nl-status-pair-in-CO` | `if [[ $st_js == 3 && $st_kagi == 1 ]]; then nlegs=$((nlegs - 1)); fi` | 3 1 0 0 0 0 0 0 0 | FAIL cases=9… → FAIL cases=8… | yes | **KILL** (1) | runtime (2) |
| `nl-status-pair-126-127` | `if [[ $st_mado == 126 && $st_checklist == 127 ]]; then nlegs=$((nlegs - 1)); fi` | 0 0 0 126 127 0 0 0 0 | SETUP cases=9… → SETUP cases=8… | yes | **KILL** (1) | runtime (2) |
| `nl-status-pair-3-3` | `if [[ $st_js == 3 && $st_kagi == 3 ]]; then nlegs=$((nlegs - 1)); fi` | 3 3 0 0 0 0 0 0 0 | SETUP cases=9… → SETUP cases=8… | yes | **KILL** (1) | runtime (2) |
| `nl-status-zero-pair-6` | `if [[ $st_js == 0 && $st_roundgate == 6 ]]; then nlegs=$((nlegs - 1)); fi` | 0 0 0 0 0 0 6 0 0 | SETUP cases=9… → SETUP cases=8… | yes | **KILL** (1) | runtime (2) |
| `replay-pair3-r33` | `nlegs=$((nlegs + (st_js == 3 && st_kagi == 3)))` | 3 3 0 0 0 0 0 0 0 | SETUP cases=9… → SETUP cases=10… | yes | **KILL** (1) | runtime (2) |
| `replay-pair127-r33` | `nlegs=$((nlegs - (st_tsu == 127 && st_mado == 127)))` | 0 0 127 127 0 0 0 0 0 | SETUP cases=9… → SETUP cases=8… | yes | **KILL** (1) | runtime (2) |
| `nl-sum-recompute-inert` | `nlegs=$(( npass + nfail + nsetup ))` | stress (below) | — | — | **KILL** (1) | runtime (36, all stress) |
| `nl-status-pair-6` | `if [[ $st_js == 6 && $st_kagi == 1 ]]; then nlegs=$((nlegs - 1)); fi` | 6 1 0 0 0 0 0 0 0 | FAIL cases=9… → FAIL cases=8… | **no** | **survived** (0, PASS) | — |
| `nl-status-pair-8` | `if [[ $st_kagi == 8 && $st_tsu == 1 ]]; then nlegs=$((nlegs - 1)); fi` | 0 8 1 0 0 0 0 0 0 | FAIL cases=9… → FAIL cases=8… | **no** | **survived** (0, PASS) | — |
| `nl-status-pair-200` | `if [[ $st_claims == 1 && $st_citecheck == 200 ]]; then nlegs=$((nlegs - 1)); fi` | 0 0 0 0 0 1 0 0 200 | FAIL cases=9… → FAIL cases=8… | **no** | **survived** (0, PASS) | — |
| `nl-status-pair-6-6` | `if [[ $st_js == 6 && $st_kagi == 6 ]]; then nlegs=$((nlegs - 1)); fi` | 6 6 0 0 0 0 0 0 0 | SETUP cases=9… → SETUP cases=8… | **no** | **survived** (0, PASS) | — |
| `nl-arith-pair-5-121` | `(( nlegs -= (st_tsu == 5 && st_mado == 121) ))` | 0 0 5 121 0 0 0 0 0 | SETUP cases=9… → SETUP cases=8… | **no** | **survived** (0, PASS) | — |
| `nl-triple-in-CO` | `if [[ $st_js == 1 && $st_kagi == 2 && $st_tsu == 3 ]]; then nlegs=$((nlegs - 1)); fi` | 1 2 3 0 0 0 0 0 0 | FAIL cases=9 passed=6 failed=1 setup=2 → FAIL cases=8… | **no** | **survived** (0, PASS) | — |

`nl-status-pair-3-3` uses the same witness vector as `replay-pair3-r33`; `nl-status-pair-in-CO`
uses its own `(3,1)` vector. They differ only in edit form (`[[ ]]` vs arithmetic), and all four
in-alphabet pair rows are killed.

## Survivors — exact witness evidence

Every survivor's direct audit ends
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, exit 0, with
`CHECK runtime PASS … vectors=15158 mismatched=0`; static/head pass because `local nlegs=9` and the
nine `st_*=$?` assignments are untouched.

```
nl-status-pair-6      witness 6 1 0 0 0 0 0 0 0
  pristine (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
  mutant   (1, 'REGRESSION: FAIL (cases=8 passed=7 failed=1 setup=1)')
nl-status-pair-8      witness 0 8 1 0 0 0 0 0 0
  pristine (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
  mutant   (1, 'REGRESSION: FAIL (cases=8 passed=7 failed=1 setup=1)')
nl-status-pair-200    witness 0 0 0 0 0 1 0 0 200
  pristine (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
  mutant   (1, 'REGRESSION: FAIL (cases=8 passed=7 failed=1 setup=1)')
nl-status-pair-6-6    witness 6 6 0 0 0 0 0 0 0
  pristine (2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')
  mutant   (2, 'REGRESSION: SETUP (cases=8 passed=7 cannot-verify=2)')
nl-arith-pair-5-121   witness 0 0 5 121 0 0 0 0 0
  pristine (2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')
  mutant   (2, 'REGRESSION: SETUP (cases=8 passed=7 cannot-verify=2)')
nl-triple-in-CO       witness 1 2 3 0 0 0 0 0 0
  pristine (1, 'REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)')
  mutant   (1, 'REGRESSION: FAIL (cases=8 passed=6 failed=1 setup=2)')
```

Each `cases=` field is wrong on exactly the trigger vector, and the printed `cases=` is the block's
only statement of `nlegs`; `killed-delta`/`flips` bookkeeping is unaffected, so a real runner copy
carrying the defect would report a wrong case total while every branch stays self-consistent.
Reproduce one:

```
cd /fast/scratch/hyaku/tameshi-r34-seats/ResidueNlegsAllPairs
timeout 900 python3 -I tool.py --runner mut/nl-status-pair-6.sh; echo $? > out/repro-pair6.rc
```

Observed when `probe_run.py` issued this argv: rc 0,
`CHECK runtime PASS vectors=15158 mismatched=0`,
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` (`out/probe.log`).

Under the frozen amendment-6 witness rule, all six are valid must-kill copies — `validate_ho`
passes (kill + len-9 vector) and `ho_witness_ok` returns `True 'vector'` for each
(`out/validity.log`, `out/validity.json`). A sealed set containing any of them would have made the
frozen tool miss; the landed set contains none (next section).

Plausibility: 8 is `ENOEXEC` — a runner leg whose target is not executable exits 8, and a natural
"a leg that never executed is not a case" refactor decrements `nlegs` when a leg exits 8; 6 is
`ENXIO`. 121/200 are less canonical but inside the 0..255 range the panel itself sweeps singly
(`tool.py:381-388`), so the tool already treats those statuses as meaningful at one leg.

## Killed — exact first mismatches (all runtime-only)

From `out/receipts.json` (`runtime_check.detail`); the seven status-vector kills all show
witness `flips=True` and the sum-formula kill is witnessed by the operand drop below, so no kill is
a false reject:

```
nl-count-pair-sub1     mismatched=1592; first statuses 1 2 0 0 0 0 0 0 0:
                       got FAIL cases=8 want FAIL cases=9
nl-status-pair-in-CO   mismatched=2; first 3 1 0 0 0 0 0 0 0: got FAIL cases=8 want cases=9
nl-status-pair-126-127 mismatched=2; first 0 0 0 126 127 0 0 0 0: got SETUP cases=8 want cases=9
nl-status-pair-3-3     mismatched=2; first 3 3 0 0 0 0 0 0 0: got SETUP cases=8 want cases=9
nl-status-zero-pair-6  mismatched=2; first 0 0 0 0 0 0 6 0 0: got SETUP cases=8 want cases=9
replay-pair3-r33       mismatched=2; first 3 3 0 0 0 0 0 0 0: got SETUP cases=10 want cases=9
replay-pair127-r33     mismatched=2; first 0 0 127 127 0 0 0 0 0: got SETUP cases=8 want cases=9
```

The two replays are the exact round-33 DevNlegs survivor edits
(`corpus/lessons/round-33.md:74-78`; `.ufo/waves/round-33/w1/DevNlegs.md` "Survivors"), now killed by the landed
co-occurrence vectors for `(3,3)` and `(127,127)`. `nl-status-zero-pair-6` is killed by the
single-position sweep (status 6 at position 6 leaves every other leg 0, satisfying the pair gate).

## The sum-formula mutant is not inert (correction of the pre-run label)

`nl-sum-recompute-inert` was authored on the hypothesis that `nlegs=$((npass+nfail+nsetup))` is
equivalent for every 9-operand vector. The measurement falsified that: the tool's operand stress
kills it (`mismatched=36`, first `stress dup operand 0 … got PASS cases=10 passed=10, want SETUP
case-tally mismatch`), and the drop witness is the round-29 defect shape:

```
drop last operand, statuses 0 0 0 0 0 0 0 0 0
  pristine (2, 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)')
  mutant   (0, 'REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)')
```

So this row confirms the dup/drop stress arm works; it is not a vector-class datum. (The same row
was already KILLED in round 33 as `recompute-sum`; `corpus/lessons/round-33.md`, DevNlegs table.)

## What this does and does not say about C1

* The deciding receipt (`.ufo/evidence/round-34/measure/c1-deciding-run.stdout`, sha
  `3e28149f…b05c`, exit 0 in `c1-deciding-run.exit`) reports `C1_R33_PASS=true` with
  `ho_kill=8/8 ho_accept=6/6`. The sealed kill set is
  `ho-kill-head-extra-assign`, `ho-kill-head-nonbare`, `ho-kill-vector-arm-swap`,
  `ho-kill-vector-count-field-swap`, `ho-kill-vector-fail-exit-swap`,
  `ho-kill-vector-fail-threshold`, `ho-kill-vector-setup-arm-skip`,
  `ho-kill-vector-setup-threshold` (all 14 sealed JSONs read from the sealed dir; only `count-field-swap` mentions
  `nlegs`, and it swaps printf arguments, a different class the sweep kills). **No sealed copy is an
  `nlegs`-formula recompute**, so the deciding run is untouched and this seat does not overturn it.
* What is proven: the frozen tool accepts six behaviour-bearing, amendment-6-valid must-kill copies.
  If such a copy reaches a future sealed set, C1-style claims fail. That is a coverage finding for
  round 35, not permission to change the contract or the frozen pin.

## Smallest safe correction (recommendation only; nothing edited)

1. **Form-based (cheapest, kills all 14).** The reference block never assigns `nlegs` after its
   `local nlegs=N` declaration. Extend `check_static` (`tool.py:344-359`) to fail a tally block that
   assigns `nlegs` after the declaration (`^[ \t]*nlegs=` / `(( nlegs` / `nlegs=` in arithmetic).
   Conservative and exact: it refuses a recompute form regardless of the status alphabet or arity,
   with no vector growth. False-reject risk is limited to a legitimate recompute, which no measured
   runner has.
2. **Vector-based, if the sweep is preferred.** The complement dimension is 244 statuses wide —
   a single added pair closes nothing (this seat's five out-of-alphabet survivors use four
   different statuses and one self-pair). Exhaustive closure over 255 statuses at 36 position pairs
   is 2.34 M vectors/config (infeasible at the current ~6 s budget); a defensible sample would be
   all 256 self-pairs per position pair (9 216 vectors, ≈ ×2.2 runtime) plus every non-CO status
   paired with each of `{0,1,2,3,5,7,8,9,120,126,127,128,200,255}` (244 × 14 × 36 = 122 976,
   ≈ ×16). Arity ≥3 must be added deliberately (84 position triples × a status alphabet) or
   excluded by the form check in (1).
3. Do not widen the alphabet by one observed value alone; the survivors show the escape surface is
   the whole complement, and arity is orthogonal to it.

## Bounds, restoration and evidence inventory

* Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ResidueNlegsAllPairs/` — `tool.py`, `pristine.sh`,
  `counter.py`, `probe/` (counter import layout), `mut/` (14 mutant copies), `out/` (receipts and
  logs), `probe_run.py`, `probe_add.py`, `validity.py`. `du -sh` 174 MB; `/fast` 21 GB free.
* Restoration: `pristine.sh` re-hashed after all runs — `a7d3f2dd…2eb9`, identical to the pin;
  `tool.py` — `7b11ba25…8d10`, identical to the pin; the fleet artifacts re-hashed after the sweep
  (`tools/tally-audit-v2.py`, `tools/mutate-and-run.sh`, `c1-measure.py`) — all three pin-equal.
  Mutants exist only as separate files; nothing was edited in place. The lane checkout is clean
  (`git status --porcelain` empty).
* No git/jj write command, no `MANIFEST.json`/`templates/`/`scripts/`/`.ufo/state/`/watchdog touch,
  no sibling repo, no process killed, no tool install or upgrade (host python3/bash/awk/sed/git/bwrap
  sufficed), no counter default-mode run.
* Evidence pointers:
  `out/receipts.json` (battery 1: 11 mutants, panel facts, sandbox outcomes),
  `out/receipts-add.json` (battery 2: 3 mutants + sum-formula stress witnesses),
  `out/validity.json` + `out/validity.log` (all six survivors valid must-kill under amendment 6),
  `out/panel-invariants.json` (measured `n=7561`, `max_nonzero_when_nonCO=1`,
  `max_nonzero_when_ge3=2`, `two_nonzero_statuses` = the 12-status alphabet),
  `out/probe.log` + `out/probe.rc`=0, `out/probe-add.log` + `out/probe-add.rc`=0,
  `out/pristine.tool.txt`/`.rc`=0, `mut/*.sh` (14 files; sha256 per mutant in the two receipts
  files — e.g. `nl-status-pair-6` `a28061d1…d28e`, `nl-triple-in-CO` `392d4e3a…2162`),
  `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (sha `3e28149f…b05c`).
