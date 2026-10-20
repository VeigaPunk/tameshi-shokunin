# S_DUP_LINE survivor non-equivalence probe

Pinned source: `kumitate-shokunin/scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5`; the pre-registered spec records blob SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` and specifies the exact mutation at `sources-check.defects.spec:43-46` (`index + 1` → `index + 2`).

## Materialization and mutant

Command:

```sh
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs > /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check.mjs
```

Observed pinned blob SHA-256: `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (matches the spec). The mutant is `/tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check-mutant.mjs`, copied from that blob and changed only at line 251 from `index + 1` to `index + 2`. `diff -u` showed exactly that one-line replacement and no other changes; diff exit 1 means the files differ. Mutant SHA-256: `7015c23fa4506046c75506f1100717bee1849c54faa9b75c70ea51fdb9783be2`.

## Retained off-suite fixture bytes

Input directory: `.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture/`, containing `corpus/SOURCES.md` and an empty `corpus/knowledge/` directory. The `SOURCES.md` file is 542 bytes, SHA-256 `712d5c9e2bb01e31cca23df22db4edd21e06294fb8807c2dd244588a6b167814`, UTF-8 with a final LF; its exact content is:

```markdown
# SOURCES — S_DUP_LINE fixture

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | Fixture — https://example.test/source | docs | A | fixture scope | § Fixture; r1 | fixture teaches | queued | 2026-10-19 | on-release | — |
| S001 | Fixture — https://example.test/source | docs | A | fixture scope | § Fixture; r1 | fixture teaches | queued | 2026-10-19 | on-release | — |

## Paths

## Search log

## Leads (unopened)
```

## Runs and exact outputs

All commands used `--today 2026-10-19`; both programs read the same retained fixture.

Pristine text command:

```sh
node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19
```

Exit 1; stdout:

```text
SOURCES  error  ID_DUPLICATE  corpus/SOURCES.md:8  id=S001
SOURCES_CHECK: DRIFT (ID_DUPLICATE)
```

Mutant text command:

```sh
node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check-mutant.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19
```

Exit 1; stdout:

```text
SOURCES  error  ID_DUPLICATE  corpus/SOURCES.md:9  id=S001
SOURCES_CHECK: DRIFT (ID_DUPLICATE)
```

Pristine JSON command:

```sh
node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19 --json
```

Exit 1; stdout:

```json
{"schema":"kumitate-sources-v1","verdict":"DRIFT","exitCode":1,"findings":[{"severity":"error","kind":"ID_DUPLICATE","path":"corpus/SOURCES.md","line":8,"detail":"id=S001"}],"totals":{"errors":1,"warnings":0},"counts":{"rows":2,"tiers":{"A":2,"B":0,"C":0},"status":{"queued":2,"mined":0,"rejected":0},"entriesWithSource":0,"legacy":0},"info":{"legacyEntriesWithoutHeader":0}}
```

Mutant JSON command:

```sh
node /tmp/tameshi-r18w2-SurvivorSDUPLINE-4wT5w9/sources-check-mutant.mjs --self /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/sources-check/survivor-probes/S_DUP_LINE/fixture --today 2026-10-19 --json
```

Exit 1; stdout:

```json
{"schema":"kumitate-sources-v1","verdict":"DRIFT","exitCode":1,"findings":[{"severity":"error","kind":"ID_DUPLICATE","path":"corpus/SOURCES.md","line":9,"detail":"id=S001"}],"totals":{"errors":1,"warnings":0},"counts":{"rows":2,"tiers":{"A":2,"B":0,"C":0},"status":{"queued":2,"mined":0,"rejected":0},"entriesWithSource":0,"legacy":0},"info":{"legacyEntriesWithoutHeader":0}}
```

## Contract assessment

The source header at `scripts/sources-check.mjs:10-32` promises an `ID_DUPLICATE` error for a repeated otherwise-well-formed registry ID. Lines 39-44 document the final text-mode verdict, exit map, and that `--json` emits one object. The header does not state which occurrence's line is reported or promise exact line-number attribution. Thus the probe demonstrates an externally observable output difference (text location and JSON `findings[0].line`), while both variants satisfy the header's explicit duplicate-kind and exit behavior. [INFERENCE] Exact duplicate-row location is natural diagnostic intent but is not an explicit promise in the header comment.

Verdict: falls — the S_DUP_LINE mutant is distinguishable off-suite: pristine reports the repeated row at `corpus/SOURCES.md:8`, mutant reports line 9; exact line attribution is not expressly specified by the header contract.
