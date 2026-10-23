# Mutacceptheadcomment — sealed `ho-accept-head-comment` reproduces ACCEPT; one comment word makes the amended gate admit a copy the tool kills

Round 34 / wave 1 / mutation-tester seat. Lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`
(`git -C .../lane rev-parse HEAD`, checkout rc 0). Scratch root
`/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptheadcomment/`; the only writes are there and this
report file. No tool installed or upgraded. The lane stayed read-only (`git -C lane status
--porcelain` → 0 lines before and after; HEAD unchanged). The default-mode kill rule was never
invoked: the counter was imported as a module from the lane path and only `validate_ho`,
`apply_edits`, `ho_witness_ok`, `run_tool_sandboxed` (plus `CounterError`) were called, on scratch
copies. No subagent dispatch (leaf member).

## Verdict

| probe | expected detector | actual | verdict |
|---|---|---|---|
| assigned sealed copy `ho-accept-head-comment` (set=accept) | `ho_witness_ok` → `(True,'head')`; real tool → rc 0, `TALLY_AUDIT: PASS` | `(True,'head')`; `('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')` | **label honored — no defect for this copy** |
| adversarial head-edit family, same construction, different content | find a copy the amended gate validates as `accept` but the tool labels FAIL | found (comment naming a leg; inline comment; masking assignment) | **critical finding** |
| adversarial, reverse direction | copy the gate validates and the tool passes although the head is broken | found (comment merges into the next line, destroying the `bash-surface-census` call) | **critical finding** |

The deciding run stands: my reproduction of this copy is consistent with the receipt's
`ho_accept=6/6`. The findings below bound what `ho_witness_ok`'s accept+head branch can certify; they
do not change the contract and were not used to re-run the counter.

## 1. Setup and pins

Every substantive command's exit code was captured as `cmd; echo $? > file` (the setup chain is the
one `mkdir -p && git clone` exception, so `clone.rc=0` also means mkdir succeeded).

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptheadcomment && \
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane                 # clone.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach 0b99d48e…  # co.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show 0b99d48e…:tools/tally-audit-v2.py > tool.py       # tool_show.rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh   # sh_show.rc=0
sha256sum tool.py pristine.sh
```

| artifact | sha256 (measured) | pin | match |
|---|---|---|---|
| `tool.py` = `tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` = `mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| counter `c1-measure.py` (in the clone) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `f6b8868c…a07f28c` | YES |
| sealed `ho-accept-head-comment.json` (working tree) | `a08f7e21a9d74f5fffb9507d7582b55b28a8444b68369db0c5ce76242dcd69ba` | `git show c17e593b…:…heldout/ho-accept-head-comment.json \| sha256sum` → `a08f7e21…` | YES |
| sealed set commit | `c17e593 round-34: sealed held-out set authored after the amendment-6 counter freeze (8 must-kill + 6 must-accept…)` | `git log --oneline -3 c17e593b -- …/ho-accept-head-comment.json` | — |

`bwrap` `/usr/bin/bwrap` 0.13.1, `bash` 5.3.20, `python3` 3.14.8; the counter's sandbox path was
exercised on every copy (its `bwrap_argv` mounts `/usr /bin /lib /lib64 /etc` read-only and binds the
per-run workdir at `/w`). No installs.

## 2. Probe 1 — the assigned copy, `ho-accept-head-comment` (set=accept)

The edit's `old` `"  st_js=$?\n"` occurs exactly once in `pristine.sh` (line 1390; `start` at 1432;
`grep -c` = 1), so the counter's `apply_edits` accepts it. Bytes were re-derived with
`apply_edits(pristine, sealed['edits'])` (`probe.py`, `probe.rc=0`). sha256
`dc8fd28c60ad3b4c39e561240de603851098c8f45daa58a4ef6a5e560a2e1cb9`. One hunk, comment-only:

```diff
@@ -1388,6 +1388,7 @@
     "$root/js-kimi-census"
   st_js=$?
+  # tameshi sealed held-out accept A1 (inert head marker)
   regression_case_git bash-surface-census \
```

Witness gate: `ho_witness_ok(ho, pristine, mutated, work)` → **`(True, 'head')`** (accept+head branch,
counter lines 192–208: head differs, tally block byte-identical, set=accept). Real tool via
`run_tool_sandboxed(tool.py, copies/sealed-ho-accept-head-comment.sh, work)` → **`('ACCEPT', 0,
'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')`**.

Direct diagnostic run of the same tool bytes (`python3 -I tool.py --runner <copy>`, rc 0) gives the
per-check detail:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Pristine baseline, same detector: `run_tool_sandboxed(tool.py, pristine.sh, work)` → `('ACCEPT', 0,
PASS)`; the restored-bytes run after all probes → `('ACCEPT', 0, PASS)`. Baseline and restored agree,
so a mutant failure would have been attributable (none occurred for the assigned copy).

## 3. Adversarial constructions (set=accept, witness kind=head, same head-edit family)

Each JSON was produced with `validate_ho` → OK and `apply_edits` (old string exactly once); each was
run through `ho_witness_ok` under **both** declared sets and through `run_tool_sandboxed`; ground truth
was established by diff plus a bash region harness. Files live in `copies/`.

| id | sha256 (copy bytes) | witness accept | witness kill | tool (sandboxed) | behavior vs pristine |
|---|---|---|---|---|---|
| sealed (probe 1) | `dc8fd28c…a2e1cb9` | `(True,'head')` | `(False,'head-edit-cannot-kill')` | ACCEPT rc 0 | identical (comment) — label correct |
| `adv-comment-names-leg` | `20d3f480…b4195ada8` | `(True,'head')` | `(False,'head-edit-cannot-kill')` | **FAIL rc 1** (head) | identical (comment) — **tool wrong** |
| `adv-comment-other-leg` | `1a9c8b6d…a9acb7e3` | `(True,'head')` | `(False,'head-edit-cannot-kill')` | **FAIL rc 1** (head) | identical (comment) — **tool wrong** |
| `adv-comment-out` | `93f4689c…b3c6f3ae` | `(True,'head')` | `(False,'head-edit-cannot-kill')` | **FAIL rc 1** (head) | identical (comment) — **tool wrong** |
| `adv-inline-comment` | `05beefe1…070e2a37` | `(True,'head')` | **`(True,'head-leg-assignment')`** | **FAIL rc 1** (all four) | identical (comment) — **tool wrong; gate accepts a kill label for an inert copy** |
| `adv-mask-assign` | `c8615c3e…e7c8c5499` | `(True,'head')` | **`(True,'head-leg-assignment')`** | FAIL rc 1 (head) | lethal (`st_js=0`) — tool right, **gate accept wrong** |
| `adv-trailing-comment` (merge) | `61fcbe2c…d19b5dfa` | `(True,'head')` | `(False,'head-edit-cannot-kill')` | **ACCEPT rc 0** | **broken head** (kagi call swallowed) — **tool wrong; gate accept wrong** |
| `adv-comment-swallow` (control) | `3d2363bb…d1888f9c` | `(True,'head')` | `(False,'head-edit-cannot-kill')` | ACCEPT rc 0 | identical — control: a comment line alone cannot swallow the following line |

(label-matrix runs: `probe.py`, `probe3.py`, and two inline label-swap snippets; all rc 0.)

### 3.1 The critical construction (same family, different content)

`adv-comment-names-leg.json` — byte-for-byte the sealed construction (an own-line comment appended
after `st_js=$?`), differing only in the comment text:

```json
{
 "author": "tameshi seat (mutacceptheadcomment, adversarial)",
 "edits": [
  {"new": "  st_js=$?\n  # st_js inert marker\n", "old": "  st_js=$?\n"}
 ],
 "id": "adv-comment-names-leg",
 "note": "full-line comment exactly like the sealed one, differing only by naming a leg",
 "set": "accept",
 "witness": {"kind": "head"}
}
```

* Gate: `validate_ho` OK; `ho_witness_ok` → `(True,'head')` (identical block, head changed).
* Tool: `('KILL', 1, 'TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)')`.
* Detail: `CHECK head FAIL legs=9; leg st_js appears 3 times in the head (want exactly 2: the local
  declaration and its bare st_x=$?)` — the twice-only substring count at `tally-audit-v2.py:328-334`.
* Ground truth: comment-only diff; the copy executes exactly like pristine. Bash demo: `f(){ return 3; };
  f; a=$?  # inert marker` → `a=3` (rc 0).
* Consequence: if a sealed accept copy were authored with a comment that names a leg (e.g.
  `# st_js is the census leg`), `ho_invalid` stays 0 and the copy enters `ho_at`, but the tool returns
  FAIL → `ho_a < ho_at` → `C1_R33_PASS=false`. The sealed copy passes only because its comment text
  happens not to contain a leg name.

`adv-inline-comment.json` is the same family with the comment on the assignment line:

```json
{"new": "  st_js=$?  # inert marker\n", "old": "  st_js=$?\n"}
```

Tool: `FAIL (head=fail static=fail runtime=fail harness=fail)`; detail `non-bare leg assignment(s) in
the head: st_js=$?  # inert marker` (`tally-audit-v2.py:313-320`) then cascading `legs=8` failures.
The assignment is still correct in bash (`f; b=$?  # c` → `b=3`), so this is a false kill.

### 3.2 The gate-permissiveness construction

`adv-mask-assign.json`:

```json
{"new": "  st_js=$?\n  st_js=0\n", "old": "  st_js=$?\n"}
```

* Gate: `set=accept` → `(True,'head')`; `set=kill` → `(True,'head-leg-assignment')`. **The same bytes
  validate under both labels** — the verdict is a function of the declared set, not of the bytes'
  behavior.
* Tool: `FAIL (head)` — `non-bare leg assignment(s) in the head: st_js=0; leg st_js assigned 2 times`.
  Tool is right; the gate would have certified the dishonest accept label.
* Root: accept+head only requires `mb == pb` (block identity) and `head_of(mutated) != head_of(pristine)`
  (`c1-measure.py:192-208`); no check that the head edit is behavior-preserving. The comment in the
  gate ("a lethal ride-along behind a benign head edit is refused") holds only for block edits.

### 3.3 The false-accept construction

`adv-trailing-comment.json` (comment with no trailing newline, so the next line merges into it):

```json
{
 "edits": [{"new": "  st_js=$?\n  # inert marker", "old": "  st_js=$?\n"}],
 "id": "adv-trailing-comment", "set": "accept", "witness": {"kind": "head"}
}
```

Diff (one line replaced):

```diff
-  regression_case_git bash-surface-census \
+  # inert marker  regression_case_git bash-surface-census \
```

The `bash-surface-census` call head is now a comment; its continuation lines execute as commands.
Region harness (`region_demo_rc=0`, extracted `st_js=$?` … `st_kagi=$?` with a stub
`regression_case_git` returning 7):

```
pristine        -> CALL <bash-surface-census>   st_kagi=7   calls=1
merged-comment  -> (no call)                    st_kagi=127 calls=0
```

* Gate: `(True,'head')` for set=accept; `(False,'head-edit-cannot-kill')` for set=kill, although the
  copy is genuinely broken — the honest kill label is refused because the leg surface is unchanged.
* Tool: `('ACCEPT', 0, 'TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)')`. Every
  check passes because all nine bare `st_x=$?` lines are intact and only the tally block is audited
  (`run_tool_sandboxed` invokes the tool in default mode, never `--then-regression`).
* Consequence: this copy is a must-kill defect that the gate certifies as `accept` and the tool passes.
  Labeled kill (its true class), the gate refuses the label (`ho_invalid` becomes 1, which alone turns
  `C1_R33_PASS` false); labeled accept, it is laundered into the accept total with a PASS.

Control `adv-comment-swallow` (a comment line that repeats the call opening, with its own newline)
stays inert: the original call line still runs, tool ACCEPT, gate accept — so the 3.3 break is caused
by the swallowed line, not by comment text alone.

## 4. Findings

**F1 (critical, gate): the accept+head branch certifies any head edit whose tally block is identical.**
It validates (a) inert comments the tool kills (`adv-comment-names-leg`, `adv-comment-other-leg`,
`adv-comment-out`, `adv-inline-comment`), (b) lethal masking (`adv-mask-assign`), and (c) a head that
no longer runs a regression case (`adv-trailing-comment`). For (b) — and for the inert inline comment —
it validates the same bytes under set=kill as well; the gate is not label-injective and cannot tell
benign from lethal head edits. The kill+head leg-surface diff (counter lines 197–207) refuses the
honest kill label for (c) while accepting the inert inline comment as a kill. Reproduce:
`python3 probe.py`, `python3 probe3.py`, `python3 probe2.py`.

**F2 (tool, false-kill class): `check_head` rejects behavior-preserving comment placements.**
The twice-only substring rule (`leg %s appears %d times in the head`, tool line 334) fires when a
comment merely names a leg; the non-bare scan (tool line 320) fires for a trailing comment on the
assignment. Both copies are behaviorally identical to pristine (comment-only diffs; bash demo above),
so the tool's FAIL is not a true detection. If one such copy is sealed as accept, the gate validates
it (`ho_invalid` unchanged) and `C1_R33_PASS` turns false.

**F3 (tool, false-accept class): a head-region defect can leave the audit green.**
`adv-trailing-comment` disables `regression_case_git bash-surface-census` while keeping all nine bare
captures; head/static/runtime/harness all pass and the tool returns PASS. Default mode never runs the
runner (`run_tool_sandboxed` argv is `python3 -I /w/tool.py --runner /w/copy.sh`; `--then-regression`
is not used by the counter), so the dead case is invisible.

These are coverage findings. They do not authorize any change to the frozen tool, counter, or sealed
set this wave; the measurement-only v3 residue classes in `corpus/lessons/round-34.md` are untouched.

## 5. Bounds, restoration, and reproduction

* Lane read-only: `git -C lane status --porcelain | wc -l` → `0` before and after; HEAD
  `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` unchanged. No git/jj write commands were run anywhere;
  the clone and its detached checkout are inside the scratch dir (per the task's setup line).
* Pinned bytes never modified: `sha256sum tool.py pristine.sh` after every probe →
  `7b11ba25…598d10` / `a7d3f2dd…12eb9` (identical before/after; `probe.log` `RESTORE` line). Every
  mutant is a separate file under `copies/`; nothing needed restoring in place.
* No default-mode counter run: only `validate_ho`, `apply_edits`, `ho_witness_ok`,
  `run_tool_sandboxed` were imported and called, from the lane clone path.
* No model parameter, no `agent://all`, no subagents, no installs.

Reproduce (from the scratch root; all rc 0):

```
python3 probe.py     # sealed copy + first adversarial batch; writes results.json, probe.rc=0
python3 probe2.py    # corrected inline variants + per-copy CHECK detail; results2.json, probe2.rc=0
python3 probe3.py    # corrected own-line comment naming st_kagi; results3.json, probe3.rc=0
```

Label matrix (set=accept vs set=kill on the same bytes) is a 20-line snippet calling
`ho_witness_ok` twice per copy with only `ho['set']` changed; outputs are quoted in §3 and the table.
The region harness that proves the merged-comment break reproduces with the extraction shown in §3.3.
