## Certification attempt (appended round 94) — the verdict-content reader

Appended; the entry and the round-92/93 blocks above are unchanged. Round 93's counter was
killed by three sentences of its own record: its `coverage` scan was fence-blind, it never
read the delimiter row so it could not see a GFM-invalid table, and its seal compared the
spec to itself — one lane commit repointing the spec and regenerating `pins.json` made it
execute a foreign gate while printing `pin=true pins=true`. Round 94's successor,
`.ufo/evidence/round-94/c1/measure-v94.py`, answers each:

- **The gate identity is anchored in the counter's own self-pinned bytes.**
  `GATE_COMMIT` and `GATE_SHA256` are constants inside the file whose sha256 is itself
  pinned; when the spec-derived identity disagrees the counter refuses at setup
  (`C1_SETUP gate-identity-mismatch`, exit 2) and never materialises or runs the subject.
  The battery's `gate-foreign` state repoints `gate.path` to another real fleet blob with
  its real sha and gets exactly that refusal.
- **`coverage` skips fenced blocks and matches the note path as its own cell.** The scan
  runs through `block_lines` (S322) and requires a backtick-delimited cell whose first
  token is the path, so a fenced denial row cannot flip a committed assertion and a longer
  filename cannot satisfy it (S321's cell rule).
- **The delimiter row is read and checked.** `tables()` returns the delimiter cells; a
  table whose delimiter width differs from its header adds a `delim:` finding; a
  remainder row is padded or truncated when its one verdict token sits in the verdict
  column and refused when the verdict-bearing cells are ambiguous (S321's pad/ignore rule).

**What this reader certifies.** The twelve cells of the single verdict table above — one
cell per spec id `C01` to `C12`, in the header-named `verdict` column — agree with the
verdicts the counter itself re-derives, by re-running the pinned gate's own `selftest`
twice per mutant over the twelve single-edit mutants: `n=12 killed=5 survived=7`,
`mismatched=0`, every survivor's witness registry rebuilt and differing between pristine
and mutant, the spec still carrying its twelve ids, and the note's own figure line
matching the re-derived kill count. The committed receipt is `C1_R94_PASS=true`, exit 0,
with `verdict_tables=1`, `badrows=0`, `mismatched=0`.

**What this reader does not certify.** It certifies those twelve cells and nothing about
how they were obtained: a note that copies the committed predictions instead of the
measured receipt carries the same cells and passes, because the reader compares the cells
against its own re-execution and not against the provenance of the text. It does not
certify a fenced presentation: a fenced block is literal text (S322), so a fenced
inverted table, or a fenced figure line, is neither keyed nor counted, and the figure it
checks is the block-level one. And it does not certify a table whose header row carries
no `verdict` cell: such a table is not a verdict table at all (S321), so an id-keyed
table that asserts no verdict is never refused and §2's survivor table and §2b's impact
table are outside the reader's scope by construction, not by accident.

The three ground rules are cited by their located quotes, each in the snapshot the reader
itself reads:

- S320 (sha256sum(1), the self-pin's digest ground) — "Print or check SHA256 (256-bit)
  checksums." (`.ufo/evidence/round-94/sources/s320.html:88`).
- S321 (GitHub Flavored Markdown Spec, §4.10 Tables) — "a single header row, a delimiter
  row separating the header from the data"
  (`.ufo/evidence/round-94/sources/s321.html:4506-4507`) and "The table is broken at the
  first empty line, or beginning of another block-level structure"
  (`.ufo/evidence/round-94/sources/s321.html:4607-4608`).
- S322 (CommonMark Spec 0.31.2, §4.5 Fenced code blocks) — "A fenced code block begins
  with a code fence, preceded by up to three spaces of indentation."
  (`.ufo/evidence/round-94/sources/s322.html:2732-2733`).

Round 94's battery registers 45 states — 6 positive, 30 hostile, 1 gate-identity setup, 3
setup, 5 removal mutants — and every hostile state names the conjunct it must falsify.
Admission remains the non-author closure's.
