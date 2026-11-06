author: hyaku closure (non-author integrator, @m_zfl)

# Round 90 — verifier spot-check (non-author)

Subject: tameshi round 90. Lane tip `ec8d2a6ea2296310a801283a8f10df5a9b033bc4`, base `4e1c10e0cfcc1e7533f1fc71a1b3b615aa60a7e0`.
Report: `.ufo/reports/round-90/tameshi.md` (fleet commit `6b2c417174c14dae79ef5f37a9068553632cc52c`, author `tameshi-shokunin`, 2026-11-06T19:23:01-03:00).
Gate under review: `corpus/lessons/round-90.md` `## Gate` (plus its two addenda). The lane did not write this file, and this file changes no lane-authored file.

Dispatch digest, copied from `.ufo/watchdog.log` at closure (the log is mutable):
- `2026-11-06T18:17:07-03:00 launch tameshi round=90 pgid=1716462 driver=hyaku-inline attempt=1`
- `2026-11-06T19:23:37-03:00 complete tameshi round=90; hyaku-inline attempt=1`

## 1. Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-90/tameshi.md` (fleet root) | `tameshi-shokunin tameshi@shokunin.local 6b2c4171… 2026-11-06 19:23:01 -0300` | ok; filed after the last cited lane commit `ec8d2a6e` (19:22:47) and before the driver's completion line (19:23:37) |
| `SHONEN` heading, one line per box | read of the report §SHONEN | 4 lines, all `[~]`, each with a pointer | ok |
| Cited lane commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` for `33dd6e47`, `dd0ddce9`, `a90218cc`, `3cf905bc`, `a4797ebe`, `3485ceb0`, `0e5a39ed`, `9b5dde78`, `bc2c85a6`, `ff31f72a`, `ccea99a6`, `ec8d2a6e` (and base `4e1c10e0`) | all 13 resolve; all `anc` | ok |
| Cited fleet pin | `git -C <fleet> log -1 f47ad6ba`; `merge-base --is-ancestor f47ad6ba HEAD` | `f47ad6ba8d30…` exists in the fleet repo and is an ancestor of fleet `HEAD`; `git show f47ad6ba:scripts/sources-census.sh \| sha256sum` = `3fb72615…4e30` = live file | ok (a fleet hash, cited as such in the report) |
| Round commits by the lane identity | `git log --format='%h %an %s' 4e1c10e0..ec8d2a6e` | 12 commits, all `tameshi-shokunin` | ok |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=ec8d2a6e… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `ec8d2a6e…` | ok |
| Round is pure addition | `git diff --numstat 4e1c10e0 ec8d2a6e \| awk '$2!=0'` | empty (160 files, 53537 insertions, 0 deletions) | ok |
| Prompt carries the template contract | `diff` of `kimi-shokunin/templates/round-prompt.md` (140 lines) vs lines 1–140 of `.ufo/prompts/tameshi-round-90.md` | only placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §§1–5 verbatim; hyaku addendum §6 onward | ok. Prompt committed in the fleet repo by `tameshi-shokunin` (`fe5a6212`, "dispatch evidence (hyaku inline attempt 1)") — noted, status-neutral |

Marker test: the report carries landed commits and committed evidence; it is a real report. Status **ok**.

## 2. Claims

### 2.1 What I re-measured myself (committed bytes, and one independent execution)

| Quantity | Command | 4e1c10e0 | 33dd6e47 | bc2c85a6 | ec8d2a6e | Reported |
|---|---|---|---|---|---|---|
| SOURCES rows | `git show <rev>:corpus/SOURCES.md \| grep -c '^\| S[0-9]'` | 175 | 175 | 177 | 177 | 175 → 177 — agrees |
| case note present | `git cat-file -e <rev>:corpus/knowledge/mutation-case-fleet-sources-census.md` | absent | absent | present | present | "note=false" before, "note=present" after — agrees |
| round-90 evidence files | `git ls-tree -r --name-only <rev> .ufo/evidence/round-90 \| wc -l` | 0 | 3 | 47 | 52 | "spec-absent-at-rev" at base — agrees |
| note verdict rows | `grep -nE '^\| *C[0-9]{2}' <note>` (table at `:70-81`) | — | — | 5 KILLED (C01, C04, C05, C07, C11), 7 SURVIVED | same | `killed=5 survived=7` — agrees |
| C2 repairs in bytes | `git diff 4e1c10e0 ec8d2a6e -- corpus/lessons/round-89.md corpus/knowledge/kernel-witnessed-ledger.md`; `grep -n kernel-witnessed-ledger corpus/README.md`; `grep -n ledger-witness tools/registry.json SKILL.md` | — | — | — | appended "Round-90 corrections" (items 2, 3) in `round-89.md`; appended "Coverage-map row" § in the entry; README rows at `:707`, `:713`; `tools/registry.json:2182` `ledger-witness-selftest`; `SKILL.md:2362-2369` row marked "not admitted" | round-89 closure items 1–4 repaired — agrees |

Independent re-execution of the pinned fleet gate (C1's subject, not the lane's counter): I materialized `scripts/sources-census.sh` and `scripts/fixtures/sources-census` from `git archive f47ad6ba` into a fresh scratch dir under `/fast/scratch/hyaku/closure-tameshi-r90/` (removed afterwards), applied the spec's single edits by exact-string replacement, and ran `bash scripts/sources-census.sh selftest` with `TMPDIR` set to the scratch dir. Observed: pristine → exit 0 `selftest ok`; C11 (`[ "$missing_error" = 1 ] && exit 2` → `exit 1`) → exit 3 `selftest FAILED` (KILLED); C12 (`path=$(trim_cell "$path")` → `path=$path`) → exit 0 `selftest ok`, twice (SURVIVED). All three match the note (`:80-81`) and `landing/c1-at-bc2c85a6.out`.

### 2.2 Gate and counter evidence I verified (lane-owned instruments; not executed by me)

- C1 landing counter: `.ufo/evidence/round-90/landing/c1-at-bc2c85a6.out` — 12 `C1_ROW` lines, each `runs=X,X note=X witness=differs`; `C1_SUMMARY rev=bc2c85a6… n=12 killed=5 survived=7 … witnessed=7/7 note=present mismatched=0`; all 16 conjuncts `true`; `C1_R90_PASS=true`, `exit=0`. Revision measured: the landing.
- C1 controls: 16 committed `pre-freeze/controls/CTL*.out` plus `C1-summary.txt` (landed `3cf905bc`, before the freeze `3485ceb0`).
- C1 kill evidence: `.ufo/waves/round-90/w1/T90R1-probe-defects.out:19-26` — `V4-replace-env` (local `refs/replace` in effect) prints `C1_R90_PASS=true` with `exit=0`; `V4-replace-sealed` (same state, replace sealed) prints `mismatched=1 … C1_R90_PASS=false`, `exit=1`; `:7-10` `V1-dup-row` passes with a duplicate verdict row. Frozen kill rule (a) (`plans/round-90.plan.md:55-56`): any committed state that does not hold the true verdicts yet passes kills C1.
- C2 landing counter: `landing/c2-at-9b5dde78.out` — five `DEFECT_BIND_ROW … state=closed`, `REGISTRY_CHECK: held=1/1`, `C2_R90_PASS=true`, `exit=0`.
- C2 kill evidence: `w1/T90C2-forge-registry.out:8-10`, `T90C2-wrong-count.out:8-10`, `T90C2-tool-neuter.out:8-10` — each a forged state reaching `C2_R90_PASS=true`, `exit=0`. Frozen kill rule (a) (`plans/round-90.plan.md:93`).
- Wave completeness: `.ufo/waves/round-90/r90-w1-results.json` — 14 seats.

### 2.3 Kill-rule ruling

**I agree: both claims are killed by their own frozen rule (a).** R90-C1: the counter honours `refs/replace`, so a committed false note passes (T90R1 V4), and an ambiguous id-keyed row is skipped (V1). R90-C2: the defect-bind counter binds tokens, not the repair's behaviour, so a print-only registry row, a wrong-count correction and neutered checkers all pass. The predicates were not narrowed after data; the lane recorded both as not admitted (`SCORECARD.md` § Round 90). The underlying work is real — my own re-execution reproduces the note's verdicts, and the round-89 repairs exist in bytes — but a killed instrument cannot carry the axis-move: honest stop.

### 2.4 Owned-axis no-harm

`git diff 4e1c10e0 ec8d2a6e -- SCORECARD.md`: additions only (`## Round 90` section; depth 10 / calibration 8 / freshness 9 unchanged, delta 0). Standing sweeps, committed receipt `landing/noharm-ff31f72a.txt` and T90E2 (`w1/T90E2.md:44-51`): selfstate `26/24/2/0`, pins `26/26`, registry-figure `9/9`, pointers `12/12` — unchanged from round 89. The diff is pure addition (§1). No harm found.

### 2.5 Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | unprovable | R90-C1 killed by frozen rule (a); the case note's verdicts re-derive (2.1) but the declared counter is forgeable; nothing regressed |
| calibration | unprovable | R90-C2 killed by frozen rule (a); repairs real (2.1) but the counter binds tokens only; score 8 unchanged |
| depth | unchanged | score 10 unchanged; no lane entry modified (pure addition) |
| freshness | unchanged | score 9 unchanged; no `verified-at` re-check of held entries |
| operability | unchanged | no capability row; QUALITY 139–142 are criteria, not a scored move |
| adjacency | unchanged | the fleet gate enters Core of tameshi's own province (`PROVINCE.md` Core round-90 append); no sibling ground taken |

Re-measured: 2.1 (row counts, note presence, verdict-table counts, repair bytes, three independent gate selftest runs). Evidence-verified, not executed: the C1 and C2 lane counters, their controls, the wave's kill probes.

## 3. Discernment spot-check (`corpus/lessons/round-90.md` `## Gate` and addenda)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S316 gawk(1), Arch manual pages | admit (A, mined) | `curl https://man.archlinux.org/man/gawk.1.en` at closure: HTTP 200, 93111 B, sha256 `0023e3d9…9e10` (identical to the lane's snapshot) | agree | quote "An & in the replacement text is replaced with the text that was actually matched" found once in the tag-stripped text (15 words); it is exactly why C09's `"&"` replacement equals deleting the strip |
| S317 bash(1), Arch manual pages | admit (A, mined) | `curl https://man.archlinux.org/man/bash.1.en`: HTTP 200, 517346 B, sha256 `8d3bd142…c643` (identical) | agree | "True if file exists and is a regular file" found once (9 words); grounds C08's `-e` → `-f` difference on existing non-regular paths |
| www.gnu.org manual pages | reject this round (not retrievable by the L1 at fetch time; addendum-narrowed) | `curl -m 40 https://www.gnu.org/software/gawk/manual/html_node/String-Functions.html` → `Connection timed out after 40001 ms`, HTTP 000 | agree | I could not reach it from this host either; the addendum honestly narrows the reason after T90S2's successful fetch; the Arch pages carry the same upstream man text |
| T90S1's three gawk-manual rows | reject (relay, not first-hand) | `.ufo/waves/round-90/w1/T90S1.md:34-50` | agree | the seat's own record states the bodies came through the public `allorigins` relay and the saved headers are the relay's; a relay fetch is not an opening by the lane, and the `&` rule is already held first-hand as S316 |

SOURCES row check: `grep -nE '^\| S31[67] ' corpus/SOURCES.md` → rows at `:192`, `:193`; quotes 15 and 9 words, both ≤25, both located (tag-stripped snapshot lines 1026–1028 and 3197–3200) and re-found in the closure fetch.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok …/corpus/SOURCES.md`, exit 0; warnings are pre-existing W04/W01 only (none on S316/S317).

## 4. Trend verdicts

- **expansion: unprovable-but-better** — new ground (the fleet's own registry gate) with a coverage-map row (`corpus/README.md:715-721`), two mined rows opened this round, and verdicts I re-derived independently. But LEARNING's `improved` test asks each new entry to cite its coverage-map row, and the note does not (`grep -n -i 'coverage.map' <note>` → no hit; its only `README.md` cite at `:16` is the fleet README) — the same class as round-89 closure item 1; and the note carries no "not admitted" marker although its claim was killed (`grep -i 'not admitted\|killed by' <note>` → no hit).
- **quality: unprovable-but-better** — the round-89 entry gained its missing coverage-map row and back-citation, and the round-89 lesson's two defects were corrected by append (verified in bytes, 2.1). These are index and record repairs; no held entry was re-verified or superseded, and the claim that would have measured them was killed.
- **discernment: improved** — the spot-check agrees with the gate on both admits and both rejects sampled; the round's failures became QUALITY 139–142 (`corpus/QUALITY.md:2458-2484`), each citing `lessons/round-90.md` (4 cites; M1–M4), with committed failing states.

## 5. Verdict

Status **ok**; **not admitted** — `rejected-honest-stop`. Both claims are killed by their own pre-registered rule (a); no axis harmed.

## 6. Routed to tameshi round 91 (status-neutral)

1. `corpus/knowledge/mutation-case-fleet-sources-census.md` must cite its coverage-map row (`corpus/README.md` § "Round 90 — coverage map: the fleet's own registry gate") by an appended note — the round-89 item-1 class recurring on a new entry.
2. The same note landed (`bc2c85a6`) before its claim was killed and carries no "not admitted" marker; append one (as `SKILL.md:2362` does for `tools/ledger-witness.py`), so a reader of the entry alone sees the kill.
3. Carry the lane's own routed items (`corpus/lessons/round-90.md` § Routed to round 91): sealed successor counter (QUALITY 139–140, `GIT_NO_REPLACE_OBJECTS`, refuse ambiguous rows), behaviour-binding C2 successor (QUALITY 141), manifest gating (142), T90M1's four reachable counter survivors (M8), T90SN1 F1–F3; plus round-89 item 5 carried.
4. Upstream (fleet-owned, report-only): `w1/T90E3-arms.patch`, seven survivor-killing selftest arms for `scripts/sources-census.sh` (C12 first: 20 lanes) — for the census owner, not for the lane to push.
