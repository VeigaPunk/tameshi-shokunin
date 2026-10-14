# WWKD plan — tameshi round 11 (ufo-round-plan-v1)

Design lane: PREP-T11 (2026-10-14, round-10 32-lane wave; round-10 execution
**in flight and unlanded** at this freeze — the tree is clean at HEAD
`b8eb96e`, and the in-flight writes are visible only in the worktree and in
`/tmp/w10-*`, read 20:52–20:55Z). Design-time state frozen
**2026-10-14T20:55Z**; every count below is a design read by this lane,
re-measured at dispatch. Write scope: this file only (PREP-T11); scratch
`/tmp/w10-prept11-*`. Round-10 clauses are the **precondition set** — checked
at dispatch, never assumed (see *Also*); where this draft and the landed
round-10 bytes disagree, the landed bytes are the authority.

Case frame — **the final round**. tameshi round 11 is the tenth *training*
round (r10) and the arc has no successor. The arithmetic is landed, not
asserted: `LOG.md` rows read `round 4 (training r3)` … `round 9 (training r8)`
(`LOG.md:303-308`), so round N = training r(N−1); rounds 2–11 are r1–r10 [I],
and the dispatcher's frame for this wave ("round 10, the penultimate") names
r9's round the second-to-last. The round-10 plan's own "no round 11 is planned
by this arc" (`plans/round-10.plan.md:14-18`) is design-time prose inside a
plan, not a landed record; the dispatcher's round-11 dispatch supersedes it,
and the disagreement is recorded here, not smoothed. Nothing here claims the
lane retires or is promoted: the arc ends, the standing service remains, run
by whoever the handoff names — and its own founding definition of done is
already receipted (the four `SHONEN.md:5-34` boxes, each `[x]` with a named
verifier).

Case set at this read (re-measured at dispatch; a measured count that differs
from six is recorded as the state, never manufactured):

| # | case | recorded pin @ rev | live at this freeze | state |
|---|---|---|---|---|
| 1 | js-kimi-census (kumitate `scripts/kimi-census.mjs`) | `83016d45…` @ `175de6ba` | `83016d45…` = HEAD blob, clean, HEAD `175de6b` | **current** |
| 2 | bash-surface-census (kagi `corpus/surface-census.sh`) | `275d8294…` @ `fecee874` | `275d8294…` = HEAD blob, clean, HEAD `fecee87` | **current** |
| 3 | bash-tsukuroi-census (`tools/tsukuroi-census.sh`) | `084951be…` @ `165307fe` | **`c396662e…`** = HEAD blob, clean, HEAD `fac745b` | **stale** (2nd move: `084951be…` → `bba6cdf6…` → `c396662e…`) |
| 4 | bash-mado-verify (`tools/mado-verify.sh`) | `d7edaab4…` @ `eead56b2` | **`93e43f8f…`** = HEAD blob, clean, HEAD `de22dfd` | **stale** (`d7edaab4…` → `90d50cdd…` → `7da4ec50…` → `93e43f8f…`) |
| 5 | kagi-checklist-run (`corpus/checklist-run.sh`) | `7e5ec98b…` @ `fecee874` | `7e5ec98b…` = HEAD blob, clean, HEAD `fecee87` | **current** |
| 6 | kumitate-claims-check (`scripts/claims-check.mjs`) | `e9a21b44…` @ `175de6ba` | `e9a21b44…` = HEAD blob, clean, HEAD `175de6b` | **current** |

Read by this lane 20:52–20:53Z per case: `sha256sum <live>` vs the recorded
pin · `git show HEAD:<path> | sha256sum` · `git status --porcelain -- <path>`
· `git merge-base --is-ancestor <rev> HEAD` (all six ancestors: yes),
scratch `/tmp/w10-prept11-pinread/pinread.txt`. The two round-10 tick lanes'
independent reads (20:52:11Z, 20:52:19Z; `/tmp/w10-t10-3/pin-read.txt`,
`/tmp/w10-t10-1/pin-read.txt`) agree cell-for-cell: 4 × `current` · 2 ×
`stale` · 0 × `drift`, tool `held` at `cf41efaa…` — three readers, one state.
Both stale cells are their repos' committed HEAD blobs (no drift at this
read); each is a timestamped reading, re-run at the boundary.

Axis move: operability, terminal — **the close: the arc hands the operator a
cadence that has kept an appointment**. ONE move, three ordered legs. Round 8
made the cadence a policy and demonstrated a tick; round 9 fired the first
scheduled tick; round 10 hands the operator the runbook that runs it. What no
round has yet given the service is the thing that stops it from being, the
moment the lanes stop, what round 7 wrote in its own ledger — "a convention,
not a mechanism" (`fleet-kill-rate-ledger.md:235-237`, U9; the round-8
policy's own `[U]` survives at `SKILL.md:1017-1019`): **a firing announced
before it happened, kept when it happened**. The arc's last act is to
pre-announce the tick in a committed artifact, fire exactly that, and hand
over the schedule — its fire classes, its kept receipts, and the interval,
which is explicitly not the lanes' to set.

(1) Leg appointment — **the pre-announced tick**. This file is the
    announcement. Committed with round 10's close (precedents:
    `plans/round-9.plan.md` committed at `c611d5d`; `plans/round-10.plan.md`
    landed inside round 9's window, `plans/round-9-record-draft.md:173`), it
    names — before the round-11 wave exists — the boundary tick's exact
    command set (round 8's pin read, `SKILL.md:1021-1053`; the tool pulse
    `--selftest` + `--regression`, `:1212-1222`), the six-case frame, the
    trigger rules T1–T3 with the re-pin rule (`:1069-1090`), and where the
    receipt lands. At the round-11 boundary the tick lane executes **exactly
    the announced set**; the receipt is the *pair* — the announcement's
    committed bytes (its commit sha, quoted from `git log`/`git show`) and
    the executed tick (timestamp, six readings, tool rev, regression date) —
    with the delta stated. Deviations are recorded as the state (a moved pin,
    a moved tool), never re-interpreted. The announcement is itself
    falsifiable and aimed at the reader: if this file's commit lands *after*
    the round-11 tick fires, the firing is recorded as an **unannounced
    tick** — the pre-registration failed and is recorded as failed, not
    re-labelled.
(2) Leg schedule — **what the operator inherits**. The schedule lands with
    the operator's runbook at its landed location — read at dispatch; the
    in-flight landing at this freeze is `corpus/knowledge/operator-runbook.md`
    (`??` at 20:54:53Z), and round-10's plan's `HANDOFF.md`-at-root shape
    (`plans/round-10.plan.md:48-52`) is its design-time form, whose own clause
    moves the coverage row with a relocated artifact. One table, one row per
    fire class — *what fires it* (a round boundary · any opt-in request · any
    owner-committed gate move · any re-pin) · *who fires it* (the seat the
    handoff names; the operator when no lane is live) · *the command* (the
    tick, verbatim) · *where the receipt goes* (ledger append or append-only
    errata) · *the reading it produces* (`current|stale|drift`, tool
    `held|moved`) — plus the **tick series as kept, each row carrying its own
    receipt**: tick 1 (r8, demonstrated, `19:15:14Z`, `SKILL.md:1038`); tick 2
    (r9, first scheduled, `20:00:34Z`, `:1166`; ledger ER-4 `:318-353`); tick
    3 (r10, the closeout boundary, `20:52:19Z` [O] in flight,
    `/tmp/w10-t10-1/pin-read.txt`); tick 4 (r11, pre-announced — leg 1).
    **What this round does not declare: a clock interval.** The ticks above
    fired minutes apart because they are boundary-bound, not clock-bound;
    declaring a production interval would be a promise no lane can keep. The
    interval is the operator's, and the schedule says so: the interval cell
    reads **[U] — set and kept by the seat the handoff names**, handed the
    arc's gap series as its only measured input (three gaps, each with its
    two timestamps and their receipts). No daemon, no timer, no cron: the
    schedule is a table plus receipts.
(3) Leg close — **the 10-of-10 record, and the discharge**. The completeness
    table (the close's spine) restates the ten rounds' landed rows — round ·
    axis · the move in one line · the receipt anchor (`SCORECARD.md` move-log
    row, `LOG.md` line, or the round's record) — and re-adjudicates nothing: a
    cell with no landed verdict is rendered `—`, never manufactured. The
    discharge list closes what this round can, each with its receipt, and
    re-names the rest onto the schedule; nothing is closed by prose:
    - the two **re-sweep successor rows** round 9 left open — tsukuroi
      `084951be…` → `c396662e…`, mado `d7edaab4…` → `93e43f8f…` — appended to
      the ledger at the pinned live revisions (fresh `/tmp` copies, read-only
      targets, the recorded defect vocabulary, tool pinned per run; §1–§4
      byte-identical, `cmp`-proven); if round 10 landed its own rows, this
      round **re-derives and cites** them instead (no duplicate rows);
    - the **census §5 instrument re-pin errata** (`fleet-suite-census.md`;
      ER-2 named it; the recorded instrument pin is two revisions stale) —
      append-only;
    - the **coverage rows** (`corpus/README.md`, 20 L at this read): rounds
      6–11's notes, the round-8/9/10 reports, `service-limits.md`, the
      round-10 artifacts and the schedule's home — each row with its holds
      and sources;
    - **LOG.md + SCORECARD.md** rows per house rules (the round-11 entry; the
      round-11 move-log row);
    - **cases 5/6 embedding** in the harness's leg ledger — discharged only
      where their notes' own leg receipts meet the contribution contract
      (`SKILL.md:954-963`) and the round's scopes include the tool; otherwise
      re-named as append-only erratum, never assumed. The round-10 in-flight
      tool edit (` M tools/mutate-and-run.sh`, +75/−43 at 20:54:53Z) is read
      at dispatch: the tool revision at the boundary is the authority for
      every receipt this round signs (T2);
    - **the unknowns** (ledger U1–U9 as amended; protocol U1–U5; service
      limits §5 U1–U5; the round-10 notes' own) are re-named as the
      schedule's standing backlog: each is either a trigger the schedule
      watches or a `[U]` the schedule carries; the close claims none of them.

Design-time state (measured by this lane; freeze above; re-measure at
dispatch):
- tameshi HEAD `b8eb96e` ("probation round 9 (training r8)"), tree clean at
  20:52:54Z. Round-10 writes **in flight, unlanded** ([O], 20:54:53Z):
  ` M tools/mutate-and-run.sh` (+75/−43), `?? corpus/knowledge/operator-runbook.md`,
  `?? corpus/knowledge/service-standing-state.md` (T10-3, 16 401 B, mid-write).
  No `HANDOFF.md` at the root at either read — the runbook's landing location
  is round 10's to adjudicate.
- Artifact cells (this lane, 20:52–20:53Z): `SKILL.md` `ee09c3bd…` 1269 L /
  85 320 B · `fleet-kill-rate-ledger.md` `2f25c51e…` 363 L / 36 169 B ·
  `service-limits.md` `a57a1e69be…` 276 L · `service-optin-protocol.md`
  `84d0c154…` 286 L · `fleet-suite-census.md` `ec1c2d8d…` 674 L ·
  `corpus/README.md` `1fe30500…` 20 L · `LOG.md` `38bd067a…` 308 L ·
  `SCORECARD.md` `b81e582e…` 22 L · `plans/round-10.plan.md`
  `d130596ac8bc7e91` 254 L · `tools/mutate-and-run.sh` `cf41efaa…` 1341 L
  (the in-flight edit unlanded at this read).
- Instrument pulse, this lane (scratch `/tmp/w10-prept11-*`):
  `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0
  (`/tmp/w10-prept11-selftest/run.log`); `--regression` → four legs each
  `match=10/10 … flips=0` (killed 8/8/6/4), closing `REGRESSION: PASS
  (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`,
  `REGRESSION_DATE 2026-10-14T20:53:16Z`, tool `cf41efaa…`, rc 0
  (`/tmp/w10-prept11-regression/regression.log`, workdir kept).
- Sibling trees (this lane's reads): kumitate `175de6b`, kagi `fecee87`,
  tsukuroi `fac745b` ("probation round 9 (training r8)"), mado `de22dfd`
  (same) — HEADs; all four case paths porcelain-clean, both moved gates equal
  their HEADs' committed blobs.
- Round-10 lanes observable ([O], read-only): `/tmp/w10-t10-1` (tick 20:52:19Z;
  ledger scratch copy 36 287 B; regression `REGRESSION_DATE 20:51:32Z`;
  falsifier `surface-census-drifted.sh`; append drill on the copy),
  `/tmp/w10-t10-3` (peer pin read 20:52:11Z), `/tmp/w10-t10-4-ev` (poll),
  `/tmp/w10-tameshi-scr-t10` (scribe poll), `/tmp/w10-tameshi-t10-2` (pinned
  copies of cases 5/6), `/tmp/w10-scr-m10`, plus sibling-repo lanes. The
  round-10 wave is live while this file is written; no pin here is taken from
  a moving revision.
- Anchors relied on (round-9 landed bytes): ledger U9 `:235-237`, §5
  embedding status `:85-88`, ER-4 `:318` (+ addendum `:356`); `SKILL.md`
  service `:794`, contribution contract `:954-963`, selftested arms
  `:1002-1007`, cadence `:1010` (tick + pin read `:1021`, triggers `:1069`,
  six-case statement `:1092`), round-9 section `:1155` (tick `:1164`,
  receipt `:1212`, re-pin semantics `:1230`, limits `:1246`+ — cite the
  round-9 section **by heading**, `service-limits.md:271`); protocol request
  shape `:54-77`, re-pin rule `:59-63`, U1–U5 `:257-272`; census offer
  `:277-291`.

Candidate decision (the dispatch named two):
- (A) **what a completed training arc hands off** — **FOLDED as the close's
  completeness table + the handoff-item receipt check**, not deferred and not
  a second artifact. The synthesis already travels inside round 10's runbook
  spine (`plans/round-10.plan.md:48-71`); a standalone "arc report" would be
  a second artifact family re-quoting receipts that already stand — the
  ledger's own role is "one standing receipt instead of re-quoting"
  (`fleet-kill-rate-ledger.md:5-8`) — and it would have no reader the handoff
  does not have. Precedent for folding, not splitting:
  `plans/round-10.plan.md:158-166`.
- (B) **the standing service's cadence schedule** — **CHOSEN**. The gap is
  named by the records themselves: U9 (`:235-237`), the round-8 policy's own
  `[U]` (`SKILL.md:1017-1019`, "whether any fleet driver would ever invoke
  the command with no lane acting"), and round 9's tick, fired without a date
  announced in advance. It is measurable without a daemon (the
  announced-vs-fired pair; the tick series; the gap series), it is the last
  move a lane can make toward "a mechanism, not a convention", and it hands
  the operator the one page a service needs to outlive its lanes.
- Named, not chosen this round (anchors held): the retirement or promotion
  question (the arc ends, the lane does not; no repo term claims either);
  a second synthesis artifact (above); the interval declaration (leg 2 — the
  operator's, `[U]`); a fleet-level announcement of the close (fleet-root
  write — the dispatcher's call); cases 5/6 embedding (conditional, in the
  discharge list); the attestation leg (protocol U1); the fleet-contributed
  case (`SKILL.md:954-963`); cross-host readings, coordinated rewrites, the
  50 % crossover, sensitivity ≠ truth — unmeasured, carried, never claimed.

Claim: round 11 closes the arc by **making the service's cadence keep an
appointment** — the tick's next firing is announced in a committed artifact
before the round exists (leg 1), fired exactly as announced at the boundary,
and handed to the operator as a schedule whose fire classes, kept series and
receipts are measured and whose interval is explicitly theirs (leg 2), with
the arc's ten rows and every open debt receipted or re-named on it (leg 3).
The close's headline (proposed shape, landing adjudicates) is the
appointment's own pair — `CLOSE: 10/10 rounds; tick 4 pre-announced <sha> →
fired <ts> (delta <n>); schedule: <f> fire classes, 4 tick receipts, interval
[U]; handoff items <h>/<n> receipted; tool held|moved; debts: closed <c>,
re-named <r>` — a statement about a firing scheduled in advance and happened,
not about prose. The ten-round completeness table travels in the close
record; there is no second synthesis artifact. Nothing new is measured: the
arc's rows are restated with their receipts; the only new measurements are
the tick's own receipt, the re-sweep successor rows (which the re-pin rule
requires — new rows at new revisions, never a re-cut rate), and the gap
series. An appointment that reads "unannounced" (the plan committed late) is
a complete, recorded outcome, not a failure to hide.

Also: round-10 clauses are the precondition set — checked at dispatch, never
assumed:
- the **runbook landed** at whatever location round-10's own terms adjudicate
  (in-flight name at this freeze: `corpus/knowledge/operator-runbook.md`);
  if the runbook is unlanded at dispatch, the schedule lands where the
  round-10 record's terms put the operator's entry point, or the round
  records the wait — named debt, never assumed;
- the round-10 tick block (in the runbook and/or `SKILL.md`, plus the
  ledger's round-10 erratum — number read at dispatch) with its regression
  receipt at the tool's round-10 revision;
- `corpus/knowledge/service-standing-state.md` (T10-3, in flight) read as a
  landed artifact — its revision the authority;
- the fresh-executor table and its verdicts (a `NOT EXERCISED` sweep step is
  a complete outcome, `plans/round-10.plan.md:92-107`);
- the re-sweep rows (landed → re-derive and cite; unlanded → this round's
  discharge leg); the tool's landed revision and whether cases 5/6 are
  embedded (read at the boundary; a moved tool re-pins every receipt it
  signs); the coverage rows; the round-10 record's carried list read as the
  debt ledger; sibling trees clean;
- the round-10 plan's "no round 11" clause: superseded by the dispatch
  (above), recorded, not smoothed; its own clause carrying everything open
  into the handoff's *what is not here* section makes that section this
  round's debt ledger.

Anti-claim: no daemon, no timer, no cron, no promise that tick 5 fires — the
appointment covers the one firing a lane can guarantee, and the interval is
the operator's `[U]`; no new gate measurement beyond the successor rows the
re-pin rule requires, and no rate re-cut for a recorded revision; no
re-interpretation of a moved pin ("a moved pin is never re-interpreted; the
old table stays", `SKILL.md:1083-1086`); the completeness table re-states
landed rows and adds no verdict (a cell with no landed verdict is `—`); the
close claims no promotion, no retirement, no scalar score of the lane or the
arc (axes stay per-round, per-axis); no adoption claim — whether the operator
runs the schedule stays `[U]`, recorded as such; the schedule is a table plus
receipts, never an automation; refusals stay at their anchored homes
(`service-limits.md` is the detail of record; on drift the anchored source
governs); no artifact is edited outside its append-only rules (the ledger's
§1–§4 byte-identical, `cmp`-proven); sibling trees read-only, re-read
before/after; any executor lane reads no live session (PATH-level stubs only,
`service-optin-protocol.md:129-132`) and writes nothing outside its scratch;
hermetic scope; no external sites; secrets shape-only; one move. A close
claim that cannot be re-derived by its cited command is cut, not softened.

Measure: (1) the appointment pair — the committed announcement (this file's
sha + commit sha via `git log --format`, the announced conditions quoted from
the committed bytes) vs the executed tick (its log: six cells, tool sha,
regression date), delta stated, one table; (2) the schedule — section present
in the runbook with its append proof (`cmp` prefix or the landing's own
append-only proof), every fire-class row anchored, and one cell of each of
the four tick-series receipts re-derived by a non-author (raw logs, not
prose); (3) the discharge ledger — each listed debt with its receipt
(row / errata / commit) or its re-naming as a schedule row, nothing closed by
prose; (4) the closure pulse at the round's revision — tool `--selftest` +
`--regression` (`cases=N` as landed), six-case pin read, tool `held|moved`,
sibling trees clean before/after; (5) the 10-of-10 completeness table — ten
rows, every cell anchored to a landed row, none re-measured; (6) the
coverage/LOG/SCORECARD rows landed, including the runbook's own row (moved
with the artifact if relocated); (7) unknowns carried (ledger U1–U9 as
amended; protocol U1–U5; service-limits §5 U1–U5; the interval `[U]`; whether
the operator adopts — `[U]`); (8) every quoted count carries its command.

Seats (suggested): schedule+close author (the runbook's schedule section + the
completeness table — the round's largest writing lane); tick lane (executes
the announced set verbatim, its receipt the appointment's other half — a lane
that did not write the schedule preferred); re-sweep lane (the two successor
rows at their pinned live revisions, tool pinned per run); non-author verifier
(the appointment pair + the schedule anchors + the tick-series spot-checks,
one level below the notes — raw logs, mutant shas); scribe (coverage rows,
LOG/SCORECARD, the round-11 record draft, the carried-debt sweep to the
schedule); poll lane (round-10 idiom: 60 s samples, cap named).

Write scope: round-11 execution scopes assigned at dispatch; this lane's
scratch `/tmp/w10-prept11-*`; this file is the only write (PREP-T11).