# Round 49 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26
lane HEAD measured: `7d3d977f39acaa5723a696dff85ab183c80ddc8b` (base `8ca67421111fa354b47b803358391d0b07fc6db9`; counter freeze `14d03ea4270c6904064022b62b6faf467e5c0968`; content (deciding) revision `bda60768afe172fe9e81359f51c835d8d53494d9`)
driver lines (`.ufo/watchdog.log`, digest copied at closure):
- `2026-10-26T16:49:03-03:00 launch tameshi round=49 pgid=1624230 driver=hyaku-inline attempt=1`
- `2026-10-26T18:21:05-03:00 complete tameshi round=49; hyaku-inline attempt=1`

Lane gates (the round's frozen C1/C2 counters, the round-21 cold-read monitor, `deciding-run.sh`, `no-harm.sh`) were not executed here (PROTOCOL §Gate standard, Closure consequence); their committed evidence was verified. Every other number below comes from a measurement this closure ran over committed bytes, or from a source it re-opened.

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by the lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-49/tameshi.md` (fleet repo) | `tameshi-shokunin 258460ff… 18:19:49` and `tameshi-shokunin 08ae56fa… 18:20:45 -0300`; the final revision comes after its last cited commit `7d3d977f` (18:20:27) and before the driver's completion line (18:21:05) |
| SHONEN heading | read report `## SHONEN` | 4 lines, one per box, all `[~]` with pointers |
| Cited lane commits exist and are ancestors of the branch | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> refs/heads/master` for the 13 distinct cited hashes | 13/13 resolve, are ancestors of `master` and descend from the base. `0cbee392` and `d6dd2cf3` are sha256 prefixes, not commits: `tools/pbt-staged-id.py` hashes to `0cbee392a83e…` and `c2/panel.json` to `d6dd2cf38317…`, which equals `contract.json` `panel.sha256` |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git -C <lane> status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=7d3d977f… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote prints `7d3d977f…` |
| Prompt carries the template contract | render `templates/round-prompt.md` with LANE/ROUND/FLEET_ROOT/AXES, then check each non-empty line is present in `.ufo/prompts/tameshi-round-49.md` | 139 of 140 lines verbatim. The one remaining line is line 1, where the driver resolved `<{{LANE}}-repo>` to the real repo path. Hyaku addendum `## 6` and scratch `## 7` are present |
| Freeze held | sha256 of every path in `freeze.json` at `14d03ea4`, `bda60768` and `7d3d977f` | 13/13 paths are equal at all three revisions (contract, both counters, the controls harnesses, no-harm, deciding-run, the round-21/18 monitors, `tools/staged-id-guard.py`, round-48 precheck) |
| Controls before the deciding run | commit times; `after/c*.start` | controls committed at `6885adb4` 17:19:55 -03, a descendant of the freeze; deciding starts `c2` 21:17:17Z and `c1` 21:17:50Z (18:17 -03), after `bda60768` (18:16:13) and before `143d91e9` (18:18:32), which ships them |
| Generator blind to the panel | presence of `tools/pbt-staged-id.py` and `c2/panel.json` per commit; generator sha256 | generator first appears at `9b9b2a01`, the panel at `bda60768`; the generator is byte-identical at both (`0cbee392a83e`), so it was not edited after the reveal |

Conformance defects: none that bar anything. Hygiene note: the report says the hidden panel copy remains at `~/.local/state/tameshi-r49/`, outside the lane. It is revealed and committed, so that copy is redundant.

## Claims

### C1 — calibration (measured; gate evidence verified, inputs re-measured)

Reported: `covered 57 → 64`, score 6 → 8, `total 105 → 0`, `C1_R49_PASS=true`.

- Committed evidence:
  - `after/c1.stdout` last line: `C1_R49: self=a055e9297cc9 rev=bda60768… sections=64 covered=64 score=8 durable_covered=64/64 headings=7/7 pointers=94 … absent=3 total=0 C1_R49_PASS=true`; `after/c1.exit` = `0`.
  - The counter's self-sha `a055e9297cc9` equals the freeze digest.
  - Selftest `C1_R49_SELFTEST: cases=34 failed=0`, exit 0.
  - Controls `CTL_0 total=105`, `CTL_J total=94`, `CTL_K total=2` are all false. The positive fabrication control `CTL_K2 total=0` is true, and that is the disclosed blind spot.
  - `after/coldread-precheck.stdout`: `floor_credited=57 cand_credited=64 lost=0 ok`.
- Re-measured here:
  - **Ledger append-only.** `.ufo/evidence/round-21/coldread/ledger.json` grew 497 → 511 entries, and the first 497 are equal to base (`eb == ea[:497]` True).
  - **Section hashes.** For each of the 7 final entries (`read_rev 54a52365`), I recomputed sha256 of SKILL.md lines `start..end` at `bda60768`, without the trailing newline. All 7 equal the entry's `sha256`.
  - **Entry inputs.** Every non-SKILL input's sha256 equals its blob at `bda60768` (39/39 `ok`). Each entry's inputs intersect the counter's `VOLATILE` record files (`LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`) in the empty set, so a record append cannot lapse them.
  - **Tip check.** `git diff --stat bda60768 7d3d977f` touches only receipts, `w2` reports and SCORECARD (an append), so the credit holds at the tip.
  - **Reads.** `reads.json` has 94 rows, 91 `holds` and 3 `absent`. Each of the 91 `holds` excerpts is present (whitespace-normalised) in its cited file and line range at `bda60768`: 51 ranged rows, 39 whole-file rows, and 1 external row (`../PROTOCOL.md:63–68`, present in fleet `PROTOCOL.md`). The 3 `absent` rows are `mutate_driver.py`, `plans/round-N.plan.md` and `plans/round-N-record-draft.md`. None has a blob (`git cat-file -t` is fatal), and the sections call them conventions or one-offs.
  - **Corrections.** `corrections.json` has 44 + 1 (pass 2) + 4 (wave-2 pass 3) = **49** applied and 2 not applied (routed). The report says 49.
  - **Line-neutral.** SKILL.md is 2136 → 2136 lines, with 12 hunks of +49/−49. Headings are 62 → 62.
  - **Semantic sample.** A read-only reviewer seat I dispatched checked 8 corrections spread across all 7 sections against their cited surfaces at `bda60768`. All 8 are **correct** and replace a false, unverifiable or stale statement. Examples: `mutate-and-run.sh:569-574` divides by every defect and prints DEGRADED; `SCORECARD.md:13` shows retained scratch, not "from scratch"; `service-optin-protocol.md` §1–§4 has no "boundaries" section; `repeat-control.py` decides `command_unavailable` first and both ids exit 2; `round-14/verification.json` shows 18 FAIL of 34. No correction made a statement false.
- Verdict: **verifies**. calibration **improved** (6 → 8, by the unchanged round-21 monitor; evidence-verified).

### C2 — coverage (F10 open → held; capability; measured and reproduced)

Reported: `generator=absent total=25` → `confirmed=12 target=11 total=0 C2_R49_PASS=true`.

- Committed evidence:
  - `after/c2.stdout` last line: `C2_R49: self=f4971d02b8b1 rev=bda60768… generator=present pristine_exit=0 cases=400 violations=0 … classes_short=0 panel=12 panel_valid=1 confirmed=12 target=11 selftest_kills=6 records_bad=0 total=0 C2_R49_PASS=true`; exit 0.
  - The counter's self-sha `f4971d02b8b1` equals the freeze digest.
  - Selftest `cases=11 failed=0`.
  - Controls `CTL_ABSENT total=25` and `CTL_FIX confirmed=6 total=10` are false; `WITNESS witness_confirmed=12`.
- Re-measured here, without the counter:
  - **Generator presence.** `tools/pbt-staged-id.py` is absent at base and present at `bda60768`.
  - **Pristine run.** In a temp dir I copied the generator and the guard (guard sha256 = `panel.target_sha256`) from `bda60768` and ran `python3 -I pbt.py --guard <copy> --seed 4949 --cases 400 --dump <f>`. It exited `0` with `PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31`. These are the same 12 class counts as `after/c2.stdout`, and all are ≥ 10.
  - **Panel runs.** I applied each of the 12 `panel.json` `old → new` edits to a guard copy and ran the same command. **12/12 exited 1** with `violations=1`:

    | Mutant | Name | Counterexample at |
    |---|---|---|
    | M01 | row-indent-4 | case 20 |
    | M02 | row-column0 | case 0 |
    | M03 | id-width-3 | case 3 |
    | M04 | www-kept | case 12 |
    | M05 | slash-kept | case 8 |
    | M06 | held-form-sensitive | case 8 |
    | M07 | naive-off-by-one | case 0 |
    | M08 | cascade-vs-registry | case 5 |
    | M09 | duplicate-accepted | case 50 |
    | M10 | short-row-accepted | case 11 |
    | M11 | map-injectivity-dropped | case 93 |
    | M12 | map-uncovered-dropped | case 41 |

    The temp dir was removed.
  - **Guard access.** In the generator source, the guard path is only checked by `os.path.isfile` and invoked as a subprocess. It is never opened or imported, which agrees with `T49W2ExecGenTrace.md`.
  - **Frontier line.** `corpus/README.md` `## Round 49` gains F10 open → held, conditioned on the receipt, which prints PASS. The entry `corpus/knowledge/pbt-generator-pilot.md` opens with `source:` S269 and S270, both `mined`.
- Verdict: **verifies**. coverage **improved**. Capability row "property-based generator for a fixture gate" (SCORECARD round-49 section) is demonstrated by the run above.

### No-harm

- **SCORECARD.** `git diff 8ca67421 7d3d977f -- SCORECARD.md` is append-only (+30/−0 by `--numstat`; base is a byte prefix). The other numeric axes are restated: depth 9, freshness 9.
- **Record files.** LOG.md +13/−0, QUALITY +22/−0, README +8/−0, SOURCES +5/−0, and `knowledge/` +1 file (58 → 59), with no deletions.
- **Monitors.** `after/no-harm.stdout` has all 9 monitors `ok`: commandD depth 9, coldread-floor 8/64, r45-freshness 71/73, registry 130, and the r45/r46/r47 coverage monitors. `no-harm-at-base.stdout` has the same values except coldread 6/57 and registry 128. `frozen.stdout`: `FROZEN_UNCHANGED=1`.

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 verified; ledger and reads re-measured; monitor score 6 → 8 evidence-verified |
| coverage | improved | C2 verified; generator run reproduced 400/0 and 12/12 |
| depth | unchanged | commandD `depth_score=9` before and after; SKILL.md edits are line-neutral corrections |
| freshness | unchanged | r45 freshness `fresh=71/73` before and after |
| operability | unchanged | no claim on this axis; new tool counted under coverage/capability |
| adjacency | unchanged | no claim; the sibling PBT connector note (`T49ConnSiblingPBT.md`) reports and absorbs nothing |

## Discernment spot-check (LEARNING.md)

Sources were re-opened by this closure on 2026-10-26: `curl` plus `pdftotext`, non-layout mode for the two-column ICFP paper.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| staged S182 → **S269** (QuickCheck, ICFP 2000) | admit | `https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf`: HTTP 200, 194,315 B, sha256 `bfddcaa648f8…` = the lesson's pin | agree | The 20-word quote "The combinator collect will gather all values that are passed to it, and print out a histogram of these values" is present in §2.4 Monitoring Test Data (PDF p. 3; heading `2.4 Monitoring Test Data`). The 14-word abstract quote is also present. The `ICFP '00` block is on the article text. The tier A and the mirror-carrier disclosure are honest |
| staged S183 → **S270** (Smallbone TR 76L), anchor corrected §4.1 p. 44 → §2.10 p. 34 | admit, with correction | `https://smallbone.se/papers/lic.pdf`: HTTP 200, 1,269,821 B, sha256 `eaee48f930ba…` = pin | agree | The 19-word quote "As always with random testing tools, the quality of the test data determines the quality of the generated equations" is present on PDF p. 39, printed p. 34, which carries §2.10. "fit the program at hand" is also on PDF p. 39. PDF p. 49 (printed 44) is `3.4 shr: Problems with Partiality` and has no "generator", so the package locator was wrong and the correction is right |
| `r4-quickcheck-primary-correction.md` | reject | `https://doi.org/10.1145/1660572.1660575` → **404**; `api.crossref.org/works/…` → **404**; control `doi.org/10.1145/351240.351266` → 302. Lane: `git log -S'1660572.1660575' 8ca67421` → 0 commits; all `--all` hits are round-49 commits that write the rejection | agree | The entry's identifying premise ("The lane's leads list has carried `doi:10.1145/1660572.1660575`", package file line 12) is false at base and in history, and the DOI does not resolve (QUALITY 2) |
| `pbt-generator-craft-author.md` | reject | `https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf` (HTTP 200): the abstract reads "…extensions made for testing stateful code, via a toy example in C". `grep -cE '^ {0,3}\| S116 \|'` over lane SOURCES at base → 0 | agree | The entry says S170's subject is "not toy" (package line 24), which the abstract contradicts. Its `S116` pointer resolves to no tameshi row |

- **New SOURCES row re-opened:** S270 (above). Its ≤25-word quote is located and present; its `teaches` cell matches §2.10.
- **Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0. It prints 15 W-lines, all on older rows and identical to `census-start.stdout`/`census-end.stdout` (15 = 15, `diff` empty). S269 and S270 raise none.
- **Result:** the spot-check agrees with the gate on 2 admits and 2 rejects. QUALITY criterion 99 is grounded in a lesson (round-48 spot-check defects 2-3, round-49 `## Mistakes` row 1). Its falsifier is committed and refuses as stated (`T49ExecMistakeGate/case-{a,b,c}.stdout`: `DECIDING_REFUSED control-receipt-missing`, `second-invocation c1`, `control-receipt-not-after-freeze`).

## Trend verdicts

- **expansion: improved.** One net new admitted `knowledge/` entry on uncovered ground: F10 was `open` at `corpus/README.md:87` at base. It cites two `mined` rows that were re-opened and quote-checked here, and the capability row is demonstrated by this closure's own run.
- **quality: improved.** 49 corrections replace false, stale or bare statements in seven sections. A non-author sample of 8 found all correct, and no admitted entry failed its re-check. The stale sentences outside the sections are marked and routed in the lesson (`corpus/lessons/round-49.md:79` for SKILL.md:1509 and 1555, `:125` for SKILL.md:1503), not left unmarked.
- **discernment: improved.** The outside spot-check agrees on admits and rejects. The new QUALITY criterion has a lesson and a committed red-before falsifier.

## Routed defects for the lane next round

1. **Generator error paths** (`.ufo/waves/round-49/w2/T49W2RevGenCode.md`, F1–F3). Fix: an unreadable guard exits 1, where the docstring says 2, because `main()` checks only `os.path.isfile`; F2/F3 are minor error paths. Each fix needs a selftest case that fails before it. The lane already routed this.
2. **Counter blind spots** (SCORECARD `Planned (round 50)`). C1 `absent` is uncapped and needs no evidence. C2 cannot tell a property-based generator from a differential one; the property currently rests on a seat's access trace. Close these with a successor counter, not prose.
3. **Outside-section stale sentences.** SKILL.md:1503 (`/tmp/tameshi-r12-*` namespace overlap), 1509 and 1555 are routed in `corpus/lessons/round-49.md` and still open.
4. **Standing axis table.** The round-49 SCORECARD section states "calibration 8 (was 6)" in prose. The last standing axis table, at the round-48 section line 2355, still reads `calibration | 6`. Append a restated standing table with the round-49 values; do not rewrite.
5. **Carried round-48 items** (round-48 spot-check routed defect 4): still listed as carried, not landed.
6. **SHONEN.** All four boxes remain `[~]`. Box 3's evidence is lane-dispatched readers plus this closure's 8-item sample, which is not a full non-author cold read. No box is fully checkable by a non-author this round. Promotion stays operator-owned.
