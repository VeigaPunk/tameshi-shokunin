# ReopenS156 — round 42 wave 2 (FALSIFY)

seat: L1Tameshi42.ReopenS156 (scout) · date 2026-10-25 · lane tip read: `a21845f523b75adbd3e3f7a62af91294db224ad9`
Attacked thing: the S156 row (`corpus/SOURCES.md:126`), its snapshot `.ufo/evidence/round-42/sources/pit-faq.html`,
and every quote attributed to S156 in the round-42 records.
No counter was run. No lane file was edited apart from this report. The tracked files read are byte-identical at
`a21845f` and in the working tree (`git show a21845f:<f> | cmp -s - <f>` printed "same" for all five).
No tools were installed.

## F1 — Re-open: the live page is byte-identical to the snapshot (survives)

```
D=$(mktemp -d /tmp/tameshi-r42w2-ReopenS156-XXXX)   # → /tmp/tameshi-r42w2-ReopenS156-aWxf
curl -fsSL -m 60 https://pitest.org/faq/ -o $D/pit-faq.html          # exit=0
sha256sum $D/pit-faq.html .ufo/evidence/round-42/sources/pit-faq.html
ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1  /tmp/tameshi-r42w2-ReopenS156-aWxf/pit-faq.html
ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1  .ufo/evidence/round-42/sources/pit-faq.html
wc -lc → 434 lines 20845 B (both);  cmp → IDENTICAL
```

The digest matches `.ufo/evidence/round-42/sources/sha256.txt:2`, the row's anchor (`20845 B sha256 ccf6ac49`), the
`source:` header at `corpus/knowledge/pit-outcome-vocabulary.md:2`, and `corpus/lessons/round-42.md:24-25`.
The page title is `<title>FAQ</title>` at snapshot line 5, which matches lesson line 24 ("title "FAQ"").
The recheck predicate in the lesson (`corpus/lessons/round-42.md:88`) also holds:
`curl -fsSL -m 60 'https://pitest.org/faq/' | grep -c 'timed out on one run'` returns `1`, both live and on the fresh file.

## F2 — The S156 row (survives)

`sed -n 126p corpus/SOURCES.md | awk -F'|' …` gives 13 fields, which is 11 cells. The header (line 10) also has 11.

| # | column | value |
|---|---|---|
| 1 | id | S156 |
| 2 | source | FAQ (PIT docs) — https://pitest.org/faq/ |
| 3 | kind | docs |
| 4 | tier | A |
| 5 | scope | PIT's own statement of which verdicts are run-dependent, for F1 and F3 |
| 6 | anchor | §Is it random? and §Timeouts @ page fetched 2026-10-25, snapshot …/pit-faq.html 20845 B sha256 ccf6ac49 |
| 7 | teaches | two factors, timeouts and static initializers, can make results differ … killed or survive on another |
| 8 | status | mined |
| 9 | opened | 2026-10-25 |
| 10 | recheck | 180d |
| 11 | used-by | corpus/knowledge/pit-outcome-vocabulary.md |

- **No pipe inside a cell.** `rg -c '\\\||`[^`]*\|[^`]*`'` on the row finds nothing (rc=1). The contract's NF check (`SOURCES-CONTRACT-v1.md:70`), run on a scratch clone, prints `nf!=13: 0` for the whole registry.
- **The anchor resolves.** `id="is-it-random"` is at snapshot line 287 and `id="timeouts"` at line 295. The anchor gives a fetch date plus the snapshot digest as the revision. 66 of 113 rows use the same `fetched` form, and the contract (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:32-33`) allows a dated revision.
- **The teaches cell is faithful to the source.**
  - "two factors" matches line 293.
  - "timeouts" matches `<h3 id="timeouts">` at line 295.
  - "static initializers" matches `<h3 id="static-initializers">` at line 301.
  - "small differences between runs" is at lines 303–304.
  - "timed out on one run, but killed or surviving on another" is at lines 298–299.
- **The used-by file exists.** `exists: corpus/knowledge/pit-outcome-vocabulary.md`, from the contract's used-by awk (`SOURCES-CONTRACT-v1.md:80`) run on the clone.
- **The registry validates.** `git clone --shared` into `/tmp/tameshi-r42w2-ReopenS156-clone` (HEAD `a21845f`), then `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md` exits 0 with `file ok`. It reports no code for S155–S158; the only warnings are the existing S101 W01 and S104 W04. The clone was removed afterwards.
- **Observation, not a defect: used-by omits the lesson.** The cell lists only the knowledge entry, but `corpus/lessons/round-42.md:24` and `corpus/README.md:530` also cite S156. The contract says used-by holds "the knowledge entries or lessons citing the row" (`SOURCES-CONTRACT-v1.md:40`). Only 26 of 113 rows list lessons, and S155, S157 and S158 follow the same knowledge-only pattern, so this is lane convention.
- **Observation: the Gate quote grounds only half of teaches.** The Gate (`corpus/lessons/round-42.md:24-27`) records only the line-293 quote. That quote grounds the first clause ("results differ between runs"). The second clause ("a mutant may time out on one run…") is grounded by the Timeouts quote, which the lesson's Gate does not record; it is located at `pit-outcome-vocabulary.md:28-30` and checked by the recheck predicate at `round-42.md:88`. Contract rule 1 (`SOURCES-CONTRACT-v1.md:45-47`) requires only "a ≤25-word quote … grounding `teaches`", so this is satisfied, though only partly for the second clause.

## F3 — Quotes attributed to S156 (all survive)

Method: I stripped tags from the snapshot, collapsed whitespace, and checked the exact strings with Python
(`q in flat`, per-line containment, and `len(q.split())`).

| # | where cited | quote | verbatim | words (claimed) | cited line | actual line |
|---|---|---|---|---|---|---|
| Q1 | `corpus/knowledge/pit-outcome-vocabulary.md:25-27` | "Pitest works hard to be fully deterministic, but two factors might cause the results to differ slightly between two runs with the same input." | yes; `L293 contains Q1: True` | 24 (24) | 293 | 293, under h2 `is-it-random` (line 287) |
| Q1′ | `corpus/lessons/round-42.md:24-27` | the same sentence | yes | 24 (24) | 293 | 293 |
| Q2 | `corpus/knowledge/pit-outcome-vocabulary.md:28-30` | "a mutant may be detected as timed out on one run, but killed or surviving on another" | yes, across the line break; `L298+299 joined contains Q2: True` (`L298 alone: False`) | 17 (17) | 298–299, §Timeouts | 298–299, under h3 `timeouts` (line 295) |

The quote-free S156 claims checked out as follows:

- `pit-outcome-vocabulary.md:27-28` and `round-42.md:41` (E2) both say "The FAQ names two factors, timeouts and static initializers". The source supports this at line 293 and at the h3 headings on lines 295 and 301.
- `pit-outcome-vocabulary.md:55`, "S156 adds a reason for the lane's choice: a timeout verdict depends on machine load", is a paraphrase, not a quote. The source says "external factors (other processes on the machine etc)" (line 298). "Machine load" is a fair, slightly narrower reading; it is unquoted, so the word and line rules do not apply.
- `round-42.md:58`: "`staged:S156` (arXiv 2406.09843) is a package id and is not the lane's S156". This is correctly kept apart from the lane's S156, and the lesson attributes no quote to it.
- `corpus/knowledge/r42-attribute-and-outflag-destinations.md` attributes nothing to S156. `rg -n -i 'faq|S156|deterministic|timed out|random'` returns rc=1, which matches a used-by cell that does not list that file.

## Verdict

SURVIVES. The snapshot matches the live page, the row is well-formed and validates, and all three S156 quotes
(Q1 twice, Q2 once) are verbatim, within 25 words and correctly located. The only notes are the two observations
in F2 (used-by omits the lesson; the Gate quote grounds only the first teaches clause), and neither breaks the contract.
