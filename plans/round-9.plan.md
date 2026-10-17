# WWKD plan — tameshi round 9 (ufo-round-plan-v1)

Design lane: PREP-T9 (2026-10-14, round-8 32-lane wave; round-8 execution in
flight and **unlanded** at this freeze — tameshi tree clean, no round-8
artifact on disk). Design-time state frozen **2026-10-14T19:15Z**; every
count below is a design read by this lane, re-measured at dispatch. Write
scope: this file only (PREP-T9); scratch `/tmp/w8-prept9-*`. Round-8 clauses
are the **precondition set** — checked at dispatch, never assumed
(`plans/round-8.plan.md:108-134`); where this draft and the landed round-8
artifacts disagree, the landed bytes are the authority.

Case frame — **6 cases in** (dispatch frame). Design-time arithmetic [O]: the
tool's leg ledger carries **4** cases at `cf41efaa…` (`REGRESSION: PASS
(cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, this lane's
run 19:14Z, workdir `/tmp/w8-prept9-regression/`), and the two
moved-substrate successors measured below — tsukuroi live `bba6cdf6…`, mado
live `90d50cdd…` — are the round's re-sweep cases that make six. The count
and composition are re-measured at dispatch; a measured count that differs
from six is recorded as the state, never manufactured (no case dropped,
widened, or re-cut to produce work).

Axis move: operability — **the ledger's cadence fires its first scheduled
tick**. ONE move, three ordered legs.
(1) Leg tick: the pin read at the round boundary, executed under the landed
    cadence policy (round 8's mechanism — pin state `current|stale|drift`,
    tool `held|moved`, tick, T1–T3, `plans/round-8.plan.md:11-31`) and pasted
    with its output; per case the recorded revision's relation to the live
    gate is read mechanically (`git show <rev>:<path>` sha256 vs the pin;
    `git merge-base --is-ancestor <rev> HEAD`), never inferred from prose. If
    the cadence section did not land, the pin read runs anyway and the
    unlanded mechanism is named debt finished first under round 8's own
    contract — this round does not re-design it.
(2) Leg re-sweep: every case the tick reads `stale`/`moved` is re-measured at
    its live revision — fresh `/tmp` copies, read-only targets, the same
    10-step recipe, the tool pinned per run (`MUTATE_TOOL`), the **recorded
    defect vocabulary** (each case's spec re-cut against the live bytes only
    where every `@old` still occurs exactly once — the tool's fail-closed
    spec parse; a moved anchor makes a NEW pre-registered spec, never a
    re-interpretation of the old table). Result lands as an **appended row**
    (case · recorded pin/rev → live pin/rev · tool sha · control line ·
    per-defect verdict delta · composition · date), the recorded tables
    byte-identical; the tool's leg registry gains a successor leg only where
    the contribution contract is met (pinned file set + spec + one-command
    hermetic suite + recorded table, `SKILL.md:954-963`) — otherwise the row
    is marked *not embedded* on the embedding-status line
    (`fleet-kill-rate-ledger.md:85-88`, append-only).
(3) Leg limits: the service's limits note — **what tameshi refuses to
    mutation-test and why** — lands as the refusal table the cadence applies
    at intake. Each refusal carries a measured anchor: (a) no pinned revision
    / no opted-in lane → no sweep (offer not a schedule,
    `fleet-suite-census.md:277-286`; `service-optin-protocol.md:26-30`);
    (b) no one-command hermetic suite → refused before any suite runs
    (`SKILL.md:813-817`); (c) a moved substrate without a re-pin → a
    recommendation, never an edit (`SKILL.md:823-825`); (d) live
    substrates/sessions → never read, PATH stubs only
    (`service-optin-protocol.md:129-132`); (e) credential material / endpoint
    health → out of province, report never absorb (`PROVINCE.md:14-18`);
    (f) product semantics — whether a gate's verdicts are right → never
    measured (sensitivity ≠ truth, `SKILL.md:879-881`;
    `fleet-suite-census.md:288-291`); (g) coordinated multi-edit rewrites →
    outside the vocabulary, no rate claimed (ledger U2, `:220`); (h) the
    exit-flatten family → harness boundary, named not fixed
    (`service-optin-protocol.md:267-269`); (i) a directed-repair re-run
    presented as a rate → recorded as directed repair
    (`fleet-kill-rate-ledger.md:35-36`); (j) foreign scratch → never removed
    (`service-optin-protocol.md:86-91`). Plus the one cadence precondition
    round 8's intake leg named: a **re-pin rule for a moved substrate** in
    the opt-in protocol — absent there, the finding lands as append-only
    contract errata (`corpus/QUALITY.md` item 4).

Design-time state (measured by this lane; freeze above; re-measure at
dispatch):
- tameshi HEAD `9f1d3c3` ("probation round 7 (training r6)", 16:06:31
  −03:00), `git status --porcelain` empty at 19:13Z.
- Tool `tools/mutate-and-run.sh` `cf41efaa8be5f52d…` (1341 L / 61632 B,
  `VERSION` r7-1 `:135`): `--selftest` → `MUTATE_SELFTEST: 67/67 pass` /
  `VERDICT: PASS`, rc 0, 4.8 s; `--regression` → 4 legs, per-leg
  `match=10/10 … flips=0`, closing PASS as quoted above, rc 0 (this lane's
  runs; logs `/tmp/w8-prept9-selftest/`, `/tmp/w8-prept9-regression/`).
  Embedded cases `:511-518`: js-kimi-census `83016d45…` @ `175de6ba…`;
  bash-surface-census `275d8294…` @ `fecee874…`; bash-tsukuroi-census
  `084951be…` @ `165307fe…`; bash-mado-verify `d7edaab4…` @ `eead56b2…`.
- `SKILL.md` `d36e9a28…` 1007 L / 68019 B — leg-ledger section `:921-1007`
  (contribution contract `:954-963`, receipt discipline `:965-1001`,
  selftested arms `:1002-1007`).
- `corpus/knowledge/fleet-kill-rate-ledger.md` `e08efe79…` 269 L: §1 rows
  `:45-48` (with `cases=2` quoted at `:160-176` — superseded by the r7-1
  revision and by this lane's `cases=4` run; a reader note, append-only),
  embedding status `:85-88`, §4 boundary `:155-158`, U3 `:221-223`
  (tsukuroi/mado not re-verified by the harness), U9 `:235-237` (cadence was
  a convention), ER-1 `:244-268` (mid-round tool drift + tsukuroi
  working-tree move, both superseded by round-7 lands).
- `corpus/knowledge/service-optin-protocol.md` `84d0c154…` 286 L — three
  engagement forms `:32-38` (attestation unexecuted), request shape
  `:54-77`, U1 `:259-261`, U3 (dispatch hand-off) `:264-266`.
- `corpus/knowledge/fleet-suite-census.md` `ec1c2d8d…` 674 L — §5 offer
  `:249-291`; its instrument pin `597e1419…`/1001 L is **two revisions
  stale** against `cf41efaa…` (a re-pin item for the scribe, append-only).
- `corpus/README.md` 20 L — coverage rows for the round-6/7 notes
  (`mutation-case-mado-verify.md`, `self-hardening-r6.md`,
  `fleet-kill-rate-ledger.md`, `service-optin-protocol.md`) still absent
  (carried debt, `plans/round-7-record-draft.md:220-221`). `LOG.md` /
  `SCORECARD.md` carry the round-7 rows.

The six cases at design time (target state read now; `current` = recorded pin
is the live sha, `stale` = recorded revision is an ancestor of the live gate):

| # | case | recorded pin @ rev | live today | state |
|---|---|---|---|---|
| 1 | js-kimi-census (kumitate `scripts/kimi-census.mjs`) | `83016d45…` @ `175de6ba…` | `83016d45…`, HEAD `175de6b`, clean | **current** |
| 2 | bash-surface-census (kagi `corpus/surface-census.sh`) | `275d8294…` @ `fecee874…` | `275d8294…`, HEAD `fecee87`, clean | **current** |
| 3 | bash-tsukuroi-census (`tools/tsukuroi-census.sh`) | `084951be…` @ `165307fe…` | **`bba6cdf6…`** 1472 L / 73919 B, = HEAD blob `aa136d6`, clean | **stale** (ancestor verified) |
| 4 | bash-mado-verify (`tools/mado-verify.sh`) | `d7edaab4…` @ `eead56b2…` | **`90d50cdd…`** 1755 L / 75771 B, = HEAD blob `0c20a76`, clean | **stale** (ancestor verified) |
| 5 | tsukuroi live successor | — | `bba6cdf6…`; `--selftest` → `PASS (49 cases, 49 passed, 0 failed)` rc 0 | re-measure case |
| 6 | mado live successor | — | `90d50cdd…`; `--selftest` → `89/89 assertions passed` rc 0; gate now carries its own `--regression` (mado M7-1) | re-measure case |

[O — post-freeze, 19:16:43Z, during this draft's write] mado's gate moved
again: `90d50cdd…` → `6ea07110…` (working tree, ` M tools/mado-verify.sh`),
and `plans/round-8-record-draft.md` appeared untracked in tsukuroi's and
mado's trees — round-8 execution is landing while this file is written. The
mado live cell above is a 19:15Z reading, superseded within the minute; no
pin in this plan is taken from the moving revision and the dispatch read is
the authority.

[O] Rows 3/4 are two revisions past the ledger's cells: row 3's cell recorded
live `aae45531…` (1,032 newlines), row 4's recorded live `c4c1afb7…`
(1,186 L) — both superseded (`:47-48`, `:81-83`). The tool's legs are
git-materialized, so the replay is unmoved by that drift (`SKILL.md:941-948`)
— the drift is ledger hygiene until the round re-measures, which is exactly
leg (2). [I] Rows 5/6 are the fifth/sixth cases only if round 8's drift leg
left them re-measured-or-open: whichever it left is named at dispatch; the
round sweeps what the ledger carries, not what this draft hopes it carries.

Candidate decision (the dispatch named two):
- (A) **the fleet ledger's first scheduled re-sweep — CHOSEN.** The gap is
  named by the ledger itself (U9; round 8 lands the mechanism, not the
  firing), the drift is measured and live (two gates two revisions past
  their cells, today), and every falsifier is in-hand and read-only (pin
  read, replay, re-sweep, append proof). It also closes the ledger's U3 for
  whichever cases the re-sweep reaches.
- (B) **the service's limits note — FOLDED as leg (3), not deferred.** A
  cadence that re-sweeps and re-pins must state what it will never sweep:
  the intake decision needs the refusal table, and round 8's intake leg named
  exactly the precondition (a re-pin rule) this note must either find in the
  protocol or file as errata. Precedent for folding, not splitting: tsukuroi's
  round-8 candidate logic (`tsukuroi-shokunin/plans/round-8.plan.md:45-50`).
  One mechanism, two readers — a second artifact family would be a defect.
- Named, not chosen this round (anchors held): the ten queue gates (ledger
  §3 `:98-130` — each needs an opt-in; no opt-in means the no-opt-in line);
  cite-check's full sweep (probe 1/4 only, ledger `:94`); the attestation
  form (protocol U1, `:259-261`); the fleet-contributed case (U,
  `SKILL.md:962-963`); the cross-host/coordinated-rewrite unknowns (ledger
  U1/U2) stay unmeasured — no move claims them.

Claim: round 9 makes the cadence fire once, by measurement. Its headline
(proposed shape, landing adjudicates) is the tick's own block —
`LEDGER: <N> cases in; target current=2 stale=2 drift=0; tool held|moved=…` —
followed by one appended row per stale case, the recorded tables
byte-identical, and `REGRESSION: PASS (cases=N passed=N; ledger legs exact)`
with `N` the leg count after the round. U9 is closed by execution for the
case set the ledger carries (the mechanism's first invocation; who physically
runs it stays the dispatcher's call), U3 by whatever the re-sweep reaches —
with any unlanded leg taken as named debt, never assumed. The limits note
lands with every refusal anchored; a re-sweep that reads `stale=0` on every
case is a complete outcome, recorded as such.

Also: round-8 clauses are the precondition set — the cadence policy (tick ·
T1–T3 · re-pin rule) landed in the ledger + SKILL; the drift rows if its leg
(2) landed them; the intake record (queue case or no-opt-in line); the
per-case pins in §1; the 4-leg replay still exact at the landed tool
revision; sibling trees clean. An unlanded clause is named debt finished
first under round 8's own contract — never re-designed here.

Anti-claim: no daemon — the tick is a command executed at the round boundary,
not a timer; no case is dropped, widened, or re-cut to manufacture work; a
moved pin is never re-interpreted (the old table stays; the live revision is
an appended row); a successor re-measure is a reading of an EXISTING case at
a named revision+composition (per-revision, per-host) — no new defect class,
no rate chased, the four-case confidence statement is not re-opened; a
divergence between tameshi's re-sweep and an owner's receipt is the FINDING
(two seats never merged, `service-optin-protocol.md:48-52`), never smoothed;
a FAIL never hand-re-swept to "confirm" — the row is quoted
(`SKILL.md:980-988`); the limits note states refusals, it does not adjudicate
them (out-of-province → report, never absorb, `PROVINCE.md:20`); sibling
trees read-only (kumitate `175de6b`, kagi `fecee87`, tsukuroi `aa136d6`, mado
`0c20a76`, all porcelain-clean at this read — re-checked before/after);
live sessions never read (stubs only); hermetic scope; no external sites;
secrets shape-only; one move.

Measure: (1) the pin-read block — the exact command and its output, per case
target `current|stale|drift` + tool `held|moved` with sha pairs, the
ancestor check named, run at the tick; (2) the re-sweep table per stale case:
control line, per-defect verdicts vs the recorded expectation, delta lines,
`MUTATE_RESTORE: OK`, target sha before=after, sibling tree clean
before/after, tool sha in every log; (3) the append proof — ledger sha
before → after with the pre-round bytes of §1–§4 shown byte-identical
(`git diff` appends-only, or a pre/post region comparison) and the new rows
quoted; (4) the tool receipt — `REGRESSION_PIN` per leg, per-leg
`match=10/10 flips=0`, `REGRESSION: PASS (cases=N passed=N)`, selftest green,
all at whatever revision the round executes; (5) the falsifier pair aimed at
the ledger's trigger, not the engine (the engine's pin-mismatch/unresolvable
arms are selftested, `SKILL.md:1002-1007`): a scratch copy whose case row
points at a superseded blob must read `stale` with the sweep lines unchanged,
while an untouched copy reads `current` (a doctored recorded pin is the
engine's own SETUP); (6) the limits note with every refusal anchored (a
refusal without an anchor is not written) and the intake precondition line
(present in the protocol → cited; absent → errata); (7) SKILL append (the
tick + the limits pointer + the re-pin semantics as executed), README
coverage rows for the four outstanding notes, LOG/SCORECARD per house rules;
(8) every quoted count carries its command; unknowns carried (ledger U1–U9 +
the round-8 U: whether any driver would invoke the command with no lane
acting + new: whether rows 5/6 reproduce the recorded mechanisms at the live
revisions — unknown until measured).

Seats (suggested): tick + pin-read seat (the block pasted); re-sweep seat
(one stale case per pass, evidence dirs lane-scoped `/tmp/w9-*`); limits-note
seat (refusal table + intake precondition); non-author verifier (falsifier
pair, byte-identity of the pre-round tables, one independent re-sweep row);
scribe (ledger append, SKILL append, README coverage rows, LOG/SCORECARD,
the census §5 re-pin errata).

Write scope: round-9 execution scopes assigned at dispatch; this lane's
scratch `/tmp/w8-prept9-*`; this file is the only write (PREP-T9).
