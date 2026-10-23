# ScoutCorpusRows — S102 row vs committed snapshot

Axes: content hash, byte count, section anchor, quote word count (adjacency: used-by path and rule-1 gate quote).

Pin: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (scratch checkout `/fast/scratch/hyaku/tameshi-r35-seats/ScoutCorpusRows/lane`, clean). Worktree HEAD of the lane repo at read time was descendant `1fc6cb7f764e150b038e132590b7f23250254fe7`; `corpus/SOURCES.md` was byte-identical to the pin (`sha256 f85c02e76b0994477df7ded8d95585d260885f2d93fbeb91e57deb358d7855fe`, git blob `d030edb3f334f9c52125817e647c378a8f9f119d`). No install. No frozen artifact edited.

Attacked: the S102 registry row at `corpus/SOURCES.md:110` (introduced in `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`) against committed snapshot `.ufo/evidence/round-35/src/s102-posix-chap02.html` (git blob `d9cf6d822b5c1bf1233e23d9fbe4d5504027ba4c`).

## Could not break

The row's hash, size, and §2.3 anchor match the snapshot. The `#` sentence inside that section is 25 whitespace words.

Command (cwd = scratch lane; exit 0):

```
sha256sum .ufo/evidence/round-35/src/s102-posix-chap02.html
wc -c .ufo/evidence/round-35/src/s102-posix-chap02.html
```

```
0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd  .ufo/evidence/round-35/src/s102-posix-chap02.html
357953 .ufo/evidence/round-35/src/s102-posix-chap02.html
```

`sha_exit:0`, `wc_exit:0`. `git cat-file -s HEAD:.ufo/evidence/round-35/src/s102-posix-chap02.html` is also `357953`. The row's anchor cell writes the same digest and `357,953` (thousands separator only). The digest is the file's SHA-256, not the git blob id `d9cf6d82…`.

Section anchor. Raw heading at file offset 15187 (`s102-posix-chap02.html:237`):

```
<h3><a name="tag_19_03" id="tag_19_03"></a>2.3 Token Recognition</h3>
```

The page identity line is `IEEE Std 1003.1-2024` / `POSIX.1-2024` (`:26`, `:35`). The document ends `</html>\n` (5918 lines, 0 CR). The URL digit string `9799919799` is not inside the saved HTML; the row's canonical URL was not re-fetched.

The `#` sentence the anchor names is list item 10 of 10 in that section (span 15187–21526, before `2.3.1 Alias Substitution`), file offset 20769, lines 303–304:

```
<p>If the current character is a <tt>'#'</tt>, it and all subsequent characters up to, but excluding, the next &lt;newline&gt;
shall be discarded as a comment. The &lt;newline&gt; that ends the line is not considered part of the comment.</p>
```

Tag-stripped, whitespace-collapsed first sentence (25 tokens, period kept on the last):

`If` `the` `current` `character` `is` `a` `'#',` `it` `and` `all` `subsequent` `characters` `up` `to,` `but` `excluding,` `the` `next` `<newline>` `shall` `be` `discarded` `as` `a` `comment.`

Item 9, immediately before it, is "If the previous character was part of a word, the current character shall be appended to that word." The row's teaches cell ("a `#` at the point a token begins…") matches that order; it was not shown false.

Row shape at the pin: `awk` `NF=13`, kind `spec`, tier `A`, status `mined`, opened `2026-10-23`, recheck `365d`. Census `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `99` (exit 0). Malformed (`NF!=13`) → `0`. `git grep -c` of `^| S` is 98 at `d16f9b5a^` and 99 at `d16f9b5a`, matching the id-allocation line "Rows 98 → 99". `tools/tally-audit-v3.py:29` (blob at the pin) cites S102. That used-by path exists (`git cat-file -e` exit 0).

## Ranked findings

### CRITICAL

None on the four re-derived row claims. Hash, byte count, §2.3 anchor, and the snapshot sentence's word count are not false.

### BOUND

**B-1. The rule-1 gate quote is not in the commit, so a clean pin cannot re-derive it.** Contract `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` rule 1 requires the round lesson `## Gate` to hold the ≤25-word quote. The row's `used-by` cell is `tools/tally-audit-v3.py, corpus/lessons/round-35.md`. At pin `7da6e076` and at worktree HEAD `1fc6cb7f`:

```
git cat-file -e HEAD:corpus/lessons/round-35.md
```

exit 128, `fatal: path 'corpus/lessons/round-35.md' does not exist in 'HEAD'`. The contract census loop (`[ -e "$p" ] || echo missing`) run in the scratch checkout prints `MISSING corpus/lessons/round-35.md` and `exists tools/tally-audit-v3.py`. `mined` still has one real citer (the tool). The lesson file is only an untracked worktree path (`?? corpus/lessons/round-35.md`, 8484 bytes, sha256 `29c11a3cdd7cab1d73f6c15064e665deb79d3abc0f90e29b1e10a77133bc028f`).

### HYGIENE

**H-1. The untracked gate quote inserts one byte and is 26 whitespace words, not 25.** `corpus/lessons/round-35.md:72-74` says `Located quote (25 words):` and then:

`If the current character is a '#' , it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment.`

Whitespace split of that flattened string is 26 tokens. Token 8 is a lone `,` because of an inserted `0x20`. File offset 5225 (0-based) is the bytes `23 27 20 2c 20 69` (`#' , i`). The snapshot window at the same words is `3c74743e2723273c2f74743e2c206974` = `<tt>'#'</tt>, it`, which renders `'#',` with no space (`0x27` then `0x2c`). Lengths 142 vs 141. Every other character of the first sentence matches. The parenthetical `(25 words)` is false for the quote as written; the snapshot sentence the row actually anchors is the 25-word string above.

## What was not claimed

Live re-fetch of `pubs.opengroup.org` was not done. No C1/C2 counter was run. No package was installed.
