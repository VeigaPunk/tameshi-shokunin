# Round-35 w2 — ScoutHarnessRegion

Seat: `ScoutHarnessRegion` (leaf scout, godspeed). Lane pin at dispatch: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (scratch checkout, read-only).

Frozen bytes, sha256 of the scratch checkout (and of the fleet worktree at the same pin; both matched):

- `tools/mutate-and-run.sh` `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (106538 bytes, 2080 lines)
- `tools/tally-audit-v3.py` `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`
- `tools/tally-audit-v2.py` `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`

Attacked: the runner's tally selftest harness, the region the v3 tool brackets with `HARNESS_START` / `HARNESS_END` (`local tblock` … `tblock=$tblock_full`). Question: what that region asserts, which faults `faults()` enumerates, and which of those asserts a weakened harness can still satisfy.

No installs. Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/`. No git mutation, no write under `/home/vgpnk/Projects/shokunin/` except this report.

C1 is not shown false. The pinned harness rejects every panel fault. The limits below are about which asserts are load-bearing and about the scorer that judges them.

---

## Region boundaries (pinned runner)

`tally-audit-v3.py` anchors, applied to the pinned runner (`HARNESS_START` / `HARNESS_END` / `EXTRACT_RE`, each exactly one hit):

| anchor | line | text |
|---|---|---|
| start | **1992** | `  local tblock tgot tvec ti tj` |
| extract | **1994** | `  tblock=$(awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' "$SELF")` |
| end | **2040** | `  tblock=$tblock_full` |

Span **1992–2040** inclusive (49 lines, 2922 bytes). `local tblock_full=$tblock` at **2035** is inside the span and is not the end anchor (`HARNESS_END` is `tblock=$tblock_full`, not the reverse). The next `st` calls (help, missing `--target`) at 2042+ are outside the region and are not part of the harness check.

The block the awk extracts is byte-identical to `REF_BLOCK` (`tally-audit-v3.py:100-139`): both 1562 bytes, `awk` exit 0. The harness injects statuses around that block; it does not re-derive the oracle.

Command: `python3 /fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/probe_harness.py` exit **0**.

---

## What the region asserts

Nine `st` calls. `tally_line` (1998–2007) is the comparator: exit code **and** the first stdout line (`${out%%$'\n'*}`), joined by `&&`, at **line 2006**. The tally script it writes pins one config only, **line 2003**: `local root=selftest-tally auto=0 KEEP=1`. It does not sweep the four `(auto,KEEP)` triples, and it does not compare `REGRESSION_WORKDIR`.

Call inventory (24 `tally_line` sites = 1 + 9 + 9 + 4 + 1):

| id | lines | assert, on success |
|---|---|---|
| A0 | 1996–1997 | awk block non-empty and exactly 9 `st_<leg>=$?` names from `run_regression` |
| A1 | 2008–2009 | nine zeros → `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, exit 0 |
| A2 | 2010–2021 | status **1** at each index 0..8 → `FAIL (… failed=1 setup=0)`, exit 1, **9/9** (`tgot -eq 9` at 2019) |
| A3 | same loop | status **2** at each index 0..8 → `SETUP (… cannot-verify=1)`, exit 2, 9/9 |
| A4 | 2024, 2030–2031 | `1 1 0 0 0 0 0 0 0` → `FAIL (… failed=2 setup=0)`, exit 1 |
| A5 | 2025 | `2 2 0 0 0 0 0 0 0` → `SETUP (… cannot-verify=2)`, exit 2 |
| A6 | 2026 | `1 2 0 0 0 0 0 0 0` → `FAIL (… failed=1 setup=1)`, exit 1 (FAIL wins over SETUP) |
| A7 | 2027 | `3 0 0 0 0 0 0 0 0` → `SETUP (… cannot-verify=1)`, exit 2 (status 3 is not a pass; **index 0 only**) |
| A8 | 2035–2039 | `sed` drops the last `"$st_<leg>"` on the first `for st in` line; the result must be `SETUP (case-tally mismatch: cases=9 counted=8)`, exit 2, and the sed must actually change the block (`[[ != ]] && tally_line`) |

Index order, from `REF_NAMES` and the operand list at runner 1433: 0 `st_js`, 1 `st_kagi`, 2 `st_tsu`, 3 `st_mado`, 4 `st_checklist`, 5 `st_claims`, 6 `st_roundgate`, 7 `st_sourcescheck`, 8 `st_citecheck`.

On the reference block the independent harness runner (same `st` contract as `run_harness`) recorded `HARNESS cases=9 failed=0`, bash exit 0. Reconfirmed by the tool: `CHECK` detail `reference cases=9; faults rejected=34/34`.

---

## What the v3 panel enumerates

`faults()` at `tally-audit-v3.py:569-616`. **34** names, no duplicates. Every fault block is byte-identical to `tally-audit-v2.py:faults()` (`FAULT_BLOCKS_IDENTICAL 34 of 34`, both directions empty). Round 35 did not add a harness-panel fault; the four round-35 fixes sit in the runtime oracle, the code view, and the auto-root witness, not in this region.

| # | fault | built by |
|---|---|---|
| 00 | `label` | every `passed=%s` → `passing=%s` |
| 01 | `fail-exits-0` | first `exit 1` → `exit 0` |
| 02 | `drop-last-operand` | drop `"$st_citecheck"` from the `for` line |
| 03–11 | `ignore-<leg>` ×9 | unconditional `<leg>=0` before the loop |
| 12–20 | `ignore-alone-<leg>` ×9 | zero the leg only when it is the single status-1 or status-2 leg |
| 21 | `guard-removed` | delete the `!= nlegs` guard |
| 22 | `guard-overcount-only` | `!= nlegs` → `> nlegs` |
| 23 | `setup-before-fail` | swap the FAIL and SETUP `if`s |
| 24 | `fail-needs-exactly-one` | `$nfail -gt 0` → `-eq 1` |
| 25 | `setup-needs-exactly-one` | `$nsetup -gt 0` → `-eq 1` |
| 26 | `status-3-passes` | arm `3)` counts as `npass` |
| 27 | `fail-exits-2` | first `exit 1` → `exit 2` |
| 28 | `fail-wording` | `failed=%s` → `failures=%s` |
| 29 | `setup-wording` | `cannot-verify=%s` → `unverified=%s` |
| 30 | `verdict-word` | `REGRESSION: FAIL` → `REGRESSION: FAILURE` |
| 31 | `pass-wording` | ledger phrase → `ledger legs ok` |
| 32 | `printf-counts-swapped` | first FAIL printf swaps `$nfail` and `$nsetup` |
| 33 | `guard-overcount-only-alt` | `> nlegs` and message `tally over` |

`check_harness` (`tally-audit-v3.py:664-680`) accepts the reference iff `cases>0` and `failed==0` (it does **not** pin `cases==9`), then rejects a fault iff the run prints `HARNESS` and `failed!=0`. **`r is None` (no `HARNESS` line) is counted as rejected** — lines 675–676.

---

## What I could not break

Unweakened pinned section, independent bash, same injection as `run_harness` (splice `tblock=$AUDIT_INJECT` after the last extract, `SELF` = pinned runner):

- reference `HARNESS (9, 0)`, bash 0, `ref_ok`
- **0 of 34 accepted, 0 aborted**

Tool's own `check_harness` on the pinned bytes: `ok=True`, `reference cases=9; faults rejected=34/34`.

The docstring's named weakenings (`tally-audit-v3.py:80-81`, and the selftest seeds at 791–795) each accept at least one panel fault while the reference stays green. Measured, not assumed:

| weakening (the form the selftest / round-32 counter actually uses) | reference | accepted |
|---|---|---|
| exit only (`[[ $rc -eq $want_rc ]]`, H03, selftest 791) | (9, 0) | **6**: `label` `fail-wording` `setup-wording` `verdict-word` `pass-wording` `printf-counts-swapped` |
| swallowed (`rc=$?` after the compare, H04, selftest 792) | (9, 0) | **all 34** |
| skip position 8 by duplicating 7 (`for ti in 0 1 2 3 4 5 6 7 7`, H05, selftest 793) | (9, 0) | `ignore-st_citecheck` `ignore-alone-st_citecheck` |
| skip position 0 (`6 1 2 3 4 5 6 7 8`, selftest 794) | (9, 0) | `ignore-alone-st_js` only |
| skip position 1 (`0 3 2 3 4 5 6 7 8`, selftest 795) | (9, 0) | `ignore-alone-st_kagi` only |
| skip any index 2..8 the same way | (9, 0) | that index's `ignore-<leg>` **and** `ignore-alone-<leg>` |
| drop one multi vector (N01: two-fail / two-setup / mixed / status-3) | (8, 0) | exactly one: `fail-needs-exactly-one` / `setup-needs-exactly-one` / `setup-before-fail` / `status-3-passes` |
| guard stress `&&` flipped to OR, or the tally call replaced by `true`, or the block deleted (N02) | (9, 0) or (8, 0) | exactly `guard-removed` `guard-overcount-only` `guard-overcount-only-alt` |
| `rc -ge want_rc` (the H24 comment on `fail-exits-2`) | (9, 0) | `fail-exits-2` only |
| compare with OR instead of AND (N03) | (9, 0) | the 6 wording faults **plus** `fail-exits-0` `fail-exits-2` |
| drop the all-pass assert (H11 comment) | (8, 0) | `pass-wording` only |
| `[[ $tgot -ge 8 ]]` or `-ge 1` in place of `-eq 9` | (9, 0) | **16**: every `ignore-alone-*`, plus `ignore-*` for indices 2..8 (not `ignore-st_js` / `ignore-st_kagi`, which the multi vectors still hit) |

The round-32 hole (a skipped singleton at index 0 or 1 was invisible, because `ignore-<leg>` at those indices is also caught by the multi vectors) is **closed** on this panel: `ignore-alone-*` fires only for a single status 1 or 2, which no multi vector produces. Skipping index 0 accepts `ignore-alone-st_js` and nothing else. Tool-confirmed: `H05-skip0 ok=False … accepted: ignore-alone-st_js`.

Commands (both exit **0**):

- `python3 /fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/probe_weak.py`
- `python3 /fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/probe_toolcheck.py`

`probe_toolcheck.py` calls `check_harness` itself. Its `H03` / `H04` / `H05-skip0` / pristine lines match the independent runner, including the accepted-name lists.

---

## BOUND — three asserts are not load-bearing

Deleting any one of these leaves the reference green and **34/34 rejected**. A harness weakened that way still satisfies the whole panel, and `check_harness` returns pass.

1. **A0, the extract / name-count assert (1996–1997).** `drop-extract`: independent `ref=(8, 0) acc=0`. Tool: `ok=True detail=reference cases=8; faults rejected=34/34`. No panel fault fails extraction, because every fault is injected *after* the awk line; the awk still reads the pinned runner. The check also never inspects whether the awk pattern is the right one (`run_harness` overwrites `tblock` from `AUDIT_INJECT`). Round-34's note that extraction correctness is ignored while `EXTRACT_RE` matches at least once still holds at this pin.
2. **The status-1 entry of the position loop (the `1:1:REGRESSION: FAIL …` arm at 2010), with the status-2 arm kept.** `drop-status1-vector`: `ref=(8, 0) acc=0`. Tool: `ok=True … cases=8; faults rejected=34/34`.
3. **The status-2 entry, with the status-1 arm kept.** Same: tool `ok=True … cases=8; faults rejected=34/34`.

`ignore-alone-*` is caught by **either** arm (the fault triggers on status 1 and on status 2). `fail-wording`, `verdict-word`, `fail-exits-0`, `fail-exits-2`, and `printf-counts-swapped` are also caught by A4 and/or A6. `setup-wording` is also caught by A5 and A7. So neither arm is the sole witness of any panel fault. The load-bearing position check is "every index is visited," which is what the H05 duplicate-index shape breaks, not "both status values are present."

`check_harness` line 669 treats any `cases>0` as a live reference. Dropping an `st` (cases 9 → 8) is not itself a failure.

---

## BOUND — abort is scored as a reject

`check_harness` lines 675–676: if the harness prints no `HARNESS` line, the fault is not added to `accepted`. A comparison weakened to

```bash
[[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]] || exit 1
```

(one hit, line 2006) keeps the reference at `(9, 0)` and **aborts all 34 faults**. Independent: `ref_ok acc=0 abort=34`. Tool: `die-on-mismatch ok=True detail=reference cases=9; faults rejected=34/34`.

The check passes. The weakened harness did not record a single `st` failure; it died, and the scorer counted death as detection. This is outside the docstring's parenthetical (those weakenings return a status, and each one is caught). It is not a C1 break: the tally block is untouched, so the copy is behaviorally an accept under C1's predicate. It is a limit on reading `CHECK harness PASS` as "every fault produced `failed!=0`."

---

## BOUND — asserts the sound harness still satisfies

These are not panel faults. Each was injected into the **unweakened** section. `HARNESS (9, 0)` means every assert above returned success.

| specimen | result | why every assert still holds |
|---|---|---|
| status **4** counts as `npass` | accepted `(9, 0)` | the region never sends a status other than 0, 1, 2, and a single 3 |
| FAIL-path `REGRESSION_WORKDIR` text `(kept)` → `(retained)` | accepted `(9, 0)` | line 2006 compares the first line only |
| `nfail=0` when `auto==1 && KEEP==0` (the runner's real default) | accepted `(9, 0)` | line 2003 pins `auto=0 KEEP=1` |
| same gate on `(auto,KEEP)=(0,0)` and on `(1,1)` | accepted `(9, 0)` | same pin |
| same gate on `(0,1)` | **rejected `(9, 3)`** | that is the pin; the three FAIL asserts fire |
| PASS-arm workdir phrase `removed on PASS; --keep retains` → `deleted on PASS` | accepted `(9, 0)` | that arm is `auto==1 && KEEP==0`, never taken |
| guard message `case-tally mismatch` → `tally mismatch`, operator left at `!=` | **rejected `(9, 1)`** | A8 does compare that string |

So a weakened *tally* can satisfy the entire harness region whenever the defect is off the pinned config, off the first stdout line, or off the status set {0,1,2,3-at-index-0}. The audit as a whole does not: `check_runtime` is a separate check and is the one round 35 widened to four configs and full stdout. This seat did not re-run that sweep. The harness check alone would accept every row marked accepted above.

A8 is an undercount stress only (one operand removed, all-zero vector). It never duplicates an operand. `guard-overcount-only` and `guard-overcount-only-alt` therefore fail A8 for the same reason (undercount falls through to PASS, exit 0). The alt's message change is not what the harness observes. A message-only edit, tested separately, is rejected — so the string at line 2038 is load-bearing, but the panel's alt fault does not isolate it.

---

## HYGIENE — two "ONLY" comments are false

`tally-audit-v3.py:605-610` says each of those faults "is visible ONLY through the case a weakened harness deletes," and names the weakening:

- `fail-wording` / "H06: status-1 entry deleted" — **false.** Deleting that entry accepts nothing (BOUND above). The fault stays rejected by A4 (`1 1 0…`) and A6 (`1 2 0…`).
- `setup-wording` / "H05: status-2 entry deleted" — **false.** Same measurement, witnesses A5 and A7.
- `fail-exits-2` / `rc -ge` — true (that weakening accepts it and only it).
- `pass-wording` / drop all-pass — true (only that fault).
- `verdict-word` / line match loosened — true for the loosenings that were run (exit-only, 11-char prefix, and `||` all accept it). Not the sole fault those loosenings accept.

The H-numbers in those comments are not the round-32 ids (H03 exit-only, H04 swallow, H05 skipped index, N01 dropped vector, N02 guard, N03 `||`). The behaviors those round-32 ids name are the ones the selftest seeds, and those are caught.

---

## Commands

Pin (exit 0). First `git clone` into the scratch path exited 128 (`destination path … already exists`, that tree was at `d16f9b5a`, runner sha already `a7d3f2dd…`, v3 sha was **not** the freeze). Removed that scratch checkout and re-ran the prescribed clone:

```text
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r35-seats/ScoutHarnessRegion/lane
git -C …/lane checkout -q --detach 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

`rev-parse` → `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. sha256s as in the header.

| command | exit | what it established |
|---|---|---|
| `python3 …/probe_harness.py` | 0 | anchors 1992/1994/2040 each unique; section 1992–2040; awk block == `REF_BLOCK` (1562 bytes); panel 34 == v2 panel, block-for-block |
| `python3 …/probe_weak.py` | 0 | independent weakening matrix and the seven non-panel specimens; tool `check_harness` on the pristine runner `ok=True … 34/34` |
| `python3 …/probe_toolcheck.py` | 0 | `check_harness` on pristine, die-on-mismatch, drop-extract, H03, H05-skip0, H04, drop-status1, drop-status2. cmp line = 2006, one hit |

`probe_behavior.py` (instrumented `st` / per-index trace) printed the reference as 9 passing `st` lines and then exited **1** (`PicklingError` in a later pool). Nothing in the ranked findings depends on that trace; the matrix above was re-run under the two exit-0 commands.
