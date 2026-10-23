# Mutacceptvectorarithspace — sealed accept copy `ho-accept-vector-arith-space`

Seat: mutation tester (v2 wave, round 34). Claim under attack: **C1** operability capability
acquisition (`tools/tally-audit-v2.py`) MEASURED TRUE at `c17e593b51802dd4ed568da3265f21c6d00c4273`
(receipt `.ufo/evidence/round-34/measure/c1-deciding-run.stdout`, exit 0). Lane tip at dispatch
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Scratch:
`/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorarithspace/`. The lane was read-only for
this seat; every write is a fresh copy under that scratch dir plus this one report.

## Verdict

1. **The copy's label holds.** On the counter's own path (JSON edits → mutated runner bytes →
   amended `ho_witness_ok` → real tool via `run_tool_sandboxed`) the copy validates
   `(True, 'vector-equivalence')` and the tool answers `ACCEPT rc=0
   TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` — the same tuple as the
   copy's authoring receipt row (`.ufo/evidence/round-34/dev/authoring-receipts.json`,
   `ho-accept-vector-arith-space`: witness `[true, 'vector-equivalence']`, tool
   `["ACCEPT", 0, "TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)"]`).
   Required outcome for `set=accept` met; **survived** (an accept copy is supposed to survive).
2. **Assigned fault family: no witness-valid/tool-killed construction exists.** Seven
   independently constructed family clones are witness-valid *and* tool-PASS (§4), and the
   mechanism proof in §5 shows why an inert arithmetic/whitespace edit cannot be killed.
3. **Critical finding — the amended witness gate, not the tool.** Three constructions derived
   from this copy validate under `ho_witness_ok` as `set=accept` while the real tool returns
   `TALLY_AUDIT: FAIL` (rc=1): two inside the same block region (tally `case` arms), one in the
   head. The tool is right on all three (each is a genuine defect); the gate is wrong to mint a
   must-accept label for them. Exact JSONs and reproductions in §6. Consequence: an accept copy
   authored this way would score `ho_a=5/6` with a blameless tool — precisely the failure mode
   amendment 6's rationale claims to remove (`corpus/knowledge/witness-equivalence-rule.md`).
   The deciding run itself is **not** refuted: its accept copies (this one included) are genuinely
   equivalent and the tool accepts them.

## 1. Pins verified before any run

| artifact | pin | observed | command / pointer |
|---|---|---|---|
| tool | `7b11ba25…8d10` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | `sha256sum tool.py` → `pins_actual.txt`, rc 0 |
| runner | `a7d3f2dd…2eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same, rc 0 |
| counter (imported, never run in default mode) | `f6b8868c…a07f28c` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `sha256sum lane/.ufo/evidence/round-33/c1/c1-measure.py`; blob at `c17e593b` hashes the same (`blob_counter_c17.txt`, rc 0) |
| sealed copy JSON | — | `3f8ad257fd11a1325ee3a3c47be73aecaf8395ee8bd2965b813697b80f2918dc` | `sha256sum …/heldout/ho-accept-vector-arith-space.json`; blob at `c17e593b` **and** at tip `0b99d48` hash identically (`blob_ho_c17.txt`, `blob_ho_tip.txt`, rc 0) — the attacked copy is the committed one |
| bwrap / interpreter | — | `/usr/bin/bwrap`, `/usr/bin/python3` (3.14.8) | `which bwrap; ls -l /usr/bin/python3` |

Setup commands (all exit 0, each captured with `cmd; echo $? > file`):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorarithspace
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorarithspace/lane   # clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C …/lane checkout -q --detach 0b99d48e…   # checkout.rc=0
git -C …/lane show 0b99d48e…:tools/tally-audit-v2.py > tool.py                                   # show_tool.rc=0
git -C …/lane show 0b99d48e…:tools/mutate-and-run.sh  > pristine.sh                              # show_sh.rc=0
```

## 2. Mutation derivation (the copy exactly as the counter builds it)

The copy's one edit targets the runner's tally `case` arms, `pristine.sh:1435-1437`; the old
string occurs **exactly once** in the pinned runner (byte 74223, line 1435) — `apply_edits`
(`.ufo/evidence/round-33/c1/c1-measure.py:131-136`) accepts it, and so did this seat's build
(asserted, script would have aborted otherwise).

```diff
--- pristine.sh
+++ mutant-sealed.sh          (106218 -> 106212 bytes, sha256 671a331dc99a9bbadfcc3497944a15da67d15e3621419f66a780645428691c10)
@@ -1432,9 +1432,9 @@
   local nlegs=9 npass=0 nfail=0 nsetup=0 st
   for st in "$st_js" … "$st_citecheck"; do
     case $st in
-      0) npass=$((npass + 1)) ;;
-      1) nfail=$((nfail + 1)) ;;
-      *) nsetup=$((nsetup + 1)) ;;
+      0) npass=$((npass+1)) ;;
+      1) nfail=$((nfail+1)) ;;
+      *) nsetup=$((nsetup+1)) ;;
     esac
   done
```

`diff -u pristine.sh mutant-sealed.sh` → rc 1 (differences, as expected); the read-only pins were
never touched (`restore_after.txt`: tool `7b11ba25…`, runner `a7d3f2dd…`).

## 3. Backbone run — real tool through the counter's boundary

`probe.py` (rc 0) imports the frozen counter as a module, calls `apply_edits`, `ho_witness_ok`
and `run_tool_sandboxed` (`.ufo/evidence/round-33/c1/c1-measure.py:131,184,234`). Actual output,
`probe.out`:

```
CONTROL pristine tool_outcome=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
SEALED apply_edits ok mutated_sha=671a331dc99a9bbadfcc3497944a15da67d15e3621419f66a780645428691c10 changed=True
SEALED witness=True kind=vector-equivalence tool_outcome=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Satisfies the accept predicate the counter scores (`score_tool`: `rc == 0 and last.startswith
('TALLY_AUDIT: PASS')`, `c1-measure.py:265-283`). **Verdict: survived / label correct.**

## 4. Family sweep — same fault family, seven different constructions

Every clone below was derived *from the sealed copy's bytes* with one exact edit (count==1
asserted), then run through `ho_witness_ok` and `run_tool_sandboxed`. Result: **7/7 witness
`(True,'vector-equivalence')` and 7/7 tool `ACCEPT rc=0 PASS`** — no false kill.

| probe | construction (edit on the sealed copy) | body sha256 | witness | tool |
|---|---|---|---|---|
| `fam-pad-inside-arith` | `npass=$((npass+1))` → `npass=$(( npass + 1 ))` | `fbe61f77…0dc20c` | True/equiv | ACCEPT 0 |
| `fam-reversed-operands` | → `npass=$((1+npass))` | `69f80e26…bd8a23` | True/equiv | ACCEPT 0 |
| `fam-tab-arith` | `nfail=$((nfail+1))` → `nfail=$((nfail\t+1))` (literal tab) | `773b734e…1cc0ec` | True/equiv | ACCEPT 0 |
| `fam-trailing-comment` | `*) nsetup=$((nsetup+1)) ;;` → `… ;; # setup bucket` | `c0c39851…376eb6` | True/equiv | ACCEPT 0 |
| `fam2-octal-literal` | `npass=$((npass+01))` | `4e4296f0…a339eb` | True/equiv | ACCEPT 0 |
| `fam2-hex-literal` | `npass=$((0x1+npass))` | `f51d5721…84f8b3` | True/equiv | ACCEPT 0 |
| `fam2-blank-line-in-case` | blank line between the last arm and `esac` | `a1e36680…ae84f1` | True/equiv | ACCEPT 0 |

`01`/`0x1` matter: they are textually new but numerically identical, so they also prove the tool
does not byte-compare the block against `REF_BLOCK` anywhere on the audit path.

## 5. Why the assigned family admits no divergence (proof, not just evidence)

The family is inert by construction. Bash semantics (`case` first-match, `$(( ))` evaluation —
the runner's own ground, `corpus/SOURCES.md` row S097) are invariant under spacing, operand
order, numeric-literal spelling, blank lines and comments inside the block. The tool's block
detectors are all behaviour/operand based and none reads arm bytes for equality:

- `check_head` reads only assignments *upstream* of the tally start (`tool.py:307-342`);
- `check_static` reads the loop operands and `local nlegs=` (`tool.py:344-360`);
- `check_runtime` compares `(rc, first stdout line)` against an independent oracle over 15,158
  vector runs (every status 0..255 at every position, every count pair, co-occurrence pairs,
  operand dup/drop stress) (`tool.py:372-438`, `CONFIGS` `tool.py:265`);
- `check_harness` replays the *copy's own harness section* with blocks injected as
  `$AUDIT_INJECT` (`tool.py:496-554`); `REF_BLOCK` is used only to build the fault panel
  (`tool.py:441-494`), never as an equality target for the copy's block.

Identical semantics ⇒ identical runtime tuples ⇒ PASS. Empirically confirmed 7/7 (§4).
**Therefore: for the strict cosmetic-arithmetic family, none exists** — any construction the
tool kills has left the family.

## 6. Critical finding — witness-valid `accept` copies the tool (correctly) kills

Each JSON below is **pristine-relative and self-contained** — the form the counter consumes
(`apply_edits(pristine, ho['edits'])`, `c1-measure.py:131-136`) — and each is a variant of this
copy: it keeps the sealed copy's spacing change as its base and adds one further construction.
`probe3.py` (rc 0) applies each JSON *exactly as written* to the pinned runner, asserts the
resulting body is the one probed (`BODY_MATCH probed=3/3`), and re-runs the amended witness and
the real tool. All three returned `(True, 'vector-equivalence')` and a tool `TALLY_AUDIT: FAIL`
(rc 1). Each passed the counter's own `validate_ho` (schema gate, `c1-measure.py:102-128`); tool
runs used `run_tool_sandboxed` (`c1-measure.py:234`), the same bwrap boundary as the deciding run.

### 6a. `adv3-status4-arm` — same block region, status 4 counted as a pass

```json
{
 "author": "seat Mutacceptvectorarithspace",
 "edits": [
  {
   "new": "      0) npass=$((npass+1)) ;;\n      1) nfail=$((nfail+1)) ;;\n      4) npass=$((npass+1)) ;;\n      *) nsetup=$((nsetup+1)) ;;\n",
   "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n"
  }
 ],
 "id": "adv3-status4-arm",
 "set": "accept",
 "witness": {
  "vector": [
   1,
   2,
   3,
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

- witness: `(True, 'vector-equivalence')`; body sha256 `51fc671691099aecf035708c7e411313a0277c407919c0ae3d469bcd3f8988b8`.
- tool: `KILL`, rc 1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`;
  `CHECK runtime FAIL vectors=15158 mismatched=1674; first: cfg(0,1) statuses 4 0 0 0 0 0 0 0 0:
  got (0, 'REGRESSION: PASS (cases=9 passed=9; …)'), want (2, 'REGRESSION: SETUP (cases=9
  passed=8 cannot-verify=1)')` (`probe.out`).
- direct tuples (`block_run`, `c1-measure.py:154`): witness vector
  `[1,2,3,0,0,0,0,0,0]` → both `(1,'REGRESSION: FAIL (cases=9 passed=6 failed=1 setup=2)')`,
  equal; **off-witness** `[4,0,…]` → pristine `(2,'… SETUP (cases=9 passed=8 cannot-verify=1)')`,
  mutated `(0,'REGRESSION: PASS (cases=9 passed=9; …)')`, unequal.
- Real defect: the block's own contract routes every status other than 0/1 to the setup arm, so
  status 4 must yield `SETUP (cannot-verify=1)`; the variant silently classifies it as a pass.
  The tool's per-status sweep is exactly the audit surface that catches this, and its kill is the
  correct verdict against the block's contract.

### 6b. `adv3-triple-digit-arm` — same block region, statuses 100-255 counted as passes

```json
{
 "author": "seat Mutacceptvectorarithspace",
 "edits": [
  {
   "new": "      0) npass=$((npass+1)) ;;\n      1) nfail=$((nfail+1)) ;;\n      [0-9][0-9][0-9]) npass=$((npass+1)) ;;\n      *) nsetup=$((nsetup+1)) ;;\n",
   "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n"
  }
 ],
 "id": "adv3-triple-digit-arm",
 "set": "accept",
 "witness": {
  "vector": [
   1,
   2,
   3,
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

- witness `(True, 'vector-equivalence')`; body sha256 `cfcf8a8a9bc39dd0046654aad0f23b292387f445bb90aa9884a4517e292b0bf3`.
- tool `KILL` rc 1, `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)`;
  `CHECK runtime FAIL vectors=15158 mismatched=9648; first: cfg(0,1) statuses 100 0 … : got
  (0,'REGRESSION: PASS (cases=9 passed=9; …)'), want (2,'REGRESSION: SETUP (cases=9 passed=8
  cannot-verify=1)')` (`adv2-full.out`, wrapper rc 0, tool rc 1).
- Real defect, and reachable: 124 (timeout) and 126/127 (suite not runnable) are exactly the
  runner's INCONCLUSIVE statuses in its own exit map; the triple-digit arm turns them into
  passes, so a timed-out or unrunnable leg can produce a green `REGRESSION: PASS` line. The
  tool's kill is the correct verdict.

### 6c. `adv3-head-overwrite` — accept+vector never reads the head

```json
{
 "author": "seat Mutacceptvectorarithspace",
 "edits": [
  {
   "new": "      0) npass=$((npass+1)) ;;\n      1) nfail=$((nfail+1)) ;;\n      *) nsetup=$((nsetup+1)) ;;\n",
   "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n      *) nsetup=$((nsetup + 1)) ;;\n"
  },
  {
   "new": "  st_claims=$?\n  st_claims=0\n",
   "old": "  st_claims=$?\n"
  }
 ],
 "id": "adv3-head-overwrite",
 "set": "accept",
 "witness": {
  "vector": [
   1,
   2,
   3,
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

Body sha256
`9b4f546e6aebd56d6ed35c15b905047349c56c220f794eca8932d8211b569d9d`; witness
`(True,'vector-equivalence')`; tool `KILL` rc 1 `TALLY_AUDIT: FAIL (head=fail static=pass
runtime=pass harness=pass)`, detail: `non-bare leg assignment(s) in the head: st_claims=0; leg
st_claims assigned 2 times in the head; leg st_claims appears 3 times in the head`
(`probe.out`; the JSON as written re-derives the same body in `probe3.out`).

Structural proof that the accept+vector arm is head-blind: `ho_witness_ok`'s accept branch is
`return a == b and mutated != pristine` over `tally_block_of(pristine)/tally_block_of(mutated)`
only (`c1-measure.py:214-215`); the same head variant still validates with the **all-zero**
witness vector (`[0]*9` → `(True,'vector-equivalence')`, `probe2.out`). So *any* head defect —
including the two head faults the kill arm relies on — can be minted as a valid must-accept copy.

### 6d. The counter would score it exactly as a missed accept

`score_tool` (`c1-measure.py:265-283`) over `[sealed, adv3-status4-arm]` both `set=accept`
(the `adv3-status4-arm` body is byte-identical to the probed `adv-status4-arm` body —
`probe3.out`, `BODY_MATCH probed=3/3`): `kill=0/0 accept=1/2` (`probe2.out`). In the deciding run's arithmetic that is `ho_accept=5/6`
with a blameless tool → `C1_R33_PASS=false`. No tool check fails on the sealed copy (it is
genuinely equivalent); the loss would come solely from the label.

## 7. What this does and does not refute

- **Not a tool defect.** On all three adversarial copies the tool's kill is the correct verdict
  (each copy demonstrably changes classification off-witness: status 4/100-255 become passes, or
  a leg status is overwritten in the head). The pinned tool accepted the genuinely equivalent
  copies: pristine + sealed + 7 family clones, 9/9 PASS.
- **The deciding run stands.** This copy's authoring receipt, my witness call and my tool run all
  agree; the 6 sealed accept copies are not shown to be faulty. Nothing here moves
  `C1_R33_PASS=true` at `c17e593b`.
- **The finding is in the amended gate as a labeling procedure.** The rule doc states
  accept+vector demands equivalence "on the named 9-status vector"
  (`corpus/knowledge/witness-equivalence-rule.md`, §The rule) — the implementation matches the
  document, but a one-vector sample (head not consulted at all) is not equivalence; S101
  (equivalent mutants) is cited as the reason for the arm, yet the arm samples. The doc's claim
  that the set-aware rule tests the tool's real surfaces "instead of the author's construction
  tricks" does not hold for an accept copy faulted off-witness. Post-data, this cannot amend the
  frozen rule: **routed as a round-35 Hold** (accept+vector witness should compare a witness
  *family* — e.g. every count pair plus per-position extremes — and reject any head difference,
  or accept+vector should require a byte-identical head).

## 8. Limits

- One accept copy attacked; the kill arm was not attacked by this seat.
- Not probed, therefore **no claim**: the analogous false-*accept* direction. The tool's
  co-occurrence sweep uses a fixed status set (`CO`, `tool.py:407`) plus single-position sweeps;
  a block fault keyed on two statuses outside that set would be invisible to both the tool and
  this witness vector. Named as a residue class by L1 (`corpus/lessons/round-34.md`, Holds:
  "nonzero-leg stress, all-pairs nlegs recompute"). Recording it as an unexecuted pointer only.

## 9. Restoration evidence and tooling

- Read-only pins re-hashed after every probe: `tool.py` `7b11ba25…8d10`, `pristine.sh`
  `a7d3f2dd…2eb9` (`restore_after.txt`, rc 0) — identical to §1.
- Lane clone clean: `git -C lane status --porcelain` → 0 bytes (`lane_status_after.txt`,
  rc 0). No git/jj write command was run anywhere.
- Sealed copy file unchanged: `3f8ad257…8dc`; committed blobs at `c17e593b` and `0b99d48`
  identical to it.
- Every mutant lived under `/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorarithspace/`;
  nothing outside that dir and this report was written.
- **Tool installs/updates: none** (pacman transactions paused host-wide per the orchestrator
  ruling; `bwrap`, `git`, `/usr/bin/python3` 3.14.8 already present and sufficient).

## 10. Reproduce

```
cd /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorarithspace
/usr/bin/python3 probe.py   > probe.out   2> probe.err ; echo $? > probe.rc    # rc 0
/usr/bin/python3 probe2.py  > probe2.out  2> probe2.err; echo $? > probe2.rc   # rc 0
/usr/bin/python3 probe3.py  > probe3.out  2> probe3.err; echo $? > probe3.rc   # rc 0
```

`probe.py` builds the sealed mutant, runs pristine control + sealed copy + 4 family clones + 2
adversarial clones (witness + `run_tool_sandboxed`) and dumps `probe-results.json`.
`probe2.py` adds 3 more family clones, the triple-digit construction, the `score_tool` pair, the
direct `block_run` tuple table and the all-zero-vector head structural check
(`probe2-results.json`). `probe3.py` takes the three §6 JSONs *as printed above*, applies each to
the pinned runner, asserts the body equals the probed one (`BODY_MATCH probed=3/3`) and re-scores
witness + tool (`probe3-results.json`). Constructor-form bodies from the first passes:
`adversarial-jsons.txt`. Full tool stdout: `probe.out`, `probe3.out`, `adv2-full.out`.
Diff: `sealed.diff`. Pins: `pins_actual.txt`, `restore_after.txt`, `blob_*.txt`.
