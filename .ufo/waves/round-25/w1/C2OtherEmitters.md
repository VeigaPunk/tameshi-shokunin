# C2OtherEmitters — which mutation tools emit mutation-testing-elements JSON

Round 25 / wave 1, seat C2OtherEmitters (2026-10-22). Question: besides this lane's
ledger, which mutation tools emit the mutation-testing-elements (MTE) report JSON — the
format `tools/mte-interop.py` validates against schema 3.9.0 and scores with metrics
3.9.0 (both vendored, sha512-pinned, in `tools/vendor/`).

## Verdict

- **Native MTE JSON emitters:** StrykerJS, Stryker.NET, Stryker4s, Mull, pitest (through
  the third-party `io.github.wmaarts:pitest-mutation-testing-elements-plugin`),
  muttest (R), irradiate (Python).
- **Partial emitter:** Infection (PHP). It builds an MTE report and embeds it in its HTML
  dashboard, and can upload it to the Stryker Dashboard; it has no standalone MTE JSON
  log target.
- **Not emitters:** cargo-mutants (own `mutants.out/mutants.json`), mutmut (Shields
  endpoint JSON only).

| Tool | Ecosystem | MTE JSON | How it is produced | `schemaVersion` written | MTE version pinned |
| --- | --- | --- | --- | --- | --- |
| StrykerJS | JS/TS | yes | `json` reporter (default `reports/mutation/mutation.json`); `html` renders MTE | `"1.0"` | 3.8.4 (elements, metrics, report-schema) |
| Stryker.NET | C# / .NET | yes | `--reporter json`; same report feeds the HTML reporter | `"2"` | 3.9.0 (libman) |
| Stryker4s | Scala | yes | `json` reporter beside `html` | `"2"` (test expectation) | 3.9.0 (elements + metrics) |
| Mull | C / C++ | yes | `Elements` reporter writes `<name>.json` + `<name>.html` | `"1.7"` | hand-serialised, no package pin |
| pitest | Java | yes, via plugin | output formats `JSON` / `HTML2` | not observed | 3.9.0 (plugin pom) |
| muttest | R | yes | `JSONMutationReporter` (0.3.0) | not observed | claimed, no pin |
| irradiate | Python | yes | `--report json` | claimed "v2" | claimed, no pin |
| Infection | PHP | partial | MTE JSON embedded in `html` log; `stryker` log uploads it | `"1"` | CDN `mutation-testing-elements` latest, unpinned |
| cargo-mutants | Rust | no | own `mutants.out/mutants.json` | — | — |
| mutmut | Python | no | `export-cicd-stats` → Shields endpoint JSON | — | — |

## Evidence per tool

Quotes are from the primary pages opened for this seat; each is ≤25 words.

### StrykerJS (JavaScript/TypeScript)

- Doc (repo source of <https://stryker-mutator.io/docs/stryker-js/configuration/>),
  `stryker-js/docs/configuration.md:487`: "These reporters can be used out of the box:
  `html`, `json`, `progress`, `clear-text`, `dots`, `dashboard` and `event-recorder`."
- Source contract, `stryker-js/packages/api/src/report/reporter.ts:32-33`: "the
  mutation test result that is valid according to the mutation-testing-report-schema
  (json schema)".
- Emitted version: `stryker-js/packages/core/src/reporters/mutation-test-report-helper.ts:248`
  sets `schemaVersion: '1.0'`; pin `packages/core/package.json:83-85` =
  `mutation-testing-elements` / `mutation-testing-metrics` /
  `mutation-testing-report-schema` all `3.8.4`.

### Stryker.NET (C#/.NET)

- Doc page <https://stryker-mutator.io/docs/stryker-net/reporters/>, Json reporter
  section: "This reporter outputs a json file with all mutation testrun info of the last
  run." and "The json is also used for the HTML reporter".
- The same page states the dashboard reporter will "upload your stryker result as json
  to the stryker dashboard" — the consumer expects the MTE schema.
- Emitted version: `stryker-net/src/Stryker.Core/Stryker.Core/Reporters/Json/JsonReport.cs:14`
  `public string SchemaVersion { get; init; } = "2";`
- Pin: `stryker-net/src/Stryker.Core/Stryker.Core/libman.json:6`
  `"library": "mutation-testing-elements@3.9.0"` — the same 3.9.0 revision this round
  vendors.

### Stryker4s (Scala)

- Doc (repo source of <https://stryker-mutator.io/docs/stryker4s/configuration/>),
  `stryker4s/docs/configuration.md:145`: "The JSON is in the
  mutation-testing-report-schema format." (the same bullet names the `html` reporter as
  "mutation-testing-elements" at line 144).
- Emitted version: `stryker4s/modules/core/src/test/scala/stryker4s/report/HtmlReporterTest.scala:27`
  expects `"schemaVersion":"2"` (test expectation, not a live run).
- Pin: `stryker4s/project/Dependencies.scala:45,47` = `mutationTestingElements` and
  `mutationTestingMetrics` `"3.9.0"`, consumed at lines 78-82.

### Mull (C/C++)

- Doc page <https://mull-project.com/reference/reporters/>, "Elements HTML" section:
  "This reporter generates a self-contained HTML report in that format." and "By default,
  it generates the report in the current working directory `$timestamp.html`/`$timestamp.json`."
- Repo `mull/docs/Features.rst:22`: "JSON file that conforms `mutation-testing-elements
  schema`" (line 24: "`Mutation Testing Elements HTML Reporter`").
- Repo `mull/rust/mull-reporters/src/elements_reporter.rs:11`:
  `/// Mutation Testing Elements schema version 1.7`; writes `schema_version: "1.7"`
  (line 239) and maps statuses Killed/Survived/NoCoverage/Timeout/RuntimeError
  (`execution_status_to_mutant_status`).

### pitest (Java) — third-party plugin only

- Plugin README
  <https://raw.githubusercontent.com/Wmaarts/pitest-mutation-testing-elements-plugin/master/README.md>:
  "`JSON` for a JSON file of stryker mutation-testing-elements format" and `HTML2` for
  the Stryker HTML report. The plugin is `io.github.wmaarts`, not part of pitest.
- Pin: `pitest-mte/pom.xml:67-69` depends on `io.stryker-mutator:mutation-testing-elements`
  `3.9.0` — again the exact revision vendored here.
- Not checked: which schema revision each published plugin release emits; the README's
  Maven snippet still shows plugin version 0.6.5 while the pom is a MASTER-SNAPSHOT.

### Infection (PHP) — partial

- Doc page <https://infection.github.io/guide/usage.html>, `logs` section: "human-readable
  report, similar to PHPUnit HTML report. Based on Stryker Elements."
- Implementation: `infection/src/Reporter/Html/HtmlFileReporter.php:60` loads
  `mutation-testing-elements` from jsDelivr (unpinned) and assigns
  `app.report = {…}` from `StrykerHtmlReportBuilder`; that builder writes
  `'schemaVersion' => '1'` (`.../StrykerHtmlReportBuilder.php:116`).
- `infection/src/Reporter/Http/StrykerCurlClient.php:58` cites the MTE report schema for
  the dashboard upload (`logs.stryker`, `StrykerReporter`).
- No standalone MTE JSON target exists: `infection/src/Configuration/Entry/Logs.php:39-51`
  enumerates `text`, `html`, `summary`, `json`, `gitlab`, `debug`, `perMutator`, `github`,
  `stryker`, `summaryJson`, `debugEvents` — the `json` log is Infection's own format.

### muttest (R) and irradiate (Python) — documented only, not exercised

- muttest NEWS 0.3.0, <https://cran.r-project.org/web/packages/muttest/news/news.html>:
  "New `JSONMutationReporter` writes a report conforming to the mutation-testing-elements
  schema"; the entry continues "cross-language standard shared by StrykerJS/.NET/Scala".
- irradiate README, <https://raw.githubusercontent.com/nwyin/irradiate/main/README.md>:
  "`--report json` # Stryker mutation-testing-report-schema v2" and "compatible with the
  Stryker Dashboard". Both are the projects' own claims; neither was run.

### cargo-mutants (Rust) — not an emitter

- Doc page <https://mutants.rs/list.html>: "Diffs are always included in JSON output.
  (The same format is written to `mutants.out/mutants.json` when running tests.)"
- <https://mutants.rs/output.html> describes only stdout/stderr display options, no MTE.
- Repo check at `6c720ae82a1784b84cfa06066f7b0d59ed1798d0`:
  `grep -rn -i 'stryker\|mutation-testing-elements' cargo-mutants --exclude-dir=.git`
  → no output (whole clone, including `book/src/integrations.md`, which lists only
  shell completion and a vim plugin).
- Ecosystem converter exists and is honest about being a converter:
  <https://raw.githubusercontent.com/max-te/mutant-report/master/README.md> — "We convert
  the cargo-mutants output into a Stryker-compatible json format".

### mutmut (Python) — not an emitter

- `mutmut/README.rst:628`: "`mutmut badge` turns `mutmut export-cicd-stats` output into
  Shields endpoint JSON" — the only JSON mentioned.
- Repo check at `7d5fff33cff22da5f6d0eb1a7bdc764362444221`:
  `grep -rn -i 'stryker\|mutation-testing-elements' mutmut/README.rst mutmut/docs` → only
  the Shields sentence above; no MTE mention.

## What this means for comparing sibling-lane gates

- Three emitters pin exactly the revision this round vendors — Stryker.NET (libman 3.9.0),
  Stryker4s (Maven 3.9.0), pitest plugin (Maven 3.9.0). A leg produced by any of them is
  validated by the same schema revision and scored by the same metrics version as our
  legs, so a comparison needs no version reconciliation.
- StrykerJS pins 3.8.4 and writes `schemaVersion: "1.0"`; that is still accepted by the
  3.9.0 schema, whose `schemaVersion` pattern is
  `^([1-2])(\.(([1-9]\d*)|0)){0,2}$` (verified in
  `tools/vendor/mutation-testing-report-schema-3.9.0.tgz`, member
  `package/src/mutation-testing-report-schema.json`). Metrics differ by one minor
  (3.8.4 vs 3.9.0), so scores are comparable but not from an identical library build.
- Mull writes 1.7 and only the status subset Killed/Survived/NoCoverage/Timeout/
  RuntimeError; all of those are in the 3.9.0 enum, so it validates, but the report
  carries no `framework`/`config` metadata and no package pin to cite.
- Infection cannot be read as a file: its MTE JSON lives inside the HTML as
  `app.report = {…}`; ingesting it means extracting that object.
- Any imported leg must supply `files[*].source` and per-mutant `id`, `mutatorName`,
  `location`, `status` — those are the schema's `required` fields (verified in the
  vendored 3.9.0 schema). `tools/mte-interop.py` already emits all of them
  (`mte-interop.py:146-161`).
- cargo-mutants and mutmut would each need a converter before a gate could be compared;
  mutmut has no MTE converter in evidence in this pass.

## Sibling-lane scan (negative)

A name-and-config scan of the fleet root `/home/vgpnk/Projects/shokunin` (depth ≤ 6,
`node_modules`/`.git` excluded, config file extensions plus `Cargo.toml`/`pom.xml`/
`pyproject.toml`, and named files `mutants.toml`, `stryker.conf.*`, `stryker.config.*`,
`mull.yml`, `infection.json*`) found no repository that configures any of these tools.
The only fleet-wide text hit for these names is a lesson sentence mentioning pitest
inside `MANIFEST.json` (`S063`, "pitest f7fe5adf DetectionStatus.java:63"). So no sibling
gate can be compared today; this list is the menu, not a description of existing lanes.
Scope limit: filename/content scan only — a tool invoked from a script under another
name would be missed.

## Revisions and method

Shallow, read-only clones into `/tmp/emitters` (public GitHub, default branch, cloned
2026-10-22):

| Clone | HEAD |
| --- | --- |
| cargo-mutants | `6c720ae82a1784b84cfa06066f7b0d59ed1798d0` |
| mutmut | `7d5fff33cff22da5f6d0eb1a7bdc764362444221` |
| infection | `b9c50e56afe00cb3d6f62adf7b9c4354177afdb1` |
| stryker-js | `c931a93237816901f1e9f48da411170beeb3dfca` |
| stryker4s | `6f42804f6b477ffeded96df433188ff874653594` |
| stryker-net | `02e1307655a3661f9da984a31355fcdc21bcbea9` |
| mull | `5ac9d612b1fa0ad984a9f898fe20eb0378164a7b` |
| pitest-mutation-testing-elements-plugin | `ebf361d1666862701612c54fc479470f75998147` |

Reproduce the core negative result:

```
mkdir -p /tmp/emitters && cd /tmp/emitters
git clone -q --depth 1 https://github.com/sourcefrog/cargo-mutants
git clone -q --depth 1 https://github.com/boxed/mutmut
grep -rn -i 'stryker\|mutation-testing-elements' cargo-mutants --exclude-dir=.git   # no output
grep -rn -i 'stryker\|mutation-testing-elements' mutmut --exclude-dir=.git          # no output
```

Notes on sources:

- `https://stryker-mutator.io/docs/stryker-js/reporters/` and
  `https://stryker-mutator.io/docs/stryker4s/reporters/` return HTTP 404; reporters for
  both are documented inside their configuration pages, so the repo doc sources were
  opened instead (paths above).
- No tools were installed or upgraded for this seat; only `git clone` into `/tmp` was
  used. The only lane file written is this report.

## Remaining unknowns

- Whether Stryker4s' JSON reporter writes `"2"` in a live run (only a test expectation
  was observed); no Stryker4s run was performed.
- Whether Infection's embedded report always includes `files[*].source` for every file
  (builder read partially); relevant only if someone tries to extract its HTML payload.
- Which schema revision each published pitest-plugin release emits (pom now 3.9.0;
  released artifacts may lag).
- muttest and irradiate are documented claims only; neither was installed or run.
