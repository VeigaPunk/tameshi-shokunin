# Reopen S072 — Linux man-pages: open(2)

Seat: TameshiR18.ReopenS072 (wave 2, independent re-open). Read rev
`01d586ddbc5fcd78659557c4e93a6ee8517b87d1`. Lane clone at
`/tmp/tameshi-r18w2-ReopenS072-E7YVY2/fleet/tameshi-shokunin` (checked out detached at the
read rev). No peer output was consulted; every claim below was re-derived from the page, the
lane bytes at the read rev, and the kaika contract.

Tooling: nothing installed or upgraded.

## Artifact identities

| artifact | identity |
|---|---|
| `corpus/SOURCES.md` @ read rev | sha256 `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` |
| S072 row (@ `corpus/SOURCES.md:81`) | sha256 `4116bf726811c33c0a8e842db6ffa64448cd9268555282fc25b1be3f08eb2849` |
| `corpus/knowledge/guard-kill-closure.md` @ read rev | sha256 `9312bdebd4e93d427ea32d3db8652f95530237477b49ffecffdf4e4ac49991fb` |
| `.ufo/waves/round-18/staged/lesson-round-18-gate.md` @ read rev | sha256 `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` |
| served `https://man7.org/linux/man-pages/man2/open.2.html` (2026-10-20) | sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`, 76506 bytes |
| same page, tags stripped + whitespace normalised | sha256 `a584d768a64e1eb111496178485b04d4d4e086fcfaa1b61e8c925167b3d3b988` |

Staged vs installed: `.ufo/waves/round-18/staged/corpus/SOURCES.md` and `corpus/SOURCES.md`
are byte-identical at the read rev (both `1d4b5910…`), and the S072 line is byte-identical in
both (`4116bf72…`). The gated artifact is the installed row.

## Checks

| # | check | command (abridged) | exit | result |
|---|---|---|---|---|
| 1 | row parses as 11 cells | `git show REV:corpus/SOURCES.md \| sed -n '81p'` → cell split | 0 | 11 cells; kind `docs`, tier `A`, status `mined`, opened `2026-10-20`, recheck `365d`, used-by `corpus/knowledge/guard-kill-closure.md` |
| 2 | quote word count | `wc -w` on the staged quote | 0 | **17 words** (limit 25) |
| 3 | quote verbatim in page | fetch, strip tags, normalise whitespace, substring test | 0 | `True`; **1 occurrence** |
| 4 | anchor containment | offsets in normalised page text | 0 | quote/entry at 18406, `DESCRIPTION` starts 901, next `RETURN VALUE` 20000 → inside DESCRIPTION |
| 5 | anchor revision | page footer | 0 | `Linux man-pages 6.19 2026-02-08 open(2)` |
| 6 | tier/kind enums | kaika contract §tier/§kind | 0 | `docs` and `A` are both defined enums; A is explicitly "official docs" for the scope |
| 7 | used-by path exists at rev | `git cat-file -e REV:corpus/knowledge/guard-kill-closure.md` | **0** | exists (negative control on a missing path: exit 128) |
| 8 | used-by actually cites S072 | `grep -n "src: S072" corpus/knowledge/guard-kill-closure.md` | 0 | line 118, inside `## 6. Trace-collector guards` (line 116); header line 1 also names S072 |
| 9 | cited quote consistency | `grep -o 'quote "[^"]*"'` on line 118 | 0 | byte-identical to the staged quote |
| 10 | contract census on the registry | malformed-row awk, enum awk, duplicate-id check, missing-used-by loop | 0 | malformed `0`; no enum/tier-inflation output; duplicate ids `0`; missing used-by paths `0` |
| 11 | page reachable on 2026-10-20 | `curl -sS -o /tmp/man_open2.html -w '%{http_code}\n'` | 0 | HTTP **200**, 76506 bytes |

## Findings

### F1 — Quote is verbatim and within the word limit (holds)

The staged quote (`.ufo/waves/round-18/staged/lesson-round-18-gate.md:24`):

> "the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0."

is a contiguous substring of the tag-stripped, whitespace-normalised page text, preceded by
`O_TRUNC If the file already exists and is a regular file and ` and followed by
` If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored. Otherwise, the
effect of O_TRUNC is unspecified.` It appears exactly once. 17 words ≤ 25. The gate's stated
method — "matched after whitespace normalisation and tag stripping" — is the method under
which it matches; the raw HTML has a line break between `it` and `will`.

### F2 — Anchor is correct (holds)

`§DESCRIPTION, O_TRUNC entry in the file creation flags list` is accurate: `O_TRUNC` is listed
in the DESCRIPTION file-creation-flags enumeration
(`O_CLOEXEC, O_CREAT, O_DIRECTORY, O_EXCL, O_NOCTTY, O_NOFOLLOW, O_TMPFILE, and O_TRUNC`), and
the quoted entry sits in the alphabetised flag list that follows, still inside DESCRIPTION.
Revision `Linux man-pages 6.19`, footer date `2026-02-08`, matches the anchor cell exactly.

### F3 — The `teaches` cell overstates the page in one clause (minor, non-blocking)

Row `teaches` (`corpus/SOURCES.md:81`) says `O_TRUNC truncates the file at open whenever the
access mode allows writing`. The page makes that conditional. Verbatim (page, O_TRUNC entry):

> "If the file already exists and is a regular file and the access mode allows writing (i.e.,
> is O_RDWR or O_WRONLY) it will be truncated to length 0. If the file is a FIFO or terminal
> device file, the O_TRUNC flag is ignored. Otherwise, the effect of O_TRUNC is unspecified."

The row's `whenever` drops three qualifications: the file must already exist, it must be a
regular file, and FIFO/terminal files ignore O_TRUNC ("otherwise … unspecified"). The chosen
quote cannot carry them: the full conditional sentence is 28 words, over the 25-word Gate
limit, and the quote starts mid-sentence after the 11-word
`If the file already exists and is a regular file and`.

Why this is non-blocking: the row's operative conclusion — an `O_RDWR` open is write-capable,
not a pure read — is independently stated on the same page: `The argument flags must include
one of the following access modes: O_RDONLY, O_WRONLY, or O_RDWR. These request opening the
file read-only, write-only, or read/write, respectively.` That sentence is 14 words and is a
valid ≤25-word grounding quote for the conclusion. The used-by entry's defect logic (collector
write-flag regex must include `RDWR`) rests on the access-mode fact, not on universal
truncation. [INFERENCE: the surviving-mutant receipt itself (`P05` / `X03DefectProbes.md:37`,
cited by the used-by entry) was not re-run here — that is other seats' scope.]

Minimal correction if the L1 wants the cell exact: say "truncates an existing regular file at
open when the access mode allows writing; O_TRUNC is ignored for FIFO/terminal files and
otherwise unspecified", or keep the wording and switch the Gate quote to the 14-word
access-modes sentence.

### F4 — Tier and kind fit (holds)

Contract `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` defines kind `docs` as a valid enum and
tier A as "primary or authoritative for that scope (spec, official docs, source code, …)".
A Linux man-pages page is official documentation, and the row's scope cell is deliberately
narrow: `open(2)'s access modes and open-time effects, for whether an O_RDWR open is a pure
read input`. Tier A is scoped to that, not to POSIX or to kernel-implementation behaviour.
Kind `docs` (not `spec`) is right: the page documents the syscall, it is not the standard.
Recheck `365d` is an allowed cadence. Observation, not a defect: it is the only man-page row
in this batch at `365d` (S067/S068/S069 use `180d`); the page is stable, so this is a taste
choice the contract permits.

### F5 — Used-by path exists and cites S072 (holds)

`corpus/knowledge/guard-kill-closure.md` exists at the read rev (`git cat-file -e` exit 0;
negative control exit 128). It cites S072 twice:

- `:1` — source list: `S072 — open(2) §DESCRIPTION, O_TRUNC, https://man7.org/linux/man-pages/man2/open.2.html`
  (same anchor as the row).
- `:118` — inside `## 6. Trace-collector guards` (`:116`):
  `A write-mode open with O_TRUNC truncates at open time whenever the access mode allows
  writing, and O_RDWR and O_WRONLY both do [src: S072, quote "the access mode allows writing
  (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0."].`

The inline quote is byte-identical to the Gate quote. The knowledge entry repeats the same
`whenever` overstatement; the same non-blocking qualification applies.

### F6 — Gate-file source-line check is imprecise (minor)

`.ufo/waves/round-18/staged/lesson-round-18-gate.md:30` says "the quote is the tag-stripped
text of the O_TRUNC sentence". It is a contiguous fragment of that sentence, not the whole
sentence: the first 11 words (`If the file already exists and is a regular file and`) are
omitted, and that omission is what permits the `whenever` reading in F3. The second half of
the claim — "no words are added or changed" — is true. Suggested wording: "a 17-word fragment
of the O_TRUNC sentence beginning after its two conditions".

## What was not checked

- The mutation receipt behind the `RDWR` guard (`P05`, `w1/X03DefectProbes.md:37`) and the
  promoted `tools/trace-inputs.py` exclusion — outside this row's target.
- No other used-by path exists to check; S072 lists exactly one.

## Verdict

**Partial (teaches-only): quote, anchor, 17/25 word count, `docs`/A tier, and the existing
used-by citation all verify at `01d586d`; the `teaches` cell and the used-by prose overstate
O_TRUNC by dropping the existing-regular-file condition, while the row's conclusion (O_RDWR
is write-capable) is independently supported by the page's access-modes sentence.**
