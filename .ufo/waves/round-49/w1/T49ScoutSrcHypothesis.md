# T49ScoutSrcHypothesis — C2 source recon (read-only; access date 2026-10-26)

Tooling installed/updated: none.

## 1. Document → held id / staged id / verdict

Method: the lane registry `corpus/SOURCES.md` was matched by document (DOI, URL, title, authors), form-insensitive, against the four staged F10 rows in `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` (read-only).
Command: `grep -n -E 'joss\.01891|quviq-testing|351240|smallbone|lic\.pdf|QuickCheck|Hughes|Claessen' corpus/SOURCES.md`, run from the lane root. Its only hits are `corpus/SOURCES.md:278` (a Leads bullet) and `corpus/SOURCES.md:277`, which is unrelated (Regehr).
Rule: CORPUS.md:112-118 (rule 1: a row is a claim, written only after opening the source in the round that writes it; a lead "is not evidence and never a row", `corpus/SOURCES.md:273`; rule 2: append-only).

| document | held id (lane) | staged id | verdict |
|---|---|---|---|
| Hypothesis: A new approach to property-based testing (MacIver, Hatfield-Dodds; JOSS 2019), doi 10.21105/joss.01891 | none as a row. It is only a Leads bullet, `corpus/SOURCES.md:278`, which `corpus/SOURCES.md:273` says is never evidence. | S157 (`SOURCES.append.md:11`) | **new**: the lead is promoted to a row by opening it. It is not a duplicate. The staged id S157 collides with held S157 (argparse, `corpus/SOURCES.md:127`). |
| Hughes, Experiences with QuickCheck: Testing the Hard Stuff and Staying Sane (Quviq) | none | S170 (`SOURCES.append.md:24`) | **new**. Staged id S170 is free in the lane. |
| Claessen and Hughes, QuickCheck (ICFP 2000), doi 10.1145/351240.351266 | none | S182 (`SOURCES.append.md:36`) | **new**. Staged id S182 is free in the lane. |
| Smallbone, Property-based testing for functional programs (Chalmers TR 76L, 2011), smallbone.se/papers/lic.pdf | none | S183 (`SOURCES.append.md:37`) | **new**. Staged id S183 is free in the lane. |

Nothing in the four staged rows is a duplicate. Lane F10-adjacent rows are different documents:
- S018 is the Hypothesis API reference, `corpus/SOURCES.md:29`.
- S019 is Goldstein et al., ICSE 2024, `corpus/SOURCES.md:30`.
- S020 is de Oliveira et al., EMSE 2026, `corpus/SOURCES.md:31`.
- S021 is Maaz et al., arXiv 2510.09907, `corpus/SOURCES.md:32`.
- S046 is the pbt-bibliography, `corpus/lessons/round-1.md:396`. It is a bibliography page, not any of the four.

Extra staged F10 row outside the named four: S204 (googletest parameter generators, `SOURCES.append.md:58`) is also a new document in the lane. `grep -n 'reference/testing.md' corpus/SOURCES.md` shows no hit; the lane holds only S256/S257 (advanced.md/primer.md). It is not in the item's list and the contract names QuickCheck and Smallbone only.

### Id-space finding (affects what C2 appends)
- The lane ids run S001-S037, S040-S097, S099-S108, S132, S152-S160 and S256-S268. The command is `grep -o -E '^ {0,3}\| S[0-9]+' corpus/SOURCES.md`.
- The next id after the lane's tail is S269.
- Staged ids S157-S160 collide with held S157-S160 (argparse, PIT, ...). A census duplicate-id check would fail. The earlier staged rows were renumbered into S256-S268.
- C2 should renumber its rows, for example S269+, not reuse the staged ids verbatim. contract.json "frontier_step.sources" already says "re-numbered after the scratch id-collision check".
- The append-only rule 2 means a row cannot be edited later, so the row text must be rewritten at append time anyway: a row is a claim opened in the round that writes it (rule 1) and needs a fresh `opened` date of 2026-10-26.

URL liveness, checked 2026-10-26 with `curl -sIL`:
- https://doi.org/10.21105/joss.01891 resolves to https://joss.theoj.org/papers/10.21105/joss.01891 (200).
- The quviq-testing.pdf mirror returns 200.
- https://smallbone.se/papers/lic.pdf returns 200.
- S182's DOI was not curl-checked. The staged anchor uses `aaron papers fetch`, so the re-opening seat must use that route.

## 2. Hypothesis statistics quote (held S018 page, no new row needed)

- URL: https://hypothesis.readthedocs.io/en/latest/reference/api.html, section `hypothesis.event` (page lines 470-518 in the read; the section sits under the `note`/`event` block).
- Access date: 2026-10-26.
- Held row: S018 (`corpus/SOURCES.md:29`). Its current anchor is "§Settings, Built-in profiles", so the `event()` use is a new `used-by` or anchor use of an existing document, not a second row.
- Quote (24 words): "Statistics on the number of test runs with each event will be reported at the end if you run Hypothesis in statistics reporting mode."
- The same section names the pytest flag: "These events appear in observability output, as well as the output of our pytest plugin when run with `--hypothesis-show-statistics`." It then shows a sample block with `Events:` percentages, e.g. `31.06%, i mod 3 = 2`.
- Verifying command, which returned the quote string once on 2026-10-26: `curl -fsSL https://hypothesis.readthedocs.io/en/latest/reference/api.html | tr '\n' ' ' | sed 's/<[^>]*>//g' | tr -s ' ' | grep -o 'Statistics on the number of test runs with each event will be reported at the end if you run Hypothesis in statistics reporting mode'`
- `event()` links to a "Test statistics" page, `integrations.html#statistics`. It was not opened by this seat, so any claim from it is unobserved.

## 3. What C2 should append

| append | doc | source id to use | note |
|---|---|---|---|
| yes (2 rows, matching the contract) | QuickCheck, Claessen and Hughes ICFP 2000 | renumber, e.g. S269 | new. Re-open by DOI (`aaron papers fetch 10.1145/351240.351266`); `opened` 2026-10-26. |
| yes | Smallbone TR 76L (lic.pdf) | renumber, e.g. S270 | new. Re-open the PDF §4.1 p.44; `opened` 2026-10-26. |
| optional | Hypothesis JOSS 2019 | renumber | new, but the contract names only QuickCheck and Smallbone. It would promote the lead at `corpus/SOURCES.md:278`. |
| optional | Hughes, Experiences with QuickCheck | renumber | new. Tier B (course mirror). |
| no new row | Hypothesis `event()` and statistics | S018 | cite S018 with the quoted anchor; update `used-by` per rule 2 (the status/recheck/used-by columns may change in place) and log it old→new in the round lesson Gate. |

Counter and pilot-entry constraint: the contract's `sourced` predicate requires the pilot entry to cite at least one row `opened 2026-10-26`. Both QuickCheck/Smallbone rows meet that once re-opened.

## Summary
- All four staged F10 rows (S157, S170, S182, S183) are new documents relative to the lane; there are no duplicates.
- The JOSS Hypothesis paper is held only as a Leads bullet (`corpus/SOURCES.md:278`), not a row, so it is new as a row.
- Staged id S157 collides with held S157 (argparse). Next free tail id is S269, so C2 must renumber.
- C2 should append QuickCheck (ICFP 2000) and Smallbone (TR 76L) at minimum. The JOSS and Hughes rows are optional.
- The Hypothesis `event()`/statistics quote (24 words, https://hypothesis.readthedocs.io/en/latest/reference/api.html, accessed 2026-10-26) belongs to held S018; no new row needed.
- No tools installed; scratch dir removed.
