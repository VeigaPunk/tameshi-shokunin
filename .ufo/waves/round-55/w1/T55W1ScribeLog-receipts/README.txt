T55W1ScribeLog-2 receipts — what each file shows (all produced 2026-10-28).

base-freeze-and-rolemix.txt   base and freeze full hashes; wave-1 seat count, role mix, axes
                              (tally over .ufo/waves/round-55/w1/swarm-registry.json)
freeze-manifest-check.out     first observation: worktree sha256 vs freeze.json pins, amendment
                              lists, committed vs worktree before/c2.stdout
freeze-integrity.txt          the same check re-run later: 2 mismatches, freeze 3 / contract 4
before-receipt-drift.txt      committed before/c2.stdout (total=18) vs the amended re-run
                              (total=19, usable=12/13) vs the worktree copy (0 bytes, 43 deletions)
c1-base-explain.stdout        the frozen C1 counter at base: total=10, 8 stale hits in 4 classes;
                              byte-identical to the committed before/c1.stdout
c1-candidate.stdout           the same bytes at the candidate commit 63d08ed1: total=0 PASS
                              (provisional; NOT the deciding run)
c2-candidate-partial.stdout   the frozen C2 counter on the candidate: grammar 8/8, lazy 5/5,
                              empty 13/13 ok, stopped inside the usable arm
allocating-modes-probe.txt    the eight allocating modes driven by hand with an unusable TMPDIR;
                              only repeat-control leaves a stdout token
env-diff-contract-mode.txt    the eighth mode (env-diff --contract) with its fixture: rc 2,
                              one grammar line, empty stdout
repeat-control-stdout.txt     the stdout residue, the proposed one-line fix, and the patched
                              clone's behaviour (stdout empty, own 29-case selftest still PASS)
bash-witness-invocations.txt  bash-witness-study.py takes the `selftest` subcommand; the
                              `--selftest` flag is an argparse usage error (rc 64)
source-fetches.txt            the two round-55 source fetches: HTTP 200, size, sha256, locators
c2-base-amended.stdout       the amended C2 bytes re-run at base: usable=12/13 (registry-check --selftest rc=1), total=19; the frozen receipt's 18 is the pre-amendment instrument
freeze-integrity-at-c0.txt     the manifest check after the L1 re-froze it: freeze.json at e2979f2 lists amendments 1-7 and 7/7 pins match the C0 bytes; no frozen path differs e2979f2..9cf0146
c1-base-refrozen.stdout       C1 at base with the re-frozen bytes: premise=9/10 (R54.9 staged=0), stale=4 classes / 11 occurrences
c1-c0-explain.stdout          C1 at C0 9cf0146: premise=10/10 stale=0 total=0 PASS
registry-check-rev-mode.txt   registry-check --rev at C0: rc 2, stderr grammar, stdout empty (the pre-C0 worktree printed its token on stdout)
c2-c0-amendment7*            C2 at C0 with the amendment-7 bytes: every arm green, bad={}, total=1 PASS=false (the defect amendment 8 repairs)
c2-c0-amendment8*            C2 at C0 with the amendment-8 bytes: total=0 C2_R55_PASS=true
c2-base-amendment8*          C2 at base with the amendment-8 bytes: grammar=6/9 … total=20 (the committed receipt's 21 was one higher than its own arms)
