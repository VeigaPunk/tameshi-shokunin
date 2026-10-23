# ResidueHelperRefactor — round-34 w1 mutation seat

Claim under attack: C1 (operability, `tools/tally-audit-v2.py`) MEASURED TRUE at
`c17e593b51802dd4ed568da3265f21c6d00c4273`, deciding receipt
`.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (exit `0`). This seat attacks one routed
v3 residue class, measurement-only: **helper-function refactors** — move the tally loop into a
helper the static check might miss; measure the tool's verdict on a behaviorally-faulted variant.
The tool is byte-pinned and frozen; the deciding run stands; no contract change is proposed and no
tool edit was made.

## Verdict first

The class splits into two measurable outcomes, and the second one is a **live false PASS**:

1. **Literal extraction (tally loop moved into a top-level helper, loop gone from
   `run_regression`): REFUSED, not killed.** Both the behavior-preserving twin (`v1`,
   `ef263faa…5ddc3`) and the faulted twin (`v2`, `a8e8223b…00498`) return
   `TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found)`, **exit 2**, with no `CHECK` line at
   all. The tool does not discriminate benign from faulted; and under the counter's own scoring an
   exit-2 refusal is **not a kill** (`rc == 1 and last.startswith('TALLY_AUDIT: FAIL')`,
   `c1-measure.py:275`), so a helper-extraction kill copy would register as a tool miss.
2. **The class's natural live-fault form: SURVIVED.** A per-leg policy helper defined at top level
   and called from inside the tally loop (`v6-policyhelper-faulted`, `321d2aab…5ff`) flips the real
   runner's verdict for every failing leg (FAIL → SETUP, exit 1 → 2) yet the frozen tool prints
   `CHECK head PASS / static PASS / runtime PASS vectors=15158 mismatched=0 / harness PASS` and
   `TALLY_AUDIT: PASS`, **exit 0**. The dispatch variant (`v7`, `7b5015a7…1601`) is also **exit 0**
   and additionally passes the runner's own tally harness.
3. **Scope controls isolate the cause.** The same net fault written inline (`v6-inline-faulted`,
   `416a6a7a…7cd6`) is **KILLED**: `CHECK runtime FAIL vectors=15158 mismatched=1800`,
   `TALLY_AUDIT: FAIL`, exit 1. A helper the dataflow can see inside the loop (`v4`,
   `6ac0b507…9547`) is **KILLED**, same 1800. So the fault is detectable; the helper's *scope*
   (outside `run_regression`) is what hides it.
4. **The sealed-set witness gate has the same boundary.** Calling the amendment-6 gate
   (`ho_witness_ok`, `c1-measure.py:184-219`) on the same bytes: the faulted policy-helper copy is
   **refused as must-kill** (`False, 'vector'`) and **certified as must-accept**
   (`True, 'vector-equivalence'`); the behaviorally-equivalent benign refactor `v1` is
   **certified as must-kill** (`True, 'vector'`). The gate reverses the labels across the same scope
   boundary the tool cannot see.

Baseline on pristine bytes before, during (TMPDIR pinned) and after every probe: `TALLY_AUDIT:
PASS`, exit 0 all three times (see Detector table). A baseline failure would have made every
mutant verdict inconclusive; none occurred.

## Frozen bytes, verified before any run

Extracted from a detached clone at the dispatch tip; all writes confined to seat scratch.

| object | sha256 | source / check |
|---|---|---|
| `tool.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | `git show 0b99d48:tools/tally-audit-v2.py > tool.py`; equals the brief pin |
| `pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `git show 0b99d48:tools/mutate-and-run.sh > pristine.sh`; equals the brief pin |
| counter `c1-measure.py` (imported read-only, never executed in default mode) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | live lane; equals brief `f6b8868c…a07f28c` and identical at rev `6aaad5b3` |
| controls receipt (read only) | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` | live lane `.ufo/evidence/round-33/c1/controls-receipt.json` |
| deciding receipt `.exit` / `.stdout` | `9a271f2a…86aa` / `3e28149f…b05c` | `.ufo/evidence/round-34/measure/`; `.exit` reads `0` |

The two pinned blobs hash identically at the dispatch tip, the measurement rev and the live HEAD
(`work/fleet_hashes.txt`, `work/pins_by_rev.txt`):

```
$ for rev in 0b99d48… c17e593b… a5b19364…; do git -C $LIVE show $rev:tools/tally-audit-v2.py | sha256sum; done
7b11ba25…8d10  (×3)
$ for rev in 0b99d48… c17e593b… a5b19364…; do git -C $LIVE show $rev:tools/mutate-and-run.sh | sha256sum; done
a7d3f2dd…2eb9  (×3)
```

Live lane HEAD at probe time `a5b1936425d3533b2ce280b16208386dcb0dc4ee`; clone detached at
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (`git -C lane rev-parse HEAD` exit 0);
`git -C lane status --porcelain` empty (`work/lane_status.txt`, 0 lines).

## Mutant family

Built by `work/build_variants.py` and `work/build_more.py`; each edit must apply exactly once or
the builder refuses (exit 1). `v5-noop-control` is an identity edit whose output sha equals the pin,
proving the builder is byte-faithful (`a7d3f2dd…2eb9`). Every variant is valid bash
(`bash -n` exit 0 on all eleven files, `work/bashn.txt`).

| variant | sha256 | net behavior vs pristine |
|---|---|---|
| `v0-pristine` | `a7d3f2dd…2eb9` | — |
| `v1-helper-benign` | `ef263faa…5ddc3` | tally loop moved into top-level `tally_legs()`; **behaviorally identical** (0 divergent witness vectors) |
| `v2-helper-faulted` | `a8e8223b…00498` | same, helper arm `1) nfail` → `1) nsetup`: every failing leg becomes a setup |
| `v3-arghelper-faulted` | `2ff781d9…1604` | helper nested in the block using `case $1`, called from the loop; same fault |
| `v4-inloop-helper-faulted` | `6ac0b507…9547` | helper defined inside the loop body, `case $st` (dataflow-visible); same fault |
| `v6-policyhelper-benign` | `717be1b7…518c` | per-leg `tally_policy "$st"` call added in the loop; top-level helper is a no-op |
| `v6-policyhelper-faulted` | `321d2aab…5ff` | same, helper rewrites `nfail−1; nsetup+1` when `$1 == 1`; sum preserved |
| `v6-inline-faulted` | `416a6a7a…7cd6` | identical net fault written **inline** in the loop (scope control) |
| `v7-dispatch-faulted` | `7b5015a7…1601` | loop moved into helper **plus** an inline fallback loop under `if declare -F tally_legs`; helper faulted |

The two decisive diffs (`work/v2-helper-faulted.diff`, `work/v6-policyhelper-faulted.diff`,
`diff -u` exit 1 each):

```diff
--- pristine
+++ v2 (loop extracted; helper faulted at arm 1)
+tally_legs() {
+  local st
+  for st in "$@"; do
+    case $st in
+      0) npass=$((npass + 1)) ;;
+      1) nsetup=$((nsetup + 1)) ;;          # fault: fail counted as setup
+      *) nsetup=$((nsetup + 1)) ;;
+    esac
+  done
+}
 run_regression() {
@@ -1430,13 +1441,7 @@
   local nlegs=9 npass=0 nfail=0 nsetup=0 st
-  for st in "$st_js" … "$st_citecheck"; do
-    case $st in … esac
-  done
+  tally_legs "$st_js" … "$st_citecheck"
```

```diff
--- pristine
+++ v6-policyhelper-faulted (per-leg policy extracted to a top-level helper)
+tally_policy() { # per-leg tally policy: a leg that cannot verify at status 1 is a setup
+  if [[ "$1" == 1 ]]; then
+    nfail=$((nfail - 1))
+    nsetup=$((nsetup + 1))
+  fi
+}
@@ -1436,6 +1443,7 @@
       *) nsetup=$((nsetup + 1)) ;;
     esac
+    tally_policy "$st"
   done
```

The v6 fault is behaviour-preserving for the runner's own completeness guard — `nfail−1, nsetup+1`
keeps `npass+nfail+nsetup == nlegs` (`pristine.sh:1456-1462`), so the real runner prints
`REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)` where pristine prints
`REGRESSION: FAIL (…failed=1 setup=0)`.

## Detector: the frozen audit on every byte state

Same bounded detector each time: `TMPDIR=$PWD/tmp python3 tool.py --runner work/<variant>.sh`
(tool never edited; temp dirs confined inside the seat scratch). Re-run twice with identical
results (`work/<v>.stdout` and `work/<v>.audit2.out`).

| bytes | exit | verdict |
|---|---|---|
| `v0-pristine` (before probes) | **0** | `head PASS / static PASS / runtime PASS vectors=15158 mismatched=0 / harness PASS reference cases=9; faults rejected=34/34` → `TALLY_AUDIT: PASS` |
| `v1-helper-benign` | **2** | `TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found)` — no `CHECK` lines |
| `v2-helper-faulted` | **2** | same refusal, byte-identical stdout to `v1` |
| `v3-arghelper-faulted` | **2** | same refusal |
| `v4-inloop-helper-faulted` | **1** | `CHECK runtime FAIL vectors=15158 mismatched=1800; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0: got (2, '…cannot-verify=1'), want (1, '…failed=1 setup=0')` → `TALLY_AUDIT: FAIL` |
| `v6-policyhelper-benign` | **0** | full PASS (control: the tool passes the benign refactor, as it should) |
| `v6-policyhelper-faulted` | **0** | **full PASS on faulty bytes** — `head PASS / static PASS / runtime PASS vectors=15158 mismatched=0 / harness PASS faults rejected=34/34` |
| `v6-inline-faulted` | **1** | `CHECK runtime FAIL vectors=15158 mismatched=1800` (same first mismatch) → `TALLY_AUDIT: FAIL` |
| `v7-dispatch-faulted` | **0** | **full PASS on faulty bytes**, identical four-check output |
| `v0-pristine` (after all probes) | **0** | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `restored.sh` (`cp pristine → restored`, sha `a7d3f2dd…`) | **0** | `TALLY_AUDIT: PASS`, `runtime … mismatched=0` |

Head and static pass on v6/v7 by construction: the only thing that changed inside the audited
window is a *call*, and the operands/nlegs/head surface are untouched.

## Behavioural witness (helper present, independent of the tool)

`work/witness.py` sources each variant's own preamble (everything before `run_regression() {`, so a
top-level helper is defined exactly as in the runner) and drives the extracted block under the
tool's hermetic config (`root=tally-audit, auto=0, KEEP=1`), stderr discarded, first stdout line +
exit compared. Driver exit 0 on every variant.

| vector | pristine | v1 benign | v2 faulted | v6 benign | v6 faulted | v7 dispatch |
|---|---|---|---|---|---|---|
| `0 0 0 0 0 0 0 0 0` | rc 0 PASS | = | = | = | = | = |
| `1 0 0 0 0 0 0 0 0` | rc 1 FAIL failed=1 | = | **rc 2 SETUP cannot-verify=1** | = | **rc 2 SETUP cannot-verify=1** | **rc 2 SETUP cannot-verify=1** |
| `2 0 0 0 0 0 0 0 0` | rc 2 SETUP cannot-verify=1 | = | = | = | = | = |
| `1 1 0 0 0 0 0 0 0` | rc 1 FAIL failed=2 | = | **rc 2 SETUP cannot-verify=2** | = | **rc 2 SETUP cannot-verify=2** | **rc 2 SETUP cannot-verify=2** |
| `0 1 2 0 0 0 0 0 0` | rc 1 FAIL failed=1 setup=1 | = | **rc 2 SETUP cannot-verify=2** | = | **rc 2 SETUP cannot-verify=2** | **rc 2 SETUP cannot-verify=2** |

Divergence counts vs pristine (`work/witness.stdout`): `v1 0`, `v6-benign 0`, `v2 3`, `v6-faulted
3`, `v7 3`. The faults are real in the runner's own execution scope; the tool never sees them.

## Where the PASS comes from

The audit's entire window is `run_regression`'s body: `regression_body` (`tool.py:117-134`),
`tally_block` = `local nlegs=` → the brace before the function's closing `}` (`tool.py:149-156`),
`head_section` = body before `local nlegs=` (`tool.py:159-166`). A top-level helper is outside both,
so:

- **When the loop moved with it**, `counting_case` (`tool.py:190-201`) finds no `case` in the block
  and `tally_loop` (`tool.py:202-241`) raises `CannotAudit`; `audit()` builds its result list
  eagerly (`tool.py:555-569`) so the exception reaches `main` (`tool.py:690`) and the tool prints
  only `TALLY_AUDIT: SETUP (…)`, exit 2, with no `CHECK` line. That is the v1/v2/v3 path. `CASE_RE`
  (`tool.py:177`) also cannot match a positional subject (`case $1 in`), so v3 is refused twice
  over.
- **When only a call was added**, the block still contains the identified loop, so static and head
  pass; `run_vectors` (`tool.py:268-288`) wraps **only the block** in `tally() { … }` and runs it in
  a fresh bash with `PATH/LC_ALL/HOME/TMPDIR` — the helper is undefined there. The call fails to
  stderr, which is deliberately written to a side file and never compared (`tool.py:271,281`;
  stdout-only is the round-32 review decision). Counters therefore come only from the inline loop,
  which is correct, so every one of the 15158 vector/stress results matches the oracle. Direct
  mechanism evidence — `work/block_only.py` reproduces the `run_vectors` shape exactly (block only,
  stderr kept), exit **0**, vector `1 0 0 0 0 0 0 0 0`:

```
$ python3 work/block_only.py v0-pristine v6-policyhelper-faulted v6-policyhelper-benign v7-dispatch-faulted
v0-pristine:             stdout='RC 1 REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)' stderr_lines=0
v6-policyhelper-faulted: stdout='RC 1 REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)' stderr_lines=9
                         first_stderr='…/b.sh: line 12: tally_policy: command not found'
v6-policyhelper-benign:  same stdout, stderr_lines=9, same first_stderr line
v7-dispatch-faulted:     same stdout, stderr_lines=0 (the declare -F guard takes the inline branch)
```

The stdout the oracle compares is byte-identical to pristine; the helper call exists only as nine
discarded stderr lines (one per leg).

The same blind spot exists in the counter's witness runner: `block_run` wraps only the block and
discards stderr with `2>/dev/null` (`c1-measure.py:154-181`, line 168).

## Scope boundary (controls that kill)

| control | why it isolates scope | tool verdict |
|---|---|---|
| `v6-inline-faulted` | same net fault, no helper | **KILLED**, exit 1, 1800 mismatches |
| `v4-inloop-helper-faulted` | helper present, but the case and loop variable are inside the block's loop, so `tally_loop` identifies it and the sandbox executes the fault | **KILLED**, exit 1, 1800 mismatches |
| `v6-policyhelper-benign` | proves the tool's exit 0 on v6 is not fault-specific, i.e. the tool cannot tell the twins apart | exit 0 |

So the residue is precisely: *behaviour delegated to a top-level helper*. Neither the static
identification nor the runtime sandbox pins it, and the fault can be sum-preserving so the runner's
own guard is satisfied.

## What other detectors do with the class (honest mitigation)

The runner's embedded tally harness (`pristine.sh:1992-2040`) extracts the block with awk
(`:1994`) and writes a *new* script containing only the block (`tally_line`, `:1998-2005`).
Faithful replay (single merged stream, exactly `out=$(bash … 2>&1)` at `:2004`):

| bytes | harness `tally_line` on vector `1 0 …` | first line |
|---|---|---|
| `v0-pristine` | PASS | `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)` |
| `v6-policyhelper-faulted` | **FAIL (mismatch)** | `…: tally_policy: command not found` |
| `v6-policyhelper-benign` | **FAIL (mismatch)** | same undefined-call line |
| `v7-dispatch-faulted` | **PASS** | the expected FAIL line (guard sends it to the inline loop) |

So the runner's harness refuses the whole refactor class by accident (missing helper in its
extracted snippet), faulted and benign alike — it is brittle, not discriminating — while v7 passes
both the tool and that harness. This is an observation about a different detector; the audited
tool's verdict is exit 0 regardless, and the tool never executes `runner --selftest`.

## Sealed-set gate interaction (amendment 6)

`ho_witness_ok` called read-only on scratch bytes (`work/gate.exit`, exit 0; `block_run` under real
bwrap):

| variant | kill+vector `[1,0,…]` | accept+vector `[1,0,…]` |
|---|---|---|
| `v2-helper-faulted` | `True (vector)` | `False (vector-equivalence)` |
| `v6-policyhelper-faulted` | **`False (vector)`** | **`True (vector-equivalence)`** |
| `v6-inline-faulted` | `True (vector)` | `False (vector-equivalence)` |
| `v1-helper-benign` | **`True (vector)`** | `False (vector-equivalence)` |

Consequences if round 35 authors this class into the sealed set:

- the faulted policy-helper copy is certifiable as **must-accept** (block-only runs tie with
  pristine, `mutated != pristine`), and the tool returns PASS → it would score as a correct accept;
- the behaviorally-equivalent benign refactor is certifiable as **must-kill** (`a != b` because the
  undefined call changes the block-only output), and the tool returns exit 2 → it would score as a
  tool miss;
- the loop-extraction kill copy (`v2`) is gate-valid but the tool refuses with exit 2 → also a
  scored miss (`c1-measure.py:275` requires exit 1).

The gate's `a != b` rule and the tool's sandbox share the same scope boundary, so the labels invert
instead of failing closed.

## Coverage note

`grep -l 'tally_legs\|tally_policy\|declare -F' .ufo/evidence/round-33/heldout/*.json` exit **1**:
no committed sealed copy uses a helper, so the class has no sealed representative. Round-34 Holds
already names it as unadopted pre-data (`corpus/lessons/round-34.md:56-58`).

## Restoration evidence

The mutation target is the seat's scratch copy; the pinned bytes were never overwritten (variants
are separate files). A dedicated restore was taken and audited after every probe:

```
$ cp work/v0-pristine.sh work/restored.sh       # exit 0
$ sha256sum work/restored.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  work/restored.sh
$ TMPDIR=$PWD/tmp python3 tool.py --runner work/restored.sh   # exit 0
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Before/after hashes (`work/build.stdout`, `work/final_hashes.txt`):
`work/v0-pristine.sh` `a7d3f2dd…2eb9` before and after; `tool.py` `7b11ba25…8d10` before and
after; fleet `tools/tally-audit-v2.py` and `tools/mutate-and-run.sh` still hash to the pins
(`work/fleet_hashes.txt`); lane clone HEAD `0b99d48…`, working tree clean.

## Command log (exits captured with `cmd; echo $? > file`, never `&&`)

| command | exit |
|---|---|
| `git clone -q --no-hardlinks <fleet> …/ResidueHelperRefactor/lane` | 0 (`setup.exit`) |
| `git -C lane checkout -q --detach 0b99d48…` | 0 (`setup.exit`) |
| `git -C lane show 0b99d48:tools/tally-audit-v2.py > tool.py` | 0 (`extract_tool.exit`) |
| `git -C lane show 0b99d48:tools/mutate-and-run.sh > pristine.sh` | 0 (`extract_runner.exit`) |
| `sha256sum tool.py pristine.sh` (matches both pins) | 0 (`pins.sha256`) |
| `python3 work/build_variants.py` / `work/build_more.py` | 0 / 0 (`build*.exit`) |
| `python3 tool.py --runner work/v0-pristine.sh` (×3: before, with TMPDIR, after) | 0, 0, 0 |
| `python3 tool.py --runner work/v1-helper-benign.sh` | 2 |
| `python3 tool.py --runner work/v2-helper-faulted.sh` | 2 |
| `python3 tool.py --runner work/v3-arghelper-faulted.sh` | 2 |
| `python3 tool.py --runner work/v4-inloop-helper-faulted.sh` | 1 |
| `python3 tool.py --runner work/v6-policyhelper-benign.sh` | 0 |
| `python3 tool.py --runner work/v6-policyhelper-faulted.sh` | 0 |
| `python3 tool.py --runner work/v6-inline-faulted.sh` | 1 |
| `python3 tool.py --runner work/v7-dispatch-faulted.sh` | 0 |
| `python3 work/witness.py <7 variants>` | 0 (`witness.exit`) |
| `python3 -` (`ho_witness_ok` on 4 variants × 2 sets) | 0 (`gate.exit`) |
| runner-harness replay (`awk` extract + `tally_line` shape, 4 variants) | 0 (`runnerharness2.exit`) |
| `bash -n` on 11 files | 0 each (`work/bashn.txt`) |
| `cp work/v0-pristine.sh work/restored.sh; sha256sum; tool.py --runner restored.sh` | 0, 0, 0 |

## Findings for round 35 (measurement-only; tool frozen, no edit proposed)

1. **The class is not closed.** A helper that stays in the runner but outside `run_regression`
   hides a sum-preserving behavioral fault from all four checks (`v6` : exit 0) and from the
   counter's witness runner (same block-only wrapper, stderr discarded). The literal
   loop-extraction shape is refused (exit 2) rather than killed, and exit 2 is not a kill under
   `score_tool`, so both directions of the class are weak.
2. **The sandbox boundary, not the fault, decides.** Inline or in-loop-visible copies of the same
   net fault are killed with 1800 mismatches; the only difference is where the code lives. Any
   future "audit a runner by extracting its block" design inherits this: code the extractor does
   not carry is code the oracle cannot test.
3. **Route the gate, not just the tool.** `ho_witness_ok` (`c1-measure.py:184-219`) certifies the
   faulted copy as must-accept and the benign twin as must-kill across the same boundary. A round-35
   author following the current rules would produce inverted labels; the pre-data authoring gate
   therefore cannot be relied on to discover this class.
4. **Suggested direction (Hold, not an edit):** have the audit assert that every command invoked in
   the audited block resolves inside the sandbox (e.g. `declare -F`/`command -v` for each bare
   callee, or run the assembled function *with the runner's own preamble*), and let the witness gate
   compare real-run behaviour rather than block-only behaviour. Both are contract changes and are
   out of scope for a seat whose tool pin is frozen.
5. **No sealed representative.** No round-33 heldout copy uses a helper (grep exit 1), so
   `ho_kill=8/8 ho_accept=6/6` in the deciding receipt does not measure this class — an observation
   about coverage, not a defect in the deciding run.

## Bounds compliance

- All work inside `/fast/scratch/hyaku/tameshi-r34-seats/ResidueHelperRefactor/` (clone, byte
  extractions, variants, drivers, audit `TMPDIR`); the lane is read-only. No writes to
  `MANIFEST.json`, `templates/`, `scripts/`, `.ufo/state/`, `.ufo/watchdog.log`, sibling repos, jj
  state or the Git index; the only fleet-root write is this report.
- No `git`/`jj` write commands (`clone`/`checkout` target only the seat scratch; `rev-parse`,
  `status`, `show` are reads). No `agent://all`. No model parameter.
- Kill rule not invoked: the counter was never executed in default mode. It was imported read-only
  in scratch to call `ho_witness_ok`/`block_run` on scratch copies, as permitted.
- No tool installs or upgrades this seat.

## Pointers

- Residue class as routed: `corpus/lessons/round-34.md:56-58`.
- Deciding receipt: `.ufo/evidence/round-34/measure/c1-deciding-run.stdout:1`, `.exit` (`0`),
  sha `3e28149f…b05c` / `9a271f2a…86aa`.
- Tool window: `tools/tally-audit-v2.py:117-166` (body/head/block), `:177` (`CASE_RE`), `:190-241`
  (`counting_case`/`tally_loop`), `:268-288` (`run_vectors`, stderr side file), `:307-343`
  (`check_head`, twice-only rule), `:344-361` (`check_static`), `:372-437` (`check_runtime`),
  `:555-569` (`audit`), `:690` (`CannotAudit` → exit 2).
- Runner tally and scope: `tools/mutate-and-run.sh:1345` (`run_regression`), `:1432-1439` (tally
  loop), `:1456-1462` (sum guard), `:1992-2005` (embedded harness extraction + `tally_line`),
  `:2006-2032` (harness vectors).
- Counter semantics: `c1-measure.py:154-181` (`block_run`, stderr to `/dev/null`),
  `:184-219` (`ho_witness_ok`, `a != b` at `:218`), `:234-262` (`run_tool_sandboxed` outcome map),
  `:265-283` (`score_tool`, kill requires exit 1 at `:275`), `:286-295` (`public_panel`).
- Seat artifacts (all with captured exits): `work/build_variants.py`, `work/build_more.py`,
  `work/witness.py`, `work/block_only.py`, `work/v*.stdout|audit2.out|exit`, `work/v*.diff`,
  `work/block_only.stdout|exit`, `work/gate.exit`, `work/runnerharness2.exit`, `work/bashn.txt`,
  `work/final_hashes.txt`, `work/fleet_hashes.txt`, `work/pins_by_rev.txt`, `work/lane_head.txt`,
  `work/lane_status.txt`.

Report: .ufo/waves/round-34/w1/ResidueHelperRefactor.md
