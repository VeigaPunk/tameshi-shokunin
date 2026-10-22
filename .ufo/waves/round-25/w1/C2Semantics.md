# C2Semantics — does tameshi INCONCLUSIVE map to RuntimeError better than to Timeout?

Seat: TameshiR25.C2Semantics (leaf, no subagents). Scope: read the official mutant-states page, quote the
five requested definitions, and judge the `INCONCLUSIVE -> RuntimeError` mapping at
`tools/mte-interop.py:58` against those definitions. No production file touched.

**Access date: 2026-10-22** (fetch of the canonical URL, reader's native route, `Content-Type: text/html`,
page meta `generator: Docusaurus v3.10.2`, `docusaurus_version: current`; the page exposes no "last updated"
stamp). Same page was previously opened 2026-10-19 for
`corpus/knowledge/mutation-score-semantics.md` (its source S001, `verified-at: 2026-10-19`); today's fetch
re-verifies it and the quoted sections are unchanged.

## Verdict

**Yes — `RuntimeError` is the better mapping, and `Timeout` would be wrong for tameshi's semantics.**
Decisive reason: MTE counts `Timeout` as **detected** and inside **valid**, while tameshi's rule is
"Inconclusive … Not a kill" and "Kill rate = killed / (killed + survived) — inconclusive runs are excluded
from the denominator" (`SKILL.md:208-210`). `RuntimeError` is the only one of the two that MTE excludes from
`valid` and from the score, which is exactly what tameshi does with an inconclusive. The mapping is a
compromise on *wording* (see §5, the merged bucket) but exact on *arithmetic* (§4).

## 1. Verbatim definitions (fetched 2026-10-22; each quote <= 25 words)

Source: `https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/`

| State | Quote | Words |
|---|---|---|
| **Killed** | "When at least one test failed while this mutant was active, the mutant is killed." | 15 |
| **Survived** | "When all tests passed while this mutant was active, the mutant survived. You're missing a test for it." | 18 |
| **Timeout** | "The running of tests with this mutant active resulted in a timeout." … "It is counted as 'detected'." | 17 |
| **Runtime error** | "The running of the tests resulted in an error (rather than a failed test)." … "It is not represented in your mutation score." | 22 |
| **Mutation score** | "`detected / valid * 100` … The total percentage of mutants that were detected. The higher, the better!" | 15 |

Supporting metric lines quoted from the same page, needed for the argument (§Metrics):

- "**Detected** `killed + timeout` — The number of mutants detected by your tests."
- "**Valid** `detected + undetected` — The number of valid mutants. They didn't result in a compile error or runtime error."
- "**Invalid** `runtime errors + compile errors` — The number of invalid mutants."

## 2. What tameshi's INCONCLUSIVE actually is (observed, in-lane)

- `SKILL.md:208-209`: "**Inconclusive** = no definitive verdict (timeout, crash before the summary, count not enumerated). **Not a kill.**"
- `SKILL.md:210-212`: "**Kill rate = killed / (killed + survived)** — inconclusive runs are excluded from the denominator and named beside it."
- `SKILL.md:845-846` (runner contract): "KILLED (suite exit ≠ 0) / SURVIVED (exit 0) / INCONCLUSIVE (timeout 124, or 126/127 not runnable)."
- `tools/mutate-and-run.sh:79` exit map: "0 done · 1 done-with-inconclusive (DEGRADED) · 2 setup/refusal · 64 usage error"; headline at `:563-566` is `MUTATE: DEGRADED (… killed=… survived=… inconclusive=… kill-rate=…%)`, exit 1.
- Runner selftest asserts the record literally: `tools/mutate-and-run.sh:1536-1538` — `DEFECT K: INCONCLUSIVE (exit=124 note=timeout`, `DEFECT S: SURVIVED (exit=0`, `MUTATE: DEGRADED (target=fixture defects=2 killed=0 survived=1 inconclusive=1 kill-rate=0%)`.

So tameshi's bucket is "the run produced no verdict": a timeout (124), an unrunnable run (126/127), a crash
before the summary, or a missing count. Only Killed and Survived are verdicts; INCONCLUSIVE is deliberately
outside the score.

## 3. The two candidate mappings against those definitions

Mapping site: `tools/mte-interop.py:58` — `STATUS = {'KILLED': 'Killed', 'SURVIVED': 'Survived', 'INCONCLUSIVE': 'RuntimeError'}`.
Both `RuntimeError` and `Timeout` are legal in the vendored schema 3.9.0 enum
(`tools/vendor/mutation-testing-report-schema-3.9.0.tgz`, member
`package/src/mutation-testing-report-schema.json`, `properties.files.additionalProperties.properties.mutants.items.properties.status.enum`
= `["Killed","Survived","NoCoverage","CompileError","RuntimeError","Timeout","Ignored","Pending"]`), so the
schema does not decide the question — semantics do.

| | RuntimeError (current) | Timeout (rejected alternative) |
|---|---|---|
| Definitional fit | "the running of the tests resulted in an error (rather than a failed test)" — a run with **no verdict** is precisely not-a-failed-test; "not represented in your mutation score" matches tameshi excluding inconclusives | Matches only the exit-124 sub-case; its stated policy "counted as 'detected'" is the **opposite** of `SKILL.md:208` "Not a kill" |
| Official `detected` | `killed` | `killed + inconclusive` — asserts a detection tameshi never observed |
| Official `valid` | `killed + survived` (= tameshi's denominator) | `killed + inconclusive + survived` — inconclusives enter the denominator |
| Official `mutationScore` | `killed/(killed+survived)*100` — identical to `SKILL.md:210` | `(killed+inconclusive)/(killed+inconclusive+survived)*100` — diverges |
| Direction of error | conservative: an inconclusive is unscored, never claimed as detected | optimistic: fabricates detections |

The arithmetic is the pinned official implementation, not the docs' prose alone: vendored
`mutation-testing-metrics-3.9.0.tgz` → `package/dist/src/calculateMetrics.js`, `toMetrics(...)`:
`totalDetected = timeout + killed`, `totalUndetected = survived + noCoverage`,
`totalValid = totalUndetected + totalDetected`, `totalInvalid = runtimeErrors + compileErrors`,
`mutationScore = totalValid > 0 ? (totalDetected / totalValid) * 100 : NaN`. (Sibling seat C2SchemaSource
pins the same lines in the TS source, `packages/metrics/src/calculateMetrics.ts:234-255` —
`.ufo/waves/round-25/w1/C2SchemaSource.md` §4.)

**Numeric witness on an observed record.** The runner's own DEGRADED fixture row
(`killed=0 survived=1 inconclusive=1`, `tools/mutate-and-run.sh:1538`) gives: RuntimeError mapping →
`mutationScore = 0/(0+1) = 0 %` = tameshi's rate; Timeout mapping → `detected = 1`, `valid = 2`,
`mutationScore = 50 %` — a 50-point divergence from the record, on a mutant the runner explicitly labelled
"Not a kill". That is the whole argument in one row.

## 4. Consequence for the interop judge (arithmetic, observed)

`tools/mte-interop.py:206-212`: `tameshi_score = 100*killed/(killed+survived)`; check `score` compares it to
`official['mutationScore']`; check `ledger` requires `official['killed'] == recorded-killed` **and**
`official['totalValid'] == recorded defects`.

- Under the current RuntimeError mapping both checks are satisfiable exactly when the fresh measurement equals
  the recorded ledger (`official killed == recorded-killed`) and `inconclusive = 0`. Observed: all
  eight fleet legs carry `inconclusive=0` in their recorded rows — e.g.
  `.ufo/evidence/round-24/replay/observations.json:883-884` (and the same rows in
  `.ufo/evidence/round-24/noharm-c8c5b88.json:355`) show `REGRESSION_TABLE bash-tsukuroi-census: match=10/10
  recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0`, and the swept distinct rows for the
  eight legs all read `inconclusive=0` with `killed + survived = defects`. So the current mapping is what makes
  the 8/8 target reachable.
- Under the Timeout mapping, `official['mutationScore']` would leave tameshi's rule as soon as
  `inconclusive > 0`, failing the `score` check on exactly the DEGRADED legs the runner flags.

**Flagged limitation (not a mapping defect).** Because tameshi's own "valid" excludes inconclusives, the
`ledger` check as written (`totalValid == recorded defects`) is satisfiable for a leg with `inconclusive > 0`
under *neither* mapping: RuntimeError gives `totalValid = killed+survived < defects`; Timeout passes that check
but fails `score`. [INFERENCE] If such a leg is ever judged, the minimal change consistent with these
definitions is to compare `official['totalMutants']` (valid + invalid + ignored + pending = `killed + survived +
inconclusive` = defects) with the recorded defect count, leaving the RuntimeError mapping and the `score` check
untouched. **Not applied** — lane bounds forbid editing production files.

## 5. Residuals and unknowns

- **Merged bucket.** `INCONCLUSIVE` merges a literal timeout (exit 124) with unrunnable runs (126/127) and other
  no-verdict cases. A split mapping (124 → `Timeout`, 126/127 → `RuntimeError`) would match each sub-case's
  wording, but it would re-introduce "timeouts count as detected" and break the score agreement above, so it is
  worse for this interop, not better. [INFERENCE] The discriminator is in the data — `results.tsv` column 3 is
  `exit` (`tools/mutate-and-run.sh:531`: `id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc`) — but
  `leg_report` reads only columns 1-2 (`tools/mte-interop.py:126-127`), so the emitted report cannot express the
  split today. Recorded as an observation, no change proposed.
- **Headline vs rule denominator (observation only).** The runner's headline percentage uses the defect count as
  denominator (`tools/mutate-and-run.sh:562`: `pct=$(( (200 * killed + total) / (2 * total) ))`, printed as
  `kill-rate=`), while `SKILL.md:210` and the interop judge use `killed/(killed+survived)`. The two coincide on
  every observed record, because every observed leg and fixture has `inconclusive = 0` or `killed = 0`; they
  differ arithmetically only when `killed > 0` **and** `inconclusive > 0` at once, a combination I did not
  observe in any record. [INFERENCE] Flagged for the planner; no correction proposed from this seat.
- **Page versioning.** The page carries no date or version pin beyond `docs-default-current`; the durable
  artifacts for this question are the vendored 3.9.0 tarballs (sha512-verified, byte-identical to the published
  artifacts per C2SchemaSource §2), which is why the arithmetic above is cited from the tarball and not only from
  the prose.
- **Unknown.** Whether MTE's own UI/consumer treats `RuntimeError` mutants as reportable-but-unscored in every
  downstream tool was not investigated (out of scope: the question is the definition and the score).

## 6. Tooling

No installs, upgrades or host changes. Reads only: one HTTP fetch of the canonical docs URL, read-only tarball
extraction into `/tmp/schemaprobe` and `/tmp/metprobe`, and in-lane reads. No command was run inside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` beyond read-only `grep`/`sed`; no gate, selftest or sweep was
executed by this seat.
