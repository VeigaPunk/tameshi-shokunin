# S07 — mutate-and-run.sh --selftest and --regression at the lane tip

Scope: run `bash tools/mutate-and-run.sh --selftest` and `--regression` in the live lane
(/home/vgpnk/Projects/shokunin/tameshi-shokunin), record exits, counts, elapsed, and the SETUP
behaviour when a sibling pinned revision is missing.

Axes: (1) exit map; (2) assertion/leg counts; (3) elapsed; (4) fail-closed SETUP on a missing
sibling pin; (5) scratch/lane hygiene.

Tool under test: `tools/mutate-and-run.sh` at tip
`98bea7da5801f4bc58e4187690ee1687c8a5061f`; live bytes sha256
`0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa` = committed blob sha256
(`git show <tip>:tools/mutate-and-run.sh | sha256sum`), so the run is against committed bytes.

## 1. --selftest (live lane)

```
$ bash tools/mutate-and-run.sh --selftest
RC=0  ELAPSED_MS=5139
MUTATE_SELFTEST: 83/83 pass
VERDICT: PASS
```

- Exit 0; 83/83 assertions PASS; 85 stdout lines (83 `PASS`, 1 `MUTATE_SELFTEST`, 1 `VERDICT`);
  0 lines matching `^FAIL`; stderr empty.
- Elapsed 5139 ms (5.14 s). Timing via `date +%s%N` deltas because `/usr/bin/time` is not
  installed on this host; the first attempt with `/usr/bin/time -f` exited 127 on the wrapper,
  not on the tool.
- Scratch root is `mktemp -d /tmp/tameshi-r4-2-selftest.XXXXXX` and is removed on PASS
  (`tools/mutate-and-run.sh:1705-1711`: prints `MUTATE_SELFTEST: <pass>/<cases>`, then
  `rm -rf "$root"; exit 0`); no selftest scratch dir from this run remains.

The 83 assertions include the seven embedded leg specs / recorded-table agreement checks and the
regression-engine arms (fixture PASS, pin-mismatch SETUP, missing-target SETUP, unresolvable-rev
SETUP, pin-mismatch on the git leg, exec-bit mirroring, exact-tolerance flip), ending with
`help exits 0`, `missing --target exits 64`, `--regression refuses --target (exit 64)`.

## 2. --regression (live lane, all seven ledger legs)

```
$ bash tools/mutate-and-run.sh --regression
RC=0  ELAPSED_MS=115574
REGEX: REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.pw5min (removed on PASS; --keep retains)
```

| leg | pin source | mode | killed/defects | table match | flips | inconclusive | case |
|---|---|---|---|---|---|---|---|
| js-kimi-census | kumitate-shokunin@175de6b:scripts/kimi-census.mjs | 100644 | 8/10 | 10/10 | 0 | 0 | PASS |
| bash-surface-census | kagi-shokunin@fecee87:corpus/surface-census.sh | 100755 | 8/10 | 10/10 | 0 | 0 | PASS |
| bash-tsukuroi-census | tsukuroi-shokunin@165307f:tools/tsukuroi-census.sh | 100755 | 6/10 | 10/10 | 0 | 0 | PASS |
| bash-mado-verify | mado-shokunin@eead56b:tools/mado-verify.sh | 100755 | 4/10 | 10/10 | 0 | 0 | PASS |
| bash-checklist-run | kagi-shokunin@fecee87:corpus/checklist-run.sh | 100755 | 7/15 | 15/15 | 0 | 0 | PASS |
| js-claims-check | kumitate-shokunin@175de6b:scripts/claims-check.mjs | 100755 | 7/10 | 10/10 | 0 | 0 | PASS |
| js-round-gate | kumitate-shokunin@364f1d5:scripts/round-gate.mjs | 100755 | 5/10 | 10/10 | 0 | 0 | PASS |

- Exit 0; 7/7 cases PASS by the exact ledger band (killed-delta<=0 flips<=0), 0 SETUP, 0 FAIL;
  41 stdout lines, stderr empty; 115574 ms (115.6 s).
- Every leg materialized from the sibling's git object store at the recorded rev, and each
  printed `REGRESSION_PIN ... sha256=<recorded>` with the hash equal to the file's `PIN_*`
  constant (e.g. js-kimi-census `83016d45…`, bash-mado-verify `d7edaab4…`), i.e. no working-tree
  bytes were used. Blob mode is mirrored from `ls-tree` (js-kimi-census is recorded `100644`; the
  other six `100755`), matching `tools/mutate-and-run.sh:1014-1040`.
- Pre-check independently confirmed all seven `REV_*` commits resolve and all seven `<rev>:<path>`
  blobs exist in their sibling repos (`git rev-parse --verify`, `git cat-file -e` — all OK).
- Scratch: on PASS the auto root `/tmp/tameshi-r4-2-regression.pw5min` is removed
  (`tools/mutate-and-run.sh:1250-1256`); verified absent after the run.

## 3. SETUP behaviour when a sibling pinned rev is missing

Contract (header `:107-128`, code `:1144-1256`): a ledger leg resolves its repo as
`$FLEET_ROOT/${rel%%/*}` where `FLEET_ROOT` is three dirnames above `$SELF`
(`tools/mutate-and-run.sh:1164`), then refuses at the first failed precondition with
`REGRESSION_CASE <name>: SETUP (<reason>)` and return 2; any setup leg makes the whole run
`REGRESSION: SETUP (cases=N passed=M cannot-verify=K)` with exit 2 and the scratch root kept
(`:1241-1246`).

Two probes, both in a /tmp fleet-mirror clone (lane cloned at the tip, siblings symlinked, the
lane repo never touched):

**A. sibling repo absent** (mado-shokunin omitted from the mirror):

```
REGRESSION_CASE bash-mado-verify: SETUP (revision not found: .../fleet/mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c)
REGRESSION: SETUP (cases=7 passed=6 cannot-verify=1)
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.ywlS6o (kept)
RC=2  ELAPSED_MS=118384
```

stderr carried git's own `fatal: cannot change to '.../mado-shokunin': No such file or directory`
(the `rev-parse` at `:1001` does not silence stderr); the verdict lines are clean and the run
stays fail-closed (never PASS).

**B. sibling present but its history lacks the pinned rev** (mado-shokunin replaced by a
`--depth 1` clone at `0ab1ccc`, pinned rev `eead56b` absent):

```
REGRESSION_CASE bash-mado-verify: SETUP (revision not found: .../fleet/mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c)
REGRESSION: SETUP (cases=7 passed=6 cannot-verify=1)
RC=2  ELAPSED_MS=118459
```

Both probes: the other six legs still PASS (so a missing pin is isolated to its leg and cannot
mask the rest), the run exits 2, the scratch root is kept, and no sweep is attempted for the
affected leg. This matches the documented SETUP map at `:1002` (`revision not found`), `:1006`
(`path not in revision`), `:1043` (`target missing`), `:1048` (`pin mismatch`), `:1061`
(`sweep refused`), aggregation at `:1236-1246`. Elapsed for both probes is inflated by the two
concurrent runs (~118 s each vs 115.6 s solo); others legs ran the same number of sweeps.

## 4. Hygiene / observations

- No lane writes: `git status --porcelain` after the runs is byte-identical to before (the
  pre-existing dirt — ` M .gitignore`, ` M .ufo/evidence/round-16/round-gate/runner-sha256.txt`,
  plus untracked round-15/16/17 dirs — belongs to other lanes/owners and was not touched).
- Scratch: PASS paths self-clean (`--selftest` root, `--regression` auto root). On SETUP the root
  is intentionally kept, as documented.
- On a missing sibling repo the leg emits a raw git `fatal:` line to stderr before the SETUP
  verdict; cosmetic only (exit/verdict correct), but a report-reader sees an unlabelled fatal
  line — noted, not a blocker.
- No tool installs or upgrades were made; `/usr/bin/time` is absent (used epoch-delta timing,
  no pacman transaction per the host-wide pause).

## Verdict

holds — `--selftest` exits 0 with 83/83 in 5.14 s and `--regression` exits 0 with 7/7 exact-ledger
legs (flips=0, inconclusive=0) in 115.6 s at tip 98bea7d; a missing sibling pinned rev fails
closed as `REGRESSION: SETUP (cases=7 passed=6 cannot-verify=1)` with exit 2 and the scratch kept.
