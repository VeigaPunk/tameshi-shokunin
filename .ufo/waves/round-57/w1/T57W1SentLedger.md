# T57W1SentLedger: forging the round-50 ledger rules

Seat: T57W1SentLedger (leaf; no dispatch). Item: attack the round-50 ledger rules that the successor C1 counter inherits. Base `5e3569969b532310d2b8a3d130901757a3df356b`. Machine-readable output: `T57W1SentLedger.json`. Receipts: `T57W1SentLedger-receipts/`.

## Verdict

- The inherited rules accept forged ledgers. Three fixed-row forgeries pass (off-topic prose line, off-topic code line, comment line), and four more pass (SHONEN restatement, one commit, four rows). A ledger with 20 real fixed rows and 29 rows flipped to `open` (all named in one planned paragraph) gets `total=0 C1_R50_PASS=true` from the real round-50 CLI.
- The harness can fail: four controls are refused for the expected reasons.
- No cheap mechanical check blocks every forgery class without harming genuine fixes. Measured on the 31 real fixed rows: word-overlap ≥3 (X1) is the best single check (1 false reject, R49.1, catches 3 of 4 forged classes); X1 plus a key-length check (X9) catches all four classes at 4 false rejects.
- The base ledger is not a pass under the round-50 counter itself: `total=9 C1_R50_PASS=false` (below).

## What was run

Scratch clone `git clone --shared` of the lane, detached at base. Only the clone was written to (fixture identity `fixture@example.invalid`, toplevel asserted each run). The lane and the fleet repo were not mutated.

1. Base: `measure.py --lane CL --rev BASE --explain` → `total=9 C1_R50_PASS=false` (`evidence_bad=3` R41.6 fixed, R42.3 declined, R49.3 open; `open_unplanned=6` R45.1, R45.4, R46.2, R47.5, R48.4, R49.5). Receipt: `base-round50-explain.stdout`.
2. Round-50 selftest at base: `C1_R50_SELFTEST: cases=25 failed=0`. Receipt: `round50-selftest.stdout`.
3. `forge.py` builds four appended-only commits on base (K1 `corpus/QUALITY.md`, K2 `tools/staged-id-guard.py`, K3 `tools/pbt-staged-id.py`, K4 `SHONEN.md`) and a fifth (K5) that appends a `**Planned (round 51):**` paragraph naming all 49 ids to `SCORECARD.md`. Each forged row is probed by writing the 49-row ledger with one row replaced, committing on top, and calling the inherited `measure()`; pass means no `explain` note names that id. Output: `out.json`.
4. `step2.py`: X1 threshold sweep, X6, X5 defeat search. Output: `out2.json`.
5. `step3.py`: X9 and X1∧X9. Output: `out3.json`.
6. Real CLI on the full forged ledger commit: `C1_R50: ... fixed=20 open=29 declined=0 ... total=0 C1_R50_PASS=true`. Receipt: `full-forgery-round50-cli.stdout`.

Harness sha256 (round-50 measure.py, bytes unchanged): `ceee320c9ad84c89a7846fd746a072a60758a465d25ff80343fb95e0bd88ae29` (`round50-measure.sha256`).

## Forgeries (fixed rows, rules as inherited)

| id | forged row | what makes it new and keyed | passes? |
|---|---|---|---|
| F1 | R41.1 fixed, commit K1 touches `corpus/QUALITY.md` | appended prose line "Index note: the line-scoped digest was regenerated…", key `line-scoped`, commit message names no item | **PASS** |
| F2 | R43.3 fixed, commit K2 | appended code `SHADOW_NOTE = "anchor digest rebuilt nightly"`, key `anchor` | **PASS** |
| F3 | R49.1 fixed, commit K3 | comment line `# pbt-staged-id.py: header comment reflowed; behaviour unchanged`, key is the file name | **PASS** |
| F4 | R46.5, R47.7, R48.6, R49.6 fixed, commit K4 (one commit) | appended `- [~] box five: unchanged this round, operator-owned`, keys `SHONEN`/`[~]`; restates the defect | **PASS ×4** |

Every probe's per-id notes are empty. Other notes present (`evidence_bad=3`, `open_unplanned=6`) are the base's pre-existing ones.

Controls, all refused for the expected reason: C-a existing line not new (`excerpt-not-in-lines` at base line), C-b excerpt absent (`excerpt-not-in-lines`), C-c commit does not touch the evidence path (`fixed-not-new`), C-d open without a planned paragraph (`open-unplanned`).

## Disposition-space forgeries (open, declined)

- **Open, planned-names-everything (item 2).** With K5 at REV, flipping each row individually to `open` (real evidence) is accepted for 46 of 49. The three refusals are the pre-existing bad evidence (R41.6, R42.3, R49.3). Flipping fixed rows to open is accepted too; R41.1 (which the lane's own ledger records as fixed by `322b5cd3`) is accepted as open.
- **Full forged ledger.** 20 fixed (the 9 this-round fixes plus 11 others, all with resolving evidence) and 29 open (evidence substituted for R41.6, R42.3, R49.3 by a keyed grep). `total=0`, `C1_R50_PASS=true` from the real CLI. The fixed floor (20) and the declined cap (12) are the only bounds on this space. `open` has none.
- **Declined.** A 57-character reason passes per item for 46 of 49 (same three evidence refusals). The cap of 12 is the only bound.

## Candidate extra checks, measured

Each check runs on the 31 real fixed rows (evidence at base) and on the forged rows (evidence at K4). "fresh" is the round-50 fixed-branch logic. Counts are false rejects of genuine fixes unless noted.

| check | false rejects on 31 real fixed | forged classes caught | notes |
|---|---|---|---|
| X1: fresh keyed excerpt shares ≥3 content words with item `text` | **1** (R49.1, overlap 1) | F1, F2, F3 | misses F4 (overlap 3) |
| X1 at ≥2 | 1 (R49.1) | F3 only | F1 and F2 have overlap 2 and pass; F4 has overlap 3 and passes |
| X1 at ≥4 | 7 | all | too strict |
| X2: commit message names item id or key | 20 | F1, F2, F3 | reject; accepts F4 (the K4 message names `SHONEN`) |
| X2d: diff added lines mention a key | 0 | 0 | vacuous: keyed excerpt is itself an added keyed line |
| X3: fixed commit removes a keyed line | 29 | — | reject: the lane is append-only, fixes are appends |
| X4: excerpt is not a comment-only line in a code file | **0** | F3 | cheap, free, but X1 also catches F3 |
| X6: no backticked span of item text in excerpt | 15 | F2, F4 ×4 | reject |
| X9: fresh excerpt contains a key of length ≥6 | 4 (R43.1, R46.1, R47.6, R49.1) | F4 ×4 | misses F1–F3 |
| X1 ∧ X9 | 4 (R43.1, R46.1, R47.6, R49.1) | F1–F4, all | blocks everything tested |
| X5: open row, some excerpt already present at routed_at | 0 of 7 real open rows | rejects 9 of 11 fixed→open flips | defeated: one `git grep` at routed_at finds a line still present at REV for 8 of the 9 (e.g. R46.1: `.ufo/evidence/kaika-round-1/sources-opened.tsv` line 27) |

X5 costs nothing on fixed rows (it applies only to open rows).

## Recommendation for the successor C1 counter

1. Add X4 (comment-only excerpt in a code file refused) and X1 at ≥3 content words. Measured cost: one genuine fix (R49.1). That is a real harm, so the choice is the L1's, not free.
2. If the SHONEN class must close too, X1 ∧ X9 closes all tested forgeries at 4 of 31 genuine fixes. None of the other mechanical checks I tried closes it cheaply.
3. Open rows: add X5, and note it is a speed bump (defeated by re-pointing). Semantic review of open claims stays with the closure, as the counter's own docstring says.
4. Fixture gap: round-50's selftest defects have no `text` field, so any check that reads item text is untested by the harness. The successor needs a fixture case for it.
5. Inherited regex gap: `planned_ids` matches only `R4\d\.\d+`. Round 50–56 ids (R5x) would never count as planned, so the successor must widen it. The newest "**Planned (round" paragraph is taken by file position, not round number, so an appended paragraph names any ids.
6. The base needs repair before any counter can pass (`total=9`): R41.6's two evidence items no longer resolve in `corpus/SOURCES.md` (lines 469–471), R42.3 and R49.3 also refuse on evidence, and six open rows are not named in the newest planned paragraph.

## Limits (not run)

- No semantic check of any row: whether a keyed excerpt resolves the defect is outside the mechanical rules, as the docstring says.
- The round-57 counter (`.ufo/evidence/round-57/c1/measure.py`) does not exist yet; everything here is against the round-50 rules it inherits.
- Forged commits and ledgers exist only in the scratch clone, which is removed at exit. The harness sources and outputs are in the receipts directory.

## Installs

None. Tools used: git, python3 (stdlib).
