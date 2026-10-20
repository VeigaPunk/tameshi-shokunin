# S01 — gate/probe registry enumeration (round 17, wave 1)

Question: enumerate every gate/probe registry row in `SKILL.md` at
`98bea7da5801f4bc58e4187690ee1687c8a5061f` and every `SCORECARD.md`
`## Capabilities` evidence command; count the active entry commands. This is the
independent source list for X04's `tools/registry.json`.

Method (observed, not inferred):

- Page bytes read with `git show 98bea7da…:SKILL.md` / `:SCORECARD.md`
  (`SKILL.md` = 1813 lines, last line unterminated; `SCORECARD.md` = 594).
- Row census: `grep -c -E '^\| .*\| *(gate|probe|historical gate, not active) *\|'`
  → **12**; `grep -c 'Self-test command'` → **4** (the round-16 table drops that
  column).
- `git status --porcelain -- SKILL.md SCORECARD.md` at check time → empty; the
  tracked tree equals the pin for both pages. Only `.gitignore` and
  `.ufo/evidence/round-16/round-gate/runner-sha256.txt` differ vs the pin
  (unrelated to instruments), so live tool runs below are the pinned bytes
  (`tools/mutate-and-run.sh` blob sha256 `0673d2e5…8118aa` at the pin and live).
- `tools/registry.json`: **absent at the pin** (`git ls-tree
  98bea7da…:tools/` lists only the seven pre-existing tools) and still absent
  at check time — it is X04's wave-1 new file. `tools/registry-check.py` is
  also absent at the pin but **present in the live tree** (24,399 bytes,
  mtime 12:26 — X03's new file), so it is wave material, not pin material.
  §4 is therefore a comparison key, not a diff against a delivered registry.

## 1. SKILL.md — five registry tables, 12 rows

Table locations: §Round-12 `### Gate/probe registry` @1499 (header @1501),
§Round-13 @1548 (header @1550), §Round-14 @1597 (header @1599),
§Round-15 @1676 (header @1678), §Round-16 @1806 (header @1808). The first four
are 8-column (`Name|Kind|Entry command|Verdict map|Self-test command|Pinned
values|Write scope|Owner`); round 16 is 4-column (`Name|Kind|Command|Exits`),
so it has no self-test/pins/write-scope/owner columns. All 8-column rows list
owner `tameshi`.

| # | Line | Name | Kind (cell) | Entry command | Verdict map (row text) | Self-test (row text) | State — marker |
|---|---|---|---|---|---|---|---|
| R1 | 1503 | `repeated pristine controls` | gate | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` **or** `--snapshot DIR` | `0 clean; 1 failed; 2 and 64 could-not-evaluate` | `python3 tools/repeat-control.py --selftest` | **active** — round-12 table carries no archive/supersede marker (1499–1514) |
| R2 | 1504 | `bash declared-witness study` | probe | `python3 tools/bash-witness-study.py count` | `0 complete classified sample; 1 unresolved/failed integrity; 2 could-not-evaluate; 64 usage/could-not-evaluate` | `python3 tools/bash-witness-study.py selftest` (positional subcommand, **not** `--selftest`) | **active** — no marker |
| R3 | 1552 | `six-leg content disposition` | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | `0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed` | `python3 tools/pin-disposition.py --selftest` | **active** — no marker |
| R4 | 1553 | `exposed witness provenance companion` | gate | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | `0 metadata_consistent/clean; 1 metadata_inconsistent/failed; 2 input_unavailable or snapshot_tampered/could-not-evaluate, including usage` | `python3 tools/witness-metadata.py --selftest` | **active** — no marker |
| R5 | 1601 | `effective expectation disposition` (round-14 row) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | `0 clean; 1 failed semantic expectations; 2 could-not-evaluate invalid/missing/tampered inputs; 64 usage` | `python3 tools/evidence-disposition.py --selftest` | **superseded** — table heading @1597 is `### Round-14 historical registry — superseded by round 15`; the same capability is re-registered @1681 (R8) |
| R6 | 1602 | `archived invocation context capture` | **`historical gate, not active`** (cell verbatim) | **`do not run; retained source .ufo/evidence/round-14/capture-context.py only`** (verbatim) | `historical outcomes retained, not an active verdict map` | `historical helper-only controls do not satisfy the standalone gate selftest` | **archived** — row kind cell; @1630 `inline archive marker, not a callable entry`; @1632 `**archived, not active**`; @1636 `both are now marked archive-only` |
| R7 | 1680 | `retained invocation-context gate` | gate | `python3 tools/context-capture.py --check` (frozen round-14 clean receipt); `--check --receipt FILE --expected FILE` for a caller-pinned retained receipt | `0 clean (context_consistent); 1 failed stable finding ID (e.g. missing_injected_environment); 2 and 64 could-not-evaluate (receipt/expected missing, malformed or tampered, e.g. snapshot_tampered; 64 usage_error)` | `python3 tools/context-capture.py --selftest` (prose @1705: selftest `0/1/2` pass/case-fail/setup-inability, `64` invalid invocation) | **active** — no marker |
| R8 | 1681 | `effective expectation disposition` (round-15 row) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` **+ in-row erratum:** since round 16 the runner input moved, so `--root .` returns `2 expected_input_digest_mismatch` by design; use `--root` on `git archive 28aeef4` extracted to /tmp → `0 clean` | `0 clean; 1 failed semantic expectations; 2 and 64 could-not-evaluate (invalid, missing or tampered inputs; 64 usage)` | `python3 tools/evidence-disposition.py --selftest` | **active** — the errata @1741 is an in-place repair of this row; no archive marker |
| R9 | 1810 | `tools/mutate-and-run.sh` | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | `selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage` | in Command cell (`--selftest`); no separate column in the 4-col table | **active** — no marker |
| R10 | 1811 | `.ufo/evidence/round-16/measure.py` | probe | `python3 .ufo/evidence/round-16/measure.py --rev REV` · `--selftest` | `0 measured · 2 rev/blob missing · 64 usage` | in Command cell (`--selftest`) | **active** — no marker |
| R11 | 1812 | `.ufo/evidence/round-16/coldread/assemble.py` | gate | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` **only** — live mode is not declared | `0 every bucket covered · 1 a bucket uncovered or a report rejected · 2 usage (argparse) or an invalid override` (errata @1742: argparse usage exits 2, not 64) | in Command cell (`--selftest`) | **active** — no marker; **entry gap** (see §4) |
| R12 | 1813 | `.ufo/evidence/round-16/attribution/reattribute.py` | probe | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` **only** — live mode is not declared | `0 corrected rule passes the oracle · 1 it fails` | in Command cell (`--selftest`) | **active** — no marker; **entry gap** (see §4) |

Pins that determine verdicts (quoted, not reproduced in full): R7 pins the
frozen clean receipt `.ufo/evidence/round-14/context-receipt.json` sha256
`05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`, negative
fixture `context-missing-env.json` sha256
`1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`, and schema
`tameshi-context-expected-v1`; R8 pins the round-14 manifest pair. R7's write
scope: check writes nothing, never opens recorded root paths or executes stored
argv; selftest writes isolated temp fixtures.

## 2. SCORECARD.md `## Capabilities` — 8 rows (240–247)

The table has no `Kind`/`Self-test`/`Status` columns: `Kind` below is derived
from the matching SKILL registry row; `Status` follows the table convention
(`@249`: “Rows enter only through a round that demonstrates the capability
running (`AXES.md` §Capabilities); none enter through this rollout.”). No row
carries an archive marker; the “historical …” strings are the *first-working
round* notes, not retirement.

| # | Line | Capability | Evidence command (verbatim) | Kind | Registered entry / verdict map (SKILL) | Self-test | Status marker (quoted) | SKILL line |
|---|---|---|---|---|---|---|---|---|
| B1 | 240 | sources-registry | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 44 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | **unregistered** (no SKILL row; the script is live-tree, gate-shaped: `exit $bad`, 0 CLEAN / 1 VIOLATIONS; no argv, no selftest) | itself; verdict `SOURCES_CENSUS: CLEAN` / `VIOLATIONS` | none | active — `fleet round 1 (kaika)` | **none** (0 occurrences of the command in SKILL.md) |
| B2 | 241 | mutation sweep runner | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | gate | R9 @1810; verdict map as R9 | same command | active — `historical round 3 (SCORECARD.md:16); re-demonstrated fleet round 1` | 1810 (map row 1391) |
| B3 | 242 | six-leg regression ledger | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/h1b-regression.stdout`) | gate | R9 @1810 (`--regression`); verdict map as R9 | `bash tools/mutate-and-run.sh --selftest` | active — `historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1`; **name/evidence dated**: SKILL @1391 says “seven since round 16”, SCORECARD @570 says `cases 6 → 7 PASS` | 1810 (map row 1391) |
| B4 | 243 | repeated pristine-control gate | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; red-before loop mutant fails the same mismatch oracle; measured `9df9212d…` | gate | R1 @1503 | same command | active — `round 12; lane demonstrated, outside admission pending` | 1503 |
| B5 | 244 | six-leg content-disposition probe | `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0; real read changed3/unchanged3/unavailable0; measured `4acc607d…` | probe | R3 @1552 | same command | active — `round 13; lane demonstrated, outside admission pending` | 1552 |
| B6 | 245 | exposed witness provenance correction | pointer is four receipts, no single command: `metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0` + `producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607d…` | gate | R4 @1553 (entry `--check --companion …`); verdict map as R4 | `python3 tools/witness-metadata.py --selftest` | active — `round 13; lane demonstrated, outside admission pending` | 1553 |
| B7 | 246 | effective expectation reconciliation | `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; measured `6431478` | gate | R8 @1681 is active (R5 @1601 is the superseded row); verdict map as R8 | same command | active — `round14; lane demonstrated, separate outside admission pending` | 1681 (historical row 1601) |
| B8 | 247 | retained invocation-context gate | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | gate | R7 @1680 (`tools/context-capture.py --check`); verdict map as R7 | `python3 tools/context-capture.py --selftest` | active — `round15; lane demonstrated, separate non-author admission pending` | 1680 — **the evidence command itself has no SKILL line** (0 hits for `verify.py` in SKILL.md) |

## 3. Counts (acceptance)

- **SKILL registry rows: 12** across 5 tables (4 eight-column, 1 four-column).
  - **Active: 10** (R1, R2, R3, R4, R7, R8, R9, R10, R11, R12).
  - **Superseded: 1** (R5 @1601 — same capability re-registered at R8 @1681).
  - **Archived / not active: 1** (R6 @1602 — kind cell `historical gate, not active`, entry cell `do not run`).
- **Active entry commands: 10 command forms across 8 active rows**
  (non-selftest):
  1. `tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` and
     `--snapshot DIR` (2 forms);
  2. `tools/bash-witness-study.py count`;
  3. `tools/pin-disposition.py --manifest … --root …`;
  4. `tools/witness-metadata.py --check --companion …`;
  5. `tools/context-capture.py --check` and
     `--check --receipt FILE --expected FILE` (2 forms);
  6. `tools/evidence-disposition.py --root … --dispositions … --json`;
  7. `tools/mutate-and-run.sh --regression`;
  8. `.ufo/evidence/round-16/measure.py --rev REV`.
  The remaining **2 active rows (R11 assemble, R12 reattribute) declare no
  live entry**: their Command cell is `--selftest` only.
- **Active self-test commands: 10** (one per active row; R2's is the
  `selftest` positional subcommand, not `--selftest`).
- **+1 SCORECARD-only active entry** (B1 `sources-census-v2.sh`, no SKILL row)
  → **11 active registered callables** in total; **10** of them carry a SKILL
  registry line.
- **1 active capability whose SCORECARD evidence command is not the
  SKILL-registered instrument** (B8: `round-15/verify.py` vs
  `tools/context-capture.py`).
- **2 active rows with an undeclared live mode** (R11, R12).

## 4. Independent check key for X04's registry (file absent at pin and check time)

Expected active instrument rows from the two sources (10 SKILL + 1 SCORECARD-only),
before X04's deliberate round-17 additions (disposition v2 live/before split,
`registry-check.py`, round-17 `measure.py` v2, `trace-inputs.py`, v2
`assemble.py`, and their selftest rows). Traps, each grounded in §1/§2 or an
observed run:

1. **Skip R6** (`archived invocation context capture`). `tools/` has no
   `capture-context.py`; the retained script is evidence-only at the pin.
2. **Do not register R5's `--root .` as the active disposition row.** R8 @1681
   is the active row and already carries the erratum: at the pin, R5/R8's
   literal command exits `2 expected_input_digest_mismatch` (observed; detail
   `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`). Round 17
   replaces it with `.ufo/evidence/round-17/dispositions.json` (expect 0) and
   `dispositions-before.json` (expect 1) per X04's target.
3. **B8's `verify.py` is not the live instrument.** It is a round-15
   integration runner pinned to `7650fe4…`; SKILL names only
   `tools/context-capture.py` (@1680). Registering `verify.py` would make the
   monitor replay a frozen round, not the branch tip.
4. **B1 `sources-census-v2.sh` has no SKILL row.** It is an active SCORECARD
   capability row with no archive marker, so it must be registered from
   SCORECARD alone; its argv has no arguments and no `timeout`-sensitive output.
5. **R11/R12 declare only `--selftest`.** Their default modes exist
   (`assemble.py` resolves `DEFAULT_OUT = <script dir>/ledger.json` and the
   round-16 report globs; `reattribute.py` writes `OUT_PATH =
   <script dir>/correction.json`), i.e. a live run rewrites frozen evidence —
   [INFERENCE] the rows list only the selftest for that reason. Do not invent a
   live argv; register the selftest row only.
6. **Argv spelling:** R2's selftest is `["selftest"]`; all others are
   `--selftest`. R9's live mode is `--regression`; R10's is `--rev REV`.
7. **Do not pin dated literal counts from evidence pointers.** Observed at the
   pin/live tree: `MUTATE_SELFTEST: 83/83 pass` (SCORECARD says 80/80),
   `SOURCES_CENSUS` A rows = 55 (SCORECARD says 44), `--regression` ledger = 7
   cases (SCORECARD's B3 evidence says `cases=6`; SKILL @1391 already says
   seven since round 16). Exit-only (or stable-token + exit) expectations
   survive; literal counts do not.
8. **The round-16 table's 4-column shape** means a registry builder must take
   `--selftest` from the Command cell there and from the Self-test column in
   rounds 12–15.
9. **Verdict maps are not uniform on `64`:** rounds 12/13/15/16 assign `64`
   usage; the round-13 pin-disposition row carries a *selftest* `1 failed`
   instead of a normal-mode `1`; R7 folds usage into `64 usage_error`; R8 folds
   usage into `64`. Copy the row's own map, never a global lattice.

## 5. Observed runs (hermetic/read-only; live tree = pin for the instruments)

| Command | Exit | Key line |
|---|---|---|
| `python3 tools/repeat-control.py --selftest` | 0 | `SELFTEST: PASS (29 cases)` |
| `python3 tools/bash-witness-study.py selftest` | 0 | `WITNESS_SELFTEST: 41/41 pass` / `VERDICT: PASS` |
| `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 | observations emitted; last leg `content_status=unchanged`, `result_reuse=not_established` |
| `python3 tools/pin-disposition.py --selftest` | 0 | `SELFTEST: PASS (18/18)` |
| `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 | `WITNESS_METADATA: metadata_consistent reason=ok …` |
| `python3 tools/witness-metadata.py --selftest` | 0 | `SELFTEST: PASS 39/39` |
| `python3 tools/context-capture.py --check` | 0 | `CONTEXT: OK (id=context_consistent … exit=0 findings=0)` |
| `python3 tools/context-capture.py --selftest` | 0 | `SELFTEST: PASS (49/49)` |
| `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | 2 | `id=expected_input_digest_mismatch`, `error.message` = `tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…` — confirms the @1741 erratum |
| `python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (34/34)` |
| `bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 83/83 pass` / `VERDICT: PASS` |
| `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 38/38 pass` |
| `python3 .ufo/evidence/round-16/measure.py --rev 98bea7da…` | 0 | `box3_full_page: true`, `depth_score: 7`, `sections 54/54`, under the round-16 tool |
| `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | `SELFTEST: all checks passed` |
| `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` |
| `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | 0 | `== A rows` → `55`; `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` |

Not run (out of scope for enumeration; X04's `registry-check.py` is the caller):
`--regression` (7-case replay), `repeat-control.py` run/snapshot modes,
`bash-witness-study.py count`, and the round-16 instruments' live modes.

## 6. Remaining unknowns

- **B1 status.** `sources-registry` is an active SCORECARD capability with no
  SKILL registry row and a script under a historical evidence directory
  (`.ufo/evidence/kaika-round-1/`). [UNKNOWN] whether the L1 registry treats it
  as an active entry command or as historical evidence; the SCORECARD gives no
  archive marker either way.
- **Round-17 rows are not at the pin.** The wave's five new rows (disposition
  v2 live, entry-command monitor, measure v2, trace-inputs, assemble v2) exist
  only in the W03 draft (`.ufo/waves/round-17/w1/W03SkillR17Draft.md:85-101`)
  and the contract, so they cannot be graded against committed SKILL bytes.
- **X04's registry was unwritten at check time** (`ls tools/registry.json` →
  no such file), so no row-by-row comparison was possible; §4 is the key to
  apply when it lands.
- **Selftest-row granularity** (one row per selftest vs entry+selftest folded
  into one row) is X04's schema decision under contract B's
  `kind: gate|probe|selftest`; this enumeration gives both commands per row so
  either shape can be checked.

Verdict: **built** — 12 SKILL registry rows (10 active, 1 superseded, 1 archived/do-not-run) and all 8 SCORECARD capability rows enumerated with entry command, verdict map, self-test, state marker and line, giving **10 active SKILL entry commands (+1 SCORECARD-only = 11)** for X04's independent check.
