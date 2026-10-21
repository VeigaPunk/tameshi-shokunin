# FAudit965 — scoped review (2026-10-21)

**Axes:** artifact integrity; execution/provenance; revision/input binding; historical applicability.

**Strongest assertion:** the final ancestor-run sentence in `audit-965.stdout:67` is unsupported by that captured trace, but not proven false. **Verdict: AGREE.** The retained line says “ancestor runs have the same instrument blobs as the read revision” (stdout:67; historical receipt reviewed 2026-10-21).

## Exact evidence and arithmetic

- Re-opened the retained stdout, empty stderr, `traces/L1/audit-965.json`, and matching `ledger.json` entry. At frozen revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`, `git show` hashes equal the checked stdout (`a66e51f6…8bdac`), trace (`5de115cf…f4303`), ledger (`d654f3d2…85939`), and round-19 `measure.py` (`bb651eef…5053`).
- Reproduced stdout size as 5,614 bytes; stderr is 0 bytes with the empty-file SHA-256. The stdout hash matches Audit965's measured value, but this remains a present-file measurement, not an expected hash bound into its trace/ledger.
- Read-only JSON comparison: trace `rev` and ledger `read_rev` both equal `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`; exit is 0; ledger `commands_executed_count` is 1. Trace has 14 inputs; ledger has 13, exactly the trace inputs minus `SKILL.md`. Neither binds `audit-965.stdout`.
- Trace `argv[32]` is one Python `-c` body: it reads the named section and paths, runs listed assertions, then prints the final sentence. It has no ancestor-run input or instrument-blob comparison. Thus the report's “unsupported by this receipt, not shown false” characterization is accurate; section hash is not stdout hash.

## C1 comparison / staleness

- The delivered round-19 ruler at `55e1…` explicitly scopes `PATHS` to the five `R18-1`–`R18-5` defects; Audit965's stdout, trace, and ledger are not in its input set. Its exact receipt/instrument checks bind a different round-18 measurement, not the ancestor statement in Audit965. I did not execute the ruler or selftests.
- `corpus/lessons/round-19.md:146-151` (2026-10-21) expressly records that the historical audit sentence is not established by its captured reads or reused as ancestry evidence; new refresh receipts separately retain output digests. This is an honest disposition/forward correction, not a retroactive change to Audit965's captured bytes. No stale finding or omitted C1 correction found.

**Concrete falsifier to this agreement:** an ancestor-run instrument manifest included in Audit965's trace inputs plus an executed, revision-bound equality comparison. The captured `argv` and input maps lack both; none was found.

**Residual unknowns / verification gaps:** whether ancestor runs actually used identical instrument blobs remains unknown; no conclusion that they differed is supported. `xd://lsp` is not mounted here, so no LSP status/references/definition/diagnostics were available; no grep result was used as semantic proof. This is a scoped evidence review, not round-admission authority.