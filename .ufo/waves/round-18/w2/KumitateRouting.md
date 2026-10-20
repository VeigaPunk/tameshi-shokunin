# Route note — kumitate `sources-check` survivor assertions

Seat `TameshiR18.KumitateRouting`. Route only. Kumitate owns the gate (`PROVINCE.md:15`). This note does not edit or push that repo.

Axes kept together: kill-specificity (each registered survivor fails one named check), intent-fit (the checks enforce clauses kumitate already wrote down), operability (kumitate tree and `origin/master` stay as found).

## Recommendation

Add six checks to `scripts/sources-check.mjs` `--selftest`, immediately after the one-sided coverage check at `scripts/sources-check.mjs:784-785`, and add `chmodSync` to the `node:fs` import at `:48`. Leave every existing check in place. The pinned file is blob `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (897 lines, 43497 bytes, HEAD `1770305fae20826b39905a8251ddeca6b4957ac4`, same bytes as `0acb7752:scripts/sources-check.mjs`).

| Survivor | Edit the suite does not see | Assertion that kills it |
|---|---|---|
| `S_KIND` | drop `'RECHECK_OVERDUE'` from `FINDING_KINDS` (`:114`) | `every observed finding kind is declared` — `[...observed].filter(kind => !FINDING_KINDS.includes(kind))` is empty |
| `S_VERDICT` | `SOURCES_CHECK: DRIFT (…)` becomes `DRIFT […]` (`:483`) | `DRIFT verdict line spells the parenthesized kind list` — final line `=== 'SOURCES_CHECK: DRIFT (TIER_ENUM)'` |
| `S_DUP_LINE` | `ID_DUPLICATE` line `index + 1` becomes `index + 2` (`:251`) | `ID_DUPLICATE reports the duplicate row line` — text `corpus/SOURCES.md:N` equals the second `S001` row in the fixture |
| `S_ENTRY_COUNT` | `entriesWithSource += 1` becomes `+= 2` (`:368`) | clean text contains `entries_with_source=1 legacy=0`, and `--json` has `counts.entriesWithSource === 1` |
| `S_FILE_READ` | per-file `READ_FAILED` becomes `SOURCES_MISSING` (`:356`) | a mode-`0o000` `corpus/knowledge/alpha.md` ends `SOURCES_CHECK: FAIL-CLOSED (READ_FAILED)` and the detail contains `cannot read corpus/knowledge/alpha.md (` |

Proven insertion (copy only; kumitate was not patched):

```javascript
const undeclaredKinds = [...observed].filter((kind) => !FINDING_KINDS.includes(kind));
check('every observed finding kind is declared', () => ({ ok: undeclaredKinds.length === 0, detail: `undeclared=[${undeclaredKinds.join(',')}]` }));

check('DRIFT verdict line spells the parenthesized kind list', () => {
  const run = runCase('drift-verdict-line', { tier: 'D' });
  const line = finalLine(run);
  return { ok: line === 'SOURCES_CHECK: DRIFT (TIER_ENUM)', detail: `last=${line}` };
});

check('ID_DUPLICATE reports the duplicate row line', () => {
  const root = makeDefault('duplicate-line', {
    rows: [
      makeRow({ id: 'S001', status: 'mined', usedBy: 'corpus/knowledge/alpha.md' }),
      makeRow({ id: 'S001' }),
    ],
  });
  const hits = [];
  readFileSync(join(root, 'corpus', 'SOURCES.md'), 'utf8').split(/\r?\n/).forEach((row, index) => {
    if (/^\|\s*S001\s*\|/.test(row)) hits.push(index + 1);
  });
  const expectedLine = hits[1];
  const run = runTool(['--self', root, '--today', FIXTURE_TODAY]);
  const match = run.stdout.match(/^SOURCES\s+error\s+ID_DUPLICATE\s+corpus\/SOURCES\.md:(\d+)\s+id=S001$/m);
  const got = match ? Number(match[1]) : null;
  return { ok: run.status === 1 && got === expectedLine, detail: `exit=${run.status} line=${got} expected=${expectedLine} hits=${hits.join(',')}` };
});

check('clean fixture pins entries_with_source=1', () => {
  const run = runTool(['--self', clean, '--today', FIXTURE_TODAY]);
  const line = finalLine(run);
  return { ok: run.status === 0 && line.includes('entries_with_source=1 legacy=0'), detail: `exit=${run.status} last=${line}` };
});

check('--json pins entriesWithSource=1', () => {
  const run = runTool(['--self', clean, '--today', FIXTURE_TODAY, '--json']);
  const parsed = JSON.parse(run.stdout);
  return { ok: run.status === 0 && parsed.counts && parsed.counts.entriesWithSource === 1, detail: `exit=${run.status} entriesWithSource=${parsed.counts && parsed.counts.entriesWithSource}` };
});

check('per-entry knowledge read failure is READ_FAILED', () => {
  const root = makeDefault('per-entry-unreadable', { entry: null });
  const file = join(root, 'corpus', 'knowledge', 'alpha.md');
  writeFileSync(file, BASE_ENTRY);
  chmodSync(file, 0o000);
  try {
    const run = runTool(['--self', root, '--today', FIXTURE_TODAY]);
    const line = finalLine(run);
    const detailOk = run.stdout.includes('cannot read corpus/knowledge/alpha.md (');
    return {
      ok: run.status === 2 && line === 'SOURCES_CHECK: FAIL-CLOSED (READ_FAILED)' && detailOk,
      detail: `exit=${run.status} last=${line} detailOk=${detailOk}`,
    };
  } finally {
    chmodSync(file, 0o644);
  }
});
```

`runCase` (`:658`) and `clean` (`:586`) are already in scope at the insertion point. `observed` at `:784` already contains `RECHECK_OVERDUE` from the fixture at `:656` and the cadence fixture at `:743-745`. Computing `undeclaredKinds` there is what makes `S_KIND` fail.

## What the sweep already showed

`sweep/sweep.txt` (sha256 `4ba2a595668439e6ca77bdb26fb462e71e88fe9079a50a77ea9e7d7ff2586097`), context commit `93d22aa`, target sha `6a293a72…258f`. Oracle is exit status (`sources-check.defects.spec:3`, sha256 `c8d24cb4…8c91`, matches `predictions.json` `spec_sha256`).

| id | sweep line | measured | suite tail |
|---|---|---|---|
| `S_KIND` | `sweep.txt:29` | SURVIVED exit 0 | `46/46` `VERDICT: PASS` (`:36-37`) |
| `S_VERDICT` | `:47` | SURVIVED exit 0 | `:54-55` |
| `S_DUP_LINE` | `:83` | SURVIVED exit 0 | `:90-91` |
| `S_ENTRY_COUNT` | `:92` | SURVIVED exit 0 | S1000 still PASS with `entries_with_source=2` (`:94`) |
| `S_FILE_READ` | `:101` | SURVIVED exit 0 | `:108-109` |

`PREDICTION_MATCH: 10/10` (`sweep.txt:130`). Pristine control of the same suite prints the unpinned values the new checks lock: `entries_with_source=1 legacy=0` (`control/hazard-git-dir.stdout:1`) and `SOURCES_CHECK: DRIFT (TIER_ENUM)` (`:8`). The S1000 line there is `entries_with_source=1` (`:42`); the mutant sweep prints `2` on that same check and still passes (`sweep.txt:94`).

Registered edits (`sources-check.defects.spec`):

- `S_KIND` `:14-16` — delete the declaration element. Emission at `:331` and `:335` stays. Coverage at `:784-785` walks `FINDING_KINDS` only (`predictions.json:15-18`).
- `S_VERDICT` `:24-26` — parentheses to brackets at `:483`. `expectKind` (`:575-581`) asserts exit and `SOURCES  error|warn  KIND`, and the detail string carries `finalLine` without comparing it (`predictions.json:25-28`).
- `S_DUP_LINE` `:44-46` — `:251`. The `ID_DUPLICATE` case (`:602-604`, `:669-672`) asserts kind and exit (`predictions.json:45-48`).
- `S_ENTRY_COUNT` `:49-51` — `:368`. The positive count is unpinned. The zero count is already pinned (`:768`, `entries_with_source=0 legacy=1`). JSON asserts `counts.rows === 1` (`:813-816`) (`predictions.json:50-53`).
- `S_FILE_READ` `:54-56` — `:356`. The existing `READ_FAILED` fixture sets `knowledgeIsFile: true` (`:790-794`), which returns at the `readdirSync` catch (`:343-349`) (`predictions.json:55-58`).

## Intent fit (kumitate SKILL / QUALITY)

These checks enforce text the gate already states. They do not add a contract.

- Script header `:39-44` already defines `SOURCES_CHECK: CLEAN (… entries_with_source=k legacy=l)`, `SOURCES_CHECK: DRIFT (<kind list>)`, and `SOURCES_CHECK: FAIL-CLOSED (<kind>)`. `S_VERDICT` and `S_ENTRY_COUNT` pin that spelling inside `--selftest`.
- `SKILL.md:605` records the gate as `SOURCES_CHECK: CLEAN|DRIFT` plus `--selftest`. `SKILL.md:629-630` requires live exit 0 + `SOURCES_CHECK: CLEAN`, and suite exit 0 + `VERDICT: PASS`. The new DRIFT pin is hermetic. The live checklist item stays the CLEAN run.
- `SKILL.md:608-609` names an unclaimed gap: no digest-pinned expected-verdict file, and no verdict line carries the revision it measured. This route does not add that file and does not put a revision on the verdict line.
- `QUALITY.md:41-44` (Q7) and `:83-86` (How to apply, open) quote whole DRIFT lines from `proxy-check`, `kimi-census`, and `round-gate`. `sources-check` is not in that run list. The new assertion is a suite pin of `:41`, not a new admission criterion.
- `QUALITY.md:109-117` limits the headerless legacy set to the 38 paths frozen in the script. That pin already exists at `:753-769`. Leave it.
- `SCORECARD.md:1616` records `--selftest` 46/46 as capability evidence. The checklist does not freeze 46. Landing these checks moves the count to 52/52. Kumitate's own admission updates that cell.
- Keep `:784-785` (`every declared finding kind fires`). The new check is the other inclusion. A second handwritten copy of `FINDING_KINDS` would be a second declaration beside `:108-115`.
- Keep the S1000 prefix check (`:822-824`). It pins id width (`rows=2`). The sweep's doubled counter shows up on that line; the positive pin belongs on the clean fixture, where the contract value is 1.
- Keep the directory `READ_FAILED` fixture (`:790-800`). The per-file check is a second fixture. The detail `cannot read corpus/knowledge/alpha.md (` is produced by `:356` (`relPath`). The directory arm at `:349` says `cannot read corpus/knowledge (`. `detailOk=true` on the mutant run is the evidence the per-file arm ran. `chmodSync(path, 0o000)` is the shape `kimi-census.mjs:810-820` already uses for an unreadable path; restore `0o644` before the temp dir is removed.

## Proof

Scratch `W=/tmp/tameshi-r18w2-KumitateRouting-jmEv8L`. Source copy is the worktree file; sha256 matched the pin (`SOURCE=worktree pin-match`). Harness writes only under `$W`. Each `--selftest` ran in bwrap (`--ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $WORK $WORK --unshare-net`) with `env -i` and the `suite.txt` variables (`PATH`, `HOME`, `TMPDIR`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CEILING_DIRECTORIES`) plus `GIT_CONFIG_GLOBAL=/dev/null`.

```text
bwrap probe: exit=0  node v24.21.0  uid=1000
W=/tmp/tameshi-r18w2-KumitateRouting-jmEv8L python3 $W/harness.py
HARNESS_EXIT=0
PROOF holds
```

Mutant-only rows reapply the spec edit to the pinned file and reproduce the sweep. Plus rows are that edit plus the six checks.

| run | exit | suite | failed checks |
|---|---|---|---|
| recommended (pinned + six checks) | 0 | `52/52` `VERDICT: PASS` | none |
| `S_KIND-only` | 0 | `46/46` | none |
| `S_KIND-plus` | 1 | `51/52` | `undeclared=[RECHECK_OVERDUE]` |
| `S_VERDICT-only` | 0 | `46/46` | none |
| `S_VERDICT-plus` | 1 | `51/52` | `last=SOURCES_CHECK: DRIFT [TIER_ENUM]` |
| `S_DUP_LINE-only` | 0 | `46/46` | none |
| `S_DUP_LINE-plus` | 1 | `51/52` | `line=9 expected=8 hits=7,8` |
| `S_ENTRY_COUNT-only` | 0 | `46/46` | none |
| `S_ENTRY_COUNT-plus` | 1 | `50/52` | text `entries_with_source=2`; json `entriesWithSource=2` |
| `S_FILE_READ-only` | 0 | `46/46` | none |
| `S_FILE_READ-plus` | 1 | `51/52` | `FAIL-CLOSED (SOURCES_MISSING)` and `detailOk=true` |
| `K_EXIT-plus` (existing kill, no-harm) | 1 | `50/52` | the two usage checks, `exit=65`; all six new checks PASS |

On every plus run the other new checks stayed PASS. `K_EXIT` (`return 64` → `return 65` at `:492`) still fails only `invalid/missing option value uses usage exit 64` and `unknown option uses usage exit 64`.

Pristine recommended details: duplicate rows at fixture lines 7 and 8, reported line 8; clean line `entries_with_source=1 legacy=0`; json `entriesWithSource=1`; per-file arm `FAIL-CLOSED (READ_FAILED)`.

## Kumitate untouched

No push, commit, index write, or editor write in `kumitate-shokunin`. Read-only git used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`.

```text
git -C kumitate-shokunin status --porcelain=v1 --untracked-files=all --branch
→ ## master...origin/master
git rev-parse HEAD → 1770305fae20826b39905a8251ddeca6b4957ac4
git rev-list --left-right --count @{upstream}...HEAD → 0 0
sha256sum scripts/sources-check.mjs → 6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
wc -lc → 897 43497
```

The same status and the same sha256 were taken after the proof (`STATUS_UNCHANGED`, `HASH_UNCHANGED`). `git diff --exit-code -- scripts/sources-check.mjs SKILL.md corpus/QUALITY.md PROVINCE.md` → exit 0.

Host `id` was `uid=1000(vgpnk)`. No package was installed.

## Risks

- Mode `0o000` does not stop a reader with `euid` 0. This proof ran as uid 1000. `kimi-census.mjs:811` has the same shape.
- `S_KIND`'s reverse inclusion fires because the `RECHECK_OVERDUE` fixture still emits the kind. The registered edit only deletes the array element (`spec:14-16`).
- The DRIFT assertion locks this fixture to the single kind `TIER_ENUM`, which `control/hazard-git-dir.stdout:8` already prints. A second error kind on that fixture would fail the pristine suite.
- The capability cell's `46/46` (`SCORECARD.md:1616`) moves to `52/52` when kumitate lands the checks. `SKILL.md:630` continues to require `VERDICT: PASS`.

Inputs: `kumitate-shokunin/SKILL.md` `a9a7f00d4fd9202f7c743aa9d003be0a708fef4c390735151f178aabf7b6f574`; `corpus/QUALITY.md` `3da34b0f9b329f16af544293e82da0a44d86b8acfdace1ff77f793dc3a2eb849`; `PROVINCE.md` `fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f`.

verdict: holds — six additive selftest checks kill S_KIND, S_VERDICT, S_DUP_LINE, S_ENTRY_COUNT, and S_FILE_READ on separate assertions, and kumitate was neither edited nor pushed.
