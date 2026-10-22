# ReopenS059 — re-open of https://bazel.build/remote/caching

Verdict: **agree** — the quote is verbatim and located as the Gate states, the
known-issues line still appears, and the lesson's use is within what the page
says. Two small blemishes noted below (word count off by one; recorded
markdown-alternate sha256 stale), neither affects the row's scope.

## What was checked

Row S059 at `b05d2ee8` (`git show b05d2ee8:corpus/SOURCES.md`, line 68):
tier A, docs source, notes "§Known issues, 'Bazel does not track tools outside
a workspace' @ page fetched 2026-10-20, version unstated, markdown alternate
sha256 0d362d11…", lesson claim "a cache hit is reuse keyed to the recorded
inputs; an input outside the key keeps the same hash while the outcome
changes…".

Gate of `b05d2ee8:corpus/lessons/round-28.md` claims: fetched 2026-10-22 with
`curl -sL`, HTML sha256 `9e3a2ebb…`, quote "The action cache, which is a map
of action hashes to action result metadata." located under "The remote cache
stores two types of data:", and §Known issues still reading "Bazel currently
does not track tools outside a workspace".

## Evidence

Fetch (ordinary means, no challenge):

```
curl -sSL --max-time 60 -A "Mozilla/5.0…" https://bazel.build/remote/caching
→ 297255 bytes, exit 0
sha256: 9e3a2ebba08234a1b5896faaea54be7c4aea2adb3e1051037f477d8f24d42348
```

The HTML sha256 **matches** the Gate's claimed hash exactly.

Rendered-text extraction of the fetch (traces receipt:
`.ufo/evidence/round-28/coldread/traces/ReopenS059-1.json`):

- Line 140: `The action cache, which is a map of action hashes to action
  result metadata.` — verbatim, and it sits directly under the sentence "The
  remote cache stores two types of data:" in the Overview section, exactly
  the location the Gate gives. Word count is **14**, not the Gate's "(13
  words)" — trivial, does not affect verbatimity.
- §Known issues (line 459 heading; lines 486–487): bold item "Bazel does not
  track tools outside a workspace" with body "Bazel currently does not track
  tools outside a workspace. This can be a problem if, for example, an action
  uses a compiler from /usr/bin/. Then, two users with different compilers
  installed will wrongly share cache hits because the outputs are different
  but they have the same action hash. See issue #4558…" — the sentence the
  Gate quotes is present verbatim and still under Known issues.
- Markdown alternate `https://bazel.build/remote/caching.md` fetched
  2026-10-22: sha256 `266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b
  16d67768a5b`, which **differs** from the row's recorded `0d362d11…`.
  Source content has drifted in some non-quoted part since 2026-10-20; both
  quotes are still present in it (lines 34, 343–345). The row's scope note is
  stale on the pin but not on substance.

## Tier-A call and lesson use

The page is Bazel's official documentation of its own caching behavior —
the strongest available source class for this claim, so tier A stands. The
lesson claim reads as a restatement of the §Known issues mechanism: the
action hash keys reuse, tools outside the workspace are outside the key
(page: "Bazel currently does not track tools outside a workspace"), so an
input outside the key can change while the hash stays, producing a false
hit ("outputs are different but they have the same action hash"). The
round-28 lesson's use — "the same digest-keyed miss S059 describes" applied
to the lane monitor keying credit to input sha256s — is an analogy to that
mechanism and stays within it; the page does not literally use the word
"miss" (it describes a false *hit*), but the shared mechanism (outcome
decoupled from key) is what the lesson invokes, and it does not overstate.

## Residual nits (not blocking)

1. Gate says "(13 words)"; the quote is 14 words.
2. Row's recorded markdown-alternate sha256 `0d362d11…` no longer matches
   live `266915c5…`; the pinned-by-hash note will mislead a future byte-diff
   even though both quoted passages survive unchanged.
