# ReopenS073 — independent re-open of SOURCES row S073

Seat: `TameshiR18.ReopenS073` (scout, wave 2). Read rev
`01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; comparison base `183f87b`.
Live page opened 2026-10-20. One write only: this report. Scratch under
`/tmp/tameshi-r18w2-ReopenS073-3tnxuN`.

## Verdict

**Holds.** S073 is verbatim against the live page (22 words, exact §1.2
anchor), its teaches cell asserts nothing the page does not say, tier `A` /
kind `docs` fit the frozen contract, and its used-by path exists at the read
rev and cites S073 twice. Three non-blocking wording/completeness notes below.

## 1. Row presence and shape

```
$ git -C <lane> show 01d586d:corpus/SOURCES.md | sed -n '82p' | awk -F'|' '{print NF}'
13
```

- `corpus/SOURCES.md:82` — `| S073 | Command line and environment (CPython
  3.15.0 docs) — https://docs.python.org/3/using/cmdline.html | docs | A | … |
  mined | 2026-10-20 | on-release | corpus/knowledge/guard-kill-closure.md |`
- Fields: kind `docs`, tier `A`, status `mined`, opened `2026-10-20`,
  recheck `on-release`, used-by `corpus/knowledge/guard-kill-closure.md`.
  NF = 13, the contract's row shape (`SOURCES-CONTRACT-v1.md:19`).
- Base `183f87b:corpus/SOURCES.md` contains 0 occurrences of `S073`; the row
  is new in round 18. Its installed row matches the staged registry byte for
  byte: `git show 01d586d:.ufo/waves/round-18/staged/corpus/SOURCES.md | diff -
  <(git show 01d586d:corpus/SOURCES.md)` → no output, printed `IDENTICAL`.
- Census enum / tier-inflation awk rules copied from the in-lane
  `sources-census.sh` (`.ufo/evidence/kaika-round-1/sources-census.sh:6`),
  applied to `git archive 01d586d corpus`: **no output** (no enum violation,
  no tier inflation; 72 rows parsed). S073 specifically: tier `A` ∈ `[ABC]`,
  kind `docs` ∈ the enum, and not the `A + community` case.

## 2. Quote verbatim at the stated anchor, ≤ 25 words

Staged quote: `.ufo/waves/round-18/staged/lesson-round-18-gate.md:25`
(`# quote … (§1.2 Environment variables, PYTHONPYCACHEPREFIX)`).

Live fetch:

```
$ curl -sS -o …/cmdline.html -w 'http=%{http_code}\n' https://docs.python.org/3/using/cmdline.html
http=200
$ sha256sum …/cmdline.html
7642c278e14be8bf334dbfc586686e246f42c054493336888de49d9f11278dd5
```

- Same hash from three variants today — plain `curl -sS`, `curl -fsSL`, and
  `curl --compressed` — so the served bytes are stable for this session.
- Title: `1. Command line and environment — Python 3.15.0 documentation`, so
  the source cell's "CPython 3.15.0 docs" and the anchor's "@ Python 3.15.0
  docs" both fit.
- Section: `<h2><span class="section-number">1.2. </span>Environment
  variables</h2>` (HTML line 987). The two anchor ids exist exactly once each
  (`envvar-PYTHONDONTWRITEBYTECODE`, HTML line 1131;
  `envvar-PYTHONPYCACHEPREFIX`, line 1139) and both sit inside the open §1.2
  section (1 `<section>` opened, 0 closed between section start and each
  `<dt>`).
- Verbatim: after tag stripping and whitespace normalisation, the staged text
  is a contiguous substring of the `PYTHONPYCACHEPREFIX` `<dd>`:
  `quote in entry: True`. The only raw markup inside the sentence is
  `<code>` around `.pyc` and `__pycache__`; stripping reproduces the staged
  words exactly.
- Word count (whitespace split of the quoted string): **22** ≤ 25.
- Truncation: the page continues ` within the source tree. This is equivalent
  to specifying the -X pycache_prefix=PATH option.` The gate quote stops at
  `directories` with no ellipsis (see minor note 2).

## 3. Teaches cell does not overstate the page

Page text at the two anchors (tag-stripped):

> **PYTHONDONTWRITEBYTECODE** — If this is set to a non-empty string, Python
> won’t try to write .pyc files on the import of source modules. This is
> equivalent to specifying the -B option.
>
> **PYTHONPYCACHEPREFIX** — If this is set, Python will write .pyc files in a
> mirror directory tree at this path, instead of in __pycache__ directories
> within the source tree. This is equivalent to specifying the -X
> pycache_prefix=PATH option. Added in version 3.8.

Clause-by-clause:

| Row clause (`SOURCES.md:82`, field 8) | Page support | Verdict |
|---|---|---|
| non-empty `PYTHONDONTWRITEBYTECODE` equals `-B` | "This is equivalent to specifying the -B option." | exact |
| … stops `.pyc` writes on import of source modules | "won’t try to write .pyc files on the import of source modules" | paraphrase, no strengthening of scope |
| set `PYTHONPYCACHEPREFIX` writes `.pyc` in a mirror tree at that path instead of `__pycache__` | "will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories within the source tree" | exact except the omitted qualifier (immaterial) |
| (added in 3.8) | "Added in version 3.8." | exact |
| a fixture can keep bytecode out of the source tree by environment | entailed by the mirror-tree sentence; "can" keeps it conditional | sound application |
| the entries state write behaviour only and say nothing about reads | regex over both entries for the tokens `read`, `reads`, `load`, `loads`, `cache`, `existing` (case-insensitive) → all False | true |

No teaches clause claims more than the page states.

## 4. Tier / kind / anchor fit (frozen contract)

Contract: `<fleet>/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` at fleet commit
`5b471e4` (sha256 `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119`).

- kind enum includes `docs` (`:24-25`) — prose documentation, not a spec,
  fits.
- tier **A** = "primary or authoritative for that scope (spec, official docs,
  source code, original paper, maintainer statement, …)" (`:26-30`) —
  official CPython docs are the authoritative source for CPython env-var
  behaviour: fits. No `A + community` inflation.
- anchor = exact section/heading plus revision, "never a bare homepage"
  (`:32-33`) — row carries §1.2, both entry ids, `Python 3.15.0`, fetched
  `2026-10-20`: fits.
- `mined` requires ≥ 1 used-by path (`:36-37`); one is present.
- Gate rule (`:45-47`) requires URL + access date + ≤ 25-word quote with
  location: all three are in the staged gate row.

## 5. Used-by path exists and cites S073

```
$ git -C <lane> cat-file -e 01d586d:corpus/knowledge/guard-kill-closure.md
exit 0 (EXISTS)
$ git grep -n 'S073' 01d586d -- corpus/
corpus/knowledge/guard-kill-closure.md:1      (header source list)
corpus/knowledge/guard-kill-closure.md:120    (body, under §6 at :116)
corpus/README.md:266                          (coverage map row)
corpus/SOURCES.md:82, :207
```

- `guard-kill-closure.md:1` names it in the note's `source:` header:
  "S073 — CPython 3.15 command line §1.2 PYTHONPYCACHEPREFIX and
  PYTHONDONTWRITEBYTECODE".
- `guard-kill-closure.md:120` (inside `## 6. Trace-collector guards`, heading
  at `:116`) cites the row for the actual claim:
  "`PYTHONPYCACHEPREFIX` writes `.pyc` files in a mirror tree at that path
  instead of `__pycache__`. A non-empty `PYTHONDONTWRITEBYTECODE` stops `.pyc`
  writes on import [src: S073, quotes]." — a substantive, matching citation.
- Census E11 (mined used-by missing) and H4 (mined used-by file lacks the row
  id) at the read rev: no `S073` line, so both pass. (H4 prints only
  `S031`–`S037`, a registry-wide pre-existing condition outside this row.)
- Completeness: no other file under `corpus/knowledge/` or `corpus/lessons/`
  cites S073; `corpus/README.md:266` lists it in the note's coverage-map
  sources, consistent with the used-by cell.
- Staged lesson's census note (`.ufo/waves/round-18/staged/lesson-round-18-gate.md:97-100`)
  claims 8 E11 "used-by path missing" at base for this path. Verified
  independently: `git cat-file -e 183f87b:corpus/knowledge/guard-kill-closure.md`
  → exit 128 ("exists on disk, but not in '183f87b'"), and the staged
  registry has exactly 8 mined rows citing that path (S065 S066 S068 S069
  S070 S072 S073 S074).

## 6. Staged served-hash note (surrounding claim)

Staged lesson `:32-34` says the draft recorded served-HTML sha256
`a4863a38…b734` and a re-fetch returned `7642c278…dd5`. Both halves check out:
the draft hash is on record at `.ufo/waves/round-18/w1/B10SrcPycachePrefix.md:8`
and `.ufo/waves/round-18/sources/S074-B10SrcPycachePrefix.md:11,18`, and all
three of today's fetches return
`7642c278e14be8bf334dbfc586686e246f42c054493336888de49d9f11278dd5`. Dropping
the served-HTML hash from the registry row was therefore correct; the quote
is unchanged.

## Minor gaps (non-blocking)

1. **Scope cell verb.** `SOURCES.md:82`, field 6 says "the two environment
   variables that **redirect** .pyc writes". Only `PYTHONPYCACHEPREFIX`
   redirects; the page says `PYTHONDONTWRITEBYTECODE` stops writes ("won't try
   to write"). The teaches cell states both correctly, so nothing downstream
   is misled, but "control" would be exact. Wording only; the row's status,
   tier and citations are unaffected.
2. **Gate quote truncation.** The S073 quote is a verbatim prefix that ends
   mid-sentence at `directories`, without an ellipsis; the page continues
   ` within the source tree.` The house method (whitespace normalisation + tag
   stripping) and the ≤ 25-word rule are satisfied, and other gate rows
   truncate similarly (e.g. S070), but the dropped qualifier is exactly what
   scopes "instead of `__pycache__`". Suggest `…` on a future gate pass.
3. **One quote, two entries.** The gate's single S073 quote grounds the
   `PYTHONPYCACHEPREFIX` half of a two-entry teaches cell; the
   `PYTHONDONTWRITEBYTECODE` clause rests on the anchor's second id, not on a
   quoted sentence. Not a contract breach (the rule says "a ≤ 25-word quote"),
   but a cold reader checking only the quote cannot see the `-B` equivalence.

Nothing here moves the row's tier, status, or citation chain.

## Commands exercised (exit 0 unless stated)

1. `git -C <lane> show 01d586d:corpus/SOURCES.md | sed -n '82p' | awk -F'|' '{print NF}'` → `13`.
2. `git -C <lane> show 01d586d:corpus/SOURCES.md | grep -c S073` → `2`; same at `183f87b` → `0`.
3. `git -C <lane> cat-file -e 01d586d:.ufo/waves/round-18/staged/…` + `diff` against installed `corpus/SOURCES.md` → identical.
4. `curl -sS … https://docs.python.org/3/using/cmdline.html` → `http=200`,
   sha256 `7642c278…dd5`; `curl -fsSL` and `curl --compressed` → same hash.
5. Python 3 extraction over the fetched HTML: title, `<h2>` 1.2 heading, both
   `<dt>` ids (one occurrence each, inside the open section), quote substring
   `True`, word count `22`, continuation ` within the source tree. …`,
   read-word regex false on both entries.
6. `git archive 01d586d corpus | tar -x -C <tmp>` then the census `awk` rules
   from `.ufo/evidence/kaika-round-1/sources-census.sh:6-8` → rows `72`,
   enum/tier output empty, E11 empty, H4 outputs only S031–S037.
7. `git -C <lane> git grep -n S073 01d586d -- corpus/` → 4 hits (SOURCES
   `:82`, `:207`; knowledge `:1`, `:120`; README `:266`).
8. `git -C <lane> cat-file -e 183f87b:corpus/knowledge/guard-kill-closure.md`
   → **exit 128** (absent at base).
9. `git -C <fleet> show 5b471e4:.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` →
   contract read for kind/tier/anchor/used-by/gate rules.

## Inputs (lane-relative, sha256 at the read rev)

| path | sha256 |
|---|---|
| `corpus/SOURCES.md` | `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` |
| `corpus/knowledge/guard-kill-closure.md` | `9312bdebd4e93d427ea32d3db8652f95530237477b49ffecffdf4e4ac49991fb` |
| `.ufo/waves/round-18/staged/lesson-round-18-gate.md` | `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` |
| `.ufo/evidence/kaika-round-1/sources-census.sh` (census rule source) | `30fb4e9bede2a3aabe36ada66de0499d942f856ec72d77b9f852afbc50206c40` |

External: `<fleet>/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` @ `5b471e4` —
sha256 `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119`.
Live page `https://docs.python.org/3/using/cmdline.html` — sha256
`7642c278e14be8bf334dbfc586686e246f42c054493336888de49d9f11278dd5`.

**Verdict: holds — S073 is verbatim at the stated §1.2 anchor (22 words), does not overstate the page, fits tier A / kind docs, and its used-by path exists and cites it; only the scope cell's "redirect" verb and the gate quote's mid-sentence truncation are imprecise (both non-blocking).**
