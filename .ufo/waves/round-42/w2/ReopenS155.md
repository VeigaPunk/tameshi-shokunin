# W2 ReopenS155 — re-open S155 (PIT basic concepts) and attack its row and quotes

seat: L1Tameshi42.ReopenS155 · date: 2026-10-25 · lane tip read: `a21845f523b75adbd3e3f7a62af91294db224ad9` (read-only; no counter run)
Tools installed or updated: none.

## Findings

### F1 — Re-open: the fresh fetch is byte-identical to the committed snapshot (held)

```
D=$(mktemp -d /tmp/tameshi-r42w2-ReopenS155-XXXX)   # → /tmp/tameshi-r42w2-ReopenS155-Vgax
curl -fsSL -m 60 -o "$D/pit-basic-concepts.html" https://pitest.org/quickstart/basic_concepts/   # curl_exit=0
sha256sum "$D/pit-basic-concepts.html" .ufo/evidence/round-42/sources/pit-basic-concepts.html
c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a  /tmp/.../pit-basic-concepts.html
c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a  .ufo/evidence/round-42/sources/pit-basic-concepts.html
wc -lc → 270 lines, 12155 B each;  cmp → IDENTICAL
```

- The committed blob matches too: `git show a21845f:.ufo/evidence/round-42/sources/pit-basic-concepts.html | sha256sum` → `c51d8423…92b3a`. The same holds at `5f739ac`, the commit that added it.
- `.ufo/evidence/round-42/sources/sha256.txt:1` has the same digest. `opened-at.txt` reads `2026-10-25T09:35:08Z`.
- `<title>Basic concepts</title>` is at snapshot line 5, which matches the title quoted at `corpus/lessons/round-42.md:19`.

### F2 — The S155 row at `corpus/SOURCES.md:125` (held)

Parsed with `python3` (`row.strip().strip('|').split('|')`). It has **11 cells**, matching the header at `corpus/SOURCES.md:10`, and **0** `\|` escapes. Because the split yields exactly 11 cells, no cell contains a pipe.

| # | cell | check |
|---|---|---|
| 1 | `S155` | ok |
| 2 | `Basic concepts (PIT docs) — https://pitest.org/quickstart/basic_concepts/` | URL re-fetched, exit 0 (F1) |
| 3–4 | `docs`, `A` | ok |
| 5 | scope: PIT's outcome vocabulary for F1 interop | ok |
| 6 | anchor `§Running the tests (outcome list) … 12155 B sha256 c51d8423` | `<h2 id="running-the-tests">Running the tests</h2>` is at snapshot line 154 and is the last `<h2>` in the file, so the section runs to the end and covers lines 163–194. The size and digest prefix both match (F1). |
| 7 | teaches: "seven outcomes; No coverage is Survived with no exercising test; a run error means something went wrong when testing … not the Killed outcome" | Snapshot lines 166–172 hold exactly 7 `<li>` items: Killed, Survived, No coverage, Non viable, Timed Out, Memory error, Run error. The paraphrases match lines 179 and 192, and Killed is defined separately at line 175. |
| 8–10 | `mined`, `2026-10-25`, `180d` | ok |
| 11 | used-by `corpus/knowledge/pit-outcome-vocabulary.md` | `test -f` → exists; the file is tracked (`git ls-files --error-unmatch`) |

- **Used-by convention (observation, not a defect).** `corpus/README.md:530` and `corpus/lessons/round-42.md` also cite S155 but are not in the used-by cell.
  - No registry row lists README in used-by: `awk … $12 ~ README` → 0.
  - 26 rows do list a lesson. However, S153 and S154 are cited by `corpus/lessons/round-41.md` and `corpus/lessons/round-42.md` without listing either lesson.
  - The S155 omission therefore matches the most recent practice.

### F3 — Every quote attributed to S155 (all held)

Checks use the snapshot as committed:
- Python reads each cited line, strips tags with `re.sub(r'<[^>]+>','',…)`, and tests whether the quote appears on that line. It also counts hits in the whole flattened, tag-stripped text.
- Words are counted with `str.split()`.

| # | quote | file:line citing it | cited line | found on line (tag-stripped) | unique in page | words | ≤25 |
|---|---|---|---|---|---|---|---|
| Q1 | "For each mutation PIT will report one of the following outcomes" | `corpus/knowledge/pit-outcome-vocabulary.md:16-17` | 163 | 163 (raw too) | 1 | 11 | yes |
| Q2 | "No coverage is the same as Survived except there were no tests that exercised the line of code where the mutation was created" | `pit-outcome-vocabulary.md:19-21` (states 23 words); `corpus/lessons/round-42.md:23` (line 179, 23 words; paraphrased as "the No coverage sentence", not quoted) | 179 | 179 | 1 | 23 | yes |
| Q3 | "Killed means a test caught the mutation successfully." | `pit-outcome-vocabulary.md:22-23` (8 words); `corpus/lessons/round-42.md:21-22` (8 words) | 175 | 175 | 1 | 8 | yes |
| Q4 | "A run error means something went wrong when trying to test the mutation." | `pit-outcome-vocabulary.md:23-24` (13 words); `corpus/lessons/round-42.md:22-23` (13 words) | 192 | 192 | 1 | 13 | yes |

- All four quotes are verbatim, every cited line number is correct, and every stated word count matches.
- `corpus/knowledge/r42-attribute-and-outflag-destinations.md` attributes **no** quote to S155. `grep -n -i -E 'S15[5-8]|pitest|PIT\b'` hits only S157 and S158 lines (:1, :4, :13, :19, :42, :61–64), and its `source:` header names S157, S153, S001 and S158.
- **Observation, not breakage.** Q2, Q3 and Q4 do not appear in the raw bytes, because the snapshot wraps the outcome names in `<strong>`. For example, line 175 is `<p><strong>Killed</strong> means a test caught …`. A raw `grep -F 'Killed means'` on the snapshot finds nothing; the quotes are located only in tag-stripped text.
  - The S157 entry says so in its recheck (`r42-attribute-and-outflag-destinations.md:6`, "in the tag-stripped text").
  - The `recheck:` line of `pit-outcome-vocabulary.md:6` asks to "re-locate the quotes" and does not say tag-stripped.
  - Its live predicate uses a fragment that does survive in raw HTML, so the predicate itself is sound (F4).

### F4 — Claims about S155 beyond quotes (held)

- **Live recheck predicate** at `pit-outcome-vocabulary.md:6`: `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'there were no tests that exercised the line of code'` → `1`, which matches "(1 on 2026-10-25)".
- **Stripped recheck** at `corpus/lessons/round-42.md:87`: `curl -fsSL 'https://pitest.org/quickstart/basic_concepts/' | grep -c 'No coverage'` → `2`, which matches "(2 on 2026-10-25)". The same counts come from grepping the fresh file in the scratch dir.
- **"S155 defines no score at all"** (`corpus/lessons/round-42.md:43`): `grep -i -c 'score' pit-basic-concepts.html` → `0`. Held.
- **"A run error is not a kill in PIT's vocabulary"** (`pit-outcome-vocabulary.md:22`): this follows from Q3 and Q4, which define the two outcomes separately and give Run error no Killed status. The entry draws the scoring split from S158, not S155 (`:31`). Held.
- The renumber map in `corpus/lessons/round-42.md:75`, `corpus/SOURCES.md:447` and `LOG.md:2206` (`staged:S159` → S155) agrees across all three files and names the same URL.

## Scratch

`/tmp/tameshi-r42w2-ReopenS155-Vgax` was deleted before return. No lane file was touched except this report.

Verdict: SURVIVES
