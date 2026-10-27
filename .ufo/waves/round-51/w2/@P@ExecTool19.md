# T51W2ExecTool19 — C3 registry row falsification: `tools/tally-audit-v2.py`

**Seat:** T51W2ExecTool19 (executor; axis operability; milestone C3 row falsification)
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Base:** `9962033fd7a75aa2f2847e979dd687a5d28505a1` · **Candidate audited:** `6d8c11e378aa90b12650808e1b79270742935f15`
**Row audited:** `SKILL.md:2160`, inside `#### Gate/probe registry — round 51` (`SKILL.md:2138`)

Read-only on the lane, fleet and sibling repos. I wrote only this report and the receipt
directory `.ufo/waves/round-51/w2/@P@ExecTool19/`. No source written, no row repaired. Nothing
installed; no tool/channel record is owed. Scratch
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool19/` deleted before yield.

Clone: `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin cand`;
`git -C cand rev-parse --show-toplevel` → the clone; `checkout --detach 6d8c11e3…` → HEAD
`6d8c11e378aa90b12650808e1b79270742935f15`. A second fresh `git clone --shared --no-checkout`
served the frozen counter's own `measure.py` logic at the same rev.

---

## 0. Verdict in one line

The row is **counter-conformant and operable at CAND** — its exact backticked self-test exits 0
from a clone at CAND with the claimed last line (22/22), the usage probe exits 2 and 2 is
declared, and the frozen counter's own unmodified `row_reason` / `run_row` return no reason
against it. The row is nevertheless **materially wrong in two cells**: its verdict map omits an
exit code the tool actually surfaces (**64**, and arbitrary codes, via `--then-regression`),
and its Pinned-values cell says `none` while the tool hard-pins the audited runner's leg-name
panel and block text — a legitimate runner edit turns the gate red. Neither failure breaks the
C3 predicate as frozen; both are falsification-grade row defects for the L1.

## 1. The row under audit, cell by cell

`SKILL.md:2160` (raw bytes in receipt `row-raw-SKILL.md-2160.txt`):

| # | cell | row text (abridged) |
|---|---|---|
| 1 | name | tally audit v2 (mutation runner tally) |
| 2 | kind | `gate` |
| 3 | entry | `python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh` (add `--then-regression --workdir DIR` …) |
| 4 | verdict map | 0 clean; 1 failed (audit FAIL or a selftest case failure); 2 could-not-evaluate (cannot audit, setup, usage); a timed-out then-regression reports 124 and folds to 2 |
| 5 | self-test | `python3 tools/tally-audit-v2.py --selftest` → TALLY_AUDIT_V2_SELFTEST: 22/22 pass, one seeded-fault case per check |
| 6 | pinned values | none — expected tallies are literals of the tool's independent oracle and its 22 selftest seeds; audited surface defaults to `tools/mutate-and-run.sh` |
| 7 | write scope | lane read-only; scratch under TMPDIR (tally-audit-v2.*, removed in finally); the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires; --then-regression writes only the runner's caller-named --workdir |
| 8 | owner | tameshi |

## 2. The two required runs (row's exact commands, clone at CAND, scratch TMPDIR, stdin /dev/null)

| run | command | exit | last stdout line | wall |
|---|---|---|---|---|
| self-test | `python3 tools/tally-audit-v2.py --selftest` | **0** | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | 150.75 s |
| usage probe | `python3 tools/tally-audit-v2.py --r51-no-such-flag` | **2** | (stdout empty; stderr `usage: tally-audit-v2.py …` / `error: unrecognized arguments: --r51-no-such-flag`) | 0.032 s |

Receipts: `selftest.stdout.txt` (22 `CASE … PASS` lines then the tally line), `selftest.stderr.txt`
(empty), `usage-stderr.txt`.

The self-test is **clone-local**: it reads the runner *beside the tool*
(`tools/tally-audit-v2.py:601-603`, `runner = os.path.join(HERE, 'mutate-and-run.sh')`), never a
sibling fleet repo. So this row does **not** inherit the known row16 (`tools/round21-measure.py`,
`SKILL.md:2157`) clone-context failure; it is one of the rows the C3 counter can decide.

## 3. Row fields checked against source

### 3.1 kind = `gate` — TRUE

PROTOCOL §Gate standard: "A tool that cannot fail is a probe." This tool fails. Seeded-fault
probe (weakened the runner's majority guard, `if [[ $nfail -gt 0 ]]; then` →
`if [[ $nfail -gt 0 && $KEEP -eq 1 ]]; then`) and re-audited:

```
CHECK head PASS legs=10
CHECK static PASS legs=10 operands=10 nlegs=10
CHECK runtime FAIL vectors=18288 mismatched=1118; first: cfg(1,0) statuses 1 0 0 0 0 0 0 0 0 0: got (0, 'REGRESSION: PASS (cases=10 passed=9 …)'), want (1, 'REGRESSION: FAIL (cases=10 passed=9 failed=1 setup=0)')
CHECK harness PASS reference cases=9; faults rejected=36/36
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
```
exit **1** (receipt `probe-broken-runner-exit1.txt`). A gate, not a probe. ✓

### 3.2 entry command — TRUE, with one context caveat

`python3 tools/tally-audit-v2.py --runner tools/mutate-and-run.sh` → exit **0**,
`TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, 7.44 s
(`entry-audit.stdout.txt`). The `--then-regression --workdir DIR` add-on does what the row says
(`:591-596`: the `REGRESSION:` line must name `cases == nlegs`).

Caveat (context, not a row defect): the `--then-regression` path is **not runnable from a
clone**. The runner materialises each of its ten legs from the sibling fleet repos
(`tools/mutate-and-run.sh:1430`, `FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")`), so
from a clone all ten legs SETUP and the tool exits **2**:
`REGRESSION: SETUP (cases=10 passed=0 cannot-verify=10)` →
`TALLY_AUDIT_REGRESSION: SETUP (cases=10 legs=10 exit=2)`
(`probe-then-regression-from-clone-exit2.txt`). Exit 2 is declared, so the row stays truthful;
the C3 predicate only runs the self-test and the usage probe, so this is context, not counter input.

### 3.3 verdict map — **INCOMPLETE (main finding, F1)**

The cell declares `0`, `1`, `2` and explains `124 → 2`. It never declares **64**, which the
tool does exit.

`then_regression()` returns the runner's exit code **verbatim** at `tools/tally-audit-v2.py:596`
(`return p.returncode`) after only folding 124 (`:588-591`). Anything the runner's `--regression`
exits with is the tool's exit code. Measured, driving `then_regression()` directly with synthetic
runners (`probe-exit-code-passthrough.txt`):

```
>> runner exit 1  -> tool returned 1
>> runner exit 2  -> tool returned 2
>> runner exit 64 -> tool returned 64      <-- undeclared
>> runner exit 3  -> tool returned 3       <-- undeclared
>> SIGKILLed runner after its REGRESSION line -> tool returned -9   (negative -> shell 247)
```

End-to-end through `main()`, with a copy of the canonical runner carrying a **header** `EXIT`
trap (`trap 'exit 64' EXIT` inserted after the shebang; the tally block is byte-identical, so the
audit still passes and `main()` proceeds to `then_regression`):

```
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
TALLY_AUDIT_REGRESSION: SETUP (cases=10 legs=10 exit=64)
TOOL_EXIT=64
```
(`probe-then-regression-undeclared-exit64.txt`)

Two independent reasons this is a real row defect and not a curiosity:

1. **The lane's own sibling row declares exactly this code.** `SKILL.md:2162`
   (`tools/tally-audit.py`, same lane, same pattern) reads:
   `0 clean; 1 failed; 2 could-not-evaluate (cannot audit, usage, or regression SETUP); 64 could-not-evaluate (runner usage error surfaced through --then-regression)`.
   The v2 row's map is the same shape minus the 64 clause — an inconsistency inside one table.
2. **C3's own `cannot_see` names this as the wave-2 attack surface**: "that the verdict map names
   every code the tool can exit with beyond 0, 1 and the usage code (attacked per row by wave-2
   probes)".

Honest scope limit: with the **canonical** runner the reachable set is `{0,1,2}` — the runner's
`usage_exit` → 64 (`tools/mutate-and-run.sh:250`) is only reachable via `--target/--defects/
--suite/--label`, which `then_regression` never passes (`:1419`), and `die_setup` → 2 (`:255`).
So today the 64 path needs a runner that deviates — but the tool's whole job is to grade
runners, and PROTOCOL §Verdict ("every other code a gate exits … is declared in its registry
entry") plus the client's `--runner PATH` parameter make an undeclared passthrough a defect
whether or not the shipped runner reaches it. PROTOCOL's fallback ("an undeclared nonzero code
reads as could-not-evaluate") contains the damage; C3's counter does not test it.

Everything else about the map checks out:

* `0` clean — entry command exit 0. ✓
* `1` failed — audit FAIL verified (§3.1); a selftest case failure returns 1 (`:676`; measured
  `TALLY_AUDIT_V2_SELFTEST: 14/22 pass`, exit 1, on a shape-mismatched runner). ✓
* `2` could-not-evaluate (cannot audit / setup / usage) — `CannotAudit`, `OSError`,
  `UnicodeDecodeError`, `ValueError` mapped to 2 at `:689-693`; verified with a nonexistent runner
  (`TALLY_AUDIT: SETUP ([Errno 2] …)`, exit 2) and a runner with no `run_regression()`
  (`TALLY_AUDIT: SETUP (run_regression() not found)`, exit 2). argparse's usage error exits 2 and
  the map files "usage" under 2. ✓
* `124 → 2` — verified: `p.returncode == 124` caught at `:588-590`, prints
  `TALLY_AUDIT_REGRESSION: SETUP (--then-regression timed out after 2s)` and returns **2**
  (white-box probe with `THEN_REGRESSION_TIMEOUT=2` against a sleeping script).

Wording nit inside the same clause: "a timed-out then-regression **reports 124**" — the gate
never exits *or prints* 124; the inner `timeout` does, and the tool's own report is
`SETUP (--then-regression timed out after 1200s)`. Declared set right, phrasing loose.

### 3.4 self-test cell — count exact, composition misstated (F3)

`TALLY_AUDIT_V2_SELFTEST: 22/22 pass` — exactly true (22 `CASE` lines, all PASS, exit 0),
confirmed three independent runs.

The parenthetical **"one seeded-fault case per check"** does not describe the panel. Parsing the
case list at `tools/tally-audit-v2.py:630-655`, the 22 cases are:

* **1 pristine** baseline (`:631`, want exit 0);
* **17 seeded-fault cases** (want exit 1), distributed **runtime 7, harness 5, static 2,
  head 2** — plus **one fault case with no check label** (`'in-block 7-bit mask'`, `:637`,
  check `None`, asserted only by exit code);
* **4 equivalence cases** (want exit 0 — the tool must *not* reject them): `'aux wrapper loop'`,
  `'aux pre-count loop'`, `'second extraction line'`, `'reversed operands'` (`:651-654`).

So no check has *exactly* one seeded-fault case (head 2, static 2, runtime 7, harness 5), one
fault case is attributed to no check, and five of the 22 are not seeded-fault cases at all. The
claim survives only in the weak sense "every check has at least one" — which is true, and which is
what the tool's own header says (`:9`, "show every check able to fail on seeded faults").

### 3.5 pinned values = "none" — the cell's justification is misleading (F2)

The counter's rule (`.ufo/evidence/round-51/c3/measure.py:145-152`) accepts a cell that starts
with `none` and then skips path-existence checks, so the cell passes mechanically. The **prose**
fails:

> "expected tallies are literals of the tool's independent oracle and its 22 selftest seeds"

Two dependencies are not independent of the runner:

1. **The harness check's reference is a frozen copy of the runner's own block.**
   `REF_BLOCK` (`:67-105`) is byte-identical to the candidate runner's tally block — I extracted
   the runner's block with the tool's own `tally_block()` and diffed: **0 differing lines,
   1576 == 1576 characters**. `REF_NAMES` (`:107-108`) is a frozen copy of the runner's ten-leg
   panel, and `check_harness` (`:536-538`) **fails the whole audit** when the runner's leg names
   differ from it.

   Measured, with a runner carrying an 11th leg (`st_extra`: declared, assigned, looped,
   `nlegs=11`), entry command exits **1**:

   ```
   CHECK head PASS legs=11
   CHECK static PASS legs=11 operands=11 nlegs=11
   CHECK runtime PASS vectors=21708 mismatched=0
   CHECK harness FAIL leg names differ from the reference panel (st_js … st_driftpins st_extra)
   TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)
   ```
   (`probe-11leg-runner-exit1.txt`)

2. **The 22 selftest seeds are not frozen literals — they are string replacements computed
   against the runner's *live* bytes at run time.** `selftest()` reads the runner (`:601-604`) and
   builds each fault body with `text.replace(...)` against that text. If the runner's shape
   changes, a seed edit silently stops applying and the case reports
   `CASE … FAIL (edit did not apply)`. Measured with the 11-leg runner:
   `TALLY_AUDIT_V2_SELFTEST: 14/22 pass`, exit **1** (`probe-11leg-selftest-14of22.txt`).

So the truthful description is: the tool's expectations are literals **of a snapshot of the
runner**, and the gate turns red — in both the entry command and the self-test — the moment the
runner's leg panel changes, with no change to the tool. The lane already knows this coupling:
round-51 amendment 2 names `tools/tally-audit-v2.py (REF_NAMES :107, :614)` as one of the four
tools that pin the runner's leg panel. The *registry row* does not say so.

Correct sub-claim: "audited surface defaults to `tools/mutate-and-run.sh`" is true — argparse's
default is `os.path.join(HERE, 'mutate-and-run.sh')` (`:681`).

### 3.6 write scope — TRUE, and unusually candid (F5 disclosed risk)

* **lane read-only** — `git status --porcelain` in the clone is empty after every run (audit,
  self-test, usage probe, `--then-regression`). The tool opens the runner read-only (`:556-558`)
  and writes nothing under the lane.
* **scratch under TMPDIR, removed in finally** — `audit()` uses
  `tempfile.mkdtemp(prefix='tally-audit-v2.')` (`:562`) with `shutil.rmtree` in `finally`
  (`:571`); `selftest()` uses `prefix='tally-audit-v2-selftest.'` (`:656`) with rmtree in its
  `finally` (`:674`). Every `bash` subprocess gets `TMPDIR=tmp`, `HOME=tmp` (`:257`, `:520-521`),
  so nothing escapes TMPDIR. My TMPDIR was empty after each completed selftest. Nit: the
  selftest scratch prefix is `tally-audit-v2-selftest.*`, which does not literally match the
  cell's `tally-audit-v2.*` glob (hyphen, not dot) — cosmetic; both are TMPDIR-rooted and removed.
* **"the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a
  PASS vector fires"** — **verified exactly, and attributed.** `CONFIGS` (`:265`) is
  `(('tally-audit','0','1'), ('/tmp/tally-audit-work','1','0'))`; the injected block's
  `rm -rf "$root"` (`:101`) fires on the exit-0 (PASS) path when `auto=1 && KEEP=0`. Attribution
  experiment, `run_vectors()` once per `CONFIGS` entry with an all-pass vector:

  ```
  cfg 0 ('tally-audit', '0', '1')           -> /tmp/tally-audit-work exists after: n/a
  cfg 1 ('/tmp/tally-audit-work', '1', '0') -> /tmp/tally-audit-work exists after: False
  ```
  End-to-end: created `/tmp/tally-audit-work/MARKER`, ran the entry command (exit 0) → dir gone;
  same during `--selftest` (`probe-fixed-tmp-path.txt`).

  Disclosed hazard the cell states but does not flag: the tool deletes a **fixed global /tmp path
  it never creates** — the literal appears nowhere else in the lane's tools
  (`tools/mutate-and-run.sh` uses `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"`,
  `:1432`). Any unrelated process owning `/tmp/tally-audit-work` loses it on every run, and
  concurrent runs of this tool race on it. The C3 counter gives each row its own TMPDIR
  (`measure.py:170-176`) but this write escapes it. Cell 7 is the only place that says so — good
  disclosure, worth the L1 knowing.
* **"--then-regression writes only the runner's caller-named --workdir"** — TRUE: the tool passes
  `--workdir` straight through (`:584-585`) and the runner then owns it
  (`tools/mutate-and-run.sh:1434-1436`, `root=$WORKDIR`).

### 3.7 owner = `tameshi` — TRUE (lane convention; not checkable from the tool).

### 3.8 last-line marker is a real diagnostic — TRUE

`TALLY_AUDIT_V2_SELFTEST: 22/22 pass` is the tool's own finding id plus a count over per-case
verdicts (`:675`), not help text. Stable across three runs and two clones. The counter's
finding-id rule (first whitespace token of the last non-empty stdout line must appear in the
self-test cell) is satisfied: marker `TALLY_AUDIT_V2_SELFTEST:`, present in the cell.

## 4. The frozen counter's own logic against this row

Imported the **unmodified** `.ufo/evidence/round-51/c3/measure.py` and ran
`registry_rows` → `row_reason` → `run_row` on the candidate rev in a fresh
`git clone --shared --no-checkout` at CAND, `TMPDIR` inside scratch:

```
total rows parsed: 32
line 2160 why= None
candidates: [(2160, ['python3', 'tools/tally-audit-v2.py', '--selftest'],
                     ['python3', 'tools/tally-audit-v2.py', '--r51-no-such-flag'])]
run_row line 2160 why= None last= 'TALLY_AUDIT_V2_SELFTEST: 22/22 pass'
```
(`counter-row-logic.txt`; 254.58 s)

`row_reason` → `None` (kind `gate` ✓; entry names `tools/tally-audit-v2.py` ✓; verdict map holds
0 and 1 ✓; exactly one backticked self-test command with no shell metacharacters ✓; pinned cell
starts with `none` ✓; write scope non-empty ✓; owner `tameshi` ✓). `run_row` → `None`: self-test
exit 0, its finding id in the cell, usage exit 2 declared in the map. **This row is covered at
CAND** — consistent with the sibling full-counter receipt
(`@P@ExecTool02/c3-counter-full-run.txt`: `C3_TOOL tools/tally-audit-v2.py: covered line 2160
selftest exit=0 last=TALLY_AUDIT_V2_SELFTEST: 22/22 pass`).
`tools/tally-audit-v2.py` is in the frozen base-30 list (`.ufo/evidence/round-51/c3/tools-base.json`)
and its bytes contain `selftest`, so the counter grades it.

## 5. Findings, ranked

| # | severity | finding | evidence |
|---|---|---|---|
| **F1** | **medium — row is wrong** | **Verdict map omits exit code 64 (and arbitrary runner codes).** `then_regression()` returns the runner's code verbatim (`:596`), folding only 124. Demonstrated end-to-end: `TOOL_EXIT=64` with `TALLY_AUDIT_REGRESSION: SETUP (cases=10 legs=10 exit=64)`, and 3 / -9 in direct probes. The identical sibling row at `SKILL.md:2162` *does* declare `64 could-not-evaluate (runner usage error surfaced through --then-regression)`. C3's `cannot_see` names this exact attack. Counter does not test it; PROTOCOL's undeclared-code fallback contains it. | `probe-then-regression-undeclared-exit64.txt`, `probe-exit-code-passthrough.txt`, `tools/tally-audit-v2.py:588-596` |
| **F2** | **medium — row is wrong** | **Pinned-values cell says `none`; the tool hard-pins the runner's shape.** `REF_BLOCK` (`:67`) is byte-identical to the candidate runner's tally block (0-line diff, 1576 B), `REF_NAMES` (`:107`) pins the ten-leg panel, and `check_harness` (`:537-538`) fails the audit on any leg-name drift. An 11-leg runner → entry command exit **1**, self-test **14/22** exit 1, tool unchanged. The prose "literals of the tool's independent oracle" is only true of the runtime oracle (`:290-302`); the 22 seeds are `text.replace` edits of the runner's live bytes. Round-51 amendment 2 already names this coupling. | `probe-11leg-runner-exit1.txt`, `probe-11leg-selftest-14of22.txt`, `tools/tally-audit-v2.py:67,107,537-538,601-655` |
| F3 | low — row text | Self-test cell's "one seeded-fault case per check" misstates the panel: 22 = 1 pristine + 17 seeded-fault (runtime 7, harness 5, static 2, head 2, **1 unattributed**) + 4 equivalence cases expecting exit 0. | `tools/tally-audit-v2.py:630-655` |
| F4 | low — row text | "a timed-out then-regression reports 124" — the gate neither exits nor prints 124; the inner `timeout` does and the tool folds to 2 (verified). Declared set correct, phrasing loose. | `tools/tally-audit-v2.py:588-591` |
| F5 | low — disclosed risk | The sweep deletes the fixed global `/tmp/tally-audit-work`, which the tool never creates, outside its own TMPDIR — cell 7 does disclose it, but concurrent runs race on it and an unrelated owner of that path loses it. | `tools/tally-audit-v2.py:265,101`; `probe-fixed-tmp-path.txt` |
| F6 | low — context | The `--then-regression` add-on cannot run from a clone (needs the sibling fleet repos); exits 2, which is declared. Not the row16 blocker. | `probe-then-regression-from-clone-exit2.txt` |
| F7 | cosmetic | Write-scope glob `tally-audit-v2.*` does not literally match the selftest scratch prefix `tally-audit-v2-selftest.*`. No behavioural gap. | `tools/tally-audit-v2.py:562,656` |

**No counter-breaking mismatch.** The row passes the frozen C3 predicate and is covered at CAND.
F1 and F2 are the two defects a falsification wave exists to surface: both are measurable against
source, both are inconsistent with the lane's own sibling row or its own amendment, and neither is
visible to the frozen counter.

## 6. What I did not do

No lane source written, no row repaired, no lane build/test/lint run, no commit/push. No sibling
gate executed beyond the target tool, the frozen counter's own `measure.py` logic (read-only
import), and `git show` / `git clone --shared` reads. Lane `git status --porcelain` shows only the
wave-2 output directories this seat and its peers were told to write.

## 7. Receipts

`.ufo/waves/round-51/w2/@P@ExecTool19/`:

* `row-raw-SKILL.md-2160.txt` — the row's exact bytes at CAND
* `selftest.stdout.txt` / `selftest.stderr.txt` — row's self-test: exit 0, 22/22, 150.75 s
* `usage-stdout.txt` / `usage-stderr.txt` — usage probe: exit 2
* `entry-audit.stdout.txt` / `entry-audit.stderr.txt` — entry command: exit 0, all four checks PASS
* `counter-row-logic.txt` — frozen counter's `row_reason` / `run_row` on this row (both `None`)
* `probe-broken-runner-exit1.txt` — tool really fails on a weakened runner (gate, not probe)
* `probe-then-regression-undeclared-exit64.txt` — **F1** end-to-end `TOOL_EXIT=64`
* `probe-exit-code-passthrough.txt` — **F1** verbatim passthrough: 1, 2, 64, 3, -9
* `probe-11leg-runner-exit1.txt` — **F2** entry audit red on an 11-leg runner
* `probe-11leg-selftest-14of22.txt` — **F2** self-test 14/22 on an 11-leg runner
* `probe-fixed-tmp-path.txt` — **F5** attribution of the `/tmp/tally-audit-work` removal
* `probe-then-regression-from-clone-exit2.txt` — **F6** `--then-regression` from a clone, exit 2

Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool19/` deleted before yield.
