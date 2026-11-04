# tameshi round 74 — verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-03 against lane tip `ef57dc2ae0511ecbc608ec66719421ebe0ad5f4a`
(branch `master` == `origin/master`), base `3d6ea1ee8e551e3baf94904384890e3a112088f0`
(the admitted round-73 non-author closure). Every reading below was taken by
this verifier from committed bytes with plain git/awk/python counts; the lane's
own gates were read as committed receipts and were **not executed**. Verdict:
**admitted** — both claims verify, no axis is harmed; one undisclosed EOL
rewrite and five record defects are routed.

## 1. Step-1 conformance

| Check | Result | Evidence (this verifier's own run) |
|---|---|---|
| Report committed in the fleet repo by the lane identity | PASS | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-74/tameshi.md` → `tameshi-shokunin <tameshi@shokunin.local> 4dbb30f586392b91b88a129303e2c6ceb6942cd7`; the commit touches that path only |
| Report lands after the lane work | PASS | lane tip `ef57dc2a` committed 22:59:58 -03; report commit `4dbb30f5` committer date 23:00:57 -03 (file mtime 23:00:34), i.e. after the tip; complete line 23:01:44 -03 |
| `SHONEN` heading, one line per box | PASS | `grep -c '^## SHONEN'` → 1, followed by four `[~]` lines; `SHONEN.md` carries four boxes (all `[~]`), so the count matches |
| Every cited lane commit exists and is an ancestor of the branch | PASS | 19 round commits plus the base, each `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> refs/heads/master` (detached-HEAD tolerant — every one ANCESTOR: `a7cd78ae 2bbf9796 2e0ac486 9fe58b40 607b96d8 141dead0 9d9ab7d3 ee395675 1c3a428e eb677017 47cd112f 906303c7 e84728d6 5f2f88aa 9c27267b e3fb9358 f5e9f9e2 2eb49f9a ef57dc2a`) |
| Round range matches the report | PASS | `git rev-list --count 3d6ea1ee..ef57dc2a` → `19`; the landed-changes table carries all 19 (the round-73 defect of a 22-of-23 table is not repeated) |
| Lane repo clean, nothing uncommitted, pushed | PASS | `jj-lane.sh state` → `branch=master local=ef57dc2a… remote=ef57dc2a… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints nothing; `git ls-remote origin refs/heads/master` → `ef57dc2ae0511ecbc608ec66719421ebe0ad5f4a` |
| Frozen plan declared before any claim data | PASS | first round commit `a7cd78ae` adds `plans/round-74.plan.md` + LOG declaration + the pre-data receipts; the plan blob is identical at `a7cd78ae` and `ef57dc2a` (`de1aad62e977…`) |
| Prompt carries the template contract | PASS | `templates/round-prompt.md` is 140 lines; `diff` of the prompt's first 140 lines against it yields 11 changed lines per side, every one a `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitution; the run-15 §6 hyaku addendum and the §7 scratch discipline follow. `MISSION.md` §L2 is ≥8 subagents in one batched call and the prompt states exactly that |
| Real report, not a marker | PASS | work performed, per-claim before→after counters, 19-commit landed table tied to `LOG.md` entries, evidence pointers that resolve, trend verdicts, SHONEN |
| Report accuracy — round shape | PASS | `.ufo/waves/round-74/w1-results.json` has 12 records and `w1/*.md` 12 top-level seat reports; role multiset `executor=4 reviewer=2 scribe=1 scout=1 critic=1 mutation-tester=1 connector=1 sentinel=1`; attack seats `reviewer 2 + critic 1 + mutation-tester 1 = 4/12 = 33.3 %`; `w1-dispatch.json` `counts={spawn:12,resume:0,total:12}`, 12 tasks in one call, no `model` key, each task leading with `/skill:godspeed` |
| Defect — SCORECARD EOL rewrite, undisclosed | **DEFECT (status-neutral, routed)** | `SCORECARD.md` was CRLF at base (4406 CR in 4490 lines) and is LF at the tip (0 CR in 4606 lines); the conversion happened at `1c3a428e` and is absent from the report, `LOG.md` and the lesson. Content is additive (`git diff --numstat --ignore-cr-at-eol` → `116 0`) |
| Defect — cold-read pointer names the wrong revision | **DEFECT (status-neutral, routed)** | the report and SHONEN box 3 say `credited=64/64` "at `ef57dc2a`" / "at the tip"; `live-green4-r74.out` reads `rev=f5e9f9e2`, and commit `2eb49f9a`'s message says the same |
| Defect — live SCORECARD counters stale | **DEFECT (status-neutral, routed)** | the live capability rows still quote `WAVE_RECONCILE_SELFTEST: 12/12 pass` (SCORECARD.md:262) and `ADDRANGE: rows=6 met=6 unexpected=0` (SCORECARD.md:264) while the tip tool prints 15/15 and the tip receipt `.ufo/evidence/round-74/addr-r74.txt` reads `rows=11`; the round-73 historical rows (:4439, :4485, :4506) are records and correctly stay |
| Defect — registry home partially paid | **DEFECT (status-neutral, routed)** | `tools/registry.json` gains four rows (wave-reconcile-selftest, wave-reconcile-mutants, additivity-range-selftest, additivity-range-sweep; `REGISTRY_CHECK held=1/1` ×4 in `final-tip-r74.txt`), but `SKILL.md`'s registry table still lists neither instrument (`grep -n 'wave-reconcile\|additivity-range' SKILL.md` → no match; SKILL.md blob identical base→tip) and the JSON rows carry no verdict map, pinned-value path, write scope or owner |
| Defect — S294 old→new not in the lesson | **DEFECT (status-neutral, routed)** | the report says the `used-by` change is "logged in the lesson's Gate"; the lesson records only the added path. The old→new pair appears in the report and the SOURCES `Round 74` note |
| Defect — round-73 routed items 3–4 still open | **DEFECT (status-neutral, routed)** | no erratum was appended to `plans/round-73.plan.md` for its contradicted kill-rule sentence, and the round-73 report's 22-of-23 landed table / 19-vs-18 W04 census count are still uncorrected in a later report |

Nothing above changes the lane status; the defects are record-discipline items
and none touches the two declared claims.

## 2. Per-claim re-check

Two claims, distinct axes, frozen in `plans/round-74.plan.md` at `a7cd78ae`
(before any claim data). Neither is exploratory.

### R74-C1 — operability (verdict-only): the three named arm gaps become measured arms

**Before (re-measured static).**

```
git show 3d6ea1ee:tools/wave-reconcile.py | grep -oE 'arm[0-9]+' | sort -u
  -> arm1 arm2 arm3 arm4 arm5 arm6 arm7 arm8 arm9 arm10 arm11 arm12
git show 3d6ea1ee:tools/wave-reconcile.py | grep -cE '^\s+arm\('   -> 12
```

Committed base receipt `.ufo/evidence/round-74/base-measure-r74.txt` (at
`a7cd78ae`) → `WAVE_RECONCILE_SELFTEST: 12/12 pass`, exit 0. Seats T74W1E1 and
T74W1E3 re-built the three frozen mutants and measured all three surviving
12/12 (`T74W1E3.md` §1: `MUTATE: DONE (… defects=3 killed=0 survived=3 …)`).

**After (re-measured static + evidence-verified tallies).**

```
git show ef57dc2a:tools/wave-reconcile.py | grep -oE 'arm1[3-5][^ ]*' | sort -u
  -> arm13-printed-undelimited-refused arm14-span-not-in-record-refused
     arm15-seatreports-top-level-only
git show ef57dc2a:tools/wave-reconcile.py | grep -cE '^\s+(arm|arm_raises)\('  -> 15
git show ef57dc2a:tools/wave-reconcile.py | sha256sum
  -> 97bb9272afb6c243cf7fb2dfde7bd34b90b4bcd769974d112ca574fccafd21fa
git show ef57dc2a:tools/wave-reconcile-mutants.spec | grep -c '^@defect' -> 3
```

The committed battery receipt `battery-r74.txt` names that same target sha256
at `ee395675`/the tip and the earlier `9532c12b…` at `2bbf9796`; both show
`CONTROL: GREEN`, each defect `KILLED` with the FAIL line on its **named** arm
only (`arm13`, `arm14`, `arm15`), the suite at `14/15` under each mutation,
`MUTATE_RESTORE: OK` byte-identical, and
`MUTATE: DONE (… defects=3 killed=3 survived=0 inconclusive=0 kill-rate=100%)`.
`final-tip-r74.txt` carries `WAVE_RECONCILE_SELFTEST: 15/15 pass` and the same
battery line.

*Re-measured by this verifier:* the arm inventory, the 12→15 assertion count,
the tool hash at `2bbf9796`/tip, the spec's defect count, and the receipt's
internal consistency. *Evidence-verified (not executed):* the selftest tally
and the mutant battery. The seat T74W1R1 hardening (`arm_raises` asserting the
named refusal) is visible in the committed source at :415-497 and does not
change the arm count.

### R74-C2 — calibration (the lowest scored numeric axis at 8): a declared-range additivity sweep

**Before (re-measured static).**

```
git show 3d6ea1ee:tools/additivity-receipt.py | grep -c rev-list   -> 0
```

The committed base receipt shows the per-pair tool exiting **0** on the
round-73 `LOG.md` rewrite pair (`raw_old_only=3484 raw_new_only=3523
norm_cr_old_only=0 … eol_rewrite_disclosed=true`) and 1 on the QUALITY pair
with no claim class declared — a clean-looking receipt for a real rewrite.

**After (re-derived independently by this verifier, own code over committed
git blobs; the lane's tool was not executed).**

| Row | kind | file | walked | changed | worst commit | raw_old_only | norm_cr_old_only |
|---|---|---|---|---|---|---|---|
| r73-log-declaration-append | commits | LOG.md | 1 | 1 | 17cd19396b36 | 0 | 0 |
| r73-log-post-wave-append | commits | LOG.md | 1 | 1 | e309f59f4007 | 0 | 0 |
| r73-log-eol-rewrite | commits | LOG.md | 1 | 1 | 862e88444817 | 3484 | 0 |
| r73-quality-append | commits | corpus/QUALITY.md | 1 | 1 | be1199d3874d | 0 | 0 |
| r73-quality-criterion-pin | commits | corpus/QUALITY.md | 1 | 1 | 21a7332f4d53 | 1593 | 5 |
| r73-log-range-total | pair | LOG.md | 1 | 1 | 3d6ea1ee8e55 | 3484 | 0 |
| r73-sources-damage-commit | commits | corpus/SOURCES.md | 1 | 1 | be1199d3874d | 1 | 1 |
| r73-sources-row-repair | commits | corpus/SOURCES.md | 1 | 1 | 1d118c14cce6 | 1 | 1 |
| r73-log-closeout-append | commits | LOG.md | 1 | 1 | bbb7b18907db | 0 | 0 |
| r73-log-range-walk | commits | LOG.md | 24 | 4 | 862e88444817 | 3484 | 0 |
| r73-quality-range-walk | commits | corpus/QUALITY.md | 21 | 1 | 21a7332f4d53 | 1593 | 5 |

Union over the `kind: commits` rows keyed `(file, worst commit)` → **keys 8,
raw_old_only 5079, norm_cr_old_only 7** — identical to the published
`ADDRANGE: rows=11 met=11 unexpected=0` /
`ADDRANGE_TOTALS kind=commits-union keys=8 raw_old_only=5079
norm_cr_old_only=7`.

The frozen six-row predicate was re-run at its own commit: the six
`ADDRANGE_ROW` lines and the summary in `.ufo/evidence/round-74/
frozen-six-row-r74.txt` are **byte-identical** to the receipt committed at
`2e0ac486` (`diff` of the row/summary lines → no output). The selftest
`ADDITIVITY_RANGE_SELFTEST: 8/8 pass` and the controls (class control
`rows=11 met=7 unexpected=4`; range flip `unexpected=1` exit 1; echo stub;
do-nothing exit 0; pair-vs-walk naming the tip) are in the committed receipts
and are evidence-verified, not executed here.

The two round-73 closure defects are re-derived from committed bytes:
`LOG.md` at `862e8844` → raw 3484 / normalized 0 (numstat `3801 3759`;
`--ignore-cr-at-eol` → `42 0`); `corpus/QUALITY.md` at `21a7332f` → raw 1593 /
normalized 5 (numstat `1925 1920`; ignore-cr `10 5`). The set-difference vs
line-counting gap is disclosed in the lesson's "Number note (honesty)".

*Re-measured by this verifier:* every row and the totals, the frozen six-row
re-run identity, and the two rewrite counts (own predicate). *Evidence-verified
(not executed):* `ADDITIVITY_RANGE_SELFTEST: 8/8` and the controls receipt.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | unchanged | `SKILL.md` blob `95d1f935…` identical base→tip; no new decision-table case or error pattern; `SCORECARD.md` content diff `116 0` (`--ignore-cr-at-eol`) is appends only |
| coverage | unchanged | `corpus/README.md` blob `d0ffbfb8…` and `PROVINCE.md` `98296a40…` identical; no frontier row advanced (the report says so and the blobs agree) |
| operability | **improved** | `tools/wave-reconcile.py` gains arms 13/14/15 (12 → 15 assertions); the committed battery kills all three named mutants on their named arms with a byte-identical restore; tool sha256 `97bb9272…` equals the receipt target |
| freshness | unchanged | census 163 → 164 rows; the S294 re-open refreshes quotes but leaves `recheck` and `verified-at` untouched; no stale item was flagged or fixed; the freshness counter's population is otherwise unchanged |
| calibration | **improved** | the range instrument's 11 rows and totals re-derive exactly; the round-73 closure's two routed EOL rewrites now stand as declared red rows at their own commits; criterion 124 records the rule with a falsifier; the frozen six-row predicate is re-run byte-identically at its commit |
| adjacency | unchanged | `PROVINCE.md` identical; no sibling write (T74W1CN1 read-only census); the KAMA sibling instrument is reported as a different frame and the pattern is **not** claimed general (one lane only), which matches the connector's own note |

**No axis is harmed.** Content is preserved on every file the round touched:
`LOG.md` `76 0` raw, `corpus/QUALITY.md` `24 0` raw, `corpus/SOURCES.md` `4 1`
(the documented S294 `used-by` in-place edit), `tools/registry.json` additive
rows, and `SCORECARD.md` `116 0` ignoring CR. The SCORECARD line-ending
conversion is a record-discipline defect (routed, §6), not a content loss: the
cold-read monitor reads `credited=64/64` at `f5e9f9e2` after four rekey
batches (receipt `live-green4-r74.out`), and `probe_mismatches=0`.

## 4. Discernment spot-check (`corpus/lessons/round-74.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S304 (git-diff `--ignore-cr-at-eol`) | admit | live `https://git-scm.com/docs/git-diff` (fetched by this verifier) and the committed extract `.ufo/evidence/round-74/sources/s304-git-diff.html` (sha256 `05206b6fbf4c…`, 229,283 B, identical to the live page) | **agree** | the quote "Ignore carriage-return at the end of line when doing a comparison." occurs once at page line **4157**, 11 words (≤25); the row is tier A docs, `status: mined`, `used-by corpus/lessons/round-74.md` resolves |
| S294 (gitattributes) re-open, three quotes | admit | live `https://git-scm.com/docs/gitattributes` and the committed extract (sha256 `ceb3351f931a…`, 131,174 B, identical to the live page) | **agree (one line-number correction)** | all three quotes occur verbatim after line-joining: Quote 1 at 2667–2668 (13 words), Quote 3 at 2758–2759 (20 words); Quote 2 ("Line endings are normalized to LF in the index") opens on **2679** and runs into **2680**, which is exactly the lesson's appended correction (the Gate block's `2678–2679` was off by one and is superseded append-only) |
| A new gitattributes row for the round-74 ground | reject (standing, re-sampled) | the same live page and the S294 row cells (`scope`: git's declared line-ending conversion layer; `source` same URL) | **agree** | same URL, same document, same scope → within-scope duplicate; the S289/S293 precedent and CORPUS rule 2 make the re-open the contract-shaped act; the flip condition (row retired or page superseded) is named and honest |
| ≤25-word quote on the newly written SOURCES row | check | S304 row cells in `corpus/SOURCES.md` | **agree** | 11 words, located at page line 4157, and the quote grounds the declared-class purpose |
| Census validate | gate | this verifier's own run of `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | **agree** | exit 0, `tameshi ok`, rows 163 (base) → 164 (tip), malformed rows 0, duplicate ids none, warnings only (`18` W04 + `1` W01 S101) — the report's prose matches the run |

## 5. Trend verdicts

- **expansion — improved.** A capability entered `SCORECARD.md`
  `## Capabilities` (`round-range additivity sweep`, first working round 74)
  through a demonstrated run — 11 declared rows, eight selftest arms, five
  controls and a frozen re-run — and the registry grew by one tier-A row
  (S304) with a second row re-opened (S294). No new `knowledge/` entry and no
  frontier move; the report states both, and the blobs agree
  (`corpus/README.md` identical).
- **quality — improved.** Three unguarded rules became load-bearing arms with a
  committed mutant battery (`killed=3 survived=0`, each on its named arm); the
  instrument gained a range mode that no per-pair recipe reproduces, exercised
  by 24- and 21-commit walks; two wave-caught defects (row-sum totals,
  `walked=`) were fixed with the frozen counters unchanged; criterion 124
  records the rule. Caveats, routed not absorbed: the SCORECARD EOL rewrite,
  the two stale live capability counters, and the cold-read pointer's
  off-by-two revision. No admitted entry was found false; content is preserved
  and the monitor is green.
- **discernment — improved.** This verifier agrees with the new-row admit, the
  duplicate reject and the re-open's quotes; four seat attacks were adopted as
  work (named refusals, the unexercised range mode, the totals double-count,
  the echo-stub analysis), three of the round's own mistakes are mined in
  `## Mistakes`, the `M-C` survivor is named as a gap instead of argued away,
  and two frozen-text defects plus the echo-stub limitation are disclosed.
  The one line-number correction is append-only, not a rewrite.

## 6. Routed defects for the lane (status-neutral; next round)

1. **`SCORECARD.md` EOL rewrite, undisclosed.** `1c3a428e` converted the file
   CRLF→LF: base 4,406 CR / 4,490 lines → tip 0 CR / 4,606 lines; raw diff
   `4522 4406`, CR-blind `116 0` (content additive). Name it in a LOG erratum
   or restore the base bytes, and state whether the range manifest should
   declare `SCORECARD.md` (it is not append-only, so the fix is disclosure,
   not a claim change).
2. **Cold-read pointer names the wrong revision.** Report and SHONEN box 3 say
   `credited=64/64` at `ef57dc2a` / "at the tip"; `live-green4-r74.out` reads
   `rev=f5e9f9e2` (and `2eb49f9a`'s message says so). Commit a tip re-run or
   name `f5e9f9e2` in the report and the box.
3. **Live SCORECARD counters stale.** `SCORECARD.md:262` still quotes
   `WAVE_RECONCILE_SELFTEST: 12/12 pass` (tip prints 15/15) and `:264` quotes
   `rows=6` while its cited tip receipt reads `rows=11`; the :4439/:4485/:4506
   round-73 lines are historical records and stay. Supersede the two live rows
   or point them at the frozen receipt and commit.
4. **Gate registry home still missing the two instruments.** The four
   `tools/registry.json` rows exist (`held 4/4`), but `SKILL.md`'s registry
   table lists neither `tools/wave-reconcile.py` nor
   `tools/additivity-range.py`, and the JSON rows carry no verdict map,
   pinned-value path, write scope or owner. Add the SKILL.md rows with the
   PROTOCOL §Gate standard fields (this is the un-paid half of round-73
   routed defect 5).
5. **S294 `used-by` old→new not in the lesson.** The report says the change is
   "logged in the lesson's Gate"; the lesson records the added path only. The
   old→new string lives in the report and the SOURCES `Round 74` note; append
   it to the lesson (append-only) or fix the pointer.
6. **Round-73 routed items 3–4 remain open.** `plans/round-73.plan.md` still
   carries the contradicted "any control … reaches `unexpected=0`" sentence
   with no erratum, and the round-73 report's 22-of-23 landed table and
   "19 × W04" census sentence are still uncorrected in a later report.
7. **Carries the round already names (keep on the queue).** `M-C` (printed
   integer bound to the record rather than the span) survives all 15 arms; a
   selective `_record_claim` bypass on roles/attack_share alone survives; the
   echo stub can print the summary and typed totals (disclosed); the six older
   standing instruments still lack registry rows; rounds 61–71 carry no
   `results.json` and round 60's vocabulary is `agent='task'` (round-73
   carries, untouched).

## 7. Closure

Conformance: real report, lane identity `tameshi-shokunin`, `SHONEN` heading
with four `[~]` lines against four boxes, all 19 round commits ancestors of
`refs/heads/master`, lane clean and pushed (`ahead=0`), prompt a faithful
template rendering plus the run-15 addendum. Claim R74-C1 verifies — the
12→15 arm move and the named-arm kill battery are re-measured statically and
the tallies are evidence-verified. Claim R74-C2 verifies — all 11 rows and the
union totals re-derive exactly with this verifier's own code, the frozen
six-row re-run is byte-identical, and the two round-73 EOL rewrites stand as
measured rows. No axis is harmed; one EOL rewrite and five record defects are
routed. **Admitted.**

No promotion or mint: SHONEN boxes remain `[~]` lane assertions and promotion
stays operator-owned. The boxes are checkable by a non-author (the lane's
SKILL tables, LOG entries and evidence resolve), but this closure does not
write marks.
