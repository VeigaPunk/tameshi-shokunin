seat: RevGuardMap

# By-document adoption id map review (C2: S202→S256, S203→S257)

Scope: `.ufo/evidence/round-45/assimilation/adoption-map.json` + `guard-map.json` (verdict admitted) + the two refused maps; staged rows S202/S203 in the read-only package; registry/staged id sets; the 8 collisions and held dedupes; the CORPUS.md id rule. All lane reads at the working tree; registry bytes also checked at freeze `3310e7be803516ca5934b4e949d91bcec824b179`. Scratch: `/tmp/tameshi-r45-RevGuardMap/`. No tool installs (operator rule 2026-10-19: nothing installed; preexisting python3/git/coreutils only).

## F1 — Staged S202/S203 are exactly the two claimed GoogleTest documents at cd8e73f — CONFIRMED

`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:56-57` (read `:raw:56-57`):

- S202 source cell: `Advanced GoogleTest Topics (googletest docs/advanced.md …) — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/advanced.md` — exact path, exact 40-hex pin.
- S203 source cell: `GoogleTest Primer (googletest docs/primer.md …) — https://raw.githubusercontent.com/google/googletest/cd8e73f067129f8489e35c7b51c7a68552b289d2/docs/primer.md` — exact path, exact pin.

Snapshot cross-check: S202 declares the pin's bytes as sha256 `05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2`; the committed snapshot hashes to exactly that:

```
sha256sum .ufo/evidence/round-45/coverage/sources/googletest-{advanced,primer}.md
05546ed6db9221444a77702a9519b0f7e289cf8b281a7dcedcce893a2840d1c2  googletest-advanced.md
03d756ab11521933cb59ef9bc081e7524e79c2dfbea496f6583ec166f819c26e  googletest-primer.md
```
Worktree snapshots are byte-identical to the freeze rev (`git show 3310e7b:… | sha256sum` matches for both). The staged S202 anchor names commit cd8e73f… as `main` head; S203 documents the `gtest_for_dummies.md` → `primer.md` rename with the upstream commit `de47b0d30c1d`.

## F2 — Neither document is already held by any lane row — CONFIRMED

`grep -i googletest corpus/SOURCES.md` → **0 matches**; `grep -i googletest corpus/knowledge/ corpus/README.md` → **0 matches**; `grep cd8e73f` over the registry → 0 matches. Matches contract C2 before_state "0 rows and 0 entries citing github.com/google/googletest at base".

## F3 — S256/S257 are in neither id set — CONFIRMED

Independent extraction with the census-valid 0-3-space pattern (`grep -oE '^ {0,3}\| S[0-9]+ '`, ids sorted) reproduces both committed id sets exactly (`diff` clean vs `reg-ids`, 115 ids, max S160; vs `staged-ids`, 103 ids, S153–S255). S256/S257 are absent from both sets and absent as row ids from both files. The only registry occurrences of S256 are footer prose pre-declaring the adoption floor: `corpus/SOURCES.md:455` (round-43 footer: "the safe floor for a partial adoption is `S256`") and `:460` (round-44 footer: "Safe floor S256"). S257–S261 occur nowhere in either file.

## F4 — The 8 collisions and the held dedupes — CONFIRMED

`comm -12` of my two extractions = exactly `S153 S154 S155 S156 S157 S158 S159 S160` — identical to the `collisions` file (8 lines) and to guard `collisions`/`column0_collisions`; strict column-0 extraction of the staged package yields the same 103 ids, so `column0_miss=[]` is real (no collision hides behind indentation; the `guard-proof-collisions` = `S002` / `guard-proof-column0-collisions` = empty pair is the guard selftest T1 extractor proof: 0-3-space sees an indented collision, column-zero is blind).

Held dedupes, by document (URL equality between staged row and held row):

| staged (SOURCES.append.md) | document | held (corpus/SOURCES.md) | same URL? |
|---|---|---|---|
| S153 (:7) | pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html | S105 (:117) | yes → dedupe S153→S105 |
| S154 (:8) | raw.githubusercontent.com/google/golden/master/golden.go | S106 (:118) | yes → dedupe S154→S106 |
| S159 (:13) | pitest.org/quickstart/basic_concepts/ | S155 (:125) | yes → dedupe S159→S155 |
| S160 (:14) | pitest.org/faq/ | S156 (:126) | yes → dedupe S160→S156 |

The other four collisions are genuinely different documents from the held rows wearing the same ids — staged S155 = arXiv 2302.09330 vs held S155 = PIT basic concepts; staged S156 = arXiv 2406.09843 vs held S156 = PIT FAQ; staged S157 = JOSS 10.21105/joss.01891 vs held S157 = Python argparse; staged S158 = mir.cs.illinois.edu LamETAL20 PDF vs held S158 = PIT DetectionStatus.java — so they must move to fresh ids, and the map sends them to S258–S261. Map totals: 10 entries, 10 distinct targets, injective, covers all 8 collisions, consumes S256–S261 consecutively with no gap, `map_uncovered`/`map_undocumented`/`map_clash`/`map_below_floor`/`map_held_moved` all empty.

## F5 — Guard receipt is authentic and reproducible from frozen bytes — CONFIRMED

All 15 files in `.ufo/evidence/round-45/assimilation/` are in the freeze commit and worktree-identical (`git cat-file -e` + `git show | diff` per file). Receipt inputs byte-verified: `sha256sum` of freeze-rev `corpus/SOURCES.md` = `d1a4004377cc1db5…` = guard `registry_sha256` (and = current worktree registry); sha256 of the package `SOURCES.append.md` = `020fbeaa048fc672…` = guard `staged_sha256`.

Reproduction (`python3 -I tools/staged-id-guard.py --registry <frozen registry> --staged <package> --map adoption-map.json --json`, tool is read-only — `read_bytes`/`read_text` only, `staged-id-guard.py:421-436`): exit 0, `verdict admitted`, `map_ok true`, `map_reasons []`, `map_floor S256`, `safe_floor S256`, `held {S153:S105, S154:S106, S159:S155, S160:S156}`, `cascade_count 8` — full sorted-JSON diff against committed `guard-map.json` clean.

Refused maps reproduced against the same frozen bytes:
- `refused-map-identity.json` (S202→S202, S203→S203): exit 1, `inadmissible`, `map_staged_clash ['S202','S203']`, reason `map targets are still staged ids: S202,S203` — stdout diff vs committed `refused-map-identity.out` clean.
- `refused-map-next.json` (S202→S161, S203→S162): exit 1, `inadmissible`, `map_staged_clash ['S161','S162']`, reason `map targets are still staged ids: S161,S162` — stdout diff clean.
- No-map analysis: exit 1, `refused`, cascade 8 — naive arithmetic map S153→S161…S160→S168 targets ids another staged row still holds.

## F6 — Id-rule verdict: SATISFIED

Rule, fleet `/home/vgpnk/Projects/shokunin/CORPUS.md:89` (SOURCES.md contract v1): "`id` — `S` + 3 or more digits, the next unused; never reused."

**Con (steelman).** At the freeze the registry's own footer says "Next unused id: S161" twice (`corpus/SOURCES.md:318` Id-allocation section; `:462` round-44 footer). Read over the registry file alone, "the next unused" = S161/S162, and S256/S257 skip 95 ids. The staged package is external and has never landed ("Assimilation: none" through round 44), so a literalist can call S161–S255 unused and the S256 floor an id-space reservation that the next-unused discipline exists to prevent. The guard's floor is tool policy; the contract's "guard verdict admitted" binds mechanics, not the rule's meaning.

**Pro.** (1) "Never reused" is the rule's hard clause; "the next unused" is the discipline serving it. The lane's own precedent — S038–S039 "allocated, never written, retired — never reused or renumbered" (`corpus/SOURCES.md:277-280`, lesson `round-1.md` ER-K8) — treats even allocated-but-never-written ids as under a never-reuse obligation. Staged S161–S255 are stronger still: written, committed documents in the lane's declared assimilation pipeline (S161 = Change-Aware Mutation Testing, S162 = Keeping Mutation Test Suites…, `SOURCES.append.md:15-16`), tracked in the round-43/44 footers. They are claimed, hence not "unused". (2) Under the by-document doctrine the guard operationalizes ("the URL or DOI is the evidence and the id follows it, never arithmetic", `tools/staged-id-guard.py:3-9`), assigning S161 to googletest advanced.md forces staged S161's different document to renumber on adoption — exactly the cascade the guard refuses; the alternative reading is the one that risks the never-reuse invariant itself. (3) The registry footer is two-track by its own text: "Next unused id: S161" for registry-grown rows coexists with "Safe floor S256" for package adoptions (`:455`, `:460` — pre-declared before this round). S256/S257 are the two lowest ids of the adoption track, and the admitted map consumes S256–S261 with no gap. (4) Both ids are first-use anywhere: registry max S160, staged max S255, no retired id touched (S038/S039 untouched).

**Verdict: the id rule is satisfied by S256/S257.** The only reading that rejects them (registry-only next-unused) is the reading that produces the guard-refused cascade and would force a future renumber of staged S161/S162 — i.e., it subordinates the rule's hard "never reused" clause to its allocation heuristic. The admitted guard verdict, the S038–S039 precedent, and the footer's own two-track doctrine all agree on S256/S257.

## Residual risk / verification gaps

- The deciding C2 run is L1's; at review time the registry still equals the freeze (no S256/S257 rows landed yet). My review covers the map/id-rule layer; the landed rows are judged by `.ufo/evidence/round-45/coverage/measure.py` (which counts any mined googletest row with a committed snapshot + sha prefix — ids are not hardcoded there, so the guard-admitted map is the only id authority, as reviewed here).
- Handoff note for the coverage executor: for `gt_rows` to count them, the adopted S256/S257 rows must be 13-cell `mined` rows whose anchor cell carries `.ufo/evidence/round-45/coverage/sources/googletest-advanced.md` / `googletest-primer.md` plus matching sha prefixes (`05546ed6…`, `03d756ab…`), and whose used-by lists the re-grounded entries.
- The registry footer's "Next unused id: S161" line will need its append-only reconciliation at landing (adoption-track note); not a map defect.
- I did not fetch upstream bytes (no network claim in scope); the pin's byte-identity rests on the committed snapshot sha matching the row's declared sha, which I verified.
