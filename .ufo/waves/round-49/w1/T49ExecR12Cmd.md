# T49ExecR12Cmd — round-12 recipe re-execution

Seat: T49ExecR12Cmd (leaf, C1 command re-execution). Base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Target section: `SKILL.md:1479-1513` — `## Repeated controls and gate registry — round 12`.
Deliverable: `.ufo/waves/round-49/w1/T49ExecR12Cmd.json`; receipts: `.ufo/waves/round-49/w1/T49ExecR12Cmd/`.

Setup: `git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane" && git -C "$S/lane" checkout -q --detach 8ca67421111fa354b47b803358391d0b07fc6db9` with `S=/fast/scratch/hyaku/tameshi-r49/T49ExecR12Cmd`; `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`. Every command below ran with `cd $S/lane` (the section's recipe path `/tmp/tameshi-r12-controls-UNIQUE` at `SKILL.md:1492` is a documented scratch example and was replaced by `$S/...` under the 2026-10-25 scratch directive; `$S` is deleted before yield, the citable copies are the receipts).
Tool under test: `tools/repeat-control.py`, 35454 B, sha256 `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25` (`wc -c`, `sha256sum`).

Selftest: `python3 tools/repeat-control.py --selftest` → exit 0, `SELFTEST: PASS (29 cases)` (`T49ExecR12Cmd/selftest.txt`); matches the registry row's `stdout_contains: SELFTEST: PASS` (`tools/registry.json`, row `repeat-control-selftest`).

## Decision table, claim by claim

| SKILL.md | Claim | Re-execution | Matches |
|---|---|---|---|
| 1487 | ≥3 zero-exit controls matching raw stdout+stderr → `controls_match` | `--runs 3 --out $S/r12-controls -- /bin/echo pristine-control` → `REPEAT_COMPARE identical=yes runs=3`, `REPEAT_CONTROL: controls_match`, exit 0 (A.txt) | yes |
| 1488 | any differing exit/stream → `controls_mismatch` | `--runs 3 --out $S/r12-diff -- /usr/bin/date +%N` → `identical=no`, `controls_mismatch`, exit 1 (C.txt); per-run stdout sha256 differ | yes, except the mixed-availability case (M1) |
| 1489 | equal nonzero controls → could-not-evaluate | `--runs 3 --out $S/r12-nonzero -- /bin/bash -c 'exit 7'` → `baseline_nonzero`, exit 2 (D.txt) | yes |
| 1489 | command unavailable → could-not-evaluate | `--runs 3 --out $S/r12-absent -- /nonexistent/r12-cmd` → `command_unavailable`, exit 2 (E.txt) | yes |
| 1493-1495 | "The output directory must not exist" | same `--out $S/r12-controls` again → stderr `--out already exists (refused, never overwritten)`, `invalid_usage`, exit 64 (B.txt); source `tools/repeat-control.py:315-317` uses `os.makedirs(..., exist_ok=False)` | yes |
| 1492 | `--runs 3` | `--runs 2` → `invalid_usage`, exit 64 (L.txt); floor enforced at `tools/repeat-control.py:261-262`, and `SKILL.md:1487` says "Three or more" | yes |
| 1491 | "put evidence outside any tree it inspects" | `/bin/ls` with `--out $S/inspected/ev` (non-recursive, does not read the DIR interior) → `controls_match` exit 0 (J.txt); `/usr/bin/find . -type f` with the same layout → `controls_mismatch` exit 1, run k sees run k-1's evidence files (K.txt) | yes (as written, the warning is about trees the command actually reads) |
| 1494-1495 | "Caller owns timeout policy; hanging commands yield no verdict" | no `timeout=` anywhere in the subprocess call; stated at `tools/repeat-control.py:84-88` | yes (source, not executed) |
| 1495-1497 | "Do not … normalize output … interpret a finite match as proof" | byte comparison only: selftest cases `mismatch-newline-only`, `mismatch-stderr`, `mismatch-run3-only` all PASS at `controls_mismatch/1` (selftest.txt:4-6); limitation text at `tools/repeat-control.py:93-95` | yes |
| 1503 | verdict map `0 clean; 1 failed; 2 and 64 could-not-evaluate` | observed exits 0/1/2/64 with exactly that split (A,C,D+E,G,H,B,L,M); `EXIT_BY_ID` at `tools/repeat-control.py:122-130` | yes |
| 1503 | pinned values `.ufo/evidence/round-12/ControlGate/expected.json`, `mismatch/expected.json` | `--snapshot .ufo/evidence/round-12/ControlGate` → `SNAPSHOT_INPUTS 9 verified`, `controls_match`, exit 0 (G.txt); `--snapshot …/mismatch` → `controls_mismatch`, exit 1 (H.txt); both dirs exist with `expected.json` + 9 run files | yes |
| 1503 | write scope "snapshot read-only" | `sha256sum` of all 20 snapshot files before and after both snapshot runs: identical (`snap-before.sha` == `snap-after.sha`, 20 lines each) | yes |

Registry rows executed exactly as registered (`python3 tools/repeat-control.py --snapshot …`, `--selftest`, relative paths, cwd = clone root) — all three matched their `expect` blocks. No other row in `tools/registry.json` has an argv starting with `tools/repeat-control.py` (56 rows scanned).

## Mismatches between the section and the tool

**M1 — `SKILL.md:1488` omits the availability-first precedence.** Row 2 says "Any available controls differ in exit or either stream → `controls_mismatch`"; the tool tests availability before disagreement (`tools/repeat-control.py:30-32` docstring; `classify()` `:206-209` before `:210-218`).
Evidence: probe script (state-file counter: run1 `A`, run2 `B`, run3 `C` then `rm -f "$0"`, run4 exec fails; source preserved at `T49ExecR12Cmd/vanish-probe.sh`, since the script deletes itself) — `python3 tools/repeat-control.py --runs 4 --out $S/r12-mixed -- $S/probe/vanish.sh` → runs 1-3 `exit=0` with differing stdout, run 4 `exit=unavailable`, and the tool printed `REPEAT_CONTROL: command_unavailable`, exit 2 (I.txt, observations `r12-mixed/run-{1..4}.stdout`). Row 2 read literally predicts `controls_mismatch`, exit 1. The section needs the precedence stated (row 3's "or command unavailable" also matches the observed result, so the two rows conflict in the overlap as written).

**M2 — `SKILL.md:1489` decision cell is prose the tool never emits.** "Could not evaluate baseline" does not occur in `tools/repeat-control.py` (`grep -n "Could not evaluate" tools/repeat-control.py` → no match); the two cases print different IDs with the same exit 2: `REPEAT_CONTROL: baseline_nonzero` (D.txt) and `REPEAT_CONTROL: command_unavailable` (E.txt), from `EXIT_BY_ID` `:122-130` and `finish()`'s `REPEAT_CONTROL: {finding}` line. Rows 1-2 name literal IDs; row 3 does not, so a cold reader cannot map it to a printed string.

**M3 — `SKILL.md:1503` write-scope glob overlaps the recipe's example path.** The cell reserves "isolated `/tmp/tameshi-r12-*` selftest", but the selftest scratch is only `tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")` (`tools/repeat-control.py:597`), while the recipe at `SKILL.md:1492` tells the caller to write evidence to `/tmp/tameshi-r12-controls-UNIQUE` — inside the registry's stated selftest namespace. Observed scratch residue after the selftest run: 0 directories matching `/tmp/tameshi-r12-repeat-control-selftest.*`, so the isolation itself holds; the glob wording and the recipe disagree about who owns `/tmp/tameshi-r12-controls-*`.

**M4 — `SKILL.md:1487` bound drops the tool's scope.** The section says "Only this finite sample matched; not a determinism proof"; the tool says "N finite observations agreed on this host in this environment — it is not a determinism proof and it cures no flakiness" (`tools/repeat-control.py:93-95`). Weaker paraphrase, no false claim; the host/environment scope is load-bearing for a later cold reader.

No other discrepancy: the recipe's remaining sentences (evidence outside the inspected tree, retain raw observations, no retry-until-green, no normalization, non-secret fixture command) match the tool's stated and observed behaviour.

## Cross-reference (advisory, outside this seat's edit scope)

`SKILL.md:1481` cites `corpus/knowledge/repeated-control-precondition.md` as the section's source; that note's pins are stale at base:
- `corpus/knowledge/repeated-control-precondition.md:58` pins 30,557 B / sha `29d80254…`; actual is 35454 B / sha `296fe566…` (`wc -c`, `sha256sum`), and its line cites are shifted: finding map `:115-123` vs actual `EXIT_BY_ID` `:122-130`; precedence `:191-205` vs `classify()` `:206-220`; snapshot validator `:337-435` vs `load_snapshot()` `:361`; selftest `:545` vs `def selftest()` `:592`.
- `corpus/knowledge/repeated-control-precondition.md:35` cites the `--runs` floor at `:245-247`; actual is `:261-262`.
Current pointer: `.ufo/evidence/round-12/verification-final.json` records `tool_sha256 296fe566…`, `passed: true`, and repeat-control selftest/snapshot check rows (`python3 -c` json load).

## Evidence index

`T49ExecR12Cmd.json` (13 command records: argv, exit, stdout_tail, matches_section, skill_line); receipts `T49ExecR12Cmd/{A,B,C,D,E,G,H,I,J,K,L,M,selftest}.txt` (stdout+stderr with the trailing `EXIT=` line) and observation dirs `r12-controls`, `r12-diff`, `r12-nonzero`, `r12-absent`, `r12-mixed` (`command.txt`, `finding.txt`, `run-{1..}.{stdout,stderr,exit}`), plus `snap-before.sha`/`snap-after.sha` and the preserved M1 probe `vanish-probe.sh` (it self-deletes when driven; the copy is provenance, not re-executed). All runs used non-secret fixture commands. No tool installed or upgraded. The lane checkout was not written to (all runs happened in the scratch clone); scratch `$S` removed after the receipts were copied.

## Summary
- Re-executed the round-12 recipe and every decision-table row against `tools/repeat-control.py` (sha256 `296fe566…`) in a clone at base: all 12 verdict/exit claims reproduce (0 / 1 / 2 / 64 as mapped; existing `--out` refused with 64; snapshot dirs verified read-only).
- One substantive mismatch: `SKILL.md:1488` says "any available controls differ → `controls_mismatch`", but the tool decides `command_unavailable` (exit 2) first; demonstrated with 4 runs (three differing zero-exit runs + one unavailable → `command_unavailable`).
- `SKILL.md:1489`'s "Could not evaluate baseline" is not a string the tool emits; the actual IDs are `baseline_nonzero` and `command_unavailable` (both exit 2).
- `SKILL.md:1503`'s `/tmp/tameshi-r12-*` selftest scope overlaps the recipe's `/tmp/tameshi-r12-controls-UNIQUE` example; selftest itself leaves no residue.
- `SKILL.md:1487`'s bound omits "on this host in this environment".
- Selftest PASS (29 cases); all three `tools/repeat-control.py` registry rows match their expectations.
- Advisory: the knowledge note cited at `SKILL.md:1481` carries a stale tool pin (size/sha/line cites).
- No claim decided; no build/lint/test run beyond the tool's own `--selftest` and the registry rows.
