# CalibCritic — C2 calibration 6→8

**Verdict: PARTIAL — lane-seat evidence can support the box-3 `[~]` increment and 8 is the existing lane-attainable rubric cap, but C2's 6→8 does not hold at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`; its counter returns 6, and the ledger admits vacuous evidence.** This is a falsification review, not round admission or promotion judgment.

## Axes and scope

- **Calibration:** primary — self-assessment, evidence sufficiency, correct lane/non-author provenance, and avoiding premature saturation.
- **Depth:** guardrail — verification-fixture craft must distinguish execution of a procedure from a count of report labels.
- **Operability:** impacted by the counter's incompatibility with the canonical checklist layout and replacement-mode validation.

All lane source references below are to **`c699c8c36d6e4eca4b796b81a8247904aa145ec8`**, not the changing worktree. Committed files were extracted with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <revision>:<path>` into `/tmp/tameshi-r16w2-CalibCritic-ZYj77F`; each extraction exited 0. No lane tool was executed from the lane worktree. No other agent was dispatched, no canonical judge/runtime was invoked, and no commits or git-index changes were made. The only persistent write is this report. No tools were installed or updated; existing Python is **3.14.8**.

Pinned program identities:

| Path | SHA-256 |
|---|---|
| `.ufo/evidence/round-16/measure.py` | `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e` |
| `.ufo/evidence/round-16/coldread/assemble.py` | `8484a1b3204c506655a5e33a17fa65d5717432e322ba51ae47ee3ede6da65378` |
| `SKILL.md` | `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` |
| `.ufo/evidence/round-16/coldread/SKILL.snapshot.md` | `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` |

## 1. Lane-seat admissibility and the cap: agreement, with a strict boundary

**The authority objection alone does not defeat the proposed two points.** `SCORECARD.md:67` explicitly scores correctly restrained, durable-evidence-linked lane assertions at two points each, caps that component at 8, and reserves the last 2 for independent promotion review. `SCORECARD.md:255-260` repeats that this is a lane policy choice, not an observation. Canonical protocol evidence independently agrees on the authority distinction: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:63-73` says a lane-dispatched subagent remains the lane, permits its evidence-linked `[~]`, and reserves `[x]` for a named non-author. Thus another seat name does not confer independence, but independence is not a prerequisite to the lane's own `[~]` assertion.

**Conditions:** the evidence must actually establish the scope of box 3; all marks remain restrained; neither the score nor a lane seat may substitute for independent round closure or promotion review. Eight is the **existing numeric restraint rubric's lane-attainable cap**, not a universal ceiling on calibration expertise, not independent promotion credit, and not proof that all axes have saturated. `SCORECARD.md:209-225` pins the prior score at 6 despite four `[~]` marks. `corpus/QUALITY.md:43-46` bars Appendix-A/B-only credit. The present claim must remove that actual evidence deficit, not merely recount marks or headings.

## 2. Concrete shipped failure: the counter cannot recognize the canonical evidence line

Executed:

```sh
python3 /tmp/tameshi-r16w2-CalibCritic-ZYj77F/.ufo/evidence/round-16/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c699c8c36d6e4eca4b796b81a8247904aa145ec8
```

**Exit 0**, key output:

```text
calibration_restraint_score: 6
shonen.marks: ["~", "~", "~", "~"]
shonen.box3_marked: true
shonen.box3_ledger_link: false
shonen.box3_points: false
coldread.ledger_present: false
coldread.sections_total: 54
coldread.sections_covered: 0
coldread.box3_full_page: false
```

There are **two independent failures**:

1. No committed `.ufo/evidence/round-16/coldread/ledger.json` resolves at the pin. This is an observed pre-integration state, not evidence that future wave-2 reports cannot finish the task.
2. Even after supplying a complete ledger, the link check still fails. `SHONEN.md:9` is the canonical unchanged checkbox wording; its actual link is on the permitted indented evidence line **`:10`**. `measure.py:62,137-139,255,261-263` captures only checkbox-line text and searches that text for the link. It never inspects line 10. Its synthetic successful fixture instead appends evidence directly to the checkbox wording (`measure.py:310-318`), so its success case does not model the delivered canonical layout.

An isolated counterfactual helper call supplied the complete synthetic ledger from probe 3 below in memory while retaining **all other real committed blobs**: `coldread.box3_full_page=True`, `shonen.box3_ledger_link=False`, and `calibration_restraint_score=6`. This is explicitly a synthetic substitution, not a claimed 54-section cold-read.

**Smallest safe correction:** parse each checkbox and its single indented evidence line as one box record; resolve the ledger from the box-3 evidence line. Preserve the canonical checkbox wording rather than appending the path to it. Add a regression fixture using the actual canonical two-line layout. Commit the real ledger and measure the delivered revision before reporting 8.

## 3. Credit rule: useful guardrails, but a section can pass vacuously

### What holds

`measure.py:162-199` rejects blocking gaps, wrong expectations, failed verdicts, instruction/`verified-record` mismatches, and instructions with a zero command count. `assemble.py:388-409` merges strictest verdicts and sums blocking/wrong counts; `:222-225` downgrades declared clean results carrying minor gaps. Both section parsers agreed on **all 54 actual final-page section starts and hashes** in this review. I did not find an actual current-page sectioning discrepancy.

### Executed adversarial counterexamples

Executed **`python3 /tmp/tameshi-r16w2-CalibCritic-ZYj77F/probe.py`**, exit **0**. The script imported the two unchanged pinned programs and invoked the assembler's public CLI on scratch-only inputs. Each row below reports that CLI's actual exit, then the unchanged `measure.coldread()` result over its ledger. These are deliberately false synthetic reports, **not allegations that real seats executed nothing**.

| Synthetic input | Assembler exit | Counter result |
|---|---:|---|
| All 54 real page buckets labeled `record/verified-record`, with `commands_executed:[]` and `opened:[]` | 0 | `full_page=True covered=54 total=54` |
| All 54 real page buckets labeled `instruction/executed-ok`, with **`commands_executed:[null]`**, `opened:[]` | 0 | `full_page=True covered=54 total=54` |
| One section: instruction observation `executed-ok` with **no commands**, plus record observation `gap-minor` with one record-anchor command | 0 | `full_page=True covered=1 total=1` |

Input schema used for each observation (start and heading were copied exactly from the committed sectionizer):

```json
{"start":17,"heading":"## Standing rules","class":"instruction","verdict":"executed-ok","commands_executed":[null],"opened":[],"blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[]}
```

The top-level report supplied only `seat`, the actual `skill_sha256`, and `sections`, inside a final fenced JSON block. For the first experiment, every section instead used `class:"record"`, `verdict:"verified-record"`, and an empty command list. For the third experiment, the second observer used `class:"record"`, `verdict:"gap-minor"`, `commands_executed:["record anchor lookup only"]`, and `minor_gaps:["Record-only qualification"]`.

**Why they pass:** `assemble.py:195-215` checks list container types, not command element validity or record evidence; `:407-409` turns their lengths into credit. `measure.py:195-197` grants record credit with no command, opening, or anchor requirement. Cross-class merging at `assemble.py:388-409` donates a record observer's command count to an instruction observer that executed nothing. This is more than the unavoidable fact that JSON cannot prove a human read: the current structural check accepts **null as execution** and composes evidence from the wrong class.

**Smallest safe correction:** validate nonempty command/evidence objects or strings; keep evidence attached to each observation and evaluate class-appropriate credit **before** merging; require at least one checked, revision-qualified anchor per record claim cluster rather than an ungrounded record label. Treat mixed instruction/record sections as instruction whenever they contain actionable requirements. Human/L1 review still has to check that the claimed commands exercise the section's requirements; one unrelated command is not an end-to-end execution proof. The actual reassembled wave-1 record entries all had positive command counts, so the empty-record experiment identifies an acceptance hole, not a measured failure by every record seat.

## 4. Replacement overrides can erase a live blocker without validating the replacement

Additional rows from the same executed probe script:

| Input | Assembler exit | Counter result |
|---|---:|---|
| One real synthetic section, `instruction/gap-blocking`, `blocking_gaps:["Known gap"]` | 0 | `full_page=False covered=0 total=1` |
| Replace that entry using a report with the matching skill hash/start but **heading `# NOT THE SECTION`** and `executed-ok` | 0 | `full_page=True covered=1 total=1` |
| Replace using a report with two observations at the same start: first `executed-ok`, second `gap-blocking` with `blocking_gaps:["Still broken"]` | 0 | `full_page=True covered=1 total=1` |

The scratch skill bytes were `# Procedure\nRun the page-defined procedure.\n`. The replacement JSON record was exactly the following shape, with the computed section digest and scratch report path substituted:

```json
{"sha256":"<section digest>","report":"<replacement report>","reason":"Synthetic adversarial input"}
```

**Evidence:** normal assembly checks headings at `assemble.py:368-379`, but replacement at `:509-552` only checks the skill hash and section start. It takes **`robs[0]`** at `:542`, bypassing both heading validation and the normal strictest merge of replacement observations. It replaces gap counts with the first observation's counts. The old verdict is retained as metadata (`:557-563`), but the blocker has nevertheless disappeared from effective credit.

**Smallest safe correction:** run replacements through the same boundary/heading validation and strictest per-observation credit path as normal reports; reject duplicate conflicting replacement observations or merge them conservatively. A same-sha relaxation requires an explicit, checked disposition of each earlier blocker, not merely a report path and free-text reason. Allow a justified correction of a seat mistake, but do not let an arbitrary author override silently convert a known procedural failure into success.

The baseline `gap-blocking` case itself exits 0 because assembly exit 0 means **entry presence**, not credited coverage (`assemble.py:431,1066`). That distinction is intentional in the code, but callers must not cite an assembler exit 0 as proof of box-3 success.

## 5. Repairs + re-read: viable method, not yet the delivered evidence

I extracted the **38 committed `CR*.md` wave-1 files** and executed the pinned assembler with `--skill <snapshot> --skill <final SKILL.md> --out /tmp/tameshi-r16w2-CalibCritic-ZYj77F/actual-w1.ledger.json` and those 38 explicit report paths. **Exit 1**; key output:

```text
ledger written: .../actual-w1.ledger.json (51 entries)
coverage: 51/65 sections covered
```

The 65 is the **union of pre/post section hashes**, not 65 final-page buckets. Feeding that actual ledger into `measure.coldread()` over final `SKILL.md` gave **40/54 credited, full_page=False**. Fourteen final-page buckets lack entries: starts **6, 58, 131, 246, 314, 497, 921, 933, 1380, 1464, 1609, 1707, 1740, 1789**. These are eleven changed sections and three appended sections. Non-seat critic/ledger reports lacking the JSON trailer were loudly skipped; their skipping is not itself a missing execution.

This is positive evidence that the hash rule does **not** simply carry repaired text forward on its old pass. Rereading changed/new buckets, preserving validated byte-identical observations, and separately checking whole-page coherence is a reasonable way to assemble a **lane** full-page assertion. There is no evidence requirement here that every specialist must rerun every unrelated section. However, section hashes alone do not validate dependencies: changed pointer targets, tool revisions, or cross-section context can invalidate a byte-identical section's earlier execution. In-place repair needs retained old observations, explicit supersession, final pins, and a final-page coherence/pointer check. Keeping line counts unchanged (`SKILL.md:1713-1715`) addresses line shifts, not every dependency change.

At this pin the prose is ahead of its evidence: `SHONEN.md:10` claims a full-page ledger; `SKILL.md:1781-1787` says repaired and new sections **were re-read in wave 2**, but there is no committed ledger and the committed wave-1 observations leave 14 post-page sections uncovered. That is an unfinished integration state, not a verified 6→8 result. This review makes no claim about subsequently delivered wave-2 artifacts.

### Strong remaining scope objection: Appendix B's fixtures

The repair also leaves the old self-containment deficit standing:

- `SCORECARD.md:209-218` excludes the previous box-3 increment after Appendix A/B-only work with reconstructed Appendix-B fixtures. The non-author record `corpus/lessons/round-1-verifier-spotcheck.md:17` explicitly retains both qualifications and calls for a fresh reader to execute the **full page-defined procedure**.
- `SKILL.md:594` still says **“reproduce from this page alone”**. Its probe commands at `:621-623` consume fixture files that its preceding setup does not construct. The explicitly named source's `corpus/knowledge/mutation-case-kagi-census.md:208-254` names those fixture paths and repeats the commands, again without constructing the fixtures.
- The new execution reports confirm, rather than remove, that gap: `.ufo/waves/round-16/w1/CR12a.md:45-59` says the seat derived fixtures from the substrate schema and calls the page not self-contained; `CR12b.md:100-106` likewise describes constructing fixtures from usage/selftest builders. Both executions can be genuine and useful; neither changes the written setup.
- `SKILL.md:1733-1737` explicitly carries this as a minor gap. Consequently the assembler's `gap-minor` allowance can count the very missing setup the prior adjudication named, without any additional scope test.

**Assessment:** successfully designing fixtures after reading named source code is not necessarily oral-context contamination. Nevertheless it is not proof of the stronger, unchanged “from this page alone” wording, and merely relabeling the retained omission minor is not a safe resolution of the earlier outside exclusion. **Smallest safe correction:** add the missing minimal fixture-construction recipe, or a precise pointer to a durable reproducible fixture artifact/setup; have an unexposed seat execute that final route. If retaining reconstruction as an intentional exercise instead, state that requirement and its dependencies explicitly and obtain outside agreement that it satisfies the excluded box-3 scope. Do not silently relax the existing expectation to obtain 8.

## Conditions for a defensible C2 candidate

1. Keep lane authorship explicit: `[~]`, no independent `[x]`, and no promotion or canonical admission inferred.
2. Correct canonical evidence-line parsing and measure a commit that actually contains the linked ledger.
3. Validate evidence before aggregation; reject null commands, ungrounded record credit, command donation, and replacement-mode bypasses.
4. Supply genuine final-pin reads/executions for all changed/new buckets (the committed wave-1 set is 40/54 on the final page), plus dependency and whole-page coherence checks; preserve superseded observations and reasons.
5. Resolve the Appendix-B fixture/self-containment objection without counting the unchanged missing setup as a cosmetic minor gap.
6. Only then compare 6→8 using the recorded rubric. Eight remains the local lane-only restraint cap; saturation and promotion are separate claims.

No built-in selftest, mutation sweep, or broader round verification was run by this seat. Exercised checks were the pinned counter, scratch-only public-CLI adversarial cases, committed-report reassembly, and pure helper comparisons described above. Findings are fixable defects in the evidence/counter path; none justifies a trade in calibration for apparent coverage. The final admissibility decision belongs to the canonical judge/non-author closure, not this seat.
