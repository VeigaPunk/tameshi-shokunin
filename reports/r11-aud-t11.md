# AUD-T11 — verdict table: the round-11 closeout re-derived (2 claims), the 6-leg receipt re-run, the zero-debt check

Audit run 2026-10-14 21:34:07Z–21:42:47Z by lane AUD-T11 (round-11 wave; lane
scratch `/tmp/w11-aud-t11-{work,ev}/`). **Read-only: no fleet file was written
or edited by this audit.** The tameshi tree and all sibling repos were read
only; my `--regression`/`--selftest`/leg-check runs write only into
`/tmp/w11-aud-t11-*` workdirs. No substrate-mutating command; no secret file
read; no external site. The assignment was "do NOT edit" — my only fleet write
is this report (a new file), per the r7–r10 audit precedent
(`reports/r7-aud-t7.md` … `r10-aud-t10.md`).

## 0. What was audited, and the frozen revisions

| object | identity at freeze | state |
|---|---|---|
| **the closeout** — `corpus/knowledge/closeout-r11.md` (lane T11-1) | `cea3352aa60eb51b51e2722fdb820cac19cd1514670df931212904e826940265`, 420 `wc -l` / 26 695 B, mtime 21:38:56Z | untracked (`??`) at every read; same sha across ≥4 samples spanning 21:39:0x–21:41:41Z (incl. a +20 s re-read); unchanged at my close |
| the instrument — `tools/mutate-and-run.sh` | `75ed934dc86360f5…`, r10-2, 1 642 L; = blob at HEAD | committed at `606716f` |
| tameshi HEAD | `606716f703f7699af458476a31fc78ddc9bf552c` ("probation round 10 (training r9)") | throughout my window |
| the wave (concurrent, [O]) | ` M SKILL.md` (`bfbdd2fd99c36aac…`, 1 461 L); `?? plans/completion-evidence.md`; `?? corpus/lessons/round-10.md` (T11-2); `?? corpus/knowledge/closeout-r11.md` | `plans/round-11-record-draft.md` **not landed** at my close |

Contamination statement **[O]**: I had read the closeout in full, the round-11
plan, the round-10 record, the runbook, the SKILL round-11 section and the tick
lanes' scratch before re-deriving. Every re-derivation below is command-level
regardless; where a cell is a reading, it is stamped.

## 1. The closeout's claim A — re-derived: the appointment pair (§2.5)

Claim shape: *the tick was pre-announced in a committed artifact before the
wave existed, fired exactly as announced, with the delta stated.*

| step | command | observed |
|---|---|---|
| announcement committed | `git log --format='%h %cI %ct %s' -- plans/round-11.plan.md` | `606716f`, `2026-10-14T18:28:23-03:00`, `1792013303`; `TZ=UTC git show -s --format=%cd --date=iso-strict 606716f` → **2026-10-14T21:28:23Z** |
| announced bytes = committed bytes = live bytes | `git show 606716f:plans/round-11.plan.md \| sha256sum` vs `sha256sum plans/round-11.plan.md` | both `068578f198367b79…` (300 L) |
| the announced set (quoted from the committed bytes, leg 1, `:62-79`) | — | "round 8's pin read, `SKILL.md:1021-1053`; the tool pulse `--selftest` + `--regression`, `:1212-1222`; the six-case frame; the trigger rules T1–T3 with the re-pin rule; where the receipt lands" |
| the fired tick (first execution) | `/tmp/w11-t11-4-ev/pin-read.txt`; `regression.log` | pin read **21:32:35Z**; pulse `--selftest` 80/80; `--regression` `REGRESSION_DATE 2026-10-14T21:32:40Z` |
| independent firings | `/tmp/w11-t11-1/pin-read.txt`; `/tmp/w11-t11-3-ev/pin-read.txt`; my `pin-read.txt` | 21:35:54Z · 21:36:02Z · **21:37:16Z** — all `4 current · 2 stale · 0 drift` |
| "before the wave existed" | earliest round-11 lane artifacts I observe | `/tmp/w11-b11-4-pins`, `/tmp/w11-m11-1` at 21:31Z; T11-3 context 21:33:44Z — none predates 21:28:23Z |
| delta | arithmetic | 21:32:35Z − 21:28:23Z = **+4 m 12 s** → **announced**, not unannounced |

Verdict: **CONFIRMED** — the announcement precedes the firing by 4 m 12 s, and
the executed set is the announced set (pin read + selftest + regression at the
six-case frame; receipts at both lanes).

## 2. The closeout's claim B — re-derived: the tick series, one cell per receipt (§2.5)

The closeout's table carries four ticks, "each row carrying its own receipt".
I re-derived one cell per row as a non-author:

| tick | closeout cell | my re-derivation | verdict |
|---|---|---|---|
| 1 (r8) | `19:15:14Z` · `cf41efaa…` · `SKILL.md:1038`; `/tmp/w8-tameshi-t84/pin-read.txt` | SKILL.md:1038 reads "Executed instance — this lane, tick 2026-10-14T19:15:14Z, host `plazir27`, tool `cf41efaa…`"; the scratch file exists; the block carries `4 × current · 2 × stale · 0 × drift; tool held` | CONFIRMED (see finding F1) |
| 2 (r9) | `20:00:34Z` · `4 current · 2 stale · 0 drift` · `cf41efaa…` · `SKILL.md:1166`; ledger ER-4 `:318-353` | SKILL.md:1166 "Pin read at the round-9 boundary, **2026-10-14T20:00:34Z**"; ledger `:333` "target current=4 stale=2 drift=0; tool held (cf41efaa…)"; `/tmp/w9-tameshi-t93/pin-read-final.txt` exists | CONFIRMED |
| 3 (r10) | `20:52:19Z` · `4 current · 2 stale · 0 drift` · `cf41efaa…` · runbook §6/§9; round-10 record | `/tmp/w10-t10-1/pin-read.txt` header "TICK-BOUNDARY READ — 2026-10-14T20:52:19Z", rows 4/2/0; runbook §9 states "six-case pin read (§6) → current=4 stale=2 drift=0; tool held at `cf41efaa…`" | CONFIRMED |
| 4 (r11) | `21:32:35Z` (T11-4) · `21:35:54Z` (T11-1) · `4 current · 2 stale · 0 drift` · `75ed934d…` **held** | T11-4/T11-1 evidence (above) + my read 21:37:16Z, all 4/2/0; `git show 606716f:tools/mutate-and-run.sh \| sha256sum` → `75ed934d…`; held vs the r10 receipts' revision (all four r10 receipts ran at `75ed934d…`) | CONFIRMED |

- **Gap series** (the closeout: 45 m 20 s · 51 m 45 s · 40 m 16 s): recomputed
  from the four timestamps — 19:15:14→20:00:34, 20:00:34→20:52:19,
  20:52:19→21:32:35 — **exact**.
- **F1 — minor, recorded not repaired:** tick 1's "pin read" cell renders "—",
  while its own cited receipt (SKILL.md:1038) carries the reading
  (`4 × current · 2 × stale · 0 × drift; tool held`). The plan's own tick-1
  clause also renders no reading (`plans/round-11.plan.md:92`), so the
  closeout mirrors its source; the receipt nonetheless governs. Under-rendering,
  not misstatement.

## 3. The 6-leg receipt re-run (§4.2's r11 re-verification, independent)

**My run** (log `aud-regression.log`; workdir kept
`/tmp/w11-aud-t11-work/regression/`):

```
REGRESSION_TOOL: …/tools/mutate-and-run.sh sha256=75ed934dc86360f5…
REGRESSION_DATE: 2026-10-14T21:34:12Z
REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)   rc 0
```

every leg exact: `match=10/10` legs 1–4/6, `match=15/15` leg 5; killed
8/8/6/4/7/7; `flips=0 inconclusive=0`.

**Independent leg check** (`/tmp/w11-aud-t11-work/leg-check.py`, not trusting
the tool's selftest; `legcheck.txt`): `LEGCHECK: PASS (6/6 legs clean)` —
git-materialized blob == recorded pin ×6; materialized pristine == pin ×6;
65 `@old` strings all unique (10/10/10/10/15/10); no no-op edits; **and, stronger
than the r10 audit's check, all 65 edits independently re-applied
(`pristine.replace(old,new,1)`) byte-compare equal to the tool's `mutant-D*`
files — 65/65.**

**Legs 5/6 expectations vs their source notes:** kagi checklist "7/15 =
46.7 %, printed 47 %" (`mutation-case-kagi-checklist.md:131`); kumitate claims
"kill rate 7/10 (70 %)" (`mutation-case-kumitate-claims.md:63`) — both match
`REGRESSION_EXPECT`; live pins equal the legs' pins.

**The closeout's §4.2 r11-re-verification claim** ("the round's own
`--regression` receipt 21:32:40Z (`cases=6 passed=6`) and this lane's selftest
80/80") — **CONFIRMED** (T11-4 `regression.log`; T11-1 `selftest.log`); cross-lane
also T11-3's and SCR-T11's runs at the same revision.

## 4. The zero-debt check — what the closeout names as debt, is it really debt

Every debt the closeout names (§4.1–§4.3), re-derived at my reads (21:40–21:46Z):

| # | debt as the closeout names it (anchor) | state re-derived by me | really debt? |
|---|---|---|---|
| 1 | two `stale` successor rows; "no appended rows yet — the ledger is byte-identical `2f25c51e…`" (§4.3) | `sha256sum` → `2f25c51e3e0a7851…`, 363 L; no rows below the ER-4 addendum (`:356-362`) | **YES — open** |
| 2 | ledger §1 embedding text "cases 1 and 2 only"; no six-leg registry row (§4.2) | `:85-88` reads "embeds **cases 1 and 2 only**"; no registry row anywhere in the ledger | **YES — open** |
| 3 | runbook's four-leg lines stay stale; "ER-R3 open" (§4.2) | runbook `e1e349b69d798acb…`, 511 L; `:173` / `:374-375` / `:458` still "four legs / not embedded"; `grep -c '^\*\*ER-R'` → 2 (ER-R1/R2; no ER-R3) | **YES — open** |
| 4 | census §5 instrument re-pin errata (§4.3) | census `ec1c2d8d2877a21d…`, 674 L unchanged; §5 still pins the instrument at `597e1419…` (r4-2, `:252`); Errata section "(none yet)" | **YES — open** |
| 5 | coverage map lags (`corpus/README.md`, 20 L) (§4.3) | `1fe3050002f54b29…`, 20 L, 9 rows covering 6 of 16 notes — unchanged | **YES — open** |
| 6 | the runbook's fresh-executor sufficiency table; no `reports/r10-ver-t10.md` (§4.3) | `ls reports/` → r7–r10 audit/verifier files only; `r10-ver-t10.md` absent; no r11 verifier report landed at my close | **YES — open** |
| 7 | tsukuroi's 9 un-exercised clause sites ("coverage debt, not silent gaps") (§4.1) | anchors resolve: `memory-arm-ver-s8.md:177-181` (D2 block, "9 clause sites un-exercised by the 49-case suite"), tsukuroi `SKILL.md:1059-1063` ("not clause-complete"); live gate `10452443…` @ `af8adf1`, 2 402 L — exactly the closeout's cell; closure at the live revision `[U]`, carried | **YES — open** (closure unknown, named as such) |
| 8 | unexecuted surfaces: attestation (protocol U1), fleet-contributed leg, third-lane adoption (U2), dispatch hand-off (U3), cite-check's full sweep, the ten surveyed-but-unmeasured gates (§4.3) | anchors resolve: protocol `:32-38` ("attestation … planned, in flight"); ledger `:98-124` (the queue); register state unchanged | **YES — registers, still open** |
| 9 | unknown registers + the arc's unmeasured classes (§4.3) | ledger U1–U9 `:216-237`, protocol U1–U6 `:259-274`, limits U1–U5 `:220-237`; interval/driver/adoption `[U]` — homes unchanged | **YES — carried** |

**No false closure found.** The items the closeout renders *resolved* — the
4-vs-6 leg cut (an embedding at r10-2, committed `606716f`; four r10 receipts;
r11 re-verified) and the r10 landing (commit stat 9 files, +2 212/−61) —
re-verify as landed.

**F2 — minor, recorded not repaired:** §2.6 restates the visibility counts
("tsukuroi 12 files · mado 19 · kumitate 0 · kagi 0") without an as-of. Re-run
of the anchor note's own command at my read: tsukuroi **17** working-tree /
**16** tracked-at-HEAD; mado **27** / **25**; kumitate **0**; kagi **0** — the
direction (asymmetry; kumitate/kagi zero) holds, and the drift is the siblings'
own later commits and in-flight writes (both repos' round-10 landings postdate
the anchor note's read); the note's numbers stand as its own read.

## 5. Verdict table

| # | claim audited | verdict |
|---|---|---|
| 1 | The closeout landed (`corpus/knowledge/closeout-r11.md`) and is stable at my reads | **CONFIRMED** (`cea3352a…`, 420 L; untracked; ×4 stable samples) |
| 2 | Claim A — the appointment pair: announced at `606716f` (21:28:23Z, before the wave; committed bytes = live bytes) → fired 21:32:35Z; delta +4 m 12 s | **CONFIRMED** |
| 3 | The announced set == the executed set (pin read + selftest + regression, six-case frame) | **CONFIRMED** |
| 4 | Claim B — the tick series: 4 receipts, one cell each re-derived; gap series 45 m 20 s / 51 m 45 s / 40 m 16 s | **CONFIRMED** (one under-rendering, F1) |
| 5 | Tool identity + held: `75ed934d…` (r10-2, committed at `606716f`) | **CONFIRMED** (`git show 606716f:tools/mutate-and-run.sh \| sha256sum`; held vs the r10 receipts' revision) |
| 6 | The 6-leg receipt re-run | **CONFIRMED** — `cases=6 passed=6`, rc 0, 21:34:12Z; `LEGCHECK: PASS (6/6 legs clean)`; 65/65 mutant re-apply byte-match; legs 5/6 == source notes |
| 7 | Zero-debt check: every named debt is really debt (9/9 above) | **CONFIRMED** — all open at my reads; no false closure |
| 8 | §2 anchor spot-checks (72 `@defect`; six-leg header `:85-97`; ledger table rates/pins; protocol forms `:32-38`; limits a–j `:42-55`; adjudication `:199-204`; visibility `:34-47`) | **CONFIRMED** at spot-check depth |
| 9 | §1 completeness table cells (spot: `SCORECARD.md:13-23` rows, `LOG.md:68/:173/:303-309`, commits `2587e0a`/`606716f`, `SHONEN.md` 4×`[x]` last touched `53e74a8`) | **CONFIRMED** at spot-check depth |
| 10 | §6 source table (12 pins + lines) | **CONFIRMED** — every cell re-measured equal at my reads |
| 11 | §5 SC1's `grep -c '^@defect'` = 72 | **CONFIRMED** (measured 72) |
| 12 | This audit wrote nothing but this report | **CONFIRMED** (all writes `/tmp/w11-aud-t11-*`) |

**Findings (minor, recorded, not repaired):** F1 (§2, tick-1 dash vs its own
receipt); F2 (§4, count restatement without as-of — drift measured 17/27).
Neither changes any headline claim.

## 6. Spot-checks (three, re-runnable)

- **SC1 — the 6-leg receipt + leg check.**
  `bash tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/…`
  → `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0
  flips<=0)`, rc 0, `REGRESSION_DATE 2026-10-14T21:34:12Z`,
  `REGRESSION_TOOL sha256=75ed934dc86360f5…` (~2 min);
  `python3 /tmp/w11-aud-t11-work/leg-check.py <fleet-root> <workdir> <log>` →
  `LEGCHECK: PASS (6/6 legs clean); defects=65; mutant re-apply
  byte-match=65/65`.
- **SC2 — the appointment pair.**
  `git log --format='%h %cI %ct' -- plans/round-11.plan.md` → `606716f
  2026-10-14T18:28:23-03:00`; `TZ=UTC git show -s --format=%cd --date=iso-strict
  606716f` → `2026-10-14T21:28:23Z`; `/tmp/w11-t11-4-ev/pin-read.txt` header →
  `2026-10-14T21:32:35Z`; delta 4 m 12 s; `git show
  606716f:plans/round-11.plan.md | sha256sum` == live `068578f198367b79…`.
- **SC3 — the debt-state pass.**
  `sha256sum corpus/knowledge/fleet-kill-rate-ledger.md` → `2f25c51e…` (no
  successor rows); `wc -l corpus/README.md` → 20; `grep -c '^\*\*ER-R'
  corpus/knowledge/operator-runbook.md` → 2; `ls reports/` → no
  `r10-ver-t10.md`; `sha256sum corpus/knowledge/fleet-suite-census.md` →
  `ec1c2d8d…` (§5 pin `597e1419…` stands); tsukuroi live gate `10452443…`, 2 402 L.

## 7. Unknowns

- **U1 — the closeout is untracked** (`??`) at my close; a later edit moves the
  sha. Every verdict binds to `cea3352a…` / 420 L; re-resolve on a differing
  revision.
- **U2 — the round's own record is in flight** (`plans/round-11-record-draft.md`
  absent; LOG/SCORECARD r11 rows and coverage rows unwritten at my close). Not
  audited here; the closeout's §7 already names the landing state `[U]`.
- **U3 — the closeout's carried `[U]`s** (the interval; adoption; whether a
  fleet driver invokes the tick) are unmeasured by design — I did not measure
  them either.
- **U4 — single host** (`plazir27`), 2026-10-14; timings are host-local.
- **U5 — timestamped readings.** Sibling trees and the tameshi worktree move
  under their own lanes; re-read before quoting (e.g. the F2 counts).
- **U6 — contamination.** This is a declared-contamination audit (§0), not a
  cold-executor seat; the verifier's fresh-executor leg remains the independent
  test the r10 record already names as not reported.
- **U7 — scratch volatility.** All evidence lives under
  `/tmp/w11-aud-t11-{work,ev}/` (`freeze-snapshot.txt`, `pin-read.txt`,
  `aud-regression.log`, `legcheck.txt`, `poll.log`, `draft-report.md`).

## 8. Errata (append-only)

(none yet — new entries go below this line, never edits above)