# ExecReplayAtFreeze — wave-2 falsification: independent replay of all three counters at the freeze

Seat: `L1Tameshi43.ExecReplayAtFreeze` (replay / calibration lane)
Scope: run the three counters at `--rev 3aee2c07 --freeze 3aee2c07` (NOT the records
commit `c5335c70`), paste their decisive lines + exit codes, and diff against the
committed prerun receipts under `.ufo/evidence/round-43/prerun/`.
Lane repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only; ran from a
`git clone --shared` scratch copy under `/tmp` so the pinned counter, not the
live working tree, was executed).

## Reproduce

```
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r43-w2-ExecReplayAtFreeze
cd /tmp/tameshi-r43-w2-ExecReplayAtFreeze && git checkout 3aee2c078f8976499b587086af3577fc94dc8cf1
python3 .ufo/evidence/round-43/mutants/measure.py    --lane . --rev 3aee2c07 --freeze 3aee2c07   # C1
python3 .ufo/evidence/round-43/calibration/measure.py --lane . --rev 3aee2c07 --freeze 3aee2c07  # C2
python3 .ufo/evidence/round-43/guard/measure.py      --lane . --rev 3aee2c07 --freeze 3aee2c07   # C3
```

Counters execute the checked-out rev's pinned copies; `self_pin` then equals the
contract pin. Pins verified: C1 `0d0f81bd…`, C2 `97609511…`, C3 `ae66342d…`,
tool `2e8f2e89…` (all match `contract.json` at `3aee2c07`).

## The decisive lines + exit codes (replay at `3aee2c07` / freeze `3aee2c07`)

C1 — exit `0` (PASS):
```
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1 rev=3aee2c07 freeze=3aee2c07 C1_R43_PASS=true
```

C2 — exit `1` (FAIL):
```
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 m13=0 total=8 records=4 sources_rows=114 standing=114 receipts=17 revisions=2 m13_probe=standing=7_column0=113_valid=114 rev=3aee2c07 freeze=3aee2c07 C2_R43_PASS=false first=m7:corpus/lessons/round-43.md_unknown_S160
```

C3 — exit `0` (PASS):
```
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=24 selftest_failed=0 staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 safe_floor=S256 rev=3aee2c07 freeze=3aee2c07 C3_R43_PASS=true
```

(That is three PASS-verdict lines; the fourth "decisive" datum is the aggregate:
2 of 3 claims pass at the named freeze — **C2 does not**.)

## Diff against the committed prerun receipts

The committed receipts were generated **at freeze `114ffacd` (the A6/A7 freeze)**,
printed during wave 1, and only committed later at the records commit `c5335c70`
(`git ls-tree` shows `prerun/` is empty at `114ffacd`; the files first appear at
`c5335c70`). They are therefore **stale relative to the freeze of record
`3aee2c07` (A10)**. Field-level diff (prereceipt `114ffacd` → my `3aee2c07`):

### C1 — only `rev=`/`freeze=` differ; every measurement field identical
```
identical on: self_pin tool_absent tool_sha_ok selftest_exit fixtures_pass(12/12)
run_errors live_ok(3/3) live_unflagged_v4 live_tool_errors mutants_declared
mutants_killed dead_code_only equivalent not_killed runtime_error apply_error
unresolved killed_names dead_code_names dead_code_cases dead_code_arg_ok
kill_fixture_reachable C1_R43_PASS
differs:     rev  (114ffacd → 3aee2c07)
differs:     freeze (114ffacd → 3aee2c07)
```
**Meaning:** a clean transfer. The C1 counter and the v4 tool are byte-identical
across the two revs and none of the round-42/43 *records* feed C1, so the receipt
travels unchanged. The only delta is the echoed revision — expected and benign.

### C3 — three value deltas + three fields absent in the prereceipt
```
field                  prereceipt(114ffacd)   replay(3aee2c07)     cause
selftest_cases         23                     24                   A10 added a whole-set selftest case (contract A10)
live_collisions        6                      7                    registry grew S159 at the records commit (113→114 rows; staged file unchanged)
live_held              2                      3                    same: S159 became a held document of the staged S159 row
staged_sha256          <absent>               020fbeaa…            field added post-A9 (not emitted by the A6/A7-era receipt)
naive_agree            <absent>               1                    field added post-A9
substitute             <absent>               0                    field added post-A9
rev / freeze           114ffacd               3aee2c07             the stale pin
(identical: self_pin tool_absent tool_sha_ok selftest_exit selftest_failed
 staged_rows live_collisions_agree live_held_agree live_unmapped live_cascade
 live_verdict naive_map_refused safe_map_admitted map_dedupe_live safe_floor
 C3_R43_PASS — PASS in both)
```
**Meaning:** the receipt's *result* (PASS) survives, but its *evidence* is not the
freeze's evidence — `selftest_cases`, `live_collisions`, `live_held` all moved
because the registry gained `S159` and the selftest gained a case between the
receipt's generation rev (`114ffacd`) and the freeze of record (`3aee2c07`). A
prerun is only a valid baseline for the exact rev it echoes; this one echoes the
pre-records freeze.

### C2 — there is **no** committed at-freeze prerun receipt to diff against
`prerun/` contains only `c1-…` and `c3-…`. The only C2 receipts anywhere are the
**base** runs (`before/c2-at-base.stdout` `total=2`, `before/c2-at-base-A10.stdout`
`total=3`). No C2 run at the freeze of record was ever committed as a prerun.

## Finding 1 — C2 fails at the named freeze (`total=8`, exit 1)

At `3aee2c07` the C2 counter reports `m7=5 m8=3 total=8` and prints
`C2_R43_PASS=false`. All eight hits live in records written *after* the freeze's
last base run — i.e., the C2 "after" state was never measured at any freeze:

- `m7` (5): `corpus/lessons/round-43.md` lines 75 (S160), 83 (S160–S166),
  84 & 192 (S256), 116 (S259); `LOG.md` round-43 line ~+23 (S256).
- `m8` (3): `lesson:118` `` `.ufo/waves/...` ``, `lesson:140` `` `tools/*.py` ``,
  `SCORECARD.md:2059/2060/2061` `` `.ufo/evidence/round-43/after/` ``.

What each difference *means*:

- `m8` — **one real record-agreement defect, two extractor over-matches.**
  `SCORECARD.md:2059–2061` cite `.ufo/evidence/round-43/after/` in the Evidence
  column, but `git ls-tree 3aee2c07 -- .ufo/evidence/round-43/after/` is empty —
  the records point to an evidence directory that does not exist at the rev
  (git cannot track an empty dir). That is a genuine "record disagrees with the
  tree" hit. By contrast `tools/*.py` (a glob) and `.ufo/waves/...` (an elision in
  prose) are not resolvable paths, so the extractor flags them anyway — those two
  are extractor breadth, not record error.

- `m7` — **extractor over-match on non-source S-ids.** The class sentence is
  "every S-id *cited as a source* is a mined row." The extractor flags any bare
  `S###` that isn't a registry row. `S160`/`S166`/`S256`/`S259` are cited as the
  *naive-map targets* and the *safe floor* — not as source citations — and are
  correctly not registry rows. The records are right; the counter conflates "any
  bare S-id mention" with "a source citation." The mask list (`staged:S###`,
  `Next unused id: S###`) does not cover "this S-id is an arithmetic target," so
  the counter measures a different predicate than its own class sentence. (The
  live `f551ca69`/A13 prerun still leaves `m7=1` on `lesson:116`'s `S259` — the
  safe-map target `{'S158':'S259'}` — so this over-match persists into A13.)

## Finding 2 — the freeze of record is not stable; it moved under wave 2

My assignment named `3aee2c07` as the freeze. While I worked, the lane landed
`b510ad1` (A11, 08:05), `bb36f80c` (A12, 08:07), `f551ca69` (A13, 08:09), and
`6b83a11` (A14). Each is an ancestor chain extending past my named rev. Two live
proofs of what that means:

- Running the **live working-tree** C1 counter (now the A11 bytes, `b56a34d7…`)
  against the A10 contract at `--rev/--freeze 3aee2c07` prints `self_pin=0` and
  exits 1 — the counter and its pin are no longer the same generation, so a
  "replay at the freeze" is only possible from a pinned copy, not the live tree.
- The SCORECARD round-43 block (`SCORECARD.md:2059–2061`) still prints the
  counting command as `--freeze 17f6ef0c` (the A2/A3 freeze). The contract at
  `17f6ef0c` pins the *original* counters (`ad7ecf8c`/`092c76cd`/`6278edcd`,
  tool `8140945a`), so re-running the *recorded* command from the `3aee2c07` tree
  yields `self_pin=0` on all three counters — statically, without running:
  the recorded command cannot reproduce the recorded target from the recorded
  tree. `m12` (block-round/Planned-field) does not cover the freeze field, and
  `m11` only checks that `17f6ef0c` *exists* — so this record-vs-contract
  disagreement is invisible to C2's own classes.

## Judgement

- **C1 (depth):** reproduced — `C1_R43_PASS=true`, exit 0, byte-for-byte equal on
  every field except `rev`/`freeze`.
- **C3 (operability):** reproduced — `C3_R43_PASS=true`, exit 0; the value deltas
  are a records-commit registry change and post-A9 fields, not a claim regression.
- **C2 (calibration):** **falsified at the named freeze** — `C2_R43_PASS=false`,
  exit 1, `total=8`. One of the three `m8` hits is a real record-vs-tree defect
  (empty `after/` evidence dir cited in SCORECARD); all five `m7` hits and two of
  the `m8` hits are extractor over-match (bare non-source S-ids, a glob, an
  elision). There is no committed at-freeze C2 receipt at all, and the freeze of
  record moved (A11–A14) during wave 2.
- No tools installed/upgraded; only the read-only `git`/`python3` already present.
