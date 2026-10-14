# Round-8 record draft — for the parent scribe to finalize (TAMESHI-SCR-T8)

Drafted 2026-10-14, poll window 19:10:57–19:44:57Z (16:10:57–16:44:57 local;
assignment: 30-min cap; 34 samples at 60 s, then close reads to ~19:47Z) by the
round-8 scribe-prep lane (SCR-T8). This file carries: **A** the SCORECARD
move-log rows, **B** the LOG.md round-8 entry text, **C** the SCR-T8 evidence
ledger, **D** landing status + parent checklist. Write-scope: this file only;
scratch `/tmp/w8-tameshi-scr-t8/` (poll log `poll.log`; the poll task is
`bash-nm1h4xdm`). Anchors: **O** observation · **I** inference · **U** unknown.

## Round-8 shape — planned vs realized

- **Planned** (`plans/round-8.plan.md`, 172 L / 11924 B / `7e53c9d8…`, mtime
  15:30:48; ufo-round-plan-v1): axis move **operability (post-service, second
  turn)** — one move, three ordered legs: (1) **cadence** — the ledger gains a
  mechanism: per-case pin read (`current`/`stale`/`drift`; tool
  `held`/`moved`), triggers T1–T3, an executed command at the round boundary,
  closing the ledger's own U9 (`fleet-kill-rate-ledger.md:235-237`);
  (2) **drift** — a moved case nobody has re-measured is the round's re-sweep
  work, recorded at its newest revision, old tables intact; (3) **intake** — a
  queue position freed by round 7 enters as a case, and the round-7 opt-in
  protocol is checked for the one cadence precondition (a re-pin rule for a
  moved substrate). Claim shape (proposed, "landing adjudicates"): U9 closed by
  mechanism; U3 closed to whatever the case set reproduces; a headline
  `LEDGER: <cases> pinned: held=N moved=M stale=K`.
- **Realized (observed 19:10–19:47Z; lane credits from file text + scratch
  names).** All three legs landed, with two form differences:
  1. **Cadence landed as policy + executed read** — ledger **ER-3**
     (`fleet-kill-rate-ledger.md:285-315`) + SKILL
     `## The re-sweep cadence and the six-case confidence statement (round 8,
     measured)` (`SKILL.md:1010`): readings table, triggers T1–T3, re-pin rule,
     "what the cadence is not" (no daemon, no timer; who runs it stays the
     dispatcher's call [U]). The proposed one-line headline shape was **not
     adopted**; the pin read landed as a table in both files, executed at
     19:15:14Z (SKILL instance) and 19:21:00Z (ER-3), with a live-drift
     re-read at 19:20:29Z.
  2. **Intake landed as TWO full service sweeps** (not "a queue position"):
     case 5 kagi `corpus/checklist-run.sh` by T8-1 — **7/15 killed (47 %)**,
     note 367 L / 22952 B / `43da70e6…`; case 6 kumitate
     `scripts/claims-check.mjs` by T8-2 — **7/10 killed (70 %)**, note 409 L /
     29236 B / `3da1312e…`. Both specs pre-registered; both notes hand the
     ledger its row; ER-2 (`:272-284`) appends rows 5/6 → **six measured
     gates**, rate sequence 80 · 80 · 60 · 40 · 47 · 70.
  3. **Drift leg read, not re-swept**: tsukuroi `084951be…` → live
     `bba6cdf6…` and mado `d7edaab4…` → HEAD blob `90d50cdd…` both read
     **stale**; mado additionally read **drift** (live edit `dc864c6a…` at
     19:20:29Z, `7da4ec50…` at 19:35/19:46Z, uncommitted). T1's record-the-
     STALE-cell branch was taken; the re-sweeps are `plans/round-9.plan.md`
     leg 2. No case was re-cut or widened to manufacture work; `moved=2` is the
     reading (tool itself `held`).
  - **Verification landed**: VER-T8 (independent re-derivation, B2 CONFIRMED,
    mutant sha byte-identical) and AUD-T8 (8/8 claims CONFIRMED, four mutants
    re-run byte-identical). **Design landed**: `plans/round-9.plan.md`
    (PREP-T9, frozen 19:15Z pre-landing — its "6 cases in" dispatch frame
    counts the moved-substrate successors; the landed notes make cases 5/6 the
    queue gates; its own clause defers to the landed bytes).
  - **Tool held** at `cf41efaa…` — round 8 made no instrument edit; cases 5/6
    are **not embedded** in `--regression` (named hand-offs T8-2 E3 / T8-1 U5).

## 0. Landing status

### 0.1 Baseline at window open (measured 19:10–19:12Z)

- HEAD `9f1d3c3` ("probation round 7 (training r6)", 16:06:31 -0300); tameshi
  tree clean; no `.ufo/waves/tameshi-r8-*` directory exists ([O], `ls`).
- Cells (my reads): `LOG.md` 306 L / 22660 B / `aecc3e7f4d42e506`;
  `SCORECARD.md` 20 L / 11681 B / `46a46e2dedd91c14` (round-7 stub row at
  `:20`; `LOG.md:306` = the round-7 entry); `SKILL.md` 1007 L / 68019 B /
  `d36e9a28accdec97` (round-7 revision); `tools/mutate-and-run.sh` 1341 L /
  61632 B / `cf41efaa8be5f52d` (r7-1, mtime 15:29:01);
  `corpus/knowledge/fleet-kill-rate-ledger.md` 269 L / 19781 B /
  `e08efe79bb58c850` (U9 at `:235-237`, U3 at `:221-223`, four-row §1);
  `service-optin-protocol.md` 286 L / 17644 B / `84d0c1547eed257d`;
  `fleet-suite-census.md` 674 L / 48719 B / `ec1c2d8d2877a21d` (its §5 pins
  `597e1419…`/1001 L and `dd2f4dee…`/665 L are two revisions stale);
  `plans/round-8.plan.md` `7e53c9d8…`; 13 `corpus/knowledge/*.md`; `reports/`
  held only `r7-aud-t7.md`.
- Round-7 landed form re-read: `git show --numstat 9f1d3c3` → LOG +1,
  SCORECARD +1, SKILL +90/−1, ledger 270, protocol 286, r7-draft 365,
  r8-plan 173, r7-aud 174, tool +337/−76.
- **Baseline pulse (this lane).** `bash tools/mutate-and-run.sh --selftest` →
  `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0, 4.8 s;
  `--regression --workdir /tmp/w8-tameshi-scr-t8/open/regr` →
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0
  flips<=0)`, all four `match=10/10 … flips=0`, rc 0, ~42 s
  (`/tmp/w8-tameshi-scr-t8/{open-selftest,open-regression}.log`).
- Execution lanes already visible at open ([O], `/tmp`): `w8-tameshi-t81`
  (tool copy + `pristine-checklist-run.sh`, 16:10), `w8-tameshi-t83`
  (`watch.sh`, 16:11), `w8-ver-t8-work` + `w8-ver-t8-poll.sh` (16:11),
  `w8-t8-2-claims` (16:12), `w8-tameshi-t84` (16:15).

### 0.2 Measured at window close (this lane, ~19:34–19:47Z)

- `SKILL.md` **1152 L / 77612 B / `6753b1b224f4bd18`**, `git diff --numstat`
  **+146/−1** (was 1007 L / 68019 B); new section `:1010` (cadence + six-case
  confidence statement); six-case table rows `:1103-1104`.
- `corpus/knowledge/fleet-kill-rate-ledger.md` **315 L / 28503 B /
  `71bc15e365a3574f`**, `git diff --numstat` **+47/−1**; **ER-2** at `:272`,
  **ER-3** at `:285`; §1's four-row table untouched.
- `corpus/knowledge/mutation-case-kagi-checklist.md` (T8-1, untracked)
  **367 L / 22952 B / `43da70e675b8a482`** (mtime 19:19:31Z); headline
  `MUTATE: DONE (target=kagi-checklist defects=15 killed=7 survived=8
  inconclusive=0 kill-rate=47%)`; survivors A1, B1, B3, C1, D1, E2, F2, G1.
- `corpus/knowledge/mutation-case-kumitate-claims.md` (T8-2, untracked)
  **409 L / 29236 B / `3da1312e0a624ca5`** (mtime 19:19:12Z); headline
  `7/10 (70 %)`; survivors D7, D8, D9; D10 = recorded calibration miss.
- `reports/r8-ver-t8.md` (VER-T8) **115 L / 6557 B / `f2c8d91d6d441569`**
  (mtime 19:23:11Z). `reports/r8-aud-t8.md` (AUD-T8) **170 L / 11331 B /
  `8223ac0fed58a417`** (mtime 19:25:31Z). `plans/round-9.plan.md` **222 L /
  15198 B / `230ed6b61e4c89d9`** (mtime 19:16:53Z).
- `tools/mutate-and-run.sh` **unchanged** — `cf41efaa…`, mtime 15:29:01
  (tool `held`). `LOG.md` / `SCORECARD.md` **unchanged** — writing them is
  this draft's job.
- `git status` at close: `M SKILL.md`, `M …ledger.md`, untracked the two case
  notes, `plans/round-9.plan.md`, `reports/r8-{aud,ver}-t8.md`.
- Sibling trees at close: kumitate `175de6b` clean; kagi `fecee87` clean;
  tsukuroi `aa136d6` (6 dirty files; the **gate path clean**,
  `tools/tsukuroi-census.sh` = `bba6cdf6…` = HEAD blob); mado `0c20a76`
  (7 dirty; the **gate path dirty**, live `7da4ec50…` vs HEAD blob
  `90d50cdd…`) — the owners' round-8 lanes were live.
- **Close pulse (this lane).** `--selftest` → `MUTATE_SELFTEST: 67/67 pass`,
  rc 0; `--regression --workdir /tmp/w8-tameshi-scr-t8/close/regr` →
  `REGRESSION_TOOL … sha256=cf41efaa…`, `REGRESSION_DATE
  2026-10-14T19:45:14Z`, four legs `match=10/10 … flips=0`,
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0
  flips<=0)`, rc 0 (~44 s).

### 0.3 Corrections ledger — what moved during the window (append-only)

| cell | at open / intermediate | at close | reading |
|---|---|---|---|
| tool revision | `cf41efaa…` 1341 L / 61632 B | `cf41efaa…` (unchanged; mtime 15:29:01) | **held** — no instrument edit in round 8 ([O], every poll sample) |
| SKILL | 1007 L / 68019 B (`d36e9a28…`, r7) | **1152 L / 77612 B @19:21:04Z** (`6753b1b2…`, +146/−1) | one landing write; the r7 text above `:1010` untouched |
| ledger | 269 L / 19781 B (`e08efe79…`, r7) | **315 L / 28503 B @19:22:06Z** (`71bc15e3…`, +47/−1) | ER-2 + ER-3; no §1–§4 edit |
| cases | 4 embedded legs | 4 embedded + **2 measured gates (rows 5/6)** | notes landed; **no embedding** — named follow-up |
| case notes in flight | — | checklist 4 revisions (`25f50378…`→`ba390484…`→`8cc06046…`→`43da70e6…`, VER-T8 §0.1); claims 2 (`e64e8a2a…`→`3da1312e…`, AUD-T8 §0.1) | bind to the frozen shas only |
| mado gate | `90d50cdd…` = HEAD blob, clean (my 19:16Z read) | live `dc864c6a…` dirty @19:20:29Z (SKILL re-read; ER-3 19:21:00Z) → `7da4ec50…` dirty @19:35Z/19:46Z (mine) | owner lane mid-edit; every cell is a timestamped reading, re-run at the next tick |
| tsukuroi gate | `d666bba3…` working tree (r7 draft close, in flight) | `bba6cdf6…` @ HEAD `aa136d6` (committed 16:06:31) | recorded pin `084951be…` now an ancestor → stale |
| reports | — | VER + AUD landed 19:23:11Z / 19:25:31Z | both bind to the frozen note shas; later edits need re-audit |

## A. SCORECARD.md — move-log rows (append after the round-7 row)

Precedent: rounds 4–7 landed as terse stubs; round 7 is one axis, one stub row.
Round 8 is ONE move (operability, second turn), three legs — full row first,
stub form after.

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 8 | operability (post-service, second turn) | round-7 state: 4-leg ledger (`cases=4`, exact band) with the tool's own U9 open — "the ledger's update cadence is a convention, not a mechanism" (`fleet-kill-rate-ledger.md:235-237`); U3 narrow (two surveyed queue gates, `checklist-run`/`claims-check`, unmeasured); tsukuroi and mado gates had moved again in their round-7 commits (recorded pins stale) | the cadence mechanism landed and executed: ledger **ER-2/ER-3** (`:272-315`) + SKILL `:1010` — per-case pin read (`current`/`stale`/`drift`, tool `held`/`moved`), triggers T1–T3, re-pin rule, executed 6-case read (SKILL 19:15:14Z; ER-3 19:21:00Z) with a live-drift catch (mado 19:20:29Z); no daemon, no timer; **TWO queue cases swept** — kagi `checklist-run.sh` **7/15 (47 %)** (15/15 predictions held) and kumitate `claims-check.mjs` **7/10 (70 %)** (D10 miss recorded), specs pre-registered, survivors each with a non-equivalence probe, restores OK, **six gates measured** (rate sequence 80 · 80 · 60 · 40 · 47 · 70); U3 narrowed — the tsukuroi/mado tables **are** re-verified at their recorded pins by the 4-leg `--regression` (`cases=4 passed=4`, every leg `flips=0`; my runs) while cases 5/6 stay **unembedded** (E3/U5 hand-offs); the drift leg read **stale ×2** (no re-cut; re-sweep = round-9 leg 2); independently verified — **VER-T8** B2 re-derived CONFIRMED (mutant sha byte-identical) and **AUD-T8** 8/8 claims CONFIRMED (4 mutants re-run byte-identical); tool **held** at `cf41efaa…` — no instrument edit this round | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 (open + close, this lane); `--regression` → `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, four `match=10/10 … flips=0`, rc 0, `REGRESSION_DATE 2026-10-14T19:45:14Z` (this lane; opens 19:11Z / closes 19:45Z); pin read ×3 (19:16/19:35/19:46Z: 4 current · tsukuroi stale `084951be…`→`bba6cdf6…` · mado stale+drift `d7edaab4…`→HEAD `90d50cdd…`, live `dc864c6a…`→`7da4ec50…`); notes' headlines vs raw `results.tsv` (7 KILLED of 15 with survivor ids; 7 KILLED of 10, survivors D7/D8/D9) and vs AUD-T8's re-run shas (F1 `8eb8b805…`, G1 `68fba490…`, D7 `f694e232…`, D10 `2c7fecd9…`); `git diff --numstat` → `146 1 SKILL.md`, `47 1 corpus/knowledge/fleet-kill-rate-ledger.md`; ledger ER-2 `:272`, ER-3 `:285`; SKILL `:1010`. Re-run 2026-10-14 (TAMESHI-SCR-T8) |

Stub form (rounds 4–7 convention):

```
| 8 | operability (post-service, 2nd turn) | cases=4 embedded; cadence a convention (U9); 2 queue gates unmeasured | cadence executed (ER-3 pin read 4 current/2 stale + T1–T3 in SKILL :1010) + 2 queue cases measured (checklist 47 %, claims 70 % → 6 gates) + audit/verifier CONFIRMEDs; tool held; cases 5/6 not embedded | wave-8 32-lane + SCR-T8 (selftest 67/67, regression 4/4) |
```

## B. LOG.md — round-8 entry (append as a new bullet after the round-7 entry)

- 2026-10-14 — round 8 (training r7): planned as a ufo-round-plan
  (`plans/round-8.plan.md`, ufo-round-plan-v1 — axis move **operability
  (post-service, second turn)**: the fleet ledger's update stops being a
  convention and gains a mechanism). Same dispatch shape as rounds 1–7 — lane
  write-scopes leave this LOG to the scribe; the lane deliverables in this
  repo ARE the wave record (observation; no `.ufo/waves/tameshi-r8-*`
  directory was created). Lane scratch observed (`/tmp/w8-tameshi-{t81,t83,
  t84}`, `/tmp/w8-t8-2-claims`, `/tmp/w8-aud-t8-{work,evidence}`,
  `/tmp/w8-ver-t8-work`, `/tmp/w8-tameshi-scr-t8`).
  TAMESHI-T8-1 → `corpus/knowledge/mutation-case-kagi-checklist.md` (367 L,
  `43da70e6…`): **the fifth fleet mutation case** (third service engagement,
  form = service) — kagi `corpus/checklist-run.sh` @ `7e5ec98b…` (506 L,
  committed HEAD blob, tree clean) swept through the r7-1 harness
  (`cf41efaa…`) on `/tmp` copies; 15 defects pre-registered as 7 kill-aimed +
  8 hole-aimed, **7/15 killed (47 %)**, predictions held **15/15**; survivors
  A1, B1, B3, C1, D1, E2, F2, G1 — each with a measured non-equivalence probe;
  new mechanisms: CLI fail-open (G1), output-capture loss (E2), deny-list
  re-openable (B3); `MUTATE_RESTORE: OK` before=after=pin; 7 ranked owner-side
  recommendations; U4: no kagi-side opt-in is recorded in kagi's tree — the
  dispatch is the record and the owner's intent stays U.
  TAMESHI-T8-2 → `corpus/knowledge/mutation-case-kumitate-claims.md` (409 L,
  `3da1312e…`): **the sixth case** — kumitate `scripts/claims-check.mjs`
  @ `e9a21b44…` (925 newlines, HEAD blob, tree clean), 39-case suite, 10
  defects (6 kill-aimed + 4 hole-aimed), **7/10 killed (70 %)**; survivors D7
  (cap — the kimi D2 site), D8 (assert-blind threshold, a new measured shape),
  D9 (first JS unreached arm); pre-registration 9/10 verdicts and 8/10 counts
  with the D10 miss recorded as E1 (predicted SURVIVED, measured KILLED — the
  safe direction); `--regression` at `cf41efaa…` runs 4/4 PASS (19:14:16Z,
  this note's run); cases 5/6 are **not embedded** — E3 hands the target pin /
  suite / spec to the tool's owner.
  TAMESHI-T8-3 → `corpus/knowledge/fleet-kill-rate-ledger.md` (+47/−1;
  269 → 315 L; `71bc15e3…`): **ER-2** appends rows 5/6 (six gates measured;
  rate sequence 80 · 80 · 60 · 40 · 47 · 70; the co-extensive assertion/kill
  shape gets a third measured instance, 7/7 + 0/8; §3 supersession with eight
  queue rows standing; U3 narrows — the tsukuroi and mado tables are
  re-verified at their recorded pins by the four materialized legs) and
  **ER-3** lands the **cadence policy** — per-case pin read
  (`current`/`stale`/`drift`; tool `held`/`moved`), triggers T1–T3, the
  re-pin rule ("a moved pin is never re-interpreted; the old table stays"),
  executed read 19:21:00Z (4 current · tsukuroi stale `084951be…` →
  `bba6cdf6…` · mado stale + drift `d7edaab4…` → HEAD blob `90d50cdd…`, live
  edit `dc864c6a…`); §1–§4 never edited.
  TAMESHI-T8-4 → `SKILL.md` (+146/−1; 1007 → 1152 L; `6753b1b2…`):
  `## The re-sweep cadence and the six-case confidence statement (round 8,
  measured)` (`:1010`) — the tick (round boundary), the readings table, the
  executed instance at 19:15:14Z (4 current · 2 stale · 0 drift; tool held;
  scratch `/tmp/w8-tameshi-t84/`) with the 19:20:29Z re-read catching mado's
  live drift, the falsifiers (superseded blob reads stale; one appended line
  reads drift; untouched reads current), T1–T3, the re-pin rule and the
  six-case table (`:1103-1104`); no daemon, no timer — who runs the command
  stays the dispatcher's call [U].
  VER-T8 (verifier lane, read-only) → `reports/r8-ver-t8.md` (115 L,
  `f2c8d91d…`): independent re-derivation of ONE mutant outcome — T8-1's B2
  (`((ns >= 20))` → `((ns >= 0))` at `checklist-run.sh:160`): built from the
  pinned blob with its own applier, **CONFIRMED** (killed, rc 1, 1 of 34
  failing, label `padded reason: exit 0 want 2`); its mutant sha
  `7ac5b530…163db` is byte-identical to the producer's `sweep/results.tsv`
  record; kagi tree porcelain-clean throughout.
  AUD-T8 (audit lane, read-only) → `reports/r8-aud-t8.md` (170 L,
  `8223ac0f…`): **8/8 claims CONFIRMED** — both targets at their pins (git
  blob = live file = lane copy), both control cells reproduce, four mutants
  re-run (F1 `8eb8b805…` / G1 `68fba490…` / D7 `f694e232…` / D10
  `2c7fecd9…`; each byte-identical to the case records), both originals
  unchanged, no fleet file written by the audit beyond its report; verdicts
  bind to the frozen note shas (`43da70e6…` / `3da1312e…`; U1: later edits
  need re-audit).
  PREP-T9 (design lane) → `plans/round-9.plan.md` (222 L, `230ed6b6…`):
  next round's plan — leg tick (the pin read executed under the landed
  cadence), leg re-sweep (every case the tick reads stale/moved, at its live
  revision); frozen 19:15Z pre-landing (its "6 cases in" frame reads the
  moved-substrate successors; the landed bytes are the authority, per its own
  clause).
  Scribe verification (this draft, TAMESHI-SCR-T8; scratch
  `/tmp/w8-tameshi-scr-t8/`): baseline pulse at open (selftest 67/67;
  regression `cases=4 passed=4`) and at close (`--selftest` → 67/67;
  `--regression` → 4/4 exact, `REGRESSION_DATE 2026-10-14T19:45:14Z`, rc 0 —
  this lane's own runs); six-case pin read ×3 (19:16Z / 19:35Z / 19:46Z:
  4 current · 2 stale; mado's live edit observed `dc864c6a…` → `7da4ec50…`);
  the notes' headline cells checked against the lanes' raw `results.tsv`
  (7 KILLED of 15 with the survivor ids; 7 KILLED of 10 with D7/D8/D9) and
  against AUD-T8's re-run shas. Tool **held** at `cf41efaa…`; cases 5/6 are
  the named embedding debt (T8-2 E3 / T8-1 U5); the census §5 re-pin errata
  is named but unlanded (ER-2 follow-up); the tsukuroi/mado re-sweeps are
  round 9's leg.
  SCORECARD round-8 move: operability improved (U9 closed by mechanism and
  an executed command; six gates measured with composition-bound rates and
  pre-registered specs; independent verifier + audit CONFIRMEDs) — the
  embedding half and the re-sweeps are **published, not yet exercised**.
  Carried to round 9 (recommendations, not absorbed): cases 5/6 leg-cut
  (embedding of the 15- and 10-defect specs); census §5 re-pin errata;
  re-sweeps of the two stale cases at their live revisions (round-9 plan
  leg 2); the round-7 opens still open (attestation leg unexecuted; the
  fleet-contributed case; cite-check's full sweep; README coverage rows for
  the five round-6/7/8 notes + two round-8 reports).

## C. SCR-T8 evidence ledger (measured by this lane 2026-10-14; scratch `/tmp/w8-tameshi-scr-t8/`)

1. **Baseline pins + pulse (open, 19:10–19:12Z).** HEAD `9f1d3c3`, tree
   clean; cells and shas in §0.1; selftest `67/67` rc 0 (4.8 s); regression
   `cases=4 passed=4` rc 0 (~42 s), logs `open-selftest.log` /
   `open-regression.log`, workdir `open/regr`. Round-7 landed form:
   `git show --numstat 9f1d3c3` (§0.1); `SCORECARD.md:20` stub row;
   `LOG.md:306` one-paragraph entry.
2. **Close pulse (this lane's independent runs, 19:44:57/19:45:14Z).**
   `--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0;
   `--regression --workdir /tmp/w8-tameshi-scr-t8/close/regr … --keep` →
   `REGRESSION_TOOL … sha256=cf41efaa8be5f52d…bce37242c75`,
   `REGRESSION_DATE 2026-10-14T19:45:14Z`, four `REGRESSION_TABLE` lines
   (`match=10/10`; recorded/measured killed 8/8/6/4; `flips=0`), four
   `REGRESSION_CASE … PASS`, `REGRESSION: PASS (cases=4 passed=4; ledger legs
   exact: killed-delta<=0 flips<=0)`, rc 0.
3. **Six-case pin read (×3: 19:16Z, 19:35Z, 19:46Z; read-only).** Per case,
   `sha256sum <live>` vs recorded pin, `git show HEAD:<path> | sha256sum`,
   `git status --porcelain -- <path>`: kimi-census `83016d45…` current;
   surface-census `275d8294…` current; tsukuroi-census `084951be…` → live/HEAD
   blob `bba6cdf6…` **stale** (worktree clean at the path); mado-verify
   `d7edaab4…` → HEAD blob `90d50cdd…` **stale**, live file `dc864c6a…`
   (19:20:29Z) → `7da4ec50…` (19:35/19:46Z) **drift** (` M`); checklist-run
   `7e5ec98b…` current; claims-check `e9a21b44…` current. Tool `held`
   (sha `cf41efaa…` at every read). These are independent reproductions of
   the ER-3/SKILL pin read; the mado drift is the same event both files
   caught at 19:20:29/19:21:00Z.
4. **The notes' headline cells vs raw evidence (O).** T8-1:
   `sweep/results.tsv` = 15 rows, 7 `KILLED` (A2, B2, B4, C2, D2, E1, F1) +
   8 `SURVIVED` (A1, B1, B3, C1, D1, E2, F2, G1) = the note's 47 % table;
   VER-T8 §1 cross-check: B2 mutant sha `7ac5b530…163db` = the results row.
   T8-2: `work/results.tsv` = 10 rows, 7 `KILLED` (D1–D6, D10) + 3 `SURVIVED`
   (D7, D8, D9) = the note's 70 %; AUD-T8 §1 re-runs reproduce F1/G1/D7/D10
   with byte-identical mutant shas. Frozen note shas re-read at close:
   `43da70e6…` / `3da1312e…` (unchanged since ≥19:20Z; VER-T8 observed four
   in-flight revisions of the checklist note, AUD-T8 two of the claims note —
   every cell above binds to the final shas only).
5. **Anchor re-reads for the record's citations.** Ledger ER-2 `:272`, ER-3
   `:285` (file 315 L); U9 `:235-237`, U3 `:221-223` (still as written, now
   narrowed by ER-2); §3 queue rows `:107-123` (eight stand); SKILL
   `:1010` header, `:1103-1104` six-case rows; protocol re-pin rule
   `service-optin-protocol.md:59-62` (cited by ER-3); census §5 pins
   `:251-267` (stale: `597e1419…`/1001 L, `dd2f4dee…`/665 L — ER-2 names the
   re-pin errata as a follow-up); `corpus/README.md` (20 L) carries no
   coverage rows for the two new notes (or the r6/r7 notes).
6. **Round-7 landed form** (§0.1, §C.1) — for the "before" column.
7. **Cross-lane observations (read-only; not this lane's evidence of fact).**
   Scratch dirs seen across the window: `/tmp/w8-tameshi-{t81,t83,t84}`,
   `/tmp/w8-t8-2-claims`, `/tmp/w8-aud-t8-{work,evidence}`,
   `/tmp/w8-ver-t8-work` (+ its poll log), plus sibling repos' own round-8
   scratch (`/tmp/w8-s8*`, `w8-mado-m8-*`, etc. — other waves' lanes). T8-3's
   watcher log recorded the sibling repos' dirty counts moving mid-window
   (tsukuroi 4→5; mado 5 at 19:23Z — both 6 and 7 dirty respectively at my
   close read) — the owners' round-8 lanes were live; no file of ours was
   touched by them and none of ours was written by this lane beyond this
   draft.
8. **Unknowns from this lane.** (i) Cases 5/6 are not embedded in
   `--regression` — the leg-cut is the tool owner's call (T8-2 E3 / T8-1 U5);
   their tables carry no `REGRESSION` line today. (ii) The census §5 re-pin
   errata and README coverage rows are named, unlanded. (iii) The mado gate
   is under an uncommitted owner edit — any live-mado cell is a timestamped
   observation, not a standing claim. (iv) The stale cases were read, not
   re-swept; their live-revision behaviour is unmeasured (round-9 leg 2).
   (v) Single host / toolchain for every number; cross-host stability stays
   unmeasured fleet-wide. (vi) Whether the cadence command is ever invoked by
   a fleet driver with no lane acting stays [U]. (vii) Lane role labels
   (T8-1/2/3/4, VER, AUD, PREP) are from file credits and scratch names —
   the dispatch itself was not visible to this lane.

**Spot-checks (three, all run this session).**

- **SC1 — the pulse pair (open vs close).** Tool `cf41efaa…` at both ends:
  open selftest 67/67 + regression `cases=4 passed=4` (19:11Z); close
  selftest 67/67 + regression `cases=4 passed=4`, `REGRESSION_DATE
  2026-10-14T19:45:14Z` (rc 0, this lane's runs, `open/` and `close/` logs).
  The tool "held" cell is the instrument's own counters, not prose.
- **SC2 — the 6-case pin read, three times.** 19:16Z: 4 current · tsukuroi
  stale (live `bba6cdf6…`) · mado stale (live = HEAD blob `90d50cdd…`, clean);
  19:35Z and 19:46Z: mado live `dc864c6a…`→`7da4ec50…` dirty (drift), all
  else unchanged — the same reading ER-3 and SKILL froze at 19:21:00/
  19:20:29Z (§C.3).
- **SC3 — the intake cells from the raw tables.** `results.tsv` counts match
  both notes' headlines (7 of 15 · 7 of 10), survivor ids match, and the four
  AUD-T8 re-run mutant shas are byte-identical to the producers' records
  (§C.4) — the claims the record quotes are checked one level below the
  notes.

## D. Parent checklist (round close)

- **Honesty item 1 — the tool held; nothing was re-interpreted.** No round-8
  edit to `tools/mutate-and-run.sh`; `cf41efaa…` is the revision every
  receipt in this record carries. Cases 5/6 tables are **not** embedded; do
  not render them as ledger legs — T8-2 E3 and T8-1 U5 are the hand-offs.
- **Honesty item 2 — drift was read, not swept.** The tsukuroi and mado
  rows read `stale` (+ mado `drift` under an uncommitted owner edit); the
  round's complete outcome for leg 2 is exactly that reading — the re-sweeps
  are round 9's leg. `moved=2` recorded; nothing re-cut to manufacture work.
- **Honesty item 3 — the census/README items are debt, not done.** Census §5
  re-pin errata and `corpus/README.md` coverage rows (rounds 6–8) stay
  unlanded; ER-2 names the census item.
- **Binding revisions.** Notes `43da70e6…` / `3da1312e…`; VER-T8 binds B2 to
  the checklist note revision; AUD-T8 binds 8 anchors to both frozen shas
  (U1: an edit after 19:25Z needs re-audit). SKILL `6753b1b2…`, ledger
  `71bc15e3…` — if the parent edits either before commit (e.g., trims), the
  anchors quoted here are the shas above.
- **Cross-lane numbers to reconcile at close.** ER-2's "six gates measured"
  spans §1's four rows + ER rows 5/6 (cite rows, not "§1's table"); SKILL's
  six-case table (`:1103-1104`) and ER-2's rows are the same cells; the
  round-9 plan's "6 cases in" dispatch frame (frozen 19:15Z) predates the
  notes — the landed case set is 4 embedded + 2 measured, and the plan's own
  clause defers to landed bytes.
- **Commit items** (lane identity + round shape; precedents through
  `9f1d3c3`): `SKILL.md` (+146/−1); `corpus/knowledge/fleet-kill-rate-ledger.md`
  (+47/−1); `corpus/knowledge/mutation-case-kagi-checklist.md`;
  `corpus/knowledge/mutation-case-kumitate-claims.md`; `reports/r8-ver-t8.md`;
  `reports/r8-aud-t8.md`; `plans/round-9.plan.md`; the round-8 record draft
  itself (precedent: round-5/6/7 drafts are committed); plus `LOG.md` +1 and
  `SCORECARD.md` +1 (not yet written — that is this draft's purpose).
- **Row convention**: round 8 is one axis with three legs; §A offers a full
  row and a stub. Rounds 4–7 landed stubs; decide the form and record either
  way.
- **Coverage-map rows** (`corpus/README.md`): add rows for the two new case
  notes, the two reports, and the still-open round-6/7 items
  (`mutation-case-mado-verify.md`, `self-hardening-r6.md`,
  `fleet-kill-rate-ledger.md`, `service-optin-protocol.md`); the round-5
  carries remain open.
- **Unlanded items to watch in round 9**: cases 5/6 embedding (the tool
  owner's call); census §5 re-pin errata; re-sweeps of tsukuroi `bba6cdf6…`
  and mado `90d50cdd…`(+ live edit) — round-9 plan leg 2; the attestation leg
  (r7 U1) still unexecuted; the fleet-contributed case; cite-check's full
  sweep (queue head, unclaimed); README rows; mado's owner-side acceptance of
  its round-8 edits; T8-1's U1–U7 and T8-2's U1–U7 and the two reports'
  unknown lists.
- **Shared scratch**: `/tmp/w8-tameshi-{t81,t83,t84,scr-t8}`,
  `/tmp/w8-t8-2-claims`, `/tmp/w8-aud-t8-{work,evidence}`,
  `/tmp/w8-ver-t8-work`; /tmp is volatile — the notes/reports carry the
  reproduce blocks, not the scratch.