# ScoutWikiEquiv — Wikipedia "Mutation testing" (S160)

Seat: L1Tameshi43.ScoutWikiEquiv (leaf, read-only). Access date for all evidence below: **2026-10-25**.
Scratch: `/tmp/tameshi-r43-ScoutWikiEquiv-/` (deleted before return). Lane checkout untouched; no git/jj command run.

## 1. Fetch receipt

| item | value |
|---|---|
| command | `curl -fsSL https://en.wikipedia.org/wiki/Mutation_testing -o /tmp/tameshi-r43-ScoutWikiEquiv-/mutation_testing.html` |
| bytes (`wc -c`) | **170793** |
| HTTP `content-length` | **170793** (exact match → no local truncation) |
| sha256 | **`6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43`** |
| `<title>` | **`Mutation testing - Wikipedia`** (HTML line 5) |
| revid (`wgCurRevisionId`/`wgRevisionId`) | **1373580212** (HTML line 6) |
| HTTP status / date / last-modified | `HTTP/2 200`; `Sat, 24 Oct 2026 17:19:39 GMT`; `Sat, 10 Oct 2026 17:19:39 GMT` |
| content-type | `text/html; charset=UTF-8` |

Lines counted: 1159. All "HTML line N" citations below are 1-based lines of this exact artifact.

## 2. Location finding — there is no "Equivalent mutants" section on the live page

The assignment's premise ("In the Equivalent mutants section") does not hold for rev 1373580212. Observed:

- Complete heading inventory (`grep -o '<h[2-6] id="[^"]*"'`): `Introduction`(735), `Overview`(738), `Goals`(745), `History`(753), `Mutation_testing_overview`(762), `Mutation_operators`(800), `Types_of_mutation_operators`(816), `Types_of_mutation_testing`(821), `Statement_mutation`(824), `Value_mutation`(836), `Decision_mutation`(861), `See_also`(882), `References`(888). **No heading id contains `Equivalent`.**
- `grep -c 'Equivalent_mutants'` → **0**; `grep -o 'aria-labelledby="…"' | sort | uniq -c` → 15 sections, none equivalent-related.
- Case-insensitive `equivalent` occurs on only 4 lines: 794, 796, 798 (subsumed mutants), 904 (cite note 15, Umar thesis title).

The two defining sentences are plain `<p>` elements inside the `Mutation testing overview` h2, i.e. section `data-mw-section-id="5" id="mwcw"` at **HTML line 762**:

- **L794** — `<p id="mw-Q">` (the definition)
- **L796** — `<p id="mw-w">` (the obstacle sentence)

So: the correct citation target is *Mutation testing overview §, paragraphs `mw-Q`/`mw-w`*, not a named section. Any lane/scribe text that cites "Wikipedia § Equivalent mutants" is citation-inaccurate; cite lines 794/796 and the parent section instead.

## 3. Two located quotes (each ≤25 words, accessed 2026-10-25)

**Q1, HTML line 794** (`<p id="mw-Q">`), 16 words — rendered text; raw HTML wraps the final phrase in `<i id="mw-g">…</i>`:

> "The resulting program is behaviorally equivalent to the original one. Such mutants are called equivalent mutants."

**Q2, HTML line 796** (`<p id="mw-w">`), 15 words:

> "Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation testing."

Verbatim-substring check on the artifact: Q2 occurs exactly 1× in the raw bytes; Q1 occurs 0× as a contiguous substring **only because** of the `<i id="mw-g">` tags around `equivalent mutants` — its rendered text is exact and it is present in line 794's content (`q1 in lines[793]` → False, tag-interrupted; `q2 in lines[795]` → True).

Immediately following Q2 (same paragraph, not quoted): the effort to decide equivalence "can be very high, even for small programs" (cite 18), then the 2014 SLR naming the **Equivalent Mutant Problem**, 17 techniques in 22 articles, split into DEM (detecting) / SEM (suggesting) / AEMG (avoiding equivalent mutant generation), with Higher Order Mutation + JudyDiffOp called promising.

Adjacent definitional scaffolding (for context, not part of the two quotes):
- L767: a mutant is "killed" if the test suite detects the change (one test fails) — `if … then the mutant is said to be killed`.
- L748/L750: goal vocabulary is "mutants are not killed"; mutation score = killed / total.
- L785–L790: kill requires the RIP model: reach the mutated statement (L786), infect state (L787), propagate to output (L788).

## 4. Does the page distinguish an equivalent mutant from a survivor on unreachable code?

**No. The page does not distinguish them, and does not even carry the vocabulary to do so.** This is the lane-relevant negative, with the counts that establish it:

| term (case-insensitive, whole artifact) | count |
|---|---|
| `surviv` (survivor/survives/surviving) | **0** |
| `unreach` (unreachable) | **0** |
| `unkilled` | 0 |
| `uncaught` | 0 |
| `live mutant` | 0 |
| `undetected` | 0 |
| `trivial mutant` | 0 |
| `stillborn` | 0 |
| `alive` | 0 |
| `dead code` / `dead-code` | **1** → L741 |
| `not detected` | **1** → L741 |

What the page actually does:

1. **L741** (Introduction): an undetected mutant "typically indicates that the test suite is unable to locate the faults represented by the mutant, but it can also indicate that the mutation introduces no faults"; then "One (common) way a mutant can be valid is that the code that has been changed is \"dead code\" that is never executed." → dead/unreachable code is classified as a **valid, fault-free change**, not as a distinct outcome class, and the sentence is not linked to L794.
2. **L794** defines an equivalent mutant **purely behaviorally**: "it is not possible to find a test case that could kill this mutant" ⇒ the program is "behaviorally equivalent to the original one". No cause is discriminated — operator-level semantic equivalence and unexecuted code are indistinguishable under this definition.
3. **L786** supplies reachability only as RIP condition 1 ("A test must reach the mutated statement") — a necessary condition for killing, with no corollary drawn about unreachable mutants.
4. There is **no outcome taxonomy at all**: no mention of survivors as a class, no "equivalent vs. unkilled-on-dead-code" split, no statement that a dead-code mutant is *not* equivalent.

Consequence (INFERENCE, but forced by the text): on this page's own definitions, a mutant in never-executed code satisfies L794's antecedent (no test can kill it, since none can reach it) and is therefore subsumed **under "equivalent mutant"**. L741's "valid change" framing is a *cause* description, not a competing category. So the article supports conflation rather than the distinction this lane's K/D/E/U rule requires (`dead_code_only` vs `equivalent` as separate verdicts).

**Lane ruling for citations:** Wikipedia (rev 1373580212) may be cited only for (a) the behavioral definition of an equivalent mutant — L794; (b) equivalence detection being a practical obstacle / the "Equivalent Mutant Problem" — L796. It MUST NOT be cited as evidence that an equivalent mutant is distinct from a dead-code/unreachable survivor; that separation is the lane's pre-declared rule (round-43 contract C1: `dead_code_only=1`, `equivalent=0`), sourced elsewhere. Any report sentence of the form "Wikipedia distinguishes equivalent mutants from survivors on unreachable code" is unsupported by this artifact and would be a fabricated citation.

## 5. Residual unknowns

- Revid is whatever Wikipedia served at fetch time; the page is editable, so a later re-fetch may shift line numbers. The sha256 above is the pin — re-verify bytes+sha before reusing any line number, and treat mismatch as a stale citation rather than re-deriving.
- The page's references (cite 18/19, the 2014 SLR) were not opened; nothing here asserts what secondary sources say about the equivalent/survivor split.
- No claim made about other-language Wikipedia editions.

## 6. Tools installed

None. `curl`, `grep`, `sed`, `wc`, `sha256sum`, `python3` were already present; no pacman/uv/npm transaction attempted (pacman paused host-wide).
