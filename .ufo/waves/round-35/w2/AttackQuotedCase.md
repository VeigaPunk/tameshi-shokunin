# Round-35 w2 — AttackQuotedCase

Seat: `tameshi-r35-w2-AttackQuotedCase` (leaf mutation tester, godspeed). Lane clone at
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (detached), **read-only: no commit, no write inside the
checkout**. All scratch under `/fast/scratch/hyaku/tameshi-r35-seats/AttackQuotedCase/`. No tool
installs; `pacman` untouched.

Pins verified on my clone (sha256):
- `tools/tally-audit-v3.py` = `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` (contract pin)
- `tools/tally-audit-v2.py` = `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`
- `tools/mutate-and-run.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (byte-pinned)
- `.ufo/evidence/round-35/c1/c1-measure.py` = `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` (A5 logic; contract pin at 7da6e07)

Lane-state note (adapted, not a finding): while I worked the lane advanced to
`68f25573d075d04189158e7eac76408b0e0a981f`; commit `f9df589` (A6) re-pins the counter's
`TOOL_SHA256` from `da23d3a2` (freeze bytes) to `ef98fc53` and bumps the counter to
`d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2`; contract pins updated.
`git diff 7da6e076 68f2557 -- tools/tally-audit-v3.py` is empty and SHA-256 of the tool at both
revs is `ef98fc53…`, so every result below applies unchanged to the deciding revision. The
counter delta is only that constant (verified by diff); my ground truth used the A5 `behavior()`
logic from the clone. **The deciding run must be at a rev >= f9df589**, else the stale
`TOOL_SHA256` alone forces `tool_sha_ok=0`.

## 1. Method

- Each mutant is an exact edit on the pinned runner bytes. Every anchor asserted to apply exactly
  once (`one()` in `work/probe.py`); each mutant is a standalone file; the lane was never written.
- Behavioural ground truth = the frozen counter's own `behavior()` (`c1-measure.py:204-214`):
  four `(auto,KEEP)` triples (`CONFIGS`, real auto root), `vectors_for(9)` (267 vectors), full
  stdout; `diverge()` reports the diverging configs.
- Tool verdicts = the real CLI:
  `python3 <lane>/tools/tally-audit-v3.py --runner <copy>` and the same with `tally-audit-v2.py`;
  rc, `CHECK` lines and `TALLY_AUDIT` line captured in `work/out/*.txt`.
- Real-runner proof = `bash <copy> --regression` from `/tmp/r35-realrun` (the runner's own default
  auto root, `mutate-and-run.sh:1357-1365`); outputs in `/tmp/r35-realrun/*.real.out`.
- Runner-context inline harness (`work/ctx/`): the extracted tally block run inline inside a
  `run_regression()`-shaped function with `local root=… auto=1 KEEP=0`, statuses as locals, **no
  positional args**, `SELF` set or unset — i.e. the real runner's calling context vs the audit
  harness's calling context.

Vector-superset check used in §4: `CONFIGS` tuples of v3 and counter are equal; the counter's 267
vectors are a strict subset of the tool's 7,561 (programmatic assert: `counter missing from tool:
0`).

## 2. Locator attacks — verdicts

| # | mutant (`work/`) | edit | counter divergence | v3 | v2 | verdict |
|---|---|---|---|---|---|---|
| 1 | `mutants/case-quoted.sh` `2f4b7507…` | `case "$st" in` | none | **SETUP rc2** | SETUP rc2 | BOUND (fail-closed) |
| 2 | `mutants/case-braced.sh` `5adb13e4…` | `case ${st} in` | none | **SETUP rc2** | SETUP rc2 | BOUND (fail-closed) |
| 3 | `mutants/case-nl-in.sh` `7f1b975f…` | `case $st`⏎`in` | none | **SETUP rc2** | SETUP rc2 | BOUND (fail-closed) |
| 4 | `mutants/case-doubled-brace.sh` `c97e8168…` | `case ${{st}} in` | all 4 configs | **SETUP rc2** | SETUP rc2 | BOUND (abstention on divergent) |
| 5 | `mutants/case-subshell.sh` `0f2ad16d…` | counting `case` wrapped in `( … )` | all 4 configs | **KILL rc1** (`runtime` only) | KILL rc1 (`runtime`) | correct kill |
| 6 | `mutants/case-subshell-decoy.sh` `5e9e2411…` | inert `( case $st in 3) : ;; esac )` before real case | none | ACCEPT rc0 | ACCEPT rc0 | correct accept |
| 7 | `mutants/case-subshell-steer.sh` `f4a3cff2…` | counting case in subshell before real case | none | ACCEPT rc0 | ACCEPT rc0 | correct accept |
| 8 | `loc/loop-renamed.sh` `a48dbb8c…` | `for leg …; case $leg in` | none | ACCEPT rc0 | ACCEPT rc0 | correct accept |
| 9 | `loc/loop-renamed-collide.sh` `c6519989…` | `for nlegs …; case $nlegs in` | all 4 configs | **KILL rc1** (`runtime` only) | KILL rc1 | correct kill |
| 10 | `limit/loop-while-identical.sh` `b56deb73…` | `for` → `while (( i < nlegs ))` + array | none | **crash rc1** (TypeError) | crash rc1 | BOUND + false docstring claim |

Exact-vs-expected summary of the CLI runs (all as above; raw stdout in `work/out/<mutant>.{v3,v2}.txt`
and `work/out/<mutant>.tally-audit-v{3,2}.txt`). `probe-results.json` carries the same rows.

### 2.1 Quoted / braced / newline-before-`in` subjects — SETUP, never accepted (BOUND)

All three are POSIX-identical at runtime (`bash` accepts `case "$st" in`; `case ${st} in`;
`case $st` newline `in` — verified live: `bash /tmp/case-nl.sh` → `three`, exit 0), and the
counter's `behavior()` reports **no divergence on any config** for any of them. The tool refuses:

```
$ python3 lane/tools/tally-audit-v3.py --runner work/mutants/case-quoted.sh ; echo rc=$?
TALLY_AUDIT: SETUP (counting `case $VAR in` not found)
rc=2
```
Same line for `case-braced` and `case-nl-in` (v3 and v2; `work/out/case-*.v3.txt`, `.v2.txt`).
Mechanism: `CASE_RE = re.compile(r'case[ \t]+\$([A-Za-z_][A-Za-z0-9_]*)[ \t]+in\b')`
(`tally-audit-v3.py:258`, byte-identical at v2:177) — the `"`, `{` and newline forms cannot match;
`counting_case()` (`:271`) raises `CannotAudit`, which escapes `audit()` (per-check exceptions are
not caught; `main` catches it at `:835`) and prints only the SETUP line (no `CHECK` lines).

This is a **false-refuse of a behaviourally identical copy** — fail-closed, so a BOUND, not a pass,
and not a C1 falsifier unless such a copy is put in the sealed *accept* set.

The literal `${{st}}` variant is different: bash reports `${{st}}: bad substitution` (exit 1;
verified) and the copy diverges on **all four** configs (`work/mutants/case-doubled-brace.sh`,
first diff at vector 0: pristine `(0, PASS…)`, mutant `(1, '')`). v3 still SETUP-refuses (rc 2) —
**an abstention on a divergent copy, which is a BOUND by the assignment's rule, not a kill.**

### 2.2 `case` inside a subshell — KILL when it matters (correct)

Wrapping the counting case in `( … )` loses the counter updates; the copy diverges on all four
configs. The locator is not fooled (`counting_case` finds it inside the parens, `tally_loop` finds
the enclosing `for`, static PASSes) and the runtime oracle kills it:

```
CHECK runtime FAIL vectors=30316 mismatched=30316; first: cfg(1,0) statuses 0 0 0 0 0 0 0 0 0:
  got 2 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=0) …', want 0 'REGRESSION: PASS …'
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)   rc=1
```
(v2: same, `vectors=15158 mismatched=15158`, rc=1.)

Two controls show the subshell construct itself is not the trigger:
- inert subshell case before the real one (`case-subshell-decoy`): identical behaviour, v3 ACCEPT rc0;
- a *counting* case in a subshell **before** the real counting case (`case-subshell-steer`): the
  locator is steered to the subshell case (`counting_case` returns it; static still passes because
  the enclosing loop's operands are the leg list), behaviour is identical, v3 ACCEPT rc0. The
  acceptance is safe because the runtime oracle executes the whole block — locator steers cannot
  hide a divergence, they only change which loop is stressed.

### 2.3 Renamed loop variable — ACCEPT; renaming onto `nlegs` — KILL (correct)

`for leg in "$st_js" …; do case $leg in …` is identical (counter div none) and v3 ACCEPTs rc0,
v2 ACCEPTs rc0. Renaming onto an existing variable that participates in the output
(`for nlegs …; case $nlegs in`) is divergent on all four configs (`cases=0 counted=9`) and v3
KILLs rc1 under `runtime` alone (v2 too) — `tally_loop` matches loop var == case var (`:297`),
static passes, the runtime oracle catches the clobber.

### 2.4 A `while` refactor crashes the tool — BOUND, and the docstring claim is false

`for` replaced by `while (( i < nlegs )); do st=${sts[i]}; case $st in …` is behaviourally
identical (counter div none; the real runner prints the same `REGRESSION: SETUP (cases=9 passed=0
cannot-verify=9)`, exit 2). The tool does not refuse cleanly — it crashes:

```
Traceback (most recent call last):
  … tally-audit-v3.py:695 audit → check_static(body, block)
  … tally-audit-v3.py:479 check_static: if sorted(ops) != sorted(names):
TypeError: 'NoneType' object is not iterable           rc=1
```
v2 crashes identically at `tally-audit-v2.py:352`. `tally_loop` returns `ops=None` for the
while-kind (`tally-audit-v3.py:321`) and `check_static` never implements the documented fallback:
the docstring explicitly promises "`while`/`until` traversals are accepted" (`:289`, verbatim the
same sentence at v2:208). Two consequences: (a) a fail-closed BOUND (a behaviourally identical copy
is refused, with a traceback instead of a `TALLY_AUDIT` line); (b) if a sealed **accept** specimen
uses a while-loop, the contract's falsifier "an accept specimen the v3 tool kills or refuses
(rc != 0)" (`contract.json:37`) fires. It is pre-existing in v2 (not a v3 regression).

## 3. Limit proof — CRITICAL: context-gated arms are accepted (fail-open)

The audit's runtime witness executes the block as a freshly built script (`run_vectors`, `:376-399`):

```
set -u -o pipefail
tally() {
  local st_js=${1} … local st_citecheck=${9}
  local root=<cfg root> auto=<a> KEEP=<k>
  <block>
}
out=$(tally <9 statuses> …)
```
The real runner executes the same block **inline** in `run_regression`, called with no arguments
(`mutate-and-run.sh:2078`: `regression) run_regression ;;`), inside the runner process: `SELF` is
set (`mutate-and-run.sh:178`), `$#` is 0, and the runner's whole function table and environment are
present. Anything the tally block reads from that context is invisible to the witness — and to the
frozen counter, which uses the same driver convention.

Three cheapest copies, each a one-line insertion after the tally loop, each **accepted by both
tools** (rc 0, all checks pass) while changing the real runner's output:

| mutant | inserted gate | real-runner REGRESSION line | v3 | v2 | counter `behavior()` |
|---|---|---|---|---|---|
| `work/limit/limit-argc-gate.sh` `0b5762fb…` | `if [[ $# -ne 9 ]]; then nfail=0; npass=$((npass+1)); fi` | `SETUP (cases=9 passed=1 cannot-verify=9)` vs pristine `passed=0` | PASS rc0 | PASS rc0 | div = none |
| `work/limit/limit-self-gate.sh` `e99f4a01…` | `if [[ -n ${SELF:-} ]]; then nfail=0; npass=$((npass+1)); fi` | `passed=1` vs `passed=0` | PASS rc0 | PASS rc0 | div = none |
| `work/limit/limit-func-gate.sh` `88497ea7…` | `if declare -F regression_case_git >/dev/null 2>&1; then nfail=0; npass=$((npass+1)); fi` | `passed=1` vs `passed=0` | PASS rc0 | PASS rc0 | div = none |

Exact evidence for the canonical one (`limit-argc-gate`):

```
$ bash work/pristine.sh --regression | grep '^REGRESSION: '        # exits 2
REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)
$ bash work/limit/limit-argc-gate.sh --regression | grep '^REGRESSION: '   # exits 2
REGRESSION: SETUP (cases=9 passed=1 cannot-verify=9)
$ python3 lane/tools/tally-audit-v3.py --runner work/limit/limit-argc-gate.sh ; echo rc=$?
CHECK head PASS … CHECK static PASS … CHECK runtime PASS vectors=30316 mismatched=0 … CHECK harness PASS
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
rc=0
```
(Verdict-level proof in the runner-shaped context, vector `[1,0,0,0,0,0,0,0,0]`, `SELF` set, `$#=0`,
statuses as locals — `work/ctx/realctx-SELF-{pristine,mutant}.sh`):
```
pristine: REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) … RC=1
mutant  : REGRESSION: PASS (cases=9 passed=9; ledger legs exact: …) … (removed on PASS…) RC=0
```
The same two scripts with `SELF` unset (the audit's context) are identical: both FAIL, RC=1.

**Ranking: CRITICAL (false-accept, non-fail-closed).** This is the exact class wave-1 seat
RevengerRootShape rated CRITICAL and amendment A4 answered: a tally arm whose divergence is keyed
on a real-runner context value that the witness fabricates. A4 pinned one such value (the auto
root); the general class — `$#`, `SELF`, function-table membership, and any other environment
element the harness does not reproduce — remains open. The witness does not even reproduce the
runner's calling convention. Its only defence is that the frozen counter shares the omission (as it
did for the root value), so the measurement will *also* label these copies accept.

**Operational consequence for the sealed set (important):** do **not** submit a context-gated copy
as a sealed **kill** — the counter's `behavior()` sees no divergence, so it is scored INVALID and
`ho_invalid > 0` fails C1. The finding is that C1's guarantee ("kills every kill specimen,
divergent under at least one of the four configs") is only as strong as the witness's context; by
the RevengerRootShape precedent these are kill specimens and they are silently accepted.

## 4. What I could NOT break (with proof)

**No counter-defined kill specimen can be accepted by v3 within the harness convention.** The
counter's behavioural vectors for n=9 (267, `vectors_for`) are a strict subset of the tool's runtime
vectors (7,561: `256 + 8·256 + 55 count-pairs + mixes + 12×12 pairs`), `CONFIGS` are identical, and
the driver convention is identical (same prelude, statuses as positional args). Asserted
programmatically: `counter vectors: 267 tool vectors: 7561 counter missing from tool: 0`. `static`
(`:471`, pinning comparison at `:479`) forces the identified operand multiset == the head's leg names and `nlegs` == the
count, so the analytic oracle is pristine's semantics; v3 PASS on the pinned pristine confirms
pristine ≡ oracle on the superset. Therefore an accepted copy equals the oracle on every counter
vector under every config, hence cannot diverge from pristine under the counter's ground truth.
A false accept must come from (a) omitted context (§3), or (b) vectors outside both sets
(e.g. three simultaneous status-3 legs — a real divergence the counter's `vectors_for` also never
reaches, so it is not a counter-defined kill specimen either).

Also not breakable:
- Quoted/braced/newline case subjects are **never accepted**; they fail closed (§2.1).
- A subshell that actually changes semantics is killed by `runtime` even though the locator locates
  it correctly (§2.2); locator steering by an inert counting case is harmless (§2.2 controls).
- Renamed loop variables are accepted only while behaviour is identical; the collision form is
  killed (§2.3).

## 5. v2 vs v3 — no regression found

- The locators are byte-identical: `LOOP_RE` v2:174 = v3:255, `WLOOP_RE` v2:175 = v3:256,
  `CASE_RE` v2:177 = v3:258 (same regex text, verified by grep). Consequently **every one of the
  ten mutants gets the same rc/verdict from v2 and v3** (table §2).
- There is **no class v2 caught that v3 now accepts**. The only classes v2 "catches" that v3 does
  not are the three inert-comment copies on the public panel: v2's control receipt
  (`.ufo/evidence/round-35/control/c1-v2-control.stdout`) shows v2 killing/refusing
  `comment-brace` (rc1 runtime), `comment-esac` (rc2), `comment-names-leg` (rc1 head), while the
  same receipt's `div=-` column (and my `behavior()` runs) show them behaviourally identical. Those
  were false kills; v3's acceptance is the intended round-34/35 de-blinding, not a regression.
- v3 is strictly stronger elsewhere: four configs vs two, full stdout vs first line, comment-blind
  `code_view` (`:150`), real auto root (`:354`). v2's control result on the A4 panel is 0/5
  kill and 0/3 accept (receipt above), so v2 is strictly weaker on the object under test.
- One shared defect: the while-loop crash exists in both (§2.4).

## 6. Restoration / integrity evidence

- Lane checkout untouched and still at the dispatch pin:
  `git -C lane status --porcelain` → empty (exit 0); `git -C lane rev-parse HEAD` →
  `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.
- `work/pristine.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
  == `PIN_RUNNER` == `lane/tools/mutate-and-run.sh` at the pin; no source bytes were modified; all
  mutants are separate files under `work/`.
- Full mutant hashes: `case-quoted 2f4b7507…`, `case-braced 5adb13e4…`, `case-nl-in 7f1b975f…`,
  `case-doubled-brace c97e8168…`, `case-subshell 0f2ad16d…`, `case-subshell-decoy 5e9e2411…`,
  `case-subshell-steer f4a3cff2…`, `loop-renamed a48dbb8c…`, `loop-renamed-collide c6519989…`,
  `limit-argc-gate 0b5762fb…`, `limit-self-gate e99f4a01…`, `limit-func-gate 88497ea7…`,
  `loop-while-identical b56deb73…` (full 64-hex in `sha256sum` output / `probe-results.json`).
- The only lane path written is this report.

## 7. Tooling

No installs or upgrades (nothing was needed); `pacman` untouched. Scratch: `probe.py`,
`work/{mutants,loc,limit,ctx,out,div,div2}`, real-runner logs `/tmp/r35-realrun/*.real.out`.
