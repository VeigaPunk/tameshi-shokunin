# Mutkillheadnonbare — round 34 w1 mutation probe

Seat: `tameshi-r34-w1-Mutkillheadnonbare` (mutation tester, leaf; no subagent dispatch).
Claim under attack: **C1** (operability capability acquisition, `tools/tally-audit-v2.py`), receipt
`C1_R33_PASS=true` at rev `c17e593b51802dd4ed568da3265f21c6d00c4273`
(`.ufo/evidence/round-34/measure/`). Lane tip at dispatch `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/Mutkillheadnonbare/` (all writes there, plus this one
report). Tool installs: **none** (bwrap 0.13.1, Python 3.14.8 already present; no pacman/uv/npx used).
Lane stayed read-only; source of every extraction was `git show` on the scratch clone.

## Pins verified before any run

| artifact | lane path | sha256 |
|---|---|---|
| tool | `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` = pin |
| runner | `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` = pin |
| counter (amendment 6) | `.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` = pin |
| sealed copy attacked | `.ufo/evidence/round-33/heldout/ho-kill-head-nonbare.json` | `32c69340eda67f57f7a2a624fb37685620dc4fef34c44937d30122189918b648` |

Clone/checkout: `clone=0 checkout=0`, `git -C lane rev-parse HEAD` = `0b99d48e…f68b7`
(`clone.rc`, `checkout.rc`, `head.txt` in scratch). Extractions `git show
0b99d48e…:tools/tally-audit-v2.py > tool.py` and `…:tools/mutate-and-run.sh > pristine.sh` both rc 0;
recomputed shas equal the pins (`sha256sum tool.py pristine.sh`, rc 0). The lane clone's counter and
sealed copy hash to the same pins as the fleet copies (`sha256sum` on both, rc 0).

## Assigned probe — `ho-kill-head-nonbare` (set=kill)

Mutation is the JSON's single edit, applied with the counter's own `apply_edits` (exactly-once
enforced): `  st_claims=$?\n` → `  st_claims=0\n` at runner line 1415, inside `run_regression`
before the tally block. Bytes: `evidence/ho-kill-head-nonbare.sh`, sha256
`bafb6e0de34b01d0d791f4812074fb95295667dd6046337b6bc238c2e6e3ebd9`.

Witness gate (counter `ho_witness_ok`, amendment 6): **`(True, 'head-leg-assignment')`** — block is
byte-identical, head differs, A-set differs (`st_claims` loses its bare `=$?` line). This is the
envelope the deciding run scored as a kill hit (receipt `ho_kill=8/8 ho_invalid=0`); no conflict.

Detector (the REAL tool, through the counter's `run_tool_sandboxed`; bwrap argv per
`c1-measure.py:223-263`), command:
`python3 probe_one.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/heldout/ho-kill-head-nonbare.json`
→ rc 0 (`evidence/sealed.rc`); record `evidence/sealed.result.json`, full tool stdout
`evidence/ho-kill-head-nonbare.stdout`:

```
tool_outcome=KILL  rc=1
TALLY_AUDIT: FAIL (head=fail static=fail runtime=fail harness=fail)
CHECK head FAIL legs=8; non-bare leg assignment(s) in the head: st_claims=0
CHECK static FAIL legs=8 operands=9 nlegs=9; loop operands != legs (missing -; miscounted ['st_claims']); nlegs=9 but 8 legs assigned
CHECK runtime FAIL tally loop operands ['st_claims'] have no leg assignment in the head
CHECK harness FAIL leg names differ from the reference panel (…)
```

**Verdict: KILLED** — label satisfied (rc 1, `TALLY_AUDIT: FAIL`). Note the kill is even
over-determined: dropping the bare line shrinks `names` to 8, so static/runtime/harness also fail;
the head check independently names `st_claims=0` as a non-bare leg assignment.
Priming baseline on pristine bytes through the same detector: `ACCEPT`, rc 0,
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`
(`work/base.sh`, sha `a7d3f2dd…`, `evidence/adv_batch.out` first record).

## Adversarial probe — same family, different construction

Detector identical for every row (`run_tool_sandboxed` on the exact mutant bytes); witness column is
the counter's `ho_witness_ok` on the same bytes. All four case runs (plus the baseline) rc 0
(`evidence/adv.rc`, `probe_base_sealed.rc`, `probe_adv.rc`, `evidence/adv_batch.rc`).

| case | edit(s) after `st_claims=$?` | mutant sha256 | witness | tool |
|---|---|---|---|---|
| `decoy` | `  st_decoy =0` | `96b50e73…995e7cd` | **(True, head-leg-assignment)** | **ACCEPT rc 0** |
| `mask` | `  n=claims; printf -v "st_$n" 0` | `dcadf0f0…bd2d78e` | (False, head-edit-cannot-kill) | **ACCEPT rc 0** |
| `decoy_mask` | both lines (order: decoy, mask) | `37165adf…497d7efc` | **(True, head-leg-assignment)** | **ACCEPT rc 0** |
| `legspaced` | drop ` st_claims` from the `local` declaration + `  st_claims =0` | `9c6bc007…cf93ce5` | **(True, head-leg-assignment)** | **ACCEPT rc 0** |

Witness-set instrumentation (`evidence/witness_sets.out`): pristine A = X = the nine leg names;
`decoy`/`decoy_mask` differ in X only by `st_decoy`; `mask` has A and X *identical*; `legspaced` has
X = nine names + a second `st_claims`.

### Critical finding — witness-valid kill that the tool passes

Exact JSON written at `evidence/adv-kill-head-indirect-mask.json` (mutant bytes
`evidence/adv-kill-head-indirect-mask.sh`, sha `37165adff317ca08f5e0779d48c9b742aad66d913faeb3cf7d9d10c5497d7efc`;
`probe_one.py` → rc 0, `evidence/adv.result.json`, `evidence/adv-kill-head-indirect-mask.stdout`):

```json
{
 "id": "adv-kill-head-indirect-mask",
 "set": "kill",
 "edits": [
  {"old": "  st_claims=$?\n",
   "new": "  st_claims=$?\n  st_decoy =0\n  n=claims; printf -v \"st_$n\" 0\n"}
 ],
 "witness": {"kind": "head"}
}
```

* `validate_ho` = true; `ho_witness_ok` = **(True, 'head-leg-assignment')** — the amended gate
  certifies it as a must-kill.
* Tool: **ACCEPT**, rc 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`;
  `CHECK head PASS legs=9`, `CHECK static PASS legs=9 operands=9 nlegs=9`,
  `CHECK runtime PASS vectors=15158 mismatched=0`, `CHECK harness PASS reference cases=9; faults
  rejected=34/34`.
* The copy is genuinely lethal: `printf -v "st_$n"` resolves to `printf -v st_claims 0` and
  overwrites the leg-6 status after its bare capture; the mask line never spells `st_claims`, so
  every head scan misses it.

Behavioural proof on the mutant's exact bytes (`demo_exact.py` → `evidence/demo_exact.out`,
`evidence/demo_exact.rc`): mutant lines 1415–1417 verbatim plus the counter's own
`tally_block_of(mutated)` (bit-identical to pristine's block) under `bash`, with leg 6 forced to
status 1:

```
control (mask removed):     rc=1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
mutant (exact 3 lines):     rc=0  REGRESSION: PASS (cases=9 passed=9; ledger legs exact: …)
```

A failing leg is counted as pass. This is the `printf -v` masking class named at `tool.py:326-330`,
constructed with an assembled variable name so the literal never appears.

### Minimal witness-gate defect (independent of the tool)

`decoy` alone — the single inserted line `  st_decoy =0`, which bash executes as a *command
invocation* (`st_decoy: command not found`, rc 127; `st_decoy` stays unset — `demo_mask.sh` output in
`evidence/demo_mask.out`), is inert. Yet `ho_witness_ok` returns **(True, 'head-leg-assignment')** because
`c1-measure.py:203`'s `X = ^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*=` matches `st_decoy =0`, while the tool's
line-initial scans (`tool.py:309,316`) require the name to touch `=`. Bash has no space-around-`=`
assignment: every line X can see that the tool tolerates is a command invocation. So the amendment-6
"diff must touch the leg-assignment surface" test (`c1-measure.py:202-207`) is satisfiable by inert
text. `legspaced` corroborates a second path to the same effect (X gains a second `st_claims` while
the twice-only count stays 2 because the declaration occurrence was dropped).

### The mirror defect in the gate

`mask` alone — a real, lethal mask — is *rejected* by the gate as `(False,
'head-edit-cannot-kill')`, because name-indirection leaves A and X untouched. So the amended gate is
wrong in both directions on this family: it certifies inert decoys and refuses the true fault.

## Root cause and the shape of the hole

Tool PASS forces, simultaneously: every line-initial `st_*=` assignment is bare `$?`, each name once,
each of the nine names occurs exactly twice as a substring, the bare set equals the loop operands,
and the block equals the reference. Hence A is pinned to the nine names, and the only X-visible edit
the tool tolerates is a line `st_<name>` + whitespace + `=` — a shell *command invocation*, never an
assignment. The witness gate therefore cannot be satisfied by the fault's assignment syntax; it is
satisfied by command-invocation text — inert as written in `decoy`, or made to act only through the
same tool-invisible constructs (a helper defined earlier, or name indirection). The real fault rides
along invisibly (a name assembled at run time). The tool's own guarantee is falsified in the same
stroke: `tool.py:326-330` claims "any other occurrence (… printf -v, read, declare, …) … fails closed
here … substring counting catches them all", but `printf -v "st_$n"` contains no leg-name substring.
`check_runtime` only executes the tally block (`tool.py:372`), `check_harness` only extracts
`st_*=$?` lines and the block (`tool.py:496`, `tool.py:510`), and `check_head` is purely syntactic
over the head (`tool.py:307-340`) — no check executes or taints the head, which is where leg statuses
are captured.

Scope of the claim: **no landed number is contradicted.** The sealed 8-kill / 6-accept set is
untouched; every sealed copy scores as before (this seat's copy: KILL). What is proven is that the
tool's head check is incomplete for its own documented masking class, and that amendment 6 accepts a
witness-valid kill it cannot deliver. A kill held-out authored in this family would be scored a miss
by the tool while the gate would wave it through. Per the contract I report, not change it: closing
the hole needs either an executing/tainting head check or a rejection of name-assembling constructs
(`printf -v`, `eval`, `declare`, `read`, `export` with a quoted/concatenated name) in the head, and a
gate X that models bash assignment syntax rather than `st_* <ws> =`.

## Restoration evidence

Every mutant lives in scratch; `pristine.sh` was never edited and no lane/fleet file was touched.
After all probes: `sha256sum pristine.sh tool.py lane/.ufo/…/c1-measure.py` =
`a7d3f2dd…` / `7b11ba25…` / `f6b8868c…` (all equal the pins); `git -C lane status --porcelain`
prints nothing, rc 0; and the post-mutant baseline harness (`probe_adversary.py base`, first record
of `evidence/adv_batch.out`) re-runs the pristine bytes (sha `a7d3f2dd…`, the pin) to `ACCEPT`,
rc 0. Extraction and mutant hashes are stable before/after (`evidence/` inventory).

## Command ledger (exit codes captured as `cmd; echo $? > file`)

| # | command (scratch cwd) | rc | output |
|---|---|---|---|
| 1 | `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin lane` | 0 | `clone.rc` |
| 2 | `git -C lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` | 0 | `checkout.rc`, `head.txt` |
| 3 | `git show 0b99d48e…:tools/tally-audit-v2.py > tool.py` | 0 | sha = pin |
| 4 | `git show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh` | 0 | sha = pin |
| 5 | `python3 probe_adversary.py base sealed` | 0 | `probe_base_sealed.rc`; ACCEPT / KILL |
| 6 | `python3 probe_adversary.py decoy mask decoy_mask legspaced` | 0 | `probe_adv.rc` |
| 7 | `python3 probe_one.py evidence/adv-kill-head-indirect-mask.json` | 0 | `evidence/adv.rc`, `.result.json`, `.stdout` |
| 8 | `python3 probe_one.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/heldout/ho-kill-head-nonbare.json` | 0 | `evidence/sealed.rc`, `.result.json`, `.stdout` |
| 9 | `python3 demo_exact.py` | 0 | `evidence/demo_exact.out` (control FAIL vs mutant PASS) |
| 10 | `bash demo_mask.sh` | 0 | mask semantics: `st_claims=1→0`, nfail `1→0` |
| 11 | `python3 probe_adversary.py base decoy mask decoy_mask legspaced` | 0 | `evidence/adv_batch.rc`, `evidence/adv_batch.out` |
| 12 | `sha256sum pristine.sh tool.py lane/…/c1-measure.py`; `git -C lane status --porcelain` | 0 | pins unchanged; empty status |

Scratch evidence pointers: `evidence/adv.result.json`, `evidence/sealed.result.json`,
`evidence/adv-kill-head-indirect-mask.{json,sh,stdout}`, `evidence/ho-kill-head-nonbare.stdout`,
`evidence/witness_sets.out`, `evidence/demo_exact.out`, `work/{base,sealed,decoy,mask,decoy_mask,legspaced}.sh`.
Drivers: `probe_one.py`, `probe_adversary.py`, `demo_exact.py`, `demo_mask.sh` (all scratch-only).

*Session attribution: executed by `tameshi-r34-w1-Mutkillheadnonbare`; scratch-only writes plus this
report. Verdicts are observations; the deciding run stands.*
