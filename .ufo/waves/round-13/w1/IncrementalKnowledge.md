# IncrementalKnowledge — F7: pin match is not a reuse licence

## Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md` — new, 311 lines / 22,089 B, sha256 `395ee0122166ad700a104d97d19e8ddebffd3bbaee582e6cf784d227d9d0fe75`. No other doc was edited by this seat; `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md` and `corpus/lessons/round-13.md` are L1's concurrent writes, not mine.

## What the entry establishes (bounded)

- Header satisfies QUALITY 10: `source:`, `verified-at:`, `recheck:`, `ground:`.
- §1 quotes S003 and S041 verbatim, and attributes the item-4/item-5 correction to **S047** (same URL and same fetched bytes as S041; correction, not a new fetch).
- §2 states both tools' reuse predicate (unchanged mutant + unchanged killing/covering tests), their declared detection gaps, and that neither discusses a content hash or gate pin.
- §3 is the core method: the lane's pin covers one blob path, one revision, one sha256 (`tools/mutate-and-run.sh:81-83, 540-553`); it carries no mutant inventory, test identity, covering relation or dependency closure. `result_reuse: not_established` is labeled a **lane inference** from the dependency/environment blind spots, not a source sentence. A replay is an execution, not reuse; byte hashes also exclude file mode.
- §4 gives the six-leg table from own-work S031 and separates a **content disposition** (read-only classification) from a **fresh re-sweep** (execution with pre-registered spec, control, restore, new row). No new kill-rate, no seventh case; the ER-4 2026-10-14 reading is cited as historical receipt only.
- §5 maps the source-named blind spots; §5a records measured unpinned inputs for three legs from read-only reads.
- §6 points to the eventual `.ufo/evidence/round-13/pin-dispositions.json` and claims none of its contents; it lists the invariants a reader applies, including `observed_at` and per-repo HEAD so a row cannot go stale silently, and a freshness falsifier (re-pinning or appending a ledger row at a new HEAD without an executed control/spec/table at that revision).
- §7 withholds cross-lane generality (PROVINCE two-lane rule), leaves F7 status to L1, records the same-byte identity across the 2026-10-19/20 accesses (via `sources-opened.tsv:4,:33`) and the remaining page-version unknown.

## Source quotes for L1 Gate and SOURCES source-cell mining

Fetch facts (this seat, 2026-10-20T04:46:12Z): S003 sha256
`9054e311a0569231aa2a1427a4137729c8180d7f2687dfd450322e855cc9ad90` (33,898 B);
S041/S047 sha256 `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db` (8,892 B).

**S003 §Incremental mode** (each phrase verified present once in the raw page):

> Reuse is possible when: A mutant was "Killed"; the culprit test still exists, and it didn't change. A mutant was not "Killed"; no new test covers it, and no tests changed.

> StrykerJS will do a git-like diff of your code and test files to the previous version it finds in the incremental report file in order to match the mutants and tests to the current version of the code.

> The dry run remains required; as it discovers tests, mutation coverage per test, and ensures Stryker runs successfully when no mutant is active.

**S003 §Limitations:**

> Stryker will not detect any changes you've made in files other than mutated files and test files.

> Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies, changes to environment variables, changes to .snap files, readme files, etc.

> Static mutants don't have test coverage; thus, Stryker won't detect test changes for them.

Runner-support table: "All test details are unknown incremental mode will only detect changes in mutants, not their tests." (page wording as printed). `--force` reruns "all mutants in scope, regardless of the incremental file."

**S041/S047 §Incremental analysis:**

> PIT will track changes to the code and tests and store the results from previous runs. It will then use this information to avoid re-running analysis when the results can be logically inferred.

> With the exception of 4), all these optimisations introduce a degree of potential error into the analysis.

> The main issue is that class behaviour is defined not only by its bytecode, but also by its dependencies (i.e the classes it interacts with and the graph of classes that they interact with). PIT will only consider the strongest of these dependencies - changes to super classes and outer classes, when deciding if a class's behaviour might have changed.

> So the incremental feature is based on the assumption that it will be relatively rare for changes in the dependencies of a class to change the status of a mutation. Although this assumption seems reasonable, it is currently unproven.

Item 4: "it should therefore be prioritised above others. (since 1.14.4)". Item 5: "(not yet implemented)".

**Suggested source-cell treatment (advisory):** S047 already carries the precision wording — "the dependency assumption is unproven; item 4 prioritises an old killing test, while proposed item 5 is not yet implemented; the potential-error sentence covers optimisations, not only live result-reuse skips". Two wording cautions for any future cell: the source's "it" in item 4 is ambiguous, so keep the verbatim "it should therefore be prioritised above others" and a neutral gloss ("a prioritisation, not a reuse skip") instead of naming a referent; and "reuse optimisation" is the registry's term — the page says "all these optimisations". S041's original row stays as written; do not rewrite the `teaches` cell. S003's row already names env/dependencies/`.snap`; the one refinement available is that its reuse predicate is about mutated and test files, not about a tool-content pin. The header's `recheck: 90d` is the tighter of the two registry cadences (S003 180d, S041/S047 90d); it is a reader-side choice, not a registry rewrite.

## Observed at write (read-only, no gate executed)

- `corpus/SOURCES.md`: S003, S041 and S047 all read `mined`; `used-by` contains `corpus/knowledge/incremental-pin-disposition.md` 3 times; S047 exists at row 56; search log already has the 2026-10-20 F7 bounded re-open; id allocation notes S048 as next.
- `tools/mutate-and-run.sh` sha256 is still `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, so S031's anchor holds.
- `.ufo/evidence/round-13/pin-manifest.json` has schema `pin-manifest-v1` and 6 legs; its `expected_sha256` and `pinned_commit` values equal the runner's `PIN_*`/`REV_*` pairs for all six (checked by script: `ALL_MATCH True`). This corroborates §4's table; it is not a disposition receipt.
- **Digest identity is established, not just today's access.** `.ufo/evidence/kaika-round-1/sources-opened.tsv:4` records S003 `9054e311…` at 2026-10-19T21:43:50Z and `:33` records S041 `e9cbc3e1…` at 2026-10-19T21:47:33Z — both equal this re-open's digests. §7 was corrected accordingly; only the page *version* remains unknown.
- Sibling anchors used in §5a were re-read at their pinned revisions and match (surface-census `:82-83, 817-823, 710, 789-790`; checklist-run `:65, 416, 438-439`; claims-check `:82-93, 582-583, 600`; round-10 record `:84-88`).
- A peer's line "claims-check depends on `$UFO_SRC`/homedir" is true for CLI mode but **not** for the leg: the source says the default is resolved lazily and "never in `--selftest`" (`claims-check.mjs:82-93`). §5a records only interpreter and tmpdir for that leg.

## Review incorporation (KnowledgeSupport, read-only)

Applied after the first draft: (1) replaced the false "no opening digest" claim with the `sources-opened.tsv:4,:33` same-digest recheck; (2) narrowed the PIT predicate to per-rule units (rule 1 class, rule 2 class + killing test, rule 3 covering tests); (3) replaced the inferred `--force` rationale with the page's own quote and an explicit [I] marker; (4) neutralized item 4 to "a prioritisation, not a reuse skip" with the verbatim "it should therefore be prioritised above others", since the pronoun is ambiguous; (5) dropped "identical bytes" from the round-10 mode record (the source says only that the materialized blob lacked the exec bit); (6) marked the PATH case-set deduction [I]; (7) marked "a `current` reading is not a re-sweep request" [I] and cited the three ER-3 triggers at `fleet-kill-rate-ledger.md:306-310` (trigger 1 after hardening is present).

KnowledgeSupport's final read confirmed all seven corrections, the 311-line/22,089-B/`395ee012…` state, and withdrew the quote-mark point (the served HTML uses `"Killed"`). Residual wording outside this seat's scope: `corpus/SOURCES.md:56` (S047 teaches, "prioritises an old killing test") and `corpus/lessons/round-13.md:12` ("prioritises tests") still name a referent the source leaves ambiguous; lesson line 40 says "all but one item a reuse optimisation" where the page says "all these optimisations". Main owns SOURCES; L1 owns the lesson. Neither was edited here.

## Exact checks L1 should run (not executed by this seat)

1. **Header (QUALITY 10):** `head -4 corpus/knowledge/incremental-pin-disposition.md | grep -cE '^(source|verified-at|recheck|ground):'` → `4`.
2. **Source identity (two dates):** `curl -fsSL https://stryker-mutator.io/docs/stryker-js/incremental/ | sha256sum` → `9054e311…cc9ad90`; `curl -fsSL https://pitest.org/quickstart/incremental_analysis/ | sha256sum` → `e9cbc3e1…590db`. Compare both with `.ufo/evidence/kaika-round-1/sources-opened.tsv:4` (S003, 2026-10-19T21:43:50Z) and `:33` (S041, 2026-10-19T21:47:33Z); the four values must agree, establishing same-byte access across the two dates. A mismatch means re-read quotes before admitting.
3. **Quote presence (raw page, one each):** for S003 `grep -Fc` on `'Reuse is possible when'`, `'The dry run remains required'`, `'files other than mutated files and test files'`, `'Any other changes to your environment are not detected'`, `'all mutants in scope, regardless of'`; for S041 `'avoid re-running analysis when the results can be logically inferred'`, `'With the exception of 4)'`, `'prioritised above others'`, `'class behaviour is defined not only by its bytecode'`, `'it is currently'`, `'not yet implemented'`. All were 1 against this fetch.
4. **Pin table equality:** `grep -E '^(PIN|REV)_(JS|BASH|TSUKUROI|MADO|CHECKLIST|CLAIMS)=' tools/mutate-and-run.sh` → 12 lines; compare each to the §4 row. `sha256sum tools/mutate-and-run.sh` → `75ed934d…`.
5. **Manifest cross-check:** parse `.ufo/evidence/round-13/pin-manifest.json`; assert 6 legs, distinct names, and `expected_sha256`/`pinned_commit` equal to the 12 runner values (this read returned all true).
6. **Receipt gate once PinProbe lands:** `.ufo/evidence/round-13/pin-dispositions.json` must parse, contain exactly six rows for the §4 legs, carry each recorded pin equal to `PIN_*`, separate committed blob from worktree content, mark missing inputs `unavailable`, and show `result_reuse: not_established` on every row with no row claiming established reuse. It must also carry `observed_at` (UTC) and each repo's HEAD commit; check those are present and that a row's HEAD matches at read time. If the tool's schema names differ, apply these invariants to its documented fields; reject a five-row, duplicate-leg or untimestamped receipt.
7. **Freshness gate:** confirm no disposition was converted into a rate. A refreshed `PIN_*`/`REV_*` or a new ledger row at a HEAD sha is a re-pin claim, admissible only with an executed control, pre-registered spec and table at that revision. A `changed` row is ER-3 trigger T3 (request a re-sweep), not a successor measurement.
8. **Frontier/coverage:** `grep -n '| F7 |' corpus/README.md` — decide the status and next move for the bounded claim actually made (content dispositions + a constant reuse field), not for incremental execution generally. Add/confirm the coverage row per QUALITY 7.
9. **Anchor spot-checks (read-only `git show`, no execution):** `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show fecee874:corpus/surface-census.sh | sed -n '82,83p;817,823p'`; `… fecee874:corpus/checklist-run.sh | sed -n '65p;416p;438,439p'`; `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 175de6ba:scripts/claims-check.mjs | sed -n '82,93p;600p'`.
10. **No collateral edits:** `git status --short` — this seat wrote only the knowledge file and this report. `SOURCES.md` must remain L1's own write; README/QUALITY/SKILL/lessons/LOG untouched by this seat.

## Risks and blockers

- **Receipt name/schema may differ.** §6 points to `pin-dispositions.json` as the planner's declared output; PinProbe's actual filename and field names were still landing. Reconcile the pointer before citing; the invariants are schema-agnostic.
- **Mode is outside a content status.** §5a records a measured round-10 SETUP when the materialized copy at the pin lacked the exec bit. If the probe reports only sha256 content status, it cannot cover mode; that is a declared omitted input, not a silent pass. L1 decides whether the schema must surface mode.
- **Identity established; version not.** The 2026-10-19 opening digests in `sources-opened.tsv:4,:33` equal this 2026-10-20 re-open's, so same-byte access is verified. The unknown is the page *version* (S003 "since Stryker 6.2"; S041/S047 no version). Do not overwrite the opening anchor; the entry cites the evidence row.
- **Freshness can masquerade as progress.** A peer read during this wave reported kimi, tsukuroi and mado content-changed and the mado HEAD moving mid-wave. That read is data, not this entry's claim; it is why §6 now requires `observed_at` and per-repo HEAD. An untimestamped receipt, or a re-pin presented as a new result, is the failure mode to reject.
- **No generality.** Two vendor docs are not two independent lanes; PROVINCE's two-lane admission rule is not met. F7 status and any Core movement are L1's call.
- **No blocker.** No gate, test, lint, formatter, build or sibling command was executed; no tool was installed or upgraded, so the tooling directive has nothing to record.
