# T56W1RevNoHarmSet — no-harm monitor audit (round 56, wave 1)

Item: audit the 15 monitors in `.ufo/evidence/round-56/no-harm.sh` against
`contract.json` (`no_harm_monitors: 15`): name each, say what it would catch, say whether it can
turn RED, and answer (a) tree-vs-REV, (b) vacuous-by-base-constant, (c) axes with no monitor.
The script is frozen and **was not edited**; every proposed change is a diff, demonstrated in a
scratch clone or an extracted two-line harness.

- Script: `.ufo/evidence/round-56/no-harm.sh`, sha256 `a13ba1a8433752c8e2d928c129dc4889181f34caa917099d4aaa96ec1d33e3b4`
  (identical to `git show c3e2ca9f:.ufo/evidence/round-56/no-harm.sh`; verified, receipt `noharm-frozen.sha256`).
- Count: **15 emitted lines, 15 names, matches `no_harm_monitors: 15`** (`demo8-exit-status-and-count.stdout`).
- Runs: at BASE `981c5e8b` → 14 ok / 1 RED; at freeze `c3e2ca9f` → 14 ok / 1 RED; the RED is
  `coldread-floor` in both. The single RED is the round's own lowest axis.
- Machine-readable: `T56W1RevNoHarmSet.json` (same directory).

## Headline

Three findings decide the audit:

1. **A1 — the C1-axis monitor is not REV-bound.** `coldread-floor` executes the *working tree's*
   `.ufo/evidence/round-21/coldread/measure.py`, which imports the *working tree's*
   `.ufo/evidence/round-18/measure.py`. Neither has a self-pin and the JSON payload carries no
   pass field. An uncommitted edit to the wrapper makes the line print `score=8 credited=64 ok` at
   `c3e2ca9f`, whose clean bytes read `score=6 credited=46 RED`. The one monitor this round exists
   to turn green is the one a contaminated tree can turn green without touching REV — the R55.7
   failure mode, in the exact place it matters.
2. **A3/C — operability has no monitor at all.** A REV whose
   `tools/receipt-revision-gate.py` is replaced by `sys.exit(0)  # stub: refuses nothing` yields the
   identical 15 lines. `tools-scope` reports `A:tools/receipt-revision-gate.py ok` because it reads
   name-status, and a path added since BASE is `A:` whatever its content.
3. **The set cannot fail as a set.** It exits 0 while printing a RED, prints no line asserting that
   15 monitors ran, and has no `set -e`/`set -u`: a monitor line that never prints leaves no trace.

## The table

`verdict`: **live** = can turn RED on the harm it claims and cannot be fed by the tree;
**weak** = can turn RED but is fakeable, saturating, fail-open, or blind on its claimed input class;
**vacuous** = cannot turn RED at all (none).

| # | monitor | line | reads | would catch | RED-able | base observed | verdict |
|---|---------|------|-------|-------------|----------|---------------|---------|
| 1 | `commandD` | 13–14 | REV (`git show REV:tools/mutate-and-run.sh`) | deletion of the driver's recorded case list | yes (0 cases → RED) | `recorded_cases=10 depth_score=10 ok` | **weak** |
| 2 | `coldread-floor` | 15–16 | **working tree code**, REV data | credit loss at REV (the C1 obligation) | yes (RED at base) | `score=6 credited=46 RED` | **weak** (A1) |
| 3 | `r45-freshness` | 17–18 | **working tree code**, REV data; discards `self_pin` | stale SOURCES row / disputed review | yes | `population=74 fresh=71 score=9 ok` | **weak** (A2) |
| 4 | `r45-coverage` | 19–20 | working tree code, consumes `C2_R45_PASS` (embeds `self_pin`) | loss of S256/S257 row, entry or README index line | yes | `rows=2 entries=2 C2_R45_PASS=true ok` | live |
| 5 | `S160-count` | 21–22 | REV | deletion/duplication of one row (S160) | yes | `1 ok` | **weak** |
| 6 | `registry-rows-not-below-140` | 23–24 | REV vs literal 140 | shrink below 140 rows | yes | `140 ok` | **weak** |
| 7 | `r46-coverage` | 25–26 | working tree code, consumes `C3_R46_PASS` | loss of S258–S260 surfaces | yes | `rows=3 entries=3 C3_R46_PASS=true ok` | live |
| 8 | `r47-coverage` | 27–28 | working tree code, consumes `C3_R47_PASS` | loss of S261/S263/S264 surfaces | yes | `rows=3 entries=3 C3_R47_PASS=true ok` | live |
| 9 | `tools-scope` | 29–31 | REV name-status only | tools/ edit outside the allowlist | yes (`M:` of a non-allowlisted path → RED) | `[] ok`; at freeze `[A:tools/receipt-revision-gate.py ] ok` | **weak** (A3) |
| 10 | `registry-rows-not-shrunk` | 32–34 | BASE+REV | registry row deletion (base 56) | yes | `base=56 rev=56 ok` | live |
| 11 | `r49-generator-capability` | 35–38 | REV bytes into `$SCR`, run there | any movement in the 400-case class histogram | yes | exact line `ok` | live (brittle) |
| 12 | `r50-shrinker-selftest` | 39–41 | REV bytes into `$SCR`, run there | shrinker crash or reported failure | yes (empty output → RED) | `[SHRINK_SELFTEST: cases=14 failed=0] ok` | **weak** (B1) |
| 13 | `r53-scratch-hygiene` | 42–43 | REV (`git grep` at REV) | one syntactic form of `/tmp` use in tools/ | yes | `tmp_hits=0 ok` | **weak** (B2) |
| 14 | `ledger-not-shrunk` | 44–46 | BASE+REV | ledger entry deletion (base 591) | yes | `base=591 rev=591 ok` | live |
| 15 | `sources-not-shrunk` | 47–49 | BASE+REV | SOURCES row deletion (base 140) | yes | `base=140 rev=140 ok` | live |

Tally: **7 live** (4, 7, 8, 10, 11, 14, 15)**, 8 weak, 0 vacuous.**

## (a) Monitors that read the working tree and can pass on a contaminated tree

Five monitors invoke a Python counter by *tree path* (`python3 .ufo/evidence/round-XX/...`), after
`cd "$LANE"`. Three of them are nevertheless safe because they consume the counter's own PASS token,
which embeds a `self_pin` (running bytes vs `REV:` bytes). Two are not:

**A1 `coldread-floor` (line 15) — no guard anywhere in the chain.**
Round-18 `measure.py` has zero occurrences of `self_pin`; the round-21 wrapper has none; the JSON
payload has no `pass`/`self_pin` key (`box3`, `coldread`, `calibration_restraint_score`, `sources`,
`overrides_used`, `trace_gate`, `ledger_source`, `ledger_committed`).

```
-- clean baseline (REV bytes):        score=6 credited=46
-- patch working tree only (no commit; HEAD stays c3e2ca9):
 M .ufo/evidence/round-21/coldread/measure.py
CR=[score=8 credited=64]
NOHARM coldread-floor score=8 credited=64 ok
-- after restore, same REV:           score=6 credited=46
```
receipt `demo2-coldread-tree-code.stdout`. The patch was an early-exit inserted after
`sys.dont_write_bytecode = True` that prints a fabricated payload for any `--repo` invocation; the
lane was never touched (all work in `$S/clone`).

**A2 `r45-freshness` (line 17) — the guard exists and the monitor throws it away.**
```
C1_R45: self_pin=0 population=74 ... C1_R45_PASS=false
F=[population=74 fresh=71 ]
NOHARM r45-freshness population=74 fresh=71 ok
```
receipt `demo1-freshness-selfpin-ignored.stdout`. The counter *told* the monitor the code is not the
REV's code; the grep extracts only `population=`/`fresh=`.

**The contrast (why 4/7/8 are live):** appending one comment to `r45/coverage/measure.py` yields
`C2_R45_PASS=false` and `NOHARM r45-coverage ... RED` (`demo6-coverage-selfpin-consumed.stdout`).
`self_pin` is a mistake-detector, not a forgery detector — a deliberate patch can print
`self_pin=1` — but it is exactly right for the R55.7 threat (uncommitted round work at closure).

**Sweep of the other ten:** `commandD`, `S160-count`, `registry-rows-not-below-140`, `tools-scope`,
`registry-rows-not-shrunk`, `r49`, `r50`, `r53`, `ledger-not-shrunk`, `sources-not-shrunk` all
obtain their subject through `git show REV:`/`git diff BASE REV`/`git grep REV`; `r49`/`r50` even
extract the tool into `$SCR` before running it. None can be fed by the tree.

**Fail-closed sweep:** 14 of 15 turn RED when their measurement errors (empty `$CR` → `KeyError`,
empty `$P`/`$K` → string mismatch, empty `$L1`/`$C1N` → integer-expression error). **`r53` alone
fails open.**

## (b) Base constants that hollow a monitor out

- **B1 `r50-shrinker-selftest` (line 41)** — the guard is the suffix glob `*" failed=0"`, not a case
  count. A shrinker whose selftest runs nothing passes:
  `K=[SHRINK_SELFTEST: cases=0 failed=0]` → `ok` (`demo4-r50-empty-suite.stdout`). A crash is still
  caught (`K=[]` → RED), so the monitor is live against breakage and vacuous against emptiness.
  Fix: `case "$K" in *"cases=14 failed=0")`.
- **`commandD` (line 13)** — `depth_score=min(10,n)` saturates: 40 documented cases print
  `depth_score=10`, same as 10 (`demo10-commandD-saturation.stdout`). It also counts *comment* lines
  (`#   js-kimi-census ... 8/10 (80 %)`), so it measures documentation, not executed cases.
- **B2 `r53-scratch-hygiene` (line 42)** — fails open. `git grep` at an unparsable REV exits 128,
  `awk` still sums to 0:
  `fatal: unable to parse object: 0000…` / `git_grep_exit=128` / `NOHARM r53-scratch-hygiene tmp_hits=0 ok`
  (`demo3-r53-failopen.stdout`). The pattern `dir\s*=\s*["']/tmp` also misses `TMPDIR=/tmp`,
  `"/tmp/x"` bound to another name, and `/tmp` in a non-assignment position.
- **`registry-rows-not-below-140` (line 24)** — the literal 140 is the base count, duplicating the
  base-relative `sources-not-shrunk` (47–49). Two monitors, one surface, different semantics: a
  rewrite of all 140 rows passes both; a legitimate retirement below 140 reads as harm.
- **`S160-count` (line 21)** — a one-row canary out of 140; the other 139 can be rewritten in place
  with the same id.
- **Monotonic counters (10/14/15)** — `-ge` on a count cannot see content drift. This matters for
  C1: the re-key *rewrites* bound ledger entries in place, and `ledger-not-shrunk` cannot see it;
  only `coldread-floor`'s credit arm reacts.
- **`r49-generator-capability` (line 37)** — exact full-line equality including the class histogram.
  Live, but it cannot distinguish a legitimate improvement from a regression, and the failure never
  names which arm moved.
- **`r45-freshness` (line 18)** — live with **zero headroom**: `fresh=71` equals the floor 71, and
  the ratio arm binds at population ≤ 78. The C0 commit adds a SOURCES row (74 → 75: still ok) but
  any single quote drift at the same time is RED (`demo11-freshness-headroom.stdout`).

## (c) Axes with no monitor

1. **Operability (C2) — none.** Proven, not inferred: in `$S/clone2` (scratch clone, toplevel ==
   clone2, asserted) I committed `bafabeb8` with the gate replaced by `sys.exit(0)`. The frozen
   script at that REV prints **the same 15 lines as the freeze run** (14 ok / 1 RED, the RED still
   `coldread-floor`) — `demo7-stub-gate-noharm.stdout`. `tools-scope` admits it as
   `A:tools/receipt-revision-gate.py`; a fixture reproducing the real shape (gate absent at BASE,
   present at REV with replaced content) prints `A:` and `ok` while the bytes are
   `import sys; sys.exit(0)` (`demo5b-tools-scope-A-blindness.stdout`).
   *Mitigation, outside this set:* the C2 counter extracts the gate from REV and runs its suite —
   at `bafabeb8` it reads `selftest=none ... total=6 C2_R56_PASS=false`
   (`demo9-c2-counter-catches-stub.stdout`). So the no-harm set is not the thing that certifies C2;
   the round must not present it as if it were.
2. **Adjacency / the standing calibration row — none.** No monitor opens `SCORECARD.md`, `LOG.md`,
   `SKILL.md` or `corpus/QUALITY.md`. R55.3's exact defect — a standing row asserting 8 at a commit
   where the monitor reads 6 — has no falsifier in this set; only the C1 counter's `restate` arm
   checks that the row states the monitor's score at the commit the row names. Corollary for the
   report: the restated row must be checked by the C1 counter, and this set must not be cited as
   evidence for it.
3. **Round-56 coverage (the C2 quartet) — none.** `r45/r46/r47-coverage` monitor *other rounds'*
   surfaces. At the freeze rev the C2 documentation is `docs=0/4` and this set is 14 ok / 1 RED
   (`noharm-at-freeze.stdout`) — a REV that ships zero C2 content passes 14 of 15.
4. **The set's own completeness and verdict — none.** `script_exit=0` with `lines=15 ok=14 RED=1`
   (`demo8-exit-status-and-count.stdout`); no line asserts the monitor count; no `set -e/-u`; a
   monitor that dies silently is indistinguishable from one that passed to a consumer counting REDs.

## Additional defect: fixed scratch path (S1, line 10)

`SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r56/no-harm` is the same path for every
concurrent run, and the script `rm -rf`s it at start and in the exit trap. Two runs at the **same**
REV are benign — demonstrated, both 15 lines, both 14/1 (`demo12-concurrent-scratch-collision.stdout`).
Two runs at **different** REVs are not: extracting the monitor's own lines 39–40 and running them
concurrently (a 2 s pause widening the window; the frozen file untouched) makes the honest rev
report the other run's shrinker:

```
RUN_A(rev=c3e2ca9f…) [SHRINK_SELFTEST: cases=14 failed=1] RED
RUN_B(rev=baf7f0bf…) [SHRINK_SELFTEST: cases=14 failed=1] RED
-- the honest rev alone: SOLO [SHRINK_SELFTEST: cases=14 failed=0]
```
receipt `demo13-shared-scratch-cross-rev.stdout`. In a 32–64 seat wave, a reviewer running this
script at C0 while the L1 runs it at REV can produce a **false RED on a good revision** (and, with
the roles reversed, a false ok). Fix: `SCR=$(mktemp -d …/tameshi-r56/no-harm.XXXXXX)`.

## Proposed diffs (not applied; the script is frozen)

```diff
@@ line 10
-SCR=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r56/no-harm
+SCR=$(mktemp -d "${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r56/no-harm.XXXXXX")

@@ line 15 (A1: bind the C1 monitor's code to REV)
+git diff --quiet "$REV" -- .ufo/evidence/round-18/measure.py .ufo/evidence/round-21/coldread/measure.py || { echo "NOHARM coldread-floor tree-not-at-rev RED"; s=RED; }

@@ lines 17-18 (A2: keep the counter's own verdict)
-F=$(... grep -oE 'population=[0-9]+|fresh=[0-9]+' ...)
-python3 -c '... sys.exit(0 if f>=71 and 10*f//p>=9 else 1)'
+F=$(... grep -oE 'population=[0-9]+|fresh=[0-9]+|self_pin=[0-9]+|C1_R45_PASS=[a-z]+' ...)
+python3 -c '... sys.exit(0 if s["self_pin"]=="1" and s["C1_R45_PASS"]=="true" and f>=71 and 10*f//p>=9 else 1)'

@@ line 30 (A3: an added file's content is its name-status)
+s=ok; for t in $T; do case "$t" in
+  A:tools/receipt-revision-gate.py) [ "$(git rev-parse "$REV:tools/receipt-revision-gate.py")" = "$(git rev-parse "c3e2ca9f:tools/receipt-revision-gate.py")" ] || s=RED;;
+  M:tools/registry.json|...) ;;
+  *) s=RED;; esac; done

@@ line 41 (B1)
-case "$K" in *" failed=0") s=ok;; *) s=RED;; esac
+case "$K" in *"cases=14 failed=0") s=ok;; *) s=RED;; esac

@@ line 42 (B2: fail closed, widen the pattern)
-Q=$(git grep -c -E "dir\\s*=\\s*[\"']/tmp" "$REV" -- tools/ 2>/dev/null | awk ...)
+Q=$(git grep -c -E '/tmp' "$REV" -- tools/ 2>/dev/null | awk ...); rc=${PIPESTATUS[0]}
+[ "$rc" -le 1 ] || { echo "NOHARM r53-scratch-hygiene unmeasurable rc=$rc RED"; s=RED; }

@@ line 24 (drop the duplicated literal; derive from BASE as line 47 does)

@@ end of script (the set's verdict)
+bad=$(grep -c ' RED$' "$SCR/report"); echo "NOHARM monitor-count $(wc -l < "$SCR/report") REDs=$bad"; [ "$bad" -eq 0 ]
```
(The last one requires the script to tee its lines; a simpler variant is `bad=$((bad+1))` in each
`|| s=RED` arm and `exit $((bad>0))` at the end.)

## Constraints these constants place on the C0 content commit

Derived, each with a receipt:

- `corpus/SOURCES.md` may gain at most **4** rows while `fresh` stays 71 (population 74 → 78 passes,
  79 fails the ratio arm) — `demo11-freshness-headroom.stdout`. C0 adds one: 75, still `score=9 ok`.
- The new `corpus/knowledge/receipt-revision-binding.md` must **not** have a line-1 `source:` citing
  S256, S257 (r45), S258–S260 (r46) or S261, S263, S264 (r47): those counters require exactly
  `entries=2` / `entries=3` and would turn RED on a legitimate addition. Its `source:` line must
  therefore cite the round-56 source row only (plus repo paths).
- SOURCES rows ≥ 140, `tools/registry.json` rows ≥ 56, ledger entries ≥ 591.
- tools/ name-status between BASE and REV must stay inside the allowlist — C0's
  `M:tools/registry.json` is allowed; the gate must remain an `A:` entry.

## Residual risk and verification gaps

- **`self_pin` is not a forgery detector.** A deliberate patch can print `self_pin=1`; the coverage
  monitors (4/7/8) are safe against the R55.7 accident, not against an adversary. The same holds for
  the `A1`/`A2` fixes above: they close the accidental hole, not the deliberate one.
- **Count-only monitors cannot see content.** `ledger-not-shrunk`, `registry-rows-not-shrunk`,
  `sources-not-shrunk`, `S160-count` and `registry-rows-not-below-140` all pass on a REV that
  rewrites every row/entry in place.
- **`r49`'s expected line is a round-49 recording.** It is a change detector; if the generator is
  legitimately touched this round the monitor turns RED and the report must say why, not re-record
  the constant.
- **The stub-gate run is my fixture, not the lane.** `bafabeb8` lives only in
  `/fast/scratch/hyaku/tameshi-r56/T56W1RevNoHarmSet/clone2`; the lane tree was never modified and
  no lane commit was made. `git -C clone2 rev-parse --show-toplevel` printed the clone2 path before
  the commit.
- **Not audited (outside the item):** whether the *counters* are correct at REV (their own selftests),
  and the deciding-run/controls scripts. This audit covers only what `no-harm.sh` measures and how.

## Receipts

All under `T56W1RevNoHarmSet-receipts/`:

| file | what |
|------|------|
| `noharm-at-base.stdout` / `.stderr` | 15 lines at `981c5e8b`, 14 ok / 1 RED |
| `noharm-at-freeze.stdout` / `.stderr` | 15 lines at `c3e2ca9f`, 14 ok / 1 RED |
| `demo1-freshness-selfpin-ignored.stdout` | A2 |
| `demo2-coldread-tree-code.stdout` | A1 |
| `demo3-r53-failopen.stdout` | B2 |
| `demo4-r50-empty-suite.stdout` | B1 |
| `demo5-tools-scope-name-status-only.stdout` | name-status only (file present at BASE → `M:`) |
| `demo5b-tools-scope-A-blindness.stdout` | real shape: `A:` + `ok` for a stub |
| `demo6-coverage-selfpin-consumed.stdout` | contrast: coverage monitors are REV-pinned |
| `demo7-stub-gate-noharm.stdout` | (c)1: stub gate, 15 identical lines |
| `demo8-exit-status-and-count.stdout` | exit 0 with a RED; 15 lines; names |
| `demo9-c2-counter-catches-stub.stdout` | mitigation: the C2 counter catches the stub |
| `demo10-commandD-saturation.stdout` | saturation + comment-line counting |
| `demo11-freshness-headroom.stdout` | population threshold 78 |
| `demo12-concurrent-scratch-collision.stdout` | same-REV concurrency: no effect (sweep) |
| `demo13-shared-scratch-cross-rev.stdout` | S1: cross-REV false RED |
| `noharm-frozen.sha256` | the extracted script's digest equals the lane's frozen file |

Tooling: none installed; `bash`, `git`, `python3` (stdlib) as present. Census
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits 0 (140 rows)
at the start and at the end of this seat.
