seat: ConnPackageCross
(runtime id ConnPackageCross-2; w1, round 45, lane tameshi-shokunin; date 2026-10-25)

# Package x registry cross map (shokuknow merge/tameshi vs lane SOURCES.md)

## 1. Bounds compliance

- Contract read first: `.ufo/evidence/round-45/contract.json` (frozen; never edited). Tooling rules read: `/home/vgpnk/.omp/agent/RULES.md`.
- Lane checkout read-only except this report. Scratch only under `/tmp/tameshi-r45-ConnPackageCross/` (created).
- Read-only package `/home/vgpnk/Projects/shokuknow/merge/tameshi` opened read-only only; nothing written, no campaign tool run there.
- No tool installed/upgraded. No git/jj mutating command run.
- Leaf seat: no subagent dispatch.

## 2. Method

Parsed `corpus/SOURCES.md` (lane, 115 row ids) and `SOURCES.append.md` (package, 103 staged ids) with the same 11-column schema the round-45 counter uses (`ROW_RE = ^ {0,3}\|\s*(S\d{3,})\s*\|`, 13 split cells). URL normalization for comparison: lowercase host, drop leading `www.`, drop trailing `/` from path, keep query/fragment (`norm_url`). The 73-row C1 population was recomputed with the counter's own `measure.population()` (status `mined`, id <= S160, first http(s) URL present) → 73 rows confirmed.

## 3. (a) Staged rows citing a document the lane already holds

Same URL modulo scheme/www/trailing slash, staged source cell vs lane source cell:

| staged id | SOURCES.append.md line | lane id | SOURCES.md line | document |
|---|---|---|---|---|
| S153 | 7 | S105 | 117 | POSIX diff spec (pubs.opengroup.org/…/diff.html) |
| S154 | 8 | S106 | 118 | google/golden `golden.go` |
| S159 | 13 | S155 | 125 | PIT basic concepts |
| S160 | 14 | S156 | 126 | PIT FAQ |
| S196 | 50 | S152 | 122 | UFMG snapshot-testing thesis PDF |
| S209 | 63 | S107 | 119 | TensorFlow Federated golden_tests.md |
| S211 | 65 | S002 | 13 | stryker mutation-testing-report-schema.json |
| S212 | 66 | S026 | 37 | Google Testing Blog, Flaky Tests at Google (rendered page) |
| S216 | 70 | S026 | 37 | same post (per-post Atom/JSON record; source cell also names the rendered page) |

9 staged rows → 8 distinct lane rows. The same four URL pairs (S153→S105, S154→S106, S159→S155, S160→S156) are independently recorded in the freeze-time guard receipt `.ufo/evidence/round-45/assimilation/guard-map.json` (`"held"` / `"map_dedupe"`), so this list agrees with the round's own assimilation machinery.

No other staged row matches any population URL (all 73 population URLs checked; also checked arXiv `abs/pdf/html` same-article variants — none). The four amendments (`amendments/corpus/knowledge/golden-comparison-verdict.md`, `r3-snapshot-fixture-update-paths.md`, `r6-snapshot-practice-corpus.md`, `r8-golden-update-flag.md`) target files the lane already holds; they are appends, not new documents.

**Staging hazard (collision, not dedupe):** package staged ids S153–S160 collide with lane-held ids S153–S160 (lane added these rows in rounds 41–44 after the package was staged; e.g. package S153 = POSIX diff, lane S153 = Python `ast` docs). The guard receipt records this: `"collisions": ["S153"…"S160"]`, `"column0_collisions"` same, `"naive_map"` refused. The current round's adoption map only covers 10 staged ids (S153–S160 dedupe/renumber + S202/S203→S256/S257); the other 93 staged rows have no id assignment yet. Any later wholesale append must renumber S153–S255 before writing, otherwise `measure.parse_rows` (dict keyed by id, last-wins) would overwrite population rows S153–S160.

## 4. (b) Package themes vs frontier F1–F10 (new ground, ranked)

Theme = new package knowledge file (81 files, 80 not present in lane `corpus/knowledge/`). Support = number of distinct staged rows (S153+) referenced inside the file's `source:`/text (via `S\d{3,}` scan). Ranked by staged-row support:

| rank | frontier | status in lane README | new pkg knowledge files | distinct staged rows referencing | lead themes |
|---|---|---|---|---|---|
| 1 | F3 determinism/flaky-aware | open | 42 | 66 | repeat-control-measured-n3 (S172); run-identity normalisation/wider pattern (S186, S201); gtest order/seed + primer independence (S202/S203); width-sweep-and-race (S208); flaky clusters (S195); quarantine threshold (S241–S244) |
| 2 | F5 hermetic env | open | 29 | 40 | env-diff measured (S184, S188); run-identity reveals env sensitivity (S193); sibling-import staging (S233, S245/S246); exclusion port (S234); two-level import chain (S251) |
| 3 | F1 mutation-score semantics/interop | held | 20 | 33 | schema vocabulary (S211/S215); ledger-leg blockers (S179, S187, S191, S194, S213, S222, S227, S230); interop measured (S174) |
| 4 | F7 incremental re-sweep | open | 19 | 31 | cadence (S161/S162); prediction side (S205/S206); cost baseline (S207); false-red calibration (S212/S225/S229/S235); cadence+floor (S236); recheck-carrier fix (S232); ICST address (S252) |
| 5 | F9 LLM-era mutants | open | 4 | 9 | equivalence cost (S156/S165); CJK score semantics (S163–S165, S168); criteria cost (S200) |
| 6 | F10 PBT generators | open | 5 | 8 | generator-as-fixture (S157/S166); generator-craft (S170); QuickCheck primary correction (S182/S183); gtest generator contract (S204) |
| 7 | F8 oracle anchoring | open | 6 | 8 | survivor classification (S166); metamorphic oracle Chinese (S199); CJK suite effectiveness (S181); flaky clusters (S195); LLM-era criteria (S200) |
| 8 | F4 golden/snapshot | open | 6 | 6 | vendor verdict (S175); write-path audit (S185, S189); published study (S198); update-flag (S209/S210); thesis corpus (S196) |
| 9 | F2 witness-scoped kill | held | 4 | 6 | witness-scope counted (S218); gtest primer independence (S203); gtest order/seed (S202); schema killedBy (S211) |
| 10 | F6 fixture minimization | open | 4 | 4 | delta-debugging contract (S167); IEICE access route (S177, S192); IEICE abstraction authority (S197) |

New ground *outside* F1–F10: `r16-trajectory-evaluation-in-the-chinese-tradition.md`, `r16-process-level-agent-evaluation-in-japanese.md`, `r16-step-level-verification-in-english.md` (staged S253–S255) — meta-level agent/process evaluation; they reference F3/F5 in scope but their core content is not any F1–F10 ground. Candidates for a future (unlisted) frontier.

Cross-check with the merge report: `MERGE-REPORT.md` lines 23–112 list the same 80 new files with titles/notes; the per-frontier count above was computed by scanning the files themselves.

## 5. (c) C1 population rows the package re-opened (same URL), quote agreement

8 of the 73 population rows have a staged row citing the identical URL. Quote agreement = staged teaches/anchor claim vs lane anchor/teaches claim, compared on content (error `measure.words()` shared content words between staged scope+anchor+teaches and lane scope+anchor+teaches):

| population row | staged re-open(s) | shared content words | agreement |
|---|---|---|---|
| S002 | S211 | 11 | AGREE — staged adds schema version/thresholds and `killedBy`-as-witness (F2 expressibility); lane teaches the same status enum/export shape |
| S026 | S212, S216 | 13 / 6 | AGREE — staged quotes “about 84% of the transitions…” and the 1.5% base rate; lane teaches both numbers |
| S105 | S153 | 23 | AGREE — same three outcomes 0/1/>1; staged adds LANG/LC_ALL/TZ environment effect (F5) |
| S106 | S154 | 25 | AGREE — same `-update_golden` flag behind write path; staged adds “rather than a silent rewrite” |
| S107 | S209 | 16 | AGREE — same `--update_goldens` + diff review; staged adds the exact `--test_arg=--update_goldens --test_strategy=local` invocation |
| S152 | S196 | 6 | AGREE — lane: fragility/lack of context → false positives; staged: 569-project study, dominant drawbacks + negative mutation-tool results |
| S155 | S159 | 13 | AGREE — lane: seven outcomes, No coverage vs Survived distinction; staged: “no coverage” and “survived” are different outcomes → denominator choice |
| S156 | S160 | 13 | AGREE — both: timeouts + static initializers make verdicts run-dependent; a mutant may time out on one run and die/survive on another |

All 8 re-opened population rows have staged quotes that agree with the lane's anchor — none contradicts. Caveat: package rows were opened 2026-10-23/24 (< the round's `opened >= 2026-10-25`), so these re-openings are **not** C1 verifications; they are validated quote candidates and URL-confirmed first targets for the sweep.

**Verified live-check (Google Blog, S026):** `curl -fsSL 'https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html'` → 236 374 bytes; the post body appears twice — inside a `<script type='text/template'>` block (bytes ~32284–38488) and again in the rendered body. After the counter's `extract()` (strip script/style, strip tags, unescape, fold), normalized text still contains “We define a “flaky” test result” and “about 84% of the transitions we observe from pass to fail involve a flaky test” and “hardly a perfect solution” (output: `'…' in normalized live page: True`). So the package's claim (S216/r10-blog-carrier-reachability.md) that the corpus checker “cannot reach a single one” of the sentences does **not** hold for the round-45 freshness counter — S026 is verifiable against the live rendered page today. The package's carrier fix (Atom/JSON feed) remains the safer long-term recheck address, but it is not required for C1.

## 6. Proposed move (one bounded proposal)

**Freshness-focused, cross-package synthesis:** seed the C1 sweep with the 8 package-re-opened population rows and reuse one snapshot blob across URL-shared rows.

- Which rows: S002, S026, S105, S106, S107, S152, S155, S156 (each already has a package-validated quote). Fetch each row's *own* URL on/after 2026-10-25, commit the snapshot under `.ufo/evidence/round-45/freshness/sources/`, and write ledger entries whose quotes are taken fresh from that snapshot (not from the package anchor cells — verbatim copying of the row's own cells is rejected as `quote copied from row`).
- Snapshot reuse: 7 population URL groups share one normalized URL (S028/S081 bazel test-encyclopedia; S041/S047/S048 pitest incremental-analysis; S060/S075 strace; S061/S076 jj-vcs; S068/S077 PR_SET_CHILD_SUBREAPER; S072/S078 open.2; S089/S160 Stryker equivalent-mutants). One fetch per group + per-row quotes → 73 rows at fewer fetches, still 1 entry per row as required.
- Non-harm: touches only the freshness axis; coverage (C2) is untouched. It does not modify the contract, counters, or guard map.

Risks:
- Package staged quotes are anchor-adjacent; a quote identical to the row's anchor/teaches text is rejected. Mitigation: quotes must be located afresh from the snapshot and checked with `measure.py --check` per row before commit.
- `S160` is in two URL groups simultaneously (also the round-44 monitor row); it counts once in the population (confirmed 73), so no double-count risk, but its entry must name the exact first URL from its source cell (Stryker equivalent-mutants URL).
- The 93 unmapped staged rows are out of scope for this round; no adoption action is proposed here.

Verification (for main agent / later waves):
1. `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev <deciding rev>` after the seed entries are in → expect `verified` to include the 8 rows and `fresh >= 50` target unchanged.
2. `python3 .ufo/evidence/round-45/freshness/measure.py --check .ufo/evidence/round-45/freshness/ledger.json --lane LANE --rev <rev>` style per-entry `--check` on each seeded fragment (or the wave's own check) → each of the 8 outputs `verified`.
3. Re-run the URL-group enumeration (script in scratch) to confirm 7 shared-URL groups unchanged from base.

## 7. Evidence commands (selected outputs)

- `python3 -c "… measure.population(parse_rows(open('corpus/SOURCES.md').read())) …"` → `Total population rows: 73`.
- Normalized-URL scan: `Total matches between staged and lane: 9` (table in §3).
- Guard receipt: `.ufo/evidence/round-45/assimilation/guard-map.json` → `verdict=admitted`, `collisions=[S153…S160]`, `held={S153:S105,S154:S106,S159:S155,S160:S156}`, `registry_max=S160`, `staged_max=S255`, `map_entries=10`.
- Live-page quote check (S026): see §5 output lines.

## 8. Notes

- No new tool installed; no counter run executed (returns bounds: seats run counters only as `--selftest`/`--check`/`--extract` or against `--rev 3310e7be…`/`5891bdb…`; this seat ran none).
- All file:line references above are to the frozen/current lane worktree and the read-only package; no lane file was edited.
