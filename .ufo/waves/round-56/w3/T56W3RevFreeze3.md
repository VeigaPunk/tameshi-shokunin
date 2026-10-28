# T56W3RevFreeze3 - FROZEN_UNCHANGED at PIN, deciding FROZEN= list, freeze amendments

Seat: T56W3RevFreeze3 (wave 3, item: freeze at PIN). Judged on: calibration. Read-only. No lane file, frozen file, or deciding invocation was touched. `deciding-run.sh` was NOT executed (its single invocation would be consumed). Scratch removed. No tools installed.

Revisions: base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; freeze `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1); PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd`. Freeze is an ancestor of PIN.

## 1. FROZEN_UNCHANGED at PIN: `1`

Command (run in the lane, `-- ` list = the 13 paths of `contract.json` `frozen_paths`, which covers every path in the assignment's list plus `freeze.json` and `contract.json`):

```
git diff --quiet 21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 2f5512a8ab0771fb2eee463ec16db359174f5edd -- <13 paths>
```

Output: empty; exit 0 => `FROZEN_UNCHANGED=1`.

Guards against a vacuous pass:
- All 13 paths exist at PIN and at the freeze commit (`git cat-file -e`, 0 missing).
- Positive control, same list, `git diff --quiet c3e2ca9f... 21eb3c63...` => exit 1, `7 files changed, 190 insertions(+), 43 deletions(-)`. The detector sees the amendment, so the empty PIN result is not a dead comparison.
- No commit in `21eb3c63..PIN` touches any frozen path (`git log --oneline 21eb3c63..PIN -- <frozen paths>` is empty).

## 2. Deciding-run `FROZEN=` list vs `freeze.json` key set: equal by mapping; literally unequal by exactly `freeze.json` itself

`deciding-run.sh` builds `FROZEN=$(python3 -c '... c["frozen_paths"] ...' "$E/contract.json")` and diffs it with `git diff --quiet $FREEZE $REV -- $FROZEN`. That list has **13** entries; `freeze.json` `files` has **12** keys. The literal set difference is `{.ufo/evidence/round-56/freeze.json}` and nothing else. This is by design: a file cannot carry its own digest, and the gate-0 key mapping (`if k != 'freeze.json'`) excludes it. So "FROZEN list == key set" holds only after that exclusion; I am reporting it as a stated design exception, not as a pass of the literal wording.

Evidence:
- Mapped comparison (13 frozen paths mapped to manifest keys, minus `freeze.json`): `mapped - keys = []`, `keys - mapped = []`. Equal.
- The deciding script's own gate-0 freeze-integrity block, extracted verbatim from `deciding-run.sh` at PIN and run read-only (only `git show` / `git rev-list`, no writes):

  ```
  python3 freeze-integrity.py <lane> 21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 .ufo/evidence/round-56
  FREEZE_INTEGRITY: OK files=12 amendments=1      (exit 0)
  ```
- Independent digest recompute of the 12 `freeze.json` entries against PIN bytes: 12/12 OK (`contract.json`, `c1/measure.py`, `c1/lost-headings-at-base.json`, `c2/measure.py`, `control/frozen-surface.paths`, `c2/red-before/round-54-surface.paths`, `c2/red-before/round-54-ctl-pos-c1.stdout.sha256`, `c2/red-before/round-54-ctl-pos-c1.stdout`, `no-harm.sh`, `deciding-run.sh`, `controls.sh`, `tools/receipt-revision-gate.py`).
- Freeze pointer check the deciding run performs: the `FREEZE` argument must be the last commit touching `freeze.json` at REV. `git log -1 --format=%H 2f5512a -- .ufo/evidence/round-56/freeze.json` = `21eb3c63...` = the freeze argument. Holds at PIN; it will keep holding as long as no later commit touches `freeze.json` (bootstrap controls commits must not).

The `FROZEN=` string the deciding run will build from PIN bytes (13 entries):
```
.ufo/evidence/round-56/contract.json .ufo/evidence/round-56/freeze.json .ufo/evidence/round-56/c1/measure.py .ufo/evidence/round-56/c1/lost-headings-at-base.json .ufo/evidence/round-56/c2/measure.py .ufo/evidence/round-56/control/frozen-surface.paths .ufo/evidence/round-56/c2/red-before/round-54-surface.paths .ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout.sha256 .ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout .ufo/evidence/round-56/no-harm.sh .ufo/evidence/round-56/deciding-run.sh .ufo/evidence/round-56/controls.sh tools/receipt-revision-gate.py
```

## 3. Freeze pointer amendments: 1 (named, reasoned, own commit) - passes the "0 or each named" rule

- `freeze.json` `amendments`: one entry, `n=1`, `prior_freeze=c3e2ca9f020776b3d66c7af854fb82c834674fcf`, `what` = six named defects with reasons (C2 arm6 index bug, `clone_rev=` relabel, sidecars, QUALITY/SKILL scoping, controls blob reads, frozen-surface completeness, red-before slice).
- Its commit: `21eb3c63` ("round-56 amendment 1 ..."), the only commit after `c3e2ca9f` that touches `freeze.json` (`rev-list --count` = 2 = `len(amendments)+1`, which is the gate-0 consistency condition). Its stat: 7 files, all on the frozen surface or the contract.
- `contract.json` `amendments` equals `freeze.json` `amendments` (checked).
- Caveat (recorded, not a failure): the amendment record has no explicit `commit` field; its commit is identified through `rev-list`, as the gate does. The `what` text's claim that "predicates, targets and denominators unchanged" was not re-verified here; that is outside this item.
- Amendment count is consistent with the frozen surface: no commit between `21eb3c63` and PIN touches it, so the freeze is not silently re-frozen.

## 4. Discrepancies found (not changed; reported to the L1)

- `contract.json` says `"attempt": 2, "l1": "TameshiR56a2"`. The assignment says attempt 3 / `TameshiR56a3`. The contract is frozen and must not be edited; the L1 should record that the attempt number in the frozen contract predates the attempt-3 relabel (the claims are the same).
- No deciding run has occurred: no `.ufo/evidence/round-56/` deciding outdir at PIN; `control/` holds only `frozen-surface.paths` (no `controls-a/b.*` committed). This matches the two-pass bootstrap expectation: the first real controls run is the bootstrap input, the second run's receipts feed the deciding run.
- Tree hygiene: `__pycache__` under `round-56` is ignored by `.gitignore:4` and not tracked (0 tracked), so it does not dirty `git status --porcelain`.

## Receipts the deciding run will reproduce

```
FREEZE_INTEGRITY: OK files=12 amendments=1
FROZEN_UNCHANGED=1 freeze=21eb3c63cd0f3190c0deeb8953c6c91c7742cd68 rev=<certified rev>   (produced by deciding-run.sh at the certified REV; equivalent check run here at PIN: empty diff, exit 0)
```

## Verdict for this item

- FROZEN_UNCHANGED at PIN: **1** (empty `git diff`, exit 0; detector verified live by positive control).
- Deciding `FROZEN=` list vs freeze key set: equal after the designed `freeze.json` self-exclusion; literal inequality is exactly `freeze.json`. Gate-0 freeze-integrity: `OK files=12 amendments=1`.
- Freeze amendments: 1, named with reason and its own commit `21eb3c63`. Within the rule.
- Open items for L1: the attempt/L1 label in the frozen contract (`a2`/`TameshiR56a2` vs the assignment's `a3`/`TameshiR56a3`); the controls bootstrap must not touch `freeze.json` or any frozen path.
