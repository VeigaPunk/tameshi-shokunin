# DevAccept — wave 1 dev sweep against frozen tally-audit-v2 (BENIGN-edit family)

Seat: `tameshi-r33-w1-DevAccept-3` (leaf; no subagents). Date 2026-10-23.
Scratch: `/fast/scratch/hyaku/tameshi-r33-seats/DevAccept/` (lane clone detached at
`f6d8a891f1d966c5c3cdda385090da3a6e804675`).

## Verdict

**One false reject found (operability), plus two coverage notes. Every other benign variant in the
assigned family passes, and every variant the tool PASSes is tally-equivalent to the pristine runner
on a 2613-vector differential sweep (0 mismatches).**

- F1 **false reject**: a behavior-preserving rename of the head-local `auto` (declared at
  `pristine.sh:1357`, assigned at `:1361`, read by the tally block at `:1464`) together with the same
  rename in the copy's own harness wrapper string (`:2003`) is rejected with `TALLY_AUDIT: FAIL`
  (exit 1, `runtime=fail harness=fail`), although the copy's `--regression` tally and its own tally
  harness are both behaviorally identical to pristine.
- F2 **reject that is correct in effect but for an incidental mechanism**: the one-edit version of the
  same rename is rejected by `runtime` (10/2395 vector mismatches) while the tool's `harness` check
  *passes* it; the copy is in fact degraded (its own harness 8/9) — but the tool never sees that.
- Coverage note: accepted copies v07 (split `for` line), v12 (auxiliary wrapper loop) and v34
  (my own non-equivalent second extraction) each have a degraded own-selftest (1/9, 1/9, 8/9 failing
  cases) while the audit says PASS. v07/v12 are in-family variants the contract requires the tool to
  accept (round-32 held-out class 3); the degradation is a property of the runner's own fragile
  harness `sed`, and the tool's harness check deliberately injects `REF_BLOCK` and cannot see it.

No survivor in the tally dimension: 33 PASS variants × 2613 status vectors each = 0 differences
against pristine (v35 was not put through the differential; see F1).

## Frozen bytes under test

```
$ git -C lane show f6d8a89...:tools/mutate-and-run.sh > pristine.sh
$ git -C lane show f6d8a89...:tools/tally-audit-v2.py  > tool.py
$ sha256sum tool.py pristine.sh
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```
`pristine.sh` matches the contract's `a7d3f2dd…2eb9`. Baseline audit of the untouched runner:

```
$ timeout 300 python3 tool.py --runner base/pristine.sh; echo $? > base/pristine.rc
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```
(`base/pristine.rc` = 0; wall time 1.8 s.)

## Method

Every variant is generated from the pristine bytes by exact string replacement; the generator
(`gen_variants.py`) asserts the old string's occurrence count and refuses no-ops. Variants are
written as copies in `mutants/vNN.sh`; the pristine runner is never edited. Each copy was audited
with the frozen tool and, independently, (a) differentially against pristine's extracted tally block
(2613 vectors: every status 0..255 at every leg position, every (failing,setup) count pair 0..9 in
two placements, plus 200 seeded random mixes; exit code + first stdout line compared) and (b) run
through its **own** tally selftest harness (no injection) to see whether the copy itself still
behaves like the runner.

```
$ for f in mutants/*.sh; do id=$(basename "$f" .sh); \
    timeout 300 python3 tool.py --runner "$f" > "out/$id.stdout" 2> "out/$id.stderr"; \
    echo $? > "out/$id.rc"; done
```

## Sweep log

`tool` = audit exit code / final line; `diff` = mismatching vectors out of 2613; `own-h` = the
copy's own tally harness (`HARNESS cases=9 failed=N`).

| id | edit (benign class) | tool | diff | own-h |
|----|---------------------|------|------|-------|
| v01 | comment added in head before tally block | 0 PASS | 0 | 9/0 |
| v02 | comment added before `run_regression()` | 0 PASS | 0 | 9/0 |
| v03 | comment inside the tally block | 0 PASS | 0 | 9/0 |
| v04 | blank line between two case arms | 0 PASS | 0 | 9/0 |
| v05 | trailing whitespace on `esac` line | 0 PASS | 0 | 9/0 |
| v06 | re-indent the whole tally loop | 0 PASS | 0 | 9/0 |
| v07 | operands split with `\`-newline continuation | 0 PASS | 0 | **9/1** |
| v08 | rename local `auto` → `auto_remove` only | **1 FAIL** | 10 | **9/1** |
| v09 | reorder `local auto=0 specs root` | 0 PASS | 0 | 9/0 |
| v10 | unused `local unused_probe=0` in head | 0 PASS | 0 | 9/0 |
| v11 | second, identical `tblock=$(awk …)` extraction (round-32 a3) | 0 PASS | 0 | 9/0 |
| v12 | wrapper `for tally_once in "$st_js"; do` around tally loop (round-32 Loop-3) | 0 PASS | 0 | **9/1** |
| v13 | pre-count loop over leg statuses (round-32 a4) | 0 PASS | 0 | 9/0 |
| v14 | reversed operand order | 0 PASS | 0 | 9/0 |
| v15 | `;;` spacing (`…+ 1));;`) | 0 PASS | 0 | 9/0 |
| v16 | no-op `:` before the counting `case` | 0 PASS | 0 | 9/0 |
| v17 | comment after the tally loop | 0 PASS | 0 | 9/0 |
| v18 | unused function `probe_dead_helper()` | 0 PASS | 0 | 9/0 |
| v19 | comment inside the selftest harness | 0 PASS | 0 | 9/0 |
| v20 | trailing whitespace on `local -a tnames` | 0 PASS | 0 | 9/0 |
| v21 | extra blank line at end of file | 0 PASS | 0 | 9/0 |
| v22 | harness preamble comment wording | 0 PASS | 0 | 9/0 |
| v23 | blank line between independent head statements | 0 PASS | 0 | 9/0 |
| v24 | reorder harness declarations | 0 PASS | 0 | 9/0 |
| v25 | rename harness local `tgot` → `tally_hits` | 0 PASS | 0 | 9/0 |
| v26 | rename local `h` → `digest` in `sha_of()` | 0 PASS | 0 | 9/0 |
| v27 | reorder independent functions `usage_exit()` / `die_setup()` | 0 PASS | 0 | 9/0 |
| v28 | comment before the default case arm | 0 PASS | 0 | 9/0 |
| v29 | blank line inside the harness | 0 PASS | 0 | 9/0 |
| v30 | whitespace compression in the completeness guard | 0 PASS | 0 | 9/0 |
| v31 | trailing whitespace on an independent head line | 0 PASS | 0 | 9/0 |
| v32 | comment before the `REGRESSION_TOOL` banner printf | 0 PASS | 0 | 9/0 |
| v33 | rename head-only local `specs` → `specs_dir` (not read by the block) | 0 PASS | 0 | 9/0 |
| v34 | second extraction with a different awk expression (probe, not benign) | 0 PASS | 0 | **9/8** |
| v35 | rename `auto` consistently **and** its own harness wrapper string | **1 FAIL** | n/a | 9/0 |

Family coverage: comments (v01–v03, v17, v19, v22, v28, v32), whitespace-only (v04–v07, v15, v20,
v21, v23, v29–v31), renamed locals outside the tally path (v25, v26, v33), reordered independent
functions (v27), unused variable (v10) and unused function (v18), second extraction line (v11),
wrapper loop (v12), pre-count loop (v13). 33 variants; ≥ 20 required.

## F1 — false reject: consistent rename of the head-local `auto`

Edit (v35, two exact replacements; the second is needed because the copy's own harness wrapper is
the only other place the name appears):

```
pristine.sh:1357  -  local root specs auto=0          +  local root specs auto_remove=0
pristine.sh:1361  -    auto=1                         +    auto_remove=1
pristine.sh:1464  -  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
                  +  if [[ $auto_remove -eq 1 && $KEEP -eq 0 ]]; then
pristine.sh:2003  -  '  local root=selftest-tally auto=0 KEEP=1' "$tblock" …
                  +  '  local root=selftest-tally auto_remove=0 KEEP=1' "$tblock" …
```

Only four lines mention `auto` (`grep -n '\bauto\b' pristine.sh` → 1357, 1361, 1464, 2003 in
run_regression plus the harness wrapper); no callee reads it, so the rename is behavior-preserving.
Its own selftest confirms it: `HARNESS cases=9 failed=0`.

Audit output (exit 1):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime FAIL vectors=2395 mismatched=10; first: statuses 0 0 0 0 0 0 0 0 0:
      got (1, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)'),
      want (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
CHECK harness FAIL harness rejects or cannot run the reference block ((9, 1))
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=fail)
```

The 10 runtime mismatches are exactly the ten all-zero vectors (the duplicated all-pass vector from
the position loops plus `count_vectors(9)[0]`). Mechanism: `run_vectors` synthesises the enclosing
scope as `local root=tally-audit auto=0 KEEP=1` (`tool.py:225`) and runs under `set -u`; the renamed
block reads `$auto_remove`, which is unbound, so the block aborts with exit 1 *after* printing the
correct first line. `run_harness` (`tool.py:423`, env at `tool.py:432`) injects `REF_BLOCK` into the
copy's harness, and `REF_BLOCK` reads `$auto`; v35's wrapper string no longer defines it, so the
reference block cannot run and the harness check fails `(9, 1)`.

Smallest safe correction (tool is frozen; proposed, not applied):

1. `tool.py:225` — build the synthetic preamble from the audited head instead of a fixed name list:
   collect `^\s*local\s+([A-Za-z_][A-Za-z0-9_]*)` names from `head_section`, drop the leg names and
   `root`/`auto`/`KEEP`, and append `NAME=0` for the rest. For pristine this adds only `specs=0`
   (inert); for v35 it adds `auto_remove=0`.
2. `tool.py:432` — prepend `  auto=0 KEEP=1\n` to the injected block text (`AUDIT_INJECT`) so the
   reference panel does not depend on the copy's wrapper variable names.

Neither change weakens a check: faults are still judged by printed verdict lines and exit codes; the
seed only supplies free variables the real enclosing function declares.

## F2 — correct reject, incidental mechanism

v08 (the single-edit form of the same rename: the harness wrapper at `:2003` still says `auto=0`)
returns `TALLY_AUDIT: FAIL` with `CHECK runtime FAIL … mismatched=10` and
`CHECK harness PASS reference cases=9; faults rejected=29/29`. The copy is genuinely degraded — its
own harness fails the all-pass case (`HARNESS_FAIL tally harness: all nine legs pass -> PASS
passed=9, exit 0`; 9 cases, 1 failed) because the block it extracts reads `$auto_remove` while its
wrapper declares `auto`. So exit 1 is defensible for this copy, but the tool did not detect the
actual breakage: the `harness` check passed it because it replaces the extracted block with
`REF_BLOCK`. With the F1 correction applied, v08 would become `TALLY_AUDIT: PASS` even though its
own `--selftest` fails; that blind spot already exists for v07/v12/v34 today and is a property of the
injection design, not of the correction.

## Coverage notes (accepted copies whose own selftest degrades)

Each of these was audited PASS and is tally-equivalent to pristine, but its own tally harness reports
a failing case:

- v07 (operands split across a `\` continuation): own harness 8/9. The harness's own fault case
  `sed -E '0,/^  for st in /s/ "\$st_[a-z]+"; do$/; do/'` no longer matches the first physical
  `for` line, so the operand-removal fault is not applied and the case fails. The copy's
  `--regression` tally is identical (differential 0/2613).
- v12 (wrapper loop, round-32 HeldOutLoop-3): own harness 8/9. The same `sed` substitutes on **every**
  line in its range, so it strips `"$st_js"` from the wrapper line as well as the last tally operand;
  the wrapper then iterates zero times and the case prints `case-tally mismatch: cases=9 counted=0`.
  The tool must accept this copy (contract class 3), and does.
- v34 (my probe: second extraction `awk '/^  local nlegs=9/{f=1} f{print} f&&/^}$/{exit}'`): own
  harness 1/9 because that expression prints the closing `}` line too (block 40 lines vs 39), so the
  copy's own generated tally script is malformed. Recorded so nobody reuses this expression as an
  "equivalent" second extraction; the in-family a3 case is covered by v11, which passes. The tool
  accepts v34 because it injects after the last extraction and never runs the copy's own extraction.

## Restoration evidence

The pristine runner was never mutated; every edit was applied to a copy. Hashes were recorded before
the sweep and re-verified after it:

```
$ sha256sum mutants/*.sh pristine.sh tool.py > hashes.final2.txt
$ sha256sum -c hashes.final2.txt > hashcheck.txt; echo $? > hashcheck.rc
$ cat hashcheck.rc
0
$ grep -c OK hashcheck.txt
37
```
37/37 OK (35 mutant copies + pristine + tool). `pristine.sh` remains
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`. Two audit sweeps over the same
bytes produced byte-identical per-variant stdout (`out.run1/` vs `out/`: no `DIFF` lines), so the
verdicts are deterministic. All runs were wrapped in `timeout`; no process started here remains
running, and no git write command was issued in the lane or the fleet repo.

Tooling installed/upgraded: none (system python3 only). Disk: `/fast` 34 G free at start; the seat
wrote ~1.5 MB (lane clone + 35 copies + logs).
