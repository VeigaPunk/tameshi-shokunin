# ReopenS058 — live re-open of source row S058

Lane: tameshi-shokunin. Target: `corpus/SOURCES.md:67` (S058) at
`eb7838b16490ca7ba17ea3242ade76a61f744af2`, the lesson quote at
`corpus/lessons/round-17.md:32`, and the used-by file
`corpus/knowledge/input-keyed-coldread-credit.md`.

Claim attacked: S058's lesson quote is verbatim at the stated location and ≤25
words; the row's tier/scope/teaches cells are supported by the live source; the
used-by file exists at the landing rev and actually cites S058.

Work environment (required fleet-mirror clone):
`W=/tmp/tameshi-r17w2-ReopenS058-6LvkGa`, `C=$W/fleet/tameshi-shokunin`,
`git -C $C rev-parse HEAD` → `eb7838b16490ca7ba17ea3242ade76a61f744af2` (exit 0).
Tooling: `pdftotext version 26.08.0` (poppler), `curl`, `python3`, `sha256sum`;
nothing installed or upgraded.

## 1. Live fetch — row anchor digest

Row anchor cell (`corpus/SOURCES.md:67`, field 6): `§4.2.2 Verifying Traces p.
79:14 @ published PDF sha256 d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede, fetched 2026-10-20`.

```
$ curl -sS -o bs.pdf -w '%{http_code} %{size_download}\n' \
    https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf
200 728559                                   # exit 0
$ sha256sum bs.pdf
d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede  bs.pdf   # exit 0
$ file bs.pdf
bs.pdf: PDF document, version 1.5, 29 page(s)
```

Observed: the live URL still serves the PDF, and its sha256 equals the digest
the row records byte-for-byte. No digest drift.

## 2. Lesson quote — verbatim and ≤25 words at the stated location

Lesson row (`corpus/lessons/round-17.md:32`):

> `| S058 | https://.../build-systems-final.pdf | 2026-10-20 | "record the
> values/hashes of dependencies used last time, and if something has changed,
> the key is dirty and must be rebuilt" (§4.2.2 Verifying Traces, p. 79:14) |`

```
$ pdftotext -layout -f 14 -l 15 bs.pdf p14.txt          # exit 0
$ grep -n "4.2.2 Verifying Traces\|record the val\|ues/hashes\|be rebuilt" p14.txt
41:   4.2.2 Verifying Traces. An alternative way to determine if a key is dirty is to record the val-
42:ues/hashes of dependencies used last time, and if something has changed, the key is dirty and must
43:be rebuilt ś in essence a trace which we can use to verify existing values. For traces, there are two
```

Page 14 opens with the running head `79:14` (`p14.txt:1`:
`79:14   Andrey Mokhov, Neil Mitchell, and Simon Peyton Jones`); §4.2.3
Constructive Traces begins on page 15 (`79:15`), so the heading, the quote and
its immediate continuation all sit on **p. 79:14**, exactly as stated.

Normalized check (join `-\n` hyphen wraps, collapse whitespace) over page 14:

```
heading_idx 3432 quote_idx 3512 heading_precedes_quote True
quote_on_p14 True words 21
```

- Verbatim: the quote, after joining the line-break hyphen in `val-` + `ues/hashes`,
  is an exact substring of the page-14 text. The neighbouring separator glyph
  after `rebuilt` extracts as `ś` (U+015B) — outside the quoted span; the
  quoted words themselves are unaffected.
- Length: 21 words ≤ 25.
- Location string matches the page header and section heading text exactly
  (`4.2.2 Verifying Traces`).

## 3. Source-identity cells (source cell metadata)

```
$ curl -sS -o /dev/null -w '%{http_code} %{redirect_url}\n' -I https://doi.org/10.1145/3236774
302 https://dl.acm.org/doi/10.1145/3236774
$ curl -sS -H 'Accept: application/vnd.citationstyles.csl+json' -L https://doi.org/10.1145/3236774 | \
  python3 -c '...'
Build systems à la carte
['Mokhov', 'Mitchell', 'Peyton Jones']
Proceedings of the ACM on Programming Languages 2 ICFP 1-29 {'date-parts': [[2018, 7, 30]]}
```

PDF's own imprint (`p14.txt:39`, also on every odd page):
`Proc. ACM Program. Lang., Vol. 2, No. ICFP, Article 79. Publication date:
September 2018.` → title, authors, PACMPL vol. 2 / ICFP, Article 79 and the
September 2018 date in the row's `source` cell are all supported.

## 4. Tier / scope / teaches cells

Contract in force: `/home/vgpnk/Projects/shokunin/CORPUS.md:86-108` (row shape and
definitions) and `:112-116` (rule 1: ≤25-word quote with location grounding
`teaches`). Census block `:131-151`.

| cell | value (`corpus/SOURCES.md:67`) | support | verdict |
|---|---|---|---|
| kind | `paper` | PDF is a PACMPL/ICFP article; `paper` is in the contract enum (`CORPUS.md:89-90`) | holds |
| tier | `A` | `CORPUS.md:93-97`: A = "primary or authoritative for that scope ... original paper". This row's scope is §4.2.2 of the original published paper; no `community`-to-A inflation (enum census prints nothing) | holds |
| scope | "the verifying-traces rebuilder — how a previously built value is checked against later inputs" | §4.2 is titled "The Rebuilder: Determining Out-of-date Keys" (`bs.txt:671`); §4.2.2 is "Verifying Traces" (`bs.txt:701`), stating traces are used "to verify whether a key needs rebuilding" and "we can use to verify existing values" | holds |
| teaches | "rebuild when a recorded dependency hash differs: a trace of input hashes lets a later build verify an existing value instead of trusting a clean bit" | quote at `p14.txt:41-43`: record values/hashes of dependencies last time; changed ⇒ key dirty and must be rebuilt; trace verifies existing values; §4.2.1 (`bs.txt:676-698`) is the dirty-bit alternative the "instead of" clause contrasts | holds |

Row shape, from the contract census run in the clone:

```
rows: 62                        # exit 0
malformed: 0                    # 11 columns => NF=13; exit 0
S058 rows: 1                    # exit 0
dup ids: (none)                 # uniq -d empty; pipeline exit 1 (no dups)
enum violations: (none)         # tier/status/kind + A/community inflation; exit 0
S058-fields=11                  # awk NR==67; exit 0
```

## 5. Used-by file at the landing rev

```
$ git cat-file -e eb7838b16490ca7ba17ea3242ade76a61f744af2:corpus/knowledge/input-keyed-coldread-credit.md
cat-file-exit=0
$ grep -c "S058" corpus/knowledge/input-keyed-coldread-credit.md
2                               # grep-exit=0
$ grep -n "S058" corpus/knowledge/input-keyed-coldread-credit.md
1:source: S058 — https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf — §4.2.2 Verifying Traces, p. 79:14 (published PDF sha256 d6c175a4…4ede, fetched 2026-10-20); ...
28:This is a verifying trace (S058): record the hashes of what a step used, and
```

Observed: the file exists at the rev as a regular blob, and it cites S058 twice
— in the `source:` line and in the body rule (§2) that the entry exists to
state. This satisfies `status: mined` ("cited by ≥1 path in `used-by`",
`CORPUS.md:103-104`). The contract's mined-used-by existence sweep over the whole
registry printed nothing:

```
$ awk ... corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
```

## 6. Non-blocking observations

- `recheck 730d` is a cadence value; `CORPUS.md:105-106` allows "ISO date or
  cadence (`90d`, `180d`, `on-release`)" and the parenthetical is illustrative
  (S057 already carries `365d`); no census rejects it. Not a support failure.
- The row's `teaches` is a paraphrase, not a quotation; rule 1 puts the ≤25-word
  quote in the round lesson, and there it is (`lessons/round-17.md:32`) and it
  matches the page exactly. The row's own cells are consistent with that quote.
- Extraction artifact only: the text extractor renders the separator after
  `rebuilt` as `ś` (U+015B); it falls outside the quoted span and does not
  affect the quote words.

## Verdict

**Holds** — S058's lesson quote is verbatim at §4.2.2 Verifying Traces p. 79:14
after hyphen-wrap join (21 words), the live PDF still hashes to the row's
recorded `d6c175a4…4ede`, kind/tier/scope/teaches are each supported by the
source, and `corpus/knowledge/input-keyed-coldread-credit.md` exists at
`eb7838b` and cites S058 at lines 1 and 28.
