# WWKD plan — tameshi round 10 (ufo-round-plan-v1)

Design lane: PREP-T10 (2026-10-14, round-9 32-lane wave; round-9 execution in
flight and **partially landed** at this freeze — the tree carries its writes:
` M SKILL.md`, ` M corpus/knowledge/fleet-kill-rate-ledger.md`,
`?? corpus/knowledge/service-limits.md`, `?? plans/round-9-record-draft.md`,
all read 20:04:22Z). Design-time state frozen **2026-10-14T20:04Z**; every
count below is a design read by this lane, re-measured at dispatch. Write
scope: this file only (PREP-T10); scratch `/tmp/w9-prept10-*`. Round-9
clauses are the **precondition set** — checked at dispatch, never assumed
(`plans/round-9.plan.md:167-172`); where this draft and the landed round-9
artifacts disagree, the landed bytes are the authority.

Case frame — **the final training round** (round 10; no round 11 is planned
by this arc, and nothing here claims the lane retires — the standing service
remains, run by whoever the handoff names; anything still open at this
round's close is carried by the handoff's own *what is not here* section, not
by a future plan). Case set at this read (re-measured at dispatch; a measured
count that differs from six is recorded as the state, never manufactured):

| # | case | recorded pin @ rev | live today | state |
|---|---|---|---|---|
| 1 | js-kimi-census (kumitate `scripts/kimi-census.mjs`) | `83016d45…` @ `175de6ba` | `83016d45…`, HEAD `175de6b`, clean | **current** |
| 2 | bash-surface-census (kagi `corpus/surface-census.sh`) | `275d8294…` @ `fecee874` | `275d8294…`, HEAD `fecee87`, clean | **current** |
| 3 | bash-tsukuroi-census (`tools/tsukuroi-census.sh`) | `084951be…` @ `165307fe` | **`bba6cdf6…`** 1472 L / 73 919 B, = HEAD blob `72b038d` | **stale** (ancestor verified; dirty again by 20:02:42Z, `5d16378d…` — re-read at dispatch) |
| 4 | bash-mado-verify (`tools/mado-verify.sh`) | `d7edaab4…` @ `eead56b2` | **`7da4ec50…`** 2 887 L / 131 612 B, = HEAD blob `12c8f08` | **stale** (ancestor verified; dirty again by 20:02:38Z, `5b6ace8e…` — re-read at dispatch) |
| 5 | kagi-checklist-run (`corpus/checklist-run.sh`) | `7e5ec98b…` @ `fecee874` | `7e5ec98b…`, HEAD `fecee87`, clean | **current** |
| 6 | kumitate-claims-check (`scripts/claims-check.mjs`) | `e9a21b44…` @ `175de6ba` | `e9a21b44…`, HEAD `175de6b`, clean | **current** |

Read by this lane at 20:00Z, per case: `sha256sum <live>` vs the recorded pin ·
`git show HEAD:<path> | sha256sum` · `git status --porcelain -- <path>` ·
`git merge-base --is-ancestor <rev> HEAD` (both stale rows: ancestor yes).
Tool `held` at `cf41efaa…`. The tick's own read (ER-4, 19:58Z; second raw
pass 20:00:29Z) is the same six cells; ER-4's addendum (`:356-359`) then
caught both moved gates worktree-dirty again minutes later — a moved cell is
a timestamped reading, re-run at the next boundary.

Axis move: operability, terminal — **the closeout: the ten rounds' product is
handed to the operator as one runbook**. ONE move, three ordered legs. The
operator is the one reader left when the lanes stop, and both records end at
that unnamed seat: the ledger's U9 ("who runs the update is the dispatcher's
call", `fleet-kill-rate-ledger.md:235-237`; ER-3: "[U] whether any fleet
driver would invoke the command unaided") and the opt-in protocol's U3 ("the
dispatch hand-off … with no tameshi lane live",
`service-optin-protocol.md:264-266`). This round names the seat and hands it
the receipt.

(1) Leg note: the handoff lands as **`HANDOFF.md`** at the repo root — the
    operator's entry point, sibling of `SKILL.md`/`PROVINCE.md` (a
    `corpus/knowledge/` placement would bury the one reader this artifact
    exists for; if the landing lane relocates it, the coverage row moves with
    it). One artifact, two readers:
    - the **ten-round synthesis** — what the fleet learned about verification
      — is its spine (§ *What stands*): the six measured gates and the
      composition-bound rate sequence 80 · 80 · 60 · 40 · 47 · 70
      (`fleet-kill-rate-ledger.md:134-137`, ER-2 `:279`); the survivor
      taxonomy with its measured instances — four classes plus the round-8
      mechanisms (CLI fail-open, output-capture loss, deny-list re-openable,
      assert-blind threshold, first JS unreached arm) (`SKILL.md:1092-1154`,
      the six-case statement; `:1010`); the two hardening precedents,
      directed repair ≠ an independent rate (`:35-36`); the instrument's
      revision chain and its own meta-sweep 0/6 → 6/6 (`self-hardening-r6.md`;
      ledger `:95`); the service contract and its boundaries
      (`SKILL.md:794-920`); the cadence and its first firing (`SKILL.md:1155`;
      ER-4 `:318`); the limits (`service-limits.md`, the refusal table's
      detail of record; compact copy on the method page); and the unknowns
      that stay unknowns (ledger U1/U2 `:218-220`, cross-host, coordinated
      rewrites, the 50 % crossover, sensitivity ≠ truth) — each line carrying
      its anchor (note:line, command, or standing receipt). The synthesis
      adds **no gate measurement** of its own — the ledger's own rule
      (`fleet-kill-rate-ledger.md:7`).
    - the **runbook** is its second half (§ *How to run it*): the tick's
      exact command set (ER-3 `:287-293`; executed ER-4 `:320-353`;
      `SKILL.md:1164`), the reading map (`current|stale|drift`, tool
      `held|moved`) and the trigger table T1–T3 with what to do on each
      (`SKILL.md:1069-1091`), the re-pin rule ("a moved pin is never
      re-interpreted; the old table stays"), where rows go (append-only; new
      errata below the last; `corpus/QUALITY.md` item 4), the re-sweep
      request shape (`service-optin-protocol.md:54-77`), and the refusals
      restated for the operator with pointers (the refusal table's home stays
      `service-limits.md` / the method-page copy; on drift the anchored
      source governs).
(2) Leg execution: the runbook is **executed by its author lane at the
    round's revision and pasted** — the tick (pin read + `--selftest` +
    `--regression`), the append discipline demonstrated on a scratch copy
    (a row appended only to the copy; the pre-round bytes of §1–§4 shown
    byte-identical; the real file written only where this round's own terms
    say), and, for each trigger class the round's state actually provides,
    one executed reading (T1/T2/T3); a class the state does not provide is
    recorded as not exercised, never manufactured. A runbook line that was
    never run is not written.
(3) Leg sufficiency: a **fresh executor** with no tameshi context beyond
    `HANDOFF.md` (its citations read-only) reproduces the operator loop the
    way round 3's executor reproduced the method from `SKILL.md` alone
    (`executor-test-sufficiency.md`; verdict vocabulary SUFFICIENT /
    SUFFICIENT (latitude) / ADDITIVE-IMPROVISATION / NOT EXERCISED / ADAPTED;
    contamination statement; evidence dir): (i) the tick; (ii) the sweep path
    exercised once — the round's dispatch read decides the form (a case the
    tick reads stale and the ledger carries no row for at its live revision
    gets a real appended row; otherwise the drill runs on a case 5/6 copy and
    is labeled a drill — no rate claimed for a recorded revision; if the tick
    reads `stale=0`, NOT EXERCISED is the complete outcome, not a failure);
    (iii) one refusal reading (no opt-in → no sweep); (iv) the append
    discipline on a scratch copy. Plus the falsifier pair aimed at the
    reader, not the engine: a doctored scratch copy whose case row points at
    a superseded blob reads `stale` while the untouched row reads `current`
    (the engine's own arm is selftested, `SKILL.md:1002-1007`).

Design-time state (measured by this lane; freeze above; re-measure at
dispatch):
- tameshi HEAD `c611d5d` ("probation round 8 (training r7)", 16:55:09 −03:00
  = 19:55:09Z). Round-9 writes mid-landing, unlanded at this read: ` M
  SKILL.md` (+104/−1 as of 20:02:45Z, still growing — 1152 → 1255 → 1269 L),
  ` M corpus/knowledge/fleet-kill-rate-ledger.md` (+38/−0 then +10/−0; 316 →
  353 → 363 L), `?? corpus/knowledge/service-limits.md` (266 L / 19 776 B /
  `0d4daea4…`, lane T9-2), `?? plans/round-9-record-draft.md` (scribe poll
  lane SCR-T9, in flight).
- Tool `tools/mutate-and-run.sh` `cf41efaa8be5f52d…` (1341 L / 61 632 B,
  r7-1): this lane's runs — `--selftest` → `MUTATE_SELFTEST: 67/67 pass` /
  `VERDICT: PASS`, rc 0 (`/tmp/w9-prept10-selftest/run.log`); `--regression`
  → `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0
  flips<=0)`, every leg `match=10/10 … flips=0`, `REGRESSION_DATE
  2026-10-14T19:59:30Z`, rc 0 (`/tmp/w9-prept10-regression/`).
- `SKILL.md` live `ee09c3bd…` 1269 L at 20:04Z (mid-write; round-8 revision
  was `6753b1b2…` 1152 L / 77 612 B). Round-9 section `:1155` (tick `:1164`,
  receipt `:1203`, re-pin semantics `:1221`, limits `:1236`+; line cells move
  with the file). Earlier anchors hold: service `:794`, leg ledger `:921`
  (contribution contract `:954`, receipt discipline `:965`, selftested arms
  `:1002`), cadence `:1010` (tick and pin read `:1021`, triggers `:1069`,
  six-case statement `:1092`), bands `:314-374`.
- `corpus/knowledge/fleet-kill-rate-ledger.md` live `2f25c51e…` 363 L at
  20:04Z (mid-write; pre-round-9 `71bc15e3…` 316 L / 28 503 B): §1 rows
  `:45-48`, embedding status `:85-88`, §3 queue `:98-130` (eight rows stand
  after ER-2's supersession `:280`), §4 `:132-158`, §8 unknowns `:216-237`
  (U9 `:235-237`), ER-2 `:272` (named hand-offs `:282`), ER-3 `:285`, ER-4
  `:318`, ER-4 addendum `:356`.
- `corpus/knowledge/service-limits.md` `0d4daea4…` 266 L (T9-2, round 9) —
  the refusal table's detail of record. `service-optin-protocol.md`
  `84d0c154…` 286 L — request shape `:54-77`, U1/U2/U3 `:259-266`.
  `fleet-suite-census.md` `ec1c2d8d…` 674 L — offer `:277-291` (scope
  `:288-291`); §5's instrument pin `597e1419…`/1001 L is two revisions stale
  (re-pin errata outstanding). `corpus/README.md` `1fe30500…` 20 L — coverage
  rows for the rounds 6–8 notes and both round-8 reports still absent at this
  read. `LOG.md` 307 L (`36e0f970…`), `SCORECARD.md` 21 L (`54202192…`)
  carry the round-8 rows.
- Round-9 lanes observable at this read ([O], read-only): `/tmp/w9-tameshi-t91`
  (tick: `tick.log`, `pin-read.log`, `regression/`), `/tmp/w9-tameshi-t93`
  (`pin-read-final.txt`, `falsifier/`), `/tmp/w9-t9-2` (limits lane),
  `/tmp/w9-tameshi-scr-t9` (scribe poll), `/tmp/w9-ver-t9-*`,
  `/tmp/w9-aud-t9-*`.
- Sibling trees: kumitate `175de6b`, kagi `fecee87`, tsukuroi `72b038d`, mado
  `12c8f08` (HEADs, this lane's reads); case paths clean at the 20:00Z read;
  both moved gates worktree-dirty again by 20:02:38/42Z (ER-4 addendum
  `:358-359`) — the owners' own round-9 lanes are live. Round-9 execution
  continues while this file is written; no pin in this plan is taken from a
  moving revision — the dispatch read is the authority.

Candidate decision (the dispatch named two):
- (A) the ten-round synthesis — **FOLDED as the handoff's spine**, not
  deferred and not a second file. Its content is exactly the operator's trust
  basis, and its rows already stand as receipts (ledger §0–§4;
  `SKILL.md:1092`); a standalone note would be a second artifact family
  re-quoting them — the ledger's own role is "one standing receipt instead of
  re-quoting" (`:5-8`) — and it would have no reader the handoff does not
  have. Precedent for folding, not splitting: round 9's candidate logic
  (`plans/round-9.plan.md:134-153`).
- (B) the ledger handoff note to the operator — **CHOSEN**. The gap is named
  by the records themselves (U9 `:235-237`; protocol U3 `:264-266`; the arc
  ends, and the operator is the seat left). Every falsifier is in-hand and
  read-only: the runbook's command set (ER-3/ER-4, executed), the refusals
  (`service-limits.md`), the fresh-executor pattern
  (`executor-test-sufficiency.md`), the append discipline (scratch copy). It
  also closes the loop the whole operability arc was building: round 8 made
  the ledger a service, round 9 made its cadence fire once — round 10 makes
  it someone's.
- Named, not chosen this round (anchors held): a standalone synthesis note
  (above — its would-be rows are the handoff's spine); cases 5/6 embedding
  (the tool owner's call, ER-2 `:282`); the census §5 re-pin errata; the
  eight standing queue gates (each needs an opt-in — the offer stands,
  `fleet-suite-census.md:277-291`); the attestation form (protocol U1,
  `:259-261`); the fleet-contributed case (`SKILL.md:954-963`); the L0
  announcement of the handoff (fleet-root write — the dispatcher's call);
  cross-host / coordinated-rewrite unknowns (ledger U1/U2) stay unmeasured —
  no move claims them.

Claim: round 10 closes the arc by making its product **self-carrying** — the
ten rounds' measured craft and its standing service handed to the operator as
one note a stranger can run. Its headline (proposed shape, landing
adjudicates) is the executor's own table — `HANDOFF: 1 note; tick
author-executed <date>; fresh executor <n>/<m> steps sufficient, <k> not
exercised; refusals <r> anchored; tool held|moved` — a statement about a
document a stranger ran, not about prose. The ten-round synthesis travels
inside the handoff; there is no second synthesis note. Nothing new is
measured: what ten rounds measured is what the note hands over, each line
still pointing at the receipt that carries it. An executor table that reads
NOT EXERCISED on the sweep step (the tick read `stale=0`) is a complete
outcome, recorded as such.

Also: round-9 clauses are the precondition set — checked at dispatch, never
assumed: the tick's landed block (ER-4 + addendum; the SKILL `:1155`
section); the limits note (`service-limits.md`, read as landed artifact — its
revision the authority); the re-sweep rows for the two stale cases (tsukuroi
`084951be…` → `bba6cdf6…`; mado `d7edaab4…` → `7da4ec50…`) as appended rows
with §1–§4 byte-identical — **unlanded at this read, in flight**; the re-pin
rule in the protocol or as append-only errata; the round-9 SKILL append; the
round-9 record draft's carried list, read as the debt ledger; the embedded
leg count (4; cases 5/6 unembedded unless the tool owner lands them — named
debt); sibling trees clean. An unlanded clause is named debt finished first
under round 9's own contract — never re-designed here. Whether rows 3/4's
re-sweep reproduces the recorded mechanisms at the live revisions is unknown
until measured — the re-sweep rows or their absence are read at dispatch.

Anti-claim: no new gate measurement, no rate re-cut, no service engagement —
the synthesis restates measured rows and nothing else; no generalization
beyond the measured bar (`PROVINCE.md:14-18`: a pattern is general only from
≥2 independent lanes; the survivor taxonomy stays a taxonomy; the bands stay
a report convention); no daemon, no timer, no schedule — "who runs it"
becomes the operator's standing choice, not a promise a lane can make ([U]
survives whether anyone invokes the command); the refusal lines are
restatements with pointers, never a second home (on drift the anchored source
governs, `service-limits.md` §0); no re-quoting of case tables where a
standing receipt exists (cite the ledger row, not the rate's prose); the
executor reads no live session (PATH-level stubs only,
`service-optin-protocol.md:129-132`) and writes nothing outside its scratch
(the ledger copy is a copy); sibling trees read-only, re-read before/after;
hermetic scope; no external sites; secrets shape-only; one move. A handoff
claim that cannot be re-derived by its cited command is cut, not softened.

Measure: (1) the handoff note — section map + the synthesized-claim set with
anchors (every claim line cites its receipt; spot-checked by a non-author one
level below the notes — raw `results.tsv`, mutant shas, headline cells —
across all sections); (2) the runbook executed by its author — the tick
pasted with output (pin read, selftest 67/67 or as landed, regression
`cases=N passed=N`), the append proof on a scratch copy (pre/post append-only
or region byte-compare), every quoted count carrying its command; (3) the
fresh executor's table — per-step verdicts + evidence dir + contamination
statement + the falsifier pair; (4) the closure pulse at the round's revision
— tool selftest/regression, six-case pin read, tool `held|moved`, sibling
trees clean before/after; (5) the coverage-map row for the handoff + the
outstanding rows (rounds 6–8 notes, both round-8 reports, any round-9 notes)
landed or re-named, LOG/SCORECARD per house rules; (6) unknowns carried
(ledger U1–U9 as amended by round 9; whether the operator adopts — [U]: the
round lands the handoff, not adoption); (7) every quoted count carries its
command.

Seats (suggested): synthesis+note seat (the handoff's author — the arc's
largest writing lane); runbook-execution seat (the tick + the scratch-append
proof); fresh-executor seat (a lane that did not write the note;
no-oral-context hygiene, `executor-test-sufficiency.md` precedent); non-author
verifier (claim sample one level below + byte-identity of quoted literals +
the refusal pointers); scribe (coverage rows — the handoff's own included —
LOG/SCORECARD, the round-10 record draft, the carried-debt sweep).

Write scope: round-10 execution scopes assigned at dispatch; this lane's
scratch `/tmp/w9-prept10-*`; this file is the only write (PREP-T10).