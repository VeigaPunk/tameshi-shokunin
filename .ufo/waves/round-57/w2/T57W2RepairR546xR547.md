# T57W2RepairR546xR547 — repair of ledger rows R54.6 and R54.7 (round 57, wave 2)

Seat T57W2RepairR546xR547, L1 TameshiR57, lane base `5e3569969b532310d2b8a3d130901757a3df356b`.
Judged on: calibration. Milestone: repair ledger rows R54.6 R54.7.

## Verdict

**Both rows are `unrepairable` under the amended C1 counter as frozen.** No admissible evidence
exists for either row. Neither row is repaired, and neither status is changed.

- `R54.6` (fixed): key-miss on the current evidence; the only tie-admissible candidate that passes the
  counter is a path-suffix match with an excerpt that carries no key (a counter loophole, see below). Not used.
- `R54.7` (fixed): fixed-not-new on the current evidence; zero tie-admissible candidates exist anywhere after
  routing.
- Status is kept. Proof that `fixed` is true for both (not a finding that changes status):
  - R54.6: `ff2a821` (ancestor of routed_at `650987a`) added `.ufo/waves/round-54/w2/T54W2Sent03.md`,
    `…/T54W2Sent03-receipts/c1committed-positive.stdout`, `…/rejection-attribution.txt`; all three are present at
    base (`receipts/base-presence.txt`).
  - R54.7: `7fa9a5e` (ancestor of `650987a`) renamed `T54W2Sent01-forged-reader.json` (`R100`) to
    `.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json`; the renamed file is present at base.
- `status_at_base` is consistent (`fixed`; both fix commits are ancestors of base).

## Why no repair is honest

The counter's `judge` (fixed branch) requires, for a keyed evidence item at path P:
1. the fix commit C is an ancestor of rev and NOT an ancestor of `routed_at`;
2. P is touched by C;
3. the tie: C's message names the item id, OR P is in the item text, OR basename(P) is a substring of the item text;
4. the excerpt is absent at `routed_at` and at C's first parent (introduced by C), and its span has no ACK word.

The only post-routing commits that record these items are the record corrections in `9cf0146`
(`SCORECARD.md` ER-R54-6 at line 2667 with `Receipts:` and `Corrected:` lines; `corpus/lessons/round-55.md`
rows 60-61). `git show --format=%B 9cf0146` does not name R54.6 or R54.7, and the paths `SCORECARD.md`,
`corpus/lessons/round-55.md` appear in neither item text. The tie (3) therefore fails for every excerpt in
`9cf0146` — this is why the EXPLAIN line for R54.7 reads `fixed-not-new`, and why R54.6's excerpt-bearing
lines cannot be credited. The wave-1 note's assumption that `9cf0146` is the credited commit cannot pass the
amended tie rule.

The commits that do introduce the item's deliverables (`ff2a821`, `7fa9a5e`) are ancestors of `routed_at`,
so rule 1 rejects them by design.

## Sweeps run (command and output)

All sweeps read git objects only. Scripts are copied to `.ufo/waves/round-57/w2/T57W2RepairR546xR547-receipts/`
(`sweep.py`, `tie.py`); outputs `key-sweep.txt` and `tie-sweep.txt` are beside them.

1. Commits naming the ids after routing (`git log --grep 'R54\.[67]' 650987a..5e35699`): **none** (empty output).
2. Commits in `650987a..5e35699` (29), each added line checked for a key token of its item, with the commit
   message checked for the id (`sweep.py`). Keys-in-added-lines exist in many paths (see `key-sweep.txt`);
   none of them is an admissible tie for R54.7, and for R54.6 only the path listed in item 3.
3. Tie-admissible candidates (`tie.py`, which applies the counter's soft-path rule, the id-in-message rule and
   the basename-in-text rule before printing):
   - `R54.6`: `18bbdab .ufo/evidence/round-56/after/clean-tree-after.txt`. Its only line at base is
     `?? .ufo/evidence/round-56/after/` (a round-56 snapshot, no key token, no R54.6 deliverable), its
     commit message does not name R54.6, so it is not evidence that THIS item is fixed.
   - `R54.7`: **no candidate** (empty output of `tie.py` for R54.7).
4. `9cf0146` non-wave files (`receipts/9cf0146-nonwave-files.txt`): 13 paths; none has a basename in the
   R54.6 or R54.7 item text.
5. `git show 650987a:SCORECARD.md | grep -c ER-R54-6` → `0`: the ER-R54-6 block is created after routing, in `9cf0146`
   (so the block itself is a valid "introduced after routing" source — the tie is the only blocker).

## Dry-run (scratch clone, `dry-c1.sh 80`, `LEDGER` = patched ledger; receipts `dry-c1-current.txt`)

The rows.json I wrote is the two current rows verbatim (see below). The patch is a no-op
(`patch-ledger.py` output `patched 2`, and `json` equality with the working tree ledger: `noop-identical: True`).
Dry-run lines:

```
EXPLAIN key-miss R54.6
EXPLAIN fixed-not-new R54.7
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=8 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=839d3f0194ab rows=51/51 agree=31/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=21 C1_R57_PASS=false
```

Both ids appear in EXPLAIN fault lines, as expected, since no honest repair exists.

## Counter finding (not a repair; for the L1)

Loophole control (`receipts/loophole-control-row.json`, `receipts/dry-c1-loophole-control.txt`): a `R54.6` row
with `commit=18bbdab…`, evidence `{path: .ufo/evidence/round-56/after/clean-tree-after.txt, lines: 1-1,
excerpt: "?? .ufo/evidence/round-56/after/"}` passes the item's check. The output is:

```
C1_R57_TERMS: fixed=34 open=15 declined=2 fixed_this_round=7 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=4 key_miss=7 fixed_bad=8 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=1 panel_over=0 base_status_bad=0
C1_R57: self=63a88c257490 rev=044f7d039e5e rows=51/51 agree=32/51 old49=ok fixed=34 declined=2 thisround=7 panel=pin spot=ok total=20 C1_R57_PASS=false
```

(the control with the full hash: `key_miss` 8→7, `agree` 31→32). The path-suffix arm of `has_key` lets a file
whose path ends with a key carry an excerpt that never mentions the item, and the tie is satisfied by
basename coincidence. I did not use this row. The L1 should decide whether the path-suffix arm should keep
admitting excerpts that do not carry the key token. I did not change the counter (not mine to change).

Second counter finding: the amended tie rule (`names_id or path/basename in item text`) cannot credit a
record-correction commit that does not name the id, for any item whose keys live in SCORECARD or lessons
files. Both rows hit it. Any fix needs a decision by the L1 (a counter amendment or a new commit that names
the id); I have not made that decision and have not invented one.

## What I did not do

- No commit, edit or git mutation in the lane or the fleet repo. Writes: this report, the `.json`, `rows.json`
  and the receipts directory under `.ufo/waves/round-57/w2/`.
- No status change. No fabricated evidence. No key weakened. No counter edited.
- No tool installed or upgraded (nothing needed; `python3` and `git` only). Scratch removed after the run.

## Artifacts

- `.ufo/waves/round-57/w2/T57W2RepairR546xR547/rows.json` — the two current rows verbatim (a no-op patch).
- `.ufo/waves/round-57/w2/T57W2RepairR546xR547.json` — machine-readable verdict.
- `.ufo/waves/round-57/w2/T57W2RepairR546xR547-receipts/` — `sweep.py`, `tie.py`, `key-sweep.txt`,
  `tie-sweep.txt`, `base-presence.txt`, `9cf0146-nonwave-files.txt`, `dry-c1-current.txt`,
  `dry-c1-loophole-control.txt`, `loophole-control-row.json`.

## Checks for the main agent

- Run `dry-c1.sh` once after the L1 has decided on the two counter questions above. Expect `R54.6` and
  `R54.7` to remain `key-miss` / `fixed-not-new` until the rule changes or a new commit naming the id exists.
