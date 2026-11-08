author: hyaku closure (non-author integrator, @m_zfl)

# Round 94 verifier spot-check (non-author integrator, @m_zfl)

Lane `tameshi` round 94 (verification-fixture craft), closure judge (non-author). Lane
HEAD after round: `507adb5cc3ed610c209791ad07dbb2ed75961cd9`; base before round:
`a8f0e14bd400002324793d82030431696435d9a7`. Report:
`.ufo/reports/round-94/tameshi.md`; wave `r94-w1`.

## Step-1 conformance

- Report committed in the fleet repo by the lane identity:
  `git log --format='%an %H %s' -- .ufo/reports/round-94/tameshi.md` →
  `tameshi-shokunin c70259ced103594bd3ef596b8e58778d0e714301 round-94: tameshi report addendum — late commits and final lane tip`
  and `tameshi-shokunin fc241b5f6cf97b21868305e2dc56aabbcbb0e546 round-94: tameshi report`.
  The report was filed after the lane tip (`507adb5c` 07:12:14-03:00; report
  `fc241b5f` 07:12:35-03:00; addendum `c70259ce` 07:12:59-03:00) — lands last.
- `## SHONEN` heading present once, four `[~]` box lines (four `SHONEN.md` boxes), each
  with an evidence pointer; no `[x]` claimed. Not a marker.
- Every cited lane commit exists and is an ancestor of the branch ref:
  `git merge-base --is-ancestor <hash> master` holds for `a8f0e14b`, `7084358c`,
  `fdbd18c6`, `33279f40`, `4dc919ac`, `67ce02ba`, `6a2a1fdd`, `2ad7ebb0`,
  `b98b0864`, `67b1ab85`, `cdf669cf`, `02b43cad`, `6b19eb92`, `93164a68`,
  `bfd79afd`, `069a5055`, `70fcf8b0`, `5abf500c`, `507adb5c` (19/19 ancestor-ok;
  lane git HEAD is detached by jj-colocation, tested against `master` as required).
- Lane repo clean and pushed: `jj-lane.sh state` →
  `branch=master local=507adb5c remote=507adb5c ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` → empty; `git ls-remote origin refs/heads/master` →
  `507adb5cc3ed610c209791ad07dbb2ed75961cd9` (matches).
- Prompt fidelity: `.ufo/prompts/tameshi-round-94.md` is 989 lines; lines 1–140 are the
  `templates/round-prompt.md` rendering with only the documented substitutions
  (`LANE`, `ROUND`, `FLEET_ROOT`, `AXES`, `paths`), followed by the hyaku addendum §6/§7
  and §8 (pre-file ledger). The five child-lane items are present: report path and
  filename (§4), commit-before-report ordering (§5 and the `fleet-commit.sh` text),
  `SHONEN` heading requirement (§4 and the `grep -c '^## SHONEN'` pre-report gate),
  commit-hash citation rule (§4 Landed changes + §5 “cites the pushed lane hash”), and
  the lane write scope (§5 push scope). The round-level contract is present: §1
  MISSION/AXES binding, §2 1–3 claims, §3 L2 floor ≥8 in one batched call, §5
  commit-then-push and L0 side channel. No L2 route map is quoted, so there is nothing
  to compare with the current `MISSION.md` bucket (the §3 text points at the host route
  table; it does not restate a bucket).
- Conformance defects are named under *Routed defects* below; they are status-neutral.

## Per-claim re-check

Both claims are lane-owned gates; per PROTOCOL §Gate standard (Closure consequence) I
verified their committed evidence and did not execute either gate. The measurements
below are plain parses/counts over committed bytes at `507adb5c`.

### R94-C1 (coverage) — verified

- Instrument blobs at the instrument revision and at the tip:
  `git show 7084358c:.ufo/evidence/round-94/c1/measure-v94.py | sha256sum` →
  `a22563b0c2b4a2b43922cec3d1ab3fa511110e035b9edfdfdc6eaebb97023010` (matches
  `claims.json`); `controls-v94.py` →
  `9a0870c2e33b8634dcd9dbd28adbec3fe5178ba76cce9a94a16e9e063b4c6ecf` (matches).
  The same two digests hold at `507adb5c`.
- Receipt population: `ls .ufo/evidence/round-94/pre-freeze/controls/*.out | wc -l` →
  `45`; `grep -c 'MATCH' .../controls/C1-summary.txt` → `45`;
  `grep 'C1_CONTROLS' .../pre-freeze/controls-run.log` →
  `C1_CONTROLS states=45 matched=45 mismatches=0 missing=0`.
- Per-state re-derivation (my parser over the committed receipts): 6 positive states
  exit 0 / `C1_R94_PASS=true`; 30 hostile states exit 1 / `C1_R94_PASS=false` with the
  plan's named conjunct false; `gate-foreign` exit 2 with
  `C1_SETUP gate-identity-mismatch`; `nowork-base` exit 2 with
  `C1_SETUP spec-absent-at-rev`; `selfpin-edit`/`replace-honest` exit 2 with their
  setup tokens; D01–D05 exit 0 with `C1_R94_PASS=true` (the removal cheats return).
  Checked 44 receipt files plus `nowork-base`; **0 mismatches** against the plan's
  table. 37 receipts carry `parent=7084358c…`; the 5 removal receipts and the 3 setup
  controls are the expected exceptions.
- Landing: `grep 'C1_R94_PASS' .../landing/c1-at-landing.out` → `C1_R94_PASS=true`;
  `pos-real.out` carries `n=12 killed=5 survived=7 inconclusive=0 unstable=0 invalid=0
  trivial=0 witnessed=7/7 note=present mismatched=0 badrows=0 verdict_tables=1` and
  `C1_SOURCE S320=row:1,quote:1 S321=row:1,quote:1 S322=row:1,quote:1`.
- Before: `nowork-base.out` → `exit=2`, `C1_SETUP spec-absent-at-rev`,
  `C1_R94_PASS=false` at base `a8f0e14b`. After: `C1_R94_PASS=true`, exit 0 at
  `cdf669cf`; battery `states=45 matched=45`. The claim's before→after and its
  30-state named-conjunct sentence hold. Verdict: **improved** (coverage,
  verdict-only axis).

### R94-C2 (calibration) — NOT verified as filed (honest stop)

- Checker blob: `git show 6a2a1fdd:.ufo/evidence/round-94/conjunct-disposition-v94.py
  | sha256sum` → `6d4d270644b036cdd7106a5ab24be05b5d05ed01919f7f9ce24090977bdf9b7e`
  (rev 3, the operative instrument named by A1); manifest at `507adb5c` →
  `81e4a14bf939c8e8a371d3a9c1fb42f4165fa312bc33d9a0341eed0d1f7d81db`.
- Manifest: 19 rows, 17 `state`, 2 `unfalsifiable`; the 19 keys equal the counter's
  `C1_CONJUNCTS` keys exactly (no missing, no extra). Each of the 17 state rows maps to
  a committed receipt that moves its conjunct false (`selfpin` by the `self-pin-mismatch`
  setup token); 0 bad mappings. Both `unfalsifiable` reasons are >40 chars and name
  `state timeout` plus the `GATE_COMMIT`/`GATE_SHA256` digests (527 and 498 chars).
- `pre-freeze/c2-pos.out` and `landing/c2-at-landing.out` both print
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`; the `--min-falsifiable
  17` floor is in the command. Before: `c2-nowork-base.out` →
  `DISPOSITION_SETUP counter-absent-at-rev`, exit 2.
- The A4 witness: `c2-cheat-mechanism-word.rev1.out` prints
  `rows=19 falsifiable=0 unfalsifiable=19 findings=0` (the false green);
  `c2-cheat-mechanism-word.out` prints `findings=20` (19
  `reason-names-no-state-or-digest` + the floor) — the reason test can fail.
- **The claim's stated selftest tally does not verify.** The frozen claim
  (`.ufo/waves/round-94/claims.json`, C2 `battery_predicate`) and
  `plans/round-94.plan.md:165` require `DISPOSITION_SELFTEST: 8/8 pass`. The committed
  operative receipt `pre-freeze/c2-selftest.out` (first written at `2ad7ebb0`) prints
  `DISPOSITION_SELFTEST: 9/9 pass`: rev 2 added the `a4-prose-state-word-cheat` case
  (the 9th), and rev 3 kept it. A1 declares rev 3 operative but says “No claim wording,
  predicate, state expectation or target changes” — which is false for this tally. The
  report's claims table and SCORECARD print `9/9`, but `plans/round-94.plan.md:165`,
  `LOG.md` Round 94 (“8/8 (QUALITY 166)”) and `corpus/lessons/round-94.md`
  § Measurements (“8/8 pass”) still print `8/8`; the scribe's own finding
  (`.ufo/waves/round-94/w1/R94SC1.md` F5) named the mismatch and asked for a records
  reconciliation that did not land. The claim's core counts and the cheat witness hold,
  but its filed sentence is not the artifact's output. Under the closure rule a real
  wording falsification that is not narrowed in the record means the claim does not
  verify. Verdict: **unprovable** as filed; honest stop.

### Per-axis verdicts

| Claim | Axis | Verdict | Basis |
|---|---|---|---|
| R94-C1 | coverage | **improved** | 45/45 battery states, 30 named hostile conjuncts, gate-identity refusal; before/after re-derived from committed receipts |
| R94-C2 | calibration | **unprovable** | 19/17/2/0 and 17 state rows verified, but the frozen `DISPOSITION_SELFTEST: 8/8` sentence is 9/9 at the operative revision and no amendment narrows it |
| — | depth / operability / freshness / adjacency | unchanged | no score or claim in the round; `SCORECARD.md` diff shows `Scores unchanged: depth 10, calibration 8, freshness 9 (delta 0)`, no retirement, no capability row |

No owned axis is harmed (scores unchanged; no cross-domain file altered; `PROVINCE.md`,
`SKILL.md`, `AGENTS.md`, `SHONEN.md` untouched).

## Pre-file falsification ledger (Amendment 59)

- The closure prompt's exact command
  `python3 scripts/hyaku/prefile-falsification.py --lane tameshi --round 94` →
  `FINDING wave-missing .../.ufo/waves/round-94/w1-results.json` and
  `PREFILE-FALSIFICATION: SETUP findings=1`, exit 2. The wave is named `r94-w1`, not the
  validator's default `w1`.
- With the round's declared wave name (the report's own command):
  `python3 scripts/hyaku/prefile-falsification.py --lane tameshi --round 94 --wave r94-w1 --json`
  → `PREFILE-FALSIFICATION: pass claims=2 rows=14 attack_seats=6 findings=0`, exit 0.
- Ledger content: `.ufo/waves/round-94/claim-falsification.tsv` has 14 rows; both claims
  are covered; all six attack seats (R94R1, R94R2, R94C1, R94M1, R94SN1, R94CN1) appear
  for both claims; 5 `falsifies-wording` rows name A1–A5; the rest name reasons. The
  ledger's own pass is accepted with the wave-name caveat.
- The ledger does **not** cover the scribe's F5 (8/8 vs 9/9); the scribe is not an
  attack-role seat, but the artifact is a wave artifact and the mismatch is the C2
  wording failure above. The report's “Four rows are falsifies-wording” also conflicts
  with its own five-item list and the five `falsifies-wording` rows in the TSV.

## Discernment spot-check (LEARNING.md)

No new `corpus/SOURCES.md` row was admitted this round (182 → 182 content rows; 0 rows
added, 3 rows re-opened). The admit-side sample is therefore the re-open decisions; the
two reject decisions are sampled as required.

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S321 GFM §4.10 Tables | re-opened (A, `mined`, no status change) | `.ufo/evidence/round-94/sources/s321.html:4506-4507,4607-4608`; sha256 `b153d814…a220` | agree | Both quotes are verbatim at the cited lines: “single header row, a delimiter row separating the header from the data” (13 words) and “The table is broken at the first empty line, or beginning of another block-level structure” (15 words). The delimiter-width and remainder-row rules rest on this source; the re-open is sound. |
| S322 CommonMark §4.5 Fenced code blocks | re-opened (A, `mined`, no status change) | `.ufo/evidence/round-94/sources/s322.html:2732-2733`; sha256 `c85f56cc…0f0d` | agree | “A fenced code block begins with a code fence, preceded by up to three spaces of indentation.” (17 words) is verbatim at the cited lines; the fence-aware `coverage` rule rests on it. |
| S320 sha256sum(1) | re-opened (A, `mined`, no status change) | `.ufo/evidence/round-94/sources/s320.html:88`; sha256 `b968bc09…277b` | agree | “Print or check SHA256 (256-bit) checksums.” (6 words) is verbatim; the self-pin digest ground is correctly re-checked. |
| Candidate: keep the gate identity in the lane's spec + `pins.json` | reject | `.ufo/waves/round-93/w1/R93SN1-probe18.log` (`PROBE F1.foreign-gate-EXECUTED YES`; `pin=true pins=true green=true canary=true`) | agree | The probe shows the arrangement executing a foreign gate while every pin reads true; the rejection is exactly the round-92/93 killer class. Flip condition (an anchor outside the lane's commit graph) is correctly stated as unavailable. |
| Candidate: name the `canary` and `unstable0` conjuncts falsifiable | reject | `.ufo/evidence/round-94/pre-freeze/controls/timeout.out` (`green=false inconclusive0=false`; `canary=true unstable0=true`) | agree | The harshest battery state leaves `canary` and `unstable0` true; declaring them falsifiable would be wider than the battery shows. They remain `unfalsifiable` with state/digest reasons under QUALITY 166. |

The three re-opened rows' `used-by` changes are logged old→new in the lesson (§ Registry
changes); the census row count and status histogram match (`182` rows; `mined=148
queued=23 rejected=11`). No ≤25-word quote violation found.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → `tameshi ok …/corpus/SOURCES.md`, exit 0, with
the same pre-existing `W04` duplicate-URL warnings and the pre-existing `W01` S101
tier-C-mined warning.

## Trend verdicts (closure)

- **expansion: unchanged.** No knowledge entry was added (`git diff --name-status
  a8f0e14b 507adb5c --diff-filter=A -- corpus/knowledge/` → empty); the case note is
  modified only (Part 2/status block); SOURCES 182 → 182 content rows; frontier rows
  advanced: none. A source re-open is not expansion (`CORPUS.md` rule 4).
- **quality: improved.** QUALITY 163–168 are appended, each with an “Able to fail”
  receipt (the gate-identity `gate-foreign` refusal; the fence-aware coverage states; the
  delimiter/remainder states; the mechanism-word cheat; the post-freeze edit; the
  receipt-pointer erratum). The C2 instrument supersedes the weaker round-93 reason test
  (rev-1 cheat witness `findings=0` vs rev-3 `findings=20`); the battery is 45/45. Caveat:
  the 12 rule-level survivors (A8) and the C2 tally defect mean the quality move is real
  but incomplete; the record defects below must land.
- **discernment: improved.** The two sampled rejects and the three re-opens agree. The
  wave falsified six sentences of the record and each became an amendment (A1–A8), and
  the nine sentinel findings were reported rather than passed. Caveat: the scribe's F5
  was not amended, and five sentinel findings (F4–F7, F9) are not in the plan's routed
  list, so the report's “nine sentinel findings are routed” overstates; route them next
  round.

## Routed defects for next round (status-neutral except where marked)

1. **C2 tally (claim-affecting):** reconcile `DISPOSITION_SELFTEST: 8/8` in
   `plans/round-94.plan.md:165`, `LOG.md` Round 94 and
   `corpus/lessons/round-94.md` § Measurements with the operative `9/9` receipt; append
   an erratum/amendment naming the superseded sentence (never edit the frozen file).
   Until it lands, C2 is `unprovable` as filed.
2. **Report Sources & frontier count:** the report's “A 150, B 17, C 4, rejected 11” is
   not reproducible. Measured at both `a8f0e14b` and `507adb5c`: raw tier histogram
   `A=164 B=14 C=4`; excluding rejected `A=158 B=12 C=1`; `rejected=11`; total `182`.
   Give the command and correct the numbers.
3. **Prefile record:** the report says “Four rows are falsifies-wording” while listing
   five amendments and the TSV has five `falsifies-wording` rows; and the ledger's C2
   row for R94SN1 is `neutral` (“no C2 finding beyond the receipt write path”) although
   R94SN1 F1–F3 are C2 findings and A7 narrows that surface. Correct the count and the
   row's reason; A6/A7 are not in the report's five-row adjudication.
4. **Plan vs wave roster:** the frozen plan's §Wave declares 14 seats (including
   security-reviewer and simplifier); the executed wave is 12 (`w1-dispatch.json`
   `counts.total=12`; `r94-w1-results.json` 12 results). Policy is still met (12 in band
   8–16; attack 4/12 = 33 % by the role set, 6/12 = 50 % with sentinel/connector), but
   the plan and report must reconcile the two absent seats.
5. **Sentinel routing:** F4 (the grader reads the highest-index `.rerun-N.out`), F5 (the
   grader's `open()` follows symlinks), F6 (`make-pins94.py` symlink / `--lane ''`),
   F7 (empty `--rev` reads the index), F9 (`/tmp` canary dir) are not named in any
   “Routed to round 95” line; add them or correct “nine sentinel findings routed”.
6. **Pointer:** `corpus/lessons/round-94.md` § Measurements cites
   `pre-freeze/controls/C1-summary.txt` for the aggregate `C1_CONTROLS` line; the
   aggregate is in `pre-freeze/controls-run.log:47` (the summary carries the 45 `MATCH`
   rows). Fix the pointer.
7. **Command fidelity:** the frozen battery command uses `--jobs 6` (`claims.json`,
   plan §Controls); the report and SCORECARD print `--jobs 12`. The 45 states are the
   same, but record the invocation variance or use the frozen flag.
8. **Wave naming:** the validator's default wave is `w1`; this round's wave is `r94-w1`,
   so the closure's exact `prefile-falsification.py --lane tameshi --round 94` exits 2
   `SETUP wave-missing`. The report's command includes `--wave r94-w1` and passes; use
   the default name next round or carry the flag in the canonical command.

## SHONEN box checkability

All four boxes are `[~]` lane-asserted with evidence pointers; no `[x]` claimed. The wave
(12 seats; R94E3's 45-state replay from committed bytes; R94CN1 `no-overlap`) independently
supports boxes 2–4. A fully checkable non-author promotion review remains operator-owned;
the lane's `SHONEN.md` is not edited by this closure.

## Closure verdict

C1 verifies; C2 does not verify as filed (the frozen selftest tally is 8/8, the operative
committed receipt is 9/9, and no amendment narrows it). No axis is harmed. Lane status
`ok`; round **not admitted** — honest stop; the next round files the C2 narrowing and the
record corrections above.
