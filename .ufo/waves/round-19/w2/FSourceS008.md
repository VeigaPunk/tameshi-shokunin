# FSourceS008: falsification of w1/SourceS008.md (round 19 w2, advisory, 2026-10-21)

Target sha256 `4098f770…6f60` (= completion1.json; byte-identical at 55e1d31; mtime 02:51:11-03:00; landed eedbc95).
Read-only git show/log/diff/grep (GIT_* unset) + arXiv reader; no ruler/selftest run, no installs. Axes: source fidelity · revision attribution · C1 R18-2 status.

## Strongest material assertion
"Observed internal mismatch": case :1 labels S008 "queued"/"not yet a mined row", while SOURCES.md:19 says
`mined` with that note in `used-by`. This is the report's only repository-state claim, and it is C1 item R18-2
(verifier §5 item 2). The report pins no revision.

## Verdict: AGREE on the bytes; DISAGREE as the current state at 55e1d312c4e8ac67aefad80099bd27581ff805c9
1. Line 1 holds `**queued**` + "not yet a mined row" at 7243e7f, 4b7c682 and 55e1d31. The SOURCES.md:19 S008 row
   is byte-identical at all three. `git diff --numstat 7243e7f 55e1d31 -- corpus/SOURCES.md` = `12 4`
   (S049/S063/S077/S078 rows plus an S049 note; no S008 change).
2. At 55e1d31 the case file has `## Erratum R18-2 — source metadata (2026-10-21, round 19)` (:266):
   "This correction explicitly supersedes line 1's S008 `queued` / `not yet a mined row` description."
   (:268-269). A sweep addendum (:278-282) calls "line 1 and line 215" historical.
3. Commit times (-03:00): the freeze 78b99dd at 02:28:10 has 0 R18-2 markers; 21e7932 at 02:48:27 adds the erratum;
   the report was written at 02:51:11; 7af123b at 02:58:18 adds the addendum. The report omits an erratum
   committed about 3 minutes before it was written.
4. Line 1 is retained by design. measure.py@55e1d31:164 requires `**queued**` before the erratum. QUALITY 37
   (QUALITY.md:334-337 @55e1d31) lets a draft line "remain byte-identical only when a dated, explicitly
   superseding erratum gives its effective value".
Overlooked: (a) Erratum R18-2; (b) a second stale status at case :215 ("S008 is `queued` with `used-by —`"),
caught by MetadataDraft (round-19.md:130) and covered at 7af123b. No uncovered S008 status mention remains at
55e1d31 (S008/queued hits :1 :76 :215 :228 :256 :266-281; :76, :228 and :256 are currently true).

## Reproduced arithmetic (my own read-only code; measure.py not executed)
Python mirrors measure.py@55e1d31:149-164 on `git show REV:path` blobs (CASE, SOURCES, source-round18-final.txt).
It checks 12 terms: erratum present; S008 row has 13 parts in both blobs; pin sha; cells 1-7 and 9 equal the pin;
status mined; opened 2026-10-19; CASE in used-by; note has `line 1`, REV18 and `mined`; `**queued**` kept.
7243e7f open · 78b99dd open · 21e7932/7af123b open (no pinned snapshot yet) · 55e1d31 corrected, 12/12.
Snapshot sha256 `018ee9a8…4e0e` = SOURCE_PINS[SOURCE_AFTER] = sha256(4b7c682:corpus/SOURCES.md).
measure.py@55e1d31 sha256 is `bb651eef…5053`. Quote word count: 18, confirmed.

## Source fit and recommendation: AGREE
Re-opened arxiv.org/abs/2102.11378 and …v2 on 2026-10-21 (arXiv API): same title, authors and abstract; v2
reports `2102.11378v2`. The report's quote matches Abstract item (1) word for word, except the source's ";" is
rendered "." (minor). Items (1)-(3) and "more than 24,000 developers on more than 1,000 projects" support the S008
teaches cell. The build agrees with rejecting S008 as C1 closure evidence: measure.py has no URL/arXiv term, and
round-19.md @55e1d31 cites S008 only as registry/metadata state (:18 :19 :51 :118 :130 :212), never as paper
text. `git grep -e 2102.11378 -e SourceS008 55e1d31 -- corpus .ufo/evidence/round-19` hits only
registry/snapshot/case/lesson rows.

## Concrete falsifier
`git show 55e1d312…:corpus/knowledge/mutation-case-kumitate-sources-check.md | sed -n 266,282p` prints the erratum
and addendum, and all 12 R18-2 terms reproduce true. The report's mismatch would be an open R18-2 defect only if
that blob lacked `## Erratum R18-2`, or its note lacked `line 1`/REV18/`mined`, or the S008 row diverged from
the pin. None of these holds at 55e1d31; the erratum is absent only at 7243e7f and 78b99dd.

## Residual unknowns
- U1: whether the seat read the case file before 21e7932 landed. Only the mtime is known; the report gives no revision.
- I1 [INFERENCE from measure.py@55e1d31:149-164, not probed]: no R18-2 term references :215 or the addendum, so
  deleting the addendum would leave R18-2 `corrected`. Outside routed §5 item 2 (line 1 only), so no C1 count change;
  QUALITY 37's "never leave a second current-result implication" is enforced here by prose only.
- I2 [INFERENCE]: :164 accepts only the append remedy, though §5 item 2 also allowed "Sweep the metadata mention".
  A sweep-only fix would read open. That is conservative and cannot inflate 5/5.
- Post-freeze working tree, not evaluated: measure.py is dirty (sha `3f19a16b…590f`, +39/−9, uncommitted).
  Its R18-2 hunk adds "This correction explicitly supersedes line 1's", which is present at case :268, so the
  verdict is unchanged; it still has no :215 term. The full paper body was not re-opened.
