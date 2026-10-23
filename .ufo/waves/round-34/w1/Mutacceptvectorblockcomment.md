# Mutacceptvectorblockcomment — C1 sealed accept copy `ho-accept-vector-block-comment` (comment family) + adversarial construction of the same family

Round 34 / wave 1 (v2, build+attack) / mutation-tester seat
`tameshi-r34-w1-Mutacceptvectorblockcomment`. Claim under attack: **C1** (operability capability
acquisition, `tools/tally-audit-v2.py`), measured TRUE at revision
`c17e593b51802dd4ed568da3265f21c6d00c4273`; deciding receipt `C1_R33: … v1_kill=18/18 v1_accept=8/8
ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 … C1_R33_PASS=true`, exit 0
(`.ufo/evidence/round-34/measure/`). Lane tip at dispatch:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Scratch (all writes):
`/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorblockcomment/`. Lane read-only throughout.

**Verdicts**

- Assigned sealed copy (`set=accept`): **ACCEPTED by the real tool — the label is satisfied.** Witness
  `(True, 'vector-equivalence')`, tool `('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass
  runtime=pass harness=pass)')`. Baseline (pristine) and restored bytes both ACCEPT; the mutant is a
  legitimate accept-class member.
- Adversarial probe: **FINDING (critical) — the amended witness gate validates comment-injection
  constructions that the frozen tool does not ACCEPT.** The sharpest is an *inert head comment that
  mentions a leg name*: behavior is byte-identical to pristine (same tally block hash, same
  head+block run), the amendment-6 witness returns `(True, 'vector-equivalence')`, and the tool
  returns `rc=1 TALLY_AUDIT: FAIL (head=fail …)`. Two further constructions are SETUP refusals
  (`rc=2`). All three are in the assigned fault family (comment injection), so a sealed accept copy
  authored this way would pass `ho_witness_ok` (hence `ho_invalid=0`) and then miss the tool's
  accept tally → `C1_R33_PASS=false`. The landed deciding run is unaffected (its copy is §3); no
  false *pass* of C1 exists in this family (§4.5).

## 1. Pins and setup (exit code of every command captured to a file, never `&&`)

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorblockcomment
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../Mutacceptvectorblockcomment/lane   # clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                             # checkout.rc=0
git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7              # tip.txt, rc=0
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py  > tool.py                       # show1.rc=0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh   > pristine.sh                   # show2.rc=0
sha256sum tool.py pristine.sh                                                             # exact pins below
```

| artifact | sha256 observed | pin | match |
|---|---|---|---|
| `tool.py` (`tools/tally-audit-v2.py`) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (`tools/mutate-and-run.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| counter `lane/.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amend-6 pin `f6b8868c…a07f28c` | YES |
| sealed `ho-accept-vector-block-comment.json` (fleet, read-only) | `3da5127049bcc371e2254581697264ea0f62fbaf0746ed3483daeb5ac0f312ac` | lane copy identical (same sha) | YES |

Post-run re-hash (`finalize.log`): `pristine.sh` = `a7d3f2dd…2eb9`, `tool.py` = `7b11ba25…8d10`;
the live fleet artifacts hash to the same values (§8).

## 2. Detector and witness

The counter is imported as a module from the lane path (never run in default mode; the consumed kill
rule is honored). The detector is the counter's own `run_tool_sandboxed(tool, copy, work)`
(`c1-measure.py:234-263`): `python3 -I /w/tool.py --runner /w/copy.sh` under `bwrap --unshare-all`
with read-only runtime mounts, writes confined to the workdir. Outcome mapping is the counter's:
KILL iff `rc==1` and the last `TALLY_AUDIT:` line starts `FAIL`; ACCEPT iff `rc==0` and it starts
`PASS`; anything else is OTHER. For accept-set copies a hit needs ACCEPT (`score_tool`, lines
265-284). The witness detector is `ho_witness_ok(ho, pristine_text, mutated_text, work)` at
`c1-measure.py:184-220` (amendment 6), plus `validate_ho`, `apply_edits` (exactly-once anchors),
`tally_block_of`/`head_of`, `block_run` (real bwrap). Script `probe.py` (sha256
`009abc47e3069759b7e17b100bfe4f92c658ffde523a36c8d06be9f41c837f48`) writes every case file and
records the full result in `probe-result.json` (sha256
`cbaf0b819402ec6d194cfb028c96b8fda1f8cc638a7a13d23b0e807d9f88bacc`); run exit `probe.rc=0`.

## 3. Assigned sealed copy — `ho-accept-vector-block-comment` (label accept)

JSON (fleet file, unmodified): one edit,
`old="      0) npass=$((npass + 1)) ;;\n"` → same + `"      # audit witness note (inert block
marker)\n"`; witness `vector [1,2,0,0,0,0,0,0,0]`. `apply_edits` found each old string exactly once
(the function raises otherwise).

| stage | bytes | sha256 | witness | tool |
|---|---|---|---|---|
| pristine | 106538 | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | — | `ACCEPT rc=0 TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| sealed mutant | 106586 | `5f111e99de83d01d703a76a7c3b98a37cd17e8fc3f0d2fe98e465416000903c0` | `(True, 'vector-equivalence')` | `ACCEPT rc=0 TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| restored | 106538 | `a7d3f2dd…2eb9` (equal, `finalize.log`) | — | `ACCEPT rc=0 TALLY_AUDIT: PASS (…)` |

Behavioural grounding of the witness (`witness_tuples.py`, exit `witness_tuples.rc=0`), vector
`[1,2,0,0,0,0,0,0,0]`:

```
pristine block sha e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d (1562 B)
a = block_run(pristine block) = (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
b = block_run(sealed block)   = (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')   a==b True
```

`CHECK` lines from the instrumented sandboxed run (`probe.log`): head PASS legs=9 · static PASS legs=9
operands=9 nlegs=9 · runtime PASS vectors=15158 mismatched=0 · harness PASS reference cases=9; faults
rejected=34/34. The tool's entire sweep agrees with the oracle on the mutated block: the added comment
is cosmetic exactly as the label claims.

Baseline determinism: pristine ACCEPT (rc 0), restored bytes ACCEPT (rc 0), same sha —
`RESTORED_TOOL ['ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)']`
(`finalize.log`).

## 4. Adversarial — same fault family (comment injection), three constructions the witness validates and the tool does not ACCEPT

All variants are built from the pinned `pristine.sh` with exactly-once anchors; each is validated by
`validate_ho` and returns `(True, 'vector-equivalence')` from the amended witness.

| variant | construction (comment placement) | block vs pristine | witness | tool outcome |
|---|---|---|---|---|
| **F1** `v-head-mention-leg` | inert comment **before the tally block** mentioning `st_citecheck` | byte-identical | `(True,'vector-equivalence')` | **KILL rc=1** `TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)` |
| **F2** `v-loop-semi-comment` | inert comment between `;` and `do` in the tally loop header | changed (comment) | `(True,'vector-equivalence')` | **OTHER rc=2** `TALLY_AUDIT: SETUP (no loop governing the counting case)` |
| **F3** `v-case-esac-comment` | inert comment containing the word `esac` right after `case $st in` | changed (comment) | `(True,'vector-equivalence')` | **OTHER rc=2** `TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found)` |
| N1 `v-head-plain` | inert comment before the block, no leg name | byte-identical | `(True,'vector-equivalence')` | ACCEPT rc=0 (control) |
| N2 `v-block-mention-leg` | inert comment after arm `0)`, mentions `st_js` | changed (comment) | `(True,'vector-equivalence')` | ACCEPT rc=0 (control) |
| N3 `v-cont-swallow-citecheck` | inert comment ending in `\` before `st_citecheck=$?` | byte-identical | `(True,'vector-equivalence')` | ACCEPT rc=0 (control, see §4.4) |

Mutant hashes (bytes retained under `cases/`): F1 `5e79ab8c3fd158d2bf041cc00c82c7ab8b716f37afa7ce0db254337114efd4aa`,
F2 `cd6d1159f0128f0b76ee6c547fe194c67bbbe16ffad0a70156ccc52bc226bfd6`,
F3 `351eedaf260af9757ff7df8641c33e691c739114ccb51dc0ed33da58c1cce0d2`,
N1 `35702851d855b92f4e71405991de4957a91371ddccb7a395e48c3292f725061b`,
N2 `da53305077660c87c9c865a873a319ff0d3cbf2fc7be568c770599ed2e03e16d`,
N3 `7505edfb007faf48edd9a0bbe732f3c35ea8ae2cc70504a84ddc3c7a49a26d1a`.

### 4.1 F1 — inert head comment mentioning a leg name: FAIL on behaviourally identical bytes (critical)

Exact JSON (validated by `validate_ho`; same shape as the sealed paper):

```json
{
 "id": "v-head-mention-leg",
 "author": "tameshi-r34-w1 mutation seat",
 "set": "accept",
 "edits": [
  {"old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n",
   "new": "  # audit witness note: st_citecheck is the ninth leg (inert block marker)\n  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n"}
 ],
 "witness": {"vector": [1, 2, 0, 0, 0, 0, 0, 0, 0]}
}
```

Tool verdict: `('KILL', 1, 'TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)')`,
`CHECK head FAIL legs=9; leg st_citecheck appears 3 times in the head (want exactly 2: the local
declaration and its bare st_x=$?)` (`probe.log`). Trigger: `check_head`'s twice-only rule
(`tool.py:326-334`) counts **substring occurrences of each leg name in the head text**, and a comment
line is head text: declaration (1) + bare `st_citecheck=$?` (1) + comment (1) = 3.

The runner is behaviourally identical to pristine, shown four ways:

1. the diff is one inserted line whose first non-space byte is `#`, between a blank line and
   `local nlegs=…` inside `run_regression()` (`repro.log`; `bash -n` rc 0);
2. the audited tally block is **byte-identical** (sha `e163133c…2215d`, `witness_tuples.log`);
3. the amendment-6 witness returns `(True,'vector-equivalence')` with identical `block_run` tuples;
4. head+block behavioural probe on the runner's own bytes with every leg stubbed to return 0 (state
   primed; `auto=0 KEEP=1`): `rc=0`, stdout sha256
   `67cd472ecd30fe2c1dfe432b603077c6c631dac39a556b36fdc4edf6c8ad754f`
   (`REGRESSION: PASS (cases=9 passed=9; …)`, 120 B), identical for pristine and all seven variants
   (`repro2.log`, `finalize.log`).

The tool's own head surface is unchanged: `assigns=9 bare=9 nonbare=[]` for pristine and F1
(`repro2.log`, tool regexes imported). So this is a **false positive of the frozen tool**: a cosmetic
comment that names a leg is reported FAIL, while the same comment without the leg name (N1) is
ACCEPT. The accept-side discrimination is text-sensitive, not semantic.

### 4.2 F2 — inert comment between the loop operand list and `do`

```json
{
 "id": "v-loop-semi-comment",
 "author": "tameshi-r34-w1 mutation seat",
 "set": "accept",
 "edits": [
  {"old": " \"$st_citecheck\"; do\n",
   "new": " \"$st_citecheck\"; # audit witness note (inert block marker)\n do\n"}
 ],
 "witness": {"vector": [1, 2, 0, 0, 0, 0, 0, 0, 0]}
}
```

`for st in … ; # comment` + newline + `do` is valid bash with unchanged semantics (verified rc 0,
headprobe rc 0 / stdout sha `67cd472e…754f`). The witness validates. The tool's `LOOP_RE`
(`tool.py:174`) allows only `[ \t]*(?:;[ \t]*|\n[ \t]*)do\b` after the operand list, so the comment
prevents identification of the tally loop; `check_static → loop_operands → tally_loop` raises
`CannotAudit`, `main` prints `TALLY_AUDIT: SETUP` and exits 2 (`tool.py:679-690`). The tool refuses
to certify a behaviourally identical runner.

### 4.3 F3 — inert comment containing `esac` after `case $st in`

```json
{
 "id": "v-case-esac-comment",
 "author": "tameshi-r34-w1 mutation seat",
 "set": "accept",
 "edits": [
  {"old": "    case $st in\n",
   "new": "    case $st in\n      # esac (inert block marker)\n"}
 ],
 "witness": {"vector": [1, 2, 0, 0, 0, 0, 0, 0, 0]}
}
```

Bash treats the line as a comment (headprobe rc 0, same stdout). `counting_case` (`tool.py:190-200`)
cuts the case body at the first literal `esac` **in the raw text**, comment included, finds no counter
increment there, and raises `CannotAudit('counting \`case $VAR in\` not found')` → `SETUP`, rc 2. The
witness validates.

### 4.4 N3 — closure of the "comment swallows the next line" attack (negative result)

A comment ending in `\` before `st_citecheck=$?` does **not** swallow the assignment: bash ends a
comment at the newline, so the backslash is inside the comment. Verified on a 5-line script
(`tiny-cont.sh`): `rc=0 stdout='y=0' stderr=''`, and on the runner's own head+block bytes (rc 0,
stdout sha `67cd472e…754f`). The tool's ACCEPT of N3 is therefore correct; no false-accept of a
leg-dropping comment exists in this family.

### 4.5 What the finding does and does not establish

- It does **not** contradict the landed receipt: the assigned copy is ACCEPT (§3), and the deciding
  run's six accept copies are all tool-ACCEPT by construction (their comment texts avoid leg names and
  parse-sensitive placements). No false *pass* of C1 arises: every construction here makes the tool
  *stricter*, so the counter fails closed (`ho_a < ho_at` → `C1_R33_PASS=false`) if such a copy were
  sealed (`c1-measure.py:422-427`).
- What it bounds: amendment-6 `accept+vector` validates by **tally-block equivalence only**
  (`c1-measure.py:184-220`); a head-scoped edit is invisible to it (`tally_block_of(mutated) ==
  tally_block_of(pristine)` → `a == b`), and in-block edits are validated without ever asking whether
  the tool can parse the copy. Witness validity is therefore necessary but **not sufficient** for
  tool-ACCEPT in this family: three of seven sibling constructions validated by the gate are not
  ACCEPT. An author following the gate can mint an accept copy that fails the deciding predicate.
- F1 is additionally a **tool** false positive against the family's own definition of cosmetic: the
  `check_head` twice-only rule (`tool.py:326-334`) is a raw substring count and cannot distinguish a
  comment from a status rewrite (its docstring lists rewrites: spaced arithmetic, `printf -v`, `read`,
  `declare`, `unset`, wrappers, conditional zeroing). The frozen tool is byte-pinned and the v3 residue
  classes are measurement-only this wave: **no tool or runner edit is proposed**, this is a coverage
  finding for the residue list and for future accept-copy authoring (avoid leg names in comment text
  before the block, comments between the loop operand list and `do`, and the word `esac` inside the
  case).
- The contract is unchanged; verdicts here are observations, not integration decisions.

## 5. Reproduction (scratch root `S=/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorblockcomment`)

```bash
cd "$S"
/usr/bin/python3 probe.py          > probe.log          2>&1; echo $? > probe.rc            # 0
/usr/bin/python3 repro2.py         > repro2.log         2>&1; echo $? > repro2.rc           # 0
/usr/bin/python3 witness_tuples.py > witness_tuples.log 2>&1; echo $? > witness_tuples.rc   # 0
/usr/bin/python3 finalize.py       > finalize.log       2>&1; echo $? > finalize.rc         # 0
bash headprobe-pristine-0.sh > hp.out 2> hp.err; echo $? > hp.rc                            # 0
```

`probe.py` imports the counter from `lane/.ufo/evidence/round-33/c1/c1-measure.py`, applies each
case's `edits` through `apply_edits`, writes `cases/<name>.sh`, then prints one line per case:
`CASE <name> sha=<sha> bash_n=<rc> witness=<(bool,reason)|None> tool=(outcome,rc,last)` and the
`CHECK` lines. Expected (all observed, `probe.log`): pristine/sealed/N1/N2/N3 `('ACCEPT',0,'…PASS…')`;
F1 `('KILL',1,'TALLY_AUDIT: FAIL (head=fail …)')`; F2 `('OTHER',2,'TALLY_AUDIT: SETUP (no loop
governing the counting case)')`; F3 `('OTHER',2,'TALLY_AUDIT: SETUP (counting \`case $VAR in\` not
found)')`; every non-pristine case `witness=(True,'vector-equivalence')`.

## 6. Bounds compliance and restoration evidence

- Lane untouched: `git -C lane status --porcelain | wc -l` → `0`; `git -C lane rev-parse HEAD` →
  `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. No git/jj write commands anywhere (clone/checkout/show
  only, in the scratch clone); no writes to `.ufo/state/`, MANIFEST, fleet templates/scripts, the
  lane index, or sibling repos.
- Frozen artifacts intact after all runs: `pristine.sh` `a7d3f2dd…2eb9`, `tool.py` `7b11ba25…8d10`;
  live fleet copies re-hashed to the same values (`finalize.log`). Restored bytes equal pristine
  (`EQUAL=True`) and re-score ACCEPT rc 0.
- Kill rule honored: the counter was only imported and its functions called on scratch copies; no
  default-mode invocation of `c1-measure.py`.
- Writes confined to the scratch dir and this report. No tool installs/upgrades, no pacman
  transactions, no network fetch, no subagents.
- Caller-side error, not evidence: the first segment extraction in `repro.py` sliced the leg
  assignments together with the preceding `regression_case_git` calls, so it failed on an unprimed
  `PIN_BASH` for pristine and variant alike. It was replaced by the corrected head+block probe in
  `repro2.py` (§4.1); `repro.log` is cited only for its diff/block-identity lines.
