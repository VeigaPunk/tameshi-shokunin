# L1 Tameshi R42 W1 — ScribeEntryPit

Draft of the re-grounded lane entry `corpus/knowledge/pit-outcome-vocabulary.md` (fenced block below). Read-only seat: no lane checkout edits; only this report file written.

## Findings

1. **All five quotes verified verbatim** against freshly fetched pages (access date 2026-10-25). Snapshots saved to `/tmp/tameshi-r42-ScribeEntryPit/`:
   - `basic_concepts.html` — 12155 bytes, sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a`
   - `faq.html` — 20845 bytes, sha256 `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1`
   - Command: `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' -o /tmp/tameshi-r42-ScribeEntryPit/basic_concepts.html && curl -fsSL 'https://pitest.org/faq/' -o /tmp/tameshi-r42-ScribeEntryPit/faq.html && wc -c ... && sha256sum ...`
2. **Quote grounds** (exact grep hits in the snapshots):
   - `For each mutation PIT will report one of the following outcomes` — `basic_concepts.html` §"Running the tests" (list follows: Killed, Survived, No coverage, Non viable, Timed Out, Memory error, Run error).
   - `<strong>Survived</strong> means the mutation was not detected by the covering test` — §"Survived".
   - `<strong>No coverage</strong> is the same as <strong>Survived</strong> except there were no tests that exercised the line of code where the mutation was created` — §"No coverage".
   - `Pitest works hard to be fully deterministic, but two factors might cause the results to differ slightly between two runs with the same input` — `faq.html` §"Is it random?".
   - `a mutant may be detected as timed out on one run, but killed or surviving on another` — §Timeouts (line-wrapped in HTML source, contiguous in rendered text; verified with `grep -zo ... | tr '\n' ' '`).
3. **Boundary claim re-checked**: `https://pitest.org/quickstart/mutationcoverage/` still returns HTTP 404. Command: `curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' 'https://pitest.org/quickstart/mutationcoverage/'` → `404 https://pitest.org/quickstart/mutationcoverage/`. Boundary section kept as-is.
4. **Header ids**: adopted rows S155 (basic concepts) / S156 (FAQ) per task template; staged ids cited only as `staged:S159` / `staged:S160` in the body (original raw `S159`/`S160` inline cites removed).
5. No tools installed or updated (system `curl`/`grep` sufficed; no install record).

## Draft entry (fenced)

```
---
source: S155 — https://pitest.org/quickstart/basic_concepts/ — §"Running the tests" → §"Survived" §"No coverage" — fetched 2026-10-25
source: S156 — https://pitest.org/faq/ — §"Is it random?" → §Timeouts — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: F1
---

# A mutation score's denominator is a choice of outcome class, and one of those classes is not stable across runs

## What the sources state

- PIT's own documentation defines a seven-way outcome vocabulary: Killed,
  Survived, No coverage, Non viable, Timed Out, Memory error, Run error
  (`staged:S159`). It separates two classes a reader of a report could easily
  merge: "Survived means the mutation was not detected by the covering test",
  while "No coverage is the same as Survived except there were no tests that
  exercised the line of code where the mutation was created" (`staged:S159`).
- PIT's FAQ states that it "works hard to be fully deterministic, but two
  factors might cause the results to differ slightly between two runs with
  the same input", and names the timeout class as the mechanism: "a mutant
  may be detected as timed out on one run, but killed or surviving on
  another" (`staged:S160`).

## What this means for the lane's report semantics

- **The lane's held Stryker semantics and PIT's semantics are not the same
  lattice.** The lane holds Stryker's score definition (its own held S001:
  score = detected ÷ valid, with compile and runtime errors excluded) but
  does **not** hold PIT's outcome vocabulary. Observation: PIT's "no
  coverage" is a *distinct class* from "survived" even though it sounds like
  a special case of it, and "timed out" is a class whose membership depends
  on machine load (`staged:S160`). Inference: a report that states one number
  without stating which outcome classes entered its denominator cannot be
  compared with a report from the other tool — which is exactly the lane's
  F1 interoperability question, now answerable in the negative for at least
  one pair.
- **The lane's own convention has a known hole.** The lane's recorded
  convention treats a timeout as a detection (its held S001 semantics).
  `staged:S160` shows that a timeout classification is not stable across runs
  under load. Inference: the lane's score can move without any code change.
  This is a finding about the lane's convention, grounded in the vendor's own
  documentation; it is **not** a measurement of the lane's gates, and the
  fix (exclude timeouts, or record the load condition) is not made here.
- **What a report must publish.** The seven classes of `staged:S159` give a
  concrete answer to the lane's F1 "report interop" question: publish the
  outcome classes and their denominator, not just the percentage.

## Boundary of this entry

- PIT's vocabulary is PIT's; the lane holds Stryker's separately. This entry
  records the two vocabularies side by side and does not claim they can be
  mapped onto each other.
- The current PIT path `pitest.org/quickstart/mutationcoverage/` returns 404;
  the two pages opened here are the live carriers of the outcome and
  metric definitions, and they must be re-pinned on a later round.

---
```

## Could not check

- Nothing material: both source pages fetched live today, all quotes grepped verbatim from the saved snapshots, and the 404 boundary claim re-confirmed. The S155/S156 adoption numbers are taken from the task template and the round contract's assimilation section (adopted rows would be S155=S159, S156=S160); final numbering is the main agent's cutover decision.
