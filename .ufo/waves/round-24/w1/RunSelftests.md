# RunSelftests — round-24 W1

Verdict: PASS — both selftests green at REV `c8c5b88c8e961a929cdc351b95a7074c76958909` (`command-binding.py --selftest` 44/44 exit 0; `registry-replay.py --selftest` 10/10 exit 0). No defects observed.

## Environment
- Private clone: `/tmp/TameshiR24-2.RunSelftests-r24` (created with `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin <clone>`, then `git checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909`)
- Post-checkout `git rev-parse HEAD` → `c8c5b88c8e961a929cdc351b95a7074c76958909` (matches assigned REV)
- `python3 -V` → `Python 3.14.8`
- No tool installs or updates performed this wave (nothing beyond stock python3 needed).

## Run 1 — command-binding selftest
- cwd: `/tmp/TameshiR24-2.RunSelftests-r24`
- argv: `python3 tools/command-binding.py --selftest`
- exit: `0`
- decisive output lines:
  - `COMMAND_BINDING_SELFTEST: 44/44 pass`
- Case lines observed (all PASS): clean-with-expected-red, source-read-not-command, wrong-cwd, stale-revision, missing, duplicate, unknown, wrong-exit, stderr-cannot-supply-token, bool-exit, empty-requirements, duplicate-requirement, noncanonical-cwd, short-revision, string-exit, bool-expected-exit, blank-argv, argv-order, argv-missing, argv-extra, argv-joined-collision, argv-normalized, argv-second-only, unknown-added, all-stale, second-cwd, multiple-findings, receipt-order-clean, stderr-clean, stdout-surround-clean, duplicate-before-malformed, unknown-expect-key, unknown-receipt-key, unknown-bundle-key, argv-shell-string, all-of-tokens, argv-swapped-between-names, argv-case-only, argv-padded-token, argv-repeated-flag, negative-exit-mismatch, negative-exit-declared-match, tampered, duplicate-json-key (44 CASE lines, every one `PASS`).

## Run 2 — registry-replay selftest
- cwd: `/tmp/TameshiR24-2.RunSelftests-r24`
- argv: `python3 tools/registry-replay.py --selftest`
- exit: `0`
- decisive output lines:
  - `REGISTRY_REPLAY_SELFTEST: 10/10 pass`
- Case lines observed (all PASS): clean, not-held, cleanup, held-missing, stream, stream-at-limit, external, non-hermetic, invalid, plan-realpath (10 CASE lines, every one `PASS`).

## Bounds compliance
- Both selftests executed only inside the private `/tmp` clone; nothing was executed in `/home/vgpnk/Projects/shokunin/tameshi-shokunin` itself.
- No writes anywhere except this report file; no git write commands against the fleet repo.
