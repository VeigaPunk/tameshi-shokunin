# DevNlegs — round 33 wave 1: the `nlegs` family against frozen tally-audit v2

## Verdict

**Two non-equivalent mutants survive the frozen tool** (`TALLY_AUDIT: PASS`, exit 0):

| survivor | one-line edit inside `run_regression` | witness status vector | pristine | mutant |
|---|---|---|---|---|
| `nlegs-pair127-recompute` | `nlegs=$((nlegs - (st_tsu == 127 && st_mado == 127)))` after the counting loop | `0 0 127 127 0 0 0 0 0` | `SETUP (cases=9 passed=7 cannot-verify=2)`, exit 2 | `SETUP (cases=8 passed=7 cannot-verify=2)`, exit 2 |
| `nlegs-pair3-recompute` | `nlegs=$((nlegs + (st_js == 3 && st_kagi == 3)))` after the counting loop | `3 3 0 0 0 0 0 0 0` | `SETUP (cases=9 passed=7 cannot-verify=2)`, exit 2 | `SETUP (cases=10 passed=7 cannot-verify=2)`, exit 2 |

The tool's runtime sweep contains **no vector with two co-occurring statuses outside `{0,1,2}`**. Replaying the
tool's own vector construction (`tool.py:299` `count_vectors`, `tool.py:309` `check_runtime`) gives 2377 vectors
(the tool's `vectors=2395` log line is 2377 + 18 dup/drop stress runs), maximum co-occurring non-`{0,1,2}` statuses
**1**, vectors with ≥2: **0** (`out/vector-space.txt`). A copy that
recomputes `nlegs` from a conjunction of two legs' statuses is therefore invisible to the oracle, while every
single-leg and every count-based recomputation is killed (`runtime=FAIL` in all six `recompute-*` /
`nlegs-decr-pre` rows below). The other ten
passing mutants were proven behaviorally identical over 12 955 vectors.

This is vector sparsity, not a parser blind spot: the static check, the head check and the harness check all pass
the two survivors because the declaration is still `local nlegs=9`, the leg assignments are untouched, and the
harness check injects `REF_BLOCK` rather than the copy's block (`tool.py:421-437`), so it can never see a
tally-block edit.

Sweep totals: 30 mutants → 17 killed (exit 1), 1 refused as unauditable (exit 2, non-local declaration), 12 passed
(exit 0), of which 10 are equivalent and 2 are survivors. Baseline control PASS; tool and runner bytes at the end
identical to the freeze; I edited no production file and ran no counter.

## Pins and setup

```
mkdir -p /fast/scratch/hyaku/tameshi-r33-seats/DevNlegs      # one-off; no output cited
cd /fast/scratch/hyaku/tameshi-r33-seats/DevNlegs
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin lane;          echo $? > clone.rc          # 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
    f6d8a891f1d966c5c3cdda385090da3a6e804675;                     echo $? > checkout.rc       # 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane show \
    f6d8a891f1d966c5c3cdda385090da3a6e804675:tools/tally-audit-v2.py > tool.py;  echo $? > tool.rc      # 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane show \
    f6d8a891f1d966c5c3cdda385090da3a6e804675:tools/mutate-and-run.sh > pristine.sh; echo $? > pristine.rc  # 0
```

`GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` were unset for every git command (`env -u …`). No git write command,
no `jj` command, nothing written outside my scratch dir and this report.

```
$ sha256sum tool.py pristine.sh
9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
$ git -C <lane> show f6d8a891…:tools/mutate-and-run.sh | sha256sum
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  -
```

Runner matches the pinned `a7d3f2dd…2eb9`. Tool `9dbbce62…33a4` is the instrument, never edited (re-hashed at the
end, unchanged).

Baseline control (`timeout 300 python3 tool.py --runner pristine.sh`, exit 0 in `out/pristine.rc`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=2395 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=29/29
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

The tool's own panel is green as frozen: `timeout 900 python3 tool.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 21/21 pass`,
exit 0 (`out/tool-selftest.log`, `out/tool-selftest.rc`).

## Method

1. `gen.py` / `gen2.py` apply **one exact-string replacement** per mutant after asserting `text.count(old) == 1`;
   no-ops are skipped (three initial candidates were skipped for non-unique or zero matches and re-anchored).
   Every mutant is `m/<id>.sh`; edits recorded in `manifest.json`, `manifest2.json`.
2. Each mutant: `timeout 300 python3 tool.py --runner m/<id>.sh > out/<id>.log 2> out/<id>.err; echo $? > out/<id>.rc`
   — the exit code is captured with `;` on the same command line, never `&&`.
3. Every exit-0 mutant went through `diff.py`: it extracts the pristine block and the mutant block with the tool's
   own `tally_block`/`regression_body`, runs both in bash under `set -u` with `local root=t auto=0 KEEP=1`, and
   compares `(exit code, first stdout line)` over 12 955 vectors — all 256 statuses at all 9 positions; all 55
   `(failing, setup)` count pairs; all 36 position pairs × `{1,2,3,4,126,127,128,255}²`; all 84 position triples ×
   `{(3,3,3),(1,3,3),(2,3,3),(127,127,127)}`; 8000 seeded random 9-tuples over
   `{0,0,0,0,1,1,2,2,3,4,126,127,128,255}`. Command and result: `out/diff.log`, `out/diff.rc` = 0.
4. Witness outputs re-run standalone in fresh drivers (`out/witness-compare.txt` = pristine beside both mutants,
   `out/witness.rc`/`out/witness-compare.rc` = driver exits 0); each tally's printed `rc=` is the block's own exit
   code, which the driver does not propagate.

## Survivors — exact edits, evidence

Both insert one line between the counting loop's `done` and the FAIL branch, i.e. after `pristine.sh:1440`:

```
       *) nsetup=$((nsetup + 1)) ;;
     esac
   done
+  nlegs=$((nlegs - (st_tsu == 127 && st_mado == 127)))     # nlegs-pair127-recompute
+  nlegs=$((nlegs + (st_js == 3 && st_kagi == 3)))          # nlegs-pair3-recompute
 
   if [[ $nfail -gt 0 ]]; then
```

`nlegs` is then read by the four `printf` count fields and the completeness guard (`pristine.sh:1443, 1449, 1456-1458, 1463`),
so the printed `cases=` is wrong on exactly those vectors.

Tool verdict on both: `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, exit 0
(`out/nlegs-pair127-recompute.rc`, `out/nlegs-pair3-recompute.rc`), runtime detail
`vectors=2395 mismatched=0`.

Differential (`out/diff.log`):

```
DIFF nlegs-pair3-recompute.sh nmismatch=48
  witness statuses: 3 3 0 0 0 0 0 0 0
  pristine: (2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')
  mutant:   (2, 'REGRESSION: SETUP (cases=10 passed=7 cannot-verify=2)')
DIFF nlegs-pair127-recompute.sh nmismatch=47
  witness statuses: 0 0 127 127 0 0 0 0 0
  pristine: (2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')
  mutant:   (2, 'REGRESSION: SETUP (cases=8 passed=7 cannot-verify=2)')
```

Independent witness run, pristine block beside both mutant blocks (`out/witness-compare.txt`, driver exit 0 in
`out/witness-compare.rc`):

```
== statuses 3 3 0 0 0 0 0 0 0
  pristine   rc=2 first=REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
  pair3      rc=2 first=REGRESSION: SETUP (cases=10 passed=7 cannot-verify=2)
  pair127    rc=2 first=REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
== statuses 0 0 127 127 0 0 0 0 0
  pristine   rc=2 first=REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
  pair3      rc=2 first=REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
  pair127    rc=2 first=REGRESSION: SETUP (cases=8 passed=7 cannot-verify=2)
```

Each mutant is wrong only on its own trigger pair, which is also why a per-position sweep cannot see either.

Why `nlegs-pair127-recompute` is a plausible defect and not a puzzle copy: 127 is the shell's "command not found",
and two legs can exit 127 together when one interpreter is missing from the sandbox (both `bash-*` legs, or both
`node` legs). A copy whose intent is "a leg that never executed is not a case" is a natural refactor; it misstates
`cases=` and is invisible to the sweep because the tool only ever sets one leg away from `0`/`1`/`2` at a time.

## Full sweep

`PASS (0)` rows marked *equiv* were proven identical to pristine over 12 955 vectors; the two survivors are marked
**SURVIVOR**.

| mutant | edit (new text) | tool exit | failing check(s) | equivalence |
|---|---|---|---|---|
| `nlegs-8` | `  local nlegs=8 npass=0 nfail=0 nsetup=0 st` | FAIL (1) | static, runtime, harness | — |
| `nlegs-10` | `  local nlegs=10 npass=0 nfail=0 nsetup=0 st` | FAIL (1) | static, runtime, harness | — |
| `nlegs-arith-9` | `  local nlegs=$((9)) npass=0 nfail=0 nsetup=0 st` | FAIL (1) | static, harness | tally block identical, copy's own extraction broken |
| `nlegs-quoted-9` | `  local nlegs="9" npass=0 nfail=0 nsetup=0 st` | FAIL (1) | static, harness | tally block identical, copy's own extraction broken |
| `nlegs-leading-zero` | `  local nlegs=09 npass=0 nfail=0 nsetup=0 st` | FAIL (1) | runtime, harness | — (prints `cases=09`) |
| `nlegs-trail-space` | declaration line ends ` st ` | FAIL (1) | harness | tally identical, copy's own extraction broken |
| `nlegs-trail-comment` | declaration line ends ` st  # nine legs` | FAIL (1) | harness | tally identical, copy's own extraction broken |
| `nlegs-nonlocal` | `  nlegs=9 npass=0 nfail=0 nsetup=0 st` | SETUP (2) | — (cannot audit) | tally identical; unauditable by form |
| `failprintf-lit9` | `      9 "$npass" "$nfail" "$nsetup"` | PASS (0) | — | equiv (`nlegs` is 9) |
| `setupprintf-lit9` | `      9 "$npass" "$nsetup"` | PASS (0) | — | equiv (`nlegs` is 9) |
| `passprintf-lit9` | `    9 "$npass"` | PASS (0) | — | equiv (PASS path has `p=9`) |
| `misprintf-lit9` | `      9 "$((npass + nfail + nsetup))"` | PASS (0) | — | equiv (mismatch path has `nlegs=9`) |
| `failprintf-npass` | `      "$npass" "$npass" "$nfail" "$nsetup"` | FAIL (1) | runtime | — |
| `passprintf-npass` | `    "$npass" "$npass"` | PASS (0) | — | equiv (PASS path has `p=nlegs=9`) |
| `failprintf-braces` | `      "${nlegs}" "$npass" "$nfail" "$nsetup"` | PASS (0) | — | equiv (same expansion) |
| `guard-lit9` | `npass + nfail + nsetup != 9` | PASS (0) | — | equiv (`nlegs` is 9) |
| `guard-gt-lit9` | `npass + nfail + nsetup > 9` | FAIL (1) | runtime | — |
| `guard-gt-nlegs` | `npass + nfail + nsetup > nlegs` | FAIL (1) | runtime | — |
| `guard-plus-nsetup` | `npass + nfail + nsetup != nlegs + nsetup` | PASS (0) | — | equiv (guard only reached with `nsetup=0`) |
| `guard-minus-nfail` | `npass + nfail + nsetup != nlegs - nfail` | PASS (0) | — | equiv (guard only reached with `nfail=0`) |
| `recompute-sum` | `nlegs=$((npass + nfail + nsetup))` after loop | FAIL (1) | runtime | — (defeats guard under drop) |
| `recompute-npass` | `nlegs=$npass` after loop | FAIL (1) | runtime | — |
| `recompute-inloop` | `nlegs=$((nlegs + 1))` in loop body | FAIL (1) | runtime | — |
| `recompute-local8` | `local nlegs=8` after loop | FAIL (1) | runtime | — |
| `recompute-plus-nsetup` | `nlegs=$((nlegs + nsetup))` after loop | FAIL (1) | runtime | — |
| `nlegs-decr-pre` | `nlegs=$((nlegs - 1))` before loop | FAIL (1) | runtime | — |
| `nlegs-count-pre` | `nlegs=0` + 9-operand pre-count loop before the tally loop | PASS (0) | — | equiv (pre-count yields 9) |
| `operand-dup-drop` | loop operands with `"$st_citecheck"` → `"$st_js"` (9 operands, one duplicated) | FAIL (1) | static | — |
| `nlegs-pair3-recompute` | `nlegs=$((nlegs + (st_js == 3 && st_kagi == 3)))` after loop | **PASS (0)** | — | **SURVIVOR** |
| `nlegs-pair127-recompute` | `nlegs=$((nlegs - (st_tsu == 127 && st_mado == 127)))` after loop | **PASS (0)** | — | **SURVIVOR** |

Notes on three rows that look like false rejects but are not:

* `nlegs-arith-9`, `nlegs-quoted-9`, `nlegs-trail-*` fail only at the harness check, and that failure is real for
  the copy: the runner's own selftest extracts its tally block with `awk '/^  local nlegs=9 npass=0 nfail=0
  nsetup=0 st$/{f=1} …'` (`pristine.sh:1994`) and its leg-count agreement with
  `sed -n 's/^  local nlegs=\([0-9][0-9]*\) .*/\1/p'` (`pristine.sh:1954-1956`). Any declaration respelling breaks
  `bash copy --selftest`, so rejecting the copy is correct.
* `nlegs-nonlocal` returns SETUP (2) with ``TALLY_AUDIT: SETUP (tally start `local nlegs=` not found)``, not PASS — an unauditable copy is never reported as good. That is the
  documented meaning of exit 2, not a defeat.
* `nlegs-count-pre` shows the round-32 class-3 fix working in this family: an auxiliary 9-operand loop that
  recomputes `nlegs` before the real tally loop is not stressed, the real loop is, and the copy is accepted.

## Smallest safe correction

Extend `check_runtime`'s vector list (`tool.py:309-341`) with co-occurring non-standard statuses before the stress
block:

```python
    # co-occurring non-standard statuses at every position pair (round-33 nlegs recompute class)
    for i in range(n):
        for j in range(i + 1, n):
            for s in (3, 4, 126, 127, 128, 255):
                v = [0] * n
                v[i] = v[j] = s
                vectors.append(v)
```

36 position pairs × the 6 same-status choices = 216 vectors, or 36 position pairs × all 36 status pairs = 1296
vectors. Both witnesses here are same-status pairs (`3 3`, `127 127`), so the 216-vector subset already kills them;
allowing the cross-status pairs costs under a second more and closes the whole dimension. The oracle needs no change: it already expects `cases=nlegs`, so both survivors die on their witness
(`cases=8`/`cases=10` ≠ 9). Do not touch the guard stress, the head check, or the harness injection; the dup/drop
stress is what kills `recompute-sum` and `guard-gt-nlegs` and must stay.

Adding status pairs to an existing status class is exactly the round-32 class-1/class-2 lesson one dimension further
out: the sweep enumerates *one* anomalous leg exhaustively (`0..255` at every position) and *count* combinations
exhaustively, but never a *conjunction of two anomalous legs*.

## Bounds and evidence inventory

* Working dir and every artefact: `/fast/scratch/hyaku/tameshi-r33-seats/DevNlegs/` — `tool.py`, `pristine.sh`,
  `mutate-and-run.sh` (a copy of `pristine.sh` so the tool's `--selftest` default path resolves), `gen.py`,
  `gen2.py`, `diff.py`, `manifest.json`, `manifest2.json`, `m/` (30 mutants), `out/` (per-mutant logs and `.rc`
  files, `diff.log`, `tool-selftest.log`, `vector-space.txt`, `witness.txt`, `witness-compare.txt`), `hashes-before.txt`.
* Nothing outside that directory was written except this report. No production file touched; no `jj`; no git write
  in the lane; no process killed; no counter run (`c1-measure.py`/`c2-measure.py` never invoked).
* Tool installs/upgrades: none — python3, bash, awk, sed, git from the host sufficed.
* Disk: `/fast` had 33–46 GB free throughout; total scratch footprint is a few MB (30 copies of a 2080-line
  script plus logs). No `du`/`find` over `/fast/scratch`.
* Restoration: `pristine.sh` re-hashed after the sweep — `a7d3f2dd…2eb9`, unchanged; `tool.py` — `9dbbce62…33a4`,
  unchanged. Mutants exist only as separate files; the control copy was never edited in place.
