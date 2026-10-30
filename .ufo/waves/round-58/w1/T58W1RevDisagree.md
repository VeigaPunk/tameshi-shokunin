# T58W1RevDisagree — disagreement budget plan

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Axes: calibration truth, committed-evidence strength, disagreement economy. Recommendation only; no admission or integration performed.

## Findings, severity first

**HIGH — do not budget against the wrong panel.** `.ufo/evidence/round-58/c1/measure.py:450-466` compares each row's `status_at_base` against the **new round-58** pinned panel, not the old round-57 panel. `PANEL_ALLOWED = 5` at line 115 is a tolerance for that comparison. Therefore the seven historical candidates below do not automatically spend seven disagreements. Never knowingly describe a resolved item as open merely to fit five. The new panel may independently recognize all five strongest repairs.

**MEDIUM — R56.3 is not literally complete.** The new superseding errata gives 19/19 and the README indexes it, but `corpus/knowledge/receipt-revision-binding.md:3` still gives 14/14 without pointing to the errata. The item expressly asks for a superseding entry or errata the recheck line points to. This is the weakest arguably-fixed claim.

**MEDIUM — R56.2 contains two obligations.** `SKILL.md:53` now correctly gives CONTENT_DRIFT with paths, but the requested docs-arm code-to-role-truth discriminator is not established by that cell correction. Do not infer full closure from presence of the code. Keep open at base pending evidence for the conjunctive arm.

## Ranked old-open / potentially fixed-at-new-base items

All seven were `open` in `.ufo/evidence/round-57/c1/panel.json`. Provenance comes from immutable `git show BASE:path` plus `git blame --line-porcelain -L RANGE BASE -- path`, with the exact commands, exits and full outputs saved in `T58W1RevDisagree-receipts/commands.json`.

| Rank | Item | Recommendation | Committed evidence at base |
|---|---|---|---|
| 1 | R56.4 | Prioritize if a disagreement is needed | `.ufo/evidence/round-57/coldread-referent-r56.md:1-13`, `ca75c2674645ab6bdadeecb8584007c74342bfa9`. Explicit referent recorded, with exact source/quality hashes independently reproduced for 877eedee; item expressly allows recording rather than rebinding. |
| 2 | R55.2 | Prioritize if a disagreement is needed | `corpus/lessons/round-57.md:19-26`, `adf87899c70d616140a81185a8f9acbbdfb30392`. Superseding correction identifies the 9-mode total=1 false result and distinguishes earlier 8-mode total=0; directly answers the quotation defect. |
| 3 | R56.7 | Prioritize if a disagreement is needed | `corpus/lessons/round-57.md:27-36`, `adf87899c70d616140a81185a8f9acbbdfb30392`. Supersedes no-byte-change claim with exact C0-to-bind and bind-to-base intervals; explicitly states the changed files. |
| 4 | R53.8 | Prioritize if a disagreement is needed | `corpus/lessons/round-57.md:12-18`, `ca75c2674645ab6bdadeecb8584007c74342bfa9`. New correction supplies 20/20 word counts; physical p.3 locator already present at old base in SOURCES.md and change-aware-resweep-cadence.md. |
| 5 | R56.6 | Prioritize if a disagreement is needed | `tools/registry.json:1309-1390`, `ca75c2674645ab6bdadeecb8584007c74342bfa9`. Three gate-kind registry rows encode exits 0,3,2 and SKILL registry describes map. Bare code elements remain absent: distinct round-58 C2 repair still owed. |
| 6 | R56.3 | Keep open: unmet literal clause | `corpus/knowledge/receipt-revision-binding.md:247-262`, `ca75c2674645ab6bdadeecb8584007c74342bfa9`. Superseding 19/19 errata and README index exist, but original recheck line still says 14/14 and does not point to errata as item requests. |
| 7 | R56.2 | Keep open: unmet literal clause | `SKILL.md:51-55`, `ca75c2674645ab6bdadeecb8584007c74342bfa9`. Standing cell corrected to CONTENT_DRIFT with --paths, but conjunctive docs-arm code-to-role-truth repair is not demonstrated at base. |

**Recommended historical-risk allocation, at most five:** R56.4, R55.2, R56.7, R53.8, R56.6. Reserve no automatic disagreement for R56.3 or R56.2. This is not a directive to falsify statuses if stronger evidence or the new panel establishes closure.

R56.6 is the original registry-map obligation, **not** the stricter round-58 exact-element C2 target: the two refusal arrays still contain `code=RECEIPT_REV_CONTENT_DRIFT` / a full UNRESOLVABLE verdict line, not the bare code elements. The new C2 fix is still owed even if R56.6 is fixed.

## Executed corroboration (commands and output)

Full commands and output: `T58W1RevDisagree-receipts/corroboration.json`.

- `git -C LANE show BASE:.ufo/waves/round-55/w1/T55W1ScribeSkill.md` exits 0. Lines 147-148: `rev=08d64e946006 grammar=9/9` and `docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false`; line 157 labels the earlier 8-mode `total=0`. This independently corroborates R55.2's correction, rather than trusting its assertion.
- `git -C LANE show OLD:corpus/SOURCES.md` and `git -C LANE show OLD:corpus/knowledge/change-aware-resweep-cadence.md` exit 0 and already say `p. 3 (physical)` for S275. R53.8's remaining word-count correction is the new round-57 lesson at lines 12-18; no new source-page repair is needed.
- `git -C LANE diff --stat 877eedee3ddb7fe25d7a6a09922b04ba13e5a99b OLD -- SKILL.md corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge tools` exits 0 with empty stdout. The corresponding C0-to-877eedee diff prints QUALITY +31, SOURCES +2, knowledge entry +39 (and the separately included round-56 lesson +144). This independently corroborates R56.7's interval distinction.
- SHA256 of `git show 877eedee...:corpus/SOURCES.md` is `6c2096d8091f5d5be87a638f1a90ab6322a203c2be516d59dcfb970d4f55a6d3`; QUALITY is `54c49d3873b03acfa5ac4db7e0b7e6621808d80eee3b5ae60b90ad0fa2e2aab7`. C0 hashes instead begin `11c5682902d5` / `80792b7d466d`. Those observed digests match the new R56.4 referent record; no rebinding is asserted.

`LANE` expands to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; `BASE` is the full hash above; `OLD` is `5e3569969b532310d2b8a3d130901757a3df356b`. Receipt files contain expanded commands, not these abbreviations.

## Sweep and exclusions

Executed `git -C LANE log --format='%H %s' OLD..BASE` and `git -C LANE diff --name-only OLD BASE`: 11 commits, 2214 changed paths, dominated by wave evidence and cold-read binding. Non-wave/non-coldread changes are retained in the receipt, including all changed content paths. No original round-50..56 lesson, receipt gate implementation, or round-51 counter repair appears among changed content. The seven ranked items are the concrete closure candidates surfaced by this committed-content sweep.

Other old-open items screened, not promoted: R50.4, R51.4, R51.5, R51.6, R51.8, R52.3, R52.6, R53.1, R53.2, R53.3, R53.4, R53.5, R53.7, R54.7, R54.9, R55.1, R55.4, R56.1, R56.5.

- R51.4: the historical panel explicitly distinguishes a passing host selftest from the unmet counter-level fleet-bound amendment and mutation attack. No new repair to those surfaces appeared.
- R51.6: round-57 now has an explicit rejected-candidate Gate row, but this does not repair the original round-51 Gate omission; do not spend tolerance on an extrapolated prospective fix.
- R54.7 / R54.9: historical panel reports explicitly retain the unsuperseded deletion statement and unresolved staged-count denominator, respectively. Neither original surface changed in this range.
- Remaining items: **INFERENCE**, not an exhaustive negative semantic proof: no item-specific committed remedy was established in this sweep. Retain open rather than upgrade based on later unrelated receipts or honest-stop prose. The report does not assert that no hidden fix exists anywhere in 2214 artifacts.

## Residual risk and verification gaps

No new round-58 blind-panel verdicts were consulted. Final allocation must use that panel, so this is a ranked risk plan, not a prediction of final disagreement count. No runtime, tests, build, lint, counter, gate execution or cold-read monitor run was performed. Static code/registry presence is not a runtime PASS. No canonical runtime or resume logic was changed, reviewed or claimed compliant: those surfaces are outside this ticket.

LSP prerequisite attempt: `read xd://lsp` returned `No such tool: xd://lsp`; no status/references/definition/diagnostics device is mounted. Immutable git content and literal text are therefore evidence only, not semantic caller proof.

No lane content edited; only this seat's report/JSON/receipts written. No tools installed or upgraded. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W1RevDisagree` was created and removed; executed cleanup printed `scratch removed: /fast/scratch/hyaku/tameshi-r58/T58W1RevDisagree`. No scratch clone was necessary: git object reads are pinned to BASE.

Self-evaluation: accuracy 4 (static evidence, no runtime assertions); completeness 4 (all old-open ids screened, remaining negative conclusions explicitly inferential); clarity 4 (old/new panel distinction explicit); actionability 4 (five priorities and two concrete unmet clauses); conciseness 4 (large raw receipts kept outside report). Overall 4.0. Main should resolve against the new panel rather than treat this historical ranking as a scoring result.
