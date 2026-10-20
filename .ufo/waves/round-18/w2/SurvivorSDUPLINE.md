# S_DUP_LINE off-suite survivor probe

## Finding

S_DUP_LINE is not observationally equivalent: a retained off-suite duplicate-row fixture makes the pinned pristine source and the exact mutant differ in output. Both exit 1 with `SOURCES_CHECK: DRIFT (ID_DUPLICATE)`, but pristine attributes the duplicate to `corpus/SOURCES.md:8` and mutant to `corpus/SOURCES.md:9`. In JSON, the only changed field is `findings[0].line` (8 → 9). The fixture's repeated ID is on line 8.

The pre-registered mutation spec says the defect changes `index + 1` to `index + 2` (`sources-check.defects.spec:43-46`). The pinned blob materialized from `kumitate-shokunin/scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5` had SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, matching the spec. `diff -u` of pristine and mutant showed exactly that one-line change; `diff` returned 1 (files differ). Mutant SHA-256: `7015c23fa4506046c75506f1100717bee1849c54faa9b75c70ea51fdb9783be2`.

## Commands and observations

Text runs (each exit 1):

```sh
node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19
# SOURCES  error  ID_DUPLICATE  corpus/SOURCES.md:8  id=S001
# SOURCES_CHECK: DRIFT (ID_DUPLICATE)

node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check-mutant.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19
# SOURCES  error  ID_DUPLICATE  corpus/SOURCES.md:9  id=S001
# SOURCES_CHECK: DRIFT (ID_DUPLICATE)
```

JSON runs (each exit 1; exact JSON stdout is retained in the transcript):

```sh
node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19 --json
# findings[0].line = 8

node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check-mutant.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19 --json
# findings[0].line = 9
```

## Contract and evidence

The source header at `scripts/sources-check.mjs:10-32` promises an `ID_DUPLICATE` error for an otherwise-well-formed repeated registry ID. Its `:39-44` comments specify the final text verdict, exit map, and that `--json` emits one object. The header does not specify which occurrence's line is used or promise exact line attribution. So this is an observable diagnostic difference, but both outputs meet the explicit header promises. [INFERENCE] Reporting the repeated row's exact line is natural intent, but the header does not explicitly guarantee it.

Retained fixture: `.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture/corpus/SOURCES.md` (542 bytes, SHA-256 `712d5c9e2bb01e31cca23df22db4edd21e06294fb8807c2dd244588a6b167814`); fixture includes an empty `corpus/knowledge/` directory. The source fixture bytes, materialization, mutant delta, and exact stdout/exit records are retained in `.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/transcript.md` (SHA-256 `8a14cc4b9b82d5de5892f783c84bc2db75756e86b4ef1eda62da9d5b2553761f`).

Files written: the fixture, transcript, and this scoped report. No tools were installed. No blocker.

Verdict: falls — the suite-survivor mutation is externally distinguishable off-suite by line 8 vs line 9, although exact line attribution is not expressly specified in the header contract.
