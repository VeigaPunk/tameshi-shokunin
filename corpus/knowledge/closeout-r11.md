# The arc's closeout — the service as it stands (T11-1, round 11)

Written 2026-10-14 by lane T11-1 (tameshi round 11 — the final round, training
r10; `plans/round-11.plan.md:13-25`). Role: the corpus-side closeout of the
ten-round arc **as it stands** — the service (the tool, the six-leg ledger, the
opt-in protocol, the limits, the cadence schedule for the standing future),
the line the lane hands across (fleet-visible) versus what stays lane-owned,
and the named carried debts. This note adds no gate measurement of its own
beyond §5's boundary readings; every claim restates a landed source and
carries its anchor. It re-cuts no rate, edits no sibling record, and claims no
promotion or retirement — the arc ends, the service remains
(`plans/round-11.plan.md:20-25`).

Anchors: **O** observation · **I** inference · **U** unknown. Write scope:
this file only; scratch `/tmp/w11-t11-1/`. Substrates read-only during this
write; secrets shape-only; no external sites. Line cites are this write's
revision of each file (§6 pins, measured 2026-10-14T21:35Z). Round-11's own
writes are in flight and partly uncommitted; where this note and a landed
round-11 byte disagree, the landed byte governs, and a reader on a differing
revision re-resolves rather than trusts.

## 0. Frame — the arc, and what this file is

- **The arithmetic.** Commit subjects label rounds 4–10 `(training r3)` …
  `(training r9)` (`LOG.md:303-309`); round N = training r(N−1), so the
  ten-round arc is **rounds 2–11 = training r1–r10** and round 11 is its last
  [I]. The round-10 plan's "no round 11 is planned by this arc" prose is
  superseded by the round-11 dispatch — recorded, not smoothed
  (`plans/round-11.plan.md:16-24`).
- **What this file is not.** Not the tick's receipt and not the round record:
  the round-11 execution (the pre-announced tick, the schedule, the 10-of-10
  record) lands in the round's own documents; `plans/completion-evidence.md`
  (this wave, in flight) is the parent's audit input; `SKILL.md`'s round-11
  section (heading "Final pointers — the standing map at the arc's close")
  is the method page's map. This note is the corpus-side closeout: what a
  reader inherits, with the debts named and anchored.
- **In flight at this write [O].** `SKILL.md` +99 L (the round-11 section,
  uncommitted); `plans/completion-evidence.md` (new, uncommitted); the
  round-11 record to land; no round-11 commit yet — HEAD `606716f`
  ("probation round 10 (training r9)").

## 1. The ten rounds, restated (no cell re-adjudicated)

| Round | Axis | The move, one line | Anchor |
|---|---|---|---|
| 2 (r1) | depth + calibration | first measured kill-rate: kimi-census 43-case suite vs 10 mutants → 8/10 (80 %); wave-1 errata append-only; fleet 4th pattern | `SCORECARD.md:13-14`; `LOG.md:68` |
| 3 (r2) | depth + operability | second kill-rate, first bash gate (surface-census 8/10, 80 %); first tool (selftest 24/24); SKILL 244→665 L; no-oral-context executor test | `SCORECARD.md:15-16`; `LOG.md:173` |
| 4 (r3) | calibration | arm-class matrix + `--regression` mode + round-gate §13 projection (projection, not measurement) | `SCORECARD.md:17`; `LOG.md:303` |
| 5 (r4) | depth | third kill-rate, cross-author (tsukuroi 6/10, 60 %); incident I1 recorded; six-gate suite/arm census | `SCORECARD.md:18`; `LOG.md:304` |
| 6 (r5) | adjacency + operability | first service engagement (mado 4/10, 40 %): in-surface 4/4 vs out-of-surface 0/6; own-tool meta-hardening | `SCORECARD.md:19`; `LOG.md:305` |
| 7 (r6) | operability | the leg ledger: 4 cases replayed at pinned git blobs; standing ledger + opt-in protocol land | `SCORECARD.md:20`; `LOG.md:306` |
| 8 (r7) | coverage | cases 5+6 (47 %, 70 %) → six gates measured; cadence policy + first pin read | `SCORECARD.md:21`; `LOG.md:307` |
| 9 (r8) | operability | first scheduled tick (4 current · 2 stale · 0 drift); the limits note | `SCORECARD.md:22`; `LOG.md:308` |
| 10 (r9) | operability | the operator runbook; the leg cut resolved (six legs); the boundary note | `SCORECARD.md:23`; `LOG.md:309` |
| 11 (r10) | operability, terminal | the close: the pre-announced tick fired; the schedule + the 10-of-10 record — **in flight at this write**; no landed verdict cells here (`—`, never manufactured) | `plans/round-11.plan.md`; the round record, to land |

Full move-log rows with their counting commands: `SCORECARD.md:11-23`; full
round entries: `LOG.md`. Commit map `2 → 2587e0a … 10 → 606716f`: the round
record drafts and the completion pack's appendix.

## 2. The service as it stands

### 2.1 The tool — `tools/mutate-and-run.sh`

`75ed934dc86360f5…` (r10-2, 1 642 L; committed at `606716f`), version string
`mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)`.

- **What it does.** Per defect: "if this one exact edit were present in the
  target, would the gate's hermetic suite go red?" — KILLED / SURVIVED /
  INCONCLUSIVE per defect, one kill-rate headline (`:22-27`); the target is
  never a write target (`MUTATE_RESTORE: OK`, sha256 before = after).
- **Four invocations** (`:150-192`): `--target/--defects/--suite …` ·
  `--regression [--workdir] [--keep]` · `--selftest` · `--help`. The suite
  runs as `bash -c CMD` with `$MUTANT`; exit 0 green, non-zero red,
  124/126/127 inconclusive (`:43-51`). Defect spec v1 is fail-closed: every
  `@old` unique and `@new != @old`, asserted **before any suite run**; any
  spec failure or a red control = `MUTATE: SETUP`, exit 2 (`:29-41`,
  `:53-59`). Exit map 0/1/2/64 (`:69-70`).
- **The six embedded legs.** The fleet's recorded cases replayed as legs,
  each **materialized from its repo's git object store** at its recorded
  revision (`git show <rev>:<path>` — a drifted tree cannot move a replay; a
  pin mismatch is a SETUP refusal; `100755` blobs are `chmod +x`'d, the
  exec-bit mirror): `js-kimi-census` 8/10 · `bash-surface-census` 8/10 ·
  `bash-tsukuroi-census` 6/10 · `bash-mado-verify` 4/10 · `bash-checklist-run`
  7/15 · `js-claims-check` 7/10 (`:85-97`, `:522-559`).
- **Selftest.** Hermetic, 80/80 at this revision [O, §5 SC1]; the refusal
  arms are selftested, not conventions (duplicate `@old`, no-op edit, unknown
  escape, drifted working tree does not move a git-pinned leg, regression
  refusals).
- **Receipt discipline.** Every run log carries its own `MUTATE_TOOL` /
  `REGRESSION_TOOL` sha — "cite the pin that ran"; a mid-round tool move is an
  incident recorded, not smoothed; `SETUP` is not a verdict.

### 2.2 The six-leg ledger — `fleet-kill-rate-ledger.md`

`2f25c51e3e0a7851…` (363 L). One row per measured gate, so a kill-rate claim
cites one standing receipt (`:1-8`). Built append-only: §1 four rows, ER-1
(concurrent drift), ER-2 (cases 5/6 measured; the six-gate view), ER-3 (the
re-sweep cadence), ER-4 + addendum (the first scheduled tick) — §1–§4 never
edited (`:312`; `corpus/QUALITY.md:7`).

| # | case (owner · file) | suite | rate · composition | pin |
|---|---|---|---|---|
| 1 | kumitate · `scripts/kimi-census.mjs` | 43 | 8/10 = 80 % · 10 kill-aimed | `83016d45…` |
| 2 | kagi · `corpus/surface-census.sh` | 16 | 8/10 = 80 % · 10 kill-aimed | `275d8294…` |
| 3 | tsukuroi · `tools/tsukuroi-census.sh` | 26 | 6/10 = 60 % · 6 kill + 4 hole | `084951be…` |
| 4 | mado · `tools/mado-verify.sh` | 28 | 4/10 = 40 % · 4 in + 6 out | `d7edaab4…` |
| 5 | kagi · `corpus/checklist-run.sh` | 34 | 7/15 = 47 % · 7 kill + 8 hole | `7e5ec98b…` |
| 6 | kumitate · `scripts/claims-check.mjs` | 39 | 7/10 = 70 % · 6 kill + 4 hole | `e9a21b44…` |

- **Readings the ledger is built to keep.** A rate is **composition-bound**
  (mado's 40 % is 4/4 in-surface + 0/6 out-of-surface — a co-extensive suite,
  read as composition, not regression); a post-hardening re-run of the same
  spec is a **directed repair**, not an independent rate (`:35-36`); survivors
  are measured and classed — (a) reported-but-unasserted surface, (b) unreached
  fixture/arm, (c) one-directional assert, (d) out-of-band exit map
  (`:143-150`); the not-claimed list stands — cross-host, coordinated
  multi-edit rewrites, gate truth, live-substrate drift (`:154-158`).
- **Known carried text.** §1's embedding line still reads "cases 1 and 2
  only" (`:85-88`) — superseded by ER-2 (`:281`, four legs) and by r10-2 (six
  legs); a ledger row recording the six-leg registry is the ledger owner's
  follow-on (the sliver of §4.2).

### 2.3 The opt-in protocol — `service-optin-protocol.md`

`84d0c1547eed257d…` (286 L). What an opting-in lane brings — a pinned
revision (a moved substrate needs a re-pin, never a re-interpretation), a
one-command hermetic suite that exercises the copy and reads no live path, a
clause-mapped single-edit spec with pre-registered expectations, nothing else
(`:54-77`) — and what comes back: the kill-rate table, survivor
non-equivalence probes, the restore proof, recommendations as a corpus note;
**the note is the only fleet file the run writes**; absorption stays
owner-side (`:109-218`). Three engagement forms: self-service (tsukuroi r5),
service (mado r6), **attestation — planned, not yet executed** (`:32-38`;
U1). Owner-hardens discipline: rules 1–6 (`:142-180`), including "no
acceptance means recorded unabsorbed — a complete outcome" and "harden the
boundary classes, not just the survivors". Adjudication kept fleet-wide:
killed = suite red **and** the count still enumerated; inconclusive excluded
from the rate and named beside it; `kill-rate = killed/(killed+survived)`;
bands are a report convention (`:199-204`).

### 2.4 The limits — `service-limits.md`

`a57a1e69be02896a…` (276 L, round 9). Ten refusal rows (a–j), one verbatim
anchor per row (`:42-55`): no opt-in/no pin · no hermetic suite/no runnable
spec · a moved substrate held to the old table · live substrates/sessions
(incl. handler-gated cases) · secrets-adjacent code · product semantics ·
coordinated multi-edit rewrites · the exit-flatten family ·
directed-repair-as-rate · foreign scratch. The intake precondition was
checked at round 9 and found **present**: the re-pin rule lives in the
protocol's request shape (`service-optin-protocol.md:59-62`), not as a
separate clause (`service-limits.md:172-194`). The refusals are stated, not
adjudicated — out of province → report, never absorb.

### 2.5 The cadence schedule — for the standing future

The tick is a **pin read executed at a boundary**, plus the instrument's own
pulse; no daemon, no timer, no cron (`SKILL.md:1010-1019`).

**The command set** (from the repo root; captured in a lane-scoped scratch):

```
bash tools/mutate-and-run.sh --selftest
bash tools/mutate-and-run.sh --regression --workdir /tmp/<scratch>/regression
# per case:
sha256sum <gate-file>                                  # live vs the recorded pin
git -C <repo> show HEAD:<path> | sha256sum             # is the recorded revision the HEAD blob?
git -C <repo> status --porcelain -- <path>             # worktree vs HEAD
git -C <repo> merge-base --is-ancestor <rev> HEAD      # moved past the recorded revision?
```

**Fire classes — what puts the tick on the calendar:**

| Fires on | Who fires it | Where the receipt lands |
|---|---|---|
| a round boundary | the seat the handoff names (the operator when no lane is live) | ledger append / the round record |
| any opt-in request | the seat the handoff names | the protocol's report shape (`:182-197`) |
| an owner-committed gate move (T1/T3) | the gate's owner, with its own record | an appended ledger row at the measured revision |
| a re-pin (T2: the tool moved) | the seat that notices; the tool owner records | both pins recorded, appended |

**Readings it produces:** per case `current` / `stale` / `drift`; tool
`held` / `moved` (`SKILL.md:1031-1036`). **Triggers:** T1 stale → re-measure
at the live revision, or record the STALE cell with its reason — never edit
the recorded table · T2 harness moved → re-run under the new revision, record
both pins · T3 owner re-run at a new revision → appended row. **The re-pin
rule:** a moved pin is never re-interpreted against the new bytes; both
revisions stay in the record; `moved=0 stale=0` is a complete outcome
(`SKILL.md:1069-1090`).

**The tick series, as kept — each row carrying its own receipt:**

| tick | boundary | executed | pin read | tool | receipt |
|---|---|---|---|---|---|
| 1 | r8 (demonstrated) | 19:15:14Z | — | `cf41efaa…` | `SKILL.md:1038`; `/tmp/w8-tameshi-t84/pin-read.txt` |
| 2 | r9 (first scheduled) | 20:00:34Z | 4 current · 2 stale · 0 drift | `cf41efaa…` | `SKILL.md:1166`; ledger ER-4 `:318-353` |
| 3 | r10 | 20:52:19Z | 4 current · 2 stale · 0 drift | `cf41efaa…` | runbook §6/§9; round-10 record |
| 4 | r11 (pre-announced) | 21:32:35Z (T11-4) · 21:35:54Z (this lane) | 4 current · 2 stale · 0 drift | `75ed934d…` **held** | SKILL round-11 section; the round record |

Pre-announcement: `plans/round-11.plan.md` (committed at `606716f`, before
the wave existed) names the boundary tick's exact set; the announced-vs-fired
pair is the round's receipt (`:62-79`).

**Gap series [O, computed from the receipts' timestamps]:** 45 m 20 s
(19:15:14Z → 20:00:34Z) · 51 m 45 s (20:00:34Z → 20:52:19Z) · 40 m 16 s
(20:52:19Z → 21:32:35Z). The ticks fired minutes apart because they are
**boundary-bound, not clock-bound**. **The interval is `[U]` — set and kept
by the seat the handoff names**; no lane declares a clock interval
(`plans/round-11.plan.md:96-103`).

**What the schedule is not:** no daemon, no timer, no promise that tick 5
fires; the refusals stay at their anchored homes; whether any fleet driver
invokes the tick with no lane acting stays `[U]` (`SKILL.md:1017-1019`).

### 2.6 The boundary — fleet-visible vs lane-owned

Detail of record: `service-standing-state.md` (`d326c1a4d61c9705…`, 242 L) —
11 fleet-visible artifact classes, 7 lane-owned classes, 16 handoff
conditions grouped by the line they cross (`:49-155`). Two facts that ride
it: visibility is **by citation, not by index** — no fleet-root document
indexes these artifacts; measured cross-repo mentions tsukuroi 12 files ·
mado 19 · kumitate 0 · kagi 0 (`:34-47`) — and the **coverage map lags**:
9 rows covering 6 of 16 knowledge notes (`corpus/README.md`, 20 L; `:60-66`).

## 3. What the lane hands across, and what stays lane-owned

- **Handed (fleet-visible, citable, re-derivable):** the instrument (never
  writes a target; pinned per run); the standing receipt (the ledger); the
  contract (the protocol); the refusals (the limits); the method page
  (`SKILL.md`) — whose round-11 section is the arc's standing map; the
  operator's entry point (`operator-runbook.md`); the six case notes; the
  census and surveys; the boundary rules (`PROVINCE.md`, `AGENTS.md`); the
  coverage map; `LOG.md` / `SCORECARD.md`; the round plans and reports.
- **Not handed (lane-owned):** round scratch and run evidence (lane-scoped;
  foreign scratch never removed); the default run/regression scratch's own
  removal rules; in-flight / working-tree state (`drift` is a reading — a
  writer waits for the commit, then the pin re-reads); **the substrates
  themselves** — the service never edits, repairs or re-pins a gate
  (recommendations only); the live plane (PATH-level stubs only, never a
  session); secrets and session material (shape-only, never content-read);
  drafts (landed bytes are the authority once committed).
- **The handoff is conditions, not a file move.** A gate crosses in on pin +
  hermetic suite + clause-mapped spec, with the note the only fleet file
  written; a result crosses out on the report shape (kills verbatim from
  `evidence/<id>.out`, probes, restore proof, recommendation + unknowns) and
  enters the standing record **appended** — never as an edit of §1–§4 — with
  receipts read as blocks, not last lines; what never crosses: the refusals,
  the schedule's interval, the dispatch hand-off [U]
  (`service-standing-state.md:80-155`).

## 4. The named carried debts

### 4.1 The 9 un-exercised clause sites pattern — owner: tsukuroi (ledger case 3)

- **The debt, as the owner named it.** `tsukuroi-shokunin/corpus/knowledge/
  memory-arm-ver-s8.md:177-181` (VER-S8, D2): "consolidated coverage debt:
  **9 clause sites un-exercised by the 49-case suite**" — S8-1's
  D9/D10/D11, the verifier's M04/M06/M10/M12/M15, and M17. Tsukuroi's method
  page is explicit: "The shipped suite is **not** to be described as
  clause-complete" (`tsukuroi-shokunin/SKILL.md:1059-1063`); the round-10
  calibration synthesis restates it in the calibration record
  (`calibration-synthesis.md:230-231`, `:319-323`).
- **Why it rides this closeout.** That gate is **case 3** of the six-leg
  ledger (sweep pin `084951be…`, 26-case suite, 6/10 = 60 %; survivors
  B7/B8/B9/B10; the owner's hardening 26 → 35 closed B10; the replay left
  B7/B8/B9 open — "tameshi's B7/B8/B9 have **no landed closure** through
  round 9", `calibration-synthesis.md:321-323`). The owner's gate has since
  moved and grown — case-count history **17 → 26 → 35 → 49 → 63 → 74**
  (`:311-312`); at this read it is live `10452443…` @ `af8adf1` (2 402 L;
  §5 SC2) — and its own records carry the clause debt forward, not closed.
- **The pattern (the method lesson, [I]).** A rate — even a directed-repair
  100 % — does **not** imply clause-completeness: un-exercised clause sites
  are invisible to any kill-rate, because a rate is bounded by its defect
  vocabulary. This is the same family as tameshi's measured survivor classes
  — (b) unreached fixture/arm, (a) reported-but-unasserted — at the owner's
  suite level; and it is the arc's strongest cross-author evidence: "a
  different author's mutants found clause gaps the owner's own 100 %
  re-sweep could not see" (`:319-320`). The owner's own framing is the honest
  one — "coverage debt, not silent gaps": every site is detectable by a case
  built from the arm's own vocabulary (`memory-arm-ver-s8.md:177-181`), so
  the repair is named work, not open semantics.
- **What the close hands forward.** Any re-sweep of case 3 is a **fresh spec
  at the revision it measures** (T1/T3; the re-pin rule); the successor row
  lands appended in the ledger; nothing here absorbs or re-cuts the owner's
  debt — sibling gates stay sibling-owned (`PROVINCE.md:14-20`). [U] whether
  the debt was closed at tsukuroi's live revision: this lane did not sweep it
  (read-only), and tsukuroi's own round-11 is in flight.

### 4.2 The 4-vs-6 → 6-leg resolution receipt — owner: the tameshi tool owner

- **The debt it resolved.** Round 8 (r7) embedded four legs; cases 5/6
  (checklist-run, claims-check) carried no `REGRESSION` line — the round-8
  hand-offs (mutation-case-kagi-checklist.md U5;
  mutation-case-kumitate-claims.md E3), the round-9 record's "cases 5/6
  remain unembedded — named debt", and the ledger's own follow-up note
  (`fleet-kill-rate-ledger.md:282`).
- **The resolution (round 10 = r9, T10-2 r10-2): an embedding, never a
  re-cut.** `cf41efaa…` (1 341 L) → `75ed934dc86360f5…` (1 642 L,
  `+361/−60`): cases 5/6 embedded as legs 5/6; `REGRESSION_EXPECT` lists six
  recorded rates. The checklist leg's control first read **SETUP** (every
  case exit 126 — the materialized blob lacked the exec bit) and was fixed
  by **mirroring the blob mode** (`100755` → `chmod +x`, selftest arms
  added) (`plans/round-10-record-draft.md:78-92`).
- **The receipt — four independent lanes, one revision:**
  `PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)` at
  `75ed934d…`, with `--selftest` 80/80 — T10-2 21:00:24Z · AUD-T10 21:01:53Z ·
  T10-4 21:02:39Z · VER-T10 21:05:10Z; the audit's own leg-check
  `LEGCHECK: PASS (6/6 legs clean)` (`reports/r10-aud-t10.md:101-113`,
  `:175-178`). Round-11 re-verified at the same revision: the round's own
  `--regression` receipt 21:32:40Z (`cases=6 passed=6`) and this lane's
  selftest 80/80 (§5 SC1).
- **The carried sliver (open at this write).** The ledger's §1 embedding text
  still reads "cases 1 and 2 only" (`fleet-kill-rate-ledger.md:85-88`) and no
  ledger row records the six-leg registry — an append-only follow-on named
  to the ledger owner (`SKILL.md` round-10 section;
  `plans/round-11.plan.md:126-129`). And the runbook's §2/§3/§7 four-leg
  lines stay stale at the landed revision (AUD-T10 finding row 7; ER-R3
  open) — the anchored source governs; cite the pin that ran
  (`operator-runbook.md:173-175`).

### 4.3 The rest of the debt ledger (carried, each with its anchor)

- **Two `stale` successor rows.** Case 3 `084951be…` → live `10452443…`
  (HEAD `af8adf1`); case 4 `d7edaab4…` → live `93e43f8f…` (HEAD `f7bfc9f`).
  Both are their repos' committed HEAD blobs, trees clean, **0 drift** at
  this read (§5 SC2). No appended rows yet — the ledger is byte-identical
  `2f25c51e…`.
- **Ledger gaps.** The six-leg registry row; the census §5 instrument re-pin
  errata (`fleet-suite-census.md`; ER-2 named it).
- **Coverage map** (`corpus/README.md`, 20 L): rows for the round-6–11
  notes, the r9/r10 reports, the runbook (new path), the standing-state
  note.
- **The runbook's fresh-executor sufficiency table.** VER-T10 executed the
  loop but no `reports/r10-ver-t10.md` landed; NOT EXERCISED / partial is
  the honest state, and the runbook's stale lines above ride with it.
- **Unexecuted surfaces.** The attestation form (protocol U1); a
  fleet-contributed leg (the contribution contract, `SKILL.md:954-963`); a
  third-lane adoption (protocol U2); the dispatch hand-off (U3);
  cite-check's full sweep (probe-only, 1/4); the ten surveyed-but-unmeasured
  gates (the queue, `fleet-kill-rate-ledger.md:98-124`).
- **Unknown registers carried as written.** The ledger's U1–U9 (`:216-237`;
  U3 narrowed by ER-2 `:281`; U9 fired as ER-4), the protocol's U1–U6
  (`:259-274`), the limits' U1–U5 (`:218-239`), the cadence's driver `[U]`,
  the interval `[U]`, adoption `[U]`.
- **The arc's own unmeasured classes.** The 50 % crossover (both 80 % runs
  sit above it), coordinated multi-edit rewrites, cross-host readings —
  named, not claimed.

## 5. Spot-checks (three, executed at this write; scratch `/tmp/w11-t11-1/`)

- **SC1 — the instrument pulse.** `bash tools/mutate-and-run.sh --selftest` →
  `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0
  (`/tmp/w11-t11-1/selftest.log`); `sha256sum tools/mutate-and-run.sh` →
  `75ed934dc86360f5…`, 1 642 L (**held** — the r10-2 revision the round-10
  receipts ran under); `grep -c '^@defect'` → 72 (embedded leg specs +
  selftest fixture specs); the header lists all six legs (`:85-97`). [O]
- **SC2 — the six-case pin read (ER-3's command set).** 2026-10-14T21:35:54Z:
  **4 current · 2 stale · 0 drift**, all six paths porcelain-clean, every
  recorded revision ancestor-of-HEAD: kimi-census `83016d45…` current ·
  surface-census `275d8294…` current · **tsukuroi `084951be…` → `10452443…`
  stale** (HEAD `af8adf1`; moved again since round 10's read of
  `c396662e…`) · **mado `d7edaab4…` → `93e43f8f…` stale** (HEAD `f7bfc9f`) ·
  checklist-run `7e5ec98b…` current · claims-check `e9a21b44…` current
  (`/tmp/w11-t11-1/pin-read.txt`). [O]
- **SC3 — the debt anchors on the live bytes.** `sed -n '177,181p'`
  (tsukuroi, `memory-arm-ver-s8.md`) → the D2 "9 clause sites un-exercised by
  the 49-case suite" block; `sed -n '1059,1063p'` (tsukuroi `SKILL.md`) →
  "Coverage debt, named … not clause-complete"; `sed -n '78,92p'
  plans/round-10-record-draft.md` → the leg-cut resolution block (embedding;
  SETUP → exec-bit mirror; four-lane receipts); `sed -n '101,113p'
  reports/r10-aud-t10.md` → the six-leg `cases=6 passed=6` receipt;
  `sed -n '85,88p' corpus/knowledge/fleet-kill-rate-ledger.md` → the
  superseded "cases 1 and 2 only" text. [O]

## 6. Sources (pinned at this write; sha256 first-16 · lines)

| File | sha256 (16) | lines |
|---|---|---|
| `tools/mutate-and-run.sh` | `75ed934dc86360f5` | 1 642 |
| `SKILL.md` | `bfbdd2fd99c36aac` | 1 461 (round-11 section uncommitted; cite it by heading) |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | `2f25c51e3e0a7851` | 363 |
| `corpus/knowledge/service-optin-protocol.md` | `84d0c1547eed257d` | 286 |
| `corpus/knowledge/service-limits.md` | `a57a1e69be02896a` | 276 |
| `corpus/knowledge/service-standing-state.md` | `d326c1a4d61c9705` | 242 |
| `corpus/knowledge/operator-runbook.md` | `e1e349b69d798acb` | 511 |
| `corpus/README.md` | `1fe3050002f54b29` | 20 |
| `PROVINCE.md` / `AGENTS.md` | `f5e28bf144b0601c` / `cb9409e1c6fde1f1` | 20 / 6 |
| `LOG.md` / `SCORECARD.md` | `34258dc12675fc42` / `118c97cd5c6bdfcc` | 309 / 23 |
| `reports/r10-aud-t10.md` | `84837d2cca2e2962` | 228 |
| `plans/round-11.plan.md` | `068578f198367b79` | 300 |
| `plans/round-10-record-draft.md` | `8020f9bda4206469` | 469 |
| tsukuroi `memory-arm-ver-s8.md` / `calibration-synthesis.md` | `c5b42e28bbf42cb5` / `483d578ebac47999` | — |

[O] tameshi HEAD `606716f` at this write; round-11 writes are uncommitted or
in flight (`SKILL.md` +99 L round-11 section; `plans/completion-evidence.md`
new). Sibling HEADs: kumitate `175de6b` · kagi `fecee87` · tsukuroi `af8adf1`
· mado `f7bfc9f`. A concurrent round-11 lane may move files after this write;
every line cite above is tied to the pins in this table, and a reader on a
differing revision re-resolves.

## 7. Unknowns

- **[U] tsukuroi's clause debt at its live revision** (4.1) — unmeasured
  here (read-only probe); tsukuroi's own round-11 is in flight.
- **[U] the standing future itself:** the interval (the operator's, not the
  lanes'); whether the operator adopts the schedule/runbook; whether any
  fleet driver invokes the tick with no lane acting.
- **[U] the two `stale` successor rows** — open at this read (ledger
  byte-identical `2f25c51e…`); whether they land this round is the round's
  call.
- **[U] round-11's landing state:** the round record, the LOG/SCORECARD
  rows, the coverage rows — in flight; nothing here pre-claims them.
- **[U] the arc's unmeasured classes** — the 50 % crossover, coordinated
  multi-edit rewrites, cross-host readings — and all registers' unknowns
  (ledger U1–U9, protocol U1–U6, limits U1–U5), carried as written.
- Single host (`plazir27`), single date (2026-10-14): no cross-host reading
  for any cell here.

## 8. Errata (append-only)

(none yet — new entries go below this line, never edits above, per
`corpus/QUALITY.md:7`, item 4)