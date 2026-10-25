seat: RevJudge03

# Round-45 C1 falsify — independent re-judgment of S047, S058, S099

Inputs read at commit `ad5942c6e9858af19d00000b58439b321ddfa62b` (lane `tameshi-shokunin`): ledger `.ufo/evidence/round-45/freshness/ledger.json`, committed snapshots `.ufo/evidence/round-45/freshness/sources/S{047,058,099}.raw.gz`, registry rows `corpus/SOURCES.md:56` (S047), `:67` (S058), `:107` (S099), author reports `.ufo/waves/round-45/w1/ExecRows05.md`, `ExecRows08.md`, `ExecRows19.md`. I am not the author of any of the three entries. Live fetches re-run by me on 2026-10-25; scratch and this verification used only `curl`, `gunzip`, `sha256sum`, and the frozen counter in `--extract` mode (script `/tmp/tameshi-r45-RevJudge03/verify.py` reusing the counter's own `fold`/`words`/`parse_rows` for the token, overlap and not-copied checks). No tools installed or updated.

## Verdicts

S047 agree — reviewer RevJudge03 — live sha256 equals the ledger and committed-snapshot digest `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db`; the 10-token quote was located afresh in the dependency-assumption paragraph of the anchored section, is not copied from the row's scope/anchor/teaches cells, shares `assumption`/`unproven` with teaches, and still states that the dependency assumption is unproven.

S058 agree — reviewer RevJudge03 — live PDF sha256 `d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede` equals ledger, committed snapshot and the row's anchored published-PDF digest (fetch needed one 403→browser-UA retry, then HTTP 200, 728,559 bytes); the 10-token quote sits afresh in §4.2.2 Verifying Traces body prose, is not copied from row cells, shares `trace`/`verify`/`existing` with teaches, and still says a trace verifies existing values.

S099 agree — reviewer RevJudge03 — live sha256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc` equals ledger, committed snapshot and the row's pinned 2026-10-23 digest; the 15-token quote was located afresh under the anchored "What is mutation testing?" heading, is not copied from row cells, shares `faults`/`mutations`/`seeded`/`tests` with teaches, and its killed/lived continuation still supports the seeded-mutation and test-quality claims.

## sha256 comparisons (live fetched 2026-10-25 by RevJudge03)

```
S047  live         e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db
S047  snapshot.gz  e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db   (gunzip -c | sha256sum)
S047  ledger       e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db   → all three equal

S058  live         d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede   (Mozilla/5.0 → curl 22 HTTP 403; Chrome/126 UA → 200)
S058  snapshot.gz  d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede
S058  ledger       d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede   → all three equal; also equals the anchor's published-PDF pin (corpus/SOURCES.md:67)

S099  live         b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc
S099  snapshot.gz  b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc
S099  ledger       b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc   → all three equal; also equals the anchor's 2026-10-23 pin (corpus/SOURCES.md:107)
```

Because live bytes equal snapshot bytes, each `--extract` of the snapshot and of today's live file is identical (S047 3,260 B; S058 101,696 B; S099 3,799 B), so each quote also appears in today's live text.

## Located context (snapshot normalized text, `--extract`; <<QUOTE>> marks the ledger quote)

- S047 (10 tokens): "…on the assumption that it will be relatively rare for changes in the dependencies of a class to change the status of a mutation. <<Although this assumption seems reasonable, it is currently unproven .>> Optimisation 5) carries the additional risk that the mutations within the meta mutant might cancel each other out…" — body prose of the anchored §Incremental analysis dependency paragraph; states the claim, not nav/footer/title.
- S058 (10 tokens): "…record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt — in essence <<a trace which we can use to verify existing values>>. For traces, there are two essential operations…" (the em dash extracts as `ś` in pdftotext output) — §4.2.2 Verifying Traces body; matches the anchor p. 79:14 region and the verifying-traces teaches.
- S099 (15 tokens): "…What is mutation testing? How it works in 51 words Mutation testing is conceptually quite simple. <<Faults (or mutations ) are automatically seeded into your code, then your tests are run.>> If your tests fail then the mutation is killed , if your tests pass then the mutation lived . The quality of your tests can be gauged…" — body under the anchored heading; with its continuation it grounds the teaches (seeded → rerun → killed/lived → quality gauge).

## Per-row contract checks (measured with the counter's own fold/words logic)

- Quote located afresh in snapshot normalized text: S047 yes, S058 yes, S099 yes (and in today's live text, since bytes are equal).
- Whitespace-token count in 6–25: S047 10, S058 10, S099 15.
- Not copied from the row's own scope/anchor/teaches cells (folded quote not a substring of the folded cells): S047 no, S058 no, S099 no.
- Content-word overlap (len ≥ 4, counter STOP list) with scope/anchor/teaches ≥ 2: S047 {assumption, unproven} = 2; S058 {trace, verify, existing} = 3; S099 {faults, mutations, seeded, tests} = 4.
- Ledger `url` equals the row's own URL; `opened` = 2026-10-25; entry author fields: S047 ExecRows05, S058 ExecRows08, S099 ExecRows19.

## Commands

```
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-RevJudge03/S###.live '<row url>'          # S058: retry with Chrome/126 UA after curl 22 (403)
sha256sum /tmp/tameshi-r45-RevJudge03/S###.live
gunzip -c /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/sources/S###.raw.gz | sha256sum
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-RevJudge03/S###.snap   # and on the .live file
python3 /tmp/tameshi-r45-RevJudge03/verify.py    # quote location, token count, cell-copy and overlap checks
```

Tooling authorization: nothing installed or updated (stock curl/python3/git sufficient).

Reviews file: `/tmp/tameshi-r45-RevJudge03/reviews.json` (verdicts above; report path `.ufo/waves/round-45/w2/RevJudge03.md`).
