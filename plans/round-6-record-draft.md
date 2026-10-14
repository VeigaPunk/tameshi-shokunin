# Round-6 record draft — for the parent scribe to finalize (TAMESHI-SCR-T6)

Drafted 2026-10-14, poll window 14:38–15:08 (assignment: 30-min cap) by the
round-6 scribe-prep lane (SCR-T6). This file carries: **A** the SCORECARD
move-log rows, **B** the LOG.md round-6 entry text, **C** the SCR-T6 evidence
ledger, **D** landing status + parent checklist. Write-scope: this file only;
scratch `/tmp/w6-tameshi-scr-t6/`.

**Round-6 shape — planned vs realized.**

- **Planned** (`plans/round-6.plan.md`, 34 L, mtime 14:08; ufo-round-plan-v1):
  axis move **adjacency** — the method ships as the SERVICE offered in the
  round-5 fleet census (`corpus/knowledge/fleet-suite-census.md` §5 queue) to
  a lane that opts in; the census's expected-yield ordering (cite-check first)
  itself under test; `--regression` becomes the fleet-facing kill-rate
  regression gate, embedding the round-5 tsukuroi case and this engagement's
  case at their pinned revisions, every kill-rate claim from round 6 carrying
  `REGRESSION: PASS`. Anti-claims: read-only regardless of opt-in; no
  acceptance → recorded unabsorbed; integration group stays a declared skip;
  a sweep contradicting the probe or a kill-rate that breaks the census
  ordering is the finding, recorded not smoothed.
- **Realized (observed, 14:38–15:08).** The engagement that materialized is
  **mado's** opt-in (`mado-verify.sh`), not the census queue head
  (cite-check); cite-check keeps only the round-5-tail PREP-T6 feasibility
  probe (1/4 killed) plus the scribe's re-measurement. The `--regression`
  embedding of tsukuroi + cite-check did **not** land (working tool still
  embeds only js-kimi-census + bash-surface-census; the round-7 plan carries
  the embedding as its own leg 1, quoting `plans/round-6.plan.md:20-22` as the
  unlanded claim). What DID move beyond the plan: a **harness self-hardening**
  (T6-4) — mutant coverage of the `--regression` comparator folded into
  `--selftest` (T6-4 also cites a `corpus/knowledge/self-hardening-r6.md`
  that had not landed at poll close).

## 0. Landing status

### 0.1 Baseline (tameshi tree; HEAD `e0c453e`, tree clean at 14:38)

Round 5 finalized as `e0c453e` (14:33): LOG.md 304 L (`5f3724e8…`),
SCORECARD.md 18 L (`0970ecde…`) with its round-5 row landed as a **terse
stub** (`| 5 | depth | round-4 state | 3rd mutation case … | wave-5 32-lane |`)
— the full row offered in `plans/round-5-record-draft.md` §A was not the form
that landed; round-4's row is the same stub shape. SKILL.md 791 L / 55138 B
(`928e073f…`, round-5 revision; no service/opt-in text at open — checked).
`tools/mutate-and-run.sh` committed at 1001 L / 42291 B (`597e141989065e03…`,
round-5 revision). All nine `corpus/knowledge/*.md` pins as listed in §C.1.

Target pins used by this round (read-only): kumitate
`scripts/cite-check.mjs` 2537 L / 126735 B / `40573448330f52…` (matches the
plan's pin; kumitate HEAD `175de6b`); mado `tools/mado-verify.sh` 45334 B /
`d7edaab4bf108625…` (mtime 14:08:57; matches T6-1's pre-registration).

### 0.2 Re-measured landing status (this lane, 2026-10-14, at draft write time)

Every pin below was re-read by this lane in this session. Values that differ
from this draft's first pass are carried in §0.3, not smoothed.

- **tameshi tree**: HEAD `e0c453e`; working set = `M SKILL.md`,
  `M corpus/knowledge/fleet-suite-census.md`, `M tools/mutate-and-run.sh`, plus
  untracked `corpus/knowledge/{mutation-case-mado-verify,self-hardening-r6}.md`,
  `plans/round-6-record-draft.md`, `plans/round-7.plan.md`.
- `LOG.md` 304 L / `5f3724e85359879c…`; `SCORECARD.md` 18 L / `0970ecde293f933d…`
  — both unchanged from the round-5 close (changing them is this draft's job).
- `tools/mutate-and-run.sh` **1080 L / 46850 B /
  `b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb`** (round-5
  revision `597e141989065e03…`, 1001 L / 42291 B); header `:5-7` names the r6
  T6-4 hardening; `VERSION` deliberately still `r4-2` (`:114`).
- `SKILL.md` **918 L / 62373 B /
  `137879dd174383ca79ba70c5f68f51dc6055eb78d0e799fb547de001d72059bb`**;
  `git diff --stat` = **+128/−1**; `git show HEAD:SKILL.md` (55138 B) is a byte
  prefix of it (`cmp`: `EOF on … after byte 55138, in line 792`); the new
  section is `SKILL.md:794` = `## The mutation service — running a sweep for an
  opting-in lane (round 6, measured)`.
- `corpus/knowledge/mutation-case-mado-verify.md` **323 L / 24534 B /
  `f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3`**
  (mtime 14:49:27; final byte `\n`).
- `corpus/knowledge/self-hardening-r6.md` **261 L / 16252 B /
  `f2c347acd323b077f94c4026571796294200d2c9ed96ca548e0414600d49acf1`**
  (mtime 14:51:05).
- `corpus/knowledge/fleet-suite-census.md` modified, **+290/−1** (uncommitted).
- **Target pins.** kumitate `scripts/cite-check.mjs` 2537 L / 126735 B /
  `40573448330f52…` (unchanged; still only the PREP-T6 probe, no engagement
  note). mado `tools/mado-verify.sh`: the swept revision `d7edaab4…` is still
  mado's HEAD blob (`git -C mado-shokunin show HEAD:tools/mado-verify.sh` →
  same sha, 1098 L / 45334 B), but the **live working tree moved**:
  `c4c1afb75dd1…`, 1186 L / 50126 B, mtime 14:55:16, `git diff --stat`
  **+88/−0** — mado's own round-6 hardening, inside `selftest()` only.
- **Owner follow-up landed (new since this draft's first pass).**
  `mado-shokunin/corpus/knowledge/gate-mutation-proof.md` (168 L, untracked,
  lane M6-1) records the three ordered steps of mado's round-6 plan §(a) and
  re-runs **tameshi's exact 10-defect spec** against the hardened gate:
  `CONTROL: GREEN` + `MADO_SELFTEST: 53/53 assertions passed`, **killed 10 /
  survived 0 / inconclusive 0 — kill-rate 100 %** (the same spec on `d7edaab4…`:
  4/10, 40 %), `MUTATE_RESTORE: OK` before=after=`c4c1afb7…`; its §5 supersedes
  the round-5 gate identity and asks downstream records — this one included — to
  cite the hardened pin.

### 0.3 Corrections ledger — what moved since this draft's first pass (append-only)

Recorded, not smoothed; the first pass's cells are kept here verbatim so nothing
is lost by the re-write.

| cell | first pass (as written) | measured now | reading |
|---|---|---|---|
| mado sweep note | 321 L / 24479 B / `23b1d26d8c8354fc…` / mtime 14:48:24 | 323 L / 24534 B / `f2d53d49…` / mtime 14:49:27 | the note was re-pinned a minute after the first pass read it; §A/§B/§C below cite the new sha |
| target, live | `d7edaab4…` (45334 B) | HEAD blob still `d7edaab4…`; **working tree `c4c1afb7…` (50126 B, +88/−0)** | mado absorbed the sweep's survivors on its own lane; the sweep table stays tied to `d7edaab4…` |
| `SKILL.md` | 918 L / 62373 B / `21cf9a93dea03f0a…` | 918 L / 62373 B / `137879dd…` | same size and line count, different sha — the first pass's sha does not verify against the file on disk now; the byte-prefix and +128/−1 readings do |
| mado acceptance | "NOT LANDED at poll close" | `gate-mutation-proof.md` present (untracked) + gate hardened to 53/53, 10/10 on tameshi's spec | the anti-claim's "no acceptance → recorded unabsorbed" is superseded: the owner accepted and re-ran the spec itself |
| harness | `597e1419…` (sweep) → `b56c6e57…` (re-pin, incident I1) | `b56c6e57…`, pinned by this lane's runs | unchanged; the drift cell is now measured, not open (§C.3) |
| census | `fleet-suite-census.md` unchanged | **+290/−1** (uncommitted) | the round-6 census update landed |
| first pass's §C.5–§C.8 re-sweeps | cite-check 1/4 + mado 4/10 re-run, both tool revisions | superseded for mado by §C.3 (measured under `b56c6e57…`); **cite-check was NOT re-run this session** — its scratch `/tmp/w5-prept6-cite/` is present but unread | one cell re-measured, one carried as the first pass left it |

**Lines 1–50 of this file are byte-preserved from the first pass**, so that
`corpus/knowledge/mutation-case-mado-verify.md:21` (its incident-I1 note, "same
pin the round-6 draft records at `plans/round-6-record-draft.md:50`") still
resolves to the mado target pin — verified below (§C.6).

## A. SCORECARD.md — move-log rows (append after the round-5 row)

Precedent: rounds 3 and 4 appended two rows; round 5 appended one terse stub.
Measured cells only; counting commands in the Evidence column. Full rows first,
then the stub form the parent may prefer (rounds 4–5 landed as stubs).

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 6 | adjacency | the method had measured 3× in-lane (JS `kimi-census.mjs` 80 %, kagi `surface-census.sh` 80 %, tsukuroi gate 60 % — every case cut by tameshi on a sibling gate); the round-5 census queue (`fleet-suite-census.md` §5) was an offer never served; the plan's named first engagement was the queue head, kumitate `cite-check.mjs`, probed at 1/4 killed | first service engagement executed **read-only** for an opting-in lane — mado (`tools/mado-verify.sh` @ `d7edaab4…`, 45334 B; its `plans/round-6.plan.md` §(a) pre-registers the engagement, harness consumed read-only): 10 pre-registered single-edit mutants vs the 28-assertion hermetic selftest → **4/10 killed (40 %)**, the corpus's first rate below the 50–80 band, composition-explained — **4 in-surface 4/4 vs 6 out-of-surface 0/6**, i.e. the suite's assertion set and kill set are **co-extensive**; six survivors each with a measured non-equivalence probe (P3 row+counts, P5 exit code, P7 verdict flip, P8 detail text, P9 verdict flip, PR1 row); **D9 = a safety row asserted only in its PASS direction — new arm-class-matrix shape**; control `28/28`, `MUTATE_RESTORE: OK`, target pin before=after, mado tree untouched; seven ranked recommendations (recommendations only); census-ordering question left OPEN (delivered mado, not cite-check); SKILL gains the service opt-in contract (791 → 918 L, +128/−1); **owner follow-up measured: mado's own M6-1 hardening re-ran the same spec 10/10 killed (100 %) at `c4c1afb7…` with selftest 28/28 → 53/53 — acceptance now recorded** | `bash tools/mutate-and-run.sh --target <pinned d7edaab4 copy> --defects <10-defect spec> --suite 'bash "$MUTANT" --selftest'` → `CONTROL: GREEN (exit=0 duration-ms=450)`, `MADO_SELFTEST: 28/28 assertions passed`, `DEFECT D1/D2/D4/D6: KILLED`, `DEFECT D3/D5/D7/D8/D9/R1: SURVIVED`, `MUTATE_RESTORE: OK` before=after=`d7edaab4…`, `MUTATE: DONE (target=mado-verify-d7edaab4 defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)`, rc 0, 5.1 s (this lane, tool `b56c6e57…`, §C.3); all ten mutant sha256 identical to the note's listed prefixes; note tallies re-read (`mutation-case-mado-verify.md` @ `f2d53d49…`: `**KILLED**` ×4, probe rows 6, E1–E5, U1–U6, §8 items 7); ten cited anchors re-read byte-exact on the pinned blob (§C.5); mado hardened gate `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 53/53`, rc 0; mado note `gate-mutation-proof.md:45` → `killed 10 / survived 0 / inconclusive 0 — kill-rate 100 %`. Re-run 2026-10-14 (TAMESHI-SCR-T6) |
| 6 | operability | tool r4-2 revision `597e1419…` (1001 L / 42291 B): `--regression` re-ran two embedded cases, `--selftest` 37/37; the comparator's band edges, absent-row accounting, DEGRADED-rc and asymmetric-table arms were themselves untested | own-gate hardening (T6-4, note `self-hardening-r6.md`): a meta-sweep of the tool's **own** `--regression` comparator — sweep A on the pre-hardening revision **0/6 killed (6/6 survived, prediction held)**, then the surviving comparator mutants folded into `--selftest` (+83/−4 → `b56c6e57…`, 1080 L / 46850 B) and **sweep B 6/6 killed (100 %)** on new labels rg5–rg9; selftest **37/37 → 55/55**; probe identity R1 ≡ R2 (comparator bytes behaviour-identical); `--regression` re-run under the new revision `REGRESSION: PASS (cases=2 passed=2)`; and the round-6 service table reproduces under the new revision (§C.3) — the mado note's U3 drift cell measured, not left open | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 55/55 pass` / `VERDICT: PASS`, rc 0, 4.6 s (was 37/37); `wc -l tools/mutate-and-run.sh` → 1080; `git diff --stat` → `83 insertions(+), 4 deletions(-)`; `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-kimi-census: PASS (band: killed-delta<=1 flips<=1 inconclusive=0 defects=10)`, `REGRESSION_CASE bash-surface-census: PASS (… match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0)`, `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1 flips<=1)`, rc 0, 18.7 s; note cells re-read (`self-hardening-r6.md` @ `f2c347ac…`: sweep A `MUTATE: DONE (… killed=0 survived=6 inconclusive=0 kill-rate=0%)`, sweep B `6/6 killed — kill-rate 100%`, selftest `37/37 (R1) → 55/55 (R2)`, §3 rg5–rg9 kill-attribution table, §6 unknowns ×3). Re-run 2026-10-14 (TAMESHI-SCR-T6) |

Stub form (rounds 4–5 convention):

```
| 6 | adjacency | round-5 state | mado service sweep: 4/10 killed (40 %), read-only, co-extensive surface, 7 recommendations; owner hardened to 10/10 at c4c1afb7… | wave-6 32-lane + SCR-T6 re-sweep |
| 6 | operability | tool 597e1419… 37/37 | self-hardened selftest 55/55 (comparator mutants), REGRESSION PASS 2/2 | wave-6 32-lane |
```

## B. LOG.md — round-6 entry (append as a new bullet after the round-5 entry)

- 2026-10-14 — round 6 (training r5): planned as a ufo-round-plan
  (`plans/round-6.plan.md`, ufo-round-plan-v1 — axis move **adjacency**: the
  method ships as the census-offered service to the first opting-in lane;
  `--regression` to become the fleet kill-rate gate). Same dispatch shape as
  rounds 1–5 — lane write-scopes leave this LOG to the scribe; the lane
  deliverables in this repo ARE the wave record (observation; no
  `.ufo/waves/tameshi-r6-*` directory was seen).
  TAMESHI-T6-1 → `corpus/knowledge/mutation-case-mado-verify.md` (323 `wc -l`,
  24534 B, sha256 `f2d53d495e6c1d8b…`): the first SERVICE engagement — mado
  opted in (`mado-shokunin/plans/round-6.plan.md` §(a), harness consumed
  read-only); target `tools/mado-verify.sh` @ `d7edaab4…` (1098 L / 45334 B),
  suite `bash "$MUTANT" --selftest` (28 assertions, four scenarios, hermetic
  fixtures, no substrate), 10 pre-registered single-edit mutants → **4/10
  killed (40 %)**, the corpus's first sub-50 rate; composition 4 in-surface
  (4/4) + 6 out-of-surface (0/6), so the suite's assertion set and its kill set
  are **co-extensive** (neither weak nor strong — the rate is composition, not
  a regression); kills D1 (CLEAN token renamed, 1 assert), D2 (UNKNOWN guard
  dropped — 3 asserts incl. the no-fake-CLEAN arm), D4 (DIVERGED `exit 1`→0,
  seen twice), D6 (`xdph` dropped from the declared census, caught via scenario
  B's named FAIL); survivors D3 (SKIP→PASS row unread), D5 (failure-path exit
  2→1 unobservable — the harness cannot see it either), D7 (include-count
  `-ne`→`-lt`, boundary never reached; tsukuroi-B7 shape), D8 (sha-pin NOTE
  always "matches"), **D9 (boundary read-only row asserted only in its PASS
  direction — new matrix shape)**, R1 (tomllib-unavailable arm unreachable
  in-suite); six measured non-equivalence probes, no live session read
  (PATH-level stubs only); control 28/28, `MUTATE_RESTORE: OK`, target pin
  before=after, mado tree untouched; **incident I1**: the harness moved
  mid-round by a concurrent lane (`597e1419…` → `b56c6e57…`) — every cell tied
  to the old revision, and this lane closed the drift cell by re-running the
  whole spec against the pinned bytes under `b56c6e57…`: 4/10, same six
  survivors, all ten mutant shas identical (§C.3); E1–E5 (pre-registration
  held: predicted and measured tables identical); U1–U6; §8 seven ranked
  recommendations to mado (recommendations only). Note §6 records the plan's
  `--regression` embedding clause as unlanded (the tool still re-runs two
  cases; `plans/round-7.plan.md` leg 1 carries it) and the census-ordering test
  as open (delivered mado, not cite-check).
  TAMESHI-T6-4 → harness self-hardening: the tool's OWN `--regression`
  comparator swept at meta level — six single-edit comparator mutants, all
  predicted (statically) to survive — sweep A on the pre-hardening revision
  `597e1419…` → **0/6 killed (6/6 survived)**, prediction held; the surviving
  mutants folded into `--selftest` (+83/−4 → `b56c6e57…`, 1080 L / 46850 B;
  comparator bytes unchanged) → sweep B **6/6 killed (100 %)**, every kill on a
  new label (rg5–rg9: band edge 1 flip / killed-delta 1, recorded-entry-absent,
  measured-row-unrecorded, DEGRADED rc=1 table-compared, all-killed table);
  `MUTATE_SELFTEST: 37/37 → 55/55`; probe identity R1 ≡ R2; `--regression` on
  R2 `PASS (cases=2 passed=2)`; landed as `corpus/knowledge/self-hardening-r6.md`
  (261 L, `f2c347ac…`) with three unknowns (§6) and a §5 recommendation to fold
  the same case classes into future service engagements.
  SKILL round-6 append → `SKILL.md` (791 → 918 L, +128/−1, sha
  `137879dd…`): `## The mutation service — running a sweep for an opting-in
  lane (round 6, measured)` — the opt-in contract (pinned revision,
  one-command hermetic suite exercising the copy, clause-mapped spec), the
  fail-closed protocol, and the mado engagement as the worked instance (the
  append is byte-prefix-preserving; it also terminated the previously
  unterminated final line).
  Owner follow-up (mado's own lane M6-1, not tameshi's write scope) →
  `mado-shokunin/corpus/knowledge/gate-mutation-proof.md` (168 L, untracked):
  the gate's selftest extended from A–D to A–D + E/F/H/I (28 → 53 assertions,
  `+88/−0` inside `selftest()`), and **tameshi's exact 10-defect spec re-run
  against the hardened revision → 10/10 killed (100 %)**, control
  `MADO_SELFTEST: 53/53`, `MUTATE_RESTORE: OK` before=after=`c4c1afb7…`. The
  six survivors of tameshi's sweep are each killed by a case added in that
  round; the four already-killed stay killed. Recorded as the acceptance the
  plan's anti-claim left open — the recommendation was absorbed by the owner,
  and the sweep's findings were the cause.
  PREP-T6 (round-5 tail) → the cite-check feasibility probe (1/4 killed) is
  unchanged; no cite-check engagement note exists at this draft's close.
  Scribe verification (this draft, TAMESHI-SCR-T6, re-run 2026-10-14; scratch
  `/tmp/w6-scr-t6-*`): `tools/mutate-and-run.sh --selftest` → 55/55 PASS, rc 0;
  `--regression` → `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1
  flips<=1)`, rc 0, 18.7 s; independent mado re-sweep against the pinned
  `d7edaab4` bytes (recovered read-only from mado's git) under the hardened
  tool → 4/10, verdicts and all ten mutant shas identical to T6-1's table;
  `mado-shokunin/tools/mado-verify.sh --selftest` (live, read-only) → 53/53,
  rc 0; ten cited anchors re-read byte-exact on the pinned blob; tameshi pins
  re-read (LOG 304 L `5f3724e8…`, SCORECARD 18 L `0970ecde…`, kumitate
  cite-check `40573448…` unchanged).
  SCORECARD round-6 move: adjacency improved (first service engagement
  delivered read-only with per-defect verdicts, survivor probes and
  recommendations; first sub-50 rate, composition-bound and co-extensive; first
  safety-row-only-PASS survivor class; owner acceptance recorded) and
  operability improved (harness self-hardened 37→55 selftest; regression gate
  re-verified; the drift cell measured).
  Carried to round 7 (recommendations, not absorbed): the `--regression`
  embedding of tsukuroi + cite-check (round-7 plan leg 1); a cite-check
  engagement note (census head; probe only so far); mado's `gate-mutation-proof.md`
  hardening is landed but its residual items stay mado-owned (dead rc-6 arm,
  exit-flatten family bounded by the harness, the 51 live-plane row sites —
  tameshi §8 #1 unabsorbed); the mado note's U1–U2, U4–U6 (live-plane
  sensitivity, suite-vs-truth, shared-scratch attribution, host gating); the
  T6-4 note's §6 unknowns; the round-5 carries (coverage rows, glued errata
  headings, matrix fold T5-3 status).

## C. SCR-T6 evidence ledger (measured by this lane 2026-10-14; scratch `/tmp/w6-scr-t6-*`)

1. **Baseline pins re-read** (tameshi, HEAD `e0c453e`): `LOG.md` 304 L
   `5f3724e85359879c…`; `SCORECARD.md` 18 L `0970ecde293f933d…`;
   `tools/mutate-and-run.sh` 1080 L / 46850 B / `b56c6e57…`; `SKILL.md` 918 L
   / 62373 B / `137879dd…` with `git diff --stat` +128/−1 and the HEAD blob
   (55138 B) a byte prefix (`cmp`: `EOF on … after byte 55138, in line 792`);
   `grep -n '^## The mutation service' SKILL.md` → `:794`; kumitate
   `scripts/cite-check.mjs` 2537 L / 126735 B / `40573448…`.
2. **Source-note pins**: `mutation-case-mado-verify.md` 323 L / 24534 B /
   `f2d53d49…` (mtime 14:49:27, final byte `\n`); `self-hardening-r6.md` 261 L
   / 16252 B / `f2c347ac…` (mtime 14:51:05); `fleet-suite-census.md`
   `git diff --stat` +290/−1.
3. **Independent mado re-sweep against the pinned bytes, under the hardened
   tool** (the note's U3, measured). Pinned revision recovered read-only:
   `git -C mado-shokunin show HEAD:tools/mado-verify.sh` → sha256
   `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13`, 1098 L /
   45334 B (the live tree is now `c4c1afb7…` / 1186 L / 50126 B, `+88/−0`), so
   the sweep was pointed at a byte copy under `/tmp`. Command: `bash
   tools/mutate-and-run.sh --target /tmp/scr-t6-target-d7edaab4.sh --defects
   /tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec --suite 'bash
   "$MUTANT" --selftest' --workdir /tmp/w6-scr-t6-mado-sweep --label
   mado-verify-d7edaab4` (spec = the T6-1 spec, sha re-read from the note's §9
   layout). Readings: `MUTATE_TOOL: … sha256=b56c6e57…`; `CONTROL: GREEN
   (exit=0 duration-ms=450 …)`, `MADO_SELFTEST: 28/28 assertions passed`;
   `DEFECT D1/D2/D4/D6: KILLED` (suite exits 2, `FAILED — 27 passed, 1 failed`),
   `DEFECT D3/D5/D7/D8/D9/R1: SURVIVED` (exit 0, 28/28); `MUTATE_RESTORE: OK`
   before=after=`d7edaab4…`; `MUTATE: DONE (target=mado-verify-d7edaab4
   defects=10 killed=4 survived=6 inconclusive=0 kill-rate=40%)`, rc 0, 5.1 s.
   `results.tsv` mutant shas match the note's ten listed prefixes exactly
   (D1 `ec60ae5c8f82`, D2 `41ae4e6e26e6`, D3 `1c0e1d3ee758`, D4 `7902653acf98`,
   D5 `5f0937367e74`, D6 `4b94c1802ba0`, D7 `ce37404f12eb`, D8 `81351c897a8b`,
   D9 `81817f67c950`, R1 `6f3affd3849e`).
4. **Tool selftest + regression** (tameshi, live revision): `bash
   tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 55/55 pass` /
   `VERDICT: PASS`, rc 0, 4.6 s; `bash tools/mutate-and-run.sh --regression
   --workdir /tmp/w6-scr-t6-regression` → both cases PASS
   (`match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0
   flips=0`), `REGRESSION: PASS (cases=2 passed=2; band killed-delta<=1
   flips<=1)`, rc 0, 18.7 s.
5. **Cited anchors on the pinned mado revision** (all ten re-read byte-exact;
   `sed -n '<n>p'` on the recovered `d7edaab4` blob): `:1086` = `if [ "$FAIL"
   = 0 ] && [ "$UNKNOWN" = 0 ]; then`; `:1088` = the file-plane
   `MADO_VERIFY: CLEAN (…)` printf; `:1099` = `exit 1`; `:522` = the `local -a
   LOCAL=(…)` census; `:574` = `if [ "$sha" = "4f52854a3c14" ]; then`; `:738` =
   `if [ "$after" = "$before" ]; then`; `:429` = `return 2`; `:484` =
   `if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then`; `:588` = the `row hypr-live
   live.plane SKIP …` call; `:651` = the `row walker walker.config UNKNOWN
   "python3 tomllib unavailable — cannot parse TOML"` call.
6. **Cross-file anchor**: `sed -n '50p' plans/round-6-record-draft.md` →
   `` `d7edaab4bf108625…` (mtime 14:08:57; matches T6-1's pre-registration).``
   — the line `mutation-case-mado-verify.md:21` cites; lines 1–50 are
   byte-preserved by this re-write so the citation still resolves.
7. **Hardened-gate spot-check** (mado, read-only): `bash
   mado-shokunin/tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 53/53
   assertions passed`, rc 0, 1.1 s.
8. **Note tallies re-read**: `mutation-case-mado-verify.md` — `**KILLED**` ×4,
   probe rows 6, `E1–E5` ×5, `U1–U6` ×6, §8 numbered items 7, table rows 11;
   the co-extensive cell at `:69-71`; the headline at `:60`. `self-hardening-r6.md`
   — two 6-row M-tables (sweep A + kill attribution), sweep-A line `:41`,
   sweep-B line `:43`, `55/55` at `:47`.

**Spot-checks (two, both re-run this session).**

- **SC1 — the headline cells, on the note's own bytes.** `sed -n '60p'` →
  `- O: **kill rate 4/10 (40 %)**, survivors D3, D5, D7, D8, D9, R1, **0
  inconclusive** — all 11`; `sed -n '69,71p'` → `… here the suite's assertion
  set and its kill set are **co-extensive** — nothing / outside the asserted
  surface was caught, and nothing inside it escaped. The 40 % rate is …`.
  Both re-read on `f2d53d49…`; the draft's headline quotes them verbatim.
- **SC2 — the pinned anchors + the cross-file line.** Ten cited `d7edaab4` line
  refs match the note's cites verbatim (§C.5), and
  `plans/round-6-record-draft.md:50` still carries the mado pin (§C.6) — the
  line the note's I1 paragraph points at.

## D. Parent checklist (round close)

- **Honesty item 1 — which revision measured what.** Name incident I1 wherever
  the 4/10 table is quoted: T6-1's numbers are tied to tool `597e1419…`; this
  lane's re-run (§C.3) reproduces the table and all ten mutant shas under the
  hardened tool `b56c6e57…`, so the drift is behavior-preserving **for this
  case** — but say the revision.
- **Honesty item 2 — the target moved too.** The sweep measured `d7edaab4…`
  (still mado's HEAD blob); mado's working tree is now `c4c1afb7…` (+88/−0,
  selftest 53/53) because mado absorbed the findings on its own lane. The
  4/10 headline is a statement about the round-5 revision; mado's
  `gate-mutation-proof.md` §5 asks the round-6 record to cite the hardened pin
  as the current identity — cite both, never merge them.
- **Plan-vs-delivered.** The plan's first-engagement claim (cite-check, census
  queue head) was NOT executed as a sweep — the delivered engagement is mado's;
  the `--regression` embedding clause did not land (round-7 plan leg 1 carries
  it). Record both as findings/carries, not smoothed (the sweep note §6 says the
  same).
- **Commit items** (lane identity + round shape; precedents `2587e0a`,
  `53e74a8`, `b58b26f`, `e0c453e`): `corpus/knowledge/mutation-case-mado-verify.md`;
  `corpus/knowledge/self-hardening-r6.md`; `corpus/knowledge/fleet-suite-census.md`
  (+290/−1); `tools/mutate-and-run.sh` (+83/−4); `SKILL.md` (+128/−1); the
  round-6 record draft itself — **precedent says the draft IS committed**
  (`git show --stat e0c453e` lists `plans/round-5-record-draft.md`; `b58b26f`
  lists `plans/round-4-record-draft.md`); each round commit also carries
  `LOG.md` +1 line, `SCORECARD.md` +1 line, and a rewritten plan file
  (`plans/round-6.plan.md` is 34 L and already committed in `e0c453e`).
  `plans/round-7.plan.md` is the next round's plan (its own item). The mado-side
  files (`gate-mutation-proof.md`, the hardened `tools/mado-verify.sh`) commit
  under mado's lane, not here.
- **Row convention**: rounds 4–5 landed as terse stubs; §A offers full rows and
  the stub pair — decide which form lands (record either way).
- **Coverage-map rows** (`corpus/README.md`): add rows for
  `mutation-case-mado-verify.md` and `self-hardening-r6.md`; round-5 carries
  still open (arm-class-matrix, fleet-suite-census, tsukuroi-census rows; SKILL
  row revision).
- **Glued errata headings** (round-5 carry, both files) — repair
  byte-prefix-safe or record as a rendering defect.
- **Unlanded items to watch in round 7**: a cite-check engagement note (census
  head; probe only); mado's residual items (dead rc-6 arm, exit-flatten family,
  the 51 live-plane row sites — tameshi §8 #1); audit verdicts, if any land
  after this draft.
- **Shared scratch**: `/tmp/w5-mado-m52-selftest.*` carried ≥37 foreign
  directories during the sweep (note §I1/U4; 44 at mado's cleanup) — if another
  round sweeps the same gate, namespace the fixtures per run.
