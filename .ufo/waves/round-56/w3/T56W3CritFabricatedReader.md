# T56W3CritFabricatedReader — C1 blind spot demonstrated on a scratch clone at PIN

Seat: T56W3CritFabricatedReader (critic, leaf). Axis: calibration. Milestone: `cannot_see`, demonstrated.
Base `981c5e8b`; PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd`; C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`.
Scratch clone: `git clone --shared` of the lane, detached at PIN. The lane and the real `.ufo/waves/round-56/w2` were not touched.
Tools installed: none.

## Verdict in one line

The counter credits a reader report whose `section_sha256` was computed from the tree and never read, and the verdict stays true. That is the `cannot_see` the contract names. The round's sentence about it is accurate for arm 4 but overstates "the only guard". The C1 verdict is also already false at PIN for a reason unrelated to the blind spot (F1), so the attack is measured only after a one-line scratch repair.

## Commands and verdicts

Setup: `S=/fast/scratch/hyaku/tameshi-r56/T56W3CritFabricatedReader`, `C=$S/clone`.
Heading used: `## Context gate classification and explicit exit classes — round 15` (frozen index 0, C0 section start 1652, end 1718, sha256 `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6`, computed by the frozen round-18 `sectionize` at PIN over `git show PIN:SKILL.md`; 64 sections, all 18 frozen headings present).

| State (scratch commit) | Command | Verdict line |
|---|---|---|
| PIN, unchanged (real readers) | `python3 $C/.ufo/evidence/round-56/c1/measure.py --lane $C --rev HEAD --work $S/work-base --explain` | `C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false` (exit 1) |
| K1 = PIN + scratch SCORECARD row fix `8df7ea9f` (real readers) | `... --rev 8df7ea9ff7cd80721cbbc65899f0cdf2746cbf4d --work $S/work-K1 --explain` | `C1_R56: rev=8df7ea9ff7cd c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` (exit 0) |
| K2 = K1 minus `T56W2Read01.json` `e220d132` (heading 1 never read) | `... --rev e220d132a4c9a4170f5ac9d7a09627cb00b8e0e5 --work $S/work-K2 --explain` | `C1_R56: rev=e220d132a4c9 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=17/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false` (exit 1) |
| K3 = K2 plus fabricated `T56W3CritFabricatedRead01.json` in `w2/` `26a92ce8` | `... --rev 26a92ce88e8d3dd30054eff6f765339b8af4b75a --work $S/work-K3 --explain` | `C1_R56: rev=26a92ce88e8d c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` (exit 0) |

Fabricated report (K3), exactly as committed (the `notes` text is the seat's own label, so the scratch file cannot be mistaken for a real read):

```json
{
  "seat": "T56W3CritFabricatedRead01",
  "heading": "## Context gate classification and explicit exit classes — round 15",
  "cand": "c0137451f5b7f22d65f748fc69f1b181f55e1378",
  "section_sha256": "132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6",
  "section_start": 1652,
  "section_end": 1718,
  "findings": [],
  "notes": ["Read the section in full at c0137451; no findings. (Written without reading: section_sha256 computed from the tree by the frozen sectionize.)"]
}
```

Each K-state reads `arm1 ... lost=0 ok`, `arm2 covered=64 score=8 box3=True`, `arm3 dirs=['rekey-r56-c0137451f5b7']`, `arm6 row_score=8 score_at_row=8`, and `unstable=0` (see `--explain` output). The only arm that changes is arm 4 (`readers=17/18` in K2, `18/18` in K3).

## F1 (real, at PIN): the C1 verdict is FALSE, on arm 6's case-sensitive substring

The verdict at PIN is `total=1 C1_R56_PASS=false`. Every other arm is green; the failing check is arm 6's `'round-21' in cells[2]`. The last calibration row, `SCORECARD.md:2718`, reads `Round-21 cold-read monitor ...` (capital R, sentence-initial). The row names the monitor, but the frozen counter needs the lowercase token.

- Fix used in scratch (K1, one line): `SCORECARD.md:2718` `Round-21 cold-read monitor` → `round-21 cold-read monitor`. Nothing else changed. With it, `total=0` and the other arms are unchanged (K1 above; `unstable=0`, because SCORECARD is not a bound input of any rekey entry).
- This is a lane production-file edit for the L1 to integrate, not a counter change. It must land before the deciding run; the new revision is then the certified one.
- Knock-on: `controls.sh` `CTL_POS_c1` (phase B, line 147) runs the counter at PIN and expects `true`. At PIN it prints `false`, so the positive control fails at the revision it certifies. Any controls run must use the post-fix revision.

## F2 (the blind spot, measured): arm 4 credits a report that was never read

- K2 → K3 is the whole demonstration. Removing the real report for heading 1 drops arm 4 to `17/18` and the verdict to `false`; adding the fabricated report restores `18/18` and `true`. The counter cannot tell the two reports apart: it checks only `heading` (via the frozen glob `/T56W\d+.*Read.*\.json$`), `cand == C0`, and `section_sha256 ==` the sha of the section at REV.
- Note on method: with the real report still present (K1 state), adding a fabricated one changes nothing (the counter takes the first match per heading), so the removal is what makes the test meaningful.
- So "the verdict stays true" holds once F1 is repaired. Before F1 is repaired the verdict is false in both states, so F1 is not a result of the fabrication.

## F3: the companion gate `validate-readers.py` is also fabricable, and it is not green at PIN

`.ufo/waves/round-56/validate-readers.py` (wave gate, not called by the counter) checks `commands` (non-empty) and a committed sibling `.md` that runs one listed command verbatim, in addition to the counter's three fields.

Verdicts (`--c0 c0137451f5b7f22d65f748fc69f1b181f55e1378`):

- PIN: `READERS_R56: rev=2f5512a8ab07 ... passed=14/18 failed=4 refusals=10 warn=12 xrev=0 READERS_R56_PASS=false`. The four failing headings are the real reports for heading 1 (`T56W2Read01.md runs none of the listed commands`), 14, 16, 18 (same message). Two receipt JSON files under `T56W2Read02-receipts/` and `T56W2Read05-receipts/` also match the report glob and are refused (`READER_JSON_INVALID`, `READER_HEADING_MISSING`); the counter's regex is identical and it skips them silently.
- K3 (fabricated, no `commands`, no `.md`): heading 1 refused with `READER_COMMANDS_EMPTY` and `READER_MD_MISSING`.
- K4 = K3 plus `"commands": ["git show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md"]` and a `T56W3CritFabricatedRead01.md` naming the heading and containing that command verbatim (`26a92ce8` → `b9473be7`): heading 1 passes, `passed=15/18`. The fabricated report clears the validator with two added fields.

So the validator is a second mechanical check, but it is not a guard against a fabrication that copies one command. The four real refusals at PIN mean the wave's own reader gate is not green at PIN; the L1 should expect that and disposition it.

## F4: what the readers add that the counter cannot check

The real reports carry `findings`, `notes`, `verdict` and `commands`, none of which the counter reads. The real Read01 notes make claims a fabricator would have to get right, and they check out against the tree at PIN:

- `.ufo/evidence/round-15/verification.json`: `passed=False`, `failed_checks=['selftest-new','selftest-new-full-count']` (matches).
- `verification-2.json`: `passed=False`, `failed_checks=['runner-internal-error']` (matches).
- `verification-3.json`: `passed=True` (matches).
- `verification-4.json`: `attempt=4`, `passed=False`, five named failed checks (matches).

Those values were read from the committed receipts, not derivable from the section hash. A fabricated report like K3 contains none of them. The counter therefore certifies that a report exists with the right hash; whether the reader read the section and got its claims right is outside the counter and rests on the seats' review of the notes.

## F5: is the round's sentence about the blind spot accurate?

Contract `cannot_see` (C1), repeated in `T56W1ScribeLesson.md` and `T56W1CritC1.md`: "a fabricated reader report satisfies arm 4 ... The wave's adversarial seats are the only guard, and the report says so."

- The first clause is confirmed: K3 is a fabricated report that arm 4 credits, and the verdict stays true once F1 is repaired (F2).
- "the only guard" is overstated in two ways:
  1. `validate-readers.py` exists. It is a mechanical gate, and K4 shows it can be passed by a fabrication that copies one command (F3). It is weaker than a guard, but it is not nothing.
  2. The lesson lists `CTL_FAB_c1` among "the only guards". That control fabricates a *wrong* hash (`'0' * 64`) and expects `false`. It tests the counter, and it cannot catch a fabrication whose hash is correct, which is the case demonstrated here. It is a control for the counter's arm, not a guard against this blind spot.
- Accurate version: the counter cannot tell a read report from a fabricated report whose hash is correct; the only guard against that is the review of `findings`/`notes` by the wave's seats (F4), and `validate-readers.py` is a shape check that a copied command satisfies.

## Scratch-only patches (for the L1; none applied to the lane)

- `SCORECARD.md` line 2718: `Round-21 cold-read monitor` → `round-21 cold-read monitor` (F1). Scratch commit `8df7ea9f`.
- Removal and fabrication steps in scratch commits `e220d132` (K2) and `26a92ce8` (K3), and the validator-field addition in `b9473be7` (K4). Recipe: `git -C $C rm .ufo/waves/round-56/w2/T56W2Read01.json`; copy the fabricated JSON above to `.ufo/waves/round-56/w2/T56W3CritFabricatedRead01.json`; commit each with `-c user.name=scratch -c user.email=scratch@invalid`.

## Not done

- No lane production file, frozen instrument, bound ledger, or the real `.ufo/waves/round-56/w2` directory was modified; the real `T56W2Read01.json` is intact.
- The C2 counter, the controls run, and the deciding run were not executed here.
- The scratch clone was removed at the end of the seat (per the scratch rule); the commands and outputs above are the receipts.
