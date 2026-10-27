# T53W1ScribeSource — S275/S276 registry row verification

- Seat: T53W1ScribeSource (scribe, wave 1, hyaku run 10 / tameshi round 53)
- Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
- Content commit C*: a41195dfc13a73958e4c5228ec196b28d03ded03 (lane HEAD at read time: ace79e3df61266e9474e5c02086c0f7c79664580)
- Rows under test: corpus/SOURCES.md:150 (S275), corpus/SOURCES.md:151 (S276)
- Scratch: /fast/scratch/hyaku/tameshi-r53/w1/T53W1ScribeSource (deleted before yield)
- Tools installed: none. `curl`, `pdftotext`/`pdfinfo` (poppler) were already on PATH; no pacman, no uv/npx/cargo/npm install was needed.
- No git/jj mutation was run anywhere; the only git reads were `rev-parse`, `log`, `show`, `status --porcelain`, `ls-files`, `check-ignore`, `cat-file` in the lane.

## Verdicts

| Row | Verdict | Scope of the verdict |
|---|---|---|
| S275 | **MISMATCH** (one cell) | URL/http/size/sha256/snapshot identity, quote content, 11-column parse, escaped-pipe absence and used-by cell all HOLD. The anchor cell's page — `p. 4` — does not hold: the located 93% sentence is on page **3** of the cited camera-ready (folio 1787). |
| S276 | **VERIFIED** | Every cell holds: HTTP 200, 41423 B, sha256 `d6dc4cf6…`, byte-identical snapshot, abstract quote re-located byte-exact, v1 / 2022-12-22 confirmed, 11 columns, no escaped pipes, used-by cell names the knowledge file. |

## What was run (commands and observed output)

Scratch dir created first: `mkdir -p /fast/scratch/hyaku/tameshi-r53/w1/T53W1ScribeSource`.

### 1. Re-fetch of both URLs (fresh copies)

```
curl -sS -L --max-time 120 -o cam2.pdf   -w 'PDF http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf
curl -sS -L --max-time 120 -o arxiv2.html -w 'ARXIV http=%{http_code} size=%{size_download} url=%{url_effective}\n' \
  https://arxiv.org/abs/2212.11762
```

Observed:

```
PDF http=200 size=131622 url=https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf
ARXIV http=200 size=41423 url=https://arxiv.org/abs/2212.11762
4d755c4e0b1925d131ed066195afb979a3651198188de044833884d59a22a869  cam2.pdf
d6dc4cf6512861f5d317dac3af751bfcf0887f3d7da000e9ed230e353f0a1487  arxiv2.html
131622 cam2.pdf
 41423 arxiv2.html
```

### 2. Committed snapshots

```
sha256sum .ufo/evidence/round-53/assimilation/S161-camera-ready.pdf .ufo/evidence/round-53/assimilation/S162-arxiv.html
cmp -s cam2.pdf  <snapshot>/S161-camera-ready.pdf
cmp -s arxiv2.html <snapshot>/S162-arxiv.html
```

Observed:

```
4d755c4e0b1925d131ed066195afb979a3651198188de044833884d59a22a869  …/S161-camera-ready.pdf     (131622 B)
d6dc4cf6512861f5d317dac3af751bfcf0887f3d7da000e9ed230e353f0a1487  …/S162-arxiv.html           (41423 B)
PDF cmp: IDENTICAL
HTML cmp: IDENTICAL
```

Both fresh fetches are byte-identical to the snapshots, and both snapshots reproduce the row cells' size and 8-hex sha prefix (`4d755c4e…`, `d6dc4cf6…`).

### 3. Row structure (11 columns, no escaped pipes, used-by)

```
python3 - <<'EOF'   # split each row line on '|', print column count and cells
...
EOF
awk 'NR>=150 && NR<=151 {n=gsub(/\|/,"|"); print NR": pipes="n}' corpus/SOURCES.md
```

Observed:

```
150 columns= 11   pipes=12   escaped pipes: False
151 columns= 11   pipes=12   escaped pipes: False
c11 = ' corpus/knowledge/change-aware-resweep-cadence.md '   (both rows)
line lengths: 150: 741 chars, 151: 636 chars
```

Table header at corpus/SOURCES.md matches the census schema (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`), so 11 cells is the expected width. The used-by path resolves: `corpus/knowledge/change-aware-resweep-cadence.md` exists (3582 B, `source:` lines 2–3 name S275 and S276).

### 4. Fleet census (W04 — informational)

```
cd /fast/scratch/hyaku/tameshi-r53/w1/T53W1ScribeSource
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

Observed (exit 0, last line `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`; the per-row lines are reproduced with the URL segment abridged to `…`, ids and warning classes verbatim):

```
tameshi W04 S047 … S048 … S075 … S076 … S077 … S078 … S081 … S092 …
tameshi W01 S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi W04 S104 … S160 … S265 … S266 … S267 … S268 …
tameshi W04 S274 duplicate url bazel.build/basics/hermeticity across scopes
tameshi ok   /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

**No W04 line for S275 or S276.** S274 (this round's other new row) does carry one; S275/S276 do not. This agrees with the round's own census snapshots (`.ufo/evidence/round-53/census-start.stdout`, `census-mid.stdout`), which likewise list S274 and no S275/S276 line.

Independent cross-lane check over the 21 sibling registries (`*/corpus/SOURCES.md` under /home/vgpnk/Projects/shokunin, excluding the lane):

```
for f in */corpus/SOURCES.md; do … grep -qF "3558911" | "2212.11762" | "change-aware-mutation-testing" …; done
```

Result: **no hit in any sibling lane** (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tsukuroi). Whole-fleet literal scan for the two URL strings (`grep -rlF`, excluding the lane) also returned nothing. In-lane the URLs occur exactly once each (`grep -c` = 1).

An earlier loose regex scan (`3558911\|2212\.11762`) hit two audio-shokunin receipt files; the context dump shows these are digit substrings inside timing integers, not URLs — false positives, not duplicates.

### 5. DOI (row anchor, not a fetch target of this item)

```
curl -sSI -L --max-time 25 https://doi.org/10.1145/3540250.3558911
doi http=403 final=https://dl.acm.org/doi/10.1145/3540250.3558911
```

The DOI resolves to the ACM DL record and is access-controlled (HTTP 403), matching what the round-53 lesson and knowledge entry already record. The DOI string itself is printed twice in the opened artefact (`5 pages. https://doi.org/10.1145/3540250.3558911`), and `pdfinfo` reports the title `Change-Aware Mutation Testing for Evolving Systems`, so the row's title/DOI pairing holds.

## S275 — MISMATCH detail

Row cells (corpus/SOURCES.md:150):

| # | Cell | Holds? | Evidence |
|---|---|---|---|
| 1 | `S275` | yes | unique id (`grep -c '^| S275 '` = 1) |
| 2 | title + DOI | yes | PDF `Title:` matches; DOI printed in PDF |
| 3 | `paper` | yes | — |
| 4 | `A` | yes | — |
| 5 | scope statement ("per-commit reuse decision … for F7") | yes | §3.2/§3.3 content; no measurable claim |
| 6 | `§3.2–3.3 (commit-relevant and subsuming mutants), p. 4 @ author camera-ready URL, fetched 2026-10-27 (HTTP 200, 131622 B, sha256 4d755c4e…)` | **no (page only)** | HTTP 200, 131622 B, sha256 `4d755c4e0b19…` all reproduce; §3.2 (`On the Use of Commit-Relevant Mutants`) and §3.3 (`Studying Relevance of Mutants to Code-Evolution`) both start on **page 3**; the 93% sentence is on page 3, not 4 |
| 7 | teaches cell (the 93% claim) | yes | verbatim source sentence located (below) |
| 8 | `mined` | yes | — |
| 9 | `2026-10-27` | yes | matches snapshot mtime and fetch date |
| 10 | `365d` | yes | schema cadence |
| 11 | `corpus/knowledge/change-aware-resweep-cadence.md` | yes | file exists and cites S275 |

Page evidence (two independent pdftotext modes, and folios):

```
pdfinfo cam2.pdf            -> Pages: 5, Title: Change-Aware Mutation Testing for Evolving Systems
folios page1..page5         -> 1785, 1786, 1787, 1788, 1789
pdftotext -f 3 -l 3         -> quote present on page 3
pdftotext -f 4 -l 4         -> "93%" absent; "reduce the number" absent
whole-document split on \f  -> pages containing "93%": [3]
```

Section placement on page 3 (`pdftotext -layout`, page 3): `3.2  On the Use of Commit-Relevant Mutants`, then `3.3  Studying Relevance of Mutants to Code-Evolution` (whose text contains the 93% sentence), then `3.4  Approximating Relevant Mutants with High-Order Mutations`. Page 4 carries the continuation of §3.3 — it contains "miss approximately 45% of subsuming commit-relevant mutants" — so a `§3.2–3.3` *span* does reach page 4, but the cited sentence does not.

Located sentence, verbatim (page 3, whitespace-normalised over the PDF's hard line wraps):

```
by selecting only subsuming commit relevant mutants, we reduce the number of mutants requiring analysis by around 93% on average
```

(continues: "Furthermore, we report that 69% of the mutants are located outside the changed methods…"; also on page 3: "around 30% of mutants are commitrelevant" — the PDF hyphenates "commit-relevant" at the line break, pdftotext joins it.)

Content comparison, row cell 7 vs source: the row says "selecting only subsuming commit-relevant mutants cut the mutants requiring analysis by around 93% on average". The source says "we reduce the number of mutants requiring analysis by around 93% on average". The magnitude, the population and the mechanism agree; this is a correct paraphrase. Only the page anchor fails.

Net: **MISMATCH on the anchor cell's page (`p. 4` → the carrier's page 3 / folio 1787)**; all other S275 cells verified against fresh bytes.

## S276 — VERIFIED detail

Row cells (corpus/SOURCES.md:151):

| # | Cell | Holds? | Evidence |
|---|---|---|---|
| 1 | `S276` | yes | unique id (`grep -c '^| S276 '` = 1) |
| 2 | title/authors/arXiv id | yes | `citation_title` = "Keeping Mutation Test Suites Consistent and Relevant with Long-Standing Mutants"; `citation_author` = Ojdanic, Milos / Papadakis, Mike / Harman, Mark |
| 3–4 | `paper`, `A` | yes | — |
| 5 | scope statement | yes | abstract is about comparability of re-computed suites |
| 6 | `§Abstract @ arXiv:2212.11762v1 (submitted 2022-12-22), fetched 2026-10-27 (HTTP 200, 41423 B, sha256 d6dc4cf6…)` | yes | HTTP 200, 41423 B, sha256 `d6dc4cf65128…`; page shows `Submitted on 22 Dec 2022`, `[v1]` and only v1; `citation_date` = 2022/12/22 |
| 7 | teaches cell (incomparability + 52% of 143,500) | yes | three fragments byte-exact in the fresh abs page |
| 8–10 | `mined`, `2026-10-27`, `365d` | yes | — |
| 11 | `corpus/knowledge/change-aware-resweep-cadence.md` | yes | file exists and cites S276 |

Located abstract text, verbatim (fresh `arxiv2.html`, HTML-unescaped):

```
Much previous work implicitly assumed it to be sufficient to re-compute mutant suites per release. Sadly, this makes mutation results inconsistent; mutant scores from each release cannot be directly compared, making it harder to measure test improvement.
```

```
We measure this degradation in relevance for 143,500 mutants in 4 non-trivial systems finding that, on overage, 52% degrade.
```

```
We also demonstrate how consistent-by-construction long-standing mutant suites can be identified with a 10x improvement in mutant relevance over an arbitrary test suite.
```

(`grep -cF` = 3 for each of the fragments "re-compute mutant suites per release. Sadly, this makes mutation", "finding that, on overage, 52% degrade", "143,500 mutants in 4 non-trivial systems" — the count of 3 is the abstract block plus the `citation_abstract` meta and the dc description copies on the same page.)

The row's paraphrase — "re-computing the mutant suite per release makes scores incomparable — 52% of 143,500 mutants degrade in relevance — so a pinned long-standing suite is the consistency device" — preserves the source's two separate claims (incomparability; measured relevance decay) and its proposal (consistent-by-construction long-standing suites). The paper's own typo "on overage" is in the carrier; the row does not reproduce it, which is fine for a paraphrase.

## Findings (calibration)

1. **S275 anchor page is wrong by one page.** Row cell 6 cites `p. 4`; the 93% sentence is on page 3 (folio 1787) of the cited camera-ready, and page 4 contains no occurrence of "93%". This is the only failing cell in either row.
   - Corroborating: `corpus/lessons/round-53.md` states "Located quote (22 words, camera-ready p. 4 …)" and `corpus/knowledge/change-aware-resweep-cadence.md:2` states "§3.2 (commit-relevant mutants) and §3.3 (subsuming, high-order mutations), p. 4" — the same page error is copied into both downstream artefacts. The knowledge file's line 19 quotes the sentence correctly otherwise.
   - Out of my write scope (never edit corpus/ or .ufo/evidence/), so this is reported, not fixed.

2. **S276 has no failing cell.** Nothing to report beyond the verdict.

## Informational / out of scope

- **Snapshot tracking:** in the git view of the lane, `.ufo/evidence/round-53/assimilation/` is untracked (`git status --porcelain` → `?? .ufo/evidence/round-53/assimilation/`; `git ls-files` empty; not gitignored). So the "committed snapshots" are working-tree files, and the byte identity above is against those files, not against a git blob. The lane is jj-colocated (`.jj` present); I did not run jj because every jj command snapshots the working copy, which would be a mutation. Readers who need the snapshot commit identity must resolve it in jj, not here.
- **Lesson word count:** `corpus/lessons/round-53.md` calls the S275 quote "22 words"; the quoted span tokenises to 20 words. Cosmetic, and in the lesson rather than the registry row.
- **W04:** no cross-scope duplicate warnings for either URL, from the census (exit 0, `ok`) and from a literal scan of all 21 sibling registries. S274 is the only round-53 row carrying a W04.
- **ACM copy:** 403 on the DOI (expected; recorded by the round's own lesson and knowledge entry), so the opened artefact remains the author camera-ready.

## Artifacts

- This report: /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w1/T53W1ScribeSource.md
- Fresh copies and extractions lived only in /fast/scratch/hyaku/tameshi-r53/w1/T53W1ScribeSource and were deleted before yield; no other file was created or modified.
