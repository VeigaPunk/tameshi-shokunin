# PreregAudit — C1 pre-registration falsification (round 16, wave 2)

Seat: TameshiR16.PreregAudit (critic, leaf). Mode: read-only. I used `git show`, `git log`, `git diff`, `git reflog` and `git rev-parse`, plus `stat`, `find` and `sha256sum` on the live L1 sweep dir under /tmp. I made no lane edits and wrote nothing except this report.
Scratch: `/tmp/tameshi-r16w2-PreregAudit-sfro26ru/` (copies of committed files and the w1 reports from e69b488).
Revs: registration commit `e69b488f65b17bcfd41949abf7d538a77678dc26`; lane commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8`. All paths below are relative to `.ufo/evidence/round-16/round-gate/` (RG/) unless they are given in full.
Tool installs/upgrades: none.

**Verdict: HOLDS.** The pre-registration came before every round-gate mutant run. The spec, predictions, embedded leg spec and spec.copy are byte-identical. All 10 defects carry the same prediction everywhere. No defect was added or removed after registration. The 5/5 composition was declared in the registration commit. Two minor provenance defects remain in the landed runner's comments (D1), and the suite string is missing from the sweep log (D2). Neither one breaks the pre-registration.

## Falsifiers checked

| # | Falsifier (C1 falls if…) | Command(s) → exit | Key observation | Result |
|---|---|---|---|---|
| P1 | registration commit not before the sweep | `git log -1 --format='%aI %cI' e69b488` → 0; `git reflog --date=iso-strict` → 0; `git reflog show refs/remotes/origin/master` → 0; `stat` sweep dir | Original commit `f32e654` at 10:39:50-03 (13:39:50Z). `pull --rebase` produced e69b488: AD 13:39:50Z, CD 13:39:59Z. Push `origin/master@{10:40:02-03} update by push` → e69b488 at **13:40:02Z**. `predictions.json:73` `registered_at_utc 13:39:42Z`. `sweep/sweep.log:2` `MUTATE_DATE: 2026-10-20T13:40:15Z`. Sweep dir `/tmp/tameshi-r16-L1-sweep.YbD9ET` birth 10:40:15.39-03. First `mutant-A1.round-gate.mjs` mtime 10:40:15.454-03. | holds (13 s after push, 16 s after CD) |
| P2 | rebase changed the registered bytes | `git rev-parse f32e654:RG/round-gate.defects.spec e69b488:…` and the same for predictions.json → 0; `git diff --stat f32e654 e69b488` | The spec blob is `e85f252e…` at both revs and predictions is `13715cbe…` at both. The rebase diff is only `considerthese/2026-10-20.md`. | holds |
| P3 | spec ≠ spec.copy ≠ embedded leg spec | `sha256` of `git show <rev>:RG/round-gate.defects.spec` at e69b488 and c699c8c, `RG/sweep/spec.copy` at c699c8c, the live `/tmp/…YbD9ET/work/spec.copy`, and the heredoc body at `tools/mutate-and-run.sh:906-962` (c699c8c) | All five are `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4`, 4320 B. The heredoc is byte-equal to the spec file. `predictions.json:6` `spec_sha256` holds the same value. | holds |
| P4 | sweep ran a different runner from the one present at registration | `sha256` of `git show {0baf52e,e69b488,c699c8c}:tools/mutate-and-run.sh` | The runner is `75ed934d…` at parent and at e69b488, and `sweep.log:1` `MUTATE_TOOL … sha256=75ed934d…` matches. The landed runner at c699c8c is `89722ddb…` (`RG/runner-sha256.txt`). It came after the sweep and only adds the ledger leg (diff reviewed). | holds (swept runner = registration-time runner) |
| P5 | predictions.json omits a defect or carries a different prediction | python cross-check: `@defect` lines in the spec vs `predictions.json` vs `sweep/defects.tsv` vs `TABLE_ROUNDGATE` (`tools/mutate-and-run.sh:570`) vs `sweep/results.tsv` | All five sources carry the same 10 ids in the same order: A1 A3 B1 E3 C1060 = KILLED; C1059 A2 B2 CKIND E1 = SURVIVED. Id sets are equal and mismatches = `[]`. Each `desc` equals the spec's `@defect` text minus `(predict …)`. The spec has 10 `# PREDICT` lines, 5 of them KILLED. `results == predictions` → True, so 10/10 held. | holds |
| P6 | a defect was added or removed after registration | `git diff --stat e69b488 c699c8c -- RG/predictions.json RG/round-gate.defects.spec RG/suite.txt` → empty; `git --no-optional-locks status --porcelain -- RG tools/mutate-and-run.sh` → empty; `stat` worktree files | No diff. The worktree is clean. Both files have mtime 10:39:59.94-03 (the rebase checkout) and have not been touched since. `sweep.log:4` `defects=10`. | holds |
| P7 | pre-registration dropped candidates silently | `predictions.json:64-72`; w1 RGSpecB/C/D/E | Seven rejected candidates are declared with reasons at registration: RGD-B3, RGC-PASS-COUNT, RGD1-3, RGE-2, RGC-THIN-FLOOR(512) (the last replaced by C1059/C1060 per RGCritic F5). Every pruning happened before e69b488. | holds |
| P8 | 5/5 composition not declared before the sweep | `RG/round-gate.defects.spec:5` and `predictions.json:60-63` at e69b488 | `composition 5 kill-aimed / 5 hole-aimed` and `{"kill_aimed":5,"hole_aimed":5}` are both in the registration commit. Wave 1 had proposed 3+7 (`w1/RGConnector.md:173-175`). The change to 5/5 happened before registration and was declared. RGCritic F5's "composition must be stated" (`w1/RGCritic.md:48`) is satisfied. | holds |
| P9 | a round-gate mutant ran before registration | `find /tmp -maxdepth 6 \( -name 'mutant-*round-gate*' -o -name spec.copy -o -name results.tsv \) -newermt 2026-10-20` → 0 | The earliest round-gate mutant file is 10:40:15.454-03 (the L1 sweep). The only earlier js-round-gate directory is `/tmp/tameshi-r16-CR23-JMg8qF/regression/js-round-gate` (13:28:29Z). Its `sweep.log` reads `spec: line 1: unrecognized line: '@@R16_ROUNDGATE_SPEC@@'` / `MUTATE: SETUP (spec parse failed)`, and its `evidence/` dir is empty, so zero mutants ran. CR23 already recorded this near-miss at e69b488 (`w1/CR23.md:113,150`). Every w1 RG* seat states it ran no mutant (e.g. `w1/RGSpecA.md:18`, `w1/SurvivorPrep.md:9`, `w1/RGControl.md:3`). | holds (deleted dirs are unobservable) |
| P10 | committed sweep evidence ≠ what actually ran | `sha256` of the live `/tmp/…YbD9ET/{sweep.log,work/results.tsv}` and the 10 live mutant files | The live sweep.log `03e82be7…` = committed `sweep/sweep.log`. The live results.tsv `97a93776…` = committed. All 10 live mutant shas equal the `results.tsv` mutant-sha256 column. | holds |
| P11 | §13 was retro-edited after the sweep to fit the outcomes | `git log -- corpus/knowledge/arm-class-matrix.md` → 0; `git diff e69b488 c699c8c -- …` | The last edit before c699c8c was `e0c453e` (2026-10-14). The c699c8c diff only appends an "Errata — round 16" block after `:524`; no §13 line is removed or changed. At e69b488, §13 already states interval `[26, 1059]` (`:415-416`), the B2 tracked-site asymmetry (`:384,:439`) and `UFO_SRC` (`:329,:447`). | holds |
| P12 | killed verdicts came from a mechanism other than the one registered | `git show c699c8c:RG/sweep/evidence/<id>.out` FAIL lines | A1: [1,2,3,12,16,21,22,27,46,47] are parseVerdict sites. A3: [52,53] = rt1/rt2. B1: [32,45] = fcA/jFc. E3: [54] = rt3. C1060: [8] = r8. Every kill also fails [51], the nested hermeticity re-run. Each `basis` names checks that actually failed. Only the verdict was registered; this is corroboration. | holds |
| P13 | suite at registration ≠ suite in the landed ledger leg | python: `suite.txt` == `predictions.json:7` == the `regression_case_git js-round-gate` suite literal in the c699c8c runner | All three are equal. | holds |

## Defects found (fixable; none breaks pre-registration)

**D1 — false or duplicate provenance in the landed runner comments.** The file is `tools/mutate-and-run.sh` at c699c8c.
- `:101-102` says "leg 7's spec/table are L1-substituted placeholders pending the measured sweep". `:546-547` says "its spec and table are L1-substituted placeholders". Both are false at this rev: the table is filled at `:570` and the spec is embedded verbatim at `:906-962`. These are leftovers from RGLeg's draft (`w1/RGLeg.mutate-and-run.sh:96,901-905`).
- `:95-96` says "leg 7's predictions are pre-registered in corpus/knowledge/arm-class-matrix.md §13 (before any mutant run)". This names a second registration authority. §13 is the 2026-10-14 projection source. The registered artifact, with its 10 ids and verdicts, is `RG/predictions.json` plus `RG/round-gate.defects.spec` @ e69b488. `:900-904` in the same file states that correctly.
- Impacted axis: calibration (provenance honesty).
- Smallest fix: an append-style comment edit. Replace the two "placeholders" clauses with "leg 7's spec is the pre-registered spec (sha256 e99b87eb…, committed e69b488 before the sweep)". Change `:95-96` to cite `RG/predictions.json` @ e69b488, with §13 as its projection source.

**D2 — the sweep log does not bind the suite.** Runner `75ed934d` prints `MUTATE_TOOL/DATE/TARGET/SPEC` (`:436-447`) but no suite line. So the suite actually used in the sweep is not recorded verbatim in `sweep.log`. It is only implied by the `sandbox-<ID>/tmp/kumitate-round-gate-selftest-*` paths in the output tails (e.g. `sweep.log:7,16`), which match `suite.txt`.
- Impacted axis: calibration (evidence completeness).
- Fix: none required for C1. If wanted, the ledger replay (`--regression`) re-binds the suite literal, and that equals `suite.txt` (P13).

**Residual (not a defect).** Every timestamp used here is local and author-controlled: git author and committer dates, reflog, and filesystem mtime/birth. The strongest ordering anchor is the remote-tracking reflog push at 13:40:02Z, and that is a local record too. I did not query a server-side timestamp such as the GitHub push event, because the Target limits me to git only. The window is narrow: the sweep began 13 s after the push. Nothing I observed contradicts the order.

## Commands (all exit 0 unless noted)
- `git -C <lane> log -1 --format=… e69b488` / `c699c8c` / `f32e654`
- `git -C <lane> show --stat --format= e69b488`; `… c699c8c`
- `git -C <lane> merge-base --is-ancestor e69b488 c699c8c` → 0
- `git -C <lane> reflog --date=iso-strict -n 30`; `git -C <lane> reflog show refs/remotes/origin/master -n 6`
- `git -C <lane> diff --stat e69b488 c699c8c -- RG/{predictions.json,round-gate.defects.spec,suite.txt}` → empty
- `git -C <lane> diff e69b488 c699c8c -- tools/mutate-and-run.sh`; `… -- corpus/knowledge/arm-class-matrix.md`
- `git -C <lane> rev-parse f32e654:… e69b488:…`
- `git --no-optional-locks -C <lane> status --porcelain -- RG tools/mutate-and-run.sh` → empty
- `find /tmp -maxdepth 6 … -newermt 2026-10-20`; `stat -c '%w | %y'` on `/tmp/tameshi-r16-L1-sweep.YbD9ET/*`
- python `hashlib` and `re` cross-checks (P3, P5, P10, P13) over `git show` bytes
- `ls -d /tmp/tameshi-r16-CR*/*/js-round-gate` → exit 2 (glob noise). One hit: CR23 → `cat …/sweep.log`
