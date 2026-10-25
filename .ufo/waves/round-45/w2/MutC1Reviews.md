seat: MutC1Reviews

# C1 review-gate mutation audit (freshness counter)

Item: copy `.ufo/evidence/round-45/freshness/measure.py` (frozen; sha256
`ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`) to
`/tmp/tameshi-r45-MutC1Reviews/measure.py`; one minimal mutation per rule;
detector = `python3 measure.py --selftest` (cwd `/tmp/tameshi-r45-MutC1Reviews`).
Baseline on pristine bytes: exit 0, `C1_R45_SELFTEST: cases=19 failed=0`,
`VERDICT: PASS` — no inconclusive runs. Every mutant was restored to exact
base bytes before the next case (restored hash re-verified each time).
No lane file was touched; only scratch under `/tmp/tameshi-r45-MutC1Reviews/`
and this report were written. No tool installs (stdlib only).

## Verdict table (rule -> mutation -> selftest)

| # | Rule | Mutation (file:line) | Verdict |
|---|------|----------------------|---------|
| 1 | review_sets non-author | drop `or who == authors.get(rid)` from skip gate (measure.py:204) | SURVIVED |
| 2 | review_sets seat membership | drop `or who not in seats` (measure.py:204) | KILLED |
| 3 | review_sets report prefix | `if not report.startswith('.ufo/waves/round-45/'):` -> `if False:` (measure.py:206) | SURVIVED |
| 4 | review_sets report names id | drop `or not re.search(...rid...)` (measure.py:209) | KILLED |
| 5 | review_sets report names reviewer | drop `or who not in text` (measure.py:209) | SURVIVED |
| 6 | review_sets agree/dispute | `if r.get('verdict') == 'agree':` -> `if r.get('verdict') != 'dispute':` (measure.py:211) | SURVIVED |
| 7 | review_sets dispute sinks agree | `fresh = len(agreed - disputed)` -> `fresh = len(agreed)` (measure.py:254) | SURVIVED |
| 8 | wave_seats non-empty output | drop `and str(x.get('output') or '').strip()` (measure.py:189) | KILLED |
| 9 | population mined | `r['status'] == 'mined'` -> `r['status'] != 'queued'` (measure.py:97) | SURVIVED |
| 10 | population id<=160 | `int(rid[1:]) <= MAX_ID` -> `int(rid[1:]) < MAX_ID` (measure.py:97) | SURVIVED |
| 11 | population URL | drop `and r['url']` (measure.py:97) | SURVIVED |
| 12 | population 0-3 spaces | ROW_RE `^ {0,3}\|` -> `^ {0,4}\|` (measure.py:63) | KILLED |
| 13 | measure duplicate-entry refusal | `if counts[rid] != 1:` -> `if False:` (measure.py:241) | SURVIVED |
| 14 | grade quote copied from row | `if quote.lower() in fold(cells).lower():` -> `if False:` (measure.py:160) | KILLED |

6 killed, 8 survived. Killed mutants were caught by existing fixtures:
#2/#8 -> `FAIL T17_independent_reviews fresh=['S001', 'S008'] disputed=['S003']`;
#4 -> `FAIL T17_independent_reviews fresh=['S001', 'S006'] disputed=['S003']`;
#12 -> `FAIL T15_population_bounds got=['S001', 'S003']`;
#14 -> `FAIL T19_quote_copied_from_row got=verified (ok)`.

## Survivors and the case that would kill each

1. **Non-author gate (measure.py:204)** — the only self-review in T17 is
   S002/ExecA, whose report text `RevX RevY RevZ S001 S002 S003 S004 S005 S008`
   does not name `ExecA`, so removing the author check changes nothing (the
   reviewer-in-text check at line 209 still drops it). Kill case: a self-review
   whose committed report names both the reviewer and the id (e.g. report text
   containing `ExecA` and `S002`) — fresh would wrongly include S002.
3. **Report prefix gate (measure.py:206)** — both out-of-prefix reviews in T17
   (S005 -> Gone.md, S007 -> /tmp/Rev.md) are unreadable through `reports.get`
   (returns None), so the `not text` check at line 209 masks the prefix removal.
   Kill case: a committed, readable report outside `.ufo/waves/round-45/` that
   names id + reviewer (e.g. `/tmp/Rev.md` resolved by read_text).
5. **Reviewer-in-text gate (measure.py:209)** — no fixture review is blocked
   solely by this check: S002 is blocked by the author gate first, all others
   are blocked earlier. Kill case: an eligible review whose report names the id
   but not the reviewer.
6. **Agree/dispute dispatch (measure.py:211)** — `!= 'dispute'` accepts any
   non-dispute verdict as agree; T17 contains only `agree`/`dispute` verdicts,
   so behavior is identical. Kill case: an eligible review with a bogus verdict
   (e.g. `fine`) would count as agree.
7. **Dispute sinks agree (measure.py:254)** — `--selftest` never invokes
   `measure()`; T17 re-implements `agreed - disputed` inline, so the counter
   arithmetic is unexercised. Kill case: run `measure()` on a fixture where a
   verified row carries both an agree and a dispute — fresh must exclude it.
9. **Population mined (measure.py:97)** — `!= 'queued'` only changes verdict for
   rows whose status is neither `mined` nor `queued`; T15 rows are all mined or
   queued. Kill case: a census-valid row with a third status (e.g. `ready`/
   `retired` with URL, id<=160) would be wrongly included.
10. **Population id<=160 (measure.py:97)** — `< MAX_ID` excludes S160; T15's
    over-cap row is S161, so nothing changes. Kill case: a mined S160 row with a
    URL (should be included; would be dropped).
11. **Population URL (measure.py:97)** — every T15 row has a URL, so dropping
    the check changes nothing. Kill case: a mined row id<=160 with no http(s)
    URL in the source cell (would be wrongly included).
13. **Duplicate-entry refusal (measure.py:241)** — `--selftest` never invokes
    `measure()`; no ledger fixture exists. Kill case: a ledger with two entries
    for one population id (must be `invalid`, not verified).

## Restoration evidence

Detector byte hash before (base) and after final restore (identical):
`ba64041f49ffcf15bb0d881604a5fe3ccf9d24e56f72bef055035fbe3d27c6ed`.
Per-mutant hashes (mutant sha256 prefix..suffix, all restored to base afterwards):
- #1 cbe5268371ca..eb65677f9c73; #2 e82a9b0cf76b..25f36e0ec07a
- #3 1130792c33ef..f27ca9827bf2; #4 ef891026420d..c5c2fd50d5c1
- #5 1cb58216d8dc..6683219c917e; #6 23e7cdb9e89f..b4d2a263793b
- #7 2e26d75eb514..c001cf2df67e; #8 7590d43254d3..d592c713a4a0
- #9 57710692d3d1..841e0d4f1a80; #10 6657dd5de4c6..b623baf62ae4
- #11 7e226cee44bb..2ca63f8592db; #12 e0f625952459..a689e115a470
- #13 fa542e8ce6ab..e37a988ff9d2; #14 791c00d02e41..515bac15c603
`sha256sum` of scratch measure.py after the run equals the lane file's hash
(see command output: all three identical). No lane edits, no git/jj mutations.

Commands: `cp .ufo/evidence/round-45/freshness/measure.py /tmp/tameshi-r45-MutC1Reviews/measure.py`; `python3 /tmp/tameshi-r45-MutC1Reviews/driver.py` (applies one mutation per rule from pristine base, runs `python3 measure.py --selftest`, restores, verifies hashes).
