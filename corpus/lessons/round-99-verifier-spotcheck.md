# Round 99 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-08 (closure pass 2026-11-08T23:42Z)
lane-round: tameshi round 99; base `ff93fa16a1f65e66385b7c7f564f03b218d91ea2` → tip `e209a1fe7f42d866eddeb3c7a6d50ca1e49ff897`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-99/tameshi.md`
records revision R: `808a43778701cf1b05762584954d435481dc6fa2`

Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-08T19:52:55-03:00 launch tameshi round=99 pgid=552086 driver=hyaku-inline attempt=1`;
`2026-11-08T20:40:35-03:00 complete tameshi round=99; hyaku-inline attempt=1`.

## Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-99/tameshi.md` (fleet repo) | `tameshi-shokunin 62d918e5e95175f6ee30491266ed5588ea66ac8d 2026-11-08T20:39:38-03:00` (before the 20:40:35 completion line) | ok |
| `## SHONEN` heading, one line per box | `grep -c '^## SHONEN' <report>`; `grep -c '^- \[' SHONEN.md` | 1 heading; 4 report lines (`[~]`) for 4 SHONEN boxes | ok |
| cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <full> master` for ff93fa16 46651051 ab598d03 27a5e49e 808a4377 7cd85a42 e4cfbbb1 cec42d97 e209a1fe 3b7ae127 | all resolve; all `anc=0` | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state tameshi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=e209a1fe… remote=e209a1fe… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `e209a1fe7f42…` | ok |
| round commits | `git log --format='%h %an %s' ff93fa16..e209a1fe` | 8 commits, all `tameshi-shokunin` | ok |
| prompt carries template contract | `grep -n` over `.ufo/prompts/tameshi-round-99.md` | 1002 lines; `SHONEN` contract at :118, §6 hyaku addendum at :141, SHONEN-heading check at :521 | ok |
| pre-existing files only appended | `git diff --numstat ff93fa16 e209a1fe \| awk '$2>0'` | empty (zero deleted lines); modified pre-existing files: LOG.md, SCORECARD.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md — all pure appends | ok |

Status: **ok** (real report with checkable commits; not a marker).

## Pre-file falsification ledger (step 2b)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tameshi --round 99`
→ `PREFILE-FALSIFICATION: pass claims=2 rows=20 attack_seats=8 findings=0`, exit 0.
Ledger `.ufo/waves/round-99/claim-falsification.tsv`: 10 `falsifies-wording` rows (C1: R99R1,
R99SN1, R99C1, R99S1; C2: R99R2, R99E2, R99M1, R99C1, R99CN1, R99RV1), each naming
`plans/round-99.plan.md` and a narrowing/repair; sampled R99R1 (A2/A3/A4) and R99R2 (A1) — both
resolve to rows of `plans/round-99.plan.md` §Amendments (line 184 ff.). No failing row to adjudicate.

## Claims (step 2)

Both claims rest on lane **instruments** (no `tools/registry.json` gate row; the lane's own
Planned note says so), not registered sibling gates, so I re-executed them read-only from
the blob bytes at R (`git show R:<tool> > tmpdir`, `python3 -I`, `--repo <lane> --rev R`;
the tools read git blobs, no worktree write) and also ran independent plain measurements.

Tool digests at R: `git show R:tools/tally-reconcile.py | sha256sum` → `a1c50bb4…b482`;
`git show R:tools/control-assertion-audit-v2.py | sha256sum` → `7527e40f…6368` — match the report.

### C1 — calibration: tally-receipt reconciler — **re-measured, verified**

| measurement | reported | observed by me |
|---|---|---|
| before: `git -C tameshi-shokunin grep -c TALLY_RECONCILE ff93fa16 -- .` | empty, rc 1 | empty, rc 1 |
| twelve records (round-93..98 lessons+plans) at R | `records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`, exit 1 | identical line, rc 1 |
| sole mismatch | `corpus/lessons/round-94.md:66 … claimed=8/8 … observed=9/9` | identical (`c1-population.out` also matches) |
| `--record corpus/lessons/round-94.md` only | `mismatched=1`, exit 1 | `records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0`, rc 1 |
| `--record corpus/lessons/round-93.md` only | `matched=1`, exit 0 | `… matched=1 mismatched=0 …`, rc 0 |
| `--selftest` | 25/25 | `TALLY_RECONCILE_SELFTEST: 25/25 pass` |
| independent plain check of the mismatch | — | `git show R:corpus/lessons/round-94.md \| sed -n 66p` → `DISPOSITION_SELFTEST: 8/8 pass … (.ufo/evidence/round-94/pre-freeze/c2-selftest.out)`; that receipt at R prints `DISPOSITION_SELFTEST: 9/9 pass` (9 SELFTEST case lines). The mismatch is real. |

Axis calibration: **improved** — the lane now holds an able-to-fail check that catches the
exact self-assessment-vs-receipt overreach class two closures (r94, r98 D2) found by eye.

### C2 — coverage: recorder-alias site audit — **re-measured, verified**

| measurement | reported | observed by me |
|---|---|---|
| before: `git grep -c CONTROL_ASSERT_RECORDERS ff93fa16 -- .` | rc 1 | empty, rc 1 |
| v2 on `.ufo/evidence/round-99/c2/alias-driver.py` at R | `aliases=1 … names=add,record`; `sites=4 measured=3 literal=1 unmeasured=1`, exit 1 | `CONTROL_ASSERT_RECORDERS aliases=1 ambiguous=0 partial=0 names=add,record`; `CONTROL_ASSERT sites=4 measured=3 literal=1 unmeasured=1`; rc 1 |
| round-98 audit (unmoved) on the same driver | `sites=2 measured=2 literal=0 unmeasured=0`, exit 0 | identical, rc 0 |
| v1 vs v2 on `controls98.py` / `controls97.py` | site+summary lines identical | identical after dropping the v2-only `RECORDERS` line; v2 prints `sites=15 measured=15 literal=0 unmeasured=0` and `sites=15 measured=14 literal=1 unmeasured=1` (real output, not refusals) |
| `--selftest` | 38/38 | `CONTROL_ASSERT_V2_SELFTEST: 38/38 pass` |

Axis coverage: **improved** — a declared round-98 blind edge class (renamed recorder) is now
governed by the audit, with the old audit kept as the unmoved comparison.

Evidence-verified only (not re-run): `RECEIPT_BIND … receipts=16 bound=16 … unbound=0`
(`records-aux/receipt-bytes-bind.out`, read); discrimination "4/8 and 9/11 new arms fail under
frozen bytes" (`records-aux/a1-a9-discrimination.out`, not re-derived).

### Owned axes, harm check

`git diff ff93fa16 e209a1fe -- SCORECARD.md`: only two appended capability rows and an
appended `## Round 99` section (scores unchanged: depth 10, calibration 8, freshness 9; D1
append-only correction of the r94 cell). No pre-existing line deleted anywhere in the lane.

| axis | verdict |
|---|---|
| calibration | improved |
| coverage | improved |
| operability | unchanged |
| depth | unchanged |
| freshness | unchanged |
| adjacency | unchanged |

## Discernment spot-check (step 3)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S324 Nuijten et al. 2016 | admit (`mined`, tier A) | live `curl` of the Europe PMC REST URL in the row; parsed `resultList.result[0].abstractText` | **agree** | title matches; the 25-word quote is present verbatim; the prevalence finding grounds C1's premise that recorded figures drift from their computation often enough to recompute; committed snapshot `s324.json` sha256 `346dcf46…0349` matches the row |
| S326 Brown & Heathers 2016, GRIM | reject (tier A, `rejected`) | live `curl https://api.crossref.org/works/10.1177/1948550616673876`; tag-stripped `abstract` | **agree** | the 25-word quote is present verbatim; GRIM tests arithmetic feasibility of means of integer data, while the lane's tallies are integer counts copied from receipts — nothing to bind; reason and flip are concrete |
| S325 statcheck FAQ (SOURCES row quote check) | admit (`mined`) | live `curl -L http://statcheck.io/`, tag-stripped, whitespace-collapsed | **agree** | both quotes present verbatim ("statcheck is a "spellchecker" for statistics. … degrees of freedom." 21 words; "Statcheck usually can't find statistics in tables." 7 words), each ≤25 words |

Registry: `git show <rev>:corpus/SOURCES.md | grep -cE '^\s{0,3}\| *S[0-9]+'` → 183 at
`ff93fa16`, 186 at `e209a1fe`; diff adds exactly S324-S326, no existing row touched.
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok`,
exit 0 (pre-existing W04 duplicate-url and one W01 warnings, none on S324-S326).

## Trend verdicts

- **expansion: improved** — new knowledge entry `corpus/knowledge/tally-receipt-reconciliation.md`
  on ground the coverage map did not hold (README `## Round 99` row), citing two `mined` rows
  re-opened above; two capability rows admitted to SCORECARD; census 183 → 186, exit 0.
- **quality: improved** — falsified records marked rather than left standing: D1 append-only
  SCORECARD correction of the r94 cell, D2 erratum for the r98 `18/18` freeze claim; r98
  registry red/green pairs re-verified by a non-author seat (D4); QUALITY 178-179 appended; no
  admitted entry failed its re-check here.
- **discernment: improved** — this spot-check agrees with the gate on the admit (S324, S325) and
  the reject (S326).

## Defects (status-neutral) and routed items for round 100

1. A12 was recorded after the records run (`e4cfbbb1`, after landing `7cd85a42`) although the
   §Amendments header says rows are added "before the records run". It is disclosed and only
   narrows a declared-limit description (no tool byte, number or predicate changed), so no claim
   is affected — route: a post-data amendment gets its own marked sub-table or goes to the next
   round's plan.
2. C1's coverage is thin by its own measurement: 19 of 28 tallies `uncited` and 6 `unbound`; only
   2 of 28 tallies are confirmed. The claim is worded as a count, so it verifies, but round 100
   should not read the reconciler's silence as agreement (the lane's own S325 lesson).
3. Neither round-98/99 audit has a `tools/registry.json` row (lane Planned note) — they remain
   instruments, not gates; register them before any claim rests on them as gates.
4. The lane now holds two citation-resolution grammars and two binding walkers (A8); route the
   consolidation or a cross-check arm.
5. SHONEN: all four boxes remain `[~]` lane assertions; boxes 1, 2 and 4 look checkable by a
   non-author reader (SKILL.md tables/sources, LOG.md end-to-end entries, PROVINCE.md) — operator
   promotion review is the owner; nothing promoted here.
