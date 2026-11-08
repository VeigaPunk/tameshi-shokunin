# Round 98 — non-author verifier spot-check (tameshi)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-08
report: `.ufo/reports/round-98/tameshi.md` (fleet repo; lane-identity commits `0f465374`, `51662c19`)
lane base: `034240a591575167f0747ad7372a1f4b9cd33a58`; lane tip: `28e7bda908bcef05261961f744dfe11edbf099a9`;
records revision R: `3b7ae1272d161aa0297e1d04b2b7ec5b40112912`

The closure prompt gave lane HEAD before = after = `28e7bda9` (driver snapshot taken after
three `lane-dead-no-report` retries). All before→after measurements below use the round's real
base `034240a5` (report line 4, `claims.json` `base`, first parent of `6b1428c8`).

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-98/tameshi.md` | `tameshi-shokunin 51662c19…`, `tameshi-shokunin 0f465374…` | ok |
| SHONEN heading, one line per box | `grep -c '^## SHONEN' <report>`; `grep -c '^- \[' SHONEN.md` | 1; 4 boxes / 4 `[~]` lines | ok |
| cited lane commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for 034240a5 6b1428c8 d32043ec 764aca97 cdaecece 3b7ae127 fa2d2169 647408f0 4b8f4ed1 28e7bda9 07e50d6d 0b19af5f 29734beb | all 13 ok | ok |
| lane pushed, clean | `jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; empty; `28e7bda9…` | ok |
| commits authored by lane | `git log --format='%an' 034240a5..master` | 9 × `tameshi-shokunin` | ok |
| prompt carries template contract | `grep` of `.ufo/prompts/tameshi-round-98.md` | L2 minimum (:82), report path (:101), SHONEN (:118, :521), push scope + L0 (:131-139), write scope (:448), lands-last (:516) | ok |
| pre-file falsification ledger | `python3 scripts/hyaku/prefile-falsification.py --lane tameshi --round 98` | `PREFILE-FALSIFICATION: pass claims=2 rows=19 attack_seats=7 findings=0`, exit 0 | ok |
| census | `scripts/sources-census.sh validate --root … tameshi` | `tameshi ok …/corpus/SOURCES.md`, exit 0 (W01/W04 warnings only, none on round-98 rows) | ok |

Not a marker report: nine landed lane commits, committed receipts.

## 2. Claims

### C1 — calibration (lowest non-retired, pinned 8): measurement-derived control codes

Re-measured (plain commands over committed bytes, not the lane gate):

- before: `git grep -c CONTROL_ASSERT 034240a5 -- .ufo/evidence` → rc 1; `git show
  034240a5:.ufo/evidence/round-97/controls97.py | grep -n c2-nowork-absent` →
  `156:    add("c2-nowork-absent", 0,` — literal code, as reported.
- after: independent AST count (my own `ast.walk` over bare-name `add(...)` calls, blob at R):
  `controls98.py` → `15 sites; constant-code sites: []`; `controls97.py` → `15 sites;
  constant-code sites: [(156, "'c2-nowork-absent'", '0')]`. Agrees with the audit's
  `sites=15 measured=15 literal=0` vs `sites=15 measured=14 literal=1`, line 156.
- repaired line at R: `159: add("c2-nowork-absent", g.returncode, …, 1)`.
- digests: `git show R:<path> | sha256sum` → audit `82c2e54b…`, driver `f1c1db0e…`; identical at
  tip; equal to `claims.json` `instrument_sha256`/`driver_sha256`.

Evidence-verified (gate not executed, §Gate standard): `records/c1-audit-controls98.out`
(`sites=15 measured=15 literal=0 unmeasured=0`, `rc=0`), `records/c1-audit-r97-driver.out`
(`measured=14 literal=1 unmeasured=1`, line 156 `class=literal detail=constant`, `rc=1`),
`records/c1-audit-selftest.out` (18 PASS / 0 FAIL, `18/18 pass`, `rc=0`),
`records/controls98-run.out` (`CONTROLS98 states=18 matched=18 mismatched=0`, `rc=0`);
`.ufo/waves/round-98/records-rev.txt` = R. Predicate unchanged freeze→R (`claims.json` at
`764aca97` vs `3b7ae127`); only the selftest tally (12→18) and the instrument digest moved, via
amendments A5/A6 from wave artifacts — tightening only.

Verdict: **verified** → calibration **improved**.

### C2 — operability: all six guard refusal classes receipted end to end

Re-measured:

- before: `git grep -c '<token>' 034240a5 -- .ufo/evidence` for `GUARD_REFUSALS`,
  `GUARD_SETUP state-unbuildable`, `GUARD_SETUP limit-mechanism-missing` → rc 1 each. Unscoped
  (`-- .`) the two class tokens return rc 0 (7 non-receipt files: round-97 claims/plan/wave prose)
  — the "receipt" scope is load-bearing (see D3).
- frozen tool: `git show R:.ufo/evidence/round-97/c2/guard-inertia.py | sha256sum` →
  `634997d0…`, last changed at round-97 `406119cd`; each of the six class names appears in its bytes.
- battery digest at R and tip `de94cbcc…` = `claims.json`.

Evidence-verified: `records/c2-refusals-positive.out` (six `GUARD_REFUSAL <class> rc=2
token=ok`, `GUARD_REFUSAL_POSITIVE rows=10 rc=0`, `classes=6 refused=6 wrong=0 positive=ok`,
`rc=0`), `records/c2-refusals-red.out` (`GUARD_REFUSALS_RED state-unbuildable observed=missed
rc=0`, `refused=5 wrong=1 … red=state-unbuildable`, `rc=1`), `records/c2-refusals-selftest.out`
(`9/9 pass`). R98M1's mutation matrix leaves 5/10 battery mutants alive after repair (disclosed
in SCORECARD and the lesson); the claim wording does not assert mutation strength.

Verdict: **verified** → operability **improved**.

### Harm check

`git diff 034240a5 28e7bda9 -- SCORECARD.md`: 60 insertions, 1 deletion; scores unchanged
(depth 10, calibration 8, freshness 9). The one deletion is an in-place edit of a filed round-94
row (D1) — a conformance defect, status-neutral by closure precedent, not an axis regression.
SOURCES: one cell (`S012 used-by`) changed, an in-place-allowed cell.

| axis | verdict |
|---|---|
| calibration | improved |
| operability | improved |
| depth | unchanged |
| coverage | unchanged |
| freshness | unchanged |
| adjacency | unchanged |

## 3. Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S012 (admit: re-opened, kept `mined`, cited by new `knowledge/control-assertion-anchoring.md`) | admit | `curl https://arxiv.org/abs/2608.17214` → 200, 42588 B, sha256 `fb6f384d…` (identical to the lane's snapshot) | agree | the 16-word quote "A test oracle that obtains its expected value from the system it is judging cannot fail." is present under the stated renderer; the row's `teaches` facts (state-anchored, 8 of 46, 366 mutants) are all in the abstract; the source does ground C1's class |
| S009 (reject: not promoted, kept `queued`, `teaches` clause flagged as ungrounded) | reject | `curl` default UA → 403, 5517 B; declared UA → 200, 42254 B (both as the lane recorded) | agree | the 14-word quote is present; "more than 7%" and "approximately 30%" are present but "identical compiled output" is absent, so refusing to cite the row and routing a superseding row instead of an in-place `teaches` edit is the correct call |

Registry row re-opened: no row was newly written this round (183 → 183). The touched row S012
(diff = `used-by` cell only) was re-opened above; its lesson quote is 16 words (≤ 25).

## 4. Trends

- **expansion: unchanged** — SOURCES 183 → 183, no frontier row advanced (census-before/after).
- **quality: improved** — new knowledge entry grounded on a live-verified source, QUALITY appended,
  two able-to-fail instruments with committed red arms, registry-cell audit for D-1's class.
- **discernment: improved** — the wave falsified C1's classification clause and C2's pin/red
  wording (ledger: 19 rows, 7 attack seats, 6 `falsifies-wording` rows each naming a narrowing);
  both sampled gate decisions agree on re-open, including the S009 `teaches` caveat.

## 5. Routed defects (lane fixes next round; status-neutral)

- **D1** `fa2d2169` rewrote the filed round-94 `R94-C1` verdict cell in place
  (`**verified under the amended wording**` → `**… (A3-A10)**`); round 94 had amendments A1-A8
  only, so the cell is now false. Append a named correction restoring the round-94 text.
- **D2** report lines 31-32 say the C1 selftest is `18/18` at the freeze
  (`pre-freeze/c1-audit-selftest.out`); that file prints `12/12` (v1 audit; frozen
  `battery_predicate` 12/12). Erratum in the round-99 report.
- **D3** before receipts `pre-freeze/c1-before-token.out`, `c2-before-*.out`,
  `c1c2-before-tokens.out` hold only `rc=1` — no command, pattern, tree or scope; the
  `.ufo/evidence` scope that makes C2's before true is absent from `claims.json` C2 `before`
  (also R98C1). Record the command line inside each receipt.
- **D4** dead seat R98E4 (registry re-check) — the registry red/green pairs are L1-run only;
  re-run them under a non-author seat.
- **D5** carried limits: battery leaves 5/10 mutants alive (R98M1); audit is blind to renamed
  recorders and `want=code` tautology (A2/A6).

SHONEN: all four boxes `[~]`; boxes 1-2 look checkable by a non-author from committed artifacts
(operator-owned promotion).
