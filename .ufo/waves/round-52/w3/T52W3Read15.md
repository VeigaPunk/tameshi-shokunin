# T52W3Read15 — `### The tick and the pin read`

Candidate: `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`; section SKILL.md:1021–1068.

## Findings

None. I found no section statement that fails at CAND1.

## Holds

1. The cited fleet watchdog at `17c1fad` lines 3–5 describes the report-file round boundary and 450-second tick; line 14's then-current lane list omits tameshi. Checked with `git -C /home/vgpnk/Projects/shokunin show 17c1fad:scripts/shokunin-watchdog.sh`.
2. `5efb4114` is dated 2026-10-19 and its `shokunin.conf`, as well as the current fleet `shokunin.conf`, names tameshi. Checked with `git -C /home/vgpnk/Projects/shokunin show -s ... 5efb4114` and `git -C /home/vgpnk/Projects/shokunin show 5efb4114:shokunin.conf` (plus current file read).
3. The lane's `../scripts/hyaku/jj-lane.sh state <repo>` pointer resolves to the fleet helper. `cmd_state` emits `state branch=...`; its branch selection uses `lane_branch_git` (`lane.branch`) then `detect_branch()`. Checked at `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh:101-105,116-129,158-182`.
4. The CAND1 `fleet-kill-rate-ledger.md:420` identifies the branch-tip rule and ER-jj; line 422 records the later correction to cite `detect_branch()` by function name, which the section does. Checked via `git show` at CAND1.
5. Round-17 lesson records source S061 and the jj migration context; the ledger records the round-8 historical 67/67 self-test and six-case table. Checked in CAND1 `corpus/lessons/round-17.md` and `corpus/knowledge/fleet-kill-rate-ledger.md:324-348`.
6. CAND1 round-51 cold-read receipts record the runner's 107/107 output, so the section's round-52 runner count holds; the round-8 67/67 is explicitly historical. Checked with `git grep '107/107 pass'` at CAND1 and the CAND1 ledger receipt above.
7. The section's 4 current / 2 stale / 0 drift tally agrees with its six table rows; its later mado observation explicitly records the live-file change separately from the HEAD blob, consistent with the stated stale-plus-drift reading.

## Summary

- Findings: none.
- Holds checked: 7.
- Section digest (lines joined by `\n`): `9f03259125bbfd3cb5007dd33674c9b1676e871d7bcb14b23f73f403922f4b2c`.
