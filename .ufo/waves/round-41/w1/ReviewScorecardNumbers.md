# ReviewScorecardNumbers — round 41, wave 1

Seat: `L1Tameshi41.ReviewScorecardNumbers` (reviewer, axis calibration). Read-only on the lane;
the only lane write is this report. No counter was run in default/`--rev <round-tip>` mode.
Tooling: nothing installed or upgraded (no pacman transaction attempted; host guard respected).

Artefact audited: `ScribeScorecard.md`, 180 lines, untracked,
sha256 `92f33f5a5f3d4e108c62a591fee5732d972d3b04dda7eac169c5c7860b6244c4`. Verdicts are taken
against **committed blobs**, never the moving working tree
(`git show <rev>:<path>`), because peers were writing `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`corpus/README.md`, `SCORECARD.md` and the contract during this review. The lane advanced
`d4ee4e6` → `b37ce97` mid-review; both revs are checked where they differ.

## Verdict table

| # | Number in the draft | Verdict | Command run and result |
|---|---|---|---|
| 1 | registry **107** rows (base `a3d6c69` / freeze `d4ee4e6`) | **AGREE** | `git show a3d6c69:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} \|'` → `107`; same command at `d4ee4e6` → `107`; the C1 counter's own field agrees: `.ufo/evidence/round-41/before/c1-at-base.stdout` → `sources_rows=107 rev=a3d6c690…`, exit 1 (`before/c1-at-base.exit` = `1`). The draft's companion claim "109 at the round commit" is also right: `git show b37ce97:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} \|'` → `109`. |
| 2 | statuses **79 mined / 22 queued / 6 rejected** (base/freeze) | **AGREE** | Parse of the committed blob (status column: index 7 after stripping the outer pipes, index 8 under the counter's raw `split('|')`, per amendment A1) at `a3d6c69` and at `d4ee4e6`: `{'mined': 79, 'queued': 22, 'rejected': 6}` (sum 107). At the round commit `b37ce97`: `{'mined': 81, 'queued': 22, 'rejected': 6}` (monitor `sources` block, see row 5 command), matching the draft's "81/22/6 at tree". |
| 3 | max id **S152** (base/freeze) | **AGREE** | `git show d4ee4e6:corpus/SOURCES.md \| grep -oE '^\| S[0-9]{3}' \| sort -u \| tail -1` → `\| S152`; at `b37ce97` → `\| S154`, matching the draft's "max id S154 at tree" and `corpus/lessons/round-41.md:42` ("109 (`S001` through `S154`)"). |
| 4 | **depth 9** | **AGREE** | Command D (`SCORECARD.md:72-73`) at `a3d6c69`, `d4ee4e6` and `b37ce97` → `recorded_cases=9 depth_score=9`; criterion row `SCORECARD.md:1536`. Independent: the coldread monitor's `depth_score` is `9` at `a3d6c69` and at `b37ce97`. |
| 5 | **calibration 8** | **DISAGREE** | Criterion `SCORECARD.md:1537` defines the numeric calibration score as `calibration_restraint_score` from `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV`. At `a3d6c69` → `6` (`sections_covered 60/64`, `box3_full_page false`, `shonen.box3_points false`); at `b37ce97` → `6`; at `5641ed84` (round-40's own measured rev) → `6`; at `e118024` (round 38) → `6`. It was `8` only at `ae9b771` (round 37) and in the committed round-36 receipt `.ufo/evidence/round-36/after/monitor-at-b455001e.stdout:2`. The draft's support — command C at `a3d6c69` → `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8` — is reproduced exactly, but `SCORECARD.md:74` labels that command "mark census only; this upper bound awards no evidence/authority credit", and `:1537` grants box 3's two points only "when the monitor credits the full page" (it does not: 60/64). So 8 is an upper bound, not the score; the value at base and at the round commit is 6. |
| 6 | **SHONEN boxes=4 checked=0 asserted=4** | **AGREE** | `git show d4ee4e6:SHONEN.md \| grep -cE '^- \[~\]'` → `4`; `… \| grep -cE '^- \[x\]'` → `0`; command C prints `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`; monitor `shonen` block at `b37ce97` → `{'boxes': 4, 'checked': 0, 'asserted': 4, 'untouched': 0, 'marks': ['~','~','~','~'], 'box3_points': False}`. |
| 7 | **v2 sha `40228532…`** | **AGREE** | `git show b37ce97:tools/write-path-census-v2.py \| sha256sum` → `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b`; equals the contract field `claims.C2.v2_sha256` and the C2 receipt's `v2_sha_ok=1` (`.ufo/evidence/round-41/after/c2-at-b37ce…stdout`). |
| 8 | **v3 sha `095924a7…`** | **AGREE** | `git show b37ce97:tools/write-path-census-v3.py \| sha256sum` → `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279`; equals `claims.C2.tool_sha256` and the C2 receipt's `tool_sha_ok=1`. |

Seven of eight agree. The single disagreement is calibration, and it is the axis this round
claims to move.

## Findings

**F1 (high) — `calibration 8` is not re-derivable and the draft states it as the axis value.**
The draft's headline sentence "Calibration 8 is the lowest non-retired axis and carries C1" and
its "**calibration 8 → 8**" both assert 8. Under the criterion's own command the value is **6** at
`a3d6c69` and at `b37ce97`; it was 8 last at `ae9b771` (round 37) and the committed round-36
receipt. Four sections are uncredited with reason `input-drift:` on `LOG.md`, `SCORECARD.md`,
`corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `tools/mutate-and-run.sh` — all
in-repo edits made in rounds 37–40. The lane has therefore carried an unimplemented 8 for three
rounds; round 40's `SCORECARD.md:1891` "calibration 8 → 8" is already false at its own measured
rev (`5641ed84` → 6). Required in the round-41 block: either `6 → 6` (the re-derivable reading) or
"last measured 8 at `b455001e`; 6 at this revision", never a bare `8 → 8`. The claim's *placement*
is unaffected (calibration 6 is still the lowest non-retired axis), so C1 need not move axes.

**F2 (high) — the draft's paste-ready "After" cells would ship a number contradicted by a receipt
in the same tree.** The block writes `NOT-YET-MEASURED` for both After cells. That is honest at
draft time, but the L1's own rev-mode run now exists: `.ufo/evidence/round-41/after/c1-at-b37ce974…stdout`
reads `C1_R41: m6=0 m7=0 m8=1 m9=0 total=1 records=3 sources_rows=109 rev=b37ce97… C1_R41_PASS=false`,
exit `1`, with `MISMATCH m8 .ufo/waves/round-41/w1/swarm-registry.json cited but does not resolve`.
The commit's `SCORECARD.md:1909` still prints the *target* `total=0 … C1_R41_PASS=true` in the After
cell and points at an "after subsection" that does not exist (`git show b37ce97:SCORECARD.md | grep -c 'after subsection'` → `2`, both cells; file is 1937 lines, block at 1895–1934). The draft *predicted* this exact hazard ("Work-mode green ≠ rev-mode green … or m8 fires on them") — the prediction is confirmed by the receipt. If the block is pasted unchanged, the After cell contradicts the receipt already on disk. Either commit `.ufo/waves/round-41/w1/` (including this draft, which is `??` untracked — a record citing it trips the same m8 class) or write the After cell as `m8=1 … C1_R41_PASS=false` with that receipt path.

**F3 (medium) — the draft's own live-block defects are accurate; two of the three are number
defects and both reproduce.** Contract amendment list at `b37ce97`:
`[a['id'] for a in json.load(git show b37ce97:.ufo/evidence/round-41/contract.json)['amendments']]`
→ `['A1','A2','A3','A4']`, so the block's "three pre-data amendments" (`SCORECARD.md:1903-1905`)
undercounts by one. `SCORECARD.md:1918-1919` claims command D prints 9 at "base and at the round
commit" — the round-commit read is now true (verified in row 4) but was unmeasured when the block
was committed.

**F4 (medium) — the draft's "Numbers re-checked (agree)" line bundles the one disagreeing number
into the agree list.** It reads "… calibration `boxes=4 checked=0 asserted=4 untouched=0
asserted_mark_upper_bound=8` (command C at base)". Command C is the mark census, not the
calibration criterion (`SCORECARD.md:74-75` vs `:1537`); listing it beside v2/v3 shas and depth
hides that calibration is the one number that does not derive. Split the two instruments.

**F5 (low) — the stale C1 counter pin the draft reports is real and unchanged at `b37ce97`.** Contract
`claims.C1.counter_sha256` = `8bc9b4221c59…`; the committed counter hashes to
`9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd`
(`git show b37ce97:.ufo/evidence/round-41/calibration/measure.py | sha256sum`), same as the
working file. A4's *code* is present in that blob (`os.path.exists` at `:113`, `.rstrip('/')` at
`:185`), so the amendment is implemented; only the pin is wrong. C1 does not verify its own sha,
so no predicate fails — the draft states this correctly.

## Residual risk and verification gaps

- I did not run either C1/C2 counter in default mode at any round-41 revision. The only instrument
  I ran was the **coldread monitor** (`round-21/coldread/measure.py`, not a contract counter), at
  `a3d6c69`, `b455001e`, `ae9b771`, `e118024`, `5641ed84` and `b37ce97`, inside a `/tmp` clone
  (`/tmp/tameshi-r41-reviewscore/`), exit 0 each, 28–90 s. Its only write path
  (`round-21/coldread/measure.py:48`) is inside `selftest()`'s temporary directory; the measured
  path is stdout-only. The `b455001e` run reproduces the committed round-36 receipt byte-for-byte
  on the scored fields (8 / 64/64 / box3 true), which is the control for this method.
- If the lane's convention is "numeric calibration = last measured value, held", then 8 is a
  defensible *held* number — but the block then owes the qualifier ("last measured at `b455001e`")
  and still cannot use `asserted_mark_upper_bound=8`, because box 3's credit is negative at every
  rev from `e118024` onward. As written, the sentence "calibration 8 → 8 … no SHONEN box moved"
  reads as a measurement and is not one.
- The working tree moved under this review and at one point carried 109 registry rows with the
  contract's counter pins edited in place; every verdict above is pinned to a `git show` blob.
  Nothing here should be read from the live files alone.
- Out of scope, untouched: C1/C2 predicate internals, the census tool's classifier, the round-40
  quarantine table, and the source-row content of S153/S154 (owned by `ReviewSourceRows`).

Report: .ufo/waves/round-41/w1/ReviewScorecardNumbers.md
