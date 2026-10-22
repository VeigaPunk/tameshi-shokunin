# DraftSources — SOURCES.md rows S086/S087 and the round-25 search-log paragraph

Seat: `TameshiR25.DraftSources` (scribe, w1, axis: coverage).
Deliverable: **drafts only**. Nothing in `corpus/SOURCES.md`, `corpus/knowledge/`,
`corpus/lessons/` or any tool was edited; the only file written is this report.
Scratch extracts live under `/tmp/sources-draft/` (outside the lane).

Verdict: **two rows are ready to land, with one landing precondition** (the
`used-by` path must exist when the rows land) and one recorded access caveat
(the npmjs.com HTML pages refuse a scripted fetch; the registry endpoints do
not). No producer-authentication, promotion or numeric-score claim is made
here.

---

## 1. Row shape (what the file requires)

`corpus/SOURCES.md:11` header — eleven columns:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

Reference rows read in place: `corpus/SOURCES.md:93` (S084) and
`corpus/SOURCES.md:94` (S085). `SOURCES-CONTRACT-v1.md`
(`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`,
read-only) fixes `kind` ∈ `spec · docs · paper · code · tool · dataset · talk ·
book · community · own-work`, tier `A|B|C` scoped to `scope`, `status` ∈
`queued|mined|rejected`, `opened` = ISO date, `recheck` = ISO date or cadence,
`used-by` = repo-relative paths, comma-separated, or `—`; no `|` inside any
cell; rule 1 — *a row is a claim; write it only after opening the source in the
round that writes the row*, and the round lesson's `## Gate` records URL,
access date and a ≤25-word quote with its location grounding `teaches`.

## 2. Sources opened (both, in this round)

Both npm releases were opened on **2026-10-22**: the registry metadata document
and the tarball itself, extracted to `/tmp/sources-draft/mt/{schema,metrics}`.
The lane's vendored copies were used as the byte-identical carrier:

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/vendor
$ openssl dgst -sha512 -binary mutation-testing-report-schema-3.9.0.tgz | openssl base64 -A
28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ==
$ openssl dgst -sha512 -binary mutation-testing-metrics-3.9.0.tgz | openssl base64 -A
E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==
```

Both strings equal the `dist.integrity` values published by the npm registry
documents and the pins already held by `tools/mte-interop.py:56-61` — i.e. the
vendored artifacts are the published releases, not local edits:

```
$ curl -sS https://registry.npmjs.org/mutation-testing-report-schema/3.9.0
  "integrity": "sha512-28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ=="
  "version": "3.9.0", "license": "Apache-2.0",
  "gitHead": "00aa7bdc1da9df9f474e363cd70041ef4d389b4e",
  "repository": { "url": "git+https://github.com/stryker-mutator/mutation-testing-elements.git",
                  "directory": "packages/report-schema" },
  "tarball": "https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz"
$ curl -sS https://registry.npmjs.org/mutation-testing-metrics/3.9.0
  "integrity": "sha512-E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw=="
  "version": "3.9.0", "license": "Apache-2.0",
  "gitHead": "00aa7bdc1da9df9f474e363cd70041ef4d389b4e",
  "dependencies": { "mutation-testing-report-schema": "3.9.0" }
```

Both packages carry the same `gitHead` `00aa7bdc1da9df9f474e363cd70041ef4d389b4e`
in `stryker-mutator/mutation-testing-elements` (directories `packages/report-schema`
and `packages/metrics`) — the two rows are two packages of one upstream commit.

**Access caveat (recorded, not smoothed).** The human-facing package pages
refuse a scripted fetch, so the registry endpoints are the openable canonical
URLs:

```
$ curl -sS -o /dev/null -w "%{http_code} %{size_download}\n" -L https://www.npmjs.com/package/mutation-testing-report-schema/v/3.9.0
403 4565
$ curl -sS -o /dev/null -w "%{http_code} %{size_download}\n" -L https://www.npmjs.com/package/mutation-testing-metrics/v/3.9.0
403 4565
$ curl -sS -o /dev/null -w "%{http_code} %{size_download}\n" -L https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz
200 11872
$ curl -sS -o /dev/null -w "%{http_code} %{size_download}\n" -L https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz
200 32668
```

(The 200 byte counts equal the sizes of the lane's vendored tarballs:
11,872 B and 32,668 B.) The `source` cells therefore point at the registry
tarball, which is the artifact the quoted lines actually live in.

## 3. Anchors and quotes (for the row cells and for the lesson `## Gate`)

**S086 — `mutation-testing-report-schema@3.9.0`**, extracted file
`package/src/mutation-testing-report-schema.json`
(sha256 `404575e9264686dbf85c399f6531fdb489bebc3146e7e1d793b8083bc6a041ae`):

- `:7` → `"required": ["schemaVersion", "thresholds", "files"],`
- `:41` → `"required": ["id", "mutatorName", "location", "status"],`
- `:88-93` → the `status` property, `title` `MutantStatus`,
  `"enum": ["Killed", "Survived", "NoCoverage", "CompileError", "RuntimeError", "Timeout", "Ignored", "Pending"]` (`:92`)

Gate quotes (each ≤25 words, with location):

- `"required": ["schemaVersion", "thresholds", "files"]` — `package/src/mutation-testing-report-schema.json:7` (4 words)
- `"enum": ["Killed", "Survived", "NoCoverage", "CompileError", "RuntimeError", "Timeout", "Ignored", "Pending"]` — `package/src/mutation-testing-report-schema.json:92` (9 words)

**S087 — `mutation-testing-metrics@3.9.0`**, extracted files
`package/src/model/metrics.ts` (sha256 `49c5fe23e7a6ed7fc35f89da6890b1689029533a07c0f260f47e8ffa8cf1bc76`)
and `package/src/calculateMetrics.ts` (sha256 `b84b2d8b100dc47e0d8b7f750e92699404efe6eb2b41a705b66f3a86005c9eb4`):

- `:40-43` → `totalDetected` — *"The total number of mutants that were detected, meaning either killed or caused a time out."* / `` `killed + timed out` ``
- `:50-53` → `totalInvalid` — *"The total number of invalid mutants."* / `` `runtimeErrors + transpileErrors` ``
- `:55-58` → `totalValid` — *"Total number of valid mutants."* / `` `totalDetected + totalUndetected` ``
- `:69-73` → `mutationScore` — *"The total percentage of mutants that were killed, or NaN if not available."* / `` `totalDetected / totalValid * 100` ``
- `calculateMetrics.ts:234-255` → the same arithmetic in code: `totalDetected = timeout + killed` (`:234`), `totalUndetected = survived + noCoverage` (`:235`), `totalValid = totalUndetected + totalDetected` (`:237`), `totalInvalid = runtimeErrors + compileErrors` (`:238`), `mutationScore: totalValid > 0 ? (totalDetected / totalValid) * 100 : DEFAULT_SCORE` (`:253`, `DEFAULT_SCORE = NaN` at `:9`).

Gate quotes (each ≤25 words, with location):

- "The total number of mutants that were detected, meaning either killed or caused a time out. `killed + timed out`" — `package/src/model/metrics.ts:40-41` (17 words)
- "The total percentage of mutants that were killed, or NaN if not available. `totalDetected / totalValid * 100`" — `package/src/model/metrics.ts:70-71` (15 words)
- "The total number of invalid mutants. `runtimeErrors + transpileErrors`" — `package/src/model/metrics.ts:50-51` (7 words)

## 4. The drafted rows (drop-in, after `corpus/SOURCES.md:94`)

```markdown
| S086 | npm package mutation-testing-report-schema 3.9.0 (stryker-mutator/mutation-testing-elements) — https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz | spec | A | the released 3.9.0 report schema as an integrity-pinned npm artifact, not the master-branch file S002 tracks | package/src/mutation-testing-report-schema.json:7 (required schemaVersion, thresholds, files), :41 (required id, mutatorName, location, status) and :88-93 (status enum) @ mutation-testing-report-schema@3.9.0, npm tarball sha512 28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ==, gitHead 00aa7bdc1da9df9f474e363cd70041ef4d389b4e, repository directory packages/report-schema; opened 2026-10-22 | the released schema requires schemaVersion, thresholds and files at the top level and gives every mutant one of eight named statuses, so an exported report is checked against a pinned upstream shape instead of a hand-written one | mined | 2026-10-22 | 180d | corpus/knowledge/mte-report-interop.md |
| S087 | npm package mutation-testing-metrics 3.9.0 (stryker-mutator/mutation-testing-elements) — https://registry.npmjs.org/mutation-testing-metrics/-/mutation-testing-metrics-3.9.0.tgz | code | A | the official metric arithmetic of the 3.9.0 metrics library, not tameshi's own kill-rate formula | package/src/model/metrics.ts:39-42 (totalDetected = killed + timed out), :50-58 (totalInvalid, totalValid) and :69-73 (mutationScore = totalDetected / totalValid * 100) with package/src/calculateMetrics.ts:234-255 (the same arithmetic) @ mutation-testing-metrics@3.9.0, npm tarball sha512 E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==, gitHead 00aa7bdc1da9df9f474e363cd70041ef4d389b4e, repository directory packages/metrics; opened 2026-10-22 | the upstream score counts a killed or timed-out mutant as detected over killed plus survived plus noCoverage, while compile and runtime errors are invalid rather than surviving, so a kill rate is compared against the library and not against a local formula | mined | 2026-10-22 | 180d | corpus/knowledge/mte-report-interop.md |
```

Why these cells, briefly:

- **kind** — `spec` for S086 (it ships the JSON Schema; the sibling row S002
  `corpus/SOURCES.md:13` uses `spec` for the same artifact family),
  `code` for S087 (it ships the metric implementation; `code` is the contract's
  kind for source implementations, cf. S005/S006/S032).
- **tier A** — both are the upstream's own published release, primary and
  authoritative for their scope (a released schema and the released metric
  arithmetic). Tier is scoped by the `scope` cell, not global.
- **scope** — deliberately narrow and non-duplicating. S002
  (`corpus/SOURCES.md:13`) tracks the schema at the GitHub *master* branch;
  S086 tracks the *released* 3.9.0 artifact and its published integrity, so
  the two do not supersede each other and no `supersedes S0NN —` opener is
  used. S001 (`corpus/SOURCES.md:12`) states the metric definitions in prose
  from the Stryker docs; S087 is the released library that computes them.
- **teaches** — one grounded learner benefit each, each covered by the Gate
  quotes above: the schema's required shape and eight-status enum (S086), and
  the upstream detection/valid/score arithmetic including the invalid-not-
  surviving rule (S087).
- **status `mined`, `recheck 180d`, `opened 2026-10-22`** — as specified for
  this item; `mined` is correct only once the `used-by` path exists (see §6).
- **used-by** — `corpus/knowledge/mte-report-interop.md`, the knowledge entry
  this pair backs (repo-relative path, matching the convention of S084/S085's
  `corpus/knowledge/...` and `corpus/lessons/...` entries).

### Shape check (run on the draft rows in scratch, not in the lane)

```
$ cd /tmp/sources-draft
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' draft-rows.md
2
$ awk -F'|' '/^\| S0/{print $2, "NF=" NF}' draft-rows.md
 S086  NF=13
 S087  NF=13
```

NF=13 ⇒ eleven columns, as the contract's malformed-row check requires.
Kind/tier/status enum check (contract census script) prints no violation and
no duplicate id. The only failing check is the "mined rows whose used-by paths
do not exist" one — see §6.

## 5. The round-25 search-log paragraph

The round-24 counterpart is the paragraph at `corpus/SOURCES.md:302-307`
(`Round24 bounded lookup: …` followed by `- Next unused id: S086.`), which is
how the lane has written its per-round lookup note since round 22. The draft
below has the same shape and the same field order, and also carries the
contract's rule-5 fields (question, where, date, identified / screened /
included / excluded, exclusion reasons, stop rationale).

```markdown
Round25 bounded lookup: opened the two published npm releases behind the F1
report interop — mutation-testing-report-schema 3.9.0 and
mutation-testing-metrics 3.9.0 — at the registry metadata documents and the
integrity-pinned tarballs (both sha512 values equal the published
dist.integrity and the pins in tools/mte-interop.py); identified2/screened2/
included2/excluded0. New tierA/mined rows S086 and S087; no existing row
changes. Stop: the two official releases fix both the report shape and the
score arithmetic the interop check compares against, so the bounded question
is answered from the releases themselves and no wider source sweep is pursued.
One access caveat, recorded rather than smoothed: the npmjs.com package pages
returned HTTP 403 to a scripted fetch, so both rows cite the registry tarball,
which is where the quoted lines live.
- Next unused id: S088.
```

Placement notes for the integrator:

- Round 22–24 wrote this note at the end of the `## Id allocation` section
  (`corpus/SOURCES.md:302-307`), not under `## Search log`. The draft above
  follows that placement so it sits directly after the round-24 paragraph and
  the file's tail order is preserved.
- The contract's `## Search log` section (rule 5) is where a per-search note
  belongs; the same text satisfies rule 5's fields, so if the L1 prefers
  strict contract placement it may be moved to the end of `## Search log`
  (after the round-21 bullet at `corpus/SOURCES.md:210-218`) without any
  wording change. Nothing else in the file depends on the choice.
- The trailing `- Next unused id: S086.` at `corpus/SOURCES.md:307` becomes
  `- Next unused id: S088.` when the two rows land. Per the file's append-only
  practice (SOURCES.md id-allocation note, "the two `Next unused id` lines above
  are kept append-only"), keep the older lines and add the new one.
- Row order: S086 and S087 append after S085 (`corpus/SOURCES.md:94`), i.e. the
  new table rows go at the end of the registry table, before the `## Paths`
  section.

## 6. Out of scope / not claimed

- `corpus/SOURCES.md` was **not** edited; `corpus/knowledge/mte-report-interop.md`
  was **not** created (sibling seat `DraftKnowledge` owns it),
  `corpus/lessons/round-25.md` was **not** written (sibling seat `DraftLesson`
  owns it), and `corpus/SKILL.md` / `SKILL.md` were **not** touched (sibling
  seat `DraftSkillTable`).
- **Landing precondition:** `status: mined` requires a citing path. The
  contract census check "mined rows whose used-by paths do not exist — must
  print nothing" will flag both rows until `corpus/knowledge/mte-report-interop.md`
  exists. Land the knowledge entry first or in the same change; the row
  otherwise violates rule "mined = cited by ≥1 path in used-by".
- No gate, selftest, sweep or `tools/mte-interop.py --check` was executed in
  the lane. The claims here are about *what the two upstream artifacts say*;
  they say nothing about whether the interop check passes, and no
  `MTE_INTEROP: PASS legs_conforming=8/8` result is asserted or implied.
- No producer authentication, promotion, frontier-closure or numeric-score
  claim is made. Tier A here means "authoritative for the scope cell", not
  "verified for this lane".
- **Tools installed or upgraded: none.** No package manager was invoked; the
  two npm artifacts were fetched with `curl` and unpacked with `tar` into
  `/tmp/sources-draft/`, leaving the lane and the fleet repo untouched.
