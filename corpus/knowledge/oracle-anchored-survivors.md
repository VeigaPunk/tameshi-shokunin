source: S012 — https://arxiv.org/abs/2608.17214 (Canedo, "Oracles That Cannot Fail"), abstract re-opened 2026-10-22; S090 — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3, §ERRORS EX_USAGE, opened 2026-10-22; S091 — https://git-scm.com/docs/gitrevisions, §SPECIFYING REVISIONS `<sha1>`, opened 2026-10-22; S088 — kumitate `scripts/cite-check.mjs` @ 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a (blob sha256 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f), header comment lines 35, 38, 61, 69 and 71, read-only
verified-at: 2026-10-22; anchors committed in `06a6707904582cc2f268d8a74861c6a8d09dd1fe` before the probe ran; probe run with node v24.21.0, receipt `.ufo/evidence/round-27/f8/receipt.json` (probe sha256 `2d9308ba950c…`, anchors sha256 `780e1009fc48…`, both checked by `.ufo/evidence/round-27/c2-measure.py`)
recheck: `python3 .ufo/evidence/round-27/f8/anchor-probe.py --kumitate <fleet>/kumitate-shokunin --anchors .ufo/evidence/round-27/f8/anchors.json --out /tmp/r.json` → `ANCHOR_PROBE: ran=4/4 anchored_holes=4`; reopen S012, S090, S091; a new pin of `cite-check.mjs` needs new anchors (header line numbers move)
ground: F8 — oracle anchoring as a survivor class (`corpus/README.md` frontier F8: "0 test-oracle lines → one survivor classified against an independently anchored expectation"); this entry classifies four survivors on one gate.

# Oracle-anchored survivor classification — cite-check holes (round 27)

## 1. The question

Round 26 called four of the five `cite-check.mjs` survivors suite holes
(`mutation-case-kumitate-cite-check.md` §4). Each call rests on an off-suite
witness that runs the pristine and the mutant and finds a difference. The
pristine output is the expected value. S012 names that kind of expectation
**state-anchored**: it "flows, directly or transitively, from" the code under
mutation, so if the pristine were itself wrong on the witness input, the
differential would still report a hole, and it would also report a hole when
the mutant is the correct one. A **specification-anchored** expectation is
"composed from values fixed outside the code under mutation" (S012 abstract).

This entry re-judges the four holes with specification-anchored expectations
and records which anchor holds each one.

## 2. Method (executed)

1. For each survivor, write the expected exit status and finding kind from
   anchors outside the mutated statement, before any run
   (`.ufo/evidence/round-27/f8/anchors.json`, committed in `06a6707`):
   - **contract**: a header comment line of the pinned blob. The mutated
     statements are code lines, so no survivor edit moves the anchor.
   - **external**: a SOURCES row opened this round.
   - **arithmetic**: a fact the probe computes from the witness bytes it
     wrote (here, the newline count of the cited file).
2. Run the pristine and the mutant on the survivor's witness tree under
   `env -i` (`.ufo/evidence/round-27/f8/anchor-probe.py`). Compare each run
   with the anchored expectation, not with the other run.
3. Class: `anchored-hole` when the pristine meets the anchor and the mutant
   does not; `anchor-disagrees-with-pristine` when the pristine misses it (a
   gate defect, or a wrong anchor); `mutant-meets-anchor` otherwise.

## 3. Results

| survivor | witness | anchored expectation | anchors | pristine | mutant | class |
|---|---|---|---|---|---|---|
| S_OOR_EDGE | cite line 21 of a file the probe wrote with 20 newlines | exit 1, `LINE_OOR` | arithmetic (20 lines); header :61 (`LINE_OOR` is an error), :69 (error → exit 1) | exit 1, `LINE_OOR` | exit 0, none | anchored-hole |
| S_STRICT | `--strict`, one doc with one ownerless ref | exit 1, `ORPHAN_REF` | header :35 (ownerless ref is `ORPHAN_REF`, warn), :69 (warn under `--strict` → exit 1) | exit 1 | exit 0 | anchored-hole |
| S_USAGE | unknown flag | exit 64 | header :71 (`64 usage error.`); S090 (`EX_USAGE (64)` … "a bad flag") | exit 64 | exit 65 | anchored-hole |
| S_PIN_INCLUDES | content pin = digest chars 8–20 | exit 1, `PIN_MISMATCH` | header :38 (7–40 hex only); S091 (a short name is a leading substring) | exit 1, `PIN_MISMATCH` | exit 0, none | anchored-hole |

`ANCHOR_PROBE: ran=4/4 anchored_holes=4` (`.ufo/evidence/round-27/f8/probe.stdout`).

## 4. What this changes

- The four hole calls of round 26 no longer rest on the pristine alone. In
  each case the pristine agrees with an outside anchor and the mutant breaks
  it. The differential and the anchored oracle agree on all four, so no
  round-26 call flips.
- Anchor strength differs and is recorded, not averaged. Three survivors are
  held by the gate's own written contract (S_OOR_EDGE also by arithmetic,
  S_USAGE also by S090). **S_PIN_INCLUDES is held by convention only**: the
  header fixes the pin length, and the prefix rule comes from Git's
  abbreviated-name convention (S091), applied to a content sha256 by analogy.
  A gate owner could declare substring pins legal, and the hole would become
  a contract change, not a defect.
- The fifth survivor, S_EMPTY_GUARD, stays an equivalent mutant on the
  round-26 argument; anchoring cannot help there, because no input separates
  the two programs.
- Recipe value for the lane: a hole call needs an expectation the mutant
  cannot move. Before calling a survivor a hole, name its anchor; when the
  only anchor is the pristine run, say "differential hole" and route it to
  the gate owner as unanchored.

## 5. Bounds

- One gate, one pin, four survivors. No claim about other legs: their hole
  calls (rounds 16–26) remain differential until anchored.
- The probe checks exit status and the presence of one finding kind. It does
  not check message text or the JSON totals.
- Header comments are written by the same owner as the code. They are fixed
  outside the mutated statement, which is what S012's definition needs, but
  they are not an independent specification document.
- S012 is a single-system, single-author preprint (tier B). This entry uses
  its definitions, not its measured rates.
