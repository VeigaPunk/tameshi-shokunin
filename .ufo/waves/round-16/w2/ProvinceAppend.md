# ProvinceAppend — round-16 Core append, statement by statement

Seat: ProvinceAppend (reviewer, leaf — no delegation, no background jobs).
Target: `PROVINCE.md` @ `c699c8c36d6e4eca4b796b81a8247904aa145ec8`, section
`## Core — round 16 append (2026-10-20)` (`PROVINCE.md:49-66`), against the
repo and sibling evidence; append-only base `28aeef4`.
Page sha verified: `git show c699c8c:SKILL.md | sha256sum` →
`3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4`, exit 0
(matches the assignment). This is not an RR cold-read seat, so no section
range was imposed and no fenced JSON block is emitted.

Scratch: `/tmp/tameshi-r16w2-ProvinceAppend-04YnIX` (old/new prefixes),
`/tmp/tameshi-r16w2-ProvinceAppend-run` (committed tool copy, selftest),
`/tmp/tameshi-r16w2-ProvinceAppend-reg` (fleet mirror of symlinks, regression).
Only write: this report. Tools installed: none.
Head state: lane HEAD `c699c8c`; the worktree `PROVINCE.md` sha256
`c0845697…7fd356e1` equals `git show c699c8c:PROVINCE.md` (wave-2 sibling edits
exist elsewhere in the tree, not in this file).

## Verdict

**PARTIAL (non-blocking)** — every enumerated structural/factual claim holds
(seven legs, rev, blob sha, `:85-91`, kumitate seven gates, tsukuroi
self-service, template path, append-only), but the unqualified sentence
“only the round-6 mado run was a service run” (`PROVINCE.md:63-64`) is
contradicted by the lane’s own round-8 records; it holds only under the
round-5/6 scope its context implies (or under “only recorded opt-in”).

## Statement ledger

| # | Statement (`PROVINCE.md`) | Verdict | Decisive evidence |
|---|---|---|---|
| 1 | Heading + date; “lines 1-47 are unchanged” (`:49-51`) | **holds** | `git diff --numstat 28aeef4 c699c8c -- PROVINCE.md` → `19 0 PROVINCE.md`; old file 47 lines, new 66; `cmp` of `git show 28aeef4:PROVINCE.md` vs the first 47 lines of the new file → exit 0, byte-identical |
| 2 | Mutation legs are **seven**, not six (`:51-52`) | **holds** | `tools/mutate-and-run.sh:81` header “r10-2 six legs; **r16 seven**”; leg lines `:85-91`; leg array `:1660-1668` has 7 entries; `--selftest` → `PASS embedded leg specs: seven files written`; independent `--regression` → `cases=7 passed=7` |
| 3 | The seventh is kumitate `scripts/round-gate.mjs` (`:52-53`) | **holds** | leg array entry `js-round-gate:js-round-gate.spec:TABLE_ROUNDGATE:10:5` (`:1667`); `regression_case_git js-round-gate` (`:1219-1222`); `REGRESSION_PIN js-round-gate … path=scripts/round-gate.mjs` |
| 4 | rev `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` (`:53`) | **holds** | `git -C kumitate-shokunin cat-file -p 364f1d5^{commit}` exit 0 (commit dated 2026-10-13 22:49:20 -0300); the same rev appears in the regression pin and the case note (`mutation-case-kumitate-round-gate.md:1,17`) |
| 5 | blob sha256 `f890e277…d3e9` (`:53-54`) | **holds** | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`; 80,415 B, 1,511 lines; kumitate HEAD blob sha `1f7d623e…` (git SHA-1) is the same object, content sha256 unchanged |
| 6 | ledger leg `js-round-gate` (`:54-55`) | **holds** | leg name at `:91`, `:1219`, `:1667`; independent replay `REGRESSION_CASE js-round-gate: PASS … defects=10`, `match=10/10`, killed `5/10` |
| 7 | probed read-only as a kumitate `scripts/*` primary surface (`:55`) | **holds** | case note `mutation-case-kumitate-round-gate.md:7-13` (byte copy from the git object store; `git status --porcelain` 0 before/after); tool header `:103-113` (“the fleet trees are never written”); kumitate `status --porcelain` → 0 after my replay |
| 8 | “not a service run and needed no opt-in” (`:56`) | **holds** (caveat) | case note `:10-13` (“No owner opt-in exists or was needed … This is not a service run”); no kumitate opt-in recorded (`grep -rIn tameshi kumitate-shokunin/` → 0); RGCritic O12 records the same and the queue-row precedent. Caveat: round-gate **is** a census queue row (RGCritic O11); the protocol’s drain rule is scoped “at round-7 dispatch” (`service-optin-protocol.md:26-30`), so the round-16 tameshi-owned read-only case is not a service engagement |
| 9 | `tools/mutate-and-run.sh:84-89` is the round-1 six-leg anchor (`:56-57`) | **holds** (revision-relative) | `git show c7986cd:tools/mutate-and-run.sh \| nl -ba` → six leg lines exactly `84-89` (js-kimi-census … js-claims-check), `# Sources:` at 90. At `c699c8c` the same range is the `# expectation:` comment + five legs, so the range is only true of the round-1 blob; the append’s “round-1” qualifier and the next clause make it recoverable, but no rev is named |
| 10 | seven-leg list now sits at `:85-91` (`:57`) | **holds** | `git show c699c8c:tools/mutate-and-run.sh \| nl -ba \| sed -n '84,92p'` → leg lines `85` (js-kimi-census) through `91` (js-round-gate), `# Sources:` at 92. Exactly 7 lines |
| 11 | kumitate carries **seven** gates; `sources-check.mjs` landed in `1a8eed5` (2026-10-19), after the line-8 survey (`:61-62`) | **holds** | kumitate `SKILL.md:589-590` “All seven are gates”; registry rows `:599-605` (cite-check, surface-probe, round-gate, proxy-check, claims-check, kimi-census, sources-check); `git log --reverse -- scripts/sources-check.mjs` first commit `1a8eed5 2026-10-19`; `git ls-tree 1a8eed5^ scripts/` → 6 files, HEAD → 7; the line-8 survey is dated 2026-10-14 (`gates-survey-kumitate.md:1-3`, “six hermetic suites”). Both named wave-1 seats flagged the correction (Overlap1 F1, ProvinceBox4 F2) |
| 12 | The round-5 tsukuroi engagement was self-service (`:63`) | **holds** | `tsukuroi-shokunin/plans/round-5.plan.md:3-11` (the lane applies tameshi’s tool to its **own** census gate, read-only tool, copies in `/tmp`, lane measures its own kill-rate); `service-optin-protocol.md:36` (self-service → tsukuroi r5) |
| 13 | “only the round-6 mado run was a service run” (`:63-64`) | **partial — falls as written; holds scoped** | Holds for the round-5/6 pair: `service-optin-protocol.md:36-37`; `mutation-case-mado-verify.md:3-11` (“the *service round*”, “mado-shokunin opted in”); `mado-shokunin/corpus/knowledge/gate-mutation-proof.md:4-19` (“tameshi’s read-only sweep”). **Falls unqualified**: the lane’s own round-8 records call two further sweeps service-form — `mutation-case-kagi-checklist.md:1,5-9` (“service sweep”, “third engagement … form = **service**”; its opt-in is U4 at `:354-355`), `fleet-kill-rate-ledger.md:272` (“Two independent sweeps ran this round — service form”), `plans/round-8-record-draft.md:169-170` (“third service engagement, form = service”). The sentence needs “of the round-5/6 entries” or “the only recorded opt-in” |
| 14 | line 26’s template path resolves as `/home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md:6-19` (`:65-66`) | **holds** | `ls -l` → 651 B; `git -C kimi-shokunin ls-files templates/mint/PROVINCE.md` → tracked; `nl -ba` → `## Core` at 6, `## Frontier` at 11, `## Adjacent` at 16, line 19 ends the Adjacent paragraph. `kimi-shokunin` is **not** under the fleet root (`ls /home/vgpnk/Projects/shokunin/kimi-shokunin` → ENOENT), which is exactly why the absolute path is the useful correction |
| 15 | Append-only discipline (`git diff 28aeef4 c699c8c -- PROVINCE.md`) | **holds** | `--numstat` `19 0`; `git diff -U0` shows only `+` lines (48-66), no `-` lines; the first 47 lines are byte-identical (cmp exit 0) |

## Commands run (exits and key lines)

| command | exit | key output |
|---|---|---|
| `git -C tameshi-shokunin show c699c8c:SKILL.md \| sha256sum` | 0 | `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4  -` |
| `git -C tameshi-shokunin diff --numstat 28aeef4 c699c8c -- PROVINCE.md` | 0 | `19	0	PROVINCE.md` |
| `git show 28aeef4:PROVINCE.md > old; git show c699c8c:PROVINCE.md \| head -47 > new47; cmp old new47` | 0 | silent; wc: old 47, new 66; `CMP: lines 1-47 byte-identical` |
| `git -C kumitate-shokunin cat-file -p 364f1d5^{commit}` | 0 | commit exists, author/committer 2026-10-13 22:49:20 -0300 |
| `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| sha256sum` | 0 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -` |
| `… \| wc -c` / `… \| wc -l` | 0 | `80415` / `1511` |
| `git -C kumitate-shokunin rev-parse 364f1d5:scripts/round-gate.mjs` | 0 | `1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3` (git blob id; matches the note’s short `1f7d623e`) |
| `git show c7986cd:tools/mutate-and-run.sh \| nl -ba \| sed -n '80,92p'` | 0 | six leg lines at `84-89`; `# Sources:` at 90 |
| `git show c699c8c:tools/mutate-and-run.sh \| nl -ba \| sed -n '78,95p'` | 0 | header `:81` “r10-2 six legs; **r16 seven**”; legs `85-91`; `# Sources:` 92 |
| `git show c699c8c:tools/mutate-and-run.sh \| grep -n 'js-round-gate'` | 0 | `91`, `1219-1222`, `1667`, spec `905`, table `570` |
| `bash /tmp/tameshi-r16w2-ProvinceAppend-run/mutate-and-run.sh --selftest` | 0 | `PASS embedded leg specs: seven files written`; `PASS embedded leg js-round-gate: spec and recorded table agree`; `MUTATE_SELFTEST: 81/81 pass`; `VERDICT: PASS` (5.3 s) |
| `bash /tmp/tameshi-r16w2-ProvinceAppend-reg/fleet/tameshi-shokunin/tools/mutate-and-run.sh --regression` | 0 | `REGRESSION_TOOL … sha256=89722ddb…`; `REGRESSION_PIN js-round-gate … rev=364f1d5… sha256=f890e277…`; `REGRESSION_SWEEP js-round-gate … killed=5 survived=5 kill-rate=50%`; `REGRESSION_TABLE … match=10/10 … flips=0`; `REGRESSION_CASE js-round-gate: PASS`; `REGRESSION: PASS (cases=7 passed=7)` (131 s) |
| `git -C kumitate-shokunin log --reverse --format='%h %ad' --date=short -- scripts/sources-check.mjs \| head -1` | 0 | `1a8eed5 2026-10-19` |
| `git -C kumitate-shokunin ls-tree --name-only 1a8eed5^ scripts/` | 0 | six files (cite-check, claims-check, kimi-census, proxy-check, round-gate, surface-probe) |
| `grep -n 'All seven' kumitate-shokunin/SKILL.md` | 0 | `589:… All seven are` (continues `gates` on 590) |
| `grep -nE '^\| (cite-check\|surface-probe\|round-gate\|proxy-check\|claims-check\|kimi-census\|sources-check) ' kumitate-shokunin/SKILL.md` | 0 | `599-605`, seven rows, `sources-check` at 605 |
| `git show c699c8c:corpus/knowledge/gates-survey-kumitate.md \| nl -ba \| sed -n '1,3p'` | 0 | “`# Gates survey — kumitate-shokunin's six hermetic suites`”, “Survey date: 2026-10-14” |
| `nl -ba tsukuroi-shokunin/plans/round-5.plan.md \| sed -n '3,11p'` | 0 | “tameshi's mutate-and-run.sh is applied to tsukuroi's OWN census gate … copies in /tmp … the lane measures its own suite's kill-rate” |
| `git show c699c8c:corpus/knowledge/service-optin-protocol.md \| nl -ba \| sed -n '32,38p'` | 0 | `:36` self-service → tsukuroi r5; `:37` service → mado r6 |
| `git show c699c8c:corpus/knowledge/mutation-case-mado-verify.md \| sed -n '3,11p'` | 0 | “the *service round*”, “mado-shokunin opted in” |
| `sed -n '4,19p' mado-shokunin/corpus/knowledge/gate-mutation-proof.md` | 0 | “tameshi's read-only sweep”, “tameshi's sweep ran `597e1419…`, this lane's re-run …” |
| `git show c699c8c:corpus/knowledge/mutation-case-kagi-checklist.md \| nl -ba \| sed -n '1,12p'` | 0 | title “service sweep”; “third engagement … form = **service**”; “no kagi-side opt-in is recorded … whether the owner asked is U4” |
| `git show c699c8c:corpus/knowledge/mutation-case-kagi-checklist.md \| nl -ba \| sed -n '354,355p'` | 0 | `U4 — provenance: no kagi-side opt-in is recorded … the dispatch is the record, and the owner's intent is U` |
| `git show c699c8c:corpus/knowledge/fleet-kill-rate-ledger.md \| nl -ba \| sed -n '272p'` | 0 | “Two independent sweeps ran this round — service form …” |
| `git show c699c8c:plans/round-8-record-draft.md \| nl -ba \| sed -n '169,170p'` | 0 | “the fifth fleet mutation case (third service engagement, form = service)” |
| `git show c699c8c:corpus/knowledge/mutation-case-kumitate-round-gate.md \| nl -ba \| sed -n '1,13p'` | 0 | source line with rev/sha; “No owner opt-in exists or was needed … This is not a service run and does not drain the service queue” |
| `ls -l /home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md` | 0 | `-rw-r--r-- 651 …` |
| `git -C kimi-shokunin ls-files templates/mint/PROVINCE.md` | 0 | `templates/mint/PROVINCE.md` |
| `nl -ba /home/vgpnk/Projects/kimi-shokunin/templates/mint/PROVINCE.md \| sed -n '6p;11p;16p;19p'` | 0 | `## Core`, `## Frontier`, `## Adjacent`, final Adjacent line |
| `git -C kumitate-shokunin status --porcelain \| wc -l` (before/after replay) | 0 | `0` / `0`; kagi, tsukuroi, mado also `0` after |
| `git show c699c8c:.ufo/evidence/round-16/round-gate/runner-regression.txt \| nl -ba \| grep -E 'REGRESSION_TOOL\|REGRESSION: PASS\|js-round-gate'` | 0 | `:1` tool sha `89722ddb…`; `:35` pin; `:39` case PASS; `:40` `REGRESSION: PASS (cases=7 passed=7)` |
| `git show c699c8c:.ufo/evidence/round-16/round-gate/runner-selftest.txt \| nl -ba \| grep …` | 0 | `:71` seven files; `:78` js-round-gate agree; `:82` `81/81 pass` |

## Findings

**F1 (minor, actionable) — the “only … service run” sentence is over-broad.**
`PROVINCE.md:63-64` says “only the round-6 mado run was a service run”. That is
true of the round-5/6 pair the bullet corrects, and true if “service” means a
recorded opt-in engagement (mado’s opt-in is in its round-6 plan; the r8 kagi
note’s opt-in is U4). It is false as unqualified English: the lane’s own
round-8 records label the kagi checklist sweep “service sweep” / “third
engagement … form = **service**” (`mutation-case-kagi-checklist.md:1,5-9`), call
the two r8 sweeps “service form” (`fleet-kill-rate-ledger.md:272`), and the
round-8 record says “third service engagement, form = service”
(`plans/round-8-record-draft.md:169-170`). Suggested repair: “of the round-5/6
entries, only the round-6 mado run was a service engagement” or “the only
recorded opt-in service engagement”. This is a wording/calibration defect, not
a structural one; the cited protocol table (`:36-37`) supports the pair
classification itself.

**F2 (residual, not a statement of the append) — line 8 is corrected only in
part.** Overlap1 F1 (the round-16 wave-1 source named in the append) says the
line-8 parenthetical is “wrong twice”: the count (six → seven) and “mutation
controls” (tameshi’s legs, not kumitate’s gates). The append fixes the count and
leaves the “mutation controls” wording uncorrected at `PROVINCE.md:8-9`. If the
bullet’s purpose was a full correction of line 8, it is incomplete; if only the
count was in scope, the bullet should say so.

**F3 (note, no action required) — `:84-89` is revision-relative.** It is exactly
the six-leg list at the round-1 blob `c7986cd` (verified), but at `c699c8c` line
84 is the `# expectation:` comment and 85-89 are five of the seven legs. The
append’s “round-1” qualifier plus “the seven-leg list now sits at `:85-91`”
makes the shift recoverable; pinning `c7986cd` would make the first range
self-resolving.

**F4 (note) — survey attribution.** “after the line-8 survey (Overlap1,
ProvinceBox4)” (`:61-62`) names the round-16 seats that re-checked the line-8
claim (Overlap1 F1, ProvinceBox4 F2). The survey itself is the 2026-10-14
tameshi survey (`gates-survey-kumitate.md:1-3`). Read as credit for the finding,
the parenthetical holds; read as survey authorship, it is imprecise.

## Residual risk and verification gaps

- The independent `--regression` ran the committed tool bytes from
  `c699c8c` in a `/tmp` fleet mirror whose sibling repos are symlinks to the
  live trees (read-only; git object store). The lane’s recorded run
  (`runner-regression.txt:1`) used the same tool sha `89722ddb…` and the live
  fleet root, and reports the same `cases=7 passed=7` shape. Sibling worktrees
  were `status --porcelain` 0 before and after my replay.
- I did not separately run `node round-gate.mjs --selftest` (the 60-check
  target suite) in isolation; the ledger leg replays it under the guarded
  `env -i` command and the regression’s `js-round-gate` case passed at
  `match=10/10`. The append does not claim the 60/60 number, so this is a
  corroboration gap, not a statement gap.
- The lane worktree has wave-2 edits in flight (other seats); I read
  `PROVINCE.md` and `tools/mutate-and-run.sh` at `c699c8c`, and verified the
  worktree `PROVINCE.md` sha equals the commit. No lane file was edited.
- I did not install or update any tool; no subagents, no background jobs.

**One-line verdict:** partial (non-blocking) — all structural/factual claims of
the round-16 append hold and the append-only diff is exact, but the unqualified
“only the round-6 mado run was a service run” fails against the lane’s own r8
service-form records; scope it to the round-5/6 pair (or to “recorded opt-in”)
and the section is clean.
