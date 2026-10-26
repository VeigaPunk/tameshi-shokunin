# T47ScribeEntryCost — C3 entry draft for S264 (ICST 2024 flaky-cost case study)

Seat: T47ScribeEntryCost, leaf, no dispatch. Item: draft the re-grounded knowledge entry
`corpus/knowledge/r8-flaky-cost-baseline.md` (staged S207 → adopted S264) as a wave deliverable.

## Behavior

Wrote one deliverable file, 9,478 bytes, 47 lines, sha256
`d2bd183573fc8da04ed0ff5c2f0874f48389a0f94e4ddac984145b9cb2f41aad`:

- `.ufo/waves/round-47/w1/T47ScribeEntryCost.entry.md`

Nothing else in the lane was touched. Scratch under `/tmp/tameshi-r47-T47ScribeEntryCost/`
(`abstract.txt`, `abstract_wrapped.txt`). No git or jj command was run in the lane, no fixture repo was
created, no tool was installed or upgraded (none needed; the pacman guard was irrelevant because
nothing was installed).

Entry shape follows the lane's other entries (`corpus/knowledge/r9-false-red-rate.md` read as the
convention sample): the required provenance trio, then `ground: F3 …`, then a `#` title, then
`## What the snapshot states`, `## What is inferred`, `## What is not claimed`. Header lines 1–3 are
byte-exact to the item's specification:

- line 1 `source: S264 — https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=title%2Cabstract%2Cyear%2Cvenue%2Cauthors%2CexternalIds — abstract field — retrieved 2026-10-25` (compared byte-for-byte, equal)
- line 2 `verified-at: 2026-10-25`
- line 3 `recheck: 180d — …` (sha256 re-fetch to `6ab5b3f5…de06` plus a `grep -c 'Automatically rerunning a test costs 0.02 cents'` probe)

## Gates I ran (seat-level, none is a verdict)

1. **Snapshot digest.** `sha256sum .ufo/evidence/round-47/coverage/sources/s2-icst24-cost-of-flaky.json`
   → `6ab5b3f58b27827c265422f958689bbeda4514286a532b3ce2f4a6b720bfde06`, equal to the digest named in
   the item. The snapshot is one JSON line, 3,116 bytes, so the entry cites fields, not line numbers.
2. **Counter predicate, imported read-only.** Loaded `.ufo/evidence/round-47/coverage/measure.py` with
   `importlib` (no run, no `--rev`, no `--selftest`) and called its own `entry_ok` against a synthetic
   row `S264` whose `text` is `norm_text(snapshot)` and whose `used` contains
   `corpus/knowledge/r8-flaky-cost-baseline.md`:
   `entry_ok(...) -> (True, 'ok', ['S264'])`.
3. **Quote audit under the counter's own `fold`/`QUOTE_RE`.** 19 located quotes of 6–25 whitespace
   tokens (max 24), of which 16 are absent from the package copy — well past the "≥1 located, ≥1 fresh"
   floor. Three located quotes are non-fresh by construction: the title (11 tokens), the 2.5 % floor
   sentence (20 tokens) and the "Contrary to most other studies" sentence (17 tokens), all of which the
   package copy already carries.
4. **Cost-figure locations.** Every figure in the entry names its location: 2.5 %, 1.1 %, 1.3 %, 0.1 %,
   0.02 cents, $5.67, each cited to field `abstract` of the single-line snapshot. The only arithmetic is
   the ratio, explicitly labelled `[INFERENCE]` with its inputs (5.67 USD, 0.02 cents = 0.0002 USD).
5. **Not run:** the deciding counter, the no-harm script, the C1/C2 counters, and the census. Measurement
   bounds respected (no `--rev` run into any work dir).

## Findings

1. **Carrier defect confirmed, and the brief's premise is wrong in one part.** `venue` reads
   "International Conference on Information Control Systems & Technologies", which the DOI
   (`10.1109/ICST60714.2024.00037`) and DBLP key (`conf/icst/LeinenEPSSJ24`) do not support. The item
   also says "the abstract's own text name the ICST 2024 paper"; it does not: `abstract` contains
   neither "ICST" nor "Conference". "ICST" occurs in the snapshot only inside `externalIds.DOI`, and
   "Conference" only inside `venue` itself (verified by substring counts over the raw bytes). The entry
   reports this verbatim and cites the DOI plus `abstract` only; no venue is claimed.
2. **The package's ratio is wrong by two orders of magnitude.** The package copy prints "~280×" for
   `$5.67 / 0.02 cents`. 0.02 cents is $0.0002, so the ratio is 28,350; ~280 is what you get by dividing
   by 0.02 *dollars*. The entry states the corrected value as `[INFERENCE]` with its inputs and says why
   the package figure was not carried. This is a real numeric defect in the shipped package copy, not a
   style issue.
3. **The package cites a row that does not exist.** Its "S205 (over 95 % of individual test failures
   still reported)" cross-reference has no row: `grep -n 'S205' corpus/SOURCES.md` returns nothing, and
   the abstract states no such figure. The claim is dropped and the drop is recorded in the entry's
   "not claimed" section.
4. **Ground moved from F7 to F3 as the contract requires.** The package opened `ground: F7 (the cost
   baseline a re-sweep cadence trades against)`; the round-47 contract places this surface in F3's
   measurement half, so the entry grounds F3 and makes no F7 claim. The F7 relevance is stated inside
   the F3 ground line as a relation, not as a frontier move.
5. **Two fresh, load-bearing statements the package did not carry**, both located in `abstract` and
   absent from the package copy: the studied project "led to the decision to shift effort from
   investigation and repair to automatically rerunning tests" (23 words), and "Our cost model can help
   practitioners analyze the cost of flaky tests in their context" (15 words). The first is what makes
   the row a policy datum rather than only a price; the second is what limits it to a context-local
   measurement.
6. **The denominator ambiguity is recorded, not resolved.** The abstract's "1.1% of the total time
   spent" does not say total of what. The entry notes that `1.1 + 1.3 + 0.1 = 2.5` reproduces the stated
   "at least 2.5 %" floor (`[INFERENCE]`, inputs given), which is the only consistent reading, and marks
   the wording as ambiguous rather than silently sharpening it.
7. **The "at least 2.5 %" is a floor that includes tooling.** The 0.1 % share is monitoring-tool work, so
   the floor already contains the cost of building observability — stated as `[INFERENCE]` with the
   three inputs. The entry draws no claim about the lane's own monitoring cost.

## Integration requirements (for the seat that lands the corpus files)

The entry only passes the counter when the other C3 pieces exist at the deciding revision; none of
these exist yet at this seat's read (`grep -n 'ICST60714' corpus/SOURCES.md` is empty, and both
`corpus/knowledge/r8-flaky-cost-baseline.md` and its `corpus/README.md` index line are absent):

- `corpus/SOURCES.md` row **S264** with `status` `mined`, the DOI URL as the first URL in the source
  cell, a snapshot path under `.ufo/evidence/round-47/coverage/sources/` plus an 8+-hex sha256 prefix
  `6ab5b3f5` in the anchor cell, **and** the used-by cell listing
  `corpus/knowledge/r8-flaky-cost-baseline.md` verbatim (the counter's `path in rows[c]['used']` test).
- The deliverable copied to `corpus/knowledge/r8-flaky-cost-baseline.md` unchanged (its line 1 must keep
  citing `S264`).
- An index line in `corpus/README.md` carrying the backticked path `corpus/knowledge/r8-flaky-cost-baseline.md`.

## Out of scope / not done

- Did not add the S264 registry row, copy the entry into `corpus/knowledge/`, or edit `corpus/README.md`:
  those are sibling C3 deliverables and the seat is read-only outside its own two files.
- Did not open the IEEE page or the mediaTUM open-access PDF; only the committed snapshot was read. The
  package's retrieval narrative (JavaScript shell, timed-out fetches) is not restated in the entry because
  this seat did not run those attempts.
- Did not verify the record's `abstract` is verbatim against the publisher; the entry says so only as a
  limit ("verbatim-ness … not verified" is implicit in "only the `abstract` field was read" and the venue
  defect note). No tier/score claim is made by this seat.
- No re-run of any deciding counter; the C3 verdict remains the L1's to take.

## Artifacts

- `.ufo/waves/round-47/w1/T47ScribeEntryCost.entry.md` — deliverable (sha256 `d2bd1835…2f41aad`, 9,478 bytes, 47 lines)
- `.ufo/waves/round-47/w1/T47ScribeEntryCost.md` — this report
- `/tmp/tameshi-r47-T47ScribeEntryCost/abstract.txt`, `/tmp/tameshi-r47-T47ScribeEntryCost/abstract_wrapped.txt` — scratch copies of the snapshot's `abstract` field (scratch only, not part of the record)
