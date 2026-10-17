# Round-9 record draft — for the parent scribe to finalize (SCR-T9)

Drafted 2026-10-14, poll window **19:57:46Z–20:27:46Z** (60 s samples, 30
samples, `POLL DONE 2026-10-14T20:27:46Z`; assignment cap 30 min). Lane SCR-T9
(round-9 scribe prep). This file
carries: **Round-9 shape** (planned vs realized), **0** landing status +
corrections ledger, **A** the SCORECARD move-log rows, **B** the LOG.md
round-9 entry, **C** the SCR-T9 evidence ledger, **D** the parent checklist.
Write-scope: this file only; scratch `/tmp/w9-tameshi-scr-t9/` (poll log
`poll.log`; poll task `bash-dgmgv28n`). Anchors: **O** observation · **I**
inference · **U** unknown. Every cell below binds to a measured sha; nothing
is carried from a plan or from a producer's prose.

## Round-9 shape — planned vs realized

- **Planned** (`plans/round-9.plan.md`, 222 L / 15198 B / `230ed6b61e4c89d9`,
  committed at `c611d5d`; ufo-round-plan-v1): axis move **operability — the
  ledger's cadence fires its first scheduled tick.** ONE move, three ordered
  legs (plan `:24-69`):
  1. **Leg tick** — the pin read at the round boundary under the landed
     cadence policy (round 8's mechanism: pin state `current|stale|drift`,
     tool `held|moved`, triggers T1–T3; `plans/round-8.plan.md:11-31`), pasted
     with its output; per case `git show <rev>:<path>` sha256 vs the pin +
     `git merge-base --is-ancestor <rev> HEAD`, read mechanically.
  2. **Leg re-sweep** — every case the tick reads `stale`/`moved`, re-measured
     at its live revision (fresh `/tmp` copies, read-only targets, the same
     10-step recipe, tool pinned per run via `MUTATE_TOOL`, the recorded defect
     vocabulary — a moved anchor makes a NEW pre-registered spec, never a
     re-interpretation). Outcome = an **appended row** (case · recorded pin/rev
     → live pin/rev · tool sha · control line · per-defect verdict delta ·
     composition · date), recorded tables byte-identical; the tool's leg
     registry gains a successor leg only where the contribution contract is
     met (`SKILL.md:954-963`) — otherwise the row is marked *not embedded*
     (`fleet-kill-rate-ledger.md:85-88`, append-only).
  3. **Leg limits** — the service's limits note ("what tameshi refuses to
     mutation-test and why") as the refusal table the cadence applies at
     intake, every refusal anchored; plus the one cadence precondition round
     8 named — a re-pin rule for a moved substrate in the opt-in protocol
     (present → cited; absent → append-only contract errata,
     `corpus/QUALITY.md` item 4).
- **Case frame** (re-measured at this window's open, §0.1): **6 cases = 4
  `current` · 2 `stale` · 0 `drift`**, tool `held`. The plan's design-time
  live cells (mado `90d50cdd…`, dirty) are superseded by the committed
  `7da4ec50…` (mado HEAD `12c8f08a`).
- **Realized — legs 1 and 3 landed; leg 2 open at this draft's close:**
  1. **Tick — landed, twice, independently, and kept un-merged.** Ledger
     **ER-4** (`fleet-kill-rate-ledger.md:318-353`, lane T9-1; instance 19:58Z,
     second raw pass 20:00:29Z) + **SKILL.md `:1155`** round-9 section (lane
     T9-3; instance 20:00:34Z, scratch `/tmp/w9-tameshi-t93/pin-read-final.txt`).
     Both records agree cell-for-cell: six cases 4 `current` · 2 `stale` ·
     0 `drift`; both drift chains (`084951be…` → `bba6cdf6…`;
     `d7edaab4…` → `7da4ec50…`); regression re-run exact (`cases=4
     passed=4`, every leg `match=10/10 … flips=0`); tool **held** at
     `cf41efaa…`. Headline as measured:
     `LEDGER: 6 cases in; target current=4 stale=2 drift=0; tool held (cf41efaa…)`.
     T9-3's falsifier (aimed at the reader): the same script with
     kimi-census's recorded pin doctored to a superseded sha reads `stale`
     while the untouched row reads `current` (`:1191-1194`).
  2. **Re-sweep — NOT landed inside this window.** ER-4's own addendum
     (`:356-360`) reads both moved gates worktree-**dirty** again by 20:02Z
     (tsukuroi `5d16378d…` +63/−0 vs HEAD blob; mado `5b6ace8e…` +196/−7) and
     SKILL's re-read at 20:03:34Z reads them `stale + drift` again
     (`b54f5732…` / `31364115…`) — the owners' own round-9 lanes are editing
     their gates. T3 is live on both rows; any re-sweep must pin the revision
     it measures. **No re-sweep row exists in the ledger at this close**
     (no ER-5; `git status` shows no new case note). This is **named, open
     debt** for the parent, not a completed leg.
  3. **Limits — landed.** `corpus/knowledge/service-limits.md` (lane T9-2; new
     file; §1 refusal table rows a–j, each with a measured anchor; §2 verbatim
     anchor detail; §3 the intake precondition; §4 SC1–SC3; §5 U1–U3) +
     the compact rendering in `SKILL.md` § *The service's limits* (heading
     `:1246`; table `:1256-1267` on the final revision — see the line-shift
     note in §0.3) (landed "during this
     write" per the note's own §0 [O]). **Intake precondition: present, cited,
     no errata** — `service-optin-protocol.md:59-63` (item 1: "A moved
     substrate needs a re-pin, never a re-interpretation of the old table.");
     the note's §3 states "No errata needed", and the protocol itself is
     **unchanged** (`84d0c1547eed257d`, 286 L — same revision as at open).
- **Independent verification — landed.** `reports/r9-ver-t9.md` (lane VER-T9,
  146 L / 9332 B / `803ec00849347b54`): re-derives ER-4 **row 3** (tsukuroi
  drift event) with its own commands → **CONFIRMED** (recorded blob
  `084951be…` @ `165307fe`, blob chain `aae45531…` @ `da95290` → `bba6cdf6…` @
  `aa136d6`, movement set exactly `da95290`+`aa136d6`, every cell matched), and
  proves the ledger's round-9 append append-only: `diff` → `315a316,363`
  (48 added, 0 removed, 0 changed).
- **Audit — landed at the window's edge.** `reports/r9-aud-t9.md` (lane AUD-T9,
  167 L / 12829 B / `6cdc8d7cdd23dea8`): an 11-row verdict table — rows 1–9 and
  11 **CONFIRMED** (tool held ×3 hashes; `--selftest` and two independent
  `--regression` runs reproducing 8/8/6/4 `match=10/10 flips=0` with
  `MUTATE_RESTORE: OK`; the six-cell pin read re-read at 20:00:07Z; both drift
  chains re-derived; the addendum's dirty cells matched at same sizes; ledger
  append-only by byte-prefix `cmp` ×2 + append hunk `315a316,363` + ER-4 region
  hash stable; SKILL a pure append) and row 10 **"NOT CLAIMED — honestly
  open"** for leg 2 (no ER-5; nothing claims the re-sweeps). Not audited
  (named, not claimed): T9-3's falsifier, the limits rows, the leg-2 re-sweep
  itself.
- **Next round's design — landed inside this window.** `plans/round-10.plan.md`
  (lane PREP-T10, 254 L / 17671 B / `d130596ac8bc7e91`; frozen 20:04Z, file
  mtime 20:05Z): the terminal round's plan (axis move operability — the
  ten-round closeout as a `HANDOFF.md` runbook), whose own case frame
  re-measures the same six cells and reads *this draft* as its debt ledger
  (`:206`).

## 0. Landing status

### 0.1 Baseline at window open (measured 19:57–19:59Z)

- HEAD `c611d5d` ("probation round 8 (training r7): see LOG", 16:55:09 −03:00
  = 19:55:09Z); `git status --porcelain` **empty**; no `.ufo/waves/tameshi-r9-*`
  directory exists ([O], `ls` — same shape as rounds 1–8: the lane deliverables
  in this repo ARE the wave record).
- Cells (this lane's reads; sha = first 16 hex):
  - `LOG.md` 307 L / 22914 B / `36e0f97076d84cd6` (round-8 stub at `:307`)
  - `SCORECARD.md` 21 L / 11884 B / `54202192fa85cfb7` (round-8 stub row `:21`)
  - `SKILL.md` 1152 L / 77612 B / `6753b1b224f4bd18` (round-8 revision)
  - `tools/mutate-and-run.sh` 1341 L / 61632 B / `cf41efaa8be5f52d` (r7-1)
  - `corpus/knowledge/fleet-kill-rate-ledger.md` 315 L / 28503 B /
    `71bc15e365a3574f` (ER-2 `:272`, ER-3 `:285`)
  - `corpus/knowledge/service-optin-protocol.md` 286 L / 17644 B /
    `84d0c1547eed257d`
  - `corpus/knowledge/fleet-suite-census.md` 674 L / 48719 B /
    `ec1c2d8d2877a21d` (its §5 instrument pin is two revisions stale — ER-2
    follow-up, still unlanded)
  - `corpus/README.md` 20 L / 12182 B / `1fe3050002f54b29` (no coverage rows
    for the round-6/7/8 notes — carried debt)
  - `plans/round-9.plan.md` 222 L / 15198 B / `230ed6b61e4c89d9`; `reports/`
    held exactly `r7-aud-t7.md`, `r8-aud-t8.md`, `r8-ver-t8.md`.
- Round-8 landed form (`git show --numstat c611d5d`): `LOG.md` +1,
  `SCORECARD.md` +1, `SKILL.md` +146/−1, ledger +47/−1,
  `mutation-case-kagi-checklist.md` 368, `mutation-case-kumitate-claims.md`
  410, `plans/round-8-record-draft.md` 390, `plans/round-9.plan.md` 223,
  `reports/r8-aud-t8.md` 171, `reports/r8-ver-t8.md` 116.
- **Baseline pulse (this lane).** `bash tools/mutate-and-run.sh --selftest` →
  `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0, 4.9 s
  (`/tmp/w9-tameshi-scr-t9/open-selftest.log`);
  `--regression --workdir /tmp/w9-tameshi-scr-t9/open/regr` →
  `REGRESSION_TOOL … sha256=cf41efaa…bce37242c75`,
  `REGRESSION_DATE 2026-10-14T19:57:54Z`, four legs `match=10/10 … flips=0`
  (killed 8/8/6/4), `REGRESSION: PASS (cases=4 passed=4; ledger legs exact:
  killed-delta<=0 flips<=0)`, rc 0, 45.9 s
  (`/tmp/w9-tameshi-scr-t9/open-regression.log`).
- **Baseline pin read (this lane, 19:57Z; read-only).** 4 current · 2 stale ·
  0 drift: kimi-census `83016d45…` current; surface-census `275d8294…`
  current; tsukuroi-census `084951be…` → live `bba6cdf6…` **stale** (tsukuroi
  HEAD `72b038da`, path clean); mado-verify `d7edaab4…` → live `7da4ec50…`
  **stale** (mado HEAD `12c8f08a`, path clean); checklist-run `7e5ec98b…`
  current; claims-check `e9a21b44…` current. All four recorded revs are
  ancestors of their HEADs (`merge-base --is-ancestor` → rc 0 ×4); all four
  sibling trees porcelain-**clean**; tool `held`.
- Execution lanes already visible at open ([O], `/tmp`): `/tmp/w9-tameshi-t91`
  (tick + regression), `/tmp/w9-tameshi-t93` (pin read + falsifier +
  regression), `/tmp/w9-t9-2` (limits note), `/tmp/w9-ver-t9-work` (verifier
  baseline + poll), `/tmp/w9-aud-t9-{work,evidence}` (auditor),
  `/tmp/w9-prept10{, -selftest,-regression}` (round-10 design),
  `/tmp/w9-scrb9` (a sibling repo's scribe), plus sibling-repo lanes
  (`w9-tsukuroi-s9*`, `w9-mado-m9*`, `w9-tabi-b91`, …).

### 0.2 Measured at window close (this lane, 20:26–20:27Z; poll ran to 20:27:46Z)

Every cell in §0.3/§C binds here. `git status --porcelain` at close: ` M SKILL.md`,
` M corpus/knowledge/fleet-kill-rate-ledger.md`,
`?? corpus/knowledge/service-limits.md`, `?? plans/round-10.plan.md`,
`?? plans/round-9-record-draft.md`, `?? reports/r9-aud-t9.md`,
`?? reports/r9-ver-t9.md` — exactly the round-9 writes + this draft.

| artifact | close cell | note |
|---|---|---|
| `SKILL.md` | 1269 L / 85320 B / `ee09c3bddb6cc705` | +118/−1 vs open; round-9 section header `:1155` (unmoved); limits table `:1256-1267` on the final revision |
| `fleet-kill-rate-ledger.md` | 363 L / 36169 B / `2f25c51e3e0a7851` | +48/−0; ER-4 `:318` + addendum `:356` |
| `service-limits.md` | 276 L / 21720 B / `a57a1e69be02896a` | T9-2, new file (was 266 → 274 → 276 L during the window) |
| `reports/r9-ver-t9.md` | 146 L / 9332 B / `803ec00849347b54` | VER-T9 — ER-4 row 3 CONFIRMED |
| `reports/r9-aud-t9.md` | 167 L / 12829 B / `6cdc8d7cdd23dea8` | AUD-T9 (mtime 20:22:45Z; first seen in this lane's status read 20:26:46Z); 11-row verdict table: CONFIRMED ×10, row 10 = leg 2 "NOT CLAIMED — honestly open" |
| `plans/round-10.plan.md` | 254 L / 17671 B / `d130596ac8bc7e91` | PREP-T10, new file (landed ~20:05Z; frozen 20:04Z) |
| `tools/mutate-and-run.sh` | `cf41efaa8be5f52d` 1341 L / 61632 B | **held** — no round-9 instrument edit |
| `LOG.md` / `SCORECARD.md` | 307 L / 22914 B · 21 L / 11884 B, unchanged | writing the r9 rows is this draft's purpose |
| `service-optin-protocol.md` / census / README | `84d0c154…` / `ec1c2d8d…` / `1fe30500…`, unchanged | precondition was present → no errata |

### 0.3 Corrections ledger — what moved during the window (append-only)

| cell | at open | during/at close | reading |
|---|---|---|---|
| tool revision | `cf41efaa…` 1341 L / 61632 B | `cf41efaa…` (unchanged; mtime 15:29:01 −03:00) | **held** — no instrument edit in round 9 ([O], every read incl. ER-4's 20:02Z re-read) |
| ledger | 315 L / 28503 B (`71bc15e3…`) | 363 L / 36169 B (`2f25c51e…`); append `315a316,363` = +48/−0/−0 | ER-4 + addendum; §1–§4 byte-identical (my `diff` + VER-T9's) |
| SKILL | 1152 L / 77612 B (`6753b1b2…`) | 1269 L / 85320 B (`ee09c3bd…`); +118/−1 | the one "removed" line is the round-8 revision's **unterminated final line** being terminated: round-8 SKILL + `\n` = first **77613 B** of round-9 SKILL (`cmp` → identical), 7707 B appended. **Line-shift caveat (recorded in T9-2's errata, `service-limits.md:271`):** the round-9 section was **edited in place** after T9-2 read it (write-time cites superseded: `:1230-1249` → the limits table now `:1256-1267`; both states are the same content at different offsets, and the section header `:1155` is unmoved). Cite the round-9 SKILL section **by heading, not by line**, while the round is in flight |
| case notes | — | **none new** | the leg-2 re-sweeps did not land |
| service notes | — | `service-limits.md` new (T9-2) | limits leg, with SKILL compact rendering (`:1246` heading, table `:1256-1267`) |
| reports | 3 files | + `r9-ver-t9.md` (VER-T9, 146 L) and + `r9-aud-t9.md` (AUD-T9, 167 L, mtime 20:22:45Z) | both r9 reports landed inside the window |
| plans | `round-9.plan.md` 222 L | + `round-10.plan.md` (PREP-T10, 254 L / 17671 B / `d130596a…`) | the next round's design landed inside this window |
| tsukuroi gate | live `bba6cdf6…` = HEAD blob, clean | worktree `5d16378d…` (20:02Z, ER-4) → `b54f5732…` (20:03Z, SKILL) | owner lane mid-edit — **stale + drift**; every cell is a timestamped reading |
| mado gate | live `7da4ec50…` = HEAD blob, clean | worktree `5b6ace8e…` (20:02Z) → `31364115…` (20:03Z) | owner lane mid-edit — **stale + drift** |
| LOG / SCORECARD | 307 L / 21 L | unchanged | r9 rows not yet written |

## A. SCORECARD.md — move-log rows (append after the round-8 row at `:21`)

Precedent: rounds 4–8 landed as terse one-line stubs. Round 9 is ONE move
(operability: the cadence's first scheduled tick), three legs — full row
first, stub form after. **Honesty constraint: the full row must render leg 2
as OPEN** (no re-sweep landed); do not let the row read as a closed re-sweep.

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 9 | operability | round-8 state: the cadence landed as policy + one demonstrated pin read (ER-3 `:285`, SKILL `:1010`) but had never fired at a round boundary; two cases read `stale` with no re-sweep and no recorded delta; no intake-refusal note existed, and the one cadence precondition (a re-pin rule in the opt-in protocol) was unchecked | the cadence's **first scheduled tick** ran and is recorded **twice, independently, kept un-merged**: ledger **ER-4** (`:318-353`, T9-1; 19:58Z, second pass 20:00:29Z) + SKILL `:1155` § *The cadence's first scheduled tick* (T9-3; 20:00:34Z) — headline `LEDGER: 6 cases in; target current=4 stale=2 drift=0; tool held (cf41efaa…)`; both drift chains appended (`084951be…`→`bba6cdf6…`; `d7edaab4…`→`7da4ec50…`); the instrument re-passed at the boundary (`--selftest 67/67`; `--regression` `cases=4 passed=4`, each leg `match=10/10 … flips=0`, `REGRESSION_DATE 19:58:59Z`); a reader-aimed falsifier (doctored pin → `stale`; untouched → `current`); **the service-limits note lands** — `corpus/knowledge/service-limits.md` + SKILL compact table (`:1256-1267`; heading `:1246`), refusal rows a–j each anchored, and the round-8 intake precondition checked **present** (`service-optin-protocol.md:59-63`) → cited, no errata; **leg 2 open**: both moved gates read worktree-dirty again by 20:02/20:03Z (`stale + drift`), the re-sweeps are appended-row work not yet landed (no ER-5); independent verification: **VER-T9** CONFIRMED (ER-4 row 3 re-derived cell-for-cell; ledger append-only proven `315a316,363`), **AUD-T9** 10/11 verdicts CONFIRMED on ER-4 + addendum (two independent `--regression` runs; both drift chains; byte-prefix `cmp`; SKILL pure append) with row 10 = leg 2 **"NOT CLAIMED — honestly open"** | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 (mine 19:57:35Z; T9-1 tick.log; T9-3 selftest.txt); `--regression` → `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0 (`REGRESSION_DATE 19:57:54Z` mine / 19:58:18Z T9-1 / 19:58:59Z T9-3); pin read ×4 agreeing (mine 19:57Z, T9-1 19:58Z+20:00:29Z, T9-3 20:00:34Z, VER-T9 19:58:12Z re-derived) → 4 current · 2 stale · 0 drift, tool held; ledger `diff` before→after → `315a316,363` (48 added, 0 removed, 0 changed), ER-4 `:318`, addendum `:356`; SKILL `cmp`: round-8 bytes + `\n` = first 77613 B, +7707 B appended, section `:1155`; `service-limits.md` new (rows a–j; §3 "No errata needed"); `reports/r9-ver-t9.md` `803ec008…` CONFIRMED; `reports/r9-aud-t9.md` `6cdc8d7c…` (10 CONFIRMED, leg 2 row "NOT CLAIMED"). Re-run 2026-10-14 (SCR-T9) |

Stub form (rounds 4–8 convention):

```
| 9 | operability | round-8: cadence landed as policy only; 2 stale, no re-sweep; no limits note | cadence's 1st scheduled tick executed + recorded twice (ER-4 + SKILL :1155; 4 current/2 stale/0 drift; tool held; regression 4/4 exact) + limits note (service-limits.md, 10 refusals anchored; intake precondition present→cited) + VER CONFIRMED; re-sweeps of the 2 stale cases open (both gates dirty again by 20:02Z) | wave-9 32-lane + SCR-T9 (selftest 67/67, regression 4/4) |
```

## B. LOG.md — round-9 entry (append as a new bullet after the round-8 entry at `:307`)

Recommended form first (stub, matching the landed rounds 4–8 convention —
`LOG.md:303-307`), then the full form the parent may prefer if it wants the
detail inside `LOG.md` rather than only in this draft.

**Stub (recommended):**

```
- 2026-10-14 — round 9 (training r8): the cadence's first scheduled tick, recorded twice and independently (ledger ER-4 + SKILL :1155; 4 current/2 stale/0 drift; tool held; regression 4/4 exact) + the service-limits note (service-limits.md, 10 refusals each anchored; the round-8 intake precondition found present in the protocol :59-63 -> cited, no errata); re-sweeps of the two stale gates OPEN at close (both read stale+drift again). Axis: operability. Verifiers: VER-T9 | AUD-T9.
```

*(Derivation note [I]: "training r8" follows the landed naming pattern round N
= training r(N−1) — rounds 4–8 → r3–r7; if the parent's dispatch calls it
something else, the parent's label wins.)*

**Full form (if the parent wants the detail inline):**

- 2026-10-14 — round 9: planned as a ufo-round-plan (`plans/round-9.plan.md`,
  ufo-round-plan-v1 — axis move **operability**: the fleet ledger's cadence
  fires its first scheduled tick; three ordered legs: tick · re-sweep ·
  limits). Same dispatch shape as rounds 1–8 — lane write-scopes leave this
  LOG to the scribe; the lane deliverables in this repo ARE the wave record
  (observation; no `.ufo/waves/tameshi-r9-*` directory was created).
  TAMESHI-T9-1 → `corpus/knowledge/fleet-kill-rate-ledger.md` **ER-4**
  (`:318-353`, + addendum `:356-360`; ledger 315 → 363 L, `71bc15e3…` →
  `2f25c51e…`; pure append `315a316,363`): the tick's receipt — six-case pin
  read at 19:58Z (4 current · 2 stale · 0 drift; `LEDGER: 6 cases in; target
  current=4 stale=2 drift=0; tool held`), both drift chains (`084951be…` →
  `bba6cdf6…`; `d7edaab4…` → `7da4ec50…`), the regression re-run exact
  (`cases=4 passed=4`, `REGRESSION_DATE 19:58:18Z`), and the addendum's
  post-tick continuation (both gates worktree-dirty again by 20:02Z;
  `stale + drift`); §1–§4 untouched.
  TAMESHI-T9-2 → `corpus/knowledge/service-limits.md` (new; refusal table
  rows a–j, each anchored; §2 verbatim reasons; §3 the intake precondition —
  **present** at `service-optin-protocol.md:59-63` → cited, **no errata**;
  §4 SC1–SC3; §5 U1–U3) + the compact rendering in `SKILL.md` § *The
  service's limits* (heading `:1246`; table `:1256-1267` on the final revision
  — its §6 errata records the in-place edit that shifted these lines).
  TAMESHI-T9-3 → `SKILL.md` round-9 section `:1155` (+118/−1; 1152 →
  1269 L; `6753b1b2…` → `ee09c3bd…`; the one "removed" line is the round-8
  revision's unterminated final line being terminated — round-8 bytes + `\n`
  = first 77613 B, `cmp`-verified): the tick's executed instance
  (20:00:34Z; falsifier: doctored pin reads `stale`, untouched `current`;
  `--selftest` 19:58:49Z, `--regression` `REGRESSION_DATE 19:58:59Z`), the
  re-pin semantics as executed, and the limits table.
  VER-T9 (verifier lane, read-only) → `reports/r9-ver-t9.md` (146 L,
  `803ec008…`): ER-4 **row 3** re-derived cell-for-cell from the pinned blobs
  → **CONFIRMED**; ledger round-9 append proven append-only (`315a316,363`);
  poll 19:59:10–20:02:55Z (append detected 20:01:25Z, stable 20:02:55Z).
  AUD-T9 (audit lane, read-only) → `reports/r9-aud-t9.md` (167 L,
  `6cdc8d7c…`, mtime 20:22:45Z): an 11-row verdict table on ER-4 + addendum —
  10 CONFIRMED (tool held ×3 hashes; `--selftest` + two independent
  `--regression` runs reproducing per-leg `match=10/10 flips=0` killed
  8/8/6/4 with `MUTATE_RESTORE: OK`; the six-cell pin read at 20:00:07Z; both
  drift chains re-derived from the repos' git stores; the addendum's dirty
  cells matched at same sizes; ledger append-only by byte-prefix `cmp` ×2 +
  single append hunk + stable ER-4 region hash; SKILL a pure append),
  and row 10 — **"NOT CLAIMED — honestly open"** for leg 2 (the re-sweeps).
  PREP-T10 (design lane) → `plans/round-10.plan.md` (254 L / 17671 B /
  `d130596a…`; frozen 20:04Z): the terminal round's plan — the closeout as a
  `HANDOFF.md` runbook, its case frame re-measuring the same six cells, and
  this draft read as its debt ledger.
  Scribe verification (this draft, SCR-T9; scratch `/tmp/w9-tameshi-scr-t9/`):
  baseline pulse at open (`--selftest` 67/67 rc 0; `--regression`
  `cases=4 passed=4`, `REGRESSION_DATE 19:57:54Z`, rc 0) and the same
  instrument `held` at every read; six-case pin read at open agreeing with
  both tick lanes (4 current · 2 stale · 0 drift; tsukuroi `bba6cdf6…`, mado
  `7da4ec50…` both HEAD blobs, trees clean); the ledger's append proof
  reproduced independently (`diff` → `315a316,363`); the SKILL prefix proof
  (`cmp`). Leg 2 (re-sweeps of the two `stale` cases) is **open**: the owners'
  lanes moved both gates again by 20:02/20:03Z; the re-sweeps must pin the
  revision they measure and land as appended rows (both gates still carry no
  successor row, and cases 5/6 remain unembedded in `--regression` — carried
  debt from round 8).
  SCORECARD round-9 move: operability improved (the cadence's first executed
  boundary tick, recorded twice and independently; the limits note lands with
  every refusal anchored; the intake precondition checked and cited) — the
  re-sweep leg and the embedding of cases 5/6 stay **open, named debt**.
  Carried to round 10: the two re-sweeps at their pinned moved revisions;
  cases 5/6 embedding (ER-2 follow-up); census §5 instrument re-pin errata;
  `corpus/README.md` coverage rows (rounds 6–9 notes + r9 report);
  attestation leg (r7 U1); fleet-contributed case; cite-check's full sweep.

## C. SCR-T9 evidence ledger (measured by this lane; scratch `/tmp/w9-tameshi-scr-t9/`)

1. **Baseline pulse (19:57:35–19:58:40Z).** Selftest `67/67 pass`, rc 0,
   4.9 s; regression `cases=4 passed=4`, `REGRESSION_DATE
   2026-10-14T19:57:54Z`, per-leg `match=10/10` killed 8/8/6/4 `flips=0`,
   rc 0, 45.9 s; logs `open-selftest.log` / `open-regression.log`, workdir
   `open/regr`.
2. **Baseline pin read (19:57Z, read-only).** Per case `sha256sum <live>` vs
   recorded pin, `git show HEAD:<path> | sha256sum`,
   `git status --porcelain -- <path>`, `git merge-base --is-ancestor <rev>
   HEAD` → 4 current · 2 stale · 0 drift; tool `held`; sibling trees clean
   (0 porcelain lines each; kumitate `175de6b`, kagi `fecee87`, tsukuroi
   `72b038da`, mado `12c8f08a`).
3. **Append-only proof, reproduced (20:12Z).** `diff
   /tmp/w9-tameshi-t91/ledger-pre.md corpus/knowledge/fleet-kill-rate-ledger.md`
   → `315a316,363`; 48 `>` lines, 0 `<` lines. Same result in VER-T9's report
   (`reports/r9-ver-t9.md` §0/§1), independently.
4. **SKILL prefix proof (20:13Z).** `{ cat skill-pre-round9.md (77612 B,
   `6753b1b2…`); printf '\n'; }` `cmp` `head -c 77613 SKILL.md` → identical;
   round-9 SKILL = that prefix + 7707 B appended. The `+118/−1` numstat is the
   terminated last line, not edited content.
5. **Cross-lane reads (read-only; attribution from file credits + scratch
   names, not from a dispatch this lane saw [U]).** `/tmp/w9-tameshi-t91`
   (`tick.log` 6226 B: selftest 67/67 + full regression `REGRESSION_DATE
   19:58:18Z` + `REGRESSION_RC=0`, workdir kept; `ledger-pre.md` 28503 B;
   `pin-read.log` 1455 B); `/tmp/w9-tameshi-t93` (`pin-read-final.txt`
   mirrored into SKILL; `falsifier/doctored-read.txt`); `/tmp/w9-t9-2`
   (`anchors.txt` 5786 B, `selftest.log`, `spotchecks.txt`);
   `/tmp/w9-ver-t9-work` (baseline 19:58:12Z, ledger-before/-after,
   poll.log); `/tmp/w9-aud-t9-evidence` (snapshots: `ledger-pre-round9.md`,
   `skill-pre-round9.md`, `record-draft-snap.md` = this file's 20:04Z
   revision, `drift-timeline.txt`).
6. **Landing revisions observed** (all read this window; final cells §0.2):
   ledger `71bc15e3…` (315 L) → `e94633cc…` (351) → `dce68463…` (353) →
   `5ccf95c2…` (353, stable 20:02:25–20:02:55Z per VER-T9) → `2f25c51e…`
   (363 L / 36169 B); SKILL `6753b1b2…` (1152 L) → `ee09c3bd…` (1269 L /
   85320 B); `service-limits.md` new (266 → 274 → 276 L during the window);
   `reports/r9-ver-t9.md` new (146 L / 9332 B / `803ec008…`);
   `reports/r9-aud-t9.md` new (167 L / 12829 B / `6cdc8d7c…`, mtime
   20:22:45Z; first seen in this lane's status read at 20:26:46Z);
   `plans/round-10.plan.md` new (254 L / 17671 B / `d130596a…`).
7. **Round-8 landed form** (`git show --numstat c611d5d`, §0.1) — the
   "before" column; `SCORECARD.md:21` and `LOG.md:307` = the round-8 stubs.
8. **Unknowns from this lane.** (i) **Leg 2 is open** — no re-sweep row
   exists; both targets read `stale + drift` under live owner edits, so any
   re-sweep cell must pin its revision (T3) and the parent must not read leg 2
   as closed (AUD-T9 verdict row 10 records exactly this as "NOT CLAIMED —
   honestly open"). (ii) The tool embeds **4** legs; cases 5/6 (checklist-run,
   claims-check) carry no `REGRESSION` line — round-8 debt, unchanged.
   (iii) AUD-T9's report landed inside the window (mtime 20:22:45Z,
   first seen here 20:26:46Z) and is quoted
   from its bytes here; the audit's own un-audited list (T9-3's falsifier, the
   limits rows, the leg-2 re-sweep) is named there, not claimed here.
   PREP-T10's `plans/round-10.plan.md` landed at ~20:05Z (mtime 20:05:46Z) and is
   read here from its bytes (its plan is for round 10; it does not close any
   round-9 leg). (iv) Lane role
   labels (T9-1/2/3, VER, AUD, PREP) are from file credits and scratch names —
   the dispatch itself was not visible. (v) The tsukuroi/mado worktree cells
   are moving targets under the owners' round-9 lanes; every such cell in this
   file is a timestamped reading, not a standing claim. (vi) Single host /
   toolchain for every number; cross-host stability stays unmeasured
   fleet-wide. (vii) Whether any fleet driver would invoke the tick with no
   lane acting remains [U] (SKILL `:1019`).

**Spot-checks (three, all run this session).**

- **SC1 — the pulse pair (open + instrument held).** My open runs: selftest
  67/67 rc 0 (19:57:35Z); regression `cases=4 passed=4`, `REGRESSION_DATE
  19:57:54Z`, rc 0. Cross-checked against T9-1's tick.log (19:58:18Z) and
  T9-3's regression.txt (19:58:59Z) — three independent runs of the same
  instrument at the same revision, all green; tool sha `cf41efaa…` in every
  log and re-read held at 20:02Z (ER-4).
- **SC2 — the six-case pin read, four independent reads agreeing.** Mine
  (19:57Z), T9-1's (19:58Z + 20:00:29Z), T9-3's (20:00:34Z), VER-T9's
  (19:58:12Z, its own commands) → 4 current · 2 stale · 0 drift; tsukuroi
  `084951be…` → `bba6cdf6…`, mado `d7edaab4…` → `7da4ec50…`, both HEAD blobs,
  trees clean at the reads; the readers agree, and T9-3's doctored-pin
  falsifier shows the reading follows the row's pin.
- **SC3 — the landed bytes.** Ledger append proof reproduced (`315a316,363`);
  SKILL prefix proof (`cmp`, 77613 B + 7707 B); `reports/r9-ver-t9.md`
  CONFIRMED verdict and its append-only proof read at the file; the protocol
  revision is unchanged (`84d0c154…`, 286 L) — the intake precondition was
  cited, not written.

## D. Parent checklist (round close)

- **Honesty item 1 — the tool held.** No round-9 edit to
  `tools/mutate-and-run.sh`; `cf41efaa…` is the revision every receipt in
  this record carries (mine, T9-1's, T9-3's, T9-2's SC2).
- **Honesty item 2 — leg 2 is OPEN.** No re-sweep row exists (no ER-5; no new
  case note). Both moved gates read `stale + drift` under the owners' live
  edits by 20:02/20:03Z. Do not render round 9 as a closed re-sweep; the
  appended rows remain the work, and any re-sweep must pin its revision.
- **Honesty item 3 — the ledger append is append-only; the SKILL edit is
  not.** Ledger `315a316,363` (0 removed/changed; mine and VER-T9's). SKILL
  `1153c1153,1270` — the round-8 revision's unterminated final line terminated
  + 117 lines appended (`cmp` on the 77613 B prefix). Quote the `cmp`, not
  "no edit".
- **Honesty item 4 — the two tick records are kept un-merged.** ER-4 (T9-1)
  and SKILL `:1155` (T9-3) are two independent records of one tick; they
  agree, and neither was smoothed into the other (`SKILL.md:1190-1193`). A
  divergence would have been the finding.
- **Binding revisions.** Ledger `2f25c51e…` (363 L / 36169 B) binds ER-4
  `:318` + addendum `:356`; VER-T9 binds its cells to that sha (span `:316-353`
  sha256 `2ac5da32…`, line `:337` sha256 `750f4709…`). SKILL `ee09c3bd…`
  (1269 L / 85320 B) binds the round-9 section header `:1155` + the limits
  table `:1256-1267`; cite that section **by heading** (a line-shifted
  revision exists in the round's own history, `service-limits.md:271`); if the
  parent edits either
  file before commit, the anchors quoted here are the shas above — and
  VER-T9's CONFIRMED verdict binds to the ledger sha it read (a later edit
  needs re-audit).
- **Cross-lane numbers to reconcile.** The plan's "6 cases in" frame = the
  tick's 6 rows (4 embedded + 2 measured); the tool embeds 4 legs only
  (cases 5/6 carry no `REGRESSION` line — do not merge the two counts). The
  plan's design-time mado cell (`90d50cdd…`) is superseded by `7da4ec50…`
  (committed); tsukuroi's design-time `aa136d6` HEAD is now `72b038da`.
- **Commit items** (lane identity + round shape; precedents through
  `c611d5d`): `SKILL.md` (+118/−1); `corpus/knowledge/fleet-kill-rate-ledger.md`
  (+48/−0); `corpus/knowledge/service-limits.md` (new, parent to confirm the
  untracked file); `reports/r9-ver-t9.md`; `reports/r9-aud-t9.md` (both r9
  reports landed inside the window); `plans/round-10.plan.md` (new, PREP-T10 —
  unless the parent's round split assigns it to the next round's commit);
  `plans/round-9-record-draft.md` (precedent: rounds 4–8 drafts are
  committed); plus `LOG.md` +1 and `SCORECARD.md` +1 (not yet written — this
  draft's purpose).
- **Row convention**: rounds 4–8 landed stubs; §A offers full + stub. Decide
  and record either way.
- **Coverage-map rows** (`corpus/README.md`, still 20 L): add rows for
  `service-limits.md` and both r9 reports (`r9-ver-t9.md`, `r9-aud-t9.md`),
  and the still-open round-6/7/8 items (`mutation-case-mado-verify.md`,
  `self-hardening-r6.md`, `fleet-kill-rate-ledger.md`,
  `service-optin-protocol.md`, the two round-8 case notes, the two r8
  reports); the census §5 re-pin errata is still unlanded (ER-2 named it).
- **Unlanded items to watch**: the two re-sweeps (round-9 leg 2, open); cases
  5/6 embedding (tool owner's call); census §5 re-pin errata; attestation leg
  (r7 U1); fleet-contributed case; cite-check's full sweep (queue head,
  unclaimed); mado's and tsukuroi's owner lanes mid-edit (their gates are
  moving — the next tick re-reads them); `service-limits.md`'s U1–U3 (driver
  invocation; handler-present hosts; request-side secrets refusal untested).
- **Shared scratch**: `/tmp/w9-tameshi-{t91,t93,scr-t9}`, `/tmp/w9-t9-2`,
  `/tmp/w9-ver-t9-work`, `/tmp/w9-aud-t9-{work,evidence}`, `/tmp/w9-prept10*`,
  `/tmp/w9-scrb9`; sibling lanes `/tmp/w9-tsukuroi-s9*`, `/tmp/w9-mado-m9*`;
  /tmp is volatile — the notes/reports carry the reproduce blocks, not the
  scratch. Foreign scratch is never removed (service-limits row j).
