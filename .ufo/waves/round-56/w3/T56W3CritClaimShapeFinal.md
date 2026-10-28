# T56W3CritClaimShapeFinal — final claim-shape audit at PIN

Seat: T56W3CritClaimShapeFinal (critic, leaf, no dispatch). L1: TameshiR56a3.
Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`;
frozen instruments `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68`; C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`;
PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd`.
Scratch (deleted on exit): `/fast/scratch/hyaku/tameshi-r56/T56W3CritClaimShapeFinal/`.
Tools installed: none. Lane files written: this report only. Fixtures were scratch commits in
`git clone --shared` copies; `git -C <fixture> rev-parse --show-toplevel` asserted before each commit.

## Summary

| item | verdict | one-line reason |
|---|---|---|
| (a) one value, one command, both verdict lines quoted | PASS on shape / both targets **unmet at PIN** | C1 `total=1` (arm 6), C2 `total=1` (arm 5) |
| (b) universal clauses have enumerators | **FAIL** | "every receipt a round certifies" (QUALITY 107, knowledge note, counter docstring) and "all selftests pass" (SCORECARD) are not enumerated by any command |
| (c) lowest non-retired axis | PASS (calibration 8 < freshness 9 < depth 10) | calibration sits at the monitor's ceiling; freshness denominator in SCORECARD is stale (73 vs 74) |
| (d) do-nothing controls cannot reach targets | C1 **PASS**; C2 **FAIL** | C1 skips total 5/5/5/5/6; C2 stub and borrowed receipts reach `C2_R56_PASS=true` on the live counter |
| (e) C1 and C2 causally separable | **FAIL (one direction)** | C2 verdict invariant to C1 tree; C1 verdict is NOT invariant to C2's corpus bytes (13 of 18 headings drop) |
| (f) a claim cites an S-row opened this round | PASS | S281 opened 2026-10-28, `mined`, cited by the C2 knowledge note; census exit 0 |

Measured verdicts at PIN, both FALSE. Neither claim may be presented as admitted.

## Re-derived commands and verdict lines (PIN)

Counters (run from a clean `--shared` clone at PIN for the monitor and freshness; the counters ran against the lane at PIN with `--work` empty):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work <empty dir> --explain
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work <empty dir> --explain
```

C1 at PIN (exit 1):
```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=2f5512a8ab07 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
EXPLAIN arm3-rekey dirs=['rekey-r56-c0137451f5b7'] c0=c0137451f5b7f22d65f748fc69f1b181f55e1378
EXPLAIN arm4-readers 18/18
EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='Round-21 cold-read monitor `calibration_restraint_score`; tw' round='56'
C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false
```
C2 at PIN (exit 1):
```
EXPLAIN arm1-selftest exit=0 19/19
EXPLAIN arm2-red54 exit=3 codes=RECEIPT_REV_CONTENT_DRIFT old-gate-accepted=True
EXPLAIN arm3-red54b exit=3 codes=RECEIPT_REV_UNRESOLVABLE
EXPLAIN arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT
EXPLAIN arm6-docs 4/4
C2_R56: rev=2f5512a8ab07 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false
```

**(a)** Each target is a single value (`total=0`) that one command re-derives over committed bytes (`git show REV:...` throughout). Shape passes. Measured at PIN: C1 fails on arm 6 alone; C2 fails on arm 5 alone (`own-receipts-missing`, the expected bootstrap state: `.ufo/evidence/round-56/control/controls-{a,b}.stdout` are not committed at PIN). Both targets are unmet.

**C1 failing arm, and why it is a letter-case miss.** Arm 6 tests `'round-21' in cells[2]`. The committed row reads `Round-21 cold-read monitor` (capital R). Verified:
```
python3 (replica of arm 6 on the PIN row): 'round-21' in cells[2] = False | 'Round-21' in cells[2] = True
re.search(r'\b56\b', cells[4]) = True '56'   (row: calibration | 8 | Round-21 ... | c1dd23b3f83f5dff676c4a4482498e87345375ef | 56)
```
Scratch fixture `fx-case` (PIN with that one row's `Round-21` changed to `round-21`, `git diff --stat` = `1 file changed, 1 insertion(+), 1 deletion(-)`) gives:
```
C1_R56: rev=93f039795558 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
exit=0
```
So arm 6 is the only failing arm at PIN. Under the kill rule the measured verdict stays `C1_R56_PASS=false`. A post-data edit to the row is a new revision, a post-data rule change, and an L1 decision. The shape of the fix, if L1 adopts it, is in the diff below. The frozen counter was not changed and no seat may narrow the target.

```diff
--- SCORECARD.md (round-56 standing row, line 2718)
-| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points ...
+| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points ...
```

**(b) FAIL — universal clauses without an enumerating command.** Sweep: contract `claims.{C1,C2}.{before,target,kill_rule,cannot_see,counter}`; SCORECARD round-56 section (lines 2704-end); `corpus/QUALITY.md:1612-1626` (criterion 107); `corpus/knowledge/receipt-revision-binding.md`; `corpus/lessons/round-56.md` (R55.2 row); both counter docstrings. Command: `python3` regex sweep for `\b(all|every|each|complete|anywhere|always|never|any|no|none|full|entire)\b` on the contract and `grep -o -i -E` on the other records.

| universal clause | where | enumerator | result |
|---|---|---|---|
| "every receipt a round certifies — a control, a positive control or a verdict — states ... and the lane's certification path runs `tools/receipt-revision-gate.py` over it" | `corpus/QUALITY.md:1618-1619` | none. `c2/measure.py` checks exactly five receipts (red54 slice, red54b, red55, own a/b). It does not enumerate the round's certified set and does not check that `deciding-run.sh` runs the gate (gates 0b/0c only cover its own control and verdict outputs) | **unenumerated** |
| same claim, in the counter docstring: "every receipt the lane certifies is bound to the revision it was measured against" | `c2/measure.py:2-3` | same as above | **unenumerated** |
| same claim, in knowledge note: "every receipt a round certifies carries in its own bytes the revision" | `corpus/knowledge/receipt-revision-binding.md:20` | same as above | **unenumerated** |
| "all selftests pass" | SCORECARD round-56 C2 row (`total=0; all selftests pass`) | arm 1 runs one suite (the gate's `--selftest`), so the claim is wider than the enumeration | **overreach** |
| "every value this round's records quote names the committed receipt that carries it" | `corpus/lessons/round-56.md` R55.2 | the lesson itself says "no instrument can fail it" | **self-declared unenforced** |
| "the gate's selftest passes every case" | C2 target | arm 1 requires `N/N` | enumerated, OK |
| "for EVERY heading frozen"; "18/18 reader reports"; "exactly one rekey dir"; "no bound entry pinning LOG.md or SCORECARD.md"; "the standing row" | C1 target | arms 3, 4, 5, 6 enumerate the frozen 18, the readers, the `ls-tree` dir set, the bound entries, the last row | enumerated, OK |
| "any arm short of its denominator" | C1 and C2 kill rules | every arm carries its denominator | enumerated, OK |

Fix requested: the QUALITY 107 / knowledge / docstring sentence must either be narrowed to the five receipts the counter enumerates, or the counter must enumerate the round's certified set (after the frozen-instrument freeze that is a post-data change, so narrowing the prose is the honest option). The SCORECARD "all selftests pass" should read "the gate's selftest passes".

**(c) PASS — calibration remains the lowest non-retired axis.** SCORECARD carries three numeric standing axes (depth, calibration, freshness); `Retired: none` is recorded in the baseline table. Re-derived at PIN:

```
# D (command D, SCORECARD.md:72-73, run on the PIN bytes of tools/mutate-and-run.sh)
recorded_cases=10 depth_score=10
# calibration (round-21 monitor, python3 .ufo/evidence/round-21/coldread/measure.py --repo <clean clone at PIN> --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd)
{'calibration_restraint_score': 8, 'depth_score': 10, 'ledger_committed': True, ... 'recorded_cases': 10, ...}
{'box3_full_page': True, 'inputs_overlay_merged': 0, 'ledger_present': True, 'sections_covered': 64, 'sections_total': 64}
# freshness (round-45, python3 .ufo/evidence/round-45/freshness/measure.py --lane <clean clone at PIN> --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd)
DISPUTED S048
DISPUTED S093
C1_R45: self_pin=1 population=74 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=2f5512a8ab0771fb2eee463ec16db359174f5edd C1_R45_PASS=true
```
Ranking: calibration 8 < freshness 9 < depth 10. Calibration is still the lowest. Two caveats, neither changing the ranking:
- Calibration 8 is the monitor's **ceiling** (SCORECARD: "8 is that monitor's ceiling"; last 2 points need independent promotion review). This round's C1 is a restoration from the monitor's base reading of 6, not a raise; no further calibration move is available to this monitor.
- Freshness denominator is stale. SCORECARD states `floor(10 * fresh / 73)`; the counter's population is **74 at base, C0 and PIN** (`population(parse_rows(SOURCES.md))`). Score is 9 under both. The missing ledger row is **S022** (population row with no round-45 entry); it is in the denominator but no printed category (`unreviewed`, `unreachable`, `invalid`) reports it. This is an uncounted row, not a score change.

**(d)** Controls.
- Official `controls.sh` outputs are not committed at PIN (`git ls-tree -r PIN .ufo/evidence/round-56/control` lists only `frozen-surface.paths`). No official CTL score exists at PIN.
- C1 do-nothing evidence (wave 2, committed receipts at mutated trees, `.ufo/waves/round-56/w2/T56W2CritDoNothingC1.md:36-40`): ctrl1 (delete 18 headings' entries) `total=5`; ctrl2 (restate row only) `restate=6 total=5`; ctrl3 (re-pin one entry, no readers) `rekeyed=0/18 readers=0/18 total=5`; ctrl4 (empty rekey dir) `total=5`; ctrl5 (strongest fake, 295 entries rebound) `rekeyed=2/18 readers=0/18 unstable=10 total=6`. Trivial do-nothing (C0 itself): `C1_R56: rev=c0137451f5b7 ... total=5 C1_R56_PASS=false` (`.ufo/waves/round-56/w2/T56W2CritDoNothingC1-receipts/control.out`). **C1: none reaches PASS.** (Fabricated-reader attacks are another seat's item.)
- C2 do-nothing evidence (wave 2, `T56W2CritDoNothingC2.md`, rows v1-v6, live amended counter): v1 docs-only `own=own-receipts-missing docs=4/4 total=1 ... false`; **v2 two 79-byte stubs** `own=PASS docs=4/4 total=0 C2_R56_PASS=true` at `38895e5c3096`; **v3 borrowed slice (round-54 CTL_POS_c1, one `rev=` rewritten)** `own=PASS docs=4/4 total=0 C2_R56_PASS=true` at `b60a76ff7ca8`. The verdict lines are in `.ufo/waves/round-56/w2/T56W2CritDoNothingC2-receipts/v2-stub-receipts.stdout:16` and `v3-rewritten-slice.stdout:14`. **C2: a do-nothing tree reaches the target.** The do-nothing test fails; the measured PIN verdict cannot be presented as admission evidence.

**(e) FAIL in one direction — the two claims are not causally separable.** Two trees, both scratch commits on top of PIN, each measured with both counters:

| tree | construction | C1 verdict line | C2 verdict line |
|---|---|---|---|
| PIN | none | `credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1` | `own=own-receipts-missing docs=4/4 total=1` |
| fx-t1 (C1 state reverted) | `SCORECARD.md`, `.ufo/evidence/round-21/coldread/ledger.json` and the `rekey-r56-c0137451f5b7/` dir reverted/removed to C0 bytes | `c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5` | `own=own-receipts-missing docs=4/4 total=1` (identical to PIN) |
| fx-t2 (C2 corpus bytes reverted) | `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/receipt-revision-binding.md` reverted to C0 bytes | `cand_credited=51 lost=13 ... rekeyed=5/18 readers=18/18 monitor=6/51 unstable=0 restate=8 total=4` | `own=own-receipts-missing docs=4/4 total=1` (identical to PIN) |

- C2 is separable from C1's tree: C2's verdict is unchanged when every C1 artifact is reverted (fx-t1).
- C1 is **not** separable from C2's corpus bytes: reverting the C2 documents that changed after C0 (the S281 search paragraph in `SOURCES.md`, +2 lines; `QUALITY.md`; the knowledge note) drops 13 of 18 bound headings (`rekeyed=5/18`). Mechanism: the round-21 ledger pins the PIN bytes of these files in its entries' `inputs`. Counted by `sha256` of `git show PIN:<path>` against each entry's `inputs` value: `corpus/SOURCES.md` pin-sha in 13 entries (other 185), `corpus/QUALITY.md` in 6, `tools/registry.json` in 11 [INFERENCE: the 13 SOURCES-pinning entries are the 13 dropped headings; the per-heading mapping was not enumerated].
- Consequence for the deciding run: any further edit to `corpus/SOURCES.md` (or `QUALITY.md`) after PIN breaks C1 at 64/64 unless the ledger is re-bound.

Fixture recipe (reproducible): `git clone --shared <lane> F`; `git -C F checkout --detach PIN`; `git -C F checkout C0 -- <paths>`; `git -C F rm -r --cached`-free removal of the rekey dir; `git -C F commit` after `test "$(git -C F rev-parse --show-toplevel)" = F`.

**(f) PASS — an S-row opened this round is cited.** `corpus/SOURCES.md:156` S281 (`in-toto Statement v1`): `opened 2026-10-28`, `cells[7] = mined`. `corpus/SOURCES.md:157` S282: `opened 2026-10-28`, `rejected` (retained with reason). Census:
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi   -> exit 0
SOURCES.md table rows: 142 (S281 mined, S282 rejected)
```
The C2 knowledge note head cites S281 and S103; the C2 counter's arm 6 accepts any cited `mined` S-row (`c2/measure.py:243-253`). The counter does not check that the cited row is about the note (the wave-2 v6 probe confirms it), so S281 is cited and opened this round, but the arm is weak on topic.

## Limits of this audit
- I did not run the official `controls.sh` (executor items). Control scores above are wave-2 committed receipts only.
- Fabricated-reader attacks on arm 4 are not re-tested here.
- The C1 `fx-case` demonstration shows the counter's sole failing arm at PIN; it is not an admission of the claim.
- Tools installed: none. Lane production files and frozen instruments: not edited.
