# Mutacceptvectorinertline — sealed accept copy reproduced; the amended witness gate admits two copies the tool kills

Round 34 / wave 1 / mutation-tester seat. Lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`
(`git -C .../lane rev-parse HEAD`, `checkout.rc=0`). Scratch:
`/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorinertline/` — every write is here plus this report
file. No tool installed or upgraded. The lane stayed read-only (`git -C lane status --porcelain` → 0 bytes,
rc 0 before and after). The default-mode kill rule was never invoked: the counter was imported as a module
from the lane path and only `validate_ho`, `apply_edits`, `tally_block_of`, `block_run`, `ho_witness_ok`,
`run_tool_sandboxed` were called, on scratch copies.

## 1. Setup and pins

All commands run from the scratch root; every substantive command's exit code was captured as
`cmd; echo $? > file`. The one exception is the setup chain, where mkdir and clone are joined by `&&`
(and the `cd`/`cat` navigation in a few probe invocations), so `clone.rc=0` also means mkdir succeeded.

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorinertline
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks <lane repo> .../lane   # clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach 0b99d48e…    # checkout.rc=0
git -C .../lane show <tip>:tools/tally-audit-v2.py                 > tool.py                       # extract-tool.rc=0
git -C .../lane show <tip>:tools/mutate-and-run.sh                 > pristine.sh                   # extract-runner.rc=0
git -C .../lane show <tip>:.ufo/evidence/round-33/c1/c1-measure.py > c1-measure.py                # extract-counter.rc=0
```

The mkdir and clone were one `&&` chain (`mkdir -p … && git clone …; echo $? > clone.rc`), so
`clone.rc=0` also means mkdir succeeded. The three `show` extractions were re-run afterwards under the
clean git env (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show …` →
`recheck-tool.rc=recheck-runner.rc=recheck-counter.rc=0`) and `cmp` against the first extraction reported
0 for all three, so the pinned bytes did not depend on the shell's git environment.

| artifact | sha256 (measured) | pin | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `c1-measure.py` (amendment-6 counter) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `f6b8868c…a07f28c` | YES |
| controls receipt (round-33/c1) | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` | read-only evidence | — |
| assigned sealed copy `ho-accept-vector-inert-line.json` | `edc3c69f519058f13ce1e2a6ec7ecbc768c118527ef9d9497690d5b73571c7cd` | read-only evidence | — |

The counter module is imported from
`/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorinertline/lane/.ufo/evidence/round-33/c1/c1-measure.py`;
its own `HERE/../../round-32/c1-measure.py` dependency resolves inside the clone (`r32.rc=0`). `bwrap`
0.13.1 and python 3.14.8 are present (`bwrap.rc=0`, `py.rc=0`); the counter's sandbox argv was smoke-tested
(`bwrap-test.rc=0`).

## 2. Probe 1 — the assigned copy, `ho-accept-vector-inert-line` (set=accept)

### 2.1 Bytes

The JSON edit's `old` string `"  done\n\n  if [[ $nfail -gt 0 ]]; then\n"` occurs exactly **1** time in
`pristine.sh` (counted directly; the counter's `apply_edits` would otherwise raise,
`c1-measure.py:131-137`). The counter's own `apply_edits` produced the copy; sha256
`8f3b60325786522dc52c106e35631d7cda461727d392831aa6b5d693a0dd2d29` (`mut-sealed.sh`). One hunk
(`diff -u pristine.sh mut-sealed.sh`, diff rc 1 = differences present):

```diff
@@ -1437,6 +1437,7 @@
     esac
   done
+  : "${TAMESHI_SEALED_A4:=0}"
 
   if [[ $nfail -gt 0 ]]; then
```

### 2.2 Witness gate (expected detector #1: `ho_witness_ok` → accept)

`ho_witness_ok(ho, pristine, mutated, work)` → **`(True, 'vector-equivalence')`** (`gate-results.json`,
`gate.rc=0`). Measured block runs at the declared witness vector `[0,0,0,0,0,0,0,0,0]`:

```
pristine  -> (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
mutated   -> (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
```

At the failing vector `[1,0,0,0,0,0,0,0,0]` both are `(1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')`.
A full-stdout comparison (my own detector, `probe_fullstdout.py`, `fullstdout.rc=0`) over six vectors
`000000000`, `100000000`, `000000002`, `120000000`, `255000000`, `011200000` shows
`sealed_identical_to_pristine=True` for **every** vector — the inserted `:` line is genuinely inert, not
merely witness-invisible.

### 2.3 Real tool (expected detector #2: `tally-audit-v2.py` → ACCEPT)

`run_tool_sandboxed(tool.py, mut-sealed.sh, work)` → **`('ACCEPT', 0,
'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')`** (`tool-results.json`,
`tool.rc=0`). Full capture from the identical sandbox invocation
(`timeout 600 bwrap --unshare-all --die-with-parent --new-session --clearenv --dev /dev --proc /proc
--tmpfs /tmp --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind /lib64 /lib64
--ro-bind /etc /etc --bind <work> /w --chdir /w /usr/bin/python3 -I /w/tool.py --runner /w/copy.sh`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
```

Baseline sanity on unmodified bytes: `pristine.sh` → `('ACCEPT', 0, 'TALLY_AUDIT: PASS
(head=pass static=pass runtime=pass harness=pass)')` with the identical four CHECK lines
(`tool-results.json`), so the detector was not failing closed by accident.

**Verdict P1: label honoured.** The copy is `set=accept`, the witness gate validates it, and the tool
accepts it (rc 0, `TALLY_AUDIT: PASS`). Nothing about the frozen copy is wrong.

## 3. Probe 2 — variant A: gate VALIDATES, tool KILLS (the gate is the wrong side)

Exact JSON (written to `adv-adv-accept-vector-nfail-branch-note.json`; `validate_ho` → OK, so the counter's
measurement loop would have admitted it as a sealed copy):

```json
{
 "id": "adv-accept-vector-nfail-branch-note",
 "author": "tameshi-r34-w1-Mutacceptvectorinertline",
 "set": "accept",
 "edits": [
  {
   "old": "  if [[ $nfail -gt 0 ]]; then\n",
   "new": "  if [[ $nfail -gt 0 ]]; then\n    printf 'SEALED_NOTE\\n'\n"
  }
 ],
 "witness": {
  "vector": [0, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Copy sha256 `852f489ae5caab3bb38e5524443f88530141130558cad22f16cd29631b596dd7`. It uses the same anchor
line as the assigned copy (`if [[ $nfail -gt 0 ]]`, one line lower) and the same "one inserted line"
construction, with a payload live on the FAIL path.

Gate (`probe_gate.py`, `gate.rc=0`): **`(True, 'vector-equivalence')`**. At the declared witness vector the
runs are identical (all-pass branch not entered); at `[1,0,…]` the mutated first line becomes
`SEALED_NOTE` (measured: `block_run_mutated_at_failvec = [1, "SEALED_NOTE"]`).

Tool (`run_tool_sandboxed`, `tool.rc=0`): **`('KILL', 1, 'TALLY_AUDIT: FAIL (head=pass static=pass
runtime=fail harness=pass)')`**, with

```
CHECK runtime FAIL vectors=15158 mismatched=1800; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0:
  got (1, 'SEALED_NOTE'), want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
```

**Mechanism.** The accept+vector rule is equivalence at *one author-chosen* vector
(`c1-measure.py:188-189`, `:215`: `return a == b and mutated != pristine, 'vector-equivalence'`), and
`validate_ho` accepts any 9-element vector of ints 0..255 (`c1-measure.py:119-124`). Nothing requires the witness
vector to exercise the code the edit touches. An all-pass vector `[0]*9` leaves the entire
`if [[ $nfail -gt 0 ]]`, `if [[ $nsetup -gt 0 ]]` and completeness-guard surface unobserved, so any line
placed there is certified "equivalent" without ever running. (Of the six frozen accept copies, only the
assigned copy and `ho-accept-vector-tail-comment` use `[0]*9`, and both of those edits are a `:`-expansion
no-op / a comment; the two block edits use `[1,2,3,…]` or `[1,2,…]` witnesses.)

**Verdict P2: gate unsound, tool correct.** This is a critical-level finding about the *amendment-6 witness
gate as admission control*: it does not prove benignity, only equality on one probe. It does **not**
falsify the landed C1 line — the frozen copy is genuinely inert (§2.2) and the six accept copies were
scored against the tool, so `ho_accept=6/6` is unaffected. The risk direction is fail-closed, not
fail-open: had this copy been authored, the gate would have admitted it and the tool would have killed it,
turning `ho_accept=6/6` into `6/7` and `C1_R33_PASS=false`. So the gate can void a true PASS; it cannot by
itself manufacture a false one.

## 4. Probe 3 — variant B: gate VALIDATES, tool KILLS a benign copy (tool precision)

Exact JSON (`adv-adv-accept-inert-head-comment-leg-name.json`; `validate_ho` → OK):

```json
{
 "id": "adv-accept-inert-head-comment-leg-name",
 "author": "tameshi-r34-w1-Mutacceptvectorinertline",
 "set": "accept",
 "edits": [
  {
   "old": "  local st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck\n",
   "new": "  local st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck\n  # witness note: st_js is the kimi-census leg\n"
  }
 ],
 "witness": {
  "vector": [0, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Copy sha256 `1fd84bec89bf133f73ca7f3c1cae86eed8ef4fc8dd171186a0a03789f1325760`; the diff is one comment line
inside `run_regression` (`diff-B rc=1`), which bash ignores.

Gate: **`(True, 'vector-equivalence')`** — the tally block is byte-identical, so the witness sees nothing
to object to (`block_changed=false`).

Tool: **`('KILL', 1, 'TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)')`**:

```
CHECK head FAIL legs=9; leg st_js appears 3 times in the head (want exactly 2: the local declaration and its bare st_x=$?)
CHECK runtime PASS vectors=15158 mismatched=0
```

**Mechanism.** The documented head check is assignment-based — "no other assignment to a leg var appears
outside the identified tally loop's operand list" (`tool.py:35-38`) — but the implementation counts
`head.count(name)` substrings and requires exactly 2 (`tool.py:326-334`). A comment is not an assignment,
so this is a false positive of the fail-closed twice-only rule. The frozen set's own head-comment copy
(`ho-accept-head-comment.json`) inserts its comment *without* naming a leg, which is why the measured
`ho_accept=6/6` does not expose this.

**Verdict P3: tool false-kill on the accept side; the gate is the correct side.** No kill is missed; a
benign family member is rejected. Same family as the assigned copy (an inert inserted line), different
construction. Measured, not inferred: runtime/static/harness all pass on this copy; the sole failure is
the substring count. Frozen C1 numbers stand (no such copy in the sealed set).

## 5. Probe 4 — co-failure: a line-2-only change is invisible to both (the DevPrintf class is still open)

Exact JSON (`adv-adv-accept-vector-line2-note-failpath.json`; `validate_ho` → OK): insert a line after the
FAIL `printf`, i.e. the mutation only ever changes **stdout line 2**:

```json
{
 "id": "adv-accept-vector-line2-note-failpath",
 "author": "tameshi-r34-w1-Mutacceptvectorinertline",
 "set": "accept",
 "edits": [
  {
   "old": "      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n",
   "new": "      \"$nlegs\" \"$npass\" \"$nfail\" \"$nsetup\"\n    printf 'NOTE_AFTER_FIRST_LINE\\n'\n"
  }
 ],
 "witness": {
  "vector": [0, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Copy sha256 `dd87a9dee14b2ad31106dd23254ae69dc14fa6ef6caa70279336e621d08703e2`.

Gate: **`(True, 'vector-equivalence')`** (block_run compares rc + first line only,
`c1-measure.py:154-181`).
Tool: **`('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')`** with
`CHECK runtime PASS vectors=15158 mismatched=0` (`line2-results.json`, `line2.rc=0`).

The divergence is real and observable (`fullstdout.json`, `fullstdout.rc=0`), at three of six vectors:

```
[1,0,…]    pristine: RC=1 / REGRESSION: FAIL … / REGRESSION_WORKDIR: r (kept)
           mutant  : RC=1 / REGRESSION: FAIL … / NOTE_AFTER_FIRST_LINE / REGRESSION_WORKDIR: r (kept)
[1,2,…]    same extra line;  [0,1,1,2,…] same extra line
```

**Mechanism and pointer.** The pinned tool compares the first stdout line and the exit code only —
documented at `tool.py:44-45` ("Exact stdout first line and exit code compared"), implemented at
`tool.py:268-287` (the `printf "R\t%s\t%s\n" "$rc" "${out%%$'\n'*}"` driver line at 281) and
`tool.py:290-302` (the oracle). Round 33's own lesson records this as an **open v3 class**: "DevPrintf: first-stdout-line-only
oracle — 7 survivors on lines 2+ (… injected note lines); whole-stdout compare … is the ninth measured v3
fix" (`corpus/lessons/round-33.md:61`; listed again at `:132`). Round 34's Holds, however, says
"whole-stdout comparison already landed as the r33 DevPrintf fix" (`corpus/lessons/round-34.md:59`). The
pin contradicts that sentence: no whole-stdout comparison exists in `7b11ba25…8d10`, and this probe is a
live specimen of the class surviving it.

**Verdict P4: co-failure / routing defect.** Both artifacts label this copy accept while its FAIL-path
stdout differs from the original. It is not a C1 falsification — the frozen accept set contains no line-2
change and the assigned copy is inert — but the "already landed" annotation is wrong and, left
uncorrected, would let round 35 drop a class that is still open. Recommended correction to the Holds line
(routed, not edited here): keep `whole-stdout comparison` on the v3 residue list.

## 6. Verdict summary

| probe | label | amended witness gate | real tool (`tally-audit-v2.py`) | read |
|---|---|---|---|---|
| `ho-accept-vector-inert-line` (assigned) | accept | `(True, 'vector-equivalence')` | `ACCEPT`, rc 0, all four checks PASS | **label honoured**; copy fully inert (full-stdout equal on 6/6 vectors) |
| `pristine.sh` baseline | — | — | `ACCEPT`, rc 0, identical CHECK lines | detector is not failing closed |
| variant A (`nfail`-branch note) | accept | `(True, 'vector-equivalence')` | `KILL`, rc 1, `runtime=fail`, 1800/15158 mismatches | **gate unsound** (tool correct) |
| variant B (head comment naming `st_js`) | accept | `(True, 'vector-equivalence')` | `KILL`, rc 1, `head=fail` (3 occurrences) | **tool false-kill** of a benign copy |
| variant C (line-2 note on FAIL path) | accept | `(True, 'vector-equivalence')` | `ACCEPT`, rc 0, all four checks PASS | **co-failure**; DevPrintf class still open |

C1's landed receipt stands: my assigned copy is a true accept, the tool accepts it, and the four checks are
green. The two gate-admits/tool-kills variants are admission-control defects (both caught by the tool at
measurement time, i.e. fail-closed), and the line-2 variant is a documentation/routing defect plus a
known open coverage class.

## 7. Restoration, containment, limits

- No in-place mutation was performed: each variant is a separate file under the scratch root, and
  `pristine.sh` was never rewritten — re-hashed after all runs at
  `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (= pin), with `tool.py`
  `7b11ba25…8d10` and the counter copy `f6b8868c…a07f28c` also unchanged. The frozen lane artifacts
  re-hash to their pins at the end of the seat (§1 table), and `ho-accept-vector-inert-line.json` is
  untouched at `edc3c69f…c7cd`.
- `git -C .../lane status --porcelain` produced 0 bytes (rc 0) after the clone/checkout and again after all
  probes; no git/jj write command ran anywhere; all writes are under the scratch dir and this report.
- `main()` was never executed and the counter was never run in default mode; the module was loaded with
  `importlib` (`spec.loader.exec_module`), so its `__main__` guard never fires. Only the named functions
  were called, on scratch copies.
- Limits: only the assigned copy was attacked, plus three constructed variants; the other 13 sealed copies
  were not probed here (their `set`/`witness` fields were read for context, and two of the accept copies'
  edits were read). Block-level equivalence of the
  assigned copy was checked over six representative vectors plus a diff, not all 15158 oracle vectors;
  "fully inert" rests on the diff (`:` expansion, no output) plus the vector sample. Each tool verdict was
  produced twice per copy (the counter's `run_tool_sandboxed` and an independent full capture of the same
  sandbox argv); both agreed every time.

## 8. Reproduce

```
cd /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectorinertline
python3 probe_gate.py       > gate-results.json    2> gate-results.err;     echo $? > gate.rc        # 0
python3 probe_tool.py       > tool-results.json    2> tool-results.err;     echo $? > tool.rc        # 0
python3 probe_line2.py      > line2-results.json   2> line2.err;            echo $? > line2.rc       # 0
python3 probe_fullstdout.py > fullstdout.json      2> fullstdout.err;       echo $? > fullstdout.rc  # 0
```

`probe_tool.py` calls `run_tool_sandboxed` for every copy and, in parallel, replays the identical sandbox
argv keeping `stdout` so the `CHECK` lines are visible. Evidence shas: `probe_gate.py`
`da51123d4cf89bd0f9e5319d2ab370c0a2ff060531796583e975d36a075447b0`, `probe_tool.py`
`5215ef0577d1d12643057dedf9cfc2afd82828c14dcfc55cb86549e7c0e1a023`, `probe_line2.py`
`58919e9b3db6bb59dd9a9b751cf65ffd2dc09a5b831ffdd6a139d9076ce5ee1c`, `probe_fullstdout.py`
`822c1ed6c05479223d2de37361b4599c3b2dcf47e654571fb162f6f0f3a60d00`, `gate-results.json`
`d017bb2bb3c7197047b7eaa9f4f3e557424135a3e8d3b317d152efde9f812334`, `tool-results.json`
`2741783a7ac826fb5842b0b535f4cbc9078f81b0d5a504a033b7621cd199ecda`, `line2-results.json`
`13965d85d2cae0d39689b8416c557795eb6be93d27737b5c1dc0ff7fc08479f1`, `fullstdout.json`
`3009b077dd75a0eecdd6646a349d9080b7126e324e4be6a7238c0030dbb25382`; variant JSONs
`e7bf6511a699d028e0bbc682750417b544ef83c0d2c5d9e317afc9a8fd8892d6` (A),
`bafb2dc49fc7fef7c02872523316509138796d041fced60b8e10c24e0f6601a2` (B),
`a771abceb63f434e39ac70c361734941f19361c35d47082dc0e4d7d500b713c0` (C); mutated runner copies
`mut-sealed.sh` `8f3b6032…2d29`, A `852f489a…dd7`, B `1fd84bec…5760`, C `dd87a9de…3e2`.

No tools were installed or upgraded during this seat.
