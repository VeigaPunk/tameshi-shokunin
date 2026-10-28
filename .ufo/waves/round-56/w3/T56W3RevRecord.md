# T56W3RevRecord — round-56 record drafts and integrated records against the receipts at PIN

- seat: T56W3RevRecord (leaf, wave 3; L1 `TameshiR56a3`, hyaku run 11)
- lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- PIN audited: `2f5512a8ab0771fb2eee463ec16db359174f5edd` (`round-56: restate calibration at the C1 bind`)
- C0: `c0137451f5b7f22d65f748fc69f1b181f55e1378` (`c013745`); base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; operative freeze `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1); original freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
- no lane file, frozen instrument, bound ledger entry or git ref was mutated. All git calls were reads (`show`, `cat-file`, `rev-parse`, `ls-tree`, `grep`, `log`) or inside scratch clones (`git clone --shared`, toplevel asserted equal to the clone path). Tools installed: none.

## 0. Verdict

**The drafts disagree with the receipts in five places, and the integrated PIN records disagree in four more. One of the PIN disagreements is decisive for the deciding run: the standing calibration row as committed at PIN fails the frozen C1 counter's own arm 6, so C1 cannot pass at PIN as filed.**

| # | severity | where | disagreement |
|---|---|---|---|
| R1 | **blocking** | `SCORECARD.md` @PIN, calibration row line 2718, cell 2 | `Round-21 cold-read monitor …` — the frozen arm 6 tests `'round-21' in cells[2]` (case-sensitive). The counter at PIN prints `total=1 C1_R56_PASS=false`; the one failing arm is arm 6. Demonstrated fixed by a one-character case change in a scratch commit (§4). |
| R2 | high | `SCORECARD.md` @PIN, C2 claim row (line ~2725) and `contract.json` `claims.C2.before` | Both say `total=6`. The receipt `.ufo/evidence/round-56/before/c2.stdout` says `total=2`. No measured receipt carries `total=6`; the value exists only in contract prose and the PIN block. Wave 1 already flagged the same misquote (`T56W1CritClaimShape.md:75`, `T56W1CritClaimShape-receipts/c2-before-misquote.txt`, F3) and it was copied into the PIN block anyway. |
| R3 | high | `SCORECARD.md` @PIN block + drafts | The C2 "before" receipt was measured on the superseded instrument at `c3e2ca9f` (`selftest=14/14`). The PIN block names the operative freeze as `21eb3c63`, where the same counter reads `selftest=19/19` (§3). The before line therefore does not come from the operative instrument, and the block does not say so. |
| R4 | high | `corpus/lessons/round-56.md` @PIN, `## Round-57 deferrals`, "Blocker, not a deferral" paragraph (lines 150–154) | States "C1 is an honest miss this attempt; the seven headings stay unbound and the monitor stays at 46/64". Contradicted by `.ufo/waves/round-56/integration/binder.stdout` (`REFRESH rekeyed=18 skipped=0 headings=18`), by the PIN monitor (64/64, score 8) and by the same file's attempt-3 section ("All 18 C0 reader reports are now present"). |
| R5 | high | `corpus/lessons/round-56.md` @PIN, header lines 11–12 | Says "frozen at `c3e2ca9f` … `amendments` `<L1 fills>`; Content commit C0 `<L1 fills>`". The operative freeze is `21eb3c63` with one amendment (`freeze.json` @PIN); C0 is `c0137451f5b7`. Placeholders still in the committed record. |
| R6 | high | `corpus/lessons/round-56.md` @PIN, lines 27, 103, 104, 105 | `<L1 fills>` remains in the census line and in the R55.1, R55.2, R55.3 dispositions (after-receipts not yet produced). |
| R7 | high | Scorecard draft `T56W1ScribeScorecard.md` §1 + §3; Log draft; Lesson draft header | "frozen at `c3e2ca9f` … `amendments: []`, ten frozen files". Receipt `freeze.json` @c3e2ca9f: 10 files, 0 amendments; `freeze.json` @PIN: **12 files, 1 amendment** (`n=1`, `prior_freeze=c3e2ca9f`). The draft's pointer is the superseded freeze. |
| R8 | high | Scorecard draft §3 (the integration obligation) | Prescribes the measured-commit cell = C0 and the score cell = the monitor's reading at C0. The monitor at C0 reads **6** (`covered=46/64 box3=False`, 18 uncovered headings), so the draft's own rule can never reach 8 and the draft's arm-6 walk-through (§4b) runs on an unbound tree. The PIN row uses `c1dd23b`, where the monitor reads 8 (correct; §2). |
| R9 | high | `corpus/lessons/round-56.md` @PIN, `## Round-55 routed defects` R55.6 and `## Mistakes` class "landing" | Cites `clean-tree-before.txt` / `DECIDING_REFUSED dirty-tree` (and `clean-tree-after.txt`) as the red-before showing the deciding run refuses a dirty tree. No such file exists at PIN (`git cat-file -e PIN:.ufo/evidence/round-56/clean-tree-before.txt` → absent); the file is written only by a deciding run that has not happened. The fix is therefore unshown. |
| R10 | high | `corpus/lessons/round-56.md` @PIN, `## Round-57 deferrals` F1-R1 | Attributes the monitor's 47/64 → 46/64 to "one post-C0 line" in `SKILL.md`. The cited probe `.ufo/waves/round-55/w1/T55W1RevLedger-receipts/probe2.stdout` lines 3–4 say: "re-keying ONLY `## Standing rules` → covered=47/64" and "… + a **post-PIN `QUALITY.md` edit** → covered=46/64". The receipt names QUALITY.md, not SKILL.md, and is round-55 evidence, not a round-56 frozen-binder measurement. |
| R11 | high | `corpus/lessons/round-56.md` @PIN, `## Gate` S282 row (line 21) and draft lesson §3 (C0) | S282 quote "Provenance is a predicate that describes how a software build was executed." (11 words). Not in the source: `.ufo/waves/round-56/integration/l1-source-reopen.txt` line 15 gives "Provenance is an attestation that a particular build platform produced a set of software artifacts through execution of the buildDefinition." The errata (lesson ~lines 232–240) supersedes it, but the table row still carries the false quote. |
| R12 | medium | `corpus/lessons/round-56.md` @PIN, `## Gate` DSSE row (line 20) | "(6 words)" for `SERIALIZED_BODY: Arbitrary byte sequence to be signed.`; the same file's errata (line 191) says "(7 words", and `l1-source-reopen.txt` says "(7 words)". The link is `blob/master/protocol.md`; the L1 re-open pins `blob/b531b787bb3e5f0c3e1c19cee84da1c5d569b061/protocol.md`. The draft says 6 words and `master`. |
| R13 | medium | `corpus/lessons/round-56.md` @PIN, errata "S282 quote re-opened by L1" / "source search log" paragraph (line ~197) | "The source search log records 3 identified/screened, 1 included (S281), 2 excluded." No receipt carries this count: `corpus/SOURCES.md` round-56 paragraph (line 523) lists S281 and S282 and no identified/screened numbers; no round-56 receipt contains "identified 3". Value with no receipt. |
| R14 | medium | `corpus/lessons/round-56.md` @PIN, `## Mistakes` 3rd bullet and draft §1 | "`git cat-file -e c3e2ca9f:…/before/c1.stdout` → absent" is correct (exit 128) but historical; C0 now commits the three `before/` receipts (`git cat-file -e c0137451f5b7:…` resolves). The PIN record should say so. |
| R15 | medium | Lesson draft §3 `## Mistakes`, class "landing" (before-receipts) and `T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt` | The lesson quotes `rev=077d431e6996 credited=99 lost=0 → verdict=PASS` and cites the receipt. The receipt (4 lines) carries `GATE OK … revs=077d431e6996` and `verdict=PASS`; the string `credited=99 lost=0` is not in it. It appears only in `T56W1ScribeQuality.md:108`. |
| R16 | medium | `corpus/knowledge/receipt-revision-binding.md` @PIN, lines 155 and 166 | Re-derive block says `GATE_SELFTEST: 14/14 pass`. The C0 gate prints `19/19` (`c2-pin` arm1, §3; the knowledge note's own errata ER-R56-K1, lines 225–226, says 19/19). Stale body, errata present. |
| R17 | medium | Scorecard draft, Log draft, lesson draft: "census at round end" and "140 rows" | 140 is the round-start census (`census-start.exit`=0, 140 rows). At PIN `corpus/SOURCES.md` has **142** rows (grep, §2). No round-end census receipt exists at PIN; the lesson placeholder is still `<L1 fills>`. Value with no receipt. |
| R18 | medium | `LOG.md` @PIN | No round-56 entry (`git show PIN:LOG.md | grep -c 'round 56'` → 0). The Log draft is not integrated; when integrated it must replace its `amendments: []` and `c3e2ca9f` freeze pointer with `21eb3c63` (R7). |
| R19 | low | Draft Scorecard §2 "freeze.json files = 10, amendments = []"; draft §6 "frozen at c3e2ca9f" | Correct for `c3e2ca9f` only. Keep, but label as historical. |
| R20 | low | Contract `claims.C1/C2.controls` and PIN block control ids (`CTL_0`, `CTL_SKIP`, …) vs `controls.sh` emitted names (`CTL_0_c1`, `CTL_SKIP_c1`, …) | Unsuffixed in the contract, suffixed in the script. Not a value mismatch; the deciding gate greps `CONTROLS_A/B` lines, not the ids. Note only. |
| R21 | low (counter output) | `c1/measure.py` print statement, `restate=%s` | Prints `row_score`, not the arm-6 boolean. A failing line reads `… restate=8 total=1 …` and a reader can take `restate=8` as a pass. Frozen; cannot change. Quote `total=` only. |

## 1. What was checked, and how

**Drafts (wave 1, the item):** `.ufo/waves/round-56/w1/T56W1ScribeScorecard.md` (block byte-exact at `T56W1ScribeScorecard-receipts/block.md`, sha256 `ef4166a6…ffad9`, 7034 B — verified), `T56W1ScribeLog-log-entry.md` (the LOG text; `T56W1ScribeLog.md` is its report), `T56W1ScribeLesson.md` §3 (the lesson text). The wave-3 directory contains no rewritten scribe text (`.ufo/waves/round-56/w3/` holds only `T56W3ExecControlsA-receipts`, `T56W3ExecControlsB-receipts` and the registry), so the drafts are the final texts for this audit; the integrated PIN texts are audited alongside them because those are what the deciding run reads.

**Receipts:** read from PIN via `git show PIN:<path>` (committed bytes). Uncommitted working-tree files were not used as evidence.

**Frozen instruments at PIN:** `sha256` of `contract.json`, `c1/measure.py`, `c2/measure.py`, `controls.sh`, `no-harm.sh`, `deciding-run.sh`, `tools/receipt-revision-gate.py` equal the `freeze.json` (21eb3c6) entries (first 16 hex digits, all seven match: `254dd0983735ae61`, `048122cf1c7c65d2`, `915580190cb1d5c3`, `65b4b5105668786f`, `a13ba1a8433752c8`, `a644123e764a568f`, `c60772ceb0ce3f51`). So the counter runs below are the frozen instruments.

**Counter and monitor runs (scratch clones, read-only):** clones at PIN, C0, `c1dd23b`, base, `d33053f7`, `21eb3c6`; `git clone --shared` from the lane; toplevel asserted equal to the clone path; checkouts `--detach`.

| run | command (clone = `$S/clone-<n>`, `S=/fast/scratch/hyaku/tameshi-r56/T56W3RevRecord`) | verdict line(s), exit |
|---|---|---|
| monitor @PIN | `python3 $S/clone-pin/.ufo/evidence/round-21/coldread/measure.py --repo $S/clone-pin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd` | JSON: `calibration_restraint_score 8`, `sections_covered 64/64`, `box3_full_page True`, `revision 2f5512a8ab07…` |
| monitor @c1dd23b | same, `--rev c1dd23b3f83f5dff676c4a4482498e87345375ef` | `score 8`, `64/64`, `box3 True`, `revision c1dd23b3f83f…` |
| monitor @C0 | same, `--rev c0137451f5b7f22d65f748fc69f1b181f55e1378` | `score 6`, `46/64`, `box3 False`, `missing 18` |
| monitor @base | same, `--rev 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` | `score 6`, `46/64`, `box3 False` |
| monitor @d33053f7 | same, `--rev d33053f7552db4bd290c99a36979760f544c41ad` | `score 6`, `57/64`, `box3 False`, `missing 7` |
| C1 @PIN | `python3 $S/clone-pin/.ufo/evidence/round-56/c1/measure.py --lane $S/clone-pin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work $S/w-c1-pin --explain` | `EXPLAIN arm1-precheck exit=0 … cand_credited=64 lost=0 ok`; `arm2-monitor covered=64 score=8 box3=True`; `arm3-rekey dirs=['rekey-r56-c0137451f5b7'] c0=c0137451f5b7…`; `arm4-readers 18/18`; `arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='Round-21 cold-read …' round='56'`; **`C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false`**; exit 1 |
| C1 @C0 | same, `--rev c0137451f5b7f22d65f748fc69f1b181f55e1378` | `arm1-precheck exit=1 … cand_credited=46 lost=18 RED`; `C1_R56: rev=c0137451f5b7 … monitor=6/46 … total=5 C1_R56_PASS=false`; exit 1 |
| C1 @base (frozen counter, base rev) | `python3 $S/clone-freeze/.ufo/evidence/round-56/c1/measure.py --lane $S/clone-freeze --rev 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 --work $S/w-c1-base2 --explain` | `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`; exit 1 |
| C2 @PIN | `python3 $S/clone-pin/.ufo/evidence/round-56/c2/measure.py --lane $S/clone-pin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work $S/w-c2-pin --explain` | `arm1-selftest exit=0 19/19`; `arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True`; `arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE`; `arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT`; `arm6-docs 4/4`; **`C2_R56: rev=2f5512a8ab07 selftest=19/19 … own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false`**; exit 1 |
| C2 @21eb3c6 (operative freeze) | same with `clone-freeze`, `--rev 21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` | `selftest=19/19 … docs=0/4 total=2 C2_R56_PASS=false`; exit 1 |
| C1 demo (§4) | `python3 $S/demo-fix/.ufo/evidence/round-56/c1/measure.py --lane $S/demo-fix --rev 5cdab54dd54a057731927d121c09a091acb77b86 --work $S/w-c1-demo --explain` | `arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='round-21 cold-read …' round='56'`; **`C1_R56: rev=5cdab54dd54a c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true`** |

The C1 base run is the frozen-counter re-derivation of the draft's `c1-at-base.stdout`, and matches it byte for byte. The C2 freeze run at `c3e2ca9f` was not repeated (the draft's `c2-at-freeze.stdout` and `before/c2.stdout` agree with each other).

Predicate check, arm 6, on the PIN row (same parse as `c1/measure.py:255-281`, run over `git show PIN:SCORECARD.md`): `n_rows 8`, last row score `8`, `'round-21' in cells[2]: False`, `'Round-21' in cells[2]: True`, commit cell hits `['c1dd23b3f83f5dff676c4a4482498e87345375ef']`, `56 in cells[4]: True`.

## 2. Record-versus-receipt table

Status: **OK** = value matches its receipt at the stated line; **MISMATCH** = record and receipt disagree; **NO RECEIPT** = value stated with no receipt at the cited place; **SUPERSEDED** = matched at its own commit but wrong for the operative revision/instrument.

### 2a. Scorecard draft (`T56W1ScribeScorecard.md`; block sha `ef4166a6…`)

| # | value as written | where written | receipt (path : line) | status |
|---|---|---|---|---|
| S1 | `C1_R56: rev=981c5e8b20a2 … monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` | block §1 C1 "Before" cell; §2 row 2 | `.ufo/evidence/round-56/before/c1.stdout` : 6; re-run `c1-base.txt` (frozen counter @base) : last line | OK |
| S2 | `C2_R56: rev=c3e2ca9f0207 selftest=14/14 … docs=0/4 total=2 C2_R56_PASS=false` | block §1 C2 "Before" cell | `.ufo/evidence/round-56/before/c2.stdout` : 6 (identical in `T56W1ScribeScorecard-receipts/c2-at-freeze.stdout`) | OK at `c3e2ca9f`; **SUPERSEDED** at `21eb3c6` (19/19, §3) |
| S3 | `C2_R56: error=gate-missing` not in block | Log draft / lesson draft | `.ufo/evidence/round-56/before/c2-at-base.stdout` : 1 `C2_R56: error=gate-missing total=1 C2_R56_PASS=false` | OK (in Log & Lesson drafts) |
| S4 | calibration `6` at `981c5e8b`, `covered=46/64`, `box3=false` | block §1 standing row; §2 row 1 | `T56W1ScribeScorecard-receipts/monitor-base.txt` : 1; re-run @base `score 6, 46/64, box3 False` | OK |
| S5 | calibration `6` at `d33053f7`, `57/64` | block §2 row 2 | `T56W1ScribeScorecard-receipts/monitor-d33053f7.txt` : 1; re-run @`d33053f7` `score 6, 57/64, box3 False` | OK |
| S6 | `calibration_restraint_score=6`, `sections_covered=46/64`, `box3_full_page=false` | block §2 row 1 | re-run @base (above) | OK |
| S7 | "draft's measured-commit cell = C0; score = monitor at C0" | block §3 steps 1–2 | re-run @C0: `score 6, 46/64, box3 False` (18 missing) | **MISMATCH with its own plan** — R8 |
| S8 | "ten frozen files, `amendments: []`" | block §1 header; §2 | `freeze.json` @c3e2ca9: 10 files, `amendments []`; @PIN / @21eb3c6: **12 files, 1 amendment** | SUPERSEDED — R7 |
| S9 | "frozen at `c3e2ca9f`" | block §1 header | commit `c3e2ca9f` exists (`freeze` commit) | OK historically; **superseded** by `21eb3c63` — R7 |
| S10 | "fifteen no-harm monitors" | block §1 | `contract.json` `no_harm_monitors` = 15; `no-harm.sh` `echo "NOHARM` count = 15 | OK |
| S11 | "byte-identical to `fa48c06c` on every claim path; diff empty" | block §1 | `git diff --stat fa48c06c 981c5e8b -- SKILL.md SCORECARD.md LOG.md corpus tools` → no output | OK |
| S12 | `fa48c06c`, `c3e2ca9f`, `981c5e8b`, `d33053f7` all resolve | block §2 | `git rev-parse --verify <h>^{commit}`: `fa48c06c3669…`, `c3e2ca9f0207…`, `981c5e8b20a2…`, `d33053f7552d…` | OK |
| S13 | control ids `CTL_0_c1 CTL_SKIP_c1 CTL_FAB_c1 CTL_RESTATE_c1 CTL_POS_c1; CTL_0_c2 CTL_SKIP_c2 CTL_FAB_c2 CTL_POS_c2` | block §2 | `.ufo/evidence/round-56/controls.sh` `emit` lines 59–148 (names as listed) | OK (contract uses unsuffixed names — R20) |
| S14 | round-54 gate accepted the set: `DECIDING_RUN_EXIT=0` | block §2 | `.ufo/evidence/round-54/after/deciding-run.exit` : 1 | OK |
| S15 | census at round start "140 rows (S001–S280)" | block §2 | `T56W1ScribeScorecard-receipts/census.txt`; `corpus/SOURCES.md` @base: 140 rows | OK (round start only) — R17 |
| S16 | `block.md` sha256 `ef4166a6…ffad9`, 7 034 B | report header | `sha256sum` / `wc -c` | OK |

### 2b. Log entry draft (`T56W1ScribeLog-log-entry.md`, appended after LOG.md:2554)

| # | value as written | receipt (path : line) | status |
|---|---|---|---|
| L1 | `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` | `before/c1.stdout` : 6 | OK |
| L2 | arm2 `covered=46 score=6 box3=False` | `before/c1.stdout` : 2 | OK |
| L3 | row `calibration | 8 | … | d33053f7 | 53 |` at `SCORECARD.md:2579` | base `SCORECARD.md` line 2579 | OK |
| L4 | arm6 `row_score=8 row_commit=d33053f7552d score_at_row=6` | `before/c1.stdout` : 5 | OK |
| L5 | `C2_R56: rev=c3e2ca9f0207 … docs=0/4 total=2 C2_R56_PASS=false` | `before/c2.stdout` : 6 | OK (superseded instrument — S2) |
| L6 | round-54 `CTL_POS_c1 … rev=077d431e6996` | `.ufo/evidence/round-54/control/controls-b.stdout` : 1 | OK |
| L7 | round-54 `CTL_EXIT0 … rev=7df0e0426c98` | `…/controls-b.stdout` : 4 | OK |
| L8 | `7df0e0426c98` is not a git object (`fatal: Not a valid object name`, exit 128) | `git cat-file -t 7df0e0426c98` | OK |
| L9 | `077d431e6996`, `c21081008adb` resolve | `git rev-parse --verify` (`077d431e69965fa4…`, `c21081008adbb6b6…`) | OK |
| L10 | round measured `c21081008adb` | `.ufo/evidence/round-54/after/c1.stdout` : `C1_R54: rev=c21081008adb …` | OK |
| L11 | round-54 gate accepted: `DECIDING_RUN_EXIT=0` | `round-54/after/deciding-run.exit` : 1 | OK |
| L12 | round-55 C2 receipt has `rev=` count 0; last line `EXPLAIN usable repeat-control --selftest rc=0 ok` | `.ufo/evidence/round-55/after/c2.stdout` (base): `grep -c 'rev='` → 0; last line as quoted | OK |
| L13 | `QUALITY` last criterion 106 at `corpus/QUALITY.md:1592` | base `corpus/QUALITY.md` line 1592 `### Criterion 106` | OK |
| L14 | SOURCES 140 rows; S281 next free | base `corpus/SOURCES.md`: 140 rows; S280 last; "Next unused id: S281" (line 517 round-55 note) | OK |
| L15 | append after `LOG.md:2554`; tail `produced. Waves measured close and deciding receipts follow under this entry.` | base `LOG.md` 2552–2554 | OK |
| L16 | `lost-headings-at-base.json` denominator 18 | `.ufo/evidence/round-56/c1/lost-headings-at-base.json` : list length 18 | OK |
| L17 | `freeze` `amendments: []` "as this entry is drafted" | `freeze.json` @c3e2ca9 : `amendments []`; @PIN : 1 amendment | SUPERSEDED — R7/R18 |
| L18 | `git cat-file -e c3e2ca9f:.ufo/evidence/round-56/before/c1.stdout` absent | exit 128: "exists on disk, but not in 'c3e2ca9f'" | OK (historical; C0 commits the file — R14) |
| L19 | `C1 before` line identical; `C2 before (pre-gate)` `error=gate-missing total=1` | `before/c2-at-base.stdout` : 1 | OK |
| L20 | `CORPUS` / "the append" fields | — | not checkable as receipts; `<L1 fills>` placeholders present in draft (expected) |

### 2c. Lesson draft (`T56W1ScribeLesson.md` §3; the `corpus/lessons/round-56.md` text)

| # | value as written | receipt (path : line) | status |
|---|---|---|---|
| Z1 | QUALITY next number 106 (so 107); "`### Criterion 83` twice, 85 absent" | base `corpus/QUALITY.md`: `### Criterion 85` count 0; `### Criterion 83` count 2 | OK |
| Z2 | S280 last id; "Next unused id: S281" | `T56W1ScribeLesson-receipts/ids-and-source.txt`; base SOURCES | OK |
| Z3 | 140 registry rows; snapshot sha256 `cbe684a1…ebea` | `ids-and-source.txt`; `sha256sum .ufo/evidence/round-56/assimilation/in-toto-statement-v1.md` → `cbe684a18b812b8b…ebea` ; PIN `assimilation/in-toto-statement-v1.md` 2492 B | OK |
| Z4 | S281 quote "Subject artifacts are matched purely by digest, regardless of content type." (11 words), snapshot lines 54–55 | `in-toto-statement-v1.md` lines 54–55 (`IMPORTANT: Subject artifacts are matched purely by digest, regardless of content type.`); `T56W1ScoutSource.json` `quote_words: 11` | OK |
| Z5 | DSSE quote "SERIALIZED_BODY: Arbitrary byte sequence to be signed." — "(6 words)" | `l1-source-reopen.txt` : "(7 words)"; draft and PIN lesson line 20 say 6; URL `master` vs pinned `b531b787` | **MISMATCH** (word count, URL) — R12 |
| Z6 | S282 quote "Provenance is a predicate that describes how a software build was executed." (11 words), as a located quote | `l1-source-reopen.txt` : 15 "Provenance is an attestation that a particular build platform produced …" (20 words). Quote not in source. | **MISMATCH** (false quote) — R11; the draft carried this quote into C0 (`git show c013745:corpus/lessons/round-56.md`) |
| Z7 | `7df0e0426c98` "Not a valid object name" | exit 128 (L8) | OK |
| Z8 | round-55 R55.6 seven files and times (13:55:47, 13:58:42, 14:02:24, 14:31:03, 14:34:53 before tip 14:54:02); "83 entries", "7 of them" | `.ufo/waves/round-55/…/corpus/lessons/round-55-verifier-spotcheck.md` lines 28, 35, 139–141 (base) | OK |
| Z9 | round-55 "14 tracked `T55W1MutC2-receipts` files deleted" | same file line 145 | OK |
| Z10 | `CORPUS.md:174-177` vocabulary includes `landing`, `attribution` | `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 174–177 | OK |
| Z11 | R55.2 receipt `c2-integrated.out` `total=1 C2_R55_PASS=false` where the report quoted `total=0` | `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` : `… total=1 C2_R55_PASS=false`; report `T55W1ScribeSkill.md:157` quotes `total=0` for an earlier commit | OK |
| Z12 | R55.4 `CTL_SKIP_c2 … total=4`, `CONTROLS_A: 5/5` | `.ufo/evidence/round-55/control/controls-a.stdout` | OK |
| Z13 | C1 red-before line; arm6 `row_score=8 row_commit=d33053f7552d score_at_row=6` | `before/c1.stdout` : 5–6 | OK |
| Z14 | C2 red-before `selftest=14/14 red54=… red54b=… red55=… docs=0/4 total=2` | `before/c2.stdout` : 6 | OK at `c3e2ca9f`; SUPERSEDED at 21eb3c6 (19/19) |
| Z15 | `DECIDING_REFUSED dirty-tree` with `clean-tree-before.txt` / `clean-tree-after.txt` as the red-before of R55.6 | `deciding-run.sh` lines 129–132, 164–165 write these files at deciding time; **no file at PIN** (`git cat-file -e PIN:.ufo/evidence/round-56/clean-tree-before.txt` → absent) | **NO RECEIPT** — R9 |
| Z16 | R55.1 `receipt-gate-verdicts.stdout`, gate 0c | `deciding-run.sh` line 160–162 names it; file not produced at PIN | the script reference is OK; the "after" receipt is `<L1 fills>` |
| Z17 | `T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`: `rev=077d431e6996 credited=99 lost=0 → verdict=PASS` | receipt (4 lines): `GATE OK … revs=077d431e6996`, `verdict=PASS`; **`credited=99 lost=0` absent from the receipt** | **MISMATCH (partial)** — R15 |
| Z18 | "wave 2 reader findings 13 total, six headings" | `.ufo/waves/round-56/integration/resolutions.json` : 6 entries, n = 1+1+3+2+2+4 = 13 | OK |
| Z19 | "Read17 page-local ranges 57 of 61 drifted; +4 and +13 offsets" | `.ufo/waves/round-56/w2/T56W2Read17-receipts/page-wide-sweep.txt` lines 14–16 (`page-local ranges total : 61`, `DRIFTED (cited bytes moved): 57`) and lines 3–11 (`+4`, `+13`) | OK |
| Z20 | "the C0 gate selftest `GATE_SELFTEST: 19/19 pass`" | C2 counter arm1 at PIN: `exit=0 19/19`; `T56W1MutGate-receipts/11-patch-demo.log` is a *patched* baseline (applied_to_lane false) and not the C0 gate | OK via the counter (arm1); the MutGate receipt is not the citation |
| Z21 | "freeze 21eb3c6 amendment 1 … 19-case suite" (errata) | `freeze.json` @PIN `amendments[0].n = 1`, `prior_freeze c3e2ca9f` | OK |
| Z22 | "seven of eighteen reader reports do not exist at C0 … C1 is an honest miss; monitor stays at 46/64" | `binder.stdout` : `REFRESH rekeyed=18 skipped=0 headings=18`; `bind-monitor` / PIN monitor 64/64 score 8 | **MISMATCH (stale, contradicted)** — R4 |
| Z23 | R1: "one post-C0 line [SKILL.md] takes the monitor 47/64 -> 46/64" | `T55W1RevLedger-receipts/probe2.stdout` lines 3–4: 47/64 after `## Standing rules` only; 46/64 after a *post-PIN `QUALITY.md` edit* | **MISMATCH (file)** — R10 |
| Z24 | `SKILL.md` `## Standing rules` text (F2): "role=verdict paths=1 → RECEIPT_REV_CONTENT_DRIFT …" | `T56W2RevSkillScope.md` §6a cited; not re-measured here | not checked (outside the item's numbers) |
| Z25 | `corpus/lessons` R55.6 "seven files" and `git log 981c5e8` messages | `git show --stat 981c5e8`, `6efd2a1` (commit messages name R55.6/R55.7) | OK (commit existence verified) |

### 2d. Integrated records at PIN (what the deciding run reads)

| # | value as written | where | receipt | status |
|---|---|---|---|---|
| P1 | calibration `8` at `c1dd23b3f83f5dff676c4a4482498e87345375ef`, last-change `56`, "`64/64`, `box3=true`" | `SCORECARD.md` @PIN line 2718 | `bind-monitor.json` (`calibration_restraint_score 8`, `sections_covered 64`, `box3_full_page true`, `revision c1dd23b…`); re-run @c1dd23b: `score 8, 64/64, box3 True` | OK value; **counter-unreadable (R1)** |
| P2 | row evidence cell "Round-21 cold-read monitor …" | `SCORECARD.md` @PIN line 2718 cell 2 | arm 6 `'round-21' in cells[2]` → False | **MISMATCH with frozen predicate — R1** |
| P3 | C1 before `C1_R56: credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5` | `SCORECARD.md` @PIN block, "Frozen claims" table | `before/c1.stdout` : 6 | OK |
| P4 | C2 before `…total=6 C2_R56_PASS=false` | `SCORECARD.md` @PIN block table; `contract.json` `claims.C2.before` | `before/c2.stdout` : `total=2` (also `c2-at-base` total=1) | **MISMATCH — R2** |
| P5 | "operative freeze `21eb3c63` (amendment 1; original `c3e2ca9f`)" | `SCORECARD.md` @PIN header | `freeze.json` @PIN: `amendments[0]` n=1, `prior_freeze c3e2ca9f…` | OK |
| P6 | C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378` | `SCORECARD.md` @PIN header | `git rev-parse c0137451f5b7…` = `c013745`; commit `c013745 round-56 C0` | OK |
| P7 | "18/18 headings bound at C0, 18/18 committed readers, no LOG/SCORECARD inputs" | `SCORECARD.md` @PIN target column (claim text) | C1 @PIN: `rekeyed=18/18 readers=18/18` ; `rekey-r56-c0137451f5b7` present | OK (the bound entries are not re-audited here) |
| P8 | `W2's C2 do-nothing attack` ; `T56W2CritDoNothingC2.md` | `SCORECARD.md` @PIN block | `.ufo/waves/round-56/w2/T56W2CritDoNothingC2.md` exists | OK |
| P9 | "the C1 counter the deciding run reads at PIN" — not stated | — | C1 @PIN `total=1` (arm 6) ; C2 @PIN `total=1` (own-receipts-missing) | observed; record does not claim either |
| P10 | LOG: round-56 entry | `LOG.md` @PIN | `grep -c 'round 56' LOG.md` → 0 | **NOT INTEGRATED — R18** |
| P11 | lesson header: "frozen at `c3e2ca9f`; amendments `<L1 fills>`; C0 `<L1 fills>`" | `corpus/lessons/round-56.md` @PIN lines 11–12 | `freeze.json`: 1 amendment; C0 = `c013745` | **MISMATCH + placeholder — R5** |
| P12 | census at round end `<L1 fills>` | lesson @PIN line 27 | `SOURCES.md` @PIN: 142 rows (`grep -cE '^ {0,3}\| S[0-9]{3,} \|'`); no round-end census receipt | **NO RECEIPT — R17** |
| P13 | lesson R55.1/R55.2/R55.3 after-receipts `<L1 fills>` | lesson @PIN lines 103–105 | `.ufo/evidence/round-56/after/` absent at PIN (expected: deciding run not run) | placeholder — R6 |
| P14 | lesson "Blocker: C1 honest miss … 46/64" | lesson @PIN lines 150–154 | `binder.stdout` REFRESH rekeyed=18; PIN monitor 64/64 | **MISMATCH — R4** |
| P15 | S281 row "snapshot lines 36-37 and 54-55 … body sha256 cbe684a1…ebea identical at main 50bf0171" | `corpus/SOURCES.md` @PIN line 156 | `in-toto-statement-v1.md` (sha256 `cbe684a1…ebea`, 2492 B) ; `main 50bf0171` not re-fetched | OK on receipt; `main` commit not re-checked |
| P16 | S282 row "REJECTED"; quote "Provenance is an attestation …" in errata | `corpus/SOURCES.md` @PIN S282 row; lesson errata | `l1-source-reopen.txt` line 15 | OK in SOURCES & errata; **false quote still in lesson Gate row — R11** |
| P17 | knowledge note `14/14 pass` (lines 155, 166) | `corpus/knowledge/receipt-revision-binding.md` @PIN | C0 gate prints `19/19` (P/§3); errata lines 225–226 | **MISMATCH (body stale) — R16** |
| P18 | "3 identified/screened, 1 included, 2 excluded" | lesson errata (line ~197) | none at PIN — R13 | **NO RECEIPT** |
| P19 | C2 docs 4/4 at PIN, rule present in QUALITY / knowledge / SKILL / registry | counter arm6 at PIN | `c2-pin.txt` `docs=4/4` | OK |

## 3. The C2 "before" receipt is not the operative instrument

`contract.json` (frozen, unchanged) and the PIN SCORECARD both describe the C2 before receipt as the operative freeze's output. The receipts:

| commit | instrument | command output (exact) | exit |
|---|---|---|---|
| `c3e2ca9f` (original freeze; the source of `before/c2.stdout`) | gate with 14 selftest cases | `C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` (`before/c2.stdout`, line 6) | 1 |
| `21eb3c6` (operative, amendment 1) | gate with 19 selftest cases | `C2_R56: rev=21eb3c63cd0f selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` (re-run, `c2-freeze.txt`) | 1 |
| `2f5512a` (PIN) | same as 21eb3c6 | `C2_R56: rev=2f5512a8ab07 selftest=19/19 … docs=4/4 total=1 C2_R56_PASS=false` (re-run, `c2-pin.txt`) | 1 |

So the before receipt is the superseded instrument's output, its `docs=0/4` is at `c3e2ca9f` (where the rule was absent), and no measured receipt carries `total=6` (wave 1 F3 flagged that value before PIN). The record should quote `total=2` and name `c3e2ca9f` as the instrument that produced it, or cite the operative `21eb3c6` line that prints `selftest=19/19`. The frozen contract's prose is not changed by this audit.

## 4. Demonstration of the R1 fix (scratch only; not a lane patch)

Scratch clone `$S/demo-fix` at PIN, toplevel asserted equal to the clone path; one commit `5cdab54dd54a057731927d121c09a091acb77b86` (`demo: lowercase round-21 in calibration row cell 2`), the only change:

```diff
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ (calibration row, last table line of the round-56 block)
-| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |
+| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |
```

Frozen C1 counter at that commit: `C1_R56: rev=5cdab54dd54a c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` (exit code not captured; the `total=0` line is the verdict). Arm 1–4 and 6 pass. This is evidence that arm 6 is the only failing arm at PIN. It is not a deciding receipt: the L1 must commit the case fix, choose the new REV, and re-run the monitor and counters at that REV. The C0 bind is unaffected (the bound headings are unchanged; arm 3 still `rekey-r56-c0137451f5b7`).

Two cautions for the L1: (a) the demo counter line is on a commit one step past PIN, so the deciding receipt must be re-measured at the revision the deciding run certifies; (b) the monitor value 8 is pinned to `c1dd23b` in the row's measured-commit cell — the row must not move that cell to C0 (R8: the monitor reads 6 at C0).

## 5. Counter-facing notes (frozen; recorded, not changed)

- `C1_R56: … restate=8 total=1 C1_R56_PASS=false` at PIN: `restate=` prints `row_score` (`c1/measure.py` lines 289–292), not the arm-6 boolean. Read `total=`.
- C2 at PIN prints `own=own-receipts-missing`: the operability target still needs the round's own controls at PIN, as the contract says.

## 6. Values with no receipt (consolidated)

1. The clean-tree refusal claimed as red-before (R9): `clean-tree-before.txt` and `DECIDING_REFUSED dirty-tree` — no receipt.
2. The round-end census "exit 0, 142 rows" (R17): no receipt at PIN; `census-start` only (140, exit 0).
3. "3 identified/screened, 1 included (S281), 2 excluded" (R13): no receipt.
4. `credited=99 lost=0` in the scope-gap receipt (R15): not in the cited file.
5. The C2 `total=6` in the contract and PIN SCORECARD (R2): no measured receipt carries it (wave-1 F3 already flagged it).
6. The `<L1 fills>` placeholders in the PIN lesson (R5/R6) and the draft placeholders (`amendments`, C0, the round-end census, the after-receipts): by design unfilled until the deciding run, but the lesson is committed at PIN with them still present.

## 7. Recommended corrections for the L1 (record-only; no frozen file)

1. SCORECARD @PIN row (line 2718): lowercase `round-21` in cell 2 (§4). Verify by re-running the C1 counter at the revision the deciding run certifies.
2. SCORECARD @PIN C2 before cell and the lesson's C2 before wording: `total=2`, and name the instrument (`c3e2ca9f`, 14/14) or cite the operative 21eb3c6 line (19/19, `total=2`). Do not write `total=6`.
3. Lesson @PIN: replace the header freeze pointer with `21eb3c63` (1 amendment), fill C0 with `c0137451f5b7f22d65f748fc69f1b181f55e1378`, and fill or explicitly defer `<L1 fills>` in the census and R55.x rows.
4. Lesson @PIN lines 150–154: delete or rewrite the "Blocker … C1 is an honest miss" paragraph (superseded by the bind; `rekeyed=18`).
5. Lesson @PIN R55.6 and R1: remove the claim that `clean-tree-before.txt` is red-before evidence until the deciding run produces it; re-attribute the 47→46 probe to the post-PIN `QUALITY.md` edit (probe2.stdout lines 3–4), not a SKILL.md line.
6. Lesson @PIN Gate S282 row: replace the quote with the L1-re-opened sentence (`l1-source-reopen.txt` line 15), or mark the row "quote superseded by errata".
7. Lesson @PIN DSSE row: "(7 words)" and the pinned URL, or drop the word count.
8. Lesson errata "3 identified/screened": cite the search log or delete the count.
9. Knowledge note `receipt-revision-binding.md` lines 155, 166: `19/19`.
10. LOG: integrate the draft only after 1–3 (its freeze pointer and `amendments: []` are superseded).
11. Scope-gap receipt (Z17/R15): add the counter line to `107-scope-gap-fabricated-line.txt` or quote only `verdict=PASS` and `revs=`.

## 8. Method limits

- The audit covers the three named drafts and their PIN integrations; it does not re-audit the bound reader reports, the 18 bind entries, the controls or the no-harm monitors.
- The receipts for the S282 blob sha256 `efece57a…76fc`, the `main 50bf0171` commit and the DSSE pinned commit were not re-fetched (no network; the L1 re-open records are the receipts).
- The controls harness (`controls.sh`) and the deciding script were not run; per the seat spec, they are the L1's measurements. The only frozen-instrument runs are the counters and the monitor above, each in a scratch clone.
- The working tree of the lane is dirty with other seats' files; no working-tree file was used as evidence.

## 9. Scratch and artifacts

- Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W3RevRecord/` (clones `clone-pin`, `clone-c0`, `clone-c1dd`, `clone-base`, `clone-freeze`, `clone-d330`, `demo-fix`; outputs `mon-*.txt`, `c1-*.txt`, `c2-*.txt`). Removed after this report was written.
- This report: `.ufo/waves/round-56/w3/T56W3RevRecord.md`. No other lane file written.
- Peer messages sent: to `TameshiR56a3` only (C2 total=6 vs total=2 and the base/freeze distinction; R1 finding and the demo result).
