# Service limits — what tameshi refuses to mutation-test, and why (T9-2, round 9)

Written 2026-10-14 by lane T9-2 (tameshi round 9, leg 3 of
`plans/round-9.plan.md:47-69`). Role: the **refusal table the re-sweep cadence
applies at intake** — what this service will not sweep, the trigger that fires
each refusal, what happens instead, and the measured reason. It is the
complement of the standing offer (`fleet-suite-census.md:269-275`): the offer
states what a sweep needs; this note states what no sweep is run against. It
states refusals; it does not adjudicate them (out-of-province → report, never
absorb, `PROVINCE.md:20`). The same table renders compactly on the method page
(`SKILL.md:1230-1249`, round-9 section `:1155`, landed during this write);
this note is the detail of record, with the verbatim anchors behind each row.

Anchors: **O** observation (command output / file:line, re-quoted measured
cell) · **I** inference · **U** unknown. Substrates read-only during this
write; scratch `/tmp/w9-t9-2/`; this note is the lane's only write. Line cites
are this write's revision of each file (§6 pins, re-measured
2026-10-14T20:02:29Z). [O] The ledger and `SKILL.md` were under concurrent
round-9 appends while this note was written — the ledger gained ER-4 (T9-1's
tick receipt) and `SKILL.md` gained its round-9 section mid-write; every line
cited below was re-checked against the post-append bytes, and a reader on a
differing revision re-resolves rather than trusts (the page's own rule,
`SKILL.md:1249-1250`).

## 0. Reading the table

- One row = one refusal; "refused" means one of: **no sweep runs** · **no rate
  is claimed** · **no edit is made** — never a silent drop, and never a case
  re-cut or widened to manufacture work (`plans/round-9.plan.md:174-181`).
- **A refusal without an anchor is not written here** (this round's measure
  clause, `plans/round-9.plan.md:205-207`): every reason cell is a quoted
  file:line or a run output; §2 carries the verbatim quotes.
- Three claim-bounds ride every sweep and are not re-derived per row:
  single-edit mutants only · hermetic suites only · per-revision and per-host
  results (`fleet-suite-census.md:288-291`; `SKILL.md:860-863`).
- The consumer: the round-boundary tick + pin read (`fleet-kill-rate-ledger.md:285`
  ER-3, `:318` ER-4; `SKILL.md:1010`). Executed state at the round-9 tick:
  `LEDGER: 6 cases in; target current=4 stale=2 drift=0; tool held`
  (`fleet-kill-rate-ledger.md:333`) — a tick that reads `stale=0` is as
  complete as one that reads `stale=2` (SKILL `:1085-1086`).

## 1. The decision table

| # | Refused — no sweep runs against … | Trigger at intake | What happens instead | Measured reason (anchor) |
|---|---|---|---|---|
| a | a gate with no opt-in and no pinned revision | no lane names the gate; or a request arrives without committed bytes (sha256 · size · lines · porcelain-clean tree at open) | no sweep; the queue is an offer, not a schedule; the standing default head is surface-probe; a round with no opt-in records the no-opt-in line as its complete outcome | `service-optin-protocol.md:26-30`; `fleet-suite-census.md:269-275`, `:277` |
| b | a gate with no one-command hermetic suite (and no runnable spec) | the suite cannot run against a copy, does not exercise the copy, prints no executed count, or reads a live path; or an `@old` is not unique | refused before any suite runs — `MUTATE: SETUP (<reason>)`, exit 2, no headline; a red control also exits 2 | `SKILL.md:813-817`, `:840-844`; `service-optin-protocol.md:199-201` |
| c | a moved substrate held to the old table | `stale` (the recorded revision no longer names the live bytes) or `drift` (worktree differs from HEAD) | a re-pin, never a re-interpretation — the old table stays, the moved case lands appended at its newest revision with both shas; the service never edits, repairs or re-pins a gate (recommendation to the owner); a dirty tree waits for the commit | `SKILL.md:811-812`, `:823-825`, `:1035`, `:1083-1086`; `fleet-kill-rate-ledger.md:293`, `:310` |
| d | live-substrate-coupled gates — incl. handler-gated cases (`the-janitor` handlers) | any suite or probe that would read the live plane — host state, services, a session, a live handler | never read: PATH-level stubs only, never the session; the hermetic subset is measured, the live rows declared out of scope; a handler-absent host records `skip-case … substrate-absent` and does not execute the verbs block | `service-optin-protocol.md:129-132`; `mutation-case-mado-verify.md:10-11`, `:161-163`; `mutation-case-kagi-census.md:27-29`, `:36-38` |
| e | secrets-adjacent code — credential material and endpoint health | a target or probe whose content is credential material (vault refs, `op.env`, tokens) or whose verdicts are endpoint health | out of province: report, never absorb (credential → kagi; endpoint → kama); secrets shape-only, never content-read; secret *guards* (deny-list rows naming the handlers) are swept hermetically — the material is not | `PROVINCE.md:16-18`, `:20`; `SKILL.md:21`; `AGENTS.md:4-5`; `gates-survey-kagi.md:136-138`, `:179-182`, `:610-614`; `mutation-case-kagi-checklist.md:185`, `:221-223` |
| f | product semantics — whether a gate's verdicts are right | the question asked is truth, not detectability | never measured — sensitivity ≠ truth; a sweep measures what the suite can detect | `SKILL.md:879-881`; `fleet-kill-rate-ledger.md:156-158` |
| g | coordinated multi-edit rewrites | the defect set would be multi-site | outside the vocabulary — no rate claimed; a rate is bounded by its defect vocabulary | `SKILL.md:860-861`; `fleet-kill-rate-ledger.md:220` (U2); `fleet-suite-census.md:288-289` |
| h | the exit-flatten family | a mutant whose only observable change is the exit map, under an exit-code-only harness | named boundary, not fixed — exit-only adjudication cannot kill it; a stdout-reading harness is a named future | `service-optin-protocol.md:267-269`, `:200-201`; `fleet-kill-rate-ledger.md:48` |
| i | a directed-repair re-run presented as a rate | an owner's post-hardening re-run of the same spec arrives as an independent rate | recorded as directed repair — a re-sweep (fresh or extended spec) is the new independent reading | `fleet-kill-rate-ledger.md:35-36`, `:308`; `service-optin-protocol.md:160-161` |
| j | foreign scratch | the work area holds other lanes' `/tmp` dirs, or a suite shares fixture scratch | never removed — only the service's own scratch paths are removed; the mado run kept exactly its own 8 of ≥37 foreign dirs | `service-optin-protocol.md:86-91`, `:105` |

## 2. Row detail — the measured reasons, verbatim

**(a) No opt-in / no pin.** `service-optin-protocol.md:26-30` — "The queue
(`fleet-suite-census.md:277-286`) is an offer, not a schedule: at round-7
dispatch it drains only under a fresh opt-in naming a pinned target + a
hermetic suite, the standing default head is surface-probe, and a round with
no opt-in records the no-opt-in line as its complete outcome." The offer
itself is standing with "no current commitment" (`fleet-suite-census.md:269`).
[U] The dispatch hand-off — how an opt-in reaches the service between waves
with no tameshi lane live — is unmeasured; "the standing record is the
no-opt-in line" (protocol `:264-266`).

**(b) No hermetic suite / no runnable spec.** The suite "must exercise the copy
it is handed …, print its own executed count and verdict …, and read no live
path" (`SKILL.md:813-817`). The refusal is fail-closed and pre-run: every
`@old` unique "asserted **before any suite run**; `@new == @old` is refused.
Any spec failure is `MUTATE: SETUP (<reason>)`, exit 2 — no headline"
(`SKILL.md:840-842`); "a red control exits 2 (kills could not be attributed)"
(`:843-844`). Mado's run pre-registered exactly these semantics: "a red
control, an unrunnable suite, or target drift is exit 2 with no headline"
(protocol `:80-85`). The refusal arms are selftested at the tool's current
revision — §4 SC2.

**(c) A moved substrate.** `SKILL.md:811-812` — "A moved substrate needs a
re-pin, never a re-interpretation of the old table." `:823-825` — "The service
never edits, repairs or re-pins the gate; a needed change is a recommendation
to the owner". `:1083-1085` — "The re-pin rule. A moved pin is never
re-interpreted against the new bytes (:811-812). The old table stays; the moved
case lands at its newest revision with both shas and the delta, appended."
`moved=0 stale=0` is a complete outcome, "drift is never manufactured by
re-cutting cases" (`:1085-1086`). Drift: "a writer is on the gate; wait for
the commit, then re-pin" (`fleet-kill-rate-ledger.md:293`); the round-9 tick
watched mado's drift close into a committed `stale` cell — the working-tree
transients resolved into `7da4ec50…` (`SKILL.md:1186-1189`; ledger `:338`).

**(d) Live substrates / sessions — incl. `the-janitor` handlers.**
`service-optin-protocol.md:129-131` — "No live substrate read. Hermetic suites
by construction; where a probe needs a live-plane branch it is a PATH-level
stub, never the session". Mado's measured instance: "no live substrate read —
every live-plane probe binary used in §2 was a local stub, never the session"
(`mutation-case-mado-verify.md:10-11`); of 106 `row …` call sites, "51 under
`hypr-live`" and "the hermetic suite executes exactly the two guard rows"
(`:161-163`) — [I] every live-plane defect is invisible by construction, and
none was mutated; the forward path is a stub scenario, "extend it from
*starving* the command to *answering* it" (`:244-246`). The `the-janitor`
instance: kagi's surface-census carries two trailing verb cases that are
substrate-gated — "`command -v "$JANITOR"` (`:817`) records `skip-case …
substrate-absent (handler not on PATH)` (`:820-823`) and does not execute the
verbs block. Measured host facts: `the-janitor` is **MISSING** from PATH"
(`mutation-case-kagi-census.md:27-29`); [I] on a handler-present host "the two
cases would exec the real binary … a verbs-logic mutant's verdict would then
be host-dependent" — kept as that case's U2 (`:36-38`); re-read at this write:
`command -v the-janitor` → rc 1 (§4 SC2). The guard rows *naming* the handlers
are still sweepable hermetically — kagi's `DENY_WORD_RE` (`op|the-janitor|…`,
`gates-survey-kagi.md:119-121`) and checklist `DENY_CHECK` (`op.env`,
`op run|read|inject`, `the-janitor start|stop|run`; `:133-135`); the measured
sweep-side instance is in (e).

**(e) Secrets-adjacent code.** `PROVINCE.md:16-18` — "Never edits a sibling's
gate code (read-only probes; recommendations travel in round reports).
Credential material (→ kagi), endpoint health (→ kama)."; `:20` — "Out of
province → report, never absorb." `SKILL.md:21` — "Secrets shape-only, never
content-read." `AGENTS.md:4-5` — "Substrates outside this repo are read-only
unless PROVINCE.md declares otherwise. Secrets are shape-only, never
content-read." The gates' own pins are the model: `drift-pins.sh:146` emits
`POLICY` for a no-hash path — "secret-bearing path is never hashed"
(`gates-survey-kagi.md:136-138`); the `op.env` row is "pinned by mode + lines
only, sha field `-`, since a content hash of a secret-bearing file is an
offline guessing oracle" (`:179-182`); secret hygiene is "stated in the header
as a prohibition", and `claim-ledger.sh:85-86` "never echoes a claim's output"
(`:199-203`). The survey's positive statement: "never read the content of
`~/.config/the-janitor/op.env`, any `op://` reference path, any vault item, any
OAuth token, or any `server.token`" — one shape-only path-presence check only
(`:612-614`). Measured sweep-side instance: case 5's B3 — the deny-list
alternative `the-janitor stop` dropped → SURVIVED; probe: pristine `POLICY row
C1 …`, rc 2 vs mutant "accepted; listed, rc 0 (probe never execs the verb)"
(`mutation-case-kagi-checklist.md:185`); "the deny-list drop (B3) is the first
secret-hygiene surface this method has found re-openable by a single edit"
(`:221-223`). Reading: the *guard* is sweepable and was swept; the *material*
was never read.

**(f) Product semantics.** `SKILL.md:879-880` — "Sensitivity, not truth — a
sweep measures what the suite can detect, never whether the gate's verdicts are
right". Ledger boundary: "suite sensitivity ≠ gate truth (nothing here
measures whether a gate's verdicts about the real world are right)"
(`fleet-kill-rate-ledger.md:156-158`).

**(g) Coordinated rewrites.** `SKILL.md:860-861` — "Single-edit mutants only —
coordinated rewrites are unmeasured (matrix row F); a rate is bounded by its
defect vocabulary." Ledger U2 — "coordinated multi-edit rewrites unmeasured
everywhere (matrix §7)" (`:220`); census scope `:288-289`.

**(h) The exit-flatten family.** `service-optin-protocol.md:267-269` — "U4 — a
harness that adjudicates by exit code alone cannot kill the exit-flatten
family; a stdout-reading harness is a named future, not a measurement". The
adjudication rule that bounds kills: "killed = suite red **and** the full case
count still enumerated (exit-only is insufficient)" (`:200-201`). Mado's row
keeps the residue named: "rc-6 dead arm, exit-flatten family, 51 live-plane
row sites, 2 out-of-band usage exits" (`fleet-kill-rate-ledger.md:48`).

**(i) A directed-repair re-run presented as a rate.** Ledger `:35-36` — "A
post-hardening re-run of the same spec is a **directed repair**, not an
independent rate; it is recorded as such." ER-3 T1: "the owner's own spec
re-run closes *that spec* (directed repair, §0) — an independent re-sweep
(fresh or extended spec) is the new independent reading" (`:308`). Protocol
rule 3: "A re-run proves the hardened suite kills *that* spec; it is not a
general rate" (`:160-161`).

**(j) Foreign scratch.** `service-optin-protocol.md:86-91` — "Scratch namespace
per lane. Every write is lane-scoped (round-7 convention `/tmp/w7-<lane>-*`).
A suite with shared fixture scratch is an incident, not a licence: the mado
run saw ≥37 foreign `/tmp/w5-mado-m52-selftest.*` directories, kept exactly its
own 8, and removed exactly those paths". Template: "scratch: /tmp/w7-<lane>-*
(lane-scoped; foreign scratch never removed)" (`:105`).

## 3. The intake precondition — the re-pin rule (checked: present, cited)

Round 8's intake leg named one cadence precondition to check: a re-pin rule for
a moved substrate in the opt-in protocol — absent there, it was to be filed as
append-only contract errata (`corpus/QUALITY.md:7`, item 4), never patched in.

Checked at this write: **present.** `service-optin-protocol.md:59-63` (request
shape, item 1) carries: "A moved substrate needs a re-pin, never a
re-interpretation of the old table." (`:61-62`). The method-side restatement is
`SKILL.md:811-812`; the landed cadence cites the same sentence — "the request
shape already carries this (`service-optin-protocol.md:59-62`)"
(`fleet-kill-rate-ledger.md:310`, ER-3 trigger 3) — and operationalizes it at
`SKILL.md:1083-1086`; the round-9 section records the same finding at
`SKILL.md:1220-1223`.

- [O] Its form: one sentence inside the request shape's pin item, not a
  separately numbered clause; the operational procedure (re-measure at the
  live revision · append · never edit the recorded table · both revisions stay
  in the record) lives in the cadence policy, not the protocol.
- **No errata needed** — the precondition was found, verbatim, where round 8
  said to look. Had it been absent, the finding would have been filed as an
  append-only contract errata block by the note's scribe, not written into the
  protocol from this lane (write scope: this file only).

## 4. Spot-checks (run at this write, 2026-10-14; scratch `/tmp/w9-t9-2/`)

- **SC1 — the intake precondition, on the live bytes.** `sed -n '59,63p'
  corpus/knowledge/service-optin-protocol.md` → item 1 ending "A moved
  substrate needs a re-pin, never a re-interpretation of the old table.";
  `sed -n '808,812p' SKILL.md` → the restatement, same sentence. [O]
- **SC2 — the-janitor / live-handler boundary + the refusal arms.**
  `command -v the-janitor; echo rc=$?` → no path printed, rc 1 (absent from
  PATH at this write — a PATH-level reading, the allowed form, protocol
  `:129-131`). `sed -n '27,30p' corpus/knowledge/mutation-case-kagi-census.md`
  → the substrate-gated case + "`the-janitor` is **MISSING** from PATH".
  `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` /
  `VERDICT: PASS`, rc 0, tool `cf41efaa…` (log
  `/tmp/w9-t9-2/selftest.log`) — the SETUP / unresolved-pin refusal arms are
  selftested, not conventions (`SKILL.md:1002-1007`). [O]
- **SC3 — the out-of-province lines.** `sed -n '14,20p' PROVINCE.md` →
  "Credential material (→ kagi), endpoint health (→ kama)." + "**Out of
  province → report, never absorb.**"; `sed -n '21p' SKILL.md` → "Secrets
  shape-only, never content-read."; `sed -n '136,138p'
  corpus/knowledge/gates-survey-kagi.md` → the no-hash POLICY,
  "secret-bearing path is never hashed". [O]

## 5. Unknowns

- **U1 — driver invocation.** Whether any fleet driver would apply this table
  (or the tick) with no lane acting is the cadence's open [U]
  (`SKILL.md:1017-1019`); ER-4 runs the tick only as an executed command at a
  round boundary.
- **U2 — handler-present hosts.** The kagi case's own U2 stands: no sweep of
  the verbs block has been made on a host where `the-janitor` is on PATH; a
  verbs-logic mutant's verdict there would be host-dependent
  (`mutation-case-kagi-census.md:36-38`).
- **U3 — request-side secrets refusal untested.** The secrets refusal is
  policy- and design-anchored (province boundaries + the gates' own guard
  design + the measured B3 guard survivor), not instance-anchored: no recorded
  request has asked tameshi to sweep credential material.
- **U4 — the exit-flatten boundary** is named from one harness generation;
  whether a stdout-reading harness would close it is unmeasured (protocol U4
  `:267-269`).
- **U5 — host-dependence of the PATH readings.** `the-janitor` absent at this
  write and at the kagi survey (two readings, one host); cross-host readings
  unmeasured (protocol U5 `:270-272`).
- Carried: the ledger's U1–U9 stand as written; this note adds no measurement
  to them.

## 6. Sources (pinned at this write; sha256 first-16 · `wc -l`)

| File | sha256 (16) | lines |
|---|---|---|
| `SKILL.md` | `b9a1b567f82cddb0` | 1249 |
| `PROVINCE.md` | `f5e28bf144b0601c` | 20 |
| `AGENTS.md` | `cb9409e1c6fde1f1` | 6 |
| `corpus/QUALITY.md` | `1923c94f49788ade` | 8 |
| `corpus/knowledge/service-optin-protocol.md` | `84d0c1547eed257d` | 286 |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | `5ccf95c26f0a1501` | 353 |
| `corpus/knowledge/fleet-suite-census.md` | `ec1c2d8d2877a21d` | 674 |
| `corpus/knowledge/mutation-case-kagi-census.md` | `0d5dc3cd7d2d21a3` | 258 |
| `corpus/knowledge/mutation-case-mado-verify.md` | `f2d53d495e6c1d8b` | 323 |
| `corpus/knowledge/mutation-case-kagi-checklist.md` | `43da70e675b8a482` | 367 |
| `corpus/knowledge/gates-survey-kagi.md` | `4734f0a0bd28e90f` | 619 |
| `tools/mutate-and-run.sh` | `cf41efaa8be5f52d` | 1341 |

[O] Drift during the write, recorded not smoothed: the ledger moved
`71bc15e3…` → `dce68463…` → `5ccf95c2…` and `SKILL.md` `6753b1b2…` →
`b9a1b567…` while this note was being written (round-9 lanes appending ER-4
and the round-9 SKILL section). Every line cited above was re-checked against
the final bytes; a reader on any later revision re-resolves.

## 7. Errata (append-only)

(none yet — new entries go below this line, never edits above, per
`corpus/QUALITY.md:7`, item 4)

**ER-1 — post-write concurrent drift, recorded not smoothed (O; appended 2026-10-14 ~20:05Z by T9-2, minutes after §6 was written).** Between §6's re-measure (20:02:29Z) and this append both round-9 landings kept moving — the concurrent lanes are still writing.

1. **`SKILL.md`** — `b9a1b567…` (1249 L, §6's pin) → `52330fee…` (1265 L) → `ee09c3bd…` (1269 L at this append). The round-9 section was **edited in place**, not merely appended: its internal lines shifted. Write-time cites inside that section are therefore superseded — `:1230-1249` (the limits-table rendering), `:1220-1223` (the intake-precondition bullet), `:1249-1250` (the re-resolve line). Orientation readings at this append: section header `## The cadence's first scheduled tick, and the service's limits` `:1155` (unmoved); the intake bullet `:1235-1238`; `### The service's limits — what tameshi refuses to mutation-test` `:1246`; re-resolve line `:1269-1270`. **Cite the round-9 SKILL section by heading, not by line, while the round is in flight.** Every cite of this note outside that section re-read unmoved (incl. `SKILL.md:1002-1007`, `:1017-1019`, `:1035` on the current bytes).
2. **`fleet-kill-rate-ledger.md`** — `5ccf95c2…` (353 L, §6's pin) → `2f25c51e…` (363 L; ER-4 addendum, an append). All ledger cites (`:36`, `:48`, `:156-158`, `:220`, `:285`, `:293`, `:310`, `:333`, `:338`) re-read unmoved; §6's ledger pin is superseded.
3. Re-read unmoved at this append: protocol `84d0c154…`, census `ec1c2d8d…`, both case notes, the kagi survey, `PROVINCE.md`, `AGENTS.md`, `corpus/QUALITY.md`; tool still `cf41efaa…` (held).

No claim in §1–§5 is re-cut by this entry; the moved cells are read-only observations, and the SKILL rendering still agrees with this note's table (row ids a–j, same refusals). A third party appending here is normal: the block is errata, append-only.

New errata entries go below this one.

**ER-jj — jj-era reading of "HEAD" (round 17, 2026-10-20; append-only).** Lane and owner repos are jj-colocated, so git HEAD is detached at the working-copy commit's parent and may differ from the branch tip (S061). Every active instruction above that reads `HEAD` (`show HEAD:<path>`, ancestor of HEAD, worktree vs HEAD, `git archive HEAD`) now reads the branch tip `refs/heads/<branch>` (`detect_branch`, `../scripts/hyaku/jj-lane.sh:53-65`) or an explicit 40-hex revision; dated records above are not re-interpreted. Canonical rule: `SKILL.md:1027-1035`, `operator-runbook.md` ER-R3.

**ER-jj2 (round 18, 2026-10-20; append-only).** The line anchor `../scripts/hyaku/jj-lane.sh:53-65` in the ER-jj note above is stale: that range is the `usage()` help text, not the branch resolver. The resolver the note means is the function `detect_branch()` in `scripts/hyaku/jj-lane.sh` (fleet root); it returns a branch name (the attached HEAD's branch, else `origin/HEAD`), and the tip is still `refs/heads/<branch>`. Cite it by function name, not by line. This block corrects only the anchor: the reading rule above is unchanged and dated records are not re-interpreted.
