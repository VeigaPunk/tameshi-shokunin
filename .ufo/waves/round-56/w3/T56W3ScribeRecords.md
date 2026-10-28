# T56W3ScribeRecords — round-56 closing SCORECARD block and LOG entry

- **seat:** T56W3ScribeRecords (scribe, leaf) · **L1:** `TameshiR56a3` · hyaku run 11, wave 3
- **lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin` · **PIN:** `2f5512a8ab0771fb2eee463ec16db359174f5edd` · **C0:** `c0137451f5b7f22d65f748fc69f1b181f55e1378` · **base:** `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` · **operative freeze:** `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1; original `c3e2ca9f020776b3d66c7af854fb82c834674fcf`)
- **writes:** this report and `.ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/`. No lane production file, frozen instrument, bound ledger, or git mutation was made by this seat. Scratch under `/fast/scratch/hyaku/tameshi-r56/T56W3ScribeRecords`, removed at exit.
- **tools installed or updated:** none.

## 0. Axes named

1. **Calibration** — the standing row. The number that may be written is the round-21 monitor's `calibration_restraint_score` at the commit the row names; the monitor is read at that commit, not inherited from the C0 text.
2. **Operability** — C2, the receipt-revision binding. Its numbers are the frozen counter's line and the gate's refusals, not any prose.
3. **Evidence hygiene** (the R55.x classes). Each disposition cites a receipt, or it says that there is none.

## 1. Verdicts on the inputs (what the texts depend on)

| # | Check | Result | Receipt |
|---|---|---|---|
| V1 | Monitor at base `981c5e8b` | `score=6`, `sections_covered=46/64`, `box3_full_page=False` | `T56W3ScribeRecords-receipts/monitor-scores.txt` line 1 |
| V2 | Monitor at `d33053f7` (the round-53 row commit) | `score=6`, `57/64`, `box3=False` | `monitor-scores.txt` line 2 |
| V3 | Monitor at C0 `c0137451` | `score=6`, `46/64`, `box3=False` — expected: the bind that adds `rekey-r56-*` is committed at `c1dd23b`, after C0 | `monitor-scores.txt` line 3 |
| V4 | Monitor at the bind commit `c1dd23b` | **`score=8`, `64/64`, `box3_full_page=True`, `box3_points=True`, marks `~~~~`** | `monitor-scores.txt` line 4 |
| V5 | Monitor at PIN `2f5512a` | **`score=8`, `64/64`, `box3_full_page=True`, `box3_points=True`, marks `~~~~`** | `monitor-scores.txt` line 5 |
| V6 | Standing row (`2f5512a` block, `SCORECARD.md` line 2718) asserts `8` at `c1dd23b3f83f` | **consistent with V4** (and V5) | this table |
| V7 | Ledger at PIN: entries with a `rekey-r56-` trace | 18; `read_rev` = `c0137451f5b7f22d65f748fc69f1b181f55e1378` for all 18; `(wrong_expectations, blocking_gaps)` = `(0, 0)` for all 18 | `git show 2f5512a8ab0771fb2eee463ec16db359174f5edd:.ufo/evidence/round-21/coldread/ledger.json`, parsed by a one-line `python3` filter over `entries` (609 entries total) |
| V8 | Rekey directories at PIN | exactly one, `rekey-r56-c0137451f5b7`, 19 files (18 `traces/section-NN.json` + `refresh-receipts.json`) | `git ls-tree -r --name-only 2f5512a… -- .ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7` |
| V9 | Census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | **exit 0**; `tameshi ok …/corpus/SOURCES.md`; 142 rows (`grep -cE '^ {0,3}\| S[0-9]{3} \|'` on PIN `corpus/SOURCES.md` = 142); 16 warnings (W04 duplicate-URL notices + one W01 notice), no errors | `T56W3ScribeRecords-receipts/census-validate.stdout`, `census-validate.stderr` |
| V10 | C1 before receipt | `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` — matches the contract | `git show 2f5512a…:.ufo/evidence/round-56/before/c1.stdout` |
| V11 | C2 before receipt | **`C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false`** — measured at the freeze, not at base | `git show 2f5512a…:.ufo/evidence/round-56/before/c2.stdout` |
| V12 | C2 base-revision receipt | `C2_R56: error=gate-missing total=1 C2_R56_PASS=false` | `git show 2f5512a…:.ufo/evidence/round-56/before/c2-at-base.stdout` |
| V13 | **Quoted C2 before total** | contract `contract.json` (C2 `before`) and PIN SCORECARD (`2f5512a` block, C2 row) both quote **`total=6`** and cite `before/c2.stdout`. That file reads **`total=2`**. No committed receipt carries `6` (`git grep -n 'total=6' 2f5512a… -- .ufo/evidence/round-56/before/` → empty). R55.2 class, in this round's own record. Corrected below; the frozen contract is not edited. | V11, V12 |
| V14 | After receipts | `.ufo/evidence/round-56/after/` exists and is **empty** at PIN; `.ufo/evidence/round-56/control/` holds only `frozen-surface.paths` — no official `controls-a.stdout` / `controls-b.stdout` | `git ls-tree -r --name-only 2f5512a… -- .ufo/evidence/round-56/after .ufo/evidence/round-56/control` |
| V15 | Freeze pointer | `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` resolves (`git cat-file -t` = commit, subject "round-56 amendment 1 …"); `freeze.json` `amendments` = one entry, `n=1`, `prior_freeze=c3e2ca9f…` | `git cat-file -t 21eb3c63…`; `.ufo/evidence/round-56/freeze.json` |

## 2. Lane tree state at check (not caused by this seat)

`git status --porcelain` in the lane at the time of check: **30 entries**, 20 tracked modified, 10 untracked. Full list: `T56W3ScribeRecords-receipts/dirty-tree-at-check.txt`.

- Tracked, modified: `ledger.json` (18 changed lines — the rekey-r56 `"L1 TameshiR56a3 re-key (round 56)"` label becomes `"L1 TameshiR56 re-key (round 56)"`), 18 `rekey-r56-c0137451f5b7/traces/section-NN.json` (argv paths made absolute; same label change), `corpus/lessons/round-56.md` (the `<L1 fills>` placeholders being filled in place).
- Their mtimes are 2026-10-28 17:50:20–17:50:41 −0300, **before this seat's first command (17:55)**. This seat only ran `.ufo/evidence/round-21/coldread/measure.py --rev <rev>` (reads git objects, `ledger_source=rev`) and wrote only to scratch and the receipts directory above.
- `deciding-run.sh:132` refuses any tracked change (`grep -vc "^?? ${OUT#$LANE/}/"` must be 0). The working tree as it stands would refuse the deciding run with `DECIDING_REFUSED dirty-tree`.
- The L1 has been messaged (`TameshiR56a3`, delivered).

## 3. The closing SCORECARD block (append after the `2f5512a` round-56 block)

```markdown

### Round 56 — measured close (calibration row restated; claim rows; deciding run pending)

Written by T56W3ScribeRecords (wave 3) from the receipts named in each cell. The
after cells read `pending deciding run` because no deciding invocation has run:
`.ufo/evidence/round-56/after/` is empty at PIN `2f5512a8ab07`. Nothing in this
block is a counter's after value.

#### Standing axis table — calibration at the monitor's own reading

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score=8` at the row's commit, with `sections_covered=64/64` and `box3_full_page=True` (`python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV`; receipt `.ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/monitor-scores.txt` line 4). The same command at PIN prints 8 at 64/64 (line 5). At C0 the monitor prints 6 at 46/64 because the bind is committed later, at `c1dd23b` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |

#### Claims — before, target, counting command, controls, after

| Claim | Before (receipt) | Target | Counting command | Frozen controls | After |
|---|---|---|---|---|---|
| **C1** calibration — bind the 18 base-lost headings at C0, restore 64/64 credit, restate the standing row to the monitor's reading: `C1_R56_PASS=true` | `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` (`.ufo/evidence/round-56/before/c1.stdout`) | `total=0`: precheck `lost=0 ok` (64 credited); monitor `64/64 score=8 box3=true` at the bound commit; one `rekey-r56-c0137451f5b7` with 18/18 headings at `read_rev=c0137451`; 18/18 reader reports; no LOG/SCORECARD inputs; standing row equal to the monitor at the commit it names | `python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `CTL_0_c1`, `CTL_SKIP_c1`, `CTL_FAB_c1`, `CTL_RESTATE_c1`, `CTL_POS_c1` (`controls.sh` phase A and B; **not yet run** at PIN) | pending deciding run (`.ufo/evidence/round-56/after/c1.stdout` absent at PIN) |
| **C2** operability — certify receipt revisions through `tools/receipt-revision-gate.py`, its documented rule, and the real refused receipts: `C2_R56_PASS=true` | `C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` (`.ufo/evidence/round-56/before/c2.stdout`, measured at the freeze). At base the counter reads `C2_R56: error=gate-missing total=1` (`before/c2-at-base.stdout`) | `total=0`; all selftests pass; three real red-before receipts refused with their named codes; own control receipts accepted at the certified revision; rule stated in QUALITY 107, sourced knowledge entry, SKILL `## Standing rules`, and a registry cell | `python3 .ufo/evidence/round-56/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `CTL_0_c2`, `CTL_SKIP_c2`, `CTL_FAB_c2`, `CTL_POS_c2` (**not yet run** at PIN) | pending deciding run (`.ufo/evidence/round-56/after/c2.stdout` absent at PIN) |

**Correction to the `2f5512a` block's C2 row.** That row and the contract quote
`total=6` against `before/c2.stdout`. The receipt reads `total=2` (the line above). The
receipt's bytes govern; the quoted `6` names no committed receipt and is withdrawn.

**What the counters cannot see.** C1: whether a reader read its section — a
`section_sha256` is computable from the tree without reading it, so a fabricated report
satisfies arm 4; the wave's adversarial seats and `CTL_FAB_c1` are the only guards. C2:
whether a receipt naming the certified revision was produced by the run it claims; a copied
`rev=` token passes the gate, and the digest sidecar narrows but does not close it.

**C2 is not admitted as a measured improvement.** Wave 2's do-nothing attack
(`.ufo/waves/round-56/w2/T56W2CritDoNothingC2.md`) shows the frozen counter printing
`C2_R56_PASS=true` from two hand-written stub receipts or a borrowed receipt with only its
`rev=` token rewritten — no controls run produced those bytes. The §9 no-op discriminator
therefore fails for C2. The counter line is recorded for transparency; admission needs an
independent producer-provenance condition, which this round does not have.

**Capabilities:** none claimed this round.

**Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
exit 0; 142 rows; no errors (`.ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/census-validate.stdout`).
```

## 4. The LOG entry (append after the round-55 entry)

```markdown

## 2026-10-28 — round 56, attempt 3 (close, before the deciding run)

L1 TameshiR56a3, hyaku run 11. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; content
commit C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`; content-final revision PIN
`2f5512a8ab0771fb2eee463ec16db359174f5edd`; operative freeze
`21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1 of
`c3e2ca9f020776b3d66c7af854fb82c834674fcf`; `.ufo/evidence/round-56/freeze.json`, one
amendment, `n=1`, before any control score or deciding invocation). Attempt 3 on the
inherited frozen contract; claims, targets, counters and arms are unchanged.

**Claims.**
- **C1 calibration** (the lowest non-retired axis, 8): the cold-read floor and the standing
  row. Before: `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18
  readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`
  (`.ufo/evidence/round-56/before/c1.stdout`). After: pending deciding run
  (`.ufo/evidence/round-56/after/c1.stdout` absent at PIN).
- **C2 operability** (receipt-revision binding): before `C2_R56: rev=c3e2ca9f0207 …
  total=2 C2_R56_PASS=false` (`.ufo/evidence/round-56/before/c2.stdout`, measured at the
  freeze; base reads `error=gate-missing total=1`, `before/c2-at-base.stdout`). After:
  pending deciding run. The `total=6` quoted in the contract and the C2 row of the
  `2f5512a` block names no receipt and is withdrawn (R55.2 class, found this round).

**Landed changes** (`git log 981c5e8b..2f5512a8`, oldest first):
- `c3e2ca9f` — freeze the claim instruments (contract, both counters, receipt-revision gate, controls, no-harm, deciding run).
- `21eb3c63` — amendment 1 (operative freeze): counters/controls/deciding/gate repaired from wave-1 findings — index bug in the C2 docs arm, `clone_rev=` relabel for clone-local commits, `.sha256` sidecars, frozen surface, 19-case gate suite.
- `c0137451` (C0) — receipt-binding rule in SKILL `## Standing rules`; QUALITY criterion 107; knowledge entry `receipt-revision-binding`; SOURCES S281 (admitted) and S282 (rejected, retained); lesson `round-56`; registry cell; `before/` receipts; assimilation and census-start evidence.
- `63fb53a` — reader-finding adjudications (gap-minor, deferred); lesson records F1 (anchor drift) and R1 (SKILL byte-identity gap); seven missing reader reports committed.
- `be7cf96` — lesson records F2 (Standing-rules role→code mapping) and the round-57 repair scope.
- `877eede` — integrate wave-one and wave-two evidence.
- `c1dd23b` — bind the 18 cold-read headings at C0: `.ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/` (18 traces, `read_rev=C0`, `wrong_expectations=0`, `blocking_gaps=0`); `ledger.json` +18 entries.
- `2f5512a` (PIN) — round-56 SCORECARD block (spec-stage, with the standing row at `c1dd23b`).

**Calibration, measured.** `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev <rev>`
(receipts `.ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/monitor-scores.txt`):

| rev | score | sections covered | box 3 full page |
|---|---|---|---|
| base `981c5e8b` | 6 | 46/64 | False |
| `d33053f7` (round-53 row) | 6 | 57/64 | False |
| C0 `c0137451` (bind not yet committed) | 6 | 46/64 | False |
| `c1dd23b` (bind commit; row's measured commit) | **8** | **64/64** | **True** |
| PIN `2f5512a` | **8** | **64/64** | **True** |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exit 0, 142 rows, no errors (`.ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/census-validate.stdout`).

**Controls.** Not run at PIN. `.ufo/evidence/round-56/control/` holds only `frozen-surface.paths`; there is no official `controls-a.stdout` or `controls-b.stdout`. The `T56W3ExecControls{A,B}-receipts/` files in the wave directory are seat dry runs and are not inputs to the deciding run. The bootstrap pass (`controls.sh` phase A, then phase B at PIN) is still owed.

**Round-55 routed defects (R55.1–R55.7) — dispositions.** The source is `corpus/lessons/round-55-verifier-spotcheck.md`. Each row cites the receipt that decides it.

| id | disposition | receipt / reason |
|---|---|---|
| R55.1 — no C2 verdict at the measured revision | **fixed in code; carrier pending** — deciding-run gate 0c runs `tools/receipt-revision-gate.py --certified REV` on the verdicts the run produces | `deciding-run.sh` gate 0c; `after/receipt-gate-verdicts.stdout` not yet produced |
| R55.2 — a quoted total its own receipt contradicts | **carried** — no instrument checks quoted bytes. Recurred in this round's own record: `total=6` quoted against `before/c2.stdout` (`total=2`) | `corpus/QUALITY.md` 107 scope sentence; V13 in the wave-3 scribe report |
| R55.3 — instrument regressed, row still asserts 8 | **fixed by C1, pending the counter's after** — the monitor reads 8 at `c1dd23b` and PIN (64/64, box 3) | `monitor-scores.txt` lines 4–5; `after/c1.stdout` pending |
| R55.4 — stale control sentence ("still running at filing") | **carried** — the lesson's "FIXED by construction" is narrowed: the deciding script checks verdict-line presence, not report prose, and no instrument reads prose | `deciding-run.sh` (`control-receipt-missing`, `controls-*-verdict-missing`); wave-1 finding F2 (`T56W1RevRound55Dispositions.md`) |
| R55.5 — deciding gate cannot compare the revision it certifies | **fixed in code; blocked on the official control receipts** — gate 0b (controls) and 0c (verdicts); amendment 1(b) relabels clone-local commits `clone_rev=` so a mutation control's `rev=` names a lane revision. Acceptance of the official control receipt by the gate is not yet demonstrated | `21eb3c63` (`controls.sh` `emit()`); `tools/receipt-revision-gate.py`; `after/receipt-gate.stdout` pending |
| R55.6 — uncommitted round work at closure | **carried; recurred in this run** — at the check the lane held 30 entries (20 tracked modified incl. `ledger.json`, 18 rekey traces, `corpus/lessons/round-56.md`) | `T56W3ScribeRecords-receipts/dirty-tree-at-check.txt`; `deciding-run.sh:132` refuses |
| R55.7 — closure-environment contamination | **carried** — wave-3 seats write into the lane tree (`w3/T56W3ExecControls{A,B}-receipts`, the untracked `w3/` directory) | `git status` at check (same receipt) |

**Known limits (stated, not closed).** C1 cannot see a fabricated reader report (`CTL_FAB_c1`
is the guard); C2 cannot tell a produced receipt from a copied `rev=` token (gate digest
sidecar narrows it). C2 is not admitted as a measured improvement (wave-2 do-nothing attack).

**Evidence:** `.ufo/evidence/round-56/` (contract, freeze, counters, controls, before),
`.ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/`,
`.ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/`; deciding receipts to follow under
`.ufo/evidence/round-56/after/`.
```

## 5. Findings for the L1 (blocking before the deciding run)

1. **Dirty bound ledger — detected at check, L1-reported resolved (not re-verified by this seat).** At this seat's check the tree had `ledger.json` (18 lines), the 18 rekey traces and `corpus/lessons/round-56.md` modified (mtimes 17:50:20–41, before this seat's first command). The L1 reports that the modification came from its own validation rerun (default label and absolute argv), that it reran the binder with the committed arguments, and that `git diff c1dd23b... -- ledger.json rekey-r56-c0137451f5b7` is empty (`BIND_TREE_MATCH=1`). Retained as a detection record. The deciding-run dirty-tree gate (`deciding-run.sh:132`) must still see a clean tree at the deciding moment.
2. **C2 before quote (blocking the record, not the counter).** Contract and PIN SCORECARD quote `total=6` against `before/c2.stdout`; the receipt says `total=2`. The SCORECARD block above withdraws the quote. The lesson's round-56 `## Mistakes` and any LOG line citing `total=6` must be corrected to `total=2` (or cite `c2-at-base.stdout`).
3. **Controls not yet run.** No official `controls-a/b.stdout` exists. Bootstrap: run `controls.sh` phase A at PIN, commit its real stdout as the first-pass input, then rerun at the resulting PIN. Only the second run feeds the deciding run. Do not hand-write these.
4. **R55.4 disposition.** The lesson's "FIXED by construction" row overclaims (wave-1 F2). The LOG above says **carried**. The lesson row should be aligned with the LOG.
5. **C2 do-nothing limitation (carried, not fixed).** The LOG and SCORECARD state it; the counter cannot be changed post-data. Any "C2 PASS" line is not admission evidence.
6. **Monitor timing.** Each monitor run takes 60–100 s. The deciding run's no-harm set should budget for it; the monitor output (3 MB JSON) is not committed, only the extracted fields in `monitor-scores.txt`.

## 6. Reproduction (the deciding run re-derives these)

```
# monitor (run from any scratch dir; prints one JSON document; ~60-100 s each)
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <rev>
#   <rev> = 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 | d33053f7552d | c0137451f5b7f22d65f748fc69f1b181f55e1378 | c1dd23b3f83f5dff676c4a4482498e87345375ef | 2f5512a8ab0771fb2eee463ec16db359174f5edd
#   fields read: calibration_restraint_score, coldread.sections_covered, coldread.box3_full_page, shonen.box3_points, shonen.marks
#   extracted lines: .ufo/waves/round-56/w3/T56W3ScribeRecords-receipts/monitor-scores.txt

# census (exit 0 expected)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi; echo "exit=$?"

# before receipts and rekey shape at PIN
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2f5512a8ab0771fb2eee463ec16db359174f5edd:.ufo/evidence/round-56/before/c2.stdout
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -d --name-only 2f5512a8ab0771fb2eee463ec16db359174f5edd -- .ufo/evidence/round-21/coldread/ | grep rekey-r56
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -t 21eb3c63cd0f3190c0deeb8953c6c91c7742cd68
```

## 7. Scratch

`/fast/scratch/hyaku/tameshi-r56/T56W3ScribeRecords` held the 3 MB monitor JSON files and the census capture. Removed at the end of this seat. The committed receipts above are copies of the extracted values.
