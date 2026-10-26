# T50Disp45 — C1 dispositions, round-45 verifier spot-check

seat: T50Disp45 (C1 disposer, round 45)
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base rev read: `e3729de862f73ae080d98fcf522a7081ce16e40a` (round-49 verifier spot-check; lane tip at read time `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`)
spot-check: `corpus/lessons/round-45-verifier-spotcheck.md`, `routed_at` `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`
frozen set: `.ufo/evidence/round-50/c1/defects.json` (R45.1-R45.4, all four routed in the same commit)
counter: `.ufo/evidence/round-50/c1/measure.py` (read, not run against the lane; run only with `--explain` on a scratch clone)

Rows: `T50Disp45.rows.json`. Per-row outcomes: R45.1 open, R45.2 open, R45.3 declined, R45.4 open.
No product file was edited; the only writes are this report, the rows JSON, the two explain receipts in this directory, and commits inside a scratch clone under `/fast/scratch/hyaku/tameshi-r50/T50Disp45/` (deleted).

## R45.1 — no-harm monitor false red (`c-r44-at-content`, `cd8e73f0`, round-parametric)

**Ask.** "Fix the counter (exempt pinned external hashes and be round-parametric) before it is named in another contract's `no_harm`."

**Found.** The counter that produced the false red is `.ufo/evidence/round-44/calibration/measure.py`. `git -C <lane> show e3729de8:.ufo/evidence/round-45/after/c-r44-at-content.stdout` prints, line 1: `C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=1 m12=1 m13=0 total=2 ... C2_R44_PASS=false first=m11:SCORECARD.md#round-45:cd8e73f067129f8489e35c7b51c7a68552b289d2` — the two false-red classes the routing names are still printed. Neither property asked for exists in the source at base: `m11_revisions` (`.ufo/evidence/round-44/calibration/measure.py:351-357`) still fails every 40-hex token that `git cat-file -e` cannot resolve inside the lane, with no exemption for a pinned upstream revision; the m12 gate (`.ufo/evidence/round-44/calibration/measure.py:519-521`) still appends `newest block is round %d, the contract round is %s` for any newest SCORECARD block that is not the contract's round, so it is still round-bound. `git -C <lane> log --oneline 683eedde..e3729de8 -- .ufo/evidence/round-44/calibration/measure.py` prints nothing: the file is byte-unchanged since its own freeze (`ba01973c`). What rounds 46-49 did instead is remove the harm path, not fix the counter: QUALITY criterion 88 (`corpus/QUALITY.md:1297-1299`) rules that such a round-bound counter "cannot be a monitor of a later round", `.ufo/evidence/round-46/quality/no-harm-gate.py` refuses a red monitor, and no later script runs it as a monitor: `grep -rn 'round-44/calibration/measure.py' .ufo/evidence/round-46/no-harm.sh .ufo/evidence/round-47/no-harm.sh .ufo/evidence/round-48/no-harm.sh .ufo/evidence/round-49/no-harm.sh` prints nothing, while `.ufo/evidence/round-46/no-harm.sh:3` states the exclusion in its header (`# Round-bound counters (the round-44 record-agreement counter) are deliberately NOT here`).

**Status: open.** Both named properties are missing from the tree; the ask was a source fix, and a source fix is the only thing that closes it. The routing's second clause (not re-cited in `no_harm`) holds, which is why the counter is not named again, but a compound ask is closed only when every part exists. `fix_plan` (in the row): exempt a token pinned as an external upstream revision in `m11_revisions`, grade `contract["round"]`'s block instead of the newest block in `m12`, and add one selftest case per property.

## R45.2 — selftest receipts and survivors (`selftest receipt`, `selftest.stdout`, `C1_R45`, `C2_R45`)

**Ask.** Two halves: "Commit `--selftest` stdout (tally) for both `measure.py` counters; kill the 12 (C1) and 8 (C2) selftest survivors already routed in SCORECARD 'Planned (round 46)'."

**Found.** The committed selftest tallies belong to the round-46 counters, not to the two round-45 counters: `git -C <lane> show e3729de8:.ufo/evidence/round-46/selftest/c1-selftest.stdout` lines 19-20 print `C1_R46_SELFTEST: cases=18 failed=0` / `VERDICT: PASS` (and `c2-selftest`, `c3-selftest` are the round-46 mutation driver and coverage counter). The round-45 counters still carry a `--selftest` mode — `.ufo/evidence/round-45/freshness/measure.py:36` `Modes: --lane L --rev R (deciding/measure); --selftest; --check FRAGMENT.json` and `.ufo/evidence/round-45/coverage/measure.py:19` `Modes: --lane L --rev R; --selftest.` — but no committed receipt of either exists: `git -C <lane> ls-tree -r --name-only e3729de8 -- .ufo/evidence/round-45 | grep -ci selftest` prints `0`. The kill half is done, on copies: `.ufo/evidence/round-46/after/c2.stdout:36` prints `C2_R46: self_pin=1 targets=hardened declared=25 killed=25 survived=0 ... C2_R46_PASS=true`, and the round-46 spot-check (`corpus/lessons/round-46-verifier-spotcheck.md:44`) records the limit the lane itself discloses: "the operative round-45 counters are untouched (credit sits on the hardened copies)". `git -C <lane> log --oneline 683eedde..e3729de8 -- .ufo/evidence/round-45/freshness/measure.py .ufo/evidence/round-45/coverage/measure.py` prints nothing, so the round-45 selftests still let those survivors through and only the hardened copies kill them.

**Status: open.** The literal ask — committed `--selftest` stdout for *those two* counters — is absent, and the survivor kill lives in copies, not in the counters the routing audited. `fix_plan` (in the row): commit two `--selftest` receipts for the round-45 counters with a SCORECARD citation; the kill half is already receipted.

## R45.3 — freshness score definitional jump (`floor(10*fresh/73)`, `fresh=71`, one-document unit)

**Ask.** "The score 1 → 9 changes the formula (`floor(10*fresh/73)` vs the one-document unit); cite the 0 → 71 count as the comparable measure and keep the old unit as monitor (already done)."

**Found.** The routing itself marks the remedy "(already done)", and the tree agrees at the routing commit. `git -C <lane> show 683eedde:SCORECARD.md | grep -n 'floor(10 \* fresh / 73)\|one-document unit'` prints 2 hits: the round-45 block line `Freshness score rule (replaces the round-44 one-document unit): floor(10 * fresh / 73) → 0 at freeze, 9 at the deciding run. The round-44 unit stays a monitor …` and the C1 row whose after cell carries `verified=73 disputed=2 fresh=71 score=9`. Rounds 46-49 restate the same count in standing rows (base line 2200: `` `floor(10 * fresh / 73)` … (`fresh=71`, `score=9`; 2 rows disputed: S048, S093); the round-44 one-document unit … stays a monitor``; `git log -S'one-document unit' 683eedde..e3729de8 -- SCORECARD.md` → e630ae79, 8b0e15d2, c7586b9a).

**Status: declined** — an observation, not a defect: no tree artifact is missing, the comparable count and the retained monitor already exist at `routed_at`, and no post-routing commit can "add" what was present before it (the counter's own fixed rule requires the keyed excerpt to be absent at `routed_at`, which it is not). Reason in the row.

## R45.4 — anchor refresh (`ConnDriftAnchors`, `S026`, `S093`, `S108`, pin by quote)

**Ask.** "Five anchor-refresh candidates in `.ufo/waves/round-45/w2/ConnDriftAnchors.md` stay open; S026/S093/S108 live bytes now differ from the snapshots (dynamic pages) — the next recheck should pin by quote, not by whole-page hash."

**Found.** Half is done. Round 48 re-anchored S026, S093 and S108 by quote with committed snapshots and fetch receipts: `corpus/SOURCES.md:140` (S265) `supersedes S026's anchor and quote only: … re-anchored to the 2026-10-26 bytes`, `:142` (S267) `supersedes S093's anchor and quote only: …`, `:143` (S268) `supersedes S108's anchor and quote only: … re-located in a committed 2026-10-26 snapshot`. The five candidates the routing names are still unrefreshed: `git -C <lane> show e3729de8:corpus/SOURCES.md | grep -cE 'supersedes S(153|154|157|159|100)'` prints `0` (and prints `0` again at the current tip `4afb060`), while the same five rows still pin the drifted round-41/42/33 snapshot digests — `corpus/SOURCES.md:123` (S153) `… snapshot .ufo/evidence/round-41/sources/ast.html 362029 B sha256 183a4f8c`, which `.ufo/waves/round-45/w2/ConnDriftAnchors.md` recorded as `≠ today's raw` (`f4c18b31…`). The lane's own record agrees they were not worked: `SCORECARD.md:2253` "the third (re-pin the anchor-refresh candidates of `.ufo/waves/round-45/w2/ConnDriftAnchors.md`) were not worked and stay open for round 47".

**Status: open** (compound: quote-pinning done for three rows, five refreshes missing). `fix_plan` (in the row): one supersede row per drifted document, pinned by quote plus committed round-50 snapshot bytes, per the round-44 anchor-refresh rule.

## Self-check

Scratch clone `git clone -q --shared <lane> /fast/scratch/hyaku/tameshi-r50/T50Disp45/lane` (toplevel verified equal to the clone), my four rows written into `corpus/routed-defects.json` as `{"defects": [...4 rows...]}`, committed with a scratch identity (`8201a59`, then `161fe20`), then:

    python3 .ufo/evidence/round-50/c1/measure.py --lane <clone> --rev <rows-only commit> --explain

Observed, rows only — full output in `.ufo/waves/round-50/w1/T50Disp45.explain-rows-only.stdout` (49 lines: 45 `missing` lines for the other rounds' ids, the three lines below, the final line), exit 1 because `total>0`:

    EXPLAIN open-unplanned R45.1
    EXPLAIN open-unplanned R45.2
    EXPLAIN open-unplanned R45.4
    C1_R50: self=ceee320c9ad8 rev=8201a59a… fixed=0 open=3 declined=1 fixed_this_round=0 missing=45 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=3 declined_bad=0 fixed_short=20 declined_over=0 this_round_short=5 total=73 C1_R50_PASS=false

The three `open-unplanned` lines are the L1-owned dependency: `open` requires the id in the newest `**Planned (round` paragraph, and the base `**Planned (round 50):**` paragraph names none of R45.1/R45.2/R45.4 (`git show e3729de8:SCORECARD.md | sed -n '2410p'`). After appending `…; the round-45 routed items this ledger leaves open (R45.1, R45.2, R45.4).` to that paragraph inside the same scratch clone, the same command printed (full output in `.ufo/waves/round-50/w1/T50Disp45.explain-with-planned.stdout`, 46 lines, exit 1 because `total>0`):

    C1_R50: self=ceee320c9ad8 rev=161fe20a… fixed=0 open=3 declined=1 fixed_this_round=0 missing=45 extra=0 duplicate=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=20 declined_over=0 this_round_short=5 total=70 C1_R50_PASS=false

`missing=45` is the other nine round groups' rows I did not write; `fixed_short=20` / `this_round_short=5` are ledger-wide floors, not this seat's rows. Every per-row term for R45.1-R45.4 is 0 in both runs; the only difference is the three planned lines, so the rows are internally consistent and hinge only on the L1's Planned edit.

## Findings

1. R45.1 is still false-red at base — `.ufo/evidence/round-45/after/c-r44-at-content.stdout:1` prints `m11=1 m12=1 … C2_R44_PASS=false` — because `.ufo/evidence/round-44/calibration/measure.py` was never edited after its freeze (`git log --oneline 683eedde..e3729de8 -- <that path>` is empty). The lane closed the citation path (QUALITY 88, `no-harm-gate.py`), not the counter; I therefore record it open, not fixed.
2. R45.2's receipts exist for the round-46 counters only (`.ufo/evidence/round-46/selftest/c1-selftest.stdout:19`), and `git ls-tree -r --name-only e3729de8 -- .ufo/evidence/round-45 | grep -ci selftest` prints `0`; the 25/25 kill sits on hardened copies (`.ufo/evidence/round-46/after/c2.stdout:36`), with the operative counters untouched (round-46 spot-check line 44).
3. R45.3 could not be a "fixed" row even though the text exists: `git show 683eedde:SCORECARD.md | grep -c 'floor(10 \* fresh / 73)\|one-document unit'` prints `2`, i.e. the keyed text predates `routed_at`; the honest disposition is declined-as-observation.
4. R45.4's five named candidates have no supersede row at base or tip (`grep -cE 'supersedes S(153|154|157|159|100)'` → `0` twice), while S026/S093/S108 are quote-pinned by S265/S267/S268 (`corpus/SOURCES.md:140,142,143`). Partial → open.
5. Ledger-wide dependency for the L1: the newest `**Planned (round 50):**` paragraph must name every id any seat leaves open, otherwise the frozen counter counts `open_unplanned` (observed 3 here, 0 after the simulated append).
6. Evidence paths were checked against the counter's own rules: no spot-check file, no `corpus/routed-defects.json`, nothing under `.ufo/evidence/round-50/{c1,control}`, no `.ufo/waves/` path (the only `.ufo/waves/` citation, `ConnDriftAnchors.md`, would be refused by the soft-path rule, so the SCORECARD and SOURCES rows carry the keyed evidence instead).

## Touched surfaces

- Wrote `.ufo/waves/round-50/w1/T50Disp45.md`, `.ufo/waves/round-50/w1/T50Disp45.rows.json`, `.ufo/waves/round-50/w1/T50Disp45.explain-rows-only.stdout`, `.ufo/waves/round-50/w1/T50Disp45.explain-with-planned.stdout`.
- Scratch only: `git clone --shared` at `/fast/scratch/hyaku/tameshi-r50/T50Disp45/lane`, two commits by scratch identity `T50Disp45 <T50Disp45@scratch.local>`; scratch dir deleted after the receipts were copied.
- Lane checkout, fleet repo, `~/.local/state/`, `shokuknow/` untouched; no git/jj mutation outside the scratch clone. No tool installed or upgraded.

## Summary

R45.1 open: the round-44 record-agreement counter is byte-unchanged since its freeze; m11 still flags the pinned upstream `cd8e73f0` and m12 is still round-bound; QUALITY 88 removed it from `no_harm` but did not fix it.
R45.2 open: committed selftest tallies are the round-46 counters'; the round-45 freshness/coverage counters have no committed `--selftest` receipt (0 files) and their survivors are killed only in the hardened copies (25/25).
R45.3 declined as an observation: the 0→71 count and the retained one-document monitor already exist at the routing commit (SCORECARD 2154/2159), so there is no missing artifact and no new keyed text.
R45.4 open: S026/S093/S108 are quote-pinned by S265/S267/S268, but the five named candidates S153/S154/S157/S159/S100 still have no supersede row (0 hits at base and tip).
Counter self-check on a scratch clone: every per-row term 0; only `open-unplanned ×3` depends on the L1 naming R45.1/R45.2/R45.4 in the newest Planned (round 50) paragraph (observed 3 → 0 after the simulated append).
