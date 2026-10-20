# ReadmeAppend — round-16 `corpus/README.md` append verification

Seat: `TameshiR16.ReadmeAppend`
Target: `corpus/README.md` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`, baseline `28aeef4`
Scratch: `/tmp/tameshi-r16w2-ReadmeAppend-8ex5JY`
Method: committed bytes only via `git show`; one re-execution of the committed cold-read assembler and of the committed counter (`measure.py`), all writes to scratch. No lane files edited; no tool installs.

**One-line verdict: partial — the case-7 row and every cited line anchor hold; the cold-read supersession at `corpus/README.md:230-233` falls at `c699c8c` because `.ufo/evidence/round-16/coldread/ledger.json` does not exist in the commit or the worktree, and the lane's own counter reports `ledger_present:false`, `sections_covered:0`, `box3_full_page:false`.**

## Statement-by-statement findings

| # | Statement (path:line) | Verdict | Evidence |
|---|---|---|---|
| 1 | Heading: "seventh recorded case" (`README:219`) | **holds** | Exactly seven `corpus/knowledge/mutation-case-*.md` files at the commit; note self-identifies "Mutation case 7" (`mutation-case-kumitate-round-gate.md:5`); `measure.py` at the commit: `recorded_cases = 7`, `depth_score = 7`, `ledger_legs` = the six prior legs + `js-round-gate`. |
| 2 | Heading: "full-page cold-read" (`README:219`) | **falls (at this commit)** | The cited ledger does not exist (§4). A wave-1-only assembly covers the 51-section pre-edit snapshot but has 5 `wrong-expectation` entries; the post-edit page is 54 sections. Full-page, passing coverage is not established at `c699c8c`. |
| 3 | "Appended; rows above keep their line numbers." (`README:221`) | **holds** | `git diff --numstat 28aeef4 c699c8c -- corpus/README.md` → `20	0	corpus/README.md`; `git diff --unified=0` → `@@ -217,0 +218,20 @@` (insertion at EOF only); zero deletion lines; every cited baseline line (15, 47, 49, 143-146, 160, 190, 207) is byte-identical at `28aeef4` and `c699c8c`; 217 → 237 lines. |
| 4 | "QUALITY 7: the new note gets its row in the same round." (`README:221-222`) | **holds** | `corpus/knowledge/mutation-case-kumitate-round-gate.md` and its row are both added by `c699c8c` (`git show --stat c699c8c`); `QUALITY.md:18-20` item 7. |
| 5 | Row 226: "case 7: kumitate `round-gate.mjs` 5/10 (50 %)" | **holds** | `mutation-case-kumitate-round-gate.md:49` and table `:58-67`; `sweep/results.tsv` has exactly 5 `KILLED` (A1, A3, B1, E3, C1060) and 5 `SURVIVED` (C1059, A2, B2, CKIND, E1); `sweep.log` final line `kill-rate=50%`. |
| 6 | Row 226: "10/10 pre-registered predictions held" | **holds** | `.ufo/evidence/round-16/round-gate/predictions.json`: `registered_at_utc 2026-10-20T13:39:42Z`, spec sha `e99b87eb…11c4`; pre-registration commit `e69b488` committer time `2026-10-20T10:39:59-03:00` (= 13:39:59Z) contains `predictions.json` + the spec; sweep `MUTATE_DATE 2026-10-20T13:40:15Z`; every measured verdict in `results.tsv` matches its `(predict …)` label. |
| 7 | Row 226: "projected floor interval [26,1059] confirmed at its edge (1059 survives, 1060 killed)" | **holds** | Projection pre-exists round 16: `arm-class-matrix.md:404-417` at `28aeef4` states the interval and "Projected, not measured"; note `:77-79`; `results.tsv` C1059 `SURVIVED exit=0`, C1060 `KILLED exit=1`; `sweep/evidence/C1059.out` / `C1060.out`; `defects.tsv` labels both. |
| 8 | Row 226: "guarded `env -i` suite" | **holds** | `round-gate/suite.txt` is exactly the `exec env -i PATH=… HOME=… TMPDIR=… LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=… node "$MUTANT" --selftest` command; `predictions.json` carries the same string; note `:21-27`; `sweep.log` control 60/60. |
| 9 | Row 226: "ledger leg `js-round-gate` (`--regression` cases=7)" | **holds** | `runner-regression.txt`: `REGRESSION_CASE js-round-gate: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`, `REGRESSION_SWEEP js-round-gate: … killed=5 … kill-rate=50%`, final `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: …)`; current `tools/mutate-and-run.sh` sha256 `89722ddb…5594` equals the receipt's `REGRESSION_TOOL` and `runner-sha256.txt`; ledger round-16 row at `fleet-kill-rate-ledger.md:403-412` records the same leg. |
| 10 | Row 226 sources: "S053, S052, S056, S057; `arm-class-matrix.md` §13" | **holds** | `SOURCES.md:61,62,65,66`: S052/S053/S056/S057 all `status=mined`, opened 2026-10-20, `used-by corpus/knowledge/mutation-case-kumitate-round-gate.md`; note source header line 1 cites all four; `arm-class-matrix.md` §13 exists and its round-16 errata (`:527-547`) references the measured interval/species. |
| 11 | "rows 47 and 49 above … describe six recorded cases" (`README:228-229`) | **partial** | Line 49 literally supports it: `README:49` source cell says "the six mutation-case notes". Line 47 does not: `README:47` cites only `mutation-case-kimi-census.md` and `mutation-case-kagi-census.md`, and the matrix note describes a two-case artifact (20 mutants, 16 killed/4 survived; `arm-class-matrix.md:232-243`) with "two artifacts, two languages" (`:267-268`). The operative point ("seven since round 16") is true (7 notes; `measure.py` depth 7). |
| 12 | "there are seven since round 16" (`README:229-230`) | **holds** | 7 mutation-case notes; `PROVINCE.md` round-16 append "recorded mutation legs are now seven"; `measure.py` recorded_cases 7 / seven ledger legs. |
| 13 | "Row 15's prior box-3 evidence (partial)" (`README:230`) | **holds** | `README:15` calls itself "SHONEN box 3 evidence" and limits scope: "scope honest: ONE mutant of the JS case, not the full sweep"; the row's own per-step tally includes one `NOT EXERCISED` and one `ADDITIVE-IMPROVISATION` (`corpus/knowledge/executor-test-sufficiency.md` lines 116, 120). "Partial" is a fair characterization. |
| 14 | Line anchors `143-146, 160, 190, 207` (`README:230-231`) | **holds (minor wording)** | All four locations contain the exact open/limiting text: `143-146` "Full-page box-3 sufficiency is still unearned; … adds no full-page cold-read or promotion credit"; `160` "current full-page cold-read/box3 remain debt"; `190` "current full-page cold-read/box3"; `207` "current-page cold-read/box3 remain open". Minor: `143-146` contains two sentences (five total if counted strictly), not one. |
| 15 | "are superseded by `.ufo/evidence/round-16/coldread/ledger.json`" (`README:230-233`) | **falls — blocking** | The file is absent from commit `c699c8c` and from the worktree; the lane's own `measure.py` at the commit says `ledger_present:false`, `box3_full_page:false`; the wave-1 assembler author's own report says coverage 0/51 and "w2 dir does not exist yet" (`CRLedger.md:67-69`). Details in §4. |
| 16 | "the full-page cold-read ledger (lane assertion, no independent promotion review)" (`README:232-233`) | **falls on existence; qualifier holds** | Same missing path. "No independent promotion review" is accurate; no such review is claimed anywhere in the append. |
| 17 | "No frontier item moves to Core" (`README:234`) | **holds** | The Frontier table (`README:76-87`) is unchanged by the append; F8 remains `open` at `README:85`; the round-16 PROVINCE append records seven mutation legs, not a frontier ground. |
| 18 | "F8 needs a mutant-side survivor probe tied to an independently anchored expectation. Round 16 records mutant-side probes, but against SurvivorPrep's pristine-derived expectations only." (`README:234-237`) | **holds** | Note §4 table (`:100-107`) shows pristine exit 0 vs mutant exit 1 for A2/P1, A2/P1b, B2/P6, E1/P9; probe logs exist for both sides; `probes.mjs:48` records hardcoded expected values that the pristine passes; no independently anchored oracle is claimed. The `probes.mjs:3` comment ("Runs the PRISTINE pinned blob only. Never runs a mutant") describes the harness not mutating itself; the mutant logs were produced by pointing `GATE` at a mutant copy. |

## 4. The blocking finding: cited ledger is absent

Committed-state checks (all read-only):

```
$ git ls-tree -r --name-only c699c8c | grep -i ledger
.ufo/waves/round-12/w2/SourceLedger.md
.ufo/waves/round-16/w1/CRLedger.md
corpus/knowledge/fleet-kill-rate-ledger.md
$ git ls-tree -r c699c8c .ufo/evidence/round-16/coldread
.ufo/evidence/round-16/coldread/SKILL.snapshot.md
.ufo/evidence/round-16/coldread/assemble.py
$ git --no-optional-locks status --porcelain -- .ufo/evidence/round-16/coldread/
(empty, rc 0)
$ git check-ignore -v .ufo/evidence/round-16/coldread/ledger.json
(no output, rc 1)          # not ignored; it was simply never committed
$ find .ufo/evidence/round-16 -name '*ledger*'
(no output)
```

The lane's own committed counter, re-executed from its committed bytes against the commit:

```
$ python3 measure.py --rev c699c8c --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin
exit 0
coldread: ledger_present=false, sections_total=54, sections_covered=0,
          box3_full_page=false, missing=54 sections, box3_ledger_link=false,
          box3_points=false
```

Why 54 sections: `SKILL.md` at the commit is 1,795 lines / sha256 `3d8a1edb…b7a4`; the cold-read snapshot is the 51-section pre-edit page (`SKILL.snapshot.md` sha256 `97cf436b…`). The final ledger must merge pre and post section shas; wave-1 `CRLedger.md:67-69` records its own run at `coverage: 0/51 sections covered`, exit 1, "no seat reports exist yet — expected; w2 dir does not exist yet".

I also re-ran the committed assembler on the committed wave-1 reports (pre-edit snapshot, outputs only to `/tmp`):

```
$ python3 assemble.py --skill SKILL.snapshot.md --out /tmp/.../ledger.json \
    /tmp/.../.ufo/waves/round-16/w1/*.md
exit 0
ledger written: /tmp/.../coldread/ledger.json (51 entries)
coverage: 51/51 sections covered
verdicts: 3 executed-ok, 7 verified-record, 36 gap-minor, 5 wrong-expectation
wrong-expectation starts: 58, 246, 314, 497, 921
```

This shows a wave-1-only, pre-edit ledger is not a passing "full-page" ledger: five sections carry `wrong-expectation` (e.g. CR02's live-gate exit-lattice misstatement, start 58). Wave-2 is the repair/re-read wave (round-16 lesson G6: "repaired sections re-read in wave 2"). At `c699c8c`, neither the ledger nor the repair is committed. The README's present-tense "are superseded" therefore has no committed anchor at the cited commit and violates QUALITY 2 (measured anchor) and QUALITY 9 (evidence copied into the repo before the citing commit). It may become true after wave 2 lands, but it is not true of `c699c8c`.

## 5. Related sibling-evidence findings (not additional README line defects)

- **X1 — the lane's own counter cannot credit the SHONEN box-3 link even if the ledger lands.** `measure.py:137-139` (`shonen_boxes`) returns only the `- [m] …` line; `measure.py:262` tests `BOX3_LINK in boxes[2][1]`. The SHONEN box-3 link sits on the continuation line (`SHONEN.md:10`), so `box3_ledger_link` is `false` at `c699c8c` despite the literal path being present. Consequence: `box3_points = box3_marked and box3_link and cr['box3_full_page']` (`measure.py:263-264`) can never be true for the current two-line format. This does not affect README line 226, but it affects the round's C2 "lane assertion" if the L1 counts with this tool.
- **X2 — same premature link in SHONEN.md.** `SHONEN.md:9-10` at `c699c8c` already claims "full page … ledger `.ufo/evidence/round-16/coldread/ledger.json`" and links the absent file, with the same wave-2 repair language. The README append repeats the claim; the defect is systemic, not README-only.

## 6. Residual risk / verification gaps

- I did **not** re-run the 7-leg `tools/mutate-and-run.sh --regression` (it re-sweeps six sibling gates and the round-gate leg; the committed receipt is dated `2026-10-20T13:41:49Z`, its tool sha matches the committed tool `89722ddb…5594`, and its per-leg outputs are committed). The regression claim is therefore verified from the retained receipt + pin, not by a fresh execution; an unrun check is not claimed as run.
- The wave-1 assembly above is my scratch re-execution, not a committed artifact. It used the pre-edit snapshot and wave-1 reports only; wave-2 reports may repair its five `wrong-expectation` entries. The missing-file finding at `c699c8c` is independent of that.
- The `--regression` receipt uses runner `89722ddb…`, while the sweep log uses `75ed934d…`; the README row says only "ledger leg … (`--regression` cases=7)" and does not claim the sweep ran under the later runner, so this is not a contradiction, but the two tool pins should not be conflated by a reader.
- No files under the lane root were edited except this report; no packages installed.

## 7. Commands executed (exits and key lines)

| Command | Exit | Key output |
|---|---|---|
| `git diff --numstat 28aeef4 c699c8c -- corpus/README.md` | 0 | `20	0	corpus/README.md` |
| `git diff --unified=0 28aeef4 c699c8c -- corpus/README.md` | 0 | `@@ -217,0 +218,20 @@` |
| `git show 28aeef4:…` vs `git show c699c8c:…` for lines 15,47,49,143-146,160,190,207 | 0 | all `SAME` |
| `git ls-tree -r --name-only c699c8c \| grep -i ledger` | 0 | no `coldread/ledger.json` |
| `git --no-optional-locks status --porcelain -- .ufo/evidence/round-16/coldread/` | 0 | empty |
| `git check-ignore -v .ufo/evidence/round-16/coldread/ledger.json` | 1 | not ignored |
| `python3 measure.py --rev c699c8c --repo …` | 0 | `ledger_present:false`, `sections_total:54`, `sections_covered:0`, `box3_full_page:false`, `box3_ledger_link:false`, `box3_points:false`, depth 7 |
| `python3 assemble.py --skill SKILL.snapshot.md … w1/*.md` | 0 | 51/51 covered; 5 `wrong-expectation`; ledger written to `/tmp` |
| `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277…d3e9`; 1,511 lines |
| `sha256sum` on predictions spec vs `sweep/spec.copy` | 0 | both `e99b87eb…11c4` |
| `git show c699c8c:…/runner-regression.txt` | 0 | `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`; `js-round-gate: PASS` |
| `git show c699c8c:…/results.tsv` | 0 | 5 `KILLED`, 5 `SURVIVED`; C1059 exit 0, C1060 exit 1 |
| `git show c699c8c:SHONEN.md` + `measure.py:137-139,262` | 0 | box-3 link on continuation line; `box3_ledger_link:false` |

## 8. Bottom line

The append is genuinely append-only and the case-7 row is accurate down to the pre-registration clock, the interval edge pair, the `env -i` guard, the seven-leg ledger receipt, and the four source rows. The one load-bearing defect is the cold-read supersession: it names a committed evidence path that is not in the commit, while the lane's own counter and the wave-1 assembler author both record that the ledger did not yet exist. The four "open" sentences are therefore not superseded at `c699c8c`; the wave-2 repair/re-read can supersede them later, but that is a future state.

```json
{"seat":"TameshiR16.ReadmeAppend","target":"corpus/README.md:218-237 @ c699c8c36d6e4eca4b796b81a8247904aa145ec8","verdict":"partial","blocking_findings":["README:230-233 cites .ufo/evidence/round-16/coldread/ledger.json, absent from commit and worktree; measure.py reports ledger_present=false, sections_covered=0, box3_full_page=false; CRLedger.md:67-69 records coverage 0/51 and no w2 dir"],"minor_findings":["README:228-229 six-case attribution holds for row 49 but not row 47 (two-case matrix; U4 'two artifacts, two languages')","README:230-231 'four sentences': lines 143-146 contain two sentences, five total if counted strictly"],"holds":["append-only diff 20/0 at EOF","row 226 all subclaims: 5/10, 10/10 preregistered, interval edge 1059/1060, env -i suite, js-round-gate cases=7, S052-S057 + matrix §13","cited line locations 15, 47, 49, 143-146, 160, 190, 207","row 15 partial box-3 characterization","seven recorded cases","no frontier move to Core","F8 mutant-probe restraint"]}
```
