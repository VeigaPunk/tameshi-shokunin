# S19 — C1 target recon: kumitate `scripts/sources-check.mjs`

Read-only. No mutants run. Probes below are the **unmutated** tool on `/tmp` fixtures.

## 1. Target and provenance

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file -t 0acb7752d19058b953ebbeba253b1e35f6548de5
commit
$ git -C … show 0acb775…:scripts/sources-check.mjs > /tmp/…/sources-check.mjs
$ wc -l  → 897   sha256sum → 6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
$ git rev-parse 0acb775…:scripts/sources-check.mjs
6b57424fc5a213a01015beaceb97de47a67967f0
$ git rev-parse HEAD:scripts/sources-check.mjs   # HEAD=1770305 (master)
6b57424fc5a213a01015beaceb97de47a67967f0
```
- Blob sha256 matches the C1 declaration exactly. The same blob is at lane HEAD, so rev == tip for this file (no drift between 0acb775 and master).
- Commit: `0acb775 2026-10-19 20:44:37 -0300 round-34: fix SOURCES Markdown row parsing` (+76/−2 in the tool).
- File history (`git log --follow`): **3 commits, all round 34** — `1a8eed5` (gate introduced), `06757b0` (post-review fixes, +195/−…), `0acb775` (targeted parser correction).
- Self-test, run from the extracted blob:
```
$ node sources-check.mjs --selftest
SOURCES_SELFTEST: 46/46 pass
VERDICT: PASS        EXIT=0
```
46 `PASS` lines counted: `grep -c '^PASS'` → 46. **C1's "46-check --selftest" is accurate.**

## 2. Self-test inventory (46 checks)

23 are table-driven "one finding kind fires" cases (`const cases`, file:592-666; expected exit at :671 — `USED_BY_ASYMMETRY`/`RECHECK_OVERDUE` expect **0**, all other kinds expect **1**). The other 23 are individual checks. Exact labels from the run:

| # | check | observed |
|---|---|---|
| 1 | clean fixture returns CLEAN | exit 0, `rows=1` |
| 2-24 | ROW_MALFORMED, ID_FORM, ID_DUPLICATE, ROW_OUTSIDE_REGISTRY, ROW_FIELD_EMPTY, KIND_ENUM, TIER_ENUM, STATUS_ENUM, TIER_INFLATION, OPENED_INVALID, RECHECK_INVALID, USED_BY_MISSING, MINED_UNUSED, REJECTED_NO_REASON, REJECTED_NO_FLIP, SECTION_MISSING, ENTRY_SOURCE_UNKNOWN, HEADER_INCOMPLETE (missing recheck), HEADER_INCOMPLETE (empty trio), ENTRY_HEADER_REQUIRED (new headerless), ENTRY_HEADER_REQUIRED (source header removed), USED_BY_ASYMMETRY, RECHECK_OVERDUE | 21×exit 1, 2×exit 0 (last two) |
| 25 | 1-3-space headings/rows normalized; 4-space row stays code | exit 0, `rows=4` |
| 26 | 1-3-space indented invalid rows report field+tier findings | exit 1, 3×ROW_FIELD_EMPTY, 3×TIER_ENUM |
| 27 | 1-3-space indented rows outside Registry rejected | exit 1, 3×ROW_OUTSIDE_REGISTRY |
| 28 | `reflip:` does not satisfy `flip:` | exit 1 (under `--strict`) |
| 29 | opened + Nd strictly before today is overdue | exit 0, kind fires |
| 30 | opened + Nd exactly due today not overdue | exit 0, kind absent |
| 31 | frozen legacy identity set = 38 unique paths | base=38 unique=38 |
| 32 | frozen base identity stays legacy+counted after growth | `entries_with_source=0 legacy=1` |
| 33 | over-wide row (14 split fields) flagged | exit 1 |
| 34 | ISO recheck exactly today not overdue | exit 0, kind absent |
| 35 | **every declared finding kind fires** (meta) | `unfired=[]` |
| 36-38 | SELF_NOT_A_DIR, SOURCES_MISSING, READ_FAILED fail-closed | exit 2 each |
| 39 | **every fail-closed arm fires** (meta) | `unfired=[]` |
| 40 | `--strict` promotes warnings | exit 1 |
| 41 | `--json` one parseable contract object (CLEAN only) | exit 0 |
| 42 | S1000 accepted and counted | exit 0, `rows=2` |
| 43 | invalid/missing option value → usage | exit 64 (only `--self` with no value) |
| 44 | unknown option → usage | exit 64 |
| 45 | `-h` prints usage | exit 0 |
| 46 | frozen awk census parity (rows / malformed / duplicate ids) | node=4/1/1 awk=4/1/1 |

Assertion shape matters for case design: 44 of 46 checks assert only `(exit, kind)`; the two indented suites additionally assert `id=S00N` detail fragments; #31 asserts the frozen list length; #35/#39 are internal meta-checks. **No check asserts a finding's `line`/`:N` location, no check asserts any `detail` outside those `id=` fragments, and only #1/#25/#32/#42/#46 assert any part of the `CLEAN (…)` counters.** #46 prints `SKIP` (and is dropped from the denominator) when awk is absent — LOG.md:1496-1498 names this limit.

## 3. Findings and exit map (as coded)

21 finding kinds (`FINDING_KINDS`, :108-114) and 3 fail-closed kinds (`FAIL_CLOSED_KINDS`, :116):

- **error** — ROW_MALFORMED (E01), ID_FORM (E02), ID_DUPLICATE (E03), ROW_OUTSIDE_REGISTRY (E12), ROW_FIELD_EMPTY (—), KIND_ENUM (E05), TIER_ENUM (E06), STATUS_ENUM (E07), TIER_INFLATION (E10), OPENED_INVALID (E08), RECHECK_INVALID (E09), USED_BY_MISSING (E11), MINED_UNUSED (W03), REJECTED_NO_REASON (—), REJECTED_NO_FLIP (W02), SECTION_MISSING (—), ENTRY_SOURCE_UNKNOWN (—), ENTRY_HEADER_REQUIRED (—), HEADER_INCOMPLETE (—)
- **warn** — USED_BY_ASYMMETRY (—), RECHECK_OVERDUE (no fleet validate code; fleet `overdue` report)
- **fail-closed** — SELF_NOT_A_DIR, SOURCES_MISSING, READ_FAILED

Verdict lines (`emitResult`, :440-483): `SOURCES_CHECK: CLEAN (rows=N tiers=A:a,B:b,C:c status=queued:q,mined:m,rejected:r entries_with_source=k legacy=l)` · `SOURCES_CHECK: DRIFT (<kinds>)` · `SOURCES_CHECK: FAIL-CLOSED (<kind>)`; `--json` prints one `kumitate-sources-v1` object instead.
Exit map (:43-44, :479, :486-497): **0** clean (warnings advisory) · **1** drift (`--strict` promotes warn→drift) · **2** fail-closed · **64** usage. `--selftest`/`--self-test` exits 0/1 on PASS/FAIL. Verified live: P1/P2/P9 → 1, P3/P4/P5 → 2, P6/P12 → 64, selftest → 0.

## 4. Coverage measurement (evidence for §5)

```
$ npx -y c8 --reporter=json --include=sources-check.mjs node sources-check.mjs --selftest
sources-check.mjs | 98.21 % Stmts | 86.07 % Branch | 100 % Funcs | 98.21 % Lines
ZERO STMT LINES: 175,176,189,190,239-243,356,357,447,572,573,881,895
UNCOVERED FUNCS: none
```
Uncovered branch operands (istanbul `binary-expr`/`if`): 147,148,149,164,174,183(×2),185,188,231,238,255,256,259,337,349,355,381,388,417,428,446,468,550(×2),553,569,570,571,707,708,723,750,780,849,860,861,862,879,881,884,885,892,895.
Harness-internal only (not gate behaviour): 550,553,569-573,707-708,723,750,780,849,860-862,879-885,892-895.

## 5. Candidate survivors (paths with no self-test case)

Class A = statement/branch never executed (c8 evidence). Class B = branch executed but only one outcome ever observed (static reasoning, **[INFERENCE]** where noted — istanbul counts operand evaluation, not outcomes). Class C = unreachable/equivalent mutants: a defect spec should **not** expect these to be killed.

**Class A — top candidates (each currently survives a single-point mutation):**
1. **`isoDay` leap computation, :148** — `leap` is never true: every fixture date is 2026 (FIXTURE_TODAY 2026-10-19). A mutant `leap=false` survives. Also `month<1||month>12` (:147) never triggers. Live check: `opened=2024-02-29` → CLEAN (correct today); `2023-02-29` → OPENED_INVALID (P7a/P7b).
2. **`repoPathExists` traversal guard, :164** — no fixture uses a `..`/absolute used-by. Removing the guard survives. Live check: `used-by ../outside/secret.md` (file exists outside root) → USED_BY_MISSING, exit 1 (P2) — correct today, unguarded by test.
3. **`statSync(opts.self)` catch, :174-176** — SELF_NOT_A_DIR is only tested with a *file* (isDirectory false, :177); a nonexistent `--self` path (ENOENT throw) is untested. Mutation deleting the catch survives. Live: exit 2, same verdict (P3).
4. **SOURCES.md fail-closed sub-arms, :183/:185/:188-190** — non-ENOENT stat error, `isFile()` false, and `readFileSync` throw are all unexecuted; READ_FAILED is exercised only through the knowledge-dir-as-file fixture. Live: SOURCES.md as a directory → `READ_FAILED … not a readable file`, exit 2 (P4).
5. **empty-id row branch, :238-243** — unexecuted. Deleting it survives for 13-field rows (ID_FORM still fires at :259 with the same kind/exit); only an all-empty 13-field row (currently silently ignored) would flip to ID_FORM. Live: `| | Fixture | …` → `ID_FORM … id=(empty)` (P8).
6. **`fields[4] ?? ''` / `fields[8] ?? ''`, :255-256** — a valid-id row with ≤4 split cells is untested; deleting `?? ''` would crash `trim(undefined)` on such a row and survive the suite.
7. **knowledge-file `readFileSync` catch, :355-357** — stat/read race or unreadable child file untested (readdir failure *is* covered).
8. **`--today` argument arms, :417, :428** — only `--self` is tested for usage-64. Deleting the `need()` check for `--today` or the invalid-ISO guard survives. Live: `--today` (no value) → 64; `--today -5` → 64; `--today 2026-13-01` → 64 with `--today must be an ISO YYYY-MM-DD date` (P12/P6).
9. **`--json` fail-closed object, :446-448** — fail-closed fixtures never pass `--json`. Replacing that branch with text output survives. Live: JSON `{schema, verdict:"FAIL-CLOSED", exitCode:2, failClosed:{…}, findings:[], counts:null}`, exit 2 (P5).
10. **`--json --strict` totals, :468** — `warnings: opts.strict ? 0 : warnings.length`; the strict branch is unexecuted (JSON tested CLEAN-only, strict tested text-only). Live: promoted warning → `totals {errors:2,warnings:0}`, all findings `severity:"error"`, exit 1 (P11).

Secondary Class A: dev-only/robustness paths — duplicate suppression for a **3rd** occurrence (:250-252, only 2-duplicate fixture); separator-row alignment variant `:---:` (:244, only plain `---` tested); multi-path / `—`-mixed used-by lists (:157-158, only single path or bare `—`); used-by target that is a directory (existsSync accepts it, untested); non-`.md` knowledge files and `entry.isFile()` symlink behaviour (:345 — a symlinked knowledge file is silently ignored, documented limit); a row with a valid id outside `## Registry` but non-`S` id (ignored by design); `# top-level heading` resetting Registry (:199-201 — live: P15 → ROW_OUTSIDE_REGISTRY, correct); `L###` legacy file that *does* carry a header (entries_with_source path); `--help` long form and `--self-test` alias (only `-h` and `--selftest` tested; P13: alias exit 0).

**Class B — one-outcome predicates (mutants that survive):**
11. **future `opened`** — `openedDay > opts.todayDay` (:303) is reached only when it is false (all valid fixture openings equal FIXTURE_TODAY; the OPENED_INVALID fixture dies at `=== null`). Deleting the future-date half survives. Live: `opened=2026-10-20` → `OPENED_INVALID … opened=2026-10-20`, exit 1 (P1). **[INFERENCE] on mutant survival (coverage-invisible).**
12. **`normalizeMarkdownIndent` lookahead, :136** — mutant `^ {1,3}(?=\S)` → `^ {1,3}` survives: a 4-space code row becomes `' | …'`, still fails `startsWith('|')`, so `rows=4` still passes. **[INFERENCE]**
13. **tier-inflation conjunction, :298** — mutant dropping `row.kind === 'community'` survives (fixtures only exercise community+A); dropping the tier half is caught.
14. **counters beyond `rows`/`legacy`** — `counts.tiers`/`counts.status` (:257-258) and `entriesWithSource` (:368) are asserted only as `rows=N` prefixes and `entries_with_source=0 legacy=1`; e.g. `tiers[x] += 2` survives. **[INFERENCE]**
15. **detail text and line numbers** — only `id=S00N` fragments are asserted; a mutant changing every `index + 1` to `index`, or rewriting any `detail` string not containing that fragment, passes all 46. **[INFERENCE]**
16. **`SECTION_MISSING` multiplicity** — only one section omitted in any fixture; a mutant reporting just the first missing section survives. **[INFERENCE]**

**Class C — unreachable/equivalent (exclude from the defect spec):**
- :259 `id || '(empty)'` — `id !== ''` is guaranteed by :238, so the fallback is dead.
- :231 `fields[1] ?? ''` — `line.split('|')` on a `|`-prefixed line always yields ≥2 fields.
- :381 `lines[0] ?? ''` — `split` always returns ≥1 element.
- :337 cadence `catch` — `BigInt(/\d+/)` cannot throw; `openedDay` is a bounded integer.
- :182 `?? 'unknown error'` and :349 same — reachable only with an error object lacking `code`.

## 6. Kumitate's own documentation of the gate

| anchor | content |
|---|---|
| `SKILL.md:605` | `## Gate registry` row: `sources-check | gate | node scripts/sources-check.mjs [--strict] → SOURCES_CHECK: CLEAN\|DRIFT | --selftest | independent gate; corpus/SOURCES.md + frozen 16a5441 legacy identity set; not a kumitate-proxy-v1 pin` |
| `SKILL.md:629-630` | checklist items 12-13: gate exit 0 + `CLEAN`; suite exit 0 + `VERDICT: PASS` (both count-agnostic) |
| `PROVINCE.md:15` | core-band primary surface: "The lane's own instruments `scripts/*.mjs` … and its learning registry `corpus/SOURCES.md` (checked by `scripts/sources-check.mjs`)" — the declared C1 anchor "PROVINCE.md:7-11" lands on the band header at :8-10; the instrument line is **:15** |
| `LOG.md:1414-1445` | round-34 claim 1: new gate, "34-case hermetic suite", live `CLEAN (rows=20 …)`, `34/34` |
| `LOG.md:1494-1498` | named limits: `ID_FORM` scans every `\| S…` row (superseded by the same-rev correction), awk-parity SKIP |
| `LOG.md:1514-1524` | post-review correction: rows only under `## Registry`; nonempty cells; rejected needs both `REJECTED:` and `flip:`; 38-path legacy identity set |
| `LOG.md:1536-1537` | "after the correction: `--selftest` → `SOURCES_SELFTEST: 42/42 pass`" |
| `LOG.md:1550-1563` | targeted parser correction: 1-3-space normalization, `flip:` word boundary, direct-only knowledge scan |
| `SCORECARD.md:307` | operability: A=7 including `scripts/sources-check.mjs`; `f_O = 20/23` |
| `SCORECARD.md:393` | round-34 move row: "34-case hermetic suite incl. awk-census parity" |
| `SCORECARD.md:1616` | capability `sources-registry`: "`node scripts/sources-check.mjs` → CLEAN …; `--selftest` **42/42**" |
| `corpus/QUALITY.md:112-117` | post-review clarification: legacy exemption = the frozen 38 identities; any non-base knowledge path needs a nonempty `source:`/`verified-at:`/`recheck:` trio |
| `corpus/README.md:92`, `corpus/lessons/round-34.md:77` | capability/round evidence pointers; live `CLEAN (rows=20 …)` |
| `.ufo/rounds/round-34/sources-gate.md` | full gate boundary record; §Post-review (line ~112) and §Targeted parser correction (line ~125); `:120` "Post-review behavior fixtures are in `scripts/sources-check.mjs --selftest`" |
| `scripts/proxy-check.mjs:1455,2007-2009` | cross-gate coupling: proxy-check's own suite rejects `pin.sources-check` as `STANZA_KEY_UNKNOWN` — a "registered as a v1 pin" defect is caught **there**, not by this tool's suite |

## 7. Documentation drift observed at the rev

- **Stale case count**: live suite = **46/46**, but `SCORECARD.md:1616` (capability row, the live pointer) says **42/42**, and `SCORECARD.md:393` + `LOG.md:1420` say **34-case**. `LOG.md:1537` (42/42) is a chronological entry, but commit `0acb775` grew 42→46 and updated no count anywhere. `SKILL.md` is deliberately count-free, so the checklist is unaffected.
- `LOG.md:1494-1498` states "`ID_FORM` scans every `| S…` table row in the file, not only `## Registry`" as a named limit; the same rev's targeted correction (`LOG.md:1514-1524`) makes rows outside Registry report `ROW_OUTSIDE_REGISTRY` and skip field checks. Historically ordered, but the superseded sentence carries no erratum pointer at its own line.
- The C1 anchor "PROVINCE.md:7-11" is off by a few lines (see table): the gate's primary surface is stated at :15.

## 8. Tooling used

`npx -y c8` (ephemeral npm-cache fetch, no persistent install; drives Node's own `NODE_V8_COVERAGE`) for §4. Nothing installed or upgraded on the host; no pacman, no lane mutation.

## 9. Remaining unknowns

- Whether the tameshi `--regression` leg counts `cases=8` from this suite's 46/46 (out of this target's scope; the round-16 procedure doc is not kumitate's).
- Class B survivor claims are coverage-invisible by construction; they are static reasoning ([INFERENCE]) and would need a single mutant each to confirm — deliberately not run here.
- c8 merged child processes; branch percentages include the harness, so the 86.07% branch figure overstates gate-code coverage.

## Verdict

**holds** — at `0acb775…` the file is exactly the declared blob (sha256 `6a293a72…`), its `--selftest` is 46/46 PASS exit 0, the documented 0/1/2/64 exit map is accurate, and recon identifies ten Class-A plus six Class-B untested paths (led by `isoDay` leap, the used-by traversal guard, the empty-id branch, the `--json` fail-closed/strict paths, and future-`opened`) alongside four genuinely equivalent mutants that a 10-defect spec must not count as survivors.
