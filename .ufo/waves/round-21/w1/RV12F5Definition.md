partial — the seven-profile matrix is a defensible extension, but the nine-surface population and receipt acceptance do not yet faithfully establish the F5 move.

# RV12 F5 definition review

**Axes:** coverage (which selftests are measured) and calibration (what the measurement supports).

## Findings

### Major — the nine surfaces are not an unambiguous operationalisation of “the six gate selftests”

`corpus/README.md:82` defines F5’s next move as measuring “the six gate selftests the same way”; it does not name those six. The contract names nine surfaces (`.ufo/evidence/round-21/c2-contract.json:24-33`): the H3 runner at line 25, six gate files at lines 26-31, and two more at lines 32-33 (`round-gate.mjs`, `sources-check.mjs`).

One documented reading of “six gates” is the six measured fleet gates: Kimi census, surface census, tsukuroi census, mado verify, checklist run, and claims check (`corpus/knowledge/fleet-kill-rate-ledger.md:43-48,272-277`). The contract includes those six, plus the runner and two additional surfaces. On that reading, 9 is an explicit scope expansion, not an inflated count **if** the result is reported as nine and the two additions are identified as extras.

There is also a distinct documented six-suite population: Kumitate’s six hermetic suites (`corpus/knowledge/gates-survey-kumitate.md:1,19-26`). Of those, the contract includes only `kimi-census`, `claims-check`, and `round-gate`; it omits `cite-check`, `surface-probe`, and `proxy-check`, while adding other lanes’ gates and `sources-check`. If this is the intended F5 population, the receipt is both incomplete and broadened. The F5 row alone does not resolve these two meanings. Therefore `classified 9/9` is coverage of the frozen list, not proof that the six F5 gates have all been covered.

**Recommendation:** name the intended six by path in the contract or the F5 row. If the intended set is the fleet-ledger six, retain the nine only as “six target gates + the H3 reference runner + two explicitly additional gates,” and report those counts separately. If it is the Kumitate survey six, cover all six or explicitly revise the F5 scope before claiming closure.

### Major — accepted receipts can classify failed invocations as invariant and can normalize away differences

The contract allows hashes “after the tool’s declared normalization” and requires only a normalization field (`c2-contract.json:18`). The frozen F5 profile protocol specifies unnormalized output (`normalization: none`). The counter checks only that `normalization` is a string (`.ufo/evidence/round-21/c2-count.py:61`); it then requires tuple-shaped values and checks the classification rules (`:63-83`), but does not require the baseline `--selftest` to have succeeded or show that the suite ran. A uniform usage/error response can therefore be classified `invariant`; a lossy declared normalization can mask output changes while still satisfying the counter.

The H3 evidence demonstrates the stronger reference: the scrubbed runner selftest reported 80/80 pass and `VERDICT: PASS`, exit 0, empty stderr, and line-identical full stdout (`.ufo/evidence/kaika-round-1/capability-demo/README.md:85-92`). It is evidence for that one runner/pair of environments, not the other gates.

**Recommendation:** freeze `normalization` to `none` and have the counter reject any other value. Require the clean baseline to demonstrate successful selftest completion (exit 0 plus the target’s recognized pass/count signal); keep failures in variant profiles as measured sensitivity rather than discarding them. Preserve exit and both raw-stream hashes in every tuple.

### Moderate — seven profiles are a reasonable strengthening, not a universal hermeticity test

The contract defines host, clean, clean-repeat, TZ, locale, HOME, and terminal/columns profiles (`c2-contract.json:9-22`). H3 established only host versus one scrubbed environment for the runner; the seven profiles add controlled one-variable probes and a clean repeat, which is directly relevant to F5 and F3. This is not inherently inflation when stated as a larger, explicit profile set. It is also not a full environment matrix: the profile variants are individual perturbations, clean is repeated only once, and the result says nothing about untested variable combinations, operating systems, or runtime/toolchain versions.

**Recommendation:** describe the outcome as differential classification at the seven named profiles, for the exact pinned files—not as proof of universal hermeticity or independence from every environment.

### Minor — source-entry acceptance is broader than F5 provenance

F5 lists candidate sources S015, S016, and S028 (`corpus/README.md:82`; `corpus/SOURCES.md:26-28,39`). S015 and S016 are queued; S028 is mined. But `c2-count.py:110-126` accepts a `source:` header containing *any* mined S###, including a source unrelated to F5. That can satisfy `f5_entry` without grounding this specific lesson.

**Recommendation:** require the entry to cite a mined F5-relevant source (currently S028, or a relevant candidate once mined), not merely any mined row.

## Honest Core statement

> For the explicitly listed and pinned surfaces, the tool records exit status and unnormalized stdout/stderr hashes under the seven named profiles, and classifies each result as invariant, environment-sensitive, or nondeterministic according to the frozen comparison rules. The initial target set is the six named fleet-ledger gates; the runner is the H3 reference and any other gates are reported as additional coverage. This is a measurement capability over those exact revisions and profile conditions.

It may say which surfaces were classified and what each classification was. It must **not** say that all surfaces are invariant unless the receipts show that; that every gate in the repository/fleet is covered; that the result proves universal hermeticity; or that `9/9` means the six-gate F5 target was closed without naming the population. Classification coverage is not a green result for every selftest.

## Verification gaps / commands

- No selftests, C2 counter, or environment-profile executions were run for this review; no command exit codes are available. This is a frozen-document review, not an execution result.
- Evidence read: `corpus/README.md:82`; `.ufo/evidence/round-21/c2-contract.json:3-36`; `.ufo/evidence/kaika-round-1/capability-demo/README.md:80-92`; `corpus/knowledge/fleet-kill-rate-ledger.md:43-48,272-280`; `corpus/knowledge/gates-survey-kumitate.md:1,19-31`; `.ufo/evidence/round-21/c2-count.py:43-83,110-126`; `corpus/SOURCES.md:26-28,39`.
