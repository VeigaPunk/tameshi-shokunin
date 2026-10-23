# SrcRecheckS101 — freshness

Verdict: no finding. https://mutation-testing.org/ is still the same document the S101 row pins. HTTP 200, 0 redirects, effective URL unchanged, 4,341 bytes, sha256 `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`. That digest is the committed snapshot at tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` and the digest in `corpus/SOURCES.md` row S101 and in `corpus/lessons/round-34.md` Gate. `cmp` of the live body against the committed blob exits 0. Not a moved page. Not a 404 or timeout.

The Gate quote is on the page as three consecutive Overview list items (live HTML lines 44–46, same bytes in the snapshot). It is not one contiguous substring: tags sit between the items, and line 46 continues past the quoted stop.

## Pins (before the fetch)

Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/`. No tools installed. Lane checkout is the scratch clone only.

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101 && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane; echo "clone:$?" > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/clone.exit && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; echo "checkout:$?" > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/checkout.exit && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane rev-parse HEAD > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/head.txt; echo "revparse:$?" >> /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/checkout.exit && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/tool.py; echo "toolshow:$?" > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/show.exit && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/pristine.sh; echo "runnershow:$?" >> /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/show.exit && sha256sum /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/tool.py /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/pristine.sh > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/pins.sha256
```

Exits: `clone:0`, `checkout:0`, `revparse:0`, `toolshow:0`, `runnershow:0`. `head.txt` is `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

- `tool.py`: `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` (matches the byte pin)
- `pristine.sh`: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches the byte pin)

The tool and the runner were not executed.

## Live fetch

Access: `Date: Fri, 23 Oct 2026 19:41:22 GMT`. One ordinary curl, no browser.

```
curl -sS -L --max-redirs 5 -D /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.headers -o /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.html -w "http_code:%{http_code}\nsize_download:%{size_download}\nurl_effective:%{url_effective}\nnum_redirects:%{num_redirects}\nredirect_url:%{redirect_url}\ncontent_type:%{content_type}\nexit:%{exitcode}\n" --max-time 30 "https://mutation-testing.org/" > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.curlmeta; echo "curl:$?" > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.exit && sha256sum /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.html > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.sha256 && wc -c /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.html > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/live.bytes
```

`live.exit`: `curl:0`. `live.curlmeta`: `http_code:200`, `size_download:4341`, `url_effective:https://mutation-testing.org/`, `num_redirects:0`, `redirect_url:` empty, `content_type:text/html; charset=UTF-8`, `exit:0`. `wc -c`: `4341`. sha256: `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`.

First response line (`live.headers`): `HTTP/1.1 200 OK`. Also `Content-Length: 4341`, `Last-Modified: Fri, 27 Sep 2024 02:42:43 GMT`, `ETag: "10f5-62310cf3dcfc3"`. No 3xx status in the header file.

## Committed snapshot and row digest

Working-tree copy of the checkout (detached at the tip):

```
cp -a /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane/.ufo/evidence/round-34/src/s101-mutation-testing.html /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/committed-snapshot.html && sha256sum /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/committed-snapshot.html > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/snapshot.sha256 && wc -c /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/committed-snapshot.html > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/snapshot.bytes
```

sha256 `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`, `4341` bytes.

Blob at the tip (not the worktree file):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:.ufo/evidence/round-34/src/s101-mutation-testing.html | sha256sum > /fast/scratch/hyaku/tameshi-r34-seats/SrcRecheckS101/blob.sha256
```

`blob.exit`: `blobpipe:0`. Same digest `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420`.

```
cmp -s live.html committed-snapshot.html; echo $?   # cmp.exit: cmp_live_snapshot:0
cmp -s live.html <(git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:.ufo/evidence/round-34/src/s101-mutation-testing.html); echo $?   # cmp.exit: cmp_live_blob:0
```

Row digest (`corpus/SOURCES.md` line 109, anchor cell) and Gate digest (`corpus/lessons/round-34.md` lines 18–20) are the same 64 hex digits. Both name 4,341 bytes and `.ufo/evidence/round-34/src/s101-mutation-testing.html`.

## Quote location

Gate quote (`corpus/lessons/round-34.md` lines 20–22), the quote the S101 row's anchor calls the Overview feature list:

`exporting source-code mutants; suppressing equivalent mutants; computing the mutant-detection rate and the set of live mutants`

Located in the live body (identical offsets in the snapshot; `quote-detail.txt`):

| fragment | byte offset | HTML line |
|---|---|---|
| `exporting source-code mutants;` | 1760 | 44: `<li><p>exporting source-code mutants;</p></li>` |
| `suppressing equivalent mutants;` | 1811 | 45: `<li><p>suppressing equivalent mutants;</p></li>` |
| `computing the mutant-detection rate and the set of live mutants` | 1863 | 46, which continues ` for a given set of tests;` |

`str.find` of the joined quote is `-1` in both live and snapshot (tags between the `<li>`s). The row's `teaches` paraphrase ("frameworks treat equivalent mutants as first-class") is also absent (`find` = -1); the page text is the three list items, not that sentence.

Note, not a freshness failure: the Gate labels that quote "15 words". `len(quote.split())` is 16 (`quote-detail.txt`, `detail.exit` = `detail:0`). The clauses themselves are verbatim.

## What was not claimed

No symbol contract was in question, so LSP was not used; location is a byte search of the fetched HTML. The kill-rule counter was not run. C1's deciding-run receipt was not re-executed.
