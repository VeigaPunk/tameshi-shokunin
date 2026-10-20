# Frontier — SOURCES census and sourced-claim obligations checklist (round 15, w1)

Seat: `TameshiR15.Frontier` (leaf, report-only). Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scope: census state of `corpus/SOURCES.md`, sourced-claim obligations for C1, and missing pointers for L1.
Basis: files as read during this seat, not predicted outcomes. Snapshot digests are in §7.

## 0. Summary

- The registry is at 48 rows and already contains the round-14 rows S049 and S050. No new row exists in round 15 yet. Next unused id is S051.
- Round-15 mutable-field work on S049 is applied: `used-by` now also lists `corpus/lessons/round-15.md`. Its status and recheck are unchanged.
- The round-15 search-log entry for the S049 re-open is present in `corpus/SOURCES.md`.
- QUALITY criterion 17, which the round-15 lesson cites, is present in `corpus/QUALITY.md`.
- Open pointers for L1 (§6): no `tools/context-capture.py`; no round-15 census before/after artifact; `claims.json` carries no `S###` pointer; no S051 decision recorded; no SKILL.md registry row for the new gate; the 64 mapping is not yet explicit.
- The census validator does not enforce several contract rules. L1 must check those by hand (§4).
- I executed no census, validator, selftest, gate, or network fetch. Read-only file reads, `grep`, and `sha256sum`/`wc` only.

## 1. Census evidence (read from the files)

Registry rows in `corpus/SOURCES.md` (lines 12–59), counted against the ids listed:

| Measure | Value | Basis |
|---|---|---|
| Rows | 48 | ids S001–S037 (37) and S040–S050 (11); S038–S039 retired, never written (`## Id allocation`) |
| Tier A / B / C | 41 / 5 / 2 | B: S012, S024, S030, S040, S045. C: S029, S046 |
| Status mined / queued / rejected | 21 / 24 / 3 | mined: S001–S006, S011, S026, S028, S031–S037, S041, S047–S050. rejected: S029, S030, S046 |
| Own-work rows | S031 (lane harness), S032–S037 (fleet gates, read-only), S050 (lane gate) | `kind` column |
| Next unused id | S051 | last line of `## Id allocation` |
| Search-log entries this round | `2026-10-20 — round-15 explicit child invocation` (S049 re-open, identified 1 / screened 1 / included 1 / excluded 0) | `## Search log` |

S049 row, as read (line 58): `status mined`, `opened 2026-10-20`, `recheck on-release`, `used-by corpus/lessons/round-14.md, corpus/knowledge/incremental-pin-disposition.md, corpus/lessons/round-15.md`.
S050 row, as read (line 59): own-work, tier A, `mined`, `opened 2026-10-20`, `recheck on-release`, `used-by corpus/lessons/round-14.md`. Anchor: `docstring lines10–13 and CLI r14 at measured commit6431478`.

Validator facts (`scripts/sources-census.sh`, 806 lines, read only):

- Command the lane uses: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`. Last recorded output (round-14 closure note; not re-run here): `tameshi W04 S047 …`, `tameshi W04 S048 …`, `tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, exit 0. W04 comes from the S047/S048 correction rows that share the PIT URL with S041. These are disclosed warnings, not errors.
- Exit map (script header, lines 16–18): 0 clean or warnings · 1 E/overdue findings · 2 usage or missing registry · 3 selftest failure.
- Selftest fixtures exist at `scripts/fixtures/sources-census/` (root, a-, b-, c-, z-shokunin, injection-shokunin).

## 2. Sourced-claim obligations (what the lane must show)

Each obligation is grounded in the file named. Status is what the files show now.

| # | Obligation | Source | Status (as read) |
|---|---|---|---|
| O1 | A new row is written only after the source is opened in the round that writes it; the round lesson `## Gate` records URL, access date, and a ≤25-word quote with location | `SOURCES-CONTRACT-v1.md` rule 1 (`.ufo/waves/kaika/`); `CORPUS.md` §SOURCES.md | S049 re-open recorded in `corpus/lessons/round-15.md` `## Gate` (URL, 2026-10-20, 19-word quote). No new row, so nothing else owed |
| O2 | Append-only. Only `status`, `recheck`, `used-by` change in place; each change logged old→new in the round lesson | contract rule 2 | S049 `used-by` change logged in round-15 lesson `## Gate` (old list → old list plus `corpus/lessons/round-15.md`). Matches the row as read |
| O3 | A correction is a new row whose `teaches` opens `supersedes S0NN —` | contract rule 2 | No correction row this round |
| O4 | Search-log entry per bounded search, with identified / screened / included / excluded and stop rationale | contract rule 5; `PROTOCOL.md` frontier step | Present (round-15 entry in `## Search log`) |
| O5 | Expansion counts admitted `knowledge/` entries citing a `mined` row, not row count | contract rule 4; `LEARNING.md` expansion | No new knowledge entry this round; expansion claim must stay unchanged |
| O6 | A new `knowledge/` entry opens with `source:`, `verified-at:`, `recheck:`; an external source enters through an opened SOURCES row; tier-C never sole support | `QUALITY.md` criterion 10 | No new knowledge entry; nothing owed |
| O7 | Frontier step: curate SOURCES (opened rows only), record census before→after, mine ≥1 mistake into `corpus/lessons/round-<N>.md` `## Mistakes` (class · evidence · captured-by · fix), file ≥1 claim as *sourced* with an `S###` citation | `PROTOCOL.md` lines 138–145 | Mistakes: present (2 rows in round-15 lesson). Sourced claim: the lesson names S049 in prose; `claims.json` cites no `S###` (P3). Census before→after: not yet recorded (P5) |
| O8 | Report `## Sources & frontier` section: rows before→after with counting command, rows added by tier, rows touched old→new, frontier rows advanced; `SOURCES: unchanged — <reason>` if no change | `PROTOCOL.md` lines 156–162; `PROTOCOL-APPENDIX.md` "Sources & frontier" | Not yet in any round-15 report. Inputs in §5 |
| O9 | Mined rows' `used-by` paths must exist | census `usedby_findings` (script lines 538–571; checks only `status == mined`) | Not checked by this seat. L1 runs the validator once after integration |
| O10 | Own-work rows are the lane's re-runnable gate output, tier A allowed, anchored by path @ commit (+ sha256) | contract `tier`/`anchor`; `CORPUS.md`; S050 precedent | No own-work row for the new tool yet (P4) |
| O11 | A gate is registered in its own `SKILL.md` registry with: name, `gate|probe`, entry command, verdict map (code→class), self-test command, pinned values, write scope, owner. Undeclared nonzero code = could-not-evaluate | `PROTOCOL.md` "Gate standard" lines 375–403 | Round-14 rows in `SKILL.md` lines 1597–1602 still show the context capture as `probe` with no standalone selftest, and the disposition row maps `64` as "usage". Round-15 registry row not yet appended (P6) |
| O12 | A gate's self-test runs in an isolated temp tree, asserts the exit code and a stable finding ID, with expected values committed in the owning repo | `PROTOCOL.md` "Gate standard" lines 385–389; `QUALITY.md` criterion 17 | The historical `capture-context.py` has no `selftest` or `argparse` match (grep); its CLI returns 64 on unexpected arguments (lines 608–613). New tool not yet present |

## 3. Round-15 lesson as read

`corpus/lessons/round-15.md` (sha256 in §7) already has:

- `## Gate`: S049 re-open with URL, date, quote, bounded search counts, and the S049 used-by change.
- An explicit statement that new own-work sources are recorded only after the tool exists and is opened: "no row is promised in advance."
- `## Mistakes`: two rows (gate-misclassification; exit-class-ambiguity) with class, evidence pointer, captured-by, and fix. Both name QUALITY17, which is present at `corpus/QUALITY.md` lines 75–80.

## 4. Census validator limits L1 must cover by hand

The validator (`scripts/sources-census.sh`) does not check these. Each is a manual step for L1.

1. Contract rule 1 (Gate entry for each new row: URL, date, ≤25-word quote). Not checked.
2. Contract rule 2 (append-only; only `status`/`recheck`/`used-by` may change). Not checked. Needs a diff of `corpus/SOURCES.md` against the round baseline `a9cf4da78f2514c7bedd91a850a88590009d7df0` (from the round-15 lesson header).
3. E04 exemption is substring-based: `teaches !~ /supersedes S[0-9]{3}/` (script ~line 648). It accepts the phrase anywhere in `teaches`, does not require it to open the cell as contract rule 2 says, and does not check that the named id exists.
4. E09 accepts any alphabetic token as a symbolic recheck (script line 665: `^[A-Za-z][A-Za-z0-9 _-]*$`). Contract lists `90d`, `180d`, `on-release`, or an ISO date. The selftest itself accepts `annual` (script line 149).
5. E11 checks used-by paths only for `status == mined` (script lines 559, 566). Queued or rejected `used-by` cells are not checked.
6. `Next unused id: S051` and the `## Id allocation` bullets are prose, not parsed. An id can be allocated in prose and absent from the table, or the reverse.
7. Overdue uses `--today` defaulting to `date -u`. For reproducibility pass `--today` explicitly, as the selftest does.
8. No overdue row exists for the current window. 90d rows opened 2026-10-19 come due 2027-01-17; those opened 2026-10-20 (S047, S048, S049 if 90d) come due 2027-01-18. 180d rows opened 2026-10-19 come due 2027-04-17. S049 and S050 are `on-release` and are reported, never judged overdue.

## 5. Inputs for the report's `## Sources & frontier` section (pre-round values, from current files)

- Command: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (L1 to run once after integration; not run here).
- Rows before: 48. Rows after: 48 unless L1 allocates S051 (P4).
- Tiers (before = after unless S051 is added): A 41 · B 5 · C 2.
- Status (before = after unless S051 is added): mined 21 · queued 24 · rejected 3.
- Rows touched old→new: S049 `used-by` gains `corpus/lessons/round-15.md` (already in the file; logged in round-15 lesson `## Gate`). No other row cell change is visible in the reads.
- Frontier rows advanced: none. C1 is a calibration capability; PROVINCE.md:40–42 requires an admitted `knowledge/` entry with a `source:` header citing a `mined` row before any F-row moves. No such entry exists this round.
- Mistakes mined: 2 (round-15 lesson `## Mistakes`).

## 6. Missing pointers for L1 (exact, bounded)

| ID | Missing or unresolved pointer | Where it is required | Bounded action for L1 |
|---|---|---|---|
| P1 | `tools/context-capture.py` does not exist. `tools/` holds `bash-witness-study.py`, `evidence-disposition.py`, `mutate-and-run.sh`, `pin-disposition.py`, `repeat-control.py`, `witness-metadata.py` | spec1.json integration interface; round-15 lesson | Gate executor creates it; L1 pins its sha256 after landing. Historical `.ufo/evidence/round-14/capture-context.py` stays byte-identical (sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, 647 lines, matching `tool_sha256` in the round-14 receipts) |
| P2 | No round-15 census before/after artifact. `.ufo/evidence/round-15/` holds only `claims.json` | PROTOCOL.md frontier step; round-14 precedent (`sources-before.json`, `sources-after.json`) | L1 writes `.ufo/evidence/round-15/sources-before.json` and `sources-after.json` from the census output, or states the counts in the report |
| P3 | `claims.json` C1 entry has no `S###` citation and no sourced marker | PROTOCOL.md lines 138–142 ("files at least one claim … as *sourced* — its evidence citing an `S###` row") | Add a `sources` field to C1 naming `S049` (and `S051` if P4 creates it). Keep existing fields unchanged |
| P4 | S051 is unallocated and no decision is recorded. Spec says "Cite round15 lesson S051 once present"; round-15 lesson says no row is promised in advance | contract id rules; round-15 lesson `## Gate` | Single owner (L1) decides before the gate lands. Either (a) allocate S051 as own-work after `tools/context-capture.py` is committed: `anchor` = path @ landed commit + sha256 (S050 pattern), tier A, `status mined`, `used-by corpus/lessons/round-15.md`, `recheck on-release`, plus a round-15 `## Gate` entry with a ≤25-word quote from the tool's own docstring; or (b) state "no new row" in the report and cite no S051 anywhere. Update `## Id allocation` and "Next unused id" in the same edit if (a) |
| P5 | Round-15 census before→after not recorded in lesson or report | PROTOCOL.md lines 138–139, 156–157 | Record §5 values, with the counting command and result, in the report `## Sources & frontier` |
| P6 | `SKILL.md` has no round-15 registry row for the context gate. Existing round-14 row (`SKILL.md` ~line 1602) names the instrument `probe` with "no standalone selftest"; disposition row (~line 1601) maps `64` as "usage" | PROTOCOL.md "Gate standard" lines 380–403; round-15 lesson `## Mistakes` exit-class-ambiguity | Append a round-15 gate/probe registry section (append-only; keep round-14 rows). Row fields: name, `gate`, entry command `python3 tools/context-capture.py …`, verdict map with `64 could-not-evaluate` named explicitly, self-test command `python3 tools/context-capture.py --selftest`, pinned values, write scope, owner `tameshi`. Keep `64` explicit in the disposition row too, or mark it superseded |
| P7 | `corpus/SOURCES.md` line 4 says `Contract: SOURCES-CONTRACT-v1.md`, a bare name that does not resolve from `corpus/`. The frozen contract lives at `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` and is also carried in full in fleet `CORPUS.md` §SOURCES.md | `RegistryReview` R6 (round 12); `CORPUS.md` lines 64–67 | Optional, prose only, not a row: replace the bare name with `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` or `CORPUS.md` §SOURCES.md. Do not edit any table row |
| P8 | Historical `corpus/SOURCES.md` and `corpus/QUALITY.md` changed during this seat's reads | — | L1 pins digests at its own read time (§7). A drift record, not a defect |

## 7. Snapshot digests and counts (as read by this seat)

| File | sha256 | Size / lines |
|---|---|---|
| `corpus/SOURCES.md` | `daa83a3f1219c382c14254e4b103cf32dd97d9671e0a167f960dda3f1144ca56` | 170 lines (an earlier read ended near line 165; a later read showed the round-15 search-log entry and the S049 `used-by` change) |
| `corpus/QUALITY.md` | `534f42f51b16f64e1ee672daac55557b721478c59f1ccfa0e9cf956e1a02a68d` | criterion 17 at lines 75–80 |
| `corpus/lessons/round-15.md` | `e8448ab21071617ec7ce285da4905b7ac15908cffb2b50b67651d21089095ffc` | Gate, Mistakes, dispatch sections |
| `.ufo/evidence/round-14/capture-context.py` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | 647 lines (historical, unchanged) |
| `tools/evidence-disposition.py` | `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95` | matches the checker pin recorded in the round-14 lesson |
| `scripts/sources-census.sh` (fleet) | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` | 806 lines |

Not computed by this seat: `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` digest; `.ufo/evidence/round-15/claims.json` digest.

## 8. Bounded recommendations (L1)

1. Keep S049 as is. Its `used-by` change is logged and matches the file. Do not change its status or recheck.
2. Decide S051 once, as sole allocator (P4). Prefer (b) "no new row" if the existing S049/S050 rows and the lesson already cover the tool's claim; choose (a) only after the tool is committed and its digest is pinned.
3. Add the `sources` pointer to `claims.json` C1 (P3). Do not change any other claim field.
4. Write the round-15 census before/after artifact and the report `## Sources & frontier` from §5 (P2, P5). Run the validator once after integration; expect no E-codes. Compare the W04 pair against the round-14 closure record.
5. Append the SKILL.md round-15 registry row and make the `64` class explicit (P6). Keep historical round-14 rows.
6. Optional prose fix for the SOURCES.md line 4 pointer (P7). No row edits.
7. Diff `corpus/SOURCES.md` against baseline `a9cf4da78f2514c7bedd91a850a88590009d7df0` after integration. The only allowed changes are: S049 `used-by` (already present), the round-15 search-log entry (present), an optional S051 row with its lesson entry (only under option a), and the `Next unused id` line if S051 is used.
8. Do not rewrite historical round-12 to round-14 evidence, the historical `capture-context.py`, or the round-14 checker.

## 9. Not done by this seat

- No census, validator, selftest, gate, or build run.
- No network fetch of S049 or any other URL.
- No git subcommands, no sibling gate runs.
- No reads of `~/.omp/agent/agent.db*`, credential or auth files, or omp CLI.
- No edits outside this report.

## 10. Tool installs and updates

None. Tool installs/updates: none.

## 11. Authority

Advisory, lane-internal, leaf seat. This report is not an independent admission sample and does not replace the separate non-author closure duty.
