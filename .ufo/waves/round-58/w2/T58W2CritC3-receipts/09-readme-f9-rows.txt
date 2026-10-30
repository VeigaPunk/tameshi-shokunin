Receipt 09 — item (d): F9 README row, base vs C0, plus coverage-map rows
Command (cwd clone):
  git show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/README.md | grep -n '^| F9'
  grep -n '^| F9' corpus/README.md
  grep -n 'llm-mutant-equivalence-cost' corpus/README.md
Output:

BASE:
86:| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open | no LLM-specific search run yet (U) → bounded pilot with an independent outcome check |
624:| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open — README.md:86 | before: no LLM-specific search run yet (U) → after: bounded pilot with an independent outcome check: untouched; round 43 states F9 is not touched (README.md:555-556) |
C0:
86:| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044, S286, S287 | open — equivalence-cost contract entered (round 58, `knowledge/llm-mutant-equivalence-cost.md`); bounded pilot unmeasured | no LLM-specific search run yet (U) → bounded pilot with an independent outcome check |
624: (unchanged historical round-43 record row)
659:| `knowledge/llm-mutant-equivalence-cost.md` | F9 equivalence-cost counting contract: distinguish non-compilability, duplication and equivalence before interpreting surviving mutants. The Java study's measured improvements do not transfer numerically to this lane's gates. A bounded LLM-mutant pilot remains unmeasured | S286 (arXiv §Abstract), S287 (deck extract lines 230-241) |

Reading: the live row (line 86) was updated in the candidate-sources and status cells this
round, but its last column still opens "no LLM-specific search run yet (U)". At C0 an
LLM-specific literature search HAS run: S286 was opened from the previously-unopened arXiv
LLM-mutation lead (lead bullet removed after S286 landed) and the S287 deck was opened the
same round; both are now mined rows with used-by → the F9 entry. The last column therefore
contradicts the same row's own status cell. Candidate finding F1 (minor).
Line 624 is an append-only historical record row ("untouched; round 43 states F9 is not
touched") — historical, not adjudicated here; its README.md:86 pointer drifts by design of
the append-only convention.
