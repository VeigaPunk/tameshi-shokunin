# Planner data-walk — round 16 integration map (bounded supplement; L1 holds the planner seat)

Scope: map C1, C2, routed defects 1–2 and the frontier step onto **every** lane file that must
change at round end, with the protocol rule that requires each, an ordered integration checklist,
and the critical path. No lane file was edited; this is the only write (§Contract, Target).
Reader: L1 (TameshiR16). Baseline `git rev-parse HEAD` → `28aeef498cc070c3183271b709bc79d344ff547a`
(`git log --oneline -3` → `28aeef4` round-15 verifier spot-check, `9f2c86f` round-15 land,
`7650fe4` round-15 second-harness-failure preservation).

## Axes named

| Axis | Round-16 work | Required by |
|---|---|---|
| **depth** (6 → 7) | C1: seventh recorded mutation case `js-round-gate`, pre-registered from `arm-class-matrix.md` §13, embedded as a ledger leg | `AXES.md:25-42` (1–3 claims, distinct axes, one on the lowest non-retired axis); `AXES.md:75-83` (SCORECARD contract) |
| **calibration** (6 → 8) | C2: full-page cold-read earns the box-3 `[~]` assertion; four restrained marks become durable-evidence-linked | `AXES.md:43-55` (exploratory/`unprovable-but-better` path **not** used here — C2 is countable); `LEARNING.md:26-39`, `:40-45` |
| no-harm monitors | coverage / operability / freshness / adjacency | `AXES.md:33-35` ("no axis is harmed"); `LEARNING.md:37-39` |
| **frontier step** (not a claim) | S052 own-work row; one mistake mined; C1 filed as the sourced claim | `PROTOCOL.md:138-145` |

## Verified evidence (commands, exits, key lines)

| # | Command | Exit | Key line |
|---|---|---|---|
| E1 | `git show "$REV:tools/mutate-and-run.sh" \| python3 -c …` (SCORECARD command D, `SCORECARD.md:73`) at `28aeef4` | 0 | `recorded_cases=6 depth_score=6` → C1's before is exact |
| E2 | `git show "$REV:SHONEN.md" \| python3 -c …` (command C, `SCORECARD.md:75`) | 0 | `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8` — the 6→8 headroom is the excluded box 3, nothing else |
| E3 | `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md` | 0 | `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` — matches C2's declared snapshot |
| E4 | fence-aware heading scan of the snapshot (stub below) | 0 | `fence-aware sections: 50`, `raw ^#{1,3} count: 54`; the 4 extras are shell-comment pseudo-headings inside code fences at snapshot `:549,552,618,621` |
| E5 | `git -C kumitate-shokunin cat-file -e 364f1d59…` then `git show 364f1d5:scripts/round-gate.mjs \| sha256sum` / `wc -l` / `grep -c "check('"` | 0 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`, `1511`, `60` — **the rev resolves and the blob is byte-identical to §13's projection pin** (`arm-class-matrix.md:298`, pin `f890e277…a834d3e9`) |
| E6 | `cat .ufo/evidence/round-16/census-start.txt` | 0 | 2 W04 rows (`S047`, `S048` duplicate PIT URL) + `tameshi ok …`, `exit=0`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `49` |
| E7 | `grep -n 'six…' SKILL.md corpus/knowledge/*.md corpus/README.md` | 0 | live present-tense six-count sites at `SKILL.md:1010,1092,1136,1152,1285,1339,1426,1555,1689`, `corpus/knowledge/repeated-control-precondition.md:54,79,80`, `fleet-kill-rate-ledger.md:109,285`, `incremental-pin-disposition.md:153,190`, `operator-runbook.md:145,374` |
| E8 | `python3 -` over `.ufo/evidence/round-15/verification-3.json` | 0 | `runner: .ufo/evidence/round-15/verify.py`; `checks[11]` = `integrity-tools/mutate-and-run.sh` `baseline sha256=75ed934d… rev sha256=75ed934d…`; `checks[12]` pins `SHONEN.md` `3b1dc526…`; `checks[13]` pins `corpus/lessons/round-14-verifier-spotcheck.md` `d267576a…` |
| E9 | `grep -n` on `tools/mutate-and-run.sh` | 0 | structure anchor set: ledger `:84-89`; provenance note `:93-97`; usage text `:195-197`; constants `:542-553`; tables `:554-559`; embedded specs `:589-888`; embedded-spec `-s` check `:889-891`; `REGRESSION_EXPECT` `:1103-1109`; leg calls `:1111-1141`; `nlegs=6` `:1143-1144`; selftest "six files" `:1576` |
| E10 | `grep -n` on spotcheck | 0 | routed defect 1 `corpus/lessons/round-15-verifier-spotcheck.md:159`; defect 2 `:160`; residual 5 `:163`; quota accounting `:26-40` |
| E11 | `grep -n` on PROVINCE / QUALITY / README / SCORECARD tails | 0 | `PROVINCE.md:28-38` Core lists **six** legs; `:40-42` Core-admission gate; `QUALITY.md:77-84` criterion 17, append point EOF `:85`; `corpus/README.md:61` coverage table end, `:217` EOF; `SCORECARD.md:551` EOF; `LOG.md:1022` EOF |

All counts carry their command (`CORPUS.md:27-31`). No installs or upgrades were made in this walk.

## Mapping — declared item → every lane file that must change

Row legend: **F** = file, **A** = anchor/insert point at baseline, **C** = required change,
**R** = the rule that requires it.

### C1 — depth 6 → 7 (`js-round-gate` ledger leg)

| # | F | A | C | R |
|---|---|---|---|---|
| C1.1 | `tools/mutate-and-run.sh` | `:84-89` | add `#   js-round-gate          kumitate-shokunin/scripts/round-gate.mjs   <k>/10 (<p> %)`; shape must satisfy the command-D regex `^#   (?:js\|bash)-\S+\s+\S+\s+\d+/\d+` | `SCORECARD.md:73` (D is the depth counter); `CORPUS.md:27-31` |
| C1.2 | same | `:14`, `:80`, `:93-97`, `:195-197`, `:535-537` | six → seven in the mode header, provenance note and usage text | `AXES.md:14` (re-verification recorded, not silently left) |
| C1.3 | same | `:542-553` | `PIN_ROUNDGATE=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`, `REV_ROUNDGATE=364f1d5954158ef8844bca4a5fef57b05d2f2ca5` | `PROTOCOL.md:138` (frontier step) not applicable; this is the leg's pin contract, `tools/mutate-and-run.sh:80-108` |
| C1.4 | same | `:554-559` | `TABLE_ROUNDGATE='…'` — the **recorded** 10-row verdict table from the executed sweep, not the predicted one | `CORPUS.md:112` (row is a claim, written after opening); `QUALITY.md:15-17` (prediction carries executed outcome) |
| C1.5 | same | `:589-888` | embedded `js-round-gate.spec` with 10 `@defect` blocks; every `@old` must occur exactly once in the pinned blob (spec v1: `§Interfaces`) | `tools/mutate-and-run.sh:61-66` (fail-closed count==1 before any suite run) |
| C1.6 | same | `:889-891` | extend the `[[ -s … ]]` embedded-spec assertion to the seventh file | **vacuity guard** — without it the leg is not self-test-covered (see R3) |
| C1.7 | same | `:1103-1109` | `REGRESSION_EXPECT` gains the seventh pair | `tools/mutate-and-run.sh:109-117` (stated expectation) |
| C1.8 | same | `:1111-1144` | seventh `regression_case_git` call, seventh status var, `nlegs=6`→`7`, status list | same |
| C1.9 | same | `:1576` | `st 'embedded leg specs: six files written'` → seven | same as C1.6 |
| C1.10 | `corpus/SOURCES.md` | registry end of `## Registry` (S051 row) | new `S052` row: `own-work`, tier `A`, scope = kumitate `scripts/round-gate.mjs` pinned bytes, anchor = rev `364f1d5` + blob sha256 + `1511` lines + `60` checks, `status=mined`, `opened=2026-10-20`, `recheck=on-release`, `used-by=corpus/knowledge/mutation-case-round-gate.md`; update `## Id allocation` "Next unused id: S052" → `S053` | `CORPUS.md:112-120` (row opened in the round that writes it; append-only; only `status`/`recheck`/`used-by` change in place); `CORPUS.md:163-170` (external source cites its `S###` row) |
| C1.11 | `corpus/knowledge/mutation-case-round-gate.md` **(new)** | — | provenance trio first (`source:`, `verified-at:`, `recheck:`); then: pre-registered predictions table (mutant → §13 anchor → predicted verdict), executed outcomes, survivor classes, runner pin at the measured revision, and the **denominator table** (see R1/proposal) | `CORPUS.md:163-170`; `QUALITY.md:18-20` (coverage-map row same round) |
| C1.12 | `corpus/knowledge/fleet-kill-rate-ledger.md` | `:109` (§3 queue row `round-gate \| 60 \| f890e277af83a78f \| unmeasured; hermetic`) | append a new section (e.g. `## 8. Round 16 — the seventh case (append-only)`) that discharges that queue row: measured 60-case suite, pin, kill table, survivor classes. **Do not rewrite the §3 table** | `CORPUS.md:46-48` (index row is a claim; corrections are new entries); file's own appended-block convention (`:285`, ER-3 carries `appended 2026-10-14`) |
| C1.13 | `corpus/knowledge/repeated-control-precondition.md` | `:54` pins runner `75ed934d…` + "six recorded legs at `:84-89`" | append errata naming the new runner sha256 and 6→7 legs — **written after the runner's final edit** (see checklist gate G4) | `CORPUS.md:179-184` (a fix/claim ships its red-before and is not left stale); `AXES.md:14` (drift flagged or fixed) |
| C1.14 | `corpus/README.md` | rows end `:61` | coverage-map addendum row for the new knowledge note (one line: what it holds, `S052`) | `QUALITY.md:18-20` (criterion 7: landed in the same round) |
| C1.15 | `PROVINCE.md` | `:28-38` Core says "the six recorded mutation legs' gates" | append a Core correction block: seven legs, new read-only surface `kumitate scripts/round-gate.mjs` @ blob `f890e277…`; leave `:1-20` untouched (file's own append convention `:24-26`) | `PROVINCE.md:40-42` — Core moves only through an admitted, source-headed `knowledge/` entry whose `source:` cites a **mined** row ⇒ **hard ordering edge after C1.10/C1.11** |
| C1.16 | `SKILL.md` | append after `:1704` (EOF of the round-15 section; `wc -l SKILL.md` → 1704) | new `## A seventh measured case — kumitate \`round-gate\` (round 16, measured)` with: 10-row predict→observe decision table; survivor classes; the projection-transfer rule (byte-identical blob ⇒ §13 prediction valid — E5); the **seven-case denominator** statement superseding `:1092`'s six-case confidence sentence; and an explicit "no new registry row" paragraph | `LEARNING.md:16-21` (fold durable understanding into SKILL.md: decision tables/checklists); `AXES.md:11` (depth = decision tables with real thresholds) |
| C1.17 | `SCORECARD.md` | append after `:551` | `## Round 16 — measured claims` with the C1 row (depth 6→7), the counting command (`python3 .ufo/evidence/round-16/measure.py --rev REV` printing `recorded_cases=7 depth_score=7`), the measured hash, the no-harm table, trends, next intended claim | `AXES.md:75-83`; `LEARNING.md:26-39`; rounds 12–15 precedent (`SCORECARD.md:284,334,399,483`) |
| C1.18 | `.ufo/evidence/round-16/` | — | `prereg.json` (predictions, committed **before** the sweep), `sweep/` workdir logs + `results.tsv` + `spec.copy`, `selftest.txt`, `regression-7leg.txt`, `measure.py` + `before.json`/`after.json` | `QUALITY.md:24-26` (criterion 9: evidence copied into the repo before the commit that cites it) |
| C1.19 | `LOG.md` | append after `:1022` | `## Round 16 — …` entry: claim, before→after, commands/exits, the runner-pin drift disclosure (R2), sources/limits; append-only | `PROTOCOL.md:463`; `PROTOCOL.md:154` (each landed change tied to a LOG entry) |

### C2 — calibration 6 → 8 (full-page cold-read)

| # | F | A | C | R |
|---|---|---|---|---|
| C2.1 | `.ufo/evidence/round-16/coldread/SKILL.snapshot.md` | staged `A` at write time | commit as the read authority (sha E3) | `QUALITY.md:24-26`; `PROTOCOL.md:156-159` (rows/evidence the report cites) |
| C2.2 | `.ufo/evidence/round-16/coldread/ledger.json` | — | L1-assembled per the `§Interfaces` schema: exactly **50** entries (E4), `start` = snapshot line, `sha256` = heading-line-through-preceding-line joined `\n`; `seats[]`/`reports[]`; one entry per seat-JSON block | `§Interfaces` ledger schema; `CORPUS.md:27-31` (count carries its command) |
| C2.3 | per-seat `.json` blocks | ends of the CR seat reports | validate every block: one fenced ```json, `skill_sha256` = E3, `sections` non-empty, `opened[]` populated | `§Interfaces` cold-read block; contamination rule |
| C2.4 | `SHONEN.md` | `:9-10` (box 3) | replace only the **evidence pointer inside the box-3 bracket**; keep the canonical box wording and keep `[~]` | `PROTOCOL.md:59-77` (only a non-author `<id>` may write `[x]`; a lane-dispatched subagent is still the lane); `QUALITY.md:43-46` (criterion 13); see D2 |
| C2.5 | `SCORECARD.md` | same round-16 section | C2 row: calibration 6→8, counted by a `measure.py` that prints `2 × (restrained boxes with resolvable durable pointer) = 8`; command C output (E2) recorded as the mark census, explicitly **not** the score by itself (`SCORECARD.md:74` says the bound awards no credit) | `AXES.md:79` (score + evidence pointer + last-change round); `CORPUS.md:27-31` |
| C2.6 | `corpus/README.md` | append after `:217` | `## Round 16` block: full-page cold-read executed; **name the superseded sentences** `:142-146`, `:160`, `:188-193`, `:205-209` ("full-page box-3 remains open") | append-only convention of that file (round blocks `:123,:148,:180,:195`) |
| C2.7 | `corpus/lessons/round-16.md` | new | `## Gate` (candidates/admitted/rejected with reasons + spot-check result) records the cold-read's admit/reject sample and the ledger verdict counts | `CORPUS.md:19-21`; `LEARNING.md:69-71` |
| C2.8 | `corpus/QUALITY.md` | append after `:85` | `## Criteria appended — round 16`, one criterion grounded in the round's outside-routed defect (R5/D4) | `LEARNING.md:20-22` (a mistake no criterion caught adds a criterion citing the lesson); `CORPUS.md:171-179` |
| C2.9 | `.ufo/evidence/round-16/coldread/repair-*.json` | if any gap-blocking | repairs are their own receipt: pre-repair section sha, post-repair sha, the re-read verdict — never rewritten into the wave-1 entries | `PROTOCOL.md:123-137` (append corrections, never rewrite the filed record) |

### Routed defect 1 — credited sibling-overlap connector scan

| # | F | A | C | R |
|---|---|---|---|---|
| D1.1 | `.ufo/waves/round-16/w1/Overlap*.md` | — | a **credit-eligible** scan: method, sibling inventory opened, overlap findings with `path:line`, per-finding owner lane, and a coverage statement — not a partial | `corpus/lessons/round-15-verifier-spotcheck.md:159` (defect 1: "a partial SiblingOverlap report is not the required successful scan"); `PROTOCOL.md:240-243` (step 2: route, do not absorb) |
| D1.2 | `corpus/lessons/round-16.md` | `## Mistakes` | row: class `attribution` · evidence `round-15-verifier-spotcheck.md:36-40,159` · captured-by `none` (or the new criterion if D4 adds one) · fix = credited scan this round + report accounting | `CORPUS.md:171-178` (class vocabulary: `vacuous, survivor, stale-premise, reference-drift, number-drift, scope, attribution, landing, provider`) |
| D1.3 | round report (`.ufo/reports/round-16/tameshi.md`, main repo — L1's write) | — | name the scan credited; do **not** relabel round 15's `56/66` completed | `PROTOCOL.md:146-168` (report minimum content); spotcheck `:159` |
| D1.4 | `PROVINCE.md` | `:44-47` Adjacent | if the scan finds contested scope, it is **reported**, never absorbed; no PROVINCE Core addition from overlap findings | `PROVINCE.md:44-47`; `AXES.md:16` (adjacency) |

### Routed defect 2 — usage-finding attribution repair (append-only)

| # | F | A | C | R |
|---|---|---|---|---|
| D2.1 | `.ufo/evidence/round-16/usage-attribution.py` **(new)** | — | corrected extractor: read the **terminal structured verdict** (`id=<token>` on the last non-empty line / stderr token), not the first help-text match (`verify.py:197-213` is the defect) | `corpus/lessons/round-15-verifier-spotcheck.md:160` |
| D2.2 | `.ufo/evidence/round-16/usage-attribution.json` | — | red-before / corrected-after on the **same fixture and argv**: old parse yields a help-text `observed_id` for `gate-usage` and `usage-proof-new` (verify.py `:552,:558`); corrected parse yields `usage_error` | `CORPUS.md:179-184` ("a fix is shown able to fail before it counts") |
| D2.3 | `.ufo/evidence/round-15/verification-3.json` | — | **MUST NOT be edited** | spotcheck `:160`; `QUALITY.md:7` (errata append-only) |
| D2.4 | `.ufo/evidence/round-15/verify.py` | — | if its bytes change at all, retain the pre-repair copy under round-16 evidence and disclose the runner-byte move; `verification-3.json`'s `runner` field names this path | `PROTOCOL.md:123-137` |
| D2.5 | `corpus/lessons/round-16.md` + `corpus/QUALITY.md` | `## Gate` / `## Mistakes`; `:85` | lesson row (class `reference-drift` or `attribution`) and one criterion: a verdict-attribution parser reads the terminal structured verdict and ships both parses on one argv | `LEARNING.md:20-22`; `CORPUS.md:171-179` |

### Frontier step (every round, not a claim)

| # | F | A | C | R |
|---|---|---|---|---|
| F1.1 | `corpus/SOURCES.md` | registry + id allocation | S052 opened/mined (C1.10); census before→after 49→50, A42→43, mined22→23, W04 `S047`/`S048` unchanged | `PROTOCOL.md:138-145`; `CORPUS.md:63-160` (contract v1 + census commands) |
| F1.2 | `corpus/lessons/round-16.md` | `## Mistakes` | ≥1 own mistake mined, or the sweep that found none pasted | `PROTOCOL.md:139-141` |
| F1.3 | C1's evidence | — | one claim filed as *sourced*: C1 cites `S052` | `PROTOCOL.md:141-142` |
| F1.4 | `corpus/README.md` `## Frontier` (`:68-87`) | append-only status correction after `:121` | state which F-row advanced; the honest default is **none** (same-ground case; `F8` oracle anchoring remains open unless a survivor is classified against an independently anchored expectation, which would need its own source-headed entry) | `LEARNING.md:73-80`; `PROVINCE.md:40-42` |
| F1.5 | round report | `## Sources & frontier` | rows before→after with the counting command, rows added by tier, rows touched old→new, frontier rows advanced | `PROTOCOL.md:156-159` |

## Ordered integration checklist

Gate notation: **[G#]** = a check that must pass before the next phase. Commit boundaries are
*suggested*; the hard edges are marked ⚠.

**Phase 0 — freeze the read authorities (no code change).**
1. Commit the cold-read snapshot + `census-start.txt` + the wave-1 seat JSONs. Evidence must exist
   before the commit that cites it (`QUALITY.md:24-26`).
2. Validate the seat JSON corpus: exactly one fenced ```json per CR seat, `skill_sha256` = E3.
   **[G1]** `50` fence-aware sections covered; per-section `sha256` reproducible from the snapshot.
3. Commit `prereg.json` (10 mutants: id, `@old`, `@new`, predicted verdict, §13 anchor line,
   discriminator). ⚠ **Preregistration must be a commit that precedes every mutant run** — C1's
   blindness claim is only as strong as that ordering (`QUALITY.md:15-17`; `CORPUS.md:112`).
   **[G2]** `git log` shows the prereg commit strictly before the sweep's evidence timestamp.

**Phase 1 — C1 sweep (L1 only, wave 2).**
4. Run the 10 mutants through `tools/mutate-and-run.sh` against the pinned blob (fresh `/tmp`
   copies; sibling tree read-only). Retain `results.tsv`, `spec.copy`, control + per-defect logs.
   **[G3]** control GREEN, `MUTATE_RESTORE: OK`, every run enumerates the same suite count.
5. Record outcomes vs predictions; every miss is an errata row naming the discriminator
   (`QUALITY.md:15-17`).

**Phase 2 — embed the leg (the only lane-code change in C1).**
6. Apply C1.1–C1.9 to `tools/mutate-and-run.sh` in one commit.
7. `bash tools/mutate-and-run.sh --selftest` and `--regression`.
   ⚠ **[G4] The runner's bytes are now final.** The `--selftest` embedded-spec assertion must cover
   the seventh file (C1.6/C1.9) — otherwise the leg is self-test-blind (R3).
   ⚠ **[G5]** `--regression` → `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: …)`.
8. Only now: write C1.13 (runner-pin errata) with the **final** sha256, and run command D at the
   working tree. **[G6]** `recorded_cases=7 depth_score=7`.

**Phase 3 — admit the case (source → knowledge → coverage → province).**
9. C1.10 `S052` + C1.11 knowledge note + C1.14 coverage row + C1.12 ledger §8 — one commit.
   ⚠ **[G7]** `bash scripts/sources-census.sh validate --root … tameshi` (fleet script) → exit0,
   `49→50` rows, no malformed rows, `S052` unique, `used-by` path exists, W04 unchanged.
   **[G8]** the new note opens with the provenance trio and its `source:` names `S052`.
10. C1.15 PROVINCE Core append — only after G8 (`PROVINCE.md:40-42`).

**Phase 4 — C2 integration (parallel with 1–3 where possible).**
11. Assemble `ledger.json` (C2.2); triage `blocking_gaps` → `wrong_expectations` → `minor_gaps`.
    ⚠ If any blocking gap requires a SKILL repair: repair, snapshot the repaired file, re-read the
    affected sections in wave 2, and record repair receipts (C2.9). **Do not mix** wave-1 `start`
    coordinates with post-repair hashes (R2).
    **[G9]** Ledger total = 50; Σ verdicts = 50; every `reports[]` path exists; every seat count in
    `seats[]` matches the committed seat files.
12. C2.4 SHONEN pointer, C2.5 SCORECARD calibration row. **[G10]** command C at the measured rev
    prints `asserted_mark_upper_bound=8` **and** `measure.py` prints `8` from the four durable
    pointers (D2: never `[x]`).

**Phase 5 — routed defects.**
13. D1.1–D1.2 (credited scan + Mistakes row); D1.3 accounting in the report.
14. D2.1–D2.5 (attribution repair receipts + criterion). **[G11]** red-before diverges from
    corrected on the same argv; `verification-3.json` byte-identical to `7650fe4:…` (sha compare).

**Phase 6 — synthesize.**
15. C1.16 SKILL section (includes the seven-case denominator + "no registry row" statement).
16. C2.6 README round block; F1.4 Frontier status correction; C2.7/F1.2 lesson (`## Gate` +
    `## Mistakes`); C2.8 QUALITY criterion.
17. C1.17 SCORECARD round-16 section: two claim rows, the no-harm table, trends, the runner-pin
    drift disclosure (R2), the capability decision (D1), next intended claim.
18. C1.19 LOG entry. **[G12]** `git status --porcelain` clean; every evidence path cited exists at
    HEAD (`git cat-file -e`); append-only files grew, never rewrote (`git diff --stat` shows 0
    deletions in `LOG.md`, `SHONEN.md:9-10` only, `PROVINCE.md` append-only).
19. Final re-run at the delivered commit: `--selftest`, `--regression`, command D, command C,
    `measure.py --rev HEAD`. A post-verification edit needs its own proof (rounds 12–15 precedent:
    `SCORECARD.md:296-297`, `:415-422`).
20. Lane report `.ufo/reports/round-16/tameshi.md` (main repo) **last**: work + evidence + commit
    hash, `## Sources & frontier`, a `SHONEN` heading with one line per box — `[~]` throughout.
    ⚠ Report after the lane commits; the hash it cites must be an ancestor of `HEAD`
    (`PROTOCOL.md:117-122`).

## Critical path

Two chains, joining at the SCORECARD + report:

```
CHAIN A (C1, 8 serial steps, longest)
  prereg commit [G2] → sweep [G3] → runner edit → selftest [G4] → regression 7 legs [G5]
  → command D = 7 [G6] → S052+knowledge+coverage+census [G7,G8] → PROVINCE Core
  → SKILL §round-16 → SCORECARD depth row → final re-run → report

CHAIN B (C2)
  one JSON block per CR seat (wave 1, parallel; roster shows `CR01`–`CR23` and others) → [G1] ledger assembly → gap triage
  → (repair → repaired snapshot → wave-2 re-read)* → SHONEN pointer → [G10] calibration row

JOIN: SCORECARD §round-16 → LOG → report (lands last)
```

Longest path is **A**; B is parallel except for the ledger-assembly gate and any repair cycle.
The two hard edges no ordering may violate:
- ⚠ **prereg commit < first mutant run** (C1's calibration claim depends on it).
- ⚠ **runner final bytes < C1.13 pin errata and < command D** (a pin written against a
  not-yet-final tool is a false record; `CORPUS.md:179-184`).

## Contradictions and risks (stated, not smoothed)

- **R1 — the seventh case falsifies ten live "six" statements.** E7 lists them. `fleet-kill-rate-ledger.md:109`
  is not merely prose: it is the standing queue row that says `round-gate` is *unmeasured* — the
  exact opposite of C1. `repeated-control-precondition.md:54` machine-pins the runner sha and leg
  count. If the round lands the leg and only writes the new note, the next outside reviewer
  re-derives a false present tense and records `quality: harmed` (`LEARNING.md:33-39`). The round
  must therefore resolve every **present-tense** site (append-only) and mark the historically-scoped
  ones as such. This is in the checklist (C1.12, C1.13, C1.16) but is the item most likely to be
  dropped under schedule pressure.
- **R2 — C1's runner edit drifts round-15's retained integrity pin.** `verification-3.json`
  `checks[11]` pins `tools/mutate-and-run.sh` at `75ed934d…` for both baseline and revision (E8).
  After C1 the file's bytes differ, so nobody may claim "round-15 verification still green at HEAD";
  the receipt stays valid for its own revision. Disclose in the LOG entry and the round-16
  SCORECARD block. Same for `SHONEN.md` (`checks[12]` pins `3b1dc526…`) — C2.4 changes exactly the
  box-3 pointer, which is a real byte move inside a pinned file; it is honest, but it is a move and
  must be named.
- **R3 — self-test vacuity for the new leg.** The embedded-spec assertion (`:889-891`) and its
  label (`:1576`) enumerate six files. Adding a seventh spec without extending them leaves the
  check passing while blind to the new leg — precisely the "reported-but-unasserted" survivor class
  this lane studies. Fix both (C1.6/C1.9) or the round ships its own class instance.
- **R4 — `[x]` on SHONEN box 3 would cost two points and violate the gate.** PROTOCOL allows `[x]`
  only from a non-author (`PROTOCOL.md:59-77`); a lane subagent is still the lane. And command C
  counts `~`, not `x`: flipping box 3 to `[x]` takes `checked` to 1 and `asserted` to 3, printing
  `asserted_mark_upper_bound=6` — the score would *fall* to 6. Keep `[~]` (D2).
- **R5 — ledger schema ambiguities that will silently disagree across seats.** (i) Section `sha256`
  boundary at EOF: trimming trailing blank lines gives preamble `0ffdbd947a5a881d…` (4 lines) while
  the strict reading gives `955cabcd17dfc192…` (5 lines). Pick one rule and record it in the ledger
  README. (ii) `start` is defined against the **snapshot**; after any SKILL repair those coordinates
  are stale for new bytes — re-reads need their own snapshot hash, never a mixed file. (iii) 54 raw
  `^#{1,3}` hits vs 50 sections (E4) — the four pseudo-headings at snapshot `:549,552,618,621` must
  not become entries. Anchor hashes for assembler validation under the trim rule:
  preamble `0ffdbd947a5a881d345acd4ad86192701ae9e40de6be327f780c7808cfbbf661`,
  `## Source notes` (30–57) `293fd76b1cb91cca7ba664f59c2ff2872cd9cb7c162b0f19796b52b37eda38b1`,
  `### Round-15 gate/probe registry` (1676–1704; the 1705th split element is the final newline) `7544ca6940553ecd2adca2d1d9d6571b4a55f0ad191013507ff4d7bd14b32dde`.
- **R6 — capability table**. D1: appending `seven-leg regression ledger` is legitimate only with the
  `REGRESSION: PASS (cases=7 …)` output in the round report (`AXES.md:57-65`). A name-only edit of
  the existing `six-leg regression ledger` row would rewrite a historical evidence pointer — avoid.
- **R7 — C2's snapshot is already staged (`A`).** If the round ends with it uncommitted, the box-3
  evidence is not durable (`PROTOCOL.md:117-122` "landed means committed").

## Proposed move (one, bounded)

**Make the denominator supersession a receipt, not a sentence.** Commit
`.ufo/evidence/round-16/six-count-census.txt` produced by one reproducible command that lists every
present-tense "six <cases|legs|recorded>" site across `SKILL.md`, `corpus/knowledge/*.md`,
`corpus/README.md` with `file:line`, each classified `historical | superseded | live`; resolve every
`live` row in the same round by one append-only block (`fleet-kill-rate-ledger.md` §8,
`repeated-control-precondition.md` errata, the new SKILL §round-16 denominator sentence); cite the
receipt's before→after count in the round-16 no-harm table.

- **Affected axes:** freshness (protected from a self-inflicted stale pin), depth (the seventh case's
  denominator becomes explicit), calibration (no scalar change; a falsifiable check replaces a prose
  promise).
- **Why not the alternatives:** editing each old file in place rewrites historical claims (forbidden
  by `CORPUS.md:46-48` and the append-only corrections rule); doing nothing leaves R1's false
  present tense; a free-floating "see round 16" note has no count and no command.
- **Risks:** scope creep into a fleet-wide grep. Bound it to the lane root, present tense only,
  with the historical-scoped ones explicitly marked and not edited.
- **Verification:** the census command must exit0 and print the same `live` set at the delivered
  commit after the supersessions land (i.e. `live=0`); the receipt plus `git diff --stat` showing
  0 deletions in the superseded files is the proof.

## Verification commands the main agent / L1 should run after integration

```sh
# C1 depth: recorded ledger legs = 7 at the delivered revision
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
# C2 calibration: mark census (upper bound) and the durable-pointer score
git show "$REV:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" bound="+str(min(8,2*m.count("~"))))'
python3 .ufo/evidence/round-16/measure.py --rev "$REV"
# the runner's own gates, on the delivered bytes
bash tools/mutate-and-run.sh --selftest   # expect MUTATE_SELFTEST: n/n pass, exit0
bash tools/mutate-and-run.sh --regression # expect REGRESSION: PASS (cases=7 passed=7 ...)
# sources census against the contract
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
# ledger shape
python3 - <<'EOF'
import json; d=json.load(open('.ufo/evidence/round-16/coldread/ledger.json'))
print(d['schema'], len(d['entries']), sorted({e['skill_sha256'] for e in d['entries']}))
EOF
```

## Bounds

No files outside this report were written; no sibling tree, `MANIFEST.json`, fleet script or
`.ufo/state/` was touched; no mutants, builds or suite runs were executed in this walk (wave-1 leaf
rule). Tool installs/upgrades: none.
