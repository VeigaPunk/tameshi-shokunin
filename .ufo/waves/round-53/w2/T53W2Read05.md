# T53W2Read05 — wave-2 re-read of `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`

- Candidate content commit: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C\*\*, fix pass 2).
- Lane repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- Source read via git objects only: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md` (working tree never read for section bytes; no git/jj mutation anywhere).
- C\*\* `SKILL.md`: 2 189 lines (`wc -l`), blob sha256 `4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d`.
- Section: **start 924, end 937** per the monitor's own splitter; body = lines 924–936 (13 lines), next heading line 938 (`### Using the ledger`), trailing whitespace-only lines stripped, no trailing newline.
- `section_sha256` = `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993`.
- Findings: **0** (the wave-1 finding is fixed in the C\*\* bytes; no other statement in the section fails at C\*\*).

## Split and hash verification (before hashing)

Two independent implementations plus the frozen monitor's own code agree:

1. Scratch splitter (my `split.py`, `^#{1,3}(\s|$)` outside triple-backtick fences, strip trailing whitespace-only lines, join `\n`, no trailing newline, sha256 over UTF-8/surrogateescape): start 924, end 936, 13 lines, sha256 `430dd86f…b993`.
2. Independent second pass: 1-based 924 to 936, next heading at 938, 13 lines, 1 096 chars, no trailing newline; first bytes `## The leg ledger — replay, receipt, and`, last bytes `in their own notes, not as ledger rows).`; same sha256.
3. **The monitor itself**: I copied `.ufo/evidence/round-18/measure.py` (the frozen implementation `measure.py` at round 21 imports) into scratch and called its `sectionize(raw)` on the C\*\* blob with `sys.dont_write_bytecode = True`. Result: **64 sections** (preamble + 63 headings — matching contract C1's "64 of 64"), and for this heading `{'start': 924, 'end': 937, 'heading': '## The leg ledger — replay, receipt, and how it is read (round 7, measured)', 'sha256': '430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993'}`. Hash identical to my split.
4. Fence parity before the heading: 12 fence-delimiter lines before line 924 (even ⇒ heading is outside a fence), 20 fences total in the file. The heading string occurs exactly once in the file.

## Fix verification FIRST (the item's named fix)

The item's parenthetical: "ledger row count corrected (eight rows; ninth/tenth in case notes)".

1. **The fix is in the C\*\* bytes.** `git diff a41195dfc13a73958e4c5228ec196b28d03ded03 5b703c6 -- SKILL.md` shows exactly this replacement at the section's last paragraph:
   - C\*: `(ten measured rows: six in the §1/ER-2 table plus the round-16/18/26/51 appends)` (C\* line 933; verified present once at C\* and absent at C\*\*).
   - C\*\*: `(eight ledger rows — six in the §1/ER-2 table plus the round-16 and round-18 appends; the ninth and tenth cases, cite-check and drift-pins, are recorded in their own notes, not as ledger rows)` (C\*\* line 936; present once in the section).
   - No other "measured rows" phrasing remains in the section (`sed -n '924,936p' | grep -n 'measured rows'` → none).
2. **The corrected count is true at C\*\*.** `corpus/knowledge/fleet-kill-rate-ledger.md` is **byte-identical between C\* and C\*\*** (`git diff --stat a41195d 5b703c6 -- corpus/knowledge/fleet-kill-rate-ledger.md` → empty output). Measured rows at C\*\*:
   - §1 table, lines 45–48: `| 1 |` … `| 4 |` — four rows.
   - ER-2 table, lines 276–277 — two rows (4 + 2 = the "six in the §1/ER-2 table"), opening cells quoted verbatim:

     ```
     | 5 | kagi · `corpus/checklist-run.sh` | 34 cases |
     | 6 | kumitate · `scripts/claims-check.mjs` | 39 checks |
     ```
   - `## Round 16 — seventh row appended (2026-10-20)` (line 403; one row at line 410) and `## Round 18 — eighth row appended (2026-10-20)` (line 424; one row at line 432).
   - Total **8**, and the file's own row numbering tops at "eighth".
   - Heading inventory (`grep -n '^#\{1,3\} '`): 15 headings, lines 1, 21, 41, 90, 98, 132, 160, 178, 200, 216, 239, 366, 403, 424, 439. There is **no** round-26 and **no** round-51 row-append block; line 439 is `## Round 52 — §3 drift-pins cell superseded (2026-10-27)`, a **cell** supersession ("cell, not edit … §3's table stays as written"), not a row.
3. **The ninth and tenth cases are in their own notes, not ledger rows.**
   - `git cat-file -e 5b703c6:corpus/knowledge/mutation-case-kumitate-cite-check.md` → present; header `` # Mutation case 9 — kumitate `scripts/cite-check.mjs` (round 26) ``; measured result header `## 2. Result — 5/10 killed (50 %), 10/10 verdict predictions held` with a full 10-row table.
   - `git cat-file -e 5b703c6:corpus/knowledge/mutation-case-kagi-drift-pins.md` → present; header `` # Mutation case 10 — kagi `corpus/drift-pins.sh` (round 51) ``; measured result header `## 2. Result — 2/10 killed (20 %), 7/10 verdict predictions held` with a full 10-row table.
   - Neither case has a numbered measured row in the ledger (row numbering stops at 8; the only case-10 trace in the ledger is the round-52 bullet, which is a static cell supersession, not a row).
4. **Fix verdict: VERIFIED.** The sentence at C\*\* states the count the ledger actually carries and routes the two later cases to the notes that record them. Nothing in the fix overstates or understates what the ledger holds at C\*\*.

## Checks run (commands → outcomes)

1. `git cat-file -t 9f1d3c3` / `git cat-file -t 4b7c682` → `commit` / `commit` (both anchors resolve at C\*\*).
2. `git show 9f1d3c3:tools/mutate-and-run.sh | sed -n '72p;108p;109p'` → line 72 `# --regression (r4-2; r7-1 leg ledger) — the fleet's recorded mutation cases,`, line 108 `# --target/--defects/--suite/--label are refused (usage error).`, line 109 `#`. Lines 75–78 carry the four leg names with their rates (`8/10 (80 %)`, `8/10 (80 %)`, `6/10 (60 %)`, `4/10 (40 %)`) — i.e. the quoted content resolves inside the cited `:72-109`.
3. `git show 9f1d3c3:tools/mutate-and-run.sh | sed -n '500,530p'` → 511 `PIN_JS=…`, 512 `REV_JS=…`, 513/514 `PIN_BASH/REV_BASH`, 515/516 `PIN_TSUKUROI/REV_TSUKUROI`, 517/518 `PIN_MADO/REV_MADO`, 519–522 `TABLE_JS/TABLE_BASH/TABLE_TSUKUROI/TABLE_MADO`. `:511-522` lands on pins + recorded verdict tables.
4. `git show 4b7c682:tools/mutate-and-run.sh | sed -n '590,625p'` → 597 `PIN_JS` … 604 `REV_MADO`, 605–612 `PIN_CHECKLIST` … `REV_SOURCESCHECK`, 613–620 `TABLE_JS` … `TABLE_SOURCESCHECK`. `:597-620` lands on the recorded tables (eight legs at round 18); `grep -c 'regression_case_git \(js\|bash\)-'` at `4b7c682` → `8`.
5. `git log -1 --format='%H %s' 4b7c682` → `4b7c6823a462f5ea2eafcb262275300a545f3ed7 round-18: …` (the round-18 runner the section names).
6. `git show 9f1d3c3^:tools/mutate-and-run.sh | grep -c 'regression_case_git \(js\|bash\)-'` → `0`; the same blob reads `# --regression (r4-2) — this tool's own gate: re-runs BOTH worked cases.` and `--regression re-runs both worked cases (JS round 2, bash round 3)` — so the pre-round-7 `--regression` really was the two-case self-check.
7. `git show 9f1d3c3:tools/mutate-and-run.sh | grep -n 'regression_case_git \(js\|bash\)-'` → exactly four fleet legs (927 `js-kimi-census`, 932 `bash-surface-census`, 937 `bash-tsukuroi-census`, 942 `bash-mado-verify`); plus fixture selftest legs. "Round 7 recorded four legs at r7-1" holds.
8. Rates vs the section: runner comment at 9f1d3c3 (`8/10 (80 %)`, `8/10 (80 %)`, `6/10 (60 %)`, `4/10 (40 %)`) and ledger rows 45–48 (`**8/10 (80 %)**`, `**8/10 (80 %)**`, `**6/10 (60 %)**`, `**4/10 (40 %)**`) match the section's four legs; `TABLE_MADO` has 10 entries with 4 KILLED (40 %), `TABLE_TSUKUROI` 10 entries with 6 KILLED (60 %).
9. Ten legs at C\*\*: `grep -n 'regression_case_git'` → 1459 `js-kimi-census`, 1464 `bash-surface-census`, 1469 `bash-tsukuroi-census`, 1474 `bash-mado-verify`, 1479 `bash-checklist-run`, 1484 `js-claims-check`, 1489 `js-round-gate`, 1494 `js-sources-check`, 1499 `js-cite-check`, 1504 `bash-drift-pins`; pins/tables for legs 9/10 at 630–633 and 642–643; round provenance comment at 2013: `r16 adds leg 7, r18 leg 8, r26 leg 9 and r51 leg 10`. The ten `corpus/knowledge/mutation-case-*.md` notes at C\*\* map one-to-one onto the ten legs (checked by subject), so "every recorded mutation case is a leg of this ledger" holds.
10. "replayed at its pinned original revision": each leg is dispatched as `regression_case_git <repo path> <PIN_*> <REV_*>` with git-object materialization (`FLEET_ROOT=''   # set by run_regression; regression_case_git resolves repos from it`; leg 9/10 dispatch lines 1499–1508). Holds.
11. Receipt claim: `git grep -l 'fleet-kill-rate-ledger' 5b703c6 -- corpus/knowledge` → nine docs (closeout-r11, incremental-pin-disposition, mutation-case-kagi-checklist, mutation-case-kagi-drift-pins, mutation-case-kumitate-cite-check, mutation-case-kumitate-claims, operator-runbook, service-limits, service-standing-state). "The ledger is the receipt tameshi's records cite for kill-rate claims" holds.
12. Scratch-directive scan of the section: `grep -n '/tmp\|HYAKU_SCRATCH\|50 MB' section.txt` → none; the section carries no scratch directive to violate.

## Holds

- Heading text, section boundary (924–936, next heading 938), and `section_sha256` `430dd86f…b993` (three-way verified, monitor code included).
- The fixed ledger sentence: eight rows = 4 (§1) + 2 (ER-2) + 1 (round 16) + 1 (round 18); cases 9/10 recorded in `mutation-case-kumitate-cite-check.md` / `mutation-case-kagi-drift-pins.md`, not as ledger rows.
- `tools/mutate-and-run.sh@9f1d3c3:72-109` and `:511-522` land on the recorded rates and the pins/tables (checks 2–3).
- `4b7c682:597-620` lands on the round-18 recorded tables (check 4).
- Round 7 recorded four legs at r7-1 with the four rates the section lists; the pre-round-7 `--regression` was the two-case self-check (checks 6–8).
- Every recorded mutation case (ten notes) is a runner leg replayed from git objects at its pinned revision (checks 9–10).
- The ledger exists at C\*\* and is cited by nine knowledge records (check 11).
- The dated-milestone parenthetical is explicitly dated history and is also independently true: the runner comment at C\*\* line 2013 says `r16 adds leg 7, r18 leg 8, r26 leg 9 and r51 leg 10`, and the notes are numbered 7/8/9/10 accordingly. Section lines 5–6, line break reproduced (byte-exact fragment):

```
seven from round 16, eight from round 18, nine from
round 26, ten from round 51
```

## Findings

**None.** No statement in the section fails at C\*\*.

## Considered and rejected (calibration notes, not findings)

- Ledger §3 `cite-check` cell (`:107`) still reads `**probe only, 1/4** (§2); full sweep open`, although case 9 was swept at round 26 (5/10) and is replayed as leg 9. This is a ledger-cell staleness, not a failure of this section's sentence: the fixed text explicitly says cases 9 and 10 are recorded in their own notes, not as ledger rows, so the section no longer presents the ledger as the receipt for those two cases. The cite-check note itself discloses the stale cell: its §3 says the standing ledger still lists cite-check as a four-defect probe (1/4) and a queue row, and that this case is that full sweep. No section statement is contradicted.
- **The round-52 block states case 10's rate (20 %) inside the ledger.** The section says the tenth case is recorded "not as ledger rows" — a supersession bullet is not a row, and the block itself says "That case 10 measurement supersedes the cell; §3's table stays as written". The wording is precise; rejected as a finding.
- **"six in the §1/ER-2 table"** compresses two table locations (§1 rows 1–4, ER-2 rows 5–6) into one slashed reference. Numerically exact (6), and the appended rows are in ER-2 as the ledger says ("§1's table is not edited; these rows are the append"). Style only; rejected.
- **§4/§5 tables carry numbered rows 1–6** (identity/currentness readings at lines 299–304, 326–331) but no kill-rate cells; they are not "ledger rows" in the section's measured-row sense (the sentence accounts for its eight explicitly). Rejected.

## Scratch, tooling, write scope

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read05/` (created with `mkdir -p`; held `SKILL_Cstarstar.md`, `SKILL_Cstar.md`, `ledger.md`, `note9.md`, `note10.md`, `section.txt`, `split.py`, `monitor_measure.py`; all well under 50 MB). Removed with `rm -rf` before yield.
- Tooling installed/upgraded: **none** (system `git`, `python3`, `grep`, `sed`, `wc`, `sha256sum` sufficed). No pacman transaction attempted.
- No git/jj mutating command was run anywhere; every git call was `show`/`cat-file`/`log`/`grep`/`diff --stat` against the lane repo. The monitor module was imported from scratch with `sys.dont_write_bytecode = True` (no `__pycache__` written into `.ufo/evidence/`).
- Write scope respected: only `.ufo/waves/round-53/w2/T53W2Read05.json` and `.ufo/waves/round-53/w2/T53W2Read05.md` in the lane.
