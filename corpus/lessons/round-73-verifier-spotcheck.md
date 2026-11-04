# tameshi round 73 — verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-03 against lane tip `5c9a5559039e6ba90e006e768fa6a034fb03ba17`
(branch `master` == `origin/master`), base `a3dd35742eee608d1205843dacebc461b4242b9e`.
Every reading below was taken by this verifier from committed bytes with plain
git/awk/python counts; the lane's own gates were read as committed receipts and
were not executed. Verdict: **admitted** — both claims verify, no axis is
harmed, a report/record EOL-rewrite defect and four minor defects routed.

## 1. Step-1 conformance

| Check | Result | Evidence (this verifier's own run) |
|---|---|---|
| Report committed in the fleet repo by the lane identity | PASS | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-73/tameshi.md` → `tameshi-shokunin <tameshi@shokunin.local> 236a034a6e81377b85f5d2cc3fb48a11d0c72ab4` |
| Report lands after the lane work | PASS | lane tip `5c9a5559` committed 22:24:20 -03:00; report commit `236a034a` 22:24:57 -03:00 (37 s later); dispatch/complete lines 21:51:27 / 22:25:36 -03:00 |
| `SHONEN` heading, one line per box | PASS | `grep -c '^## SHONEN'` → 1, followed by four `[~]` lines; `SHONEN.md` carries four boxes (all `[~]`), so the count matches |
| Every cited lane commit exists and is an ancestor of the branch | PASS | 23 round commits plus the base: each resolved with `git rev-parse --verify <h>^{commit}` and tested with `git merge-base --is-ancestor <h> refs/heads/master` (detached-HEAD tolerant — every one `ANCESTOR`: `17cd1939 fddbb667 be1199d3 2e89e539 7982619f 4ebf7a1e 3e0ef1c8 1d118c14 caa5c4c5 7c5ffe04 8f7ff279 21a7332f 06ce20f7 8b6e1bbe 9ffaf039 862e8844 bbb7b189 de036cc9 314a68de 9afadc1a 1decfb23 e309f59f 5c9a5559`) |
| Round range matches the report | PASS | `git rev-list --count a3dd3574..5c9a5559` → `23`; the report's landed-changes table lists 22 of them (defect 3 below) |
| Lane repo clean, nothing uncommitted, pushed | PASS | `jj-lane.sh state` → `branch=master local=5c9a5559… remote=5c9a5559… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints nothing |
| Frozen plan declared before any claim data | PASS | first round commit `17cd1939` (22:00:03 -03:00) adds `plans/round-73.plan.md` + LOG declared entry; the plan blob is identical at `17cd1939` and `5c9a5559` (`098afe2e1329…`) — frozen, not rewritten |
| Prompt carries the template contract | PASS | `templates/round-prompt.md` is 140 lines; `diff` of the prompt's first 140 lines against it yields 22 changed lines in 10 hunks, every one a `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitution (the single changed line carrying no placeholder is the `{{AXES}}` line itself); the run-15 §6 hyaku addendum follows; the five child-lane items (SOURCES/frontier, lesson gate, SHONEN lines, before→after, trends) are present and the L2 item matches `MISSION.md` §L2 (≥8 subagents, one batched call) |
| Real report, not a marker | PASS | work performed, per-claim before→after counters, 22-row landed-changes table tied to `LOG.md` entries, evidence pointers that resolve, trend verdicts, SHONEN |
| Report accuracy — round shape | PASS | `.ufo/waves/round-73/w1-results.json` has 13 records and `w1/*.md` 13 top-level seat reports; role multiset `executor=3 scribe=2 reviewer=2 scout=1 critic=1 mutation-tester=1 sentinel=1 revenger=1 connector=1`; attack seats `reviewer 2 + critic 1 + mutation-tester 1 = 4/13 = 30.8 %`; `w1-dispatch.json` `counts.spawn=13`, policy band 8–16 |
| Defect — landed-changes table completeness | **DEFECT (minor, status-neutral)** | the table has 22 rows; the range has 23 commits. `e309f59f` (the `LOG.md` post-wave entry) is cited only as a *measurement revision* in the tip-receipts row, not as a landed change |
| Defect — census warning count in the report prose | **DEFECT (minor, status-neutral)** | the report's Sources section says "19 × W04, 1 × W01 S101"; the committed `census-start-r73.txt` and this verifier's live run both read `18` W04 + `1` W01, exit 0 |
| Defect — evidence standard, EOL rewrites | **DEFECT (status-neutral, routed)** | `corpus/QUALITY.md` and `LOG.md` were rewritten CRLF→LF this round (raw old-only 1,915 and 3,759); see §6 defects 1–2. Content is preserved (normalised old-only 0) and the monitor is green, so no claim is touched |
| Gate registry | **DEFECT (status-neutral, routed)** | `tools/wave-reconcile.py` has gate shape (verdict 0/1/2, `--selftest`, expected values in `tools/wave-reconcile.json`) but no registry row at the lane's registry home (`SKILL.md` names none of the standing instruments) or in `tools/registry.json`; PROTOCOL §Gate standard §Delivery binds (defect 5) |

Nothing above changes the lane status; none of the defects touches the two
declared claims.

## 2. Per-claim re-check

Two claims, distinct axes, frozen in `plans/round-73.plan.md` at `17cd1939`
(before any claim data). Neither is exploratory.

### R73-C1 — calibration (capability acquisition: wave-record reconciliation)

**Before (re-measured).**

```
git ls-tree -r a3dd3574 -- tools/ | grep -c wave-reconcile   -> 0
git grep -c WAVE_RECONCILE a3dd3574 -- tools/                -> no match, exit 1
```

**After (re-measured).** `git ls-tree -r 5c9a5559 -- tools/ | grep wave-reconcile`
→ `100755 blob 314e02da… tools/wave-reconcile.py` and
`100644 blob b4d0856f… tools/wave-reconcile.json`; the capability row is
present at `SCORECARD.md:262` (`wave-record reconciliation … round 73`).

**Independent re-derivation of all six rows (this verifier's own git/python
counts; the lane's tool was not executed).**

| Row | Record claim (fleet rev `3664a6d3` / lane rev `a3dd3574`) | Artifact re-derivation | Result |
|---|---|---|---|
| `r72-report-seats` | report span `12 seats, 11 reports`, printed seat count 12 | `w1-results.json` `.results` length = 12 | meet |
| `r72-report-seatreports` | same span, printed report count 11 | top-level `w1/*.md` = 12 (any-depth `.md` = 17) | drift (as declared) |
| `r72-plan-seats` | plan span `**one v1 wave, 12 seats**` | 12 records | meet |
| `r72-spec-roles` | `w1-spec.json` item roles | results agents: `connector 1 critic 1 executor 3 mutation-tester 1 revenger 1 reviewer 1 scout 1 scribe 2 sentinel 1` — identical multiset | meet |
| `r72-plan-roles` | plan `1 labrat`, no `revenger` | results have `revenger 1`, `labrat 0` | drift (as declared) |
| `r72-attack-share` | report span, printed 12, named `reviewer critic mutation-tester labrat` | `(1+1+1+0)/12 = 3/12 = 25.0 %` against floor 25 | meet |

The two red arms are the round-72 closure's routed defects 1–2 (the
`11 reports` sentence and the `labrat`/`revenger` freeze drift), both measured
as drift on every sweep, as the report claims. The r72 report blob at
`3664a6d3` carries `12 seats, 11 reports` exactly once; the r72 plan blob at
`a3dd3574` carries `1 labrat`.

**Evidence-verified (committed receipts, not executed by this verifier).**
`wave-selftest-r73.txt` → `WAVE_RECONCILE_SELFTEST: 12/12 pass` exit 0;
`wave-reconcile-live-r73.txt` → six `WAVE_ROW` lines and
`WAVE_RECONCILE: rows=6 met=6 unexpected=0` exit 0, with
`printed=11 files=12` and the `labrat`/`revenger` detail; `reh/reh-c1-controls.txt`
→ always-meet and echo-printed stubs `rows=6 met=4 unexpected=2` exit 1,
green-only stub `rows=4 met=4 unexpected=0` exit 0 (cannot print the frozen
six-row line); `hardening-r73.txt` → the S03 fixes shown able to fail
(`span-not-in-record` and `unknown-root` setup exit 2) with the frozen
counters unchanged.

**Verdict: `improved`** — a capability entered the repertoire through its own
demonstration, every one of its six standing rows re-derives from committed
bytes by an independent reading, and the two round-72 closure defects are now
standing-measured.

### R73-C2 — operability (the rekey-cost arm battery becomes executable)

**Before (re-measured).**

```
git show a3dd3574:tools/rekey-cost.py | grep -c REKEY_ARMS   -> 0
M3 over the six recorded arms (receipt reh/reh-c2-m3-six-arms.txt) -> KILLING_ARMS=0/6
```

**After (re-measured).** `git show 5c9a5559:tools/rekey-cost.py | grep -c
REKEY_ARMS` → `2`. This verifier re-implemented the documented forecast rule
(split `SKILL.md` on `^#{1,3}` outside fences, newest ledger entry per heading,
a section at risk when a planned path is in that entry's `inputs`, `IGNORED`
removed) over the committed blobs at both revisions:

```
a3dd3574 pristine {sources 13, province 6, quality 6, scorecard 0,
                   pointer 0, union 17, ignored-skill 0}  sections 64  entries 820
a3dd3574 M3       {… ignored-skill 9}          (IGNORED filter dropped)
5c9a5559 pristine {sources 13, province 6, quality 6, scorecard 0,
                   pointer 0, union 17, ignored-skill 0}  sections 64  entries 852
5c9a5559 M3       {… ignored-skill 9}
```

So the six recorded arms read the same under pristine and mutant at the base
(`KILLING_ARMS=0/6`, the before-state), and the round-73 seventh arm
(`ignored-skill`, expected 0) measures 9 under M3 — the mutant is killed on
both sides of the round. The republication does not move any arm across the
rekey (`13/6/6/0/0/17/0` at base and tip); `sections=64` and `entries 820 → 852`
are the report's own figures.

**Evidence-verified.** `rekey-arms-r73.txt` → seven `REKEY_ARM` lines,
`REKEY_ARMS: arms=7 meet=7 unexpected=0` exit 0, `REKEY_COST_SELFTEST: 8/8
pass`; `reh/reh-c2-m3-battery.txt` → pristine 7/7 and mutant
`ARM_UNEXPECTED ignored-skill expected=0 measured=9` with
`arms=7 meet=6 unexpected=1` exit 1.

**Verdict: `improved`** — the recorded arm table is now a re-runnable battery,
the ignored-path arm the round-72 coverage finding named is present and is the
one that kills M3, and the value set reproduces independently at both revisions.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | unchanged | `SKILL.md` blob `95d1f935…` identical base→tip; no new decision-table case; `SCORECARD.md` diff `85 0` (appends only) |
| coverage | unchanged | `corpus/README.md` blob `d0ffbfb8…` identical; no frontier row advanced (the report says so and the blob agrees); `PROVINCE.md` `98296a40…` identical |
| operability | **improved** | `tools/rekey-cost.py --arms` is a runnable 7-arm battery (selftest 8/8, arms 7/7); the rule reproduces independently at base and tip |
| freshness | unchanged | no stale source item flagged or fixed by the round; the S066 re-open is a curation event (§4), the freshness counter's population is untouched (163 rows → 163) |
| calibration | **improved** | a new record-vs-artifact reconciliation gate whose six rows re-derive independently; the two round-72 closure record defects are now standing red arms; the round caught its own S066 collapse in-round and adopted four seat attacks as work |
| adjacency | unchanged | no sibling write; the connector seat read `kaidoku-shokunin/tools/round-47/record.py` read-only (`ASSIMILATION=readable`); `PROVINCE.md` identical |

**No axis is harmed.** Content is preserved on every file the round touched:
`corpus/QUALITY.md` normalised old-only 0 (base 1,915 CRLF → tip 0; raw
old-only 1,915), `LOG.md` raw old-only 3,759 with 0 content deletions
(`git diff --ignore-cr-at-eol` → 50 lines, all additions), the ledger is
raw-additive (base→tip `raw_old_only=0`, CRLF 303,657 → 336,698), and
`corpus/SOURCES.md` raw old-only 1 (the documented S066 `used-by` cell edit).
The cold-read monitor reads `lost=0 ok` at both floors and `credited=64/64` in
rev mode at `06ce20f7` (verified receipts). The two EOL rewrites are a record
discipline defect, not a content loss — routed in §6.

## 4. Discernment spot-check (`corpus/lessons/round-73.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S066 RFC 8259 re-open for §8.1 (encoding + BOM ground) | admit | `.ufo/evidence/round-73/sources/rfc8259.txt` at the tip (sha256 `61a5378f4255…`, 28,360 B; headers `date: Wed, 04 Nov 2026 00:58:08 GMT`): page lines 485–486, 494–495, 496–498 | **agree** | all three quotes occur at the stated lines; word counts 18 / 17 / 21 (each ≤25); the two normative sentences and the permitted-alternative sentence ground the instrument's UTF-8 and fail-closed-BOM rules exactly; `used-by` gained `corpus/lessons/round-73.md` (old→new logged in the lesson; rule 2 permits `used-by` in place) |
| A new RFC 8259 row for the §8.1 ground | reject (standing, re-sampled) | the same snapshot plus `corpus/SOURCES.md:75` (S066) and the S289/S293 precedent rows (`S293` reads `REJECTED: within-scope duplicate — the URL is already held as S289 …`) | **agree (wording caveat)** | the URL and document are already held by S066, and the lane's established precedent (S293 for S289) is to re-open instead of holding a second row; a duplicate-URL row would surface as census `W04 … across scopes` and validate clean, which the lane itself restates in Gate §2 — so "within-scope duplicate" is the precedent's term, not an error claim. The flip condition is named and honest |
| ≤25-word quote check on a newly written SOURCES row | n/a — no new row this round | `grep -cE '^\|[[:space:]]*S[0-9]{3,}'` on the base and tip blobs → `163` and `163`; malformed rows 0; tiers `A 145 B 14 C 4` | **agree** | the round writes no row (the honest rejection of a duplicate); the three quotes it does carry are the re-open's and were checked above against the snapshot at their stated lines |
| Census sentence correction (r72 closure defect 3) | admit (mechanism) | live `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` and `S303`'s row: `grep -c E04` → 0, `W04.*S303` → 1 | **agree** | the live registry prints `tameshi W04 S303 duplicate url … across scopes` and `tameshi ok` exit 0; the round-72 sentence's E04 is a same-scope-fixture effect, exactly as the correction states |
| Census validate | gate | this verifier's own run | **agree** | exit 0, `tameshi ok`, 163 rows; warnings only (`18` W04 + `1` W01 S101; no E rows). The report's prose "19 × W04" is off by one (defect 4) |

## 5. Trend verdicts

- **expansion — improved.** A capability entered `SCORECARD.md` `## Capabilities`
  (`wave-record reconciliation`, first working round 73) through a demonstrated
  run, and the round's sourced claim rests on a re-opened row (S066 §8.1) with
  three fresh located quotes and three new QUALITY criteria (121–123). No new
  knowledge entry and no frontier move — the report states both, and the blobs
  agree (`corpus/README.md` identical).
- **quality — improved.** Two round-72 closure defects now stand as measured
  red arms on every sweep; three falsifiers were corrected to revision-stable
  forms (criterion 122 pinned to the round-72 bytes it contradicts); the cold-
  read monitor reads `lost=0 ok` at both floors and `credited=64/64` in rev mode
  after three rekeys; two seat findings were hardened in-round with the frozen
  counters unchanged. The round repeats the r72 EOL class on `QUALITY.md` and
  `LOG.md` without disclosure — content is preserved and the monitor is green,
  so no admitted entry failed its re-check (not `harmed`), but the record
  defect is routed (§6).
- **discernment — improved.** This verifier agrees with the obviously
  admissible admit and the standing reject; four seats' attacks were adopted as
  work (S03's three binding defects, S05's collapsed row, S02's docstring
  overclaim, S04's unstable falsifier), S10's W2 gap and S09's M3c
  over-filtering mutant are carried as named gaps instead of argued away, and
  one self-caught mistake is recorded in `## Mistakes`. The one wording caveat
  above and the undisclosed EOL rewrites are routed, not absorbed.

## 6. Routed defects for the lane (status-neutral; next round)

1. **`corpus/QUALITY.md` EOL rewrite, undisclosed.** `21a7332f` (the
   criterion-122 re-pin) rewrote the file CRLF→LF: base 1,915 CRLF → tip 0;
   base→tip `raw_old_only=1,915`, normalised old-only 0. The report's sentence
   "additivity raw `raw_old_only=0` on the ledger and QUALITY" is true only of
   the two additivity receipts it ships (`…2e89e539`, `…caa5c4c5`), both taken
   before `21a7332f`; no receipt covers the manual edit commit. The r72 lesson
   made the additivity receipt a named step of the *rekey* run-book — extend it
   to manual corpus edits, and append the disclosure/errata (or rebuild on the
   CRLF base, the r72 `b611e763` precedent).
2. **`LOG.md` EOL rewrite, undisclosed.** `862e8844` rewrote the append-only log
   CRLF→LF: base 3,759 CRLF → tip 0; `raw_old_only=3,759`, content-preserving
   (`git diff --ignore-cr-at-eol 862e8844^ 862e8844 -- LOG.md` → 50 lines, 0
   content deletions). `FILE contract` says `LOG.md` is append-only; disclose
   the rewrite or restore the base bytes.
3. **Frozen plan kill-rule wording.** The plan still carries the sentence
   "C1 fails if … any control below reaches `unexpected=0`", contradicted by
   the green-only control (`rows=4 met=4 unexpected=0` exit 0). The round
   reports it in the report/lesson but appends no erratum to
   `plans/round-73.plan.md`; the r72 erratum (`3e0ef1c8`, appending to
   `plans/round-72.plan.md`) is the precedent. The operative predicate (the
   six-row line) is unaffected.
4. **Report minor counts.** (a) The landed-changes table lists 22 of the 23
   round commits — `e309f59f` (the `LOG.md` post-wave entry) is missing;
   (b) the census summary says "19 × W04" where the receipt and the live run
   read `18`.
5. **Gate registry row.** `tools/wave-reconcile.py` meets the gate shape but has
   no row at the lane's registry home (`SKILL.md`; also absent from
   `tools/registry.json`), and neither do the six standing instruments the
   report lists. PROTOCOL §Gate standard §Delivery: closure grades no gate
   conformant until its registry row exists; add the rows (name, gate/probe,
   entry command, verdict map, selftest command, pinned-value path, write
   scope, owner).
6. **Carries from the wave (the lane already names them; keep on the queue).**
   Delimited-token and span-substring selftest arms (`delimited := True`
   survives 12/12, T73W1S02); `seat_reports` counting at any depth (W2 survives
   the sweep, `files=12` vs `13`, T73W1S10 — this verifier confirms 12
   top-level vs 17 any-depth on the r72 wave); the IGNORED filter's
   over-filtering direction (M3c, T73W1S09); rounds 61–71 carry no
   `results.json` (11 unpinnable rounds) and round 60's vocabulary is
   `agent='task'` (T73W1S06).
7. **Inherited record misses (not this round's debt).** SCORECARD 20 missing
   cited paths and LOG 5 missing quotes at the tip, disclosed in
   `inherited-misses-r73.txt`; inherited from rounds 17–66 and 35/41.

## 7. Closure

Conformance: real report, lane identity `tameshi-shokunin`, `SHONEN` heading
with four `[~]` lines against four boxes, all 23 round commits ancestors of
`refs/heads/master`, lane clean and pushed (`ahead=0`), prompt a faithful
template rendering plus the run-15 addendum. Claim C1 verifies — re-derived
row by row from committed bytes by this verifier, with the two red arms
measured and the selftest/sweep receipts evidence-verified. Claim C2 verifies —
the rule re-implemented independently reproduces all seven arms at base and
tip and kills M3 on both sides. No axis is harmed; two EOL rewrites and four
minor record defects are routed. **Admitted.**
