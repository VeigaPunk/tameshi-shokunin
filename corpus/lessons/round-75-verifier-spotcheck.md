# tameshi round 75 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-04 against lane tip `587ee30e20fa540f255474223d40da70c1339349`
(branch `master` == `origin/master`), base `21ef81e99966198cf8cdb2c6d8e56aa3c482da56`.
Every reading below was taken by this verifier from committed bytes with plain
git/awk/python counts; the lane's own gates and selftests were read as committed
receipts and were **not executed** (PROTOCOL §Gate standard, Closure consequence).
Dispatch/complete digest (from the mutable `.ufo/watchdog.log`, copied verbatim):
`2026-11-03T23:15:32-03:00 launch tameshi round=75 pgid=2160140 driver=hyaku-inline attempt=1`;
`2026-11-03T23:56:31-03:00 complete tameshi round=75; hyaku-inline attempt=1`.
Verdict: **rejected-honest-stop** — C2 verifies as declared; C1 does **not**
verify against the kill rule declared before data (Correction 1 was appended
after the L1's own battery measured the original rule failing); no axis is
harmed; the corrected-predicate measurements are real and are credited below.

## 1. Step-1 conformance

| Check | Result | Evidence (this verifier's own run) |
|---|---|---|
| Report committed in the fleet repo by the lane identity | PASS | `git log --format='%an %ae %H' -- .ufo/reports/round-75/tameshi.md` → `tameshi-shokunin <tameshi@shokunin.local> a98157bd34931211c8695cd3de4f5a063aa8f272` |
| Report lands after the lane work | PASS | lane tip `587ee30e` committer date 2026-11-03 23:54:16 -0300; report commit `a98157bd` 23:55:51 -0300 |
| `SHONEN` heading, one line per box | PASS | `grep -c '^## SHONEN'` → 1, followed by four `[~]` lines; `SHONEN.md` carries four boxes (all `[~]` unchanged, blob identical base→tip) |
| Every cited lane commit exists and is an ancestor of the branch | PASS | base + 8 round commits, each `git merge-base --is-ancestor <h> master` → true (`640d3fcc 7745d0e0 82f7a809 4e610748 08f09759 a9e6eef4 72b1ef6c 587ee30e`) |
| Lane repo clean, nothing uncommitted, pushed | PASS | `jj-lane.sh state` → `ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` → `587ee30e…` |
| Round range matches the report | PASS | `git rev-list --count 21ef81e9..587ee30e` → 8; the landed-changes table carries all 8 |
| Prompt carries the template contract | PASS | `templates/round-prompt.md` (140 lines) vs the dispatched prompt: only substitution lines differ (`{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}`); §3 states the MISSION L2 floor verbatim (≥8 subagents, one batched call — MISSION.md:55 agrees); the five child-lane items present (report path §4, commit-before-report "the report lands last and cites the pushed lane hash", SHONEN pre-commit grep, measured-commit citation rule, write scope §3); run-15 §6 addendum and §7 scratch discipline follow |
| Real report, not a marker | PASS | work performed, per-claim counters, 8-commit landed table tied to `LOG.md`, evidence pointers that resolve, trend verdicts, SHONEN |
| Round shape | PASS | `w1-results.json` 12 records, all outputs non-empty (0 dead seats); `w1-dispatch.json` `counts={spawn:12,resume:0,total:12}`, 12 tasks in one call, no `model` key, every task leads with `/skill:godspeed`; seat reports `T75W1{E1..E4,S1,SC1,R1,R2,C1,M1,CN1,SN1}.md` = 12; roles 4 executor + 1 scribe + 1 scout + 2 reviewer + 1 critic + 1 mutation-tester + 1 connector + 1 sentinel; attack seats 4/12 = 33.3 % |

## 2. Per-claim re-check

Two claims, distinct axes, frozen in `plans/round-75.plan.md` at `640d3fcc`
(before the wave). Neither is exploratory. Corrections 1 (`7745d0e0`) and 2
(`82f7a809`) were appended while the wave was running; the lesson's settlement
errata states the broad "pre-data" wording is too broad and names both frozen-text
defects as admission defects for this closure. Both are judged here on the
predicates declared before data (round-prompt §9: "A rule changed after any seat
has scored is not the claim's rule"; fleet precedent kumitate r42).

### R75-C1 — operability: the round-74 survivors become measured arms

**Judgment: NOT verified as declared.** The frozen kill rule (ii) — "any mutant is
killed by an arm other than the one it is named against" — fails on the landed
bytes. Committed evidence, re-read by this verifier:

- The L1's own pre-freeze battery `.ufo/evidence/round-75/l1-c1-battery.txt`
  (landed in the same commit `7745d0e0` as Correction 1) already prints the
  collateral matrix: `m2` → arm13 + arm16; span-rule → arm14 + arm17 + arm18. The
  rule was therefore amended in response to a measurement that showed it failing;
  the wave critic `T75W1C1` §4a independently scored the same matrix against the
  frozen text ("C1 fails as frozen") before the correction.
- The landed battery receipt `c1-landed-battery.txt` confirms the corrected-rule
  matrix on the landed bytes: each of the three R75 mutants fails only its named
  arm (17/18 each); `m2` → arm13+arm16 (16/18); span-rule → arm14+arm17+arm18
  (15/18); seat-reports → arm15 (17/18). That is exactly what Correction 1 says
  the original rule (ii) cannot tolerate.
- The critic (`T75W1C1` §4a) also proved the arm16↔m2 collision is intrinsic to
  the frozen fixture design (any span-delimiting arm must rely on `delimited()`
  being honest; m2 makes it unconditionally true), i.e. the original rule was
  unsatisfiable by construction once the arms were frozen — a predicate-design
  defect that was provable before any data.

**What verifies (corrected predicate, evidence-verified, gates not executed):**
`git show 587ee30e:tools/wave-reconcile.py | sha256sum` →
`bf10c0e49…a7f791`, equal to the receipt's `MUTATE_TARGET`; arm assertions
15 → 18 with `arm16/17/18` present (`grep -cE '^\s+(arm|arm_raises)\('` → 18);
the spec is the three base `@defect` blocks byte-identical plus three appended
blocks (`diff 21ef81e9..587ee30e -- tools/wave-reconcile-mutants.spec` shows only
the banner comment and the appended blocks); the committed receipt prints
`CONTROL: GREEN`, `MUTATE_RESTORE: OK` with identical before/after/pristine
sha256, and `MUTATE: DONE (… defects=6 killed=6 survived=0 inconclusive=0
kill-rate=100%)`; the rule (iii) baseline receipt `c1-arms1-15-diff.txt` shows
arms 1–15 unchanged.

### R75-C2 — calibration: the declared live figures re-derive from their instruments

**Judgment: verified as declared.** Before and after re-derived from committed
receipts and static tuple comparison:

- `.ufo/evidence/round-75/exact-final-exits.json` entry 1 (`--doc-rev 21ef81e9…`):
  exit **1**, `SELFSTATE: rows=17 match=9 stale=8 unexpected=7` (this also
  corrects the `c2-before.txt` pipeline-tail exit-0 defect the report discloses).
  Entry 2 (`--doc-rev 72b1ef6c…`): exit **0**, `rows=17 match=16 stale=1
  unexpected=0`, 17 per-row lines, every live row `match`, frozen row
  `expect=stale measured=stale ok`. Entry 3 (coldread at `72b1ef6c`): exit 0,
  `credited=64/64 probe_mismatches=0`.
- Tuple freeze (Correction 2) re-measured statically: the landed
  `tools/selfstate-freshness.json` carries exactly 17 rows — 16 `mode: capability`
  + 1 `mode: span` (`r74-frozen-addr-six`, `expect: stale`); the 16 live rows are
  set-equal to the committed pre-freeze prototype
  `.ufo/evidence/round-75/selfstate-control-scan.py` SPECS on
  (capability, figure regex, instrument path, argv); every instrument is pinned at
  rev `21ef81e9`.
- Nine SCORECARD capability cells superseded in the diff (7 in-population:
  commit-bind `4/4`→`7/7`, quoted-line `4/4`→`5/5`, arm-liveness `4/4`→`5/5` and
  `rows=3`→`rows=9`, anchor-drift `rows=4`→`rows=16`, line-pointer `rows=8`→`rows=12`,
  additivity `rows=6`→`rows=11`; 2 out-of-population: mutation sweep runner
  `80/80`→`107/107`, wave-record reconciliation `12/12`→`18/18`), each a full-row
  supersession, historical rows untouched.
- The critic's attack and its disposition are committed: `controls-c75b.txt`
  shows a loose-token manifest at **base** printing the full expected after-state
  with zero repairs — the counter as first written was reachable without the
  claimed work; Correction 2's tuple freeze is the fix, and the landed manifest
  passes it. The freeze was appended after the critic scored (procedural
  admission defect, disclosed; the target `rows=17 match=16 stale=1
  unexpected=0` never changed and the landed bytes satisfy every kill rule
  (i)–(v) as originally written).
- Selftest tally `SELFSTATE_SELFTEST: 10/10 pass` and the instrument-mutant
  battery are evidence-verified from committed receipts, not executed; the
  settlement errata honestly records that the `--doc-rev`-ignored mutant survives
  (4/5 killed, not 5/5).

**No-harm re-derivation:** cold-read credit `64/64` at base → `48/64` at
`08f09759` (receipt `coldread-red-r75.out`) → `64/64` at `a9e6eef4`
(`coldread-tip-r75.out`) and at `72b1ef6c` (`exact-final-exits.json`);
rekey batch `r75-batch-1` rekeys 16 sections, ledger 883 → 899
(`rebind-stdout-r75.txt`, `rekey-summary-r75.json`); the final commit `587ee30e`
is receipts-only (`--stat`: 2 files under `.ufo/evidence/round-75/`), so pinned
monitor inputs are unchanged at the tip. `SKILL.md`, `PROVINCE.md`, `SHONEN.md`,
`AGENTS.md`, `corpus/README.md` are byte-identical base→tip; `LOG.md` (+101/−0),
`corpus/QUALITY.md` (+35/−0, criterion 125), `corpus/lessons/round-75.md` (+206/−0),
`corpus/SOURCES.md` (+20/−1, the documented S006 `used-by` cell), `SCORECARD.md`
(+80/−8, the nine supersessions + two round rows), `tools/registry.json` (+61/−6)
— no owned axis content lost.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | unchanged | `SKILL.md` blob identical base→tip; no new decision-table case |
| coverage | unchanged | `PROVINCE.md`, `corpus/README.md` identical; no frontier move; report states both |
| operability | **unprovable-but-better** | C1 fails as declared (original kill rule (ii) amended after measurement showed it failing); under the corrected, disclosed rule the improvement verifies from committed evidence: 15→18 arms, 6/6 named-arm kills, control GREEN, byte-identical restore, arms 1–15 unchanged. Named non-author reviewer: this closure |
| freshness | unchanged | S006 re-opened with fresh quotes but `recheck`/`verified-at` stand (append-only); no stale skill item flagged or fixed |
| calibration | **improved** | C2 verifies as declared: before `9/8/7` exit 1 → after `16/1/0` exit 0 over the frozen 17-row tuple population; nine stale cells superseded; score held at cap 8 per saturation (critic §5: "8 → 8 (held at cap)") |
| adjacency | unchanged | connector `T75W1CN1` read-only; no sibling repo touched; `PROVINCE.md` identical |

**No axis is harmed.** The round's own defects (freeze timing, pipeline-exit
record, EOL erratum for r74) are disclosed in the report, `LOG.md` and the
lesson's settlement errata.

## 4. Discernment spot-check (`corpus/lessons/round-75.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S006 re-open (admit) | admit | live `https://raw.githubusercontent.com/BWBama85/shmutant/master/README.md` fetched by this verifier (HTTP date Wed, 04 Nov 2026 03:11:34 GMT; 13,970 B; sha256 `960577288ed5…54e2`) and the committed extract `.ufo/evidence/round-75/sources/s006-shmutant-readme.md` — live bytes and extract are byte-identical | **agree** | all three located quotes occur verbatim at extract lines 24 ("**witness**: the assertion that must fail.", 6 words), 29 ("The suite went red **on its witness**. The test detects the defect.", 12), 31 ("The suite went red, but not on its witness. Caught by accident, not by the assertion that claims to cover it.", 21); the supporting `unapplied` locator at line 38 is verbatim (13 words); all ≤25 words; the row's status/recheck/anchor stand as written; `used-by` old→new logged in the Gate and the SOURCES Round-75 note |
| New shmutant row at current bytes (reject) | reject | the S006 row cells (`source` = same URL, `scope` = shmutant's own bash mutation verdict semantics) and the live page | **agree** | same URL, same document, same scope → within-scope duplicate under CORPUS.md rule 2; the S289/S293 precedent and the named flip condition (S006 retired or page superseded) make the re-open the contract-shaped act |
| Newly written `SOURCES.md` row quote | check | n/a — **no new row this round** (re-open in place; rows 164 → 164) | **agree** | census row count unchanged; the only cell edit is the documented S006 `used-by` append |
| Census validate | gate | this verifier's own run of `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | **agree** | exit 0, `tameshi ok`, 164 rows (base and tip), 18 × W04 + 1 × W01 S101 warnings only — matches the report's before/after blocks |

## 5. Trend verdicts

- **expansion — unchanged.** No `knowledge/` entry, no capability-table row (the
  lane explicitly declines acquisition credit for the C2 instrument), no frontier
  move; registry rows 164 → 164; `corpus/README.md` identical.
- **quality — improved.** Three new discriminating arms with a committed 6/6
  named-arm kill battery and byte-identical restore; seven in-population stale
  figures re-derived from their instruments plus two out-of-population record
  repairs; cold-read credit restored 48/64 → 64/64 with a receipts-only tip; the
  r74 EOL rewrite disclosed as a LOG erratum; known survivors (`M-C` class,
  printed-less seat_reports bypass) are named, not argued away.
- **discernment — improved.** This verifier agrees with the round's admit (S006
  re-open) and its reject (duplicate row); the critic's scored counterexample
  (control 4) was adopted as a control freeze rather than argued away; four
  mistakes are mined in `## Mistakes` with criterion 125 grounded in them; the
  freeze-timing and pipeline-exit defects are disclosed in a settlement errata
  instead of being relabelled pre-data.

## 6. Routed defects for the lane (status-neutral; next round)

1. **Predicate design: kill rules must be satisfiable by construction before
   data.** The arm16↔m2 collision was provable from the frozen fixture table
   (critic §4a) before any battery ran. A rule shown unsatisfiable mid-round is a
   defect disclosure and an honest stop, never a rule amendment (kumitate r42;
   round-prompt §9). C1 is judged failed-as-declared for round 75.
2. **Freeze counter tuples in the plan, not after a scored counterexample.**
   Correction 2's tuple freeze was the right fix and the landed manifest passes
   it, but a post-score counter change cannot certify the claim's counter;
   declare (capability, regex, instrument, rev, argv) tuples in the frozen plan.
3. **Round-73 routed items still open.** `plans/round-73.plan.md` still carries
   the contradicted kill-rule sentence with no erratum; the r73 report's 22-of-23
   table and 19-vs-18 W04 counts were properly corrected in this round's report
   (the correcting-round form) but the r75 lesson still lists them as open —
   reconcile the queue.
4. **Round-74 S294 used-by old→new lesson append still open** (r74 spotcheck
   defect 5); append it to `corpus/lessons/round-74.md` (append-only).
5. **Registry home still unpaid.** `SKILL.md`'s registry table still lists none
   of the round-74/75 instruments; the `tools/registry.json` rows lack verdict
   map, pinned-value path, write scope and owner (carried from r73/r74 routings).
   The hermetic tip run is `held=57/59 superseded=7` exit 1 with two inherited
   red rows (`sources-census`, `verify-round15`) — status-neutral gate redness,
   verified as committed evidence, never executed.
6. **Dated-literal cells** (`pin-disposition` 18/18→19/19, `evidence-disposition`
   34/34→66/66) and the stale r17 supersession figures (`95/95`, `56/56`) —
   already routed to round 76 by the lane; keep on the queue.
7. **Selftest survivor** `--doc-rev`-ignored (4/5 instrument mutants killed, not
   5/5) — already named as a round-76 carry in the settlement errata; add the
   CLI-level arm.
8. **Load order** not fully in the requested order (lane self-reported
   procedural defect) — keep as process debt.

## 7. Closure

Conformance: real report, lane identity `tameshi-shokunin`, `SHONEN` heading with
four `[~]` lines, all 8 round commits + base ancestors of `refs/heads/master`,
lane clean and pushed (`ahead=0`), prompt a faithful template rendering plus the
run-15 addendum, report lands after the tip. Claim R75-C2 verifies as declared —
before/after re-derived from committed receipts, tuple freeze re-measured
statically, nine cell supersessions in the diff. Claim R75-C1 does **not** verify
as declared: the original kill rule (ii) fails on the landed bytes and was amended
after measurement (L1 pre-freeze battery and critic both scored the failure
first); under the corrected, disclosed rule the improvement is real and fully
evidence-backed. No axis is harmed. **Rejected — honest stop** (the lane
disclosed both defects itself and asked to be judged on the original predicates).

No promotion or mint: SHONEN boxes remain `[~]` lane assertions and promotion
stays operator-owned. The boxes remain checkable by a non-author, but this
closure writes no marks.
