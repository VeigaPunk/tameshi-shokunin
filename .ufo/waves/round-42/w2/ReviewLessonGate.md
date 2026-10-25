# ReviewLessonGate — round 42 wave 2 (FALSIFY)

Seat: `L1Tameshi42.ReviewLessonGate` (leaf, read-only). Access date 2026-10-25.
Attacked: `## Gate` of `corpus/lessons/round-42.md` (lines 6–107). The working copy is byte-identical
to the tip `a21845f523b75adbd3e3f7a62af91294db224ad9`
(`git show a21845f…:corpus/lessons/round-42.md | diff - corpus/lessons/round-42.md` → no output).
No counter was run. No tools were installed. The scratch dir `/tmp/tameshi-r42w2-ReviewLessonGate-zenn/` has been deleted.

## Survived

1. **Japanese quote drift claim is true** (lesson `:51-52`).
   - `curl -fsSL -m 60 'https://zenn.dev/seckeyjp/articles/j-six-mutation-testing' -o zenn.html` → exit 0, 171806 B, sha256 `2b2ff78eb71b221f7ff1b1ef24c91211df01f33beef95c673b93d0629b3c5d1f`.
   - `grep -o 'テストの穴とは当たりません' zenn.html | wc -l` → `0`. `grep -o '当たりません' zenn.html | wc -l` → `0`.
   - `grep -o 'テストの穴とは限りません' zenn.html | wc -l` → `2`. Context: `生き残ったミュータントがすべてテストの穴とは限りません。` appears twice.
   - The staged text really carries 当たりません: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/survivor-classification.md:13-14` reads `"生き残ったミュータントがすべてテストの穴とは当たり` followed by `ません"`.
   - The recheck count claim (`:54`) also holds: `grep -c '168 killed' zenn.html` → `2`.
   - Side note: three same-size fetches gave three different digests (ScoutSurvivorEntry `a6bcc4ec…`, ReviewSurvivorGate `1688b8a1…`, mine `2b2ff78e…`). That backs the lesson's flip condition, which says to re-quote from a *committed* snapshot.

2. **Renumber map, by document, is correct** (lesson `:75-76`).
   - The package's `SOURCES.append.md:13` lists `S159` as https://pitest.org/quickstart/basic_concepts/, and `:14` lists `S160` as https://pitest.org/faq/.
   - At the tip, `git show a21845f…:corpus/SOURCES.md | grep -n '^| S15[5-8] '` gives:
     - `:125` S155 = basic_concepts
     - `:126` S156 = faq
     - `:127` S157 = argparse (new)
     - `:128` S158 = DetectionStatus.java @ f7fe5adf… (new)
   - Package `SOURCES.append.md:10` `S156` = arXiv 2406.09843, so lesson `:58` ("not the lane's S156") is right.
   - Counts match. `staged-ids` has 103 lines, `reg-ids` has 109, `assimilation/collisions` = `S153 S154`, `guard/collisions` = `S153 S154 S159` (three) and `guard/collisions-col0` = `S153 S154` (two). This matches `:69-74`.

3. **Admit is consistent with `w1/ReviewPitEntry.md:8` (ADMIT-WITH-EDITS)**, and all five edit or obligation items have landed at the tip:
   - **E1** (timeout is Inconclusive, not a kill): `pit-outcome-vocabulary.md:50-52` cites `SKILL.md:208-212`, and `SKILL.md:208-212` at the tip is the Inconclusive / kill-rate rule.
   - **E2** (two factors): `pit-outcome-vocabulary.md:28` says "two factors, timeouts and static initializers".
   - **E3** (lane anchors): `:35` and `:51-52` carry them.
   - **E4** (committed snapshots): `git ls-tree a21845f… .ufo/evidence/round-42/sources/` lists five snapshots plus `sha256.txt`, with digests equal to lesson `:20,25,31,36`. ReviewPitEntry called this "criterion 9"; the lesson's "criterion 79" also exists (`corpus/QUALITY.md:944`).
   - **E5** (README coverage row): `corpus/README.md:530` has the coverage row for `knowledge/pit-outcome-vocabulary.md`.
   - The located quotes match the committed snapshots at the cited lines: basic-concepts `:175`, `:179`, `:192`; faq `:293`; DetectionStatus `:63` `RUN_ERROR(true),`, `:78`, `:108`, 2988 B; stryker `:26` "It is not represented in your mutation score."

4. **Refusal is consistent with `w1/ReviewSurvivorGate.md:9` (REFUSE as submitted).** `w1/ScoutSurvivorEntry.md:44` said "ADMIT, with one flip condition": fix the drifted quote and fix the recheck. Neither fix was made, so that admit never took effect. The refusal is correct.

5. **Deferral is consistent with the gate verdicts.** Both CJK gates said admit (`w1/ScoutCjkEntry.md` "Verdict: admit"; `w1/ReviewCjkGate.md:8` "ADMIT"). The lesson records it as "not adopted", not as a refusal (`:60-64`). The contract requires only ">=1 admit and >=1 reject" (`contract.json:60`), so not adopting it is allowed.

6. **Every backticked path resolves at the tip, with one convention to note.** Command:
   `sed -n '6,107p' corpus/lessons/round-42.md | grep -o '`[^`]*`' | tr -d '`' | sort -u` → `git cat-file -e a21845f…:<path>`.
   - These resolve as written: all `.ufo/...` paths, `corpus/README.md`, `corpus/knowledge/oracle-anchored-survivors.md`, `corpus/knowledge/pit-outcome-vocabulary.md`, `PROVINCE.md`, `SKILL.md`, `considerthese/2026-10-24.md`, `reports/round-1-calibration.md`, and `.ufo/evidence/round-21/coldread/measure.py`.
   - These resolve under the stated prefix:
     - The bare `ScribeRows.md`, `ReviewPitEntry.md`, `CriticOracleSource.md` and `ReviewCjkGate.md` resolve under `.ufo/waves/round-42/w1/`.
     - The five bare knowledge names at `:89-92` resolve under `corpus/knowledge/`, which `:92` itself states ("All in `corpus/knowledge/`").
   - `sources-census.sh` (`:77`, `:80`) is a command, not a lane path. It lives at the fleet root, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.
   - `survivor-classification.md` and `mutation-score-semantics-cjk.md` are correctly absent from the lane. They exist only in the package, under `knowledge/corpus/knowledge/`.
   - The remaining tokens are commands, ids, hashes or code literals, not paths.

## Did not survive

1. **[MED] The digest-reproduction claim is overstated** (lesson `:11-15`). The lesson says "the snapshot digests reproduced across four independent wave-1 fetches (`ScoutPitConcepts.md`, `ScribeRows.md`, `ReviewPitEntry.md`, `CriticOracleSource.md`)". Grep for each digest in those four reports at the tip:
   - basic_concepts `c51d8423…`: in 4 of 4 (`git show a21845f…:.ufo/waves/round-42/w1/<f>.md | grep -c c51d8423f5a7` → 1, 2, 1, 1).
   - faq `ccf6ac49…`: in 2 of 4 (ScribeRows, ReviewPitEntry; ScoutPitConcepts and CriticOracleSource both give 0).
   - stryker `ac273386…`: in 1 of 4 (CriticOracleSource).
   - DetectionStatus `3bf295ad…`: in 0 of 4. `git grep -l 3bf295ad5312 a21845f… -- .ufo/waves/round-42/w1/` gives no output, so no wave-1 report reproduces S158's digest. It rests on the L1's own fetch alone.
   - Only the basic_concepts digest reproduced four times. The sentence should be scoped per digest.

2. **[MED] The CJK deferral rationale contradicts the contract.** Lesson `:63-64` says the entry is "a sibling theme" outside "which outcomes count as a kill". But `contract.json:57` lists `knowledge/corpus/knowledge/mutation-score-semantics-cjk.md` as a candidate under this round's single theme (`:53`). The addendum's rule is "ONE theme and 1–3 knowledge entries" (`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:253-254`), so one theme does not stop a second entry from being adopted. The outcome (not adopted) is allowed. The stated reason is not the binding constraint.

3. **[LOW] The CJK flip condition drops a gate's admission condition** (lesson `:65`). `w1/ReviewCjkGate.md:103` makes repair of the dangling `CANNOT-ANSWER.md §3.7` pointer (`:80`) "a condition of admission, not a waiver". The lesson's flip ("re-opens the three sources and snapshots them") omits it. A later round that follows only the lesson would admit an entry with a dangling reference.

4. **[LOW] The refusal's sourcing and flip condition are incomplete** (lesson `:51-57`).
   - Reason (1), the quote drift, comes from `w1/ScoutSurvivorEntry.md:23`, but the lesson cites only `ReviewSurvivorGate.md`. That reviewer actually says the opposite: "S166 quotes are present and located" (`w1/ReviewSurvivorGate.md:70`). The lesson records neither the scout's conditional ADMIT nor this disagreement between the two gates.
   - The lesson's three-part flip condition omits these ReviewSurvivorGate flip items:
     - 1: open renumbered, collision-free rows as mined.
     - 2: a located ≤25-word S156 quote and in-round `verified-at`.
     - 5: the coverage row lands in the same round.
   - The refusal itself still stands.

## Residual risk / gaps

- `corpus/README.md:85` (cited at lesson `:55`) is the F8 frontier row, and it still shows status `open`. The "held" status comes from the later round-27/29 rows, which ReviewSurvivorGate cites at `README.md:418-438`. The citation is weak, but it does not mislead about the duplication.
- I did not re-fetch the PIT, Stryker or GitHub sources. I checked only the committed snapshots.

Verdict: BROKEN: Gate prose overclaims that four wave-1 fetches reproduced every snapshot digest (only basic_concepts did; S158's digest appears in no wave-1 report), and the CJK deferral rationale contradicts contract.json:57. The admit/reject/deferral outcomes, the renumber map, the Japanese drift claim and path resolution all held.
