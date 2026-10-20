# RoutedLedger — cross-round ledger of routed verifier defects

Seat: `TameshiR16.RoutedLedger` (connector, leaf). Round 16, wave 2 (falsify).
Pinned revision: `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (round-16 wave-1 landing;
`git show -s` → lane identity `tameshi-shokunin <tameshi@shokunin.local>`, 2026-10-20 10:49:37 -0300,
subject `round-16: land js-round-gate case 7, cold-read repairs, sources S052-S057, attribution repair`).
Every lane read below is `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <rev>:<path>`.
Read-only except this file. Scratch: `/tmp/tameshi-r16w2-RoutedLedger-3gl3dm/` plus per-check
`mktemp -d` dirs. No tool installs/upgrades; no pacman/uv/npx/cargo transaction; REA MCP unused.

## 0. Sources, extraction rule, age convention

Five `corpus/lessons/round-*-verifier-spotcheck.md` files exist at the pin; all were parsed.

| file | sha256 at c699c8c | "Routed defects" heading | numbered items |
|---|---|---|---|
| `round-1-verifier-spotcheck.md` | `f99ef0ae2b3a3e4939c86b9ce5ab1e701733801c1cc1c7063767edf692e0edad` | **none** — debts sit in `## Adjudication`, :17 | 2 debts (box-3; 19 provenance headers) |
| `round-12-verifier-spotcheck.md` | `6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30` | `:140` | 4 (`:144-147`) |
| `round-13-verifier-spotcheck.md` | `6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420` | `:175` | 5 (`:179-183`) |
| `round-14-verifier-spotcheck.md` | `d267576a0d165d81b734b6c40b5b80bf61ccd9c24c8765992093afbd097cf654` | `:154` | 5 (`:156-160`) |
| `round-15-verifier-spotcheck.md` | `cbc9a81176afbb0e723458e3629c5080f19eb2ecb8c4172753b8b55e55d96fde` | `:157` | 5 (`:159-163`) |

19 top-level items. Two compound items are split at their own semicolons — R12.3 into
`3a` (host-addendum line citations) and `3b` (`declaration.kind=null`), R13.4 into
`4a` (Report-path trailer) and `4b` (append helper) — yielding **21 rows**:
**11 closed, 10 open**. Items that name several carried debts (R12.4, R13.5, R14.3, R15.5)
stay one row and are expanded in §2.

Age convention: **age = 16 − the round that first routed the item**, counted while the item is
still open at c699c8c. Origin r1 → 15 rounds; r12 → 4; r13 → 3; r14 → 2; r15 → 1.

Record defect in the source set, disclosed up front: `round-14-verifier-spotcheck.md:160`
is truncated **inside the committed file** at 844 chars, ending `…defects in the non-cla…`.
The operative instruction (register capture-context as a gate, add a standalone selftest, map
exit 64) is legible; the tail is not. Not caused by this seat's read.

## 1. Master ledger

Status is `closed (<commit>)` when a later round's committed artifact discharges the item at
c699c8c; `open (<age> rounds)` otherwise. Lane commits are abbreviated to 7 hex; full hashes
are in the spot-check headers cited in §0.

| ID | Routed at | Item (verbatim scope, abridged) | Status at c699c8c | Evidence |
|---|---|---|---|---|
| **R12.1** | r12:144 | Operator/hyaku renderer appended **relative** seat `Report:` paths while tools run from fleet root; preserve the absolute/lane-root correction in future dispatched text. | **closed (c699c8c, dispatch text)** | `.ufo/waves/round-16/spec1.json` → `context` line 7: "Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/tameshi-shokunin — write it at …/<that path>"; line 9 makes `agent://TameshiR16` mandatory. Each of the 68 `dispatch1.json` task texts also carries the absolute write path ("Write your report at /home/vgpnk/Projects/shokunin/tameshi-shokunin/…"). The hyaku renderer source itself is operator-owned and was not inspected. |
| **R12.2** | r12:145 | Operator closure mechanics: run-now capability wording conflicts with the Gate standard's non-execution rule; the append helper is not the full committed frozen closure-status/history-pin checker. | **open (4 rounds)** | `ls /home/vgpnk/Projects/shokunin/scripts/closure-check.py` → `No such file or directory`; fleet has only `scripts/hyaku/append-closure.py` and per-round `.ufo/waves/round-{12,13,15}/closure-check.py` (no round-16 closure checker). Lane contract forbids fleet-script edits. |
| **R12.3a** | r12:146 | Replace brittle host-addendum **line citations** with the named planner-ruling section in an append-only correction. | **closed (4acc607, r13)** | `corpus/lessons/round-13.md:39` records the new citation as the named "Planner seat (orchestrator ruling 2026-10-19, kama/tsukuroi r11–12 L0 lines)"; `git log -S'Planner seat (orchestrator ruling 2026-10-19'` → `4acc607`. |
| **R12.3b** | r12:146 | Disclose/repair nested `declaration.kind=null` metadata without rewriting the frozen declaration. | **closed (4acc607, r13)** | `.ufo/evidence/round-13/witness-metadata-old-null.json` (old-null FAIL) and `.ufo/evidence/round-13/claims.json:6` (normalized companion, 6→6); round-13 delivered `7dd16d9`. Round-14 spot-check C1 confirms. |
| **R12.4** | r12:147 | Tameshi carried debt: box-3, legacy provenance headers, F1 interop, stale-successor ledger, runbook. | **open (4 rounds)** | All five sub-items still open at the pin — §2 rows B1–B5. |
| **R13.1** | r13:179 | `expected.json expected_checks.producer_before` still demands the exact kind assertion from a run that crashed earlier; add an effective/superseded disposition. | **closed (0c6e36d, r14)** | `.ufo/evidence/round-14/dispositions.json` row `producer_before`: `state=superseded`, reason names the `FileNotFoundError` setup failure, `superseded_by=["producer_before_oracle","producer_after_oracle"]`; delivered `13c1367`. |
| **R13.2** | r13:180 | GIT_DIR-poisoning check retains no injected-env field; record bounded injected variables or a reproducible setup, and explicit mapping results. | **closed (6431478, r14)** | `.ufo/evidence/round-14/context-receipt.json` (26,427 B) contains the poison path and injected-environment block; round-14 spot-check C1 records injection `/nonexistent/tameshi-round14-poison`, baseline absence, and five true mapping checks. |
| **R13.3** | r13:181 | Knowledge §6 is a deferred-at-write account; add a later empirical backlink and prefer S048 wording. | **closed (0c6e36d, r14)** | `corpus/knowledge/incremental-pin-disposition.md:316`: "This addendum supersedes only section6's **deferred-at-write** status"; `git log -S'deferred-at-write'` → `0c6e36d`. |
| **R13.4a** | r13:182 | Retain the relative seat-Report trailer correction in the validated future context/body, not just outer instructions. | **closed (c699c8c, dispatch text)** | Same `spec1.json` context lines 7–9 and the same per-task absolute write path as R12.1 (`dispatch1.json`, 68 tasks); the wave-2 per-seat Acceptance block repeats the lane-root-relative rule. |
| **R13.4b** | r13:182 | Authorized append helper is not the full canonical frozen closure checker. | **open (3 rounds)** | Same operator evidence as R12.2; no `scripts/closure-check.py`, no round-16 closure checker. |
| **R13.5** | r13:183 | Carried debt: box-3, legacy provenance, F1, successor sweeps (kimi/tsukuroi/mado), runbook. | **open (3 rounds)** | §2 rows B1–B5; no successor-sweep artifact in `.ufo/evidence/round-16/`. |
| **R14.1** | r14:156 | Status record: "prior routed items 1–3 addressed within their bounded scopes". | **closed (13c1367, r14; record re-verified)** | All three closing artifacts exist at the pin: `dispositions.json` (r13.1), `context-receipt.json` (r13.2), `incremental-pin-disposition.md:316` (r13.3). |
| **R14.2** | r14:157 | Operator: append helper is not a frozen closure-status/history-pin checker. | **open (2 rounds)** | §R12.2 evidence. |
| **R14.3** | r14:158 | Carried debt: box-3, legacy provenance, F1, successor sweeps, runbook. | **open (2 rounds)** | §2 rows B1–B5. |
| **R14.4** | r14:159 | Preserve the no-mid-flight-check instruction next round (one seat's AST/plain-git check breached it). | **closed (c699c8c, dispatch text)** | `spec1.json` → `context` line 10: "no build/lint/test/formatter runs on lane code mid-flight unless your Target says to execute something". Caveat: the same wave breached a sibling rule — RGLeg edited `tools/mutate-and-run.sh` in place while readers ran (`lessons/round-16.md:56`), now QUALITY 20. |
| **R14.5** | r14:160 | Register `capture-context.py` as a gate; add a standalone isolated self-invocation; map exit 64 explicitly to could-not-evaluate. | **closed (0494c24, r15)** | `SKILL.md:1680` gate row with selftest command and `2 and 64 could-not-evaluate … 64 usage_error`; `tools/context-capture.py` carries `--selftest` (`SELFTEST: PASS` writer at :1785). Round-15 spot-check measured gate=1, standalone=1, explicit64 classes=2. |
| **R15.1** | r15:159 | Complete the uncredited **sibling-overlap connector function** (23-lane scan), with failed-seat accounting preserved. | **open (1 round) — artifact landed, own credit gate unmet** | `w1/Overlap1.md` lands 23 `O-NN` rows and a 30-digest manifest inline, but (a) `:34` still says "SKILL.md absent in audio/game-dev-2d/game-dev-3d/revenger" while `:47` says the three missing are audio, game-dev-2d, revenger (18/21 have both files) — the RoutedDisposition erratum was not applied; (b) `git cat-file -e c699c8c:.ufo/evidence/round-16/Overlap1/manifest.sha256` → exit 128; the directory is absent from the commit (it exists only as an **uncommitted** worktree copy). `lessons/round-16.md:7-9` claims item 1 done — premature at this pin. |
| **R15.2** | r15:160 | Repair usage-finding attribution in the integration verifier; demonstrate old misattribution and corrected finding on the same fixture/argv; name the two affected rows; retain `verification-3.json`. | **closed (c699c8c)** | `.ufo/evidence/round-16/attribution/correction.json` names exactly `usage-proof-new` and `gate-usage`, `context_consistent → usage_error`, `coverage_changes=[]`, source sha `3c419055…d8ce` = committed `verification-3.json`; `verify.py` untouched (`7e4519d9…2522`). Executed: `reattribute.py --selftest` → exit 0, `SELFTEST: PASS (new rule 4/4; old rule fails 3/4)`; regeneration reproduces committed correction sha `1caf1237…`. QUALITY 18 at `QUALITY.md:88-96`. |
| **R15.3** | r15:161 | Continue execution discipline: SpecClean's mid-flight synthetic checks and the SpecMismatch/Types/Environment/Mapping probes stay process incidents; transcribers get no runtime credit. | **open (1 round)** | QUALITY 20 (`QUALITY.md:102-107`) is about in-place instrument edits, **not** seat-executed mid-flight checks; RoutedDisposition recommended this class become a criterion, but the landed criteria are 18 (attribution), 19 (misroot), 20 (in-place edit). The dispatch clause exists (`spec1.json` context :10) but no gate/criterion binds the SpecClean class. |
| **R15.4** | r15:162 | Operator: inherited closure-checker debt. | **open (1 round)** | §R12.2 evidence. |
| **R15.5** | r15:163 | Prior bounded residuals: box-3, legacy provenance, F1, whole-F7 reuse, runbook, successor sweeps; note defect 5 resolved. | **open (1 round) — 6/6 sub-items open; defect 5 confirmed resolved** | §2 rows B1–B6. Prior defect 5 is resolved: `SKILL.md:1680` gate row and r15 spot-check C1. |

Counts: **11 closed / 10 open**. The operator closure-checker debt alone occupies four rows
(R12.2, R13.4b, R14.2, R15.4) and has not moved since r12; the lane cannot repair it
(`scripts/`, `MANIFEST.json`, `.ufo/state/` are outside the lane write scope).

## 2. Long-running residuals (the idea's named residuals)

| ID | Residual | First routed | Age | Status at c699c8c | Evidence |
|---|---|---|---|---|---|
| **B1** | Full-page SKILL cold-read / box-3 | `round-1-verifier-spotcheck.md:17` | **15 rounds** | **open** | `.ufo/evidence/round-16/coldread/ledger.json` absent (`git cat-file -e …` exit 128, "does not exist in 'c699c8c'"). `SHONEN.md:9-10` still `[~]` and links that absent path. Executed committed `measure.py --rev c699c8c` → exit 0: `coldread {sections_total:54, sections_covered:0, box3_full_page:false, ledger_present:false}`, `shonen.box3_ledger_link:false`, `restraint 6`. Synthetic contrast (§4 item 2): complete ledger + the real two-line SHONEN layout → 6; single-line layout → 8. Wave-1 cold-read itself: 32 seat JSON blocks, **51/51 snapshot buckets** observed, but the delivered page has **54 sections**: 40/54 are byte-identical to an observed snapshot section; **14 lack an observation at the delivered sha** (11 repaired sections + 3 new headings `:1707`, `:1740`, `:1789`). Verdict tally: 22 executed-ok / 21 verified-record / 6 gap-minor / 5 wrong-expectation. |
| **B2** | 19 legacy provenance headers | `round-1-verifier-spotcheck.md:17` | **15 rounds** | **open** | At the pin `corpus/knowledge/` has 24 files; 19 lack `^source:` (5 carry it). `corpus/README.md:91-95` still routes the repair to the operator ("prepending would shift every `path:line` cite"). New entry `mutation-case-kumitate-round-gate.md` carries the header, as required. |
| **B3** | F1 interop (ledger leg as schema JSON) | `round-12-verifier-spotcheck.md:147` | **4 rounds** | **open** | `corpus/README.md:78`: "validator unavailable this round: U". `grep -n -- '--json' tools/mutate-and-run.sh` → exit 1, no match: the runner emits six/seven text `PIN_*` legs only. |
| **B4** | Stale-successor ledger / owner-approved successor sweeps (kimi, tsukuroi, mado) | `round-12-verifier-spotcheck.md:147`; named per leg at `round-13-verifier-spotcheck.md:183` | **4 rounds** | **open** | `.ufo/evidence/round-16/` has no re-sweep artifact. The only fleet-ledger change this round appends the case-7 row (`fleet-kill-rate-ledger.md:403-414`) and leaves the successor debt named. Round-13's changed-leg reading stands as intake, not sweep. |
| **B5** | Operator runbook corrections (ER-R3) | `round-12-verifier-spotcheck.md:147` | **4 rounds** | **open** | `operator-runbook.md:173-175` and `:374`: harness "carries four legs; cases 5/6 are **not embedded**"; the runner now carries **7** cases (`tools/mutate-and-run.sh`, seven `#   js/bash-*` lines; `measure.py` → `recorded_cases=7`). README `:98` still names ER-R3 open. |
| **B6** | Whole-F7 per-leg reuse decisions | `round-15-verifier-spotcheck.md:163` | **1 round** | **open** | `corpus/README.md:84` F7 `open`; `:175` "full F7 per-leg **reuse-decision** frontier remains open". The seventh leg is a new case, not a reuse decision. |

## 3. Falsification detail on this round's three live closure claims

### 3.1 R15.2 — holds (executed, not merely read)

- Committed `correction.json` names two rows and only two: `usage-proof-new`, `gate-usage`;
  both `context_consistent → usage_error`; `coverage_changes: []`; `source_receipt.sha256`
  `3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` equals the hash of
  `.ufo/evidence/round-15/verification-3.json` at the pin.
- `verify.py` is byte-unchanged from round 15: sha256 `7e4519d9a0ea68ebbd02890629f06a6fac8e6eab034d9fa3b19d386b088a2522`.
- Executed from scratch (receipt materialized at the script's expected `LANE_ROOT`):
  `python3 …/reattribute.py --selftest` → exit 0, four cases, old rule fails 3/4
  (`usage-proof-new`, `gate-usage`, `forged-first-line`), new rule passes 4/4,
  `usage-proof-old` passes under both. Correction-mode rerun regenerates
  `correction.json` sha `1caf1237af5890beac86c8be04d9c25849c710128da9fd346738217f60bfcea1`
  = committed bytes. **Closed.**
- Minor record defect: `w1/RoutedDisposition.md` quotes `correction.json` `34455895…`
  and `reattribute.py` `8804ca2d…` and "7 coverage_changes"; committed bytes are
  `1caf1237…`, `b81086b0…`, and `0` coverage changes. That seat read a transient draft
  (it discloses live edits); the closure does not depend on those quoted hashes.

### 3.2 R15.1 — falls at this commit (partial artifact, unmet credit gate)

- The scan exists: `w1/Overlap1.md` carries 23 `O-NN` rows (one per `shokunin.conf` lane),
  a 30-digest manifest at `:49-95`, a 29/30 replay with the `MANIFEST.json` drift named at `:91`,
  and the corrected coverage statement at `:47` (18 of 21 lanes have both `PROVINCE.md` and `SKILL.md`).
- The scan's own acceptance conditions, as spelled out by `w1/RoutedDisposition.md`, are not met
  in the commit: `:34` still lists `game-dev-3d` as SKILL-less (it has `SKILL.md`), and
  `.ufo/evidence/round-16/Overlap1/manifest.sha256` does not exist at `c699c8c`
  (`cat-file` exit 128; an uncommitted worktree copy exists and is excluded from this status).
- `w1/Overlap2.md` is a different, narrower scan (kama r16 / kaidoku r17 path-and-write-target
  overlap) and does not substitute for the 23-lane PROVINCE/SKILL scan.
- `lessons/round-16.md:7-9` states items 1 and 2 are "done this round". Item 2 is; item 1 is
  not discharged at this pin. **Open (age 1) / partial.**

### 3.3 box-3 / C2 — falls at this pin (the named counter returns 6)

`lessons/round-16.md:5-7` claims **C2 calibration 6→8** from the full-page cold-read. At
c699c8c the named evidence does not exist and the named counter does not award it:

- `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` → exit 128;
  `SHONEN.md:9-10` links the absent path.
- Executed committed `.ufo/evidence/round-16/measure.py --rev c699c8c --repo <lane>`
  (copy in scratch) → exit 0, `calibration_restraint_score: 6`,
  `depth_score: 7`, `recorded_cases: 7` (leg `js-round-gate` present),
  `coldread.sections_total: 54`, `sections_covered: 0`, `ledger_present: false`,
  `shonen.box3_ledger_link: false`.
- Independent of the missing ledger, the counter cannot see the link: `BOX_RE`
  (`measure.py:62`) captures only the bullet line, and `box3_link` (`:262`) tests
  `BOX3_LINK in boxes[2][1]`; the real link sits on SHONEN's continuation line 10.
  Executed synthetic proof with a complete 4/4 ledger: SHONEN single-line link → 8;
  SHONEN two-line (the real layout) → 6, while `box3_full_page` is true in both.
- `SCORECARD.md` at the pin is 551 lines and contains **no round-16 section** (`grep -i 'round 16'`
  empty; the tail still ends round 15's "Next intended claim remains freshness"). The 6→8
  claim has no scorecard accounting at this commit.
- Wave-2 worktree repairs exist (`git status --porcelain` at read time: `M measure.py`,
  `M w1/Overlap1.md`, `M corpus/lessons/round-16.md`, `?? .ufo/evidence/round-16/Overlap1/`,
  `?? .ufo/evidence/round-16/measure-repair/`, `?? .ufo/evidence/round-16/coldread/anchor-check.py`,
  `?? .ufo/waves/round-16/w2/`). They are **not** in c699c8c and are excluded from every status
  above; they are consistent with these defects being known and under repair.

**Verdict on the attack: box-3/C2 does not hold at c699c8c.**

## 4. New defects observed at the pin (not routed by any prior spot-check)

1. **Dangling box-3 evidence link.** `SHONEN.md:10` links `.ufo/evidence/round-16/coldread/ledger.json`;
   `cat-file` exit 128 at c699c8c. The link promises evidence the commit does not contain.
2. **`measure.py` cannot credit the real SHONEN layout.** `BOX_RE` at `:62` matches one line;
   `:262` searches only the bullet for the ledger path, but the path is on the continuation line.
   Executed contrast: complete ledger + real two-line layout → 6; single-line → 8. The selftest
   only exercises the single-line shape (`measure.py` `SHONEN_TEXT`), so it passes while the live
   page fails.
3. **Counter/ledger denominator drift.** The delivered `SKILL.md` (sha256
   `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4`) sectionizes to 54
   sections (preamble + 53 headings), while the round's own G10 rejects "50 sections" and the
   snapshot's cold-read covered 51 buckets. Three headings are new this round (`:1707`, `:1740`,
   `:1789`) and 11 existing sections were repaired; wave 1 cannot credit them at the delivered sha.
4. **Overlap1 erratum unapplied.** `w1/Overlap1.md:34` contradicts `:47` and `:123` on which lanes
   lack `SKILL.md`; the RoutedDisposition acceptance gate explicitly required the erratum before credit.
5. **Round-16 lesson overclaims R15.1.** `lessons/round-16.md:7-9` says routed items 1 and 2 are done;
   item 2 is, item 1 is not (see §3.2).
6. **RoutedDisposition hash drift.** The seat's quoted `correction.json`/`reattribute.py` hashes and
   coverage-change count do not match committed bytes (§3.1). The artifact itself is deterministic,
   so the closure survives; the seat report's evidence values do not.
7. **Round-14 spot-check record truncated mid-word.** `round-14-verifier-spotcheck.md:160` ends
   `…non-cla…` in the commit (844-char line). The instruction is recoverable but the record is lossy.

## 5. Commands executed (all read-only; lane tools run from /tmp copies)

| Command (abridged) | Exit | Key observed line |
|---|---|---|
| `git ls-tree -r --name-only c699c8c -- corpus/lessons/ \| grep verifier-spotcheck` | 0 | five files (r1, r12–r15) |
| `git show c699c8c:<each spotcheck> \| sha256sum` | 0 | hashes in §0 |
| `git show c699c8c:<spotcheck> \| nl -ba` around each `## Routed defects` | 0 | heading and item lines in §0/§1 |
| `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` | **128** | `fatal: path … does not exist in 'c699c8c…'` |
| `git cat-file -e c699c8c:.ufo/evidence/round-16/Overlap1/manifest.sha256` | **128** | `path … exists on disk, but not in 'c699c8c…'` (uncommitted worktree copy only) |
| `python3 <scratch>/measure.py --rev c699c8c --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin` | 0 | `recorded_cases 7 depth 7`; `coldread {sections_total:54, sections_covered:0, box3_full_page:false, ledger_present:false}`; `box3_ledger_link:false`; `restraint 6`; sources 55 rows A47/B6/C2 |
| `python3 <scratch>/reattribute.py --selftest` (receipt materialized at expected LANE_ROOT) | 0 | `SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)` |
| same script, correction mode (writes only scratch) | 0 | `corrections: usage-proof-new context_consistent->usage_error, gate-usage …`; regenerated sha `1caf1237…` = committed |
| synthetic repo built from committed `measure.SKILL_LINES` + complete 4-entry ledger; single-line vs two-line SHONEN; committed measure.py | 0 | single-line: covered 4/4, `box3_full True`, `link True`, score **8**; two-line: covered 4/4, `box3_full True`, `link False`, score **6** |
| Python parse of the last fenced `json` block in 32 w1 reports vs fence-aware sectionizer | 0 | snapshot 51/51 buckets; delivered 54 sections, 40 same-sha observations, 14 missing (11 changed + 3 new) |
| Python count of `S###` table rows in `corpus/SOURCES.md` plus footer read | 0 | 55 rows; S052–S057 present; `Next unused id: S058` |
| `grep -cE '^PIN_[A-Z_]+=' tools/mutate-and-run.sh` (committed bytes) | 0 | 7; case lines include `#   js-round-gate … 5/10 (50 %)` |
| `grep -n -- '--json' tools/mutate-and-run.sh` | **1** | no CLI flag (mutant string only) |
| `for f in corpus/knowledge/*.md; do grep -q '^source:' …` | 0/1 | 24 files, 19 missing |
| `ls scripts/closure-check.py` at fleet root; `find . -maxdepth 4 -name 'closure-check*'` | 2 / 0 | no canonical checker; only `.ufo/waves/round-{12,13,15}/closure-check*.py` |
| `git show c699c8c:SCORECARD.md \| grep -in 'round 16'` | 1 | no round-16 section (551-line file) |
| `grep -n 'SKILL.md absent' w1/Overlap1.md`; `ls-tree .ufo/evidence/round-16/` | 0 | `:34` stale; evidence tree = attribution/, census-start.txt, coldread/, measure.py, round-gate/ |
| `git status --porcelain` (lane worktree, read-only) | 0 | uncommitted wave-2 repairs listed in §3.3 (excluded) |

Tooling: none installed or upgraded; no pacman/uv/npx/cargo transaction; no host service touched;
no `~/.omp/agent/agent.db*` or credential file read.

## 6. Verdict

**Partial — routed defect 2 (usage attribution) holds with executed, deterministic proof; routed defect 1 (sibling-overlap scan) falls at c699c8c because its own credit gate is unmet; box-3/C2 falls at c699c8c: the ledger it names is absent and the committed `measure.py` returns calibration 6, not 8.**
