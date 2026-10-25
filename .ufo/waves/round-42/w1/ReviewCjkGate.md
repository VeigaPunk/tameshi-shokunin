# Review — CJK entry gate: mutation-score-semantics-cjk.md

Reviewer: L1Tameshi42.ReviewCjkGate (leaf; no subagents). Date: 2026-10-25.
Candidate: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/mutation-score-semantics-cjk.md`
(staged, read-only seat — never written). Gate: QUALITY.md, PROVINCE.md, CORPUS rule 4,
and "does it add ground beyond the held `mutation-score-semantics.md`".

## Verdict: ADMIT

Reason: every cited source re-opens and carries the quoted claim verbatim; the
entry adds ground the lane does not hold (Chinese academic denominator
statement; LLM-era equivalence framing; vendor-published denominators); it
satisfies the provenance, tier and falsifiability criteria; it is knowledge,
not rows (CORPUS rule 4).

## Findings

1. **All three sources re-open (curl exit 0) and every quoted claim is located
   verbatim in the fetched snapshot.**
   - S164 (`https://gist.nju.edu.cn/csbse15/doc/%E8%BF%9B%E5%8C%96%E5%8F%98%E5%BC%82%E6%B5%8B%E8%AF%95.pdf`):
     `curl -fsSL -m 60 … -o s164.pdf` → exit 0; snapshot 2 078 268 B, sha256
     `e59a69985f48edbe25bc1240cbab5b58f3857e928c0eaa8a08fbb52846c42389`.
     `pdftotext -layout s164.pdf s164.txt` then
     `grep -n '变异得分=被杀死的变异体个数/非等价变异体个数' s164.txt` → line 98
     exact. Surrounding three-class definition (killed/alive/equivalence) at
     lines 90–96 matches the entry's paraphrase.
   - S163 (`https://support.huaweicloud.com/usermanual-testman/cloudtest_01_7006.html`):
     `curl -fsSL -m 60 … -o s163.html` → exit 0; snapshot 98 614 B, sha256
     `badf0929a2cb22d1bc8bd494bbf37f580f9cb2d1d0951d5a09662db6b0ee6968`.
     `grep -o` finds all three formulas verbatim: `用例通过率=成功数/总数`,
     `用例有效性比例=发现缺陷的测试执行用例数量/测试执行用例数量`,
     `用例执行率 = 计划内执行有执行结果的用例数量/计划内所有用例数量`.
     Recheck string `用例通过率` count = 1 (matches the entry's `recheck:`).
   - S165 (`https://pdf.dfcfw.com/pdf/H3_AP202503221646031757_1.pdf`):
     `curl -fsSL -m 60 … -o s165.pdf` → exit 0; snapshot 5 409 054 B, sha256
     `531abe11d23f2e3703925a98fabd52ade3793832c1959149d1a8fb8d7d5bd161`.
     `pdftotext -layout s165.pdf s165.txt` → lines 183–194 hold
     `挑战3：等价变异体`, `等价变异体：变异后的程序与原始程序在功能上完全相同`,
     `影响变异分数计算的精确度`, `判断等价变异体是不可判定问题：不存在一个自动算法完美解决`.
   Snapshots retained under `/tmp/tameshi-r42-ReviewCjkGate/`.

2. **The entry adds ground beyond the held `corpus/knowledge/mutation-score-semantics.md`.**
   Held S001 entry grounds score = detected/valid on five English/code sources
   (S001 Stryker, S002 report schema, S004 cargo-mutants, S005 mutmut,
   S006 shmutant) plus the six-case recomputation and the rejected timeout-as-kill
   rule. It holds **no** Chinese-source ground and **no** vendor-documentation
   ground. The candidate adds:
   - cross-literature confirmation that the denominator excludes equivalent
     mutants by construction (S164, Chinese academic definition: killed ÷
     non-equivalent — the first non-English ground the lane would hold);
   - LLM-era framing (S165): equivalence is undecidable in general and erodes
     score precision — stated as cross-channel agreement with the staged S156
     English LLM-equivalence entry;
   - vendor report-interop precedent (S163): a cloud vendor publishes every
     report item with its denominator as a formula — relevant to the F1
     report-interop half, which no held source demonstrates.
   The entry adds **no** new measurement or method authority: it explicitly
   states the F1 interop measurement stays open and the specifiable S159×S164
   fixture test is not run. Boundaries disclosed (S164/S165 tier B; S163 tier A
   only for its own product's metrics) are accurate against the reopened sources.

3. **QUALITY bar — satisfied with one required repair (finding 4).**
   - Criterion 10 / CORPUS provenance: entry opens with `source:` (3 rows,
     S163/S164/S165 with URLs + anchors), `verified-at:` 2026-10-23,
     `recheck:` 365d with command. Staged rows S163/S164/S165 were opened
     2026-10-23 in the round that writes them; all are `mined`, tiers A/B —
     no tier-C sole support.
   - Falsifiability: claims are quotes or measured facts with source pointers;
     every inference is marked `Inference:`; the "not run" interop test is
     plainly labeled as not run.
   - CORPUS rule 4: this is a knowledge entry (claims), not a row; it cites
     mined rows on uncovered coverage-map ground (F1 partly held; F9 open).
   - PROVINCE: F1/F9 are frontier; ground moves to Core only through an
     admitted, source-headed `knowledge/` entry citing mined `SOURCES.md`
     rows — this entry structurally qualifies; it is in-province
     (mutation-score semantics = verification-fixture craft).

4. **Required repair before/at adoption: dangling internal reference.**
   The entry's Boundary section says the method-authority gap "is recorded in
   `CANNOT-ANSWER.md` §3.7". No such file exists anywhere in the lane or the
   merge package:
   `find /home/vgpnk/Projects/shokunin/tameshi-shokunin /home/vgpnk/Projects/shokuknow/merge/tameshi -iname '*CANNOT*'`
   → only `.ufo/evidence/round-17/coldread/traces/CR45/12-witness-cannot.json`
   (unrelated); `grep -rn 'CANNOT-ANSWER' corpus/` → no matches. The sentence
   "the gap is recorded" is therefore unverifiable as written (QUALITY 2).
   Fix at adoption: point the sentence at a real record (e.g. the coverage-map
   Known-gaps block or LOG.md debt entry) or delete the pointer. This is a
   peripheral boundary note, not the core claim — hence repair, not refusal.

5. **Not checked.** Whether the lane's own scores diverge between S164's
   three-class and the held Stryker/Tameshi semantics: the entry does not claim
   this measurement, and none was run here (recorded as open in the entry).
   S163's exact section header `§测试报告总览` was not separately located in the
   fetched HTML body; the three formulas themselves are confirmed present.

## Flip conditions (refuse if any becomes true)

- (a) A recheck finds any of the three quoted strings absent from a live
  source (all located 2026-10-25).
- (b) The lane adopts a scoring contract that counts equivalent mutants **in**
  the denominator — the CJK formulation would then contradict, not parallel,
  the held semantics, and the entry would misstate the agreement.
- (c) The finding-4 dangling reference is not repaired at adoption (repair is
  a condition of admission, not a waiver).

## Tooling

No installs made. Used `curl` (present), `pdftotext` (poppler 26.08.0,
`/usr/bin/pdftotext`), `grep`/`find`/`awk`. Snapshots and sha256/sizes in
finding 1 under `/tmp/tameshi-r42-ReviewCjkGate/`.
