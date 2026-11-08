---
author: hyaku closure (non-author integrator, @m_zfl)
---

# Round 97 verifier spot-check — non-author closure (tameshi r97)

Lane HEAD verified: `29734beb095984038d66bb5dd4d149d81378de31` (branch `master`; `jj-lane.sh state` →
`branch=master local=29734beb… remote=29734beb… ahead=0 behind=0 head=detached tracked=0 untracked=0`;
`git status --porcelain` empty; `git ls-remote origin refs/heads/master` agrees).
Pre-round lane HEAD as dispatched: `0b19af5f8666f9c54a437f511e9155a66d0d418d` (integrator r96 spot-check);
the round's own measurement base is `07e50d6d0142b21e8443b5417b8edc4d1dd76455` (round-96 records base).
Report: `.ufo/reports/round-97/tameshi.md` (fleet repo), committed by lane identity:
`git log --format='%an %H' -- .ufo/reports/round-97/tameshi.md` → `tameshi-shokunin eeb065675e11c8c990bb738975a8e1475b7e7426`
at 12:12:00 -03, after the lane tip commit at 12:11:32 -03 (report lands last).
Prompt: `.ufo/prompts/tameshi-round-97.md` (996 lines): lines 1–140 diff `templates/round-prompt.md`
with substitutions only (`diff` shows only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` expansions);
addendum §6 (hyaku) plus §7 scratch and §8 pre-file ledger follow. Template prompt committed at
`7684e789` by `tameshi-shokunin` at 10:54:20 -03, before the 10:55:07 launch.

Dispatch digest (`.ufo/watchdog.log`, mutable log, copied verbatim):
- `2026-11-08T10:55:07-03:00 launch tameshi round=97 pgid=1189392 driver=hyaku-inline attempt=1`
- `2026-11-08T12:12:46-03:00 complete tameshi round=97; hyaku-inline attempt=1`

## Conformance (step-1)

- Report committed in the fleet repo by the lane identity: **PASS** (author `tameshi-shokunin <tameshi@shokunin.local>`, `eeb06567`).
- `SHONEN` heading present with one line per box: **PASS** (4 lines, all `[~]`, matching the four `SHONEN.md` boxes; no `[x]`).
- Cited lane commits exist and are ancestors of `master`: **PASS**. Every 40/7-hex token in the report
  (33 tokens) was resolved with `git cat-file -t` and tested with
  `git merge-base --is-ancestor <hash> 29734beb095984038d66bb5dd4d149d81378de31`; every commit token is an
  ancestor (07e50d6d, 8ed9c526, 917d7109, 997ce0c4, e72a0c8b, 136e98a8, 43acfe81, f5ace66a, 605c9c58,
  6f080522, 406119cd, 35db02e9, 2170db76, 2a57b42f, 21eca3c1, ef427ff0, 4460bba, 1074ab52, 8152e924, 29734beb).
  The non-object tokens are sha256 digests (88bcca86… driver, 02a5482a… checker, 9de0b7e9… manifest,
  4b5a8374… s159, 55bb7196… s006, 00082805… equiv, 54c6f667…/254536aa… landing bytes).
- Lane repo clean and pushed: **PASS** (see lane HEAD line above).
- Prompt carries the template contract: **PASS**. The five child-lane items are present: report path and
  filename (`:101`), commit-before-report ordering and pushed-hash citation (`:516`; "The report lands last
  and cites the pushed lane hash"), `SHONEN` heading check (`:521-522`), commit-hash citation (`:106-107`),
  and lane write scope (`:448`). Any L2 route map quoted (§6 amendments) is the orchestrator/operator host
  route table; `MISSION.md` §L2 makes its role-class buckets advisory to that table, so no bucket mismatch.
- Marker test: **not a marker** — the report cites 21 lane commits, measurements and the 12-seat wave record.
- Verdict: **status ok**. All defects below are conformance defects and status-neutral.

Conformance defects (status-neutral):
- **D-1 anchor cells edited in place.** `corpus/SOURCES.md` S159 and S006 `anchor` cells gained the
  round-97 re-open text in place (`git diff --numstat 0b19af5f..29734beb -- corpus/SOURCES.md` →
  `2\t2\tcorpus/SOURCES.md`: two rows replaced, each gaining the re-open text in its `anchor` cell). `CORPUS.md` §SOURCES rule 2 allows only `status`, `recheck`, `used-by` to change in
  place, and requires each change logged old→new in the round lesson; the lesson's Registry changes logs
  only the `used-by` change, and the report's "Rows touched old → new" names only `used-by`.
- **D-2 C2 no-work control cannot fail its own premise.** `controls97.py` registers
  `add("c2-nowork-absent", 0, "git grep GUARD_INERTIA at base %s: rc=%d out=%r" % (...), 0)` — the recorded
  code is the literal `0`, not `g.returncode`; the inner `git grep` rc (1) only appears in the receipt text.
  A14 fixed the two C1 no-work controls this way but not the C2 one. The report's C2 before clause is
  independently true (this closure's `git grep` rc 1), but the control is not an assertion.
- **D-3 stale pre-A15 receipts kept.** `.ufo/evidence/round-97/pre-freeze/c1-forge-conjunct.out` is an
  unregistered 19th receipt (the final controls set is 18 states) printing the pre-A15 shadowed
  `MISMATCH(counter-sha)`; `w1/SC1-quote-backability.txt` and `w1/SC1-receipt-catalog.txt` claim "at the
  lane's committed HEAD" yet quote pre-A15 bytes (exit/payload receipts as `MISMATCH(counter-sha)`, all
  three forge receipts at sha256 `1c9754f3…`); the receipts themselves are correct at tip.
- **D-4 capability rows not in the `## Capabilities` table.** SCORECARD's round-97 section names
  `committed-battery binder` and `guard-inertia matrix`; the `## Capabilities` table still ends at the
  round-81 rows. `AXES.md` §Capabilities puts rows in that table.
- **D-5 report record errors.** The report's Work-performed bullet says S159's quote is "14 words" and
  "snapshot `00082805…`-class bytes under `s159.html`": the renderer measures **15** words (lesson says 15),
  and `00082805…` is `equiv.html`'s digest — `s159.html` is `4b5a8374…`. It also gives S006 as "lines
  490-491" where the lesson says 490-492 (the renderer span of the quote is 490-491; 490-492 is the
  paragraph). The aggregate `CONTROLS97 states=18 matched=18 mismatched=0` line is quoted in the report and
  lesson but is stdout-only (the 18 per-control receipts are committed; the summary is not).
- **D-6 C2 wording exceeds exercised evidence.** The claims.json C2 wording includes
  `GUARD_SETUP state-unbuildable` and `GUARD_SETUP limit-mechanism-missing`; both branches exist in
  `guard-inertia.py` (`:228`, `:214`) and are recorded by A11, but no committed receipt or selftest case
  executes either one. The other four refusal classes are receipted (`edit-no-op`, `edit-ambiguous`,
  `manifest-sha-mismatch`, `manifest-empty`).
- **D-7 stale-lane line not graded.** The mission ran 77 m 39 s (> two 450 s driver ticks); the report's
  "Stale-lane" line says only that it is the lane's only open mission. Progress is evident (21 lane commits
  after the launch), but the report does not use the protocol's `progressing` / `silent` words.

## Per-claim re-check

Both claims rest on lane-owned instruments with selftests; per PROTOCOL §Gate standard (Closure
consequence) the instruments were **not executed** by this closure. Their committed evidence was verified
(self-test tally, frozen-run verdict, revision measured) and the plain measurements below were re-run.

### R97-C1 (calibration) — evidence-verified + counts re-measured. Verdict: **improved**

Commands run by this closure (committed bytes; lane is the cwd):
```
git grep -c 'BATTERY states=' 07e50d6d0142b21e8443b5417b8edc4d1dd76455 -- .   # (no output) rc 1
git grep -c 'BATTERY states=' 0b19af5f8666f9c54a437f511e9155a66d0d418d -- .   # (no output) rc 1
git cat-file -e 07e50d6d:.ufo/evidence/round-97/c1/battery-bind.py           # fatal: not in rev; rc 128
git ls-tree -r --name-only 2a57b42f .ufo/evidence/round-96/pre-freeze/controls/ | wc -l   # 50
git cat-file blob 2a57b42f:.ufo/evidence/round-97/c1/battery-bind.py | sha256sum  # 36b3103a445c… (claims 36b3103a…)
git cat-file blob 2a57b42f:.ufo/evidence/round-96/c1/controls-v96.py | sha256sum  # 88bcca8651f6… (claims 88bcca86…)
git cat-file blob 2a57b42f:.ufo/evidence/round-96/c1/measure-v96.py | sha256sum   # 69ee68b6fa23… (claims 69ee68b6…)
sha256sum .ufo/evidence/round-97/landing/*.out .ufo/evidence/round-97/repeat/*
```
Observed: the three `landing/c1-positive-*.out` and the three `repeat/c1-run-*.txt` are byte-identical,
sha256 `54c6f667886e71d450e6988f270195fad18be6927bd4a71cec96d2ef30f0b9a2`; each reads
`BATTERY states=50 matched=50 mismatched=0 missing=0`. The oracle's own union is 50:
`states()` holds 41 unique names (the source list prints `sharp-delim-5-4` twice) + `EXPECT_EXTRA`
9 keys (`nowork-base`, `selfpin-edit`, `double-pin`, `replace-honest`, `D01`–`D05`) = 50; the receipt
directory has exactly 50 `.out` files at `2a57b42f`, and the reader enumerates `sorted(expectations)`
and reads each receipt with `git cat-file blob <rev>:<path>` (`battery-bind.py:137-148`).

Receipts re-read at `2a57b42f`: `pre-freeze/c1-positive.out` → predicate + `rc=0`;
`pre-freeze/c1-selftest.out` → `BATTERY_SELFTEST: 7/7 pass` + `rc=0`; `c1-forge-worktree-only.out`
→ `BATTERY_ROW pos-real:MISSING(receipt-absent-at-rev)` + `matched=49 mismatched=0 missing=1`, rc 1;
`c1-forge-counter-sha.out` → `MISMATCH(counter-sha)` + `mismatched=1`, rc 1;
`c1-forge-exit.out` → `MISMATCH(exit=7)`, rc 1; `c1-forge-payload.out` → `MISMATCH(exit=0)`, rc 1;
`c1-forge-driver-sha.out` → `BATTERY_SETUP driver-sha-mismatch`, rc 2; `c1-forge-driver-sha-{empty,short}.out`
→ `BATTERY_SETUP driver-sha-invalid`, rc 2. `git cat-file -e 8ed9c526:…/C1-summary.txt` → rc 128 (the
before clause's absent summary). The after run's exit code is the `rc=0` in the committed pre-freeze
positive at the same records revision (the `landing/*.out` files carry stdout only).

Evidence-verified: instrument sha256 matches the claims pin; driver/counter pins match; 50 oracle
states = 50 committed receipts; landing 3/3 byte-identical; base absence and summary absence re-measured.
Not executed: the reader itself.

### R97-C2 (operability) — evidence-verified + manifest/edits re-measured. Verdict: **improved**

Commands run by this closure:
```
git grep -c 'GUARD_INERTIA' 07e50d6d0142b21e8443b5417b8edc4d1dd76455 -- .   # (no output) rc 1
git grep -c 'GUARD_INERTIA' 0b19af5f8666f9c54a437f511e9155a66d0d418d -- .   # (no output) rc 1
git cat-file -e 07e50d6d:.ufo/evidence/round-97/c2/guard-inertia.py          # rc 128
git cat-file blob 2a57b42f:.ufo/evidence/round-97/c2/guard-inertia.py | sha256sum    # 634997d0… (claims 634997d0…)
git cat-file blob 2a57b42f:.ufo/evidence/round-97/c2/guard-inertia.json | sha256sum  # 9de0b7e9… (claims 9de0b7e9…)
git cat-file blob 2a57b42f:.ufo/evidence/round-96/conjunct-disposition-v96.py | sha256sum  # 02a5482a… (claims 02a5482a…)
sha256sum .ufo/evidence/round-97/landing/*.out
```
Observed: the three `landing/c2-positive-*.out` and the three `repeat/c2-run-*.txt` are byte-identical,
sha256 `254536aa0cd7d9389bf8625d6d478ff211b8938d827a02c6abfa4bfa1d52853b`; each ends
`GUARD_INERTIA rows=10 killed=8 limits=2 survived=0 unmet=0` and `pre-freeze/c2-positive.out` carries
`rc=0` at `2a57b42f`. Manifest re-measured: 10 rows, `expect` histogram 8 `killed` / 2 `limit`; every
row's `edit.old` occurs **exactly once** in the checker blob at `2a57b42f` and differs from `edit.new`;
both `limit` rows carry a ≥40-character `limit_mechanism`. The five per-row `GUARD_ROW` lines show the
eight killed rows' pristine exit/token against mutant exit 0, and `verify-quiet` / `git-absolute` as
identical pairs (`limit`). `c2-selftest.out` → `GUARD_INERTIA_SELFTEST: 7/7 pass` + `rc=0`;
`c2-forge-flipped-expect.out` → `killed=8 limits=1 survived=1 unmet=1`, rc 1;
`c2-forge-noop.out` → `GUARD_SETUP edit-no-op:rev-hex`, rc 2; `c2-forge-manifest-subst.out` →
`GUARD_SETUP manifest-sha-mismatch`, rc 2; `c2-forge-manifest-empty.out` → `GUARD_SETUP manifest-empty`, rc 2.
Before clause re-measured: `GUARD_INERTIA` absent at `07e50d6d` and `0b19af5f`; round-96 `R96M1` is a
matrix over `measure-v96.py` (counter, not the checker); `w1/R96L1.md` exists with "partly refuted" and no
committed runnable matrix. `edit-ambiguous` is receipted by the wave (`w1/R97R2-receipts/atk5-ambig-real-checker.out`
→ `GUARD_SETUP edit-ambiguous:amb:22`, rc 2). `state-unbuildable` and `limit-mechanism-missing` are code-only (D-6).

## Prefile falsification ledger (step-2b)

Command run by this closure:
```
python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tameshi --round 97
```
Observed: `PREFILE-FALSIFICATION: pass claims=2 rows=18 attack_seats=7 findings=0`, exit 0.
Ledger read (`.ufo/waves/round-97/claim-falsification.tsv`): 18 rows, C1 10 / C2 8; all seven
attack-role seats appear (R97R1, R97R2, R97C1, R97M1, R97SN1, R97CN1, R97L1); every
`falsifies-wording` row names `plans/round-97.plan.md` and its note names the amendment.
Adjudication: no failing row is unreconciled — C1 rows → A3 (mutant digest exemption), A4 (pin-invalid),
A5 (`__pass` scope), A6 (rc 128), A7 (committed vs index deletion), A8 (plan sync), A14/A15 (control rc /
fixture), A3/A14 (critic §1/§2); C2 rows → A9 (Before clause), A12/A13 (manifest pin/declaration).
Every `falsifies-wording` narrowing is real and present in the frozen wording;
`R97S1`/`R97SC1` are `falsifies-number` with A15/SC1 repairs (D-3 records the residual stale fragments).

## Discernment spot-check

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ exit 0 (`tameshi ok`) with the standing W01/W04 advisories only. Registry counts (frozen census commands):
rows 183, malformed 0, A=165 B=14 C=4, mined=149 queued=23 rejected=11, duplicate ids none — matches the
report and both `census-before.txt` / `census-after.txt`.

No **new** row was written this round (rows 183 → 183; the only candidate, S324, was withdrawn as a
duplicate of S160 before the freeze). The sample therefore checks the two **re-opened** rows and the two
refusals; both admits and both rejects were re-opened.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S159 (Wikipedia, Mutation testing) | admit / re-open (mined; `used-by` gains round-97 lesson) | live `https://en.wikipedia.org/wiki/Mutation_testing` (curl, 2026-11-08) + committed `.ufo/evidence/round-97/sources/s159.html` (171636 B, sha256 `4b5a8374…`), rendered by the canonical lane renderer `R93S1-tagstrip.py:strip_tags` | agree | the sentence "Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing." is present live; the renderer puts it at **line 762**, `len(quote.split())` = **15** (≤25); the snapshot digest matches the row. It grounds the C2 `limit` class (an edit with no observable change is measured, not presumed). |
| S006 (shmutant README) | admit / re-open (mined; `used-by` gains round-97 lesson) | live `https://github.com/BWBama85/shmutant` + raw `README.md` (lines 91-92) + committed `sources/s006.html` (281627 B, sha256 `55bb7196…`), same renderer | agree | "A row whose old literal occurs more than once in its target there is refused" is present in the live README and in the snapshot; renderer span **490-491**, 15 words; grounds the `edit-ambiguous` refusal. |
| S324 (draft Stryker "Equivalent mutants" row) | reject / withdrawn before freeze | `corpus/SOURCES.md` S160 row (the same URL) + committed `census-before.txt` `W04 S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants`; no S324 row exists | agree | S160 already holds the document; a second row for one URL is exactly the CORPUS rule-2 duplicate class the census flags; withdrawing keeps one row and the re-open was grounded on S159 instead. |
| S009 (UCL Discovery, Trivial Compiler Equivalence) | reject / not opened; no verdict from an unread page | committed `sources/headers-s009.txt` (HTTP 403, `cf-mitigated: challenge`, 5474 B) and `sources/s009.html` (sha256 `106e61ab…`) + live `https://discovery.ucl.ac.uk/id/eprint/1499169/` | agree on the round's decision; note flip now open | the round correctly refused a verdict from a challenge page. However, this closure's live fetch returned **HTTP 200, 42254 B** with the title and abstract ("Identifying equivalent mutants remains the largest impediment … We propose Trivial Compiler Equivalence (TCE) …"), so the row's stated flip condition (a fetchable author/repository copy with a located quote) is now met: re-open S009 next round. |

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1: 50 committed receipts re-graded by the committed driver oracle with pinned digests; base absence (`git grep` rc 1, `cat-file -e` 128) re-measured; five refusal classes receipted; `7/7` selftest. Scalar stays 8 (monitor ceiling; the last 2 points need independent promotion review). |
| operability | improved | C2: 10 pre-registered exact edits, 8 killed / 2 measured limits, digest-pinned checker and manifest, four receipted refusal classes + selftest `7/7`; D-6 records the two code-only branches. |
| depth | unchanged | scores 10; no depth claim; the round adds no recorded mutation case. |
| freshness | unchanged | no successor freshness sweep; the counter side is re-verified at `2a57b42f` but the row population is unchanged. |
| coverage | unchanged | no new domain surface; `corpus/knowledge/` unchanged (`git diff --stat` empty), SOURCES 183 → 183, frontier F1–F11 unchanged. |
| adjacency | unchanged | connector (R97CN1) found no duplicate implementation; no sibling file written. |

No axis harmed: `git diff 0b19af5f..29734beb -- SCORECARD.md` is a single 41-line append with no score
deletion; `LOG.md` +39/-0; `corpus/QUALITY.md` +23/-0; `corpus/knowledge/` unchanged; `SKILL.md`,
`PROVINCE.md`, `SHONEN.md`, `corpus/README.md` unchanged. The only non-append edit in the corpus is the
SOURCES anchor cells (D-1), a form defect, not an entry failing its bar.

Admitted: **true** — both claims verified (evidence-verified, with the plain counts re-measured above),
no axis harmed; the defects above are status-neutral and routed.

## Trend verdicts (must agree with the MANIFEST entry)

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | no new admitted `knowledge/` entry; SOURCES 183 → 183 (A165/B14/C4; mined 149/queued 23/rejected 11); frontier unchanged; one duplicate candidate withdrawn (S324). |
| quality | improved | QUALITY 175–176 appended, each with an `Able to fail:` receipt (the five C1 forgeries; the two measured C2 `limit` rows and the two C2 refusals); two instruments replace an uncommitted summary (D-a of r96) and an absent probe (D-b); S159/S006 re-verified with pinned snapshots. |
| discernment | improved | the round's own wave falsified twelve atomic assertions pre-data — R97R1 F1–F6, R97E3 FW-C1-1, R97C1 §1/§2, R97L1 §9, R97R2 F1 — and every one became A3–A14 with its artifact cited; the prefile ledger passes; this closure's admit/reject sample agrees on all four gate decisions (S159, S006, S324, S009). |

## Routed defects (lane must fix next round)

1. **D-1** SOURCES contract v1 rule 2: revert the in-place `anchor` additions on S159/S006, or log the
   anchor old → new in the next round lesson and move the re-open provenance into a superseding row/entry.
2. **D-2** `controls97.py` `c2-nowork-absent`: record and grade the inner `git grep` rc (1) as the C1 pair
   does; currently the wrapper's hardcoded 0 cannot fail. Also reconcile the report/SCORECARD's "rc 1" wording
   with the receipt's outer `rc=0`.
3. **D-3** remove or mark superseded the stale pre-A15 fragments: `pre-freeze/c1-forge-conjunct.out`,
   `w1/SC1-quote-backability.txt`, `w1/SC1-receipt-catalog.txt` (they quote the pre-A15 forge bytes; the
   receipts at tip are correct).
4. **D-4** enter `committed-battery binder` and `guard-inertia matrix` in the SCORECARD `## Capabilities`
   table (name · what it can now do · evidence pointer · first-working round), per AXES §Capabilities.
5. **D-5** next-round erratum for the report's S159 "14 words"/`00082805…` mislabel (15 words; `4b5a8374…`)
   and the S006 490-491/490-492 span; commit the `CONTROLS97 states=18 matched=18` summary receipt instead
   of citing stdout.
6. **D-6** add executed receipts or selftest cases for `GUARD_SETUP state-unbuildable` and
   `GUARD_SETUP limit-mechanism-missing` (or narrow the wording); code + A11 is the only support today.
7. **D-7** grade the 77 m 39 s mission as `progressing` (21 lane commits after launch) in the stale-lane line.
