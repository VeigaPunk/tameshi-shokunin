# Round 12 w2 — KnowledgeSupport (seat TameshiR12.KnowledgeSupport)

Scope: read-only check of `corpus/knowledge/repeated-control-precondition.md` and the S004/S026 retained quote report `.ufo/evidence/round-12/ControlKnowledge/{quotes.tsv,README.md}` for claim-vs-source support and for three-run determinism overreach. Advisory only; not an independent non-author admission or promotion.

## Method and receipts

- Re-fetched both source bodies to scratch `/tmp/tameshi-r12-kn/fetch/` (not committed). SHA-256 matches the pins in the knowledge header and `ControlKnowledge/README.md:24-25`: S004 `5ec9ba95…2334` (29,579 B, 326 lines); S026 `ca1145fb…6c7a` (236,385 B, 6,171 newline lines + 1 unterminated).
- Located every quote in `quotes.tsv` (Q1–Q10) and every quote in the knowledge body against the served HTML, with tags stripped and entities unescaped.
- Compared the two S026 copies: `text/template` block at `S026.html:1088-1122` (post body `:1095-1102`) and `<noscript>` block at `:1123-1157` (post body `:1130-1137`). Sentence text is identical.
- Re-ran the README recheck counts: `hardly a perfect solution` → 2 lines (`:1101`, `:1136`); `passes reliably when copied to a temporary directory` → 1 line (`:187`). Both healthy.
- Cross-refs checked: `SKILL.md:148-149`, `PROVINCE.md:16-17`, `tools/mutate-and-run.sh` sha256 `75ed934d…adc5` and six legs at `:84-89`, `REGRESSION_EXPECT` at `:1103`, `SOURCES.md:42` (S031).
- Gate contract checked against `tools/repeat-control.py` (usage, exit table, floor, snapshot).
- Installs or updates: none.

## Findings (severity order)

### F1 — medium — misattributed quotation
- `corpus/knowledge/repeated-control-precondition.md:55`: “**Not an admission** … advisory and lane-internal: “NOT independent non-author promotion/admission”.”
- The quoted string does not occur in any retained repo source I searched (`*.md`, `*.json`). The wave contract wording is "not independent non-author admission/promotion" (word order reversed; capitalised NOT added). Either quote the source verbatim or drop the quotation marks and mark it as paraphrase.

### F2 — medium — gate contract table omits an emitted class; `--runs` floor not stated
- `corpus/knowledge/repeated-control-precondition.md:34-41` lists the exit classes. It omits `setup_error` (exit 2), which the gate emits at `tools/repeat-control.py:185-188` and lists at `:43-44`. Add it.
- `repeated-control-precondition.md:48` says `--runs` is "caller-supplied" and "N≥3 is the round's choice". The gate enforces the floor: `tools/repeat-control.py:246-247` (`--runs must be >= 3`) and snapshot `:349-350`. The round-choice statement is accurate, but the enforced floor is a fact the note should cite. It is not a sourced threshold and should stay labelled as a lane choice.

### F3 — low — contract non-claim clause not present verbatim
- `SiblingOverlap.md:165` requires the knowledge note to contain "no flakiness cured or determinism proven". `repeated-control-precondition.md` contains neither "proven" nor "cured" (grep empty). The substance is present: `:26` ("no line in either source upgrades it to determinism") and `:54` ("does not remove nondeterminism"). Either add the clause or record the wording deviation.

### F4 — low — paraphrase presented beside source-quote form
- `repeated-control-precondition.md:14`: "`timeout` = the suite was killed after a long run." Not in S004. Served text at `S004.html:208`: "The mutation caused the test suite to run for a long time, until it was eventually killed." Mark as paraphrase, or quote it.

### F5 — low — word-count notes wrong; unlabelled inference in note column
- `quotes.tsv` note column counts (whitespace split of the quote text):
  - Q4 (`:8`) says 21; actual 22.
  - Q5 (`:9`) says 17; actual 16.
  - Q7 (`:11`) says 16; actual 15.
  - Q8 (`:12`) says 18; actual 17.
  - Q10 (`:14`) says 17; actual 16.
  - Q1, Q6 and Q9 are correct.
- `quotes.tsv:8` note "the definition that makes determinism a universal over runs" is an interpretation. S026 at `S026.html:1130` defines "flaky" and says nothing about determinism. Label it `[I]` or remove it.
- Quote fidelity note: `quotes.tsv:3` says quotes are verbatim. Q1–Q3 drop `<code>`/`<strong>` markup (`S004.html:187`, `:193`, `:203`), and Q2/Q3 span wrapped lines (`:193-194`, `:203-205`). Acceptable, but say so in the note.

### F6 — low — cross-artifact inconsistency on S026/S004 credit and access dates
- `corpus/lessons/round-12.md:13`: S026 "No article quotation is credited from that partial view"; body support deferred to "the source-opening executor".
- `repeated-control-precondition.md:4` credits ten S026 body quotes fetched `2026-10-20T02:13:47Z`. The lesson row has not been reconciled. Append an errata row or update the lesson so one of the two is not stale.
- `corpus/SOURCES.md:15` (S004) and `:37` (S026) record "fetched 2026-10-19"; the knowledge header records 2026-10-20T02:13:47Z. Reconcile in an append-only SOURCES note.

## Claim-vs-source — supported (no action)

- S004 Q1 "Fix this first … copied to a temporary directory." — `S004.html:187` ✓ (tags stripped).
- S004 Q2 "caught — A test failed with this mutant applied. This is a good sign about test coverage." — `:193-194` ✓.
- S004 Q3 "unviable — … inconclusive about test coverage and no action is needed" — `:203-205` ✓.
- S026 Q4 definition `:1130` ✓; Q5 1.5% `:1130` ✓; Q6 16% `:1130` ✓; Q7 84% `:1132` ✓ and "build monitors typically wait for additional CI cycles to run this test again" `:1132` ✓ (knowledge:20 quotes it accurately).
- S026 Q8 retry family `:1136` ✓; Q9 `:1136` ✓ including "report[s] a failure only if it fails 3 times in a row" with the bracketed edit; Q10 `:1137` ✓.
- Template copy line numbers `:1095/1097/1101/1102` for the same sentences ✓.
- Knowledge §2 "retries … delays detection" paraphrases `:1137` ✓ and is marked (I).
- Header `source/verified-at/recheck` present (QUALITY criterion 10) ✓.

## Determinism overreach

- No overreach found in the knowledge note. Disclaimers are present at `repeated-control-precondition.md:26`, `:48`, `:54-55`. "N≥3 is the round's choice, not a sourced rule" (`:48`) is correct.
- `corpus/lessons/round-12.md:22` rejects "three matches prove determinism" and states the flip condition. Consistent with the note.
- The remaining `--runs 3` and "N=3" occurrences in round-12 evidence and wave files either disclaim determinism or use it as an invocation example (`registry-row-draft.md:21`, `ScorecardReview.md:128`, `LessonScribe.md:45`). I found none asserting that N=3 proves determinism in committed corpus files. Note that `LessonScribe.md:15` and `outline.md:45` describe N=3 as a "lane choice matching S026's mitigation convention". The source-based note is consistent with that: S026 says the fail-3-in-a-row mark is a mitigation, so the tie is an analogy, not a sourced threshold.

## Verification gaps

- I did not verify the verbatim wording of the S026 page header/footer or the noscript tag at `:1123` beyond the block boundaries above.
- I did not verify `tools/repeat-control.py` behaviour beyond the usage, exit table, floor and snapshot paths quoted above. The ControlGate seat owns that.
- Main L1 should verify integrated changes once after all seats land. I ran no builds, tests or gate runs.
