# SourceLedger — SOURCES mutable-field vs round-12 lesson ledger

- Seat: `TameshiR12.SourceLedger` (leaf member, read-only, no subagent dispatch)
- Scope: status / recheck / used-by only. Compared the inherited registry (`git show 18ad5d0:corpus/SOURCES.md`, via `git --no-pager diff`) with the worktree `corpus/SOURCES.md` and the lesson ledger `corpus/lessons/round-12.md`.
- Contract applied: `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (rule 2: only `status`, `recheck`, `used-by` change in place, each logged old→new in the round lesson; `mined` = cited by ≥1 `used-by` path). Note: the contract is not at `corpus/`; `corpus/SOURCES.md:4` names it by bare name (see RegistryReview R6).
- Tooling: no installs or updates. Read-only only: `git show`, `git --no-pager diff`, `git status --short`, `find`, grep, file reads.

## 1. Ledger vs registry — field match (all agree)

Pre-values in the ledger match the inherited registry; post-values match the worktree. The git diff shows no other cell changed in any row (tier, opened, teaches, anchor, kind, scope untouched).

| Row | Field | Inherited (18ad5d0) | Ledger old→new (`round-12.md`) | Worktree (`SOURCES.md`) | Result |
|---|---|---|---|---|---|
| S004 | used-by | `…/mutation-score-semantics.md` | `+ corpus/knowledge/repeated-control-precondition.md` (:16) | `…/mutation-score-semantics.md, …/repeated-control-precondition.md` (:15) | match |
| S004 | status / recheck | mined / on-release | mined→mined; on-release→on-release (:16) | mined / on-release (:15) | match |
| S006 | used-by | `witness-scoped-kill-verdict.md, mutation-score-semantics.md` | `+ corpus/lessons/round-12.md` (:17) | `…, corpus/lessons/round-12.md` (:17) | match |
| S006 | status / recheck | mined / 90d | mined→mined; 90d→90d (:17) | mined / 90d (:17) | match |
| S011 | status | queued | queued→mined (:49) | mined (:22) | match |
| S011 | used-by / recheck | — / 730d | —→corpus/lessons/round-12.md; 730d→730d (:49) | corpus/lessons/round-12.md / 730d (:22) | match |
| S026 | status | queued | queued→mined (:18) | mined (:37) | match |
| S026 | used-by / recheck | — / 730d | —→corpus/knowledge/repeated-control-precondition.md; 730d→730d (:18) | …repeated-control-precondition.md / 730d (:37) | match |
| S028 | status | queued | queued→mined (:50) | mined (:39) | match |
| S028 | used-by / recheck | — / 365d | —→corpus/lessons/round-12.md; 365d→365d (:50) | corpus/lessons/round-12.md / 365d (:39) | match |

Rows S001–S003, S005, S007–S010, S012–S025, S027, S029–S031, S040–S046: no change in any field (git diff). S040 stays `queued` (SOURCES.md:49), consistent with ledger silence (see D5).

## 2. Discrepancies (path:line)

### D1 — S026 `mined` rests on a Gate row the ledger itself contradicts (stale ledger)
- Ledger Gate row: `corpus/lessons/round-12.md:13` — "Opened by L1; reader omitted the article body. No article quotation is credited from that partial view." The same ledger flips S026 to `mined` at `round-12.md:18`, and the registry shows `mined` at `corpus/SOURCES.md:37`.
- In-tree evidence contradicts the Gate row: `corpus/knowledge/repeated-control-precondition.md:1,16-21` cites S026 body quotes at `S026.html:1130/1132/1136`; `.ufo/waves/round-12/w1/ControlKnowledge.md:44-46` states "This seat read the body" and calls the lesson gate-table line stale; `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv:8-14` (Q4–Q10) holds the located quotes.
- Consequence: `mined` is contract-valid (cited by a used-by path, rule 2 / status enum), but the ledger's own Gate record for S026 says no quote is credited. The ledger was not updated after the body was read. Correction required in the lesson (append-only), not in the registry cell.

### D2 — Pointer to quotes/mutable changes is wrong for S026
- `corpus/SOURCES.md:101-102` (search log) says "Source quotes and mutable-field changes: `corpus/lessons/round-12.md`, `## Gate`."
- LOG claim, `LOG.md:661`: "Mutable-field ledger and located quotes in `corpus/lessons/round-12.md`." The lesson holds no S026 located quote (`round-12.md:13`); S026 quotes exist only in `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv` and the untracked knowledge file.

### D3 — S011 and S028 flip logs are outside `## Gate`
- `corpus/lessons/round-12.md:5` opens `## Gate`; its ledger (`:15-18`) covers S004, S006, S026 only.
- The S011 and S028 old→new entries (`round-12.md:48-50`) sit under `## Authority and dispatch` → `### Source-review limits` (`round-12.md:34,44`) as "Additional source mining", not under `## Gate`. The registry pointer (`SOURCES.md:101-102`) names `## Gate`, so a reader following it finds no S011/S028 change record. Contract rule 2 is met by content, not by the section the registry names.

### D4 — Registry search log counts omit two opened rows
- `corpus/SOURCES.md:101` (round-12 entry): "Opened existing rows S004, S006 and S026 … identified 3, screened 3, included 3, excluded 0."
- Opened and status-changed in the same round with no registry search-log entry: S011 (`round-12.md:49`; `.ufo/evidence/round-12/SourceFlakyPaper/evidence.json`) and S028 (`round-12.md:50`; `.ufo/evidence/round-12/SourceBazel/source-excerpt.txt:3`, fetched 2026-10-20T02:15:01Z). Contract rule 5 requires the bounded search log to carry the counts. The entry's counts describe 3 rows, not the 5 that changed status or were opened.

### D5 — S040 opened in round 12 but unledgered; LOG cites a ledger that does not contain it
- `LOG.md:661`: "source scouts also opened S011/S028/S040" — cited against `corpus/lessons/round-12.md`.
- S040 opening evidence: `.ufo/waves/round-12/w1/SourceSurvey.md:29` (access 2026-10-19T23:14:00Z) and `.ufo/evidence/round-12/SourceSurvey/opened.tsv:2`.
- Registry: `corpus/SOURCES.md:49` remains `queued`, used-by `—`, recheck 730d. No status cell is wrong: `queued` is the contract value for "opened, worth mining", and ledger silence means unchanged. But the lesson has no S040 entry, so the LOG pointer has no backing record.

### D6 — Used-by targets are untracked files (commit-ordering risk)
- `git status --short`: `?? corpus/lessons/round-12.md`, `?? corpus/knowledge/repeated-control-precondition.md`. Both are used-by targets of changed `mined` rows: `SOURCES.md:15,37` (S004, S026 → knowledge file); `SOURCES.md:17,22,39` (S006, S011, S028 → lesson).
- The worktree census (contract "mined used-by paths exist") passes now; a commit that omits either file leaves committed `mined` rows pointing at nonexistent paths. The seat draft flagged the same risk (`.ufo/evidence/round-12/LessonScribe/outline.md:72`, `capture.txt:37`). Not a ledger mismatch; flagged for L1's commit set.

### D7 — S011/S028 `mined` is contract-valid but stricter than the LessonScribe draft
- `.ufo/evidence/round-12/LessonScribe/outline.md:74` ("mined only if a knowledge file cites it; otherwise stays queued") and `:76` (S028 "queued"). The registry and ledger instead flip both to `mined` with a lesson-only used-by.
- Contract `SOURCES-CONTRACT-v1.md` `used-by` accepts "knowledge entries or lessons", so the flip is permitted. The outline's gate is a seat-level criterion, not a contract rule. Noted for L1; not a contract violation.

## 3. Adjacent, out of field (status-relevant, not status/recheck/used-by)

- `.ufo/waves/round-12/w1/RegistryReview.md:66` (R5): S004 `teaches` ("--in-diff and --iterate carry explicit cautions") is unsupported by the retained body (`RegistryReview.md:36`), and S026 `teaches` is paraphrased beyond its quote. Contract rule 2 forbids in-place edits of `teaches`; a `supersedes S0NN —` row is required. Neither the ledger nor the registry addresses this. This bears on whether S004/S026 `mined` should be considered supported as written.
- `corpus/SOURCES.md:133` next-id `S047` is unchanged; no new rows were written in round 12 (consistent with ledger "No new registry rows").

## 4. Checks that pass
- Ledger pre-values equal the inherited registry for all five rows (S004, S006, S011, S026, S028).
- No tier, `opened`, `kind`, `scope`, `anchor`, or `teaches` cell changed (git diff hunks at `SOURCES.md:12-17`, `34-43`, `98-101`).
- Every `mined` row's used-by path exists in the worktree and names a file that cites the row id (S004→`repeated-control-precondition.md:1`; S006→`round-12.md:12,17`; S011→`round-12.md:46,49`; S026→`repeated-control-precondition.md:16-21`; S028→`round-12.md:46,50`).
- Quoted source sentences in the ledger match retained excerpts: S004 `S004.html:187`; S011 `SourceFlakyPaper/excerpt.txt:10`; S028 `SourceBazel/source-excerpt.txt:11`.

## 5. Residual risk / verification gaps
- No census script was run (assignment is read-only; main agent verifies once). Pass/fail statements above are read-only inspection of the file state, not census output.
- The contract's own census command (`SOURCES-CONTRACT-v1.md` census block) was not executed here.
- `opened` dates for S011 (2026-10-19 per source report) and S040 (2026-10-19T23:14Z) predate the round's observed UTC date 2026-10-20; noted in the ledger at `round-12.md:49`; not a status/recheck/used-by discrepancy.

## 6. Owned paths
- Written: `.ufo/waves/round-12/w2/SourceLedger.md` (this file).
- Not modified: `corpus/SOURCES.md`, `corpus/lessons/round-12.md`, `LOG.md`, all knowledge files.
