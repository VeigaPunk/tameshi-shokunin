# T55W3SimplReaders — could fewer readers re-key the 18 sections?

Seat: leaf simplifier, wave 3. Attacks the reader-count premise of the re-key: *does the
credit rule need one reader per section, or can one reader bind several sections?*
No lane production file was touched; every run used `git clone --shared` copies at C0
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`; scratch under
`$HYAKU_SCRATCH/tameshi-r55/T55W3SimplReaders` (removed; receipts copied here).

## Verdict

**18 ledger entries and 18 reader report files are required; 18 reader seats are not.**
One reader could have bound all 18 sections. The round spent **21 reader seats** —
**20 over the mechanism minimum, 3 over the deliverable minimum** — and the 3 extra seats
are not merely redundant: under the binder's first-match loop they can **block** the
re-key of the one section that actually changed.

The deciding code is `.ufo/evidence/round-18/measure.py:609-612` (frozen credit rule):

```python
if isinstance(entry.get('sha256'), str):
    by_sha.setdefault(entry['sha256'], []).append(entry)
for sec in sections:
    matches = by_sha.get(sec['sha256'], [])
```

Coverage joins on the **section's content sha**, and an entry carries **exactly one string
sha** (a list sha is not a string, so the entry is silently dropped — fixture D). So one
entry credits one section, and the 18 sections (18 distinct shas, `sections-sha.txt`) need
18 entries. But the entry says nothing about *who* read it: `grep -c seat` over
`.ufo/evidence/round-18/measure.py` and `.ufo/evidence/round-21/coldread/measure.py` is
**0** — the credit algorithm never reads `seats`.

The binder is what adds the per-heading shape, and it adds only a per-*file* shape
(`.ufo/evidence/round-55/integrate/binder.py:101-102`):

```python
if isinstance(d, dict) and isinstance(d.get('heading'), str):
    readers.setdefault(d['heading'], []).append((f, d))
```

A report is indexed by one heading string, matched to one section (`binder.py:113-114`),
and emits one trace + one entry (`binder.py:106`, `:173-187`). A file naming two headings
is not indexed at all (receipt RUN 1: `T55W3TestMulti.json` is never bound). The seat
record on the entry is derived from the **file name**, not an agent identity
(`binder.py:184`: `'seats': [Path(f).stem, 'L1 TameshiR55a2 re-key (round 54)']`).

So: **1 reader deliverable cannot cover 2 headings; 1 reader seat can produce all 18
deliverables.** Nothing in either program can tell eighteen readers from one.

## How many readers the round actually needed

| scheme | seats | ground |
|---|---|---|
| mechanism minimum: one author writes 18 json+md pairs | **1** | RUN 1 binds 3 headings from 3 single-heading files written in one scripted pass |
| one deliverable per heading | 18 | binder.py:101-102, 113-114 |
| independent verdicts preserved (stratified, e.g. 3 readers × 6) | 3 | not required by any code; the only defensible reason to spend more |
| what round 55 dispatched | **21** | 18 (w3 R01–R18) + 3 (w2 Read01–03, all on `## Standing rules`) |

`## Standing rules` was read **4 times at the same C0** (w2 Read01/02/03 + w3 R07). That is
the only in-round duplication; the other 17 seats are the structural one-per-section split.

Round-54 precedent is worse, not better: 23 lost headings, **46 reader seats** — 23 in w1
at cand `59c38109bf11`, then the same 23 in w2 at `99c3bc88d704` (two waves, the second
after fixes). The round-54 binder consumes both waves.

## Excess cost

- **Seats**: 21 vs 1 = 20 excess; vs 18 deliverables = 3 excess.
- **Round size**: 75 + 34 + 32 = **141 dispatched** against the 64–128 band (+13). Not
  dispatching the 20 extra reader seats puts the round at **121**, inside the band. The
  per-section reader split is exactly what pushes the round over its own band.
- **Work per seat**: ~834 portable characters of item text (15,017 over 18 w3 seats), a
  `git show C0:SKILL.md`, a frozen-sectionize extraction, the section itself (9–140 lines
  for these 18), 1–3 pinned inputs, and two files written. Multiplied by 18 that is 18
  independent re-derivations of facts the counter does not check: the binder recomputes the
  section sha itself and rejects a wrong one.
- The **drift is one shared set**: all 17 input-drift sections lost credit to the same
  **14 paths** (three tools, `registry.json`, `SOURCES.md`, `QUALITY.md`, and seven older
  drifts); `## Standing rules` is not input-drift at all. One reader that re-reads the 14
  changed inputs once and then the 18 sections is the minimal work, not 18 readers each
  re-opening the same inputs.

## Correction to the item's premise

"Eighteen sections whose bytes did not change" holds for 17. At C0 the measure reports
`## Standing rules ——> no-ledger-entry` (its bytes *did* change at C0, so the prior entry's
sha no longer matches); the other 17 report `input-drift:…` (`c0-explain.json`,
`counts.tsv`). The section whose bytes changed is also the one the w2 readers found
2 / 3 / 7 findings in.

## Live defect this uncovers (the reason the 3 extra seats are worse than dead weight)

`binder.py:113-127` takes the **first** report in sorted path order and **aborts the whole
heading** on findings beyond `resolutions.json`'s `n`:

```python
for f, d in readers.get(h, []):
    ...
    if len(findings) > allowed:
        skipped.append((h, 'reader-has-findings:%d>%d' % (len(findings), allowed)))
        good = None
        break
```

Sorted paths put wave 2 before wave 3. The live w2 deliverables for `## Standing rules`
carry 2 / 3 / 7 findings at C0, and `integrate/resolutions.json` has **no `## Standing
rules` entry** (`allowed = 0`). Therefore the real binder run will print
`SKIP ## Standing rules reader-has-findings:2>0` and **never look at T55W3R07's clean
report** — reproducing RUN 2 exactly. The three w2 seats read the same bytes as R07, so
they add no independent signal and actively shadow the clean reader. To bind the heading
the L1 must either adjudicate it in `resolutions.json` with `n >= 2` (RUN 3: binds the
*findings-bearing* w2 report, `verdict gap-minor, minor_gaps 2`, and still ignores R07),
or the section must be fixed and re-read — the extra readers cannot help.

## Tradeoff (why not simply one reader)

Keeping the mechanism is free; the only argument for more than one seat is **independence
of findings**, not credit. `corpus/QUALITY.md` criterion 53 requires the affected sections
be "cold-read again by independent seats at its content revision" — independent *of the
author*, not one seat per section. One reader satisfies that literally, but its 18 verdicts
are correlated (one context, one set of blind spots), and `findings` feeds `minor_gaps`
and the findings-veto. The cheap point on the frontier is 2–3 stratified readers (~6
sections each), not 18; any move beyond that pays seats for no new independently measured
fact. Below 1 reader the mechanism cannot represent the result at all: credit is per
section sha, so entries cannot be merged, only authored by the same seat.

## Preserved contract

- Credit predicate, binder and ledger untouched in the lane; all measurements on
  `git clone --shared` copies at C0, `git -C <clone> rev-parse --show-toplevel` asserted
  before any commit there.
- No frozen file, wave spec, or production file written. Writes limited to this report,
  its receipts directory, and scratch.
- Census after the work: `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` exits **0** (140 rows; W04 duplicate-url warnings
  unchanged).
- Tool installs: none.

## Receipts (in `T55W3SimplReaders-receipts/`)

| file | what it shows |
|---|---|
| `driver.py` + `credit-fixtures.out` | the credit rule's binding unit, five fixtures (A–E) |
| `run-receipts.sh` + `binder-runs.txt` | one-author bind, findings-veto, adjudicated bind, floor 46→49 |
| `sections-sha.txt` | start/end/sha of the 18 headings at C0 (frozen round-18 `sectionize`) |
| `counts.tsv` | every number above with its command/source |
| `counts-inputs.tsv` | the binder's pinned-input union per heading (12–7706 paths) |
| `code-lines.txt` | the decisive lines quoted above, with `grep -c seat = 0` |
| `c0-explain.json` | `measure.py --rev C0 --explain`: 17 `input-drift`, 1 `no-ledger-entry` |

Key outputs:

```
$ S=.../T55W3SimplReaders; S="$S" python3 "$S/driver.py"      # credit-fixtures.out
A 4_entries_4_sections          covered 3/4 (preamble has no entry)
B bogus_start_still_credits     covered 3  (Beta entry start=500 still credits: start/end unused)
C one_entry_one_section         covered 1  (one entry -> one section)
D list_sha                      covered 0  (a list sha256 is not a str; entry silently dropped)
E one_entry_two_identical_sections covered 2/2, both shas acceda898c4d
                               (an entry covers several headings ONLY when their bytes are identical)

$ bash "$S/run-receipts.sh" "$S"                              # binder-runs.txt
RUN 1  REKEY ## Standing rules / ### Gate/probe registry / ### Round-13 gate/probe registry
       REFRESH rekeyed=3 skipped=15 headings=18        (T55W3TestMulti.json, two headings, never bound)
RUN 2  SKIP ## Standing rules reader-has-findings:2>0   REFRESH rekeyed=2 skipped=16
RUN 3  REKEY ## Standing rules ... reader=T55W2TestA     REFRESH rekeyed=3 (clean w3 report still unused)
floor  rev f64265d819da covered 49 of 64;  ## Standing rules / ### Gate/probe registry /
       ### Round-13 gate/probe registry -> True credited
base   rev 9cf0146b94dd covered 46 of 64

$ python3 .ufo/evidence/round-21/coldread/measure.py --rev 9cf0146b94dd --explain   # c0-explain.json
covered 46 of 64; the 18 lost headings: 17 input-drift (14 distinct paths), 1 no-ledger-entry
```

## Artifacts opened

`.ufo/evidence/round-18/measure.py` (609-612, 604-660, 209-253, 716-860); `.ufo/evidence/round-21/coldread/measure.py`
(all); `.ufo/evidence/round-55/integrate/binder.py` (all 209 lines); `.ufo/evidence/round-55/integrate/resolutions.json`;
`.ufo/evidence/round-55/c1/lost-headings-at-c0.json`; `.ufo/evidence/round-21/coldread/ledger.json`;
`.ufo/waves/round-55/{spec-w2,spec-w3,w2-dispatch,w3-dispatch}.json`; `.ufo/waves/round-55/w2/T55W2Read0{1,2,3}.json`;
`.ufo/waves/round-54/{spec-w1,spec-w2,reader-section.py}.…`, `.ufo/waves/round-54/w1|w2/T54W*Read0*.json`;
`.ufo/evidence/round-48/quality/coldread-precheck.sh`; `corpus/QUALITY.md` (355-380, 585-600); `SKILL.md` at C0.
