seat: T46RevEntryFalseRed
item: non-author claim-vs-source review of corpus/knowledge/r9-false-red-rate.md (row S260; snapshot .ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json); drafted by wave-1 seat ScribeEntryFalseRed, not by me.

# Verdict: ADMIT

Every check below was run with a method independent of the lane's counter: my own `json` decode + `html.parser` strip of `entry.content.$t` into whitespace-folded plain text, then substring tests (`/tmp/tameshi-r46-T46RevEntryFalseRed/check.py`). The lane counter is never the source of any finding; where it is mentioned it is labelled "observed".

# 1. Header trio — exact

| line | check | result |
|---|---|---|
| 1 `source:` | row id S260 = `adoption-map.json` target of staged S216 (the feed document); the quoted title `"Flaky Tests at Google and How We Mitigate Them"` is verbatim `entry.title.$t`; `(Micco, 2016-05-27)` matches `category term:"John Micco"`, body line `<i>by John Micco</i>` and `entry.published.$t=2016-05-27T17:31:00.000-07:00`; sha256 prefix `434d8658…` equals `sha256sum` of the snapshot → `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929` | OK |
| 2 | `verified-at: 2026-10-25` | OK |
| 3 `recheck:` | I RAN all three commands. `curl -fsSL 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' \| sha256sum` → `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  -` (byte-identical to committed snapshot, 8,353 B); `… \| grep -c '84% of the transitions we observe from pass to fail'` → `1`; `… \| grep -c 'Almost 16% of our tests have some level of flakiness'` → `1`. Stated outputs match observed. | OK |

# 2. Quoted spans — 21 total, all located, all token counts truthful

My decode: `json.loads` → `entry.content.$t` → `html.parser` (skips script/style, convert_charrefs) → NFKC + whitespace fold. Entry quotes extracted with `"([^"\n]{6,400})"` + curly-quote variant; `(N words)` tail annotation compared to my own whitespace token count.

- 18 body quotes: every one a verbatim substring of the stripped body text; all 18 declared `(N words)` counts equal my counts exactly (15/14/11, 13/15, 15, 13/17/12/9, 15/14/16, 18/19/20/16, 17). Zero lies.
- 2 short inference-line quotes (`"flaked three times in a row"` 6 tok, `"broken"` 1 tok, line 29): verbatim substrings; no declared counts.
- 1 header quote (the title): verbatim in the folded raw JSON (`entry.title.$t`); the entry cites it as the post title, which is where it sits.
- Location claim: entry line 10 says citations "name the field" — confirmed, all inside `entry.content.$t`; snapshot is one line (`0` newlines, `0` literal `<`, `40` `\u003C` escapes, 8,353 B) — all stated values verified.
- Fresh vs package: of the in-range (6–25-token) located quotes, 16 do not occur in the folded package copy (`fold(package)`) — the contract needs ≥1. Package-shared: the 84% sentence, the 15-tests sentence, the masking sentence, and the title quote — consistent with `ScribeEntryFalseRed.md` §19.

# 3. Numbers and names in the body — all sourced or labelled

Every body figure found in the snapshot text: 1.5% result rate, 16% reach, 1 in 7, 84% transitions, 3-times-in-a-row, 45 minutes, "15 minute integration test" (body reads "Imagine a 15 minute integration test marked as flaky"), 1000 tests, 8,353-byte/0-newline snapshot shape. Non-snapshot facts are either labelled `**Inference —` (five bullets, lines 28–32) or confined to `## What is not claimed`: the package's 0.02-cent rerun price, $5.67 investigation and 95%-floor attribution to S156 appear nowhere in the entry — `grep -n '5\.67\|0\.02\|95%\|95 %\|S212\|S216' r9-false-red-rate.md` → only line 39's description of the drop; `grep` for those figures over corpus/SOURCES.md and corpus/knowledge/ → no hits, so the "lane holds no row carrying those prices" bullet is true (lane S156 is the PIT FAQ row, no percentage). Cross-references verified: S026 is the rendered page (`SOURCES.md:37`); `repeated-control-precondition.md:20` does quote the 84% sentence; the row's `post id tag:blogger.com,1999:blog-15045980.post-6277555988217606236` and `entry.link[rel=alternate].href` → the S026 URL both confirmed in the JSON.

# 4. Registration

- `corpus/SOURCES.md:135` S260 row: used-by cell (cell 12) = `corpus/knowledge/r9-false-red-rate.md` — exact entry path; anchor names the snapshot path + `sha256 434d8658`; status `mined`; 13 cells.
- `corpus/README.md:575`: `` `knowledge/r9-false-red-rate.md` `` backticked in the round-46 table — indexed.
- Observed (not a verdict; the deciding run is the L1's): `python3 .ufo/evidence/round-46/coverage/measure.py --lane LANE --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32` → `ENTRY corpus/knowledge/r9-false-red-rate.md`, `self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 … C3_R46_PASS=true`, exit 0.

# 5. Package vs entry — claims dropped, claims added

Dropped from the package copy (`.ufo/evidence/round-46/assimilation/package/r9-false-red-rate.md`): the 0.02-cent rerun price and $5.67 manual-investigation price (round-8 own-work figures); the >95% detection floor attributed to S156; the cadence-cost-model argument built on those prices; ground line F7-only → now F3+F7; "What is still unknown" → "What is not claimed". All dropped figures are correctly absent rather than restated — the lane holds no row for them and the feed snapshot states none (`grep` counts 0 for each in the raw snapshot).

Added by the entry (all snapshot-grounded, verified located): the flake definition; the 1.5% steady-state/insertion-equals-fix-rate claim; the 16% and 1-in-7 reach figures; the monitor-wait/rerun-as-delay mechanism; "the average project contains 1000 or so individual tests"; the declared-flaky 3-in-a-row gate; the explicit 45-minute discovery latency; the "human nature" generalisation; the quarantine tool and its race-condition masking caveat; the publisher's correlation direction; the S026 same-document/dual-carrier framing; five labelled Inference bullets (false-red prior, same-job rerun blindness, discovery-latency term, suppression-without-floor, variance prior) — every one grounded in the now-carried quotes.

# Findings

- **LOW** — Headline gloss "Four red builds in five are not defects" (line 6) restates "about 84%" as 4/5 = 80%; an approximation, not a quote, and the exact figure is given with its source two sentences later. The body is unambiguous, so admission is unaffected; a fix would read "about four in five". Not blocking.
- **INFO** — Adjacent, outside this entry: `corpus/README.md:577` reiterates the carrier rationale "the rendered page's body sits in a script template that the lane's HTML extract[or] discards", which `ScribeEntryFalseRed.md` §39 already reported as contradicted by the artifacts (the body is extractable from the rendered page). The entry under review does not repeat that claim — it only states the feed is a second carrier of an already-held document, which is true. Owner: README/lesson text, not this file.
- Everything else: no unreproduced claims; no finding severe enough to block admission. Flip condition for REFUSE: none found; would require a quote that fails verbatim substring or a token-count lie — observed none (21/21 located, 18/18 counts exact).

# Method and bounds

Independent extraction (json + html.parser, NFKC fold) in `/tmp/tameshi-r46-T46RevEntryFalseRed/` (`check.py`, `live-feed.json`). Lane writes: this report only. No commits, no jj mutation, no writes to the read-only package or the fleet repo. No tools installed; no pacman transaction. Unrun: the deciding counter run (the L1's); other rows'/entries' reviews (sibling seats).
