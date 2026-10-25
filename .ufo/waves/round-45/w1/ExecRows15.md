seat: ExecRows15

# C1 row re-verification: S086, S087 (author)

Item: C1 freshness re-verification of held registry rows S086 and S087, both npm
tarballs (mutation-testing-report-schema@3.9.0, mutation-testing-metrics@3.9.0).
Contract read (read-only) at `.ufo/evidence/round-45/contract.json`; counter reviewed
at `.ufo/evidence/round-45/freshness/measure.py` (`extract`/`grade`/`check`, lines
109-165, 271-297). Rows read raw from `corpus/SOURCES.md:95-96`. No tools installed
(uv/pacman/npx not needed; stock curl/python3/tar used).

## S086 — mutation-testing-report-schema 3.9.0

- URL (byte-exact first http(s) URL from source cell, SOURCES.md:95):
  `https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz`
- Fetch: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows15/S086.raw '<url>'`
  - curl exit: 0
  - bytes: 11872
  - sha256: `adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280`
- Member (anchor cites `package/src/mutation-testing-report-schema.json`): `package/src/mutation-testing-report-schema.json`
- Extract: `measure.py --extract S086.raw --member package/src/mutation-testing-report-schema.json` → exit 0
- Quote (6-25 tokens, verbatim from the extract output; 21 tokens):
  `"status": { "type": "string", "title": "MutantStatus", "description": "Result of the mutation.", "enum": ["Killed", "Survived", "NoCoverage", "CompileError", "RuntimeError", "Timeout", "Ignored", "Pending"] }`
  (shares content words `status`, `enum`, `mutation` with the row's anchor/teaches)
- CHECK: `CHECK S086 verified ok` (exit 0), run with
  `--lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S086.json --snapdir /tmp/tameshi-r45-ExecRows15`
- Verdict: holds. The live 3.9.0 tarball's report schema still carries the eight named
  `MutantStatus` enum values (anchor :88-93) and the top-level required array
  `[schemaVersion, thresholds, files]` (anchor :7), so teaches' "eight named statuses"
  and "requires schemaVersion, thresholds and files at the top level" claims hold.
- Fragment:

```json
{"id":"S086","url":"https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz","opened":"2026-10-25","verdict":"holds","raw_sha256":"adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280","quote":"\"status\": { \"type\": \"string\", \"title\": \"MutantStatus\", \"description\": \"Result of the mutation.\", \"enum\": [\"Killed\", \"Survived\", \"NoCoverage\", \"CompileError\", \"RuntimeError\", \"Timeout\", \"Ignored\", \"Pending\"] }","snapshot":".ufo/evidence/round-45/freshness/sources/S086.raw.gz","member":"package/src/mutation-testing-report-schema.json","author":"ExecRows15","note":"The live 3.9.0 tarball's report schema still lists the eight named MutantStatus enum values (anchor :88-93) and the top-level required array [schemaVersion, thresholds, files] (anchor :7), so teaches' eight-named-statuses claim holds."}
```

## S087 — mutation-testing-metrics 3.9.0

- URL (byte-exact first http(s) URL from source cell, SOURCES.md:96):
  `https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz`
- Fetch: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows15/S087.raw '<url>'`
  - curl exit: 0
  - bytes: 32668
  - sha256: `ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548`
- Member (anchor cites `package/src/model/metrics.ts`): `package/src/model/metrics.ts`
- Extract: `measure.py --extract S087.raw --member package/src/model/metrics.ts` → exit 0
- Quote (6-25 tokens, verbatim from the extract output; 24 tokens):
  `The total number of mutants that were detected, meaning either killed or caused a time out. * `killed + timed out` */ totalDetected: number;`
  (shares content words `killed`, `timed`, `detected`, `totalDetected` with the row's anchor/teaches)
- CHECK: `CHECK S087 verified ok` (exit 0), same invocation as S086 with S087.json
- Verdict: holds. The live 3.9.0 metrics.ts still defines `totalDetected` as killed + timed
  out (anchor :39-42), and the same file still carries `totalInvalid`/`totalValid`
  (anchor :50-58) and `mutationScore = totalDetected / totalValid * 100`
  (anchor :69-73), so teaches' detected-over-killed-plus-survived-plus-noCoverage
  arithmetic holds.
- Fragment:

```json
{"id":"S087","url":"https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz","opened":"2026-10-25","verdict":"holds","raw_sha256":"ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548","quote":"The total number of mutants that were detected, meaning either killed or caused a time out. * `killed + timed out` */ totalDetected: number;","snapshot":".ufo/evidence/round-45/freshness/sources/S087.raw.gz","member":"package/src/model/metrics.ts","author":"ExecRows15","note":"The live 3.9.0 metrics.ts still defines totalDetected as killed + timed out (anchor :39-42), and the same file still carries totalInvalid/totalValid and mutationScore = totalDetected / totalValid * 100 (anchors :50-58, :69-73), so teaches' detected-over-killed-plus-survived-plus-noCoverage arithmetic holds."}
```

## Artifacts
Raw snapshots kept at `/tmp/tameshi-r45-ExecRows15/S086.raw` and
`/tmp/tameshi-r45-ExecRows15/S087.raw` (with extract outputs `S086.txt`/`S087.txt`
and fragments `S086.json`/`S087.json`) for L1 integration into
`.ufo/evidence/round-45/freshness/sources/`.

## Risks / notes
- Both live tarballs match the pinned 3.9.0 shape; no drift observed. Both CHECK runs
  printed `verified ok`.
- S087's anchor also cites `package/src/calculateMetrics.ts:234-255`; the fragment carries
  one member, so the quote grounds the metrics.ts half of the teaches arithmetic
  (killed + timed out = detected), which is the claim's core; the same file also shows the
  mutationScore formula and totalInvalid/totalValid definitions.
- No blockers. Not run as measurement: only `--check` (seat helper) used, per bounds.
