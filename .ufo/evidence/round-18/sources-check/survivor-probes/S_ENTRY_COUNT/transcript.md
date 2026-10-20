# S_ENTRY_COUNT off-suite differential probe

## Pinned input and mutation

Materialized with `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs` into `/tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/sources-check.pristine.mjs`.

- Pinned blob SHA-256: `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (897 lines; agrees with the pre-registered spec header).
- Mutant SHA-256: `6b6373f47f301375781039e4578424ffccc42f97c1f0dad549f42a5b4349a30a`.
- The complete `diff -u` had one changed line only (`diff` exit 1, expected for differing files): `scripts/sources-check.mjs:368`, `counts.entriesWithSource += 1;` → `counts.entriesWithSource += 2;`.

## Retained fixture bytes

- `fixture/corpus/SOURCES.md` — 398 bytes, SHA-256 `0ebe004933b24b59a4e39f6748b337b66e4ae9c56f241d6be3ec5c131b17fb9e`.
- `fixture/corpus/knowledge/probe-entry.md` — 143 bytes, SHA-256 `dd1e6dd4f60413edfb2156f5daf611724c8c96b342748f3841cc6560d3dbee32`.

This hand-authored fixture has the four required headings, one valid queued S001 registry row, and exactly one direct knowledge `.md` file with a complete `source:` / `verified-at:` / `recheck:` header. The row's `used-by` names that file. It is run directly with `--self`, not through `--selftest`.

## Runs and exact outputs

All four invocations used `--today 2026-10-20`, the retained fixture above, and `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`.

### Pristine text mode

Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/sources-check.pristine.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20`

Exit: `0`

```text
SOURCES_CHECK: CLEAN (rows=1 tiers=A:0,B:1,C:0 status=queued:1,mined:0,rejected:0 entries_with_source=1 legacy=0)
```

### Mutant text mode

Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/mutant/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20`

Exit: `0`

```text
SOURCES_CHECK: CLEAN (rows=1 tiers=A:0,B:1,C:0 status=queued:1,mined:0,rejected:0 entries_with_source=2 legacy=0)
```

### Pristine JSON mode

Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/sources-check.pristine.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20 --json`

Exit: `0`

```json
{"schema":"kumitate-sources-v1","verdict":"CLEAN","exitCode":0,"findings":[],"totals":{"errors":0,"warnings":0},"counts":{"rows":1,"tiers":{"A":0,"B":1,"C":0},"status":{"queued":1,"mined":0,"rejected":0},"entriesWithSource":1,"legacy":0},"info":{"legacyEntriesWithoutHeader":0}}
```

### Mutant JSON mode

Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/mutant/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20 --json`

Exit: `0`

```json
{"schema":"kumitate-sources-v1","verdict":"CLEAN","exitCode":0,"findings":[],"totals":{"errors":0,"warnings":0},"counts":{"rows":1,"tiers":{"A":0,"B":1,"C":0},"status":{"queued":1,"mined":0,"rejected":0},"entriesWithSource":2,"legacy":0},"info":{"legacyEntriesWithoutHeader":0}}
```

## Finding

This is a distinguishing off-suite input: both executions exit 0 and say CLEAN, but both externally observable summaries report a different positive source-header-entry count (`1` versus `2`). The JSON difference is exactly `counts.entriesWithSource`.

The difference **is promised by the contract header**: pinned `scripts/sources-check.mjs:39-45` defines the final CLEAN line with `entries_with_source=k` and says `--json` emits the contract object. The implementation formats that count at lines 437-440 and serializes `result.counts` into JSON at lines 461-470. Therefore the pre-registered survivor prediction is falsified for off-suite output equivalence; this mutant changes a contract-visible count, although the existing selftest prediction at `sources-check.defects.spec:48-51` says the positive count is not pinned there.
