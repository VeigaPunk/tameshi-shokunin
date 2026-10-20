# S_VERDICT survivor probe

## Finding
A single off-suite corpus fixture distinguishes the pristine checker from the S_VERDICT mutant through the text-mode final stdout line. Both runs exit 1 and report the same `KIND_ENUM` finding at `corpus/SOURCES.md:6`, but the final lines differ:

- Pinned pristine: `SOURCES_CHECK: DRIFT (KIND_ENUM)`
- Mutant: `SOURCES_CHECK: DRIFT [KIND_ENUM]`

The difference is one the checker contract promises: the source header defines the final DRIFT text line as `SOURCES_CHECK: DRIFT (<kind list>)` at `scripts/sources-check.mjs:39-44`; the mutated output violates that spelling. In JSON mode, both emitted the same `verdict:"DRIFT"` and `exitCode:1` object. This fixture is outside the embedded `--selftest` suite and is passed through `--self`.

## Pinned bytes and exact mutation

Materialized with:
```sh
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs > /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/sources-check.pristine.mjs
```
Exit 0; `sha256sum` was `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`, matching `sources-check.defects.spec:2`. The spec's S_VERDICT mutation at `sources-check.defects.spec:24-26` changes the output template at pristine line 483 from `DRIFT (${driftKinds.join(',')})` to `DRIFT [${driftKinds.join(',')}]`. `diff -u` showed exactly this single changed line (expected diff exit 1). Mutant SHA-256: `ff6d889e3a8b9406d108795f194c006f3f7413cbab9646304e68ffb402385264`.

## Fixture and runs

Fixture bytes are retained under `.ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/fixture/`:
- `corpus/SOURCES.md`: 464 bytes; SHA-256 `45e07f90fd44046168bbff8b66d655a90ddca127b922ee523eed40994f453ca3`.
- `corpus/knowledge/probe.md`: 150 bytes; SHA-256 `d147c7758af8a9e94b2a74e4b8aa302727927f9a61a917716329d8759cd7745a`.

The same file hashes were observed for the temporary `/tmp/.../probe-corpus` copies used for execution. Full fixture bytes, exact commands and complete captured outputs are in `.ufo/evidence/round-18/sources-check/survivor-probes/S_VERDICT/transcript.md`.

Text runs (both exit 1):
```sh
node /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/sources-check.pristine.mjs --self /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/probe-corpus --today 2026-10-20
node /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/sources-check.mutant.mjs --self /tmp/tameshi-r18w2-SurvivorSVERDICT-8fpiB0/probe-corpus --today 2026-10-20
```
Captured outputs:
```text
pristine:
SOURCES  error  KIND_ENUM  corpus/SOURCES.md:6  id=S001 kind=not-a-kind
SOURCES_CHECK: DRIFT (KIND_ENUM)

mutant:
SOURCES  error  KIND_ENUM  corpus/SOURCES.md:6  id=S001 kind=not-a-kind
SOURCES_CHECK: DRIFT [KIND_ENUM]
```
The matching JSON-mode runs with `--json` each exited 1 and emitted the same JSON record with `verdict:"DRIFT"` and `exitCode:1` (full record in transcript). No install or external-state changes were made.

Verdict: S_VERDICT is externally distinguishable off-suite, and its mutant output violates the documented DRIFT-line contract.
