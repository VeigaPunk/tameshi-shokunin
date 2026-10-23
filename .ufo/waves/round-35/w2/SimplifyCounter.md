# Round-35 w2 — SimplifyCounter

Seat: `tameshi-r35-w2-SimplifyCounter` (leaf simplifier, godspeed). Lane tip at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`; **attacked bytes = the counter in force at HEAD
`68f25573d075d04189158e7eac76408b0e0a981f`**, sha256
`d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2` (amendment A6 re-pin,
commit `f9df589`). The dispatch-tip bytes `515b0b1b…` differ by exactly one line
(`TOOL_SHA256` `da23d3a2…` → `ef98fc53…`); every finding below holds for both blobs —
the diff never touches the attacked paths. Contract `frozen_artifacts.c1_counter_sha256`
at HEAD agrees: `d27e6769…`.

Slice assigned: attack the C1 counter's size — identify code paths that cannot change
`C1_R35_PASS` (dead branches, unused parameters, redundant checks), prove each by a
targeted edit in a COPY of the counter with the predicate re-evaluated. Report
candidates; never apply.

All scratch under `/fast/scratch/hyaku/tameshi-r35-seats/SimplifyCounter/` (lane checkout
`lane/` read-only at `7da6e076`; a second throwaway clone `lane-w/` carried my own local
fixture commits — never the lane). No tool installs; `pacman` untouched; no git mutations
outside `lane-w`.

## Rig (how each deletion was proven)

- `lane-w` = scratch clone at HEAD + one local commit `986b56e0a10450204b186459d7209f960c96e975`
  adding `.ufo/evidence/round-35/c1/sealed/` = a **synthetic held-out set** (the 8 public
  panel JSONs + `manifest.json` naming `freeze_rev = d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`,
  the commit that first added `contract.json`). This exercises the complete deciding-mode
  predicate: both loaders, the full behavior oracle, all 16 tool invocations, and every
  A5 provenance conjunct.
- Per candidate: one edited copy of the counter (`variants/dNN.py`), run as
  `python3 variants/dNN.py --lane lane-w --rev 986b56e0… --work runs/dNN/work --sealed .ufo/evidence/round-35/c1/sealed`
  with a fresh empty work dir; receipt compared to the untouched-counter run.
- Condition-isolated fixture commits on `lane-w` for candidates dead only under specific inputs:
  `bfce22d0` (adds `sealed-empty/` = manifest only) and `69299e55` (adds `sealed-bare/` +
  removes `tools/tally-audit-v3.py` → tool-absent path, near-zero cost), `351e6452`
  (tool restored; public panel replaced by ONE bare doc without a `"copies"` wrapper —
  the minimal `_docs_to_copies` discriminator).
- **Negative control** (`variants/neg.py`: `diverge()` returns `[]`) proves harness
  sensitivity: all 10 kill copies scored `INVALID`, `C1_R35_PASS=false`, exit 1.

## Baseline (untouched counter, deciding mode, synthetic sealed set)

```
python3 variants/base.py --lane lane-w --rev 986b56e0… --work runs/base/work \
    --sealed .ufo/evidence/round-35/c1/sealed   →  exit 0
C1_R35: mode=deciding tool_present=1 tool_sha=ef98fc5367cdb12c tool_sha_ok=1 runner_sha_ok=1
pub_kill=5/5 pub_accept=3/3 pub_slots=8 pub_distinct=8 ho_kill=5/5 ho_accept=3/3 ho_invalid=0
ho_distinct=8 sealed_after_freeze=1 rev=986b56e0… C1_R35_PASS=true
```

Claim-critical rows reproduced: both A4 root-keyed kills diverge under exactly the
real-auto-root triples — `root-keyed-auto-mask`/`root-keyed-auto-zero` `div=(1,0),(1,1)`,
killed with `checks=runtime` alone; `workdir-branch-swap` `div=(1,0),(0,0)`;
`cfg00-accept-swap` `div=(0,0)`; `cfg11-pass-mask` `div=(1,1)`; all 6 accept copies
`rc=0 div=-`. Wave-1 wall 337 s for 16 parallel deciding runs; wave-2 196 s for 8.

## Findings (ranked)

### CRITICAL — none

No claim is false. Under the deciding predicate the counter is correct on every input
exercised, and the A4/A5 apparatus holds: root-keyed kills diverge only under the real
root triples and die at `runtime`; sealed provenance (manifest freeze binding, strict
ancestry, `--follow --diff-filter=A` lineage, committed-bytes scoring) all evaluated
live in the runs above.

### BOUND-1 — sealed provenance is keyed on the copy's self-declared `file` field, not the committed filename

`_docs_to_copies` (c1-measure.py:227) uses `c.setdefault('file', fn)` — a specimen JSON
may carry its own `"file"` value, and the per-file provenance check (line 414:
`fpath = '%s/%s' % (srel, c['file'])`) then inspects THAT path's history, not the path
the bytes were loaded from (`load_copies_rev` never records the source path). A copy
loaded from a pre-freeze-committed path can name any post-freeze path and pass the gate —
fail-open for provenance, gated only by the practical scarcity of pre-freeze JSON files
inside `sealed/`. No landed specimen uses the field (census: all 8 `file_field=None`);
the sealed schema is Seat-authored so this is an L1-authoring-trap class, not an
authoring-seat evasion. Fix direction (post-data): derive `fpath` from the ls-tree name,
or reject copies whose declared `file` disagrees with it.

### BOUND-2 — deleting the empty-sealed guard flips `sealed_after_freeze` 0→1 on an empty set

`if not ho: sealed_ok = False` (lines 428-430) is verdict-dead — an empty sealed set
already fails via `ho_kill_total >= 4` — but it is not receipt-dead: at `bfce22d0`,
base prints `SEALED-SET-EMPTY` + `sealed_after_freeze=0` while the deletion variant
prints `sealed_after_freeze=1` (provenance "OK" on an empty set). The field means
"sealed set exists AND descends from the freeze"; dropping the guard makes a missing
sealed set receipt-indistinguishable on that field. Keep (receipt honesty).

## Deletion candidates — PROVEN, verdict- and receipt-identical (recommend)

Each was proven by a full deciding-mode run; `cmp` vs the baseline stdout is
byte-identical (all 20 lines: 16 COPY lines + provenance + receipt). Candidates
marked ★ are dead on **all** inputs, not merely on this panel (proof sketched with each).

| # | Path (lines in `d27e6769`) | Class | Proof |
|---|---|---|---|
| 1 | `SEP = '\x1f'` (line 55) | unused constant ★ | zero references anywhere; d01 exit 0, stdout identical |
| 2 | `FREEZE_REV = '__FREEZE_REV__'` (line 47) | unused constant ★ | zero references; superseded by A5's contract-first-add lookup (its own comment "filled at freeze" is stale); d02 identical |
| 3 | `git_ok(..., 'merge-base', '--is-ancestor', last, rev)` conjunct (line 423) | tautological check ★ | `last` is output of `git log <rev>` — a reported commit is an ancestor of `<rev>` by construction; d03 identical at rev1; d03t byte-identical at tool-absent rev `69299e55` |
| 4 | `rev != first` conjunct (line 409) | unreachable check ★ | if `rev == first`, every sealed file's `last` touch IS `first` → `last == first` fails each file (or `ho` is empty); the conjunct can never be the sole decider; d04 identical at rev1; d04t identical at `69299e55` |
| 5 | `git_ok(..., 'merge-base', '--is-ancestor', first, rev)` conjunct (line 409) | tautological check ★ | `first` comes from `git log <rev> --diff-filter=A` — same construction as #3; d16 identical at rev1; d16t identical at `69299e55` |
| 6 | `load_copies(directory)` (lines 235-245) | orphaned function ★ | zero call sites since `7267738` (A4/A5 moved both loads to `load_copies_rev`; last caller was `load_copies(panel_dir)` at `d16f9b5`); greps across the tree show the counter is invoked only as the counting command — nothing imports it; d05 identical |
| 7 | duplicate all-zero vector: `for s in range(0, 256)` re-appends `[0]*n` already seeded at line 191 → `range(1, 256)` | redundant computation ★ | `run_block` compares element-wise; a duplicated element cannot change `diverge` (saves 16 tally runs per `behavior()` call); d07 (fixed form) identical |
| 8 | `run_tool`'s 4th return `out` (line 282) + `rc, failed, last, _ =` (line 303) | dead return slot ★ | sole caller discards it; d10 identical |
| 9 | tool-absent synthetic pub rows `results['pub'] = [{…} for c in pub]` (lines 390-391) → `[]` | dead diagnostic ★ | the only consumer is `counted()`; `pub_kill`/`pub_accept` are 0 either way — **byte-identical stdout under the tool-absent rev `69299e55`** (b3 ≡ d14t), not just at rev1; d14 identical |
| 10 | combined d17 = #1-#6,#8,#9 (minus zero-dup variant) | — | d17 (447 lines vs 464) exit 0, stdout byte-identical at rev1; d17t byte-identical at `69299e55`. sha256 `7cc15e499ad1b1a0d59f6e63bffe2ef07b2825fe621c2e3139372f418183e0bb` |

## Proven verdict-identical but REJECTED (deletion would harm another axis)

| Path | Panel verdict | Why rejected |
|---|---|---|
| `auto_root()` recreate: `elif not os.path.isdir(AUTO_ROOT[0]): os.makedirs(...)` (69-70) | identical (d08) | live for sealed classes: the tally block `rm -rf "$root"`s on PASS under `(auto=1,KEEP=0)`; a sealed specimen that reads `$root` existence would see a state the real runner never produces (real auto root always exists at block entry). The elif preserves oracle fidelity; cost is one `makedirs` per cfg. KEEP |
| `_docs_to_copies` else-branch (bare doc without `"copies"`) (229-231) | identical (d09) | **live, proven**: at `351e6452` (panel = one bare doc) base scores `pub_accept=1/1`, d09 scores `0/0`. A bare-doc sealed specimen would be silently dropped → fail-closed but ho counts corrupted. KEEP |
| `vectors_for` `if len(v) == n` filter (199-200) | identical (d11) | live for `n<2` specimens: drops the two length-2 vectors from a 1-leg panel, changing `diverge`. The runner pins nlegs=9 today but the oracle is specimen-general. KEEP |
| `if not ho: sealed_ok=False` (428-430) | identical (d12) | BOUND-2 above: receipt-semantics change on the empty-sealed input. KEEP |
| `atexit.register(rmtree(auto_root))` (68) | identical (d13) | deletes `/tmp/tameshi-r4-2-regression.*` litter discipline; removal is silent resource leak for zero gain. KEEP |
| `os.listdir(a.work)` empty-work gate (346-348) | identical (d15) | enforces the counting command's documented `EMPTY_DIR` precondition; removing it weakens contract enforcement for zero gain. KEEP |
| `score_copies` per-copy `behavior(runner_text)` → hoisted once (294-297) | identical (d06, `os.makedirs(pdir, exist_ok=True)` fix) | halves oracle cost and matches the tool's own pristine-once convention; rejected only on a marginal sealed boundary: a specimen writing into the shared oracle `cwd` could make copy-adjacent pristine runs differ from a once-computed pristine (ordering, not correctness). Listed for the L1's call, not adopted into d17. |

## What I could NOT break (with proof)

- The deciding verdict under every proven deletion: 13/15 single-edit variants +
  combined d17 print `C1_R35_PASS=true` with **byte-identical stdout** to the untouched
  counter (`cmp -s` verified). The two non-identical runs were my own buggy edits
  (d06 `os.mkdir` collision → `FileExistsError`; d07 deleting the zero vector outright →
  the `workdir-branch-swap` kill losing its only divergence), fixed and re-proven —
  they additionally demonstrate the harness catches real semantic loss.
- Sensitivity: stubbing `diverge()` flips the verdict to `false` (neg, exit 1) — the
  equivalence results are not vacuous.
- A4 closure holds: root-keyed kills diverge under `(1,0),(1,1)` only and die at
  `runtime`; no accept false-kill under the real root.
- A5 closure holds on the synthetic set: manifest-bound freeze (`d16f9b5a`), strict
  ancestry, lineage `--diff-filter=A`, committed-bytes scoring all green; the
  tool-absent rev shows `sealed_after_freeze=1` survives independently of scoring.
- `--before`/`--tool` control plumbing, `ho_distinct`/`pub_distinct`/`pub_slots`
  receipt fields, and `SEALED-*` diagnostics are unreachable in deciding mode by design
  — kept: they are the audit/control surface the kill rule relies on (receipts re-runnable).

## Commands / evidence inventory

- Counter attacked: `git show HEAD:.ufo/evidence/round-35/c1/c1-measure.py` → sha256
  `d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2` (= `counter-base.py`).
- Runs: `runs/{base,neg,d01..d17,*t,*e}/stdout|stderr|exit` under the scratch dir;
  per-variant diffs `diffs-dNN.txt`; fixture revs `986b56e0`, `bfce22d0`, `69299e55`,
  `351e6452` on `lane-w` (all scratch-local).
- Frozen artifacts never edited; verified byte-identical reads: tool `ef98fc53…`,
  runner `a7d3f2dd…`, counter `d27e6769…`, contract A6 block as quoted.
- Lane repo untouched except this report; pre-existing untracked files
  (`w2/ExecReplayC2Before.md`, `w2/ScribeS102.md`, `corpus/lessons/round-35.md`) were
  present before this seat ran and are not mine.

## Tradeoff note

d17 shrinks the counter 464→447 lines with zero behavioral delta on every input class
I could construct, including the two adversarial fixture revs. Everything rejected is
rejected because it is *specimen-general* load-bearing (oracle fidelity for sealed
specimens the panel does not exercise) or receipt-semantic, not because the proof was
weak — those deletions are also byte-identical on this panel, which is exactly why
the report separates "cannot change the verdict on this panel" from "safe to delete."
