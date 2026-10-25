seat: CritC1Control

# C1 cheapest-pass attack (round-45 w1)

Counter under test: `.ufo/evidence/round-45/freshness/measure.py` @ freeze `3310e7be803516ca5934b4e949d91bcec824b179`.
Per-row gate `grade()`: measure.py:132-165; review gate `review_sets()`: 192-215; seat helper `--check`: 271-297.
Every fragment below was graded with
`python3 .ufo/evidence/round-45/freshness/measure.py --lane <LANE> --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check <frag>.json --snapdir /tmp/tameshi-r45-CritC1Control`
(snapshot bytes live in the scratch dir; the counter reads the registry from the lane at the freeze rev).

## What the counter actually checks per row
1. `entry.url == row.url` (measure.py:137-138) — else `invalid url mismatch`.
2. `opened >= 2026-10-25` (139-140).
3. snapshot blob present and `sha256(raw) == raw_sha256` (141-144).
4. verdict `holds`/`drifted`/`unreachable`+evidence (145-148).
5. quote 6-25 whitespace tokens (149-152).
6. quote present in the normalized extracted text of the snapshot (153-158).
7. quote not a folded substring of the row's source/scope/anchor/teaches cells (159-161).
8. `words(quote) ∩ words(scope+anchor+teaches) >= 2` (162-164) — the source cell is excluded from overlap; quote `opened` is a self-declared string, never checked against anything.
`measure()` never touches the network; `live()` (300-322) is a separate manual helper outside the deciding run. `fresh` additionally requires an `agree` review: reviewer ≠ entry author, reviewer named with non-empty output in `.ufo/waves/round-45/w2-results.json` (orchestrator-written, unverifiable by the counter), committed report under `.ufo/waves/round-45/` whose text names the id and the reviewer (192-215).

## Attack fragments — accepted / refused (3 real rows)
Rows: S001 (Stryker mutant-states-and-metrics URL), S049 (docs.python.org subprocess), S102 (POSIX Shell Command Language §2.3).

| # | attack | row | snapshot bytes used | quote (6-25 tokens) | result |
|---|---|---|---|---|---|
| A1 | boilerplate (page-title chrome) | S001 | fresh fetch of S001 URL, sha `ac273386…` (s001-stryker.html) | `Mutant states and metrics | Stryker Mutator` | `CHECK S001 verified ok` |
| A1b | boilerplate (page-title chrome) | S049 | fresh fetch of S049 URL, sha `587938d2…` (sp.html) | `subprocess - Subprocess management - Python 3.15.1 documentation` | `CHECK S049 verified ok` |
| A2 | unrelated section of the right page | S102 | fresh fetch of S102 URL, sha `0889867a…` (s102-stale.html); quote taken from §2.2.2 Escape Character, not anchor §2.3 | `\e yields an <ESC> character. \f yields a <form-feed> character. \n yields a <newline> character.` | `CHECK S102 verified ok` |
| A3 | different-URL bytes mentioning the same words | S001 | Wikipedia "Mutation testing" article, sha `616dd5a5…` (wiki.html ≠ S001 URL bytes); `entry.url` stays the Stryker URL | `Rejection is called killing the mutant. The value of a test suite is measured by the percentage of mutants that it kills.` | `CHECK S001 verified ok` |
| A4 | stale cached copy | S102 | the lane's round-35 committed blob `.ufo/evidence/round-35/src/s102-posix-chap02.html` (sha `0889867a…`, fetched 2026-10-23 per row; `cmp -s` shows it is byte-identical to today's live fetch), `opened` declared 2026-10-25 | `it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment` | `CHECK S102 verified ok` |

Full `--check` output matrix (fragments in /tmp/tameshi-r45-CritC1Control):
```
F-S001-A1b-title                    S001 verified ok
F-S001-A3-diff-url                  S001 verified ok
F-S049-A1-boilerplate               S049 verified ok
F-S102-A2-unrelated-section         S102 verified ok
F-S102-A4-stale                     S102 verified ok
N-url-mismatch                      S049 invalid url mismatch
N-opened-before                     S049 invalid opened before round
N-verdict-bad                       S049 invalid bad verdict
N-sha-mismatch                      S049 invalid sha mismatch
N-quote-len5                        S049 invalid quote length 5
N-quote-absent                      S049 invalid quote absent
N-overlap1                          S049 invalid overlap 1
N-quote-copied                      S001 invalid quote copied from row
```
Accepted: all four attack classes (A1/A1b, A2, A3, A4). Refused: URL mismatch, opened before round, bad verdict, sha mismatch, quote length outside 6-25, quote absent, overlap < 2, quote copied from the row's own cells. The counter has no check of snapshot provenance (which URL the bytes came from), snapshot age, or topicality beyond a 2-word lexical overlap with scope/anchor/teaches.

## Cheapest ledger that passes the full counter (not just `--check`)
Scratch fixture `/tmp/tameshi-r45-cheapest-9pzlt0ym` (git init -b m; seeded from lane archive @ freeze; counter copied into the tree for self_pin; ENV-clean as run-controls.py:42-43). Files added:
- `.ufo/evidence/round-45/freshness/sources/shared.raw` — ONE 5,537-byte snapshot holding 50 synthetic sentences;
- `ledger.json` — 50 entries (first 50 population ids, S001..S094), author `ControlAuthor`, `snapshot=shared.raw` for all, `opened=2026-10-25`, `verdict=holds`, each quote = a per-row sentence embedding ≥2 of that row's scope/anchor/teaches words (guaranteed overlap ≥ 2, not a substring of the row cells);
- `reviews.json` — 50 `agree` reviews by `ForgeReviewer`, report `.ufo/waves/round-45/w2/ForgeReviewer.md` (names every id + the reviewer);
- `.ufo/waves/round-45/w2-results.json` — `{"results":[{"name":"ForgeReviewer","output":"agree"}]}` (forged orchestrator seat evidence, as in CTL_C).

Run: `python3 $D/.ufo/evidence/round-45/freshness/measure.py --lane $D --rev m`
→ `C1_R45: self_pin=1 population=73 entries=50 verified=50 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=50 score=6 target=50 rev=m C1_R45_PASS=true` (exit 0).
No live byte is fetched by the counter or by any reviewer at any point; the deciding measurement is fully offline.

## CTL_A-C vs a cheaper control
`run-controls.py` builds CTL_A (73 gzip snapshots each containing the row's own teaches cell + ledger), CTL_B (+ reviews + committed report), CTL_C (+ forged w2-results.json). Receipt `controls-at-base.stdout`: all three end `fresh=0`, `invalid=73`, reason `quote copied from row` — their quotes are the rows' own teaches cells (measure.py:159-161). They are the cheapest *honest-skip* ledgers, but they do NOT reach the target.
A strictly cheaper tree does: the shared-snapshot forged ledger above — ~5 files (~6 KB) vs CTL_A's 74 files — and it scores `fresh=50 C1_R45_PASS=true`. So the answer is: CTL_A-C are NOT the cheapest way to pass; the counter's decisive gate is the falsify-wave reviewer consent, and even that gate only checks reviewer-name presence, non-empty output, and a report containing two strings (measure.py:182-215). The counter's per-row mechanics are fully forgeable without any re-verification.

## Residual trust placed on W2 reviewers — what each accepted attack requires to be closed
- A1/A1b (boilerplate/title chrome): reviewer must refetch the row URL (`curl -fsSL`), compare sha256 with `raw_sha256` and the committed snapshot, and read the quote in context: it must be article-body prose (not `<title>`/nav/footer/cookie chrome) and must substantively state the row's scope/anchor/teaches claim. A 2-word lexical overlap is nowhere near sufficient — `Mutant states and metrics | Stryker Mutator` passes on shared vocabulary alone.
- A2 (unrelated section): same, plus check the quote's section location relative to the row's anchor section and that the sentence actually carries the claimed semantics (e.g., S102's anchor is §2.3; an §2.2.2 escape-character sentence is about a different rule).
- A3 (different-URL bytes): reviewer must fetch the row's OWN URL and diff bytes against the committed snapshot; any mismatch (or absence of an in-window fetch) → dispute. This is the decisive check for the whole class and is entirely manual — the counter never makes it.
- A4 (stale copy): reviewer must establish the snapshot was actually fetched on/after 2026-10-25 (e.g., curl date/Last-Modified/ETag observation, or a fetch receipt committed in wave artifacts). For URLs whose bytes are stable across rounds (S102 today: identical sha to the lane's round-35 snapshot) only such fetch-time evidence distinguishes stale from fresh.

No tools were installed (RULES.md consulted; existing git/python3/curl used). No lane state was modified apart from this report.
