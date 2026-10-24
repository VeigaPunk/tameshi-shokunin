# W2ScoutEvidenceTree — round-36 evidence-tree recon

Attacked: `.ufo/evidence/round-36/` — full inventory (file, size, sha256, claim
supported) plus orphan-receipt analysis against the citing documents
`LOG.md` §Round 36, `SCORECARD.md` §Round 36, `corpus/lessons/round-36.md`, and
`corpus/lessons/round-36-verifier-spotcheck.md` (closure verifier; cited as
secondary context where relevant).

Recon commands (read-only, lane HEAD `fbb01cf46f`):
- `find .ufo/evidence/round-36 -type f -exec sha256sum {} \;` (34 files)
- `git ls-tree -r HEAD --name-only -- .ufo/evidence/round-36/` vs `find` (diff)
- `git log --all --name-only -- .ufo/evidence/round-36/` (files ever committed)
- `git show --stat d9c496b` (receipts commit), `git log --oneline -8` (rev map)
- `grep -F <stem>` of every file basename/stem against the four citing docs
- content reads: `contract.json`, `affected-sections.json`,
  `refresh-receipts.json`, all monitor/counter `.stdout`/`.exit` receipts

## Revision map (resolved from `git log` + receipt contents)

| Short rev | Role | Commit subject |
|---|---|---|
| `796e08b8` | C1 **before** (r35 tip) | round-35 verifier spot-check |
| `e423c41b` | content commit / do-nothing **control** | round-36 content (LOG/SCORECARD/lesson/S103/contract/specs) |
| `b455001e` | **refresh commit** (measurement commit, C1 after) | round-36 cold-read refresh (ledger entries + traces + receipts) |
| `d9c496b` | receipts commit | adds all `after/` + `control/` run receipts |
| `fbb01cf` | lane tip | round-36 verifier spot-check |

`91373d55` (in the two control counter receipts) is the emptied-panel mutant —
created in a scratch clone, unreachable from the lane (verifier spotcheck
routed note 1, status-neutral).

## Inventory (34 files)

### contract.json + c1/

| File | Bytes | sha256 | Claim | Cited by |
|---|---|---|---|---|
| `contract.json` | 3,214 | `3aaabcdd…` | both (frozen pre-data contract) | LOG, SCORECARD, spotcheck |
| `c1/c1-measure-v2.py` | 24,639 | `9eb8944c…` | **C2** counter (frozen; pin matches contract `counter_sha256`) | LOG, SCORECARD, spotcheck |
| `c1/__pycache__/c1-measure-v2.cpython-314.pyc` | 35,496 | `435e5522…` | none — build artifact | **NONE — ORPHAN** (see below) |

### coldread/ (C1 refresh proof)

| File | Bytes | sha256 | Claim | Cited by |
|---|---|---|---|---|
| `coldread/affected-sections.json` | 2,127 | `0a0a707a…` | C1 (drift map, rev `e423c41b`) | weak — only via SCORECARD's `.ufo/evidence/round-36/coldread/` dir citation; no basename hit anywhere |
| `coldread/refresh-specs.json` | 1,883 | `a53e45e3…` | C1 | LOG (pattern `refresh-{specs,receipts}.json`), SCORECARD |
| `coldread/refresh-receipts.json` | 7,179 | `407478a9…` | C1 (+S103 mining: every receipt carries `cited_source: S103…` and the verbatim scope line) | LOG (pattern), SCORECARD, lesson Gate, spotcheck |
| `coldread/traces/L1/source-{1..4}.json` | 2,334 / 1,576 / 1,724 / 1,482 | `908dfa76…` `1e23a1ad…` `c039d691…` `065c4a14…` | C1 (L1 author source-read traces for the four drifted headings) | dir-pattern citation `traces/L1/` in LOG + SCORECARD; individual filenames never named |

### control/ (do-nothing controls)

| File | Bytes | sha256 | Claim | Cited by |
|---|---|---|---|---|
| `control/monitor-at-e423c41b.{exit,stderr,stdout}` | 7 / 0 / 247,191 | `418a5c17…` `e3b0c442…` `b49c84b1…` | C1 control — measured `calibration_restraint_score: 6, sections_covered: 60` at content commit (verified in stdout) | LOG + SCORECARD as **stale alias** `monitor-at-content-commit.*` (pattern does not match the real filename); spotcheck cites the real name |
| `control/v1-at-emptypanel.{exit,stderr,stdout}` | 10 / 0 / 1,100 | `aa0b9bd9…` `e3b0c442…` `88ce373f…` | C2 before-demo — v1 vacuous PASS `pub_kill=0/0 pub_accept=0/0 … C1_R35_PASS=true`, exit 0 (verified) | LOG, SCORECARD |
| `control/v2-at-emptypanel.{exit,stderr,stdout}` | 10 / 0 / 1,105 | `6a7b8257…` `e3b0c442…` `1334ae1f…` | C2 — v2 fails same mutant `C1_R36V2_PASS=false`, exit 1 (verified) | LOG, SCORECARD |

### after/ (deciding + before + guardrail receipts)

| File | Bytes | sha256 | Claim | Cited by |
|---|---|---|---|---|
| `after/monitor-at-796e08b.{exit,stderr,stdout}` | 7 / 0 / 247,100 | `418a5c17…` `e3b0c442…` `7685a130…` | C1 **before** — score `6`, `60/64` (verified in stdout) | LOG, SCORECARD, spotcheck — **but misplaced under `after/`** (it is the before run) |
| `after/monitor-at-b455001e.{exit,stderr,stdout}` | 7 / 0 / 243,253 | `418a5c17…` `e3b0c442…` `6b287d9e…` | C1 **after** — score `8`, `64/64` at refresh commit (verified) | spotcheck; LOG names it only via "`monitor-at-<rev>` receipt filename" pattern |
| `after/c1v2-at-b455001e.{exit,stderr,stdout}` | 7 / 0 / 2,079 | `418a5c17…` `e3b0c442…` `5e2b4e15…` | C2 deciding run — `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 … C1_R36V2_PASS=true`, exit 0 (verified; exactly ONE deciding run per kill rule) | LOG + SCORECARD via `c1v2-at-<rev>.*` pattern; spotcheck verbatim |
| `after/census-at-b455001e.{exit,stdout}` | 14 / 863 | `565cdcbc…` `19f1d44f…` | **Frontier** (S103 row growth; census exit 0, `tameshi ok` final line) | **ORPHAN by name** — lesson says receipts "kept under `.ufo/evidence/round-36/`" without naming files; no basename hit in any citing doc (value cited: "exit 0, 100 rows" in LOG/lesson) |
| `after/sources-rows-at-b455001e.txt` | 4 | `eea8254c…` | Frontier — row count `100` | **ORPHAN by name** — same as above |
| `after/depthD-at-b455001e.stdout` | 99 | `1c3e232d…` | Guardrail — `recorded_cases=9 depth_score=9` + runner sha `a7d3f2dd…` | spotcheck only (`after/depthD-at-b455001e.stdout`); LOG/SCORECARD cite the value, never the file |

### src/ (frontier)

| File | Bytes | sha256 | Claim | Cited by |
|---|---|---|---|---|
| `src/s103-git-hash-object.html` | 29,933 | `dd826dae…` | Frontier S103 snapshot — sha matches LOG/lesson/contract/spotcheck (verified) | LOG, lesson, spotcheck |

## Orphans

**True orphan (uncited AND uncommitted):**
- `c1/__pycache__/c1-measure-v2.cpython-314.pyc` — the only file on disk
  absent from `git ls-tree` (all 33 other files are committed). Interpreter
  build artifact left by a `python3` run without `-B`; not a receipt, cited by
  nothing. Harmless but dirty: a future `add -A` would commit a non-receipt.

**Cited-by-value-only (receipt exists, its *result* is cited, filename never is):**
- `after/census-at-b455001e.{exit,stdout}` — LOG/lesson cite "exit 0, 100 rows"
  and lesson says "both receipts kept under `.ufo/evidence/round-36/`" but no
  doc names the files.
- `after/sources-rows-at-b455001e.txt` — same.
- `after/depthD-at-b455001e.stdout` — SCORECARD's numeric block quotes
  `recorded_cases=9 depth_score=9` + runner sha but not the path; only the
  verifier spotcheck names it.

**Dir-pattern-only (never individually named):**
- `coldread/traces/L1/source-{1..4}.json` (cited as `traces/L1/`),
  `coldread/affected-sections.json` (cited only via the `coldread/` dir),
  `after/monitor-at-b455001e.*` + `after/c1v2-at-b455001e.*` (cited via
  `<rev>` filename patterns — resolvable, the rev is named in text).

## Citation-side defects (receipt missing / dead pointer)

1. **Start-census receipt absent.** Lesson Gate: "Census: round start (tip
   `796e08b`) `sources-census.sh validate` exit 0, 99 rows … — **both receipts
   kept under `.ufo/evidence/round-36/`**." Only the round-end receipt
   (`census-at-b455001e.*`) exists; no start-census file was ever committed
   under `round-36/` (`git log --all --name-only` confirms — every prior round
   keeps a `census-start.*`/before receipt). The 99-row claim is backed only
   by the monitor's sources block (spotcheck re-derived it), not by a stored
   census receipt — an evidence-standard gap under the same class as routed
   defect 1 (a cited artifact that does not resolve).
2. **Stale alias for the control monitor receipt.** LOG and SCORECARD cite
   `control/monitor-at-content-commit.*`; the committed file is
   `control/monitor-at-e423c41b.*`. The pattern is unresolvable as written;
   only the spotcheck cites the real name.
3. **"Round-36 report" is not a lane file.** LOG names it twice (hash source
   for the refresh commit; itemized prepared seats). It resolves only outside
   the lane: `.ufo/reports/round-36/tameshi.md` @ fleet `f4ef9536` (per the
   verifier spotcheck header). Under QUALITY criterion 72's letter this is a
   pointer whose target lives outside the citing repo.
4. **Misplaced before-receipt.** `after/monitor-at-796e08b.*` is the C1
   *before* run living in `after/` (naming is rev-keyed, so harmless to
   resolve, but the dir lies: `after/` holds two monitor runs at different
   revs, only one of them the after).

## Consistency spot-checks (all pass)

- v2 counter sha256 `9eb8944c…` = contract `counter_sha256` = frozen list. ✔
- S103 snapshot sha `dd826dae…` = LOG = lesson = contract `new_source_row`. ✔
- Monitor scores read back: `796e08b`→6/60-64, `e423c41b`→6/60-64 (control:
  record edits alone do not restore credit), `b455001e`→8/64-64. Matches
  LOG/SCORECARD claims exactly. ✔
- Counter verdicts: v1 empty-panel `C1_R35_PASS=true` exit 0; v2 same panel
  `C1_R36V2_PASS=false` exit 1; v2 deciding `C1_R36V2_PASS=true` exit 0.
  Exactly one deciding receipt — kill rule honored. ✔
- `refresh-receipts.json`: 4 entries added / 493 retained, revision
  `e423c41b`, carries the verbatim protocol scope line; every receipt cites
  S103 (`cited_source`) — the lesson's "mined into refresh-receipts" holds. ✔
- `affected-sections.json` revision field is `e423c41b` (the content commit,
  pre-refresh) — consistent with its role as the drift map that drove the
  refresh, not an after-state.

## Verdict

**INVENTORY COMPLETE — 34 files mapped (33 committed); 1 true orphan
(`__pycache__/*.pyc`, uncited + untracked); 3 receipts orphan-by-name
(census pair, sources-rows; values cited); 6 files dir-pattern-only; 4
citation-side defects: missing start-census receipt vs. lesson claim,
`monitor-at-content-commit.*` stale alias in LOG+SCORECARD, fleet-resident
"round-36 report" pointer, before-receipt filed under `after/`.**
