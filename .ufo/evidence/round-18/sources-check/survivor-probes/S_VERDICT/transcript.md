# S_VERDICT off-suite probe transcript

Workspace: `/tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0`

## Pinned source and mutant

Command:
```sh
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs > /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/sources-check.pristine.mjs
```
Exit: 0. `sha256sum` output for the materialized pinned blob: `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (matches the spec's blob digest).

Copied pristine to `sources-check.mutant.mjs`, then applied exactly the S_VERDICT replacement from `sources-check.defects.spec:25-26` at pristine/mutant line 483:
```diff
-  if (exitCode === 1) process.stdout.write(`SOURCES_CHECK: DRIFT (${driftKinds.join(',')})\n`);
+  if (exitCode === 1) process.stdout.write(`SOURCES_CHECK: DRIFT [${driftKinds.join(',')}]\n`);
```
`diff -u pristine mutant` exited 1 because this single expected difference exists; its output showed only that one-line replacement. Mutant SHA-256: `ff6d889e3a8b9406d108795f194c006f3f7413cbab9646304e68ffb402385264`.

## Fixture bytes

Stored evidence fixture:
- `fixture/corpus/SOURCES.md` — 464 bytes, SHA-256 `45e07f90fd44046168bbff8b66d655a90ddca127b922ee523eed40994f453ca3`
- `fixture/corpus/knowledge/probe.md` — 150 bytes, SHA-256 `d147c7758af8a9e94b2a74e4b8aa302727927f9a61a917716329d8759cd7745a`

The same files were copied to `/tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/probe-corpus`; SHA-256 outputs for evidence and temporary copies matched byte-for-byte.

`SOURCES.md` bytes (UTF-8, LF, final LF):
```markdown
# Source registry fixture

## Registry
| ID | Source | Kind | Tier | Scope | Anchor | Teaches | Status | Opened | Recheck | Used-by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S001 | https://example.test/source | not-a-kind | A | survivor probe | § fixture | exercise DRIFT spelling | queued | 2026-10-20 | on-release | corpus/knowledge/probe.md |

## Paths
Fixture-only path.

## Search log
Not applicable.

## Leads (unopened)
None.
```

`knowledge/probe.md` bytes (UTF-8, LF, final LF):
```markdown
source: S001 https://example.test/source
verified-at: 2026-10-20 fixture round-18
recheck: on-release

# Probe fixture
Off-suite input for S_VERDICT.
```

## Runs and outputs

Text mode, pristine:
```sh
node /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/sources-check.pristine.mjs --self /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/probe-corpus --today 2026-10-20
```
Exit: 1. Stdout:
```text
SOURCES  error  KIND_ENUM  corpus/SOURCES.md:6  id=S001 kind=not-a-kind
SOURCES_CHECK: DRIFT (KIND_ENUM)
```

Text mode, mutant:
```sh
node /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/sources-check.mutant.mjs --self /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/probe-corpus --today 2026-10-20
```
Exit: 1. Stdout:
```text
SOURCES  error  KIND_ENUM  corpus/SOURCES.md:6  id=S001 kind=not-a-kind
SOURCES_CHECK: DRIFT [KIND_ENUM]
```

JSON mode, pristine and mutant respectively, used the same arguments with `--json`; each exited 1 and emitted the same JSON object:
```json
{"schema":"kumitate-sources-v1","verdict":"DRIFT","exitCode":1,"findings":[{"severity":"error","kind":"KIND_ENUM","path":"corpus/SOURCES.md","line":6,"detail":"id=S001 kind=not-a-kind"}],"totals":{"errors":1,"warnings":0},"counts":{"rows":1,"tiers":{"A":1,"B":0,"C":0},"status":{"queued":1,"mined":0,"rejected":0},"entriesWithSource":1,"legacy":0},"info":{"legacyEntriesWithoutHeader":0}}
```

## Contract comparison

The checker header at pristine `sources-check.mjs:39-44` defines the final text-mode stdout line for DRIFT as `SOURCES_CHECK: DRIFT (<kind list>)` and specifies exit 1 for drift; it says `--json` prints one JSON object instead. The observed exit map and JSON verdict stayed the same, but the mutant changed the promised final text line's parentheses to square brackets. The changed output is externally observable and contradicts the header contract.
