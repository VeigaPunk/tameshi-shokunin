# Mutacceptheadversionrename — mutation seat, round 34 / wave 1

Target: `.ufo/evidence/round-33/heldout/ho-accept-head-version-rename.json` (set=`accept`,
witness=`{kind: head}`), attacked at lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Claim under observation: C1 (operability capability acquisition, `tools/tally-audit-v2.py`),
deciding run at `c17e593b51802dd4ed568da3265f21c6d00c4273`.

Summary: the sealed copy **behaves as labelled** — the real tool accepts it exactly as the
set demands (mutant survives, expected detector output matched on pristine and mutated bytes).
An adversarial probe of the same family found **one critical soundness gap in the amended
`ho_witness_ok` accept+head rule**: a tool-inert head comment that names a leg is validated by
the counter as must-accept while the real tool kills it (F1 below). The landed C1_R33 numbers
are not contradicted; the gap is forward-looking (any sealed accept+head copy of that shape
would enter the accept denominator as unsatisfiable).

## 1. Setup and pins (all paths absolute under the fleet root unless noted)

Scratch root: `/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptheadversionrename/`.

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptheadversionrename
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptheadversionrename/lane      # rc 0  (clone.rc)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                    # rc 0  (checkout.rc)
git -C .../lane rev-parse HEAD                  # 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
```

Pinned bytes extracted from the **tip** commit:

```
git -C .../lane show 0b99d48e...:tools/tally-audit-v2.py > tool.py       # rc 0 (tool_extract.rc)
git -C .../lane show 0b99d48e...:tools/mutate-and-run.sh > pristine.sh   # rc 0 (sh_extract.rc)
sha256sum tool.py pristine.sh
```

| artifact | sha256 | pin | match |
|---|---|---|---|
| `tool.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | yes |
| `pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | yes |
| counter `lane/.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `f6b8868c...a07f28c` | yes |
| sealed JSON (read-only, unmodified) | `2e600127ab1d86f7e52f312db5ca4440223a0996bc4c6974f6eab3cf149bce90` | n/a | n/a |

The counter was imported **as a module** from the scratch lane path
(`probe.py`, `importlib.util.spec_from_file_location`); its default mode was never run
(kill rule consumed). `sys.dont_write_bytecode = True` was set before import.

## 2. Mutant derivation (counter's own edit applier)

`probe.py` loads the JSON, calls `validate_ho` then `apply_edits(pristine_text, ho['edits'])`.
`apply_edits` (counter lines 131–137) raises `CounterError` unless each `old` string occurs
**exactly once**; it did not raise, so uniqueness is asserted by the frozen counter itself.

The single edit, verbatim from the JSON:

```json
{"old": "VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'\n",
 "new": "VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14) sealed-a2'\n"}
```

Derived `mutated.sh` sha256: `c70bd0b38ec397425b123a9eb1d22747e6d0cdb1c81302f6c6c51995b2dca127`.
Diff against pristine is one line (177). Counter-level structure:

- `tally_block_of(pristine) == tally_block_of(mutated)` → **True** (`block_identical`)
- `head_of(pristine) != head_of(mutated)` → **True** (`head_differs`)
- `ho_witness_ok(ho, pristine, mutated, work)` → **`(True, 'head')`** — the amended gate
  validates the copy (counter line 208: accept+head, block identical).

## 3. Detector runs (real tool, counter's `run_tool_sandboxed`)

`probe.py` writes each runner to its own dir and calls
`c.run_tool_sandboxed(tool.py, copy, work)` — the counter's own bwrap boundary (counter
lines 234–262): `timeout 600` outside, `python3 -I /w/tool.py --runner /w/copy.sh` inside.
Command: `python3 probe.py variants ...` — rc **0** (`probe.rc`), log `variants.log`.

| copy | expected (label) | outcome | rc | last stdout line |
|---|---|---|---|---|
| pristine baseline | ACCEPT | **ACCEPT** | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `mutated.sh` (sealed copy) | ACCEPT | **ACCEPT** | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |

Full stdout for the mutant, captured under the counter's own `bwrap_argv`
(`python3 capture.py tool.py mutated.sh`, exit 0):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Verdict on the sealed copy: **survived — expected behaviour, label honoured**. The VERSION
line (runner line 177) is upstream of `run_regression()` (line 1345), which is outside the
tool's `head_section()` scope (tool lines 159–167: the prefix of the *function body*), so the
edit is inert for all four checks. No defect found in `ho-accept-head-version-rename`.

## 4. Restoration evidence

The mutation is a derived file; no target was ever written to.

- `pristine.sh` before/after: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` / same
- `tool.py`: `7b11ba25...598d10` throughout
- Frozen fleet artifacts, re-hashed after all runs: `tools/tally-audit-v2.py` = `7b11ba25...598d10`,
  `tools/mutate-and-run.sh` = `a7d3f2dd...12eb9`, sealed JSON = `2e600127...bce90` — unchanged.
- Scratch lane: `git -C .../lane status --porcelain` → empty (0 lines); `git -C lane rev-parse HEAD`
  still `0b99d48e...`. Import-created `__pycache__` dirs were removed; final
  `find lane -name __pycache__ | wc -l` → 0.

## 5. ADVERSARIAL — F1 (critical): accept+head witness validates a copy the tool kills

### Mechanism

The counter's head is the **whole-file prefix** before `  local nlegs=` (`START`, counter line
61; `head_of`, lines 147–152). The tool's head is only the prefix of the **`run_regression()`
body** (tool `head_section`, lines 159–167; `audit`, lines 555–565). The accept+head witness
rule (counter lines 194–208) checks only *head differs* + *block identical*. The tool adds a
conservative substring rule inside its head: each leg name must occur **exactly twice** (tool
lines 326–335, `cnt != 2` at line 333). Therefore an inert head comment that merely **names a
leg** is validated as must-accept by the counter and killed by the tool. Identical block is
necessary but not sufficient for a head edit to be tool-inert.

### Exact variant JSON (same family: `set=accept`, `witness.kind=head`, block untouched)

```json
{
 "id": "var-a-comment-legname",
 "author": "r34-w1 adversarial probe (Mutacceptheadversionrename)",
 "set": "accept",
 "edits": [
  {
   "old": "run_regression() {\n  if [[ -n \"$TARGET$SPEC$SUITE$LABEL\" ]]; then\n",
   "new": "run_regression() {\n  # adjudication note: the st_js leg runs first (documentation only)\n  if [[ -n \"$TARGET$SPEC$SUITE$LABEL\" ]]; then\n"
  }
 ],
 "witness": {
  "kind": "head"
 }
}
```

Derived bytes sha256: `c96abc939e99165d56a3339a04ff44296c8dfcbceeead5042431edeb730a46bc`.
Counter-level structure: `block_identical` **True**, `head_differs` **True**,
`ho_witness_ok` → **`(True, 'head')`** (validated as an accept).

### Tool verdict (opposite to the witness-set)

`python3 capture.py tool.py var-a-comment-legname.sh` → exit **1** (`var-a.cap.rc`):

```
rc=1
CHECK head FAIL legs=9; leg st_js appears 3 times in the head (want exactly 2: the local declaration and its bare st_x=$?)
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)
```

Through the counter's own scorer on one accept copy
(`c.score_tool(tool.py, [('var-a','accept',bytes)], work)`) → **`(0, 0, 0, 1)`**:
0/1 accept hits. In a deciding run this copy would be counted at counter line 405
(`ho_at += 1`) as a valid accept and would miss at line 282 (`a_hit += bool(accept)`) — the
gate admits a sealed copy the tool can never satisfy. Reproduce:
`python3 probe.py variants variants/var-a-comment-legname.json` (rc 0, witness and outcome in
`variants.log`) and the capture command above (exit 1).

### Impact and classification

- Critical as a **soundness gap in amendment 6's accept+head rule**: "identical block" does not
  entail "tool accepts"; the tool's own head check can be tripped by a head edit, so the
  witness set can contain unsatisfiable accepts.
- The landed `C1_R33` receipt is **not** contradicted: the attacked copy and the frozen six
  sealed accepts were measured at `c17e593b` as 6/6, and no sealed copy of the variant shape
  exists in `.ufo/evidence/round-33/heldout/` (14 files; this seat attacks one of them).
  The finding is forward-looking: a future accept+head copy written this way inflates the
  accept denominator with a guaranteed miss.
- Plausibility is not hypothetical: the sibling sealed copy `ho-accept-head-comment` already
  inserts a comment inside `run_regression()`'s head (`  # tameshi sealed held-out accept A1
  (inert head marker)` after `  st_js=$?`). It survives only because its text names no leg;
  adding one leg name to an "inert head marker" is a one-token construction step.

## 6. Corroboration and controls (all in the same family)

| variant | sha256 | witness | tool | note |
|---|---|---|---|---|
| `var-b-duplicate-bare-assign` (second `  st_js=$?` in the head) | `b8ef92903b7d08d5942c356a9516eafa74eb91fbb9fe30d0f80ff029aeb74dca` | `(True,'head')` | **KILL** rc 1, all four checks fail | corroborates the same gate gap with a structural head edit; tool output in `var-b.full.txt` |
| `var-c-comment-benign` (head comment, no leg names) | `8f992467063e1bdcb6b471be9fe025a998b05286e5e82ed29d2c342c237b5a32` | `(True,'head')` | **ACCEPT** rc 0, all pass | control: the rule also validates tool-inert head edits; no conflict |
| `var-d-usage-grep-bait` (help-text line matching `^  regression_case_git js-`) | `a9c4e0422ae6bdcf52ebf3e6aacd6284682c37a84985a9d1f70faec2905af2b0` | `(True,'head')` | **ACCEPT** rc 0, all pass | not a finding: `check_harness` extracts only the tally-harness section (tool lines 496–509), so the selftest call-site grep is outside the audited text |

Boundary: the accept+head family is sound only for head edits outside the tool's audited
surfaces (file lines 1–1344, e.g. the VERSION line, and leg-name-free text in
`run_regression()`'s head). Variant A shows the family as defined by the counter is **not**
sound in general. No attempt was made to alter the contract; the family claim stands as an
observation.

## 7. Bounds, tooling, and evidence inventory

- No writes outside the scratch root `/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptheadversionrename/`
  and this report. Fleet `tools/`, `.ufo/state/`, lane jj/Git index untouched; no `agent://all`,
  no model parameter, no subagent dispatch. Every command's exit code was captured to a file;
  no `&&` chains around detectors. Counter default mode never run; only module function calls
  (`validate_ho`, `apply_edits`, `tally_block_of`, `head_of`, `ho_witness_ok`,
  `run_tool_sandboxed`, `score_tool`, `bwrap_argv`) on scratch copies.
- Tooling: none installed or upgraded.
- Evidence in scratch: `probe.py` + `probe.log` (rc 0), `variants.log` (rc 0),
  `capture.py`, `mutated.sh`, `pristine.sh`, `tool.py`, `variants/*.json`,
  `var-{a,b,c,d}-*.sh`, `var-{a,b,c,d}.full.txt`, `*.cap.rc`, `clone.rc`, `checkout.rc`,
  `tool_extract.rc`, `sh_extract.rc`, `probe.rc`, `variants.rc`.

Verdict: sealed copy **PASS** (ACCEPT as labelled, mutant survived, no defect);
adversarial probe **finding F1** (amended accept+head witness unsound for tool-audited head
edits), with F2 corroboration and two controls.
