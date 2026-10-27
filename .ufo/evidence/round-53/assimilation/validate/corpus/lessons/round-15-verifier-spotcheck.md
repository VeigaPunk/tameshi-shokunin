author: hyaku closure (non-author integrator, @m_strong)

# Round 15 — non-author verification and admit/reject spot-check

Date: 2026-10-20. Lane: tameshi. Baseline `a9cf4da78f2514c7bedd91a850a88590009d7df0`; delivered `9f2c86ffdc8069a194fafee37865d299903fd0a5`; runtime-measured revision `7650fe4db89f3a706aed63d048ac47e02289cc72`. Fleet report `.ufo/reports/round-15/tameshi.md`, commit `800cf862e54b94b8b71652a8764c0437ce3c98f7`.

**Status: ok. Admission: admitted.** C1's bounded calibration capability verifies, scalar6→6; no axis is harmed. Structural counts and byte pins were independently re-measured. Gate/selftest/frozen-run behavior was **evidence-verified, not rerun**. Neither this integrator nor the three read-only reviewers executed the lane's gate, verifier, measurement script or selftest.

## Step-1 conformance

Executed commands:

```sh
git -C /home/vgpnk/Projects/shokunin log -1 --format='%an <%ae> %H %aI' -- .ufo/reports/round-15/tameshi.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff a9cf4da78f2514c7bedd91a850a88590009d7df0 9f2c86ffdc8069a194fafee37865d299903fd0a5 -- SCORECARD.md
```

Observed report author `tameshi-shokunin <tameshi@shokunin.local>`, report commit above, time `2026-10-20T05:51:25-03:00`; lane porcelain empty before closure writes; ahead count0. SCORECARD diff:71 insertions/0 deletions, adding one capability and the round's bounded accounting, without scalar inflation. Delivered lane commit time `2026-10-20T05:49:33-03:00` precedes the report. All five round-work commits have the lane identity. Historical push-before-report ordering is report-attested; current pushed state was directly checked.

Independent Python extracted every full40-hex report commit and ran `git cat-file -e HASH^{commit}` and `git merge-base --is-ancestor HASH HEAD`: both exited0 for all six, namely baseline `a9cf4da…`, `bca5deb2f61f4235d7f5baac71219c55459f29b5`, `0494c2442a7aab924d4c55e879ffb4b8d676ccd0`, `b2550559b495e622f537877c7999bb3899da30c8`, measured `7650fe4…`, and delivered `9f2c86f…`.

The report is real committed work, not a marker. All six required sections appear in order; SHONEN has four `[~]` lines. The committed prompt's first140 lines exactly equal the committed `templates/round-prompt.md` after substituting LANE=tameshi, ROUND=15, FLEET_ROOT, AXES and `<tameshi-repo>`; Python `prompt.startswith(rendered_template)` returned True. Prompt commit: `d8aff65d8fcd53fd7bfaf8238bb9d76728bafc2d`. The host addendum explicitly assigns canonical planner to L1; no unvalidated planner spawn is required. MISSION's route buckets are advisory; routing changes are operator-attributed rather than a lane routing mutation.

### L2 floor — ten quota failures do not erase dispatch, but do erase credited work

Independent stdlib JSON parsing of committed `spec{1,2}.json`, `dispatch{1,2}.json` and `failures.json`, with committed Markdown-path census, reproduced:

| Wave | Dispatched / credited completed | Role mix dispatched | Reports |
|---|---|---|---|
| Build |66 /56|executor19, scout13, connector2, reviewer12, critic8, sentinel4, revenger4, scribe4|57, including one uncredited partial|
| Falsify |32 /32|executor1, connector2, reviewer10, critic10, sentinel4, revenger1, scribe4|32|
| Round |98 /88|No replacement identities|89, not89 successful reviews|

`spawn1.json`/`spawn2.json` corroborate one batched call each. All98 task payloads lack a model key and start with `/skill:godspeed`. The ten failures are nine scouts (ReconMapping, ReconTamper, ReconMismatch, ReconUnavailable, ReconControl, ReconJSON, ReconClean, ReconUsage, ReconTypes) and connector SiblingOverlap. Build's surviving roles are executor19/scout4/connector1/reviewer12/critic8/sentinel4/revenger4/scribe4. Its remaining scouts are SourcePrimary, ReconTimestamp, ReconEnvironment, ReconNames; its connector is PlannerDataWalk. `replacement_identities` is empty.

**Numerical L2 floor holds in wave1 alone:**66 dispatched, even56 completed exceeds8. The contractual concurrency bands are dispatch bands:66 fits64–100,32 fits32–64, total98≤128. Do not invent an additional64-successful-completions rule or count failed/partial reports as completed work. The required scout count also survives. L1 planner mapping is expressly authorized.

**Functional conformance debt remains:** the named connector sibling-overlap scan has no credited completed output. SiblingOverlap.md is partial, not a successful verdict; PlannerDataWalk is a bounded planning supplement, not that scan. Wave2's RetainedVsLive and FrontierBoundary are not replacements for it. Route the missing scan to tameshi next round. This does not make the real report a marker or falsify C1. Retained timestamps are consistent with build-before-falsify, but failures.json has no per-failure timestamps; exact completion/retry timing is not independently established.

## C1 — independent before → delivered measurements

Executed Python through the evaluation tool, using only standard-library parsing/hashing and read-only git subprocesses, not lane-owned scripts. Core counting expressions:

```python
import collections, hashlib, json, re, subprocess
root = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
def git(*a): return subprocess.check_output(['git', '-C', root, *a])
def blob(r,p): return git('show', r + ':' + p)
for r in ['a9cf4da78f2514c7bedd91a850a88590009d7df0',
          '9f2c86ffdc8069a194fafee37865d299903fd0a5']:
    paths = set(git('ls-tree','-r','--name-only',r).decode().splitlines())
    skill = blob(r,'SKILL.md').decode()
    tool = blob(r,'tools/context-capture.py').decode() if 'tools/context-capture.py' in paths else ''
    rows = []
    for line in skill.splitlines():
        c = [v.strip() for v in line.strip().strip('|').split('|')]
        if line.strip().startswith('|') and len(c)>=8 and c[1].strip('`*_ ').lower() in ('gate','probe'):
            rows.append(c)
    ctx = [c for c in rows if 'tools/context-capture.py' in c[2]]
    gate = int(bool(tool) and any(c[1].strip('`*_ ').lower()=='gate' for c in ctx)
               and not any(c[1].strip('`*_ ').lower()=='probe' for c in ctx))
    standalone = int('--selftest' in tool and 'SELFTEST: PASS' in tool)
    classes64 = sum(any(re.search(r'64[^;|]*could-not-evaluate',c[3]) for c in rows if name in c[2])
                    for name in ('tools/context-capture.py','tools/evidence-disposition.py'))
    src = [l.split('|')[1:-1] for l in blob(r,'corpus/SOURCES.md').decode().splitlines()
           if re.match(r'^\|\s*S\d{3,}\s*\|',l)]
    marks = re.findall(rb'^- \[([x~ ])\] ',blob(r,'SHONEN.md'),re.M)
    print(gate, standalone, classes64,
          len(re.findall(rb'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+',blob(r,'tools/mutate-and-run.sh'),re.M)),
          2*sum(marks[i-1]==b'~' for i in (1,2,4)), len(src),
          dict(collections.Counter(c[3].strip() for c in src)),
          dict(collections.Counter(c[7].strip() for c in src)))
```

Observed values agree with the report and extend its count to final delivery:

| Observable | Before | Delivered |
|---|---:|---:|
| Maintained gate actively classified as gate |0|1|
| Standalone selftest artifact (structural only) |0|1|
| Explicit64 classes across two active gates |0|2|
| Recorded mutation cases / restraint score |6 /6|6 /6|
| Source rows / malformed |48 /0|49 /0|
| Tiers A/B/C |41/5/2|42/5/2|
| Status mined/queued/rejected |21/24/3|22/24/3|

Independent `git ls-tree -r REV -- .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14` blob-map comparison:599→599 paths, changed/missing0, added0. Runner, frozen summary, PROVINCE, SHONEN and prior non-author note are byte-identical. Runner SHA256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; summary `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`. New source ID is exactly S051; only existing source-cell change is S049 used-by adding `corpus/lessons/round-15.md`, logged in the Gate. Added knowledge paths: none.

## C1 — committed execution evidence, not a rerun

`verification-3.json`: requested7650fe4, passed=true, failed_checks=[],44 checks with passed=true. `attempt-3/expected.json` resolves the same revision. Independently hashing its five source bindings (including prefix source at bca5deb) plus six frozen expected/receipt files finds **11/11 matches at measured7650fe4 and11/11 at delivered9f2c86f**. Maintained source SHA256 is `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726` at both. Frozen expectation files already exist in b255055, before the successful measured revision. The final SKILL delta only points from the first failed receipt to the effective third receipt; production tool/frozen bytes are unchanged.

| Retained invocation/evidence | Observed result |
|---|---|
| Same temporary `<scratch>/lane/tools/candidate.py --selftest`, old versus maintained source |64 unsupported →0;49 unique successful case lines; `SELFTEST: PASS (49/49)`|
| Actual registered `tools/context-capture.py --check --json` |0/context_consistent, built-in receipt digest and expected-verdict match true|
| Explicit frozen clean / missing environment |0/context_consistent;1/missing_injected_environment|
| Edited snapshot |2/snapshot_tampered; expected_verdict_match=false; unavailable precedence retained|
| Invalid invocation / recognized flag consumed as value |64; raw terminal stderr `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`|
| Same mapping fixture and literal mapping_mismatch/1 oracle |Prefix id expected_verdict_mismatch/1 fails oracle; final mapping_mismatch/1 passes oracle|

Forty receipt fixtures, seven usage fixtures and two meta checks total49, not whole-domain or all-input hermeticity. Digests are configured integrity, not author authentication; replay does not execute retained argv. The registered-path frozen command and copied-path selftest are distinct, honestly described observations.

Failed history remains intact: verification.json at0494c244 has42/44 passing, failed selftest-new/selftest-new-full-count due copied-tool layout; verification-2.json atb255055 has17/18 passing before missing ID_TOKEN_RE stops integration. These were inspected, never rerun or presented as green. They motivate the committed harness repairs, not production-gate changes.

**New status-neutral receipt-attribution defect:** `verify.py`'s generic first-`id=` extraction captures help text's context_consistent in gate-usage and usage-proof-new. Their `observed_id` fields are wrong. Expected_id is null, so those rows assert exit64 and the separate stderr token `id=usage_error`, not equality to the misparsed field. Raw terminal stderr and public selftest independently support the actual usage_error result. Route extractor correction with a failure-backed fixture next round; preserve the old receipt and append corrected attribution, never rewrite it. This is not a clean-result gate defect and does not invalidate C1's bounded proof.

## Outside discernment spot-check

Reopened on2026-10-20 by this closure and fresh read-only reviewers; these are the lesson's actual claim-level Gate decisions, not invented rejected source rows.

| Item | Decision | Re-opened source | Judgment | Reason |
|---|---|---|---|---|
| Public isolated CLI selftest, literal finding/exit pins |admit|Maintained source SelftestHarness/check_case; verification-3 selftest-new raw stdout|agree|Actual subprocess boundary with literal cases, exit0 and49/49 retained; not helper-only calls.|
| Digest-bound retained verdict replay |admit|run_check ordering; frozen expected/receipt files; registered frozen and tampered checks|agree|Digest precedes interpretation; clean, mismatch and could-not-evaluate stay distinct.|
| Helper-only controls constitute standalone self-invocation |reject|Historical round14 helper controls versus maintained subprocess selftest|agree|A helper call cannot demonstrate the public CLI boundary.|
| One clean finite receipt proves global environment independence, safe reuse or historical authentication |reject|Maintained source scope, SKILL limits, original retained receipt and verification-3|agree|Only retained predicates and configured byte binding are demonstrated; omitted experiments remain omitted.|
| Promotion, current full-page cold-read/box3 or successor sweep inferred from replay |reject|SCORECARD round15, unchanged SHONEN/PROVINCE, SKILL limits|agree|No such task was executed or independently certified by this replay.|
| New S051 own-work scoped quote |admit|`git show bca5deb:tools/context-capture.py`, docstring; identical quoted text in delivered tool|agree|“Check mode writes nothing; the only writes are --selftest fixtures under mkdtemp.” is12 words and exact; check mode is read-only.|
| Re-opened S049 subprocess environment semantics |admit|[Official Python subprocess documentation](https://docs.python.org/3/library/subprocess.html), run() env paragraph, Python3.15.0 as served|agree|“If env is not None, it must be a mapping that defines the environment variables for the new process” is19 words and exact.|

S051's registry anchor gives r15 and line ranges; the lesson additionally identifies the source-opening commit bca5deb. A reviewer preferred an explicit final source commit in the registry. Closure does not treat lack of a commit *in that cell* as a mandatory defect: CORPUS accepts a version, commit **or** publication date, and the exact quote remains true at both revisions. The pre-repair selftest's TMPDIR weakness is not authenticated isolation proof from the quote; it was found, repaired, and independently separated from runtime evidence. Optional: add an append-only superseding source row if the source's final revision needs a sharper anchor.

Required census executed independently:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Exit0, output:

```text
tameshi W04 S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi W04 S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Actual separators are tabs. Existing W04 warnings remain disclosed append-only correction-URL duplication, not errors.

## Per-axis verdicts and learning trends

| Axis | Verdict | Evidence/bound |
|---|---|---|
| calibration |improved|C1 maintained gate, stronger active registry, isolated failure-backed CLI and QUALITY17; scalar6 unchanged|
| depth |unchanged|Six recorded cases; no new target-depth measurement|
| coverage |unchanged|No new knowledge path or whole-F7 completion|
| operability |unchanged|C1 credited once to calibration; runner unchanged|
| freshness |unchanged|No owner-approved current successor sweep|
| adjacency |unchanged|PROVINCE unchanged; retained-receipt craft does not absorb sibling ownership|

- **Expansion: unchanged.** A capability row is added and observable, but it is same-ground retained-receipt work. No uncovered knowledge entry/map ground is gained; one own-work source row is not expansion by itself.
- **Quality: improved.** The weaker, wrongly classified active context entry is explicitly superseded by the maintained gate entry, with standalone public-CLI and byte-pinned frozen evidence that the prior lacked. QUALITY17 is lesson-backed. This is bounded instruction/instrument quality, not a claim of a full knowledge freshness sweep. A reviewer preferred unchanged absent a reverified knowledge entry; closure judges the actual superseded active entry and stronger verified replacement sufficient for LEARNING's weaker-entry supersession, without pretending any knowledge-file timestamp changed.
- **Discernment: improved.** The outside sample agrees on admits and rejects; prior outside defect5 becomes a grounded criterion and discriminating capability. The new receipt-parser disagreement is durably routed below, not silently ignored; its corrective implementation belongs to the next lane round.

## Routed defects and residuals

1. **Tameshi: complete the uncredited sibling-overlap connector function.** Quota deaths do not violate the numerical dispatch floor, but a partial SiblingOverlap report is not the required successful scan. Preserve failed-seat accounting; plan explicit coverage recovery next round without relabeling this round's56 as66 completed.
2. **Tameshi: repair usage finding attribution in the integration verifier.** Parse the actual terminal structured verdict rather than the first help-text id; demonstrate old misattribution and corrected finding with the same fixture/argv. Append a correction naming the two affected receipt fields; retain verification-3.json unchanged. Raw exits and terminal usage_error support the admitted boundary meanwhile.
3. **Tameshi: continue execution discipline.** SpecClean's prohibited mid-flight synthetic checks and SpecMismatch/SpecTypes/SpecEnvironment/SpecMapping probes remain process conformance incidents, disclosed in the lesson. Their transcriptions receive no runtime credit. Integrated L1 receipts, not seat prose, support this admission.
4. **Operator/protocol: inherited closure-checker debt stays open.** The serialized append helper is not the full committed frozen closure-status/history-pin checker required by canonical PROTOCOL. This manual closure does not claim that checker passed or repair operator-owned scripts.
5. **Tameshi: prior bounded residuals stay open.** Current full-page SKILL cold-read/box3, legacy provenance headers, F1 interop, whole-F7 reuse, runbook corrections and owner-approved current-revision kimi/tsukuroi/mado successor sweeps are not completed by receipt replay. Prior defect5's gate classification/standalone selftest/explicit64 corrections are resolved within C1. No promotion recommendation: all SHONEN boxes are not independently certified, especially box3. No SHONEN edit, promotion or mint occurred.

Dispatch/completion digest copied from the closure prompt (mutable driver log, not promoted to an immutable runtime measurement):

```text
2026-10-20T04:58:54-03:00 launch tameshi round=15 pgid=2461314 driver=hyaku-inline attempt=1
2026-10-20T05:51:48-03:00 complete tameshi round=15; hyaku-inline attempt=1
```

Tool installs/updates: none. No credential/auth file, agent database, separate omp process, host service operation or pacman transaction was used. Closure writes only this verifier note and a temporary JSON input to the authorized closure helper; lane-authored files remain untouched.
