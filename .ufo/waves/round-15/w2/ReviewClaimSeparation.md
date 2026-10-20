# Round 15 — C1 claim-separation review (static, author-side advisory)

Seat: `TameshiR15.ReviewClaimSeparation` (leaf reviewer). Lane: tameshi. Scope: whether the single C1 calibration claim (score 6→6) stays one calibration capability, with no hidden independent axis move and no promotion credit. Static reads only. No checks, builds, tests, selftests, hashes, or gate runs were executed. No commits. No tool installs or updates. No pacman. `~/.omp/agent/agent.db*` and credential files were not read.

Status: **no implementation-critical defect found.** Four premise/wording findings (two medium, two low) and three watch items. Bounded agreement on the claim-separation questions is recorded below. Nothing here is a verdict or admission; it is advisory evidence for L1 and the non-author closure.

## Source read (exact)

- `AGENTS.md#A117` (1–6)
- `corpus/lessons/round-14-verifier-spotcheck.md` (Routed defects item 5, line 160; claim-level decision table, lines 121–131; scorecard table lines 108–116)
- `corpus/lessons/round-15.md` (whole file, 94 lines; Gate, Mistakes table, Routed-item disposition)
- `.ufo/evidence/round-15/claims.json` (whole file)
- `.ufo/evidence/round-15/integration-decisions.json` (whole file)
- `SKILL.md` lines 1609–1692 (round-15 appendix: classification correction, archive status, retained-check semantics, evidence table at 1661–1667, exit classes 1669–1675, round-15 registry row 1681, closing bounds 1684–1692)
- `tools/context-capture.py` lines 1–123 (docstring, modes, stable finding IDs, exit map), 121–176 (pins and constants: `FROZEN_RECEIPT_SHA256` 137–139, `FROZEN_TOOL_SHA256` 140–142), 298–352 (`tool_sha256`, `read_regular`), 1132–1180 (`check_receipt`, `tool_declaration_mismatch` frozen-only), 1186–1348 (expected pin, `make_result`, `emit`, `apply_expected`, `run_check`), 1349–1600 (fixture helpers, `SelftestHarness` 1572–1725), 1728–2004 (case list, enumerated via grep), 2005–2116 (`run_selftest`, `parse_argv`, `main`)
- `corpus/QUALITY.md` (diff, criterion 17), `corpus/README.md` (diff), `corpus/SOURCES.md` (diff; S049 used-by cell, S051 row, next id S052)
- `LOG.md` (round-15 section, lines 924–946; tied-lowest bullet at 927–928)
- `SKILL.md` (round-15 diff, full added text)
- `SCORECARD.md`: `git diff` is empty (no round-15 row). Axis rows read at 66–67, 107–112, 183–188, 236–262, 296–305, 318–323, 336–337, 350–351, 381–386, 398–403, 438–443
- `AXES.md` lines 1–80 (six axes; "Working the axes"; "Capabilities"; "stagnation nudge")
- `PROTOCOL.md` lines 93–97, 375–400 (Gate standard), 505–517 (Fleet-2 conventions)
- `git status --short` and `git diff --stat`: changed paths are `LOG.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, plus untracked `.ufo/evidence/round-15/`, `.ufo/waves/round-15/`, `corpus/lessons/round-15.md`, `tools/context-capture.py`. `git status --short -- .ufo/evidence/round-14 .ufo/evidence/round-13 tools/evidence-disposition.py` printed nothing, so the round-13/14 archive and the disposition tool are unmodified relative to HEAD.

## Claim inventory under review

`claims.json` declares exactly one claim: `C1`, `axis: calibration`, `type: capability`, `score: "6→6 bounded capability, no promotion points"`. The before/after and scope text is at `claims.json` lines 6–12. The LOG entry, SKILL appendix, corpus README and QUALITY criterion 17 all describe that same claim. SCORECARD is unchanged this round.

## Claim-separation checks

| Question | Evidence | Verdict |
|---|---|---|
| Does any artifact credit a second axis? | Grep of the round diff and of `tools/context-capture.py` for axis, score, promotion, SHONEN, depth, coverage, operability, freshness, adjacency. Only `context-capture.py:9` ("promoted, active replacement") matches. Every axis-like mention in SKILL, LOG and corpus is a disclaimer ("no promotion credit", "no successor sweep", "freshness … remain open", "earns no SHONEN points"; SKILL.md:1619–1621, 1689–1692; LOG.md round-15 bullets; corpus/README.md round-15 section). | **Bounded agreement.** No hidden axis credit is written. |
| Is the SCORECARD left unmoved? | `git diff -- SCORECARD.md` empty. | **Bounded agreement** for this wave. Recording the C1 row is an L1 duty (see W3). |
| Is the claim one axis-move? | Single entry in `claims.json`; `integration-decisions.json` has one claim line. | **Agreement.** Fleet-root `AXES.md` ("Working the axes") requires distinct axes per claim; one is declared. |
| Is the calibration "before" accurate? | `round-14 registry row` at `SKILL.md` (historical, unedited) says `invocation context capture | probe`, "no standalone selftest", and has no 64 class; disposition row says "64 usage". `context-capture.py` docstring lines 58–97 map 0/1/2/64. | **Agreement** with the before text in `claims.json`. |
| Does the exit map stay within the declared lattice? | `main` 2083–2116 and `run_selftest` 2005–2017 return only 0, 1, 2 or 64. `emit` returns `result["exit"]` (0/1/2). Internal exceptions map to exit 2 (2106–2112). Selftest returns 0/1 from `finish` and 2 on setup error. | **Bounded agreement** with SKILL.md:1669–1675 and the docstring at 88–97. |
| Does check mode execute retained argv or open recorded roots? | Only `subprocess` use in the file is `SelftestHarness.run` (1602–1610). Check path reads the receipt via `read_regular` (330–351) and the expected pin (1212–1216). It reads its own bytes for `tool_sha256` (300–306). | **Bounded agreement** with the "data only" claim at SKILL.md:1646–1648. Reading its own source and the lane's frozen receipt is not "live lane input" execution. |
| Are stored verdict fields trusted? | `verify_recorded_verdict` (1108–1129) recomputes exit and status from findings and reports disagreement as `receipt_verdict_mismatch`. | **Agreement** with SKILL.md:1648–1651. |
| Is the frozen pin a literal in the tool? | `FROZEN_RECEIPT_SHA256` at `context-capture.py:137–139`, `FROZEN_TOOL_SHA256` at 140–142, `FROZEN_EXPECTED_ID/EXIT` at 143–144. The strings match the literal text in SKILL.md:1657 and :1634. | **Literal agreement only.** I did not hash the files. Byte identity is not observed here. |
| Do selftest cases pin literal id and exit? | `SelftestHarness.check_case` (1614–1676) asserts `returncode == expected_exit`, `observed_id == expected_id`, `observed_exit == expected_exit`, and no traceback. `usage_case` (1684–1697) asserts exit 64 and `id=usage_error`. Cases enumerated 1737–1994, 1996–2002. | **Bounded agreement.** Literal id/exit pairs are pinned per case. Secondary finding IDs are asserted only in `missing-injected-env` (1741–1747, via `expected_ids`). Other cases pin the primary ID only. |
| Is the selftest hermetic? | `SELFTEST_ENV` (1572–1576), `-I` isolation (1632–1633, 1686), `mkdtemp` root (1581), `hermetic-no-lane-path` and `hermetic-temp-only` cases (1708–1716) and `rmtree` in `finish` (1717) and `run_selftest` (2017). | **Bounded agreement** with the claimed isolation. |

## Findings

### F1 — MEDIUM — "tied-lowest" premise cannot be re-derived from SCORECARD

- **Claim affected:** C1 selection as "lowest non-retired axis" (`claims.json:9–11` before/after/score text; `LOG.md:927–928` "tied-lowest6 with depth6"; `corpus/lessons/round-15.md:4` "tied-lowest axis6 with depth6"; `SCORECARD.md:336` and `:400`).
- **Evidence:** `SCORECARD.md:303` says "Both owned axes tie at 6". `SCORECARD.md:336` and `:400` repeat "tied-lowest"/"tied with depth6 for lowest non-retired axis". The only numeric axis scores are depth 6 and calibration 6 (`SCORECARD.md:66–67`, `:318–319`, `:381–382`, `:438–439`). Coverage, operability, freshness and adjacency appear only as verdict words ("unchanged") at `SCORECARD.md:109–112`, `:320–323`, `:383–386`, `:440–443`. The SCORECARD does not list the owned-axis set, and neither `AXES.md` nor `PROTOCOL.md` in this tree names it.
- **Rule:** fleet-root `AXES.md` ("Working the axes") requires the claim to work "the lane's **lowest-scoring non-retired axis**". Fleet-root `PROTOCOL.md:512–514` (Fleet-2 conventions) says "a score no reader can re-derive is an opinion, not a measurement".
- **Counterexample (not observed, arithmetic only):** if coverage, operability, freshness or adjacency held a numeric score below 6, calibration would not be the lowest axis. Nothing in the SCORECARD excludes that. The verdict-word rows do not establish the tie.
- **Scope:** this affects only the selection premise. The calibration 6→6 score is unaffected. C1 does not become a different axis.
- **Suggested disposition for L1 / lane:** either record numeric scores for all owned non-retired axes in the round-15 SCORECARD row, or state the owned set and the reason the others are out of the tie. Do not carry "tied-lowest" forward as a fact until then.

### F2 — MEDIUM — `claims.json` "after" states unverified runtime results as achieved

- **Text:** `claims.json` "after": "context gate correctly registered with standalone isolated exit+finding selftest and frozen digest-bound retained run; both exit64 classes explicit".
- **What the source supports:** the registry text, the exit-class text and the selftest code exist (`SKILL.md:1681`, `:1669–1675`; `context-capture.py:1728–2004`). Neither the selftest nor the frozen run is observed by this seat, and SKILL says so: "Nothing below was executed for this write" (`SKILL.md:1617–1618`).
- **Rule:** `AXES.md` "Capabilities" says a capability "without a passing demonstration in the round report is pre-claiming and does not enter the table."
- **Risk:** a reader could take claims.json "after" as an observed post-state. That would be a pre-claim.
- **Disposition:** until L1 runs `--selftest` and the frozen `--check` and retains their output, `claims.json` "after" should be read as the declared target, not as observation. The capability row must wait for the demonstration.

### F3 — LOW — Own-work source is the claim's own tool

- **Evidence:** `corpus/SOURCES.md` S051 row ("own-work", tier A, "r15 docstring lines9–14 and Modes lines16–28") and `claims.json` `source` naming S051 as the direct source. The quoted line is `context-capture.py:11–12` ("Check mode writes nothing; the only writes are --selftest fixtures under mkdtemp."), which is the author's own declaration.
- **Bounded reading:** the round-15 lesson itself limits S051 to "bounded data-only replay and demonstrated CLI capability, not historical experiment authentication" (round-15.md, Gate). Under that limit the row is acceptable. It is still circular as support for the "check writes nothing" property. Independent support comes only from the L1 run.
- **Related:** the round-15 lesson states "Source-row count alone is not expansion"; the S051 row should not be counted as coverage (see W2).

### F4 — LOW — Lesson fix wording vs. selftest coverage

- **Requirement:** `corpus/lessons/round-15.md` Mistakes table, gate-misclassification fix: "public --selftest must distinguish old unsupported invocation from new isolated exit/finding cases, with observed receipts retained."
- **Source:** the selftest exercises the new CLI's usage cases (`context-capture.py:1996–2002`: no args, receipt without expected, expected without receipt, unknown flag, selftest with extra argument). It never invokes or names the historical `.ufo/evidence/round-14/capture-context.py` invocation. This is consistent with `context-capture.py:102–103` ("The archived round-14 script is never imported and its main/evaluate/write paths are never used"), so the "old invocation" distinction is carried only by `usage-no-args` exiting 64.
- **Retention:** "observed receipts retained" is an L1 artifact duty. Nothing in the source retains selftest output.
- **Disposition:** L1 should retain the selftest stdout and state explicitly that the old-invocation distinction is established through the new tool's exit-64 usage path, not through the historical script.

### F5 — LOW — "promoted" wording collides with promotion vocabulary

- **Evidence:** `tools/context-capture.py:9` "This is the promoted, active replacement". In this repo "promotion" means SHONEN/shokunin promotion (`PROTOCOL.md` Promotion gates; SCORECARD "no promotion points"). `corpus/lessons/round-15.md` also uses "promote maintained context gate".
- **Effect:** the word could be read as promotion credit inside a claim-separation review. It does not change behavior.
- **Disposition:** prefer "maintained" in the docstring, or accept the lesson's usage and note it in the registry.

## Watch items (no defect now; must stay bounded when scored)

- **W1 — operability double-count risk.** The new artifact is a runnable CLI with `--selftest` (`AXES.md` operability signal: "scripts that run"). The round-14 precedent is that the same capability is "credited once, not another independent axis move" (`SCORECARD.md:441`). The L1 row should keep operability "unchanged" and credit C1 once.
- **W2 — freshness and coverage double-count risk.** S049 was reopened live on 2026-10-20 (`corpus/SOURCES.md` S049 row; round-15.md Gate). That is a re-verification act, which `AXES.md` freshness describes ("re-verified against live surfaces"). S051 adds a source row. Both are disclaimed in the text (round-15.md, "freshness successor sweeps … remain open"; corpus/README.md round-15 section). The freshness and coverage rows must stay "unchanged" and must not cite S049 or S051 as expansion.
- **W3 — SCORECARD and capability rows are absent.** `SCORECARD.md` has no round-15 entry (git diff empty). L1 must append a C1 row with the counting command and measured commit (fleet-root `PROTOCOL.md:512–514`), and enter the capability row only after the selftest and frozen run are retained. This is the integration duty, not a source defect.

## Bounded agreement (what this review affirms)

- One claim, one axis (calibration), one capability type. No other axis is credited in any round artifact read.
- No promotion credit: SHONEN, SCORECARD and the six recorded cases are unchanged; SKILL and LOG state this explicitly.
- Exit classes: the tool emits only 0, 1, 2 and 64, consistent with SKILL.md:1669–1675 and the docstring. Internal failures do not traceback as verdicts (`context-capture.py:2106–2112`).
- Retained-check semantics: check mode does not run argv or open recorded roots; stored verdict fields are recomputed and disagreement is a finding (`context-capture.py:1108–1129`).
- Frozen pins are literal in the tool and match the SKILL text. Byte identity of those files was not observed (F2 / Verification gaps).
- Historical round-12–14 bytes: `git status` shows no change under `.ufo/evidence/round-13` or `round-14`, and the disposition tool is unmodified.

## Considered and rejected

- I first read a possible double `self.failed.append(name)` in `SelftestHarness.record`. Re-reading `context-capture.py:1593–1600` shows a single append. The duplicate came from overlapping line ranges in my own `sed` output. No defect.

## Counterexample status

No concrete counterexample to the single-axis, no-promotion, or exit-class claims was found in the static source. The only concrete premise gap is F1. The only overclaim risk is F2 (pre-claim wording).

## Verification gaps (all L1 duties)

- No selftest, frozen `--check`, or explicit receipt run was executed. Exit codes, finding IDs and `SELFTEST: PASS (N/N)` are not observed here.
- File hashes (`FROZEN_RECEIPT_SHA256`, `FROZEN_TOOL_SHA256`, the historical script's sha256) were not computed. Literal agreement with SKILL text only.
- `SCORECARD.md` numeric scores for coverage, operability, freshness and adjacency were not located (F1).
- `sources-census` was not run. The round-14 lesson records the census result for the prior round only.

## Tool and install record

None. No installs, updates, or package-manager transactions. Pacman paused per operator ruling was not touched.

## Messages

None sent to `TameshiR15`. No implementation-critical defect was found, so no message was warranted.

Report: .ufo/waves/round-15/w2/ReviewClaimSeparation.md
