# Scout findings — PIT Basic concepts (S159)

Task: locate verbatim quotes defining "Killed", "Run error", "No coverage" on
https://pitest.org/quickstart/basic_concepts/, state whether the page says a run
error counts toward the score or as a kill, and compare with staged row `staged:S159`
(SOURCES.append.md line 13).

## Snapshot (fetched 2026-10-25)

- Command: `curl -fsSL https://pitest.org/quickstart/basic_concepts/ -o /tmp/tameshi-r42-ScoutPitConcepts-src/basic_concepts.html`
- sha256: `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a`
- Size: 12155 bytes
- Title: `<title>Basic concepts</title>`

## Verbatim quotes (HTML line numbers in fetched snapshot)

1. **"Killed"** — line 175:
   `<p><strong>Killed</strong> means a test caught the mutation successfully.</p>`
   Quote (9 words): "Killed means a test caught the mutation successfully."
2. **"Run error"** — lines 192–193:
   `<p>A <strong>run error</strong> means something went wrong when trying to test the mutation. ...`
   Quote (13 words): "A run error means something went wrong when trying to test the mutation."
3. **"No coverage"** — line 179:
   `<p><strong>No coverage</strong> is the same as <strong>Survived</strong> except there were no tests that exercised the line of code where the mutation was created.</p>`
   Quote (23 words): "No coverage is the same as Survived except there were no tests that exercised the line of code where the mutation was created."

The page lists the seven outcome classes in a `<ul>` (lines 166–172): Killed, Survived,
No coverage, Non viable, Timed Out, Memory error, Run error. Definitions follow at lines
175, 177, 179, 184, 187, 192.

## Does a run error count toward the score or as a kill?

**The page says neither.** It contains zero occurrences of "score", "kill ratio", or
"mutation score" (`grep -c -i -E 'score|kill ratio|mutation score'` → 0). The only
normative statements about run errors are the definition (lines 192–193) and: "Under
normal circumstances you should see no non viable mutations or run errors." (line 196).
The page does not define a score at all, so it cannot say whether a run error counts
toward it or as a kill — the run-error class is presented as an abnormal diagnostic, not
as a scoring input.

## S159 claim comparison (SOURCES.append.md line 13)

S159's `teaches` field: "no coverage" and "survived" are different outcomes, so a
score's denominator is a choice of outcome class, not a neutral fact.

- **Supported**: the live page lists "No coverage" and "Survived" as two separate
  named outcomes (lines 167–168) with separate definitions (lines 177, 179), i.e. the
  outcome vocabulary PIT reports includes both classes. (Nuance: the page's own text
  says "No coverage is the same as Survived except there were no tests that exercised
  the line..." — the classes are distinct list items but the prose treats them as the
  same status differing only in whether covering tests existed.)
- **Not supported**: the claim that "a score's denominator is a choice of outcome
  class" — the page never mentions a score or a denominator, so the denominator claim
  is not derivable from this page.
- S159's other fields: the source URL, kind `docs`, tier A, and section list
  (Killed, Survived, No coverage, Non viable, Timed out, Memory error, Run error) all
  match the live page. The recheck string `grep -c 'No coverage'` passes (matches at
  lines 168 and 179).

## Could not check

- The page's score semantics (whether run errors count toward the score or as kills):
  the page simply does not discuss scores; that question would need a different PIT
  source (e.g. the FAQ or the report format docs), which was out of scope for this task.
