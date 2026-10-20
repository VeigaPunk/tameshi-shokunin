# Mention sweep recheck — wave 2

Seat `TameshiR17.MentionSweepRecheck-2` (scout, leaf). Target: the 19-item stale-mention
list in `.ufo/waves/round-17/w1/S10MentionSweep.md`, re-checked at
`eb7838b16490ca7ba17ea3242ade76a61f744af2` (henceforth `E`). Question per item:
**swept** / **still stale** / **record** (append-only, correctly left). No existing lane
file was edited; this report is the only lane write, and every run below is in a
fleet-mirror clone of `E`. No tool installed or updated.

## 1. Ground truth (executed, with exits)

Clone: `W=/tmp/tameshi-r17w2-MentionSweepRecheck-2-SsTTSd`, `C=$W/fleet/tameshi-shokunin`,
`git rev-parse HEAD` → `eb7838b16490ca7ba17ea3242ade76a61f744af2`. `sha256sum SKILL.md`
→ `b1bd20aee58a0bd241e257f69e3610f3b8c2b805b2ebbb18f48b8e3184bf9d09`.

| # | Command | Observed |
|---|---|---|
| G1 | `git archive 28aeef498cc070c3183271b709bc79d344ff547a \| tar -x -C $W_arch`; then `cd $W_arch && python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json` | **exit 1**; `status: failed`; finding `id=expected_contains_missing`, `expectation=producer_before` |
| G2 | same cwd, `--dispositions .ufo/evidence/round-14/dispositions.json` | **exit 0**; `status: clean`; `counts {effective 11, superseded 1, failed 0, findings 0}` |
| G3 | from `$C`: current tool, `--root $W_arch` with the same two manifests | **exit 1** / **exit 0** — identical findings (the recipe's "cwd = extracted tree" and the wave-1 archived-root variant agree) |
| G4 | from `$C`: `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json` | **exit 1**; `expected_contains_missing` / `producer_before` |
| G5 | from `$C`: same with `.ufo/evidence/round-17/dispositions.json` | **exit 0**; `status: clean`; `counts {effective 11, superseded 1, failed 0}` — matches `SKILL.md:1837-1838` |
| G6 | from `$C`, live round-14 forms at `--root .` (both manifests) | **exit 2** each; `kind=expected_input_digest_mismatch`; message `observed fb6d86d59… expects 75ed934dc…` |
| G7 | `python3 tools/evidence-disposition.py --selftest` | **exit 0**; `SELFTEST: PASS (56/56)` |
| G8 | `python3 .ufo/evidence/round-17/measure.py --rev eb7838b…` | **exit 0**; `ledger_present: false`, `coldread.box3_full_page: false`, `sections_total: 58`, `sections_covered: 0`, `calibration_restraint_score: 6`, `overrides_used: false` |
| G9 | `.ufo/evidence/round-17/redbefore/measure-09ee1d0.json` | `box3_full_page: false`, score `6`, `overrides_used: true`, `inputs_overlay_merged: 1`, credited `0`; reasons `{input-drift:tools/mutate-and-run.sh: 1, inputs-unrecorded: 53}` |
| G10 | own sectionizer, `SKILL.snapshot.md` vs `E:SKILL.md` | `### Round-15 gate/probe registry` body **30 → 31** lines (1676-1705 → 1676-1706); `## Effective expectation reconciliation — round 14` body **34 → 34** |
| G11 | `git cat-file -e E:.ufo/evidence/round-17/coldread/ledger.json` | **absent at `E`**; `git ls-tree` shows only `assemble.py`, `bucket-commands.json`, `trace-inputs.py` under `round-17/coldread/` |
| G12 | `git show E:tools/mutate-and-run.sh \| sha256sum` | `fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a` |

`corpus/lessons/round-16-verifier-spotcheck.md` (non-author closure, committed at `E`) §2–§3
grounds the "truth" column: 53/54 counterfactual, `box3_full_page false`, restraint **6**,
operability **harmed**. `SCORECARD.md` has no Round-17 heading (last heading `## Round 16`,
594 lines); `LOG.md` has no Round-17 entry (1055 lines, tail ends in the round-16 block).

## 2. Item-by-item

Landing line numbers are at `E` (they moved for SKILL items 1–5).

| # | Landing path:line | Class at `E` | Observed |
|---|---|---|---|
| 1 | `SKILL.md:1581-1584` | **swept** (executed) | Dated "Historical (round 14, runner `75ed934d…`)"; states both manifests return 2 at `--root .` and gives the archived-tree replay → 1. G1 reproduces exit 1 with exactly `producer_before` / `expected_contains_missing`; G6 reproduces the 2 at the live tree. Minor: the parenthetical says "the runner moved in round 16", but the observed runner at `E` is a newer move (`fb6d86d5…`, G12) — outcome unchanged |
| 2 | `SKILL.md:1585-1586` | **swept** (executed) | "The same command with `dispositions.json` → 0 … Live-tree form: the round-17 re-pin section." G2 exits 0 `clean`; G5 confirms the named live entry exits 0. The cross-reference resolves (`SKILL.md:1814-1853`) |
| 3 | `SKILL.md:1601` | **swept** | Row now reads "(historical; live entry since round 17: `.ufo/evidence/round-17/dispositions.json`)"; section heading is `### Round-14 historical registry — superseded by round 15`. The misleading live entry point is gone. Minor: the row's exit map still says only "invalid/missing/tampered inputs"; the moved-input cause is stated in step 2, not the row |
| 4 | `SKILL.md:1511-1513` | **swept** | "`SHONEN.md` box 3 **carried** a scope-bounded `[~]` **at round 12**, not `[ ]`" — dated, no present-tense claim. `SHONEN.md:10` now carries the full-page claim |
| 5 | `SKILL.md:1717-1719` + correction `:1863-1869` | **swept** (append-only supersession) | Flat invariant still stands as written; `:1867-1868` says exactly what wave-1 measured: "`### Round-15 gate/probe registry` grew from 30 to 31 lines. Both statements stay as written; this paragraph supersedes them." G10 confirms 30→31 and that the round-14 section stayed 34 |
| 6 | `SKILL.md:1798-1804` + correction `:1863-1866` | **swept** (append-only supersession) | "Every bucket … earns the box-3 lane assertion" stands, but `:1863-1866` names it ("the round-16 full-page assertion … was wrong at `09ee1d0` on one bucket … its recipe then exited 2") and supersedes it. The non-author closure (§2) and G9 agree |
| 7 | `SHONEN.md:10` + append `:11` | **swept** (append-only, as routed) | Line 11 appends "Correction (round 17, routed R16-C2c): … was wrong at 09ee1d0 on one bucket … its credit was sha-only … exited 2 instead of the recorded 1/0". Line 10 untouched. The appended link target is absent at `E` (see §4) |
| 8 | `SCORECARD.md:246` | **record** (dated) | Verbatim: "`--selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; … executable measurement6431478". Dated at 6431478; the live capability is restored by the round-17 manifests (G4/G5) and its live entry is `SKILL.md:1814-1853`. Residual minor drift: `--selftest` now prints **PASS (56/56)**, not 34/34 (G7). Not counted as a stale outcome |
| 9 | `SCORECARD.md:571` | **still stale** (F-r) | Still "box-3 full-page coverage 0/51 … → 54/54 buckets at the measured page sha `906fb649…`" and "calibration 6 → 8". Under the input-keyed rule the round-16 ledger yields `box3_full_page false`, **0/54 credited** at 09ee1d0 in the v2 measure (G9: 1 input-drift + 53 inputs-unrecorded), score **6**. The 54/54 is reproducible only by the superseded sha-only counter |
| 10 | `SCORECARD.md:586` | **still stale** | "calibration \| improved, 6 → 8 (pending non-author)". The non-author returned: `round-16-verifier-spotcheck.md:128` — "calibration \| unchanged \| C2's 6→8 does not hold at 09ee1d0 … the rubric score stays 6". No SCORECARD supersession block exists at `E` |
| 11 | `SCORECARD.md:588` | **still stale** | "operability \| unchanged \| … The round-14 disposition gate now exits 2 at `--root .` by design … archived-root form exits 0". The gate facts are true (G1/G2/G6), but the non-author graded the axis **harmed** (`spotcheck:129,134-155`: "That is a checklist item that no longer produces its stated outcome"). No supersession at `E`. (Round 17's re-pin restores the live verdict, G4/G5, but the round-16 row still asserts the false verdict) |
| 12 | `LOG.md:1036` | **still stale** | "C2 calibration 6→8: every bucket of SKILL.md was cold-read by lane seats" unchanged; no Round-17 LOG entry or errata. The read happened; the 8 does not hold (spotcheck:128; G8 score 6) |
| 13 | `LOG.md:1041-1042` | **still stale** (F-r) | "75 entries, 54/54 buckets of the measured page" unchanged. Entry count is true; the credit is not: v2 measure of that ledger is 0/54 (G9), and the spotcheck's own counterfactual is 53/54, `box3_full_page false` (spotcheck:115-117) |
| 14 | `LOG.md:1044` | **still stale** | "`--rev 09ee1d0` → cases 7, restraint 8, coldread 54/54" unchanged. v2 measure at 09ee1d0: score **6**, box3 false (G9); spotcheck:128 "rubric score stays 6" |
| 15 | `corpus/README.md:230-233` | **still stale at `E`** (partially addressed) | "the four 'full-page cold-read / box 3 open' sentences at lines 143-146, 160, 190 and 207 **are superseded** by … ledger.json" stands. The Round-17 append `:248-255` only narrows the *round-16 ledger's* standing ("was wrong at 09ee1d0 on the round-14 bucket … the round-17 ledger … replaces it"). At `E` the four sentences' content is still true: measure reports `ledger_present false`, box3 false, 0 covered (G8). Supersession becomes true only when the round-17 ledger lands [INFERENCE] |
| 16 | `corpus/lessons/round-16.md:6` | **record** (append-only) | "C2 calibration 6→8 (full-page cold-read …)" unchanged; no in-file errata block. Correctly not rewritten; the falsification is in `round-16-verifier-spotcheck.md` §2/§3 and `SKILL.md:1863-1869`. Residual: the lesson still states 6→8 with no local pointer to the spotcheck |
| 17 | `corpus/lessons/round-16.md:23` | **record** (append-only) | G6 "admit" row unchanged. Its literal reason ("every bucket … has a passing entry at its own section sha") is true of the v1 ledger; the **admit** is falsified by the spotcheck (`:165` "**disagree**"), which is the correct place for that judgement. No rewrite |
| 18 | `corpus/lessons/round-16.md:63` | **record** (append-only) | "Correct fail-closed behaviour. The registry row now names the archived-root invocation (`git archive 28aeef4` → exit 0)." The exit-0 half is true (G1/G2); the "Correct" judgement is superseded by the page's own round-17 rule, `SKILL.md:1828` — "'By design' names the mechanism; it never excuses the outcome" — and by the non-author operability verdict. Left as a dated record |
| 19 | `corpus/knowledge/incremental-pin-disposition.md:361-364` | **still stale** (minor) | "Read `.ufo/evidence/round-14/dispositions.json` …; exit1 alone does not make its FileNotFoundError the intended mechanism failure." Reading the file is still valid, but at `E` a live re-run of either round-14 form yields **2** (G6), not 1; no round-17 note covers this entry (the appended `ER-jj` at `:386` covers `HEAD`, not dispositions). The "exit1" framing needs the archived-tree qualifier |

## 3. Count

- **Swept: 7** — #1, #2, #3, #4, #5, #6, #7 (recipe steps 2–3 executed to their stated
  1/0; registry row dated historical + live entry; box-3 state dated; the two flat round-16
  invariants explicitly superseded by `SKILL.md:1863-1869`; SHONEN corrected append-only).
- **Record (append-only, correctly left): 4** — #8 (dated 6431478 capability demonstration;
  minor drift: selftest now 56/56), #16, #17, #18 (round-16 lesson rows left unrewritten;
  falsification lives in the spotcheck and the round-17 page).
- **Still stale active statements: 8** — #9, #10, #11 (SCORECARD round-16 score/axis rows),
  #12, #13, #14 (LOG round-16 outcomes), #15 (README "four sentences are superseded"),
  #19 (knowledge entry's live-tree exit-1 framing). The seven #9–#15 are the substantive
  ones; the non-author result they ignore is committed at `E` in
  `corpus/lessons/round-16-verifier-spotcheck.md:70-155`.

## 4. Adjacent findings

1. **The round-17 ledger is cited before it exists at `E`.** `git cat-file -e
   E:.ufo/evidence/round-17/coldread/ledger.json` → absent (G11); `measure.py --rev E`
   → `ledger_present: false`, `box3_full_page: false`, `sections_total: 58`,
   `sections_covered: 0`, score 6 (G8). Two committed links point at the absent file:
   `SHONEN.md:11` ("[round-17 input-keyed cold-read ledger](.ufo/evidence/round-17/coldread/ledger.json)")
   and `corpus/README.md:251-252` ("the round-17 ledger `.ufo/evidence/round-17/coldread/ledger.json`
   replaces it"). This is the round-16 "landing" mistake class
   (`corpus/lessons/round-16.md:61`: "cited … ledger.json before it existed") repeated at
   the wave-1 landing; it resolves only at the L1's ledger commit. Consequently the
   round-context claim "`measure.py --rev <landing>` → `box3_full_page true`, score 6 → 8"
   cannot hold at `E` as written: at `E` the measured page has 58 buckets and no ledger.
   The claim needs the ledger's landing rev named, or the ledger committed at `E`.
2. **The runner moved again in round 17.** `SKILL.md:1581` and `:1681` attribute the
   live-tree exit 2 to the round-16 runner move; at `E` the observed runner is
   `fb6d86d5…` (G12) against the pinned `75ed934d…` (G6), i.e. the round-17 guard/scrub
   edit. The exit-2 outcome and both replay instructions hold; only the parenthetical is
   incomplete.
3. **`SCORECARD.md:246` selftest count drifted.** The row quotes `PASS34/34`; at `E`
   `--selftest` prints `SELFTEST: PASS (56/56)` exit 0 (G7). Dated-capability records
   elsewhere in the table carry the same convention, so this is a pointer-drift note, not a
   false capability claim.

## 5. Verdict

**Partial — holds for the recipe, registry row and box-3/SHONEN corrections (7 items swept,
4 correctly-left records), but 8 stale active outcome statements remain at
`eb7838b16490ca7ba17ea3242ade76a61f744af2` (SCORECARD 571/586/588, LOG 1036/1041-1042/1044,
README 230-233, knowledge 361-364), and the round-17 ledger those pages link is absent at
that rev.**
