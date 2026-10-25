# Scout: PIT FAQ and equivalent / unkillable mutants — round 43, wave 1

**Question.** Does the PIT FAQ say anything about equivalent or unkillable mutants, and is the
live page still the committed snapshot (`ccf6ac49…`)?

**Answer.** It says nothing. There is **no such text** on the page — no "equivalent", no
"unkillable", no statement that a mutant cannot be killed. The live page is **byte-identical**
to the committed snapshot.

## 1. Live page vs. committed snapshot — MATCH

| Property | Value |
|---|---|
| Committed snapshot | `.ufo/evidence/round-42/sources/pit-faq.html` |
| sha256 snapshot | `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1` |
| sha256 live (`curl -fsSL https://pitest.org/faq/`) | `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1` |
| Bytes / lines | 20845 B / 434 lines, both copies |
| `cmp` live vs snapshot | identical (no output); `diff` line count `0` |
| HTTP | `200`, `content-length: 20845`, `ETag: "6a1fe9b1-516d"` (= 20845 B), `last-modified: Wed, 03 Jun 2026 08:45:37 GMT` |
| Fetch stability | two consecutive fetches, same sha256 (`cmp` → STABLE) |
| Title | `FAQ` (line 5) |

The full hash matches the prefix `ccf6ac49` in the item, the committed manifest
`.ufo/evidence/round-42/sources/sha256.txt:2`, and the locator header of
`corpus/knowledge/pit-outcome-vocabulary.md:2`.

Scratch: `/tmp/tameshi-r43-ScoutPitEquiv-live/{live.html,live2.html}` (deleted after this report;
the committed snapshot is the durable copy).

## 2. Located evidence of absence

Counts over the snapshot, case-insensitive, whole file (live copy identical, so the same counts):

```
equivalent       0      unkillable       0      "equivalent mutant"  0
"never be killed" 0     "cannot be killed" 0    "can't be killed"    0
"can not be killed" 0   impossible       0      undetectable         0
vanity           0      "no test can"    0
```

The only `http-equiv` hit is the charset meta at line 3, i.e. not the word "equivalent".
The page has 24 `<h2>` and 5 `<h3>` headings (lines 76–358; `grep -c` = 24 / 5); none is about equivalent
mutants, surviving mutants, or unkillable mutants.

The kill/survive vocabulary occurs for a not-killed mutant in exactly two places — lines 223
and 299 — and neither is about equivalence:

```
223:<h2 id="i-have-mutations-that-are-not-killed-but-should-be">I have mutations that are not killed but should be</h2>
299:but killed or surviving on another.</p>
```

## 3. Nearest section (two located quotes, ≤25 words)

**§"I have mutations that are not killed but should be"** — heading `pit-faq.html:223`, body
225–231. This is the nearest section, and it explains *compiler-inlined `finally` blocks*,
not equivalence.

> "Are the mutations in finally blocks? Do you seem to have two or more identical mutations, some killed and some not?" — `pit-faq.html:225` (21 words, `grep -F` hits 1)

> "Most test suites are only able to kill one of these mutations." — `pit-faq.html:229` (12 words, `grep -F` hits 1)

The paragraph's own cause (`pit-faq.html:227–229`): the Java compiler copies a `finally` block
"for each possible exit point" and "PIT creates separate mutations for each of the copied
blocks". So the FAQ's non-killed mutant is a *duplicate the suite has no reason to reach*,
not a mutant that is behaviourally identical to the original. No equivalence claim, no
"unkillable" claim, no guidance to retire such a mutant.

Second-nearest use of "surviving" is §Timeouts, `pit-faq.html:295–299`, where survival is a
*run-to-run variance* statement, not a property of the mutant:

> "so a mutant may be detected as timed out on one run, but killed or surviving on another." — `pit-faq.html:298–299` (18 words)

Machine rechecks (run this session, both exit 0):

```
$ curl -fsSL https://pitest.org/faq/ | grep -c -i 'equivalent'          # 0
$ curl -fsSL https://pitest.org/faq/ | grep -c 'Most test suites are only able to kill one of these mutations.'   # 1
```

## 4. Where the equivalence statement actually is (depth note)

The FAQ being silent does **not** mean the lane lacks a located statement — it is in a source
this lane already committed, `S158`, and it is currently uncited:

> "Mutation is equivalent to the un-mutated code. Treated as detected although by definition it cannot be." — `.ufo/evidence/round-42/sources/pit-DetectionStatus.java:71–72` (16 words; javadoc block 70–75, constant `EQUIVALENT(true)` at line 75)

That is the Javadoc of `DetectionStatus.EQUIVALENT(true)` (`pit-DetectionStatus.java:70–75`),
and it is the strongest PIT-side statement the lane holds on the class: the tool *names*
equivalence, treats it as `detected` (so `isDetected()` excludes it from the score by
construction), and says it "cannot be" detected. `grep -rn EQUIVALENT corpus/ .ufo/evidence/round-42/ .ufo/waves/round-42/w1/*.md`
returns only `pit-DetectionStatus.java:75` — the lane's
`corpus/knowledge/pit-outcome-vocabulary.md` uses S158 only for `RUN_ERROR`/`isDetected`
(lines 4, and the S158 bullet), not for `EQUIVALENT`.

## 5. Load-bearing check on existing lane text

- `corpus/SOURCES.md:126` (S156, the FAQ row) claims only run-dependence: "two factors,
  timeouts and static initializers, can make results differ between runs…". No equivalence.
- `corpus/knowledge/pit-outcome-vocabulary.md:2` cites S156 for §"Is it random?" → §Timeouts only;
  line 3 cites S158 for the enum, and the `EQUIVALENT` constant is never mentioned.
- `grep -rn -i -E 'unkillable|un-killable' corpus/` → no hits.

So no lane claim about equivalent/unkillable mutants rests on the FAQ, and nothing needs
retracting. If a round wants a PIT-side equivalence citation, use
`pit-DetectionStatus.java:71–72`, not the FAQ.

This reproduces, independently and on 2026-10-25, the earlier finding recorded at
`.ufo/waves/round-26/w1/OpenEquivalentSource.md:76–83` ("The FAQ has no equivalent-mutant
section: its nearest entry, 'I have mutations that are not killed but should be', explains
compiler-inlined `finally` blocks, not equivalence").

## 6. Confidence and remaining unknowns

- **High confidence** on the headline: absence was tested with 11 literal phrases plus a
  full-file scan for `equiv`, and the live page is byte-identical (full sha256), so the
  absence is a property of the current page, not of an old copy.
- **High confidence** on the live/snapshot match: `cmp` identical, ETag length equals byte
  count, `last-modified: 2026-06-03` precedes both the round-42 fetch (2026-10-25 09:35Z,
  `sources/opened-at.txt`) and this one.
- **Unresolved (out of this item's scope):** whether any *other* PIT page (mutators,
  incremental analysis) states equivalence. Not opened here. Also unresolved: whether
  `EQUIVALENT` is ever *emitted* by the current PIT runtime — the enum declares it and treats
  it as detected, but this item did not trace `DetectionStatus.EQUIVALENT` to a producer
  (no caller search was in scope; the snapshot is the enum file alone).

Tooling: no installs or upgrades; `curl`, `grep`, `sha256sum`, `cmp`, `awk` from the host.
