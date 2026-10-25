seat: ScribeEntryCluster
item: Drafted the re-grounded F3 entry `r6-flaky-failures-cluster.md` as `.ufo/waves/round-46/w1/ScribeEntryCluster.entry.md` from S258 (arXiv 2504.16777 abstract snapshot), every quote re-located in the committed snapshot, and proved it admitted by the frozen C3 counter in a throwaway fixture.

# ScribeEntryCluster — C3 entry (flaky failures cluster)

## Axes used (godspeed)

1. **located-quote coverage** — how many quotes the snapshot actually supports, and how many of them are fresh against the package copy (the counter's `no quote fresh against the package copy` refusal).
2. **claim support** — every package sentence either re-located or dropped/softened.
3. **counter admission** — does the drafted file pass `entry_ok()` of `.ufo/evidence/round-46/coverage/measure.py`.

Moves were kept only when they raised one axis without lowering another (e.g. a longer located span raised axis 1 and cost nothing on axis 2).

## Deliverable

`.ufo/waves/round-46/w1/ScribeEntryCluster.entry.md` (45 lines, 7,035 bytes), basename kept as `r6-flaky-failures-cluster.md` because the counter's freshness rule keys on the package copy of the same basename. Header trio, byte-exact against the item's required line 1:

```
$ cmp want_h1.txt got_h1.txt   # sed -n '1p' of the entry vs the required string
H1_EXACT
source: S258 — https://arxiv.org/abs/2504.16777 — §Abstract — arXiv:2504.16777v1 — snapshot .ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html (sha256 28d2954d…)
verified-at: 2026-10-25
recheck: 365d — `curl -fsSL 'https://arxiv.org/abs/2504.16777' | grep -c 'co-occurring failures that share the same root causes'` → `3` (...)
```

Line 4 is `ground: F3 — …` (plus the F8 link, see §4).

## Provenance checks (run)

```
$ sha256sum .ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html
28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14  …/arxiv-2504.16777-abs.html

$ python3 .ufo/evidence/round-45/freshness/measure.py --extract …/arxiv-2504.16777-abs.html > /tmp/tameshi-r46-ScribeEntryCluster/extract.txt
exit=0 ; wc -l -c extract.txt -> 1 5169
```

Every quotation was then tested against that extraction with the same fold the counter applies (`unicodedata.normalize('NFKC')` + the curly/dash/soft-hyphen/NBSP map + whitespace collapse), and against the folded package copy:

```
$ python3 /tmp/tameshi-r46-ScribeEntryCluster/audit_entry.py
L12  tokens=14 located=1 fresh=1 OK
L14  tokens=21 located=1 fresh=1 OK
L16  tokens=20 located=1 fresh=1 OK
L16  tokens=13 located=1 fresh=1 OK
L16  tokens=18 located=1 fresh=1 OK
L18  tokens=24 located=1 fresh=1 OK
L18  tokens=19 located=1 fresh=1 OK
L20  tokens=12 located=1 fresh=1 OK
L20  tokens=22 located=1 fresh=0 OK      <- the 75% / 13.5 quote, present in the package copy
L20  tokens=6  located=1 fresh=1 OK
L22  tokens=11 located=1 fresh=1 OK
L22  tokens=17 located=1 fresh=1 OK
L24  tokens=16 located=1 fresh=1 OK
L24  tokens=17 located=1 fresh=1 OK
L32  tokens=8  located=1 fresh=1 OK
quotes=15 located=15 fresh=14
```

15 located quotes, all inside the 6–25-token band, 14 of them absent from the package copy (the item asks for at least two).

Revision notes on the final text: (a) the ground line now marks its last step `Inference:` so no unlabelled inference survives outside the quoted spans; (b) §2's bound direction was corrected — the F3 rule's `N ≥ 3` is a floor on controls and therefore bounds the distinct causes a sweep can have touched only from above, which is the direction the clustering result supports. Both edits left the quote audit unchanged (`quotes=15 located=15 fresh=14`) and the fixture admission unchanged.

## Recheck command (run, count pasted)

```
$ curl -fsSL 'https://arxiv.org/abs/2504.16777' | grep -c 'co-occurring failures that share the same root causes'
3
```

The live page fetched 2026-10-25 was 43,376 bytes and `cmp`-identical to the snapshot:

```
$ stat -c '%s %n' snapshot live-abs.html
43376 …/arxiv-2504.16777-abs.html
43376 /tmp/tameshi-r46-ScribeEntryCluster/live-abs.html
$ cmp -s snapshot live-abs.html && echo IDENTICAL
IDENTICAL
```

`grep -c` counts lines, and the page is minified enough that the phrase appears on 3 lines; the entry says so by pasting the raw count, not by calling it an occurrence count.

## Counter admission (fixture, not the lane)

Fixture repo per bounds: `D=$(mktemp -d) && git -C "$D" init -q`, `git -C "$D" rev-parse --show-toplevel` printed `/tmp/tmp.ecvDkId5vf` = `$D` before the first commit; commits used `-c user.name=ScribeEntryCluster -c user.email=scribe@localhost` on the fixture only. Contents: the real snapshot, the real `measure.py` (so `self_pin=1`), the real package copy, a 13-cell `S258` row citing the snapshot with prefix `28d2954d` and `used-by` = `corpus/knowledge/r6-flaky-failures-cluster.md`, a README indexing the path, and the deliverable copied to `corpus/knowledge/r6-flaky-failures-cluster.md`.

```
$ python3 "$D/.ufo/evidence/round-46/coverage/measure.py" --lane "$D" --rev HEAD
ENTRY corpus/knowledge/r6-flaky-failures-cluster.md
C3_R46: self_pin=1 rows=1 entries=1 indexed=1 covered=1 row_ids=S258 rev=HEAD C3_R46_PASS=false
counter_exit=1
```

`PASS=false` is only `rows=1 < 3` — the fixture carries one row; the entry itself is admitted (`entries=1 indexed=1 covered=1`). First fixture run was refused, and that refusal was a real defect in my first draft:

```
REFUSED corpus/knowledge/r6-flaky-failures-cluster.md no located quote
```

Cause: `QUOTE_RE` in the counter is `"([^"\n]{10,400})"` — a newline inside the quoted span kills the match. The draft wrapped quotes across lines; the rewrite puts every quoted span on one line. A second pass caught a 5-token quote (`share the same root causes`) below the 6-token floor and replaced it with the 8-token span.

Counter selftest, run as allowed (`--selftest`):

```
$ python3 .ufo/evidence/round-46/coverage/measure.py --selftest
… 24 PASS lines …
C3_R46_SELFTEST: cases=24 failed=0
VERDICT: PASS
selftest_exit=0
```

T05 (`not_in_used_by`) is the case that matters for handoff: if the real `S258` row's `used-by` cell does not carry `corpus/knowledge/r6-flaky-failures-cluster.md`, this entry is refused with `not in used-by` no matter how good the quotes are.

## What was dropped or softened from the package copy

| package claim | disposition |
|---|---|
| `CC BY 4.0` licence | **dropped** — `grep -o -i 'CC BY' extract.txt \| wc -l` → 0; the extraction has only the `view license` link (1 occurrence of `license`) |
| `S140, round 5: the same-job rerun misses 9.8 %–16.3 %` | **dropped from this entry** — not in this snapshot; §5 records that no rerun-blindness rate is stated here |
| `preprint …, not a peer-reviewed publication at the time of opening` | **softened** — `grep -o -i 'Journal reference'` → 0, `grep -o -i 'Comments'` → 0; §5 says only that the snapshot states no peer-review status, and lists the venue facts that are visible (`arXiv:2504.16777v1 [cs.SE]`, `Submitted on 23 Apr 2025`, `Wed, 23 Apr 2025 14:51:23 UTC (79 KB)`) |
| `tier A for its own scope` | **dropped** — lane grading, not a statement of the snapshot |
| package id `S195` | **renumbered to S258** per `.ufo/evidence/round-46/assimilation/adoption-map.json` |
| `75% … mean cluster size of 13.5` and `challenging the deep-seated assumption …` | **kept, re-located**; the 75% span is the one quote also present in the package copy (the other 14 are fresh) |
| `Inference:` marks | carried on every lane-meaning step (F3 cause-vs-control count, F8 one-anchor-not-two, §4 survivor/rerun independence) |

## F8 link

Kept, and only from a located sentence: `co-occurring failures that share the same root causes` (8 tokens) is the premise; the step from a shared cause to "two survivors from one cluster supply one anchor, not two" is marked `Inference:` in the entry. No F8 claim rests on anything the abstract does not say.

## Out of scope (not done by this seat)

- `corpus/SOURCES.md` row `S258` — not written; the row seat owns it, and it must carry the snapshot anchor with prefix `28d2954d` and `used-by` including `corpus/knowledge/r6-flaky-failures-cluster.md`.
- `corpus/README.md` index line — not written; L1 adds the backticked `corpus/knowledge/r6-flaky-failures-cluster.md` (or `knowledge/…` form; counter test T16 accepts both).
- The copy into `corpus/knowledge/` — not made; L1 copies after review.
- No deciding run: the counter was exercised only as `--selftest` and against a fixture repo; the lane's deciding run is the L1's.

## Known limits

- The snapshot is the abstract page only; the paper body (PDF/HTML) is linked but was not fetched, so nothing here rests on the full text.
- The abstract carries one aggregate clustering figure and one mean cluster size; it has no per-project cluster rate, no cluster-size distribution, and no data on mutation survivors — §4 states the transfer is inference.
- The live-page `grep -c` is a line count (3), not an occurrence count; a future rewording can keep the count non-zero while changing the sentence, so the recheck instruction is to reopen and re-locate every quote, not to trust the count.

## Tooling

No installs, no upgrades, no pacman. Scratch confined to `/tmp/tameshi-r46-ScribeEntryCluster/`; fixture repo `/tmp/tmp.ecvDkId5vf`. Lane checkout touched only at `.ufo/waves/round-46/w1/ScribeEntryCluster.entry.md` and this report.
