seat: CritC1Predicate

# C1 claim = predicate = label — side-by-side review

## 1. The three texts (quoted verbatim)

**A. Contract statement** (`.ufo/evidence/round-45/contract.json:21`):
> "At least 50 of the lane's held external source rows are re-verified this round against live bytes: each has a committed snapshot fetched on/after 2026-10-25 from the row's own URL, a 6-25-token quote located afresh in that snapshot (not copied from the row's own cells) that shares >= 2 content words with the row's scope/anchor/teaches, and an agree verdict by a non-author falsify-wave seat whose committed report names the row, with no dispute."

**B. Contract target** (contract.json:22): `"C1_R45_PASS=true: self_pin=1 fresh>=50"`

**C. Frozen predicate** (`freshness/measure.py:4-9`, docstring):
> "C1_R45_PASS=true iff fresh >= 50, where fresh = the population rows that are `verified` AND carry >= 1 `agree` review by a reviewer other than the entry's author AND carry no `dispute` review; the population is the census-valid rows at REV with status `mined`, id <= S160 and an http(s) URL in the source cell; and the counter's own bytes at REV equal the running file (self_pin=1)."

**D. Printed receipt label** (measure.py:263-267; observed at freeze):
```
C1_R45: self_pin=1 population=73 entries=0 verified=0 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=0 score=0 target=50 rev=3310e7be803516ca5934b4e949d91bcec824b179 C1_R45_PASS=false   (exit=1)
```
PASS condition implemented: `passed = self_pin == 1 and fresh >= TARGET` (measure.py:256).

## 2. Same statement? Verdict

**Yes — A, C and D express the same predicate**: PASS iff `self_pin=1` and `fresh>=50`, where `fresh` counts population rows that are `verified` (entry verdict `holds`, opened >= 2026-10-25, exact URL match, committed snapshot with sha256 match, 6-25-token quote present afresh in normalized snapshot text, >=2 shared content words) AND carry >=1 agree review by a non-author seat with committed report AND carry no dispute review. Every clause of the statement has a direct counterpart in the docstring and in `grade()`/`review_sets()` (measure.py:132-165, 192-215). No clause is dropped or inverted; the target/label string matches the PASS branch exactly.

## 3. Flagged widenings/narrowings (all minor, none inverts the claim)

1. **"re-verified … against live bytes" vs measured reality (narrowing of the guarantee).** The counter never fetches live bytes. `verified` is proved by: ledger `opened >= 2026-10-25` (measure.py:139-140) + committed snapshot blob at REV whose raw sha256 equals the entry's `raw_sha256` (measure.py:143-144) + quote presence in that snapshot. Live re-fetch exists only as `--live`, explicitly *outside* the predicate (measure.py:36-39, 300-322). So “live bytes” is attested only by the authored `opened` date; a post-freeze ledger could in principle cite a snapshot never fetched this round. Design-inherent (snapshot identity), but the literal phrase is stronger than what is measured.
2. **"falsify-wave seat" is not enumerated — only the results filename is (widening).** `wave_seats()` (measure.py:182-189) admits *any* seat with non-empty text in orchestrator-written `.ufo/waves/round-45/w2-results.json`. Wave membership is asserted by the file name alone; there is no check that the seat actually ran in the falsify wave. If the orchestrator ever wrote another wave's outputs into w2-results.json, those seats would qualify. Currently `w2-results.json` does not exist at the freeze (verified via `git show <freeze>:…`), so the set is empty at base.
3. **"census-valid" is not enumerated (assumption).** `population()` (measure.py:95-97) checks only `status == 'mined'`, `id <= 160`, and an http(s) URL in the source cell. No census routine is run; the counter trusts the SOURCES.md state at REV. If a row were mined but no longer census-valid, it would still be counted. The root-census exit-0 is a separate no-harm monitor (contract.json:45), not part of this counter.
4. **Statement "names the row" → docstring/code "names both the id and the reviewer" (narrowing).** A review counts only when the committed report path under `.ufo/waves/round-45/` exists at REV and its text contains both the row id and the reviewer name (measure.py:206-210). The statement requires only the row name; the extra reviewer-name condition excludes otherwise-valid agrees.
5. **"non-author" depends on the ledger's `author` field (small assumption).** `authors` is built only from ledger entries (`{id: author}`, measure.py:228); a missing/empty author makes `who != None` pass, so self-review protection relies on the ledger being accurate.
6. **"content words" is counter-defined (narrowing vs unstated meaning).** `words()` (measure.py:128-129) counts only lowercase `[a-z0-9]+` tokens of length >=4 excluding a ~40-word STOP list (`the`…`opened`,`page`,`docs`,`fetched`,`used`,`using`,`same`,`just`…). Shorter tokens and stopwords contribute to neither side. This is a reasonable definition but is narrower than “content words” read plainly.
7. **6-25-token quote** is counted on the *folded* quote (NFKC, typographic quotes/dashes folded, whitespace collapsed, measure.py:149-151); consistent with locating it in folded snapshot text — same tokenization on both sides, so not a drift.
8. Rows with no ledger entry are silently absent from `states` (neither invalid nor counted) — matches the claim's “at least 50 of … rows” reading; no issue.

No widening/narrowing changes the threshold (50), the population (73), or the PASS boolean for any verifiable run; all deviations are definitional precision inside the same statement.

## 4. Population claim (73 at base) — confirmed two ways

**Counter at freeze** (per item command):
```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179
C1_R45: self_pin=1 population=73 entries=0 verified=0 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=0 fresh=0 score=0 target=50 rev=3310e7be803516ca5934b4e949d91bcec824b179 C1_R45_PASS=false
exit=1
```
Matches the frozen receipt `.ufo/evidence/round-45/before/c1-at-freeze.stdout` exactly. `self_pin=1` at freeze (counter bytes at REV == running file).

**Independent awk recount** over `git show <freeze>:corpus/SOURCES.md` (row regex `^ {0,3}\|\s*S\d{3,}\s*\|`, 13 cells, status cell == `mined`, id <= S160, first `https?://…` in source cell):
```
population=73 over160=0 notmined=28 nourl=14 bad_cells=0 bad_id=0
```
73 ids: S001-S006, S008, S011-S012, S024, S026, S028, S041, S047-S049, S052, S054-S066, S068-S070, S072-S079, S081, S084, S086-S087, S089-S091, S093-S097, S099-S108, S132, S152-S160 (S007/S009/S010/… absent: not mined — 28 rows with a URL but status != `mined`; 14 mined rows without URL).
`diff` of the awk id list vs the counter's own `parse_rows`+`population` output: identical 73 ids (only the awk summary line differs). No duplicates (`sort | uniq -d` empty).

Population claim **holds**: 73 at base = freeze; freshness 0 at base (no ledger/reviews/results at freeze — all three files absent via `git show`), so `C1_R45_PASS=false` correctly.

## 5. Score rule vs AXES.md

- Rule (contract.json:26): `freshness score = floor(10 * fresh / population)`; implementation measure.py:255 `score = (10 * fresh) // len(pop)` (guard `pop==0` → 0). Identical for non-negative ints.
- AXES.md (`/home/vgpnk/Projects/shokunin/AXES.md:79`) requires axis scores 0-10. Since `fresh <= population`, floor(10*fresh/pop) ∈ [0,10] always. **Compliant.**
- Reference points: base → score 0 (fresh=0/73). A passing C1 run with fresh=50 → floor(500/73) = **6** (not 7: 500/73 = 6.849). This replaces the round-44 one-document unit (contract.json:26, no-harm monitor `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` must stay 1).

## 6. Bottom line

Claim, frozen predicate, and printed label are the same statement; PASS condition (`self_pin=1 && fresh>=50`) matches the target string. Population 73 at base confirmed by counter run and independent awk. Score rule matches the AXES 0-10 contract. Flagged items are precision definitions (live-bytes attestation, falsify-wave membership, census-valid, report-names-reviewer, content-word filter) — none changes any observable verdict at base or the threshold.
