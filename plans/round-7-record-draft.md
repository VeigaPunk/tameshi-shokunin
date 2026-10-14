# Round-7 record draft — for the parent scribe to finalize (TAMESHI-SCR-T7)

Drafted 2026-10-14, poll window 18:20–18:51Z (15:20–15:51 local; assignment:
30-min cap) by the round-7 scribe-prep lane (SCR-T7). This file carries: **A**
the SCORECARD move-log rows, **B** the LOG.md round-7 entry text, **C** the
SCR-T7 evidence ledger, **D** landing status + parent checklist. Write-scope:
this file only; scratch `/tmp/w7-tameshi-scr-t7/` (poll log
`poll.log`, 31 samples, 60 s cadence; the poll task is `bash-cy0axytr`).

## Round-7 shape — planned vs realized

- **Planned** (`plans/round-7.plan.md`, 71 L, mtime 14:44; ufo-round-plan-v1):
  axis move **operability (post-service)** — three ordered legs: (1) the
  **leg ledger**, `--regression` replaying EVERY recorded case at its pinned
  revision, a case becoming a CONTRIBUTION (pinned file set) so a fleet lane
  can add one without a tameshi code edit; (2) the **fleet-run case** —
  mado's round-6 self-service sweep (`mado-shokunin/corpus/knowledge/
  gate-mutation-proof.md`) ATTESTED read-only, or its missing piece named;
  (3) the **queue** — at most ONE position drains, only under a fresh round-7
  opt-in naming a pinned target + a hermetic suite; no opt-in → the no-opt-in
  line is the record (default head surface-probe, `fleet-suite-census.md:282`).
  Measure: selftest green incl. the contributed-case path; `REGRESSION: PASS`
  over all embedded cases with per-case pins and `flips=0`; the attestation
  note; the queue record; SKILL append = the contribution + attestation
  contract; every quoted count carries its command.
- **Realized (observed, 18:20–18:51Z).** Legs **1 and 3 landed**; leg **2 was
  not executed by any lane** — T7-3's protocol note says so in its own bytes
  ("the attestation form is planned, not yet executed",
  `service-optin-protocol.md:260`, §7 U1); this lane reproduced mado's
  declared pins itself as a spot-check (§C.2) so the record carries the
  attestation's substance with its provenance stated. The plan's "cite-check r6
  if landed" resolved **negative** (cite-check stayed the 1/4 probe); the
  realized 4th leg is **mado r6** (`r7-aud-t7.md` records the same reading).
  Beyond the plan's list, three artifacts landed: the standing
  `fleet-kill-rate-ledger.md` (T7-2), the `service-optin-protocol.md` (T7-3),
  and an audit report `reports/r7-aud-t7.md` (AUD-T7) — plus
  `plans/round-8.plan.md` (next round's plan). The contributed-case path is
  **unexercised** ((U) in `SKILL.md`, and the ledger's case set is
  tameshi-carried): leg 1's contract is published, its first fleet contribution
  is not.

## 0. Landing status

### 0.1 Baseline at window open (tameshi tree; HEAD `4494715` = round-6 commit, tree clean)

Round 6 finalized 15:17:26 local as `4494715`; `git show --numstat` = LOG +1,
SCORECARD +1, SKILL +128/−1, census +290/−1, mado note +323, self-hardening
+262, r6-draft +349, r7-plan +72, tool +83/−4. The round-6 move landed as
**one combined stub row** — `| 6 | adjacency + operability | round-5 state |
the service round on mado's gate: 4/10 killed, in-surface 4/4 vs
out-of-surface 0/6 — the co-extensive assertion/kill finding | wave-6 32-lane
(2 lanes rerouted alibaba->hyper) |` — and **one terse LOG line**
(`LOG.md:305`); the full rows and long entry offered in
`plans/round-6-record-draft.md` §A/§B did not land. `corpus/README.md` carries
**no** coverage rows for `mutation-case-mado-verify.md` or
`self-hardening-r6.md` (round-6 checklist item unlanded, carried here).

Pins at open (all re-read by this lane): `LOG.md` 305 L / 22301 B /
`8e4194cc90f243e7…`; `SCORECARD.md` 19 L / 11506 B / `be2789969c190421…`;
`SKILL.md` 918 L / 62373 B / `137879dd174383ca…` (round-6 revision);
`tools/mutate-and-run.sh` 1080 L / 46850 B / `b56c6e57f1b7ae91…` (r6
revision); `plans/round-7.plan.md` 71 L / 4645 B / `49cd55fd0efaf892…`;
11 `corpus/knowledge/*.md` (pins in §C.1). Baseline pulse: `--selftest` →
`MUTATE_SELFTEST: 55/55 pass` / `VERDICT: PASS`, rc 0, 4.6 s; `--regression`
→ `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)`, rc 0,
18.0 s — the tool still embedded **two** cases at open (leg 1 unlanded).

### 0.2 Measured at window close (this lane, 2026-10-14 ~18:50Z)

- `tools/mutate-and-run.sh` **1341 L / 61632 B /
  `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`**,
  mtime 15:29:01, `git diff --numstat` **+337/−76** (uncommitted). Header
  `:8-14` names the leg ledger (git-materialized replay). Selftest
  **67/67** (r6: 55/55); `--regression` → 4 legs, per-leg
  `REGRESSION_TABLE … match=10/10 … flips=0`, closing
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0
  flips<=0)`, rc 0 (§C.2/§C.3; this lane's runs).
- `SKILL.md` **1007 L / 68019 B /
  `d36e9a28accdec970f903977e5b39dfdbe3b17175895558d31639beefad5e60d`**,
  `git diff --numstat` **+90/−1**; new section `SKILL.md:921` =
  `## The leg ledger — replay, receipt, and how it is read (round 7,
  measured)` — using the ledger, the contribution contract, the receipt-reading
  discipline (6 items + selftested arms) and the attestation rule.
- `corpus/knowledge/fleet-kill-rate-ledger.md` **269 L / 19781 B /
  `e08efe79bb58c85002c37db486a0b88ff85e51c5fb664a6c41f108839dc05cc5`**
  (T7-2; mtime 15:27:16; append-only errata ER-1 records the mid-round tool
  drift). Its §5/§6 pulse cells ("cases=2 at this write") are **pre-landing**
  and superseded by the 4-leg revision (§0.3).
- `corpus/knowledge/service-optin-protocol.md` **286 L / 17644 B /
  `84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e`**
  (T7-3; mtime 15:27:38) — the offer, the three engagement forms
  (self-service/service/**attestation: planned, not executed**), the request
  and report shapes, no-opt-in line at `:260-266`.
- `reports/r7-aud-t7.md` **173 L / 10896 B /
  `9a977e05adcb3f2e1f12f8b7d0ff0d9888c627ad8f741a957d775932307ad351`**
  (AUD-T7; mtime 15:40:44) — independent audit of the 4-leg ledger: 5/5 claims
  **CONFIRMED** (primary run 44.9 s, four `match=10/10 flips=0`, F1–F4
  fail-closed, no-write proof), verdicts bound to `cf41efaa` (§7 U2: a later
  edit needs re-audit).
- `plans/round-8.plan.md` **172 L / 11924 B /
  `7e53c9d89b4887a482816639c6678346e8ed500137eefbcae6cac8997cc0358e`**
  (mtime 15:30:48).
- `LOG.md` / `SCORECARD.md` **unchanged** — writing them is this draft's job.
  `git status` at close: `M SKILL.md`, `M tools/mutate-and-run.sh`, untracked
  `corpus/knowledge/{fleet-kill-rate-ledger,service-optin-protocol}.md`,
  `plans/round-8.plan.md`, `reports/`.

### 0.3 Corrections ledger — what moved during the window (append-only)

Recorded, not smoothed (round-6 precedent). No cell above was rewritten; each
row is the open-state → close-state pair.

| cell | at open / intermediate | at close | reading |
|---|---|---|---|
| tool revision | `b56c6e57…` 1080 L / 46850 B | 49360 B @15:26:45 → 61305 B @15:28:38 → **`cf41efaa…` 1341 L / 61632 B @15:29:01** | the leg-1 edit landed in three visible writes; every pulse before 15:29 measured the pre-ledger revision — cite the revision with every number |
| SKILL | `137879dd…` 918 L / 62373 B | 68017 B @15:34:32 → **`d36e9a28…` 1007 L / 68019 B @15:35:32** | the round-7 append; two writes, second one byte-final at close |
| knowledge files | 11 files | **13** (two new notes) | the ledger + protocol notes |
| regression cases | `cases=2` | **`cases=4`** | leg 1 landed; the 4th leg is mado r6 (cite-check r6 did not land) |
| in-flight sibling drift | — | T7-2's ledger ER-1 records the tool edit and a concurrent `tsukuroi-census.sh` working-tree move (`d666bba3…`, mtime 15:24:40) | the reference revisions stand; a future sweep must re-pin (their U-carry) |
| audit binding | — | `r7-aud-t7.md` §7 U2: verdicts bind to `cf41efaa`; a later edit needs re-audit | if the parent commits an edited tool, the audit row is stale by construction |

## A. SCORECARD.md — move-log rows (append after the round-6 row)

Precedent: rounds 4–5 and 6 landed as terse stubs; round 6 combined two axes in
one row. Round 7 is ONE move (operability), three legs — full row first, stub
form after.

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 7 | operability (post-service) | `--regression` re-ran TWO worked cases on the tool's own band (`597e1419…`/`b56c6e57…`; `cases=2`, fixture band killed-delta<=1 flips<=1); a case was a tameshi-carried table, not a portable contract; mado's r6 self-service proof (`gate-mutation-proof.md`) and the census queue stood as offers with no receipt/queue record; `SKILL.md` 918 L | the **leg ledger** landed: `--regression` replays **4 recorded cases at their pinned revisions**, materialized from each repo's git object store (`git show <rev>:<path>`, immune to working-tree drift; SETUP refusal on pin mismatch) — `js-kimi-census` (r2, 8/10), `bash-surface-census` (r3, 8/10), `bash-tsukuroi-census` (r5, 6/10), `bash-mado-verify` (r6, 4/10) — exact band (`killed-delta<=0 flips<=0`), every leg `match=10/10 flips=0`, `REGRESSION: PASS (cases=4 passed=4)`, rc 0, independently audited 5/5 CONFIRMED (`reports/r7-aud-t7.md`, bound to `cf41efaa…`); the **contribution contract** is published (`SKILL.md:921-1007`, +90/−1) — pinned file set + spec + one-command hermetic suite + recorded table as the leg's expectation — with the fleet-contributed case **unexercised** (U); the **standing receipt** `fleet-kill-rate-ledger.md` (269 L) carries one row per measured gate with composition, survivor classes and hardened-or-not, so kill-rate claims cite one file; the **protocol** `service-optin-protocol.md` (286 L) fixes the request/report shapes and both guarantees; the **queue did not drain** — no opt-in landed, so the no-opt-in line is the round's complete outcome (default head surface-probe, `fleet-suite-census.md:282`); **attestation leg not executed** — the scribe reproduced mado's declared pins itself (10/10 at `c4c1afb7…`, restore OK, tree clean), recorded as scribe-verified, not lane-delivered | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 (was 55/55); `bash tools/mutate-and-run.sh --regression --workdir /tmp/w7-tameshi-scr-t7/final/regr --keep` → `REGRESSION_PIN` ×4 (kumitate `175de6b`/`83016d45…`; kagi `fecee87`/`275d8294…`; tsukuroi `165307fe`/`084951be…`; mado `eead56b`/`d7edaab4…`), `REGRESSION_TABLE` ×4 `match=10/10 … flips=0`, `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0 (this lane); `git diff --numstat` → `337 76 tools/mutate-and-run.sh`, `90 1 SKILL.md`; `grep -n '^## The leg ledger' SKILL.md` → `:921`; ledger note `:41-48` four rows + `:85-88` embed status; protocol note `:260` "attestation form is planned, not yet executed"; census `sed -n '282p'` = the surface-probe row. Re-run 2026-10-14 (TAMESHI-SCR-T7) |

Stub form (rounds 4–6 convention):

```
| 7 | operability (post-service) | regression cases=2 (tool-owned, loose band) | 4-leg pinned ledger (git-materialized replay, exact band, cases=4 passed=4) + contribution contract in SKILL + standing kill-rate ledger + opt-in protocol; queue held (no opt-in); attestation leg carried | wave-7 32-lane + SCR-T7 re-run (selftest 67/67, regression 4/4) |
```

## B. LOG.md — round-7 entry (append as a new bullet after the round-6 entry)

- 2026-10-14 — round 7 (training r6): planned as a ufo-round-plan
  (`plans/round-7.plan.md`, ufo-round-plan-v1 — axis move **operability
  (post-service)**: the service's outputs pass to the fleet as instruments).
  Same dispatch shape as rounds 1–6 — lane write-scopes leave this LOG to the
  scribe; the lane deliverables in this repo ARE the wave record (observation;
  no `.ufo/waves/tameshi-r7-*` directory was seen).
  TAMESHI-T7-1 → `tools/mutate-and-run.sh` (1080 → **1341 L**, 46850 → 61632 B,
  `cf41efaa…`, `+337/−76`): `--regression` becomes the **leg ledger** — every
  recorded case replayed at its pinned revision, materialized from its repo's
  git object store (`git show <rev>:<path>`, so a drifted working tree cannot
  move a leg; pin mismatch / unresolvable revision = SETUP refusal before any
  suite runs). Four legs at exact band (ledger legs `killed-delta<=0 flips<=0`;
  the r4-2 fixture band stays selftest-only): js-kimi-census (r2, 8/10),
  bash-surface-census (r3, 8/10), bash-tsukuroi-census (r5, 6/10),
  bash-mado-verify (r6, 4/10) — `REGRESSION: PASS (cases=4 passed=4; ledger
  legs exact: killed-delta<=0 flips<=0)`, per-leg `match=10/10 flips=0`, rc 0;
  selftest 55/55 → **67/67** (the +12 are ledger-engine arms: git-materialized
  replay, drift immunity, pin mismatch/unresolvable rev SETUP, one flipped
  entry failing loudly). The plan's "cite-check r6 if landed" resolved
  negative — cite-check stayed the 1/4 probe and the 4th leg is mado r6.
  TAMESHI-T7-2 → `corpus/knowledge/fleet-kill-rate-ledger.md` (269 L,
  `e08efe79…`): the standing verification-health view — one row per gate with
  suite size at the sweep pin, composition-bound kill-rate, measured survivor
  classes, hardened-or-not, last sweep pin+driver (four measured: 80 % kimi r2,
  80 % kagi r3, 60 % tsukuroi r5, 40 % mado r6; two directed repairs 1/4 and
  6/6 → 100 % mado); the ten surveyed gates as the offer's queue with re-read
  pins; boundary unknown list U1–U9; append-only errata ER-1 recording the
  mid-round tool drift it observed (and a concurrent tsukuroi working-tree
  move — read-only observation, reference revisions stand).
  TAMESHI-T7-3 → `corpus/knowledge/service-optin-protocol.md` (286 L,
  `84d0c154…`): the opt-in protocol behind the standing offer — the three
  engagement forms (self-service = r5 tsukuroi, service = r6 mado, attestation
  = planned, **not yet executed**), the request shape (pinned revision,
  one-command hermetic suite exercising the copy, clause-mapped spec), the
  read-only guarantees (substrate never written; the owner stays the owner),
  the report shape, unknowns U1–U6, and the no-opt-in line as the standing
  record.
  SKILL round-7 append → `SKILL.md` (918 → **1007 L**, `+90/−1`, sha
  `d36e9a28…`): `## The leg ledger — replay, receipt, and how it is read
  (round 7, measured)` (`:921`) — using the ledger, the contribution contract
  (what a case must carry to become a leg; the fleet-contributed case stays
  (U)), receipt-reading discipline (read the block not the last line; PASS is
  exact for ledger legs; FAIL names its rows; SETUP is not a verdict; the
  ledger proves the instrument, not the gates; attesting a sibling's claim uses
  the same discipline), and the selftested arms.
  AUD-T7 (audit lane, read-only) → `reports/r7-aud-t7.md` (173 L, `9a977e05…`):
  independent audit of the 4-leg ledger at `cf41efaa…` — 5/5 claims CONFIRMED
  (primary run rc 0, 44.9 s, four `match=10/10 flips=0`; each leg's pin
  re-derived from `git show` = `cat-file` = pin; worktree-drift immunity
  demonstrated on legs 3/4 plus a decoyed-worktree fixture; F1–F4 fail-closed
  exits 2/2/0/1; no fleet file written), verdicts append-only bound to the
  audited sha (U2: a later edit needs re-audit).
  **Queue (leg 3): no opt-in landed** — the protocol note's own bytes carry it
  (`:260-266`) — so the no-opt-in line is the round's complete outcome; the
  default head remains surface-probe (`fleet-suite-census.md:282`) and the
  standing record is the ledger's §3 queue. No position was forced.
  **Attestation (leg 2): not executed by a lane** (protocol §7 U1); the scribe
  lane reproduced mado's declared self-service pins read-only itself — spec
  `c7ee75b9…` (byte copy of the r6 spec), hardened gate `c4c1afb7…` (1186 L /
  50126 B), through the r6 harness `b56c6e57…`: `CONTROL: GREEN` +
  `MADO_SELFTEST: 53/53`, D1–D9 R1 all KILLED, `MUTATE_RESTORE: OK` before=after
  = `c4c1afb7…`, `MUTATE: DONE (… killed=10 survived=0 inconclusive=0
  kill-rate=100%)`, mado tree porcelain-clean before/after — recorded as
  **scribe-verified**, the sibling note left read-only and unedited.
  Scribe verification (this draft, TAMESHI-SCR-T7; scratch
  `/tmp/w7-tameshi-scr-t7/`): baseline pulse at open (selftest 55/55;
  regression `cases=2` PASS) and at close (`--selftest` → 67/67; `--regression`
  → 4/4 exact, rc 0, this lane's own runs, evidence
  `/tmp/w7-tameshi-scr-t7/final/regr`); pins re-read for every quoted cell
  (§C); round-6 landed form re-read (SCORECARD combined stub row, `LOG.md:305`).
  SCORECARD round-7 move: operability improved (regression → 4-leg pinned
  ledger with git-materialized replay and the contribution contract published,
  independently audited; the fleet's kill-rate claims gain one standing
  receipt; the opt-in protocol is fixed in writing) — the fleet-facing half of
  the move is **published, not yet exercised**: no fleet-contributed case, no
  opt-in, no executed attestation.
  Carried to round 8 (recommendations, not absorbed): the attestation leg
  (planned, unexecuted — `service-optin-protocol.md` §7 U1); the
  fleet-contributed case path (U in `SKILL.md`; the ledger's case set is
  tameshi-carried); cite-check's full sweep (probe 1/4 only; queue head,
  unclaimed); the round-6 carries still open (README coverage rows for
  `mutation-case-mado-verify.md` + `self-hardening-r6.md`; audit-verdict
  freshness if the tool is edited after `cf41efaa…`); T7-2's U1–U9 and T7-3's
  U1–U6; mado's and tsukuroi's residual hardening items stay owner-owned.

## C. SCR-T7 evidence ledger (measured by this lane 2026-10-14; scratch `/tmp/w7-tameshi-scr-t7/`)

1. **Baseline pins re-read** (tameshi, HEAD `4494715`, tree clean):
   `LOG.md` 305 L / 22301 B / `8e4194cc90f243e77c77efc333c50467…`;
   `SCORECARD.md` 19 L / 11506 B / `be2789969c1904214a4a0bfa61ad1c6e…`;
   `SKILL.md` 918 L / 62373 B / `137879dd174383ca…`;
   `tools/mutate-and-run.sh` 1080 L / 46850 B / `b56c6e57f1b7ae91…`;
   `plans/round-7.plan.md` 71 L / 4645 B / `49cd55fd0efaf892…`;
   11 `corpus/knowledge/*.md` (arm-class-matrix 524 L `63187323…`;
   executor-test-sufficiency 211 L `b2602129…`; fleet-suite-census 674 L
   `ec1c2d8d…`; gates-survey-kagi 619 L `4734f0a0…`; gates-survey-kumitate
   382 L `3dca7a1a…`; mutation-case-kagi-census 258 L `0d5dc3cd…`;
   mutation-case-kimi-census 237 L `034524ef…`; mutation-case-mado-verify
   323 L `f2d53d49…`; mutation-case-tsukuroi-census 396 L `b431bc6c…`;
   self-hardening-r6 261 L `f2c347ac…`; verification-patterns-fleet 306 L
   `bbf04a5e…`). Round-6 landed form: `git show --numstat 4494715`;
   `SCORECARD.md` round-6 row (combined stub) and `LOG.md:305` re-read.
2. **Baseline pulse (open).** `bash tools/mutate-and-run.sh --selftest` →
   `MUTATE_SELFTEST: 55/55 pass` / `VERDICT: PASS`, rc 0, 4.6 s;
   `--regression --workdir /tmp/w7-tameshi-scr-t7/regression` →
   `REGRESSION_CASE bash-surface-census: PASS (band: killed-delta<=1 flips<=1
   inconclusive=0 defects=10)`; `REGRESSION: PASS (cases=2 passed=2; band
   killed-delta<=1 flips<=1)`, rc 0, 18.0 s. Tool's embedded case registry at
   open: `:738` js-kimi-census, `:743` bash-surface-census (2 cases).
3. **Close pulse (this lane's independent runs).** `--selftest` →
   `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0, 4.9 s.
   `--regression --workdir /tmp/w7-tameshi-scr-t7/final/regr --keep` →
   `REGRESSION_TOOL: … sha256=cf41efaa…bce37242c75`;
   `REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10
   bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10`;
   `REGRESSION_PIN` ×4 — kumitate `175de6ba…`/`83016d45…f2724f426`, kagi
   `fecee874…`/`275d8294…db53009f`, tsukuroi `165307fe…`/`084951be…c5809c78c5`,
   mado `eead56b2…`/`d7edaab4…32d0e13`; `REGRESSION_TABLE` ×4 `match=10/10
   recorded-killed=8/8/6/4 measured-killed=8/8/6/4 survived=2/2/4/6
   inconclusive=0 flips=0`; `REGRESSION_CASE` ×4 `PASS (band: killed-delta<=0
   flips<=0 inconclusive=0 defects=10)`; `REGRESSION: PASS (cases=4 passed=4;
   ledger legs exact: killed-delta<=0 flips<=0)`, rc 0.
4. **Attestation reproduction from mado's declared pins (this lane,
   read-only).** Spec = `/tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec`,
   sha256 `c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8`
   (= the sha mado's note names, `gate-mutation-proof.md:36-38`). Target =
   live `mado-shokunin/tools/mado-verify.sh` `c4c1afb75dd1c8aa…` (1186 L /
   50126 B; committed HEAD blob = live, tree clean). Harness = r6 revision
   `b56c6e57…`. Readings: `CONTROL: GREEN (exit=0 duration-ms=1017
   pristine-sha256=c4c1afb7…)` + `MADO_SELFTEST: 53/53 assertions passed`;
   D1·D2·D3·D4·D5·D6·D7·D8·D9·R1 **KILLED** (D2 6 failing asserts, D4 5, D7 4,
   D9 4, rest 1 each); `MUTATE_RESTORE: OK (target-sha256 before=c4c1afb7…
   after=c4c1afb7… pristine-sha256=c4c1afb7…)`; `MUTATE: DONE
   (target=mado-verify-hardened defects=10 killed=10 survived=0
   inconclusive=0 kill-rate=100%)`, rc 0, 12.2 s; mado
   `git status --porcelain` empty before and after. Reading: mado's declared
   proof reproduces from its pins under a tameshi harness; the attestation leg
   as a lane deliverable remains unexecuted (T7-3 §7 U1).
5. **Anchor re-reads for the record's citations.** `sed -n '282p'
   corpus/knowledge/fleet-suite-census.md` → the surface-probe row (default
   queue head; contract §5 at `:249-291`); `sed -n '776,792p' SKILL.md` → the
   four-case falsifier list ("What a fourth case would need to show", 6 items);
   `sed -n '66,81p' tools/mutate-and-run.sh` → the r4-2 regression contract text
   (both worked cases, pins, band); `grep -n '^## The leg ledger' SKILL.md` →
   `:921`; `grep -n 'PIN_TSUKUROI\|PIN_MADO' tools/mutate-and-run.sh` → `:515`
   / `:517`; ledger note rows `:45-48` (four gates) and embed-status `:85-88`;
   protocol note `:260` (attestation planned, not executed) and `:266`
   (no-opt-in line).
6. **Round-6 landed form (for the "before" column).** `git show --numstat
   4494715` (§0.1); `sed -n '305p' LOG.md` → the one-line round-6 entry;
   `grep -n 'mutation-case-mado-verify\|self-hardening-r6' corpus/README.md` →
   no matches (coverage rows unlanded); `SHONEN.md` unchanged since round 3.
7. **Cross-lane observations (read-only; not this lane's evidence of fact).**
   T7-1/T7-2/T7-4 scratch (`/tmp/w7-tameshi-1-pins`, `-t72`, `-t7-4-work`)
   visible in flight; AUD-T7's report carries its own frozen copies
   (`/tmp/w7-aud-t7-work/tool-cf41efaa.sh`, byte-identical at freeze and write
   time) and its no-write proof. The tool's revision is uncommitted at this
   draft's close; every quoted cell names the revision it was measured at.

**Spot-checks (three, all run this session).**

- **SC1 — the pulse pair (open vs close).** Opened at `b56c6e57…`:
  selftest 55/55, regression `cases=2` PASS (fixture band). Closed at
  `cf41efaa…`: selftest 67/67, regression `cases=4 passed=4` (exact band), both
  rc 0 and both re-run independently by this lane (§C.2/§C.3) — the ledger's
  landing is visible in the tool's own counters, not only in prose.
- **SC2 — the attestation reproduction.** Mado's declared proof re-cut from its
  own pinned bytes under tameshi's harness: 10/10 killed, 53/53 self-asserts,
  restore OK before=after=`c4c1afb7…`, mado tree clean before/after (§C.4) —
  and the D2/D4/D7/D9 failing-assert counts match the numbers mado's note
  tabulates (`gate-mutation-proof.md` §1 table).
- **SC3 — the record's cells against the files.** Every pin in §0.2 re-read at
  close: tool `cf41efaa…` 1341 L / 61632 B (+337/−76), SKILL `d36e9a28…`
  1007 L / 68019 B (+90/−1), ledger `e08efe79…` 269 L, protocol `84d0c154…`
  286 L, audit `9a977e05…` 173 L, round-8 plan `7e53c9d8…` 172 L; LOG/SCORECARD
  still `8e4194cc…` / `be278996…` (§C.1, §0.2).

## D. Parent checklist (round close)

- **Honesty item 1 — the tool revision moves.** Every cell ties to a revision:
  open pulse `b56c6e57…` (r6), close pulse and ledger leg `cf41efaa…` (r7-1,
  uncommitted). AUD-T7 §7 U2: verdicts bind to `cf41efaa`; if the parent (or a
  later lane) edits the tool before commit, re-run `--selftest`/`--regression`
  and re-audit before quoting the audit row.
- **Honesty item 2 — leg 2 was carried, not executed.** "Attestation form is
  planned, not yet executed" (`service-optin-protocol.md:260`). The record may
  state the scribe's reproduction (§C.4) as scribe-verified; it must not be
  rendered as a lane-delivered attestation, and the sibling note stays
  read-only (`gate-mutation-proof.md`, landed at 167 L / `716836ca…` — its §5
  asks downstream records to cite the hardened pin).
- **Honesty item 3 — the fleet-facing half is published, not exercised.** No
  fleet-contributed case ((U) in `SKILL.md`), no opt-in (no-opt-in line), no
  executed attestation. The round's complete outcome for leg 3 is exactly the
  no-opt-in line; nothing was forced. The realized 4th leg is mado r6, not
  cite-check (plan's "if landed" resolved negative — say so).
- **Cross-lane numbers to reconcile at close.** T7-2's ledger §5/§6 pulse says
  `cases=2` and tool `b56c6e57…` (its own ER-1 already flags the drift); T7-3's
  note ties its SKILL line refs to the r6 revision (`:806-825`, `:883-889`) —
  the round-7 append begins at `:921`, so those refs still resolve to r6 text
  but the file sha is now `d36e9a28…`. Re-pin before quoting (their E2).
- **Commit items** (lane identity + round shape; precedents `2587e0a`,
  `53e74a8`, `b58b26f`, `e0c453e`, `4494715`): `tools/mutate-and-run.sh`
  (+337/−76); `SKILL.md` (+90/−1); `corpus/knowledge/fleet-kill-rate-ledger.md`;
  `corpus/knowledge/service-optin-protocol.md`; `reports/r7-aud-t7.md`;
  `plans/round-8.plan.md`; the round-7 record draft itself — precedent says the
  draft IS committed (`4494715` lists `plans/round-6-record-draft.md`); each
  round commit also carries `LOG.md` +1 and `SCORECARD.md` +1 (not yet written —
  that is this draft's purpose). The sibling-side files stay siblings'
  (tsukuroi's working-tree edit `d666bba3…`, mado's note edits, both owner
  lanes).
- **Row convention**: round 7 is one axis (operability) with three legs; §A
  offers a full row and a stub. Rounds 4–6 landed stubs; decide the form and
  record either way.
- **Coverage-map rows** (`corpus/README.md`): add rows for
  `fleet-kill-rate-ledger.md`, `service-optin-protocol.md`, and (still open
  from round 6) `mutation-case-mado-verify.md`, `self-hardening-r6.md`; the
  round-5 carries (arm-class-matrix, fleet-suite-census, tsukuroi-census rows;
  SKILL row revision) remain open.
- **Unlanded items to watch in round 8**: the attestation leg; the
  fleet-contributed case; cite-check's full sweep (queue head, unclaimed);
  a third adopting lane (T7-3 U2); README rows; audit freshness after any tool
  edit; T7-2's U1–U9 (incl. its U9: the ledger's update cadence is a
  convention, not a mechanism) and T7-3's U1–U6.
- **Shared scratch**: `/tmp/w7-tameshi-*` namespaces seen across lanes
  (`-1-pins`, `-t72`, `-t7-4-work`, `-scr-t7`); if another round sweeps the
  same gates, namespace per run (round-6 U4 precedent).
