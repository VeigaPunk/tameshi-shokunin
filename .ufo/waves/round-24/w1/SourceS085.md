# SourceS085 — round24 SOURCES S085 quote (line 66) and scope (critic, w1)

Target: `corpus/SOURCES.md:94` (S085) and `corpus/lessons/round-24.md:32-37`, read against
`.ufo/waves/round-23/fresh-adjudication.json@6a1821a8897eea6e7d9669292160ec9593669409:53-104`
(accepted slice per this ticket: lines 53–104, quote at 66). All reads read-only
(`GIT_OPTIONAL_LOCKS=0 git show`, `sha256sum`, `python3` parsers); no gate, battery or selftest run;
nothing installed.

## Verdict

**AGREE on the quote and on the scope's identity claim. Two wording defects, both fixable, neither
blocking.**

- The line-66 quote is byte-exact, unique in the file, correctly located, 15 words (≤25 contract
  limit), and it quotes the right defect.
- The `scope` cell's substance holds: the source is the lane's own adjudication of *unexecuted*
  hardening gaps; the `findings` labels resolve to real round23 seat reports, so "their originating
  seats" is supported; "not their truth" is the honest qualifier given one routed item was a seat
  tradeoff, not a defect.
- **D1 (anchor endpoint):** the cell names the array `routed_not_executed` but cites `lines53–104`.
  That range is exactly the eight `defect` fields, not the array (lines 48–106); it clips entry 1's
  `"ArgvExact"` at line 51 and the closing brace at 105, so the cited slice is not JSON-parseable.
- **D2 (teaches overclaim):** "turn **each** routed hardening gap into a named predicate" is not
  delivered: 5 of 8 routed entries map wholly to K-predicates, 2 partially, 1 not at all (runner
  digest is explicitly "recorded per run, not a ruler predicate" in the entry the row cites).

No evidence of producer authentication, promotion, R17-CMD-BIND closure or numeric uplift is offered
by the row, and I claim none.

## Claim-by-claim

| # | Claim (S085/lesson) | Result | Evidence |
|---|---|---|---|
| 1 | Quote at line 66, revision 6a1821a | HOLDS | `python3` check on `git show 6a1821a:…`: the 15-word string `do not pin bundle_sha256 literals, so a regenerated bundle and expected pair would still hold` is `in` line 66 exactly (`True`) and appears on no other line (`[66]`) |
| 2 | Line 66 is that text | HOLDS | `:66` = `"defect": "The command-binding-frozen-clean and source-read-red registry rows do not pin bundle_sha256 literals, so a regenerated bundle and expected pair would still hold."` |
| 3 | Line 66 is stable at the delivered revision | HOLDS | whole-file sha256 is `44f9fb583121365732e9723cc44142dba03623b3eeb05a7d3a12b035acc03fee` at **both** 6a1821a and c8c5b88, and in the working tree; line numbers cannot drift between the pin and HEAD |
| 4 | Defect attribution `RevisionDeclared F1` | HOLDS | `.ufo/waves/round-23/w2/RevisionDeclared.md:5` "Finding 1 … the registry does not enforce \"frozen\"" names the same two rows and proposes the same two digests round24 adopted |
| 5 | Defect attribution `CorpusClaim F3` | HOLDS as routing, wider seat verdict | `.ufo/waves/round-23/w2/CorpusClaim.md:19-22` F3 says "Replacing both files in a later commit would still hold" but is titled "tradeoff to word carefully, not a defect" — the adjudication reclassifies a seat tradeoff as a routed defect; S085's "not their truth" qualifier is what keeps that honest |
| 6 | "registry rows do not pin bundle_sha256 literals" | HOLDS at base | `registry.json@6a1821a` rows expect only `"finding_ids": []` / `"finding_ids": ["ARGV_MISMATCH"]`; `tools/command-binding.py:120-125` accepts `expected = {schema, bundle_sha256}` and `expected.json` sits beside the bundle, so bundle+expected can be regenerated together |
| 7 | "a regenerated bundle and expected pair would still hold" | HOLDS, and is exactly what K5/K6 test | `.ufo/evidence/round-24/measure.py:107-118` `substitute()` writes a valid different bundle and rewrites `expected.json` to its digest; `pin_rows()` `:121-139` marks discrimination only when a pristine-held row fails after substitution |
| 8 | "and their originating seats" | HOLDS | every `findings` label is a seat: `.ufo/waves/round-23/w2/{ArgvExact,MutationDesign,CwdDeclared,Replay31,Replay34,RevisionDeclared,CorpusClaim,RunnerIsolation}.md` exist and `swarm-registry.json` maps e.g. `ArgvExact -> TameshiR23.ArgvExact`; suffixes are finding/severity indices (`RevisionDeclared F1`, `RunnerIsolation Medium x2`) |
| 9 | `own-work`, tier A, `mined`, opened 2026-10-21, recheck `on-change` | HOLDS | own-work row pointing at a repo path is precedented (S082 `on-change`, S083); both `used-by` paths exist and cite S085 (`replay-projection-hardening.md:1`, `round-24.md:38`); census: 1 row S085, `NF=13`, malformed rows `0` |
| 10 | Anchor `routed_not_executed lines53–104` | PARTIAL (D1) | array opens at `:48`, closes at `:106`; entries at 49–105; `"defect"` fields at 53, 59, 66, 74, 81, 87, 93, 104 — the range is the defect span, not the array |
| 11 | Teaches "each routed hardening gap" | FAILS as written (D2) | mapping below: 5/8 wholly, 2 partial, 1 none |

## D1 — anchor range clips the array it names

Counterexample: a reader who follows the anchor literally and asks for the JSON at
`fresh-adjudication.json:53-104` gets eight `defect` lines interleaved with six `findings` blocks,
beginning mid-object — entry 1's `"findings": ["ArgvExact"]` is at line 51, outside the range, and
the array's `[` (48) and `]` (106) are both outside. `json.loads` of that slice fails. The defect
texts themselves are all inside, so nothing substantive is lost; only the pointer is imprecise, and
it is the one cell a non-author re-verifier will dereference first.

Smallest correction: replace the anchor with `routed_not_executed lines48–106, revision6a1821a…`
(or, keeping the field-scoped style, `routed_not_executed defect fields lines53,59,66,74,81,87,93,104`).
The lesson's `S085 opened …` paragraph and the knowledge file's `source:` header carry the same
`53-104` and should move together.

## D2 — "each" is not what the entry delivers

Observed mapping (entry number = order in `routed_not_executed`; predicates from `measure.py:24-42`,
`:141-142`):

| Routed entry | Predicate | Wholly? |
|---|---|---|
| 1 `ArgvExact` (name-insensitive argv mutant) | K1 `argv-name-insensitive`; supplemental `argv-swapped-between-names` case present in `.ufo/evidence/round-24/extra-cases.json`; K2 casefold goes further than the routed text | yes |
| 2 `MutationDesign` (negative exit ignored) | K3 `exit-negative-ignored` | yes |
| 3 `RevisionDeclared F1`/`CorpusClaim F3` (no digest pin) | K5/K6 substitution | yes |
| 4 `Replay31/34`, `CwdDeclared 2` (projection drops `held`, `cleanup_ok`, `external`, `non_hermetic_argv`) | K7/K8/K10 | partial — the second sentence ("the receipt schema cannot carry a live-dependency marker") is not implemented as a schema change; the knowledge table substitutes a `live_dependent` list, so the marker requirement is sidestepped, not satisfied |
| 5 `RevisionDeclared F3`/`CorpusClaim F2` (runner/instrument digest from live tree) | none | no — the cited entry's own table says "runner digest from the live tree … — (recorded per run, not a ruler predicate)" |
| 6 `CwdDeclared 3` (sibling identity by string) | K11 `fleet-root-realpath` | yes |
| 7 `RunnerIsolation Medium x2` (unbounded streams) | K9 `stream-limit-refused` | yes |
| 8 `Replay32/33/35/36/29/43` (loose stdout tokens, kept unchanged) | K5/K6 pin only the two bundle rows | partial — `tools/registry.json` still has **42** active rows whose `stdout_contains` carries no `bundle_sha256` token, and the routed item explicitly keeps them unchanged |

So 5 of 8 wholly, 2 partial, 1 none — the same 5/8 count independently reached by sibling
`CorpusReadme.md` D2. The word "each" promises 8/8. The located quote grounds entry 3 only, so
contract rule 1's "quote grounding `teaches`" is met for one representative gap, not for the
sentence's quantifier.

Smallest correction: `turn each discriminable routed hardening gap into a named predicate that can
be shown to fail before and pass after, recording the ones that stay per-run` — or keep "each" and
drop the entry's own "recorded per run, not a ruler predicate" row from the claim's universe.

## Nits (no correction required)

- N1: `round-24.md:36-37` opens the quotation mid-sentence (`do not pin …`) without an ellipsis, so
  it reads as a whole claim. The `(line 66)` location makes it verifiable, and the elided subject is
  recovered in the same sentence's next clause.
- N2: line 66 says "source-read-red registry rows"; the registry name is
  `command-binding-source-read-red`. Unambiguous — no other row matches.
- N3: SOURCES spells the range with an en dash (`53–104`) while the knowledge header uses a hyphen
  (`53-104`); both sibling predecessors (S082, S083) mix the same way. Cosmetic.

## Bounds of this finding

I verified the quote, its location, its stability, the seat attribution of the labels, the base-state
truth of the defect, and the coverage the `teaches` cell promises against the frozen ruler. I did not
execute `measure.py`, `registry-replay.py --selftest` or any registry row, so I assert nothing about
the 1/11 → N/11 result; the pinned digest literals were only checked against `sha256sum` of the two
bundle files (`3d6c99b7…a50b9`, `db620668…0d3cf`), which they match. Code-lane review of
`command-binding.py`/`registry-replay.py` and the mutation sweep belong to sibling seats.

Tools installed: none.
