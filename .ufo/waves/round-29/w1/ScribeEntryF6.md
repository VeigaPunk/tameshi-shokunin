# Survivor fixture minimization — B5 probe, delta debugging
source: S024 (https://www.fuzzingbook.org/html/Reducer.html, re-opened 2026-10-23)

## Frontier question
F6 is open: the `corpus/README.md:83` row asks to move from an unmeasured B5 probe fixture to a reduced fixture plus a kill check. The Round-29 pre-registration (`corpus/README.md:440-447`) names survivor B5 of the kagi surface-census leg and calls for delta debugging that retains the kill and reaches 1-minimality. The frozen v2 counter defines that check at line granularity for the four fixture files.

## Source lesson
S024 presents delta debugging as reducing a failure-inducing input while retaining the outcome recognized by its test. It describes 1-minimality in its character-level example: “Its result is 1-minimal, meaning that every character contained is required to produce the error.” This fixture uses the counter's line units instead; the quoted character-level property does not imply byte-level minimality here.

## Why B5 survives
The earlier kagi census note says B5 deletes the `exec` x-bit check at `surface-census.sh:214-217`. Its suite fixture creates an executable `exec` row but never removes its execute bit, so the deleted arm is not reached (`mutation-case-kagi-census.md:107-116`). The separate B5 probe receipts show the distinguishing case: pristine reports `SURFACE DIVERGED ... (declared exec, no execute bit)`; the mutant reports `SURFACE OK ... (exec 644)` (`.ufo/evidence/kaika-round-1/coldread/B-probe-B5-pristine.txt:1-2`; `B-probe-B5-mutant.txt:1-2`). The old recipe also records the deleted four-line block and sensitivity-check expectations (`mutation-case-kagi-census.md:225-226,248-254`). These receipts explain the target behavior; they do not establish the result of the new round-29 fixture.

## Frozen fixture method and guard
The v2 counter requires `original/census.tsv` to be byte-identical to the pinned kagi declaration; every original shapes and baseline line must occur in the corresponding pinned declaration. Its `Oracle.kills()` materializes the fixture, runs the pinned pristine gate, and accepts only exit 1 plus a `SURFACE DIVERGED` line containing `(declared exec, no execute bit)`. Only then does it run the B5 mutant built from the runner's own `@defect B5` specification and require exit 0. Thus a reduction preserving a different failure is not counted as a B5 kill (`c2-measure-v2.py:10-22,149-180,240-265`).

`ddmin()` applies the frozen complement-form delta-debugging loop to the original units. The committed minimized units must exactly match that reducer output; removing any one minimized unit must lose the kill (`c2-measure-v2.py:183-202,260-271`). The `host.tsv` manifest has one tab-separated node per line: relative path, `dir` or `file`, octal mode, and content. The counter rejects invalid, duplicate, absolute, or parent-traversal paths and does not create symlinks (`c2-measure-v2.py:29-33,114-147`).

A unit is one line of `census.tsv`, `shapes.tsv`, `baseline.tsv`, or `host.tsv`, including blank lines. Consequently, 1-minimal means no single such line can be removed while preserving the oracle's B5 kill; it says nothing about bytes within a line or about a globally smallest fixture. In particular, a host manifest line is the unit even though it describes a host node.

## Result slots
The builders have not published results yet. Fill these from BuildF6A/B; do not infer them from the older probe receipts:

`units_original=<from BuildF6A/B>`
`units_minimized=<from BuildF6A/B>`

No round-29 fixture outcome or C2 predicate result is claimed here. F6 remains open absent the frozen counter result.

## Scribe evidence and bounds
- Read-only sources: `corpus/README.md:83,440-447`; `corpus/knowledge/mutation-case-kagi-census.md:107-116,225-226,248-254`; both B5 receipts; `corpus/lessons/round-29.md:23`; `.ufo/evidence/round-29/contract-amendment-1.json:12-21`; `.ufo/evidence/round-29/c2-measure-v2.py:10-39,103-202,240-304`; and the S024 snapshot around its 1-minimal passage.
- Provenance qualification: the required source line follows the frozen source metadata. The round-29 lesson records `curl -sL` and a fetch at `2026-10-23T01:09Z`; I read the committed snapshot and did not fetch the live URL.
- Commands run by this scribe: none. The frozen gate command is `python3 .ufo/evidence/round-29/c2-measure-v2.py --repo CLONE --rev REV`; it was not run here. No tests, sweeps, builds, or product edits were made.
- Touched surface: this report only. No product, fixture, registry, lesson, or counter file was edited; no tools were installed.
- Out of scope: building/integrating the fixture, running C2, changing the source registry or making an F6 status/promotion claim. The L1 integrator owns those steps.
