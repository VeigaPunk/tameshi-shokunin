# ReviewTool — tally-audit-v2.py (frozen bytes at f6d8a891f1d966c5c3cdda385090da3a6e804675)

Reviewer seat: tameshi-r33-w1-ReviewTool-4. Scratch: /fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-ReviewTool-4/

Reviewed object: the tool bytes at lane commit f6d8a891 (sha256 9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4, 608 lines), extracted via `git -C tameshi-shokunin show <f6d8a891>:tools/tally-audit-v2.py` (exit 0). Runner bytes at the same commit: sha256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 == working copy, unedited. All audit runs below executed the FROZEN tool bytes from scratch (tally-audit-v2-probe.py = frozen, sha 9dbbce62…). Every cited command had its exit code captured via `…; echo $? > file`.

## Verdict first

v2 is faithful to its documented design (no held-out path reads, no memorized digests, stdout-only comparison and --then-regression timeout both hold) but does **not** beat the sealed round-32 held-out set: byte-exact replays of all 22 committed held-out runner copies give **5 wrong verdicts** — 2 false PASSes on kill-class defects (HeldOutGuard-2, HeldOutTallyArms-02) and 3 false SETUPs on behavior-preserving accept-class copies (HeldOutRefactor-a1, -a2, HeldOutTallyArms-04). 17/22 match ground truth (8/10 kills caught, 9/12 accepts pass). The tool's own `--selftest` is 21/21, which hides these holes because 16/22 held-out classes have no byte-matching seed.

## Findings by severity

### CRITICAL 1 — False PASS on kill-class HeldOutGuard-2 (divisibility guard)
- Replay: `python3 tally-audit-v2-probe.py --runner evidence/replay/HeldOutGuard-2.sh` → `CHECK head PASS … CHECK static PASS … CHECK runtime PASS vectors=2395 mismatched=0 … TALLY_AUDIT: PASS`, exit 0 (audits/HeldOutGuard-2.sh.out:1-5, .exit=0). JSON ground truth: set=kill.
- Mechanism: guard is `(( (npass+nfail+nsetup) % nlegs != 0 ))` (HeldOutGuard-2.json edits[0]). Every vector and every stress the tool generates counts exactly 8, 9 or 10 statuses (9-ops loop; stress 'dup' = one operand duplicated → 10 ops, 'drop' → 8 ops, tall lines ~352-361). For those counts divisibility and equality agree (9%9=0, 8%9=8, 10%9=1), so runner and oracle never diverge. The defect only shows on an 18-status doubled panel (JSON witness lists all 9 legs twice), which v2's stress never builds (it duplicates at most one operand per position).
- Smallest safe correction: add a stress sub-case that duplicates ALL operands (full double panel, count=18); then runner prints PASS(cases=9 passed=18) while the oracle expects SETUP(case-tally mismatch cases=9 counted=18) → FAIL.

### CRITICAL 2 — False PASS on kill-class HeldOutTallyArms-02 (126|127 flag arm)
- Replay: `… --runner evidence/replay/HeldOutTallyArms-02.sh` → PASS, exit 0 (audits/HeldOutTallyArms-02.sh.out:1-5). JSON ground truth: set=kill.
- Mechanism: arm `126|127) nsetup=1 ;;` (HeldOutTallyArms-02.json edits[0]) turns the setup counter into a flag; it is indistinguishable from correct counting unless 126 AND 127 coexist in one vector. v2's status sweep places exactly one non-zero status per vector; the count-pair and mix vectors use only statuses 0/1/2. No tested vector contains both 126 and 127 (JSON witness [126,127,0…0]).
- Smallest safe correction: add interaction vectors combining 126 and 127 (e.g. [126,127,…] and placements).

### HIGH 3 — False SETUP on accept-class HeldOutRefactor-a1 (helper-function refactor)
- Replay exit 2: `TALLY_AUDIT: SETUP (counting \`case $st in\` not found)` (audits/HeldOutRefactor-a1.sh.out:1). JSON ground truth: set=accept (semantics-preserving; case moved into a per-leg helper).
- Cause: CASE_RE (frozen line 155) requires a literal `case $st in` inside a matched for-loop extent; a called helper escapes both.

### HIGH 4 — False SETUP on accept-class HeldOutRefactor-a2 (quoted case subject)
- Replay exit 2, same SETUP message (audits/HeldOutRefactor-a2.sh.out:1). `case "$st" in` breaks CASE_RE (line 155). JSON ground truth: set=accept.

### HIGH 5 — False SETUP on accept-class HeldOutTallyArms-04 (arithmetic subject, reordered arms)
- Replay exit 2, same SETUP message (audits/HeldOutTallyArms-04.sh.out:1). `case $((st == 0 ? 0 : st == 1 ? 1 : 2)) in` breaks CASE_RE. JSON ground truth: set=accept.

### MEDIUM 6 — Loop-identity brittleness (independent probes, frozen bytes)
- while-loop rewrite (same semantics, array + index): `SETUP (no loop governing the counting case)` (LOOP_RE, line 152, matches `for` only), exit 2.
- Loop-variable rename `for s … case $s`: `SETUP (counting \`case $st in\` not found)`, exit 2.
- Subshell-bodied case `( case … esac )`: `SETUP (loop has no done)`, exit 2.
- All three are benign copies; any of these shapes in the fresh wave-2 authored set would SETUP the measure.

### MEDIUM 7 — Replay-seed fidelity (item 1)
- Byte-identical selftest seeds exist for 5 of the 7 named mappings: HeldOutLoop-1 (mask_7bit, seed line 541), HeldOutLoop-3 (wrapper, 542-543), HeldOutGuard-1 (majority_guard, 547-548), HeldOutTallyArms-01 (double_count, 549), HeldOutRefactor-a3 (second_extract, 552-553).
- HeldOutRefactor-a4: seed (line 544) differs ONLY by a leading comment `# r32: count the leg statuses once before tallying them.` present in the JSON edit — otherwise identical.
- HeldOutPrintf-1: seed `printf_swap` (line 546) is a DIFFERENT fault (plain field swap `"$nsetup" "$nfail"`) than the held-out mutation (conditional decrement `$((nfail - (nfail > 2 && npass > 0 ? 1 : 0)))`). The runtime oracle catches the real Printf-1 anyway (replay FAIL, exit 1), but the seed does not replay the held-out edit.
- No byte-matching seed at all for 16/22 held-out files: Guard-2, Guard-3, Guard-4, Loop-2, Loop-4, Printf-1, Printf-2, Printf-3, Printf-4, Refactor-a1, Refactor-a2, Refactor-k1, Refactor-k2, TallyArms-02, TallyArms-03, TallyArms-04. The two defeated kill classes (Guard-2, Arms-02) and the three false-SETUP classes (a1, a2, Arms-04) are among them — hence the green selftest (21/21, exit 0, ~90 s) despite 5 wrong verdicts on replays.

## Verified claims (item 3)

- Stdout-only comparison: `run_vectors` redirects stderr to `$TMPDIR/stderr.<i>` and compares rc + first stdout line only (lines 235-236). Probe `stderr-noise.sh` (printf >&2 inside the tally block) → PASS, exit 0 (identical verdict to pristine). Negative control `stdout-noise.sh` → `CHECK runtime FAIL vectors=2395 mismatched=2395` first mismatch `got (0, 'noise to stdout')`, exit 1.
- --then-regression timeout: argv `['timeout', str(THEN_REGRESSION_TIMEOUT), 'bash', runner, '--regression']` (lines 506-509), constant 1200 (line 65), rc 124 → `TALLY_AUDIT_REGRESSION: SETUP (--then-regression timed out after 1200s)` exit 2; only invoked after audit PASS (main gate). Probe with patched constant 3 s on a runner that sleeps 30 s before the tally: `… PASS … TALLY_AUDIT_REGRESSION: SETUP (--then-regression timed out after 3s)`, exit 2; control `timeout 3 bash -c 'sleep 30'` → rc=124.
- Shortcut hunt (item 2): grep over the tool finds no use of held-out paths, `.ufo`, `hashlib`, sha/digest, or any file I/O beyond the runner path; no memorized mutant digests. REF_BLOCK (lines 67-124) is byte-identical (1562 B) to the tally block the tool itself extracts from the live runner (extraction via importing the frozen module's `regression_body`/`tally_block`); REF_NAMES equals the runner's actual `st_*=$?` assignments (9).

## Residual risk and verification gaps

- The production working copy diverged during this review (15:52, sha d0b5fe79a53362fde29739e28cfd448b03b98c674e24dd9d6a0b6484a8435b9d, 624 lines): a DevGuard-driven update adds a dual-config (root/auto/KEEP) sweep and a keep-conjunct selftest case (diff 78 lines). It does NOT address findings 1-6 (no full-panel stress, no 126+127 vectors, CASE_RE/LOOP_RE unchanged). The contract freezes f6d8a891; the L1 should confirm which bytes the wave-2 measurement actually consumes.
- I could not reproduce the peer CriticTool-4's reported PASS on "a nested tally_result wrapper that masks its subshell exit" (my subshell shapes exit SETUP, finding 6); the family is confirmed brittle, but the exact PASS shape is unverified here (peer keeps its own scratch).
- Fresh wave-2 authored sets may extend beyond the 22 committed classes (while/until, renamed variables, quoted subjects, helper functions); v2 currently SETUPs all of them (findings 3-6).
- No tools installed; no production files edited; no git/jj write commands run; all probe/replay code and outputs confined to the seat scratch.

Report: .ufo/waves/round-33/w1/ReviewTool.md
