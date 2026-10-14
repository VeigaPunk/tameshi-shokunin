# AUD-T10 — verdict table: cold-read audit of the round-10 operator runbook + the 6-leg regression

Audit run 2026-10-14 20:53–21:06Z by lane AUD-T10 (round-10 32-lane wave; lane
scratch `/tmp/w10-aud-t10-{work,evidence}/`). **Read-only: no fleet file was
written or edited by this audit.** The tameshi tree, the instrument and all four
sibling repos were read only; the instrument's `--selftest`/`--regression` runs
write only into `/tmp` workdirs. No substrate-mutating command was run against a
fleet repo; no secret file read; no external site contacted. The assignment was
"do NOT edit" — my only fleet write is this report (a new file), per the
r7/r8/r9 audit precedent (`reports/r7-aud-t7.md`, `r8-aud-t8.md`, `r9-aud-t9.md`).

## 0. What was audited, and the frozen revisions

Two objects, both landed by concurrent round-10 lanes inside this audit's window:

| object | identity at freeze | state |
|---|---|---|
| **the runbook** — `corpus/knowledge/operator-runbook.md` (T10-1) | `e1e349b69d798acb…`, 511 `wc -l` / 31 416 B, mtime 20:57:29Z | untracked (`??`) at freeze |
| **the instrument** — `tools/mutate-and-run.sh` (T10-2) | `75ed934dc86360f5…`, 1 642 `wc -l` / 77 904 B, `VERSION='mutate-and-run.sh r10-2 …'`, mtime 21:00:00Z | worktree ` M` (uncommitted) at freeze |

Tameshi HEAD `b8eb96e` throughout; other pending round-10 writes at freeze:
`?? corpus/knowledge/service-standing-state.md` (T10-3), `?? plans/round-11.plan.md`.

Both objects moved inside the window and were each sampled until stable
(20 s cadence, three consecutive identical samples, `evidence/stability.log`,
`evidence/poll2.log`):

- **tool:** held `cf41efaa…` (= HEAD blob) → `818889d0`/1 358 L (20:54:11Z) →
  `8624cf7d`/1 359 → `ac779b91`/1 373 → `efe38d2f`/1 497 → `4b3dfed5`/1 509 →
  `5807fd38`/1 547 → `46877c8b` (20:59:22) → `17208c11` (20:59:52) →
  **`75ed934d`/1 642 stable from 21:00:22Z** through my close (21:05:33Z).
- **runbook:** `ed73e302`/480 L (first read 20:53Z) → `6d3a87e8` → `766879ac` →
  **`e1e349b6`/511 L stable from 20:56:13Z** through close.

The runbook's own errata ER-R1/ER-R2 (appended ~20:58/21:00Z) already record the
tool's in-flight move up to `5807fd38…` and state the remedy: "**T2 is the
fix** — when the edit lands, re-run `--selftest` and `--regression` under the
new revision and record both pins". This audit executes exactly that step.

## 1. The cold-read test — two procedures, re-run from the runbook alone

I froze `operator-runbook.md` (`e1e349b6…`) and followed its text for execution
decisions. Verdict vocabulary (the round-3 precedent,
`corpus/knowledge/executor-test-sufficiency.md:106-109`): **SUFFICIENT** /
**SUFFICIENT (latitude)** / **ADDITIVE-IMPROVISATION** / **NOT EXERCISED** /
**ADAPTED**.

**Contamination statement (O).** This is a *declared-contamination* read, not the
naive-executor seat: before executing I had read the runbook in full, plus
`SKILL.md:1155-1270`, `fleet-kill-rate-ledger.md:283-364` (ER-3/ER-4, the
command set's source), `plans/round-10.plan.md`, the tool's source, and the r9
audit. Where the runbook's text was thin I may have filled gaps from that
context; every such point is named below, so each "latitude" verdict is a lower
bound on a true stranger's friction. I used no oral context, wrote nothing
outside `/tmp/w10-aud-t10-*`, and read no live session.

### P1 — the operator loop: instrument gates + six-case pin read (§0 steps 1–3; §2/§6/§7 readouts)

| step (runbook ref) | verdict | record |
|---|---|---|
| (a) tool sha, "is the tool the revision the records were measured under?" (§0(1), §2) | **SUFFICIENT** | `sha256sum` → `75ed934d…` (1 642 L); the stamp says `cf41efaa` → the checksum step itself correctly reads **moved** (T2) — evidence `p1a-tool-sha.txt` |
| (b) `--selftest` (§0(2)) | **SUFFICIENT** | `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0, 5.1 s — evidence `p1b-selftest.log` |
| (c) `--regression --workdir …` (§0(2), §7) | **SUFFICIENT** | `REGRESSION: PASS (cases=6 passed=6; ledger legs exact…)`, rc 0, 81.7 s, `REGRESSION_DATE 2026-10-14T21:01:53Z`; the receipt's expectations (§7 "four legs") do **not** match the observed six — see §4 row 7. The command, flags and workdir-retention rule ran exactly as written |
| (d) six-case pin read, ER-3's command set (§0(3)) | **SUFFICIENT (latitude)** | all four commands per case as written; 21:03:26Z: 4 `current` · 1 `stale` (mado-verify) · 1 `stale+drift` (tsukuroi-census, worktree `10452443…` ≠ HEAD blob `c396662e…`, path-scoped ` M`) — evidence `p1d-pin-read.txt` |

Latitude points, precisely:

1. **`REV` resolution.** §0(3) says "`<gate-file>` / `<owner-repo>` / `<path>` /
   `REV` are the case's recorded row (§3)". §3's table carries file + pin + rate +
   ledger anchor but **no revision**; the revisions live in §6's executed-tick
   table ("recorded pin @ rev") and §7's leg list. Naming §3 alone sends the
   reader one section away for `REV`; the value is recoverable and I resolved it
   from §6, cross-checked against the tool's own `REGRESSION_PIN … rev=` lines.
2. **The reading map's `drift` parenthetical.** §6 renders drift as "worktree
   differs from HEAD (porcelain non-empty, or live sha ≠ HEAD blob sha)". Read
   literally, any untracked file in a sibling repo makes its row `drift`; ER-3's
   command set scopes the porcelain check to `<path>`
   (`git … status --porcelain -- <path>`). I applied the anchored command set
   (path-scoped), which is also what produces the runbook's own readings
   (mado has unrelated untracked files yet reads `stale`). The map's wording is
   looser than the command set it renders; the anchored source governs.
3. **Compound readings.** tsukuroi-census satisfies both `stale` (recorded rev
   ancestor, live blob differs) and `drift` (worktree ≠ HEAD) at once; the map
   presents two-valued readings, while ER-4's addendum precedent writes
   `stale + drift`. I recorded the compound and note the map does not spell it
   out.

### P2 — the append-discipline drill (§6, on a scratch copy)

Runbook text: "pre-append **36 169 bytes byte-identical** (`head -c 36169 copy |
cmp -` → rc 0), then the drill row appended below; the real ledger's sha
unchanged (`2f25c51e3e0a7851…` before = after; scratch `/tmp/w10-t10-1/ledger-copy.md`,
drill block `DR-1`)".

| step | verdict | record |
|---|---|---|
| copy → prefix byte-identity | **SUFFICIENT (latitude)** | `head -c 36169 copy \| cmp - <ledger>` → rc 0; the printed command's `cmp -` lacks its second operand — reconstructed from context (the audit's own r9 form uses `cmp <file>`); evidence `p2-append-drill.txt` |
| drill row appended below the last line | **ADAPTIVE/ADAPTED** | no row schema is given for a drill; I recorded a clearly-labelled `DR-A10` no-rate block below the last entry |
| real ledger unchanged | **SUFFICIENT** | `2f25c51e3e0a7851…` / 36 169 B before = after; the copy advanced to `02e0f5f9…` / 36 465 B |

## 2. The 6-leg regression — re-run, and independently checked

My run (evidence `p1c-regression.log`, workdir retained
`/tmp/w10-aud-t10-ev/p1-regression/`):

```
REGRESSION_TOOL: …/tools/mutate-and-run.sh sha256=75ed934d…
REGRESSION_DATE: 2026-10-14T21:01:53Z
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10
  bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10
REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)   rc 0
```

| leg | materialized rev | pin sha256 | sweep | table | restore |
|---|---|---|---|---|---|
| js-kimi-census | `175de6ba…` | `83016d45…` | 8/10 (80 %) | match=10/10 flips=0 | OK before=after=pin |
| bash-surface-census | `fecee874…` | `275d8294…` | 8/10 (80 %) | match=10/10 flips=0 | OK |
| bash-tsukuroi-census | `165307fe…` | `084951be…` | 6/10 (60 %) | match=10/10 flips=0 | OK |
| bash-mado-verify | `eead56b2…` | `d7edaab4…` | 4/10 (40 %) | match=10/10 flips=0 | OK |
| **bash-checklist-run** | `fecee874…` | `7e5ec98b…` | 7/15 (47 %) | match=15/15 flips=0 | OK |
| **js-claims-check** | `175de6ba…` | `e9a21b44…` | 7/10 (70 %) | match=10/10 flips=0 | OK |

Independent checks (not trusting the tool's own selftest, which also asserts
them):

- **Every leg re-materialized from git and re-parsed** (`/tmp/w10-aud-t10-work/leg-check.py`):
  blob sha == recorded pin ×6; materialized `target.*` sha == pin ×6; every
  embedded `@old` occurs **exactly once** (10/10/10/10/15/10 strings);
  `@new ≠ @old` ×6 → `LEGCHECK: PASS (6/6 legs clean)` (`legcheck.txt`).
- **Per-leg sub-invocation output** (each `sweep.log`): `CONTROL: GREEN` with
  `pristine-sha256` = the pin, `MUTATE_RESTORE: OK (before = after = pristine)`,
  `MUTATE: DONE` at the expected rate — ×6.
- **Legs 5/6 expectations vs their source notes**: kagi checklist "7/15 = 46.7 %,
  printed 47 %" (`mutation-case-kagi-checklist.md:130-131`); kumitate claims
  "kill rate 7/10 (70 %)" (`mutation-case-kumitate-claims.md` §1) — both match
  `REGRESSION_EXPECT` and the measured tables.

## 3. The runbook's own receipts, checked — and the divergence that is the finding

- **Receipts at the stamped revision are honest.** I materialized the HEAD blob
  of the tool (`git show HEAD:tools/mutate-and-run.sh` = `cf41efaa…`, exactly the
  stamp) into a scratch fleet skeleton and re-ran it:
  `--selftest` → `67/67 pass`; `--regression` → `REGRESSION: PASS (cases=4
  passed=4 …)`, rc 0 (`head-replay.log`, `head-selftest.txt`). §7's quoted
  receipt block and §9's receipt list reproduce at their own revision.
- **The 4-vs-6 divergence (the finding).** The frozen runbook states the tool's
  contract revision is `cf41efaa…` (r7-1, 1 341 L) and that "`--regression`
  carries four legs; cases 5/6 are **not embedded**" (§2, §3, §7). At the landed
  revision (`75ed934d…`, r10-2, 1 642 L, VERSION line r10-2) the regression
  carries **six** legs and the operator who follows §7 will see `cases=6
  passed=6`, not `cases=4 passed=4`. The runbook's own rules cover this — the
  anchored source governs, and ER-R1/R2 name the move and prescribe T2 — but as
  written the operator-facing "embedding status" and the §2 contract line are
  **stale against the tool that will ship in the same commit**. Neither file
  smoothed it; the divergence is recorded here as the audit's finding, not
  repaired (assignment: do not edit).
- **Reader-side drift falsifier** (§6/§9 claim) reproduced: a `/tmp` copy of
  kagi's `surface-census.sh` with one line appended hashes `8f25008f…` vs the
  HEAD blob `275d8294…` → would read `drift`, while the substrate shows 0
  porcelain lines after (`falsifier-drift.txt`).
- **Runbook's executed tick (§6)** was true at its timestamp (20:52Z); at my
  21:03:26Z read the same six cases read 4 · 1 · 1 and its row 3 has moved from
  `stale`, clean, to `stale + drift` because tsukuroi's own round-10 lane is
  editing its gate mid-window (` M tools/tsukuroi-census.sh`). A moving file is
  never re-interpreted; both readings stand at their timestamps.

## 4. Verdict table

| # | claim audited | verdict |
|---|---|---|
| 1 | The round-10 runbook landed and is runnable as the service's single operator document | **CONFIRMED — with a relocation**: it landed at `corpus/knowledge/operator-runbook.md`, not `HANDOFF.md` at repo root (the round-10 plan's landing shape; the plan allows relocation if the coverage row moves with it). Note for the wave: the T10-4 / VER-T10 polls watch for `HANDOFF.md` / `*handoff*` and will not see this path |
| 2 | P1: the operator loop (tool sha → selftest → regression → six-case read) is executable from the runbook alone | **SUFFICIENT (latitude)** — every command ran as written; two latitude points (REV resolution, drift-map wording), one compound-reading gap (§1) |
| 3 | P2: the append drill is executable from §6 | **SUFFICIENT (latitude)** + one ADAPTED cell (drill-row format); the strong property — real ledger untouched — reproduced |
| 4 | The selftest step, executed | **CONFIRMED** at both revisions: `80/80` at the landed `75ed934d…`; `67/67` replayed at the stamped `cf41efaa…` |
| 5 | The 6-leg regression | **CONFIRMED** — `cases=6 passed=6`, exact band, rc 0, 81.7 s; 6/6 independent leg-check; control green + `MUTATE_RESTORE: OK` ×6; legs 5/6 expectations equal their source notes |
| 6 | The runbook's §7/§9 receipts (4 legs, 67/67 at `cf41efaa…`) | **CONFIRMED at their revision** (my replay) — the divergence from the landed tool is a revision fact, not a fabrication |
| 7 | The runbook's embedding-status and contract-revision lines (§2/§3/§7: four legs; cases 5/6 not embedded) | **STALE at the landed revision** — the finding; the anchored source (the tool) governs; ER-R1/R2 record the move but predate the landing |
| 8 | Six-case pin read as commanded | **CONFIRMED** at 21:03:26Z: `current=4 stale=1 stale+drift=1`; all recorded revisions ancestor-of-HEAD (rc 0 ×6); the difference from the runbook's 20:52Z tick is a live writer on tsukuroi's gate |
| 9 | The append proof (`head -c 36169`; real-ledger sha `2f25c51e…` unchanged) | **CONFIRMED** on the scratch copy |
| 10 | Reader-side drift falsifier (scratch copy reads `drift`, substrate clean) | **CONFIRMED** |
| 11 | tool `held|moved` is single-valued as the map words it ("vs the sha on the last `REGRESSION_TOOL`/`MUTATE_TOOL` line") | **AMBIGUOUS at this window** — two legitimate anchors disagree: vs the records' pin (`cf41efaa…`) the tool is **moved**; vs my own latest receipt line (`75ed934d…`) it is **held**. I recorded both; the map should name its anchor |
| 12 | This audit wrote nothing but this report; substrates read-only | **CONFIRMED** (all writes under `/tmp/w10-aud-t10-*`; per-leg workdirs retained there) |

## 5. Spot-checks (three, re-runnable)

- **SC1 — the 6-leg regression.**
  `bash tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/…` →
  `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0
  flips<=0)`, rc 0, `REGRESSION_TOOL sha256=75ed934dc86360f5…` (log
  `p1c-regression.log`; ~82 s).
- **SC2 — embedded legs are real, pinned, unique.**
  `python3 /tmp/w10-aud-t10-work/leg-check.py <fleet-root> <workdir>` →
  `LEGCHECK: PASS (6/6 legs clean)`; e.g.
  `git -C kagi-shokunin show fecee874:corpus/checklist-run.sh | sha256sum` →
  `7e5ec98b9e1d0afa…` and `git -C kumitate-shokunin show
  175de6ba:scripts/claims-check.mjs | sha256sum` → `e9a21b44f1216bf…`, both equal
  to the tool's `REGRESSION_PIN` lines and to the ledger/notes' recorded pins.
- **SC3 — the runbook's own receipt at its own revision.**
  `git -C tameshi-shokunin show HEAD:tools/mutate-and-run.sh` → `cf41efaa…`;
  run it from a scratch fleet skeleton → `cases=4 passed=4`, `67/67 pass`
  (`head-replay.log`, `head-selftest.txt`).

## 6. Unknowns

- **U1 — freeze vs commit.** Both audited objects are uncommitted/untracked at my
  freeze (tool ` M`, runbook `??`); the round-10 commit had not landed. Verdicts
  bind to `75ed934d…` / `e1e349b6…`; a later revision must be re-resolved
  (`SKILL.md:1269-1270`).
- **U2 — the runbook may be re-stamped.** T10-1's errata stop at `5807fd38…`
  (ER-R2); whether an ER-R3 records the landed `75ed934d…` (and the 6-leg cut)
  is unknown at this write — if it does, §4 row 7 is closed by the author lane,
  not by me.
- **U3 — relocation follow-through.** Whether the coverage map / `corpus/README.md`
  row and the fleet hand-off will name `corpus/knowledge/operator-runbook.md`
  (and whether T10-4/VER-T10's `HANDOFF.md`-specific polls record "not landed"
  while the runbook exists) — observed, not resolvable here.
- **U4 — single host** (`plazir27`), 2026-10-14; timings (81.7 s / 45.3 s /
  5.1 s) are host-local.
- **U5 — timestamped readings.** The pin read's `drift` cell and the sibling
  worktrees are moving under their own lanes' writers; re-read before quoting.
- **U6 — contamination.** This cold-read is contamination-declared (§1), not the
  naive-executor seat; VER-T10's or a later fresh-executor run is the independent
  test the runbook's §9 names as not executed.
- **U7 — scratch volatility.** All evidence lives under
  `/tmp/w10-aud-t10-{work,evidence}/`.

## 7. Errata (append-only)

(none yet — new entries go below this line, never edits above)