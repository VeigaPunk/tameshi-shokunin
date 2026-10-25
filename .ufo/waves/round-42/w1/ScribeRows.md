# ScribeRows — round 42 wave 1: draft registry rows S155, S156, S157

Scribe: L1Tameshi42.ScribeRows — access date 2026-10-25
Milestone: Draft rows. The three rows below are DRAFTS for the round-42
append; the live lane checkout was not edited (read-only seat). Ready to be
appended to `corpus/SOURCES.md` once the wave's L1 integration owner applies
them (registry confirmation: next unused id S155).

## Findings (evidence first)

1. **IDs S155, S156, S157 are free.** `grep -cE '^\| {0,3}S(155|156|157)[^0-9]' corpus/SOURCES.md` in the lane at base `c77c2b7e64d2e356381441ecf94abac03e984606` → `0`. Registry currently holds 109 rows S001–S154 (ScoutRegistryState verifies the 109-row census; this report re-ran the id check against the live checkout, no matches).
2. **All three URLs opened by this seat on 2026-10-25, snapshots saved under `/tmp/tameshi-r42-ScribeRows-src/`**:
   - `curl -fsSL -A "Mozilla/5.0" -o pit-basic-concepts.html https://pitest.org/quickstart/basic_concepts/` → `12155` bytes, sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a` (page title "Basic concepts"). Same hash as ScoutPitConcepts's snapshot.
   - `curl -fsSL -A "Mozilla/5.0" -o pit-faq.html https://pitest.org/faq/` → `20845` bytes, sha256 `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1` (page title "FAQ"). Same hash as ScoutPitFaq's snapshot.
   - `curl -fsSL -A "Mozilla/5.0" -o python-argparse.html https://docs.python.org/3/library/argparse.html` → `328434` bytes, sha256 `3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7` (Python 3.15.1 documentation). Same hash as ScoutArgparse's snapshot.
3. **Verbatim quotes (each <=25 words), located with section/anchor, access date 2026-10-25:**
   - S155, `§Running the tests` (outcome list): "Killed means a test caught the mutation successfully." (8 words; snapshot line 175).
   - S156, `§I'm seeing a lot of timeouts`: "PIT may therefore incorrectly flag the mutation as causing an infinite loop." (13 words; snapshot lines 298–299). Also `§Is it random?`, `§Timeouts`: "a mutant may be detected as timed out on one run, but killed or surviving on another." (17 words; snapshot lines 298–299).
   - S157, `§argparse.ArgumentParser.add_argument`, `§dest`: "For optional argument actions, the value of dest is normally inferred from the option strings." (15 words; snapshot lines 1504–1505). "Any internal - characters will be converted to _ characters to make sure the string is a valid attribute name." (19 words; snapshot lines 1513–1514).
4. **Used-by targets do not exist at the base revision** (verified: `corpus/knowledge/pit-outcome-vocabulary.md` and `corpus/knowledge/r42-attribute-and-outflag-destinations.md` return "No such file or directory"). They are the round-42 wave's own outputs (C2 knowledge entry and the PIT outcome-vocabulary entry), so the rows' used-by cells resolve at the measurement revision, not at the base; consistent with C2's `sourced` field.
5. **Recheck cadence** set to `180d` for all three rows (docs pages, matching S153/S154/S099 precedent).

## Drafted rows (exact 11-column schema of `corpus/SOURCES.md` header: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by)

| S155 | Basic Concepts (PIT docs) — https://pitest.org/quickstart/basic_concepts/ | docs | A | PIT's mutant outcome vocabulary: Killed, Survived, No coverage, Non viable, Timed Out, Memory error and Run error, and what each means for detection | §Running the tests @ page fetched 2026-10-25, snapshot /tmp/tameshi-r42-ScribeRows-src/pit-basic-concepts.html 12155 B sha256 c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a | Killed means a test caught the mutation successfully; Survived means the covering test did not detect it; No coverage is Survived with no exercising tests; Timed Out flags suspected infinite loops; Non viable mutants fail JVM loading; Memory error and Run error are harness-level diagnostics, not detection outcomes | mined | 2026-10-25 | 180d | corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r42-attribute-and-outflag-destinations.md |
| S156 | FAQ (PIT docs) — https://pitest.org/faq/ | docs | A | why suites turn red only under PIT, how timeout outcomes are inferred, and why identical finally-block mutants kill separately | §I'm seeing a lot of timeouts and §I have mutations that are not killed but should be @ page fetched 2026-10-25, snapshot /tmp/tameshi-r42-ScribeRows-src/pit-faq.html 20845 B sha256 ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1 | timeouts are detected by comparing per-test execution time without and with the mutant against normal time * x + y, so PIT may incorrectly flag a mutation as an infinite loop; a suite must pass green standalone because hidden environment or order dependencies surface only under PIT; javac copies finally blocks per exit point, so PIT creates one mutation per copy and most suites kill only one | mined | 2026-10-25 | 180d | corpus/knowledge/pit-outcome-vocabulary.md |
| S157 | argparse — Parser for command-line options, arguments and subcommands (Python 3.15.1 documentation) — https://docs.python.org/3/library/argparse.html | docs | A | how add_argument's dest maps an option string to the Namespace attribute name | §argparse.ArgumentParser.add_argument §dest @ docs page fetched 2026-10-25, snapshot /tmp/tameshi-r42-ScribeRows-src/python-argparse.html 328434 B sha256 3158c439e504752c93f582ddec59483a75c890411c1d3ee3b733125950bf93b7 | for optional argument actions dest is normally inferred from the option strings: take the first double-dash long option string and strip initial '-' characters, else the first single-dash long option, else the first short option; internal '-' become '_' so the string is a valid attribute name; positional dest is normally the first argument to add_argument | mined | 2026-10-25 | 180d | corpus/knowledge/r42-attribute-and-outflag-destinations.md |

## Row hygiene

- No `|` appears inside any cell (checked on all three drafts); each row is 11 pipe-delimited fields, matching the S153/S154 model.
- `status` = mined (each URL was opened by this seat; snapshots pinned with sha256 + byte size).
- `kind` = docs, `tier` = A for all three, matching the staged rows' kind/tier and the PIT doc-row precedent (S041, S056, S099).
- Source-cell title style mirrors existing PIT rows (S056 "Mutation operators (PIT docs)") and Python docs rows (S153/S154).
- Staged ids: S155 drafts `staged:S159` (PIT basic concepts), S156 drafts `staged:S160` (PIT FAQ), S157 is new (Python argparse docs). Collisions staged/lane S153/S154 do not affect these rows.

## Could not check

- The assimilation package `/home/vgpnk/Projects/shokunin/merge/tameshi/` does not exist on this host (read-only reference package unavailable); staged-row field comparison relied on the live pages and this wave's scout reports (ScoutPitConcepts, ScoutPitFaq, ScoutArgparse), whose snapshot hashes match this seat's fetches exactly.
- `pit-outcome-vocabulary.md` and `r42-attribute-and-outflag-destinations.md` were absent at base; their eventual existence at the measurement revision is the responsibility of the sibling seats that write them (this seat does not create them).
- Rows are drafts only: appending to `corpus/SOURCES.md` is the integration owner's step, not this seat's (read-only lane).

## Tooling

No tools installed or upgraded (curl, sha256sum, wc, python3, grep already present; nothing new recorded).
