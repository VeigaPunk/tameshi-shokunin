# Seat ResidueNonzeroLegStress — round-34 w1 (v2, build+attack)

Measurement-only seat. Claim under attack: C1 (operability capability acquisition,
`tools/tally-audit-v2.py`) MEASURED TRUE at `c17e593b51802dd4ed568da3265f21c6d00c4273`, receipt:
`C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18
v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1
seed=685f63bd25263908 rev=c17e593b… C1_R33_PASS=true`, exit 0
(`.ufo/evidence/round-34/measure/c1-deciding-run.{exit,stdout}`).
Lane tip at dispatch: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

**Verdict in one paragraph.** The 2304-vector pair battery was built and validated (pristine agrees
with the tool's oracle on 0/2304 mismatches), then six block faults were spliced into runner copies
and run through both detectors. **Three faults survive the frozen tool** — `pair-status6-masked`
(F1), `triple-status9-dedupe` and `triple-mixed-collapse` (F2) — and **all three are admitted by
the gate with a valid witness**, so each is a witness-admissible v2 miss, not just a contrived
divergence. The two independent bounds are: (a) a second non-zero leg whose status is outside the
tool's 12-value `CO` set (243 of 255 non-zero statuses are never paired), and (b) three
simultaneously non-zero legs with any status outside `{1,2}` (all 64 of the tool's ≥3-leg vectors
use only 1/2). A sixth fault that changes only the second stdout line survives both by comparison
surface and is correctly not gate-admissible. The landed C1 measurement is not contradicted: none
of these classes is in the sealed set (whose six kill witnesses are all single-status vectors),
so `ho_kill=8/8` stands as measured for that set.

No frozen artifact was edited. The tool and runner are byte-pinned and re-hashed before and after
(§7). All work is under `/fast/scratch/hyaku/tameshi-r34-seats/ResidueNonzeroLegStress/`
(abbreviated `$S` below); the lane clone is read-only and ended clean (`git status --porcelain`
0 lines).

## 1. Pins verified at the tip (before any run)

```
$ mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ResidueNonzeroLegStress
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/lane                     # rc 0  ($S/clone.rc)
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C $S/lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                   # rc 0  ($S/checkout.rc)
$ env … git -C $S/lane rev-parse HEAD
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
$ env … git -C $S/lane show 0b99d48e…:tools/tally-audit-v2.py  > $S/tool.py    # rc 0  ($S/tool.rc)
$ env … git -C $S/lane show 0b99d48e…:tools/mutate-and-run.sh  > $S/pristine.sh# rc 0  ($S/runner.rc)
$ sha256sum $S/tool.py $S/pristine.sh
  7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Counter pin (amended rev, module used by import only — the default-mode kill rule was never run):

```
$ sha256sum $S/lane/.ufo/evidence/round-33/c1/c1-measure.py
  f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c
$ env … git -C $S/lane show 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum
  f6b8868c…a07f28c        (identical)
```

The runner's tally block is byte-identical to the tool's own `REF_BLOCK` and its leg names equal
`REF_NAMES` (checked in-process; `tool.regression_body` → `tool.tally_block`), so a fault spliced
into the block is the same text the tool splices into its own fault panel at the reference point.

## 2. Battery and detectors

Battery (the r33-seats stress shape, exactly as tasked): every unordered position pair
`(a,b)`, `a<b`, over 9 legs × every **ordered** status pair over `S = {3,4,5,7,9,120,126,127}`

```
C(9,2) × 8 × 8 = 36 × 64 = 2304 witness vectors   ($S/measure.py: battery())
```

Two bounded behavioral detectors, both run on pristine, mutated and restored bytes:

* **GATE** = the counter's own admission predicate, `c1-measure.block_run(block, vector, work)`
  compared pristine vs mutant for one length-9 vector, i.e. exactly what
  `ho_witness_ok({'set':'kill','witness':{'kind':'vector','vector':v}}, …)` computes
  (`block_run` returns `(rc, stdout first line)`; a kill witness needs `a != b` and
  `pb != mb`). Sweeping the 2304-vector battery with this predicate is the measure of what a
  pair-witness battery can admit.
* **TOOL** = frozen `tally-audit-v2.py` run on a runner copy with the fault spliced into the
  tally block, executed through the counter's own sandbox helper
  `c1-measure.run_tool_sandboxed` (bwrap, `--unshare-all`, `timeout 600`), and cross-checked by a
  second identical run that keeps the full stdout (`$S/measure.py: run_tool_full`). Verdict =
  `KILL` iff rc 1 + last line `TALLY_AUDIT: FAIL…`, `ACCEPT` iff rc 0 + `TALLY_AUDIT: PASS…`.

Baseline (pristine bytes, before any mutant):

```
$ cd $S && python3 measure.py     # rc 0 ($S/measure.rc); 204.8 s; $S/measure.log; $S/results.json
battery vectors=2304 statuses=[3, 4, 5, 7, 9, 120, 126, 127]
BASELINE pristine-vs-oracle mismatched=0/2304
CONTROL pristine tool rc=0 outcome=ACCEPT counter_helper=('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
```

Zero baseline mismatches against the tool's independent `oracle()` on all 2304 vectors is the
precondition for using this battery as a witness set: `pristine` is correct on every vector the
battery contains, so a pristine-vs-mutant divergence on any of them is a real defect.

## 3. What each detector can see (reconstructed from the tool's own source, executed)

`$S/coverage.py` (rc 0, output verbatim):

```
tool vectors per config = 7561 (expected 7561)
battery vectors = 2304
battery subset of tool vectors = True (missing 0)
tool vectors with >=3 non-zero legs = 64
tool vectors with >=3 non-zero legs AND any status not in {1,2} = 0
tool vectors with >=2 non-zero legs AND any status outside CO = 0
tool vectors containing status 6 at all = 9
tool vectors with status 6 plus any other non-zero leg = 0
statuses 1..255 never paired with a second non-zero leg: 243 values
  first 24: [6, 8, 10, 11, …, 31]          last 6: [249, …, 254]
```

with `CO = (1,2,3,4,5,7,9,120,126,127,128,255)` (`tool.py: check_runtime`), and 7561×2 configs +
36 operand-stress runs = the 15158 the control CHECK reports. Two consequences are load-bearing:

1. **The assigned battery is a strict subset of the tool's vector set** (2304 ⊂ 7561, 0 missing).
   Since pristine equals the tool's oracle on all 2304, any fault the battery distinguishes is
   necessarily a fault the tool's runtime sweep also flags. A pair battery over `S` can confirm the
   tool, not out-run it. (§5, F0 and F2 are the empirical confirmation.)
2. The tool's own bounds are: **≥3 simultaneously non-zero legs only with statuses ∈ {1,2}**, and
   **a second non-zero leg only with a status ∈ CO** (243 of the 255 non-zero statuses never
   co-occur with another non-zero leg).

## 4. Fault panel — measured, one row per mutant

Each fault is a splice between the tally loop's `done` and the `if [[ $nfail -gt 0 ]]` guard, so
`head`/`static` see nothing (they stayed PASS in every audit) and only `runtime` can react. Loop
body, `local nlegs=9` line and operand list are asserted unchanged (`$S/measure.py: faults()`).
Mutant runner copies: `$S/runs/<name>.sh`; per-mutant hashes and raw outputs: `$S/results.json`.

| mutant | injected defect | sha256 (mutant runner) | battery diffs | gate admits | tool rc / line | verdict |
|---|---|---|---|---|---|---|
| `pair-visible` (control) | `js=7 && kagi=120` → one setup leg becomes a fail | `f71abbb8d11767a6eabe7d3d08433e5e93585ba022c6a7cc0c9b9690ea76e68f` | **1**/2304 | yes, `[7,120,0,…]` | **1** / `TALLY_AUDIT: FAIL (… runtime=fail …)` | KILLED (both) |
| `pair-status6-masked` | `roundgate=6` **and** `nsetup>=2` → one setup becomes a fail | `a5c9545eeedfeecf194b6f5e0b69551bbb3845ced80c8aac191d509c50a9e6cd` | **0**/2304 | yes, `[3,0,0,0,0,0,6,0,0]` | **0** / `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | **SURVIVED tool + battery** |
| `pair-128-255` | `mado=128 && claims=255` → one setup becomes a fail | `eaa16400a5165e7c93d4a9f0f06fe46359a403918072833e418fe4bf00f104da` | 0/2304 | yes, `[0,0,0,128,0,255,0,0,0]` | 1 / `TALLY_AUDIT: FAIL (… runtime=fail …)` | KILLED by tool, battery-blind |
| `triple-status9-dedupe` | `js=tsu=claims=9` → three setup legs become passes | `0df37c0e76d4f986d684a001e3e2e5cea2f41c195029188e906bc54c8da15799` | 0/2304 | yes, `[9,0,9,0,0,9,0,0,0]` | 0 / `TALLY_AUDIT: PASS (… runtime=pass …)` | **SURVIVED tool + battery** |
| `triple-mixed-collapse` | `nsetup>=3 && mado=5` → one setup becomes a pass | `e77c2776d9ed4b9b3ddaa27ab18f2229d350c2414a9d02a3c7270e6266d78c3f` | 0/2304 | yes, `[7,3,0,5,0,0,0,0,0]` | 0 / `TALLY_AUDIT: PASS (… runtime=pass …)` | **SURVIVED tool + battery** |
| `fail-workdir-wording` | FAIL path's 2nd line `(kept)` → `(retained)` | `3f49c8b4531a87f1beb08227d25e23d9d0fc5f0abe0025ef01eb7bb1706b6f91` | 0/2304 | **no** (`False,'vector'`, no witness exists) | 0 / `TALLY_AUDIT: PASS (… runtime=pass …)` | SURVIVED both detectors by surface |

Witness-level outputs (pristine vs mutant, `block_run` at the row's witness;
`$S/witness_evidence.json`, regenerated by the command in §6):

```
pair-visible          [7,120,0,…]        pristine (2,SETUP passed=7 cannot-verify=2) -> mutant (1,FAIL passed=7 failed=1 setup=1)
pair-status6-masked   [3,0,0,0,0,0,6,0,0] pristine (2,SETUP passed=7 cannot-verify=2) -> mutant (1,FAIL passed=7 failed=1 setup=1)
pair-128-255          [0,0,0,128,0,255,…] pristine (2,SETUP passed=7 cannot-verify=2) -> mutant (1,FAIL passed=7 failed=1 setup=1)
triple-status9-dedupe [9,0,9,0,0,9,0,0,0] pristine (2,SETUP passed=6 cannot-verify=3) -> mutant (0,PASS passed=9)
triple-mixed-collapse [7,3,0,5,0,0,0,0,0] pristine (2,SETUP passed=6 cannot-verify=3) -> mutant (2,SETUP passed=7 cannot-verify=2)
fail-workdir-wording  [1,0,0,0,0,0,0,0,0] pristine (1,FAIL passed=8 failed=1 setup=0) -> mutant (1,FAIL passed=8 failed=1 setup=0)
```

## 5. Findings

### F1 (primary) — a two-leg fault keyed on any status outside `CO` evades the tool; an admissible witness exists

`pair-status6-masked` turns one unverifiable leg into a failure whenever the roundgate leg
returned exit 6 and any second leg is non-zero. It is a genuine behavior change — at witness
`[3,0,0,0,0,0,6,0,0]` the pristine block says
`SETUP (cases=9 passed=7 cannot-verify=2)` (exit 2) and the mutant says
`FAIL (cases=9 passed=7 failed=1 setup=1)` (exit 1). The admission gate accepts it
(`ho_witness_ok` → `(True,'vector')`, i.e. `pb != mb` and `a != b`), so an authored must-kill of
this shape would enter the sealed set. The frozen tool nevertheless returns
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, exit 0
(`$S/witness_evidence.json`; audit log in `$S/runs/audit-pair-status6-masked`), because:

* status 6 appears in the tool's vectors only in single-position sweeps, where no second leg is
  non-zero (`nsetup=1`, the `nsetup>=2` guard is not reached) — §3, line 8;
* its 5184-vector co-occurrence sweep draws both statuses from the fixed 12-value `CO`, so a
  status outside it is never combined with a second non-zero leg — §3, line 6.

Scope of the class: **243 of the 255 non-zero statuses** are never paired with another non-zero
leg in the tool's runtime sweep. The assigned battery shares the same blindness for its own
reasons: `S ∩ {6} = ∅`. This is the round-34 wave's stated target class ("nonzero-leg stress")
landing as a real, witness-admissible v2 miss.

### F2 — a fault needing three simultaneous non-zero legs evades the tool, also with an admissible witness

`triple-status9-dedupe` collapses three status-9 legs into passes: at
`[9,0,9,0,0,9,0,0,0]` pristine is `SETUP (cases=9 passed=6 cannot-verify=3)` exit 2 and the mutant
is `PASS (cases=9 passed=9 …)` exit 0 — a three-leg "skips that turn SETUP into PASS", the class
the tool's docstring says the co-occurrence vectors were added for. The gate admits it
(`(True,'vector')`); the tool returns `TALLY_AUDIT: PASS`, exit 0. Cause: the tool's only
multi-leg vectors use statuses 1 and 2 for every non-zero leg (64 vectors with ≥3 non-zero legs,
0 of them containing a status outside {1,2} — §3 lines 4–5); the pair sweep never has three
non-zero legs. `triple-mixed-collapse` (status-keyed **and** count-keyed) reproduces the same
miss with a second shape, so the bound is "≥3 non-zero unusual legs", not one contrived text
pattern.

### F3 — the assigned battery is weaker than the tool, and cannot itself discover a tool miss

`pair-128-255` (statuses inside `CO`, outside `S`) is battery-blind (0/2304) but the tool kills it
(`runtime=fail`, 2 mismatches — one per config). Together with §3(1): a fault the pair battery
distinguishes is necessarily tool-visible, so the battery's operative value is as an **admission
witness** stress (what the gate will accept), not as a tool-finder. `pair-visible` is the positive
control that the battery is capable of killing at all (1 distinguishing vector of 2304, tool
`runtime=fail`).

### F4 — shared observation surface: only `rc` + the first stdout line are compared

`fail-workdir-wording` changes the FAIL path's second line from `REGRESSION_WORKDIR: %s (kept)` to
`(retained)`. Both detectors read `(rc, first stdout line)` (`c1-measure.block_run`;
`tool.run_vectors` uses `${out%%$'\n'*}`, `tool.py: check_runtime`/`run_vectors`), so no witness
vector can distinguish it: the gate correctly refuses it (`(False,'vector')`), and the tool
`ACCEPT`s. This is not a held-out miss (nothing could be admitted as a kill through it) but it is
a real behavior change — the runner's stated workdir disposition (line 141 of `mutate-and-run.sh`)
— outside both comparison surfaces. Routes naturally to the r34 Holds item "whole-stdout
comparison".

### F5 — context: the deciding run never exercised co-occurrence

All six sealed kill witnesses are single-status vectors:
`ho-kill-vector-arm-swap/-count-field-swap/-fail-exit-swap/-fail-threshold` use `[1,0,…]` and
`ho-kill-vector-setup-arm-skip/-setup-threshold` use `[2,0,…]`
(`.ufo/evidence/round-33/heldout/*.json`, witness field). The receiving gate admitted them, and v2
killed all eight. That is consistent with the receipt (`ho_kill=8/8`) but it is not evidence that
v2 covers pair or three-leg co-occurrence; F1/F2 show it does not. This does not contradict the
landed measurement: the sealed set was frozen before data and contains no copy of these classes.

## 6. Reproducing commands

```
$ cd /fast/scratch/hyaku/tameshi-r34-seats/ResidueNonzeroLegStress
$ python3 measure.py        # rc 0; rebuilds battery + all 6 mutants; writes results.json (204.8 s)
$ python3 coverage.py       # rc 0; vector-set reconstruction and gap counts (§3)
$ python3 tool.py --runner runs/pair-status6-masked.sh ; echo $?   # -> TALLY_AUDIT: PASS …, 0
$ python3 tool.py --runner runs/triple-status9-dedupe.sh ; echo $? # -> TALLY_AUDIT: PASS …, 0
$ python3 tool.py --runner runs/pair-visible.sh ; echo $?          # -> TALLY_AUDIT: FAIL …, 1
$ python3 tool.py --runner runs/pair-128-255.sh ; echo $?          # -> TALLY_AUDIT: FAIL …, 1
```

(Each `--runner` command above was executed directly with the same exit codes as the sandboxed
counter helper; both verdicts are recorded per mutant in `results.json` fields `tool_rc`,
`tool_outcome`, `tool_counter_helper`. The direct invocation is a convenience reproduction; the
sandboxed run is the authoritative detector.)

## 7. Restoration evidence and read-only guarantees

Pristine → mutated → restored cycle on one byte copy (`$S/restore/`, `$S/restore/restore.json`),
detector run at each step:

| step | sha256 of the runner copy | tool | gate at `[9,0,9,0,0,9,0,0,0]` |
|---|---|---|---|
| pristine | `a7d3f2dd…12eb9` | ACCEPT rc 0 (run twice) | `(False,'block-identical')` |
| mutated (`triple-status9-dedupe`) | `0df37c0e76d4f986…15799` | ACCEPT rc 0 (run twice) | `(True,'vector')` |
| restored | `a7d3f2dd…12eb9` | ACCEPT rc 0 (run twice) | `(False,'block-identical')` |

`restored_exact=True`. End state of every pinned file:

```
$ sha256sum $S/tool.py $S/pristine.sh $S/lane/tools/tally-audit-v2.py $S/lane/tools/mutate-and-run.sh
  7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
  7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  lane/tools/tally-audit-v2.py
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
$ env … git -C $S/lane status --porcelain | wc -l
  0
```

`measure.py` records `hashes_before == hashes_after` for `tool.py`/`pristine.sh`
(`results.json: restored_exact=true`). The lane was never written; no git/jj write command was
run anywhere; the tool was never edited (measurement-only seat; the v3 residue classes stay
Holds).

## 8. Tooling

No install or upgrade was performed (no `pacman`, `uv`, `npx`, `cargo`, no binary fetched); the
host pacman guard was not touched. Only existing host tools were used: `python3`, `bwrap 0.13.1`,
`git` (read-only verbs), `sha256sum`.

## 9. Artefacts (scratch, disposable)

`$S/measure.py`, `$S/coverage.py`, `$S/measure.log`+`measure.rc`, `$S/results.json`,
`$S/witness_evidence.json`, `$S/runs/*.sh` (six mutant runners + audit logs),
`$S/restore/restore.json`+`demo.sh`, `$S/lane/` (detached clone at `0b99d48e`).
