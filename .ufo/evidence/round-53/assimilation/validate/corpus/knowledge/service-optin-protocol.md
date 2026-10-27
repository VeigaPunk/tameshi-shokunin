# Service opt-in protocol — how a fleet lane engages tameshi's mutation sweep (T7-3)

Written 2026-10-14, tameshi round 7 (training), lane T7-3. Anchors: **O** =
observation (command output / file:line, re-quoted measured cell); **I** =
inference; **U** = unknown. This note is the fleet-facing protocol behind the
standing offer: what a lane brings (request shape), what stays untouched
(read-only guarantees), who absorbs (owner-hardens discipline), and what comes
back (report shape). It is distilled from the two measured engagements — one
per mode — and restates the method-side rendering at `SKILL.md:794-919` and
the offer itself at `corpus/knowledge/fleet-suite-census.md:249-291`.

This lane wrote only this file; mado and tsukuroi trees were read-only (pins
re-read 2026-10-14; tameshi HEAD `4494715`, mado HEAD `c8f6667`, tsukuroi HEAD
`dc3436d` — all three `git status --porcelain` clean at the read).

## 0. The offer, and the three engagement forms

The offer (O, `fleet-suite-census.md:269-275`): any lane may ask for a sweep
of one of its gates; the sweep needs a pinned revision and a hermetic suite
invocable on a copy, and returns a kill-rate table, per-defect verdicts with
failing-case labels, survivor non-equivalence evidence, and a restore proof —
as a corpus note plus a recommendation; absorption stays with the gate's
owner (`PROVINCE.md:14-18`). Scope, stated so it is not over-claimed (O,
`fleet-suite-census.md:288-291`): single-edit mutants only; hermetic suites
only; results are per-revision and per-host. The queue
(`fleet-suite-census.md:277-286`) is an offer, not a schedule: at round-7
dispatch it drains only under a fresh opt-in naming a pinned target + a
hermetic suite, the standing default head is surface-probe, and a round with
no opt-in records the no-opt-in line as its complete outcome
(`plans/round-7.plan.md:16-20`).

Three forms have been used or named (the first two measured):

| form | who runs the harness | who hardens | measured instance |
|---|---|---|---|
| **self-service** | the opting-in lane, on /tmp copies | the same lane, in-round | tsukuroi r5 (`tsukuroi-shokunin/plans/round-5.plan.md:3-11`) |
| **service** | tameshi, for the opted-in lane | the owner lane, after the note | mado r6 (`mado-shokunin/plans/round-6.plan.md:8-26`) |
| **attestation** | tameshi, from the owner's recorded pins (or names the missing piece) | owner stays owner; the sister note stays read-only | planned, in flight at this write (`plans/round-7.plan.md:11-15`) |

- **Self-service fit check (O).** The harness's suite contract is `bash -c
  CMD` with `$MUTANT` = the artifact under test; exit 0 = green, non-zero =
  red, 124/126/127 = inconclusive. A bash gate whose `--selftest` prints its
  own case count and an rc 0/1 verdict satisfies it — tsukuroi's plan
  pre-registered the fallback ("run the mutation manually per tameshi's
  published recipe") and the record resolved it as **fit, not gap**
  (`tsukuroi-shokunin/plans/round-5.plan.md:3-11`,
  `tsukuroi-shokunin/SKILL.md:558-568`).
- **Two seats, never merged (O).** When both tameshi and the owner sweep the
  same artifact, the two tables stay two tables, each tied to its own pin;
  the record cites the other only as cross-reference
  (`tsukuroi-shokunin/plans/round-5-record-draft.md:70-79`; tameshi's own
  independent case on the same bytes: `corpus/knowledge/mutation-case-tsukuroi-census.md`).

## 1. Request shape — what the opting-in lane brings

The contract items (O, `SKILL.md:806-825`, with mado's run as the worked
instance):

1. **A pinned revision** — committed bytes of the gate: sha256, size, line
   count, mtime, porcelain-clean sibling tree at open. Mado's pin
   `d7edaab4…d0e13`, 45334 B, 1098 newlines. A moved substrate needs a
   re-pin, never a re-interpretation of the old table.
2. **A one-command hermetic suite** invocable against a copy — mado's gate
   takes `bash "$MUTANT" --selftest`; it exercises the copy it is handed
   (re-enters `$0`), prints its own executed count and verdict (`MADO_SELFTEST:
   28/28 assertions passed` on green), and reads no live path
   (`corpus/knowledge/mutation-case-mado-verify.md:44-49`).
3. **A clause-mapped defect spec** — one single-edit defect per declared
   contract clause, expectations pre-registered `killed|survived`. Mado's: 10
   defects over six clauses (A verdict token · B UNKNOWN-never-CLEAN · C exit
   map · D declared-plane census · E sha comparison · F reader fallback); the
   plan asked for ≥8 (`mado-shokunin/plans/round-6.plan.md:8-26`). The tool
   asserts every `@old` occurs exactly once **before any suite run** and
   refuses a no-op edit (`SKILL.md:838-852`).
4. **Nothing else.** The service never edits, repairs or re-pins the gate; a
   needed change is a recommendation to the owner, not a patch
   (`SKILL.md:823-825`).

Locally binding riders from the two runs:

- **Mode + records named up front.** Mado's plan named the target, the suite
  line, the ≥8-defect floor, the evidence path
  (`corpus/knowledge/gate-mutation-proof.md`), and the SETUP refusal
  semantics before any run — a red control, an unrunnable suite, or target
  drift is exit 2 with no headline (`mado-shokunin/plans/round-6.plan.md:8-26`).
- **Scratch namespace per lane.** Every write is lane-scoped (round-7
  convention `/tmp/w7-<lane>-*`). A suite with shared fixture scratch is an
  incident, not a licence: the mado run saw ≥37 foreign
  `/tmp/w5-mado-m52-selftest.*` directories, kept exactly its own 8, and
  removed exactly those paths
  (`corpus/knowledge/mutation-case-mado-verify.md:24-29`).
- **The note is the only fleet file the run writes.** Owner-side records
  (acceptance, hardening) are separate files written by the owner's lane
  (`corpus/knowledge/mutation-case-mado-verify.md:8-9`; mado's own
  `mado-shokunin/corpus/knowledge/gate-mutation-proof.md`).

Request template (fill into the lane's own plan or the dispatch note):

```
mode:       service | self-service | attestation
target:     <path> @ sha256 <…>, <B> B, <n> lines, mtime <…>; tree porcelain-clean at open
suite:      <one command with "$MUTANT">; prints own count + verdict; hermetic (no live path)
spec:       <n> single-edit defects, one per clause <A…>; @old uniqueness asserted; expect: pre-registered
evidence:   <corpus note path>   (the only fleet file the run writes)
scratch:    /tmp/w7-<lane>-*     (lane-scoped; foreign scratch never removed)
absorption: owner lane hardens + accepts; the service side is recommendations-only
```

## 2. Read-only guarantees — and what is provable

Both modes bind to the same guarantees; the record keeps the provable
negative, never a stability claim it cannot make.

- **The target is never a write target.** The harness copies the target to a
  pinned pristine, cuts every mutant from a fresh byte copy, and restores by
  sha — `MUTATE_RESTORE: OK` (sha256 before = after) is part of every run
  (mado: before=after=`d7edaab4…`; tsukuroi: before=after=`084951be…`).
- **The sibling tree stays clean.** `git status --porcelain` on the target's
  repo, before and after. What this proves is the negative — "this lane's
  writes never touched the gate" — not the positive "the bytes were stable":
  when a concurrent lane edits its own gate mid-run, the pin moves and the
  record keeps both pins, the frozen copy's sha, and the write-fencing
  evidence (tsukuroi incident I1,
  `corpus/knowledge/mutation-case-tsukuroi-census.md:9-35`).
- **The harness itself is pinned per run.** Every log carries its own
  `MUTATE_TOOL` sha256; a mid-round tool move is an incident recorded, not
  smoothed (mado run executed `597e1419…`, re-pin `b56c6e57…`,
  `corpus/knowledge/mutation-case-mado-verify.md:17-23`).
- **No live substrate read.** Hermetic suites by construction; where a probe
  needs a live-plane branch it is a PATH-level stub, never the session (mado:
  "no live substrate read — every live-plane probe binary used in §2 was a
  local stub, never the session", `mutation-case-mado-verify.md:8-11`).
- **Writes confined to scratch + the note.** The mado run's entire evidence
  tree lives under `/tmp/w6-tameshi-mado-verify/`; the fleet holds only the
  note (`mutation-case-mado-verify.md:262-277`).

Not claimed by any of this (O, `SKILL.md:858-881`;
`fleet-suite-census.md:288-291`): substrate-drift or cross-host stability;
coordinated multi-edit behavior; gate truth — a sweep measures what the
suite can detect, never whether the gate's verdicts are right.

## 3. Owner-hardens discipline — absorption stays with the owner

- **Rule 1 — recommendations only.** The service's output is a ranked
  recommendation list, each item naming the swept mutant it would kill
  (measured evidence, not opinion), plus named unknowns; acceptance is the
  owner's decision (`mutation-case-mado-verify.md:240-260`;
  `PROVINCE.md:14-18`).
- **Rule 2 — the owner hardens, with a ledger.** One new selftest case per
  survivor class, landed in the owner's own tree, mapped survivor → case
  label → added line → executed count (tsukuroi's shape: 9 new cases,
  D14+D15 die to one class-counts case, 26 → 35, block
  `tsukuroi-shokunin/tools/tsukuroi-census.sh:915-970`; ledger skeleton
  `tsukuroi-shokunin/plans/round-5-record-draft.md:316-319`).
- **Rule 3 — closure is proven by re-running the spec.** The owner re-cuts
  the same defect spec against the hardened revision and quotes the rate
  before → after: tsukuroi 13/23 (56.5 %; tool prints 57 %) → **23/23
  (100 %)** at `aae45531` (`tsukuroi-shokunin/SKILL.md:599-609`); mado
  4/10 (40 %) → **10/10 (100 %)** at `c4c1afb7…`
  (`mado-shokunin/corpus/knowledge/gate-mutation-proof.md:31-49`). A re-run
  proves the hardened suite kills *that* spec; it is not a general rate.
- **Rule 4 — hardening closes what it covers; a replay names what remains.**
  Tameshi's independent replay of its four tsukuroi survivors against the
  hardened revision found one closed (B10, PCI-unreadable) and three still
  open (B7 default-cap site, B8 usage parser, B9 roll fields)
  (`corpus/knowledge/mutation-case-tsukuroi-census.md:306-321`). Mado's
  residuals stay recorded unabsorbed: the dead rc-6 arm, the exit-flatten
  family (a harness boundary — exit-only adjudication), and the 51
  live-plane row sites
  (`mado-shokunin/corpus/knowledge/gate-mutation-proof.md:103-129`).
- **Rule 5 — no acceptance means recorded unabsorbed.** The anti-claim is
  explicit: nothing is forced, and an unabsorbed recommendation is a
  complete, honest record (`plans/round-6.plan.md:23-25`). Mado's case is the
  positive instance: the owner accepted, and the round record folds the
  acceptance in as the owner's own measured work
  (`plans/round-6-record-draft.md:107`).
- **Rule 6 — harden the boundary classes, not just the survivors.** Tameshi's
  own-tool meta-sweep recommends adding boundary, absent-row, DEGRADED-rc and
  asymmetric-table cases before a kill rate is published
  (`corpus/knowledge/self-hardening-r6.md:186-192`).

## 4. Report shape — what the opting-in lane receives

O, `SKILL.md:883-897`, worked instance `mutation-case-mado-verify.md`:

- **pins**: target sha256/size/lines, tool sha256, suite command + control
  line, spec clause map;
- **the kill-rate table**: control row + one row per defect (id, clause,
  exact edit site, exit, verdict, failing-case labels for kills, verbatim
  from `evidence/<id>.out`);
- **survivor non-equivalence probes**: each survivor re-run on an input
  outside the suite's fixtures, pristine vs mutant outputs recorded (mado:
  six probes, `mutation-case-mado-verify.md:103-115`);
- **restore proof** `MUTATE_RESTORE: OK` (sha before = after) + the
  tree-clean check;
- **recommendation + named unknowns**, as a corpus note; the note is the only
  fleet file the run writes, and its reproduce block rebuilds the sweep.

Adjudication rules kept fleet-wide (O, `tsukuroi-shokunin/SKILL.md:611-617`):
killed = suite red **and** the full case count still enumerated (exit-only is
insufficient); survived = green at the same count; inconclusive (timeout 124 /
126-127 not runnable) is excluded from the rate and named beside it;
`kill-rate = killed/(killed+survived)`; bands are a report convention, not a
gate.

Two conventions that make a table quotable later:

- **Pre-register the expected table.** Mado's sweep wrote its predictions
  before the run and held 10/10 on verdicts and 4/4 on the named kill
  mechanisms (`corpus/knowledge/mutation-case-mado-verify.md:73, :185-189`);
  tsukuroi held 10/10 on failing-case counts
  (`corpus/knowledge/mutation-case-tsukuroi-census.md:283-288`).
- **Record composition beside the rate.** A rate without its composition
  (kill-aimed vs hole-aimed defects) is not comparable across authors — mado's
  40 % is 4 in-surface (4/4) + 6 out-of-surface (0/6), read as a co-extensive
  suite, not a regression (band amendment,
  `corpus/knowledge/mutation-case-tsukuroi-census.md:296-300`;
  `corpus/knowledge/mutation-case-mado-verify.md:66-72`).

## 5. The two precedent runs at a glance (O unless marked)

| | tsukuroi r5 — self-service | mado r6 — service |
|---|---|---|
| opt-in recorded in | tsukuroi's own plan (`tsukuroi-shokunin/plans/round-5.plan.md:3-11`) | mado's own plan §(a) (`mado-shokunin/plans/round-6.plan.md:8-26`) |
| tool pin (executed) | r4-2 `597e1419…331b`, md5 `26a27d35…` | `597e1419…ff6331b`; re-pin `b56c6e57…` mid-round (I1) |
| target, swept | `tsukuroi-census.sh` `084951be…`, 976 L, 44 947 B | `mado-verify.sh` `d7edaab4…`, 1098 L, 45 334 B |
| suite | `bash "$MUTANT" --selftest` (26 cases) | `bash "$MUTANT" --selftest` (28 assertions) |
| defects → verdicts | 23 → 13 killed / 10 survived (56.5 %; printed 57 %) | 10 → 4 killed / 6 survived (40 %) |
| restore | `MUTATE_RESTORE: OK`, before=after=`084951be…` | OK, before=after=`d7edaab4…`; tree untouched |
| owner hardening | 9 cases, 26 → 35; spec re-run **23/23** at `aae45531…` | six survivor→case mappings (4 new scenarios E/F/H/I + 2 asserts folded into A), 28 → 53 (`+88/−0`, inside `selftest()` only); spec re-run **10/10** at `c4c1afb7…` |
| residue kept | B7/B8/B9 still open at `aae45531` (tameshi replay §6) | rc-6 dead arm; exit-flatten family; 51 live rows |
| second seat | tameshi's independent case on the same bytes: 6/10 (60 %); I1 gate moved mid-run | SCR-T6 re-ran the spec under `b56c6e57…`: 4/10, all ten mutant shas identical |

Cross-check receipts: tsukuroi's sweep headline and hardening block are quoted
in §6; the mado spec's independent re-run under the hardened tool reproduced
the table and all ten mutant sha prefixes
(`plans/round-6-record-draft.md:243-262`).

## 6. Spot-checks (three, re-run 2026-10-14 on the live bytes)

- **SC1 — the service-mode closure line.** `sed -n '43,48p'
  mado-shokunin/corpus/knowledge/gate-mutation-proof.md` → `CONTROL: GREEN
  (exit=0 …)` + `MADO_SELFTEST: 53/53 assertions passed`,
  `**Headline: killed 10 / survived 0 / inconclusive 0 — kill-rate 100 %**`,
  `MUTATE_RESTORE: OK (target-sha256 before=c4c1afb7…a5171 after=c4c1afb7…a5171 …)`.
- **SC2 — the self-service headline + hardening block.** `sed -n '578p'
  tsukuroi-shokunin/SKILL.md` → `MUTATE: DONE (target=tsukuroi-census-census-v2
  defects=23 killed=13 survived=10 inconclusive=0 kill-rate=57%)`;
  `sed -n '915,920p' tsukuroi-shokunin/tools/tsukuroi-census.sh` → the
  hardening block comment naming `tameshi's mutate-and-run.sh, 23 single-edit
  defects, first pass 13 killed / 10 survived` and the D02…D20 label map.
- **SC3 — the contract this note restates.** `sed -n '806,812p'` and
  `sed -n '883,889p' tameshi-shokunin/SKILL.md` → the opt-in contract's item 1
  (pinned revision, mado's pin verbatim) and the report shape's pins +
  kill-rate-table bullets; both restatements above match byte-for-byte.

## 7. Unknowns

- **U1** — two measured engagement instances (one per mode) bound this
  protocol; the attestation form is planned, not yet executed
  (`plans/round-7.plan.md:11-15`).
- **U2** — no third-lane adoption: the protocol has not yet been exercised by
  a lane that did not write it or the census.
- **U3** — the dispatch hand-off (how an opt-in reaches the service between
  waves, with no tameshi lane live) is unmeasured; the standing record is the
  no-opt-in line.
- **U4** — a harness that adjudicates by exit code alone cannot kill the
  exit-flatten family; a stdout-reading harness is a named future, not a
  measurement (`mado-shokunin/corpus/knowledge/gate-mutation-proof.md:103-118`).
- **U5** — host/toolchain gating: all runs single-host (bash 5.3.15,
  python 3.14.7, Linux 7.2.3-arch1-3, 2026-10-14); the PATH-stub mechanisms
  may behave differently under other shells.
- **U6** — whether hardened rates hold across future spec extensions is
  answered only for the two revision pairs re-swept above.

## 8. Errata (append-only)

- **E1 — mado's proof note landed at 167 L.** The round-6 record draft read
  it at 168 L (`plans/round-6-record-draft.md:88`); at this note's write it
  is 167 L / sha256 `716836ca…`. Re-pin before quoting (its own §5
  instruction, `mado-shokunin/corpus/knowledge/gate-mutation-proof.md:145-153`);
  the cells above are line-cited, not length-cited.
- **E2 — tool revision citations.** Tameshi-side line refs in this note are
  the round-6 commit (`4494715`, `SKILL.md` `137879dd…`); earlier notes tied
  to `597e1419…` remain valid for their own numbers under their own recorded
  incident (their I1).
