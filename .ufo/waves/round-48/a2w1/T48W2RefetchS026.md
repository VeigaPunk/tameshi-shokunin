# T48W2RefetchS026 — independent re-open of S026 (C2, freshness, a2w1)

Seat: T48W2RefetchS026. Target: S026, re-opened at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`
in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Sole L1: TameshiR48a2. I am not an author of
anything attacked here (attempt-1 wave-1 seats fetched the snapshot; this report re-derives every
check from the live URL and the committed bytes at REV).

**Verdict for my item: S026 re-opens clean. No claim that rests on S026 fails against the live text,
and every C2 structural condition for S026 holds at REV. Four informational observations (none a C2
miss) are listed under Findings.**

Receipts for everything below are in this directory:
`live-fetch.receipt.txt`, `quote-and-claims.check.txt`, `recheck-command.check.txt`,
`structure.check.txt`, `byte-diff.receipt.txt`, `counter-probes.txt`.

---

## 1. Live fetch (my own, not the lane's)

```
curl -sS -L -o S026.live.html -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}' \
  https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
```
- url fetched: the receipt's url (also S265's source-cell url) — `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`
- HTTP `200`, **236387 bytes**, sha256 **`dfea6b9ba73478621e4d7c9e748b698155f7377d23547047f17c0b95a101c780`**
- committed snapshot `.ufo/evidence/round-48/freshness/sources/S026.html`: sha256
  **`a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25`**, **236387 bytes**
- receipt `.ufo/evidence/round-48/freshness/sources/S026.receipt.json`: url above,
  `fetched_at 2026-10-26T08:40:51Z`, `http_status 200`, `bytes 236387`, sha256 = the snapshot's. Agrees.

The live sha differs from the snapshot sha at identical length. That is the rotating Blogger chrome,
not content: 97 differing bytes in 4 tokens (dyncss `zx=` UUID, `widgets.js` id, `__wavt` token,
`lbx.js` id), none inside `div[itemprop='articleBody']`; the amendment-2 extracted text is
**byte-identical** across round-45 snapshot, round-48 snapshot and today's live fetch
(26248 chars, sha256 `171d74b0ed416fa601c7ec5c738a4c72ebc27ce7fddd1039402a771a75fea3a1`). See
`byte-diff.receipt.txt`.

## 2. Extraction and quote checks (contract amendment 2, verbatim)

Extraction implemented as amendment 2 states: UTF-8 decode, drop `<script>`/`<style>` element
contents, strip tags, `html.unescape`, collapse every whitespace run to one space; quote
whitespace-collapsed, substring match, no case or punctuation folding. Word count = whitespace
tokens (`quote-and-claims.check.txt`).

Gate line, `corpus/lessons/round-48.md:21` at REV:
`- C2-QUOTE S265 S026: \`about 84% of the transitions we observe from pass to fail involve a flaky test\``

| check | result |
|---|---|
| line matches amendment-2 regex, R then T | yes — R=S265, T=S026 |
| quote ≤25 words | **15** |
| carries required phrase (`required_phrases.S026 = ("84%",)`) | yes, `84%` present |
| located in committed snapshot's extracted text | **yes**, count 1, index 2137 |
| located in live extracted text | **yes**, count 1, index 2137 |
| byte-exact after whitespace collapse (no folding) | yes — exact substring both sides |
| not boilerplate/navigation | yes — article prose inside `div[itemprop='articleBody']` (raw line 1132, visible `<noscript>` copy; same sentence in the `text/template` copy at raw 1097) |

**Does the quote state the row's teaches claim?** The teaches cell (`corpus/SOURCES.md:140`, cell 6)
is a three-clause conjunction; the quote grounds clause 2 exactly, and the other two clauses are
present in the same live article body:

| teaches clause | live text (`S026.live.html`, extracted) | raw line |
|---|---|---|
| "about 1.5% of test runs are flaky" | "a continual rate of about 1.5% of all test runs reporting a \"flaky\" result" (count 1) | 1130 |
| "about 84% of pass-to-fail transitions involve a flaky test" | the Gate quote (count 1) | 1132 |
| "a fail-3-in-a-row flaky mark cuts false positives but teaches people to ignore flakiness" | "This reduces false positives, but encourages developers to ignore flakiness in their own tests unless their tests start failing 3 times in a row, which is hardly a perfect solution" (count 1) | 1136 |

The lesson itself scopes the quote to the 84% clause (`corpus/lessons/round-48.md:32-33`), so the
quote is not presented as grounding all three. No mismatch.

## 3. C2 structural conditions for S026 (re-derived, not read off the counter)

All reads are `git -C tameshi-shokunin show c7586b9:<path>` (`structure.check.txt`):

- exactly one row whose teaches cell opens `supersedes S026 —` (U+2014 verified): **S265**, id above
  S264, status `mined`, opened `2026-10-26`, `corpus/SOURCES.md:140`.
- source cell of S265 carries S026's base URL (amendment 1 URL set) — yes; anchor cell has no other
  https URL, so the receipt url (same blog url) is in the set.
- snapshot set for S026 at REV is exactly `S026.html` + `S026.receipt.json`; snapshot sha256 starts
  `a4c5c46b4af9`, which is what S265's anchor cell states, with 236387 bytes.
- receipt: url in R's URL set, `fetched_at` on 2026-10-26, `http_status 200`, sha = snapshot's. All agree.
- Gate line: present, names R then T, 15 words, located in snapshot and live, phrase `84%`.
- used-by: base S026 used-by = `corpus/knowledge/repeated-control-precondition.md`; S265 used-by is
  exactly that single path; the entry's `source:` line (first 10 lines) names S265
  (`corpus/knowledge/repeated-control-precondition.md:1`) and `verified-at: 2026-10-26` (`:2`).
- base row `corpus/SOURCES.md:37` is byte-identical at REV (lesson claim `round-48.md:104` "S026 keeps
  its status, recheck and used-by cells" holds).

## 4. Knowledge-entry claims resting on S026, against the live text

Entry `corpus/knowledge/repeated-control-precondition.md` (base used-by of S026; re-pointed in
`c7586b9` by a 2-line diff: `:1` source line S026→S265 with the 2026-10-26 sha, `:2` verified-at).

| claim (entry line) | live text | holds |
|---|---|---|
| `:1` post body, John Micco, published 2016-05-27, 236,387 B, sha `a4c5c46b4af9…` | `by John Micco` (raw 1089/1124); `publishdate` "Friday, May 27, 2016" (raw 1082); size/sha as receipt | yes |
| `:3` recheck command `grep -c 'hardly a perfect solution'` on the live URL → 2, body served twice (text/template + noscript) | `grep -c` on today's live fetch = **2** (raw 1101, 1136); copies are `text/template` script raw 1088-1122 (copy 1095-1102) and `<noscript>` raw 1123-1157 (copy 1130-1137); the two 3676-byte blocks are byte-identical | yes |
| `:16` body at `S026.html:1130-1137`, template copy at `:1095-1102` | both ranges resolve and hold the quoted lines | yes |
| `:18` definition quote | count 1 | yes |
| `:19` rate + "Almost 16% of our tests…" | count 1 each | yes |
| `:20` transitions quote + "wait for additional CI cycles to run this test again" | count 1 each ("build monitors typically wait…") | yes |
| `:21` retry family quote + fail-3-in-a-row verdict | count 1 (`report[s]` — see F3) | yes |
| `:22` 45-minute cost | count 1 | yes |
| `:27` retry family reduces false positives, teaches ignoring flakiness, delays detection | supported by `:21`/`:22` text | yes |
| `:29` S026's fail-3-in-a-row is a retry-mitigation rule, not a control-repeat rule | no counter-claim in the source; source describes it as a mitigation | yes (interpretive, unchanged) |

Cross-entry: `corpus/knowledge/r9-false-red-rate.md:16` says the entry "already quotes this sentence
from the rendered page" and is grounded on S260 (the feed). Its claim is still true; see F4 for the
label.

No claim that rests on S026 fails against the live text, and none was re-pointed while stale.

## 5. Counter probes (probes only; never a verdict)

`counter-probes.txt`. `measure.py` sha256 `faefe9b44274…` on disk equals the blob at REV (self_pin 1).

- `measure.py --selftest`: `C2_R48_SELFTEST: cases=43 failed=0`.
- `measure.py --lane <lane> --rev c7586b9… --no-live`: all four targets print
  `row=… snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED`;
  `C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=off rev=c7586b9… C2_R48_PARTIAL=true`, exit 0.
  S026's line independently matches §2-§4 above. I did not run live mode (seat bound).

## 6. Findings (informational, none blocks C2)

- **F1 — the sha256 pin is not reproducible from a fresh fetch.** Today's fetch of the receipt URL is
  236387 B, sha256 `dfea6b9b…`, not the snapshot's `a4c5c46b…`; the 97 differing bytes are four
  rotating Blogger chrome tokens and the extracted article text is identical. The frozen C2 live
  check only asks whether the quote is in the fetched text, so this is not a miss — but any later
  re-open that compares live sha to the receipt sha will see drift. Show:
  `cmp -l S026.snap.html S026.live.html | wc -l` → 97; extraction hashes in
  `live-fetch.receipt.txt`.
- **F2 — the Gate quote grounds one of the teaches cell's three clauses.** Quote = the 84% clause;
  clauses 1 and 3 are in the live body at raw 1130 and 1136 (§2 table). The lesson discloses the
  scope (`round-48.md:32-33`), so this is a disclosure note, not a mismatch: if a later round reads
  the Gate line as grounding the whole teaches cell, it would over-credit it.
- **F3 — entry quote is not byte-exact at one word.** `corpus/knowledge/repeated-control-precondition.md:21`
  writes `report[s] a failure only if it fails 3 times in a row`; the source reads "causing it to
  **report** a failure only if it fails 3 times in a row" (live raw 1136). The bracket interpolation
  widens the source word (`report`/`reports`); the claim holds, but the quote is editorial, not
  verbatim. Show: `grep -o 'causing it to report a failure only if it fails 3 times in a row' S026.live.html`.
- **F4 — stale label in a neighbouring entry.** `corpus/knowledge/r9-false-red-rate.md:16` still calls
  `repeated-control-precondition.md` "the lane's **S026-ground** entry"; after the re-point it is
  S265-ground (S265 supersedes S026). Same entry cites S026 but is not in S026's used-by cell, so the
  C2 used-by check never inspects it; its substantive claim (the rendered page carries the same
  sentence) is true today. Wording-only.
- **F5 — the size change recorded by the re-anchor is chrome-only.** Base row `corpus/SOURCES.md:37`
  cited 236,385 B / `ca1145fb…` (2026-10-20); S265 records 236,387 B / `a4c5c46b…`. The +2 bytes and
  the sha change are confined to rotating tokens: the round-45 committed snapshot's extracted text
  is identical (`171d74b0…`). A reader comparing only size/sha could read this as content drift; it
  is not.

## 7. Bounds, tooling, scratch

- Read-only on the lane: every lane read used `git show <rev>:<path>` or plain reads; no git/jj
  mutating command, no writes outside `.ufo/waves/round-48/a2w1/`.
- No tool installed or upgraded. No network fetch other than the one receipt URL.
- Scratch: `/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS026` (all curl/extract/diff work), removed
  before yielding; disk guard checked before the pass (`/fast` 622G free).
- Blocker: none. The deciding live-mode invocation remains the L1's, not mine.
