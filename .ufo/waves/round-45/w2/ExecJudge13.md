seat: ExecJudge13

# Round-45 w2 — C1 falsify review of S001, S006, S028

Inputs read (all read-only): `.ufo/evidence/round-45/contract.json` (frozen, not edited),
`.ufo/evidence/round-45/freshness/ledger.json` at ad5942c6e9858af19d00000b58439b321ddfa62b (73 entries, one entry per id),
the three committed snapshots `.ufo/evidence/round-45/freshness/sources/{S001,S006,S028}.raw.gz`, the registry rows
`corpus/SOURCES.md:12` (S001), `:17` (S006), `:39` (S028), and the author reports `.ufo/waves/round-45/w1/ExecRows01.md`,
`ExecRows02.md`, `ExecRows04.md`. I am the author of none of the three entries (authors ExecRows01 / ExecRows02 / ExecRows04).

## Verdicts

S001 agree — reviewer ExecJudge13 — sha equal (today's live fetch, the entry's raw_sha256 and the gunzipped snapshot are all ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11), and the quote is the §Metrics table row "Mutation score detected / valid * 100" (heading at 2461, quote at 3125, next heading §Test states and metrics at 3388) with "Detected killed + timeout" at 2580 and all eight mutant states still defined in §Mutant states, so it states the score formula and state set the teaches cell claims.
S006 agree — reviewer ExecJudge13 — sha differs from the entry only as GitHub page chrome (today's live `--extract` text is byte-identical to the snapshot's, 15805 B, quote at the same offset 4579), and the quote is the §The three verdicts table rows for `unapplied` / `baseline` (heading 3866, quote 4579, next heading §How a row is run 6699) with the non-unique-literal refusal still present at 6865, so it supports the row's verdict-semantics teaches.
S028 agree — reviewer ExecJudge13 — sha equal (d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a), and the quote is body text of §Role of the test runner (heading 5208, quote 5547, next §Test sharding 8404) stating exit-zero-passes / any other result fails / PASS or FAIL on stdout has no significance, with the `LANG unset required` and `TZ UTC required` rows still at 9648 and 12526, so it supports the normative exit-code clause of teaches.

No dispute. Each quote is 6-25 whitespace tokens (15 / 22 / 20), occurs in the counter's normalized snapshot text, shares >= 2
distinct content words with scope+anchor+teaches (3 / 3 / 3: `detected score valid`, `baseline literal unapplied`, `code exit test`),
is not a substring of the folded source+scope+anchor+teaches cells (False for all three), and every entry names exactly its row's
first http(s) URL, carries `opened` 2026-10-25 and verdict `holds`.

## Commands and output

```
$ mkdir -p /tmp/tameshi-r45-ExecJudge13
$ for id in S001 S006 S028; do gunzip -c .../.ufo/evidence/round-45/freshness/sources/$id.raw.gz > /tmp/tameshi-r45-ExecJudge13/$id.snap; done
$ sha256sum /tmp/tameshi-r45-ExecJudge13/*.snap   # via gunzip -c | sha256sum
S001 snapshot: ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11  -
S006 snapshot: a61a08aa40750e29393df2c2983c2fcce216a2742352d37cf5ef6e9cb03e2263  -
S028 snapshot: d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a  -
```

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecJudge13/S###.live '<entry.url>' ; sha256sum ...
S001 rc=0 bytes=27068   ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11
S006 rc=0 bytes=323925  45420df3b7971671506ca093b2a527df8bdc1621325737e88c97be7591033db2
S028 rc=0 bytes=221292  d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a
```

sha256 comparison lines (live vs entry.raw_sha256 vs gunzip snapshot):

```
S001 live==entry==snapshot : ac2733869c64ac637a6beb6f2b315d46ca1afaa585eb5322c1a76be18698fc11  (equal, 27068 B)
S006 live!=entry==snapshot : live 45420df3b7971671506ca093b2a527df8bdc1621325737e88c97be7591033db2 ; entry==snapshot a61a08aa40750e29393df2c2983c2fcce216a2742352d37cf5ef6e9cb03e2263  (dynamic chrome)
S028 live==entry==snapshot : d12c985aff6170d53e4f2f60c4be187665df6d2921282e97b06a9b693510c55a  (equal, 221292 B)
```

S006 fallback (no `member` on any of the three entries): the live page differs from the snapshot raw bytes only in GitHub
dynamic chrome, so per the review rule the quote had to appear in today's live text too — it does, at the same offset, and the
extracts are byte-identical:

```
$ python3 .../.ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecJudge13/S006.live > S006.live.txt
$ cmp -l S006.snap.txt S006.live.txt   # no output; both 15805 bytes
S006 snapshot extract 15807 B (incl. trailing newline) / live extract 15805 B; quote found at 4579 in both
```

```
$ for id in S001 S006 S028; do python3 .../.ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecJudge13/$id.snap > $id.snap.txt; done
S001 4163 B   S006 15807 B   S028 92025 B

$ python3 .../.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecJudge13/$id.json
CHECK S001 verified ok   rc=0
CHECK S006 verified ok   rc=0
CHECK S028 verified ok   rc=0
```

Only the allowed `--extract` and `--check` modes were used; no deciding `--lane/--rev` measurement was run by this seat.

## Located context (a few words either side of the quote)

- S001, quote at offset 3125 of 4160 (15 tokens): `… Total mutants valid + invalid + ignored + pending All mutants. [Mutation score detected / valid * 100 The total percentage of mutants that were detected.] The higher, the better! Mutation score based on covered code detected …`
  Section: heading `Metrics` at 2461, quote at 3125, next heading `Test states and metrics` at 3388 — the row's own anchor (§Mutant states and §Metrics), body content, not nav/footer/cookie banner. Corroboration in the same extract: `Detected killed + timeout The number of mutants detected by your tests.` (2580), `Compile error … It is not represented in your mutation score.` (2093), and the eight states `Pending` (916), `Killed` (1051), `Survived`, `No coverage`, `Timeout` (1369), `Runtime error` (1729), `Compile error`, `Ignored` (2282).
- S006, quote at offset 4579 of 15805 (22 tokens): `… a mutation harness fails silently in exactly the way the tests it checks do: Verdict Meaning [unapplied The old literal matched nothing. The row injected no defect and tests nothing . baseline The selected tests were not green] before any defect was injected (red, or aborted: the red status with no red line), or, with SHMUTANT_COUNTS=1 , …`
  Section: heading `The three verdicts` at 3866, quote at 4579, next heading `How a row is run` at 6699 — the row's own anchor (§The three verdicts). The quote is a table excerpt whose `baseline` cell is cut mid-sentence, but the clause it carries ("selected tests were not green") is the verdict definition the teaches cell names, and the neighbouring `killed` / `survived` / `accidental` rows precede it at 3972-4460. The row's other anchored clause is still present: `A row whose old literal occurs more than once in its target there is refused: the rewrite takes the first copy, which might not be the one the row means.` (6865, §How a row is run).
- S028, quote at offset 5547 of 92023 (20 tokens): `… the result of running the test as a standalone process must be considered authoritative. [If a test process runs to completion and terminates normally with an exit code of zero, the test has passed.] Any other result is considered a test failure. In particular, writing any of the strings PASS or FAIL to stdout has no significance to the test runner. …`
  Section: body heading `Role of the test runner` at 5208 (the 1264 occurrence is the page TOC), quote at 5547, next heading `Test sharding` at 8404. The §Initial conditions rows the teaches cell names are still present: `LANG unset required` (9648), `TZ UTC required` (12526), `TEST_PREMATURE_EXIT_FILE … (used for catching calls to exit() ) optional` (10921).

## Notes / risks

- No tool installs or upgrades (curl, python3, gzip, git already present); no pacman transaction attempted (host-wide pause respected); no model passed anywhere.
- No git/jj command was run in the lane; nothing in the lane was modified except this report file. Scratch is confined to `/tmp/tameshi-r45-ExecJudge13/` (`S0*.snap`, `S0*.live`, `S0*.snap.txt`, `S0*.live.txt`, `S0*.json`, `reviews.json`).
- `reviews.json` for merging into `.ufo/evidence/round-45/freshness/reviews.json` is at `/tmp/tameshi-r45-ExecJudge13/reviews.json`; its `report` field is `.ufo/waves/round-45/w2/ExecJudge13.md`.
- Residual imprecision, recorded but not a dispute: S028's teaches cell says `TEST_PREMATURE_EXIT_FILE catches early exits` while the live page scopes it to `catching calls to exit()` and marks it `optional` — the quote I judged does not carry that clause, the exit-code clause it does carry is exactly what the page says, and S081 is the precise superseding row for that wording.
- Nothing here changes the population, the target or the frozen contract; all three entries would also be `verified` on the counter's own predicate.
