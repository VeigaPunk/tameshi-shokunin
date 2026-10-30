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

The substantive correction sections below preserve the original historical records and distinguish retrospective reruns from contemporaneous deciding executions.

## Gate

R51.6 — rejected candidates and reasons are recorded below alongside admitted entries; the Gate is not an admits-only list.

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
The eight collisions are S153–S160 (S156 collides, S165 does not). Both adopted documents receive continuation ids S286/S287; S288 is the new S285 supersession. These adopted ids collide with
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
| number-drift | The draft lesson incorrectly said staged S165 collided; `.ufo/waves/round-58/l1/assimilation/collisions` actually lists only S153–S160. | collision-census receipt review | Corrected the prose to the actual eight-id set before closing. The frozen spacing-tolerant intersection catches the deliberately indented S156 fixture; neither an absent collision nor a filename was inferred as evidence. |

## Wave record

(completed at the round's close: wave sizes, role mix, dead seats, results paths)

## R51.5 — cross-domain handoff to kagi

At kagi revision `c49023b773b69de983f0e6eb7e5867ceb5c2c634`, `corpus/drift-pins.sh` lines 400 and 403 use `grep -q "$3" <<< "$out"` to search expected verdict words as unanchored regular expressions. Line 158 prints `DRIFT   %s %s` with path text, which can contaminate such a word search; it is a diagnostic producer, not itself a grep.

Recommendation to kagi: anchor the intended verdict record and distinguish it from path-bearing diagnostics; preserve separate pass/fail assertions. No kagi file was edited. This handoff is included in the round-58 fleet report.

Evidence: `.ufo/waves/round-58/w1/T58W1Fix08/stage/kagi-crossdomain-r51.5.md` records the read-only source and revision commands.


## R53.2 and R53.4 — direct measurements and revision binding

R53.2: direct reruns at `88afa941545469457c78c7f4014bcda1afdee52c` now have committed carriers in `.ufo/evidence/round-53/after/`: `c1.stdout` prints `credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false`; `c2.stdout` prints `cr47=rc=2` and `total=0 C2_R53_PASS=true`. These are round-58 retrospective direct runs, not a claim that round 53 executed its deciding wrapper.

R53.4: the earlier `c2-counter-repaired.stdout` naming scratch revision `9c6ef7bc80c0` is superseded by `.ufo/evidence/round-53/after/c2.stdout`, whose `rev=88afa9415454` resolves in the lane and whose `cr47=rc=2` matches the declared could-not-evaluate class.

Invocation: extract each counter with `git show 88afa941545469457c78c7f4014bcda1afdee52c:.ufo/evidence/round-53/c1/measure.py` (or `c2/measure.py`), then `python3 -I COUNTER --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 88afa941545469457c78c7f4014bcda1afdee52c --work EMPTY_DIR --explain`. The c1 verdict appears before its per-heading PROBLEM details, not on the last stdout line.

## R55.1 — full C2 measurement at the certified revision

At measured revision `4c04c1d3`, the extracted frozen C2 counter prints `C2_R55: rev=4c04c1d3 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`. Full stdout is `.ufo/evidence/round-55/after/c2-full.stdout`; this round-58 rerun supersedes reliance on the truncated historical receipt without deleting that historical artifact.

Invocation: `git show 4c04c1d3:.ufo/evidence/round-55/c2/measure.py`, then `python3 -I COUNTER --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4c04c1d3 --work EMPTY_DIR --explain` (exit 0).


## R55.4 — control-completion record corrected

The earlier report sentence that `CTL_SKIP_c2` was still running at filing is superseded: `.ufo/evidence/round-55/control/controls-a.stdout` lines 5-6 already contain `CTL_SKIP_c2 ... total=4 C2_R55_PASS=false` and `CONTROLS_A: 5/5 as pre-registered`. This records completion, not an outstanding run.

Re-derivation: search `CTL_SKIP_c2|CONTROLS_A` in that committed receipt. Both lines exist at measured revision `4c04c1d3`, which predates the round-55 report.


## Wave-1 decisive falsifiers and corrections

- **C2 does not earn admission from its counter.** `T58W1RevengerC2` reproduced the round-56 failure one layer higher: a claimant-authored `tools/registry-check.py` prints forged held/differs lines without executing rows, and the frozen C2 counter accepts `held=3/3 mutants=3/3 total=0`. The real executor on the same fixture yields only `held=1/3`. Receipts: `.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/attack-b-out.txt` and its `attack.py`. The strict exact-element repair is real, but the frozen target fails the do-nothing discriminator. Neither target nor counter is weakened or repaired after this observation; a later numerical PASS will be reported without claiming C2 admission.
- **C3 rejected wording repaired.** `T58W1RevC3Gate` correctly rejected an overall equivalence rate being rewritten as equivalence conditional on survival, and two original sampled gates being presented as the entire lane population. The entry now distinguishes the overall rate from the conditional probability and names ten replay cases across JS/bash. This is a content correction, not a changed claim target.
- **R55.1 replay variation retained.** The L1's full counter rerun at `4c04c1d3` prints `usable=13/13 total=0`; `T58W1Fix05` independently prints `usable=12/13 total=1`, with the registry-check usable selftest failing. Both full receipts are retained. R55.1 is a missing-verdict-record repair, not proof of environment-invariant green behavior.
- **Cold-read forecast miss named.** R56.3's frontmatter link repair was not in the original per-file draft forecast. The measured content precheck still loses the same 17 headings (`content-precheck.stdout`); the reader set is not silently reduced.
- **Missing review credit remains missing.** W1's orchestrator handoff contains 67 seats but omits status/id fields. Fifteen seats have empty terminal outputs and no reports: the four scouts, five first critics, three mutation-testers, two sentinels and CritC3. No provider error text was supplied. They are not counted as successful reviews or fabricated as known deaths.

