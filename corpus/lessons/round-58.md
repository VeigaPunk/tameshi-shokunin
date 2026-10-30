# tameshi round 58 — lesson (hyaku run 11, 2026-10-30)

L1 `TameshiR58`, attempt 1. Base `2a32aa8228d5f86a85c81a923a3148bf792a9538`; contract
`.ufo/evidence/round-58/contract.json`; freeze `e2c2e654ff4c764d554810eabc849370052743d7`
(five commits 460684b4 → e2c2e654 in the declared order: defects/keys/panel stub, c1 counter,
c2 counter + mutants, shell instruments, contract+freeze manifest+SCORECARD planned).
Pre-freeze verification at the round-58 bytes: `C1_R58_SELFTEST: 110/110 pass` (exit 0),
`C2_R58_SELFTEST: 23/23 pass` (exit 0, includes strict cases P7/P8 landing round-57 critique
T57W3CritContract B2 before freeze). This file is completed from committed receipts at the
round's close.

## Claims

- **C1 (calibration)** — the routed-defect ledger gains one tree-supported row per item of the
  frozen 51-item set (routed items of the round 50–56 closure spot-checks); counter
  `.ufo/evidence/round-58/c1/measure.py` (round-57 arms A1–A9 re-pinned to base `2a32aa82`;
  blind round-58 panel `c1/panel.json`, PANEL_SHA256 set by amendment 1 from the wave-1 seats).
- **C2 (operability)** — the receipt-revision gate's registry rows hold under strict
  element-equality code binding; counter `.ufo/evidence/round-58/c2/measure.py`.
- **C3 (coverage)** — F9 (LLM-era mutant generation + equivalence) enters through
  `corpus/knowledge/llm-mutant-equivalence-cost.md` citing S286/S287; S288 supersedes S285's
  unreachable anchor. Stagnation-nudge frontier move.

## Corrections to earlier records

(to be completed from this round's corrections; append-only)

## Sources opened this round (Gate records)

Every row below was opened by this lane (L1 fetch) on 2026-10-30; fetch receipts and located
extracts are committed at `.ufo/waves/round-58/l1/sources/`.

| Row | URL and access date | Located quote (≤25 words) | Decision |
|---|---|---|---|
| S286 | https://arxiv.org/abs/2406.09843 — 2026-10-30, 44019 B HTML, sha256 `7af7e470fca3ef38…` | §Abstract (extract `arxiv-2406.09843-abstract.txt`): "the LLM-generated mutants have worse non-compilability, duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage points" | admit, mined: grounds the F9 survivor-counting contract; `used-by` → `corpus/knowledge/llm-mutant-equivalence-cost.md`. Lead-list conversion: the unopened lead at `corpus/SOURCES.md` (arXiv 2406.09843) moved to this row (old: lead bullet; new: row S286, status mined) |
| S287 | https://pdf.dfcfw.com/pdf/H3_AP202503221646031757_1.pdf — 2026-10-30, 5409054 B PDF, sha256 `531abe11d23f2e37…` | pdftotext extract line 241 (of `dfcfw-deck.txt`): "判断等价变异体是不可判定问题：不存在一个自动算法完美解决" | admit, mined: the equivalence class, its score-precision hazard (line 239) and its undecidability; `used-by` → the same entry |
| S288 | https://www.atlassian.com/incident-management/handbook/postmortems — 2026-10-30, live fetch 2310224 B, sha256 `0633b142efce0b08…` | markup-stripped (extract `atlassian-postmortems.txt`): "we understand and remediate the root cause of every incident with a severity of level 2 or higher" | new row, `teaches` opens "supersedes S285 —" (CORPUS rule 2): a reachable anchor replacing S285's absent >1 MiB snapshot; the rejection (vendor self-description, no measured outcomes) and the flip condition carry over unchanged; S285 untouched; status rejected |

Admits (assimilation set, §10 per-entry gates): ONE theme (F9 equivalence-cost counting
contract), ONE entry — `corpus/knowledge/llm-mutant-equivalence-cost.md` (staged
`merge/tameshi/knowledge/corpus/knowledge/llm-mutant-equivalence-cost.md`, staged ids S156/S165
re-pointed by document to S286/S287 after the id collision check; package text adapted before
landing: source headers re-written to this lane's fetch facts, ids re-pointed, boundary section
restated). PROVINCE scope check: survivor-counting method is verification-fixture craft
(in scope). QUALITY bar: provenance trio, falsifiable, boundary-honest. Expansion credit:
F9 held zero entries at base (`grep -rl 2406.09843 corpus/knowledge` at base → empty).

Rejects (assimilation set):

- **delta-debugging-minimization-contract (staged S167)** — REFUSED: ground already held.
  Round 50 admitted this exact entry from the same package (S271,
  `corpus/knowledge/delta-debugging-minimization-contract.md`; SCORECARD round-50 section,
  `corpus/README.md` F6 row). The round-53/54/55 "Planned" paragraphs still listed it as a
  candidate — see `## Mistakes` row 1. Flip: none needed (ground held); a successor candidate
  is any staged entry whose ground is not already held.
- **Considered and not taken this round**: the round-57 candidate `r8-predictive-test-selection-cost.md`
  (round-53 planned) — deferred on capacity; its theme (test-selection cost) is not among this
  round's claims and adopting two themes would dilute the §10 one-theme shape.

Id collision check (before any append; scratch receipt committed with the wave evidence):
reg-ids (lane registry, 0–3-leading-space pattern) vs staged-ids (`SOURCES.append.md`);
collisions listed S156, S165 among others by ID; adopted ids S286/S287/S288 collide with
nothing (next unused after S285). The 0–3-space guard was proven on an indented-collision
fixture (nonempty `collisions`) before any append.

Status/recheck/used-by changes (old→new, append-only log):

- S285: no cell changed (the correction is a new row, S288).
- Lead list: arXiv 2406.09843 lead bullet removed after S286 landed (old: unopened lead; new:
  row S286) — the S040–S046 precedent.
- No other row changed this round.

## Mistakes

| Class | Evidence | Captured-by | Fix and failability |
|---|---|---|---|
| stale-premise | The round-53/54/55 SCORECARD "Planned" paragraphs named the `delta-debugging-minimization-contract` package entry as an adoption candidate; round 50 had already admitted it from the same package (S271). Discovered 2026-10-30 when this round's C3 draft was being built: `ls corpus/knowledge | grep delta` at base → the entry exists, `source: S271`. | none — a planned-item candidate was never required to be swept against the corpus before adoption | Fix (this round): the adoption set was re-selected (F9 entry); the claim's before-state was re-derived at base by command (`grep -rl 2406.09843 corpus/knowledge` → empty at base), not from the planned text. Fix is shown able to fail: the same sweep at base against the delta-debugging paper URL finds the held entry (`grep -l 'delta-debugging.pdf' corpus/knowledge/*.md` → `corpus/knowledge/delta-debugging-minimization-contract.md`), so the guard (an adoption candidate whose subject URL is already cited is refused) has a red case it catches. Carried as a planned-item rule candidate for QUALITY.md |
| (in-round rows to be appended from wave findings) | | | |

## Wave record

(completed at the round's close: wave sizes, role mix, dead seats, results paths)
