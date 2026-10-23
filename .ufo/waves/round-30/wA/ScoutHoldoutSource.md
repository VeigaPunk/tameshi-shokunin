# ScoutHoldoutSource — sealed holdout, one opened paper

Seat: TameshiR30A2.ScoutHoldoutSource-7. Axes named: source fidelity, row-contract fit, what a sealed hash does and does not buy, report completeness. No tools installed. No lane file except this report was written. No gate was run. The Science publisher page was not opened.

## Verdict

The opened primary source is Dwork, Feldman, Hardt, Pitassi, Reingold, and Roth, "Preserving Statistical Validity in Adaptive Data Analysis", arXiv:1411.2664v3 (2 Mar 2016), PDF https://arxiv.org/pdf/1411.2664, sha256 `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697`, fetched 2026-10-23T05:56:18Z. It is the technical paper the same authors point to from their Science landing note. It teaches that a test set hidden from submitters still overfits once scores come back and new candidates are sent, and that the final comparison uses a second, unused test. A hash sealed before scoring commits the bytes. It does not, by itself, stop that reuse. Draft row S094 is below. It was not appended to `corpus/SOURCES.md`.

## Evidence

### What was opened

Command: `curl -fsSL --max-time 60 -A 'Mozilla/5.0 (research; ordinary fetch)' -o /tmp/holdout-src/1411.2664.pdf https://arxiv.org/pdf/1411.2664 && sha256sum /tmp/holdout-src/1411.2664.pdf`

Observed: file mtime `2026-10-23T05:56:18Z`, sha256 `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697`, 322643 bytes. `pdfinfo`: 29 pages, CreationDate Wed Mar 2 23:49:08 2016 -03. The abs page `https://arxiv.org/abs/1411.2664` (HTTP 200, response date `Fri, 23 Oct 2026 05:55:32 GMT`) says v3 is Wed, 2 Mar 2016, comments "Updated related work with recent developments", submitted 10 Nov 2014. The PDF's own first page is labeled `arXiv:1411.2664v3 [cs.LG] 2 Mar 2016`.

### Quote (17 words)

Printed page 2, §1 Introduction, the sentence after "Each submitted model is":

> Each submitted model is evaluated on a (fixed) test set that is available only to the organizers.

`pdftotext -f 2 -l 2 -layout` of the fetched PDF contains that sentence with the line break after "model is" and the period after "organizers". Word count 17 after dropping the period. Same page, two sentences above (20 words): "Such abuse of the holdout set is well known to result in significant overfitting to the holdout or cross-validation set". Same page, the next sentences: scores are returned, a new model can be submitted, and the best entries are then scored on "an additional, hitherto unused, test set", whose comparison with the reused test "frequently reveals significant overfitting to the reused test set".

Same page, earlier: validity theory "assumes a fixed procedure to be performed, selected before the data are gathered", and preregistration is "defining the entire data-collection and data-analysis protocol ahead of time".

### What that teaches about a hash sealed before data

Observed, from printed page 2 only:

- A procedure that the validity theory will stand behind is selected before the data are gathered. Preregistration writes the protocol down ahead of time.
- Hiding the test set is not enough. In the Kaggle setup the test is fixed and "available only to the organizers", and overfitting still shows up because each score is handed back and a new model is submitted against that same set.
- The check that is not on the reused set is a second test that has not been used yet.

[INFERENCE] Committing the sha256 of a sealed set before any candidate runs is a way to show those bytes were fixed before the candidate and before any score. That matches "selected before the data" for the set's contents, and it matches "available only to the organizers" only while nobody reads the items. It does not match the rest of the page. The Kaggle test was already fixed and hidden, and the overfitting came from the scores. A sealed hash stops the set from being rewritten after the fact. It does not stop a later candidate from being rewritten to those scores. The paper's answer to that channel is a fresh unused holdout, or an analysis that limits what the scores reveal. This PDF does not mention a hash.

### Not opened

`curl -sI -L https://doi.org/10.1126/science.aaa9375` followed to `https://www.science.org/doi/10.1126/science.aaa9375` and returned `HTTP/2 403` with `cf-mitigated: challenge` (response date `Fri, 23 Oct 2026 05:55:32 GMT`). That is the Science 349(6248) page named in the task. It was not fetched further. No challenge was passed.

The author note `https://www.cis.upenn.edu/~aaroth/reusable.html` returned HTTP 200, `Last-Modified: Mon, 18 Apr 2016 15:28:19 GMT`, 3001 bytes. It reprints an abstract and calls this arXiv paper the technical companion (`statisticalvalidity.html`, "In STOC 2015"). The note is not the source of the quote above. The quote was taken from the PDF.

This PDF's own bibliography names the Science article as Dwork et al., Science 349(6248):636–638, 2015. That citation was not re-opened.

## Draft row for S094

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 86–108 (v1). Eleven cells, no `|` inside a cell. Checked in `/tmp`: `split` on `|` gives 13 fields (awk `NF=13`). `kind` paper, `tier` A, `status` queued, `used-by` `—`. `queued` because nothing cites S094 yet. Do not mark `mined` until a lesson or knowledge path cites it, and log that change.

S094 is the id this seat was given. S093 is the id given to ScoutBwrapSource in `.ufo/waves/round-30/spec-wA.json`, not a free id for this row. The working-tree footer `corpus/SOURCES.md` line 361 still says `Next unused id: S093` because neither draft has been appended. Append S093 and S094 together, then one new footer line `Next unused id: S095`. Do not edit older footer lines. Do not append this row from this seat.

```
| S094 | Preserving Statistical Validity in Adaptive Data Analysis (Dwork, Feldman, Hardt, Pitassi, Reingold, Roth; arXiv:1411.2664v3) — https://arxiv.org/pdf/1411.2664 | paper | A | a holdout kept from the candidate, and why scores on a fixed holdout still overfit it | §1 Introduction, printed page 2, sentence beginning Each submitted model is @ arXiv:1411.2664v3 (2 Mar 2016), PDF sha256 6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697, fetched 2026-10-23 | a test set withheld from submitters still overfits once scores are returned and models are resubmitted; the final comparison uses a second hitherto unused test, so a hash sealed before scoring fixes the bytes and does not by itself stop that reuse | queued | 2026-10-23 | 730d | — |
```

## Unknowns

- The Science typeset article was not read. Whether its wording differs from printed page 2 of this PDF is unchecked.
- STOC 2015 proceedings pages were not opened. The "STOC 2015" label is the author note's, not a line on the PDF's first page.
- arXiv:1506.02629 was downloaded (sha256 `dcfbb9aa401c62949123be2d74787c4f9cca48597f18860760ef1580ddb4bc71`) and not used. One source was the task.
