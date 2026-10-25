seat: RevC2Predicate

Item: side-by-side of contract C2 statement/target vs coverage counter docstring predicate vs `C2_R45_PASS` label; unheld-surface sweep; AXES.md coverage definition; CORPUS.md rule 4. All paths below relative to the lane unless prefixed.

## 1. Side-by-side quotes

**contract.json `claims.C2.statement`** (`.ufo/evidence/round-45/contract.json`, frozen):
> "Two new registry rows for GoogleTest upstream documents (advanced.md and primer.md at commit cd8e73f067129f8489e35c7b51c7a68552b289d2), opened this round with committed snapshots and sha256 prefixes in their anchors, adopted at guard-admitted ids S256 and S257, are each cited by a re-grounded knowledge entry (verified-at 2026-10-25, listed in the row's used-by, carrying a located 6-25-token quote of the cited snapshot), and every such entry is indexed in corpus/README.md."

**contract.json `claims.C2.target`**:
> "C2_R45_PASS=true: self_pin=1 rows>=2 entries>=2 indexed==entries"

**measure.py docstring predicate** (`.ufo/evidence/round-45/coverage/measure.py:4-17`):
> "C2_R45_PASS=true iff entries >= 2 and rows >= 2 and indexed == entries and self_pin=1, where
> * rows = census-valid registry rows at REV with status `mined` whose source cell's first URL is under github.com/google/googletest/ or raw.githubusercontent.com/google/googletest/, whose anchor cell names a snapshot path under .ufo/evidence/round-45/coverage/sources/ present at REV and an 8+-hex sha256 prefix of that snapshot's bytes;
> * entries = corpus/knowledge/*.md files at REV whose line 1 is `source:` citing at least one such row id, line 2 `verified-at:` with an ISO date >= 2026-10-25, line 3 `recheck:`, that are listed in the cited row's used-by cell, and that carry at least one double-quoted ("..." or “...”) quote of 6..25 whitespace tokens found in the whitespace-folded text of a cited row's snapshot;
> * indexed = entries whose repo path appears backticked in corpus/README.md at REV."

**`C2_R45_PASS` label** (measure.py:135-138):
```python
passed = self_pin == 1 and len(entries) >= 2 and len(rows) >= 2 and len(indexed) == len(entries)
print('C2_R45: self_pin=%d rows=%d entries=%d indexed=%d row_ids=%s rev=%s C2_R45_PASS=%s' % (
    self_pin, len(rows), len(entries), len(indexed), ','.join(sorted(rows)) or '-', rev,
    'true' if passed else 'false'))
```

**Receipt label at freeze** (`.ufo/evidence/round-45/before/c2-at-freeze.stdout`, committed pre-data):
> `C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=3310e7be803516ca5934b4e949d91bcec824b179 C2_R45_PASS=false`

## 2. Drift verdict

**Boolean core: IDENTICAL across all four texts** — target ↔ docstring iff ↔ runtime conjunction (measure.py:135) ↔ receipt label: `self_pin=1 ∧ rows>=2 ∧ entries>=2 ∧ indexed==entries`. No drift in the deciding chain. Selftest 10/10 confirms label == docstring on every refusal path (§6).

Statement-vs-predicate deltas, all one-directional; two real loosenesses recorded, none flips a verdict on the intended data:

- **[minor] Statement is stronger than the predicate on per-row citation.** Statement: the two rows "are **each** cited by a re-grounded knowledge entry". The predicate (entry_ok measure.py:93-112; measure:115-135) counts *entries* citing ≥1 googletest row; it never requires every counted row to be cited by some entry. Counterexample shape: rows={S256,S257} with S257's used-by empty, both entries citing only S256 → rows=2 entries=2 indexed=2 → `C2_R45_PASS=true` with S257 uncited. The target label itself encodes only `rows>=2 entries>=2`, so target==predicate==label; the prose statement over-promises relative to the deciding instrument. Mitigation: the intended shape (selftest T1, adoption-map) has each entry cite both rows, and the falsify/integration seats read the actual landed entries. Recorded, not fixed.
- **[minor] Statement pins documents/commit/ids; predicate is document- and ref-agnostic.** Predicate rows = ANY census-valid `mined` row whose first URL is under `github.com|raw.githubusercontent.com/google/googletest/` (GT_RE measure.py:31) with a matching `sources/` snapshot sha prefix — any googletest doc, any ref: the URL's commit segment is not validated against cd8e73f (the sha256 prefix binds snapshot *bytes*, not the URL). A third committed snapshot `googletest-testing.md` exists (`.ufo/evidence/round-45/coverage/sources/`), so a testing.md row would equally satisfy `rows>=2`. Id admission is carried by the separate guard receipts, not the counter: `assimilation/guard-map.json` verdict=`admitted`, `map_floor`=`safe_floor`=`S256`, `map_ok=true`; `assimilation/adoption-map.json` = `{"map":{"S202":"S256","S203":"S257", ...}}` — exactly the contract `id_map`. The counter prints `row_ids` so an auditor sees which rows counted. Division of labor, not label drift.
- **[info] `verified-at 2026-10-25` (statement) vs `ISO date >= 2026-10-25`** (MIN_VERIFIED measure.py:40, check :100-101): deliberate superset; later in-round dates pass, pre-round dates refused — CTL_E receipt shows `reasons={"verified-at": 2}` for 2026-10-24 entries.
- **[info] "sha256 prefixes in their anchors"** — predicate stricter: prefix must match the snapshot's actual bytes at REV (gt_rows measure.py:85-86).
- **[info] "indexed in corpus/README.md"** — predicate operationalizes as the backticked repo path (`corpus/knowledge/x.md` or `knowledge/x.md`) appearing in README (measure.py:129-130); selftest T7 covers.
- **[info] "Two **new** rows"** — the counter does not diff against base; "new" is established by before_state: counter at base AND freeze both give rows=0 (§3).

## 3. Unheld-surface sweep (negative claim carries its sweep)

Assigned command, working tree:
```
$ grep -rniE 'googletest|gtest' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus /home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md
(no output) EXIT=1
$ (same) | wc -l
0
```

Authoritative at the frozen tree:
```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -niE 'googletest|gtest' 3310e7be803516ca5934b4e949d91bcec824b179 -- corpus SKILL.md PROVINCE.md
(no output) EXIT=1
```

Counter against both authorized revs (the contract's `unmoved_command`):
```
$ python3 .ufo/evidence/round-45/coverage/measure.py --lane <lane> --rev 3310e7be803516ca5934b4e949d91bcec824b179
C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=3310e7be803516ca5934b4e949d91bcec824b179 C2_R45_PASS=false   (exit 1)
$ python3 .ufo/evidence/round-45/coverage/measure.py --lane <lane> --rev 5891bdb77aba8489683533ae4cdd3b49b5e2626b
C2_R45: self_pin=0 rows=0 entries=0 indexed=0 row_ids=- rev=5891bdb77aba8489683533ae4cdd3b49b5e2626b C2_R45_PASS=false   (exit 1)
```
`self_pin=0` at base is expected, not a defect: the counter blob is committed at the freeze, not at base (contract `frozen_before`); the control harness's `BASE C2` line shows `self_pin=1` because `run-controls.py` runs the frozen counter file against a scratch rev (`rev=<scratch>`). The freeze-rev output matches the committed pre-data receipt `before/c2-at-freeze.stdout` byte-for-byte and the contract `before_state` "rows=0 entries=0 C2_R45_PASS=false".

Frontier naming: `corpus/README.md:80` — `| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | open |` — no googletest source; `PROVINCE.md:40-42` — "Frontier — F1–F10 in `corpus/README.md` `## Frontier`; ground moves to Core only through an admitted, source-headed `knowledge/` entry whose `source:` cites a `mined` `SOURCES.md` row." The GoogleTest upstream test-order/fixture-lifecycle ground under F3 is genuinely unheld at the freeze.

## 4. AXES.md coverage definition

`/home/vgpnk/Projects/shokunin/AXES.md:12`:
> | **coverage** | Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes) | PROVINCE.md lists every surface; none unexplored without reason |

`AXES.md:21`: "Expansion ↔ `coverage` + `adjacency`". C2 adds rows+entries for a surface with zero prior rows/entries (proven in §3) → expands the governed fraction. Consistent with the definition and with the expansion trend pairing.

## 5. CORPUS.md rule 4

`/home/vgpnk/Projects/shokunin/CORPUS.md:123-125`:
> 4. **Expansion is knowledge, not rows.** The expansion trend counts admitted `knowledge/` entries whose `source:` cites a `mined` row on uncovered coverage-map ground. There is no row quota; a short registry of opened, honestly tiered rows beats a long one.

C2's unit is the knowledge entry (`entries>=2`, `indexed==entries`), citing `mined` rows on uncovered ground (rows=0 at freeze) — exactly rule 4's shape. `rows>=2` is a floor, not a quota. Row-only expansion is refused by the counter, per the committed do-nothing controls (`.ufo/evidence/round-45/control/controls-at-base.stdout`): `CTL_D C2 ... rows=0 entries=0` (package rows+entries copied byte-exact) and `CTL_E C2 ... rows=2 entries=0 ... reasons={"verified-at": 2}` (rows normalized, entries not re-grounded).

## 6. Selftest (authorized mode)

```
$ python3 .ufo/evidence/round-45/coverage/measure.py --selftest
PASS T1_two_entries_pass want='C2_R45_PASS=true' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
PASS T2_rows_only_fail want='entries=0' got=C2_R45: self_pin=1 rows=2 entries=0 indexed=0 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T3_old_verified_at want='entries=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T4_quote_not_in_snapshot want='entries=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T5_not_used_by want='entries=1' got=C2_R45: self_pin=1 rows=2 entries=1 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T6_bad_sha_prefix want='rows=1' got=C2_R45: self_pin=1 rows=1 entries=2 indexed=2 row_ids=S257 rev=m C2_R45_PASS=false
PASS T7_not_indexed want='indexed=1' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=1 row_ids=S256,S257 rev=m C2_R45_PASS=false
PASS T8_queued_rows want='rows=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS T9_non_googletest_url want='rows=0' got=C2_R45: self_pin=1 rows=0 entries=0 indexed=0 row_ids=- rev=m C2_R45_PASS=false
PASS T10_indented_row_counts want='rows=2' got=C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true
C2_R45_SELFTEST: cases=10 failed=0
VERDICT: PASS   (exit 0)
```

## Verdict

Milestone "C2 claim = predicate = label": **HOLDS** on the deciding chain (contract target ↔ docstring iff ↔ runtime label ↔ frozen receipt, all identical; selftest 10/10). Two minor statement-vs-predicate loosenesses recorded in §2 (per-row citation coverage not enforced; document/commit/id pin carried by guard/adoption receipts rather than the counter) — neither is drift within the deciding chain, neither flips the intended data's verdict. No actionable defect requiring contract or counter amendment.

Residual risk / verification gaps:
- The counter alone cannot prove "each row cited by an entry" or "advanced/primer @ cd8e73f landed at S256/S257"; those ride on `assimilation/guard-map.json` + `assimilation/adoption-map.json` and on the falsify/integration seats reading the actual landed rows/entries at the deciding revision.
- My counter runs are against base/freeze only (seat-authorized); the ONE deciding run is the L1's.
- No tools installed or upgraded for this seat (none needed); no pacman transactions performed.
