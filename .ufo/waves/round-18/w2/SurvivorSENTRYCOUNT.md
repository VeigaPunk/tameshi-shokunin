# S_ENTRY_COUNT survivor probe

## Finding

A single hand-built off-suite fixture distinguishes the pinned pristine `scripts/sources-check.mjs` from the exact S_ENTRY_COUNT mutant. Both return exit 0 and `CLEAN`, but the final text line reports `entries_with_source=1` versus `2`; JSON reports `counts.entriesWithSource: 1` versus `2`. The predicted survivor is therefore not output-equivalent outside the selftest suite.

## Inputs and mutation

- Pristine blob materialized from `kumitate-shokunin` revision `0acb7752d19058b953ebbeba253b1e35f6548de5`, path `scripts/sources-check.mjs`; SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (897 lines, matching the spec header).
- Applied only the pre-registered replacement at `scripts/sources-check.mjs:368`: `counts.entriesWithSource += 1;` → `counts.entriesWithSource += 2;`. `diff -u` showed that single line change only (exit 1, expected for different files); mutant SHA-256 `6b6373f47f301375781039e4578424ffccc42f97c1f0dad549f42a5b4349a30a`.
- Retained fixture: `.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture/corpus/SOURCES.md` (398 bytes, SHA-256 `0ebe004933b24b59a4e39f6748b337b66e4ae9c56f241d6be3ec5c131b17fb9e`) and `.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture/corpus/knowledge/probe-entry.md` (143 bytes, SHA-256 `dd1e6dd4f60413edfb2156f5daf611724c8c96b342748f3841cc6560d3dbee32`). It contains one valid queued S001 row, all required headings, and one complete source header; the row's used-by lists that knowledge file.

## Commands and observed results

Each command ran with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`, `--self` set to the retained fixture directory, and `--today 2026-10-20`:

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/sources-check.pristine.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20` — exit 0; final line `SOURCES_CHECK: CLEAN (rows=1 tiers=A:0,B:1,C:0 status=queued:1,mined:0,rejected:0 entries_with_source=1 legacy=0)`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/sources-check.pristine.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20 --json` — exit 0; `counts.entriesWithSource` is `1`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/mutant/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20` — exit 0; final line `SOURCES_CHECK: CLEAN (rows=1 tiers=A:0,B:1,C:0 status=queued:1,mined:0,rejected:0 entries_with_source=2 legacy=0)`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR node /tmp/tameshi-r18w2-SENTRYCOUNT-DzVk46/mutant/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/fixture --today 2026-10-20 --json` — exit 0; `counts.entriesWithSource` is `2`.

Complete stdout, JSON objects, fixture hashes, pinned and mutant hashes, and the exact one-line diff are retained in `.ufo/evidence/round-18/sources-check/survivor-probes/S_ENTRY_COUNT/transcript.md`.

## Contract relation

The difference is contract-promised: pinned `kumitate-shokunin/scripts/sources-check.mjs:39-45` specifies the CLEAN final line with `entries_with_source=k`; `kumitate-shokunin/scripts/sources-check.mjs:437-440` formats the count; `kumitate-shokunin/scripts/sources-check.mjs:461-470` serializes the counts into JSON. The defect spec at `.ufo/evidence/round-18/sources-check/sources-check.defects.spec:48-51` predicts this as a survivor because the selftest does not pin a positive count. This probe confirms the test-suite blind spot but falsifies external-output equivalence.

## Risks and blockers

No blockers. This result establishes the mutant changes the contract-visible count on the retained fixture; it does not claim to have run the complete selftest or regression suite.

**Verdict: falls — the S_ENTRY_COUNT mutant is not externally equivalent to pristine.**
