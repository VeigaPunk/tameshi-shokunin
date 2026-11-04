# tameshi round 72 — verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-03 against lane tip `9b4ffe4722befcf6d271d6e168d6a3d20575e913`
(branch `master` == `origin/master`), base `f20ba482c7441d4c75818e7cd8a3165fee7821a1`.
Every reading below was taken by this verifier from committed bytes with plain
git/awk/python counts; the lane's own gates were read as committed receipts and
were not executed. Verdict: **admitted** — both claims verify, no axis is harmed,
two report-accuracy defects and three freeze/report consistency defects routed.

## 1. Step-1 conformance

| Check | Result | Evidence (this verifier's own run) |
|---|---|---|
| Report committed in the fleet repo by the lane identity | PASS | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-72/tameshi.md` → `tameshi-shokunin <tameshi@shokunin.local> 3664a6d30051410c3d2bb8c32926d13e284a5118` |
| Report lands after the lane work | PASS | lane tip commit `9b4ffe47` dated 21:39:39 -0300; report commit 21:39:58 -0300 (19 s later) |
| `SHONEN` heading, one line per box | PASS | report has `## SHONEN` with four `[~]` lines; `tameshi-shokunin/SHONEN.md` carries four boxes (all `[~]`), so the count matches |
| Every cited lane commit exists and is an ancestor of the branch | PASS | 18 cited hashes resolved with `git rev-parse --verify <h>^{commit}` and `git merge-base --is-ancestor <h> refs/heads/master` (detached-HEAD tolerant): `dfb534ca d618518a bc7dc2fb b611e763 b3392010 de43f7dc 93cae77b b7b98375 d7eb02c2 a533d7d3 ebad004b d8e7f337 56866fa3 9b4ffe47 292ceec0 f20ba48 8b0042bd 4ed9ce1c` — all `anc` |
| Round range matches the report | PASS | `git rev-list --count f20ba48..9b4ffe47` → `17` commits, the declaration → tip sequence the report lists |
| Lane repo clean, nothing uncommitted, pushed | PASS | `scripts/hyaku/jj-lane.sh state <lane>` → `branch=master local=9b4ffe47… remote=9b4ffe47… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints nothing |
| Prompt carries the template contract | PASS | `diff <(sed -n '1,140p' .ufo/prompts/tameshi-round-72.md) templates/round-prompt.md` differs only on `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §6 hyaku addendum and §7 scratch discipline follow; §3's `at least 8 L2 subagents in ONE batched AgentSwarm call` matches `MISSION.md` §L2 concurrency |
| Report is a real report, not a marker | PASS | work performed with evidence pointers, landed changes tied to LOG entries and commit hashes, before→after counters, Sources & frontier, trend verdicts, SHONEN |
| Report accuracy — wave count | **DEFECT (status-neutral)** | the round-shape line says `12 seats, 11 reports`; `ls .ufo/waves/round-72/w1/*.md` → `12` seat reports and `w1-results.json` carries `12` seat records (the report's own Wave paragraph says all 12 returned) |
| Freeze consistency — seat roles | **DEFECT (status-neutral)** | `plans/round-72.plan.md` (frozen at `dfb534ca`) lists `1 labrat` and `attack roles … labrat = 4 = 33 %`; the same commit's `w1-spec.json` and the executed wave list `revenger` (12 items: executor×3, scribe×2, scout, reviewer, critic, mutation-tester, sentinel, revenger, connector), i.e. 3/12 = 25 % by the policy's named set — which the report does state |
| Landed-changes to LOG-entry binding | **DEFECT (minor, status-neutral)** | the report's table leaves the LOG-entry column as `—` for `93cae77b`, `ebad004b`, `d8e7f337`; PROTOCOL's minimum content asks each landed change to be tied to a `LOG.md` entry |

Nothing above changes the lane status; none of the defects touches the round's
claims.

## 2. Per-claim re-check

Two claims, distinct axes, both frozen in `plans/round-72.plan.md` at `dfb534ca`
(before any claim data; the declaration commit is the parent-side commit of the
17-commit range).

### R72-C1 — operability (capability acquisition: planning-time rekey-cost forecast)

**Before (re-measured).**

```
git ls-tree -r f20ba48 tools/ | grep -c rekey-cost      -> 0
git grep -l rekey-cost f20ba48 | wc -l                  -> 0
```

**After (re-measured).** `git ls-tree -r 9b4ffe47 tools/` → `100755 blob
859a4860… tools/rekey-cost.py` (277 lines); `SCORECARD.md` gains the row
`| rekey-cost forecast | … | round 72 |` under `## Capabilities`
(`git diff --numstat f20ba48 9b4ffe47 -- SCORECARD.md` → `81 0`).

**Independent re-derivation of the model (not the tool).** This verifier
re-implemented the documented rule — split `SKILL.md` on `^#{1,3}` outside
fences, keep the newest ledger entry per heading, a section is at risk when a
planned path is in that entry's `inputs` — and ran it over the committed blobs
at both revisions:

```
sections=64; SOURCES 13; PROVINCE 6; QUALITY 6; SCORECARD 0; POINTER 0; BOTH 17
```

identical at `f20ba48` and at `9b4ffe47`; the union is 17, not the sum 19.
This reproduces every frozen arm and the round's forecast without executing the
lane's tool.

**Evidence-verified (committed receipts, not executed by this verifier).**
`cost-live-selftest-r72.txt` → `REKEY_COST_SELFTEST: 8/8 pass` (arms 1–8 all
`ok`); `cost-prediction-at-edit.json` → `at_risk: 17, predicted_lost: 17`;
`reh/reh-*.out` → the guard counterfactuals `lost=13/6/6/0/17`;
`live-red-r72.out` → `COLDREAD_PRECHECK floor=f20ba482c744 floor_credited=64
cand=d618518a6783 cand_credited=47 lost=17 RED`.

**Verdict: `improved`** — a capability entered the repertoire through its own
demonstration (tool in the tree, capability row, selftest tally, live forecast
equal to the guard's measured loss), and the model reproduces independently.

### R72-C2 — calibration (the two round-71 routed record defects paid)

**Before (re-measured at `f20ba48`).** `corpus/SOURCES.md:177` (S302) reads
`§4.3's numeric-address form … page line 2255` and pins the §4.4 quote at
`page lines 2445–2448`; `PROVINCE.md:56` reads `tools/mutate-and-run.sh:84-89`
and `:57` reads `:85-91`.

**After (re-measured at `9b4ffe47`).**

```
corpus/SOURCES.md rows: 162 (f20ba48) -> 163 (9b4ffe47)
S303 row at line 178: anchor "§4.4 … page lines 2446–2449 (S302's 2445–2448 is
off by one); §4.2 Selecting lines by numbers … page line 2246 … 2255";
teaches opens "supersedes S302 —"; status mined; used-by corpus/lessons/round-72.md
PROVINCE.md diff f20ba48..9b4ffe47: +25 / -0 (two appended correction blocks;
lines 56-57 stand append-only, byte-identical)
ledger .ufo/evidence/round-21/coldread/ledger.json:
  entries 797 (f20ba48) -> 814 (bc7dc2fb) -> 820 (d7eb02c2, tip)
  base lines missing at tip: 0 of 281,926; CRLF counts 281,925 -> 0 (bc7dc2fb,
  the disclosed defect) -> 293,268 (b611e763) -> 303,657 (tip)
  rekey batches: r72-batch-1 = 17 entries, r72-batch-2 = 6 entries
```

**Pointer rows (re-measured by this verifier's own extractor over committed
blobs, `pointer` token in the record + `needle` in the target span):**
all 12 rows of `tools/pointer-recheck.json` reproduce `rows=12 met=12` (9 `hit`,
3 standing-red `miss`); the two-row control manifest reproduces `rows=2 met=2`
both `miss`; the aimed control reproduces `rows=3 met=2 unexpected=1` with
`sources-s303-aimed-base` the MISMATCH row (the base cannot satisfy the label
check), exactly as the lesson reports.

**Source snapshot (re-measured).** `git show 9b4ffe47:.ufo/evidence/round-72/sources/sed.html`
→ sha256 `511edd60a6f5034d4f28ca1dbe0772bbfd4c9865aaf6c0f85e2f05d4294b6bac`,
415,310 bytes — identical to the row's pin and to the r71 snapshot. Page lines:
2246 = `<h3 … 4.2 Selecting lines by numbers>`; 2255 = "Specifying a line number
will match only that line in the input." (12 words); 2442 = `<h3 … 4.4 Range
Addresses>`; the quote's paragraph spans 2446–2449 (the quoted sentence starts
on 2447 and runs to 2449). S302's `§4.3` label and `2445–2448` pin were both
wrong; the correction is right.

**PROVINCE spans (re-measured at the base blob).**
`tools/mutate-and-run.sh` at `f20ba48`: line 84 `# --regression …`, 85–87 the
narrative, 88–93 legs 1–6 (`js-claims-check` at 93), 88–94 legs 1–7
(`js-round-gate` at 94), 88–97 legs 1–10 (`bash-drift-pins` at 97). The appended
correction's three spans are exact; `:84-89` and `:85-91` were both stale, as
the round-71 closure routed.

**Evidence-verified.** `live-green-r72.out` → floor `f20ba482c744` 64 → 64,
`lost=0 ok` at `cand=56866fa37ec4`; `live-green-hist-r72.out` → `8b0042bd`
46 → 64; `live-green-floor4ed9-r72.txt` → `4ed9ce1c` 64 → 64 at
`cand=d8e7f33724b4`; `live-revmode-r72.out` → `credited=64/64`; both rebind
summaries → `entries_added: 17` (before 797) and `entries_added: 6` (before
814), with `skill_sha256 b56c0252…` equal to `sha256(SKILL.md)` at both pins.

**Census (this verifier's own run).**

```
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
-> exit 0; last line "tameshi ok <lane>/corpus/SOURCES.md"; warnings only
   (W04 duplicate-url rows incl. S303, W01 S101 tier-C mined)
```

Row histograms re-measured independently: tier `A 144→145, B 14, C 4`; status
`mined 130→131, queued 22, rejected 10`; kind `docs 89→90`; malformed rows `0`;
duplicate ids none — every figure the report prints.

**Verdict: `improved`** — a weaker row is superseded by a stronger one with
measured anchors, both routed defects are corrected and now standing-measured on
every sweep, the mid-round EOL defect was caught and repaired to byte
additivity, and the cold-read monitor reads green at both floors and in rev mode.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | **improved** | capability `rekey-cost forecast` in `SCORECARD.md` `## Capabilities` (round 72), tool committed, selftest 8/8, forecast 17 = guard `lost=17`; the rule reproduces independently |
| calibration | **improved** | S302 superseded by S303 (§4.2, 2446–2449); PROVINCE `:85-91` and `:84-89` corrected by append with measured spans; 12 pointer rows met; census exit 0 |
| depth | unchanged | `SKILL.md` sha256 `b56c0252…` identical base→tip; no case added; `SCORECARD.md` diff `81 0` |
| coverage | unchanged | `corpus/README.md` sha256 `84602843…` identical; no frontier row advanced (the report says so and the bytes agree) |
| freshness | unchanged | no re-pin of held sources; `corpus/QUALITY.md` identical; the standing instruments re-read clean (receipts: figure-attribution 3/3, count-recheck 7/7, anchor-drift 16/16, arm-liveness 9/9) |
| adjacency | unchanged | no sibling write; PROVINCE.md unchanged except the two in-scope append blocks |

No axis is harmed: the only monitored edits are `corpus/SOURCES.md` and
`PROVINCE.md` (plus the free `LOG.md`/`SCORECARD.md` appends), and both edited
files were rekeyed; `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`,
`tools/registry.json`, `SHONEN.md`, `tools/mutate-and-run.sh` and
`tools/coldread-precheck-portable.py` are sha256-identical base→tip.

## 4. Discernment spot-check (`corpus/lessons/round-72.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S303 row (admit, supersedes S302) | admit | `.ufo/evidence/round-72/sources/sed.html` at `9b4ffe47` (sha256 `511edd60…`, 415,310 B) — page lines 2246, 2255, 2442, 2446–2449 | **agree** | the heading at 2246 is `4.2 Selecting lines by numbers` (not §4.3); the 12-word sentence sits at 2255; the §4.4 quote's paragraph spans 2446–2449, so S302's 2445–2448 was off by one; the row's `teaches` opens `supersedes S302 —` per CORPUS rule 2 |
| S293 row (standing reject re-sampled) | reject | `corpus/SOURCES.md` rows S289 (line 164) and S293 (line 168) at `9b4ffe47` | **agree** | S289 already holds `git-cat-file` docs at tier A for object inspection; S293 adds batch framing on the same URL, so the within-scope-duplicate rejection with a named flip stands |
| S303's ≤25-word quotes | admit | the same snapshot lines (2255, 2447–2449) | **agree** | 12 words and 20 words, both located; the row and the lesson carry the locations |
| Census exemption sentence (report Sources: "the counter-run without the prefix prints E04") | admit (mechanism) | live census counter-runs: the real row with the prefix removed prints `W04 duplicate url … across scopes` and the lane stays clean; `E04` appears only when the superseding row's scope string is identical to S302's (this verifier reproduced `E04 S303 duplicate url … within scope …` with the scopes aligned) | **disagree (wording only)** | on the real registry S303's scope is restated, so the E04 exemption is not load-bearing for it — only the W04 warning applies; the seat's fixture exercised E04 by aligning the scopes, which the report's sentence does not say. The row itself is correct |
| Census validate | gate | `scripts/sources-census.sh validate --root … tameshi` (this verifier's own run) | **agree** | exit 0, `tameshi ok`; the warnings are the pre-existing W04/W01 set plus S303's expected duplicate-URL warning |

## 5. Trend verdicts

- **expansion — improved.** A capability entered `SCORECARD.md` `## Capabilities`
  (`rekey-cost forecast`, first working round 72) through a demonstrated run, and
  the registry gained one mined row (S303, tier A docs) with a located quote;
  no admitted entry was displaced (S302's cells are byte-identical, the SOURCES
  diff is `1 0`). The frontier itself did not move, which the report states.
- **quality — improved.** A weaker entry (S302) is superseded by a stronger one
  with measured anchors; the two routed defects are now standing-measured (12
  pointer rows met, the red arm still measuring the stale cell); the round's own
  EOL defect was caught by a seat and repaired to byte additivity (0 of 281,926
  base lines missing, CRLF restored); the monitor reads `lost=0 ok` at both
  floors and `credited=64/64` in rev mode.
- **discernment — improved.** The gate re-sampled its standing rejection and
  agreed; three seats' attacks were adopted as work (the EOL rewrite, the third
  stale span, the arm-coverage gap); one frozen control line was found
  unattainable and reported as wrong instead of silently rewritten. This
  verifier agrees with the admit and the reject re-opened above; the one wording
  disagreement (§4) is routed, not absorbed.

## 6. Routed defects for the lane (all status-neutral; next round)

1. **Frozen plan vs executed wave.** `plans/round-72.plan.md` names `1 labrat`
   and "attack roles … = 4 = 33 %"; the committed `w1-spec.json` and the wave
   ran `revenger` (3/12 = 25 % by the policy's named set). Append an erratum to
   the plan naming the superseded line (plans are frozen text, not rewritable),
   and have the next report state the freeze mismatch explicitly.
2. **Report count.** "12 seats, 11 reports" contradicts 12 committed seat
   reports and 12 `w1-results.json` records; correct it in the next round's
   erratum/report.
3. **Census sentence precision.** "the counter-run without the prefix prints
   E04" is true only for a same-scope fixture; on the real row the removal
   prints W04 and the lane still validates clean. Restate, since the census gate
   is one of the lane's standing instruments.
4. **Manifest note count.** `tools/pointer-recheck.json`'s top-level `note` now
   ends "round 72 adds three green arms" while four r72 green arms are present
   (the fourth, `province-r72-sixleg-cut-88-93`, was added post-freeze and is
   disclosed elsewhere). The note is not append-only by contract, but its count
   is stale.
5. **LOG binding for receipt-only commits.** `93cae77b`, `ebad004b`, `d8e7f337`
   are listed with `—` in the report's LOG column; tie receipt-only commits to
   the "Round 72 — appended after the wave" entry, or say they inherit it.
6. **Carry — arm coverage.** The `IGNORED`-filter mutant survives every frozen
   arm and is killed only by the selftest (seat T72W1S09); the lane already
   records the ignored-path arm as next-round work. Keep it on the queue.
7. **Carry — inherited record misses.** SCORECARD's 6 absent cited paths and
   LOG's 5 missing quotes (rounds 35–41), both disclosed by the tip receipts, are
   inherited, not this round's.

## 7. Closure

Conformance: real report, lane identity, `SHONEN` heading with four `[~]` lines,
all 18 cited commits ancestors of `master`, lane clean and pushed (`ahead=0`),
prompt a faithful template rendering plus the hyaku addendum. Claim C1 verifies
(part re-measured by an independent implementation of the documented rule, part
evidence-verified from the committed receipts); C2 verifies (re-measured against
the committed bytes, including the source snapshot, the pointer rows and the
ledger additivity; the guard receipts evidence-verified, census run by this
verifier). No axis harmed. **Admitted**, with the five routed defects above.
