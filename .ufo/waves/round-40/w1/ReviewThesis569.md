# ReviewThesis569 — r6-snapshot-practice-corpus.md vs the Portuguese 569-project sentence

## Verdict

Attack **does not land** on its named condition — the file does not treat the
Portuguese 569-project sentence as the English quote. But the attack surface is
not clean: the file's disclaimer contains one factual defect and one miscount.

## Primary condition — not met

- `corpus/knowledge/r6-snapshot-practice-corpus.md:10` quotes
  `"drawbacks such as fragility and lack of context can lead to false positives"`,
  which is verbatim English.
- `grep -c "drawbacks such as fragility and lack of context can lead to false positives" .ufo/evidence/round-40/sources/s152-excerpt.txt` → `1` (line 6, byte-exact).
- Live check: `curl -sL https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download` → sha256 `65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703` (matches frontmatter), `pdftotext` shows the quote in the `Abstract` (English) section.
- The Portuguese Resumo's 569 sentence (`...em 569 projetos de código aberto...`) is never quoted or conflated; `:14` explicitly disclaims it.

## Finding 1 (factual defect, medium)

`corpus/knowledge/r6-snapshot-practice-corpus.md:14` —

> "does not adopt the campaign's 569-project sentence (that figure is in the
> Portuguese abstract, not in the English sentence quoted here)"

is wrong about where the figure lives. The English abstract of the same PDF
contains `"comprehensive investigation into the use of snapshot testing in 569
open-source projects by analyzing a random sample of 380 tests"`
(pdftotext output; PDF fetched 2026-10-24, scratch
`/tmp/tameshi-r40-ReviewThesis569/s152.pdf`). The 569 figure is in **both**
abstracts. Moreover, the campaign's own staged copy
(`shokuknow/merge/tameshi/knowledge/corpus/knowledge/r6-snapshot-practice-corpus.md`)
quotes the 569 figure explicitly from `"§Abstract (English), p. viii"`. So the
campaign's 569 sentence was English, not Portuguese: the parenthetical both
misattributes the campaign quote's language and invites a future reader to
dismiss the English `569 open-source projects` sentence as a translation.

## Finding 2 (miscount, minor)

`corpus/knowledge/r6-snapshot-practice-corpus.md:10` — `"The quote is 11 words"`.
The quoted span is 13 words:

```
echo -n "drawbacks such as fragility and lack of context can lead to false positives" | wc -w   # → 13
```

Same miscount repeated at `corpus/lessons/round-40.md:14` and baked into the
wave spec (`spec-w1.json` ScoutS152 item) — likely the L1 propagated the task
text rather than re-counting.

## Verified clean

- Frontmatter sha256 matches the fetched PDF byte-for-byte.
- Committed excerpt matches PDF text modulo de-hyphenation artifacts
  (`fron-tend`→`frontend`), and truncates mid-word (`fo-cus`) **before** the
  569 sentence — so the excerpt neither confirms nor denies the figure's
  English-abstract presence; the fetched PDF is the only ground truth.
- No 569/projetos text anywhere under `.ufo/evidence/round-40/` (scout's
  cross-check reproduced).

## Residual risk / gaps

- The miscount and the "Portuguese abstract" misattribution sit outside the
  frozen C1/C2 predicates; neither flips a counter. Their cost is citation
  hygiene: a corpus page that exists to keep attribution straight now asserts
  where a figure lives and gets it wrong.
- Scope: only this entry's fidelity to S152 was checked; registry/used-by
  correctness is covered by sibling seats.

## Commands run (scratch only, lane untouched)

```
mkdir -p /tmp/tameshi-r40-ReviewThesis569 && cd /tmp/tameshi-r40-ReviewThesis569
curl -sL -o s152.pdf 'https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download'
sha256sum s152.pdf        # 65f9603f… == frontmatter
pdftotext s152.pdf s152-full.txt
grep -n '569' s152-full.txt   # :124 English abstract; :96 Portuguese Resumo
```
