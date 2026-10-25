seat: T46ExecLive
item: live re-fetch of the three C3 documents (S258 arXiv 2504.16777, S259 TUM portal record, S260 Google Testing Blog per-post feed) compared byte-wise and normalized-text-wise with the committed snapshots, plus every `recheck:` command of the three C3 entries run exactly as written

Wave 2, falsify. Attacked: the C3 snapshot pins and the `recheck:` lines of `corpus/knowledge/{r6-flaky-failures-cluster,r5-undetected-flaky-failures,r9-false-red-rate}.md` at CONTENT rev `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`. Read first: `.ufo/evidence/round-46/contract.json` (never edited), `.ufo/waves/round-46/w1/ScribeRows.md` (the snapshot-identity receipt at its lines 104-114). Scratch: `/tmp/tameshi-r46-T46ExecLive/`. Lane checkout untouched except this report; no git/jj command run in the lane.

## 1. Live fetch vs committed snapshot

Fetch command, per URL, exactly as the item specifies:

```
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o <scratch>/<f> <url>
```

| doc | URL | curl exit | live bytes | live sha256 | snapshot sha256 | byte-equal? |
|---|---|---|---|---|---|---|
| S258 | https://arxiv.org/abs/2504.16777 | 0 | 43376 | `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14` | `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14` | **YES** (`cmp` exit 0) |
| S259 | https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/ | 0 | 51850 | `b88636cce1ee264a61d9d34e4671035fd52c7a96e8c5b9e5ada7551a8a6ef125` | `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f` | **NO** (`cmp` exit 1, char 51156, line 845) |
| S260 | https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json | 0 | 8353 | `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929` | `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929` | **YES** (`cmp` exit 0) |

All three 8-hex anchor prefixes in `corpus/SOURCES.md:133-135` (`28d2954d`, `5eb59adf`, `434d8658`) match the committed snapshots' digests, so the anchors still pin the files they name.

### S259 byte diff localized

`ndiff = 10` bytes, offsets 51155-51189, all inside the portal's analytics bootstrap:

```
SNAP: ..."loadTime":"201","loadTimestamp":"1792961760971"...
LIVE: ..."loadTime":"199","loadTimestamp":"1792966872860"...
```

No bibliographic, abstract, keyword, DOI, RIS or BibTeX byte differs. This is the volatile-page behavior the r5 entry itself states.

### Normalized text

`python3 .ufo/evidence/round-45/freshness/measure.py --extract <file>` (exit 0 on both):

| file | bytes of extraction | sha256 of extraction | words |
|---|---|---|---|
| snapshot `tum-portal-flaky-failures.html` | 12011 | `1d18a333e45ec90643fee529904f41e0f090d68b6f8d1b8ddc6a660b8d2b8063` | 1668 |
| live `tum-portal-flaky-failures.html` | 12011 | `1d18a333e45ec90643fee529904f41e0f090d68b6f8d1b8ddc6a660b8d2b8063` | 1668 |

`diff tum-snap.txt tum-live.txt` → exit 0, 0 diff lines. The two normalized texts are identical, and 1668 words is the figure the r5 entry states ("1668 words each"). So the S259 byte drift is analytics-only: **no content drift**.

## 2. Quoted-span presence in LIVE text

Method: every `"..."` span of the entry markdown, token count over the counter's own `fold()` (`measure.py:100-106`: NFKC, curly quotes/dashes folded, whitespace collapsed), kept when 6 <= tokens <= 25, then substring-tested against the LIVE extraction of the same URL.

| entry | quoted spans | in 6-25 token band | present in LIVE | absent |
|---|---|---|---|---|
| r6-flaky-failures-cluster (S258) | 15 | 15 | **15** | 0 |
| r5-undetected-flaky-failures (S259) | 25 | 18 | **13 source quotes** | 5 non-source |
| r9-false-red-rate (S260) | 21 | 20 | **20** | 0 |

The 5 absent r5 spans are not source quotations; each was located in the lane file it actually quotes:

- `A standalone exact-tuple repeated-control gate; a clean result is finite sample agreement, not proof of determinism or a flaky-test cure` (20 tok) → `corpus/README.md:127`
- `N ≥ 3 byte-identical controls, or a named mismatch` (9 tok) → `corpus/README.md:80`
- `is not a determinism proof and it cures no flakiness` (10 tok) → `tools/repeat-control.py:94`
- `N ≥ 3 controls that agree while the environment tuple varies` (11 tok) → the entry's own labelled `Inference:` phrasing
- `open access per the institutional record` (6 tok) → `.ufo/evidence/round-46/assimilation/package/r5-undetected-flaky-failures.md` (the package overstatement the entry corrects)

The 13 present source spans include all 10 numbered "Located quotes" and 3 further quoted sentences, each at its stated occurrence count in the LIVE text:

| # | quote (head) | tokens | LIVE count | stated count | match |
|---|---|---|---|---|---|
| 1 | Flaky tests produce non-deterministic outcomes… | 19 | 4 | 4 | OK |
| 2 | Modern CI systems commonly rerun failed tests within the same job… | 15 | 4 | 4 | OK |
| 3 | Existing research predominantly analyzes data from this detection mechanism… | 19 | 4 | 4 | OK |
| 4 | All apparently deterministic failures were systematically validated… | 18 | 3 | 3 | OK |
| 5 | We found that, across all projects, undetected flaky failures account for 9.8 %–16.3 %… | 18 | 3 | 3 | OK |
| 6 | These flaky failure rates spike temporarily… | 14 | 4 | 4 | OK |
| 7 | While failures concentrate heavily in small test case subsets | 9 | 4 | 4 | OK |
| 8 | the most disruptive test cases with undetected flaky failures… | 19 | 4 | 4 | OK |
| 9 | Additionally, test environments significantly influence flakiness, with up to 3× variation… | 16 | 3 | 3 | OK |
| 10 | Our publicly available dataset of 154,000 flaky test cases… | 18 | 4 | 4 | OK |
| + | for developing improved strategies for industrial CI environments | 8 | 4 | — | OK |
| + | under conditions that developers intend to maintain constant | 8 | 4 | — | OK |
| + | We analyzed 8.8 billion test executions from four industry-scale projects… | 13 | 4 | — | OK |

The en-dash detail the entry names reproduces: `9.8 %–16.3 %` folds to `9.8 %-16.3 %` and matches 3 visible copies; the BibTeX `{\textendash}` spelling matches 0 in both texts.

## 3. `recheck:` commands run exactly as written

Run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (the r5 recheck uses the lane-relative `measure.py` path and writes `/tmp/tum-r46.html`, outside the lane).

| entry | stated output | observed output | verdict |
|---|---|---|---|
| r6 (S258) | `grep -c 'co-occurring failures that share the same root causes'` → `3`; 43,376 bytes; sha256 `28d2954d…`; `cmp`-identical | `3`; live fetch 43,376 bytes; `28d2954d22ea…a26a14`; `cmp` identical | **reproduces** |
| r5 (S259) | count `4`; two digests `b3051e44…`, `b0619632…`; normalized text 1668 words | count `4`; digest `f62a934611c98d2128d66a573cfcc333f432835c2c360eba669d184b4e6e4c93`; normalized text 1668 words, equal to snapshot word for word | **count reproduces**; digest is a third distinct value |
| r9 (S260) a | sha256 `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  -` | identical | **reproduces byte-exactly** |
| r9 (S260) b | `grep -c '84% of the transitions we observe from pass to fail'` → `1` | `1` | **reproduces** |
| r9 (S260) c | `grep -c 'Almost 16% of our tests have some level of flakiness'` → `1` | `1` | **reproduces** |

`curl` exit 0 on every recheck invocation (`PIPESTATUS[0]=0` checked for the r6 pipe).

## Findings

- **INFO — S258 snapshot pin is live and exact.** `https://arxiv.org/abs/2504.16777` returned 43,376 bytes, sha256 `28d2954d…a26a14`, `cmp`-identical to `coverage/sources/arxiv-2504.16777-abs.html`; all 15 of the entry's 6-25-token quoted spans are present in the LIVE extraction; the recheck count is `3` as stated. No drift.
- **INFO — S260 snapshot pin is live and exact.** The per-post feed returned 8,353 bytes, sha256 `434d8658…8889929`, `cmp`-identical to `coverage/sources/google-flaky-feed-6277555988217606236.json`; all 20 quoted spans present; all three recheck outputs identical to the stated ones, digest included.
- **INFO — S259 differs byte-wise but not in content; the entry already declares this.** The live page differs from the committed snapshot in 10 bytes confined to `"loadTime":"201"→"199"` and `"loadTimestamp":"1792961760971"→"1792966872860"` in the portal analytics block; the `measure.py --extract` normalizations are byte-identical (sha256 `1d18a333…b8063`, 12011 bytes, 1668 words both) and `diff` is empty; all 10 numbered located quotes and 3 further source spans are present at their stated occurrence counts. `corpus/SOURCES.md:134`'s `sha256 5eb59adf` anchor therefore still pins the committed bytes while the page's live bytes are volatile — the anchor is a snapshot pin, not a live-URL pin, and the entry says so.
- **INFO — the r5 recheck digest is now a third distinct value (`f62a9346…`) beyond the two the entry names (`b3051e44…`, `b0619632…`).** This is not a defect against the entry: its line 3 states the page serves volatile bytes and that "the drift signal is the count falling to 0, not a digest mismatch", and the count is still `4` with normalized text unchanged at 1668 words. Recorded because a later reader comparing digests will see a value the entry does not list. No content-bearing quote, number or bibliographic field changed.
- No BLOCKING, HIGH or LOW defect found. Nothing in the C3 snapshot set or the three `recheck:` lines failed to reproduce.

## Not done / limits

- No counter was run as a verdict (bounds: the L1 owns deciding runs); no `measure.py --selftest` was run, as the item does not name it.
- The arXiv paper body (PDF/HTML) was not fetched, matching the entry's own stated boundary; only the abstract page was compared.
- Fetch was a single sample per URL (one curl each, plus the recheck invocations), so the "volatile" characterization of the TUM page rests on the observed timestamp difference plus the two earlier digests the entry records.
- No tools installed or upgraded; no pacman transaction attempted (host-wide pause respected). Only `curl`, `sha256sum`, `cmp`, `diff`, `grep`, `wc`, `stat` and `python3` were used.

## Risk

- None to the lane: no lane file other than this report was written, no git/jj state was touched, and all scratch output is under `/tmp/tameshi-r46-T46ExecLive/`.
