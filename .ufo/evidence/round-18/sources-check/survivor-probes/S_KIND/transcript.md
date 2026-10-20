# S_KIND survivor probe

## Source and mutation

- Pinned input: `kumitate-shokunin/scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5`, materialized read-only with `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs` (exit 0) to `/tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/pristine.mjs`.
- Pinned blob SHA-256: `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (matches `.ufo/evidence/round-18/sources-check/sources-check.defects.spec:2`).
- Built `/tmp/tameshi-r18w2-SurvivorSKIND-JY5Cns/mutant.mjs` by requiring exactly one occurrence of `  'RECHECK_OVERDUE',\n` and replacing it with the empty string (the pre-registered `@old`/`@new` at `.ufo/evidence/round-18/sources-check/sources-check.defects.spec:14-16`). Mutant SHA-256: `c80cb365d1093156013b3ddc839863d224685eae579280da0c6ff90c004f67c4`.
- `diff -u pristine.mjs mutant.mjs` exited 1, with exactly one source-line deletion: `'RECHECK_OVERDUE',` (pinned source line 114; declaration at `scripts/sources-check.mjs:108-115`). No other source bytes differ.

## Fixture bytes

Stored at `fixture/corpus/SOURCES.md` (SHA-256 `7a7c9dca345efe7e90deb6d0a196750c0b5bf97b46321d4786e5caa4422090bd`):

```markdown
# SOURCES — S_KIND probe

## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | Fixture — https://example.test/one | docs | B | probe | § Probe; r1 | probe fixture | queued | 2026-10-18 | 2026-10-18 | corpus/knowledge/alpha.md |

## Paths

## Search log

## Leads (unopened)
```

Stored at `fixture/corpus/knowledge/alpha.md` (SHA-256 `4568a06e3dd7904d2d0593dadf5d204c20bcf1116f2822903e19bafdb0fc255e`):

```markdown
source: S001 https://example.test/one
verified-at: 2026-10-19 fixture r1
recheck: on-release

# Fixture knowledge
```

## Commands and observed outputs

All commands ran against the materialized `/tmp` copies and this fixture; each stderr file is empty (0 bytes).

1. `node "$W/pristine.mjs" --self "$F" --today 2026-10-19 --json` — exit 0. Exact stdout is `pristine-check.json` (SHA-256 `4666ccc69425289143cb81156fc382ddaffdc42f98a61ef5596ebd12d1f617a0`).
2. `node "$W/mutant.mjs" --self "$F" --today 2026-10-19 --json` — exit 0. Exact stdout is `mutant-check.json`, byte-identical to pristine (same SHA-256). The JSON reports the expected `RECHECK_OVERDUE` warning at `corpus/SOURCES.md:6`; the checker still emits the removed kind.
3. `node "$W/pristine.mjs" --self "$F" --today 2026-10-19 --help` — exit 0. Exact stdout retained as `pristine-help.txt` (SHA-256 `f1d41678d8478f08089abc6650be113aae3271151ae72ee632a4250e23949bb1`).
4. `node "$W/mutant.mjs" --self "$F" --today 2026-10-19 --help` — exit 0. Exact stdout retained as `mutant-help.txt` (SHA-256 `55b9fc15f8338c6c5d4aa0982e2b6f05a8c3ae63e428b6eb97ee4feb5c97e7578`). `diff -u pristine-help.txt mutant-help.txt` exited 1; the sole changed line is:

```text
pristine: findings: ROW_MALFORMED ID_FORM ID_DUPLICATE ROW_OUTSIDE_REGISTRY ROW_FIELD_EMPTY KIND_ENUM TIER_ENUM STATUS_ENUM TIER_INFLATION OPENED_INVALID RECHECK_INVALID USED_BY_MISSING MINED_UNUSED REJECTED_NO_REASON REJECTED_NO_FLIP SECTION_MISSING ENTRY_SOURCE_UNKNOWN ENTRY_HEADER_REQUIRED HEADER_INCOMPLETE USED_BY_ASYMMETRY RECHECK_OVERDUE
mutant:   findings: ROW_MALFORMED ID_FORM ID_DUPLICATE ROW_OUTSIDE_REGISTRY ROW_FIELD_EMPTY KIND_ENUM TIER_ENUM STATUS_ENUM TIER_INFLATION OPENED_INVALID RECHECK_INVALID USED_BY_MISSING MINED_UNUSED REJECTED_NO_REASON REJECTED_NO_FLIP SECTION_MISSING ENTRY_SOURCE_UNKNOWN ENTRY_HEADER_REQUIRED HEADER_INCOMPLETE USED_BY_ASYMMETRY
```

## Interpretation

The mutation is **not whole-CLI observationally equivalent**: the `--help` output omits `RECHECK_OVERDUE`. This is a help-inventory discrepancy, not a corpus-dependent checker distinction: `runCli` returns `USAGE` for help before calling `runCheck` (`scripts/sources-check.mjs:488-497`), so the fixture path and bytes do not affect that output. On the real corpus-validation path exercised with `--json`, the outputs are byte-identical and preserve the overdue warning.

The source header comment lists `RECHECK_OVERDUE` as a warning (`scripts/sources-check.mjs:31`) and defines the JSON/check result contract (`:39-44`); the help list comes from `FINDING_KINDS` (`:130`). The header does not explicitly promise that help enumerates every finding kind. Thus the observed omission is externally visible and makes help inconsistent with the documented finding inventory, but it does not falsify the promised checker behavior that `RECHECK_OVERDUE` is emitted as a warning. The registered one-sided selftest coverage check is at `scripts/sources-check.mjs:784-785`; this probe did not run `--selftest`.

**Result:** partial against the strict corpus-input criterion: no distinguishing corpus-check output was observed; a separate CLI help-output difference was confirmed and retained above.
