# DepthCritic — round 16 wave 2: falsifying C1 "depth 6→7"

Seat: TameshiR16.DepthCritic (critic, leaf). Lane commit under attack: `c699c8c36d6e4eca4b796b81a8247904aa145ec8`; before: `28aeef498cc070c3183271b709bc79d344ff547a`.
Scratch: `/tmp/tameshi-r16w2-DepthCritic-dtIFN8` (a `git clone --no-checkout` of the lane, checked out at c699c8c; `--no-checkout` clones of kumitate/kagi/tsukuroi/mado under `fleet/`; committed runner bytes copied to `fleet/tameshi-shokunin/tools/mutate-and-run.sh`, sha256 `89722ddb…5594`). Nothing was written outside the scratch directory except this report. Tool installs: none.

**Verdict: C1 HOLDS as scored.** Under rubric D the depth score is 6 at `28aeef4` and 7 at `c699c8c`. Case 7 is a new, distinct target, inside the lane's province, pre-registered, and it replays exactly. Three caveats do not change the score: (a) the 50 % is set by the case's composition; (b) the case adds no new owner lane; (c) rubric D itself can be gamed. The landing also has four small documentation/instrument defects (§5), which can be fixed without touching the score.

## 1. Re-measurement (executed)

All commands ran from `/tmp/…/clone` with `--repo` pointing at the clone. Every command below exited 0.

| command | 28aeef4 | c699c8c |
|---|---|---|
| `python3 .ufo/evidence/round-16/measure.py --rev R --repo $S/clone` | `recorded_cases 6`, `depth_score 6`, legs kimi…claims | `recorded_cases 7`, `depth_score 7`, + `js-round-gate` |
| command D (`SCORECARD.md:73`, verbatim) | `recorded_cases=6 depth_score=6` | `recorded_cases=7 depth_score=7` |
| `.ufo/evidence/round-12/measure.py --rev R` | `recorded_cases 6`, `unique_recorded_gates 6` | `7`, `7` |
| `.ufo/evidence/round-13/measure.py --rev R` | `6`, `6` | `7`, `7` |
| `measure.py --selftest` | — | `MEASURE_SELFTEST: 33/33 pass` |

The new counted line is `tools/mutate-and-run.sh:91`: `#   js-round-gate  kumitate-shokunin/scripts/round-gate.mjs  5/10 (50 %)`.

Consistency at c699c8c: the leg names in the comment ledger match the `regression_case_git` calls and the selftest `lent` tuples (both `diff`s are empty), and `local nlegs=7` (`:1225`). The embedded heredoc spec (`:906-959`) has sha256 `e99b87eb…11c4`. That equals `.ufo/evidence/round-16/round-gate/round-gate.defects.spec` at both e69b488 and c699c8c.

## 2. Independent replay of leg 7 (executed)

- Pin: `git show 364f1d5…:scripts/round-gate.mjs | sha256sum` → `f890e277…d3e9`, 1511 lines. The git blob is `1f7d623e…` at 364f1d5, 175de6ba and kumitate HEAD 1770305, so the note's claim at `mutation-case-kumitate-round-gate.md:17-18` holds. kumitate `status --porcelain` → 0 lines.
- Command: `mutate-and-run.sh --target rg.mjs --defects rg.spec --suite "$(suite.txt)" --workdir leg7 --label js-round-gate`, run with the committed runner `89722ddb…` → **exit 0**.
- Result: `CONTROL: GREEN`. A1, A3, B1, E3 and C1060 KILLED (exit 1); C1059, A2, B2, CKIND and E1 SURVIVED (exit 0). `MUTATE_RESTORE: OK`, `MUTATE: DONE (… killed=5 survived=5 inconclusive=0 kill-rate=50%)`.
- This matches `TABLE_ROUNDGATE` (`:570`) and `sweep/results.tsv` row for row. Wall time was 40 s.
- Not run: the full 7-leg `--regression`. It needs more than 60 s, and leaf seats may not run background jobs. The committed receipt `.ufo/evidence/round-16/round-gate/runner-regression.txt` shows `REGRESSION: PASS (cases=7 passed=7 …)`. RerunRegression owns that re-execution.

## 3. Attacks

### 3a. Independence (third kumitate gate, same author as cases 1 and 6) — does not break C1

- **Same author: confirmed.** `git log` per file in kumitate shows the same committer identities on all three files: `kumitate-shokunin <kumitate@shokunin.local>` (round-gate 364f1d5, claims-check e404431, kimi-census 1a8eed5), plus `Joao Pedro Veiga` in earlier history. Owner lanes per ledger path: before `{kumitate 2, kagi 2, tsukuroi 1, mado 1}`, after `{kumitate 3, kagi 2, tsukuroi 1, mado 1}`. The case adds **no new owner lane**.
- **The independence criterion that does exist is met.** The rubric has no author or lane clause: "One point per recorded mutation case listed in the tool's pinned replay ledger" (`SCORECARD.md:66`). The only depth-independence precedent is round 12: "reanalysis of the same bash target is depth within a case, not a new independent case" (`SCORECARD.md:288-289`). It applies to the *same target*. round-gate.mjs is a distinct path (`unique_recorded_gates` 6→7 under both the round-12 and round-13 measures). It imports only `node:` builtins (`round-gate.mjs:130-137`), so it shares no code with the kimi-census or claims-check legs. It also has its own suite (`--selftest`, 60 checks).
- **Instrument regression (fixable).** The round-12/13 measures reported `unique_recorded_gates`, which `SCORECARD.md:314-315,369` calls a "reported guardrail". The round-16 counter `.ufo/evidence/round-16/measure.py:253-284` no longer emits it, so a future duplicate leg would pass the round-16 command without any signal. This does not matter at c699c8c (7 = 7).

### 3b. Province (no opt-in) — holds

- `PROVINCE.md:7-8` lists `kumitate-shokunin/scripts/*` as primary surfaces the lane owns. `:16-17` allows read-only probes. My replay used a git-materialized copy; kumitate's tree stayed porcelain-clean.
- No opt-in exists: RGCritic O12 reports 0 `tameshi` matches in kumitate (I did not re-run this). Case 6 had the same status: claims-check was a queue row (`fleet-suite-census.md:285`), was swept in r8, and its note `mutation-case-kumitate-claims.md:1-30` records no opt-in. It is counted in D. Case 5 records its missing opt-in as U4 (`mutation-case-kagi-checklist.md:10-12,354-355`). Case 7 follows the precedent already counted.
- The "drains only under a fresh opt-in" rule (`service-optin-protocol.md:26-30`) is scoped to the service queue "at round-7 dispatch". The province grant at `PROVINCE.md:7-8` is the stronger authority for kumitate `scripts/*`.
- Wording tension (minor, see §5 D4): the note says it "does not drain the service queue" (`mutation-case-kumitate-round-gate.md:12-13`). But the ledger append (`fleet-kill-rate-ledger.md:405-406`) says the queue row "said `unmeasured`. It is measured now", and calls it the "§5 queue". In that file the queue is §3 (`:98`, row `:109`); §5 is the queue in `fleet-suite-census.md`.

### 3c. Is 50 % with hole-aimed composition a legitimate recorded case? — yes for D; the rate is not representative

- **Precedent.** Hole-aimed composition is how the lane has run sweeps since case 3. Case 6 was "6 kill-aimed + 4 hole-aimed" (`mutation-case-kumitate-claims.md:72-75`), and its comparison table (`:267`) lists 6+4 and 4+6 for cases 3 and 4. D counts recorded cases, not rates (a 0/10 case would count too).
- **Pre-registration ordering.** The spec was committed at e69b488 (committer 2026-10-20T10:39:59-03:00, on `origin/master`), 16 s before the sweep's `MUTATE_DATE 13:40:15Z`. The spec sha is unchanged through c699c8c, and `predictions.json` is byte-identical at both commits (`bb344eee…`). Wave-1 seats that touched round-gate say no mutant was run: SurvivorPrep `:9`, RGMatrix `:7`, RGSpecA `:18,83`, RGSpecB `:5`, RGSource1 `:7`, RGConnector `:4`. RGCritic O13 found no early `results.tsv` or `spec.copy` as of about 10:26. [INFERENCE] Commit dates are set by the author; I have no local push-time evidence, so the ordering rests on these timestamps plus the seat reports.
- **Counterexample on what the rate means (executed).** I took a blind, deterministic sample: one operator flip per line (`===`↔`!==`, `<`/`<=`, `&&`↔`||`, `true`↔`false`), restricted to non-comment gate-code lines 139-688 where the line occurs once. That gave 97 candidates on 77 lines. I took the first 16 by `sha256('r16w2-DepthCritic|line|op')` (script `blind.py`) and ran them with the committed runner and the same guarded suite, in two batches, both exit 0:
  - batch 0: 7/8 killed; X436 survived.
  - batch 1: 6/8 killed; X220 and X477 survived.
  - Total **13/16 (81 %)**. Five of the kills (X268, X269, X270, X272, X284; exit 2/64 in about 20 ms) only break argument parsing for `--selftest`. Without them the rate is **8/11 (73 %)**.
  - X477 (REPORT_UNTRACKED severity flip at `:477`) survived. This is independent confirmation of the wave-1 erratum that `:477` is an arm no fixture reaches (`arm-class-matrix.md` round-16 errata).
- **Reading.** The recorded 5/10 is set by the 5+5 design. A blind sample of the same suite kills 73-81 %. The note already says this in its limits section (`mutation-case-kumitate-round-gate.md:128-130`), so the case does not misreport itself. But the counted ledger line `:91` shows `5/10 (50 %)` with no composition qualifier, as the lines for cases 3, 4 and 6 do. That is a tradeoff the judge should see, not a defect of C1.
- **CKIND sits in the denominator.** The note says it is "equivalent for gate behaviour" (`:87-92`). Conventional mutation scoring drops equivalent mutants, which would give 5/9. The lane counts it because it changes what the suite's own meta-check reads. This is defensible, but it is a choice.
- **C1059 has no off-suite witness yet at c699c8c.** Its non-equivalence is deferred to wave-2 seat C1059Probe (note `:106`). The survivor-evidence part of the case is incomplete at the landing commit. This does not affect D.

## 4. Rubric D can be gamed (tradeoff for the canonical judge)

I appended one line, `#   js-fake-leg   nowhere/fake.mjs   0/1 (0 %)`, to a /tmp copy of the c699c8c runner (`game.sh`):

- Command D → `GAMED recorded_cases=8 depth_score=8`.
- `bash game.sh --selftest` → exit 0, `MUTATE_SELFTEST: 81/81 pass`.

D counts comment lines, and nothing in the runner's selftest ties those lines to an embedded spec, table or `regression_case_git` call. C1 does not exploit this: at c699c8c, comment, `lent` and regression legs agree (§1). Smallest guard: have measure.py (or the runner selftest) require comment-leg names == `lent` names == `regression_case_git` names, and report `unique_recorded_gates`.

## 5. Fixable defects in the landing (do not change the score)

| # | Where (c699c8c) | Defect | Smallest correction |
|---|---|---|---|
| D1 | `tools/mutate-and-run.sh:101-102` and `:546-548` | The comments still say leg 7's "spec/table are L1-substituted placeholders pending the measured sweep". The heredoc comment at `:899-903` says the opposite: swept, 5/10, spec verbatim. This is false provenance left over from the RGLeg draft (`.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh:96,901-903`). | Replace both comments with "leg 7: pre-registered spec e99b87eb… (e69b488), measured table 2026-10-20T13:40:15Z". |
| D2 | `tools/mutate-and-run.sh:95-96` | Says leg 7's predictions "are pre-registered in corpus/knowledge/arm-class-matrix.md §13". §13 is the projection source; the pre-registration is the spec file at e69b488 (as `:900-902` correctly says). | Cite the spec path and e69b488 here, with §13 as the source. |
| D3 | `.ufo/evidence/round-16/measure.py:253-284` | Drops the `unique_recorded_gates` guardrail that the round-12/13 measures printed (`SCORECARD.md:314-315,369`). | Emit `unique_recorded_gates` (and optionally a per-owner-lane histogram). |
| D4 | `corpus/knowledge/fleet-kill-rate-ledger.md:405-406`; `mutation-case-kumitate-round-gate.md:12-13` | Calls the queue the "§5 queue" (it is §3, `:98`). Also says the case "does not drain the service queue" while superseding a queue row. | Change "§5" to "§3", and say "supersedes the §3 queue cell (as rows 5/6 did, `:280`); not a service-form engagement". |

## 6. Commands, key output

```
measure.py --rev 28aeef4            exit 0  recorded_cases 6 depth_score 6
measure.py --rev c699c8c…           exit 0  recorded_cases 7 depth_score 7
command D @28aeef4 / @c699c8c       exit 0  recorded_cases=6 depth_score=6 / recorded_cases=7 depth_score=7
round-12|13 measure.py @ both       exit 0  unique_recorded_gates 6 → 7
measure.py --selftest               MEASURE_SELFTEST: 33/33 pass
leg-7 replay (run mode)             exit 0  MUTATE: DONE (killed=5 survived=5 inconclusive=0 kill-rate=50%), RESTORE OK
blind0.spec / blind1.spec           exit 0  7/8, 6/8 killed (13/16; 8/11 excluding argparse crashes)
game.sh: command D / --selftest     depth_score=8 / MUTATE_SELFTEST: 81/81 pass
kumitate status --porcelain         0 lines
```

**One-line verdict:** C1 depth 6→7 **holds**. It is a distinct target inside the province, pre-registered and replayed exactly. Independence holds against the rubric and the round-12 criterion, but the case adds no new owner lane. The 50 % is set by composition; a blind sample kills 73-81 %. Defects D1-D4 and the gameability of rubric D are fixable and do not change the score.
