author: hyaku closure (non-author integrator, @m_strong)

# Round 13 — non-author closure and discernment spot-check

Date: 2026-10-20. Lane: tameshi. Before: `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`; delivered: `7dd16d9bdd15ef64228297e76e3b1bee690efde8`; executable/content measurement: `4acc607dfd79f19d508bd50cdd06b77269fccd1d`.
Report: fleet `.ufo/reports/round-13/tameshi.md@bf51124e140372251f7b90b6fd5235266d81ca34`.

**Closure: status ok; admitted true.** C1 depth improved through structured content-disposition capability and sourced detail; C2 calibration improved through checked provenance correction and producer repair. All scalar scores remain 6; no axis harmed. Neither claim is exploratory. This admits neither full F7 verdict reuse, a successor mutation sweep, a seventh case, blind preregistration, nor promotion.

## Step-1 conformance

Commands used absolute lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin` and fleet root `/home/vgpnk/Projects/shokunin`.

- Fleet `git log --format='%an %H' -- .ufo/reports/round-13/tameshi.md` returned `tameshi-shokunin bf51124e140372251f7b90b6fd5235266d81ca34`. `git show -s --format='%H%n%an <%ae>%n%aI%n%cI'` reports lane identity and report time `2026-10-20T02:05:01-03:00`, after delivered lane commit `2026-10-20T02:03:44-03:00`, also lane-authored.
- `git merge-base --is-ancestor HASH HEAD` exited 0 for every full report-cited lane commit: before, measured-content, and delivered hashes above. Report contains real landed work, LOG links, all required sections, and four `[~]` SHONEN lines: not a marker.
- Before this note, lane `git status --porcelain` returned no lines; `git rev-parse HEAD` returned delivered hash; `git rev-list --count '@{u}..HEAD'` returned `0`. Independent closure reviewer also read remote master at delivered hash. No uncommitted round work was inherited or modified by closure.
- Prompt is committed (`a53aad815114854271cc3b50111d67153cfd200d`, lane identity). Independent Python rendering of fleet `templates/round-prompt.md` with the actual lane, round, root and axes produced an **exact prefix** of the dispatch prompt. Sections 1–5 include the operative contract, five child-lane items, frontier, commit/push, scope and L0 duties. Campaign addendum explicitly assigns canonical planner to L1; host routing, not historical advisory bucket labels, supplies model selection.
- Committed wave evidence: `dispatch.json counts={spawn:32,resume:0,total:32}`; 32 registry members and 32 retained seat `.md` reports. Roles: executor3/scout6/reviewer8/critic6/connector3/scribe2/sentinel2/revenger2. `taskCall.tasks` has 32 entries and zero model fields. Validator/task receipts are inspected, not re-executed. Relative `Report:` trailer debt remains disclosed; no historical payload was rewritten.
- History pin independently verified: `sha256(json.dumps(rounds[:48],sort_keys=True,separators=(',',':')).encode())` equals `ce97497ed699a8f0939be062d042cf4d6e3e7531116fbe4681593991d67f0a8e` for both current MANIFEST and `git show ae19fca:MANIFEST.json`. Default JSON ASCII escaping is significant. No prior hyaku tameshi r13 closure existed before append.

Conformance: **not fully conformant**, for the status-neutral routed items below. No defect turns this substantive report into a marker or falsifies its two bounded claims. This closure does not claim the operator's append helper is the complete frozen step-1/status checker required by canonical protocol.

## Independent before → delivered measurements

These are plain counts and SHA-256 comparisons of committed bytes, **not executions of lane gates, selftests, mutation runners or measure.py**. The following Python procedure was run in the closure session; observed values follow. Lane-relative paths below resolve under the absolute lane root.

```python
import collections, hashlib, json, re, subprocess
lane = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
before = '546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50'
after = '7dd16d9bdd15ef64228297e76e3b1bee690efde8'
base = '.ufo/evidence/round-13/'
def blob(rev, path, repo=lane):
    r = subprocess.run(['git','-C',repo,'show',f'{rev}:{path}'],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None
def obj(path):
    return json.loads(blob(after, path))
for rev in (before, after):
    rows = [list(map(str.strip, line.split('|')))
            for line in blob(rev,'corpus/SOURCES.md').decode().splitlines()
            if re.match(r'^\|\s*S\d{3,}\s*\|', line)]
    gates = re.findall(rb'^#   (?:js|bash)-\S+\s+(\S+)\s+\d+/\d+',
                       blob(rev,'tools/mutate-and-run.sh'), re.M)
    marks = re.findall(r'^- \[([x~ ])\] ',
                       blob(rev,'SHONEN.md').decode(), re.M)
    print(rev,
          [int(blob(rev,p) is not None) for p in
           ('tools/pin-disposition.py','tools/witness-metadata.py',
            base+'witness-metadata.json')],
          len(gates),len(set(gates)),
          2*sum(marks[i-1]=='~' for i in (1,2,4)),
          len(rows),dict(collections.Counter(r[4] for r in rows)),
          dict(collections.Counter(r[8] for r in rows)),
          sum(len(r)!=13 for r in rows),
          hashlib.sha256(blob(rev,
            '.ufo/evidence/round-12/BashWitness/summary.json')).hexdigest())
expected = obj(base+'expected.json')
print('input digests',len(expected['inputs']), 'mismatches',
      [p for p,h in expected['inputs'].items()
       if hashlib.sha256(blob(after,p)).hexdigest()!=h])
counts = collections.Counter()
for leg in obj(base+'pin-dispositions.json')['legs']:
    repo = '/home/vgpnk/Projects/shokunin/'+leg['repo']
    p = leg['path']
    pin = hashlib.sha256(blob(leg['pinned']['commit'],p,repo)).hexdigest()
    head = hashlib.sha256(blob(leg['head']['commit'],p,repo)).hexdigest()
    counts['unchanged' if pin==head else 'changed'] += 1
    print(leg['leg'],
          pin==leg['pinned']['expected_sha256']==leg['pinned']['blob_sha256'],
          head==leg['head']['blob_sha256']==leg['worktree']['sha256'],
          leg['result_reuse'])
print('content states',dict(counts))
```

| Observable | Before observed | Delivered observed | Judgment |
|---|---|---|---|
| C1 pin probe artifact | 0 | 1 | agrees |
| C2 checker / companion | 0 / 0 | 1 / 1 | agrees |
| Recorded cases / unique recorded gates | 6 / 6 | 6 / 6 | unchanged |
| Calibration restraint, boxes1/2/4 only | 6 | 6 | unchanged; not promotion authority |
| Source rows / malformed | 44 / 0 | 46 / 0 | agrees |
| Source tiers A/B/C | 37/5/2 | 39/5/2 | agrees |
| Source statuses mined/queued/rejected | 15/26/3 | 19/24/3 | agrees |
| Frozen summary SHA256 | `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` | identical | preserved |

Expected-input digest observation: **13 inputs; mismatches=[]**. The original `verification.json` records 12 measured-input digests, all independently matched; the later oracle's digest is additionally pinned in `expected.json` and `producer-oracle-repair.json`.

### C1 — remeasured content, evidence-verified execution

All six historical pin blob digests and all six **recorded observation-time HEAD** blob digests matched retained values. For every leg, recorded HEAD digest also equals recorded worktree digest. Re-derived classifications:

| Leg | Content state | Pin / recorded HEAD hash checks | Reuse |
|---|---|---|---|
| js-kimi-census | changed | true / true | not_established |
| bash-surface-census | unchanged | true / true | not_established |
| bash-tsukuroi-census | changed | true / true | not_established |
| bash-mado-verify | changed | true / true | not_established |
| bash-checklist-run | unchanged | true / true | not_established |
| js-claims-check | unchanged | true / true | not_established |

Observed **changed3/unchanged3/unavailable0** agrees. These are historical recorded HEADs, not a claim that siblings cannot advance after the sequential reading window ended at `2026-10-20T04:59:26Z`. Mado subsequently acquired its own closure-only commit; that does not invalidate its earlier recorded blob. Independent DepthEvidence reviewer also checked manifest PIN/REV/path mappings against unchanged runner constants; all six match.

`verification.json` retained `pin_selftest` exit0 and final line `SELFTEST: PASS (18/18)` with 18 successful case lines. Probe executable SHA `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` matches committed expected values and disposition receipt. Runtime capability is **evidence-verified, not rerun**. Modes, runner/spec, command/harness, toolchain, environment, dependencies, fixtures and timeouts are explicitly not compared. Configured manifest authority is not adversarial baseline authentication.

**C1 depth improved**, scalar6 unchanged. The new structured method did not exist before; old manual six-row pin readings did. Neither a date-named absence nor the constant reuse label is counted as the improvement.

### C2 — remeasured semantic delta, evidence-verified red/green

Independent JSON comparison found exactly one companion delta: `/declaration/kind`, null → `declared-witness mapping (not a blind preregistration)`. The frozen declaration top-level kind matches exactly; its original nested field remains null in both canonical and rerun summaries. No exposure disclosure is removed.

Retained `verification.json` observations:

- `metadata_selftest`: exit0, `SELFTEST: PASS 39/39`; reviewer counted 39 matching unique fixture cases without running them.
- `metadata_old_null`: exit1, `metadata_inconsistent`, `normalized_kind_null`.
- `metadata_corrected`: exit0, `metadata_consistent`, `ok`, verified sources `summary,declaration,declared,rerun_summary`.
- `metadata_emit` matches the corrected companion semantically.
- Witness check/count remain historical clean evidence: 96 files, ten classifications8/0/2/0, denominator16=14 exercised+2 skipped. This is not a new target execution by closure.

`producer-oracle-repair.json` retains the same oracle SHA `d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b`: before exit1, `WITNESS_SELFTEST: 40/41 pass`, exact assertion `summary preserves top-level exposed declaration kind FAIL`; after exit0, `41/41 pass`, same assertion `ok`. Independent textual diff between retained `producer-before.py` and delivered producer shows **only** nested `declaration.get("declared", {}).get("kind")` → top-level `declaration.get("kind")`; the new regression assertion is identical in both variants. This discriminates the root cause, unlike the explicitly superseded initial path-layout crash.

The historical producer SHA `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a` resolves to baseline producer bytes. It is explicitly marked historical/checked_live=false in the companion. Current producer SHA `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80` is separately pinned. Checker lines478–518 bind exact covered canonical path/hash/field and uncovered rerun path/hash/disposition; final canonical-companion equality rejects extras. These explicit scope/identity declarations defeat suggestions that the companion silently claims a live old producer or normalizes every rerun.

**C2 calibration improved**, scalar6 unchanged. Gate execution is **evidence-verified, not rerun**; static semantic/digest/source comparisons were performed independently. Original frozen bytes remain historical.

## Per-axis verdicts and harm check

Executed `git diff BEFORE DELIVERED -- SCORECARD.md`: 67 insertions, no deletions; two capability rows and appended round13 measurements, not scalar inflation. Static `git diff --name-only BEFORE DELIVERED -- .ufo/evidence/round-12` returned no paths; runner and SHONEN byte comparisons each returned true. Spot reads covered SKILL decision table/registry, QUALITY14, source corrections, knowledge scope, README frontier and lesson mistakes.

| Axis | Verdict | Evidence / bound |
|---|---|---|
| depth | improved | C1 structured method, six independently re-derived blob comparisons and source-backed omitted-input detail |
| calibration | improved | C2 kind-only red/green, producer root repair, preserved disclosure and QUALITY14 |
| coverage | unchanged | F7 prerequisite advances; complete reuse-decision frontier remains open |
| operability | unchanged | existing runner unchanged; no extra independent axis claim |
| freshness | unchanged | successor mutation sweeps remain open; content observation is not their discharge |
| adjacency | unchanged | sibling reads only, no product-gate ownership absorbed |

## Discernment spot-check

Reopened on 2026-10-20 by this non-author integrator and independent closure reviewer SourceDiscernment, not by the lane. URLs were read directly; reviewer also observed served bytes matching the recorded page digests. Gate rejections are **claim-level**, not new rejected-source rows; the required admit/reject sample is from the round's actual Gate decisions.

| Item | Lane decision | Re-opened source | Judgment | Reason |
|---|---|---|---|---|
| Bounded F7 method: content equality is not reusable verdict proof | admit | S003 https://stryker-mutator.io/docs/stryker-js/incremental/, Limitations; PIT https://pitest.org/quickstart/incremental_analysis/, dependency paragraphs | agree | S003 explicitly excludes environment/dependency changes; PIT calls its assumption unproven. Lane labels the transfer to pin granularity as inference. |
| Unchanged SHA establishes safe verdict reuse | reject | Same S003 Limitations and required dry-run text; same PIT dependency qualification | agree | One gate-file hash does not establish the tested/dependency/environment inputs required by those scoped methods. |
| Current pin closes successor mutation re-sweeps | reject | `tools/mutate-and-run.sh` committed replay ledger and `knowledge/incremental-pin-disposition.md` §§3–4, with ER-3 ledger distinction | agree | A content-only observation neither executes control/mutants nor creates a new outcome table. |
| Normalization makes exposed declaration blind | reject | Digest-pinned `round-12/BashWitness/declaration.json`, companion disclosure and kind | agree | Exposure cannot be undone by adding metadata; blind=false remains checked. |
| S048 new correction row | admit, object-neutral precision only | PIT numbered item4 and item5; lesson Source precision addendum | agree | Exact quote “it should therefore be prioritised above others” is **7 words** (≤25), present in item4; item5 explicitly says “not yet implemented”. No pronoun resolution or new URL is claimed. |

Additional new-row quote check: S047 lesson Gate quote “With the exception of 4), all these optimisations introduce a degree of potential error into the analysis.” is **17 words**, verified after PIT's numbered list. S003 quote is17 words; dependency-assumption quote9 words. Both new rows are append-only corrections to the same existing PIT URL, not two newly discovered sources. S048 explicitly supersedes intermediate object-specific S047 wording.

Executed required census:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Observed exit0:

```text
tameshi W04 S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi W04 S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Output is tab-separated; spaces above are rendering only. W04 warnings are intentional correction-row duplication, not suppressed errors.

## Learning trends

- **expansion improved** — one new provenance-headed knowledge entry on formerly uncovered F7 prerequisite ground; mined S003/S041/S047/S048 support it, README round13 row indexes it, and demonstrated capability enters SCORECARD. No growth credit for duplicate URL correction rows, new kill rate, or full F7 completion.
- **quality improved** — null-kind weakness becomes a checked additive companion and exact producer regression; frozen evidence remains intact; PIT overbreadth is qualified by visible corrections. Deferred pre-integration prose and stale expected-row debt below are disclosed, not false current result claims.
- **discernment improved** — this outside sample agrees on admits and rejects; prior outside defect3 becomes grounded QUALITY14, with the same checker rejecting old-null and accepting kind-only repair. Lane-dispatched seats are not counted as outside authority.

## Routed defects and residuals

All items below are status-neutral and do not falsify C1/C2. Fixes belong in the owning next round as append-only corrections/new evidence, never by rewriting this round's filed history.

1. **Tameshi, next-round evidence contract:** `expected.json expected_checks.producer_before` still asks the initial relocated command to contain the exact kind assertion, while that raw run crashed before it. The explicit supersession in `verification-verdict.json` and `producer-oracle-repair.json` is valid proof and was used here, but a naive reader applying every stale expected row sees a mismatch. Add a clearly effective/superseded expectation disposition or replacement receipt in new evidence. Do not erase the initial failure or call exit_matches alone mechanism proof.
2. **Tameshi, next-round environmental receipt:** the claimed GIT_DIR-poisoning check retains identical argv and no injected-env field. Static code scrubbing and equality of retained JSON are visible, but the precise poisoning setup is not durably recorded in that row. This closure verifies equality, not the omitted setup. Record bounded injected variable names/values or a reproducible non-secret setup if claiming that experiment again. Also retain explicit manifest-versus-runner mapping results rather than requiring reader reconstruction (the independent reconstruction here passed).
3. **Tameshi, next-round reading clarity:** knowledge §6 is explicitly a pre-integration/deferred-at-write account, while report/lesson/README carry final receipts. Add a later empirical backlink/correction in future knowledge maintenance; do not let that dated section be mistaken for present absence. Prefer newest S048 wording in future guidance; leave disclosed superseded S041/S047 history intact. S003 source cadence180d versus combined-entry90d is a deliberate stricter entry cadence, not a contract violation.
4. **Operator/protocol:** retain relative seat-Report trailer correction in the actual validated future context/body, not just outer instructions. Preserve the committed-evidence non-execution closure contract. The authorized append helper serializes and validates entries but is not the full canonical frozen closure checker; this remains orchestration conformance debt, not a tameshi marker predicate.
5. **Tameshi carried debt:** full current-page SKILL cold-read/box3, legacy provenance headers, F1 interop, successor mutation sweeps (kimi/tsukuroi/mado) and runbook corrections remain open. All SHONEN boxes are **not** independently checkable yet; no promotion recommendation and no SHONEN edits.

Review integration: three fresh read-only closure reviewers inspected C1, C2 and sources. Their finite-coverage/test-extension suggestions are advisory, not proof that the checked bounded capability fails. A calibration reviewer proposed fixing lane bytes before closure; closure has no such authority, and the explicit superseded failed setup is excluded rather than silently graded green. Historical producer identity and exact observation scope were independently re-opened in the checker and companion; no new live-identity or whole-rerun-normalization claim is admitted.

## Dispatch/completion digest

Durable copy of the prompt-supplied driver evidence:

```text
2026-10-20T01:43:27-03:00 launch tameshi round=13 pgid=1470633 driver=hyaku-inline attempt=1
2026-10-20T02:05:14-03:00 complete tameshi round=13; hyaku-inline attempt=1
```

Tool installs/updates: none by this closure or its reviewers. No lane-authored file, SHONEN mark, promotion or mint changed. Closure writes only this required note and the temporary authorized ledger-entry input; helper owns MANIFEST append/commit/push.
