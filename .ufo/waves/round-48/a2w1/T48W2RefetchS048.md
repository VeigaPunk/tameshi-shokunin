# T48W2RefetchS048 — independent re-open of C2 target S048

Seat: T48W2RefetchS048 (leaf, attempt 2 / a2w1). Judged on freshness. I am not an author of the
material I attacked: I wrote no part of SOURCES.md, the lesson, the entry, the snapshot, the
receipt, the counters or the contract, and I changed only this report file.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- CONTENT revision opened: `c7586b9a10effc63b4bd327f976edc094c1bdc17` (attempt-2 content revision)
- Base: `473336d9d789f6081195e7376d17836a24666bc3`; counter freeze: `755298415f8c…` (`freeze-2.json`)
- Lane HEAD at read time: `17cc5ce141868454d05bf75ef5cd230e35f0cdf4` (a2w1 wave spec only)
- Scratch: `/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS048` (removed; see §7)

## 1. My own live fetch (independent of the author's receipt)

```
S=/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS048
curl -sS -L -D "$S/headers.txt" -o "$S/S048.live.html" \
     -w '%{http_code} %{size_download} %{url_effective}\n' \
     --max-time 60 https://pitest.org/quickstart/incremental_analysis/
sha256sum "$S/S048.live.html"
```

Observed (2026-10-26T13:29:04Z):

| field | live | committed receipt `.ufo/evidence/round-48/freshness/sources/S048.receipt.json` |
|---|---|---|
| HTTP | `HTTP/2 200` | `http_status: 200` |
| bytes | 8892 | `bytes: 8892` |
| sha256 | `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db` | same |
| url | `https://pitest.org/quickstart/incremental_analysis/` (no redirect) | same |
| `Last-Modified` | `Wed, 03 Jun 2026 08:45:37 GMT` → 2026-06-03 | S266 anchor cell: `Last-Modified 2026-06-03` |
| `content-length` / `etag` | `8892` / `"6a1fe9b1-22bc"` | (not claimed) |
| fetch time | 2026-10-26T13:29:04Z | `fetched_at: 2026-10-26T08:40:42Z` |
| tool | `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 …` | identical tool string |

`cmp` of the live bytes against the committed snapshot:

```
cmp "$S/S048.live.html" .ufo/evidence/round-48/freshness/sources/S048.html && echo CMP: byte-identical
→ CMP: byte-identical
```

So the live page is **byte-identical** to the committed snapshot *and* to the receipt digest, and the
committed worktree file is identical to the committed blob:

```
git cat-file -p bf79e4f8623334bcbc6cefbeb7734251b7d8d2d7 | sha256sum
→ e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db
cat-file of receipt blob c7f27113… vs worktree receipt → diff empty, IDENTICAL
```

No drift of the pitest page since 2026-10-26T08:40:42Z (and, by the retained kaika digest, since
2026-10-19T21:47:33Z: `.ufo/evidence/kaika-round-1/sources-opened.tsv:33` carries the same sha256).

## 2. The registry rows (CONTENT rev)

```
git show c7586b9a10effc63b4bd327f976edc094c1bdc17:corpus/SOURCES.md | sed -n '57p;141p'
```

Header: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (`corpus/SOURCES.md:10`).

- **S048 (held, unchanged since base)**: source cell `https://pitest.org/quickstart/incremental_analysis/`;
  teaches `supersedes S047 — item 4 is prioritisation rather than a reuse skip; no claim here resolves its
  pronoun to test versus mutation; item 5 is explicitly not yet implemented and the dependency assumption
  remains unproven`; used-by `corpus/knowledge/incremental-pin-disposition.md`.
- **S266 (new)**: id above S264; source cell carries T's URL; scope `supersedes S048's anchor and quote only:
  PIT's item-4 prioritisation distinction, with the disputed consequent located on the 2026-10-26 bytes`;
  anchor `§Incremental analysis, item 4 (raw line 86); page version unstated, Last-Modified 2026-06-03,
  fetched 2026-10-26; sha256 e9cbc3e1ab7c, 8892 bytes`; teaches opens
  `supersedes S048 — item 4 is prioritisation rather than a reuse skip, its consequent is the located quote,
  no claim here resolves its pronoun to test versus mutation, item 5 is not yet implemented and the
  dependency assumption remains unproven`; status `mined`; opened `2026-10-26`; recheck `90d`; used-by
  `corpus/knowledge/incremental-pin-disposition.md`.

Exactly one row opens `supersedes S048 —`:

```
awk -F'|' 'NF>=9 {g=$8; sub(/^[ \t]+/,"",g); if (g ~ /^supersedes S048 —/) print $2}' corpus/SOURCES.md
→  S266
```

Anchor cell claims verified against the bytes:

```
grep -n "prioritised above others" .ufo/evidence/round-48/freshness/sources/S048.html
→ 86:  <li>If a mutation was previously killed, but the class or killing test has changed then it is likely
  that the last killing test will still kill it and it should therefore be prioritised above others. (since 1.14.4)</li>
```

Raw line 86 is the **fourth `<li>`** of the single `<ol>` (`<ol>` at line 82; `<li>` at 83, 84, 85, 86, 87;
item 5 = line 87, `<em>… (not yet implemented)</em>`). "item 4 (raw line 86)" ✓.

## 3. The Gate line and the quote — verdict per check

```
grep -n "C2-QUOTE" corpus/lessons/round-48.md
→ 21 S265 S026, 22 S266 S048, 23 S267 S093, 24 S268 S108   (one line per target, 4 total)
```

Line 22, parsed with the amendment-2 grammar `^- C2-QUOTE (S[0-9]{3,}) (S[0-9]{3,}): `([^`]+)`$`
(parsed with `re.M`, anchors satisfied): `R=S266`, `T=S048`,
quote = `then it is likely that the last killing test will still kill it and it should therefore be prioritised above others`.

Amendment-2 extraction (UTF-8, no script/style contents, tags stripped, `html.unescape`, every whitespace
run collapsed to one space, no case/punctuation folding) applied to the snapshot, and separately to my own
live bytes:

| check | result |
|---|---|
| quote is a substring of the **snapshot's** extracted text | **yes** — once, at normalized offset 1014 of 3255 chars (the frozen counter's own `extract()` gives 1013 of 3253; the 1-char/2-char delta is only `tag→' '` vs my `tag→''`) |
| quote is a substring of the **live** extracted text (my fetch) | **yes** — same offset, because live bytes == snapshot bytes (`cmp` above) |
| quote present literally in the raw snapshot bytes | **yes** (ASCII quote, raw line 86) |
| word count per amendment 2 (whitespace tokens) | **21** ≤ 25 |
| required phrase `should therefore be prioritised` | **present, exactly once, case-exact** |
| boilerplate / navigation? | **no** — it is the consequent of item 4 of the optimisation list, page content |
| states the row's teaches claim? | **yes for the clause it is offered for**: teaches says "item 4 is prioritisation rather than a reuse skip, its consequent is the located quote". The quote is that consequent ("should therefore be prioritised above others") and, with the same `<li>`'s antecedent it follows, it is PIT's ordering rule for a previously killed mutation whose class/killing test changed. It does **not** carry the teaches cell's other two clauses (item 5 not implemented; dependency assumption unproven) — the contract does not require them in the quote, and the entry cites them from their own sentences |
| the fix matches the round-45 dispute it claims to answer | **yes** — `.ufo/evidence/round-45/freshness/reviews.json` (id S048, reviewer CritJudge02) named the missing text as `then it is likely that the last killing test will still kill it and it should therefore be prioritised above others`; the Gate line is that text verbatim |

Lesson Admit block (lines 35-42) restates the same facts: HTTP 200, 8892 bytes, sha prefix `e9cbc3e1ab7c…`,
`Last-Modified: 2026-06-03`, 21 words, fourth `<li>`, raw line 86. All confirmed above.

## 4. Knowledge entry of S048's base used-by cell

Base used-by cell `corpus/knowledge/incremental-pin-disposition.md` (one entry). At CONTENT rev:

```
git show c7586b9a10effc63b4bd327f976edc094c1bdc17:corpus/knowledge/incremental-pin-disposition.md | sed -n '1,6p'
git diff 473336d9… c7586b9a… -- corpus/knowledge/incremental-pin-disposition.md   → 1 file, +2/−2 (lines 1 and 2)
```

- line 1 `source:` (inside the first 10 lines) now cites **S266** with `re-fetched 2026-10-26T08:40:42Z,
  sha256 e9cbc3e1ab7c… (8,892 B)`; line 2 `verified-at: 2026-10-26`.
- S266's used-by cell lists exactly `corpus/knowledge/incremental-pin-disposition.md` — no extra, none missing.

Every claim in that entry which rests on S048/the pitest bytes, checked against the live text
(live == snapshot bytes, so the same check holds for the snapshot). Containment tests ran on the
amendment-2 extracted live text; source lines are the entry at CONTENT rev.

| entry loc | claim | live evidence | verdict |
|---|---|---|---|
| :1 | S266, same URL, §Incremental analysis (items 1–5 + dependency paragraphs), re-fetched 2026-10-26T08:40:42Z, sha256 `e9cbc3e1ab7c…`, 8892 B | my fetch: 200 / 8892 B / same sha | holds |
| :5 | "same reopened bytes and numbered items 4–5 as S041/S047" | sha equals S041's recorded digest in the same `source:` line; the page has numbered items 1–5 (one `<ol>`, raw lines 83–87) | holds |
| :5, :346-349 | "object-neutral prioritisation distinction"; "item4 prioritisation, not a reuse skip; no pronoun referent is resolved here" | `With the exception of 4), all these optimisations introduce a degree of potential error…` (1×) + `…should therefore be prioritised above others` (1×) | holds |
| :63-66 | rule 4 is prioritisation not a reuse skip, quoted `should therefore be prioritised above others` `(since 1.14.4)`; "the pronoun's referent is left as written"; rule 5 is `not yet implemented` | `since 1.14.4` 1×; `not yet implemented` 1× (item 5) | holds |
| :52-57 | rule 1 conditions on the class, rule 2 on class+killing test, rule 3 on covering tests | the three quoted sentences are located verbatim on the page | holds |
| :47-50 | "PIT calls the feature experimental and frames reuse as inference" | `PIT contains an experimental feature…`; the inference paragraph is located verbatim | holds |
| :59-61 | "With the exception of 4), all these optimisations introduce a degree of potential error into the analysis." | located verbatim, 1× | holds |
| :71-76 | dependency limitation quote; assumption `it is currently unproven` | sentence located; `it is currently` 1×, `unproven` in `<strong>` | holds in substance, **not byte-exact** — see F2 |
| :78-80 | "you will need to implement some mechanism to swap the values between runs" | present verbatim | holds |
| :97-100 | S047's summary: experimental, unproven, item 4 exception, item 5 not implemented | all four located | holds |
| :286-303 | S003/S041 re-open digests equal the kaika opening digests | `.ufo/evidence/kaika-round-1/sources-opened.tsv:33` digest = `e9cbc3e1ab7c…` = today's fetch | holds |

Side check of the entry's own `recheck:` probes (line 3), which touch the pitest bytes:
`curl -fsSL https://stryker-mutator.io/... | grep -c 'The dry run remains required'` → 1 and
`'Any other changes to your environment are not detected'` → 1; on the pitest page
`all these optimisations introduce a degree of potential error` → 1 and `it is currently` → 1. All four
still hold live (commands re-run today, 2026-10-26).

No claim that rests on S048 was found to have stopped holding. The re-pointing is therefore not a
"re-pointed anyway" case.

## 5. Findings

**F1 — `corpus/lessons/round-48.md:41` attaches the unresolved pronoun to the wrong clause (low; prose,
not a C2 field).** The Admit block says "the pronoun in “still kill it” is left unresolved". On the live
text the object of "kill it" is available: a killing test kills the mutation (item 1 of the same list says
"this mutation is still killed"; item 4's subject is "a mutation was previously killed"). What the lane
actually declines to resolve — S047's "prioritises an old killing test" vs S048's object-neutral
statement — is the referent of the *prioritisation* clause "it should therefore be prioritised above
others", not the object of "still kill it".

```
grep -n "still kill it" corpus/lessons/round-48.md
→ 41:  a prioritisation, not a reuse skip, and the pronoun in “still kill it” is left unresolved.
sed -n '86p' .ufo/evidence/round-48/freshness/sources/S048.html
→ <li>If a mutation was previously killed, but the class or killing test has changed then it is likely that
  the last killing test will still kill it and it should therefore be prioritised above others. (since 1.14.4)</li>
```

This does not touch the Gate line or any frozen check; the Gate quote is located and carries the phrase.
Reported because I am the seat that re-opened this target's bytes.

**F2 — `corpus/knowledge/incremental-pin-disposition.md:74` is not a byte-exact quote (low; pre-existing,
carried through the re-point).** S266's source cell / the entry's `source:` line says "The quoted excerpts
in §1 are the retained location". The dependency-paragraph excerpt differs from the live text in one
character: the entry writes `class's` (U+0027) where the page serves `class’s` (U+2019). Everything else in
that excerpt matches.

```
git show c7586b9a…:corpus/knowledge/incremental-pin-disposition.md | sed -n '74p'
# vs extracted live text
```

Not introduced by round 48 (present since round 13) and it changes no claim: the "unproven" sentence and
the dependency limitation both hold. No fix made — out of my write scope.

**F3 — disclosure, not a defect: `corpus/knowledge/fleet-kill-rate-ledger.md:374` still names S048.**
"source method: S003 and S048" for the round-13 `result_reuse=not_established` claim. That path is not in
S048's base used-by cell, so it is outside C2's entry requirement, and its claim still holds on live text
(`not_established` follows from the unproven assumption and the coordinate/strongest-dependency limit,
both located). It simply is not re-pointed to S266; the newest-row convention would eventually want S266,
but nothing in the frozen predicate asks for it.

**F4 — observation on attestation dates (informational).** `verified-at: 2026-10-26` (entry line 2) is
dated for the whole entry; the `recheck:` commands on line 3 are still dated 2026-10-20, and only the PIT
half is given a 2026-10-26 re-fetch in the `source:` line. I re-ran all four recheck probes live today and
they return the claimed counts (1/1/1/1), so the date claim is true in fact; the point is that only the
S048/S266 half carries a 2026-10-26 dated receipt inside the entry.

Residual observation on the Gate quote itself (no finding): the quote is the consequent only and begins
mid-sentence ("then it is likely…"), so the Gate line alone does not name what is prioritised; the lesson
Admit block and S266's anchor supply the antecedent and the item number. The round-45 defect was the
*opposite* truncation (antecedent without consequent), and this is the dispute's own nominated text, so
this is the registered remedy, not a regression.

## 6. Counter probes (probes, not verdicts)

```
python3 .ufo/evidence/round-48/freshness/measure.py --selftest
→ C2_R48_SELFTEST: cases=43 failed=0
sha256sum .ufo/evidence/round-48/freshness/measure.py
→ faefe9b442741bcd7238ffe028841a0da7453c14c70f9f33afbd0f77be2df63f   (= freeze-2.json freshness entry)

python3 .ufo/evidence/round-48/freshness/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --no-live
→ TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
  C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=off rev=c7586b9a… C2_R48_PARTIAL=true
```

Both ran with `TMPDIR` under my scratch dir; the counter's census materialises into its own temp tree and
the lane `corpus/`, `tools/`, `SCORECARD.md` stayed clean (`git status --porcelain` over those paths
returned nothing at read time). `C2_R48_PARTIAL=true` with `live=off` is the counter's own label for a
probe; it is not a verdict, and the deciding run is the L1's single invocation.

## 7. Verdict per the item's checks

| check | verdict |
|---|---|
| live fetch sha/bytes recorded | `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db` / 8892 B at 2026-10-26T13:29:04Z, HTTP 200 |
| quote located live | yes, once, offset 1014/3255 (counter extract: 1013/3253) |
| quote located in snapshot, byte-exact after whitespace collapse | yes — live bytes are byte-identical to the snapshot (`cmp`), quote present literally on raw line 86 |
| ≤25 tokens | 21 |
| carries required phrase `should therefore be prioritised` | yes, once, case-exact |
| states the row's teaches claim (not boilerplate/navigation) | yes for the clause it is registered for (item-4 consequent = prioritisation, the round-45 dispute's own nominated text) |
| used-by entry re-pointed and its S048 claims re-checked | source line cites S266, `verified-at: 2026-10-26`, R's used-by cell matches exactly; all S048-resting claims hold live |
| any finding that falsifies the target | none. F1/F2 are prose/verbatim nits in the lesson and entry, outside the frozen C2 fields |

Net: S048 is independently re-opened and consistent at CONTENT `c7586b9a…`. No falsifying finding; the
target's live freshness survives my own fetch, and the round-45 dispute that caused the re-anchor is
addressed with the exact text that dispute named.

## 8. Scratch, tools, risks

- Scratch `S=/fast/scratch/hyaku/tameshi-r48/T48W2RefetchS048` (fetch + headers + live extraction) was
  `rm -rf`'d before this report was finalised; nothing of mine remains on disk outside this report. I did
  not use `/tmp`, did not touch `.ufo/waves/round-48/w1`, and wrote no file in the lane except this report.
- No installs or upgrades: `curl 8.23.0` was already present and is the exact tool string the receipt
  records; `pacman` untouched (transactions paused host-wide anyway).
- Commands run against the lane were read-only: `git show`, `git cat-file`, `git ls-tree`, `diff`, `awk`,
  `grep`, `sed`, `sha256sum`, `python3`, and the counter in `--selftest` / `--no-live` probe modes. No git
  or jj mutation, no counter invocation with `live` on.
- Residual risk: the deciding run's own live fetch is the only live-mode check that counts; if pitest.org
  served different bytes to the L1 later today, that is the L1's observation to record, not something my
  snapshot-backed probe can pre-empt. Today the page is byte-stable across 2026-10-19, 2026-10-26T08:40Z and
  2026-10-26T13:29Z.
