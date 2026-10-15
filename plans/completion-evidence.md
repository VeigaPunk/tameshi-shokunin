# tameshi-shokunin — completion pack: rounds 2–11

Audit input for the parent, written by lane PACK-T during the round-11 wave
(2026-10-14). One line per round (round · axis · headline · commit hash ·
verifier names), the SHONEN status, and the debts. Nothing is re-adjudicated
here: every headline is a pointer into the round's landed record (LOG.md,
SCORECARD.md move-log, `plans/round-N-record-draft.md`, `reports/`); every
number stays in its record. This lane wrote only this file (dispatch scope;
the LOG append is the parent scribe's — dispatch-scope-overrides-append
precedent, `LOG.md:5-8`). Read-only elsewhere; no secrets read; no external
sites.

State at this write [O]: HEAD `606716f703f7699af458476a31fc78ddc9bf552c`
("probation round 10 (training r9): see LOG"); `git status --porcelain`
empty. Rounds 2–10 are committed; round 11's execution is in flight and
uncommitted (its plan is pre-committed inside `606716f`). The round-10
plan's "no round 11 is planned by this arc" clause is superseded by the
round-11 dispatch — recorded, not smoothed (`plans/round-11.plan.md:16-24`).
Commit hashes were derived with `git log --format='%h%x09%H%x09%s'` (7-char
short form; full hashes in the appendix).

Round labels [I]: commit subjects label rounds 4–10 "(training r3)" …
"(training r9)" (round N = training r(N−1); round 11 = training r10, the
final; `plans/round-11.plan.md:14-20`). Rounds 2–3 are committed as
"probation round 2/3".

## One line per round

| Round | Axis | Headline | Commit | Verifiers |
|---|---|---|---|---|
| 2 | depth (primary) + calibration | First measured kill-rate (JS `kumitate/scripts/kimi-census.mjs`): 43-case hermetic suite vs 10 single-edit mutants → **8/10 killed (80 %)**, survivors D2/D10 = reported-but-unasserted surfaces; wave-1 errata applied append-only (K-R2×4, G-R2×6, V-R2×4, +E1); fleet 4th verifier pattern (g2d D0–D10); SKILL mutation-bar bands (171→244 L) | `2587e0a` | scribe re-runs (TAMESHI-SCR — SCORECARD.md:13-14 rows carry the re-run commands); in-note per-claim re-runnable audit evidence; no separate audit-lane report landed |
| 3 | depth (cross-language generality) + operability | Second kill-rate, first bash gate (kagi `surface-census.sh`): **8/10 (80 %)**; cross-language divergence finding (same rate, narrower bash kill width; B5 fixture-absent-arm survivor class); first tool `tools/mutate-and-run.sh` (hermetic selftest 24/24); SKILL 244→665 L; no-oral-context executor test (D5 killed from SKILL.md alone, 42/43) | `53e74a8` | TAMESHI-B1/B2/B3 non-author audits (independent driver rebuild; D5 tool re-run, same kill + mutant sha; dual tool sweeps verdict-identical to both notes' tables, restore OK ×2); scribe TAMESHI-B4 (SHONEN boxes [x]) |
| 4 (r3) | calibration | Arm-class matrix (20 mutants re-cut by arm class; ledger 16 killed/4 survived; 5 classes admitted / 1 proposed / 1 unknown; row E = sole instance B5) + tool `--regression` gate (selftest 37/37) + round-gate §13 static projection (projection, NOT measurement) | `b58b26f` | VER-T1 (row E CONFIRMED; 2 precision errata landed in round 5); scribe SCR-T re-ran the tool gates |
| 5 (r4) | depth | Third kill-rate, cross-author (tsukuroi `tsukuroi-census.sh`): **6/10 (60 %)** — first measurement in the 50–80 % band; incident I1 recorded not smoothed (substrate moved mid-run; §6 replay: hardening closed B10 only); six-gate suite/arm census (348 cases, 6/6 green; 0/6 kill-rate harnesses) | `e0c453e` | no round-5 audit verdict landed (AUD-T5 carried control/pin evidence only — `plans/round-5-record-draft.md:147-151`); scribe re-sweep SCR-T5 (10/10 mutant shas identical); VER-T1's two errata landed (T5-2) |
| 6 (r5) | adjacency + operability | First service engagement, read-only (mado `mado-verify.sh`): **4/10 (40 %)**; in-surface 4/4 vs out-of-surface 0/6 — the co-extensive assertion/kill finding; six survivors each with a non-equivalence probe; tool self-hardening (sweep A 0/6 → folded into selftest → sweep B 6/6; selftest 55/55); mado owner hardening re-run recorded 10/10 | `4494715` | VER-T6 (independent re-sweep, identical mutant shas — `LOG.md:305`); scribe SCR-T6 (full re-runs) |
| 7 (r6) | operability | The leg ledger: `--regression` replays 4 recorded cases at pinned git blobs (drift-immune; 4/4 PASS; expectation-flip fails loudly; selftest 67/67); contribution contract + `fleet-kill-rate-ledger.md` + opt-in protocol land; queue did not drain; attestation leg not executed | `9f1d3c3` | AUD-T7 (`reports/r7-aud-t7.md`, 5/5 CONFIRMED); cross-lane audit named AUD-X7 in `LOG.md:306` (git-show-only reads, zero working-tree writes); VER-T7 named `LOG.md:306` (no report landed at this write) |
| 8 (r7) | coverage | Cases 5+6: kagi `checklist-run.sh` **7/15 (47 %)** (third co-extensive instance; 15/15 pre-registered predictions) + kumitate `claims-check.mjs` **7/10 (70 %)**; six gates measured; cadence policy lands + first executed 6-case pin read (live-drift catch) | `c611d5d` | VER-T8 (B2 CONFIRMED, mutant sha byte-identical); AUD-T8 (8/8 claims CONFIRMED, 4 mutants re-run byte-identical) |
| 9 (r8) | operability | First scheduled cadence tick fires (4 current · 2 stale · 0 drift; tool held; regression 4/4 exact; recorded twice independently — ledger ER-4 + SKILL :1155); `service-limits.md` lands (10 refusal rows, each anchored); the two stale-gate re-sweeps OPEN at close | `b8eb96e` | VER-T9 (ER-4 row 3 re-derived cell-for-cell; ledger append-only proven); AUD-T9 (10/11 CONFIRMED; row 10 = leg 2 "NOT CLAIMED — honestly open"); peer pin-read corroboration (T9 lane reads agreeing per timestamp) |
| 10 (r9) | operability | The closeout: `corpus/knowledge/operator-runbook.md` lands (executed tick; append drill; drift falsifier; ER-R1/ER-R2); the 4-vs-6 leg cut resolves as an embedding (cases 5/6 = legs 5/6; selftest 80/80; six-leg regression `cases=6 passed=6` ×4 independent lanes); `service-standing-state.md`; finding: runbook 4-leg lines stale | `606716f` | AUD-T10 (`reports/r10-aud-t10.md`, 12-row table, CONFIRMED ×8 + P1/P2 SUFFICIENT with contamination statement; finding row 7 = STALE runbook lines); VER-T10 cold-reader (executed the loop; **report absent** — debt b below) |
| 11 (r10, final) | operability, terminal — the close | In flight at this write: the pre-announced tick (leg 1) + operator schedule (leg 2) + 10-of-10 completeness record (leg 3); `plans/round-11.plan.md` pre-committed in `606716f`; execution writes uncommitted, tree clean | — (no round-11 commit at this write; HEAD `606716f`) | not yet landed; planned seats per `plans/round-11.plan.md:290-298` (schedule+close author, tick lane, re-sweep lane, non-author verifier, scribe, poll) |

## SHONEN status

`SHONEN.md` (36 L) — the probation checklist; **all four boxes `[x]`**, each
naming a non-author verifier with retained evidence; last touched by commit
`53e74a8` (round 3) and unchanged since [O — `git log -- SHONEN.md`]:

- SKILL craft — verifier **TAMESHI-B3** (Appendix A/B defect manifests
  replayed end-to-end through the tool; every per-defect verdict identical to
  both notes; restore OK ×2; evidence `/tmp/tameshi-b3-r3b-1-work/{dsweep,bsweep}`
  + scribe re-sweep `/tmp/tameshi-b4-r3b-verify/sweep/`).
- End-to-end task — verifier **TAMESHI-B1** (independent bash rebuild from a
  `cmp`-verified pristine copy: control `PASS (16 cases)`, B1 `FAIL (1/16)`,
  B5/B10 `PASS (16 cases)`; evidence `/tmp/tameshi-b1-r3b/evidence/`).
- No-oral-context — verifier **TAMESHI-B2** (the executor's D5 kill re-run
  through the tool; identical verdict; mutant sha `b0dfe1a7…0668`; evidence
  `/tmp/tameshi-b2-r3b-work/D5/results.tsv`).
- PROVINCE accuracy — verifier **TAMESHI-B3** (`MUTATE_RESTORE: OK` ×2;
  kagi + kumitate trees porcelain-clean; no cross-domain bleed).

Probation requirement (≥3 verified rounds before any roster row — round-0
commit `40f8e1f`; MINT.md carries the demand evidence) satisfied at round 3
("probation-completing"). Rounds 4–10 proceeded as training rounds. Round
11's plan states the arc ends and the lane does not; no promotion or
retirement claim is made in-repo (`plans/round-11.plan.md:20-25, 201-204`).
Whether a fleet roster row was minted is outside this repo — unknown here.

## Debts

### Open at round-10 close (round-11's planned discharge; in flight, NOT landed at this write)

- a. **Two stale-gate re-sweeps**: tsukuroi `084951be…` → live `c396662e…`;
  mado `d7edaab4…` → live `93e43f8f…`. Ledger byte-identical (`2f25c51e…`),
  no ER-5, no appended rows; tsukuroi worktree drifting again at close
  (`plans/round-10-record-draft.md:417-421`).
- b. **Fresh-executor sufficiency table unreported**: VER-T10 executed the
  loop at `75ed934d…` but no `reports/r10-ver-t10.md` (confirmed absent at
  this write — `ls reports/`), no refusal reading, no append drill; its
  `reading:` classifier is buggy (8 vs 16 chars). NOT EXERCISED / partial is
  the honest state; parent should re-run or re-seat before rendering leg 3
  done (`:422-426`).
- c. **Runbook's four-leg lines stale**: `operator-runbook.md` §2/§3/§7 still
  describe four legs at the landed six-leg revision (`reports/r10-aud-t10.md:177`,
  STALE finding row 7); the tool MOVED `cf41efaa…` → `75ed934d…` — every
  receipt must cite the pin that ran; do not render the instrument as held
  (`:404-410`).
- d. **Ledger gaps**: no row for the six-leg registry; §1 embedding text
  ("cases 1 and 2 only") superseded by ER-2 and by r10-2 (`:366-369`).
- e. **Coverage-map rows** (`corpus/README.md`, still 20 L — confirmed this
  write): rounds 6–10 notes, both r9/r10 reports, `operator-runbook.md` (new
  path), `service-standing-state.md`; plus the census §5 instrument re-pin
  errata (named by ER-2; unlanded) (`:450-456`).
- f. **Watch items**: cases 5/6 notes' U-items (T8-1 U5, T8-2 E3) superseded
  by the embedding; attestation leg (protocol U1); the fleet-contributed
  case unexercised; cite-check's full sweep (`:457-463`).
- g. **`[U]`s the close carries**: the schedule's interval (operator's, not
  the lanes' — `plans/round-11.plan.md:96-103`); whether the operator adopts
  the runbook/schedule; whether any fleet driver invokes the cadence.

### Sibling-owned, carried since rounds 1–3 (recorded-not-absorbed)

- kumitate integration groups + round-gate `INTERNAL_ERROR` arm uncovered
  (K-R2-4; `corpus/README.md:10`).
- kagi live verdicts 5/6 + F-2 (two-lines-per-path fix candidate) (G-R2-6;
  `corpus/README.md:11`); F-1 `--falsify` 16/18 stands as kagi's own [INF]
  host-state dependence.

### Unknown registers carried (unmeasured; stand as written)

- `fleet-kill-rate-ledger.md` §8 U1–U9 (`:218-238`; U3 narrowed by ER-2
  `:281`; U9's first firing executed as ER-4): cross-host stability;
  coordinated multi-edit rewrites; ten surveyed gates' kill profiles;
  live-substrate sensitivity; sensitivity ≠ gate truth; hardened revisions
  vs directed repair; sightings' gate-ness; cadence interval.
- `service-optin-protocol.md` U1–U6 (`:257-273`): attestation not executed;
  no third-lane adoption; dispatch hand-off; exit-flatten family;
  host/toolchain gating; hardened rates vs future spec extensions.
- `service-limits.md` §5 U1–U5 (`:220-238`) + carried ledger U1–U9.
- Cross-case unmeasured classes: the 50 % crossover unprobed (bands are a
  report convention); coordinated multi-edit rewrites (matrix row F unknown);
  cross-host readings.

### Resolved by commit `606716f` [O]

- Round-10 writes were uncommitted at its close (HEAD `b8eb96e`,
  `plans/round-10-record-draft.md:372-376`); `606716f` lands them:
  LOG.md +1 · SCORECARD.md +1 · SKILL.md +95 · `operator-runbook.md` (512 L)
  · `service-standing-state.md` (243 L) · round-10 record draft (470 L) ·
  `plans/round-11.plan.md` (301 L) · `reports/r10-aud-t10.md` (229 L) ·
  `tools/mutate-and-run.sh` (+361/−60 → `75ed934d…`, 1 642 L — re-measured
  this write).
- The runbook landed RELOCATED at `corpus/knowledge/operator-runbook.md`
  (no `HANDOFF.md` existed at any read); the coverage row still needs the
  new path (debt e).

## Appendix — full commit hashes (`git rev-parse`)

| Round | Commit |
|---|---|
| 2 | `2587e0a821a2bffa7e10a78e2a928dc9e7f39408` |
| 3 | `53e74a890c70fdcb97487eadb67c2e36faf7bb7b` |
| 4 | `b58b26fbeba8fd972e1d31ac8a9175a81e333b32` |
| 5 | `e0c453e1ae44b31616268e94b080f4b01d7e082f` |
| 6 | `44947154c23772f766f9f5439090fb5c7ad76e46` |
| 7 | `9f1d3c339a7094968041c7708a65dbf7eab9fae6` |
| 8 | `c611d5d52d1dfe9bf1184768ba4aef4e414a4a0f` |
| 9 | `b8eb96e1d0333a9878e57d834c6213121d5575b9` |
| 10 | `606716f703f7699af458476a31fc78ddc9bf552c` |
| 11 | — (in flight; no commit at this write) |

Sources read by this lane (all read-only): `LOG.md`, `SCORECARD.md`,
`SHONEN.md`, `MINT.md`, `PROVINCE.md`, `AGENTS.md`, `plans/round-2.plan.md`,
`plans/round-11.plan.md`, `plans/round-4…10-record-draft.md`,
`reports/r7-aud-t7.md` … `reports/r10-aud-t10.md`, `corpus/README.md`,
`corpus/knowledge/{fleet-kill-rate-ledger,service-optin-protocol,service-limits}.md`,
and `git log`/`git status` in this repo.

## Fleet round-1 correction — 2026-10-15

The historical SHONEN-status interpretation at lines 44–59 is superseded by
`reports/round-1-calibration.md#box-1` through `#box-4` and that audit's
historical-independence correction. TAMESHI-B1/B2/B3/B4 remain historical
run lineage, not independent promotion authority: a dispatched subagent is
still the lane (`../PROTOCOL.md:63–68`). Temporary logs are not durable
closure evidence (`../PROTOCOL.md:340–343`).

The same correction applies to the promotion-authority interpretation in
`LOG.md:237–249,283–290`, `plans/round-11.plan.md:23–25`, and the
mark-count confirmation in `reports/r11-aud-t11.md:140`. Those historical
bytes and reported run outcomes remain unchanged; no current promotion
is inferred from them. Current SHONEN marks: three lane assertions and an
unchecked no-oral-context box. A historical single-JS-mutant exercise is
not current full-sweep/bash cold-read evidence. The bounded calibration
move does not reopen or renumber the completed training arc.

### Interactive continuation admission hold — 2026-10-15

The correction above is retained as local work, not a completed fleet
round. `SCORECARD.md`'s interactive-continuation section records the
bounded per-axis delta and the formal dispatch block. The predecessor's
nine-seat report does not meet the current exact-32 contract; the
canonical planner validated 32 distinct audit scopes, but the existing
role-to-alias bindings cannot realize the requested routes. No specialist
was dispatched under substitute bindings and no native judgment or
promotion is inferred. Fresh local gate/CLI evidence and exact unblocks:
`reports/round-1-calibration.md#interactive-continuation--blocked-dispatch-local-correction-retained`
and `.ufo/evidence/fleet-round-1/`. The launch counter still earns no
verified-round credit. Continue through the local handoff in a fresh
authorized session, never a second round inside this one.
