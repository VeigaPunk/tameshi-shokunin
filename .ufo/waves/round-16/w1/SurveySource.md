# SurveySource — Papadakis et al., "Mutation Testing Advances: An Analysis and Survey" (round 16, w1)

Seat: TameshiR16.SurveySource. Target: open copy of the survey; quote on equivalent mutants / mutant selection; draft SOURCES row. Access date: 2026-10-20 (UTC, from `date -u`).

## Result

- **Open copy found and opened: yes — but it is the Dec-2017 author preprint, not the published Advances in Computers chapter.** The published full text was not reachable (ScienceDirect HTTP 403; DOI resolves to linkinghub.elsevier.com with no open PDF).
- Three URLs return the **same bytes** (sha256 `63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023`, 1,129,278 bytes, 153 pages). The UCL record labels it "Accepted Version" but the file is the LaTeX preprint (`Preprint submitted to Journal of LATEX Templates, December 14, 2017`, page 1).
- Quotes below are therefore **preprint text**. They are not verified against the published chapter. Wording may differ in the published version.
- No fabricated quotes. All quotes are copied from `pdftotext -layout` output and were re-matched by script.

## Evidence (commands, exits, key lines)

1. Search: `web_search` "Mutation Testing Advances: An Analysis and Survey" Papadakis … pdf → 8 hits. Open-copy hits: `https://mpapad.github.io/publications/pdfs/MutationSurvey2019.pdf` (author page), `https://mutationtesting.uni.lu/survey.pdf` (group page), `https://discovery.ucl.ac.uk/id/eprint/10056704` (UCL record). Paywalled/not opened: dl.acm.org, ieeexplore, sciencedirect. Non-PDF: researchgate.
2. `curl -sSL -o mpapad.pdf https://mpapad.github.io/publications/pdfs/MutationSurvey2019.pdf` → http=200, 1129278 bytes.
   `curl -sSL -o uni-lu.pdf https://mutationtesting.uni.lu/survey.pdf` → http=200, 1129278 bytes; sha256 identical to mpapad.pdf.
   `curl -sSL -o ucl-accepted.pdf https://discovery.ucl.ac.uk/id/eprint/10056704/1/survey.pdf` → http=200, 1129278 bytes; sha256 identical. UCL metadata: `Advances in Computers, 112, pp. 275-378 (2019)`, DOI `10.1016/bs.adcom.2018.03.015`, `oa_status: green`, file "Accepted Version", note "author accepted manuscript".
3. `pdfinfo mpapad.pdf`: Creator "LaTeX with hyperref package", CreationDate Thu Dec 14 2017, Pages 153. `pdftotext -layout` → survey.txt (5,750 lines; 154 form-feed pages).
4. Publisher probes: `curl … https://www.sciencedirect.com/science/article/pii/S0065245818300305` → **HTTP 403** (1.2 MB challenge body, no article). `curl https://doi.org/10.1016/bs.adcom.2018.03.015` → 200, redirects to linkinghub.elsevier.com (no PDF link). `curl https://www.semanticscholar.org/paper/d461ab9482b7fb5eadd7e6cd2c6dffced8ede8b8` → HTTP 202, empty body (unusable).
5. Page mapping by script (form-feed split): quotes below map to the same PDF page index and printed page number in both the mpapad and UCL copies (identical bytes).
6. Reference [28] (cited for "undecidable"): `L. Madeyski, W. Orzeszyna, R. Torkar, M. Jozala, Overcoming the equivalent mutant problem: A systematic literature review and a comparative experiment of second order mutation, IEEE Trans. Software Eng. 40 (1)…` (entry truncated in extraction; year not observed).

## Quotes (exact; preprint text; pdftotext-normalised, line-wraps joined)

- **Q1** — §5.3.1 "Identifying Equivalent Mutants", p. 29 (preprint printed p. = PDF p. 29): "Detecting equivalent mutants is a well-known undecidable problem" (8 words; the survey adds the citation [28], Madeyski et al.).
- **Q2** — same paragraph, p. 29: "The best we can do is to form heuristics that can remove most of these mutants." (16 words)
- **Q3** — §5.1 "Mutant Selection (Step 1.)", p. 19: "Therefore, in practice it might be important to select representative subsets of them." (13 words)
- **Q4** — §5.1 "Mutant Reduction Strategies", p. 23 (attributes to Gopinath et al. [113]): "a small constant number of randomly selected mutants is capable of providing statistically similar results" (15 words)
- **Q5** — same section, p. 24 (attributes to Zhang et al. [112]): "there are no significant differences between the two approaches" (9 words; the approaches are random mutant selection vs selective mutation)
- **Q6** — §5.3.1, p. 29 (TCE claim, attributed to [37,152]): "Empirical results suggest TCE is surprisingly effective, being able to identify at least 30% of all the equivalent mutants." (19 words)

Also noted (not quoted): the survey states that random sampling and selective mutation using more than 20% of mutants achieve almost the same results as the full set (pp. 25, citing [17,125]), and that Kurtz et al. [122] found reduction approaches "perform poorly when evaluated against subsuming mutants" (p. 25).

## Draft SOURCES row (NOT written — SOURCES.md is not owned by this seat)

| Field | Value |
|---|---|
| Citation | Papadakis M, Kintis M, Zhang J, Jia Y, Le Traon Y, Harman M. Mutation Testing Advances: An Analysis and Survey. *Advances in Computers* 112 (2019) 275–378. DOI 10.1016/bs.adcom.2018.03.015 |
| Open copy used | https://discovery.ucl.ac.uk/id/eprint/10056704/1/survey.pdf (byte-identical to https://mpapad.github.io/publications/pdfs/MutationSurvey2019.pdf and https://mutationtesting.uni.lu/survey.pdf) |
| Accessed | 2026-10-20 |
| Sha256 of opened file | 63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023 |
| Version status | **Preprint** (LaTeX, "Preprint submitted … December 14, 2017"). Labelled "Accepted Version" by UCL but bytes match the preprint. Published text NOT reached (publisher 403). |
| Sections used | §5.1 (pp. 19, 23–24); §5.3.1 (p. 29) |
| Quotes usable | Q1–Q6 above, with the preprint caveat |
| Reliability | Secondary survey; for the undecidability claim it cites Madeyski et al. [28] — cite that primary source if the claim is used |

## Disposition

- **Accepted as a LEAD and as background only** (status: open-copy-preprint). It is not the published text, so it cannot be cited as the published chapter's wording without a caveat.
- Not accepted as evidence for any C1 prediction. §13 of corpus/knowledge/arm-class-matrix.md was not read by this seat (out of scope); if L1 needs the survey to support a prediction, it can use only the framing in Q1–Q5.

## Recommendations (bounded)

1. SOURCES row: record the open copy as the **preprint** with the sha256 above; mark the published-version check as unreached. Do not write "published chapter" wording from this copy.
2. If the published wording matters for a verdict: request institutional access (UCL or Luxembourg library proxy) to the Elsevier PDF, then re-run the quote check against it. This seat did not attempt proxy access.
3. For equivalent-mutant undecidability, cite Madeyski et al. (the primary source the survey cites as [28]), not only the survey.
4. Q4/Q5 are secondary restatements of Gopinath et al. [113,121] and Zhang et al. [112]. Use the primary sources if a number or conclusion is load-bearing.

## Tooling

- No installs or upgrades. `pdftotext`/`pdfinfo` (poppler), `python3`, `curl`, `sha256sum` were already present on the host. No pacman transactions (host-wide pause respected).

## Opened (URLs / paths)

- https://mpapad.github.io/publications/pdfs/MutationSurvey2019.pdf (opened, 200)
- https://mutationtesting.uni.lu/survey.pdf (opened, 200, identical bytes)
- https://discovery.ucl.ac.uk/id/eprint/10056704 (opened, record)
- https://discovery.ucl.ac.uk/id/eprint/10056704/1/survey.pdf (opened, 200, identical bytes)
- https://www.sciencedirect.com/science/article/pii/S0065245818300305 (HTTP 403)
- https://www.sciencedirect.com/science/article/abs/pii/S0065245818300305 (HTTP 403)
- https://doi.org/10.1016/bs.adcom.2018.03.015 (redirect to linkinghub; no PDF)
- https://www.semanticscholar.org/paper/d461ab9482b7fb5eadd7e6cd2c6dffced8ede8b8 (HTTP 202, empty)
- https://mutation-testing.org/ (unrelated Major framework page; read, not used)
- Scratch: /tmp/tameshi-r16-SurveySource-scratch/ (mpapad.pdf, uni-lu.pdf, ucl-accepted.pdf, survey.txt, ucl.txt)

## Search log (for the record)

- Query: `"Mutation Testing Advances: An Analysis and Survey" Papadakis Kintis Zhang Jia Le Traon Harman pdf` → identified 8 hits; screened 8 by title/URL; opened 3 PDF URLs (identical bytes) and the UCL record; included 1 distinct content (preprint). Rejected for access: ScienceDirect (403), Semantic Scholar (202).
- Second query (published volume/DOI) → identified 6 hits; confirmed volume/pages/DOI via UCL record and listings. Included: none as content.

## Findings / limits

- The published chapter's text was NOT observed. Everything quoted is preprint text.
- The "Accepted Version" label on UCL is inaccurate with respect to the bytes (the file is the Dec-2017 preprint). Report this to whoever curates SOURCES.
- Exit codes: all curl calls returned 0 with HTTP codes as listed above; sha256 match confirmed by `sha256sum`; pdftotext conversion succeeded.
