# T48ScribeLessonCorrection — report

seat: `T48ScribeLessonCorrection` (w1, round 48, L1 TameshiR48)
date: 2026-10-26
base rev: `473336d9d789f6081195e7376d17836a24666bc3`
mode: read-only on the lane checkout; one deliverable written inside `.ufo/waves/round-48/w1/`

## Behavior

Drafted two append-only corrections for the round-48 lesson, each ready to paste and each grounded in files opened at this seat's run.

1. **C1-R48-1** — the round-47 dependence sets. `corpus/lessons/round-47.md:117-118` states `six-leg regression ledger` {fleet-root, node} and `hermetic env-differential probe` {env, node} as the round's "observed dependence sets". Those two sets are byte-identical to the **freeze-time** emission (`.ufo/evidence/round-47/before/c1-at-freeze.stdout:5,17`, also `control/emit-observed-pre-freeze.out:5,17`), printed with no receipt, revision or round named. The round-47 standing rows, which restate the content-revision emission, declare {env, fleet-root, node} (`SCORECARD.md:2270`) and {bwrap, node} (`SCORECARD.md:2276`). The deciding run at `8b0e15d2…` (`.ufo/evidence/round-47/after/c1.stdout:5,17`, exit 1) observed {fleet-root, node} and {bwrap, node} and scored the six-leg row `DEPS-MISMATCH`; its verdict is `total=2 … dep_mismatch=1 … C1_R47_PASS=false`. The correction states all three sets with their receipts, names the class (reference-drift + stale observation), and adds the rule: a dependence set is restated only from the deciding `--emit`, with that receipt's path and revision named.
2. **C1-R48-2** — the refusal of `r8-predictive-test-selection-cost.md`. The round-47 record cites `PROVINCE.md:14-18` as the refusal's ground (`corpus/lessons/round-47.md:81`; `.ufo/waves/round-47/w1/T47RevProvince.md:30`; §6.5 at `:428`). Those lines (quoted verbatim in the draft) refuse product domains, sibling gate code and credential/endpoint material — not test selection. The closure ruled the decisive reason is QUALITY 10/2 (`corpus/lessons/round-47-verifier-spotcheck.md:90`) and routed the citation fix (`:106`). The entry's `source:` cites `S205` / arXiv 1810.05286 and the lane has no such row: `grep -c '1810.05286' corpus/SOURCES.md` → `0`, and `S205` occurs `0` times in that file. The corrected row is written with the unopened-row reason as decisive, QUALITY 2 as second, `PROVINCE.md:14-18` withdrawn as the decisive cite (the §6.5 prose stands, never rewritten), and a two-part flip condition (an `S205` row opened `mined` in the writing round with a committed snapshot whose anchor the entry pins, **and** a named own-leg F7 move that consumes change-level selection).

Both blocks name the destination `corpus/lessons/round-48.md` (absent at this seat's run) and state that `corpus/lessons/round-47.md` is never rewritten (QUALITY criterion 4, `corpus/QUALITY.md:7`; routed item 3, `round-47-verifier-spotcheck.md:105`).

## Gates

- No counter was run — not `--selftest`, not `--only`/`--no-live`, not against a clone. This seat's item carries no measurement, and a verdict is the L1's. `.ufo/evidence/round-47/after/c1.stdout` was **read**, not re-executed; `after/c1.exit` (`1`) was read, not produced.
- Every quoted fragment was verified against its source file programmatically after the draft was written: 24/24 checks returned present (single-line quotes exact; the five wrapped quotes compared after collapsing whitespace runs). The QUALITY line citations were corrected during that pass (criterion 4 is `corpus/QUALITY.md:7`; criterion 2 is `:4-5`; criterion 10 is `:27-30`).
- Absence claims re-checked rather than trusted: `1810.05286` → 0 occurrences, `S205` → 0 occurrences in `corpus/SOURCES.md` (sha256 `bb8f0997b820b859…`).
- No network fetch; no source re-opened live (the package copy was read from the local read-only package tree).

## Commands run

| command | outcome |
|---|---|
| `read contract.json`, `read corpus/lessons/round-47.md:100-140` and `:112-122:raw` | contract and the two corrected lesson lines opened |
| `wc -l corpus/lessons/round-47.md`; `grep -n "dependence sets\|hermetic env-differential probe\|six-leg regression ledger"` | 119 lines; the two statements at 117-118 |
| `grep -n "six-leg regression ledger\|hermetic env-differential probe" SCORECARD.md`, `sed -n '2260,2272p;2305,2316p'` | standing rows at 2270 / 2276; disclosure at 2314; section head at 2262 |
| `cat .ufo/evidence/round-47/after/c1.stdout`; `sed -n '1,12p' … | cut -c1-400` | deciding verdict `total=2 … C1_R47_PASS=false`; six-leg at `:5`, hermetic at `:17` |
| `grep -rn "observed_deps=" .ufo/evidence/round-47/`; `sed -n '5p;17p' .ufo/evidence/round-47/before/c1-at-freeze.stdout` | freeze emission carries `{fleet-root,node}` and `{env,node}` — the lesson's two sets |
| `grep -rn "env,fleet-root,node" .ufo/waves/round-47/`; `sed -n '250,254p' .ufo/waves/round-47/w1/T47CritC1Control.md` | origin of the declared six-leg set: a wave-1 probe under load (`:253`) |
| `grep -n "r8-predictive\|cite the unopened-row\|Lesson correction" corpus/lessons/round-47-verifier-spotcheck.md` | defect 5 at `:25`; discernment ruling at `:90`; routed items 3-4 at `:105-106` |
| `sed -n '12,20p' PROVINCE.md`; `grep -c 1810.05286 corpus/SOURCES.md` | PROVINCE 14-18 are the domain/sibling/credential refusals; count 0 |
| `sed -n '1,4p' <package>/r8-predictive-test-selection-cost.md` | `source: S205 — https://arxiv.org/abs/1810.05286 …`, `verified-at: 2026-10-24`, `ground: F7` |
| `python3` (hash/quote checks) | 12 file sha256s; 24/24 quoted fragments located |

## Touched surfaces

| path | change |
|---|---|
| `.ufo/waves/round-48/w1/T48ScribeLessonCorrection.draft.md` | written (deliverable, 14861 B, sha256 `9346d959fffc9aae…`) |
| `.ufo/waves/round-48/w1/T48ScribeLessonCorrection.md` | written (this report) |

Nothing else in the lane was created, edited or deleted. `corpus/lessons/round-47.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `round-47-verifier-spotcheck.md`, `T47RevProvince.md`, `T47CritC1Control.md` and the round-47 evidence tree were read only. No git/jj command was run. No file was written under `/home/vgpnk/Projects/shokunin` (fleet), a sibling lane, or the package.

## Out of scope (left to their owners)

- Landing the blocks into `corpus/lessons/round-48.md` — the L1's append; the lesson does not exist yet.
- The round-47 C1 miss itself, the six-leg standing row's supersession and the R=3 counter — round-48 C1's subject, not a scribe's.
- The §6.5 prose, the classifier line and the package copy: corrected ahead of, never rewritten.
- The `S205` row: correcting the refusal does not open it; opening it is the flip condition.

## Findings

1. **The item's premise is confirmed, with one nuance worth recording.** The lesson's six-leg set {fleet-root, node} is not a stale set — it is the deciding run's *observed* set; its error is that it is offered as what the standing rows restate, where the declared set is {env, fleet-root, node}. The lesson's hermetic set {env, node} is genuinely stale: the deciding run observed {bwrap, node}. The draft states the two cases separately rather than calling both stale.
2. **The lesson's paragraph is defect-shaped, not wrong-at-the-source.** It sits under "at the freeze `total=22` (… `before/c1-at-freeze.stdout`)", so read only as the freeze state it is accurate; what is missing is the receipt pointer and the fact that the freeze sets are not the round's finding. The correction therefore adds a restatement rule instead of a retraction.
3. **The `PROVINCE.md:14-18` cite is off-target, and the closure said so before this seat.** `round-47-verifier-spotcheck.md:90` states the `PROVINCE.md:14-18` cite "is weak (those lines refuse product domains and sibling gates, not test selection)"; `:106` routes the citation fix. The corrected row keeps the refusal verdict and the flip condition, and moves the decisive weight to QUALITY 10/2, which is measurable: the cited row does not exist in the registry.
4. **No conflict to report for the canonical judge.** The three governing statements agree with each other and with the receipts: `round-47-verifier-spotcheck.md:25` (standing rows {env, fleet-root, node} / {bwrap, node}; deciding run {fleet-root, node} / {bwrap, node}), `SCORECARD.md:2270,2276` (the same declared sets), `.ufo/evidence/round-47/after/c1.stdout:5,17` (the same observed sets). The item's summary matches all three.
5. **Known limits.** The draft is a draft: nothing is appended, so no lesson row yet cites it; the two blocks are the only artifact, and the round-48 lesson's own Gate/refusal table may need the C1-R48-2 row to be re-flowed into whatever table shape the L1 adopts. `S205`'s live URL was not re-fetched (the package copy's local bytes were sufficient for the refusal citation); no claim in this seat rests on live network bytes.

## Tooling

No tool was installed, upgraded or removed; no `pacman` transaction was attempted; no model was passed.

## Scratch

No clone, work dir or temp file was created: `/fast/scratch/hyaku/tameshi-r48/T48ScribeLessonCorrection` does not exist (`ls` → "No such file or directory"), so there is no tree to delete. All reads and hashes ran against absolute paths in the lane and the read-only package.

## Artifacts

- deliverable: `tameshi-shokunin/.ufo/waves/round-48/w1/T48ScribeLessonCorrection.draft.md` (14861 B, sha256 `9346d959fffc9aae…`)
- report: `tameshi-shokunin/.ufo/waves/round-48/w1/T48ScribeLessonCorrection.md`
- read, not produced: `.ufo/evidence/round-47/after/c1.stdout` (sha256 `b56a8c2a861664046d6026a95dd452b00ec9331b00e5b523eeb9e0e0b6b37305`), `.ufo/evidence/round-47/after/c1.exit` (`1`), `.ufo/evidence/round-47/before/c1-at-freeze.stdout` (`27ca1e91cc61f08c…`), `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` (`1d70c44ed2edbc82…`)
