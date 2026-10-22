# C2SchemaSource — source-of-truth metadata for mutation-testing-report-schema 3.9.0 / mutation-testing-metrics 3.9.0

Seat: TameshiR25.C2SchemaSource (leaf, no subagents). Scope: record publish date, license, repository URL,
plus one located quote each for the Position definition and the mutationScore formula.
All observations below are from live registry metadata and from the tarballs vendored in this lane
(`tools/vendor/`), extracted read-only into `/tmp/mte-src`. No production file touched; no installs needed.

## Verdict

Both packages are **Apache-2.0**, published **2026-07-27** from
`github.com/stryker-mutator/mutation-testing-elements` at shared `gitHead 00aa7bdc1da9df9f474e363cd70041ef4d389b4e`.
The vendored tarballs are **byte-identical to the published artifacts** (sha512 base64 matches `dist.integrity`
exactly for both). Both requested quotes located; the `Position` definition lives in the **report-schema**
package (it does not occur anywhere in the metrics package), the `mutationScore` formula in
`packages/metrics/src/calculateMetrics.ts:253`.

## 1. Registry metadata (observed)

Source: `https://registry.npmjs.org/<pkg>/3.9.0` and the packument `time` field, fetched with Python urllib.

| field | mutation-testing-report-schema 3.9.0 | mutation-testing-metrics 3.9.0 |
|---|---|---|
| publish date (packument `.time["3.9.0"]`) | **2026-07-27T10:31:57.725Z** | **2026-07-27T10:39:14.991Z** |
| license | **Apache-2.0** | **Apache-2.0** |
| repository | `git+https://github.com/stryker-mutator/mutation-testing-elements.git`, `directory: packages/report-schema` | same URL, `directory: packages/metrics` |
| gitHead | `00aa7bdc1da9df9f474e363cd70041ef4d389b4e` | `00aa7bdc1da9df9f474e363cd70041ef4d389b4e` |
| dist.integrity | `sha512-28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ==` | `sha512-E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==` |
| slsa provenance | present (`dist.attestations.provenance`, GitHub Actions OIDC trusted publisher) | present, same |
| npm page | `https://www.npmjs.com/package/mutation-testing-report-schema` — "Latest: 3.9.0 · License: Apache-2.0", weekly downloads 2.3M | `https://www.npmjs.com/package/mutation-testing-metrics` — same header, dependency `mutation-testing-report-schema: 3.9.0` (exact pin) |

Note: `www.npmjs.com` returns **403** to `curl` (bot protection); the npm page content above was read through
the reader's npm route (registry-backed). The registry JSON is the authoritative source and was read directly.
`dist-tags.latest` for both packages is `3.9.0`.

Command (observed output):
```
$ python3 -c '...urllib packument...'
mutation-testing-report-schema 3.9.0 published: 2026-07-27T10:31:57.725Z | modified: 2026-07-27T10:31:58.056Z | license: Apache-2.0 | repo: {'url': 'git+https://github.com/stryker-mutator/mutation-testing-elements.git', 'type': 'git', 'directory': 'packages/report-schema'}
mutation-testing-metrics 3.9.0 published: 2026-07-27T10:39:14.991Z | modified: 2026-07-27T10:39:15.255Z | license: Apache-2.0 | repo: {'url': 'git+https://github.com/stryker-mutator/mutation-testing-elements.git', 'type': 'git', 'directory': 'packages/metrics'}
```

## 2. Vendored artifacts match the published artifacts (observed)

```
$ sha512sum tools/vendor/mutation-testing-{report-schema,metrics}-3.9.0.tgz | cut -d' ' -f1 | xxd -r -p | base64 -w0
mutation-testing-metrics-3.9.0.tgz       E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==
mutation-testing-report-schema-3.9.0.tgz 28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ==
```
Both base64 digests equal the registry `dist.integrity` values in §1 — the vendored tarballs ARE the published
3.9.0 artifacts (not re-rolled builds). This is the strongest available evidence that a schema/metrics consumer
inside this lane is validating against the official bytes.

## 3. Position definition (observed)

Located in the **report-schema** package. Published artifact (vendored tarball member
`package/dist/src/mutation-testing-report-schema.json`, `definitions.position`) and GitHub source
`packages/report-schema/src/mutation-testing-report-schema.json:306-321` (verified 200 at pinned commit
`00aa7bdc`; the two are identical after JSON normalization — the published dist copy is 4-space indented,
the GitHub src copy 2-space indented, no semantic difference).

Quote (10 words), `packages/report-schema/src/mutation-testing-report-schema.json:309`:
> "Position of a mutation. Both line and column start at one."

Full definition (observed):
```json
"position": {
  "type": "object",
  "title": "Position",
  "description": "Position of a mutation. Both line and column start at one.",
  "required": ["line", "column"],
  "properties": {
    "line":   { "type": "integer", "minimum": 1, "examples": [4] },
    "column": { "type": "integer", "minimum": 1, "examples": [3] }
  }
}
```
Generated TypeScript twin, `package/dist/src-generated/schema.d.ts:108-113`:
`/** Position of a mutation. Both line and column start at one. */ export interface Position { line: number; column: number; }`
Referenced by `definitions.location` (`#/definitions/position` at lines 331, 334) and `definitions.openEndLocation`
(lines 345, 348), and `location` in turn is referenced from the mutant definition (line 72).

**`Position` does NOT occur anywhere in the metrics package** — `grep -rn 'Position' package/{src,dist}` over the
extracted metrics tarball returns zero hits. If a seat cites "Position" as a metrics symbol, that is wrong; it is a
report-schema type.

## 4. mutationScore formula (observed)

`packages/metrics/src/calculateMetrics.ts:253` (GitHub src at pinned commit is byte-identical to the tarball's
`package/src/calculateMetrics.ts` — `diff -q` silent):

Quote (13 words), `packages/metrics/src/calculateMetrics.ts:253`:
> `mutationScore: totalValid > 0 ? (totalDetected / totalValid) * 100 : DEFAULT_SCORE,`

Context (observed, same file): `:9` `const DEFAULT_SCORE = NaN;`; `:234` `const totalDetected = timeout + killed;`;
`:236` `const totalUndetected = survived + noCoverage;`; `:237` `const totalValid = totalUndetected + totalDetected;`.
So `mutationScore = (killed + timeout) / (killed + timeout + survived + noCoverage) * 100`, and **`NaN` when
totalValid == 0**. Sibling formula `:255` `mutationScoreBasedOnCoveredCode: totalValid > 0 ? (totalDetected / totalCovered) * 100 || 0 : DEFAULT_SCORE`
with `:235` `totalCovered = totalDetected + survived` — note the extra `|| 0` there (0 coverage → 0, not NaN).
Compiled twin: `package/dist/src/calculateMetrics.js:189` (and `:5` for `DEFAULT_SCORE`).

**NaN-serialization caveat for MTE report consumers:** `DEFAULT_SCORE = NaN` means a report with zero valid
mutants carries `NaN`, which JSON cannot express; any emitter must decide the encoding (the official MTE metrics
pipeline emits `null`/omits — [INFERENCE], not verified here; the schema's `thresholds` object, not `metrics`,
is what the report schema pins).

## 5. Repo/path facts useful to sibling seats (observed)

- `packages/metrics/src/calculateMetrics.ts` — 200 at pinned commit; identical to tarball src.
- `packages/report-schema/src/mutation-testing-report-schema.json` — 200 at pinned commit; semantically identical to tarball dist copy.
- `packages/report-schema/src/index.ts` — 200.
- `packages/report-schema/dist/src/mutation-testing-report-schema.json` and `packages/metrics/dist/src/calculateMetrics.js`
  — **404 on GitHub**: `dist/` is build output and exists only inside the npm tarballs. Cite dist paths as
  *tarball member* paths (`package/dist/...`), not GitHub paths, or the citation is wrong.
- Package export map (report-schema): `.` → `dist/src/index.js`, `./api` → `dist/src-generated/schema.js`,
  `./mutation-testing-report-schema.json` → `dist/src/mutation-testing-report-schema.json` (the last one is the
  importable schema path for validators). metrics exports only `.`.
- Both packages are ESM (`"type": "module"`).

## Remaining unknowns

- The packument `time` field gives the publish instant but the git commit date of `gitHead` was not fetched
  (would need the GitHub commit API; not required by the ticket).
- `www.npmjs.com` page rendered content (download graph, "published X ago" phrasing) was not read literally —
  403 to curl; the registry-backed page summary above stands in.
- No verification of how the metrics package serializes `NaN` in the MTE report wire format (out of scope;
  flagged as a caveat in §4).

## Tooling

No installs or upgrades performed; all reads via the reader's HTTP/registry routes, `curl -s -o /dev/null -w %{http_code}`
for path liveness, and read-only tarball extraction into `/tmp/mte-src`.
