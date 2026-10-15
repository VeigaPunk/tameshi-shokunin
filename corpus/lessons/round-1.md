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

