# R06Box3Correction — SHONEN box-3 appended correction (round 17, wave 1)

Seat `TameshiR17.R06Box3Correction` (reviewer, leaf). Lane root
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; measured tip
`98bea7da5801f4bc58e4187690ee1687c8a5061f` (branch `master`). Target: compare the
`SHONEN.md` box-3 text (`:9-10` at the tip) with
`corpus/lessons/round-16-verifier-spotcheck.md` §2 / §6 item 4 (R16-C2c), draft an
appended correction (never a rewrite of the existing evidence clause), and check how the
round-16 `measure.py` and command C parse SHONEN so the append keeps exactly 4 boxes and
the `~` mark.

No live lane file was edited. The draft was applied and parsed only in a fleet-mirror
clone under `/tmp/tameshi-r17w1-R06Box3Correction-YPjqVN/fleet/tameshi-shokunin`
(test commit `0cde5c3129c353d8f51e6a11dcad2a0400ebf4e7`, test-only, not in the lane).

## 1. Comparison: the box-3 claim vs the closure

`SHONEN.md:9-10` at the tip:

> `- [~] Instructions executable by an agent without oral context`
> `  [lane assertion, full page: round-16 cold-read of every SKILL.md bucket (preamble + every heading outside code fences) by lane-dispatched seats, instructions executed in /tmp, records re-anchored, wrong expectations repaired and re-read; ledger .ufo/evidence/round-16/coldread/ledger.json, counted by .ufo/evidence/round-16/measure.py; …](…)`

(abbreviated at the `…`; the full line is in §4 and is byte-unchanged by the draft.)

The closure says that sentence is false at the measured commit:

- `corpus/lessons/round-16-verifier-spotcheck.md:94-122` §2 "Why C2 still fails": the
  ledger credits a bucket by its section sha; a bucket whose bytes did not change keeps
  its wave-1 credit even when the surface its instructions run against moved. For
  `## Effective expectation reconciliation — round 14` that happened; the count would be
  `53/54`, `box3_full_page` false, score 6. "What fails is the full-page assertion, on
  one bucket the round itself made stale."
- `:128` (per-axis table): "The box-3 text overclaims by one bucket."
- `:231-233` §6 item 4 (R16-C2c): "the SHONEN box-3 line overclaims 'every bucket …
  wrong expectations repaired'. Correct it by appending, never by rewrite of evidence."

So exactly one bucket needs the correction, and the page plus SHONEN bytes are
unchanged from `09ee1d0` to `98bea7d`
(`git diff --stat 09ee1d0 98bea7d -- SKILL.md SHONEN.md` → empty), so the correction
written for the measured commit also applies at the tip.

## 2. Facts re-verified by execution (not taken from the closure)

All commands ran in the /tmp fleet-mirror clone. `git checkout` inside that clone is a
sandbox write; nothing was written in the lane.

| Fact | Command (rev) | Observed |
|---|---|---|
| Round-13 pin for the runner | `git show 98bea7d:.ufo/evidence/round-13/expected.json` | `"tools/mutate-and-run.sh": "75ed934d…19adc5"` (line 12) |
| Baseline runner equals the pin | `git show 28aeef4:tools/mutate-and-run.sh \| sha256sum` | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |
| Measured-rev runner moved | `git show 09ee1d0:tools/mutate-and-run.sh \| sha256sum` | `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa` |
| Recipe step 2 pre-round | at `28aeef4`: `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json` | `status=failed`, exit `1` |
| Recipe step 3 pre-round | at `28aeef4`: same with `dispositions.json` | `status=clean`, exit `0` |
| Recipe step 2 at measured rev | at `09ee1d0`: as above with `dispositions-before.json` | `id=expected_input_digest_mismatch`, `status=could_not_evaluate`, exit `2` |
| Recipe step 3 at measured rev | at `09ee1d0`: as above with `dispositions.json` | `id=expected_input_digest_mismatch`, `status=could_not_evaluate`, exit `2` |
| Same at tip | at `98bea7d`: both commands | both exit `2`, same id/status |
| No tool/evidence byte change 09ee1d0→98bea7d | `git diff --stat 09ee1d0 98bea7d -- tools/evidence-disposition.py .ufo/evidence/round-13/expected.json .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-14/dispositions-before.json` | empty |
| Bucket's ledger credit | round-16 ledger JSON at `98bea7d` | heading `## Effective expectation reconciliation — round 14`, `start=1563`, `end=1596`, seat `CR26`, snapshot `97cf436b…`, `verdict=gap-minor`, `commands_executed_count=4`, `wrong_expectations=0`; it is the only entry for that heading |
| What CR26 recorded | `.ufo/waves/round-16/w1/CR26.md:27-28` | step 2 exit `1`; step 3 exit `0` |
| Bucket line number at tip | `git show 98bea7d:SKILL.md \| grep -n 'Effective expectation reconciliation'` | `1563:## Effective expectation reconciliation — round 14` |

The gate's mismatch text names exactly the drift:
`tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`.
Thus the closure's `[INFERENCE]` ("step 2 takes the same path to exit 2") is now an
executed result: both recipe steps exit 2 at `09ee1d0`, not the recorded 1/0.

## 3. How command C and round-16 `measure.py` parse SHONEN

- **Command C** (`SCORECARD.md:75`) is
  `re.findall(r"^- \[([x~ ])\] ", text, re.M)` over the whole blob. It sees only
  **column-0** line starts of the form `- [x] `, `- [~] `, `- [ ] `. Continuation lines
  are invisible to it. An indented correction line cannot change `boxes`/`asserted`; a
  column-0 line beginning `- [~] ` would add a fifth box and fifth `~`.
- **Round-16 `measure.py`** (`.ufo/evidence/round-16/measure.py` at the tip):
  `BOX_RE = r'^- \[([x~ ])\] (.*)$'` (`:62`); `shonen_boxes()` (`:137-155`) attaches
  **following lines that start with a space or tab and are non-blank** to the preceding
  box as its block; a blank or non-indented line closes the block. `measure()` then uses
  `marks[2] == '~'` and `BOX3_LINK in boxes[2][1]`, with
  `BOX3_LINK = '.ufo/evidence/round-16/coldread/ledger.json'` (`:68`, `:286`).
- **Round-17 v2 contract** (interface C): `box3_link = SHONEN box-3 block contains
  '.ufo/evidence/round-17/coldread/ledger.json'`. When this seat checked, the v2
  `measure.py` was not in the tree (`.ufo/waves/round-17/staged/` held only
  `tools/mutate-and-run.sh` and `tools/pin-disposition.py`; no `measure.py`, no
  `ledger.json`). The v2 check below therefore uses the committed round-16
  `shonen_boxes` block extractor (the same continuation rule) plus the contract's
  substring test, executed read-only. The L1 must re-run the real v2 tool when X07
  lands.

Consequences for the draft: insert exactly **one** line between `SHONEN.md:10` and
`:11`, indent it with **two spaces** (so it joins the box-3 block), and start it with a
non-box token (`Correction…`). Do not append it after `:12`, and do not make it a
top-level `- [~]` bullet.

## 4. Exact draft (one insertion, zero deletions)

Placement: after `SHONEN.md:10` (the round-16 evidence line) and before
`:11` (`- [~] No cross-domain bleed…`). The file goes from 12 to 13 lines;
`git diff --numstat 98bea7d 0cde5c3 -- SHONEN.md` → `1	0	SHONEN.md`.

Exact inserted line — two leading spaces, no trailing whitespace (686 bytes without
newline / 687 with; sha256 `d3d74b3c49ffc0310eb8f60ab3259cefb8b5f7e74278649605517f3e9e5ec0ca`
without the newline, `c06f93f2a61be4f00191bd524dc4ecee3980a849df5fa5d1d3b16db8d346cac8`
with it):

```markdown
  Correction (round 17, R16-C2c): the round-16 full-page assertion above was wrong at 09ee1d0 on the round-14 bucket `## Effective expectation reconciliation — round 14` (SKILL.md:1563-1596). Its credit is sha-only: the credited read had `tools/mutate-and-run.sh` at `75ed934d…`, but at the measured rev that tool is `0673d2e5…`, so recipe steps 2-3 exit 2 `expected_input_digest_mismatch` instead of the recorded 1/0 and the bucket does not hold (corpus/lessons/round-16-verifier-spotcheck.md §2). Round 17's credit rule for executed entries requires recorded input digests, not section sha alone; ledger [round-17 cold-read ledger](.ufo/evidence/round-17/coldread/ledger.json).
```

Unified diff for the L1 (the two long evidence lines are byte-unchanged; only the `+`
line is new):

```diff
@@ -8,5 +8,6 @@ Promotion to shokunin requires all of:
   [lane assertion, no independent promotion verifier](reports/round-1-calibration.md#box-2)
 - [~] Instructions executable by an agent without oral context
   [lane assertion, full page: round-16 cold-read of every SKILL.md bucket (preamble + every heading outside code fences) by lane-dispatched seats, instructions executed in /tmp, records re-anchored, wrong expectations repaired and re-read; ledger .ufo/evidence/round-16/coldread/ledger.json, counted by .ufo/evidence/round-16/measure.py; supersedes the round-1 Appendix A + B-only scope (reports/round-1-kaika-coldread.md); no independent promotion verifier](.ufo/evidence/round-16/coldread/ledger.json)
+  Correction (round 17, R16-C2c): the round-16 full-page assertion above was wrong at 09ee1d0 on the round-14 bucket `## Effective expectation reconciliation — round 14` (SKILL.md:1563-1596). Its credit is sha-only: the credited read had `tools/mutate-and-run.sh` at `75ed934d…`, but at the measured rev that tool is `0673d2e5…`, so recipe steps 2-3 exit 2 `expected_input_digest_mismatch` instead of the recorded 1/0 and the bucket does not hold (corpus/lessons/round-16-verifier-spotcheck.md §2). Round 17's credit rule for executed entries requires recorded input digests, not section sha alone; ledger [round-17 cold-read ledger](.ufo/evidence/round-17/coldread/ledger.json).
 - [~] No cross-domain bleed (PROVINCE.md still accurate)
   [lane assertion, no independent promotion verifier; PROVINCE.md Core list corrected by append (tsukuroi and mado gates), fleet round 1](reports/round-1-calibration.md#box-4)
```

Apply this only when `.ufo/evidence/round-17/coldread/ledger.json` is committed at the
same rev (it does not exist at the tip; `W04QualityDraft.md` records that as in-flight).
Applying it before the ledger lands leaves the box-3 link dangling.

## 5. Parse check output

All on the test commit `0cde5c3129c353d8f51e6a11dcad2a0400ebf4e7`.

Command C, baseline at `98bea7d`:

```
boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
```

Command C, drafted SHONEN:

```
boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
```

Round-16 `measure.py`, `--rev 0cde5c3 --repo <clone>`, rc 0:

```
boxes 4 marks ['~', '~', '~', '~']
box3_marked True box3_ledger_link True box3_points True
coldread 54 54 box3_full_page True
calibration_restraint_score 8
```

(The v1 output stays score 8 with coverage 54/54 because that is exactly the sha-only
hole; the append does not break the v1 parser and does not rewrite the v1 clause.)

v2 contract block check (`shonen_boxes` from the committed round-16 `measure.py` +
the contract substring rule for `.ufo/evidence/round-17/coldread/ledger.json`):

```
boxes=4 marks=['~', '~', '~', '~'] block3_lines=3
v2_box3_block_has_r17_ledger=True
v1_box3_block_has_r16_ledger=True
```

Sensitivity controls on constructed bytes (same parsers), showing the two-space indent
is load-bearing:

```
dedented boxes=4 marks=['~', '~', '~', '~'] v2_box3_link=False
fifth-bullet boxes=5 marks=['~', '~', '~', '~', '~'] v2_box3_link=False
```

- `dedented` (correction at column 0): still 4 boxes, but the line falls out of the
  box-3 block, so the v2 ledger link is not seen.
- `fifth-bullet` (`- [~] Correction…` at column 0): command C and `measure.py` both see
  5 boxes / 5 `~`, and the block index shifts; both the "4 boxes" and the "mark `~`"
  conditions fail.

No trailing whitespace in the drafted file (`grep -n ' $'` → none).

## 6. Residual risk and notes

- The actual v2 `measure.py` did not exist when this seat checked. The v2 row above is a
  contract simulation over committed block semantics; it is not a run of the real
  instrument. `[INFERENCE]` that X07's implementation uses the same continuation rule
  (the contract's "box-3 block" plus the round-16 precedent). The L1 must re-run
  `python3 .ufo/evidence/round-17/measure.py --rev <tip> --ledger-file
  .ufo/evidence/round-17/coldread/ledger.json` (or `--ledger-rev`) and confirm
  `box3_link` and `boxes=4`.
- Wording follows `S16SrcStrace.md` §5 ("weaker, observed phrasing") and
  `W05ReadmeRows.md` ("a round-17 credit reading is only the output of measure.py …
  with the v2 ledger"). The line does not claim a new credit; it records that the
  round-16 assertion was wrong and points at the round-17 ledger. "Requires recorded
  input digests" applies to executed entries only, per the contract's
  `commands_executed_count>0` rule.
- `SKILL.md:1563-1596` is the bucket at the tip. `W03SkillR17Draft.md` appends its
  section at the end of SKILL.md, so those lines stay valid unless an earlier insertion
  lands; the heading name keeps the bucket identifiable if they shift.
- The mark is unchanged: box 3 stays `[~]`, a lane assertion. This correction is not a
  promotion and does not change the other three boxes.
- Live lane state: `git --no-optional-locks status --porcelain -- SHONEN.md` empty;
  `git diff --stat -- SHONEN.md` empty; working `SHONEN.md` sha256
  `4a11ade530ac802fa148bcd77661cb5c9447b0db099bf1d5532517560fadd26f` equals
  `98bea7d:SHONEN.md`. Only the report file above was written.

Verdict: **built** — exact one-line append drafted, no rewrite, and both known SHONEN
parsers hold `boxes=4` / `marks=['~','~','~','~']` on the drafted bytes; the round-17
box-3 link rule holds under the committed block extractor (real v2 run still owed by
the L1).
