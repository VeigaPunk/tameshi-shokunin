# CriticCmdBind — attack on the R17-CMD-BIND resolution

Seat: TameshiR18.CriticCmdBind (critic, leaf). Read rev:
`01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, attacked in a detached /tmp clone
(`git clone` + `checkout --detach`; all greps/reads via `git grep`/`sed` in the
clone or `git show <rev>:<path>`). Phrase list taken from
`.ufo/waves/round-18/w1/K03CmdBindChoice.md` §2 (8 wordings). Scope swept:
`SKILL.md`, `corpus/**`, `.ufo/evidence/round-18/**` docstrings, plus
`LOG.md`/`SCORECARD.md`/`.ufo/waves/round-18/staged/**` as a bonus (K03 named
SCORECARD/LOG in its guard). No tools installed; no lane writes other than
this report.

## What holds

All three K03-F2 conditions landed as appended text, and the guard text is
clean:

- `corpus/lessons/round-17.md:99-108` — append-only "Correction — round 18
  wave 1" block names all three required corrections: G5 breadth ("holes 1–4
  … closed" → holes 3+4 and the input half of 1; command binding still open,
  `:102`), G7 pointer hole 5 → hole 7 (`:103`), and 89-is-W2-receipt vs
  final-94 tally (`:104`). The original overclaim lines `:22`/`:24` keep
  their bytes (append-only is sanctioned, not a defect).
- `corpus/knowledge/input-keyed-coldread-credit.md:127-147` — erratum §3
  "R17-CMD-BIND: the narrower claim" states inputs-bound / argv-not-bound
  exactly, and keeps the required disclosure verbatim (`:67`: "A seat can
  still skip a command; the rule makes a recorded read checkable, not
  complete."). Body lines `:35` ("trace receipts whose **inputs** it
  covers") are accurate.
- `corpus/QUALITY.md:236-250` — criterion 33 is worded precisely: credit is
  "evidence about the inputs a read ran against, not about the commands it
  ran"; its falsifier ("a 'closed' sentence over an input-keyed-only entry …
  fails") is exactly the guard needed.
- `SKILL.md:1932` — registry row carries the narrowing inline: "input-keyed
  credit only: it binds credit to recorded inputs, not to the commands a
  bucket requires — never cite it as command coverage".
- `corpus/lessons/round-17-verifier-spotcheck.md:230,324,332` — the original
  spot-check already says "not a mechanical proof that every command an
  agent ought to run was executed"; historical text, unchanged.
- `LOG.md` — no round-18 entry exists yet; the round-17 entry (`:1062-1064`)
  claims only "verified lane inputs, committed trace receipts". Clean.
- `.ufo/evidence/round-18/coldread/assemble.py:38-44` — docstring's "A4 trace
  binding" binds receipt `inputs`/`external` into the entry; accurate.
- `.ufo/waves/round-18/staged/corpus/lessons/round-17.md` and
  `staged/corpus/knowledge/input-keyed-coldread-credit.md` are **byte-
  identical** to the landed files (verified by `diff`, exit 0 both) — no
  divergent unguarded duplicate authority.

## Findings

### F1 (minor, fixable) — round-18 kit docstring still claims command binding

`.ufo/evidence/round-18/measure.py:374` — `trace_reason` docstring reads:

```python
def trace_reason(repo, rev, entry, strict):
    """Bind commands to committed trace receipts; None when satisfied/na.
```

The function binds *inputs*: it validates receipt schema, receipt `inputs`
coverage/drift, `external`, and `live_lane_reads`. It never reads a receipt's
`argv` — verified: `grep -n "argv" .ufo/evidence/round-18/measure.py` → only
`:789` (selftest fixture `{'argv': ['cat', INPUT_FILE]}`), `:1516`
(`def main(argv=None)`), `:1539` (`parse_args`). Zero `commands-unbound`
reason exists; `bucket-commands.json` has no consumer. The docstring is
inherited verbatim from `.ufo/evidence/round-17/measure.py:369` — i.e. the
L1 narrowed every *prose* claim but carried the overclaim inside the copied
instrument, directly inside a file covered by K03's phrase list ("bind …
commands" as a description of what the gate does). A docstring is exactly
the "kit docstring" surface my Target names.

- Impacted axes: calibration (a selftest-blessed instrument mislabels its own
  contract; a seat reading the docstring could cite command coverage and
  trip QUALITY 33's own falsifier).
- Smallest safe correction: `"Bind recorded inputs to committed trace
  receipts; None when satisfied/na."` — or `"Require committed trace
  receipts and bind their inputs"`. One line; no behaviour change, selftest
  cannot regress (docstrings are unasserted — itself a noted survivor class,
  but the text is wrong regardless).

### F2 (minor, borderline) — `corpus/README.md` frontier cell overstates the binding

`corpus/README.md:246` (round-17 row for `input-keyed-coldread-credit.md`):

> "… **trace receipts bind executed commands to inputs**; a failing read
> with verified inputs vetoes; …"

Read one way it is literally true (a receipt records argv and the inputs the
traced argv touched). Read the other — the way a frontier-table reader will —
it says the executed commands are *bound* (verified/matched) to the entry,
which is the exact reading R17-CMD-BIND forbade and the erratum at
`input-keyed-coldread-credit.md:146` ("not a command-coverage proof, and it
does not show that the declared commands ran") exists to kill. The row has
no erratum pointer; README is append-only ("rows above keep their line
numbers", `:240`), so the cell survives uncorrected next to the corrected
lesson. This is the same class K03 §2.3 flags — "commands are traced" as a
summary of credit.

- Impacted axes: calibration; freshness of the corpus index (the frontier row
  is the highest-traffic summary of the entry).
- Smallest safe correction: a dated README erratum line near `:270` (where an
  erratum pointer already exists for another row) — reword the cell as
  "trace receipts bind the **inputs** a recorded command touched; receipt
  argv is recorded but not consumed by the credit rule". No line moves
  needed; append-only is the file's own convention.

### F3 (not a defect, recorded for completeness)

`.ufo/waves/round-17/` and `round-18/` seat reports and dispatch JSONs still
contain "trace binding" unqualified and the original "holes 1–4 closed"
quotation — e.g. `.ufo/waves/round-18/staged/lesson-round-18-mistakes.md:10`,
dispatch prompts quoting the old row. These are dated seat artifacts
quoting the defect to correct it; no correction needed and none is possible
under artifact immutability.

## Verdict

**partial** — the sanctioned narrowing landed completely in prose (lesson
corrections, erratum, QUALITY 33, SKILL registry row), but two sentences
still imply command coverage: the `trace_reason` docstring at
`.ufo/evidence/round-18/measure.py:374` ("Bind commands to committed trace
receipts") and the frontier cell at `corpus/README.md:246` ("trace receipts
bind executed commands to inputs"). Both are one-line/docstring fixes;
neither changes behavior.
