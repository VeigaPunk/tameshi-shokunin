# T54W1RevDedup01 — dedupe C1/C2 arms vs rounds 48–53; QUALITY 105

Seat: reviewer (dedupe; no distiller lane). Milestone: dedupe against rounds 48–53.
Judged on: calibration. Axes named: **calibration (C1)** · **operability (C2)**.
No lane production files edited. Tool installs: none.

## Sources opened

| Artifact | What checked |
|---|---|
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/contract.json` | frozen C1/C2 targets |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py` (docstring arms 1–5) | R54 C1 arm inventory |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c2/measure.py` (docstring arms 1–5) | R54 C2 arm inventory |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-53/c1/measure.py` (docstring arms 1–3) | R53 C1 arm inventory |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-53/c2/measure.py` (docstring arms 1–4) | R53 C2 arm inventory |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-{48,49,50,51,52,53}/tameshi.md` | routed defects / claim surfaces (fleet reports; lane `.ufo/reports/round-5N/tameshi.md` absent) |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-4{8,9}.md`, `round-5{0,1,2,3,4}.md` | Gate / Mistakes / QUALITY drafts |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-5{2,3}-verifier-spotcheck.md` | R52.1–R52.6, R53.1–R53.9 |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md` criteria 17, 98, 99, 101, 103, 105 | overlap test for criterion 105 |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout` | `rekeyed=0/30` at R53 tip |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/control/controls.sh` | CTL_0 (do-nothing) vs CTL_POS |

## Verdict up front

Five C1/C2 arms restate earlier claim arms (duplicate pairs below). Draft QUALITY **105 is a duplicate specialization of QUALITY 101** (the printed claim-label totals must be exercised — a `rekeyed=` total frozen at 0 on every tree, including the content revision, was never exercised). The one genuinely new arm is **C1.stable** (re-key entries must not pin `LOG.md` / `SCORECARD.md`).

## Duplicate pairs (R54 arm ↔ earlier arm)

1. **R54 C1.precheck** (`cand_credited=64 lost=0 ok`) ↔ **R53 C1.floor** ↔ **R52.1** (coldread re-key debt) ↔ **R49 C1** (restore seven lapsed sections) ↔ **R48 spotcheck routed #1** (restore three lapsed headings). Same obligation: the round-21/48 cold-read floor reads 64/64 at the deciding revision. Evidence: R53 counter docstring arm 1; R54 `c1/measure.py:9-11`; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/tameshi.md:13-16`; `corpus/lessons/round-52-verifier-spotcheck.md:83` (R52.1); `/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/tameshi.md:9`; `corpus/lessons/round-48-verifier-spotcheck.md:114`.

2. **R54 C1.rekey** (ledger entries under `rekey-r54-<c0>`) ↔ **R53 C1.rekey** (`rekey-r53-<c0>`). Same arm class; R54 only repairs the R53.1 pathspec (`ls-tree -r` vs non-recursive). Evidence: R53 `c1/measure.py:11-18`; R54 `c1/measure.py:14-22`; `corpus/lessons/round-53-verifier-spotcheck.md:78` (R53.1); `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout` → `rekeyed=0/30`.

3. **R54 C1.readers** (committed `*Read*.json` pins `section_sha256` at c0) ↔ **R53 C1.readers**. Evidence: R53 `c1/measure.py:19-23`; R54 `c1/measure.py:24-28`.

4. **R54 C2.usable** (selftest exit 0 under usable TMPDIR; strace shows no mkdir under `/tmp`) ↔ **R53 C2** arms grep+selftests (`tmp_hits=0`, redirected-TMPDIR selftests) ↔ **R52.5** (hard-coded `/tmp` in tools). Evidence: R54 `c2/measure.py:16-18`; R53 `c2/measure.py:8-14`; `corpus/lessons/round-52-verifier-spotcheck.md:87` (R52.5); `/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/tameshi.md:27-35`.

5. **R54 C2.unusable** (7/7 exit 2, naming `could-not-evaluate`, no traceback) ↔ **R53 C2.cr47** (registry-check only) + **R53.6** (four of seven tools still rc=1). Same exit-class arm; R54 widens the measured population 1→7. Evidence: R54 `c2/measure.py:9-11`; R53 `c2/measure.py:15-18`; `corpus/lessons/round-53-verifier-spotcheck.md:83` (R53.6).

Also noted (reinforcement, not a sixth pair): **R54 C1.monitor** (`sections_covered==64`, `calibration_restraint_score==8`) is the same round-21 selector R49/R51/R53 already used as the floor's score surface; R53's counter did not print it as its own arm, but the obligation is not new.

## QUALITY 105 — duplicate of QUALITY 101

Round-54 obligation behind the draft criterion: **R53.1** — the frozen C1 rekey arm was structurally dead (`rekeyed=0/30` at every revision) while do-nothing / pre-registered controls still printed their expected `PASS=false` for other reasons (`corpus/lessons/round-54.md:64-76`, `:98-104`; QUALITY.md:1584-1590).

The lesson marks that mistake `captured-by: none`. That understates **QUALITY 101** (`corpus/QUALITY.md:1526-1532`):

> so the pins, floors and **total that print the claim label** are exercised, not only pure helpers.

R53's claim label prints `rekeyed=K/N`. A total that is `0/N` on the do-nothing tree **and** on the content revision (`r53-counter-at-88afa941.stdout`) was never exercised as a discriminating total — mutation receipts stayed INCONCLUSIVE for the same reason (`corpus/lessons/round-53-verifier-spotcheck.md:41`). QUALITY 101 already binds that the printed totals be exercised; QUALITY 105 only renames the missing fixture shape (a positive tree where the arm must fire) as a standing criterion.

Not covered by QUALITY 99: that criterion "binds the order, not the values" (`QUALITY.md:1446-1455`); R53 did score controls before deciding.

Not a fresh capture of QUALITY 17 either: 17 already covers **R53.6** (classify every nonzero exit as could-not-evaluate). That is the C2.unusable duplicate above, not the 105 draft.

**Duplicate pair (criterion):** QUALITY 105 ↔ QUALITY 101 (arm-level reading of "totals that print the claim label are exercised"). Drafting 105 as a new numbered criterion is the duplicate; the fix (recursive pathspec + CTL_POS requiring `rekeyed=7/7`) still belongs in the counter and controls.

## The one genuinely new C1/C2 arm

**C1.stable** — no re-key entry under `rekey-r54-*` may pin `LOG.md` or `SCORECARD.md` as an input (`c1/measure.py:29-31`, `UNSTABLE_INPUTS`).

Why new: R49's durability fix *required* reading those record files through git blobs so appends would not lapse credit (`corpus/lessons/round-49.md:80-84`, Mistakes row 2). R53 then lost floor credit when re-keys pinned those same files (`corpus/lessons/round-54.md:88-90`). R54 inverts the R49 rule: forbid the pins entirely. No R48–R53 claim arm measured that prohibition.

Not chosen as "the new arm":
- **C2.empty** (`TMPDIR=""` → exit 0) is also absent from R53's counter, but it is an operability arm; this seat is judged on calibration.
- **C2.docs** / **C2.note** are documentation/census arms around the same scratch-root contract R53 already claimed.

## Residual risk / verification gaps

- Phase-B `controls-b.stdout` (QUALITY 105's cited green receipt for `rekeyed=7/7` on CTL_POS) is not present yet under `.ufo/evidence/round-54/control/`; the red R53 receipt is present. Dedup of the *obligation* does not wait on that receipt.
- Fleet reports for rounds 48–53 were read at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-N/tameshi.md` (lane copies absent); lessons and spotchecks were read under the lane.
- No census run by this seat (L1 conformance item).
