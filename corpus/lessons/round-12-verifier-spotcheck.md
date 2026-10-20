author: hyaku closure (non-author integrator, @m_strong)

# Round 12 — non-author closure and discernment spot-check

Date: 2026-10-20. Lane: tameshi. Baseline: `18ad5d050ef4bcd830fe513825baed878f025024`; delivered revision: `8742f5dcebf82bb1b57da7d7d2a7dd98a0e5c32e`; measured content: `9df9212d33dc2dbda133e88f28ad47bb08839a5b`.
Report: fleet `.ufo/reports/round-12/tameshi.md@dcc316c77961a373e31c7f3f5e203188aa1f515c`.

**Closure: status ok; admitted true.** C1 calibration improved (capability), C2 depth improved (bounded detail); no axis harmed. Scalar depth/calibration remain 6. This is not promotion, a seventh recorded gate, a blind witness experiment, assertion-level causality, or proof of determinism.

## Step-1 conformance

Commands below used the absolute lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin` and fleet root `/home/vgpnk/Projects/shokunin`; subsequent lane-relative commands run from that lane root.

- `git log -1 --format='%an <%ae> %H %aI %cI' -- .ufo/reports/round-12/tameshi.md` at fleet root returned `tameshi-shokunin <tameshi@shokunin.local> dcc316c77961a373e31c7f3f5e203188aa1f515c 2026-10-20T01:04:25-03:00 2026-10-20T01:04:25-03:00`.
- `git show -s --format='%an <%ae> %H %aI %cI' 9df9212d33dc2dbda133e88f28ad47bb08839a5b 8742f5dcebf82bb1b57da7d7d2a7dd98a0e5c32e` returned lane identity for both, dated 01:01:32 and 01:02:21 -03:00 respectively. Independent conformance review observed origin push at 01:02:23, preceding report mtime 01:04:21 and report commit 01:04:25.
- `git merge-base --is-ancestor HASH HEAD` exited 0 for all three hashes above (baseline plus both report-cited lane commits).
- Before this verifier file was written, `git status --porcelain` returned no lines; `git rev-parse HEAD` returned the delivered revision; `git rev-list --count '@{u}..HEAD'` returned `0`. Independent review also observed remote master at the delivered revision and upstream behind count 0.
- Report has all required sections and four `[~]` SHONEN lines with evidence. It names actual landed work and LOG links: not a completion marker. No `[x]` or lane-authored file was changed by closure.
- Dispatched `.ufo/prompts/tameshi-round-12.md` is committed (`5bbfa4b`). Independent template comparison found sections 1–5 rendered faithfully, including all five child-lane items. The host addendum assigns canonical planner to L1. Current host role aliases are not assigned tiers by the fleet files; their grouping alone cannot prove a routing violation.
- Wave records show 32 + 32 = 64 seats. W1 has 30 retained reports and the two named interrupted seats; W2 has 32. Independent conformance review found no surviving fleet-root copies of their seat reports. The recorded task payloads have no model parameter and include the tooling authorization. Validator approval was not independently re-executed by closure; dispatch files retain taskCall/policy/count evidence rather than a separately labelled approval receipt.
- History pin: canonical SHA-256 of current `MANIFEST.json rounds[:48]` equals `ce97497ed699a8f0939be062d042cf4d6e3e7531116fbe4681593991d67f0a8e`; `git show ae19fca:MANIFEST.json` exits 0 and its canonical prefix hash also matches. No existing hyaku tameshi r12 closure was present before append.

Conformance is **not fully conformant**, for the status-neutral routing items below. None turns this substantive report into a marker or falsifies C1/C2.

## Per-claim counting replay

Re-executed both commands, exit 0 each:

```sh
python3 .ufo/evidence/round-12/measure.py --rev 18ad5d050ef4bcd830fe513825baed878f025024
python3 .ufo/evidence/round-12/measure.py --rev 8742f5dcebf82bb1b57da7d7d2a7dd98a0e5c32e
```

| Observable | Before observed | Delivered observed | Comparison |
|---|---|---|---|
| C1 repeat_control_artifact | 0 | 1 | agrees |
| C2 bash witness summary / classified | absent (`{}`), 0 | complete, 10 | agrees |
| C2 witness/accidental/survived/inconclusive | no study | 8 / 0 / 2 / 0; unresolved=[] | agrees |
| Control slots | no study | denominator16, exercised14, skipped2 | agrees |
| recorded_cases / unique_recorded_gates | 6 / 6 | 6 / 6 | unchanged guardrail |
| calibration_restraint_score | 6 (boxes1/2/4, excluding3) | 6 (same) | unchanged; not fresh promotion authority |
| Source rows / malformed | 44 / 0 | 44 / 0 | agrees |
| Source tiers A/B/C | 37/5/2 | 37/5/2 | agrees |
| mined/queued/rejected | 12/29/3 | 15/26/3 | agrees |

The after replay targets the requested delivered HEAD, not only the intermediate measured-content commit. Summary rows expose B2/B6 generic-only labels and B3's extra `runtime-absent` failure; no dedicated generic-hit JSON field is needed to derive that bounded distinction.

### C1 — verifying demonstrated capability, without executing a sibling gate

Current canonical `PROTOCOL.md` Gate standard, Closure consequence, says the integrator verifies committed selftest/frozen-run evidence and **does not execute a sibling gate**. This overrides the closure prompt's run-now wording. Accordingly **no repeat-control CLI, selftest, pristine bash gate, mutation runner, or sibling gate was executed by this closure**. The following independent read-only replay ran now over git-pinned bytes, not a mutable worktree or target command:

```python
import hashlib, json, subprocess
lane = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
rev = '8742f5dcebf82bb1b57da7d7d2a7dd98a0e5c32e'
base = '.ufo/evidence/round-12/'
def blob(path):
    return subprocess.check_output(['git', '-C', lane, 'show', f'{rev}:{path}'])
receipt = json.loads(blob(base + 'verification-final.json'))
sha = hashlib.sha256(blob('tools/repeat-control.py')).hexdigest()
assert sha == receipt['tool_sha256']
print('tool_sha256=' + sha)
for rel in ('ControlGate', 'ControlGate/mismatch'):
    expected = json.loads(blob(base + rel + '/expected.json'))
    for name, digest in expected['inputs'].items():
        assert hashlib.sha256(blob(base + rel + '/' + name)).hexdigest() == digest
    samples = [(int(blob(base + rel + f'/run-{i}.exit')),
                blob(base + rel + f'/run-{i}.stdout'),
                blob(base + rel + f'/run-{i}.stderr'))
               for i in range(1, expected['runs'] + 1)]
    actual = (('controls_mismatch', 1) if len(set(samples)) > 1 else
              ('baseline_nonzero', 2) if samples[0][0] else ('controls_match', 0))
    assert actual == (expected['expected_id'], expected['expected_exit'])
    print(rel, len(expected['inputs']), actual)
samples = [(int(blob(base + f'replayed-controls/run-{i}.exit')),
            blob(base + f'replayed-controls/run-{i}.stdout'),
            blob(base + f'replayed-controls/run-{i}.stderr')) for i in range(1, 4)]
assert len(set(samples)) == 1 and samples[0][0] == 0
assert all(c['observed_exit'] == c['expected_exit'] and c['passed']
           for c in receipt['checks'])
assert receipt['checks'][0]['stdout'].count('SELFTEST_CASE ') == 29
print('pristine tuples=3 identical; bytes=', len(samples[0][1]), len(samples[0][2]))
print('committed checks=', len(receipt['checks']), '; selftest cases=29 (not rerun)')
```

Observed: tool SHA `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`; ControlGate 9 input digests verified, match/0; mismatch 9 verified, mismatch/1; three stored pristine tuples identical with exit0/stdout1202B/stderr0B; 10 committed checks match their expected exits; 29 selftest-case lines. The actual executed Python cell printed these same values with explanatory labels.

Committed receipts in `verification-final.json` and `oracle-repair.json` retain the 29-case CLI selftest, real three-control run, both frozen results, one-loop mutant oracle FAIL/1 and restored-loop oracle PASS/0. The same mismatch oracle and changing fixture distinguish the two implementations. Final tool SHA ties the receipts to delivered content; SCORECARD records the measured commit. Historical argv under `/tmp` describe actual execution, while committed fixture/mutant/raw-output copies under `oracle-repair/` make the evidence durable. Rewriting historical argv would misrepresent that execution and is not requested.

**C1 verdict: calibration improved (capability), scalar6 unchanged.** Capability acquisition explicitly still lands a per-axis verdict (AXES, Capabilities). Evidence demonstrates finite exact-tuple observation, not determinism or a flaky-test cure. Caller-owned timeout and coordinated-rewrite limitations remain disclosed.

### C2 — replaying the registered read-only probe

```sh
python3 tools/bash-witness-study.py check
python3 tools/bash-witness-study.py count
```

Both exited 0 now. `check`: `WITNESS_CHECK: CLEAN (declared.tsv sha256=0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3, 96 files covered, 95 manifest entries)`.
`count`: control exit0/denominator16/exercised14/skipped2; `counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10 witness_classified=10`; declared_none B5,B10; unresolved none. B2/B6 fail clean/runtime-absent; B3 additionally fails runtime-absent. This tool is registered **probe**, not gate (`SKILL.md:1504`); these commands read retained observations, not a fresh target sweep.

**C2 verdict: depth improved (detail), scalar6 unchanged.** The declaration is prior-exposed, not blind; case labels are not assertions. Reanalysis remains one existing leg. The old six-leg runner and recorded gates remain unchanged. The 80/80 selftest and six-leg regression PASS were inspected in committed evidence, not re-executed by closure.

## Per-axis verdicts and harm check

`git diff 18ad5d050ef4bcd830fe513825baed878f025024 8742f5dcebf82bb1b57da7d7d2a7dd98a0e5c32e -- SCORECARD.md` showed an added capability row and appended measured-claim section, not scalar inflation or deletion of old evidence. Spot reads: SKILL registry/decision table, witness errata E2/E3, knowledge final addendum, README F3 resolution, QUALITY11–13, prior outside adjudication.

| Axis | Verdict | Bound |
|---|---|---|
| depth | improved | 10 classified defects with checked raw case labels; C2 |
| calibration | improved | finite-control capability and lesson-backed restraint; C1; no promotion points |
| coverage | unchanged | no province/Core takeover or numeric coverage claim |
| operability | unchanged | existing runner unchanged; historical runtime receipts retained |
| freshness | unchanged | stale-successor debt not repaired or hidden |
| adjacency | unchanged | pinned sibling artifact read-only; no sibling patch or absorbed province |

## Discernment spot-check — non-author Gate sampling

Reopened on 2026-10-20. SourceSpotcheck, ClaimsReview and ConformanceCheck were fresh read-only reviewer seats dispatched by this closure, not by the lane; integrator decisions below own the verdict. The integrator also reopened S004, S006 and S026 directly. S026's reader view omitted article text, so raw served HTML was reopened; comments were not substituted as authority.

| Item | Lane decision | Re-opened source | Outside judgment | Reason |
|---|---|---|---|---|
| Reliable copied-tree baseline | admit | S004 https://mutants.rs/using-results.html, “Tests fail in an clean tree?” | agree | Exact ≤25-word quote: “cargo-mutants can’t do anything until you have a tree where `cargo test` passes reliably when copied to a temporary directory.” 20 words; does not prescribe three repeats. |
| Witness versus accidental red | admit | S006 https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md, “The three verdicts”, accidental row | agree | “The suite went red, but not on its witness.” 9 words. Source distinguishes intended witness from unrelated failure; adapter non-equivalence is disclosed. |
| Flaky-result definition | admit, definition only | S026 https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html, post definition paragraph; raw HTML1095/1130 | agree | “a test that exhibits both a passing and a failing result with the same code.” 15 words. Source does not establish reliability from matching trials. |
| Three matches prove determinism | reject | Same S004/S026 bodies; source reviewer additionally reopened S011 https://mir.cs.illinois.edu/awshi2/publications/ISSTA2019.pdf p9 | agree | S011: “some flaky tests may continue to show the same coverage even on our repeated executions, only to appear flaky another day.” Finite agreement cannot exclude future divergence. |
| Bash reanalysis is a seventh independent gate | reject | `tools/mutate-and-run.sh` recorded-leg header, SCORECARD diff and current count output | agree | Six recorded cases/gates persist; new classification of the same target/spec does not create independent evidence. |
| Lane-dispatched review is outside authority | reject | Current canonical LEARNING “Discernment is checked from outside”; SHONEN/report assessment | agree | Same-lane seats are still the lane. This separate closure provides the outside sample; it earns no SHONEN `[x]`. |

No new SOURCES rows were written this round, so a newly added-row sample is inapplicable, not silently waived. Reopened existing rows S004/S006/S026 above satisfy the substantive quote check; independent source diff found only allowed mutable-cell changes on S004/S006/S011/S026/S028 and appended ledger notes. Source reviewer also verified S011 p9 and S028 test-runner wording. Uncredited quote-word notes and Markdown backtick normalization do not change the scoped admissions.

Ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` now: `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit0.

## Learning trends

- **expansion improved** — new `knowledge/repeated-control-precondition.md` cites mined S004/S026; README123–140 connects it to formerly open F3; demonstrated capability enters SCORECARD. This is new finite-control ground, not merely more rows.
- **quality improved** — witness E2/E3 explicitly correct abbreviated baseline semantics, whole-token versus exact-line behavior, and an invalid alternative; final runtime addendum supersedes earlier open-arm state. Red-before oracle and failed integration evidence remain visible. The dated earlier tool pin is historical and the final addendum states the final SHA; it is not a current unmarked false claim.
- **discernment improved** — this committed outside sample agrees on admits and rejects. Independently, prior box3 disagreement (`round-1-verifier-spotcheck.md:17`) becomes grounded QUALITY13 with a round12 mistake lesson. Both LEARNING branches have evidence; no same-lane seat is counted as outside authority.

## Routed defects and residuals

All are status-neutral; none falsifies the admitted bounded claims.

1. **Operator/protocol, hyaku renderer:** dispatch appended relative seat `Report:` destinations despite fleet-root tool cwd. W1 write-scope mistakes were disclosed and copies removed; current addendum adds absolute-seat-path guidance. Preserve that correction in future dispatched task text as well as context. Dispatched prompt predates the later addendum clarification; no historical prompt rewrite requested.
2. **Operator/protocol, closure mechanics:** prompt run-now capability wording conflicts with current Gate standard's non-execution rule; render the current committed-evidence verification rule. The helper validates and serializes ledger appends but is not itself the full committed frozen step1/status checker required by current protocol. This pass has explicit pinned rechecks/history verification, but does not claim a newly committed frozen closure-gate run. Route that orchestration conformance debt; do not mislabel it a lane marker or force a sibling-gate execution.
3. **Tameshi next round:** replace brittle host-addendum line citations with the named planner-ruling section in an append-only correction; the document's lines moved. Disclose/repair the already named nested `declaration.kind=null` metadata defect only through new evidence without rewriting the frozen declaration. The top-level kind/disclosure and measured claim remain explicit.
4. **Tameshi carried debt, intentionally unchanged:** full-page current SKILL cold-read/box3 remains unearned, scalar6 excludes it; legacy provenance headers, F1 interop, stale-successor ledger and runbook debts remain open. All SHONEN boxes are not yet independently checkable: no promotion recommendation.

Review integration: an initial ClaimsReview interpretation incorrectly treated scalar stability as no axis improvement and stored-byte replay as sibling-gate execution; after citing AXES40–41, the registry's probe kind and actual execution record, that reviewer explicitly withdrew both interpretations and accepted bounded C1/C2 and criterion13 discernment. Its suggestions to rewrite historical `/tmp` argv, add redundant generic-hit fields, or duplicate a measured revision inside every receipt are not adopted as admission blockers: committed copies, raw labels, tool SHA and SCORECARD already resolve those claims. This file supplies the separately committed outside sample it correctly requested.

## Dispatch/completion digest (durable copy)

```text
2026-10-19T23:10:59-03:00 launch tameshi round=12 pgid=13129 driver=hyaku slot=3 attempt=1
2026-10-19T23:24:27-03:00 lane-dead-no-report tameshi round=12; retry same round (hyaku: headless attempt ended by operator directive to run in-session)
2026-10-20T00:41:11-03:00 launch tameshi round=12 pgid=288438 driver=hyaku-inline attempt=1
2026-10-20T01:04:41-03:00 complete tameshi round=12; hyaku-inline attempt=1
```

Tool installs/updates: none. Closure writes only this non-author note and the serialized closure-entry input; ledger append/commit/push is delegated to the authorized helper. No promotion, mint, lane-authored edit or SHONEN mark change.
