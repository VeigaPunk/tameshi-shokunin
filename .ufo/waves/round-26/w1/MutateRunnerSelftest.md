# MutateRunnerSelftest — round 26, wave 1 (does the runner catch its own round-26 wiring mutants?)

**Verdict: 3 of the 5 named mutants are killed by the tool's own `--selftest`
and 2 survive it. Under the second (file-absent) reading of the spec-file item,
4 of 5 are killed. `--regression` — the production ledger gate — catches
exactly one of the five (the file-absent variant, and only as a SETUP refusal),
and one of the two survivors (`$st_citecheck` dropped from the status loop)
turns `--regression` into a green gate that silently swallows an unverifiable
leg.**

| id | edit (one exact edit per scratch copy) | line | `--selftest` | `--regression` |
|---|---|---|---|---|
| M0 | pristine (control) | — | **PASS** 97/97, exit 0 | **PASS** `cases=9 passed=9`, exit 0 |
| M1 | `local nlegs=9` → `local nlegs=8` | 1430 | **KILLED** — `FAIL leg-count agreement: calls=9 specs=9 nlegs=8 (want 9)` (96/97, exit 1) | **SURVIVED** — `REGRESSION: PASS (cases=8 passed=9)`, exit 0 |
| M2 | drop the `js-cite-check` lent tuple | 1955 | **KILLED** — `FAIL leg-count agreement: selftest leg tuples=8 (want 9)` (95/96, exit 1) | n/a — the tuple exists only inside the selftest |
| M3a | lent tuple killed count `10:5` → `10:4` | 1955 | **KILLED** — `FAIL embedded leg js-cite-check: spec and recorded table agree` (96/97, exit 1) | n/a — same, selftest-only |
| M3b | `TABLE_CITECHECK`: `K_UNRESOLVED_SEV:KILLED` → `:SURVIVED` (table killed count 5 → 4) | 629 | **KILLED** — same check as M3a (96/97, exit 1) | **KILLED** — `REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)`, exit 1 |
| M4a | drop `&& -s "$d/js-cite-check.spec"` from the `regression_specs` guard | 1144 | **SURVIVED** — 97/97 PASS, output byte-identical to the control (`sha256 ae655c36…`) | **SURVIVED** — `REGRESSION: PASS (cases=9 passed=9)`, exit 0 |
| M4b | the `js-cite-check` spec file is never written (heredoc target renamed) | 1082 | **KILLED** — 3 FAILs, 94/97, exit 1 | **KILLED (as SETUP)** — exit 2, `MUTATE: SETUP (cannot write the embedded case specs)` |
| M4c (probe) | M4a **plus** the spec file truncated to empty | 1141 | **KILLED** — `FAIL embedded leg js-cite-check: spec and recorded table agree` (96/97, exit 1) | n/a |
| M5 | drop `"$st_citecheck"` from the status loop | 1431 | **SURVIVED** — 97/97 PASS, output byte-identical to the control | **SURVIVED and masking** — `REGRESSION: PASS (cases=9 passed=8)`, exit 0 |

Answer to the routed question, in one line: **the tool catches the leg-count
and table-agreement mutants (M1, M2, M3a, M3b) and the spec-file-absent
mutant (M4b); it does not catch the removal of the spec-file `-s` guard
(M4a) nor the removal of the cite-check leg status from the summary loop
(M5).**

---

## 1. Scope and provenance

| item | value |
|---|---|
| routed item | round-26 wave-1 `MutateRunnerSelftest` (mutate the round-26 lines of `tools/mutate-and-run.sh` and see what the tool catches) |
| private clone | `/tmp/MutateRunnerSelftest-r26` (created with `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/MutateRunnerSelftest-r26`) |
| clone revision | `a08e85c5d7f899e8a5992e20517edb1a380d79eb` (detached, `git -C /tmp/MutateRunnerSelftest-r26 checkout -q --detach …`) |
| target under test | `tools/mutate-and-run.sh` — 2016 lines, sha256 `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| detector 1 | the tool's own `--selftest` (hermetic, 97 cases at this revision) |
| detector 2 | the tool's own `--regression` (9 ledger legs replayed from the sibling repos' git object stores) |
| scratch root | `/tmp/mrs26/` (mutant copies, outputs, fake fleet roots) |
| host tools | GNU bash 5.3.20(1), Python 3.14.8, git 2.56.0, node v24.21.0, Linux 7.2.11-arch1-1 |

Nothing in the lane was written except this report file. No `jj` command was
run anywhere; no git write command (`add`/`commit`/`checkout`/`reset`/`stash`/
`push`/`fetch`/`pull`) was run in the lane or in any sibling repo. All mutant
runs happened in `/tmp` copies.

## 2. Method

1. Clone the lane at the pinned revision (above) and confirm the target bytes.
2. Control run of the pristine copy: `bash tools/mutate-and-run.sh --selftest`
   → `MUTATE_SELFTEST: 97/97 pass`, `VERDICT: PASS`, exit 0, 5.4 s.
3. For each named mutant: copy the pristine file into its own scratch
   directory (`/tmp/mrs26/<id>/tools/mutate-and-run.sh`), apply **one** exact
   edit, run `--selftest`, record exit code and the failing check names.
4. For the mutants whose effect lives in the `--regression` path (M1, M3b,
   M4a, M4b, M5) also run `--regression` — but only over a **fake fleet root**
   so that the tool's `FLEET_ROOT` (derived as `dirname^3($SELF)`) resolves the
   sibling repos: `/tmp/mrs26/fleet-*/` holds symlinks to the real
   `kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`
   (read-only; `git show` only) plus a real `tameshi-shokunin/tools/` holding
   the mutant copy. The sibling repos are used read-only; every pinned
   revision resolves (`git -C <repo> cat-file -e <rev>^{commit}` → OK for all
   seven pins).
5. Restore proof: the lane file and the clone file are byte-identical to the
   pinned blob before and after all runs (§7).

`--regression` costs ~2m25s per full run on this host (9 legs, ~100 suite
invocations), so it was run on the control, on M1, M3b, M4a, M4b and M5, and
on the two masking probes — not on M2/M3a, whose edits live only in the
selftest body.

## 3. Control (pristine) runs

```
$ cd /tmp/MutateRunnerSelftest-r26 && bash tools/mutate-and-run.sh --selftest
…
PASS embedded leg js-cite-check: spec and recorded table agree
PASS help exits 0
PASS missing --target exits 64
PASS --regression refuses --target (exit 64)
MUTATE_SELFTEST: 97/97 pass
VERDICT: PASS
EXIT=0        (real 0m5.400s)
```

```
$ cd /tmp/mrs26/fleet-pristine/tameshi-shokunin && bash tools/mutate-and-run.sh --regression --keep
…
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
EXIT=0        (real 2m28.522s)
```

The cite-check leg replays the round-26 measurement at its pin
(`REV_CITECHECK=1205c662…`, materialized sha256 `40573448330f52fb…`):
`MUTATE: DONE (target=js-cite-check defects=10 killed=5 survived=5
inconclusive=0 kill-rate=50%)`, `REGRESSION_TABLE js-cite-check:
match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0
flips=0`. The runner and the round-26 sweep record agree at this revision.

## 4. Mutant-by-mutant evidence

### M1 — `nlegs` 9 → 8 (`tools/mutate-and-run.sh:1430`)

```diff
-  local nlegs=9 npass=0 nfail=0 nsetup=0 st
+  local nlegs=8 npass=0 nfail=0 nsetup=0 st
```

```
$ bash /tmp/mrs26/m1-nlegs8/tools/mutate-and-run.sh --selftest
FAIL leg-count agreement: calls=9 specs=9 nlegs=8 (want 9)
MUTATE_SELFTEST: 96/97 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.6wcOvg)
EXIT=1
```

The selftest's r16/r18 leg-count agreement arm (`sed -n 's/^  local nlegs=\([0-9][0-9]*\) .*/\1/p' "$SELF"`)
reads the mutant's own value and fails the check. `--regression` does **not**
catch it — and this is the interesting part:

```
$ bash /tmp/mrs26/fleet-m1/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
REGRESSION: PASS (cases=8 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
EXIT=0
```

The ledger gate prints a self-contradictory summary (`cases=8` but
`passed=9`) and still exits green: `run_regression` never checks that
`npass + nfail + nsetup == nlegs`. Same defect class as M5 below.

### M2 — drop the `js-cite-check` lent tuple (`:1955`)

```diff
     'js-sources-check:js-sources-check.spec:TABLE_SOURCESCHECK:10:5'
-    'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5'
   )
   [[ ${#lent[@]} -eq 9 ]]
```

```
$ bash /tmp/mrs26/m2-drop-lent/tools/mutate-and-run.sh --selftest
FAIL leg-count agreement: selftest leg tuples=8 (want 9)
MUTATE_SELFTEST: 95/96 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.9oZJz9)
EXIT=1
```

(The total case count also drops from 97 to 96: the per-leg agreement loop now
iterates over eight tuples instead of nine.)

### M3a — the lent tuple's `TABLE_CITECHECK` killed count off by one (`:1955`)

```diff
-    'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5'
+    'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:4'
```

```
$ bash /tmp/mrs26/m3-killed-off1/tools/mutate-and-run.sh --selftest
FAIL embedded leg js-cite-check: spec and recorded table agree
MUTATE_SELFTEST: 96/97 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.hJ2P6n)
EXIT=1
```

The per-leg arm parses the embedded spec, compares its ids with the recorded
table's ids, and checks `table_count "$TABLE_CITECHECK" KILLED == 5`. The
mutant expects 4 → the arm fails.

### M3b — `TABLE_CITECHECK` itself carries one killed verdict fewer (`:629`)

The other reading of "TABLE_CITECHECK killed count off by one": flip one
recorded verdict so the table's killed count drops from 5 to 4.

```diff
-TABLE_CITECHECK='K_UNRESOLVED_SEV:KILLED,K_PIN_KIND:KILLED,…
+TABLE_CITECHECK='K_UNRESOLVED_SEV:SURVIVED,K_PIN_KIND:KILLED,…
```

```
$ bash /tmp/mrs26/m3b-table-verdict/tools/mutate-and-run.sh --selftest
FAIL embedded leg js-cite-check: spec and recorded table agree
MUTATE_SELFTEST: 96/97 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.ytVMdr)
EXIT=1
```

This reading is the one both detectors see:

```
$ bash /tmp/mrs26/fleet-m3b/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
REGRESSION_DEFECT js-cite-check K_UNRESOLVED_SEV: measured=KILLED recorded=SURVIVED
REGRESSION_TABLE js-cite-check: match=9/10 recorded-killed=4 measured-killed=5 survived=5 inconclusive=0 flips=1
REGRESSION_CASE js-cite-check: FAIL (out of band: killed-delta=1 flips=1; log: /tmp/tameshi-r4-2-regression.Tam5c6/js-cite-check/sweep.log)
REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
EXIT=1
```

### M4a — drop the `js-cite-check` spec-file check (`:1144`)

```diff
      && -s "$d/js-round-gate.spec" && -s "$d/js-sources-check.spec" \
-     && -s "$d/js-cite-check.spec" ]]
+     && -s "$d/js-sources-check.spec" ]]
```

(The mutant keeps the eight remaining `-s` terms and drops only the ninth; the
original lines 1143-1144 were `&& -s "$d/js-round-gate.spec" && -s
"$d/js-sources-check.spec" \` and `&& -s "$d/js-cite-check.spec" ]]`.)

```
$ bash /tmp/mrs26/m4a-drop-spec-check/tools/mutate-and-run.sh --selftest
MUTATE_SELFTEST: 97/97 pass
VERDICT: PASS
EXIT=0
```

```
$ diff <(grep -E '^(PASS|FAIL) ' baseline.out) \
       <(grep -E '^(PASS|FAIL) ' m4a-drop-spec-check/selftest.out) && echo IDENTICAL
IDENTICAL
```

The mutant's `--selftest` output is **byte-identical** to the control's
(`sha256 ae655c36ebbd39f41f0254e213620763ac1ccb45c2383bd3282285b146609b1b`
for all three files). `--regression` also passes it unchanged:

```
$ bash /tmp/mrs26/fleet-m4a/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
EXIT=0
```

**This is a coverage finding, not a defect in the contract.** The removed
`-s` term is the *production-path* guard that makes `regression_specs` refuse
(`die_setup 'cannot write the embedded case specs'`) when an embedded spec is
empty or missing. The selftest's per-leg parse-and-table arm already covers
the empty-file case — proven by probe M4c (M4a plus a truncation of the
written spec to zero bytes):

```
$ bash /tmp/mrs26/m4c-emptyspec/tools/mutate-and-run.sh --selftest
FAIL embedded leg js-cite-check: spec and recorded table agree
MUTATE_SELFTEST: 96/97 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.I2vwmU)
EXIT=1
```

So the empty-spec scenario is still caught, but by the selftest arm, not by
`regression_specs`. What M4a removes is the fail-closed refusal on the
production path: with the guard gone, an empty embedded spec no longer
produces `MUTATE: SETUP`; the leg instead runs with zero defects and reports a
table mismatch. That is a weaker, later failure mode, not a silent pass.

### M4b — the `js-cite-check` spec file is never written (`:1082`)

The second reading of "drop the js-cite-check spec file check": the file
itself is gone.

```diff
-  cat >"$d/js-cite-check.spec" <<'EOT'
+  cat >"$d/js-cite-check.spec.not-written" <<'EOT'
```

```
$ bash /tmp/mrs26/m4b-spec-file-absent/tools/mutate-and-run.sh --selftest
FAIL embedded leg specs: nine files written
FAIL leg-count agreement: calls=9 specs=8 nlegs=9 (want 9)
FAIL embedded leg js-cite-check: spec and recorded table agree
MUTATE_SELFTEST: 94/97 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.b6ChEi)
EXIT=1
```

```
$ bash /tmp/mrs26/fleet-m4b/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
MUTATE: SETUP (cannot write the embedded case specs)
EXIT=2
```

Both detectors catch this one — `--regression` catches it as a SETUP refusal
(exit 2), the selftest as three failing arms.

### M5 — drop `"$st_citecheck"` from the status loop (`:1431`)

```diff
-  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
+  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck"; do
```

```
$ bash /tmp/mrs26/m5-drop-st-citecheck/tools/mutate-and-run.sh --selftest
MUTATE_SELFTEST: 97/97 pass
VERDICT: PASS
EXIT=0
```

Byte-identical to the control output again
(`sha256 ae655c36…` for baseline, M4a and M5). `--regression` accepts it and
prints a visibly inconsistent summary:

```
$ bash /tmp/mrs26/fleet-m5/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)
REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
EXIT=0        (real 2m29.615s)
```

`nlegs` still says 9, but only eight leg statuses are ever inspected. The
cite-check leg is still *run* (its verdict line is printed), it is simply
never counted.

## 5. The masking probe (M5 is a soundness hole, not just a counter slip)

A counter slip would be cosmetic. The falsifiable hypothesis is stronger:
with M5, a cite-check leg that **cannot be verified** is swallowed and the
gate reports green. Test: break `PIN_CITECHECK` in both runners (pristine and
M5) so the leg is unverifiable, and compare the verdicts.

```
$ sed -n 's/^PIN_CITECHECK=//p' fleet-probe-*/tameshi-shokunin/tools/mutate-and-run.sh
0000000000000000000000000000000000000000000000000000000000000001   (both probes)
```

Pristine runner, same broken pin:

```
$ bash /tmp/mrs26/fleet-probe-pristine/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
REGRESSION_CASE js-cite-check: SETUP (pin mismatch: recorded=0000000000000000000000000000000000000000000000000000000000000001 materialized=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f source=/tmp/tameshi-r4-2-regression.l7B7Qv/js-cite-check/target.cite-check.mjs)
REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
EXIT=2        (real 2m21.633s)
```

M5 runner, same broken pin — **identical leg line, opposite gate verdict**:

```
$ bash /tmp/mrs26/fleet-probe-m5/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep
REGRESSION_CASE js-cite-check: SETUP (pin mismatch: recorded=0000000000000000000000000000000000000000000000000000000000000001 materialized=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f source=/tmp/tameshi-r4-2-regression.avEojX/js-cite-check/target.cite-check.mjs)
REGRESSION: PASS (cases=9 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
EXIT=0        (real 2m21.633s)
```

Both runs execute the same nine legs and print the same per-leg lines; only
the summary differs, because M5 never looks at `st_citecheck`. A leg that
cannot be verified is thus reported as a green ledger. The same holds for a
leg that *fails* (exit 1) — its `st` value is simply not in the loop, so
`nfail` stays 0 and the gate prints PASS.

This is the same structural gap M1 exposes from the other side: `run_regression`
has no invariant tying `nlegs` to the number of statuses it inspects, and no
invariant tying `npass + nfail + nsetup` to `nlegs`.

## 6. Smallest safe corrections (for the integrator; nothing was changed here)

These are coverage findings about the runner's own self-checks. The contract
(the nine legs, the recorded tables, the exact band) is not in question, and no
production file was edited by this seat. The L1 integrator decides whether to
adopt any of these.

1. **M5 (the soundness hole).** Two independent one-line additions:
   * restore `"$st_citecheck"` to the `for st in …` list at `:1431`; and
   * make the omission impossible to reintroduce — either assert in
     `run_regression` that the number of collected statuses equals `nlegs`
     (e.g. collect the statuses in an array and refuse with
     `die_setup`/`usage_exit` when `count != nlegs`), or extend the existing
     selftest leg-count agreement arm (`:1938-1945`) with a fourth counter
     that counts the `"$st_` references in the loop and requires it to equal
     `nlegs`. The second alone would have killed M5 at `--selftest`; the
     first alone would have kept the gate honest but silent.
   * The same arm should also require `npass + nfail + nsetup == nlegs`, which
     is what M1's `cases=8 passed=9` line shows is currently unchecked.
2. **M4a (redundant guard).** Either restore the ninth `-s` term at `:1144`,
   or replace the growing literal `-s` list with a loop over the written
   specs (`for f in "$d"/*.spec; do [[ -s "$f" ]] || return 1; done`), which
   keeps the production-path refusal and stops the list from drifting from the
   leg set — the same drift class the r16/r18 leg-count arm was added for.

## 7. Restore proof

The lane file was never opened for writing; it is byte-identical to the pinned
commit and to the private clone's copy, before and after every run:

```
$ sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
            /tmp/MutateRunnerSelftest-r26/tools/mutate-and-run.sh
fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de  …/tameshi-shokunin/tools/mutate-and-run.sh
fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de  /tmp/MutateRunnerSelftest-r26/tools/mutate-and-run.sh
```

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain`
shows only other seats' work (`M corpus/knowledge/mte-report-interop.md`,
untracked `.ufo/evidence/round-26/after/`, untracked `.ufo/waves/round-26/`)
plus this report file; the runner is untouched. The sibling repos were read
through `git show`/`cat-file` only, and every run's scratch directory lives
under `/tmp` (`/tmp/mrs26/`, `/tmp/tameshi-r4-2-selftest.*`,
`/tmp/tameshi-r4-2-regression.*`).

Mutant file hashes (sha256 of each scratch copy, all distinct from the
pristine `fb91ef76…`):

| scratch copy | sha256 |
|---|---|
| `m1-nlegs8/tools/mutate-and-run.sh` | `c682c63442f03c216398df207832df8a579cdc4fd03a7c2c5a368378908f1eb2` |
| `m2-drop-lent/tools/mutate-and-run.sh` | `eb75643842c15909135ed4971dfa58c6e9222a83039d437d72cd6f4461238643` |
| `m3-killed-off1/tools/mutate-and-run.sh` | `e14a846f70659b6291853212889be7d57e7f6657b053ee30666d9541d4ec45a9` |
| `m3b-table-verdict/tools/mutate-and-run.sh` | `054126f8f05c61cc8364bdc06c07266df51057195916b0b8fb55c950f87a9c84` |
| `m4a-drop-spec-check/tools/mutate-and-run.sh` | `b2372dd16d71e856043977b9dd0bb1e408a1c2d4507c216deceb5d2405acc2c1` |
| `m4b-spec-file-absent/tools/mutate-and-run.sh` | `4457c8167a8dd3015fc487b87d76652209897a365ac4feff98e68a36405b992c` |
| `m4c-emptyspec/tools/mutate-and-run.sh` | `56bb955a981d0db9c9404fd800b5ae87cafdb4be52b45ef8e62f9d1797583580` |
| `m5-drop-st-citecheck/tools/mutate-and-run.sh` | `ab14287950fa9bb0a0fee4e0960855f53b773453b0bc6fbe866e0deb1ca71461` |
| `fleet-probe-pristine/…` (broken pin) | `b0fb68ce76db11efe370ef258d954ec9fc075c181a4c00a5782ef4ba6ed875ce` |
| `fleet-probe-m5/…` (broken pin) | `2985e3b89532cf1817aeaa032b5e93bf428e6b8f09efc50fdf07c5910efb49a4` |

## 8. Tooling

No tool was installed or upgraded by this seat; every command ran on the
host's pre-existing bash 5.3.20(1), Python 3.14.8, git 2.56.0 and node
v24.21.0. No `pacman` transaction was attempted (the host-wide pacman guard
is PAUSED), and no host service was restarted.

## 9. Summary for the integrator

* The runner's `--selftest` is the effective detector for the round-26 wiring
  edits: it kills M1, M2, M3a, M3b, M4b and M4c.
* Two named mutants survive `--selftest` completely (M4a, M5) — their
  `--selftest` output is byte-identical to the control's.
* `--regression` detects only the table-verdict reading (M3b, as a FAIL) and
  the file-absent reading (M4b, as a SETUP refusal). It does **not** detect
  M1, M2, M3a or M4a, and M5 makes it *mask* an unverifiable or failing leg:
  the same nine legs and the same per-leg lines end in `REGRESSION: SETUP …
  cannot-verify=1` (exit 2) on the pristine runner and `REGRESSION: PASS …
  cases=9 passed=8` (exit 0) on the M5 runner.
* Suggested smallest corrections are in §6; this seat changed no production
  file.

Report: .ufo/waves/round-26/w1/MutateRunnerSelftest.md
