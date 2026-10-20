author: hyaku closure (non-author integrator, @m_strong)

# Round 14 — non-author verification and admit/reject spot-check

Date: 2026-10-20. Lane: tameshi. Baseline `d6809df7775338f000e44c8a916067b8866867fb`; delivered revision `13c1367db106066395d245ed9ab7a972943cdd40`. Report: fleet `.ufo/reports/round-14/tameshi.md`, committed as `3fcaaaec50aa46425f24386a43db2bdde28944e0`.

**Status: ok. Admission: admitted.** One declared claim, C1 calibration capability acquisition, verifies within its configured receipt-reconciliation boundary. Calibration improves without scalar inflation (6→6); no other axis is harmed. Static counts and digest/semantic comparisons below were independently re-measured over committed bytes. Gate execution, selftest and context experiment are **evidence-verified, not rerun**. Neither this integrator nor its read-only reviewers executed a lane gate, selftest or context harness.

## Step-1 conformance

Commands executed from the fleet root, with absolute git `-C` paths:

```sh
git -C /home/vgpnk/Projects/shokunin log -1 --format='%an %H' -- .ufo/reports/round-14/tameshi.md
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff d6809df7775338f000e44c8a916067b8866867fb 13c1367db106066395d245ed9ab7a972943cdd40 -- SCORECARD.md
```

Observed: report author `tameshi-shokunin`, commit `3fcaaaec50aa46425f24386a43db2bdde28944e0`; lane porcelain empty before closure writes; ahead count **0**. SCORECARD diff is **85 insertions, 0 deletions**, comprising one capability and appended round14 measurements, not a rewritten scalar baseline.

- Report is real committed work, not a marker; all six required sections occur in order. `## SHONEN` has four `[~]` assessments, matching four boxes. No independent promotion marks were claimed.
- For every full lane commit cited in the report, independent `git cat-file -e HASH^{commit}` and `git merge-base --is-ancestor HASH HEAD` each exited0: `d6809df7775338f000e44c8a916067b8866867fb`, `0c6e36d0bd2fd98077de4cff4c90c6f467c2e1fb`, `64314783836bb0d05ad06a774d7310fd3a23b5bd`, `4d409d796ad8f9bf2aa8d380489da9e7d6cb9ca1`, `13c1367db106066395d245ed9ab7a972943cdd40`.
- `git log --diff-filter=A --format='%an %ae %H %cI' -- REPORT` confirms original report attribution `tameshi-shokunin <tameshi@shokunin.local>`, committed `2026-10-20T03:44:52-03:00`. Delivered lane commit time is `2026-10-20T03:43:12-03:00`, before report commit. All four round-work commits have the lane identity. Historical push ordering is report-attested; current pushed state was checked directly.
- Prompt is tracked by fleet commit `2186c5bf20beddca708e84df290842fa6f7f06e1`. Python `difflib.unified_diff` comparing its pre-addendum text with `templates/round-prompt.md`, after substituting LANE=tameshi, ROUND=14, FLEET_ROOT, AXES and the first-line repo placeholder, produced **no differences**. This covers the full template, not merely heading presence. Host routing remains operator-bound; the campaign addendum names the planner-seat ruling rather than silently removing it.
- Committed dispatch JSON has spawn32/resume0/total32; taskCall has32 tasks and no task-level model keys. Role counts independently parsed: executor3/scout6/reviewer8/critic6/connector3/scribe2/sentinel2/revenger2. The32 markdown seat reports exist at the delivered revision; validated context explicitly resolves every relative Report trailer under the absolute lane root. L1 canonical planner mapping is reported. These committed artifacts corroborate dispatch; they are not independent claim-admission votes.
- Known orchestration debt remains: the authorized append helper is not the canonical committed frozen closure-status/history-pin checker. This manual closure does not assert that such a checker or its history-pin gate passed. The lane disclosed the mid-flight AST/plain-git design control; it does not replace integrated runtime evidence.

## Independent before → delivered measurements

Executed Python via the evaluation tool, invoking only read-only git subprocesses and standard-library JSON/hash/count operations; no lane measurement script was executed. The following reproduces the counting expressions used (absolute repo path, committed blobs only):

```python
import collections, hashlib, json, re, subprocess
root = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
def git(*a):
    return subprocess.check_output(['git', '-C', root, *a])
def blob(r, p): return git('show', r + ':' + p)
def obj(r, p): return json.loads(blob(r, p))
for rev in ['d6809df7775338f000e44c8a916067b8866867fb',
            '13c1367db106066395d245ed9ab7a972943cdd40']:
    paths = set(git('ls-tree', '-r', '--name-only', rev).decode().splitlines())
    exp = obj(rev, '.ufo/evidence/round-13/expected.json')['expected_checks']
    raw = next(x for x in obj(rev, '.ufo/evidence/round-13/verification.json')['checks']
               if x['name'] == 'producer_before')
    ledger = '.ufo/evidence/round-14/dispositions.json'
    rows = obj(rev, ledger)['rows'] if ledger in paths else []
    runner = blob(rev, 'tools/mutate-and-run.sh')
    marks = re.findall(rb'^- \[([x~ ])\] ', blob(rev, 'SHONEN.md'), re.M)
    src = [l.split('|') for l in blob(rev, 'corpus/SOURCES.md').decode().splitlines()
           if re.match(r'^\|\s*S\d{3,}\s*\|', l)]
    print(rev, int('tools/evidence-disposition.py' in paths), len(exp),
          len(set(exp) & {x['name'] for x in rows}),
          dict(collections.Counter(x['state'] for x in rows)),
          raw['exit'], exp['producer_before']['contains'] in raw['stdout'],
          len(re.findall(rb'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', runner, re.M)),
          2 * sum(marks[i-1] == b'~' for i in (1, 2, 4)),
          len(src), dict(collections.Counter(x[4].strip() for x in src)),
          dict(collections.Counter(x[8].strip() for x in src)),
          hashlib.sha256(runner).hexdigest(),
          hashlib.sha256(blob(rev, '.ufo/evidence/round-12/BashWitness/summary.json')).hexdigest())
```

Observed values agree with the report, now measured against the final delivered revision rather than only its earlier content commit:

| Observable | Before | Delivered |
|---|---:|---:|
| Reconciliation artifact | 0 | 1 |
| Original expected keys | 12 | 12 |
| Disposition-name coverage | 0/12 | 12/12 |
| Effective / superseded rows | 0 / 0 | 11 / 1 |
| Historical setup exit / intended assertion present | 1 / false | 1 / false |
| Recorded cases / calibration restraint | 6 / 6 | 6 / 6 |
| Source rows | 46 | 48 |
| Source tiers A/B/C | 39/5/2 | 41/5/2 |
| Source statuses mined/queued/rejected | 19/24/3 | 21/24/3 |

At both revisions, runner SHA256 is `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; frozen summary SHA256 is `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`.

Additional independent JSON comparison: removing `rows` from the paired ledgers leaves identical top-level pins; zipped rows differ **only at producer_before**; its old receipt/check equals its new raw_receipt/raw_check. Original SOURCES rows compare byte-for-byte unchanged; added IDs are exactly S049/S050. `git diff --name-only BEFORE DELIVERED -- .ufo/evidence/round-12 .ufo/evidence/round-13` printed no paths. Runner, SHONEN, PROVINCE and prior non-author closure note each compare byte-identical.

## C1 — remeasured structure; evidence-verified discriminating execution

Committed `.ufo/evidence/round-14/verification-final.json` and `expected-runtime-final.json` both name executable measured revision `64314783836bb0d05ad06a774d7310fd3a23b5bd`. Independently hashing their six pinned source/input paths over both that revision and delivered13c1367 finds **6/6 matching at each**. The checker hash is `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`. Disposition manifest pins all three direct expected/receipt inputs, **3/3 matching**; original expected.json pins thirteen historical inputs, **13/13 matching**.

Retained commands and observed evidence (read, not executed by closure):

| Retained command | Observed result |
|---|---|
| `python3 tools/evidence-disposition.py --selftest` | exit0;34 unique successful case lines; final `SELFTEST: PASS (34/34)` |
| Same checker, `--root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json` | exit1; expected12/effective12/pass11/fail1; exactly producer_before/expected_contains_missing |
| Same checker, repaired `dispositions.json` | exit0; expected12/effective11/pass11/superseded1; findings0; superseded raw_expectation_failed=true and raw expected_contains_missing retained |

Thus the measured obligation closure is **11/12→12/12**, not twelve newly passing historical experiments. Both oracle replacements remain effective and checked. `verification.json` retains the initial failed selftest; the final receipt does not erase it. The independent source reviewer inspected the two source-diff hunks between0c6e36d and6431478: missing GAMMA_OK fixture construction and JSON-brace formatting only, not production predicates or literal expected finding IDs.

SKILL.md round14 registry declares C1's entry command, selftest, pinned values, write scope and owner. Its0/1/2 classes are explicit;64 is labelled only “usage”, which needs an explicit could-not-evaluate class next round. S050 is properly A/own-work under canonical CORPUS.md's explicit allowance for the lane's own re-runnable gate output. Configured pins are not author authentication or a claim that recorded argv was re-executed. No exploratory claim is present.

Independent gate review found no discrepancy breaking C1. Additional limits: historical expected.json, producer-oracle-repair.json, producer-oracle.py and verification.json landed together in4acc607 after observation, so these are not independently preregistered oracle expectations. “Checked mechanism” here means matching the retained exact assertion and source-bound receipt, not a blind experiment. The checker enforces a genuinely failed raw predicate and exact replacement identities, but its free-text setup-failure explanation is not itself mechanically proved: closure corroborated the FileNotFoundError by reopening raw stderr. No recorded oracle argv was executed by this closure. These limits preserve scalar6→6 and no promotion credit.

**C1 calibration improved, scalar6 unchanged.**

## Non-claim corrections and no-harm bounds

Prospective `context-receipt.json` retains actual GIT_DIR injection `/nonexistent/tameshi-round14-poison`, baseline GIT_DIR absence, same argv/cwd and equal raw stdout including timestamp. Only top-level observed_at is excluded from normalized comparison. Its plain-git control records0→128, and six mappings have five true checks apiece. `guardrails.json` retains context_setup_positive0/context_setup_recorded, missing-field1/missing_injected_environment, equal-valued variable-name-swap rejection0, historical integrity0. These are evidence-verified finite controls, not a new mutation rate, broad environment independence or retrospective proof of round13's missing setup.

Knowledge §8 and its after-integration backlink visibly supersede deferred-at-write status without erasing §6, use S048 object-neutral PIT guidance and retain historical unknowns. QUALITY15–16 cite the originating mistakes and outside routed defects. Spot reads of those sections, SKILL decision table/registry and SCORECARD's limits reveal no claimed successor sweep, seventh recorded case, new uncovered knowledge area or product-gate ownership.

| Axis | Verdict | Bound |
|---|---|---|
| calibration | improved | C1 explicit checked reconciliation plus grounded QUALITY15–16;6→6 |
| depth | unchanged | no seventh recorded mutation case or new target-depth claim |
| coverage | unchanged | no new covered target surface or whole-frontier completion |
| operability | unchanged | capability credited to calibration once, runner unchanged |
| freshness | unchanged | owner-readiness intake is not an executed successor sweep |
| adjacency | unchanged | province unchanged; sibling reads do not absorb their product gates |

## Outside discernment spot-check

Reopened on2026-10-20 by this non-author closure and fresh read-only source reviewer. These are the round lesson's actual **claim-level** Gate decisions, not manufactured rejected-source rows.

| Item | Lane decision | Re-opened source | Judgment | Reason |
|---|---|---|---|---|
| Complete twelve-row disposition with retained raw failure | admit | round13 expected.json, verification.json and producer-oracle-repair.json; round14 paired ledgers and verification-final.json | agree | All twelve original names retained, only the stale row is superseded, both exact mechanism replacements pass their recorded predicates. |
| Prospective context receipt is evidence only of its documented experiment | admit | context-receipt.json environment/invocation/comparison/positive_control; S049 [Python subprocess docs](https://docs.python.org/3/library/subprocess.html), run() env paragraph | agree | Explicit override and non-vacuous control are retained; documentation does not retroactively prove omitted setup. |
| Exit agreement alone proves intended regression | reject | round13 producer_before raw receipt and original expected contains marker | agree | exit1 agrees while stdout lacks the named assertion; FileNotFoundError occurs before the intended mechanism. |
| Drop an inconvenient historical expected row | reject | paired ledgers and original expected key set | agree | Explicit raw retention and checked replacements are required; removing a row would not account for the original obligation. |
| Infer broad environment independence or safe reuse from one GIT_DIR injection | reject | context-receipt.json not_compared/result_reuse; [Stryker incremental Limitations](https://stryker-mutator.io/docs/stryker-js/incremental/) | agree | A single bounded override cannot discharge unmeasured environment/dependency/suite/fixture inputs. |
| S050 scoped source declaration | admit | tools/evidence-disposition.py:10–13, measured6431478 and delivered source digest | agree | The source explicitly limits itself to retained receipt declarations and does not execute receipt argv. |

New-row quote checks: S049 live docs served Python3.15.0 and contain verbatim **“If env is not None, it must be a mapping that defines the environment variables for the new process”** in the run() env paragraph, **19 words**. S050 docstring lines10–11 contains **“It never executes receipt argv.”**, **5 words**, with a line wrap. Both meet≤25 words and ground their scopes. Reopened S003 Limitations contains **“Any other changes to your environment are not detected”**,9 words. No external page is used to prove the lane's recorded execution.

Required census executed independently:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Observed exit0, tab-separated output:

```text
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

W04 warnings are disclosed append-only correction-URL duplication, not suppressed census errors.

## Learning trends

- **expansion unchanged** — same-ground capability and additive existing-entry corrections; two source rows do not create uncovered knowledge or whole-F7 completion.
- **quality improved** — stale effective-expectation accounting and deferred empirical reading receive checked additive corrections, preserving original failure and superseded history; no sampled admitted entry fails its bounded recheck.
- **discernment improved** — this independent sample agrees on admits and rejects; prior independent closure's stale-expectation/missing-setup disagreements become lesson-backed QUALITY15–16 and failure-backed discrimination. This is not a general out-of-sample detection-rate claim.

## Routed defects and residuals

1. **Tameshi prior routed items1–3: addressed within their bounded scopes.** Explicit checked supersession repairs the stale effective account; prospective environment/mapping provenance supplies a new documented experiment while leaving historical setup unproven; empirical knowledge backlink lands additively. Do not relabel those as newly rerun round13 commands.
2. **Operator/protocol: open orchestration conformance debt.** Authorized ledger append remains a serialized validator/commit/push helper, not a full committed frozen closure-status/history-pin checker. Preserve non-execution closure and the actual validated Report-path context correction. This debt does not make real tameshi work a marker.
3. **Tameshi: carry current-page SKILL cold-read/box3, legacy provenance headers, F1 interop, owner-approved current-revision successor sweeps for kimi/tsukuroi/mado and runbook corrections.** Intake refusal is not sweep completion. All SHONEN boxes are not independently checkable; no promotion recommendation or SHONEN edits.
4. **Process disclosure:** one seat's AST/plain-git design check breached the lane's no-mid-flight-check instruction; retained integrated L1 evidence, not that seat check, supports this admission. Preserve the instruction next round.
5. **Tameshi, next round registry/selftest correction:** capture-context.py is labelled a probe, but it compares runner/probe source digests and mappings against committed expected.json/pin-manifest values, and its decide() emits mismatch/exit1. Under §Gate standard this persisted-expectation verdict behavior makes it a gate. Register it as a gate and supply a standalone isolated self-invocation testing exits and stable expected finding IDs; the helper-only missing-field/variable-swap controls are useful evidence but do not satisfy that clause. Also map C1's exit64 explicitly to could-not-evaluate and declare the context harness's64 path (present in source exit map but absent from its registry). These are status-neutral conformance defects in the non-claim context instrument/registry, not a failure of C1 or harm to an existing axis.

No new blocking claim defect was found. Suggested optional source-byte digests are not a mandatory SOURCES-v1 field; A/own-work is explicitly allowed. Neither is routed as a fabricated contract violation. A static count printer such as measure.py is not a verdict gate requiring registry admission merely because it prints counts; not every emitted finding ID needs a separate fixture under the current minimum selftest contract. The actual context-gate classification and explicit exit-class defects above remain routed rather than dismissed.

## Dispatch/completion digest

Durable copy of prompt-supplied mutable-driver evidence:

```text
2026-10-20T03:13:36-03:00 launch tameshi round=14 pgid=2007675 driver=hyaku-inline attempt=1
2026-10-20T03:45:26-03:00 complete tameshi round=14; hyaku-inline attempt=1
```

Tool installs/updates: none. No lane-authored report, scorecard, log, lesson, skill, province or SHONEN mark changed. Closure writes only this note and the authorized temporary ledger-entry input; the append helper owns MANIFEST append/commit/push.
