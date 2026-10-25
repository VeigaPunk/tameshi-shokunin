seat: RevC3Predicate
item: C3 predicate identity audit — contract statement vs counter docstring vs `C3_R46_PASS` label, base-unmoved check, frozen-doc check, AXES/CORPUS/§9 sizing compliance

## Side by side

Contract `.ufo/evidence/round-46/contract.json` C3 `target`:
> `C3_R46_PASS=true: self_pin=1 rows>=3 entries>=3 indexed==entries covered==rows`

Contract C3 `statement`:
> "Three new registry rows for the frozen documents (arxiv.org/abs/2504.16777; the portal.fis.tum.de record of the undetected-flaky-failures paper; the testing.googleblog.com per-post feed 6277555988217606236?alt=json), opened this round with committed snapshots and 8-hex sha256 prefixes in their anchors, adopted at guard-admitted ids S258/S259/S260, are each cited by a re-grounded knowledge entry (verified-at >= 2026-10-25, listed in the row's used-by, carrying a located 6-25-token quote and at least one located quote absent from the package copy of the same entry), and every such entry is indexed in corpus/README.md."

`measure.py:5-6` docstring predicate:
> `C3_R46_PASS=true iff self_pin=1 and rows >= 3 and entries >= 3 and indexed == entries and covered == rows`

`measure.py:176-180` code + label:
```python
passed = (self_pin == 1 and len(rows) >= MIN_ROWS and len(entries) >= MIN_ENTRIES
          and len(indexed) == len(entries) and len(covered) == len(rows))
print('C3_R46: self_pin=%d rows=%d entries=%d indexed=%d covered=%d row_ids=%s rev=%s C3_R46_PASS=%s' % (...
    rev, 'true' if passed else 'false'))
```
with `MIN_ROWS = 3`, `MIN_ENTRIES = 3` (`measure.py:41-42`).

**Same statement? Yes at predicate level.** Target ↔ docstring iff ↔ code condition ↔ label boolean are one sentence (prompt §9: "the same sentence in the plan, the same condition in the counter's code and the same label in the receipt"). The docstring's four field definitions (rows/entries/indexed/covered) implement, respectively: census-valid 13-cell `mined` rows whose first source URL folds (`doc_key`: scheme/`www.`/trailing-slash/case-insensitive, `measure.py:73-76,93-98`) to one of the three frozen docs; the source/verified-at≥2026-10-25/recheck trio with used-by membership, a 6–25-token double-quoted quote located in the folded snapshot text, and ≥1 located quote absent from the committed package copy (`entry_ok`, `measure.py:114-136`); backticked repo path in `corpus/README.md` (`measure.py:167-169`); line-1 citation coverage (`measure.py:166,176`).

## Surface genuinely unmoved at base

Command: `python3 .ufo/evidence/round-46/coverage/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433`
Output (deciding line): `C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C3_R46_PASS=false`, exit 1.
Frozen receipt `.ufo/evidence/round-46/before/c3-at-freeze.stdout` deciding line is byte-identical. Unmoved-command claim (`rows=0 entries=0 shows the surface unmoved`) verified, not assumed.

## Documents frozen in counter and contract

`DOCS` tuple (`measure.py:46-50`) = exactly the three documents the contract C3 statement names, in the same order:
1. `arxiv.org/abs/2504.16777`
2. `portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures` ("the portal.fis.tum.de record of the undetected-flaky-failures paper")
3. `testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`

Committed at base (`git ls-tree -r --name-only 745a5831…`): `coverage/sources/arxiv-2504.16777-abs.html`, `coverage/sources/google-flaky-feed-6277555988217606236.json`, `coverage/sources/tum-portal-flaky-failures.html`, plus package copies `assimilation/package/r5-undetected-flaky-failures.md`, `r6-flaky-failures-cluster.md`, `r9-false-red-rate.md`. Snapshot↔document binding checked by content grep: `2504.16777` in the arxiv snapshot, `6277555988217606236` in the feed snapshot, `an-empirical-study-of-detected-and-undetected-flaky-test-failures` in the TUM snapshot.

Selftest (`--selftest`): `cases=24 failed=0`, `VERDICT: PASS`, exit 0.

## Universal-word audit (prompt §9, /home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-46.md:417-439)

- "are each cited by a re-grounded knowledge entry" → backed by `covered == rows` over a full line scan of `corpus/SOURCES.md` at REV (`flaky_rows`); every counted row must be line-1-cited.
- "every such entry is indexed in corpus/README.md" → backed by `indexed == entries` over a full `git ls-tree` of `corpus/knowledge/`.
- No unbacked "all"/"complete"/"no harm anywhere" inside the C3 statement; the only universals are enumeration-backed equalities. Compliant.

## AXES.md coverage definition

AXES.md:12: coverage = "Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes)". C3 names the surface it moves — contract C3 `surface`: "F3 determinism precondition / flaky-aware verdicts: what the literature measures about flaky-failure clustering, same-job rerun blindness and the false-red rate; 0 rows and 0 entries citing [the three docs] at base" — a new sourced edge class entering the governed domain, not a re-score of held ground. §9 requires the claim to also name "the command that would show it unmoved": present as contract C3 `unmoved_command`, executed above. Compliant.

## CORPUS.md rule 4

CORPUS.md:123: "Expansion is knowledge, not rows. … There is no row quota". C3 does not farm rows: the three rows are exactly the three frozen source documents, and `covered == rows` forces every counted row to carry a re-grounded entry, so entries (knowledge) are the substance and rows the sourcing. A fourth row citing one of the same docs would demand a fourth entry; only first-URL matches count. Consistent with rule 4.

## §9 sizing checklist

- One concrete after-state, one command, committed bytes: target = one label line via `counting_command` at REV. ✓
- Do-nothing controls cannot reach the target: `control/controls-at-freeze.stdout` CTL_A (byte-exact package copies) `entries=0`, CTL_B (relabel, quotes kept) `entries=0`, CTL_C (rows only) `entries=0`, CTL_D (wrong digest) `rows=0`, all `C3_R46_PASS=false`; the selftest independently kills each cheat class (T21 relabel, T02 rows-only, T06 bad digest). ✓
- Predicate frozen before data (committed at base; `amendments: []`). ✓

## Findings

1. **LOW (wording drift, no pass divergence)** — contract says "8-hex sha256 prefixes"; docstring says "8+-hex" and the code accepts 8–64 hex (`HEX_RE = \b[0-9a-f]{8,64}\b`, `measure.py:39`; `digest.startswith(h)`, `measure.py:102`). A row anchoring a full 64-hex digest passes the counter though the contract prose names only the 8-hex form. The binding minimum (≥8, validated against snapshot bytes) is identical, so target/label/predicate never diverge; the docstring's "8+-hex" is the accurate reading. No action possible (frozen), recorded for honesty.
2. **LOW (clause carried outside the predicate)** — "adopted at guard-admitted ids S258/S259/S260" is not enforced by `passed`; any three S\d{3,} ids citing the three docs would pass. Mitigated: the label prints `row_ids=`, so the deciding receipt exposes the actual ids for the closure to compare against the frozen `assimilation/adoption-map.json` (S195→S258, S190→S259, S216→S260) and `assimilation/guard-map.json`.
3. **INFO** — "opened this round" is not byte-checkable at a single rev; carried by the frozen adoption map, not the counter. Inherent to a byte counter.
4. **INFO** — quotes are additionally bounded to 10–400 chars by `QUOTE_RE` (`measure.py:40`) beyond the contract's "6-25-token"; in practice subsumed (6 tokens ≥ 11 chars), no divergence.

## Residual risk and verification gaps

- I did not re-run the CTL fixtures myself; I cite the committed receipt `control/controls-at-freeze.stdout` plus the selftest cases that model the same cheats. The deciding-run authority stays with the L1 per measurement bounds.
- Finding 2 means a closure should eyeball `row_ids=` on the deciding line, not just `C3_R46_PASS=true`.
- Tooling: none installed (none needed); pacman untouched. Scratch: /tmp/tameshi-r46-RevC3Predicate (holds nothing persistent; all commands quoted above ran read-only against the lane or its git objects).
