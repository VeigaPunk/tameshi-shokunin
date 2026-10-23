# CriticNoHarm — six-axis review

## Verdict

**The no-harm assertion is false at content revision `bb681566b18211adf8ae9c28df91e17678e3f545`, before this wave's ledger append.** Calibration is harmed: strict cold-read credit falls **64/64 → 33/64**, restraint **8 → 6**, and box 3 mismatch **0 → 1**. Unchanged SHONEN marks and the supporting C1 counter cannot cancel that loss. This is a fixable evidence deficit, not a permissible trade for a better runner.

Seat: `CriticNoHarm`. Comparison: `9ed6db840dc97a0a5f4758b6b5f60cee83a61645` → `bb681566b18211adf8ae9c28df91e17678e3f545`. These are scoped review findings, not a C1 judgment, admission decision, or promotion review.

| Axis | Review verdict | What the round touched; committed-number exposure |
|---|---|---|
| calibration | **Harmed at the reviewed revision** | QUALITY criteria 58–65, scoped exploratory language, and edits to traced corpus/runner inputs. The observed restraint loss is 8 → 6, despite all four SHONEN marks staying `[~]`. Credit loses 31 sections; the wave's planned reads are not yet credited in this revision. |
| coverage | **Unchanged in this comparison** | One knowledge entry on the already owned runner surface; README explicitly preserves every frontier status. More status vectors and source rows are not a new domain-coverage score. No coverage-map row or SCORECARD number is reduced by the diff. |
| depth | **Unchanged, measured** | The nine recorded ledger cases remain intact. Command D returns `recorded_cases=9 depth_score=9` at both revisions. Added detector cases do not create a tenth recorded mutation case. |
| operability | **No additional harm demonstrated; exploratory C1 judgment reserved** | The runner adds a pre-PASS completeness guard and a detector that actually invokes the extracted tally in Bash. Existing FAIL-before-SETUP precedence remains. Supporting committed evidence reports pristine success and the finite mutant/rewrite outcomes; this review did not replay the nine legs or establish universal behavioral equivalence. No operability numeric score is changed by this diff. |
| freshness | **Unchanged as a scored commitment; local correction recorded** | S092 supersedes the stale S059 anchor without rewriting S059; S087 gains a used-by path; S093/S094 supply newly opened, bounded sources. This does not re-pin the nine sibling gates or establish fleet-wide freshness. No freshness score is changed. |
| adjacency | **Unchanged in this comparison** | Work remains the lane's own runner and verification method. S087 is not made the authority for local refusal policy; S093 is not presented as a measured security boundary. PROVINCE and sibling ownership are unchanged. No adjacency score is changed. |

The operability row deliberately does not award `unprovable-but-better`: that belongs to the assigned C1 judgment, not this critic. The overall no-harm counterexample already exists independently of that judgment.

## Evidence

### 1. Exact change surface and unchanged authorities

Executed read-only command:

```sh
env GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 bb681566b18211adf8ae9c28df91e17678e3f545 -- . ':!.ufo'
```

Observed:

```text
 corpus/QUALITY.md                                 | 101 ++++++++++++++++++++++
 corpus/README.md                                  |   9 ++
 corpus/SOURCES.md                                 |  14 ++-
 corpus/knowledge/regression-tally-completeness.md |  68 +++++++++++++++
 tools/mutate-and-run.sh                           |  66 +++++++++++++-
 5 files changed, 256 insertions(+), 2 deletions(-)
```

In an isolated, no-checkout shared clone, this exact command produced no output and exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git diff --no-ext-diff --no-color 9ed6db840dc97a0a5f4758b6b5f60cee83a61645 bb681566b18211adf8ae9c28df91e17678e3f545 -- SHONEN.md SCORECARD.md SKILL.md PROVINCE.md tools/registry.json
```

The same revision comparison for `.ufo/evidence/round-21/coldread/ledger.json` also produced no output, exit 0. The reviewed content revision does not already contain this wave's restoration entries.

### 2. Strongest counterexample: unchanged marks, lost credit

The following exact read-only commands were executed in the isolated clone. They read committed observations; the monitors were **not rerun**:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git show 9207f226e177c8a1a9a82de677df3cd9f8d1cda3:.ufo/evidence/round-30/monitor-at-base.stdout
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git show 9207f226e177c8a1a9a82de677df3cd9f8d1cda3:.ufo/evidence/round-30/head/c1monitor-at-bb681566.stdout
```

Observed first lines, respectively:

```text
C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9 rev=9ed6db840dc97a0a5f4758b6b5f60cee83a61645
C1_MONITOR: covered=33/64 restraint=6 box3_mismatch=1 depth_score=9 rev=bb681566b18211adf8ae9c28df91e17678e3f545
```

The second retained stdout ends `exit=1` and lists 31 uncovered sections (`.ufo/evidence/round-30/head/c1monitor-at-bb681566.stdout:1-33`). Successful `git show` is not a successful monitor verdict.

One concrete falsifier is `SKILL.md`'s “Mutation-sweep recipe” section, lines 131–245. The committed explanation marks it `credited: false` and names input drift in QUALITY, README, SOURCES and the runner (`.ufo/evidence/round-30/head/monitor-bb681566-explain.json:1554-1565`). This is lost revision-bound evidence, not proof that the instructions themselves are wrong.

The explanation also records `overrides_used: false`, all four marks `~`, and `box3_points: false` (`:2312-2330`). SHONEN box 3 still asserts executability and links the input-keyed ledger (`SHONEN.md:9-10`). Therefore identical checkbox bytes cannot establish calibration no-harm.

The base receipt first landed in `dcdf2d08cb6f7921a194e51299dab4383f3d2716`; the content-revision monitor receipts landed in `07ed440a5b3af74f4e33a80550b669816161bb2f`. These are receipt commits, not substitute measured content revisions.

### 3. Depth command D and SHONEN census

`SCORECARD.md:72-75` defines D and explicitly labels C an upper bound with no evidence/authority credit. Executed D at the target:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git show bb681566b18211adf8ae9c28df91e17678e3f545:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Observed `recorded_cases=9 depth_score=9`. The identical command with the revision replaced by `9ed6db840dc97a0a5f4758b6b5f60cee83a61645` also returned `recorded_cases=9 depth_score=9`. The actual ledger rows remain at `tools/mutate-and-run.sh:87-95`.

Executed C at the target:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git show bb681566b18211adf8ae9c28df91e17678e3f545:SHONEN.md | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
```

Observed:

```text
boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8
```

An initial transcription of C had an extra closing parenthesis and failed with `SyntaxError: unmatched ')'`; the corrected command above produced the stated census. That was a review-command error, not a runner defect. The observed upper bound of 8 does not override measured restraint 6.

### 4. Bounds on the other axes

- **Operability:** `tools/mutate-and-run.sh:1432-1463` preserves the three status buckets and existing FAIL/SETUP decisions, adding the mismatch guard before PASS. `:1994-2006` extracts the real block and executes it with Bash; `:2008-2039` supplies the fixed vectors and guard stress case. The nine-leg assumptions are real maintenance coupling, explicitly disclosed in `corpus/knowledge/regression-tally-completeness.md:64-67`, not a current loss of depth. The retained supporting receipt `.ufo/evidence/round-30/v4/head.stdout:1,59-61` reports pristine exit 0, `harness=19/19`, `refused_drops=9/9`, the finite kill/rewrite results, and predicate true. It is supporting evidence only: amendment 4 (`.ufo/evidence/round-30/contract-amendment-4.json:9,19-27`) expressly removes a numeric C1 target. A predicate pass cannot discharge calibration harm.
- **Coverage:** `corpus/README.md:449-456` identifies existing Core ground and says no frontier row changes status. `corpus/knowledge/regression-tally-completeness.md:23,64-67` excludes actual leg replay and universal detector coverage. Neither 97 → 106 selftest assertions nor 89 → 92 source rows is an expertise-score delta.
- **Freshness:** `corpus/SOURCES.md:101-103,357-364` distinguishes the superseding anchor from new mined sources and records S087's used-by change without replacing its historical row. The retained census ends `ok`, `exit=0`, while retaining the S092 duplicate-URL warning (`.ufo/evidence/round-30/head/census-at-bb681566.stdout:8-10`). The monitor explanation records 92 rows and zero malformed rows (`:2332-2338`). I did not independently reopen those external sources; this is a review of the committed correction and receipts, not a fresh live-source verification.
- **Adjacency and provenance:** `PROVINCE.md:14-20,28-47` retains local-runner ownership and report-only sibling boundaries. The new entry explicitly denies that S087 requires the runner's refusal policy (`corpus/knowledge/regression-tally-completeness.md:17,25-31`) and denies a measured security-boundary claim for S093 (`:68`). No general two-lane claim, frontier closure, or retirement follows from this local fix.

## Smallest safe correction

1. Preserve the harmed observation exactly as measured. Do not describe `bb681566…` as no-harm, replace restraint 6 with checkbox upper bound 8, or carry a later result backward to it.
2. Complete the already assigned two independent fresh cold reads for each of the 31 drifted sections at `bb681566…`; retain failing outcomes without normalization. L1 alone appends the actually bound entries, preserving the historical ledger prefix. Dispatch count or report existence is not credited coverage.
3. After assembly, the main integrator records the strict monitor at the actual committed landing revision. Only an observed `covered=64/64 restraint=8 box3_mismatch=0`, without overrides and with required bindings intact, repairs this numeric no-harm deficit. Partial restoration remains partial; any intervening input edits require their own applicable reads. This critic does not presume the wave will pass.
4. Keep C1 exploratory and its supporting predicate separate from that restoration. No production-code expansion or ruler rewrite is needed to address the counterexample. If restoration fails, report the remaining harm for the canonical judge rather than treating operability gains as compensation.

Tools installed or updated: none. No seats spawned, production files edited, lane Git writes, `jj` commands, gates, selftests, or sweeps were run by this seat. Counting commands ran in `/tmp/tameshi-CriticNoHarm.NZctbQuG/repo` with Git context variables unset; that scratch clone was removed. All launched commands completed; no service or background process remains from this review.
