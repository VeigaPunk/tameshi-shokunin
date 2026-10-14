# Gates survey — kumitate-shokunin's six hermetic suites

Survey date: 2026-10-14. Lane: tameshi (probation wave 1, TAMESHI-1).
Substrate status: kumitate-shokunin read-only (no writes made; probe command
ran with cwd under `/tmp`, every suite's writes go to its own `mkdtemp` root).
Anchors marked O = observation (file:line or command output), I = inference,
U = unknown. All `scripts/` paths below are
`kumitate-shokunin/scripts/`.

## 0. Method and executed evidence

Command (all six, exit codes recorded):

```
cd /tmp/tameshi-probe
node <kumitate-shokunin>/scripts/<gate>.mjs --selftest
```

| gate | exit | last summary lines (verbatim from capture) |
|---|---|---|
| cite-check | 0 | `62/62 cases passed (hermetic)` / `VERDICT: PASS` |
| surface-probe | 0 | `42/42 cases passed` / `VERDICT: PASS` |
| round-gate | 0 | `ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS` |
| proxy-check | 0 | `PROXY_SELFTEST: 102/102 pass` / `VERDICT: PASS` |
| claims-check | 0 | `CLAIMS_SELFTEST: 39/39 pass` / `VERDICT: PASS` |
| kimi-census | 0 | `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS` |

O: every suite builds its fixtures under `mkdtempSync(join(tmpdir(), ...))`
and removes them in a `finally` block — cite-check.mjs:1842,
surface-probe.mjs:984, round-gate.mjs:690, proxy-check.mjs:1245,
claims-check.mjs:600, kimi-census.mjs:472.

O: scripts' mtimes at survey time — cite-check Oct 14 06:37,
surface-probe/round-gate/proxy-check/claims-check Oct 13 18:53-22:01,
kimi-census Oct 13 18:53. Re-running after substrate drift invalidates counts;
append errata rather than editing rows (house rule, QUALITY.md:4-8).

## 1. cite-check.mjs (2537 L)

**A. Identity.** Resolves path/line/symbol/pin citations in docs; hermetic
group `--selftest` (aliases `--self-test`), integration group `--integrations`
(cite-check.mjs:11, 73-85). Exit map: 0 CLEAN, 1 DRIFT, 2 fail-closed, 64 usage
(cite-check.mjs:69).

**B. Hermetic cases: 62** (O: run output; O: 62 literal `check(` call sites
counted by `grep -cE "^\s+check\("`). Source reporting format
`n/m cases passed (group)` at cite-check.mjs:2494, final `VERDICT:` at
cite-check.mjs:2501. The suite also holds 9 `checkI(` integration call sites
(O: `grep -cE "^\s+checkI\("` = 9) — see D.

**C. Mutation control — one true mutation copy, but integration-gated.**
O: cite-check.mjs:2372-2384, case `real symbol machinery fires on a repaired
site (mutation copy)`: copies the live self tree, rewrites `gate.rs:15` →
`gate.rs:11` in the copied `SKILL.md` (2377), re-runs the checker, and requires
a `SYMBOL_OFF_LINE`/`GateDecision` hit (2380-2383). It is `checkI` — recorded in
the integration group and additionally guarded by
`existsSync(... gate.rs) && existsSync(... SKILL.md)` (2357). It does not
run under `--selftest` (skip arm 2354-2356).
O: no kill-rate harness; no fault injection against the gate's own code exists
in the hermetic group. `grep -n -iE "mutant|kill|mutation" cite-check.mjs`
returns only the mutation-copy block and unrelated prose.
O: cite-check has **no** "every declared kind fires" completeness meta-check
(O: no match for `observed|codes observed|every .* fires` in the file), unlike
the other five suites.
O: hermetic before/after evidence instead: repair-regression cases assert
`before`/`after` token resolution around fences and repairs, e.g.
`fence content is never tokenized` (2020-2024), `alignment self-heal`
(2026-2031), `R23 repro ... tokens before AND after a ``` fence` (2103-2111).

**D. Fail-closed arms.** O: no `FAIL_CLOSED_KINDS` enum in this file. Runtime
exit-2 arms live in `main()`: `--src/--self/--fleet` not a directory
(cite-check.mjs:2517-2523), and post-scan `empty scan set` / `zero resolved
citations` (2527-2533). Hermetic coverage: `bare run (no --src): both
candidates absent keeps the --src fail-closed arm (exit 2)` spawns the CLI with
`HOME` redirected and asserts `status === 2` + stderr `--src … is missing`
(2334-2343); observed pass in run output.
O: the case named `fail-closed: empty scan set → exit-2 condition`
(1964-1970) asserts the **in-process condition** `filesScanned === 0 &&
verdict === 'FAIL'` — it does not exercise the CLI `return 2` mapping at 2527-2533.
I: the empty-scan exit-2 path is therefore uncovered by the hermetic suite;
only the condition that triggers it is asserted.

**E. Verdict-line exactness.** O: hermetic asserts are **substring**, not
literal-match: `text.includes(\`VERDICT: ${rep.verdict}\`)` and
`text.includes('CITE_CHECK:')` plus JSON `"verdict"` agreement
(cite-check.mjs:1956-1962). Text renderer emits `VERDICT: ${report.verdict}`
(1625) with report verdict `PASS|FAIL` (1590); JSON twin `citeCheck: CLEAN|DRIFT`
(1595). Suite-level summary `n/m cases passed (hermetic)` + `VERDICT: PASS`
(2494, 2501).

## 2. surface-probe.mjs (1506 L)

**A. Identity.** Modes: `--selftest` wins, then `--checklists`, else
conformance (surface-probe.mjs:8-15, 23). Exit map 0/1/2/64.

**B. Hermetic cases: 42** (O: run output; O: 42 literal `check(` sites).
Summary format `${n}/${m} cases passed` + `VERDICT:` at 1444-1445.

**C. Mutation control — absent.** O: no mutant/kill/mutation references
(`grep -iE "mutant|kill|mutation"` returns none). Substitute control: arm
coverage meta-check `every declared finding code fires in at least one fixture`
(1432-1435) over `SUITE_CODES` (217-218), observed `21 codes observed` in the
run output. I: this detects uncovered arms, not unsound assertions — a weaker
control than mutation testing.

**D. Fail-closed arms — dynamic strings, no token enum.** O: `failClosed` is a
free-text field set at: sighting surface unreachable (437-438), manifest
unparsable (454-455), foreign manifest kind (464-465), `zero checks executed`
when `checks.length === 0` (496). Verdict `FAIL-CLOSED` + exit 2
(497-499). Hermetic fixtures assert `totals.failClosed !== null` for
unreachable/unparsable/foreign-kind (1031-1057). CLI `--src` arm prints
`SURFACE_PROBE: FAIL-CLOSED (--src <dir> is <kind>)` (stderr 1494, stdout
1495), exercised by the bare-run case (1341-1345, observed pass).
O: checklist mode has its own fail-closed shape, `CHECKLIST: FAIL-CLOSED …
VERDICT: FAIL` + exit 2 for `--self` not-a-dir (836-843) and missing SKILL.md
(841-843), with cases at 1408-1411 and `--self is a file` (observed in run).
I: because fail-closed reasons are assembled strings rather than an enum, the
suite cannot (and does not) assert arm coverage for them.

**E. Verdict-line exactness.** O: conformance verdict line
`SURFACE_PROBE: ${verdict} (surfaces=… checks=… errors=… warnings=…)`
(791-793) — asserted by **substring** in checklist-mode cases and by
`report.verdict === 'CLEAN'` object checks (1024); checklist summary asserted
with `text.includes('CHECKLIST: 2/2 pass')` (1369), `'CHECKLIST: 0/2 pass'`
(1378), `'CHECKLIST: 0/0 pass'` (1402) plus exact exit codes. Suite summary
substring-free but format-literal: `${n}/${m} cases passed` (1444).

## 3. round-gate.mjs (1511 L)

**A. Identity.** Modes `--selftest` (wins) / `--tracked` / `--close`
(round-gate.mjs:9, 23); exit map 0/1/2/64 (183).

**B. Hermetic cases: 60** (O: run output; O: 60 literal `check(` sites).
Summary `ROUND_GATE_SELFTEST: n/m pass` (1505) + `VERDICT:` (1506); nested
self-check asserts `^ROUND_GATE_SELFTEST: \d+\/\d+ pass$` **anchored regex**
plus exact `tail.at(-1) === 'VERDICT: PASS'` (1399-1401).

**C. Mutation control — absent.** O: no mutant/kill/mutation text in the file.
Substitute: `every declared finding kind fires in at least one fixture`
(1487-1493) over `FINDING_KINDS` (171-176, 14 kinds); run output
`14 kinds observed`. No fail-closed-arm completeness check exists (O: no
`observedFc`-style filter in the file).

**D. Fail-closed arms — 7 declared tokens, 6 fired in the hermetic run.**
O: declared list, header doc 115-117: `REPORTS_DIR_MISSING`,
`NOT_A_GIT_WORKTREE`, `NO_CLOSED_ROUND`, `NO_FILED_REPORTS`, `UPSTREAM_MISSING`,
`MAIN_REPO_NOT_GIT`, `INTERNAL_ERROR`; emission site 596-617 (`failClosed()`,
line 604 sets `verdict: 'FAIL-CLOSED'`, 617 prints
`ROUND_GATE: FAIL-CLOSED (${token}) ${detail}`).
O: hermetic case labels observed firing: REPORTS_DIR_MISSING (1187-1191),
NOT_A_GIT_WORKTREE (1192-1196) and the `--repo does not exist` variant
(1197-1204), UPSTREAM_MISSING (1211-1216), NO_CLOSED_ROUND (1205-1210),
NO_FILED_REPORTS (1434-1438), MAIN_REPO_NOT_GIT twice (1217-1219, 1449-1451),
plus a `--json` `verdict: FAIL-CLOSED` shape case (1279-1284).
U: `INTERNAL_ERROR` (683) has no hermetic case (O: no match in run capture) and
no completeness meta-check stands in for it.

**E. Verdict-line exactness — strongest parser of the six.** O: the suite
extracts the last non-blank line (`verdictLine`, 861) and full-match regexes it:
`/^ROUND_GATE: (CLEAN|DRIFT) \(round=(\d+) lane=(\S+) checks=(\d+) errors=(\d+) warnings=(\d+)\)$/`
(863-868, `$`-anchored + numeric fields). Cases then assert exit + parsed
fields, e.g. `checks === 10 && errors === 0 && warnings === 0` (878-883).
Fail-closed lines are asserted by regex `ROUND_GATE: FAIL-CLOSED \(TOKEN\)`
(1188, 1435, 1450) and the JSON `findings[0].kind` equals the token (1282-1284).

## 4. proxy-check.mjs (2354 L)

**A. Identity.** Recomputes the SCORECARD proxy terms; `--selftest` wins over
help/json (proxy-check.mjs:52-63). Exit map 0 MATCH / 1 DRIFT / 2 fail-closed /
64 usage (USAGE text 417; DRIFT exit 941; usage exit 64 at 2341).

**B. Hermetic cases: 102 executed** (O: `PROXY_SELFTEST: 102/102 pass`), vs 71
literal `check(` call sites (O) — the difference is loop-generated per-arm
cases (e.g. per-token loops). Summary 2288-2289; nested hermeticity case
asserts `^PROXY_SELFTEST: \d+\/\d+ pass$` + exact `VERDICT: PASS` (2261-2263).

**C. Mutation control — absent as fault injection, but the suite pins its own
arithmetic against literals.** O: `determinism: the same fixture yields
byte-identical stdout on a re-run` compares full stdout strings (1392-1395).
O: MATCH verdicts are asserted against **hand-arithmetic literal strings**
(comment 1213-1214, cases 1366-1385); fixtures deliberately avoid re-deriving
expected numbers (1329, 1364). O: no mutant/kill/mutation references.
Substitute control: `every declared finding kind fires` (2269-2271, 21 kinds
observed) and `every declared fail-closed arm fires in at least one fixture`
(2273-2276, run output: `12 arms observed`).

**D. Fail-closed arms: 12 declared, all 12 fired.** O: `FAIL_CLOSED_KINDS` =
`SELF_NOT_A_DIR, SRC_NOT_A_DIR, KIMI_ROOT_NOT_A_DIR, SCORECARD_MISSING,
STANZA_MISSING, STANZA_MALFORMED, STANZA_KEY_UNKNOWN, STANZA_KEY_DUPLICATE,
REGISTRY_MISSING, SKILL_MISSING, README_MISSING, CORPUS_DIRS_MISSING`
(proxy-check.mjs:385-391; 12 entries). Emission path maps unexpected throws to
`INTERNAL_ERROR` unless the kind is declared (1044), prints
`PROXY: FAIL-CLOSED (${token}) ${detail}` (989). Coverage enforced by the
2273-2276 meta-check; run output reports all 12 observed and the count per token
in the captured run matches the declared list (e.g. STANZA_MALFORMED ×9 cases).

**E. Verdict-line exactness — literal full-string equality.** O: MATCH cases
compare `verdictLine(r) === 'PROXY: MATCH (A=6 C=3 operability=7; C1=1/2 C2=2/2
coverage=5; S=0/3 coverage:script-layer=0; R=0/2 coverage:runtime-layer=0;
K=0/29 coverage:kimi-layer=0; pins=6 match)'` (1368; 1378, 1384, 1479, 1616,
1724 same style). Fail-closed asserted by regex
`/^PROXY: FAIL-CLOSED \(([A-Z_]+)\)/` (1283). `--strict` case asserts two runs
produce the identical verdict line (1399-1400).

## 5. claims-check.mjs (925 L)

**A. Identity.** Verifies SCORECARD member rows against `corpus/knowledge`
notes; single hermetic mode `--selftest` (claims-check.mjs:136, 913). Exit map
0 MATCH / 1 DRIFT / 2 fail-closed / 64 usage (883, 898).

**B. Hermetic cases: 39 executed** (O: `CLAIMS_SELFTEST: 39/39 pass`) vs 35
literal `check(` sites (O) — loop expansion. Failure-only printing: passing
cases are not echoed, only `FAIL` lines and the summary (858-862). I: the
per-case evidence for this gate must come from source anchors, not run stdout —
in the captured run, zero case lines were printed, which itself is the pass
signal.

**C. Mutation control — absent; deliberately externalized.** O: comment
820-822: "the acceptance run proves it from outside by poisoning the env
(`UFO_SRC=/nonexistent … --selftest` → PASS)"; the env-poisoning probe is not a
case inside the suite. Substitute controls: `every finding kind fired by the
suite` and `every fail-closed arm fired by the suite` meta-checks (846-851).

**D. Fail-closed arms: 5 declared, all covered by cases + meta-check.** O:
`FAIL_CLOSED_KINDS` = `SELF_NOT_A_DIR, SCORECARD_MISSING, REGISTRY_MISSING,
SRC_NOT_A_DIR, CORPUS_DIRS_MISSING` (117-120). Cases built in a loop over `arms`
(736-752): each asserts `status === 2 && verdictLine.includes('FAIL-CLOSED
(${token}')`; the `--src` absent case additionally asserts the `--src … is
absent` detail (776-779). Emission shape `CLAIMS: FAIL-CLOSED (${token}
${detail})` (449) with a preceding `CLAIMS  fail-closed  TOKEN  detail` line.

**E. Verdict-line exactness — literal equality on the green arm, substring on
fail-closed.** O: `GREEN_MATCH = 'CLAIMS: MATCH (rows=2 yes=2 notes=2
sections=2 adv=0)'` (756) and several cases assert
`verdictLine(r) === GREEN_MATCH` (759, 763, 769). O: one case tightens to full
string with different counts and a row-vs-verdict agreement assertion —
`'CLAIMS: MATCH (rows=2 yes=2 notes=2 sections=1 adv=1)'` + `row form=topic
sections=0 adv=1` (827-835, comment names it the kind-blind-mutant detector).
Fail-closed asserts use `.includes(FAIL-CLOSED (${token})` (745), not equality.
Summary `CLAIMS_SELFTEST: n/m pass` (861) + `VERDICT:` (862).

## 6. kimi-census.mjs (896 L)

**A. Identity.** Verifies the frozen 49-member `~/.kimi-code` census;
`--selftest` mode (kimi-census.mjs:162, 885). Exit map 0 CLEAN / 1 DRIFT /
2 fail-closed / 64 usage (864, 876).

**B. Hermetic cases: 43 executed** (O: `KIMI_CENSUS_SELFTEST: 43/43 pass`) vs
41 literal `check(` sites (O). Failure-only printing (851-853). Fixture tree is
shape-clean with a 0600 leaf token; secrecy case at 630 (`secrecy: fixtures are
shape-clean with a 0600 leaf token (mode floor passes)`).

**C. Mutation control — absent.** O: no mutant/kill/mutation text. Substitute:
`every finding kind fired by the suite` and `every fail-closed arm fired by the
suite` (836-840) over `FINDING_KINDS = ['MEMBER_MISSING','UNLISTED',
'SHAPE_DRIFT']` (147) and `FAIL_CLOSED_KINDS = ['KIMI_ROOT_MISSING']` (148).
O: a filename-canary case asserts the fixture long-random root name does not
leak into output (case 658-663).

**D. Fail-closed arms: 1 declared, 3 cases.** O: KIMI_ROOT_MISSING fired by
`--root /nonexistent` (774-782; assertion 777), unreadable root via chmod 000
(786-793; assertion 789), and `--json` (796-803; assertions 800-801); each case
passes `failClosed: ['KIMI_ROOT_MISSING']` for the meta-check. Emission
`KIMI_CENSUS: FAIL-CLOSED (${token} ${detail})` (393), declaring `fatal.kind`
in JSON with `totals.members === 0` (390, 800).

**E. Verdict-line exactness — full-line equality for CLEAN, prefix for
fail-closed.** O: green case asserts
`lastLine(r) === 'KIMI_CENSUS: CLEAN (members=49 checked=49 chain=3 info=4)'`
(508-514); DRIFT asserted by `startsWith('KIMI_CENSUS: DRIFT')` + kind and
`members=` presence (498-500); fail-closed by `startsWith('KIMI_CENSUS:
FAIL-CLOSED (KIMI_ROOT_MISSING')` (777, 789). `--json` totals cross-checked
against the text line via `lastLine(t).includes('members=…')` +
`includes('checked=…')` + `j.verdict === 'CLEAN'` (531-538). Summary 852-853.

## 7. Cross-cutting observations (O)

1. Corpus-wide, the only true mutation-testing style control is cite-check's
   mutation copy (2372-2384) and it is integration-gated; **no gate ships a
   kill-rate harness or fault injection against its own code** (O: grep for
   `mutant|kill|mutation` across all six returns only cite-check's mutation
   copy and claims-check's comment at 827).
2. Five gates carry a suite-exercises-every-declared-arm meta-check
   (surface-probe 1432-1435; round-gate 1487-1493; proxy-check 2269-2276;
   claims-check 846-851; kimi-census 836-840). cite-check carries none (O: no
   match for `observed|every .* fires`).
3. Fail-closed arm strength divides: proxy 12 tokens with full coverage; claims
   5 with full coverage; kimi-census 1 with 3 cases; round-gate 7 declared with
   6 fired (INTERNAL_ERROR uncovered, no meta-check); surface-probe has no
   token enum at all; cite-check has no token enum and one CLI arm exercised
   (the empty-scan exit-2 mapping at 2527-2533 is asserted only as a condition,
   not as an exit code, 1964-1970).
4. Verdict-line exactness tiers observed: (a) full-line literal equality —
   proxy-check 1368, claims-check 756, kimi-census 512; (b) anchored regex with
   numeric field capture — round-gate 863-868; (c) `startsWith` — kimi-census
   777; (d) `.includes` — cite-check 1960, surface-probe 1369, claims-check 745,
   round-gate fail-closed 1188.
5. Every suite ends with the same two-line shape: a summary count line and one
   `VERDICT:` line; round-gate/proxy additionally self-check that exact shape
   in a nested run (1399-1401, 2261-2263). claims-check and kimi-census print
   FAIL lines only before the summary (858-862, 851-853).
6. All six emit usage exit 64 (cite-check 2512, surface-probe 1481,
   round-gate 633/638, proxy-check 2341, claims-check 883/898,
   kimi-census 864/876).

## 8. Inference (I)

1. I: the "every declared kind fires" meta-checks are arm-coverage detectors,
   not mutation controls — they prove each branch is *reached*, not that a
   wrong implementation would be *caught* (e.g. claims-check 827 named the one
   case where a kind-blind mutant would be caught).
2. I: cite-check's hermetic group is the weakest of the six on
   self-checking axes (no arm-coverage meta-check, no mutation arm, substring
   verdict asserts); its compensating strength is repair-regression case names
   citing rounds 13/23/25-29 (e.g. 139, 161, 2034, 1711-1829).
3. I: the hermetic counts are loop-sensitive (proxy 71 literal sites → 102
   cases; claims 35 → 39; kimi 41 → 43), so "case count" in any report must
   name the executed summary line, not a source grep.

## 9. Unknowns (U)

1. Integration group of cite-check was not executed (`--integrations` needs the
   live tree; read-only probe chose not to trigger it). Actual integration case
   count and pass state unmeasured — the 9 `checkI(` sites are source-level only.
2. round-gate `INTERNAL_ERROR` fail-closed arm fire-state unverified.
3. No measure of whether these suites would catch a *regression* inserted into
   their own gate code (no mutant experiments were run — out of read-only probe
   scope; any future run must be a copy under `/tmp`).
4. Whether any of the six suites was run by kumitate's own closeouts at these
   exact revisions is not checked here (would need kumitate LOG.md/round reports;
   not in this assignment's scope).

## Errata (append-only)

(none yet)
