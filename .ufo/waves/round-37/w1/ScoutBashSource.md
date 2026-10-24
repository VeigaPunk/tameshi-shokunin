# ScoutBashSource — S104 §ANSI-C Quoting anchor verification

Scoped question: re-open the pinned Bash 5.3 `doc/bashref.texi` §ANSI-C Quoting at commit `b8c60bc9ca365f8261fa97900b6fa939f6ebc303`; verify the ≤25-word quote and the exact line/section anchor supporting **only** `$'...'` escape behavior.

## Fetch and pin (observed)

```
curl -fsSL --max-time 90 \
  'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303' \
  -o bashref-pinned.texi
wc -c      -> 415804
sha256sum  -> f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5
```

- Bytes + digest match the lane's previously recorded S097 pin (round-32/round-34 re-fetches, same commit): 415,804 B, `f3d37d57…32d5`. Fetched 2026-10-24 UTC; `git.savannah.gnu.org` first returned a bare 301 and one transient 502; the canonical host `cgit.git.savannah.gnu.org` served 200.
- Commit is the Bash-5.3 distribution point: cgit commit page shows it on `bash-5.3-testing`, tagged `bash-5.3`, `bash-5.3-rc2`, `bash-5.3-rc1`, authored 2025-07-03. `version.texi` is `@include`d (not inline); file states Edition @value{EDITION} for @value{VERSION} 5.3 per prior receipt.

## Anchor and quote (observed)

`@node ANSI-C Quoting` / `@subsubsection ANSI-C Quoting` at `doc/bashref.texi:489–490` (`@cindex` lines 491–492). The node body runs lines 493–544 (`@end table` 540, closing sentence 543–544); next node `Locale Translation` starts at line 546.

Exact bytes, lines 494–495:
```
Character sequences of the form @code{$'@var{string}'} are treated as
a special kind of single quotes.
```

Quote as recorded in `corpus/lessons/round-37.md` Gate: "Character sequences of the form `$'string'` are treated as a special kind of single quotes."

```
printf '%s\n' "Character sequences of the form \`\$'string'\` are treated as a special kind of single quotes." | wc -w  -> 15
```

**15 words ≤ 25 — PASS.** The sentence is verbatim modulo Texinfo→plain markup (`@code{…}`, `@var{string}`).

## What the anchor supports (and does not)

- Section scope is exactly `$'string'`: the table at 500–540 lists only backslash escapes (`\a`…`\c@var{x}`), including **`\'` → single quote** at lines 520–521 — the source ground for honoring an escaped `'` inside the quote without closing it. Line 543: "The expanded result is single-quoted, as if the dollar sign had not been present."
- Corroborating sentence at `doc/bashref.texi:11004–11006` (`@node Major Differences From The Bourne Shell`, 10943): "Bash supports the `$'…'` quoting syntax, which expands ANSI-C backslash-escaped characters in the text between the single quotes."
- The section says nothing about `#` comments, nested `$(...)`, or backslash-newline continuation — consistent with the frozen C2 scope "supporting only `$'...'` escape behavior" and the lesson's explicit non-goals.

## Nuance found (report, not repair)

- The quote text physically occupies **lines 494–495**. The committed S104 row and lesson cite `@node ANSI-C Quoting` **"lines 489–493"** and URL fragment `#L489-L493`. That cited window covers the node header/`@cindex` block (489–493); the quoted sentence is the adjacent body lines 494–495 — off by the header lines. The section name and node anchor are exact; the numeric line window describing where the quote sits is 494–495, not 489–493.
- `git.savannah.gnu.org` (host used for S097) currently 301-redirects; `cgit.git.savannah.gnu.org` is the serving host.

## Confidence and remaining unknowns

- High: pin/digest verified first-hand against the lane's recorded values; quote word-count and line numbers verified on the fetched bytes.
- None remaining for this item; the line-window discrepancy above is the only adverse finding, left for the reviewer/scorer seats.

No installs needed. Live lane checkout untouched (report write only).
