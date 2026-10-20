# CRSource — C2 source: Diátaxis grounding for instruction-vs-record section classification

Seat: `TameshiR16.CRSource` · round 16 (w1) · access date **2026-10-20** (UTC 13:24–13:26 GMT) · scratch `/tmp/tameshi-r16-CRSource-work/`.
Deliverable per Target: URLs, access date, anchors, exact ≤25-word quotes with location, and one 11-column SOURCES.md row drafted (not applied). `corpus/SOURCES.md` was read, never edited.

## Axes (godspeed)

- **A1 grounding precision** — every classification claim carries a URL#anchor plus a quote that is an exact substring of the fetched page (machine-checked), with a paragraph-level location and a word count ≤25.
- **A2 transferability** — turn Diátaxis criteria into a decision rule that can be applied to a 50-section `SKILL.md` at section granularity, not just document granularity.
- **A3 provenance** — status codes, `Last-Modified`, ETags, byte counts and sha256 for each fetched page, so a later round can re-fetch and diff instead of re-reading blind.
- **A4 honesty/scope** — mark what is observed vs inferred; state what the source does *not* cover (the cold-read schema's `record` is narrower than Diátaxis `reference`).

## 1. Fetch evidence (observed)

All fetches via `curl -sS -L`, exit 0 each. Files kept in scratch; `sha256sum` run over the saved bytes.

| page | URL | bytes | sha256 | HTTP | Last-Modified | ETag |
|---|---|---|---|---|---|---|
| index | https://diataxis.fr/ | 22287 | `41be933acddc4c59981ec80a0e5bc2ca8b8e2436ada66cbeb324d369ef93603b` | 200 | Thu, 06 Aug 2026 07:20:43 GMT | `W/"0e56fdef82f323f3318e85ee2352cf10"` |
| how-to | https://diataxis.fr/how-to-guides/ | 31595 | `99b2a0f504ccde78ffb515f0bd1fbd703de55baf4f6123b9a7f6315149e0c9f6` | 200 | Thu, 06 Aug 2026 07:20:44 GMT | `W/"f495f21f19ec12e636c1dc6b191482c8"` |
| reference | https://diataxis.fr/reference/ | 25269 | `78ac456f11534eb022b173f1aba98e478349fd4efe0031a1979e2767d9e6d6b0` | 200 | Thu, 06 Aug 2026 07:20:44 GMT | `W/"01808a519424ae2c33b0f7e68a4daed1"` |
| compass (supplementary) | https://diataxis.fr/compass/ | 20288 | `8597a5b13f235ddff56b24b234745fd46ba9a115af2b165b1f4e59b82514e1a0` | 200 | Thu, 06 Aug 2026 07:20:44 GMT | `W/"a801230224ee010cbbfc21e2019399f3"` |
| map (supplementary) | https://diataxis.fr/map/ | 25791 | `755b5649df4f5be8135b77aae6db70a5173931ec7d323e7d7cdd18d645ad8373` | 200 | Thu, 06 Aug 2026 07:20:44 GMT | `W/"94532ce92b51dcdc820e64f1e5196426"` |

Access date for every row above: **2026-10-20**. Response header lines observed: `HTTP/2 200`, `date: Tue, 20 Oct 2026 13:24:44 GMT` (how-to, reference), `date: Tue, 20 Oct 2026 13:26:42 GMT` (index, compass, map).

Command/exit evidence (re-run at the end of the seat, printed verbatim):

```
https://diataxis.fr/ curl_exit=0 http=200
https://diataxis.fr/how-to-guides/ curl_exit=0 http=200
https://diataxis.fr/reference/ curl_exit=0 http=200
https://diataxis.fr/compass/ curl_exit=0 http=200
https://diataxis.fr/map/ curl_exit=0 http=200
index.html: OK / how-to-guides.html: OK / reference.html: OK   (sha256sum -c, exit 0)
```

Anchor inventory (observed, `grep -o '<section id="[^"]*"'`):

- `/how-to-guides/`: `how-to-guides`, `how-to-guides-addressed-to-problems`, `what-how-to-guides-are-not`, `key-principles`, `address-real-world-complexity`, `omit-the-unnecessary`, `provide-a-set-of-instructions`, `describe-a-logical-sequence`, `seek-flow`, `pay-attention-to-naming`, `the-language-of-how-to-guides`, `applied-to-food-and-cooking`.
- `/reference/`: `reference`, `reference-as-description`, `key-principles`, `describe-and-only-describe`, `adopt-standard-patterns`, `respect-the-structure-of-the-machinery`, `provide-examples`, `the-language-of-reference-guides`, `applied-to-food-and-cooking`.
- `/`: `diataxis`, `contents`. `/compass/`: `the-compass`, `using-the-compass`. `/map/`: `the-map`, `the-problem-of-structure`, `expectations-and-guidance`, `blur`, `the-journey-around-the-map`.

Sphinx headings carry no `id` attribute; the anchor lives on the enclosing `<section>`. So a citation's anchor is the *section* anchor, and a paragraph ordinal inside that section is the finest honest location. Ordinals below are "Nth non-heading block (p or li) inside that section".

Snapshot identity (for the block at the end of this report): `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md` → `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`, size 118906 bytes, matching the declared `skill_sha256`. The file was hashed only; its contents were never opened by this seat (no line range was assigned to me).

Supplementary pages `compass/` and `map/` were opened because the Target asks for grounding of *classification*; `/compass/` is Diátaxis's own decision instrument and is the only page that states the classification rule as a rule. They are labelled supplementary everywhere below so L1 can discount them.

## 2. Quote verification (observed)

A Python substring check (`q in clean(article_text)`) was run over every quote used below against the saved page bytes.

- 33/33 quotes **OK** (exact substring of the fetched article text).
- All ≤25 words; longest is 24 words (R4).
- `MISS` count: 0. No quote was reconstructed from memory; no ellipsis was used except where a quote is a deliberate mid-sentence fragment (then the fragment itself is the exact substring).

## 3. Quotes that ground "instruction = how-to"

Field order: id · URL#anchor · heading (section anchor) · block ordinal · exact quote · words.

| id | location | quote | w |
|---|---|---|---|
| I1 | https://diataxis.fr/how-to-guides/#how-to-guides ¶1 | "How-to guides are directions that guide the reader through a problem or towards a result. How-to guides are goal-oriented." | 19 |
| I2 | same §, ¶2 | "A how-to guide helps the user get something done, correctly and safely; it guides the user’s action." | 17 |
| I3 | https://diataxis.fr/how-to-guides/#provide-a-set-of-instructions ¶1 | "A how-to guide describes an executable solution to a real-world problem or task." | 13 |
| I4 | same §, ¶1 | "The steps are in the form of actions." | 8 |
| I5 | same §, ¶1 | "It’s in the form of a contract" — and in the same block — "if you’re facing this situation, then you can work your way through it" | 7 / 13 |
| I6 | https://diataxis.fr/how-to-guides/#key-principles ¶1 | "A how to-guide is concerned with work - a task or problem, with a practical goal." | 16 |
| I7 | same §, li5 | "action and only action" | 4 |
| I8 | same §, li6 | "no digression, explanation, teaching" | 4 |
| I9 | same §, li4 | "assume the user knows what they want to achieve" | 9 |
| I10 | https://diataxis.fr/how-to-guides/#how-to-guides-addressed-to-problems ¶1 | "How-to guides must be written from the perspective of the user, not of the machinery." | 15 |
| I11 | https://diataxis.fr/how-to-guides/#the-language-of-how-to-guides ¶2 | "Use conditional imperatives." | 3 |
| I12 | https://diataxis.fr/how-to-guides/#describe-a-logical-sequence ¶1 | "The fundamental structure of a how-to guide is a sequence." | 10 |
| I13 | https://diataxis.fr/how-to-guides/#omit-the-unnecessary ¶1 | "In how-to guides, practical usability is more helpful than completeness." | 10 |
| I14 | https://diataxis.fr/how-to-guides/#what-how-to-guides-are-not ¶1 | "How-to guides are wholly distinct from tutorials." | 7 |

Reading: an instruction section is defined by **action**, by **an executable contract with stated steps**, by being **written from the reader's side** (not the machinery's), and it is deliberately **not complete** and **not explanatory**. Those four are the tests to apply.

## 4. Quotes that ground "record = reference"

| id | location | quote | w |
|---|---|---|---|
| R1 | https://diataxis.fr/reference/#reference ¶1 | "Reference guides are technical descriptions of the machinery and how to operate it. Reference material is information-oriented." | 17 |
| R2 | same §, ¶2 | "Reference material contains propositional or theoretical knowledge that a user looks to in their work." | 15 |
| R3 | same §, ¶3 | "The only purpose of a reference guide is to describe, as succinctly as possible, and in an orderly way." | 19 |
| R4 | same §, ¶3 | "Whereas the content of tutorials and how-to guides are led by needs of the user, reference material is led by the product it describes." | 24 |
| R5 | https://diataxis.fr/reference/#reference-as-description ¶1 | "Reference material describes the machinery. It should be austere. One hardly reads reference material; one consults it." | 17 |
| R6 | same §, ¶2 | "There should be no doubt or ambiguity in reference; it should be wholly authoritative." | 14 |
| R7 | same §, ¶4 | "reference should not attempt to show how to perform tasks" | 10 |
| R8 | same §, ¶4 | "it can and often needs to include a description of how something works or the correct way to use it" | 20 |
| R9 | https://diataxis.fr/reference/#describe-and-only-describe ¶1 | "Neutral description is the key imperative of technical reference." | 9 |
| R10 | https://diataxis.fr/reference/#the-language-of-reference-guides ¶1 | "State facts about the machinery and its behaviour." | 8 |
| R11 | same §, ¶2 | "List commands, options, operations, features, flags, limitations, error messages, etc." | 10 |
| R12 | https://diataxis.fr/reference/#provide-examples ¶1 | "an example of usage of a command can be a succinct way of illustrating it and its context" | 18 |
| R13 | https://diataxis.fr/reference/#applied-to-food-and-cooking ¶2 | "you do not want to be confronted by opinions, speculation, instructions or interpretation" | 13 |

Reading: a record section is **description of a thing** ("the machinery"), **led by the thing described, not by the reader's need** (R4), **authoritative/factual** (R6, R10), and it **must not teach how to act** (R7, R13) — while still being allowed to *quote* commands as illustration (R12, R8). That last pair is the load-bearing distinction for cold-read classification, because lane records embed commands everywhere.

## 5. Quotes that give the discriminator itself (supplementary: compass)

| id | location | quote | w |
|---|---|---|---|
| D1 | https://diataxis.fr/compass/#the-compass ¶5 | "The Diátaxis compass is something like a truth-table or decision-tree of documentation." | 12 |
| D2 | same §, ¶22 | "To use the compass, just two questions need to be asked: action or cognition? acquisition or application?" | 17 |
| D3 | https://diataxis.fr/compass/#using-the-compass ¶12 | "try applying them close-up, at the level of sentences and words, or from a wider perspective, considering an entire document." | 20 |
| D4 | same §, li3 | "action: practical steps, doing" | 4 |
| D5 | same §, li4 | "cognition: theoretical or propositional knowledge, thinking" | 6 |

D3 is the licence for **section-level** classification: the instrument is explicitly meant to be applied "at the level of sentences and words". D2 is the two-question rule; the first question alone separates the cold-read's two classes.

Taxonomy anchor: https://diataxis.fr/#diataxis ¶5 — "Diátaxis identifies four distinct needs, and four corresponding forms of documentation - tutorials, how-to guides, technical reference and explanation." (19 words). This is the four-form frame the two classes sit inside; it also warns that "explanation" is a third thing, so a rationale section is neither instruction nor record by Diátaxis's own terms (see inference note).

## 6. Derived rule for C2 (the actual deliverable)

Apply the compass **per section**, in this order. Every clause is tied to a quote above; the ones without a quote are marked `[INFERENCE]`.

1. **Question 1 — action or cognition?** (D2). If the section tells the reader what to do next, now or on a future occasion ("run", "check", "write", "decide") → `class: instruction` (D4, I2, I4). If it reports what is or what happened (state, artifacts, hashes, outcomes) → `class: record` (D5, R1, R10).
2. **Instruction confirmation** — it should read as a contract with steps (I3, I5), in a sequence (I12), written from the reader's side (I10), in conditional imperatives (I11). Absence of *explanation* is not a defect (I7, I8); absence of *completeness* is not a defect (I13); the reader is assumed competent (I9).
3. **Record confirmation** — it should describe the thing, be neutral and authoritative, and avoid telling the reader to act (R3, R6, R7, R9, R10). A command string inside it is not disqualifying (R12) **unless the surrounding sentence directs a future action**, in which case that sentence is instruction material and the section is mixed `[INFERENCE]`.
4. **Verdict vocabulary maps onto the same axis** (this is the piece the cold-read schema needs):
   - `executed-ok` is a property only an **instruction** can have — it is the how-to contract being honoured (I5: "It’s in the form of a contract" / "if you’re facing this situation, then you can work your way through it"; the "then" clause is the stated outcome the cold-read verdict checks). A record marked `executed-ok` is category-incoherent `[INFERENCE]`.
   - `verified-record` is a property only a **record** can have — it is R6/R10 being honoured by re-checking concrete anchors. An instruction marked `verified-record` is category-incoherent `[INFERENCE]`.
   - `gap-blocking` on an instruction = not executable without oral context, i.e. it fails I3/I4 (steps in action form) or I10 (written from the reader's side).
   - `gap-minor` on an instruction = executable, but needed a named non-blocking inference; this is legitimate under I13 (usability over completeness), so it must not be escalated to blocking merely for being incomplete.
   - `wrong-expectation` = the instruction's stated outcome did not occur (I5's contract broken), not "the section was hard".
   - `not-executed` is verdict-only on instructions; on records it should be stated as "not verified" `[INFERENCE]`.
5. **Mixed sections** — pick the dominant move by counting directive vs descriptive blocks, and record the minority in `minor_gaps`. Diátaxis's own two documents do exactly this: `/reference/` contains imperative guidance about writing reference ("State facts…", "List commands…", R10/R11) inside a document whose subject is description — so a page can legitimately contain instructions *about* records. That is not contamination; it is the genre boundary being observable.

### Honest limits of this source

- **The two Diátaxis pages are explanation *about* the forms, not specimens of them.** `/how-to-guides/` and `/reference/` are meta-documents that define the forms. They are tier-A authority for the *definitions* (what makes content instruction vs reference) and zero evidence for what a lane's actual instruction or record looks like. Do not cite them as genre exemplars.
- **"record" in the cold-read schema ≠ "reference" in Diátaxis, exactly.** Diátaxis reference describes *the machinery* (API, product, behaviour — R1, R4). The cold-read `record` reports *what happened* (round outcomes, artifacts, verification). The mapping is by **function**: both are cognition-oriented, thing-led, factual, authoritative, and non-directive (D5, R4, R6, R10). Narrowing "describes the machinery" to "reports the run that touched the machinery" is `[INFERENCE]`; it is the only inference this report leans on.
- Diátaxis's fourth form, explanation, has no cold-read class. A section whose function is *rationale* (why the lane does X) is not instruction and not record by Diátaxis's terms. The cold-read schema forces a binary, so such a section should be classified by its dominant move and flagged `[INFERENCE]` in `minor_gaps` rather than silently binned.

## 7. Bounded recommendations

1. **Classifier**: for each `SKILL.md` section, answer D2's first question and record the answer as the class. Do not classify by heading verb alone — I11 says imperatives are a *style* of instruction, while R10/R11 show an imperative sentence can be prescriptive guidance *about* described content rather than a step the reader must take.
2. **Do not treat fenced commands as evidence of class.** R12 explicitly licenses command examples inside reference. Use the surrounding sentence's direction of fit: future action → instruction; past/state fact → record.
3. **Keep completeness out of the verdict.** I13 ranks usability above completeness, so an instruction must not be marked blocking merely for being incomplete; a `gap-minor` naming the inference is the correct ceiling unless the instruction is genuinely unexecutable without oral context.
4. **Enforce verdict/class coherence** (item 4 in §6): `executed-ok` only on instructions, `verified-record` only on records. This is a cheap mechanical check on the ledger and catches exactly the misclassification class that the cold-read is meant to expose.
5. **Provenance**: if any cold-read report needs to justify its class axis, cite `/compass/#the-compass` D2 and `/how-to-guides/#key-principles` I7 rather than the index page — the index states the taxonomy but not the decision rule.

## 8. SOURCES.md row draft (11 columns) — do not apply

Registry currently ends at `S051` and its footer says "Next unused id: S052." Row is a single line, no internal pipes, ready to append after S051. Column order matches the live header `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

```markdown
| S052 | Diátaxis: How-to guides, Reference, and The compass — https://diataxis.fr/how-to-guides/ | docs | A | definitional criteria separating instruction (how-to) content from record/reference content at section granularity | §How-to guides, §Key principles, §Provide a set of instructions, §The language of how-to guides @ /how-to-guides/#key-principles; §Reference as description, §The language of reference guides, §Provide examples @ /reference/#reference-as-description; compass table @ /compass/#the-compass; fetched 2026-10-20, Last-Modified 2026-08-06, sha256 99b2a0f5…/78ac456f…/8597a5b1… | instruction content is action and only action, an executable contract of steps written from the reader's side in a sequence of conditional imperatives, and is neither complete nor explanatory by design; reference content is neutral authoritative description led by the thing described, never showing how to perform tasks, yet free to quote a command as illustration; the compass reduces the choice to action-or-cognition and is meant to be applied at sentence level | mined | 2026-10-20 | 365d | .ufo/waves/round-16/w1/CRSource.md |
```

Append-completeness notes for whoever owns `corpus/SOURCES.md` (not this seat):
- Add footnote bullet in the closing notes list: `- S052: round-16 C2 Diátaxis grounding for instruction-vs-record section classification; compass cited as supplementary.`
- Bump footer `- Next unused id: S052.` → `S053.`
- `used-by` points at this report because no `corpus/knowledge/` doc was written this round; repoint it if L1 lands the rule in a knowledge file.

## 9. Unknowns / not done

- I did **not** read `SKILL.md` or the snapshot's contents, nor `LOG.md`, `SCORECARD.md`, or any other seat's material — my mandate was the external source (the snapshot was hashed only). So I cannot say whether any specific `SKILL.md` section is currently misclassified; §6 gives the rule, not an audit.
- I did **not** check the diataxis source repository for page age beyond HTTP `Last-Modified` (2026-08-06); I saw no per-page version string in the fetched page bodies.
- No tooling installed or upgraded this round; no `pacman` transaction was attempted (host-wide pause respected). Only `curl`, `sha256sum`, `grep` and the stdlib Python in the scratch dir were used.
- No writes outside this report and `/tmp/tameshi-r16-CRSource-work/`.

```json
{"seat":"TameshiR16.CRSource","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[],"scratch":"/tmp/tameshi-r16-CRSource-work"}
```
