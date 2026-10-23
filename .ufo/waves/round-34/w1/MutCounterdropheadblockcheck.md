# MutCounterdropheadblockcheck — round 34 w1 mutation probe

Seat: `tameshi-r34-w1-MutCounterdropheadblockcheck` (mutation tester, leaf).
Claim under attack: **C1** (operability capability acquisition, `tools/tally-audit-v2.py`), receipt
`C1_R33_PASS=true` at rev `c17e593b51802dd4ed568da3265f21c6d00c4273`
(`.ufo/evidence/round-34/measure/`). Lane tip at dispatch `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropheadblockcheck/` (all writes there,
plus this one report). Tool installs: **none** (bwrap 0.13.1, Python 3.14.8 already present; no
pacman/uv/npx channel used).

## Pins verified before any run

| artifact | path (lane) | sha256 |
|---|---|---|
| tool | `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` = pin |
| runner | `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` = pin |
| counter (amendment 6) | `.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` = pin |
| controls receipt | `.ufo/evidence/round-33/c1/controls-receipt.json` | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` |

Lane was cloned scratch-internally and detached at the dispatch tip; `git -C lane rev-parse HEAD` =
`0b99d48e…f68b7` (`out/lane-head.txt`), `git -C lane status --porcelain` empty (`out/lane-status-final.txt`,
0 lines, rc 0). Lane stayed read-only throughout (source of all extractions: `git show`).

## Mutation (the counter's head branch, not the tool)

Frozen counter lines 195–196 of `.ufo/evidence/round-33/c1/c1-measure.py` (`grep -n` in lane):

```
195:        if mb != pb:
196:            return False, 'head-with-block-edit'
```

Mutant = those two lines deleted and nothing else (`out/mutant.diff`; `diff` rc 1 = difference):

```
--- mut-pristine/.../c1-measure.py
+++ mutant/.../c1-measure.py
@@ -192,8 +192,6 @@
     if w.get('kind') == 'head':
         if head_of(mutated) == head_of(pristine):
             return False, 'head'
-        if mb != pb:
-            return False, 'head-with-block-edit'
         if ho['set'] == 'kill':
```

| bytes | sha256 |
|---|---|
| pristine counter copy | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` |
| **mutant** counter | `70d2966933118d60817d158386310c9199021cbaa01ca4b89f065a9b37663176` |
| restored counter (after probe) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` |

## Detector: 8-case probe battery

Committed expectation set: `.ufo/evidence/round-34/dev/witness-probes.json` (8 names + expected
`(bool, reason)`); committed transcript `witness-probes.stdout` shows the pristine counter at 8/8.
The authoring driver itself is **not committed** (fleet-wide search for the probe ids returns only
those two files), so I rebuilt the eight mutated runners from `pristine.sh` and graded
`ho_witness_ok`. Reconstruction is validated by the fact that the pristine counter reproduces the
committed transcript **exactly, 8/8**, on the same expected tuples.

Probe constructions (`probes.py`, applied with the counter's own `apply_edits`):

| probe | set | edits | witness |
|---|---|---|---|
| Q1-comment-accept | accept | comment inserted after the tally START | vector `[0,1,2,0,1,2,0,1,2]` |
| Q3-inert-head-kill | kill | `VERSION='…'` → `'… probe'` | head |
| Q3b-ridealong-accept | accept | VERSION rename + guard `!= nlegs` → `< nlegs` | head |
| K-extra-leg-assign-kill | kill | second `st_js=$?` line after the first | head |
| K-nonbare-leg-kill | kill | `st_kagi=$?` → `st_kagi=$(($?))` | head |
| A-inert-head-accept | accept | `VERSION` rename | head |
| A-head-with-block | accept | `VERSION` rename + block comment | head |
| KV-block-identical | kill | `VERSION` rename (block untouched) | vector `[0,1,2,0,1,2,0,1,2]` |

Detector command (identical for all three byte states):
`PYTHONDONTWRITEBYTECODE=1 python3 probes.py <counter> pristine.sh <workdir> lane/.ufo/evidence/round-34/dev/witness-probes.json`

## Runs and actual output

1. **Pristine** — counter sha `f6b8868c…`, `out/pristine-battery.stdout`, rc `0` (`out/pristine-battery.rc`):

```
Q1-comment-accept -> (True, 'vector-equivalence')  MATCH
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')  MATCH
Q3b-ridealong-accept -> (False, 'head-with-block-edit')  MATCH
K-extra-leg-assign-kill -> (True, 'head-leg-assignment')  MATCH
K-nonbare-leg-kill -> (True, 'head-leg-assignment')  MATCH
A-inert-head-accept -> (True, 'head')  MATCH
A-head-with-block -> (False, 'head-with-block-edit')  MATCH
KV-block-identical -> (False, 'block-identical')  MATCH
BATTERY: 8/8 exact; flips=none
```

2. **Mutant** — counter sha `70d29669…`, `out/mutant-battery.stdout`, rc `0` (`out/mutant-battery.rc`):

```
Q1-comment-accept -> (True, 'vector-equivalence')  MATCH
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')  MATCH
Q3b-ridealong-accept -> (True, 'head')  FLIP (expected (False, 'head-with-block-edit'))
K-extra-leg-assign-kill -> (True, 'head-leg-assignment')  MATCH
K-nonbare-leg-kill -> (True, 'head-leg-assignment')  MATCH
A-inert-head-accept -> (True, 'head')  MATCH
A-head-with-block -> (True, 'head')  FLIP (expected (False, 'head-with-block-edit'))
KV-block-identical -> (False, 'block-identical')  MATCH
BATTERY: 6/8 exact; flips=Q3b-ridealong-accept,A-head-with-block
```

3. **Restored** — bytes copied back from the pristine copy; sha `f6b8868c…` (`out/restored-sha.txt`),
   `out/restored-battery.stdout`, rc `0` (`out/restored-battery.rc`): **8/8 exact, flips=none**,
   i.e. identical to run 1. Restoration is byte-exact against the pin, not just behaviorally.

## Verdict

**Killed by the probe battery (2/8 verdict flips), not a no-op mutant and not a surviving
semantics hole in the battery.** Removing the `mb != pb` refusal makes the amended witness gate
label an `accept` + `kind=head` copy carrying a **lethal tally-block edit** as a valid must-accept
(`(True, 'head')`), where the frozen rule demands `(False, 'head-with-block-edit')`. Both probes
that exercise the refusal flip; every other probe is unchanged. (The counter's own comment still
claims the refusal — lines 188–189, “is refused” — so the mutant is also a silent
comment/code divergence.)

**Coverage finding (sealed data):** the removed branch is unreachable on the committed held-out
set, so the mutant is *dormant* on the deciding data. Parity run (`impact2.py`,
`out/impact2.stdout`, rc 0) over all 14 sealed JSON copies: `same=14 diff=0`. The two committed
`accept`+`head` copies (`ho-accept-head-comment`, `ho-accept-head-version-rename`) both have
`block_identical=True`; `accept+head copies with block edit (refusal-reachable): 0`
(`out/ridedemo.stdout`). The probe battery is the only committed cover for this branch.

## Could the mutant have voided or falsely passed C1?

**Voided: yes — demonstrated.** Counterfactual copy `counterfactual-accept-head-ridealong`
(accept, `kind=head`, benign `VERSION` rename + lethal guard `!=` → `<`; bytes sha
`258e3be6e02786ccc2b6be3b0c0922830d04cfb1d900524a3949ce73cfa4d73e`), executed via
`ridedemo.py` (`out/ridedemo.stdout`, rc 0):

```
pristine_gate: (False, 'head-with-block-edit')      # correctly refused as invalid
mutant_gate:   (True, 'head')                       # admitted as a valid must-accept
tool_on_ridealong: ('KILL', 1, 'TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)')
```

A gate-clean author using the mutant witness rule could therefore seal a lethal ride-along as
`accept`; the pinned, sound tool correctly KILLs it → `ho_accept` miss → `C1_R33_PASS=false` with
a blameless tool. That is claim voiding, not a tool defect. It cannot void the *landed* run,
because no such copy exists in `.ufo/evidence/round-33/heldout/` (parity above).

**Falsely passed: no demonstrated route.** The removal only widens admission in the `kind=head`
branch; it never relaxes scoring. The kill-side widening (`kill` + head + block edit that *does*
touch a leg-assignment line) was executed: `counterfactual-kill-head-ridealong` (sha
`7ec6e5ec127bc20f833487a8f05fea6cc8c86d276fb5ac2de6808587fa57e7d9`) → mutant gate
`(True, 'head-leg-assignment')`, tool `('KILL', 1, 'TALLY_AUDIT: FAIL (head=fail static=fail
runtime=fail harness=fail)')` (`out/impact2.stdout`). The only widened accept class is
`accept`+head+block edit, which is exactly the voiding direction above; a widened accept that is
behaviorally equivalent is still legitimately acceptable. No configuration was found where the
mutant gate admits a defective copy that the pinned tool PASSes.

## Reproduction

```
S=/fast/scratch/hyaku/tameshi-r34-seats/MutCounterdropheadblockcheck
cd $S
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py        # sha 7b11ba25…
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh      # sha a7d3f2dd…
cp lane/.ufo/evidence/round-33/c1/c1-measure.py mut-pristine/.ufo/evidence/round-33/c1/c1-measure.py # sha f6b8868c…
# mutation: delete lines `if mb != pb:` / `return False, 'head-with-block-edit'` (differences in out/mutant.diff)
PYTHONDONTWRITEBYTECODE=1 python3 probes.py mut-pristine/.ufo/evidence/round-33/c1/c1-measure.py pristine.sh out/work-pristine lane/.ufo/evidence/round-34/dev/witness-probes.json; echo $? > out/pristine-battery.rc
PYTHONDONTWRITEBYTECODE=1 python3 probes.py mutant/.ufo/evidence/round-33/c1/c1-measure.py pristine.sh out/work-mutant lane/.ufo/evidence/round-34/dev/witness-probes.json; echo $? > out/mutant-battery.rc
cp mut-pristine/.ufo/evidence/round-33/c1/c1-measure.py mut/.ufo/evidence/round-33/c1/c1-measure.py; echo $? > out/restore.rc
PYTHONDONTWRITEBYTECODE=1 python3 probes.py mut/.ufo/evidence/round-33/c1/c1-measure.py pristine.sh out/work-restored lane/.ufo/evidence/round-34/dev/witness-probes.json; echo $? > out/restored-battery.rc
PYTHONDONTWRITEBYTECODE=1 python3 ridedemo.py > out/ridedemo.stdout 2> out/ridedemo.stderr; echo $? > out/ridedemo.rc
PYTHONDONTWRITEBYTECODE=1 python3 impact2.py  > out/impact2.stdout  2> out/impact2.stderr;  echo $? > out/impact2.rc
```

All six rc files contain `0`; the tool verdict `KILL rc=1` is the sandboxed tool's own exit,
carried inside `ridedemo`/`impact2` output. No default-mode counter run, no `--write-controls`, no
`--then-regression`, no git/jj write command anywhere; the lane checkout reports clean.

## Evidence files (scratch)

`probes.py`, `ridedemo.py`, `impact2.py`, `out/{pristine,mutant,restored}-battery.{stdout,stderr,rc}`,
`out/mutant.diff`, `out/{ridedemo,impact2}.{stdout,stderr,rc}`, `out/counter-shas.txt`,
`out/restored-sha.txt`, `out/lane-head.txt`, `out/lane-status-final.txt`, `out/lane-pins-final.txt`,
`out/ridealong.sh`, `out/kill-ridealong.sh`.

*Session attribution: executed by `tameshi-r34-w1-MutCounterdropheadblockcheck`; scratch-only writes.*
