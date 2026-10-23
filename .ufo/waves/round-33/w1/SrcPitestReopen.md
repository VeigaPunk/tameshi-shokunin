# Source recheck S099 — pitest.org

## Verdict

Unchanged. The live page digest equals the round-32 Gate digest. Do not add a supersedes row.

## Evidence

Frozen pin, full digest `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc`, 12,023 bytes, fetched 2026-10-23 UTC:

- Round-32 Gate: `.ufo/waves/round-32/w1/SrcMutationAdequacy.md:13` and the quote at `:23`.
- Lesson record: `corpus/lessons/round-32.md:27-29`.
- Current row: `corpus/SOURCES.md:107` (opened 2026-10-23, recheck cadence `180d`). The prefix `b0c7e050` and the suffix `10cc` are that same digest.

This recheck is the same UTC date as that pin. It is the opening this round asked for, not a later 180-day visit.

Seat directory: `/fast/scratch/hyaku/tameshi-r33-seats/SrcPitestReopen/`. An earlier copy of the same bytes was fetched in a misnamed directory and moved here; the command below was run in the seat directory and is the cited fetch. No tool was installed.

```sh
curl --location --max-time 45 --max-filesize 2097152 --silent --show-error \
  --dump-header headers-from-seat.txt --output pitest-homepage-seat.html \
  --write-out 'http_code=%{http_code}\nsize_download=%{size_download}\nurl_effective=%{url_effective}\nnum_redirects=%{num_redirects}\ncontent_type=%{content_type}\n' \
  https://pitest.org/ > curl-seat-writeout.txt; echo $? > curl-seat.exit
sha256sum pitest-homepage-seat.html > pitest-seat.sha256; echo $? > sha-seat.exit
cmp pitest-homepage.html pitest-homepage-seat.html > cmp-seat.out; echo $? > cmp-seat.exit
wc -c < pitest-homepage-seat.html > seat-bytes.txt; echo $? > seat-bytes.exit
```

Observed:

- `curl-seat.exit:1` is `0`. `curl-seat-writeout.txt:1-5`: `http_code=200`, `size_download=12023`, `url_effective=https://pitest.org/`, `num_redirects=0`, `content_type=text/html; charset=utf-8`.
- `headers-from-seat.txt:1` is `HTTP/2 200`. `:4` last-modified `Wed, 03 Jun 2026 08:45:38 GMT`. `:6` etag `"6a1fe9b2-2ef7"`. `:14` date `Fri, 23 Oct 2026 18:49:42 GMT`. `:22` `content-length: 12023`.
- `seat-bytes.txt` is `12023` (exit `seat-bytes.exit:1` = `0`).
- `pitest-seat.sha256` is `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc  pitest-homepage-seat.html` (exit `sha-seat.exit:1` = `0`).
- `cmp-seat.exit:1` is `0` and `cmp-seat.out` is empty, so this body is byte for byte the same as the earlier `pitest-homepage.html`, whose `pitest.sha256:1` is the same digest.

Digest equal, byte count equal, status 200. That is the unchanged verdict.

### Quote for this opening

The round-32 sentence is still present and was not reused. `pitest-homepage-seat.html:114` (also `quote-lines.txt:1`):

"The quality of your tests can be gauged from the percentage of mutations killed."

Different quote, 19 words, from the "What?" section (heading at HTML line 116). The sentence starts on line 121 and ends on line 122 (`quote-lines.txt:2-3`; `quote-counts.txt:3` and `:7`):

"If a unit test does not fail in this situation, it may indicate an issue with the test suite."

The preceding words on line 121 say the modified application code should make the unit tests fail, so this sentence is the page's claim that a test which does not fail on that change may show a problem in the suite.

The nearby gold-standard sentence (`quote-lines.txt:4-5`, HTML lines 137-138) is about the same subject, but the full sentence is 28 words (`quote-counts.txt:6`), over the 25-word Gate limit, so it is not the quote.

## Smallest safe correction

No production change. `corpus/SOURCES.md:107` already names this URL, 12,023 bytes, and this digest, and line 114 still matches the round-32 quote. A supersedes row is the correction only when the digest differs. It does not.

For the round-33 lesson Gate, record the recheck as unchanged, with URL `https://pitest.org/`, access date 2026-10-23 UTC, the 19-word quote above, and location HTML lines 121-122. Leave the S099 row as it is.

## Bounds

No production file was edited. No git write and no jj command was run. Nothing was installed. Curl finished; no process was left running. This report makes no claim that the page's account is true, and it states no score.
