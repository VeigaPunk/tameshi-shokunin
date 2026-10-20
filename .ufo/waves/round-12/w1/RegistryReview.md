# RegistryReview — SOURCES registry check (tameshi round 12, w1)

Read-only. No repo file written except this report. No tools installed or updated. No network fetch; all values below are from committed or retained repo evidence.

## 1. Contract allowed mutations (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, frozen)

- Rule 1: a row is a claim, written only after opening its source in the round that writes it. Round lesson `## Gate` records URL, access date, and a ≤25-word quote with location for each **new** row.
- Rule 2 (append-only): only `status`, `recheck`, and `used-by` change in place. Each change is logged old→new in the round lesson. A correction is a **new** row whose `teaches` opens `supersedes S0NN —`.
- Immutable in place: `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`, `id`.
- `status` vocabulary: `queued` | `mined` (requires ≥1 existing `used-by` path) | `rejected`.
- `used-by`: repo-relative paths, comma-separated, or `—`.
- Next unused id: S047 (`corpus/SOURCES.md` Id allocation). S038–S039 retired, never reused.
- Rule 5: a search log entry is required for any bounded search; a negative claim carries its sweep.

## 2. Current committed values (HEAD = working tree; `sha256 corpus/SOURCES.md` = `6b34e899…2827` both; no uncommitted drift at check time)

| id | tier | kind | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S004 | A | docs | mined | 2026-10-19 | on-release | corpus/knowledge/mutation-score-semantics.md |
| S006 | A | code | mined | 2026-10-19 | 90d | corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md |
| S026 | A | docs | queued | 2026-10-19 | 730d | — |
| S040 | B | paper | queued | 2026-10-19 | 730d | — |

Anchors (immutable): S004 `§Tests fail in an clean tree? and §Mutant outcomes @ mutants.rs, fetched 2026-10-19`; S006 `README §The three verdicts and §How a row is run @ currentOid 7eefc73010ad6342b80e3ed43915503e02c90618`; S026 `Post body, published 2016-05-27 (fetched 2026-10-19)`; S040 `Abstract, p. 17:1; TOSEM 2021 author copy`.

Recheck commands (not in registry; recorded elsewhere):
- S004: `curl -fsSL 'https://mutants.rs/using-results.html' | grep -c 'inconclusive about test coverage'` → observed 1 (`score-semantics/opened.tsv`, S004.html:203-205).
- S006: knowledge file `witness-scoped-kill-verdict.md` line 3 greps `raw.githubusercontent.com/BWBama85/shmutant/main/README.md`, not the pinned commit → 1. The pinned-commit recheck is `.../7eefc73.../README.md`. See risk R3.
- S026, S040: no recheck command recorded anywhere in the repo.

## 3. Evidence for the teaches claims (retained bodies only)

- S004: `score-semantics/S004.html` (sha256 5ec9ba95…2334, matches ledger) contains:
  - L184–187 "Tests fail in an clean tree?" … "cargo test passes reliably when copied to a temporary directory" → supports the teaches clause "tests must first pass reliably in a copied tree".
  - L203–205 unviable "is inconclusive about test coverage" → supports the inconclusive clause.
  - **Not found**: `in-diff`, `--iterate`, or any caution about them in the retained body (0 matches). The teaches clause "--in-diff and --iterate carry explicit cautions" rests on pages in the registry source list (in-diff.html, iterate.html) that are not retained.
- S006: `score-semantics/S006.md` (sha256 dc0051c7…0178a3) L29–31 contains the `killed` and `accidental` verdict lines. The retained body does not contain "0 stars" or "239 commits" (teaches clause unverified in retained evidence).
- S026: no retained body in the repo. The sole evidence is the ledger quote `about 1.5% of all test runs reporting a "flaky" result` (`.ufo/evidence/kaika-round-1/sources-opened.tsv`). The teaches "about 1.5% of test runs are flaky" is a paraphrase that differs in meaning ("reporting a flaky result" vs "are flaky"). The "about 84% of pass-to-fail transitions" and "fail-3-in-a-row" clauses have no retained support.
- S040: no retained body. Ledger quote `Tests that fail inconsistently, without changes to the code under test, are described as flaky.` supports the teaches clause "defining flakiness as failing inconsistently without changes to the code under test".

## 4. Old-value table for L1 change ledger (values to restate before any edit)

| id | field | old value | allowed new value (this round) | required log |
|---|---|---|---|---|
| S004 | status | mined | mined (unchanged) | none unless status moves |
| S004 | recheck | on-release | unchanged unless re-cadenced | log if changed |
| S004 | used-by | corpus/knowledge/mutation-score-semantics.md | append `corpus/knowledge/repeated-control-precondition.md` if cited | old→new in round lesson |
| S006 | status | mined | mined | — |
| S006 | recheck | 90d | unchanged | — |
| S006 | used-by | witness-scoped-kill-verdict.md, mutation-score-semantics.md | unchanged unless new citer | — |
| S026 | status | queued | `mined` only if used-by is non-empty and the file exists | old→new logged |
| S026 | recheck | 730d | unchanged | — |
| S026 | used-by | — | path of the citing knowledge file | old→new logged |
| S040 | status | queued | `mined` only if used-by is non-empty and the file exists | old→new logged |
| S040 | recheck | 730d | unchanged | — |
| S040 | used-by | — | path of the citing knowledge file | old→new logged |

Frozen for all four: id, source, kind, tier, scope, anchor, teaches, opened.

## 5. Census risks

- R1 (census A, `sources-census-v2.sh`): setting S026 or S040 to `mined` with a used-by path that does not yet exist fails `== A mined used-by missing`. The knowledge file `corpus/knowledge/repeated-control-precondition.md` does not exist yet (`ls corpus/knowledge`). Create it before the status flip, in the same change.
- R2 (census H4 / B2): the cited file must contain the row id (`S026` / `S040`) or the source basename (`flaky-tests-at-google-and-how-we.html` / `2021a.pdf`). Otherwise `no-id-or-path-cite` (B2 gate, exit 1).
- R3: S006 recheck command in the witness knowledge file targets `main`, not the pinned commit. A README change on main makes the recheck print 0 for reasons unrelated to pinned semantics. Registry recheck `90d` does not say which ref to use.
- R4: sources-opened.tsv records S006 sha256 `164e5fb8…7752`, but the retained body digest (score-semantics/S006.md and witness/README.md) is `dc0051c7…0178a3`. The ledger hash is not the body digest. Mismatch left unexplained in the repo.
- R5 (append-only): S004 teaches "--in-diff and --iterate carry explicit cautions" is unsupported by the retained body, and S026 teaches is paraphrased beyond its quote. Under rule 2 neither can be edited in place. A correction must be a new row `S047 … teaches: supersedes S004 — …` (or S026/S040 equivalent), with a rule-1 gate entry.
- R6 (no repo-side `SOURCES-CONTRACT-v1.md` in `corpus/`): the contract lives at `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`. Both `corpus/SOURCES.md` line 4 and `corpus/QUALITY.md` point at `SOURCES-CONTRACT-v1.md` by bare name, which does not resolve from `corpus/`.
- R7 (log target): contract rule 2 names the round lesson (`corpus/lessons/round-N.md`). No round-12 lesson file exists (`corpus/lessons` has round-1.md, round-1-verifier-spotcheck.md, round-10.md). The round-12 LOG.md entry is also absent. The assignment asks for L1 LOG.md. L1 must record old→new in both or the contract log rule is not met.
- R8: `corpus/SOURCES.md` is the only SOURCES file. Its Search log has no round-12 entry yet. Any re-open must add one (rule 5).

## 6. Exact owned paths for a future write (for L1, not written here)

- `corpus/SOURCES.md` (status / used-by / recheck cells of S004, S006, S026, S040; new rows start at S047)
- `corpus/knowledge/repeated-control-precondition.md` (new; source/verified-at/recheck header per QUALITY.md 10)
- `corpus/lessons/round-12.md` (or LOG.md entry per L1 plan) for the old→new log and the rule-1 Gate entries
- `corpus/README.md` frontier row F3 only if L1 decides so

Not touched by this review.

## 7. Not verified

- No live fetch of S004, S006, S026, S040 in this check. Current live-page status is unobserved.
- `sources-census-v2.sh` and the other census scripts were not run (instruction: no mid-flight tests). The R1–R2 risks come from reading the scripts and the registry, not from a run.
- No authority is claimed. This report is advisory and lane-internal, not an independent non-author admission.

## Install/update record

None. No tool was installed or upgraded.
