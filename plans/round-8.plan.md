# WWKD plan — tameshi round 8 (ufo-round-plan-v1)
Axis move: operability (post-service, second turn) — ONE move, three ordered
legs: the ledger stops being a snapshot and gains a MECHANISM — a re-sweep
CADENCE with pin-state semantics — closing the ledger's own U9 ("update
cadence is a convention, not a mechanism", `corpus/knowledge/
fleet-kill-rate-ledger.md:235-237`) and carrying its U3 (the tsukuroi/mado
tables "not re-verified by the harness's own --regression", `:221-223`).
The method's outputs already outlive their rounds (four sweeps, two owner
hardening passes); nothing yet says what re-runs them, at which revision, or
what a moved substrate reads as.
(1) Leg cadence: the policy + the mechanical pin read — per case, the
    target's relation to the fleet's live bytes (`current` = the recorded pin
    is the file's HEAD blob; `stale` = the recorded revision is an ancestor of
    the live gate — tsukuroi `084951be…` and mado `d7edaab4…` are both
    ancestors today, ledger `:47-48`; `drift` = a working tree differing from
    its HEAD), tool `held|moved` — read at the tick (the round boundary: the
    fleet driver idiom ends a lane's round on a report file and ticks 450 s,
    `scripts/shokunin-watchdog.sh:2-5`, and its lane map does not name
    tameshi, `:14` [O]; tameshi's tick is its own round series [I]; whether
    any driver would invoke the command with no lane acting [U]). Round 7's
    r7-1 edit already removes replay safety from this policy — a drifted
    working tree cannot move a materialized leg (`git show <rev>:<path>`) — so
    the pin read is ledger hygiene and a drift reading, not a replay guard.
    Triggers: T1 a case reads `stale` → a re-measurement at the live revision
    or the STALE cell with its reason, never an edit of the recorded table;
    T2 the harness sha ≠ a case's recorded tool pin → the reproduction is
    re-run under the new revision and both pins recorded (precedents: the mado
    spec re-cut under `b56c6e57…` with identical verdicts + mutant shas,
    ledger `:48`; the harness itself kept moving today, state block below);
    T3 an owner lane records a re-run at a new revision → an appended
    row, never an edit of §1–§4 (the ledger's own rule, `:170-172`).
(2) Leg drift: a moved pin is never re-interpreted against the new bytes
    (`SKILL.md:811-812`); the ledger carries the moved case at its newest
    revision with the old table intact. Four measured instances, all manual:
    the harness `597e1419…` → `b56c6e57…` (round 6, mid-round, by a concurrent
    lane, `mutation-case-mado-verify.md:17-23`) and again `b56c6e57…` →
    `4dc69ef9…` → `e3f838d4…` → `cf41efaa…` (this lane's window, 15:27–15:29;
    the case tables measured under the earlier revision were not re-run by the
    moving lane); mado `d7edaab4…` 4/10 → hardened
    `c4c1afb7…`, same spec, 10/10
    (`mado-shokunin/corpus/knowledge/gate-mutation-proof.md:20-22`, `:45`);
    tsukuroi `084951be…` 6/10, its four survivors replayed at the hardened
    `aae45531…` → B10 killed, B7/B8/B9 still survived (ledger `:47`). A moved
    case nobody has re-measured is this round's re-sweep work — fresh /tmp
    copies, read-only, the same 10-step recipe, bounded by the recorded
    defect vocabulary (no case is dropped or widened to produce work).
(3) Leg intake: the cadence covers whatever case set the ledger carries at
    dispatch — embed status measured, never assumed (the ledger says the
    four-case embed had not landed at its write, `:170-172`; the two-case tool
    this lane executed, and the r7-1 edit landing four legs during this
    draft, state block below) — a queue position freed
    by round 7 enters as a case, and the round-7 opt-in protocol
    (`corpus/knowledge/service-optin-protocol.md:53-106`) is checked for the
    one precondition a cadence needs: a re-pin rule for a moved substrate; a
    request shape without it is the finding and lands as contract errata.

Design-time state (frozen 2026-10-14T18:26Z, PREP-T8 lane; this is a design,
every count re-measured at dispatch): HEAD `4494715` (round 6 landed 15:17;
`git log -1`), tameshi tree clean at 18:20Z. Tool, the revision this lane executed:
`b56c6e57…22bcb`, 1080 L / 46850 B (`sha256sum`, `wc -l`, `stat -c %s`),
`VERSION` still r4-2 — `--selftest` → `MUTATE_SELFTEST: 55/55 pass` /
`VERDICT: PASS` rc 0; `--regression` → `REGRESSION: PASS (cases=2 passed=2;
band killed-delta<=1 flips<=1)`, both cases `match=10/10 … flips=0`, rc 0
(`/tmp/w7-prept8/{selftest,regression}.log`; `REGRESSION_DATE
2026-10-14T18:23:52Z`). Two cases embedded at that revision
(`regression_specs :512`), headline literals `cases=2` (`:756`, `:766`),
pin-mismatch refusal (`:613`) selftested (`:957`, `:960`) — an engine arm,
not a ledger service. [O] The tool kept moving inside this lane's window:
`b56c6e57…` → `4dc69ef9…` (15:27:40, 1247 L / 56518 B: header
`r7-1 leg ledger` — all four fleet specs embedded, each leg materialized from
its repo's git object store `git show <rev>:<path>`, pin mismatch = SETUP,
while the runner body still executed two legs) → `e3f838d4…` (15:28:38,
61305 B: the headline count parameterized, `:965`) → `cf41efaa…` (15:29:01,
61632 B) — still moving at this freeze. Those revisions were
read at their headers, never executed by this lane — the landed revision at
dispatch is the authority, and its mechanism (materialized legs, exact
expectation) is what leg (1) below must be written against.
SKILL `137879dd…59bb`, 918 L (final line unterminated) / 62373 B; service
section `:794`+, 4th-case list `:776-792`. Census `fleet-suite-census.md`,
674 L (final line unterminated) / 48719 B: §5 pins the instrument at
`597e1419…`/1001 L (`:251-262`) and the method at `dd2f4dee…`/665 L
(`:263-267`) — both two revisions stale against today's live files (a re-pin
item, never a re-interpretation). Round 7 was landing during this freeze
(untracked, mtime 15:25): `corpus/knowledge/fleet-kill-rate-ledger.md`
(241 L, `30917b4b…`) and `corpus/knowledge/service-optin-protocol.md`
(283 L, `45b355a4…`) — shape and named unknowns used as anchors here; at
dispatch they are re-read as landed artifacts, not taken from this read.

Candidate decision (the dispatch named two):
- (A) the fleet ledger as a standing service with a re-sweep cadence —
  CHOSEN: the gap is named by the ledger itself (U9 above), the evidence is
  four measured drift instances (the harness alone moved three times in one
  day), and every falsifier is in-hand and
  read-only (pin read, replay, re-sweep, intake). It also un-parks round 7's
  U3 rather than leaving it to a future embedding round.
- (B) the regression gate adopted by a 3rd lane — DEFERRED with anchors:
  tameshi owns the instrument; mado is the intended second carrier but its
  round-7 stage (a) had not landed at its own draft's read (`usage error:
  unknown argument '--regression'`, rc 2, `mado-shokunin/plans/
  round-7-record-draft.md:136-137`; `grep -c regression` → 0 in the gate,
  `mado-shokunin/plans/round-8.plan.md:32-33`) and mado's own round-8 plan
  consumes the mode for its widening (`:93`). A third carrier needs a second
  lane to land first, and an opt-in that may not come. Deferred, not dropped:
  (A)'s intake leg measures the same generality from inside the ledger — a
  lane's case living on after its round — and this section is (B)'s anchor
  set for the next draft.

Claim: round 8 makes the ledger stand. Its headline (proposed shape, landing
adjudicates) carries the pin state — `LEDGER: <cases> pinned: held=N moved=M
stale=K` + `REGRESSION: PASS (cases=H passed=H)` over the held set
(H = N − moved − stale), per-case `REGRESSION_TABLE … flips=0` re-verified
against each recorded table — and drift is a line, not a footnote: each moved
case carries its newest revision with both shas and the delta, appended
(mado 40 % → 100 % and tsukuroi's 1-of-4 survivor replay are the two
precedents this ledger absorbs). The cadence policy lands as an executed
command — the pin read pasted with its output, the tick and T1–T3 stated, the
update rule fixed — which is U9 closed by measurement for the *mechanism*
(who physically runs it stays the dispatcher's call, the ledger's own scope).
U3 is closed to whatever the case set reproduces: the count is measured
(cases=2 in the revision this lane executed; the r7-1 edit landing four legs
during this draft makes 4 the likely dispatch state), with any unlanded leg
taken as named debt. A read
that finds `moved=0 stale=0` is a complete outcome, recorded as such.

Also: round-7 clauses are the precondition set — checked at dispatch, never
assumed (`plans/round-7.plan.md:36-44`, `:62-69`): the ledger note with
per-case pins and sources (at this read §1/§5/§7 carried them), the
contribution/opt-in protocol (landed as `service-optin-protocol.md`), the
every-case `--regression` embedding (round-7 leg 1; two legs in the revision
executed here, four in the r7-1 edit landing during this draft), the mado
fleet-run attestation or its named missing piece, the queue record
(engagement #2 or the no-opt-in line), sibling trees clean. An unlanded
clause is named debt finished first under round 7's own contract — never
re-designed here — and the ledger carries what actually landed.

Anti-claim: no daemon — "standing" = the ledger + the policy + the executed
command at the round boundary; tameshi starts no background process and
installs no timer ([O] no round created one; [U] whether a fleet driver would
ever invoke the command unaided); a moved pin is never re-interpreted (the old
table stays; the new revision is an appended row); `moved=0` is recorded,
never manufactured by re-cutting cases to make drift; divergence between a
cadence re-sweep and an owner's receipt is the FINDING (per-revision,
per-host scope, `fleet-suite-census.md:288-291`), not smoothed; the 4th case
stays falsifier-only (`SKILL.md:776-792`) — a re-sweep at a hardened revision
is a drift reading of an EXISTING case, no new gate, no new defect class, no
rate chased; a tool change made by this round lands with a selftest label and
its new revision is itself a T2 event the ledger records; sibling trees
read-only (kumitate `175de6b`, kagi `fecee87`, tsukuroi `dc3436d`, mado
`c8f6667` porcelain-clean before/after — ledger §6 S1, `:186`); hermetic
scope; no external sites; secrets shape-only; one move.

Measure: the per-case pin read (target `current|stale|drift` + tool
`held|moved`, sha pairs) with the exact counting command; the headline +
`REGRESSION: PASS`
with H stated, per-case tables byte-compared to the recorded ones (flips=0)
and T2's re-verification line if the tool moved; the drift table (case,
recorded revision → live revision → newest case revision → delta, each with
its source file/command); the falsifier pair on the cadence — a scratch copy
whose case row points at a superseded blob must read `stale` (one at an
uncommitted tree `drift`) with the sweep lines for that case unchanged, while
an untouched copy reads `current` (a doctored recorded pin is the engine's
own SETUP, already selftested `:957`/`:960`, so this falsifier is aimed at the
ledger's trigger,
not the engine); the ledger's cadence section + SKILL append (service section
gains tick, T1–T3, RE-PIN semantics) + census §5 re-pin errata if round 7 did
not land it; LOG/SCORECARD per house rules; every quoted count carries its
command. Seats (suggested): cadence+drift seat (pin read + ledger section),
intake seat (queue case + opt-in precondition check), non-author verifier
(falsifier pair + per-case table comparison), scribe (LOG/SCORECARD/SKILL/
census errata).

Write scope: this file only (PREP-T8). Round-8 execution scopes assigned at
dispatch; this lane's scratch `/tmp/w7-prept8-*`.