# Scout findings — mutation-score-semantics-cjk.md (staged:S163/S164/S165)

Task: evaluate staged entry
`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/mutation-score-semantics-cjk.md`
for adoption — re-open the three cited sources, verify quotes, and decide
whether the entry adds ground the lane does not already hold.

All three fetches ran `curl -fsSL -m 60`; snapshots are retained under
`/tmp/tameshi-r42-ScoutCjkEntry-src/` (sha256 + byte size below). No tool
installs were made: `pdftotext` (poppler 26.08.0) already present at
`/usr/bin/pdftotext`.

## S163 — huaweicloud CodeArts TestPlan page

- URL: `https://support.huaweicloud.com/usermanual-testman/cloudtest_01_7006.html`
- Reachable: **yes** (`curl -fsSL` exit 0)
- sha256: `badf0929a2cb22d1bc8bd494bbf37f580f9cb2d1d0951d5a09662db6b0ee6968`
- Size: 98614 bytes
- Claim located: **yes** — all three report-item formulas present verbatim in
  fetched HTML (`grep -o` hits, one instance each):
  - `用例通过率=成功数/总数`
  - `用例有效性比例=发现缺陷的测试执行用例数量/测试执行用例数量`
  - `用例执行率 = 计划内执行有执行结果的用例数量/计划内所有用例数量`
- Recheck string from the entry: `grep -c '用例通过率'` → `1` (non-zero, matches).

## S164 — nju GIST hosted PDF (进化变异测试 slides)

- URL: `https://gist.nju.edu.cn/csbse15/doc/%E8%BF%9B%E5%8C%96%E5%8F%98%E5%BC%82%E6%B5%8B%E8%AF%95.pdf`
- Reachable: **yes**
- sha256: `e59a69985f48edbe25bc1240cbab5b58f3857e928c0eaa8a08fbb52846c42389`
- Size: 2078268 bytes
- Claim located: **yes** — extracted text (`pdftotext -layout`, line 98):
  - `变异得分=被杀死的变异体个数/非等价变异体个数`
  - Surrounding three-class definition also located (lines 90–96): killed =
    "如果存在某个测试用例，能够从输出结果上区分原程序和变异体，称该变异体是被杀死的";
    alive = "暂时没被杀死的变异体，称为活着的变异体"; equivalent = "任何测试用例都不能杀死的变异体，称为等价变异体"

## S165 — dfcfw hosted PDF (大语言模型时代的变异分析 deck)

- URL: `https://pdf.dfcfw.com/pdf/H3_AP202503221646031757_1.pdf`
- Reachable: **yes**
- sha256: `531abe11d23f2e3703925a98fabd52ade3793832c1959149d1a8fb8d7d5bd161`
- Size: 5409054 bytes
- Claim located: **yes** — extracted text (`pdftotext -layout`, lines 183–194):
  - `挑战3：等价变异体` (line 183)
  - `等价变异体：变异后的程序与原始程序在功能上完全相同，即它们对所有可能的输入产生相同的输出` (line 185)
  - `影响变异分数计算的精确度` (line 192)
  - `判断等价变异体是不可判定问题：不存在一个自动算法完美解决` (line 194)

## Does the entry add ground the lane does not hold?

The lane's held S001 entry (`corpus/knowledge/mutation-score-semantics.md`)
grounds score = detected/valid on five English/code sources: Stryker docs
(S001), the mutation-testing-elements report schema (S002), cargo-mutants
(S004), mutmut (S005), shmutant (S006). It holds **no** Chinese-source ground,
and **no** vendor-documentation ground.

The staged entry adds ground the lane does not hold:

1. **Cross-literature confirmation of the denominator shape.** S164 (Chinese
   academic definition) states 变异得分 = killed / non-equivalent — the same
   exclude-by-construction shape as Stryker's `detected/valid` (compile/runtime
   errors excluded) and Tameshi's `k/(k+s)`. This is the first non-English
   ground the lane would hold; the entry itself notes the two vocabularies are
   not yet measured for divergence.
2. **LLM-era framing (S165).** Equivalence is undecidable in general and
   erodes score precision — a stated cross-channel agreement with the lane's
   held S156 (LLM-equivalence entry), cited by the entry.
3. **Vendor report-interop precedent (S163).** A Chinese cloud vendor publishes
   every report item with its denominator as a formula — directly relevant to
   the lane's F1 question (report interoperability discipline), which no held
   source demonstrates.

The entry adds **no** new measurement or method authority: S164 (workshop
handout) and S165 (speaker deck) are tier B; S163 is tier A only for its own
product's metric definitions — both boundaries are disclosed in the entry's
"Boundary of this entry" section, and it explicitly states the lane's F1
interop measurement remains open (the specifiable S159×S164 fixture test is
not claimed as run).

## Verdict: **admit**

Reason: all three cited sources re-open (curl exit 0), every quoted claim is
located verbatim in the fetched snapshots (formulas for S163/S164, equivalence
+ undecidability statements for S165), and the entry adds ground the lane does
not hold — a Chinese academic statement of the denominator-exclusion semantics,
an LLM-era equivalence framing, and a vendor-documentation precedent for
publishing report denominators (all absent from held S001/S002/S004/S005/S006).
The entry's own boundary disclosures (tier B for S164/S165; S163 limited to
its own product metrics; no measurement claimed) are accurate against the
reopened sources.

Flip condition: refuse if (a) any later recheck finds one of the three quotes
absent from a live source (currently all located), or (b) the lane adopts a
scoring contract that counts equivalent mutants in the denominator — the CJK
formulation would then contradict, not parallel, the held semantics, and the
entry would misstate the agreement.

## Could not check

- Whether the lane's own scores diverge between S164's three-class and the
  held semantics: the entry does not claim this measurement, and none was run
  here (out of scope for a scout; the entry records it as open).
- S163's exact page/HTML line numbers in the source's own navigation: the
  formulas are confirmed present in the fetched body; the §测试报告总览 section
  header itself was not separately located in the HTML text.
