# T57W2RepairR536xR537 — ledger rows R53.6, R53.7 (round 57, wave 2, C1 calibration)

Verdict: **both rows unrepairable** under the amended C1 counter. No admissible evidence exists for either fixed row. I did not invent evidence, did not weaken a key, and did not change `status` or `status_at_base`. The rows in `rows.json` are the working-tree rows unchanged, so installing them is a no-op. Plus one finding on R53.6 (its nit is still open at REV) that the L1 must decide.

## Why no admissible evidence exists

The amended counter accepts a fixed row's keyed evidence as the fix only when the commit (a) names the item id in its message, or (b) touches an evidence path that the item's own text names (`item['path'] in text` or `basename in text`). Both routes are closed for both items.

Both fix commits are real, ancestors of the base, and not ancestors of the routed commit:

- R53.6 fix = `59c3810` ("round-54: C0 content — one scratch-root exit class across seven tools"). Its message has no `R53` reference.
- R53.7 fix = `19c7558` ("round-54: re-freeze ..."). Its message has no `R53` reference.

The text-path route is also closed:

- R53.7's item text names no lane path. Its only tokens are commit hashes (`8f474419`, `5b703c6f`, `ceb372c`), `read_rev`, `inputs pinned`. No lane path or basename is a substring of the text.
- R53.6's item text names `tools/context-capture.py` (the nit) and the tool names `bash-witness-study`, `env-diff`, `evidence-disposition`, `pin-disposition`. The four evidence paths (`tools/env-diff.py` and three others) are not named; their basenames are `env-diff.py` etc., and the text has only `env-diff`, which does not contain `env-diff.py`. So the four mapping excerpts can never satisfy the tie.

### The one candidate I considered and rejected: context-capture.py

`tools/context-capture.py` is named in the R53.6 text, and two commits after routed_at touch it: `9cf0146` (round-55 C0) and `51d1f0e` (round-55 C1). Both name no R53.6. Using either would be a tie by path, not a fix:

- `9cf0146` makes `context-capture.py` raise `ScratchRootUnusable` (a `RuntimeError` subclass) for an unusable TMPDIR. The R53.6 text itself says context-capture "maps correctly" at routed_at. The defect is the four other tools. So `9cf0146` is a uniformity refactor in a tool that was not defective. Its keyed excerpt (`A set-but-unusable TMPDIR: could-not-evaluate ...`) is new, but it does not fix the item.
- The nit the item names at `context-capture.py:27` is **not** fixed by any commit (see the finding below). So the named path's only named defect is still open at REV.

Accepting `9cf0146` would be a tie that the item does not support. Rejected.

## Finding (proved): R53.6 nit still open at REV

The R53.6 item text has a second part: `Nit: tools/context-capture.py:27 docstring still mentions the old gettempdir() path.` Command output (receipts `sweep.txt`, S5):

```
rev 2ef0a5ad4 (routed_at): / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir())), pinning literal expected ids and
rev 5e3569969 (base):      / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir())), pinning literal expected ids and
rev ca75c2674 (C0):        / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir())), pinning literal expected ids and
C0 touches context-capture: (C0 diff-tree has no tools/context-capture.py; latest toucher is 51d1f0e)
```

So the nit is still open at REV. The row's `fixed` status is correct for the mapping defect (the four tools; S6 shows `ScratchRootUnusable` in all four at base, and the note's rc claims were not re-run here). But the row's status "fixed" for the whole item overstates it, since the nit is part of the item. I did not change `status` (the mapping is fixed and the change is a finding for the L1, not a repair). Options for the L1: (a) keep `fixed` and record in the note that the nit is open at REV; (b) fix the nit in round-57 content (out of this seat's scope); (c) downgrade to a partial status, which needs a status change and `status_at_base` change, and is therefore the L1's call.

## Dry-run lines (scratch dry run, patched ledger = working tree rows)

Command: `python3 .ufo/waves/round-57/patch-ledger.py corpus/routed-defects.json .ufo/waves/round-57/w2/T57W2RepairR536xR537/rows.json $S/ledger.json` → `patched 2`; `cmp` against the working tree → IDENTICAL-LEDGER.

Command: `LEDGER=$S/ledger.json bash .ufo/waves/round-57/dry-c1.sh 80`, full output in `T57W2RepairR536xR537-receipts/dry-c1-R536-R537.txt`:

```
EXPLAIN fixed-not-new R53.6
EXPLAIN fixed-not-new R53.7
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=6c34bacacd71 rows=51/51 agree=31/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

Both ids still appear as fault lines (`fixed-not-new`), so the rows do not pass. This is the expected outcome for an unrepairable row. The `rev=` differs from the earlier wave run (629cbec9 vs 6c34bac) because `dry-c1.sh` snapshots the working tree into a new scratch commit; the tallies are identical.

## Sweep (command + output in receipts `sweep.txt`)

- S1: `git log --all -E -i --grep='R53\.[67]|53\.[67]\b'` → no commit names R53.6 or R53.7 (empty).
- S2: fix commits `59c3810` and `19c7558`: body contains no `R53`, both ancestors of base, neither ancestor of routed_at `2ef0a5a`.
- S3: lane paths that are substrings of the item text (path or basename) at base: R53.6 → four paths, of which only `tools/context-capture.py` has commits after routed_at (`51d1f0e`, `9cf0146`); R53.7 → none.
- S4: commits after routed_at touching each R53.6/R53.7 evidence path: `tools/env-diff.py` (99c3bc8, 59c3810), `tools/bash-witness-study.py` / `evidence-disposition.py` / `pin-disposition.py` (59c3810), `.ufo/evidence/round-54/integrate/binder.py` (7fa9a5e, 077d431, 19c7558). None of these names R53.6/R53.7, and none is a path named by the item text.
- S5: nit at context-capture.py:27 is unchanged at routed_at, base, and C0 (see the finding above).
- S6: the four tools at base contain `ScratchRootUnusable` (3–4 refs each), so the mapping defect is fixed in substance. This supports the status "fixed" for the mapping. It is not a tie.

## Evidence the rows stay as they are

- status `fixed` and status_at_base `fixed` are unchanged. I found no command that proves the mapping defect unfixed (S6). The nit finding is flagged above for the L1.
- `rows.json` (`T57W2RepairR536xR537/rows.json`): the two working-tree rows, full fields (`id`, `status`, `evidence`, `commit`, `seat`, `note`, `status_at_base`), byte-equal to the ledger. Installing it changes nothing.

## Tools installed

None. Only `git`, `python3`, `grep`, `sed`, and `cmp` were used.

## Out of scope / not done

- No lane file edited; no commit; no fleet-root file touched.
- The four tools' rc=2 claim (note of R53.6) was not re-run at base; S6 checks the mapping code only. Nothing in this report depends on that rerun.
- The `R53.9` / `R54.8` / `R55.4` / `R55.6` soft-excluded-path lines and the other key-miss / fixed-not-new lines are outside this item and are not analysed here.

## For the L1

1. R53.6 and R53.7 are unrepairable as the counter stands. The fix commits do not name the ids, and the item texts name no evidence path. Re-binding them needs one of: a commit that names the id (not possible without rewriting history), a counter amendment (a decision for you, not a repair), or a documented exception.
2. R53.6 nit (context-capture.py:27 still says gettempdir()) is open at REV. Decide whether the row keeps `fixed` with a note or is narrowed.
