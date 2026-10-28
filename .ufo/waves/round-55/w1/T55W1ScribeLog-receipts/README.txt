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
