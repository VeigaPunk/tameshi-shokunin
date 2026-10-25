# Scout: Stryker equivalent-mutants snapshot verify (round 44, wave w1)

Access date: **2026-10-25** (live fetch performed this date).

Milestone: Stryker snapshot verify. Item: committed snapshot vs live page — size, sha256, `<title>`, byte-identity, lines 15–17, `10 ** 0` example, two ≤25-word quotes with HTML line numbers.

## 1. Committed snapshot

- Path: `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`
  (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`)
- Size: **38687 bytes**
- sha256: **79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce** (matches contract C2 `79f6501a...`)
- `<title>` (HTML line 1): `<title data-rh=true>Equivalent mutants | Stryker Mutator</title>`; `og:title` = "Equivalent mutants | Stryker Mutator"
- 24 HTML lines (1–24); `wc -l` reports 23 because line 24 ends with `>` (0x3e), no trailing newline

## 2. Live page

- URL: `https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/`
- Fetch: `curl -fsSL -o /tmp/tameshi-r44-ScoutStrykerSnapshot-/stryker-equivalent-mutants-live.html ...` (exit 0)
- Size: **38687 bytes**
- sha256: **79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce**
- `<title>`: identical `<title data-rh=true>Equivalent mutants | Stryker Mutator</title>` (line 1)

## 3. Byte-identity

`cmp -s <snapshot> <live>` → exit `0`. Identical sha256 (79f6501a...) and identical size (38687 bytes) corroborate.

## 4. Lines 15–17 verbatim (HTML line numbers, snapshot == live)

- Line 15: `<p>Notice that 10 ** 0 = 1, so even if we change <code>>=</code> to <code>&lt;=</code> and even <code>&lt;</code> or <code>></code> we will get the same output each time!</p>`
- Line 16: `<p>It is called <em>equivalent mutant</em>. There is no definitive way for Stryker to find and ignore them. There is currently also no way yet to mark them to be ignored.</p>`
- Line 17: `<p>For now, the only solution is by finding these by hand, which is time consuming and try to rewrite the code so it won't occur, or accept that you won't make 100%.</p>`

## 5. `10 ** 0` example

HTML line **15** (first occurrence, only occurrence): `10 ** 0 = 1` in the "Notice that ..." paragraph.

## 6. Two ≤25-word quotes (HTML line numbers)

Quote 1 — line **16** (12 words): "There is no definitive way for Stryker to find and ignore them."
Quote 2 — line **16** (13 words): "There is currently also no way yet to mark them to be ignored."

Both are full sentences of line 16's text (tags stripped), each ≤25 words (`wc -w` = 12 and 13).

## 7. Versus S089 anchor (2026-10-22)

`corpus/SOURCES.md:98` (S089 row) names the stale anchor: `html sha256 bc572676…e04d`, `page fetched 2026-10-22 (version unstated; ...)`. That digest **differs** from the new `79f6501a...` (live snapshot of 2026-10-25), which supersedes it per C2.

Note: `corpus/SOURCES.md` currently contains no `| S160 ` row (grep found none) — consistent with the base state; C2's counting command expects `1` at the landing commit.

## 8. Tools

No tool installed or updated (pacman paused host-wide; used system `curl`). Scratch evidence kept at `/tmp/tameshi-r44-ScoutStrykerSnapshot-/stryker-equivalent-mutants-live.html`.
