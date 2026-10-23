# S094 reopen — fresh-seed holdout rationale

## Verdict

**Applies narrowly.** S094 supports using an unseen, one-time holdout to resist adaptation to previously returned scores. That is a sound methodological rationale for generating fresh must-kill copies at measurement time, hidden from the auditor. It does **not** establish a statistical guarantee for this mutation-audit counter or prove the copies are independent or unpredictable.

## Evidence

- Frozen source: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c31814978969a41a8e9b0f7d99fa308c5993c1b7:corpus/SOURCES.md` returned the S094 row. The staged frozen copy locates it at `corpus/SOURCES.md:103`; its pin is PDF SHA-256 `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697`.
- Exact fetch command: `curl -fL https://arxiv.org/pdf/1411.2664 -o s094.pdf && sha256sum s094.pdf && file s094.pdf`. Observed output: `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697  s094.pdf`; `s094.pdf: PDF document, version 1.4, 29 page(s)`. The downloaded digest matches the registry pin.
- Re-located quote: §1 Introduction, **printed page 2** (PDF page 2): “Each submitted model is evaluated on a (fixed) test set that is available only to the organizers.” The immediately following text says participants receive scores and may submit another model; at the competition's conclusion, entries are evaluated on an “additional, hitherto unused, test set.” The paper reports overfitting when the fixed test set is reused adaptively.
- The frozen counter source is `.ufo/evidence/round-32/c1-measure.py` at the same revision. Its docstring says generated must-kill copies are drawn from a seeded RNG at run time and unknown when the tool is written (lines 17–19); the auditor receives only the copy path, not a label or seed (lines 23–24). The implementation defaults to `secrets.token_hex(8)` when `--seed` is absent and initializes the RNG from it (lines 218–219); it invokes the auditor with `--runner COPY` (lines 177–184). Thus the default run provides the intended hidden, freshly generated cases. `--seed` is an explicit replay option, so freshness is not guaranteed when a caller deliberately reuses a seed.
- Provenance command for the frozen inputs: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c31814978969a41a8e9b0f7d99fa308c5993c1b7:corpus/SOURCES.md > frozen-SOURCES.md && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c31814978969a41a8e9b0f7d99fa308c5993c1b7:.ufo/evidence/round-32/c1-measure.py > frozen-c1-measure.py && wc -l frozen-SOURCES.md frozen-c1-measure.py`. Observed counts: 377 and 281 lines respectively. These were source reads, not executions of the counter.

## Proposed registry change (not applied)

S094 `used-by` old → new:

`corpus/knowledge/regression-tally-completeness.md` → `corpus/knowledge/regression-tally-completeness.md, .ufo/evidence/round-32/c1-measure.py`

Leave S094's status (`mined`), recheck (`730d`), and other cells unchanged. The added backlink is appropriate because the counter implements the held-out-copy design; it does not imply the paper validates the counter.

## Proposed Gate line

`S094 re-opened 2026-10-23: https://arxiv.org/pdf/1411.2664, §1 Introduction, printed p. 2: “Each submitted model is evaluated on a (fixed) test set that is available only to the organizers.” (17 words). The returned-score/resubmission and additional hitherto-unused final-test passages support the holdout rationale; the transfer to generated tally mutations is an analogy, not a result proved by the paper.`

## Gates and limits

No C1 counter, `tally-audit.py`, mutation runner, regression, or acceptance gate was run. This is a source reopen and static read of the frozen counter only; no behavioral result is claimed. The paper studies adaptive data analysis, not mutation-testing fixtures. A fresh default seed limits reuse of the same cases, but the paper does not establish RNG quality, secrecy from every observer, or protection if prior outcomes are exposed and adapted to.

## Touched surfaces and artifacts

- New report: `.ufo/waves/round-32/w1/ReopenS094.md`.
- Scratch-only artifacts: `/fast/scratch/hyaku/tameshi-r32-seats/ReopenS094/s094.pdf`, `frozen-SOURCES.md`, and `frozen-c1-measure.py`.
- No product, source-registry, or knowledge-entry file was edited. No tool was installed or updated.
