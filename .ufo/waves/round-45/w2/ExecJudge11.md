seat: ExecJudge11

# Round-45 w2 — C1 falsify review: S052, S055, S069

Independent re-judgment at `ad5942c6e9858af19d00000b58439b321ddfa62b` (ledger, committed snapshots, w1 reports). I am not the author of any of the three (authors: ExecRows06, ExecRows07, ExecRows12). Every fetch and extraction below was run by me today under `/tmp/tameshi-r45-ExecJudge11/`; no lane file was written except this report, no git/jj command was run.

## Verdicts

S052 agree — reviewer ExecJudge11 — live fetch is byte-identical to the entry and the committed snapshot (sha256 b19e6ca97778551a09fcc772e50c33f711c374817e34248fef1fdf42cb754c8c), and the 19-token quote is the `Support` table header plus its first three rows inside §Supported mutators (section heading offset 565, table header 816, quote 824, table continues with `Block Statement` at 944), so it is body content at the row's anchor and its StrykerJS column glyphs (`Array Declaration` ✅, `Assignment Expression` ❌) state the discriminating part of the teaches claim — which JS single-edit operator families StrykerJS supports and that assignment expression is the one it does not.

S055 agree — reviewer ExecJudge11 — live fetch is byte-identical (sha256 6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52), and the 18-token quote is the first bullet of the doctest module introduction (offset 1250, immediately after `Source code: Lib/doctest.py` at 1009 and after the lead sentence `…executes those sessions to verify that they work exactly as shown`), so it is body content at the row's anchor and supports the checkable-claim teaches (examples are executed and compared against what is documented); the page now reads `Python 3.15.1 Documentation` where the row's scope cell pins 3.15.0 — wording unchanged, so this is anchor-version drift worth a later row refresh, not a loss of the claim.

S069 agree — reviewer ExecJudge11 — live fetch is byte-identical (sha256 52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30), and the 18-token quote is verbatim DESCRIPTION paragraph 2 (offset 826; ¶1 is the session-leader/group-leader paragraph, ¶3 is `Initially, the new session has no controlling terminal.`), exactly where the anchor points, and it states the teaches claim that the caller is the only process in the new process group and new session; §ERRORS still carries the second half of the anchor (`EPERM The process group ID of any process equals the PID of the calling process. Thus, in particular, setsid() fails if the calling process is already a process group leader.`) and the footer still reads `Linux man-pages 6.19 2026-06-05`, matching the anchor exactly.

No disputes. I looked for a reason to dispute each row and none held up: no quote is a title/nav/footer/cookie string, none is copied from the row's own cells (`quote copied from row` false for all three), and none sits away from its anchor.

## sha256 provenance (live vs entry vs gunzipped snapshot)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecJudge11/S0XX.live '<entry.url>'
$ gunzip -c .ufo/evidence/round-45/freshness/sources/S0XX.raw.gz > /tmp/tameshi-r45-ExecJudge11/S0XX.snap
S052 https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/   47923 bytes   live b19e6ca97778551a09fcc772e50c33f711c374817e34248fef1fdf42cb754c8c  snap b19e6ca9…754c8c  entry b19e6ca9…754c8c
S055 https://docs.python.org/3/library/doctest.html                                 216574 bytes  live 6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52  snap 6f6c1467…ca52    entry 6f6c1467…ca52
S069 https://man7.org/linux/man-pages/man2/setsid.2.html                             11555 bytes   live 52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30  snap 52cbc190…7f30    entry 52cbc190…7f30
```

`git -C <lane> show ad5942c:…/sources/S0XX.raw.gz | gunzip -c | sha256sum` reproduced the same three digests, so the bytes the counter will read at the deciding revision are the bytes I fetched live. Live == snapshot == entry for all three: provenance confirmed, no dynamic page chrome, so no `--extract` fallback on live bytes was needed (I extracted the snapshots for the context check anyway).

Ledger entries for all three are identical at `ad5942c6e9858af19d00000b58439b321ddfa62b` and at the current tip `1f9266a` (compared field-by-field).

## Located context (a few words either side of each quote)

S052 (`--extract` normalized text, offset 824):
```
… The difference in support is listed below. Support [Mutator StrykerJS Stryker.NET Stryker4s Arithmetic Operator ✅ ✅ ❌ Array Declaration ✅ ✅ ❌ Assignment Expression ❌ ✅ n/a] Block Statement ✅ ✅ ❌ Boolean Literal ✅ ✅ ✅ Checked Statement n/a ✅ n/a Conditional Expression ✅ ✅ ✅ Equality Operator ✅ ✅ ✅ … String Literal ✅ ✅ ✅
```
The quote is the table header plus three data rows of the §Support table the anchor names; the families the teaches lists that fall outside the quote (conditional, equality, string literal, boolean) are the adjacent rows of the same table, so the anchor as a whole supports the teaches. `Unsupported`/`Ignored mutations` do not appear on the page — the support/unsupported distinction is carried only by the ✅/❌ columns, which is what the teaches asserts.

S055 (offset 1250):
```
… The doctest module searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work exactly as shown. There are several common ways to use doctest: [To check that a module's docstrings are up-to-date by verifying that all interactive examples still work as documented.] To perform regression testing by verifying that interactive examples from a test file or a test object work as expected. …
```

S069 (offset 826):
```
… The calling process also becomes the process group leader of a new process group in the session (i.e., its process group ID is made the same as its process ID). [The calling process will be the only process in the new process group and in the new session.] Initially, the new session has no controlling terminal. For details of how a session acquires a controlling terminal, see credentials(7).
```
The teaches' third element (a group-directed signal to the old group does not reach the caller) is flagged `[INFERENCE: … killpg is not named on this page]` in the row itself, so it is not claimed as page content and its absence from the quote is not a defect.

## Counter check (seat helper, not a measurement)

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane <lane> --rev ad5942c6e9858af19d00000b58439b321ddfa62b --check /tmp/tameshi-r45-ExecJudge11/S0XX.entry.json
CHECK S052 verified ok      (exit 0)
CHECK S055 verified ok      (exit 0)
CHECK S069 verified ok      (exit 0)
```
The mechanical predicate and my independent reading agree; no row needed the overlap/length escape hatch.

## Integration notes for L1

- Review records are at `/tmp/tameshi-r45-ExecJudge11/reviews.json` (3 entries, `report` = `.ufo/waves/round-45/w2/ExecJudge11.md`, verdicts all `agree`). They must be merged into `.ufo/evidence/round-45/freshness/reviews.json` (absent from the lane right now — `measure.py:57` `REVIEWS`), otherwise `review_sets()` counts none of them.
- `review_sets()` also requires the reviewer name to appear in the orchestrator-written `.ufo/waves/round-45/w2-results.json` seats (`measure.py:192-217`), and this report must be committed at the deciding revision and name both the id and `ExecJudge11` — it does, per row.
- One non-blocking observation for a later row refresh (not a C1 dispute, and not something I changed): S055 `corpus/SOURCES.md:64` scope cell pins `Python 3.15.0 documentation`, live page is `Python 3.15.1 Documentation` (`Last updated on Oct 25, 2026 (18:32 UTC)`). Quote text identical.

## Tools / blockers

- No tools installed or upgraded (curl, python3, git, gzip already present; pacman paused per operator directive and not needed).
- Blockers: none. Nothing written outside `/tmp/tameshi-r45-ExecJudge11/` and this report.
