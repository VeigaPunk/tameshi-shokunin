# Round-10 record draft — for the parent scribe to finalize (SCR-T10)

Drafted 2026-10-14, poll window **20:51:19Z–21:20:19Z** (60 s samples, 30
samples, `POLL DONE 2026-10-14T21:20:19Z`; assignment cap 30 min). Lane SCR-T10
(round-10 scribe prep). This file carries: **Round-10 shape** (planned vs
realized), **0** landing status + corrections ledger, **A** the SCORECARD
move-log rows, **B** the LOG.md round-10 entry, **C** the SCR-T10 evidence
ledger, **D** the parent checklist. Write-scope: this file only; scratch
`/tmp/w10-tameshi-scr-t10/` (poll log `poll.log`; task `bash-x3f0w7tj`;
`pin-read.sh` / `my-pin-read-open.txt`, `open-selftest.log`,
`open-regression.log`, `open/`). Anchors: **O** observation · **I** inference ·
**U** unknown. Every cell below binds to a measured sha; nothing is carried
from a plan or a producer's prose.

## Round-10 shape — planned vs realized

- **Planned** (`plans/round-10.plan.md`, 254 L / 17671 B / `d130596ac8bc7e91`,
  committed at `b8eb96e`; ufo-round-plan-v1): axis move **operability,
  terminal — the closeout: the ten rounds' product is handed to the operator as
  one runbook.** ONE move, three ordered legs (plan `:48-107`):
  1. **Leg note** — the handoff lands as `HANDOFF.md` at the repo root
     (synthesis spine + runbook; every claim line carrying its anchor; "adds no
     gate measurement"); relocation allowed if the coverage row moves with it.
  2. **Leg execution** — the runbook is executed by its author lane and pasted:
     the tick (pin read + `--selftest` + `--regression`), the append discipline
     demonstrated on a scratch copy, and one executed reading per trigger class
     the state provides (T1/T2/T3); a class the state does not provide is
     recorded as not exercised.
  3. **Leg sufficiency** — a fresh executor with no tameshi context beyond the
     note reproduces the operator loop (tick; the sweep path once; one refusal
     reading; the append discipline on a scratch copy) plus the falsifier pair;
     verdict vocabulary SUFFICIENT / SUFFICIENT (latitude) /
     ADDITIVE-IMPROVISATION / NOT EXERCISED / ADAPTED; contamination statement;
     evidence dir.
- **Case frame** (plan, re-measured at this window's open and close, §0.1/§0.2):
  **6 cases = 4 `current` · 2 `stale` · 0 `drift`** at both my reads; tool
  `held` at the open read, **moved** during the round (below).
- **Realized at this window's close — the runbook landed, executed, and
  audited; the leg cut resolved as an embedding; two legs stay open:**
  1. **The handoff landed — relocated.** `corpus/knowledge/operator-runbook.md`
     (lane T10-1): `e1e349b6…`, 511 `wc -l` / 31 416 B, mtime 20:57:29Z,
     untracked at close. Its own credit line: "Landed at
     `corpus/knowledge/operator-runbook.md` per the round-10 dispatch (T10-1)"
     — the plan's proposed repo-root `HANDOFF.md` does not exist at any read in
     this window ([O], `ls HANDOFF.md` absent ×30 samples; relocation is the
     plan's own allowed form, `:48-52`). Contents measured: §0 quick start · §1
     service in one page · §2 the tool · §3 the six-case ledger (rate sequence
     80·80·60·40·47·70 restated) · §4 the opt-in protocol · §5 the limits
     (a–j) · §6 the cadence (reading map + T1–T3) · §7 the regression mode · §8
     the operator's full loop · §9 executed receipts · §10 unknowns carried ·
     append-only errata **ER-R1, ER-R2** (`grep -c '^\*\*ER-R'` = 2).
  2. **Leg execution — receipts executed by its author (T10-1) at `cf41efaa…`
     (r7-1, four legs):** tick 20:52:19Z (`current=4 stale=2 drift=0`, tool
     held; pin-read.txt + pin-read-shas.txt), `--selftest` 67/67 rc 0,
     `--regression` `cases=4 passed=4` rc 0 (`REGRESSION_DATE
     2026-10-14T20:51:32Z`), append drill on a scratch copy (`ledger-copy.md`;
     pre-append **36 169 B byte-identical**; real ledger sha unchanged;
     drill row `DR-1`), reader-side drift falsifier
     (`falsifier/surface-census-drifted.sh`). ER-R1/ER-R2 then record the
     instrument moving under it and name the remedy ("**T2 is the fix** — when
     the edit lands, re-run `--selftest` and `--regression` under the new
     revision and record both pins"); the T2 receipt is the round's own
     six-leg evidence (§ below).
  3. **Leg sufficiency — open at close.** VER-T10 (cold-reader seat) polled
     20:52:32–21:02:32Z for a `*handoff*` file (21 iterations, all `absent` —
     the artifact is `operator-runbook.md`; the poll pattern never matches it),
     then executed the loop from the runbook anyway 21:04:58–21:06:47Z: tool
     `75ed934d…` before=after, `--selftest` rc 0, **six-leg `--regression`
     PASS (`cases=6 passed=6`, 21:05:10Z, rc 0)**, pin read written
     (`run/pin-read.log`). Its per-case `reading:` classifier is an
     executor-side artifact: it compares an 8-char pin against 16-char shas
     (`run_case … 83016d45` vs `head_blob 83016d45049b009a`), so five
     `current` cells print `stale` while the printed shas show
     live = HEAD blob = pin (recorded, not smoothed — do not quote those
     `reading:` lines as readings). No `reports/r10-ver-t10.md`, no refusal
     reading, no sweep-path run, no append drill from that seat at close [O] —
     **the sufficiency table and the falsifier pair are not yet reported**.
  4. **The round-8 4-vs-6 leg cut resolved — an embedding, not a re-cut
     (T10-2, r10-2).** `tools/mutate-and-run.sh`: `cf41efaa…` (1 341 L) → …
     → **`75ed934dc86360f5…`** (1 642 L / 77 904 B, `VERSION
     mutate-and-run.sh r10-2`), first stable in this lane's samples at sample
     10 (21:00:19Z), unchanged through close; `+361/−60` vs HEAD blob. Cases
     5/6 (kagi `checklist-run.sh`, kumitate `claims-check.mjs`) are embedded as
     legs 5/6; `REGRESSION_EXPECT` lists six recorded rates. The checklist leg
     first read **SETUP** (control red, every case exit 126 — the
     materialized blob lacked the exec bit; T10-2's `regression.log` 20:57:14Z,
     `REGRESSION: SETUP (cases=6 passed=5 cannot-verify=1)`): fixed in r10-2 by
     **mirroring the blob mode** (`100755` → `chmod +x`, selftest arms added).
     Six-leg receipts at `75ed934d…`, four independent lanes, all
     `PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`:
     T10-2 21:00:24Z (own `regression2.log`, rc 0; `selftest3.log` 80/80) ·
     AUD-T10 21:01:53Z · T10-4 21:02:39Z · VER-T10 21:05:10Z.
  5. **Companion round-10 artifacts.** T10-3 → `corpus/knowledge/
     service-standing-state.md` (`d326c1a4…`, 242 L / 17 513 B; the
     fleet-visible vs lane-owned boundary table; 16 handoff conditions; SC1–SC3;
     ER-1 records the tool move). T10-4 → the **SKILL.md round-10 section**
     (+94/−1; 1 269 → 1 362 `wc -l`; `ee09c3bd…` → `ff566814…`): the runbook's
     section map + the six-leg registry + this round's receipt (its own
     `--selftest` 80/80 and `--regression` at `75ed934d…`), the exec-bit mirror
     rationale, and the named debt that "the ledger's §1 embedding text still
     reads 'cases 1 and 2 only'" (a ledger row recording the six-leg registry
     is the ledger owner's follow-on). AUD-T10 → `reports/r10-aud-t10.md`
     (`84837d2c…`, 228 `wc -l` / 16 542 B, mtime 21:06:45Z): a 12-row verdict
     table — **CONFIRMED ×8**, P1/P2 cold reads `SUFFICIENT (latitude)` (with a
     declared-contamination statement), **finding row 7: the runbook's
     §2/§3/§7 "four legs / cases 5–6 not embedded" lines are STALE against the
     tool that will ship in the same commit** (anchored source governs; ER-R1/R2
     predate the landing), row 11 **AMBIGUOUS** on the `held|moved` anchor.
  6. **Next round's design landed inside the window:** `plans/round-11.plan.md`
     (PREP-T11, 300 L / 20 935 B / `068578f198367b79`; §0 notes the dispatcher's
     round-11 supersedes the round-10 plan's "no round 11" prose and records
     the disagreement, not smoothed).

## 0. Landing status

### 0.1 Baseline at window open (measured 20:51–20:53Z)

- HEAD `b8eb96e` ("probation round 9 (training r8): see LOG"); `git status
  --porcelain` **empty** at 20:50Z reads; no `.ufo/waves/tameshi-r10-*`
  directory exists ([O] — the lane deliverables in this repo ARE the wave
  record, rounds 1–9 precedent).
- Cells (this lane's reads; sha = first 16 hex):
  - `tools/mutate-and-run.sh` `cf41efaa8be5f52d…` 1 341 L / 61 632 B (r7-1,
    **held** = ER-4's pin `fleet-kill-rate-ledger.md:320`)
  - `SKILL.md` `ee09c3bddb6cc705…` 1 269 L / 85 320 B (round-9 revision)
  - `fleet-kill-rate-ledger.md` `2f25c51e3e0a7851…` 363 newlines / 36 169 B
    (ER-4 `:318` + addendum `:356`; **no ER-5**)
  - `LOG.md` `38bd067ad4b851e1…` 308 L (round-9 stub `:308`); `SCORECARD.md`
    `b81e582efb1da8e1…` 22 L (round-9 stub `:22`)
  - `corpus/README.md` `1fe3050002f54b29…` 20 L (coverage map unchanged since
    round 8 — carried debt)
  - `service-optin-protocol.md` `84d0c1547eed257d…` 286 L; `service-limits.md`
    `a57a1e69be02896a…` 276 L; `plans/round-10.plan.md` `d130596ac8bc7e91…`
    254 L; `reports/` held exactly the five r7–r9 files.
- **Baseline pulse (this lane).** `--selftest` → `MUTATE_SELFTEST: 67/67 pass`
  / `VERDICT: PASS`, rc 0 (`/tmp/w10-tameshi-scr-t10/open-selftest.log`,
  end 20:52:02Z); `--regression --workdir /tmp/w10-tameshi-scr-t10/open/regr` →
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0
  flips<=0)`, `REGRESSION_DATE 2026-10-14T20:52:02Z`, rc 0, every leg
  `match=10/10 … flips=0` (`open-regression.log`). Tool `cf41efaa…` in both.
- **Baseline pin read (this lane, 20:53:39Z; read-only; ER-3's command set).**
  **4 current · 2 stale · 0 drift**: kimi-census `83016d45…` current;
  surface-census `275d8294…` current; tsukuroi-census `084951be…` → live
  `c396662e…` **stale** (HEAD `fac745b2`, path clean); mado-verify
  `d7edaab4…` → live `93e43f8f…` **stale** (HEAD `de22dfde`, path clean);
  checklist-run `7e5ec98b…` current; claims-check `e9a21b44…` current. All six
  recorded revs ancestor-of-HEAD (rc 0 ×6). The two moved cells are **past**
  ER-4's tick readings (`bba6cdf6…` @ `72b038d` → now `c396662e…` @ `fac745b2`;
  `7da4ec50…` @ `12c8f08` → now `93e43f8f…` @ `de22dfde`): the owners'
  round-9 commits (17:47:30 −03:00 = 20:47:30Z) landed between rounds.
- Round-10 lanes already visible at open ([O], `/tmp`): `/tmp/w10-t10-1`
  (initial-state, selftest, regression), `/tmp/w10-t10-3` (pin read + selftest
  tail), `/tmp/w10-t10-4-ev` + `w10-t10-4-poll.sh` (state poller), plus
  sibling-repo lanes (`w10-mado-m10-*`, `w10-tsukuroi-s10*`, `w10-tabi-*`,
  `w10-m10-1`, `w10-scrb10`, …).

### 0.2 Measured at window close (this lane, 21:20–21:21Z; poll ran to 21:20:19Z)

`git status --porcelain` at close: ` M SKILL.md`, ` M tools/mutate-and-run.sh`,
`?? corpus/knowledge/operator-runbook.md`,
`?? corpus/knowledge/service-standing-state.md`, `?? plans/round-11.plan.md`,
`?? reports/r10-aud-t10.md` — exactly the round-10 writes this lane saw.

| artifact | close cell | note |
|---|---|---|
| `SKILL.md` | 1 362 `wc -l` / 91 418 B / `ff56681441aec2ea` | +94/−1 vs HEAD `ee09c3bd…`; round-10 section heading `:1272` "The operator's runbook and the six-leg regression (round 10, measured)"; first seen 21:06:19Z, stable through close |
| `tools/mutate-and-run.sh` | 1 642 L / 77 904 B / `75ed934dc86360f5` | r10-2; **moved** from `cf41efaa…` (r7-1); +361/−60; stable in my samples from 21:00:19Z |
| `corpus/knowledge/operator-runbook.md` | 511 `wc -l` / 31 416 B / `e1e349b69d798acb` | T10-1; mtime 20:57:29Z; untracked; first seen by me 21:01:45Z, stable through close |
| `corpus/knowledge/service-standing-state.md` | 242 L / 17 513 B / `d326c1a4d61c9705` | T10-3; stable at every read |
| `plans/round-11.plan.md` | 300 L / 20 935 B / `068578f198367b79` | PREP-T11; edited in place 20:56:20 → 20:57:22Z (`9df6d9fa…` → `068578f1…`), stable after |
| `reports/r10-aud-t10.md` | 228 `wc -l` / 16 542 B / `84837d2cca2e2962` | AUD-T10; mtime 21:06:45Z; 12-row verdict table |
| `reports/r10-ver-t10.md` | **ABSENT** | VER-T10 executed (run/ logs) but no report at close |
| `fleet-kill-rate-ledger.md` | 363 newlines / 36 169 B / `2f25c51e3e0a7851` | **unchanged all window** — no ER-5, no appended rows; §1–§4 stand |
| `LOG.md` / `SCORECARD.md` | 308 L / 22 L, unchanged | writing the r10 rows is this draft's purpose |
| `corpus/README.md` | 20 L / 12 182 B / `1fe3050002f54b29` | unchanged — coverage rows unlanded |
| `service-optin-protocol.md` / `service-limits.md` | `84d0c154…` 286 L · `a57a1e69…` 276 L | unchanged |
| sibling trees | kumitate `175de6b` clean · kagi `fecee87` clean · tsukuroi `fac745b` **` M tools/tsukuroi-census.sh`** · mado `de22dfde` clean | tsukuroi's own round-10 lane is editing its gate again (path-scoped porcelain) |

### 0.3 Corrections ledger — what moved during the window (append-only)

| cell | at open | during/at close | reading |
|---|---|---|---|
| tool | `cf41efaa…` 1 341 L, = HEAD blob, held | `…b4af796e`/1 358 → `ac779b91`/1 373 → `5807fd38`/1 547 → `c4b2ae0a`/1 567 → `46877c8b`/1 634 → **`75ed934d`/1 642** (my samples); the audit's finer list adds `818889d0`/1 358, `8624cf7d`/1 359, `efe38d2f`/1 497, `4b3dfed5`/1 509, `17208c11` (r10-aud-t10.md §0) | **moved** — the round's own T2: every receipt must cite the pin that ran; the runbook's §2/§3/§7 text still names the four-leg r7-1 revision (AUD-T10 row 7, STALE) |
| runbook | absent | first written ~20:53Z (`ed73e302`/480) → `6d3a87e8` → `766879ac`/480 → `fafda12d`/498 → `309528e9`/500 → `5c1416bd`/501 (my 20:57:22Z read) → **`e1e349b6`/511**, mtime 20:57:29Z, stable from 21:01:45Z through close | landed + two errata appends |
| standing-state note | absent | `d326c1a4`/242 stable from first sight (20:57:22Z) | landed |
| round-11 plan | absent | `9df6d9fa`/300 (20:56:20Z) → `068578f1`/300 (20:57:22Z) | landed + in-place edit |
| SKILL | `ee09c3bd…` 1 269 L / 85 320 B | `ff566814…` 1 362 L / 91 418 B; +94/−1 | round-10 section (T10-4) |
| ledger | `2f25c51e…` 363 / 36 169 B | `2f25c51e…` **unchanged** at every sample | the round-10 rows/errata not landed |
| reports | 5 files (r7–r9) | + `r10-aud-t10.md` (21:06:45Z) | audit landed; verifier report open |
| tsukuroi gate | live `c396662e…` = HEAD blob, path clean (20:53:39Z) | worktree `10452443…` at 21:03:26Z (AUD-T10 p1d) → ` M` at close | **stale + drift** at close — owner's own lane mid-edit; every cell a timestamped reading |
| mado gate | live `93e43f8f…` = HEAD blob, path clean | clean at every read | **stale**, clean |
| `corpus/README.md` / LOG / SCORECARD | unchanged | unchanged | coverage + house rows not yet written |

## A. SCORECARD.md — move-log row (append after the round-9 row at `:22`)

Precedent: rounds 4–9 landed as terse one-line stubs. Round 10 is ONE move
(operability: the closeout — the runbook handed to the operator; the leg cut
resolved as an embedding). **Honesty constraints:** the row must render the two
stale-gate re-sweeps as OPEN (no appended rows), the runbook as landed but
**uncommitted**, the tool as **moved** (not held), and the fresh-executor table
as not yet reported.

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 10 | operability | round-9 state: the cadence's first tick recorded (4/4 legs PASS) but the operator had no single entry point; the registry ran **four** legs (cases 5/6 "not embedded — named debt"); both moved gates `stale` with no re-sweep rows | **the closeout:** `corpus/knowledge/operator-runbook.md` lands (lane T10-1; `e1e349b6…` 511 L / 31 416 B; tool + six-case ledger + protocol + limits + cadence + regression, every line anchored — relocated from the plan's repo-root `HANDOFF.md` per the dispatch) with its receipts executed by the author (tick 20:52:19Z: 4 current · 2 stale · 0 drift; `--selftest` 67/67; `--regression` cases=4 passed=4; append drill on a scratch copy pre-append 36 169 B byte-identical, real ledger sha unchanged; drift falsifier) and the tool-drift errata ER-R1/ER-R2 naming T2; the leg cut **resolves as an embedding** (T10-2 r10-2, `75ed934d…` 1 642 L / +361−60): cases 5/6 = legs 5/6, the checklist leg's control initially SETUP (exit 126, exec bit) then fixed by the blob-mode mirror, **six-leg `--regression` PASS (cases=6 passed=6) recorded by four independent lanes** (T10-2 21:00:24Z · AUD-T10 21:01:53Z · T10-4 21:02:39Z · VER-T10 21:05:10Z; `--selftest` 80/80); companion: T10-3 boundary note `service-standing-state.md` (fleet-visible vs lane-owned, 16 handoff conditions, SC1–SC3), T10-4 SKILL round-10 section (+94/−1), `reports/r10-aud-t10.md` (12-row verdict table: CONFIRMED ×8, P1/P2 SUFFICIENT (latitude) with contamination statement; **finding: the runbook's four-leg lines stale at the landed revision**), PREP-T11's `plans/round-11.plan.md`; **open at close:** the two `stale` gates' re-sweeps (ledger byte-identical `2f25c51e…`, no appended rows), the fresh-executor sufficiency table (`r10-ver-t10.md` absent; VER-T10 executed the loop 21:04–21:06Z), the coverage-map rows, a ledger row for the six-leg registry | my pulse at `cf41efaa…` (selftest 67/67 rc 0; regression cases=4 passed=4, `REGRESSION_DATE 20:52:02Z`); my six-case pin read 20:53:39Z → 4 current · 2 stale · 0 drift (tsukuroi `084951be…`→`c396662e…`; mado `d7edaab4…`→`93e43f8f…`, both = HEAD blobs, ancestors yes, trees clean); tool trajectory per §0.3; T10-2 `regression2.log` (`REGRESSION: PASS (cases=6 passed=6…)`, rc 0) + `selftest3.log` 80/80 at `75ed934d…`; AUD-T10 §2 six-leg table + leg-check `LEGCHECK: PASS (6/6 legs clean)`; VER-T10 `run/regression.log` `PASS (cases=6 passed=6)`, `bounds.log` tool-sha before=after `75ed934d…`; my `diff` of the ledger → unchanged; `grep -c '^\*\*ER-R'` on the runbook → 2 (ER-R1/R2). Re-run 2026-10-14 (SCR-T10) |

Stub form (rounds 4–9 convention):

```
| 10 | operability | round-9: cadence ticked; 4-leg cut; no operator entry point; 2 stale gates | the closeout — operator runbook lands (corpus/knowledge/operator-runbook.md, T10-1; executed tick 4 current/2 stale/0 drift; append drill; drift falsifier) + the 4-vs-6 leg cut resolves as an embedding (r10-2: cases 5/6 as legs 5/6; selftest 80/80; six-leg regression PASS cases=6 passed=6 ×4 lanes; exec-bit mirror fix) + boundary note (T10-3) + SKILL r10 section (T10-4) + AUD-T10 (finding: runbook 4-leg lines stale at landed r10-2); open: 2 stale-gate re-sweeps, executor sufficiency table | wave-10 32-lane + SCR-T10 |
```

*(Derivation note [I]: "wave-10 32-lane" follows the landed stub convention
(`SCORECARD.md:17-22`); the dispatcher's own label wins if different.)*

## B. LOG.md — round-10 entry (append as a new bullet after the round-9 entry at `:308`)

**Stub (recommended — the landed convention, rounds 4–9):**

```
- 2026-10-14 — round 10 (training r9): the operator closeout — corpus/knowledge/operator-runbook.md lands (T10-1; tool + six-case ledger + protocol + limits + cadence + regression, every line anchored; executed tick 4 current/2 stale/0 drift; append drill; drift falsifier) and the round-8 4-vs-6 leg cut resolves as an embedding (T10-2 r10-2: cases 5/6 as legs 5/6; selftest 80/80; six-leg --regression PASS cases=6 passed=6, four independent receipts) with the exec-bit mirror fix; companion notes: service-standing-state.md (T10-3) + SKILL r10 section (T10-4) + AUD-T10 (finding: the runbook's 4-leg lines stale at the landed revision). Open: the two stale gates' re-sweeps (no appended rows; ledger unchanged), the fresh-executor sufficiency table (VER-T10 executed the loop; report not landed), coverage rows. Axis: operability. Verifiers: AUD-T10 | VER-T10 (cold read).
```

**Full form (if the parent wants the detail inline):**

- 2026-10-14 — round 10: planned as a ufo-round-plan (`plans/round-10.plan.md`,
  ufo-round-plan-v1 — axis move **operability, terminal**: the closeout, the
  ten rounds' product handed to the operator as one runbook; three legs: note ·
  execution · fresh-executor sufficiency). Same dispatch shape as rounds 1–9 —
  lane write-scopes leave this LOG to the scribe; the lane deliverables in this
  repo ARE the wave record (no `.ufo/waves/tameshi-r10-*` directory).
  TAMESHI-T10-1 → `corpus/knowledge/operator-runbook.md` (**new**; 511 `wc -l` /
  31 416 B / `e1e349b6…`; relocated from the plan's repo-root `HANDOFF.md` per
  its dispatch; §0–§10 + errata ER-R1/ER-R2): the operator's single entry point —
  tool + six-case ledger + opt-in protocol + limits + cadence + regression mode,
  every line restating an anchored source; receipts executed at `cf41efaa…`
  (tick 20:52:19Z 4 current · 2 stale · 0 drift; selftest 67/67; regression
  cases=4 passed=4 `REGRESSION_DATE 20:51:32Z`; append drill on a scratch copy —
  pre-append 36 169 B byte-identical, real ledger sha `2f25c51e…` unchanged;
  reader-side drift falsifier); ER-R1/ER-R2 record the instrument moving and
  name the T2 remedy.
  TAMESHI-T10-2 → `tools/mutate-and-run.sh` **r10-2** (`cf41efaa…` r7-1 1 341 L
  → `75ed934d…` 1 642 L / 77 904 B, +361/−60): cases 5/6 embedded as legs 5/6 —
  the round-8 leg cut resolved as an embedding, never a re-cut; the checklist
  leg's control first read SETUP (exit 126 — no exec bit on the materialized
  blob) and is fixed by mirroring the blob mode (`100755` → `chmod +x`, new
  selftest arms); `--selftest` 80/80; six-leg `--regression`
  `PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`.
  TAMESHI-T10-3 → `corpus/knowledge/service-standing-state.md` (**new**;
  `d326c1a4…` 242 L / 17 513 B): the boundary table — fleet-visible vs
  lane-owned, 16 handoff conditions each anchored, SC1–SC3 (pin read; the
  write-boundary text on live bytes; visibility-by-citation counts
  kumitate 0 · kagi 0 · tsukuroi 12 · mado 19; README covers 6 of 16 notes);
  ER-1 records the tool move.
  TAMESHI-T10-4 → `SKILL.md` round-10 section (+94/−1; 1 269 → 1 362 `wc -l`;
  `ee09c3bd…` → `ff566814…`): the runbook's section map, the six-leg registry
  and this round's T2 receipt at `75ed934d…` (its own selftest 80/80 and
  six-leg regression 21:02:39Z), the exec-bit mirror rationale, and the named
  ledger follow-on (the ledger's §1 embedding text still reads "cases 1 and 2
  only").
  AUD-T10 (audit lane, read-only) → `reports/r10-aud-t10.md` (**new**;
  `84837d2c…`, 228 `wc -l` / 16 542 B, mtime 21:06:45Z): a 12-row verdict
  table — CONFIRMED ×8 (the runbook landed and is runnable; selftest at both
  revisions 80/80 & reproduced 67/67; the six-leg regression with 6/6
  independent leg-check; the append proof; the falsifier), P1/P2 cold reads
  `SUFFICIENT (latitude)` with a declared-contamination statement, **row 7 the
  finding**: the runbook's §2/§3/§7 four-leg / "cases 5–6 not embedded" lines
  are **stale** against the landed r10-2 (anchored source governs; ER-R1/R2
  predate the landing); row 11 ambiguous on the `held|moved` anchor; row 12
  confirms the audit wrote nothing but its report.
  VER-T10 (cold-reader seat) → ran the operator loop from the runbook
  21:04:58–21:06:47Z (tool `75ed934d…` before=after; selftest rc 0; six-leg
  regression `PASS (cases=6 passed=6)`, 21:05:10Z; scratch
  `/tmp/w10-ver-t10-ev/run/`), but its poll never matched the artifact's name
  (`*handoff*` vs `operator-runbook.md`, 21 iterations `absent`) and **no
  `reports/r10-ver-t10.md` landed at close** — the sufficiency table and
  falsifier pair named in the plan's leg 3 remain unreported; its pin-read
  classifier compares 8-char pins to 16-char shas (five `current` cells print
  `stale`; the printed shas are the evidence).
  PREP-T11 (design lane) → `plans/round-11.plan.md` (**new**; 300 L /
  20 935 B / `068578f1…`): the next round's plan; its §0 records that the
  dispatcher's round-11 supersedes the round-10 plan's "no round 11" prose.
  Scribe verification (this draft, SCR-T10; scratch `/tmp/w10-tameshi-scr-t10/`):
  baseline pulse at open (selftest 67/67 rc 0; regression cases=4 passed=4,
  `REGRESSION_DATE 20:52:02Z`, rc 0) and the six-case pin read at 20:53:39Z
  (4 current · 2 stale · 0 drift; both moved cells = HEAD blobs, ancestors yes,
  trees clean); the tool's move to `75ed934d…` sampled every 60 s (stable from
  21:00:19Z); the ledger **byte-identical all window** (`2f25c51e…`) — the
  round-10 re-sweeps did **not** land.
  SCORECARD round-10 move: operability improved (the operator's single entry
  point lands with executed receipts; the leg cut resolves as an embedding with
  four independent six-leg receipts; the boundary note and audit land) — the
  two stale-gate re-sweeps, the fresh-executor sufficiency table, and the
  coverage rows stay **open, named debt**.
  Carried to round 11: the two re-sweeps at their measured revisions (T1) —
  tsukuroi live `c396662e…` (worktree drifting again at close), mado live
  `93e43f8f…`; a ledger row for the six-leg registry (the ledger's §1 text
  "cases 1 and 2 only" is superseded by ER-2 `:281` for four legs and now by
  r10-2 for six); the census §5 instrument re-pin errata;
  `corpus/README.md` coverage rows (rounds 6–10 notes + r9/r10 reports; the
  runbook's row moves with its `corpus/knowledge/` relocation); attestation leg
  (r7 U1); fleet-contributed case; cite-check's full sweep.

## C. SCR-T10 evidence ledger (measured by this lane; scratch `/tmp/w10-tameshi-scr-t10/`)

1. **Baseline pulse (20:51:5x–20:52:48Z).** `open-selftest.log`: `MUTATE_SELFTEST:
   67/67 pass` / `VERDICT: PASS`, rc 0. `open-regression.log`: `REGRESSION:
   PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`,
   `REGRESSION_DATE 2026-10-14T20:52:02Z`, per-leg `match=10/10` killed
   8/8/6/4 `flips=0`, rc 0, tool `cf41efaa…` in `REGRESSION_TOOL`.
2. **Six-case pin read (20:53:39Z, read-only; `pin-read.sh` →
   `my-pin-read-open.txt`).** Per case `sha256sum <live>` ·
   `git show HEAD:<path> | sha256sum` · `git status --porcelain --
   <path>` · `merge-base --is-ancestor <rev> HEAD` → 4 current · 2 stale ·
   0 drift; tsukuroi `084951be…`→`c396662e…` (HEAD `fac745b2`), mado
   `d7edaab4…`→`93e43f8f…` (HEAD `de22dfde`); all six paths clean at the read.
3. **Poll (20:51:19–21:20:19Z; 30 samples × 60 s; `poll.log`).** Cells:
   ledger `2f25c51e…` **unchanged every sample**; LOG/SCORECARD/README/
   protocol/limits unchanged; tool trajectory §0.3 (mine); worktree first shows
   `?? operator-runbook.md` + `?? service-standing-state.md` at sample 5
   (20:55:19Z; runbook `e1e349b6…` 511 L from 21:01), `?? plans/round-11.plan.md`
   at sample 7 (20:57:19Z); SKILL `ff566814…`
   1 362 L from sample 16 (21:06:19Z); `r10-aud-t10.md` first seen sample 16;
   `HANDOFF.md ABSENT` all 30 samples; `plans/round-10-record-draft.md ABSENT`
   (this file).
4. **Ledger append-drill check (mine, 20:53Z).** `diff` of live ledger vs
   `/tmp/w10-t10-1/ledger-copy.md` → `364c364,365` (the live file's unterminated
   final line terminated + the `DR-1` drill row appended; 36 287 B copy vs
   36 169 B live) — the drill ran on the copy only; live sha unchanged.
5. **Cross-lane reads (read-only; attribution from file credits + scratch
   names, not from a dispatch this lane saw [U]).** `/tmp/w10-t10-1/`
   (`initial-state.txt`, `selftest.log`, `regression.log` 20:51:32Z,
   `pin-read.txt` 20:52:19Z, `pin-read-shas.txt`, `ledger-copy.md`,
   `falsifier/surface-census-drifted.sh`); `/tmp/w10-tameshi-t10-2/`
   (`pinned-checklist-run.sh`, `pinned-claims-check.mjs`, `selftest3.log`
   80/80, `regression.log` 20:57:14Z SETUP leg 5 → `regression2.log` 21:00:24Z
   `cases=6 passed=6` rc 0, `regression/specs/*.spec` 6 files);
   `/tmp/w10-t10-3/` (`pin-read.txt` 20:52:11Z, `selftest-tail.txt`);
   `/tmp/w10-t10-4-ev/` (`initial-state.txt`, `poll.log`, `poll2.log`,
   `selftest.log` 80/80, `regression.log` 21:02:39Z, `tool-at-run.txt`);
   `/tmp/w10-ver-t10-ev/` (`poll.log` 21 iterations absent, `run/bounds.log`
   tool before=after `75ed934d…`, `run/selftest.log`, `run/regression.log`
   21:05:10Z, `run/pin-read.log`, `regression/`, `pin-read.sh`);
   `/tmp/w10-aud-t10-work|ev/` (baseline, poll/poll2/stability logs,
   `leg-check.py`, `legcheck.txt`, `head-replay.log`, `p1*-*.log/txt`,
   `p2-append-drill.txt`, `falsifier-drift.txt`).
6. **The audit's report read at its bytes** (`reports/r10-aud-t10.md`,
   `84837d2c…`): 12-row verdict table; six-leg table (§2); finding (§3);
   verdicts and unknowns quoted in §B/§D.
7. **Minor discrepancy, recorded.** AUD-T10 §0's stability narrative dates the
   runbook's `e1e349b6`/511 L as stable "from 20:56:13Z"; my own reads show
   501 L (`5c1416bd`) at 20:57:22Z and 511 L first at 21:01:45Z, and the
   audit's own `poll2.log` lines sit between (`fafda12d`/498 at 20:56:33Z,
   `309528e9`/500 at 20:56:53Z); its freeze-table mtime (20:57:29Z) agrees with
   my reads — [I] a summarization date slip in one sentence, end cells agree.
8. **Unknowns from this lane.** (i) **The two stale-gate re-sweeps did not
   land**: the ledger is byte-identical (`2f25c51e…`, +0/−0), no ER-5, no new
   case notes; both rows carry T1-live triggers at close (tsukuroi additionally
   `drift` — its own lane is editing). (ii) **The fresh-executor sufficiency
   table is unreported**: VER-T10 executed the loop (selftest + six-leg
   regression + a pin read) but wrote no report, no refusal reading, no
   sweep-path run, no append drill; its registry-vs-artifact name mismatch
   (`*handoff*` vs `operator-runbook.md`) is a live coordination fact for the
   parent. (iii) The runbook's §2/§3/§7 four-leg lines are stale at the landed
   r10-2 (the audit's finding) — a re-stamp (ER-R3) or a §-edit is the author
   lane's call, not this draft's. (iv) The ledger's §1 embedding text
   ("cases 1 and 2 only") is superseded by ER-2 `:281` (four legs) and now by
   r10-2 (six legs) with no ledger row recording the six-leg registry (named in
   the SKILL section as the ledger owner's follow-on). (v) Lane role labels
   (T10-1…T10-4, VER-T10, AUD-T10, PREP-T11) are from file credits and scratch
   names; the dispatch itself was not visible. (vi) Single host (`plazir27`),
   2026-10-14 — no cross-host reading; timings are host-local. (vii) All
   round-10 writes are **uncommitted** at close (HEAD `b8eb96e`); every cell
   here binds to the worktree revisions measured, and the parent's commit is
   the landing. (viii) Whether the operator adopts the runbook is [U] — the
   round lands the runbook, not its use.

**Spot-checks (three, all run this session).**

- **SC1 — the pulse pair at both revisions.** Mine at `cf41efaa…`: selftest
  67/67 rc 0 + regression cases=4 passed=4 (`REGRESSION_DATE 20:52:02Z`) —
  agreeing with T10-1's 20:51:32Z/20:52:19Z runs and T10-3's selftest tail
  (67/67). At the landed `75ed934d…`: four independent lanes' receipts
  (T10-2 `80/80` + `cases=6 passed=6` 21:00:24Z; AUD-T10 80/80 + 21:01:53Z;
  T10-4 80/80 + 21:02:39Z; VER-T10 rc 0 + 21:05:10Z) — the instrument's own
  gates green at every revision in the record.
- **SC2 — the six-case pin read, four lanes agreeing per timestamp.** Mine
  20:53:39Z (4 · 2 · 0), T10-1's 20:52:19Z (4 · 2 · 0), T10-3's 20:52:11Z
  (4 · 2 · 0), AUD-T10's 21:03:26Z (4 · 1 · 1 — tsukuroi's own writer made row
  3 `stale + drift`); the moved cells (`084951be…`→`c396662e…`;
  `d7edaab4…`→`93e43f8f…`) and the ancestor checks agree everywhere; the
  readings follow the pins, and VER-T10's `reading:` lines are its script's
  8-vs-16-char artifact (its printed shas are correct).
- **SC3 — the landed bytes.** Ledger: byte-identical all window (`2f25c51e…`,
  my poll ×30; my `diff` of T10-1's copy proves the drill stayed on the copy).
  SKILL: `+94/−1` append of the round-10 section (the one removed line is the
  round-9 revision's unterminated final line being terminated — same
  shape as round 9's own landing). Runbook: read end-to-end at `e1e349b6…`
  (511 lines; §0–§10 + ER-R1/R2); its receipts were replayed at the HEAD blob
  by AUD-T10 (`head-replay.log`, `head-selftest.txt` → 67/67 + cases=4).

## D. Parent checklist (round close)

- **Honesty item 1 — the tool MOVED; cite the pin that ran.** `cf41efaa…`
  (r7-1, four legs) is what the runbook's §2/§7/§9 receipts were executed at;
  **`75ed934d…`** (r10-2, six legs) is the landed revision. Do not render the
  round's instrument as "held". The runbook's
  §2/§3/§7 text still describes four legs (AUD-T10 finding row 7) — reconcile
  at commit (re-stamp via ER-R3, or accept the divergence with the runbook's
  own "anchored source governs" rule).
- **Honesty item 2 — the runbook landed RELOCATED.** Path
  `corpus/knowledge/operator-runbook.md`, not repo-root `HANDOFF.md`; no
  `HANDOFF.md` existed at any read in this window. VER-T10's and T10-4's polls
  watched `HANDOFF.md`/`*handoff*` and logged `absent` throughout — record the
  relocation wherever the wave's expectations are written, and give the
  coverage row the new path.
- **Honesty item 3 — the two re-sweeps are OPEN.** Ledger byte-identical
  (`2f25c51e…`); no ER-5, no appended rows. tsukuroi `084951be…` → live
  `c396662e…` (`fac745b2`; worktree drifting again at close), mado
  `d7edaab4…` → live `93e43f8f…` (`de22dfde`). Any re-sweep is a new
  pre-registered spec at the revision it measures (T1; re-pin rule).
- **Honesty item 4 — the fresh-executor table is NOT reported.** VER-T10
  executed the loop at `75ed934d…` but no `r10-ver-t10.md`, no refusal reading,
  no append drill, no falsifier pair at close; its `reading:` classifier is
  buggy (8 vs 16 chars) — the parent should re-run or re-seat that leg before
  rendering leg 3 as done; NOT EXERCISED / partial is the honest current state.
- **Binding revisions.** SKILL `ff566814…` (1 362 `wc -l` / 91 418 B; round-10
  section heading `:1272`); tool `75ed934d…` (r10-2); runbook `e1e349b6…`
  (511 / 31 416; mtime 20:57:29Z); standing-state `d326c1a4…`; audit
  `84837d2c…` (228 / 16 542); round-11 plan `068578f1…`; ledger `2f25c51e…`
  unchanged; LOG `38bd067a…` / SCORECARD `b81e582e…` (this draft's rows land
  after). All round-10 files are **uncommitted** at close (HEAD `b8eb96e`).
- **Cross-lane numbers to reconcile.** Six-leg receipts ×4 at `75ed934d…`
  (T10-2/AUD-T10/T10-4/VER-T10) all `cases=6 passed=6`; `--selftest` 80/80 at
  the landed revision vs 67/67 at `cf41efaa…` (both true at their pins). The
  plan's "executor table" headline shape was not produced (leg 3 open). T10-2's
  first six-leg run was **SETUP** (leg 5, exit 126, 20:57Z) — do not quote it
  as the final state; the fix was the blob-mode mirror.
- **Commit items** (lane identity + round shape; precedents through `b8eb96e`):
  `SKILL.md` (+94/−1); `tools/mutate-and-run.sh` (+361/−60, r10-2);
  `corpus/knowledge/operator-runbook.md` (new, untracked);
  `corpus/knowledge/service-standing-state.md` (new, untracked);
  `reports/r10-aud-t10.md` (new); `plans/round-11.plan.md` (new, PREP-T11 —
  unless the parent's round split assigns it to the next round's commit);
  `plans/round-10-record-draft.md` (this file; precedent: rounds 4–9 drafts are
  committed); plus `LOG.md` +1 and `SCORECARD.md` +1 (not yet written — this
  draft's purpose). A `reports/r10-ver-t10.md` may land after this draft.
- **Row convention**: rounds 4–9 landed stubs; §A and §B offer full + stub.
  Decide and record either way.
- **Coverage-map rows** (`corpus/README.md`, still 20 L): add rows for the
  round-6–10 notes still uncarried (`mutation-case-mado-verify.md`,
  `self-hardening-r6.md`, `fleet-kill-rate-ledger.md`,
  `service-optin-protocol.md`, the two round-8 case notes,
  `service-limits.md`, both r9 reports, **`operator-runbook.md`** (new path),
  `service-standing-state.md`, `r10-aud-t10.md`, and `r10-ver-t10.md` if it
  lands); the census §5 re-pin errata is still unlanded (ER-2 named it).
- **Unlanded items to watch**: the two re-sweeps (T1); a ledger row for the
  six-leg registry; ER-R3 or an in-place §-edit for the runbook's four-leg
  text; the fresh-executor table + falsifier pair; cases 5/6's notes' U-items
  (T8-1 U5, T8-2 E3) now superseded by the embedding; attestation leg (r7 U1);
  fleet-contributed case; cite-check's full sweep; `r10-ver-t10.md`;
  tsukuroi's and mado's owner lanes (their gates move — the next tick re-reads
  them).
- **Shared scratch**: `/tmp/w10-t10-1`, `/tmp/w10-tameshi-t10-2`,
  `/tmp/w10-t10-3`, `/tmp/w10-t10-4-ev` (+ `w10-t10-4-poll{,2}.sh`),
  `/tmp/w10-ver-t10-ev`, `/tmp/w10-aud-t10-{work,ev}`, `/tmp/w10-audx10-*`,
  `/tmp/w10-prept11-*`, `/tmp/w10-tameshi-scr-t10` (mine); sibling lanes
  `/tmp/w10-mado-m10-*`, `/tmp/w10-tsukuroi-s10*`, `/tmp/w10-tabi-*`; /tmp is
  volatile — the notes/reports carry the reproduce blocks, not the scratch.
  Foreign scratch is never removed (limits row j).