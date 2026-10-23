# Reopen S087

Verdict: disagree. The reopened 3.9.0 tarball is the same bytes as row S087 and the local pin, and it does compute several derived totals as sums of selected status counts. It does not support the fix comment's claim that "a total must equal the sum of per-state counts" is why a regression tally that does not sum to `nlegs` must refuse as SETUP.

Axes used: byte identity of the reopened tarball, exact source lines for those sums, and whether those lines are the rationale in the fix comment.

## Identity

Reopened by curl, not from the sealed tree.

```
curl -fsSL -o /fast/scratch/hyaku/tameshi-r30a2-seats/ReopenS087-11/m.tgz \
  https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz
```

Observed: 32668 bytes.

```
openssl dgst -sha256 -r /fast/scratch/hyaku/tameshi-r30a2-seats/ReopenS087-11/m.tgz
ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548

openssl dgst -sha512 -binary /fast/scratch/hyaku/tameshi-r30a2-seats/ReopenS087-11/m.tgz | openssl base64 -A
E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==
```

Row S087 at `f09d3425258403a51422c9959e25340807982947:corpus/SOURCES.md` (1115 characters) records that same sha512, without the `sha512-` prefix, plus `gitHead 00aa7bdc1da9df9f474e363cd70041ef4d389b4e` and repository directory `packages/metrics`.

Registry metadata `https://registry.npmjs.org/mutation-testing-metrics/3.9.0` returns `dist.integrity` `sha512-E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==`, the same tarball URL, and the same `gitHead`. `package/package.json` inside the tarball is `mutation-testing-metrics` `3.9.0` with that `gitHead` and `"directory": "packages/metrics"`.

Local pin `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/sources/S087-mutation-testing-metrics-3.9.0.tgz` has the same sha256 and the same sha512. `cmp -s` of the two files printed `CMP_EQUAL`.

No tool was installed.

## Quotes

Paths are members of that tarball (`package/` stripped in the citation, matching the S087 row). Each quote is at most 25 words. The same assignments are in `package/dist/src/calculateMetrics.js:170-174` and `:190`.

Sums the library actually assigns (`package/src/calculateMetrics.ts`, function `toMetrics`):

- `package/src/calculateMetrics.ts:234` — `const totalDetected = timeout + killed;`
- `package/src/calculateMetrics.ts:235` — `const totalUndetected = survived + noCoverage;`
- `package/src/calculateMetrics.ts:236` — `const totalCovered = totalDetected + survived;`
- `package/src/calculateMetrics.ts:237` — `const totalValid = totalUndetected + totalDetected;`
- `package/src/calculateMetrics.ts:238` — `const totalInvalid = runtimeErrors + compileErrors;`
- `package/src/calculateMetrics.ts:254` — `totalMutants: totalValid + totalInvalid + ignored + pending,`

Comments that describe those sums (`package/src/model/metrics.ts`). Two of them do not match the assignments above:

- `package/src/model/metrics.ts:41` — `` `killed + timed out` ``
- `package/src/model/metrics.ts:46` — `` `survived + no coverage` ``
- `package/src/model/metrics.ts:51` — `` `runtimeErrors + transpileErrors` ``
- `package/src/model/metrics.ts:56` — `` `totalDetected + totalUndetected` ``
- `package/src/model/metrics.ts:61` — `` `totalInvalid + totalValid` ``
- `package/src/model/metrics.ts:66` — `` `totalDetected + survived + ignored` ``

`totalMutants` in the comment (`metrics.ts:61`) is only invalid plus valid. The code (`calculateMetrics.ts:254`) also adds `ignored` and `pending`. `totalCovered` in the comment (`metrics.ts:66`) adds `ignored`. The code (`calculateMetrics.ts:236`) does not.

Counts, not a checked equality:

- `package/src/calculateMetrics.ts:187` — `countByStatus[mutant.status]++;`
- `package/src/calculateMetrics.ts:190-198` — only the eight named keys (`Pending`, `Killed`, `Timeout`, `Survived`, `NoCoverage`, `RuntimeError`, `CompileError`, `Ignored`) are passed into `toMetrics`.
- `package/src/calculateMetrics.ts:146` — `metrics.total++;` runs for every test, before the status switch at `:147-157`. `total` is not assigned as `killing + covering + notCovering`.

There is no comparison of a derived total to a mutant count or a test count, and no refusal if they differ.

## Why that does not carry the fix comment

The comment under test is `.ufo/evidence/round-30/witness/fix.diff:9-12`:

> A PASS needs every one of the nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals of a mutation report are sums of its per-state counts).

What the source does support, which is also what row S087 itself says it is for: a detected mutant is killed or timed out; valid is that plus survived plus no coverage; compile and runtime errors are invalid and stay out of the score. See `metrics.ts:39-42`, `:50-58`, `:69-73`, and `calculateMetrics.ts:234-238` and `:253`. The row's use text is that kill-rate comparison, not a tally that must match a population.

What it does not support:

- A requirement. Totals are computed from the status counts. Nothing checks that a total already equals those counts.
- A population check. `totalMutants` is the sum of eight buckets by construction. It is not compared with the number of mutants, and a status outside those eight keys is left out of `totalMutants` with no error (`calculateMetrics.ts:187-198` and `:254`).
- A refusal. The library returns the metrics. The SETUP exit in the fix is not in this package.
- One rule for every total. `totalDetected`, `totalValid`, `totalInvalid`, and `totalCovered` each omit some statuses. Pending and ignored are inside `totalMutants` and outside `totalValid`, which is the score denominator (`calculateMetrics.ts:237` and `:253-254`).
- The test total. `metrics.total` is a separate increment (`calculateMetrics.ts:146`). It can exceed `killing + covering + notCovering` when a status matches none of the three cases, and the function still returns.

So the parenthetical is a loose description of some derived fields, not a rule the `nlegs` guard can cite. The three regression buckets are not this library's status partition.

## Smallest safe correction

Delete the parenthesis from the fix comment. Keep the local check (`npass + nfail + nsetup != nlegs` refuses as SETUP) as this tool's own completeness guard, with no S087 citation.

If a citation stays, limit it to the arithmetic that is actually there: `totalMutants` is defined as the sum of the eight known status counts (`package/src/calculateMetrics.ts:254`). Do not say the library requires that sum to equal an outside count, or that a mismatch must refuse.

## Unresolved

None for this question. The sealed set was not opened. The published `dist` JavaScript matches the TypeScript assignments cited above; no second formula was found.
