# Mutacceptvectortailcomment — sealed accept copy re-derived; same-family inert comments that the tool rejects anyway

Round 34 / wave 1 / mutation-tester seat (v2 wave, C1 operability). Lane tip:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Scratch (all writes here + this file):
`/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectortailcomment/`. No tools installed or
upgraded; no network; lane read-only; the default-mode kill rule was never invoked (only the
counter imported as a module, functions called on scratch copies).

## 1. Setup and pins

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectortailcomment
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../Mutacceptvectortailcomment/lane   # rc=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                            # checkout_rc=0
git -C .../lane rev-parse HEAD -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7             # rc=0
git -C .../lane show HEAD:tools/tally-audit-v2.py  > tool.py                          # show_tool_rc=0
git -C .../lane show HEAD:tools/mutate-and-run.sh  > pristine.sh                      # show_runner_rc=0
sha256sum tool.py pristine.sh                                                         # rc=0
```

| artifact | sha256 (observed) | pin | match |
|---|---|---|---|
| `tool.py` = `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` = `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `.ufo/evidence/round-33/c1/c1-measure.py` (counter, imported) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amend-6 rev | YES |
| `.ufo/evidence/round-33/c1/controls-receipt.json` | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` | untouched | — |
| `.ufo/evidence/round-33/heldout/ho-accept-vector-tail-comment.json` | `d23afb234c4a0dd643805c48ac32e2c4c0007b219ceb9fdf551dfa69e5022bfd` | untouched | — |

The counter is imported from the lane path (`lane/.ufo/evidence/round-33/c1/c1-measure.py`,
which resolves its `../../round-32/c1-measure.py` inside the clone); no counter file is edited
or executed in default mode.

## 2. Assigned probe — `ho-accept-vector-tail-comment` (set=accept)

Sealed copy's single edit (anchor count in `pristine.sh` = 1, asserted by `apply_edits`):

```json
{"old": "  fi\n  exit 0\n}\n",
 "new": "  fi\n  # tameshi sealed held-out accept A6 (unreachable marker)\n  exit 0\n}\n"}
witness: {"vector": [0,0,0,0,0,0,0,0,0]}
```

Re-derived runner bytes: `106597` bytes,
sha256 `2a2b73053bb55ec132d5ed5aae868a7d0315d3b174ae7257c08152cd5357f477`.

Detectors, both on the same re-derived copy (`python3 probe.py sealed`, `sealed.probe.rc=0`):

```
witness=(True, 'vector-equivalence')
tool_outcome='ACCEPT' rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
copy_sha_before=2a2b7305…f477 copy_sha_after=2a2b7305…f477 restored=True
```

**Verdict: label holds — the accept copy is accepted, not killed.** Witness validator and the
real tool (through `run_tool_sandboxed`) agree. Copy bytes are identical before/after the runs
(the tool copies into its own sandbox workdir).

## 3. Adversarial probes (same family: one inert line added to the tally block)

Each variant below is a single added line in the tally block, `set=accept`, witness
`{"vector": [0]*9}` (the sealed witness kind). Same two detectors, same scratch boundary
(`probe.py variant variant-<X>.json`; every `variant-*.probe.rc=0`).

| id | construction (one added line) | witness | tool | rc | last line |
|---|---|---|---|---|---|
| A | `# scope {head, tally} (inert marker)` at sealed anchor | `(True,'vector-equivalence')` | ACCEPT | 0 | `PASS (head=pass static=pass runtime=pass harness=pass)` |
| B | `# tally close } (inert marker)` at sealed anchor | `(True,'vector-equivalence')` | ACCEPT | 0 | same PASS |
| **C** | `# tally complete } (inert marker)` **after the tally loop, before the guard** | `(True,'vector-equivalence')` | **KILL** | **1** | **`FAIL (head=pass static=pass runtime=fail harness=pass)`** |
| **D** | `# case $st in 0) npass=$((npass + 1)) ;; 1) nfail=$((nfail + 1)) ;; esac` at block start | `(True,'vector-equivalence')` | **OTHER** | **2** | **`SETUP (no loop governing the counting case)`** |
| E | `# for st in "$st_js"; do` at sealed anchor | `(True,'vector-equivalence')` | ACCEPT | 0 | same PASS |
| F | `st_js=0` (not a comment) at sealed anchor | `(True,'vector-equivalence')` | KILL | 1 | `FAIL (head=fail static=pass runtime=pass harness=pass)` |

A and B show the sealed anchor is insensitive: a `}` in the tail comment truncates the audited
body only after the final `exit 0` (no observable rc/first-line change), and a `{` extends the
body past EOF where the tally's earlier `exit` makes the swallowed tail unreachable. C moves the
same inert marker four lines earlier and the truncation then removes the whole guard/printf
section. E is ignored because the tool's loop regexes are line-anchored (`#` precedes `for`).

### 3.1 Critical finding — variant C (`variant-C.json`,
sha256 `727e0703ad750e3aa7ba7ca4de96c654c5a9487abfb3818f082a5c686df243ec`)

```json
{
 "id": "adv-accept-vector-tail-comment-C",
 "author": "tameshi-shokunin r34 mutation seat (Mutacceptvectortailcomment)",
 "set": "accept",
 "edits": [
  {
   "old": "  done\n\n  if [[ $nfail -gt 0 ]]; then\n",
   "new": "  done\n  # tally complete } (inert marker)\n\n  if [[ $nfail -gt 0 ]]; then\n"
  }
 ],
 "witness": {"vector": [0,0,0,0,0,0,0,0,0]}
}
```

Copy sha256 `cb6fee5cbf7463bcc15d69b66d34e5e2860c85029339d84974355dd0e8310ced` (106574 bytes),
inserted at line 1440 of the copy. The full-file diff is exactly one added comment line
(`diff -u pristine.sh variant-C.sh`, `variant-C.diff.rc=1` = files differ):

```
@@ -1437,6 +1437,7 @@
       *) nsetup=$((nsetup + 1)) ;;
     esac
   done
+  # tally complete } (inert marker)
```

**Inertness proof (counter's own `block_run`, real bwrap boundary).** `equivalence.py`
(`equivalence.rc=0`) ran the pristine block and the variant-C block over 133 vectors — all 55
(failing, setup) count-pair representatives, every position with statuses {0,1,2,3,127,255}, and
extreme co-occurrence pairs at 4 position pairs:

```
block differs by lines: pristine_lines=39 mutated_lines=40   (one-line hunk above)
EQUIV vectors=133 mismatches=0
```

The sealed vector `[0]*9` is inside that set. This copy is behaviorally identical to pristine on
every sampled vector; the amended `ho_witness_ok` is right to validate it as accept.

**Tool failure mechanism (comment text parsed as code).** `tally-audit-v2.py` extracts the block
with `regression_body()` (char-wise brace counting) + `tally_block()` (`rfind('}')`); comments are
not skipped. The `}` inside the comment closes `run_regression()` early:

```
TOOL_PARSER body_chars=5648 body_last80='…    esac\n  done\n  # tally complete }'
TOOL_PARSER block_chars=333 block_last80='…    esac\n  done\n  # tally complete '
```

The audited block therefore stops after the counting loop (no guard, no printf, no exit), and
`check_runtime` compares it to the oracle for every vector. Direct run on the copy
(`python3 -I tool.py --runner variant-C.sh`, `variant-C.tool.out`, rc saved as 1):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime FAIL vectors=15158 mismatched=15158; first: cfg(0,1) statuses 0 0 0 0 0 0 0 0 0:
      got (0, ''), want (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
```

So a legal, bash-inert comment containing `}` between the tally loop and the guard makes the
frozen tool reject a behaviorally pristine runner. The amended witness gate says accept; the tool
says FAIL. Reproduce with:

```
python3 probe.py variant variant-C.json            # variant-C.probe.rc=0
python3 equivalence.py                             # equivalence.rc=0
python3 -I tool.py --runner variant-C.sh; echo $?  # 1
```

### 3.2 Second construction — variant D (`variant-D.json`,
sha256 `ddfea0b86ef8e035d7950e4079b3add7d5e5ac6d241b77cc30a0bbc7d4ee8428`)

```json
{
 "id": "adv-accept-vector-tail-comment-D",
 "author": "tameshi-shokunin r34 mutation seat (Mutacceptvectortailcomment)",
 "set": "accept",
 "edits": [
  {
   "old": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  for st in",
   "new": "  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n  # case $st in 0) npass=$((npass + 1)) ;; 1) nfail=$((nfail + 1)) ;; esac\n  for st in"
  }
 ],
 "witness": {"vector": [0,0,0,0,0,0,0,0,0]}
}
```

Copy sha256 `3b40016b10aaf92cbe3531feb8fd353f1b2bf4e7cfff1af5f3f2f52f945ae9ac`. Inert on the
same 133-vector sweep (`D EQUIV vectors=133 mismatches=0`, `D_equiv_rc=0`). The tool's
`counting_case()` scans comment text (its `CASE_RE`/`COUNTER_INC_RE` are not line-anchored):

```
D counting_case -> 'case $st in 0) npass=$((npass + 1)) ;; 1) nfail=$((' var='st'
D tool exception: CannotAudit: no loop governing the counting case
```

The forged case is the first `case` in the block but no loop contains it, so the tool prints
`TALLY_AUDIT: SETUP (no loop governing the counting case)` and exits 2. For an accept-labelled
copy, exit 2 is not acceptance: under the counter's own predicate (`rc==0 and last.startswith
('TALLY_AUDIT: PASS')`) this valid copy scores as a miss. Same root cause as C — inert comment
text is treated as code — different construction (forged counting case instead of brace).

### 3.3 Witness-gate observation — variant F (`variant-F.json`,
sha256 `0baecfdb7f28ceb75c780709a9135ddee14cff201bc6c5c0aa07bb79da0bf998`)

```json
{
 "id": "adv-accept-vector-tail-comment-F",
 "author": "tameshi-shokunin r34 mutation seat (Mutacceptvectortailcomment)",
 "set": "accept",
 "edits": [
  {
   "old": "  fi\n  exit 0\n}\n",
   "new": "  fi\n  st_js=0\n  exit 0\n}\n"
  }
 ],
 "witness": {"vector": [0,0,0,0,0,0,0,0,0]}
}
```

Copy sha256 `4453223b20491ed1d3ec25566e2c21c2327e06410f16bfd2a0f88943fcb15b2e`. The line is
behaviorally dead (it sits after every `exit` path, before the final `exit 0`): `block_run` is
identical to pristine on `[0]*9`, `[1,0…]`, `[0,1,0…]`, `[2,0…]` (all four compared, no
mismatch). The tool kills it at the head rule (`FAIL (head=fail static=pass runtime=pass
harness=pass)`) because the tool's documented head contract rejects "any other assignment to a
leg var … outside the identified tally loop's operand list". This is not a tool defect — it is
the documented static rule — but it shows the `accept+vector` gate is behavioral-only: it
validates copies that the tool's static contract rejects, so an accept-labelled copy can pass the
gate and still score as a miss. `[INFERENCE]` that no inflating direction exists: the gate cannot
admit a must-kill copy here (the tool decides; the gate only filters).

## 4. What this establishes for C1

- The assigned sealed copy behaves exactly as labelled: mutated bytes
  `2a2b7305…f477`, witness `(True,'vector-equivalence')`, tool `ACCEPT` rc 0, PASS line.
  Nothing here contradicts the deciding receipt
  (`ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true`).
- The frozen tool has a **demonstrated false-reject class for legal inert comments inside
  `run_regression`**: (i) a `}` in a comment before the guard truncates the audited block and
  fails `runtime` on a behaviorally pristine runner (variant C, 15 158/15 158 vectors
  mismatched); (ii) a comment mentioning `case … npass=$(( … nfail=$(( … esac` before the loop is
  seized as the counting case and the tool refuses to audit (variant D, exit 2). Both copies are
  byte-different from pristine by exactly one comment line and behaviorally identical on the
  133-vector sweep.
- Counterfactual, marked `[INFERENCE]` and grounded on §2–§3 runs: had any of the 6 sealed accept
  copies carried such a comment, the deciding run would have printed `ho_accept=5/6` and
  `C1_R33_PASS=false`; conversely the must-kill side is not at risk (C kills, D refuses, neither
  accepts). The sealed set as committed does not carry such comments, so the landed measurement
  stands. This is a coverage/robustness finding against the tool's parser, not evidence that the
  deciding run is wrong, and it is not permission to change the contract or the pinned tool.
- Suggested (not applied; tool is byte-pinned, NO tool edits this wave): skip bash comments (and
  quoted text) before `regression_body`/`counting_case` extraction, e.g. strip full-line comments
  and mask `#` spans before brace/case analysis, then re-run the frozen acceptance panel.

## 5. Restoration and containment

| stage | sha256 of the copy the tool saw | tool outcome |
|---|---|---|
| pristine baseline (`restore-pristine-baseline.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT rc 0 |
| variant-C mutated (`restore-variant-C-mutated.sh`) | `cb6fee5cbf7463bcc15d69b66d34e5e2860c85029339d84974355dd0e8310ced` | KILL rc 1 |
| variant-C restored (`restore-variant-C-restored.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT rc 0 |

`python3 restore_probe.py` → `restore.rc=0`; `restored=True` on every trial (the tool copies the
copy into its sandbox workdir and never writes back). No mutant bytes remain in the scratch copy
used for the restored trial.

- Frozen artifacts re-hashed after all runs: tool `7b11ba25…8d10`, runner `a7d3f2dd…2eb9`,
  counter `f6b8868c…a07f28c`, controls receipt `f1e62421…de3aa`, sealed copy
  `d23afb23…22bfd` — all as pinned/untouched (`frozen_sha_rc=0`).
- `git -C lane status --porcelain` empty (`lane_status_rc=0`); no git/jj write command was run
  anywhere; no sibling repo touched; the default-mode counter command was never run (only module
  import + `apply_edits` / `tally_block_of` / `block_run` / `ho_witness_ok` / `run_tool_sandboxed`
  on scratch copies).
- No tool installs or upgrades (nothing needed; `bwrap`, `timeout`, `python3` already present).

## 6. Evidence files (scratch, `/fast/scratch/hyaku/tameshi-r34-seats/Mutacceptvectortailcomment/`)

`probe.py` (`9610b1f9…c433`), `equivalence.py` (`d62a3d8c…0d8c`), `restore_probe.py`
(`657bb3a9…a150`), `sealed.probe.log`/`.rc=0`, `variant-{A..F}.probe.log`/`.rc=0`,
`variant-C.json` (`727e0703…43ec`), `variant-D.json` (`ddfea0b8…8428`), `variant-F.json`
(`0baecfdb…b998`), `variant-C.sh` (`cb6fee5c…0ced`), `variant-C.diff`/`.rc=1`,
`variant-C.tool.out` (direct tool, exit 1), `equivalence.log`/`.rc=0`, `restore.log`/`.rc=0`,
`pins.sha256`/`.rc=0`.
