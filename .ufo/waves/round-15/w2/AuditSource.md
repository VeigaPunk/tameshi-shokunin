# AuditSource — round-15 S049/S051 source rows, Gate quotes, used-by transitions

Seat: `TameshiR15.AuditSource` (leaf reviewer, static). Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Method: static reads only. No gate, selftest, census, frozen replay or sibling command was executed. Hashing, git read commands and Python parsing (`ast`, regex over `corpus/SOURCES.md`) were used as inspection. One read-only HTTPS fetch of the cited Python documentation page was made to check the S049 quote.

## Bottom line

- **No implementation-critical defect found.** No message was sent to TameshiR15.
- S049 quote, S049 used-by transition, S051 quote and line anchors, the "does not execute retained argv" teaching cell, and the exit-64/classification grounding all **agree** with the source bytes read.
- Bounded weaknesses, all non-blocking: S051 anchor names a version label (`r15`) that does not pin bytes; the file under the S051 anchor changed after its commit; 9 of 28 documented stable finding IDs have no literal selftest pin; a few integration wording and typo defects; LOG does not name the S051 row.
- **Moving target.** `tools/context-capture.py` was committed as `bca5deb` at 05:21:10 (not by this seat) and then edited in the working tree while this review ran. Both revisions were checked; S051's anchor lines resolve in both (see §3).

## 1. Exact reads

| Artifact | Read | Result |
|---|---|---|
| `corpus/SOURCES.md` (working) vs `HEAD` | `git diff`; rows S049 (l.58), S050 (l.59), S051 (l.60); log l.131–135; Id allocation l.169–172 | Diff adds S051 row, appends S049 to used-by only, adds a search-log entry, sets next id S052 |
| `corpus/lessons/round-15.md` | l.1–94; Gate l.11–44; Mistakes l.46–51 | Quotes, word counts, used-by transition and S051 location are stated here |
| `CORPUS.md` | l.89–129 (fields, rules 1–2, tier A, census awk) | Own-work path substitutes for URL; A includes "the lane's own re-runnable gate output"; Rule 1 needs the Gate quote; Rule 2 needs logged old→new |
| `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` | l.19–40, l.49 | `anchor` requires exact line plus revision (version, commit, or date) |
| `tools/context-capture.py` committed `bca5deb`, blob sha256 `0ed784e0…edc` | l.1–31, l.9–14, l.16, l.25–28; `run_selftest_cases`; `parse_argv`/`main` | See §2 |
| `tools/context-capture.py` working tree, sha256 `95f20467…fd43` | same ranges; full diff vs `bca5deb` (23+ / 10−) | Anchors hold; edits are in-flight falsifier repairs |
| `SKILL.md` l.1563–1691 | round-14 and round-15 sections, registry rows, exit-class paragraph | See §2 |
| `corpus/QUALITY.md` l.75–85 | "Criteria appended — round 15" | Criterion `17.` exists; cited as QUALITY17 |
| `corpus/knowledge/incremental-pin-disposition.md` l.359; `corpus/lessons/round-14.md` l.15–42 | S049 citations | Reciprocal citation exists |
| `LOG.md` l.922–942 | round-15 entry | See §2.6 |
| `.ufo/evidence/round-14/capture-context.py` l.553–580 | `decide()` | Returns `mismatch`, exit 1 on any reason |
| `.ufo/evidence/round-14/*` hashes | `sha256sum` of script, `context-receipt.json`, `context-missing-env.json` | `7313e9…`, `05cb55…`, `1ee9d0…`; all equal the SKILL and tool pins |
| `https://docs.python.org/3/library/subprocess.html` | read-only fetch, text normalised | Served as "Python 3.15.0 documentation"; see §2.1 |

## 2. Findings with the evidence behind each

### 2.1 S049 quote — AGREE
- The lesson quote is "If env is not None, it must be a mapping that defines the environment variables for the new process" (l.16–17). The live page contains this exact sentence in the run() env paragraph (counted 2 occurrences). Word count 19, which meets the ≤25 rule in CORPUS Rule 1.
- The sentence continues "these are used instead of the default behavior of inheriting the current process' environment". That supports the row's teaching: explicit mapping defines the child environment. The row does not claim historical injection, so no overclaim.

### 2.2 S049 used-by transition — AGREE, one wording gap
- `git diff` of the S049 row changes only the used-by cell, from `corpus/lessons/round-14.md, corpus/knowledge/incremental-pin-disposition.md` to the same list plus `corpus/lessons/round-15.md`. Status `mined` and recheck `on-release` are unchanged. This matches the lesson l.22–24 and CORPUS Rule 2 (logged old→new).
- Reciprocity: `incremental-pin-disposition.md` l.359 cites S049; `round-14.md` cites S049; `round-15.md` cites S049 and S051. Every used-by path exists on disk.
- **Wording gap (non-blocking).** Lesson l.13 says "Opened this round 2026-10-20: S049". No new S049 row was written; the row dates from round 14. SOURCES log says "Reopened" and LOG says "re-opened". Suggested wording: "Re-opened this round".

### 2.3 S051 quote and anchor lines — AGREE
- Lesson quote: "Check mode writes nothing; the only writes are --selftest fixtures under mkdtemp." In the committed file this sentence wraps across lines 11–12 of the docstring, inside the claimed 9–14 range. Working-tree line 9–10 text changed; lines 11–12 did not.
- Row anchor "Modes lines16–28": in both revisions `Modes:` is at line 16 and `--selftest` spans lines 25–28. Confirmed.
- Static inspection of write sites: `open(..., "w"/"wb")` appears only in `SelftestHarness.check_case` (two sites) and `mkdtemp`/`makedirs` only in the selftest harness. The check path writes nothing.

### 2.4 S051 teaching "replay re-derives bounded raw fields and does not execute retained argv" — AGREE
- The only `subprocess.run` call is `SelftestHarness.run`. The check-mode code path does not spawn git or the probe. The recompute helpers (`recompute_environment`, `recompute_runs`, `recompute_comparison`, `recompute_positive_control`, `recompute_sources`, `recompute_mapping`) read stored raw fields.
- The row scope, "not live command execution or authentication", matches docstring l.9–12 and l.99–103.

### 2.5 S051 "isolated public-CLI self-invocation" — AGREE, bounded
- Selftest invokes `[sys.executable, "-I", SELF, ...]` with `SELFTEST_ENV` (PATH, LC_ALL, GIT_DIR poison), `cwd` set to a temp case directory, and `timeout=60`. This is public CLI, not helper-only.
- AST inventory of `run_selftest_cases` (static, not run): 36 calls, all with literal `expected_id`/`expected_exit` or literal usage expectations. Exit-code pairs in source: 0, 1, 2 and usage 64.
- **Coverage bound (non-blocking).** Documented stable IDs in the docstring number 28. Selftest-pinned IDs number 19. Not pinned in selftest:
  - `environment_delta_mismatch`, `environment_baseline_git_dir`
  - `run_argv_mismatch`, `run_cwd_mismatch`, `run_env_delta_mismatch`
  - `tool_declaration_mismatch` (frozen only)
  - `receipt_unreadable`, `expected_unreadable`, `internal_error`
  - Two of these, the `environment_*` IDs, test the GIT_DIR explicit-environment predicates that the S049 teaching is about. The S051 row and lesson do not claim full ID coverage, and QUALITY17 and PROTOCOL Gate standard require only a literal exit plus a stable finding pair per gate. So this is not a defect; it is a scope to record.

### 2.6 S051 anchor revision — weak, non-blocking
- Contract v1 `anchor` requires "exact section / heading / page / line plus revision (version, commit, or publication date)". S051 gives "r15" (the `VERSION` label on line 121) and `opened 2026-10-20`.
- The `VERSION` line is identical in `bca5deb` and the working tree, so "r15" does not identify the bytes. Counterexample: the committed blob (`0ed784e0…`) and the working copy (`95f20467…`) both satisfy the S051 anchor text, yet they differ in mkdtemp `dir="/tmp"`, a new `KNOWN_ARGUMENTS` value check, `finish()` lane-leak logic, and rewording of docstring lines 9–10. The quote survives, so the located quote still resolves, but the row cannot distinguish which bytes were read.
- Precedent: S050 pins commit `6431478`; S031 pins sha256. Recommend S051 pin the final commit or blob sha at closure. This is not a contract violation as written.

### 2.7 Exit-class and classification grounding — AGREE
- `decide()` in round-14 `capture-context.py` (l.553–580) returns `("mismatch", 1, reasons)` for any reason. Lesson l.49–50 and SKILL l.1626–1632 are consistent with this.
- Round-14 registry row (SKILL l.1602) has no 64 entry. Round-14 script exits 64 at l.613. Lesson l.51 is consistent.
- Round-15 registry rows (SKILL l.1680–1681) map 2 and 64 to could-not-evaluate. The tool docstring stable-ID list (l.58–86) and exit map (l.88–97) match. PROTOCOL.md "Gate standard / Verdict" requires this mapping.
- Frozen pins in the tool (`FROZEN_RECEIPT_SHA256 05cb55…`, `FROZEN_TOOL_SHA256 7313e9…`) equal the on-disk digests of the retained receipt and the archived script.

### 2.8 QUALITY17 — AGREE
- `corpus/QUALITY.md` contains `17.` under "Criteria appended — round 15". The lesson and LOG cite QUALITY17; the reference resolves. The criterion text matches the lesson Mistakes row.

### 2.9 Census invariants — static parse only, no census run
- `corpus/SOURCES.md` working tree: 49 rows, all with 13 `|`-fields, no duplicate ids. Tiers A42/B5/C2. Status mined22/queued24/rejected3. Kind own-work 3 (S031, S050, S051).
- `HEAD`: 48 rows, A41/B5/C2, mined21/queued24/rejected3. The delta is exactly S051 (tier A, mined). Next unused id S052 is consistent.
- Predicted, not observed: W04 warnings unchanged, since S049 and S051 add no new duplicate URL. Stated as static inference.

### 2.10 Integration-document gaps (non-blocking)
1. **LOG.md round-15 entry** (l.922–942, committed in `bca5deb`) does not name the S051 row, the S049 used-by transition, or the next-id change. AGENTS.md requires a LOG entry per change with motivating evidence. Suggested: one added line.
2. **Committed LOG refers to uncommitted artifacts.** At audit time `git status` shows `corpus/lessons/round-15.md`, `corpus/QUALITY.md` (QUALITY17), `corpus/SOURCES.md` (S051), `SKILL.md`, `corpus/README.md` and `.ufo/evidence/round-15/` untracked or modified. The commit must land with them.
3. **SKILL round-15 section** (l.1611–1616) says no S051 row existed "at this write" and cites the lesson rather than the row. The statement is time-bounded and now stale. Optional: cite S051.
4. **Missing-space typos** that break token search and cell reading: lesson l.14 `Python3.15.0`; l.26 `access2026-10-20`; l.29 `contractv1`; LOG l.939 `re-opened2026-10-20`; SOURCES S051 anchor `opened2026-10-20`; round-14 lesson l.42 `idS051`.
5. **Lesson l.13** "Opened this round" — see §2.2.

## 3. Revision state at audit time

- `HEAD` = `bca5deb` ("round-15: retain context gate before falsifier repairs", 05:21:10), touching `LOG.md` and `tools/context-capture.py`. Not authored by this seat.
- Working tree (uncommitted): `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `tools/context-capture.py`; untracked `.ufo/evidence/round-15/`, `.ufo/waves/round-15/`, `corpus/lessons/round-15.md`.
- Historical bytes: `git diff --quiet a9cf4da -- .ufo/evidence/round-14` exits 0. Round-12/13 evidence untouched in this audit's range.

## 4. Missing evidence (awaiting L1; not defects)

- No retained runs of `python3 tools/context-capture.py --selftest` or `--check`, so the "isolated self-invocation" and "frozen replay" claims are **declared, not observed**. Per the target, this is expected and not a defect.
- No retained census run for the round-15 `SOURCES.md` state.
- No retained negative-fixture run for `context-missing-env.json` under the new tool.
- S049 fixture behaviour under a live child process remains unproven, as the lesson itself states (l.19–20, l.30–31).

## 5. Out of scope / not done

- No sibling gates, no outside-lane reads of product code, no credential or `agent.db` access.
- No messages sent to TameshiR15; no implementation-critical defect was identified.
- Tool installs or updates: none.
- Read-only network access: one fetch of `https://docs.python.org/3/library/subprocess.html` (S049 check).
