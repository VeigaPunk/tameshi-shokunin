seat: CritJudge02

# Round-45 w2 — C1 falsify: independent re-judgment of S004, S024, S048

Inputs read (none authored by me): `.ufo/evidence/round-45/contract.json` (read only, unedited),
`.ufo/evidence/round-45/freshness/ledger.json` at `ad5942c6e9858af19d00000b58439b321ddfa62b`
(`git show ad5942c6:…/ledger.json | sha256sum` = `433a624bf8cdd42ccf2ea2a818aa0bdc40dd2c77cd636e1121d0aa51eb5a9913` =
the working-tree file), the three committed snapshots under `.ufo/evidence/round-45/freshness/sources/`,
registry rows `corpus/SOURCES.md:15` (S004), `:35` (S024), `:57` (S048), and the author reports
`.ufo/waves/round-45/w1/ExecRows02.md`, `ExecRows04.md`, `ExecRows05.md`. Authors are ExecRows02 /
ExecRows04 / ExecRows05; I am none of them. Scratch dir `/tmp/tameshi-r45-CritJudge02/`; the lane was
read-only for me except this report. No tool installs or upgrades were performed (curl, python3, gzip
already present; pacman is host-paused and was not used).

## Verdicts

S004 agree — reviewer CritJudge02 — sha256 equal (today's live fetch, the entry's `raw_sha256` and the gunzipped snapshot are all `5ec9ba95…`), and the 23-token quote is the complete body sentence of the row's own anchored section `h2#tests-fail-in-an-clean-tree` (h2 at raw 15226, quote at 15558, next h2 `mutant-outcomes` at 15716, enclosing `<p>` 15355-15711) stating that `cargo test` must pass reliably in a copied tree before anything runs, which is the teaches' second clause; the other clauses are still in the same snapshot (§Mutant outcomes: `caught`, `missed`, `unviable - … This is inconclusive about test coverage`, `timeout`), and the companion `in-diff.html` / `iterate.html` pages the source cell names each still carry their `Caution` paragraph (checked live this session, not part of the committed snapshot).
S024 agree — reviewer CritJudge02 — sha256 equal (live, entry and snapshot all `3abede35…`), and the 17-token quote is body prose in a `<p>` (271981-272197) asserting "Delta Debugging is a simple and robust reduction algorithm. We can tie a `DeltaDebuggingReducer` to this runner", immediately followed in the same passage by the ZeroDivisionRunner FAIL-on-ZeroDivisionError definition, `dd.reduce(python_input) → '3/0'` and "The input is reduced to the minimum", i.e. the runnable-reducer teaches — with the recorded caveat that the quote sits in `h2#Synopsis` (raw 266347), not in the row's anchored `h2#Delta-Debugging` (raw 297699), so the ledger note's phrase "the §Delta Debugging passage" misattributes the section (see Corrections).
S048 dispute — reviewer CritJudge02 — sha256 equal (live, entry and snapshot all `e9cbc3e1…`), but the 14-token quote is only item 4's antecedent, truncated inside the same `<li>` at "has changed" (`<li>` raw 3786-4000, quote 3790-3868, 132 chars of the item dropped) and the dropped consequent "then it is likely that the last killing test will still kill it and it should therefore be prioritised above others" is the only part that states the teaches ("item 4 is prioritisation rather than a reuse skip"); as recorded it asserts nothing and is textually indistinguishable from the preceding reuse-skip item's premise.

## sha256 comparison lines

```
$ for id in S004 S024 S048; do curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-CritJudge02/$id.live '<entry.url>'; done
$ sha256sum S004.live S024.live S048.live
5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334  S004.live
3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99  S024.live
e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db  S048.live
$ for id in S004 S024 S048; do gunzip -c …/.ufo/evidence/round-45/freshness/sources/$id.raw.gz > /tmp/tameshi-r45-CritJudge02/$id.snap; done
$ sha256sum /tmp/tameshi-r45-CritJudge02/*.snap
5ec9ba952d4d2c12fc2e775965b4138cfdb5dc13b7cff392344383093f012334  S004.snap
3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99  S024.snap
e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db  S048.snap
```

Live = ledger `raw_sha256` = gunzipped snapshot for all three rows: provenance confirmed; no
dynamic-chrome divergence, so the `--extract` fallback was not needed. Cross-check that the
snapshot is today's page and not an older blob: `measure.py --extract` output of each `.live` file is
byte-identical to that of its `.snap` (`cmp -s` → identical for S004, S024, S048).

## Located context (few words either side of each quote, from the `--extract` normalized text)

S004 — inside the anchored section, `<p>` 15355-15711:
```
… passing when run from a different location. Fix this first: cargo-mutants can't do anything until you
have a tree where cargo test passes reliably when copied to a temporary directory. </p>
<h2 id="mutant-outcomes">Mutant outcomes</h2> …
```
23 tokens, complete sentence, not a title/nav/footer/cookie/menu fragment, not a bare code block;
absent verbatim from `corpus/SOURCES.md` (`q.lower() in fold(cells).lower()` → False); shared content
words with scope+anchor+teaches = `cargo, copied, first, mutants, reliably, tree` (6).

S024 — `<p>` 271981-272197, section `h2#Synopsis`:
```
… >>> outcome 'FAIL'  Delta Debugging is a simple and robust reduction algorithm. We can tie a
DeltaDebuggingReducer to this runner, and have it determine the substring that causes the python program
to fail: >>> dd = DeltaDebuggingReducer(python_runner) >>> dd.reduce(python_input) '3/0'
The input is reduced to the minimum …
```
17 tokens; absent verbatim from the registry cells (False); shared content words = `debugging, delta,
runner` (3). Section check: the enclosing heading is `h2#Synopsis` (266347); `h2#Why-Reducing?` 283651,
`h2#Manual-Input-Reduction` 292554, `h2#Delta-Debugging` 297699 — the quote is not in the anchored
section. The anchored section was checked independently and still carries the runnable reducer:
`class DeltaDebuggingReducer ( CachingReducer )`, its `reduce()` body using `Runner.FAIL`, and
"To see how the DeltaDebuggingReducer works, let us run it on our failing input … until only two
characters remain".

S048 — item 4 of the ordered list, `<li>` 3786-4000, section `h1#incremental-analysis` (2840):
```
<li>If a mutation was previously killed, but the class or killing test has changed then it is likely that
the last killing test will still kill it and it should therefore be prioritised above others.
(since 1.14.4)</li>
```
The quote covers only the first 14 tokens and stops mid-item; the assertion (prioritisation) is in the
dropped tail. Absent verbatim from the registry cells (False); shared content words = `mutation, test`
(2) — the counter's bare minimum, which is exactly why the counter passes while the quote says nothing.
The rest of the page is unchanged (`(not yet implemented)` still on item 5, the dependency paragraph
still reads "it is currently unproven"), so the row's claim is live; the defect is the quote, not the row.

## S048 — smallest safe correction, and why re-quoting alone does not fix it

The obvious repair — quote the consequent instead — does not satisfy the frozen counter's own
`>= 2` shared-content-word rule. Exhaustive scan over the snapshot's normalized text for every
6-25-token span containing `prioritised`:

```
$ python3 - <<'EOF'   # measure.py words()/cells reused
… for n in 6..25, every window containing 'prioritised': max shared content words = 1
EOF
candidates with >=2 shared content words: 0
max shared for spans containing "prioritised": (1, 25, 'then it is likely that the last killing test will
still kill it and it should therefore be prioritised above others. (since 1.14.4) If a')
```

`prioritised` occurs once on the page and the row's cells only tokenize to `prioritisation`/`mutation`/
`test`/…, so no compliant quote can carry the prioritisation clause. The smallest safe correction is
therefore at row/counter level, not at quote level: either (a) reword S048's `teaches` cell to the clause
that is quotable (the changed-class-or-killer premise plus the "(since 1.14.4)" status), or (b) accept the
premise quote only with a contract-level allowance — and (b) is unavailable mid-round because the
contract records amendments as pre-data only. As the entry stands, the quote does not state the claim:
dispute.

## Corrections requested (not claim failures)

- S024 ledger `note` says "Live Reducer.html still has the §Delta Debugging passage: …". The passage it
  describes is in `h2#Synopsis` (raw 266347-283651), not `h2#Delta-Debugging` (297699). Wording fix only;
  the row's verdict `holds` is right and the anchored section does still carry the reducer class.
- S024 row `anchor` (`corpus/SOURCES.md:35`) names "§Delta Debugging", but no 6-25-token paragraph in that
  section shares ≥2 content words with the cells (all 23 `<p>` elements of 6-25 tokens: max 1, on
  `input`/`fail`), so the anchor cannot host a compliant quote; the anchor is imprecise rather than wrong.
- S004 ledger `note` also asserts the companion `in-diff.html` / `iterate.html` Caution sections. That is
  true (verified live: `Caution --in-diff makes tests faster …`, `Caution --iterate is a heuristic …`,
  sha256 `05f1cdef…` / `a4805774…`), but neither page is in the committed snapshot, so the note rests on
  evidence outside the entry.

## Commands and output

```
$ grep -nE '^ {0,3}\| S(004|024|048) ' corpus/SOURCES.md
15:| S004 | cargo-mutants book: Using the results (also in-diff.html and iterate.html) — https://mutants.rs/using-results.html | … §Tests fail in an clean tree? and §Mutant outcomes …
35:| S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | … §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer …
57:| S048 | Incremental analysis (PIT docs), object-neutral precision — https://pitest.org/quickstart/incremental_analysis/ | … §Incremental analysis, numbered items 4–5 … | supersedes S047 — item 4 is prioritisation rather than a reuse skip …

$ python3 …/.ufo/evidence/round-45/freshness/measure.py --extract $id.snap
S004 5493 bytes / S024 49430 bytes / S048 3260 bytes   (quote found in each: True)

$ python3 - (measure.py words()/fold()) — counter-style checks
S004 tokens 23 shared ['cargo','copied','first','mutants','reliably','tree'] | in SOURCES.md cells: False
S024 tokens 17 shared ['debugging','delta','runner']                        | in SOURCES.md cells: False
S048 tokens 14 shared ['mutation','test']                                   | in SOURCES.md cells: False
```

No deciding run of either counter was made by this seat (no `--lane/--rev` scoring run); only
`--extract` was used, as the bounds allow. `reviews.json` for integration:
`/tmp/tameshi-r45-CritJudge02/reviews.json` (3 reviews, verdicts agree/agree/dispute, each pointing at
this report).
