# T57W2RepairR511xR513 — repair of ledger rows R51.1 and R51.3 (round 57, wave 2, C1)

## Verdict

Neither row can be repaired with honest, counter-admissible evidence under the amended C1 counter.
Both rows are left unchanged. `rows.json` holds the two current rows verbatim, so the patched ledger
equals the working tree (`PATCH_IDENTITY` ok). No status changed. The dry run still prints one
EXPLAIN fault line for each id.

| id | status (kept) | fault at dry run | honest evidence? | why |
|---|---|---|---|---|
| R51.1 | fixed | key-miss | no | The fix commit `bcba892` changed the registry row in compact JSON. The lane's registry was reformatted by `9cf0146` (round-55). No keyed excerpt is both in `bcba892` and at REV and absent at `bcba892^`. |
| R51.3 | fixed | fixed-not-new | no | The fix commit `bcba892` appends the 20 correction records (the item's first remedy) and is true. The tie rule refuses it: its message does not name R51.3, and `.ufo/evidence/round-21/coldread/ledger.json` is named neither by the item text nor by basename. The only tie-admissible commit (`f1a3246`) does not fix the item (see R51.3 below). |

Status is not proven wrong for either row. The status findings are in "Findings for L1" below.

## Dry runs (verbatim)

Unchanged rows (`rows.json` = current rows), `LEDGER=$S/ledger.json bash .ufo/waves/round-57/dry-c1.sh 80`:

```
EXPLAIN key-miss R51.1
EXPLAIN fixed-not-new R51.3
... (other ids, unchanged from the L1 dry run: key-miss R51.6, R52.1, R52.2, R52.6, fixed-not-new R53.6/R53.7, ...)
EXPLAIN panel-pin .ufo/evidence/round-57/c1/panel.json
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=241d82c10a66 rows=51/51 agree=31/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

Full output: `w2/T57W2RepairR511xR513-receipts/dry-c1-patched.txt`. `patch-ledger.py` printed `patched 2`.

Scratch-only experiments (NOT in `rows.json`, NOT committed; they show what the counter would accept):

- R51.1 with a counterfeit excerpt (REV lines 1251-1266, absent at `1f72d7d`, not in `bcba892`): R51.1 leaves the EXPLAIN list, `agree=32/51 total=20`. See Finding F1. File: `receipts/counter-gap-R51.1-scratch.txt`.
- R51.3 with `f1a3246` (`.ufo/evidence/round-52/coldread/refresh.py:216`): R51.3 leaves the EXPLAIN list, `agree=32/51 total=20`. Refused, see below. File: `receipts/f1a3246-candidate-R51.3-scratch.txt`.

## R51.1 — registry gate (keys: `mte-interop-check`, `ten-leg`, `registry-check --only mte-interop-check`)

Current evidence: `tools/registry.json:1266` and `tools/mte-interop.py:343`. Neither excerpt contains a key, so `key-miss`.

Sweeps run:

1. `git show bcba892:tools/registry.json` vs `1f72d7d` (parent): the row changed only `legs_conforming=9/9` to `10/10` (line 1014) and the `source` line. The name line `"name": "mte-interop-check",` (line 1011) is in both, so it fails the fresh arm.
2. `git log -G'mte-interop-check|ten-leg|legs_conforming' -- tools/registry.json`: `bcba892`, `9cf0146` (round-55 full reformat of registry.json, 1028 to 1277 lines, indent-expanded arrays), `a08e85c`, `2b064cf`.
3. Keyed-excerpt sweep (`receipts/sweep-rev-keyed-excerpts.py`): every window of at most 30 lines of REV's `tools/registry.json` that holds a key, every substring of 15-400 normalised chars containing a key, tested for presence in `bcba892` and absence at `1f72d7d`. Output: `REV key lines scanned; candidate (in bcba892, absent at parent, keyed) hits: 0`.
4. `grep -n 'ten-leg'` over the lane: no lane file that `bcba892` touches carries the key, except as a tie-less path (`SKILL.md`, `round21-measure.py`, not named by the item text). `bcba892` does not name R51.1 in its message.
5. The only counter-admissible keyed excerpt I found is the REV span 1251-1266 (249 chars, name line through `"MTE_INTEROP: PASS legs_conforming=10/10"`). It is absent at `1f72d7d`, so the fresh arm accepts it. But it is not in `bcba892` (`present_in_bcba892 False`). Citing `bcba892` with it would be a false provenance claim (F1). Refused.

Truth check (status not changed):

- Live-fleet check, same command the row runs, with the fleet root passed explicitly: `python3 <clone>/tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` at `master` (`06e9849`). Output: `MTE_INTEROP: PASS legs_conforming=10/10`, rc 0, 287.9 s. Receipt: `receipts/mte-interop-check-live-fleet.*`.
- `python3 tools/registry-check.py --root <clone> --rev master --only mte-interop-check --json` gave `ROW mte-interop-check expect=0 got=2 differs`, `REGISTRY_CHECK: held=0/1`, stdout `MTE_INTEROP: SETUP (regression exit 2)`. Receipt: `receipts/registry-check-rev-master.*`. Under `--rev` the row's default fleet root is the parent of the mirror, which holds no sibling repos [INFERENCE: the regression needs the siblings; not separately verified]. The row does not hold under `--rev`, but the tool output itself is correct at the live fleet root.
- No committed receipt exists. `git grep -n 'registry-check --only' master` returns only pre-fix or unrelated text, and no committed `mte-interop-check` result after `bcba892` reports held. The item's acceptance ("green at the fix revision with a committed receipt") is not met by any lane file (F3).

Decision: R51.1 stays `fixed` (not proven wrong), `unrepairable` under the counter.

## R51.3 — cold-read re-key overstates (keys: `wrong_expectations`, `coldread/refresh.py`, `T51W2Read20`, `correction`)

Current evidence: `.ufo/evidence/round-21/coldread/ledger.json:112211` and `:112193` (keyed, resolve), and `.ufo/evidence/round-52/coldread/refresh.py:216` (keyed). The fault is `fixed-not-new`: no keyed item is both in a path `bcba892` touches and tied to the item.

Sweeps run:

1. `git log --grep='R51\.3'` over all refs: no commit names R51.3. `git log $routed..master --grep='R51\.1' --grep='R51\.3'`: none.
2. `bcba892` touches `.ufo/evidence/round-21/coldread/ledger.json`. The item text names neither that path nor its basename `ledger.json` (it says "the round-21 ledger"). Tie fails.
3. Counts of the wrong record: `git show <rev>:.ufo/evidence/round-21/coldread/ledger.json | grep -c 'wrong_expectations 0 was written from code (round-51 refresh.py:227)'`: parent `1f72d7d` = 0, `bcba892` = 20, `master` = 20. So the correction is real and introduced by `bcba892` (true fix).
4. `git log -- '*refresh.py'` after routed: `f1a3246` (`.ufo/evidence/round-52/coldread/refresh.py`, line 216 `'wrong_expectations': len(reader['findings'])`, absent at `f1a3246^`) and `0de8515`/waves path (soft, not tied). `f1a3246` is an ancestor of base and not of `ef19d8e`. It passes the counter (receipt `f1a3246-candidate-R51.3-scratch.txt`).
5. Refused `f1a3246` as the fix: it adds a wave-3 re-key instrument that computes the count from findings. It appends no correction and corrects no record. The item's requested remedy is "append a named correction ... or supersede those entries". The 20 zero entries in the round-21 ledger still stand at `f1a3246`; only `bcba892` corrects them. Citing `f1a3246` would make the counter pass for a commit that does not do what the item asks.

Truth check: the item's remedy is done in `bcba892` (20 correction records, all naming `round-51 refresh.py:227`). Status `fixed` is true. Not proven wrong.

Decision: R51.3 stays `fixed`, `unrepairable` under the counter as amended.

## Findings for L1

- F1 (counter gap, measure.py `judge`, fixed arm): the fresh arm checks an excerpt is absent at `commit^` (`prev`), but never that the excerpt is present at `commit` (`git show <commit>:<path>`). A REV-only excerpt passes for any commit that touches the path and whose parent lacks the text. Demonstrated in scratch: R51.1 with REV lines 1251-1266 (not in `bcba892`) drops out of the EXPLAIN list (`agree=32/51`). Recommend: require `norm(excerpt) in norm(show(commit, path))` in the fresh arm. Not committed; the counter is not edited by this seat.
- F2 (R51.3 tie): the counter's tie rule refuses the true fix (`bcba892`) because the commit message does not name R51.3 and the item text names neither the ledger path nor its basename. Remedy options for L1: (a) a lane content commit whose message names R51.3 and carries the correction (new content, outside this seat); or (b) accept that the item text describes the ledger ("the round-21 ledger") and say so in the amendment record. Option (c), citing `f1a3246`, is refused as not a fix (above).
- F3 (R51.1 acceptance): the item asks for `registry-check --only mte-interop-check` green at the fix revision with a committed receipt. No committed receipt exists. Live-fleet output is PASS 10/10 (rc 0). `registry-check --rev` reports the row as `differs` (SETUP) in a mirror. This is an operability question for C2 (the row depends on the checkout's parent directory holding the sibling repos), not a calibration fact. Status `fixed` is kept.
- F4: the L1's `panel-pin` line (`PANEL_SHA256` still `PIN_PENDING`) is unrelated to these rows; it remains in the dry run.

## Commands (all run; outputs in receipts)

- `git clone --shared <lane> $S/clone`; `git -C $S/clone checkout --detach` failed on the dry-run rev (`629cbec`, scratch commit, not in the lane). Used `master` (`06e9849`) for lane reads; the lane's `git show` content for paths I cite is unchanged at REV.
- `git -C $C log/show/grep` over `bcba892`, `1f72d7d`, `ef19d8e`, `f1a3246`, `9cf0146`, `master`.
- `python3 patch-ledger.py ... rows.json $S/ledger.json` then `cmp` (identity) and `LEDGER=... dry-c1.sh 80`.
- `python3 $S/sweep51_1.py $C` (0 hits).
- `TMPDIR=... python3 $C/tools/registry-check.py --root $C --rev master --only mte-interop-check --json` (exit 1, held 0/1).
- `TMPDIR=... python3 $C/tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` (rc 0, PASS 10/10).

Tools: none installed or upgraded. Existing `uv 0.13.0` (`~/.local/bin/uv`) and `/usr/bin/python3` were used as-is. No pacman, no git mutation in the lane or fleet repo, no lane file edited.

## Outputs

- `w2/T57W2RepairR511xR513/rows.json`: the two current rows, unchanged.
- `w2/T57W2RepairR511xR513.json`: machine-readable verdicts.
- `w2/T57W2RepairR511xR513-receipts/`: dry run, counter-gap and f1a3246 scratch runs, registry-check and mte-interop outputs, sweep script.
