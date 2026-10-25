seat: ScribeEntryFalseRed
item: re-grounded the package entry r9-false-red-rate.md against the committed Google per-post feed snapshot (S260) as a C3 deliverable entry, dropping every figure the lane does not hold

# What was built

`.ufo/waves/round-46/w1/ScribeEntryFalseRed.entry.md` (7,584 B, to land as `corpus/knowledge/r9-false-red-rate.md` — the exact used-by path `ScribeRows`' item already names for S260). Header is the spec header verbatim; body separates observation from `Inference:` and names what is dropped.

Checks run against it, all from `/tmp/tameshi-r46-ScribeEntryFalseRed/`:

| check | command | output |
|---|---|---|
| header line 1 exact | python string compare to the item's line 1 | `line1 exact: True` |
| header line 2 | `== 'verified-at: 2026-10-25'` | `line2 exact: True` |
| header line 3 | `startswith('recheck: 365d — ')` | `True` |
| line 4 | read | `ground: F3 (determinism precondition, flaky-aware verdicts) — …; F7 (incremental re-sweep granularity) — …` |
| stated quote word counts | 18 `(N words)` tails compared to `fold()` token counts via the counter's own `QUOTE_RE`/`fold` | `stated-count mismatches: []`, `quotes with stated count: 18` |
| located vs fresh quotes | imported `measure.py`, applied `QUOTE_RE`+`fold`+`norm_text` | `located quotes: 20 fresh: 16` |

The 16 fresh located quotes (none occurs in the package copy) include: `a test that exhibits both a passing and a failing result with the same code` (15), `we see a continual rate of about 1.5% of all test runs reporting a` (14), `Almost 16% of our tests have some level of flakiness associated with them` (13), `The breakage will not be discovered until 3 executions of the test complete, or 45 minutes` (16), `could easily mask a real race condition or some other bug in the code being tested` (16), `we are seeing promising correlations with features that should enable us to identify a flaky result accurately` (17). The four located-but-package quotes are the title string, the 84% transition sentence, the 15-tests sentence and the masking sentence.

# Gates (run; not a verdict)

Scratch harness only: `D=$(mktemp -d …)` under `/tmp/tameshi-r46-ScribeEntryFalseRed/`, `git -C "$D" init -q -b m`, `git -C "$D" rev-parse --show-toplevel` → equals `$D` (`toplevel ok: True`) before the first commit; every commit inside `$D` with `-c user.name=t -c user.email=t@t`. The harness carried byte copies of the round-46 `measure.py`, the committed S260 snapshot, the package copy, a synthesized S260 row (13 cells, anchor `.ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json sha256 434d8658`, used-by `corpus/knowledge/r9-false-red-rate.md`), my entry and a README index line.

1. Entry admitted: `python3 $D/.ufo/evidence/round-46/coverage/measure.py --lane $D --rev HEAD` → exit 1, stdout `ENTRY corpus/knowledge/r9-false-red-rate.md` / `C3_R46: self_pin=1 rows=1 entries=1 indexed=1 covered=1 row_ids=S260 rev=HEAD C3_R46_PASS=false`. `PASS=false` is structural: `rows=1` because only S260 exists in the harness; `entries=1 indexed=1 covered=1` and the un-suffixed `ENTRY` line are the admission of this entry.
1b. Re-run with the **actual drafted row**: `ScribeRows.rows.md` line `| S260 | …` (13 cells after `split('|')`) substituted for my synthesized row → same output `ENTRY corpus/knowledge/r9-false-red-rate.md` / `C3_R46: self_pin=1 rows=1 entries=1 indexed=1 covered=1 row_ids=S260 … C3_R46_PASS=false`, exit 1. The row's anchor digest `434d8658`, its `mined` status, its `doc_key` and its used-by `corpus/knowledge/r9-false-red-rate.md` all satisfy `flaky_rows`/`entry_ok`.
2. Negative control, package-shared quotes only: `REFUSED corpus/knowledge/r9-false-red-rate.md no quote fresh against the package copy`, `entries=0`.
3. Negative control, one unlocatable quote plus the 84% sentence: `REFUSED … no quote fresh against the package copy`, `entries=0` (the counter's reason label is coarse; the 84% quote is located but package-held, so the refusal is correct either way).

Not run: the counter's `--selftest`, and any deciding run — those are the L1's. The harness verdict is not reported as a C3 pass.

# Provenance of the snapshot (re-verified live)

- `curl -fsSL 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' | sha256sum` → `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  -`; identical to the committed snapshot's `sha256sum` (`434d8658…9929`, 8,353 B). Same command with `| grep -c '84% of the transitions we observe from pass to fail'` → `1`, and `| grep -c 'Almost 16% of our tests have some level of flakiness'` → `1`.
- `python3 .ufo/evidence/round-45/freshness/measure.py --extract <snapshot>` → exit 0, 1 line; `grep -cF` on four located quotes (the 1.5%, 16%, 45-minute and race-condition sentences) → `1` each.

# Findings

1. **The item's carrier rationale is not what the artifacts show (conflict, reported verbatim).** The item says the lane cites the feed "because the rendered page's body sits in a script template the lane's HTML extraction discards". Observed: the live rendered page (`curl -fsSL 'https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html'`, 236,387 B, sha256 `5d74dd1c3c75d5ec1b8d53d6a518b4b01ae085f03006f1f44febbb8143e92296`) holds the body **twice** — `84%` occurs 2 times, of which **1** occurrence sits inside a `<script>` block; the round-46 counter's `norm_text` on that page yields `has84=True`, and the round-45 extractor's output contains `84% of the transitions`. The same holds for the round-45 snapshot `S026.raw.gz` (236,387 B after `gunzip -c`, first `84%` at byte offset 34455 in plain HTML, `script blocks containing 84%: 1`). So one copy is discarded and one survives; the feed is not required because the page's body is unextractable. I did **not** put that rationale in the entry. The entry states instead what is verifiable: the feed's `entry.link[rel=alternate].href` is the rendered page held as S026, so the feed is a second carrier of the same document.
2. **Snapshot shape.** The snapshot has `0` newlines and `0` literal `<` characters (`count u003C 40`, `literal < 0`), so the counter's `norm_text` does **not** enter its HTML branch for this file; the searched text is the folded raw JSON, where the body appears as `\u003C…\u003E`-escaped HTML and inner quotes as `\"`. Every quote I chose therefore lies inside one unescaped text run; quotes that would span an escape sequence are absent.
3. **Arithmetic dropped, with the held rows checked.** `grep -n 'S156' corpus/SOURCES.md` → the only row is line 126, whose text is run-dependence of PIT verdicts ("two factors, timeouts and static initializers, can make results differ between runs with the same input …") — it carries no detection-floor percentage. `grep -n '5\.67\|0\.02\|95%\|95 %' corpus/SOURCES.md` → no hits; `grep -rln '5\.67\|0\.02 cents' corpus/knowledge/` → no hits. The rerun price, the investigation price and the 95% floor are therefore not restated anywhere in the entry; the "What is not claimed" section names them as dropped without repeating their values.
4. **Rows and index are not mine and are absent now.** `grep -n 'S258\|S259\|S260' corpus/SOURCES.md` → one hit, line 467 `- Next unused id: S258 …`; no row exists yet, so `rows>=3` cannot be satisfied by this seat. `grep -n 'r9-false-red\|false-red' corpus/README.md` → no hits, so the entry is not indexed yet; the counter requires `knowledge/r9-false-red-rate.md` (or `corpus/knowledge/…`) backticked in `corpus/README.md`. QUALITY criterion 7 (entry lands with its coverage-map row) is therefore an open dependency on `ScribeRows`/the integrator. I messaged `ScribeRows` confirming the basename, the `434d8658` prefix and the single-line-JSON shape.
5. **Criterion 51 is not triggered.** The entry vouches for no tool bytes; the digest it names is the snapshot's, on line 1, and the recheck line carries the live re-fetch digest.

# Touched surfaces

- Written: `.ufo/waves/round-46/w1/ScribeEntryFalseRed.entry.md` (deliverable) and this report `.ufo/waves/round-46/w1/ScribeEntryFalseRed.md`.
- Read only: `.ufo/evidence/round-46/contract.json`, `.ufo/evidence/round-46/coverage/{measure.py,sources/*}`, `.ufo/evidence/round-46/assimilation/package/r9-false-red-rate.md`, `.ufo/evidence/round-45/freshness/{measure.py,sources/S026.raw.gz}`, `.ufo/waves/round-46/w1/swarm-registry.json`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `PROVINCE.md`.
- No lane git/jj state touched; no mutating command run in the lane; the read-only package `/home/vgpnk/Projects/shokuknow` was not touched.

# Out of scope / left to others

- Rows S258/S259/S260 (`ScribeRows`), `corpus/README.md` indexing, the deciding counter run and the counter selftest (L1), the province/quality verdict (`RevProvince`), the cheap-pass attack (`CritC3Control`).

# Tooling

No install or upgrade; no pacman transaction. Scratch: `/tmp/tameshi-r46-ScribeEntryFalseRed/` (harness `c3-harness-oslnrm8c/`, `extract45.txt`, `snapshot-norm.txt`, `snapshot-plain.txt`, `live-feed.json`, `live-rendered.html`, `s026.html`).

# Known limits

- Admission evidence comes from a single-row scratch harness; the row used in the second run is `ScribeRows`' real drafted S260 row, but the remaining two rows (S258, S259) and the `corpus/README.md` index line are other seats' deliverables and were not present to test against.
- Quote freshness is measured against the package copy as committed at the freeze; a later edit to that copy could change which of my 16 quotes count as fresh, though 16 gives a wide margin over the required one.
- The 84% and 1.5% figures remain one company's system in 2016; the entry says so and draws no transfer claim.
