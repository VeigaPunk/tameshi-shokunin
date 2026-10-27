# Fleet round-1 lesson — tameshi-shokunin (2026-10-15)
## Promotion assertions: who may mark `[x]`, what durable proof looks like, and what one mutant proves

Authored by the fleet round-1 **LessonExecutor** seat; this file (`corpus/lessons/round-1.md`)
is that seat's only write. Every agent in the round-1 batch is tameshi-dispatched, so every
verdict below is a **lane-local check, never `[x]` promotion authority**
(PROTOCOL.md — `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:63-68`).

**Disambiguation — two different "round 1" [O].** The historical probation/training arc ran
rounds 1–11 on 2026-10-14 (round 1: `LOG.md:5-8`; its depth/calibration move rows:
`SCORECARD.md:39-40`; the ten-round verdict table: `SCORECARD.md:54-80`). This lesson is
**fleet round-1** (2026-10-15), a separate baseline declared in `LOG.md:392-393`
("(separate from the completed historical training arc)"). The register numbering follows the
round id, not chronology: the register's first entry is the historical
`corpus/lessons/round-10.md` (248 `wc -l` lines); this is its second
(`corpus/lessons/` measured 1 file at this write, `glob corpus/lessons/*`).

Anchors: **O** observation · **I** inference · **U** unknown — kept separate per
`corpus/QUALITY.md:6`.

**Revision pins at this write** (commands in §Re-run below; a reader on a differing
revision re-resolves rather than trusts):

| cell | value |
|---|---|
| HEAD at write | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` (`284ab0f`, 2026-10-14T19:49:31−03:00, round-11 closeout) |
| working tree at write | ` M LOG.md`, ` M SCORECARD.md`, ` M SHONEN.md` — fleet-round-1 rows and the SHONEN rework are **uncommitted at this write** (sole integration: parent); cite lines carry "at write" |
| baseline SHONEN | `git show 284ab0f:SHONEN.md` → sha256 `b158a0785ae4f312…` (first16); the four boxes at `:5-34` are baseline content — the blob, not the mutable file, is the durable pointer |
| canonical seed | PROTOCOL.md:419-431; the four seed lines :425-428 hash `1761fd68e0660c35…` (first16 of `sed -n '425,428p'`) |
| measured rubrics | `SCORECARD.md` §Current axes (relocated to `:58-85` at write to preserve historical line cites); command D `recorded_cases=6 depth_score=6`; command C, baseline: `boxes=4 checked=4 asserted=0 untouched=0` (`LOG.md:400-401`) |

## The observed trigger [O]

At the measured commit, `SHONEN.md:5-34` marks **every box `[x]`** with verifier ids
TAMESHI-B1/B2/B3/B4 and evidence pointers living under `/tmp/...`. `LOG.md:395-398` records
the finding in the baseline entry: those marks use "tameshi-dispatched B1/B2/B3/B4 evidence
and temporary paths", against canonical requirements at PROTOCOL.md:63-73 (lane-dispatched
agents are still the lane; `[x]` only from a non-author id), :340-343 (evidence must resolve
at closure; `/tmp` is not evidence) and :413 + :419-431 (canonical box wording; marks
confined to the box character plus one indented evidence line). The calibration axis is the
lowest measured (0 vs depth 6), making this the falsifiable next move
(`SCORECARD.md:66-67`, `LOG.md:402`). The calibration axis definition — "gaps named
honestly, confidence graded, overreach caught" — is `<fleet-root>/AXES.md:15`.

## The distinctions

1. **`[x]` authority is an identity property, not a quality property [O/I].** The B1–B4
   artifacts themselves were substantive (the executed sweeps and the executor test are
   recorded at `corpus/knowledge/mutation-case-kagi-census.md` and
   `corpus/knowledge/executor-test-sufficiency.md`). They still cannot license a `[x]`,
   because the protocol gates on *who writes the mark*: "a subagent the lane dispatched is
   still the lane" (PROTOCOL.md:64-65; LEARNING.md:42), and "only a non-author `<id>` may
   write `[x]`" (PROTOCOL.md:66-67). [I] A lane can hold excellent evidence and a zero
   promotion score at the same time — the marks must fall to lane-authored `[~]` with
   pointers, and the score rubric pays for restraint (`SCORECARD.md:67`: two points per
   *correctly restrained*, durable-evidence-linked `[~]`), not for confidence.

2. **A pointer must resolve at closure, not at write [O].** `/tmp/tameshi-b*` receipts were
   real receipts, and PROTOCOL.md:340-343 bars them anyway: tmpfs paths and session-scoped
   artifacts "are not evidence — commit the artifact or cite a reproducible command." The
   lane has already learned this in both directions: round 10's own falsifier names "a pass
   that exists only in scratch" (`corpus/lessons/round-10.md:206-207`), and its gate refused
   an executed-but-unreported verifier report ("not counted as landed",
   `corpus/lessons/round-10.md:197`). Fleet round 1 caught the same defect standing in the
   promotion file itself — the gate's written rules held over the file they govern. [I] The
   durable replacement shape for the B-series receipts is committed report rows with fixed
   headings in this repo (the round-1 report, `reports/round-1-calibration.md`, plus the
   baseline `LOG.md`/`SCORECARD.md` rows the parent integrates).

3. **A historical one-mutant success proves exactly one mutant [O].**
   `corpus/knowledge/executor-test-sufficiency.md` measures, honestly scoped: an executor
   with no oral context beyond `SKILL.md` reproduced **one killed mutant end-to-end** — D5,
   JS case (`:3-8`); the bash case was not touched and the scope was "ONE killed mutant …
   not a full 10-defect sweep" (`:52-54`); the `--only` subset mode was
   ADDITIVE-IMPROVISATION, not described by the recipe (`:116`, `:126-134`); the note's own
   §5 confirms the SKILL's core claim "for the executed scope" only (`:155-163`). The
   overreach did not live in the note — it entered the box line that credits it, which read
   as a **current, whole-skill cold-read capability** claim. This round's gate rejected that
   reading rather than laundering a subset into a blanket claim: the critic seat found the
   broad current box-3 assertion unsupported by the historical n=1 JS D5 result, and the
   parent's recorded decision keeps box 3 `[ ]` with candidate calibration **6, not 8**
   (lane-local decision report at this write; durable home pending — see §Gate). [I] Evidence
   carries its scope stamp with it: a `[~]` line earns its points by bounding its claim to
   what was executed, at what revision — the box-3 case is now the worked example.

4. **Mark counting is a census, not credit [O].** The round's command C was reworked to a
   capped mark census (`SCORECARD.md:74-75` at write: `asserted_mark_upper_bound`); candidate
   8 additionally requires the exact canonical seed diff, four resolvable same-revision
   evidence links, and a semantic source review — not the counting of `~` characters
   (`SCORECARD.md:67`, `:80-81` falsifier). [I] The census/rubric split is the same
   discipline the mutation notes carry (executed counters vs static site counts,
   `corpus/README.md` coverage rows): a syntactic count bounds a claim; it never establishes
   it.

## Gate

Per CORPUS.md:18-19 and LEARNING.md:61-62. All verdicts are the lane's own admissions under
`corpus/QUALITY.md` (falsifiable, source-cited `:4`, separated classes `:6`, rejections kept
`:8`); none is promotion authority.

- **Candidates considered:** the promotion-independence correction; the canonical
  box-form/wording correction; the durable-pointer correction; the capped census rubric; the
  box-3 blanket cold-read assertion (historical one-mutant success read as full/current
  capability); a new cross-domain/general pattern from this round; a new general
  `QUALITY.md` criterion.
- **Admitted (corrections):** independence — lane-dispatched verifier ids count as the lane,
  baseline `[x]` marks fall to `[~]`-or-`[ ]` (PROTOCOL.md:63-68); canonical wording — the
  four seed boxes verbatim with `<name>` = tameshi-shokunin (PROTOCOL.md:419-431); durability
  — same-revision in-repo pointers replace `/tmp` receipts (PROTOCOL.md:340-343); scope
  bounding — evidence lines may assert only the executed scope at the executed revision
  (`executor-test-sufficiency.md:3-8,52-54,155-163`). The landing of these corrections into
  `SHONEN.md` is the ChecklistExecutor seat's write and the parent's integration — state at
  close is **[U]** here, never asserted.
- **Rejected, with reasons (kept per `corpus/QUALITY.md:8`):**
  1. **Box-3 blanket claim** — the historical n=1 JS D5 execution cannot support a current,
     whole-SKILL, both-appendix cold-read assertion; laundering a subset into a blanket claim
     fails `corpus/QUALITY.md:3` (falsifiable, bounded) and the evidence standard's
     claimed-vs-re-executed rule (PROTOCOL.md:345-346). Decision recorded: box 3 `[ ]`,
     candidate calibration 6, not 8. The rejection itself is the round's calibration earn —
     overreach caught before it lands.
  2. **Promotion by this batch** — no agent in the task batch is an independent promotion
     verifier (none exists in the batch; PROTOCOL.md:63-68), so `[x]` authority and the
     rubric's reserved 2 points stay unearned (SCORECARD.md:67).
  3. **No new cross-domain pattern claimed** — the ≥2-independent-lane rule for calling any
     pattern general (`corpus/knowledge/verification-patterns-fleet.md:16`; the same sentence
     in this repo's `PROVINCE.md:15-16`, wrapped across two lines) is unmet: every round-1
     contributor is one lane. Nothing general is admitted from this round.
  4. **No new `QUALITY.md` criterion** — the existing bar already sources, separates, and
     keeps rejections (`corpus/QUALITY.md:4,6,8`); LEARNING.md:32 bars a criterion with no
     lesson behind it, and inventing a general criterion from a single-lane round would
     violate exactly the rejection in item 3. QUALITY is unchanged by this lesson.
- **Spot-check result — NOT performed [O].** No non-author of this lane's gate decisions
  spot-checked the admits/rejects this round: agents dispatched by this lane are still the
  lane (LEARNING.md:39-43; PROTOCOL.md:64-65). Discernment trend verdict: **unprovable**
  (LEARNING.md:25-26 vocabulary), named honestly, not manufactured.
- **Open external review (named, pending):** (a) a non-author operator or fresh-reviewer
  spot-check of at least one admit and one reject from this `## Gate`, recorded as an
  append-only entry below (CORPUS.md:52-55 — corrections are new entries, never rewrites);
  (b) the independent promotion review of all four boxes that the calibration rubric's
  reserved 2 points require (`SCORECARD.md:67`); (c) the parent's post-integration smoke of
  the actual CLI, whose output the round report must carry as a committed row
  (`reports/round-1-calibration.md`, absent at this write — `glob reports/*` → 7 files,
  all historical). Until (a)–(c) land, this round's discernment stays unprovable by
  construction.
- **Falsifier (what would defeat this lesson):** any current `[x]` on the four boxes without
  a named non-author verifier; any `/tmp`-path cited as durable evidence; any box line whose
  claim exceeds the scope of its cited execution; any score cited without its counting
  command and measured commit; any "general" pattern claimed from this single lane.

## Round-record pointers (fleet round-1)

- `LOG.md:392-403` — fleet round-1 calibration baseline entry (working tree at this write;
  carries motivating evidence, the rubric commands' observed outputs, and the axis pick;
  commit hash at close [U]).
- `SCORECARD.md:58-85` — Current axes: depth 6 / calibration 0 at
  `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`, commands C (capped census) and D, planned
  calibration move and its falsification (working tree at this write; section relocated from
  the provisional `:7-34` so historical move-log line cites stay valid — do not cite the
  provisional range).
- `reports/round-1-calibration.md` — the round report (EvidenceExecutor seat); absent at
  this write — the durable home for the admits/rejects above plus the parent smoke; the
  parent was asked to land them before shipping. Pending ≠ evidence until committed
  (PROTOCOL.md:340-343).

## Unknowns carried [U]

The fleet round-1 landing commit; the landed `SHONEN.md` state and whether its marks match
the recorded decision (box 3 `[ ]`, boxes 1/2/4 `[~]`, candidate 6); whether the report and
smoke rows land; whether external review (a)–(c) ever lands; whether a future full-sweep,
both-appendix, current-revision cold read (executed by a seat with no lane context) can
re-earn box 3 — nothing here says it cannot, nothing here says it has.

## Re-run

```sh
cd <fleet-root>/tameshi-shokunin
git log -1 --format='%H %cI'                              # 284ab0f… at this write; re-resolve at close
git show 284ab0f:SHONEN.md | sha256sum | cut -c1-16       # b158a0785ae4f312
git show 284ab0f:SHONEN.md | sed -n '5,34p'               # four [x]; B1..B4 ids; /tmp pointers
REV=284ab0f0b8b989ee73d9c00c0c0df0a59757af8d              # commands C and D verbatim:
sed -n '/^```sh/,/^```/p' SCORECARD.md                    #   SCORECARD.md command block (:71-76 at write)
grep -n 'fleet round-1' LOG.md SCORECARD.md               # baseline entry + axes section (at-write lines)
sed -n '3,8p;52,54p;104,134p;155,163p' corpus/knowledge/executor-test-sufficiency.md
sed -n '14,18p' PROVINCE.md                               # the rule wraps :15-16 — a one-line grep
                                                          #   for "TWO independent lanes" misses it there
grep -n 'TWO independent lanes' corpus/knowledge/verification-patterns-fleet.md  # :16, contiguous quote
sed -n '425,428p' /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md \
  | sha256sum | cut -c1-16                                # 1761fd68e0660c35 — the canonical seed four lines
```

## Errata (append-only)

(none yet — new entries go below this line, never edits above, per `corpus/QUALITY.md:7`
and CORPUS.md:52-55; the first expected entrant is the external spot-check of this
round's `## Gate`, agree/disagree with reason.)

### ER-I1 — interactive continuation and admission hold (2026-10-15)

The interrupted headless work above is retained as at-write testimony,
not freshly replayed native-session evidence. This continuation stays
within the same unfinished **fleet round 1**; it does not reopen the
historical training arc or count a driver launch as a verified round.
The historical move rows cited at lines 10–11 resolve at
`SCORECARD.md:11-12`; the ten-training-round verdict table is at
`SCORECARD.md:41-52`, not the ranges quoted there.

Correction to lines 134 and 143: `unprovable` is not the canonical verdict
token. Current discernment is **unprovable-but-better**: overclaims are
explicitly rejected, but no outside spot-check of one admit and one reject
exists. The lane's own parent or dispatched seats cannot supply that
outside authority (`LEARNING.md:37-43`). This token does not mean the
outside criterion passed.

The previously absent audit exists at `reports/round-1-calibration.md`.
Its `## Interactive continuation` section records this parent's direct
source review and fresh CLI/selftest evidence, separately from the
inherited measurements above. Reproducible local comparison and full
command outputs are in `.ufo/evidence/fleet-round-1/`: baseline four
unsupported `[x]` / no canonical box rows / no durable checklist links;
candidate canonical rows with `[~], [~], [ ], [~]` and four resolving
links. The supporting source review remains lane-authored. The actual
CLI observed one killed and one survived defect plus byte-identity, not a
new fleet rate, a whole cold-read or a promotion review.

**Admission hold:** current role bindings do not realize content
`@m_composer`, audit `@m_grok`, connector `@m_antigravity` with `@m_zfl`
fallback. The exact missing bindings are persisted in
`.ufo/evidence/fleet-round-1/route-bindings.json` and the live config
observation beside it. The canonical wave planner validated 32 distinct
scopes, exit 0; no `run` registry or specialist dispatch was produced.
Thus the local correction is retained, but this attempt earns no
verified-round credit. The older nine-seat narrative is not current
exact-32 compliance.

Admit the bounded authority/durability corrections already listed under
`## Gate`; reject route substitution, invented receipts and round-credit
from plans or live panes for the same evidence-standard reason. These
are lane-local decisions, not new general patterns or new QUALITY
criteria. Outside review is still pending. Unblock: the authorized route
owner supplies the existing alias bindings, then a fresh session
reconciles this handoff, dispatches the complete canonical 32-scope
payload, and runs acceptance after integration. No second round runs
inside this session.

### ER-I2 — own scratch-policy miss, corrected before commit

The first interactive CLI smoke used `.ufo/scratch` and therefore did
not meet this lane's existing `SKILL.md:25-28` namespace rule. Successful
behavior and later deletion did not make that run conforming. Its output
is kept in `.ufo/evidence/fleet-round-1/cli-smoke.json` as a rejected
admission candidate, superseded explicitly by the audit's scratch
erratum. No generic new quality criterion is needed: the existing
standing rule already decided this case.

The parent corrected only the namespace and ran the real CLI in a fresh
`/tmp/tameshi-r1-…` directory. Reproduction program, full output and exits:
`.ufo/evidence/fleet-round-1/cli-smoke-canonical.json`. At 05:14:49Z:
green control, the observable defect killed, unasserted defect survived,
byte-identical target; runner and driver exits 0. Temporary files were
removed after capture, not cited as the closure dependency. No selftest
or reported Phase 0 failure was rerun to confirm an already known result.
This corrects the namespace failure, not the independent-review,
current full cold-read, exact-routing or receipt prerequisites.


## Mistakes (kaika continuation, 2026-10-19)

Mined from the lane's own record — rejected, erratum-carrying and
debt-carrying rounds — per the kaika W1 STATE dossier §4–§5
(`/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tameshi-state.md:59-107`,
a non-author read-only sweep; every pointer below was re-resolved by the
lane at 2026-10-19 in worktree base `4eb4cf3`). No landed row records a
`harmed` verdict (`grep -c 'harmed' LOG.md` → 0 at base) and no honest-stop
round exists; the blocked fleet round-1 dispatch is one blocked attempt
(`LOG.md:524-525`). Format: class · evidence pointer · captured-by
criterion or `none` · fix.

| # | Class | Evidence pointer | Captured by | Fix |
|---|---|---|---|---|
| MK-1 | Citation drift: line cites transcribed from a stripped view | `corpus/knowledge/gates-survey-kagi.md:508-543` (ER-1, 16 wrong-line cites) | `QUALITY.md` 2 + `SKILL.md` re-resolve rule | none needed |
| MK-2 | Pre-registered prediction wrong, kept only by author habit (round 2, D7) | `corpus/knowledge/mutation-case-kimi-census.md:185`; `LOG.md:90` | none — no criterion binds a *prediction* (vs a claim) to its executed outcome | `QUALITY.md` 6 |
| MK-3 | Same class repeated one round later (round 3, failing-case counts) | `corpus/knowledge/mutation-case-kagi-census.md:186`; `LOG.md:196-198` ("same shape as round-2 E1") | none (repeat of MK-2) | `QUALITY.md` 6 |
| MK-4 | Index lags the corpus: knowledge files land without coverage-map rows | `corpus/lessons/round-10.md:175-176` (9 rows / 6 of 16 notes); at base 9 rows / 6 of 19 notes — `grep -cE '^\| \`knowledge/' corpus/README.md` → 9 | none — `CORPUS.md` bars *premature* rows only | `QUALITY.md` 7 |
| MK-5 | Executed verification never landed as a report | `LOG.md:368`, `:383`, `:389` (`reports/r10-ver-t10.md`, `reports/r11-ver-t11.md` absent); principle already stated `corpus/lessons/round-10.md:129` | none — stated as a lesson, never a bar | `QUALITY.md` 8 |
| MK-6 | Evidence retained only under `/tmp`, later lost | `corpus/knowledge/executor-test-sufficiency.md:14-18` (evidence under `/tmp/tameshi-r3-4-work/`); `ls -d /tmp/tameshi-r3-4-work` → `No such file or directory` 2026-10-19; fleet rule `PROTOCOL.md:341-343` | fleet `PROTOCOL.md` only; the lane's own scratch rule (`SKILL.md:25-28`) sends scratch to `/tmp` and says nothing about copying evidence out | `QUALITY.md` 9 |
| MK-7 | Entries admitted without provenance header or recheck cadence | 19/19 entries: `for f in corpus/knowledge/*.md; do head -5 "$f" \| grep -c '^source:'; done \| sort \| uniq -c` → `19 0` at base; canonical `CORPUS.md` §Layout | none — `QUALITY.md` 2 demands an anchor, not the header form or a recheck | `QUALITY.md` 10 (new entries); old entries: named debt, see below |
| MK-8 | Substrate moved mid-run | `plans/round-5-record-draft.md:108` (incident I1) | `corpus/lessons/round-10.md` lesson 3; ledger drift semantics | none needed |
| MK-9 | Scratch-namespace miss | ER-I2 above | `SKILL.md:25-28` | none needed (ER-I2) |
| MK-10 | Overreach: one historical JS mutant read as whole-skill cold-read capability | `## Gate` rejected-1 above | `QUALITY.md` 1/3 | none needed |
| MK-11 | Same-lane authority claimed as independent | `## Gate` rejected-2..4 above | `PROVINCE.md:15-16`; fleet `LEARNING.md` | none needed |

Unlearned classes this round: MK-2/3, MK-4, MK-5, MK-6, MK-7 → five
criteria appended to `QUALITY.md` (6–10), each citing its row here.

MK-7 repair limit (named debt, not a rewrite): prepending three header
lines to the 19 existing entries would shift every `path:line` cite into
them (the ER-1 lesson, MK-1), harming depth and calibration evidence.
The 19 old entries keep their bytes; the header bar binds new entries
from this round on. Route chosen for the old ones is an operator call
(round report, L0 questions).

## Gate — kaika continuation (2026-10-19)

Candidates this round, admitted and rejected with reasons. The
non-author spot-check (≥1 admit, ≥1 reject) is the orchestrator's after
landing; lane seats (Reviewer, Critic) are still the lane and are not it.
Spot-check result: **pending** — recorded here when it lands, as an
appended entry.

**Admitted**

- `knowledge/mutation-score-semantics.md` (F1) — clears `QUALITY.md`
  1–10: formulas recomputed with arithmetic shown, five sources
  re-opened with hashes (`.ufo/evidence/kaika-round-1/score-semantics/opened.tsv`),
  O/I/U separated, NoCoverage kept U, rejected rule kept, header present.
- `knowledge/witness-scoped-kill-verdict.md` (F2) — pre-registered split
  (declaration sha256 `32241b02…e9dd` at 22:05:45Z, sweep at 22:07:13Z),
  8 killed-on-witness / 0 accidental / 2 survived = recorded 8/10;
  contamination recorded (an unscoped grep exposed historical outcomes
  before declaration — the split is **not blind**, and the entry says so).
- `SOURCES.md` rows S001–S030, S040–S045 (re-opened this round, table
  below) and own/gate rows S031–S037 (anchored by path @ commit with
  blob sha256; no quote — the source is the lane's own re-runnable
  output or a pinned sibling blob).
- SHONEN box 3 `[ ]` → `[~]` (lane assertion): `../../reports/round-1-kaika-coldread.md`
  — `COLDREAD: SUFFICIENT (appendixA=8/10 recorded=8/10 appendixB=8/10 recorded=8/10 blocking-gaps=0 wrong-expectations=0 survivors-probed=4/4)`
  against `SKILL.md` sha256 `33e3009c…0f81` (unchanged this round).
  Scope bound kept in the box line: service, cadence and runbook
  sections not exercised.

**Rejected (kept)**

- S029 mutate4bash, S030 LLMShot (re-opened; reasons and flips in the
  rows), S046 pbt-bibliography (community index, not primary support).
- Rule "count Timeout as a kill" (Stryker's) — no denominator evidence
  (`SKILL.md:191-193`, `:208-209`); kept as a comparison only.
- Claim K3 "coverage 0 → 2 frontier grounds held" — withdrawn before
  landing on the Critic seat's findings: the rubric was pinned in the
  same round it moved, a header-count proxy is gameable, and the
  entries depend on K2's mined rows (not causally separable). The two
  entries stay admitted as knowledge (expansion trend) and as the
  demonstration that K2's registry mines into admitted entries.
- Folding decision-table rows into `SKILL.md` this round — rejected:
  any `SKILL.md` edit would move the bytes the cold-read executed
  (`33e3009c…`) and re-open box 3.
- Header repair on the 19 pre-round entries — rejected as a rewrite
  that shifts cited lines (MK-7).

**Status changes (contract rule 2, old → new):** S005 `queued` → `mined`
(used-by `corpus/knowledge/mutation-score-semantics.md`); S006 used-by
gained `corpus/knowledge/mutation-score-semantics.md`. Both before the
round commit; no committed row changed.

**Fetch records for every new external row** (URL · access UTC · ≤25-word
quote · location; sha256 of each fetched body in
`../../.ufo/evidence/kaika-round-1/sources-opened.tsv`):

| id | URL | accessed | quote | location |
|---|---|---|---|---|
| S001 | https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ | 2026-10-19T21:43:50Z | Mutation score detected / valid * 100 | §Metrics, docs page fetched 2026-10-19 |
| S002 | https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json | 2026-10-19T21:43:50Z | enum: ["Killed", "Survived", "NoCoverage", "CompileError", "RuntimeError", "Timeout", "Ignored", "Pending"] | mutation-testing-report-schema.json:92 (MutantStatus), master |
| S003 | https://stryker-mutator.io/docs/stryker-js/incremental/ | 2026-10-19T21:43:50Z | Any other changes to your environment are not detected, such as ... changes to environment variables, changes to .snap files | §Limitations, docs page fetched 2026-10-19 |
| S004 | https://mutants.rs/using-results.html | 2026-10-19T21:43:50Z | This is inconclusive about test coverage and no action is needed | §Mutant outcomes (unviable), mutants.rs fetched 2026-10-19 |
| S005 | https://raw.githubusercontent.com/boxed/mutmut/main/HISTORY.rst | 2026-10-19T21:43:50Z | Fix mutants stopped by the CPU-time limit being reported as killed instead of timed out | HISTORY.rst:23 (§3.8.0), main |
| S006 | https://github.com/BWBama85/shmutant | 2026-10-19T21:43:50Z | The suite went red, but not on its witness. Caught by accident, not by the assertion that claims to cover it. | README §The three verdicts; page currentOid 7eefc73010ad6342b80e3ed43915503e02c90618 |
| S007 | https://arxiv.org/abs/2501.12862 | 2026-10-19T21:43:50Z | an LLM-based equivalent mutant detection agent that achieves a precision of 0.79 and a recall of 0.47 | Abstract, arXiv:2501.12862v1 (submitted 2025-01-22) |
| S008 | https://arxiv.org/abs/2102.11378 | 2026-10-19T21:43:50Z | more than 24,000 developers on more than 1,000 projects | Abstract, arXiv:2102.11378v2 (last revised 2021-02-26) |
| S009 | https://discovery.ucl.ac.uk/id/eprint/1499169/ | 2026-10-19T21:43:50Z | TCE can discard more than 7% and 21% of all the mutants as being equivalent and duplicated mutants respectively. | Abstract, UCL Discovery eprint 1499169 (ICSE 2015), page fetched 2026-10-19 |
| S010 | https://discovery.ucl.ac.uk/id/eprint/1508136/ | 2026-10-19T21:43:50Z | Type I errors occur, for arbitrary experiments that fail to take countermeasures, approximately 62% of the time | Abstract, UCL Discovery eprint 1508136 (ISSTA 2016), page fetched 2026-10-19 |
| S011 | https://mir.cs.illinois.edu/awshi2/publications/ISSTA2019.pdf | 2026-10-19T21:43:51Z | mutation scores vary by four percentage points on average between repeated executions, and 9% of mutant-test pairs have an unknown status | Abstract, ISSTA 2019 PDF p.1, fetched 2026-10-19 |
| S012 | https://arxiv.org/abs/2608.17214 | 2026-10-19T21:43:50Z | An expectation is specification-anchored when composed from values fixed outside the code under mutation, and state-anchored when it flows, directly or transitively, from that code. | Abstract, arXiv:2608.17214v1 (submitted 2026-08-17) |
| S013 | https://jestjs.io/docs/cli | 2026-10-19T21:43:51Z | Discover and print all test suites and test names without executing them | §Options, --collectTests, Jest docs Version 30.5 |
| S014 | https://insta.rs/docs/advanced/ | 2026-10-19T21:43:51Z | auto: the default. no for CI environments or new otherwise | §Controlling Snapshot Updating, insta docs fetched 2026-10-19 |
| S015 | https://bitheap.org/cram/ | 2026-10-19T21:43:51Z | LANG, LC_ALL, and LANGUAGE are set to C. TZ is set to GMT. | §Usage, environment resets, bitheap.org/cram fetched 2026-10-19 |
| S016 | https://raw.githubusercontent.com/rogpeppe/go-internal/master/testscript/doc.go | 2026-10-19T21:43:51Z | Each script runs in a fresh temporary work directory tree, available to scripts as $WORK. | testscript/doc.go:56, master |
| S017 | https://bats-core.readthedocs.io/en/stable/writing-tests.html | 2026-10-19T21:43:51Z | In focus mode, the exit code of successful runs will be overridden to 1 | §Special tags, Focusing on tests with bats:focus tag, stable docs |
| S018 | https://hypothesis.readthedocs.io/en/latest/reference/api.html | 2026-10-19T21:43:51Z | If the CI environment variable is set to any value, the ci profile is active by default | §Settings, Built-in profiles, latest docs fetched 2026-10-19 |
| S019 | https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf | 2026-10-19T21:43:52Z | using data from 30 in-depth interviews with experienced users of PBT at Jane Street | Abstract, ICSE 2024 PDF p.1, fetched 2026-10-19 |
| S020 | https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf | 2026-10-19T21:45:13Z | only 18.23% were fully automatable, while most required partial adaptation (30.05%) or were incompatible (51.72%) | Abstract, EMSE 2026 paper; authors' copy opened because the Springer DOI page served an anti-bot challenge |
| S021 | https://arxiv.org/abs/2510.09907 | 2026-10-19T21:43:51Z | 56\% were valid bugs and 32\% were valid bugs that we would report to maintainers | Abstract, arXiv:2510.09907v1 (submitted 2025-10-10) |
| S022 | https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | 2026-10-19T21:43:52Z | we apply it internally, to the sequence of random choices made during generation | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13) |
| S023 | https://github.com/DRMacIver/shrinkray | 2026-10-19T21:43:51Z | they're only accepted if your interestingness test still passes, so a bad model costs time but never correctness | README §LLM mode; page currentOid 5fe6ee135d732e4b7758b3dbe3d91428523018fb |
| S024 | https://www.fuzzingbook.org/html/Reducer.html | 2026-10-19T21:43:52Z | one first has to build a Runner whose outcome is FAIL if the precise error occurs | §Delta Debugging, fuzzingbook.org fetched 2026-10-19 |
| S025 | https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf | 2026-10-19T21:43:52Z | Most flaky tests (78%) are flaky the first time they are written | §Findings F.2, FSE 2014 PDF p.2, fetched 2026-10-19 |
| S026 | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | 2026-10-19T21:43:52Z | about 1.5% of all test runs reporting a "flaky" result | post body, published 2016-05-27, fetched 2026-10-19 |
| S027 | https://arxiv.org/abs/2602.19098 | 2026-10-19T21:43:51Z | We identified a total of 65 environmental flaky projects | Abstract, arXiv:2602.19098v1 (submitted 2026-02-22) |
| S028 | https://bazel.build/reference/test-encyclopedia | 2026-10-19T21:43:52Z | writing any of the strings PASS or FAIL to stdout has no significance to the test runner | §Role of the test runner, bazel.build fetched 2026-10-19 |
| S029 | https://github.com/lukasa1993/mutate4bash | 2026-10-19T21:43:52Z | Timeouts, invalid syntax, and compile errors return status 1; surviving mutants return status 2 | README; page currentOid 01cb2d872edadc72c3ff9a7bd8405fe099b49953 |
| S030 | https://arxiv.org/abs/2507.10062 | 2026-10-19T21:43:52Z | This paper introduces LLMShot, a novel framework that leverages Vision-Language Models (VLMs) | Abstract, arXiv:2507.10062v2 (v1 2025-07-14, last revised 2025-07-24) |
| S040 | https://o-parry.github.io/papers/2021a.pdf | 2026-10-19T21:47:33Z | Tests that fail inconsistently, without changes to the code under test, are described as flaky. | Abstract, p. 17:1 (author copy of TOSEM 2021) |
| S041 | https://pitest.org/quickstart/incremental_analysis/ | 2026-10-19T21:47:33Z | With the exception of 4), all these optimisations introduce a degree of potential error into the analysis. | Incremental analysis, paragraph after the optimisation list |
| S042 | https://arxiv.org/abs/2103.07189 | 2026-10-19T21:47:33Z | our analyses further provide evidence that mutants are indeed coupled with real faults. | Abstract |
| S043 | https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf | 2026-10-19T21:47:33Z | The results show a statistically significant correlation between mutant detection and real fault detection, independently of code coverage. | Abstract |
| S044 | https://arxiv.org/pdf/2404.09952 | 2026-10-19T21:47:33Z | We find LLMorpheus to be capable of producing mutants that resemble existing bugs that cannot be produced by StrykerJS | Abstract, p. 1 (arXiv v2) |
| S045 | https://blog.nelhage.com/post/two-kinds-of-testing/ | 2026-10-19T21:47:33Z | This change didn't break anything that was previously known to work. | section Novelty |
| S046 | https://github.com/ngernest/pbt-bibliography | 2026-10-19T21:47:33Z | This bibliography aims to cover the literature on property-based testing (PBT) à la Haskell QuickCheck. | README opening paragraph |

## Errata — kaika continuation (append-only)

- **ER-K1 — Gate rejected-4 vs criteria 6–10.** `## Gate` above rejected
  "a new QUALITY criterion without a lesson behind it" and said QUALITY
  was unchanged by that lesson. Both stand for that lesson. This round
  appends criteria 6–10, each citing a `## Mistakes` row (MK-2…MK-7) —
  the lesson the earlier rejection said was missing. Not a reversal;
  flagged by the Reviewer seat as an unreconciled contradiction.
- **ER-K2 — `SKILL.md` pointers.** `SKILL.md:462` cites `PROVINCE.md:16-17`;
  the generality rule is at `PROVINCE.md:15-16`. `SKILL.md:1469`'s
  `../PROTOCOL.md` resolves from the lane's main checkout, not from a
  `.tower` worktree. Recorded, not repaired: `SKILL.md` stays byte-stable
  this round (box 3 binding).
- **ER-K3 — box 4 evidence.** The Reviewer seat found box 4's "PROVINCE.md
  still accurate" overreached: the "Owns" list omits the tsukuroi and
  mado gates the lane measured in rounds 5–6. Corrected by an appended
  `PROVINCE.md` section (Core / Frontier / Adjacent), lines 1-20
  unchanged; box 4 stays `[~]`.
- **ER-K4 — provider exhaustion.** Three L2 seats (cold-read, score
  semantics, witness) died on a provider rate limit
  (`resource_exhausted`); a second cold-read on a reassigned executor
  route failed at capacity. Re-dispatched as fresh seats, with scratch
  dirs of dead seats declared off-limits; the cold-read ran on the
  `labrat` role route. No dead seat's output is used.

### Gate addendum — own/gate rows S031–S037 (contract rule 1)

The Critic seat (phase 2) found the seven own/gate rows admitted with no
Gate quote, contrary to contract v1 rule 1. Fetch records, opened
2026-10-19 by `git show <commit>:<path>` (sibling object stores,
read-only); blob sha256 prefixes re-derived in the same command:

| id | source @ commit | accessed | quote (≤25 words) | location |
|---|---|---|---|---|
| S031 | `tools/mutate-and-run.sh` @ `4eb4cf3` | 2026-10-19 | "the fleet's recorded mutation cases, replayed as legs. Each leg carries its recorded revision pin" | `tools/mutate-and-run.sh:80-81` |
| S032 | `kumitate-shokunin/scripts/kimi-census.mjs` @ `175de6ba` (`83016d45…`) | 2026-10-19 | "kimi-census.mjs — the Kimi Code CLI substrate census gate (contract `kumitate-kimi-census-v1`)." | blob lines 3-4 |
| S033 | `kagi-shokunin/corpus/surface-census.sh` @ `fecee874` (`275d8294…`) | 2026-10-19 | "Nothing detected a surface disappearing, changing kind/mode" | blob lines 4-5 |
| S034 | `tsukuroi-shokunin/tools/tsukuroi-census.sh` @ `165307fe` (`084951be…`) | 2026-10-19 | "Answers exactly one question, read-only" | blob line 7 |
| S035 | `mado-shokunin/tools/mado-verify.sh` @ `eead56b2` (`d7edaab4…`) | 2026-10-19 | "mado-verify.sh — mado-shokunin config-plane verdict gate (v1, round 5 / M5-2)" | blob line 3 |
| S036 | `kagi-shokunin/corpus/checklist-run.sh` @ `fecee874` (`7e5ec98b…`) | 2026-10-19 | "This gate binds every item to exactly one row of" (then `corpus/checklist.tsv`, line 9) | blob lines 6-7 |
| S037 | `kumitate-shokunin/scripts/claims-check.mjs` @ `175de6ba` (`e9a21b44…`) | 2026-10-19 | "claims-check.mjs — the member-claims gate (contract `kumitate-claims-v1`)." | blob line 3 |

### Errata — kaika continuation, phase-2 findings (append-only)

- **ER-K5 — `SKILL.md` status sentences now stale.** `SKILL.md:14-15`
  ("current full-sweep/bash sufficiency remains unverified") and
  `:133-135` say what this round's cold-read
  (`../../reports/round-1-kaika-coldread.md`) has since measured for
  Appendix A + B. Marked here and in `corpus/README.md` `## Known gaps`;
  not edited this round, so box 3 stays bound to the executed bytes
  (`git show 4eb4cf3:SKILL.md | sha256sum` → `33e3009c…0f81`). Owner:
  the round that next edits `SKILL.md`, which must re-run the cold-read.
- **ER-K6 — K2 census wording.** `SCORECARD.md`, `LOG.md` and the
  capability row say "contract census clean": true for contract v1's
  census, but the Critic and Reviewer seats read the run's extra H4
  block (id-cite, fleet critic H4, not contract v1) as part of it — it
  printed 25 `no-id-cite` links, all own/gate rows S031–S037 whose
  used-by entries predate the registry and cite the source by path.
  Census v2 (`../../.ufo/evidence/kaika-round-1/sources-census-v2.sh`)
  separates contract checks from H4, reports strict id-cite as
  informational (25), gates on id-or-path (0 violations), exits non-zero
  on any gated violation, and was mutation-tested (a mined row pointed at
  a file citing neither → `SOURCES_CENSUS: VIOLATIONS`). Also missing
  at landing: the Gate quotes for S031–S037 (addendum above).
- **ER-K7 — box 3 line breadth.** The Reviewer seat found the box-3
  evidence line broader than the run: the sweep used
  `tools/mutate-and-run.sh` plus the seat's own uniqueness checker, not
  the appendices' python driver; Appendix B's survivor-probe fixtures
  were reconstructed from the gate's input contract; the
  no-permissiveness audit recipe (`SKILL.md:466-495`) and the
  fail-closed taxonomy (`:497-525`) were not exercised. The line now
  says so. Whether `[~]` holds at that scope is for the non-author
  verifier; the Critic seat's view is "candidate, scope-incomplete".
- **ER-K8 — S038–S039 unused.** Reserved for own-work rows; never
  written; the merge-assigned rows start at S040 by plan. Never reused.

### Non-author adjudication and post-review fixes (orchestrator, 2026-10-19)

Outside verdict on this round (orchestrator; not a lane seat):
reviewer — admit with conditions; critic — **K2 admit**, **K1 reject
as measured**: the cold-read covered only Appendix A + B with
reconstructed Appendix B probes, so the box-3 increment is not earned.
Recorded as a disagreement with the lane's Gate admit of the box-3
move (`## Gate — kaika continuation`); the lesson it teaches is
already criterion-shaped by ER-K7 — a mark's evidence covers the
mark's whole wording or the mark does not score. Fixes, append-only:
`SCORECARD.md` post-review corrections (calibration pinned 6 without
box 3; measured-commit cells → `121696b`; K2 pointer → census v2);
`corpus/README.md` F1/F2 `held` → `partly held`; `corpus/SOURCES.md`
`## Id allocation` (S038–S039 retired, never reused); quality trend
`unchanged`, not `improved`. No `SOURCES.md` row cell changed (no
status/recheck/used-by edit, so no old→new entries owed). No new
claims.
