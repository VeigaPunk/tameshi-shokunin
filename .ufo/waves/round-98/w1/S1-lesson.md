# R98S1 — lesson fragments for `corpus/lessons/round-98.md`

> Draft by seat R98S1 (scribe). Sections `## Gate`, `## Mistakes`, `## Registry changes` in
> the round-97 lesson's shape. Every receipt line quoted here was read from a blob committed
> at `764aca97e513d650949999362cd4b0f5f0e566a5` (`git show`), except the round-97 SOURCES
> cells read at `29734beb095984038d66bb5dd4d149d81378de31`. Wave-artifact citations name
> their path and must land with the wave record.

## Gate

Sources opened this round (the L1's fetches, 2026-11-08; snapshots committed at `764aca97`
under `.ufo/evidence/round-98/sources/`). Located quotes use the lane renderer
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py:strip_tags`: script/style removed, each tag
replaced by one space, entities unescaped, lines right-trimmed). Word counts are
`len(quote.split())`.

- S012 (re-opened, tier B) "Oracles That Cannot Fail" (Canedo), `https://arxiv.org/abs/2608.17214`,
  fetched 2026-11-08 (HTTP date `Sun, 08 Nov 2026 15:46:31 GMT`; 42588 B; snapshot
  `s012.html` sha256 `fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80`),
  line 112 under the same renderer: "A test oracle that obtains its expected value from the
  system it is judging cannot fail." (16 words) — grounds C1's class: a comparison whose
  recorded side is a constant has no measurement to move, so it cannot fail; S012 names the
  dual direction (the expectation itself flowing from the system under test). `used-by`
  gains `corpus/knowledge/control-assertion-anchoring.md`.
- S009 (probed, not re-opened) `https://discovery.ucl.ac.uk/id/eprint/1499169/`: the L1's
  fetch on 2026-11-08 returned HTTP 403 (5517 B, sha256
  `d04c1de85d861c7c846e1dd39d576f352035acb8866b4ecdf56d6c5733d3e75e`, headers
  `cf-mitigated: challenge`, `date: Sun, 08 Nov 2026 15:46:44 GMT`), a challenge page with no
  abstract. The wave scout's fetch with a declared user agent returned HTTP 200, 42254 B,
  sha256 `be3f85dbdb766ab8d1935145099d77b3888915e0220183511253b5c1fa29ed7c`
  (`date: Sun, 08 Nov 2026 16:13:38 GMT`), and the default `curl/8.23.0` UA re-fetched the
  403 in the same minute while two distinct non-default UAs fetched the 42254 B page
  byte-identically (`.ufo/waves/round-98/w1/R98SC1-fetch.out`). The same-minute control shows
  the challenge is keyed on the user agent, so the round-97 spot-check's 200 and the round-98
  L1's 403 — both fetches whose UA the closures did not record as non-default — are recorded
  as host- and UA-bound observations, not as a row fact. The abstract is at renderer line 413 of the
  scout's snapshot; candidate quote for the next round (14 words): "Identifying equivalent
  mutants remains the largest impediment to the widespread uptake of mutation testing."
  No verdict is recorded from the 403 page: the row stays `queued` this round, its flip
  condition is **met under a declared UA**, and the next round re-opens it with that UA —
  quoting a rate sentence, not the row's "identical compiled output" clause.

Refused / not opened this round: **none beyond S009's probe.** No new row is written.

Registry changes are in §Registry changes.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **an append-only registry cell edited in place** (mined from round 97): the `anchor` cells of S006 and S159 gained round-97 re-open text; `CORPUS.md` §SOURCES.md rule 2 allows only `status`, `recheck` and `used-by` to change in place, and every other cell is frozen. | `git diff --numstat 0b19af5f..29734beb -- corpus/SOURCES.md` → `2 2 corpus/SOURCES.md` (two rows replaced, each gaining text only in its `anchor` cell; the exact old → new text is in §Registry changes). The census exits 0 before and after — it checks row shape, not cell mutability. | the non-author round-97 spot-check (D-1): no lane instrument compared cell values between revisions. | `tools/registry-cell-immutability.py` measures the class: the red pair `--from 0b19af5f --to 29734beb` prints `REGISTRY_CELL S006:anchor changed`, `REGISTRY_CELL S159:anchor changed`, `REGISTRY_IMMUTABLE from=0b19af5f8666 to=29734beb0959 shared=183 changed=2 removed=0 added=0`, `rc=1` (`.ufo/evidence/round-98/pre-freeze/registry-red-r96-r97.out`); the green pair `29734beb..d32043ec` prints `changed=0 removed=0 added=0`, `rc=0` (`registry-green-r97-instr.out`); selftest `REGISTRY_IMMUTABLE_SELFTEST: 10/10 pass` (`registry-selftest.out`). Remedy is append-only: the cells stay as landed, logged old → new in §Registry changes. |
| M2 | **an instrument whose exit code is not its verdict**: the round-98 battery at `6b1428c8` ended `if __name__ == "__main__": main()`, so `main()`'s `return 1` for the red arm was discarded and the process exited 0 while printing the failing verdict. | the committed one-line repair `6b1428c8..d32043ec` (the single line `main()` replaced by `sys.exit(main())`; commit subject `round-98: instruments — guard refusal battery exits on its verdict`). No committed receipt of the broken run exists: a replay of the committed blob at `6b1428c8` against `--red state-unbuildable` prints `GUARD_REFUSALS_RED state-unbuildable missed-as-declared rc=0`, `GUARD_REFUSALS classes=6 refused=5 wrong=1 positive=ok red=state-unbuildable`, then `rc=0` (scribe R98S1 replay; command and environment in the seat report). | the red arm's verdict line against the process exit — the receipt writer's `rc=` field, which the fixed run records as `rc=1`. | `sys.exit(main())`; the committed `c2-refusals-red.out` prints the same two lines and `rc=1`, which is the receipt that shows the fix able to fail. |

Sweep for an inherited mistake: the round-97 spot-check's D-1…D-7 are this round's work
items (D-1/M1 above, D-2/C1, D-3, D-4, D-5, D-6/C2, D-7); nothing else in that closure is
left unrouted, and the round-97 lesson's own M1–M4 were already mined.

## Registry changes

No row is added, removed, retired or status-changed this round.

- `used-by` change, old → new: S012
  `corpus/knowledge/oracle-anchored-survivors.md` →
  `corpus/knowledge/oracle-anchored-survivors.md, corpus/knowledge/control-assertion-anchoring.md`.
  `status` stays `mined`; `recheck` stays `90d`; no other cell of S012 changes.

Round-97 in-place `anchor` edits, logged old → new (spot-check D-1, append-only remedy B: the
cells are not rewritten a second time; the class is measured by
`tools/registry-cell-immutability.py`, M1):

- S006 `anchor` old: `README §The three verdicts and §How a row is run @ page currentOid
  7eefc73010ad6342b80e3ed43915503e02c90618, fetched 2026-10-19`; new (round 97):
  `README §The three verdicts and §How a row is run @ page currentOid
  7eefc73010ad6342b80e3ed43915503e02c90618, fetched 2026-10-19; re-opened 2026-11-08:
  snapshot .ufo/evidence/round-97/sources/s006.html 281627 B sha256 55bb7196, lines 490-492
  under the same renderer`. The added text belongs in a Gate record, not the anchor cell.
- S159 `anchor` old: `§Mutation testing overview, p ids mw-Q and mw-w, and §Overview p mw-Q @
  page fetched 2026-10-25, snapshot .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html
  170793 B sha256 6e4a06c0 revid 1373580212`; new (round 97): `§Mutation testing overview,
  p ids mw-Q and mw-w, and §Overview p mw-Q @ page fetched 2026-10-25, snapshot
  .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html 170793 B sha256 6e4a06c0
  revid 1373580212; re-opened 2026-11-08: snapshot .ufo/evidence/round-97/sources/s159.html
  171636 B sha256 4b5a8374, line 762 under the lane renderer (script/style and comments
  removed, each tag to one space, entities unescaped, lines right-trimmed)`. Same
  disposition.

Census before: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` exits 0 with the standing W01/W04 advisories only
(`.ufo/waves/round-98/census-before.txt`, committed at `764aca97`: 22 warning lines and the
`ok` line). Population at the freeze: 183 rows (A 165 · B 14 · C 4), mined 149 · queued 23 ·
rejected 11 (counted from `corpus/SOURCES.md`; no row changes this round). Census after:
`<TO FILL AT RECORDS>` (the records run rewrites `.ufo/waves/round-98/census-after.txt`).
